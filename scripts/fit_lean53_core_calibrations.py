#!/usr/bin/env python3
"""Fit isotonic calibration heads for the 7 wp_core lean53 artifacts.

Calibration set: April 1-14, 2026. Same approach as fit_lean53_calibrations.py
but for the 47-feature wp_core lean53 (no workout filter).
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
from shared.feature_definitions import get_lean53_core_features

CAL_START = date(2026, 4, 1)
CAL_END   = date(2026, 4, 14)
SPECS = ['general', 'speed', 'closer', 'class_riser',
         'class_dropper', 'sprint', 'route']
LOCAL_DIR = "/tmp/calibrations_lean53_core"
os.makedirs(LOCAL_DIR, exist_ok=True)
S3 = boto3.client("s3")
BUCKET = "equine-model-artifacts"


def _download(uri, dest):
    bucket, _, key = uri[5:].partition("/")
    S3.download_file(bucket, key, dest)


def _upload(local, uri):
    bucket, _, key = uri[5:].partition("/")
    S3.upload_file(local, bucket, key)


def _find_artifact(spec: str):
    if spec == 'general':
        pat = r'^wp_core_lean53_\d{8}_\d{4}\.json$'
    else:
        pat = rf'^wp_core_lean53_{spec}_\d{{8}}_\d{{4}}\.json$'
    paginator = S3.get_paginator('list_objects_v2')
    matches = []
    for page in paginator.paginate(Bucket=BUCKET, Prefix='win_prob/'):
        for obj in page.get('Contents', []):
            name = obj['Key'].rsplit('/', 1)[-1]
            if re.match(pat, name):
                matches.append((obj['LastModified'], obj['Key'], name))
    if not matches:
        return None
    matches.sort(reverse=True)
    _, key, name = matches[0]
    return name.rsplit('.', 1)[0], f"s3://{BUCKET}/{key}"


def _calibration_table(probs, y_true, label=""):
    print(f"\n  Calibration deciles ({label}):")
    print(f"  {'decile':<14} {'N':>6} {'mean_pred':>10} "
          f"{'obs_rate':>10} {'delta':>8}")
    for lo, hi in [(0.0,0.1),(0.1,0.2),(0.2,0.3),(0.3,0.4),
                   (0.4,0.5),(0.5,0.6),(0.6,0.7),(0.7,0.8),
                   (0.8,0.9),(0.9,1.001)]:
        m = (probs >= lo) & (probs < hi)
        n = int(m.sum())
        if n == 0: continue
        mp = float(probs[m].mean())
        obs = float(y_true[m].mean())
        delta = obs - mp
        print(f"  [{lo:.1f}, {hi:.1f})  {n:>6,} {mp*100:>9.2f}% "
              f"{obs*100:>9.2f}% {delta*100:>+7.2f}pp")


def fit_one(spec, version, s3_uri, features_df, labels_df, feat_names):
    print(f"\n{'─'*72}")
    print(f"Fitting calibration: wp_core_{spec} = {version}  ({len(feat_names)} feats)")
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
        local = f.name
    _download(s3_uri, local)
    booster = xgb.Booster()
    booster.load_model(local)

    X = feat_cal[feat_names].values.astype(np.float32)
    dm = xgb.DMatrix(X, feature_names=feat_names)
    raw = booster.predict(dm)

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
    _calibration_table(cal, y_true, "post-fit")

    artifact = {
        "model_version": version,
        "model_type": f"win_prob_core_{spec}",
        "specialist": spec,
        "feature_set": "lean53_core",
        "n_features": len(feat_names),
        "fit_window": {"start": CAL_START.isoformat(), "end": CAL_END.isoformat()},
        "n_samples": int(len(raw)), "n_winners": n_winners,
        "x_thresholds": iso.X_thresholds_.tolist(),
        "y_thresholds": iso.y_thresholds_.tolist(),
        "method": "sklearn.isotonic.IsotonicRegression(out_of_bounds='clip', y_min=0.0, y_max=1.0)",
        "applied_softmax_pre_isotonic": False,
        "fit_at": datetime.utcnow().isoformat() + "Z",
    }
    out_local = f"{LOCAL_DIR}/{version}_calibration.json"
    with open(out_local, "w") as f:
        json.dump(artifact, f, indent=2)
    s3_calib = s3_uri.replace(".json", "_calibration.json")
    _upload(out_local, s3_calib)
    print(f"  ✓ saved + uploaded {s3_calib}")
    return artifact


def main():
    print("=" * 72)
    print("Stream A2.9 — Fit isotonic calibration for 7 wp_core lean53 artifacts")
    print(f"  calibration set: {CAL_START} → {CAL_END}")
    print("=" * 72)

    print("\nBuilding 2026 feature matrix...", flush=True)
    conn = _get_conn()
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2026, end_year=2026, include_odds=True,
    )
    conn.close()
    print(f"  full 2026 matrix: {len(features_df):,} rows")

    feat_core = get_lean53_core_features()
    summary = []
    for spec in SPECS:
        found = _find_artifact(spec)
        if not found:
            print(f"  ⚠ no wp_core lean53 artifact found for {spec}")
            continue
        v, s3 = found
        r = fit_one(spec, v, s3, features_df, labels_df, feat_core)
        if r: summary.append((spec, v, len(r["x_thresholds"])))

    print()
    print("=" * 72)
    print(f"DONE — {len(summary)} calibrations fit + uploaded")
    print("=" * 72)
    for spec, ver, n in summary:
        print(f"  wp_core_{spec:<14} {ver:<48} {n} thresholds")


if __name__ == "__main__":
    main()
