import logging
from datetime import date
from shared.db import get_db
from services.ingestion_service import (
    IngestionService
)

logger = logging.getLogger(__name__)


def handler(event, context):
    logger.info(
        f"Ingestion triggered for {date.today()}"
    )
    with get_db() as conn:
        service = IngestionService(conn)
        service.fetch_daily_entries(date.today())
    return {'statusCode': 200,
            'body': 'Ingestion complete'}
