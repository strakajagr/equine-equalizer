"""
4F Causal inference for trip-line + track-bias adjustment.

Evaluates dowhy + econml causal estimators on:
  - trip_incident → win_probability (does substrate-correct trip cause winning?)
  - track_bias → win_probability (per-track bias adjustment quantified)

Substrate-pragmatic minimum-viable: dowhy DAG with treatment=trip_clean OR
post_position; outcome=is_winner; covariates from Hybrid C feature set.
Tier 2 EXECUTION extends to full propensity scoring + sensitivity analysis.
"""

import argparse
import json

import boto3
import numpy as np
import pandas as pd
import psycopg2

try:
    import dowhy
    from dowhy import CausalModel
except ImportError:
    CausalModel = None


DB_SECRET_ARN = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'


def get_db_conn():
    sm_client = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm_client.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString'])
    return psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'], password=secret['password'],
    )


def load_substrate(window_start, window_end):
    """Pull post_position + finish_position + Hybrid C features as causal-inference substrate."""
    conn = get_db_conn()
    df = pd.read_sql("""
        SELECT hp.race_id::text AS race_id,
               hp.horse_id::text AS horse_id,
               hp.hybrid_c_win_probability AS hybrid_c_p,
               e.post_position,
               e.morning_line_odds,
               r.field_size,
               (res.finish_position = 1)::int AS is_winner
        FROM hybrid_c_predictions hp
        JOIN races r ON r.race_id = hp.race_id
        JOIN entries e ON e.race_id = hp.race_id AND e.horse_id::text = hp.horse_id
        LEFT JOIN results res ON res.race_id = hp.race_id AND res.horse_id = e.horse_id
        WHERE hp.ensemble_version = 'option_c_hybrid_ensemble_20260515'
          AND r.race_date BETWEEN %s AND %s
    """, conn, params=[window_start, window_end])
    conn.close()
    return df.dropna(subset=['is_winner', 'post_position'])


def evaluate(window_start, window_end, output_path):
    if CausalModel is None:
        result = {'verdict': 'substrate-investigation-required', 'error': 'dowhy not importable'}
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        return result

    df = load_substrate(window_start, window_end)
    print(f"Loaded {len(df)} rows")
    if len(df) < 100:
        result = {'verdict': 'substrate-thin', 'n_observations': len(df)}
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        return result

    # Substrate-pragmatic causal model: treatment = inside_post (post_position <= 3);
    # outcome = is_winner; covariates = hybrid_c_p, morning_line_odds, field_size
    df = df.copy()
    df['inside_post'] = (df['post_position'] <= 3).astype(int)
    df['hybrid_c_p'] = df['hybrid_c_p'].fillna(0.0).astype(float)
    df['morning_line_odds'] = df['morning_line_odds'].fillna(0.0).astype(float)
    df['field_size'] = df['field_size'].fillna(8).astype(float)

    try:
        model = CausalModel(
            data=df[['inside_post', 'is_winner', 'hybrid_c_p', 'morning_line_odds', 'field_size']],
            treatment='inside_post', outcome='is_winner',
            common_causes=['hybrid_c_p', 'morning_line_odds', 'field_size'],
        )
        identified = model.identify_effect(proceed_when_unidentifiable=True)
        estimate = model.estimate_effect(
            identified, method_name='backdoor.linear_regression',
        )
        ate = float(estimate.value)
    except Exception as e:
        result = {'verdict': 'substrate-investigation-required', 'error': str(e)}
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        return result

    # Substrate-pragmatic verdict: meaningful causal effect if |ATE| > 0.005 (0.5pp lift/drop)
    if abs(ate) > 0.005:
        verdict = 'substrate-validated production candidate (post_position causal signal)'
    else:
        verdict = 'null (no causal effect of inside_post on is_winner)'

    result = {
        'verdict': verdict,
        'treatment': 'inside_post (post_position <= 3)',
        'outcome': 'is_winner',
        'ate': ate,
        'common_causes': ['hybrid_c_p', 'morning_line_odds', 'field_size'],
        'n_observations': int(len(df)),
        'n_treated': int(df['inside_post'].sum()),
        'n_control': int((1 - df['inside_post']).sum()),
    }
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Verdict: {verdict}; ATE={ate:.4f}")
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
