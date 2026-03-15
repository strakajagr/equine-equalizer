from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class Track:
    track_code: str
    track_name: str
    track_id: Optional[str] = None
    location: Optional[str] = None
    timezone: Optional[str] = None
    surfaces: list = field(default_factory=list)
    is_qualifying: bool = False
    min_claiming_price: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class Horse:
    horse_name: str
    horse_id: Optional[str] = None
    registration_id: Optional[str] = None
    sire: Optional[str] = None
    dam: Optional[str] = None
    dam_sire: Optional[str] = None
    sire_id: Optional[str] = None
    dam_id: Optional[str] = None
    dam_sire_id: Optional[str] = None
    foaling_date: Optional[date] = None
    country_of_origin: str = 'USA'
    sex: Optional[str] = None
    color: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Trainer:
    trainer_name: str
    trainer_id: Optional[str] = None
    license_number: Optional[str] = None
    country: str = 'USA'
    created_at: Optional[datetime] = None


@dataclass
class Jockey:
    jockey_name: str
    jockey_id: Optional[str] = None
    license_number: Optional[str] = None
    country: str = 'USA'
    is_apprentice: bool = False
    created_at: Optional[datetime] = None


@dataclass
class Workout:
    horse_id: str
    workout_date: date
    track_code: str
    distance_furlongs: float
    workout_time: float
    workout_id: Optional[str] = None
    is_bullet: bool = False
    track_condition: Optional[str] = None
    workout_type: Optional[str] = None
    rank_on_day: Optional[int] = None
    total_works_on_day: Optional[int] = None
    exercise_rider: Optional[str] = None
    # Computed in transform: workout_time / distance_furlongs
    workout_speed_index: Optional[float] = None
    created_at: Optional[datetime] = None


@dataclass
class PastPerformance:
    horse_id: str
    race_date: date
    track_code: str
    pp_id: Optional[str] = None
    race_id: Optional[str] = None
    race_number: Optional[int] = None
    race_start_number: Optional[int] = None

    # Race conditions
    distance_furlongs: Optional[float] = None
    surface: Optional[str] = None
    race_type: Optional[str] = None
    claiming_price_entered: Optional[int] = None
    claiming_price_taken: Optional[int] = None
    was_claimed: bool = False
    purse: Optional[int] = None
    field_size: Optional[int] = None
    track_condition: Optional[str] = None
    moisture_level: Optional[str] = None
    track_variant: Optional[int] = None
    going_stick_reading: Optional[float] = None
    temperature: Optional[int] = None
    weather_conditions: Optional[str] = None
    wind_speed: Optional[int] = None
    wind_direction: Optional[str] = None
    off_turf: bool = False

    # Connections
    jockey_name: Optional[str] = None
    trainer_name: Optional[str] = None
    previous_trainer: Optional[str] = None
    trainer_change: bool = False
    jockey_change: bool = False
    apprentice_allowance: int = 0
    weight_carried: Optional[int] = None

    # Medication
    lasix: bool = False
    lasix_first_time: bool = False
    bute: bool = False

    # Equipment
    blinkers_on: bool = False
    blinkers_off: bool = False
    blinkers_first_time: bool = False
    tongue_tie: bool = False
    bar_shoes: bool = False
    front_bandages: bool = False
    mud_caulks: bool = False
    equipment_change_from_last: bool = False
    medication_change_from_last: bool = False

    # Post and finish
    post_position: Optional[int] = None
    finish_position: Optional[int] = None
    official_finish: Optional[int] = None
    lengths_behind: Optional[float] = None
    is_disqualified: bool = False
    photo_finish: bool = False
    nose_bob: bool = False
    disqualification_involved: bool = False
    stewards_inquiry: bool = False

    # Speed figures
    beyer_speed_figure: Optional[int] = None
    timeform_rating: Optional[int] = None
    equibase_speed_figure: Optional[int] = None
    winner_beyer: Optional[int] = None
    field_average_beyer: Optional[float] = None

    # Leader fractional times (seconds)
    fraction_1: Optional[float] = None
    fraction_2: Optional[float] = None
    fraction_3: Optional[float] = None
    final_time: Optional[float] = None

    # This horse's own fractional times
    horse_fraction_1: Optional[float] = None
    horse_fraction_2: Optional[float] = None
    horse_fraction_3: Optional[float] = None

    # Running positions
    call_1_position: Optional[int] = None
    call_1_lengths: Optional[float] = None
    call_2_position: Optional[int] = None
    call_2_lengths: Optional[float] = None
    call_3_position: Optional[int] = None
    call_3_lengths: Optional[float] = None
    stretch_position: Optional[int] = None
    stretch_lengths: Optional[float] = None
    finish_call_position: Optional[int] = None

    # Pace (computed in transform)
    early_pace_figure: Optional[float] = None
    late_pace_figure: Optional[float] = None
    pace_delta: Optional[float] = None
    pace_scenario: Optional[str] = None
    running_style: Optional[str] = None
    early_pace_pressure: Optional[int] = None

    # Derived speed (computed in transform)
    raw_speed_index: Optional[float] = None
    raw_speed_vs_par: Optional[float] = None

    # Race context
    winner_name: Optional[str] = None
    second_name: Optional[str] = None
    third_name: Optional[str] = None
    winner_time: Optional[float] = None
    closing_odds: Optional[float] = None
    morning_line_that_day: Optional[float] = None
    was_favorite: bool = False
    odds_rank_in_field: Optional[int] = None
    class_rating: Optional[int] = None
    days_since_last_race: Optional[int] = None

    # Comments
    comment: Optional[str] = None
    trouble_comment: Optional[str] = None

    created_at: Optional[datetime] = None


@dataclass
class Entry:
    race_id: str
    horse: Horse
    trainer: Trainer
    post_position: int
    entry_id: Optional[str] = None
    jockey: Optional[Jockey] = None
    program_number: Optional[str] = None
    morning_line_odds: Optional[float] = None
    weight_carried: Optional[int] = None
    allowance_weight: int = 0
    apprentice_allowance: int = 0

    # Medication
    lasix: bool = False
    lasix_first_time: bool = False
    bute: bool = False

    # Equipment
    blinkers_on: bool = False
    blinkers_off: bool = False
    blinkers_first_time: bool = False
    tongue_tie: bool = False
    bar_shoes: bool = False
    front_bandages: bool = False
    mud_caulks: bool = False
    equipment_change_from_last: bool = False
    medication_change_from_last: bool = False

    is_scratched: bool = False
    scratch_reason: Optional[str] = None
    is_entry: bool = False

    # Loaded by repository
    past_performances: list = field(default_factory=list)

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Race:
    track: Track
    race_date: date
    race_number: int
    distance_furlongs: float
    surface: str
    race_type: str
    race_id: Optional[str] = None
    post_time: Optional[datetime] = None
    grade: Optional[int] = None
    race_name: Optional[str] = None
    purse: Optional[int] = None
    claiming_price: Optional[int] = None
    conditions: Optional[str] = None
    field_size: Optional[int] = None
    rail_position: Optional[float] = None
    track_condition: Optional[str] = None
    moisture_level: Optional[str] = None
    track_variant: Optional[int] = None
    going_stick_reading: Optional[float] = None
    temperature: Optional[int] = None
    weather_conditions: Optional[str] = None
    wind_speed: Optional[int] = None
    wind_direction: Optional[str] = None
    off_turf: bool = False
    equibase_race_id: Optional[str] = None

    # Loaded by repository
    entries: list = field(default_factory=list)

    created_at: Optional[datetime] = None


@dataclass
class RaceCard:
    track: Track
    race_date: date
    races: list = field(default_factory=list)


@dataclass
class Result:
    entry: Entry
    race_id: str
    horse_id: str
    finish_position: int
    official_finish: int
    result_id: Optional[str] = None
    is_disqualified: bool = False
    dq_from: Optional[int] = None
    dq_to: Optional[int] = None
    lengths_behind: Optional[float] = None
    final_time: Optional[float] = None
    beyer_speed_figure: Optional[int] = None
    call_1_position: Optional[int] = None
    call_1_lengths: Optional[float] = None
    call_2_position: Optional[int] = None
    call_2_lengths: Optional[float] = None
    stretch_position: Optional[int] = None
    stretch_lengths: Optional[float] = None
    win_payout: Optional[float] = None
    place_payout: Optional[float] = None
    show_payout: Optional[float] = None
    exacta_payout: Optional[float] = None
    trifecta_payout: Optional[float] = None
    superfecta_payout: Optional[float] = None
    daily_double_payout: Optional[float] = None
    created_at: Optional[datetime] = None


@dataclass
class ModelVersion:
    version_name: str
    training_date: datetime
    training_data_start: date
    training_data_end: date
    model_version_id: Optional[str] = None
    training_race_count: Optional[int] = None
    exacta_hit_rate: Optional[float] = None
    trifecta_hit_rate: Optional[float] = None
    top1_accuracy: Optional[float] = None
    top3_accuracy: Optional[float] = None
    calibration_score: Optional[float] = None
    feature_list: dict = field(default_factory=dict)
    hyperparameters: dict = field(default_factory=dict)
    s3_artifact_path: Optional[str] = None
    is_active: bool = False
    notes: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class Prediction:
    entry: Entry
    race_id: str
    horse_id: str
    prediction_id: Optional[str] = None
    model_version_id: Optional[str] = None
    win_probability: Optional[float] = None
    place_probability: Optional[float] = None
    show_probability: Optional[float] = None
    predicted_rank: Optional[int] = None
    confidence_score: Optional[float] = None
    is_top_pick: bool = False
    is_value_flag: bool = False
    morning_line_implied_prob: Optional[float] = None
    overlay_pct: Optional[float] = None
    feature_importance: dict = field(default_factory=dict)
    recommended_bet_type: Optional[str] = None
    exotic_partners: list = field(default_factory=list)
    actual_finish: Optional[int] = None
    was_win: Optional[bool] = None
    was_place: Optional[bool] = None
    was_show: Optional[bool] = None
    exacta_hit: Optional[bool] = None
    trifecta_hit: Optional[bool] = None
    created_at: Optional[datetime] = None
