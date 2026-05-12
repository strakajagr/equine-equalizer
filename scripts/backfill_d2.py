#!/usr/bin/env python3
"""D2 Backfill: 2026-05-02 → 2026-05-08 data-gap recovery.

Backfills the 7-day data gap during the equine-ingestion fire-and-fail
window (post-2026-05-02 Lambda INACTIVE per CDK image cull; restored
2026-05-09 at OCRC). During the gap window no fresh entries/results/
workouts rows were written to DB.

Scope:
  - Entries (HRN scraper)
  - Results (HRN scraper, post-Bug #28 patch; uses header-aware
    column resolution per Phase 5.3.1 fix at commit 3465195)
  - NYRA workouts (NYRA scraper)

Per-date isolation: failure on one date does not abort the run.
Idempotent: re-runnable safely via UPSERT on natural keys.

Preconditions:
  - Bug #28 patch (D1) deployed to local working tree (commit 3465195
    or later). Script depends on patched _parse_race_result.
  - DATABASE_URL env var set OR DB_SECRET_ARN + AWS credentials.
  - Playwright + Chromium installed (HRN scraper requires).
  - Internet access for HRN + NYRA endpoints.

Usage:
  python3 scripts/backfill_d2.py --start-date 2026-05-02 --end-date 2026-05-08
      # ^ dry-run (default; no DB writes)
  python3 scripts/backfill_d2.py --start-date 2026-05-02 --end-date 2026-05-08 --execute
      # ^ apply writes (commit to DB)

Logs: scripts/logs/backfill_d2_<timestamp>.log + stdout.

After run, verify via DB query:
  SELECT race_date, COUNT(*) FROM entries
    WHERE race_date BETWEEN '2026-05-02' AND '2026-05-08'
    GROUP BY race_date ORDER BY race_date;
  -- similar for results (via races join) and workouts.
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


# ── DB credential setup (must run before any shared.db.get_db() invocation) ──
# Why: Tony's local env has DB_SECRET_ARN pointing at a different
# project's (fantasy-baseball) secret whose JSON lacks 'host' key.
# shared.db._get_connection_string prefers DATABASE_URL over
# DB_SECRET_ARN — so we set DATABASE_URL from the equine-equalizer
# secret and shared.db sees the correct credentials without needing
# any env-var collision resolution. Works for IngestionService and
# all other service code that internally calls shared.db.get_db().
def _setup_database_url():
    """Fetch equine-equalizer secret and set DATABASE_URL env var.

    Hardcoded SecretId per scripts/reparse_payouts.py:177 precedent.
    """
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


# Set DATABASE_URL BEFORE service imports (they may eagerly import
# shared.db at module load).
_setup_database_url()


# ── Existing primitives (do not author new write code) ──────────────
from shared.db import get_db, execute_query  # noqa: E402
from shared.horse_naming import horse_match_key, normalize_horse_name  # noqa: E402
from services.ingestion_service import IngestionService  # noqa: E402
from services.data_sources import HRNScraper  # noqa: E402
from repositories.result_repository import ResultRepository  # noqa: E402
from repositories.horse_repository import HorseRepository  # noqa: E402
from repositories.workout_repository import WorkoutRepository  # noqa: E402

# NYRA scraper — Lambda handler exposes scrape primitives as
# module-level functions; import directly.
import handler as nyra_handler  # noqa: E402

# ── Configuration ───────────────────────────────────────────────────
NYRA_TRACKS = ["SAR", "BEL", "AQU"]


def _setup_logging(dry_run: bool) -> str:
    """Configure stdout + file logging. Returns log file path."""
    logs_dir = os.path.join(REPO_ROOT, "scripts", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = "_dryrun" if dry_run else ""
    log_path = os.path.join(logs_dir, f"backfill_d2_{ts}{suffix}.log")

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
    """Yield dates from start to end inclusive."""
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


def _backfill_entries(target_date: date, dry_run: bool) -> int:
    """Invoke IngestionService.fetch_daily_entries for target_date.

    fetch_daily_entries internally handles HRN scrape + race-card
    storage via existing UPSERT primitives. Returns # rows reported
    by service (best-effort; service-internal counting may vary).
    """
    if dry_run:
        logging.info(f"  [DRY-RUN] entries fetch skipped for {target_date}")
        return 0
    with get_db() as conn:
        svc = IngestionService(conn)
        result = svc.fetch_daily_entries(target_date)
    # Return service-reported count (shape varies; defensive parse).
    if isinstance(result, dict):
        return int(result.get("entries_inserted", 0) or result.get("count", 0) or 0)
    if isinstance(result, int):
        return result
    return 0


def _backfill_results(target_date: date, dry_run: bool) -> int:
    """Invoke HRNScraper.fetch_results + UPSERT via ResultRepository.

    Replicates the fetch_results action handler pattern from
    backend/lambdas/ingestion/handler.py:244-318. Uses post-Bug-#28
    patched _parse_race_result for header-aware payout extraction.
    Returns # results upserted.
    """
    scraper = HRNScraper()
    race_results = scraper.fetch_results(target_date)
    logging.info(
        f"  HRN returned {len(race_results)} races for {target_date}"
    )

    if dry_run:
        # Count what would be inserted without writing.
        total = sum(len(r.get("results", [])) for r in race_results)
        logging.info(f"  [DRY-RUN] would upsert {total} result rows")
        return total

    inserted = 0
    skipped = 0
    errors = []
    with get_db() as conn:
        result_repo = ResultRepository(conn)
        for race_data in race_results:
            tc = race_data["track_code"]
            rn = race_data["race_number"]
            race_rows = execute_query(
                conn,
                """SELECT r.race_id FROM races r
                   JOIN tracks t ON r.track_id = t.track_id
                   WHERE t.track_code = %s AND r.race_number = %s
                     AND r.race_date = %s""",
                (tc, rn, target_date),
            )
            if not race_rows:
                skipped += 1
                continue
            race_id = race_rows[0]["race_id"]
            entry_rows = execute_query(
                conn,
                """SELECT e.entry_id, e.horse_id, h.horse_name
                   FROM entries e
                   JOIN horses h ON e.horse_id = h.horse_id
                   WHERE e.race_id = %s""",
                (race_id,),
            )
            entry_by_name = {
                horse_match_key(er["horse_name"]): er for er in entry_rows
            }
            for result in race_data.get("results", []):
                entry = entry_by_name.get(
                    horse_match_key(result["horse_name"])
                )
                if not entry:
                    continue
                try:
                    result_repo.insert_result({
                        "entry_id": entry["entry_id"],
                        "race_id": race_id,
                        "horse_id": entry["horse_id"],
                        "finish_position": result["finish_position"],
                        "official_finish": result["official_finish"],
                        "win_payout": result.get("win_payout"),
                        "place_payout": result.get("place_payout"),
                        "show_payout": result.get("show_payout"),
                        "exacta_payout": result.get("exacta_payout"),
                        "trifecta_payout": result.get("trifecta_payout"),
                    })
                    inserted += 1
                except Exception as e:
                    errors.append(
                        f"{tc} R{rn} {result['horse_name']}: "
                        f"{type(e).__name__}: {str(e)[:80]}"
                    )
    logging.info(
        f"  results: {inserted} upserted, {skipped} races skipped, "
        f"{len(errors)} errors"
    )
    for err in errors[:5]:
        logging.warning(f"  result error: {err}")
    return inserted


def _backfill_workouts(target_date: date, dry_run: bool) -> int:
    """Scrape NYRA workouts via NYRA scraper primitives + UPSERT.

    Replicates load_workouts_from_s3 action handler pattern from
    backend/lambdas/ingestion/handler.py:1537-1644 minus the S3 hop:
    scrape directly from NYRA pages, write directly to DB via
    WorkoutRepository.insert_workout (UPSERT).
    Returns # workout rows upserted across all 3 NYRA tracks.
    """
    target_iso = target_date.isoformat()
    all_workouts = []
    for tc in NYRA_TRACKS:
        track_slug = nyra_handler.NYRA_TRACKS.get(tc)
        if not track_slug:
            continue
        try:
            html = nyra_handler.fetch_track_page(track_slug, target_iso)
            rows = nyra_handler.parse_nyra_html(html, tc, target_iso)
            logging.info(
                f"  NYRA {tc}: {len(rows)} workouts on {target_iso}"
            )
            all_workouts.extend(rows)
        except Exception as e:
            logging.warning(
                f"  NYRA {tc} scrape failed: "
                f"{type(e).__name__}: {str(e)[:80]}"
            )

    if dry_run:
        logging.info(
            f"  [DRY-RUN] would upsert {len(all_workouts)} workout rows"
        )
        return len(all_workouts)

    inserted = 0
    skipped = 0
    errors = []
    with get_db() as conn:
        horse_repo = HorseRepository(conn)
        workout_repo = WorkoutRepository(conn)
        for row in all_workouts:
            horse_name = normalize_horse_name(row.get("horse_name", ""))
            eq_refno = row.get("eq_refno")
            sex = row.get("sex")
            if not horse_name:
                skipped += 1
                continue
            try:
                # Resolve horse_id per load_workouts_from_s3 pattern:
                # refno first, then name, then create via upsert_horse.
                horse_id = None
                if eq_refno:
                    h = horse_repo.get_horse_by_registration(str(eq_refno))
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
                    "total_works_on_day": row.get("total_works_on_day"),
                    "exercise_rider": row.get("exercise_rider"),
                })
                inserted += 1
            except Exception as e:
                errors.append(
                    f"{row.get('track_code')} {horse_name}: "
                    f"{type(e).__name__}: {str(e)[:80]}"
                )
    logging.info(
        f"  workouts: {inserted} upserted, {skipped} skipped, "
        f"{len(errors)} errors"
    )
    for err in errors[:5]:
        logging.warning(f"  workout error: {err}")
    return inserted


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--start-date", type=str, required=True,
        help="Backfill start date (YYYY-MM-DD, inclusive)",
    )
    parser.add_argument(
        "--end-date", type=str, required=True,
        help="Backfill end date (YYYY-MM-DD, inclusive)",
    )
    parser.add_argument(
        "--execute", action="store_true",
        help=(
            "Apply writes to DB. Default behavior is dry-run "
            "(no writes); pass --execute to commit."
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
            f"--start-date ({start_date}) must be <= --end-date ({end_date})"
        )

    dry_run = not args.execute

    log_path = _setup_logging(dry_run)
    logging.info("=" * 70)
    logging.info(
        f"D2 backfill {'DRY-RUN ' if dry_run else ''}START"
    )
    logging.info(f"Window: {start_date} → {end_date} (inclusive)")
    logging.info(f"Log: {log_path}")
    logging.info("=" * 70)

    per_date_summary = []  # (date, entries, results, workouts, error_msg)
    total_entries = total_results = total_workouts = 0
    failed_dates = []

    for target_date in _date_range(start_date, end_date):
        logging.info(f"\n── {target_date} ──")
        date_error = None
        e_count = r_count = w_count = 0

        try:
            e_count = _backfill_entries(target_date, dry_run)
            total_entries += e_count
        except Exception as e:
            date_error = f"entries: {type(e).__name__}: {str(e)[:120]}"
            logging.error(f"  entries FAILED: {date_error}")
            logging.debug(traceback.format_exc())

        try:
            r_count = _backfill_results(target_date, dry_run)
            total_results += r_count
        except Exception as e:
            msg = f"results: {type(e).__name__}: {str(e)[:120]}"
            date_error = f"{date_error}; {msg}" if date_error else msg
            logging.error(f"  results FAILED: {msg}")
            logging.debug(traceback.format_exc())

        try:
            w_count = _backfill_workouts(target_date, dry_run)
            total_workouts += w_count
        except Exception as e:
            msg = f"workouts: {type(e).__name__}: {str(e)[:120]}"
            date_error = f"{date_error}; {msg}" if date_error else msg
            logging.error(f"  workouts FAILED: {msg}")
            logging.debug(traceback.format_exc())

        per_date_summary.append(
            (target_date, e_count, r_count, w_count, date_error)
        )
        if date_error:
            failed_dates.append(target_date)

    # ── Final summary ────────────────────────────────────────────────
    logging.info("\n" + "=" * 70)
    logging.info("D2 backfill SUMMARY")
    logging.info("=" * 70)
    logging.info(
        f"{'Date':<12} {'Entries':>8} {'Results':>8} {'Workouts':>9}  Status"
    )
    for d, ec, rc, wc, err in per_date_summary:
        status = "FAIL: " + err if err else "OK"
        logging.info(f"{str(d):<12} {ec:>8} {rc:>8} {wc:>9}  {status}")
    logging.info("-" * 70)
    logging.info(
        f"{'TOTAL':<12} {total_entries:>8} {total_results:>8} "
        f"{total_workouts:>9}"
    )
    logging.info(
        f"Dates with errors: {len(failed_dates)} of "
        f"{len(per_date_summary)} "
        f"({', '.join(str(d) for d in failed_dates) if failed_dates else 'none'})"
    )
    logging.info(f"Log: {log_path}")

    # Exit non-zero if any date failed entirely (so CI / cron can detect).
    return 1 if len(failed_dates) == len(per_date_summary) else 0


if __name__ == "__main__":
    sys.exit(main())
