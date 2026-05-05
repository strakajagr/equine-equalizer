"""
Finish Position Ranker (Layer 2)
Objective: rank:pairwise (LambdaMART)
Learns: who finishes 1st, 2nd, 3rd, etc.
Two models: ranker_core (58 feat) and ranker_full (66 feat)
"""
import numpy as np
import pandas as pd

XGB_PARAMS = {
    'objective':        'rank:pairwise',
    'eval_metric':      'ndcg',
    'learning_rate':    0.05,
    'max_depth':        6,
    'min_child_weight': 20,
    'subsample':        0.8,
    'colsample_bytree': 0.8,
    'reg_alpha':        0.1,
    'reg_lambda':       1.0,
    'tree_method':      'hist',
    'random_state':     42,
}

NUM_ROUNDS = 1000
EARLY_STOPPING_ROUNDS = 50


def compute_rank_labels(labels_df: pd.DataFrame) -> np.ndarray:
    """
    Inverted finish position: 1st place gets highest score.
    For a 7-horse race: 1st=7, 2nd=6, ..., 7th=1.
    Horses with invalid finish_position get 0.
    """
    labels = np.zeros(len(labels_df), dtype=np.float32)
    for race_key, group in labels_df.groupby('race_key'):
        field_size = len(group)
        for idx in group.index:
            fp = int(labels_df.loc[idx, 'finish_position'])
            if 1 <= fp <= field_size:
                labels[idx] = float(field_size - fp + 1)
            else:
                labels[idx] = 0.0
    return labels
