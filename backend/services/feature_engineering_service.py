import logging
import numpy as np
import pandas as pd
from datetime import date, timedelta
from typing import Optional
from models.canonical import (
    Race, Entry, PastPerformance, Workout
)
from repositories.past_performance_repository \
    import PastPerformanceRepository
from repositories.workout_repository import (
    WorkoutRepository
)
from shared.constants import (
    RAW_SPEED_PAR_TIMES,
    RUNNING_STYLE_THRESHOLDS,
    LAYOFF_BUCKETS,
    PACE_SCENARIO_THRESHOLDS,
    MIN_STARTS_FOR_SPEED_TREND,
    MIN_STARTS_FOR_STYLE,
    WORKOUT_LOOKBACK_DAYS
)

logger = logging.getLogger(__name__)


class FeatureEngineeringService:
    """
    Transforms canonical Race/Entry objects into
    a numerical feature matrix for XGBoost.

    One row per horse per race.
    Approximately 70 features per row.
    All features are numeric (float or int).
    All None values replaced with 0.0 or averages.
    No odds data ever loaded or used here.
    """

    def __init__(self, conn):
        self.conn = conn
        self.pp_repo = PastPerformanceRepository(conn)
        self.workout_repo = WorkoutRepository(conn)

    # ═══════════════════════════════════════════
    # PUBLIC: Build complete feature matrix
    # ═══════════════════════════════════════════

    def build_feature_matrix(
        self, race: Race
    ) -> pd.DataFrame:
        """
        Build complete feature matrix for all entries
        in a race. One row per horse.
        Returns pandas DataFrame with horse_id and
        entry_id as index columns plus ~70 feature cols.

        Called by inference service for predictions
        and by training pipeline for model training.
        """
        rows = []

        # Compute field-level context first
        # (needed for relative features)
        field_context = self._compute_field_context(race)

        for entry in race.entries:
            if entry.is_scratched:
                continue
            try:
                features = self._build_entry_features(
                    entry, race, field_context
                )
                features['horse_id'] = (
                    entry.horse.horse_id
                )
                features['entry_id'] = entry.entry_id
                features['horse_name'] = (
                    entry.horse.horse_name
                )
                rows.append(features)
            except Exception as e:
                logger.error(
                    f"Feature build failed for "
                    f"{entry.horse.horse_name}: {e}",
                    exc_info=True
                )
                continue

        if not rows:
            return pd.DataFrame()

        df = pd.DataFrame(rows)

        # Fill any remaining NaN with 0
        numeric_cols = df.select_dtypes(
            include=[np.number]
        ).columns
        df[numeric_cols] = df[numeric_cols].fillna(0.0)

        return df

    # ═══════════════════════════════════════════
    # PRIVATE: Assemble all features for one entry
    # ═══════════════════════════════════════════

    def _build_entry_features(
        self,
        entry: Entry,
        race: Race,
        field_context: dict
    ) -> dict:
        """
        Combine all feature groups for one horse.
        Merges all compute_* dicts into one flat dict.
        """
        features = {}

        # Load additional PP data from DB
        # (entry.past_performances has last 10,
        #  but some features need surface/distance
        #  specific lookups)
        all_pps = entry.past_performances

        # Load workouts
        workouts = self.workout_repo \
            .get_workouts_before_race(
                entry.horse.horse_id,
                race.race_date
            )

        # Merge all feature groups
        features.update(
            self.compute_speed_features(
                entry, race, field_context
            )
        )
        features.update(
            self.compute_pace_features(
                entry, race, field_context
            )
        )
        features.update(
            self.compute_workout_features(
                entry.horse.horse_id,
                race.race_date,
                workouts
            )
        )
        features.update(
            self.compute_trainer_features(
                entry, all_pps
            )
        )
        features.update(
            self.compute_class_features(
                entry, race
            )
        )
        features.update(
            self.compute_equipment_features(entry)
        )
        features.update(
            self.compute_physical_features(
                entry, race
            )
        )

        return features

    # ═══════════════════════════════════════════
    # PUBLIC: Speed features (~18 features)
    # ═══════════════════════════════════════════

    def compute_speed_features(
        self,
        entry: Entry,
        race: Race,
        field_context: dict
    ) -> dict:
        """
        All speed-related features for one horse.
        Uses raw times AND Beyer figures.
        Raw times are Tony's core insight —
        physics doesn't lie the way variants can.
        """
        pps = entry.past_performances
        valid_pps = [
            p for p in pps
            if p.beyer_speed_figure is not None
        ]
        raw_pps = [
            p for p in pps
            if p.raw_speed_index is not None
        ]

        # ── Beyer figure features ──
        # Most recent Beyer speed figure
        beyer_last = (
            valid_pps[0].beyer_speed_figure
            if valid_pps else 0.0
        )
        # Average of last 3 Beyer figures
        beyer_last_3 = [
            p.beyer_speed_figure
            for p in valid_pps[:3]
        ]
        beyer_avg_3 = (
            float(np.mean(beyer_last_3))
            if beyer_last_3 else 0.0
        )
        # Trend: positive = improving
        beyer_trend = (
            float(beyer_last - beyer_avg_3)
            if beyer_last_3 else 0.0
        )
        # Highest Beyer ever recorded
        beyer_best_career = (
            max(p.beyer_speed_figure for p in valid_pps)
            if valid_pps else 0.0
        )
        # Best Beyer in last 90 days
        cutoff_90 = race.race_date - timedelta(days=90)
        recent_pps = [
            p for p in valid_pps
            if p.race_date and p.race_date >= cutoff_90
        ]
        beyer_best_90d = (
            max(p.beyer_speed_figure for p in recent_pps)
            if recent_pps else 0.0
        )

        # ── Raw speed features ──
        # raw_speed_index = final_time / furlongs
        # Lower = faster
        # This is the core of Tony's approach:
        # pure physics, not adjusted figures
        raw_last = (
            raw_pps[0].raw_speed_index
            if raw_pps else 0.0
        )
        raw_last_3 = [
            p.raw_speed_index
            for p in raw_pps[:3]
        ]
        raw_avg_3 = (
            float(np.mean(raw_last_3))
            if raw_last_3 else 0.0
        )
        # Trend: negative = getting faster (good)
        raw_trend = (
            float(raw_last - raw_avg_3)
            if raw_last_3 else 0.0
        )
        # How this horse's raw speed compares to par for the distance
        raw_vs_par_last = (
            raw_pps[0].raw_speed_vs_par
            if raw_pps else 0.0
        ) or 0.0

        # ── Key discrepancy feature ──
        # When Beyer says one thing but raw time
        # says another, that's a variant distortion.
        # Positive = raw speed suggests horse is
        # FASTER than Beyer implies (underrated).
        # This is where overlooked horses live.
        beyer_pct = 0.0
        raw_pct = 0.0
        if valid_pps and field_context.get(
            'field_beyer_avg', 0
        ) > 0:
            beyer_pct = (
                beyer_last /
                field_context['field_beyer_avg']
            )
        if raw_pps and field_context.get(
            'field_raw_avg', 0
        ) > 0:
            raw_pct = (
                field_context['field_raw_avg'] /
                raw_last  # inverted: lower raw = better
            )
        beyer_vs_raw_discrepancy = raw_pct - beyer_pct

        # ── Surface and distance specific ──
        # Best Beyer on today's surface
        surface_pps = [
            p for p in pps
            if p.surface == race.surface
            and p.beyer_speed_figure is not None
        ]
        speed_on_surface = (
            max(p.beyer_speed_figure
                for p in surface_pps)
            if surface_pps else beyer_avg_3
        )

        # Best Beyer at today's distance (+/- 0.5f)
        dist_pps = [
            p for p in pps
            if p.distance_furlongs is not None
            and abs(p.distance_furlongs -
                    race.distance_furlongs) <= 0.5
            and p.beyer_speed_figure is not None
        ]
        speed_at_distance = (
            max(p.beyer_speed_figure
                for p in dist_pps)
            if dist_pps else beyer_avg_3
        )

        # Best Beyer at today's track
        track_pps = [
            p for p in pps
            if p.track_code == race.track.track_code
            and p.beyer_speed_figure is not None
        ]
        speed_at_track = (
            max(p.beyer_speed_figure
                for p in track_pps)
            if track_pps else beyer_avg_3
        )

        # ── Condition-matched speed ──
        # Best Beyer in same track conditions (fast/sloppy/etc)
        condition = race.track_condition or 'fast'
        condition_pps = [
            p for p in pps
            if p.track_condition == condition
            and p.beyer_speed_figure is not None
        ]
        speed_in_conditions = (
            max(p.beyer_speed_figure
                for p in condition_pps)
            if condition_pps else beyer_avg_3
        )

        # ── Field-relative speed ──
        # How this horse's last Beyer compares to the field average
        beyer_vs_field = (
            beyer_last -
            field_context.get('field_beyer_avg', beyer_last)
        )
        # Quality of competition in last race (winner's Beyer)
        winner_beyer_last = (
            float(pps[0].winner_beyer)
            if pps and pps[0].winner_beyer else 0.0
        )

        return {
            # Beyer features
            'beyer_last': float(beyer_last),
            'beyer_avg_3': beyer_avg_3,
            'beyer_trend': beyer_trend,
            'beyer_best_career': float(beyer_best_career),
            'beyer_best_90d': float(beyer_best_90d),

            # Raw speed features
            'raw_speed_last': float(raw_last),
            'raw_speed_avg_3': float(raw_avg_3),
            'raw_speed_trend': float(raw_trend),
            'raw_speed_vs_par': float(raw_vs_par_last),

            # Discrepancy — the key overlay signal
            'beyer_vs_raw_discrepancy': float(
                beyer_vs_raw_discrepancy
            ),

            # Context-specific speed
            'speed_on_todays_surface': float(
                speed_on_surface
            ),
            'speed_at_todays_distance': float(
                speed_at_distance
            ),
            'speed_at_todays_track': float(speed_at_track),
            'speed_in_todays_conditions': float(
                speed_in_conditions
            ),

            # Field-relative
            'beyer_vs_field_avg': float(beyer_vs_field),
            'winner_beyer_last_race': winner_beyer_last,

            # Start count for speed features
            'speed_sample_size': float(len(valid_pps)),
            'raw_speed_sample_size': float(len(raw_pps)),
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Pace features (~12 features)
    # ═══════════════════════════════════════════

    def compute_pace_features(
        self,
        entry: Entry,
        race: Race,
        field_context: dict
    ) -> dict:
        """
        Pace and running style features.
        Captures whether a horse's running style
        is set up by today's pace scenario.
        A closer in a field of 4 front-runners
        has a structural advantage — the model
        needs to see this.
        """
        pps = entry.past_performances
        valid_pps = [p for p in pps if p.call_1_position]

        # ── Running style ──
        # Average first-call position across last 5 starts
        call1_positions = [
            p.call_1_position
            for p in valid_pps[:5]
            if p.call_1_position is not None
        ]
        avg_call1 = (
            float(np.mean(call1_positions))
            if call1_positions else 5.0
        )

        # Encode running style as numeric
        # front_runner=1, presser=2, midpack=3, closer=4
        style_map = {
            'front_runner': 1,
            'presser': 2,
            'midpack': 3,
            'closer': 4
        }
        running_style_str = self._classify_running_style(
            avg_call1
        )
        running_style_numeric = style_map.get(
            running_style_str, 3
        )

        # ── Pace delta features ──
        # Negative pace_delta = horse accelerated late
        # This is a strong quality signal
        pace_deltas = [
            p.pace_delta
            for p in pps[:5]
            if p.pace_delta is not None
        ]
        pace_delta_avg = (
            float(np.mean(pace_deltas))
            if pace_deltas else 0.0
        )
        # Most negative = best late acceleration
        best_pace_delta = (
            float(min(pace_deltas))
            if pace_deltas else 0.0
        )

        # ── Today's pace scenario ──
        # How many front-runners are in today's field
        front_runner_count = field_context.get(
            'front_runner_count', 0
        )
        pace_scenario_numeric = self \
            ._encode_pace_scenario(front_runner_count)

        # ── Style vs scenario match ──
        # Does this horse's running style benefit
        # from today's pace setup?
        # Closers benefit from fast/contested pace
        # Front-runners benefit from lone speed
        style_scenario_match = self \
            ._compute_style_scenario_match(
                running_style_str,
                front_runner_count
            )

        # ── Early pace pressure history ──
        # How much pressure this horse typically faces early
        pressure_values = [
            p.early_pace_pressure
            for p in pps[:5]
            if p.early_pace_pressure is not None
        ]
        avg_pressure = (
            float(np.mean(pressure_values))
            if pressure_values else 0.0
        )

        # ── Win rate by pace scenario ──
        # How this horse performs in fast-pace races
        fast_pace_pps = [
            p for p in pps
            if p.early_pace_pressure is not None
            and p.early_pace_pressure >= 3
            and p.finish_position is not None
        ]
        win_in_fast_pace = (
            float(sum(
                1 for p in fast_pace_pps
                if p.finish_position == 1
            )) / len(fast_pace_pps)
            if fast_pace_pps else 0.0
        )

        # How this horse performs in slow-pace races
        slow_pace_pps = [
            p for p in pps
            if p.early_pace_pressure is not None
            and p.early_pace_pressure <= 1
            and p.finish_position is not None
        ]
        win_in_slow_pace = (
            float(sum(
                1 for p in slow_pace_pps
                if p.finish_position == 1
            )) / len(slow_pace_pps)
            if slow_pace_pps else 0.0
        )

        # ── Stretch gain/loss ──
        # How many positions does this horse
        # typically gain or lose in the stretch?
        # Positive = gains positions (good closer)
        stretch_gains = []
        for p in pps[:5]:
            if (p.stretch_position is not None
                    and p.finish_position is not None):
                stretch_gains.append(
                    p.stretch_position - p.finish_position
                )
        avg_stretch_gain = (
            float(np.mean(stretch_gains))
            if stretch_gains else 0.0
        )

        return {
            'avg_call1_position': avg_call1,
            'running_style_numeric': float(
                running_style_numeric
            ),
            'pace_delta_avg': pace_delta_avg,
            'best_pace_delta': best_pace_delta,
            'front_runner_count_today': float(
                front_runner_count
            ),
            'pace_scenario_today': float(
                pace_scenario_numeric
            ),
            'style_scenario_match': float(
                style_scenario_match
            ),
            'avg_early_pace_pressure': avg_pressure,
            'win_rate_fast_pace': win_in_fast_pace,
            'win_rate_slow_pace': win_in_slow_pace,
            'avg_stretch_gain': avg_stretch_gain,
            'pace_sample_size': float(len(valid_pps)),
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Workout features (~8 features)
    # ═══════════════════════════════════════════

    def compute_workout_features(
        self,
        horse_id: str,
        race_date: date,
        workouts: list
    ) -> dict:
        """
        Workout features going into a race.
        Workouts are trainer intent signals —
        especially bullet works and gate works.
        A horse with 3 bullets in 30 days is
        being pointed at this spot.
        """
        if not workouts:
            return {
                'days_since_last_workout': 30.0,
                'workout_count_30d': 0.0,
                'bullet_work_14d': 0.0,
                'bullet_count_30d': 0.0,
                'best_workout_speed_index': 0.0,
                'workout_speed_trend': 0.0,
                'gate_work_30d': 0.0,
                'workout_frequency_score': 0.0,
            }

        # Days since most recent workout
        last_workout = workouts[0]
        days_since = (
            race_date - last_workout.workout_date
        ).days if last_workout.workout_date else 30

        # Count workouts in last 30 days
        cutoff_30 = race_date - timedelta(days=30)
        workouts_30d = [
            w for w in workouts
            if w.workout_date and
            w.workout_date >= cutoff_30
        ]
        workout_count_30d = float(len(workouts_30d))

        # Bullet work (fastest of morning) in last 14 days
        cutoff_14 = race_date - timedelta(days=14)
        bullet_14d = any(
            w.is_bullet and w.workout_date
            and w.workout_date >= cutoff_14
            for w in workouts
        )
        # Total bullet works in last 30 days
        bullet_count_30d = float(sum(
            1 for w in workouts_30d if w.is_bullet
        ))

        # Best (lowest) workout speed index in 30 days — lower = faster
        speed_indices = [
            w.workout_speed_index
            for w in workouts_30d
            if w.workout_speed_index is not None
        ]
        best_speed = (
            min(speed_indices)
            if speed_indices else 0.0
        )

        # Workout speed trend (negative = improving)
        workout_trend = 0.0
        if len(speed_indices) >= 2:
            workout_trend = float(
                speed_indices[0] - np.mean(speed_indices)
            )

        # Gate works (breaking drills) in last 30 days
        gate_work_30d = float(any(
            w.workout_type == 'gate'
            and w.workout_date
            and w.workout_date >= cutoff_30
            for w in workouts
        ))

        # Frequency score: is horse being worked
        # more or less than their historical average?
        # Positive = more active than usual (pointed at this spot)
        if len(workouts) > len(workouts_30d):
            older = workouts[len(workouts_30d):]
            if older:
                oldest_date = older[-1].workout_date
                if oldest_date:
                    span_days = (
                        race_date - oldest_date
                    ).days or 1
                    hist_avg = (
                        len(older) / (span_days / 30)
                    )
                    frequency_score = (
                        workout_count_30d - hist_avg
                    )
                else:
                    frequency_score = 0.0
            else:
                frequency_score = 0.0
        else:
            frequency_score = 0.0

        return {
            'days_since_last_workout': float(days_since),
            'workout_count_30d': workout_count_30d,
            'bullet_work_14d': float(bullet_14d),
            'bullet_count_30d': bullet_count_30d,
            'best_workout_speed_index': float(best_speed),
            'workout_speed_trend': float(workout_trend),
            'gate_work_30d': gate_work_30d,
            'workout_frequency_score': float(
                frequency_score
            ),
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Trainer/jockey features (~10)
    # ═══════════════════════════════════════════

    def compute_trainer_features(
        self,
        entry: Entry,
        all_pps: list
    ) -> dict:
        """
        Trainer and jockey pattern features.
        Computed from past_performances history —
        we aggregate win rates by condition
        across the horse's PP record.

        Note: In a full implementation these would
        be computed from the entire trainers/jockeys
        results table across ALL horses they've trained.
        Here we use the horse's own PP record as a
        proxy until we have a full trainer stats table.
        These features will improve significantly
        after the first full training dataset is loaded.
        """
        pps = all_pps
        trainer_name = entry.trainer.trainer_name
        jockey_name = (
            entry.jockey.jockey_name
            if entry.jockey else None
        )

        # ── Trainer win rate from PP record ──
        # Overall win rate with this trainer
        trainer_pps = [
            p for p in pps
            if p.trainer_name and
            p.trainer_name.lower() ==
            trainer_name.lower()
            and p.finish_position is not None
        ]
        trainer_win_rate = (
            float(sum(
                1 for p in trainer_pps
                if p.finish_position == 1
            )) / len(trainer_pps)
            if trainer_pps else 0.0
        )
        # In the money rate (top 3 finish)
        trainer_itm_rate = (
            float(sum(
                1 for p in trainer_pps
                if p.finish_position is not None
                and p.finish_position <= 3
            )) / len(trainer_pps)
            if trainer_pps else 0.0
        )

        # ── Trainer off layoff ──
        # Win rate when horse returns from 45+ day layoff
        layoff_pps = [
            p for p in trainer_pps
            if p.days_since_last_race is not None
            and p.days_since_last_race >= 45
        ]
        trainer_layoff_win_rate = (
            float(sum(
                1 for p in layoff_pps
                if p.finish_position == 1
            )) / len(layoff_pps)
            if layoff_pps else trainer_win_rate
        )

        # ── Trainer first time Lasix ──
        # Win rate when adding Lasix for the first time
        lasix_pps = [
            p for p in trainer_pps
            if p.lasix_first_time
            and p.finish_position is not None
        ]
        trainer_lasix_win_rate = (
            float(sum(
                1 for p in lasix_pps
                if p.finish_position == 1
            )) / len(lasix_pps)
            if lasix_pps else trainer_win_rate
        )

        # ── Trainer claimed horses ──
        # Win rate with horses claimed from other barns
        claimed_pps = [
            p for p in trainer_pps
            if p.was_claimed
            and p.finish_position is not None
        ]
        trainer_claimed_win_rate = (
            float(sum(
                1 for p in claimed_pps
                if p.finish_position == 1
            )) / len(claimed_pps)
            if claimed_pps else trainer_win_rate
        )

        # ── Jockey win rate ──
        # Win rate with today's jockey (from this horse's record)
        jockey_pps = [
            p for p in pps
            if jockey_name and p.jockey_name and
            p.jockey_name.lower() ==
            jockey_name.lower()
            and p.finish_position is not None
        ]
        jockey_win_rate = (
            float(sum(
                1 for p in jockey_pps
                if p.finish_position == 1
            )) / len(jockey_pps)
            if jockey_pps else 0.0
        )

        # ── Jockey-trainer combo ──
        # Win rate when this jockey rides for this trainer
        combo_pps = [
            p for p in trainer_pps
            if jockey_name and p.jockey_name and
            p.jockey_name.lower() ==
            jockey_name.lower()
            and p.finish_position is not None
        ]
        combo_win_rate = (
            float(sum(
                1 for p in combo_pps
                if p.finish_position == 1
            )) / len(combo_pps)
            if combo_pps else trainer_win_rate
        )

        # ── Change flags ──
        # Did jockey change from last race?
        jockey_change = float(entry.jockey_change
            if hasattr(entry, 'jockey_change')
            else (
                1.0 if pps and jockey_name
                and pps[0].jockey_name
                and pps[0].jockey_name.lower() !=
                jockey_name.lower()
                else 0.0
            )
        )

        # Did trainer change from last race?
        trainer_change = float(
            pps[0].trainer_change
            if pps and pps[0].trainer_change
            else 0.0
        )

        return {
            'trainer_win_rate': trainer_win_rate,
            'trainer_itm_rate': trainer_itm_rate,
            'trainer_layoff_win_rate': (
                trainer_layoff_win_rate
            ),
            'trainer_lasix_win_rate': (
                trainer_lasix_win_rate
            ),
            'trainer_claimed_win_rate': (
                trainer_claimed_win_rate
            ),
            'jockey_win_rate': jockey_win_rate,
            'jockey_trainer_combo_win_rate': (
                combo_win_rate
            ),
            'jockey_change_flag': jockey_change,
            'trainer_change_flag': trainer_change,
            'trainer_sample_size': float(
                len(trainer_pps)
            ),
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Class features (~6 features)
    # ═══════════════════════════════════════════

    def compute_class_features(
        self,
        entry: Entry,
        race: Race
    ) -> dict:
        """
        Class movement features.
        Class drop is one of the strongest signals
        in handicapping — a horse trying easier
        company than it has recently run.
        Class rise is the opposite.
        """
        pps = entry.past_performances
        today_purse = race.purse or 0
        today_claiming = race.claiming_price or 0

        if not pps:
            return {
                'class_direction': 0.0,
                'purse_change_pct': 0.0,
                'claiming_price_change_pct': 0.0,
                'career_class_ceiling': 0.0,
                'current_vs_ceiling_pct': 0.0,
                'class_consistency': 0.0,
            }

        last_pp = pps[0]
        last_purse = last_pp.purse or 0
        last_claiming = (
            last_pp.claiming_price_entered or 0
        )

        # ── Class direction ──
        # +1 = moving up in class (harder competition)
        # -1 = dropping down (often positive signal — easier spot)
        #  0 = same class
        if today_purse > 0 and last_purse > 0:
            if today_purse > last_purse * 1.15:
                class_direction = 1.0
            elif today_purse < last_purse * 0.85:
                class_direction = -1.0
            else:
                class_direction = 0.0
        elif today_claiming > 0 and last_claiming > 0:
            if today_claiming > last_claiming * 1.15:
                class_direction = 1.0
            elif today_claiming < last_claiming * 0.85:
                class_direction = -1.0
            else:
                class_direction = 0.0
        else:
            class_direction = 0.0

        # ── Purse change pct ──
        # Percentage change in purse vs last race
        purse_change_pct = (
            float((today_purse - last_purse) /
                  last_purse)
            if last_purse > 0 else 0.0
        )

        # ── Claiming price change ──
        # Percentage change in claiming price vs last race
        claiming_change_pct = (
            float((today_claiming - last_claiming) /
                  last_claiming)
            if last_claiming > 0 else 0.0
        )

        # ── Career class ceiling ──
        # Highest purse this horse has ever competed for
        purses = [
            p.purse for p in pps if p.purse
        ]
        career_ceiling = (
            float(max(purses)) if purses else 0.0
        )

        # ── Current vs ceiling ──
        # Today's purse as fraction of career best — lower = class drop
        current_vs_ceiling = (
            float(today_purse / career_ceiling)
            if career_ceiling > 0 else 1.0
        )

        # ── Class consistency ──
        # What % of last 5 races at similar class level (within 25%)
        similar_class = [
            p for p in pps[:5]
            if p.purse and today_purse > 0 and
            abs(p.purse - today_purse) /
            today_purse < 0.25
        ]
        class_consistency = (
            float(len(similar_class)) / 5.0
        )

        return {
            'class_direction': class_direction,
            'purse_change_pct': purse_change_pct,
            'claiming_price_change_pct': (
                claiming_change_pct
            ),
            'career_class_ceiling': career_ceiling,
            'current_vs_ceiling_pct': (
                current_vs_ceiling
            ),
            'class_consistency': class_consistency,
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Equipment features (~8 features)
    # ═══════════════════════════════════════════

    def compute_equipment_features(
        self, entry: Entry
    ) -> dict:
        """
        Equipment and medication features.
        First-time Lasix and first-time blinkers
        are among the highest-signal features
        in horse racing handicapping.
        They indicate trainer intent and often
        precede significant performance improvements.
        """

        # ── First-time signals (STRONGEST) ──
        # First time getting Lasix (anti-bleeding medication)
        lasix_first = float(entry.lasix_first_time)
        # First time wearing blinkers (focus aid)
        blinkers_first = float(
            entry.blinkers_first_time
        )

        # ── Change signals ──
        # Blinkers added since last race
        blinkers_on = float(entry.blinkers_on)
        # Blinkers removed since last race
        blinkers_off = float(entry.blinkers_off)
        # Any equipment change from last race
        equipment_change = float(
            entry.equipment_change_from_last
        )
        # Any medication change from last race
        medication_change = float(
            entry.medication_change_from_last
        )

        # ── Wet track intent ──
        # Mud caulks added = trainer expects wet track and prepared for it
        mud_caulks = float(entry.mud_caulks)

        # ── Composite trainer intent score ──
        # Weighted sum of all equipment/medication signals
        # Maximum intent = first Lasix + first blinkers
        # on the same day. Rare but very powerful.
        trainer_intent_score = (
            lasix_first * 2.0 +      # strongest signal
            blinkers_first * 1.5 +   # strong signal
            blinkers_on * 0.5 +      # moderate signal
            equipment_change * 0.3 + # mild signal
            medication_change * 0.3
        )

        return {
            'lasix_first_time': lasix_first,
            'blinkers_first_time': blinkers_first,
            'blinkers_on': blinkers_on,
            'blinkers_off': blinkers_off,
            'equipment_change': equipment_change,
            'medication_change': medication_change,
            'mud_caulks': mud_caulks,
            'trainer_intent_score': float(
                trainer_intent_score
            ),
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Physical features (~8 features)
    # ═══════════════════════════════════════════

    def compute_physical_features(
        self,
        entry: Entry,
        race: Race
    ) -> dict:
        """
        Physical and situational features.
        Layoff length is critical —
        too short and the horse may not be ready,
        too long and fitness is a question.
        The sweet spot varies by trainer pattern.
        """
        pps = entry.past_performances

        # ── Layoff ──
        # Days since last race — key fitness indicator
        days_since_last = 0
        if pps and pps[0].race_date:
            days_since_last = (
                race.race_date - pps[0].race_date
            ).days

        # Layoff bucket as ordered numeric (0=short through 4=long)
        layoff_bucket = self._encode_layoff(
            days_since_last
        )

        # ── Experience ──
        # Total career starts — more experienced horses are more predictable
        career_starts = len(pps)
        # First-time starter flag — debut horses are high variance
        is_first_start = float(career_starts == 0)

        # First start on today's surface — surface switch is a question mark
        surface_starts = sum(
            1 for p in pps
            if p.surface == race.surface
        )
        first_time_surface = float(
            surface_starts == 0
            and career_starts > 0
        )

        # ── Was claimed last out ──
        # New connections often improve a horse's performance
        was_claimed_last = float(
            pps[0].was_claimed if pps else False
        )

        # ── Weight ──
        # Weight carried in pounds (higher = disadvantage)
        weight = float(entry.weight_carried or 126)
        # Apprentice jockey weight allowance (pounds off)
        apprentice_allowance = float(
            entry.apprentice_allowance or 0
        )

        # ── Win rate at today's track ──
        # Some horses perform better at specific tracks
        track_pps = [
            p for p in pps
            if p.track_code == race.track.track_code
            and p.finish_position is not None
        ]
        win_rate_this_track = (
            float(sum(
                1 for p in track_pps
                if p.finish_position == 1
            )) / len(track_pps)
            if track_pps else 0.0
        )

        # ── Overall win rate ──
        # Career win percentage
        finished_pps = [
            p for p in pps
            if p.finish_position is not None
        ]
        overall_win_rate = (
            float(sum(
                1 for p in finished_pps
                if p.finish_position == 1
            )) / len(finished_pps)
            if finished_pps else 0.0
        )

        return {
            'days_since_last_race': float(
                days_since_last
            ),
            'layoff_bucket': float(layoff_bucket),
            'career_starts': float(career_starts),
            'is_first_start': is_first_start,
            'first_time_on_surface': first_time_surface,
            'was_claimed_last_out': was_claimed_last,
            'weight_carried': weight,
            'apprentice_allowance': apprentice_allowance,
            'win_rate_this_track': win_rate_this_track,
            'overall_win_rate': overall_win_rate,
        }

    # ═══════════════════════════════════════════
    # PRIVATE: Field context
    # ═══════════════════════════════════════════

    def _compute_field_context(
        self, race: Race
    ) -> dict:
        """
        Compute race-level context used by
        multiple feature groups.
        Runs once per race, not per horse.

        Returns:
        - field_beyer_avg: avg Beyer of field
        - field_raw_avg: avg raw speed index of field
        - front_runner_count: horses likely on lead
        - field_size: number of starters
        """
        beyers = []
        raws = []
        front_runners = 0

        for entry in race.entries:
            if entry.is_scratched:
                continue
            pps = entry.past_performances
            if pps:
                valid = [
                    p for p in pps
                    if p.beyer_speed_figure is not None
                ]
                if valid:
                    beyers.append(
                        valid[0].beyer_speed_figure
                    )
                raw_valid = [
                    p for p in pps
                    if p.raw_speed_index is not None
                ]
                if raw_valid:
                    raws.append(
                        raw_valid[0].raw_speed_index
                    )
                # Classify running style from avg first-call position
                call1s = [
                    p.call_1_position for p in pps[:5]
                    if p.call_1_position
                ]
                if call1s:
                    avg = np.mean(call1s)
                    if avg <= RUNNING_STYLE_THRESHOLDS[
                        'front_runner'
                    ]:
                        front_runners += 1

        return {
            'field_beyer_avg': (
                float(np.mean(beyers))
                if beyers else 85.0
            ),
            'field_raw_avg': (
                float(np.mean(raws))
                if raws else 11.7
            ),
            'front_runner_count': front_runners,
            'field_size': len([
                e for e in race.entries
                if not e.is_scratched
            ]),
        }

    # ═══════════════════════════════════════════
    # PRIVATE: Classification helpers
    # ═══════════════════════════════════════════

    def _classify_running_style(
        self, avg_call1: float
    ) -> str:
        """Classify running style from avg first-call position."""
        if avg_call1 <= RUNNING_STYLE_THRESHOLDS[
            'front_runner'
        ]:
            return 'front_runner'
        if avg_call1 <= RUNNING_STYLE_THRESHOLDS[
            'presser'
        ]:
            return 'presser'
        if avg_call1 <= RUNNING_STYLE_THRESHOLDS[
            'midpack'
        ]:
            return 'midpack'
        return 'closer'

    def _encode_pace_scenario(
        self, front_runner_count: int
    ) -> float:
        """
        Encode pace scenario as numeric.
        0 = no front runners (all closers)
        1 = lone speed
        2 = contested
        3 = fast duel (3+ speed)
        """
        if front_runner_count == 0:
            return 0.0
        if front_runner_count == 1:
            return 1.0
        if front_runner_count == 2:
            return 2.0
        return 3.0

    def _compute_style_scenario_match(
        self,
        running_style: str,
        front_runner_count: int
    ) -> float:
        """
        Score how well this horse's running style
        matches today's pace scenario.
        Returns float 0.0 to 1.0.
        1.0 = perfect setup for this horse
        0.0 = worst possible setup

        Logic:
        - Closers: benefit from contested/fast pace
          (front runners will tire)
        - Front runners: benefit from lone speed
          (no competition for lead)
        - Pressers/midpack: relatively neutral
        """
        if running_style == 'closer':
            # Closers love fast duel (score 1.0)
            # Hate lone speed (score 0.0)
            return min(
                1.0, front_runner_count / 3.0
            )
        if running_style == 'front_runner':
            # Front runners love lone speed (1.0)
            # Hate fast duel (0.0)
            if front_runner_count <= 1:
                return 1.0
            if front_runner_count == 2:
                return 0.5
            return 0.0
        # Presser/midpack: moderate match always
        return 0.5

    def _encode_layoff(
        self, days: int
    ) -> float:
        """
        Encode layoff length as ordered numeric.
        0 = short (0-14 days)
        1 = normal (15-45)
        2 = freshened (46-90)
        3 = extended (91-180)
        4 = long (181+)
        """
        for i, (bucket, (low, high)) in enumerate(
            LAYOFF_BUCKETS.items()
        ):
            if low <= days <= high:
                return float(i)
        return 4.0

    # ═══════════════════════════════════════════
    # PUBLIC: Feature names list
    # ═══════════════════════════════════════════

    def get_feature_names(self) -> list[str]:
        """
        Returns ordered list of all feature names.
        Used to ensure training and inference use
        identical feature ordering.
        XGBoost requires consistent column order.
        """
        return [
            # Speed (18)
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

            # Pace (12)
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

            # Workouts (8)
            'days_since_last_workout',
            'workout_count_30d',
            'bullet_work_14d',
            'bullet_count_30d',
            'best_workout_speed_index',
            'workout_speed_trend',
            'gate_work_30d',
            'workout_frequency_score',

            # Trainer/jockey (10)
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

            # Class (6)
            'class_direction',
            'purse_change_pct',
            'claiming_price_change_pct',
            'career_class_ceiling',
            'current_vs_ceiling_pct',
            'class_consistency',

            # Equipment (8)
            'lasix_first_time',
            'blinkers_first_time',
            'blinkers_on',
            'blinkers_off',
            'equipment_change',
            'medication_change',
            'mud_caulks',
            'trainer_intent_score',

            # Physical (10)
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
        ]
