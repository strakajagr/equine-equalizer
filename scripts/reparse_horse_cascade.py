#!/usr/bin/env python3
"""Re-parse all 2,755 chart PDFs in S3 and cascade-upsert horses + jockeys
+ trainers + entries + results + past_performances using the patched
chart_parser (E + F + G).

This is a thin wrapper around chart_parser.process_pdf — process_pdf
already implements the full idempotent cascade with proper ON CONFLICT
semantics. This script provides:

  Phase 1 (--dry-run): re-parse all PDFs, cross-check identities vs DB,
                       enumerate counts and sample 30 of each missing class.
  Phase 2 (--dry-run continues): per-horse race-history enumeration.
                       Sanity-check sample 30 horses with their full history.
  Phase 3 (--apply only): call process_pdf for every PDF — per-race
                       atomic transactions, idempotent on existing data.
  Phase 4 (after --apply): per-horse integrity verification.

Resolves DEFERRED BUG #8 (country-suffix horse cascade) + Bug G (nested-
paren jockey rows). The patched parser correctly extracts these runners;
the cascade brings their identities + entries + PP rows into the DB.

Usage:
  --sample N        # process first N PDFs (test)
  --dry-run         # default: Phases 1+2 only, no writes
  --apply           # commits via process_pdf
  --workers N       # parallelism for parse step (default 8)
  --phase {1,2,3,4} # subset of phases (default: 1+2 dry-run, 3+4 apply)
"""
from __future__ import annotations
import argparse, io, json, os, re, sys, time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

import boto3
import psycopg2
from psycopg2.extras import RealDictCursor

sys.path.insert(0, "/home/strakajagr/projects/equine-equalizer/backend")
from services.chart_parser import (
    extract_all_text, split_into_races, parse_race_header,
    find_trainer_for_pgm, normalize_horse_name, horse_match_key,
    process_pdf,
)

S3_BUCKET = "equine-raw-data"
S3_PREFIX = "charts/"
PDF_NAME_RE = re.compile(r'^([A-Z]+)_(\d{8})\.pdf$')


# ─── Phase-1 / Phase-2 worker: re-parse one PDF ──────────────────────
def _parse_one_pdf(key: str) -> tuple[str, str | None, list]:
    """Worker: download one PDF, extract per-runner identity tuples.
    Returns (key, error, rows) where each row is dict:
      {file_date, track_code, race_number, program_number,
       horse_name, jockey_name, trainer_name, finish_position}
    """
    s3 = boto3.client("s3")
    base = os.path.basename(key)
    m = PDF_NAME_RE.match(base)
    if not m:
        return key, None, []
    track_code = m.group(1)
    from datetime import date
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
                trainer_name = (
                    find_trainer_for_pgm(b, str(runner['program_number']))
                    or 'Unknown'
                )
                rows.append({
                    'file_date': file_date.isoformat(),
                    'track_code': track_code,
                    'race_number': hdr['race_number'],
                    'program_number': str(runner['program_number']),
                    'horse_name': runner['horse_name'],
                    'jockey_name': runner['jockey_name'],
                    'trainer_name': trainer_name,
                    'finish_position': runner['finish_position'],
                })
        except Exception:
            continue
    return key, None, rows


def _list_pdfs():
    s3 = boto3.client("s3")
    keys = []
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=S3_PREFIX):
        for obj in page.get("Contents", []):
            if obj["Key"].endswith(".pdf"):
                keys.append(obj["Key"])
    return keys


# ─── DB cross-check helpers ───────────────────────────────────────────
def _get_conn():
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    sec = json.loads(sm.get_secret_value(
        SecretId="equine-equalizer/db-credentials")["SecretString"])
    return psycopg2.connect(
        host=sec["host"], port=sec["port"], dbname=sec["dbname"],
        user=sec["username"], password=sec["password"],
        cursor_factory=RealDictCursor,
    )


def phase_1_2_dry_run(args):
    """Re-parse all PDFs in parallel, then cross-check parsed identities
    against the DB to enumerate missing horses, jockeys, trainers, entries.
    """
    print(f"=== reparse_horse_cascade — DRY-RUN ===", flush=True)
    keys = _list_pdfs()
    if args.sample:
        keys = keys[:args.sample]
    print(f"PDFs to process: {len(keys):,}", flush=True)

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
                      f"runners={len(all_rows):,}", flush=True)

    print(f"\nParse done. PDFs: {len(keys):,} runners: {len(all_rows):,} "
          f"errors: {len(errors)} ({time.perf_counter()-t0:.0f}s)")

    # ─── Phase 1: cross-check identities vs DB ───────────────────────
    print(f"\n{'='*72}\nPhase 1 — Missing-identity enumeration\n{'='*72}")
    parsed_horses   = {r['horse_name'] for r in all_rows}
    parsed_jockeys  = {r['jockey_name'] for r in all_rows}
    parsed_trainers = {r['trainer_name'] for r in all_rows}

    print(f"  distinct parsed horses:   {len(parsed_horses):,}")
    print(f"  distinct parsed jockeys:  {len(parsed_jockeys):,}")
    print(f"  distinct parsed trainers: {len(parsed_trainers):,}")

    conn = _get_conn()
    cur = conn.cursor()

    # Existing horses (by match_key)
    cur.execute("SELECT horse_name FROM horses")
    existing_horse_keys = {
        horse_match_key(r['horse_name']) for r in cur.fetchall()
    }
    missing_horses = sorted(
        h for h in parsed_horses
        if horse_match_key(h) not in existing_horse_keys
    )
    print(f"\n  missing horses (no matching key in DB): {len(missing_horses):,}")
    print("  Sample 30 missing horses:")
    import random
    sample = random.sample(missing_horses, min(30, len(missing_horses)))
    for h in sample:
        print(f"    {h}")

    # Existing jockeys (case-insensitive)
    cur.execute("SELECT jockey_name FROM jockeys")
    existing_jockey_lc = {r['jockey_name'].lower() for r in cur.fetchall()}
    missing_jockeys = sorted(
        j for j in parsed_jockeys if j.lower() not in existing_jockey_lc
    )
    print(f"\n  missing jockeys: {len(missing_jockeys):,}")
    print("  Sample 30 missing jockeys:")
    sample = random.sample(missing_jockeys, min(30, len(missing_jockeys)))
    for j in sample:
        print(f"    {j}")

    # Existing trainers (case-insensitive)
    cur.execute("SELECT trainer_name FROM trainers")
    existing_trainer_lc = {r['trainer_name'].lower() for r in cur.fetchall()}
    missing_trainers = sorted(
        t for t in parsed_trainers if t.lower() not in existing_trainer_lc
    )
    print(f"\n  missing trainers: {len(missing_trainers):,}")
    print("  Sample 30 missing trainers:")
    sample = random.sample(missing_trainers, min(30, len(missing_trainers)))
    for t in sample:
        print(f"    {t}")

    # Missing entries: parsed runner has no entries row by
    # (track_code, race_date, race_number, program_number) → resolved
    # via horse_match_key intersection too (since horse may need cascade).
    # We'll count entries-rows by resolving (race_id, horse_id) per parsed
    # runner.
    print(f"\n  Computing missing-entries count... (this may take a moment)")
    cur.execute("""
      CREATE TEMP TABLE rp_parsed (
        race_date date, track_code varchar, race_number int,
        program_number varchar, horse_name varchar
      ) ON COMMIT DROP
    """)
    from psycopg2.extras import execute_values
    execute_values(
        cur,
        "INSERT INTO rp_parsed VALUES %s",
        [
            (r['file_date'], r['track_code'], r['race_number'],
             r['program_number'], r['horse_name'])
            for r in all_rows
        ],
        page_size=2000,
    )
    cur.execute("""
      SELECT COUNT(*) AS n FROM (
        SELECT p.race_date, p.track_code, p.race_number, p.program_number
        FROM rp_parsed p
        LEFT JOIN tracks t ON t.track_code = p.track_code
        LEFT JOIN races r  ON r.track_id = t.track_id
                          AND r.race_date = p.race_date
                          AND r.race_number = p.race_number
        LEFT JOIN entries e ON e.race_id = r.race_id
                            AND e.program_number = p.program_number
        WHERE e.entry_id IS NULL
      ) sub
    """)
    missing_entries_count = cur.fetchone()['n']
    print(f"  missing entries (no entries row for this parsed runner): "
          f"{missing_entries_count:,}")

    cur.execute("""
      SELECT p.race_date, p.track_code, p.race_number, p.program_number,
             p.horse_name
      FROM rp_parsed p
      LEFT JOIN tracks t ON t.track_code = p.track_code
      LEFT JOIN races r  ON r.track_id = t.track_id
                        AND r.race_date = p.race_date
                        AND r.race_number = p.race_number
      LEFT JOIN entries e ON e.race_id = r.race_id
                          AND e.program_number = p.program_number
      WHERE e.entry_id IS NULL
      ORDER BY RANDOM()
      LIMIT 30
    """)
    print(f"  Sample 30 missing-entries rows:")
    for r in cur.fetchall():
        print(f"    {r['race_date']} {r['track_code']:<4} R{r['race_number']:>2}"
              f" pgm={r['program_number']:>3}  {r['horse_name']}")

    # ─── Phase 2: per-horse race-history enumeration ──────────────────
    print(f"\n{'='*72}\nPhase 2 — Per-horse race history (for missing horses)\n{'='*72}")
    horse_to_races = defaultdict(list)
    for r in all_rows:
        if horse_match_key(r['horse_name']) not in existing_horse_keys:
            horse_to_races[r['horse_name']].append(
                (r['file_date'], r['track_code'], r['race_number'],
                 r['finish_position'])
            )

    counts = Counter(len(v) for v in horse_to_races.values())
    print(f"  distinct missing horses: {len(horse_to_races):,}")
    print(f"  races-per-horse distribution:")
    for k in sorted(counts):
        print(f"    {k} race{'' if k == 1 else 's'}: {counts[k]:,} horses")

    print(f"\n  Sample 30 horses with race history:")
    sampled_horses = random.sample(
        list(horse_to_races.keys()),
        min(30, len(horse_to_races))
    )
    for h in sampled_horses:
        races = horse_to_races[h]
        races.sort()
        print(f"\n  {h}  ({len(races)} race{'' if len(races)==1 else 's'}):")
        for r in races[:10]:
            print(f"    {r[0]} {r[1]:<4} R{r[2]:>2} fin={r[3]}")
        if len(races) > 10:
            print(f"    ... +{len(races)-10} more")

    cur.close()
    conn.close()
    print(f"\n{'='*72}\nDRY-RUN complete. Tony reviews counts + samples.\n"
          f"{'='*72}")


def phase_3_apply(args):
    """Re-run process_pdf for every PDF. Idempotent. Reports per-PDF stats."""
    print(f"=== reparse_horse_cascade — APPLY (Phase 3) ===", flush=True)
    keys = _list_pdfs()
    if args.sample:
        keys = keys[:args.sample]
    print(f"PDFs to process: {len(keys):,}")

    s3 = boto3.client("s3")
    conn = _get_conn()
    conn.autocommit = False  # process_pdf manages its own commits per-race

    total = {'races_loaded': 0, 'runners_loaded': 0, 'errors': 0}
    t0 = time.perf_counter()
    for i, key in enumerate(keys):
        filename = key.split('/')[-1]
        try:
            body = s3.get_object(Bucket=S3_BUCKET, Key=key)["Body"].read()
        except Exception as e:
            print(f"  [{i+1}/{len(keys)}] {filename} download FAILED: {e}")
            total['errors'] += 1
            continue
        try:
            summary = process_pdf(conn, io.BytesIO(body), filename)
            total['races_loaded']   += summary.get('races_loaded', 0)
            total['runners_loaded'] += summary.get('runners_loaded', 0)
            total['errors']         += len(summary.get('errors', []))
            if (i + 1) % 100 == 0:
                print(f"  [{i+1}/{len(keys)}] races={total['races_loaded']} "
                      f"runners={total['runners_loaded']} "
                      f"errs={total['errors']} "
                      f"({time.perf_counter()-t0:.0f}s)", flush=True)
        except Exception as e:
            print(f"  [{i+1}/{len(keys)}] {filename} CRASH: {e}", flush=True)
            conn.rollback()
            total['errors'] += 1

    print(f"\nApply done. races_loaded={total['races_loaded']:,} "
          f"runners_loaded={total['runners_loaded']:,} "
          f"errors={total['errors']:,} "
          f"({time.perf_counter()-t0:.0f}s)")
    conn.close()


def phase_4_verify(args):
    """Per-horse integrity verification post-apply."""
    print(f"=== reparse_horse_cascade — VERIFY (Phase 4) ===")
    conn = _get_conn()
    cur = conn.cursor()

    # Country-suffix-or-coupled-pgm horses: count entries vs PPs vs results
    cur.execute("""
      SELECT
        COUNT(*) FILTER (WHERE h.horse_name LIKE '%(%)%') AS country_suffix_horses,
        COUNT(*) AS total_horses
      FROM horses h
    """)
    r = cur.fetchone()
    print(f"  total horses: {r['total_horses']:,}")
    print(f"  country-suffix horses: {r['country_suffix_horses']:,}")

    cur.execute("""
      SELECT COUNT(*) AS no_entries FROM horses h
      WHERE NOT EXISTS (
        SELECT 1 FROM entries e WHERE e.horse_id = h.horse_id
      )
    """)
    print(f"  horses with NO entries rows: {cur.fetchone()['no_entries']:,}")

    cur.execute("""
      SELECT COUNT(*) AS no_pps FROM horses h
      WHERE NOT EXISTS (
        SELECT 1 FROM past_performances p WHERE p.horse_id = h.horse_id
      )
    """)
    print(f"  horses with NO past_performances: {cur.fetchone()['no_pps']:,}")

    # Re-run multi-winner / missing-winner integrity checks
    cur.execute("""
      SELECT COUNT(*) AS n FROM races r
      WHERE r.race_date >= '2022-01-01'
        AND r.race_date < CURRENT_DATE
        AND EXISTS (
            SELECT 1 FROM entries e
            JOIN results res ON res.entry_id = e.entry_id
            WHERE e.race_id = r.race_id
        )
        AND NOT EXISTS (
            SELECT 1 FROM entries e
            JOIN results res ON res.entry_id = e.entry_id
            WHERE e.race_id = r.race_id AND res.finish_position = 1
        )
    """)
    print(f"  missing-winner races (target 0): {cur.fetchone()['n']:,}")

    cur.close(); conn.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Run Phase 3 cascade-upsert. Default: dry-run only.")
    ap.add_argument("--sample", type=int, default=0,
                    help="Process only first N PDFs (test).")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--phase", type=int, choices=[1,2,3,4], default=0,
                    help="Run specific phase only. 0=auto (1+2 dry, 3+4 apply).")
    args = ap.parse_args()

    if args.phase in (0, 1, 2):
        phase_1_2_dry_run(args)
    if args.apply or args.phase in (3, 4):
        if args.apply:
            phase_3_apply(args)
        phase_4_verify(args)


if __name__ == "__main__":
    main()
