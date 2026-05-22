#!/bin/bash
# Gate 6 — launch parse_charts Lambda for Sep 2025 → present in parallel.
# Covers both Bug #28 (running_style/trainer_name 2026-04-30+) and
# Sep-2025 cliff (weight_carried, weather, results positions).
set -uo pipefail

LOGDIR=/tmp/gate6_reparse_logs
mkdir -p "$LOGDIR"
START_DATE="2025-09-01"
END_DATE="2026-05-21"
REGION="us-east-1"
MAX_PARALLEL=8

# Build date list
DATES=$(python3 -c "
from datetime import date, timedelta
d = date.fromisoformat('$START_DATE')
end = date.fromisoformat('$END_DATE')
while d <= end:
    print(d.strftime('%Y%m%d'))
    d += timedelta(days=1)
")

echo "$(date) — re-parse: $START_DATE → $END_DATE, max_parallel=$MAX_PARALLEL"
total=$(echo "$DATES" | wc -l)
echo "Total dates: $total"

# Use xargs for parallelism
i=0
echo "$DATES" | xargs -P $MAX_PARALLEL -I {} bash -c '
  d={}
  aws lambda invoke --function-name equine-ingestion \
    --payload "{\"action\":\"parse_charts\",\"date_from\":\"$d\",\"date_to\":\"$d\"}" \
    --cli-binary-format raw-in-base64-out --region '"$REGION"' \
    --cli-read-timeout 300 "'"$LOGDIR"'/$d.json" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    rl=$(python3 -c "import json; d=json.load(open(\"'"$LOGDIR"'/$d.json\")); print(json.loads(d[\"body\"]).get(\"races_loaded\", \"?\")) " 2>/dev/null || echo "?")
    echo "$(date +%H:%M:%S) $d races_loaded=$rl"
  else
    echo "$(date +%H:%M:%S) $d FAILED"
  fi
'

echo "$(date) — re-parse loop complete"
echo "Logs: $LOGDIR"
