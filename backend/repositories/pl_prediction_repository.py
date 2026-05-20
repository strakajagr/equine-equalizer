from typing import Optional
from datetime import date
from psycopg2.extras import Json
from .base_repository import BaseRepository
from .transforms import (
    transform_entry, transform_horse,
    transform_trainer, transform_jockey
)
from models.canonical import PLPrediction, Entry


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


class PLPredictionRepository(BaseRepository):
    """
    Prediction repository for the P&L (Profit & Loss)
    model. Targets pl_predictions table — independent
    schema with EV, Kelly sizing, edge columns.
    """

    def get_predictions_by_race(
        self, race_id: str, style: str = 'general'
    ) -> list[PLPrediction]:
        """
        All P&L predictions for a race ordered
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
               FROM pl_predictions p
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
        return self._build_pl_prediction_list(rows)

    def get_predictions_by_date(
        self, race_date: date
    ) -> list[PLPrediction]:
        """All P&L predictions for a given date."""
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
               FROM pl_predictions p
               JOIN entries e ON p.entry_id = e.entry_id
               JOIN races r ON p.race_id = r.race_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               LEFT JOIN results res
                 ON res.entry_id = p.entry_id
               WHERE r.race_date = %s
                 AND p.style = 'general'
                 AND COALESCE(e.is_scratched, FALSE) = FALSE
               ORDER BY r.post_time ASC,
                        p.predicted_rank ASC""",
            (race_date,)
        )
        return self._build_pl_prediction_list(rows)

    def get_todays_predictions(
        self
    ) -> list[PLPrediction]:
        """P&L predictions for today."""
        from datetime import date as date_type
        return self.get_predictions_by_date(
            date_type.today()
        )

    def get_value_bets_by_date(
        self, race_date: date
    ) -> list[PLPrediction]:
        """
        P&L predictions where is_value_bet = true.
        Ordered by edge_pct descending (best edge first).
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
               FROM pl_predictions p
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
                 AND p.is_value_bet = true
                 AND p.style = 'general'
                 AND COALESCE(e.is_scratched, FALSE) = FALSE
               ORDER BY p.edge_pct DESC""",
            (race_date,)
        )
        return self._build_pl_prediction_list(rows)

    def insert_prediction(
        self, prediction_data: dict
    ):
        """Insert P&L prediction.

        Returns the new prediction_id (str) on a fresh insert. Returns
        None if the row already existed (ON CONFLICT DO NOTHING fires,
        RETURNING yields no row). The PL daily pipeline doesn't use the
        return value, but earlier code would crash here with
        `TypeError: 'NoneType' object is not subscriptable` on every
        race re-run (manual smoke test, backfill of a date that already
        has predictions) — surfaced 2026-05-20 on a 5/17 backfill smoke.
        """
        row = self._write_returning(
            """INSERT INTO pl_predictions (
                 entry_id, race_id, horse_id,
                 model_version_id, style,
                 win_probability, predicted_ev,
                 confidence_score, predicted_rank,
                 is_top_pick,
                 closing_odds, implied_probability,
                 edge_pct, is_value_bet, is_strong_value,
                 kelly_fraction, kelly_bet_size,
                 feature_importance,
                 handicapping_prob, market_prob
               ) VALUES (
                 %s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s
               )
               -- REPAIR-4: DO NOTHING substrate-protects clean writes
               ON CONFLICT (race_id, entry_id, style) DO NOTHING
               RETURNING prediction_id""",
            (
                prediction_data['entry_id'],
                prediction_data['race_id'],
                prediction_data['horse_id'],
                prediction_data.get('model_version_id'),
                prediction_data.get('style', 'general'),
                prediction_data.get('win_probability'),
                prediction_data.get('predicted_ev'),
                prediction_data.get('confidence_score'),
                prediction_data.get('predicted_rank'),
                prediction_data.get('is_top_pick', False),
                prediction_data.get('closing_odds'),
                prediction_data.get('implied_probability'),
                prediction_data.get('edge_pct'),
                prediction_data.get('is_value_bet', False),
                prediction_data.get(
                    'is_strong_value', False),
                prediction_data.get('kelly_fraction'),
                prediction_data.get('kelly_bet_size'),
                Json(prediction_data.get(
                    'feature_importance') or {}),
                prediction_data.get('handicapping_prob'),
                prediction_data.get('market_prob'),
            )
        )
        # ON CONFLICT DO NOTHING + RETURNING produces no row when the
        # (race_id, entry_id, style) tuple already exists. Treat as a
        # silent no-op (existing prediction stays). Caller doesn't use
        # the return value in the daily pipeline.
        if row is None:
            return None
        return str(row['prediction_id'])

    def get_track_record(self, window_days: int) -> dict:
        """Aggregate PL top-1 picks for the trailing window_days. Stream E2."""
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
               FROM pl_predictions p
               JOIN entries e ON p.entry_id = e.entry_id
               JOIN races r ON p.race_id = r.race_id
               JOIN tracks t ON r.track_id = t.track_id
               LEFT JOIN results res ON res.entry_id = p.entry_id
               WHERE r.race_date >= CURRENT_DATE - %s::int
                 AND r.race_date <= CURRENT_DATE
                 AND p.predicted_rank = 1
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
        bet_profit: Optional[float]
    ) -> None:
        """Fill in actual results after race completes."""
        self._write(
            """UPDATE pl_predictions SET
                 actual_finish = %s,
                 was_win = %s,
                 bet_profit = %s
               WHERE prediction_id = %s""",
            (actual_finish, was_win, bet_profit,
             prediction_id)
        )

    def _build_pl_prediction_list(
        self, rows: list[dict]
    ) -> list[PLPrediction]:
        """Build PLPrediction objects from joined rows."""
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
            predictions.append(PLPrediction(
                prediction_id=_to_str(
                    row.get('prediction_id')),
                entry=entry,
                race_id=_to_str(row.get('race_id')) or '',
                race_number=_to_int(row.get('race_number')),
                horse_id=_to_str(
                    row.get('horse_id')) or '',
                model_version_id=_to_str(
                    row.get('model_version_id')),
                win_probability=_to_float(
                    row.get('win_probability')),
                predicted_ev=_to_float(
                    row.get('predicted_ev')),
                confidence_score=_to_float(
                    row.get('confidence_score')),
                predicted_rank=_to_int(
                    row.get('predicted_rank')),
                is_top_pick=_to_bool(
                    row.get('is_top_pick')),
                closing_odds=_to_float(
                    row.get('closing_odds')),
                implied_probability=_to_float(
                    row.get('implied_probability')),
                edge_pct=_to_float(row.get('edge_pct')),
                is_value_bet=_to_bool(
                    row.get('is_value_bet')),
                is_strong_value=_to_bool(
                    row.get('is_strong_value')),
                kelly_fraction=_to_float(
                    row.get('kelly_fraction')),
                kelly_bet_size=_to_float(
                    row.get('kelly_bet_size')),
                feature_importance=row.get(
                    'feature_importance') or {},
                actual_finish=_to_int(
                    row.get('actual_finish')),
                was_win=row.get('was_win'),
                bet_profit=_to_float(
                    row.get('bet_profit')),
                created_at=row.get('created_at'),
                handicapping_prob=_to_float(
                    row.get('handicapping_prob')),
                market_prob=_to_float(row.get('market_prob')),
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
                track_code=_to_str(row.get('track_code')),
                track_name=_to_str(row.get('track_name')),
            ))
        return predictions
