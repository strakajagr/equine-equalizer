#!/bin/bash
# Gate 6 §D-NYRA — backfill NYRA workouts for the Jan 2024 → Aug 2025 gap.
# Iterates dates, invokes equine-nyra-workouts Lambda per date.
# Each invocation scrapes SAR/BEL/AQU for that date and writes to workouts table.
# Note: NYRA only races at SAR/BEL/AQU certain times of year — many dates
# will return zero workouts (no NYRA meet). That's normal.
set -uo pipefail

LOGDIR=/tmp/gate6_nyra_workouts_logs
mkdir -p "$LOGDIR"
START_DATE="2024-01-01"
END_DATE="2025-08-31"
MAX_PARALLEL=4

DATES=$(python3 -c "
from datetime import date, timedelta
d = date.fromisoformat('$START_DATE')
end = date.fromisoformat('$END_DATE')
while d <= end:
    print(d.strftime('%Y-%m-%d'))
    d += timedelta(days=1)
")

total=$(echo "$DATES" | wc -l)
echo "$(date) — NYRA workouts backfill: $START_DATE → $END_DATE, total=$total dates, parallel=$MAX_PARALLEL"

echo "$DATES" | xargs -P $MAX_PARALLEL -I {} bash -c '
  d={}
  aws lambda invoke --function-name equine-nyra-workouts \
    --payload "{\"date\":\"$d\"}" \
    --cli-binary-format raw-in-base64-out --region us-east-1 \
    --cli-read-timeout 120 "'"$LOGDIR"'/$d.json" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    rl=$(python3 -c "import json; o=json.load(open(\"'"$LOGDIR"'/$d.json\")); b=o.get(\"body\",\"\");
print(json.loads(b).get(\"total_workouts\",\"?\") if b else \"NORESP\")" 2>/dev/null || echo "?")
    echo "$(date +%H:%M:%S) $d total_workouts=$rl"
  else
    echo "$(date +%H:%M:%S) $d FAILED"
  fi
'

echo "$(date) — NYRA backfill complete"
