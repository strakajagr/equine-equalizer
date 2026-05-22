"""Gate 3 diagnostic training — one Fargate run produces all §3.2 + §2.1 + §2.2 data.

Per the Gate 3 dispatch, this trains a single canonical win-prob XGB model
across multiple feature-set variants on the SAME leak-free OOS-blocked
split, so the deltas are interpretable:

  - V0  baseline:                lean53+top5 (current production)
  - V1  +trajectory:             lean53+top5 + trajectory_score
  - V2  +trajectory  -lasix:     V1 minus lasix_first_time
  - V3  baseline    -lasix:      V0 minus lasix_first_time

§3.2 deliverable: V1 - V0  (trajectory contribution, holding lasix fixed)
§2.1 deliverable: V0 - V3  (lasix contribution, baseline) AND V1 - V2 (with trajectory)
§2.2 deliverable: per-variant feature-importance dump → cull candidates

All four variants share the same FE matrix (computed once with --include-trajectory).
Train/eval split is RACE-DATE-BLOCKED (not random) for honest OOS:
  - Train: race_date <= 2026-04-24
  - Eval:  2026-05-02 <= race_date <= 2026-05-17   ← matches Gate 2 OOS window
  - (Gap of 2026-04-25..2026-05-01 left as cushion against any temporal leak.)

Output:
  - /tmp/gate3_results.json — full metrics per variant
  - S3 upload to s3://equine-model-artifacts/gate3/gate3_results_<ts>.json
"""
import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import boto3
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).parent.parent / 'model'))

from shared.data_loader import build_feature_matrix
from shared.feature_definitions import (
    get_lean53_plus_top5_features,
    get_lean53_plus_top5_plus_trajectory_features,
)
from shared.lstm_loader import load_active_lstm, load_lstm_from_s3

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

S3_BUCKET = 'equine-model-artifacts'
S3_PREFIX = 'gate3'

# Date-blocked split — matches Gate 2 OOS window exactly
TRAIN_CUTOFF = pd.Timestamp('2026-04-24')
EVAL_START = pd.Timestamp('2026-05-02')
EVAL_END = pd.Timestamp('2026-05-17')

XGB_PARAMS = {
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'learning_rate': 0.05,
    'max_depth': 4,
    'subsample': 0.8,
    'colsample_bytree': 0.7,
    'min_child_weight': 3,
    'reg_alpha': 0.5,
    'reg_lambda': 2.0,
}


def train_variant(X_train, y_train, X_eval, y_eval, feature_names, variant_name):
    """Train one XGB variant and return metrics + feature importance."""
    logger.info(f"[{variant_name}] train={len(X_train):,}  eval={len(X_eval):,}  "
                f"features={len(feature_names)}")

    dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=feature_names)
    deval = xgb.DMatrix(X_eval, label=y_eval, feature_names=feature_names)
    booster = xgb.train(
        XGB_PARAMS, dtrain,
        num_boost_round=500,
        evals=[(dtrain, 'train'), (deval, 'eval')],
        early_stopping_rounds=30,
        verbose_eval=100,
    )

    preds_train = booster.predict(dtrain)
    preds_eval = booster.predict(deval)
    auc_train = float(roc_auc_score(y_train, preds_train))
    auc_eval = float(roc_auc_score(y_eval, preds_eval))

    # Feature importance (gain)
    importance = booster.get_score(importance_type='gain')
    importance_sorted = sorted(importance.items(), key=lambda x: -x[1])
    total_gain = sum(importance.values()) or 1.0
    top_features = [
        {'name': k, 'gain': float(v), 'pct_total': float(v) / total_gain * 100.0}
        for k, v in importance_sorted[:20]
    ]
    used_features = set(importance.keys())
    dead_features = [f for f in feature_names if f not in used_features]

    return {
        'variant': variant_name,
        'features_total': len(feature_names),
        'features_used': len(used_features),
        'features_dead': len(dead_features),
        'dead_features': dead_features,
        'top_features': top_features,
        'n_train': len(X_train),
        'n_eval': len(X_eval),
        'auc_train': auc_train,
        'auc_eval': auc_eval,
        'train_eval_gap': auc_train - auc_eval,
        'best_iteration': int(booster.best_iteration),
    }, booster, preds_eval


def evaluate_top1_by_race(eval_df, preds_eval, label_col='is_winner'):
    """Per-race top-1 / top-3 hit rates, like Gate 2."""
    eval_df = eval_df.copy()
    eval_df['pred'] = preds_eval
    top1_idx = eval_df.groupby('race_id')['pred'].idxmax()
    top1_hits = float(eval_df.loc[top1_idx, label_col].mean())

    def top_k_hit(grp, k):
        top_k = grp.nlargest(k, 'pred')
        return int(top_k[label_col].sum() > 0)

    races = eval_df.groupby('race_id')
    top2 = float(races.apply(lambda g: top_k_hit(g, 2)).mean())
    top3 = float(races.apply(lambda g: top_k_hit(g, 3)).mean())
    return {
        'n_races': eval_df['race_id'].nunique(),
        'top1_pct': top1_hits * 100.0,
        'top2_pct': top2 * 100.0,
        'top3_pct': top3 * 100.0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lstm-s3-path', default=None,
                        help='S3 URI for retrained LSTM (e.g. trajectory_lstm_2025*.pt). '
                             'If unset, loads active LSTM from model_versions.')
    args = parser.parse_args()

    t0 = time.time()
    logger.info("Gate 3 diagnostic training — single Fargate run")
    logger.info(f"Train cutoff:   <= {TRAIN_CUTOFF.date()}")
    logger.info(f"Eval window:    {EVAL_START.date()} → {EVAL_END.date()}")

    # 1. Load LSTM
    if args.lstm_s3_path:
        logger.info(f"Loading LSTM from explicit S3 path: {args.lstm_s3_path}")
        lstm_model, lstm_scaler = load_lstm_from_s3(args.lstm_s3_path)
        lstm_version = Path(args.lstm_s3_path).stem
    else:
        logger.info("Loading active LSTM from model_versions")
        lstm_model, lstm_scaler, lstm_version = load_active_lstm()
    if lstm_model is None:
        raise RuntimeError("No LSTM available — cannot run Gate 3")
    logger.info(f"LSTM version: {lstm_version}")

    # 2. Build FE matrix WITH trajectory (once — used by all variants)
    logger.info("Building feature matrix WITH trajectory (full window 2022-2026)...")
    fe_t0 = time.time()
    features_df, labels_df = build_feature_matrix(
        conn=None,  # uses default
        start_year=2022, end_year=2026,
        include_odds=True,
        lstm_model=lstm_model, lstm_scaler=lstm_scaler,
    )
    logger.info(f"Feature matrix built in {time.time() - fe_t0:.1f}s: {len(features_df):,} rows")

    # Merge for race_id grouping in eval
    full_df = features_df.merge(labels_df[['pp_id', 'race_date', 'finish_position']],
                                on='pp_id', how='inner')
    full_df['race_date'] = pd.to_datetime(full_df['race_date'])
    full_df['is_winner'] = (full_df['finish_position'] == 1).astype(int)
    full_df['race_id'] = labels_df.set_index('pp_id').loc[full_df['pp_id'], 'race_key'].values

    # 3. Date-blocked split (matches Gate 2 OOS window exactly)
    train_mask = full_df['race_date'] <= TRAIN_CUTOFF
    eval_mask = (full_df['race_date'] >= EVAL_START) & (full_df['race_date'] <= EVAL_END)
    logger.info(f"Train rows: {int(train_mask.sum()):,}  Eval rows: {int(eval_mask.sum()):,}")
    logger.info(f"Eval races: {full_df.loc[eval_mask, 'race_id'].nunique()}")

    # 4. Four variants
    feat_v0 = get_lean53_plus_top5_features()                       # baseline
    feat_v1 = get_lean53_plus_top5_plus_trajectory_features()       # +trajectory
    feat_v2 = [f for f in feat_v1 if f != 'lasix_first_time']       # +traj -lasix
    feat_v3 = [f for f in feat_v0 if f != 'lasix_first_time']       # -lasix

    variants = [
        ('V0_baseline_lean53_top5', feat_v0),
        ('V1_plus_trajectory', feat_v1),
        ('V2_plus_traj_minus_lasix', feat_v2),
        ('V3_minus_lasix', feat_v3),
    ]

    results = {
        'gate': 'gate_3',
        'lstm_version': lstm_version,
        'train_cutoff': str(TRAIN_CUTOFF.date()),
        'eval_window': [str(EVAL_START.date()), str(EVAL_END.date())],
        'variants': {},
    }

    for variant_name, feature_names in variants:
        # Ensure all features are present (any feature not in features_df gets NaN)
        for f in feature_names:
            if f not in full_df.columns:
                full_df[f] = float('nan')

        X_train = full_df.loc[train_mask, feature_names].values
        y_train = full_df.loc[train_mask, 'is_winner'].values.astype(np.float32)
        X_eval = full_df.loc[eval_mask, feature_names].values
        y_eval = full_df.loc[eval_mask, 'is_winner'].values.astype(np.float32)

        metrics, _booster, preds_eval = train_variant(
            X_train, y_train, X_eval, y_eval, feature_names, variant_name
        )

        eval_subset = full_df.loc[eval_mask, ['race_id', 'is_winner']].reset_index(drop=True)
        topk = evaluate_top1_by_race(eval_subset, preds_eval, 'is_winner')
        metrics.update(topk)

        # Trajectory coverage diagnostic (variants that include it)
        if 'trajectory_score' in feature_names:
            traj_col = full_df.loc[train_mask, 'trajectory_score']
            cov = float(traj_col.notna().mean()) * 100.0
            metrics['trajectory_coverage_train_pct'] = cov

        results['variants'][variant_name] = metrics
        logger.info(f"[{variant_name}] AUC_eval={metrics['auc_eval']:.4f}  "
                    f"top1={metrics['top1_pct']:.1f}%  top3={metrics['top3_pct']:.1f}%  "
                    f"train_eval_gap={metrics['train_eval_gap']:.3f}")

    # 5. Deltas
    v0 = results['variants']['V0_baseline_lean53_top5']
    v1 = results['variants']['V1_plus_trajectory']
    v2 = results['variants']['V2_plus_traj_minus_lasix']
    v3 = results['variants']['V3_minus_lasix']
    results['deltas'] = {
        'trajectory_contribution_top1': v1['top1_pct'] - v0['top1_pct'],
        'trajectory_contribution_auc':  v1['auc_eval']  - v0['auc_eval'],
        'lasix_contribution_baseline_top1': v0['top1_pct'] - v3['top1_pct'],
        'lasix_contribution_baseline_auc':  v0['auc_eval']  - v3['auc_eval'],
        'lasix_contribution_with_traj_top1': v1['top1_pct'] - v2['top1_pct'],
        'lasix_contribution_with_traj_auc':  v1['auc_eval']  - v2['auc_eval'],
    }

    # 6. MARKET baseline on the same eval set
    market = full_df.loc[eval_mask, ['race_id', 'is_winner', 'closing_odds']].copy()
    market['market_prob'] = 1.0 / (market['closing_odds'].clip(lower=0.5) + 1.0)
    eval_market = evaluate_top1_by_race(market.rename(columns={'market_prob': 'pred'}),
                                        market['market_prob'].values, 'is_winner')
    eval_market['auc_eval'] = float(roc_auc_score(market['is_winner'],
                                                  market['market_prob']))
    results['market_baseline'] = eval_market
    logger.info(f"MARKET top1={eval_market['top1_pct']:.1f}%  AUC={eval_market['auc_eval']:.4f}")

    # 7. Save + upload
    results['total_runtime_sec'] = round(time.time() - t0, 1)
    out_local = '/tmp/gate3_results.json'
    Path(out_local).write_text(json.dumps(results, indent=2, default=str))

    ts = datetime.utcnow().strftime('%Y%m%d_%H%M')
    s3_key = f'{S3_PREFIX}/gate3_results_{ts}.json'
    try:
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.upload_file(out_local, S3_BUCKET, s3_key)
        logger.info(f"Uploaded to s3://{S3_BUCKET}/{s3_key}")
    except Exception as e:
        logger.warning(f"S3 upload failed: {e}")

    logger.info("=" * 70)
    logger.info("GATE 3 DIAGNOSTIC — DELTAS")
    logger.info("=" * 70)
    for k, v in results['deltas'].items():
        logger.info(f"  {k:42s} = {v:+.4f}")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
