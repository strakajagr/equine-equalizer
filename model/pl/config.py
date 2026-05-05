"""
P&L Optimization Model (Path 2) — Configuration
Same clean EV labels as WR. Always odds-aware.
Kelly is ONLY used at inference time for bet sizing, never in training labels.
"""
from wr.config import (
    compute_ev_labels,
    XGB_PARAMS,
    WORKOUT_XGB_PARAMS,
    NUM_ROUNDS,
    EARLY_STOPPING_ROUNDS,
    WORKOUT_NUM_ROUNDS,
    WORKOUT_EARLY_STOPPING_ROUNDS,
)

# Re-export under PL names for clarity in train.py imports
XGB_PARAMS_PL = XGB_PARAMS
WORKOUT_XGB_PARAMS_PL = WORKOUT_XGB_PARAMS
