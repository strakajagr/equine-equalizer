"""REPAIR-5 §1 live-DB dry-run.

Real FE pipeline against a real 5/16 race; for each loaded booster,
diagnose contract: (model_features, supplied_by_FE, would_be_padded).
Then ACTUALLY run the patched predict_race and show real prediction values.

Verdict criterion:
  - padded == 0 across all substantive features → PASS (contract aligns with FE)
  - padded > 0 on any meaningful feature → COVERAGE GAP, surface for fix

Run:
  DB_SECRET_ARN='arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials-7CD7Mt' \\
  PYTHONPATH=backend:. python3 scripts/dryrun_live_db.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import os

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
sys.path.insert(0, str(ROOT))

# Target: CD R4 on 5/16 (10 horses, 8.5f turf — first prod-dead day)
TARGET_RACE_ID = '33409c51-9650-496a-b815-2215a5483c7b'
TARGET_DATE = '2026-05-16'

from shared.db import get_db
from repositories.race_repository import RaceRepository
from repositories.entry_repository import EntryRepository
from services.feature_engineering_service import FeatureEngineeringService
from services.feature_contract import get_model_features
from services.wr_inference_service import WRInferenceService
from services.pl_inference_service import PLInferenceService
from services.multicohort_inference_service import MultiCohortInferenceService


def diagnose_contract_against_fe(label: str, booster, fe_columns: set) -> dict:
    feats = get_model_features(booster)
    supplied = [f for f in feats if f in fe_columns]
    padded = [f for f in feats if f not in fe_columns]
    return {
        'label': label,
        'model_feat_count': len(feats),
        'supplied_by_fe': len(supplied),
        'would_pad': len(padded),
        'padded_features': padded,
    }


def main() -> int:
    print(f'== target race {TARGET_RACE_ID} on {TARGET_DATE} (CD R4, 10 horses) ==')
    with get_db() as conn:
        race_repo = RaceRepository(conn)
        entry_repo = EntryRepository(conn)
        fe = FeatureEngineeringService(conn)

        race = race_repo.get_race_by_id(TARGET_RACE_ID)
        if race is None:
            print(f'FATAL: race {TARGET_RACE_ID} not found')
            return 1
        race.entries = entry_repo.get_entries_by_race(
            TARGET_RACE_ID, as_of_date=race.race_date,
        )
        print(f'   race: {race.race_id} entries={len(race.entries)} '
              f'distance={race.distance_furlongs}f surface={race.surface}')

        print()
        print('== building real FE feature matrix ==')
        feature_df = fe.build_feature_matrix(race, include_odds=True)
        print(f'   feature_df shape={feature_df.shape}')
        print(f'   feature_df cols (count={len(feature_df.columns)}) sample={sorted(feature_df.columns)[:10]}...')
        fe_columns = set(feature_df.columns)

        print()
        print('═══ WR (style=general) ═══')
        wr = WRInferenceService(conn, style='general')
        wr.load_model()
        rows = []
        for name, m in [
            ('wp_core', wr.wp_core_model),
            ('wp_full', wr.wp_full_model),
            ('rk_core', wr.rk_core_model),
            ('rk_full', wr.rk_full_model),
        ]:
            if m is None:
                print(f'   {name}: NOT LOADED')
                continue
            d = diagnose_contract_against_fe(name, m, fe_columns)
            rows.append(d)
            print(f'   {name:8s} feats={d["model_feat_count"]:3d}  '
                  f'supplied={d["supplied_by_fe"]:3d}  '
                  f'would_pad={d["would_pad"]:3d}  '
                  f'pad_examples={d["padded_features"][:6]}')
        print()
        print('   Running patched predict_race...')
        preds = wr.predict_race(race)
        print(f'   produced {len(preds)} predictions')
        for p in preds[:3]:
            print(f'      horse {p.horse_id}: win_prob={p.win_probability:.4f} '
                  f'rank_score={getattr(p, "rank_score", None)} '
                  f'model_used={getattr(p, "model_used", None)}')

        print()
        print('═══ PL (style=general) ═══')
        pl = PLInferenceService(conn, style='general')
        pl.load_model()
        d = diagnose_contract_against_fe('pl_core', pl.model, fe_columns)
        print(f'   pl_core  feats={d["model_feat_count"]:3d}  '
              f'supplied={d["supplied_by_fe"]:3d}  '
              f'would_pad={d["would_pad"]:3d}  '
              f'pad_examples={d["padded_features"][:6]}')
        print()
        print('   Running patched predict_race...')
        pl_preds = pl.predict_race(race)
        print(f'   produced {len(pl_preds)} predictions')
        for p in pl_preds[:3]:
            print(f'      horse {p.horse_id}: win_prob={getattr(p,"win_probability",None)} '
                  f'edge_pct={getattr(p,"edge_pct",None)} '
                  f'kelly={getattr(p,"kelly_fraction",None)}')

        print()
        print('═══ MultiCohort (Hybrid C) ═══')
        mci = MultiCohortInferenceService(conn)
        init = mci.initialize()
        print(f'   initialize: {init}')
        xgb_arts = [a for a in mci._l1_artifacts if a.artifact_format == 'xgb_json']
        sklearn_arts = [a for a in mci._l1_artifacts if a.artifact_format == 'pkl_sklearn']
        print(f'   xgb_json artifacts={len(xgb_arts)} sklearn={len(sklearn_arts)} '
              f'hybrid_c feats={len(mci._hybrid_c_feature_names)}')
        worst_pad = 0
        worst_arts = []
        for art in xgb_arts:
            d = diagnose_contract_against_fe(art.column_name, art.model, fe_columns)
            if d['would_pad'] > 0:
                worst_pad = max(worst_pad, d['would_pad'])
                worst_arts.append((art.column_name, d['would_pad'], d['padded_features']))
        if worst_arts:
            print(f'   {len(worst_arts)} artifacts would pad features:')
            for name, pad, exs in worst_arts[:5]:
                print(f'      {name}  pad={pad}  examples={exs[:6]}')
        else:
            print('   all xgb artifacts have ZERO would_pad — contract aligns with FE for MCI')
        print()
        print('   Running patched predict_race...')
        mci_result = mci.predict_race(TARGET_RACE_ID)
        if mci_result is None:
            print('   MCI returned None')
        else:
            probs = mci_result['hybrid_c_win_probability']
            print(f'   produced {len(probs)} hybrid_c predictions; sum={sum(probs):.4f}')
            for i, (hid, p) in enumerate(zip(mci_result['horse_ids'], probs)):
                if i >= 3: break
                print(f'      horse {hid}: hybrid_c={p:.4f}')

    print()
    print('═══ VERDICT ═══')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
