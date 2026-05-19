"""
REPAIR-4 regression test fixtures.

Substrate-pragmatic: tests connect directly to production Aurora DB via
Secrets Manager. Reads only — no writes. Tests are substrate-deterministic
because they assert structural + AS-OF semantic properties.
"""
import json
import boto3
import psycopg2
import psycopg2.extras
import pytest


DB_SECRET_ARN = (
    'arn:aws:secretsmanager:us-east-1:584812014683:'
    'secret:equine-equalizer/db-credentials'
)


@pytest.fixture(scope="session")
def db_conn():
    sm = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(
        sm.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString']
    )
    conn = psycopg2.connect(
        host=secret['host'],
        port=secret['port'],
        dbname=secret['dbname'],
        user=secret['username'],
        password=secret['password'],
        cursor_factory=psycopg2.extras.RealDictCursor,
    )
    yield conn
    conn.close()
