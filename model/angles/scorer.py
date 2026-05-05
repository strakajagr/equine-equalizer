"""
Bayesian Angle Scorer (Layer 6)
Beta-Binomial conjugate prior for handicapping angles.
No training — pure statistical computation from historical data.

Angles: first_time_lasix, off_the_claim, blinkers_on, blinkers_off,
class_drop, class_rise, surface_switch, distance_change, jockey_change,
trainer_layoff_30_60
"""

import logging
from typing import Optional
from scipy.stats import beta as beta_dist

logger = logging.getLogger(__name__)

# Uninformative prior: Beta(1,1) = uniform
PRIOR_ALPHA = 1.0
PRIOR_BETA = 1.0

# Angle definitions: (angle_name, sql_condition_for_detection)
ANGLE_DEFS = [
    'first_time_lasix',
    'off_the_claim',
    'blinkers_on',
    'blinkers_off',
    'class_drop',
    'surface_switch',
    'jockey_change',
]


def score_angle(wins: int, starts: int, odds: float,
                prior_a: float = PRIOR_ALPHA,
                prior_b: float = PRIOR_BETA) -> dict:
    """
    Bayesian angle scoring with Beta-Binomial conjugate prior.
    """
    if starts <= 0:
        return {
            'wins': 0, 'starts': 0,
            'posterior_mean': 0.0, 'ci_low': 0.0, 'ci_high': 0.0,
            'ev_per_bet': -2.0, 'sample_size_adequate': False,
        }

    post_alpha = prior_a + wins
    post_beta = prior_b + (starts - wins)

    posterior_mean = post_alpha / (post_alpha + post_beta)
    ci_low = float(beta_dist.ppf(0.025, post_alpha, post_beta))
    ci_high = float(beta_dist.ppf(0.975, post_alpha, post_beta))

    decimal_odds = float(odds) + 1.0 if odds and odds > 0 else 6.0
    ev_per_bet = (posterior_mean * decimal_odds * 2.0) - 2.0

    return {
        'wins': wins,
        'starts': starts,
        'posterior_mean': round(posterior_mean, 4),
        'ci_low': round(ci_low, 4),
        'ci_high': round(ci_high, 4),
        'ev_per_bet': round(ev_per_bet, 2),
        'sample_size_adequate': starts >= 20,
    }


def detect_angles(entry, pps, race) -> list[str]:
    """
    Detect which angles apply to this entry.
    Returns list of angle names.
    """
    angles = []

    if getattr(entry, 'lasix_first_time', False):
        angles.append('first_time_lasix')

    if pps and getattr(pps[0], 'was_claimed', False):
        angles.append('off_the_claim')

    if getattr(entry, 'blinkers_on', False):
        angles.append('blinkers_on')

    if getattr(entry, 'blinkers_off', False):
        angles.append('blinkers_off')

    if pps and race:
        today_purse = float(race.purse or 0)
        last_purse = float(pps[0].purse or 0) if pps[0].purse else 0
        if today_purse > 0 and last_purse > 0:
            if today_purse < last_purse * 0.85:
                angles.append('class_drop')

    if pps and race:
        last_surface = pps[0].surface if pps else None
        if last_surface and race.surface and last_surface != race.surface:
            angles.append('surface_switch')

    if entry.jockey and pps and hasattr(pps[0], 'jockey_name'):
        if (pps[0].jockey_name and entry.jockey.jockey_name
                and pps[0].jockey_name.lower() != entry.jockey.jockey_name.lower()):
            angles.append('jockey_change')

    return angles


def query_angle_stats(conn, angle_name: str,
                      trainer_name: Optional[str] = None) -> dict:
    """
    Query historical angle performance.
    Returns {wins, starts} for this angle + optional trainer filter.
    """
    from shared.db import execute_one
    try:
        if trainer_name:
            row = execute_one(conn,
                "SELECT wins, starts FROM angle_stats "
                "WHERE angle_name = %s AND trainer_name = %s",
                (angle_name, trainer_name))
        else:
            row = execute_one(conn,
                "SELECT wins, starts FROM angle_stats "
                "WHERE angle_name = %s AND trainer_name IS NULL",
                (angle_name,))
        if row:
            return {'wins': int(row['wins']), 'starts': int(row['starts'])}
    except Exception:
        pass
    return {'wins': 0, 'starts': 0}


def score_entry_angles(entry, pps, race, conn, odds: float = 5.0) -> dict:
    """
    Full angle scoring for one entry.
    Returns best angle with posterior + EV.
    """
    angles = detect_angles(entry, pps, race)
    if not angles:
        return {
            'angle_name': None, 'angle_posterior': 0.0,
            'angle_ev': -2.0, 'angle_ci_low': 0.0,
            'angle_ci_high': 0.0, 'angle_count': 0,
        }

    trainer_name = entry.trainer.trainer_name if entry.trainer else None
    best = None

    for angle in angles:
        # Try trainer-specific first
        stats = query_angle_stats(conn, angle, trainer_name)
        if stats['starts'] < 5 and trainer_name:
            # Fall back to global
            stats = query_angle_stats(conn, angle)

        scored = score_angle(stats['wins'], stats['starts'], odds)
        scored['angle_name'] = angle

        if best is None or scored['ev_per_bet'] > best['ev_per_bet']:
            best = scored

    if best is None:
        return {
            'angle_name': None, 'angle_posterior': 0.0,
            'angle_ev': -2.0, 'angle_ci_low': 0.0,
            'angle_ci_high': 0.0, 'angle_count': 0,
        }

    return {
        'angle_name': best['angle_name'],
        'angle_posterior': best['posterior_mean'],
        'angle_ev': best['ev_per_bet'],
        'angle_ci_low': best['ci_low'],
        'angle_ci_high': best['ci_high'],
        'angle_count': len(angles),
    }
