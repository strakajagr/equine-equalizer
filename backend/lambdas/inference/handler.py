import json
import logging
import re
from datetime import date
from shared.db import get_db
from services.inference_service import InferenceService
from routers import (
    race_router, prediction_router,
    horse_router, dashboard_router
)
from routers.health_router import health_check

logger = logging.getLogger(__name__)

# Module-level service instance for Lambda
# container reuse (warm start optimization)
_inference_service = None


def _get_inference_service(conn):
    global _inference_service
    if _inference_service is None:
        _inference_service = InferenceService(conn)
        _inference_service.load_model()
    return _inference_service


def _cors_response(status_code=200, body=''):
    """CORS preflight response."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': body if isinstance(body, str) else json.dumps(body)
    }


def handler(event, context):
    path = event.get('rawPath', '')
    method = event.get(
        'requestContext', {}
    ).get('http', {}).get('method', 'GET')

    logger.info(f"{method} {path}")

    # CORS preflight
    if method == 'OPTIONS':
        return _cors_response()

    # EventBridge scheduled trigger
    if 'source' in event and event['source'] == 'aws.events':
        logger.info("EventBridge trigger: running daily predictions")
        with get_db() as conn:
            service = InferenceService(conn)
            service.load_model()
            summary = service.run_daily_predictions(date.today())
        return {'statusCode': 200, 'body': str(summary)}

    # Batch inference trigger (from ingestion Lambda)
    if 'source' in event and event['source'] == 'batch':
        target_date = date.fromisoformat(event['date'])
        logger.info(f"Batch inference for {target_date}")
        with get_db() as conn:
            service = InferenceService(conn)
            service.load_model()
            summary = service.run_daily_predictions(target_date)
        return {'statusCode': 200, 'body': str(summary)}

    # ── Health ──
    if path == '/health':
        return health_check(event, context)

    # ── Dashboard ──
    if path == '/dashboard/metrics':
        return dashboard_router.get_dashboard_metrics(
            event, context
        )

    # ── Available dates ──
    if path == '/races/available-dates':
        return dashboard_router.get_available_dates(
            event, context
        )

    # ── Races ──
    if path == '/races/today':
        return race_router.get_todays_races(event, context)

    # POST /predictions/run?date=YYYY-MM-DD
    if path == '/predictions/run' and method == 'POST':
        return race_router.run_predictions(event, context)

    # GET /predictions/run?date=YYYY-MM-DD (allow GET too)
    if path == '/predictions/run':
        return race_router.run_predictions(event, context)

    # GET /races/{raceId}/detail
    if '/races/' in path and '/detail' in path:
        return race_router.get_race_detail(event, context)

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

    # GET /horses/{horse_id}/pps
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

    # ── Predictions ──
    if path == '/predictions/value' or path.startswith('/predictions/value'):
        return prediction_router.get_value_plays(
            event, context
        )

    if path == '/predictions/today':
        return prediction_router.get_todays_predictions(
            event, context
        )

    # GET /predictions/{date}/{track_code}/{race_number} — unified endpoint
    # Must come BEFORE the bare /predictions/{date} match below so the
    # unanchored date regex doesn't swallow the more-specific path.
    unified_match = re.match(
        r'/predictions/(\d{4}-\d{2}-\d{2})/([A-Z]+)/(\d+)$', path
    )
    if unified_match:
        if not event.get('pathParameters'):
            event['pathParameters'] = {}
        event['pathParameters']['date'] = unified_match.group(1)
        event['pathParameters']['track_code'] = unified_match.group(2)
        event['pathParameters']['race_number'] = unified_match.group(3)
        from routers.unified_prediction_router import (
            get_unified_predictions
        )
        return get_unified_predictions(event, context)

    # GET /predictions/{date}
    pred_date_match = re.match(
        r'/predictions/(\d{4}-\d{2}-\d{2})$', path
    )
    if pred_date_match:
        if not event.get('pathParameters'):
            event['pathParameters'] = {}
        event['pathParameters']['date'] = (
            pred_date_match.group(1)
        )
        return prediction_router.get_predictions_by_date(
            event, context
        )

    # GET /races/{date} (YYYY-MM-DD format)
    race_date_match = re.match(
        r'/races/(\d{4}-\d{2}-\d{2})', path
    )
    if race_date_match:
        if not event.get('pathParameters'):
            event['pathParameters'] = {}
        event['pathParameters']['date'] = (
            race_date_match.group(1)
        )
        return race_router.get_race_by_date(event, context)

    # ── PB.4 Daily report routes ──
    if path == '/api/reports/strategy/list' or path == '/reports/strategy/list':
        from routers.daily_report_router import get_strategy_list
        return get_strategy_list(event, context)

    if path == '/api/reports/strategy_pnl/range' or path == '/reports/strategy_pnl/range':
        from routers.daily_report_router import get_strategy_pnl_range
        return get_strategy_pnl_range(event, context)

    # GET /api/reports/strategy/{name}/history
    strat_hist_match = re.match(r'(?:/api)?/reports/strategy/([^/]+)/history$', path)
    if strat_hist_match:
        from routers.daily_report_router import get_strategy_history
        return get_strategy_history(event, context)

    # GET /api/reports/daily/{race_date}
    daily_match = re.match(r'(?:/api)?/reports/daily/(\d{4}-\d{2}-\d{2})$', path)
    if daily_match:
        from routers.daily_report_router import get_daily_report
        return get_daily_report(event, context)

    return {
        'statusCode': 404,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': f'Route not found: {path}'})
    }
