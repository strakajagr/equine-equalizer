"""
Daily report generator — runs every strategy in registry against current-day races.

Pre-race report: every strategy's picks + every raw-layer top-N + per-strategy
historical context. Tony reads → Tony decides → Tony bets.

Post-race report: actual results + per-strategy P&L + cumulative running P&L.
"""
from __future__ import annotations
from dataclasses import asdict
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional
from collections import defaultdict

from services.strategy_harness import (
    StrategyHarness, RacePredictionLoader, race_context_from_predictions,
    BetRecommendation, RacePredictions, RaceContext,
)
from services.strategy_registry import get_registry, registry_size_by_category


class DailyReportGenerator:
    """Builds pre-race and post-race daily reports across the full strategy registry."""

    def __init__(self, conn):
        self.conn = conn
        self.strategies = get_registry()
        self.harness = StrategyHarness(self.strategies)

    # ── PRE-RACE REPORT ──

    def generate_pre_race_report(self, race_date: date) -> Dict[str, Any]:
        """For every race on race_date, run every strategy and assemble report."""
        loader = RacePredictionLoader(self.conn)
        races_meta = self._get_races(race_date)

        report = {
            'race_date': str(race_date),
            'generated_at': datetime.utcnow().isoformat(),
            'strategy_count': len(self.strategies),
            'strategy_categories': registry_size_by_category(),
            'race_count': len(races_meta),
            'historical_context': self._historical_context_per_strategy(race_date),
            'races': [],
            'multi_leg_recommendations': [],
            'errors': [],
        }

        # Group races by card (track) for multi-leg processing
        cards: Dict[str, List[Dict]] = defaultdict(list)
        for r in races_meta:
            cards[r['track_code']].append(r)

        # Single-race recommendations
        for track_code, card_races in cards.items():
            for r in card_races:
                race_id = r['race_id']
                preds_general = loader.load(race_id, 'general')
                if not preds_general:
                    continue
                ctx = race_context_from_predictions(preds_general)

                # Per-style loading: only for strategies that need non-general
                style_preds_cache = {'general': preds_general}
                for s in self.strategies:
                    if s.style != 'general' and s.style not in style_preds_cache:
                        style_preds_cache[s.style] = loader.load(race_id, s.style)

                # Run all single-race strategies (each gets its style's predictions)
                strategy_recs: Dict[str, Optional[Dict]] = {}
                for s in self.strategies:
                    if s.is_multi_leg: continue
                    rp = style_preds_cache.get(s.style) or preds_general
                    if not rp.horses:
                        strategy_recs[s.name] = None
                        continue
                    try:
                        rec = s.recommend(rp, ctx)
                    except Exception as e:
                        report['errors'].append({
                            'strategy': s.name, 'race_id': race_id,
                            'error': f'{type(e).__name__}: {str(e)[:200]}',
                        })
                        rec = None
                    strategy_recs[s.name] = asdict(rec) if rec else None

                # Skip stats + consensus signals computed across single-race strategies
                single_race_strategies = [s for s in self.strategies if not s.is_multi_leg]
                skip_stats = self._compute_skip_stats(strategy_recs, len(single_race_strategies))
                consensus = self._compute_consensus_signals(
                    strategy_recs, preds_general, skip_stats['skip_rate']
                )

                # Per-race section
                report['races'].append({
                    'race_id': str(race_id),
                    'track': track_code,
                    'race_number': r['race_number'],
                    'race_name': r.get('race_name'),
                    'post_time': str(r['post_time']) if r.get('post_time') else None,
                    'field_size': r.get('field_size'),
                    'distance_furlongs': float(r['distance_furlongs']) if r.get('distance_furlongs') else None,
                    'surface': r.get('surface'),
                    'race_type': r.get('race_type'),
                    'purse': r.get('purse'),
                    'grade': r.get('grade'),
                    'layer_outputs': self._summarize_layer_outputs(preds_general),
                    'skip_stats': skip_stats,
                    'consensus_signals': consensus,
                    'strategy_recommendations': strategy_recs,
                })

        # Multi-leg recommendations per card
        for track_code, card_races in cards.items():
            card_preds: List[RacePredictions] = []
            card_ctx: List[RaceContext] = []
            for r in card_races:
                rp = loader.load(r['race_id'], 'general')
                if rp and rp.horses:
                    card_preds.append(rp)
                    card_ctx.append(race_context_from_predictions(rp))
            if len(card_preds) < 2: continue

            for s in self.strategies:
                if not s.is_multi_leg: continue
                try:
                    recs = s.recommend_multi_race(card_preds, card_ctx)
                except Exception as e:
                    report['errors'].append({
                        'strategy': s.name, 'card': track_code,
                        'error': f'{type(e).__name__}: {str(e)[:200]}',
                    })
                    continue
                for rec in recs:
                    rec_dict = asdict(rec)
                    rec_dict['track'] = track_code
                    report['multi_leg_recommendations'].append(rec_dict)

        return report

    # ── POST-RACE REPORT ──

    def generate_post_race_report(self, race_date: date) -> Dict[str, Any]:
        """Reads strategy_recommendations from DB; matches against actuals;
        computes per-strategy P&L; persists to strategy_pnl."""
        # Pull recommendations for race_date
        recs = self._query("""
            SELECT recommendation_id, race_id, strategy_name, bet_type,
                   horses_json, legs_json, leg_race_ids_json, stake
            FROM strategy_recommendations
            WHERE race_date = %s
        """, (race_date,))

        if not recs:
            return {
                'race_date': str(race_date), 'n_recommendations': 0,
                'note': 'No recommendations found — pre-race report may not have run',
            }

        # Per-strategy P&L aggregates
        per_strategy: Dict[str, Dict] = defaultdict(
            lambda: {'n': 0, 'wins': 0, 'stake': 0.0, 'payout': 0.0, 'pnl': 0.0}
        )
        pnl_inserts: List[tuple] = []

        for rec in recs:
            outcome, payout, pnl = self._evaluate_recommendation(rec)
            ag = per_strategy[rec['strategy_name']]
            ag['n'] += 1; ag['stake'] += float(rec['stake'])
            ag['payout'] += payout; ag['pnl'] += pnl
            if outcome == 'W': ag['wins'] += 1
            pnl_inserts.append((
                rec['recommendation_id'], rec['race_id'], race_date,
                rec['strategy_name'], rec['bet_type'], float(rec['stake']),
                payout, pnl, outcome == 'W',
            ))

        # Bulk insert into strategy_pnl
        with self.conn.cursor() as cur:
            from psycopg2.extras import execute_values
            execute_values(cur, """
                INSERT INTO strategy_pnl (
                    recommendation_id, race_id, race_date, strategy_name,
                    bet_type, stake, payout, pnl, is_win
                ) VALUES %s
                ON CONFLICT DO NOTHING
            """, pnl_inserts)

        return {
            'race_date': str(race_date),
            'n_recommendations': len(recs),
            'per_strategy_pnl': dict(per_strategy),
            'top_winners': sorted(per_strategy.items(),
                                  key=lambda x: x[1]['pnl'], reverse=True)[:10],
            'top_losers': sorted(per_strategy.items(),
                                 key=lambda x: x[1]['pnl'])[:10],
        }

    # ── HISTORICAL CONTEXT ──

    def _historical_context_per_strategy(self, as_of: date) -> Dict[str, Dict]:
        """For each strategy: rolling P&L 7d/30d/since-inception + signals."""
        window_7d_start = as_of - timedelta(days=7)
        window_30d_start = as_of - timedelta(days=30)

        rows = self._query("""
            SELECT strategy_name, race_date, stake, payout, pnl, is_win
            FROM strategy_pnl
            WHERE race_date < %s
        """, (as_of,))

        by_strategy: Dict[str, List] = defaultdict(list)
        for r in rows:
            by_strategy[r['strategy_name']].append(r)

        out: Dict[str, Dict] = {}
        for s in self.strategies:
            entries = by_strategy.get(s.name, [])
            out[s.name] = {
                'rolling_7d': self._aggregate([e for e in entries if e['race_date'] >= window_7d_start]),
                'rolling_30d': self._aggregate([e for e in entries if e['race_date'] >= window_30d_start]),
                'since_inception': self._aggregate(entries),
                'signals': self._detect_signals(s.name, entries),
            }
        return out

    def _aggregate(self, entries: List[Dict]) -> Dict[str, Any]:
        n = len(entries)
        if n == 0:
            return {'n': 0, 'wins': 0, 'stake': 0.0, 'payout': 0.0, 'pnl': 0.0, 'roi': None, 'win_rate': None}
        stake = sum(float(e['stake']) for e in entries)
        payout = sum(float(e['payout']) for e in entries)
        pnl = sum(float(e['pnl']) for e in entries)
        wins = sum(1 for e in entries if e['is_win'])
        return {
            'n': n, 'wins': wins,
            'stake': round(stake, 2), 'payout': round(payout, 2), 'pnl': round(pnl, 2),
            'roi': round(pnl / stake * 100, 2) if stake > 0 else None,
            'win_rate': round(wins / n * 100, 2),
        }

    def _detect_signals(self, strategy_name: str, entries: List[Dict]) -> List[str]:
        """Detect notable patterns: hot streaks, drawdowns, track-specific gaps."""
        signals = []
        if not entries: return signals
        # Sort by date asc
        entries = sorted(entries, key=lambda e: e['race_date'])
        # Hot streak: last 7 race-days win rate
        last_7_days_entries = entries[-50:] if len(entries) > 50 else entries
        win_rate = sum(1 for e in last_7_days_entries if e['is_win']) / max(1, len(last_7_days_entries))
        if win_rate >= 0.40 and len(last_7_days_entries) >= 10:
            signals.append(f'hot: {int(win_rate*100)}% win rate over last {len(last_7_days_entries)} bets')
        # Drawdown: cumulative P&L from peak
        cum, peak, dd_dur, max_dd, max_dd_dur = 0.0, 0.0, 0, 0.0, 0
        for e in entries[-100:]:
            cum += float(e['pnl'])
            if cum > peak: peak = cum; dd_dur = 0
            else: dd_dur += 1
            drawdown = peak - cum
            if drawdown > max_dd:
                max_dd = drawdown; max_dd_dur = dd_dur
        if max_dd > 50 and max_dd_dur >= 5:
            signals.append(f'drawdown: -${max_dd:.0f} over {max_dd_dur} bets from peak')
        return signals

    # ── CONSENSUS + SKIP STATS ──

    def _compute_skip_stats(self, strategy_recs: Dict[str, Optional[Dict]],
                             total_single_race_strategies: int) -> Dict[str, Any]:
        """Skip count + rate across single-race strategies for this race."""
        skips = sum(1 for v in strategy_recs.values() if v is None)
        active = total_single_race_strategies - skips
        rate = skips / total_single_race_strategies if total_single_race_strategies else 0.0
        return {
            'skips_count': skips,
            'active_count': active,
            'total_strategies': total_single_race_strategies,
            'skip_rate': round(rate, 4),
        }

    def _compute_consensus_signals(
        self, strategy_recs: Dict[str, Optional[Dict]],
        rp: RacePredictions, skip_rate: float,
    ) -> Dict[str, Any]:
        """Cross-strategy consensus surfacing per race."""
        active_recs = [(name, rec) for name, rec in strategy_recs.items() if rec is not None]
        if not active_recs:
            return {
                'top_pick_consensus': None,
                'top_3_overlap': None,
                'bet_type_consensus': None,
                'longshot_alerts': None,
                'high_conviction_flag': False,
                'no_edge_flag': skip_rate > 0.75,
            }

        # Top-pick consensus: who appears as horses[0] (the lead pick) most often
        first_pick_counts: Dict[str, List[str]] = defaultdict(list)
        for name, rec in active_recs:
            horses = rec.get('horses') or []
            if not horses: continue
            first_pick_counts[horses[0]].append(name)
        top_pick = None
        if first_pick_counts:
            best_horse, best_strategies = max(first_pick_counts.items(), key=lambda x: len(x[1]))
            n_strats = len(best_strategies)
            if n_strats >= 15: strength = 'high'
            elif n_strats >= 8: strength = 'medium'
            elif n_strats >= 3: strength = 'low'
            else: strength = 'none'
            top_pick = {
                'horse_name': best_horse,
                'strategies_agreeing': n_strats,
                'strategy_names_sample': best_strategies[:6],
                'consensus_strength': strength,
            }

        # Top-3 overlap: 3 horses appearing in most recommendation `horses` lists
        appear_counts: Dict[str, int] = defaultdict(int)
        for name, rec in active_recs:
            for h in (rec.get('horses') or []):
                appear_counts[h] += 1
        ranked_horses = sorted(appear_counts.items(), key=lambda x: -x[1])[:3]
        top_3_overlap = None
        if ranked_horses:
            top_3_overlap = {
                'horses': [h for h, _ in ranked_horses],
                'appearance_counts': [c for _, c in ranked_horses],
                'strategies_with_overlap': sum(
                    1 for _, rec in active_recs
                    if any(h in (rec.get('horses') or []) for h, _ in ranked_horses)
                ),
            }

        # Bet-type consensus
        bt_counts: Dict[str, int] = defaultdict(int)
        for _, rec in active_recs:
            bt_counts[rec['bet_type']] += 1
        bet_type_consensus = None
        if bt_counts:
            dom, n = max(bt_counts.items(), key=lambda x: x[1])
            bet_type_consensus = {'dominant_bet_type': dom, 'strategies_recommending': n}

        # Longshot alerts: horses flagged by longshot layer + appearing in 3+ strategy recs
        alerted_names = {h.horse_name for h in rp.horses if h.longshot_alert}
        ls_overlap = []
        for hn in alerted_names:
            count = sum(1 for _, rec in active_recs if hn in (rec.get('horses') or []))
            if count >= 3:
                ml = next((h.morning_line_odds for h in rp.horses if h.horse_name == hn), None)
                ls_overlap.append({
                    'horse_name': hn,
                    'morning_line_odds': ml,
                    'strategies_picking_longshot': count,
                })
        longshot_alerts = ls_overlap if ls_overlap else None

        high_conviction = top_pick is not None and top_pick['strategies_agreeing'] >= 15
        no_edge = skip_rate > 0.75

        return {
            'top_pick_consensus': top_pick,
            'top_3_overlap': top_3_overlap,
            'bet_type_consensus': bet_type_consensus,
            'longshot_alerts': longshot_alerts,
            'high_conviction_flag': high_conviction,
            'no_edge_flag': no_edge,
        }

    # ── HELPERS ──

    def _summarize_layer_outputs(self, rp: RacePredictions) -> Dict[str, Any]:
        """Top-5 per layer for transparency in report."""
        out = {}
        for layer, field in [('wr_top5', 'win_probability'),
                              ('pl_top5', 'pl_win_probability'),
                              ('ranker_top5', 'rank_score'),
                              ('ensemble_top5', 'ensemble_win_prob'),
                              ('longshot_top5', 'longshot_prob'),
                              ('angle_top5', 'angle_posterior'),
                              ('trajectory_top5', 'trajectory_score')]:
            top5 = rp.top_n_by(field, n=5)
            if not top5: continue
            out[layer] = [
                {'horse_name': h.horse_name, 'program_number': h.program_number,
                 'morning_line_odds': h.morning_line_odds,
                 'value': float(getattr(h, field)) if getattr(h, field) is not None else None}
                for h in top5
            ]
        out['longshot_alerts'] = [
            {'horse_name': h.horse_name, 'longshot_prob': h.longshot_prob,
             'morning_line_odds': h.morning_line_odds}
            for h in rp.horses if h.longshot_alert
        ]
        return out

    def _get_races(self, race_date: date) -> List[Dict]:
        return self._query("""
            SELECT r.race_id, t.track_code, r.race_number, r.race_name,
                   r.post_time, r.field_size, r.distance_furlongs, r.surface,
                   r.race_type, r.purse, r.grade
            FROM races r JOIN tracks t USING (track_id)
            WHERE r.race_date = %s
              AND r.race_id IN (
                  SELECT race_id FROM entries WHERE is_scratched = false
                  GROUP BY race_id HAVING COUNT(*) >= 4
              )
            ORDER BY t.track_code, r.race_number
        """, (race_date,))

    def _query(self, sql: str, params=None) -> List[Dict]:
        with self.conn.cursor() as cur:
            cur.execute(sql, params or ())
            return [dict(row) for row in cur.fetchall()]

    def _evaluate_recommendation(self, rec: Dict) -> tuple:
        """Match a recommendation against actual race results.
        Returns (outcome 'W'/'L'/'-', payout, pnl)."""
        bet_type = rec['bet_type']
        stake = float(rec['stake'])
        horses = rec['horses_json'] or []
        # Pull race outcomes
        out = self._query("""
            SELECT h.horse_name, res.finish_position, res.win_payout, res.place_payout,
                   res.show_payout, res.exacta_payout, res.trifecta_payout, res.superfecta_payout,
                   res.daily_double_payout, res.pick3_payout, res.pick4_payout, res.pick5_payout
            FROM results res JOIN horses h ON res.horse_id = h.horse_id
            WHERE res.race_id = %s
        """, (rec['race_id'],))
        if not out:
            return ('-', 0.0, 0.0)
        finish = {r['horse_name']: r['finish_position'] for r in out}
        wp = next((float(r['win_payout']) for r in out if r['win_payout'] and r['horse_name'] in horses), None)
        exa = next((float(r['exacta_payout']) for r in out if r['exacta_payout']), None)
        tri = next((float(r['trifecta_payout']) for r in out if r['trifecta_payout']), None)
        sf = next((float(r['superfecta_payout']) for r in out if r['superfecta_payout']), None)

        # Single-race
        if bet_type == 'win':
            if finish.get(horses[0]) == 1 and wp:
                return ('W', wp, wp - stake)
            return ('L', 0.0, -stake)
        if bet_type.startswith('exacta_box_'):
            actual_top2 = sorted([(n,f) for n,f in finish.items() if f and f<=2], key=lambda x:x[1])
            if len(actual_top2) < 2: return ('L', 0.0, -stake)
            hit = actual_top2[0][0] in horses and actual_top2[1][0] in horses
            if hit and exa: return ('W', exa, exa - stake)
            return ('L', 0.0, -stake)
        if bet_type.startswith('trifecta_box_'):
            actual_top3 = {n for n,f in finish.items() if f and f<=3}
            if len(actual_top3) < 3: return ('L', 0.0, -stake)
            if actual_top3 <= set(horses) and tri: return ('W', tri, tri - stake)
            return ('L', 0.0, -stake)
        if bet_type.startswith('superfecta_box_'):
            actual_top4 = {n for n,f in finish.items() if f and f<=4}
            if len(actual_top4) < 4: return ('L', 0.0, -stake)
            if actual_top4 <= set(horses) and sf: return ('W', sf, sf - stake)
            return ('L', 0.0, -stake)
        # Multi-leg: need leg_race_ids + legs_json
        if bet_type.startswith('dd_') or bet_type.startswith('pick'):
            legs = rec['legs_json']
            leg_ids = rec['leg_race_ids_json']
            if not legs or not leg_ids: return ('-', 0.0, 0.0)
            # Get winner per leg race
            n_legs = len(leg_ids)
            payout_col = 'daily_double_payout' if bet_type.startswith('dd') else f'{bet_type.split("_")[0]}_payout'
            # Get winners for each leg
            winners = []
            for lrid in leg_ids:
                wr = self._query("""
                    SELECT h.horse_name FROM results res JOIN horses h USING (horse_id)
                    WHERE res.race_id = %s AND res.finish_position = 1 LIMIT 1
                """, (lrid,))
                winners.append(wr[0]['horse_name'] if wr else None)
            if any(w is None for w in winners): return ('-', 0.0, 0.0)
            hit = all(winners[i] in legs[i] for i in range(n_legs))
            # Pull payout from final leg
            final_payout = self._query(f"""
                SELECT res.{payout_col} AS p FROM results res
                WHERE res.race_id = %s AND res.{payout_col} IS NOT NULL LIMIT 1
            """, (leg_ids[-1],))
            if hit and final_payout and final_payout[0]['p']:
                pay = float(final_payout[0]['p'])
                return ('W', pay, pay - stake)
            return ('L', 0.0, -stake)
        return ('-', 0.0, -stake)
