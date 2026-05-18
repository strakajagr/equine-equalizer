"""
Specialist architecture variants per BD2v2 Section 3E.

Substrate-pragmatic variants (partition training cohort then train per-partition
XGBoost stacker; meta-routing deferred to Tier 2 EXECUTION):

  style_specialist:      partition by race style (Sprint/Route via race distance)
  track_specialist:      partition by track family (NY/SoCal/KY/FL/Mid-Atl per T5)
  field_size_specialist: partition by field_size buckets (≤6 / 7-9 / 10-12 / 13+)

Each variant produces N sub-artifacts (one per partition) + a meta-artifact
collecting their substrate. Tier 2 EXECUTION would route at inference time.

§ 4.33 shared registration applied per sub-artifact.
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
from registration import register_trained_artifact


# Per T5 substrate-pragmatic taxonomy
TRACK_FAMILIES = {
    'NY':       ['AQU', 'BEL', 'SAR'],
    'SoCal':    ['SA', 'DMR'],
    'KY':       ['CD', 'KEE'],
    'FL':       ['GP'],
    'MidAtl':   ['PIM', 'MTH', 'LRL'],
    'Other':    [],  # catch-all
}

FIELD_SIZE_BUCKETS = [
    ('small',  0, 6),
    ('med',    7, 9),
    ('large',  10, 12),
    ('xlarge', 13, 99),
]


def load_race_metadata(window_start, window_end):
    """Pull race metadata for partitioning: track_code + field_size + distance_furlongs."""
    conn = get_db_conn()
    df = pd.read_sql("""
        SELECT r.race_id::text AS race_id,
               t.track_code,
               r.field_size,
               r.distance_furlongs::float AS distance_furlongs
        FROM races r
        LEFT JOIN tracks t ON t.track_id = r.track_id
        WHERE r.race_date BETWEEN %s AND %s
    """, conn, params=[window_start, window_end])
    conn.close()
    return df


def partition_style(race_meta_df):
    """Substrate-pragmatic style: Sprint (≤6.5f) vs Route (>6.5f)."""
    df = race_meta_df.copy()
    df['partition'] = df['distance_furlongs'].apply(
        lambda d: 'sprint' if (d is not None and d <= 6.5) else 'route'
    )
    return df[['race_id', 'partition']]


def partition_track(race_meta_df):
    df = race_meta_df.copy()

    def family(code):
        for fam, tracks in TRACK_FAMILIES.items():
            if code in tracks:
                return fam
        return 'Other'

    df['partition'] = df['track_code'].apply(family)
    return df[['race_id', 'partition']]


def partition_field_size(race_meta_df):
    df = race_meta_df.copy()

    def bucket(fs):
        if fs is None or fs == 0:
            return 'med'
        for name, lo, hi in FIELD_SIZE_BUCKETS:
            if lo <= fs <= hi:
                return name
        return 'med'

    df['partition'] = df['field_size'].apply(bucket)
    return df[['race_id', 'partition']]


PARTITION_FN = {
    'style_specialist':      partition_style,
    'track_specialist':      partition_track,
    'field_size_specialist': partition_field_size,
}


def train_specialist(parquet_dir, variant, output_path,
                     window_start='2026-04-25', window_end='2026-05-01',
                     register=True):
    feature_cols = HYBRID_C_32_L1_INPUTS

    training_df = load_training_parquets(parquet_dir)
    training_df['horse_id'] = training_df['horse_id'].astype(str)
    training_df['race_id'] = training_df['race_id'].astype(str)

    actuals_df = load_actuals(window_start, window_end)
    race_meta = load_race_metadata(window_start, window_end)

    merged = training_df.merge(actuals_df, on=['race_id', 'horse_id'], how='inner')
    partitions = PARTITION_FN[variant](race_meta)
    merged = merged.merge(partitions, on='race_id', how='left')
    merged['partition'] = merged['partition'].fillna('Other')

    print(f"Variant: {variant}")
    print(f"Partition distribution:")
    print(merged.groupby('partition')['race_id'].nunique())

    sub_artifacts = {}
    s3 = boto3.client('s3', region_name='us-east-1')
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')

    for partition_name, sub_df in merged.groupby('partition'):
        if sub_df['race_id'].nunique() < 5:
            print(f"  [{partition_name}] substrate-thin (<5 races); skipped")
            sub_artifacts[partition_name] = {'status': 'substrate-thin', 'n_races': sub_df['race_id'].nunique()}
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
            print(f"  [{partition_name}] eval substrate-thin (<5 rows); skipped")
            sub_artifacts[partition_name] = {'status': 'eval-thin', 'n_train_races': len(train_races)}
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
            print(f"  [{partition_name}] training failed: {e}")
            sub_artifacts[partition_name] = {'status': 'training-failed', 'error': str(e)}
            continue

        preds_eval = booster.predict(deval)
        try:
            auc_eval = float(roc_auc_score(y_eval, preds_eval)) if y_eval.sum() > 0 and y_eval.sum() < len(y_eval) else None
        except Exception:
            auc_eval = None
        brier_eval = float(brier_score_loss(y_eval, preds_eval.clip(0, 1)))

        print(f"  [{partition_name}] n_races={len(train_races)+len(eval_races)} "
              f"eval_auc={auc_eval} brier={brier_eval:.4f}")

        # Persist sub-booster
        version_name = f'specialist_{variant}_{partition_name}_{timestamp}'
        booster_local = output_path.replace('.json', f'.{partition_name}.booster.json')
        booster.save_model(booster_local)

        s3_key = f'{S3_PREFIX}/{version_name}.json'
        s3_path = f's3://{S3_BUCKET}/{s3_key}'
        try:
            s3.upload_file(booster_local, S3_BUCKET, s3_key)
        except Exception as e:
            s3_path = booster_local
            print(f"    S3 upload warning: {e}")

        sub_artifact = {
            'status': 'trained',
            'partition': partition_name,
            'version_name': version_name,
            'eval_auc': auc_eval,
            'eval_brier': brier_eval,
            'n_train_races': len(train_races),
            'n_eval_races': len(eval_races),
            'booster_s3_path': s3_path,
        }

        if register and auc_eval is not None:
            try:
                model_version_id = register_trained_artifact(
                    version_name=version_name,
                    model_type=f'ensemble_specialist_{variant}_{partition_name}',
                    s3_artifact_path=s3_path,
                    training_metadata={
                        'eval_auc': auc_eval, 'eval_brier': brier_eval,
                        'variant': variant, 'partition': partition_name,
                        'n_train_races': len(train_races),
                        'n_eval_races': len(eval_races),
                        'hyperparameters': HYBRID_C_HYPERPARAMS,
                    },
                    is_active=False,
                )
                sub_artifact['version_value'] = model_version_id
            except Exception as e:
                print(f"    Registration warning: {e}")

        sub_artifacts[partition_name] = sub_artifact

    # Meta-artifact
    meta = {
        'name': f'specialist_{variant}_{timestamp}',
        'description': f'Specialist architecture: {variant}',
        'variant': variant,
        'training_window': [window_start, window_end],
        'feature_cols': feature_cols,
        'sub_artifacts': sub_artifacts,
        'training_hyperparams': HYBRID_C_HYPERPARAMS,
        'substrate_version': 'v3-patched-f',
        'created_at': datetime.utcnow().isoformat(),
        # forensic_measure consumption: meta-artifact requires meta-router at inference
        'note': 'Meta-router for partition→sub-artifact routing deferred to Tier 2 EXECUTION',
    }

    with open(output_path, 'w') as f:
        json.dump(meta, f, indent=2, default=str)
    return meta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--variant', required=True, choices=list(PARTITION_FN.keys()))
    parser.add_argument('--parquet-dir', default='/tmp/option_c_predictions_train_aug')
    parser.add_argument('--training-window-start', default='2026-04-25')
    parser.add_argument('--training-window-end', default='2026-05-01')
    parser.add_argument('--output', required=True)
    parser.add_argument('--no-register', action='store_true')
    args = parser.parse_args()

    train_specialist(
        args.parquet_dir, args.variant, args.output,
        args.training_window_start, args.training_window_end,
        register=not args.no_register,
    )


if __name__ == '__main__':
    main()
