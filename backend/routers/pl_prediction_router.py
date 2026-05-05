import json
import logging
from datetime import date
from shared.db import get_db
from repositories.pl_prediction_repository import (
    PLPredictionRepository
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
    GET /pl/predictions/today
    Returns all P&L predictions for today.
    """
    try:
        with get_db() as conn:
            repo = PLPredictionRepository(conn)
            predictions = repo.get_todays_predictions()
            return _response(200, {
                'model': 'pl',
                'date': str(date.today()),
                'count': len(predictions),
                'predictions': [
                    _serialize_pl_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(
            f"PL get_todays_predictions error: {e}"
        )
        return _response(500, {'error': str(e)})


def get_predictions_by_date(
    event: dict, context
) -> dict:
    """
    GET /pl/predictions/{date}
    """
    try:
        path_params = event.get('pathParameters') or {}
        date_str = path_params.get('date')
        race_date = date.fromisoformat(date_str)
        with get_db() as conn:
            repo = PLPredictionRepository(conn)
            predictions = repo.get_predictions_by_date(
                race_date
            )
            return _response(200, {
                'model': 'pl',
                'date': date_str,
                'count': len(predictions),
                'predictions': [
                    _serialize_pl_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(
            f"PL get_predictions_by_date error: {e}"
        )
        return _response(500, {'error': str(e)})


def get_predictions_by_date_track_race(
    event: dict, context
) -> dict:
    """
    GET /pl/predictions/{date}/{track_code}/{race_number}
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
            repo = PLPredictionRepository(conn)
            predictions = repo.get_predictions_by_race(race_id, style=style)
            response = {
                'model': 'pl',
                'date': date_str,
                'track_code': track_code,
                'race_number': race_number,
                'race_id': race_id,
                'style': style,
                'count': len(predictions),
                'predictions': [
                    _serialize_pl_prediction(p)
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
            f"PL get_predictions_by_date_track_race error: {e}"
        )
        return _response(500, {'error': str(e)})


def get_value_bets(event: dict, context) -> dict:
    """
    GET /pl/predictions/value-bets?date=YYYY-MM-DD
    Returns P&L value bets (edge >= MIN_EDGE_TO_BET).
    Ordered by edge_pct descending.
    """
    try:
        params = event.get('queryStringParameters') or {}
        date_str = params.get('date', str(date.today()))
        race_date = date.fromisoformat(date_str)
        with get_db() as conn:
            repo = PLPredictionRepository(conn)
            predictions = repo.get_value_bets_by_date(
                race_date
            )
            return _response(200, {
                'model': 'pl',
                'date': date_str,
                'count': len(predictions),
                'value_bets': [
                    _serialize_pl_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(f"PL get_value_bets error: {e}")
        return _response(500, {'error': str(e)})


def get_strong_value_bets(
    event: dict, context
) -> dict:
    """
    GET /pl/predictions/strong-value?date=YYYY-MM-DD
    Returns P&L strong value bets (is_strong_value=true).
    Filtered in-memory from value_bets_by_date.
    """
    try:
        params = event.get('queryStringParameters') or {}
        date_str = params.get('date', str(date.today()))
        race_date = date.fromisoformat(date_str)
        with get_db() as conn:
            repo = PLPredictionRepository(conn)
            all_value = repo.get_value_bets_by_date(
                race_date
            )
            strong = [
                p for p in all_value
                if p.is_strong_value
            ]
            return _response(200, {
                'model': 'pl',
                'date': date_str,
                'count': len(strong),
                'strong_value_bets': [
                    _serialize_pl_prediction(p)
                    for p in strong
                ]
            })
    except Exception as e:
        logger.error(
            f"PL get_strong_value_bets error: {e}"
        )
        return _response(500, {'error': str(e)})


def _serialize_pl_prediction(p) -> dict:
    """
    Convert PLPrediction dataclass to JSON-safe dict.
    Includes all P&L-specific fields: ev, edge, Kelly.
    """
    return {
        'prediction_id': p.prediction_id,
        'race_id': p.race_id,
        'race_number': p.race_number,
        'horse_name': p.entry.horse.horse_name,
        'post_position': p.entry.post_position,
        'program_number': p.entry.program_number,
        'win_probability': p.win_probability,
        'predicted_ev': p.predicted_ev,
        'confidence_score': p.confidence_score,
        'predicted_rank': p.predicted_rank,
        'is_top_pick': p.is_top_pick,
        'closing_odds': p.closing_odds,
        'morning_line_odds': p.entry.morning_line_odds,
        'implied_probability': p.implied_probability,
        'edge_pct': p.edge_pct,
        'is_value_bet': p.is_value_bet,
        'is_strong_value': p.is_strong_value,
        'kelly_fraction': p.kelly_fraction,
        'kelly_bet_size': p.kelly_bet_size,
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
        ),
        'actual_finish': p.actual_finish,
        'was_win': p.was_win,
        'bet_profit': p.bet_profit,
        # Stream A2 dual-prediction
        'handicapping_prob': getattr(p, 'handicapping_prob', None),
        'market_prob': getattr(p, 'market_prob', None),
        # Stream E results-aware fields
        'actual_finish_position': getattr(p, 'actual_finish_position', None),
        'actual_win_payout':   getattr(p, 'actual_win_payout', None),
        'actual_place_payout': getattr(p, 'actual_place_payout', None),
        'actual_show_payout':  getattr(p, 'actual_show_payout', None),
        'prediction_outcome':  getattr(p, 'prediction_outcome', None),
        'flat_bet_pl':         getattr(p, 'flat_bet_pl', None),
        'track_code':          getattr(p, 'track_code', None),
        'track_name':          getattr(p, 'track_name', None),
    }


def get_track_record(event: dict, context) -> dict:
    """GET /pl/predictions/track-record?days=N
    Aggregate PL top-1 picks for the trailing window.
    days valid: 7|14|30|60|90 (default 30)."""
    from repositories.track_record import parse_window_days
    try:
        params = event.get('queryStringParameters') or {}
        days = parse_window_days(params.get('days'))
        with get_db() as conn:
            repo = PLPredictionRepository(conn)
            payload = repo.get_track_record(days)
        payload['model'] = 'pl'
        return _response(200, payload)
    except ValueError as e:
        return _response(400, {'error': str(e)})
    except Exception as e:
        logger.error(f"PL get_track_record error: {e}", exc_info=True)
        return _response(500, {'error': str(e)})
