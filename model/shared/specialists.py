"""
Specialist-model gallery — sample-weight + filter logic for handicapping styles.

Specialists fall into two categories:

- FILTER specialists (sprint, route): restrict the training pool to in-distribution
  races by filtering the pps DataFrame BEFORE feature-matrix construction. The
  filter applies to iteration target AND historical context (pps_by_horse) since
  data_loader.build_feature_matrix uses one filtered pps for both.

- WEIGHT specialists (speed, closer, class_riser, class_dropper): trained on the
  full feature matrix but with sample_weight=3.0 applied to all rows in races
  whose winner met the specialist's criterion.

Used by model/win_prob/train.py and model/ranker/train.py via --specialist arg.
"""
import os
from typing import Callable, Optional
import logging

import numpy as np
import pandas as pd

from shared.class_tiers import add_class_tier_columns

logger = logging.getLogger(__name__)

VALID_SPECIALISTS = (
    "general",        # baseline — no filter, no weight
    "speed",          # weight: winner top-3 in race by speed_fig_vs_field
    "closer",         # weight: winner gained ≥4 pos from c2 to finish
    "class_riser",    # weight: winner has tier_delta ≥ +2
    "class_dropper",  # weight: winner has tier_delta ≤ −2
    "sprint",         # filter: distance_furlongs ≤ 7.0
    "route",          # filter: distance_furlongs > 7.0
    "gonzo_sauce",    # feature-set: lean53 + 14 Gonzo Sauce features (Phase A3)
)
FILTER_SPECIALISTS = ("sprint", "route")
WEIGHT_SPECIALISTS = ("speed", "closer", "class_riser", "class_dropper")
FEATURE_SET_SPECIALISTS = ("gonzo_sauce",)  # train on full pool, larger feature set
WEIGHT_VALUE = 3.0

DISPLAY_NAMES = {
    "general":       "General",
    "speed":         "Speed",
    "closer":        "Closer",
    "class_riser":   "Class Riser",
    "class_dropper": "Class Dropper",
    "sprint":        "Sprint",
    "route":         "Route",
    "gonzo_sauce":   "Gonzo Sauce",
}

CRITERION_DESCRIPTIONS = {
    "general":       "all races, equal weight (baseline)",
    "speed":         "3× sample weight on races where winner top-3 by speed_fig_vs_field rank",
    "closer":        "3× sample weight on races where winner has call_2_position − finish_position ≥ 4",
    "class_riser":   "3× sample weight on races where winner has tier_delta ≥ +2",
    "class_dropper": "3× sample weight on races where winner has tier_delta ≤ −2",
    "sprint":        "filter: distance_furlongs ≤ 7.0 only",
    "route":         "filter: distance_furlongs > 7.0 only",
    "gonzo_sauce":   "feature-set specialist: lean53 base + 14 Gonzo Sauce features (speed at distance, trajectory routes-only, class established) — trains on full race pool, no sample weighting",
}


def validate(specialist: str) -> str:
    """Return specialist if valid, else raise ValueError."""
    if specialist not in VALID_SPECIALISTS:
        raise ValueError(
            f"Unknown specialist {specialist!r}. "
            f"Valid: {VALID_SPECIALISTS}"
        )
    return specialist


def get_pp_filter(specialist: str) -> Optional[Callable[[pd.DataFrame], pd.DataFrame]]:
    """Return a callable that filters the loaded pps DataFrame, or None."""
    if specialist == "sprint":
        def _f(df):
            mask = df["distance_furlongs"] <= 7.0
            logger.info(f"[sprint] filtering pps: {len(df):,} → {int(mask.sum()):,} rows (≤7.0f)")
            return df[mask].reset_index(drop=True)
        return _f
    if specialist == "route":
        def _f(df):
            mask = df["distance_furlongs"] > 7.0
            logger.info(f"[route] filtering pps: {len(df):,} → {int(mask.sum()):,} rows (>7.0f)")
            return df[mask].reset_index(drop=True)
        return _f
    return None


def compute_sample_weights(
    features_df: pd.DataFrame,
    labels_df: pd.DataFrame,
    pps_df: pd.DataFrame,
    specialist: str,
) -> np.ndarray:
    """Return numpy weight array (default 1.0; 3.0 for rows in qualifying races).

    For general/sprint/route: returns all-1.0 (no weighting beyond the filter).
    """
    n = len(features_df)
    weights = np.ones(n, dtype=np.float32)
    if specialist in ("general",) + FILTER_SPECIALISTS + FEATURE_SET_SPECIALISTS:
        return weights

    if specialist == "speed":
        m = pd.DataFrame({
            "race_key":           labels_df["race_key"].values,
            "speed_fig_vs_field": features_df["speed_fig_vs_field"].values,
            "finish_position":    labels_df["finish_position"].values,
        })
        m["vs_field_rank"] = m.groupby("race_key")["speed_fig_vs_field"].rank(
            ascending=False, method="min"
        )
        winners = m[m["finish_position"] == 1]
        qual = set(winners.loc[winners["vs_field_rank"] <= 3, "race_key"])

    elif specialist == "closer":
        cls = pps_df.copy()
        cls["gain"] = cls["call_2_position"] - cls["finish_position"]
        cls["race_key"] = (
            cls["track_code"] + "_" +
            pd.to_datetime(cls["race_date"]).dt.strftime("%Y%m%d") + "_" +
            cls["race_number"].astype(str)
        )
        winners = cls[(cls["finish_position"] == 1) & (cls["gain"] >= 4)]
        qual = set(winners["race_key"])

    elif specialist in ("class_riser", "class_dropper"):
        tiered = add_class_tier_columns(pps_df)
        tiered["race_key"] = (
            tiered["track_code"] + "_" +
            pd.to_datetime(tiered["race_date"]).dt.strftime("%Y%m%d") + "_" +
            tiered["race_number"].astype(str)
        )
        winners = tiered[tiered["finish_position"] == 1]
        if specialist == "class_riser":
            winners = winners[winners["class_delta"] >= 2]
        else:
            winners = winners[winners["class_delta"] <= -2]
        qual = set(winners["race_key"])

    else:
        raise ValueError(f"unhandled specialist {specialist!r}")

    in_qual = labels_df["race_key"].isin(qual).values
    weights[in_qual] = WEIGHT_VALUE
    logger.info(
        f"[{specialist}] sample-weight: {len(qual):,} qualifying race_keys, "
        f"{int(in_qual.sum()):,}/{n:,} rows weighted at {WEIGHT_VALUE}× "
        f"(effective sample size: {float(weights.sum()):,.0f})"
    )
    return weights


def artifact_suffix(model_kind: str, specialist: str) -> str:
    """Compose version_suffix for save_artifacts.
       model_kind: 'wp_full', 'rk_full', 'pl_core', 'pl_workout'.
       specialist='general' → returns 'wp_full' (legacy-compatible).

       Reads env var LEAN_TAG (e.g. 'lean53'). When set, the tag is
       appended after the model_kind so artifacts are namespaced and
       coexist with prior galleries. Empty/unset → legacy behavior."""
    base = model_kind if specialist == "general" else f"{model_kind}_{specialist}"
    lean_tag = os.environ.get("LEAN_TAG", "").strip()
    if lean_tag:
        if specialist == "general":
            base = f"{model_kind}_{lean_tag}"
        else:
            base = f"{model_kind}_{lean_tag}_{specialist}"
    return base
