"""
P&L Optimization Model (Path 2) — Two-Layer Training Script

Always odds-aware. Uses clean EV labels (same as WR).
Kelly is only used at inference time for bet sizing, never in training.

Layer 1 (Core): 58 features (excludes workouts, always includes odds).
Layer 2 (Workout Adjustment): core_predicted_prob + 8 workout features.
    Trained ONLY on rows where real workout data exists.

Run on Fargate:
  aws ecs run-task --cluster equine-cluster \
    --task-definition equine-training-manual --launch-type FARGATE \
    --overrides '{"containerOverrides":[{"name":"training","command":["python3","model/pl/train.py"]}]}'
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

from shared.data_loader import build_feature_matrix, _get_conn, _load_raw_pps
from shared.evaluation import full_evaluation
from shared.feature_definitions import (
    get_core_features,
    get_workout_features,
    get_lean53_core_features,
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
from pl.config import (
    XGB_PARAMS_PL, NUM_ROUNDS, EARLY_STOPPING_ROUNDS,
    WORKOUT_XGB_PARAMS_PL, WORKOUT_NUM_ROUNDS, WORKOUT_EARLY_STOPPING_ROUNDS,
    compute_ev_labels,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)
logger = logging.getLogger(__name__)

S3_BUCKET      = 'equine-model-artifacts'
S3_PREFIX      = 'pl'
LOCAL_ARTIFACTS = Path(__file__).parent / 'artifacts'


def predictions_to_probs(predictions_df: pd.DataFrame) -> pd.DataFrame:
    """Softmax within each race."""
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
        'label_type':   'ev',
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
    # REPAIR-5-RESCUE: pass model_type=None so derive_model_type maps
    # lean58 prefixes → canonical model_type names (pl_core_lean58_X → pl_core_X)
    try:
        from training.registration import register_trained_artifact
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
                    f'pl per-layer training; model_type={model_type}; '
                    f'specialist={specialist}'
                ),
            },
        )
    except Exception as e:
        logger.warning(f'model_versions registration failed for {version}: {e}')


def has_real_workout_data(features_df: pd.DataFrame) -> np.ndarray:
    """True for rows where workout data is real (not defaults)."""
    wc = features_df['workout_count_30d'].values
    ds = features_df['days_since_last_workout'].values
    return (wc > 0) | (ds != 30.0)


def train_full_model_only(specialist: str = 'general'):
    """Daily-retrain entry for both PL layers, parameterised by specialist.

    'general' is byte-identical to the legacy main() flow:
    - pps_filter=None
    - sample_weight=None
    - artifact_suffix('pl_core', 'general') → 'pl_core' (no _general tag)
    """
    specialist = validate_specialist(specialist)
    logger.info(
        f"P&L two-layer daily retrain starting (specialist={specialist})"
    )

    pps_filter = get_pp_filter(specialist)  # None unless sprint/route

    conn = _get_conn()
    logger.info("Building feature matrix (2022-2026, odds-aware)...")
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2022, end_year=2026, include_odds=True,
        pps_filter=pps_filter,
    )

    sample_weight = None
    if specialist in WEIGHT_SPECIALISTS:
        # Weight specialists need raw pps to compute their per-row criterion.
        pps_df_for_weight = _load_raw_pps(conn, 2022, 2025)
        sample_weight = compute_sample_weights(
            features_df, labels_df, pps_df_for_weight, specialist
        )
    conn.close()

    ev_labels = compute_ev_labels(labels_df)
    logger.info(
        f"EV label stats: mean={ev_labels.mean():.3f}  "
        f"winners={int((ev_labels > 0).sum()):,}  "
        f"losers={int((ev_labels < 0).sum()):,}"
    )

    workout_feats = get_workout_features()

    # ── Layer 1: pl_core ─────────────────────────────────────────
    suffix_l1 = artifact_suffix('pl_core', specialist)
    logger.info("=" * 60)
    logger.info(
        f"LAYER 1: P&L Core Model (58 features, no workouts)  "
        f"specialist={specialist}"
    )
    logger.info("=" * 60)

    lean_tag = os.environ.get("LEAN_TAG", "").strip()
    if lean_tag == "lean58":
        # Phase 3 (2026-05-16): lean53_core + 5 Phase B Top-5 = 52 features
        from shared.feature_definitions import get_lean53_core_plus_top5_features
        feature_names = get_lean53_core_plus_top5_features()
    elif lean_tag == "lean53":
        feature_names = get_lean53_core_features()  # 47 features
    else:
        feature_names = get_core_features(include_odds=True)  # 58
    logger.info(f"pl_core feature set: {len(feature_names)} (LEAN_TAG={lean_tag!r})")
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')
    version_l1 = f'{suffix_l1}_{timestamp}'

    train_mask = labels_df['race_date'] <= pd.Timestamp('2026-04-24')
    val_mask   = (labels_df['race_date'] >= pd.Timestamp('2026-04-25')) & (labels_df['race_date'] <= pd.Timestamp('2026-05-01'))

    X_train = features_df.loc[train_mask, feature_names].values.astype(np.float32)
    y_train = ev_labels[train_mask]
    X_val   = features_df.loc[val_mask,   feature_names].values.astype(np.float32)
    y_val   = ev_labels[val_mask]

    sw_train = sample_weight[train_mask.values] if sample_weight is not None else None
    sw_val   = sample_weight[val_mask.values]   if sample_weight is not None else None

    if sw_train is not None:
        logger.info(
            f"[{suffix_l1}] sample_weight: train mean={sw_train.mean():.3f} "
            f"max={sw_train.max():.1f} "
            f"(n_weighted={int((sw_train > 1).sum()):,})"
        )

    logger.info(
        f"[{suffix_l1}] train={len(X_train):,}  val={len(X_val):,}  "
        f"features={len(feature_names)}"
    )

    dtrain = xgb.DMatrix(X_train, label=y_train,
                         feature_names=feature_names, weight=sw_train)
    dval = xgb.DMatrix(X_val, label=y_val,
                       feature_names=feature_names, weight=sw_val)

    booster = xgb.train(
        XGB_PARAMS_PL,
        dtrain,
        num_boost_round=NUM_ROUNDS,
        evals=[(dtrain, 'train'), (dval, 'val')],
        early_stopping_rounds=EARLY_STOPPING_ROUNDS,
        verbose_eval=50,
    )
    logger.info(f"[{suffix_l1}] best_iteration={booster.best_iteration}")

    # Evaluate Layer 1
    raw_val_preds = booster.predict(dval)
    val_labels_df = labels_df[val_mask].copy().reset_index(drop=True)
    val_labels_df['predicted_score'] = raw_val_preds
    val_labels_df = predictions_to_probs(val_labels_df)
    eval_core = full_evaluation(val_labels_df, model_name=f'P&L {suffix_l1}')

    logger.info(
        f"PRIMARY METRICS  kelly_roi={eval_core['kelly_roi']:+.1%}  "
        f"value_bet_win_rate={eval_core['value_bet_win_rate']:.3f}"
    )

    save_artifacts(booster, feature_names, eval_core, XGB_PARAMS_PL,
                   version_l1, suffix_l1, specialist=specialist)

    # Generate predictions on ALL rows for Layer 2 input
    X_all = features_df[feature_names].values.astype(np.float32)
    dall = xgb.DMatrix(X_all, feature_names=feature_names)
    all_preds = booster.predict(dall)

    # ── Layer 2: pl_workout (stacked on THIS specialist's Layer 1) ────
    suffix_l2 = artifact_suffix('pl_workout', specialist)
    logger.info("")
    logger.info("=" * 60)
    logger.info(
        f"LAYER 2: P&L Workout Adjustment Model  specialist={specialist}"
    )
    logger.info("=" * 60)

    # core_predicted_prob via per-race softmax (specialist-specific)
    temp_df = labels_df.copy()
    temp_df['core_score'] = all_preds
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
    logger.info(
        f"[{suffix_l2}] Rows with real workout data: "
        f"{n_workout:,} / {n_total:,}"
    )

    if n_workout < 100:
        logger.warning(
            f"[{suffix_l2}] Too few workout rows ({n_workout}) — "
            f"skipping Layer 2"
        )
    else:
        l2_feature_names = ['core_predicted_prob'] + workout_feats
        l2_features = pd.DataFrame(
            {'core_predicted_prob': temp_df['core_predicted_prob'].values}
        )
        for wf in workout_feats:
            l2_features[wf] = features_df[wf].values

        l2_features_w = l2_features[workout_mask].reset_index(drop=True)
        ev_labels_w = ev_labels[workout_mask]
        labels_w = labels_df[workout_mask].reset_index(drop=True)

        # Slice sample_weight to workout-only subset (specialist-aware)
        sw_w = sample_weight[workout_mask] if sample_weight is not None else None

        l2_train_mask = labels_w['race_date'] <= pd.Timestamp('2026-04-24')
        l2_val_mask   = (labels_w['race_date'] >= pd.Timestamp('2026-04-25')) & (labels_w['race_date'] <= pd.Timestamp('2026-05-01'))
        n_train = int(l2_train_mask.sum())
        n_val   = int(l2_val_mask.sum())

        sw_l2_train = (sw_w[l2_train_mask.values]
                       if sw_w is not None else None)
        sw_l2_val   = (sw_w[l2_val_mask.values]
                       if sw_w is not None and n_val > 0 else None)

        logger.info(
            f"[{suffix_l2}] Layer 2 train={n_train:,}  val={n_val:,}  "
            f"features={len(l2_feature_names)}"
        )
        if sw_l2_train is not None:
            logger.info(
                f"[{suffix_l2}] sample_weight: train mean={sw_l2_train.mean():.3f} "
                f"max={sw_l2_train.max():.1f} "
                f"(n_weighted={int((sw_l2_train > 1).sum()):,})"
            )

        if n_train >= 50:
            X_l2_train = l2_features_w.loc[l2_train_mask, l2_feature_names].values.astype(np.float32)
            y_l2_train = ev_labels_w[l2_train_mask.values]

            dl2_train = xgb.DMatrix(X_l2_train, label=y_l2_train,
                                   feature_names=l2_feature_names,
                                   weight=sw_l2_train)
            l2_evals = [(dl2_train, 'train')]

            if n_val > 0:
                X_l2_val = l2_features_w.loc[l2_val_mask, l2_feature_names].values.astype(np.float32)
                y_l2_val = ev_labels_w[l2_val_mask.values]
                dl2_val = xgb.DMatrix(X_l2_val, label=y_l2_val,
                                     feature_names=l2_feature_names,
                                     weight=sw_l2_val)
                l2_evals.append((dl2_val, 'val'))

            version_l2 = f'{suffix_l2}_{timestamp}'
            wo_booster = xgb.train(
                WORKOUT_XGB_PARAMS_PL,
                dl2_train,
                num_boost_round=WORKOUT_NUM_ROUNDS,
                evals=l2_evals,
                early_stopping_rounds=(
                    WORKOUT_EARLY_STOPPING_ROUNDS if len(l2_evals) > 1 else None
                ),
                verbose_eval=50,
            )
            logger.info(
                f"[{suffix_l2}] Layer 2 best_iteration={wo_booster.best_iteration}"
            )

            eval_workout = None
            if n_val > 10:
                wo_preds = wo_booster.predict(dl2_val)
                wo_val_labels = labels_w[l2_val_mask].copy().reset_index(drop=True)
                wo_val_labels['predicted_score'] = wo_preds
                wo_val_labels = predictions_to_probs(wo_val_labels)
                eval_workout = full_evaluation(
                    wo_val_labels, model_name=f'P&L {suffix_l2}'
                )
            else:
                logger.info(
                    f"[{suffix_l2}] Only {n_val} val rows — skipping Layer 2 eval"
                )

            save_artifacts(
                wo_booster, l2_feature_names,
                eval_workout or {'note': f'no val eval — only {n_val} val rows'},
                WORKOUT_XGB_PARAMS_PL, version_l2, suffix_l2,
                specialist=specialist,
            )
        else:
            logger.warning(
                f"[{suffix_l2}] Too few training rows ({n_train}) — skipping"
            )

    # Final summary
    print("\n" + "=" * 70)
    print(f"  P&L TRAINING COMPLETE — specialist={specialist}")
    print("=" * 70)
    print(f"  Layer 1 ({suffix_l1}):  "
          f"kelly_roi={eval_core.get('kelly_roi', 0):+.1%}  "
          f"top1={eval_core.get('top1_win_rate', 0):.3f}  "
          f"roi={eval_core.get('flat_bet_roi', 0):+.1%}")
    print("=" * 70)
    logger.info(
        f"P&L two-layer daily retrain complete (specialist={specialist})"
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--specialist', default='general',
                        choices=list(VALID_SPECIALISTS),
                        help="Specialist gallery member; 'general' is byte-"
                             "identical to legacy main()")
    args = parser.parse_args()
    train_full_model_only(specialist=args.specialist)
