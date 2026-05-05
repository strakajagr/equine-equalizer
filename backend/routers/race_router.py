import json
import logging
from datetime import date, datetime
from shared.db import get_db, execute_query

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


# Feature name → human-readable label mapping
FEATURE_LABELS = {
    'jockey_win_rate': 'Jockey win rate',
    'win_rate_this_track': 'Win rate at this track',
    'trainer_win_rate': 'Trainer win rate',
    'layoff_bucket': 'Layoff pattern',
    'lasix_first_time': '1st time Lasix',
    'blinkers_first_time': '1st time blinkers',
    'running_style_numeric': 'Running style',
    'raw_speed_sample_size': 'Speed data depth',
    'avg_stretch_gain': 'Late closing ability',
    'raw_speed_trend': 'Speed trending up',
    'claiming_price_change_pct': 'Class change',
    'raw_speed_vs_par': 'Speed vs par',
    'career_class_ceiling': 'Class ceiling',
    'current_vs_ceiling_pct': 'Current vs peak',
    'jockey_change_flag': 'Jockey switch',
    'avg_call1_position': 'Early position',
    'raw_speed_avg_3': 'Avg speed (last 3)',
    'beyer_vs_raw_discrepancy': 'Beyer vs raw gap',
    'days_since_last_race': 'Days since last',
    'pace_sample_size': 'Pace data depth',
    'career_starts': 'Experience level',
    'style_scenario_match': 'Pace scenario fit',
    'purse_change_pct': 'Purse change',
    'first_time_on_surface': '1st on surface',
    'raw_speed_last': 'Last race speed',
    'overall_win_rate': 'Career win rate',
    'trainer_intent_score': 'Trainer intent',
    'beyer_last': 'Last Beyer',
    'beyer_avg_3': 'Avg Beyer (last 3)',
    'beyer_trend': 'Beyer trending',
}


def _get_top_feature(feature_importance: dict) -> str:
    """
    Return human-readable string for the top feature
    driving a horse's model score.
    e.g. "Jockey 34% win rate here"
    """
    if not feature_importance:
        return None
    # Get the feature with highest absolute importance
    top = max(
        feature_importance.items(),
        key=lambda x: abs(x[1]) if x[1] else 0
    )
    name, value = top
    label = FEATURE_LABELS.get(name, name.replace('_', ' ').title())
    if value and abs(value) > 0.01:
        direction = '\u2191' if value > 0 else '\u2193'
        return f"{direction} {label}"
    return label


def _serialize_prediction_with_race(pred, race_info=None):
    """
    Convert Prediction to JSON dict with race metadata
    and top feature explanation.
    """
    fi = pred.feature_importance or {}
    return {
        'prediction_id': pred.prediction_id,
        'race_id': pred.race_id,
        'horse_id': pred.horse_id,
        'horse_name': pred.entry.horse.horse_name,
        'post_position': pred.entry.post_position,
        'program_number': pred.entry.program_number,
        'win_probability': pred.win_probability,
        'place_probability': pred.place_probability,
        'show_probability': pred.show_probability,
        'predicted_rank': pred.predicted_rank,
        'confidence_score': pred.confidence_score,
        'is_top_pick': pred.is_top_pick,
        'is_value_flag': pred.is_value_flag,
        'overlay_pct': pred.overlay_pct,
        'morning_line_odds': pred.entry.morning_line_odds,
        'recommended_bet_type': pred.recommended_bet_type,
        'exotic_partners': pred.exotic_partners,
        'feature_importance': fi,
        'top_feature': _get_top_feature(fi),
        'trainer_name': pred.entry.trainer.trainer_name,
        'jockey_name': (
            pred.entry.jockey.jockey_name
            if pred.entry.jockey else None
        ),
        'lasix_first_time': pred.entry.lasix_first_time,
        'blinkers_first_time': pred.entry.blinkers_first_time,
        'equipment_change': (
            pred.entry.equipment_change_from_last
        ),
        'weight_carried': pred.entry.weight_carried,
        'sex': pred.entry.horse.sex,
        'sire': pred.entry.horse.sire,
        'actual_finish': pred.actual_finish,
        'was_win': pred.was_win,
        'was_place': pred.was_place,
        'was_show': pred.was_show,
        'exacta_hit': pred.exacta_hit,
        'trifecta_hit': pred.trifecta_hit,
        'rank_score': getattr(pred, 'rank_score', None),
        'edge_pct': getattr(pred, 'edge_pct', None),
        'kelly_bet': getattr(pred, 'kelly_bet', None),
        'has_workout_data': getattr(pred, 'has_workout_data', False),
        'model_used': getattr(pred, 'model_used', 'core'),
        'ensemble_win_prob': getattr(pred, 'ensemble_win_prob', None),
        'trajectory_score': getattr(pred, 'trajectory_score', None),
        'longshot_alert': getattr(pred, 'longshot_alert', False),
        'confidence': getattr(pred, 'confidence', None),
        'angle_name': getattr(pred, 'angle_name', None),
    }


def _get_races_with_predictions(conn, race_date, style: str = 'general'):
    """
    Get races grouped by track with full race metadata
    and predictions for each race.

    style: 'general' (default) | 'gonzo_sauce' | other gallery styles
    """
    from repositories.wr_prediction_repository \
        import WRPredictionRepository
    pred_repo = WRPredictionRepository(conn)
    predictions = pred_repo.get_predictions_by_date(race_date, style=style)

    if not predictions:
        return [], {}

    # Get race metadata for all races on this date
    race_rows = execute_query(
        conn,
        """SELECT
             r.race_id, r.race_number, r.race_date,
             r.distance_furlongs, r.surface, r.race_type,
             r.purse, r.claiming_price, r.conditions,
             r.post_time, r.field_size, r.race_name,
             r.track_condition, r.grade,
             t.track_code, t.track_name
           FROM races r
           JOIN tracks t ON r.track_id = t.track_id
           WHERE r.race_date = %s
           ORDER BY t.track_code, r.race_number""",
        (race_date,)
    )
    race_meta = {r['race_id']: dict(r) for r in race_rows}

    # Group predictions by race, enriched with race metadata
    races = {}
    tracks = {}
    for pred in predictions:
        rid = pred.race_id
        if rid not in races:
            meta = race_meta.get(rid, {})
            track_code = meta.get('track_code', 'UNK')
            races[rid] = {
                'race_id': rid,
                'race_number': meta.get('race_number'),
                'distance_furlongs': meta.get('distance_furlongs'),
                'surface': meta.get('surface'),
                'race_type': meta.get('race_type'),
                'purse': meta.get('purse'),
                'claiming_price': meta.get('claiming_price'),
                'conditions': meta.get('conditions'),
                'post_time': str(meta.get('post_time') or ''),
                'field_size': meta.get('field_size'),
                'race_name': meta.get('race_name'),
                'track_condition': meta.get('track_condition'),
                'grade': meta.get('grade'),
                'track_code': track_code,
                'track_name': meta.get('track_name'),
                'predictions': []
            }
            # Track sidebar data
            if track_code not in tracks:
                tracks[track_code] = {
                    'track_code': track_code,
                    'track_name': meta.get('track_name'),
                    'race_count': 0,
                }
            tracks[track_code]['race_count'] += 1

        races[rid]['predictions'].append(
            _serialize_prediction_with_race(pred)
        )

    return list(races.values()), tracks


def get_todays_races(event: dict, context) -> dict:
    """
    GET /races/today?style=<style>
    Returns today's races grouped by track with
    full race metadata and model predictions.
    """
    try:
        qs = event.get('queryStringParameters') or {}
        style = qs.get('style', 'general')
        with get_db() as conn:
            races, tracks = _get_races_with_predictions(
                conn, date.today(), style=style
            )
            return _response(200, {
                'date': str(date.today()),
                'style': style,
                'race_count': len(races),
                'races': races,
                'tracks': list(tracks.values()),
            })
    except Exception as e:
        logger.error(f"get_todays_races error: {e}")
        return _response(500, {'error': str(e)})


def get_race_by_date(event: dict, context) -> dict:
    """
    GET /races/{date}?style=<style>
    Returns races for a specific date with full metadata.

    Optional ?style= query param (default 'general'). Phase A3 added
    'gonzo_sauce' support; pass-through to wr_prediction_repository
    so the embedded predictions match the requested style.
    """
    try:
        path_params = event.get('pathParameters') or {}
        qs = event.get('queryStringParameters') or {}
        date_str = path_params.get('date')
        style = qs.get('style', 'general')
        race_date = date.fromisoformat(date_str)
        with get_db() as conn:
            races, tracks = _get_races_with_predictions(
                conn, race_date, style=style
            )
            return _response(200, {
                'date': date_str,
                'style': style,
                'race_count': len(races),
                'races': races,
                'tracks': list(tracks.values()),
            })
    except Exception as e:
        logger.error(f"get_race_by_date error: {e}")
        return _response(500, {'error': str(e)})


def get_race_detail(event: dict, context) -> dict:
    """
    GET /races/{raceId}/detail
    Returns full race detail with all predictions.
    """
    try:
        from repositories.prediction_repository \
            import PredictionRepository
        path_params = event.get('pathParameters') or {}
        race_id = path_params.get('raceId')
        with get_db() as conn:
            pred_repo = PredictionRepository(conn)
            predictions = pred_repo.get_predictions_by_race(
                race_id
            )
            return _response(200, {
                'race_id': race_id,
                'prediction_count': len(predictions),
                'predictions': [
                    _serialize_prediction_with_race(p)
                    for p in predictions
                ]
            })
    except Exception as e:
        logger.error(f"get_race_detail error: {e}")
        return _response(500, {'error': str(e)})


def get_card(event: dict, context) -> dict:
    """GET /cards/{date}/{track_code} — full day's card metadata for a
    track. Authoritative race-list endpoint for external integrations
    (SmartBoard etc.) — single source of truth for race numbers, names,
    distances, post times, purses, field sizes.
    """
    try:
        pp = event.get('pathParameters') or {}
        date_str = pp.get('date')
        track_code = pp.get('track_code')
        try:
            race_date = date.fromisoformat(date_str)
        except (ValueError, TypeError):
            return _response(400, {
                'error': f'invalid date: {date_str!r} (expected YYYY-MM-DD)'
            })
        if not track_code:
            return _response(400, {'error': 'track_code path param required'})
        with get_db() as conn:
            from repositories.race_repository import RaceRepository
            repo = RaceRepository(conn)
            card = repo.get_card_metadata(track_code, race_date)
            if not card:
                return _response(404, {
                    'error': f'no card found for {track_code} on {date_str}'
                })
            return _response(200, card)
    except Exception as e:
        logger.error(f"get_card error: {e}")
        return _response(500, {'error': str(e)})


def run_predictions(event: dict, context) -> dict:
    """
    POST /predictions/run?date=YYYY-MM-DD
    Triggers inference for a specific date.
    """
    try:
        params = event.get('queryStringParameters') or {}
        date_str = params.get('date')
        if not date_str:
            return _response(400, {
                'error': 'date query param required (YYYY-MM-DD)'
            })
        race_date = date.fromisoformat(date_str)

        from services.inference_service import InferenceService
        with get_db() as conn:
            service = InferenceService(conn)
            service.load_model()
            summary = service.run_daily_predictions(race_date)
            return _response(200, summary)
    except Exception as e:
        logger.error(f"run_predictions error: {e}")
        return _response(500, {'error': str(e)})
