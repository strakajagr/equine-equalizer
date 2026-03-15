#!/bin/bash
set -e  # exit on any error

# ─────────────────────────────────────────
# Equine Equalizer — Backend Deploy Script
# ─────────────────────────────────────────
# Deploys CDK infrastructure and Lambda code
# to AWS.
#
# Usage:
#   ./scripts/deploy-backend.sh
#   ./scripts/deploy-backend.sh --bootstrap
#   ./scripts/deploy-backend.sh --stack StorageStack
#
# Requirements:
#   - AWS CLI configured (aws configure)
#   - Node.js installed
#   - Python 3.11 installed
#   - CDK installed: npm install -g aws-cdk

# ─────────────────────────────────────────
# Color output helpers
# ─────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
GOLD='\033[0;33m'
WHITE='\033[1;37m'
DIM='\033[0;37m'
NC='\033[0m' # no color

log()     { echo -e "${WHITE}$1${NC}"; }
success() { echo -e "${GREEN}✓ $1${NC}"; }
warn()    { echo -e "${GOLD}⚠ $1${NC}"; }
error()   { echo -e "${RED}✗ $1${NC}"; exit 1; }
step()    { echo -e "\n${GOLD}▶ $1${NC}"; }

# ─────────────────────────────────────────
# Parse arguments
# ─────────────────────────────────────────
BOOTSTRAP=false
STACK=""

for arg in "$@"; do
  case $arg in
    --bootstrap)
      BOOTSTRAP=true
      ;;
    --stack)
      STACK="$2"
      shift
      ;;
  esac
  shift 2>/dev/null || true
done

# ─────────────────────────────────────────
# Verify prerequisites
# ─────────────────────────────────────────
step "Checking prerequisites"

command -v aws >/dev/null 2>&1 \
  || error "AWS CLI not found. Install: brew install awscli"

command -v node >/dev/null 2>&1 \
  || error "Node.js not found."

command -v cdk >/dev/null 2>&1 \
  || error "CDK not found. Run: npm install -g aws-cdk"

command -v python3 >/dev/null 2>&1 \
  || error "Python3 not found."

# Verify AWS credentials
aws sts get-caller-identity \
  --query 'Account' \
  --output text > /dev/null 2>&1 \
  || error "AWS credentials not configured. Run: aws configure"

AWS_ACCOUNT=$(aws sts get-caller-identity \
  --query 'Account' --output text)
AWS_REGION=$(aws configure get region \
  || echo "us-east-1")

success "AWS Account: $AWS_ACCOUNT"
success "AWS Region:  $AWS_REGION"

# ─────────────────────────────────────────
# Project root
# ─────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CDK_DIR="$PROJECT_ROOT/infrastructure/cdk"
BACKEND_DIR="$PROJECT_ROOT/backend"

log "Project root: $PROJECT_ROOT"

# ─────────────────────────────────────────
# Install CDK dependencies
# ─────────────────────────────────────────
step "Installing CDK dependencies"

cd "$CDK_DIR"
npm install --silent
success "CDK dependencies installed"

# ─────────────────────────────────────────
# Build CDK TypeScript
# ─────────────────────────────────────────
step "Building CDK TypeScript"

npm run build \
  || error "CDK TypeScript build failed"
success "CDK TypeScript compiled"

# ─────────────────────────────────────────
# Bootstrap (first time only)
# ─────────────────────────────────────────
if [ "$BOOTSTRAP" = true ]; then
  step "Bootstrapping CDK (first time setup)"
  cdk bootstrap \
    "aws://$AWS_ACCOUNT/$AWS_REGION" \
    || error "CDK bootstrap failed"
  success "CDK bootstrapped"
fi

# ─────────────────────────────────────────
# Package Lambda dependencies
# ─────────────────────────────────────────
step "Packaging Lambda layers"

LAYER_DIR="$BACKEND_DIR/layers/ml-dependencies"
LAYER_BUILD="$LAYER_DIR/python"

mkdir -p "$LAYER_BUILD"

pip3 install \
  -r "$LAYER_DIR/requirements.txt" \
  -t "$LAYER_BUILD" \
  --quiet \
  || error "Lambda layer packaging failed"

success "Lambda dependencies packaged"

# ─────────────────────────────────────────
# Run CDK synth (validate before deploy)
# ─────────────────────────────────────────
step "Synthesizing CloudFormation templates"

cd "$CDK_DIR"
cdk synth --quiet \
  || error "CDK synth failed — check stack code"
success "CloudFormation templates valid"

# ─────────────────────────────────────────
# Deploy
# ─────────────────────────────────────────
step "Deploying to AWS"

cd "$CDK_DIR"

if [ -n "$STACK" ]; then
  log "Deploying single stack: $STACK"
  cdk deploy "$STACK" \
    --require-approval never \
    --outputs-file "$PROJECT_ROOT/cdk-outputs.json" \
    || error "Stack deploy failed: $STACK"
else
  log "Deploying all stacks..."
  log "Order: StorageStack → DatabaseStack → ComputeStack → FrontendStack"
  cdk deploy --all \
    --require-approval never \
    --outputs-file "$PROJECT_ROOT/cdk-outputs.json" \
    || error "Full deploy failed"
fi

# ─────────────────────────────────────────
# Extract and display outputs
# ─────────────────────────────────────────
step "Deployment outputs"

if [ -f "$PROJECT_ROOT/cdk-outputs.json" ]; then
  # Extract API Gateway URL
  API_URL=$(python3 -c "
import json, sys
with open('$PROJECT_ROOT/cdk-outputs.json') as f:
  outputs = json.load(f)
for stack in outputs.values():
  for key, val in stack.items():
    if 'ApiUrl' in key or 'HttpApi' in key:
      print(val)
      sys.exit(0)
" 2>/dev/null || echo "")

  # Extract CloudFront URL
  CF_URL=$(python3 -c "
import json, sys
with open('$PROJECT_ROOT/cdk-outputs.json') as f:
  outputs = json.load(f)
for stack in outputs.values():
  for key, val in stack.items():
    if 'CloudFront' in key or 'Distribution' in key:
      print(val)
      sys.exit(0)
" 2>/dev/null || echo "")

  # Extract S3 frontend bucket
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

  echo ""
  echo -e "${GOLD}════════════════════════════════════════${NC}"
  echo -e "${GOLD}  DEPLOYMENT COMPLETE${NC}"
  echo -e "${GOLD}════════════════════════════════════════${NC}"

  if [ -n "$API_URL" ]; then
    echo -e "${WHITE}  API Gateway URL:${NC}"
    echo -e "${GREEN}  $API_URL${NC}"
    echo ""
    # Write to .env for frontend deploy script
    echo "REACT_APP_API_URL=$API_URL" \
      > "$PROJECT_ROOT/frontend/.env.production"
    success "API URL written to frontend/.env.production"
  fi

  if [ -n "$CF_URL" ]; then
    echo -e "${WHITE}  CloudFront URL:${NC}"
    echo -e "${GREEN}  https://$CF_URL${NC}"
  fi

  if [ -n "$S3_BUCKET" ]; then
    echo -e "${WHITE}  Frontend S3 Bucket:${NC}"
    echo -e "${GREEN}  $S3_BUCKET${NC}"
    # Save for frontend deploy script
    echo "$S3_BUCKET" \
      > "$PROJECT_ROOT/.frontend-bucket"
  fi

  # Save CloudFront distribution ID
  CF_ID=$(python3 -c "
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

  if [ -n "$CF_ID" ]; then
    echo "$CF_ID" > "$PROJECT_ROOT/.cf-distribution-id"
    success "CloudFront ID saved to .cf-distribution-id"
  fi

  echo -e "${GOLD}════════════════════════════════════════${NC}"
  echo ""
  echo -e "${DIM}Next step: run ./scripts/deploy-frontend.sh${NC}"
  echo ""
else
  warn "No outputs file found — check AWS console"
fi

# ─────────────────────────────────────────
# Run database migrations
# ─────────────────────────────────────────
step "Running database migrations"

warn "Database migrations must be run manually."
warn "The database is in a private VPC subnet"
warn "and cannot be reached from this machine"
warn "without a bastion host or VPN."
echo ""
log "To run migrations:"
log "  1. Use AWS Systems Manager Session Manager"
log "     to connect to a Lambda function"
log "  2. Or temporarily enable RDS public access"
log "     (dev only — never production)"
log "  3. Or use AWS Cloud9 inside the VPC"
echo ""

success "Backend deploy complete"
