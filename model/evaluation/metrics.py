import numpy as np
import pandas as pd
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def exacta_hit_rate(
    predictions_df: pd.DataFrame,
    results_df: pd.DataFrame
) -> float:
    """
    What % of races did our top 2 predicted
    horses cover the actual exacta?

    An exacta is covered if our top 2 horses
    finished 1st and 2nd in any order.

    predictions_df columns required:
      race_id, horse_id, predicted_rank
    results_df columns required:
      race_id, horse_id, official_finish

    Returns float 0.0 to 1.0
    """
    hits = 0
    total = 0

    for race_id in predictions_df[
        'race_id'
    ].unique():
        race_preds = predictions_df[
            predictions_df['race_id'] == race_id
        ].sort_values('predicted_rank')

        race_results = results_df[
            results_df['race_id'] == race_id
        ]

        if len(race_preds) < 2 or len(
            race_results
        ) < 2:
            continue

        # Our top 2 predicted horses
        top2_predicted = set(
            race_preds.head(2)['horse_id'].tolist()
        )

        # Actual top 2 finishers
        actual_top2 = set(
            race_results.nsmallest(
                2, 'official_finish'
            )['horse_id'].tolist()
        )

        if top2_predicted == actual_top2:
            hits += 1
        total += 1

    return hits / total if total > 0 else 0.0


def trifecta_hit_rate(
    predictions_df: pd.DataFrame,
    results_df: pd.DataFrame
) -> float:
    """
    What % of races did our top 3 predicted
    horses cover the actual trifecta?

    A trifecta is covered if our top 3 horses
    finished 1st, 2nd, and 3rd in any order.

    Same df structure as exacta_hit_rate.
    Returns float 0.0 to 1.0
    """
    hits = 0
    total = 0

    for race_id in predictions_df[
        'race_id'
    ].unique():
        race_preds = predictions_df[
            predictions_df['race_id'] == race_id
        ].sort_values('predicted_rank')

        race_results = results_df[
            results_df['race_id'] == race_id
        ]

        if len(race_preds) < 3 or len(
            race_results
        ) < 3:
            continue

        top3_predicted = set(
            race_preds.head(3)['horse_id'].tolist()
        )
        actual_top3 = set(
            race_results.nsmallest(
                3, 'official_finish'
            )['horse_id'].tolist()
        )

        if top3_predicted == actual_top3:
            hits += 1
        total += 1

    return hits / total if total > 0 else 0.0


def top1_accuracy(
    predictions_df: pd.DataFrame,
    results_df: pd.DataFrame
) -> float:
    """
    What % of races did our top-ranked horse win?
    This is win rate — useful but NOT our primary
    metric. We optimize for exacta/trifecta.
    """
    hits = 0
    total = 0

    for race_id in predictions_df[
        'race_id'
    ].unique():
        race_preds = predictions_df[
            predictions_df['race_id'] == race_id
        ].sort_values('predicted_rank')

        race_results = results_df[
            results_df['race_id'] == race_id
        ]

        if race_preds.empty or race_results.empty:
            continue

        top_pick = race_preds.iloc[0]['horse_id']
        winner = race_results[
            race_results['official_finish'] == 1
        ]

        if not winner.empty:
            if winner.iloc[0]['horse_id'] == top_pick:
                hits += 1
        total += 1

    return hits / total if total > 0 else 0.0


def top3_accuracy(
    predictions_df: pd.DataFrame,
    results_df: pd.DataFrame
) -> float:
    """
    What % of races did our #1 pick finish in
    the top 3? A softer metric than top1_accuracy
    but shows model is finding competitive horses.
    """
    hits = 0
    total = 0

    for race_id in predictions_df[
        'race_id'
    ].unique():
        race_preds = predictions_df[
            predictions_df['race_id'] == race_id
        ].sort_values('predicted_rank')

        race_results = results_df[
            results_df['race_id'] == race_id
        ]

        if race_preds.empty or race_results.empty:
            continue

        top_pick = race_preds.iloc[0]['horse_id']
        result = race_results[
            race_results['horse_id'] == top_pick
        ]

        if not result.empty:
            if result.iloc[0]['official_finish'] <= 3:
                hits += 1
        total += 1

    return hits / total if total > 0 else 0.0


def calibration_score(
    predictions_df: pd.DataFrame,
    results_df: pd.DataFrame,
    n_buckets: int = 10
) -> float:
    """
    Measures how well win_probability matches
    actual win rates across probability buckets.

    A perfectly calibrated model: horses given
    20% win probability should win 20% of the time.

    Uses Expected Calibration Error (ECE).
    Lower ECE = better calibration.
    Returns 1.0 - ECE so higher = better,
    consistent with other metrics.

    predictions_df needs: horse_id, race_id,
      win_probability, predicted_rank
    results_df needs: horse_id, race_id,
      official_finish
    """
    merged = predictions_df.merge(
        results_df[['race_id', 'horse_id',
                     'official_finish']],
        on=['race_id', 'horse_id'],
        how='left'
    )
    merged['actual_win'] = (
        merged['official_finish'] == 1
    ).astype(float)

    merged = merged.dropna(
        subset=['win_probability', 'actual_win']
    )

    if merged.empty:
        return 0.0

    # Bin predictions into buckets
    merged['bucket'] = pd.cut(
        merged['win_probability'],
        bins=n_buckets,
        labels=False
    )

    ece = 0.0
    n = len(merged)

    for bucket in merged['bucket'].unique():
        if pd.isna(bucket):
            continue
        bucket_df = merged[
            merged['bucket'] == bucket
        ]
        bucket_size = len(bucket_df)
        if bucket_size == 0:
            continue
        avg_predicted = bucket_df[
            'win_probability'
        ].mean()
        avg_actual = bucket_df['actual_win'].mean()
        ece += (bucket_size / n) * abs(
            avg_predicted - avg_actual
        )

    return round(1.0 - ece, 4)


def print_evaluation_report(
    predictions_df: pd.DataFrame,
    results_df: pd.DataFrame,
    model_name: str = 'Model'
) -> dict:
    """
    Print and return full evaluation report.
    Called after training validation step.
    """
    metrics = {
        'exacta_hit_rate': exacta_hit_rate(
            predictions_df, results_df
        ),
        'trifecta_hit_rate': trifecta_hit_rate(
            predictions_df, results_df
        ),
        'top1_accuracy': top1_accuracy(
            predictions_df, results_df
        ),
        'top3_accuracy': top3_accuracy(
            predictions_df, results_df
        ),
        'calibration_score': calibration_score(
            predictions_df, results_df
        ),
        'race_count': len(
            predictions_df['race_id'].unique()
        ),
    }

    logger.info(f"\n{'=' * 50}")
    logger.info(f"  {model_name} Evaluation Report")
    logger.info(f"{'=' * 50}")
    logger.info(
        f"  Races evaluated: "
        f"{metrics['race_count']}"
    )
    logger.info(
        f"  Exacta hit rate:   "
        f"{metrics['exacta_hit_rate']:.3f}"
        f"  (top 2 cover actual exacta)"
    )
    logger.info(
        f"  Trifecta hit rate: "
        f"{metrics['trifecta_hit_rate']:.3f}"
        f"  (top 3 cover actual trifecta)"
    )
    logger.info(
        f"  Win rate (top1):   "
        f"{metrics['top1_accuracy']:.3f}"
        f"  (not primary metric)"
    )
    logger.info(
        f"  Top3 rate:         "
        f"{metrics['top3_accuracy']:.3f}"
        f"  (#1 pick finishes in top 3)"
    )
    logger.info(
        f"  Calibration score: "
        f"{metrics['calibration_score']:.3f}"
        f"  (1.0 = perfect)"
    )
    logger.info(f"{'=' * 50}\n")

    return metrics
