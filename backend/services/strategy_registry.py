"""
Strategy registry — every named strategy candidate that runs daily.

Tony reads daily report; Tony decides; Tony bets. No canonical "production"
strategy is selected from this registry.

Adding a new strategy:
  1. Subclass StrategyBase
  2. Append instance to STRATEGIES list at module level
  3. Strategy auto-appears in next day's report; auto-tracks historical P&L
"""
from __future__ import annotations
from typing import List, Optional, Tuple, Dict, Any

from services.strategy_harness import (
    StrategyBase, RacePredictions, RaceContext, BetRecommendation,
    HorsePrediction, RANKING_LAYER_FIELDS,
)


# ════════════════════════════════════════════════════════════════
# EV-based strategies (T1.x)
# ════════════════════════════════════════════════════════════════
# These wrap the existing EVEngine + EVStrategy for in-harness use.

class T1_1_6_EV_Median(StrategyBase):
    """T1.1.6 — EV-MEDIAN with losers (trifecta_key, exacta_key, wide Pick-4)
    disabled. +322% ROI on 11-day OOS."""
    name = 't1_1_6_ev_median'
    description = 'EV-optimized; losers disabled; median payout estimator'
    category = 'ev'
    style = 'general'
    ranking_layer = 'wr'

    def __init__(self):
        super().__init__()
        from services.ev_engine import EVEngine
        from services.ev_strategy import EVStrategy
        import json, os
        lookup_path = '/tmp/t11_5_payout_lookup.json'
        if os.path.exists(lookup_path):
            lookup = json.load(open(lookup_path))
            self._engine = EVEngine(lookup, payout_estimator='median')
            self._strategy = EVStrategy(self._engine, min_ev_threshold=0.0, max_ticket_cost=60.0)
        else:
            self._strategy = None

    def recommend(self, rp, ctx):
        if not self._strategy or not rp.horses: return None
        preds = [
            {'horse_id': h.horse_id, 'horse_name': h.horse_name,
             'win_prob': h.win_probability or 0.0}
            for h in rp.horses if h.win_probability is not None
        ]
        if len(preds) < 3: return None
        rec = self._strategy.recommend_bet(preds, ctx.field_size)
        if rec['bet_type'] == 'skip': return None
        return BetRecommendation(
            strategy_name=self.name, race_id=rp.race_id,
            bet_type=rec['bet_type'],
            horses=[h['horse_name'] for h in rec['horses']],
            stake=rec['ticket_cost'], confidence=rec['expected_ev'],
            rationale=f"EV={rec['expected_ev']:+.2f} p_hit={rec['p_hit']:.4f}",
        )


class T1_4_Pool_Conditional(StrategyBase):
    """T1.4 — Pool-conditional EV. Informational despite -9pp vs T1.1.6."""
    name = 't1_4_pool_conditional'
    description = 'EV with pool-bucket conditional payout lookup'
    category = 'ev'
    style = 'general'
    ranking_layer = 'wr'

    def __init__(self):
        super().__init__()
        from services.ev_engine import EVEngine
        from services.ev_strategy import EVStrategy
        import json, os
        cond_path = '/tmp/t14_conditional_lookup.json'
        proxy_path = '/tmp/t14_pool_proxy.json'
        if os.path.exists(cond_path) and os.path.exists(proxy_path):
            cond = json.load(open(cond_path))
            proxy = json.load(open(proxy_path))
            for bet in proxy:
                for tc, m in proxy[bet].items():
                    proxy[bet][tc] = {(int(k) if k != 'avg' else 'avg'): v
                                       for k, v in m.items()}
            self._engine = EVEngine(
                payout_lookup=cond['conditional_payout_lookup'],
                payout_estimator='median', pool_proxy=proxy,
                pool_quartiles=cond['pool_quartiles'], conditional=True,
            )
            self._strategy = EVStrategy(self._engine, min_ev_threshold=0.0, max_ticket_cost=60.0)
        else:
            self._strategy = None

    def recommend(self, rp, ctx):
        if not self._strategy or not rp.horses: return None
        self._engine.set_race_context(ctx.track_code, ctx.race_date)
        preds = [
            {'horse_id': h.horse_id, 'horse_name': h.horse_name,
             'win_prob': h.win_probability or 0.0}
            for h in rp.horses if h.win_probability is not None
        ]
        if len(preds) < 3: return None
        rec = self._strategy.recommend_bet(preds, ctx.field_size)
        if rec['bet_type'] == 'skip': return None
        return BetRecommendation(
            strategy_name=self.name, race_id=rp.race_id,
            bet_type=rec['bet_type'],
            horses=[h['horse_name'] for h in rec['horses']],
            stake=rec['ticket_cost'], confidence=rec['expected_ev'],
            rationale=f"EV={rec['expected_ev']:+.2f} (pool-conditional)",
        )


# Production_Heuristic removed Phase 7.3 per Option C adjudication
# (heuristic baseline superseded by Hybrid C + specialist-layer strategies)


# ════════════════════════════════════════════════════════════════
# Raw-layer top-N strategies
# ════════════════════════════════════════════════════════════════

class _RawLayerWin(StrategyBase):
    """Generic: bet $2 to win on top-1 from configured ranking layer."""
    category = 'raw_layer'
    def recommend(self, rp, ctx):
        top = self.top_n(rp, 1)
        if not top: return None
        return BetRecommendation(
            strategy_name=self.name, race_id=rp.race_id, bet_type='win',
            horses=[top[0].horse_name], stake=2.0,
            confidence=getattr(top[0], self.get_ranking_field()),
            rationale=f'{self.ranking_layer} top1; prob={getattr(top[0], self.get_ranking_field()):.4f}',
        )


class WR_Top1_Win(_RawLayerWin):
    name = 'wr_top1_win'
    description = 'WR layer top-1 → $2 win bet'
    ranking_layer = 'wr'


class PL_Top1_Win(_RawLayerWin):
    name = 'pl_top1_win'
    description = 'PL layer top-1 → $2 win bet'
    ranking_layer = 'pl'


class Ensemble_Top1_Win(_RawLayerWin):
    name = 'ensemble_top1_win'
    description = 'Ensemble top-1 → $2 win bet'
    ranking_layer = 'ensemble'


class Ranker_Top1_Win(_RawLayerWin):
    name = 'ranker_top1_win'
    description = 'Ranker top-1 → $2 win bet'
    ranking_layer = 'ranker'


class Longshot_Top1_Win(StrategyBase):
    """Bet $2 win on the highest longshot_prob horse, IF it has longshot_alert."""
    name = 'longshot_top1_win'
    description = 'Longshot layer alerted top pick → $2 win bet'
    category = 'raw_layer'
    ranking_layer = 'longshot'

    def recommend(self, rp, ctx):
        flagged = [h for h in rp.horses if h.longshot_alert]
        if not flagged: return None
        top = sorted(flagged, key=lambda h: h.longshot_prob or 0, reverse=True)[0]
        return BetRecommendation(
            strategy_name=self.name, race_id=rp.race_id, bet_type='win',
            horses=[top.horse_name], stake=2.0,
            confidence=top.longshot_prob,
            rationale=f'longshot alert; longshot_prob={top.longshot_prob:.4f}',
        )


class Bayesian_Angle_Top(StrategyBase):
    """Bet $2 win on horse with highest angle_posterior across ALL angle types.

    Tier 1 2B substrate finding (2026-05-16): this aggregate strategy is dominated
    by `class_drop` angle firings (76% of firings; AUC 0.4978 = signal-less)
    which mask the strong `first_time_lasix` signal (AUC 0.7630 / 22% win rate /
    122 firings). Aggregate ROI: −7.4%. See Bayesian_Angle_Top_FirstTimeLasix
    for the substrate-isolated variant.
    """
    name = 'bayesian_angle_top'
    description = 'Bayesian angle posterior top pick → $2 win (aggregate; mixed signal)'
    category = 'angle'
    ranking_layer = 'angle'

    def recommend(self, rp, ctx):
        ranked = [h for h in rp.horses if h.angle_posterior is not None and h.angle_posterior > 0]
        if not ranked: return None
        top = sorted(ranked, key=lambda h: h.angle_posterior, reverse=True)[0]
        return BetRecommendation(
            strategy_name=self.name, race_id=rp.race_id, bet_type='win',
            horses=[top.horse_name], stake=2.0, confidence=top.angle_posterior,
            rationale=f'angle={top.angle_name} posterior={top.angle_posterior:.4f}',
        )


class Bayesian_Angle_Top_FirstTimeLasix(StrategyBase):
    """Substrate-isolated: first_time_lasix angle only (substrate-validated 2026-05-16).

    Tier 1 2B forensic: AUC 0.7630, 22.13% win rate, 122 firings in 40-day window.
    Strong signal hidden inside aggregate `bayesian_angle_top` which is dominated
    by class_drop (76% firings, AUC 0.4978 = signal-less). Isolating first_time_lasix
    extracts the substrate-real edge.
    """
    name = 'bayesian_angle_top_first_time_lasix'
    description = 'Bayesian first_time_lasix angle (substrate-isolated) → $2 win'
    category = 'angle'
    ranking_layer = 'angle'

    def recommend(self, rp, ctx):
        # Filter to horses with angle_name='first_time_lasix' AND positive posterior
        ranked = [
            h for h in rp.horses
            if h.angle_name == 'first_time_lasix'
            and h.angle_posterior is not None and h.angle_posterior > 0
        ]
        if not ranked: return None
        top = sorted(ranked, key=lambda h: h.angle_posterior, reverse=True)[0]
        return BetRecommendation(
            strategy_name=self.name, race_id=rp.race_id, bet_type='win',
            horses=[top.horse_name], stake=2.0, confidence=top.angle_posterior,
            rationale=f'first_time_lasix posterior={top.angle_posterior:.4f}',
        )


# ── Box / Key strategies on ensemble top-N ──

class _EnsembleBox(StrategyBase):
    """Generic boxed bet on ensemble top-N. N + bet_type derived from subclass."""
    category = 'raw_layer'
    ranking_layer = 'ensemble'
    n_horses: int = 3
    bet_kind: str = 'exacta'  # 'exacta' / 'trifecta' / 'superfecta'
    base_unit: float = 1.0    # $2 for exacta, $1 for tri, $0.10 for sf

    def recommend(self, rp, ctx):
        if ctx.field_size < self.n_horses: return None
        top = self.top_n(rp, self.n_horses)
        if len(top) < self.n_horses: return None
        n = self.n_horses
        if self.bet_kind == 'exacta':
            combos = n * (n - 1)
        elif self.bet_kind == 'trifecta':
            combos = n * (n - 1) * (n - 2)
        else:  # superfecta
            combos = n * (n - 1) * (n - 2) * (n - 3)
        stake = combos * self.base_unit
        return BetRecommendation(
            strategy_name=self.name, race_id=rp.race_id,
            bet_type=f'{self.bet_kind}_box_{n}',
            horses=[h.horse_name for h in top], stake=stake,
            confidence=top[0].ensemble_win_prob,
            rationale=f'{self.bet_kind}_box_{n} on ensemble top {n}',
        )


class Ensemble_Top2_ExactaBox(_EnsembleBox):
    name = 'ensemble_top2_exa_box'
    description = 'Exacta box top-2 from ensemble (ticket $4)'
    n_horses = 2; bet_kind = 'exacta'; base_unit = 2.0


class Ensemble_Top3_TriBox(_EnsembleBox):
    name = 'ensemble_top3_tri_box'
    description = 'Trifecta box top-3 from ensemble (ticket $6)'
    n_horses = 3; bet_kind = 'trifecta'; base_unit = 1.0


class Ensemble_Top4_TriBox(_EnsembleBox):
    name = 'ensemble_top4_tri_box'
    description = 'Trifecta box top-4 from ensemble (ticket $24)'
    n_horses = 4; bet_kind = 'trifecta'; base_unit = 1.0


class Ensemble_Top4_SFBox(_EnsembleBox):
    name = 'ensemble_top4_sf_box'
    description = 'Superfecta box top-4 from ensemble (ticket $2.40)'
    n_horses = 4; bet_kind = 'superfecta'; base_unit = 0.10


class Ensemble_Top5_SFBox(_EnsembleBox):
    name = 'ensemble_top5_sf_box'
    description = 'Superfecta box top-5 from ensemble (ticket $12)'
    n_horses = 5; bet_kind = 'superfecta'; base_unit = 0.10


class Ensemble_Top6_SFBox(_EnsembleBox):
    name = 'ensemble_top6_sf_box'
    description = 'Superfecta box top-6 from ensemble (ticket $36)'
    n_horses = 6; bet_kind = 'superfecta'; base_unit = 0.10


# ── Specialist-style raw-layer variants (gonzo_sauce / speed) ──

class WR_Top1_Win_Gonzo(_RawLayerWin):
    name = 'wr_top1_win_gonzo'
    description = 'WR (gonzo_sauce style) top-1 → $2 win'
    style = 'gonzo_sauce'; ranking_layer = 'wr'


class WR_Top1_Win_Speed(_RawLayerWin):
    name = 'wr_top1_win_speed'
    description = 'WR (speed style) top-1 → $2 win'
    style = 'speed'; ranking_layer = 'wr'


class WR_Top1_Win_Closer(_RawLayerWin):
    name = 'wr_top1_win_closer'
    description = 'WR (closer style) top-1 → $2 win'
    style = 'closer'; ranking_layer = 'wr'


# ════════════════════════════════════════════════════════════════
# Multi-leg strategies — parameterized
# ════════════════════════════════════════════════════════════════

# Spread enumerations from T1.1.6 force-eval (substrate-validated)
DD_SPREADS = [(1,1),(1,2),(2,1),(2,2),(2,3),(3,2),(3,3)]
P3_SPREADS = [(1,1,1),(2,1,1),(1,2,1),(1,1,2),(2,2,1),(2,1,2),(1,2,2),(2,2,2),
              (3,2,2),(2,3,2),(2,2,3),(3,3,2),(3,2,3),(2,3,3),(3,3,3)]
P4_SPREADS = [(1,1,1,1),(2,1,1,1),(1,2,1,1),(1,1,2,1),(1,1,1,2),
              (2,2,1,1),(2,1,2,1),(2,1,1,2),(1,2,2,1),(1,2,1,2),(1,1,2,2),
              (2,2,2,1),(2,2,1,2),(2,1,2,2),(1,2,2,2),(2,2,2,2)]
P5_SPREADS = [(1,1,1,1,1),(2,1,1,1,1),(1,2,1,1,1),(1,1,2,1,1),(1,1,1,2,1),(1,1,1,1,2),
              (2,2,1,1,1),(2,1,2,1,1),(2,1,1,2,1),(2,1,1,1,2),(1,2,2,1,1),(1,2,1,2,1),
              (1,2,1,1,2),(1,1,2,2,1),(1,1,2,1,2),(1,1,1,2,2),
              (2,2,2,1,1),(2,2,2,2,1),(2,2,2,2,2),
              (3,2,2,2,2),(2,3,2,2,2),(3,3,2,2,2)]


class _MultiLegSpread(StrategyBase):
    """Parameterized multi-leg strategy. spread tuple = horses-per-leg.

    Subclasses set bet_root ('dd','pick3','pick4','pick5') + base_unit.
    Instances created via _make() factory per spread."""
    is_multi_leg = True
    category = 'multi_leg'
    ranking_layer = 'ensemble'
    bet_root: str = 'pick3'
    base_unit: float = 0.50

    def __init__(self, spread: Tuple[int, ...]):
        super().__init__()
        self.spread = spread
        self.n_legs = len(spread)
        self._spread_str = 'x'.join(str(s) for s in spread)
        self._name = f'ensemble_{self.bet_root}_{self._spread_str}'

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return f'{self.bet_root.upper()} spread {self._spread_str} on ensemble top-N per leg'

    def recommend_multi_race(self, card_preds, card_ctx):
        recs = []
        if len(card_preds) < self.n_legs:
            return recs
        for start in range(len(card_preds) - self.n_legs + 1):
            window = card_preds[start:start + self.n_legs]
            window_ctx = card_ctx[start:start + self.n_legs]
            leg_horses = []
            for i, rp in enumerate(window):
                top = self.top_n(rp, self.spread[i])
                if len(top) < self.spread[i]:
                    leg_horses = None; break
                leg_horses.append(top)
            if leg_horses is None: continue
            n_combos = 1
            for s in self.spread: n_combos *= s
            ticket = n_combos * self.base_unit
            recs.append(BetRecommendation(
                strategy_name=self.name,
                race_id=window[0].race_id,
                bet_type=f'{self.bet_root}_{self._spread_str}',
                horses=[h.horse_name for legs in leg_horses for h in legs],
                legs=[[h.horse_name for h in legs] for legs in leg_horses],
                leg_race_ids=[rp.race_id for rp in window],
                stake=ticket,
                confidence=None,  # Could compute joint prob; deferred to T1.x EV upgrade
                rationale=f'{self.bet_root} {self._spread_str} on ensemble top-N per leg',
            ))
        return recs


class _DD_Spread(_MultiLegSpread):
    bet_root = 'dd'; base_unit = 2.0


class _P3_Spread(_MultiLegSpread):
    bet_root = 'pick3'; base_unit = 0.50


class _P4_Spread(_MultiLegSpread):
    bet_root = 'pick4'; base_unit = 0.50


class _P5_Spread(_MultiLegSpread):
    bet_root = 'pick5'; base_unit = 0.50


# ════════════════════════════════════════════════════════════════
# Hybrid C culled-rebuilt ensemble strategies (Phase 7.4)
# ════════════════════════════════════════════════════════════════

class HybridC_Top1_Win(_RawLayerWin):
    name = 'hybrid_c_top1_win'
    description = 'Hybrid C ensemble top-1 → $2 win'
    ranking_layer = 'ensemble_hybrid_option_c'


class _HybridCBox(_EnsembleBox):
    ranking_layer = 'ensemble_hybrid_option_c'


class HybridC_Top2_ExaBox(_HybridCBox):
    name = 'hybrid_c_top2_exa_box'
    description = 'Exacta box top-2 from Hybrid C (ticket $4)'
    n_horses = 2; bet_kind = 'exacta'; base_unit = 2.0


class HybridC_Top3_TriBox(_HybridCBox):
    name = 'hybrid_c_top3_tri_box'
    description = 'Trifecta box top-3 from Hybrid C (ticket $6)'
    n_horses = 3; bet_kind = 'trifecta'; base_unit = 1.0


class HybridC_Top4_TriBox(_HybridCBox):
    name = 'hybrid_c_top4_tri_box'
    description = 'Trifecta box top-4 from Hybrid C (ticket $24)'
    n_horses = 4; bet_kind = 'trifecta'; base_unit = 1.0


class HybridC_Top4_SFBox(_HybridCBox):
    name = 'hybrid_c_top4_sf_box'
    description = 'Superfecta box top-4 from Hybrid C (ticket $2.40)'
    n_horses = 4; bet_kind = 'superfecta'; base_unit = 0.10


class HybridC_Top5_SFBox(_HybridCBox):
    name = 'hybrid_c_top5_sf_box'
    description = 'Superfecta box top-5 from Hybrid C (ticket $12)'
    n_horses = 5; bet_kind = 'superfecta'; base_unit = 0.10


class HybridC_Top6_SFBox(_HybridCBox):
    name = 'hybrid_c_top6_sf_box'
    description = 'Superfecta box top-6 from Hybrid C (ticket $36)'
    n_horses = 6; bet_kind = 'superfecta'; base_unit = 0.10


class _HybridC_MultiLegSpread(_MultiLegSpread):
    ranking_layer = 'ensemble_hybrid_option_c'

    def __init__(self, spread):
        super().__init__(spread)
        self._name = f'hybrid_c_{self.bet_root}_{self._spread_str}'


class _HybridC_DD_Spread(_HybridC_MultiLegSpread):
    bet_root = 'dd'; base_unit = 2.0


class _HybridC_P3_Spread(_HybridC_MultiLegSpread):
    bet_root = 'pick3'; base_unit = 0.50


class _HybridC_P4_Spread(_HybridC_MultiLegSpread):
    bet_root = 'pick4'; base_unit = 0.50


class _HybridC_P5_Spread(_HybridC_MultiLegSpread):
    bet_root = 'pick5'; base_unit = 0.50


# ════════════════════════════════════════════════════════════════
# specialist_style sprint sub-booster strategies (β.3; Q-pre-β-3 Option A)
# Substrate-evidence: δ.2 multi-track +71.4pp ΔROI on sprint stratum
# (distance ≤ 6.5f); Q1 P1 SPRINT-ONLY routing; Q2 R1 route DEPRECATED.
# Substrate-isolated from production routing pre-β.4 activation.
# ════════════════════════════════════════════════════════════════

class _SpecialistStyleSprintBox(_EnsembleBox):
    ranking_layer = 'specialist_style_sprint'


class SpecialistStyleSprint_Top1_Win(_RawLayerWin):
    name = 'specialist_style_sprint_top1_win'
    description = 'Sprint sub-booster top-1 → $2 win (distance ≤ 6.5f routing)'
    ranking_layer = 'specialist_style_sprint'


class SpecialistStyleSprint_Top2_ExaBox(_SpecialistStyleSprintBox):
    name = 'specialist_style_sprint_top2_exa_box'
    description = 'Exacta box top-2 from sprint sub-booster (ticket $4)'
    n_horses = 2; bet_kind = 'exacta'; base_unit = 2.0


class SpecialistStyleSprint_Top3_TriBox(_SpecialistStyleSprintBox):
    name = 'specialist_style_sprint_top3_tri_box'
    description = 'Trifecta box top-3 from sprint sub-booster (ticket $6)'
    n_horses = 3; bet_kind = 'trifecta'; base_unit = 1.0


class SpecialistStyleSprint_Top4_SFBox(_SpecialistStyleSprintBox):
    name = 'specialist_style_sprint_top4_sf_box'
    description = 'Superfecta box top-4 from sprint sub-booster (ticket $2.40)'
    n_horses = 4; bet_kind = 'superfecta'; base_unit = 0.10


# ════════════════════════════════════════════════════════════════
# Specialist standalone strategies (per F2 substrate evidence)
# Style filtering applied via wr_predictions.style; ranker layer via rank_score.
# ════════════════════════════════════════════════════════════════

class _SpecialistTop1Win(_RawLayerWin):
    """Top-1 win from a specialist style's ranker output."""
    ranking_layer = 'ranker'


class _SpecialistBox(_EnsembleBox):
    """Box bet ranked by specialist style's ranker output.
    Note: _EnsembleBox defaults to ranking_layer='ensemble'; we override per-style."""
    ranking_layer = 'ranker'


# Speed specialist
class RkFullSpeed_Top1_Win(_SpecialistTop1Win):
    name = 'rk_full_speed_top1_win'
    description = 'Phase B.x rk_full_speed top-1 → $2 win'
    style = 'speed'


class RkFullSpeed_Top3_TriBox(_SpecialistBox):
    name = 'rk_full_speed_top3_tri_box'
    description = 'Trifecta box top-3 from Phase B.x rk_full_speed'
    style = 'speed'; n_horses = 3; bet_kind = 'trifecta'; base_unit = 1.0


class RkFullSpeed_Top5_SFBox(_SpecialistBox):
    name = 'rk_full_speed_top5_sf_box'
    description = 'Superfecta box top-5 from Phase B.x rk_full_speed'
    style = 'speed'; n_horses = 5; bet_kind = 'superfecta'; base_unit = 0.10


# Class-riser specialist
class RkFullClassRiser_Top1_Win(_SpecialistTop1Win):
    name = 'rk_full_class_riser_top1_win'
    description = 'Phase B.x rk_full_class_riser top-1 → $2 win'
    style = 'class_riser'


class RkFullClassRiser_Top3_TriBox(_SpecialistBox):
    name = 'rk_full_class_riser_top3_tri_box'
    description = 'Trifecta box top-3 from Phase B.x rk_full_class_riser'
    style = 'class_riser'; n_horses = 3; bet_kind = 'trifecta'; base_unit = 1.0


class RkFullClassRiser_Top5_SFBox(_SpecialistBox):
    name = 'rk_full_class_riser_top5_sf_box'
    description = 'Superfecta box top-5 from Phase B.x rk_full_class_riser'
    style = 'class_riser'; n_horses = 5; bet_kind = 'superfecta'; base_unit = 0.10


# Closer specialist
class RkFullCloser_Top1_Win(_SpecialistTop1Win):
    name = 'rk_full_closer_top1_win'
    description = 'Phase B.x rk_full_closer top-1 → $2 win'
    style = 'closer'


class RkFullCloser_Top3_TriBox(_SpecialistBox):
    name = 'rk_full_closer_top3_tri_box'
    description = 'Trifecta box top-3 from Phase B.x rk_full_closer'
    style = 'closer'; n_horses = 3; bet_kind = 'trifecta'; base_unit = 1.0


class RkFullCloser_Top5_SFBox(_SpecialistBox):
    name = 'rk_full_closer_top5_sf_box'
    description = 'Superfecta box top-5 from Phase B.x rk_full_closer'
    style = 'closer'; n_horses = 5; bet_kind = 'superfecta'; base_unit = 0.10


# Gonzo-sauce specialist
class RkFullGonzoSauce_Top1_Win(_SpecialistTop1Win):
    name = 'rk_full_gonzo_sauce_top1_win'
    description = 'Phase B.x rk_full_gonzo_sauce top-1 → $2 win'
    style = 'gonzo_sauce'


class RkFullGonzoSauce_Top3_TriBox(_SpecialistBox):
    name = 'rk_full_gonzo_sauce_top3_tri_box'
    description = 'Trifecta box top-3 from Phase B.x rk_full_gonzo_sauce'
    style = 'gonzo_sauce'; n_horses = 3; bet_kind = 'trifecta'; base_unit = 1.0


class RkFullGonzoSauce_Top5_SFBox(_SpecialistBox):
    name = 'rk_full_gonzo_sauce_top5_sf_box'
    description = 'Superfecta box top-5 from Phase B.x rk_full_gonzo_sauce'
    style = 'gonzo_sauce'; n_horses = 5; bet_kind = 'superfecta'; base_unit = 0.10


# WP-full speed specialist (ranking by win_probability, not rank_score)
class WpFullSpeed_Top1_Win(_RawLayerWin):
    name = 'wp_full_speed_top1_win'
    description = 'Phase B.x wp_full_speed top-1 → $2 win'
    ranking_layer = 'wr'  # reads win_probability
    style = 'speed'


class WpFullSpeed_Top3_TriBox(_EnsembleBox):
    name = 'wp_full_speed_top3_tri_box'
    description = 'Trifecta box top-3 from Phase B.x wp_full_speed'
    ranking_layer = 'wr'  # reads win_probability
    style = 'speed'; n_horses = 3; bet_kind = 'trifecta'; base_unit = 1.0


class WpFullSpeed_Top5_SFBox(_EnsembleBox):
    name = 'wp_full_speed_top5_sf_box'
    description = 'Superfecta box top-5 from Phase B.x wp_full_speed'
    ranking_layer = 'wr'
    style = 'speed'; n_horses = 5; bet_kind = 'superfecta'; base_unit = 0.10


# ════════════════════════════════════════════════════════════════
# Dispatch B — wp_55feat_odds_blind_orphan (F1 activation, 2026-05-16)
# Orphan moved into wp_full_general slot via Path α; serves general style.
# Forensic: AUC 0.691 / top-1 37.8% / ROI +61.7% (beats prior canonical +30%).
# ════════════════════════════════════════════════════════════════

class Wp55featOddsBlindOrphan_Top1_Win(_RawLayerWin):
    name = 'wp_55feat_odds_blind_orphan_top1_win'
    description = 'Odds-blind orphan top-1 → $2 win (forensic AUC 0.691 / ROI +61.7%)'
    ranking_layer = 'wr'  # reads win_probability (now produced by orphan via wp_full_general slot)
    style = 'general'


class Wp55featOddsBlindOrphan_Top3_TriBox(_EnsembleBox):
    name = 'wp_55feat_odds_blind_orphan_top3_tri_box'
    description = 'Trifecta box top-3 from odds-blind orphan'
    ranking_layer = 'wr'
    style = 'general'; n_horses = 3; bet_kind = 'trifecta'; base_unit = 1.0


class Wp55featOddsBlindOrphan_Top5_SFBox(_EnsembleBox):
    name = 'wp_55feat_odds_blind_orphan_top5_sf_box'
    description = 'Superfecta box top-5 from odds-blind orphan'
    ranking_layer = 'wr'
    style = 'general'; n_horses = 5; bet_kind = 'superfecta'; base_unit = 0.10


# ════════════════════════════════════════════════════════════════
# REGISTRY
# ════════════════════════════════════════════════════════════════

STRATEGIES: List[StrategyBase] = [
    # ── EV strategies (2; Production_Heuristic removed Phase 7.3) ──
    T1_1_6_EV_Median(),
    T1_4_Pool_Conditional(),

    # ── Raw-layer single-bet strategies (general style; 4) ──
    WR_Top1_Win(),
    PL_Top1_Win(),
    Ensemble_Top1_Win(),
    Ranker_Top1_Win(),

    # ── Specialist-style raw-layer variants (3) ──
    WR_Top1_Win_Gonzo(),
    WR_Top1_Win_Speed(),
    WR_Top1_Win_Closer(),

    # ── Longshot + Bayesian (2; aggregate Bayesian_Angle_Top deprecated 2026-05-16 ──
    # ── per Decision 3 — class_drop noise dominated aggregate signal; only ──
    # ── first_time_lasix substrate-isolated variant retained) ──
    Longshot_Top1_Win(),
    Bayesian_Angle_Top_FirstTimeLasix(),

    # ── Ensemble box-bet strategies (6) ──
    Ensemble_Top2_ExactaBox(),
    Ensemble_Top3_TriBox(),
    Ensemble_Top4_TriBox(),
    Ensemble_Top4_SFBox(),
    Ensemble_Top5_SFBox(),
    Ensemble_Top6_SFBox(),

    # ── Multi-leg parameterized (60) ──
    *[_DD_Spread(s) for s in DD_SPREADS],
    *[_P3_Spread(s) for s in P3_SPREADS],
    *[_P4_Spread(s) for s in P4_SPREADS],
    *[_P5_Spread(s) for s in P5_SPREADS],

    # ── Hybrid C single-race (7) — Phase 7.4 ──
    HybridC_Top1_Win(),
    HybridC_Top2_ExaBox(),
    HybridC_Top3_TriBox(),
    HybridC_Top4_TriBox(),
    HybridC_Top4_SFBox(),
    HybridC_Top5_SFBox(),
    HybridC_Top6_SFBox(),

    # ── Hybrid C multi-leg parameterized (60) — Phase 7.4 ──
    *[_HybridC_DD_Spread(s) for s in DD_SPREADS],
    *[_HybridC_P3_Spread(s) for s in P3_SPREADS],
    *[_HybridC_P4_Spread(s) for s in P4_SPREADS],
    *[_HybridC_P5_Spread(s) for s in P5_SPREADS],

    # ── Specialist standalone (15) — Phase 7.4 ──
    RkFullSpeed_Top1_Win(), RkFullSpeed_Top3_TriBox(), RkFullSpeed_Top5_SFBox(),
    RkFullClassRiser_Top1_Win(), RkFullClassRiser_Top3_TriBox(), RkFullClassRiser_Top5_SFBox(),
    RkFullCloser_Top1_Win(), RkFullCloser_Top3_TriBox(), RkFullCloser_Top5_SFBox(),
    RkFullGonzoSauce_Top1_Win(), RkFullGonzoSauce_Top3_TriBox(), RkFullGonzoSauce_Top5_SFBox(),
    WpFullSpeed_Top1_Win(), WpFullSpeed_Top3_TriBox(), WpFullSpeed_Top5_SFBox(),

    # ── Dispatch B orphan (3; F1 activation, 2026-05-16) ──
    Wp55featOddsBlindOrphan_Top1_Win(),
    Wp55featOddsBlindOrphan_Top3_TriBox(),
    Wp55featOddsBlindOrphan_Top5_SFBox(),

    # ── specialist_style sprint sub-booster (4; β.3 Q-pre-β-3 Option A) ──
    # Substrate-isolated from production routing pre-β.4 activation.
    SpecialistStyleSprint_Top1_Win(),
    SpecialistStyleSprint_Top2_ExaBox(),
    SpecialistStyleSprint_Top3_TriBox(),
    SpecialistStyleSprint_Top4_SFBox(),
]


def get_registry() -> List[StrategyBase]:
    """Public accessor; lets daemons reload the registry without restart."""
    return STRATEGIES


def registry_size_by_category() -> Dict[str, int]:
    """Diagnostic: count of strategies per category for report header."""
    counts: Dict[str, int] = {}
    for s in STRATEGIES:
        counts[s.category] = counts.get(s.category, 0) + 1
    return counts


if __name__ == '__main__':
    # Smoke test: instantiate registry, verify uniqueness + counts
    names = [s.name for s in STRATEGIES]
    assert len(names) == len(set(names)), f"Duplicate strategy names: {set(n for n in names if names.count(n) > 1)}"
    print(f"Registry: {len(STRATEGIES)} strategies")
    print(f"By category: {registry_size_by_category()}")
    print(f"By is_multi_leg: True={sum(1 for s in STRATEGIES if s.is_multi_leg)}, "
          f"False={sum(1 for s in STRATEGIES if not s.is_multi_leg)}")
    print(f"By style (top 5): {sorted(set(s.style for s in STRATEGIES))[:5]}")
    print(f"\nFirst 20 strategy names:")
    for n in names[:20]:
        print(f"  {n}")
    print(f"...\nLast 5 strategy names:")
    for n in names[-5:]:
        print(f"  {n}")
