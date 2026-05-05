#!/usr/bin/env python3
"""Mass historical re-inference — runs WR + PL + LS inference for every
distinct race_date in the races table, in chronological order.

Why: today's architectural fixes changed the semantic of:
  - wr_predictions.win_probability (now ranker-softmax, calibration bypassed)
  - pl_predictions.predicted_rank (now sorted by predicted_ev)
  - ls_predictions.predicted_rank (now sorted by longshot edge ratio)

Old prediction rows in the database were produced by the prior code paths
and are inconsistent with the new schema. Dashboard ROI / hit-rate /
track-record metrics are computed against these stored rows. Until they
get re-inferred, those metrics reflect the OLD broken architecture.

This script idempotently re-runs inference for all dates. UNIQUE
constraints + ON CONFLICT DO UPDATE on each prediction table mean repeat
runs are no-ops on data that hasn't changed.

Usage:
  python3 scripts/reinfer_all_historical.py                 # all dates
  python3 scripts/reinfer_all_historical.py --since YYYY-MM-DD  # filter
  python3 scripts/reinfer_all_historical.py --dry-run       # list dates
  python3 scripts/reinfer_all_historical.py --resume-from YYYY-MM-DD

Logs to /tmp/mass_reinfer_<YYYYMMDD>_<HHMMSS>.log via tee-style.
Resumable: if the run crashes mid-flight, find the last completed date
in the log and use --resume-from to pick up.
"""
from __future__ import annotations
import argparse, json, os, sys, time
from datetime import date

import boto3
import psycopg2
from psycopg2.extras import RealDictCursor
import urllib.request
import urllib.error

API_BASE = "https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com"
MODELS = ['wr', 'pl', 'ls']


def _list_dates(since: str | None, resume_from: str | None) -> list[str]:
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    sec = json.loads(sm.get_secret_value(
        SecretId="equine-equalizer/db-credentials")["SecretString"])
    conn = psycopg2.connect(
        host=sec["host"], port=sec["port"], dbname=sec["dbname"],
        user=sec["username"], password=sec["password"],
        cursor_factory=RealDictCursor,
    )
    cur = conn.cursor()
    where = []
    params = []
    if since:
        where.append("race_date >= %s")
        params.append(since)
    if resume_from:
        where.append("race_date >= %s")
        params.append(resume_from)
    where_clause = (" WHERE " + " AND ".join(where)) if where else ""
    cur.execute(
        f"SELECT DISTINCT race_date FROM races{where_clause} "
        f"ORDER BY race_date ASC",
        tuple(params),
    )
    dates = [r['race_date'].isoformat() for r in cur.fetchall()]
    cur.close(); conn.close()
    return dates


def _invoke(model: str, date_str: str, retries: int = 3) -> tuple[int, str]:
    url = f"{API_BASE}/{model}/predictions/run?date={date_str}"
    req = urllib.request.Request(url, method='POST')
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=900) as resp:
                body = resp.read().decode('utf-8', errors='replace')
                return resp.status, body
        except urllib.error.HTTPError as e:
            if attempt == retries:
                return e.code, e.read().decode('utf-8', errors='replace')
            time.sleep(8 * attempt)  # backoff
        except Exception as e:
            if attempt == retries:
                return 0, f"{type(e).__name__}: {e}"
            time.sleep(8 * attempt)
    return 0, "unreachable"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="YYYY-MM-DD lower bound")
    ap.add_argument("--resume-from", help="YYYY-MM-DD resume point")
    ap.add_argument("--dry-run", action="store_true",
                    help="List dates without invoking")
    ap.add_argument("--models", default="wr,pl,ls",
                    help="Comma-separated model subset (default: wr,pl,ls)")
    args = ap.parse_args()

    selected_models = [m.strip().lower() for m in args.models.split(',') if m.strip()]
    invalid = [m for m in selected_models if m not in MODELS]
    if invalid:
        raise SystemExit(f"unknown models: {invalid}. valid: {MODELS}")

    dates = _list_dates(args.since, args.resume_from)
    print(f"=== mass_reinfer — {len(dates):,} dates "
          f"(from {dates[0] if dates else 'n/a'} "
          f"to {dates[-1] if dates else 'n/a'}) ===", flush=True)

    if args.dry_run:
        for d in dates:
            print(f"  {d}")
        return

    t0 = time.perf_counter()
    completed = 0
    errors = 0
    for i, d in enumerate(dates, 1):
        date_t0 = time.perf_counter()
        date_results: list[str] = []
        for m in selected_models:
            status, body = _invoke(m, d)
            ok = (status == 200)
            date_results.append(f"{m}={status}")
            if not ok:
                errors += 1
                print(f"  [{i}/{len(dates)}] {d} {m} FAILED status={status}: "
                      f"{body[:200]}", flush=True)
        completed += 1
        elapsed = time.perf_counter() - date_t0
        total_elapsed = time.perf_counter() - t0
        avg = total_elapsed / i
        eta = avg * (len(dates) - i)
        print(f"  [{i}/{len(dates)}] {d}  {' '.join(date_results)}  "
              f"({elapsed:.0f}s  total {total_elapsed:.0f}s  ETA {eta/60:.0f}m)",
              flush=True)

    print(f"\nDone. completed={completed} errors={errors} "
          f"elapsed={time.perf_counter()-t0:.0f}s "
          f"({(time.perf_counter()-t0)/60:.1f}m)")


if __name__ == "__main__":
    main()
