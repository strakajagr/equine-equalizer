import logging
from datetime import date
from shared.db import get_db
from services.inference_service import (
    InferenceService
)
from routers import race_router, prediction_router
from routers.health_router import health_check

logger = logging.getLogger(__name__)

# Module-level service instance for Lambda
# container reuse (warm start optimization)
_inference_service = None


def _get_inference_service(conn):
    """
    Return cached inference service if available.
    On cold start: creates new instance,
    loads model from S3.
    On warm start: reuses existing instance
    with model already in memory.
    This avoids re-downloading the model
    on every invocation.
    """
    global _inference_service
    if _inference_service is None:
        _inference_service = InferenceService(conn)
        _inference_service.load_model()
    return _inference_service


def handler(event, context):
    path = event.get('rawPath', '')
    method = event.get(
        'requestContext', {}
    ).get('http', {}).get('method', 'GET')

    logger.info(f"{method} {path}")

    # EventBridge scheduled trigger
    # (no path — this is the daily pipeline run)
    if 'source' in event and event[
        'source'
    ] == 'aws.events':
        logger.info(
            "EventBridge trigger: running daily"
            " predictions"
        )
        with get_db() as conn:
            service = InferenceService(conn)
            service.load_model()
            summary = service.run_daily_predictions(
                date.today()
            )
        return {
            'statusCode': 200,
            'body': str(summary)
        }

    # API Gateway requests
    if path == '/health':
        return health_check(event, context)

    if '/races/today' in path:
        return race_router.get_todays_races(
            event, context
        )

    if '/races/' in path and '/detail' in path:
        return race_router.get_race_detail(
            event, context
        )

    if '/predictions/value' in path:
        return prediction_router.get_value_plays(
            event, context
        )

    if '/predictions/today' in path:
        return prediction_router \
            .get_todays_predictions(event, context)

    if '/predictions/' in path:
        return prediction_router \
            .get_predictions_by_date(event, context)

    return {
        'statusCode': 404,
        'body': 'Route not found'
    }
