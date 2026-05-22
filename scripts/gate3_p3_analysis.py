"""Gate 3 §4 — P3 construction matrix on the rebuilt model's win-prob.

Inputs:
  - V1 (rebuilt model) per-race per-horse win-prob predictions
    (we re-run V1 prediction locally from the diagnostic's eval window)
  - results.pick3_payout / pick3_payout_base_unit per race (DB)

Construction matrix (every construction NAMED):
  - 1x1x1 — pick exactly 1 horse per leg
  - 2x2x2 — pick top-2 per leg
  - 3x3x3 — pick top-3 per leg
  - CONVICTED — include horses above win-prob threshold (capped 4/leg),
                sweep threshold 0.10 → 0.25

For each construction:
  - Per P3 sequence: ticket cost = product of leg sizes × base_unit
  - HIT if our picks contain the winner of every leg
  - flat_bet_ROI = (sum(payouts on hits) - sum(ticket cost across ALL sequences)) / sum(ticket costs)
  - Hit rate = hits / sequences_eligible
  - Avg payout when hit, sample size, ticket cost summary
  - Strip-top-1 and strip-top-3: re-compute removing the 1 / 3 biggest winners

For CONVICTED: longshot vs chalk profit split.
  - LONGSHOT-CONTAINING: any winning leg's actual winner had ml_odds ≥ 10
  - CHALK-ONLY: every winning leg's winner had ml_odds < 10

Verdict per construction:
  - REAL EDGE (flat ROI > 0 AND strip-3 still > 0)
  - FRAGILE (flat ROI > 0 BUT strip-3 ≤ 0)
  - NO EDGE (flat ROI ≤ 0)
  - INSUFFICIENT-SAMPLE (< 30 hits)

Output: /home/strakajagr/EE_GATE3_P3_VERDICT_<ts>.md +
        /home/strakajagr/EE_GATE3_P3_VERDICT_<ts>.json
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
    """Run a SELECT via the equine-ingestion Lambda raw_query action."""
    cli = boto3.client('lambda', region_name='us-east-1')
    payload = json.dumps({'action': 'raw_query', 'sql': sql}).encode()
    resp = cli.invoke(FunctionName='equine-ingestion',
                      Payload=payload,
                      InvocationType='RequestResponse')
    body = json.loads(resp['Payload'].read())
    if isinstance(body, dict) and body.get('statusCode') != 200:
        raise RuntimeError(f"Lambda error: {body}")
    inner = json.loads(body['body']) if 'body' in body else body
    return inner['rows']


def load_predictions(predictions_csv):
    """V1 predictions CSV: race_id, horse_id, pred_win_prob, race_date, race_number, track_code"""
    df = pd.read_csv(predictions_csv)
    df['race_date'] = pd.to_datetime(df['race_date'])
    return df


def load_pick3_payouts(start, end):
    """Pull all P3 results in the eval window. The pick3_payout is printed
    on the LAST leg of the sequence, per Gate 2 calc-audit finding."""
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
        ORDER BY t.track_code, r.race_date, r.race_number
    """
    rows = lambda_query(sql)
    df = pd.DataFrame(rows)
    df['race_date'] = pd.to_datetime(df['race_date'])
    df['race_number'] = df['race_number'].astype(int)
    return df


def load_winners_and_odds(start, end):
    """Per-race winner + ml_odds for longshot detection."""
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
    return df


def build_p3_sequences(p3_payouts, winners):
    """For each P3 row (last leg = N+2), find races N, N+1, N+2 at same
    track/date. Returns list keyed by (track, date, race_number) tuples."""
    # De-duplicate winners by (track, date, race_number) — multiple finish_position=1
    # rows can exist for dead-heat races; we want one canonical winner per leg.
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
            continue  # missing leg winner

        has_longshot = any((o is not None and o >= 10.0) for o in ml_odds_list)
        sequences.append({
            'track_code': tc,
            'race_date': rd,
            'last_leg_race_number': last_leg,
            'leg_keys': leg_keys,   # list of (tc, rd, rn) tuples
            'leg_winners': leg_winners,
            'payout': float(p3['pick3_payout']),
            'base_unit': float(p3['base_unit']),
            'has_longshot_winner': has_longshot,
        })
    return sequences


def rank_horses_per_race(predictions_df):
    """Return dict (track_code, race_date, race_number) -> list of
    (horse_id, win_prob) sorted desc."""
    out = {}
    for (tc, rd, rn), grp in predictions_df.groupby(['track_code', 'race_date', 'race_number']):
        sorted_grp = grp.sort_values('pred_win_prob', ascending=False)
        out[(tc, pd.Timestamp(rd), int(rn))] = list(zip(
            sorted_grp['horse_id'].astype(str),
            sorted_grp['pred_win_prob'].astype(float),
        ))
    return out


def evaluate_construction(sequences, ranked_by_race, construction_fn, name):
    """Generic evaluator. construction_fn(race_horses) -> list of horse_ids
    we'd play in that leg."""
    n_eligible = 0
    n_hit = 0
    total_cost = 0.0
    total_payout = 0.0
    hit_payouts = []  # for strip-N analysis
    longshot_hits = []   # payouts for longshot-containing winners
    chalk_hits = []      # payouts for chalk-only winners
    per_seq = []

    for seq in sequences:
        # Construct ticket: for each leg, pick our candidates
        picks = []
        try:
            for leg_key in seq['leg_keys']:
                horses = ranked_by_race.get(leg_key)
                if not horses:
                    raise ValueError("no predictions for this race")
                cand = construction_fn(horses)
                if not cand:
                    raise ValueError("empty candidate set")
                picks.append([str(h) for h in cand])
        except (KeyError, ValueError):
            continue  # not eligible (missing predictions)

        n_eligible += 1
        ticket_size = picks[0].__len__() * picks[1].__len__() * picks[2].__len__()
        cost = ticket_size * seq['base_unit']
        total_cost += cost

        hit = all(seq['leg_winners'][i] in picks[i] for i in range(3))
        if hit:
            n_hit += 1
            total_payout += seq['payout']
            hit_payouts.append(seq['payout'])
            if seq['has_longshot_winner']:
                longshot_hits.append(seq['payout'])
            else:
                chalk_hits.append(seq['payout'])
        per_seq.append({'cost': cost, 'hit': hit, 'payout': seq['payout'] if hit else 0.0,
                       'longshot': seq['has_longshot_winner']})

    def compute_metrics(hit_payouts, total_cost):
        pnl = sum(hit_payouts) - total_cost
        roi = pnl / total_cost if total_cost > 0 else 0.0
        return {
            'n_eligible': n_eligible,
            'n_hit': len(hit_payouts),
            'hit_rate_pct': 100.0 * len(hit_payouts) / max(n_eligible, 1),
            'total_ticket_cost': round(total_cost, 2),
            'total_payout': round(sum(hit_payouts), 2),
            'flat_pnl': round(pnl, 2),
            'flat_roi_pct': round(roi * 100.0, 2),
            'avg_payout_when_hit': round(np.mean(hit_payouts), 2) if hit_payouts else 0.0,
        }

    base = compute_metrics(hit_payouts, total_cost)

    # Strip-top-N analyses
    sorted_hits = sorted(hit_payouts, reverse=True)
    strip_1 = compute_metrics(sorted_hits[1:], total_cost) if len(sorted_hits) > 0 else base
    strip_3 = compute_metrics(sorted_hits[3:], total_cost) if len(sorted_hits) >= 3 else strip_1

    # Verdict
    if base['n_hit'] < 30:
        verdict = 'INSUFFICIENT-SAMPLE'
    elif base['flat_roi_pct'] <= 0:
        verdict = 'NO-EDGE'
    elif strip_3['flat_roi_pct'] > 0:
        verdict = 'REAL-EDGE'
    else:
        verdict = 'FRAGILE'

    # Longshot vs chalk split (only meaningful for hits)
    n_ls_hits = len(longshot_hits)
    n_chalk_hits = len(chalk_hits)
    ls_share = sum(longshot_hits) / max(sum(hit_payouts), 1e-9) if hit_payouts else 0.0
    chalk_share = sum(chalk_hits) / max(sum(hit_payouts), 1e-9) if hit_payouts else 0.0

    return {
        'construction': name,
        'baseline': base,
        'strip_1': strip_1,
        'strip_3': strip_3,
        'verdict': verdict,
        'longshot_chalk_split': {
            'n_longshot_hits': n_ls_hits,
            'n_chalk_hits': n_chalk_hits,
            'longshot_payout_share_pct': round(ls_share * 100.0, 2),
            'chalk_payout_share_pct':    round(chalk_share * 100.0, 2),
            'avg_longshot_payout': round(np.mean(longshot_hits), 2) if longshot_hits else 0.0,
            'avg_chalk_payout':    round(np.mean(chalk_hits), 2)    if chalk_hits else 0.0,
        },
    }


def construction_top_k(k):
    def fn(race_horses):
        return [h for h, _ in race_horses[:k]]
    return fn


def construction_convicted(threshold, max_picks=4):
    def fn(race_horses):
        picks = [h for h, p in race_horses if p >= threshold]
        if not picks:
            picks = [race_horses[0][0]]  # fallback: top-1 if no one clears threshold
        return picks[:max_picks]
    return fn


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--predictions', required=True,
                        help='CSV with race_id, horse_id, pred_win_prob, race_date, race_number, track_code')
    parser.add_argument('--start', default='2026-05-02')
    parser.add_argument('--end', default='2026-05-17')
    parser.add_argument('--out-prefix', default='/home/strakajagr/EE_GATE3_P3_VERDICT')
    args = parser.parse_args()

    logger.info(f"Loading predictions from {args.predictions}")
    preds = load_predictions(args.predictions)
    logger.info(f"  {len(preds):,} prediction rows across {preds['race_id'].nunique()} races")

    logger.info(f"Loading P3 payouts {args.start}..{args.end}")
    p3_payouts = load_pick3_payouts(args.start, args.end)
    logger.info(f"  {len(p3_payouts)} P3 payout rows")

    logger.info("Loading winners + ml_odds")
    winners = load_winners_and_odds(args.start, args.end)
    logger.info(f"  {len(winners)} winners")

    logger.info("Building P3 sequences")
    sequences = build_p3_sequences(p3_payouts, winners)
    logger.info(f"  {len(sequences)} complete P3 sequences")

    logger.info("Ranking horses per race")
    ranked = rank_horses_per_race(preds)

    results = {
        'gate': 'gate_3',
        'eval_window': [args.start, args.end],
        'n_sequences': len(sequences),
        'constructions': {},
    }

    # Symmetric baselines
    for k in (1, 2, 3):
        name = f'{k}x{k}x{k}'
        results['constructions'][name] = evaluate_construction(
            sequences, ranked, construction_top_k(k), name
        )

    # CONVICTED — sweep
    for threshold in (0.10, 0.12, 0.15, 0.18, 0.20, 0.25):
        name = f'CONVICTED_t{threshold:.2f}'
        results['constructions'][name] = evaluate_construction(
            sequences, ranked, construction_convicted(threshold, max_picks=4), name
        )

    # Save
    ts = datetime.utcnow().strftime('%Y%m%d_%H%M')
    json_path = f'{args.out_prefix}_{ts}.json'
    Path(json_path).write_text(json.dumps(results, indent=2, default=str))

    md_path = f'{args.out_prefix}_{ts}.md'
    write_markdown(results, md_path)

    # Console summary
    print("\n" + "=" * 80)
    print(f"GATE 3 §4 — P3 CONSTRUCTION MATRIX (n_sequences={len(sequences)})")
    print("=" * 80)
    print(f"{'Construction':<22} {'Hits':>6} {'Hit%':>7} {'Flat ROI':>10} "
          f"{'Strip-1 ROI':>12} {'Strip-3 ROI':>12} {'Verdict':>22}")
    print("-" * 100)
    for name, r in results['constructions'].items():
        b = r['baseline']
        s1 = r['strip_1']
        s3 = r['strip_3']
        print(f"{name:<22} {b['n_hit']:>6} {b['hit_rate_pct']:>6.1f}% "
              f"{b['flat_roi_pct']:>+9.2f}% {s1['flat_roi_pct']:>+11.2f}% "
              f"{s3['flat_roi_pct']:>+11.2f}% {r['verdict']:>22}")
    print(f"\nFull JSON: {json_path}\nFull MD:   {md_path}")


def write_markdown(results, path):
    lines = [
        "# EE GATE 3 §4 — P3 CONSTRUCTION MATRIX VERDICT",
        f"\n**Date:** {datetime.utcnow().date()}",
        f"**Eval window:** {results['eval_window'][0]} → {results['eval_window'][1]}",
        f"**P3 sequences evaluated:** {results['n_sequences']}",
        "",
        "## Construction matrix (every construction NAMED)",
        "",
        "| Construction | n_hits | hit_rate | flat ROI | strip-1 ROI | strip-3 ROI | longshot share | verdict |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for name, r in results['constructions'].items():
        b = r['baseline']
        s1 = r['strip_1']
        s3 = r['strip_3']
        ls = r['longshot_chalk_split']
        lines.append(
            f"| {name} | {b['n_hit']} | {b['hit_rate_pct']:.1f}% | "
            f"{b['flat_roi_pct']:+.2f}% | {s1['flat_roi_pct']:+.2f}% | "
            f"{s3['flat_roi_pct']:+.2f}% | LS {ls['longshot_payout_share_pct']:.0f}% / "
            f"chalk {ls['chalk_payout_share_pct']:.0f}% | **{r['verdict']}** |"
        )

    lines += [
        "",
        "## Verdict legend",
        "- **REAL-EDGE**: flat ROI > 0 AND strip-3 ROI > 0 (survives removing 3 biggest winners)",
        "- **FRAGILE**: flat ROI > 0 but strip-3 ROI ≤ 0 (carried by a handful of big hits)",
        "- **NO-EDGE**: flat ROI ≤ 0",
        "- **INSUFFICIENT-SAMPLE**: fewer than 30 hits",
        "",
        "## Longshot vs chalk profit split (per construction)",
        "",
        "| Construction | n_LS_hits | n_chalk_hits | LS payout share | chalk payout share | avg LS payout | avg chalk payout |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, r in results['constructions'].items():
        ls = r['longshot_chalk_split']
        lines.append(
            f"| {name} | {ls['n_longshot_hits']} | {ls['n_chalk_hits']} | "
            f"{ls['longshot_payout_share_pct']:.1f}% | {ls['chalk_payout_share_pct']:.1f}% | "
            f"${ls['avg_longshot_payout']:.2f} | ${ls['avg_chalk_payout']:.2f} |"
        )
    lines.append("\n*LS = at least one of the three winning horses had morning-line odds ≥ 10.*")

    Path(path).write_text("\n".join(lines))


if __name__ == '__main__':
    main()
