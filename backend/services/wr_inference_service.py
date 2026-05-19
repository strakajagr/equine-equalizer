import os
import json
import logging
import boto3
import numpy as np
import pandas as pd
import xgboost as xgb
from datetime import date
from typing import Optional
from models.canonical import Race, Entry, Prediction
from repositories.wr_prediction_repository import (
    WRPredictionRepository
)
from repositories.model_version_repository import (
    ModelVersionRepository
)
from repositories.race_repository import RaceRepository
from repositories.entry_repository import EntryRepository
from services.feature_engineering_service import (
    FeatureEngineeringService
)
from model.shared.feature_definitions import (
    get_core_features
)
from shared.constants import (
    OVERLAY_THRESHOLD,
    HANDICAPPING_BLEND_WEIGHT,
)
from model.shared.feature_definitions import (
    get_odds_aware_features,
    get_ranker_full_features,
    get_lean53_features,
    get_gonzo_sauce_features,
)
from model.shared.par_times import compute_workout_pars

logger = logging.getLogger(__name__)

CORE_FEATURES = get_core_features(include_odds=True)   # 58 core features (no workouts)
FULL_FEATURES = get_lean53_features()                  # 53 features — lean53 wp_full
LEGACY_FULL_FEATURES = get_odds_aware_features()       # 66 — fallback for legacy artifacts
RANKER_FULL_FEATURES = get_lean53_features()           # 53 — lean53 rk_full
GONZO_FULL_FEATURES = get_gonzo_sauce_features()       # 67 — Phase A3 gonzo_sauce wp + rk
WR_FEATURES = CORE_FEATURES  # backward compat alias

# Layer 3: Value overlay constants
VALUE_MIN_EDGE = 0.05
VALUE_HALF_KELLY = 0.5
VALUE_MAX_KELLY = 0.10
VALUE_BANKROLL = 1000.0


def compute_value_overlay(raw_win_prob: float, morning_line_odds: float) -> dict:
    """
    Layer 3: Compare model P(win) to morning line implied probability.
    Pure arithmetic — no trained model.
    """
    if morning_line_odds is None or morning_line_odds <= 0:
        return {'edge_pct': 0.0, 'kelly_fraction': 0.0, 'kelly_bet': 0.0,
                'is_value': False, 'implied_prob': 0.0}

    implied_prob = 1.0 / (morning_line_odds + 1.0)
    edge = raw_win_prob - implied_prob

    b = morning_line_odds  # net odds
    p = raw_win_prob
    q = 1.0 - p
    kelly = max(0.0, (b * p - q) / b) * VALUE_HALF_KELLY
    kelly = min(kelly, VALUE_MAX_KELLY)

    is_value = edge >= VALUE_MIN_EDGE
    kelly_bet = round(kelly * VALUE_BANKROLL, 2) if is_value else 0.0

    return {
        'edge_pct': round(edge, 4),
        'kelly_fraction': round(kelly, 4),
        'kelly_bet': kelly_bet,
        'is_value': is_value,
        'implied_prob': round(implied_prob, 4),
    }


class WRInferenceService:
    """
    Dual-model inference pipeline.

    Loads 4 models:
      - win_prob_core (58 features, binary:logistic)
      - win_prob_full (66 features, binary:logistic, workout-aware)
      - ranker_core (58 features, rank:pairwise)
      - ranker_full (66 features, rank:pairwise, workout-aware)

    Per horse:
      - If horse HAS workout data → use _full models (66 features)
      - If horse has NO workout data → use _core models (58 features)

    Computes Layer 3 value overlay on raw P(win).
    Stores all predictions in wr_predictions.
    """

    VALID_STYLES = (
        'general', 'speed', 'closer', 'class_riser',
        'class_dropper', 'sprint', 'route',
        'gonzo_sauce',  # Phase A3 — lean53 + 14 features = 67 total
    )

    def __init__(self, conn, style: str = 'general'):
        if style not in self.VALID_STYLES:
            raise ValueError(
                f"Invalid style {style!r}. Valid: {self.VALID_STYLES}"
            )
        self.style = style
        self.conn = conn
        # Layer 1: Win probability models
        self.wp_core_model = None
        self.wp_full_model = None
        self.wp_core_version = None
        self.wp_full_version = None
        # Layer 2: Ranker models
        self.rk_core_model = None
        self.rk_full_model = None
        # Calibration sidecars (lean53). None = no calibration applied.
        self.wp_full_calibration = None  # tuple (x_thresholds, y_thresholds) or None
        self.wp_core_calibration = None  # same shape; None for legacy artifacts
        # Phase A3: ranker calibration for gonzo_sauce. Other styles keep
        # the BYPASSED-calibration pattern (Bug #15) until the gallery-wide
        # fix workstream lands.
        self.rk_full_calibration = None
        # Phase A3: par-time dict for noteworthy-workout features. Built lazily
        # in load_model() when style='gonzo_sauce' to avoid the workouts-table
        # query on non-gonzo paths.
        self.par_dict: dict = {}
        # Per-loaded-artifact feature set (lean53 → 47 features for core,
        # 53 for full; legacy → 58 for core, 66 for full).
        self.wp_core_features = CORE_FEATURES
        self.wp_full_features = FULL_FEATURES
        # Backward compat
        self.model = None
        self.model_version = None
        self.model_metadata = {}
        self.fe_service = FeatureEngineeringService(conn)
        self.prediction_repo = WRPredictionRepository(conn)
        self.model_version_repo = ModelVersionRepository(
            conn
        )

    # ═══════════════════════════════════════
    # PUBLIC: Model loading
    # ═══════════════════════════════════════

    def load_model(self) -> None:
        """Load all available models (core + full, win_prob + ranker)."""
        # Layer 1: Win probability core (fallback for non-workout horses).
        # Look up specialist-specific lean53 first (added Stream A2.9), then
        # fall back to legacy general core artifacts.
        wp_core_types = [
            f'win_prob_core_{self.style}',
            'win_prob_core', 'win_prob_odds', 'wr_odds',
        ]
        self.wp_core_version = self._try_load_model_type(wp_core_types)
        if self.wp_core_version:
            self.wp_core_model = self._download_model(
                self.wp_core_version, f'/tmp/wp-core-{self.style}'
            )
            # Detect lean53 by version_name suffix; switch feature set.
            if 'lean53' in (self.wp_core_version.version_name or ''):
                from model.shared.feature_definitions import (
                    get_lean53_core_features,
                )
                self.wp_core_features = get_lean53_core_features()
                self.wp_core_calibration = self._try_load_calibration(
                    self.wp_core_version, f'/tmp/wp-core-{self.style}'
                )
                if self.wp_core_calibration is not None:
                    logger.info(
                        f"wp_core lean53 calibration loaded "
                        f"({len(self.wp_core_calibration[0])} thresholds)"
                    )
            else:
                # Legacy artifact (wp_odds 58-feature) — no calibration sidecar
                self.wp_core_features = CORE_FEATURES
                self.wp_core_calibration = None
            logger.info(
                f"wp_core feature set: {len(self.wp_core_features)} features "
                f"(version={self.wp_core_version.version_name})"
            )
            # backward compat
            self.model = self.wp_core_model
            self.model_version = self.wp_core_version

        # _full models are style-specific. _core stays general (only _full
        # was specialist-trained).
        if self.style == 'general':
            wp_full_types = ['wp_full_general', 'win_prob_full']
            rk_full_types = ['rk_full_general', 'ranker_full']
        else:
            wp_full_types = [f'wp_full_{self.style}']
            rk_full_types = [f'rk_full_{self.style}']

        self.wp_full_version = self._try_load_model_type(wp_full_types)
        if self.wp_full_version:
            self.wp_full_model = self._download_model(
                self.wp_full_version, f'/tmp/wp-full-{self.style}'
            )
            self.wp_full_calibration = self._try_load_calibration(
                self.wp_full_version, f'/tmp/wp-full-{self.style}'
            )
            if self.wp_full_calibration is not None:
                logger.info(
                    f"wp_full calibration loaded "
                    f"({len(self.wp_full_calibration[0])} thresholds)"
                )

        # Layer 2: Ranker
        rk_core_ver = self._try_load_model_type(
            ['ranker_core']
        )
        if rk_core_ver:
            self.rk_core_model = self._download_model(
                rk_core_ver, '/tmp/rk-core'
            )
        rk_full_ver = self._try_load_model_type(rk_full_types)
        if rk_full_ver:
            self.rk_full_model = self._download_model(
                rk_full_ver, f'/tmp/rk-full-{self.style}'
            )
            # Phase A3: load ranker calibration sidecar for gonzo_sauce
            # (only style with calibration fit against ranker outputs).
            if self.style == 'gonzo_sauce':
                self.rk_full_calibration = self._try_load_calibration(
                    rk_full_ver, f'/tmp/rk-full-{self.style}'
                )
                if self.rk_full_calibration is not None:
                    logger.info(
                        f"rk_full calibration loaded "
                        f"({len(self.rk_full_calibration[0])} thresholds) "
                        f"— gonzo_sauce Bug #15 fix path"
                    )

        # Phase A3: par-time dict for gonzo_sauce noteworthy-workout features.
        # Built once per service instance — single workouts-table query.
        if self.style == 'gonzo_sauce':
            self.par_dict = compute_workout_pars(self.conn)

        loaded = []
        if self.wp_core_model: loaded.append('wp_core')
        if self.wp_full_model: loaded.append(
            f'wp_full({self.wp_full_version.version_name})')
        if self.rk_core_model: loaded.append('rk_core')
        if self.rk_full_model and rk_full_ver: loaded.append(
            f'rk_full({rk_full_ver.version_name})')
        logger.info(f"Models loaded (style={self.style}): {loaded}")

        if not self.wp_core_model:
            raise ValueError(
                "No win probability core model found. "
                "Train and activate win_prob_core."
            )
        if self.style != 'general' and not self.wp_full_model:
            raise ValueError(
                f"No specialist wp_full found for style={self.style}. "
                f"Expected model_type=wp_full_{self.style} active in "
                f"model_versions."
            )

    def _try_load_model_type(self, type_list):
        """Try model types in priority order, return first found."""
        for mt in type_list:
            ver = self.model_version_repo.get_active_model_by_type(mt)
            if ver:
                return ver
        return None

    def _download_model(self, version, local_dir):
        """Download XGBoost model from S3."""
        s3_path = version.s3_artifact_path
        if not s3_path:
            return None
        s3_path = s3_path.rstrip('/')
        if not s3_path.startswith('s3://'):
            return None
        parts = s3_path[5:].split('/', 1)
        bucket = parts[0]
        prefix = parts[1] if len(parts) > 1 else ''

        os.makedirs(local_dir, exist_ok=True)
        s3_client = boto3.client('s3')
        model_key = prefix
        local_model = f"{local_dir}/model.json"

        logger.info(f"Loading model from s3://{bucket}/{model_key}")
        s3_client.download_file(bucket, model_key, local_model)

        model = xgb.Booster()
        model.load_model(local_model)
        return model

    def _try_load_calibration(self, version, local_dir):
        """Try to load <model>_calibration.json sidecar from S3.
        Returns (x_thresholds, y_thresholds) or None if absent.
        """
        s3_path = version.s3_artifact_path
        if not s3_path or not s3_path.startswith('s3://'):
            return None
        cal_uri = s3_path.replace('.json', '_calibration.json')
        parts = cal_uri[5:].split('/', 1)
        bucket = parts[0]
        key = parts[1] if len(parts) > 1 else ''
        os.makedirs(local_dir, exist_ok=True)
        local_cal = f"{local_dir}/calibration.json"
        try:
            boto3.client('s3').download_file(bucket, key, local_cal)
            with open(local_cal) as f:
                cal = json.load(f)
            return (
                np.array(cal['x_thresholds'], dtype=float),
                np.array(cal['y_thresholds'], dtype=float),
            )
        except Exception as e:
            logger.warning(
                f"No calibration sidecar for "
                f"{version.version_name}: {e}"
            )
            return None

    @staticmethod
    def _apply_calibration(raw, calibration):
        """Apply isotonic calibration via piecewise-linear interpolation.
        raw: scalar or 1-D ndarray of pre-cal probabilities/scores.
        Returns calibrated values clipped to [0, 1].
        """
        if calibration is None:
            return raw
        xt, yt = calibration
        return np.clip(np.interp(raw, xt, yt), 0.0, 1.0)

        s3_path = self.model_version.s3_artifact_path
        if not s3_path:
            raise ValueError(
                f"WR model {self.model_version.version_name}"
                f" has no S3 artifact path"
            )

        s3_path = s3_path.rstrip('/')
        if s3_path.startswith('s3://'):
            parts = s3_path[5:].split('/', 1)
            bucket = parts[0]
            prefix = parts[1] if len(parts) > 1 else ''
        else:
            raise ValueError(
                f"Invalid S3 path: {s3_path}"
            )

        local_dir = '/tmp/wr-model'
        os.makedirs(local_dir, exist_ok=True)

        s3_client = boto3.client('s3')

        # New artifact format: s3_path points directly
        # to the model JSON file (e.g. wr/v_odds_core_20260320.json)
        # Metadata is at {base}_meta.json
        model_key = prefix
        base_key = prefix.rsplit('.', 1)[0]
        metadata_key = f"{base_key}_meta.json"
        local_model = f"{local_dir}/model.json"
        local_meta = f"{local_dir}/meta.json"

        logger.info(
            f"Loading WR model from s3://{bucket}/"
            f"{model_key}"
        )
        s3_client.download_file(
            bucket, model_key, local_model
        )
        try:
            s3_client.download_file(
                bucket, metadata_key, local_meta
            )
            with open(local_meta) as f:
                self.model_metadata = json.load(f)
        except Exception:
            logger.warning("No metadata file found, continuing without")
            self.model_metadata = {}

        self.model = xgb.Booster()
        self.model.load_model(local_model)

        logger.info(
            f"WR model loaded: "
            f"{self.model_version.version_name}"
        )

    # ═══════════════════════════════════════
    # PUBLIC: Run predictions for today
    # ═══════════════════════════════════════

    def run_daily_predictions(
        self, race_date: date = None
    ) -> dict:
        """
        Run WR predictions for all qualifying races.
        Called by wr-inference Lambda at 12:30 ET.
        """
        if race_date is None:
            race_date = date.today()

        if self.model is None:
            self.load_model()

        race_repo = RaceRepository(self.conn)
        entry_repo = EntryRepository(self.conn)

        races = race_repo.get_qualifying_races_by_date(
            race_date
        )

        if not races:
            logger.info(
                f"WR: no qualifying races for {race_date}"
            )
            return {
                'model': 'wr',
                'date': str(race_date),
                'races_processed': 0,
                'predictions_stored': 0
            }

        logger.info(
            f"WR: running predictions for {race_date}: "
            f"{len(races)} races"
        )

        races_processed = 0
        predictions_stored = 0
        errors = []

        for race in races:
            try:
                with self.conn.cursor() as cur:
                    cur.execute("SAVEPOINT wr_race_sp")

                # REPAIR-4: AS-OF predicate enforced
                race.entries = (
                    entry_repo.get_entries_by_race(
                        race.race_id,
                        as_of_date=race.race_date,
                    )
                )

                if len(race.entries) < 4:
                    continue

                predictions = self.predict_race(race)
                predictions = self.rank_field(predictions)
                predictions = self.flag_value(predictions)
                predictions = self.recommend_exotic_bets(
                    predictions
                )

                for pred in predictions:
                    self._store_prediction(pred)
                    predictions_stored += 1

                with self.conn.cursor() as cur:
                    cur.execute(
                        "RELEASE SAVEPOINT wr_race_sp"
                    )

                races_processed += 1
                logger.info(
                    f"WR race {race.race_number}: "
                    f"{len(predictions)} predictions stored"
                )

            except Exception as e:
                err = f"WR race {race.race_id} failed: {e}"
                errors.append(err)
                logger.error(err, exc_info=True)
                try:
                    with self.conn.cursor() as cur:
                        cur.execute(
                            "ROLLBACK TO SAVEPOINT wr_race_sp"
                        )
                except Exception:
                    pass

        return {
            'model': 'wr',
            'date': str(race_date),
            'races_processed': races_processed,
            'predictions_stored': predictions_stored,
            'errors': errors
        }

    # ═══════════════════════════════════════
    # PUBLIC: Predict single race
    # ═══════════════════════════════════════

    def predict_race(
        self, race: Race
    ) -> list[Prediction]:
        """
        Dual-model prediction for all entries.
        Per horse: use _full (66 feat) if workout data exists,
        else _core (58 feat).
        """
        if self.wp_core_model is None:
            raise RuntimeError(
                "Models not loaded. Call load_model() first."
            )

        # Build feature matrix with ALL features (66 base + 14 Gonzo = 80).
        # par_dict only populated for style='gonzo_sauce'; empty dict for
        # other styles means A3/A4 default to False/0.
        feature_df = self.fe_service.build_feature_matrix(
            race, include_odds=True, par_dict=self.par_dict
        )

        if feature_df.empty:
            logger.warning(
                f"WR: empty feature matrix for "
                f"race {race.race_id}"
            )
            return []

        # Phase A3: select feature set per style. gonzo_sauce uses the
        # 67-feature lean53+14 set; all other styles use lean53 (53).
        if self.style == 'gonzo_sauce':
            full_feats = GONZO_FULL_FEATURES
            ranker_feats = GONZO_FULL_FEATURES
        else:
            full_feats = FULL_FEATURES
            ranker_feats = RANKER_FULL_FEATURES

        # Ensure all feature columns exist
        for col in full_feats:
            if col not in feature_df.columns:
                feature_df[col] = 0.0

        # Check which horses have workout data
        has_workout = (
            (feature_df['workout_count_30d'] > 0) |
            (feature_df['days_since_last_workout'] != 30.0)
        ).values

        # Predict with appropriate model per horse
        raw_probs = np.zeros(len(feature_df))
        rank_scores = np.zeros(len(feature_df))
        model_used = ['core'] * len(feature_df)

        for idx in range(len(feature_df)):
            row_features = feature_df.iloc[[idx]]
            if has_workout[idx] and self.wp_full_model is not None:
                # wp_full feature set per style (lean53=53; gonzo_sauce=67)
                X = row_features[full_feats].fillna(0.0)
                dm = xgb.DMatrix(X.values, feature_names=full_feats)
                raw_probs[idx] = float(self.wp_full_model.predict(dm)[0])
                if self.rk_full_model:
                    X_rk = row_features[ranker_feats].fillna(0.0)
                    dm_rk = xgb.DMatrix(X_rk.values, feature_names=ranker_feats)
                    rank_scores[idx] = float(self.rk_full_model.predict(dm_rk)[0])
                elif self.rk_core_model:
                    X_core = row_features[CORE_FEATURES].fillna(0.0)
                    dm_rk = xgb.DMatrix(X_core.values, feature_names=CORE_FEATURES)
                    rank_scores[idx] = float(self.rk_core_model.predict(dm_rk)[0])
                model_used[idx] = 'full'
            else:
                # Use core model. Feature set + calibration switch with the
                # loaded artifact (lean53 → 47 features + isotonic calibration;
                # legacy → 58 features, no calibration).
                core_feats = self.wp_core_features
                X = row_features[core_feats].fillna(0.0)
                dm = xgb.DMatrix(X.values, feature_names=core_feats)
                raw_probs[idx] = float(self.wp_core_model.predict(dm)[0])
                if self.rk_core_model:
                    # rk_core remains 58-feature legacy
                    X_rk = row_features[CORE_FEATURES].fillna(0.0)
                    dm_rk = xgb.DMatrix(X_rk.values, feature_names=CORE_FEATURES)
                    rank_scores[idx] = float(self.rk_core_model.predict(dm_rk)[0])

        # ─── Ranker-as-probability architecture (post-2026-05-01 fix) ─────
        # The wp_* models are binary classifiers: per-horse independent
        # outputs that don't sum to 1.0 within a race. Using their output
        # for display ranking produced incoherent probabilities (sums
        # >>1.0 and "all-zeros feature horses" mapping to ~29% via
        # calibration → those horses topping the rankings).
        #
        # The rk_* models are XGBoost rankers with a rank:* objective —
        # their per-horse scores are only meaningful in within-race
        # comparison. Softmax over the rank_scores produces a proper
        # within-race probability distribution that sums to 1.0 by
        # construction.
        #
        # Architecture:
        #   rank_scores  → softmax → ranker_probs (within-race, sums to 1)
        #   ranker_probs → 0-PP override (base rate for no-data horses)
        #   ranker_probs → calibration → handicapping_probs
        #   handicapping_probs → final renormalize → win_probs
        # The wp_* classifier output is preserved as raw_win_prob (already
        # populated below) for backtesting / diagnostic only.
        field_size = len(feature_df)
        shifted = rank_scores - rank_scores.max()
        exp_scores = np.exp(shifted)
        ranker_probs = exp_scores / exp_scores.sum() if exp_scores.sum() > 0 else \
                       np.ones(field_size) / field_size

        # ── Patch (β): pp_counts query — used post-calibration below ──────
        # REPAIR-4: AS-OF predicate prevents pp_count substrate-leakage
        horse_ids_str = [str(feature_df.iloc[idx].get('horse_id', '')) for idx in range(field_size)]
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT horse_id::text AS hid, COUNT(*) AS n "
                "FROM past_performances WHERE horse_id::text = ANY(%s) "
                "  AND race_date < %s "
                "GROUP BY horse_id",
                (horse_ids_str, race.race_date),
            )
            pp_counts = {r['hid']: r['n'] for r in cur.fetchall()}

        # ── Calibration BYPASS (BUG #15 + BUG #24) ────────────────────────
        # All styles (including gonzo_sauce) bypass calibration at inference
        # tonight. Original Phase A3 plan was to apply gonzo's fitted
        # ranker calibration here, but that surfaced Bug #24: isotonic
        # mapping of legitimate-PP horses' ranker_probs (≈ base_rate) to
        # near-zero, then 0-PP override at 1/field_size dominates after
        # renormalize → 0-PP horses become top picks (Wonder Dean JPN at #1
        # in Derby smoke test). Gonzo joins the legacy bypass until the
        # Phase A3.5 fix splits 0-PP horses out of the calibration path
        # entirely. Calibration sidecar remains in S3 for A3.5 use.
        handicapping_probs = ranker_probs.copy()

        # ── Patch (β): 0-PP override AFTER calibration ────────────────────
        # Pre-calibration override produced different post-calibration values
        # for 0-PP horses depending on model_used (full vs core dispatch).
        # Setting AFTER calibration bypasses that and gives uniform base_rate
        # regardless of which model path. Final renormalize below handles the
        # resulting sum != 1.0.
        for idx in range(field_size):
            if pp_counts.get(horse_ids_str[idx], 0) == 0:
                handicapping_probs[idx] = 1.0 / field_size

        # ── Patch (γ): final post-calibration renormalization ──
        hc_sum = handicapping_probs.sum()
        if hc_sum > 0:
            handicapping_probs = handicapping_probs / hc_sum

        # ── Market-prob within-race normalization ──
        # ML-odds-implied probabilities sum to >1 due to overround. Normalize
        # so edge_pct = handicapping_prob - market_prob stays coherent.
        market_probs_raw = np.zeros(field_size)
        for idx in range(field_size):
            entry = self._find_entry(race, str(feature_df.iloc[idx].get('horse_id', '')))
            if entry and entry.morning_line_odds and entry.morning_line_odds > 0:
                market_probs_raw[idx] = 1.0 / (float(entry.morning_line_odds) + 1.0)
        mp_sum = market_probs_raw.sum()
        market_probs_arr = market_probs_raw / mp_sum if mp_sum > 0 else market_probs_raw

        win_probs = handicapping_probs  # default; per-row blend below overrides

        predictions = []
        w = HANDICAPPING_BLEND_WEIGHT
        for i, row in feature_df.iterrows():
            idx = list(feature_df.index).index(i)
            entry = self._find_entry(
                race, str(row.get('horse_id', ''))
            )
            if not entry:
                continue

            handicapping_prob = float(handicapping_probs[idx])

            # Dual-prediction: market_prob is now within-race-normalized
            # (computed pre-loop), so edge_pct is coherent.
            ml_odds = entry.morning_line_odds
            if ml_odds is not None and ml_odds > 0:
                market_prob = float(market_probs_arr[idx])
                edge_pct = handicapping_prob - market_prob
                displayed_prob = (
                    w * handicapping_prob + (1.0 - w) * market_prob
                )
            else:
                market_prob = None
                edge_pct = None
                displayed_prob = handicapping_prob

            # Kelly bet sizing uses calibrated handicapping_prob (not raw)
            value = compute_value_overlay(
                handicapping_prob,
                float(ml_odds) if ml_odds else 0.0
            )

            # place/show derived from displayed_prob
            top2_prob = float(np.sum(np.sort(handicapping_probs)[-2:]))
            place_prob = min(displayed_prob * 2.5, top2_prob)
            show_prob = min(displayed_prob * 3.5, 0.95)

            pred = Prediction(
                prediction_id=None,
                entry=entry,
                race_id=race.race_id,
                horse_id=entry.horse.horse_id,
                model_version_id=(
                    self.model_version.model_version_id
                    if self.model_version else None
                ),
                win_probability=round(displayed_prob, 4),
                place_probability=round(place_prob, 4),
                show_probability=round(show_prob, 4),
                predicted_rank=None,
                confidence_score=round(float(raw_probs[idx]), 4),
                is_top_pick=False,
                is_value_flag=value['is_value'],
                morning_line_implied_prob=(
                    round(market_prob, 4) if market_prob is not None else None
                ),
                overlay_pct=(
                    round(edge_pct, 4) if edge_pct is not None else None
                ),
                feature_importance={},
            )
            # Attach extra fields for storage
            pred.raw_win_prob = round(float(raw_probs[idx]), 4)
            pred.handicapping_prob = round(handicapping_prob, 4)
            pred.market_prob = (
                round(market_prob, 4) if market_prob is not None else None
            )
            pred.edge_pct = (
                round(edge_pct, 4) if edge_pct is not None else None
            )
            pred.rank_score = round(float(rank_scores[idx]), 4)
            pred.kelly_fraction = value['kelly_fraction']
            pred.kelly_bet = value['kelly_bet']
            pred.has_workout_data = bool(has_workout[idx])
            pred.model_used = model_used[idx]
            predictions.append(pred)

        return predictions

    # ═══════════════════════════════════════
    # PUBLIC: Rank, flag value, exotic bets
    # ═══════════════════════════════════════

    def rank_field(
        self, predictions: list[Prediction]
    ) -> list[Prediction]:
        """Sort by win_probability, assign ranks."""
        if not predictions:
            return predictions
        sorted_preds = sorted(
            predictions,
            key=lambda p: p.win_probability or 0,
            reverse=True
        )
        for i, pred in enumerate(sorted_preds):
            pred.predicted_rank = i + 1
            pred.is_top_pick = (i == 0)
        return sorted_preds

    def flag_value(
        self, predictions: list[Prediction]
    ) -> list[Prediction]:
        """
        Re-evaluate value flag against the calibrated handicapping_prob.
        market_prob and edge_pct were already set in predict_race; this
        just (re-)applies the OVERLAY_THRESHOLD to the calibrated edge.
        Called AFTER rank_field — odds never influence ranking.
        """
        for pred in predictions:
            edge = getattr(pred, 'edge_pct', None)
            if edge is not None:
                pred.is_value_flag = (edge >= OVERLAY_THRESHOLD)
            else:
                pred.is_value_flag = False
        return predictions

    def recommend_exotic_bets(
        self, predictions: list[Prediction]
    ) -> list[Prediction]:
        """Recommend bet type based on probability spread."""
        if not predictions:
            return predictions

        sorted_preds = sorted(
            predictions,
            key=lambda p: p.win_probability or 0,
            reverse=True
        )

        if len(sorted_preds) < 2:
            for pred in predictions:
                pred.recommended_bet_type = 'skip'
            return predictions

        top_prob = sorted_preds[0].win_probability or 0
        second_prob = sorted_preds[1].win_probability or 0
        third_prob = (
            sorted_preds[2].win_probability or 0
            if len(sorted_preds) >= 3 else 0
        )
        gap_1_2 = top_prob - second_prob

        if top_prob < 0.15:
            bet_type = 'skip'
        elif top_prob >= 0.35 and gap_1_2 >= 0.10:
            bet_type = 'single'
        elif (top_prob >= 0.20 and
              second_prob >= 0.15 and
              third_prob >= 0.12):
            bet_type = 'trifecta_box'
        elif top_prob >= 0.20:
            bet_type = 'exacta_box'
        else:
            bet_type = 'skip'

        top_2_ids = [
            p.entry.entry_id for p in sorted_preds[:2]
        ]
        top_3_ids = [
            p.entry.entry_id for p in sorted_preds[:3]
        ]

        for pred in predictions:
            pred.recommended_bet_type = bet_type
            if bet_type == 'single':
                pred.exotic_partners = []
            elif bet_type == 'exacta_box':
                pred.exotic_partners = [
                    eid for eid in top_2_ids
                    if eid != pred.entry.entry_id
                ]
            elif bet_type == 'trifecta_box':
                pred.exotic_partners = [
                    eid for eid in top_3_ids
                    if eid != pred.entry.entry_id
                ]
            else:
                pred.exotic_partners = []

        return predictions

    # ═══════════════════════════════════════
    # PRIVATE: Helpers
    # ═══════════════════════════════════════

    def _find_entry(
        self, race: Race, horse_id: str
    ) -> Optional[Entry]:
        for entry in race.entries:
            if entry.horse.horse_id == horse_id:
                return entry
        return None

    def _store_prediction(
        self, pred: Prediction
    ) -> None:
        prediction_data = {
            'entry_id': pred.entry.entry_id,
            'race_id': pred.race_id,
            'horse_id': pred.horse_id,
            'model_version_id': pred.model_version_id,
            'win_probability': pred.win_probability,
            'place_probability': pred.place_probability,
            'show_probability': pred.show_probability,
            'predicted_rank': pred.predicted_rank,
            'confidence_score': pred.confidence_score,
            'is_top_pick': pred.is_top_pick,
            'is_value_flag': pred.is_value_flag,
            'morning_line_implied_prob': (
                pred.morning_line_implied_prob
            ),
            'overlay_pct': pred.overlay_pct,
            'feature_importance': (
                pred.feature_importance or {}
            ),
            'recommended_bet_type': (
                pred.recommended_bet_type
            ),
            'exotic_partners': (
                pred.exotic_partners or []
            ),
            'raw_win_prob': getattr(pred, 'raw_win_prob', None),
            'handicapping_prob': getattr(pred, 'handicapping_prob', None),
            'market_prob': getattr(pred, 'market_prob', None),
            'rank_score': getattr(pred, 'rank_score', None),
            'edge_pct': getattr(pred, 'edge_pct', None),
            'kelly_fraction': getattr(pred, 'kelly_fraction', None),
            'kelly_bet': getattr(pred, 'kelly_bet', None),
            'has_workout_data': getattr(pred, 'has_workout_data', False),
            'model_used': getattr(pred, 'model_used', 'core'),
            'style': self.style,
        }
        self.prediction_repo.insert_prediction(
            prediction_data
        )
