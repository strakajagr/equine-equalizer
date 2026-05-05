#!/usr/bin/env python3
"""Re-parse historical chart PDFs and rewrite the results table's
finish_position, call_1/2/stretch positions, and lengths-behind.

Sister to reparse_payouts.py — same PDF iteration, but updates result
positional fields (not payout fields). Used to fix the runner-line
parser bugs surfaced in Stream E1's multi-winner audit:
  - Bug B: country-suffix horses (FR, IRE, GB, JPN, BRZ, ARG…) silently
           dropped from runners table by old regex.
  - Bug C: 2-digit position disambiguation greedily wrong; runner_idx
           hint added to disambiguate winner notation.
  - Bug D: num_calls hardcoded at 4 — odds parsed as a "call" for sprint
           charts that have only 3 call columns (1/4 Str Fin).

Match strategy: (track_code, race_date, race_number, program_number)
→ entries.entry_id → results row. UPDATE-only for now. INSERT-new-horse
(SodSiren-class case) is REPORTED but NOT applied — cascade requires
inserting horse + entries rows too, and we want a separate audit pass
for those before touching the table.

Usage:
  python3 scripts/reparse_results.py --sample 50      # parse 50 PDFs, dry-run
  python3 scripts/reparse_results.py                  # parse all, dry-run report
  python3 scripts/reparse_results.py --apply          # parse all + UPDATE results
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
    """Worker: download one PDF, extract per-runner result data.

    Returns (key, error, rows) where each row is:
      (track_code, race_date_iso, race_number, program_number,
       finish_position, finish_lengths_behind,
       call_1_position, call_1_lengths,
       call_2_position, call_2_lengths,
       stretch_position, stretch_lengths)
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
            for runner in hdr['runners']:
                positions = runner.get('calls', [])
                lengths   = runner.get('call_lengths', [None] * len(positions))
                c1     = positions[0] if len(positions) > 0 else None
                c1_len = lengths[0]   if len(lengths) > 0 else None
                c2     = positions[1] if len(positions) > 1 else None
                c2_len = lengths[1]   if len(lengths) > 1 else None
                stretch     = positions[-2] if len(positions) >= 2 else None
                stretch_len = lengths[-2]   if len(lengths) >= 2 else None
                fin     = runner.get('finish_position')
                fin_len = runner.get('finish_lengths_behind')

                if fin is None:
                    continue

                rows.append((
                    track_code, file_date.isoformat(), hdr['race_number'],
                    str(runner.get('program_number') or ''),
                    fin, fin_len,
                    c1, c1_len, c2, c2_len, stretch, stretch_len,
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

    print(f"=== reparse_results — mode: "
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

    print(f"\nParse done. PDFs: {len(keys):,}    rows: {len(all_rows):,}    "
          f"errors: {len(errors)}    ({time.perf_counter()-t0:.0f}s)")

    # ─── Pre-flight: count UPDATEable vs would-be-INSERT cases ────────
    print("\nMatching parsed rows against existing entries...", flush=True)
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    sec = json.loads(sm.get_secret_value(
        SecretId="equine-equalizer/db-credentials")["SecretString"])
    conn = psycopg2.connect(
        host=sec["host"], port=sec["port"], dbname=sec["dbname"],
        user=sec["username"], password=sec["password"],
        cursor_factory=RealDictCursor,
    )
    conn.autocommit = False
    cur = conn.cursor()

    # Stage all rows in temp table
    cur.execute("""CREATE TEMP TABLE rp_res (
        track_code varchar, race_date date, race_number int,
        program_number varchar,
        finish_position int, finish_lengths numeric,
        call_1_position int, call_1_lengths numeric,
        call_2_position int, call_2_lengths numeric,
        stretch_position int, stretch_lengths numeric
    ) ON COMMIT PRESERVE ROWS""")
    execute_values(
        cur,
        "INSERT INTO rp_res VALUES %s",
        all_rows, page_size=2000,
    )

    # Count UPDATEs — rows where the existing results row exists AND
    # the new positional fields differ.
    cur.execute("""
      WITH joined AS (
        SELECT u.*, res.entry_id AS existing_entry_id, res.finish_position AS old_fin
        FROM rp_res u
        JOIN tracks t ON t.track_code = u.track_code
        JOIN races r ON r.track_id = t.track_id
                     AND r.race_date = u.race_date
                     AND r.race_number = u.race_number
        LEFT JOIN entries e ON e.race_id = r.race_id
                            AND e.program_number = u.program_number
        LEFT JOIN results res ON res.entry_id = e.entry_id
      )
      SELECT
        COUNT(*) AS total,
        COUNT(*) FILTER (WHERE existing_entry_id IS NOT NULL) AS would_update,
        COUNT(*) FILTER (WHERE existing_entry_id IS NOT NULL
                          AND old_fin IS DISTINCT FROM finish_position) AS pos_changed,
        COUNT(*) FILTER (WHERE existing_entry_id IS NULL) AS no_existing_entry
      FROM joined
    """)
    counts = cur.fetchone()
    print(f"\n  parsed rows: {counts['total']:,}")
    print(f"  UPDATEable (existing entries): {counts['would_update']:,}")
    print(f"    of which finish_position would change: {counts['pos_changed']:,}")
    print(f"  NO matching entries (cascade — would need horse+entries inserts): "
          f"{counts['no_existing_entry']:,}")

    # ─── Track concentration of changes ───────────────────────────────
    # If finish_position changes cluster on one track, that points to a
    # layout-specific runner-line bug we haven't caught yet.
    cur.execute("""
      SELECT u.track_code,
             COUNT(*) FILTER (WHERE res.entry_id IS NOT NULL) AS would_update,
             COUNT(*) FILTER (WHERE res.entry_id IS NOT NULL
                               AND res.finish_position IS DISTINCT FROM u.finish_position)
                 AS pos_changed,
             COUNT(*) FILTER (WHERE e.entry_id IS NULL) AS cascade_miss
      FROM rp_res u
      JOIN tracks t ON t.track_code = u.track_code
      JOIN races r ON r.track_id = t.track_id
                   AND r.race_date = u.race_date
                   AND r.race_number = u.race_number
      LEFT JOIN entries e ON e.race_id = r.race_id
                          AND e.program_number = u.program_number
      LEFT JOIN results res ON res.entry_id = e.entry_id
      GROUP BY u.track_code
      ORDER BY pos_changed DESC, would_update DESC
    """)
    track_rows = cur.fetchall()
    print(f"\nPer-track concentration (sorted by finish_position changes):")
    print(f"  {'tk':<5} {'updates':>9} {'pos_chg':>8} {'pos_chg %':>10} {'cascade':>9}")
    for r in track_rows:
        upd = r['would_update'] or 0
        chg = r['pos_changed'] or 0
        pct = (chg / upd * 100) if upd else 0
        print(f"  {r['track_code']:<5} {upd:>9,} {chg:>8,} {pct:>9.2f}% {r['cascade_miss']:>9,}")

    # Top 20 dates with most finish_position changes — clustering by date
    # would indicate a session-level or chart-layout-version glitch.
    cur.execute("""
      SELECT u.race_date, u.track_code,
             COUNT(*) FILTER (WHERE res.entry_id IS NOT NULL
                               AND res.finish_position IS DISTINCT FROM u.finish_position)
                 AS pos_changed
      FROM rp_res u
      JOIN tracks t ON t.track_code = u.track_code
      JOIN races r ON r.track_id = t.track_id
                   AND r.race_date = u.race_date
                   AND r.race_number = u.race_number
      LEFT JOIN entries e ON e.race_id = r.race_id
                          AND e.program_number = u.program_number
      LEFT JOIN results res ON res.entry_id = e.entry_id
      GROUP BY u.race_date, u.track_code
      HAVING COUNT(*) FILTER (WHERE res.entry_id IS NOT NULL
                               AND res.finish_position IS DISTINCT FROM u.finish_position) > 0
      ORDER BY pos_changed DESC
      LIMIT 20
    """)
    date_rows = cur.fetchall()
    print(f"\nTop 20 (date, track) by finish_position changes:")
    print(f"  {'date':<11} {'tk':<5} {'pos_chg':>8}")
    for r in date_rows:
        print(f"  {r['race_date']} {r['track_code']:<5} {r['pos_changed']:>8,}")

    # Sample 30 changes — for human eyeball
    cur.execute("""
      SELECT u.track_code, u.race_date, u.race_number, u.program_number,
             u.finish_position AS new_fin, res.finish_position AS old_fin,
             u.call_1_position AS new_c1, res.call_1_position AS old_c1,
             u.call_2_position AS new_c2, res.call_2_position AS old_c2,
             u.stretch_position AS new_str, res.stretch_position AS old_str,
             h.horse_name
      FROM rp_res u
      JOIN tracks t ON t.track_code = u.track_code
      JOIN races r ON r.track_id = t.track_id
                   AND r.race_date = u.race_date
                   AND r.race_number = u.race_number
      JOIN entries e ON e.race_id = r.race_id
                     AND e.program_number = u.program_number
      JOIN horses h ON h.horse_id = e.horse_id
      JOIN results res ON res.entry_id = e.entry_id
      WHERE res.finish_position IS DISTINCT FROM u.finish_position
         OR res.call_1_position IS DISTINCT FROM u.call_1_position
         OR res.call_2_position IS DISTINCT FROM u.call_2_position
         OR res.stretch_position IS DISTINCT FROM u.stretch_position
      ORDER BY RANDOM() LIMIT 30
    """)
    samples = cur.fetchall()
    print(f"\n30 sample changes (UPDATEs):")
    print(f"  {'date':<11} {'tk':<4} {'R':>3} {'pgm':>3} {'horse':<22}  fin: old → new   c1: old→new   str: old→new")
    for s in samples:
        print(f"  {s['race_date']} {s['track_code']:<4} R{s['race_number']:>2} "
              f"{s['program_number']:>3} {s['horse_name'][:22]:<22}  "
              f"{str(s['old_fin']):>3} → {str(s['new_fin']):>3}    "
              f"{str(s['old_c1']):>3} → {str(s['new_c1']):>3}    "
              f"{str(s['old_str']):>3} → {str(s['new_str']):>3}")

    # Sample 10 no-match (cascade) cases
    cur.execute("""
      SELECT u.track_code, u.race_date, u.race_number, u.program_number,
             u.finish_position AS fin
      FROM rp_res u
      JOIN tracks t ON t.track_code = u.track_code
      JOIN races r ON r.track_id = t.track_id
                   AND r.race_date = u.race_date
                   AND r.race_number = u.race_number
      LEFT JOIN entries e ON e.race_id = r.race_id
                          AND e.program_number = u.program_number
      WHERE e.entry_id IS NULL
      ORDER BY RANDOM() LIMIT 10
    """)
    misses = cur.fetchall()
    if misses:
        print(f"\n10 sample no-match cases (would need cascade INSERT):")
        for m in misses:
            print(f"  {m['race_date']} {m['track_code']:<4} R{m['race_number']:>2} "
                  f"pgm={m['program_number']:>3} fin={m['fin']}")

    if not args.apply:
        print("\nDRY-RUN complete. Re-run with --apply to commit UPDATEs.")
        cur.close(); conn.close()
        return

    # ─── Apply: UPDATE only. NO inserts (cascade is out of scope). ─────
    print(f"\nApplying UPDATEs to results table...", flush=True)
    apply_t0 = time.perf_counter()
    cur.execute("""
      UPDATE results res SET
        finish_position    = u.finish_position,
        lengths_behind     = u.finish_lengths,
        call_1_position    = u.call_1_position,
        call_1_lengths     = u.call_1_lengths,
        call_2_position    = u.call_2_position,
        call_2_lengths     = u.call_2_lengths,
        stretch_position   = u.stretch_position,
        stretch_lengths    = u.stretch_lengths
      FROM rp_res u
      JOIN tracks t   ON t.track_code = u.track_code
      JOIN races r    ON r.track_id   = t.track_id
                      AND r.race_date = u.race_date
                      AND r.race_number = u.race_number
      JOIN entries e  ON e.race_id    = r.race_id
                      AND e.program_number = u.program_number
      WHERE res.entry_id = e.entry_id
        AND (res.finish_position IS DISTINCT FROM u.finish_position
          OR res.call_1_position IS DISTINCT FROM u.call_1_position
          OR res.call_2_position IS DISTINCT FROM u.call_2_position
          OR res.stretch_position IS DISTINCT FROM u.stretch_position
          OR res.lengths_behind IS DISTINCT FROM u.finish_lengths)
    """)
    n_updated = cur.rowcount
    conn.commit()
    print(f"  rows UPDATEd: {n_updated:,}    "
          f"({time.perf_counter()-apply_t0:.0f}s)")
    cur.close(); conn.close()


if __name__ == "__main__":
    main()
