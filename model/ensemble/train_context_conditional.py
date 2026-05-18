"""
Context-conditional ensemble per BD2v2 Section 3H.

Substrate-pragmatic gating: train separate XGBoost stackers per context bucket
(field_size_bucket × claim_price_tier), then route inference via gating
function over context features. Pace_scenario gating substrate-pragmatic-deferred
per T6 (pace_pressure_score location substrate-grep at authoring time).

Substrate-pragmatic minimum-viable: 2-dimensional context (field_size_bucket +
claim_price_tier). Tier 2 EXECUTION extends to pace_scenario when substrate-grep
confirms pace_pressure_score location.

§ 4.33 shared registration applied per sub-bucket.
§ 4.34 forensic-gate discipline.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import boto3
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import roc_auc_score, brier_score_loss

sys.path.insert(0, str(Path(__file__).parent))
from train_test_combined import (
    HYBRID_C_32_L1_INPUTS, HYBRID_C_HYPERPARAMS, NUM_BOOST_ROUND,
    EARLY_STOPPING_ROUNDS, load_training_parquets, load_actuals,
    get_db_conn, S3_BUCKET, S3_PREFIX,
)

sys.path.insert(0, str(Path(__file__).parent.parent / 'training'))
try:
    from registration import register_trained_artifact
except ImportError:
    register_trained_artifact = None


FIELD_SIZE_BUCKETS = [
    ('small', 0, 6),
    ('med',   7, 9),
    ('large', 10, 99),
]

CLAIM_PRICE_TIERS = [
    ('no_claim',     None, 0),
    ('low_claim',    1, 25000),
    ('high_claim',   25001, 999999),
]


def field_size_bucket(fs):
    if fs is None or fs == 0:
        return 'med'
    for name, lo, hi in FIELD_SIZE_BUCKETS:
        if lo <= fs <= hi:
            return name
    return 'med'


def claim_price_tier(cp):
    if cp is None or cp == 0:
        return 'no_claim'
    for name, lo, hi in CLAIM_PRICE_TIERS:
        if lo is None:
            continue
        if lo <= cp <= hi:
            return name
    return 'high_claim'


def load_context_meta(window_start, window_end):
    conn = get_db_conn()
    df = pd.read_sql("""
        SELECT r.race_id::text AS race_id,
               r.field_size,
               r.claiming_price
        FROM races r
        WHERE r.race_date BETWEEN %s AND %s
    """, conn, params=[window_start, window_end])
    conn.close()
    df['field_size_bucket'] = df['field_size'].apply(field_size_bucket)
    df['claim_price_tier'] = df['claiming_price'].apply(claim_price_tier)
    df['context_bucket'] = df['field_size_bucket'] + '__' + df['claim_price_tier']
    return df


def train_context_conditional(parquet_dir, output_path,
                              window_start='2026-04-25', window_end='2026-05-01',
                              register=True):
    feature_cols = HYBRID_C_32_L1_INPUTS

    training_df = load_training_parquets(parquet_dir)
    training_df['horse_id'] = training_df['horse_id'].astype(str)
    training_df['race_id'] = training_df['race_id'].astype(str)

    actuals_df = load_actuals(window_start, window_end)
    context_df = load_context_meta(window_start, window_end)

    merged = training_df.merge(actuals_df, on=['race_id', 'horse_id'], how='inner')
    merged = merged.merge(context_df[['race_id', 'context_bucket']], on='race_id', how='left')
    merged['context_bucket'] = merged['context_bucket'].fillna('med__no_claim')

    print(f"Merged: {len(merged)} rows")
    print(f"Context bucket distribution:")
    print(merged.groupby('context_bucket')['race_id'].nunique().sort_values(ascending=False))

    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')
    s3 = boto3.client('s3', region_name='us-east-1')

    sub_artifacts = {}
    for bucket, sub_df in merged.groupby('context_bucket'):
        if sub_df['race_id'].nunique() < 5:
            sub_artifacts[bucket] = {'status': 'substrate-thin', 'n_races': sub_df['race_id'].nunique()}
            continue

        np.random.seed(42)
        races = sorted(sub_df['race_id'].unique())
        np.random.shuffle(races)
        split_idx = max(1, int(len(races) * 0.8))
        train_races = set(races[:split_idx])
        eval_races = set(races[split_idx:])

        train_df = sub_df[sub_df['race_id'].isin(train_races)]
        eval_df = sub_df[sub_df['race_id'].isin(eval_races)]
        if len(eval_df) < 5:
            sub_artifacts[bucket] = {'status': 'eval-thin'}
            continue

        X_train = train_df[feature_cols].fillna(0.0).values
        y_train = train_df['is_winner'].values.astype(np.float32)
        X_eval = eval_df[feature_cols].fillna(0.0).values
        y_eval = eval_df['is_winner'].values.astype(np.float32)

        dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=feature_cols)
        deval = xgb.DMatrix(X_eval, label=y_eval, feature_names=feature_cols)

        try:
            booster = xgb.train(
                HYBRID_C_HYPERPARAMS, dtrain, num_boost_round=NUM_BOOST_ROUND,
                evals=[(deval, 'eval')],
                early_stopping_rounds=EARLY_STOPPING_ROUNDS, verbose_eval=False,
            )
        except Exception as e:
            sub_artifacts[bucket] = {'status': 'training-failed', 'error': str(e)}
            continue

        preds_eval = booster.predict(deval)
        try:
            auc_eval = float(roc_auc_score(y_eval, preds_eval)) if y_eval.sum() > 0 and y_eval.sum() < len(y_eval) else None
        except Exception:
            auc_eval = None
        brier_eval = float(brier_score_loss(y_eval, preds_eval.clip(0, 1)))

        version_name = f'context_conditional_{bucket}_{timestamp}'
        booster_local = output_path.replace('.json', f'.{bucket}.booster.json')
        booster.save_model(booster_local)

        s3_key = f'{S3_PREFIX}/{version_name}.json'
        s3_path = f's3://{S3_BUCKET}/{s3_key}'
        try:
            s3.upload_file(booster_local, S3_BUCKET, s3_key)
        except Exception as e:
            s3_path = booster_local

        sub_artifacts[bucket] = {
            'status': 'trained',
            'version_name': version_name,
            'eval_auc': auc_eval,
            'eval_brier': brier_eval,
            'n_train_races': len(train_races),
            'n_eval_races': len(eval_races),
            'booster_s3_path': s3_path,
        }
        print(f"  [{bucket}] n_races={len(races)} eval_auc={auc_eval} brier={brier_eval:.4f}")

        if register and register_trained_artifact is not None and auc_eval is not None:
            try:
                model_version_id = register_trained_artifact(
                    version_name=version_name,
                    model_type=f'ensemble_context_conditional_{bucket}',
                    s3_artifact_path=s3_path,
                    training_metadata={
                        'eval_auc': auc_eval, 'eval_brier': brier_eval,
                        'context_bucket': bucket,
                        'n_train_races': len(train_races),
                        'feature_names': feature_cols,
                    },
                    is_active=False,
                )
                sub_artifacts[bucket]['version_value'] = model_version_id
            except Exception as e:
                print(f"    Registration warning: {e}")

    meta = {
        'name': f'context_conditional_{timestamp}',
        'description': 'Context-conditional ensemble: field_size_bucket × claim_price_tier gating',
        'training_window': [window_start, window_end],
        'feature_cols': feature_cols,
        'context_dimensions': ['field_size_bucket', 'claim_price_tier'],
        'pace_scenario_note': 'pace_pressure_score gating substrate-pragmatic-deferred per T6 (not located in feature_engineering_service.py)',
        'sub_artifacts': sub_artifacts,
        'training_hyperparams': HYBRID_C_HYPERPARAMS,
        'substrate_version': 'v3-patched-f',
        'created_at': datetime.utcnow().isoformat(),
        'note': 'Inference-time meta-router for context-bucket→sub-artifact routing deferred to Tier 2 EXECUTION',
    }

    with open(output_path, 'w') as f:
        json.dump(meta, f, indent=2, default=str)
    return meta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parquet-dir', default='/tmp/option_c_predictions_train_aug')
    parser.add_argument('--training-window-start', default='2026-04-25')
    parser.add_argument('--training-window-end', default='2026-05-01')
    parser.add_argument('--output', required=True)
    parser.add_argument('--no-register', action='store_true')
    args = parser.parse_args()

    train_context_conditional(
        args.parquet_dir, args.output,
        args.training_window_start, args.training_window_end,
        register=not args.no_register,
    )


if __name__ == '__main__':
    main()
