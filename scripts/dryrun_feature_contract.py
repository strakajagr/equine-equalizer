"""REPAIR-5 §1 dry-run: prove feature_contract works on every L1 artifact.

Loads each *.json XGBoost artifact under /tmp/l1_artifacts_inspect/,
reads booster.feature_names, builds a synthetic feature DataFrame
covering FEATURE_DEFS, and demonstrates that predict_with_contract
runs end-to-end without a feature_names mismatch.

Run from repo root:
  PYTHONPATH=backend:. python3 scripts/dryrun_feature_contract.py
"""
from __future__ import annotations
import sys
import json
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
sys.path.insert(0, str(ROOT))

from services.feature_contract import (
    get_model_features,
    select_features,
    predict_with_contract,
    diagnose_contract,
)

ARTIFACT_DIR = Path('/tmp/l1_artifacts_inspect')
N_FAKE_ROWS = 8


def build_synthetic_wide_df(all_required_features: set) -> pd.DataFrame:
    """Build a DataFrame with one column per feature any booster needs,
    plus the standard FEATURE_DEFS catalog, filled with random small floats."""
    try:
        from model.shared.feature_definitions import (
            get_odds_aware_features,
            get_gonzo_sauce_features,
        )
        catalog = set(get_odds_aware_features()) | set(get_gonzo_sauce_features())
    except Exception:
        catalog = set()
    all_cols = sorted(catalog | all_required_features)
    rng = np.random.default_rng(seed=42)
    data = {c: rng.uniform(-1.0, 5.0, size=N_FAKE_ROWS) for c in all_cols}
    return pd.DataFrame(data)


def main() -> int:
    if not ARTIFACT_DIR.exists():
        print(f'FATAL: {ARTIFACT_DIR} not found')
        return 1

    artifacts = sorted(ARTIFACT_DIR.glob('*.json'))
    if not artifacts:
        print(f'FATAL: no *.json artifacts in {ARTIFACT_DIR}')
        return 1

    print(f'== loading {len(artifacts)} L1 artifacts from {ARTIFACT_DIR} ==')
    loaded: list[tuple[str, xgb.Booster]] = []
    load_failures: list[tuple[str, str]] = []

    for p in artifacts:
        booster = xgb.Booster()
        try:
            booster.load_model(str(p))
            loaded.append((p.stem, booster))
        except Exception as e:
            load_failures.append((p.stem, f'{type(e).__name__}: {e}'))

    print(f'   loaded={len(loaded)}  failed={len(load_failures)}')
    for name, err in load_failures:
        print(f'   LOAD-FAIL {name}: {err}')

    print()
    print('== per-artifact feature_names ==')
    all_needed: set = set()
    feature_counts: dict[str, int] = {}
    for name, b in loaded:
        feats = get_model_features(b)
        feature_counts[name] = len(feats)
        all_needed.update(feats)
    for name in sorted(feature_counts):
        print(f'   {name:42s} {feature_counts[name]:3d} feats')

    print()
    print(f'== unique features across all {len(loaded)} artifacts: {len(all_needed)} ==')

    print()
    print('== building synthetic feature_df ==')
    wide_df = build_synthetic_wide_df(all_needed)
    print(f'   shape={wide_df.shape}  cols={len(wide_df.columns)}')

    print()
    print('== predict_with_contract per artifact ==')
    pass_count = 0
    fail_count = 0
    fail_details: list[tuple[str, str]] = []
    for name, b in loaded:
        try:
            preds = predict_with_contract(b, wide_df)
            assert preds.shape == (N_FAKE_ROWS,), (
                f'{name}: unexpected pred shape {preds.shape}'
            )
            pass_count += 1
        except ValueError as e:
            fail_count += 1
            fail_details.append((name, str(e)[:200]))
        except Exception as e:
            fail_count += 1
            fail_details.append((name, f'{type(e).__name__}: {str(e)[:200]}'))
    print(f'   PASS={pass_count}  FAIL={fail_count}')
    for name, err in fail_details:
        print(f'   FAIL {name}: {err}')

    print()
    print('== representative diagnose_contract (wr_odds, wp_full_general) ==')
    for representative in ('wr_odds', 'wp_full_general', 'ranker_core',
                           'pl_core_general', 'win_prob_full'):
        match = next((b for n, b in loaded if n == representative), None)
        if match is None:
            print(f'   {representative}: NOT LOADED')
            continue
        d = diagnose_contract(match, wide_df)
        print(f'   {representative}:')
        print(f'      model_feature_count = {d["model_feature_count"]}')
        print(f'      wide_feature_count  = {d["wide_feature_count"]}')
        print(f'      missing_from_wide   = {len(d["missing_from_wide"])}')
        print(f'      extra_in_wide_count = {d["extra_in_wide_count"]}')
        if d['missing_from_wide']:
            print(f'      MISSING examples    = {d["missing_from_wide"][:5]}')

    print()
    print('== EXIT ==')
    if fail_count > 0:
        print(f'FAIL: {fail_count} artifacts had contract mismatch on synthetic input')
        return 2
    print('PASS: all loaded artifacts produced predictions via predict_with_contract')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
