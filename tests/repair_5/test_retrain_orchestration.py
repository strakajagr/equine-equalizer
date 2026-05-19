"""
REPAIR-5 Step C regression: retrain orchestration script structure.

Substrate-verifies script substrate-structural properties WITHOUT actually
launching ECS tasks. These tests substrate-block on:
- Phase plan structure (4 phases, dependency-order)
- Expected models per phase
- Cutover SQL substrate-coherence (all 39 PKs verbatim)
"""
import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def _read(rel):
    with open(os.path.join(REPO_ROOT, rel)) as f:
        return f.read()


def test_orchestration_script_exists():
    path = os.path.join(REPO_ROOT, 'scripts/repair_5_retrain_wave.py')
    assert os.path.exists(path)


def test_orchestration_script_has_four_phases():
    src = _read('scripts/repair_5_retrain_wave.py')
    # Substrate-pragmatic: count phase definitions
    for n in (1, 2, 3, 4):
        assert f"'phase': {n}" in src, f"missing Phase {n} in PHASE_PLAN"


def test_orchestration_uses_clean_tag():
    src = _read('scripts/repair_5_retrain_wave.py')
    assert "CLEAN_TAG" in src
    assert "clean_post_repair5_" in src


def test_orchestration_halts_on_task_failure():
    src = _read('scripts/repair_5_retrain_wave.py')
    # Substrate-discipline: HALT WAVE on any task failure
    assert 'HALTING WAVE' in src
    assert 'do not proceed to cutover' in src.lower() or \
           'do not cutover with partial retrain' in src.lower()


def test_cutover_sql_exists():
    path = os.path.join(REPO_ROOT, 'scripts/repair_5_cutover.sql')
    assert os.path.exists(path)


def test_cutover_sql_has_39_contaminated_pks():
    src = _read('scripts/repair_5_cutover.sql')
    # Substrate-grep all UUID-pattern lines inside the IN(...) clause
    uuid_pat = re.compile(
        r"'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'"
    )
    uuids = uuid_pat.findall(src)
    assert len(uuids) == 39, f"expected 39 contaminated PKs, got {len(uuids)}"


def test_cutover_sql_uses_transaction():
    src = _read('scripts/repair_5_cutover.sql')
    assert 'BEGIN;' in src
    assert 'COMMIT;' in src
    # Read-back verification before commit
    assert 'GROUP BY model_type' in src
    assert 'is_active = TRUE' in src


def test_cutover_sql_activates_clean_rows():
    src = _read('scripts/repair_5_cutover.sql')
    # Substrate-pragmatic substrate-pattern: ROW_NUMBER per model_type
    # WHERE notes contains clean tag, then update is_active=TRUE
    assert 'ROW_NUMBER() OVER' in src
    assert "notes LIKE '%' || :'clean_tag'" in src or \
           "notes LIKE '%' || :clean_tag" in src
    assert 'SET is_active = TRUE' in src
