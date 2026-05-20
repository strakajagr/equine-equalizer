"""Outcome metric publisher for EE outcome-class CloudWatch alarms.

Publishes EquineEqualizer/Outcomes namespace metrics for results, entries,
workouts. Each invocation handles ONE metric (per EventBridge rule input).

Failure modes detected by these metrics (and corresponding alarms):
- Lambda invokes successfully but writes zero rows (silent scraper failure,
  parser regression, DB write path failure)
- EventBridge fires but Lambda async invocation gets dropped silently
  (Lambda Inactive state due to ECR image cull)
- Local manual scrape (workouts) stops without external notification

Independent of equine-ingestion pipeline by design: queries DB directly via
psycopg2; if ingestion Lambda is Inactive this Lambda still publishes the
metric (which will then be 0, triggering the alarm).
"""
import json
import logging
import os
from datetime import date, datetime, timedelta, timezone

import boto3
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REGION = os.environ.get("AWS_REGION", "us-east-1")
SECRET_ID = os.environ.get(
    "DB_SECRET_ID", "equine-equalizer/db-credentials"
)
RAW_DATA_BUCKET = os.environ.get(
    "RAW_DATA_BUCKET", "equine-raw-data"
)
WORKOUTS_S3_PREFIX = "workout-loads/"
METRIC_NAMESPACE = "EquineEqualizer/Outcomes"

_secret_cache = None
_sm_client = boto3.client("secretsmanager", region_name=REGION)
_s3_client = boto3.client("s3", region_name=REGION)
_cw_client = boto3.client("cloudwatch", region_name=REGION)


def _get_db_connection():
    global _secret_cache
    if _secret_cache is None:
        _secret_cache = json.loads(
            _sm_client.get_secret_value(SecretId=SECRET_ID)[
                "SecretString"
            ]
        )
    s = _secret_cache
    return psycopg2.connect(
        host=s["host"],
        port=s["port"],
        dbname=s["dbname"],
        user=s["username"],
        password=s["password"],
        connect_timeout=10,
    )


def _count_results_today_minus_1() -> int:
    target = (datetime.now(timezone.utc).date() - timedelta(days=1))
    sql = (
        "SELECT COUNT(res.result_id) "
        "FROM results res "
        "JOIN entries e ON res.entry_id = e.entry_id "
        "JOIN races r ON e.race_id = r.race_id "
        "WHERE r.race_date = %s"
    )
    with _get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (target,))
        return int(cur.fetchone()[0])


def _count_workouts_objects_today() -> int:
    today_utc = datetime.now(timezone.utc).date()
    cutoff = datetime.combine(
        today_utc, datetime.min.time(), tzinfo=timezone.utc
    )
    paginator = _s3_client.get_paginator("list_objects_v2")
    count = 0
    for page in paginator.paginate(
        Bucket=RAW_DATA_BUCKET, Prefix=WORKOUTS_S3_PREFIX
    ):
        for obj in page.get("Contents", []):
            if obj["LastModified"] >= cutoff:
                count += 1
    return count


def _publish_metric(metric_name: str, value: float) -> None:
    _cw_client.put_metric_data(
        Namespace=METRIC_NAMESPACE,
        MetricData=[
            {
                "MetricName": metric_name,
                "Value": value,
                "Unit": "Count",
                "Timestamp": datetime.now(timezone.utc),
            }
        ],
    )


def lambda_handler(event, context):
    metric = (event or {}).get("metric", "").lower()
    logger.info(f"outcome_metrics handler invoked: metric={metric}")

    if metric == "results":
        n = _count_results_today_minus_1()
        _publish_metric("ResultsRowsToday", float(n))
        logger.info(f"published ResultsRowsToday={n}")
    elif metric == "workouts":
        n = _count_workouts_objects_today()
        _publish_metric("WorkoutsObjectsToday", float(n))
        logger.info(f"published WorkoutsObjectsToday={n}")
    else:
        raise ValueError(
            f"Unknown metric: {metric!r} "
            "(expected results|workouts)"
        )
    return {"metric": metric, "value": n}
