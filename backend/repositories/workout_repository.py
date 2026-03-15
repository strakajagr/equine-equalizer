from typing import Optional
from datetime import date
from .base_repository import BaseRepository
from .transforms import transform_workout
from models.canonical import Workout
from shared.constants import WORKOUT_LOOKBACK_DAYS


class WorkoutRepository(BaseRepository):

    def get_workouts_by_horse(
        self,
        horse_id: str,
        days_back: int = WORKOUT_LOOKBACK_DAYS
    ) -> list[Workout]:
        """
        Get all workouts for a horse within
        the last N days. Ordered most recent first.
        """
        rows = self._query(
            """SELECT * FROM workouts
               WHERE horse_id = %s
                 AND workout_date >=
                   CURRENT_DATE - INTERVAL '%s days'
               ORDER BY workout_date DESC""",
            (horse_id, days_back)
        )
        return [transform_workout(r) for r in rows]

    def get_recent_bullet_works(
        self,
        horse_id: str,
        days: int = 30
    ) -> list[Workout]:
        """
        Get bullet workouts (fastest of morning)
        within the last N days.
        A bullet work = is_bullet = true.
        """
        rows = self._query(
            """SELECT * FROM workouts
               WHERE horse_id = %s
                 AND is_bullet = true
                 AND workout_date >=
                   CURRENT_DATE - INTERVAL '%s days'
               ORDER BY workout_date DESC""",
            (horse_id, days)
        )
        return [transform_workout(r) for r in rows]

    def get_workouts_before_race(
        self,
        horse_id: str,
        race_date: date,
        days_back: int = WORKOUT_LOOKBACK_DAYS
    ) -> list[Workout]:
        """
        Get workouts that occurred before a specific
        race date within lookback window.
        Used during feature engineering to get the
        workout picture a horse had going into a race.
        """
        rows = self._query(
            """SELECT * FROM workouts
               WHERE horse_id = %s
                 AND workout_date < %s
                 AND workout_date >= %s - INTERVAL '%s days'
               ORDER BY workout_date DESC""",
            (horse_id, race_date, race_date, days_back)
        )
        return [transform_workout(r) for r in rows]

    def get_workout_count_last_n_days(
        self,
        horse_id: str,
        days: int = 30
    ) -> int:
        """
        Count of workouts in last N days.
        Used as a feature: how actively is this
        horse being pointed at this spot?
        """
        row = self._query_one(
            """SELECT COUNT(*) as workout_count
               FROM workouts
               WHERE horse_id = %s
                 AND workout_date >=
                   CURRENT_DATE - INTERVAL '%s days'""",
            (horse_id, days)
        )
        return row['workout_count'] if row else 0

    def get_best_workout_speed_index(
        self,
        horse_id: str,
        days_back: int = WORKOUT_LOOKBACK_DAYS
    ) -> Optional[float]:
        """
        Returns the best (lowest) workout speed index
        for a horse within lookback window.
        Lower = faster.
        workout_speed_index = workout_time / furlongs
        Computed in transform, not stored in DB.
        So we derive from stored fields here.
        """
        row = self._query_one(
            """SELECT
                 MIN(workout_time / distance_furlongs)
                   as best_speed_index
               FROM workouts
               WHERE horse_id = %s
                 AND workout_date >=
                   CURRENT_DATE - INTERVAL '%s days'
                 AND distance_furlongs > 0""",
            (horse_id, days_back)
        )
        if row and row['best_speed_index']:
            return float(row['best_speed_index'])
        return None

    def insert_workout(
        self, workout_data: dict
    ) -> str:
        """Insert single workout. Returns workout_id."""
        row = self._write_returning(
            """INSERT INTO workouts (
                 horse_id, workout_date, track_code,
                 distance_furlongs, workout_time,
                 is_bullet, track_condition,
                 workout_type, rank_on_day,
                 total_works_on_day, exercise_rider
               ) VALUES (
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
               )
               ON CONFLICT
                 (horse_id, workout_date,
                  track_code, distance_furlongs)
               DO UPDATE SET
                 workout_time = EXCLUDED.workout_time,
                 is_bullet = EXCLUDED.is_bullet,
                 rank_on_day = EXCLUDED.rank_on_day,
                 total_works_on_day =
                   EXCLUDED.total_works_on_day
               RETURNING workout_id""",
            (
                workout_data['horse_id'],
                workout_data['workout_date'],
                workout_data['track_code'],
                workout_data['distance_furlongs'],
                workout_data['workout_time'],
                workout_data.get('is_bullet', False),
                workout_data.get('track_condition'),
                workout_data.get('workout_type'),
                workout_data.get('rank_on_day'),
                workout_data.get('total_works_on_day'),
                workout_data.get('exercise_rider')
            )
        )
        return str(row['workout_id'])

    def bulk_insert_workouts(
        self, workouts: list[dict]
    ) -> int:
        """
        Insert multiple workouts.
        Returns count of successfully inserted rows.
        """
        count = 0
        for workout_data in workouts:
            result = self.insert_workout(workout_data)
            if result:
                count += 1
        return count
