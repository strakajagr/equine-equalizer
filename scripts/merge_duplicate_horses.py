#!/usr/bin/env python3
"""One-shot dedup of horse rows that share an aggressive match key.

Bug context: prior ingestion had two name-normalization paths (HRN entries
preserved spaces, chart_parser stripped them when pdftotext collapsed
whitespace). Result: same horse stored under multiple horse_ids — entries
under one, past_performances under another. See
/tmp/pp_horse_dup_scale.py for the diagnostic.

The script:
  1. Buckets horses by horse_match_key (lowercase + alphanumeric-only).
  2. Within each bucket of >=2 rows, picks a canonical winner:
        - PRIMARY:   horse_name contains internal whitespace
                     (i.e. the human-readable variant).
        - TIEBREAK1: most past_performances.
        - TIEBREAK2: oldest created_at.
  3. For each (winner,loser) entry pair colliding on the same race:
        a. RECONCILE 10 fields onto the winner entry:
             - non-boolean (post_position, program_number,
               morning_line_odds, weight_carried, jockey_id,
               trainer_id): COALESCE(winner, loser) — winner wins if
               non-null, else loser fills the gap.
             - boolean (lasix, blinkers_on, equipment_change_from_last,
               is_scratched): winner OR loser — any TRUE wins, since
               schema FALSE is the default-never-set.
             - 11 same-populated-count value-conflict pairs: winner
               wins (canonical rule).
        b. Delete dependent predictions / results / wr/pl/ls predictions
           on the loser entry (entry_id-unique constraints would
           otherwise violate the next step).
        c. Delete the loser entry (the (race_id, horse_id) unique
           constraint would otherwise violate the FK redirect).
     Field-level changes are appended to an audit CSV at
     /tmp/merge_field_changes.csv (entry_id, field_name, before, after).
  4. Drop loser PPs colliding with winner PPs on
     (race_date, track_code, race_number).
  5. Drop loser workouts colliding on
     (workout_date, track_code, distance_furlongs).
  6. UPDATE every horse_id reference loser -> winner across entries,
     past_performances, workouts, results, predictions, wr_predictions,
     pl_predictions, ls_predictions, plus sire_id/dam_id/dam_sire_id
     self-references on horses.
  7. DELETE the loser horse rows.
  8. Wraps everything in a single transaction so it's atomic.

Run modes:
  --dry-run (default): all SELECTs run, audit CSV written, no DB
    mutation. ROLLBACK at the end.
  --apply: actually mutate; COMMIT at the end.

Usage:
  python3 scripts/merge_duplicate_horses.py            # dry-run
  python3 scripts/merge_duplicate_horses.py --apply    # live
"""
from __future__ import annotations
import argparse
import csv
import json
import random
import sys
import time
from collections import Counter, defaultdict
from typing import List

import boto3
import psycopg2
from psycopg2.extras import RealDictCursor

# Tables whose horse_id column must be redirected loser -> winner.
HORSE_FK_TABLES = [
    "entries", "past_performances", "workouts", "results",
    "predictions", "wr_predictions", "pl_predictions", "ls_predictions",
]
HORSE_SELF_REFS = ["sire_id", "dam_id", "dam_sire_id"]
ENTRY_DEPENDENT_TABLES = [
    "predictions", "wr_predictions", "pl_predictions",
    "ls_predictions", "results",
]

# Field-reconcile rules. (column_name, kind)
NON_BOOL_FIELDS = [
    "post_position", "program_number", "morning_line_odds",
    "weight_carried", "jockey_id", "trainer_id",
]
BOOL_FIELDS = [
    "lasix", "blinkers_on", "equipment_change_from_last", "is_scratched",
]

AUDIT_PATH = "/tmp/merge_field_changes.csv"


def _get_conn():
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    sec = json.loads(
        sm.get_secret_value(SecretId="equine-equalizer/db-credentials")[
            "SecretString"
        ]
    )
    return psycopg2.connect(
        host=sec["host"], port=sec["port"], dbname=sec["dbname"],
        user=sec["username"], password=sec["password"],
        cursor_factory=RealDictCursor,
    )


def _stage_winners_and_losers(cur):
    cur.execute("DROP TABLE IF EXISTS dup_pairs")
    cur.execute("""
      CREATE TEMP TABLE dup_pairs (
          loser_id   uuid PRIMARY KEY,
          winner_id  uuid NOT NULL
      )
    """)
    cur.execute("""
      WITH base AS (
        SELECT
          h.horse_id, h.horse_name, h.created_at,
          REGEXP_REPLACE(LOWER(h.horse_name), '[^a-z0-9]', '', 'g') AS mkey,
          (h.horse_name LIKE '%' || ' ' || '%') AS has_space,
          (SELECT COUNT(*) FROM past_performances pp
           WHERE pp.horse_id = h.horse_id) AS pp_count
        FROM horses h
        WHERE h.horse_name IS NOT NULL
          AND REGEXP_REPLACE(LOWER(h.horse_name), '[^a-z0-9]', '', 'g') <> ''
      ),
      buckets AS (
        SELECT mkey FROM base GROUP BY mkey HAVING COUNT(*) >= 2
      ),
      ranked AS (
        SELECT b.*,
               ROW_NUMBER() OVER (
                 PARTITION BY b.mkey
                 ORDER BY b.has_space DESC, b.pp_count DESC,
                          b.created_at ASC NULLS LAST
               ) AS rk
        FROM base b
        JOIN buckets bk ON bk.mkey = b.mkey
      )
      INSERT INTO dup_pairs (loser_id, winner_id)
      SELECT r.horse_id,
             (SELECT horse_id FROM ranked w WHERE w.mkey = r.mkey AND w.rk = 1)
      FROM ranked r
      WHERE r.rk > 1
    """)
    cur.execute("SELECT COUNT(*) AS n FROM dup_pairs")
    n_losers = cur.fetchone()["n"]
    cur.execute("SELECT COUNT(DISTINCT winner_id) AS n FROM dup_pairs")
    n_winners = cur.fetchone()["n"]
    return n_winners, n_losers


def _aggregate_collisions(cur):
    cur.execute("""
      SELECT COUNT(*) AS n
      FROM dup_pairs dp
      JOIN entries e_dupe ON e_dupe.horse_id = dp.loser_id
      JOIN entries e_keep ON e_keep.horse_id = dp.winner_id
                          AND e_keep.race_id = e_dupe.race_id
    """)
    entries_collide = cur.fetchone()["n"]

    cur.execute("""
      SELECT COUNT(*) AS n
      FROM dup_pairs dp
      JOIN past_performances pp_d ON pp_d.horse_id = dp.loser_id
      JOIN past_performances pp_k ON pp_k.horse_id = dp.winner_id
                                  AND pp_k.race_date  = pp_d.race_date
                                  AND pp_k.track_code = pp_d.track_code
                                  AND pp_k.race_number = pp_d.race_number
    """)
    pps_collide = cur.fetchone()["n"]

    cur.execute("""
      SELECT COUNT(*) AS n
      FROM dup_pairs dp
      JOIN workouts w_d ON w_d.horse_id = dp.loser_id
      JOIN workouts w_k ON w_k.horse_id = dp.winner_id
                        AND w_k.workout_date     = w_d.workout_date
                        AND w_k.track_code       = w_d.track_code
                        AND w_k.distance_furlongs = w_d.distance_furlongs
    """)
    workouts_collide = cur.fetchone()["n"]

    return entries_collide, pps_collide, workouts_collide


def _aggregate_redirects(cur):
    counts = {}
    for tbl in HORSE_FK_TABLES:
        cur.execute(
            f"SELECT COUNT(*) AS n FROM {tbl} t "
            f"JOIN dup_pairs dp ON t.horse_id = dp.loser_id"
        )
        counts[tbl] = cur.fetchone()["n"]
    for col in HORSE_SELF_REFS:
        cur.execute(
            f"SELECT COUNT(*) AS n FROM horses h "
            f"JOIN dup_pairs dp ON h.{col} = dp.loser_id"
        )
        counts[f"horses.{col}"] = cur.fetchone()["n"]
    return counts


def _reconcile_value(field: str, w_val, l_val, is_bool: bool):
    """Apply the reconcile rule. Returns the new winner-row value."""
    if is_bool:
        # B1 — winner OR loser (any TRUE wins; FALSE treated as default-never-set)
        return bool(w_val) or bool(l_val)
    # COALESCE(winner, loser); winner-wins on conflicts (both non-null).
    return w_val if w_val is not None else l_val


def _reconcile_colliding_entries(cur, apply_mode: bool):
    """Field-by-field reconcile of winner entries with their colliding
    loser entries, then delete loser entries (and their dependents).

    Writes per-field changes to AUDIT_PATH. Returns summary dict.
    """
    select_cols_w = ", ".join([f"e_keep.{c} AS w_{c}"
                              for c in NON_BOOL_FIELDS + BOOL_FIELDS])
    select_cols_l = ", ".join([f"e_dupe.{c} AS l_{c}"
                              for c in NON_BOOL_FIELDS + BOOL_FIELDS])
    cur.execute(f"""
      SELECT
        e_keep.entry_id AS w_entry_id,
        e_keep.race_id  AS race_id,
        dp.winner_id, dp.loser_id,
        e_dupe.entry_id AS l_entry_id,
        {select_cols_w},
        {select_cols_l}
      FROM dup_pairs dp
      JOIN entries e_dupe ON e_dupe.horse_id = dp.loser_id
      JOIN entries e_keep ON e_keep.horse_id = dp.winner_id
                          AND e_keep.race_id = e_dupe.race_id
    """)
    pairs = cur.fetchall()

    # Compute reconciled values + audit log entries.
    audit_rows = []  # (winner_entry_id, field, before, after)
    pairs_with_changes = 0
    pairs_no_change = 0
    field_change_counts = Counter()
    sanity_violations = []  # winner entries whose populated-field count drops

    def _populated_count(d, prefix):
        n = 0
        for f in NON_BOOL_FIELDS:
            if d[f"{prefix}{f}"] is not None:
                n += 1
        for f in BOOL_FIELDS:
            if bool(d[f"{prefix}{f}"]):
                n += 1
        return n

    pair_updates = []  # list of (winner_entry_id, {field: new_val}) to apply
    for r in pairs:
        new_vals = {}
        changed_any = False
        before_count = _populated_count(r, "w_")
        for f in NON_BOOL_FIELDS:
            w = r[f"w_{f}"]
            l = r[f"l_{f}"]
            new_v = _reconcile_value(f, w, l, is_bool=False)
            new_vals[f] = new_v
            if (w is None) != (new_v is None) or (w is not None and w != new_v):
                # COALESCE only changes when winner was null.
                # Winner-wins on conflict means new_v == w when both non-null,
                # so no change recorded for those.
                if w != new_v:
                    audit_rows.append(
                        (str(r["w_entry_id"]), f, _fmt(w), _fmt(new_v))
                    )
                    field_change_counts[f] += 1
                    changed_any = True
        for f in BOOL_FIELDS:
            w = bool(r[f"w_{f}"])
            l = bool(r[f"l_{f}"])
            new_v = w or l
            new_vals[f] = new_v
            if new_v != w:
                audit_rows.append(
                    (str(r["w_entry_id"]), f, _fmt(w), _fmt(new_v))
                )
                field_change_counts[f] += 1
                changed_any = True

        # Sanity: after reconcile, populated count cannot drop.
        # Reconstruct hypothetical "after" row.
        after_row = dict(r)
        for f, v in new_vals.items():
            after_row[f"w_{f}"] = v
        after_count = _populated_count(after_row, "w_")
        if after_count < before_count:
            sanity_violations.append((
                str(r["w_entry_id"]), before_count, after_count
            ))

        if changed_any:
            pairs_with_changes += 1
            pair_updates.append((r["w_entry_id"], new_vals))
        else:
            pairs_no_change += 1

    # Write audit CSV (always, even in dry-run).
    with open(AUDIT_PATH, "w", newline="") as fh:
        wcsv = csv.writer(fh)
        wcsv.writerow(["entry_id", "field", "before", "after"])
        wcsv.writerows(audit_rows)

    summary = {
        "pair_count": len(pairs),
        "pairs_with_changes": pairs_with_changes,
        "pairs_no_change": pairs_no_change,
        "audit_rows": len(audit_rows),
        "field_change_counts": dict(field_change_counts),
        "sanity_violations": sanity_violations,
    }

    if not apply_mode:
        return summary, pairs

    # ── live apply: per-pair UPDATE then loser-entry+dependents DELETE ──
    # 1. Field reconcile bulk UPDATE — single SQL using the dup_pairs join.
    cur.execute("""
      UPDATE entries w SET
        post_position    = COALESCE(w.post_position,    l.post_position),
        program_number   = COALESCE(w.program_number,   l.program_number),
        morning_line_odds = COALESCE(w.morning_line_odds, l.morning_line_odds),
        weight_carried   = COALESCE(w.weight_carried,   l.weight_carried),
        lasix            = w.lasix      OR l.lasix,
        blinkers_on      = w.blinkers_on OR l.blinkers_on,
        equipment_change_from_last
                         = w.equipment_change_from_last OR l.equipment_change_from_last,
        is_scratched     = w.is_scratched OR l.is_scratched,
        jockey_id        = COALESCE(w.jockey_id,  l.jockey_id),
        trainer_id       = COALESCE(w.trainer_id, l.trainer_id)
      FROM dup_pairs dp
      JOIN entries l ON l.horse_id = dp.loser_id
      WHERE w.horse_id = dp.winner_id
        AND w.race_id  = l.race_id
    """)
    summary["bulk_update_rowcount"] = cur.rowcount

    # 2. Delete dependents of loser entries.
    for tbl in ENTRY_DEPENDENT_TABLES:
        cur.execute(f"""
          DELETE FROM {tbl} t
          USING dup_pairs dp,
                entries el, entries ew
          WHERE t.entry_id = el.entry_id
            AND el.horse_id = dp.loser_id
            AND ew.horse_id = dp.winner_id
            AND ew.race_id  = el.race_id
        """)
        summary[f"deleted_{tbl}"] = cur.rowcount

    # 3. Delete the loser entries themselves.
    cur.execute("""
      DELETE FROM entries el
      USING dup_pairs dp, entries ew
      WHERE el.horse_id = dp.loser_id
        AND ew.horse_id = dp.winner_id
        AND ew.race_id  = el.race_id
    """)
    summary["deleted_loser_entries"] = cur.rowcount
    return summary, pairs


def _drop_pp_workout_collisions(cur):
    """Bulk-delete loser PPs and workouts whose unique key collides with
    the winner. Run only in apply mode."""
    cur.execute("""
      DELETE FROM past_performances pp_d
      USING dup_pairs dp, past_performances pp_k
      WHERE pp_d.horse_id = dp.loser_id
        AND pp_k.horse_id = dp.winner_id
        AND pp_k.race_date   = pp_d.race_date
        AND pp_k.track_code  = pp_d.track_code
        AND pp_k.race_number = pp_d.race_number
    """)
    pp_dropped = cur.rowcount
    cur.execute("""
      DELETE FROM workouts w_d
      USING dup_pairs dp, workouts w_k
      WHERE w_d.horse_id = dp.loser_id
        AND w_k.horse_id = dp.winner_id
        AND w_k.workout_date     = w_d.workout_date
        AND w_k.track_code       = w_d.track_code
        AND w_k.distance_furlongs = w_d.distance_furlongs
    """)
    w_dropped = cur.rowcount
    return pp_dropped, w_dropped


def _count_intra_bucket_collisions(cur):
    """Count rows that would collide AFTER FK redirect WITHIN a bucket
    (multiple losers in the same bucket pointing at the same race/key
    where winner has no entry of its own). These are NOT caught by
    _drop_pp_workout_collisions or by the winner-vs-loser entry pass."""
    counts = {}
    cur.execute("""
      WITH cand AS (
        SELECT e.entry_id, dp.winner_id, e.race_id,
               ROW_NUMBER() OVER (
                 PARTITION BY dp.winner_id, e.race_id
                 ORDER BY e.entry_id
               ) AS rn
        FROM entries e
        JOIN dup_pairs dp ON dp.loser_id = e.horse_id
        WHERE NOT EXISTS (
          SELECT 1 FROM entries ew
          WHERE ew.horse_id = dp.winner_id AND ew.race_id = e.race_id
        )
      )
      SELECT COUNT(*) AS n FROM cand WHERE rn > 1
    """)
    counts["entries"] = cur.fetchone()["n"]

    cur.execute("""
      WITH cand AS (
        SELECT pp.pp_id, dp.winner_id, pp.race_date, pp.track_code, pp.race_number,
               ROW_NUMBER() OVER (
                 PARTITION BY dp.winner_id, pp.race_date, pp.track_code, pp.race_number
                 ORDER BY pp.pp_id
               ) AS rn
        FROM past_performances pp
        JOIN dup_pairs dp ON dp.loser_id = pp.horse_id
        WHERE NOT EXISTS (
          SELECT 1 FROM past_performances pk
          WHERE pk.horse_id = dp.winner_id
            AND pk.race_date = pp.race_date
            AND pk.track_code = pp.track_code
            AND pk.race_number = pp.race_number
        )
      )
      SELECT COUNT(*) AS n FROM cand WHERE rn > 1
    """)
    counts["past_performances"] = cur.fetchone()["n"]

    cur.execute("""
      WITH cand AS (
        SELECT w.workout_id, dp.winner_id,
               w.workout_date, w.track_code, w.distance_furlongs,
               ROW_NUMBER() OVER (
                 PARTITION BY dp.winner_id, w.workout_date, w.track_code, w.distance_furlongs
                 ORDER BY w.workout_id
               ) AS rn
        FROM workouts w
        JOIN dup_pairs dp ON dp.loser_id = w.horse_id
        WHERE NOT EXISTS (
          SELECT 1 FROM workouts wk
          WHERE wk.horse_id = dp.winner_id
            AND wk.workout_date = w.workout_date
            AND wk.track_code = w.track_code
            AND wk.distance_furlongs = w.distance_furlongs
        )
      )
      SELECT COUNT(*) AS n FROM cand WHERE rn > 1
    """)
    counts["workouts"] = cur.fetchone()["n"]
    return counts


def _dedup_intra_bucket(cur):
    """Live: for each bucket, where multiple losers share a unique-key
    tuple AND the winner has no row at that tuple, keep the lowest-id
    one and delete the rest (plus any dependents).

    Returns dict of {table -> rows_deleted}.
    """
    # ── Entries ──
    # 1. Stage entry_ids to drop into a temp table.
    cur.execute("DROP TABLE IF EXISTS entries_to_drop")
    cur.execute("""
      CREATE TEMP TABLE entries_to_drop AS
      WITH cand AS (
        SELECT e.entry_id, dp.winner_id, e.race_id,
               ROW_NUMBER() OVER (
                 PARTITION BY dp.winner_id, e.race_id
                 ORDER BY
                   ((CASE WHEN e.weight_carried IS NOT NULL THEN 1 ELSE 0 END)
                  + (CASE WHEN e.morning_line_odds IS NOT NULL THEN 1 ELSE 0 END)
                  + (CASE WHEN e.lasix THEN 1 ELSE 0 END)
                  + (CASE WHEN e.blinkers_on THEN 1 ELSE 0 END)
                  + (CASE WHEN e.is_scratched THEN 1 ELSE 0 END)
                  + (CASE WHEN e.equipment_change_from_last THEN 1 ELSE 0 END)
                   ) DESC,
                   e.entry_id
               ) AS rn
        FROM entries e
        JOIN dup_pairs dp ON dp.loser_id = e.horse_id
        WHERE NOT EXISTS (
          SELECT 1 FROM entries ew
          WHERE ew.horse_id = dp.winner_id AND ew.race_id = e.race_id
        )
      )
      SELECT entry_id FROM cand WHERE rn > 1
    """)
    counts = {}
    # 2. Delete dependents of those entries.
    for tbl in ENTRY_DEPENDENT_TABLES:
        cur.execute(
            f"DELETE FROM {tbl} t USING entries_to_drop d WHERE t.entry_id = d.entry_id"
        )
        counts[f"{tbl}_intra"] = cur.rowcount
    # 3. Delete the entries themselves.
    cur.execute("DELETE FROM entries e USING entries_to_drop d WHERE e.entry_id = d.entry_id")
    counts["entries_intra"] = cur.rowcount

    # ── Past-performances ──
    cur.execute("""
      WITH cand AS (
        SELECT pp.pp_id,
               ROW_NUMBER() OVER (
                 PARTITION BY dp.winner_id, pp.race_date, pp.track_code, pp.race_number
                 ORDER BY pp.pp_id
               ) AS rn
        FROM past_performances pp
        JOIN dup_pairs dp ON dp.loser_id = pp.horse_id
        WHERE NOT EXISTS (
          SELECT 1 FROM past_performances pk
          WHERE pk.horse_id = dp.winner_id
            AND pk.race_date = pp.race_date
            AND pk.track_code = pp.track_code
            AND pk.race_number = pp.race_number
        )
      )
      DELETE FROM past_performances pp
      USING cand
      WHERE pp.pp_id = cand.pp_id AND cand.rn > 1
    """)
    counts["pps_intra"] = cur.rowcount

    # ── Workouts ──
    cur.execute("""
      WITH cand AS (
        SELECT w.workout_id,
               ROW_NUMBER() OVER (
                 PARTITION BY dp.winner_id, w.workout_date, w.track_code, w.distance_furlongs
                 ORDER BY w.workout_id
               ) AS rn
        FROM workouts w
        JOIN dup_pairs dp ON dp.loser_id = w.horse_id
        WHERE NOT EXISTS (
          SELECT 1 FROM workouts wk
          WHERE wk.horse_id = dp.winner_id
            AND wk.workout_date = w.workout_date
            AND wk.track_code = w.track_code
            AND wk.distance_furlongs = w.distance_furlongs
        )
      )
      DELETE FROM workouts w
      USING cand
      WHERE w.workout_id = cand.workout_id AND cand.rn > 1
    """)
    counts["workouts_intra"] = cur.rowcount
    return counts


def _redirect_fks(cur):
    """Bulk-redirect every horse_id reference loser -> winner."""
    redirected = {}
    for tbl in HORSE_FK_TABLES:
        cur.execute(f"""
          UPDATE {tbl} t
          SET horse_id = dp.winner_id
          FROM dup_pairs dp
          WHERE t.horse_id = dp.loser_id
        """)
        redirected[tbl] = cur.rowcount
    for col in HORSE_SELF_REFS:
        cur.execute(f"""
          UPDATE horses h
          SET {col} = dp.winner_id
          FROM dup_pairs dp
          WHERE h.{col} = dp.loser_id
        """)
        redirected[f"horses.{col}"] = cur.rowcount
    return redirected


def _delete_losers(cur):
    cur.execute("""
      DELETE FROM horses h
      USING dup_pairs dp
      WHERE h.horse_id = dp.loser_id
    """)
    return cur.rowcount


def _sample_buckets(cur, n: int = 10):
    cur.execute("""
      SELECT winner_id, COUNT(*) AS n_losers
      FROM dup_pairs GROUP BY winner_id ORDER BY RANDOM() LIMIT %s
    """, (n,))
    sample_winners = [r["winner_id"] for r in cur.fetchall()]
    if not sample_winners:
        return []
    cur.execute("""
      SELECT h.horse_id, h.horse_name, h.created_at,
             (SELECT COUNT(*) FROM past_performances pp
              WHERE pp.horse_id = h.horse_id) AS pp_count,
             dp.winner_id
      FROM dup_pairs dp
      JOIN horses h ON h.horse_id IN (dp.loser_id, dp.winner_id)
      WHERE dp.winner_id = ANY(%s::uuid[])
      ORDER BY dp.winner_id, h.created_at
    """, ([str(w) for w in sample_winners],))
    rows = cur.fetchall()
    by_winner: dict = defaultdict(list)
    for r in rows:
        d = dict(r)
        d["has_space"] = " " in (r["horse_name"] or "")
        by_winner[r["winner_id"]].append(d)
    return [(w, by_winner[w]) for w in sample_winners]


def _fmt(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "T" if v else "F"
    return str(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Actually commit the merge. Default is dry-run.")
    args = ap.parse_args()

    apply_mode = bool(args.apply)
    print(f"=== merge_duplicate_horses.py — mode: "
          f"{'APPLY (LIVE)' if apply_mode else 'DRY-RUN'} ===", flush=True)

    conn = _get_conn()
    cur = conn.cursor()

    t0 = time.perf_counter()
    print("\nStaging winners + losers in temp table...", flush=True)
    n_winners, n_losers = _stage_winners_and_losers(cur)
    print(f"  buckets: {n_winners:,}    losers to merge: {n_losers:,}    "
          f"({time.perf_counter()-t0:.1f}s)", flush=True)

    t0 = time.perf_counter()
    print("\nCounting collisions (bulk)...", flush=True)
    e_coll, pp_coll, w_coll = _aggregate_collisions(cur)
    print(f"  entries_collide={e_coll:,}    pps_collide={pp_coll:,}    "
          f"workouts_collide={w_coll:,}    "
          f"({time.perf_counter()-t0:.1f}s)", flush=True)

    t0 = time.perf_counter()
    print("\nCounting intra-bucket collisions (bulk)...", flush=True)
    intra = _count_intra_bucket_collisions(cur)
    print(f"  entries={intra['entries']:,}  "
          f"pps={intra['past_performances']:,}  "
          f"workouts={intra['workouts']:,}  "
          f"({time.perf_counter()-t0:.1f}s)", flush=True)

    t0 = time.perf_counter()
    print("\nCounting FK redirects (bulk)...", flush=True)
    redirects = _aggregate_redirects(cur)
    print(f"  ({time.perf_counter()-t0:.1f}s)", flush=True)

    print()
    print("=" * 78)
    print("PLAN SUMMARY")
    print("=" * 78)
    print(f"  Duplicate buckets:           {n_winners:,}")
    print(f"  Losers to merge:             {n_losers:,}")
    print(f"  Horse rows to delete:        {n_losers:,}")
    print(f"  Colliding entry pairs:       {e_coll:,}  "
          f"(reconciled then loser-entry deleted)")
    print(f"  Colliding PPs to drop:       {pp_coll:,}")
    print(f"  Colliding workouts to drop:  {w_coll:,}")
    print(f"  Intra-bucket residual collisions (deduped before redirect):")
    print(f"      entries                 {intra['entries']:>10,}")
    print(f"      past_performances       {intra['past_performances']:>10,}")
    print(f"      workouts                {intra['workouts']:>10,}")
    print(f"  FK redirects (loser -> winner) — total references on losers:")
    for tbl, n in redirects.items():
        if n > 0:
            print(f"      {tbl:<28} {n:>12,}")

    # Reconcile pass — writes audit CSV regardless of apply_mode.
    t0 = time.perf_counter()
    print(f"\nReconciling colliding entry fields → {AUDIT_PATH} ...",
          flush=True)
    rec_summary, pairs = _reconcile_colliding_entries(cur, apply_mode)
    print(f"  ({time.perf_counter()-t0:.1f}s)", flush=True)

    print()
    print("=" * 78)
    print("FIELD RECONCILE SUMMARY")
    print("=" * 78)
    print(f"  Total colliding pairs processed: {rec_summary['pair_count']:,}")
    print(f"  Pairs with at least 1 field change: "
          f"{rec_summary['pairs_with_changes']:,}")
    print(f"  Pairs unchanged (winner already richer or equal):  "
          f"{rec_summary['pairs_no_change']:,}")
    print(f"  Total field-level changes (audit rows): "
          f"{rec_summary['audit_rows']:,}")
    print(f"  Per-field change counts:")
    for f in NON_BOOL_FIELDS + BOOL_FIELDS:
        c = rec_summary["field_change_counts"].get(f, 0)
        print(f"      {f:<28} {c:>10,}")
    print(f"  Sanity guard — pairs where populated count dropped: "
          f"{len(rec_summary['sanity_violations'])}")
    if rec_summary["sanity_violations"]:
        print("  ⚠ VIOLATIONS:")
        for v in rec_summary["sanity_violations"][:5]:
            print(f"      entry_id={v[0]} before={v[1]} after={v[2]}")

    print()
    print("=" * 78)
    print("SAMPLE 20 RANDOM COLLIDING PAIRS — before vs reconciled-after")
    print("=" * 78)
    sample_pairs = random.sample(pairs, min(20, len(pairs))) if pairs else []
    for i, r in enumerate(sample_pairs, 1):
        print(f"\n--- pair {i}/{len(sample_pairs)}    "
              f"race_id={r['race_id']} ---")
        print(f"  winner_entry={r['w_entry_id']}    "
              f"loser_entry={r['l_entry_id']}")
        print(f"  {'field':<28} {'WIN_BEFORE':>14} {'LOSER':>14} "
              f"{'WIN_AFTER':>14}  diff")
        for f in NON_BOOL_FIELDS + BOOL_FIELDS:
            w = r[f"w_{f}"]
            l = r[f"l_{f}"]
            is_bool = f in BOOL_FIELDS
            new_v = _reconcile_value(f, w, l, is_bool=is_bool)
            diff = "  ←✱" if new_v != w else ""
            print(f"  {f:<28} {_fmt(w):>14} {_fmt(l):>14} "
                  f"{_fmt(new_v):>14}{diff}")

    print()
    print("=" * 78)
    print("SAMPLE 10 RANDOM HORSE BUCKETS")
    print("=" * 78)
    samples = _sample_buckets(cur, 10)
    for winner_id, rows in samples:
        rows_sorted = sorted(rows,
                             key=lambda r: str(r["horse_id"]) != str(winner_id))
        print(f"\nbucket size={len(rows)}    winner_id={winner_id}")
        for r in rows_sorted:
            mark = "  WIN " if str(r["horse_id"]) == str(winner_id) else "  los "
            sp = "[ws]" if r["has_space"] else "[no]"
            created = str(r["created_at"])[:19] if r["created_at"] else "-"
            print(f"  {mark} {sp} pp={r['pp_count']:>4}  "
                  f"created={created}  horse_name={r['horse_name']!r}")

    if not apply_mode:
        conn.rollback()
        print(f"\nDRY-RUN complete. Audit CSV written to {AUDIT_PATH} "
              f"({rec_summary['audit_rows']:,} rows).")
        print(f"Re-run with --apply to actually mutate.")
        cur.close()
        conn.close()
        return

    # ── LIVE APPLY (rec_summary already returned with mutation summaries) ──
    print()
    print("=" * 78)
    print("APPLYING REMAINING STEPS (entries reconcile already done)")
    print("=" * 78)
    t0 = time.perf_counter()
    print(f"  bulk-UPDATE rowcount: {rec_summary['bulk_update_rowcount']:,}")
    for tbl in ENTRY_DEPENDENT_TABLES:
        n = rec_summary.get(f"deleted_{tbl}", 0)
        if n:
            print(f"  deleted from {tbl:<22} {n:,}")
    print(f"  deleted loser entries: "
          f"{rec_summary['deleted_loser_entries']:,}")

    print("\nDropping colliding PPs/workouts...", flush=True)
    pp_dropped, w_dropped = _drop_pp_workout_collisions(cur)
    print(f"  PPs dropped: {pp_dropped:,}    workouts dropped: {w_dropped:,}",
          flush=True)

    print("\nDeduping intra-bucket residuals (multiple losers same key)...",
          flush=True)
    dedup_counts = _dedup_intra_bucket(cur)
    for k, v in dedup_counts.items():
        if v > 0:
            print(f"  intra dedup {k:<28} {v:>10,}")

    print("\nRedirecting FKs loser -> winner (bulk UPDATE per table)...",
          flush=True)
    redirected = _redirect_fks(cur)
    for tbl, n in redirected.items():
        if n > 0:
            print(f"  redirected {tbl:<28} {n:>10,}")

    print("\nDeleting orphan horse rows...", flush=True)
    n_deleted = _delete_losers(cur)
    print(f"  horses deleted: {n_deleted:,}    "
          f"(expected {n_losers:,})", flush=True)

    if n_deleted != n_losers:
        print(f"  ⚠ delete count mismatch — aborting via rollback.")
        conn.rollback()
        sys.exit(2)

    print(f"\nCommitting... (elapsed {time.perf_counter()-t0:.1f}s)",
          flush=True)
    conn.commit()
    print(f"COMMIT OK — {n_winners:,} buckets merged, "
          f"{n_losers:,} losers cleaned.")
    print(f"Audit CSV: {AUDIT_PATH}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
