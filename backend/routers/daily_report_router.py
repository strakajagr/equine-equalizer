"""
Daily report router — HTTP endpoints for the multi-strategy daily report.

Endpoints (consumed by frontend DailyReportPage.tsx):
  GET /api/reports/daily/{race_date}        → full pre-race report JSON
  GET /api/reports/strategy/{name}/history  → rolling P&L per strategy
  GET /api/reports/strategy/list            → registry listing (names + descriptions)
  GET /api/reports/strategy_pnl/range       → strategy_pnl rows over a date range
"""
import json
import logging
from datetime import date, datetime, timedelta
from shared.db import get_db
from services.daily_report_generator import DailyReportGenerator
from services.strategy_registry import get_registry, registry_size_by_category

logger = logging.getLogger(__name__)


def _cors_response(status_code=200, body=''):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': body if isinstance(body, str) else json.dumps(body, default=str),
    }


def get_daily_report(event, context):
    """GET /api/reports/daily/{race_date}
    race_date in URL path; format YYYY-MM-DD."""
    path = event.get('rawPath', '')
    path_parts = path.strip('/').split('/')
    try:
        race_date_str = path_parts[-1]
        race_date = datetime.strptime(race_date_str, '%Y-%m-%d').date()
    except (ValueError, IndexError) as e:
        return _cors_response(400, {'error': f'Invalid race_date in path: {e}'})

    with get_db() as conn:
        gen = DailyReportGenerator(conn)
        report = gen.generate_pre_race_report(race_date)
    return _cors_response(200, report)


def get_strategy_history(event, context):
    """GET /api/reports/strategy/{name}/history?days=30"""
    path = event.get('rawPath', '')
    parts = path.strip('/').split('/')
    try:
        strategy_name = parts[parts.index('strategy') + 1]
    except (ValueError, IndexError):
        return _cors_response(400, {'error': 'Invalid path; expected /api/reports/strategy/{name}/history'})
    qs = event.get('queryStringParameters') or {}
    days = int(qs.get('days', 30))
    cutoff = date.today() - timedelta(days=days)

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT race_date,
                  COUNT(*) AS n,
                  SUM(stake)::float AS stake,
                  SUM(payout)::float AS payout,
                  SUM(pnl)::float AS pnl,
                  SUM(CASE WHEN is_win THEN 1 ELSE 0 END) AS wins
                FROM strategy_pnl
                WHERE strategy_name = %s AND race_date >= %s
                GROUP BY race_date ORDER BY race_date DESC
            """, (strategy_name, cutoff))
            rows = [dict(r) for r in cur.fetchall()]
            # Cumulative P&L
            cur.execute("""
                SELECT SUM(pnl)::float AS total_pnl,
                       SUM(stake)::float AS total_stake,
                       SUM(payout)::float AS total_payout,
                       COUNT(*) AS total_bets,
                       SUM(CASE WHEN is_win THEN 1 ELSE 0 END) AS total_wins
                FROM strategy_pnl WHERE strategy_name = %s AND race_date >= %s
            """, (strategy_name, cutoff))
            agg = dict(cur.fetchone())
            # Per-track breakdown
            cur.execute("""
                SELECT t.track_code,
                  COUNT(*) AS n,
                  SUM(sp.stake)::float AS stake,
                  SUM(sp.pnl)::float AS pnl
                FROM strategy_pnl sp JOIN races r USING (race_id) JOIN tracks t USING (track_id)
                WHERE sp.strategy_name = %s AND sp.race_date >= %s
                GROUP BY t.track_code ORDER BY pnl DESC NULLS LAST
            """, (strategy_name, cutoff))
            by_track = [dict(r) for r in cur.fetchall()]

    return _cors_response(200, {
        'strategy_name': strategy_name, 'days': days,
        'by_date': rows, 'aggregate': agg, 'by_track': by_track,
    })


def get_strategy_list(event, context):
    """GET /api/reports/strategy/list"""
    registry = get_registry()
    listing = [
        {
            'name': s.name, 'description': s.description, 'category': s.category,
            'style': s.style, 'ranking_layer': s.ranking_layer,
            'is_multi_leg': s.is_multi_leg,
        }
        for s in registry
    ]
    return _cors_response(200, {
        'strategies': listing,
        'total': len(listing),
        'by_category': registry_size_by_category(),
    })


def get_strategy_pnl_range(event, context):
    """GET /api/reports/strategy_pnl/range?start=YYYY-MM-DD&end=YYYY-MM-DD
    Returns per-strategy aggregates across the range."""
    qs = event.get('queryStringParameters') or {}
    try:
        start = datetime.strptime(qs.get('start'), '%Y-%m-%d').date()
        end = datetime.strptime(qs.get('end'), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return _cors_response(400, {'error': 'start and end required (YYYY-MM-DD)'})
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT strategy_name,
                  COUNT(*) AS n_bets,
                  SUM(CASE WHEN is_win THEN 1 ELSE 0 END) AS wins,
                  SUM(stake)::float AS stake,
                  SUM(payout)::float AS payout,
                  SUM(pnl)::float AS pnl
                FROM strategy_pnl
                WHERE race_date BETWEEN %s AND %s
                GROUP BY strategy_name
                ORDER BY pnl DESC NULLS LAST
            """, (start, end))
            rows = [dict(r) for r in cur.fetchall()]
            for r in rows:
                r['roi'] = round(r['pnl'] / r['stake'] * 100, 2) if r['stake'] else None
                r['win_rate'] = round(r['wins'] / r['n_bets'] * 100, 2) if r['n_bets'] else None
    return _cors_response(200, {
        'start': str(start), 'end': str(end), 'per_strategy': rows,
    })
