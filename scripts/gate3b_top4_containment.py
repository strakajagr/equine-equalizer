"""Gate 3B — top-4 containment + 4x4x4 P3 + chalk-bleed vs longshot-upside.

Inputs:
  - /tmp/gate3_predictions.csv (Gate 3 V2 leak-free OOS predictions)
  - DB winners + ml_odds + pick3 payouts for 2026-05-02 → 2026-05-17

Outputs:
  - /home/strakajagr/EE_GATE3B_VERDICT_<ts>.md
  - /home/strakajagr/EE_GATE3B_VERDICT_<ts>.json
"""
import argparse
import json
import logging
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import boto3
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


def lambda_query(sql):
    cli = boto3.client('lambda', region_name='us-east-1')
    resp = cli.invoke(FunctionName='equine-ingestion',
                      Payload=json.dumps({'action': 'raw_query', 'sql': sql}).encode(),
                      InvocationType='RequestResponse')
    body = json.loads(resp['Payload'].read())
    if isinstance(body, dict) and body.get('statusCode') != 200:
        raise RuntimeError(f"Lambda error: {body}")
    inner = json.loads(body['body']) if 'body' in body else body
    return inner['rows']


def load_winners(start, end):
    """Per-race winner + ml_odds + closing_odds + field_size."""
    sql = f"""
        SELECT r.race_id::text AS race_id,
               r.race_date,
               t.track_code,
               r.race_number,
               res.horse_id::text AS winner_horse_id,
               e.morning_line_odds::float AS winner_ml_odds
        FROM results res
        JOIN races r USING(race_id)
        JOIN tracks t ON t.track_id = r.track_id
        LEFT JOIN entries e ON e.race_id = r.race_id AND e.horse_id = res.horse_id
        WHERE res.finish_position = 1
          AND r.race_date BETWEEN '{start}' AND '{end}'
    """
    rows = lambda_query(sql)
    df = pd.DataFrame(rows)
    df['race_date'] = pd.to_datetime(df['race_date'])
    df['race_number'] = df['race_number'].astype(int)
    df = df.drop_duplicates(subset=['track_code', 'race_date', 'race_number'], keep='first')
    return df


def load_market_and_field(start, end):
    """Per-(track, date, race_num, horse) closing_odds + ml_odds, for market
    ranking and field-size computation."""
    sql = f"""
        SELECT r.race_id::text AS race_id,
               r.race_date,
               t.track_code,
               r.race_number,
               e.horse_id::text AS horse_id,
               e.morning_line_odds::float AS ml_odds,
               pp.closing_odds::float AS closing_odds
        FROM entries e
        JOIN races r ON r.race_id = e.race_id
        JOIN tracks t ON t.track_id = r.track_id
        LEFT JOIN past_performances pp
               ON pp.horse_id = e.horse_id
              AND pp.race_date = r.race_date
              AND pp.track_code = t.track_code
              AND pp.race_number = r.race_number
        WHERE r.race_date BETWEEN '{start}' AND '{end}'
    """
    rows = lambda_query(sql)
    df = pd.DataFrame(rows)
    df['race_date'] = pd.to_datetime(df['race_date'])
    df['race_number'] = df['race_number'].astype(int)
    return df


def load_pick3_payouts(start, end):
    sql = f"""
        SELECT r.race_id::text AS race_id, r.race_date,
               t.track_code, r.race_number,
               res.pick3_payout::float AS pick3_payout,
               res.pick3_payout_base_unit::float AS base_unit
        FROM results res
        JOIN races r USING(race_id)
        JOIN tracks t ON t.track_id = r.track_id
        WHERE res.pick3_payout IS NOT NULL
          AND r.race_date BETWEEN '{start}' AND '{end}'
    """
    rows = lambda_query(sql)
    df = pd.DataFrame(rows)
    df['race_date'] = pd.to_datetime(df['race_date'])
    df['race_number'] = df['race_number'].astype(int)
    return df


def field_size_bucket(n):
    if n <= 6: return '≤6'
    if n <= 8: return '7-8'
    if n <= 10: return '9-10'
    return '11+'


# ─────────────────────────────────────────────────────────────────────
# §1 — TOP-K CONTAINMENT
# ─────────────────────────────────────────────────────────────────────

def containment_per_race(predictions, winners, market_field, max_k=5):
    """For each race in predictions, compute whether top-k by MODEL prob
    contains the actual winner. Also compute top-k by MARKET closing_odds.
    Stratify by field size."""
    pred = predictions.copy()
    pred['key'] = list(zip(pred['track_code'], pd.to_datetime(pred['race_date']), pred['race_number']))

    win_idx = winners.set_index(['track_code', 'race_date', 'race_number'])['winner_horse_id'].to_dict()

    # Build market-prob per horse (1/(closing_odds+1)) — fall back to ml_odds if missing
    mkt = market_field.copy()
    mkt['mkt_odds'] = mkt['closing_odds'].where(mkt['closing_odds'].notna(), mkt['ml_odds'])
    mkt['key'] = list(zip(mkt['track_code'], pd.to_datetime(mkt['race_date']), mkt['race_number']))

    results = []
    by_field = defaultdict(lambda: defaultdict(int))
    for key, grp in pred.groupby('key'):
        winner = win_idx.get(key)
        if winner is None:
            continue
        winner = str(winner)
        field_size = len(grp)

        sorted_model = grp.sort_values('pred_win_prob', ascending=False)
        model_top = list(sorted_model['horse_id'].astype(str).head(max_k))

        # Market ranking on the same race
        mkt_grp = mkt[mkt['key'] == key]
        mkt_grp_valid = mkt_grp[mkt_grp['mkt_odds'].notna() & (mkt_grp['mkt_odds'] > 0)]
        if len(mkt_grp_valid) > 0:
            mkt_sorted = mkt_grp_valid.sort_values('mkt_odds')  # lower odds = favorite
            mkt_top = list(mkt_sorted['horse_id'].astype(str).head(max_k))
        else:
            mkt_top = []

        bucket = field_size_bucket(field_size)
        by_field[bucket]['n_races'] += 1
        row = {
            'key': key,
            'field_size': field_size,
            'bucket': bucket,
            'winner': winner,
        }
        for k in range(1, max_k+1):
            mc = winner in model_top[:k]
            kc = winner in mkt_top[:k] if mkt_top else False
            row[f'model_top{k}_contains'] = int(mc)
            row[f'mkt_top{k}_contains']   = int(kc)
            by_field[bucket][f'model_top{k}_hits'] += int(mc)
            by_field[bucket][f'mkt_top{k}_hits'] += int(kc)
        results.append(row)

    df = pd.DataFrame(results)
    return df, by_field


def containment_summary(df, by_field, max_k=5):
    """Aggregate model and market top-k containment rates overall + by bucket."""
    n = len(df)
    overall = {}
    for k in range(1, max_k+1):
        overall[f'model_top{k}_pct'] = float(df[f'model_top{k}_contains'].mean() * 100)
        overall[f'mkt_top{k}_pct']   = float(df[f'mkt_top{k}_contains'].mean() * 100)
    buckets = {}
    for bucket, stats in by_field.items():
        nb = stats['n_races']
        b = {'n_races': nb}
        for k in range(1, max_k+1):
            b[f'model_top{k}_pct'] = 100.0 * stats[f'model_top{k}_hits'] / nb
            b[f'mkt_top{k}_pct']   = 100.0 * stats[f'mkt_top{k}_hits'] / nb
        buckets[bucket] = b
    return {'n_races': n, 'overall': overall, 'by_bucket': buckets}


# ─────────────────────────────────────────────────────────────────────
# §2 — P3 CONSTRUCTION MATRIX
# ─────────────────────────────────────────────────────────────────────

def rank_horses_per_race(predictions_df):
    out = {}
    for (tc, rd, rn), grp in predictions_df.groupby(['track_code', 'race_date', 'race_number']):
        sorted_grp = grp.sort_values('pred_win_prob', ascending=False)
        out[(tc, pd.Timestamp(rd), int(rn))] = list(zip(
            sorted_grp['horse_id'].astype(str),
            sorted_grp['pred_win_prob'].astype(float),
        ))
    return out


def build_p3_sequences(p3_payouts, winners):
    winners_dedup = winners.drop_duplicates(
        subset=['track_code', 'race_date', 'race_number'], keep='first'
    )
    winner_idx = winners_dedup.set_index(['track_code', 'race_date', 'race_number']).sort_index()
    sequences = []
    for _, p3 in p3_payouts.iterrows():
        tc = p3['track_code']
        rd = p3['race_date']
        last_leg = p3['race_number']
        leg_nums = [last_leg - 2, last_leg - 1, last_leg]
        if leg_nums[0] < 1:
            continue
        try:
            leg_winners = []
            leg_keys = []
            ml_odds_list = []
            for ln in leg_nums:
                w_row = winner_idx.loc[(tc, rd, ln)]
                if isinstance(w_row, pd.DataFrame):
                    w_row = w_row.iloc[0]
                leg_winners.append(str(w_row['winner_horse_id']))
                leg_keys.append((tc, rd, int(ln)))
                odds = w_row['winner_ml_odds']
                ml_odds_list.append(float(odds) if odds is not None and not pd.isna(odds) else None)
        except KeyError:
            continue
        has_longshot = any((o is not None and o >= 10.0) for o in ml_odds_list)
        which_legs_longshot = [
            (o is not None and o >= 10.0) for o in ml_odds_list
        ]
        sequences.append({
            'track_code': tc, 'race_date': rd, 'last_leg_race_number': last_leg,
            'leg_keys': leg_keys, 'leg_winners': leg_winners,
            'leg_ml_odds': ml_odds_list,
            'payout': float(p3['pick3_payout']),
            'base_unit': float(p3['base_unit']),
            'has_longshot_winner': has_longshot,
            'which_legs_longshot': which_legs_longshot,
        })
    return sequences


def construct_top_k(k):
    def fn(race_horses):
        return [h for h, _ in race_horses[:k]]
    return fn


def construct_top_k_legs(k_per_leg):
    """e.g. k_per_leg=(4,4,3) means top-4, top-4, top-3 on legs 0,1,2."""
    def fn_factory(leg_idx):
        k = k_per_leg[leg_idx]
        def fn(race_horses):
            return [h for h, _ in race_horses[:k]]
        return fn
    return fn_factory


def construct_convicted(threshold, cap=4):
    def fn(race_horses):
        picks = [h for h, p in race_horses if p >= threshold]
        if not picks:
            picks = [race_horses[0][0]]
        return picks[:cap]
    return fn


def evaluate_uniform(sequences, ranked_by_race, construction_fn, name):
    """Same k per leg."""
    return _evaluate(sequences, ranked_by_race, [construction_fn]*3, name)


def evaluate_per_leg(sequences, ranked_by_race, fn_factory, name):
    """Different fn per leg (used for 4×4×3 etc)."""
    fns = [fn_factory(i) for i in range(3)]
    return _evaluate(sequences, ranked_by_race, fns, name)


def _evaluate(sequences, ranked_by_race, fns, name):
    n_eligible = 0
    n_hit = 0
    total_cost = 0.0
    hit_payouts = []
    longshot_hits_payouts = []
    chalk_hits_payouts = []
    chalk_only_losses_cost = 0.0
    chalk_only_n = 0
    longshot_present_n = 0
    longshot_present_cost = 0.0
    longshot_winner_in_top4_hits = 0
    longshot_winner_in_top4_misses = 0

    for seq in sequences:
        try:
            picks = []
            for i, leg_key in enumerate(seq['leg_keys']):
                horses = ranked_by_race.get(leg_key)
                if not horses:
                    raise ValueError("no predictions")
                cand = fns[i](horses)
                if not cand:
                    raise ValueError("empty candidates")
                picks.append([str(h) for h in cand])
        except (KeyError, ValueError):
            continue

        n_eligible += 1
        ticket_size = picks[0].__len__() * picks[1].__len__() * picks[2].__len__()
        cost = ticket_size * seq['base_unit']
        total_cost += cost

        hit = all(seq['leg_winners'][i] in picks[i] for i in range(3))
        if hit:
            n_hit += 1
            hit_payouts.append(seq['payout'])
            if seq['has_longshot_winner']:
                longshot_hits_payouts.append(seq['payout'])
            else:
                chalk_hits_payouts.append(seq['payout'])

        # Downside-by-class accounting
        if seq['has_longshot_winner']:
            longshot_present_n += 1
            longshot_present_cost += cost
            # For each leg where the winner had ml_odds≥10, was it in our picks?
            for i in range(3):
                if seq['which_legs_longshot'][i]:
                    if seq['leg_winners'][i] in picks[i]:
                        longshot_winner_in_top4_hits += 1
                    else:
                        longshot_winner_in_top4_misses += 1
        else:
            chalk_only_n += 1
            if not hit:
                chalk_only_losses_cost += cost

    def metrics(payouts, total_cost):
        pnl = sum(payouts) - total_cost
        roi = pnl / total_cost if total_cost > 0 else 0.0
        return {
            'n_hits': len(payouts),
            'hit_rate_pct': 100.0 * len(payouts) / max(n_eligible, 1),
            'total_cost': round(total_cost, 2),
            'total_payout': round(sum(payouts), 2),
            'flat_pnl': round(pnl, 2),
            'flat_roi_pct': round(roi * 100.0, 2),
            'avg_payout_when_hit': round(np.mean(payouts), 2) if payouts else 0.0,
        }

    base = metrics(hit_payouts, total_cost)
    sorted_hits = sorted(hit_payouts, reverse=True)
    s1 = metrics(sorted_hits[1:], total_cost) if hit_payouts else base
    s3 = metrics(sorted_hits[3:], total_cost) if len(sorted_hits) >= 3 else s1

    # Verdict
    if base['n_hits'] < 30:
        verdict = 'INSUFFICIENT-SAMPLE'
    elif base['flat_roi_pct'] <= 0:
        verdict = 'NO-EDGE'
    elif s3['flat_roi_pct'] > 0:
        verdict = 'REAL-EDGE'
    else:
        verdict = 'FRAGILE'

    avg_cost = total_cost / max(n_eligible, 1)
    return {
        'construction': name,
        'n_sequences_played': n_eligible,
        'avg_ticket_cost': round(avg_cost, 2),
        'baseline': base,
        'strip_1': s1,
        'strip_3': s3,
        'verdict': verdict,
        'downside_analysis': {
            'chalk_only_n': chalk_only_n,
            'chalk_only_losses_cost': round(chalk_only_losses_cost, 2),
            'chalk_only_hits_n': len(chalk_hits_payouts),
            'chalk_only_hits_total_payout': round(sum(chalk_hits_payouts), 2),
            'longshot_present_n': longshot_present_n,
            'longshot_present_total_cost': round(longshot_present_cost, 2),
            'longshot_hits_n': len(longshot_hits_payouts),
            'longshot_hits_total_payout': round(sum(longshot_hits_payouts), 2),
            'longshot_winner_in_picks_count': longshot_winner_in_top4_hits,
            'longshot_winner_missed_count': longshot_winner_in_top4_misses,
            'longshot_winner_capture_rate_pct': (
                100.0 * longshot_winner_in_top4_hits /
                max(longshot_winner_in_top4_hits + longshot_winner_in_top4_misses, 1)
            ),
        },
    }


# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--predictions', default='/tmp/gate3_predictions.csv')
    parser.add_argument('--start', default='2026-05-02')
    parser.add_argument('--end', default='2026-05-17')
    parser.add_argument('--out-prefix', default='/home/strakajagr/EE_GATE3B_VERDICT')
    args = parser.parse_args()

    logger.info("Loading predictions, winners, market, P3 payouts")
    preds = pd.read_csv(args.predictions)
    preds['race_date'] = pd.to_datetime(preds['race_date'])
    winners = load_winners(args.start, args.end)
    market = load_market_and_field(args.start, args.end)
    p3_payouts = load_pick3_payouts(args.start, args.end)
    logger.info(f"  preds={len(preds):,} ({preds['race_id'].nunique()} races)  "
                f"winners={len(winners)}  market={len(market):,}  p3={len(p3_payouts)}")

    # ── §1 Top-K containment ─────────────────────────────────────────
    logger.info("§1 — top-K containment per race")
    cdf, by_field = containment_per_race(preds, winners, market, max_k=5)
    summary = containment_summary(cdf, by_field, max_k=5)

    print("\n" + "=" * 90)
    print("§1 — TOP-K WINNER CONTAINMENT (model vs MARKET)")
    print("=" * 90)
    print(f"  n_races (containment eval): {summary['n_races']}")
    print(f"  {'k':>3}  {'model%':>8}  {'mkt%':>7}  {'gap':>7}")
    for k in range(1, 6):
        m = summary['overall'][f'model_top{k}_pct']
        kt = summary['overall'][f'mkt_top{k}_pct']
        print(f"  {k:>3}  {m:>7.1f}%  {kt:>6.1f}%  {m - kt:>+6.1f}pp")

    print("\n  By field size:")
    print(f"  {'bucket':>8}  {'n':>4}  {'model t1':>9}  {'model t2':>9}  {'model t3':>9}  "
          f"{'model t4':>9}  {'model t5':>9}  {'mkt t4':>8}")
    for b in ['≤6', '7-8', '9-10', '11+']:
        if b in summary['by_bucket']:
            v = summary['by_bucket'][b]
            print(f"  {b:>8}  {v['n_races']:>4}  "
                  f"{v['model_top1_pct']:>8.1f}%  {v['model_top2_pct']:>8.1f}%  "
                  f"{v['model_top3_pct']:>8.1f}%  {v['model_top4_pct']:>8.1f}%  "
                  f"{v['model_top5_pct']:>8.1f}%  {v['mkt_top4_pct']:>7.1f}%")

    # ── §2 P3 construction matrix (4-leg-focused) ────────────────────
    logger.info("§2 — building P3 sequences + ranked horses")
    seqs = build_p3_sequences(p3_payouts, winners)
    ranked = rank_horses_per_race(preds)
    logger.info(f"  {len(seqs)} P3 sequences, {len(ranked)} predicted races")

    constructions = {}
    constructions['4x4x4'] = evaluate_uniform(seqs, ranked, construct_top_k(4), '4x4x4')
    constructions['4x4x3'] = evaluate_per_leg(seqs, ranked, construct_top_k_legs((4,4,3)), '4x4x3')
    constructions['4x3x3'] = evaluate_per_leg(seqs, ranked, construct_top_k_legs((4,3,3)), '4x3x3')
    # Reference points from Gate 3 — re-run on the same predictions
    constructions['3x3x3'] = evaluate_uniform(seqs, ranked, construct_top_k(3), '3x3x3')
    constructions['2x2x2'] = evaluate_uniform(seqs, ranked, construct_top_k(2), '2x2x2')

    # CONVICTED capped at 4 — finer sweep
    for thr in (0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20):
        n = f'CONVICTED_t{thr:.2f}_cap4'
        constructions[n] = evaluate_uniform(seqs, ranked, construct_convicted(thr, cap=4), n)

    print("\n" + "=" * 110)
    print("§2 — P3 CONSTRUCTION MATRIX")
    print("=" * 110)
    print(f"{'Construction':<24}{'plays':>7}{'avg_cost$':>11}{'hits':>6}{'hit%':>7}"
          f"{'total_cost$':>13}{'total_pay$':>13}{'flat_pnl$':>11}{'flat_ROI':>10}"
          f"{'strip1_ROI':>11}{'strip3_ROI':>11}{'verdict':>22}")
    print("-" * 110)
    for name, c in constructions.items():
        b = c['baseline']
        s1 = c['strip_1']; s3 = c['strip_3']
        print(f"{name:<24}{c['n_sequences_played']:>7}{c['avg_ticket_cost']:>10.2f} "
              f"{b['n_hits']:>5} {b['hit_rate_pct']:>6.1f}% "
              f"{b['total_cost']:>12,.0f} {b['total_payout']:>12,.0f} "
              f"{b['flat_pnl']:>+10,.0f} {b['flat_roi_pct']:>+9.2f}% "
              f"{s1['flat_roi_pct']:>+10.2f}% {s3['flat_roi_pct']:>+10.2f}% "
              f"{c['verdict']:>22}")

    # ── §3 downside + longshot capture (for 4x4x4) ───────────────────
    c44 = constructions['4x4x4']
    da = c44['downside_analysis']
    print("\n" + "=" * 80)
    print("§3 — 4×4×4 DOWNSIDE + LONGSHOT-CAPTURE")
    print("=" * 80)
    print(f"  Chalk-only sequences (no leg won by ml≥10): n={da['chalk_only_n']}")
    print(f"    Hits: {da['chalk_only_hits_n']}  total payout: ${da['chalk_only_hits_total_payout']:.2f}")
    print(f"    Losses cost on misses: ${da['chalk_only_losses_cost']:.2f}")
    print(f"  Longshot-present sequences (≥1 leg won by ml≥10): n={da['longshot_present_n']}")
    print(f"    Hits: {da['longshot_hits_n']}  total payout: ${da['longshot_hits_total_payout']:.2f}")
    print(f"    Total cost: ${da['longshot_present_total_cost']:.2f}")
    print(f"  Longshot WINNER capture: in our top-4 = {da['longshot_winner_in_picks_count']} / "
          f"missed = {da['longshot_winner_missed_count']}  "
          f"(rate = {da['longshot_winner_capture_rate_pct']:.1f}%)")

    # ── Save ─────────────────────────────────────────────────────────
    out = {
        'gate': 'gate_3b',
        'eval_window': [args.start, args.end],
        'predictions_source': 'gate3_v2_leakfree_lean53_top5_traj_minus_lasix',
        'top_k_containment': summary,
        'constructions': constructions,
    }
    ts = datetime.utcnow().strftime('%Y%m%d_%H%M')
    json_path = f'{args.out_prefix}_{ts}.json'
    Path(json_path).write_text(json.dumps(out, indent=2, default=str))
    write_md(out, f'{args.out_prefix}_{ts}.md')
    print(f"\nJSON: {json_path}")
    print(f"MD:   {args.out_prefix}_{ts}.md")


def write_md(out, path):
    s = out['top_k_containment']
    lines = [
        "# EE GATE 3B — TOP-4 CONTAINMENT + 4×4×4 P3 VERDICT",
        f"\n**Date:** {datetime.utcnow().date()}",
        f"**Eval window:** {out['eval_window'][0]} → {out['eval_window'][1]}",
        f"**Predictions:** {out['predictions_source']} (Gate 3 leak-free OOS)",
        f"**n races (containment):** {s['n_races']}",
        "",
        "## §1 — TOP-K WINNER CONTAINMENT (model vs MARKET)",
        "",
        "Overall:",
        "",
        "| k | model containment | market containment | gap |",
        "|---|---|---|---|",
    ]
    for k in range(1, 6):
        m = s['overall'][f'model_top{k}_pct']
        mk = s['overall'][f'mkt_top{k}_pct']
        lines.append(f"| {k} | {m:.1f}% | {mk:.1f}% | {m - mk:+.1f}pp |")
    lines += [
        "",
        "By field size:",
        "",
        "| field | n_races | model t1 | model t2 | model t3 | model t4 | model t5 | market t4 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for b in ['≤6', '7-8', '9-10', '11+']:
        if b in s['by_bucket']:
            v = s['by_bucket'][b]
            lines.append(
                f"| {b} | {v['n_races']} | {v['model_top1_pct']:.1f}% | "
                f"{v['model_top2_pct']:.1f}% | {v['model_top3_pct']:.1f}% | "
                f"**{v['model_top4_pct']:.1f}%** | {v['model_top5_pct']:.1f}% | "
                f"{v['mkt_top4_pct']:.1f}% |"
            )

    lines += [
        "",
        "## §2 — P3 CONSTRUCTION MATRIX",
        "",
        "| Construction | plays | avg cost | hits | hit% | total cost | total payout | flat PnL | flat ROI | strip-1 ROI | strip-3 ROI | verdict |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for name, c in out['constructions'].items():
        b = c['baseline']; s1 = c['strip_1']; s3 = c['strip_3']
        lines.append(
            f"| {name} | {c['n_sequences_played']} | ${c['avg_ticket_cost']:.2f} | "
            f"{b['n_hits']} | {b['hit_rate_pct']:.1f}% | "
            f"${b['total_cost']:,.0f} | ${b['total_payout']:,.0f} | "
            f"${b['flat_pnl']:+,.0f} | {b['flat_roi_pct']:+.2f}% | "
            f"{s1['flat_roi_pct']:+.2f}% | {s3['flat_roi_pct']:+.2f}% | **{c['verdict']}** |"
        )

    lines += [
        "",
        "## §3 — 4×4×4 DOWNSIDE + LONGSHOT CAPTURE",
        "",
    ]
    da = out['constructions']['4x4x4']['downside_analysis']
    lines += [
        f"- **Chalk-only sequences** (no leg won by ml-odds ≥ 10): n = {da['chalk_only_n']}",
        f"  - Hits: {da['chalk_only_hits_n']}, total payout: \\${da['chalk_only_hits_total_payout']:,.2f}",
        f"  - Losses cost on chalk-only misses: \\${da['chalk_only_losses_cost']:,.2f}",
        f"- **Longshot-present sequences** (≥1 leg won by ml-odds ≥ 10): n = {da['longshot_present_n']}",
        f"  - Hits: {da['longshot_hits_n']}, total payout: \\${da['longshot_hits_total_payout']:,.2f}",
        f"  - Total ticket cost: \\${da['longshot_present_total_cost']:,.2f}",
        f"- **Longshot winner capture (the extraction question):**",
        f"  - Winner of a longshot-winning leg was in our top-4: **{da['longshot_winner_in_picks_count']}** times",
        f"  - Missed entirely: **{da['longshot_winner_missed_count']}** times",
        f"  - **Capture rate: {da['longshot_winner_capture_rate_pct']:.1f}%**",
    ]
    Path(path).write_text("\n".join(lines))


if __name__ == '__main__':
    main()
