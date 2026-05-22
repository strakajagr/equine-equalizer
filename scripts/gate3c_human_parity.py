"""Gate 3C §3.2 — human-parity probe: does a trivial speed-figure-only
heuristic beat the ML models on top-4 containment?

Construct a dead-simple baseline for each (race, horse) in the OOS window:
score = most recent computed_speed_figure (or best_speed_last_90d as a
secondary check), strictly from PRE-RACE PPs (race_date < target race_date).
Rank within race. Compare top-K containment to the §1 model table.
"""
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


START = '2026-05-02'
END = '2026-05-17'


def fetch_baselines(start, end):
    """For each (race, horse) in the OOS window: compute trivial baselines
    using strictly-prior PPs. Returns DataFrame keyed by race_id+horse_id."""
    # Use a CTE-style subquery: for each entry, get the horse's most recent
    # PP with race_date < race_date and a speed figure populated.
    sql = f"""
        SELECT
          e.race_id::text AS race_id,
          e.horse_id::text AS horse_id,
          t.track_code,
          r.race_date,
          r.race_number,
          e.morning_line_odds::float AS ml_odds,
          (
            SELECT pp.computed_speed_figure
            FROM past_performances pp
            WHERE pp.horse_id = e.horse_id
              AND pp.race_date < r.race_date
              AND pp.computed_speed_figure IS NOT NULL
            ORDER BY pp.race_date DESC LIMIT 1
          )::float AS speed_fig_last,
          (
            SELECT MAX(pp.computed_speed_figure)
            FROM past_performances pp
            WHERE pp.horse_id = e.horse_id
              AND pp.race_date < r.race_date
              AND pp.race_date >= (r.race_date - INTERVAL '90 days')
              AND pp.computed_speed_figure IS NOT NULL
          )::float AS speed_fig_best_90d,
          (
            SELECT AVG(pp.computed_speed_figure)
            FROM past_performances pp
            WHERE pp.horse_id = e.horse_id
              AND pp.race_date < r.race_date
              AND pp.computed_speed_figure IS NOT NULL
              AND pp.race_date IN (
                  SELECT pp2.race_date FROM past_performances pp2
                  WHERE pp2.horse_id = e.horse_id
                    AND pp2.race_date < r.race_date
                    AND pp2.computed_speed_figure IS NOT NULL
                  ORDER BY pp2.race_date DESC LIMIT 3
              )
          )::float AS speed_fig_avg_3
        FROM entries e
        JOIN races r ON r.race_id = e.race_id
        JOIN tracks t ON t.track_id = r.track_id
        WHERE r.race_date BETWEEN '{start}' AND '{end}'
    """
    rows = lambda_query(sql)
    df = pd.DataFrame(rows)
    df['race_date'] = pd.to_datetime(df['race_date'])
    df['race_number'] = df['race_number'].astype(int)
    return df


def fetch_winners(start, end):
    sql = f"""
        SELECT r.race_id::text AS race_id,
               res.horse_id::text AS winner_horse_id
        FROM results res
        JOIN races r USING(race_id)
        WHERE res.finish_position = 1
          AND r.race_date BETWEEN '{start}' AND '{end}'
    """
    rows = lambda_query(sql)
    df = pd.DataFrame(rows)
    df = df.drop_duplicates('race_id')
    return df


def field_size_bucket(n):
    if n <= 6: return '≤6'
    if n <= 8: return '7-8'
    if n <= 10: return '9-10'
    return '11+'


def score_baseline(df, score_col, winners_map, ascending=False, max_k=5):
    """Rank by score_col within race, return top-K containment overall + by field."""
    d = df.dropna(subset=[score_col]).copy()
    n_races = 0
    overall = defaultdict(int)
    by_field = defaultdict(lambda: defaultdict(int))
    for race_id, grp in df.groupby('race_id'):
        # Use FULL race for field size (count all entries with this race_id),
        # but rank only horses that have a score
        fs = len(grp)
        bucket = field_size_bucket(fs)
        scored = grp.dropna(subset=[score_col])
        if len(scored) == 0:
            continue
        # For containment: rank only scored horses; if winner has no score, miss
        winner = winners_map.get(str(race_id))
        if winner is None:
            continue
        ranked = list(scored.sort_values(score_col, ascending=ascending)['horse_id'].astype(str))
        n_races += 1
        by_field[bucket]['n_races'] += 1
        for k in range(1, max_k+1):
            hit = int(str(winner) in ranked[:k])
            overall[f'top{k}_hits'] += hit
            by_field[bucket][f'top{k}_hits'] += hit
    if n_races == 0:
        return None
    r = {'n_races_scored': n_races}
    for k in range(1, max_k+1):
        r[f'top{k}_pct'] = 100.0 * overall[f'top{k}_hits'] / n_races
    r['by_field'] = {}
    for b in ['≤6', '7-8', '9-10', '11+']:
        if b in by_field:
            nb = by_field[b]['n_races']
            r['by_field'][b] = {'n_races': nb}
            for k in range(1, max_k+1):
                r['by_field'][b][f'top{k}_pct'] = 100.0 * by_field[b][f'top{k}_hits'] / nb
    return r


def main():
    logger.info(f"Loading baselines + winners for {START}..{END}")
    df = fetch_baselines(START, END)
    winners = fetch_winners(START, END)
    winners_map = winners.set_index('race_id')['winner_horse_id'].to_dict()
    logger.info(f"  {len(df):,} entries  {df['race_id'].nunique()} races  "
                f"{len(winners)} winners")

    # Coverage check
    print(f"\nCoverage of pre-race speed-figure baselines (out of {len(df):,} entries):")
    for col in ['speed_fig_last', 'speed_fig_best_90d', 'speed_fig_avg_3']:
        pct = df[col].notna().mean() * 100
        print(f"  {col:<25}  non-null: {df[col].notna().sum():>5} ({pct:.1f}%)")

    # Also: ml_odds-only (in case the model's win_prob is just a noisy version of ML odds)
    print()

    # Score each baseline
    baselines = [
        ('speed_fig_last',      'speed_fig_last',      False),  # higher = better
        ('speed_fig_best_90d',  'speed_fig_best_90d',  False),
        ('speed_fig_avg_3',     'speed_fig_avg_3',     False),
        ('ml_odds_inverse',     'ml_odds',             True),   # lower odds = favorite
    ]
    results = {}
    for name, col, asc in baselines:
        r = score_baseline(df, col, winners_map, ascending=asc)
        if r is None:
            continue
        results[name] = r

    # Print
    print("=" * 100)
    print("§3.2 — HUMAN-PARITY PROBE (trivial baselines vs ML)")
    print("=" * 100)
    print(f"{'baseline':<24}{'n':>6}{'top1':>9}{'top2':>9}{'top3':>9}{'top4':>9}{'top5':>9}")
    print("-" * 75)
    for name, r in sorted(results.items(), key=lambda kv: -kv[1]['top4_pct']):
        print(f"{name:<24}{r['n_races_scored']:>6}"
              f"{r['top1_pct']:>8.1f}%{r['top2_pct']:>8.1f}%{r['top3_pct']:>8.1f}%"
              f"{r['top4_pct']:>8.1f}%{r['top5_pct']:>8.1f}%")

    print("\n By field size, top-4 only:")
    print(f"{'baseline':<24}{'≤6':>12}{'7-8':>12}{'9-10':>12}{'11+':>12}")
    for name, r in sorted(results.items(), key=lambda kv: -kv[1]['top4_pct']):
        cells = []
        for b in ['≤6', '7-8', '9-10', '11+']:
            if b in r['by_field']:
                v = r['by_field'][b]
                cells.append(f"{v['top4_pct']:>7.1f}% n={v['n_races']:>3}")
            else:
                cells.append('—')
        print(f"{name:<24}" + ''.join(f'{c:>12}' for c in cells))

    # Save
    ts = datetime.utcnow().strftime('%Y%m%d_%H%M')
    out = {
        'gate': 'gate_3c',
        'section': 'human_parity_probe',
        'eval_window': [START, END],
        'baselines': results,
    }
    Path(f'/home/strakajagr/EE_GATE3C_PARITY_{ts}.json').write_text(json.dumps(out, indent=2, default=str))
    print(f"\nSaved: /home/strakajagr/EE_GATE3C_PARITY_{ts}.json")


if __name__ == '__main__':
    main()
