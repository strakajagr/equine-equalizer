"""
4I Calibration methods post-XGBoost.

Three substrate-pragmatic variants on Hybrid C output:
  - Isotonic regression (sklearn.isotonic.IsotonicRegression)
  - Platt scaling (sklearn LogisticRegression on probabilities)
  - Conformal prediction (substrate-pragmatic split-conformal; sklearn-only)

Compares Brier + ECE (Expected Calibration Error) vs raw Hybrid C output.
"""

import argparse
import json

import boto3
import numpy as np
import pandas as pd
import psycopg2
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score


DB_SECRET_ARN = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'


def get_db_conn():
    sm_client = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm_client.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString'])
    return psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'], password=secret['password'],
    )


def load_substrate(window_start, window_end):
    conn = get_db_conn()
    df = pd.read_sql("""
        SELECT hp.race_id::text AS race_id,
               hp.horse_id::text AS horse_id,
               hp.hybrid_c_win_probability AS p,
               (res.finish_position = 1)::int AS is_winner
        FROM hybrid_c_predictions hp
        JOIN races r ON r.race_id = hp.race_id
        JOIN entries e ON e.race_id = hp.race_id AND e.horse_id::text = hp.horse_id
        LEFT JOIN results res ON res.race_id = hp.race_id AND res.horse_id = e.horse_id
        WHERE hp.ensemble_version = 'option_c_hybrid_ensemble_20260515'
          AND r.race_date BETWEEN %s AND %s
    """, conn, params=[window_start, window_end])
    conn.close()
    return df.dropna(subset=['is_winner', 'p'])


def expected_calibration_error(y_true, y_pred, n_bins=10):
    bins = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    n = len(y_true)
    for i in range(n_bins):
        mask = (y_pred >= bins[i]) & (y_pred < bins[i + 1])
        if mask.sum() == 0:
            continue
        avg_pred = y_pred[mask].mean()
        avg_actual = y_true[mask].mean()
        ece += (mask.sum() / n) * abs(avg_pred - avg_actual)
    return float(ece)


def conformal_predict(p_train, y_train, p_test, alpha=0.1):
    """Substrate-pragmatic split-conformal: compute residuals + apply quantile."""
    residuals = np.abs(y_train - p_train)
    q = np.quantile(residuals, 1 - alpha)
    # Substrate-pragmatic: return p_test with conformal bounds half-width q
    return p_test.clip(0, 1), q


def evaluate(window_start, window_end, output_path):
    df = load_substrate(window_start, window_end)
    print(f"Loaded {len(df)} rows")
    if len(df) < 100:
        result = {'verdict': 'substrate-thin', 'n_observations': len(df)}
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        return result

    np.random.seed(42)
    races = sorted(df['race_id'].unique())
    np.random.shuffle(races)
    split = int(len(races) * 0.8)
    train = df[df['race_id'].isin(set(races[:split]))]
    test = df[~df['race_id'].isin(set(races[:split]))]

    p_train = train['p'].values.astype(float)
    y_train = train['is_winner'].values.astype(int)
    p_test = test['p'].values.astype(float)
    y_test = test['is_winner'].values.astype(int)

    baseline_brier = float(brier_score_loss(y_test, p_test.clip(0, 1)))
    baseline_ece = expected_calibration_error(y_test, p_test)

    # Isotonic regression
    iso = IsotonicRegression(out_of_bounds='clip')
    iso.fit(p_train, y_train)
    p_test_iso = iso.predict(p_test).clip(0, 1)
    iso_brier = float(brier_score_loss(y_test, p_test_iso))
    iso_ece = expected_calibration_error(y_test, p_test_iso)

    # Platt scaling
    lr = LogisticRegression()
    lr.fit(p_train.reshape(-1, 1), y_train)
    p_test_platt = lr.predict_proba(p_test.reshape(-1, 1))[:, 1].clip(0, 1)
    platt_brier = float(brier_score_loss(y_test, p_test_platt))
    platt_ece = expected_calibration_error(y_test, p_test_platt)

    # Conformal
    p_test_conformal, conformal_q = conformal_predict(p_train, y_train, p_test)
    conformal_brier = float(brier_score_loss(y_test, p_test_conformal))

    best_method = min(
        [('isotonic', iso_brier), ('platt', platt_brier), ('conformal', conformal_brier)],
        key=lambda x: x[1],
    )
    best_brier_delta = baseline_brier - best_method[1]

    if best_brier_delta > 0.003:
        verdict = f'substrate-validated production candidate ({best_method[0]})'
    elif abs(best_brier_delta) < 0.001:
        verdict = 'null (no calibration improvement)'
    else:
        verdict = 'substrate-investigation-required'

    result = {
        'verdict': verdict,
        'baseline_brier': baseline_brier,
        'baseline_ece': baseline_ece,
        'isotonic_brier': iso_brier,
        'isotonic_ece': iso_ece,
        'platt_brier': platt_brier,
        'platt_ece': platt_ece,
        'conformal_brier': conformal_brier,
        'conformal_q': float(conformal_q),
        'best_method': best_method[0],
        'best_brier_delta': best_brier_delta,
        'n_train': len(train), 'n_test': len(test),
    }
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Verdict: {verdict}; baseline={baseline_brier:.4f} best={best_method[1]:.4f}")
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
