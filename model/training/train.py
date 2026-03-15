import os
import sys
import json
import logging
import argparse
import pickle
import boto3
import numpy as np
import pandas as pd
import xgboost as xgb
from datetime import date, datetime
from sklearn.model_selection import GroupShuffleSplit
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(
    Path(__file__).parent.parent.parent / 'backend'
))

from shared.db import get_db
from shared.constants import QUALIFYING_TRACKS
from services.feature_engineering_service import (
    FeatureEngineeringService
)
from repositories.race_repository import (
    RaceRepository
)
from repositories.result_repository import (
    ResultRepository
)
from repositories.entry_repository import (
    EntryRepository
)

# Add model root to path for model.* imports
sys.path.insert(0, str(
    Path(__file__).parent.parent.parent
))

from model.features.feature_definitions import (
    ALL_FEATURES, TARGET_COLUMN,
    GROUP_COLUMN, INDEX_COLUMNS,
    FEATURE_COUNT
)
from model.evaluation.metrics import (
    print_evaluation_report
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════

# XGBoost hyperparameters
# rank:pairwise = ranking objective
# Optimizes relative ordering within groups
# (races), not absolute prediction values
DEFAULT_PARAMS = {
    'objective': 'rank:pairwise',
    'eval_metric': 'ndcg',
    'eta': 0.05,             # learning rate — low = more trees needed
                             # but better generalization
    'max_depth': 6,          # tree depth — 6 is standard starting point
    'min_child_weight': 5,   # min samples per leaf — prevents overfitting
                             # on small horse samples
    'subsample': 0.8,        # row sampling per tree — reduces overfitting
    'colsample_bytree': 0.8, # feature sampling — forces diverse trees
    'gamma': 1.0,            # min split gain — higher = more conservative
    'reg_alpha': 0.1,        # L1 regularization
    'reg_lambda': 1.0,       # L2 regularization
    'seed': 42,
    'verbosity': 1,
}

NUM_ROUNDS = 500           # max boosting rounds
EARLY_STOPPING = 50        # stop if no improvement
VALIDATION_SPLIT = 0.2     # 20% held out for eval
MIN_RACES_FOR_TRAINING = 100


# ═══════════════════════════════════════════
# FUNCTION: load_training_data
# ═══════════════════════════════════════════

def load_training_data(
    conn,
    start_date: date = None,
    end_date: date = None
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load all qualifying races with results
    from the database.

    Returns two DataFrames:
    1. features_df: one row per horse per race
       columns: INDEX_COLUMNS + ALL_FEATURES
    2. results_df: one row per horse per race
       columns: race_id, horse_id, official_finish

    Races without complete results are excluded.
    Races with fewer than 4 starters are excluded.
    """
    logger.info("Loading training data...")

    race_repo = RaceRepository(conn)
    result_repo = ResultRepository(conn)
    fe_service = FeatureEngineeringService(conn)

    all_feature_rows = []
    all_result_rows = []
    races_processed = 0
    races_skipped = 0

    # Get date range
    if not start_date:
        start_date = date(2023, 1, 1)
    if not end_date:
        end_date = date(2023, 12, 31)

    # Get all qualifying races in range
    # Process month by month to manage memory
    from datetime import timedelta
    current = start_date.replace(day=1)

    while current <= end_date:
        # Get last day of month
        if current.month == 12:
            month_end = current.replace(
                year=current.year + 1,
                month=1, day=1
            ) - timedelta(days=1)
        else:
            month_end = current.replace(
                month=current.month + 1,
                day=1
            ) - timedelta(days=1)

        month_end = min(month_end, end_date)

        logger.info(
            f"Processing {current.strftime('%B %Y')}..."
        )

        # Get each day in month
        day = current
        while day <= month_end:
            try:
                races = race_repo \
                    .get_qualifying_races_by_date(day)

                for race in races:
                    # Load entries
                    entry_repo = EntryRepository(conn)
                    race.entries = entry_repo \
                        .get_entries_by_race(race.race_id)

                    if len(race.entries) < 4:
                        races_skipped += 1
                        continue

                    # Get results for this race
                    results = result_repo \
                        .get_results_by_race(race.race_id)

                    if len(results) < 4:
                        races_skipped += 1
                        continue

                    # Build feature matrix
                    try:
                        feature_df = fe_service \
                            .build_feature_matrix(race)

                        if feature_df.empty:
                            races_skipped += 1
                            continue

                        feature_df['race_id'] = race.race_id
                        feature_df['race_date'] = (
                            race.race_date
                        )

                        all_feature_rows.append(feature_df)

                        # Build results rows
                        for result in results:
                            all_result_rows.append({
                                'race_id': race.race_id,
                                'horse_id': (
                                    result.entry.horse.horse_id
                                ),
                                'official_finish': (
                                    result.official_finish
                                )
                            })

                        races_processed += 1

                    except Exception as e:
                        logger.warning(
                            f"Feature build failed for race "
                            f"{race.race_id}: {e}"
                        )
                        races_skipped += 1

            except Exception as e:
                logger.warning(
                    f"Error loading {day}: {e}"
                )

            day += timedelta(days=1)

        # Move to next month
        if current.month == 12:
            current = current.replace(
                year=current.year + 1, month=1, day=1
            )
        else:
            current = current.replace(
                month=current.month + 1, day=1
            )

    logger.info(
        f"Loaded {races_processed} races, "
        f"skipped {races_skipped}"
    )

    if not all_feature_rows:
        raise ValueError(
            "No training data loaded. "
            "Check database has race data."
        )

    features_df = pd.concat(
        all_feature_rows, ignore_index=True
    )
    results_df = pd.DataFrame(all_result_rows)

    return features_df, results_df


# ═══════════════════════════════════════════
# FUNCTION: prepare_xgboost_data
# ═══════════════════════════════════════════

def prepare_xgboost_data(
    features_df: pd.DataFrame,
    results_df: pd.DataFrame
) -> tuple:
    """
    Merge features with results.
    Split into train/validation sets.
    Create XGBoost DMatrix objects.

    Split strategy: GroupShuffleSplit by race_id
    This ensures all horses in a race are in
    the same split — you cannot have some horses
    from a race in train and others in validation.
    That would be data leakage.

    Returns:
    - dtrain: XGBoost DMatrix for training
    - dval: XGBoost DMatrix for validation
    - val_features: DataFrame for evaluation
    - val_results: DataFrame for evaluation
    - train_groups: group sizes for ranker
    - val_groups: group sizes for ranker
    """
    # Merge features with results
    merged = features_df.merge(
        results_df[['race_id', 'horse_id',
                     'official_finish']],
        on=['race_id', 'horse_id'],
        how='inner'
    )

    # Drop rows with missing target
    merged = merged.dropna(
        subset=['official_finish']
    )

    # Ensure feature columns all exist
    for col in ALL_FEATURES:
        if col not in merged.columns:
            logger.warning(
                f"Missing feature: {col} — filling 0"
            )
            merged[col] = 0.0

    # Fill NaN in features
    merged[ALL_FEATURES] = merged[
        ALL_FEATURES
    ].fillna(0.0)

    logger.info(
        f"Total samples: {len(merged)} horses "
        f"across {merged['race_id'].nunique()} races"
    )

    # Split by race (no leakage)
    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=VALIDATION_SPLIT,
        random_state=42
    )
    train_idx, val_idx = next(
        splitter.split(
            merged,
            groups=merged['race_id']
        )
    )

    train_df = merged.iloc[train_idx]
    val_df = merged.iloc[val_idx]

    logger.info(
        f"Train: {len(train_df)} samples, "
        f"{train_df['race_id'].nunique()} races"
    )
    logger.info(
        f"Val:   {len(val_df)} samples, "
        f"{val_df['race_id'].nunique()} races"
    )

    # XGBoost ranker requires groups:
    # group = number of horses per race
    # Must be in the same order as the data
    train_groups = train_df.groupby(
        'race_id', sort=False
    )['horse_id'].count().values
    val_groups = val_df.groupby(
        'race_id', sort=False
    )['horse_id'].count().values

    # XGBoost label for ranking:
    # INVERT finish position so rank 1 = highest label
    # XGBoost rank:pairwise maximizes label ordering
    train_labels = (
        train_df['official_finish'].max() -
        train_df['official_finish'] + 1
    ).values
    val_labels = (
        val_df['official_finish'].max() -
        val_df['official_finish'] + 1
    ).values

    # Create DMatrix objects
    dtrain = xgb.DMatrix(
        train_df[ALL_FEATURES].values,
        label=train_labels,
        feature_names=ALL_FEATURES
    )
    dtrain.set_group(train_groups)

    dval = xgb.DMatrix(
        val_df[ALL_FEATURES].values,
        label=val_labels,
        feature_names=ALL_FEATURES
    )
    dval.set_group(val_groups)

    return (
        dtrain, dval,
        val_df, results_df,
        train_groups, val_groups
    )


# ═══════════════════════════════════════════
# FUNCTION: train_model
# ═══════════════════════════════════════════

def train_model(
    dtrain: xgb.DMatrix,
    dval: xgb.DMatrix,
    params: dict = None,
    num_rounds: int = NUM_ROUNDS
) -> xgb.Booster:
    """
    Train XGBoost ranking model.

    Uses early stopping on validation NDCG.
    NDCG (Normalized Discounted Cumulative Gain)
    is the standard ranking quality metric —
    it rewards correct ordering of the top horses
    more than correct ordering at the bottom.
    A model that correctly identifies the winner
    gets more credit than one that correctly
    orders 5th vs 6th place.

    Returns trained Booster object.
    """
    if params is None:
        params = DEFAULT_PARAMS

    logger.info("Training XGBoost ranking model...")
    logger.info(f"Parameters: {params}")
    logger.info(
        f"Max rounds: {num_rounds}, "
        f"Early stopping: {EARLY_STOPPING}"
    )

    evals = [(dtrain, 'train'), (dval, 'val')]
    evals_result = {}

    model = xgb.train(
        params=params,
        dtrain=dtrain,
        num_boost_round=num_rounds,
        evals=evals,
        evals_result=evals_result,
        early_stopping_rounds=EARLY_STOPPING,
        verbose_eval=50  # log every 50 rounds
    )

    logger.info(
        f"Training complete. "
        f"Best round: {model.best_iteration}, "
        f"Best NDCG: {model.best_score:.4f}"
    )

    return model


# ═══════════════════════════════════════════
# FUNCTION: evaluate_model
# ═══════════════════════════════════════════

def evaluate_model(
    model: xgb.Booster,
    val_features_df: pd.DataFrame,
    results_df: pd.DataFrame
) -> dict:
    """
    Evaluate trained model on validation set.
    Uses our actual metrics: exacta and trifecta
    hit rates — not XGBoost's internal NDCG.

    This is the key difference from the Kalshi
    mistake: we evaluate on the metric that
    actually matters for P&L (exotic hit rates),
    not a proxy metric (win rate or NDCG alone).
    """
    logger.info("Evaluating model...")

    # Get validation race IDs
    val_race_ids = val_features_df[
        'race_id'
    ].unique()

    # Build predictions DataFrame
    pred_rows = []
    for race_id in val_race_ids:
        race_df = val_features_df[
            val_features_df['race_id'] == race_id
        ]

        if race_df.empty:
            continue

        # Ensure feature order matches training
        X = race_df[ALL_FEATURES].fillna(0.0)
        dmatrix = xgb.DMatrix(
            X.values,
            feature_names=ALL_FEATURES
        )
        scores = model.predict(dmatrix)

        for i, (_, row) in enumerate(
            race_df.iterrows()
        ):
            pred_rows.append({
                'race_id': race_id,
                'horse_id': row['horse_id'],
                'score': float(scores[i]),
            })

    pred_df = pd.DataFrame(pred_rows)

    if pred_df.empty:
        logger.warning("No predictions generated")
        return {}

    # Rank within each race
    pred_df['predicted_rank'] = pred_df \
        .groupby('race_id')['score'] \
        .rank(ascending=False, method='first') \
        .astype(int)

    # Compute win probability (softmax within race)
    def softmax_probs(group):
        scores = group['score'].values
        exp_scores = np.exp(
            scores - scores.max()
        )
        group = group.copy()
        group['win_probability'] = (
            exp_scores / exp_scores.sum()
        )
        return group

    pred_df = pred_df.groupby(
        'race_id', group_keys=False
    ).apply(softmax_probs)

    # Get results for validation races only
    val_results = results_df[
        results_df['race_id'].isin(val_race_ids)
    ]

    metrics = print_evaluation_report(
        pred_df, val_results, 'Equine Equalizer v1'
    )

    return metrics


# ═══════════════════════════════════════════
# FUNCTION: save_model
# ═══════════════════════════════════════════

def save_model(
    model: xgb.Booster,
    metrics: dict,
    params: dict,
    output_dir: str = '/tmp',
    s3_bucket: str = None,
    version_name: str = None
) -> str:
    """
    Save model artifact locally and optionally
    to S3.

    Saves:
    - model.xgb: the XGBoost booster
    - model_metadata.json: params, metrics,
      feature list, version info

    Returns S3 path if bucket provided,
    else local path.
    """
    if not version_name:
        version_name = (
            f"v{datetime.now().strftime('%Y%m%d_%H%M')}"
        )

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(
        output_dir, 'model.xgb'
    )
    metadata_path = os.path.join(
        output_dir, 'model_metadata.json'
    )

    # Save model
    model.save_model(model_path)
    logger.info(f"Model saved to {model_path}")

    # Save metadata
    metadata = {
        'version_name': version_name,
        'training_date': datetime.now().isoformat(),
        'feature_count': FEATURE_COUNT,
        'feature_names': ALL_FEATURES,
        'hyperparameters': params or DEFAULT_PARAMS,
        'best_iteration': model.best_iteration,
        'best_ndcg': float(model.best_score),
        'evaluation_metrics': metrics,
        'training_data': '2023 Equibase Dataset',
    }

    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    logger.info(
        f"Metadata saved to {metadata_path}"
    )

    # Upload to S3 if bucket provided
    if s3_bucket:
        s3_key_prefix = (
            f"models/{version_name}/"
        )
        s3_client = boto3.client('s3')

        for local_file, s3_suffix in [
            (model_path, 'model.xgb'),
            (metadata_path, 'model_metadata.json')
        ]:
            s3_key = s3_key_prefix + s3_suffix
            s3_client.upload_file(
                local_file, s3_bucket, s3_key
            )
            logger.info(
                f"Uploaded to s3://{s3_bucket}/{s3_key}"
            )

        return f"s3://{s3_bucket}/{s3_key_prefix}"

    return output_dir


# ═══════════════════════════════════════════
# FUNCTION: register_model
# ═══════════════════════════════════════════

def register_model(
    conn,
    version_name: str,
    metrics: dict,
    params: dict,
    s3_path: str,
    training_race_count: int,
    set_active: bool = False
) -> str:
    """
    Register trained model in model_versions table.
    Returns model_version_id.

    set_active=True promotes this model to active,
    which the inference Lambda will pick up on
    next invocation.

    Only set_active=True after manual review of
    metrics. Never auto-promote.
    """
    from repositories.model_version_repository \
        import ModelVersionRepository

    repo = ModelVersionRepository(conn)

    model_data = {
        'version_name': version_name,
        'training_date': datetime.now(),
        'training_data_start': date(2023, 1, 1),
        'training_data_end': date(2023, 12, 31),
        'training_race_count': training_race_count,
        'exacta_hit_rate': metrics.get(
            'exacta_hit_rate'
        ),
        'trifecta_hit_rate': metrics.get(
            'trifecta_hit_rate'
        ),
        'top1_accuracy': metrics.get('top1_accuracy'),
        'top3_accuracy': metrics.get('top3_accuracy'),
        'calibration_score': metrics.get(
            'calibration_score'
        ),
        'feature_list': {'features': ALL_FEATURES},
        'hyperparameters': params or DEFAULT_PARAMS,
        's3_artifact_path': s3_path,
        'is_active': set_active,
        'notes': (
            'Initial model trained on '
            '2023 Equibase dataset'
        ),
    }

    model_version_id = repo.insert_model_version(
        model_data
    )

    if set_active:
        repo.set_active_model(model_version_id)
        logger.info(
            f"Model {version_name} set as ACTIVE"
        )
    else:
        logger.info(
            f"Model {version_name} registered "
            f"(not active — review metrics first)"
        )

    return model_version_id


# ═══════════════════════════════════════════
# FUNCTION: get_feature_importance
# ═══════════════════════════════════════════

def get_feature_importance(
    model: xgb.Booster
) -> dict:
    """
    Extract and log feature importance.
    This is the model telling you what
    actually predicts finishing position
    across thousands of races.

    Returns dict sorted by importance descending.
    Uses 'gain' importance type:
    gain = average improvement in ranking quality
    each time a feature is used to split.
    Gain is more meaningful than 'weight'
    (count of splits) for understanding
    which features actually matter.
    """
    importance = model.get_score(
        importance_type='gain'
    )
    # Fill zeros for unused features
    for feat in ALL_FEATURES:
        if feat not in importance:
            importance[feat] = 0.0

    sorted_importance = dict(
        sorted(
            importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    logger.info("\nTop 20 Features by Importance:")
    logger.info("-" * 40)
    for i, (feat, score) in enumerate(
        list(sorted_importance.items())[:20]
    ):
        logger.info(f"  {i + 1:2d}. {feat:<35} {score:.2f}")

    return sorted_importance


# ═══════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════

def main():
    """
    Main training pipeline entry point.

    Usage:
      python train.py
      python train.py --start-date 2023-01-01
      python train.py --end-date 2023-12-31
      python train.py --s3-bucket my-bucket
      python train.py --set-active
      python train.py --version-name v1.0
    """
    parser = argparse.ArgumentParser(
        description='Train Equine Equalizer XGBoost model'
    )
    parser.add_argument(
        '--start-date',
        default='2023-01-01',
        help='Training data start date YYYY-MM-DD'
    )
    parser.add_argument(
        '--end-date',
        default='2023-12-31',
        help='Training data end date YYYY-MM-DD'
    )
    parser.add_argument(
        '--s3-bucket',
        default=os.environ.get(
            'MODEL_ARTIFACTS_BUCKET'
        ),
        help='S3 bucket for model artifacts'
    )
    parser.add_argument(
        '--output-dir',
        default='/tmp/equine-model',
        help='Local output directory'
    )
    parser.add_argument(
        '--version-name',
        default=None,
        help='Model version name (default: timestamp)'
    )
    parser.add_argument(
        '--set-active',
        action='store_true',
        help='Set model as active after training'
    )
    args = parser.parse_args()

    start_date = date.fromisoformat(
        args.start_date
    )
    end_date = date.fromisoformat(args.end_date)

    logger.info("=" * 50)
    logger.info("  Equine Equalizer Training Pipeline")
    logger.info("=" * 50)
    logger.info(f"  Date range: {start_date} to {end_date}")
    logger.info(f"  Features: {FEATURE_COUNT}")
    logger.info(f"  Objective: rank:pairwise")
    logger.info(f"  Primary metric: exacta hit rate")
    logger.info("=" * 50)

    with get_db() as conn:
        # Step 1: Load data
        features_df, results_df = load_training_data(
            conn, start_date, end_date
        )

        race_count = features_df['race_id'].nunique()
        logger.info(
            f"Dataset: {len(features_df)} horse-races "
            f"across {race_count} races"
        )

        if race_count < MIN_RACES_FOR_TRAINING:
            raise ValueError(
                f"Only {race_count} races loaded. "
                f"Need at least {MIN_RACES_FOR_TRAINING}. "
                f"Run ingestion first."
            )

        # Step 2: Prepare XGBoost data
        (dtrain, dval,
         val_features_df, val_results_df,
         train_groups, val_groups
        ) = prepare_xgboost_data(
            features_df, results_df
        )

        # Step 3: Train
        model = train_model(dtrain, dval)

        # Step 4: Feature importance
        importance = get_feature_importance(model)

        # Step 5: Evaluate on held-out races
        metrics = evaluate_model(
            model, val_features_df, results_df
        )
        metrics['race_count'] = race_count

        # Step 6: Save model
        version_name = (
            args.version_name or
            f"v{datetime.now().strftime('%Y%m%d_%H%M')}"
        )
        s3_path = save_model(
            model=model,
            metrics=metrics,
            params=DEFAULT_PARAMS,
            output_dir=args.output_dir,
            s3_bucket=args.s3_bucket,
            version_name=version_name
        )

        # Step 7: Register in database
        model_version_id = register_model(
            conn=conn,
            version_name=version_name,
            metrics=metrics,
            params=DEFAULT_PARAMS,
            s3_path=s3_path,
            training_race_count=race_count,
            set_active=args.set_active
        )

        logger.info(f"\nTraining complete.")
        logger.info(
            f"Model version ID: {model_version_id}"
        )
        logger.info(
            f"Exacta hit rate: "
            f"{metrics.get('exacta_hit_rate', 0):.3f}"
        )
        logger.info(
            f"Trifecta hit rate: "
            f"{metrics.get('trifecta_hit_rate', 0):.3f}"
        )
        if not args.set_active:
            logger.info(
                f"\nReview metrics then activate with:"
                f"\n  python train.py --set-active "
                f"--version-name {version_name}"
            )


if __name__ == '__main__':
    main()
