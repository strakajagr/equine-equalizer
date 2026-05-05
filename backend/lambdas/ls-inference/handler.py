import json
import logging
import re
from datetime import date
from shared.db import get_db
from services.ls_inference_service import LSInferenceService
from routers import (
    race_router, horse_router
)
from routers import ls_prediction_router
from routers.health_router import health_check

logger = logging.getLogger(__name__)


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

    logger.info(f"LS {method} {path}")

    # CORS preflight
    if method == 'OPTIONS':
        return _cors_response()

    # EventBridge scheduled trigger (12:40 ET daily)
    # Graceful no-op if no active LS model
    if 'source' in event and \
            event['source'] == 'aws.events':
        logger.info(
            "LS EventBridge trigger: "
            "attempting daily predictions"
        )
        with get_db() as conn:
            service = LSInferenceService(conn)
            summary = service.run_daily_predictions(
                date.today()
            )
        return {
            'statusCode': 200,
            'body': json.dumps(summary)
        }

    # Batch trigger (from ingestion Lambda)
    if 'source' in event and \
            event['source'] == 'batch':
        target_date = date.fromisoformat(event['date'])
        logger.info(
            f"LS batch inference for {target_date}"
        )
        with get_db() as conn:
            service = LSInferenceService(conn)
            summary = service.run_daily_predictions(
                target_date
            )
        return {
            'statusCode': 200,
            'body': json.dumps(summary)
        }

    # Manual trigger: {"action":"run_predictions","date":"2026-03-22"}
    if event.get('action') == 'run_predictions':
        target_date = date.fromisoformat(
            event.get('date', str(date.today()))
        )
        logger.info(f"LS manual run for {target_date}")
        with get_db() as conn:
            service = LSInferenceService(conn)
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

    # ── LS predictions run ──
    if path == '/ls/predictions/run':
        target_date = None
        params = event.get('queryStringParameters') or {}
        if 'date' in params:
            target_date = date.fromisoformat(
                params['date']
            )
        with get_db() as conn:
            service = LSInferenceService(conn)
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

    # ── LS predictions today ──
    if path == '/ls/predictions/today':
        return ls_prediction_router.get_todays_predictions(
            event, context
        )

    # ── LS longshot alerts ──
    if path == '/ls/predictions/longshots' or \
            path.startswith('/ls/predictions/longshots'):
        return ls_prediction_router.get_longshot_alerts(
            event, context
        )

    # ── Stream E2: track-record (must come BEFORE the {date} regex) ──
    if path == '/ls/predictions/track-record':
        return ls_prediction_router.get_track_record(
            event, context
        )

    # GET /ls/predictions/{date}/{track_code}/{race_number}
    ls_race_scoped_match = re.match(
        r'/ls/predictions/(\d{4}-\d{2}-\d{2})/([A-Z]+)/(\d+)$', path
    )
    if ls_race_scoped_match:
        if not event.get('pathParameters'):
            event['pathParameters'] = {}
        event['pathParameters']['date'] = ls_race_scoped_match.group(1)
        event['pathParameters']['track_code'] = ls_race_scoped_match.group(2)
        event['pathParameters']['race_number'] = ls_race_scoped_match.group(3)
        return ls_prediction_router.get_predictions_by_date_track_race(
            event, context
        )

    # GET /ls/predictions/{date} — anchored with $ so race-scoped paths
    # don't silently fall through.
    ls_pred_date_match = re.match(
        r'/ls/predictions/(\d{4}-\d{2}-\d{2})$', path
    )
    if ls_pred_date_match:
        if not event.get('pathParameters'):
            event['pathParameters'] = {}
        event['pathParameters']['date'] = (
            ls_pred_date_match.group(1)
        )
        return ls_prediction_router.get_predictions_by_date(
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
            {'error': f'LS route not found: {path}'}
        )
    }
