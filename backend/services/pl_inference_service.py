import os
import json
import logging
import boto3
import numpy as np
import pandas as pd
import xgboost as xgb
from datetime import date
from typing import Optional
from models.canonical import Race, Entry, PLPrediction
from repositories.pl_prediction_repository import (
    PLPredictionRepository
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
    get_core_features,
    get_lean53_core_features,
)
from shared.constants import (
    BANKROLL, KELLY_FRACTION, MAX_BET_PCT,
    MIN_EDGE_TO_BET, STRONG_VALUE_THRESHOLD,
    HANDICAPPING_BLEND_WEIGHT,
)

logger = logging.getLogger(__name__)

SOFTMAX_TEMPERATURE = 1.0
PL_FEATURES = get_lean53_core_features()   # 47 features — lean53 pl_core
LEGACY_PL_FEATURES = get_core_features(include_odds=True)  # 58 — fallback


class PLInferenceService:
    """
    P&L (Profit & Loss) inference pipeline — odds-aware.

    Uses 66 features (includes odds data).
    Loads model of type 'pl' via get_active_model_by_type.
    Stores predictions to pl_predictions table.
    Computes Kelly sizing and edge detection.
    No exotic bet recommendations (pure EV maximization).
    Completely independent from WR and LS pipelines.

    Pipeline per race:
    1. Build feature matrix (include_odds=True, 66 feats)
    2. XGBoost inference -> raw scores
    3. Temperature-scaled softmax -> win probabilities
    4. Rank horses within race
    5. Compute EV, edge, Kelly sizing from closing odds
    6. Flag value bets where edge >= MIN_EDGE_TO_BET
    7. Persist to pl_predictions
    """

    VALID_STYLES = (
        'general', 'speed', 'closer', 'class_riser',
        'class_dropper', 'sprint', 'route',
    )

    def __init__(self, conn, style: str = 'general'):
        if style not in self.VALID_STYLES:
            raise ValueError(
                f"Invalid style {style!r}. Valid: {self.VALID_STYLES}"
            )
        self.style = style
        self.conn = conn
        self.model = None
        self.model_version = None
        self.model_metadata = None
        # Calibration sidecar (lean53). Tuple (x_thresholds, y_thresholds) or None.
        self.calibration = None
        self.fe_service = FeatureEngineeringService(conn)
        self.prediction_repo = PLPredictionRepository(conn)
        self.model_version_repo = ModelVersionRepository(
            conn
        )

    # ═══════════════════════════════════════
    # PUBLIC: Model loading
    # ═══════════════════════════════════════

    def load_model(self) -> None:
        """
        Load active P&L model for the current style.
        V1 uses Layer 1 only (pl_core_{style}); pl_workout artifacts
        exist in S3 + model_versions but are not loaded at inference.
        """
        model_type = f'pl_core_{self.style}'
        self.model_version = (
            self.model_version_repo
            .get_active_model_by_type(model_type)
        )

        if not self.model_version:
            raise ValueError(
                f"No active P&L model found for style={self.style!r} "
                f"(model_type={model_type!r}). Train and activate."
            )

        s3_path = self.model_version.s3_artifact_path
        if not s3_path:
            raise ValueError(
                f"PL model {self.model_version.version_name}"
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

        local_dir = '/tmp/pl-model'
        os.makedirs(local_dir, exist_ok=True)

        s3_client = boto3.client('s3')

        # New artifact format: s3_path points directly
        # to the model JSON file (e.g. pl/pl_core_20260320.json)
        model_key = prefix
        base_key = prefix.rsplit('.', 1)[0]
        metadata_key = f"{base_key}_meta.json"
        local_model = f"{local_dir}/model.json"
        local_meta = f"{local_dir}/meta.json"

        logger.info(
            f"Loading P&L model from s3://{bucket}/"
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
            f"P&L model loaded: "
            f"{self.model_version.version_name}"
        )

        # Try to load calibration sidecar
        cal_key = f"{base_key}_calibration.json"
        local_cal = f"{local_dir}/calibration.json"
        try:
            s3_client.download_file(bucket, cal_key, local_cal)
            with open(local_cal) as f:
                cal = json.load(f)
            self.calibration = (
                np.array(cal['x_thresholds'], dtype=float),
                np.array(cal['y_thresholds'], dtype=float),
            )
            logger.info(
                f"P&L calibration loaded "
                f"({len(self.calibration[0])} thresholds)"
            )
        except Exception as e:
            logger.warning(
                f"No PL calibration sidecar for "
                f"{self.model_version.version_name}: {e}"
            )
            self.calibration = None

    @staticmethod
    def _apply_calibration(raw, calibration):
        """Apply isotonic calibration via piecewise-linear interpolation."""
        if calibration is None:
            return raw
        xt, yt = calibration
        return np.clip(np.interp(raw, xt, yt), 0.0, 1.0)

    # ═══════════════════════════════════════
    # PUBLIC: Run predictions for today
    # ═══════════════════════════════════════

    def run_daily_predictions(
        self, race_date: date = None
    ) -> dict:
        """
        Run P&L predictions for all qualifying races.
        Called by pl-inference Lambda at 12:35 ET.
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
                f"PL: no qualifying races for {race_date}"
            )
            return {
                'model': 'pl',
                'date': str(race_date),
                'races_processed': 0,
                'predictions_stored': 0
            }

        logger.info(
            f"PL: running predictions for {race_date}: "
            f"{len(races)} races"
        )

        races_processed = 0
        predictions_stored = 0
        errors = []

        for race in races:
            try:
                with self.conn.cursor() as cur:
                    cur.execute("SAVEPOINT pl_race_sp")

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
                # Compute EV/Kelly FIRST so rank_field can sort by predicted_ev
                # (PL ranks by expected value, not raw win probability).
                predictions = self.compute_ev_and_kelly(
                    predictions
                )
                predictions = self.rank_field(predictions)

                for pred in predictions:
                    self._store_prediction(pred)
                    predictions_stored += 1

                with self.conn.cursor() as cur:
                    cur.execute(
                        "RELEASE SAVEPOINT pl_race_sp"
                    )

                races_processed += 1
                logger.info(
                    f"PL race {race.race_number}: "
                    f"{len(predictions)} predictions stored"
                )

            except Exception as e:
                err = f"PL race {race.race_id} failed: {e}"
                errors.append(err)
                logger.error(err, exc_info=True)
                try:
                    with self.conn.cursor() as cur:
                        cur.execute(
                            "ROLLBACK TO SAVEPOINT pl_race_sp"
                        )
                except Exception:
                    pass

        return {
            'model': 'pl',
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
    ) -> list[PLPrediction]:
        """
        Generate P&L predictions for all entries.
        Odds-aware: include_odds=True, 66 features.
        """
        if self.model is None:
            raise RuntimeError(
                "P&L model not loaded. "
                "Call load_model() first."
            )

        feature_df = self.fe_service.build_feature_matrix(
            race, include_odds=True
        )

        if feature_df.empty:
            logger.warning(
                f"PL: empty feature matrix for "
                f"race {race.race_id}"
            )
            return []

        for col in PL_FEATURES:
            if col not in feature_df.columns:
                feature_df[col] = 0.0

        X = feature_df[PL_FEATURES].fillna(0.0)
        dmatrix = xgb.DMatrix(
            X.values,
            feature_names=PL_FEATURES
        )

        raw_scores = self.model.predict(dmatrix)

        scaled = (
            (raw_scores - raw_scores.max())
            / SOFTMAX_TEMPERATURE
        )
        scaled = np.clip(scaled, -20, 0)
        exp_scores = np.exp(scaled)
        softmax_probs = exp_scores / exp_scores.sum()

        # Apply isotonic calibration AFTER softmax (calibration was fit
        # on post-softmax probs; raw EV scores are not probabilities).
        handicapping_probs = self._apply_calibration(
            softmax_probs, self.calibration
        )

        # ── Patch (β): 0-PP-horse override ────────────────────────────────
        # Horses with no past_performances data feed all-zero feature vectors
        # to the model, which then map to a default ~0.X via calibration —
        # often putting no-data horses ABOVE horses with real data. Override
        # them to the field base rate (1/field_size) so they don't dominate.
        field_size = len(feature_df)
        horse_ids = [str(feature_df.iloc[idx].get('horse_id', '')) for idx in range(field_size)]
        # REPAIR-4: AS-OF predicate prevents pp_count substrate-leakage
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT horse_id::text AS hid, COUNT(*) AS n "
                "FROM past_performances WHERE horse_id::text = ANY(%s) "
                "  AND race_date < %s "
                "GROUP BY horse_id",
                (horse_ids, race.race_date),
            )
            pp_counts = {r['hid']: r['n'] for r in cur.fetchall()}
        for idx in range(field_size):
            if pp_counts.get(horse_ids[idx], 0) == 0:
                handicapping_probs[idx] = 1.0 / field_size

        # ── Patch (γ): post-calibration within-race renormalization ──────
        # Isotonic calibration is non-linear so post-calibration probabilities
        # may not sum to 1.0 even though pre-calibration softmax did. Rescale.
        hc_sum = handicapping_probs.sum()
        if hc_sum > 0:
            handicapping_probs = handicapping_probs / hc_sum

        win_probs = handicapping_probs  # default; per-row blend below overrides

        shap_map = {}
        try:
            shap_values = self.model.predict(
                dmatrix, pred_contribs=True
            )
            for s_idx in range(len(shap_values)):
                row_shap = shap_values[s_idx][:-1]
                importance = {
                    PL_FEATURES[fi]: round(float(v), 4)
                    for fi, v in enumerate(row_shap)
                    if abs(v) > 0.001
                }
                top5 = dict(
                    sorted(
                        importance.items(),
                        key=lambda x: abs(x[1]),
                        reverse=True
                    )[:5]
                )
                shap_map[s_idx] = top5
        except Exception as shap_err:
            logger.warning(
                f"PL SHAP failed: {shap_err}"
            )

        # ── Market-prob within-race normalization ────────────────────────
        # ML-odds-implied probabilities (1/(ml+1)) sum to >1 due to bookmaker
        # overround. For edge_pct = handicapping_prob - market_prob to be
        # coherent with normalized handicapping_probs, market_probs must
        # also be normalized within-race.
        market_probs_raw = np.zeros(field_size)
        for idx in range(field_size):
            entry = self._find_entry(
                race, str(feature_df.iloc[idx].get('horse_id', ''))
            )
            if entry and entry.morning_line_odds and entry.morning_line_odds > 0:
                market_probs_raw[idx] = 1.0 / (float(entry.morning_line_odds) + 1.0)
        mp_sum = market_probs_raw.sum()
        market_probs = market_probs_raw / mp_sum if mp_sum > 0 else market_probs_raw

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

            # Dual-prediction (Stream A2 — see backend/shared/constants.py).
            # market_prob is now the within-race-normalized ML-implied prob,
            # so edge_pct is meaningful as "model's relative confidence vs market".
            ml_odds = entry.morning_line_odds
            if ml_odds is not None and ml_odds > 0:
                market_prob = float(market_probs[idx])
                edge_pct = handicapping_prob - market_prob
                displayed_prob = (
                    w * handicapping_prob + (1.0 - w) * market_prob
                )
            else:
                market_prob = None
                edge_pct = None
                displayed_prob = handicapping_prob

            pred = PLPrediction(
                prediction_id=None,
                entry=entry,
                race_id=race.race_id,
                horse_id=entry.horse.horse_id,
                model_version_id=(
                    self.model_version.model_version_id
                    if self.model_version else None
                ),
                win_probability=round(displayed_prob, 4),
                confidence_score=round(float(raw_scores[idx]), 4),
                predicted_rank=None,
                is_top_pick=False,
                feature_importance=shap_map.get(idx, {}),
            )
            # Attach extra fields for storage
            pred.handicapping_prob = round(handicapping_prob, 4)
            pred.market_prob = (
                round(market_prob, 4) if market_prob is not None else None
            )
            # edge_pct override happens in compute_ev_and_kelly below; record
            # the lean53 calibrated edge here too (it'll be overridden if
            # closing_odds-based logic decides to recompute).
            pred._lean53_edge_pct = (
                round(edge_pct, 4) if edge_pct is not None else None
            )
            predictions.append(pred)

        return predictions

    # ═══════════════════════════════════════
    # PUBLIC: Rank field
    # ═══════════════════════════════════════

    def rank_field(
        self, predictions: list[PLPrediction]
    ) -> list[PLPrediction]:
        """Sort by predicted_ev (expected return per $1 bet), assign ranks.
        Horses with positive EV float to top, negative-EV chalk falls to
        bottom. predicted_rank reflects PL's stated purpose (find
        profitable bets), not generic win probability. Must be called
        AFTER compute_ev_and_kelly so predicted_ev exists."""
        if not predictions:
            return predictions
        sorted_preds = sorted(
            predictions,
            key=lambda p: (
                p.predicted_ev if p.predicted_ev is not None
                else -float('inf')
            ),
            reverse=True,
        )
        for i, pred in enumerate(sorted_preds):
            pred.predicted_rank = i + 1
            pred.is_top_pick = (i == 0)
        return sorted_preds

    # ═══════════════════════════════════════
    # PUBLIC: EV and Kelly sizing
    # ═══════════════════════════════════════

    def compute_ev_and_kelly(
        self, predictions: list[PLPrediction]
    ) -> list[PLPrediction]:
        """
        Compute expected value and Kelly bet sizing.

        For each horse:
          implied_prob = 1 / (closing_odds + 1)
          edge = win_probability - implied_prob
          ev = win_probability * closing_odds - (1 - win_probability)
          kelly = (edge / closing_odds) * KELLY_FRACTION
          kelly_bet = min(kelly * BANKROLL, MAX_BET_PCT * BANKROLL)

        is_value_bet  = edge >= MIN_EDGE_TO_BET
        is_strong_value = edge >= STRONG_VALUE_THRESHOLD

        Uses morning_line_odds as closing_odds proxy until
        actual closing lines are available.
        """
        for pred in predictions:
            ml_odds = pred.entry.morning_line_odds
            # EV / Kelly are computed against handicapping_prob (the
            # calibrated, market-blind model output), not against
            # win_probability (which may be a blend of handicap + market).
            handicap = getattr(pred, 'handicapping_prob', None)
            if handicap is None:
                # Fallback for unmigrated callers
                handicap = pred.win_probability or 0.0
            if ml_odds is not None and ml_odds > 0:
                closing_odds = float(ml_odds)
                implied_prob = round(1.0 / (closing_odds + 1.0), 4)
                edge = round(handicap - implied_prob, 4)
                ev = round(
                    handicap * closing_odds - (1.0 - handicap), 4
                )

                if edge >= MIN_EDGE_TO_BET and closing_odds > 0:
                    raw_kelly = (edge / closing_odds) * KELLY_FRACTION
                    kelly_bet = min(
                        raw_kelly * BANKROLL,
                        MAX_BET_PCT * BANKROLL
                    )
                    kelly_fraction = round(raw_kelly, 4)
                    kelly_bet_size = round(max(kelly_bet, 0.0), 2)
                else:
                    kelly_fraction = 0.0
                    kelly_bet_size = 0.0

                pred.closing_odds = closing_odds
                pred.implied_probability = implied_prob
                pred.edge_pct = edge
                pred.predicted_ev = ev
                pred.kelly_fraction = kelly_fraction
                pred.kelly_bet_size = kelly_bet_size
                pred.is_value_bet = (edge >= MIN_EDGE_TO_BET)
                pred.is_strong_value = (
                    edge >= STRONG_VALUE_THRESHOLD
                )
            else:
                pred.closing_odds = None
                pred.implied_probability = None
                pred.edge_pct = None
                pred.predicted_ev = None
                pred.kelly_fraction = None
                pred.kelly_bet_size = None
                pred.is_value_bet = False
                pred.is_strong_value = False

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
        self, pred: PLPrediction
    ) -> None:
        prediction_data = {
            'entry_id': pred.entry.entry_id,
            'race_id': pred.race_id,
            'horse_id': pred.horse_id,
            'model_version_id': pred.model_version_id,
            'win_probability': pred.win_probability,
            'predicted_ev': pred.predicted_ev,
            'confidence_score': pred.confidence_score,
            'predicted_rank': pred.predicted_rank,
            'is_top_pick': pred.is_top_pick,
            'closing_odds': pred.closing_odds,
            'implied_probability': pred.implied_probability,
            'edge_pct': pred.edge_pct,
            'is_value_bet': pred.is_value_bet,
            'is_strong_value': pred.is_strong_value,
            'kelly_fraction': pred.kelly_fraction,
            'kelly_bet_size': pred.kelly_bet_size,
            'feature_importance': (
                pred.feature_importance or {}
            ),
            'handicapping_prob': getattr(pred, 'handicapping_prob', None),
            'market_prob': getattr(pred, 'market_prob', None),
            'style': self.style,
        }
        self.prediction_repo.insert_prediction(
            prediction_data
        )
