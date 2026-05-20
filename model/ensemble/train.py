"""
Stacking Ensemble (Layer 7) — PRIMARY prediction model.
Combines all layer outputs via logistic regression.
CRITICAL: Trained on 2025 held-out data ONLY (out-of-fold for base models).

Run on Fargate:
  aws ecs run-task --cluster equine-cluster \
    --task-definition equine-training-manual --launch-type FARGATE \
    --overrides '{"containerOverrides":[{"name":"training","command":["model/ensemble/train.py"]}]}'
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
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

sys.path.insert(0, str(Path(__file__).parent.parent))
# REPAIR-5-FINAL: import feature_contract for trainer-side use. Same
# fix pattern feature_contract solved in inference: read booster's own
# feature_names to select features, instead of hardcoded lists that
# mismatch when L1 boosters get retrained on a different feature set.
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'backend'))

from shared.data_loader import build_feature_matrix, _get_conn
from shared.feature_definitions import get_core_features
from shared.evaluation import full_evaluation
from ensemble.config import ENSEMBLE_FEATURES
try:
    from services.feature_contract import predict_with_contract, get_model_features
except Exception:
    # Fallback for environments where backend/ isn't co-located. In ECS
    # production the image has backend/ COPY'd to /app/ so this works.
    predict_with_contract = None
    get_model_features = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

S3_BUCKET = 'equine-model-artifacts'
S3_PREFIX = 'ensemble'
LOCAL_ARTIFACTS = Path(__file__).parent / 'artifacts'


def load_xgb_model(model_type_list, local_dir):
    """Load trained XGBoost model from S3."""
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
                    os.makedirs(local_dir, exist_ok=True)
                    local_file = f"{local_dir}/model.json"
                    s3 = boto3.client('s3', region_name='us-east-1')
                    s3.download_file(parts[0], parts[1], local_file)
                    model = xgb.Booster()
                    model.load_model(local_file)
                    return model
    finally:
        conn.close()
    return None


def load_rf_model(local_dir):
    """Load RF longshot model from S3."""
    conn = _get_conn()
    import os
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT s3_artifact_path FROM model_versions "
                "WHERE model_type = 'longshot_rf' AND is_active = true LIMIT 1")
            row = cur.fetchone()
            if not row:
                return None
            s3_path = row['s3_artifact_path'] if isinstance(row, dict) else row[0]
            if not s3_path or not s3_path.startswith('s3://'):
                return None
            parts = s3_path[5:].split('/', 1)
            os.makedirs(local_dir, exist_ok=True)
            local_file = f"{local_dir}/model.pkl"
            s3 = boto3.client('s3', region_name='us-east-1')
            s3.download_file(parts[0], parts[1], local_file)
            with open(local_file, 'rb') as f:
                return pickle.load(f)
    finally:
        conn.close()


def main():
    logger.info("Stacking Ensemble (Layer 7) training starting")
    logger.info("CRITICAL: Training on 2025 held-out data ONLY")

    conn = _get_conn()
    logger.info("Building feature matrix (2022-2026)...")
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2022, end_year=2026, include_odds=True
    )
    conn.close()

    core_features = get_core_features(include_odds=True)

    # Generate Layer 1 + Layer 2 predictions on ALL rows
    logger.info("Loading base models...")
    wp_model = load_xgb_model(['win_prob_odds', 'win_prob_core'], '/tmp/ens-wp')
    rk_model = load_xgb_model(['ranker_core'], '/tmp/ens-rk')
    rf_model = load_rf_model('/tmp/ens-rf')

    # REPAIR-5-FINAL: select features per BOOSTER's feature_names (not a
    # hardcoded 58-feature core list). The L1 boosters retrained on
    # 2026-05-20 carry 63 features (Phase B Top-5 added); the old build
    # with a 58-feature core list crashed predict() with
    #   ValueError: feature_names mismatch.
    # Pad features_df with any feature the booster needs but FE hasn't
    # emitted, then let predict_with_contract slice in the right order.
    def _l1_predict(model, label):
        if not model:
            logger.warning(f"No {label} model — using default")
            return None
        if predict_with_contract is None:
            # Legacy fallback (will fail on feature_names mismatch like before;
            # surfaces the same way the bug originally did).
            X_core = features_df[core_features].fillna(0.0).values.astype(np.float32)
            dm = xgb.DMatrix(X_core, feature_names=core_features)
            return model.predict(dm)
        needed = get_model_features(model)
        for col in needed:
            if col not in features_df.columns:
                features_df[col] = 0.0
        return predict_with_contract(model, features_df)

    # Layer 1: win probability
    wp_preds = _l1_predict(wp_model, 'L1 win_prob')
    features_df['win_prob'] = wp_preds if wp_preds is not None else 0.12

    # Layer 2: rank score
    rk_preds = _l1_predict(rk_model, 'L2 ranker')
    features_df['rank_score'] = rk_preds if rk_preds is not None else 0.0

    # Layer 4: RF longshot probability
    if rf_model:
        rf_features = core_features + ['win_prob', 'rank_score']
        # Ensure l1_win_prob and l2_rank_score columns exist for RF
        features_df['l1_win_prob'] = features_df['win_prob']
        features_df['l2_rank_score'] = features_df['rank_score']
        X_rf = features_df[core_features + ['l1_win_prob', 'l2_rank_score']].fillna(0.0).values
        features_df['longshot_prob'] = rf_model.predict_proba(X_rf)[:, 1]
    else:
        features_df['longshot_prob'] = 0.0
        logger.warning("No L4 RF model — using default")

    # Layer 5: trajectory (default for ensemble training — LSTM runs separately)
    features_df['trajectory_score'] = 0.0
    logger.info("Trajectory scores defaulted to 0.0 (LSTM scored separately)")

    # Layer 6: angle EV + posterior (default — computed at inference time)
    features_df['angle_ev'] = 0.0
    features_df['angle_posterior'] = 0.0
    logger.info("Angle scores defaulted to 0.0 (computed at inference)")

    # Add race context features
    features_df['morning_line_odds'] = labels_df['closing_odds'].values  # proxy
    features_df['race_quality_tier'] = features_df.get('race_quality_tier',
        pd.Series(2.0, index=features_df.index))
    if 'field_size' not in features_df.columns:
        features_df['field_size'] = labels_df['field_size'].values

    # Phase B.x: ensemble stacker trained on 2026 substrate prior to Derby (2026-05-02 excluded)
    val_mask = (labels_df['race_date'] >= pd.Timestamp('2026-01-01')) & (labels_df['race_date'] <= pd.Timestamp('2026-05-01'))
    X_2025 = features_df[val_mask].copy().reset_index(drop=True)
    y_2025 = (labels_df[val_mask]['finish_position'] == 1).astype(float).values

    # Ensure all ensemble features exist
    for col in ENSEMBLE_FEATURES:
        if col not in X_2025.columns:
            X_2025[col] = 0.0

    X_ensemble = X_2025[ENSEMBLE_FEATURES].fillna(0.0).values
    logger.info(f"Ensemble training: {len(X_ensemble):,} rows (2025 only), "
                f"{int(y_2025.sum()):,} winners")

    # Split 2025: first 80% train, last 20% eval
    split_idx = int(len(X_ensemble) * 0.8)
    X_train, X_eval = X_ensemble[:split_idx], X_ensemble[split_idx:]
    y_train, y_eval = y_2025[:split_idx], y_2025[split_idx:]

    logger.info(f"Ensemble split: train={len(X_train):,}  eval={len(X_eval):,}")

    # Train logistic regression
    ensemble = LogisticRegression(
        C=1.0, class_weight='balanced', max_iter=1000, random_state=42
    )
    ensemble.fit(X_train, y_train)

    # Evaluate
    y_pred_prob = ensemble.predict_proba(X_eval)[:, 1]
    y_pred = ensemble.predict(X_eval)
    acc = accuracy_score(y_eval, y_pred)
    auc = roc_auc_score(y_eval, y_pred_prob) if y_eval.sum() > 0 else 0.0

    # Evaluate as predictions (top1_win_rate etc)
    eval_labels = labels_df[val_mask].copy().reset_index(drop=True).iloc[split_idx:]
    eval_labels['predicted_score'] = y_pred_prob
    eval_labels['raw_win_prob'] = y_pred_prob
    eval_labels['predicted_prob'] = y_pred_prob
    # Normalize within race
    eval_labels['win_probability'] = 0.0
    for rk, group in eval_labels.groupby('race_key'):
        raw = group['predicted_score'].values
        total = raw.sum()
        if total > 0:
            eval_labels.loc[group.index, 'win_probability'] = raw / total
        else:
            eval_labels.loc[group.index, 'win_probability'] = 1.0 / len(raw)
    eval_labels['predicted_prob'] = eval_labels['win_probability']

    eval_results = full_evaluation(eval_labels, model_name='Ensemble L7')

    # Feature weights
    weights = dict(zip(ENSEMBLE_FEATURES, ensemble.coef_[0]))
    sorted_weights = sorted(weights.items(), key=lambda x: abs(x[1]), reverse=True)

    logger.info("=" * 56)
    logger.info("  Stacking Ensemble — Evaluation")
    logger.info("=" * 56)
    logger.info(f"  accuracy:      {acc:.3f}")
    logger.info(f"  roc_auc:       {auc:.3f}")
    logger.info(f"  top1_win_rate: {eval_results.get('top1_win_rate', 0):.3f}")
    logger.info(f"  Feature weights:")
    for feat, w in sorted_weights:
        logger.info(f"    {feat:25s} {w:+.4f}")
    logger.info("=" * 56)

    print("\n" + "=" * 56)
    print("  Stacking Ensemble — Evaluation")
    print("=" * 56)
    print(f"  accuracy:      {acc:.3f}")
    print(f"  roc_auc:       {auc:.3f}")
    print(f"  top1_win_rate: {eval_results.get('top1_win_rate', 0):.3f}")
    print(f"  Feature weights:")
    for feat, w in sorted_weights:
        print(f"    {feat:25s} {w:+.4f}")
    print("=" * 56)

    # Save
    LOCAL_ARTIFACTS.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')
    version = f'ensemble_{timestamp}'

    model_file = LOCAL_ARTIFACTS / f'{version}.pkl'
    with open(model_file, 'wb') as f:
        pickle.dump(ensemble, f)

    meta = {
        'version': version, 'model_type': 'ensemble',
        'features': ENSEMBLE_FEATURES,
        'weights': weights,
        'metrics': {'accuracy': acc, 'roc_auc': auc,
                    'top1_win_rate': eval_results.get('top1_win_rate', 0)},
        'eval_results': eval_results,
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
            model_type='ensemble',
            s3_artifact_path=f's3://{S3_BUCKET}/{S3_PREFIX}/{model_file.name}',
            training_metadata={
                'feature_names': ENSEMBLE_FEATURES,
                'hyperparameters': {'weights': weights},
                'top1_accuracy': eval_results.get('top1_win_rate'),
                'exacta_hit_rate': eval_results.get('exacta_hit_rate'),
                'trifecta_hit_rate': eval_results.get('trifecta_hit_rate'),
                'flat_bet_roi': eval_results.get('flat_bet_roi'),
                'kelly_roi': eval_results.get('kelly_roi'),
                'ensemble_accuracy': acc,
                'ensemble_roc_auc': auc,
                'notes': (
                    f'ensemble training; accuracy={acc:.3f} '
                    f'auc={auc:.3f}'
                ),
            },
        )
    except Exception as e:
        logger.warning(f'model_versions registration failed for {version}: {e}')

    logger.info(f"Ensemble training complete: {version}")


if __name__ == '__main__':
    main()
