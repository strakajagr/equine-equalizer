"""
RF Longshot Classifier (Layer 4)
Binary: did this horse WIN at 10-1 or higher?
Two-stage features: 58 core + L1 raw_win_prob + L2 rank_score = 60 total.

Run on Fargate:
  aws ecs run-task --cluster equine-cluster \
    --task-definition equine-training-manual --launch-type FARGATE \
    --overrides '{"containerOverrides":[{"name":"training","command":["model/longshot/train.py"]}]}'
"""

import json
import logging
import pickle
import sys
from datetime import datetime
from pathlib import Path

import boto3
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    classification_report
)

sys.path.insert(0, str(Path(__file__).parent.parent))
# REPAIR-5-FINAL: feature_contract import — same fix pattern as ensemble.
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'backend'))

from shared.data_loader import build_feature_matrix, _get_conn
from shared.feature_definitions import get_core_features
from longshot.config import RF_PARAMS, LONGSHOT_ODDS_THRESHOLD, compute_longshot_labels
try:
    from services.feature_contract import predict_with_contract, get_model_features
except Exception:
    predict_with_contract = None
    get_model_features = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

S3_BUCKET = 'equine-model-artifacts'
S3_PREFIX = 'longshot'
LOCAL_ARTIFACTS = Path(__file__).parent / 'artifacts'


def load_base_model(model_type_list, local_dir):
    """Load a trained XGBoost model from S3 for generating base layer predictions."""
    conn = _get_conn()
    import os
    try:
        with conn.cursor() as cur:
            for mt in model_type_list:
                cur.execute(
                    "SELECT s3_artifact_path FROM model_versions "
                    "WHERE model_type = %s AND is_active = true LIMIT 1",
                    (mt,))
                row = cur.fetchone()
                if row:
                    s3_path = row['s3_artifact_path'] if isinstance(row, dict) else row[0]
                    if not s3_path or not s3_path.startswith('s3://'):
                        continue
                    parts = s3_path[5:].split('/', 1)
                    bucket, key = parts[0], parts[1]
                    os.makedirs(local_dir, exist_ok=True)
                    local_file = f"{local_dir}/model.json"
                    s3 = boto3.client('s3', region_name='us-east-1')
                    s3.download_file(bucket, key, local_file)
                    model = xgb.Booster()
                    model.load_model(local_file)
                    logger.info(f"Loaded base model: {mt} from {s3_path}")
                    return model
    finally:
        conn.close()
    return None


def main():
    logger.info("RF Longshot Classifier (Layer 4) training starting")
    conn = _get_conn()

    logger.info("Building feature matrix (2022-2026)...")
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2022, end_year=2026, include_odds=True
    )
    conn.close()

    core_features = get_core_features(include_odds=True)  # 58

    # Generate Layer 1 + Layer 2 predictions on ALL rows
    logger.info("Loading base models for two-stage features...")
    wp_model = load_base_model(['win_prob_odds', 'win_prob_core'], '/tmp/wp-base')
    rk_model = load_base_model(['ranker_core'], '/tmp/rk-base')

    # REPAIR-5-FINAL: feature_contract — same fix as ensemble trainer.
    # L1 boosters retrained 2026-05-20 carry 63 features (Phase B Top-5
    # added); old hardcoded 58-feature DMatrix crashed predict() with
    # ValueError: feature_names mismatch. Read booster's feature_names
    # and pad features_df with missing columns at 0.0.
    def _l1_predict(model, label, default):
        if not model:
            logger.warning(f"No {label} model — using default {default}")
            return default
        if predict_with_contract is None:
            X_core = features_df[core_features].fillna(0.0).values.astype(np.float32)
            dm = xgb.DMatrix(X_core, feature_names=core_features)
            return model.predict(dm)
        needed = get_model_features(model)
        for col in needed:
            if col not in features_df.columns:
                features_df[col] = 0.0
        return predict_with_contract(model, features_df)

    features_df['l1_win_prob'] = _l1_predict(wp_model, 'Layer 1', 0.12)
    if wp_model:
        logger.info(f"Layer 1 predictions: mean={features_df['l1_win_prob'].mean():.4f}")

    features_df['l2_rank_score'] = _l1_predict(rk_model, 'Layer 2', 0.0)
    if rk_model:
        logger.info(f"Layer 2 predictions: mean={features_df['l2_rank_score'].mean():.4f}")

    # Build 60-feature matrix
    rf_features = core_features + ['l1_win_prob', 'l2_rank_score']
    logger.info(f"RF features: {len(rf_features)}")

    # Filter to horses with odds >= 3.0 (exclude heavy favorites)
    has_odds = labels_df['closing_odds'] >= 3.0
    feat_filtered = features_df[has_odds].reset_index(drop=True)
    labels_filtered = labels_df[has_odds].reset_index(drop=True)

    longshot_labels = compute_longshot_labels(labels_filtered)
    n_pos = int(longshot_labels.sum())
    n_neg = int((longshot_labels == 0).sum())
    logger.info(f"Longshot labels: {n_pos:,} positive (10-1+ winners), {n_neg:,} negative")

    # Temporal split
    train_mask = labels_filtered['race_date'] <= pd.Timestamp('2026-04-24')
    val_mask = (labels_filtered['race_date'] >= pd.Timestamp('2026-04-25')) & (labels_filtered['race_date'] <= pd.Timestamp('2026-05-01'))

    X_train = feat_filtered.loc[train_mask, rf_features].fillna(0.0).values
    y_train = longshot_labels[train_mask.values]
    X_val = feat_filtered.loc[val_mask, rf_features].fillna(0.0).values
    y_val = longshot_labels[val_mask.values]

    logger.info(f"Train: {len(X_train):,} rows ({int(y_train.sum()):,} pos)  "
                f"Val: {len(X_val):,} rows ({int(y_val.sum()):,} pos)")

    # Train RF
    logger.info("Training Random Forest...")
    rf = RandomForestClassifier(**RF_PARAMS)
    rf.fit(X_train, y_train)

    # Evaluate
    y_pred = rf.predict(X_val)
    y_prob = rf.predict_proba(X_val)[:, 1]

    prec = precision_score(y_val, y_pred, zero_division=0)
    rec = recall_score(y_val, y_pred, zero_division=0)
    f1 = f1_score(y_val, y_pred, zero_division=0)
    auc = roc_auc_score(y_val, y_prob) if y_val.sum() > 0 else 0.0

    # Longshot ROI: flat $2 bet on every horse with P(longshot_win) > 0.5
    flagged = y_prob > 0.5
    n_bets = int(flagged.sum())
    if n_bets > 0:
        wagered = n_bets * 2.0
        # For winners, estimate payout from closing_odds
        val_odds = labels_filtered.loc[val_mask, 'closing_odds'].values
        val_payouts = labels_filtered.loc[val_mask, 'win_payout'].values
        returned = sum(
            float(val_payouts[i]) if val_payouts[i] and val_payouts[i] > 0 else (float(val_odds[i]) + 1) * 2
            for i in range(len(y_val))
            if flagged[i] and y_val[i] == 1
        )
        longshot_roi = (returned - wagered) / wagered if wagered > 0 else 0
    else:
        longshot_roi = 0.0

    logger.info("=" * 56)
    logger.info("  RF Longshot Classifier — Evaluation")
    logger.info("=" * 56)
    logger.info(f"  precision:     {prec:.3f}")
    logger.info(f"  recall:        {rec:.3f}")
    logger.info(f"  f1_score:      {f1:.3f}")
    logger.info(f"  roc_auc:       {auc:.3f}")
    logger.info(f"  bets_flagged:  {n_bets}")
    logger.info(f"  longshot_roi:  {longshot_roi:+.1%}")
    logger.info("=" * 56)

    print("\n" + "=" * 56)
    print("  RF Longshot — Evaluation")
    print("=" * 56)
    print(f"  precision:     {prec:.3f}")
    print(f"  recall:        {rec:.3f}")
    print(f"  f1_score:      {f1:.3f}")
    print(f"  roc_auc:       {auc:.3f}")
    print(f"  bets_flagged:  {n_bets}")
    print(f"  longshot_roi:  {longshot_roi:+.1%}")
    print("=" * 56)

    # Feature importance
    importances = dict(zip(rf_features, rf.feature_importances_))
    top10 = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:10]
    logger.info("Top 10 features:")
    for feat, imp in top10:
        logger.info(f"  {feat:30s} {imp:.4f}")

    # Save artifacts
    LOCAL_ARTIFACTS.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')
    version = f'longshot_rf_{timestamp}'

    model_file = LOCAL_ARTIFACTS / f'{version}.pkl'
    with open(model_file, 'wb') as f:
        pickle.dump(rf, f)

    meta = {
        'version': version, 'model_type': 'longshot_rf',
        'feature_count': len(rf_features), 'feature_names': rf_features,
        'rf_params': RF_PARAMS,
        'metrics': {'precision': prec, 'recall': rec, 'f1': f1, 'auc': auc,
                    'longshot_roi': longshot_roi, 'bets_flagged': n_bets},
        'top_features': dict(top10),
        'trained_at': datetime.utcnow().isoformat(),
    }
    meta_file = LOCAL_ARTIFACTS / f'{version}_meta.json'
    meta_file.write_text(json.dumps(meta, indent=2))

    s3 = boto3.client('s3', region_name='us-east-1')
    for lp in [model_file, meta_file]:
        s3_key = f'{S3_PREFIX}/{lp.name}'
        try:
            s3.upload_file(str(lp), S3_BUCKET, s3_key)
            logger.info(f'Uploaded s3://{S3_BUCKET}/{s3_key}')
        except Exception as e:
            logger.warning(f'S3 upload failed: {e}')

    # § 4.33: register in model_versions post-S3-upload
    try:
        from training.registration import register_trained_artifact
        register_trained_artifact(
            version_name=version,
            model_type='longshot_rf',
            s3_artifact_path=f's3://{S3_BUCKET}/{S3_PREFIX}/{model_file.name}',
            training_metadata={
                'feature_names': rf_features,
                'hyperparameters': RF_PARAMS,
                'flat_bet_roi': longshot_roi,
                'longshot_precision': prec,
                'longshot_recall': rec,
                'longshot_f1': f1,
                'longshot_auc': auc,
                'longshot_bets_flagged': n_bets,
                'notes': (
                    f'longshot RF training; '
                    f'precision={prec:.3f} recall={rec:.3f} '
                    f'roi={longshot_roi:+.1%} bets={n_bets}'
                ),
            },
        )
    except Exception as e:
        logger.warning(f'model_versions registration failed for {version}: {e}')

    logger.info(f"RF Longshot training complete: {version}")


if __name__ == '__main__':
    main()
