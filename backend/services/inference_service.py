import os
import json
import logging
import boto3
import numpy as np
import pandas as pd
import xgboost as xgb
from datetime import date, datetime
from typing import Optional
from models.canonical import (
    Race, Entry, Prediction
)
from repositories.prediction_repository import (
    PredictionRepository
)
from repositories.model_version_repository import (
    ModelVersionRepository
)
from repositories.race_repository import (
    RaceRepository
)
from repositories.entry_repository import (
    EntryRepository
)
from services.feature_engineering_service import (
    FeatureEngineeringService
)
from model.features.feature_definitions import (
    ALL_FEATURES, INDEX_COLUMNS
)
from shared.constants import OVERLAY_THRESHOLD

logger = logging.getLogger(__name__)


class InferenceService:
    """
    Loads trained XGBoost model and generates
    predictions for qualifying races.

    Pipeline per race:
    1. Build feature matrix (odds-blind)
    2. Run XGBoost inference -> raw scores
    3. Softmax scores -> win probabilities
    4. Rank horses within race
    5. Flag value plays (odds comparison
       happens HERE, post-inference only)
    6. Recommend exotic bets
    7. Persist predictions to database

    CRITICAL: Model sees NO odds data.
    Morning line comparison happens in
    flag_value() AFTER ranking is complete.
    Odds never influence which horses
    the model prefers.
    """

    def __init__(self, conn):
        self.conn = conn
        self.model = None
        self.model_version = None
        self.model_metadata = None
        self.fe_service = FeatureEngineeringService(
            conn
        )
        self.prediction_repo = PredictionRepository(
            conn
        )
        self.model_version_repo = (
            ModelVersionRepository(conn)
        )

    # ═══════════════════════════════════════
    # PUBLIC: Model loading
    # ═══════════════════════════════════════

    def load_model(
        self, version_name: str = None
    ) -> None:
        """
        Load model artifact from S3.

        If version_name is None, loads the active
        model from model_versions table.

        Downloads to /tmp for Lambda execution.
        Caches in self.model for reuse within
        a single Lambda invocation — Lambda
        containers are reused between warm calls,
        so this avoids re-downloading on every
        request.
        """
        # Get model version record from DB
        if version_name:
            self.model_version = (
                self.model_version_repo
                .get_model_by_version(version_name)
            )
        else:
            self.model_version = (
                self.model_version_repo
                .get_active_model()
            )

        if not self.model_version:
            raise ValueError(
                "No active model found in database. "
                "Train a model and set it active with "
                "python train.py --set-active"
            )

        s3_path = self.model_version.s3_artifact_path
        if not s3_path:
            raise ValueError(
                f"Model {self.model_version.version_name}"
                f" has no S3 artifact path"
            )

        # Parse S3 path
        # Format: s3://bucket/models/version/
        s3_path = s3_path.rstrip('/')
        if s3_path.startswith('s3://'):
            parts = s3_path[5:].split('/', 1)
            bucket = parts[0]
            prefix = parts[1] if len(parts) > 1 else ''
        else:
            raise ValueError(
                f"Invalid S3 path: {s3_path}"
            )

        # Download model files to /tmp
        local_dir = '/tmp/equine-model'
        os.makedirs(local_dir, exist_ok=True)

        s3_client = boto3.client('s3')

        model_key = f"{prefix}/model.xgb"
        metadata_key = (
            f"{prefix}/model_metadata.json"
        )
        local_model = f"{local_dir}/model.xgb"
        local_meta = (
            f"{local_dir}/model_metadata.json"
        )

        logger.info(
            f"Loading model from s3://{bucket}/"
            f"{model_key}"
        )
        s3_client.download_file(
            bucket, model_key, local_model
        )
        s3_client.download_file(
            bucket, metadata_key, local_meta
        )

        # Load model
        self.model = xgb.Booster()
        self.model.load_model(local_model)

        # Load metadata
        with open(local_meta) as f:
            self.model_metadata = json.load(f)

        logger.info(
            f"Model loaded: "
            f"{self.model_version.version_name}, "
            f"best iteration: "
            f"{self.model_metadata.get('best_iteration')}"
        )

    # ═══════════════════════════════════════
    # PUBLIC: Run predictions for today
    # ═══════════════════════════════════════

    def run_daily_predictions(
        self, race_date: date = None
    ) -> dict:
        """
        Run predictions for all qualifying races
        on a given date.

        Called by the inference Lambda at 7:30 AM ET.
        Loads model if not already loaded.
        Processes every qualifying race on the card.
        Persists all predictions to database.

        Returns summary dict.
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
                f"No qualifying races found for "
                f"{race_date}"
            )
            return {
                'date': str(race_date),
                'races_processed': 0,
                'predictions_stored': 0
            }

        logger.info(
            f"Running predictions for {race_date}: "
            f"{len(races)} qualifying races"
        )

        races_processed = 0
        predictions_stored = 0
        errors = []

        for race in races:
            try:
                # Load entries with PPs
                race.entries = (
                    entry_repo.get_entries_by_race(
                        race.race_id
                    )
                )

                if len(race.entries) < 4:
                    logger.debug(
                        f"Skipping race {race.race_number} "
                        f"— fewer than 4 entries"
                    )
                    continue

                predictions = self.predict_race(race)
                predictions = self.rank_field(predictions)
                predictions = self.flag_value(predictions)
                predictions = self.recommend_exotic_bets(
                    predictions
                )

                # Persist to database
                for pred in predictions:
                    self._store_prediction(pred)
                    predictions_stored += 1

                races_processed += 1
                logger.info(
                    f"Race {race.race_number} at "
                    f"{race.track.track_code}: "
                    f"{len(predictions)} predictions stored"
                )

            except Exception as e:
                err = (
                    f"Race {race.race_id} failed: {e}"
                )
                errors.append(err)
                logger.error(err, exc_info=True)

        summary = {
            'date': str(race_date),
            'races_processed': races_processed,
            'predictions_stored': predictions_stored,
            'errors': errors
        }

        logger.info(
            f"Daily predictions complete: "
            f"{races_processed} races, "
            f"{predictions_stored} predictions"
        )

        return summary

    # ═══════════════════════════════════════
    # PUBLIC: Predict single race
    # ═══════════════════════════════════════

    def predict_race(
        self, race: Race
    ) -> list[Prediction]:
        """
        Generate raw predictions for all entries
        in a race.

        Returns list of Prediction objects with
        win/place/show probabilities set.
        NOT yet ranked or value-flagged.
        """
        if self.model is None:
            raise RuntimeError(
                "Model not loaded. Call load_model() first."
            )

        # Build feature matrix (odds-blind)
        feature_df = self.fe_service \
            .build_feature_matrix(race)

        if feature_df.empty:
            logger.warning(
                f"Empty feature matrix for race "
                f"{race.race_id}"
            )
            return []

        # Ensure correct feature order
        for col in ALL_FEATURES:
            if col not in feature_df.columns:
                feature_df[col] = 0.0

        X = feature_df[ALL_FEATURES].fillna(0.0)
        dmatrix = xgb.DMatrix(
            X.values,
            feature_names=ALL_FEATURES
        )

        # Run inference
        raw_scores = self.model.predict(dmatrix)

        # Convert to probabilities via softmax
        # Softmax within race so probabilities
        # sum to 1.0 across the field
        exp_scores = np.exp(
            raw_scores - raw_scores.max()
        )
        win_probs = exp_scores / exp_scores.sum()

        # Build Prediction objects
        predictions = []
        for i, row in feature_df.iterrows():
            idx = list(feature_df.index).index(i)

            # Find matching entry
            entry = self._find_entry(
                race, str(row.get('horse_id', ''))
            )
            if not entry:
                continue

            # Place probability:
            # approximated as top-2 share
            top2_prob = float(
                np.sum(np.sort(win_probs)[-2:])
            )
            place_prob = min(
                float(win_probs[idx]) * 2.5,
                top2_prob
            )
            show_prob = min(
                float(win_probs[idx]) * 3.5,
                0.95
            )

            pred = Prediction(
                prediction_id=None,
                entry=entry,
                race_id=race.race_id,
                horse_id=entry.horse.horse_id,
                model_version_id=(
                    self.model_version.model_version_id
                    if self.model_version else None
                ),
                win_probability=round(
                    float(win_probs[idx]), 4
                ),
                place_probability=round(place_prob, 4),
                show_probability=round(show_prob, 4),
                predicted_rank=None,
                confidence_score=round(
                    float(raw_scores[idx]), 4
                ),
                is_top_pick=False,
                is_value_flag=False,
                morning_line_implied_prob=None,
                overlay_pct=None,
                feature_importance={},
            )
            predictions.append(pred)

        return predictions

    # ═══════════════════════════════════════
    # PUBLIC: Rank field
    # ═══════════════════════════════════════

    def rank_field(
        self,
        predictions: list[Prediction]
    ) -> list[Prediction]:
        """
        Sort predictions by win_probability desc.
        Assign predicted_rank 1 through N.
        Set is_top_pick = true for rank 1 only.

        This is the model's final word on ordering.
        Odds have not been consulted.
        """
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

    # ═══════════════════════════════════════
    # PUBLIC: Flag value plays
    # ═══════════════════════════════════════

    def flag_value(
        self,
        predictions: list[Prediction]
    ) -> list[Prediction]:
        """
        Compare model win_probability to morning
        line implied probability.
        Flag overlays where model sees more value
        than the market implies.

        THIS IS THE ONLY PLACE ODDS ARE USED.
        Called AFTER rank_field().
        Odds never influenced the ranking.

        morning_line_implied_prob =
          1 / (morning_line_odds + 1)
          e.g. 5-1 morning line = 1/6 = 0.167

        overlay_pct =
          win_probability - implied_prob
        Positive = model likes horse MORE than market.

        is_value_flag = True when
          overlay_pct >= OVERLAY_THRESHOLD (0.15)
        """
        for pred in predictions:
            ml_odds = pred.entry.morning_line_odds
            if ml_odds is not None and ml_odds > 0:
                implied_prob = round(
                    1.0 / (ml_odds + 1.0), 4
                )
                overlay = round(
                    (pred.win_probability or 0) -
                    implied_prob, 4
                )
                pred.morning_line_implied_prob = (
                    implied_prob
                )
                pred.overlay_pct = overlay
                pred.is_value_flag = (
                    overlay >= OVERLAY_THRESHOLD
                )
            else:
                pred.morning_line_implied_prob = None
                pred.overlay_pct = None
                pred.is_value_flag = False

        return predictions

    # ═══════════════════════════════════════
    # PUBLIC: Recommend exotic bets
    # ═══════════════════════════════════════

    def recommend_exotic_bets(
        self,
        predictions: list[Prediction]
    ) -> list[Prediction]:
        """
        Set recommended_bet_type and exotic_partners
        for each prediction based on the probability
        distribution across the field.

        Logic:
        - SKIP: race has no clear top horse
          (top probability < 0.15 — very even field)

        - SINGLE: strong single bet
          top horse probability >= 0.35 AND
          gap to 2nd >= 0.10

        - EXACTA_BOX: box top 2-3 horses
          top probability 0.20-0.35 OR
          two horses clustered within 0.05

        - TRIFECTA_BOX: box top 3 horses
          when top 3 probabilities are each >= 0.12
          and no single horse dominates

        - PICK_LEG: this race is a strong single
          leg for a Pick 3/4

        exotic_partners: list of entry_ids
        to combine with in multi-horse bets
        """
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

        top_prob = (
            sorted_preds[0].win_probability or 0
        )
        second_prob = (
            sorted_preds[1].win_probability or 0
        )
        third_prob = (
            sorted_preds[2].win_probability or 0
            if len(sorted_preds) >= 3 else 0
        )

        gap_1_2 = top_prob - second_prob

        # Determine bet type
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

        # Set on all predictions in this race
        top_2_ids = [
            p.entry.entry_id
            for p in sorted_preds[:2]
        ]
        top_3_ids = [
            p.entry.entry_id
            for p in sorted_preds[:3]
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
    # PUBLIC: Multi-race exotic recommendations
    # ═══════════════════════════════════════

    def recommend_multi_race_exotics(
        self,
        race_predictions: list[list[Prediction]]
    ) -> dict:
        """
        Given predictions for multiple consecutive
        races, recommend Pick 3/4 combinations.

        A race qualifies as a strong Pick leg when:
        - bet_type is 'single' or 'exacta_box'
        - top horse win_probability >= 0.25

        Returns:
        {
          'pick3': [ { races, horses, confidence } ],
          'pick4': [ { races, horses, confidence } ],
          'daily_doubles': [ { races, horses, confidence } ]
        }
        """
        recommendations = {
            'pick3': [],
            'pick4': [],
            'daily_doubles': []
        }

        if not race_predictions:
            return recommendations

        # Find strong legs
        strong_legs = []
        for race_preds in race_predictions:
            if not race_preds:
                continue
            sorted_preds = sorted(
                race_preds,
                key=lambda p: p.win_probability or 0,
                reverse=True
            )
            top = sorted_preds[0]
            if (top.win_probability or 0) >= 0.25:
                horses = [sorted_preds[0].entry.entry_id]
                if (len(sorted_preds) > 1 and
                        (sorted_preds[1].win_probability or 0)
                        >= 0.15):
                    horses.append(
                        sorted_preds[1].entry.entry_id
                    )
                strong_legs.append({
                    'race_id': top.race_id,
                    'horses': horses,
                    'confidence': top.win_probability or 0
                })

        # Daily doubles: consecutive strong legs
        for i in range(len(strong_legs) - 1):
            leg1 = strong_legs[i]
            leg2 = strong_legs[i + 1]
            confidence = (
                leg1['confidence'] * leg2['confidence']
            )
            recommendations['daily_doubles'].append({
                'races': [
                    leg1['race_id'],
                    leg2['race_id']
                ],
                'horses': {
                    leg1['race_id']: leg1['horses'],
                    leg2['race_id']: leg2['horses'],
                },
                'confidence': round(confidence, 4),
                'combinations': (
                    len(leg1['horses']) *
                    len(leg2['horses'])
                )
            })

        # Pick 3: three consecutive strong legs
        for i in range(len(strong_legs) - 2):
            legs = strong_legs[i:i + 3]
            confidence = 1.0
            for leg in legs:
                confidence *= leg['confidence']
            recommendations['pick3'].append({
                'races': [l['race_id'] for l in legs],
                'horses': {
                    l['race_id']: l['horses']
                    for l in legs
                },
                'confidence': round(confidence, 4),
                'combinations': (
                    len(legs[0]['horses']) *
                    len(legs[1]['horses']) *
                    len(legs[2]['horses'])
                )
            })

        # Pick 4: four consecutive strong legs
        for i in range(len(strong_legs) - 3):
            legs = strong_legs[i:i + 4]
            confidence = 1.0
            for leg in legs:
                confidence *= leg['confidence']
            recommendations['pick4'].append({
                'races': [l['race_id'] for l in legs],
                'horses': {
                    l['race_id']: l['horses']
                    for l in legs
                },
                'confidence': round(confidence, 4),
                'combinations': (
                    len(legs[0]['horses']) *
                    len(legs[1]['horses']) *
                    len(legs[2]['horses']) *
                    len(legs[3]['horses'])
                )
            })

        return recommendations

    # ═══════════════════════════════════════
    # PRIVATE: Helpers
    # ═══════════════════════════════════════

    def _find_entry(
        self,
        race: Race,
        horse_id: str
    ) -> Optional[Entry]:
        """Find entry in race by horse_id."""
        for entry in race.entries:
            if entry.horse.horse_id == horse_id:
                return entry
        return None

    def _store_prediction(
        self, pred: Prediction
    ) -> None:
        """Persist prediction to database."""
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
        }
        self.prediction_repo.insert_prediction(
            prediction_data
        )

    def _get_feature_importance_for_entry(
        self,
        feature_df: pd.DataFrame,
        row_idx: int
    ) -> dict:
        """
        Get per-prediction feature importance
        using XGBoost SHAP values.

        SHAP explains WHY the model ranked this horse
        where it did for THIS specific prediction.

        Returns top 10 features by absolute
        SHAP value for display in UI.

        Called optionally — SHAP is slow,
        only use for top picks and value plays.
        """
        if self.model is None:
            return {}
        try:
            X = feature_df[ALL_FEATURES].fillna(0.0)
            dmatrix = xgb.DMatrix(
                X.values,
                feature_names=ALL_FEATURES
            )
            shap_values = self.model.predict(
                dmatrix,
                pred_contribs=True
            )
            row_shap = shap_values[row_idx][:-1]

            importance = {
                ALL_FEATURES[i]: round(float(v), 4)
                for i, v in enumerate(row_shap)
            }
            top10 = dict(
                sorted(
                    importance.items(),
                    key=lambda x: abs(x[1]),
                    reverse=True
                )[:10]
            )
            return top10
        except Exception as e:
            logger.warning(
                f"SHAP computation failed: {e}"
            )
            return {}
