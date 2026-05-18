#!/usr/bin/env python3
"""Phase 4 — Re-run inference for ensemble TRAINING window (2026-04-25..2026-05-01).

Substrate-pragmatic window: 7 days held out from BOTH Phase B.x and PRIOR cohorts:
  - Phase B.x P2 val mask: 2026-04-25..2026-05-01
  - PRIOR cohort training_date 2026-04-29 implies training data extends ~2026-04-15
  - Both OOS for this window

Outputs per-race parquets at /tmp/option_c_predictions_train/{race_id}.parquet
Same artifact load + feature_path classification as Phase 1.
"""
from __future__ import annotations
import os, sys
os.environ['DB_SECRET_ARN'] = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'
os.environ.pop('DATABASE_URL', None)

sys.path.insert(0, '/home/strakajagr/projects/equine-equalizer')
sys.path.insert(0, '/home/strakajagr/projects/equine-equalizer/backend')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Reuse Phase 1 infrastructure by importing the script module
import option_c_inference as oci
from datetime import date

# Override paths + window
oci.FORENSIC_START = date(2026, 4, 25)
oci.FORENSIC_END = date(2026, 5, 1)
oci.OUTPUT_DIR = '/tmp/option_c_predictions_train'
os.makedirs(oci.OUTPUT_DIR, exist_ok=True)

# Run Phase 1's main loop with the modified window/output
if __name__ == '__main__':
    oci.main()
