"""
Morning email Lambda — runs 07:00 ET daily via EventBridge.

Generates pre-race report, persists strategy_recommendations to DB,
sends HTML summary email via SES with link to dashboard.

Required env vars:
  RECIPIENT_EMAIL — Tony's address
  SENDER_EMAIL    — SES-verified sender
  DASHBOARD_URL   — base URL of dashboard (e.g. https://eq.example.com/reports/daily)
  DB_SECRET_ARN   — db credentials
"""
import json
import logging
import os
from datetime import date

import boto3
from psycopg2.extras import execute_values

from shared.db import get_db
from services.daily_report_generator import DailyReportGenerator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

RECIPIENT = os.environ.get('RECIPIENT_EMAIL', 'tonyragano@gmail.com')
SENDER = os.environ.get('SENDER_EMAIL', 'reports@equine-equalizer.com')
DASHBOARD_URL = os.environ.get('DASHBOARD_URL', 'https://eq.example.com/reports/daily')


def handler(event, context):
    race_date = date.today()
    # Allow override via event payload (for backfill / re-runs)
    if isinstance(event, dict) and event.get('race_date'):
        from datetime import datetime
        race_date = datetime.strptime(event['race_date'], '%Y-%m-%d').date()

    logger.info(f"Generating morning report for {race_date}")
    with get_db() as conn:
        gen = DailyReportGenerator(conn)
        report = gen.generate_pre_race_report(race_date)
        # Persist recommendations to DB
        _persist_recommendations(conn, report, race_date)

    html = _render_html(report, race_date)
    subject = f"EE Daily Report — {race_date} — {report['race_count']} races"
    _send_email(subject, html)
    return {'statusCode': 200, 'body': json.dumps({
        'race_date': str(race_date),
        'races': report['race_count'],
        'errors': len(report['errors']),
    })}


def _persist_recommendations(conn, report, race_date):
    """Insert strategy_recommendations rows for the day."""
    rows = []
    # Single-race recs
    for r in report['races']:
        for sname, rec in (r.get('strategy_recommendations') or {}).items():
            if rec is None: continue
            rows.append((
                r['race_id'], race_date, sname, rec['bet_type'],
                json.dumps(rec.get('horses') or []),
                None, None,  # legs / leg_race_ids for single-race
                float(rec['stake']),
                float(rec['confidence']) if rec.get('confidence') is not None else None,
                rec.get('rationale') or '',
                json.dumps(rec.get('metadata') or {}),
            ))
    # Multi-leg recs
    for ml in report.get('multi_leg_recommendations') or []:
        rows.append((
            ml['race_id'], race_date, ml['strategy_name'], ml['bet_type'],
            json.dumps(ml.get('horses') or []),
            json.dumps(ml.get('legs') or []),
            json.dumps(ml.get('leg_race_ids') or []),
            float(ml['stake']),
            float(ml['confidence']) if ml.get('confidence') is not None else None,
            ml.get('rationale') or '',
            json.dumps(ml.get('metadata') or {}),
        ))
    if not rows: return
    with conn.cursor() as cur:
        execute_values(cur, """
            INSERT INTO strategy_recommendations
              (race_id, race_date, strategy_name, bet_type,
               horses_json, legs_json, leg_race_ids_json,
               stake, confidence, rationale, metadata_json)
            VALUES %s
        """, rows)
    logger.info(f"Persisted {len(rows)} strategy_recommendations rows")


def _render_html(report, race_date):
    """Compact HTML email — summary only; link to dashboard for full detail."""
    races = report['races']
    hc_races = [r for r in races if r.get('consensus_signals', {}).get('high_conviction_flag')]
    ne_races = [r for r in races if r.get('consensus_signals', {}).get('no_edge_flag')]

    html = f"""<html><body style="font-family: -apple-system, sans-serif; max-width: 720px;">
    <h2 style="color:#1a3d6d;">EE Daily Report — {race_date}</h2>
    <p style="color:#555;">{report['race_count']} races across {len({r['track'] for r in races})} tracks.
    {len(report['multi_leg_recommendations'])} multi-leg recommendations.
    {report['strategy_count']} strategies running ({report['strategy_categories']}).</p>

    <h3 style="color:#1a3d6d;">High-conviction races ({len(hc_races)})</h3>
    """
    if hc_races:
        html += "<table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;font-size:13px;'>"
        html += "<tr style='background:#eef;'><th>Track</th><th>R#</th><th>Top Pick (consensus)</th><th>Bet-type consensus</th><th>Active / Skip</th></tr>"
        for r in hc_races[:30]:
            cs = r['consensus_signals']
            tp = cs.get('top_pick_consensus') or {}
            btc = cs.get('bet_type_consensus') or {}
            html += f"<tr><td>{r['track']}</td><td>{r['race_number']}</td>"
            html += f"<td><b>{tp.get('horse_name','—')}</b> ({tp.get('strategies_agreeing','—')} strategies, {tp.get('consensus_strength','')})</td>"
            html += f"<td>{btc.get('dominant_bet_type','—')} ({btc.get('strategies_recommending','—')})</td>"
            html += f"<td>{r['skip_stats']['active_count']} / {r['skip_stats']['skips_count']}</td></tr>"
        html += "</table>"
    else:
        html += "<p style='color:#777;'>No high-conviction races today (no race has 15+ strategies agreeing on top pick).</p>"

    html += f"<h3 style='color:#1a3d6d;'>No-edge races ({len(ne_races)} of {len(races)})</h3>"
    if ne_races:
        html += "<p style='color:#777;font-size:12px;'>Skip-rate > 75% on these — substrate signal suggests sit out:</p>"
        html += "<p style='font-size:12px;'>"
        for r in ne_races[:40]:
            html += f"{r['track']} R{r['race_number']} ({r['skip_stats']['skip_rate']*100:.0f}% skip) &nbsp;"
        html += "</p>"

    # Per-strategy historical context snapshot (top by 7d ROI)
    hist = report.get('historical_context', {})
    if hist:
        rolling_perf = [
            (name, ctx['rolling_7d']) for name, ctx in hist.items()
            if ctx['rolling_7d']['n'] > 0
        ]
        rolling_perf.sort(key=lambda x: x[1].get('roi') or -999, reverse=True)
        html += "<h3 style='color:#1a3d6d;'>Strategy 7-day rolling P&L (top 10)</h3>"
        html += "<table border='1' cellpadding='4' cellspacing='0' style='border-collapse:collapse;font-size:12px;'>"
        html += "<tr style='background:#eef;'><th>Strategy</th><th>Bets</th><th>Wins</th><th>Stake</th><th>P&L</th><th>ROI</th></tr>"
        for name, agg in rolling_perf[:10]:
            html += f"<tr><td>{name}</td><td>{agg['n']}</td><td>{agg['wins']}</td>"
            html += f"<td>${agg['stake']:.0f}</td><td>${agg['pnl']:+.0f}</td><td>{agg.get('roi','—')}%</td></tr>"
        html += "</table>"

    html += f"""
    <h3 style="color:#1a3d6d;">Full report</h3>
    <p><a href="{DASHBOARD_URL}/{race_date}" style="color:#1a3d6d;font-weight:bold;">→ Open dashboard for full race-by-race detail, layer outputs, all 78 strategies</a></p>
    <p style="color:#999;font-size:11px;">Generated {report['generated_at']}. Errors: {len(report['errors'])}.</p>
    </body></html>"""
    return html


def _send_email(subject, html):
    ses = boto3.client('ses', region_name='us-east-1')
    ses.send_email(
        Source=SENDER,
        Destination={'ToAddresses': [RECIPIENT]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Html': {'Data': html}},
        }
    )
    logger.info(f"Sent email to {RECIPIENT}; subject: {subject}")
