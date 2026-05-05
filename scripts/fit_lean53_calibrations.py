#!/usr/bin/env python3
"""Fit isotonic calibration heads for the 14 lean53 wp_full + pl_core
artifacts produced by Stream A2.4 (general + 6 specialists × 2 model
types). Ranker artifacts are SKIPPED — rank scores aren't probabilities.

Calibration set: April 1-14, 2026 (out-of-training, training cutoff
2025-12-31). Holdout April 15-26 reserved for diagnostic re-eval.

For each artifact:
  - wp_full_lean53_*: 53 features. Booster output is per-row binary
    win prob. Fit isotonic on (raw_prob, actual_win).
  - pl_core_lean53_*: 47 features. Booster output is EV score; converted
    to win prob via softmax-within-race. Fit isotonic on
    (post_softmax_win_prob, actual_win).

Outputs:
  /tmp/calibrations_lean53/<version>_calibration.json
  s3://equine-model-artifacts/win_prob/wp_full_lean53_*_calibration.json
  s3://equine-model-artifacts/pl/pl_core_lean53_*_calibration.json
"""
from __future__ import annotations
import json
import os
import re
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
from shared.feature_definitions import get_lean53_features, get_lean53_core_features

CAL_START = date(2026, 4, 1)
CAL_END   = date(2026, 4, 14)

SPECS = ['general', 'speed', 'closer', 'class_riser',
         'class_dropper', 'sprint', 'route']

LOCAL_DIR = "/tmp/calibrations_lean53"
os.makedirs(LOCAL_DIR, exist_ok=True)

S3 = boto3.client("s3")
BUCKET = "equine-model-artifacts"


def _download_s3(uri, dest):
    bucket, _, key = uri[5:].partition("/")
    S3.download_file(bucket, key, dest)


def _upload_s3(local, uri):
    bucket, _, key = uri[5:].partition("/")
    S3.upload_file(local, bucket, key)


def _find_artifact(prefix: str, kind: str, spec: str) -> tuple[str, str] | None:
    """Locate the most recent lean53 artifact for (kind, spec) on S3.
    Returns (version_name, s3_uri) or None."""
    # Naming: <kind>_lean53_<timestamp>.json or <kind>_lean53_<spec>_<timestamp>.json
    if spec == 'general':
        pattern = rf'^{kind}_lean53_\d{{8}}_\d{{4}}\.json$'
    else:
        pattern = rf'^{kind}_lean53_{spec}_\d{{8}}_\d{{4}}\.json$'
    paginator = S3.get_paginator('list_objects_v2')
    matches = []
    for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            name = key.rsplit('/', 1)[-1]
            if re.match(pattern, name):
                matches.append((obj['LastModified'], key, name))
    if not matches:
        return None
    matches.sort(reverse=True)  # most recent first
    _, key, name = matches[0]
    version = name.rsplit('.', 1)[0]
    return version, f"s3://{BUCKET}/{key}"


def _per_race_softmax(scores: np.ndarray, race_keys: pd.Series) -> np.ndarray:
    out = np.zeros_like(scores, dtype=float)
    df = pd.DataFrame({"score": scores, "rk": race_keys.values})
    for rk, group in df.groupby("rk"):
        s = group["score"].values.astype(float)
        shifted = s - s.max()
        exp_s = np.exp(shifted)
        probs = exp_s / exp_s.sum()
        out[group.index] = probs
    return out


def _calibration_table(probs, y_true, label=""):
    print(f"\n  Calibration deciles ({label}):")
    print(f"  {'decile':<14} {'N':>6} {'mean_pred':>10} "
          f"{'obs_rate':>10} {'delta':>8}")
    for lo, hi in [(0.0,0.1),(0.1,0.2),(0.2,0.3),(0.3,0.4),
                   (0.4,0.5),(0.5,0.6),(0.6,0.7),(0.7,0.8),
                   (0.8,0.9),(0.9,1.001)]:
        mask = (probs >= lo) & (probs < hi)
        n = int(mask.sum())
        if n == 0: continue
        mp = float(probs[mask].mean())
        obs = float(y_true[mask].mean())
        delta = obs - mp
        print(f"  [{lo:.1f}, {hi:.1f})  {n:>6,} {mp*100:>9.2f}% "
              f"{obs*100:>9.2f}% {delta*100:>+7.2f}pp")


def fit_one(kind, spec, version, s3_uri, features_df, labels_df,
            feat_names, apply_softmax: bool):
    print(f"\n{'─'*72}")
    print(f"Fitting calibration: {kind}_{spec} = {version}  ({len(feat_names)} feats)")
    print(f"{'─'*72}")

    labels_df = labels_df.copy()
    labels_df["race_date"] = pd.to_datetime(labels_df["race_date"])
    mask = ((labels_df["race_date"].dt.date >= CAL_START) &
            (labels_df["race_date"].dt.date <= CAL_END))

    feat_cal = features_df.loc[mask.values].reset_index(drop=True)
    lab_cal  = labels_df[mask].reset_index(drop=True)
    print(f"  cal window rows: {len(feat_cal):,} × "
          f"{lab_cal['race_key'].nunique():,} races")

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        local_model = f.name
    _download_s3(s3_uri, local_model)
    booster = xgb.Booster()
    booster.load_model(local_model)

    X = feat_cal[feat_names].values.astype(np.float32)
    dm = xgb.DMatrix(X, feature_names=feat_names)
    raw = booster.predict(dm)

    if apply_softmax:
        raw = _per_race_softmax(raw, lab_cal["race_key"])

    y_true = (lab_cal["finish_position"].values == 1).astype(float)
    n_winners = int(y_true.sum())
    print(f"  winners: {n_winners:,} / {len(y_true):,}  "
          f"({100*n_winners/max(len(y_true),1):.2f}%)")

    if n_winners < 30 or len(y_true) < 200:
        print(f"  ⚠ insufficient calibration set; SKIP")
        return None

    _calibration_table(raw, y_true, "pre-fit")

    iso = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
    iso.fit(raw, y_true)

    cal = iso.predict(raw)
    _calibration_table(cal, y_true, "post-fit (sanity)")

    artifact = {
        "model_version": version,
        "model_type": f"{kind}_{spec}",
        "specialist": spec,
        "feature_set": "lean53" if kind == "wp_full" else "lean53_core",
        "n_features": len(feat_names),
        "fit_window": {"start": CAL_START.isoformat(),
                       "end":   CAL_END.isoformat()},
        "n_samples": int(len(raw)),
        "n_winners": n_winners,
        "x_thresholds": iso.X_thresholds_.tolist(),
        "y_thresholds": iso.y_thresholds_.tolist(),
        "method": "sklearn.isotonic.IsotonicRegression("
                  "out_of_bounds='clip', y_min=0.0, y_max=1.0)",
        "applied_softmax_pre_isotonic": apply_softmax,
        "fit_at": datetime.utcnow().isoformat() + "Z",
    }
    out_local = f"{LOCAL_DIR}/{version}_calibration.json"
    with open(out_local, "w") as f:
        json.dump(artifact, f, indent=2)

    s3_calib = s3_uri.replace(".json", "_calibration.json")
    _upload_s3(out_local, s3_calib)
    print(f"  ✓ saved {out_local}")
    print(f"  ✓ uploaded {s3_calib}")
    return artifact


def main():
    print("=" * 72)
    print("STREAM A2.5 — Fit isotonic calibration for 14 lean53 wp+pl artifacts")
    print(f"  calibration set: {CAL_START} → {CAL_END}")
    print("=" * 72)

    print("\nBuilding 2026 feature matrix...", flush=True)
    conn = _get_conn()
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2026, end_year=2026, include_odds=True,
    )
    conn.close()
    print(f"  full 2026 matrix: {len(features_df):,} rows")

    wp_features = get_lean53_features()        # 53
    pl_features = get_lean53_core_features()   # 47

    summary = []
    for spec in SPECS:
        # WP
        wp = _find_artifact("win_prob/", "wp_full", spec)
        if wp:
            v, s3 = wp
            r = fit_one("wp_full", spec, v, s3, features_df, labels_df,
                        wp_features, apply_softmax=False)
            if r: summary.append(("wp", spec, v, len(r["x_thresholds"])))
        else:
            print(f"  ⚠ no wp_full lean53 artifact found for {spec}")

        # PL
        pl = _find_artifact("pl/", "pl_core", spec)
        if pl:
            v, s3 = pl
            r = fit_one("pl_core", spec, v, s3, features_df, labels_df,
                        pl_features, apply_softmax=True)
            if r: summary.append(("pl", spec, v, len(r["x_thresholds"])))
        else:
            print(f"  ⚠ no pl_core lean53 artifact found for {spec}")

    print()
    print("=" * 72)
    print(f"DONE — {len(summary)} lean53 calibrations fit + uploaded")
    print("=" * 72)
    for kind, spec, ver, n_thresh in summary:
        print(f"  {kind}_{spec:<14} {ver:<48} "
              f"{n_thresh} thresholds")


if __name__ == "__main__":
    main()
