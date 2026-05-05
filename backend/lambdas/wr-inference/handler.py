import json
import logging
import re
from datetime import date
from shared.db import get_db
from services.wr_inference_service import WRInferenceService
from routers import (
    race_router, horse_router, dashboard_router
)
from routers import wr_prediction_router
from routers.health_router import health_check

logger = logging.getLogger(__name__)

# Module-level service instance for Lambda
# container reuse (warm start optimization)
_wr_service = None


def _get_wr_service(conn):
    global _wr_service
    if _wr_service is None:
        _wr_service = WRInferenceService(conn)
        _wr_service.load_model()
    return _wr_service


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

    logger.info(f"WR {method} {path}")

    # CORS preflight
    if method == 'OPTIONS':
        return _cors_response()

    # EventBridge scheduled trigger (12:30 ET daily)
    if 'source' in event and \
            event['source'] == 'aws.events':
        style = event.get('style', 'general')
        logger.info(
            f"WR EventBridge trigger: running daily predictions "
            f"(style={style})"
        )
        with get_db() as conn:
            service = WRInferenceService(conn, style=style)
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
            f"WR batch inference for {target_date} (style={style})"
        )
        with get_db() as conn:
            service = WRInferenceService(conn, style=style)
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

    # ── Dashboard (migrated from retired legacy inference) ──
    if path == '/dashboard/metrics':
        return dashboard_router.get_dashboard_metrics(
            event, context
        )

    # ── Available dates (migrated from retired legacy inference) ──
    if path == '/races/available-dates':
        return dashboard_router.get_available_dates(
            event, context
        )

    # ── WR predictions run ──
    if path == '/wr/predictions/run':
        target_date = None
        params = event.get('queryStringParameters') or {}
        if 'date' in params:
            target_date = date.fromisoformat(
                params['date']
            )
        style = params.get('style', 'general')
        with get_db() as conn:
            service = WRInferenceService(conn, style=style)
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

    # ── WR predictions today ──
    if path == '/wr/predictions/today':
        return wr_prediction_router.get_todays_predictions(
            event, context
        )

    # ── WR value plays ──
    if path == '/wr/predictions/value' or \
            path.startswith('/wr/predictions/value'):
        return wr_prediction_router.get_value_plays(
            event, context
        )

    # ── WR top picks ──
    if path == '/wr/predictions/top-picks' or \
            path.startswith('/wr/predictions/top-picks'):
        return wr_prediction_router.get_top_picks(
            event, context
        )

    # ── Stream E2: track-record (must come BEFORE the {date} regex
    # below; otherwise 'track-record' would be parsed as a date) ──
    if path == '/wr/predictions/track-record':
        return wr_prediction_router.get_track_record(
            event, context
        )
    if path == '/wr/predictions/track-record-by-style':
        return wr_prediction_router.get_track_record_by_style(
            event, context
        )

    # GET /wr/predictions/{date}/compare?style=<specialist>
    # Must come BEFORE the bare /wr/predictions/{date} match below
    # (more-specific path first).
    compare_match = re.match(
        r'/wr/predictions/(\d{4}-\d{2}-\d{2})/compare$', path
    )
    if compare_match:
        if not event.get('pathParameters'):
            event['pathParameters'] = {}
        event['pathParameters']['date'] = compare_match.group(1)
        return wr_prediction_router.get_compared_predictions_by_date(
            event, context
        )

    # GET /wr/predictions/{date}/{track_code}/{race_number}
    # Race-scoped endpoint — must come BEFORE the bare {date} match.
    race_scoped_match = re.match(
        r'/wr/predictions/(\d{4}-\d{2}-\d{2})/([A-Z]+)/(\d+)$', path
    )
    if race_scoped_match:
        if not event.get('pathParameters'):
            event['pathParameters'] = {}
        event['pathParameters']['date'] = race_scoped_match.group(1)
        event['pathParameters']['track_code'] = race_scoped_match.group(2)
        event['pathParameters']['race_number'] = race_scoped_match.group(3)
        return wr_prediction_router.get_predictions_by_date_track_race(
            event, context
        )

    # GET /wr/predictions/{date}
    # Anchored with $ so longer paths (e.g. {date}/{track}/{race}) don't
    # silently fall through and return the full day's predictions.
    wr_pred_date_match = re.match(
        r'/wr/predictions/(\d{4}-\d{2}-\d{2})$', path
    )
    if wr_pred_date_match:
        if not event.get('pathParameters'):
            event['pathParameters'] = {}
        event['pathParameters']['date'] = (
            wr_pred_date_match.group(1)
        )
        return wr_prediction_router.get_predictions_by_date(
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

    # GET /cards/{date}/{track_code} — full day card metadata
    card_match = re.match(
        r'/cards/(\d{4}-\d{2}-\d{2})/([A-Z]+)$', path
    )
    if card_match:
        if not event.get('pathParameters'):
            event['pathParameters'] = {}
        event['pathParameters']['date'] = card_match.group(1)
        event['pathParameters']['track_code'] = card_match.group(2)
        return race_router.get_card(event, context)

    # GET /races/{date} (migrated from retired legacy inference).
    # Must be last among /races/* so more specific paths
    # (/races/today, /races/available-dates, /races/{id}/detail)
    # match first.
    race_date_match = re.match(
        r'/races/(\d{4}-\d{2}-\d{2})$', path
    )
    if race_date_match:
        if not event.get('pathParameters'):
            event['pathParameters'] = {}
        event['pathParameters']['date'] = (
            race_date_match.group(1)
        )
        return race_router.get_race_by_date(event, context)

    return {
        'statusCode': 404,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(
            {'error': f'WR route not found: {path}'}
        )
    }
