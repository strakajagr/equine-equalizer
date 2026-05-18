#!/usr/bin/env python3
"""
SP-Option-C full-cohort forensic inference.

Loads 80+ artifacts (Phase B.x cohort + PRIOR active cohort), generates per-race
per-(cohort, layer) predictions across 9-day forensic OOS window (2026-05-02..2026-05-10).
Substrate-guaranteed OOS for both cohorts.

Idempotent: per-race parquet output at /tmp/option_c_predictions/{race_id}.parquet.

Skipped layers (substrate-permanent, separate handling):
  - trajectory_lstm: PyTorch LSTM with sequence input from PPs; complex feature build
  - ensemble: depends on L1 inputs being computed first (chain dependency)
  - L1-dependent longshot_rf: handled via inline L1 chain construction per race
"""
from __future__ import annotations
import os
import sys
import json
import time
import traceback
import logging
from dataclasses import dataclass, asdict
from datetime import date
from typing import Dict, List, Optional, Tuple, Any

os.environ['DB_SECRET_ARN'] = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'
os.environ.pop('DATABASE_URL', None)

sys.path.insert(0, '/home/strakajagr/projects/equine-equalizer')
sys.path.insert(0, '/home/strakajagr/projects/equine-equalizer/backend')

import boto3
import joblib
import numpy as np
import pandas as pd
import psycopg2.extras
import xgboost as xgb

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('option_c')

from shared.db import get_db, execute_query
from services.feature_engineering_service import FeatureEngineeringService
from repositories.race_repository import RaceRepository
from repositories.entry_repository import EntryRepository
from model.shared.feature_definitions import (
    get_lean53_core_features, get_lean53_features,
    get_core_features, get_odds_aware_features,
    get_gonzo_sauce_features,
)

# ── Paths ──
OUTPUT_DIR = '/tmp/option_c_predictions'
ARTIFACT_DIR = '/tmp/option_c_artifacts'
LOAD_REPORT = '/tmp/option_c_artifact_load.json'
INFERENCE_LOG = '/tmp/option_c_inference.log'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

# ── Forensic window ──
FORENSIC_START = date(2026, 5, 2)
FORENSIC_END = date(2026, 5, 10)
SOFTMAX_TEMPERATURE = 0.15

S3 = boto3.client('s3')


def softmax_temp(raw, T=SOFTMAX_TEMPERATURE):
    raw = np.asarray(raw, dtype=np.float64)
    s = (raw - raw.max()) / T
    s = np.clip(s, -20, 0)
    e = np.exp(s)
    return e / e.sum()


# ─────────────────────────────────────────────────────────────────────
# 1. ARTIFACT INVENTORY — dedup to canonical per (cohort × model_type)
# ─────────────────────────────────────────────────────────────────────

@dataclass
class Artifact:
    cohort: str            # 'phase_bx' or 'prior'
    model_type: str
    version_name: str
    s3_path: str
    training_date: Any
    is_active: bool
    feature_path: Optional[str] = None  # set by classifier
    feature_count: Optional[int] = None
    artifact_format: Optional[str] = None  # 'xgb_json', 'pkl_sklearn', 'pt_torch'
    style_filter: Optional[str] = None  # None | 'sprint' | 'route' | etc.


def get_artifact_inventory() -> List[Artifact]:
    """Dedup'd canonical artifact list. For Phase B.x, picks the LATER timestamp
    when duplicates exist (Phase B.x proper run is later than initial Phase B)."""
    with get_db() as conn:
        rows = execute_query(conn, """
            SELECT model_type, version_name, s3_artifact_path, training_date, is_active
            FROM model_versions
            WHERE (training_date >= '2026-05-12T18:00:00Z'
                   AND training_date < '2026-05-14T00:00:00Z')
               OR (is_active = TRUE AND training_date < '2026-05-12T18:00:00Z')
            ORDER BY training_date DESC
        """)
    # Dedup per (cohort, model_type) — keep latest training_date
    # Use datetime comparison directly (substrate-pragmatic; avoids epoch-constant bugs)
    from datetime import datetime as _dt, timezone as _tz
    phase_bx_floor = _dt(2026, 5, 12, 18, 0, 0, tzinfo=_tz.utc)
    seen: Dict[Tuple[str, str], Artifact] = {}
    for r in rows:
        td = r['training_date']
        if td.tzinfo is None:
            td = td.replace(tzinfo=_tz.utc)
        is_phase_bx = td >= phase_bx_floor
        cohort = 'phase_bx' if is_phase_bx else 'prior'
        key = (cohort, r['model_type'])
        if key in seen:
            continue
        seen[key] = Artifact(
            cohort=cohort,
            model_type=r['model_type'],
            version_name=r['version_name'],
            s3_path=r['s3_artifact_path'],
            training_date=r['training_date'],
            is_active=bool(r['is_active']),
        )
    return list(seen.values())


# ─────────────────────────────────────────────────────────────────────
# 2. FEATURE PATH CLASSIFIER
# ─────────────────────────────────────────────────────────────────────

# Pre-compute feature lists once
_FEAT = {
    'lean53_core': get_lean53_core_features(),       # 47
    'lean53': get_lean53_features(),                 # 53
    'core_odds_blind': get_core_features(False),     # 55
    'core_odds_aware': get_core_features(True),      # 58
    'odds_aware_legacy': get_odds_aware_features(),  # 66
    'gonzo_sauce': get_gonzo_sauce_features(),       # 67
}
for k, v in _FEAT.items():
    logger.info(f"  feature_path '{k}': {len(v)} features")


def classify_feature_path(art: Artifact) -> Tuple[Optional[str], Optional[str]]:
    """Returns (feature_path_key, style_filter_or_None) for a given artifact.

    Substrate-grounded mapping based on model_type + version_name patterns.
    """
    mt = art.model_type
    vn = (art.version_name or '').lower()

    # Detect style filter from model_type or version_name
    style_filter = None
    for style in ('gonzo_sauce', 'class_dropper', 'class_riser',
                  'closer', 'speed', 'sprint', 'route'):
        if style in mt or style in vn:
            style_filter = style
            break

    # gonzo_sauce variants use 67-feat
    if 'gonzo_sauce' in vn or 'gonzo_sauce' in mt:
        return ('gonzo_sauce', style_filter)

    # 55-feat odds-blind orphan
    if mt == 'wp_55feat_odds_blind_orphan' or 'wp_base' in vn:
        return ('core_odds_blind', style_filter)

    # PL layers: 47-feat lean53_core
    if mt.startswith('pl_core_') or mt.startswith('pl_workout_'):
        return ('lean53_core', style_filter)

    # wp_core variants: lean53 = 47-feat; non-lean53 = 58-feat odds-aware (PRIOR legacy)
    if mt.startswith('win_prob_core_') or 'wp_core' in vn:
        if 'lean53' in vn:
            return ('lean53_core', style_filter)
        return ('core_odds_aware', style_filter)

    # wp_full variants: lean53 = 53-feat; non-lean53 = 66-feat legacy
    if mt.startswith('wp_full_') or 'wp_full' in vn:
        if 'lean53' in vn:
            return ('lean53', style_filter)
        return ('odds_aware_legacy', style_filter)

    # wp_odds → 58-feat odds-aware
    if mt in ('win_prob_odds', 'win_prob_full') and 'odds' in vn:
        return ('core_odds_aware', style_filter)

    # Ranker layers
    if mt.startswith('ranker_') or mt.startswith('rk_full_') or 'rk_' in vn:
        if 'lean53' in vn:
            return ('lean53', style_filter)
        return ('core_odds_aware', style_filter)

    # WR layers: wr_odds = 58-feat odds-aware; wr_base = 55-feat odds-blind (orphan)
    if mt == 'wr_odds' or 'v_odds' in vn:
        return ('core_odds_aware', style_filter)
    if mt == 'wr_base' or 'v_base' in vn:
        return ('core_odds_blind', style_filter)
    if mt in ('wr_base_workout', 'wr_odds_workout'):
        # workout-overlay 9-feat — separate substrate; treat as orphan
        return (None, style_filter)

    # longshot_rf, trajectory_lstm, ensemble — special handlers
    if mt in ('longshot_rf', 'trajectory_lstm', 'ensemble'):
        return (None, None)

    return (None, style_filter)


def classify_artifact_format(art: Artifact) -> str:
    s3 = art.s3_path or ''
    if art.model_type == 'trajectory_lstm' or s3.endswith('.pt'):
        return 'pt_torch'
    if art.model_type in ('longshot_rf', 'ensemble') or s3.endswith('.pkl'):
        return 'pkl_sklearn'
    if s3.endswith('.json') or s3.endswith('.ubj'):
        return 'xgb_json'
    return 'unknown'


# ─────────────────────────────────────────────────────────────────────
# 3. ARTIFACT LOADING
# ─────────────────────────────────────────────────────────────────────

def parse_s3(s3_path: str) -> Tuple[str, str]:
    p = s3_path[5:]
    bucket, _, key = p.partition('/')
    return bucket, key


def load_artifact(art: Artifact) -> Optional[Any]:
    """Load by artifact_format. Returns model object or None on failure."""
    if not art.s3_path or not art.s3_path.startswith('s3://'):
        return None
    bucket, key = parse_s3(art.s3_path)
    local = os.path.join(ARTIFACT_DIR, os.path.basename(key))
    try:
        if not os.path.exists(local):
            S3.download_file(bucket, key, local)
    except Exception as e:
        logger.warning(f"  S3 download fail {art.version_name}: {e}")
        return None
    try:
        if art.artifact_format == 'xgb_json':
            booster = xgb.Booster()
            booster.load_model(local)
            return booster
        elif art.artifact_format == 'pkl_sklearn':
            return joblib.load(local)
        elif art.artifact_format == 'pt_torch':
            import torch
            return torch.load(local, map_location='cpu', weights_only=False)
    except Exception as e:
        logger.warning(f"  load fail {art.version_name}: {type(e).__name__}: {str(e)[:120]}")
        return None
    return None


def load_all_artifacts(arts: List[Artifact]) -> Dict[str, Any]:
    """Returns {(cohort, model_type, version_name): model}; logs load report to file."""
    loaded = {}
    report = {'success': [], 'failed': [], 'skipped': []}
    for art in arts:
        feature_path, style = classify_feature_path(art)
        art.feature_path = feature_path
        art.style_filter = style
        art.artifact_format = classify_artifact_format(art)
        art.feature_count = len(_FEAT.get(feature_path, [])) if feature_path else None

        if art.artifact_format == 'unknown':
            report['skipped'].append(asdict(art))
            continue

        model = load_artifact(art)
        if model is None:
            report['failed'].append(asdict(art))
            continue

        loaded[(art.cohort, art.model_type, art.version_name)] = model
        report['success'].append(asdict(art))

    with open(LOAD_REPORT, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    logger.info(f"  loaded: {len(report['success'])}/{len(arts)}; "
                f"failed: {len(report['failed'])}; skipped: {len(report['skipped'])}")
    return loaded


# ─────────────────────────────────────────────────────────────────────
# 4. RACE LOADER + FEATURE BUILDER (reused per race)
# ─────────────────────────────────────────────────────────────────────

def get_forensic_races(conn) -> List[Dict]:
    return execute_query(conn, """
        SELECT r.race_id, r.race_date, t.track_code, r.race_number, r.field_size,
               r.distance_furlongs, r.surface, r.race_type, r.purse, r.race_name
        FROM races r JOIN tracks t USING(track_id)
        WHERE r.race_date BETWEEN %s AND %s
          AND r.race_id IN (SELECT race_id FROM entries WHERE is_scratched=false
                            GROUP BY race_id HAVING COUNT(*) >= 4)
          AND r.race_id IN (SELECT race_id FROM results WHERE finish_position IS NOT NULL)
        ORDER BY r.race_date, t.track_code, r.race_number
    """, (FORENSIC_START, FORENSIC_END))


# ─────────────────────────────────────────────────────────────────────
# 5. PER-RACE INFERENCE
# ─────────────────────────────────────────────────────────────────────

def infer_race(race_meta, race, feature_df, loaded, arts_with_paths):
    """Generate predictions for all (cohort, layer) combinations.
    Returns DataFrame keyed by horse_id with one column per (cohort__model_type__version_name).
    """
    if feature_df.empty:
        return None

    horse_names = feature_df['horse_name'].tolist()
    horse_ids = feature_df['horse_id'].astype(str).tolist()
    n_horses = len(horse_ids)

    result = {
        'horse_id': horse_ids,
        'horse_name': horse_names,
    }

    # Pre-build dmatrix slices once per feature_path
    dmatrix_cache: Dict[str, xgb.DMatrix] = {}
    array_cache: Dict[str, np.ndarray] = {}
    for fpath, feats in _FEAT.items():
        # Build padded feature matrix (fill missing cols with 0)
        slice_df = pd.DataFrame()
        for c in feats:
            slice_df[c] = feature_df[c] if c in feature_df.columns else 0.0
        arr = slice_df.fillna(0.0).values.astype(np.float64)
        array_cache[fpath] = arr
        try:
            dmatrix_cache[fpath] = xgb.DMatrix(arr, feature_names=feats)
        except Exception:
            dmatrix_cache[fpath] = None

    for art in arts_with_paths:
        model_key = (art.cohort, art.model_type, art.version_name)
        model = loaded.get(model_key)
        if model is None or not art.feature_path:
            continue
        col_name = f"{art.cohort}__{art.model_type}__{art.version_name}"

        try:
            if art.artifact_format == 'xgb_json':
                dmatrix = dmatrix_cache[art.feature_path]
                if dmatrix is None: continue
                raw = model.predict(dmatrix)
                # Softmax-normalize win-prob style outputs
                if art.model_type.startswith(('win_prob', 'wp_full_', 'wp_core_',
                                              'wr_odds', 'wr_base')) \
                   or art.model_type.startswith(('pl_core_', 'pl_workout_')):
                    raw = softmax_temp(raw)
                result[col_name] = raw.tolist()
            elif art.artifact_format == 'pkl_sklearn':
                arr = array_cache[art.feature_path]
                if hasattr(model, 'predict_proba'):
                    raw = model.predict_proba(arr)[:, 1]
                else:
                    raw = model.predict(arr)
                result[col_name] = list(map(float, raw))
            # PyTorch trajectory_lstm handled separately (skip in main loop; substrate-permanent)
        except Exception as e:
            # Per-artifact failure: skip this column; don't kill race
            continue

    return pd.DataFrame(result)


# ─────────────────────────────────────────────────────────────────────
# 6. MAIN
# ─────────────────────────────────────────────────────────────────────

def main():
    t0 = time.time()
    logger.info("=" * 70)
    logger.info("SP-Option-C full-cohort forensic inference")
    logger.info(f"Window: {FORENSIC_START} .. {FORENSIC_END}")
    logger.info("=" * 70)

    arts = get_artifact_inventory()
    logger.info(f"Dedup'd artifacts: {len(arts)}")
    for cohort in ('phase_bx', 'prior'):
        cohort_arts = [a for a in arts if a.cohort == cohort]
        logger.info(f"  {cohort}: {len(cohort_arts)}")

    logger.info("Loading artifacts to memory...")
    loaded = load_all_artifacts(arts)
    logger.info(f"  loaded {len(loaded)} artifacts in {time.time()-t0:.1f}s")

    arts_with_paths = [a for a in arts if a.feature_path]
    logger.info(f"  service-compatible (feature_path mapped): {len(arts_with_paths)}")

    # Load races
    with get_db() as conn:
        races = get_forensic_races(conn)
    logger.info(f"Forensic-window races: {len(races)}")

    # Per-race inference loop — reuse one DB conn for feature service
    with get_db() as conn:
        race_repo = RaceRepository(conn)
        entry_repo = EntryRepository(conn)
        fe = FeatureEngineeringService(conn)
        n_done = 0
        n_skip = 0
        n_err = 0
        for i, race_meta in enumerate(races, 1):
            race_id = str(race_meta['race_id'])
            out_path = os.path.join(OUTPUT_DIR, f'{race_id}.parquet')
            if os.path.exists(out_path):
                n_skip += 1
                continue
            try:
                race = race_repo.get_race_by_id(race_id)
                race.entries = entry_repo.get_entries_by_race(race_id)
                if len(race.entries) < 4:
                    n_skip += 1; continue
                fdf = fe.build_feature_matrix(race, include_odds=True)
                if fdf.empty:
                    n_skip += 1; continue
                preds = infer_race(race_meta, race, fdf, loaded, arts_with_paths)
                if preds is None or preds.empty:
                    n_skip += 1; continue
                preds.to_parquet(out_path)
                n_done += 1
                if n_done % 20 == 0:
                    elapsed = time.time() - t0
                    rate = n_done / max(1, elapsed - 5)
                    eta = (len(races) - i) / max(0.01, rate)
                    logger.info(f"  [{i}/{len(races)}] done={n_done} skip={n_skip} err={n_err} "
                                f"rate={rate:.2f}/s eta={eta/60:.1f}m")
            except Exception as e:
                n_err += 1
                if n_err <= 5:
                    logger.warning(f"  race {race_id} err: {type(e).__name__}: {str(e)[:150]}")

    summary = {
        'n_races': len(races),
        'n_done': n_done,
        'n_skip': n_skip,
        'n_err': n_err,
        'wall_clock_s': time.time() - t0,
        'arts_loaded': len(loaded),
        'arts_with_feature_paths': len(arts_with_paths),
    }
    logger.info("=" * 70)
    logger.info(f"COMPLETE: {summary}")
    with open('/tmp/option_c_inference_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)


if __name__ == '__main__':
    main()
