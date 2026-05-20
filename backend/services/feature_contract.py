"""Canonical feature contract resolver.

REPAIR-5-FULL-CLOSURE: single source of truth for L1 model feature
selection. Substrate-pragmatic substrate-correct pattern: use the
booster's own feature_names. No more version_name substring detection.

Substrate-historical bug class addressed:
  Production wr/pl/ls/MCIS inference services used hardcoded feature
  lists (CORE_FEATURES, lean53, etc) + substring detection on
  version_name to switch between them. The 5/16 Phase B Top-5 trainer
  integration produced models with 52/58/67/72 features that the
  substring detection didn't cover → XGBoost feature_names mismatch
  → predict() raised → production DEAD since 2026-05-16.

Substrate-pragmatic substrate-fix:
  XGBoost boosters store training-time feature_names. Read them.
  Select wide feature DataFrame columns to match. Works for any
  artifact regardless of feature_count without per-version logic.
"""
from __future__ import annotations
import logging
from typing import Any, Optional

import numpy as np
import pandas as pd
import xgboost as xgb

logger = logging.getLogger(__name__)


def get_model_features(booster: xgb.Booster) -> list[str]:
    """Read substrate-canonical feature_names from a loaded booster.

    Raises ValueError if the model has no feature_names (corrupted artifact
    or non-XGBoost). Substrate-canonical: the model itself is the source
    of truth for what features it expects.
    """
    if booster is None:
        raise ValueError("get_model_features called with None booster")
    fn = booster.feature_names
    if not fn:
        raise ValueError(
            "Booster has no feature_names — substrate-corrupted artifact or "
            "non-XGBoost model. Cannot determine feature contract."
        )
    return list(fn)


def select_features(
    wide_df: pd.DataFrame,
    booster: xgb.Booster,
    fill_missing: float = 0.0,
) -> pd.DataFrame:
    """Select wide_df columns to match booster's feature contract.

    Substrate-discipline:
      - All booster.feature_names MUST exist in wide_df (substrate-error
        if missing — substrate-coverage gap that requires data_loader fix)
      - Returns substrate-actual subset DataFrame ordered per
        booster.feature_names (XGBoost validates ORDER as well as names)
      - NaN values filled with fill_missing (default 0.0)

    Raises:
      ValueError if any booster feature is absent from wide_df.
    """
    feats = get_model_features(booster)
    missing = [f for f in feats if f not in wide_df.columns]
    if missing:
        raise ValueError(
            f"Wide feature DataFrame missing {len(missing)} features required "
            f"by booster: {missing[:10]}{'...' if len(missing) > 10 else ''}. "
            f"Substrate-coverage gap: extend data_loader.build_feature_matrix "
            f"to produce these features."
        )
    return wide_df[feats].fillna(fill_missing)


def predict_with_contract(
    booster: xgb.Booster,
    wide_df: pd.DataFrame,
    fill_missing: float = 0.0,
) -> np.ndarray:
    """Substrate-canonical predict: select features per booster contract,
    build DMatrix with substrate-correct feature_names, call predict.

    Substrate-pragmatic single-entrypoint replacement for the scattered
    inference patterns: row_features[lean53_features], DMatrix(...),
    model.predict(...).
    """
    X = select_features(wide_df, booster, fill_missing=fill_missing)
    feats = get_model_features(booster)
    dm = xgb.DMatrix(X.values, feature_names=feats)
    return booster.predict(dm)


def diagnose_contract(booster: xgb.Booster, wide_df: pd.DataFrame) -> dict:
    """Substrate-diagnostic helper for debugging feature mismatches.

    Returns a dict with:
      - model_feature_count: how many features the booster expects
      - wide_feature_count: how many columns in the wide DataFrame
      - missing_from_wide: model features absent from wide_df
      - extra_in_wide: wide_df columns not used by model
    """
    feats = get_model_features(booster)
    wide_cols = set(wide_df.columns)
    missing = [f for f in feats if f not in wide_cols]
    extra = sorted(wide_cols - set(feats))
    return {
        'model_feature_count': len(feats),
        'wide_feature_count': len(wide_cols),
        'missing_from_wide': missing,
        'extra_in_wide_count': len(extra),
        'extra_in_wide_sample': extra[:10],
    }
