#!/usr/bin/env python3
"""Re-trigger WR/PL/LS inference Lambdas for a historical date range.

Synchronous invocation per Lambda per date via `event['source'] == 'batch'`
contract (handlers at backend/lambdas/{wr,pl,ls}-inference/handler.py). The
inference Lambdas already accept the `batch` event-source branch with
`event['date']` (ISO date) — no handler patch needed. This script just
loops over the date range + invokes the 3 Lambdas per date.

Use cases:
  - Re-trigger inference for the 2026-05-10 predictions-gap window (or any
    other historical date with missing wr/pl/ls predictions)
  - Re-run inference after D2/D3 backfill lands fresh entries/results
    (predictions depend on the entries+results substrate; backfill ⇒
    re-trigger inference)

Sequencing:
  Run AFTER D3 + D2 backfills land successfully AND AFTER the scraper CDK
  deploy (Q-T1 V2 fix + BEL slug fix). Re-running inference before
  backfill completes will re-generate predictions against incomplete or
  corrupted entries data.

Wall-clock note:
  Synchronous invocation (`InvocationType=RequestResponse`); expect ~30s –
  180s per Lambda per date. 11-date × 3-Lambda re-trigger ≈ 30 minutes
  total. Synchronous chosen to surface `FunctionError` + response body
  immediately — the silent-async-drop failure mode (per Phase A-prime
  diagnostic) is the failure class this script must NOT silently repeat.

Usage:
  # Dry-run (default; preview invocations without firing)
  python3 scripts/rerun_inference.py --start-date 2026-04-30 --end-date 2026-05-08

  # Execute (re-trigger inference for date range)
  python3 scripts/rerun_inference.py --start-date 2026-04-30 --end-date 2026-05-08 --execute

  # Subset (only WR + PL, skip LS)
  python3 scripts/rerun_inference.py --start-date 2026-04-30 --end-date 2026-05-08 \
      --execute --lambdas wr,pl

  # Style override (WR/PL only; LS ignores)
  python3 scripts/rerun_inference.py --start-date 2026-05-09 --end-date 2026-05-09 \
      --execute --style turf

Logs: scripts/logs/rerun_inference_<timestamp>.log + stdout.

Idempotency:
  Inference services UPSERT predictions per (entry_id, model_version). Re-
  running on a date with existing predictions overwrites with re-computed
  values. Safe to re-run.
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

LAMBDA_NAMES = {
    "wr": "equine-wr-inference",
    "pl": "equine-pl-inference",
    "ls": "equine-ls-inference",
}
# WR + PL handlers accept event['style']; LS handler does not reference it
# (passed key is harmless — silently ignored by LS).
STYLE_ACCEPTING = {"equine-wr-inference", "equine-pl-inference"}


def _setup_logging(dry_run: bool) -> str:
    logs_dir = os.path.join(REPO_ROOT, "scripts", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = "_dryrun" if dry_run else ""
    log_path = os.path.join(
        logs_dir, f"rerun_inference_{ts}{suffix}.log"
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


def _invoke_lambda(
    client, function_name: str, payload: dict, dry_run: bool
) -> str:
    """Invoke one Lambda synchronously. Return verdict string:
    'dry-run', 'ok', 'fail' (StatusCode != 200 or FunctionError set),
    or 'exception' (boto3 / network exception)."""
    if dry_run:
        logging.info(
            f"  [DRY-RUN] would invoke {function_name} "
            f"with payload {json.dumps(payload)}"
        )
        return "dry-run"
    try:
        response = client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload).encode("utf-8"),
        )
        status_code = response["StatusCode"]
        function_error = response.get("FunctionError")
        body = response["Payload"].read().decode("utf-8")
        logging.info(
            f"  {function_name}: StatusCode={status_code} "
            f"FunctionError={function_error or 'none'} "
            f"Body={body[:200]}"
        )
        if status_code == 200 and not function_error:
            return "ok"
        return "fail"
    except Exception as e:
        logging.error(
            f"  {function_name}: exception "
            f"{type(e).__name__}: {e}",
            exc_info=True,
        )
        return "exception"


def main():
    parser = argparse.ArgumentParser(
        description=__doc__.split("\n")[0]
    )
    parser.add_argument(
        "--start-date", type=str, required=True,
        help="Re-trigger start date (YYYY-MM-DD, inclusive)",
    )
    parser.add_argument(
        "--end-date", type=str, required=True,
        help="Re-trigger end date (YYYY-MM-DD, inclusive)",
    )
    parser.add_argument(
        "--execute", action="store_true",
        help=(
            "Invoke inference Lambdas. Default behavior is dry-run "
            "(no invocations); pass --execute to fire."
        ),
    )
    parser.add_argument(
        "--style", type=str, default="general",
        help=(
            "WR/PL inference style override (default: general). "
            "LS handler does not accept style; key omitted from LS "
            "payload."
        ),
    )
    parser.add_argument(
        "--lambdas", type=str, default="wr,pl,ls",
        help=(
            "Comma-separated subset of inference Lambdas to invoke. "
            "Tokens: wr, pl, ls. Default: wr,pl,ls (all three)."
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

    tokens = [t.strip() for t in args.lambdas.split(",") if t.strip()]
    unknown = [t for t in tokens if t not in LAMBDA_NAMES]
    if unknown:
        parser.error(
            f"Unknown --lambdas token(s): {unknown}. "
            f"Valid tokens: {sorted(LAMBDA_NAMES.keys())}"
        )
    if not tokens:
        parser.error("--lambdas resolved to empty set")
    lambda_names = [LAMBDA_NAMES[t] for t in tokens]

    dry_run = not args.execute
    log_path = _setup_logging(dry_run)
    logging.info("=" * 70)
    logging.info(
        f"rerun_inference {'DRY-RUN ' if dry_run else ''}START"
    )
    logging.info(
        f"Window: {start_date} → {end_date} (inclusive); "
        f"Lambdas: {lambda_names}; style: {args.style}"
    )
    logging.info(f"Log: {log_path}")
    logging.info("=" * 70)

    client = boto3.client("lambda", region_name="us-east-1")
    per_date: dict[date, dict[str, str]] = {}

    for target_date in _date_range(start_date, end_date):
        logging.info(f"\n── {target_date} ──")
        per_date[target_date] = {}
        for fn in lambda_names:
            payload = {
                "source": "batch",
                "date": target_date.isoformat(),
            }
            if fn in STYLE_ACCEPTING:
                payload["style"] = args.style
            try:
                verdict = _invoke_lambda(client, fn, payload, dry_run)
            except Exception as e:
                # Defensive: _invoke_lambda already catches; this is
                # an outer safety net so a single Lambda's failure
                # doesn't abort the per-date loop.
                logging.error(
                    f"  {fn}: outer-loop exception "
                    f"{type(e).__name__}: {e}"
                )
                logging.debug(traceback.format_exc())
                verdict = "exception"
            per_date[target_date][fn] = verdict

    # ── Final summary ────────────────────────────────────────────────
    logging.info("\n" + "=" * 70)
    logging.info("rerun_inference SUMMARY")
    logging.info("=" * 70)
    header_cells = [f"{t.upper():>6}" for t in tokens]
    logging.info(f"  {'Date':<12} " + " ".join(header_cells))
    logging.info(f"  {'-'*12} " + " ".join(["-"*6 for _ in tokens]))
    fail_rows: list[tuple[date, str, str]] = []
    totals = {fn: {"ok": 0, "fail": 0, "exception": 0, "dry-run": 0}
              for fn in lambda_names}
    for d in sorted(per_date.keys()):
        row_cells = []
        for tok, fn in zip(tokens, lambda_names):
            v = per_date[d].get(fn, "?")
            totals[fn][v] = totals[fn].get(v, 0) + 1
            row_cells.append(f"{v.upper():>6}")
            if v in ("fail", "exception"):
                fail_rows.append((d, fn, v))
        logging.info(f"  {str(d):<12} " + " ".join(row_cells))
    logging.info(f"  {'-'*12} " + " ".join(["-"*6 for _ in tokens]))
    total_dates = len(per_date)
    total_cells = []
    for fn in lambda_names:
        ok_count = totals[fn]["ok"] + totals[fn]["dry-run"]
        total_cells.append(f"{ok_count}/{total_dates}")
    logging.info(
        f"  {'TOTAL OK':<12} " +
        " ".join(f"{c:>6}" for c in total_cells)
    )

    if fail_rows:
        logging.warning("\n" + "!" * 70)
        logging.warning(
            f"FAIL/EXCEPTION rows: {len(fail_rows)}"
        )
        for d, fn, v in fail_rows:
            logging.warning(f"  {d} {fn}: {v.upper()}")
        logging.warning("!" * 70)
    else:
        logging.info(
            "\nNo FAIL/EXCEPTION rows. "
            f"{'(dry-run)' if dry_run else 'All invocations succeeded.'}"
        )

    logging.info(f"\nLog: {log_path}")
    return 1 if fail_rows else 0


if __name__ == "__main__":
    sys.exit(main())
