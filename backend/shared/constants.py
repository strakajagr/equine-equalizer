QUALIFYING_TRACKS = [
    'CD', 'SAR', 'KEE', 'BEL', 'SA',
    'GP', 'DMR', 'OP', 'MTH', 'AQU', 'PIM'
]

HRN_SLUG_TO_TRACK_CODE = {
    'churchill-downs': 'CD',
    'saratoga': 'SAR',
    'keeneland': 'KEE',
    'belmont-park': 'BEL',
    'belmont-at-aqueduct': 'BEL',
    'belmont-at-the-big-a': 'BEL',
    'santa-anita-park': 'SA',
    'gulfstream-park': 'GP',
    'del-mar': 'DMR',
    'oaklawn-park': 'OP',
    'monmouth-park': 'MTH',
    'aqueduct': 'AQU',
    'pimlico': 'PIM',
}

MIN_CLAIMING_PRICE = 15000

QUALIFYING_RACE_TYPES = [
    'allowance',
    'allowance_optional_claiming',
    'stakes',
    'graded_stakes'
]
# Claiming races included only if claiming_price >= MIN_CLAIMING_PRICE


def is_qualifying_race_type(
    race_type: str, claiming_price: int = 0
) -> bool:
    """True if race_type qualifies for prediction generation.
    Mirrors the SQL filter in
    race_repository.get_qualifying_races_by_date().
    """
    if race_type in QUALIFYING_RACE_TYPES:
        return True
    if (race_type == 'claiming'
            and (claiming_price or 0) >= MIN_CLAIMING_PRICE):
        return True
    return False

SURFACES = ['dirt', 'turf', 'synthetic', 'wet_dirt']

RACE_TYPES = [
    'maiden',
    'maiden_claiming',
    'claiming',
    'allowance',
    'allowance_optional_claiming',
    'stakes',
    'graded_stakes'
]

# Race quality tier classification.
# Used as feature 73 in the model.
# Lower number = higher quality race.
# Model learns that same speed figure means
# different things at different quality levels.
RACE_QUALITY_TIERS = {
    'graded_stakes':              1,
    'stakes':                     2,
    'allowance':                  3,
    'allowance_optional_claiming': 3,
    'claiming_high':              4,  # $25k+
    'claiming_mid':               5,  # $15-25k
    'maiden':                     6,
    'maiden_claiming':            7,
}

TRACK_CONDITIONS_DIRT = [
    'fast', 'good', 'sloppy', 'muddy',
    'heavy', 'sealed'
]

TRACK_CONDITIONS_TURF = [
    'firm', 'good', 'soft', 'yielding', 'heavy'
]

PP_LOOKBACK_STARTS = 10

WORKOUT_LOOKBACK_DAYS = 45

FEATURE_COUNT = 73

MODEL_ARTIFACTS_PREFIX = 'models/'

# Par times in seconds per furlong by distance.
# Used for raw_speed_vs_par computation.
# Lower = faster. These are approximate industry
# averages and will be refined from training data.
RAW_SPEED_PAR_TIMES = {
    4.0:  11.40,
    4.5:  11.45,
    5.0:  11.50,
    5.5:  11.55,
    6.0:  11.60,
    6.5:  11.65,
    7.0:  11.75,
    7.5:  11.80,
    8.0:  12.00,   # 1 mile
    8.5:  12.10,
    9.0:  12.20,
    9.5:  12.30,
    10.0: 12.40,   # 1.25 miles
    12.0: 12.60    # 1.5 miles
}

# Running style classification thresholds.
# Based on average first-call position across last 5 starts.
RUNNING_STYLE_THRESHOLDS = {
    'front_runner': 2.0,   # avg call_1 <= 2.0
    'presser':      4.0,   # avg call_1 <= 4.0
    'midpack':      6.0,   # avg call_1 <= 6.0
    'closer':       99.0   # avg call_1 > 6.0
}

# Layoff classification in days
LAYOFF_BUCKETS = {
    'short':     (0,   14),
    'normal':    (15,  45),
    'freshened': (46,  90),
    'extended':  (91,  180),
    'long':      (181, 9999)
}

# Pace scenario classification.
# Based on number of front runners in field
# (horses with running_style = 'front_runner')
PACE_SCENARIO_THRESHOLDS = {
    'lone_speed': 1,   # 1 front runner
    'contested':  2,   # 2 front runners
    'fast_duel':  3,   # 3+ front runners
    'slow':       0    # no front runners (all closers)
}

# Minimum data requirements for model features.
# If a horse has fewer starts than this, use field average as fallback.
MIN_STARTS_FOR_SPEED_TREND = 3
MIN_STARTS_FOR_STYLE = 3

# Overlay threshold.
# If model win_probability exceeds morning line implied probability
# by this margin, flag as value play.
OVERLAY_THRESHOLD = 0.15

# P&L model constants
BANKROLL = 1000.0
KELLY_FRACTION = 0.5           # half-Kelly
MAX_BET_PCT = 0.10             # max 10% of bankroll per bet
MIN_EDGE_TO_BET = 0.05         # minimum edge to place a bet
STRONG_VALUE_THRESHOLD = 0.10  # edge for "strong value" flag

# LS model constants
LONGSHOT_ODDS_FLOOR = 10.0     # minimum odds to qualify as longshot (10-1+)
LONGSHOT_ALERT_EDGE = 0.05     # minimum edge for longshot alert

# Dual-prediction architecture (Stream A2 — 2026-04-29).
# Tony's two-pass handicapping methodology:
#   1. handicapping_prob — pure form-based model output, calibrated.
#   2. market_prob       — 1 / (morning_line_odds + 1).
#   3. edge_pct          — handicapping_prob - market_prob.
# The displayed probability stored in win_probability/displayed_prob is a
# weighted blend: w * handicapping_prob + (1 - w) * market_prob.
# w = 1.0 → pure handicapping (initial). Tune downward only after seeing
# holdout ROI at multiple weights.
HANDICAPPING_BLEND_WEIGHT = 1.0
