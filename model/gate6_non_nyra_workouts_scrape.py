"""Gate 6 §1 — non-NYRA workouts per-horse HRN scrape.

For each unique horse that raced at CD/GP/KEE/MTH/OP/PIM/SA/DMR during
Jan 2024 → Aug 2025, fetch their HRN profile workout history and insert
workouts within the gap window. Rate-limited (~1-2 req/sec).
"""
import logging
import os
import json
import time
import sys
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


# Path setup for HRN scraper import — direct file load to avoid the
# data_sources/__init__.py which chains in HRNScraper (playwright-deps not in
# training image).
sys.path.insert(0, '/app')
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "hrn_workout_scraper", "/app/services/data_sources/hrn_workout_scraper.py"
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
HRNWorkoutScraper = _mod.HRNWorkoutScraper

NON_NYRA_TRACKS = ['CD', 'GP', 'KEE', 'MTH', 'OP', 'PIM', 'SA', 'DMR']
GAP_START = date(2024, 1, 1)
GAP_END = date(2025, 8, 31)
RATE_LIMIT_SEC = 1.0  # pause between HRN fetches


def get_target_horses(conn):
    """Unique horses that raced at non-NYRA tracks during the gap window."""
    track_list = "','".join(NON_NYRA_TRACKS)
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT DISTINCT h.horse_id, h.horse_name
            FROM horses h
            JOIN past_performances pp ON pp.horse_id = h.horse_id
            WHERE pp.track_code IN ('{track_list}')
              AND pp.race_date BETWEEN %s AND %s
            ORDER BY h.horse_name
        """, (GAP_START, GAP_END))
        return [dict(r) for r in cur.fetchall()]


def insert_workout(conn, w):
    """Direct workouts INSERT — natural key UPSERT."""
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO workouts (
                horse_id, workout_date, track_code, distance_furlongs,
                workout_time, workout_type, is_bullet, rank_on_day,
                total_works_on_day, track_condition
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (horse_id, workout_date, track_code, distance_furlongs)
            DO NOTHING
        """, (
            w.get('horse_id'), w.get('workout_date'), w.get('track_code'),
            w.get('distance_furlongs'), w.get('workout_time'),
            w.get('workout_type'), w.get('is_bullet', False),
            w.get('rank_on_day'), w.get('total_works_on_day'),
            w.get('track_condition'),
        ))


def main():
    logger.info(f"Non-NYRA workouts scrape: {GAP_START} → {GAP_END}, tracks={NON_NYRA_TRACKS}")
    conn = get_conn()
    horses = get_target_horses(conn)
    logger.info(f"Target horses: {len(horses):,}")

    scraper = HRNWorkoutScraper()

    n_processed = 0
    n_workouts_inserted = 0
    n_errors = 0
    t_start = time.time()

    for h in horses:
        try:
            workouts = scraper.fetch_workouts(
                horse_name=h['horse_name'],
                horse_id=h['horse_id'],
                cutoff_start=GAP_START,
            )
            inserted = 0
            for w in workouts:
                if not w.get('workout_date'):
                    continue
                wd = w['workout_date']
                if wd < GAP_START or wd > GAP_END:
                    continue
                try:
                    insert_workout(conn, w)
                    inserted += 1
                except Exception:
                    pass
            n_workouts_inserted += inserted
            n_processed += 1
            if n_processed % 50 == 0:
                conn.commit()
                elapsed = time.time() - t_start
                rate = n_processed / elapsed if elapsed > 0 else 0
                eta = (len(horses) - n_processed) / rate if rate > 0 else 0
                logger.info(f"progress: {n_processed:,}/{len(horses):,} horses "
                            f"({100*n_processed/len(horses):.1f}%)  "
                            f"workouts={n_workouts_inserted:,}  "
                            f"rate={rate:.1f}/sec  eta={eta/60:.0f}min")
        except Exception as e:
            n_errors += 1
            if n_errors <= 20:
                logger.warning(f"horse={h['horse_name']!r} error: {e}")
        time.sleep(RATE_LIMIT_SEC)

    conn.commit()
    conn.close()
    logger.info(f"Done. processed={n_processed:,} workouts_inserted={n_workouts_inserted:,} "
                f"errors={n_errors}")


if __name__ == '__main__':
    main()
