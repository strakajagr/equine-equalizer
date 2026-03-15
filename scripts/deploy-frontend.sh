#!/bin/bash
set -e

# ─────────────────────────────────────────
# Equine Equalizer — Frontend Deploy Script
# ─────────────────────────────────────────
# Builds React app and deploys to S3 +
# invalidates CloudFront cache.
#
# Usage:
#   ./scripts/deploy-frontend.sh
#
# Requirements:
#   - Run deploy-backend.sh first
#     (creates .frontend-bucket and
#      frontend/.env.production)
#   - AWS CLI configured
#   - Node.js installed

# ─────────────────────────────────────────
# Color helpers
# ─────────────────────────────────────────
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

# ─────────────────────────────────────────
# Paths
# ─────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
BUILD_DIR="$FRONTEND_DIR/build"

# ─────────────────────────────────────────
# Verify prerequisites
# ─────────────────────────────────────────
step "Checking prerequisites"

command -v aws >/dev/null 2>&1 \
  || error "AWS CLI not found."

command -v node >/dev/null 2>&1 \
  || error "Node.js not found."

command -v npm >/dev/null 2>&1 \
  || error "npm not found."

aws sts get-caller-identity \
  --query 'Account' \
  --output text > /dev/null 2>&1 \
  || error "AWS credentials not configured."

success "Prerequisites verified"

# ─────────────────────────────────────────
# Get S3 bucket name
# ─────────────────────────────────────────
step "Getting deployment target"

BUCKET_FILE="$PROJECT_ROOT/.frontend-bucket"

if [ -f "$BUCKET_FILE" ]; then
  S3_BUCKET=$(cat "$BUCKET_FILE")
  success "S3 bucket: $S3_BUCKET"
else
  # Try to get from CDK outputs
  if [ -f "$PROJECT_ROOT/cdk-outputs.json" ]; then
    S3_BUCKET=$(python3 -c "
import json, sys
with open('$PROJECT_ROOT/cdk-outputs.json') as f:
  outputs = json.load(f)
for stack in outputs.values():
  for key, val in stack.items():
    if 'Frontend' in key and 'Bucket' in key:
      print(val)
      sys.exit(0)
" 2>/dev/null || echo "")
  fi

  if [ -z "$S3_BUCKET" ]; then
    error "Cannot find frontend S3 bucket.
Run deploy-backend.sh first, or set
S3_BUCKET environment variable manually:
  S3_BUCKET=your-bucket-name ./scripts/deploy-frontend.sh"
  fi
fi

# Get CloudFront distribution ID for cache invalidation
CF_DIST_ID=$(python3 -c "
import json, sys
try:
  with open('$PROJECT_ROOT/cdk-outputs.json') as f:
    outputs = json.load(f)
  for stack in outputs.values():
    for key, val in stack.items():
      if 'DistributionId' in key:
        print(val)
        sys.exit(0)
except:
  pass
" 2>/dev/null || echo "")

if [ -n "$CF_DIST_ID" ]; then
  success "CloudFront distribution: $CF_DIST_ID"
else
  warn "CloudFront distribution ID not found"
  warn "Cache invalidation will be skipped"
fi

# ─────────────────────────────────────────
# Verify API URL is set
# ─────────────────────────────────────────
step "Verifying environment config"

ENV_FILE="$FRONTEND_DIR/.env.production"

if [ ! -f "$ENV_FILE" ]; then
  warn ".env.production not found"
  warn "Creating from cdk-outputs.json..."

  API_URL=$(python3 -c "
import json, sys
try:
  with open('$PROJECT_ROOT/cdk-outputs.json') as f:
    outputs = json.load(f)
  for stack in outputs.values():
    for key, val in stack.items():
      if 'ApiUrl' in key or 'HttpApi' in key:
        print(val)
        sys.exit(0)
except:
  pass
" 2>/dev/null || echo "")

  if [ -z "$API_URL" ]; then
    error "Cannot find API URL.
Set it manually in frontend/.env.production:
  REACT_APP_API_URL=https://your-api-id.execute-api.us-east-1.amazonaws.com"
  fi

  echo "REACT_APP_API_URL=$API_URL" > "$ENV_FILE"
  success "Created .env.production with API URL: $API_URL"
else
  API_URL=$(grep REACT_APP_API_URL "$ENV_FILE" \
    | cut -d '=' -f2)
  success "API URL: $API_URL"
fi

# ─────────────────────────────────────────
# Install dependencies
# ─────────────────────────────────────────
step "Installing frontend dependencies"

cd "$FRONTEND_DIR"
npm install --silent \
  || error "npm install failed"
success "Dependencies installed"

# ─────────────────────────────────────────
# Run build
# ─────────────────────────────────────────
step "Building React application"

cd "$FRONTEND_DIR"

# Use production env file
REACT_APP_API_URL="$API_URL" \
npm run build \
  || error "React build failed"

success "React build complete"

# Show build size
BUILD_SIZE=$(du -sh "$BUILD_DIR" \
  | cut -f1)
log "Build size: $BUILD_SIZE"

# ─────────────────────────────────────────
# Upload to S3
# ─────────────────────────────────────────
step "Uploading to S3"

# Upload HTML files with no-cache
# (always fetch latest HTML)
aws s3 sync "$BUILD_DIR" \
  "s3://$S3_BUCKET" \
  --exclude "*" \
  --include "*.html" \
  --cache-control "no-cache, no-store, must-revalidate" \
  --delete \
  --quiet
success "HTML files uploaded (no-cache)"

# Upload JS/CSS with long cache
# (hashed filenames change on each build)
aws s3 sync "$BUILD_DIR" \
  "s3://$S3_BUCKET" \
  --exclude "*.html" \
  --cache-control "public, max-age=31536000, immutable" \
  --delete \
  --quiet
success "Static assets uploaded (1yr cache)"

# ─────────────────────────────────────────
# Invalidate CloudFront cache
# ─────────────────────────────────────────
step "Invalidating CloudFront cache"

if [ -n "$CF_DIST_ID" ]; then
  INVALIDATION_ID=$(aws cloudfront \
    create-invalidation \
    --distribution-id "$CF_DIST_ID" \
    --paths "/*" \
    --query 'Invalidation.Id' \
    --output text)
  success "Cache invalidation started: $INVALIDATION_ID"
  log "Changes live in ~60 seconds"
else
  warn "Skipping CloudFront invalidation"
  warn "Clear browser cache manually to see changes"
fi

# ─────────────────────────────────────────
# Get CloudFront URL
# ─────────────────────────────────────────
CF_URL=$(python3 -c "
import json, sys
try:
  with open('$PROJECT_ROOT/cdk-outputs.json') as f:
    outputs = json.load(f)
  for stack in outputs.values():
    for key, val in stack.items():
      if 'CloudFront' in key or 'Distribution' in key:
        if val.endswith('.net'):
          print(val)
          sys.exit(0)
except:
  pass
" 2>/dev/null || echo "")

# ─────────────────────────────────────────
# Done
# ─────────────────────────────────────────
echo ""
echo -e "${GOLD}════════════════════════════════════════${NC}"
echo -e "${GOLD}  FRONTEND DEPLOY COMPLETE${NC}"
echo -e "${GOLD}════════════════════════════════════════${NC}"

if [ -n "$CF_URL" ]; then
  echo -e "${WHITE}  App URL:${NC}"
  echo -e "${GREEN}  https://$CF_URL${NC}"
fi

echo -e "${WHITE}  S3 Bucket:${NC}"
echo -e "${GREEN}  s3://$S3_BUCKET${NC}"
echo -e "${GOLD}════════════════════════════════════════${NC}"
echo ""
