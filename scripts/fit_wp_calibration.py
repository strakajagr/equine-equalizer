#!/usr/bin/env python3
"""Fit isotonic calibration head for wp_full_20260429_0244.

Calibration set: April 1-14, 2026 (out-of-training-data, training cutoff
was 2025-12-31). Holdout for diagnostic re-eval is April 15-26 — kept
separate from the calibration fit.

Outputs:
  /tmp/wp_full_general_calibration.json (local)
  s3://equine-model-artifacts/win_prob/wp_full_20260429_0244_calibration.json (live)

JSON shape:
  {
    "model_version": "wp_full_20260429_0244",
    "fit_window": {"start": "2026-04-01", "end": "2026-04-14"},
    "n_samples": <int>,
    "n_winners": <int>,
    "x_thresholds": [...]  // raw predicted probabilities
    "y_thresholds": [...]  // calibrated win probabilities
    "method": "sklearn.isotonic.IsotonicRegression(out_of_bounds=clip)",
    "fit_at": "<isoformat>"
  }

Usage:
  python3 scripts/fit_wp_calibration.py
"""
from __future__ import annotations
import json
import sys
import tempfile
from datetime import date, datetime

import boto3
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.isotonic import IsotonicRegression

sys.path.insert(0, "/home/strakajagr/projects/equine-equalizer/model")
from shared.data_loader import _get_conn, build_feature_matrix
from shared.feature_definitions import get_feature_names

WP_FULL_S3 = "s3://equine-model-artifacts/win_prob/wp_full_20260429_0244.json"
CAL_S3_OUT = (
    "s3://equine-model-artifacts/win_prob/"
    "wp_full_20260429_0244_calibration.json"
)
CAL_LOCAL = "/tmp/wp_full_general_calibration.json"

CAL_START = date(2026, 4, 1)
CAL_END   = date(2026, 4, 14)


def _download_s3(uri, dest):
    bucket, _, key = uri[5:].partition("/")
    boto3.client("s3").download_file(bucket, key, dest)


def _upload_s3(local, uri):
    bucket, _, key = uri[5:].partition("/")
    boto3.client("s3").upload_file(local, bucket, key)


def main():
    print("=" * 72)
    print("Fit isotonic calibration — wp_full_20260429_0244")
    print(f"  calibration set: {CAL_START} → {CAL_END}")
    print("=" * 72)

    # Load model
    print("\nLoading wp_full booster...", flush=True)
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        local_model = f.name
    _download_s3(WP_FULL_S3, local_model)
    booster = xgb.Booster()
    booster.load_model(local_model)

    # Build features for 2026, slice to calibration window
    print("Building 2026 feature matrix...", flush=True)
    conn = _get_conn()
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2026, end_year=2026, include_odds=True,
    )
    conn.close()
    labels_df["race_date"] = pd.to_datetime(labels_df["race_date"])
    mask = (
        (labels_df["race_date"].dt.date >= CAL_START)
        & (labels_df["race_date"].dt.date <= CAL_END)
    )
    feat_cal = features_df.loc[mask.values].reset_index(drop=True)
    lab_cal  = labels_df[mask].reset_index(drop=True)
    print(f"  calibration set: {len(feat_cal):,} entries × "
          f"{lab_cal['race_key'].nunique():,} races")

    if len(feat_cal) < 500:
        print(f"⚠ calibration set is small (<500 rows). Aborting.")
        sys.exit(2)

    # Predict raw probabilities
    feat_names = get_feature_names(include_odds=True)
    X = feat_cal[feat_names].values.astype(np.float32)
    dm = xgb.DMatrix(X, feature_names=feat_names)
    raw_probs = booster.predict(dm)

    # Binary win label (settled outcomes)
    y_true = (lab_cal["finish_position"].values == 1).astype(float)
    n_winners = int(y_true.sum())
    print(f"  winners in calibration set: {n_winners:,} / {len(y_true):,}  "
          f"({100 * n_winners / len(y_true):.2f}%)")

    # Pre-fit calibration table
    print("\nPre-fit calibration deciles:")
    print(f"  {'decile':<14} {'N':>6} {'mean_pred':>10} {'obs_rate':>10} {'delta':>8}")
    for lo, hi in [(0.0, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4),
                   (0.4, 0.5), (0.5, 0.6), (0.6, 0.7), (0.7, 0.8),
                   (0.8, 0.9), (0.9, 1.001)]:
        sub_mask = (raw_probs >= lo) & (raw_probs < hi)
        n = int(sub_mask.sum())
        if n == 0:
            continue
        mean_pred = float(raw_probs[sub_mask].mean())
        obs = float(y_true[sub_mask].mean())
        delta = obs - mean_pred
        print(f"  [{lo:.1f}, {hi:.1f})  {n:>6,} {mean_pred*100:>9.2f}% "
              f"{obs*100:>9.2f}% {delta*100:>+7.2f}pp")

    # Fit isotonic regression
    print("\nFitting IsotonicRegression(out_of_bounds='clip')...", flush=True)
    iso = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
    iso.fit(raw_probs, y_true)
    print(f"  X thresholds count: {len(iso.X_thresholds_):,}")
    print(f"  Y thresholds range: "
          f"[{iso.y_thresholds_.min():.4f}, {iso.y_thresholds_.max():.4f}]")

    # Apply calibration on the fit set and re-check decile alignment
    cal_probs = iso.predict(raw_probs)
    print("\nPost-fit calibration deciles (on fit set — sanity):")
    print(f"  {'decile':<14} {'N':>6} {'mean_pred':>10} {'obs_rate':>10} {'delta':>8}")
    for lo, hi in [(0.0, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4),
                   (0.4, 0.5), (0.5, 0.6), (0.6, 0.7), (0.7, 0.8),
                   (0.8, 0.9), (0.9, 1.001)]:
        sub_mask = (cal_probs >= lo) & (cal_probs < hi)
        n = int(sub_mask.sum())
        if n == 0:
            continue
        mean_pred = float(cal_probs[sub_mask].mean())
        obs = float(y_true[sub_mask].mean())
        delta = obs - mean_pred
        print(f"  [{lo:.1f}, {hi:.1f})  {n:>6,} {mean_pred*100:>9.2f}% "
              f"{obs*100:>9.2f}% {delta*100:>+7.2f}pp")

    # Save artifact
    artifact = {
        "model_version": "wp_full_20260429_0244",
        "fit_window": {
            "start": CAL_START.isoformat(),
            "end": CAL_END.isoformat(),
        },
        "n_samples": int(len(raw_probs)),
        "n_winners": n_winners,
        "x_thresholds": iso.X_thresholds_.tolist(),
        "y_thresholds": iso.y_thresholds_.tolist(),
        "method": "sklearn.isotonic.IsotonicRegression("
                  "out_of_bounds='clip', y_min=0.0, y_max=1.0)",
        "fit_at": datetime.utcnow().isoformat() + "Z",
    }
    with open(CAL_LOCAL, "w") as f:
        json.dump(artifact, f, indent=2)
    print(f"\nWrote {CAL_LOCAL} ({len(json.dumps(artifact)):,} bytes)")

    _upload_s3(CAL_LOCAL, CAL_S3_OUT)
    print(f"Uploaded {CAL_S3_OUT}")


if __name__ == "__main__":
    main()
