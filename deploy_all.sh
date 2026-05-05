#!/bin/bash
set -e
echo "═══════════════════════════════════════════"
echo "  Equine Equalizer — Full Deploy"
echo "═══════════════════════════════════════════"

REGION="us-east-1"
ACCOUNT="584812014683"
CF_DIST="E3KVZ579NXFT4Q"

# ── 1. Backend (CDK) ──────────────────────────
echo ""
echo "▸ Step 1: CDK deploy backend Lambdas..."
cd ~/projects/equine-equalizer/infrastructure/cdk
npm run build
CDK_DEFAULT_ACCOUNT=$ACCOUNT CDK_DEFAULT_REGION=$REGION \
  cdk deploy EquineComputeStack --require-approval never
echo "✓ Backend deployed"

# ── 2. Frontend ───────────────────────────────
echo ""
echo "▸ Step 2: Build + deploy frontend..."
cd ~/projects/equine-equalizer/frontend
npm run build
aws s3 sync build/ s3://equine-frontend --delete --region $REGION
aws cloudfront create-invalidation \
  --distribution-id $CF_DIST --paths '/*' --region $REGION \
  --query 'Invalidation.Status' --output text
echo "✓ Frontend deployed"

# ── 3. Run WR inference for today ─────────────
echo ""
echo "▸ Step 3: Running WR inference for today..."
aws lambda invoke --function-name equine-wr-inference \
  --payload '{"source":"batch","date":"'$(date +%Y-%m-%d)'"}' \
  --cli-binary-format raw-in-base64-out --region $REGION \
  --cli-read-timeout 300 /tmp/deploy_wr.json
cat /tmp/deploy_wr.json
echo ""
echo "✓ WR inference done"

# ── 4. Run PL inference for today ─────────────
echo ""
echo "▸ Step 4: Running PL inference for today..."
aws lambda invoke --function-name equine-pl-inference \
  --payload '{"source":"batch","date":"'$(date +%Y-%m-%d)'"}' \
  --cli-binary-format raw-in-base64-out --region $REGION \
  --cli-read-timeout 300 /tmp/deploy_pl.json
cat /tmp/deploy_pl.json
echo ""
echo "✓ PL inference done"

# ── 5. Fetch yesterday's results from HRN ────
echo ""
echo "▸ Step 5: Fetching results from HRN..."
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d)
aws lambda invoke --function-name equine-ingestion \
  --payload '{"action":"fetch_results","date":"'$YESTERDAY'"}' \
  --cli-binary-format raw-in-base64-out --region $REGION \
  --cli-read-timeout 300 /tmp/deploy_results.json
cat /tmp/deploy_results.json
echo ""
echo "✓ Results fetched"

# ── 6. Run evaluation matcher ─────────────────
echo ""
echo "▸ Step 6: Matching results to predictions..."
aws lambda invoke --function-name equine-results \
  --payload '{"date":"'$YESTERDAY'"}' \
  --cli-binary-format raw-in-base64-out --region $REGION \
  --cli-read-timeout 120 /tmp/deploy_eval.json
cat /tmp/deploy_eval.json
echo ""
echo "✓ Evaluation done"

# ── 7. Verify ─────────────────────────────────
echo ""
echo "═══════════════════════════════════════════"
echo "  Verification"
echo "═══════════════════════════════════════════"

echo ""
echo "▸ Active models:"
aws lambda invoke --function-name equine-ingestion \
  --payload '{"action":"raw_query","sql":"SELECT version_name, model_type, is_active FROM model_versions WHERE is_active = true ORDER BY model_type"}' \
  --cli-binary-format raw-in-base64-out --region $REGION \
  --cli-read-timeout 120 /tmp/deploy_models.json 2>/dev/null
python3 -c "
import json
with open('/tmp/deploy_models.json') as f:
    d = json.load(f)
for r in json.loads(d['body'])['rows']:
    print(f\"  {r['model_type']:10s} {r['version_name']:40s} active={r['is_active']}\")
"

echo ""
echo "▸ Today's predictions:"
curl -s "https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com/wr/predictions/$(date +%Y-%m-%d)" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'  {d[\"count\"]} predictions')
if d['predictions']:
    p=d['predictions'][0]
    print(f'  Sample: {p[\"horse_name\"]} — {p[\"win_probability\"]*100:.1f}%')
"

echo ""
echo "▸ Today's races via API:"
curl -s "https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com/races/$(date +%Y-%m-%d)" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'  {d[\"race_count\"]} races across {[t[\"track_code\"] for t in d[\"tracks\"]]}')
"

echo ""
echo "▸ Yesterday's results:"
curl -s "https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com/races/$YESTERDAY" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
has_results = any(p.get('actual_finish') for r in d.get('races',[]) for p in r.get('predictions',[]))
print(f'  {d[\"race_count\"]} races, results={has_results}')
if has_results:
    for r in d['races'][:1]:
        winner = next((p for p in r['predictions'] if p.get('was_win')), None)
        if winner:
            print(f'  R{r[\"race_number\"]} {r[\"track_code\"]} winner: {winner[\"horse_name\"]} (model rank #{winner[\"predicted_rank\"]})')
"

echo ""
echo "▸ Available dates (top 3):"
curl -s "https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com/races/available-dates" | \
  python3 -c "
import sys,json
for d in json.load(sys.stdin)['dates'][:3]:
    print(f'  {d[\"date\"]}  {d[\"race_count\"]}R  predictions={d[\"has_predictions\"]}')
"

echo ""
echo "═══════════════════════════════════════════"
echo "  Deploy complete. Check the frontend at:"
echo "  https://d4nlmxq220z0z.cloudfront.net"
echo "═══════════════════════════════════════════"
