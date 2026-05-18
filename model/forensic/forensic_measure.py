"""
Forensic measurement framework: per-artifact AUC + calibration + standalone ROI + top-N hit rate + ensemble contribution.

Substrate-prerequisite for Build Dispatches 2 + 3 + Tier 2 execution.

Per § 4.23: BEL stratification (high-coverage tier excludes BEL until H3 resolution lands; BEL informational-only).
Per § 4.34: forensic-window OOS measurement substrate-grounded; training-time eval reported alongside.
Per § 4.36: dual-criterion (AUC + ROI) output for activation gate adjudication.
"""

import argparse
import json
import os
from datetime import date
from pathlib import Path

import boto3
import numpy as np
import pandas as pd
import psycopg2
from sklearn.metrics import roc_auc_score, brier_score_loss

# Substrate constants per § 4.23
HIGH_COVERAGE_TRACKS_ADJUDICATION_GRADE = ['BEL', 'SA', 'CD', 'GP', 'KEE', 'OP', 'SAR', 'DMR', 'MTH', 'AQU', 'PIM']
BEL_STRATIFICATION_PENDING_H3 = ['BEL']  # BEL informational-only until H3 fetcher fix lands

DB_SECRET_ARN = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'


def get_db_conn():
    """Substrate-pragmatic DB connection via Secrets Manager."""
    sm = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString'])
    return psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'],
        password=secret['password'],
    )


def _load_artifact_json(artifact_path):
    """Substrate-pragmatic helper: load artifact JSON from S3 or local path."""
    if artifact_path.startswith('s3://'):
        s3 = boto3.client('s3', region_name='us-east-1')
        bucket, key = artifact_path.replace('s3://', '').split('/', 1)
        obj = s3.get_object(Bucket=bucket, Key=key)
        return json.loads(obj['Body'].read())
    with open(artifact_path) as f:
        return json.load(f)


def load_artifact_predictions(artifact_path, window_start, window_end):
    """Load artifact predictions with substrate-pragmatic per-artifact schema metadata.

    Artifact metadata fields:
      - predictions: inline list of prediction rows (short-circuits DB pull)
      - predictions_table: DB table (default 'wr_predictions')
      - prediction_column: column for win probability (default 'win_probability')
      - version_column: version discriminator column (default 'model_version_id')
      - version_value: version discriminator value (UUID OR varchar); falls back
        to top-level 'model_version_id' for backward compatibility
      - date_column: date-bearing column (default 'created_at')
      - horse_id_cast: 'uuid' / 'text' / None for SELECT-side cast

    Schema-correct per substrate-actual hybrid_c_predictions (ensemble_version /
    predicted_at / horse_id TEXT) vs wr_predictions (model_version_id /
    created_at / horse_id UUID).
    """
    artifact = _load_artifact_json(artifact_path)

    if 'predictions' in artifact:
        return pd.DataFrame(artifact['predictions'])

    predictions_table = artifact.get('predictions_table', 'wr_predictions')
    prediction_column = artifact.get('prediction_column', 'win_probability')
    version_column = artifact.get('version_column', 'model_version_id')
    version_value = artifact.get('version_value') or artifact.get('model_version_id')
    date_column = artifact.get('date_column', 'created_at')
    horse_id_cast = artifact.get('horse_id_cast')

    if version_value is None:
        raise ValueError(f"Substrate-broken artifact: missing version_value: {artifact_path}")

    horse_id_select = f"horse_id::{horse_id_cast}" if horse_id_cast else "horse_id"

    conn = get_db_conn()
    df = pd.read_sql(f"""
        SELECT race_id, {horse_id_select} AS horse_id,
               {prediction_column} AS win_probability,
               {date_column} AS prediction_timestamp
        FROM {predictions_table}
        WHERE {version_column} = %s
          AND {date_column}::date BETWEEN %s AND %s
    """, conn, params=[version_value, window_start, window_end])
    conn.close()
    return df


def load_actuals(forensic_window_start, forensic_window_end):
    """Pull actuals (race results + entry payouts) from DB.

    Substrate-pragmatic: races table has track_id (UUID); track_code (alphabetic
    code referenced by § 4.23 BEL stratification) lives on tracks table.
    """
    conn = get_db_conn()
    df = pd.read_sql("""
        SELECT
            r.race_id, r.race_date, t.track_code, r.field_size,
            e.horse_id, e.morning_line_odds,
            res.finish_position,
            (res.finish_position = 1)::int AS is_winner,
            COALESCE(res.win_payout, 0.0) AS win_payout,
            COALESCE(res.place_payout, 0.0) AS place_payout
        FROM races r
        JOIN tracks t ON t.track_id = r.track_id
        JOIN entries e USING (race_id)
        LEFT JOIN results res ON res.race_id = r.race_id AND res.horse_id = e.horse_id
        WHERE r.race_date BETWEEN %s AND %s
    """, conn, params=[forensic_window_start, forensic_window_end])
    conn.close()
    return df


def compute_per_layer_metrics(predictions_df, actuals_df, track_filter=None):
    """Per-layer forensic metrics: AUC + Brier + top-1 win rate + top-3 + standalone ROI.

    Substrate-pragmatic: returns dict; None for nonsensical / substrate-thin cohorts.
    horse_id type coercion at merge boundary handles substrate-actual schema divergence
    (hybrid_c_predictions.horse_id TEXT vs entries.horse_id UUID).
    """
    predictions_df = predictions_df.copy()
    actuals_df = actuals_df.copy()
    predictions_df['horse_id'] = predictions_df['horse_id'].astype(str)
    actuals_df['horse_id'] = actuals_df['horse_id'].astype(str)

    merged = predictions_df.merge(actuals_df, on=['race_id', 'horse_id'], how='inner')

    if track_filter:
        merged = merged[merged['track_code'].isin(track_filter)]

    valid = merged.dropna(subset=['win_probability', 'is_winner'])

    if len(valid) < 30:
        return {
            'n_observations': len(valid), 'n_races': int(merged['race_id'].nunique()),
            'auc': None, 'brier': None,
            'top1_win_rate': None, 'top3_hit_rate': None,
            'standalone_roi_pct': None,
            'note': 'substrate-thin (<30 observations)'
        }

    auc = roc_auc_score(valid['is_winner'], valid['win_probability'])
    brier = brier_score_loss(valid['is_winner'], valid['win_probability'])

    # Top-1 per race
    top1 = merged.groupby('race_id').apply(
        lambda g: g.nlargest(1, 'win_probability')[['horse_id', 'is_winner', 'win_payout']].iloc[0]
        if len(g) > 0 else None
    ).dropna()

    if len(top1) == 0:
        return {
            'n_observations': len(valid), 'n_races': int(merged['race_id'].nunique()),
            'auc': auc, 'brier': brier,
            'top1_win_rate': None, 'top3_hit_rate': None,
            'standalone_roi_pct': None,
            'note': 'top1 substrate-thin'
        }

    top1_win_rate = top1['is_winner'].mean()
    standalone_roi_pct = (top1['win_payout'].sum() - 2.0 * len(top1)) / (2.0 * len(top1)) * 100

    # Top-3
    def race_top3_hit(g):
        top3 = g.nlargest(3, 'win_probability')
        return int(top3['is_winner'].sum() > 0)
    top3_hit_rate = merged.groupby('race_id').apply(race_top3_hit).mean()

    return {
        'n_observations': len(valid), 'n_races': int(merged['race_id'].nunique()),
        'auc': float(auc), 'brier': float(brier),
        'top1_win_rate': float(top1_win_rate),
        'top3_hit_rate': float(top3_hit_rate),
        'standalone_roi_pct': float(standalone_roi_pct),
    }


def compute_stratified_metrics(predictions_df, actuals_df):
    """Two-tier coverage-stratified metrics per § 4.23.

    - Adjudication-grade tier: high-coverage tracks excluding BEL until H3 lands
    - BEL informational-only tier
    - Per-track breakdown for full transparency
    """
    aggregate = compute_per_layer_metrics(predictions_df, actuals_df)

    non_bel_tracks = [t for t in HIGH_COVERAGE_TRACKS_ADJUDICATION_GRADE if t not in BEL_STRATIFICATION_PENDING_H3]
    adjudication_grade = compute_per_layer_metrics(predictions_df, actuals_df, track_filter=non_bel_tracks)

    bel_informational = compute_per_layer_metrics(predictions_df, actuals_df, track_filter=BEL_STRATIFICATION_PENDING_H3)

    # Per-track breakdown
    per_track = {}
    for track in HIGH_COVERAGE_TRACKS_ADJUDICATION_GRADE:
        per_track[track] = compute_per_layer_metrics(predictions_df, actuals_df, track_filter=[track])

    return {
        'aggregate_caveat': 'Aggregate metrics weighted-average across BEL stratification; adjudication grade reference adjudication_grade_non_bel only until H3 lands',
        'aggregate': aggregate,
        'adjudication_grade_non_bel': adjudication_grade,
        'bel_informational_only': bel_informational,
        'per_track_breakdown': per_track,
    }


def compute_per_date_metrics(predictions_df, actuals_df):
    """Per-date AUC + ROI breakdown surfacing substrate-thin vs substrate-adjudication-grade days.

    Substrate-pragmatic implementation: groupby race_date on actuals_df; pull matching
    predictions per-date; dispatch each date to compute_per_layer_metrics with properly
    separated dataframes. (Verbatim dispatch text used a double-merge pattern that would
    have produced duplicate _x/_y columns at the dropna(subset=['is_winner']) step;
    surfaced in final report.)
    """
    predictions_df = predictions_df.copy()
    actuals_df = actuals_df.copy()
    predictions_df['horse_id'] = predictions_df['horse_id'].astype(str)
    actuals_df['horse_id'] = actuals_df['horse_id'].astype(str)

    per_date = {}
    for race_date, actuals_group in actuals_df.groupby('race_date'):
        race_ids = actuals_group['race_id'].unique()
        pred_group = predictions_df[predictions_df['race_id'].isin(race_ids)]
        per_date[str(race_date)] = compute_per_layer_metrics(pred_group, actuals_group)
    return per_date


def compute_dual_criterion_delta(candidate_metrics, baseline_metrics):
    """Per § 4.36 dual-criterion: Δ AUC AND Δ ROI vs baseline."""
    if candidate_metrics.get('auc') is None or baseline_metrics.get('auc') is None:
        return {'delta_auc': None, 'delta_roi_pp': None, 'dual_criterion_pass': None}

    delta_auc = candidate_metrics['auc'] - baseline_metrics['auc']
    delta_roi_pp = candidate_metrics.get('standalone_roi_pct', 0) - baseline_metrics.get('standalone_roi_pct', 0)

    # § 4.36 default thresholds (substrate-pragmatic; caller can override)
    DELTA_AUC_THRESHOLD = 0.017
    DELTA_ROI_THRESHOLD_PP = 0.0  # No regression

    dual_criterion_pass = delta_auc >= DELTA_AUC_THRESHOLD and delta_roi_pp >= DELTA_ROI_THRESHOLD_PP

    return {
        'delta_auc': float(delta_auc),
        'delta_roi_pp': float(delta_roi_pp),
        'dual_criterion_pass': bool(dual_criterion_pass),
        'thresholds_applied': {'delta_auc': DELTA_AUC_THRESHOLD, 'delta_roi_pp': DELTA_ROI_THRESHOLD_PP},
    }


def main():
    parser = argparse.ArgumentParser(description='Forensic measurement framework per § 4.23 + § 4.34 + § 4.36')
    parser.add_argument('--artifact', required=True, help='Artifact path (S3 or local JSON)')
    parser.add_argument('--baseline', help='Baseline artifact path (for dual-criterion delta)')
    parser.add_argument('--window-start', default='2026-05-02', help='Forensic window start')
    parser.add_argument('--window-end', default='2026-05-10', help='Forensic window end')
    parser.add_argument('--stratify-bel', action='store_true', help='Apply § 4.23 BEL stratification')
    parser.add_argument('--stratify-per-date', action='store_true', help='Per-date AUC + ROI breakdown (substrate-thin vs substrate-adjudication-grade days)')
    parser.add_argument('--output', required=True, help='Output JSON path')
    args = parser.parse_args()

    print(f"Loading artifact: {args.artifact}")
    predictions_df = load_artifact_predictions(args.artifact, args.window_start, args.window_end)
    print(f"  predictions: {len(predictions_df)} rows")

    print(f"Loading actuals: {args.window_start}..{args.window_end}")
    actuals_df = load_actuals(args.window_start, args.window_end)
    print(f"  actuals: {len(actuals_df)} rows")

    if args.stratify_bel:
        metrics = compute_stratified_metrics(predictions_df, actuals_df)
    else:
        metrics = {'aggregate': compute_per_layer_metrics(predictions_df, actuals_df)}

    if args.stratify_per_date:
        metrics['per_date_breakdown'] = compute_per_date_metrics(predictions_df, actuals_df)

    if args.baseline:
        print(f"Computing dual-criterion delta vs baseline: {args.baseline}")
        baseline_predictions = load_artifact_predictions(args.baseline, args.window_start, args.window_end)
        baseline_metrics = compute_stratified_metrics(baseline_predictions, actuals_df) if args.stratify_bel else \
                           {'aggregate': compute_per_layer_metrics(baseline_predictions, actuals_df)}

        # Dual-criterion against adjudication-grade tier per § 4.34
        candidate_adj = metrics.get('adjudication_grade_non_bel') or metrics.get('aggregate')
        baseline_adj = baseline_metrics.get('adjudication_grade_non_bel') or baseline_metrics.get('aggregate')

        metrics['dual_criterion_delta_vs_baseline'] = compute_dual_criterion_delta(candidate_adj, baseline_adj)
        metrics['baseline_metrics'] = baseline_metrics

    with open(args.output, 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"Forensic measurement complete: {args.output}")

    # Surface key findings
    if 'adjudication_grade_non_bel' in metrics:
        adj = metrics['adjudication_grade_non_bel']
        print(f"  adjudication-grade AUC: {adj.get('auc')}")
        print(f"  adjudication-grade ROI: {adj.get('standalone_roi_pct')}%")
    if 'dual_criterion_delta_vs_baseline' in metrics:
        delta = metrics['dual_criterion_delta_vs_baseline']
        print(f"  Δ AUC vs baseline: {delta.get('delta_auc')}")
        print(f"  Δ ROI vs baseline: {delta.get('delta_roi_pp')}pp")
        print(f"  dual-criterion pass: {delta.get('dual_criterion_pass')}")


if __name__ == '__main__':
    main()
