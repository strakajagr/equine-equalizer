import json
import logging
from shared.db import get_db, execute_query

logger = logging.getLogger(__name__)


def _response(status_code: int, body: dict) -> dict:
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, default=str)
    }


def get_horse_pps(event: dict, context) -> dict:
    """
    GET /horses/{horse_id}/pps
    Returns last 10 past performances with full detail.
    """
    try:
        path_params = event.get('pathParameters') or {}
        horse_id = path_params.get('horse_id')
        if not horse_id:
            return _response(400, {'error': 'horse_id required'})

        params = event.get('queryStringParameters') or {}
        limit = int(params.get('limit', '10'))

        from repositories.past_performance_repository \
            import PastPerformanceRepository
        from repositories.horse_repository \
            import HorseRepository

        with get_db() as conn:
            pp_repo = PastPerformanceRepository(conn)
            pps = pp_repo.get_past_performances(
                horse_id, limit=limit
            )

            horse_repo = HorseRepository(conn)
            horse = horse_repo.get_horse_by_id(horse_id)

            figures = pp_repo.get_speed_figures_last_n(
                horse_id, n=20
            )
            best_figure = pp_repo.get_best_speed_figure(
                horse_id
            )

            # Get model predictions for this horse's races
            pred_map = {}
            if pps:
                race_dates = list(set(
                    str(pp.race_date) for pp in pps
                    if pp.race_date
                ))
                if race_dates:
                    rows = execute_query(
                        conn,
                        """SELECT p.predicted_rank,
                                  r.race_date, r.track_id
                           FROM predictions p
                           JOIN races r ON p.race_id = r.race_id
                           WHERE p.horse_id = %s""",
                        (horse_id,)
                    )
                    for r in rows:
                        key = str(r['race_date'])
                        pred_map[key] = r['predicted_rank']

            return _response(200, {
                'horse_id': horse_id,
                'horse_name': (
                    horse.horse_name if horse else None
                ),
                'sire': horse.sire if horse else None,
                'dam': horse.dam if horse else None,
                'dam_sire': (
                    horse.dam_sire if horse else None
                ),
                'sex': horse.sex if horse else None,
                'country': (
                    horse.country_of_origin
                    if horse else None
                ),
                'best_speed_figure': best_figure,
                'speed_figures': figures,
                'past_performances': [
                    _serialize_pp(pp, pred_map)
                    for pp in pps
                ]
            })
    except Exception as e:
        logger.error(f"get_horse_pps error: {e}")
        return _response(500, {'error': str(e)})


SURFACE_MAP = {
    'dirt': 'Dirt', 'd': 'Dirt',
    'turf': 'Turf', 't': 'Turf',
    'synthetic': 'Synth', 'aw': 'AW',
    'all_weather': 'AW',
}


def _fmt_finish(pos):
    """Format finish position for display."""
    if pos is None:
        return None
    if pos >= 90:
        return 'SCR'
    if pos == 0:
        return None
    return pos


def _serialize_pp(pp, pred_map=None) -> dict:
    """Full PP serialization for horse detail drawer."""
    race_date_str = (
        str(pp.race_date) if pp.race_date else None
    )
    surface = SURFACE_MAP.get(
        (pp.surface or '').lower(),
        pp.surface
    )
    mdl_rank = (
        pred_map.get(race_date_str)
        if pred_map and race_date_str else None
    )

    return {
        'race_date': race_date_str,
        'track_code': pp.track_code,
        'race_number': pp.race_number,
        'distance_furlongs': pp.distance_furlongs,
        'surface': surface,
        'race_type': pp.race_type,
        'purse': pp.purse,
        'field_size': pp.field_size,
        'track_condition': pp.track_condition,
        'post_position': pp.post_position,
        'finish_position': _fmt_finish(pp.finish_position),
        'official_finish': _fmt_finish(pp.official_finish),
        'lengths_behind': pp.lengths_behind,
        'beyer_speed_figure': pp.beyer_speed_figure,
        'final_time': pp.final_time,
        'closing_odds': pp.closing_odds,
        'jockey_name': pp.jockey_name,
        'trainer_name': pp.trainer_name,
        'weight_carried': pp.weight_carried,
        'comment': pp.comment,
        # Running positions at each call
        'call_1_position': pp.call_1_position,
        'call_1_lengths': pp.call_1_lengths,
        'call_2_position': pp.call_2_position,
        'call_2_lengths': pp.call_2_lengths,
        'call_3_position': (
            pp.call_3_position
            if hasattr(pp, 'call_3_position') else None
        ),
        'stretch_position': pp.stretch_position,
        'stretch_lengths': pp.stretch_lengths,
        # Fractional times
        'fraction_1': pp.fraction_1,
        'fraction_2': pp.fraction_2,
        'fraction_3': pp.fraction_3,
        'horse_fraction_1': (
            pp.horse_fraction_1
            if hasattr(pp, 'horse_fraction_1') else None
        ),
        'horse_fraction_2': (
            pp.horse_fraction_2
            if hasattr(pp, 'horse_fraction_2') else None
        ),
        # Style and context
        'running_style': pp.running_style,
        'days_since_last_race': pp.days_since_last_race,
        'lasix': pp.lasix,
        'lasix_first_time': pp.lasix_first_time,
        'blinkers_on': pp.blinkers_on,
        'claiming_price_entered': pp.claiming_price_entered,
        # Model prediction for this race
        'model_rank': mdl_rank,
    }
