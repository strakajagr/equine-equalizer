import json
import logging
from shared.db import get_db

logger = logging.getLogger(__name__)


def _response(status_code: int, body: dict) -> dict:
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, default=str)
    }


def get_dashboard_metrics(event: dict, context) -> dict:
    """
    GET /dashboard/metrics
    Returns model performance, feature importance,
    track breakdown, data coverage, and model history.
    """
    try:
        from repositories.model_version_repository \
            import ModelVersionRepository
        from shared.db import execute_query, execute_one

        with get_db() as conn:
            mv_repo = ModelVersionRepository(conn)

            # Active model info
            active = mv_repo.get_active_model()
            active_info = None
            if active:
                active_info = {
                    'model_version_id': active.model_version_id,
                    'version_name': active.version_name,
                    'training_date': str(active.training_date),
                    'training_race_count': active.training_race_count,
                    'exacta_hit_rate': active.exacta_hit_rate,
                    'trifecta_hit_rate': active.trifecta_hit_rate,
                    'top1_accuracy': active.top1_accuracy,
                    'top3_accuracy': active.top3_accuracy,
                    'calibration_score': active.calibration_score,
                    'feature_list': active.feature_list,
                    'hyperparameters': active.hyperparameters,
                    's3_artifact_path': active.s3_artifact_path,
                    'notes': active.notes,
                }

            # Model version history
            all_models = mv_repo.get_all_models()
            model_history = [
                {
                    'model_version_id': m.model_version_id,
                    'version_name': m.version_name,
                    'training_date': str(m.training_date),
                    'exacta_hit_rate': m.exacta_hit_rate,
                    'trifecta_hit_rate': m.trifecta_hit_rate,
                    'top1_accuracy': m.top1_accuracy,
                    'is_active': m.is_active,
                }
                for m in all_models
            ]

            # Data coverage: races by track and year
            coverage_rows = execute_query(
                conn,
                """SELECT
                     t.track_code,
                     t.track_name,
                     EXTRACT(YEAR FROM r.race_date)::int as year,
                     COUNT(*) as race_count
                   FROM races r
                   JOIN tracks t ON r.track_id = t.track_id
                   GROUP BY t.track_code, t.track_name, year
                   ORDER BY t.track_code, year"""
            )
            coverage = [dict(r) for r in coverage_rows]

            # Total counts
            counts = execute_one(
                conn,
                """SELECT
                     (SELECT COUNT(*) FROM races) as races,
                     (SELECT COUNT(*) FROM horses) as horses,
                     (SELECT COUNT(*) FROM entries) as entries,
                     (SELECT COUNT(*) FROM results) as results,
                     (SELECT COUNT(*) FROM past_performances)
                       as past_performances,
                     (SELECT COUNT(*) FROM predictions)
                       as predictions,
                     (SELECT MIN(race_date) FROM races)
                       as earliest_date,
                     (SELECT MAX(race_date) FROM races)
                       as latest_date"""
            )

            # Dates that have predictions
            pred_dates = execute_query(
                conn,
                """SELECT DISTINCT r.race_date, COUNT(*) as pred_count
                   FROM predictions p
                   JOIN races r ON p.race_id = r.race_id
                   GROUP BY r.race_date
                   ORDER BY r.race_date DESC
                   LIMIT 30"""
            )

            return _response(200, {
                'active_model': active_info,
                'model_history': model_history,
                'data_coverage': coverage,
                'counts': dict(counts) if counts else {},
                'prediction_dates': [
                    {
                        'date': str(r['race_date']),
                        'count': r['pred_count']
                    }
                    for r in pred_dates
                ],
            })
    except Exception as e:
        logger.error(f"get_dashboard_metrics error: {e}")
        return _response(500, {'error': str(e)})


def get_available_dates(event: dict, context) -> dict:
    """
    GET /races/available-dates
    Returns dates that have qualifying races with entries,
    so the frontend can show a date picker.
    """
    try:
        from shared.db import execute_query
        with get_db() as conn:
            rows = execute_query(
                conn,
                """SELECT
                     r.race_date,
                     COUNT(DISTINCT r.race_id) as race_count,
                     COUNT(DISTINCT t.track_code) as track_count,
                     BOOL_OR(p.prediction_id IS NOT NULL
                             OR wp.prediction_id IS NOT NULL)
                       as has_predictions
                   FROM races r
                   JOIN tracks t ON r.track_id = t.track_id
                   LEFT JOIN predictions p
                     ON r.race_id = p.race_id
                   LEFT JOIN wr_predictions wp
                     ON r.race_id = wp.race_id
                   WHERE r.race_date >= '2023-01-01'
                   GROUP BY r.race_date
                   HAVING COUNT(DISTINCT r.race_id) >= 3
                   ORDER BY r.race_date DESC
                   LIMIT 100"""
            )
            return _response(200, {
                'dates': [
                    {
                        'date': str(r['race_date']),
                        'race_count': r['race_count'],
                        'track_count': r['track_count'],
                        'has_predictions': r['has_predictions'],
                    }
                    for r in rows
                ]
            })
    except Exception as e:
        logger.error(f"get_available_dates error: {e}")
        return _response(500, {'error': str(e)})
