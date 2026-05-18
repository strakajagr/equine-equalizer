"""
Tier 2 EXECUTION comprehensive forensic measurement per § 4.34 + § 4.36.

Per-ensemble adjudication-grade metrics:
  - AUC (forensic OOS)
  - Calibration (predicted prob vs realized win rate per bucket; expected calibration error)
  - Top-1 / top-3 hit rate
  - Standalone ROI (flat-win bet on top-1)
  - Per-context decomposition (track / DOW / field_size_bucket / race_type / claim_price_tier)
  - § 4.36 dual-criterion: Δ AUC AND Δ ROI vs Hybrid C baseline
  - § 4.36 extension candidate: AUC↓+ROI↑ inverse-pattern detection
"""

import argparse
import json

import boto3
import numpy as np
import pandas as pd
import psycopg2
from sklearn.metrics import roc_auc_score


DB_SECRET_ARN = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'
BEL_STRATIFICATION_PENDING_H3 = ['BEL']


def get_db_conn():
    sm = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString'])
    return psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'], password=secret['password'],
    )


def load_predictions_and_actuals(ensemble_version, window_start, window_end):
    conn = get_db_conn()
    df = pd.read_sql("""
        SELECT
            hcp.race_id, hcp.horse_id,
            hcp.hybrid_c_win_probability AS win_probability,
            r.race_date, t.track_code,
            COALESCE(r.distance_furlongs, 0.0)::float AS distance_furlongs,
            COALESCE(r.field_size, 0) AS field_size,
            COALESCE(r.claiming_price, 0) AS claim_price,
            COALESCE(r.race_type, 'unknown') AS race_type,
            EXTRACT(DOW FROM r.race_date)::int AS day_of_week,
            res.finish_position,
            (res.finish_position = 1)::int AS is_winner,
            COALESCE(res.win_payout, 0.0) AS win_payout
        FROM hybrid_c_predictions hcp
        JOIN races r ON r.race_id = hcp.race_id
        JOIN tracks t USING (track_id)
        JOIN entries e ON e.race_id = r.race_id AND e.horse_id::text = hcp.horse_id
        LEFT JOIN results res ON res.race_id = r.race_id AND res.horse_id = e.horse_id
        WHERE hcp.ensemble_version = %s
          AND r.race_date BETWEEN %s AND %s
    """, conn, params=[ensemble_version, window_start, window_end])
    conn.close()
    return df


def safe_auc(df):
    v = df.dropna(subset=['win_probability', 'is_winner'])
    if len(v) < 30:
        return None
    try:
        return float(roc_auc_score(v['is_winner'], v['win_probability']))
    except Exception:
        return None


def compute_ece(df, n_buckets=10):
    v = df.dropna(subset=['win_probability', 'is_winner'])
    if len(v) < 30:
        return None
    bins = np.linspace(0, 1, n_buckets + 1)
    ece = 0.0
    n = len(v)
    for i in range(n_buckets):
        mask = (v['win_probability'] >= bins[i]) & (v['win_probability'] < bins[i + 1])
        if mask.sum() == 0:
            continue
        pred_mean = v.loc[mask, 'win_probability'].mean()
        actual_mean = v.loc[mask, 'is_winner'].mean()
        ece += (mask.sum() / n) * abs(pred_mean - actual_mean)
    return float(ece)


def topn_hit_rate(df, n):
    if df.empty:
        return None
    hits = df.groupby('race_id').apply(
        lambda g: int(g.nlargest(n, 'win_probability')['is_winner'].sum() > 0)
    )
    return float(hits.mean()) if len(hits) > 0 else None


def standalone_roi(df):
    if df.empty:
        return None
    top1 = df.sort_values('win_probability', ascending=False).groupby('race_id').head(1)
    n = len(top1)
    if n == 0:
        return None
    return float((top1['win_payout'].sum() - 2.0 * n) / (2.0 * n) * 100)


def per_context_metrics(df, context_col):
    result = {}
    if context_col == 'field_size_bucket':
        df = df.copy()
        df['field_size_bucket'] = pd.cut(df['field_size'], bins=[-1, 6, 9, 12, 99],
                                          labels=['small', 'med', 'large', 'xlarge']).astype(str)
    elif context_col == 'claim_price_tier':
        df = df.copy()
        df['claim_price_tier'] = pd.cut(df['claim_price'], bins=[-1, 0.001, 25000, 99999999],
                                         labels=['non_claim', 'low_claim', 'high_claim']).astype(str)
    for ctx_val, sub in df.groupby(context_col):
        n_races = sub['race_id'].nunique()
        n_obs = len(sub.dropna(subset=['win_probability', 'is_winner']))
        if n_obs < 30:
            result[str(ctx_val)] = {'n_obs': n_obs, 'n_races': int(n_races), 'note': 'substrate-thin'}
            continue
        result[str(ctx_val)] = {
            'n_obs': int(n_obs), 'n_races': int(n_races),
            'auc': safe_auc(sub), 'roi_pct': standalone_roi(sub),
            'top1_hit': topn_hit_rate(sub, 1),
        }
    return result


def comprehensive_forensic(ensemble_version, baseline_version, window_start, window_end):
    cand_df = load_predictions_and_actuals(ensemble_version, window_start, window_end)
    base_df = load_predictions_and_actuals(baseline_version, window_start, window_end)

    print(f"\n{'='*70}")
    print(f"Ensemble: {ensemble_version}")
    print(f"  candidate: {len(cand_df)} rows / {cand_df['race_id'].nunique()} races")
    print(f"  baseline:  {len(base_df)} rows / {base_df['race_id'].nunique()} races")

    cand_adj = cand_df[~cand_df['track_code'].isin(BEL_STRATIFICATION_PENDING_H3)]
    base_adj = base_df[~base_df['track_code'].isin(BEL_STRATIFICATION_PENDING_H3)]
    cand_bel = cand_df[cand_df['track_code'].isin(BEL_STRATIFICATION_PENDING_H3)]

    cand_auc = safe_auc(cand_adj); base_auc = safe_auc(base_adj)
    cand_roi = standalone_roi(cand_adj); base_roi = standalone_roi(base_adj)
    cand_top1 = topn_hit_rate(cand_adj, 1); base_top1 = topn_hit_rate(base_adj, 1)
    cand_top3 = topn_hit_rate(cand_adj, 3); base_top3 = topn_hit_rate(base_adj, 3)
    cand_ece = compute_ece(cand_adj); base_ece = compute_ece(base_adj)

    delta_auc = (cand_auc - base_auc) if (cand_auc is not None and base_auc is not None) else None
    delta_roi = (cand_roi - base_roi) if (cand_roi is not None and base_roi is not None) else None
    DELTA_AUC_THRESHOLD = 0.017
    dual_pass = (delta_auc is not None and delta_auc >= DELTA_AUC_THRESHOLD
                 and delta_roi is not None and delta_roi >= 0)
    inverse_pattern = (delta_auc is not None and delta_auc < 0
                       and delta_roi is not None and delta_roi > 5.0)

    per_ctx = {}
    for ctx in ['track_code', 'day_of_week', 'field_size_bucket', 'race_type', 'claim_price_tier']:
        per_ctx[ctx] = per_context_metrics(cand_adj, ctx)

    result = {
        'ensemble_version': ensemble_version,
        'baseline_version': baseline_version,
        'window': [window_start, window_end],
        'adjudication_grade_non_bel': {
            'n_obs': int(len(cand_adj.dropna(subset=['win_probability', 'is_winner']))),
            'n_races': int(cand_adj['race_id'].nunique()),
            'auc': cand_auc, 'roi_pct': cand_roi,
            'top1_hit': cand_top1, 'top3_hit': cand_top3,
            'calibration_ece': cand_ece,
        },
        'baseline_metrics': {
            'auc': base_auc, 'roi_pct': base_roi,
            'top1_hit': base_top1, 'top3_hit': base_top3,
            'calibration_ece': base_ece,
        },
        'bel_informational_only': {
            'n_obs': int(len(cand_bel.dropna(subset=['win_probability', 'is_winner']))),
            'auc': safe_auc(cand_bel), 'roi_pct': standalone_roi(cand_bel),
        },
        'dual_criterion_delta': {
            'delta_auc': delta_auc, 'delta_roi_pp': delta_roi,
            'auc_threshold': DELTA_AUC_THRESHOLD,
            'dual_criterion_pass': dual_pass,
        },
        'inverse_pattern_36_extension_candidate': {
            'detected': inverse_pattern,
            'note': 'AUC↓+ROI↑ pattern; § 4.36 codification extension candidate',
        },
        'per_context_decomposition': per_ctx,
    }

    print(f"  Adj AUC: {cand_auc} (base {base_auc}; Δ {delta_auc})")
    print(f"  Adj ROI: {cand_roi}% (base {base_roi}%; Δ {delta_roi}pp)")
    print(f"  ECE: {cand_ece} (base {base_ece})")
    print(f"  dual_criterion_pass: {dual_pass}; inverse_pattern: {inverse_pattern}")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ensemble-versions', nargs='+', required=True)
    parser.add_argument('--baseline-version', default='option_c_hybrid_ensemble_20260515')
    parser.add_argument('--window-start', default='2026-05-02')
    parser.add_argument('--window-end', default='2026-05-10')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    results = {}
    for v in args.ensemble_versions:
        results[v] = comprehensive_forensic(v, args.baseline_version, args.window_start, args.window_end)
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nComprehensive forensic complete: {args.output}")


if __name__ == '__main__':
    main()
