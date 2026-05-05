#!/usr/bin/env python3
"""Stream A2.8 — 4-check diagnostic on lean53 calibrated handicapping_prob.

Holdout: April 15-26, 2026 (out-of-training, post-calibration window).

For each lean53 artifact:
  raw = booster.predict(features_lean53)
  if PL: raw = per_race_softmax(raw)
  handicapping_prob = isotonic(raw)         # via calibration sidecar

4 checks:
  1. Per-pick ROI by ML bucket (top-1 picks)
  2. Calibration deciles on holdout
  3. Top-10 feature importance (gain) — should be performance-only,
     specifically NO 'closing_odds', 'log_closing_odds', 'odds_move',
     and ideally no zero-gain features
  4. Derby R12 (CD 2026-05-02) — top picks vs. ML chalk

Verbose output for wp_full_general + wp_full_speed; summary table for
the rest.
"""
from __future__ import annotations
import json
import re
import sys
import tempfile
from datetime import date, datetime

import boto3
import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import xgboost as xgb

sys.path.insert(0, "/home/strakajagr/projects/equine-equalizer/model")
from shared.data_loader import _get_conn, build_feature_matrix
from shared.feature_definitions import (
    get_lean53_features, get_lean53_core_features,
)

S3 = boto3.client("s3")
BUCKET = "equine-model-artifacts"

HOLD_START = date(2026, 4, 15)
HOLD_END   = date(2026, 4, 26)
DERBY_DATE = date(2026, 5, 2)

SPECS = ['general', 'speed', 'closer', 'class_riser',
         'class_dropper', 'sprint', 'route']


def _download(uri, dest):
    bucket, _, key = uri[5:].partition("/")
    S3.download_file(bucket, key, dest)


def _find_artifact(prefix: str, kind: str, spec: str) -> tuple[str, str] | None:
    if spec == 'general':
        pattern = rf'^{kind}_lean53_\d{{8}}_\d{{4}}\.json$'
    else:
        pattern = rf'^{kind}_lean53_{spec}_\d{{8}}_\d{{4}}\.json$'
    paginator = S3.get_paginator('list_objects_v2')
    matches = []
    for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix):
        for obj in page.get('Contents', []):
            name = obj['Key'].rsplit('/', 1)[-1]
            if re.match(pattern, name):
                matches.append((obj['LastModified'], obj['Key'], name))
    if not matches:
        return None
    matches.sort(reverse=True)
    _, key, name = matches[0]
    return name.rsplit('.', 1)[0], f"s3://{BUCKET}/{key}"


def _load_booster(s3_uri):
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        local = f.name
    _download(s3_uri, local)
    b = xgb.Booster()
    b.load_model(local)
    return b


def _load_calibration(s3_uri):
    cal_uri = s3_uri.replace(".json", "_calibration.json")
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        local = f.name
    _download(cal_uri, local)
    with open(local) as f:
        cal = json.load(f)
    return (np.array(cal['x_thresholds'], dtype=float),
            np.array(cal['y_thresholds'], dtype=float))


def _apply_iso(raw, xt, yt):
    return np.clip(np.interp(raw, xt, yt), 0.0, 1.0)


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


def _per_pick_roi(probs, ml_odds, finish_pos, race_keys):
    """Top-1 picks by probs per race; ROI by ML bucket."""
    df = pd.DataFrame({
        "p": probs, "ml": ml_odds, "fin": finish_pos, "rk": race_keys.values
    })
    picks = df.loc[df.groupby("rk")["p"].idxmax()].copy()
    n_races = len(picks)
    buckets = [(0, 3.0, 'chalk'), (3.0, 6.0, 'vague_fav'),
               (6.0, 12.0, 'mid'), (12.0, 25.0, 'overlay'),
               (25.0, 999.0, 'deep_ls')]
    print(f"  Per-pick ROI ({n_races} races):")
    print(f"  {'bucket':<22} {'N':>4} {'wins':>5} {'hit':>7} {'avg_ml':>7} "
          f"{'roi':>9} {'net':>10}")
    for lo, hi, name in buckets:
        m = (picks["ml"] >= lo) & (picks["ml"] < hi)
        n = int(m.sum())
        wins = int((picks.loc[m, "fin"] == 1).sum())
        if n == 0:
            print(f"  {name:<22} {n:>4}")
            continue
        avg_ml = float(picks.loc[m, "ml"].mean())
        # Win bet pays $2 + ML*2 per $2 wager (i.e., (ml+1)*2 - 2 = ml*2 net)
        # Simpler: $1 bet, profit = ml on win, -1 on loss
        wins_arr = (picks.loc[m, "fin"] == 1).values
        ml_arr = picks.loc[m, "ml"].values
        net = wins_arr * ml_arr - (1 - wins_arr.astype(int))  # +ml on win, -1 on loss
        roi_pct = float(net.sum()) / n * 100
        print(f"  {name:<22} {n:>4} {wins:>5} {100*wins/n:>6.2f}% "
              f"{avg_ml:>7.2f} {roi_pct:>+8.2f}% {net.sum():>+9.2f}")


def _calibration_table(probs, y_true, label="", indent="  "):
    print(f"\n{indent}Calibration deciles ({label}):")
    print(f"{indent}{'decile':<14} {'N':>6} {'mean_pred':>10} "
          f"{'obs':>10} {'delta':>8}")
    for lo, hi in [(0.0,0.1),(0.1,0.2),(0.2,0.3),(0.3,0.4),
                   (0.4,0.5),(0.5,0.6),(0.6,0.7),(0.7,0.8),
                   (0.8,0.9),(0.9,1.001)]:
        mask = (probs >= lo) & (probs < hi)
        n = int(mask.sum())
        if n == 0: continue
        mp = float(probs[mask].mean())
        obs = float(y_true[mask].mean())
        delta = obs - mp
        print(f"{indent}[{lo:.1f}, {hi:.1f})  {n:>6,} {mp*100:>9.2f}% "
              f"{obs*100:>9.2f}% {delta*100:>+7.2f}pp")


def _summarize_calibration(probs, y_true) -> tuple[float, float, int]:
    """Return (max_pp_delta, mean_pp_delta, n_buckets_over_5pp)."""
    deltas = []
    for lo, hi in [(0.0,0.1),(0.1,0.2),(0.2,0.3),(0.3,0.4),
                   (0.4,0.5),(0.5,0.6),(0.6,0.7),(0.7,0.8),
                   (0.8,0.9),(0.9,1.001)]:
        mask = (probs >= lo) & (probs < hi)
        n = int(mask.sum())
        if n < 5: continue
        mp = float(probs[mask].mean())
        obs = float(y_true[mask].mean())
        deltas.append(abs(obs - mp))
    if not deltas:
        return (0, 0, 0)
    arr = np.array(deltas) * 100
    return float(arr.max()), float(arr.mean()), int((arr > 5).sum())


def _top10_importance(booster, feat_names):
    """Return [(feat, gain)] sorted by gain desc, top 10."""
    imp = booster.get_score(importance_type='gain')
    items = sorted(imp.items(), key=lambda kv: -kv[1])
    # XGBoost returns f0, f1, ... if features unknown; map back
    out = []
    for k, v in items[:10]:
        if k.startswith('f') and k[1:].isdigit():
            idx = int(k[1:])
            name = feat_names[idx] if idx < len(feat_names) else k
        else:
            name = k
        out.append((name, v))
    return out


def main():
    print("=" * 78)
    print("STREAM A2.8 — Lean53 4-Check Diagnostic on Handicapping Prob")
    print(f"Holdout window: {HOLD_START} → {HOLD_END}  (Derby check: {DERBY_DATE})")
    print("=" * 78)

    print("\nBuilding 2026 feature matrix...", flush=True)
    conn = _get_conn()
    features_df, labels_df = build_feature_matrix(
        conn, start_year=2026, end_year=2026, include_odds=True,
    )
    conn.close()

    labels_df["race_date"] = pd.to_datetime(labels_df["race_date"])
    holdmask = ((labels_df["race_date"].dt.date >= HOLD_START) &
                (labels_df["race_date"].dt.date <= HOLD_END))
    feat_h = features_df.loc[holdmask.values].reset_index(drop=True)
    lab_h = labels_df[holdmask].reset_index(drop=True)
    print(f"  full 2026 matrix: {len(features_df):,} rows; holdout: {len(feat_h):,}")

    # ML lookup for holdout — keyed on (track_code, race_date, race_number, horse_id)
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    sec = json.loads(sm.get_secret_value(SecretId="equine-equalizer/db-credentials")["SecretString"])
    db = psycopg2.connect(host=sec["host"], port=sec["port"], dbname=sec["dbname"],
                          user=sec["username"], password=sec["password"], cursor_factory=RealDictCursor)
    cur = db.cursor()
    cur.execute("""SELECT t.track_code, r.race_date, r.race_number,
                          e.horse_id::text AS horse_id, e.morning_line_odds
                   FROM entries e
                   JOIN races r ON e.race_id = r.race_id
                   JOIN tracks t ON t.track_id = r.track_id
                   WHERE r.race_date BETWEEN %s AND %s""",
                (HOLD_START, HOLD_END))
    ml_map = {(r['track_code'], str(r['race_date']), int(r['race_number']),
               str(r['horse_id'])): float(r['morning_line_odds'] or 5.0)
              for r in cur.fetchall()}

    wp_features = get_lean53_features()
    pl_features = get_lean53_core_features()
    y_true = (lab_h["finish_position"].values == 1).astype(float)

    summaries = []  # for the across-style summary

    for spec in SPECS:
        for kind in ('wp_full', 'pl_core'):
            prefix = "win_prob/" if kind == 'wp_full' else "pl/"
            found = _find_artifact(prefix, kind, spec)
            if not found:
                print(f"\n  ⚠ no {kind}_{spec} lean53 artifact found; skipping")
                continue
            version, s3_uri = found
            xt, yt = _load_calibration(s3_uri)
            booster = _load_booster(s3_uri)
            feats = wp_features if kind == 'wp_full' else pl_features

            X = feat_h[feats].values.astype(np.float32)
            dm = xgb.DMatrix(X, feature_names=feats)
            raw = booster.predict(dm)
            if kind == 'pl_core':
                raw = _per_race_softmax(raw, lab_h["race_key"])
            cal = _apply_iso(raw, xt, yt)

            verbose = (spec == 'general' or (kind == 'wp_full' and spec == 'speed'))

            ml_arr = np.array([
                ml_map.get(
                    (str(lab_h.iloc[i]['track_code']),
                     str(pd.Timestamp(lab_h.iloc[i]['race_date']).date()),
                     int(lab_h.iloc[i]['race_number']),
                     str(lab_h.iloc[i]['horse_id'])),
                    float(lab_h.iloc[i].get('closing_odds') or 5.0))
                for i in range(len(lab_h))
            ])
            mxd, mnd, nb5 = _summarize_calibration(cal, y_true)
            top10 = _top10_importance(booster, feats)
            mkt_features_in_top10 = sum(
                1 for n, _ in top10 if n in
                ('closing_odds', 'log_closing_odds', 'odds_move',
                 'morning_line_odds')
            )

            summaries.append({
                'kind': kind, 'spec': spec, 'version': version,
                'cal_max_pp': mxd, 'cal_mean_pp': mnd, 'cal_n_buckets_over_5pp': nb5,
                'top10': top10,
                'market_in_top10': mkt_features_in_top10,
            })

            if verbose:
                print(f"\n{'═'*78}")
                print(f"FULL 4-CHECK — {kind}_{spec} ({version})")
                print(f"{'═'*78}")

                # Check 1: per-pick ROI by ML bucket
                print(f"\n[Check 1] Per-pick ROI by ML bucket:")
                _per_pick_roi(cal, ml_arr,
                              lab_h["finish_position"].values,
                              lab_h["race_key"])

                # Check 2: calibration deciles (post-cal on holdout)
                _calibration_table(cal, y_true, "post-cal handicapping_prob")

                # Check 3: top-10 feature importance
                print(f"\n[Check 3] Top-10 feature importance (gain):")
                for name, gain in top10:
                    flag = " ⚠ MARKET" if name in (
                        'closing_odds', 'log_closing_odds', 'odds_move',
                        'morning_line_odds') else ""
                    print(f"    {name:<32}  {gain:>10.4f}{flag}")
                print(f"  market features in top 10: {mkt_features_in_top10} "
                      f"({'PASS' if mkt_features_in_top10 == 0 else 'FAIL — bias remains'})")

    # ─────────────────────────────────────────────────────────────
    # Print across-style summary FIRST so it lands even if Derby fails
    # ─────────────────────────────────────────────────────────────
    print(f"\n{'═'*78}")
    print(f"CALIBRATION SUMMARY — all 14 lean53 artifacts on holdout")
    print(f"{'═'*78}")
    print(f"  {'kind':<10} {'spec':<14} {'cal_max':>10} {'cal_mean':>10} "
          f"{'>5pp':>5}  {'market_top10':>13}")
    for s in summaries:
        flag = "  ⚠" if s['market_in_top10'] > 0 else ""
        print(f"  {s['kind']:<10} {s['spec']:<14} "
              f"{s['cal_max_pp']:>8.2f}pp {s['cal_mean_pp']:>8.2f}pp "
              f"{s['cal_n_buckets_over_5pp']:>5}  {s['market_in_top10']:>13}{flag}")

    # Check 4: Derby R12 (CD 2026-05-02)
    print(f"\n{'═'*78}")
    print(f"[Check 4] Derby R12 — CD {DERBY_DATE} — wp_full_general lean53 picks")
    print(f"{'═'*78}")

    cur.execute("""
        SELECT r.race_id FROM races r
        JOIN tracks t ON t.track_id=r.track_id
        WHERE t.track_code='CD' AND r.race_date=%s AND r.race_number=12
    """, (DERBY_DATE,))
    derby_row = cur.fetchone()
    if derby_row:
        derby_race_id = str(derby_row['race_id'])
        # Build features just for Derby — reuse build_feature_matrix on May 2
        derby_conn = _get_conn()
        d_feat, d_lab = build_feature_matrix(
            derby_conn, start_year=2026, end_year=2026, include_odds=True,
        )
        derby_conn.close()
        d_lab["race_date"] = pd.to_datetime(d_lab["race_date"])
        # Filter Derby entries by composite key (labels_df has no race_id)
        d_mask = (
            (d_lab["track_code"] == 'CD') &
            (d_lab["race_date"].dt.date == DERBY_DATE) &
            (d_lab["race_number"] == 12)
        ).values
        d_f = d_feat.loc[d_mask].reset_index(drop=True)
        d_l = d_lab[d_mask].reset_index(drop=True)
        print(f"  Derby R12 entries: {len(d_l)}")

        # Use wp_full_general lean53 + its calibration
        wp_g = _find_artifact("win_prob/", "wp_full", "general")
        if wp_g:
            v, uri = wp_g
            xt, yt = _load_calibration(uri)
            booster = _load_booster(uri)
            X = d_f[wp_features].values.astype(np.float32)
            dm = xgb.DMatrix(X, feature_names=wp_features)
            raw = booster.predict(dm)
            cal = _apply_iso(raw, xt, yt)

            cur.execute("""
                SELECT e.entry_id, h.horse_name, e.program_number,
                       e.morning_line_odds
                FROM entries e
                JOIN horses h ON e.horse_id = h.horse_id
                WHERE e.race_id = %s
            """, (derby_race_id,))
            entry_meta = {str(r['entry_id']): r for r in cur.fetchall()}

            results = []
            for i in range(len(d_l)):
                eid = str(d_l.iloc[i]['entry_id'])
                meta = entry_meta.get(eid, {})
                results.append({
                    'pgm': meta.get('program_number', '?'),
                    'horse': meta.get('horse_name', '?'),
                    'ml': float(meta.get('morning_line_odds') or 99),
                    'raw': float(raw[i]),
                    'cal': float(cal[i]),
                })
            results.sort(key=lambda r: -r['cal'])
            print(f"  Top 10 picks by calibrated handicapping_prob:")
            print(f"  {'pgm':>3} {'horse':<22} {'ML':>6} {'raw':>8} {'cal':>8}")
            for i, r in enumerate(results[:10]):
                tag = ""
                if r['ml'] <= 5.0:
                    tag = "  ← chalk"
                if i == 0:
                    tag += " (TOP PICK)"
                print(f"  {r['pgm']:>3} {r['horse'][:22]:<22} {r['ml']:>5.1f}  "
                      f"{r['raw']*100:>6.2f}%  {r['cal']*100:>6.2f}%{tag}")

            chalk = sorted(results, key=lambda r: r['ml'])[:3]
            print(f"\n  ML chalk top-3:")
            for r in chalk:
                cal_rank = next((i+1 for i, x in enumerate(results)
                                 if x['pgm'] == r['pgm']), '?')
                print(f"    pgm={r['pgm']} {r['horse'][:22]:<22} ML={r['ml']}  "
                      f"cal_rank=#{cal_rank}")
    else:
        print("  ⚠ Derby R12 not found in DB")

    print(f"\n{'═'*78}")
    print("KEY: market_top10 = count of (closing_odds, log_closing_odds,")
    print("     odds_move, morning_line_odds) appearing in top-10 feature gain.")
    print("     For lean53, this should be 0 (those features were culled).")
    print(f"{'═'*78}")
    print("DIAGNOSTIC COMPLETE")
    print(f"{'═'*78}")
    db.close()


if __name__ == "__main__":
    main()
