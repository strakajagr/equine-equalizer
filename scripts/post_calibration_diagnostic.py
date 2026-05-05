#!/usr/bin/env python3
"""Post-calibration diagnostic — runs the 4-check on the April 15-26
HOLDOUT, applying the fitted isotonic calibration after raw model
prediction.

For wp_full_general specifically: full 4 checks (ROI by ML bucket
per-pick view, calibration table, Derby R12 sanity).

For the other 13 artifacts: calibration-table only (the only check
that materially changes — isotonic preserves rank, so per-pick ROI
and rankings are unchanged).
"""
from __future__ import annotations
import json
import sys
import tempfile
from datetime import date

import boto3
import numpy as np
import pandas as pd
import xgboost as xgb
import psycopg2
from psycopg2.extras import RealDictCursor

sys.path.insert(0, "/home/strakajagr/projects/equine-equalizer/model")
from shared.data_loader import _get_conn, build_feature_matrix
from shared.feature_definitions import get_feature_names, get_core_features

HOLD_START = date(2026, 4, 15)
HOLD_END   = date(2026, 4, 26)

ML_BUCKETS = [
    (0.0, 3.0,    "0-3.0     (chalk)"),
    (3.0, 6.0,    "3.0-6.0   (vague fav)"),
    (6.0, 12.0,   "6.0-12.0  (mid)"),
    (12.0, 25.0,  "12.0-25.0 (overlay)"),
    (25.0, 1e9,   "25.0+     (deep ls)"),
]


def _download(uri, dest):
    bucket, _, key = uri[5:].partition("/")
    boto3.client("s3").download_file(bucket, key, dest)


def _load_booster(uri):
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        local = f.name
    _download(uri, local)
    b = xgb.Booster()
    b.load_model(local)
    return b


def _load_cal(uri):
    """Load calibration JSON. Returns (x_thresholds, y_thresholds) for
    isotonic apply via np.interp."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        local = f.name
    _download(uri, local)
    d = json.load(open(local))
    return np.array(d["x_thresholds"]), np.array(d["y_thresholds"])


def _apply_iso(raw, xt, yt):
    """Replicate IsotonicRegression(out_of_bounds='clip').predict via interp."""
    return np.clip(np.interp(raw, xt, yt), 0.0, 1.0)


def _per_race_softmax(scores, race_keys):
    out = np.zeros_like(scores, dtype=float)
    df = pd.DataFrame({"score": scores, "rk": race_keys.values})
    for rk, group in df.groupby("rk"):
        s = group["score"].values.astype(float)
        shifted = s - s.max()
        out[group.index] = np.exp(shifted) / np.exp(shifted).sum()
    return out


def _ml_bucket(ml):
    if ml is None: return None
    for lo, hi, label in ML_BUCKETS:
        if lo <= ml < hi: return label
    return None


def _calibration_deltas_summary(probs, y_true) -> str:
    """Compact one-line summary: max abs delta, mean abs delta, P(>5pp)."""
    deltas = []
    for lo, hi in [(0.0,0.1),(0.1,0.2),(0.2,0.3),(0.3,0.4),
                   (0.4,0.5),(0.5,0.6),(0.6,0.7),(0.7,0.8),
                   (0.8,0.9),(0.9,1.001)]:
        mask = (probs >= lo) & (probs < hi)
        n = int(mask.sum())
        if n == 0: continue
        mp = float(probs[mask].mean())
        obs = float(y_true[mask].mean())
        deltas.append(abs(obs - mp))
    if not deltas:
        return "—"
    max_d = max(deltas) * 100
    mean_d = (sum(deltas) / len(deltas)) * 100
    over5 = sum(1 for d in deltas if d > 0.05)
    return f"max={max_d:>5.1f}pp  mean={mean_d:>5.1f}pp  buckets>5pp={over5}/{len(deltas)}"


def _calibration_full(probs, y_true, label):
    print(f"\n  Calibration ({label}):")
    print(f"  {'decile':<14} {'N':>6} {'mean_pred':>10} {'obs':>10} {'delta':>9}")
    for lo, hi in [(0.0,0.1),(0.1,0.2),(0.2,0.3),(0.3,0.4),
                   (0.4,0.5),(0.5,0.6),(0.6,0.7),(0.7,0.8),
                   (0.8,0.9),(0.9,1.001)]:
        mask = (probs >= lo) & (probs < hi)
        n = int(mask.sum())
        if n == 0:
            continue
        mp = float(probs[mask].mean())
        obs = float(y_true[mask].mean())
        delta = obs - mp
        print(f"  [{lo:.1f}, {hi:.1f})  {n:>6,} {mp*100:>9.2f}% "
              f"{obs*100:>9.2f}% {delta*100:>+8.2f}pp")


def _per_pick_roi(probs, labels_df, ml_map, label):
    df = labels_df.copy()
    df["pred"] = probs
    df["ml"] = df.apply(lambda r: ml_map.get((
        r["track_code"], pd.Timestamp(r["race_date"]).date(),
        int(r["race_number"]), r["horse_id"])), axis=1)
    df = df[df["ml"].notna()]
    df["bucket"] = df["ml"].apply(_ml_bucket)
    df["rank"] = df.groupby("race_key")["pred"].rank(ascending=False, method="first")
    top1 = df[df["rank"] == 1]
    n_races = df["race_key"].nunique()
    print(f"\n  Per-pick ROI ({label}, races={n_races}):")
    print(f"  {'bucket':<26} {'N':>5} {'wins':>5} {'hit':>8} "
          f"{'avg_ml':>7} {'roi':>9} {'net':>10}")
    for _, _, lbl in ML_BUCKETS:
        sub = top1[top1["bucket"] == lbl]
        n = len(sub)
        if n == 0:
            print(f"  {lbl:<26} {0:>5} {0:>5} {'—':>8} "
                  f"{'—':>7} {'—':>9} {'—':>10}")
            continue
        wins = int((sub["finish_position"] == 1).sum())
        hit = wins / n
        avg_ml = float(sub["ml"].mean())
        net = sum((2.0 * r["ml"] if r["finish_position"] == 1 else -2.0)
                  for _, r in sub.iterrows())
        roi = net / (n * 2.0)
        print(f"  {lbl:<26} {n:>5} {wins:>5} "
              f"{hit*100:>7.2f}% {avg_ml:>7.2f} "
              f"{roi*100:>+8.2f}% ${net:>+9.2f}")


def _connect_secrets():
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    sec = json.loads(sm.get_secret_value(
        SecretId="equine-equalizer/db-credentials")["SecretString"])
    return psycopg2.connect(
        host=sec["host"], port=sec["port"], dbname=sec["dbname"],
        user=sec["username"], password=sec["password"],
        cursor_factory=RealDictCursor)


def _ml_map(conn, start, end):
    cur = conn.cursor()
    cur.execute(
        "SELECT t.track_code, r.race_date, r.race_number, e.horse_id, "
        "e.morning_line_odds FROM entries e JOIN races r ON r.race_id=e.race_id "
        "JOIN tracks t ON t.track_id = r.track_id "
        "WHERE r.race_date BETWEEN %s AND %s",
        (start, end))
    out = {}
    for r in cur.fetchall():
        if r["morning_line_odds"] is not None:
            out[(r["track_code"], r["race_date"], int(r["race_number"]),
                 str(r["horse_id"]))] = float(r["morning_line_odds"])
    return out


def _active_artifacts():
    conn = _connect_secrets()
    cur = conn.cursor()
    types = []
    for spec in ['general','speed','closer','class_riser',
                 'class_dropper','sprint','route']:
        types.append(f"wp_full_{spec}")
        types.append(f"pl_core_{spec}")
    cur.execute(
        "SELECT model_type, version_name, s3_artifact_path FROM model_versions "
        "WHERE model_type = ANY(%s) AND is_active = TRUE", (types,))
    out = {}
    for r in cur.fetchall():
        out[r['model_type']] = (r['version_name'], r['s3_artifact_path'])
    cur.close(); conn.close()
    return out


def main():
    print("=" * 80)
    print("POST-CALIBRATION DIAGNOSTIC — holdout April 15-26, 2026")
    print("=" * 80)

    active = _active_artifacts()
    conn = _get_conn()
    print("\nBuilding 2026 feature matrix...", flush=True)
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2026, end_year=2026, include_odds=True)
    labels_df["race_date"] = pd.to_datetime(labels_df["race_date"])
    mask = ((labels_df["race_date"].dt.date >= HOLD_START) &
            (labels_df["race_date"].dt.date <= HOLD_END))
    feat_h = features_df.loc[mask.values].reset_index(drop=True)
    lab_h = labels_df[mask].reset_index(drop=True)
    print(f"  holdout rows: {len(feat_h):,}")

    print("Loading ML map...", flush=True)
    ml_map = _ml_map(conn, HOLD_START, HOLD_END)

    wp_features = get_feature_names(include_odds=True)
    pl_features = get_core_features(include_odds=True)
    Xwp = feat_h[wp_features].values.astype(np.float32)
    Xpl = feat_h[pl_features].values.astype(np.float32)
    dwp = xgb.DMatrix(Xwp, feature_names=wp_features)
    dpl = xgb.DMatrix(Xpl, feature_names=pl_features)
    y_true = (lab_h["finish_position"].values == 1).astype(float)

    # ==== Full 4-check: wp_full_general ====
    v_wp_g, s3_wp_g = active["wp_full_general"]
    s3_wp_g_cal = s3_wp_g.replace(".json", "_calibration.json")
    print(f"\n{'═'*80}")
    print(f"FULL 4-CHECK — wp_full_general ({v_wp_g})")
    print(f"{'═'*80}")
    booster = _load_booster(s3_wp_g)
    raw = booster.predict(dwp)
    xt, yt = _load_cal(s3_wp_g_cal)
    cal = _apply_iso(raw, xt, yt)

    print(f"\n[Check 3] Calibration deciles — pre-cal vs post-cal on holdout:")
    _calibration_full(raw, y_true, "PRE-cal (raw)")
    _calibration_full(cal, y_true, "POST-cal (calibrated)")

    print(f"\n[Check 1b] Per-pick ROI — pre vs post (top-1 ranking unchanged "
          "because isotonic is monotonic; values shown for completeness):")
    _per_pick_roi(raw, lab_h, ml_map, "PRE-cal")
    _per_pick_roi(cal, lab_h, ml_map, "POST-cal")

    # Derby R12 — score directly with calibration applied
    print(f"\n[Check 4] Derby R12 (CD 2026-05-02) — calibrated edges:")
    print("  (showing top-10 picks by calibrated win-prob)")
    cur = conn.cursor()
    cur.execute("""
      SELECT e.entry_id, e.program_number, h.horse_name,
             e.morning_line_odds, p.predicted_rank, p.win_probability,
             p.raw_win_prob, p.morning_line_implied_prob
      FROM wr_predictions p
      JOIN entries e ON e.entry_id = p.entry_id
      JOIN horses h ON h.horse_id = e.horse_id
      JOIN races r ON r.race_id = p.race_id
      JOIN tracks t ON t.track_id = r.track_id
      WHERE t.track_code='CD' AND r.race_date='2026-05-02'
        AND r.race_number=12 AND p.style='general'
      ORDER BY p.predicted_rank ASC
    """)
    print(f"  {'pgm':>3} {'horse':<22} {'ML':>5} {'raw':>7} {'cal':>7} "
          f"{'cal_edge':>9}")
    for r in cur.fetchall():
        ml = float(r['morning_line_odds']) if r['morning_line_odds'] else None
        ml_imp = 1.0/(ml+1.0) if ml else 0.0
        raw_p = float(r['raw_win_prob'] or 0)
        cal_p = float(_apply_iso(np.array([raw_p]), xt, yt)[0])
        edge = cal_p - ml_imp
        print(f"  {r['program_number']:>3} "
              f"{(r['horse_name'] or '?')[:22]:<22} "
              f"{(f'{ml:.1f}' if ml else '—'):>5} "
              f"{raw_p*100:>6.2f}% {cal_p*100:>6.2f}% "
              f"{edge*100:>+8.2f}%")

    # ==== Calibration-table summary across all 14 ====
    print(f"\n{'═'*80}")
    print(f"CALIBRATION SUMMARY — all 14 artifacts on holdout")
    print(f"{'═'*80}")
    print(f"  {'model_type':<24} {'PRE-cal':<48} {'POST-cal':<48}")
    rows_summary = []
    for model_type in sorted(active.keys()):
        version, s3 = active[model_type]
        s3_cal = s3.replace(".json", "_calibration.json")
        booster = _load_booster(s3)
        if model_type.startswith("wp_full"):
            raw = booster.predict(dwp)
        else:
            raw = booster.predict(dpl)
            raw = _per_race_softmax(raw, lab_h["race_key"])
        xt, yt = _load_cal(s3_cal)
        cal = _apply_iso(raw, xt, yt)
        pre_summary  = _calibration_deltas_summary(raw,  y_true)
        post_summary = _calibration_deltas_summary(cal, y_true)
        print(f"  {model_type:<24}")
        print(f"    PRE  : {pre_summary}")
        print(f"    POST : {post_summary}")
        rows_summary.append((model_type, pre_summary, post_summary))

    cur.close(); conn.close()
    print(f"\n{'═'*80}")
    print("DIAGNOSTIC COMPLETE")
    print(f"{'═'*80}")


if __name__ == "__main__":
    main()
