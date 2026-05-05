#!/usr/bin/env python3
"""One-time re-parse of historical chart PDFs to populate race_name,
conditions, and grade in the races table.

Reads every PDF under s3://equine-raw-data/charts/{TRACK}/, parses each
race block, and UPDATEs the matching races row. Does NOT change
race_type, purse, distance, or any other field that's already correct.

Concurrency: 8 worker processes by default. Per-PDF work is
download + pdfplumber-extract, ~1-3s each.

Batches: collects all per-race tuples in memory, then issues UPDATEs
in batches of 1,000 inside short transactions. A single bad PDF cannot
roll back any other PDF's contributions.

Usage:
  python3 scripts/reparse_charts.py --sample 100   # parse 100 PDFs, no writes
  python3 scripts/reparse_charts.py                # parse all, no writes
  python3 scripts/reparse_charts.py --apply        # parse all + write to DB
"""
from __future__ import annotations
import argparse, io, json, os, random, re, sys, time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import date

import boto3
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values

sys.path.insert(0, "/home/strakajagr/projects/equine-equalizer/backend")
from services.chart_parser import (
    extract_all_text, split_into_races, parse_race_header,
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
    """Worker: download one PDF, parse all race blocks, return list of
    (track_code, race_date_iso, race_number, race_name, conditions, grade,
     race_type)."""
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
            rows.append((
                track_code,
                file_date.isoformat(),
                hdr['race_number'],
                hdr.get('race_name'),
                hdr.get('conditions'),
                hdr.get('grade'),
                hdr.get('race_type'),
            ))
        except Exception:
            continue
    return key, None, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Write to DB. Default is dry-run (parse + report).")
    ap.add_argument("--sample", type=int, default=0,
                    help="Process only first N PDFs (for quick test).")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    print(f"=== reparse_charts — mode: "
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
          f"per-race rows: {len(all_rows):,}    "
          f"errors: {len(errors)}    "
          f"({time.perf_counter()-t0:.0f}s)")
    if errors:
        print("First 5 errors:")
        for k, e in errors[:5]:
            print(f"  {k}: {e}")

    n_with_name = sum(1 for r in all_rows if r[3])
    n_with_cond = sum(1 for r in all_rows if r[4])
    n_with_grade = sum(1 for r in all_rows if r[5] is not None)
    n = max(len(all_rows), 1)
    print(f"\nField population stats over {len(all_rows):,} race rows:")
    print(f"  race_name populated:  {n_with_name:,}  ({100*n_with_name/n:.1f}%)")
    print(f"  conditions populated: {n_with_cond:,}  ({100*n_with_cond/n:.1f}%)")
    print(f"  grade populated:      {n_with_grade:,}  ({100*n_with_grade/n:.1f}%)")

    # Distribution by race_type
    from collections import Counter
    by_type = Counter()
    by_type_named = Counter()
    by_type_graded = Counter()
    for r in all_rows:
        rt = r[6] or "?"
        by_type[rt] += 1
        if r[3]:
            by_type_named[rt] += 1
        if r[5] is not None:
            by_type_graded[rt] += 1
    print(f"\nDistribution by race_type:")
    print(f"  {'race_type':<28} {'total':>6} {'named':>6} {'graded':>7}")
    for rt, c in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {rt:<28} {c:>6} {by_type_named.get(rt,0):>6} "
              f"{by_type_graded.get(rt,0):>7}")

    print(f"\n20 random sampled rows:")
    for r in random.sample(all_rows, min(20, len(all_rows))):
        rn = (r[3] or '')[:42]
        cond = (r[4] or '')[:50]
        rt = r[6] or '?'
        gtag = f"G{r[5]}" if r[5] is not None else "  "
        print(f"  {r[1]} {r[0]:<4} R{r[2]:>2} {rt:<22} {gtag}  "
              f"name={rn!r:<44}  cond={cond!r}")

    if not args.apply:
        print("\nDRY-RUN complete. Re-run with --apply to update DB.")
        return

    print(f"\nApplying UPDATEs in batches of 1,000...", flush=True)
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    sec = json.loads(sm.get_secret_value(
        SecretId="equine-equalizer/db-credentials")["SecretString"])
    conn = psycopg2.connect(
        host=sec["host"], port=sec["port"], dbname=sec["dbname"],
        user=sec["username"], password=sec["password"],
        cursor_factory=RealDictCursor,
    )
    conn.autocommit = False
    BATCH = 1000
    n_updated = 0
    cur = conn.cursor()
    apply_t0 = time.perf_counter()
    for i in range(0, len(all_rows), BATCH):
        batch = all_rows[i:i+BATCH]
        try:
            cur.execute("CREATE TEMP TABLE IF NOT EXISTS rp_upd ("
                       "track_code varchar, race_date date, race_number int,"
                       " race_name varchar, conditions text, grade int) "
                       "ON COMMIT DROP")
            cur.execute("TRUNCATE rp_upd")
            execute_values(
                cur,
                "INSERT INTO rp_upd VALUES %s",
                [(t, d, n_, rn, c, g)
                 for (t, d, n_, rn, c, g, _rt) in batch],
                page_size=500,
            )
            cur.execute("""
              UPDATE races r SET
                race_name  = COALESCE(u.race_name,  r.race_name),
                conditions = COALESCE(u.conditions, r.conditions),
                grade      = COALESCE(u.grade,      r.grade)
              FROM rp_upd u
              JOIN tracks t ON t.track_code = u.track_code
              WHERE r.track_id    = t.track_id
                AND r.race_date   = u.race_date
                AND r.race_number = u.race_number
                AND (u.race_name  IS NOT NULL
                  OR u.conditions IS NOT NULL
                  OR u.grade      IS NOT NULL)
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
