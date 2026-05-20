"""
Evening email Lambda — runs 23:30 ET daily via EventBridge.

Computes post-race P&L for the day (via DailyReportGenerator.generate_post_race_report),
persists to strategy_pnl, sends HTML evening-summary email with day's results.

Required env vars (same as morning):
  RECIPIENT_EMAIL, SENDER_EMAIL, DASHBOARD_URL, DB_SECRET_ARN
"""
import json
import logging
import os
from datetime import date

import boto3

from shared.db import get_db
from services.daily_report_generator import DailyReportGenerator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

RECIPIENT = os.environ.get('RECIPIENT_EMAIL', 'tonyragano@gmail.com')
SENDER = os.environ.get('SENDER_EMAIL', 'reports@equine-equalizer.com')
DASHBOARD_URL = os.environ.get('DASHBOARD_URL', 'https://eq.example.com/reports/daily')


def handler(event, context):
    race_date = date.today()
    if isinstance(event, dict) and event.get('race_date'):
        from datetime import datetime
        race_date = datetime.strptime(event['race_date'], '%Y-%m-%d').date()

    logger.info(f"Generating post-race report for {race_date}")
    with get_db() as conn:
        gen = DailyReportGenerator(conn)
        result = gen.generate_post_race_report(race_date)

    html = _render_html(result, race_date)
    subject = f"EE P&L — {race_date} — {result['n_recommendations']} bets evaluated"
    _send_email(subject, html)
    return {'statusCode': 200, 'body': json.dumps({
        'race_date': str(race_date),
        'n_recommendations': result['n_recommendations'],
    })}


def _render_html(result, race_date):
    per_strategy = result.get('per_strategy_pnl', {})
    total_stake = sum(s['stake'] for s in per_strategy.values())
    total_payout = sum(s['payout'] for s in per_strategy.values())
    total_pnl = sum(s['pnl'] for s in per_strategy.values())

    html = f"""<html><body style="font-family: -apple-system, sans-serif; max-width: 720px;">
    <h2 style="color:#1a3d6d;">EE Evening P&L — {race_date}</h2>
    <p style="color:#555;">{result['n_recommendations']} bets evaluated across {len(per_strategy)} strategies.</p>

    <table border='0' cellpadding='8' style='font-size:14px;background:#f5f7fb;'>
      <tr><td><b>Total stake:</b></td><td>${total_stake:.2f}</td></tr>
      <tr><td><b>Total payout:</b></td><td>${total_payout:.2f}</td></tr>
      <tr><td><b>Net P&L:</b></td><td style="color:{'#0a7a0a' if total_pnl >= 0 else '#a02020'};font-weight:bold;">${total_pnl:+.2f}</td></tr>
      <tr><td><b>ROI:</b></td><td>{(total_pnl/total_stake*100 if total_stake else 0):+.2f}%</td></tr>
    </table>

    <h3 style="color:#1a3d6d;">Top 10 strategies today</h3>
    <table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;font-size:13px;'>
    <tr style='background:#eef;'><th>Strategy</th><th>Bets</th><th>Wins</th><th>Stake</th><th>Payout</th><th>P&L</th><th>ROI</th></tr>
    """
    winners = result.get('top_winners') or []
    for name, st in winners[:10]:
        roi = (st['pnl']/st['stake']*100) if st['stake'] else 0
        color = '#0a7a0a' if st['pnl'] >= 0 else '#a02020'
        html += f"<tr><td>{name}</td><td>{st['n']}</td><td>{st['wins']}</td>"
        html += f"<td>${st['stake']:.0f}</td><td>${st['payout']:.0f}</td>"
        html += f"<td style='color:{color};font-weight:bold;'>${st['pnl']:+.0f}</td>"
        html += f"<td>{roi:+.1f}%</td></tr>"
    html += "</table>"

    html += "<h3 style='color:#1a3d6d;'>Worst 10 strategies today</h3>"
    html += "<table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;font-size:13px;'>"
    html += "<tr style='background:#fee;'><th>Strategy</th><th>Bets</th><th>Stake</th><th>P&L</th></tr>"
    losers = result.get('top_losers') or []
    for name, st in losers[:10]:
        html += f"<tr><td>{name}</td><td>{st['n']}</td><td>${st['stake']:.0f}</td>"
        html += f"<td style='color:#a02020;font-weight:bold;'>${st['pnl']:+.0f}</td></tr>"
    html += "</table>"

    html += f"""
    <h3 style="color:#1a3d6d;">Full breakdown</h3>
    <p><a href="{DASHBOARD_URL}/{race_date}/pnl" style="color:#1a3d6d;font-weight:bold;">→ Open dashboard for per-bet P&L + cumulative running totals</a></p>
    <p style="color:#999;font-size:11px;">Post-race P&L computed against actual race results from results table. Pari-mutuel payouts already include track takeout.</p>
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
    logger.info(f"Sent evening email to {RECIPIENT}")
