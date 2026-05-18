"""
Forensic-window prediction generation for BD2v2 boosters per BD3v2.

Three substrate-pragmatic prediction-generation paths:
  Path 1 (standard XGBoost): 3A test_lstm / 3B test_lasix / 3C test_longshot /
                              3D multi_cohort_pure_bx / 3D multi_cohort_pure_prior
  Path 2 (closed-form linear-logit): 3F hierarchical_bayesian
                                      (alpha + track_offsets + X_std @ beta)
  Path 3 (META partition-routing):    3E specialist_style (distance_furlongs ≤ 6.5 → sprint/route)
                                      3H context_conditional (field_size_bucket × claim_price_tier)

3G bayesian_bma SKIPPED per T-A2 (sub-boosters not persisted; deferred to Tier 2 EXECUTION).
Per T-A5: forensic window 2026-05-02..2026-05-10.

Output: parquet with race_id, horse_id, win_probability, ensemble_version, predicted_at.
"""

import argparse
import glob
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import boto3
import numpy as np
import pandas as pd
import psycopg2
import xgboost as xgb


DB_SECRET_ARN = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'
FORENSIC_WINDOW_START = '2026-05-02'
FORENSIC_WINDOW_END = '2026-05-10'


def get_db_conn():
    sm = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString'])
    return psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'], password=secret['password'],
    )


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def _within_race_softmax_transform(s):
    x = s.values
    e_x = np.exp(x - x.max())
    return e_x / e_x.sum()


def load_artifact_with_booster(artifact_path):
    """Load XGBoost booster artifact (Path 1)."""
    with open(artifact_path) as f:
        artifact = json.load(f)

    # Try sibling .booster.json first
    booster_local = artifact_path.replace('.json', '.booster.json')

    if not Path(booster_local).exists() and 'booster_s3_path' in artifact:
        s3_path = artifact['booster_s3_path']
        if s3_path and s3_path.startswith('s3://'):
            s3 = boto3.client('s3', region_name='us-east-1')
            bucket, key = s3_path.replace('s3://', '').split('/', 1)
            s3.download_file(bucket, key, booster_local)

    if not Path(booster_local).exists():
        raise FileNotFoundError(f"Booster substrate-thin: {booster_local}")

    booster = xgb.Booster()
    booster.load_model(booster_local)
    return booster, artifact


def load_forensic_parquets(parquet_dir):
    """Load + concatenate per-race forensic parquets."""
    parquets = sorted(glob.glob(f"{parquet_dir}/*.parquet"))
    if not parquets:
        raise ValueError(f"Substrate-thin: no parquets in {parquet_dir}")
    dfs = []
    for p in parquets:
        race_id = Path(p).stem
        df = pd.read_parquet(p)
        if 'race_id' not in df.columns:
            df['race_id'] = race_id
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    df['race_id'] = df['race_id'].astype(str)
    df['horse_id'] = df['horse_id'].astype(str)
    return df


def load_races_substrate(window_start, window_end):
    """Race-level substrate for closed-form + META routing."""
    conn = get_db_conn()
    df = pd.read_sql("""
        SELECT r.race_id::text AS race_id,
               t.track_code,
               COALESCE(r.distance_furlongs, 0.0)::float AS distance_furlongs,
               COALESCE(r.field_size, 0) AS field_size,
               COALESCE(r.claiming_price, 0) AS claim_price
        FROM races r
        LEFT JOIN tracks t ON t.track_id = r.track_id
        WHERE r.race_date BETWEEN %s AND %s
    """, conn, params=[window_start, window_end])
    conn.close()
    return df


def predict_path1_xgboost(artifact_path, parquet_dir):
    """Path 1: standard XGBoost booster prediction."""
    booster, artifact = load_artifact_with_booster(artifact_path)
    feature_cols = artifact['feature_cols']
    version_name = artifact['name']

    df = load_forensic_parquets(parquet_dir)
    print(f"  Forensic substrate: {len(df)} rows / {df['race_id'].nunique()} races")

    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Substrate-broken: missing feature cols {missing[:3]}... ({len(missing)} total)")

    X = df[feature_cols].fillna(0.0).values
    raw = booster.predict(xgb.DMatrix(X, feature_names=feature_cols))

    df_out = df[['race_id', 'horse_id']].copy()
    df_out['raw_prediction'] = raw
    df_out['win_probability'] = df_out.groupby('race_id', group_keys=False)['raw_prediction'].transform(
        _within_race_softmax_transform
    )
    df_out['ensemble_version'] = version_name
    df_out['predicted_at'] = datetime.now(timezone.utc)
    return df_out[['race_id', 'horse_id', 'win_probability', 'ensemble_version', 'predicted_at']]


def predict_path2_closed_form_3F(artifact_path, parquet_dir, races_substrate):
    """Path 2: 3F hierarchical_bayesian closed-form linear-logit reconstruction per T-A1."""
    with open(artifact_path) as f:
        artifact = json.load(f)

    version_name = artifact['name']
    feature_cols = artifact['feature_cols']
    alpha = artifact['alpha_mean']
    beta = np.array(artifact['beta_mean'])
    track_codes_trained = artifact['track_codes']
    track_offsets = np.array(artifact['track_offsets_mean'])
    feature_means = np.array(artifact['feature_means'])
    feature_stds = np.array(artifact['feature_stds'])

    track_offset_map = {tc: float(track_offsets[i]) for i, tc in enumerate(track_codes_trained)}

    df = load_forensic_parquets(parquet_dir)
    df = df.merge(races_substrate[['race_id', 'track_code']], on='race_id', how='left')
    print(f"  Forensic substrate: {len(df)} rows / {df['race_id'].nunique()} races")

    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Substrate-broken: missing feature cols {missing[:3]}...")

    X = df[feature_cols].fillna(0.0).values.astype(float)
    feat_stds_safe = np.where(feature_stds == 0, 1.0, feature_stds)
    X_std = (X - feature_means) / feat_stds_safe

    track_offset_vec = df['track_code'].map(track_offset_map).fillna(0.0).values
    n_fallback = df['track_code'].map(track_offset_map).isna().sum()
    if n_fallback > 0:
        n_fallback_races = df[df['track_code'].map(track_offset_map).isna()]['race_id'].nunique()
        print(f"  Zero-offset fallback: {n_fallback} rows ({n_fallback_races} races) at non-trained tracks")

    logit = alpha + track_offset_vec + X_std @ beta
    raw = _sigmoid(logit)

    df_out = df[['race_id', 'horse_id']].copy()
    df_out['raw_prediction'] = raw
    df_out['win_probability'] = df_out.groupby('race_id', group_keys=False)['raw_prediction'].transform(
        _within_race_softmax_transform
    )
    df_out['ensemble_version'] = version_name
    df_out['predicted_at'] = datetime.now(timezone.utc)
    return df_out[['race_id', 'horse_id', 'win_probability', 'ensemble_version', 'predicted_at']]


def _resolve_sub_artifact_local(sub_meta, version_name_hint):
    """Resolve sub-artifact local booster path. Substrate-pragmatic: BD2v2 wrote
    <stem>.<partition>.booster.json files in /tmp/bd2v2_synthetic/."""
    # Try local /tmp/bd2v2_synthetic with partition suffix
    candidates = []
    if 'version_name' in sub_meta:
        vn = sub_meta['version_name']
        # try direct local in BD2v2 synthetic dir using partition key in name
        for stem in glob.glob('/tmp/bd2v2_synthetic/*.booster.json'):
            if Path(stem).stem.replace('.booster', '') in vn or vn.endswith(Path(stem).stem.replace('.booster', '')):
                candidates.append(stem)
    s3_path = sub_meta.get('booster_s3_path')
    return candidates[0] if candidates else None, s3_path


def predict_path3_meta_routing(artifact_path, parquet_dir, races_substrate):
    """Path 3: META partition-routing per T-A4 (specialist_style + context_conditional)."""
    with open(artifact_path) as f:
        meta = json.load(f)

    version_name = meta['name']
    variant = meta.get('variant')
    sub_artifacts = meta.get('sub_artifacts', {})

    df = load_forensic_parquets(parquet_dir)
    df = df.merge(races_substrate, on='race_id', how='left')
    print(f"  Forensic substrate: {len(df)} rows / {df['race_id'].nunique()} races")

    # Routing key
    if variant == 'style_specialist' or 'specialist_style' in version_name.lower():
        df['_route_key'] = np.where(df['distance_furlongs'] <= 6.5, 'sprint', 'route')
    elif 'context_conditional' in version_name.lower():
        # Matches train_context_conditional.py bucket conventions
        def field_bucket(fs):
            if fs is None or fs == 0: return 'med'
            if fs <= 6: return 'small'
            if fs <= 9: return 'med'
            return 'large'
        def claim_tier(cp):
            if cp is None or cp == 0: return 'no_claim'
            if cp <= 25000: return 'low_claim'
            return 'high_claim'
        df['_fs_b'] = df['field_size'].apply(field_bucket)
        df['_cp_b'] = df['claim_price'].apply(claim_tier)
        df['_route_key'] = df['_fs_b'] + '__' + df['_cp_b']
    else:
        raise ValueError(f"Substrate-broken META: unknown variant for {version_name}")

    s3 = boto3.client('s3', region_name='us-east-1')
    chunks = []
    for route_key, sub_meta in sub_artifacts.items():
        if not isinstance(sub_meta, dict) or sub_meta.get('status') != 'trained':
            print(f"    route {route_key}: skipped (status={sub_meta.get('status') if isinstance(sub_meta, dict) else '?'})")
            continue

        chunk = df[df['_route_key'] == route_key]
        if len(chunk) == 0:
            print(f"    route {route_key}: zero forensic rows match")
            continue

        # Locate booster
        sub_version = sub_meta.get('version_name', '')
        # BD2v2 wrote <meta>.<route>.booster.json
        local_candidate = artifact_path.replace('.json', f'.{route_key}.booster.json')
        if not Path(local_candidate).exists():
            s3_path = sub_meta.get('booster_s3_path', '')
            if s3_path and s3_path.startswith('s3://'):
                bucket, key = s3_path.replace('s3://', '').split('/', 1)
                s3.download_file(bucket, key, local_candidate)
            else:
                print(f"    route {route_key}: booster substrate-thin (no local + no S3)")
                continue

        sub_booster = xgb.Booster()
        sub_booster.load_model(local_candidate)

        # Sub-booster feature_cols inherited from META meta.feature_cols
        feature_cols = meta['feature_cols']
        X = chunk[feature_cols].fillna(0.0).values
        raw = sub_booster.predict(xgb.DMatrix(X, feature_names=feature_cols))

        chunk_out = chunk[['race_id', 'horse_id']].copy()
        chunk_out['raw_prediction'] = raw
        chunks.append(chunk_out)
        print(f"    route {route_key}: {len(chunk)} rows")

    if not chunks:
        raise ValueError(f"Substrate-broken: META {version_name} produced zero predictions")

    df_out = pd.concat(chunks, ignore_index=True)
    df_out['win_probability'] = df_out.groupby('race_id', group_keys=False)['raw_prediction'].transform(
        _within_race_softmax_transform
    )
    df_out['ensemble_version'] = version_name
    df_out['predicted_at'] = datetime.now(timezone.utc)
    return df_out[['race_id', 'horse_id', 'win_probability', 'ensemble_version', 'predicted_at']]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--artifact', required=True)
    parser.add_argument('--path', required=True, choices=['xgboost', 'closed_form_3F', 'meta_routing'])
    parser.add_argument('--parquet-dir', default='/tmp/option_c_predictions')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    if args.path == 'xgboost':
        df_out = predict_path1_xgboost(args.artifact, args.parquet_dir)
    elif args.path == 'closed_form_3F':
        races = load_races_substrate(FORENSIC_WINDOW_START, FORENSIC_WINDOW_END)
        df_out = predict_path2_closed_form_3F(args.artifact, args.parquet_dir, races)
    elif args.path == 'meta_routing':
        races = load_races_substrate(FORENSIC_WINDOW_START, FORENSIC_WINDOW_END)
        df_out = predict_path3_meta_routing(args.artifact, args.parquet_dir, races)

    df_out['horse_id'] = df_out['horse_id'].astype(str)
    df_out.to_parquet(args.output, index=False)
    print(f"Generated {len(df_out)} predictions across {df_out['race_id'].nunique()} races → {args.output}")


if __name__ == '__main__':
    main()
