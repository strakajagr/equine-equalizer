#!/usr/bin/env python3
"""Longshot-bias diagnostic for wp_full_20260429_0244.

Four checks against the 2026-04-15 → 2026-04-26 holdout:

  1. ROI by ML-odds bucket — per-entry (population) AND per-pick (model
     behavior). Looks for "model picks longshots disproportionately and
     loses money" pattern.

  2. Feature importance audit — flag whether ML-odds-derived features
     dominate (model is just regurgitating market) or are absent (model
     is blind to market signal).

  3. Calibration table — predicted-prob deciles vs observed win rate.
     Looks for systematic over-confidence in mid-prob deciles where
     longshot picks live.

  4. Derby R12 manual sanity — dump 24-horse field with predicted_rank,
     win_prob, edge_pct, sorted by rank. Tony eyeballs whether top picks
     are all longshots (a structural bias signal).

Doesn't fix anything. Reports.

Usage:
  python3 scripts/longshot_bias_diagnostic.py
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

sys.path.insert(0, "/home/strakajagr/projects/equine-equalizer/model")
from shared.data_loader import _get_conn, build_feature_matrix
from shared.feature_definitions import get_feature_names

WP_FULL_S3 = "s3://equine-model-artifacts/win_prob/wp_full_20260429_0244.json"
WP_FULL_IMPORTANCE_S3 = (
    "s3://equine-model-artifacts/win_prob/wp_full_20260429_0244_importance.json"
)

HOLDOUT_START = date(2026, 4, 15)
HOLDOUT_END   = date(2026, 4, 26)

# Per Tony's spec
ML_BUCKETS = [
    (0.0, 3.0,    "0-3.0     (chalk: 1/2-5/2)"),
    (3.0, 6.0,    "3.0-6.0   (vague fav: 3/1-5/1)"),
    (6.0, 12.0,   "6.0-12.0  (mid: 6/1-11/1)"),
    (12.0, 25.0,  "12.0-25.0 (overlay: 12/1-24/1)"),
    (25.0, 1e9,   "25.0+     (deep ls: 25/1+)"),
]


# ─────────────────────────────────────────────────────────────────────
def _download_s3(uri: str, dest: str) -> None:
    bucket, _, key = uri[5:].partition("/")
    boto3.client("s3").download_file(bucket, key, dest)


def _load_booster(uri: str) -> xgb.Booster:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        local = f.name
    _download_s3(uri, local)
    b = xgb.Booster()
    b.load_model(local)
    return b


def _load_json(uri: str) -> dict:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        local = f.name
    _download_s3(uri, local)
    with open(local) as fh:
        return json.load(fh)


def _load_morning_line_map(conn, start: date, end: date) -> dict:
    """Build {(track, race_date, race_num, horse_id) -> ML odds}."""
    cur = conn.cursor()
    cur.execute(
        """SELECT t.track_code, r.race_date, r.race_number,
                  e.horse_id, e.morning_line_odds
           FROM entries e
           JOIN races r  ON r.race_id  = e.race_id
           JOIN tracks t ON t.track_id = r.track_id
           WHERE r.race_date BETWEEN %s AND %s""",
        (start, end),
    )
    out = {}
    for r in cur.fetchall():
        if r["morning_line_odds"] is not None:
            out[(r["track_code"], r["race_date"],
                 int(r["race_number"]), str(r["horse_id"]))] = (
                float(r["morning_line_odds"])
            )
    return out


def _ml_to_bucket(ml: float | None) -> str | None:
    if ml is None:
        return None
    for lo, hi, label in ML_BUCKETS:
        if lo <= ml < hi:
            return label
    return None


# ─────────────────────────────────────────────────────────────────────
def check1_roi_by_bucket(df: pd.DataFrame, n_races: int) -> None:
    """ROI by ML bucket — per-entry AND per-pick."""
    print()
    print("=" * 88)
    print(f"CHECK 1 — ROI by ML-odds bucket  (holdout: {HOLDOUT_START} to {HOLDOUT_END})")
    print("=" * 88)

    df = df[df["ml"].notna()].copy()
    df["bucket"] = df["ml"].apply(_ml_to_bucket)

    # ──────── 1a. Per-entry (population behavior) ────────
    print()
    print("1a — PER-ENTRY (population): all entries in each bucket")
    print(f"     {'bucket':<32} {'N':>7} {'wins':>6} {'win_rate':>9} "
          f"{'mean_pred':>10} {'cal_delta':>10}")
    for _, _, label in ML_BUCKETS:
        sub = df[df["bucket"] == label]
        n = len(sub)
        if n == 0:
            print(f"     {label:<32} {0:>7} {0:>6} {'—':>9} {'—':>10} {'—':>10}")
            continue
        wins = int((sub["finish_position"] == 1).sum())
        rate = wins / n
        mean_pred = float(sub["pred_prob"].mean())
        delta = rate - mean_pred
        print(f"     {label:<32} {n:>7,} {wins:>6} "
              f"{rate*100:>8.2f}% {mean_pred*100:>9.2f}% {delta*100:>+9.2f}pp")

    # ──────── 1b. Per-pick (model behavior — KEY ONE) ────────
    df["pred_rank"] = df.groupby("race_key")["pred_prob"].rank(
        ascending=False, method="first"
    )
    top1 = df[df["pred_rank"] == 1].copy()
    print()
    print(f"1b — PER-PICK (model behavior): wp_full's top-1 pick per race")
    print(f"     Total races: {n_races}    Top-1 picks: {len(top1)}")
    print(f"     {'bucket':<32} {'N_pick':>8} {'%races':>7} "
          f"{'wins':>5} {'hit_rate':>9} {'avg_ml':>7} {'flat_roi':>10} {'net_PL':>10}")
    for _, _, label in ML_BUCKETS:
        sub = top1[top1["bucket"] == label]
        n = len(sub)
        pct_races = (n / n_races * 100) if n_races else 0
        if n == 0:
            print(f"     {label:<32} {0:>8} {pct_races:>6.1f}% "
                  f"{'—':>5} {'—':>9} {'—':>7} {'—':>10} {'—':>10}")
            continue
        wins = int((sub["finish_position"] == 1).sum())
        hit_rate = wins / n
        avg_ml = float(sub["ml"].mean())
        # Flat $2 bet: win → +2 * ML, loss → -2
        net_pl = 0.0
        for _, row in sub.iterrows():
            if row["finish_position"] == 1:
                net_pl += 2.0 * row["ml"]
            else:
                net_pl -= 2.0
        flat_roi = net_pl / (n * 2.0)
        print(f"     {label:<32} {n:>8} {pct_races:>6.1f}% "
              f"{wins:>5} {hit_rate*100:>8.2f}% {avg_ml:>7.2f} "
              f"{flat_roi*100:>+9.2f}% ${net_pl:>+9.2f}")

    print()
    print("Reading guide:")
    print("  Healthy: chalk picks ~40%+ hit rate, ROI -10% to +5%.")
    print("           Longshot picks ~5-10% hit rate, profitable ROI from big payouts.")
    print("  Concerning: >30% of races have top-1 from 12+ bucket AND those picks lose.")
    print("  Worst: <20% of races picked from chalk yet chalk has higher hit rate.")


def check2_feature_importance() -> None:
    """Pull importance.json from S3 sidecar; flag ML-odds rank."""
    print()
    print("=" * 88)
    print("CHECK 2 — Feature importance (wp_full_20260429_0244)")
    print("=" * 88)
    imp = _load_json(WP_FULL_IMPORTANCE_S3)
    # imp is dict feature_name → gain (XGBoost importance type='gain')
    ranked = sorted(imp.items(), key=lambda x: -x[1])
    total_gain = sum(imp.values()) or 1.0

    print()
    print(f"Top 20 features by gain (out of {len(imp)} with non-zero importance):")
    print(f"  {'rank':>4}  {'gain':>11}  {'pct':>6}  feature")
    for i, (f, g) in enumerate(ranked[:20], 1):
        pct = g / total_gain * 100
        print(f"  {i:>4}  {g:>11.2f}  {pct:>5.2f}%  {f}")

    print()
    print("Specific feature ranks (1 = highest importance):")
    odds_features = ["morning_line_odds", "morning_line_implied_prob",
                     "closing_odds", "log_closing_odds", "odds_move"]
    for f in odds_features:
        if f in imp:
            rank = next(i for i, (k, _) in enumerate(ranked, 1) if k == f)
            gain = imp[f]
            pct = gain / total_gain * 100
            print(f"  {f:<28} rank={rank:>3}  gain={gain:>9.2f}  ({pct:.2f}% of total)")
        else:
            print(f"  {f:<28} NOT IN MODEL")

    # Speed features for context
    print()
    print("Speed features (for context — should be solid mid-rank):")
    for f in ["speed_fig_last", "speed_fig_avg_3", "speed_fig_best_career",
              "speed_fig_vs_field"]:
        if f in imp:
            rank = next(i for i, (k, _) in enumerate(ranked, 1) if k == f)
            gain = imp[f]
            pct = gain / total_gain * 100
            print(f"  {f:<28} rank={rank:>3}  gain={gain:>9.2f}  ({pct:.2f}% of total)")
        else:
            print(f"  {f:<28} not in model")

    # Zero-gain features
    feature_full_list = get_feature_names(include_odds=True)
    zero_gain = [f for f in feature_full_list if f not in imp]
    print()
    print(f"Features with ZERO gain ({len(zero_gain)} of {len(feature_full_list)}):")
    for f in zero_gain[:20]:
        print(f"  {f}")
    if len(zero_gain) > 20:
        print(f"  ... {len(zero_gain) - 20} more")

    print()
    print("Reading guide:")
    print("  Healthy: ML/closing odds at ranks 8-15 (used as anchor, not dominant).")
    print("  Concerning if low: rank 30+ — model blind to market signal.")
    print("  Concerning if high: rank 1-3 — model regurgitating market, no edge.")


def check3_calibration(df: pd.DataFrame) -> None:
    """Predicted-prob deciles vs observed win rate."""
    print()
    print("=" * 88)
    print("CHECK 3 — Calibration table (predicted-prob deciles)")
    print("=" * 88)
    print()
    print(f"  {'decile':<14} {'N':>7} {'mean_pred':>10} "
          f"{'wins':>6} {'obs_rate':>10} {'delta':>9}")
    for lo, hi in [(0.0, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4),
                   (0.4, 0.5), (0.5, 0.6), (0.6, 0.7), (0.7, 0.8),
                   (0.8, 0.9), (0.9, 1.001)]:
        sub = df[(df["pred_prob"] >= lo) & (df["pred_prob"] < hi)]
        n = len(sub)
        if n == 0:
            print(f"  [{lo:.1f}, {hi:.1f}){' ':<3} {0:>7} {'—':>10} {'—':>6} "
                  f"{'—':>10} {'—':>9}")
            continue
        mean_pred = float(sub["pred_prob"].mean())
        wins = int((sub["finish_position"] == 1).sum())
        obs_rate = wins / n
        delta = obs_rate - mean_pred
        print(f"  [{lo:.1f}, {hi:.1f}){' ':<3} "
              f"{n:>7,} {mean_pred*100:>9.2f}% {wins:>6} "
              f"{obs_rate*100:>9.2f}% {delta*100:>+8.2f}pp")

    print()
    print("Reading guide:")
    print("  Healthy: per-decile delta < 5pp.")
    print("  Watch the 30-40% / 40-50% deciles — if mean_pred 35% but obs 12%,")
    print("  model is over-confident on longshot picks.")


def check4_derby_sanity(df: pd.DataFrame, conn) -> None:
    """Dump 24-horse Derby field with predicted ranks + edge."""
    print()
    print("=" * 88)
    print("CHECK 4 — Derby R12 (CD 2026-05-02) sanity dump")
    print("=" * 88)
    # Need to pull 2026-05-02 data separately (out of holdout window).
    # We'll fetch fresh predictions from wr_predictions table directly,
    # since pre-compute already wrote them.
    cur = conn.cursor()
    cur.execute("""
      SELECT e.program_number, h.horse_name, e.morning_line_odds,
             p.predicted_rank, p.win_probability, p.raw_win_prob,
             p.morning_line_implied_prob, p.overlay_pct, p.is_top_pick
      FROM wr_predictions p
      JOIN entries e ON e.entry_id = p.entry_id
      JOIN horses h  ON h.horse_id = e.horse_id
      JOIN races  r  ON r.race_id  = p.race_id
      JOIN tracks t  ON t.track_id = r.track_id
      WHERE t.track_code = 'CD'
        AND r.race_date = '2026-05-02'
        AND r.race_number = 12
        AND p.style = 'general'
      ORDER BY p.predicted_rank ASC
    """)
    rows = cur.fetchall()
    print()
    print(f"  {'pgm':>3} {'horse':<24} {'ML':>5} {'ML_imp':>7} "
          f"{'rank':>4} {'pred_p':>7} {'edge':>9}")
    for r in rows:
        pgm = (r['program_number'] or '?')
        horse = (r['horse_name'] or '?')[:24]
        ml = r['morning_line_odds']
        ml_str = f"{float(ml):.1f}" if ml is not None else "—"
        ml_imp = float(r['morning_line_implied_prob'] or 0)
        rank = r['predicted_rank']
        pp = float(r['win_probability'] or 0)
        edge = float(r['overlay_pct'] or 0)
        flag = " ←TOP" if r['is_top_pick'] else ""
        print(f"  {pgm:>3} {horse:<24} {ml_str:>5} "
              f"{ml_imp*100:>6.2f}% {rank:>4} "
              f"{pp*100:>6.2f}% {edge*100:>+8.2f}%{flag}")

    # Summary by ML bucket
    print()
    print("  Summary: where does the model find edge in this field?")
    by_bucket = {}
    for r in rows:
        ml = r.get('morning_line_odds')
        if ml is None:
            continue
        bucket = _ml_to_bucket(float(ml))
        if not bucket:
            continue
        by_bucket.setdefault(bucket, []).append(r)
    for _, _, label in ML_BUCKETS:
        sub = by_bucket.get(label, [])
        if not sub:
            continue
        edges = [float(r['overlay_pct'] or 0) for r in sub]
        ranks = [r['predicted_rank'] for r in sub]
        n_pos_edge = sum(1 for e in edges if e > 0)
        print(f"    {label:<32} N={len(sub):>2}  "
              f"avg_edge={sum(edges)/len(edges)*100:>+6.2f}%  "
              f"#with_pos_edge={n_pos_edge}/{len(sub)}  "
              f"best_rank={min(ranks)}")

    print()
    print("Reading guide:")
    print("  If top 5 picks are ALL ML > 10/1 with positive edge while chalk has")
    print("  negative edge, the model 'sees value' only in horses the public also")
    print("  sees as longshots — that's not value-finding, that's structural bias.")


# ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 88)
    print("LONGSHOT-BIAS DIAGNOSTIC — wp_full_20260429_0244")
    print("=" * 88)
    print(f"Holdout window: {HOLDOUT_START} → {HOLDOUT_END}")

    print("\nLoading wp_full booster...", flush=True)
    booster = _load_booster(WP_FULL_S3)

    print("Building feature matrix (2026 → filter to holdout)...", flush=True)
    conn = _get_conn()
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2026, end_year=2026, include_odds=True,
    )
    labels_df["race_date"] = pd.to_datetime(labels_df["race_date"])
    mask = ((labels_df["race_date"].dt.date >= HOLDOUT_START) &
            (labels_df["race_date"].dt.date <= HOLDOUT_END))
    feat_h = features_df.loc[mask.values].reset_index(drop=True)
    lab_h = labels_df[mask].reset_index(drop=True)
    print(f"  holdout: {len(feat_h):,} entries × "
          f"{lab_h['race_key'].nunique():,} races")

    print("Loading morning-line odds...", flush=True)
    ml_map = _load_morning_line_map(conn, HOLDOUT_START, HOLDOUT_END)
    print(f"  {len(ml_map):,} ML odds loaded")

    print("Predicting on holdout...", flush=True)
    feat_names = get_feature_names(include_odds=True)
    X = feat_h[feat_names].values.astype(np.float32)
    dm = xgb.DMatrix(X, feature_names=feat_names)
    pred_probs = booster.predict(dm)

    df = lab_h.copy()
    df["pred_prob"] = pred_probs
    df["ml"] = df.apply(lambda r: ml_map.get((
        r["track_code"],
        pd.Timestamp(r["race_date"]).date(),
        int(r["race_number"]),
        r["horse_id"],
    )), axis=1)
    n_races = lab_h["race_key"].nunique()

    check1_roi_by_bucket(df, n_races)
    check2_feature_importance()
    check3_calibration(df)
    check4_derby_sanity(df, conn)

    conn.close()
    print()
    print("=" * 88)
    print("DIAGNOSTIC COMPLETE.")
    print("=" * 88)


if __name__ == "__main__":
    main()
