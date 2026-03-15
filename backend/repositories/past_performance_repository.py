from typing import Optional
from datetime import date
from .base_repository import BaseRepository
from .transforms import transform_past_performance
from models.canonical import PastPerformance


class PastPerformanceRepository(BaseRepository):

    def get_past_performances(
        self,
        horse_id: str,
        limit: int = 10,
        surface: str = None,
        track_code: str = None
    ) -> list[PastPerformance]:
        """
        Get past performances for a horse.
        Optional filters: surface, track_code.
        Always ordered by race_date DESC (most recent first).
        """
        conditions = ["horse_id = %s"]
        params = [horse_id]

        if surface:
            conditions.append("surface = %s")
            params.append(surface)
        if track_code:
            conditions.append("track_code = %s")
            params.append(track_code)

        params.append(limit)
        where = " AND ".join(conditions)

        rows = self._query(
            f"""SELECT * FROM past_performances
                WHERE {where}
                ORDER BY race_date DESC
                LIMIT %s""",
            tuple(params)
        )
        return [transform_past_performance(r) for r in rows]

    def get_best_speed_figure(
        self, horse_id: str
    ) -> Optional[int]:
        """
        Returns highest Beyer speed figure ever
        recorded for this horse.
        """
        row = self._query_one(
            """SELECT MAX(beyer_speed_figure) as best_beyer
               FROM past_performances
               WHERE horse_id = %s
                 AND beyer_speed_figure IS NOT NULL""",
            (horse_id,)
        )
        return row['best_beyer'] if row else None

    def get_speed_figures_last_n(
        self,
        horse_id: str,
        n: int = 5
    ) -> list[int]:
        """
        Returns list of last N Beyer figures
        ordered most recent first.
        Excludes NULL figures.
        """
        rows = self._query(
            """SELECT beyer_speed_figure
               FROM past_performances
               WHERE horse_id = %s
                 AND beyer_speed_figure IS NOT NULL
               ORDER BY race_date DESC
               LIMIT %s""",
            (horse_id, n)
        )
        return [r['beyer_speed_figure'] for r in rows]

    def get_performances_on_surface(
        self,
        horse_id: str,
        surface: str
    ) -> list[PastPerformance]:
        """All past performances on a specific surface."""
        rows = self._query(
            """SELECT * FROM past_performances
               WHERE horse_id = %s
                 AND surface = %s
               ORDER BY race_date DESC""",
            (horse_id, surface)
        )
        return [transform_past_performance(r) for r in rows]

    def get_performances_at_distance(
        self,
        horse_id: str,
        distance_furlongs: float,
        tolerance: float = 0.5
    ) -> list[PastPerformance]:
        """
        Past performances within tolerance of distance.
        Default tolerance = 0.5 furlongs.
        e.g. querying 8.0f returns 7.5f through 8.5f.
        """
        rows = self._query(
            """SELECT * FROM past_performances
               WHERE horse_id = %s
                 AND distance_furlongs
                   BETWEEN %s AND %s
               ORDER BY race_date DESC""",
            (
                horse_id,
                distance_furlongs - tolerance,
                distance_furlongs + tolerance
            )
        )
        return [transform_past_performance(r) for r in rows]

    def get_performances_at_track(
        self,
        horse_id: str,
        track_code: str
    ) -> list[PastPerformance]:
        """All past performances at a specific track."""
        rows = self._query(
            """SELECT * FROM past_performances
               WHERE horse_id = %s
                 AND track_code = %s
               ORDER BY race_date DESC""",
            (horse_id, track_code)
        )
        return [transform_past_performance(r) for r in rows]

    def insert_past_performance(
        self, pp_data: dict
    ) -> str:
        """
        Insert single past performance.
        Returns pp_id.
        Uses ON CONFLICT DO NOTHING —
        never overwrites existing PP data.
        """
        row = self._write_returning(
            """INSERT INTO past_performances (
                 horse_id, race_id, race_date, track_code,
                 race_number, race_start_number,
                 distance_furlongs, surface, race_type,
                 claiming_price_entered, claiming_price_taken,
                 was_claimed, purse, field_size,
                 track_condition, moisture_level,
                 track_variant, temperature,
                 weather_conditions, wind_speed,
                 wind_direction, off_turf,
                 jockey_name, trainer_name,
                 previous_trainer, trainer_change,
                 jockey_change, apprentice_allowance,
                 weight_carried,
                 lasix, lasix_first_time, bute,
                 blinkers_on, blinkers_off,
                 blinkers_first_time, tongue_tie,
                 bar_shoes, front_bandages, mud_caulks,
                 equipment_change_from_last,
                 medication_change_from_last,
                 post_position, finish_position,
                 official_finish, lengths_behind,
                 is_disqualified, photo_finish,
                 nose_bob, disqualification_involved,
                 beyer_speed_figure, timeform_rating,
                 equibase_speed_figure,
                 winner_beyer, field_average_beyer,
                 fraction_1, fraction_2, fraction_3,
                 final_time,
                 horse_fraction_1, horse_fraction_2,
                 horse_fraction_3,
                 call_1_position, call_1_lengths,
                 call_2_position, call_2_lengths,
                 call_3_position, call_3_lengths,
                 stretch_position, stretch_lengths,
                 finish_call_position,
                 early_pace_figure, late_pace_figure,
                 pace_scenario, running_style,
                 early_pace_pressure,
                 winner_name, second_name, third_name,
                 winner_time, closing_odds,
                 morning_line_that_day, was_favorite,
                 odds_rank_in_field, class_rating,
                 days_since_last_race,
                 comment, trouble_comment
               ) VALUES (
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s
               )
               ON CONFLICT
                 (horse_id, race_date, track_code, race_number)
               DO NOTHING
               RETURNING pp_id""",
            (
                pp_data['horse_id'],
                pp_data.get('race_id'),
                pp_data['race_date'],
                pp_data['track_code'],
                pp_data.get('race_number'),
                pp_data.get('race_start_number'),
                pp_data.get('distance_furlongs'),
                pp_data.get('surface'),
                pp_data.get('race_type'),
                pp_data.get('claiming_price_entered'),
                pp_data.get('claiming_price_taken'),
                pp_data.get('was_claimed', False),
                pp_data.get('purse'),
                pp_data.get('field_size'),
                pp_data.get('track_condition'),
                pp_data.get('moisture_level'),
                pp_data.get('track_variant'),
                pp_data.get('temperature'),
                pp_data.get('weather_conditions'),
                pp_data.get('wind_speed'),
                pp_data.get('wind_direction'),
                pp_data.get('off_turf', False),
                pp_data.get('jockey_name'),
                pp_data.get('trainer_name'),
                pp_data.get('previous_trainer'),
                pp_data.get('trainer_change', False),
                pp_data.get('jockey_change', False),
                pp_data.get('apprentice_allowance', 0),
                pp_data.get('weight_carried'),
                pp_data.get('lasix', False),
                pp_data.get('lasix_first_time', False),
                pp_data.get('bute', False),
                pp_data.get('blinkers_on', False),
                pp_data.get('blinkers_off', False),
                pp_data.get('blinkers_first_time', False),
                pp_data.get('tongue_tie', False),
                pp_data.get('bar_shoes', False),
                pp_data.get('front_bandages', False),
                pp_data.get('mud_caulks', False),
                pp_data.get(
                    'equipment_change_from_last', False),
                pp_data.get(
                    'medication_change_from_last', False),
                pp_data.get('post_position'),
                pp_data.get('finish_position'),
                pp_data.get('official_finish'),
                pp_data.get('lengths_behind'),
                pp_data.get('is_disqualified', False),
                pp_data.get('photo_finish', False),
                pp_data.get('nose_bob', False),
                pp_data.get(
                    'disqualification_involved', False),
                pp_data.get('beyer_speed_figure'),
                pp_data.get('timeform_rating'),
                pp_data.get('equibase_speed_figure'),
                pp_data.get('winner_beyer'),
                pp_data.get('field_average_beyer'),
                pp_data.get('fraction_1'),
                pp_data.get('fraction_2'),
                pp_data.get('fraction_3'),
                pp_data.get('final_time'),
                pp_data.get('horse_fraction_1'),
                pp_data.get('horse_fraction_2'),
                pp_data.get('horse_fraction_3'),
                pp_data.get('call_1_position'),
                pp_data.get('call_1_lengths'),
                pp_data.get('call_2_position'),
                pp_data.get('call_2_lengths'),
                pp_data.get('call_3_position'),
                pp_data.get('call_3_lengths'),
                pp_data.get('stretch_position'),
                pp_data.get('stretch_lengths'),
                pp_data.get('finish_call_position'),
                pp_data.get('early_pace_figure'),
                pp_data.get('late_pace_figure'),
                pp_data.get('pace_scenario'),
                pp_data.get('running_style'),
                pp_data.get('early_pace_pressure'),
                pp_data.get('winner_name'),
                pp_data.get('second_name'),
                pp_data.get('third_name'),
                pp_data.get('winner_time'),
                pp_data.get('closing_odds'),
                pp_data.get('morning_line_that_day'),
                pp_data.get('was_favorite', False),
                pp_data.get('odds_rank_in_field'),
                pp_data.get('class_rating'),
                pp_data.get('days_since_last_race'),
                pp_data.get('comment'),
                pp_data.get('trouble_comment')
            )
        )
        return str(row['pp_id']) if row else None

    def bulk_insert_past_performances(
        self, pp_list: list[dict]
    ) -> int:
        """
        Insert multiple past performances.
        Returns count of successfully inserted rows.
        Skips duplicates silently (ON CONFLICT DO NOTHING).
        """
        count = 0
        for pp_data in pp_list:
            result = self.insert_past_performance(pp_data)
            if result:
                count += 1
        return count
