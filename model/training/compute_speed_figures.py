#!/usr/bin/env python3
"""
Equine Equalizer — Speed Figure Computation Pipeline

Computes Beyer-equivalent speed figures with:
  - Track condition adjustment (fast/sloppy/muddy/etc.)
  - Lengths-behind adjustment for non-winners
  - Par times from FAST TRACK ONLY
  - Daily track variant normalization
  - Beyer-scale normalization (0-130, median ~80)

Usage: python compute_speed_figures.py

REPAIR-4 SUBSTRATE-LEAKAGE MARKER (Step C.3, deferred to REPAIR-5+):
  Par times (Step 2 query) + Beyer normalization constants (Step 6
  median+std) are computed from the FULL past_performances corpus then
  applied uniformly to every row — including rows from race dates that
  PRECEDE the data used in the aggregate. This is substrate-leakage of
  AGGREGATE statistics into earlier rows: a 2022 horse's computed_speed_
  figure is normalized against par times that include 2024-2026 races.

  For PRODUCTION INFERENCE at race-fire-time this is substrate-mostly
  acceptable — figures on past PPs reflect par times up to roughly
  yesterday. For TRAINING the leakage is substrate-actual: models trained
  on 2022-2024 data see speed figures normalized against 2025-2026 data.

  Substrate-correct fix (rolling-window par times per race_date) is a
  substrate-substantial pipeline rewrite. Deferred to REPAIR-5 when
  retrain rules re-enable + 39 contaminated models get retrained. Until
  then, retrain rules REMAIN DISABLED (UNFUCK-3 Step A) so this leakage
  class cannot propagate into new model versions.
"""

import logging
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..'
))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..'
))

from shared.db import get_db, execute_query, execute_one

# Track condition speed adjustments (in fifths of a second)
# Applied to normalize all times to fast/firm equivalent.
# Based on actual data: fast avg=82.86, sloppy=85.03, muddy=84.68
CONDITION_ADJUSTMENTS = {
    # Dirt conditions
    'fast': 0.0,
    'fast(sealed)': 0.0,
    'good': 2.0,
    'good(sealed)': 3.0,
    'sloppy': 1.0,
    'sloppy(sealed)': 1.5,
    'muddy': 5.0,
    'muddy(sealed)': 3.0,
    'wetfast': 0.5,
    'wetfast(sealed)': 1.0,
    'heavy': 8.0,
    'frozen': 3.0,
    # Turf conditions
    'firm': 0.0,
    'yielding': 5.0,
    'soft': 7.0,
}

# Fast/firm conditions for par time computation
FAST_CONDITIONS = {
    'fast', 'fast(sealed)', 'firm', 'wetfast'
}


def main():
    logger.info("=" * 50)
    logger.info("  Speed Figure Pipeline (with condition adj)")
    logger.info("=" * 50)

    with get_db() as conn:
        # Step 1: Schema
        logger.info("Step 1: Ensuring schema columns...")
        with conn.cursor() as cur:
            cur.execute("""
                ALTER TABLE past_performances
                ADD COLUMN IF NOT EXISTS computed_speed_figure
                    DECIMAL(5,1),
                ADD COLUMN IF NOT EXISTS speed_rating_raw
                    DECIMAL(5,1),
                ADD COLUMN IF NOT EXISTS track_variant
                    DECIMAL(5,1)
            """)
        conn.commit()

        # Step 2: Par times (FAST TRACK ONLY)
        logger.info("Step 2: Building par times (fast/firm only)...")
        fast_list = "', '".join(FAST_CONDITIONS)
        par_rows = execute_query(
            conn,
            f"""SELECT
                  track_code,
                  distance_furlongs,
                  surface,
                  PERCENTILE_CONT(0.5) WITHIN GROUP
                    (ORDER BY final_time) as par_time,
                  COUNT(*) as sample_count
                FROM past_performances
                WHERE finish_position = 1
                  AND final_time > 0
                  AND final_time < 200
                  AND distance_furlongs BETWEEN 3.5 AND 12.0
                  AND surface IS NOT NULL
                  AND track_condition IN ('{fast_list}')
                GROUP BY track_code, distance_furlongs, surface
                HAVING COUNT(*) >= 5"""
        )
        par_map = {}
        for r in par_rows:
            key = (
                r['track_code'],
                float(r['distance_furlongs']),
                r['surface']
            )
            par_map[key] = float(r['par_time'])
        logger.info(f"Built {len(par_map)} par time buckets")
        for key in sorted(par_map.keys())[:8]:
            logger.info(
                f"  {key[0]} {key[1]}f {key[2]}: "
                f"{par_map[key]:.2f}s"
            )

        # Step 3: Compute speed ratings with condition + lengths adj
        logger.info(
            "Step 3: Computing condition-adjusted speed ratings..."
        )
        chunk_size = 5000
        offset = 0
        total_updated = 0

        LENGTHS_PER_SECOND = 5.0

        while True:
            rows = execute_query(
                conn,
                """SELECT pp_id, track_code,
                          distance_furlongs, surface,
                          track_condition, final_time,
                          finish_position, lengths_behind,
                          fraction_1, call_1_lengths,
                          fraction_2, call_2_lengths
                   FROM past_performances
                   WHERE final_time > 0
                     AND final_time < 200
                     AND finish_position IS NOT NULL
                     AND finish_position < 90
                     AND distance_furlongs IS NOT NULL
                     AND surface IS NOT NULL
                   ORDER BY pp_id
                   LIMIT %s OFFSET %s""",
                (chunk_size, offset)
            )
            if not rows:
                break

            updates = []
            for r in rows:
                key = (
                    r['track_code'],
                    float(r['distance_furlongs']),
                    r['surface']
                )
                par = par_map.get(key)
                if par is None:
                    continue

                ft = float(r['final_time'])
                cond = r['track_condition'] or 'fast'

                # Condition adjustment: normalize to fast equiv
                cond_adj = CONDITION_ADJUSTMENTS.get(cond, 0.0)
                adjusted_time = ft - (cond_adj / 5.0)

                # Lengths behind adjustment for non-winners
                # 1 length ≈ 0.2 seconds
                lb = float(r['lengths_behind'] or 0)
                if r['finish_position'] != 1 and lb > 0:
                    adjusted_time += lb * 0.2

                # Speed rating in fifths vs par
                raw = (par - adjusted_time) * 5.0
                raw = max(-50.0, min(50.0, raw))

                # Pace figures
                early_pace = None
                late_pace = None
                pdelta = None
                f1 = r['fraction_1']
                cl1 = r['call_1_lengths']
                f2 = r['fraction_2']
                cl2 = r['call_2_lengths']
                if f1 is not None and cl1 is not None:
                    horse_frac1_est = (
                        float(f1) + float(cl1) / LENGTHS_PER_SECOND
                    )
                    early_pace = round(horse_frac1_est, 2)
                    if f2 is not None and cl2 is not None:
                        horse_frac2_est = (
                            float(f2) + float(cl2) / LENGTHS_PER_SECOND
                        )
                        horse_final_est = (
                            ft + lb / LENGTHS_PER_SECOND
                        )
                        late_pace = round(
                            horse_final_est - horse_frac2_est, 2
                        )
                        pdelta = round(late_pace - early_pace, 2)

                updates.append((
                    round(raw, 1),
                    early_pace, late_pace, pdelta,
                    str(r['pp_id'])
                ))

            if updates:
                for attempt in range(3):
                    try:
                        with conn.cursor() as cur:
                            from psycopg2.extras import execute_batch
                            execute_batch(
                                cur,
                                """UPDATE past_performances
                                   SET speed_rating_raw = %s,
                                       early_pace_figure = %s,
                                       late_pace_figure = %s,
                                       pace_delta = %s
                                   WHERE pp_id = %s""",
                                updates,
                                page_size=500
                            )
                        conn.commit()
                        total_updated += len(updates)
                        break
                    except Exception as e:
                        conn.rollback()
                        if attempt < 2:
                            import time
                            time.sleep(2 + attempt * 3)
                        else:
                            logger.warning(
                                f"Skipped chunk at {offset}: {e}"
                            )

            offset += chunk_size
            if offset % 20000 == 0:
                logger.info(
                    f"  {offset:,} rows, "
                    f"{total_updated:,} updated"
                )

        logger.info(f"Raw ratings: {total_updated:,} updated")

        # Step 4: Daily track variants (from winners)
        logger.info("Step 4: Computing track variants...")
        variant_rows = execute_query(
            conn,
            """SELECT
                 track_code, race_date, surface,
                 AVG(speed_rating_raw) as variant,
                 COUNT(*) as race_count
               FROM past_performances
               WHERE finish_position = 1
                 AND speed_rating_raw IS NOT NULL
               GROUP BY track_code, race_date, surface
               HAVING COUNT(*) >= 3"""
        )
        variant_map = {}
        for r in variant_rows:
            key = (
                r['track_code'],
                str(r['race_date']),
                r['surface']
            )
            variant_map[key] = float(r['variant'])
        logger.info(f"Computed {len(variant_map)} daily variants")

        # Step 5: Apply variants, compute adjusted figures
        logger.info("Step 5: Applying variants...")
        offset = 0
        total_figured = 0
        all_adjusted = []

        while True:
            rows = execute_query(
                conn,
                """SELECT pp_id, track_code, race_date,
                          surface, speed_rating_raw
                   FROM past_performances
                   WHERE speed_rating_raw IS NOT NULL
                   ORDER BY pp_id
                   LIMIT %s OFFSET %s""",
                (chunk_size, offset)
            )
            if not rows:
                break

            updates = []
            for r in rows:
                key = (
                    r['track_code'],
                    str(r['race_date']),
                    r['surface']
                )
                variant = variant_map.get(key, 0.0)
                adjusted = float(r['speed_rating_raw']) - variant
                all_adjusted.append(adjusted)
                updates.append((
                    round(variant, 1),
                    round(adjusted, 2),
                    str(r['pp_id'])
                ))

            if updates:
                for attempt in range(3):
                    try:
                        with conn.cursor() as cur:
                            from psycopg2.extras import execute_batch
                            execute_batch(
                                cur,
                                """UPDATE past_performances
                                   SET track_variant = %s,
                                       computed_speed_figure = %s
                                   WHERE pp_id = %s""",
                                updates,
                                page_size=500
                            )
                        conn.commit()
                        total_figured += len(updates)
                        break
                    except Exception as e:
                        conn.rollback()
                        if attempt < 2:
                            import time
                            time.sleep(2 + attempt * 3)
                        else:
                            logger.warning(
                                f"Skipped chunk at {offset}: {e}"
                            )

            offset += chunk_size
            if offset % 20000 == 0:
                logger.info(f"  {offset:,} rows applied")

        logger.info(f"Adjusted figures: {total_figured:,}")

        # Step 6: Normalize to Beyer scale
        logger.info("Step 6: Normalizing to Beyer scale...")

        # Diagnostic: inspect speed_rating_raw distribution before norm
        raw_stats = execute_one(
            conn,
            """SELECT
                 AVG(speed_rating_raw)::float            as mean,
                 PERCENTILE_CONT(0.5) WITHIN GROUP
                   (ORDER BY speed_rating_raw)::float   as median,
                 STDDEV(speed_rating_raw)::float         as std,
                 MIN(speed_rating_raw)::float            as min_val,
                 MAX(speed_rating_raw)::float            as max_val,
                 COUNT(*)                                as cnt
               FROM past_performances
               WHERE speed_rating_raw IS NOT NULL"""
        )
        logger.info("speed_rating_raw stats (DB):")
        logger.info(f"  mean:   {float(raw_stats['mean']):.2f}")
        logger.info(f"  median: {float(raw_stats['median']):.2f}")
        logger.info(f"  std:    {float(raw_stats['std']):.2f}")
        logger.info(f"  min:    {float(raw_stats['min_val']):.2f}")
        logger.info(f"  max:    {float(raw_stats['max_val']):.2f}")
        logger.info(f"  count:  {int(raw_stats['cnt']):,}")

        import numpy as np
        arr = np.array(all_adjusted)
        logger.info("all_adjusted stats (in-memory):")
        logger.info(f"  mean:   {float(np.mean(arr)):.2f}")
        logger.info(f"  median: {float(np.median(arr)):.2f}")
        logger.info(f"  std:    {float(np.std(arr)):.2f}")
        logger.info(f"  min:    {float(np.min(arr)):.2f}")
        logger.info(f"  max:    {float(np.max(arr)):.2f}")
        logger.info(f"  count:  {len(arr):,}")

        median_fig = float(np.median(arr))
        std_fig = float(np.std(arr))
        logger.info(
            f"Pre-norm: median={median_fig:.2f}, "
            f"std={std_fig:.2f}"
        )

        with conn.cursor() as cur:
            cur.execute(
                """UPDATE past_performances
                   SET computed_speed_figure = ROUND(
                     LEAST(130, GREATEST(0,
                       (computed_speed_figure - %s) / %s
                       * 12 + 80
                     ))::numeric, 1
                   )
                   WHERE computed_speed_figure IS NOT NULL""",
                (median_fig, std_fig)
            )
        conn.commit()
        logger.info("Normalization complete")

        # Step 7: Validation
        logger.info("=" * 50)
        logger.info("  VALIDATION")
        logger.info("=" * 50)

        # Distribution
        dist = execute_query(
            conn,
            """SELECT
                 ROUND(computed_speed_figure / 5) * 5
                   as fig_bucket,
                 COUNT(*) as count
               FROM past_performances
               WHERE computed_speed_figure IS NOT NULL
               GROUP BY fig_bucket
               ORDER BY fig_bucket"""
        )
        logger.info("Figure distribution:")
        for r in dist:
            bar = '#' * min(int(r['count'] / 500), 40)
            logger.info(
                f"  {int(r['fig_bucket']):4d}: "
                f"{int(r['count']):6,} {bar}"
            )

        # Condition validation (THE KEY TEST)
        cond_val = execute_query(
            conn,
            """SELECT
                 track_condition,
                 COUNT(*) as races,
                 ROUND(AVG(computed_speed_figure)::numeric, 1)
                   as avg_figure,
                 ROUND(STDDEV(computed_speed_figure)::numeric, 1)
                   as std_figure
               FROM past_performances
               WHERE computed_speed_figure IS NOT NULL
                 AND finish_position = 1
               GROUP BY track_condition
               ORDER BY avg_figure DESC"""
        )
        logger.info("\nFigures by track condition (winners):")
        logger.info("  (Should be similar across conditions)")
        for r in cond_val:
            logger.info(
                f"  {str(r['track_condition']):18s} "
                f"avg={r['avg_figure']:5.1f} "
                f"std={r['std_figure']:5.1f} "
                f"n={int(r['races']):,}"
            )

        # Top figures
        top = execute_query(
            conn,
            """SELECT
                 h.horse_name,
                 pp.track_code,
                 pp.race_date,
                 pp.distance_furlongs,
                 pp.surface,
                 pp.computed_speed_figure,
                 pp.finish_position,
                 pp.track_condition
               FROM past_performances pp
               JOIN horses h ON h.horse_id = pp.horse_id
               WHERE pp.computed_speed_figure > 105
               ORDER BY pp.computed_speed_figure DESC
               LIMIT 20"""
        )
        logger.info("\nTop 20 speed figures:")
        for r in top:
            logger.info(
                f"  {float(r['computed_speed_figure']):5.1f} "
                f"{r['horse_name']:20s} "
                f"{r['track_code']} {r['race_date']} "
                f"{r['distance_furlongs']}f {r['surface']} "
                f"({r['track_condition']}) "
                f"fin={r['finish_position']}"
            )

        # Average by track
        track_avg = execute_query(
            conn,
            """SELECT
                 track_code,
                 ROUND(AVG(computed_speed_figure)::numeric, 1)
                   as avg_fig,
                 ROUND(MAX(computed_speed_figure)::numeric, 1)
                   as max_fig,
                 COUNT(*) as sample
               FROM past_performances
               WHERE computed_speed_figure IS NOT NULL
                 AND finish_position = 1
               GROUP BY track_code
               ORDER BY avg_fig DESC"""
        )
        logger.info("\nAverage by track (winners):")
        for r in track_avg:
            logger.info(
                f"  {r['track_code']:5s} avg={r['avg_fig']:5.1f} "
                f"max={r['max_fig']:5.1f} "
                f"n={int(r['sample']):,}"
            )

        # Final count + validation query
        final = execute_one(
            conn,
            """SELECT
                 AVG(computed_speed_figure)::float    as avg_fig,
                 MAX(computed_speed_figure)::float    as max_fig,
                 MIN(computed_speed_figure)::float    as min_fig,
                 COUNT(early_pace_figure)             as has_early_pace,
                 COUNT(late_pace_figure)              as has_late_pace
               FROM past_performances"""
        )
        logger.info(
            f"\nValidation summary:"
            f"\n  avg_fig:        {final['avg_fig']:.2f}"
            f"\n  max_fig:        {final['max_fig']:.2f}"
            f"\n  min_fig:        {final['min_fig']:.2f}"
            f"\n  has_early_pace: {int(final['has_early_pace']):,}"
            f"\n  has_late_pace:  {int(final['has_late_pace']):,}"
        )
        logger.info("  (Expected: avg 75-85, max 110-125, pace ~99%)")

    logger.info("Speed figure pipeline complete")


if __name__ == '__main__':
    main()
