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
# Phase A3: Gonzo Sauce features computed via shared module — same source
# as training-time data_loader.py to eliminate train/inference drift.
from model.shared.gonzo_features import (
    compute_gonzo_speed_features,
    compute_gonzo_trajectory_features,
    compute_gonzo_class_features,
    GONZO_SPEED_DEFAULTS,
    GONZO_TRAJECTORY_DEFAULTS,
)

logger = logging.getLogger(__name__)

# ── Constants matching model/shared/data_loader.py ──
# Layoff buckets: (lo, hi, bucket_value)
LAYOFF_BUCKETS = [
    (0, 14, 1),
    (14, 28, 2),
    (28, 60, 3),
    (60, 120, 4),
    (120, 9999, 5),
]

# Trainer defaults matching data_loader.py
TRAINER_DEFAULTS = {
    'trainer_win_rate': 0.10,
    'trainer_itm_rate': 0.30,
    'trainer_layoff_win_rate': 0.08,
    'trainer_lasix_win_rate': 0.12,
    'trainer_sample_size': 0.0,
}


class FeatureEngineeringService:
    """
    Transforms canonical Race/Entry objects into
    a numerical feature matrix for XGBoost.

    CRITICAL: All feature computations MUST match
    model/shared/data_loader.py EXACTLY. data_loader.py
    is the source of truth (used during training).
    Any mismatch = garbage predictions.
    """

    def __init__(self, conn):
        self.conn = conn
        self.pp_repo = PastPerformanceRepository(conn)
        self.workout_repo = WorkoutRepository(conn)
        self._trainer_stats_cache: dict = {}

    # ═══════════════════════════════════════════
    # PUBLIC: Build complete feature matrix
    # ═══════════════════════════════════════════

    def build_feature_matrix(
        self, race: Race, include_odds: bool = False,
        par_dict: Optional[dict] = None,
    ) -> pd.DataFrame:
        """
        Build complete feature matrix for all entries
        in a race. One row per horse.

        include_odds=False → 63 features (WR model)
        include_odds=True  → 66 base features + 14 Gonzo features = 80 cols
            (Gonzo features always computed; trainer/inference selects
            the 67-feature subset via get_gonzo_sauce_features() at the
            model.predict() boundary.)

        par_dict: Phase A3 par-time medians for noteworthy-workout
            features. Pass from caller (WRInferenceService computes once
            per service instance via shared.par_times.compute_workout_pars).
            None → empty dict; A3/A4 features default to False/0.

        Returns DataFrame with horse_id, entry_id,
        horse_name as index columns plus feature cols.
        """
        if par_dict is None:
            par_dict = {}
        rows = []
        field_context = self._compute_field_context(race)

        for entry in race.entries:
            if entry.is_scratched:
                continue
            try:
                features = self._build_entry_features(
                    entry, race, field_context, include_odds,
                    par_dict=par_dict,
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
        numeric_cols = df.select_dtypes(
            include=[np.number]
        ).columns
        df[numeric_cols] = df[numeric_cols].fillna(0.0)
        return df

    def get_feature_names(
        self, include_odds: bool = False
    ) -> list:
        """Return ordered feature names matching feature_definitions.py."""
        try:
            from model.shared.feature_definitions import (
                get_odds_blind_features,
                get_odds_aware_features,
            )
            if include_odds:
                return get_odds_aware_features()
            return get_odds_blind_features()
        except ImportError:
            base = [
                'speed_fig_last', 'speed_fig_avg_3',
                'speed_fig_trend', 'speed_fig_best_career',
                'speed_fig_best_90d', 'speed_fig_at_track',
                'speed_fig_at_distance', 'speed_fig_on_surface',
                'speed_fig_vs_field', 'speed_fig_consistency',
                'speed_fig_sample_size',
                'early_pace_last', 'late_pace_last',
                'pace_delta_last', 'avg_call1_position',
                'avg_stretch_gain', 'pace_scenario_today',
                'troubled_trip_last', 'troubled_trip_freq',
                'pace_setter_freq', 'faded_freq',
                'late_rally_freq', 'avg_wide_path',
                'wide_3plus_freq', 'gate_issue_freq',
                'trainer_win_rate', 'trainer_itm_rate',
                'trainer_layoff_win_rate',
                'trainer_lasix_win_rate',
                'trainer_sample_size',
                'days_since_last_workout',
                'workout_count_30d', 'bullet_work_14d',
                'bullet_count_30d',
                'best_workout_speed_index',
                'workout_speed_trend', 'gate_work_30d',
                'workout_frequency_score',
                'class_direction', 'purse_change_pct',
                'claiming_price_change_pct',
                'career_class_ceiling',
                'current_vs_ceiling_pct',
                'class_consistency', 'race_quality_tier',
                'days_since_last_race', 'layoff_bucket',
                'career_starts', 'is_first_start',
                'first_time_on_surface',
                'was_claimed_last_out', 'weight_carried',
                'apprentice_allowance',
                'win_rate_this_track', 'overall_win_rate',
                'lasix', 'lasix_first_time',
                'blinkers_on', 'blinkers_off',
                'trainer_intent_score',
                'jockey_win_rate',
                'jockey_trainer_combo_win_rate',
                'jockey_change_flag',
            ]
            if include_odds:
                base += [
                    'closing_odds', 'log_closing_odds',
                    'odds_move'
                ]
            return base

    # ═══════════════════════════════════════════
    # PRIVATE: Assemble all features for one entry
    # ═══════════════════════════════════════════

    def _build_entry_features(
        self,
        entry: Entry,
        race: Race,
        field_context: dict,
        include_odds: bool = False,
        par_dict: Optional[dict] = None,
    ) -> dict:
        all_pps = entry.past_performances
        workouts = self.workout_repo \
            .get_workouts_before_race(
                entry.horse.horse_id,
                race.race_date
            )
        if par_dict is None:
            par_dict = {}

        features = {}
        features.update(
            self.compute_speed_features(
                entry, race, field_context
            )
        )
        features.update(
            self.compute_pace_features(entry, race)
        )
        features.update(
            self.compute_trip_features(all_pps)
        )
        features.update(
            self.compute_trainer_features(entry, all_pps, race.race_date)
        )
        features.update(
            self.compute_workout_features(
                entry.horse.horse_id,
                race.race_date,
                workouts
            )
        )
        features.update(
            self.compute_class_features(entry, race)
        )
        features.update(
            self.compute_physical_features(entry, race)
        )
        features.update(
            self.compute_equipment_features(entry, race)
        )
        features.update(
            self.compute_jockey_features(entry, all_pps)
        )
        if include_odds:
            features.update(
                self.compute_odds_features(entry, all_pps)
            )
        # ── Gonzo Sauce — Groups A/B/C (Phase A3, 14 features) ──
        # Always-run pattern matching data_loader.py training side. The
        # 14 columns ride along on every prediction; downstream model
        # selection picks the 67-feature subset only when style='gonzo_sauce'.
        # Source-of-truth: model/shared/gonzo_features.py — same module
        # used in training, eliminating train/inference drift.
        features.update(
            self.compute_gonzo_features(
                entry, race, all_pps, workouts, par_dict
            )
        )
        return features

    # ═══════════════════════════════════════════
    # PUBLIC: Gonzo Sauce features (14, Phase A3)
    # Source-of-truth: model/shared/gonzo_features.py
    # ═══════════════════════════════════════════

    def compute_gonzo_features(
        self,
        entry: Entry,
        race: Race,
        all_pps: list,
        workouts: list,
        par_dict: dict,
    ) -> dict:
        """
        Wrapper that converts canonical Entry/Race/PastPerformance/Workout
        objects into the DataFrame/Series shape the shared gonzo helpers
        expect, then dispatches to the 3 compute_gonzo_* functions.

        Returns a dict of all 14 Gonzo Sauce features. Defaults applied
        in helpers when input data is sparse.
        """
        # Convert PPs → DataFrame
        if all_pps:
            pp_records = []
            for pp in all_pps:
                pp_records.append({
                    'race_date': pd.Timestamp(pp.race_date),
                    'distance_furlongs': pp.distance_furlongs,
                    'final_time': pp.final_time,
                    'lengths_behind': pp.lengths_behind,
                    'finish_position': pp.finish_position,
                    'call_2_position': pp.call_2_position,
                    'call_2_lengths': pp.call_2_lengths,
                    'call_3_position': pp.call_3_position,
                    'call_3_lengths': pp.call_3_lengths,
                    'race_type': pp.race_type,
                    'purse': pp.purse,
                    'claiming_price_entered': pp.claiming_price_entered,
                    'grade': getattr(pp, 'grade', None),
                })
            horse_hist = pd.DataFrame(pp_records)
        else:
            horse_hist = pd.DataFrame()

        # Convert workouts → DataFrame keyed by horse_id (one-key dict)
        workouts_by_horse = {}
        if workouts:
            wo_records = []
            for w in workouts:
                wt = (w.workout_type or '').upper()
                wo_records.append({
                    'workout_date': pd.Timestamp(w.workout_date),
                    'distance_furlongs': w.distance_furlongs,
                    'track_code': w.track_code,
                    'workout_time': w.workout_time,
                    'is_bullet': bool(w.is_bullet),
                    'workout_type': w.workout_type,
                    'is_gate_work': (wt == 'G'),
                })
            workouts_by_horse[str(entry.horse.horse_id)] = pd.DataFrame(wo_records)

        # Build today's row Series
        today_row = pd.Series({
            'horse_id': str(entry.horse.horse_id),
            'race_date': pd.Timestamp(race.race_date),
            'distance_furlongs': race.distance_furlongs,
            'race_type': race.race_type,
            'purse': race.purse,
            'grade': race.grade,
            'claiming_price_entered': None,
            'field_size': len(race.entries),
        })

        out = {}
        out.update(compute_gonzo_speed_features(
            horse_hist, today_row, workouts_by_horse, par_dict
        ))
        out.update(compute_gonzo_trajectory_features(horse_hist, today_row))
        out.update(compute_gonzo_class_features(horse_hist, today_row))

        # Coerce bools to floats (XGBoost feeds floats; matches training-side
        # behavior where bool features ride along as 1.0/0.0).
        for k in ('noteworthy_workout_recent_14d', 'is_stretching_out'):
            if k in out:
                out[k] = float(bool(out[k]))
        # NaN-allowed: A1/A2 stay None when no eligible PPs (downstream
        # NaN-imputation handled by feature_df numeric_cols.fillna at
        # build_feature_matrix tail).
        return out

    # ═══════════════════════════════════════════
    # PUBLIC: Speed features (11)
    # Matches: data_loader._compute_speed_features
    # ═══════════════════════════════════════════

    def compute_speed_features(
        self,
        entry: Entry,
        race: Race,
        field_context: dict
    ) -> dict:
        pps = entry.past_performances
        valid_pps = [
            p for p in pps
            if p.computed_speed_figure is not None
        ]

        fig_last = (
            float(valid_pps[0].computed_speed_figure)
            if valid_pps else 0.0
        )
        figs_3 = [
            p.computed_speed_figure
            for p in valid_pps[:3]
        ]
        fig_avg_3 = (
            float(np.mean(figs_3)) if figs_3 else 0.0
        )
        fig_trend = (
            float(fig_last - fig_avg_3)
            if figs_3 else 0.0
        )
        fig_best_career = (
            float(max(
                p.computed_speed_figure
                for p in valid_pps
            ))
            if valid_pps else 0.0
        )
        cutoff_90 = race.race_date - timedelta(days=90)
        recent_pps = [
            p for p in valid_pps
            if p.race_date and p.race_date >= cutoff_90
        ]
        fig_best_90d = (
            float(max(
                p.computed_speed_figure
                for p in recent_pps
            ))
            if recent_pps else 0.0
        )

        # FIX #1-3: mean() not max(), default=0.0 not fig_avg_3
        track_figs = [
            p.computed_speed_figure for p in valid_pps
            if p.track_code == race.track.track_code
        ]
        fig_at_track = (
            float(np.mean(track_figs))
            if track_figs else 0.0
        )

        dist_figs = [
            p.computed_speed_figure for p in valid_pps
            if p.distance_furlongs is not None
            and abs(p.distance_furlongs -
                    race.distance_furlongs) < 0.5
        ]
        fig_at_distance = (
            float(np.mean(dist_figs))
            if dist_figs else 0.0
        )

        surface_figs = [
            p.computed_speed_figure for p in valid_pps
            if p.surface == race.surface
        ]
        fig_on_surface = (
            float(np.mean(surface_figs))
            if surface_figs else 0.0
        )

        field_avg = field_context.get(
            'field_speed_avg', fig_last
        )
        fig_vs_field = fig_last - field_avg

        # FIX #4: ddof=1 (sample std) to match pandas .std()
        figs_5 = [
            p.computed_speed_figure
            for p in valid_pps[:5]
        ]
        fig_consistency = (
            float(np.std(figs_5, ddof=1))
            if len(figs_5) >= 2 else 5.0
        )

        return {
            'speed_fig_last': fig_last,
            'speed_fig_avg_3': fig_avg_3,
            'speed_fig_trend': fig_trend,
            'speed_fig_best_career': fig_best_career,
            'speed_fig_best_90d': fig_best_90d,
            'speed_fig_at_track': fig_at_track,
            'speed_fig_at_distance': fig_at_distance,
            'speed_fig_on_surface': fig_on_surface,
            'speed_fig_vs_field': float(fig_vs_field),
            'speed_fig_consistency': fig_consistency,
            'speed_fig_sample_size': float(len(valid_pps)),
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Pace features (6)
    # Matches: data_loader._compute_pace_features
    # ═══════════════════════════════════════════

    def compute_pace_features(
        self,
        entry: Entry,
        race: Race,
    ) -> dict:
        pps = entry.past_performances

        early_pps = [
            p for p in pps
            if p.early_pace_figure is not None
        ]
        late_pps = [
            p for p in pps
            if p.late_pace_figure is not None
        ]
        delta_pps = [
            p for p in pps
            if p.pace_delta is not None
        ]

        early_last = (
            float(early_pps[0].early_pace_figure)
            if early_pps else 24.0
        )
        late_last = (
            float(late_pps[0].late_pace_figure)
            if late_pps else 38.0
        )
        delta_last = (
            float(delta_pps[0].pace_delta)
            if delta_pps else 14.0
        )

        call1_positions = [
            p.call_1_position
            for p in pps[:5]
            if p.call_1_position is not None
        ]
        avg_call1 = (
            float(np.mean(call1_positions))
            if call1_positions else 5.0
        )

        # FIX #5: use call_2_position, not stretch_position
        stretch_gains = []
        for p in pps[:5]:
            if (p.call_2_position is not None
                    and p.finish_position is not None):
                stretch_gains.append(
                    p.call_2_position -
                    p.finish_position
                )
        avg_stretch = (
            float(np.mean(stretch_gains))
            if stretch_gains else 0.0
        )

        # FIX #6: raw count of E/EP/P running styles,
        # not categorical encoding. Matches data_loader
        # which counts running_style in ['E','EP','P'].
        # At inference we approximate by checking
        # avg call_1_position <= 2.0 in last 5 PPs
        # (same as _is_front_runner), but return the
        # RAW COUNT, not a 0/1/2/3 category.
        front_runner_count = sum(
            1 for e in race.entries
            if not e.is_scratched
            and e.past_performances
            and self._is_front_runner(e.past_performances)
        )
        pace_scenario = float(front_runner_count)

        return {
            'early_pace_last': early_last,
            'late_pace_last': late_last,
            'pace_delta_last': delta_last,
            'avg_call1_position': avg_call1,
            'avg_stretch_gain': avg_stretch,
            'pace_scenario_today': pace_scenario,
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Trip features (8) — already matches
    # ═══════════════════════════════════════════

    def compute_trip_features(
        self, pps: list
    ) -> dict:
        recent = sorted(
            pps,
            key=lambda x: x.race_date
            if x.race_date else date.min,
            reverse=True
        )[:5]
        n = max(len(recent), 1)

        if not recent:
            return {
                'troubled_trip_last': 0.0,
                'troubled_trip_freq': 0.0,
                'pace_setter_freq': 0.0,
                'faded_freq': 0.0,
                'late_rally_freq': 0.0,
                'avg_wide_path': 0.0,
                'wide_3plus_freq': 0.0,
                'gate_issue_freq': 0.0,
            }

        last = recent[0]
        return {
            'troubled_trip_last': float(
                last.trip_troubled
            ),
            'troubled_trip_freq': float(
                sum(p.trip_troubled for p in recent) / n
            ),
            'pace_setter_freq': float(
                sum(
                    p.trip_pace_setter for p in recent
                ) / n
            ),
            'faded_freq': float(
                sum(p.trip_faded for p in recent) / n
            ),
            'late_rally_freq': float(
                sum(
                    p.trip_late_rally for p in recent
                ) / n
            ),
            'avg_wide_path': float(
                sum(p.wide_path for p in recent) / n
            ),
            'wide_3plus_freq': float(
                sum(
                    1 for p in recent
                    if p.wide_path >= 3
                ) / n
            ),
            'gate_issue_freq': float(
                sum(
                    p.trip_gate_issue for p in recent
                ) / n
            ),
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Workout features (8)
    # Matches: data_loader._compute_workout_features
    # ═══════════════════════════════════════════

    def compute_workout_features(
        self,
        horse_id: str,
        race_date: date,
        workouts: list
    ) -> dict:
        if not workouts:
            return {
                'days_since_last_workout': 30.0,
                'workout_count_30d': 0.0,
                'bullet_work_14d': 0.0,
                'bullet_count_30d': 0.0,
                'best_workout_speed_index': 0.5,  # FIX #11: default=0.5
                'workout_speed_trend': 0.0,
                'gate_work_30d': 0.0,
                'workout_frequency_score': 0.0,
            }

        last_workout = workouts[0]
        days_since = (
            race_date - last_workout.workout_date
        ).days if last_workout.workout_date else 30

        cutoff_30 = race_date - timedelta(days=30)
        workouts_30d = [
            w for w in workouts
            if w.workout_date and
            w.workout_date >= cutoff_30
        ]
        workout_count_30d = float(len(workouts_30d))

        cutoff_14 = race_date - timedelta(days=14)
        bullet_14d = any(
            w.is_bullet and w.workout_date
            and w.workout_date >= cutoff_14
            for w in workouts
        )
        bullet_count_30d = float(sum(
            1 for w in workouts_30d if w.is_bullet
        ))

        # FIX #11: rank_on_day / works_on_day (0-1 ratio),
        # not workout_time / distance. Matches data_loader.
        rank_ratios = []
        for w in workouts_30d:
            rank = getattr(w, 'rank_on_day', None)
            total = getattr(w, 'total_works_on_day', None) or getattr(w, 'works_on_day', None)
            if rank is not None and total is not None and total > 0:
                rank_ratios.append(float(rank) / float(total))
        best_speed = (
            min(rank_ratios) if rank_ratios else 0.5
        )

        # FIX #12: compare mean rank of last 2 vs prior 2.
        # (older - recent) / older. Matches data_loader.
        workout_trend = 0.0
        if len(workouts_30d) >= 4:
            ranks = []
            for w in workouts_30d:
                r = getattr(w, 'rank_on_day', None)
                if r is not None:
                    ranks.append(float(r))
            if len(ranks) >= 4:
                recent_mean = np.mean(ranks[:2])
                older_mean = np.mean(ranks[2:4])
                if older_mean > 0:
                    workout_trend = float(
                        (older_mean - recent_mean) / older_mean
                    )

        # FIX #13: check workout_type upper() == 'G'
        gate_work_30d = float(any(
            getattr(w, 'workout_type', '') is not None
            and str(getattr(w, 'workout_type', '')).upper() == 'G'
            and w.workout_date
            and w.workout_date >= cutoff_30
            for w in workouts
        ))

        # FIX #14: min(count_30 / 4.0, 1.0)
        frequency_score = min(workout_count_30d / 4.0, 1.0)

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
    # PUBLIC: Trainer features (5)
    # Matches: data_loader._compute_trainer_features
    # ═══════════════════════════════════════════

    def compute_trainer_features(
        self,
        entry: Entry,
        all_pps: list,
        race_date=None
    ) -> dict:
        trainer_name = entry.trainer.trainer_name
        stats = self._get_trainer_stats(trainer_name, race_date=race_date)

        if stats:
            # FIX #7-10: use data_loader defaults, not 0.0
            trainer_win_rate = self._safe_float(
                stats.get('win_rate'),
                TRAINER_DEFAULTS['trainer_win_rate']
            )
            trainer_itm_rate = self._safe_float(
                stats.get('itm_rate'),
                TRAINER_DEFAULTS['trainer_itm_rate']
            )
            trainer_layoff_win_rate = self._safe_float(
                stats.get('layoff_win_rate'),
                TRAINER_DEFAULTS['trainer_layoff_win_rate']
            )
            trainer_lasix_win_rate = self._safe_float(
                stats.get('lasix_win_rate'),
                TRAINER_DEFAULTS['trainer_lasix_win_rate']
            )
            trainer_sample_size = self._safe_float(
                stats.get('total_starts'), 0.0
            )
        else:
            # No trainer stats found — use population defaults
            return dict(TRAINER_DEFAULTS)

        return {
            'trainer_win_rate': trainer_win_rate,
            'trainer_itm_rate': trainer_itm_rate,
            'trainer_layoff_win_rate': (
                trainer_layoff_win_rate
            ),
            'trainer_lasix_win_rate': (
                trainer_lasix_win_rate
            ),
            'trainer_sample_size': trainer_sample_size,
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Class features (7)
    # Matches: data_loader._compute_class_features
    # ═══════════════════════════════════════════

    def compute_class_features(
        self,
        entry: Entry,
        race: Race
    ) -> dict:
        pps = entry.past_performances
        today_purse = float(race.purse or 0)
        today_claiming = float(race.claiming_price or 0)

        # FIX #15: race_quality_tier matching data_loader
        # stakes=5, allowance=4, msw=3, maiden=3, claiming=2, mcl=1
        quality_tier = self._encode_race_quality_tier(
            race.race_type
        )

        if not pps:
            return {
                'class_direction': 0.0,
                'purse_change_pct': 0.0,
                'claiming_price_change_pct': 0.0,
                # FIX #17: default to today_purse, not 0.0
                'career_class_ceiling': today_purse,
                'current_vs_ceiling_pct': 1.0,
                'class_consistency': 0.0,
                'race_quality_tier': quality_tier,
            }

        last_pp = pps[0]
        last_purse = float(last_pp.purse or 0)
        last_claiming = float(
            last_pp.claiming_price_entered or 0
        )

        # class_direction: matches data_loader
        purse_change = 0.0
        if last_purse > 0:
            purse_change = (today_purse - last_purse) / last_purse
        if purse_change > 0.15:
            class_direction = 1.0
        elif purse_change < -0.15:
            class_direction = -1.0
        else:
            class_direction = 0.0

        purse_change_pct = purse_change

        # FIX #16: require BOTH today AND last > 0
        claiming_change_pct = 0.0
        if today_claiming > 0 and last_claiming > 0:
            claiming_change_pct = float(
                (today_claiming - last_claiming)
                / last_claiming
            )

        purses = [float(p.purse) for p in pps if p.purse]
        # FIX #17: default to today_purse, not 0.0
        career_ceiling = (
            float(max(purses)) if purses else today_purse
        )
        current_vs_ceiling = (
            float(today_purse / career_ceiling)
            if career_ceiling > 0 else 1.0
        )

        # FIX #18: std of last 5 purses, not fraction-at-class
        last5_purses = [
            float(p.purse) for p in pps[:5] if p.purse
        ]
        class_consistency = (
            float(np.std(last5_purses, ddof=1))
            if len(last5_purses) >= 2 else 0.0
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
            'race_quality_tier': quality_tier,
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Physical features (10)
    # Matches: data_loader._compute_physical_features
    # ═══════════════════════════════════════════

    def compute_physical_features(
        self,
        entry: Entry,
        race: Race
    ) -> dict:
        pps = entry.past_performances

        # FIX #19: default=30.0, not 0
        days_since_last = 30.0
        if pps and pps[0].race_date:
            days_since_last = float(
                (race.race_date - pps[0].race_date).days
            )

        # FIX #20: layoff buckets matching data_loader
        layoff_bucket = self._layoff_bucket(
            days_since_last
        )

        # FIX #21: len(prior) + 1 (includes current race)
        career_starts = float(len(pps) + 1)
        is_first_start = float(len(pps) == 0)

        # FIX #22: first-time starters get 1.0
        surfaces_seen = set(
            p.surface for p in pps
            if p.surface is not None
        )
        first_time_surface = float(
            race.surface not in surfaces_seen
        )

        was_claimed_last = float(
            pps[0].was_claimed if pps else False
        )
        # FIX #23: default=118, not 126
        weight = float(entry.weight_carried or 118)
        apprentice_allowance = float(
            entry.apprentice_allowance or 0
        )
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
            'days_since_last_race': days_since_last,
            'layoff_bucket': float(layoff_bucket),
            'career_starts': career_starts,
            'is_first_start': is_first_start,
            'first_time_on_surface': first_time_surface,
            'was_claimed_last_out': was_claimed_last,
            'weight_carried': weight,
            'apprentice_allowance': apprentice_allowance,
            'win_rate_this_track': win_rate_this_track,
            'overall_win_rate': overall_win_rate,
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Equipment features (5)
    # Matches: data_loader._compute_equipment_features
    # ═══════════════════════════════════════════

    def compute_equipment_features(
        self, entry: Entry, race: Race = None
    ) -> dict:
        lasix = float(entry.lasix)
        lasix_first = float(entry.lasix_first_time)
        blinkers_on = float(entry.blinkers_on)
        blinkers_off = float(entry.blinkers_off)

        # FIX #24: match data_loader formula exactly:
        # lasix_first_time * 2 + blinkers_on + class_drop
        # class_drop = 1.0 if today_purse < last_purse
        pps = entry.past_performances
        class_drop = 0.0
        if race and pps:
            today_purse = float(race.purse or 0)
            last_purse = float(pps[0].purse or 0) if pps[0].purse else 0.0
            if today_purse > 0 and last_purse > 0 and today_purse < last_purse:
                class_drop = 1.0

        trainer_intent_score = (
            lasix_first * 2.0 +
            blinkers_on +
            class_drop
        )

        return {
            'lasix': lasix,
            'lasix_first_time': lasix_first,
            'blinkers_on': blinkers_on,
            'blinkers_off': blinkers_off,
            'trainer_intent_score': float(
                trainer_intent_score
            ),
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Jockey features (3)
    # Matches: data_loader._compute_jockey_features
    # ═══════════════════════════════════════════

    def compute_jockey_features(
        self,
        entry: Entry,
        all_pps: list
    ) -> dict:
        pps = all_pps
        jockey_name = (
            entry.jockey.jockey_name
            if entry.jockey else None
        )

        # FIX #28: use population default 0.10, not 0.0.
        # Ideally compute global jockey stats, but at
        # inference time we only have this horse's PPs.
        # Use horse-specific stats with training default.
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
            if jockey_pps else 0.10  # FIX: default=0.10
        )

        # FIX #29: default=0.10
        trainer_name = entry.trainer.trainer_name
        combo_pps = [
            p for p in pps
            if jockey_name and p.jockey_name
            and p.jockey_name.lower() == jockey_name.lower()
            and p.trainer_name
            and p.trainer_name.lower() == trainer_name.lower()
            and p.finish_position is not None
        ]
        combo_win_rate = (
            float(sum(
                1 for p in combo_pps
                if p.finish_position == 1
            )) / len(combo_pps)
            if combo_pps else 0.10  # FIX: default=0.10
        )

        jockey_change = float(
            1.0 if pps and jockey_name
            and pps[0].jockey_name
            and pps[0].jockey_name.lower() !=
            jockey_name.lower()
            else 0.0
        )

        return {
            'jockey_win_rate': jockey_win_rate,
            'jockey_trainer_combo_win_rate': (
                combo_win_rate
            ),
            'jockey_change_flag': jockey_change,
        }

    # ═══════════════════════════════════════════
    # PUBLIC: Odds features (3) — P&L and LS only
    # Matches: data_loader._compute_odds_features
    # ═══════════════════════════════════════════

    def compute_odds_features(
        self, entry: Entry, pps: list
    ) -> dict:
        """
        Odds features. Only called when include_odds=True.

        KNOWN DIFFERENCE from training:
        - Training uses same-race closing_odds (actual).
        - Inference uses last-PP closing_odds or morning_line
          (approximation — race hasn't happened yet).
        This is inherent to the prediction problem.
        """
        closing = None
        if pps and pps[0].closing_odds:
            closing = float(pps[0].closing_odds)

        ml = entry.morning_line_odds

        if closing is None or closing <= 0:
            closing = float(ml) if ml else 5.0

        # FIX #25: np.log1p, not np.log
        log_odds = float(np.log1p(closing))

        # odds_move: inherently different from training
        # (training: same-race closing - ML; inference:
        # last-race closing - today's ML)
        odds_move = float(
            closing - (ml or closing)
        ) if ml else 0.0

        return {
            'closing_odds': closing,
            'log_closing_odds': log_odds,
            'odds_move': odds_move,
        }

    # ═══════════════════════════════════════════
    # PRIVATE: Field context
    # ═══════════════════════════════════════════

    def _compute_field_context(
        self, race: Race
    ) -> dict:
        speed_figs = []
        for entry in race.entries:
            if entry.is_scratched:
                continue
            pps = entry.past_performances
            if pps:
                valid = [
                    p for p in pps
                    if p.computed_speed_figure is not None
                ]
                if valid:
                    speed_figs.append(
                        valid[0].computed_speed_figure
                    )
        return {
            'field_speed_avg': (
                float(np.mean(speed_figs))
                if speed_figs else 80.0
            ),
            'field_size': len([
                e for e in race.entries
                if not e.is_scratched
            ]),
        }

    # ═══════════════════════════════════════════
    # PRIVATE: Helpers
    # ═══════════════════════════════════════════

    def _get_trainer_stats(
        self, trainer_name: str, race_date=None
    ) -> Optional[dict]:
        """REPAIR-5 Step B: AS-OF read against trainer_stats_history.

        race_date is the AS-OF anchor — query returns most recent snapshot
        with snapshot_date <= race_date. Substrate-prophylactic per § 4.32
        #18: race_date is REQUIRED (raises ValueError if missing).

        Falls back to current trainer_stats materialized view if the
        history table has no snapshot for the AS-OF date (cold-start
        before daily snapshots accumulate).
        """
        if not trainer_name:
            return None
        if race_date is None:
            raise ValueError(
                "race_date is required for trainer_stats AS-OF discipline "
                "(REPAIR-5 B). Pass race.race_date from calling context."
            )
        key = (trainer_name.lower(), str(race_date))
        if key in self._trainer_stats_cache:
            return self._trainer_stats_cache[key]
        try:
            from shared.db import execute_one
            row = execute_one(
                self.conn,
                """SELECT
                     total_starts,
                     win_rate,
                     itm_rate,
                     layoff_win_rate,
                     lasix_win_rate
                   FROM trainer_stats_history
                   WHERE LOWER(trainer_name) = LOWER(%s)
                     AND snapshot_date <= %s
                   ORDER BY snapshot_date DESC LIMIT 1""",
                (trainer_name, race_date)
            )
            if row is None:
                # Substrate-cold-start fallback: history empty for this
                # AS-OF date; use current latest (substrate-pragmatic-
                # approximate AS-OF until daily snapshots accumulate).
                row = execute_one(
                    self.conn,
                    """SELECT
                         total_starts,
                         win_rate,
                         itm_rate,
                         layoff_win_rate,
                         lasix_win_rate
                       FROM trainer_stats
                       WHERE LOWER(trainer_name) = LOWER(%s)""",
                    (trainer_name,)
                )
            self._trainer_stats_cache[key] = row
            return row
        except Exception as e:
            logger.debug(
                f"trainer_stats lookup failed for "
                f"{trainer_name}: {e}"
            )
            self._trainer_stats_cache[key] = None
            return None

    def _is_front_runner(self, pps: list) -> bool:
        """Returns True if horse avg call_1 <= 2.0."""
        call1s = [
            p.call_1_position for p in pps[:5]
            if p.call_1_position
        ]
        if not call1s:
            return False
        return np.mean(call1s) <= 2.0

    @staticmethod
    def _layoff_bucket(days: float) -> float:
        """Matches data_loader._layoff_bucket exactly."""
        if days is None or (isinstance(days, float) and np.isnan(days)):
            return 2.0
        for lo, hi, bucket in LAYOFF_BUCKETS:
            if lo <= days < hi:
                return float(bucket)
        return 5.0

    @staticmethod
    def _encode_race_quality_tier(
        race_type: Optional[str]
    ) -> float:
        """Matches data_loader._encode_race_quality_tier exactly.
        Higher number = higher quality class.
        stakes=5, allowance=4, msw/maiden=3, claiming=2, mcl=1."""
        if not race_type:
            return 2.0
        rt = race_type.lower()
        if 'stakes' in rt or 'stk' in rt:
            return 5.0
        if 'allowance' in rt or 'alw' in rt:
            return 4.0
        if 'maiden special' in rt or 'msw' in rt:
            return 3.0
        if 'maiden' in rt or 'mdm' in rt:
            return 3.0
        if 'maiden claiming' in rt or 'mcl' in rt:
            return 1.0
        if 'claiming' in rt or 'clm' in rt:
            return 2.0
        return 2.0

    @staticmethod
    def _safe_float(val, default: float) -> float:
        """Return float(val) unless val is None/NaN."""
        if val is None:
            return default
        try:
            f = float(val)
            if np.isnan(f):
                return default
            return f
        except (TypeError, ValueError):
            return default
