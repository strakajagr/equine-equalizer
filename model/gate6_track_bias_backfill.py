"""Gate 6 §F-track-bias — track_bias_history AS-OF snapshot backfill.

Per (track_code × surface × snapshot_date) computes:
  - inside_post_win_rate (posts 1-3 win pct vs all)
  - outside_post_win_rate (posts >= field_size-2)
  - front_runner_win_rate (call_1_position <= 2 → wins)
  - closer_win_rate (call_1_position >= field_size-2 → wins)
  - avg_winning_post_position

2-year rolling lookback. Strictly pre-snapshot data only.
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
            "DELETE FROM track_bias_history WHERE snapshot_date = %s",
            (snapshot_date,),
        )
        cur.execute("""
            INSERT INTO track_bias_history (
                track_code, surface, snapshot_date, n_races,
                inside_post_win_rate, outside_post_win_rate,
                front_runner_win_rate, closer_win_rate,
                avg_winning_post_position, created_at
            )
            SELECT pp.track_code,
                   COALESCE(pp.surface, 'unknown') AS surface,
                   %s::date AS snapshot_date,
                   COUNT(*)::int AS n_races,
                   AVG((pp.finish_position = 1)::int) FILTER (
                     WHERE pp.post_position <= 3
                   )::numeric AS inside_post_win_rate,
                   AVG((pp.finish_position = 1)::int) FILTER (
                     WHERE pp.post_position >= pp.field_size - 2
                   )::numeric AS outside_post_win_rate,
                   AVG((pp.finish_position = 1)::int) FILTER (
                     WHERE pp.call_1_position <= 2
                   )::numeric AS front_runner_win_rate,
                   AVG((pp.finish_position = 1)::int) FILTER (
                     WHERE pp.call_1_position >= pp.field_size - 2
                   )::numeric AS closer_win_rate,
                   AVG(pp.post_position) FILTER (
                     WHERE pp.finish_position = 1
                   )::numeric AS avg_winning_post_position,
                   NOW()
            FROM past_performances pp
            WHERE pp.race_date < %s
              AND pp.race_date >= %s
              AND pp.track_code IS NOT NULL
              AND pp.finish_position IS NOT NULL
            GROUP BY pp.track_code, COALESCE(pp.surface, 'unknown')
            HAVING COUNT(*) >= 50
        """, (snapshot_date, snapshot_date, snapshot_date - timedelta(days=730)))
        n = cur.rowcount
    conn.commit()
    return n


def main():
    conn = get_conn()
    snapshots = list(weekly_snapshots(date(2022, 1, 1), date(2026, 5, 17)))
    logger.info(f"Building {len(snapshots)} weekly track_bias snapshots")
    for sd in snapshots:
        try:
            n = backfill_snapshot(conn, sd)
            logger.info(f"snapshot={sd}  bias_rows={n}")
        except Exception as e:
            logger.error(f"snapshot={sd} failed: {e}")
            conn.rollback()
    conn.close()
    logger.info("track_bias_history backfill complete")


if __name__ == '__main__':
    main()
