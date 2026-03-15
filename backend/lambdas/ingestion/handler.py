import logging
import json
import os
import sys
from datetime import date
from shared.db import get_db
from services.ingestion_service import (
    IngestionService
)

logger = logging.getLogger(__name__)


def handler(event, context):
    logger.info(
        f"Ingestion handler called with "
        f"event: {json.dumps(event)}"
    )

    action = event.get('action')

    # ── Migration action ──
    # Invoked manually to run DB migrations
    # from inside the VPC where Aurora is reachable
    if action == 'migrate':
        logger.info("Running database migrations")
        seed = event.get('seed', False)

        try:
            # Add task root to path so migrate.py
            # can import from the same codebase
            task_root = '/var/task'
            if task_root not in sys.path:
                sys.path.insert(0, task_root)

            migrate_path = os.path.join(
                task_root,
                'database/migrations/migrate.py'
            )

            # Build args
            args = [sys.executable, migrate_path]
            if seed:
                args.append('--seed')

            import subprocess
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                }
            )

            logger.info(
                f"Migration stdout:\n{result.stdout}"
            )
            if result.stderr:
                logger.warning(
                    f"Migration stderr:\n{result.stderr}"
                )

            success = result.returncode == 0
            logger.info(
                f"Migration {'succeeded' if success else 'FAILED'}"
                f" (exit code {result.returncode})"
            )

            return {
                'statusCode': 200 if success else 500,
                'body': json.dumps({
                    'success': success,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'returncode': result.returncode
                })
            }

        except Exception as e:
            logger.error(
                f"Migration exception: {e}",
                exc_info=True
            )
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'success': False,
                    'error': str(e)
                })
            }

    # ── Health check action ──
    if action == 'health':
        with get_db() as conn:
            from shared.db import execute_one
            result = execute_one(
                conn, 'SELECT NOW() as t'
            )
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'status': 'ok',
                    'db_time': str(result['t'])
                })
            }

    # ── Normal scheduled ingestion ──
    logger.info(
        f"Daily ingestion triggered for {date.today()}"
    )
    try:
        with get_db() as conn:
            service = IngestionService(conn)
            service.fetch_daily_entries(date.today())
        return {
            'statusCode': 200,
            'body': 'Ingestion complete'
        }
    except Exception as e:
        logger.error(
            f"Ingestion failed: {e}",
            exc_info=True
        )
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
