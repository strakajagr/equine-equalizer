"""
LS Inference Service — Second-Pass Enrichment (Layers 4-7)

Reads existing wr_predictions from the 7:30 AM pass (L1+L2+L3),
enriches each horse with:
  - Layer 4: RF longshot probability
  - Layer 5: LSTM form trajectory
  - Layer 6: Bayesian angle scoring
  - Layer 7: Ensemble final probability

Updates wr_predictions rows in place.
"""

import os
import json
import logging
import pickle
from datetime import date, timedelta

import boto3
import numpy as np
import pandas as pd
import xgboost as xgb
import torch
from sklearn.preprocessing import MinMaxScaler

from shared.db import get_db, execute_query, execute_one
from repositories.model_version_repository import (
    ModelVersionRepository
)

logger = logging.getLogger(__name__)

# LSTM config (must match training)
SEQUENCE_LENGTH = 5
MIN_SEQUENCE_LENGTH = 3
FEATURES_PER_STEP = 8


class TrajectoryLSTM(torch.nn.Module):
    """Must match model/trajectory/train.py architecture exactly."""
    def __init__(self, input_size=8, hidden_size=32, num_layers=2, dropout=0.3):
        super().__init__()
        self.lstm = torch.nn.LSTM(
            input_size=input_size, hidden_size=hidden_size,
            num_layers=num_layers, dropout=dropout, batch_first=True
        )
        self.fc = torch.nn.Linear(hidden_size, 1)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_hidden = lstm_out[:, -1, :]
        return self.fc(last_hidden).squeeze(-1)

    def predict_proba(self, x):
        with torch.no_grad():
            return torch.sigmoid(self.forward(x))


class LSInferenceService:
    """Second-pass enrichment: Layers 4-7 update wr_predictions."""

    def __init__(self, conn):
        self.conn = conn
        self.model_version_repo = ModelVersionRepository(conn)
        self.rf_model = None
        self.lstm_model = None
        self.lstm_scaler = None
        self.ensemble_model = None
        # Phase B Tier 1 Decision 1: substrate-correct longshot_rf path
        # FE service lazy-init for per-race 58-feat substrate construction
        self._fe_service = None
        self._race_repo = None
        self._entry_repo = None
        self._race_feature_cache: dict = {}  # race_id → per-horse feature_df

    def load_model(self) -> bool:
        """Load all longshot stack models."""
        s3 = boto3.client('s3', region_name='us-east-1')
        loaded = []

        # Layer 4: RF Longshot
        rf_path = self._get_model_path('longshot_rf')
        if rf_path:
            try:
                local = '/tmp/ls-rf/model.pkl'
                os.makedirs('/tmp/ls-rf', exist_ok=True)
                parts = rf_path[5:].split('/', 1)
                s3.download_file(parts[0], parts[1], local)
                with open(local, 'rb') as f:
                    self.rf_model = pickle.load(f)
                loaded.append('rf')
            except Exception as e:
                logger.warning(f"Failed to load RF: {e}")

        # Layer 5: LSTM Trajectory
        lstm_path = self._get_model_path('trajectory_lstm')
        if lstm_path:
            try:
                os.makedirs('/tmp/ls-lstm', exist_ok=True)
                parts = lstm_path[5:].split('/', 1)
                bucket = parts[0]
                key = parts[1]
                local_pt = '/tmp/ls-lstm/model.pt'
                s3.download_file(bucket, key, local_pt)
                # Download scaler (same prefix, _scaler.pkl)
                base_key = key.rsplit('.', 1)[0]
                scaler_key = f'{base_key}_scaler.pkl'
                local_scaler = '/tmp/ls-lstm/scaler.pkl'
                try:
                    s3.download_file(bucket, scaler_key, local_scaler)
                    with open(local_scaler, 'rb') as f:
                        self.lstm_scaler = pickle.load(f)
                except Exception:
                    self.lstm_scaler = None
                    logger.warning("LSTM scaler not found, using raw features")

                self.lstm_model = TrajectoryLSTM()
                self.lstm_model.load_state_dict(
                    torch.load(local_pt, map_location='cpu', weights_only=True)
                )
                self.lstm_model.eval()
                loaded.append('lstm')
            except Exception as e:
                logger.warning(f"Failed to load LSTM: {e}")

        # Layer 7: Ensemble
        ens_path = self._get_model_path('ensemble')
        if ens_path:
            try:
                local = '/tmp/ls-ens/model.pkl'
                os.makedirs('/tmp/ls-ens', exist_ok=True)
                parts = ens_path[5:].split('/', 1)
                s3.download_file(parts[0], parts[1], local)
                with open(local, 'rb') as f:
                    self.ensemble_model = pickle.load(f)
                loaded.append('ensemble')
            except Exception as e:
                logger.warning(f"Failed to load ensemble: {e}")

        logger.info(f"LS models loaded: {loaded}")
        return len(loaded) > 0

    def _get_model_path(self, model_type: str) -> str:
        """Get S3 artifact path for active model of given type."""
        ver = self.model_version_repo.get_active_model_by_type(model_type)
        if ver and ver.s3_artifact_path:
            return ver.s3_artifact_path
        return None

    def run_daily_predictions(self, race_date: date = None) -> dict:
        """
        Second-pass enrichment: read wr_predictions, enrich with L4-L7, update rows.
        """
        if race_date is None:
            race_date = date.today()

        if not self.load_model():
            logger.info(f"LS: no models loaded, skipping enrichment for {race_date}")
            return {'model': 'ls', 'date': str(race_date),
                    'enriched': 0, 'status': 'no_models'}

        # Read existing wr_predictions for today.
        # entry_id added so we can write to ls_predictions per row.
        rows = execute_query(self.conn,
            """SELECT wp.prediction_id, wp.horse_id, wp.race_id,
                      wp.entry_id,
                      wp.raw_win_prob, wp.rank_score,
                      e.morning_line_odds, r.race_type, r.field_size,
                      e.lasix_first_time, e.blinkers_on,
                      h.horse_name,
                      t.trainer_name,
                      EXISTS (
                        SELECT 1 FROM past_performances pp2
                        WHERE pp2.horse_id = wp.horse_id
                          AND pp2.race_date < r.race_date
                          AND pp2.purse IS NOT NULL AND r.purse IS NOT NULL
                          AND pp2.purse > r.purse * 1.15
                      ) AS class_drop,
                      (SELECT COUNT(*) FROM past_performances pp_count
                       WHERE pp_count.horse_id = wp.horse_id
                         AND pp_count.race_date < r.race_date) AS pp_count
               FROM wr_predictions wp
               JOIN entries e ON wp.entry_id = e.entry_id
               JOIN races r ON wp.race_id = r.race_id
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers tr ON e.trainer_id = tr.trainer_id
               LEFT JOIN LATERAL (SELECT trainer_name FROM trainers WHERE trainer_id = e.trainer_id) t ON true
               WHERE r.race_date = %s
                 AND wp.style = 'general'
                 AND COALESCE(e.is_scratched, FALSE) = FALSE""",
            (race_date,))

        if not rows:
            logger.info(f"LS: no wr_predictions for {race_date}")
            return {'model': 'ls', 'date': str(race_date),
                    'enriched': 0, 'status': 'no_predictions'}

        logger.info(f"LS: enriching {len(rows)} predictions for {race_date}")
        enriched = 0

        # ─── Pass 1: per-horse layer scores (existing logic, accumulated) ───
        # Group by race_id so Pass 2 can apply within-race normalization.
        from collections import defaultdict
        by_race: dict = defaultdict(list)

        for row in rows:
            try:
                horse_id = row['horse_id']
                raw_wp = float(row['raw_win_prob'] or 0.12)
                rank_sc = float(row['rank_score'] or 0)
                ml_odds = float(row['morning_line_odds'] or 5)
                field_size = int(row['field_size'] or 8)
                race_type = row.get('race_type', '')

                # Layer 4: RF Longshot (substrate-correct path; Decision 1 2026-05-16)
                rf_prob = 0.0
                if self.rf_model is not None:
                    try:
                        rf_prob = self._predict_rf_substrate_correct(
                            row['race_id'], horse_id, raw_wp, rank_sc
                        )
                    except Exception as e:
                        logger.debug(f"RF predict failed for {horse_id}: {e}")

                # Layer 5: LSTM Trajectory — NaN = no LSTM history available
                # (explicit sentinel so consumers can distinguish from a real 0.0)
                traj_score = float('nan')
                if self.lstm_model is not None:
                    try:
                        traj_score = self._predict_trajectory(horse_id, race_date)
                    except Exception as e:
                        logger.debug(f"LSTM predict failed for {horse_id}: {e}")

                # Layer 6: Bayesian Angles
                angle_name = None
                angle_posterior = 0.0
                angle_ev = -2.0
                try:
                    angle_result = self._score_angles(row, ml_odds, race_date)
                    angle_name = angle_result.get('angle_name')
                    angle_posterior = angle_result.get('angle_posterior', 0.0)
                    angle_ev = angle_result.get('angle_ev', -2.0)
                except Exception as e:
                    logger.warning(f"Angle scoring failed for {horse_id}: {e}")

                # Layer 7: Ensemble (raw probability — will be softmaxed within race)
                ens_prob = raw_wp  # fallback to Layer 1
                if self.ensemble_model is not None:
                    try:
                        race_quality = 2.0
                        if race_type:
                            rt = race_type.lower()
                            if 'stakes' in rt: race_quality = 5.0
                            elif 'allowance' in rt: race_quality = 4.0
                            elif 'maiden' in rt: race_quality = 3.0

                        ens_features = np.array([[
                            raw_wp, rank_sc, rf_prob, traj_score,
                            angle_ev, angle_posterior,
                            ml_odds, ml_odds,
                            race_quality, field_size,
                        ]])
                        ens_prob = float(
                            self.ensemble_model.predict_proba(ens_features)[0, 1]
                        )
                    except Exception as e:
                        logger.debug(f"Ensemble predict failed for {horse_id}: {e}")

                by_race[row['race_id']].append({
                    'row': row, 'rf_prob': rf_prob, 'traj_score': traj_score,
                    'angle_name': angle_name, 'angle_posterior': angle_posterior,
                    'angle_ev': angle_ev, 'ens_prob_raw': ens_prob,
                    'ml_odds': ml_odds, 'pp_count': int(row.get('pp_count') or 0),
                })

            except Exception as e:
                logger.error(f"LS layer-score failed for {row.get('horse_id')}: {e}")

        # ─── Pass 2: per-race normalization + writes ────────────────────────
        # For each race: 0-PP override → within-race softmax → final_win_probability.
        # Write to BOTH wr_predictions (enrichment, existing path) AND
        # ls_predictions (new first-class table).
        model_version_id = (
            self.model_version.model_version_id
            if hasattr(self, 'model_version') and self.model_version
            else None
        )

        for race_id, race_horses in by_race.items():
            n = len(race_horses)
            ens_probs_raw = np.array([h['ens_prob_raw'] for h in race_horses])

            # 0-PP override: no-data horses → field base rate
            base_rate = 1.0 / n
            for idx, h in enumerate(race_horses):
                if h['pp_count'] == 0:
                    ens_probs_raw[idx] = base_rate

            # Within-race softmax
            shifted = ens_probs_raw - ens_probs_raw.max()
            exp_scores = np.exp(shifted)
            final_win_probs = exp_scores / exp_scores.sum() if exp_scores.sum() > 0 else \
                              np.full(n, base_rate)

            # Market-prob within-race normalization (computed before ranking
            # so ranking can use edge_ratio)
            market_probs_raw = np.array([
                1.0 / (h['ml_odds'] + 1.0) if h['ml_odds'] > 0 else 0.0
                for h in race_horses
            ])
            mp_sum = market_probs_raw.sum()
            market_probs = market_probs_raw / mp_sum if mp_sum > 0 else market_probs_raw

            # predicted_rank: 1 = best LONGSHOT VALUE in the field.
            # Longshot value = model_prob / market_prob (edge ratio), but
            # only for horses meeting longshot criteria (ml_odds >=
            # LONGSHOT_THRESHOLD). Below-threshold horses (chalk) sort to
            # the bottom regardless of model probability — LS's stated
            # purpose is finding longshot value, not picking winners.
            # final_win_probability stays as the within-race-normalized
            # softmax (preserves sum-to-1.0 invariant for downstream
            # metrics); only ranking changes.
            LONGSHOT_THRESHOLD = 8.0  # ML odds floor for "longshot"
            ml_odds_arr = np.array([h['ml_odds'] for h in race_horses])
            pp_count_arr = np.array([h['pp_count'] for h in race_horses])
            edge_ratios = final_win_probs / np.maximum(market_probs, 0.01)
            # Eligibility: ml_odds >= LONGSHOT_THRESHOLD AND pp_count > 0.
            # Chalk (low ML) sorts to bottom; 0-PP horses also sort to bottom
            # (we have no data to recommend a longshot we know nothing about).
            # Both ineligible classes get -inf so they don't compete for LS
            # top ranks regardless of edge_ratio (which can be inflated for
            # 0-PP horses since their base_rate / very_low_market_prob is huge).
            ranking_scores = np.where(
                (ml_odds_arr >= LONGSHOT_THRESHOLD) & (pp_count_arr > 0),
                edge_ratios,
                -np.inf,
            )
            sorted_idx = np.argsort(-ranking_scores)
            ranks = np.empty(n, dtype=int)
            for rank, i in enumerate(sorted_idx):
                ranks[i] = rank + 1

            for idx, h in enumerate(race_horses):
                row = h['row']
                pred_id = row['prediction_id']
                ens_prob_norm = float(final_win_probs[idx])
                rank_val = int(ranks[idx])
                market_prob_norm = float(market_probs[idx])
                edge_pct = ens_prob_norm - market_prob_norm
                ml_odds = h['ml_odds']

                # Longshot alert logic — NaN-aware: missing trajectory_score
                # does not trigger the > 0.0 check (np.isnan() short-circuits)
                traj_present = h['traj_score'] is not None and not (
                    isinstance(h['traj_score'], float) and h['traj_score'] != h['traj_score']
                )
                traj_val = h['traj_score'] if traj_present else 0.0
                longshot_alert = (
                    ens_prob_norm > 0.10
                    and ml_odds >= 10
                    and h['rf_prob'] > 0.05
                    and traj_present
                    and traj_val > 0.0
                )
                if longshot_alert:
                    if h['rf_prob'] > 0.10 and h['angle_ev'] > 0:
                        confidence = 'high'
                    elif h['rf_prob'] > 0.05 or (traj_present and traj_val > 0.3):
                        confidence = 'medium'
                    else:
                        confidence = 'low'
                else:
                    confidence = None

                # Write 1: existing wr_predictions enrichment (backward compat)
                try:
                    with self.conn.cursor() as cur:
                        cur.execute("""
                            UPDATE wr_predictions SET
                                ensemble_win_prob = %s,
                                trajectory_score = %s,
                                longshot_prob = %s,
                                angle_name = %s,
                                angle_posterior = %s,
                                angle_ev = %s,
                                longshot_alert = %s,
                                confidence = %s
                            WHERE prediction_id = %s
                        """, (
                            round(ens_prob_norm, 4),
                            round(h['traj_score'], 4) if traj_present else None,
                            round(h['rf_prob'], 4),
                            h['angle_name'],
                            round(h['angle_posterior'], 4) if h['angle_posterior'] else None,
                            round(h['angle_ev'], 2) if h['angle_ev'] > -2 else None,
                            longshot_alert,
                            confidence,
                            pred_id,
                        ))

                    # Write 2: NEW first-class ls_predictions row
                    with self.conn.cursor() as cur:
                        cur.execute("""
                            INSERT INTO ls_predictions (
                                entry_id, race_id, horse_id, model_version_id,
                                style, final_win_probability,
                                longshot_alert, confidence,
                                predicted_rank, xgb_rank_score,
                                rf_longshot_prob, lstm_trajectory,
                                calibrated_win_prob, bayesian_angle_ev,
                                angle_description, market_prob, edge_pct,
                                is_top_pick, morning_line_implied_prob
                            ) VALUES (
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s
                            )
                            -- REPAIR-4: DO NOTHING substrate-protects clean
                            -- race-fire-time writes from substrate-leaked
                            -- post-race re-invocation overwrite
                            ON CONFLICT (race_id, entry_id, style) DO NOTHING
                        """, (
                            row['entry_id'], race_id, row['horse_id'],
                            model_version_id, 'general',
                            round(ens_prob_norm, 4),
                            longshot_alert, confidence,
                            rank_val, round(float(row['rank_score'] or 0), 4),
                            round(h['rf_prob'], 4),
                            round(h['traj_score'], 4) if traj_present else None,
                            round(float(row['raw_win_prob'] or 0), 4),
                            round(h['angle_ev'], 2) if h['angle_ev'] > -2 else None,
                            h['angle_name'],
                            round(market_prob_norm, 4),
                            round(edge_pct, 4),
                            (rank_val == 1),
                            round(market_prob_norm, 4),
                        ))
                    enriched += 1
                except Exception as e:
                    logger.error(f"LS write failed for {row.get('horse_id')}: {e}")

        self.conn.commit()

        alerts_count = sum(1 for r in rows
                          if self._is_alert_candidate(r, ml_odds=5))
        logger.info(f"LS: enriched {enriched} predictions, "
                    f"alerts approximate: checking DB")

        # Count actual alerts (LS only enriches style='general')
        alert_row = execute_one(self.conn,
            "SELECT COUNT(*) as cnt FROM wr_predictions wp "
            "JOIN races r ON wp.race_id = r.race_id "
            "WHERE r.race_date = %s AND wp.longshot_alert = true "
            "  AND wp.style = 'general'",
            (race_date,))
        alert_count = int(alert_row['cnt']) if alert_row else 0

        return {
            'model': 'ls',
            'date': str(race_date),
            'enriched': enriched,
            'longshot_alerts': alert_count,
            'status': 'enriched',
        }

    def _is_alert_candidate(self, row, ml_odds):
        """Quick check for alert reporting."""
        return float(row.get('morning_line_odds') or 0) >= 10

    def _predict_rf_simplified(self, raw_wp, rank_score, ml_odds):
        """LEGACY: substrate-broken 57-zero + 3-real RF invocation.

        DEPRECATED 2026-05-16 per Tier 1 2C finding (AUC against trained target
        substantially better with substrate-correct invocation). Retained as
        fallback if substrate-correct path fails.
        """
        x = np.zeros(60)
        x[58] = raw_wp
        x[59] = rank_score
        x[3] = ml_odds
        return float(self.rf_model.predict_proba(x.reshape(1, -1))[0, 1])

    def _predict_rf_substrate_correct(self, race_id, horse_id, raw_wp, rank_score):
        """Substrate-correct 60-feat longshot_rf invocation (Decision 1, 2026-05-16).

        Tier 1 2C finding: AUC 0.7762 against trained target (10-1+ longshot winner)
        vs broken-path AUC 0.4399 against is_winner. Substrate-correct invocation
        unlocks the model's intended signal.

        Substrate-pragmatic per-race feature cache: build feature matrix once per race,
        reuse across all horses in that race. Falls back to _predict_rf_simplified()
        if FE service unavailable or feature matrix build fails.
        """
        try:
            if self._fe_service is None:
                from services.feature_engineering_service import FeatureEngineeringService
                from repositories.race_repository import RaceRepository
                from repositories.entry_repository import EntryRepository
                self._fe_service = FeatureEngineeringService(self.conn)
                self._race_repo = RaceRepository(self.conn)
                self._entry_repo = EntryRepository(self.conn)

            # Per-race cache: build feature matrix once
            if race_id not in self._race_feature_cache:
                race = self._race_repo.get_race_by_id(race_id)
                if race is None:
                    return self._predict_rf_simplified(raw_wp, rank_score, 5.0)
                race.entries = self._entry_repo.get_entries_by_race(race_id, as_of_date=race.race_date)
                feature_df = self._fe_service.build_feature_matrix(race, include_odds=True)
                if feature_df.empty:
                    return self._predict_rf_simplified(raw_wp, rank_score, 5.0)
                feature_df['horse_id'] = feature_df['horse_id'].astype(str)
                self._race_feature_cache[race_id] = feature_df

            feature_df = self._race_feature_cache[race_id]
            row = feature_df[feature_df['horse_id'] == str(horse_id)]
            if row.empty:
                return self._predict_rf_simplified(raw_wp, rank_score, 5.0)

            # Substrate-correct 60-feat input
            from services.longshot_substrate_correct import (
                get_longshot_rf_feature_names, _patch_sklearn_pickle_compat,
                build_longshot_rf_input,
            )
            # Patch model on first call (idempotent)
            self.rf_model = _patch_sklearn_pickle_compat(self.rf_model)

            X = build_longshot_rf_input(
                row.copy(),
                pd.Series([raw_wp]),
                pd.Series([rank_score]),
            )
            try:
                p = self.rf_model.predict_proba(X)
                # Take P(positive class); if shape weird, fall back
                if p.shape[1] >= 2:
                    return float(p[0, 1])
                return float(p[0, 0])
            except Exception as e:
                # Tree-wise fallback (some sklearn version mismatches)
                logger.debug(f"predict_proba fail; tree-wise: {e}")
                probs = 0.0
                for est in self.rf_model.estimators_:
                    pe = est.predict_proba(X)
                    probs += float(pe[0, 1]) if pe.shape[1] >= 2 else float(pe[0, 0])
                return probs / len(self.rf_model.estimators_)
        except Exception as e:
            logger.debug(f"substrate-correct longshot_rf fail for {horse_id}: {e}")
            return self._predict_rf_simplified(raw_wp, rank_score, 5.0)

    def _predict_trajectory(self, horse_id: str, race_date: date) -> float:
        """Build sequence from PPs and run LSTM.

        Returns NaN (not 0.0) for the no-history case so callers can distinguish
        "model said 0.0" from "no data to score". XGB handles NaN natively;
        the runtime DB write coerces NaN → NULL.
        """
        rows = execute_query(self.conn,
            """SELECT computed_speed_figure, finish_position, field_size,
                      early_pace_figure, late_pace_figure,
                      days_since_last_race, purse, closing_odds
               FROM past_performances
               WHERE horse_id = %s AND race_date < %s
                 AND computed_speed_figure IS NOT NULL
               ORDER BY race_date DESC LIMIT %s""",
            (horse_id, race_date, SEQUENCE_LENGTH))

        if len(rows) < MIN_SEQUENCE_LENGTH:
            return float('nan')  # explicit sentinel, not silent 0.0

        # Build sequence (most recent last)
        seq = np.zeros((SEQUENCE_LENGTH, FEATURES_PER_STEP), dtype=np.float32)
        offset = SEQUENCE_LENGTH - len(rows)
        for j, r in enumerate(reversed(rows)):  # reverse to chronological
            fs = float(r.get('field_size') or 8)
            seq[offset + j] = [
                float(r.get('computed_speed_figure') or 0),
                float(r.get('finish_position') or 5) / max(fs, 1),
                float(r.get('early_pace_figure') or 24),
                float(r.get('late_pace_figure') or 38),
                float(r.get('days_since_last_race') or 30),
                float(r.get('purse') or 0),
                fs,
                float(r.get('closing_odds') or 5),
            ]

        # Normalize with saved scaler
        if self.lstm_scaler is not None:
            flat = seq.reshape(-1, FEATURES_PER_STEP)
            seq = self.lstm_scaler.transform(flat).reshape(1, SEQUENCE_LENGTH, FEATURES_PER_STEP)
        else:
            seq = seq.reshape(1, SEQUENCE_LENGTH, FEATURES_PER_STEP)

        seq = np.nan_to_num(seq, nan=0.0)
        tensor = torch.FloatTensor(seq)
        prob = float(self.lstm_model.predict_proba(tensor).item())
        # Map 0-1 to -1 to +1
        return round(prob * 2.0 - 1.0, 4)

    def _score_angles(self, row, ml_odds: float, race_date) -> dict:
        """Check angle flags and query angle_stats_history with AS-OF predicate.

        REPAIR-4 Step C.5: angle_stats was substrate-aggregate refreshed
        in-place by ingestion Lambda — backtest/training reads of
        angle_stats were substrate-leaky. Fix is angle_stats_history
        snapshot table populated daily; reads pull WHERE snapshot_date <=
        race_date ORDER BY DESC LIMIT 1 to get the substrate-correct
        AS-OF aggregate state. Fall-through to current angle_stats handles
        the cold-start case before the daily snapshot accumulates history.
        """
        angles_found = []

        if row.get('lasix_first_time'):
            angles_found.append('first_time_lasix')
        if row.get('blinkers_on'):
            angles_found.append('blinkers_on')
        if row.get('class_drop'):
            angles_found.append('class_drop')

        if not angles_found:
            return {'angle_name': None, 'angle_posterior': 0.0, 'angle_ev': -2.0}

        trainer_name = row.get('trainer_name')
        best = None

        for angle in angles_found:
            # Try trainer-specific from history (AS-OF race_date)
            stats = execute_one(self.conn,
                "SELECT wins, starts FROM angle_stats_history "
                "WHERE angle_name = %s AND trainer_name = %s "
                "  AND snapshot_date <= %s "
                "ORDER BY snapshot_date DESC LIMIT 1",
                (angle, trainer_name, race_date))
            if not stats or int(stats.get('starts', 0)) < 5:
                # Fall back to global (AS-OF)
                stats = execute_one(self.conn,
                    "SELECT wins, starts FROM angle_stats_history "
                    "WHERE angle_name = %s AND trainer_name IS NULL "
                    "  AND snapshot_date <= %s "
                    "ORDER BY snapshot_date DESC LIMIT 1",
                    (angle, race_date))

            if stats and int(stats.get('starts', 0)) > 0:
                from scipy.stats import beta as beta_dist
                wins = int(stats['wins'])
                starts = int(stats['starts'])
                post_a = 1.0 + wins
                post_b = 1.0 + (starts - wins)
                posterior = post_a / (post_a + post_b)
                decimal_odds = ml_odds + 1.0
                ev = (posterior * decimal_odds * 2.0) - 2.0

                if best is None or ev > best.get('angle_ev', -99):
                    best = {
                        'angle_name': angle,
                        'angle_posterior': round(posterior, 4),
                        'angle_ev': round(ev, 2),
                    }

        return best or {'angle_name': None, 'angle_posterior': 0.0, 'angle_ev': -2.0}
