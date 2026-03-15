import logging
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from models.canonical import (
    Track, Horse, Trainer, Jockey, Workout,
    PastPerformance, Entry, Race, RaceCard,
    Result, ModelVersion, Prediction
)
from shared.constants import (
    RAW_SPEED_PAR_TIMES,
    RUNNING_STYLE_THRESHOLDS,
    MIN_STARTS_FOR_STYLE
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════
# Helper functions
# ═══════════════════════════════════════════

def _to_float(val) -> Optional[float]:
    """Safely coerce Decimal or numeric to float."""
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _to_int(val) -> Optional[int]:
    """Safely coerce value to int."""
    if val is None:
        return None
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def _to_bool(val) -> bool:
    """Safely coerce value to bool. Defaults False."""
    if val is None:
        return False
    return bool(val)


def _to_str(val) -> Optional[str]:
    """Safely coerce value to stripped string."""
    if val is None:
        return None
    return str(val).strip()


def _compute_raw_speed_index(
    final_time: Optional[float],
    distance_furlongs: Optional[float]
) -> Optional[float]:
    """
    Compute raw speed index: final_time / distance_furlongs
    Lower = faster.
    Example: 1:08 for 6f = 68.0 / 6.0 = 11.333
    Example: 1:11 for 6f = 71.0 / 6.0 = 11.833
    Returns None if either input is missing or zero.
    """
    if not final_time or not distance_furlongs:
        return None
    if distance_furlongs == 0:
        return None
    return round(final_time / distance_furlongs, 4)


def _compute_raw_speed_vs_par(
    raw_speed_index: Optional[float],
    distance_furlongs: Optional[float]
) -> Optional[float]:
    """
    Compare raw speed index to par time for distance.
    Negative = faster than par (good).
    Positive = slower than par (bad).
    Returns None if data missing or distance not in pars.
    """
    if raw_speed_index is None or distance_furlongs is None:
        return None
    par = RAW_SPEED_PAR_TIMES.get(distance_furlongs)
    if par is None:
        # Find nearest distance in par times
        distances = list(RAW_SPEED_PAR_TIMES.keys())
        nearest = min(distances,
            key=lambda x: abs(x - distance_furlongs))
        par = RAW_SPEED_PAR_TIMES[nearest]
    return round(raw_speed_index - par, 4)


def _compute_pace_delta(
    early_pace_figure: Optional[float],
    late_pace_figure: Optional[float]
) -> Optional[float]:
    """
    Pace delta = late_pace - early_pace.
    Negative = horse accelerated (ran faster late).
    Positive = horse decelerated (backed up).
    A negative pace_delta in a fast-pace race
    is a strong performance indicator.
    """
    if early_pace_figure is None or late_pace_figure is None:
        return None
    return round(late_pace_figure - early_pace_figure, 4)


def _compute_running_style(
    call_1_position: Optional[int],
    call_2_position: Optional[int]
) -> Optional[str]:
    """
    Classify running style from call positions.
    Uses first available call position.
    Returns: front_runner, presser, midpack, closer
    """
    position = call_1_position or call_2_position
    if position is None:
        return None
    if position <= RUNNING_STYLE_THRESHOLDS['front_runner']:
        return 'front_runner'
    if position <= RUNNING_STYLE_THRESHOLDS['presser']:
        return 'presser'
    if position <= RUNNING_STYLE_THRESHOLDS['midpack']:
        return 'midpack'
    return 'closer'


def _compute_workout_speed_index(
    workout_time: Optional[float],
    distance_furlongs: Optional[float]
) -> Optional[float]:
    """
    Same raw speed index logic applied to workouts.
    workout_time / distance_furlongs.
    Lower = faster work.
    """
    if not workout_time or not distance_furlongs:
        return None
    if distance_furlongs == 0:
        return None
    return round(workout_time / distance_furlongs, 4)


# ═══════════════════════════════════════════
# Transform functions
# ═══════════════════════════════════════════

def transform_track(row: dict) -> Track:
    """Transform raw DB row to Track dataclass."""
    return Track(
        track_id=_to_str(row.get('track_id')),
        track_code=_to_str(row.get('track_code')),
        track_name=_to_str(row.get('track_name')),
        location=_to_str(row.get('location')),
        timezone=_to_str(row.get('timezone')),
        surfaces=row.get('surfaces') or [],
        is_qualifying=_to_bool(row.get('is_qualifying')),
        min_claiming_price=_to_int(
            row.get('min_claiming_price')),
        created_at=row.get('created_at')
    )


def transform_horse(row: dict) -> Horse:
    """Transform raw DB row to Horse dataclass."""
    return Horse(
        horse_id=_to_str(row.get('horse_id')),
        registration_id=_to_str(row.get('registration_id')),
        horse_name=_to_str(row.get('horse_name')) or '',
        sire=_to_str(row.get('sire')),
        dam=_to_str(row.get('dam')),
        dam_sire=_to_str(row.get('dam_sire')),
        sire_id=_to_str(row.get('sire_id')),
        dam_id=_to_str(row.get('dam_id')),
        dam_sire_id=_to_str(row.get('dam_sire_id')),
        foaling_date=row.get('foaling_date'),
        country_of_origin=_to_str(
            row.get('country_of_origin')) or 'USA',
        sex=_to_str(row.get('sex')),
        color=_to_str(row.get('color')),
        created_at=row.get('created_at'),
        updated_at=row.get('updated_at')
    )


def transform_trainer(row: dict) -> Trainer:
    """Transform raw DB row to Trainer dataclass."""
    return Trainer(
        trainer_id=_to_str(row.get('trainer_id')),
        trainer_name=_to_str(row.get('trainer_name')) or '',
        license_number=_to_str(row.get('license_number')),
        country=_to_str(row.get('country')) or 'USA',
        created_at=row.get('created_at')
    )


def transform_jockey(row: dict) -> Jockey:
    """Transform raw DB row to Jockey dataclass."""
    return Jockey(
        jockey_id=_to_str(row.get('jockey_id')),
        jockey_name=_to_str(row.get('jockey_name')) or '',
        license_number=_to_str(row.get('license_number')),
        country=_to_str(row.get('country')) or 'USA',
        is_apprentice=_to_bool(row.get('is_apprentice')),
        created_at=row.get('created_at')
    )


def transform_workout(row: dict) -> Workout:
    """
    Transform raw DB row to Workout dataclass.
    Computes workout_speed_index in transform.
    """
    workout_time = _to_float(row.get('workout_time'))
    distance = _to_float(row.get('distance_furlongs'))

    return Workout(
        workout_id=_to_str(row.get('workout_id')),
        horse_id=_to_str(row.get('horse_id')) or '',
        workout_date=row.get('workout_date'),
        track_code=_to_str(row.get('track_code')) or '',
        distance_furlongs=distance or 0.0,
        workout_time=workout_time or 0.0,
        is_bullet=_to_bool(row.get('is_bullet')),
        track_condition=_to_str(row.get('track_condition')),
        workout_type=_to_str(row.get('workout_type')),
        rank_on_day=_to_int(row.get('rank_on_day')),
        total_works_on_day=_to_int(
            row.get('total_works_on_day')),
        exercise_rider=_to_str(row.get('exercise_rider')),
        workout_speed_index=_compute_workout_speed_index(
            workout_time, distance),
        created_at=row.get('created_at')
    )


def transform_past_performance(
    row: dict
) -> PastPerformance:
    """
    Transform raw DB row to PastPerformance dataclass.

    Computes in transform (mechanical derivations only):
    - raw_speed_index: final_time / distance_furlongs
    - raw_speed_vs_par: raw_speed_index vs par table
    - pace_delta: late_pace - early_pace
    - running_style: from call positions

    Everything else is direct field mapping.
    """
    final_time = _to_float(row.get('final_time'))
    distance = _to_float(row.get('distance_furlongs'))
    early_pace = _to_float(row.get('early_pace_figure'))
    late_pace = _to_float(row.get('late_pace_figure'))

    raw_speed_index = _compute_raw_speed_index(
        final_time, distance)
    raw_speed_vs_par = _compute_raw_speed_vs_par(
        raw_speed_index, distance)
    pace_delta = _compute_pace_delta(early_pace, late_pace)
    running_style = (
        _to_str(row.get('running_style')) or
        _compute_running_style(
            _to_int(row.get('call_1_position')),
            _to_int(row.get('call_2_position'))
        )
    )

    return PastPerformance(
        pp_id=_to_str(row.get('pp_id')),
        horse_id=_to_str(row.get('horse_id')) or '',
        race_id=_to_str(row.get('race_id')),
        race_date=row.get('race_date'),
        track_code=_to_str(row.get('track_code')) or '',
        race_number=_to_int(row.get('race_number')),
        race_start_number=_to_int(
            row.get('race_start_number')),
        distance_furlongs=distance,
        surface=_to_str(row.get('surface')),
        race_type=_to_str(row.get('race_type')),
        claiming_price_entered=_to_int(
            row.get('claiming_price_entered')),
        claiming_price_taken=_to_int(
            row.get('claiming_price_taken')),
        was_claimed=_to_bool(row.get('was_claimed')),
        purse=_to_int(row.get('purse')),
        field_size=_to_int(row.get('field_size')),
        track_condition=_to_str(row.get('track_condition')),
        moisture_level=_to_str(row.get('moisture_level')),
        track_variant=_to_int(row.get('track_variant')),
        going_stick_reading=_to_float(
            row.get('going_stick_reading')),
        temperature=_to_int(row.get('temperature')),
        weather_conditions=_to_str(
            row.get('weather_conditions')),
        wind_speed=_to_int(row.get('wind_speed')),
        wind_direction=_to_str(row.get('wind_direction')),
        off_turf=_to_bool(row.get('off_turf')),
        jockey_name=_to_str(row.get('jockey_name')),
        trainer_name=_to_str(row.get('trainer_name')),
        previous_trainer=_to_str(row.get('previous_trainer')),
        trainer_change=_to_bool(row.get('trainer_change')),
        jockey_change=_to_bool(row.get('jockey_change')),
        apprentice_allowance=_to_int(
            row.get('apprentice_allowance')) or 0,
        weight_carried=_to_int(row.get('weight_carried')),
        lasix=_to_bool(row.get('lasix')),
        lasix_first_time=_to_bool(row.get('lasix_first_time')),
        bute=_to_bool(row.get('bute')),
        blinkers_on=_to_bool(row.get('blinkers_on')),
        blinkers_off=_to_bool(row.get('blinkers_off')),
        blinkers_first_time=_to_bool(
            row.get('blinkers_first_time')),
        tongue_tie=_to_bool(row.get('tongue_tie')),
        bar_shoes=_to_bool(row.get('bar_shoes')),
        front_bandages=_to_bool(row.get('front_bandages')),
        mud_caulks=_to_bool(row.get('mud_caulks')),
        equipment_change_from_last=_to_bool(
            row.get('equipment_change_from_last')),
        medication_change_from_last=_to_bool(
            row.get('medication_change_from_last')),
        post_position=_to_int(row.get('post_position')),
        finish_position=_to_int(row.get('finish_position')),
        official_finish=_to_int(row.get('official_finish')),
        lengths_behind=_to_float(row.get('lengths_behind')),
        is_disqualified=_to_bool(row.get('is_disqualified')),
        photo_finish=_to_bool(row.get('photo_finish')),
        nose_bob=_to_bool(row.get('nose_bob')),
        disqualification_involved=_to_bool(
            row.get('disqualification_involved')),
        stewards_inquiry=_to_bool(
            row.get('stewards_inquiry')),
        beyer_speed_figure=_to_int(
            row.get('beyer_speed_figure')),
        timeform_rating=_to_int(row.get('timeform_rating')),
        equibase_speed_figure=_to_int(
            row.get('equibase_speed_figure')),
        winner_beyer=_to_int(row.get('winner_beyer')),
        field_average_beyer=_to_float(
            row.get('field_average_beyer')),
        fraction_1=_to_float(row.get('fraction_1')),
        fraction_2=_to_float(row.get('fraction_2')),
        fraction_3=_to_float(row.get('fraction_3')),
        final_time=final_time,
        horse_fraction_1=_to_float(
            row.get('horse_fraction_1')),
        horse_fraction_2=_to_float(
            row.get('horse_fraction_2')),
        horse_fraction_3=_to_float(
            row.get('horse_fraction_3')),
        call_1_position=_to_int(row.get('call_1_position')),
        call_1_lengths=_to_float(row.get('call_1_lengths')),
        call_2_position=_to_int(row.get('call_2_position')),
        call_2_lengths=_to_float(row.get('call_2_lengths')),
        call_3_position=_to_int(row.get('call_3_position')),
        call_3_lengths=_to_float(row.get('call_3_lengths')),
        stretch_position=_to_int(row.get('stretch_position')),
        stretch_lengths=_to_float(row.get('stretch_lengths')),
        finish_call_position=_to_int(
            row.get('finish_call_position')),
        early_pace_figure=early_pace,
        late_pace_figure=late_pace,
        pace_delta=pace_delta,
        pace_scenario=_to_str(row.get('pace_scenario')),
        running_style=running_style,
        early_pace_pressure=_to_int(
            row.get('early_pace_pressure')),
        raw_speed_index=raw_speed_index,
        raw_speed_vs_par=raw_speed_vs_par,
        winner_name=_to_str(row.get('winner_name')),
        second_name=_to_str(row.get('second_name')),
        third_name=_to_str(row.get('third_name')),
        winner_time=_to_float(row.get('winner_time')),
        closing_odds=_to_float(row.get('closing_odds')),
        morning_line_that_day=_to_float(
            row.get('morning_line_that_day')),
        was_favorite=_to_bool(row.get('was_favorite')),
        odds_rank_in_field=_to_int(
            row.get('odds_rank_in_field')),
        class_rating=_to_int(row.get('class_rating')),
        days_since_last_race=_to_int(
            row.get('days_since_last_race')),
        comment=_to_str(row.get('comment')),
        trouble_comment=_to_str(row.get('trouble_comment')),
        created_at=row.get('created_at')
    )


def transform_entry(
    row: dict,
    horse: Horse,
    trainer: Trainer,
    jockey: Optional[Jockey],
    past_performances: list
) -> Entry:
    """
    Transform raw DB row to Entry dataclass.
    Receives pre-built nested objects from repository.
    Never fetches its own data.
    """
    return Entry(
        entry_id=_to_str(row.get('entry_id')),
        race_id=_to_str(row.get('race_id')) or '',
        horse=horse,
        trainer=trainer,
        jockey=jockey,
        post_position=_to_int(
            row.get('post_position')) or 0,
        program_number=_to_str(row.get('program_number')),
        morning_line_odds=_to_float(
            row.get('morning_line_odds')),
        weight_carried=_to_int(row.get('weight_carried')),
        allowance_weight=_to_int(
            row.get('allowance_weight')) or 0,
        apprentice_allowance=_to_int(
            row.get('apprentice_allowance')) or 0,
        lasix=_to_bool(row.get('lasix')),
        lasix_first_time=_to_bool(row.get('lasix_first_time')),
        bute=_to_bool(row.get('bute')),
        blinkers_on=_to_bool(row.get('blinkers_on')),
        blinkers_off=_to_bool(row.get('blinkers_off')),
        blinkers_first_time=_to_bool(
            row.get('blinkers_first_time')),
        tongue_tie=_to_bool(row.get('tongue_tie')),
        bar_shoes=_to_bool(row.get('bar_shoes')),
        front_bandages=_to_bool(row.get('front_bandages')),
        mud_caulks=_to_bool(row.get('mud_caulks')),
        equipment_change_from_last=_to_bool(
            row.get('equipment_change_from_last')),
        medication_change_from_last=_to_bool(
            row.get('medication_change_from_last')),
        is_scratched=_to_bool(row.get('is_scratched')),
        scratch_reason=_to_str(row.get('scratch_reason')),
        is_entry=_to_bool(row.get('is_entry')),
        past_performances=past_performances,
        created_at=row.get('created_at'),
        updated_at=row.get('updated_at')
    )


def transform_race(
    row: dict,
    track: Track,
    entries: list
) -> Race:
    """
    Transform raw DB row to Race dataclass.
    Receives pre-built nested objects from repository.
    """
    return Race(
        race_id=_to_str(row.get('race_id')),
        track=track,
        race_date=row.get('race_date'),
        race_number=_to_int(row.get('race_number')) or 0,
        post_time=row.get('post_time'),
        distance_furlongs=_to_float(
            row.get('distance_furlongs')) or 0.0,
        surface=_to_str(row.get('surface')) or '',
        race_type=_to_str(row.get('race_type')) or '',
        grade=_to_int(row.get('grade')),
        race_name=_to_str(row.get('race_name')),
        purse=_to_int(row.get('purse')),
        claiming_price=_to_int(row.get('claiming_price')),
        conditions=_to_str(row.get('conditions')),
        field_size=_to_int(row.get('field_size')),
        rail_position=_to_float(row.get('rail_position')),
        track_condition=_to_str(row.get('track_condition')),
        moisture_level=_to_str(row.get('moisture_level')),
        track_variant=_to_int(row.get('track_variant')),
        going_stick_reading=_to_float(
            row.get('going_stick_reading')),
        temperature=_to_int(row.get('temperature')),
        weather_conditions=_to_str(
            row.get('weather_conditions')),
        wind_speed=_to_int(row.get('wind_speed')),
        wind_direction=_to_str(row.get('wind_direction')),
        off_turf=_to_bool(row.get('off_turf')),
        equibase_race_id=_to_str(row.get('equibase_race_id')),
        entries=entries,
        created_at=row.get('created_at')
    )


def transform_result(
    row: dict,
    entry: Entry
) -> Result:
    """
    Transform raw DB row to Result dataclass.
    Receives pre-built Entry from repository.
    """
    return Result(
        result_id=_to_str(row.get('result_id')),
        entry=entry,
        race_id=_to_str(row.get('race_id')) or '',
        horse_id=_to_str(row.get('horse_id')) or '',
        finish_position=_to_int(
            row.get('finish_position')) or 0,
        official_finish=_to_int(
            row.get('official_finish')) or 0,
        is_disqualified=_to_bool(row.get('is_disqualified')),
        dq_from=_to_int(row.get('dq_from')),
        dq_to=_to_int(row.get('dq_to')),
        lengths_behind=_to_float(row.get('lengths_behind')),
        final_time=_to_float(row.get('final_time')),
        beyer_speed_figure=_to_int(
            row.get('beyer_speed_figure')),
        call_1_position=_to_int(row.get('call_1_position')),
        call_1_lengths=_to_float(row.get('call_1_lengths')),
        call_2_position=_to_int(row.get('call_2_position')),
        call_2_lengths=_to_float(row.get('call_2_lengths')),
        stretch_position=_to_int(row.get('stretch_position')),
        stretch_lengths=_to_float(row.get('stretch_lengths')),
        win_payout=_to_float(row.get('win_payout')),
        place_payout=_to_float(row.get('place_payout')),
        show_payout=_to_float(row.get('show_payout')),
        exacta_payout=_to_float(row.get('exacta_payout')),
        trifecta_payout=_to_float(row.get('trifecta_payout')),
        superfecta_payout=_to_float(
            row.get('superfecta_payout')),
        daily_double_payout=_to_float(
            row.get('daily_double_payout')),
        created_at=row.get('created_at')
    )


def transform_prediction(
    row: dict,
    entry: Entry
) -> Prediction:
    """
    Transform raw DB row to Prediction dataclass.
    Receives pre-built Entry from repository.
    """
    return Prediction(
        prediction_id=_to_str(row.get('prediction_id')),
        entry=entry,
        race_id=_to_str(row.get('race_id')) or '',
        horse_id=_to_str(row.get('horse_id')) or '',
        model_version_id=_to_str(
            row.get('model_version_id')),
        win_probability=_to_float(
            row.get('win_probability')),
        place_probability=_to_float(
            row.get('place_probability')),
        show_probability=_to_float(
            row.get('show_probability')),
        predicted_rank=_to_int(row.get('predicted_rank')),
        confidence_score=_to_float(
            row.get('confidence_score')),
        is_top_pick=_to_bool(row.get('is_top_pick')),
        is_value_flag=_to_bool(row.get('is_value_flag')),
        morning_line_implied_prob=_to_float(
            row.get('morning_line_implied_prob')),
        overlay_pct=_to_float(row.get('overlay_pct')),
        feature_importance=row.get('feature_importance') or {},
        recommended_bet_type=_to_str(
            row.get('recommended_bet_type')),
        exotic_partners=row.get('exotic_partners') or [],
        actual_finish=_to_int(row.get('actual_finish')),
        was_win=row.get('was_win'),
        was_place=row.get('was_place'),
        was_show=row.get('was_show'),
        exacta_hit=row.get('exacta_hit'),
        trifecta_hit=row.get('trifecta_hit'),
        created_at=row.get('created_at')
    )


def transform_model_version(row: dict) -> ModelVersion:
    """Transform raw DB row to ModelVersion dataclass."""
    return ModelVersion(
        model_version_id=_to_str(
            row.get('model_version_id')),
        version_name=_to_str(row.get('version_name')) or '',
        training_date=row.get('training_date'),
        training_data_start=row.get('training_data_start'),
        training_data_end=row.get('training_data_end'),
        training_race_count=_to_int(
            row.get('training_race_count')),
        exacta_hit_rate=_to_float(
            row.get('exacta_hit_rate')),
        trifecta_hit_rate=_to_float(
            row.get('trifecta_hit_rate')),
        top1_accuracy=_to_float(row.get('top1_accuracy')),
        top3_accuracy=_to_float(row.get('top3_accuracy')),
        calibration_score=_to_float(
            row.get('calibration_score')),
        feature_list=row.get('feature_list') or {},
        hyperparameters=row.get('hyperparameters') or {},
        s3_artifact_path=_to_str(
            row.get('s3_artifact_path')),
        is_active=_to_bool(row.get('is_active')),
        notes=_to_str(row.get('notes')),
        created_at=row.get('created_at')
    )
