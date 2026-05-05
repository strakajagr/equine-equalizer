"""
Gonzo Sauce feature computation. Used by BOTH:
  - model/shared/data_loader.py (training-time feature matrix generation)
  - backend/services/feature_engineering_service.py (inference-time
    per-race feature computation, wired in at Step 10)

This module is the single source of truth for the 14 Gonzo Sauce features.
NO duplication of computation logic between training and inference. Drift
here = silent calibration bugs (per session learning post-Bug #15 — three
distinct bugs this week traced to code-path drift between training and
inference).

Public API (3 functions):
  compute_gonzo_speed_features(horse_hist, row, workouts_by_horse, par_dict)
  compute_gonzo_trajectory_features(horse_hist, row)
  compute_gonzo_class_features(horse_hist, row)

Each returns a dict with the keys for its feature group:
  Speed (4):       speed_at_distance_recent_weighted, speed_at_distance_best_18mo,
                   noteworthy_workout_recent_14d, noteworthy_workout_count_30d
  Trajectory (7):  route_expand_count, route_held_count, route_erode_count,
                   route_collapse_count, route_charge_short_count,
                   route_avg_delta, is_stretching_out
  Class (3):       class_tier_at_today_level_count_18mo,
                   class_tier_in_money_rate_at_or_above,
                   class_tier_avg_position_at_or_above

Phase A3, 2026-05-01.
"""
from __future__ import annotations
from typing import Optional

import numpy as np
import pandas as pd


# ═══════════════════════════════════════════════════════════════════════
# Group A — Speed at distance + noteworthy workouts (4 features)
# ═══════════════════════════════════════════════════════════════════════
#
# Distance clusters:
#   today's race < 8F      → SPRINT cluster, match PPs in [5.0, 7.75]F
#   today's race ∈ [8.0, 8.5)F → MILE cluster, match PPs in [7.0, 9.0]F
#   today's race ≥ 8.5F    → ROUTE cluster, match PPs in [8.5, ∞)F
#
# Boundary: today's race at exactly 8.0F is MILE, not SPRINT.
# Sprint cluster is strict <8F.

SPRINT_PP_WINDOW = (5.0, 7.75)
MILE_PP_WINDOW = (7.0, 9.0)
ROUTE_PP_WINDOW = (8.5, float('inf'))

# Standard handicapping conversion: 1 length back ≈ 0.2 sec.
LENGTHS_PER_SEC = 0.2

# A1 recency-weighted: 180-day half-life (~6 months).
A1_DECAY_DAYS = 180.0

# A2 peak window.
A2_BEST_WINDOW_MONTHS = 18

# Improving-times pattern (A3 condition 3): 3+ workouts at the same
# distance within trailing 30d, with strictly monotonically improving
# (decreasing) times.
IMPROVING_PATTERN_MIN_COUNT = 3
IMPROVING_PATTERN_WINDOW_DAYS = 30

GONZO_SPEED_DEFAULTS = {
    'speed_at_distance_recent_weighted': None,  # None → NaN-imputed downstream
    'speed_at_distance_best_18mo': None,
    'noteworthy_workout_recent_14d': False,
    'noteworthy_workout_count_30d': 0,
}


# ═══════════════════════════════════════════════════════════════════════
# Group B — Trajectory features (7 features, route-only)
# ═══════════════════════════════════════════════════════════════════════
#
# delta = (finish_position - call_2_position) +
#         (lengths_behind_finish - call_2_lengths)
#
# Mixed units (positions + lengths) is intentional: combines "passed
# horses" + "gained ground" into a single late-pace trajectory signal.
# Negative delta = horse moved up; positive = lost ground.
#
# All features ROUTE-ONLY (today's distance ≥8.5F). Sprint races today
# get all defaults regardless of horse history.
#
# CHARGE_SHORT is independent of EXPAND/HELD/ERODE/COLLAPSE — a single PP
# can contribute to one bucket AND simultaneously be charge-short.

ROUTE_DISTANCE_FURLONGS = 8.5

TRAJECTORY_EXPAND_THRESHOLD = -1.5     # delta < -1.5 → EXPAND
TRAJECTORY_HELD_UPPER = 1.5            # -1.5 ≤ delta ≤ 1.5 → HELD
TRAJECTORY_ERODE_UPPER = 3.0           # 1.5 < delta ≤ 3.0 → ERODE
                                       # delta > 3.0 → COLLAPSE

CHARGE_SHORT_FINISH_LOW = 2
CHARGE_SHORT_FINISH_HIGH = 4

STRETCH_OUT_THRESHOLD_FURLONGS = 0.5   # B7: today_dist > median - 0.5 → True

GONZO_TRAJECTORY_DEFAULTS = {
    'route_expand_count': 0,
    'route_held_count': 0,
    'route_erode_count': 0,
    'route_collapse_count': 0,
    'route_charge_short_count': 0,
    'route_avg_delta': 0.0,
    'is_stretching_out': False,
}


# ═══════════════════════════════════════════════════════════════════════
# Group C — Class features (3 features) — uses 11-tier scale from
# model/shared/class_tiers.py (race_class_tier returns ordinal 1-11)
# ═══════════════════════════════════════════════════════════════════════

CLASS_FEATURE_WINDOW_MONTHS = 18

GONZO_CLASS_DEFAULTS = {
    'class_tier_at_today_level_count_18mo': 0,
    'class_tier_in_money_rate_at_or_above': 0.0,
    # C3 default = today's field_size; assigned per-row, not in this dict.
}


# ═══════════════════════════════════════════════════════════════════════
# Internal helpers (private — leading underscore, module-local)
# ═══════════════════════════════════════════════════════════════════════

def _safe_float(val, default: float) -> float:
    """Local copy. Avoids circular import from data_loader."""
    if val is None:
        return default
    try:
        f = float(val)
        if np.isnan(f):
            return default
        return f
    except (TypeError, ValueError):
        return default


def _distance_cluster(distance_furlongs: Optional[float]) -> Optional[str]:
    """Sprint/mile/route bucket for today's race distance."""
    if distance_furlongs is None:
        return None
    d = float(distance_furlongs)
    if d < 8.0:
        return 'sprint'
    if d < 8.5:
        return 'mile'
    return 'route'


def _eligible_pp_window(cluster: Optional[str]) -> Optional[tuple]:
    """(low, high) furlongs PP-eligibility window for a cluster."""
    if cluster == 'sprint':
        return SPRINT_PP_WINDOW
    if cluster == 'mile':
        return MILE_PP_WINDOW
    if cluster == 'route':
        return ROUTE_PP_WINDOW
    return None


def _effective_speed_fps(pp_row) -> Optional[float]:
    """
    Lengths-adjusted speed in feet/sec.
    formula: distance_feet / (final_time + lengths_behind * 0.2)
    Returns None if any required field is missing/invalid.
    """
    distance = pp_row.get('distance_furlongs')
    final_time = pp_row.get('final_time')
    lengths_behind = pp_row.get('lengths_behind')
    if lengths_behind is None:
        lengths_behind = 0.0  # winners have null lengths_behind
    if distance is None or final_time is None:
        return None
    try:
        d = float(distance)
        ft = float(final_time)
        lb = float(lengths_behind)
    except (TypeError, ValueError):
        return None
    if d <= 0 or ft <= 30:  # any race takes >30 seconds
        return None
    distance_feet = d * 660.0
    effective_time = ft + (lb * LENGTHS_PER_SEC)
    if effective_time <= 0:
        return None
    return distance_feet / effective_time


def _detect_improving_workout_pattern(
    horse_workouts: pd.DataFrame,
    race_date: pd.Timestamp,
) -> bool:
    """
    True if horse has 3+ workouts at the SAME distance in trailing 30d
    (before race_date) with strictly monotonically improving (decreasing)
    times. Gate works excluded — they're training-behavior, not speed.
    """
    if horse_workouts is None or horse_workouts.empty:
        return False
    cutoff = race_date - pd.Timedelta(days=IMPROVING_PATTERN_WINDOW_DAYS)
    recent = horse_workouts[
        (horse_workouts['workout_date'] >= cutoff) &
        (horse_workouts['workout_date'] < race_date) &
        (horse_workouts['workout_time'].notna()) &
        (horse_workouts['workout_time'] > 0) &
        (~horse_workouts.get('is_gate_work', False))
    ]
    if len(recent) < IMPROVING_PATTERN_MIN_COUNT:
        return False
    recent = recent.copy()
    recent['dist_round'] = recent['distance_furlongs'].astype(float).round(1)
    for _dist, group in recent.groupby('dist_round'):
        if len(group) < IMPROVING_PATTERN_MIN_COUNT:
            continue
        sorted_group = group.sort_values('workout_date', ascending=True)
        times = sorted_group['workout_time'].astype(float).values
        if all(times[i] < times[i - 1] for i in range(1, len(times))):
            return True
    return False


def _compute_pp_trajectory_delta(pp_row) -> Optional[float]:
    """
    delta = (finish_position - call_2_position) +
            (lengths_behind_finish - call_2_lengths)
    Returns None if any required field is missing/invalid.
    """
    fp = pp_row.get('finish_position')
    c2p = pp_row.get('call_2_position')
    lb = pp_row.get('lengths_behind')
    c2l = pp_row.get('call_2_lengths')
    if fp is None or c2p is None or lb is None or c2l is None:
        return None
    try:
        return (float(fp) - float(c2p)) + (float(lb) - float(c2l))
    except (TypeError, ValueError):
        return None


def _classify_trajectory_bucket(delta: float) -> str:
    """Map delta to one of 4 mutually-exclusive buckets."""
    if delta < TRAJECTORY_EXPAND_THRESHOLD:
        return 'expand'
    if delta <= TRAJECTORY_HELD_UPPER:
        return 'held'
    if delta <= TRAJECTORY_ERODE_UPPER:
        return 'erode'
    return 'collapse'


def _is_charge_short(pp_row) -> bool:
    """
    True if horse was closing through the final turn but ran out of track:
      call_3_position < call_2_position
      AND call_3_lengths < call_2_lengths
      AND 2 ≤ finish_position ≤ 4

    Returns False (not None) if call_3 data is absent — don't default-flag.
    """
    fp = pp_row.get('finish_position')
    c2p = pp_row.get('call_2_position')
    c2l = pp_row.get('call_2_lengths')
    c3p = pp_row.get('call_3_position')
    c3l = pp_row.get('call_3_lengths')
    if (fp is None or c2p is None or c2l is None
            or c3p is None or c3l is None):
        return False
    try:
        finish = float(fp)
        if not (CHARGE_SHORT_FINISH_LOW <= finish <= CHARGE_SHORT_FINISH_HIGH):
            return False
        return (float(c3p) < float(c2p)) and (float(c3l) < float(c2l))
    except (TypeError, ValueError):
        return False


# ═══════════════════════════════════════════════════════════════════════
# Public API — 3 main feature-computation functions
# ═══════════════════════════════════════════════════════════════════════

def compute_gonzo_speed_features(
    horse_hist: pd.DataFrame,
    row: pd.Series,
    workouts_by_horse: dict,
    par_dict: dict,
) -> dict:
    """
    Group A — 4 speed features for the Gonzo Sauce specialist.

    A1: speed_at_distance_recent_weighted — 180-day half-life weighted
        mean of effective_speed_fps across last 5 PPs in distance cluster
    A2: speed_at_distance_best_18mo — peak effective_speed_fps in 18-month
        window within distance cluster
    A3: noteworthy_workout_recent_14d — bool: any par-noteworthy in 14d
        OR improving-times pattern in trailing 30d
    A4: noteworthy_workout_count_30d — count of par-noteworthy in 30d
        (improving-times pattern is horse-level, contributes only to A3)

    Surface-agnostic (mixes dirt/turf at same distance) per brief V1.
    """
    # Lazy-import to avoid circular at module load; par_times is a sibling
    # module. Relative import works in BOTH contexts (training: model/ on
    # sys.path; inference: model.shared.X path with /app on PYTHONPATH).
    from .par_times import is_noteworthy_workout

    out = dict(GONZO_SPEED_DEFAULTS)
    today_date = row['race_date']
    today_distance = row.get('distance_furlongs')
    cluster = _distance_cluster(today_distance)
    window = _eligible_pp_window(cluster)

    # ─── A1, A2: speed at distance ────────────────────────────────────
    if window is not None and not horse_hist.empty:
        prior = horse_hist[horse_hist['race_date'] < today_date]
        eligible = prior[
            (prior['distance_furlongs'].astype(float) >= window[0]) &
            (prior['distance_furlongs'].astype(float) <= window[1])
        ]
        if not eligible.empty:
            # A1: last 5 PPs in cluster, exponential decay weighted mean
            last5 = eligible.sort_values(
                'race_date', ascending=False
            ).head(5)
            speeds = []
            weights = []
            for _, pp in last5.iterrows():
                fps = _effective_speed_fps(pp)
                if fps is None:
                    continue
                days_ago = (today_date - pp['race_date']).days
                w = float(np.exp(-days_ago / A1_DECAY_DAYS))
                speeds.append(fps)
                weights.append(w)
            if speeds:
                out['speed_at_distance_recent_weighted'] = float(
                    np.average(speeds, weights=weights)
                )

            # A2: peak fps within last 18 months
            cutoff_18mo = today_date - pd.DateOffset(
                months=A2_BEST_WINDOW_MONTHS
            )
            eligible_18 = eligible[eligible['race_date'] >= cutoff_18mo]
            if not eligible_18.empty:
                peak_speeds = [
                    _effective_speed_fps(pp)
                    for _, pp in eligible_18.iterrows()
                ]
                peak_speeds = [s for s in peak_speeds if s is not None]
                if peak_speeds:
                    out['speed_at_distance_best_18mo'] = float(
                        max(peak_speeds)
                    )

    # ─── A3, A4: noteworthy workouts ──────────────────────────────────
    horse_id = str(row['horse_id'])
    horse_w = workouts_by_horse.get(horse_id)
    if horse_w is None or horse_w.empty:
        return out

    horse_w = horse_w[horse_w['workout_date'] < today_date]
    if horse_w.empty:
        return out

    cutoff_14 = today_date - pd.Timedelta(days=14)
    cutoff_30 = today_date - pd.Timedelta(days=30)
    w14 = horse_w[horse_w['workout_date'] >= cutoff_14]
    w30 = horse_w[horse_w['workout_date'] >= cutoff_30]

    # A3: any par-noteworthy in 14d OR improving-times pattern in 30d
    has_a3 = False
    for _, w in w14.iterrows():
        if is_noteworthy_workout(w.to_dict(), par_dict):
            has_a3 = True
            break
    if not has_a3:
        if _detect_improving_workout_pattern(w30, today_date):
            has_a3 = True
    out['noteworthy_workout_recent_14d'] = bool(has_a3)

    # A4: count of par-noteworthy workouts in 30d (pattern excluded — A3 only)
    count = 0
    for _, w in w30.iterrows():
        if is_noteworthy_workout(w.to_dict(), par_dict):
            count += 1
    out['noteworthy_workout_count_30d'] = int(count)

    return out


def compute_gonzo_trajectory_features(
    horse_hist: pd.DataFrame,
    row: pd.Series,
) -> dict:
    """
    Group B — 7 trajectory features for the Gonzo Sauce specialist.

    B1: route_expand_count       (0-5)
    B2: route_held_count         (0-5)
    B3: route_erode_count        (0-5)
    B4: route_collapse_count     (0-5)
    B5: route_charge_short_count (0-5, independent of B1-B4)
    B6: route_avg_delta          (float, default 0.0)
    B7: is_stretching_out        (bool, default False)

    ROUTE-ONLY (today's distance ≥8.5F). Sprint races today return all
    defaults — V1 design choice; trajectory is a route-handicapping
    signal. Buckets sum to actual count of route PPs (cap 5), don't pad
    to 5 with synthetic zeros.
    """
    out = dict(GONZO_TRAJECTORY_DEFAULTS)
    today_date = row['race_date']
    today_distance = row.get('distance_furlongs')

    if today_distance is None:
        return out
    if float(today_distance) < ROUTE_DISTANCE_FURLONGS:
        return out  # Sprint today → trajectory is not a signal

    if horse_hist.empty:
        return out

    prior = horse_hist[horse_hist['race_date'] < today_date].sort_values(
        'race_date', ascending=False
    )
    if prior.empty:
        return out

    # B7: is_stretching_out — uses last 5 PPs at ANY distance
    last5_any = prior.head(5)
    if not last5_any.empty:
        try:
            median_dist = float(
                last5_any['distance_furlongs'].astype(float).median()
            )
            out['is_stretching_out'] = bool(
                float(today_distance) - median_dist
                >= STRETCH_OUT_THRESHOLD_FURLONGS
            )
        except (TypeError, ValueError):
            pass

    # B1-B6: last 5 ROUTE PPs only
    route_pps = prior[
        prior['distance_furlongs'].astype(float) >= ROUTE_DISTANCE_FURLONGS
    ]
    last5_route = route_pps.head(5)
    if last5_route.empty:
        return out

    deltas = []
    for _, pp in last5_route.iterrows():
        delta = _compute_pp_trajectory_delta(pp)
        if delta is not None:
            deltas.append(delta)
            bucket = _classify_trajectory_bucket(delta)
            out[f'route_{bucket}_count'] += 1
        # CHARGE_SHORT is independent of bucket assignment; check separately
        if _is_charge_short(pp):
            out['route_charge_short_count'] += 1

    if deltas:
        out['route_avg_delta'] = float(np.mean(deltas))

    return out


def compute_gonzo_class_features(
    horse_hist: pd.DataFrame,
    row: pd.Series,
) -> dict:
    """
    Group C — 3 class features for the Gonzo Sauce specialist.

    Uses the existing 11-tier scale from model/shared/class_tiers.py.
    "Today's tier" = race_class_tier(today's race_type, today's grade).
    "At or above" = pp_tier >= today_tier comparison.

    C1: class_tier_at_today_level_count_18mo (int)
        Count of prior races at EXACTLY today's tier in last 18 months.

    C2: class_tier_in_money_rate_at_or_above (float)
        Fraction of prior races at tier ≥ today_tier where horse finished
        top 3 (in the money). 0.0 if no eligible prior races.

    C3: class_tier_avg_position_at_or_above (float)
        Average finish_position across prior races at tier ≥ today_tier.
        Default = today's field_size (signals "no data; treat as bottom").

    DNF/scratched PPs: pp.finish_position IS NULL is filtered at load
    time in _load_raw_pps (WHERE pp.finish_position IS NOT NULL AND
    pp.finish_position < 90), so horse_hist never sees them.
    """
    # Relative import — same dual-context reasoning as par_times above.
    from .class_tiers import race_class_tier

    today_field_size = float(_safe_float(row.get('field_size'), 8.0))
    out = dict(GONZO_CLASS_DEFAULTS)
    out['class_tier_avg_position_at_or_above'] = today_field_size

    today_tier = race_class_tier(
        row.get('race_type'),
        row.get('claiming_price_entered'),
        row.get('purse'),
        row.get('grade'),
    )
    if today_tier is None:
        return out  # Today's tier unclassifiable; can't compute.

    if horse_hist.empty:
        return out

    today_date = row['race_date']
    cutoff_18mo = today_date - pd.DateOffset(months=CLASS_FEATURE_WINDOW_MONTHS)
    prior = horse_hist[
        (horse_hist['race_date'] < today_date) &
        (horse_hist['race_date'] >= cutoff_18mo)
    ]
    if prior.empty:
        return out

    # Compute pp_tier per prior race; skip foreign/unclassifiable.
    pp_tiers = []
    pp_finishes = []
    for _, pp in prior.iterrows():
        pp_tier = race_class_tier(
            pp.get('race_type'),
            pp.get('claiming_price_entered'),
            pp.get('purse'),
            pp.get('grade'),
        )
        if pp_tier is None:
            continue
        pp_tiers.append(pp_tier)
        pp_finishes.append(pp.get('finish_position'))

    if not pp_tiers:
        return out

    # C1: count at exactly today's tier
    out['class_tier_at_today_level_count_18mo'] = int(
        sum(1 for t in pp_tiers if t == today_tier)
    )

    # C2 + C3: at or above today's tier
    at_or_above_finishes = [
        pp_finishes[i]
        for i, t in enumerate(pp_tiers)
        if t >= today_tier and pp_finishes[i] is not None
    ]
    if at_or_above_finishes:
        in_money = sum(1 for f in at_or_above_finishes if int(f) <= 3)
        out['class_tier_in_money_rate_at_or_above'] = float(
            in_money / len(at_or_above_finishes)
        )
        out['class_tier_avg_position_at_or_above'] = float(
            np.mean([int(f) for f in at_or_above_finishes])
        )

    return out
