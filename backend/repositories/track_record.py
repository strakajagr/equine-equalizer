"""Stream E2 — track-record aggregation helper.

Shared logic for wr/pl/ls track-record endpoints. Each repo provides a
fetch query that returns one row per pick with these columns:
  prediction_outcome  text   (win|place|show|lose|pending|scratched)
  flat_bet_pl         numeric  (NULL when winner with missing payout)
  race_date           date
  track_code          text

This module rolls those rows into the response payload.
"""
from __future__ import annotations
from collections import defaultdict
from typing import Optional


def aggregate_picks(rows: list[dict], window_days: int,
                    extra_dim: Optional[str] = None) -> dict:
    """Given a list of per-pick rows, return the response payload dict.

    rows: each must have keys prediction_outcome, flat_bet_pl, race_date, track_code.
          If extra_dim is given (e.g. 'style'), rows must also have that key
          and the result includes a by_<extra_dim> array.
    """
    n_predictions = len(rows)
    n_pending = sum(1 for r in rows if r['prediction_outcome'] == 'pending')
    n_settled = n_predictions - n_pending

    settled = [r for r in rows if r['prediction_outcome'] != 'pending']
    n_wins   = sum(1 for r in settled if r['prediction_outcome'] == 'win')
    n_places = sum(1 for r in settled
                   if r['prediction_outcome'] in ('win', 'place'))
    n_shows  = sum(1 for r in settled
                   if r['prediction_outcome'] in ('win', 'place', 'show'))

    pl_rows = [r for r in settled if r['flat_bet_pl'] is not None]
    n_pl_complete = len(pl_rows)
    flat_bet_pl_total = sum(float(r['flat_bet_pl']) for r in pl_rows)
    # ROI denominator = $2 per pick × n picks with complete payout data
    roi_denom = 2.0 * n_pl_complete
    flat_bet_roi_pct = (
        (flat_bet_pl_total / roi_denom) * 100 if roi_denom > 0 else None
    )
    data_completeness = (
        n_pl_complete / n_settled if n_settled > 0 else None
    )
    # winners_data_completeness — fraction of winners with non-NULL
    # flat_bet_pl (i.e. with ingested win_payout). Critical because the
    # chart-parser payout gap clusters disproportionately on winners,
    # making flat_bet_roi_pct misleading without this disclosure.
    # Frontend uses this metric to suppress ROI display when low.
    n_winners = n_wins  # alias for clarity
    n_winners_with_payout = sum(
        1 for r in settled
        if r['prediction_outcome'] == 'win' and r['flat_bet_pl'] is not None
    )
    winners_data_completeness = (
        n_winners_with_payout / n_winners if n_winners > 0 else None
    )

    # Per-day P/L for best/worst day
    per_day_pl: dict[str, list[dict]] = defaultdict(list)
    for r in pl_rows:
        per_day_pl[str(r['race_date'])].append(r)
    day_summaries = []
    for d, dr in per_day_pl.items():
        wins = sum(1 for x in dr if x['prediction_outcome'] == 'win')
        pl_total = sum(float(x['flat_bet_pl']) for x in dr)
        day_summaries.append({'date': d, 'wins': wins, 'pl': round(pl_total, 2)})
    best_day = max(day_summaries, key=lambda x: x['pl']) if day_summaries else None
    worst_day = min(day_summaries, key=lambda x: x['pl']) if day_summaries else None

    # Per-track breakdown
    per_track: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        if r.get('track_code'):
            per_track[r['track_code']].append(r)
    by_track = []
    for tc, tr in sorted(per_track.items()):
        n = len(tr)
        n_settled_t = sum(1 for x in tr if x['prediction_outcome'] != 'pending')
        wins_t = sum(1 for x in tr if x['prediction_outcome'] == 'win')
        pl_rows_t = [x for x in tr if x['flat_bet_pl'] is not None]
        pl_total_t = sum(float(x['flat_bet_pl']) for x in pl_rows_t)
        roi_t = (pl_total_t / (2.0 * len(pl_rows_t)) * 100
                 if pl_rows_t else None)
        by_track.append({
            'track_code': tc,
            'n': n,
            'wins': wins_t,
            'hit_rate': round(wins_t / n_settled_t * 100, 1) if n_settled_t else None,
            'roi': round(roi_t, 1) if roi_t is not None else None,
        })

    payload = {
        'window_days': window_days,
        'n_predictions': n_predictions,
        'n_settled': n_settled,
        'n_pending': n_pending,
        'wins': n_wins,
        'places': n_places,
        'shows': n_shows,
        'hit_rate_win':   round(n_wins / n_settled * 100, 1) if n_settled else None,
        'hit_rate_place': round(n_places / n_settled * 100, 1) if n_settled else None,
        'hit_rate_show':  round(n_shows / n_settled * 100, 1) if n_settled else None,
        'flat_bet_pl_total': round(flat_bet_pl_total, 2),
        'flat_bet_roi_pct': round(flat_bet_roi_pct, 2) if flat_bet_roi_pct is not None else None,
        'data_completeness': round(data_completeness, 3) if data_completeness is not None else None,
        'winners_data_completeness': (
            round(winners_data_completeness, 3)
            if winners_data_completeness is not None else None
        ),
        'best_day': best_day,
        'worst_day': worst_day,
        'by_track': by_track,
    }

    # Optional extra-dim breakdown (e.g., by_style)
    if extra_dim is not None:
        per_dim: dict[str, list[dict]] = defaultdict(list)
        for r in rows:
            v = r.get(extra_dim)
            if v is not None:
                per_dim[v].append(r)
        breakdown = []
        for k, dr in sorted(per_dim.items()):
            n = len(dr)
            n_settled_d = sum(1 for x in dr if x['prediction_outcome'] != 'pending')
            wins_d = sum(1 for x in dr if x['prediction_outcome'] == 'win')
            places_d = sum(1 for x in dr
                           if x['prediction_outcome'] in ('win', 'place'))
            pl_rows_d = [x for x in dr if x['flat_bet_pl'] is not None]
            pl_total_d = sum(float(x['flat_bet_pl']) for x in pl_rows_d)
            roi_d = (pl_total_d / (2.0 * len(pl_rows_d)) * 100
                     if pl_rows_d else None)
            comp_d = (len(pl_rows_d) / n_settled_d if n_settled_d else None)
            n_winners_d = wins_d
            n_winners_paid_d = sum(
                1 for x in dr
                if x['prediction_outcome'] == 'win' and x['flat_bet_pl'] is not None
            )
            wcomp_d = (n_winners_paid_d / n_winners_d if n_winners_d > 0 else None)
            breakdown.append({
                extra_dim: k,
                'n': n,
                'n_settled': n_settled_d,
                'wins': wins_d,
                'places': places_d,
                'hit_rate_win':   round(wins_d / n_settled_d * 100, 1) if n_settled_d else None,
                'hit_rate_place': round(places_d / n_settled_d * 100, 1) if n_settled_d else None,
                'roi': round(roi_d, 2) if roi_d is not None else None,
                'data_completeness': round(comp_d, 3) if comp_d is not None else None,
                'winners_data_completeness': (
                    round(wcomp_d, 3) if wcomp_d is not None else None
                ),
            })
        payload[f'by_{extra_dim}'] = breakdown

    return payload


VALID_WINDOW_DAYS = (7, 14, 30, 60, 90)


def parse_window_days(raw, default: int = 30) -> int:
    """Validate the days query param. Reject anything not in VALID_WINDOW_DAYS."""
    if raw is None or raw == '':
        return default
    try:
        n = int(raw)
    except (TypeError, ValueError):
        raise ValueError(f"days must be an integer; got {raw!r}")
    if n not in VALID_WINDOW_DAYS:
        raise ValueError(
            f"days must be one of {VALID_WINDOW_DAYS}; got {n}"
        )
    return n
