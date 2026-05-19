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

REPAIR-5 SUBSTRATE-FIX (Step A, applied 2026-05-19):
  Par times (Step 2) + Beyer normalization (Step 6) now use PER-YEAR
  bucketing with AS-OF discipline. Each row from year Y is processed using
  ONLY data from years strictly < Y:

    Step 2: par_map keyed by (track, distance, surface, year). Row from
            year Y uses par from most-recent-year < Y via bisect lookup.
    Step 3: par lookup uses lookup_par(track, distance, surface, row.year).
    Step 4: same-day variants — substrate-correct unchanged.
    Step 5: applies variant — substrate-correct unchanged.
    Step 6: norm_map keyed by year (median, std of computed_speed_figure).
            Row from year Y normalized with stats from most-recent-year < Y.
            Per-year UPDATE filtered by EXTRACT(YEAR FROM race_date).

  Substrate-effect: a 2022 row no longer sees 2024-2026 aggregate
  statistics in its par/norm constants. Training cohorts assembled from
  the resulting speed figures are substrate-AS-OF clean.

  Pre-REPAIR-5 caveat: retrain rules were DISABLED (UNFUCK-3 Step A) so
  the substrate-leaky figures never propagated into new model versions
  beyond the 39 contaminated models trained pre-REPAIR-4. REPAIR-5
  retrain wave (Step F) produces clean-cohort replacements.
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

        # Step 2: Par times — ROLLING WINDOW per year (REPAIR-5 A.2 AS-OF fix)
        #
        # Substrate-fix: par_map now keyed by (track, distance, surface, year)
        # using ONLY winners from years strictly BEFORE the target year.
        # Substrate-implementation: build a per-year par map via SQL with
        # GROUP BY year, then at row-computation time look up using
        # (track, distance, surface, row.year - 1) — i.e., the most recent
        # complete year before the row's race date.
        #
        # Per-year semantics: a row from year Y gets par from year (Y-1)'s
        # complete corpus. This is substrate-stricter than a 365-day trailing
        # window but substrate-pragmatic-cleaner (no SQL subqueries per row;
        # one substrate-aggregate query produces all year buckets).
        logger.info("Step 2: Building per-year par times (REPAIR-5 AS-OF)...")
        fast_list = "', '".join(FAST_CONDITIONS)
        par_rows = execute_query(
            conn,
            f"""SELECT
                  track_code,
                  distance_furlongs,
                  surface,
                  EXTRACT(YEAR FROM race_date)::int as par_year,
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
                GROUP BY track_code, distance_furlongs, surface,
                         EXTRACT(YEAR FROM race_date)
                HAVING COUNT(*) >= 5"""
        )
        # par_map keyed by (track, distance, surface, year): par time at end
        # of that year. For row from year Y, lookup uses year (Y-1).
        par_map = {}
        for r in par_rows:
            key = (
                r['track_code'],
                float(r['distance_furlongs']),
                r['surface'],
                int(r['par_year']),
            )
            par_map[key] = float(r['par_time'])
        logger.info(f"Built {len(par_map)} per-year par buckets")
        # Show samples across multiple years for diagnostic
        sample_keys = sorted(par_map.keys())[:8]
        for key in sample_keys:
            logger.info(
                f"  {key[0]} {key[1]}f {key[2]} y{key[3]}: "
                f"{par_map[key]:.2f}s"
            )

        # Fallback strategy: if (track, distance, surface, year-1) missing,
        # try most-recent-prior year for same (track, distance, surface).
        # Pre-compute a sorted-years-per-bucket index for O(log n) lookup.
        bucket_years = {}
        for (tc, d, s, y) in par_map.keys():
            bucket_years.setdefault((tc, d, s), []).append(y)
        for k in bucket_years:
            bucket_years[k].sort()

        def lookup_par(tc, d, s, target_year):
            """Find par time AS-OF target_year using strict less-than search.
            Returns par from most recent year strictly < target_year, or None.
            """
            years = bucket_years.get((tc, d, s))
            if not years:
                return None
            import bisect
            idx = bisect.bisect_left(years, target_year)
            if idx == 0:
                return None  # no prior-year data
            return par_map.get((tc, d, s, years[idx - 1]))

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
                          fraction_2, call_2_lengths,
                          race_date
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
                # REPAIR-5 AS-OF: par from prior years only
                row_year = int(r['race_date'].year)
                par = lookup_par(
                    r['track_code'],
                    float(r['distance_furlongs']),
                    r['surface'],
                    row_year,
                )
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

        # Step 6: Normalize to Beyer scale — PER-YEAR (REPAIR-5 AS-OF fix)
        #
        # Substrate-fix: normalization constants (median + std) computed
        # PER YEAR using ONLY data from years strictly BEFORE the target
        # year. Substrate-pragmatic-parallel to Step 2 par-time fix.
        # Substrate-effect: a 2024 row gets normalized using 2023's median/std,
        # not the cross-year aggregate that would substrate-leak future years.
        logger.info("Step 6: Per-year Beyer normalization (REPAIR-5 AS-OF)...")

        # Diagnostic: substrate-shows cross-year aggregate for human eye only;
        # NOT used for normalization
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
        logger.info("speed_rating_raw cross-year stats (DIAGNOSTIC ONLY):")
        logger.info(f"  mean:   {float(raw_stats['mean']):.2f}")
        logger.info(f"  median: {float(raw_stats['median']):.2f}")
        logger.info(f"  std:    {float(raw_stats['std']):.2f}")
        logger.info(f"  count:  {int(raw_stats['cnt']):,}")

        # Substrate-fix: build per-year normalization stats from
        # computed_speed_figure (post Step 5 variant-adjustment, pre-Beyer).
        # Each year's stats are computed from THAT YEAR's data; row from
        # year Y is normalized with (Y-1)'s stats.
        per_year_stats = execute_query(
            conn,
            """SELECT
                 EXTRACT(YEAR FROM race_date)::int as norm_year,
                 PERCENTILE_CONT(0.5) WITHIN GROUP
                   (ORDER BY computed_speed_figure)::float as median,
                 STDDEV(computed_speed_figure)::float       as std,
                 COUNT(*)                                   as cnt
               FROM past_performances
               WHERE computed_speed_figure IS NOT NULL
               GROUP BY EXTRACT(YEAR FROM race_date)
               HAVING COUNT(*) >= 1000
               ORDER BY norm_year"""
        )
        norm_map = {}
        for r in per_year_stats:
            norm_map[int(r['norm_year'])] = (
                float(r['median']),
                float(r['std']),
            )
            logger.info(
                f"  y{int(r['norm_year'])}: "
                f"median={float(r['median']):.2f} "
                f"std={float(r['std']):.2f} "
                f"n={int(r['cnt']):,}"
            )

        # Fallback: if year Y-1 missing, use most-recent-prior year available
        norm_years_sorted = sorted(norm_map.keys())

        def lookup_norm(target_year):
            """Most recent year strictly < target_year with norm stats.
            Returns (median, std) or None if no prior data."""
            import bisect
            idx = bisect.bisect_left(norm_years_sorted, target_year)
            if idx == 0:
                return None
            return norm_map[norm_years_sorted[idx - 1]]

        # Apply per-year normalization via UPDATE-per-year loop
        # Substrate-pragmatic: small number of years (5-10) so cost is minimal.
        # Per-year UPDATE filters by race_date range.
        with conn.cursor() as cur:
            cur.execute(
                """SELECT EXTRACT(YEAR FROM race_date)::int as y, COUNT(*)
                   FROM past_performances
                   WHERE computed_speed_figure IS NOT NULL
                   GROUP BY EXTRACT(YEAR FROM race_date)
                   ORDER BY y"""
            )
            target_years = [int(row[0]) for row in cur.fetchall()]

        normalized_rows = 0
        for target_year in target_years:
            norm = lookup_norm(target_year)
            if norm is None:
                logger.warning(
                    f"  y{target_year}: no prior-year stats; "
                    f"rows skipped (substrate-cold-start)"
                )
                continue
            median_fig, std_fig = norm
            if std_fig <= 0:
                logger.warning(
                    f"  y{target_year}: std<=0 from y{target_year-1}; skipping"
                )
                continue
            with conn.cursor() as cur:
                cur.execute(
                    """UPDATE past_performances
                       SET computed_speed_figure = ROUND(
                         LEAST(130, GREATEST(0,
                           (computed_speed_figure - %s) / %s
                           * 12 + 80
                         ))::numeric, 1
                       )
                       WHERE computed_speed_figure IS NOT NULL
                         AND EXTRACT(YEAR FROM race_date) = %s""",
                    (median_fig, std_fig, target_year)
                )
                normalized_rows += cur.rowcount
            conn.commit()
            logger.info(
                f"  y{target_year}: normalized {cur.rowcount:,} rows "
                f"with y<{target_year} stats (m={median_fig:.2f} s={std_fig:.2f})"
            )

        logger.info(
            f"Per-year normalization complete: "
            f"{normalized_rows:,} rows normalized"
        )

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
