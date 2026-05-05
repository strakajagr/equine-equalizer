"""
Win Rate Model (Path 1) — Two-Layer Training Script

Layer 1 (Core): 58/55 features (excludes workouts). Trained on ALL years.
Layer 2 (Workout Adjustment): core_predicted_prob + 8 workout features.
    Trained ONLY on rows where real workout data exists (2023 + Mar 2026).

For each layer, trains two versions:
  v_base_core / v_base_workout  — odds-blind
  v_odds_core / v_odds_workout  — odds-aware

Run on Fargate (Lambda will timeout for full dataset):
  aws ecs run-task --cluster equine-cluster \
    --task-definition equine-training --launch-type FARGATE
  aws logs tail /ecs/equine-training --follow
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import boto3
import numpy as np
import pandas as pd
import xgboost as xgb

# Allow running from model/ directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.data_loader import build_feature_matrix, _get_conn
from shared.evaluation import full_evaluation
from shared.feature_definitions import (
    get_core_features,
    get_workout_features,
)
from wr.config import (
    XGB_PARAMS, NUM_ROUNDS, EARLY_STOPPING_ROUNDS,
    WORKOUT_XGB_PARAMS, WORKOUT_NUM_ROUNDS, WORKOUT_EARLY_STOPPING_ROUNDS,
    compute_ev_labels,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)
logger = logging.getLogger(__name__)

S3_BUCKET    = 'equine-model-artifacts'
S3_PREFIX    = 'wr'
LOCAL_ARTIFACTS = Path(__file__).parent / 'artifacts'


def predictions_to_probs(predictions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw XGBoost regression scores to calibrated
    probabilities via softmax within each race.
    """
    df = predictions_df.copy()
    df['predicted_prob'] = 0.0
    for rk, group in df.groupby('race_key'):
        scores = group['predicted_score'].values.astype(float)
        shifted = scores - scores.max()
        exp_scores = np.exp(shifted)
        probs = exp_scores / exp_scores.sum()
        df.loc[group.index, 'predicted_prob'] = probs
    return df


def save_artifacts(model: xgb.Booster, feature_names: list[str],
                   eval_results: dict, params: dict, version: str,
                   model_type: str) -> None:
    """Save model + metadata locally and to S3."""
    LOCAL_ARTIFACTS.mkdir(parents=True, exist_ok=True)

    model_file = LOCAL_ARTIFACTS / f'{version}.json'
    imp_file   = LOCAL_ARTIFACTS / f'{version}_importance.json'
    eval_file  = LOCAL_ARTIFACTS / f'{version}_eval.json'
    meta_file  = LOCAL_ARTIFACTS / f'{version}_meta.json'

    model.save_model(str(model_file))

    importance = model.get_score(importance_type='gain')
    imp_file.write_text(json.dumps(importance, indent=2))

    eval_file.write_text(json.dumps(eval_results, indent=2))

    meta = {
        'version':      version,
        'model_type':   model_type,
        'feature_count': len(feature_names),
        'feature_names': feature_names,
        'xgb_params':   params,
        'trained_at':   datetime.utcnow().isoformat(),
    }
    meta_file.write_text(json.dumps(meta, indent=2))

    # Upload to S3
    s3 = boto3.client('s3', region_name='us-east-1')
    for local_path in [model_file, imp_file, eval_file, meta_file]:
        s3_key = f'{S3_PREFIX}/{local_path.name}'
        try:
            s3.upload_file(str(local_path), S3_BUCKET, s3_key)
            logger.info(f'Uploaded s3://{S3_BUCKET}/{s3_key}')
        except Exception as e:
            logger.warning(f'S3 upload failed for {local_path.name}: {e}')


def train_core(features_df: pd.DataFrame, labels_df: pd.DataFrame,
               ev_labels: np.ndarray, feature_names: list[str],
               version_suffix: str) -> tuple[xgb.Booster, dict, np.ndarray]:
    """
    Train Layer 1 (core model) on ALL data. Returns booster, eval_results,
    and predictions on ALL rows (train + val) for Layer 2 input.
    """
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')
    version = f'{version_suffix}_{timestamp}'

    train_mask = labels_df['race_date'].dt.year <= 2024
    val_mask   = labels_df['race_date'].dt.year == 2025

    X_train = features_df.loc[train_mask, feature_names].values.astype(np.float32)
    y_train = ev_labels[train_mask]
    X_val   = features_df.loc[val_mask,   feature_names].values.astype(np.float32)
    y_val   = ev_labels[val_mask]

    logger.info(
        f"[{version_suffix}] train={len(X_train):,} rows  val={len(X_val):,} rows  "
        f"features={len(feature_names)}"
    )

    dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=feature_names)
    dval   = xgb.DMatrix(X_val,   label=y_val,   feature_names=feature_names)

    booster = xgb.train(
        XGB_PARAMS,
        dtrain,
        num_boost_round=NUM_ROUNDS,
        evals=[(dtrain, 'train'), (dval, 'val')],
        early_stopping_rounds=EARLY_STOPPING_ROUNDS,
        verbose_eval=50,
    )
    logger.info(f"[{version_suffix}] best_iteration={booster.best_iteration}")

    # Evaluate on validation set
    raw_val_preds = booster.predict(dval)
    val_labels = labels_df[val_mask].copy().reset_index(drop=True)
    val_labels['predicted_score'] = raw_val_preds
    val_labels = predictions_to_probs(val_labels)
    eval_results = full_evaluation(val_labels, model_name=f'WR {version_suffix}')

    save_artifacts(booster, feature_names, eval_results, XGB_PARAMS, version, version_suffix)

    # Generate predictions on ALL rows for Layer 2 input
    X_all = features_df[feature_names].values.astype(np.float32)
    dall = xgb.DMatrix(X_all, feature_names=feature_names)
    all_preds = booster.predict(dall)

    return booster, eval_results, all_preds


def has_real_workout_data(features_df: pd.DataFrame) -> np.ndarray:
    """
    Boolean mask: True for rows where workout data is real (not defaults).
    Real data = workout_count_30d > 0 OR days_since_last_workout != 30.0.
    """
    wc = features_df['workout_count_30d'].values
    ds = features_df['days_since_last_workout'].values
    return (wc > 0) | (ds != 30.0)


def train_workout_layer(features_df: pd.DataFrame, labels_df: pd.DataFrame,
                        ev_labels: np.ndarray, core_preds: np.ndarray,
                        workout_feature_names: list[str],
                        version_suffix: str) -> tuple[xgb.Booster | None, dict | None]:
    """
    Train Layer 2 (workout adjustment) on ONLY rows with real workout data.
    Features: core_predicted_prob (from Layer 1) + 8 workout features = 9 total.
    """
    # Compute core predicted_prob per race via softmax on core predictions
    temp_df = labels_df.copy()
    temp_df['core_score'] = core_preds
    temp_df['core_predicted_prob'] = 0.0
    for rk, group in temp_df.groupby('race_key'):
        scores = group['core_score'].values.astype(float)
        shifted = scores - scores.max()
        exp_scores = np.exp(shifted)
        probs = exp_scores / exp_scores.sum()
        temp_df.loc[group.index, 'core_predicted_prob'] = probs

    # Filter to rows with real workout data
    workout_mask = has_real_workout_data(features_df)
    n_total = len(features_df)
    n_workout = int(workout_mask.sum())
    logger.info(f"[{version_suffix}] Rows with real workout data: {n_workout:,} / {n_total:,}")

    if n_workout < 100:
        logger.warning(f"[{version_suffix}] Too few workout rows ({n_workout}) — skipping Layer 2")
        return None, None

    # Build Layer 2 feature matrix: core_predicted_prob + 8 workout features
    l2_feature_names = ['core_predicted_prob'] + workout_feature_names
    l2_features = pd.DataFrame({
        'core_predicted_prob': temp_df['core_predicted_prob'].values,
    })
    for wf in workout_feature_names:
        l2_features[wf] = features_df[wf].values

    # Apply workout mask
    l2_features_w = l2_features[workout_mask].reset_index(drop=True)
    ev_labels_w = ev_labels[workout_mask]
    labels_w = labels_df[workout_mask].reset_index(drop=True)

    # Temporal split within workout-available data
    train_mask = labels_w['race_date'].dt.year <= 2024
    val_mask   = labels_w['race_date'].dt.year == 2025

    n_train = int(train_mask.sum())
    n_val = int(val_mask.sum())
    logger.info(
        f"[{version_suffix}] Layer 2 train={n_train:,}  val={n_val:,}  "
        f"features={len(l2_feature_names)}"
    )

    if n_train < 50:
        logger.warning(f"[{version_suffix}] Too few Layer 2 training rows ({n_train}) — skipping")
        return None, None

    X_train = l2_features_w.loc[train_mask, l2_feature_names].values.astype(np.float32)
    y_train = ev_labels_w[train_mask.values]
    X_val   = l2_features_w.loc[val_mask,   l2_feature_names].values.astype(np.float32) if n_val > 0 else None
    y_val   = ev_labels_w[val_mask.values] if n_val > 0 else None

    dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=l2_feature_names)
    evals = [(dtrain, 'train')]
    if X_val is not None and len(X_val) > 0:
        dval = xgb.DMatrix(X_val, label=y_val, feature_names=l2_feature_names)
        evals.append((dval, 'val'))

    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')
    version = f'{version_suffix}_{timestamp}'

    booster = xgb.train(
        WORKOUT_XGB_PARAMS,
        dtrain,
        num_boost_round=WORKOUT_NUM_ROUNDS,
        evals=evals,
        early_stopping_rounds=WORKOUT_EARLY_STOPPING_ROUNDS if len(evals) > 1 else None,
        verbose_eval=50,
    )
    logger.info(f"[{version_suffix}] Layer 2 best_iteration={booster.best_iteration}")

    # Evaluate on val if available
    eval_results = None
    if n_val > 10:
        raw_preds = booster.predict(dval)
        val_labels = labels_w[val_mask].copy().reset_index(drop=True)
        val_labels['predicted_score'] = raw_preds
        val_labels = predictions_to_probs(val_labels)
        eval_results = full_evaluation(val_labels, model_name=f'WR {version_suffix}')
    else:
        logger.info(f"[{version_suffix}] Only {n_val} val rows with workout data — skipping Layer 2 eval")

    save_artifacts(booster, l2_feature_names,
                   eval_results or {'note': f'no val eval — only {n_val} val rows'},
                   WORKOUT_XGB_PARAMS, version, version_suffix)

    return booster, eval_results


def main():
    logger.info("WR Model training starting (two-layer architecture)")
    conn = _get_conn()

    logger.info("Building feature matrix (2022-2025)...")
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2022, end_year=2025, include_odds=True
    )
    conn.close()

    ev_labels = compute_ev_labels(labels_df)
    logger.info(
        f"EV label stats: mean={ev_labels.mean():.3f}  "
        f"winners={int((ev_labels > 0).sum()):,}  "
        f"losers={int((ev_labels < 0).sum()):,}"
    )

    workout_feats = get_workout_features()

    # ── Layer 1: Core models (no workouts) ──────────────────────
    logger.info("=" * 60)
    logger.info("LAYER 1: Core Model (no workout features)")
    logger.info("=" * 60)

    logger.info("=== Training v_base_core (55 features, odds-blind) ===")
    feat_base = get_core_features(include_odds=False)
    _, eval_base, base_all_preds = train_core(
        features_df, labels_df, ev_labels, feat_base, 'v_base_core'
    )

    logger.info("=== Training v_odds_core (58 features, odds-aware) ===")
    feat_odds = get_core_features(include_odds=True)
    _, eval_odds, odds_all_preds = train_core(
        features_df, labels_df, ev_labels, feat_odds, 'v_odds_core'
    )

    # Core model comparison
    print("\n" + "=" * 70)
    print("  Layer 1 Core: v_base_core vs v_odds_core — Validation (2025)")
    print("=" * 70)
    metrics_to_show = [
        'flat_bet_roi', 'kelly_roi', 'top1_win_rate',
        'exacta_hit_rate', 'trifecta_hit_rate', 'value_bet_win_rate',
    ]
    print(f"  {'Metric':<28} {'v_base':>10} {'v_odds':>10}")
    print("-" * 54)
    for m in metrics_to_show:
        b = eval_base.get(m, 0)
        o = eval_odds.get(m, 0)
        if 'roi' in m:
            print(f"  {m:<28} {b:>+10.1%} {o:>+10.1%}")
        else:
            print(f"  {m:<28} {b:>10.3f} {o:>10.3f}")
    print("=" * 70)

    # ── Layer 2: Workout adjustment models ──────────────────────
    logger.info("")
    logger.info("=" * 60)
    logger.info("LAYER 2: Workout Adjustment Model")
    logger.info("=" * 60)

    logger.info("=== Training v_base_workout (9 features) ===")
    base_workout_booster, base_workout_eval = train_workout_layer(
        features_df, labels_df, ev_labels, base_all_preds,
        workout_feats, 'v_base_workout'
    )

    logger.info("=== Training v_odds_workout (9 features) ===")
    odds_workout_booster, odds_workout_eval = train_workout_layer(
        features_df, labels_df, ev_labels, odds_all_preds,
        workout_feats, 'v_odds_workout'
    )

    # Final summary
    print("\n" + "=" * 70)
    print("  TRAINING COMPLETE — Summary")
    print("=" * 70)
    print(f"\n  Layer 1 (Core):")
    print(f"    v_base_core: {len(feat_base)} features, "
          f"top1={eval_base.get('top1_win_rate', 0):.3f}, "
          f"roi={eval_base.get('flat_bet_roi', 0):+.1%}")
    print(f"    v_odds_core: {len(feat_odds)} features, "
          f"top1={eval_odds.get('top1_win_rate', 0):.3f}, "
          f"roi={eval_odds.get('flat_bet_roi', 0):+.1%}")
    print(f"\n  Layer 2 (Workout Adjustment):")
    if base_workout_eval:
        print(f"    v_base_workout: 9 features, "
              f"top1={base_workout_eval.get('top1_win_rate', 0):.3f}, "
              f"roi={base_workout_eval.get('flat_bet_roi', 0):+.1%}")
    else:
        print(f"    v_base_workout: skipped (insufficient val data)")
    if odds_workout_eval:
        print(f"    v_odds_workout: 9 features, "
              f"top1={odds_workout_eval.get('top1_win_rate', 0):.3f}, "
              f"roi={odds_workout_eval.get('flat_bet_roi', 0):+.1%}")
    else:
        print(f"    v_odds_workout: skipped (insufficient val data)")
    print("=" * 70)


if __name__ == '__main__':
    main()
