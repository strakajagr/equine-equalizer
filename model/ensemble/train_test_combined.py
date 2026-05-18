"""
Test combined ensemble: Hybrid C 32-input + 1 additional L1 input.

Parameterized 3A/3B/3C variants per BD2v2:
  3A: --add lstm_trajectory_score
  3B: --add first_time_lasix_posterior_sparse  (SPARSE per Tier 1.5 Q4)
  3C: --add longshot_prob_substrate_correct    (Tier 1 2C substrate-correct path)

Hybrid C training hyperparams verbatim from train_hybrid_c.py (relocated from
/tmp/option_c_phase4_train_ensemble.py). Training cohort: same window as
Hybrid C (2026-04-25..2026-05-01).

Substrate-prerequisite: augment_parquets.py executed; augmented parquets at
/tmp/option_c_predictions_train_aug/ have 3 additional columns.

§ 4.33 shared registration applied post-training.
§ 4.34 forensic-gate discipline: is_active=False at registration; forensic_measure.py
       OOS measurement gates activation.
"""

import argparse
import glob
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import boto3
import numpy as np
import pandas as pd
import xgboost as xgb
import psycopg2
from sklearn.metrics import roc_auc_score, brier_score_loss

# § 4.33 shared registration
sys.path.insert(0, str(Path(__file__).parent.parent / 'training'))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'backend'))
from registration import register_trained_artifact

# 32 L1 inputs verbatim from option_c_hybrid_ensemble_meta.json (S3 artifact learner.feature_names)
HYBRID_C_32_L1_INPUTS = [
    'phase_bx__rk_full_speed__rk_full_lean53_speed_20260513_0324',
    'phase_bx__rk_full_closer__rk_full_lean53_closer_20260513_0327',
    'phase_bx__rk_full_class_riser__rk_full_lean53_class_riser_20260513_0302',
    'phase_bx__rk_full_route__rk_full_lean53_route_20260513_0255',
    'phase_bx__rk_full_sprint__rk_full_lean53_sprint_20260513_0251',
    'phase_bx__rk_full_gonzo_sauce__rk_full_lean53_gonzo_sauce_20260513_0324',
    'phase_bx__wp_full_general__wp_full_lean53_20260513_0311',
    'phase_bx__wp_full_speed__wp_full_lean53_speed_20260513_0325',
    'phase_bx__wp_full_closer__wp_full_lean53_closer_20260513_0324',
    'phase_bx__wp_full_route__wp_full_lean53_route_20260513_0255',
    'phase_bx__wp_full_class_dropper__wp_full_lean53_class_dropper_20260513_0325',
    'phase_bx__wp_full_class_riser__wp_full_lean53_class_riser_20260513_0323',
    'phase_bx__wp_full_sprint__wp_full_lean53_sprint_20260513_0258',
    'phase_bx__wp_full_gonzo_sauce__wp_full_lean53_gonzo_sauce_20260513_0310',
    'phase_bx__wr_base__v_base_core_20260513_0259',
    'phase_bx__pl_core_route__pl_core_lean53_route_20260513_0246',
    'phase_bx__wr_odds__v_odds_core_20260513_0259',
    'phase_bx__ranker_core__rk_core_20260513_0323',
    'phase_bx__win_prob_full__wp_odds_20260513_0126',
    'prior__pl_core_general__pl_core_lean53_20260429_1907',
    'prior__pl_core_speed__pl_core_lean53_speed_20260429_1906',
    'prior__pl_core_closer__pl_core_lean53_closer_20260429_1856',
    'prior__pl_core_class_riser__pl_core_lean53_class_riser_20260429_1856',
    'prior__pl_core_class_dropper__pl_core_lean53_class_dropper_20260429_1906',
    'prior__pl_core_sprint__pl_core_lean53_sprint_20260429_1845',
    'prior__rk_full_class_dropper__rk_full_lean53_class_dropper_20260429_1854',
    'prior__win_prob_core_speed__wp_core_lean53_speed_20260429_2348',
    'prior__win_prob_core_closer__wp_core_lean53_closer_20260429_2348',
    'prior__win_prob_core_class_riser__wp_core_lean53_class_riser_20260429_2338',
    'prior__win_prob_core_class_dropper__wp_core_lean53_class_dropper_20260429_2338',
    'prior__win_prob_core_sprint__wp_core_lean53_sprint_20260429_2332',
    'prior__win_prob_core_route__wp_core_lean53_route_20260429_2329',
]

ADDITIONAL_INPUT_CHOICES = {
    'lstm_trajectory_score': 'lstm_trajectory_score',
    'first_time_lasix_posterior_sparse': 'first_time_lasix_posterior_sparse',
    'longshot_prob_substrate_correct': 'longshot_prob_substrate_correct',
}

# Hybrid C training hyperparams verbatim from train_hybrid_c.py
HYBRID_C_HYPERPARAMS = {
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'learning_rate': 0.05,
    'max_depth': 3,
    'subsample': 0.7,
    'colsample_bytree': 0.6,
    'min_child_weight': 3,
    'reg_alpha': 0.5,
    'reg_lambda': 2.0,
}
NUM_BOOST_ROUND = 500
EARLY_STOPPING_ROUNDS = 30
PHASE_BX_BASELINE_AUC = 0.786

DB_SECRET_ARN = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'
S3_BUCKET = 'equine-model-artifacts'
S3_PREFIX = 'ensemble/test'


def get_db_conn():
    sm = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString'])
    return psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'],
        password=secret['password'],
    )


def load_training_parquets(parquet_dir):
    """Load augmented training parquets; race_id stem → race_id column."""
    parquets = sorted(glob.glob(f'{parquet_dir}/*.parquet'))
    if not parquets:
        raise ValueError(f"Substrate-broken: no parquets in {parquet_dir}")

    dfs = []
    for p in parquets:
        race_id = Path(p).stem
        df = pd.read_parquet(p)
        if 'race_id' not in df.columns:
            df['race_id'] = race_id
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    print(f"Loaded {len(parquets)} parquets; {len(df)} total rows")
    return df


def load_actuals(window_start, window_end):
    """Pull is_winner target."""
    conn = get_db_conn()
    df = pd.read_sql("""
        SELECT res.race_id::text AS race_id,
               res.horse_id::text AS horse_id,
               (res.finish_position = 1)::int AS is_winner
        FROM results res
        JOIN races r ON r.race_id = res.race_id
        WHERE r.race_date BETWEEN %s AND %s
          AND res.finish_position IS NOT NULL
    """, conn, params=[window_start, window_end])
    conn.close()
    return df


def train_test_ensemble(parquet_dir, add_input_key, output_path,
                       window_start='2026-04-25', window_end='2026-05-01',
                       register=True):
    additional_col = ADDITIONAL_INPUT_CHOICES[add_input_key]
    feature_cols = HYBRID_C_32_L1_INPUTS + [additional_col]

    training_df = load_training_parquets(parquet_dir)
    training_df['horse_id'] = training_df['horse_id'].astype(str)
    training_df['race_id'] = training_df['race_id'].astype(str)

    actuals_df = load_actuals(window_start, window_end)
    print(f"Actuals rows: {len(actuals_df)}")

    merged = training_df.merge(actuals_df, on=['race_id', 'horse_id'], how='inner')
    print(f"Merged training cohort: {len(merged)} rows ({merged['race_id'].nunique()} races)")

    missing_cols = [c for c in feature_cols if c not in merged.columns]
    if missing_cols:
        raise ValueError(f"Substrate-broken: missing feature columns: {missing_cols[:5]}... (total {len(missing_cols)})")

    # Race-level 80/20 split per Hybrid C training methodology
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

    print(f"Train: {len(train_races)} races / {len(X_train)} rows / {int(y_train.sum())} winners")
    print(f"Eval:  {len(eval_races)} races / {len(X_eval)} rows / {int(y_eval.sum())} winners")

    dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=feature_cols)
    deval = xgb.DMatrix(X_eval, label=y_eval, feature_names=feature_cols)

    booster = xgb.train(
        HYBRID_C_HYPERPARAMS, dtrain, num_boost_round=NUM_BOOST_ROUND,
        evals=[(dtrain, 'train'), (deval, 'eval')],
        early_stopping_rounds=EARLY_STOPPING_ROUNDS, verbose_eval=50,
    )

    preds_train = booster.predict(dtrain)
    preds_eval = booster.predict(deval)
    auc_train = float(roc_auc_score(y_train, preds_train))
    auc_eval = float(roc_auc_score(y_eval, preds_eval))
    brier_eval = float(brier_score_loss(y_eval, preds_eval.clip(0, 1)))

    # Top-1 per race
    eval_df['ensemble_pred'] = preds_eval
    top1_eval = eval_df.loc[eval_df.groupby('race_id')['ensemble_pred'].idxmax()]
    top1_eval_wr = float(top1_eval['is_winner'].mean())

    print(f"\nTest ensemble metrics:")
    print(f"  TRAIN AUC: {auc_train:.4f}")
    print(f"  EVAL  AUC: {auc_eval:.4f}  Brier: {brier_eval:.4f}  top1: {top1_eval_wr*100:.2f}%")

    importance = booster.get_score(importance_type='gain')
    candidate_importance = float(importance.get(additional_col, 0))
    print(f"  Additional input ({additional_col}) feature gain: {candidate_importance:.2f}")

    # Serialize artifact
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')
    version_name = f'hybrid_c_plus_{add_input_key}_{timestamp}'
    booster_local = output_path.replace('.json', '.booster.json')
    booster.save_model(booster_local)

    s3_key = f'{S3_PREFIX}/{version_name}.json'
    s3_path = f's3://{S3_BUCKET}/{s3_key}'

    s3 = boto3.client('s3', region_name='us-east-1')
    try:
        s3.upload_file(booster_local, S3_BUCKET, s3_key)
        print(f"  S3: {s3_path}")
    except Exception as e:
        print(f"  S3 upload warning: {e}")
        s3_path = booster_local  # fall back to local path for artifact reference

    artifact = {
        'name': version_name,
        'description': f'Test ensemble: Hybrid C 32-input + {add_input_key} (33-input)',
        'feature_cols': feature_cols,
        'training_window': [window_start, window_end],
        'training_eval_auc': auc_eval,
        'training_eval_brier': brier_eval,
        'training_top1_winrate': top1_eval_wr,
        'training_auc_train': auc_train,
        'candidate_input': add_input_key,
        'candidate_feature_importance': candidate_importance,
        'training_hyperparams': HYBRID_C_HYPERPARAMS,
        'booster_s3_path': s3_path,
        'substrate_version': 'v3-patched-f',
        'created_at': datetime.utcnow().isoformat(),
        # forensic_measure.py consumption metadata
        'predictions_table': 'wr_predictions',
        'prediction_column': 'win_probability',
        'version_column': 'model_version_id',
        'version_value': None,  # populated post-registration
        'date_column': 'created_at',
        'horse_id_cast': None,
    }

    model_version_id = None
    if register:
        try:
            model_version_id = register_trained_artifact(
                version_name=version_name,
                model_type=f'ensemble_test_hybrid_c_plus_{add_input_key}',
                s3_artifact_path=s3_path,
                training_metadata={
                    'eval_auc': auc_eval,
                    'eval_brier': brier_eval,
                    'top1_winrate': top1_eval_wr,
                    'train_auc': auc_train,
                    'training_window': f'{window_start}..{window_end}',
                    'feature_count': len(feature_cols),
                    'candidate_input': add_input_key,
                    'candidate_feature_importance': candidate_importance,
                    'hyperparameters': HYBRID_C_HYPERPARAMS,
                    'feature_names': feature_cols,
                },
                is_active=False,  # § 4.34 forensic-gate discipline
            )
            print(f"  Registered: model_version_id={model_version_id}")
        except Exception as e:
            print(f"  Registration warning: {e}")

    artifact['version_value'] = model_version_id

    with open(output_path, 'w') as f:
        json.dump(artifact, f, indent=2, default=str)

    return artifact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--add', required=True, choices=list(ADDITIONAL_INPUT_CHOICES.keys()))
    parser.add_argument('--parquet-dir', default='/tmp/option_c_predictions_train_aug')
    parser.add_argument('--training-window-start', default='2026-04-25')
    parser.add_argument('--training-window-end', default='2026-05-01')
    parser.add_argument('--output', required=True)
    parser.add_argument('--no-register', action='store_true',
                        help='Skip §4.33 registration (substrate-pragmatic for dry runs)')
    args = parser.parse_args()

    artifact = train_test_ensemble(
        args.parquet_dir, args.add, args.output,
        args.training_window_start, args.training_window_end,
        register=not args.no_register,
    )
    print(f"\nArtifact: {args.output}")


if __name__ == '__main__':
    main()
