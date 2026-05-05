#!/usr/bin/env python3
"""Phase 1 holdout comparison: NEW (clean-data baseline) vs CURRENT
(production) artifacts on the April-15-26 holdout window.

The April 15-26 dates are *inside* the training corpus the production
artifacts saw (training cutoff 2025-12-31). The new artifacts have the
same training cutoff. Difference between them is only the data
correction work (dedup'd horses, race_type backfill, populated grade
column, race_name/conditions backfill from chart re-parse). So this
comparison directly tests whether the data corrections improve
predictive ability on a settled-outcomes window.

Usage:
  python3 scripts/phase1_holdout_compare.py \\
    --new-wp     s3://equine-model-artifacts/win_prob/wp_full_20260429_0244.json \\
    --current-wp s3://equine-model-artifacts/win_prob/wp_full_20260428_0444.json \\
    --new-rk     s3://equine-model-artifacts/ranker/rk_full_20260429_0318.json \\
    --current-rk s3://equine-model-artifacts/ranker/rk_full_lean51_20260428_1447.json \\
    --start-date 2026-04-15 \\
    --end-date   2026-04-26 \\
    --tracks     all
"""
from __future__ import annotations
import argparse
import json
import math
import os
import sys
import tempfile
import time
from datetime import date

import boto3
import numpy as np
import pandas as pd
import xgboost as xgb

sys.path.insert(0, "/home/strakajagr/projects/equine-equalizer/model")
from shared.data_loader import _get_conn, build_feature_matrix
from shared.feature_definitions import (
    get_feature_names, get_ranker_full_features,
)


def _download_s3(uri: str, dest: str) -> None:
    assert uri.startswith("s3://")
    bucket, _, key = uri[5:].partition("/")
    boto3.client("s3").download_file(bucket, key, dest)


def _load_booster(s3_uri: str) -> xgb.Booster:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        local = f.name
    _download_s3(s3_uri, local)
    booster = xgb.Booster()
    booster.load_model(local)
    return booster


def _load_meta(s3_uri: str) -> dict:
    """Best-effort: download the *_meta.json sidecar if present."""
    meta_uri = s3_uri.replace(".json", "_meta.json", 1)
    try:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            local = f.name
        _download_s3(meta_uri, local)
        with open(local) as fh:
            return json.load(fh)
    except Exception:
        return {}


def _load_morning_line_odds(conn, race_keys: list[str]) -> dict:
    """Build {(track, date, race_number, horse_id): morning_line_odds}.
    Used for ROI computation."""
    if not race_keys:
        return {}
    sql = """
      SELECT t.track_code, r.race_date, r.race_number,
             e.horse_id, e.morning_line_odds
      FROM entries e
      JOIN races r  ON r.race_id  = e.race_id
      JOIN tracks t ON t.track_id = r.track_id
      WHERE r.race_date BETWEEN %s AND %s
    """
    # Min/max race_date from race_keys (format: TRACK_YYYYMMDD_RACENUM)
    dates = [k.split("_")[1] for k in race_keys]
    min_d = f"{min(dates)[:4]}-{min(dates)[4:6]}-{min(dates)[6:8]}"
    max_d = f"{max(dates)[:4]}-{max(dates)[4:6]}-{max(dates)[6:8]}"
    cur = conn.cursor()
    cur.execute(sql, (min_d, max_d))
    out = {}
    for r in cur.fetchall():
        if r["morning_line_odds"] is not None:
            key = (r["track_code"], r["race_date"], r["race_number"],
                   str(r["horse_id"]))
            out[key] = float(r["morning_line_odds"])
    return out


def _filter_holdout(
    features_df: pd.DataFrame,
    labels_df: pd.DataFrame,
    start_date: date,
    end_date: date,
    tracks: list[str] | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Slice the feature/label DataFrames to the holdout window."""
    mask = ((labels_df["race_date"].dt.date >= start_date) &
            (labels_df["race_date"].dt.date <= end_date))
    if tracks:
        mask &= labels_df["track_code"].isin(tracks)
    sub_lab = labels_df[mask].reset_index(drop=True)
    sub_feat = features_df.loc[mask.values].reset_index(drop=True)
    return sub_feat, sub_lab


def _ndcg_at_k(actual_finish: np.ndarray, predicted_score: np.ndarray, k: int = 5) -> float:
    """NDCG@k for a single race. rank label = max(field_size, k) - finish_pos
    for in-the-money (top 3); 0 otherwise."""
    n = len(actual_finish)
    if n == 0:
        return 0.0
    # Relevance: 4 for win, 3 for place, 2 for show, 0 otherwise
    rel = np.zeros(n)
    for i, f in enumerate(actual_finish):
        if f == 1:
            rel[i] = 4
        elif f == 2:
            rel[i] = 3
        elif f == 3:
            rel[i] = 2

    def dcg(order_idx, k_):
        s = 0.0
        for i, idx in enumerate(order_idx[:k_]):
            s += (2 ** rel[idx] - 1) / math.log2(i + 2)
        return s

    pred_order = np.argsort(-predicted_score)
    ideal_order = np.argsort(-rel)
    idcg = dcg(ideal_order, k)
    if idcg == 0:
        return 0.0
    return dcg(pred_order, k) / idcg


def _per_race_metrics(
    labels: pd.DataFrame,
    pred_scores: np.ndarray,
    morning_line_map: dict | None,
    is_win_prob: bool,
) -> dict:
    """Compute per-race-then-aggregated metrics."""
    df = labels.copy()
    df["pred_score"] = pred_scores
    df["pred_rank"] = df.groupby("race_key")["pred_score"].rank(
        ascending=False, method="first"
    )

    # Top-1 hit rate
    top1 = df[df["pred_rank"] == 1]
    top1_hit_rate = float((top1["finish_position"] == 1).mean()) if len(top1) else 0.0

    # Top-3 hit rate: did the actual winner (finish=1) appear in the
    # predicted top-3?
    actual_winners = df[df["finish_position"] == 1][["race_key", "horse_id"]]
    pred_top3 = df[df["pred_rank"] <= 3][["race_key", "horse_id"]]
    merged = actual_winners.merge(
        pred_top3, on=["race_key", "horse_id"], how="left", indicator=True,
    )
    # _merge=='both' -> winner was in predicted top-3
    top3_hit_rate = float((merged["_merge"] == "both").mean()) if len(merged) else 0.0

    # NDCG@5
    ndcg_per_race = []
    for rk, grp in df.groupby("race_key"):
        ndcg_per_race.append(_ndcg_at_k(
            grp["finish_position"].values, grp["pred_score"].values, k=5,
        ))
    ndcg5 = float(np.mean(ndcg_per_race)) if ndcg_per_race else 0.0

    # Log loss + brier — only meaningful when pred_score is a probability
    log_loss = None
    brier = None
    if is_win_prob:
        # Clip probabilities to avoid log(0)
        p = np.clip(df["pred_score"].values, 1e-6, 1 - 1e-6)
        y = (df["finish_position"].values == 1).astype(float)
        log_loss = float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
        brier = float(np.mean((p - y) ** 2))

    # Flat-bet ROI: bet $2 on each race's predicted-rank-1 horse at
    # morning_line_odds. Win = $2 * decimal_odds. Loss = -$2.
    flat_pl = 0.0
    flat_n = 0
    if morning_line_map is not None:
        for _, r in top1.iterrows():
            mlo = morning_line_map.get((
                r["track_code"], pd.Timestamp(r["race_date"]).date(),
                int(r["race_number"]), r["horse_id"],
            ))
            if mlo is None:
                continue
            flat_n += 1
            decimal_odds = float(mlo) + 1.0
            if r["finish_position"] == 1:
                flat_pl += 2.0 * decimal_odds - 2.0
            else:
                flat_pl += -2.0
    flat_bet_roi = (flat_pl / (flat_n * 2.0)) if flat_n else 0.0

    return {
        "top1_hit_rate":   top1_hit_rate,
        "top3_hit_rate":   top3_hit_rate,
        "ndcg5":           ndcg5,
        "log_loss":        log_loss,
        "brier":           brier,
        "flat_bet_roi":    flat_bet_roi,
        "flat_bet_pl":     flat_pl,
        "n_top1_with_mlo": flat_n,
        "df":              df,
    }


def _paired_breakdown(labels: pd.DataFrame,
                     new_scores: np.ndarray,
                     cur_scores: np.ndarray) -> dict:
    """Per-race comparison of new vs current top-1 picks."""
    df = labels.copy()
    df["new_score"] = new_scores
    df["cur_score"] = cur_scores
    df["new_rank"] = df.groupby("race_key")["new_score"].rank(
        ascending=False, method="first")
    df["cur_rank"] = df.groupby("race_key")["cur_score"].rank(
        ascending=False, method="first")

    new_top1 = df[df["new_rank"] == 1][["race_key", "horse_id", "finish_position"]]
    cur_top1 = df[df["cur_rank"] == 1][["race_key", "horse_id", "finish_position"]]

    new_top1 = new_top1.rename(columns={"horse_id": "new_pick", "finish_position": "new_fin"})
    cur_top1 = cur_top1.rename(columns={"horse_id": "cur_pick", "finish_position": "cur_fin"})
    paired = new_top1.merge(cur_top1, on="race_key", how="inner")

    agree = (paired["new_pick"] == paired["cur_pick"]).sum()
    disagree = paired[paired["new_pick"] != paired["cur_pick"]]
    n_disagree = len(disagree)
    new_won = (disagree["new_fin"] == 1).sum()
    cur_won = (disagree["cur_fin"] == 1).sum()
    neither = ((disagree["new_fin"] != 1) & (disagree["cur_fin"] != 1)).sum()

    return {
        "n_races":         len(paired),
        "agree":           int(agree),
        "disagree":        int(n_disagree),
        "new_won":         int(new_won),
        "cur_won":         int(cur_won),
        "neither_won":     int(neither),
    }


def _print_table(label: str, new_m: dict, cur_m: dict, paired: dict, n_races: int):
    print()
    print("=" * 78)
    print(f"  {label}")
    print("=" * 78)
    cols = [
        ("top-1 hit rate",  "top1_hit_rate",  "pct"),
        ("top-3 hit rate",  "top3_hit_rate",  "pct"),
        ("NDCG@5",          "ndcg5",          "f3"),
        ("log loss",        "log_loss",       "f4"),
        ("brier",           "brier",          "f4"),
        ("flat-bet ROI",    "flat_bet_roi",   "pct"),
        ("flat-bet net P/L", "flat_bet_pl",   "money"),
    ]

    def fmt(val, kind):
        if val is None:
            return "n/a"
        if kind == "pct":
            return f"{val * 100:+6.2f}%"
        if kind == "f3":
            return f"{val:6.3f}"
        if kind == "f4":
            return f"{val:6.4f}"
        if kind == "money":
            return f"${val:+8.2f}"
        return str(val)

    print(f"  {'metric':<22} {'NEW':>14} {'CURRENT':>14}    {'Δ':>10}")
    for name, key, kind in cols:
        nv = new_m.get(key)
        cv = cur_m.get(key)
        if nv is None or cv is None:
            delta_str = "n/a"
        else:
            delta_str = f"{(nv - cv) * (100 if kind == 'pct' else 1):+6.3f}"
            if kind == "pct":
                delta_str += "pp"
        print(f"  {name:<22} {fmt(nv, kind):>14} {fmt(cv, kind):>14}    {delta_str:>10}")

    # Hit-rate SE on the paired difference (Wilson-ish via McNemar-like).
    # For paired binary data, SE_diff ~ sqrt((b + c) / n^2)
    # where b = new-correct-cur-incorrect, c = current-correct-new-incorrect.
    # Approximation: use top1 disagreement counts.
    b = paired["new_won"]
    c = paired["cur_won"]
    n = paired["n_races"]
    se = math.sqrt((b + c) / (n * n)) if n > 0 else 0.0
    delta_hr = new_m["top1_hit_rate"] - cur_m["top1_hit_rate"]
    print()
    print(f"  Hit-rate Δ:       {delta_hr * 100:+6.3f}pp     "
          f"SE ≈ ±{se * 100:6.3f}pp     "
          f"95% CI: [{(delta_hr - 1.96*se)*100:+.3f}pp, "
          f"{(delta_hr + 1.96*se)*100:+.3f}pp]")

    # Paired breakdown
    print()
    print(f"  Paired-race breakdown (n_races={paired['n_races']}):")
    print(f"    Agree on rank-1:     {paired['agree']} races")
    print(f"    Disagree on rank-1:  {paired['disagree']} races")
    print(f"      new's pick won:    {paired['new_won']}")
    print(f"      current's pick won:{paired['cur_won']}")
    print(f"      neither won:       {paired['neither_won']}")

    # ROI uses morning_line; add row counts
    print()
    print(f"  Morning-line coverage on top-1 picks: "
          f"new={new_m['n_top1_with_mlo']}/{n_races}, "
          f"current={cur_m['n_top1_with_mlo']}/{n_races}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--new-wp",     required=True)
    ap.add_argument("--current-wp", required=True)
    ap.add_argument("--new-rk",     required=True)
    ap.add_argument("--current-rk", required=True)
    ap.add_argument("--start-date", required=True)
    ap.add_argument("--end-date",   required=True)
    ap.add_argument("--tracks",     default="all")
    args = ap.parse_args()

    start_d = date.fromisoformat(args.start_date)
    end_d   = date.fromisoformat(args.end_date)
    tracks = None if args.tracks.lower() == "all" else \
        [t.strip().upper() for t in args.tracks.split(",")]

    print(f"=== Phase 1 holdout comparison ===", flush=True)
    print(f"  window: {start_d} → {end_d}    tracks: {tracks or 'ALL'}",
          flush=True)

    # Load 4 boosters + meta sidecars
    print("\nDownloading model artifacts...", flush=True)
    boosters = {}
    metas = {}
    for k, uri in [("new_wp",     args.new_wp),
                   ("current_wp", args.current_wp),
                   ("new_rk",     args.new_rk),
                   ("current_rk", args.current_rk)]:
        t0 = time.perf_counter()
        boosters[k] = _load_booster(uri)
        metas[k] = _load_meta(uri)
        print(f"  loaded {k}: {uri}    ({time.perf_counter()-t0:.1f}s)",
              flush=True)

    # Build feature matrix for the holdout year.
    print("\nBuilding feature matrix for 2026 (will slice to holdout)...",
          flush=True)
    t0 = time.perf_counter()
    conn = _get_conn()
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2026, end_year=2026, include_odds=True,
    )
    labels_df["race_date"] = pd.to_datetime(labels_df["race_date"])
    feat_h, lab_h = _filter_holdout(features_df, labels_df, start_d, end_d, tracks)
    print(f"  full 2026 matrix: {len(features_df):,}  "
          f"holdout: {len(feat_h):,} rows in "
          f"{lab_h['race_key'].nunique():,} races    "
          f"({time.perf_counter()-t0:.0f}s)", flush=True)

    if len(feat_h) == 0:
        print("ERROR: holdout is empty.")
        sys.exit(2)

    # Morning-line odds for ROI
    print("Loading morning-line odds for ROI...", flush=True)
    mlo_map = _load_morning_line_odds(conn, lab_h["race_key"].unique().tolist())
    print(f"  loaded {len(mlo_map):,} (entry → ML odds) entries", flush=True)
    conn.close()

    # Feature schemas
    feat_66 = get_feature_names(include_odds=True)         # 66 cols, wp_full input
    feat_51 = get_ranker_full_features()                   # 51 cols, rk_full lean51 input
    print(f"\nSchemas: wp_full={len(feat_66)} features    "
          f"rk_full lean51={len(feat_51)} features", flush=True)

    # Verify columns present
    missing_66 = [f for f in feat_66 if f not in feat_h.columns]
    missing_51 = [f for f in feat_51 if f not in feat_h.columns]
    if missing_66:
        print(f"⚠ wp missing features: {missing_66[:5]}...")
    if missing_51:
        print(f"⚠ rk missing features: {missing_51[:5]}...")

    X66 = feat_h[feat_66].values.astype(np.float32)
    X51 = feat_h[feat_51].values.astype(np.float32)

    # Predict
    print("\nPredicting...", flush=True)
    d66 = xgb.DMatrix(X66, feature_names=feat_66)
    d51 = xgb.DMatrix(X51, feature_names=feat_51)

    new_wp_pred = boosters["new_wp"].predict(d66)
    cur_wp_pred = boosters["current_wp"].predict(d66)
    new_rk_pred = boosters["new_rk"].predict(d51)
    cur_rk_pred = boosters["current_rk"].predict(d51)

    n_races = lab_h["race_key"].nunique()
    print(f"  Predictions for {len(feat_h):,} entries × 4 models in "
          f"{n_races:,} races", flush=True)

    # Metrics for each pair
    print("\nComputing metrics...", flush=True)
    new_wp_m = _per_race_metrics(lab_h, new_wp_pred, mlo_map, is_win_prob=True)
    cur_wp_m = _per_race_metrics(lab_h, cur_wp_pred, mlo_map, is_win_prob=True)
    new_rk_m = _per_race_metrics(lab_h, new_rk_pred, mlo_map, is_win_prob=False)
    cur_rk_m = _per_race_metrics(lab_h, cur_rk_pred, mlo_map, is_win_prob=False)

    paired_wp = _paired_breakdown(lab_h, new_wp_pred, cur_wp_pred)
    paired_rk = _paired_breakdown(lab_h, new_rk_pred, cur_rk_pred)

    _print_table(
        "WP_FULL — NEW (wp_full_20260429_0244) vs CURRENT (wp_full_20260428_0444)",
        new_wp_m, cur_wp_m, paired_wp, n_races,
    )
    _print_table(
        "RK_FULL — NEW (rk_full_20260429_0318) vs CURRENT (rk_full_lean51_20260428_1447)",
        new_rk_m, cur_rk_m, paired_rk, n_races,
    )

    print()
    print("=" * 78)
    print("DONE — comparison only. No promotion. No model_versions writes.")
    print("=" * 78)


if __name__ == "__main__":
    main()
