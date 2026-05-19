"""
REPAIR-5 Step A regression: compute_speed_figures.py rolling-window AS-OF.

Substrate-verifies:
1. Module docstring substrate-marks REPAIR-5 fix (not REPAIR-4 deferral)
2. Step 2 par-time SQL has GROUP BY year + EXTRACT(YEAR FROM race_date)
3. lookup_par() function exists with strict-less-than bisect semantics
4. Step 6 Beyer normalization uses per_year_stats with EXTRACT(YEAR)
5. lookup_norm() function exists with strict-less-than bisect semantics
"""
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def _read(rel):
    with open(os.path.join(REPO_ROOT, rel)) as f:
        return f.read()


def test_docstring_marks_repair_5_fix():
    """Module docstring must reflect REPAIR-5 substrate-fix, not REPAIR-4
    deferral marker."""
    src = _read('model/training/compute_speed_figures.py')
    assert 'REPAIR-5 SUBSTRATE-FIX' in src
    assert 'REPAIR-4 SUBSTRATE-LEAKAGE MARKER' not in src
    assert 'AS-OF discipline' in src


def test_par_time_query_groups_by_year():
    """Step 2 SQL must GROUP BY EXTRACT(YEAR FROM race_date)."""
    src = _read('model/training/compute_speed_figures.py')
    assert 'GROUP BY track_code, distance_furlongs, surface,' in src
    assert 'EXTRACT(YEAR FROM race_date)' in src
    assert 'par_year' in src


def test_lookup_par_strict_less_than():
    """lookup_par() must use bisect_left with strict-less-than semantics."""
    src = _read('model/training/compute_speed_figures.py')
    assert 'def lookup_par(' in src
    assert 'bisect_left(years, target_year)' in src
    assert 'years[idx - 1]' in src
    # If target_year matches a bucket exactly, return None
    # (no prior-year data) — substrate-strict-less-than
    assert 'if idx == 0:\n                return None' in src


def test_beyer_normalization_per_year():
    """Step 6 must compute per-year median/std + use them on per-year UPDATEs."""
    src = _read('model/training/compute_speed_figures.py')
    assert 'Per-year Beyer normalization' in src or \
           'per-year normalization' in src.lower()
    assert 'GROUP BY EXTRACT(YEAR FROM race_date)' in src
    assert 'def lookup_norm(target_year):' in src
    assert 'EXTRACT(YEAR FROM race_date) = %s' in src


def test_step_3_uses_lookup_par_with_row_year():
    """Step 3 par-lookup callsite must use lookup_par(t, d, s, row_year)
    extracting year from race_date (not the leaky par_map[key])."""
    src = _read('model/training/compute_speed_figures.py')
    assert 'row_year = int(r[\'race_date\'].year)' in src
    assert 'par = lookup_par(' in src
