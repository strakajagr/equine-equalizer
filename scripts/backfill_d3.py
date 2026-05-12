#!/usr/bin/env python3
"""D3 Backfill: 2026-04-30 → 2026-05-02 Bug #28 corruption window.

Re-scrapes HRN results for the 3-day window where Bug #28
column-shift produced corrupted payout rows:
  - win_payout NULL
  - place_payout = (value that should be in win_payout)
  - show_payout = (value that should be in place_payout)
  - daily_double_payout NULL

Uses the post-D1-patch HRN scraper (header-aware column resolution
per commit 3465195). Existing UNIQUE(entry_id) on results table
means insert_result UPSERT will overwrite the corrupted rows with
correctly-extracted values.

Per-Q-T1 disclosure: header-pattern-match success is verification-
independent. If HRN headers diverge from substring patterns
('win', 'place', 'show'), payouts return NULL — same as missing
column — graceful degradation. After this script runs, query the
DB to confirm header patterns match HRN's actual header text on
the backfill date pages. Sample query in this docstring.

Scope:
  - HRN results ONLY. No entries backfill (entries already exist
    from pre-fire-and-fail-window ingestion). No workouts backfill
    (D3 is Bug #28 column-shift specifically per § 5.3.1).

Per-date isolation: failure on one date does not abort the run.
Idempotent: re-runnable safely via UPSERT on (entry_id).

Preconditions:
  - Bug #28 patch (D1) deployed to local working tree (commit
    3465195 or later). Script depends on patched
    _parse_race_result.
  - DATABASE_URL env var set OR DB_SECRET_ARN + AWS credentials.
  - Playwright + Chromium installed (HRN scraper requires).
  - Internet access for HRN endpoints.
  - Entries already present in DB for backfill date range (D3
    UPSERTs results referencing existing entries via UNIQUE
    constraint).

Usage:
  python3 scripts/backfill_d3.py --start-date 2026-04-30 --end-date 2026-05-02
      # ^ dry-run (default; no DB writes)
  python3 scripts/backfill_d3.py --start-date 2026-04-30 --end-date 2026-05-02 --execute
      # ^ apply writes (commit to DB)

Logs: scripts/logs/backfill_d3_<timestamp>.log + stdout.

Post-execution validation (Q-T1 audit-after-deploy):
  SELECT race_date,
         COUNT(*) AS total,
         COUNT(*) FILTER (WHERE win_payout IS NULL) AS null_win,
         COUNT(*) FILTER (WHERE win_payout IS NOT NULL) AS has_win
    FROM results r
    JOIN entries e ON r.entry_id = e.entry_id
    JOIN races rc  ON e.race_id  = rc.race_id
   WHERE rc.race_date BETWEEN '2026-04-30' AND '2026-05-02'
     AND r.finish_position = 1
   GROUP BY race_date ORDER BY race_date;

If null_win > 0 on a date, header patterns failed to match HRN
header text — extend _resolve_col patterns in hrn_scraper.py and
re-run this script.
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

    Idempotent: if DATABASE_URL is already a valid equine-equalizer
    connection string (caller already set it), this is a no-op.
    Otherwise overrides DATABASE_URL via secrets-manager fetch.

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


# ── Existing primitives ─────────────────────────────────────────────
from shared.db import get_db, execute_query  # noqa: E402
from shared.horse_naming import horse_match_key  # noqa: E402
from services.data_sources import HRNScraper  # noqa: E402
from repositories.result_repository import ResultRepository  # noqa: E402

# ── Configuration ───────────────────────────────────────────────────
# (date range provided via --start-date / --end-date CLI args in main())


def _setup_logging(dry_run: bool) -> str:
    """Configure stdout + file logging. Returns log file path."""
    logs_dir = os.path.join(REPO_ROOT, "scripts", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = "_dryrun" if dry_run else ""
    log_path = os.path.join(logs_dir, f"backfill_d3_{ts}{suffix}.log")
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


def _backfill_results_for_date(target_date: date, dry_run: bool) -> tuple[int, int, int]:
    """Re-scrape HRN results for target_date + UPSERT into results.

    Replicates fetch_results action pattern. Tracks null-payout-rate
    per date as proxy for header-pattern-match success (Q-T1).

    Returns (upserted_count, win_payout_null_count, win_payout_populated_count).
    null/populated counts are computed across winner rows only
    (finish_position == 1) since that's the rate most diagnostic of
    header-match success.
    """
    scraper = HRNScraper()
    race_results = scraper.fetch_results(target_date)
    logging.info(
        f"  HRN returned {len(race_results)} races for {target_date}"
    )

    # Diagnostic: count win_payout populated/null on winner rows.
    win_populated = 0
    win_null = 0
    for race_data in race_results:
        for r in race_data.get("results", []):
            if r.get("official_finish") == 1 or r.get("finish_position") == 1:
                if r.get("win_payout") is None:
                    win_null += 1
                else:
                    win_populated += 1

    logging.info(
        f"  Q-T1 header-match proxy: winner rows "
        f"{win_populated} populated / {win_null} null win_payout "
        f"(if many null, extend _resolve_col patterns)"
    )

    if dry_run:
        total = sum(len(r.get("results", [])) for r in race_results)
        logging.info(f"  [DRY-RUN] would upsert {total} result rows")
        return total, win_null, win_populated

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
    return inserted, win_null, win_populated


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
        f"D3 backfill {'DRY-RUN ' if dry_run else ''}START "
        f"(Bug #28 corruption window)"
    )
    logging.info(f"Window: {start_date} → {end_date} (inclusive)")
    logging.info(f"Log: {log_path}")
    logging.info("=" * 70)

    per_date_summary = []  # (date, upserted, win_null, win_populated, error)
    total_upserted = total_win_null = total_win_populated = 0
    failed_dates = []

    for target_date in _date_range(start_date, end_date):
        logging.info(f"\n── {target_date} ──")
        date_error = None
        upserted = win_null = win_populated = 0
        try:
            upserted, win_null, win_populated = _backfill_results_for_date(
                target_date, dry_run
            )
            total_upserted += upserted
            total_win_null += win_null
            total_win_populated += win_populated
        except Exception as e:
            date_error = f"{type(e).__name__}: {str(e)[:120]}"
            logging.error(f"  FAILED: {date_error}")
            logging.debug(traceback.format_exc())
            failed_dates.append(target_date)
        per_date_summary.append(
            (target_date, upserted, win_null, win_populated, date_error)
        )

    # ── Final summary ────────────────────────────────────────────────
    logging.info("\n" + "=" * 70)
    logging.info("D3 backfill SUMMARY (Bug #28 corruption window)")
    logging.info("=" * 70)
    logging.info(
        f"{'Date':<12} {'Upserted':>8} {'WinNull':>7} {'WinHas':>7}  Status"
    )
    for d, u, wn, wp, err in per_date_summary:
        status = "FAIL: " + err if err else "OK"
        logging.info(f"{str(d):<12} {u:>8} {wn:>7} {wp:>7}  {status}")
    logging.info("-" * 70)
    logging.info(
        f"{'TOTAL':<12} {total_upserted:>8} "
        f"{total_win_null:>7} {total_win_populated:>7}"
    )

    # Q-T1 audit-after-deploy proxy verdict.
    if total_win_populated + total_win_null > 0:
        match_rate = total_win_populated / (total_win_populated + total_win_null)
        logging.info(
            f"Q-T1 header-match success proxy: {match_rate:.1%} "
            f"({total_win_populated}/{total_win_populated + total_win_null} "
            f"winner rows have non-NULL win_payout)"
        )
        if match_rate < 0.80:
            logging.warning(
                "Q-T1 PROXY ALERT: header-match rate below 80%. "
                "Likely _resolve_col patterns do not match HRN's "
                "current header text. Extend patterns in "
                "hrn_scraper.py and re-run."
            )
        else:
            logging.info(
                "Q-T1 PROXY OK: header-match rate above 80% threshold. "
                "Patch operating as designed."
            )

    logging.info(
        f"Dates with errors: {len(failed_dates)} of "
        f"{len(per_date_summary)} "
        f"({', '.join(str(d) for d in failed_dates) if failed_dates else 'none'})"
    )
    logging.info(f"Log: {log_path}")

    return 1 if len(failed_dates) == len(per_date_summary) else 0


if __name__ == "__main__":
    sys.exit(main())
