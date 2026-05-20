"""
Substrate-correct longshot_rf inference path (Phase B Tier 1 follow-up).

Tier 1 2C verbatim finding: production `_predict_rf_simplified()` at
ls_inference_service.py:463 invokes the 60-feature RF with 57 zeros + 3 real
values. Tier 1 measurement showed substrate-correct invocation produces
AUC 0.7762 against the trained target (10-1+ longshot winner) — a strong
signal that the broken production path destroys.

This module provides a substrate-correct invocation helper that builds the
full 60-feature vector matching training-time spec from
`model/longshot/train.py`:
    rf_features = core_features (58) + ['l1_win_prob', 'l2_rank_score']

Production wiring decision pending Tony adjudication (option a/b/c per
SP-LONGSHOT-RF-INFERENCE-FIX dispatch).
"""
from __future__ import annotations
import logging
import os
from typing import Dict, List, Optional

import boto3
import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Path-defer imports so module can be loaded outside a fully-configured runtime
try:
    from model.shared.feature_definitions import get_core_features
    _CORE_FEATURES = get_core_features(include_odds=True)
except Exception:
    _CORE_FEATURES = None


def get_longshot_rf_feature_names() -> List[str]:
    """60 feature names in training-time order — substrate-correct."""
    if _CORE_FEATURES is None:
        from model.shared.feature_definitions import get_core_features
        core = get_core_features(include_odds=True)
    else:
        core = _CORE_FEATURES
    return list(core) + ['l1_win_prob', 'l2_rank_score']


def _patch_sklearn_pickle_compat(rf_model):
    """sklearn 1.3.2 → 1.8.0 pickle compatibility: missing monotonic_cst attribute.

    Reproduced from Tier 1 2C substrate-correct invocation script.
    """
    if hasattr(rf_model, 'estimators_'):
        for est in rf_model.estimators_:
            if not hasattr(est, 'monotonic_cst'):
                est.monotonic_cst = None
            if not hasattr(est, '_n_classes'):
                est._n_classes = (
                    est.n_classes_ if hasattr(est, 'n_classes_') else None
                )
    return rf_model


def load_longshot_rf_from_s3(s3_path: str, local_path: Optional[str] = None):
    """Load longshot_rf RandomForestClassifier with sklearn-version-patch."""
    if local_path is None:
        local_path = '/tmp/longshot_rf/model.pkl'
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    if not os.path.exists(local_path):
        bucket, _, key = s3_path[5:].partition('/')
        boto3.client('s3').download_file(bucket, key, local_path)
    model = joblib.load(local_path)
    return _patch_sklearn_pickle_compat(model)


def build_longshot_rf_input(
    feature_df: pd.DataFrame,
    l1_win_prob: pd.Series,
    l2_rank_score: pd.Series,
) -> np.ndarray:
    """Build substrate-correct 60-feature input matrix.

    Args:
        feature_df: per-horse DataFrame with all 58 CORE_FEATURES columns
            (produced by FeatureEngineeringService.build_feature_matrix)
        l1_win_prob: per-horse Series of L1 win_prob predictions (from
            win_prob_odds or win_prob_core layer)
        l2_rank_score: per-horse Series of L2 rank_score predictions (from
            ranker_core layer)

    Returns:
        np.ndarray of shape (n_horses, 60) ready for RF.predict_proba()
    """
    feature_names = get_longshot_rf_feature_names()
    core_features = feature_names[:-2]  # 58 CORE
    missing = [f for f in core_features if f not in feature_df.columns]
    if missing:
        logger.warning(
            f"longshot_rf input: {len(missing)} CORE features missing from "
            f"feature_df: {missing[:5]}... filling with 0.0 per training-time "
            f"default substrate"
        )
        for c in missing:
            feature_df[c] = 0.0

    # Critical: handle closing_odds substrate-mismatch (training-time has
    # closing_odds; inference-time uses morning_line_odds as proxy because
    # closing odds aren't known until post-race)
    if 'closing_odds' in core_features and 'closing_odds' not in feature_df.columns:
        if 'morning_line_odds' in feature_df.columns:
            feature_df['closing_odds'] = feature_df['morning_line_odds']
            logger.info(
                "longshot_rf input: closing_odds substituted with "
                "morning_line_odds (inference-time substrate-pragmatic)"
            )
        else:
            feature_df['closing_odds'] = 0.0

    X_core = feature_df[core_features].fillna(0.0).values.astype(np.float32)
    X_l1 = np.asarray(l1_win_prob.values, dtype=np.float32).reshape(-1, 1)
    X_l2 = np.asarray(l2_rank_score.values, dtype=np.float32).reshape(-1, 1)
    X = np.hstack([X_core, X_l1, X_l2])
    assert X.shape[1] == 60, f"expected 60 features, got {X.shape[1]}"
    return X


def predict_longshot_rf_substrate_correct(
    rf_model,
    feature_df: pd.DataFrame,
    l1_win_prob: pd.Series,
    l2_rank_score: pd.Series,
) -> np.ndarray:
    """Substrate-correct 60-feature RF invocation.

    Returns:
        np.ndarray of P(longshot_win) per horse (positive class probability).
    """
    X = build_longshot_rf_input(feature_df, l1_win_prob, l2_rank_score)
    try:
        probs = rf_model.predict_proba(X)
        return probs[:, 1] if probs.shape[1] >= 2 else probs[:, 0]
    except Exception as e:
        # Fallback: tree-wise prediction for sklearn version mismatch edge cases
        logger.warning(f"predict_proba fail ({e}); tree-wise fallback")
        probs = np.zeros(len(X))
        for est in rf_model.estimators_:
            p = est.predict_proba(X)
            probs += p[:, 1] if p.shape[1] >= 2 else p[:, 0]
        return probs / len(rf_model.estimators_)
