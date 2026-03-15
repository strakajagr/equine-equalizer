import argparse
import json
import logging
import os
import sys
from pathlib import Path

import boto3
import psycopg2

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

MIGRATIONS_DIR = Path(__file__).parent
SEEDS_DIR = MIGRATIONS_DIR.parent / "seeds"


def get_connection_string() -> str:
    """Get database connection string from DATABASE_URL or Secrets Manager."""
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        logger.info("Using DATABASE_URL for connection")
        return database_url

    secret_arn = os.environ.get("DB_SECRET_ARN")
    if not secret_arn:
        logger.error("Neither DATABASE_URL nor DB_SECRET_ARN is set")
        sys.exit(1)

    logger.info("Fetching database credentials from Secrets Manager")
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_arn)
    secret = json.loads(response["SecretString"])

    return (
        f"postgresql://{secret['username']}:{secret['password']}"
        f"@{secret['host']}:{secret['port']}/{secret['dbname']}"
    )


def ensure_migrations_table(conn):
    """Create schema_migrations table if it doesn't exist."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                migration_id SERIAL PRIMARY KEY,
                filename VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
    conn.commit()


def get_applied_migrations(conn) -> set:
    """Return set of filenames already applied."""
    with conn.cursor() as cur:
        cur.execute("SELECT filename FROM schema_migrations")
        return {row[0] for row in cur.fetchall()}


def run_migrations(conn) -> tuple[int, int]:
    """Run pending migrations. Returns (applied_count, skipped_count)."""
    ensure_migrations_table(conn)
    applied_set = get_applied_migrations(conn)

    sql_files = sorted(
        f for f in os.listdir(MIGRATIONS_DIR)
        if f.endswith(".sql")
    )

    applied_count = 0
    skipped_count = 0

    for filename in sql_files:
        if filename in applied_set:
            logger.info("Skipping already applied: %s", filename)
            skipped_count += 1
            continue

        filepath = MIGRATIONS_DIR / filename
        sql = filepath.read_text()

        logger.info("Applying migration: %s", filename)
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
                cur.execute(
                    "INSERT INTO schema_migrations (filename) VALUES (%s)",
                    (filename,),
                )
            conn.commit()
            logger.info("Migration complete: %s", filename)
            applied_count += 1
        except Exception as e:
            conn.rollback()
            logger.error("Migration failed: %s", filename)
            logger.error("Error: %s", e)
            logger.error("Failing SQL:\n%s", sql)
            sys.exit(1)

    return applied_count, skipped_count


def run_seeds(conn) -> int:
    """Run all seed files from seeds/ directory. Returns count."""
    if not SEEDS_DIR.exists():
        logger.info("No seeds directory found, skipping")
        return 0

    sql_files = sorted(
        f for f in os.listdir(SEEDS_DIR)
        if f.endswith(".sql")
    )

    seed_count = 0
    for filename in sql_files:
        filepath = SEEDS_DIR / filename
        sql = filepath.read_text()

        logger.info("Applying seed: %s", filename)
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
            seed_count += 1
        except Exception as e:
            conn.rollback()
            logger.error("Seed failed: %s", filename)
            logger.error("Error: %s", e)
            sys.exit(1)

    return seed_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Equine Equalizer database migration runner")
    parser.add_argument("--seed", action="store_true", help="Run seed files after migrations")
    args = parser.parse_args()

    conn_string = get_connection_string()
    conn = psycopg2.connect(conn_string)

    try:
        applied, skipped = run_migrations(conn)
        seeds = 0
        if args.seed:
            seeds = run_seeds(conn)

        logger.info(
            "Migrations complete. Applied: %d  Skipped: %d  Seeds: %d",
            applied, skipped, seeds,
        )
    finally:
        conn.close()
