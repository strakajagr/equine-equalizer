"""
Win Probability Model (Layer 1) — Configuration
Binary classification: 1 = winner, 0 = loser
Objective: binary:logistic
Output: calibrated P(win) directly from sigmoid
"""
import numpy as np
import pandas as pd

XGB_PARAMS = {
    'objective':        'binary:logistic',
    'eval_metric':      'logloss',
    'learning_rate':    0.05,
    'max_depth':        6,
    'min_child_weight': 20,
    'subsample':        0.8,
    'colsample_bytree': 0.8,
    'reg_alpha':        0.1,
    'reg_lambda':       1.0,
    'tree_method':      'hist',
    'random_state':     42,
    'scale_pos_weight': 1.0,  # Set dynamically in train.py
}

NUM_ROUNDS = 1000
EARLY_STOPPING_ROUNDS = 50

# Workout layer — more conservative
WORKOUT_XGB_PARAMS = {
    **XGB_PARAMS,
    'learning_rate':    0.03,
    'max_depth':        4,
    'min_child_weight': 30,
    'reg_alpha':        0.5,
    'reg_lambda':       2.0,
}
WORKOUT_NUM_ROUNDS = 500
WORKOUT_EARLY_STOPPING_ROUNDS = 30


def compute_binary_labels(labels_df: pd.DataFrame) -> np.ndarray:
    """
    Binary labels: 1.0 for winners, 0.0 for losers.
    No payouts, no EV, no Kelly. Pure win/lose.
    """
    labels = np.zeros(len(labels_df), dtype=np.float32)
    labels[labels_df['finish_position'] == 1] = 1.0
    return labels
