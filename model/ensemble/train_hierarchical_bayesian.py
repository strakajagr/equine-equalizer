"""
Hierarchical Bayesian ensemble per BD2v2 Section 3F.

Substrate-pragmatic minimum-viable: pymc Bayesian linear model with per-track
random effects on the 32 L1 inputs. Output: posterior mean win_probability
per (race, horse). Compared against Hybrid C flat XGBoost stacker via
forensic_measure.py.

INVOCATION: must run via .venv-bayesian/bin/python (pymc installed there).

Substrate-pragmatic MCMC settings: draws=300, tune=300, chains=2 for synthetic
substrate-validation runtime (~2-3 min on 1,583 rows). Tier 2 EXECUTION
re-invokes with production-grade draws=2000+ for posterior calibration.

§ 4.33 shared registration applied.
§ 4.34 forensic-gate discipline.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from train_test_combined import (
    HYBRID_C_32_L1_INPUTS, load_training_parquets, load_actuals,
    get_db_conn, S3_BUCKET, S3_PREFIX,
)

sys.path.insert(0, str(Path(__file__).parent.parent / 'training'))
try:
    from registration import register_trained_artifact
except ImportError:
    register_trained_artifact = None

# pymc imports deferred until train_hierarchical() invocation
def _import_pymc():
    import pymc as pm
    import pytensor.tensor as pt
    return pm, pt


def train_hierarchical(parquet_dir, output_path,
                       window_start='2026-04-25', window_end='2026-05-01',
                       draws=300, tune=300, chains=2, register=True):
    pm, pt = _import_pymc()
    feature_cols = HYBRID_C_32_L1_INPUTS

    training_df = load_training_parquets(parquet_dir)
    training_df['horse_id'] = training_df['horse_id'].astype(str)
    training_df['race_id'] = training_df['race_id'].astype(str)

    actuals_df = load_actuals(window_start, window_end)

    # Pull track_code per race for hierarchical grouping
    conn = get_db_conn()
    race_meta = pd.read_sql("""
        SELECT r.race_id::text AS race_id, t.track_code
        FROM races r LEFT JOIN tracks t ON t.track_id = r.track_id
        WHERE r.race_date BETWEEN %s AND %s
    """, conn, params=[window_start, window_end])
    conn.close()

    merged = training_df.merge(actuals_df, on=['race_id', 'horse_id'], how='inner')
    merged = merged.merge(race_meta, on='race_id', how='left')
    merged['track_code'] = merged['track_code'].fillna('UNK')
    print(f"Merged: {len(merged)} rows, {merged['track_code'].nunique()} tracks")

    np.random.seed(42)
    races = sorted(merged['race_id'].unique())
    np.random.shuffle(races)
    split_idx = int(len(races) * 0.8)
    train_races = set(races[:split_idx])
    eval_races = set(races[split_idx:])

    train_df = merged[merged['race_id'].isin(train_races)].reset_index(drop=True)
    eval_df = merged[merged['race_id'].isin(eval_races)].reset_index(drop=True)

    # Encode tracks
    track_codes_all = sorted(merged['track_code'].unique())
    track_idx_map = {t: i for i, t in enumerate(track_codes_all)}
    train_track_idx = train_df['track_code'].map(track_idx_map).values
    eval_track_idx = eval_df['track_code'].map(track_idx_map).values

    X_train = train_df[feature_cols].fillna(0.0).values.astype(np.float64)
    y_train = train_df['is_winner'].values.astype(np.int8)
    X_eval = eval_df[feature_cols].fillna(0.0).values.astype(np.float64)
    y_eval = eval_df['is_winner'].values.astype(np.int8)

    # Standardize features for MCMC stability
    feat_means = X_train.mean(axis=0)
    feat_stds = X_train.std(axis=0)
    feat_stds[feat_stds == 0] = 1.0
    X_train_std = (X_train - feat_means) / feat_stds
    X_eval_std = (X_eval - feat_means) / feat_stds

    n_features = len(feature_cols)
    n_tracks = len(track_codes_all)

    print(f"Bayesian hierarchical: {n_features} features, {n_tracks} tracks")
    print(f"MCMC: draws={draws}, tune={tune}, chains={chains}")

    with pm.Model() as model:
        # Hyper-priors
        mu_beta = pm.Normal('mu_beta', mu=0.0, sigma=1.0, shape=n_features)
        sigma_beta = pm.HalfNormal('sigma_beta', sigma=0.5)

        # Per-track random effects (intercept only for substrate-pragmatic minimum-viable)
        sigma_track = pm.HalfNormal('sigma_track', sigma=0.5)
        track_offsets = pm.Normal('track_offsets', mu=0.0, sigma=sigma_track, shape=n_tracks)

        # Per-feature coefficients (pooled across tracks per substrate-pragmatic)
        beta = pm.Normal('beta', mu=mu_beta, sigma=sigma_beta, shape=n_features)

        # Intercept
        alpha = pm.Normal('alpha', mu=-2.0, sigma=1.0)  # prior: P(win) ≈ 0.12

        # Linear predictor
        logit = alpha + track_offsets[train_track_idx] + pm.math.dot(X_train_std, beta)

        # Likelihood
        pm.Bernoulli('obs', logit_p=logit, observed=y_train)

        # Sample
        trace = pm.sample(draws=draws, tune=tune, chains=chains,
                          target_accept=0.9, progressbar=True,
                          return_inferencedata=True)

    # Posterior predictive on eval set
    posterior = trace.posterior
    beta_mean = posterior['beta'].mean(dim=['chain', 'draw']).values  # (n_features,)
    alpha_mean = float(posterior['alpha'].mean(dim=['chain', 'draw']).values)
    track_offsets_mean = posterior['track_offsets'].mean(dim=['chain', 'draw']).values

    eval_logit = alpha_mean + track_offsets_mean[eval_track_idx] + X_eval_std @ beta_mean
    eval_preds = 1.0 / (1.0 + np.exp(-eval_logit))

    from sklearn.metrics import roc_auc_score, brier_score_loss
    eval_auc = float(roc_auc_score(y_eval, eval_preds))
    eval_brier = float(brier_score_loss(y_eval, eval_preds))

    eval_df['ensemble_pred'] = eval_preds
    top1_eval = eval_df.loc[eval_df.groupby('race_id')['ensemble_pred'].idxmax()]
    top1_eval_wr = float(top1_eval['is_winner'].mean())

    print(f"\nHierarchical Bayesian metrics:")
    print(f"  EVAL AUC: {eval_auc:.4f}  Brier: {eval_brier:.4f}  top1: {top1_eval_wr*100:.2f}%")

    # Persist (posterior trace + meta)
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')
    version_name = f'hierarchical_bayesian_{timestamp}'

    trace_path = output_path.replace('.json', '.trace.nc')
    try:
        trace.to_netcdf(trace_path)
    except Exception as e:
        print(f"  Trace save warning: {e}")
        trace_path = None

    artifact = {
        'name': version_name,
        'description': 'Hierarchical Bayesian: per-track random effects + pooled feature coefficients',
        'feature_cols': feature_cols,
        'training_window': [window_start, window_end],
        'training_eval_auc': eval_auc,
        'training_eval_brier': eval_brier,
        'training_top1_winrate': top1_eval_wr,
        'mcmc_draws': draws,
        'mcmc_tune': tune,
        'mcmc_chains': chains,
        'n_tracks': n_tracks,
        'track_codes': track_codes_all,
        'feature_means': feat_means.tolist(),
        'feature_stds': feat_stds.tolist(),
        'beta_mean': beta_mean.tolist(),
        'alpha_mean': alpha_mean,
        'track_offsets_mean': track_offsets_mean.tolist(),
        'trace_path': trace_path,
        'substrate_version': 'v3-patched-f',
        'created_at': datetime.utcnow().isoformat(),
    }

    if register and register_trained_artifact is not None:
        try:
            model_version_id = register_trained_artifact(
                version_name=version_name,
                model_type='ensemble_hierarchical_bayesian',
                s3_artifact_path=output_path,
                training_metadata={
                    'eval_auc': eval_auc, 'eval_brier': eval_brier,
                    'top1_winrate': top1_eval_wr,
                    'mcmc_draws': draws, 'n_tracks': n_tracks,
                    'feature_names': feature_cols,
                },
                is_active=False,
            )
            artifact['version_value'] = model_version_id
        except Exception as e:
            print(f"  Registration warning: {e}")

    with open(output_path, 'w') as f:
        json.dump(artifact, f, indent=2, default=str)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parquet-dir', default='/tmp/option_c_predictions_train_aug')
    parser.add_argument('--training-window-start', default='2026-04-25')
    parser.add_argument('--training-window-end', default='2026-05-01')
    parser.add_argument('--output', required=True)
    parser.add_argument('--draws', type=int, default=300)
    parser.add_argument('--tune', type=int, default=300)
    parser.add_argument('--chains', type=int, default=2)
    parser.add_argument('--no-register', action='store_true')
    args = parser.parse_args()

    train_hierarchical(
        args.parquet_dir, args.output,
        args.training_window_start, args.training_window_end,
        draws=args.draws, tune=args.tune, chains=args.chains,
        register=not args.no_register,
    )


if __name__ == '__main__':
    main()
