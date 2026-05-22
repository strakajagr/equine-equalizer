#!/bin/bash
# Gate 6 Close §3 — full 2022→2026 chart re-parse to backfill is_disqualified.
# The chart_parser DQ-prefix detection landed via cdk deploy.
# Re-parsing ON CONFLICT UPDATES is_disqualified for races where chart
# has DQ-prefix horse names. Non-DQ races stay FALSE.
set -uo pipefail

LOGDIR=/tmp/gate6_close_reparse_logs
mkdir -p "$LOGDIR"
START_DATE="2022-01-01"
END_DATE="2026-05-22"
REGION="us-east-1"
MAX_PARALLEL=8

DATES=$(python3 -c "
from datetime import date, timedelta
d = date.fromisoformat('$START_DATE')
end = date.fromisoformat('$END_DATE')
while d <= end:
    print(d.strftime('%Y%m%d'))
    d += timedelta(days=1)
")

total=$(echo "$DATES" | wc -l)
echo "$(date) — DQ backfill re-parse: $START_DATE → $END_DATE, total=$total dates, parallel=$MAX_PARALLEL"

echo "$DATES" | xargs -P $MAX_PARALLEL -I {} bash -c '
  d={}
  aws lambda invoke --function-name equine-ingestion \
    --payload "{\"action\":\"parse_charts\",\"date_from\":\"$d\",\"date_to\":\"$d\"}" \
    --cli-binary-format raw-in-base64-out --region '"$REGION"' \
    --cli-read-timeout 300 "'"$LOGDIR"'/$d.json" > /dev/null 2>&1
  if [ $? -ne 0 ]; then echo "$(date +%H:%M:%S) $d FAILED"; fi
'

echo "$(date) — full re-parse complete"
echo "Logs: $LOGDIR"
