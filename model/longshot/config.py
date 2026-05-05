"""
RF Longshot Classifier (Layer 4)
Binary: did this horse WIN at closing_odds >= 10.0 (10-1)?
Uses scikit-learn RandomForestClassifier.
"""
import numpy as np
import pandas as pd

RF_PARAMS = {
    'n_estimators': 500,
    'max_depth': 10,
    'min_samples_leaf': 20,
    'min_samples_split': 40,
    'max_features': 'sqrt',
    'class_weight': 'balanced',
    'random_state': 42,
    'n_jobs': -1,
}

LONGSHOT_ODDS_THRESHOLD = 10.0


def compute_longshot_labels(labels_df: pd.DataFrame) -> np.ndarray:
    """1 = won AND closing_odds >= 10-1. 0 = everything else."""
    labels = np.zeros(len(labels_df), dtype=np.float32)
    is_winner = labels_df['finish_position'] == 1
    is_longshot = labels_df['closing_odds'] >= LONGSHOT_ODDS_THRESHOLD
    labels[is_winner & is_longshot] = 1.0
    return labels
