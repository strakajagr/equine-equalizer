"""
4B Survival analysis for ordinal finish_position.

Evaluates lifelines CoxPH model on finish_position (treated as time-to-event
with event=race-end) vs is_winner XGBoost baseline. Output: ordinal model
contribution to exotic-bet (exacta/trifecta) hit-rate signal.

Substrate-pragmatic minimum-viable: CoxPH on (finish_position, win_probability)
covariates; report concordance index vs is_winner AUC. Tier 2 EXECUTION re-runs.
"""

import argparse
import json

import boto3
import numpy as np
import pandas as pd
import psycopg2
from lifelines import CoxPHFitter
from sklearn.metrics import roc_auc_score


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
               hp.hybrid_c_win_probability AS hybrid_c_p,
               res.finish_position,
               r.field_size
        FROM hybrid_c_predictions hp
        JOIN races r ON r.race_id = hp.race_id
        JOIN entries e ON e.race_id = hp.race_id AND e.horse_id::text = hp.horse_id
        LEFT JOIN results res ON res.race_id = hp.race_id AND res.horse_id = e.horse_id
        WHERE hp.ensemble_version = 'option_c_hybrid_ensemble_20260515'
          AND r.race_date BETWEEN %s AND %s
          AND res.finish_position IS NOT NULL
    """, conn, params=[window_start, window_end])
    conn.close()
    return df


def evaluate(window_start, window_end, output_path):
    df = load_substrate(window_start, window_end)
    print(f"Loaded {len(df)} rows / {df['race_id'].nunique()} races")
    if len(df) < 100:
        result = {'verdict': 'substrate-thin', 'n_observations': len(df)}
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        return result

    # CoxPH expects (duration, event_observed) — substrate-pragmatic:
    #   duration = finish_position (1..field_size; lower = better)
    #   event = always 1 (race ended for all entries)
    df = df.copy()
    df['duration'] = df['finish_position'].astype(float)
    df['event'] = 1
    df['is_winner'] = (df['finish_position'] == 1).astype(int)

    # 80/20 race-level split
    np.random.seed(42)
    races = sorted(df['race_id'].unique())
    np.random.shuffle(races)
    split = int(len(races) * 0.8)
    train = df[df['race_id'].isin(set(races[:split]))]
    test = df[~df['race_id'].isin(set(races[:split]))]

    # Baseline: AUC of hybrid_c_p on is_winner
    try:
        baseline_auc = float(roc_auc_score(test['is_winner'], test['hybrid_c_p']))
    except Exception:
        baseline_auc = None

    # Fit CoxPH with hybrid_c_p as covariate
    cph_train = train[['duration', 'event', 'hybrid_c_p', 'field_size']].dropna()
    cph = CoxPHFitter()
    try:
        cph.fit(cph_train, duration_col='duration', event_col='event')
        concordance = float(cph.concordance_index_)
    except Exception as e:
        result = {'verdict': 'substrate-investigation-required', 'error': str(e)}
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        return result

    # Test concordance: predict partial hazards on test; higher hazard → earlier finish
    test_cph = test[['duration', 'event', 'hybrid_c_p', 'field_size']].dropna()
    hazards = cph.predict_partial_hazard(test_cph[['hybrid_c_p', 'field_size']])
    # Higher hazard → predicted earlier finish (lower finish_position → winner)
    # Invert sign to align with is_winner direction for AUC
    try:
        survival_auc = float(roc_auc_score(test['is_winner'].iloc[:len(hazards)], hazards.values))
    except Exception:
        survival_auc = None

    delta_auc = (survival_auc - baseline_auc) if (survival_auc is not None and baseline_auc is not None) else None

    if delta_auc is not None and delta_auc > 0.01:
        verdict = 'substrate-validated production candidate'
    elif delta_auc is not None and abs(delta_auc) < 0.005:
        verdict = 'null (no improvement over baseline)'
    else:
        verdict = 'substrate-investigation-required'

    result = {
        'verdict': verdict,
        'baseline_auc': baseline_auc,
        'survival_auc': survival_auc,
        'concordance_train': concordance,
        'delta_auc': delta_auc,
        'n_train': len(train), 'n_test': len(test),
    }
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Verdict: {verdict}; baseline_auc={baseline_auc} survival_auc={survival_auc}")
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
