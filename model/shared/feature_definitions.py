from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class FeatureDef:
    name: str
    group: str
    derived: bool          # True = computed from history, False = direct DB column
    default_value: float
    requires_odds: bool = False
    requires_workouts: bool = False

FEATURE_DEFS = [
    # ── Speed (11) ──────────────────────────────────────
    FeatureDef('speed_fig_last',          'speed', True,  0.0),
    FeatureDef('speed_fig_avg_3',         'speed', True,  0.0),
    FeatureDef('speed_fig_trend',         'speed', True,  0.0),
    FeatureDef('speed_fig_best_career',   'speed', True,  0.0),
    FeatureDef('speed_fig_best_90d',      'speed', True,  0.0),
    FeatureDef('speed_fig_at_track',      'speed', True,  0.0),
    FeatureDef('speed_fig_at_distance',   'speed', True,  0.0),
    FeatureDef('speed_fig_on_surface',    'speed', True,  0.0),
    FeatureDef('speed_fig_vs_field',      'speed', True,  0.0),
    FeatureDef('speed_fig_consistency',   'speed', True,  5.0),
    FeatureDef('speed_fig_sample_size',   'speed', True,  0.0),

    # ── Pace (6) ─────────────────────────────────────────
    FeatureDef('early_pace_last',         'pace',  True,  24.0),
    FeatureDef('late_pace_last',          'pace',  True,  38.0),
    FeatureDef('pace_delta_last',         'pace',  True,  14.0),
    FeatureDef('avg_call1_position',      'pace',  True,  5.0),
    FeatureDef('avg_stretch_gain',        'pace',  True,  0.0),
    FeatureDef('pace_scenario_today',     'pace',  True,  2.0),

    # ── Trip (8) ─────────────────────────────────────────
    FeatureDef('troubled_trip_last',      'trip',  True,  0.0),
    FeatureDef('troubled_trip_freq',      'trip',  True,  0.0),
    FeatureDef('pace_setter_freq',        'trip',  True,  0.0),
    FeatureDef('faded_freq',              'trip',  True,  0.0),
    FeatureDef('late_rally_freq',         'trip',  True,  0.0),
    FeatureDef('avg_wide_path',           'trip',  True,  0.0),
    FeatureDef('wide_3plus_freq',         'trip',  True,  0.0),
    FeatureDef('gate_issue_freq',         'trip',  True,  0.0),

    # ── Trainer (5) ──────────────────────────────────────
    FeatureDef('trainer_win_rate',        'trainer', False, 0.10),
    FeatureDef('trainer_itm_rate',        'trainer', False, 0.30),
    FeatureDef('trainer_layoff_win_rate', 'trainer', False, 0.08),
    FeatureDef('trainer_lasix_win_rate',  'trainer', False, 0.12),
    FeatureDef('trainer_sample_size',     'trainer', False, 0.0),

    # ── Workout (8) ──────────────────────────────────────
    FeatureDef('days_since_last_workout',    'workout', True, 30.0, requires_workouts=True),
    FeatureDef('workout_count_30d',          'workout', True, 0.0,  requires_workouts=True),
    FeatureDef('bullet_work_14d',            'workout', True, 0.0,  requires_workouts=True),
    FeatureDef('bullet_count_30d',           'workout', True, 0.0,  requires_workouts=True),
    FeatureDef('best_workout_speed_index',   'workout', True, 0.5,  requires_workouts=True),
    FeatureDef('workout_speed_trend',        'workout', True, 0.0,  requires_workouts=True),
    FeatureDef('gate_work_30d',              'workout', True, 0.0,  requires_workouts=True),
    FeatureDef('workout_frequency_score',    'workout', True, 0.0,  requires_workouts=True),

    # ── Class (7) ────────────────────────────────────────
    FeatureDef('class_direction',            'class',   True, 0.0),
    FeatureDef('purse_change_pct',           'class',   True, 0.0),
    FeatureDef('claiming_price_change_pct',  'class',   True, 0.0),
    FeatureDef('career_class_ceiling',       'class',   True, 0.0),
    FeatureDef('current_vs_ceiling_pct',     'class',   True, 1.0),
    FeatureDef('class_consistency',          'class',   True, 0.0),
    FeatureDef('race_quality_tier',          'class',   False, 2.0),

    # ── Physical (10) ────────────────────────────────────
    FeatureDef('days_since_last_race',       'physical', True,  30.0),
    FeatureDef('layoff_bucket',              'physical', True,  2.0),
    FeatureDef('career_starts',              'physical', True,  0.0),
    FeatureDef('is_first_start',             'physical', True,  0.0),
    FeatureDef('first_time_on_surface',      'physical', True,  0.0),
    FeatureDef('was_claimed_last_out',       'physical', True,  0.0),
    FeatureDef('weight_carried',             'physical', False, 118.0),
    FeatureDef('apprentice_allowance',       'physical', False, 0.0),
    FeatureDef('win_rate_this_track',        'physical', True,  0.0),
    FeatureDef('overall_win_rate',           'physical', True,  0.0),

    # ── Equipment (5) ────────────────────────────────────
    FeatureDef('lasix',                      'equipment', False, 0.0),
    FeatureDef('lasix_first_time',           'equipment', False, 0.0),
    FeatureDef('blinkers_on',                'equipment', False, 0.0),
    FeatureDef('blinkers_off',               'equipment', False, 0.0),
    FeatureDef('trainer_intent_score',       'equipment', True,  0.0),

    # ── Odds (3) — excluded from v_base, included in v_odds ──
    FeatureDef('closing_odds',               'odds', False, 5.0,  requires_odds=True),
    FeatureDef('log_closing_odds',           'odds', True,  1.6,  requires_odds=True),
    FeatureDef('odds_move',                  'odds', True,  0.0,  requires_odds=True),

    # ── Jockey (3) ───────────────────────────────────────
    FeatureDef('jockey_win_rate',            'jockey', True, 0.10),
    FeatureDef('jockey_trainer_combo_win_rate','jockey', True, 0.10),
    FeatureDef('jockey_change_flag',         'jockey', True, 0.0),

    # ── Phase B Tier 1 Top-5 (5) — Decision 2 ratified 2026-05-16 ──
    FeatureDef('surface_win_rate',           'phase_b_top5', True,  0.0),
    FeatureDef('pace_pressure_score',        'phase_b_top5', True,  0.0),
    FeatureDef('class_drop_flag',            'phase_b_top5', True, -1.0),
    FeatureDef('shipped_from_flag',          'phase_b_top5', True, -1.0),
    FeatureDef('layoff_off_bucket',          'phase_b_top5', True, -1.0),
]

assert len(FEATURE_DEFS) == 71, f"Expected 71 features (66 base + 5 Phase B Top-5), got {len(FEATURE_DEFS)}"
assert len({f.name for f in FEATURE_DEFS}) == 71, "Duplicate feature names detected"


def get_feature_names(include_odds: bool = True) -> list[str]:
    return [f.name for f in FEATURE_DEFS if include_odds or not f.requires_odds]

def get_odds_blind_features() -> list[str]:
    result = get_feature_names(include_odds=False)
    assert len(result) == 68, f"Expected 68 odds-blind features (63 base + 5 Phase B Top-5), got {len(result)}"
    return result

def get_odds_aware_features() -> list[str]:
    result = get_feature_names(include_odds=True)
    assert len(result) == 71, f"Expected 71 odds-aware features (66 base + 5 Phase B Top-5), got {len(result)}"
    return result

def get_feature_defaults() -> dict[str, float]:
    return {f.name: f.default_value for f in FEATURE_DEFS}

def get_feature_groups() -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for f in FEATURE_DEFS:
        groups.setdefault(f.group, []).append(f.name)
    return groups


def get_core_features(include_odds: bool = True) -> list[str]:
    """Core features excluding workouts (58 or 55)."""
    return [f.name for f in FEATURE_DEFS
            if not f.requires_workouts
            and (include_odds or not f.requires_odds)]


def get_workout_features() -> list[str]:
    """The 8 workout features."""
    return [f.name for f in FEATURE_DEFS if f.requires_workouts]


# ─────────────────────────────────────────────────────────────────────
# Phase 1 (2026-04-28) lean51 ranker cull — applied to ranker_full ONLY.
# Both training (model/ranker/train.py) and inference
# (backend/services/wr_inference_service.py) import RANKER_FULL_CULL and
# get_ranker_full_features() from here so the schemas can never drift.
#
# Rationale: ablation on April 15-26 holdout showed dropping these 15
# features improves rk_full top-1 +3.6pp, top-3 +4.4pp, NDCG +0.024,
# ROI +10.6pp. Paired-race disagreements: 30 vs 18 favoring lean.
# Other models (wp_full, pl, ls, longshot_rf, etc.) keep all 66 features.
# ─────────────────────────────────────────────────────────────────────
RANKER_FULL_CULL: tuple[str, ...] = (
    # Tier 1: zero-variance / zero-gain (9)
    "apprentice_allowance", "blinkers_off", "gate_work_30d",
    "jockey_change_flag", "jockey_trainer_combo_win_rate", "jockey_win_rate",
    "pace_scenario_today", "was_claimed_last_out", "is_first_start",
    # Tier 2 #10: r=1.000 duplicate of workout_count_30d
    "workout_frequency_score",
    # Ablation cull (5): low-gain + ablation-validated as redundant
    "wide_3plus_freq", "bullet_count_30d", "troubled_trip_last",
    "workout_speed_trend", "blinkers_on",
)


def get_ranker_full_features() -> list[str]:
    """51-feature list for the lean51 ranker_full model.
    Equal to get_odds_aware_features() minus RANKER_FULL_CULL."""
    return [f for f in get_odds_aware_features() if f not in RANKER_FULL_CULL]


# ─────────────────────────────────────────────────────────────────────
# Stream A2 (2026-04-30) lean53 cull — applied to all lean53 retrains
# (wp_full, rk_full, pl_core × 7 styles = 21 artifacts).
#
# Architectural intent: model only sees performance features. Market
# signal (odds) is computed at inference time as a separate market_prob
# and combined via a blended displayed_prob with tunable weight. This
# mirrors Tony's two-pass handicapping methodology — handicap first
# (form only), then check market as overlay.
#
# Cull breakdown (13 features dropped from 66):
#   - 3 odds-derived (closing_odds, log_closing_odds, odds_move)
#   - 9 zero-gain per importance audit
#   - 1 r=1.000 duplicate (workout_frequency_score ≡ workout_count_30d)
# ─────────────────────────────────────────────────────────────────────
LEAN53_CULL: tuple[str, ...] = (
    # Odds / market-derived (3)
    "closing_odds", "log_closing_odds", "odds_move",
    # Zero-gain per importance audit (9)
    "pace_scenario_today", "gate_work_30d", "is_first_start",
    "was_claimed_last_out", "apprentice_allowance", "blinkers_off",
    "jockey_win_rate", "jockey_trainer_combo_win_rate", "jockey_change_flag",
    # r=1.000 duplicate of workout_count_30d (1)
    "workout_frequency_score",
    # ── Phase B Top-5 (5) — added 2026-05-16 Decision 2 ──
    # Excluded from lean53 to preserve existing 53/47 model invariants.
    # Phase 3 retraining explicitly uses get_lean53_plus_top5_features()
    # (58/52) so new models pick up phase_b_top5 signal while existing
    # lean53 models continue working.
    "surface_win_rate", "pace_pressure_score", "class_drop_flag",
    "shipped_from_flag", "layoff_off_bucket",
)


def get_lean53_features() -> list[str]:
    """53-feature list for lean53 wp_full and rk_full models.
    Equal to get_odds_aware_features() minus LEAN53_CULL."""
    result = [f for f in get_odds_aware_features() if f not in LEAN53_CULL]
    assert len(result) == 53, f"Expected 53 lean features, got {len(result)}"
    return result


def get_lean53_core_features() -> list[str]:
    """47-feature list for lean53 pl_core models (no workouts).
    Equal to get_core_features(include_odds=True) minus LEAN53_CULL."""
    result = [f for f in get_core_features(include_odds=True)
              if f not in LEAN53_CULL]
    assert len(result) == 47, f"Expected 47 lean core features, got {len(result)}"
    return result


# ─────────────────────────────────────────────────────────────────────
# Phase B Tier 1 (2026-05-16) — Top-5 substrate-recoverable features
# Decision 2 ratified. Phase 3 retraining uses get_lean53_plus_top5_*
# getters so new models include phase_b_top5 signal; existing lean53
# models continue working off get_lean53_features() (53 / 47 unchanged).
# ─────────────────────────────────────────────────────────────────────
PHASE_B_TOP5_NAMES: tuple[str, ...] = (
    "surface_win_rate", "pace_pressure_score", "class_drop_flag",
    "shipped_from_flag", "layoff_off_bucket",
)


def get_lean53_plus_top5_features() -> list[str]:
    """58-feature list for Phase 3 retrain wp_full / rk_full models."""
    result = get_lean53_features() + list(PHASE_B_TOP5_NAMES)
    assert len(result) == 58, f"Expected 58 (53+5), got {len(result)}"
    return result


def get_lean53_core_plus_top5_features() -> list[str]:
    """52-feature list for Phase 3 retrain pl_core / win_prob_core models."""
    result = get_lean53_core_features() + list(PHASE_B_TOP5_NAMES)
    assert len(result) == 52, f"Expected 52 (47+5), got {len(result)}"
    return result


def get_gonzo_sauce_plus_top5_features() -> list[str]:
    """72-feature list for Phase 3 retrain gonzo_sauce model."""
    result = get_lean53_plus_top5_features() + [f.name for f in GONZO_FEATURE_DEFS]
    assert len(result) == 72, f"Expected 72 (58+14), got {len(result)}"
    return result


# ─────────────────────────────────────────────────────────────────────
# Phase A3 (2026-05-01) — Gonzo Sauce specialist features.
# 14 new features encoding Tony's two-pass handicapping methodology:
#   speed at distance (4), trajectory routes-only (7), class established (3).
# Kept SEPARATE from FEATURE_DEFS so the existing 66-feature contracts
# (and their assertions) stay stable. The gonzo_sauce model trains on
# lean53 base (53) + these 14 = 67 features total.
# Computed by _compute_gonzo_*_features() in model/shared/data_loader.py.
# ─────────────────────────────────────────────────────────────────────
GONZO_FEATURE_DEFS = [
    # ── Group A: Speed at distance + noteworthy workouts (4) ──
    FeatureDef('speed_at_distance_recent_weighted', 'gonzo_speed', True,
               float('nan')),
    FeatureDef('speed_at_distance_best_18mo',       'gonzo_speed', True,
               float('nan')),
    FeatureDef('noteworthy_workout_recent_14d',     'gonzo_speed', True,
               0.0, requires_workouts=True),
    FeatureDef('noteworthy_workout_count_30d',      'gonzo_speed', True,
               0.0, requires_workouts=True),

    # ── Group B: Trajectory (route-only; sprint-today returns defaults) (7) ──
    FeatureDef('route_expand_count',         'gonzo_trajectory', True, 0.0),
    FeatureDef('route_held_count',           'gonzo_trajectory', True, 0.0),
    FeatureDef('route_erode_count',          'gonzo_trajectory', True, 0.0),
    FeatureDef('route_collapse_count',       'gonzo_trajectory', True, 0.0),
    FeatureDef('route_charge_short_count',   'gonzo_trajectory', True, 0.0),
    FeatureDef('route_avg_delta',            'gonzo_trajectory', True, 0.0),
    FeatureDef('is_stretching_out',          'gonzo_trajectory', True, 0.0),

    # ── Group C: Class established (3) — uses 11-tier scale from class_tiers.py ──
    FeatureDef('class_tier_at_today_level_count_18mo', 'gonzo_class', True, 0.0),
    FeatureDef('class_tier_in_money_rate_at_or_above', 'gonzo_class', True, 0.0),
    FeatureDef('class_tier_avg_position_at_or_above',  'gonzo_class', True, 8.0),
]
assert len(GONZO_FEATURE_DEFS) == 14, (
    f"Expected 14 Gonzo features, got {len(GONZO_FEATURE_DEFS)}"
)
assert len({f.name for f in GONZO_FEATURE_DEFS}) == 14, (
    "Duplicate Gonzo feature names detected"
)


def get_gonzo_sauce_features() -> list[str]:
    """67-feature list = lean53 base + 14 Gonzo Sauce features."""
    result = get_lean53_features() + [f.name for f in GONZO_FEATURE_DEFS]
    assert len(result) == 67, f"Expected 67 gonzo features, got {len(result)}"
    return result


# ─────────────────────────────────────────────────────────────────────
# Gate 3 (2026-05-21) — LSTM trajectory feature
# Defined separately from FEATURE_DEFS / GONZO_FEATURE_DEFS so the
# existing 71-feature / 14-Gonzo invariants stay intact. Default is NaN
# (not 0.0) — the dispatch's explicit-sentinel directive: a real score
# of 0.0 means "model says no trend"; NaN means "no history to score".
# XGBoost handles NaN natively as a missing-value split.
# ─────────────────────────────────────────────────────────────────────
TRAJECTORY_FEATURE_DEFS = [
    FeatureDef('trajectory_score', 'trajectory', True, float('nan')),
]
assert len(TRAJECTORY_FEATURE_DEFS) == 1


def get_lean53_plus_top5_plus_trajectory_features() -> list[str]:
    """59-feature list for Gate 3 retrain wp_full / rk_full models
    (lean53+top5 = 58, plus trajectory_score = 59)."""
    result = get_lean53_plus_top5_features() + [f.name for f in TRAJECTORY_FEATURE_DEFS]
    assert len(result) == 59, f"Expected 59 (58+1), got {len(result)}"
    return result


def get_lean53_core_plus_top5_plus_trajectory_features() -> list[str]:
    """53-feature list for Gate 3 retrain pl_core / win_prob_core models
    (lean53_core+top5 = 52, plus trajectory_score = 53)."""
    result = get_lean53_core_plus_top5_features() + [f.name for f in TRAJECTORY_FEATURE_DEFS]
    assert len(result) == 53, f"Expected 53 (52+1), got {len(result)}"
    return result


def get_gonzo_sauce_plus_top5_plus_trajectory_features() -> list[str]:
    """73-feature list for Gate 3 retrain gonzo_sauce (72 + 1)."""
    result = get_gonzo_sauce_plus_top5_features() + [f.name for f in TRAJECTORY_FEATURE_DEFS]
    assert len(result) == 73, f"Expected 73 (72+1), got {len(result)}"
    return result


def get_all_feature_defaults() -> dict[str, float]:
    """All defaults including Gonzo + trajectory features. Used by
    data_loader's row loop so any feature missing from a row's dict gets
    a default rather than KeyError."""
    result = {f.name: f.default_value for f in FEATURE_DEFS}
    result.update({f.name: f.default_value for f in GONZO_FEATURE_DEFS})
    result.update({f.name: f.default_value for f in TRAJECTORY_FEATURE_DEFS})
    return result


if __name__ == '__main__':
    print(f"Total features:       {len(FEATURE_DEFS)}")
    print(f"Odds-blind features:  {len(get_odds_blind_features())}")
    print(f"Odds-aware features:  {len(get_odds_aware_features())}")
    print(f"Ranker-full lean51:   {len(get_ranker_full_features())}")
    print(f"Lean53 (wp + rk):     {len(get_lean53_features())}")
    print(f"Lean53 core (pl):     {len(get_lean53_core_features())}")
    print(f"Core (odds-aware):    {len(get_core_features(include_odds=True))}")
    print(f"Core (odds-blind):    {len(get_core_features(include_odds=False))}")
    print(f"Workout features:     {len(get_workout_features())}")
    print()
    for group, names in get_feature_groups().items():
        print(f"  {group:12s}: {len(names):2d}  {names}")
