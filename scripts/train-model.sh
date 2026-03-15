#!/bin/bash
set -e

# ─────────────────────────────────────────
# Equine Equalizer — Model Training Script
# ─────────────────────────────────────────
# Trains XGBoost model on historical data.
#
# Usage:
#   ./scripts/train-model.sh
#   ./scripts/train-model.sh --activate
#   ./scripts/train-model.sh --version v1.1
#
# Run AFTER backfill.sh loads data.

RED='\033[0;31m'
GREEN='\033[0;32m'
GOLD='\033[0;33m'
WHITE='\033[1;37m'
NC='\033[0m'

log()     { echo -e "${WHITE}$1${NC}"; }
success() { echo -e "${GREEN}✓ $1${NC}"; }
warn()    { echo -e "${GOLD}⚠ $1${NC}"; }
error()   { echo -e "${RED}✗ $1${NC}"; exit 1; }
step()    { echo -e "\n${GOLD}▶ $1${NC}"; }

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Parse args
ACTIVATE=false
VERSION=""
while [ $# -gt 0 ]; do
  case $1 in
    --activate) ACTIVATE=true; shift ;;
    --version)  VERSION="$2"; shift 2 ;;
    *)          shift ;;
  esac
done

# Get S3 bucket from CDK outputs
S3_BUCKET=$(python3 -c "
import json, sys
try:
  with open('$PROJECT_ROOT/cdk-outputs.json') as f:
    outputs = json.load(f)
  for stack in outputs.values():
    for key, val in stack.items():
      if 'ModelArtifacts' in key or \
         ('model' in key.lower() and \
          'bucket' in key.lower()):
        print(val)
        sys.exit(0)
except:
  pass
" 2>/dev/null || echo "")

step "Equine Equalizer Model Training"
log "S3 bucket: ${S3_BUCKET:-not found}"

cd "$PROJECT_ROOT/backend"

TRAIN_ARGS="--start-date 2023-01-01 --end-date 2023-12-31"

if [ -n "$S3_BUCKET" ]; then
  TRAIN_ARGS="$TRAIN_ARGS --s3-bucket $S3_BUCKET"
fi

if [ -n "$VERSION" ]; then
  TRAIN_ARGS="$TRAIN_ARGS --version-name $VERSION"
fi

if [ "$ACTIVATE" = true ]; then
  TRAIN_ARGS="$TRAIN_ARGS --set-active"
  warn "Model will be set ACTIVE after training"
  warn "This affects live predictions immediately"
  echo -e "${WHITE}Continue? (y/N)${NC} \c"
  read -r CONFIRM
  if [ "$CONFIRM" != "y" ] && \
     [ "$CONFIRM" != "Y" ]; then
    log "Aborted. Run without --activate to"
    log "review metrics before activating."
    exit 0
  fi
fi

step "Starting training pipeline"
log "This will take several minutes..."
echo ""

python3 ../model/training/train.py \
  $TRAIN_ARGS \
  || error "Training failed"

echo ""
success "Training complete"

if [ "$ACTIVATE" = false ]; then
  echo ""
  warn "Model not yet active."
  log "Review metrics above, then activate:"
  log "  ./scripts/train-model.sh --activate \\"
  log "    --version <version-name>"
fi
