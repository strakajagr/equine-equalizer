"""
LSTM Form Trajectory (Layer 5)
Reads last N races as a time series.
Predicts: will next race speed figure improve vs sequence average?
"""

SEQUENCE_LENGTH = 5
MIN_SEQUENCE_LENGTH = 3
FEATURES_PER_STEP = 8

SEQUENCE_FEATURES = [
    'computed_speed_figure',
    'finish_position_norm',
    'early_pace_figure',
    'late_pace_figure',
    'days_since_last_race',
    'purse',
    'field_size',
    'closing_odds',
]

LSTM_PARAMS = {
    'hidden_size': 32,
    'num_layers': 2,
    'dropout': 0.3,
    'learning_rate': 0.001,
    'epochs': 50,
    'batch_size': 256,
    'patience': 10,
}
