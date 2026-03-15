import os
import json
import logging
import boto3
import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from typing import Optional

logger = logging.getLogger(__name__)


def _get_connection_string() -> str:
    """
    Returns database connection string.
    Checks DATABASE_URL env var first (local dev).
    Falls back to Secrets Manager using DB_SECRET_ARN.
    Never logs credentials.
    """
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return database_url

    secret_arn = os.environ.get('DB_SECRET_ARN')
    if not secret_arn:
        raise ValueError(
            "Neither DATABASE_URL nor DB_SECRET_ARN "
            "environment variables are set"
        )

    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_arn)
    secret = json.loads(response['SecretString'])

    return (
        f"postgresql://{secret['username']}:"
        f"{secret['password']}@{secret['host']}:"
        f"{secret['port']}/{secret['dbname']}"
    )


@contextmanager
def get_db():
    """
    Context manager for database connections.

    Usage:
      with get_db() as conn:
        with conn.cursor() as cur:
          cur.execute(...)

    Commits on clean exit.
    Rolls back on exception.
    Always closes connection.
    """
    conn = None
    try:
        conn_string = _get_connection_string()
        conn = psycopg2.connect(
            conn_string,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {type(e).__name__}: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()


def execute_query(
    conn,
    sql: str,
    params: tuple = None
) -> list[dict]:
    """
    Execute a SELECT query.
    Returns list of row dicts.
    Never returns raw cursor objects.
    """
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]


def execute_one(
    conn,
    sql: str,
    params: tuple = None
) -> Optional[dict]:
    """
    Execute a SELECT query expecting one row.
    Returns single row dict or None.
    """
    with conn.cursor() as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        return dict(row) if row else None


def execute_write(
    conn,
    sql: str,
    params: tuple = None
) -> None:
    """
    Execute an INSERT, UPDATE, or DELETE.
    Returns nothing.
    Caller is responsible for commit via context manager.
    """
    with conn.cursor() as cur:
        cur.execute(sql, params)


def execute_write_returning(
    conn,
    sql: str,
    params: tuple = None
) -> Optional[dict]:
    """
    Execute an INSERT ... RETURNING or
    UPDATE ... RETURNING.
    Returns the returned row as dict.
    Use for inserts that need the generated ID back.
    """
    with conn.cursor() as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        return dict(row) if row else None
