import logging
from datetime import date
from shared.db import get_db
from services.evaluation_service import (
    EvaluationService
)

logger = logging.getLogger(__name__)


def handler(event, context):
    logger.info(
        f"Results ingestion triggered for "
        f"{date.today()}"
    )
    with get_db() as conn:
        service = EvaluationService(conn)
        service.record_results(date.today())
    return {'statusCode': 200,
            'body': 'Results recorded'}
