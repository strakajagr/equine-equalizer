import json
import logging
import re
from datetime import date
from shared.db import get_db
from services.pl_inference_service import PLInferenceService
from routers import (
    race_router, horse_router, dashboard_router
)
from routers import pl_prediction_router
from routers.health_router import health_check

logger = logging.getLogger(__name__)

# Module-level service instance for Lambda
# container reuse (warm start optimization)
_pl_service = None


def _get_pl_service(conn):
    global _pl_service
    if _pl_service is None:
        _pl_service = PLInferenceService(conn)
        _pl_service.load_model()
    return _pl_service


def _cors_response(status_code=200, body=''):
    """CORS preflight response."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods':
                'GET,POST,OPTIONS',
            'Access-Control-Allow-Headers':
                'Content-Type',
        },
        'body': (
            body if isinstance(body, str)
            else json.dumps(body)
        )
    }


def handler(event, context):
    path = event.get('rawPath', '')
    method = event.get(
        'requestContext', {}
    ).get('http', {}).get('method', 'GET')

    logger.info(f"PL {method} {path}")

    # CORS preflight
    if method == 'OPTIONS':
        return _cors_response()

    # EventBridge scheduled trigger (12:35 ET daily)
    if 'source' in event and \
            event['source'] == 'aws.events':
        style = event.get('style', 'general')
        logger.info(
            f"PL EventBridge trigger: running daily predictions "
            f"(style={style})"
        )
        with get_db() as conn:
            service = PLInferenceService(conn, style=style)
            service.load_model()
            summary = service.run_daily_predictions(
                date.today()
            )
        return {
            'statusCode': 200,
            'body': json.dumps(summary)
        }

    # Batch trigger (from ingestion Lambda or pre-compute)
    if 'source' in event and \
            event['source'] == 'batch':
        target_date = date.fromisoformat(event['date'])
        style = event.get('style', 'general')
        logger.info(
            f"PL batch inference for {target_date} (style={style})"
        )
        with get_db() as conn:
            service = PLInferenceService(conn, style=style)
            service.load_model()
            summary = service.run_daily_predictions(
                target_date
            )
        return {
            'statusCode': 200,
            'body': json.dumps(summary)
        }

    # ── Health ──
    if path == '/health':
        return health_check(event, context)

    # ── PL predictions run ──
    if path == '/pl/predictions/run':
        target_date = None
        params = event.get('queryStringParameters') or {}
        if 'date' in params:
            target_date = date.fromisoformat(
                params['date']
            )
        style = params.get('style', 'general')
        with get_db() as conn:
            service = PLInferenceService(conn, style=style)
            service.load_model()
            summary = service.run_daily_predictions(
                target_date
            )
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(summary)
        }

    # ── PL predictions today ──
    if path == '/pl/predictions/today':
        return pl_prediction_router.get_todays_predictions(
            event, context
        )

    # ── PL value bets ──
    if path == '/pl/predictions/value-bets' or \
            path.startswith('/pl/predictions/value-bets'):
        return pl_prediction_router.get_value_bets(
            event, context
        )

    # ── PL strong value bets ──
    if path == '/pl/predictions/strong-value' or \
            path.startswith('/pl/predictions/strong-value'):
        return pl_prediction_router.get_strong_value_bets(
            event, context
        )

    # ── Stream E2: track-record (must come BEFORE the {date} regex) ──
    if path == '/pl/predictions/track-record':
        return pl_prediction_router.get_track_record(
            event, context
        )

    # GET /pl/predictions/{date}/{track_code}/{race_number}
    pl_race_scoped_match = re.match(
        r'/pl/predictions/(\d{4}-\d{2}-\d{2})/([A-Z]+)/(\d+)$', path
    )
    if pl_race_scoped_match:
        if not event.get('pathParameters'):
            event['pathParameters'] = {}
        event['pathParameters']['date'] = pl_race_scoped_match.group(1)
        event['pathParameters']['track_code'] = pl_race_scoped_match.group(2)
        event['pathParameters']['race_number'] = pl_race_scoped_match.group(3)
        return pl_prediction_router.get_predictions_by_date_track_race(
            event, context
        )

    # GET /pl/predictions/{date} — anchored with $ so race-scoped paths
    # don't silently fall through.
    pl_pred_date_match = re.match(
        r'/pl/predictions/(\d{4}-\d{2}-\d{2})$', path
    )
    if pl_pred_date_match:
        if not event.get('pathParameters'):
            event['pathParameters'] = {}
        event['pathParameters']['date'] = (
            pl_pred_date_match.group(1)
        )
        return pl_prediction_router.get_predictions_by_date(
            event, context
        )

    # ── Shared race routes ──
    if path == '/races/today':
        return race_router.get_todays_races(
            event, context
        )

    if '/races/' in path and '/detail' in path:
        return race_router.get_race_detail(event, context)

    horse_pp_match = re.match(
        r'/horses/([^/]+)/pps', path
    )
    if horse_pp_match:
        if not event.get('pathParameters'):
            event['pathParameters'] = {}
        event['pathParameters']['horse_id'] = (
            horse_pp_match.group(1)
        )
        return horse_router.get_horse_pps(event, context)

    return {
        'statusCode': 404,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(
            {'error': f'PL route not found: {path}'}
        )
    }
