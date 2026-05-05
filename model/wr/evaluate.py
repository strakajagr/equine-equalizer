"""
Win Rate Model — Evaluate a saved model artifact.
Usage: python evaluate.py --model-version v_base_20260318_1200
"""
import argparse
import json
import logging
from pathlib import Path

import boto3
import numpy as np
import pandas as pd
import xgboost as xgb
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.data_loader import build_feature_matrix, _get_conn
from shared.evaluation import full_evaluation
from wr.train import predictions_to_probs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOCAL_ARTIFACTS = Path(__file__).parent / 'artifacts'
S3_BUCKET = 'equine-model-artifacts'


def load_model(version: str) -> tuple[xgb.Booster, dict]:
    local_model = LOCAL_ARTIFACTS / f'{version}.json'
    local_meta  = LOCAL_ARTIFACTS / f'{version}_meta.json'

    if not local_model.exists():
        logger.info(f"Downloading {version} from S3...")
        s3 = boto3.client('s3', region_name='us-east-1')
        LOCAL_ARTIFACTS.mkdir(parents=True, exist_ok=True)
        for suffix in ['.json', '_meta.json']:
            s3.download_file(
                S3_BUCKET, f'wr/{version}{suffix}',
                str(LOCAL_ARTIFACTS / f'{version}{suffix}')
            )

    booster = xgb.Booster()
    booster.load_model(str(local_model))
    meta = json.loads(local_meta.read_text())
    return booster, meta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-version', required=True)
    parser.add_argument('--eval-year', type=int, default=2025)
    args = parser.parse_args()

    booster, meta = load_model(args.model_version)
    feature_names = meta['feature_names']
    include_odds = any(f in feature_names for f in
                       ['closing_odds', 'log_closing_odds', 'odds_move'])

    conn = _get_conn()
    features_df, labels_df = build_feature_matrix(
        conn, start_year=args.eval_year, end_year=args.eval_year,
        include_odds=include_odds,
    )
    conn.close()

    dmat = xgb.DMatrix(
        features_df[feature_names].values.astype(np.float32),
        feature_names=feature_names,
    )
    raw_preds = booster.predict(dmat)
    eval_df = labels_df.copy()
    eval_df['predicted_score'] = raw_preds
    eval_df = predictions_to_probs(eval_df)

    full_evaluation(eval_df, model_name=f'WR {args.model_version}')


if __name__ == '__main__':
    main()
