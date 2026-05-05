import logging
from datetime import date
from shared.db import get_db
from services.evaluation_service import (
    EvaluationService
)

logger = logging.getLogger(__name__)


def handler(event, context):
    # Accept date from event, fallback to today
    target_date = date.today()
    if isinstance(event, dict) and 'date' in event:
        target_date = date.fromisoformat(event['date'])

    logger.info(
        f"Results evaluation triggered for "
        f"{target_date}"
    )
    with get_db() as conn:
        service = EvaluationService(conn)
        result = service.record_results(target_date)
    return {'statusCode': 200,
            'body': f'Results recorded: {result}'}
