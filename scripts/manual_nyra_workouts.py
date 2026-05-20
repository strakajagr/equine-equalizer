#!/usr/bin/env python3
"""Manual NYRA workouts ingestion script.

Daily Tony-manual ingestion of NYRA workouts from www.nyra.com into the
workouts table. Replaces (or supplements) the equine-nyra-workouts
Lambda cron when manual control is needed (e.g., off-cycle re-fetch,
backfill specific date ranges, fetch just one track).

Architecture:
  - Reuses nyra-workouts/handler.py primitives (fetch_track_page +
    parse_nyra_html) for fetch/parse — same code path as production
    Lambda cron at 16:00 UTC daily.
  - Writes directly to DB via WorkoutRepository.insert_workout (UPSERT
    on UNIQUE(horse_id, workout_date, track_code, distance_furlongs)).
    Bypasses the S3 + ingestion-Lambda hop that the Lambda flow uses.
    This mirrors scripts/backfill_d2.py's existing _backfill_workouts
    pattern.

NYRA tracks (NYRA_TRACKS dict on handler.py):
  SAR — Saratoga
  BEL — Belmont Park
  AQU — Aqueduct

Usage:
  # Dry-run all NYRA tracks for one date (default; no DB writes)
  python3 scripts/manual_nyra_workouts.py --start-date 2026-05-10 --end-date 2026-05-10

  # Execute (writes to DB)
  python3 scripts/manual_nyra_workouts.py --start-date 2026-05-10 --end-date 2026-05-10 --execute

  # Subset of tracks
  python3 scripts/manual_nyra_workouts.py --start-date 2026-05-10 --end-date 2026-05-10 \\
      --execute --tracks SAR,BEL

  # Date range
  python3 scripts/manual_nyra_workouts.py --start-date 2026-05-01 --end-date 2026-05-10 --execute

Daily operational pattern:
  Tony runs this script daily (post-NYRA-workouts-publish-time) to
  ingest NYRA workouts. NYRA workouts publish to www.nyra.com at
  variable times; check NYRA's site for current-day data before
  running.

Logs: scripts/logs/manual_nyra_workouts_<UTC-timestamp>[_dryrun].log
      + stdout.

Idempotency:
  WorkoutRepository.insert_workout UPSERTs on the natural key
  (horse_id, workout_date, track_code, distance_furlongs). Re-running
  the script on the same date overwrites existing rows with
  re-extracted values; safe.
"""
from __future__ import annotations
import argparse
import json
import logging
import os
import sys
import traceback
from datetime import date, datetime, timedelta, timezone

import boto3

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "backend"))
sys.path.insert(0, os.path.join(REPO_ROOT, "backend/lambdas/nyra-workouts"))


# DB credential setup — same pattern as backfill_d2.py / backfill_d3.py.
# Tony's local env DB_SECRET_ARN points at a different project's secret;
# set DATABASE_URL explicitly from equine-equalizer/db-credentials BEFORE
# any shared.db import.
def _setup_database_url():
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    sec = json.loads(
        sm.get_secret_value(
            SecretId="equine-equalizer/db-credentials"
        )["SecretString"]
    )
    os.environ["DATABASE_URL"] = (
        f"postgresql://{sec['username']}:{sec['password']}"
        f"@{sec['host']}:{sec['port']}/{sec['dbname']}"
    )


_setup_database_url()


from shared.db import get_db  # noqa: E402
from shared.horse_naming import normalize_horse_name  # noqa: E402
from repositories.horse_repository import HorseRepository  # noqa: E402
from repositories.workout_repository import WorkoutRepository  # noqa: E402

import handler as nyra_handler  # noqa: E402


def _setup_logging(dry_run: bool) -> str:
    logs_dir = os.path.join(REPO_ROOT, "scripts", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = "_dryrun" if dry_run else ""
    log_path = os.path.join(
        logs_dir, f"manual_nyra_workouts_{ts}{suffix}.log"
    )
    fmt = "%(asctime)s %(levelname)s %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_path),
        ],
    )
    return log_path


def _date_range(start: date, end: date):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


def _fetch_and_parse(track_code: str, target_iso: str):
    """Fetch + parse one track's workouts. Returns (rows, stats).
    Raises on fetch/parse failure (caller's per-track try/except
    isolates)."""
    track_slug = nyra_handler.NYRA_TRACKS[track_code]
    url, html = nyra_handler.fetch_track_page(track_slug, target_iso)
    rows, stats = nyra_handler.parse_nyra_html(
        html, track_code, target_iso
    )
    return rows, stats


def _upsert_workouts(rows, track_code: str):
    """Write workout rows to DB via WorkoutRepository UPSERT.
    Mirrors scripts/backfill_d2.py:279-330 _backfill_workouts DB-write
    block. Returns (inserted, skipped, errors_list)."""
    inserted = 0
    skipped = 0
    errors = []
    with get_db() as conn:
        horse_repo = HorseRepository(conn)
        workout_repo = WorkoutRepository(conn)
        for row in rows:
            horse_name = normalize_horse_name(row.get("horse_name", ""))
            eq_refno = row.get("eq_refno")
            sex = row.get("sex")
            if not horse_name:
                skipped += 1
                continue
            try:
                horse_id = None
                if eq_refno:
                    h = horse_repo.get_horse_by_registration(
                        str(eq_refno)
                    )
                    if h:
                        horse_id = str(h.horse_id)
                if not horse_id:
                    h = horse_repo.get_horse_by_name(horse_name)
                    if h:
                        horse_id = str(h.horse_id)
                if not horse_id:
                    horse_id = horse_repo.upsert_horse({
                        "registration_id": eq_refno,
                        "horse_name": horse_name,
                        "sex": sex,
                    })

                workout_date = row.get("workout_date")
                if isinstance(workout_date, str):
                    workout_date = date.fromisoformat(workout_date)

                workout_repo.insert_workout({
                    "horse_id": horse_id,
                    "workout_date": workout_date,
                    "track_code": row.get("track_code"),
                    "distance_furlongs": row.get("distance_furlongs"),
                    "workout_time": row.get("workout_time"),
                    "is_bullet": row.get("is_bullet", False),
                    "track_condition": row.get("track_condition"),
                    "workout_type": row.get("workout_type"),
                    "rank_on_day": row.get("rank_on_day"),
                    "total_works_on_day": row.get(
                        "total_works_on_day"
                    ),
                    "exercise_rider": row.get("exercise_rider"),
                })
                inserted += 1
            except Exception as e:
                errors.append(
                    f"{track_code} {horse_name}: "
                    f"{type(e).__name__}: {str(e)[:80]}"
                )
    return inserted, skipped, errors


def main():
    parser = argparse.ArgumentParser(
        description=__doc__.split("\n")[0]
    )
    parser.add_argument(
        "--start-date", type=str, required=True,
        help="Start date (YYYY-MM-DD, inclusive)",
    )
    parser.add_argument(
        "--end-date", type=str, required=True,
        help="End date (YYYY-MM-DD, inclusive)",
    )
    parser.add_argument(
        "--execute", action="store_true",
        help=(
            "Apply writes to DB. Default behavior is dry-run "
            "(no writes); pass --execute to commit."
        ),
    )
    parser.add_argument(
        "--tracks", type=str, default="SAR,BEL,AQU",
        help=(
            "Comma-separated NYRA tracks to fetch. "
            "Default: SAR,BEL,AQU (all NYRA_TRACKS)."
        ),
    )
    args = parser.parse_args()

    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d").date()
    except ValueError as e:
        parser.error(
            f"Invalid date format (expected YYYY-MM-DD): {e}"
        )
    if start_date > end_date:
        parser.error(
            f"--start-date ({start_date}) must be <= "
            f"--end-date ({end_date})"
        )

    tokens = [t.strip() for t in args.tracks.split(",") if t.strip()]
    valid = sorted(nyra_handler.NYRA_TRACKS.keys())
    unknown = [t for t in tokens if t not in nyra_handler.NYRA_TRACKS]
    if unknown:
        parser.error(
            f"Unknown --tracks token(s): {unknown}. "
            f"Valid tokens: {valid}"
        )
    if not tokens:
        parser.error("--tracks resolved to empty set")

    dry_run = not args.execute
    log_path = _setup_logging(dry_run)
    logging.info("=" * 70)
    logging.info(
        f"manual_nyra_workouts {'DRY-RUN ' if dry_run else ''}START"
    )
    logging.info(
        f"Window: {start_date} → {end_date} (inclusive); "
        f"Tracks: {tokens}"
    )
    logging.info(f"Log: {log_path}")
    logging.info("=" * 70)

    # per_track[(date, tc)] = (status, fetched, inserted, skipped, errors)
    per_track: dict = {}
    fail_rows: list[tuple] = []

    for target_date in _date_range(start_date, end_date):
        target_iso = target_date.isoformat()
        logging.info(f"\n── {target_iso} ──")
        for tc in tokens:
            try:
                rows, stats = _fetch_and_parse(tc, target_iso)
                logging.info(
                    f"  {tc}: fetched {len(rows)} workouts "
                    f"(stats: {stats})"
                )
                if dry_run:
                    per_track[(target_date, tc)] = (
                        "dry-run", len(rows), 0, 0, 0
                    )
                    continue
                inserted, skipped, errs = _upsert_workouts(rows, tc)
                err_count = len(errs)
                logging.info(
                    f"  {tc}: {inserted} upserted, {skipped} skipped, "
                    f"{err_count} errors"
                )
                for err in errs[:5]:
                    logging.warning(f"    error: {err}")
                status = (
                    "ok" if err_count == 0 and inserted > 0
                    else ("zero" if err_count == 0 else "fail")
                )
                per_track[(target_date, tc)] = (
                    status, len(rows), inserted, skipped, err_count
                )
                if status == "fail":
                    fail_rows.append((target_date, tc, err_count))
            except Exception as e:
                logging.error(
                    f"  {tc}: exception {type(e).__name__}: {e}"
                )
                logging.debug(traceback.format_exc())
                per_track[(target_date, tc)] = (
                    "exception", 0, 0, 0, 1
                )
                fail_rows.append((target_date, tc, "exception"))

    logging.info("\n" + "=" * 70)
    logging.info("manual_nyra_workouts SUMMARY")
    logging.info("=" * 70)
    logging.info(
        f"  {'Date':<12} {'Track':<6} {'Fetched':>8} {'Upserted':>9} "
        f"{'Skipped':>8} {'Errors':>7}  Status"
    )
    logging.info(
        f"  {'-'*12} {'-'*6} {'-'*8} {'-'*9} {'-'*8} {'-'*7}  ------"
    )
    tot_fetched = tot_inserted = tot_skipped = tot_errors = 0
    for (d, tc) in sorted(per_track.keys()):
        status, fetched, inserted, skipped, err_count = per_track[(d, tc)]
        tot_fetched += fetched
        tot_inserted += inserted
        tot_skipped += skipped
        tot_errors += err_count
        logging.info(
            f"  {str(d):<12} {tc:<6} {fetched:>8} {inserted:>9} "
            f"{skipped:>8} {err_count:>7}  {status.upper()}"
        )
    logging.info(
        f"  {'-'*12} {'-'*6} {'-'*8} {'-'*9} {'-'*8} {'-'*7}"
    )
    logging.info(
        f"  {'TOTAL':<12} {'':<6} {tot_fetched:>8} {tot_inserted:>9} "
        f"{tot_skipped:>8} {tot_errors:>7}"
    )

    if fail_rows:
        logging.warning("\n" + "!" * 70)
        logging.warning(f"FAIL/EXCEPTION rows: {len(fail_rows)}")
        for d, tc, err in fail_rows:
            logging.warning(f"  {d} {tc}: {err}")
        logging.warning("!" * 70)
    else:
        logging.info(
            "\nNo FAIL/EXCEPTION rows. "
            f"{'(dry-run)' if dry_run else 'All tracks succeeded.'}"
        )

    logging.info(f"\nLog: {log_path}")
    return 1 if fail_rows else 0


if __name__ == "__main__":
    sys.exit(main())
