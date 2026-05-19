"""
Win Probability Model (Layer 1) — Two-Layer Training Script

Binary classification: binary:logistic
Output: calibrated P(win) via sigmoid — NO softmax.

Layer 1 (Core): 58/55 features. Trained on ALL years.
Layer 2 (Workout Adjustment): core_predicted_prob + 8 workout features.
    Trained ONLY on rows where real workout data exists.

Trains BOTH:
  v_base  — 55 features (odds-blind)
  v_odds  — 58 features (odds-aware)

Run on Fargate:
  aws ecs run-task --cluster equine-cluster \
    --task-definition equine-training-manual --launch-type FARGATE \
    --overrides '{"containerOverrides":[{"name":"training","command":["model/win_prob/train.py"]}]}'
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

# Allow running from model/ directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.data_loader import build_feature_matrix, _get_conn
from shared.evaluation import full_evaluation
from shared.feature_definitions import (
    get_core_features,
    get_workout_features,
    get_odds_aware_features,
    get_lean53_features,
    get_gonzo_sauce_features,
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
from win_prob.config import (
    XGB_PARAMS, NUM_ROUNDS, EARLY_STOPPING_ROUNDS,
    WORKOUT_XGB_PARAMS, WORKOUT_NUM_ROUNDS, WORKOUT_EARLY_STOPPING_ROUNDS,
    compute_binary_labels,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)
logger = logging.getLogger(__name__)

S3_BUCKET      = 'equine-model-artifacts'
S3_PREFIX      = 'win_prob'
LOCAL_ARTIFACTS = Path(__file__).parent / 'artifacts'

# Phase A3: dataset-dump destination. Originally specced to a separate
# `equine-training-data` bucket, but pre-flight showed that bucket doesn't
# exist. Falls back to the model-artifacts bucket (Fargate IAM role
# already has write access there).
S3_DATASET_BUCKET = 'equine-model-artifacts'
S3_DATASET_PREFIX = 'gonzo_sauce/dataset_dump'


def dump_dataset_only(specialist: str = 'gonzo_sauce') -> int:
    """
    Generate the feature matrix via build_feature_matrix() and write it to
    S3 as parquet, then exit. No XGBoost training. Used to gate dataset
    stats review before committing to a full training run.

    Output:
      s3://{S3_DATASET_BUCKET}/{S3_DATASET_PREFIX}/{timestamp}/features.parquet
      s3://{S3_DATASET_BUCKET}/{S3_DATASET_PREFIX}/{timestamp}/labels.parquet
      s3://{S3_DATASET_BUCKET}/{S3_DATASET_PREFIX}/{timestamp}/metadata.json

    Returns process exit code (0 on success).
    """
    from datetime import datetime, timezone
    import time

    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    s3_prefix = f'{S3_DATASET_PREFIX}/{timestamp}'

    logger.info(f"[dump-only] specialist={specialist}")
    logger.info(f"[dump-only] target s3://{S3_DATASET_BUCKET}/{s3_prefix}/")

    pp_filter = get_pp_filter(specialist)
    if pp_filter:
        logger.info(f"[dump-only] using pp_filter for specialist={specialist}")

    t_start = time.perf_counter()
    with _get_conn() as conn:
        features_df, labels_df = build_feature_matrix(
            conn=conn,
            start_year=2022,
            end_year=2026,
            include_odds=True,
            pps_filter=pp_filter,
        )
    build_secs = time.perf_counter() - t_start

    logger.info(
        f"[dump-only] features_df: {features_df.shape}, "
        f"labels_df: {labels_df.shape}, "
        f"build={build_secs:.1f}s"
    )

    local_dir = Path('/tmp/dataset_dump')
    local_dir.mkdir(parents=True, exist_ok=True)
    features_path = local_dir / 'features.parquet'
    labels_path = local_dir / 'labels.parquet'
    meta_path = local_dir / 'metadata.json'

    features_df.to_parquet(
        features_path, engine='pyarrow', compression='snappy', index=False
    )
    labels_df.to_parquet(
        labels_path, engine='pyarrow', compression='snappy', index=False
    )

    metadata = {
        'specialist': specialist,
        'timestamp_utc': timestamp,
        'total_rows': int(len(features_df)),
        'race_date_min': str(labels_df['race_date'].min()),
        'race_date_max': str(labels_df['race_date'].max()),
        'qualifying_race_count': int(labels_df['race_key'].nunique()),
        'feature_count': int(len(features_df.columns) - 1),
        'feature_names': [c for c in features_df.columns if c != 'pp_id'],
        'build_duration_seconds': round(build_secs, 1),
        'pipeline_source': 'model/win_prob/train.py --dump-dataset-only',
        'data_loader_version': 'phase_a3_gonzo_sauce_2026-05-01',
    }
    meta_path.write_text(json.dumps(metadata, indent=2))

    s3 = boto3.client('s3', region_name='us-east-1')
    for local_path in [features_path, labels_path, meta_path]:
        s3_key = f'{s3_prefix}/{local_path.name}'
        s3.upload_file(str(local_path), S3_DATASET_BUCKET, s3_key)
        logger.info(f"[dump-only] uploaded s3://{S3_DATASET_BUCKET}/{s3_key}")

    logger.info(
        f"[dump-only] complete. {len(features_df):,} rows × "
        f"{len(features_df.columns) - 1} features in {build_secs:.0f}s"
    )
    return 0


def normalize_within_race(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize raw sigmoid P(win) to sum to 1 within each race.
    Stores both raw_win_prob (model output) and win_probability (normalized).
    """
    out = df.copy()
    out['win_probability'] = 0.0
    for rk, group in out.groupby('race_key'):
        raw = group['raw_win_prob'].values.astype(float)
        total = raw.sum()
        if total > 0:
            normed = raw / total
        else:
            normed = np.ones_like(raw) / len(raw)
        out.loc[group.index, 'win_probability'] = normed
    return out


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

    importance = model.get_score(importance_type='gain')
    imp_file.write_text(json.dumps(importance, indent=2))

    eval_file.write_text(json.dumps(eval_results, indent=2))

    meta = {
        'version':      version,
        'model_type':   model_type,
        'specialist':   specialist,
        'criterion':    CRITERION_DESCRIPTIONS.get(specialist, ''),
        'label_type':   'binary',
        'objective':    'binary:logistic',
        'feature_count': len(feature_names),
        'feature_names': feature_names,
        'xgb_params':   params,
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

    # § 4.33: register in model_versions post-S3-upload
    try:
        from training.registration import register_trained_artifact
        # REPAIR-5-RESCUE: pass model_type=None so register_trained_artifact
        # invokes derive_model_type(version_name) → substrate-canonical mapping
        # (wp_core_lean58_X → win_prob_core_X). Passing raw version_suffix as
        # model_type bypassed derive_model_type, producing model_type values
        # that didn't match production inference service queries.
        register_trained_artifact(
            version_name=version,
            model_type=None,
            s3_artifact_path=f's3://{S3_BUCKET}/{S3_PREFIX}/{model_file.name}',
            training_metadata={
                'feature_names': feature_names,
                'xgb_params': params,
                'top1_accuracy': eval_results.get('top1_win_rate'),
                'calibration_score': eval_results.get('calibration'),
                'exacta_hit_rate': eval_results.get('exacta_hit_rate'),
                'trifecta_hit_rate': eval_results.get('trifecta_hit_rate'),
                'flat_bet_roi': eval_results.get('flat_bet_roi'),
                'kelly_roi': eval_results.get('kelly_roi'),
                'value_bet_win_rate': eval_results.get('value_bet_win_rate'),
                'notes': (
                    f'win_prob per-layer training; model_type={model_type}; '
                    f'specialist={specialist}; objective=binary:logistic'
                ),
            },
        )
    except Exception as e:
        logger.warning(f'model_versions registration failed for {version}: {e}')


def train_core(features_df: pd.DataFrame, labels_df: pd.DataFrame,
               binary_labels: np.ndarray, feature_names: list[str],
               version_suffix: str, params: dict,
               sample_weight: np.ndarray = None,
               specialist: str = 'general') -> tuple[xgb.Booster, dict, np.ndarray]:
    """
    Train Layer 1 (core model). Returns booster, eval_results,
    and raw sigmoid predictions on ALL rows for Layer 2 input.
    """
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')
    version = f'{version_suffix}_{timestamp}'

    train_mask = labels_df['race_date'] <= pd.Timestamp('2026-04-24')
    val_mask   = (labels_df['race_date'] >= pd.Timestamp('2026-04-25')) & (labels_df['race_date'] <= pd.Timestamp('2026-05-01'))

    X_train = features_df.loc[train_mask, feature_names].values.astype(np.float32)
    y_train = binary_labels[train_mask]
    X_val   = features_df.loc[val_mask,   feature_names].values.astype(np.float32)
    y_val   = binary_labels[val_mask]

    if sample_weight is not None:
        sw_train = sample_weight[train_mask.values]
        sw_val   = sample_weight[val_mask.values]
        logger.info(
            f"[{version_suffix}] sample_weight: train mean={sw_train.mean():.3f} "
            f"max={sw_train.max():.1f} (n_weighted={int((sw_train>1).sum()):,})"
        )
    else:
        sw_train = sw_val = None

    logger.info(
        f"[{version_suffix}] train={len(X_train):,} rows  val={len(X_val):,} rows  "
        f"features={len(feature_names)}"
    )

    dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=feature_names, weight=sw_train)
    dval   = xgb.DMatrix(X_val,   label=y_val,   feature_names=feature_names, weight=sw_val)

    booster = xgb.train(
        params,
        dtrain,
        num_boost_round=NUM_ROUNDS,
        evals=[(dtrain, 'train'), (dval, 'val')],
        early_stopping_rounds=EARLY_STOPPING_ROUNDS,
        verbose_eval=50,
    )
    logger.info(f"[{version_suffix}] best_iteration={booster.best_iteration}")

    # Evaluate on validation set
    # binary:logistic outputs P(win) directly from sigmoid
    raw_val_probs = booster.predict(dval)
    val_labels = labels_df[val_mask].copy().reset_index(drop=True)
    val_labels['raw_win_prob'] = raw_val_probs
    val_labels['predicted_score'] = raw_val_probs  # for ranking
    val_labels['is_winner'] = (val_labels['finish_position'] == 1).astype(float)

    # Normalize within race for display metrics
    val_labels = normalize_within_race(val_labels)
    # predicted_prob used by evaluation.py for Kelly/edge calculations
    val_labels['predicted_prob'] = val_labels['win_probability']

    eval_results = full_evaluation(val_labels, model_name=f'WinProb {version_suffix}')

    save_artifacts(booster, feature_names, eval_results, params, version,
                   version_suffix, specialist=specialist)

    # Generate predictions on ALL rows for Layer 2 input
    X_all = features_df[feature_names].values.astype(np.float32)
    dall = xgb.DMatrix(X_all, feature_names=feature_names)
    all_probs = booster.predict(dall)

    return booster, eval_results, all_probs


def has_real_workout_data(features_df: pd.DataFrame) -> np.ndarray:
    """True for rows where workout data is real (not defaults)."""
    wc = features_df['workout_count_30d'].values
    ds = features_df['days_since_last_workout'].values
    return (wc > 0) | (ds != 30.0)


def train_workout_layer(features_df: pd.DataFrame, labels_df: pd.DataFrame,
                        binary_labels: np.ndarray, core_probs: np.ndarray,
                        workout_feature_names: list[str],
                        version_suffix: str, params: dict) -> tuple:
    """
    Train Layer 2 (workout adjustment) on ONLY rows with real workout data.
    Features: core_predicted_prob + 8 workout features = 9 total.
    """
    # Compute normalized core probability per race
    temp_df = labels_df.copy()
    temp_df['raw_core_prob'] = core_probs
    temp_df['core_predicted_prob'] = 0.0
    for rk, group in temp_df.groupby('race_key'):
        raw = group['raw_core_prob'].values.astype(float)
        total = raw.sum()
        if total > 0:
            temp_df.loc[group.index, 'core_predicted_prob'] = raw / total
        else:
            temp_df.loc[group.index, 'core_predicted_prob'] = 1.0 / len(raw)

    # Filter to rows with real workout data
    workout_mask = has_real_workout_data(features_df)
    n_total = len(features_df)
    n_workout = int(workout_mask.sum())
    logger.info(f"[{version_suffix}] Rows with real workout data: {n_workout:,} / {n_total:,}")

    if n_workout < 100:
        logger.warning(f"[{version_suffix}] Too few workout rows ({n_workout}) — skipping Layer 2")
        return None, None

    l2_feature_names = ['core_predicted_prob'] + workout_feature_names
    l2_features = pd.DataFrame({
        'core_predicted_prob': temp_df['core_predicted_prob'].values,
    })
    for wf in workout_feature_names:
        l2_features[wf] = features_df[wf].values

    l2_features_w = l2_features[workout_mask].reset_index(drop=True)
    binary_labels_w = binary_labels[workout_mask]
    labels_w = labels_df[workout_mask].reset_index(drop=True)

    train_mask = labels_w['race_date'] <= pd.Timestamp('2026-04-24')
    val_mask   = (labels_w['race_date'] >= pd.Timestamp('2026-04-25')) & (labels_w['race_date'] <= pd.Timestamp('2026-05-01'))
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
    y_train = binary_labels_w[train_mask.values]

    dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=l2_feature_names)
    evals = [(dtrain, 'train')]

    if n_val > 0:
        X_val = l2_features_w.loc[val_mask, l2_feature_names].values.astype(np.float32)
        y_val = binary_labels_w[val_mask.values]
        dval = xgb.DMatrix(X_val, label=y_val, feature_names=l2_feature_names)
        evals.append((dval, 'val'))

    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')
    version = f'{version_suffix}_{timestamp}'

    booster = xgb.train(
        params,
        dtrain,
        num_boost_round=WORKOUT_NUM_ROUNDS,
        evals=evals,
        early_stopping_rounds=WORKOUT_EARLY_STOPPING_ROUNDS if len(evals) > 1 else None,
        verbose_eval=50,
    )
    logger.info(f"[{version_suffix}] Layer 2 best_iteration={booster.best_iteration}")

    eval_results = None
    if n_val > 10:
        raw_probs = booster.predict(dval)
        wo_labels = labels_w[val_mask].copy().reset_index(drop=True)
        wo_labels['raw_win_prob'] = raw_probs
        wo_labels['predicted_score'] = raw_probs
        wo_labels['is_winner'] = (wo_labels['finish_position'] == 1).astype(float)
        wo_labels = normalize_within_race(wo_labels)
        wo_labels['predicted_prob'] = wo_labels['win_probability']
        eval_results = full_evaluation(wo_labels, model_name=f'WinProb {version_suffix}')
    else:
        logger.info(f"[{version_suffix}] Only {n_val} val rows — skipping Layer 2 eval")

    save_artifacts(booster, l2_feature_names,
                   eval_results or {'note': f'no val eval — only {n_val} val rows'},
                   params, version, version_suffix)

    return booster, eval_results


def train_full_model(features_df: pd.DataFrame, labels_df: pd.DataFrame,
                     binary_labels: np.ndarray, params: dict,
                     pps_df: pd.DataFrame = None,
                     specialist: str = 'general') -> tuple:
    """
    Train the FULL model. Feature set is gated by env LEAN_TAG:
      LEAN_TAG=lean53 → 53 features (lean53 cull, no odds, no zero-gain)
      unset           → 66 features (legacy odds-aware)
    ONLY uses rows where real workout data exists.
    """
    lean_tag = os.environ.get("LEAN_TAG", "").strip()
    if specialist == 'gonzo_sauce':
        if lean_tag == "lean58":
            # Phase 3 (2026-05-16): Phase B Top-5 + Gonzo = 72 features
            from shared.feature_definitions import get_gonzo_sauce_plus_top5_features
            full_features = get_gonzo_sauce_plus_top5_features()
        else:
            # Phase A3: lean53 base (53) + 14 Gonzo Sauce features = 67 features.
            full_features = get_gonzo_sauce_features()
    elif lean_tag == "lean58":
        # Phase 3 (2026-05-16): lean53 + 5 Phase B Top-5 = 58 features
        from shared.feature_definitions import get_lean53_plus_top5_features
        full_features = get_lean53_plus_top5_features()
    elif lean_tag == "lean53":
        full_features = get_lean53_features()  # 53 features
    else:
        full_features = get_odds_aware_features()  # 66 features
    logger.info(
        f"wp_full feature set: {len(full_features)} features "
        f"(specialist={specialist}, LEAN_TAG={lean_tag!r})"
    )

    has_workouts = (
        (features_df['workout_count_30d'] > 0) |
        (features_df['days_since_last_workout'] != 30.0)
    )
    feat_wk = features_df[has_workouts].reset_index(drop=True)
    labels_wk = labels_df[has_workouts].reset_index(drop=True)
    binary_wk = binary_labels[has_workouts.values]

    n_total = len(features_df)
    n_wk = len(feat_wk)
    logger.info(f"Full model: {n_wk:,} rows with workout data (of {n_total:,} total)")

    if n_wk < 100:
        logger.warning(f"Too few workout rows ({n_wk}) — skipping full model")
        return None, None

    n_win = int((binary_wk == 1.0).sum())
    n_lose = int((binary_wk == 0.0).sum())
    params_full = dict(params)
    params_full['scale_pos_weight'] = n_lose / n_win if n_win > 0 else 1.0

    sw = None
    if specialist in WEIGHT_SPECIALISTS:
        # Filter specialists (sprint, route) get pre-filtered data, no
        # upweighting on top. General gets nothing. Only WEIGHT
        # specialists receive sample_weight.
        sw = compute_sample_weights(feat_wk, labels_wk, pps_df, specialist)

    suffix = artifact_suffix('wp_full', specialist)
    booster, eval_results, _ = train_core(
        feat_wk, labels_wk, binary_wk, full_features,
        suffix, params_full, sample_weight=sw, specialist=specialist
    )
    return booster, eval_results


def train_core_model_only(specialist: str = 'general'):
    """
    Stream A2 lean53 wp_core trainer (added 2026-04-29).

    Replaces the legacy wp_odds (58-feature, closing_odds-bearing) model
    that has been silently routing for non-workout horses. Trains on ALL
    rows (no has_workout filter) using lean53_core (47 features — no
    odds, no zero-gain, no workout features).

    Output: wp_core_lean53_<specialist>_<ts>.json under win_prob/ S3 prefix.
    Registered in model_versions as model_type=win_prob_core_<specialist>.

    LEAN_TAG=lean53 env var must be set (else suffix injection fails).
    """
    specialist = validate_specialist(specialist)
    logger.info(
        f"wp_core lean53 training starting (specialist={specialist})"
    )
    conn = _get_conn()

    logger.info("Building feature matrix (2022-2026)...")
    pps_filter = get_pp_filter(specialist)
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2022, end_year=2026, include_odds=True,
        pps_filter=pps_filter,
    )

    pps_df_for_weight = None
    if specialist in ('speed', 'closer', 'class_riser', 'class_dropper'):
        from shared.data_loader import _load_raw_pps
        pps_df_for_weight = _load_raw_pps(conn, 2022, 2025)

    conn.close()

    binary_labels = compute_binary_labels(labels_df)
    n_winners = int((binary_labels == 1.0).sum())
    n_losers = int((binary_labels == 0.0).sum())
    spw = n_losers / n_winners if n_winners > 0 else 1.0

    # Feature set per LEAN_TAG (lean53 = 47; lean58 = 52 with Phase B Top-5)
    lean_tag_inner = os.environ.get("LEAN_TAG", "").strip()
    from shared.feature_definitions import (
        get_lean53_core_features, get_lean53_core_plus_top5_features,
    )
    if lean_tag_inner == "lean58":
        feat_core = get_lean53_core_plus_top5_features()  # 52
        logger.info(
            f"wp_core lean58 feature set: {len(feat_core)} features (lean53_core + Top-5)"
        )
    else:
        feat_core = get_lean53_core_features()  # 47
        logger.info(
            f"wp_core lean53 feature set: {len(feat_core)} features (lean53_core)"
        )

    params = dict(XGB_PARAMS)
    params['scale_pos_weight'] = spw

    sw = None
    if specialist in WEIGHT_SPECIALISTS:
        sw = compute_sample_weights(
            features_df, labels_df, pps_df_for_weight, specialist
        )

    # artifact_suffix injects LEAN_TAG → 'wp_core_lean53' / 'wp_core_lean53_<spec>'
    suffix = artifact_suffix('wp_core', specialist)
    logger.info(
        f"=== Training {suffix} ({len(feat_core)} features, ALL rows, "
        f"specialist={specialist}) ==="
    )
    train_core(
        features_df, labels_df, binary_labels, feat_core,
        suffix, params, sample_weight=sw, specialist=specialist,
    )
    logger.info("wp_core lean53 training complete")


def train_full_model_only(specialist: str = 'general'):
    """
    Entry point for daily retrain of ONLY the _full (workout) models.
    Skips core training. Called by daily retrain cron.

    specialist: one of VALID_SPECIALISTS. 'general' is byte-identical to
        the legacy daily retrain. Other values produce specialist-tagged
        artifacts (e.g., wp_full_speed_<ts>.json) for the gallery.
    """
    specialist = validate_specialist(specialist)
    logger.info(f"Win Probability FULL model daily retrain starting (specialist={specialist})")
    conn = _get_conn()

    logger.info("Building feature matrix (2022-2026)...")
    pps_filter = get_pp_filter(specialist)
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2022, end_year=2026, include_odds=True,
        pps_filter=pps_filter,
    )

    # Sample-weight specialists need raw pps to compute their criteria
    pps_df_for_weight = None
    if specialist in ('speed', 'closer', 'class_riser', 'class_dropper'):
        from shared.data_loader import _load_raw_pps
        pps_df_for_weight = _load_raw_pps(conn, 2022, 2025)

    conn.close()

    binary_labels = compute_binary_labels(labels_df)
    n_winners = int((binary_labels == 1.0).sum())
    n_losers = int((binary_labels == 0.0).sum())
    spw = n_losers / n_winners if n_winners > 0 else 1.0
    XGB_PARAMS['scale_pos_weight'] = spw

    suffix = artifact_suffix('wp_full', specialist)
    logger.info(f"=== Training {suffix} (66 features, workout data only, specialist={specialist}) ===")
    train_full_model(features_df, labels_df, binary_labels, XGB_PARAMS,
                     pps_df=pps_df_for_weight, specialist=specialist)
    logger.info("Win Probability FULL model daily retrain complete")


def main():
    logger.info("Win Probability Model (Layer 1) training starting — binary:logistic")
    conn = _get_conn()

    logger.info("Building feature matrix (2022-2026)...")
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2022, end_year=2026, include_odds=True
    )
    conn.close()

    binary_labels = compute_binary_labels(labels_df)
    n_winners = int((binary_labels == 1.0).sum())
    n_losers = int((binary_labels == 0.0).sum())
    spw = n_losers / n_winners if n_winners > 0 else 1.0

    logger.info(
        f"Binary labels: {n_winners:,} winners, {n_losers:,} losers  "
        f"scale_pos_weight={spw:.2f}"
    )

    # Set scale_pos_weight dynamically
    XGB_PARAMS['scale_pos_weight'] = spw
    WORKOUT_XGB_PARAMS['scale_pos_weight'] = spw

    workout_feats = get_workout_features()

    # ── Layer 1: Core models ────────────────────────────
    logger.info("=" * 60)
    logger.info("LAYER 1: Win Probability Core (binary:logistic)")
    logger.info("=" * 60)

    logger.info("=== Training v_base (55 features, odds-blind) ===")
    feat_base = get_core_features(include_odds=False)
    _, eval_base, base_all_probs = train_core(
        features_df, labels_df, binary_labels, feat_base,
        'wp_base', XGB_PARAMS
    )

    logger.info("=== Training v_odds (58 features, odds-aware) ===")
    feat_odds = get_core_features(include_odds=True)
    _, eval_odds, odds_all_probs = train_core(
        features_df, labels_df, binary_labels, feat_odds,
        'wp_odds', XGB_PARAMS
    )

    # Core model comparison
    print("\n" + "=" * 70)
    print("  Layer 1 Core: wp_base vs wp_odds — Validation (2025)")
    print("=" * 70)
    metrics_to_show = [
        'flat_bet_roi', 'kelly_roi', 'top1_win_rate',
        'exacta_hit_rate', 'trifecta_hit_rate', 'value_bet_win_rate',
    ]
    print(f"  {'Metric':<28} {'wp_base':>10} {'wp_odds':>10}")
    print("-" * 54)
    for m in metrics_to_show:
        b = eval_base.get(m, 0)
        o = eval_odds.get(m, 0)
        if 'roi' in m:
            print(f"  {m:<28} {b:>+10.1%} {o:>+10.1%}")
        else:
            print(f"  {m:<28} {b:>10.3f} {o:>10.3f}")
    print("=" * 70)

    # ── Full model (66 features, workout data only) ─────
    logger.info("")
    logger.info("=" * 60)
    logger.info("WIN PROB FULL MODEL (66 features, workout data only)")
    logger.info("=" * 60)

    _, eval_full = train_full_model(
        features_df, labels_df, binary_labels, XGB_PARAMS
    )

    # Final summary
    print("\n" + "=" * 70)
    print("  WIN PROBABILITY TRAINING COMPLETE — Summary")
    print("=" * 70)
    print(f"\n  Core models:")
    print(f"    wp_base: {len(feat_base)} features, "
          f"top1={eval_base.get('top1_win_rate', 0):.3f}, "
          f"roi={eval_base.get('flat_bet_roi', 0):+.1%}")
    print(f"    wp_odds: {len(feat_odds)} features, "
          f"top1={eval_odds.get('top1_win_rate', 0):.3f}, "
          f"roi={eval_odds.get('flat_bet_roi', 0):+.1%}")
    if eval_full:
        print(f"  Full model:")
        print(f"    wp_full: 66 features, "
              f"top1={eval_full.get('top1_win_rate', 0):.3f}, "
              f"roi={eval_full.get('flat_bet_roi', 0):+.1%}")
    else:
        print(f"  Full model: skipped (insufficient workout data)")
    print("=" * 70)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Win-prob training. Default: full bootstrap (core + workout + full)."
    )
    parser.add_argument('--specialist', default=None,
                        choices=list(VALID_SPECIALISTS),
                        help="If set, runs train_full_model_only (or "
                             "train_core_model_only with --core-only) with the "
                             "chosen specialist (gallery training mode). "
                             "Otherwise main() runs the full bootstrap.")
    parser.add_argument('--core-only', action='store_true',
                        help="With --specialist, train wp_core lean53 (47 "
                             "features, ALL rows) instead of wp_full lean53.")
    parser.add_argument('--dump-dataset-only', action='store_true',
                        help="Generate feature matrix + write to S3 as parquet, "
                             "skip XGBoost training. Used for pre-training stats "
                             "review (Phase A3). Combine with --specialist to "
                             "scope (default: gonzo_sauce).")
    args = parser.parse_args()
    if args.dump_dataset_only:
        sys.exit(dump_dataset_only(
            specialist=args.specialist or 'gonzo_sauce'
        ))
    elif args.specialist and args.core_only:
        train_core_model_only(specialist=args.specialist)
    elif args.specialist:
        train_full_model_only(specialist=args.specialist)
    else:
        main()
