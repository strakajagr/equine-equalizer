"""
Win Rate Model (Path 1) — Configuration
Trains with EV (Expected Value) labels.
Objective: reg:squarederror (NOT rank:pairwise).
"""
import numpy as np
import pandas as pd

AVG_WIN_PAYOUT = 12.18   # fallback for winners with missing payout

XGB_PARAMS = {
    'objective':        'reg:squarederror',
    'eval_metric':      'rmse',
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

NUM_ROUNDS           = 1000
EARLY_STOPPING_ROUNDS = 50

WORKOUT_XGB_PARAMS = {
    'objective':        'reg:squarederror',
    'eval_metric':      'rmse',
    'learning_rate':    0.03,
    'max_depth':        4,
    'min_child_weight': 30,
    'subsample':        0.8,
    'colsample_bytree': 0.8,
    'reg_alpha':        0.5,
    'reg_lambda':       2.0,
    'tree_method':      'hist',
    'random_state':     42,
}
WORKOUT_NUM_ROUNDS           = 500
WORKOUT_EARLY_STOPPING_ROUNDS = 30


def compute_ev_labels(labels_df: pd.DataFrame) -> np.ndarray:
    """
    EV label per horse per race:
      winners with payout  → actual win_payout (per $2 bet)
      winners without      → AVG_WIN_PAYOUT
      losers               → -1.0

    This trains the model to score each horse by its expected
    monetary return per $2 wagered.
    """
    labels = np.full(len(labels_df), -1.0, dtype=np.float32)
    winners     = labels_df['finish_position'] == 1
    has_payout  = labels_df['win_payout'] > 0
    labels[winners &  has_payout] = labels_df.loc[winners & has_payout,  'win_payout'].values.astype(np.float32)
    labels[winners & ~has_payout] = AVG_WIN_PAYOUT
    return labels
