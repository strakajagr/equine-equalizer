from typing import Optional
from datetime import date
from psycopg2.extras import Json
from .base_repository import BaseRepository
from .transforms import (
    transform_entry, transform_horse,
    transform_trainer, transform_jockey
)
from models.canonical import LSPrediction


def _to_float(val) -> Optional[float]:
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _to_int(val) -> Optional[int]:
    if val is None:
        return None
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def _to_bool(val) -> bool:
    if val is None:
        return False
    return bool(val)


def _to_str(val) -> Optional[str]:
    if val is None:
        return None
    return str(val).strip()


class LSPredictionRepository(BaseRepository):
    """
    Prediction repository for the LS (Longshot)
    meta-model. Targets ls_predictions table —
    independent schema with ensemble base model scores
    and longshot alert flag.
    """

    def get_predictions_by_race(
        self, race_id: str, style: str = 'general'
    ) -> list[LSPrediction]:
        """
        All LS predictions for a race ordered
        by predicted_rank ascending.

        style: 'general' (default) | 'gonzo_sauce' | other gallery styles
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
                 r.race_number,
                 res.finish_position AS actual_finish_position,
                 res.win_payout      AS actual_win_payout,
                 res.place_payout    AS actual_place_payout,
                 res.show_payout     AS actual_show_payout,
                 CASE
                   WHEN e.is_scratched = TRUE       THEN 'scratched'
                   WHEN res.finish_position IS NULL THEN 'pending'
                   WHEN res.finish_position = 1     THEN 'win'
                   WHEN res.finish_position = 2     THEN 'place'
                   WHEN res.finish_position = 3     THEN 'show'
                   ELSE                                  'lose'
                 END AS prediction_outcome,
                 CASE
                   WHEN e.is_scratched = TRUE       THEN 0
                   WHEN res.finish_position IS NULL THEN NULL
                   WHEN res.finish_position = 1
                        AND res.win_payout IS NOT NULL
                                                    THEN res.win_payout - 2
                   WHEN res.finish_position = 1     THEN NULL
                   ELSE                                  -2
                 END AS flat_bet_pl
               FROM ls_predictions p
               JOIN entries e ON p.entry_id = e.entry_id
               JOIN races r ON p.race_id = r.race_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               LEFT JOIN results res
                 ON res.entry_id = p.entry_id
               WHERE p.race_id = %s
                 AND p.style = %s
                 AND COALESCE(e.is_scratched, FALSE) = FALSE
               ORDER BY p.predicted_rank ASC""",
            (race_id, style)
        )
        return self._build_ls_prediction_list(rows)

    def get_predictions_by_date(
        self, race_date: date
    ) -> list[LSPrediction]:
        """All LS predictions for a given date."""
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
                 res.finish_position AS actual_finish_position,
                 res.win_payout      AS actual_win_payout,
                 res.place_payout    AS actual_place_payout,
                 res.show_payout     AS actual_show_payout,
                 CASE
                   WHEN e.is_scratched = TRUE       THEN 'scratched'
                   WHEN res.finish_position IS NULL THEN 'pending'
                   WHEN res.finish_position = 1     THEN 'win'
                   WHEN res.finish_position = 2     THEN 'place'
                   WHEN res.finish_position = 3     THEN 'show'
                   ELSE                                  'lose'
                 END AS prediction_outcome,
                 CASE
                   WHEN e.is_scratched = TRUE       THEN 0
                   WHEN res.finish_position IS NULL THEN NULL
                   WHEN res.finish_position = 1
                        AND res.win_payout IS NOT NULL
                                                    THEN res.win_payout - 2
                   WHEN res.finish_position = 1     THEN NULL
                   ELSE                                  -2
                 END AS flat_bet_pl
               FROM ls_predictions p
               JOIN entries e ON p.entry_id = e.entry_id
               JOIN races r ON p.race_id = r.race_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               LEFT JOIN results res
                 ON res.entry_id = p.entry_id
               WHERE r.race_date = %s
                 AND COALESCE(e.is_scratched, FALSE) = FALSE
               ORDER BY r.post_time ASC,
                        p.predicted_rank ASC""",
            (race_date,)
        )
        return self._build_ls_prediction_list(rows)

    def get_todays_predictions(
        self
    ) -> list[LSPrediction]:
        """LS predictions for today."""
        from datetime import date as date_type
        return self.get_predictions_by_date(
            date_type.today()
        )

    def get_longshot_alerts_by_date(
        self, race_date: date
    ) -> list[LSPrediction]:
        """
        LS-enriched predictions: per-race top-1 longshot pick.

        Phase A3 (2026-05-02): relaxed from strict longshot_alert=TRUE
        filter to per-race predicted_rank=1 gated by ml_odds >= 8.
        Strict alert flag remains in the response payload (longshot_alert
        column) so the frontend can optionally surface a "🔥 ALERT"
        badge on entries that DO cross the strict 4-way AND threshold.
        Bug #25 — strict AND with traj_score>0 fails for thin-PP-history
        3yo fields (Derby Day produces zero alerts on CD); Phase A3.5
        will fix the alert formula upstream.

        LS data is written as second-pass enrichment to wr_predictions
        columns (ensemble_win_prob, longshot_prob, trajectory_score,
        angle_*, longshot_alert, confidence) — not to a separate
        ls_predictions table. Columns are aliased here to match the
        LSPrediction dataclass schema so _build_ls_prediction_list
        works unchanged.

        Ordered by ensemble_win_prob descending (best-conviction LS
        pick across the day comes first).
        """
        rows = self._query(
            """SELECT
                 p.prediction_id, p.entry_id, p.race_id, p.horse_id,
                 p.model_version_id,
                 p.ensemble_win_prob   AS final_win_probability,
                 p.longshot_alert, p.confidence,
                 p.kelly_fraction, p.predicted_rank,
                 p.rank_score          AS xgb_rank_score,
                 p.longshot_prob       AS rf_longshot_prob,
                 p.trajectory_score    AS lstm_trajectory,
                 p.raw_win_prob        AS calibrated_win_prob,
                 p.angle_ev            AS bayesian_angle_ev,
                 p.angle_name          AS angle_description,
                 p.feature_importance,
                 p.actual_finish, p.was_win,
                 p.created_at,
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
                 r.race_date, r.race_number, r.post_time,
                 tr.track_code, tr.track_name,
                 res.finish_position AS actual_finish_position,
                 res.win_payout      AS actual_win_payout,
                 res.place_payout    AS actual_place_payout,
                 res.show_payout     AS actual_show_payout,
                 CASE
                   WHEN e.is_scratched = TRUE       THEN 'scratched'
                   WHEN res.finish_position IS NULL THEN 'pending'
                   WHEN res.finish_position = 1     THEN 'win'
                   WHEN res.finish_position = 2     THEN 'place'
                   WHEN res.finish_position = 3     THEN 'show'
                   ELSE                                  'lose'
                 END AS prediction_outcome,
                 CASE
                   WHEN e.is_scratched = TRUE       THEN 0
                   WHEN res.finish_position IS NULL THEN NULL
                   WHEN res.finish_position = 1
                        AND res.win_payout IS NOT NULL
                                                    THEN res.win_payout - 2
                   WHEN res.finish_position = 1     THEN NULL
                   ELSE                                  -2
                 END AS flat_bet_pl
               FROM wr_predictions p
               JOIN entries e ON p.entry_id = e.entry_id
               JOIN races r ON p.race_id = r.race_id
               JOIN tracks tr ON r.track_id = tr.track_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               LEFT JOIN results res
                 ON res.entry_id = p.entry_id
               WHERE r.race_date = %s
                 AND p.style = 'general'
                 AND p.predicted_rank = 1
                 AND COALESCE(e.morning_line_odds, 0) >= 8
                 AND COALESCE(e.is_scratched, FALSE) = FALSE
               ORDER BY p.ensemble_win_prob DESC NULLS LAST""",
            (race_date,)
        )
        return self._build_ls_prediction_list(rows)

    def insert_prediction(
        self, prediction_data: dict
    ) -> str:
        """Insert LS prediction. Returns prediction_id."""
        row = self._write_returning(
            """INSERT INTO ls_predictions (
                 entry_id, race_id, horse_id,
                 model_version_id,
                 final_win_probability,
                 longshot_alert, confidence,
                 kelly_fraction, predicted_rank,
                 xgb_rank_score, rf_longshot_prob,
                 lstm_trajectory, calibrated_win_prob,
                 bayesian_angle_ev, angle_description,
                 feature_importance
               ) VALUES (
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s
               )
               -- REPAIR-4: DO NOTHING substrate-protects clean writes
               ON CONFLICT (entry_id) DO NOTHING
               RETURNING prediction_id""",
            (
                prediction_data['entry_id'],
                prediction_data['race_id'],
                prediction_data['horse_id'],
                prediction_data.get('model_version_id'),
                prediction_data.get(
                    'final_win_probability'),
                prediction_data.get(
                    'longshot_alert', False),
                prediction_data.get('confidence'),
                prediction_data.get('kelly_fraction'),
                prediction_data.get('predicted_rank'),
                prediction_data.get('xgb_rank_score'),
                prediction_data.get('rf_longshot_prob'),
                prediction_data.get('lstm_trajectory'),
                prediction_data.get('calibrated_win_prob'),
                prediction_data.get('bayesian_angle_ev'),
                prediction_data.get('angle_description'),
                Json(prediction_data.get(
                    'feature_importance') or {})
            )
        )
        return str(row['prediction_id'])

    def get_track_record(self, window_days: int) -> dict:
        """Aggregate LS longshot-alert rows for the trailing window_days.

        LS doesn't have a single top-1 pick per race — it emits 0..N alerts.
        Track record aggregates over all rows where longshot_alert=TRUE
        on wr_predictions (where LS data lives).
        """
        from .track_record import aggregate_picks
        rows = self._query(
            """SELECT
                 r.race_date,
                 t.track_code,
                 CASE
                   WHEN e.is_scratched = TRUE       THEN 'scratched'
                   WHEN res.finish_position IS NULL THEN 'pending'
                   WHEN res.finish_position = 1     THEN 'win'
                   WHEN res.finish_position = 2     THEN 'place'
                   WHEN res.finish_position = 3     THEN 'show'
                   ELSE                                  'lose'
                 END AS prediction_outcome,
                 CASE
                   WHEN e.is_scratched = TRUE       THEN 0
                   WHEN res.finish_position IS NULL THEN NULL
                   WHEN res.finish_position = 1
                        AND res.win_payout IS NOT NULL
                                                    THEN res.win_payout - 2
                   WHEN res.finish_position = 1     THEN NULL
                   ELSE                                  -2
                 END AS flat_bet_pl
               FROM wr_predictions p
               JOIN entries e ON p.entry_id = e.entry_id
               JOIN races r ON p.race_id = r.race_id
               JOIN tracks t ON r.track_id = t.track_id
               LEFT JOIN results res ON res.entry_id = p.entry_id
               WHERE r.race_date >= CURRENT_DATE - %s::int
                 AND r.race_date <= CURRENT_DATE
                 AND p.longshot_alert = TRUE
                 AND p.style = 'general'""",
            (window_days,),
        )
        return aggregate_picks(
            [dict(r) for r in rows], window_days=window_days
        )

    def update_prediction_result(
        self,
        prediction_id: str,
        actual_finish: int,
        was_win: bool,
        actual_odds: Optional[float],
        bet_profit: Optional[float]
    ) -> None:
        """Fill in actual results after race completes."""
        self._write(
            """UPDATE ls_predictions SET
                 actual_finish = %s,
                 was_win = %s,
                 actual_odds = %s,
                 bet_profit = %s
               WHERE prediction_id = %s""",
            (actual_finish, was_win, actual_odds,
             bet_profit, prediction_id)
        )

    def _build_ls_prediction_list(
        self, rows: list[dict]
    ) -> list[LSPrediction]:
        """Build LSPrediction objects from joined rows."""
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
            predictions.append(LSPrediction(
                prediction_id=_to_str(
                    row.get('prediction_id')),
                entry=entry,
                race_id=_to_str(row.get('race_id')) or '',
                horse_id=_to_str(
                    row.get('horse_id')) or '',
                model_version_id=_to_str(
                    row.get('model_version_id')),
                final_win_probability=_to_float(
                    row.get('final_win_probability')),
                longshot_alert=_to_bool(
                    row.get('longshot_alert')),
                confidence=_to_str(row.get('confidence')),
                kelly_fraction=_to_float(
                    row.get('kelly_fraction')),
                predicted_rank=_to_int(
                    row.get('predicted_rank')),
                xgb_rank_score=_to_float(
                    row.get('xgb_rank_score')),
                rf_longshot_prob=_to_float(
                    row.get('rf_longshot_prob')),
                lstm_trajectory=_to_float(
                    row.get('lstm_trajectory')),
                calibrated_win_prob=_to_float(
                    row.get('calibrated_win_prob')),
                bayesian_angle_ev=_to_float(
                    row.get('bayesian_angle_ev')),
                angle_description=_to_str(
                    row.get('angle_description')),
                feature_importance=row.get(
                    'feature_importance') or {},
                actual_finish=_to_int(
                    row.get('actual_finish')),
                was_win=row.get('was_win'),
                actual_odds=_to_float(
                    row.get('actual_odds')),
                bet_profit=_to_float(
                    row.get('bet_profit')),
                created_at=row.get('created_at'),
                race_date=row.get('race_date'),
                race_number=_to_int(row.get('race_number')),
                track_code=_to_str(row.get('track_code')),
                post_time=row.get('post_time'),
                actual_finish_position=_to_int(
                    row.get('actual_finish_position')),
                actual_win_payout=_to_float(
                    row.get('actual_win_payout')),
                actual_place_payout=_to_float(
                    row.get('actual_place_payout')),
                actual_show_payout=_to_float(
                    row.get('actual_show_payout')),
                prediction_outcome=_to_str(
                    row.get('prediction_outcome')),
                flat_bet_pl=_to_float(row.get('flat_bet_pl')),
            ))
        return predictions
