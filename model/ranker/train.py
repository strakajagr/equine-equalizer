"""
Finish Position Ranker (Layer 2) — Training Script

Objective: rank:pairwise (LambdaMART)
Labels: inverted finish position (1st=highest)
Two models: ranker_core (58 feat, all data) and ranker_full (66 feat, workout data only)

Run on Fargate:
  aws ecs run-task --cluster equine-cluster \
    --task-definition equine-training-manual --launch-type FARGATE \
    --overrides '{"containerOverrides":[{"name":"training","command":["model/ranker/train.py"]}]}'
  aws logs tail /ecs/equine-training --follow
"""

import argparse
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

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.data_loader import build_feature_matrix, _get_conn
from shared.evaluation import full_evaluation
from shared.feature_definitions import (
    get_core_features,
    get_odds_aware_features,
    get_ranker_full_features,
    get_lean53_features,
    get_gonzo_sauce_features,
    RANKER_FULL_CULL,
)
from shared.specialists import (
    validate as validate_specialist,
    get_pp_filter,
    compute_sample_weights,
    artifact_suffix,
    CRITERION_DESCRIPTIONS,
    VALID_SPECIALISTS,
    WEIGHT_SPECIALISTS,
)
from ranker.config import XGB_PARAMS, NUM_ROUNDS, EARLY_STOPPING_ROUNDS, compute_rank_labels

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)
logger = logging.getLogger(__name__)

S3_BUCKET      = 'equine-model-artifacts'
S3_PREFIX      = 'ranker'
LOCAL_ARTIFACTS = Path(__file__).parent / 'artifacts'


def save_artifacts(model: xgb.Booster, feature_names: list[str],
                   eval_results: dict, params: dict, version: str,
                   model_type: str, specialist: str = 'general') -> None:
    """Save model + metadata locally and to S3."""
    LOCAL_ARTIFACTS.mkdir(parents=True, exist_ok=True)

    model_file = LOCAL_ARTIFACTS / f'{version}.json'
    imp_file   = LOCAL_ARTIFACTS / f'{version}_importance.json'
    eval_file  = LOCAL_ARTIFACTS / f'{version}_eval.json'
    meta_file  = LOCAL_ARTIFACTS / f'{version}_meta.json'

    model.save_model(str(model_file))
    imp_file.write_text(json.dumps(model.get_score(importance_type='gain'), indent=2))
    eval_file.write_text(json.dumps(eval_results, indent=2))

    meta = {
        'version':      version,
        'model_type':   model_type,
        'specialist':   specialist,
        'criterion':    CRITERION_DESCRIPTIONS.get(specialist, ''),
        'label_type':   'rank_inverted',
        'objective':    'rank:pairwise',
        'feature_count': len(feature_names),
        'feature_names': feature_names,
        'xgb_params':   {k: v for k, v in params.items() if not callable(v)},
        'trained_at':   datetime.utcnow().isoformat(),
    }
    meta_file.write_text(json.dumps(meta, indent=2))

    s3 = boto3.client('s3', region_name='us-east-1')
    for local_path in [model_file, imp_file, eval_file, meta_file]:
        s3_key = f'{S3_PREFIX}/{local_path.name}'
        try:
            s3.upload_file(str(local_path), S3_BUCKET, s3_key)
            logger.info(f'Uploaded s3://{S3_BUCKET}/{s3_key}')
        except Exception as e:
            logger.warning(f'S3 upload failed for {local_path.name}: {e}')


def train_ranker(features_df: pd.DataFrame, labels_df: pd.DataFrame,
                 rank_labels: np.ndarray, feature_names: list[str],
                 version_suffix: str,
                 sample_weight: np.ndarray = None,
                 specialist: str = 'general') -> tuple[xgb.Booster, dict]:
    """
    Train a ranker model with rank:pairwise.
    Handles group construction for XGBoost ranking.
    """
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')
    version = f'{version_suffix}_{timestamp}'

    # Sort everything by race_key (required for group construction)
    sort_idx = labels_df.sort_values('race_key').index
    features_sorted = features_df.loc[sort_idx].reset_index(drop=True)
    labels_sorted = labels_df.loc[sort_idx].reset_index(drop=True)
    rank_labels_sorted = rank_labels[sort_idx.values]
    if sample_weight is not None:
        sample_weight_sorted = sample_weight[sort_idx.values]
    else:
        sample_weight_sorted = None

    # Temporal split
    train_mask = labels_sorted['race_date'].dt.year <= 2024
    val_mask   = labels_sorted['race_date'].dt.year == 2025

    X_train = features_sorted.loc[train_mask, feature_names].values.astype(np.float32)
    y_train = rank_labels_sorted[train_mask.values]
    X_val   = features_sorted.loc[val_mask,   feature_names].values.astype(np.float32)
    y_val   = rank_labels_sorted[val_mask.values]

    if sample_weight_sorted is not None:
        sw_train = sample_weight_sorted[train_mask.values]
        sw_val   = sample_weight_sorted[val_mask.values]
        logger.info(
            f"[{version_suffix}] sample_weight: train mean={sw_train.mean():.3f} "
            f"max={sw_train.max():.1f} (n_weighted={int((sw_train>1).sum()):,})"
        )
    else:
        sw_train = sw_val = None

    # Build group sizes for train and val
    train_groups = labels_sorted[train_mask].groupby(
        'race_key', sort=False
    ).size().values
    val_groups = labels_sorted[val_mask].groupby(
        'race_key', sort=False
    ).size().values

    assert train_groups.sum() == len(X_train), (
        f"Train groups sum {train_groups.sum()} != rows {len(X_train)}"
    )
    assert val_groups.sum() == len(X_val), (
        f"Val groups sum {val_groups.sum()} != rows {len(X_val)}"
    )

    logger.info(
        f"[{version_suffix}] train={len(X_train):,} rows ({len(train_groups):,} races)  "
        f"val={len(X_val):,} rows ({len(val_groups):,} races)  "
        f"features={len(feature_names)}"
    )

    # rank:pairwise expects ONE weight per query group (race), not per
    # row. Specialist criteria are race-level — all rows in a race
    # share the same sample-weight value by construction — so first()
    # per group is the correct aggregation. mean() would also work;
    # sum() would scale by field size and is wrong.
    def _per_group_weight(sw, lab):
        if sw is None:
            return None
        tmp = lab.copy()
        tmp["__sw"] = sw
        return tmp.groupby("race_key", sort=False)["__sw"].first().values.astype(np.float32)

    sw_train_grp = _per_group_weight(sw_train, labels_sorted[train_mask])
    sw_val_grp   = _per_group_weight(sw_val,   labels_sorted[val_mask])

    if sw_train_grp is not None:
        assert len(sw_train_grp) == len(train_groups), (
            f"per-group weight count {len(sw_train_grp)} != "
            f"train_groups {len(train_groups)}"
        )
    if sw_val_grp is not None:
        assert len(sw_val_grp) == len(val_groups), (
            f"per-group weight count {len(sw_val_grp)} != "
            f"val_groups {len(val_groups)}"
        )

    dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=feature_names, weight=sw_train_grp)
    dtrain.set_group(train_groups)
    dval = xgb.DMatrix(X_val, label=y_val, feature_names=feature_names, weight=sw_val_grp)
    dval.set_group(val_groups)

    booster = xgb.train(
        XGB_PARAMS,
        dtrain,
        num_boost_round=NUM_ROUNDS,
        evals=[(dtrain, 'train'), (dval, 'val')],
        early_stopping_rounds=EARLY_STOPPING_ROUNDS,
        verbose_eval=50,
    )
    logger.info(f"[{version_suffix}] best_iteration={booster.best_iteration}")

    # Evaluate: use ranker scores as predicted_score for evaluation
    rank_preds = booster.predict(dval)
    val_labels = labels_sorted[val_mask].copy().reset_index(drop=True)
    val_labels['predicted_score'] = rank_preds
    # Normalize to probabilities within race (for evaluation compatibility)
    val_labels['raw_win_prob'] = 0.0
    val_labels['win_probability'] = 0.0
    val_labels['predicted_prob'] = 0.0
    for rk, group in val_labels.groupby('race_key'):
        scores = group['predicted_score'].values.astype(float)
        shifted = scores - scores.max()
        exp_scores = np.exp(shifted)
        probs = exp_scores / exp_scores.sum()
        val_labels.loc[group.index, 'raw_win_prob'] = probs
        val_labels.loc[group.index, 'win_probability'] = probs
        val_labels.loc[group.index, 'predicted_prob'] = probs

    eval_results = full_evaluation(val_labels, model_name=f'Ranker {version_suffix}')

    save_artifacts(booster, feature_names, eval_results, XGB_PARAMS, version,
                   version_suffix, specialist=specialist)

    return booster, eval_results


def train_full_model_only(specialist: str = 'general'):
    """
    Entry point for daily retrain of ONLY ranker_full.
    Skips core training.

    specialist: one of VALID_SPECIALISTS. 'general' is byte-identical to
        the legacy daily retrain. Other values produce specialist-tagged
        artifacts (e.g., rk_full_speed_<ts>.json) for the gallery.
    """
    specialist = validate_specialist(specialist)
    logger.info(f"Ranker FULL model daily retrain starting (specialist={specialist})")
    conn = _get_conn()

    logger.info("Building feature matrix (2022-2025)...")
    pps_filter = get_pp_filter(specialist)
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2022, end_year=2025, include_odds=True,
        pps_filter=pps_filter,
    )

    pps_df_for_weight = None
    if specialist in ('speed', 'closer', 'class_riser', 'class_dropper'):
        from shared.data_loader import _load_raw_pps
        pps_df_for_weight = _load_raw_pps(conn, 2022, 2025)
    conn.close()

    rank_labels = compute_rank_labels(labels_df)
    lean_tag = os.environ.get("LEAN_TAG", "").strip()
    if specialist == 'gonzo_sauce':
        # Phase A3: lean53 base (53) + 14 Gonzo Sauce features = 67 features.
        full_features = get_gonzo_sauce_features()
        logger.info(
            f"rk_full feature set: {len(full_features)} features "
            f"(specialist=gonzo_sauce, lean53 + 14 Phase A3)"
        )
    elif lean_tag == "lean53":
        full_features = get_lean53_features()
        logger.info(f"rk_full feature set: {len(full_features)} (lean53)")
    else:
        full_features = get_ranker_full_features()
        logger.info(f"rk_full feature set: {len(full_features)} (66 base − {len(RANKER_FULL_CULL)} culled)")

    # Filter to workout data
    has_workouts = (
        (features_df['workout_count_30d'] > 0) |
        (features_df['days_since_last_workout'] != 30.0)
    )
    feat_wk = features_df[has_workouts].reset_index(drop=True)
    labels_wk = labels_df[has_workouts].reset_index(drop=True)
    rank_wk = rank_labels[has_workouts.values]

    logger.info(f"Ranker full: {len(feat_wk):,} rows with workout data")

    if len(feat_wk) < 100:
        logger.warning("Too few workout rows for ranker_full — skipping")
        return

    sw = None
    if specialist in WEIGHT_SPECIALISTS:
        # Filter specialists (sprint, route) get pre-filtered data, no
        # upweighting on top. General gets nothing. Only WEIGHT
        # specialists receive sample_weight.
        sw = compute_sample_weights(feat_wk, labels_wk, pps_df_for_weight, specialist)

    suffix = artifact_suffix('rk_full', specialist)
    train_ranker(feat_wk, labels_wk, rank_wk, full_features, suffix,
                 sample_weight=sw, specialist=specialist)
    logger.info("Ranker FULL model daily retrain complete")


def main():
    logger.info("Finish Position Ranker (Layer 2) training starting — rank:pairwise")
    conn = _get_conn()

    logger.info("Building feature matrix (2022-2025)...")
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2022, end_year=2025, include_odds=True
    )
    conn.close()

    rank_labels = compute_rank_labels(labels_df)
    n_labeled = int((rank_labels > 0).sum())
    logger.info(f"Rank labels: {n_labeled:,} labeled rows (of {len(rank_labels):,})")

    # ── Core model (58 features, all data) ────────────
    logger.info("=" * 60)
    logger.info("RANKER CORE (58 features, all data)")
    logger.info("=" * 60)

    core_features = get_core_features(include_odds=True)
    _, eval_core = train_ranker(
        features_df, labels_df, rank_labels, core_features, 'rk_core'
    )

    # ── Full model (66 features, workout data only) ───
    logger.info("")
    logger.info("=" * 60)
    logger.info("RANKER FULL (66 features, workout data only)")
    logger.info("=" * 60)

    lean_tag = os.environ.get("LEAN_TAG", "").strip()
    if lean_tag == "lean53":
        full_features = get_lean53_features()
        logger.info(f"rk_full feature set: {len(full_features)} (lean53)")
    else:
        full_features = get_ranker_full_features()
        logger.info(f"rk_full feature set: {len(full_features)} (66 base − {len(RANKER_FULL_CULL)} culled)")
    has_workouts = (
        (features_df['workout_count_30d'] > 0) |
        (features_df['days_since_last_workout'] != 30.0)
    )
    feat_wk = features_df[has_workouts].reset_index(drop=True)
    labels_wk = labels_df[has_workouts].reset_index(drop=True)
    rank_wk = rank_labels[has_workouts.values]

    n_wk = len(feat_wk)
    logger.info(f"Full model: {n_wk:,} rows with workout data")

    eval_full = None
    if n_wk >= 100:
        _, eval_full = train_ranker(
            feat_wk, labels_wk, rank_wk, full_features, 'rk_full'
        )
    else:
        logger.warning(f"Too few workout rows ({n_wk}) — skipping full model")

    # Summary
    print("\n" + "=" * 70)
    print("  RANKER TRAINING COMPLETE — Summary")
    print("=" * 70)
    print(f"\n  Core: {len(core_features)} features, "
          f"top1={eval_core.get('top1_win_rate', 0):.3f}, "
          f"exacta={eval_core.get('exacta_hit_rate', 0):.3f}, "
          f"trifecta={eval_core.get('trifecta_hit_rate', 0):.3f}")
    if eval_full:
        print(f"  Full: {len(full_features)} features, "
              f"top1={eval_full.get('top1_win_rate', 0):.3f}, "
              f"exacta={eval_full.get('exacta_hit_rate', 0):.3f}, "
              f"trifecta={eval_full.get('trifecta_hit_rate', 0):.3f}")
    else:
        print(f"  Full: skipped (insufficient workout data)")
    print("=" * 70)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Ranker training. Default: full bootstrap (core + full)."
    )
    parser.add_argument('--specialist', default=None,
                        choices=list(VALID_SPECIALISTS),
                        help="If set, runs train_full_model_only with the chosen "
                             "specialist (gallery training mode). Otherwise main() "
                             "runs the full bootstrap.")
    args = parser.parse_args()
    if args.specialist:
        train_full_model_only(specialist=args.specialist)
    else:
        main()
