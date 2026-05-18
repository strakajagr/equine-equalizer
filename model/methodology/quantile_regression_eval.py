"""
4A Quantile regression for probability calibration.

Evaluates whether statsmodels QuantReg on Hybrid C output improves calibration
(Brier score reduction) + EV-bet accuracy vs raw Hybrid C output.

Substrate-pragmatic minimum-viable: fit QuantReg(0.5 / 0.75 / 0.9 quantiles)
on Hybrid C win_probability → is_winner; compare Brier on held-out subset.
Tier 2 EXECUTION re-runs at production scope.
"""

import argparse
import json
from pathlib import Path

import boto3
import numpy as np
import pandas as pd
import psycopg2
import statsmodels.api as sm
from statsmodels.regression.quantile_regression import QuantReg
from sklearn.metrics import brier_score_loss, roc_auc_score


DB_SECRET_ARN = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'


def get_db_conn():
    sm_client = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm_client.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString'])
    return psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'], password=secret['password'],
    )


def load_hybrid_c_substrate(window_start, window_end):
    """Pull Hybrid C predictions + actuals for the forensic window."""
    conn = get_db_conn()
    df = pd.read_sql("""
        SELECT hp.race_id::text AS race_id,
               hp.horse_id::text AS horse_id,
               hp.hybrid_c_win_probability AS win_probability,
               (res.finish_position = 1)::int AS is_winner
        FROM hybrid_c_predictions hp
        JOIN races r ON r.race_id = hp.race_id
        JOIN entries e ON e.race_id = hp.race_id AND e.horse_id::text = hp.horse_id
        LEFT JOIN results res ON res.race_id = hp.race_id AND res.horse_id = e.horse_id
        WHERE hp.ensemble_version = 'option_c_hybrid_ensemble_20260515'
          AND r.race_date BETWEEN %s AND %s
    """, conn, params=[window_start, window_end])
    conn.close()
    return df.dropna(subset=['is_winner'])


def evaluate(window_start, window_end, output_path):
    df = load_hybrid_c_substrate(window_start, window_end)
    print(f"Loaded {len(df)} rows / {df['race_id'].nunique()} races")
    if len(df) < 100:
        verdict = 'substrate-thin'
        result = {'verdict': verdict, 'n_observations': len(df)}
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        return result

    # Random 80/20 split by race
    np.random.seed(42)
    races = sorted(df['race_id'].unique())
    np.random.shuffle(races)
    split = int(len(races) * 0.8)
    train_races = set(races[:split])
    train = df[df['race_id'].isin(train_races)]
    test = df[~df['race_id'].isin(train_races)]

    # Baseline: raw Hybrid C output
    baseline_brier = float(brier_score_loss(test['is_winner'], test['win_probability'].clip(0, 1)))
    baseline_auc = float(roc_auc_score(test['is_winner'], test['win_probability']))

    X_train = sm.add_constant(train['win_probability'].values)
    y_train = train['is_winner'].values.astype(float)

    # Fit QuantReg at 0.5, 0.75, 0.9
    calibrated_briers = {}
    for q in [0.5, 0.75, 0.9]:
        model = QuantReg(y_train, X_train).fit(q=q)
        X_test = sm.add_constant(test['win_probability'].values)
        preds = model.predict(X_test).clip(0, 1)
        calibrated_briers[f'q{q}'] = float(brier_score_loss(test['is_winner'], preds))

    print(f"Baseline Brier: {baseline_brier:.4f}; AUC: {baseline_auc:.4f}")
    for q, brier in calibrated_briers.items():
        delta = baseline_brier - brier
        print(f"  QuantReg {q}: Brier={brier:.4f}  Δ={delta:+.4f}")

    best_q = min(calibrated_briers, key=calibrated_briers.get)
    best_brier_delta = baseline_brier - calibrated_briers[best_q]

    if best_brier_delta > 0.003:
        verdict = 'substrate-validated production candidate'
    elif abs(best_brier_delta) < 0.001:
        verdict = 'null (no calibration improvement)'
    else:
        verdict = 'substrate-investigation-required'

    result = {
        'verdict': verdict,
        'baseline_brier': baseline_brier,
        'baseline_auc': baseline_auc,
        'calibrated_briers': calibrated_briers,
        'best_quantile': best_q,
        'best_brier_delta': best_brier_delta,
        'n_train': len(train), 'n_test': len(test),
    }
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Verdict: {verdict}")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--window-start', default='2026-05-02')
    parser.add_argument('--window-end', default='2026-05-17')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    evaluate(args.window_start, args.window_end, args.output)


if __name__ == '__main__':
    main()
