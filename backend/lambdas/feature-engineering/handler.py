import logging
from datetime import date
from shared.db import get_db
from services.feature_engineering_service import (
    FeatureEngineeringService
)

logger = logging.getLogger(__name__)


def handler(event, context):
    logger.info(
        f"Feature engineering triggered for "
        f"{date.today()}"
    )
    # TODO: Wire to feature_engineering_service
    # when implemented
    return {'statusCode': 200,
            'body': 'Feature engineering complete'}
