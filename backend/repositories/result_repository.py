from typing import Optional
from datetime import date
from .base_repository import BaseRepository
from .transforms import (
    transform_result, transform_entry,
    transform_horse, transform_trainer,
    transform_jockey
)
from models.canonical import Result


class ResultRepository(BaseRepository):

    def get_result_by_entry(
        self, entry_id: str
    ) -> Optional[Result]:
        """Single result with nested Entry."""
        row = self._query_one(
            """SELECT
                 res.*,
                 e.post_position, e.program_number,
                 e.morning_line_odds, e.weight_carried,
                 e.lasix, e.lasix_first_time,
                 e.blinkers_on, e.blinkers_off,
                 e.blinkers_first_time,
                 h.horse_id, h.horse_name, h.sire,
                 h.dam, h.sex, h.country_of_origin,
                 t.trainer_id, t.trainer_name,
                 j.jockey_id, j.jockey_name,
                 j.is_apprentice
               FROM results res
               JOIN entries e
                 ON res.entry_id = e.entry_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t
                 ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               WHERE res.entry_id = %s""",
            (entry_id,)
        )
        if not row:
            return None
        return self._build_result(row)

    def get_results_by_race(
        self, race_id: str
    ) -> list[Result]:
        """
        All results for a race.
        Ordered by official_finish ascending.
        """
        rows = self._query(
            """SELECT
                 res.*,
                 e.post_position, e.program_number,
                 e.morning_line_odds, e.weight_carried,
                 e.lasix, e.lasix_first_time,
                 e.blinkers_on, e.blinkers_off,
                 e.blinkers_first_time,
                 h.horse_id, h.horse_name, h.sire,
                 h.dam, h.sex, h.country_of_origin,
                 t.trainer_id, t.trainer_name,
                 j.jockey_id, j.jockey_name,
                 j.is_apprentice
               FROM results res
               JOIN entries e
                 ON res.entry_id = e.entry_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t
                 ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               WHERE res.race_id = %s
               ORDER BY res.official_finish ASC""",
            (race_id,)
        )
        return [self._build_result(r) for r in rows]

    def get_results_by_date_range(
        self,
        start_date: date,
        end_date: date
    ) -> list[Result]:
        """
        Results for a date range.
        Joins through races to filter by date.
        Used for model evaluation over time periods.
        """
        rows = self._query(
            """SELECT
                 res.*,
                 e.post_position, e.program_number,
                 e.morning_line_odds, e.weight_carried,
                 e.lasix, e.lasix_first_time,
                 e.blinkers_on, e.blinkers_off,
                 e.blinkers_first_time,
                 h.horse_id, h.horse_name, h.sire,
                 h.dam, h.sex, h.country_of_origin,
                 t.trainer_id, t.trainer_name,
                 j.jockey_id, j.jockey_name,
                 j.is_apprentice
               FROM results res
               JOIN entries e
                 ON res.entry_id = e.entry_id
               JOIN races r ON res.race_id = r.race_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t
                 ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               WHERE r.race_date
                 BETWEEN %s AND %s
               ORDER BY r.race_date ASC,
                        res.official_finish ASC""",
            (start_date, end_date)
        )
        return [self._build_result(r) for r in rows]

    def insert_result(
        self, result_data: dict
    ) -> str:
        """Insert result. Returns result_id."""
        row = self._write_returning(
            """INSERT INTO results (
                 entry_id, race_id, horse_id,
                 finish_position, official_finish,
                 is_disqualified, dq_from, dq_to,
                 lengths_behind, final_time,
                 beyer_speed_figure,
                 call_1_position, call_1_lengths,
                 call_2_position, call_2_lengths,
                 stretch_position, stretch_lengths,
                 win_payout, place_payout, show_payout,
                 exacta_payout, trifecta_payout,
                 superfecta_payout, daily_double_payout
               ) VALUES (
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s
               )
               ON CONFLICT (entry_id) DO UPDATE SET
                 official_finish = EXCLUDED.official_finish,
                 is_disqualified = EXCLUDED.is_disqualified,
                 dq_from = EXCLUDED.dq_from,
                 dq_to = EXCLUDED.dq_to,
                 beyer_speed_figure =
                   EXCLUDED.beyer_speed_figure,
                 win_payout = EXCLUDED.win_payout,
                 place_payout = EXCLUDED.place_payout,
                 show_payout = EXCLUDED.show_payout,
                 exacta_payout = EXCLUDED.exacta_payout,
                 trifecta_payout = EXCLUDED.trifecta_payout,
                 superfecta_payout =
                   EXCLUDED.superfecta_payout,
                 daily_double_payout =
                   EXCLUDED.daily_double_payout
               RETURNING result_id""",
            (
                result_data['entry_id'],
                result_data['race_id'],
                result_data['horse_id'],
                result_data['finish_position'],
                result_data['official_finish'],
                result_data.get('is_disqualified', False),
                result_data.get('dq_from'),
                result_data.get('dq_to'),
                result_data.get('lengths_behind'),
                result_data.get('final_time'),
                result_data.get('beyer_speed_figure'),
                result_data.get('call_1_position'),
                result_data.get('call_1_lengths'),
                result_data.get('call_2_position'),
                result_data.get('call_2_lengths'),
                result_data.get('stretch_position'),
                result_data.get('stretch_lengths'),
                result_data.get('win_payout'),
                result_data.get('place_payout'),
                result_data.get('show_payout'),
                result_data.get('exacta_payout'),
                result_data.get('trifecta_payout'),
                result_data.get('superfecta_payout'),
                result_data.get('daily_double_payout')
            )
        )
        return str(row['result_id'])

    def _build_result(self, row: dict) -> Result:
        """Private helper. Builds Result from joined row."""
        horse = transform_horse({
            'horse_id': row.get('horse_id'),
            'horse_name': row.get('horse_name'),
            'sire': row.get('sire'),
            'dam': row.get('dam'),
            'sex': row.get('sex'),
            'country_of_origin': row.get('country_of_origin')
        })
        trainer = transform_trainer({
            'trainer_id': row.get('trainer_id'),
            'trainer_name': row.get('trainer_name')
        })
        jockey = None
        if row.get('jockey_id'):
            jockey = transform_jockey({
                'jockey_id': row.get('jockey_id'),
                'jockey_name': row.get('jockey_name'),
                'is_apprentice': row.get('is_apprentice')
            })
        entry = transform_entry(
            row, horse, trainer, jockey, []
        )
        return transform_result(row, entry)
