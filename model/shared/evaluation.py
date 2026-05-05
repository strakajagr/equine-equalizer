"""
Equine Equalizer — P&L Evaluation Metrics

PRIMARY metrics: flat_bet_roi, kelly_roi, value_bet_win_rate
SECONDARY:       top1_win_rate, exacta/trifecta hit rates, ndcg
"""

import logging
import numpy as np
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)

FLAT_BET_SIZE = 2.0
MIN_KELLY_BET = 2.0
MAX_KELLY_FRACTION = 0.10   # cap at 10% of bankroll
MIN_EDGE = 0.05             # only bet when edge > 5%
HALF_KELLY = 0.5


def implied_probability(closing_odds: float) -> float:
    """
    closing_odds is in X-1 (American-style decimal minus 1) format.
    e.g., 4.0 means 4-1 = decimal odds of 5.0.
    """
    decimal_odds = float(closing_odds) + 1.0
    return 1.0 / decimal_odds


def kelly_fraction(win_prob: float, decimal_odds: float,
                   fraction: float = HALF_KELLY) -> float:
    """
    Kelly Criterion bet sizing.
    win_prob:     model's predicted win probability
    decimal_odds: decimal odds (e.g., 5.0 for 4-1)
    fraction:     Kelly multiplier (default 0.5 = half-Kelly)
    """
    b = decimal_odds - 1.0   # net odds
    p = float(win_prob)
    q = 1.0 - p
    if b <= 0 or p <= 0:
        return 0.0
    k = (b * p - q) / b
    k = max(0.0, k)
    return k * fraction


def flat_bet_roi(predictions_df: pd.DataFrame) -> float:
    """
    Bet FLAT_BET_SIZE on the top pick in every race.
    predictions_df must have: race_key, horse_id, predicted_score,
                              finish_position, win_payout
    """
    total_wagered = 0.0
    total_returned = 0.0
    race_keys = predictions_df['race_key'].unique()

    for rk in race_keys:
        race = predictions_df[predictions_df['race_key'] == rk]
        if race.empty:
            continue
        top_pick = race.nlargest(1, 'predicted_score').iloc[0]
        total_wagered += FLAT_BET_SIZE
        if top_pick['finish_position'] == 1 and top_pick['win_payout'] > 0:
            total_returned += float(top_pick['win_payout'])

    if total_wagered == 0:
        return 0.0
    return (total_returned - total_wagered) / total_wagered


def kelly_roi(predictions_df: pd.DataFrame,
              starting_bankroll: float = 1000.0) -> float:
    """
    Kelly-sized bets. Only bet when edge > MIN_EDGE.
    Returns ROI = (final_bankroll - start) / start.
    """
    bankroll = starting_bankroll
    total_wagered = 0.0
    total_returned = 0.0
    race_keys = predictions_df['race_key'].unique()

    for rk in sorted(race_keys):
        race = predictions_df[predictions_df['race_key'] == rk]
        if race.empty:
            continue

        for _, horse in race.iterrows():
            pred_prob = horse.get('predicted_prob', 0.0)
            odds = horse.get('closing_odds', 5.0)
            if pd.isna(pred_prob) or pd.isna(odds):
                continue
            pred_prob = float(pred_prob)
            odds = float(odds)
            if odds <= 0:
                continue
            decimal_odds = odds + 1.0
            imp_prob = implied_probability(odds)
            edge = pred_prob - imp_prob

            if edge <= MIN_EDGE:
                continue

            kf = kelly_fraction(pred_prob, decimal_odds)
            kf = min(kf, MAX_KELLY_FRACTION)
            bet_size = max(MIN_KELLY_BET, bankroll * kf)
            bet_size = min(bet_size, bankroll)

            total_wagered += bet_size
            if horse['finish_position'] == 1 and horse.get('win_payout', 0) > 0:
                returned = bet_size * (decimal_odds)
                total_returned += returned
                bankroll = bankroll - bet_size + returned
            else:
                bankroll -= bet_size

    if total_wagered == 0:
        return 0.0
    return (total_returned - total_wagered) / total_wagered


def top1_win_rate(predictions_df: pd.DataFrame) -> float:
    """% of top picks that win."""
    hits = 0
    total = 0
    for rk in predictions_df['race_key'].unique():
        race = predictions_df[predictions_df['race_key'] == rk]
        if race.empty:
            continue
        top = race.nlargest(1, 'predicted_score').iloc[0]
        total += 1
        if top['finish_position'] == 1:
            hits += 1
    return hits / total if total > 0 else 0.0


def exacta_hit_rate(predictions_df: pd.DataFrame) -> float:
    """% of races where top 2 picks are the actual top 2 finishers."""
    hits = 0
    total = 0
    for rk in predictions_df['race_key'].unique():
        race = predictions_df[predictions_df['race_key'] == rk]
        if len(race) < 2:
            continue
        top2_pred = set(race.nlargest(2, 'predicted_score')['horse_id'].tolist())
        actual_top2 = set(race.nsmallest(2, 'finish_position')['horse_id'].tolist())
        total += 1
        if top2_pred == actual_top2:
            hits += 1
    return hits / total if total > 0 else 0.0


def trifecta_hit_rate(predictions_df: pd.DataFrame) -> float:
    """% of races where top 3 picks are the actual top 3 finishers."""
    hits = 0
    total = 0
    for rk in predictions_df['race_key'].unique():
        race = predictions_df[predictions_df['race_key'] == rk]
        if len(race) < 3:
            continue
        top3_pred = set(race.nlargest(3, 'predicted_score')['horse_id'].tolist())
        actual_top3 = set(race.nsmallest(3, 'finish_position')['horse_id'].tolist())
        total += 1
        if top3_pred == actual_top3:
            hits += 1
    return hits / total if total > 0 else 0.0


def avg_edge_on_winners(predictions_df: pd.DataFrame) -> float:
    """Average (predicted_prob - implied_prob) for bets that won."""
    edges = []
    for _, row in predictions_df.iterrows():
        if row['finish_position'] != 1:
            continue
        pred_prob = row.get('predicted_prob', 0.0)
        odds = row.get('closing_odds', 5.0)
        if pd.isna(pred_prob) or pd.isna(odds):
            continue
        pred_prob = float(pred_prob)
        odds = float(odds)
        if odds <= 0:
            continue
        imp = implied_probability(odds)
        edge = pred_prob - imp
        if edge > MIN_EDGE:
            edges.append(edge)
    return float(np.mean(edges)) if edges else 0.0


def value_bet_win_rate(predictions_df: pd.DataFrame) -> float:
    """Win rate specifically on bets where edge > MIN_EDGE."""
    def _has_edge(r):
        pp = r.get('predicted_prob', 0)
        od = r.get('closing_odds', 5)
        if pd.isna(pp) or pd.isna(od) or float(od) <= 0:
            return False
        return (float(pp) - implied_probability(float(od))) > MIN_EDGE

    bets = predictions_df[predictions_df.apply(_has_edge, axis=1)]
    if bets.empty:
        return 0.0
    return float((bets['finish_position'] == 1).mean())


def ndcg_score(predictions_df: pd.DataFrame, k: int = 5) -> float:
    """
    Normalized Discounted Cumulative Gain at k.
    SECONDARY metric — do not optimize for this.
    """
    ndcg_scores = []
    for rk in predictions_df['race_key'].unique():
        race = predictions_df[predictions_df['race_key'] == rk].copy()
        if len(race) < 2:
            continue
        race = race.sort_values('predicted_score', ascending=False).head(k)
        # Relevance: 1 for winner, 0 otherwise
        race['relevance'] = (race['finish_position'] == 1).astype(float)
        dcg = sum(rel / np.log2(i + 2) for i, rel in enumerate(race['relevance']))
        # Ideal: winner ranked first
        idcg = 1.0  # max possible DCG for binary relevance
        ndcg_scores.append(dcg / idcg if idcg > 0 else 0.0)
    return float(np.mean(ndcg_scores)) if ndcg_scores else 0.0


def calibration_score(predictions_df: pd.DataFrame,
                      n_bins: int = 10) -> float:
    """
    Calibration: if model says 20%, horses should win ~20%.
    Returns mean absolute error between predicted and actual bin rates.
    Lower is better. 0.0 = perfect calibration.
    """
    df = predictions_df.copy()
    prob_col = 'raw_win_prob' if 'raw_win_prob' in df.columns else 'predicted_prob'
    if prob_col not in df.columns or df[prob_col].isna().all():
        return 0.0
    is_winner = (df['finish_position'] == 1).astype(float)
    try:
        df['prob_bin'] = pd.cut(df[prob_col], bins=n_bins, labels=False)
    except ValueError:
        return 0.0
    cal = df.groupby('prob_bin').agg(
        predicted=pd.NamedAgg(column=prob_col, aggfunc='mean'),
        actual=pd.NamedAgg(column='finish_position',
                           aggfunc=lambda x: float((x == 1).mean())),
        count=pd.NamedAgg(column=prob_col, aggfunc='count')
    ).dropna()
    if cal.empty:
        return 0.0
    return float(abs(cal['predicted'] - cal['actual']).mean())


def log_loss_score(predictions_df: pd.DataFrame) -> float:
    """Binary log loss. Lower is better."""
    prob_col = 'raw_win_prob' if 'raw_win_prob' in predictions_df.columns else 'predicted_prob'
    if prob_col not in predictions_df.columns:
        return 0.0
    probs = predictions_df[prob_col].values.astype(float)
    actual = (predictions_df['finish_position'] == 1).values.astype(float)
    # Clip to avoid log(0)
    probs = np.clip(probs, 1e-7, 1 - 1e-7)
    ll = -(actual * np.log(probs) + (1 - actual) * np.log(1 - probs))
    return float(np.mean(ll))


def full_evaluation(predictions_df: pd.DataFrame,
                    model_name: str = 'Model') -> dict:
    """
    Run all metrics and print a clean summary.

    predictions_df must have:
        race_key, horse_id, predicted_score, predicted_prob,
        finish_position, win_payout, closing_odds
    """
    n_races = predictions_df['race_key'].nunique()
    n_horses = len(predictions_df)

    metrics = {
        'flat_bet_roi':       round(flat_bet_roi(predictions_df), 4),
        'kelly_roi':          round(kelly_roi(predictions_df), 4),
        'top1_win_rate':      round(top1_win_rate(predictions_df), 4),
        'exacta_hit_rate':    round(exacta_hit_rate(predictions_df), 4),
        'trifecta_hit_rate':  round(trifecta_hit_rate(predictions_df), 4),
        'avg_edge_on_winners': round(avg_edge_on_winners(predictions_df), 4),
        'value_bet_win_rate': round(value_bet_win_rate(predictions_df), 4),
        'ndcg_at_5':          round(ndcg_score(predictions_df, k=5), 4),
        'calibration':        round(calibration_score(predictions_df), 4),
        'log_loss':           round(log_loss_score(predictions_df), 4),
        'n_races':            n_races,
        'n_horses':           n_horses,
    }

    bar = '=' * 56
    logger.info(f"\n{bar}")
    logger.info(f"  {model_name} — P&L Evaluation")
    logger.info(bar)
    logger.info(f"  Races: {n_races:,}    Horses: {n_horses:,}")
    logger.info(bar)
    logger.info(f"  flat_bet_roi          {metrics['flat_bet_roi']:+.1%}  ← PRIMARY")
    logger.info(f"  kelly_roi             {metrics['kelly_roi']:+.1%}  ← PRIMARY")
    logger.info(f"  value_bet_win_rate    {metrics['value_bet_win_rate']:.3f}")
    logger.info(f"  avg_edge_on_winners   {metrics['avg_edge_on_winners']:.3f}")
    logger.info(f"  top1_win_rate         {metrics['top1_win_rate']:.3f}")
    logger.info(f"  exacta_hit_rate       {metrics['exacta_hit_rate']:.3f}")
    logger.info(f"  trifecta_hit_rate     {metrics['trifecta_hit_rate']:.3f}")
    logger.info(f"  ndcg@5                {metrics['ndcg_at_5']:.3f}  (secondary)")
    logger.info(f"  calibration           {metrics['calibration']:.4f}  (lower=better)")
    logger.info(f"  log_loss              {metrics['log_loss']:.4f}  (lower=better)")
    logger.info(bar)

    print(f"\n{bar}")
    print(f"  {model_name} — Evaluation")
    print(bar)
    print(f"  top1_win_rate         {metrics['top1_win_rate']:.3f}  ← PRIMARY")
    print(f"  calibration           {metrics['calibration']:.4f}  ← PRIMARY (lower=better)")
    print(f"  log_loss              {metrics['log_loss']:.4f}")
    print(f"  flat_bet_roi          {metrics['flat_bet_roi']:+.1%}")
    print(f"  kelly_roi             {metrics['kelly_roi']:+.1%}")
    print(f"  value_bet_win_rate    {metrics['value_bet_win_rate']:.3f}")
    print(f"  avg_edge_on_winners   {metrics['avg_edge_on_winners']:.3f}")
    print(f"  exacta_hit_rate       {metrics['exacta_hit_rate']:.3f}")
    print(f"  trifecta_hit_rate     {metrics['trifecta_hit_rate']:.3f}")
    print(f"  ndcg@5                {metrics['ndcg_at_5']:.3f}")
    print(bar)

    return metrics
