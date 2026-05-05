"""
Par-time medians for workout-noteworthiness scoring.

Computes per-bucket median workout time over a rolling window and exposes
a helper to flag whether a single workout is "noteworthy" — defined as
either a bullet (fastest of the day at that track) OR meaningfully faster
than the bucket par.

Used by:
- model/shared/data_loader.py for the Gonzo Sauce specialist's speed
  features (noteworthy_workout_recent_14d, noteworthy_workout_count_30d)

Design:
- Bucket key = (track_code, distance_furlongs). NO surface dimension —
  only ~22 turf workouts in the dataset, statistically insignificant for
  a separate par bucket. Workouts predominantly run on the main (dirt)
  track. Limitation acknowledged; revisit if turf workout volume grows.
- 12-month rolling window (recency-weighted via window selection rather
  than EWM, since the median is the goal, not an exponential mean).
- HAVING COUNT(*) >= 30 to ensure stable medians. Sparse buckets are
  absent from the returned dict — caller uses .get() and treats `None` as
  "no signal" rather than falling back to a track-only or nationwide
  median. Silent degradation is worse than an honest absence.
- All track_conditions included (fast/sloppy/etc). Filtering to fast-only
  would cut sample sizes; the median across conditions is a reasonable
  V1 baseline. Revisit if condition-specific pars improve the model.
- Gate works (workout_type='G' or any string containing 'gate') are
  EXCLUDED. Gate works are training-behavior exercises, not speed
  exercises — including them inflates the par median and creates false-
  noteworthy flags on average breezes. Breeze ('B') and handily ('H')
  workouts are included.
"""
from __future__ import annotations
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Public API: caller's noteworthy threshold. A workout is "speed-noteworthy"
# if it is at least this many seconds FASTER than the bucket par (median).
# 1.0 second at typical workout distances (3-5f, ~37-62s par) is a ~2-3%
# improvement — meaningful but not extreme.
#
# TUNABLE: calibrate post-training based on noteworthy_workout_recent_14d
# feature firing rate. Target: 5-30% of starters flag as noteworthy.
#   <5%  → loosen threshold (e.g., 0.6-0.8s)
#   >30% → tighten threshold (e.g., 1.3-1.5s)
DEFAULT_SPEED_THRESHOLD_SEC = 1.0


def compute_workout_pars(
    conn,
    window_months: int = 12,
    min_sample: int = 30,
) -> dict[tuple[str, float], float]:
    """
    Build per-bucket par medians from the workouts table.

    Returns a dict keyed by (track_code, distance_furlongs_rounded_1dp)
    mapping to the median workout_time in seconds for that bucket over the
    last `window_months`. Sparse buckets (count < min_sample) are NOT
    included — caller must treat absence as "no signal."

    Logs total bucket count, dense (par-computed) count, and sparse count.
    """
    sql = """
        SELECT
          track_code,
          ROUND(distance_furlongs::numeric, 1) AS dist_round,
          COUNT(*) AS n_workouts,
          percentile_cont(0.5) WITHIN GROUP (ORDER BY workout_time)
            AS median_time
        FROM workouts
        WHERE workout_time IS NOT NULL
          AND workout_time > 0
          AND workout_date >= CURRENT_DATE - (%s || ' months')::interval
          AND (
            workout_type IS NULL
            OR (
              LOWER(workout_type) NOT LIKE '%%gate%%'
              AND LOWER(workout_type) != 'g'
            )
          )
        GROUP BY track_code, ROUND(distance_furlongs::numeric, 1)
        HAVING COUNT(*) >= %s
    """
    # Caller's connection uses RealDictCursor (see data_loader._get_conn),
    # so fetchall/fetchone return dict-like rows. Access by named alias only.
    with conn.cursor() as cur:
        cur.execute(sql, (str(window_months), min_sample))
        dense_rows = cur.fetchall()

        # Total bucket count (dense + sparse) for visibility.
        cur.execute(
            """
            SELECT COUNT(*) AS total_n FROM (
                SELECT track_code, ROUND(distance_furlongs::numeric, 1) AS dist_round
                FROM workouts
                WHERE workout_date >= CURRENT_DATE - (%s || ' months')::interval
                GROUP BY track_code, ROUND(distance_furlongs::numeric, 1)
            ) t
            """,
            (str(window_months),),
        )
        total_buckets = int(cur.fetchone()['total_n'])

    par_dict: dict[tuple[str, float], float] = {}
    for row in dense_rows:
        track_code = row['track_code']
        distance = float(row['dist_round'])
        median_time = float(row['median_time'])
        par_dict[(track_code, distance)] = median_time

    sparse_count = total_buckets - len(par_dict)
    logger.info(
        f"par_times: {total_buckets} total buckets, "
        f"{len(par_dict)} dense (≥{min_sample} samples, par-computed), "
        f"{sparse_count} sparse (no signal)"
    )

    return par_dict


def is_noteworthy_workout(
    workout_row: dict,
    par_dict: dict[tuple[str, float], float],
    speed_threshold_sec: float = DEFAULT_SPEED_THRESHOLD_SEC,
) -> bool:
    """
    Flag a single workout as noteworthy.

    Two independent criteria — either qualifies:
      1. Bullet flag (was the fastest workout at the track that day)
      2. Speed-vs-par (workout_time at least `speed_threshold_sec` seconds
         faster than the bucket median)

    Returns False if par is unknown for the bucket (no signal — caller
    sees a clean False, no silent fallback). The improving-times pattern
    (3+ workouts in 30d with descending times) needs horse history and is
    handled by the caller (data_loader), NOT here.

    `workout_row` is expected to have keys: is_bullet, track_code,
    distance_furlongs, workout_time. Missing values short-circuit to False
    on the speed-vs-par branch but bullet is checked first.
    """
    if workout_row.get('is_bullet'):
        return True

    track_code = workout_row.get('track_code')
    distance = workout_row.get('distance_furlongs')
    workout_time = workout_row.get('workout_time')

    if track_code is None or distance is None or workout_time is None:
        return False

    distance_key = round(float(distance), 1)
    par = par_dict.get((track_code, distance_key))
    if par is None:
        return False

    return float(workout_time) < par - speed_threshold_sec
