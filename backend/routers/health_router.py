import json
from datetime import datetime
from shared.db import get_db


def health_check(event: dict, context) -> dict:
    """
    GET /health
    Returns 200 if API and database are reachable.
    Used by monitoring and deployment verification.
    """
    db_status = 'unknown'
    db_time = None
    try:
        with get_db() as conn:
            from shared.db import execute_one
            result = execute_one(
                conn, 'SELECT NOW() as current_time'
            )
            db_status = 'connected'
            db_time = str(result['current_time'])
    except Exception as e:
        db_status = f'error: {str(e)}'

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'status': 'ok',
            'timestamp': str(datetime.utcnow()),
            'database': db_status,
            'database_time': db_time
        })
    }
