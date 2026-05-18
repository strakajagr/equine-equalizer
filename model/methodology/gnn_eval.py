"""
4D Graph Neural Network on trainer-jockey-track bipartite graphs.

Evaluates whether torch_geometric GCN over trainer-track + trainer-jockey
bipartite graphs adds signal beyond flat XGBoost features.

Substrate-pragmatic minimum-viable: small GCN with trainer/jockey/track node
embeddings; trained on is_winner classification with frozen Hybrid C feature
as covariate. Tier 2 EXECUTION re-runs at production scope.
"""

import argparse
import json

import boto3
import numpy as np
import pandas as pd
import psycopg2
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
from sklearn.metrics import roc_auc_score


DB_SECRET_ARN = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'


def get_db_conn():
    sm_client = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm_client.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString'])
    return psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'], password=secret['password'],
    )


def load_substrate(window_start, window_end):
    conn = get_db_conn()
    df = pd.read_sql("""
        SELECT hp.race_id::text AS race_id,
               hp.horse_id::text AS horse_id,
               hp.hybrid_c_win_probability AS hybrid_c_p,
               e.trainer_id::text AS trainer_id,
               e.jockey_id::text AS jockey_id,
               r.track_id::text AS track_id,
               (res.finish_position = 1)::int AS is_winner
        FROM hybrid_c_predictions hp
        JOIN races r ON r.race_id = hp.race_id
        JOIN entries e ON e.race_id = hp.race_id AND e.horse_id::text = hp.horse_id
        LEFT JOIN results res ON res.race_id = hp.race_id AND res.horse_id = e.horse_id
        WHERE hp.ensemble_version = 'option_c_hybrid_ensemble_20260515'
          AND r.race_date BETWEEN %s AND %s
    """, conn, params=[window_start, window_end])
    conn.close()
    return df.dropna(subset=['is_winner', 'trainer_id', 'jockey_id', 'track_id'])


class SmallGCN(torch.nn.Module):
    def __init__(self, n_nodes, hidden=16, out=8):
        super().__init__()
        self.emb = torch.nn.Embedding(n_nodes, hidden)
        self.conv1 = GCNConv(hidden, hidden)
        self.conv2 = GCNConv(hidden, out)

    def forward(self, edge_index, n_nodes):
        x = self.emb(torch.arange(n_nodes))
        x = F.relu(self.conv1(x, edge_index))
        x = self.conv2(x, edge_index)
        return x


def evaluate(window_start, window_end, output_path):
    df = load_substrate(window_start, window_end)
    print(f"Loaded {len(df)} rows")
    if len(df) < 100:
        result = {'verdict': 'substrate-thin', 'n_observations': len(df)}
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        return result

    # Build unified node id space: trainer / jockey / track
    trainers = sorted(df['trainer_id'].unique())
    jockeys = sorted(df['jockey_id'].unique())
    tracks = sorted(df['track_id'].unique())
    trainer_idx = {t: i for i, t in enumerate(trainers)}
    jockey_idx = {j: i + len(trainers) for i, j in enumerate(jockeys)}
    track_idx = {tk: i + len(trainers) + len(jockeys) for i, tk in enumerate(tracks)}
    n_nodes = len(trainers) + len(jockeys) + len(tracks)

    # Edges: trainer-jockey + trainer-track per row
    edges = []
    for _, row in df.iterrows():
        t = trainer_idx[row['trainer_id']]
        j = jockey_idx[row['jockey_id']]
        tk = track_idx[row['track_id']]
        edges.append([t, j])
        edges.append([j, t])
        edges.append([t, tk])
        edges.append([tk, t])
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()

    # 80/20 race-level split for evaluation
    np.random.seed(42)
    races = sorted(df['race_id'].unique())
    np.random.shuffle(races)
    split = int(len(races) * 0.8)
    train_mask_arr = df['race_id'].isin(set(races[:split])).values
    test_mask_arr = ~train_mask_arr

    # Substrate-pragmatic minimum-viable: GCN node embedding + (trainer_emb + jockey_emb + track_emb + hybrid_c_p) → logit
    model = SmallGCN(n_nodes)
    opt = torch.optim.Adam(model.parameters(), lr=0.01)

    # Per-row feature: GCN output for trainer + jockey + track concatenated
    hp_t = torch.tensor(df['hybrid_c_p'].fillna(0.0).values, dtype=torch.float)
    y_t = torch.tensor(df['is_winner'].values, dtype=torch.float)
    t_ids = torch.tensor(df['trainer_id'].map(trainer_idx).values, dtype=torch.long)
    j_ids = torch.tensor(df['jockey_id'].map(jockey_idx).values, dtype=torch.long)
    tk_ids = torch.tensor(df['track_id'].map(track_idx).values, dtype=torch.long)

    # Substrate-pragmatic head: gcn_emb (24-d) + hybrid_c_p → logit
    head = torch.nn.Linear(24 + 1, 1)
    opt_head = torch.optim.Adam(head.parameters(), lr=0.01)

    # Train 30 epochs
    model.train()
    head.train()
    for epoch in range(30):
        opt.zero_grad()
        opt_head.zero_grad()
        gcn_out = model(edge_index, n_nodes)
        row_emb = torch.cat([gcn_out[t_ids], gcn_out[j_ids], gcn_out[tk_ids]], dim=1)
        x = torch.cat([row_emb, hp_t.unsqueeze(1)], dim=1)
        logit = head(x).squeeze()
        train_mask_t = torch.tensor(train_mask_arr)
        loss = F.binary_cross_entropy_with_logits(logit[train_mask_t], y_t[train_mask_t])
        loss.backward()
        opt.step()
        opt_head.step()

    # Evaluate
    model.eval()
    head.eval()
    with torch.no_grad():
        gcn_out = model(edge_index, n_nodes)
        row_emb = torch.cat([gcn_out[t_ids], gcn_out[j_ids], gcn_out[tk_ids]], dim=1)
        x = torch.cat([row_emb, hp_t.unsqueeze(1)], dim=1)
        logit = head(x).squeeze()
        probs = torch.sigmoid(logit).numpy()

    y_test = df.loc[test_mask_arr, 'is_winner'].values
    p_test = probs[test_mask_arr]
    p_baseline = df.loc[test_mask_arr, 'hybrid_c_p'].fillna(0.0).values

    try:
        gnn_auc = float(roc_auc_score(y_test, p_test))
        baseline_auc = float(roc_auc_score(y_test, p_baseline))
    except Exception:
        gnn_auc = baseline_auc = None

    delta = (gnn_auc - baseline_auc) if (gnn_auc and baseline_auc) else None

    if delta is not None and delta > 0.01:
        verdict = 'substrate-validated production candidate'
    elif delta is not None and abs(delta) < 0.005:
        verdict = 'null (no GNN signal)'
    else:
        verdict = 'substrate-investigation-required'

    result = {
        'verdict': verdict,
        'gnn_auc': gnn_auc, 'baseline_auc': baseline_auc,
        'delta_auc': delta,
        'n_nodes': n_nodes, 'n_edges': edge_index.shape[1],
        'n_observations': int(len(df)),
    }
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Verdict: {verdict}; gnn_auc={gnn_auc} baseline_auc={baseline_auc}")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--window-start', default='2026-05-02')
    parser.add_argument('--window-end', default='2026-05-17')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    evaluate(args.window_start, args.window_end, args.output)


if __name__ == '__main__':
    main()
