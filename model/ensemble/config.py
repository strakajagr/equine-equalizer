"""
Stacking Ensemble (Layer 7) — PRIMARY prediction model.
Logistic regression meta-learner combining all layer outputs.
Trained on 2025 held-out data (out-of-fold for all base models).
Output goes into wr_predictions as the main prediction for ALL horses.
"""

ENSEMBLE_FEATURES = [
    'win_prob',          # Layer 1: P(win) raw sigmoid
    'rank_score',        # Layer 2: ranker output
    'longshot_prob',     # Layer 4: RF P(longshot win)
    'trajectory_score',  # Layer 5: LSTM trajectory (-1 to +1)
    'angle_ev',          # Layer 6: best angle expected value
    'angle_posterior',   # Layer 6: best angle posterior mean
    'closing_odds',      # Market odds (raw)
    'morning_line_odds', # Morning line
    'race_quality_tier', # Race context
    'field_size',        # Race context
]
