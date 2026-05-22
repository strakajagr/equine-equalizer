"""
Equine Equalizer — Training Data Loader
Pulls from Aurora PostgreSQL and computes all 66 features.

CRITICAL DB FACTS:
- past_performances.race_id is NULL for ALL historical rows.
  DO NOT join past_performances to races on race_id. To pull
  race-level fields the chart-parser writes only to races (e.g.,
  grade), join on the composite key (track_code, race_date,
  race_number) via tracks. See _load_raw_pps for the pattern.
- closing_odds is on past_performances (not results, not entries).
- morning_line_odds is on entries table.
- workouts table has 143k+ rows (loaded 2023 data). workout_type='G' → is_gate_work; total_works_on_day → works_on_day (aliased in query).
- track_condition strings are lowercase: 'fast', 'firm', 'sloppy(sealed)', etc.
"""

import json
import logging
import boto3
import numpy as np
import pandas as pd
import psycopg2
import psycopg2.extensions
import psycopg2.extras
from datetime import date, timedelta
from typing import Optional

# psycopg2 returns decimal.Decimal for DECIMAL/NUMERIC columns by default.
# Register a global adapter so all queries return float instead.
_DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None,
)
psycopg2.extensions.register_type(_DEC2FLOAT)

from shared.feature_definitions import (
    FEATURE_DEFS,
    GONZO_FEATURE_DEFS,
    TRAJECTORY_FEATURE_DEFS,
    get_feature_names,
    get_feature_defaults,
    get_all_feature_defaults,
)
from shared.par_times import compute_workout_pars
from shared.gonzo_features import (
    compute_gonzo_speed_features,
    compute_gonzo_trajectory_features,
    compute_gonzo_class_features,
)

# LSTM config (must match model/trajectory/config.py)
LSTM_SEQUENCE_LENGTH = 5
LSTM_MIN_SEQUENCE_LENGTH = 3
LSTM_FEATURES_PER_STEP = 8

logger = logging.getLogger(__name__)

DB_SECRET_ARN = (
    'arn:aws:secretsmanager:us-east-1:584812014683:'
    'secret:equine-equalizer/db-credentials-7CD7Mt'
)

QUALIFYING_TRACKS = [
    'CD', 'SAR', 'KEE', 'BEL', 'SA',
    'GP', 'DMR', 'OP', 'MTH', 'AQU', 'PIM',
]

RACE_QUALITY_TIERS = {
    'stakes':    5,
    'allowance': 4,
    'msw':       3,
    'maiden':    3,
    'claiming':  2,
    'mcl':       1,
}

LAYOFF_BUCKETS = [
    (0, 14,  1),   # sharp
    (14, 28, 2),   # normal
    (28, 60, 3),   # freshened
    (60, 120, 4),  # long layoff
    (120, 9999, 5), # very long layoff
]

TRAINER_DEFAULTS = {
    'trainer_win_rate':        0.10,
    'trainer_itm_rate':        0.30,
    'trainer_layoff_win_rate': 0.08,
    'trainer_lasix_win_rate':  0.12,
    'trainer_sample_size':     0.0,
}

WORKOUT_DEFAULTS = {
    'days_since_last_workout':  30.0,
    'workout_count_30d':        0.0,
    'bullet_work_14d':          0.0,
    'bullet_count_30d':         0.0,
    'best_workout_speed_index': 0.5,
    'workout_speed_trend':      0.0,
    'gate_work_30d':            0.0,
    'workout_frequency_score':  0.0,
}


def _get_conn():
    sm = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(
        sm.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString']
    )
    return psycopg2.connect(
        f"postgresql://{secret['username']}:{secret['password']}"
        f"@{secret['host']}:{secret['port']}/{secret['dbname']}",
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


def _load_raw_pps(conn, start_year: int, end_year: int) -> pd.DataFrame:
    """
    Pull all past_performances rows for qualifying tracks and the
    specified year range. Race context comes from pp.* columns; grade
    is joined from races on (track_code, race_date, race_number) —
    populated only for chart-parsed graded stakes.
    """
    sql = """
        SELECT
            pp.pp_id,
            pp.horse_id,
            pp.race_date,
            pp.track_code,
            pp.race_number,
            pp.finish_position,
            pp.field_size,
            pp.computed_speed_figure,
            pp.speed_rating_raw,
            pp.track_variant,
            pp.early_pace_figure,
            pp.late_pace_figure,
            pp.pace_delta,
            pp.call_1_position,
            pp.call_2_position,
            pp.call_3_position,
            pp.call_1_lengths,
            pp.call_2_lengths,
            pp.call_3_lengths,
            pp.lengths_behind,
            pp.fraction_1,
            pp.fraction_2,
            pp.final_time,
            pp.running_style,
            pp.trip_troubled,
            pp.trip_pace_setter,
            pp.trip_faded,
            pp.trip_late_rally,
            pp.trip_no_factor,
            pp.trip_gate_issue,
            pp.wide_path,
            pp.purse,
            pp.race_type,
            pp.track_condition,
            pp.surface,
            pp.distance_furlongs,
            pp.claiming_price_entered,
            pp.closing_odds,
            pp.trainer_name,
            pp.days_since_last_race,
            pp.race_start_number,
            r.grade
        FROM past_performances pp
        LEFT JOIN tracks t ON t.track_code = pp.track_code
        LEFT JOIN races r
               ON r.track_id    = t.track_id
              AND r.race_date   = pp.race_date
              AND r.race_number = pp.race_number
        WHERE pp.track_code = ANY(%s)
          AND EXTRACT(YEAR FROM pp.race_date) BETWEEN %s AND %s
          AND pp.finish_position IS NOT NULL
          AND pp.finish_position < 90
        ORDER BY pp.race_date, pp.track_code, pp.race_number
    """
    with conn.cursor() as cur:
        cur.execute(sql, (QUALIFYING_TRACKS, start_year, end_year))
        rows = cur.fetchall()
    df = pd.DataFrame([dict(r) for r in rows])
    df['race_date'] = pd.to_datetime(df['race_date'])
    logger.info(f"Loaded {len(df):,} PP rows ({start_year}-{end_year})")
    return df


def _load_entries(conn, start_year: int, end_year: int) -> pd.DataFrame:
    """
    Load entries for equipment/odds/jockey features.
    Joined to jockeys for jockey_name.
    morning_line_odds lives here (not on past_performances).
    """
    sql = """
        SELECT
            e.entry_id,
            e.horse_id,
            e.race_id,
            e.morning_line_odds,
            e.weight_carried,
            e.apprentice_allowance,
            e.lasix,
            e.lasix_first_time,
            e.blinkers_on,
            e.blinkers_off,
            e.blinkers_first_time,
            e.jockey_id,
            j.jockey_name
        FROM entries e
        LEFT JOIN jockeys j ON e.jockey_id = j.jockey_id
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    df = pd.DataFrame([dict(r) for r in rows])
    logger.info(f"Loaded {len(df):,} entries rows")
    return df


def _load_results(conn) -> pd.DataFrame:
    """Load win_payout from results table for EV label computation."""
    sql = """
        SELECT horse_id, race_id, finish_position, win_payout
        FROM results
        WHERE finish_position = 1 AND win_payout > 0
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    df = pd.DataFrame([dict(r) for r in rows])
    logger.info(f"Loaded {len(df):,} result payout rows")
    return df


def _load_trainer_stats(conn) -> pd.DataFrame:
    """Load trainer_stats materialized view (996 rows)."""
    sql = """
        SELECT trainer_name, win_rate, itm_rate,
               layoff_win_rate, lasix_win_rate, total_starts
        FROM trainer_stats
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    df = pd.DataFrame([dict(r) for r in rows])
    logger.info(f"Loaded {len(df):,} trainer_stats rows")
    return df


def _load_workouts(conn) -> pd.DataFrame:
    """
    Load workouts table. Schema has workout_type (not is_gate_work) and
    total_works_on_day (not works_on_day); aliased/derived here.

    track_code + workout_time added 2026-05-01 (Phase A3) for Gonzo
    Sauce noteworthy-workout feature computation via par_times helpers.
    """
    sql = """
        SELECT horse_id, workout_date, distance_furlongs, track_code,
               workout_time, is_bullet, workout_type, rank_on_day,
               total_works_on_day AS works_on_day
        FROM workouts
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    df = pd.DataFrame([dict(r) for r in rows]) if rows else pd.DataFrame(
        columns=['horse_id', 'workout_date', 'distance_furlongs',
                 'track_code', 'workout_time', 'is_bullet', 'workout_type',
                 'rank_on_day', 'works_on_day']
    )
    if not df.empty:
        df['workout_date'] = pd.to_datetime(df['workout_date'])
        df['is_gate_work'] = df['workout_type'].str.upper() == 'G'
    logger.info(f"Loaded {len(df):,} workout rows")
    return df


def _encode_race_quality_tier(race_type: Optional[str]) -> float:
    if not race_type:
        return 2.0
    rt = race_type.lower()
    if 'stakes' in rt or 'stk' in rt:
        return 5.0
    if 'allowance' in rt or 'alw' in rt:
        return 4.0
    if 'maiden special' in rt or 'msw' in rt:
        return 3.0
    if 'maiden' in rt or 'mdm' in rt:
        return 3.0
    if 'maiden claiming' in rt or 'mcl' in rt:
        return 1.0
    if 'claiming' in rt or 'clm' in rt:
        return 2.0
    return 2.0


def _layoff_bucket(days: Optional[float]) -> float:
    if days is None or np.isnan(days):
        return 2.0
    for lo, hi, bucket in LAYOFF_BUCKETS:
        if lo <= days < hi:
            return float(bucket)
    return 5.0


def _compute_speed_features(horse_hist: pd.DataFrame, row: pd.Series) -> dict:
    """Compute 11 speed features from this horse's prior race history."""
    prior = horse_hist[horse_hist['race_date'] < row['race_date']].sort_values(
        'race_date', ascending=False
    )
    figs = prior['computed_speed_figure'].dropna()
    defaults = get_feature_defaults()

    if figs.empty:
        return {
            'speed_fig_last':        defaults['speed_fig_last'],
            'speed_fig_avg_3':       defaults['speed_fig_avg_3'],
            'speed_fig_trend':       defaults['speed_fig_trend'],
            'speed_fig_best_career': defaults['speed_fig_best_career'],
            'speed_fig_best_90d':    defaults['speed_fig_best_90d'],
            'speed_fig_at_track':    defaults['speed_fig_at_track'],
            'speed_fig_at_distance': defaults['speed_fig_at_distance'],
            'speed_fig_on_surface':  defaults['speed_fig_on_surface'],
            'speed_fig_vs_field':    defaults['speed_fig_vs_field'],
            'speed_fig_consistency': defaults['speed_fig_consistency'],
            'speed_fig_sample_size': 0.0,
        }

    last = float(figs.iloc[0])
    avg3 = float(figs.head(3).mean())
    cutoff_90d = row['race_date'] - pd.Timedelta(days=90)
    recent_prior = prior[prior['race_date'] >= cutoff_90d]
    best_90d = float(recent_prior['computed_speed_figure'].max()) if not recent_prior.empty else 0.0

    at_track = prior[prior['track_code'] == row['track_code']]['computed_speed_figure'].dropna()
    at_dist = prior[abs(prior['distance_furlongs'] - row['distance_furlongs']) < 0.5]['computed_speed_figure'].dropna()
    on_surf = prior[prior['surface'] == row['surface']]['computed_speed_figure'].dropna()

    last5 = figs.head(5)
    consistency = float(last5.std()) if len(last5) >= 2 else defaults['speed_fig_consistency']

    return {
        'speed_fig_last':        last,
        'speed_fig_avg_3':       avg3,
        'speed_fig_trend':       last - avg3,
        'speed_fig_best_career': float(figs.max()),
        'speed_fig_best_90d':    best_90d,
        'speed_fig_at_track':    float(at_track.mean()) if not at_track.empty else defaults['speed_fig_at_track'],
        'speed_fig_at_distance': float(at_dist.mean()) if not at_dist.empty else defaults['speed_fig_at_distance'],
        'speed_fig_on_surface':  float(on_surf.mean()) if not on_surf.empty else defaults['speed_fig_on_surface'],
        'speed_fig_vs_field':    0.0,  # filled in post-aggregation with field average
        'speed_fig_consistency': consistency,
        'speed_fig_sample_size': float(len(figs)),
    }


def _compute_pace_features(horse_hist: pd.DataFrame, row: pd.Series,
                            today_race: pd.DataFrame) -> dict:
    """Compute 6 pace features."""
    prior = horse_hist[horse_hist['race_date'] < row['race_date']].sort_values(
        'race_date', ascending=False
    )
    last5 = prior.head(5)
    defaults = get_feature_defaults()

    early_last = float(prior['early_pace_figure'].dropna().iloc[0]) if not prior['early_pace_figure'].dropna().empty else defaults['early_pace_last']
    late_last  = float(prior['late_pace_figure'].dropna().iloc[0])  if not prior['late_pace_figure'].dropna().empty else defaults['late_pace_last']
    delta_last = float(prior['pace_delta'].dropna().iloc[0])        if not prior['pace_delta'].dropna().empty else defaults['pace_delta_last']

    call1_pos  = last5['call_1_position'].dropna()
    avg_call1  = float(call1_pos.mean()) if not call1_pos.empty else defaults['avg_call1_position']

    # stretch gain: call_2_position minus finish_position (negative = gained positions)
    valid = last5.dropna(subset=['call_2_position', 'finish_position'])
    if not valid.empty:
        gains = valid['call_2_position'] - valid['finish_position']
        avg_stretch = float(gains.mean())
    else:
        avg_stretch = defaults['avg_stretch_gain']

    # pace_scenario_today: count of early/front-running horses in today's field
    early_styles = today_race['running_style'].isin(['E', 'EP', 'P'])
    pace_scenario = int(early_styles.sum())

    return {
        'early_pace_last':    early_last,
        'late_pace_last':     late_last,
        'pace_delta_last':    delta_last,
        'avg_call1_position': avg_call1,
        'avg_stretch_gain':   avg_stretch,
        'pace_scenario_today': float(pace_scenario),
    }


def _compute_trip_features(horse_hist: pd.DataFrame, row: pd.Series) -> dict:
    """Compute 8 trip flag features from last 5 races."""
    prior = horse_hist[horse_hist['race_date'] < row['race_date']].sort_values(
        'race_date', ascending=False
    )
    last5 = prior.head(5)
    n = len(last5)
    defaults = get_feature_defaults()

    if n == 0:
        return {k: defaults[k] for k in [
            'troubled_trip_last', 'troubled_trip_freq', 'pace_setter_freq',
            'faded_freq', 'late_rally_freq', 'avg_wide_path',
            'wide_3plus_freq', 'gate_issue_freq',
        ]}

    troubled_last = float(prior.iloc[0]['trip_troubled']) if not prior.empty else 0.0

    return {
        'troubled_trip_last': troubled_last,
        'troubled_trip_freq': float(last5['trip_troubled'].sum()) / n,
        'pace_setter_freq':   float(last5['trip_pace_setter'].sum()) / n,
        'faded_freq':         float(last5['trip_faded'].sum()) / n,
        'late_rally_freq':    float(last5['trip_late_rally'].sum()) / n,
        'avg_wide_path':      float(last5['wide_path'].mean()),
        'wide_3plus_freq':    float((last5['wide_path'] >= 3).sum()) / n,
        'gate_issue_freq':    float(last5['trip_gate_issue'].sum()) / n,
    }


def _safe_float(val, default: float) -> float:
    """Return float(val) unless val is None/NaN, in which case return default."""
    try:
        if pd.isna(val):
            return float(default)
    except (TypeError, ValueError):
        pass
    try:
        return float(val)
    except (TypeError, ValueError):
        return float(default)


def _compute_trainer_features(trainer_name: Optional[str],
                               trainer_stats: pd.DataFrame) -> dict:
    """Look up trainer stats. Return population defaults if not found."""
    if trainer_name and not trainer_stats.empty:
        row = trainer_stats[trainer_stats['trainer_name'] == trainer_name]
        if not row.empty:
            r = row.iloc[0]
            return {
                'trainer_win_rate':        _safe_float(r.get('win_rate'),        TRAINER_DEFAULTS['trainer_win_rate']),
                'trainer_itm_rate':        _safe_float(r.get('itm_rate'),        TRAINER_DEFAULTS['trainer_itm_rate']),
                'trainer_layoff_win_rate': _safe_float(r.get('layoff_win_rate'), TRAINER_DEFAULTS['trainer_layoff_win_rate']),
                'trainer_lasix_win_rate':  _safe_float(r.get('lasix_win_rate'),  TRAINER_DEFAULTS['trainer_lasix_win_rate']),
                'trainer_sample_size':     _safe_float(r.get('total_starts'),    0.0),
            }
    return dict(TRAINER_DEFAULTS)


def _build_workouts_by_horse(workouts: pd.DataFrame) -> dict:
    """Pre-aggregate workouts by horse_id, sorted desc by workout_date.
    Built once before the row loop — turns a per-row full-table scan
    (O(n_pps × n_workouts)) into an O(1) dict lookup + small per-horse
    date filter. Was the dominant bottleneck (61% of loop) once the
    workouts table became populated.
    """
    if workouts.empty:
        return {}
    return {hid: grp.sort_values('workout_date', ascending=False)
            for hid, grp in workouts.groupby('horse_id')}


def _compute_workout_features(horse_id: str, race_date: pd.Timestamp,
                               workouts_by_horse: dict) -> dict:
    """
    Compute 8 workout features. Returns defaults when this horse has no
    prior workouts. `workouts_by_horse` is the pre-built dict from
    `_build_workouts_by_horse` — each value already sorted desc by date.
    """
    if not workouts_by_horse:
        return dict(WORKOUT_DEFAULTS)
    horse_w_all = workouts_by_horse.get(horse_id)
    if horse_w_all is None or horse_w_all.empty:
        return dict(WORKOUT_DEFAULTS)
    horse_w = horse_w_all[horse_w_all['workout_date'] < race_date]
    if horse_w.empty:
        return dict(WORKOUT_DEFAULTS)

    cutoff_30 = race_date - pd.Timedelta(days=30)
    cutoff_14 = race_date - pd.Timedelta(days=14)
    w30 = horse_w[horse_w['workout_date'] >= cutoff_30]
    w14 = horse_w[horse_w['workout_date'] >= cutoff_14]

    days_since = float((race_date - horse_w.iloc[0]['workout_date']).days)
    count_30 = float(len(w30))
    bullet_14 = float((w14['is_bullet'] == True).any())
    bullet_30 = float((w30['is_bullet'] == True).sum())
    gate_30 = float((w30['is_gate_work'] == True).any())

    if not w30.empty and 'rank_on_day' in w30.columns and 'works_on_day' in w30.columns:
        valid = w30.dropna(subset=['rank_on_day', 'works_on_day'])
        if not valid.empty:
            speed_idx = float((valid['rank_on_day'] / valid['works_on_day']).min())
        else:
            speed_idx = 0.5
    else:
        speed_idx = 0.5

    # workout speed trend: compare last 2 vs prior 2 speed indices
    speed_trend = 0.0
    if len(w30) >= 4 and 'rank_on_day' in w30.columns:
        recent = w30.head(2)['rank_on_day'].mean()
        older = w30.iloc[2:4]['rank_on_day'].mean()
        if older > 0:
            speed_trend = float((older - recent) / older)

    return {
        'days_since_last_workout':  days_since,
        'workout_count_30d':        count_30,
        'bullet_work_14d':          bullet_14,
        'bullet_count_30d':         bullet_30,
        'best_workout_speed_index': speed_idx,
        'workout_speed_trend':      speed_trend,
        'gate_work_30d':            gate_30,
        'workout_frequency_score':  min(count_30 / 4.0, 1.0),
    }



def _compute_class_features(horse_hist: pd.DataFrame, row: pd.Series) -> dict:
    """Compute 7 class features."""
    prior = horse_hist[horse_hist['race_date'] < row['race_date']].sort_values(
        'race_date', ascending=False
    )
    defaults = get_feature_defaults()

    today_purse = row.get('purse') or 0.0
    last_purse = float(prior['purse'].dropna().iloc[0]) if not prior['purse'].dropna().empty else today_purse

    purse_change = 0.0
    if last_purse > 0:
        purse_change = (today_purse - last_purse) / last_purse

    class_direction = 0.0
    if purse_change > 0.15:
        class_direction = 1.0
    elif purse_change < -0.15:
        class_direction = -1.0

    today_claim = row.get('claiming_price_entered') or 0.0
    last_claim = float(prior['claiming_price_entered'].dropna().iloc[0]) if not prior['claiming_price_entered'].dropna().empty else 0.0
    claim_change = 0.0
    if last_claim > 0 and today_claim > 0:
        claim_change = (today_claim - last_claim) / last_claim

    all_purses = prior['purse'].dropna()
    career_ceiling = float(all_purses.max()) if not all_purses.empty else today_purse
    ceiling_pct = today_purse / career_ceiling if career_ceiling > 0 else 1.0

    last5_purses = prior.head(5)['purse'].dropna()
    class_consistency = float(last5_purses.std()) if len(last5_purses) >= 2 else defaults['class_consistency']

    return {
        'class_direction':           class_direction,
        'purse_change_pct':          purse_change,
        'claiming_price_change_pct': claim_change,
        'career_class_ceiling':      career_ceiling,
        'current_vs_ceiling_pct':    ceiling_pct,
        'class_consistency':         class_consistency,
        'race_quality_tier':         _encode_race_quality_tier(row.get('race_type')),
    }


def _compute_phase_b_top5_features(
    horse_hist: pd.DataFrame,
    row: pd.Series,
    today_race: pd.DataFrame,
    pps_by_horse: dict,
) -> dict:
    """Phase B Top-5 features (Gate 5 train/inference drift fix).

    Mirrors `backend/services/feature_engineering_service.py::compute_phase_b_top5_features`
    using the training-side DataFrame inputs. Decision 4 sentinel pattern:
    -1.0 disambiguates "no PP history" from real-valued 0.

    LEAK-DISCIPLINE: each subquery uses race_date < row['race_date'] (strict).
    """
    prior = horse_hist[horse_hist['race_date'] < row['race_date']].sort_values(
        'race_date', ascending=False
    )

    feats = {
        'surface_win_rate':    0.0,
        'pace_pressure_score': 0.0,
        'class_drop_flag':     -1.0,
        'shipped_from_flag':   -1.0,
        'layoff_off_bucket':   -1.0,
    }

    if prior.empty:
        # All sentinels — no PP history for this horse
        return feats

    # ── Feature 1: surface_win_rate ──
    today_surface = row.get('surface')
    if today_surface:
        surface_pps = prior[
            (prior['surface'].astype(str).str.lower() == str(today_surface).lower())
            & (prior['finish_position'].notna())
        ]
        if not surface_pps.empty:
            wins = (surface_pps['finish_position'] == 1).sum()
            feats['surface_win_rate'] = float(wins) / len(surface_pps)

    # ── Feature 2: pace_pressure_score ──
    # For each OTHER horse in today's race, look at THEIR recent (last 3) prior
    # early_pace_figure. Then field-relative E-runner count.
    if today_race is not None and not today_race.empty:
        e_pace_avgs = []
        for _, other_pp in today_race.iterrows():
            other_horse_id = other_pp.get('horse_id')
            if other_horse_id is None:
                continue
            other_hist = pps_by_horse.get(other_horse_id)
            if other_hist is None or other_hist.empty:
                continue
            other_prior = other_hist[other_hist['race_date'] < row['race_date']].sort_values(
                'race_date', ascending=False
            ).head(3)
            ep = other_prior['early_pace_figure'].dropna()
            if not ep.empty:
                e_pace_avgs.append(float(ep.mean()))
        if e_pace_avgs:
            field_avg = sum(e_pace_avgs) / len(e_pace_avgs)
            n_e_runners = sum(1 for p in e_pace_avgs if p > field_avg + 1.0)
            feats['pace_pressure_score'] = n_e_runners / max(1, len(e_pace_avgs))

    # ── Feature 3: class_drop_flag ──
    last_purse = float(prior['purse'].dropna().iloc[0]) if not prior['purse'].dropna().empty else None
    today_purse = row.get('purse')
    if last_purse and today_purse and last_purse > 0:
        purse_ratio = float(today_purse) / last_purse
        feats['class_drop_flag'] = 1.0 if purse_ratio < 0.85 else 0.0
    else:
        feats['class_drop_flag'] = 0.0  # PP present but no purse data

    # ── Feature 4: shipped_from_flag ──
    last_track = prior['track_code'].dropna().iloc[0] if not prior['track_code'].dropna().empty else None
    today_track = row.get('track_code')
    if last_track and today_track:
        feats['shipped_from_flag'] = 0.0 if last_track == today_track else 1.0
    else:
        feats['shipped_from_flag'] = 0.0

    # ── Feature 5: layoff_off_bucket ──
    last_date_raw = prior['race_date'].dropna().iloc[0] if not prior['race_date'].dropna().empty else None
    today_date = row.get('race_date')
    if last_date_raw is not None and today_date is not None:
        last_date = pd.to_datetime(last_date_raw)
        today_date_ts = pd.to_datetime(today_date)
        days_off = (today_date_ts - last_date).days
        if days_off <= 14:
            feats['layoff_off_bucket'] = 0.0
        elif days_off <= 30:
            feats['layoff_off_bucket'] = 1.0
        elif days_off <= 60:
            feats['layoff_off_bucket'] = 2.0
        elif days_off <= 180:
            feats['layoff_off_bucket'] = 3.0
        else:
            feats['layoff_off_bucket'] = 4.0
    else:
        feats['layoff_off_bucket'] = 0.0

    return feats


def _compute_physical_features(horse_hist: pd.DataFrame, row: pd.Series,
                                entry_row: Optional[pd.Series]) -> dict:
    """Compute 10 physical/situational features."""
    prior = horse_hist[horse_hist['race_date'] < row['race_date']].sort_values(
        'race_date', ascending=False
    )
    defaults = get_feature_defaults()

    days_off = row.get('days_since_last_race')
    if days_off is None or (isinstance(days_off, float) and np.isnan(days_off)):
        days_off = 30.0
    else:
        days_off = float(days_off)

    career_starts = float(len(prior)) + 1
    is_first = 1.0 if len(prior) == 0 else 0.0

    surfaces_seen = prior['surface'].dropna().unique()
    first_surface = 1.0 if (row.get('surface') not in surfaces_seen) else 0.0

    was_claimed = 1.0 if (not prior.empty and prior.iloc[0].get('was_claimed') == True) else 0.0

    # win rate at this track
    track_pps = prior[prior['track_code'] == row['track_code']]
    track_wr = float((track_pps['finish_position'] == 1).mean()) if not track_pps.empty else 0.0

    overall_wr = float((prior['finish_position'] == 1).mean()) if not prior.empty else 0.0

    weight = 118.0
    app_allow = 0.0
    if entry_row is not None:
        weight = _safe_float(entry_row.get('weight_carried'), 118.0)
        app_allow = _safe_float(entry_row.get('apprentice_allowance'), 0.0)

    return {
        'days_since_last_race':  days_off,
        'layoff_bucket':         _layoff_bucket(days_off),
        'career_starts':         career_starts,
        'is_first_start':        is_first,
        'first_time_on_surface': first_surface,
        'was_claimed_last_out':  was_claimed,
        'weight_carried':        weight,
        'apprentice_allowance':  app_allow,
        'win_rate_this_track':   track_wr,
        'overall_win_rate':      overall_wr,
    }


def _compute_equipment_features(row: pd.Series,
                                  entry_row: Optional[pd.Series],
                                  horse_hist: pd.DataFrame) -> dict:
    """Compute 5 equipment features from entries + history."""
    defaults = get_feature_defaults()
    if entry_row is None:
        return {k: defaults[k] for k in
                ['lasix', 'lasix_first_time', 'blinkers_on', 'blinkers_off', 'trainer_intent_score']}

    lasix = 1.0 if entry_row.get('lasix') else 0.0
    lasix_ft = 1.0 if entry_row.get('lasix_first_time') else 0.0
    bl_on = 1.0 if entry_row.get('blinkers_on') else 0.0
    bl_off = 1.0 if entry_row.get('blinkers_off') else 0.0

    # trainer_intent_score: composite of equipment changes + class signals
    prior = horse_hist[horse_hist['race_date'] < row['race_date']]
    today_purse_val = _safe_float(row.get('purse'), 0.0)
    last_purse_val = float(prior['purse'].dropna().iloc[0]) if not prior.empty and not prior['purse'].dropna().empty else 0.0
    class_drop = 1.0 if today_purse_val < last_purse_val else 0.0
    intent_score = float(lasix_ft * 2 + bl_on + class_drop)

    return {
        'lasix':               lasix,
        'lasix_first_time':    lasix_ft,
        'blinkers_on':         bl_on,
        'blinkers_off':        bl_off,
        'trainer_intent_score': intent_score,
    }


def _compute_odds_features(row: pd.Series,
                             entry_row: Optional[pd.Series]) -> dict:
    """Compute 3 odds features."""
    closing = row.get('closing_odds')
    if closing is None or (isinstance(closing, float) and np.isnan(closing)):
        closing = 5.0
    closing = float(closing)

    morning_line = None
    if entry_row is not None:
        ml = entry_row.get('morning_line_odds')
        if ml is not None and not (isinstance(ml, float) and np.isnan(ml)):
            morning_line = float(ml)

    odds_move = (closing - morning_line) if morning_line is not None else 0.0

    return {
        'closing_odds':    closing,
        'log_closing_odds': float(np.log1p(closing)),
        'odds_move':        odds_move,
    }


def _build_pps_by_jockey(pps: pd.DataFrame) -> dict:
    """Pre-aggregate pps by jockey_name. Built once before the row loop —
    turns the per-row full-table scan in `_compute_jockey_features` into
    an O(1) dict lookup. Returns {} if the pps table has no jockey_name
    column (current pps schema), which preserves the original guard.
    """
    if 'jockey_name' not in pps.columns:
        return {}
    return {jn: grp for jn, grp in pps.groupby('jockey_name')}


def _compute_jockey_features(horse_hist: pd.DataFrame, row: pd.Series,
                               entry_row: Optional[pd.Series],
                               pps_by_jockey: dict,
                               entries_df: pd.DataFrame) -> dict:
    """Compute 3 jockey features. `pps_by_jockey` is the pre-built dict
    from `_build_pps_by_jockey`. `entries_df` is currently unused but
    kept in the signature for upstream-caller compatibility."""
    defaults = get_feature_defaults()

    if entry_row is None:
        return {k: defaults[k] for k in
                ['jockey_win_rate', 'jockey_trainer_combo_win_rate', 'jockey_change_flag']}

    jockey_name = entry_row.get('jockey_name')

    jockey_wr = defaults['jockey_win_rate']
    combo_wr = defaults['jockey_trainer_combo_win_rate']
    if jockey_name:
        jock_pps = pps_by_jockey.get(jockey_name, pd.DataFrame())
        if not jock_pps.empty:
            jockey_wr = float((jock_pps['finish_position'] == 1).mean())

        trainer = row.get('trainer_name')
        if trainer and not jock_pps.empty:
            combo = jock_pps[jock_pps['trainer_name'] == trainer]
            if not combo.empty:
                combo_wr = float((combo['finish_position'] == 1).mean())

    # jockey_change_flag: different jockey_name than most recent prior race
    prior = horse_hist[horse_hist['race_date'] < row['race_date']].sort_values(
        'race_date', ascending=False
    )
    jockey_change = 0.0
    if not prior.empty and 'jockey_name' in prior.columns:
        last_jockey = prior.iloc[0].get('jockey_name')
        if last_jockey and jockey_name and last_jockey != jockey_name:
            jockey_change = 1.0

    return {
        'jockey_win_rate':              jockey_wr,
        'jockey_trainer_combo_win_rate': combo_wr,
        'jockey_change_flag':           jockey_change,
    }


def _compute_trajectory_feature(
    horse_hist: pd.DataFrame,
    row: pd.Series,
    lstm_model,
    lstm_scaler,
) -> dict:
    """Compute the LSTM trajectory_score feature with STRICT as-of-race-date
    leak discipline.

    LEAK-DISCIPLINE INVARIANTS (Gate 3 — Tony's explicit requirement):
      1. Input sequence is filtered with `race_date < row['race_date']` — the
         current race and any future races for this horse are EXCLUDED.
      2. Only computed_speed_figure-bearing PPs are used (matches train.py
         build_sequences which filters WHERE computed_speed_figure IS NOT NULL).
      3. Returns NaN if fewer than LSTM_MIN_SEQUENCE_LENGTH prior races exist —
         the explicit sentinel directive, no silent 0.0 pad.
      4. Sequence ordering: chronological (oldest first), left-padded with
         zeros if < LSTM_SEQUENCE_LENGTH available — matches training shape.

    Caller (build_feature_matrix) is responsible for loading lstm_model +
    lstm_scaler ONCE and passing in. If lstm_model is None this function
    is not called at all (the feature is omitted from the row).
    """
    import torch  # local import — only required when LSTM is wired in

    # INVARIANT 1: strict prior-only filter (as-of-race-date)
    prior = horse_hist[horse_hist['race_date'] < row['race_date']]
    # INVARIANT 2: training-shape filters (match train.py build_sequences):
    #   computed_speed_figure IS NOT NULL  AND  finish_position IS NOT NULL
    #   AND finish_position < 90
    prior = prior[prior['computed_speed_figure'].notna()]
    if 'finish_position' in prior.columns:
        prior = prior[prior['finish_position'].notna()]
        prior = prior[prior['finish_position'] < 90]

    # INVARIANT 3: not enough history → explicit NaN sentinel
    if len(prior) < LSTM_MIN_SEQUENCE_LENGTH:
        return {'trajectory_score': float('nan')}

    # Last LSTM_SEQUENCE_LENGTH prior races, ordered most-recent FIRST then
    # reversed to chronological (oldest → newest) to match build_sequences()
    prior = prior.sort_values('race_date', ascending=False).head(LSTM_SEQUENCE_LENGTH)
    seq_rows = list(reversed(list(prior.iterrows())))  # chronological

    # Build sequence array — left-pad with zeros if fewer than LSTM_SEQUENCE_LENGTH
    seq = np.zeros((LSTM_SEQUENCE_LENGTH, LSTM_FEATURES_PER_STEP), dtype=np.float32)
    offset = LSTM_SEQUENCE_LENGTH - len(seq_rows)
    for j, (_, r) in enumerate(seq_rows):
        fs = float(r.get('field_size') or 8)
        seq[offset + j] = [
            float(r.get('computed_speed_figure') or 0),
            float(r.get('finish_position') or 5) / max(fs, 1),
            float(r.get('early_pace_figure') or 24),
            float(r.get('late_pace_figure') or 38),
            float(r.get('days_since_last_race') or 30),
            float(r.get('purse') or 0),
            fs,
            float(r.get('closing_odds') or 5),
        ]

    seq = np.nan_to_num(seq, nan=0.0, posinf=0.0, neginf=0.0)

    if lstm_scaler is not None:
        flat = seq.reshape(-1, LSTM_FEATURES_PER_STEP)
        seq = lstm_scaler.transform(flat).reshape(
            1, LSTM_SEQUENCE_LENGTH, LSTM_FEATURES_PER_STEP
        )
    else:
        seq = seq.reshape(1, LSTM_SEQUENCE_LENGTH, LSTM_FEATURES_PER_STEP)
    seq = np.nan_to_num(seq, nan=0.0)

    tensor = torch.FloatTensor(seq)
    with torch.no_grad():
        prob = float(lstm_model.predict_proba(tensor).item())
    # Map [0, 1] → [-1, +1] (matches ls_inference_service.py mapping)
    return {'trajectory_score': round(prob * 2.0 - 1.0, 4)}


def build_feature_matrix(
    conn=None,
    start_year: int = 2022,
    end_year: int = 2025,
    include_odds: bool = True,
    pps_filter=None,
    lstm_model=None,
    lstm_scaler=None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Build full feature matrix for training.

    pps_filter (optional callable): receives the loaded pps DataFrame and
        returns a filtered copy. Applied AFTER load, BEFORE prep-dict
        construction — so iteration target, pps_by_horse, and race_groups
        all reflect the filter. Used by sprint/route specialists.

    Returns:
        features_df: pp_id + 66 feature columns (or 63 if include_odds=False)
        labels_df:   pp_id, horse_id, race_date, track_code, race_number,
                     finish_position, field_size, closing_odds, win_payout
    """
    close_conn = False
    if conn is None:
        conn = _get_conn()
        close_conn = True

    try:
        logger.info(f"Loading raw data ({start_year}-{end_year})...")
        pps = _load_raw_pps(conn, start_year, end_year)
        if pps_filter is not None:
            n_before = len(pps)
            pps = pps_filter(pps)
            logger.info(f"pps_filter applied: {n_before:,} → {len(pps):,} rows")
        entries_df = _load_entries(conn, start_year, end_year)
        results_df = _load_results(conn)
        trainer_stats = _load_trainer_stats(conn)
        workouts = _load_workouts(conn)

        logger.info("Computing features row by row...")
        feature_name_list = get_feature_names(include_odds=include_odds)
        feature_defaults = get_all_feature_defaults()
        gonzo_feature_names = [f.name for f in GONZO_FEATURE_DEFS]
        trajectory_feature_names = [f.name for f in TRAJECTORY_FEATURE_DEFS]

        # Phase A3: par-time dict (built once, shared across all rows).
        par_dict = compute_workout_pars(conn)

        # Build horse-level history index for fast lookup
        pps['race_date'] = pd.to_datetime(pps['race_date'])
        pps_by_horse = {hid: grp for hid, grp in pps.groupby('horse_id')}

        # Build race key → group for pace_scenario_today
        pps['race_key'] = (pps['track_code'] + '_' +
                           pps['race_date'].dt.strftime('%Y%m%d') + '_' +
                           pps['race_number'].astype(str))
        race_groups = {k: g for k, g in pps.groupby('race_key')}

        # Build entries lookup by horse_id (latest entry per horse)
        entries_by_horse = {}
        if not entries_df.empty:
            for hid, grp in entries_df.groupby('horse_id'):
                entries_by_horse[hid] = grp.iloc[0]

        # Pre-built lookups for the two formerly-O(n^2) functions
        workouts_by_horse = _build_workouts_by_horse(workouts)
        pps_by_jockey     = _build_pps_by_jockey(pps)

        # Build results lookup: (horse_id) → win_payout
        payout_map = {}
        if not results_df.empty:
            for _, r in results_df.iterrows():
                payout_map[str(r['horse_id'])] = float(r['win_payout'])

        rows_feat = []
        rows_label = []

        for idx, row in pps.iterrows():
            horse_id = row['horse_id']
            horse_hist = pps_by_horse.get(horse_id, pd.DataFrame())
            race_key = row['race_key']
            today_race = race_groups.get(race_key, pd.DataFrame())
            entry_row = entries_by_horse.get(horse_id)

            feats = {'pp_id': str(row['pp_id'])}

            # Speed
            feats.update(_compute_speed_features(horse_hist, row))

            # Pace
            feats.update(_compute_pace_features(horse_hist, row, today_race))

            # Trip
            feats.update(_compute_trip_features(horse_hist, row))

            # Trainer
            feats.update(_compute_trainer_features(row.get('trainer_name'), trainer_stats))

            # Workout (per-horse pre-indexed)
            feats.update(_compute_workout_features(str(horse_id), row['race_date'], workouts_by_horse))

            # Class
            feats.update(_compute_class_features(horse_hist, row))

            # Phase B Top-5 (Gate 5 train/inference drift fix — previously these
            # 5 features fell through to defaults during training while the
            # inference pipeline computed them. The model trained on constants.)
            feats.update(_compute_phase_b_top5_features(
                horse_hist, row, today_race, pps_by_horse
            ))

            # Physical
            feats.update(_compute_physical_features(horse_hist, row, entry_row))

            # Equipment
            feats.update(_compute_equipment_features(row, entry_row, horse_hist))

            # Odds
            if include_odds:
                feats.update(_compute_odds_features(row, entry_row))

            # Jockey (per-jockey-name pre-indexed)
            feats.update(_compute_jockey_features(horse_hist, row, entry_row, pps_by_jockey, entries_df))

            # ── Gonzo Sauce — Groups A/B/C (Phase A3, 14 features) ──
            # Helpers live in shared.gonzo_features (imported above) — same
            # module is used by inference's feature_engineering_service to
            # eliminate train/inference computation drift.
            feats.update(compute_gonzo_speed_features(
                horse_hist, row, workouts_by_horse, par_dict
            ))
            feats.update(compute_gonzo_trajectory_features(horse_hist, row))
            feats.update(compute_gonzo_class_features(horse_hist, row))

            # ── Gate 3: LSTM trajectory_score (strict as-of-race-date) ──
            # Only computed when caller passes lstm_model (and scaler); for
            # legacy training scripts that don't pass it, the feature is
            # filled with NaN default via the all-defaults sweep below.
            if lstm_model is not None:
                feats.update(_compute_trajectory_feature(
                    horse_hist, row, lstm_model, lstm_scaler
                ))

            # Fill any missing features with defaults (covers base + gonzo + traj)
            for fname in feature_name_list + gonzo_feature_names + trajectory_feature_names:
                if fname not in feats:
                    feats[fname] = feature_defaults[fname]

            output_columns = (
                ['pp_id'] + feature_name_list + gonzo_feature_names
                + trajectory_feature_names
            )
            rows_feat.append({k: feats[k] for k in output_columns})

            # Label row
            win_payout = payout_map.get(str(horse_id), 0.0)
            if row['finish_position'] != 1:
                win_payout = 0.0
            rows_label.append({
                'pp_id':          str(row['pp_id']),
                'horse_id':       str(horse_id),
                'race_date':      row['race_date'],
                'track_code':     row['track_code'],
                'race_number':    row['race_number'],
                'race_key':       race_key,
                'finish_position': int(row['finish_position']),
                'field_size':     int(_safe_float(row.get('field_size'), 8.0)),
                'closing_odds':   _safe_float(row.get('closing_odds'), 5.0),
                'win_payout':     win_payout,
            })

        features_df = pd.DataFrame(rows_feat)
        labels_df = pd.DataFrame(rows_label)

        # Post-compute speed_fig_vs_field (needs field average)
        field_avg = features_df.groupby(
            labels_df['race_key']
        )['speed_fig_last'].transform('mean')
        features_df['speed_fig_vs_field'] = features_df['speed_fig_last'] - field_avg

        # Gate 6 §G: orphan exclusion (never zero-pad — exclude entirely).
        # Drop training rows for races that:
        #   (a) have no results row at all (260 races out of 25,951)
        #   (b) have no PP rows for the running field (179 races)
        # These rows would otherwise feed garbage labels into the model.
        # NB: we keep first-time starters (entries_no_pp_history = 42,966 rows)
        # — those are legitimate, the FE applies default-value sentinels.
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT pp.race_date, pp.track_code, pp.race_number
                FROM past_performances pp
                WHERE NOT EXISTS (
                    SELECT 1 FROM results res
                    JOIN races r ON r.race_id = res.race_id
                    JOIN tracks t ON t.track_id = r.track_id
                    WHERE r.race_date = pp.race_date
                      AND t.track_code = pp.track_code
                      AND r.race_number = pp.race_number
                )
                AND pp.race_date BETWEEN %s AND %s
            """, (
                pd.Timestamp(year=start_year, month=1, day=1).date(),
                pd.Timestamp(year=end_year, month=12, day=31).date(),
            ))
            no_results_keys = {
                f"{r['track_code']}_{r['race_date'].strftime('%Y%m%d')}_{r['race_number']}"
                for r in cur.fetchall()
            }
        n_orphans = len(no_results_keys)
        if n_orphans > 0:
            before = len(features_df)
            keep_mask = ~labels_df['race_key'].isin(no_results_keys)
            features_df = features_df.loc[keep_mask].reset_index(drop=True)
            labels_df = labels_df.loc[keep_mask].reset_index(drop=True)
            logger.info(
                f"Gate-6 orphan exclusion: dropped {before - len(features_df):,} rows "
                f"from {n_orphans} races without results"
            )

        logger.info(
            f"Feature matrix built: {len(features_df):,} rows × "
            f"{len(features_df.columns)-1} features"
        )

        # Gate 3 §1.2: print trajectory coverage after the FE pass
        if 'trajectory_score' in features_df.columns:
            n_total = len(features_df)
            n_scored = features_df['trajectory_score'].notna().sum()
            pct = 100.0 * n_scored / n_total if n_total else 0.0
            logger.info(
                f"trajectory_score coverage: {n_scored:,}/{n_total:,} "
                f"({pct:.1f}%) — NaN means <{LSTM_MIN_SEQUENCE_LENGTH} prior PPs"
            )
        return features_df, labels_df

    finally:
        if close_conn:
            conn.close()
