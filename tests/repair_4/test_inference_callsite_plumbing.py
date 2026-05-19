"""
REPAIR-4 Step B regression: all get_entries_by_race callsites pass as_of_date.

Static-analysis style: greps source files for any get_entries_by_race call
and substrate-verifies it includes as_of_date=race.race_date (or similar).
"""
import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Files known to call get_entries_by_race per Step B audit
CALLSITE_FILES = [
    'backend/services/multicohort_inference_service.py',
    'backend/services/inference_service.py',
    'backend/services/ls_inference_service.py',
    'backend/services/pl_inference_service.py',
    'backend/services/wr_inference_service.py',
    'model/ensemble/option_c_inference.py',
    'model/training/train.py',
]


def _read(rel):
    with open(os.path.join(REPO_ROOT, rel)) as f:
        return f.read()


def test_all_callsites_pass_as_of_date():
    """
    Every get_entries_by_race callsite must pass as_of_date. Without it
    the call would raise ValueError at runtime (per Step B guard).
    """
    for rel in CALLSITE_FILES:
        src = _read(rel)
        # Find any call substrate-pragmatically — match across multiple lines
        call_pattern = re.compile(
            r'get_entries_by_race\s*\(([^)]*(?:\)[^)]*)*)\)',
            re.DOTALL
        )
        matches = call_pattern.findall(src)
        if not matches:
            # File may import the symbol without calling — skip
            continue
        for match in matches:
            assert 'as_of_date' in match, (
                f"{rel}: get_entries_by_race call missing as_of_date — "
                f"would raise ValueError at runtime. Match body:\n{match[:200]}"
            )


def test_pp_count_subqueries_have_as_of_predicate():
    """
    The pp_count helper subqueries in LS/PL/WR inference services must
    filter past_performances with race_date < r.race_date (or substrate-
    equivalent variable).
    """
    targets = [
        ('backend/services/ls_inference_service.py', 'pp_count.race_date < r.race_date'),
        ('backend/services/pl_inference_service.py', 'race_date < %s'),
        ('backend/services/wr_inference_service.py', 'race_date < %s'),
    ]
    for rel, expected in targets:
        src = _read(rel)
        assert expected in src, (
            f"{rel}: missing AS-OF predicate substrate-pattern '{expected}'"
        )


def test_score_angles_uses_history_table():
    """REPAIR-4 C.5: _score_angles must query angle_stats_history with AS-OF."""
    src = _read('backend/services/ls_inference_service.py')
    assert 'angle_stats_history' in src
    assert 'snapshot_date <= %s' in src
    assert 'ORDER BY snapshot_date DESC' in src
