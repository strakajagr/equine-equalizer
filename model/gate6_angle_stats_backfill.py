"""Gate 6 §F-angles — angle_stats_history AS-OF snapshot backfill.

Populates angle_stats_history with weekly snapshots of (trainer × angle ×
track) win rates from results history. Currently angle_stats_history has
3 days of data; this backfills 4+ years.

Angles computed (extensible — start with the high-signal ones from
backend/services/feature_engineering_service.py):
  - first_time_lasix
  - layoff_60d (returning from 60+ day layoff)
  - class_drop (today's purse < 85% of last race's purse)
  - first_time_blinkers (would require entries.blinkers_first_time which
    is CONSTANT-FALSE per Gate 5 census — SKIP for now)

For each Sunday in 2022-01-02 → 2026-05-17, per (trainer_name, angle, track_code):
  wins = COUNT where horse fired with that angle at that track AND won
  starts = COUNT where horse fired with that angle at that track
"""
import logging
import os
from datetime import date, timedelta
import json

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


def backfill_first_time_lasix(conn, snapshot_date: date):
    """Snapshot: (trainer × track) win rate when horse fires with lasix_first_time=TRUE.
    Uses past_performances joined to results on (horse_id, race_date, track_code, race_number)."""
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM angle_stats_history WHERE snapshot_date = %s AND angle_name = 'first_time_lasix'",
            (snapshot_date,),
        )
        cur.execute("""
            INSERT INTO angle_stats_history (angle_name, trainer_name, track_code,
                                              wins, starts, snapshot_date, created_at)
            SELECT 'first_time_lasix' AS angle_name,
                   pp.trainer_name,
                   pp.track_code,
                   COUNT(*) FILTER (WHERE pp.finish_position = 1)::int AS wins,
                   COUNT(*)::int AS starts,
                   %s::date AS snapshot_date,
                   NOW() AS created_at
            FROM past_performances pp
            WHERE pp.race_date < %s
              AND pp.race_date >= %s
              AND pp.trainer_name IS NOT NULL
              AND pp.lasix_first_time = TRUE
            GROUP BY pp.trainer_name, pp.track_code
            HAVING COUNT(*) >= 3
        """, (snapshot_date, snapshot_date, snapshot_date - timedelta(days=730)))
        n = cur.rowcount
    conn.commit()
    return n


def backfill_layoff_60d(conn, snapshot_date: date):
    """Snapshot: (trainer × track) win rate for horses returning from 60+ day layoff."""
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM angle_stats_history WHERE snapshot_date = %s AND angle_name = 'layoff_60d'",
            (snapshot_date,),
        )
        cur.execute("""
            INSERT INTO angle_stats_history (angle_name, trainer_name, track_code,
                                              wins, starts, snapshot_date, created_at)
            SELECT 'layoff_60d' AS angle_name,
                   pp.trainer_name, pp.track_code,
                   COUNT(*) FILTER (WHERE pp.finish_position = 1)::int AS wins,
                   COUNT(*)::int AS starts,
                   %s::date AS snapshot_date, NOW() AS created_at
            FROM past_performances pp
            WHERE pp.race_date < %s
              AND pp.race_date >= %s
              AND pp.trainer_name IS NOT NULL
              AND pp.days_since_last_race >= 60
            GROUP BY pp.trainer_name, pp.track_code
            HAVING COUNT(*) >= 3
        """, (snapshot_date, snapshot_date, snapshot_date - timedelta(days=730)))
        n = cur.rowcount
    conn.commit()
    return n


def backfill_class_drop(conn, snapshot_date: date):
    """Snapshot: (trainer × track) win rate for horses dropping in class.

    Computes class drop on the fly by comparing each PP's purse to the
    horse's PREVIOUS PP's purse — joining the same horse_id earlier-race
    via LATERAL.
    """
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM angle_stats_history WHERE snapshot_date = %s AND angle_name = 'class_drop'",
            (snapshot_date,),
        )
        cur.execute("""
            INSERT INTO angle_stats_history (angle_name, trainer_name, track_code,
                                              wins, starts, snapshot_date, created_at)
            SELECT 'class_drop' AS angle_name,
                   pp.trainer_name, pp.track_code,
                   COUNT(*) FILTER (WHERE pp.finish_position = 1)::int AS wins,
                   COUNT(*)::int AS starts,
                   %s::date AS snapshot_date, NOW() AS created_at
            FROM past_performances pp
            JOIN LATERAL (
                SELECT prev.purse FROM past_performances prev
                WHERE prev.horse_id = pp.horse_id AND prev.race_date < pp.race_date
                ORDER BY prev.race_date DESC LIMIT 1
            ) prev ON TRUE
            WHERE pp.race_date < %s
              AND pp.race_date >= %s
              AND pp.trainer_name IS NOT NULL
              AND pp.purse IS NOT NULL AND prev.purse IS NOT NULL
              AND pp.purse < 0.85 * prev.purse
            GROUP BY pp.trainer_name, pp.track_code
            HAVING COUNT(*) >= 3
        """, (snapshot_date, snapshot_date, snapshot_date - timedelta(days=730)))
        n = cur.rowcount
    conn.commit()
    return n


def backfill_first_off_claim(conn, snapshot_date: date):
    """Trainer × track win rate when horse fires 1st off a claim.

    Detected: prior PP had was_claimed=TRUE (the horse was claimed
    in that prior race). The "1st off claim" is the FIRST race after
    being claimed by this trainer.
    """
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM angle_stats_history WHERE snapshot_date = %s AND angle_name = 'first_off_claim'",
            (snapshot_date,),
        )
        cur.execute("""
            INSERT INTO angle_stats_history (angle_name, trainer_name, track_code,
                                              wins, starts, snapshot_date, created_at)
            SELECT 'first_off_claim' AS angle_name,
                   pp.trainer_name, pp.track_code,
                   COUNT(*) FILTER (WHERE pp.finish_position = 1)::int AS wins,
                   COUNT(*)::int AS starts,
                   %s::date, NOW()
            FROM past_performances pp
            JOIN LATERAL (
                SELECT prev.was_claimed, prev.trainer_name AS prev_trainer
                FROM past_performances prev
                WHERE prev.horse_id = pp.horse_id AND prev.race_date < pp.race_date
                ORDER BY prev.race_date DESC LIMIT 1
            ) prev ON TRUE
            WHERE pp.race_date < %s
              AND pp.race_date >= %s
              AND pp.trainer_name IS NOT NULL
              AND prev.was_claimed = TRUE
              AND prev.prev_trainer IS DISTINCT FROM pp.trainer_name
            GROUP BY pp.trainer_name, pp.track_code
            HAVING COUNT(*) >= 3
        """, (snapshot_date, snapshot_date, snapshot_date - timedelta(days=730)))
        n = cur.rowcount
    conn.commit()
    return n


def backfill_second_off_layoff(conn, snapshot_date: date):
    """Trainer × track win rate on 2nd start back from a 60+d layoff.

    Detected: prior PP had days_since_last_race >= 60 AND days_since
    between THIS race and prior is < 60 (i.e., a normal turnaround
    after returning from layoff in the previous race).
    """
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM angle_stats_history WHERE snapshot_date = %s AND angle_name = 'second_off_layoff'",
            (snapshot_date,),
        )
        cur.execute("""
            INSERT INTO angle_stats_history (angle_name, trainer_name, track_code,
                                              wins, starts, snapshot_date, created_at)
            SELECT 'second_off_layoff' AS angle_name,
                   pp.trainer_name, pp.track_code,
                   COUNT(*) FILTER (WHERE pp.finish_position = 1)::int AS wins,
                   COUNT(*)::int AS starts,
                   %s::date, NOW()
            FROM past_performances pp
            JOIN LATERAL (
                SELECT prev.days_since_last_race
                FROM past_performances prev
                WHERE prev.horse_id = pp.horse_id AND prev.race_date < pp.race_date
                ORDER BY prev.race_date DESC LIMIT 1
            ) prev ON TRUE
            WHERE pp.race_date < %s
              AND pp.race_date >= %s
              AND pp.trainer_name IS NOT NULL
              AND prev.days_since_last_race >= 60
              AND pp.days_since_last_race < 60
            GROUP BY pp.trainer_name, pp.track_code
            HAVING COUNT(*) >= 3
        """, (snapshot_date, snapshot_date, snapshot_date - timedelta(days=730)))
        n = cur.rowcount
    conn.commit()
    return n


def backfill_blinkers_on(conn, snapshot_date: date):
    """Trainer × track win rate when horse fires with blinkers_on=TRUE."""
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM angle_stats_history WHERE snapshot_date = %s AND angle_name = 'blinkers_on'",
            (snapshot_date,),
        )
        cur.execute("""
            INSERT INTO angle_stats_history (angle_name, trainer_name, track_code,
                                              wins, starts, snapshot_date, created_at)
            SELECT 'blinkers_on' AS angle_name,
                   pp.trainer_name, pp.track_code,
                   COUNT(*) FILTER (WHERE pp.finish_position = 1)::int AS wins,
                   COUNT(*)::int AS starts,
                   %s::date, NOW()
            FROM past_performances pp
            WHERE pp.race_date < %s
              AND pp.race_date >= %s
              AND pp.trainer_name IS NOT NULL
              AND pp.blinkers_on = TRUE
            GROUP BY pp.trainer_name, pp.track_code
            HAVING COUNT(*) >= 3
        """, (snapshot_date, snapshot_date, snapshot_date - timedelta(days=730)))
        n = cur.rowcount
    conn.commit()
    return n


def backfill_surface_switch(conn, snapshot_date: date):
    """Trainer × track win rate when horse switches surface vs last race."""
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM angle_stats_history WHERE snapshot_date = %s AND angle_name = 'surface_switch'",
            (snapshot_date,),
        )
        cur.execute("""
            INSERT INTO angle_stats_history (angle_name, trainer_name, track_code,
                                              wins, starts, snapshot_date, created_at)
            SELECT 'surface_switch' AS angle_name,
                   pp.trainer_name, pp.track_code,
                   COUNT(*) FILTER (WHERE pp.finish_position = 1)::int AS wins,
                   COUNT(*)::int AS starts,
                   %s::date, NOW()
            FROM past_performances pp
            JOIN LATERAL (
                SELECT prev.surface
                FROM past_performances prev
                WHERE prev.horse_id = pp.horse_id AND prev.race_date < pp.race_date
                ORDER BY prev.race_date DESC LIMIT 1
            ) prev ON TRUE
            WHERE pp.race_date < %s
              AND pp.race_date >= %s
              AND pp.trainer_name IS NOT NULL
              AND pp.surface IS NOT NULL AND prev.surface IS NOT NULL
              AND LOWER(pp.surface) <> LOWER(prev.surface)
            GROUP BY pp.trainer_name, pp.track_code
            HAVING COUNT(*) >= 3
        """, (snapshot_date, snapshot_date, snapshot_date - timedelta(days=730)))
        n = cur.rowcount
    conn.commit()
    return n


def main():
    conn = get_conn()
    snapshots = list(weekly_snapshots(date(2022, 1, 1), date(2026, 5, 17)))
    logger.info(f"Building {len(snapshots)} weekly angle snapshots (7 angles)")
    for sd in snapshots:
        try:
            ftl = backfill_first_time_lasix(conn, sd)
            l60 = backfill_layoff_60d(conn, sd)
            cd  = backfill_class_drop(conn, sd)
            foc = backfill_first_off_claim(conn, sd)
            sol = backfill_second_off_layoff(conn, sd)
            bon = backfill_blinkers_on(conn, sd)
            sws = backfill_surface_switch(conn, sd)
            logger.info(f"snapshot={sd}  ftl={ftl:>4}  layoff60={l60:>4}  class_drop={cd:>4}  "
                        f"1off_claim={foc:>3}  2off_layoff={sol:>3}  blinkers_on={bon:>4}  surface_switch={sws:>4}")
        except Exception as e:
            logger.error(f"snapshot={sd} failed: {e}")
            conn.rollback()
    conn.close()
    logger.info("angle_stats_history backfill complete (7 angles)")


if __name__ == '__main__':
    main()
