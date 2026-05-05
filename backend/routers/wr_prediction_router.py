import json
import logging
from datetime import date
from shared.db import get_db
from repositories.wr_prediction_repository import (
    WRPredictionRepository
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
    GET /wr/predictions/today
    Returns all WR predictions for today.
    """
    try:
        with get_db() as conn:
            repo = WRPredictionRepository(conn)
            predictions = repo.get_todays_predictions()
            return _response(200, {
                'model': 'wr',
                'date': str(date.today()),
                'count': len(predictions),
                'predictions': [
                    _serialize_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(
            f"WR get_todays_predictions error: {e}"
        )
        return _response(500, {'error': str(e)})


def get_predictions_by_date(
    event: dict, context
) -> dict:
    """
    GET /wr/predictions/{date}
    """
    try:
        path_params = event.get('pathParameters') or {}
        date_str = path_params.get('date')
        race_date = date.fromisoformat(date_str)
        with get_db() as conn:
            repo = WRPredictionRepository(conn)
            predictions = repo.get_predictions_by_date(
                race_date
            )
            return _response(200, {
                'model': 'wr',
                'date': date_str,
                'count': len(predictions),
                'predictions': [
                    _serialize_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(
            f"WR get_predictions_by_date error: {e}"
        )
        return _response(500, {'error': str(e)})


def get_predictions_by_date_track_race(
    event: dict, context
) -> dict:
    """
    GET /wr/predictions/{date}/{track_code}/{race_number}
    Single-race scoped endpoint. Resolves date+track+race_number → race_id
    then delegates to get_predictions_by_race.
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
            repo = WRPredictionRepository(conn)
            predictions = repo.get_predictions_by_race(race_id, style=style)
            response = {
                'model': 'wr',
                'date': date_str,
                'track_code': track_code,
                'race_number': race_number,
                'race_id': race_id,
                'style': style,
                'count': len(predictions),
                'predictions': [
                    _serialize_prediction(p)
                    for p in predictions
                ]
            }
            # Annotate empty results from non-qualifying race types
            # (maidens, low-claiming) so SmartBoard can display
            # "no model picks available" with explanation.
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
            f"WR get_predictions_by_date_track_race error: {e}"
        )
        return _response(500, {'error': str(e)})


def get_value_plays(event: dict, context) -> dict:
    """
    GET /wr/predictions/value?date=YYYY-MM-DD
    Returns WR value-flagged predictions
    (model probability >> morning line).
    """
    try:
        params = event.get('queryStringParameters') or {}
        date_str = params.get('date', str(date.today()))
        race_date = date.fromisoformat(date_str)
        with get_db() as conn:
            repo = WRPredictionRepository(conn)
            predictions = repo.get_value_plays_by_date(
                race_date
            )
            return _response(200, {
                'model': 'wr',
                'date': date_str,
                'count': len(predictions),
                'value_plays': [
                    _serialize_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(f"WR get_value_plays error: {e}")
        return _response(500, {'error': str(e)})


def get_top_picks(event: dict, context) -> dict:
    """
    GET /wr/predictions/top-picks?date=YYYY-MM-DD
    Returns only top-ranked WR horse per race.
    """
    try:
        params = event.get('queryStringParameters') or {}
        date_str = params.get('date', str(date.today()))
        race_date = date.fromisoformat(date_str)
        with get_db() as conn:
            repo = WRPredictionRepository(conn)
            predictions = repo.get_top_picks_by_date(
                race_date
            )
            return _response(200, {
                'model': 'wr',
                'date': date_str,
                'count': len(predictions),
                'top_picks': [
                    _serialize_prediction(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(f"WR get_top_picks error: {e}")
        return _response(500, {'error': str(e)})


def get_track_record(event: dict, context) -> dict:
    """GET /wr/predictions/track-record?days=N
    Aggregate WR top-1 picks for the trailing window.
    days valid: 7|14|30|60|90 (default 30)."""
    from repositories.track_record import parse_window_days
    try:
        params = event.get('queryStringParameters') or {}
        days = parse_window_days(params.get('days'))
        with get_db() as conn:
            repo = WRPredictionRepository(conn)
            payload = repo.get_track_record(days)
        payload['model'] = 'wr'
        return _response(200, payload)
    except ValueError as e:
        return _response(400, {'error': str(e)})
    except Exception as e:
        logger.error(f"WR get_track_record error: {e}", exc_info=True)
        return _response(500, {'error': str(e)})


def get_track_record_by_style(event: dict, context) -> dict:
    """GET /wr/predictions/track-record-by-style?days=N
    Same headline payload + by_style breakdown across all 7 styles."""
    from repositories.track_record import parse_window_days
    try:
        params = event.get('queryStringParameters') or {}
        days = parse_window_days(params.get('days'))
        with get_db() as conn:
            repo = WRPredictionRepository(conn)
            payload = repo.get_track_record_by_style(days)
        payload['model'] = 'wr'
        return _response(200, payload)
    except ValueError as e:
        return _response(400, {'error': str(e)})
    except Exception as e:
        logger.error(f"WR get_track_record_by_style error: {e}", exc_info=True)
        return _response(500, {'error': str(e)})


def _serialize_prediction(p) -> dict:
    """
    Convert Prediction dataclass to JSON-safe dict.
    WR predictions are odds-blind — no closing_odds
    or kelly fields.
    """
    return {
        'prediction_id': p.prediction_id,
        'race_id': p.race_id,
        'race_number': p.race_number,
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
        ),
        'actual_finish': p.actual_finish,
        'was_win': p.was_win,
        'was_place': p.was_place,
        'was_show': p.was_show,
        'exacta_hit': p.exacta_hit,
        'trifecta_hit': p.trifecta_hit,
        # Layer 2-7 fields
        'rank_score': getattr(p, 'rank_score', None),
        'raw_win_prob': getattr(p, 'raw_win_prob', None),
        'edge_pct': getattr(p, 'edge_pct', None),
        'kelly_fraction': getattr(p, 'kelly_fraction', None),
        'kelly_bet': getattr(p, 'kelly_bet', None),
        'has_workout_data': getattr(p, 'has_workout_data', False),
        'model_used': getattr(p, 'model_used', 'core'),
        'ensemble_win_prob': getattr(p, 'ensemble_win_prob', None),
        'trajectory_score': getattr(p, 'trajectory_score', None),
        'longshot_prob': getattr(p, 'longshot_prob', None),
        'angle_name': getattr(p, 'angle_name', None),
        'longshot_alert': getattr(p, 'longshot_alert', False),
        'confidence': getattr(p, 'confidence', None),
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
    }


VALID_COMPARE_STYLES = (
    'speed', 'closer', 'class_riser',
    'class_dropper', 'sprint', 'route',
)


def get_compared_predictions_by_date(
    event: dict, context
) -> dict:
    """
    GET /wr/predictions/{date}/compare?style={specialist}
    Returns each entry joined to BOTH general and specialist predictions
    for both wr and pl. Frontend side-by-side compare view consumes this.
    """
    try:
        date_str = event.get('pathParameters', {}).get('date')
        if not date_str:
            return _response(400, {'error': 'date path param required'})
        try:
            target_date = date.fromisoformat(date_str)
        except ValueError:
            return _response(400, {'error': f'invalid date: {date_str!r}'})
        params = event.get('queryStringParameters') or {}
        compare_style = params.get('style', 'route')
        if compare_style not in VALID_COMPARE_STYLES:
            return _response(400, {
                'error': f'invalid style {compare_style!r}',
                'valid_styles': list(VALID_COMPARE_STYLES),
            })

        with get_db() as conn:
            repo = WRPredictionRepository(conn)
            rows = repo.get_compared_predictions_by_date(
                target_date, compare_style,
            )

        # Group flat rows into the {date, compare_style, races[...]} shape
        races_by_id: dict = {}
        for r in rows:
            rid = str(r['race_id'])
            if rid not in races_by_id:
                races_by_id[rid] = {
                    'race_id':     rid,
                    'race_number': r['race_number'],
                    'race_name':   r.get('race_name'),
                    'post_time':   (
                        str(r['post_time']) if r.get('post_time') else None
                    ),
                    'purse':       r.get('purse'),
                    'track_code':  r.get('track_code'),
                    'horses':      [],
                }
            races_by_id[rid]['horses'].append({
                'entry_id':           str(r['entry_id']),
                'horse_id':           str(r['horse_id']),
                'horse_name':         r.get('horse_name'),
                'program_number':     r.get('program_number'),
                'morning_line_odds':  (
                    float(r['morning_line_odds'])
                    if r.get('morning_line_odds') is not None else None
                ),
                'prediction_outcome': r.get('prediction_outcome'),
                'flat_bet_pl': (
                    float(r['flat_bet_pl'])
                    if r.get('flat_bet_pl') is not None else None
                ),
                'actual_finish_position': r.get('actual_finish_position'),
                'general': {
                    'wr': {
                        'predicted_rank':  r.get('wr_g_rank'),
                        'win_probability': (
                            float(r['wr_g_win_prob'])
                            if r.get('wr_g_win_prob') is not None else None
                        ),
                        'edge_pct': (
                            float(r['wr_g_edge'])
                            if r.get('wr_g_edge') is not None else None
                        ),
                        'kelly_fraction': (
                            float(r['wr_g_kelly'])
                            if r.get('wr_g_kelly') is not None else None
                        ),
                        'is_top_pick':   bool(r.get('wr_g_top') or False),
                        'is_value_flag': bool(r.get('wr_g_value') or False),
                    },
                    'pl': {
                        'win_probability': (
                            float(r['pl_g_win_prob'])
                            if r.get('pl_g_win_prob') is not None else None
                        ),
                        'edge_pct': (
                            float(r['pl_g_edge'])
                            if r.get('pl_g_edge') is not None else None
                        ),
                        'kelly_fraction': (
                            float(r['pl_g_kelly'])
                            if r.get('pl_g_kelly') is not None else None
                        ),
                        'is_value_bet': bool(r.get('pl_g_value') or False),
                    },
                },
                'specialist': {
                    'wr': {
                        'predicted_rank':  r.get('wr_s_rank'),
                        'win_probability': (
                            float(r['wr_s_win_prob'])
                            if r.get('wr_s_win_prob') is not None else None
                        ),
                        'edge_pct': (
                            float(r['wr_s_edge'])
                            if r.get('wr_s_edge') is not None else None
                        ),
                        'kelly_fraction': (
                            float(r['wr_s_kelly'])
                            if r.get('wr_s_kelly') is not None else None
                        ),
                        'is_top_pick':   bool(r.get('wr_s_top') or False),
                        'is_value_flag': bool(r.get('wr_s_value') or False),
                    },
                    'pl': {
                        'win_probability': (
                            float(r['pl_s_win_prob'])
                            if r.get('pl_s_win_prob') is not None else None
                        ),
                        'edge_pct': (
                            float(r['pl_s_edge'])
                            if r.get('pl_s_edge') is not None else None
                        ),
                        'kelly_fraction': (
                            float(r['pl_s_kelly'])
                            if r.get('pl_s_kelly') is not None else None
                        ),
                        'is_value_bet': bool(r.get('pl_s_value') or False),
                    },
                },
            })

        races = sorted(
            races_by_id.values(),
            key=lambda x: x['race_number'],
        )
        return _response(200, {
            'date':          str(target_date),
            'compare_style': compare_style,
            'races':         races,
        })
    except Exception as e:
        logger.error(f"compare endpoint failed: {e}", exc_info=True)
        return _response(500, {'error': str(e)})
