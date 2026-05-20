"""
MultiCohortInferenceService — production wiring for Hybrid C ensemble.

Loads 32 L1 artifacts (16 Phase B.x + 14 PRIOR) pinned by (model_type, version_name)
matching the Hybrid C training schema, runs predictions per race, applies the
Hybrid C XGBoost ensemble, and persists results to hybrid_c_predictions.

Substrate notes:
  - L1 artifacts are pinned by version_name (NOT by is_active) — this matches the
    exact 32 columns Hybrid C was trained on, robust to future activation churn.
  - FeatureEngineeringService.build_feature_matrix() supplies the per-race feature
    DataFrame; we slice per feature_path (47/53/55/58/66/67-feat) per artifact.
  - Hybrid C feature_names use the form `{cohort}__{model_type}__{version_name}`;
    we generate input columns in that exact form for the Booster.
  - Softmax-temp normalization applies to win-prob style outputs to match training.
"""
from __future__ import annotations
import os
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any

import boto3
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb

from shared.db import execute_query, execute_write
from services.feature_engineering_service import FeatureEngineeringService
from services.feature_contract import (
    get_model_features, predict_with_contract,
)
from repositories.race_repository import RaceRepository
from repositories.entry_repository import EntryRepository
from model.shared.feature_definitions import (
    get_lean53_core_features, get_lean53_features,
    get_core_features, get_odds_aware_features,
    get_gonzo_sauce_features,
)

logger = logging.getLogger(__name__)

HYBRID_C_VERSION_NAME = 'option_c_hybrid_ensemble_20260515'
HYBRID_C_S3_PATH = 's3://equine-model-artifacts/ensemble/option_c_hybrid_ensemble_20260515.json'
SOFTMAX_TEMPERATURE = 0.15

# 32 L1 inputs pinned by (cohort, model_type, version_name).
# Mirrors /tmp/option_c_hybrid_ensemble_meta.json l1_inputs exactly.
HYBRID_C_L1_SPECS: List[Tuple[str, str, str]] = [
    ('phase_bx', 'rk_full_speed', 'rk_full_lean53_speed_20260513_0324'),
    ('phase_bx', 'rk_full_closer', 'rk_full_lean53_closer_20260513_0327'),
    ('phase_bx', 'rk_full_class_riser', 'rk_full_lean53_class_riser_20260513_0302'),
    ('phase_bx', 'rk_full_route', 'rk_full_lean53_route_20260513_0255'),
    ('phase_bx', 'rk_full_sprint', 'rk_full_lean53_sprint_20260513_0251'),
    ('phase_bx', 'rk_full_gonzo_sauce', 'rk_full_lean53_gonzo_sauce_20260513_0324'),
    ('phase_bx', 'wp_full_general', 'wp_full_lean53_20260513_0311'),
    ('phase_bx', 'wp_full_speed', 'wp_full_lean53_speed_20260513_0325'),
    ('phase_bx', 'wp_full_closer', 'wp_full_lean53_closer_20260513_0324'),
    ('phase_bx', 'wp_full_route', 'wp_full_lean53_route_20260513_0255'),
    ('phase_bx', 'wp_full_class_dropper', 'wp_full_lean53_class_dropper_20260513_0325'),
    ('phase_bx', 'wp_full_class_riser', 'wp_full_lean53_class_riser_20260513_0323'),
    ('phase_bx', 'wp_full_sprint', 'wp_full_lean53_sprint_20260513_0258'),
    ('phase_bx', 'wp_full_gonzo_sauce', 'wp_full_lean53_gonzo_sauce_20260513_0310'),
    ('phase_bx', 'wr_base', 'v_base_core_20260513_0259'),
    ('phase_bx', 'pl_core_route', 'pl_core_lean53_route_20260513_0246'),
    ('phase_bx', 'wr_odds', 'v_odds_core_20260513_0259'),
    ('phase_bx', 'ranker_core', 'rk_core_20260513_0323'),
    ('phase_bx', 'win_prob_full', 'wp_odds_20260513_0126'),
    ('prior', 'pl_core_general', 'pl_core_lean53_20260429_1907'),
    ('prior', 'pl_core_speed', 'pl_core_lean53_speed_20260429_1906'),
    ('prior', 'pl_core_closer', 'pl_core_lean53_closer_20260429_1856'),
    ('prior', 'pl_core_class_riser', 'pl_core_lean53_class_riser_20260429_1856'),
    ('prior', 'pl_core_class_dropper', 'pl_core_lean53_class_dropper_20260429_1906'),
    ('prior', 'pl_core_sprint', 'pl_core_lean53_sprint_20260429_1845'),
    ('prior', 'rk_full_class_dropper', 'rk_full_lean53_class_dropper_20260429_1854'),
    ('prior', 'win_prob_core_speed', 'wp_core_lean53_speed_20260429_2348'),
    ('prior', 'win_prob_core_closer', 'wp_core_lean53_closer_20260429_2348'),
    ('prior', 'win_prob_core_class_riser', 'wp_core_lean53_class_riser_20260429_2338'),
    ('prior', 'win_prob_core_class_dropper', 'wp_core_lean53_class_dropper_20260429_2338'),
    ('prior', 'win_prob_core_sprint', 'wp_core_lean53_sprint_20260429_2332'),
    ('prior', 'win_prob_core_route', 'wp_core_lean53_route_20260429_2329'),
]


def softmax_temp(raw: np.ndarray, T: float = SOFTMAX_TEMPERATURE) -> np.ndarray:
    raw = np.asarray(raw, dtype=np.float64)
    s = (raw - raw.max()) / T
    s = np.clip(s, -20, 0)
    e = np.exp(s)
    total = e.sum()
    return e / total if total > 0 else e


@dataclass
class L1Artifact:
    cohort: str
    model_type: str
    version_name: str
    s3_path: str
    feature_path: str  # one of: lean53_core / lean53 / core_odds_blind / core_odds_aware / odds_aware_legacy / gonzo_sauce
    artifact_format: str  # xgb_json / pkl_sklearn
    model: Any = None  # populated by loader
    column_name: str = ''  # cohort__model_type__version_name


def classify_feature_path(model_type: str, version_name: str) -> str:
    """Map (model_type, version_name) → feature_path key.

    Substrate-pragmatic substrate-grounded mapping — covers all 32 Hybrid C L1 inputs.
    """
    mt = model_type
    vn = (version_name or '').lower()

    if 'gonzo_sauce' in vn or 'gonzo_sauce' in mt:
        return 'gonzo_sauce'
    if mt.startswith('pl_core_'):
        return 'lean53_core'
    if mt.startswith('win_prob_core_'):
        # PRIOR specialists are lean53_core-trained (47-feat)
        return 'lean53_core' if 'lean53' in vn else 'core_odds_aware'
    if mt.startswith('wp_full_'):
        return 'lean53' if 'lean53' in vn else 'odds_aware_legacy'
    if mt in ('win_prob_full', 'win_prob_odds'):
        return 'core_odds_aware'
    if mt.startswith('rk_full_') or mt == 'ranker_core':
        return 'lean53' if 'lean53' in vn else 'core_odds_aware'
    if mt == 'wr_odds':
        return 'core_odds_aware'
    if mt == 'wr_base':
        return 'core_odds_blind'
    raise ValueError(f"Unmappable feature_path for model_type={mt} version_name={vn}")


def classify_artifact_format(s3_path: str) -> str:
    if s3_path.endswith('.json') or s3_path.endswith('.ubj'):
        return 'xgb_json'
    if s3_path.endswith('.pkl'):
        return 'pkl_sklearn'
    if s3_path.endswith('.pt'):
        return 'pt_torch'
    return 'unknown'


def _parse_s3(s3_path: str) -> Tuple[str, str]:
    p = s3_path[5:]
    bucket, _, key = p.partition('/')
    return bucket, key


class MultiCohortInferenceService:
    """Production service that runs all 32 L1 layers + Hybrid C ensemble per race."""

    # β.1 sprint extension constants (per Q1 P1 + Q-pre-β-1 Option B; substrate-grounded
    # against substrate-permanent reference Sections 1.10 + 6.2 at commit 15891fa)
    SPRINT_MODEL_VERSION_ID = '1202021f-2937-46eb-a1fd-0dd9b0d1fe20'
    SPRINT_ENSEMBLE_VERSION = 'specialist_style_sprint_20260518_0252'
    SPRINT_S3_PATH = 's3://equine-model-artifacts/ensemble/test/specialist_style_specialist_sprint_20260518_0252.json'
    SPRINT_DISTANCE_THRESHOLD_FURLONGS = 6.5

    # Class-level cache to keep loaded artifacts across Lambda warm-starts
    _instance_cache: Dict[str, Any] = {}

    def __init__(self, conn):
        self.conn = conn
        self.s3 = boto3.client('s3')
        self.fe = FeatureEngineeringService(conn)
        self.race_repo = RaceRepository(conn)
        self.entry_repo = EntryRepository(conn)

        # Pre-compute feature lists once
        self._features = {
            'lean53_core': get_lean53_core_features(),
            'lean53': get_lean53_features(),
            'core_odds_blind': get_core_features(False),
            'core_odds_aware': get_core_features(True),
            'odds_aware_legacy': get_odds_aware_features(),
            'gonzo_sauce': get_gonzo_sauce_features(),
        }

        self._l1_artifacts: List[L1Artifact] = []
        self._hybrid_c_booster: Optional[xgb.Booster] = None
        self._hybrid_c_feature_names: List[str] = []
        self._sprint_booster: Optional[xgb.Booster] = None

    def initialize(self) -> Dict[str, Any]:
        """Load all 32 L1 artifacts + Hybrid C ensemble. Idempotent."""
        if 'l1_artifacts' in self._instance_cache:
            self._l1_artifacts = self._instance_cache['l1_artifacts']
            self._hybrid_c_booster = self._instance_cache['hybrid_c']
            self._hybrid_c_feature_names = self._hybrid_c_booster.feature_names
            return {'status': 'cached', 'l1_count': len(self._l1_artifacts)}

        # Resolve L1 (model_type, version_name) → s3_path via DB
        rows = execute_query(self.conn, """
            SELECT model_type, version_name, s3_artifact_path
            FROM model_versions
            WHERE (model_type, version_name) IN %s
        """, (tuple((mt, vn) for _, mt, vn in HYBRID_C_L1_SPECS),))
        s3_lookup = {(r['model_type'], r['version_name']): r['s3_artifact_path'] for r in rows}

        artifacts = []
        missing = []
        for cohort, mt, vn in HYBRID_C_L1_SPECS:
            s3_path = s3_lookup.get((mt, vn))
            if not s3_path:
                missing.append((cohort, mt, vn))
                continue
            try:
                feature_path = classify_feature_path(mt, vn)
            except ValueError as e:
                logger.error(f"Unmappable feature_path: {e}")
                missing.append((cohort, mt, vn))
                continue
            artifacts.append(L1Artifact(
                cohort=cohort,
                model_type=mt,
                version_name=vn,
                s3_path=s3_path,
                feature_path=feature_path,
                artifact_format=classify_artifact_format(s3_path),
                column_name=f"{cohort}__{mt}__{vn}",
            ))

        if missing:
            raise RuntimeError(f"L1 artifacts missing in model_versions for: {missing}")

        # Load each artifact from S3
        for art in artifacts:
            art.model = self._load_artifact(art)

        # Load Hybrid C ensemble
        local_path = '/tmp/option_c_hybrid_ensemble.json'
        bucket, key = _parse_s3(HYBRID_C_S3_PATH)
        if not os.path.exists(local_path):
            self.s3.download_file(bucket, key, local_path)
        booster = xgb.Booster()
        booster.load_model(local_path)

        self._l1_artifacts = artifacts
        self._hybrid_c_booster = booster
        self._hybrid_c_feature_names = booster.feature_names

        self._instance_cache['l1_artifacts'] = artifacts
        self._instance_cache['hybrid_c'] = booster

        logger.info(f"MultiCohortInferenceService initialized: "
                    f"{len(artifacts)} L1 artifacts, Hybrid C "
                    f"({len(self._hybrid_c_feature_names)} features)")
        return {'status': 'loaded', 'l1_count': len(artifacts),
                'hybrid_c_feature_count': len(self._hybrid_c_feature_names)}

    def _load_artifact(self, art: L1Artifact) -> Any:
        local = f'/tmp/mci_artifacts/{art.cohort}__{art.model_type}__{art.version_name}'
        os.makedirs('/tmp/mci_artifacts', exist_ok=True)
        bucket, key = _parse_s3(art.s3_path)
        # Use basename of s3 key as local file extension to match artifact_format dispatch
        local_path = local + '_' + os.path.basename(key)
        if not os.path.exists(local_path):
            self.s3.download_file(bucket, key, local_path)

        if art.artifact_format == 'xgb_json':
            booster = xgb.Booster()
            booster.load_model(local_path)
            return booster
        if art.artifact_format == 'pkl_sklearn':
            return joblib.load(local_path)
        raise RuntimeError(f"Unsupported artifact_format={art.artifact_format} for {art.column_name}")

    def _load_sprint_sub_booster(self) -> xgb.Booster:
        """β.1 sprint sub-booster lazy-load. Substrate-grounded against substrate-permanent
        reference Section 1.9 _load_artifact verbatim + Section 6.2 sprint S3 path verbatim.

        Substrate-pragmatic: artifact_format=xgb_json (per Section 6.2 .json extension);
        same load + idempotent S3 download pattern as Hybrid C ensemble (initialize() lines
        222-227). Route sub-booster NEVER loaded per Q2 R1 deprecation.
        """
        if self._sprint_booster is not None:
            return self._sprint_booster
        if 'sprint_booster' in self._instance_cache:
            self._sprint_booster = self._instance_cache['sprint_booster']
            return self._sprint_booster

        local_path = '/tmp/specialist_style_sprint_20260518_0252.json'
        bucket, key = _parse_s3(self.SPRINT_S3_PATH)
        if not os.path.exists(local_path):
            self.s3.download_file(bucket, key, local_path)
        booster = xgb.Booster()
        booster.load_model(local_path)
        self._sprint_booster = booster
        self._instance_cache['sprint_booster'] = booster
        logger.info(f"Sprint sub-booster loaded ({len(booster.feature_names)} features) "
                    f"version={self.SPRINT_ENSEMBLE_VERSION}")
        return booster

    def predict_race(self, race_id: str) -> Optional[Dict[str, Any]]:
        """Generate 32 L1 predictions + Hybrid C ensemble for one race.

        Returns dict with horse_ids and per-horse Hybrid C win probabilities,
        or None if race ineligible (no feature matrix / scratched / etc.).
        """
        if not self._l1_artifacts:
            self.initialize()

        race = self.race_repo.get_race_by_id(race_id)
        if race is None:
            logger.warning(f"race {race_id} not found")
            return None
        race.entries = self.entry_repo.get_entries_by_race(race_id, as_of_date=race.race_date)
        if len(race.entries) < 4:
            return None

        feature_df = self.fe.build_feature_matrix(race, include_odds=True)
        if feature_df.empty:
            return None

        horse_ids = feature_df['horse_id'].astype(str).tolist()
        n_horses = len(horse_ids)

        # REPAIR-5: pad feature_df with columns required by ANY xgb_json L1
        # artifact so predict_with_contract doesn't raise on substrate-coverage
        # gaps. sklearn artifacts still use the per-feature-path positional
        # array (pickled models depend on training-time feature ordering).
        xgb_arts = [
            a for a in self._l1_artifacts
            if a.artifact_format == 'xgb_json' and a.model is not None
        ]
        needed_xgb_features: set = set()
        for art in xgb_arts:
            needed_xgb_features.update(get_model_features(art.model))
        for col in needed_xgb_features:
            if col not in feature_df.columns:
                feature_df[col] = 0.0

        # Build per-feature-path array slices for sklearn artifacts only.
        # xgb_json uses booster.feature_names via predict_with_contract.
        array_cache: Dict[str, np.ndarray] = {}
        for fpath, feats in self._features.items():
            slice_df = pd.DataFrame()
            for c in feats:
                slice_df[c] = feature_df[c] if c in feature_df.columns else 0.0
            array_cache[fpath] = slice_df.fillna(0.0).values.astype(np.float64)

        # Generate L1 predictions per artifact
        l1_outputs: Dict[str, np.ndarray] = {}
        for art in self._l1_artifacts:
            try:
                if art.artifact_format == 'xgb_json':
                    raw = predict_with_contract(art.model, feature_df)
                    # Apply softmax for win-prob style outputs (matches training pipeline)
                    if (art.model_type.startswith(('win_prob', 'wp_full_', 'wp_core_', 'pl_'))
                            or art.model_type in ('wr_odds', 'wr_base')):
                        raw = softmax_temp(raw)
                    l1_outputs[art.column_name] = raw
                elif art.artifact_format == 'pkl_sklearn':
                    arr = array_cache.get(art.feature_path)
                    if arr is None:
                        l1_outputs[art.column_name] = np.zeros(n_horses)
                        continue
                    if hasattr(art.model, 'predict_proba'):
                        raw = art.model.predict_proba(arr)[:, 1]
                    else:
                        raw = art.model.predict(arr)
                    l1_outputs[art.column_name] = np.asarray(raw, dtype=np.float64)
            except Exception as e:
                logger.warning(f"L1 predict failed for {art.column_name}: {type(e).__name__}: {e}")
                l1_outputs[art.column_name] = np.zeros(n_horses)

        # Construct Hybrid C input in feature_names order
        X = np.column_stack([
            l1_outputs.get(name, np.zeros(n_horses))
            for name in self._hybrid_c_feature_names
        ])
        dmat = xgb.DMatrix(X, feature_names=self._hybrid_c_feature_names)
        raw_hybrid = self._hybrid_c_booster.predict(dmat)

        # Race-normalize Hybrid C to sum-to-1 per race (matches calibration of B/A cohorts)
        if raw_hybrid.sum() > 0:
            hybrid_c_probs = raw_hybrid / raw_hybrid.sum()
        else:
            hybrid_c_probs = raw_hybrid

        return {
            'race_id': race_id,
            'horse_ids': horse_ids,
            'hybrid_c_win_probability': hybrid_c_probs.tolist(),
            'hybrid_c_raw': raw_hybrid.tolist(),
            'l1_outputs': {k: v.tolist() for k, v in l1_outputs.items()},
        }

    def write_predictions(self, result: Dict[str, Any]) -> int:
        """Persist Hybrid C predictions to hybrid_c_predictions table. Idempotent."""
        if not result:
            return 0
        race_id = result['race_id']
        horse_ids = result['horse_ids']
        probs = result['hybrid_c_win_probability']
        rows_inserted = 0
        for hid, p in zip(horse_ids, probs):
            execute_write(self.conn, """
                INSERT INTO hybrid_c_predictions
                  (race_id, horse_id, hybrid_c_win_probability,
                   l1_input_count, ensemble_version)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (race_id, horse_id, ensemble_version)
                DO NOTHING
            """, (race_id, hid, float(p), len(self._l1_artifacts), HYBRID_C_VERSION_NAME))
            rows_inserted += 1
        return rows_inserted

    def predict_race_with_routing(self, race_id: str) -> Optional[Dict[str, Any]]:
        """β.1 sprint-routing extension. Substrate-grounded against substrate-permanent
        reference Sections 1.10 (ensemble_version convention) + 6.5 (distance dispatch
        boundary) at commit 15891fa.

        Routing semantics (Q1 P1 + Q2 R1):
          - Hybrid C canonical always computed (production path UNCHANGED)
          - Distance ≤ 6.5 furlongs → sprint sub-booster invoked; result tagged
            'route_dispatch'='sprint'; specialist_style_sprint_win_probability populated
          - Distance > 6.5 furlongs OR NULL → 'route_dispatch'='hybrid_c_canonical';
            specialist_style_sprint_win_probability=None
          - Route sub-booster DEPRECATED per Q2 R1; never invoked

        Returns predict_race result dict augmented with:
          - 'specialist_style_sprint_win_probability': List[float] | None
          - 'specialist_style_sprint_raw': List[float] | None
          - 'route_dispatch': 'sprint' | 'hybrid_c_canonical'
        None if race ineligible per predict_race substrate.
        """
        result = self.predict_race(race_id)
        if result is None:
            return None

        race = self.race_repo.get_race_by_id(race_id)
        distance = race.distance_furlongs if race is not None else None

        if distance is not None and distance <= self.SPRINT_DISTANCE_THRESHOLD_FURLONGS:
            sprint_booster = self._load_sprint_sub_booster()
            l1_outputs = result['l1_outputs']
            n_horses = len(result['horse_ids'])
            sprint_feature_names = sprint_booster.feature_names
            # Sprint sub-booster consumes same 32 L1 inputs as Hybrid C per
            # substrate-permanent reference Section 6.3 verbatim
            X = np.column_stack([
                np.asarray(l1_outputs.get(name, [0.0] * n_horses), dtype=np.float64)
                for name in sprint_feature_names
            ])
            dmat = xgb.DMatrix(X, feature_names=sprint_feature_names)
            raw_sprint = sprint_booster.predict(dmat)
            # Race-normalize sprint to sum-to-1 per race (mirrors Hybrid C convention)
            if raw_sprint.sum() > 0:
                sprint_probs = raw_sprint / raw_sprint.sum()
            else:
                sprint_probs = raw_sprint
            result['specialist_style_sprint_win_probability'] = sprint_probs.tolist()
            result['specialist_style_sprint_raw'] = raw_sprint.tolist()
            result['route_dispatch'] = 'sprint'
        else:
            result['specialist_style_sprint_win_probability'] = None
            result['specialist_style_sprint_raw'] = None
            result['route_dispatch'] = 'hybrid_c_canonical'

        return result

    def write_specialist_style_sprint(self, result: Dict[str, Any]) -> int:
        """β.1 sprint dual-write to hybrid_c_predictions. Substrate-grounded against
        substrate-permanent reference Section 1.10 ensemble_version convention +
        Section 5 D12 UNIQUE constraint (dual-write substrate-coherent natively).

        Write-once: ON CONFLICT (race_id, horse_id, ensemble_version) DO NOTHING
        (UNFUCK-1 Step B; substrate-protect race-fire-time write from
        post-race re-invocation overwrite per AS-OF leakage finding).
        Writes ONLY when result contains sprint predictions (route_dispatch='sprint').
        Substrate-coherent no-op when route_dispatch='hybrid_c_canonical' OR result None.
        """
        if not result:
            return 0
        sprint_probs = result.get('specialist_style_sprint_win_probability')
        if sprint_probs is None:
            return 0
        race_id = result['race_id']
        horse_ids = result['horse_ids']
        rows_inserted = 0
        for hid, p in zip(horse_ids, sprint_probs):
            execute_write(self.conn, """
                INSERT INTO hybrid_c_predictions
                  (race_id, horse_id, hybrid_c_win_probability,
                   l1_input_count, ensemble_version)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (race_id, horse_id, ensemble_version)
                DO NOTHING
            """, (race_id, hid, float(p), len(self._l1_artifacts),
                  self.SPRINT_ENSEMBLE_VERSION))
            rows_inserted += 1
        return rows_inserted

    def run_daily_predictions(self, race_date) -> Dict[str, Any]:
        """Run Hybrid C inference for all eligible races on a given date."""
        if not self._l1_artifacts:
            self.initialize()

        races = execute_query(self.conn, """
            SELECT r.race_id::text AS race_id
            FROM races r
            WHERE r.race_date = %s
              AND r.race_id IN (
                SELECT race_id FROM entries
                WHERE COALESCE(is_scratched, FALSE) = FALSE
                GROUP BY race_id HAVING COUNT(*) >= 4
              )
            ORDER BY r.race_id
        """, (race_date,))

        n_done = 0
        n_skip = 0
        n_err = 0
        for r in races:
            try:
                result = self.predict_race(r['race_id'])
                if result is None:
                    n_skip += 1
                    continue
                self.write_predictions(result)
                n_done += 1
            except Exception as e:
                n_err += 1
                if n_err <= 5:
                    logger.warning(f"race {r['race_id']} err: {type(e).__name__}: {e}")

        summary = {
            'date': str(race_date),
            'n_races': len(races),
            'n_done': n_done,
            'n_skip': n_skip,
            'n_err': n_err,
            'l1_artifact_count': len(self._l1_artifacts),
            'ensemble_version': HYBRID_C_VERSION_NAME,
        }
        logger.info(f"MultiCohortInferenceService daily complete: {summary}")
        return summary
