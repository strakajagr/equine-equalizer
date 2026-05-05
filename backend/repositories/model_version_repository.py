from typing import Optional
from psycopg2.extras import Json
from .base_repository import BaseRepository
from .transforms import transform_model_version
from models.canonical import ModelVersion


class ModelVersionRepository(BaseRepository):

    def get_active_model(self) -> Optional[ModelVersion]:
        """
        Get the currently active model version.
        Only one model should have is_active = true.
        This is what the inference Lambda loads.
        """
        row = self._query_one(
            """SELECT * FROM model_versions
               WHERE is_active = true
               ORDER BY training_date DESC
               LIMIT 1"""
        )
        return transform_model_version(row) if row else None

    def get_model_by_version(
        self, version_name: str
    ) -> Optional[ModelVersion]:
        row = self._query_one(
            """SELECT * FROM model_versions
               WHERE version_name = %s""",
            (version_name,)
        )
        return transform_model_version(row) if row else None

    def get_all_models(self) -> list[ModelVersion]:
        """All model versions ordered newest first."""
        rows = self._query(
            """SELECT * FROM model_versions
               ORDER BY training_date DESC"""
        )
        return [transform_model_version(r) for r in rows]

    def insert_model_version(
        self, model_data: dict
    ) -> str:
        """Register new trained model. Returns model_version_id."""
        row = self._write_returning(
            """INSERT INTO model_versions (
                 version_name, training_date,
                 training_data_start, training_data_end,
                 training_race_count, feature_list,
                 hyperparameters, s3_artifact_path,
                 is_active, notes
               ) VALUES (
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
               )
               RETURNING model_version_id""",
            (
                model_data['version_name'],
                model_data['training_date'],
                model_data['training_data_start'],
                model_data['training_data_end'],
                model_data.get('training_race_count'),
                Json(model_data.get('feature_list', {})),
                Json(model_data.get('hyperparameters', {})),
                model_data.get('s3_artifact_path'),
                model_data.get('is_active', False),
                model_data.get('notes')
            )
        )
        return str(row['model_version_id'])

    def set_active_model(
        self, model_version_id: str
    ) -> None:
        """
        Deactivate models OF THE SAME TYPE only,
        then activate this one. Called after training
        when new model passes evaluation thresholds.
        """
        model = self._query_one(
            "SELECT model_type FROM model_versions "
            "WHERE model_version_id = %s",
            (model_version_id,)
        )
        if not model:
            raise ValueError(
                f"Model {model_version_id} not found"
            )
        self._write(
            "UPDATE model_versions SET is_active = false "
            "WHERE model_type = %s",
            (model['model_type'],)
        )
        self._write(
            "UPDATE model_versions SET is_active = true "
            "WHERE model_version_id = %s",
            (model_version_id,)
        )

    def get_active_model_by_type(
        self, model_type: str
    ) -> Optional[ModelVersion]:
        """
        Get the active model for a specific type.
        model_type must be 'wr', 'pl', or 'ls'.
        Returns None if no active model of that type.
        """
        row = self._query_one(
            """SELECT * FROM model_versions
               WHERE is_active = true
               AND model_type = %s
               LIMIT 1""",
            (model_type,)
        )
        return transform_model_version(row) if row else None

    def update_evaluation_metrics(
        self,
        model_version_id: str,
        exacta_hit_rate: float,
        trifecta_hit_rate: float,
        top1_accuracy: float,
        top3_accuracy: float,
        calibration_score: float
    ) -> None:
        """
        Update performance metrics after evaluation.
        Called by evaluation service after accumulating
        enough race results to be statistically meaningful.
        """
        self._write(
            """UPDATE model_versions SET
                 exacta_hit_rate = %s,
                 trifecta_hit_rate = %s,
                 top1_accuracy = %s,
                 top3_accuracy = %s,
                 calibration_score = %s
               WHERE model_version_id = %s""",
            (
                exacta_hit_rate,
                trifecta_hit_rate,
                top1_accuracy,
                top3_accuracy,
                calibration_score,
                model_version_id
            )
        )
