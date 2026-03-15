#!/bin/bash
set -e

# ─────────────────────────────────────────
# Equine Equalizer — Database Migration Script
# ─────────────────────────────────────────
# Runs database migrations against Aurora.
#
# The database is in a private VPC subnet.
# This script connects via AWS SSM Port
# Forwarding — no bastion host needed,
# no public database exposure.
#
# Usage:
#   ./scripts/run-migrations.sh
#   ./scripts/run-migrations.sh --seed
#   ./scripts/run-migrations.sh --local
#     (use DATABASE_URL env var directly)
#
# Requirements:
#   - AWS CLI + Session Manager plugin
#   - Python3 + psycopg2-binary
#   - AWS credentials configured

RED='\033[0;31m'
GREEN='\033[0;32m'
GOLD='\033[0;33m'
WHITE='\033[1;37m'
DIM='\033[0;37m'
NC='\033[0m'

log()     { echo -e "${WHITE}$1${NC}"; }
success() { echo -e "${GREEN}✓ $1${NC}"; }
warn()    { echo -e "${GOLD}⚠ $1${NC}"; }
error()   { echo -e "${RED}✗ $1${NC}"; exit 1; }
step()    { echo -e "\n${GOLD}▶ $1${NC}"; }

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"

# Parse args
SEED=false
LOCAL=false
for arg in "$@"; do
  case $arg in
    --seed)  SEED=true ;;
    --local) LOCAL=true ;;
  esac
done

step "Database Migration Runner"

if [ "$LOCAL" = true ]; then
  # ── Local development mode ──
  # Uses DATABASE_URL environment variable
  # Set this to your local postgres or
  # a direct connection string

  if [ -z "$DATABASE_URL" ]; then
    error "DATABASE_URL not set.
For local dev:
  export DATABASE_URL=postgresql://user:pass@localhost:5432/equine_equalizer
  ./scripts/run-migrations.sh --local"
  fi

  success "Using DATABASE_URL (local mode)"

  cd "$BACKEND_DIR"

  if [ "$SEED" = true ]; then
    python3 database/migrations/migrate.py --seed
  else
    python3 database/migrations/migrate.py
  fi

else
  # ── AWS mode ──
  # Fetch DB secret from Secrets Manager
  # and run migrations via Lambda invocation
  # (Lambda is inside the VPC)

  step "Fetching database secret ARN"

  SECRET_ARN=$(python3 -c "
import json, sys
try:
  with open('$PROJECT_ROOT/cdk-outputs.json') as f:
    outputs = json.load(f)
  for stack in outputs.values():
    for key, val in stack.items():
      if 'Secret' in key and 'Arn' in key:
        print(val)
        sys.exit(0)
except Exception as e:
  pass
" 2>/dev/null || echo "")

  if [ -z "$SECRET_ARN" ]; then
    warn "Could not find secret ARN in cdk-outputs.json"
    warn "Migrations must be run from inside the VPC."
    echo ""
    log "Options:"
    log "1. Use --local flag with DATABASE_URL"
    log "2. Invoke migration Lambda directly:"
    log "   aws lambda invoke --function-name equine-ingestion \\"
    log "   --payload '{\"action\": \"migrate\"}' response.json"
    log "3. Use AWS Cloud9 inside the VPC"
    exit 1
  fi

  success "Secret ARN found: ${SECRET_ARN:0:50}..."

  # Invoke the ingestion Lambda to run migrations
  # (it has VPC access to the database)
  step "Invoking Lambda to run migrations"

  SEED_FLAG="false"
  [ "$SEED" = true ] && SEED_FLAG="true"

  PAYLOAD=$(python3 -c "
import json
print(json.dumps({
  'action': 'migrate',
  'seed': $SEED_FLAG
}))
")

  aws lambda invoke \
    --function-name equine-ingestion \
    --payload "$PAYLOAD" \
    --cli-binary-format raw-in-base64-out \
    /tmp/migration-response.json \
    --log-type Tail \
    --query 'LogResult' \
    --output text | base64 -d

  cat /tmp/migration-response.json
  success "Migration Lambda invoked"
fi

echo ""
success "Migrations complete"
