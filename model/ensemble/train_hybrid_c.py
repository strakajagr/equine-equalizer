#!/usr/bin/env python3
"""Phase 4 — Train hybrid culled-rebuilt ensemble on 30 surviving L1 layers."""
import os, sys, json, glob, uuid
os.environ['DB_SECRET_ARN'] = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'
os.environ.pop('DATABASE_URL', None)
sys.path.insert(0, '/home/strakajagr/projects/equine-equalizer/backend')

import boto3
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import roc_auc_score, brier_score_loss
from shared.db import get_db, execute_query

# 30 surviving layers per Tony Phase 3 adjudication (verbatim from dispatch)
SURVIVING_PHASE_BX_LAYERS = [
    # Ranker (7 variants; all B.x except class_dropper)
    'phase_bx__ranker_full__rk_full_20260513_0324',  # rk_full_general — Phase B.x has ranker_full
    'phase_bx__rk_full_speed',
    'phase_bx__rk_full_closer',
    'phase_bx__rk_full_class_riser',
    'phase_bx__rk_full_route',
    'phase_bx__rk_full_sprint',
    'phase_bx__rk_full_gonzo_sauce',
    # WP_full (8 variants; all B.x)
    'phase_bx__wp_full_general',
    'phase_bx__wp_full_speed',
    'phase_bx__wp_full_closer',
    'phase_bx__wp_full_route',
    'phase_bx__wp_full_class_dropper',
    'phase_bx__wp_full_class_riser',
    'phase_bx__wp_full_sprint',
    'phase_bx__wp_full_gonzo_sauce',
    # Other B.x
    'phase_bx__wr_base',
    'phase_bx__pl_core_route',
    # Ensemble-input-only
    'phase_bx__wr_odds',
    'phase_bx__ranker_core',
    'phase_bx__win_prob_full',
]
SURVIVING_PRIOR_LAYERS = [
    # PL_core (6 variants; all PRIOR except route)
    'prior__pl_core_general',
    'prior__pl_core_speed',
    'prior__pl_core_closer',
    'prior__pl_core_class_riser',
    'prior__pl_core_class_dropper',
    'prior__pl_core_sprint',
    # rk_full_class_dropper (only ranker where PRIOR > B.x)
    'prior__rk_full_class_dropper',
    # win_prob_core (7 PRIOR-only specialists + general)
    'prior__win_prob_core_general',
    'prior__win_prob_core_speed',
    'prior__win_prob_core_closer',
    'prior__win_prob_core_class_riser',
    'prior__win_prob_core_class_dropper',
    'prior__win_prob_core_sprint',
    'prior__win_prob_core_route',
]


def find_matching_columns(df_columns, prefix_patterns):
    """For each pattern like 'phase_bx__rk_full_speed', find the full column name(s)
    in df_columns that start with that prefix (allowing for the version_name suffix)."""
    matches = []
    for pat in prefix_patterns:
        # Column format: cohort__model_type__version_name
        # pattern may be a 2-component (cohort__model_type) or 3-component prefix
        candidates = [c for c in df_columns if c.startswith(pat + '__') or c == pat or c.startswith(pat)]
        # Pick the FIRST match (deterministic; matches the dedup'd canonical artifact)
        if candidates:
            matches.append(candidates[0])
        else:
            matches.append(None)
    return matches


def main():
    train_dir = '/tmp/option_c_predictions_train'
    files = glob.glob(f'{train_dir}/*.parquet')
    print(f"Loading {len(files)} training-window parquets...")
    dfs = []
    for f in files:
        race_id = os.path.basename(f).replace('.parquet', '')
        df = pd.read_parquet(f)
        df['race_id'] = race_id
        dfs.append(df)
    all_preds = pd.concat(dfs, ignore_index=True)
    print(f"Total rows: {len(all_preds)}; columns: {len(all_preds.columns)}")

    # Resolve patterns to actual column names
    px_cols = find_matching_columns(all_preds.columns, SURVIVING_PHASE_BX_LAYERS)
    pr_cols = find_matching_columns(all_preds.columns, SURVIVING_PRIOR_LAYERS)
    all_l1_cols = px_cols + pr_cols
    missing_px = [p for p, c in zip(SURVIVING_PHASE_BX_LAYERS, px_cols) if c is None]
    missing_pr = [p for p, c in zip(SURVIVING_PRIOR_LAYERS, pr_cols) if c is None]
    found_cols = [c for c in all_l1_cols if c is not None]
    print(f"L1 layers found: {len(found_cols)} / {len(SURVIVING_PHASE_BX_LAYERS) + len(SURVIVING_PRIOR_LAYERS)}")
    if missing_px or missing_pr:
        print(f"  missing Phase B.x patterns: {missing_px}")
        print(f"  missing PRIOR patterns: {missing_pr}")

    # Pull actuals for training window
    with get_db() as conn:
        actuals = pd.DataFrame(execute_query(conn, """
            SELECT res.race_id::text AS race_id,
                   res.horse_id::text AS horse_id,
                   (res.finish_position = 1)::int AS is_winner
            FROM results res JOIN races r USING(race_id)
            WHERE r.race_date BETWEEN '2026-04-25' AND '2026-05-01'
              AND res.finish_position IS NOT NULL
        """))
    print(f"Actuals rows: {len(actuals)}")

    merged = all_preds.merge(actuals, on=['race_id', 'horse_id'], how='inner')
    print(f"Joined rows: {len(merged)}")

    # Construct training matrix with race-level 80/20 split
    X_cols = [c for c in found_cols if c]
    np.random.seed(42)
    race_ids = sorted(merged['race_id'].unique())
    np.random.shuffle(race_ids)
    split_idx = int(len(race_ids) * 0.8)
    train_races = set(race_ids[:split_idx])
    eval_races = set(race_ids[split_idx:])

    train_df = merged[merged['race_id'].isin(train_races)].reset_index(drop=True)
    eval_df = merged[merged['race_id'].isin(eval_races)].reset_index(drop=True)
    X_train = train_df[X_cols].fillna(0.0).values
    y_train = train_df['is_winner'].values.astype(np.float32)
    X_eval = eval_df[X_cols].fillna(0.0).values
    y_eval = eval_df['is_winner'].values.astype(np.float32)
    print(f"  Train: {len(train_races)} races / {len(X_train)} rows / {int(y_train.sum())} winners")
    print(f"  Eval:  {len(eval_races)} races / {len(X_eval)} rows / {int(y_eval.sum())} winners")

    dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=X_cols)
    deval = xgb.DMatrix(X_eval, label=y_eval, feature_names=X_cols)
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'learning_rate': 0.05,
        'max_depth': 3,         # reduced from 4 to dampen overfit on 30 correlated features
        'subsample': 0.7,
        'colsample_bytree': 0.6,
        'min_child_weight': 3,
        'reg_alpha': 0.5,
        'reg_lambda': 2.0,
    }
    print("Training XGBoost ensemble with early-stopping on eval AUC...")
    booster = xgb.train(
        params, dtrain,
        num_boost_round=500,
        evals=[(dtrain, 'train'), (deval, 'eval')],
        early_stopping_rounds=30,
        verbose_eval=50,
    )

    # In/out-of-sample metrics
    preds_train = booster.predict(dtrain)
    preds_eval = booster.predict(deval)
    auc_train = roc_auc_score(y_train, preds_train)
    auc_eval = roc_auc_score(y_eval, preds_eval)
    brier_train = brier_score_loss(y_train, preds_train.clip(0, 1))
    brier_eval = brier_score_loss(y_eval, preds_eval.clip(0, 1))

    train_df['ensemble_pred'] = preds_train
    eval_df['ensemble_pred'] = preds_eval
    top1_train = train_df.loc[train_df.groupby('race_id')['ensemble_pred'].idxmax()]
    top1_eval = eval_df.loc[eval_df.groupby('race_id')['ensemble_pred'].idxmax()]
    top1_train_wr = top1_train['is_winner'].mean()
    top1_eval_wr = top1_eval['is_winner'].mean()
    print()
    print(f"Hybrid ensemble metrics:")
    print(f"  TRAIN  AUC={auc_train:.4f}  Brier={brier_train:.4f}  top1={top1_train_wr*100:.2f}%")
    print(f"  EVAL   AUC={auc_eval:.4f}  Brier={brier_eval:.4f}  top1={top1_eval_wr*100:.2f}%")

    auc = auc_eval  # use eval AUC for downstream gate
    brier = brier_eval
    top1_winrate = top1_eval_wr

    PHASE_BX_BASELINE_AUC = 0.786
    if auc < PHASE_BX_BASELINE_AUC - 0.05:
        raise RuntimeError(f"HALT: hybrid ensemble EVAL AUC {auc:.4f} > 0.05 below baseline {PHASE_BX_BASELINE_AUC}")

    # Save artifact
    artifact_path = '/tmp/option_c_hybrid_ensemble_20260515.json'
    booster.save_model(artifact_path)
    print(f"  Artifact: {artifact_path} ({os.path.getsize(artifact_path):,} bytes)")

    # Upload to S3
    s3 = boto3.client('s3')
    s3_key = 'ensemble/option_c_hybrid_ensemble_20260515.json'
    s3.upload_file(artifact_path, 'equine-model-artifacts', s3_key)
    print(f"  S3: s3://equine-model-artifacts/{s3_key}")

    # Save metadata sidecar
    meta = {
        'version_name': 'option_c_hybrid_ensemble_20260515',
        'l1_inputs': X_cols,
        'training_window': '2026-04-25..2026-05-01',
        'phase_bx_layer_count': sum(1 for c in X_cols if c.startswith('phase_bx__')),
        'prior_layer_count': sum(1 for c in X_cols if c.startswith('prior__')),
        'split': 'race-level 80/20 random (seed=42)',
        'train_auc': float(auc_train),
        'eval_auc': float(auc_eval),
        'train_brier': float(brier_train),
        'eval_brier': float(brier_eval),
        'train_top1_win_rate': float(top1_train_wr),
        'eval_top1_win_rate': float(top1_eval_wr),
        'best_iteration': int(getattr(booster, 'best_iteration', 0) or 0),
        'training_rows': int(len(merged)),
        'training_winners': int(merged['is_winner'].sum()),
    }
    with open('/tmp/option_c_hybrid_ensemble_meta.json', 'w') as f:
        json.dump(meta, f, indent=2)
    s3.upload_file('/tmp/option_c_hybrid_ensemble_meta.json',
                   'equine-model-artifacts',
                   'ensemble/option_c_hybrid_ensemble_20260515_meta.json')

    # Register in model_versions (is_active=FALSE pending Tony Phase 6 ratification)
    insert_uuid = str(uuid.uuid4())
    with get_db() as conn:
        with conn.cursor() as cur:
            # Skip if already inserted (idempotency)
            cur.execute("SELECT model_version_id FROM model_versions WHERE version_name = %s",
                        ('option_c_hybrid_ensemble_20260515',))
            row = cur.fetchone()
            if row:
                new_uuid = row['model_version_id'] if isinstance(row, dict) else row[0]
                print(f"  Already registered model_version_id: {new_uuid} (skipping re-insert)")
            else:
                cur.execute("""
                    INSERT INTO model_versions
                      (model_version_id, model_type, version_name,
                       training_date, training_data_start, training_data_end,
                       s3_artifact_path, is_active, notes)
                    VALUES (%s, %s, %s, NOW(), %s, %s, %s, FALSE, %s)
                    RETURNING model_version_id
                """, (
                    insert_uuid,
                    'ensemble_hybrid_option_c',
                    'option_c_hybrid_ensemble_20260515',
                    '2026-04-25', '2026-05-01',
                    f's3://equine-model-artifacts/{s3_key}',
                    f'Hybrid culled-rebuilt ensemble per Option C; {len(X_cols)} L1 inputs '
                    f'({sum(1 for c in X_cols if c.startswith("phase_bx__"))} Phase B.x + '
                    f'{sum(1 for c in X_cols if c.startswith("prior__"))} PRIOR); '
                    f'eval AUC={auc_eval:.4f}',
                ))
                fetched = cur.fetchone()
                new_uuid = fetched['model_version_id'] if isinstance(fetched, dict) else fetched[0]
                conn.commit()
                print(f"  Registered model_version_id: {new_uuid}")
    print(f"  is_active=FALSE pending Tony Phase 6 ratification")


if __name__ == '__main__':
    main()
