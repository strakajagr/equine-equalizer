"""
LSTM Form Trajectory (Layer 5)
Reads horse's last N races as a sequence, predicts improvement.
Output: trajectory_score -1 (declining) to +1 (improving).

Run on Fargate:
  aws ecs run-task --cluster equine-cluster \
    --task-definition equine-training-manual --launch-type FARGATE \
    --overrides '{"containerOverrides":[{"name":"training","command":["model/trajectory/train.py"]}]}'
"""

import argparse
import json
import logging
import pickle
import sys
from datetime import datetime
from pathlib import Path

import boto3
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.data_loader import _get_conn
from trajectory.config import (
    SEQUENCE_LENGTH, MIN_SEQUENCE_LENGTH, FEATURES_PER_STEP,
    SEQUENCE_FEATURES, LSTM_PARAMS,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

S3_BUCKET = 'equine-model-artifacts'
S3_PREFIX = 'trajectory'
LOCAL_ARTIFACTS = Path(__file__).parent / 'artifacts'


class TrajectoryLSTM(nn.Module):
    def __init__(self, input_size=8, hidden_size=32, num_layers=2, dropout=0.3):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size, hidden_size=hidden_size,
            num_layers=num_layers, dropout=dropout, batch_first=True
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_hidden = lstm_out[:, -1, :]
        return self.fc(last_hidden).squeeze(-1)  # Raw logits, sigmoid in loss

    def predict_proba(self, x):
        """Get probabilities (for inference/eval)."""
        with torch.no_grad():
            logits = self.forward(x)
            return torch.sigmoid(logits)


def build_sequences(conn, end_date: str = None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Build (input_sequences, labels, years) from past_performances.
    Each sequence = last N races for a horse, target = did speed improve?

    end_date (YYYY-MM-DD, optional): if provided, only PPs with
    race_date <= end_date are loaded. Used by Gate 3 to retrain with a
    strict cutoff (2025-12-31) so the 2026 OOS eval is leak-free.
    """
    logger.info(f"Loading past performances for sequence building (end_date={end_date or 'unbounded'})...")
    with conn.cursor() as cur:
        if end_date:
            cur.execute("""
                SELECT horse_id, race_date, computed_speed_figure,
                       finish_position, field_size, early_pace_figure,
                       late_pace_figure, days_since_last_race, purse,
                       closing_odds
                FROM past_performances
                WHERE computed_speed_figure IS NOT NULL
                  AND finish_position IS NOT NULL
                  AND finish_position < 90
                  AND race_date >= DATE '2022-01-01'
                  AND race_date <= %s::date
                ORDER BY horse_id, race_date
            """, (end_date,))
        else:
            cur.execute("""
                SELECT horse_id, race_date, computed_speed_figure,
                       finish_position, field_size, early_pace_figure,
                       late_pace_figure, days_since_last_race, purse,
                       closing_odds
                FROM past_performances
                WHERE computed_speed_figure IS NOT NULL
                  AND finish_position IS NOT NULL
                  AND finish_position < 90
                  AND EXTRACT(YEAR FROM race_date) BETWEEN 2022 AND 2026
                ORDER BY horse_id, race_date
            """)
        rows = cur.fetchall()

    df = pd.DataFrame([dict(r) for r in rows])
    df['race_date'] = pd.to_datetime(df['race_date'])
    df['finish_position_norm'] = df['finish_position'] / df['field_size'].clip(lower=1)

    logger.info(f"Loaded {len(df):,} PP rows for {df['horse_id'].nunique():,} horses")

    sequences = []
    labels = []
    years = []

    for horse_id, group in df.groupby('horse_id'):
        group = group.sort_values('race_date').reset_index(drop=True)
        if len(group) < MIN_SEQUENCE_LENGTH + 1:
            continue

        for i in range(MIN_SEQUENCE_LENGTH, len(group)):
            start = max(0, i - SEQUENCE_LENGTH)
            seq_rows = group.iloc[start:i]
            target_row = group.iloc[i]

            # Build sequence features
            seq = np.zeros((SEQUENCE_LENGTH, FEATURES_PER_STEP), dtype=np.float32)
            offset = SEQUENCE_LENGTH - len(seq_rows)  # left-pad with zeros

            for j, (_, row) in enumerate(seq_rows.iterrows()):
                seq[offset + j] = [
                    float(row.get('computed_speed_figure') or 0),
                    float(row.get('finish_position_norm') or 0.5),
                    float(row.get('early_pace_figure') or 24),
                    float(row.get('late_pace_figure') or 38),
                    float(row.get('days_since_last_race') or 30),
                    float(row.get('purse') or 0),
                    float(row.get('field_size') or 8),
                    float(row.get('closing_odds') or 5),
                ]

            # Label: did speed figure improve vs sequence average?
            seq_figs = [float(r.get('computed_speed_figure') or 0)
                        for _, r in seq_rows.iterrows()
                        if r.get('computed_speed_figure')]
            avg_fig = np.mean(seq_figs) if seq_figs else 0
            target_fig = float(target_row.get('computed_speed_figure') or 0)
            label = 1.0 if target_fig > avg_fig else 0.0

            sequences.append(seq)
            labels.append(label)
            years.append(target_row['race_date'].year)

    return np.array(sequences), np.array(labels, dtype=np.float32), np.array(years)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--end-date', default=None,
                        help='Strict cutoff for PP loading (YYYY-MM-DD). '
                             'Gate 3 uses 2025-12-31 to make the 2026 OOS '
                             'eval leak-free w.r.t. LSTM training.')
    args = parser.parse_args()

    logger.info(f"LSTM Form Trajectory (Layer 5) training starting (end_date={args.end_date or 'unbounded'})")
    conn = _get_conn()

    sequences, labels, years = build_sequences(conn, end_date=args.end_date)
    conn.close()

    n_pos = int(labels.sum())
    logger.info(f"Built {len(sequences):,} sequences. "
                f"Improved: {n_pos:,} ({n_pos/len(labels)*100:.1f}%)")

    # Temporal split (years is per-sequence)
    #
    # Default path (no --end-date): train on 2022-2025, val on 2026.
    # Gate 3 path (--end-date=2025-12-31): no 2026 data loaded at all, so
    # use the last available year as the validation slice.
    max_year = int(years.max())
    train_mask = years < max_year
    val_mask = years == max_year

    X_train_raw = sequences[train_mask]
    y_train = labels[train_mask]
    X_val_raw = sequences[val_mask]
    y_val = labels[val_mask]

    logger.info(f"Train: {len(X_train_raw):,}  Val: {len(X_val_raw):,}")

    # Replace NaN/Inf with 0 before scaling
    X_train_raw = np.nan_to_num(X_train_raw, nan=0.0, posinf=0.0, neginf=0.0)
    X_val_raw = np.nan_to_num(X_val_raw, nan=0.0, posinf=0.0, neginf=0.0)

    # Normalize features (fit on train only)
    scaler = MinMaxScaler(clip=True)
    n_train = len(X_train_raw)
    flat_train = X_train_raw.reshape(-1, FEATURES_PER_STEP)
    scaler.fit(flat_train)
    X_train = scaler.transform(flat_train).reshape(n_train, SEQUENCE_LENGTH, FEATURES_PER_STEP)
    flat_val = X_val_raw.reshape(-1, FEATURES_PER_STEP)
    X_val = scaler.transform(flat_val).reshape(len(X_val_raw), SEQUENCE_LENGTH, FEATURES_PER_STEP)

    # Final NaN check after scaling
    X_train = np.nan_to_num(X_train, nan=0.0)
    X_val = np.nan_to_num(X_val, nan=0.0)

    # PyTorch datasets
    train_ds = TensorDataset(
        torch.FloatTensor(X_train), torch.FloatTensor(y_train)
    )
    val_ds = TensorDataset(
        torch.FloatTensor(X_val), torch.FloatTensor(y_val)
    )
    train_loader = DataLoader(train_ds, batch_size=LSTM_PARAMS['batch_size'], shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=LSTM_PARAMS['batch_size'])

    # Model
    model = TrajectoryLSTM(
        input_size=FEATURES_PER_STEP,
        hidden_size=LSTM_PARAMS['hidden_size'],
        num_layers=LSTM_PARAMS['num_layers'],
        dropout=LSTM_PARAMS['dropout'],
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=LSTM_PARAMS['learning_rate'])
    criterion = nn.BCEWithLogitsLoss()  # Numerically stable: combines sigmoid + BCE

    # Training loop with early stopping
    best_val_loss = float('inf')
    best_state = model.state_dict().copy()
    patience_counter = 0

    for epoch in range(LSTM_PARAMS['epochs']):
        model.train()
        train_loss = 0
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            pred = model(X_batch)
            loss = criterion(pred, y_batch)
            if torch.isnan(loss):
                continue
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            train_loss += loss.item()
        train_loss /= len(train_loader)

        model.eval()
        val_loss = 0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                pred = model(X_batch)
                val_loss += criterion(pred, y_batch).item()
        val_loss /= len(val_loader)

        if epoch % 5 == 0:
            logger.info(f"Epoch {epoch:3d}: train_loss={train_loss:.4f}  val_loss={val_loss:.4f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            best_state = model.state_dict().copy()
        else:
            patience_counter += 1
            if patience_counter >= LSTM_PARAMS['patience']:
                logger.info(f"Early stopping at epoch {epoch}")
                break

    # Load best model
    model.load_state_dict(best_state)

    # Evaluate
    model.eval()
    all_preds = []
    with torch.no_grad():
        for X_batch, _ in val_loader:
            probs = model.predict_proba(X_batch)
            all_preds.extend(probs.numpy())
    val_probs = np.array(all_preds)
    val_preds_binary = (val_probs > 0.5).astype(float)
    acc = accuracy_score(y_val, val_preds_binary)

    # Correlation between trajectory score and actual speed delta
    # (trajectory_score = sigmoid * 2 - 1, range -1 to +1)
    trajectory_scores = val_probs * 2.0 - 1.0
    corr = float(np.corrcoef(trajectory_scores, y_val)[0, 1]) if len(y_val) > 1 else 0.0

    # Top quartile analysis
    q75 = np.percentile(trajectory_scores, 75)
    top_q = y_val[trajectory_scores >= q75]
    top_q_rate = float(top_q.mean()) if len(top_q) > 0 else 0.0
    base_rate = float(y_val.mean())

    logger.info("=" * 56)
    logger.info("  LSTM Trajectory — Evaluation")
    logger.info("=" * 56)
    logger.info(f"  accuracy:        {acc:.3f}")
    logger.info(f"  correlation:     {corr:.3f}")
    logger.info(f"  base_improve:    {base_rate:.3f}")
    logger.info(f"  top_q_improve:   {top_q_rate:.3f} (top 25% trajectory)")
    logger.info(f"  val_loss:        {best_val_loss:.4f}")
    logger.info("=" * 56)

    print("\n" + "=" * 56)
    print("  LSTM Trajectory — Evaluation")
    print("=" * 56)
    print(f"  accuracy:        {acc:.3f}")
    print(f"  correlation:     {corr:.3f}")
    print(f"  base_improve:    {base_rate:.3f}")
    print(f"  top_q_improve:   {top_q_rate:.3f}")
    print(f"  val_loss:        {best_val_loss:.4f}")
    print("=" * 56)

    # Save artifacts
    LOCAL_ARTIFACTS.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M')
    version = f'trajectory_lstm_{timestamp}'

    model_file = LOCAL_ARTIFACTS / f'{version}.pt'
    torch.save(model.state_dict(), str(model_file))

    scaler_file = LOCAL_ARTIFACTS / f'{version}_scaler.pkl'
    with open(scaler_file, 'wb') as f:
        pickle.dump(scaler, f)

    meta = {
        'version': version, 'model_type': 'trajectory_lstm',
        'architecture': {'input_size': FEATURES_PER_STEP, **LSTM_PARAMS},
        'sequence_features': SEQUENCE_FEATURES,
        'metrics': {'accuracy': acc, 'correlation': corr,
                    'top_q_improve': top_q_rate, 'val_loss': best_val_loss},
        'training_sequences': len(X_train_raw),
        'trained_at': datetime.utcnow().isoformat(),
    }
    meta_file = LOCAL_ARTIFACTS / f'{version}_meta.json'
    meta_file.write_text(json.dumps(meta, indent=2))

    s3 = boto3.client('s3', region_name='us-east-1')
    for lp in [model_file, scaler_file, meta_file]:
        s3_key = f'{S3_PREFIX}/{lp.name}'
        try:
            s3.upload_file(str(lp), S3_BUCKET, s3_key)
            logger.info(f'Uploaded s3://{S3_BUCKET}/{s3_key}')
        except Exception as e:
            logger.warning(f'S3 upload failed: {e}')

    # § 4.33: register in model_versions post-S3-upload
    try:
        from training.registration import register_trained_artifact
        register_trained_artifact(
            version_name=version,
            model_type='trajectory_lstm',
            s3_artifact_path=f's3://{S3_BUCKET}/{S3_PREFIX}/{model_file.name}',
            training_metadata={
                'feature_names': SEQUENCE_FEATURES,
                'hyperparameters': {
                    'input_size': FEATURES_PER_STEP, **LSTM_PARAMS,
                },
                'training_race_count': len(X_train_raw),
                'trajectory_accuracy': acc,
                'trajectory_correlation': corr,
                'trajectory_top_q_improve': top_q_rate,
                'trajectory_val_loss': float(best_val_loss),
                'notes': (
                    f'trajectory LSTM training; accuracy={acc:.3f} '
                    f'correlation={corr:.3f} val_loss={best_val_loss:.4f}'
                ),
            },
        )
    except Exception as e:
        logger.warning(f'model_versions registration failed for {version}: {e}')

    logger.info(f"LSTM Trajectory training complete: {version}")


if __name__ == '__main__':
    main()
