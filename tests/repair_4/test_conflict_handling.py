"""
REPAIR-4 Step B regression: ON CONFLICT DO NOTHING on prediction writes.

Substrate-verifies that prediction repository INSERT statements use
DO NOTHING (write-once protection) rather than DO UPDATE (which would
allow post-result overwrites of predictions).

Static-analysis style: reads repo files and asserts the substrate-actual
SQL string contains "DO NOTHING" for prediction-class writes.
"""
import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def _read(rel):
    with open(os.path.join(REPO_ROOT, rel)) as f:
        return f.read()


def _strip_comments(text):
    """Strip Python and SQL line comments to avoid matching on commentary."""
    out = []
    for line in text.splitlines():
        line_no_sql_comment = re.sub(r'--.*$', '', line)
        line_no_py_comment = re.sub(r'#.*$', '', line_no_sql_comment)
        out.append(line_no_py_comment)
    return "\n".join(out)


def test_ls_prediction_repository_uses_do_nothing():
    src = _strip_comments(_read('backend/repositories/ls_prediction_repository.py'))
    assert 'ON CONFLICT' in src
    assert 'DO NOTHING' in src
    assert 'DO UPDATE' not in src, \
        "ls_prediction_repository must not contain DO UPDATE (substrate-leakage risk)"


def test_pl_prediction_repository_uses_do_nothing():
    src = _strip_comments(_read('backend/repositories/pl_prediction_repository.py'))
    assert 'ON CONFLICT' in src
    assert 'DO NOTHING' in src
    assert 'DO UPDATE' not in src


def test_wr_prediction_repository_uses_do_nothing():
    src = _strip_comments(_read('backend/repositories/wr_prediction_repository.py'))
    assert 'ON CONFLICT' in src
    assert 'DO NOTHING' in src
    assert 'DO UPDATE' not in src


def test_prediction_repository_uses_do_nothing():
    src = _strip_comments(_read('backend/repositories/prediction_repository.py'))
    assert 'ON CONFLICT' in src
    assert 'DO NOTHING' in src
    assert 'DO UPDATE' not in src


def test_result_repository_legitimately_uses_do_update():
    """
    Substrate-intentional exception: result_repository legitimately uses
    DO UPDATE for DQ/payout corrections to RACE RESULTS (not predictions).
    Race results legitimately mutate post-race when stewards rule on a DQ
    or chart-parser correction lands. This is NOT prediction leakage.
    """
    src = _read('backend/repositories/result_repository.py')
    assert 'ON CONFLICT' in src
    assert 'DO UPDATE' in src, (
        "result_repository must retain DO UPDATE for DQ/payout corrections"
    )


def test_entry_repository_raises_without_as_of_date():
    """Static check that the substrate-prophylactic guard is in place."""
    src = _read('backend/repositories/entry_repository.py')
    assert 'as_of_date is required' in src
    assert 'raise ValueError' in src
    # AS-OF predicate present in pps query
    assert 'race_date < %s' in src
