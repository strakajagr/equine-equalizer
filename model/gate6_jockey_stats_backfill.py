"""Gate 6 §F-jockey — jockey_stats_history AS-OF snapshot backfill.

Same pattern as gate6_trainer_stats_backfill.py but for jockey_name.
Uses past_performances.finish_position directly (PP is 99.5% populated)
and the new (trainer_name, race_date) index doesn't help here — but
the (jockey_name) is uncorrelated with trainer index. Will scan PP but
queries finish quickly because there are way fewer jockeys (~1K) than
trainers, and GROUP BY jockey_name has small cardinality.
"""
import logging
import json
from datetime import date, timedelta

import boto3
import psycopg2
import psycopg2.extras

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
    d = start
    while d.weekday() != 6:
        d += timedelta(days=1)
    while d <= end:
        yield d
        d += timedelta(days=7)


def backfill_snapshot(conn, snapshot_date: date):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM jockey_stats_history WHERE snapshot_date = %s",
            (snapshot_date,),
        )
        cur.execute("""
            INSERT INTO jockey_stats_history (
                jockey_name, total_starts, wins, win_rate, itm, itm_rate,
                snapshot_date, created_at
            )
            SELECT pp.jockey_name,
                   COUNT(*)::int AS total_starts,
                   COUNT(*) FILTER (WHERE pp.finish_position = 1)::int AS wins,
                   AVG((pp.finish_position = 1)::int)::numeric AS win_rate,
                   COUNT(*) FILTER (WHERE pp.finish_position <= 3)::int AS itm,
                   AVG((pp.finish_position <= 3)::int)::numeric AS itm_rate,
                   %s::date, NOW()
            FROM past_performances pp
            WHERE pp.race_date < %s
              AND pp.race_date >= %s
              AND pp.jockey_name IS NOT NULL
              AND pp.finish_position IS NOT NULL
            GROUP BY pp.jockey_name
            HAVING COUNT(*) >= 5
        """, (snapshot_date, snapshot_date, snapshot_date - timedelta(days=730)))
        n = cur.rowcount
    conn.commit()
    return n


def main():
    conn = get_conn()
    snapshots = list(weekly_snapshots(date(2022, 1, 1), date(2026, 5, 17)))
    logger.info(f"Building {len(snapshots)} weekly jockey snapshots")
    for sd in snapshots:
        try:
            n = backfill_snapshot(conn, sd)
            logger.info(f"snapshot={sd}  jockeys={n}")
        except Exception as e:
            logger.error(f"snapshot={sd} failed: {e}")
            conn.rollback()
    conn.close()
    logger.info("jockey_stats_history backfill complete")


if __name__ == '__main__':
    main()
