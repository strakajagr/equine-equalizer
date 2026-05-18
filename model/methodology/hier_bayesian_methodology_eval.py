"""
4C Hierarchical Bayesian for trainer/jockey/sire random effects.

DISTINCT from 3F (3F was per-track random effects on Hybrid C L1 inputs).
4C models per-trainer + per-jockey random effects to quantify trainer/jockey
contribution to win probability vs flat baseline.

Substrate-pragmatic minimum-viable: pymc Bayesian linear model with
per-trainer + per-jockey random effects on is_winner. Tier 2 EXECUTION
re-runs at production MCMC scope.
"""

import argparse
import json

import boto3
import numpy as np
import pandas as pd
import psycopg2
import pymc as pm


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
               e.trainer_id::text AS trainer_id,
               e.jockey_id::text AS jockey_id,
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


def evaluate(window_start, window_end, output_path, draws=100, tune=100):
    df = load_substrate(window_start, window_end)
    print(f"Loaded {len(df)} rows; n_trainers={df['trainer_id'].nunique()} n_jockeys={df['jockey_id'].nunique()}")
    if len(df) < 100:
        result = {'verdict': 'substrate-thin', 'n_observations': len(df)}
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        return result

    trainers = sorted(df['trainer_id'].dropna().unique())
    jockeys = sorted(df['jockey_id'].dropna().unique())
    df = df.dropna(subset=['trainer_id', 'jockey_id'])
    trainer_idx = df['trainer_id'].map({t: i for i, t in enumerate(trainers)}).values
    jockey_idx = df['jockey_id'].map({j: i for i, j in enumerate(jockeys)}).values

    hybrid_c_p = df['hybrid_c_p'].fillna(0.0).values
    y = df['is_winner'].values.astype(int)

    with pm.Model() as model:
        alpha = pm.Normal('alpha', mu=-2.0, sigma=1.0)
        beta_hp = pm.Normal('beta_hp', mu=0.0, sigma=1.0)
        sigma_t = pm.HalfNormal('sigma_t', sigma=0.5)
        sigma_j = pm.HalfNormal('sigma_j', sigma=0.5)
        trainer_offset = pm.Normal('trainer_offset', mu=0.0, sigma=sigma_t, shape=len(trainers))
        jockey_offset = pm.Normal('jockey_offset', mu=0.0, sigma=sigma_j, shape=len(jockeys))
        logit = alpha + beta_hp * hybrid_c_p + trainer_offset[trainer_idx] + jockey_offset[jockey_idx]
        pm.Bernoulli('obs', logit_p=logit, observed=y)
        trace = pm.sample(draws=draws, tune=tune, chains=2, target_accept=0.9, progressbar=False)

    post = trace.posterior
    trainer_var = float(post['sigma_t'].mean(dim=['chain', 'draw']).values)
    jockey_var = float(post['sigma_j'].mean(dim=['chain', 'draw']).values)
    beta_hp_post = float(post['beta_hp'].mean(dim=['chain', 'draw']).values)

    # Substrate-pragmatic verdict: trainer/jockey contribute meaningfully if posterior sigma > 0.1
    if trainer_var > 0.1 or jockey_var > 0.1:
        verdict = 'substrate-validated production candidate'
    else:
        verdict = 'null (trainer/jockey random effects substrate-thin)'

    result = {
        'verdict': verdict,
        'sigma_trainer': trainer_var,
        'sigma_jockey': jockey_var,
        'beta_hybrid_c': beta_hp_post,
        'n_observations': int(len(df)),
        'n_trainers': len(trainers),
        'n_jockeys': len(jockeys),
        'mcmc_draws': draws,
    }
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Verdict: {verdict}; sigma_t={trainer_var:.4f} sigma_j={jockey_var:.4f}")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--window-start', default='2026-05-02')
    parser.add_argument('--window-end', default='2026-05-17')
    parser.add_argument('--draws', type=int, default=100)
    parser.add_argument('--tune', type=int, default=100)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    evaluate(args.window_start, args.window_end, args.output, args.draws, args.tune)


if __name__ == '__main__':
    main()
