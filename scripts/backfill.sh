#!/bin/bash
set -e

# ─────────────────────────────────────────
# Equine Equalizer — Historical Data Backfill
# ─────────────────────────────────────────
# Loads Equibase 2023 dataset into database.
#
# Usage:
#   ./scripts/backfill.sh --data-dir /path/to/equibase/data
#   ./scripts/backfill.sh --data-dir ~/Downloads/equibase-2023
#
# Run this AFTER:
#   1. deploy-backend.sh (infrastructure exists)
#   2. run-migrations.sh (schema created)
#   3. Equibase 2023 data downloaded

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
DATA_DIR=""
while [ $# -gt 0 ]; do
  case $1 in
    --data-dir)
      DATA_DIR="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

if [ -z "$DATA_DIR" ]; then
  error "No data directory specified.
Usage: ./scripts/backfill.sh --data-dir /path/to/data"
fi

if [ ! -d "$DATA_DIR" ]; then
  error "Data directory not found: $DATA_DIR"
fi

step "Equibase Historical Data Backfill"
log "Data directory: $DATA_DIR"

FILE_COUNT=$(find "$DATA_DIR" \
  -type f \( -name "*.csv" -o \
             -name "*.txt" -o \
             -name "*.cha" \) \
  | wc -l | tr -d ' ')

log "Files found: $FILE_COUNT"

if [ "$FILE_COUNT" -eq 0 ]; then
  error "No data files found in $DATA_DIR
Expected .csv, .txt, or .cha files"
fi

# Confirm before running
echo ""
warn "This will load $FILE_COUNT files into"
warn "the Equine Equalizer database."
echo -e "${WHITE}Continue? (y/N)${NC} \c"
read -r CONFIRM

if [ "$CONFIRM" != "y" ] && \
   [ "$CONFIRM" != "Y" ]; then
  log "Aborted."
  exit 0
fi

step "Running backfill"

cd "$PROJECT_ROOT/backend"

python3 - <<EOF
import sys
sys.path.insert(0, '.')
import os
import glob
from datetime import date
from shared.db import get_db
from services.ingestion_service import (
    IngestionService
)

data_dir = "$DATA_DIR"
files = sorted(
    glob.glob(f"{data_dir}/**/*.csv",
        recursive=True) +
    glob.glob(f"{data_dir}/**/*.txt",
        recursive=True) +
    glob.glob(f"{data_dir}/**/*.cha",
        recursive=True)
)

print(f"Processing {len(files)} files...")

with get_db() as conn:
    service = IngestionService(conn)
    summary = service.backfill_historical_data(
        files
    )

print("")
print("=" * 50)
print("  BACKFILL COMPLETE")
print("=" * 50)
print(f"  Files processed: {summary['files_processed']}")
print(f"  Files failed:    {summary['files_failed']}")
print(f"  Races stored:    {summary['races_stored']}")
print(f"  Races skipped:   {summary['races_skipped']}")
print(f"  Unique horses:   {summary['horses_seen']}")
print(f"  PP records:      {summary['pp_records_stored']}")
if summary['errors']:
    print(f"  Errors:          {len(summary['errors'])}")
    for err in summary['errors'][:5]:
        print(f"    - {err}")
print("=" * 50)
print("")
print("Next step: python model/training/train.py")
EOF
