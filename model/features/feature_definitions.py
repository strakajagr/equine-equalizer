FEATURE_GROUPS = {
    'speed': {
        'features': [
            'beyer_last',
            'beyer_avg_3',
            'beyer_trend',
            'beyer_best_career',
            'beyer_best_90d',
            'raw_speed_last',
            'raw_speed_avg_3',
            'raw_speed_trend',
            'raw_speed_vs_par',
            'beyer_vs_raw_discrepancy',
            'speed_on_todays_surface',
            'speed_at_todays_distance',
            'speed_at_todays_track',
            'speed_in_todays_conditions',
            'beyer_vs_field_avg',
            'winner_beyer_last_race',
            'speed_sample_size',
            'raw_speed_sample_size',
        ],
        'description': (
            'Speed figures and raw times. '
            'Raw speed index is final_time/furlongs '
            '— physics, not adjusted variants.'
        )
    },
    'pace': {
        'features': [
            'avg_call1_position',
            'running_style_numeric',
            'pace_delta_avg',
            'best_pace_delta',
            'front_runner_count_today',
            'pace_scenario_today',
            'style_scenario_match',
            'avg_early_pace_pressure',
            'win_rate_fast_pace',
            'win_rate_slow_pace',
            'avg_stretch_gain',
            'pace_sample_size',
        ],
        'description': (
            'Running style and pace scenario. '
            'Style-scenario match encodes whether '
            "today's field setup favors this horse."
        )
    },
    'workouts': {
        'features': [
            'days_since_last_workout',
            'workout_count_30d',
            'bullet_work_14d',
            'bullet_count_30d',
            'best_workout_speed_index',
            'workout_speed_trend',
            'gate_work_30d',
            'workout_frequency_score',
        ],
        'description': (
            'Workout patterns. Bullet works and '
            'high frequency indicate trainer intent.'
        )
    },
    'trainer_jockey': {
        'features': [
            'trainer_win_rate',
            'trainer_itm_rate',
            'trainer_layoff_win_rate',
            'trainer_lasix_win_rate',
            'trainer_claimed_win_rate',
            'jockey_win_rate',
            'jockey_trainer_combo_win_rate',
            'jockey_change_flag',
            'trainer_change_flag',
            'trainer_sample_size',
        ],
        'description': (
            'Trainer and jockey patterns. '
            'Computed from PP history as proxy '
            'until full stats table is built.'
        )
    },
    'class': {
        'features': [
            'class_direction',
            'purse_change_pct',
            'claiming_price_change_pct',
            'career_class_ceiling',
            'current_vs_ceiling_pct',
            'class_consistency',
        ],
        'description': (
            'Class movement. Class drop is one '
            'of the strongest signals in handicapping.'
        )
    },
    'equipment': {
        'features': [
            'lasix_first_time',
            'blinkers_first_time',
            'blinkers_on',
            'blinkers_off',
            'equipment_change',
            'medication_change',
            'mud_caulks',
            'trainer_intent_score',
        ],
        'description': (
            'Equipment and medication. First-time '
            'Lasix and blinkers are among the '
            'highest-signal features in the sport.'
        )
    },
    'physical': {
        'features': [
            'days_since_last_race',
            'layoff_bucket',
            'career_starts',
            'is_first_start',
            'first_time_on_surface',
            'was_claimed_last_out',
            'weight_carried',
            'apprentice_allowance',
            'win_rate_this_track',
            'overall_win_rate',
        ],
        'description': (
            'Physical and situational factors. '
            'Layoff patterns vary significantly '
            'by trainer.'
        )
    }
}

# Flat ordered list — training and inference
# MUST use this exact order
ALL_FEATURES = []
for group in FEATURE_GROUPS.values():
    ALL_FEATURES.extend(group['features'])

FEATURE_COUNT = len(ALL_FEATURES)  # should be 72

# Target variable name
TARGET_COLUMN = 'finish_position'

# Group ID for XGBoost ranker
# (identifies which race each row belongs to)
GROUP_COLUMN = 'race_id'

# Index columns — not features, not target
INDEX_COLUMNS = ['horse_id', 'entry_id',
                 'horse_name', 'race_id']

# Assertion: catches any duplicate features
assert len(ALL_FEATURES) == len(set(ALL_FEATURES)), \
    f"Duplicate features detected in ALL_FEATURES"
