#!/usr/bin/env python3
"""Re-parse historical chart PDFs and backfill the results table's
payout columns (win_payout / place_payout / show_payout + exotics).

Sister to reparse_charts.py — same PDF iteration, but updates `results`
not `races`. Used to fix the parser-version-skew gap surfaced in
Stream E1: ~44% of winners across April 2026 have NULL win_payout in
the DB despite the current parser correctly extracting them when run
today.

Match key for WPS payouts: (track_code, race_date, race_number, program_number)
→ entry_id → results row.

Match key for exotic payouts: same race + winning entry. Exotics stored
only on the winner's results row.

Usage:
  python3 scripts/reparse_payouts.py --sample 50      # parse 50 PDFs, dry-run
  python3 scripts/reparse_payouts.py                  # parse all, dry-run report
  python3 scripts/reparse_payouts.py --apply          # parse all + UPDATE results
"""
from __future__ import annotations
import argparse, io, json, os, re, sys, time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import date

import boto3
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values

sys.path.insert(0, "/home/strakajagr/projects/equine-equalizer/backend")
from services.chart_parser import (
    extract_all_text, split_into_races, parse_race_header,
    parse_payout_section,
)

S3_BUCKET = "equine-raw-data"
S3_PREFIX = "charts/"
PDF_NAME_RE = re.compile(r'^([A-Z]+)_(\d{8})\.pdf$')


def _list_pdfs():
    s3 = boto3.client("s3")
    keys = []
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=S3_PREFIX):
        for obj in page.get("Contents", []):
            keys.append(obj["Key"])
    return keys


def _parse_one_pdf(key: str):
    """Worker: download one PDF, extract per-race payouts.

    Returns (key, error, payout_rows) where each payout_row is:
      (track_code, race_date_iso, race_number, program_number,
       win, place, show,
       exacta_payout, trifecta_payout, superfecta_payout, dd_payout)
    The exotic columns are populated only for the program_number that
    wins the race (so it lands on the winner's results row).
    """
    s3 = boto3.client("s3")
    base = os.path.basename(key)
    m = PDF_NAME_RE.match(base)
    if not m:
        return key, None, []
    track_code = m.group(1)
    file_date = date(
        int(m.group(2)[:4]), int(m.group(2)[4:6]), int(m.group(2)[6:8])
    )

    try:
        body = s3.get_object(Bucket=S3_BUCKET, Key=key)["Body"].read()
    except Exception as e:
        return key, f"download: {type(e).__name__}: {e}", []

    try:
        text = extract_all_text(io.BytesIO(body))
        blocks = split_into_races(text)
    except Exception as e:
        return key, f"extract: {type(e).__name__}: {e}", []

    rows = []
    for b in blocks:
        try:
            hdr = parse_race_header(b, track_code, file_date)
            if hdr is None:
                continue
            race_number = hdr['race_number']
            payouts = parse_payout_section(b)
            wps = payouts.get('wps', {})
            exotics = payouts.get('exotics', {})

            # Identify the winner's pgm: WPS line index 0 has 'win'
            winner_pgm = None
            for pgm, prices in wps.items():
                if 'win' in prices:
                    winner_pgm = pgm
                    break

            for pgm, prices in wps.items():
                is_winner = (pgm == winner_pgm)
                rows.append((
                    track_code, file_date.isoformat(), race_number, pgm,
                    prices.get('win'),
                    prices.get('place'),
                    prices.get('show'),
                    exotics.get('exacta', {}).get('payout') if is_winner else None,
                    exotics.get('trifecta', {}).get('payout') if is_winner else None,
                    exotics.get('superfecta', {}).get('payout') if is_winner else None,
                    exotics.get('daily_double', {}).get('payout') if is_winner else None,
                ))
        except Exception:
            continue
    return key, None, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Write to DB. Default is dry-run.")
    ap.add_argument("--sample", type=int, default=0,
                    help="Process only first N PDFs (quick test).")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    print(f"=== reparse_payouts — mode: "
          f"{'APPLY' if args.apply else 'DRY-RUN'} "
          f"workers={args.workers} sample={args.sample or 'all'} ===",
          flush=True)

    keys = _list_pdfs()
    if args.sample:
        keys = keys[:args.sample]
    print(f"Will process {len(keys):,} PDFs", flush=True)

    all_rows = []
    errors = []
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(_parse_one_pdf, k) for k in keys]
        done = 0
        for fut in as_completed(futs):
            key, err, rows = fut.result()
            done += 1
            if err:
                errors.append((key, err))
            all_rows.extend(rows)
            if done % 200 == 0:
                print(f"  parsed {done:,}/{len(keys):,} "
                      f"({time.perf_counter()-t0:.0f}s) "
                      f"rows={len(all_rows):,}", flush=True)

    print(f"\nParse done. PDFs processed: {len(keys):,}    "
          f"per-WPS-row count: {len(all_rows):,}    "
          f"errors: {len(errors)}    "
          f"({time.perf_counter()-t0:.0f}s)")
    if errors:
        print("First 5 errors:")
        for k, e in errors[:5]:
            print(f"  {k}: {e}")

    n_win = sum(1 for r in all_rows if r[4] is not None)
    n_place = sum(1 for r in all_rows if r[5] is not None)
    n_show = sum(1 for r in all_rows if r[6] is not None)
    print(f"\nField population over {len(all_rows):,} WPS rows:")
    print(f"  win_payout populated:   {n_win:,}")
    print(f"  place_payout populated: {n_place:,}")
    print(f"  show_payout populated:  {n_show:,}")

    if not args.apply:
        print("\nDRY-RUN complete. Re-run with --apply to update DB.")
        return

    # ─── Apply ────────────────────────────────────────────────
    print(f"\nApplying UPDATEs in batches of 2,000...", flush=True)
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    sec = json.loads(sm.get_secret_value(
        SecretId="equine-equalizer/db-credentials")["SecretString"])
    conn = psycopg2.connect(
        host=sec["host"], port=sec["port"], dbname=sec["dbname"],
        user=sec["username"], password=sec["password"],
        cursor_factory=RealDictCursor,
    )
    conn.autocommit = False
    BATCH = 2000
    n_updated = 0
    cur = conn.cursor()
    apply_t0 = time.perf_counter()
    for i in range(0, len(all_rows), BATCH):
        batch = all_rows[i:i+BATCH]
        try:
            cur.execute("""CREATE TEMP TABLE IF NOT EXISTS rp_pay (
                track_code varchar, race_date date, race_number int,
                program_number varchar,
                win_payout numeric, place_payout numeric, show_payout numeric,
                exacta_payout numeric, trifecta_payout numeric,
                superfecta_payout numeric, dd_payout numeric
            ) ON COMMIT DROP""")
            cur.execute("TRUNCATE rp_pay")
            execute_values(
                cur,
                "INSERT INTO rp_pay VALUES %s",
                batch, page_size=1000,
            )
            cur.execute("""
              UPDATE results res SET
                win_payout         = COALESCE(u.win_payout,         res.win_payout),
                place_payout       = COALESCE(u.place_payout,       res.place_payout),
                show_payout        = COALESCE(u.show_payout,        res.show_payout),
                exacta_payout      = COALESCE(u.exacta_payout,      res.exacta_payout),
                trifecta_payout    = COALESCE(u.trifecta_payout,    res.trifecta_payout),
                superfecta_payout  = COALESCE(u.superfecta_payout,  res.superfecta_payout),
                daily_double_payout= COALESCE(u.dd_payout,          res.daily_double_payout)
              FROM rp_pay u
              JOIN tracks t   ON t.track_code = u.track_code
              JOIN races r    ON r.track_id   = t.track_id
                              AND r.race_date = u.race_date
                              AND r.race_number = u.race_number
              JOIN entries e  ON e.race_id    = r.race_id
                              AND e.program_number = u.program_number
              WHERE res.entry_id = e.entry_id
                AND (u.win_payout   IS NOT NULL
                  OR u.place_payout IS NOT NULL
                  OR u.show_payout  IS NOT NULL
                  OR u.exacta_payout IS NOT NULL
                  OR u.trifecta_payout IS NOT NULL
                  OR u.superfecta_payout IS NOT NULL
                  OR u.dd_payout IS NOT NULL)
            """)
            n_updated += cur.rowcount
            conn.commit()
        except Exception as e:
            print(f"  batch {i}-{i+len(batch)} FAILED: {e}", flush=True)
            conn.rollback()
        if (i // BATCH) % 10 == 0:
            print(f"  batch {i//BATCH}: cumulative updated={n_updated:,} "
                  f"({time.perf_counter()-apply_t0:.0f}s)", flush=True)

    print(f"\nApply complete. Total UPDATEd: {n_updated:,}    "
          f"({time.perf_counter()-apply_t0:.0f}s)")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
