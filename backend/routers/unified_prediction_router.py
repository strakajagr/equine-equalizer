import json
import logging
from shared.db import get_db
from shared.constants import is_qualifying_race_type

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


def get_unified_predictions(event: dict, context) -> dict:
    """GET /predictions/{date}/{track_code}/{race_number}
    Unified endpoint returning WR + PL + LS predictions for one race in
    a single payload, with race-level metadata. Built for SmartBoard so
    it can populate full race context with one API call instead of three.
    """
    try:
        pp = event.get('pathParameters') or {}
        qs = event.get('queryStringParameters') or {}
        date_str = pp.get('date')
        track_code = pp.get('track_code')
        race_number = int(pp.get('race_number'))
        style = qs.get('style', 'general')

        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
              SELECT r.race_id, r.race_type, r.claiming_price,
                     r.race_name,
                     (SELECT COUNT(*) FROM entries e
                      WHERE e.race_id = r.race_id
                        AND COALESCE(e.is_scratched, FALSE) = FALSE)
                       AS field_size
              FROM races r
              JOIN tracks t ON t.track_id = r.track_id
              WHERE r.race_date = %s
                AND t.track_code = %s
                AND r.race_number = %s
            """, (date_str, track_code, race_number))
            row = cur.fetchone()
            if not row:
                return _response(404, {
                    'error': (
                        f'race not found: {date_str} '
                        f'{track_code} R{race_number}'
                    )
                })

            race_id = row['race_id']

            from repositories.wr_prediction_repository import (
                WRPredictionRepository
            )
            from repositories.pl_prediction_repository import (
                PLPredictionRepository
            )
            from repositories.ls_prediction_repository import (
                LSPredictionRepository
            )
            wr_preds = WRPredictionRepository(
                conn
            ).get_predictions_by_race(race_id, style=style)
            pl_preds = PLPredictionRepository(
                conn
            ).get_predictions_by_race(race_id, style=style)
            ls_preds = LSPredictionRepository(
                conn
            ).get_predictions_by_race(race_id, style=style)

            from routers.wr_prediction_router import (
                _serialize_prediction as _ser_wr
            )
            from routers.pl_prediction_router import (
                _serialize_pl_prediction as _ser_pl
            )
            from routers.ls_prediction_router import (
                _serialize_ls_prediction as _ser_ls
            )

            response = {
                'date': date_str,
                'track_code': track_code,
                'race_number': race_number,
                'race_id': race_id,
                'race_name': row['race_name'],
                'field_size': row['field_size'],
                'predictions_skipped_reason': None,
                'predictions': {
                    'wr': [_ser_wr(p) for p in wr_preds],
                    'pl': [_ser_pl(p) for p in pl_preds],
                    'ls': [_ser_ls(p) for p in ls_preds],
                },
            }

            if not (wr_preds or pl_preds or ls_preds):
                if not is_qualifying_race_type(
                    row['race_type'], row['claiming_price']
                ):
                    response['predictions_skipped_reason'] = (
                        'non_qualifying_race_type'
                    )

            return _response(200, response)

    except Exception as e:
        logger.error(
            f"get_unified_predictions error: {e}", exc_info=True
        )
        return _response(500, {'error': str(e)})
