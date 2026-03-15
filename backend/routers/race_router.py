import json
import logging
from datetime import date, datetime
from shared.db import get_db

logger = logging.getLogger(__name__)


def _response(status_code: int, body: dict) -> dict:
    """Standard API Gateway response format."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, default=str)
    }


def get_todays_races(event: dict, context) -> dict:
    """
    GET /races/today
    Returns today's predictions from DB.
    Predictions were stored at 7:30 AM by
    the scheduled inference Lambda.
    This endpoint just reads from DB —
    it does NOT re-run inference.
    """
    try:
        from repositories.prediction_repository \
            import PredictionRepository
        from repositories.race_repository import (
            RaceRepository
        )
        with get_db() as conn:
            pred_repo = PredictionRepository(conn)
            predictions = (
                pred_repo.get_todays_predictions()
            )

            # Group by race_id for UI
            races = {}
            for pred in predictions:
                rid = pred.race_id
                if rid not in races:
                    races[rid] = {
                        'race_id': rid,
                        'predictions': []
                    }
                from routers.prediction_router import (
                    _serialize_prediction
                )
                races[rid]['predictions'].append(
                    _serialize_prediction(pred)
                )

            return _response(200, {
                'date': str(date.today()),
                'race_count': len(races),
                'races': list(races.values())
            })
    except Exception as e:
        logger.error(
            f"get_todays_races error: {e}"
        )
        return _response(500, {'error': str(e)})


def get_race_by_date(event: dict, context) -> dict:
    """
    GET /races/{date}
    Returns qualifying race predictions for
    a specific date. Date format: YYYY-MM-DD.
    """
    try:
        from repositories.prediction_repository \
            import PredictionRepository
        path_params = event.get('pathParameters') or {}
        date_str = path_params.get('date')
        race_date = date.fromisoformat(date_str)

        with get_db() as conn:
            pred_repo = PredictionRepository(conn)
            predictions = (
                pred_repo.get_predictions_by_date(race_date)
            )

            races = {}
            for pred in predictions:
                rid = pred.race_id
                if rid not in races:
                    races[rid] = {
                        'race_id': rid,
                        'predictions': []
                    }
                from routers.prediction_router import (
                    _serialize_prediction
                )
                races[rid]['predictions'].append(
                    _serialize_prediction(pred)
                )

            return _response(200, {
                'date': date_str,
                'race_count': len(races),
                'races': list(races.values())
            })
    except Exception as e:
        logger.error(
            f"get_race_by_date error: {e}"
        )
        return _response(500, {'error': str(e)})


def get_race_detail(event: dict, context) -> dict:
    """
    GET /races/{raceId}/detail
    Returns full race detail with all entries,
    predictions, and feature importance.
    """
    try:
        from repositories.prediction_repository \
            import PredictionRepository
        from repositories.race_repository import (
            RaceRepository
        )
        path_params = event.get('pathParameters') or {}
        race_id = path_params.get('raceId')

        with get_db() as conn:
            pred_repo = PredictionRepository(conn)
            predictions = (
                pred_repo.get_predictions_by_race(race_id)
            )

            from routers.prediction_router import (
                _serialize_prediction
            )
            return _response(200, {
                'race_id': race_id,
                'prediction_count': len(predictions),
                'predictions': [
                    _serialize_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(
            f"get_race_detail error: {e}"
        )
        return _response(500, {'error': str(e)})
