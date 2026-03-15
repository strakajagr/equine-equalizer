from typing import Optional
from datetime import date
from .base_repository import BaseRepository
from .transforms import (
    transform_prediction, transform_entry,
    transform_horse, transform_trainer,
    transform_jockey
)
from models.canonical import Prediction


class PredictionRepository(BaseRepository):

    def get_predictions_by_race(
        self, race_id: str
    ) -> list[Prediction]:
        """
        All predictions for a race ordered
        by predicted_rank ascending (best pick first).
        Includes nested Entry -> Horse/Trainer/Jockey.
        """
        rows = self._query(
            """SELECT
                 p.*,
                 e.post_position, e.program_number,
                 e.morning_line_odds, e.weight_carried,
                 e.lasix, e.lasix_first_time,
                 e.blinkers_on, e.blinkers_off,
                 e.blinkers_first_time,
                 e.equipment_change_from_last,
                 e.medication_change_from_last,
                 e.is_scratched,
                 h.horse_id, h.horse_name, h.sire,
                 h.dam, h.dam_sire, h.sex,
                 h.country_of_origin,
                 t.trainer_id, t.trainer_name,
                 j.jockey_id, j.jockey_name,
                 j.is_apprentice
               FROM predictions p
               JOIN entries e ON p.entry_id = e.entry_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               WHERE p.race_id = %s
               ORDER BY p.predicted_rank ASC""",
            (race_id,)
        )
        return self._build_prediction_list(rows)

    def get_predictions_by_date(
        self, race_date: date
    ) -> list[Prediction]:
        """
        All predictions for a given date.
        Joins through entries -> races to filter by date.
        Ordered by race post_time then predicted_rank.
        """
        rows = self._query(
            """SELECT
                 p.*,
                 e.post_position, e.program_number,
                 e.morning_line_odds, e.weight_carried,
                 e.lasix, e.lasix_first_time,
                 e.blinkers_on, e.blinkers_off,
                 e.blinkers_first_time,
                 e.equipment_change_from_last,
                 e.medication_change_from_last,
                 e.is_scratched,
                 h.horse_id, h.horse_name, h.sire,
                 h.dam, h.dam_sire, h.sex,
                 h.country_of_origin,
                 t.trainer_id, t.trainer_name,
                 j.jockey_id, j.jockey_name,
                 j.is_apprentice,
                 r.race_number, r.post_time
               FROM predictions p
               JOIN entries e ON p.entry_id = e.entry_id
               JOIN races r ON p.race_id = r.race_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               WHERE r.race_date = %s
               ORDER BY r.post_time ASC,
                        p.predicted_rank ASC""",
            (race_date,)
        )
        return self._build_prediction_list(rows)

    def get_todays_predictions(
        self
    ) -> list[Prediction]:
        """Predictions for today. Calls get_predictions_by_date."""
        from datetime import date as date_type
        return self.get_predictions_by_date(
            date_type.today()
        )

    def get_top_picks_by_date(
        self, race_date: date
    ) -> list[Prediction]:
        """
        Only predictions where is_top_pick = true.
        These are the #1 ranked horse per race.
        """
        rows = self._query(
            """SELECT
                 p.*,
                 e.post_position, e.program_number,
                 e.morning_line_odds, e.weight_carried,
                 e.lasix, e.lasix_first_time,
                 e.blinkers_on, e.blinkers_off,
                 e.blinkers_first_time,
                 e.equipment_change_from_last,
                 e.medication_change_from_last,
                 e.is_scratched,
                 h.horse_id, h.horse_name, h.sire,
                 h.dam, h.dam_sire, h.sex,
                 h.country_of_origin,
                 t.trainer_id, t.trainer_name,
                 j.jockey_id, j.jockey_name,
                 j.is_apprentice,
                 r.race_number, r.post_time
               FROM predictions p
               JOIN entries e ON p.entry_id = e.entry_id
               JOIN races r ON p.race_id = r.race_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               WHERE r.race_date = %s
                 AND p.is_top_pick = true
               ORDER BY r.post_time ASC""",
            (race_date,)
        )
        return self._build_prediction_list(rows)

    def get_value_plays_by_date(
        self, race_date: date
    ) -> list[Prediction]:
        """
        Predictions flagged as value plays.
        is_value_flag = true means model probability
        significantly exceeds morning line implied prob.
        These are the overlay horses.
        """
        rows = self._query(
            """SELECT
                 p.*,
                 e.post_position, e.program_number,
                 e.morning_line_odds, e.weight_carried,
                 e.lasix, e.lasix_first_time,
                 e.blinkers_on, e.blinkers_off,
                 e.blinkers_first_time,
                 e.equipment_change_from_last,
                 e.medication_change_from_last,
                 e.is_scratched,
                 h.horse_id, h.horse_name, h.sire,
                 h.dam, h.dam_sire, h.sex,
                 h.country_of_origin,
                 t.trainer_id, t.trainer_name,
                 j.jockey_id, j.jockey_name,
                 j.is_apprentice,
                 r.race_number, r.post_time,
                 tr.track_code, tr.track_name
               FROM predictions p
               JOIN entries e ON p.entry_id = e.entry_id
               JOIN races r ON p.race_id = r.race_id
               JOIN tracks tr ON r.track_id = tr.track_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               WHERE r.race_date = %s
                 AND p.is_value_flag = true
               ORDER BY p.overlay_pct DESC""",
            (race_date,)
        )
        return self._build_prediction_list(rows)

    def insert_prediction(
        self, prediction_data: dict
    ) -> str:
        """Insert prediction. Returns prediction_id."""
        row = self._write_returning(
            """INSERT INTO predictions (
                 entry_id, race_id, horse_id,
                 model_version_id,
                 win_probability, place_probability,
                 show_probability, predicted_rank,
                 confidence_score, is_top_pick,
                 is_value_flag, morning_line_implied_prob,
                 overlay_pct, feature_importance,
                 recommended_bet_type, exotic_partners
               ) VALUES (
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s
               )
               ON CONFLICT (entry_id) DO UPDATE SET
                 win_probability = EXCLUDED.win_probability,
                 place_probability =
                   EXCLUDED.place_probability,
                 show_probability =
                   EXCLUDED.show_probability,
                 predicted_rank = EXCLUDED.predicted_rank,
                 confidence_score =
                   EXCLUDED.confidence_score,
                 is_top_pick = EXCLUDED.is_top_pick,
                 is_value_flag = EXCLUDED.is_value_flag,
                 overlay_pct = EXCLUDED.overlay_pct,
                 feature_importance =
                   EXCLUDED.feature_importance,
                 recommended_bet_type =
                   EXCLUDED.recommended_bet_type,
                 exotic_partners = EXCLUDED.exotic_partners
               RETURNING prediction_id""",
            (
                prediction_data['entry_id'],
                prediction_data['race_id'],
                prediction_data['horse_id'],
                prediction_data.get('model_version_id'),
                prediction_data.get('win_probability'),
                prediction_data.get('place_probability'),
                prediction_data.get('show_probability'),
                prediction_data.get('predicted_rank'),
                prediction_data.get('confidence_score'),
                prediction_data.get('is_top_pick', False),
                prediction_data.get('is_value_flag', False),
                prediction_data.get(
                    'morning_line_implied_prob'),
                prediction_data.get('overlay_pct'),
                prediction_data.get('feature_importance'),
                prediction_data.get('recommended_bet_type'),
                prediction_data.get('exotic_partners', [])
            )
        )
        return str(row['prediction_id'])

    def update_prediction_result(
        self,
        prediction_id: str,
        actual_finish: int,
        was_win: bool,
        was_place: bool,
        was_show: bool,
        exacta_hit: bool,
        trifecta_hit: bool
    ) -> None:
        """
        Fill in actual results after race completes.
        Called by evaluation service nightly.
        """
        self._write(
            """UPDATE predictions SET
                 actual_finish = %s,
                 was_win = %s,
                 was_place = %s,
                 was_show = %s,
                 exacta_hit = %s,
                 trifecta_hit = %s
               WHERE prediction_id = %s""",
            (
                actual_finish,
                was_win,
                was_place,
                was_show,
                exacta_hit,
                trifecta_hit,
                prediction_id
            )
        )

    def get_model_performance_summary(
        self,
        model_version_id: str
    ) -> dict:
        """
        Aggregate hit rates for a model version.
        Returns dict with exacta_hit_rate,
        trifecta_hit_rate, win_rate, top3_rate.
        Used by evaluation service to update
        model_versions table after enough races.
        """
        row = self._query_one(
            """SELECT
                 COUNT(*) as total_predictions,
                 COUNT(*) FILTER (
                   WHERE is_top_pick = true
                 ) as top_pick_count,
                 AVG(CASE WHEN was_win = true
                   AND is_top_pick = true
                   THEN 1.0 ELSE 0.0 END
                 ) as win_rate,
                 AVG(CASE WHEN exacta_hit = true
                   THEN 1.0 ELSE 0.0 END
                 ) as exacta_hit_rate,
                 AVG(CASE WHEN trifecta_hit = true
                   THEN 1.0 ELSE 0.0 END
                 ) as trifecta_hit_rate
               FROM predictions
               WHERE model_version_id = %s
                 AND actual_finish IS NOT NULL""",
            (model_version_id,)
        )
        return dict(row) if row else {}

    def _build_prediction_list(
        self, rows: list[dict]
    ) -> list[Prediction]:
        """
        Private helper.
        Builds Prediction objects from joined rows.
        """
        predictions = []
        for row in rows:
            horse = transform_horse({
                'horse_id': row.get('horse_id'),
                'horse_name': row.get('horse_name'),
                'sire': row.get('sire'),
                'dam': row.get('dam'),
                'dam_sire': row.get('dam_sire'),
                'sex': row.get('sex'),
                'country_of_origin': row.get(
                    'country_of_origin')
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
            predictions.append(
                transform_prediction(row, entry)
            )
        return predictions
