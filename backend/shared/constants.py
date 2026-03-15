QUALIFYING_TRACKS = [
    'CD', 'SAR', 'KEE', 'BEL', 'SA',
    'GP', 'DMR', 'OP', 'MTH', 'AQU', 'PIM'
]

MIN_CLAIMING_PRICE = 25000

QUALIFYING_RACE_TYPES = [
    'allowance',
    'allowance_optional_claiming',
    'stakes',
    'graded_stakes'
]
# Claiming races included only if claiming_price >= MIN_CLAIMING_PRICE

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

TRACK_CONDITIONS_DIRT = [
    'fast', 'good', 'sloppy', 'muddy',
    'heavy', 'sealed'
]

TRACK_CONDITIONS_TURF = [
    'firm', 'good', 'soft', 'yielding', 'heavy'
]

PP_LOOKBACK_STARTS = 10

WORKOUT_LOOKBACK_DAYS = 45

FEATURE_COUNT = 70

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
