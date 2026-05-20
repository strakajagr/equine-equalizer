"""Shared registration substrate for trained ML artifacts.

Substrate-pragmatic shared registration: canonical model/training/train.py
and all per-layer training scripts (wr, pl, longshot, ranker, ensemble,
trajectory, win_prob) invoke register_trained_artifact() post-S3-upload.

Defaults is_active=FALSE per § 4.34 forensic-gate discipline (activation
requires forensic substrate validation, not training-time eval).

Substrate-prophylactic: Tier 1 Phase 3.5 required
/tmp/phase3_register_artifacts.py helper to backfill 37 lean58 artifacts
that per-layer training scripts had uploaded to S3 but never registered.
This module is the substrate-permanent bake-in fix.
"""

import json
import logging
import re
from datetime import date, datetime
from typing import Optional

logger = logging.getLogger(__name__)


_SPECIALIST_SUFFIXES = (
    'speed', 'closer', 'route', 'sprint',
    'class_riser', 'class_dropper', 'gonzo_sauce', 'general',
)


def derive_model_type(version_name: str) -> str:
    """Substrate-grounded pattern-match version_name → model_type.

    Mirrors the substrate established by /tmp/phase3_register_artifacts.py.
    Strips trailing _YYYYMMDD_HHMM timestamp, then maps known prefixes
    onto canonical model_type tokens.
    """
    name = re.sub(r'_\d{8}_\d{4}$', '', version_name)

    prefix_map = [
        ('pl_core_lean58_',       'pl_core_'),
        ('pl_core_lean53_',       'pl_core_'),
        ('pl_workout_lean58_',    'pl_workout_'),
        ('pl_workout_lean53_',    'pl_workout_'),
        ('wp_core_lean58_',       'win_prob_core_'),
        ('wp_core_lean53_',       'win_prob_core_'),
        ('wp_full_lean58_',       'wp_full_'),
        ('wp_full_lean53_',       'wp_full_'),
        ('rk_full_lean58_',       'rk_full_'),
        ('rk_full_lean53_',       'rk_full_'),
        ('wr_core_',              'wr_core_'),
        ('wr_workout_',           'wr_workout_'),
        ('ls_',                   'ls_'),
        ('longshot_',             'ls_'),
        ('ensemble_',             'ensemble_'),
        ('trajectory_',           'trajectory_'),
    ]

    bare_map = {
        'pl_core_lean58':    'pl_core_general',
        'pl_workout_lean58': 'pl_workout_general',
        'wp_core_lean58':    'win_prob_core_general',
        'wp_full_lean58':    'wp_full_general',
        'rk_full_lean58':    'rk_full_general',
        # REPAIR-5 retrain wave (2026-05-20): trainers now emit bare-prefix
        # artifact names without the _lean58_/_lean53_ infix the older
        # patterns above carried. Substrate-verified mapping (each new
        # artifact name maps to the same model_type as the contaminated
        # model it supersedes, per existing model_versions rows):
        #   rk_core / rk_full     → matches ranker_core / ranker_full active rows
        #   v_base_core / v_odds_core / v_base_workout / v_odds_workout
        #                         → matches wr_base / wr_odds / wr_base_workout / wr_odds_workout rows
        #   wp_base / wp_odds     → matches win_prob_base (1 inactive) / win_prob_odds (2 of 3 inactive)
        #   wp_full               → matches win_prob_full (3 of 3 prior inactive — unanimous prefix→type pattern)
        'rk_core':           'ranker_core',
        'rk_full':           'ranker_full',
        'v_base_core':       'wr_base',
        'v_odds_core':       'wr_odds',
        'v_base_workout':    'wr_base_workout',
        'v_odds_workout':    'wr_odds_workout',
        'wp_base':           'win_prob_base',
        'wp_odds':           'win_prob_odds',
        'wp_full':           'win_prob_full',
    }

    if name in bare_map:
        return bare_map[name]

    for src_prefix, dst_prefix in prefix_map:
        if name.startswith(src_prefix):
            spec = name[len(src_prefix):] or 'general'
            return f'{dst_prefix}{spec}'

    raise ValueError(
        f"Unmappable version_name '{version_name}' — extend "
        f"derive_model_type() prefix_map to cover this naming pattern."
    )


def _get_default_conn():
    """Substrate-grounded DB connection — defers import to call-time
    so this module is importable in contexts without psycopg2/boto3
    (e.g. compile validation, unit tests with mocked conns)."""
    from shared.data_loader import _get_conn
    return _get_conn()


def register_trained_artifact(
    version_name: str,
    s3_artifact_path: str,
    training_metadata: dict,
    model_type: Optional[str] = None,
    is_active: bool = False,
    db_conn=None,
) -> str:
    """Register trained ML artifact in model_versions.

    Substrate-pragmatic shared registration: per-layer training scripts
    invoke this function post-S3-upload to bake registration into the
    same Fargate cycle that produced the S3 artifact.

    Args:
        version_name: Substrate-canonical artifact name (e.g.
            'wp_core_lean58_general_20260512_1834').
        s3_artifact_path: Full s3:// URI of the model artifact (.json).
        training_metadata: Dict of training-time fields. Recognized keys:
            feature_names (list), feature_list (dict), xgb_params (dict),
            hyperparameters (dict), training_data_start (date|str),
            training_data_end (date|str), training_race_count (int),
            top1_accuracy, top3_accuracy, calibration_score,
            exacta_hit_rate, trifecta_hit_rate, flat_bet_roi, kelly_roi,
            value_bet_win_rate (all numeric, optional), notes (str).
            Any unrecognized keys are folded into hyperparameters JSONB
            so substrate-pragmatic per-layer metrics survive.
        model_type: Optional explicit model_type. If None, derived from
            version_name via substrate-grounded prefix map.
        is_active: Defaults FALSE per § 4.34 forensic-gate discipline.
            Activation is a separate forensic-substrate step, never a
            training-time auto-promotion.
        db_conn: Optional psycopg2 connection. If None, opens one via
            shared.data_loader._get_conn (substrate-canonical for
            training scripts).

    Returns:
        model_version_id (UUID string).
    """
    if model_type is None:
        model_type = derive_model_type(version_name)

    owns_conn = db_conn is None
    if owns_conn:
        db_conn = _get_default_conn()

    feature_list = training_metadata.get('feature_list')
    if feature_list is None and 'feature_names' in training_metadata:
        feature_list = {'features': training_metadata['feature_names']}
    if feature_list is None:
        feature_list = {}

    hyperparameters = (
        training_metadata.get('hyperparameters')
        or training_metadata.get('xgb_params')
        or {}
    )

    recognized = {
        'feature_names', 'feature_list', 'xgb_params', 'hyperparameters',
        'training_data_start', 'training_data_end', 'training_race_count',
        'top1_accuracy', 'top3_accuracy', 'calibration_score',
        'exacta_hit_rate', 'trifecta_hit_rate', 'flat_bet_roi',
        'kelly_roi', 'value_bet_win_rate', 'notes', 'training_date',
    }
    extras = {
        k: v for k, v in training_metadata.items() if k not in recognized
    }
    if extras:
        hyperparameters = dict(hyperparameters)
        hyperparameters.setdefault('_training_extras', {}).update(extras)

    training_date = training_metadata.get(
        'training_date'
    ) or datetime.utcnow()
    training_data_start = training_metadata.get(
        'training_data_start'
    ) or date(2022, 1, 1)
    training_data_end = training_metadata.get(
        'training_data_end'
    ) or date.today()

    try:
        with db_conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO model_versions (
                    version_name, model_type, training_date,
                    training_data_start, training_data_end,
                    training_race_count,
                    feature_list, hyperparameters, s3_artifact_path,
                    top1_accuracy, top3_accuracy, calibration_score,
                    exacta_hit_rate, trifecta_hit_rate,
                    flat_bet_roi, kelly_roi, value_bet_win_rate,
                    is_active, notes
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING model_version_id;
                """,
                (
                    version_name,
                    model_type,
                    training_date,
                    training_data_start,
                    training_data_end,
                    training_metadata.get('training_race_count'),
                    json.dumps(feature_list),
                    json.dumps(hyperparameters),
                    s3_artifact_path,
                    training_metadata.get('top1_accuracy'),
                    training_metadata.get('top3_accuracy'),
                    training_metadata.get('calibration_score'),
                    training_metadata.get('exacta_hit_rate'),
                    training_metadata.get('trifecta_hit_rate'),
                    training_metadata.get('flat_bet_roi'),
                    training_metadata.get('kelly_roi'),
                    training_metadata.get('value_bet_win_rate'),
                    is_active,
                    training_metadata.get('notes'),
                ),
            )
            row = cur.fetchone()
            model_version_id = (
                row['model_version_id']
                if isinstance(row, dict)
                else row[0]
            )
        db_conn.commit()
    except Exception:
        db_conn.rollback()
        raise
    finally:
        if owns_conn:
            db_conn.close()

    logger.info(
        f"Registered: {model_type} / {version_name} "
        f"(UUID {model_version_id}, is_active={is_active})"
    )
    return str(model_version_id)
