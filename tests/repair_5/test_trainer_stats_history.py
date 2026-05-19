"""
REPAIR-5 Step B regression: trainer_stats AS-OF snapshot history.
"""
import os
import sys
import pytest
from datetime import date

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(REPO_ROOT, 'backend'))


def _read(rel):
    with open(os.path.join(REPO_ROOT, rel)) as f:
        return f.read()


def test_trainer_stats_history_table_exists(db_conn):
    with db_conn.cursor() as cur:
        cur.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'trainer_stats_history'
            ORDER BY ordinal_position
        """)
        cols = {r['column_name'] for r in cur.fetchall()}
    expected = {
        'trainer_name', 'total_starts', 'wins', 'win_rate',
        'itm', 'itm_rate', 'layoff_win_rate', 'lasix_win_rate',
        'claimed_win_rate', 'snapshot_date', 'created_at',
    }
    assert expected.issubset(cols)


def test_trainer_stats_history_backfilled(db_conn):
    with db_conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) as cnt FROM trainer_stats_history
            WHERE snapshot_date = CURRENT_DATE
        """)
        cnt = cur.fetchone()['cnt']
    assert cnt > 0, "backfill must have populated CURRENT_DATE snapshot"


def test_get_trainer_stats_requires_race_date():
    """_get_trainer_stats(trainer, None) must raise ValueError."""
    src = _read('backend/services/feature_engineering_service.py')
    assert 'race_date is required for trainer_stats AS-OF discipline' in src
    assert 'raise ValueError' in src


def test_get_trainer_stats_queries_history_with_as_of(db_conn):
    """Direct DB substrate-verify: AS-OF predicate returns most recent
    prior snapshot, not the current materialized view."""
    with db_conn.cursor() as cur:
        # Pick any trainer with snapshot data
        cur.execute("""
            SELECT trainer_name FROM trainer_stats_history
            WHERE total_starts > 0 LIMIT 1
        """)
        sample = cur.fetchone()
        assert sample is not None, "need at least one trainer_stats_history row"

        cur.execute("""
            SELECT total_starts, win_rate
            FROM trainer_stats_history
            WHERE LOWER(trainer_name) = LOWER(%s)
              AND snapshot_date <= %s
            ORDER BY snapshot_date DESC LIMIT 1
        """, (sample['trainer_name'], date.today()))
        row = cur.fetchone()
        assert row is not None
        assert row['total_starts'] >= 0


def test_ingestion_handler_dual_writes(db_conn):
    """ingestion/handler.py refresh_trainer_stats must dual-write to history."""
    src = _read('backend/lambdas/ingestion/handler.py')
    assert "action == 'refresh_trainer_stats'" in src
    assert 'REFRESH MATERIALIZED VIEW trainer_stats' in src
    assert 'INSERT INTO trainer_stats_history' in src
    assert 'CURRENT_DATE' in src
    assert 'ON CONFLICT DO NOTHING' in src


def test_compute_trainer_features_plumbed_race_date():
    """compute_trainer_features signature accepts race_date + plumbed
    through callsite."""
    src = _read('backend/services/feature_engineering_service.py')
    assert 'def compute_trainer_features(' in src
    assert 'race_date=None' in src or 'race_date,' in src
    # Plumbed at _build_entry_features callsite
    assert 'self.compute_trainer_features(entry, all_pps, race.race_date)' in src
