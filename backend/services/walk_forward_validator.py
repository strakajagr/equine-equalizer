"""
Walk-Forward Validation Framework (Phase B Tier 1 Investigation 6A).

Reusable validation framework for substrate-grounded model + strategy evaluation
across rolling windows. Replaces single-split holdout with temporally-honest
walk-forward methodology.

Usage:
    from services.walk_forward_validator import WalkForwardValidator

    wf = WalkForwardValidator(
        train_window_days=60,
        eval_window_days=7,
        step_days=7,
        start_date=date(2026, 1, 1),
        end_date=date(2026, 5, 10),
    )

    # For a layer-level metric:
    for split in wf.iter_splits():
        train_df = pull_predictions(split.train_start, split.train_end)
        eval_df = pull_predictions(split.eval_start, split.eval_end)
        wf.record_split_metrics(split, layer_metrics)

    summary = wf.aggregate()
    confidence_intervals = wf.bootstrap_ci(n_resamples=1000)

Supports:
    - Per-strategy walk-forward
    - Per-layer walk-forward
    - Bootstrap CI on aggregate metrics (Section 6B input)
    - Per-context decomposition within each window (Section 6C input)
    - Stress testing (worst-window analysis; Section 6D input)
    - Risk-adjusted metric aggregation (Sharpe/Sortino; Section 6F input)
"""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class WalkForwardSplit:
    """One temporal split: train window + immediately-following eval window."""
    split_index: int
    train_start: date
    train_end: date
    eval_start: date
    eval_end: date

    @property
    def label(self) -> str:
        return (f"split_{self.split_index:03d}"
                f"_train_{self.train_start}_{self.train_end}"
                f"_eval_{self.eval_start}_{self.eval_end}")


@dataclass
class WalkForwardMetricsRecord:
    """Per-split metric snapshot."""
    split: WalkForwardSplit
    metrics: Dict[str, float]  # arbitrary metric dict; e.g., {'auc': 0.71, 'top1_wr': 0.31, 'roi_pct': 12.3}
    n_observations: int = 0
    n_winners: int = 0
    raw_predictions: Optional[pd.DataFrame] = None  # optional retain for re-analysis


class WalkForwardValidator:
    """Rolling-window walk-forward validation framework.

    Per § 4.30 alpha-maximization criterion: temporal validation must reflect
    actual production deployment cadence. Train on prior N days; evaluate on
    next M days; step forward by S days.
    """

    def __init__(
        self,
        train_window_days: int = 60,
        eval_window_days: int = 7,
        step_days: int = 7,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        min_eval_observations: int = 50,
    ):
        if not start_date or not end_date:
            raise ValueError("start_date and end_date required")
        if eval_window_days < 1 or train_window_days < 1:
            raise ValueError("windows must be positive")
        if start_date + timedelta(days=train_window_days + eval_window_days) > end_date:
            raise ValueError(
                f"date range [{start_date}..{end_date}] too short for "
                f"train={train_window_days}d + eval={eval_window_days}d"
            )

        self.train_window_days = train_window_days
        self.eval_window_days = eval_window_days
        self.step_days = step_days
        self.start_date = start_date
        self.end_date = end_date
        self.min_eval_observations = min_eval_observations
        self._records: List[WalkForwardMetricsRecord] = []

    def iter_splits(self) -> Iterator[WalkForwardSplit]:
        """Yield each walk-forward split. Train window ends immediately before eval start."""
        idx = 0
        cursor = self.start_date + timedelta(days=self.train_window_days)
        while cursor + timedelta(days=self.eval_window_days) <= self.end_date:
            train_end = cursor - timedelta(days=1)
            train_start = train_end - timedelta(days=self.train_window_days - 1)
            eval_start = cursor
            eval_end = cursor + timedelta(days=self.eval_window_days - 1)
            yield WalkForwardSplit(idx, train_start, train_end, eval_start, eval_end)
            idx += 1
            cursor += timedelta(days=self.step_days)

    def record(
        self,
        split: WalkForwardSplit,
        metrics: Dict[str, float],
        n_observations: int = 0,
        n_winners: int = 0,
        raw_predictions: Optional[pd.DataFrame] = None,
    ) -> None:
        if n_observations < self.min_eval_observations:
            logger.warning(
                f"{split.label}: n={n_observations} below min ({self.min_eval_observations}); skipping"
            )
            return
        self._records.append(WalkForwardMetricsRecord(
            split=split, metrics=metrics,
            n_observations=n_observations, n_winners=n_winners,
            raw_predictions=raw_predictions,
        ))

    def aggregate(self) -> Dict[str, Any]:
        """Aggregate metrics across all splits."""
        if not self._records:
            return {'note': 'no records'}
        df = pd.DataFrame([
            {**rec.metrics, 'n': rec.n_observations, 'winners': rec.n_winners,
             'split_label': rec.split.label}
            for rec in self._records
        ])
        out: Dict[str, Any] = {
            'n_splits': len(self._records),
            'total_observations': int(df['n'].sum()),
            'total_winners': int(df['winners'].sum()),
        }
        # Per-metric aggregate
        for col in df.columns:
            if col in ('n', 'winners', 'split_label'):
                continue
            vals = df[col].dropna().astype(float)
            if len(vals) == 0:
                continue
            out[f'{col}_mean'] = float(vals.mean())
            out[f'{col}_std'] = float(vals.std())
            out[f'{col}_min'] = float(vals.min())
            out[f'{col}_max'] = float(vals.max())
            out[f'{col}_median'] = float(vals.median())
            # Sharpe-like (return-volatility ratio if ROI-like metric)
            if 'roi' in col.lower() or 'pnl' in col.lower() or 'return' in col.lower():
                if vals.std() > 0:
                    out[f'{col}_sharpe_like'] = float(vals.mean() / vals.std())
                out[f'{col}_downside_std'] = float(vals[vals < 0].std()) if (vals < 0).any() else 0.0
                out[f'{col}_max_drawdown'] = float(vals.min())
        return out

    def bootstrap_ci(
        self,
        metric_key: str,
        n_resamples: int = 1000,
        confidence: float = 0.95,
        seed: int = 42,
    ) -> Dict[str, float]:
        """Bootstrap confidence interval on a per-split metric.
        Resamples splits with replacement, computes mean, reports lower/upper quantiles.
        """
        if not self._records:
            return {'note': 'no records'}
        values = np.array([
            rec.metrics[metric_key] for rec in self._records
            if metric_key in rec.metrics and rec.metrics[metric_key] is not None
        ])
        if len(values) < 3:
            return {'note': f'too few values ({len(values)})'}
        rng = np.random.RandomState(seed)
        means = np.empty(n_resamples)
        for i in range(n_resamples):
            sample = rng.choice(values, size=len(values), replace=True)
            means[i] = sample.mean()
        lower_q = (1 - confidence) / 2
        upper_q = 1 - lower_q
        return {
            'metric': metric_key,
            'point_estimate': float(values.mean()),
            'ci_lower': float(np.quantile(means, lower_q)),
            'ci_upper': float(np.quantile(means, upper_q)),
            'std_error': float(means.std()),
            'n_splits': int(len(values)),
        }

    def per_context_decomposition(
        self,
        context_col: str,
        metric_fn: Callable[[pd.DataFrame], Dict[str, float]],
    ) -> Dict[str, Dict[str, float]]:
        """Decompose metrics per context (e.g., per track / per race_type / per field_size bucket).
        Requires records to carry raw_predictions DataFrames.
        """
        out: Dict[str, Dict[str, float]] = {}
        for rec in self._records:
            if rec.raw_predictions is None:
                continue
            for ctx_val, grp in rec.raw_predictions.groupby(context_col, dropna=True):
                if len(grp) < self.min_eval_observations:
                    continue
                bucket = str(ctx_val)
                if bucket not in out:
                    out[bucket] = {'n': 0, 'splits': 0}
                metrics = metric_fn(grp)
                for k, v in metrics.items():
                    out[bucket].setdefault(k, []).append(v)
                out[bucket]['n'] += len(grp)
                out[bucket]['splits'] += 1
        # Aggregate per-context lists to mean/std
        agg = {}
        for bucket, vals in out.items():
            agg[bucket] = {'n': vals['n'], 'splits': vals['splits']}
            for k, v in vals.items():
                if isinstance(v, list) and len(v) > 0:
                    agg[bucket][f'{k}_mean'] = float(np.mean(v))
                    agg[bucket][f'{k}_std'] = float(np.std(v))
        return agg

    def stress_test_summary(self, metric_key: str = 'roi_pct') -> Dict[str, float]:
        """Worst-case window analysis: drawdown depth + recovery time + cold-streak length."""
        if not self._records:
            return {'note': 'no records'}
        vals = np.array([
            rec.metrics.get(metric_key, 0.0) for rec in self._records
        ])
        cumulative = np.cumsum(vals)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = cumulative - running_max
        # Cold streak = consecutive negative-metric windows
        signs = vals < 0
        max_cold_streak = 0
        cur_streak = 0
        for s in signs:
            cur_streak = cur_streak + 1 if s else 0
            max_cold_streak = max(max_cold_streak, cur_streak)
        return {
            'metric': metric_key,
            'max_drawdown': float(drawdown.min()),
            'max_drawdown_position': int(np.argmin(drawdown)),
            'max_cold_streak_splits': int(max_cold_streak),
            'pct_negative_splits': float((vals < 0).mean()),
            'worst_split_value': float(vals.min()),
            'best_split_value': float(vals.max()),
        }

    def kelly_simulation(
        self,
        roi_metric_key: str = 'roi_pct',
        bankroll_start: float = 1000.0,
        kelly_fraction: float = 0.25,
    ) -> Dict[str, float]:
        """Simulate bankroll growth under fractional-Kelly staking using per-split ROI.
        Each split's ROI is treated as the per-period return; stake fraction × bankroll
        per period; report final bankroll + log-growth rate.
        """
        if not self._records:
            return {'note': 'no records'}
        rois = [rec.metrics.get(roi_metric_key, 0.0) / 100.0 for rec in self._records]
        bankroll = bankroll_start
        history = [bankroll]
        for roi in rois:
            stake = bankroll * kelly_fraction
            bankroll = bankroll - stake + stake * (1 + roi)
            history.append(bankroll)
        log_growth = float(np.log(bankroll / bankroll_start) / len(rois))
        return {
            'metric': roi_metric_key,
            'kelly_fraction': kelly_fraction,
            'bankroll_start': bankroll_start,
            'bankroll_end': float(bankroll),
            'cumulative_return_pct': float((bankroll / bankroll_start - 1) * 100),
            'log_growth_per_period': log_growth,
            'n_periods': len(rois),
        }

    def records(self) -> List[WalkForwardMetricsRecord]:
        return self._records


# ─────────────────────────────────────────────────────────────────
# Standard metric functions for use with the validator
# ─────────────────────────────────────────────────────────────────

def standard_layer_metrics(df: pd.DataFrame,
                            pred_col: str,
                            outcome_col: str = 'is_winner',
                            race_id_col: str = 'race_id',
                            payout_col: str = 'win_payout') -> Dict[str, float]:
    """Standard layer metrics for use with the validator's record() call."""
    from sklearn.metrics import roc_auc_score, brier_score_loss
    valid = df[df[pred_col].notna() & df[outcome_col].notna()]
    if len(valid) < 10:
        return {}
    out = {'n_observations': len(valid)}
    try:
        out['auc'] = float(roc_auc_score(valid[outcome_col], valid[pred_col]))
    except Exception:
        out['auc'] = None
    try:
        out['brier'] = float(brier_score_loss(valid[outcome_col], valid[pred_col].clip(0, 1)))
    except Exception:
        out['brier'] = None
    if race_id_col in valid.columns:
        top1 = valid.loc[valid.groupby(race_id_col)[pred_col].idxmax()]
        out['top1_win_rate'] = float(top1[outcome_col].mean())
        if payout_col in top1.columns:
            payouts = top1[top1[outcome_col] == 1][payout_col].astype(float)
            stake = len(top1) * 2.0
            payout_sum = float(payouts.sum()) if len(payouts) else 0.0
            out['flat_win_pnl'] = round(payout_sum - stake, 2)
            out['flat_win_roi_pct'] = round((payout_sum - stake) / stake * 100, 2) if stake else 0
    return out
