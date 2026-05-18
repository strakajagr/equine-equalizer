"""
Multi-cohort ensemble variant training per BD2v2 Section 3D.

Substrate-pragmatic variants (filter HYBRID_C_32_L1_INPUTS by cohort prefix):
  pure_bx:             phase_bx__* only (19 inputs)
  pure_prior:          prior__* only (13 inputs)
  three_cohort_hybrid: all 32 inputs (Hybrid C composition baseline reference)

Reuses Hybrid C training methodology + hyperparams from train_test_combined.py.
Each variant trains XGBoost stacker; artifacts consumable by forensic_measure.py.

§ 4.33 shared registration applied post-training.
§ 4.34 forensic-gate discipline: is_active=False at registration.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

# Reuse train_test_combined.py infrastructure
sys.path.insert(0, str(Path(__file__).parent))
from train_test_combined import (
    HYBRID_C_32_L1_INPUTS, HYBRID_C_HYPERPARAMS, NUM_BOOST_ROUND,
    EARLY_STOPPING_ROUNDS, load_training_parquets, load_actuals,
    get_db_conn, S3_BUCKET, S3_PREFIX,
)

import boto3
import xgboost as xgb
from sklearn.metrics import roc_auc_score, brier_score_loss

sys.path.insert(0, str(Path(__file__).parent.parent / 'training'))
from registration import register_trained_artifact


COHORT_VARIANTS = {
    'pure_bx':            [c for c in HYBRID_C_32_L1_INPUTS if c.startswith('phase_bx__')],
    'pure_prior':         [c for c in HYBRID_C_32_L1_INPUTS if c.startswith('prior__')],
    'three_cohort_hybrid': HYBRID_C_32_L1_INPUTS,
}


def train_variant(parquet_dir, variant, output_path,
                  window_start='2026-04-25', window_end='2026-05-01',
                  register=True):
    feature_cols = COHORT_VARIANTS[variant]
    print(f"Variant: {variant} ({len(feature_cols)} features)")

    training_df = load_training_parquets(parquet_dir)
    training_df['horse_id'] = training_df['horse_id'].astype(str)
    training_df['race_id'] = training_df['race_id'].astype(str)

    actuals_df = load_actuals(window_start, window_end)
    merged = training_df.merge(actuals_df, on=['race_id', 'horse_id'], how='inner')
    print(f"Merged training cohort: {len(merged)} rows ({merged['race_id'].nunique()} races)")

    missing_cols = [c for c in feature_cols if c not in merged.columns]
    if missing_cols:
        raise ValueError(f"Substrate-broken: missing feature columns: {missing_cols[:5]}...")

    np.random.seed(42)
    races = sorted(merged['race_id'].unique())
    np.random.shuffle(races)
    split_idx = int(len(races) * 0.8)
    train_races = set(races[:split_idx])
    eval_races = set(races[split_idx:])

    train_df = merged[merged['race_id'].isin(train_races)].reset_index(drop=True)
    eval_df = merged[merged['race_id'].isin(eval_races)].reset_index(drop=True)

    X_train = train_df[feature_cols].fillna(0.0).values
    y_train = train_df['is_winner'].values.astype(np.float32)
    X_eval = eval_df[feature_cols].fillna(0.0).values
    y_eval = eval_df['is_winner'].values.astype(np.float32)

    dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=feature_cols)
    deval = xgb.DMatrix(X_eval, label=y_eval, feature_names=feature_cols)

    booster = xgb.train(
        HYBRID_C_HYPERPARAMS, dtrain, num_boost_round=NUM_BOOST_ROUND,
        evals=[(dtrain, 'train'), (deval, 'eval')],
        early_stopping_rounds=EARLY_STOPPING_ROUNDS, verbose_eval=50,
    )

    auc_train = float(roc_auc_score(y_train, booster.predict(dtrain)))
    preds_eval = booster.predict(deval)
    auc_eval = float(roc_auc_score(y_eval, preds_eval))
    brier_eval = float(brier_score_loss(y_eval, preds_eval.clip(0, 1)))

    eval_df['ensemble_pred'] = preds_eval
    top1_eval = eval_df.loc[eval_df.groupby('race_id')['ensemble_pred'].idxmax()]
    top1_eval_wr = float(top1_eval['is_winner'].mean())

    print(f"  TRAIN AUC: {auc_train:.4f}")
    print(f"  EVAL  AUC: {auc_eval:.4f}  Brier: {brier_eval:.4f}  top1: {top1_eval_wr*100:.2f}%")

    # Persist
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')
    version_name = f'multi_cohort_{variant}_{timestamp}'
    booster_local = output_path.replace('.json', '.booster.json')
    booster.save_model(booster_local)

    s3_key = f'{S3_PREFIX}/{version_name}.json'
    s3_path = f's3://{S3_BUCKET}/{s3_key}'
    try:
        boto3.client('s3', region_name='us-east-1').upload_file(booster_local, S3_BUCKET, s3_key)
    except Exception as e:
        print(f"  S3 upload warning: {e}")
        s3_path = booster_local

    artifact = {
        'name': version_name,
        'description': f'Multi-cohort variant: {variant} ({len(feature_cols)} L1 inputs)',
        'variant': variant,
        'feature_cols': feature_cols,
        'training_window': [window_start, window_end],
        'training_eval_auc': auc_eval,
        'training_eval_brier': brier_eval,
        'training_top1_winrate': top1_eval_wr,
        'training_auc_train': auc_train,
        'training_hyperparams': HYBRID_C_HYPERPARAMS,
        'booster_s3_path': s3_path,
        'substrate_version': 'v3-patched-f',
        'created_at': datetime.utcnow().isoformat(),
        'predictions_table': 'wr_predictions',
        'prediction_column': 'win_probability',
        'version_column': 'model_version_id',
        'version_value': None,
        'date_column': 'created_at',
        'horse_id_cast': None,
    }

    if register:
        try:
            model_version_id = register_trained_artifact(
                version_name=version_name,
                model_type=f'ensemble_multi_cohort_{variant}',
                s3_artifact_path=s3_path,
                training_metadata={
                    'eval_auc': auc_eval, 'eval_brier': brier_eval,
                    'top1_winrate': top1_eval_wr, 'train_auc': auc_train,
                    'variant': variant, 'feature_count': len(feature_cols),
                    'hyperparameters': HYBRID_C_HYPERPARAMS,
                    'feature_names': feature_cols,
                },
                is_active=False,
            )
            artifact['version_value'] = model_version_id
            print(f"  Registered: {model_version_id}")
        except Exception as e:
            print(f"  Registration warning: {e}")

    with open(output_path, 'w') as f:
        json.dump(artifact, f, indent=2, default=str)
    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--variant', required=True, choices=list(COHORT_VARIANTS.keys()))
    parser.add_argument('--parquet-dir', default='/tmp/option_c_predictions_train_aug')
    parser.add_argument('--training-window-start', default='2026-04-25')
    parser.add_argument('--training-window-end', default='2026-05-01')
    parser.add_argument('--output', required=True)
    parser.add_argument('--no-register', action='store_true')
    args = parser.parse_args()

    train_variant(
        args.parquet_dir, args.variant, args.output,
        args.training_window_start, args.training_window_end,
        register=not args.no_register,
    )


if __name__ == '__main__':
    main()
