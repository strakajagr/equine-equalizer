"""LSTM trajectory model loader — shared by training FE pipeline and
inference. The class definition mirrors model/trajectory/train.py exactly
(same hidden_size, num_layers, dropout, output head).

Used by:
  - model/shared/data_loader.py during training feature matrix build
  - any inference path that wants direct loading without DB metadata
"""
import logging
import os
import pickle
from typing import Optional

import boto3
import torch
import torch.nn as nn

logger = logging.getLogger(__name__)


class TrajectoryLSTM(nn.Module):
    """Must match model/trajectory/train.py architecture exactly."""

    def __init__(self, input_size: int = 8, hidden_size: int = 32,
                 num_layers: int = 2, dropout: float = 0.3):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size, hidden_size=hidden_size,
            num_layers=num_layers, dropout=dropout, batch_first=True,
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_hidden = lstm_out[:, -1, :]
        return self.fc(last_hidden).squeeze(-1)

    def predict_proba(self, x):
        with torch.no_grad():
            logits = self.forward(x)
            return torch.sigmoid(logits)


def load_lstm_from_s3(
    s3_path: str,
    local_dir: str = '/tmp/lstm-loader',
) -> tuple[TrajectoryLSTM, Optional[object]]:
    """Download a trajectory_lstm artifact (model + scaler) from S3 and
    return (model, scaler). s3_path looks like
        s3://equine-model-artifacts/trajectory/trajectory_lstm_X.pt
    Scaler is at the same prefix with `_scaler.pkl` suffix.
    """
    if not s3_path.startswith('s3://'):
        raise ValueError(f"Expected s3:// URI, got {s3_path}")

    os.makedirs(local_dir, exist_ok=True)
    parts = s3_path[5:].split('/', 1)
    bucket = parts[0]
    key = parts[1]

    local_pt = os.path.join(local_dir, os.path.basename(key))
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.download_file(bucket, key, local_pt)

    # Scaler at same prefix + _scaler.pkl
    base_key = key.rsplit('.', 1)[0]
    scaler_key = f'{base_key}_scaler.pkl'
    local_scaler = os.path.join(local_dir, os.path.basename(scaler_key))
    scaler = None
    try:
        s3.download_file(bucket, scaler_key, local_scaler)
        with open(local_scaler, 'rb') as f:
            scaler = pickle.load(f)
    except Exception as e:
        logger.warning(f"LSTM scaler not found at {scaler_key}: {e}")

    model = TrajectoryLSTM()
    model.load_state_dict(torch.load(local_pt, map_location='cpu'))
    model.eval()
    logger.info(f"Loaded LSTM from {s3_path}; scaler={'yes' if scaler else 'NO'}")
    return model, scaler


def load_active_lstm() -> tuple[Optional[TrajectoryLSTM], Optional[object], Optional[str]]:
    """Look up the active trajectory_lstm via model_versions and load it.
    Returns (model, scaler, version_name) — all None if no active row.
    """
    from shared.data_loader import _get_conn  # local to avoid circular
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT version_name, s3_artifact_path FROM model_versions
                WHERE model_type = 'trajectory_lstm' AND is_active = TRUE
                ORDER BY training_date DESC LIMIT 1
            """)
            row = cur.fetchone()
    finally:
        conn.close()
    if row is None:
        logger.warning("No active trajectory_lstm in model_versions")
        return None, None, None
    version_name = row['version_name']
    s3_path = row['s3_artifact_path']
    model, scaler = load_lstm_from_s3(s3_path)
    return model, scaler, version_name
