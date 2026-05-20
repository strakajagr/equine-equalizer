"""
Substrate-health monitor — runs daily before morning report.
Checks freshness of every critical EE substrate; emails Tony with red/yellow/green status.
"""
import os
import json
import logging
from datetime import datetime, date, timedelta

import boto3
import psycopg2

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

THRESHOLDS = {
    'chart_pipeline_stale_days': 1,
    'hrn_results_stale_hours': 30,
    'past_performances_stale_days': 2,
    'workouts_stale_hours': 30,
    'wr_predictions_stale_hours': 30,
    'lambda_error_threshold_24h': 5,
    'model_artifact_stale_days_warning': 60,
}


def handler(event, context):
    db_conn = _get_db_conn()
    s3 = boto3.client('s3')
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
    logs = boto3.client('logs', region_name='us-east-1')

    checks = []
    checks.append(_check_chart_pipeline(s3))
    checks.append(_check_hrn_results(db_conn))
    checks.append(_check_past_performances(db_conn))
    checks.append(_check_workouts(db_conn))
    checks.append(_check_wr_predictions(db_conn))

    for rule in [
        'equine-morning-report-cron',
        'equine-evening-pnl-cron',
        'equine-wr-inference-daily',
        'equine-pl-inference-daily',
        'equine-ls-inference-daily',
        'equine-nyra-workouts-daily',
    ]:
        checks.append(_check_cron_fired(rule, cloudwatch))

    for fn in ['equine-inference', 'equine-ingestion',
               'equine-daily-morning-email', 'equine-daily-evening-email',
               'equine-wr-inference', 'equine-pl-inference', 'equine-ls-inference']:
        checks.append(_check_lambda_errors(fn, logs))

    checks.append(_check_active_model_artifacts(db_conn))

    db_conn.close()

    red = [c for c in checks if c['status'] == 'red']
    yellow = [c for c in checks if c['status'] == 'yellow']
    green = [c for c in checks if c['status'] == 'green']
    summary = {
        'timestamp': datetime.utcnow().isoformat(),
        'red_count': len(red),
        'yellow_count': len(yellow),
        'green_count': len(green),
        'checks': checks,
    }
    _send_email(summary)
    return {'statusCode': 200, 'body': json.dumps(summary, default=str)}


# ── Substrate freshness checks ──

def _check_chart_pipeline(s3):
    """Latest PDF in s3://equine-raw-data/charts/ — pages through results."""
    try:
        latest = None
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket='equine-raw-data', Prefix='charts/'):
            for obj in page.get('Contents', []):
                if not obj['Key'].endswith('.pdf'):
                    continue
                if latest is None or obj['LastModified'] > latest:
                    latest = obj['LastModified']
        if latest is None:
            return {'name': 'chart_pipeline', 'status': 'red',
                    'detail': 'No PDFs found in S3 charts/'}
        age_days = (datetime.now(latest.tzinfo) - latest).days
        status = 'red' if age_days > THRESHOLDS['chart_pipeline_stale_days'] else 'green'
        return {'name': 'chart_pipeline', 'status': status,
                'detail': f'Latest PDF age: {age_days}d',
                'latest_pdf_timestamp': latest.isoformat()}
    except Exception as e:
        return {'name': 'chart_pipeline', 'status': 'red',
                'detail': f'Check failed: {type(e).__name__}: {str(e)[:200]}'}


def _check_hrn_results(db_conn):
    with db_conn.cursor() as cur:
        cur.execute("""
            SELECT MAX(created_at) FROM results WHERE finish_position IS NOT NULL
        """)
        latest = cur.fetchone()[0]
    if not latest:
        return {'name': 'hrn_results', 'status': 'red', 'detail': 'No results rows'}
    age_h = (datetime.now(latest.tzinfo) - latest).total_seconds() / 3600
    status = 'red' if age_h > THRESHOLDS['hrn_results_stale_hours'] else 'green'
    return {'name': 'hrn_results', 'status': status,
            'detail': f'Latest results row: {age_h:.1f}h ago',
            'latest_insert': latest.isoformat()}


def _check_past_performances(db_conn):
    with db_conn.cursor() as cur:
        cur.execute("SELECT MAX(race_date) FROM past_performances")
        latest_pp_date = cur.fetchone()[0]
    if not latest_pp_date:
        return {'name': 'past_performances', 'status': 'red', 'detail': 'No PPs'}
    age = (date.today() - latest_pp_date).days
    status = 'red' if age > THRESHOLDS['past_performances_stale_days'] else 'green'
    return {'name': 'past_performances', 'status': status,
            'detail': f'Latest PP race_date: {latest_pp_date} ({age}d stale)'}


def _check_workouts(db_conn):
    with db_conn.cursor() as cur:
        cur.execute("SELECT MAX(created_at) FROM workouts")
        latest = cur.fetchone()[0]
    if not latest:
        return {'name': 'workouts', 'status': 'yellow', 'detail': 'No workouts rows'}
    age_h = (datetime.now(latest.tzinfo) - latest).total_seconds() / 3600
    status = 'red' if age_h > THRESHOLDS['workouts_stale_hours'] else 'green'
    return {'name': 'workouts', 'status': status,
            'detail': f'Latest workout insert: {age_h:.1f}h ago'}


def _check_wr_predictions(db_conn):
    with db_conn.cursor() as cur:
        cur.execute("SELECT MAX(created_at) FROM wr_predictions")
        latest = cur.fetchone()[0]
    if not latest:
        return {'name': 'wr_predictions', 'status': 'red', 'detail': 'No predictions'}
    age_h = (datetime.now(latest.tzinfo) - latest).total_seconds() / 3600
    status = 'red' if age_h > THRESHOLDS['wr_predictions_stale_hours'] else 'green'
    return {'name': 'wr_predictions', 'status': status,
            'detail': f'Latest wr_prediction: {age_h:.1f}h ago'}


def _check_cron_fired(rule_name, cloudwatch):
    try:
        end = datetime.utcnow()
        start = end - timedelta(hours=24)
        resp = cloudwatch.get_metric_statistics(
            Namespace='AWS/Events',
            MetricName='Invocations',
            Dimensions=[{'Name': 'RuleName', 'Value': rule_name}],
            StartTime=start, EndTime=end,
            Period=86400, Statistics=['Sum'],
        )
        if not resp['Datapoints']:
            return {'name': f'cron_{rule_name}', 'status': 'yellow',
                    'detail': 'No CloudWatch metrics (rule may not exist or not fired in 24h)'}
        invocations = int(resp['Datapoints'][0]['Sum'])
        status = 'green' if invocations >= 1 else 'red'
        return {'name': f'cron_{rule_name}', 'status': status,
                'detail': f'Invocations in 24h: {invocations}'}
    except Exception as e:
        return {'name': f'cron_{rule_name}', 'status': 'yellow',
                'detail': f'Check failed: {type(e).__name__}'}


def _check_lambda_errors(fn_name, logs):
    try:
        log_group = f'/aws/lambda/{fn_name}'
        end = int(datetime.utcnow().timestamp() * 1000)
        start = end - 24 * 3600 * 1000
        resp = logs.filter_log_events(
            logGroupName=log_group,
            startTime=start, endTime=end,
            filterPattern='ERROR',
            limit=THRESHOLDS['lambda_error_threshold_24h'] + 5,
        )
        count = len(resp.get('events', []))
        status = 'red' if count > THRESHOLDS['lambda_error_threshold_24h'] else 'green'
        return {'name': f'lambda_errors_{fn_name}', 'status': status,
                'detail': f'Errors in 24h: {count}'}
    except Exception as e:
        if 'ResourceNotFound' in type(e).__name__:
            return {'name': f'lambda_errors_{fn_name}', 'status': 'yellow',
                    'detail': 'Log group not found'}
        return {'name': f'lambda_errors_{fn_name}', 'status': 'yellow',
                'detail': f'Check failed: {type(e).__name__}'}


def _check_active_model_artifacts(db_conn):
    with db_conn.cursor() as cur:
        cur.execute("""
            SELECT model_type, version_name, training_date,
                   EXTRACT(DAY FROM (now() - training_date))::int AS age_days
            FROM model_versions
            WHERE is_active = TRUE
              AND training_date < now() - INTERVAL '60 days'
            ORDER BY training_date ASC
        """)
        stale = cur.fetchall()
    if not stale:
        return {'name': 'model_artifacts', 'status': 'green',
                'detail': 'All active artifacts < 60d old'}
    return {'name': 'model_artifacts', 'status': 'yellow',
            'detail': f'{len(stale)} active artifacts > 60d old',
            'stale_artifacts': [
                {'model_type': r[0], 'version': r[1], 'age_days': r[3]} for r in stale[:10]
            ]}


# ── Email rendering + send ──

def _render_html_summary(summary):
    BADGE = {
        'red':    "<span style='background:#c52b2b;color:white;padding:2px 8px;border-radius:3px;font-weight:bold;'>RED</span>",
        'yellow': "<span style='background:#d8a020;color:white;padding:2px 8px;border-radius:3px;font-weight:bold;'>YELLOW</span>",
        'green':  "<span style='background:#1a8a1a;color:white;padding:2px 8px;border-radius:3px;font-weight:bold;'>GREEN</span>",
    }
    red = [c for c in summary['checks'] if c['status'] == 'red']
    yellow = [c for c in summary['checks'] if c['status'] == 'yellow']
    green = [c for c in summary['checks'] if c['status'] == 'green']

    html = [
        '<html><body style="font-family:-apple-system,sans-serif;max-width:760px;">',
        f"<h2 style='color:#1a3d6d;'>EE Substrate Health — {summary['timestamp'][:19]} UTC</h2>",
        f"<p style='color:#555;font-size:14px;'>"
        f"<b style='color:#c52b2b;'>{summary['red_count']} RED</b> &middot; "
        f"<b style='color:#d8a020;'>{summary['yellow_count']} YELLOW</b> &middot; "
        f"<b style='color:#1a8a1a;'>{summary['green_count']} GREEN</b></p>",
    ]

    def _section(title, items, default_color):
        if not items:
            return
        html.append(f"<h3 style='color:{default_color};margin-top:20px;'>{title}</h3>")
        html.append("<table cellpadding='6' cellspacing='0' "
                    "style='border-collapse:collapse;font-size:13px;width:100%;'>")
        html.append("<tr style='background:#f0f0f5;'><th align='left'>Check</th>"
                    "<th align='left'>Status</th><th align='left'>Detail</th></tr>")
        for c in items:
            html.append(
                f"<tr style='border-bottom:1px solid #eee;'>"
                f"<td><code>{c['name']}</code></td>"
                f"<td>{BADGE.get(c['status'], c['status'])}</td>"
                f"<td>{c.get('detail', '')}</td></tr>"
            )
        html.append("</table>")

    _section(f"Failing checks ({len(red)} red)", red, '#c52b2b')
    _section(f"Warning checks ({len(yellow)} yellow)", yellow, '#d8a020')
    _section(f"Healthy checks ({len(green)} green)", green, '#1a8a1a')

    html.append("<hr style='margin-top:20px;'><p style='color:#999;font-size:11px;'>"
                "Generated by equine-substrate-health-monitor. "
                "Fires daily at 06:55 EDT, 5 min before morning report.</p>")
    html.append("</body></html>")
    return "\n".join(html)


def _send_email(summary):
    ses = boto3.client('ses', region_name='us-east-1')
    html = _render_html_summary(summary)
    subject = (f"EE Substrate Health — {summary['red_count']} red, "
               f"{summary['yellow_count']} yellow, {summary['green_count']} green")
    recipients = _get_recipients()
    sender = os.environ.get('SENDER_EMAIL', 'tonyragano@gmail.com')
    for email in recipients:
        ses.send_email(
            Source=sender,
            Destination={'ToAddresses': [email]},
            Message={'Subject': {'Data': subject}, 'Body': {'Html': {'Data': html}}},
        )
        logger.info(f"Sent health-check email to {email}")


def _get_db_conn():
    secret_arn = os.environ['DB_SECRET_ARN']
    sm = boto3.client('secretsmanager', region_name='us-east-1')
    creds = json.loads(sm.get_secret_value(SecretId=secret_arn)['SecretString'])
    return psycopg2.connect(
        host=creds['host'], dbname=creds['dbname'],
        user=creds['username'], password=creds['password'],
        port=creds.get('port', 5432),
    )


def _get_recipients():
    """Try subscribers table; fall back to RECIPIENT_EMAIL env var."""
    fallback = [os.environ.get('RECIPIENT_EMAIL', 'tonyragano@gmail.com')]
    try:
        conn = _get_db_conn()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT email FROM subscribers
                WHERE active = TRUE AND ses_verified = TRUE
            """)
            emails = [r[0] for r in cur.fetchall()]
        conn.close()
        if emails:
            return emails
    except Exception as e:
        logger.info(f"subscribers table not available ({type(e).__name__}); using fallback")
    return fallback
