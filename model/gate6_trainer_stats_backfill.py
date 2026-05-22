"""Gate 6 §E — trainer_stats_history AS-OF snapshot backfill.

Builds weekly snapshots of trainer aggregates from results history, so the
training FE pipeline can query AS-OF each race_date instead of using a single
2026-05-19 snapshot (which leaks future stats into past predictions).

For each Sunday in 2022-01-02 → 2026-05-17:
  - DELETE existing rows for that snapshot_date
  - INSERT aggregates computed from results WHERE race_date < snapshot_date
    grouped by trainer_name

Idempotent. Safe to re-run.
"""
import logging
import os
from datetime import date, timedelta

import boto3
import psycopg2
import psycopg2.extras
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

DB_SECRET_ARN = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'


def get_conn():
    sm = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString'])
    return psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'],
        password=secret['password'],
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


def weekly_snapshots(start: date, end: date):
    """Yield each Sunday between start and end inclusive."""
    # Sunday = weekday 6
    d = start
    while d.weekday() != 6:
        d += timedelta(days=1)
    while d <= end:
        yield d
        d += timedelta(days=7)


def backfill_snapshot(conn, snapshot_date: date):
    """Compute + insert trainer_stats_history rows for this snapshot date.

    OPTIMIZED: uses past_performances.finish_position directly instead of
    joining results (PP table already has finish_position at 99.5%
    coverage). Removes the correlated subquery that was the bottleneck.
    """
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM trainer_stats_history WHERE snapshot_date = %s",
            (snapshot_date,),
        )
        cur.execute("""
            INSERT INTO trainer_stats_history (
                trainer_name, total_starts, wins, win_rate, itm, itm_rate,
                layoff_win_rate, lasix_win_rate, claimed_win_rate,
                snapshot_date, created_at
            )
            SELECT
                pp.trainer_name,
                COUNT(*)::int AS total_starts,
                COUNT(*) FILTER (WHERE pp.finish_position = 1)::int AS wins,
                AVG((pp.finish_position = 1)::int)::numeric AS win_rate,
                COUNT(*) FILTER (WHERE pp.finish_position <= 3)::int AS itm,
                AVG((pp.finish_position <= 3)::int)::numeric AS itm_rate,
                AVG((pp.finish_position = 1)::int)
                  FILTER (WHERE pp.days_since_last_race > 60)::numeric AS layoff_win_rate,
                AVG((pp.finish_position = 1)::int)
                  FILTER (WHERE pp.lasix = TRUE)::numeric AS lasix_win_rate,
                0.0 AS claimed_win_rate,
                %s::date AS snapshot_date,
                NOW() AS created_at
            FROM past_performances pp
            WHERE pp.race_date < %s
              AND pp.race_date >= %s  -- 2-year rolling window
              AND pp.trainer_name IS NOT NULL
              AND pp.finish_position IS NOT NULL
            GROUP BY pp.trainer_name
            HAVING COUNT(*) >= 5
        """, (snapshot_date, snapshot_date, snapshot_date - timedelta(days=730)))
        n = cur.rowcount
    conn.commit()
    return n


def main():
    conn = get_conn()
    snapshots = list(weekly_snapshots(date(2022, 1, 1), date(2026, 5, 17)))
    logger.info(f"Building {len(snapshots)} weekly snapshots")
    for sd in snapshots:
        try:
            n = backfill_snapshot(conn, sd)
            logger.info(f"snapshot={sd}  trainers={n:,}")
        except Exception as e:
            logger.error(f"snapshot={sd} failed: {e}")
            conn.rollback()
    conn.close()
    logger.info("trainer_stats_history backfill complete")


if __name__ == '__main__':
    main()
