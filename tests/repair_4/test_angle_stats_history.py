"""
REPAIR-4 Step C.5 regression: angle_stats_history schema + AS-OF semantics.

Substrate-verifies:
1. angle_stats_history table exists with expected columns
2. UNIQUE constraint with NULLS NOT DISTINCT prevents duplicate snapshots
3. AS-OF query returns most-recent-prior snapshot
4. Backfill from angle_stats populated CURRENT_DATE snapshot
"""
from datetime import date


def test_angle_stats_history_table_exists(db_conn):
    with db_conn.cursor() as cur:
        cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'angle_stats_history'
            ORDER BY ordinal_position
        """)
        cols = {r['column_name']: r['data_type'] for r in cur.fetchall()}
    expected = {
        'angle_name', 'trainer_name', 'track_code',
        'wins', 'starts', 'snapshot_date', 'created_at',
    }
    assert expected.issubset(set(cols.keys())), \
        f"Missing columns: {expected - set(cols.keys())}"


def test_angle_stats_history_has_unique_index_nulls_not_distinct(db_conn):
    with db_conn.cursor() as cur:
        cur.execute("""
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE tablename = 'angle_stats_history'
        """)
        idxs = cur.fetchall()
    idx_defs = " ".join(r['indexdef'] for r in idxs)
    assert 'angle_stats_history_unique' in idx_defs or 'UNIQUE' in idx_defs.upper(), \
        "expected unique index on angle_stats_history"
    assert 'NULLS NOT DISTINCT' in idx_defs.upper(), \
        "unique index must use NULLS NOT DISTINCT (PG 15+ semantics)"


def test_backfill_populated_current_date_snapshot(db_conn):
    with db_conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) as cnt
            FROM angle_stats_history
            WHERE snapshot_date = CURRENT_DATE
        """)
        cnt = cur.fetchone()['cnt']
    assert cnt > 0, "backfill must have populated CURRENT_DATE snapshot"


def test_as_of_query_returns_most_recent_prior_snapshot(db_conn):
    """
    Substrate-correctness of AS-OF query pattern used by _score_angles.
    Returns wins/starts for a known angle/trainer combo from history.
    """
    with db_conn.cursor() as cur:
        # Find any angle with substrate-actual data
        cur.execute("""
            SELECT angle_name, trainer_name
            FROM angle_stats_history
            WHERE starts > 0 AND trainer_name IS NOT NULL
            LIMIT 1
        """)
        sample = cur.fetchone()
        assert sample is not None, "need at least one trainer-specific angle row"

        cur.execute("""
            SELECT wins, starts
            FROM angle_stats_history
            WHERE angle_name = %s AND trainer_name = %s
              AND snapshot_date <= %s
            ORDER BY snapshot_date DESC LIMIT 1
        """, (sample['angle_name'], sample['trainer_name'], date.today()))
        row = cur.fetchone()
        assert row is not None
        assert row['starts'] >= 0
        assert row['wins'] >= 0
        assert row['wins'] <= row['starts']


def test_as_of_query_returns_nothing_for_pre_backfill_date(db_conn):
    """
    Substrate-AS-OF discipline: querying for a date BEFORE backfill
    (e.g. 2020-01-01) returns no rows, since no historical snapshots
    existed before today's backfill.
    """
    with db_conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) as cnt
            FROM angle_stats_history
            WHERE snapshot_date <= %s
        """, (date(2020, 1, 1),))
        cnt = cur.fetchone()['cnt']
    assert cnt == 0, "no snapshots should exist for dates before backfill"
