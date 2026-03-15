import json
import logging
from datetime import date
from shared.db import get_db
from repositories.prediction_repository import (
    PredictionRepository
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
    GET /predictions/today
    Returns all predictions for today
    ordered by post time then predicted rank.
    Pure passthrough to prediction_repository.
    """
    try:
        with get_db() as conn:
            repo = PredictionRepository(conn)
            predictions = repo.get_todays_predictions()
            return _response(200, {
                'date': str(date.today()),
                'count': len(predictions),
                'predictions': [
                    _serialize_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(f"get_todays_predictions error: {e}")
        return _response(500, {'error': str(e)})


def get_predictions_by_date(
    event: dict, context
) -> dict:
    """
    GET /predictions/{date}
    Pure passthrough to prediction_repository.
    """
    try:
        path_params = event.get('pathParameters') or {}
        date_str = path_params.get('date')
        race_date = date.fromisoformat(date_str)
        with get_db() as conn:
            repo = PredictionRepository(conn)
            predictions = repo.get_predictions_by_date(
                race_date
            )
            return _response(200, {
                'date': date_str,
                'count': len(predictions),
                'predictions': [
                    _serialize_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(
            f"get_predictions_by_date error: {e}"
        )
        return _response(500, {'error': str(e)})


def get_value_plays(event: dict, context) -> dict:
    """
    GET /predictions/value?date=YYYY-MM-DD
    Returns only value-flagged predictions
    (overlays where model >> morning line).
    Pure passthrough.
    """
    try:
        params = event.get('queryStringParameters') or {}
        date_str = params.get('date', str(date.today()))
        race_date = date.fromisoformat(date_str)
        with get_db() as conn:
            repo = PredictionRepository(conn)
            predictions = repo.get_value_plays_by_date(
                race_date
            )
            return _response(200, {
                'date': date_str,
                'count': len(predictions),
                'value_plays': [
                    _serialize_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(f"get_value_plays error: {e}")
        return _response(500, {'error': str(e)})


def _serialize_prediction(p) -> dict:
    """
    Convert Prediction dataclass to JSON-safe dict.
    This is the ONE transform allowed in routers —
    dataclass to wire format. No logic.
    """
    return {
        'prediction_id': p.prediction_id,
        'horse_name': p.entry.horse.horse_name,
        'post_position': p.entry.post_position,
        'program_number': p.entry.program_number,
        'win_probability': p.win_probability,
        'place_probability': p.place_probability,
        'show_probability': p.show_probability,
        'predicted_rank': p.predicted_rank,
        'confidence_score': p.confidence_score,
        'is_top_pick': p.is_top_pick,
        'is_value_flag': p.is_value_flag,
        'overlay_pct': p.overlay_pct,
        'morning_line_odds': p.entry.morning_line_odds,
        'recommended_bet_type': p.recommended_bet_type,
        'exotic_partners': p.exotic_partners,
        'feature_importance': p.feature_importance,
        'trainer_name': p.entry.trainer.trainer_name,
        'jockey_name': (
            p.entry.jockey.jockey_name
            if p.entry.jockey else None
        ),
        'lasix_first_time': p.entry.lasix_first_time,
        'blinkers_first_time': p.entry.blinkers_first_time,
        'equipment_change': (
            p.entry.equipment_change_from_last
        )
    }
