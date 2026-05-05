import json
import logging
from datetime import date
from shared.db import get_db
from repositories.ls_prediction_repository import (
    LSPredictionRepository
)

logger = logging.getLogger(__name__)


def _response(status_code: int, body: dict) -> dict:
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, default=str)
    }


def get_todays_predictions(
    event: dict, context
) -> dict:
    """
    GET /ls/predictions/today
    Returns all LS predictions for today.
    Will return empty list until LS model is trained.
    """
    try:
        with get_db() as conn:
            repo = LSPredictionRepository(conn)
            predictions = repo.get_todays_predictions()
            return _response(200, {
                'model': 'ls',
                'date': str(date.today()),
                'count': len(predictions),
                'predictions': [
                    _serialize_ls_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(
            f"LS get_todays_predictions error: {e}"
        )
        return _response(500, {'error': str(e)})


def get_predictions_by_date(
    event: dict, context
) -> dict:
    """
    GET /ls/predictions/{date}
    """
    try:
        path_params = event.get('pathParameters') or {}
        date_str = path_params.get('date')
        race_date = date.fromisoformat(date_str)
        with get_db() as conn:
            repo = LSPredictionRepository(conn)
            predictions = repo.get_predictions_by_date(
                race_date
            )
            return _response(200, {
                'model': 'ls',
                'date': date_str,
                'count': len(predictions),
                'predictions': [
                    _serialize_ls_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(
            f"LS get_predictions_by_date error: {e}"
        )
        return _response(500, {'error': str(e)})


def get_predictions_by_date_track_race(
    event: dict, context
) -> dict:
    """
    GET /ls/predictions/{date}/{track_code}/{race_number}
    Single-race scoped endpoint.
    """
    try:
        pp = event.get('pathParameters') or {}
        qs = event.get('queryStringParameters') or {}
        date_str = pp.get('date')
        track_code = pp.get('track_code')
        race_number = int(pp.get('race_number'))
        style = qs.get('style', 'general')
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
              SELECT r.race_id, r.race_type, r.claiming_price
              FROM races r
              JOIN tracks t ON t.track_id = r.track_id
              WHERE r.race_date = %s
                AND t.track_code = %s
                AND r.race_number = %s
            """, (date_str, track_code, race_number))
            row = cur.fetchone()
            if not row:
                return _response(404, {
                    'error': f'race not found: {date_str} {track_code} R{race_number}'
                })
            race_id = row['race_id']
            repo = LSPredictionRepository(conn)
            predictions = repo.get_predictions_by_race(race_id, style=style)
            response = {
                'model': 'ls',
                'date': date_str,
                'track_code': track_code,
                'race_number': race_number,
                'race_id': race_id,
                'style': style,
                'count': len(predictions),
                'predictions': [
                    _serialize_ls_prediction(p)
                    for p in predictions
                ]
            }
            if not predictions:
                from shared.constants import (
                    is_qualifying_race_type
                )
                if not is_qualifying_race_type(
                    row['race_type'], row['claiming_price']
                ):
                    response['predictions_skipped_reason'] = (
                        'non_qualifying_race_type'
                    )
            return _response(200, response)
    except Exception as e:
        logger.error(
            f"LS get_predictions_by_date_track_race error: {e}"
        )
        return _response(500, {'error': str(e)})


def get_longshot_alerts(event: dict, context) -> dict:
    """
    GET /ls/predictions/longshots?date=YYYY-MM-DD
    Returns LS longshot alerts (longshot_alert=true).
    These are high-odds horses the meta-model
    believes are undervalued by the market.
    """
    try:
        params = event.get('queryStringParameters') or {}
        date_str = params.get('date', str(date.today()))
        race_date = date.fromisoformat(date_str)
        with get_db() as conn:
            repo = LSPredictionRepository(conn)
            predictions = repo.get_longshot_alerts_by_date(
                race_date
            )
            return _response(200, {
                'model': 'ls',
                'date': date_str,
                'count': len(predictions),
                'longshot_alerts': [
                    _serialize_ls_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(
            f"LS get_longshot_alerts error: {e}"
        )
        return _response(500, {'error': str(e)})


def _serialize_ls_prediction(p) -> dict:
    """
    Convert LSPrediction dataclass to JSON-safe dict.
    Includes all LS-specific fields: ensemble base model
    scores, longshot_alert, angle_description.
    """
    return {
        'prediction_id': p.prediction_id,
        'race_id': p.race_id,
        'race_number': p.race_number,
        'horse_name': p.entry.horse.horse_name,
        'post_position': p.entry.post_position,
        'program_number': p.entry.program_number,
        'final_win_probability': p.final_win_probability,
        'longshot_alert': p.longshot_alert,
        'confidence': p.confidence,
        'kelly_fraction': p.kelly_fraction,
        'predicted_rank': p.predicted_rank,
        'xgb_rank_score': p.xgb_rank_score,
        'rf_longshot_prob': p.rf_longshot_prob,
        'lstm_trajectory': p.lstm_trajectory,
        'calibrated_win_prob': p.calibrated_win_prob,
        'bayesian_angle_ev': p.bayesian_angle_ev,
        'angle_description': p.angle_description,
        'feature_importance': p.feature_importance,
        'morning_line_odds': p.entry.morning_line_odds,
        'trainer_name': p.entry.trainer.trainer_name,
        'jockey_name': (
            p.entry.jockey.jockey_name
            if p.entry.jockey else None
        ),
        'lasix_first_time': p.entry.lasix_first_time,
        'blinkers_first_time': p.entry.blinkers_first_time,
        'actual_finish': p.actual_finish,
        'was_win': p.was_win,
        'actual_odds': p.actual_odds,
        'bet_profit': p.bet_profit,
        # Race context for the longshot card UI
        'race_date':   str(p.race_date) if p.race_date else None,
        'race_number': p.race_number,
        'track_code':  p.track_code,
        'post_time':   str(p.post_time) if p.post_time else None,
        # Stream E results-aware fields
        'actual_finish_position': getattr(p, 'actual_finish_position', None),
        'actual_win_payout':   getattr(p, 'actual_win_payout', None),
        'actual_place_payout': getattr(p, 'actual_place_payout', None),
        'actual_show_payout':  getattr(p, 'actual_show_payout', None),
        'prediction_outcome':  getattr(p, 'prediction_outcome', None),
        'flat_bet_pl':         getattr(p, 'flat_bet_pl', None),
    }


def get_track_record(event: dict, context) -> dict:
    """GET /ls/predictions/track-record?days=N
    Aggregate LS longshot-alert rows for the trailing window.
    days valid: 7|14|30|60|90 (default 30)."""
    from repositories.track_record import parse_window_days
    try:
        params = event.get('queryStringParameters') or {}
        days = parse_window_days(params.get('days'))
        with get_db() as conn:
            repo = LSPredictionRepository(conn)
            payload = repo.get_track_record(days)
        payload['model'] = 'ls'
        return _response(200, payload)
    except ValueError as e:
        return _response(400, {'error': str(e)})
    except Exception as e:
        logger.error(f"LS get_track_record error: {e}", exc_info=True)
        return _response(500, {'error': str(e)})
