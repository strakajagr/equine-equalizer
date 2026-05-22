#!/bin/bash
# Retry the 11 failed dates one track at a time (per-track invocations
# fit under Lambda's 5-min timeout).
set -uo pipefail

LOGDIR=/tmp/gate6_reparse_retry_logs
mkdir -p "$LOGDIR"
REGION="us-east-1"

# 11 dates that timed out in the parallel launcher
FAILED_DATES=(
  20260404 20260418 20260419 20260424 20260425 20260426
  20260501 20260502 20260503 20260510 20260517
)
TRACKS=(AQU BEL CD DMR GP KEE MTH OP PIM SA SAR)

echo "$(date) — per-track retry: ${#FAILED_DATES[@]} dates × ${#TRACKS[@]} tracks = $((${#FAILED_DATES[@]} * ${#TRACKS[@]})) invocations"

ARGS=""
for d in "${FAILED_DATES[@]}"; do
  for t in "${TRACKS[@]}"; do
    ARGS+="$d:$t "
  done
done

echo "$ARGS" | tr ' ' '\n' | grep -v '^$' | xargs -P 12 -I {} bash -c '
  dt={}
  d=${dt%:*}
  t=${dt#*:}
  aws lambda invoke --function-name equine-ingestion \
    --payload "{\"action\":\"parse_charts\",\"track\":\"$t\",\"date_from\":\"$d\",\"date_to\":\"$d\"}" \
    --cli-binary-format raw-in-base64-out --region '"$REGION"' \
    --cli-read-timeout 300 "'"$LOGDIR"'/${d}_${t}.json" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    rl=$(python3 -c "import json; o=json.load(open(\"'"$LOGDIR"'/${d}_${t}.json\")); b=o.get(\"body\",\"\");
print(json.loads(b).get(\"races_loaded\",\"?\") if b else \"NORESP\")" 2>/dev/null || echo "?")
    echo "$(date +%H:%M:%S) $d/$t races=$rl"
  else
    echo "$(date +%H:%M:%S) $d/$t FAILED"
  fi
'

echo "$(date) — per-track retry done"
