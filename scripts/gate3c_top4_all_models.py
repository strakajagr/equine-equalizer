"""Gate 3C §1+§2 — top-K containment for ALL evaluable models + market,
   leak-free OOS, stratified by field size.

Models scored:
  - hybrid_c        (hybrid_c_predictions.hybrid_c_win_probability — broad: 377 races)
  - wr_general      (wr_predictions.win_probability — 214 races)
  - wr_rank_score   (wr_predictions.rank_score — = ls.xgb_rank_score per Gate 2)
  - wr_ensemble     (wr_predictions.ensemble_win_prob — = ls.final_win_probability)
  - pl_general      (pl_predictions.win_probability)
  - ls_general      (ls_predictions.final_win_probability)
  - lstm_trajectory (ls_predictions.lstm_trajectory)
  - rf_longshot     (ls_predictions.rf_longshot_prob)
  - gate3_v2        (Gate 3 leak-free model from /tmp/gate3_predictions.csv)
  - MARKET          (1/(closing_odds+1), fallback ml_odds)

§2 — lean58 specialists. Their per-horse predictions are NOT stored. Run
re-inference offline (separate step). This script handles the stored set.
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


def load_all_data(start, end):
    """Pull per-(race, horse) preds from all DB-stored sources + winners + market."""
    # Winners + odds
    logger.info("Loading winners + ml_odds")
    win_sql = f"""
        SELECT r.race_id::text AS race_id, r.race_date,
               t.track_code, r.race_number,
               res.horse_id::text AS winner_horse_id,
               e.morning_line_odds::float AS winner_ml_odds
        FROM results res
        JOIN races r USING(race_id)
        JOIN tracks t ON t.track_id = r.track_id
        LEFT JOIN entries e ON e.race_id = r.race_id AND e.horse_id = res.horse_id
        WHERE res.finish_position = 1
          AND r.race_date BETWEEN '{start}' AND '{end}'
    """
    winners = pd.DataFrame(lambda_query(win_sql))
    winners = winners.drop_duplicates(subset=['track_code', 'race_date', 'race_number'])
    winners['race_date'] = pd.to_datetime(winners['race_date'])
    winners['race_number'] = winners['race_number'].astype(int)

    # WR predictions (win_probability, rank_score, ensemble_win_prob)
    logger.info("Loading wr_predictions (general)")
    wr_sql = f"""
        SELECT wp.race_id::text AS race_id, wp.horse_id::text AS horse_id,
               wp.win_probability::float AS wr_win_prob,
               wp.rank_score::float AS wr_rank_score,
               wp.ensemble_win_prob::float AS wr_ensemble,
               wp.raw_win_prob::float AS wr_raw_win_prob,
               t.track_code, r.race_date, r.race_number
        FROM wr_predictions wp
        JOIN races r ON r.race_id = wp.race_id
        JOIN tracks t ON t.track_id = r.track_id
        WHERE r.race_date BETWEEN '{start}' AND '{end}' AND wp.style = 'general'
    """
    wr = pd.DataFrame(lambda_query(wr_sql))
    wr['race_date'] = pd.to_datetime(wr['race_date'])
    wr['race_number'] = wr['race_number'].astype(int)

    # PL predictions
    logger.info("Loading pl_predictions (general)")
    pl_sql = f"""
        SELECT pp.race_id::text AS race_id, pp.horse_id::text AS horse_id,
               pp.win_probability::float AS pl_win_prob
        FROM pl_predictions pp
        JOIN races r ON r.race_id = pp.race_id
        WHERE r.race_date BETWEEN '{start}' AND '{end}' AND pp.style = 'general'
    """
    pl = pd.DataFrame(lambda_query(pl_sql))

    # LS predictions
    logger.info("Loading ls_predictions (general)")
    ls_sql = f"""
        SELECT lp.race_id::text AS race_id, lp.horse_id::text AS horse_id,
               lp.final_win_probability::float AS ls_final_win_prob,
               lp.lstm_trajectory::float AS lstm_trajectory,
               lp.rf_longshot_prob::float AS rf_longshot_prob,
               lp.xgb_rank_score::float AS ls_xgb_rank
        FROM ls_predictions lp
        JOIN races r ON r.race_id = lp.race_id
        WHERE r.race_date BETWEEN '{start}' AND '{end}' AND lp.style = 'general'
    """
    ls = pd.DataFrame(lambda_query(ls_sql))

    # Hybrid C predictions
    logger.info("Loading hybrid_c_predictions")
    hyb_sql = f"""
        SELECT hp.race_id::text AS race_id, hp.horse_id::text AS horse_id,
               hp.hybrid_c_win_probability::float AS hybrid_c_win_prob
        FROM hybrid_c_predictions hp
        JOIN races r ON r.race_id = hp.race_id
        WHERE r.race_date BETWEEN '{start}' AND '{end}'
    """
    hyb = pd.DataFrame(lambda_query(hyb_sql))

    # Market: closing_odds + ml_odds + race_id mapping
    logger.info("Loading market (closing_odds, ml_odds)")
    mkt_sql = f"""
        SELECT e.race_id::text AS race_id, e.horse_id::text AS horse_id,
               e.morning_line_odds::float AS ml_odds,
               pp.closing_odds::float AS closing_odds,
               t.track_code, r.race_date, r.race_number
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
    mkt = pd.DataFrame(lambda_query(mkt_sql))
    mkt['race_date'] = pd.to_datetime(mkt['race_date'])
    mkt['race_number'] = mkt['race_number'].astype(int)
    # Market prob: closing_odds-derived if available, else ML-odds-derived
    mkt['mkt_odds_for_rank'] = mkt['closing_odds'].where(
        mkt['closing_odds'].notna() & (mkt['closing_odds'] > 0), mkt['ml_odds']
    )

    return {
        'winners': winners,
        'wr': wr, 'pl': pl, 'ls': ls, 'hybrid_c': hyb,
        'market': mkt,
    }


def field_size_bucket(n):
    if n <= 6: return '≤6'
    if n <= 8: return '7-8'
    if n <= 10: return '9-10'
    return '11+'


def score_model_containment(per_horse_df, score_col, winners_idx, mkt_field_size,
                            ascending=False, max_k=5):
    """For each race in per_horse_df: rank horses by score_col, check if top-K
    contains the actual winner. Returns dict of metrics."""
    if score_col not in per_horse_df.columns:
        return None
    df = per_horse_df.dropna(subset=[score_col]).copy()
    if len(df) == 0:
        return None
    by_field = defaultdict(lambda: defaultdict(int))
    n_races = 0
    overall = defaultdict(int)

    for race_id, grp in df.groupby('race_id'):
        winner = winners_idx.get(str(race_id))
        if winner is None:
            continue
        winner = str(winner)
        # Field size from the market data (entries count)
        fs = mkt_field_size.get(str(race_id))
        if fs is None:
            fs = len(grp)  # fallback
        bucket = field_size_bucket(fs)

        # Sort
        sorted_grp = grp.sort_values(score_col, ascending=ascending)
        ranked = list(sorted_grp['horse_id'].astype(str))

        n_races += 1
        by_field[bucket]['n_races'] += 1
        for k in range(1, max_k+1):
            hit = int(winner in ranked[:k])
            overall[f'top{k}_hits'] += hit
            by_field[bucket][f'top{k}_hits'] += hit

    if n_races == 0:
        return None
    result = {
        'n_races_scored': n_races,
    }
    for k in range(1, max_k+1):
        result[f'top{k}_pct'] = 100.0 * overall[f'top{k}_hits'] / n_races
    result['by_field'] = {}
    for b in ['≤6', '7-8', '9-10', '11+']:
        if b in by_field:
            nb = by_field[b]['n_races']
            result['by_field'][b] = {'n_races': nb}
            for k in range(1, max_k+1):
                result['by_field'][b][f'top{k}_pct'] = 100.0 * by_field[b][f'top{k}_hits'] / nb
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--start', default='2026-05-02')
    p.add_argument('--end', default='2026-05-17')
    p.add_argument('--v2-preds', default='/tmp/gate3_predictions.csv')
    p.add_argument('--out', default='/home/strakajagr/EE_GATE3C_ALL_MODELS')
    args = p.parse_args()

    data = load_all_data(args.start, args.end)
    winners = data['winners']
    mkt = data['market']

    # Build winner map: race_id (UUID) -> winner_horse_id
    win_map = winners.set_index('race_id')['winner_horse_id'].to_dict()
    # And by (tc, rd, rn) tuple for Gate 3 V2 predictions which use that key
    win_map_tuple = {}
    for _, w in winners.iterrows():
        win_map_tuple[(w['track_code'], pd.Timestamp(w['race_date']), int(w['race_number']))] = \
            w['winner_horse_id']

    # Field size from market entries count
    fs_by_race_id = mkt.groupby('race_id').size().to_dict()
    fs_by_tuple = mkt.groupby(['track_code', 'race_date', 'race_number']).size().to_dict()
    fs_by_tuple = {(tc, pd.Timestamp(rd), int(rn)): v for (tc, rd, rn), v in fs_by_tuple.items()}

    # Models keyed by race_id (UUID): hybrid_c, wr_*, pl, ls_*, market
    # First union all to one per-horse_per-race table
    per_horse = data['wr'].merge(
        data['pl'][['race_id', 'horse_id', 'pl_win_prob']],
        on=['race_id', 'horse_id'], how='outer',
    ).merge(
        data['ls'][['race_id', 'horse_id', 'ls_final_win_prob',
                    'lstm_trajectory', 'rf_longshot_prob', 'ls_xgb_rank']],
        on=['race_id', 'horse_id'], how='outer',
    ).merge(
        data['hybrid_c'][['race_id', 'horse_id', 'hybrid_c_win_prob']],
        on=['race_id', 'horse_id'], how='outer',
    ).merge(
        mkt[['race_id', 'horse_id', 'mkt_odds_for_rank']],
        on=['race_id', 'horse_id'], how='outer',
    )

    # Scoring loop
    results = {
        'gate': 'gate_3c',
        'eval_window': [args.start, args.end],
        'models': {},
    }

    model_specs = [
        ('hybrid_c',         'hybrid_c_win_prob', False),
        ('wr_win_prob',      'wr_win_prob',      False),
        ('wr_rank_score',    'wr_rank_score',    False),
        ('wr_ensemble',      'wr_ensemble',      False),
        ('wr_raw_win_prob',  'wr_raw_win_prob',  False),
        ('pl_win_prob',      'pl_win_prob',      False),
        ('ls_final_win_prob','ls_final_win_prob',False),
        ('ls_xgb_rank',      'ls_xgb_rank',      False),
        ('lstm_trajectory',  'lstm_trajectory',  False),
        ('rf_longshot_prob', 'rf_longshot_prob', False),
        ('MARKET_closing',   'mkt_odds_for_rank', True),  # ascending (lower odds = favorite)
    ]
    for name, col, asc in model_specs:
        r = score_model_containment(per_horse, col, win_map, fs_by_race_id,
                                    ascending=asc)
        if r is None:
            logger.info(f"[{name}] no scoring data — skipped")
            continue
        results['models'][name] = r
        logger.info(f"[{name:<22}] n={r['n_races_scored']}  top1={r['top1_pct']:.1f}%  "
                    f"top4={r['top4_pct']:.1f}%  top5={r['top5_pct']:.1f}%")

    # Gate 3 V2 (from CSV) — different key style (track/date/number tuple)
    try:
        v2 = pd.read_csv(args.v2_preds)
        v2['race_date'] = pd.to_datetime(v2['race_date'])
        v2_by_field = defaultdict(lambda: defaultdict(int))
        v2_overall = defaultdict(int)
        v2_n = 0
        for (tc, rd, rn), grp in v2.groupby(['track_code', 'race_date', 'race_number']):
            key = (tc, pd.Timestamp(rd), int(rn))
            winner = win_map_tuple.get(key)
            if winner is None:
                continue
            fs = fs_by_tuple.get(key, len(grp))
            bucket = field_size_bucket(fs)
            sorted_grp = grp.sort_values('pred_win_prob', ascending=False)
            ranked = list(sorted_grp['horse_id'].astype(str).values)
            v2_n += 1
            v2_by_field[bucket]['n_races'] += 1
            for k in range(1, 6):
                hit = int(str(winner) in ranked[:k])
                v2_overall[f'top{k}_hits'] += hit
                v2_by_field[bucket][f'top{k}_hits'] += hit

        v2_result = {'n_races_scored': v2_n}
        for k in range(1, 6):
            v2_result[f'top{k}_pct'] = 100.0 * v2_overall[f'top{k}_hits'] / v2_n if v2_n else 0
        v2_result['by_field'] = {}
        for b, stats in v2_by_field.items():
            nb = stats['n_races']
            v2_result['by_field'][b] = {'n_races': nb}
            for k in range(1, 6):
                v2_result['by_field'][b][f'top{k}_pct'] = 100.0 * stats[f'top{k}_hits'] / nb
        results['models']['gate3_v2_leakfree'] = v2_result
        logger.info(f"[gate3_v2_leakfree     ] n={v2_n}  top1={v2_result['top1_pct']:.1f}%  "
                    f"top4={v2_result['top4_pct']:.1f}%  top5={v2_result['top5_pct']:.1f}%")
    except Exception as e:
        logger.warning(f"V2 CSV scoring failed: {e}")

    # Print table
    print("\n" + "=" * 110)
    print("§1 — TOP-K CONTAINMENT, ALL EVALUABLE MODELS + MARKET (leak-free OOS)")
    print("=" * 110)
    print(f"{'model':<24}{'n':>6}{'top1':>9}{'top2':>9}{'top3':>9}{'top4':>9}{'top5':>9}")
    print("-" * 75)
    for name, r in sorted(results['models'].items(), key=lambda kv: -kv[1]['top4_pct']):
        print(f"{name:<24}{r['n_races_scored']:>6}"
              f"{r['top1_pct']:>8.1f}%{r['top2_pct']:>8.1f}%{r['top3_pct']:>8.1f}%"
              f"{r['top4_pct']:>8.1f}%{r['top5_pct']:>8.1f}%")

    print("\n" + "=" * 110)
    print("Top-4 by field size (showing top-4 % per bucket per model)")
    print("=" * 110)
    print(f"{'model':<24}{'≤6':>10}{'7-8':>10}{'9-10':>10}{'11+':>10}")
    for name, r in sorted(results['models'].items(), key=lambda kv: -kv[1]['top4_pct']):
        cells = []
        for b in ['≤6', '7-8', '9-10', '11+']:
            if b in r['by_field']:
                v = r['by_field'][b]
                cells.append(f"{v['top4_pct']:>6.1f}% n={v['n_races']:>3}")
            else:
                cells.append(f"{'—':>10}")
        print(f"{name:<24}" + ''.join(f'{c:>10}' for c in cells))

    # Save
    ts = datetime.utcnow().strftime('%Y%m%d_%H%M')
    Path(f'{args.out}_{ts}.json').write_text(json.dumps(results, indent=2, default=str))
    print(f"\nSaved: {args.out}_{ts}.json")


if __name__ == '__main__':
    main()
