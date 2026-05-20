from typing import Optional
from datetime import date
from psycopg2.extras import Json
from .base_repository import BaseRepository
from .transforms import (
    transform_prediction, transform_entry,
    transform_horse, transform_trainer,
    transform_jockey
)
from models.canonical import Prediction


class WRPredictionRepository(BaseRepository):
    """
    Prediction repository for the WR (Win Rate) model.
    Targets wr_predictions table — identical schema
    to predictions, completely independent.
    """

    def get_predictions_by_race(
        self, race_id: str, style: str = 'general'
    ) -> list[Prediction]:
        """
        All WR predictions for a race ordered
        by predicted_rank ascending (best pick first).

        style: 'general' (default) | 'speed' | 'closer' | 'class_riser'
            | 'class_dropper' | 'sprint' | 'route' | 'gonzo_sauce'
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
                   WHEN res.finish_position = 1     THEN NULL  -- winner; payout data missing
                   ELSE                                  -2
                 END AS flat_bet_pl
               FROM wr_predictions p
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
        return self._build_prediction_list(rows)

    def get_predictions_by_date(
        self, race_date: date, style: str = 'general'
    ) -> list[Prediction]:
        """
        All WR predictions for a given date.
        Ordered by race post_time then predicted_rank.

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
                   WHEN res.finish_position = 1     THEN NULL  -- winner; payout data missing
                   ELSE                                  -2
                 END AS flat_bet_pl
               FROM wr_predictions p
               JOIN entries e ON p.entry_id = e.entry_id
               JOIN races r ON p.race_id = r.race_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               LEFT JOIN results res
                 ON res.entry_id = p.entry_id
               WHERE r.race_date = %s
                 AND p.style = %s
                 AND COALESCE(e.is_scratched, FALSE) = FALSE
               ORDER BY r.post_time ASC,
                        p.predicted_rank ASC""",
            (race_date, style)
        )
        return self._build_prediction_list(rows)

    def get_todays_predictions(
        self
    ) -> list[Prediction]:
        """WR predictions for today."""
        from datetime import date as date_type
        return self.get_predictions_by_date(
            date_type.today()
        )

    def get_top_picks_by_date(
        self, race_date: date
    ) -> list[Prediction]:
        """Only WR predictions where is_top_pick = true."""
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
                   WHEN res.finish_position = 1     THEN NULL  -- winner; payout data missing
                   ELSE                                  -2
                 END AS flat_bet_pl
               FROM wr_predictions p
               JOIN entries e ON p.entry_id = e.entry_id
               JOIN races r ON p.race_id = r.race_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               LEFT JOIN results res
                 ON res.entry_id = p.entry_id
               WHERE r.race_date = %s
                 AND p.is_top_pick = true
                 AND p.style = 'general'
                 AND COALESCE(e.is_scratched, FALSE) = FALSE
               ORDER BY r.post_time ASC""",
            (race_date,)
        )
        return self._build_prediction_list(rows)

    def get_value_plays_by_date(
        self, race_date: date
    ) -> list[Prediction]:
        """
        WR predictions flagged as value plays
        (model probability >> morning line).
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
                   WHEN res.finish_position = 1     THEN NULL  -- winner; payout data missing
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
                 AND p.is_value_flag = true
                 AND p.style = 'general'
                 AND COALESCE(e.is_scratched, FALSE) = FALSE
               ORDER BY p.overlay_pct DESC""",
            (race_date,)
        )
        return self._build_prediction_list(rows)

    def insert_prediction(
        self, prediction_data: dict
    ):
        """Insert WR prediction.

        Returns the new prediction_id (str) on a fresh insert. Returns
        None if the row already existed (ON CONFLICT DO NOTHING fires,
        RETURNING yields no row). Same bug class as the PL fix
        (commit 821eae2) — surfaced 2026-05-20 post-cutover when the
        new WR active model re-ran on 5/17 (a date that already had
        WR predictions stored). Caller `_store_prediction` doesn't use
        the return value in the daily pipeline.
        """
        row = self._write_returning(
            """INSERT INTO wr_predictions (
                 entry_id, race_id, horse_id,
                 model_version_id, style,
                 win_probability, place_probability,
                 show_probability, predicted_rank,
                 confidence_score, is_top_pick,
                 is_value_flag, morning_line_implied_prob,
                 overlay_pct, feature_importance,
                 recommended_bet_type, exotic_partners,
                 raw_win_prob, rank_score, edge_pct,
                 kelly_fraction, kelly_bet,
                 has_workout_data, model_used,
                 handicapping_prob, market_prob
               ) VALUES (
                 %s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s::uuid[],
                 %s,%s,%s,%s,%s,%s,%s,
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
                prediction_data.get('place_probability'),
                prediction_data.get('show_probability'),
                prediction_data.get('predicted_rank'),
                prediction_data.get('confidence_score'),
                prediction_data.get('is_top_pick', False),
                prediction_data.get('is_value_flag', False),
                prediction_data.get(
                    'morning_line_implied_prob'),
                prediction_data.get('overlay_pct'),
                Json(prediction_data.get(
                    'feature_importance') or {}),
                prediction_data.get('recommended_bet_type'),
                prediction_data.get('exotic_partners', []),
                prediction_data.get('raw_win_prob'),
                prediction_data.get('rank_score'),
                prediction_data.get('edge_pct'),
                prediction_data.get('kelly_fraction'),
                prediction_data.get('kelly_bet'),
                prediction_data.get('has_workout_data', False),
                prediction_data.get('model_used', 'core'),
                prediction_data.get('handicapping_prob'),
                prediction_data.get('market_prob'),
            )
        )
        # ON CONFLICT DO NOTHING + RETURNING → row=None when (race_id,
        # entry_id, style) already exists. Same fix as pl_prediction_
        # repository.py (commit 821eae2). Caller doesn't use the return
        # in the daily pipeline; silent no-op preserves existing row.
        if row is None:
            return None
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
        """Fill in actual results after race completes."""
        self._write(
            """UPDATE wr_predictions SET
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
        """Aggregate hit rates for a WR model version."""
        row = self._query_one(
            """SELECT
                 COUNT(*) as total_predictions,
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
               FROM wr_predictions
               WHERE model_version_id = %s
                 AND actual_finish IS NOT NULL""",
            (model_version_id,)
        )
        return dict(row) if row else {}

    def _build_prediction_list(
        self, rows: list[dict]
    ) -> list[Prediction]:
        """Build Prediction objects from joined rows."""
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


    def get_track_record(
        self, window_days: int, style: str = 'general'
    ) -> dict:
        """Aggregate WR top-1 picks for the trailing window_days.
        Returns dict per Stream E2 spec (n_predictions/wins/roi/by_track/etc).
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
                 AND p.predicted_rank = 1
                 AND p.style = %s""",
            (window_days, style),
        )
        return aggregate_picks(
            [dict(r) for r in rows], window_days=window_days
        )

    def get_track_record_by_style(
        self, window_days: int
    ) -> dict:
        """Aggregate WR top-1 picks across ALL 7 styles. Includes a
        by_style breakdown in the response."""
        from .track_record import aggregate_picks
        rows = self._query(
            """SELECT
                 r.race_date,
                 t.track_code,
                 p.style,
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
                 AND p.predicted_rank = 1""",
            (window_days,),
        )
        return aggregate_picks(
            [dict(r) for r in rows], window_days=window_days,
            extra_dim='style',
        )

    def get_compared_predictions_by_date(
        self, race_date, compare_style: str
    ) -> list[dict]:
        """Compare-view rows: each entry joined to BOTH wr+pl general
        and wr+pl specialist predictions. Used by the frontend
        side-by-side compare endpoint. Returns flat dicts."""
        rows = self._query(
            """SELECT
                 e.entry_id,
                 e.horse_id,
                 e.program_number,
                 e.morning_line_odds,
                 e.is_scratched,
                 h.horse_name,
                 r.race_id,
                 r.race_number,
                 r.race_name,
                 r.post_time,
                 r.purse,
                 t.track_code,

                 wr_g.predicted_rank   AS wr_g_rank,
                 wr_g.win_probability  AS wr_g_win_prob,
                 wr_g.edge_pct         AS wr_g_edge,
                 wr_g.kelly_fraction   AS wr_g_kelly,
                 wr_g.is_top_pick      AS wr_g_top,
                 wr_g.is_value_flag    AS wr_g_value,

                 wr_s.predicted_rank   AS wr_s_rank,
                 wr_s.win_probability  AS wr_s_win_prob,
                 wr_s.edge_pct         AS wr_s_edge,
                 wr_s.kelly_fraction   AS wr_s_kelly,
                 wr_s.is_top_pick      AS wr_s_top,
                 wr_s.is_value_flag    AS wr_s_value,

                 pl_g.win_probability  AS pl_g_win_prob,
                 pl_g.edge_pct         AS pl_g_edge,
                 pl_g.kelly_fraction   AS pl_g_kelly,
                 pl_g.is_value_bet     AS pl_g_value,

                 pl_s.win_probability  AS pl_s_win_prob,
                 pl_s.edge_pct         AS pl_s_edge,
                 pl_s.kelly_fraction   AS pl_s_kelly,
                 pl_s.is_value_bet     AS pl_s_value,

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
                   WHEN res.finish_position = 1     THEN NULL  -- winner; payout data missing
                   ELSE                                  -2
                 END AS flat_bet_pl
               FROM entries e
               JOIN races  r ON r.race_id = e.race_id
               JOIN tracks t ON t.track_id = r.track_id
               JOIN horses h ON h.horse_id = e.horse_id
               LEFT JOIN wr_predictions wr_g
                 ON wr_g.entry_id = e.entry_id
                AND wr_g.style = 'general'
               LEFT JOIN wr_predictions wr_s
                 ON wr_s.entry_id = e.entry_id
                AND wr_s.style = %s
               LEFT JOIN pl_predictions pl_g
                 ON pl_g.entry_id = e.entry_id
                AND pl_g.style = 'general'
               LEFT JOIN pl_predictions pl_s
                 ON pl_s.entry_id = e.entry_id
                AND pl_s.style = %s
               LEFT JOIN results res
                 ON res.entry_id = e.entry_id
               WHERE r.race_date = %s
                 AND COALESCE(e.is_scratched, FALSE) = FALSE
               ORDER BY r.race_number ASC,
                        wr_g.predicted_rank ASC NULLS LAST""",
            (compare_style, compare_style, race_date),
        )
        return [dict(r) for r in rows]
