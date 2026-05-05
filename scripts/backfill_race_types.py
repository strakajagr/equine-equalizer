#!/usr/bin/env python3
"""Re-classify race_type for all rows in the races table using the
shared classifier. Operates on the existing race_name + conditions + purse
columns. Dry-run prints counts + transition matrix + 20 random samples;
--apply commits the UPDATE in a single transaction.

Usage:
  python3 scripts/backfill_race_types.py            # dry-run
  python3 scripts/backfill_race_types.py --apply    # live
"""
from __future__ import annotations
import argparse, json, random, sys, time
from collections import Counter
import boto3, psycopg2
from psycopg2.extras import RealDictCursor, execute_values

sys.path.insert(0, "/home/strakajagr/projects/equine-equalizer/backend")
from shared.race_typing import classify_race_type


def _get_conn():
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    sec = json.loads(sm.get_secret_value(
        SecretId="equine-equalizer/db-credentials")["SecretString"])
    return psycopg2.connect(
        host=sec["host"], port=sec["port"], dbname=sec["dbname"],
        user=sec["username"], password=sec["password"],
        cursor_factory=RealDictCursor,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    apply_mode = bool(args.apply)
    print(f"=== backfill_race_types — mode: "
          f"{'APPLY' if apply_mode else 'DRY-RUN'} ===", flush=True)

    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("""
      SELECT race_id, race_date, race_number, race_name,
             conditions, purse, grade, race_type AS old_type
      FROM races
    """)
    rows = cur.fetchall()
    print(f"Loaded {len(rows):,} race rows.", flush=True)

    # Upgrade-only filter: only transitions that ADD information.
    # Old=allowance/AOC -> New=stakes/graded_stakes are the bug we're
    # fixing. All other transitions are skipped because we don't have
    # signal (chart-parsed historical rows have race_type set correctly
    # but conditions empty; running the classifier against empty input
    # would falsely downgrade them).
    UPGRADE_ALLOWED = {
        ('allowance',                   'stakes'),
        ('allowance',                   'graded_stakes'),
        ('allowance_optional_claiming', 'stakes'),
        ('allowance_optional_claiming', 'graded_stakes'),
    }

    transitions = Counter()
    new_types = []
    changed = []
    skipped = Counter()
    for r in rows:
        nt = classify_race_type(
            dist_text=None, race_name=r["race_name"],
            conditions=r["conditions"], purse=r["purse"],
            grade=r["grade"],
        )
        if nt != r["old_type"]:
            if (r["old_type"], nt) in UPGRADE_ALLOWED:
                transitions[(r["old_type"], nt)] += 1
                changed.append((r["race_id"], r["old_type"], nt, r))
                new_types.append((r["race_id"], nt))
            else:
                skipped[(r["old_type"], nt)] += 1
                # Keep existing classification; do not include in new_types.
        # else: no transition; skip

    if skipped:
        print(f"\nSkipped (out-of-scope transitions, NOT applied):")
        for (o, n), c in sorted(skipped.items(), key=lambda x: -x[1]):
            print(f"  {o:<28} -> {n:<28} {c:>8,}")

    print(f"\nTotal rows that WILL change (upgrade-only): {len(changed):,}")
    print(f"Transition matrix (old -> new), sorted by count:")
    for (o, n), c in sorted(transitions.items(), key=lambda x: -x[1]):
        print(f"  {o:<28} -> {n:<28} {c:>8,}")

    # Per-track distribution
    from collections import Counter as _C
    by_track = _C()
    cur.execute("SELECT race_id, t.track_code FROM races r JOIN tracks t ON t.track_id = r.track_id")
    track_lookup = {str(rr["race_id"]): rr["track_code"] for rr in cur.fetchall()}
    for r_id, _o, _n, _r in changed:
        by_track[track_lookup.get(str(r_id), "?")] += 1
    print(f"\nPer-track distribution of upgraded races:")
    for tc, c in sorted(by_track.items(), key=lambda x: -x[1]):
        print(f"  {tc:<8} {c:>4}")

    print(f"\n20 random sample changes:")
    for r_id, o, n, r in random.sample(changed, min(20, len(changed))):
        cond = (r["conditions"] or "")[:60].replace("\n", " ")
        purse = r["purse"] or 0
        print(f"  {o:<26} -> {n:<14} purse=${purse:>10,}  "
              f"{r['race_date']} R{r['race_number']}  cond={cond!r}")

    print(f"\nMay-2 2026 CD card (post-classify preview):")
    cur.execute("""
      SELECT r.race_id, r.race_number, r.conditions, r.purse, r.grade, r.race_type
      FROM races r JOIN tracks t ON t.track_id = r.track_id
      WHERE t.track_code = 'CD' AND r.race_date = '2026-05-02'
      ORDER BY r.race_number
    """)
    for r in cur.fetchall():
        nt = classify_race_type(
            dist_text=None, race_name=None,
            conditions=r["conditions"], purse=r["purse"],
            grade=r["grade"],
        )
        cond = (r["conditions"] or "")[:55].replace("\n", " ")
        flag = "  ←✱" if nt != r["race_type"] else ""
        print(f"  R{r['race_number']:>2} purse=${(r['purse'] or 0):>10,}  "
              f"{r['race_type']:<26} -> {nt:<26}{flag}  cond={cond!r}")

    if not apply_mode:
        print(f"\nDRY-RUN complete. Re-run with --apply to mutate.")
        cur.close(); conn.close(); return

    print(f"\nApplying UPDATE in single transaction...", flush=True)
    t0 = time.perf_counter()
    cur.execute("""
      CREATE TEMP TABLE race_type_updates (
        race_id uuid PRIMARY KEY,
        new_type varchar
      )
    """)
    execute_values(
        cur,
        "INSERT INTO race_type_updates (race_id, new_type) VALUES %s",
        [(str(r), t) for r, t in new_types],
        page_size=2000,
    )
    cur.execute("""
      UPDATE races r
      SET race_type = u.new_type
      FROM race_type_updates u
      WHERE r.race_id = u.race_id
        AND r.race_type IS DISTINCT FROM u.new_type
    """)
    print(f"  rows updated: {cur.rowcount:,}    "
          f"({time.perf_counter()-t0:.1f}s)")
    conn.commit()
    print("COMMIT OK.")
    cur.close(); conn.close()


if __name__ == "__main__":
    main()
