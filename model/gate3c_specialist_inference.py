"""Gate 3C §2 — score the 35 active specialist + ensemble-input models on
the leak-free OOS window. End the partial audit.

For each (race, horse) in the OOS window:
  1. Build the full FE matrix (build_feature_matrix, all features)
  2. For each active model in (pl_core_*, win_prob_core_*, rk_full_*,
     wp_full_*, wr_base, wr_odds, ranker_full, win_prob_full,
     win_prob_odds): load XGB JSON, slice the matrix to its feature_list,
     predict.
  3. Output CSV: race_id, horse_id, race_date, track_code, race_number,
     <one column per model>

Then a small post-processor (run locally) does the top-K containment scoring.
"""
import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import boto3
import numpy as np
import pandas as pd
import xgboost as xgb

sys.path.insert(0, str(Path(__file__).parent))

from shared.data_loader import build_feature_matrix

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

S3_BUCKET = 'equine-model-artifacts'
S3_PREFIX = 'gate3c'


def load_active_specialists(conn):
    """Pull active specialist + ensemble-input model versions with their
    feature_lists from the DB."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT model_version_id, version_name, model_type,
                   s3_artifact_path, feature_list
            FROM model_versions
            WHERE is_active = TRUE
              AND (model_type LIKE 'pl_core_%'
                   OR model_type LIKE 'win_prob_core_%'
                   OR model_type LIKE 'rk_full_%'
                   OR model_type LIKE 'wp_full_%'
                   OR model_type IN ('ranker_full','wr_base','wr_odds',
                                     'win_prob_full','win_prob_odds'))
            ORDER BY model_type
        """)
        rows = cur.fetchall()
    return [dict(r) for r in rows]


def download_artifact(s3_path, local_dir):
    """Download s3:// path to local; return local path."""
    parts = s3_path[5:].split('/', 1)
    bucket, key = parts[0], parts[1]
    local = os.path.join(local_dir, os.path.basename(key))
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.download_file(bucket, key, local)
    return local


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', default='2026-05-02')
    parser.add_argument('--end', default='2026-05-17')
    args = parser.parse_args()

    t0 = time.time()
    logger.info("Gate 3C §2 — specialist inference on leak-free OOS")

    # 1. Build FE matrix (no LSTM — specialists don't use trajectory)
    from shared.data_loader import _get_conn
    conn = _get_conn()
    specialists = load_active_specialists(conn)
    logger.info(f"Loaded {len(specialists)} active specialist models")
    conn.close()

    # FE matrix
    logger.info("Building full FE matrix (2022-2026)")
    features_df, labels_df = build_feature_matrix(
        conn=None, start_year=2022, end_year=2026, include_odds=True,
        lstm_model=None,  # specialists don't use trajectory
    )
    logger.info(f"  FE matrix: {len(features_df):,} rows × {len(features_df.columns)} cols")

    # Filter to OOS window
    labels_df['race_date'] = pd.to_datetime(labels_df['race_date'])
    eval_mask = ((labels_df['race_date'] >= pd.Timestamp(args.start)) &
                 (labels_df['race_date'] <= pd.Timestamp(args.end)))
    eval_pps = labels_df.loc[eval_mask, 'pp_id'].values
    eval_features = features_df[features_df['pp_id'].isin(eval_pps)].copy()
    eval_labels = labels_df[labels_df['pp_id'].isin(eval_pps)].copy()
    logger.info(f"  OOS slice: {len(eval_features):,} rows")

    # Re-parse race_key into track_code / race_date / race_number
    # race_key format: 'TRACK_YYYYMMDD_N'
    rk = eval_labels['race_key'].astype(str)
    eval_labels['track_code'] = rk.str.split('_').str[0]
    eval_labels['race_number'] = rk.str.split('_').str[-1].astype(int)
    eval_labels['race_date_str'] = eval_labels['race_date'].dt.strftime('%Y-%m-%d')

    # Output frame keyed by pp_id
    out = eval_labels[['pp_id', 'horse_id', 'race_date_str',
                       'track_code', 'race_number', 'race_key']].copy()
    out = out.rename(columns={'race_date_str': 'race_date'})

    # 2. Score each specialist
    local_dir = '/tmp/specialist_artifacts'
    os.makedirs(local_dir, exist_ok=True)
    for spec in specialists:
        mt = spec['model_type']
        s3p = spec['s3_artifact_path']
        feat_list_raw = spec['feature_list']
        # feature_list is jsonb in DB; format is {"features": [...]} — extract the list
        if isinstance(feat_list_raw, str):
            feat_list_raw = json.loads(feat_list_raw)
        if isinstance(feat_list_raw, dict):
            feat_list = feat_list_raw.get('features', list(feat_list_raw.keys()))
        else:
            feat_list = feat_list_raw

        try:
            local = download_artifact(s3p, local_dir)
            booster = xgb.Booster()
            booster.load_model(local)
            # Extract the feature columns; fill missing with NaN (XGB handles)
            missing = [f for f in feat_list if f not in eval_features.columns]
            if missing:
                logger.warning(f"  [{mt}] missing {len(missing)} feats from FE matrix: {missing[:5]}")
                for f in missing:
                    eval_features[f] = float('nan')
            X = eval_features[feat_list].values
            dmat = xgb.DMatrix(X, feature_names=feat_list)
            preds = booster.predict(dmat)
            out[f'm__{mt}'] = preds
            logger.info(f"  [{mt:<28}] scored {len(preds):,} rows  "
                        f"min/mean/max={preds.min():.3f}/{preds.mean():.3f}/{preds.max():.3f}")
        except Exception as e:
            logger.warning(f"  [{mt}] scoring failed: {e}")
            out[f'm__{mt}'] = float('nan')

    # 3. Save CSV
    out_csv = '/tmp/gate3c_specialist_predictions.csv'
    out.to_csv(out_csv, index=False)
    logger.info(f"Wrote {out_csv} ({len(out):,} rows × {len(out.columns)} cols)")
    ts = datetime.utcnow().strftime('%Y%m%d_%H%M')
    s3 = boto3.client('s3', region_name='us-east-1')
    try:
        s3.upload_file(out_csv, S3_BUCKET, f'{S3_PREFIX}/specialist_predictions_{ts}.csv')
        logger.info(f"Uploaded s3://{S3_BUCKET}/{S3_PREFIX}/specialist_predictions_{ts}.csv")
    except Exception as e:
        logger.warning(f"S3 upload failed: {e}")

    logger.info(f"Total runtime: {time.time() - t0:.1f}s")


if __name__ == '__main__':
    main()
