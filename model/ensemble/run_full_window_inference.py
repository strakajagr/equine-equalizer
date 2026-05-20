#!/usr/bin/env python3
"""REPAIR-5-INTERLEAVED-β.1 — Full-window inference against substrate-clean L1.

Substrate-bug-fix: predecessor run_window_inference.py used a 7-day window
(2026-04-25..2026-05-01) substrate-incoherent for ensemble that historically
trained on multi-year corpus. This script runs FULL substrate-clean window
2022-01-01 → 2026-05-17 (latest race date in DB).

Outputs per-race parquets at /tmp/option_c_predictions_full/{race_id}.parquet
"""
from __future__ import annotations
import os, sys
os.environ['DB_SECRET_ARN'] = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'
os.environ.pop('DATABASE_URL', None)

sys.path.insert(0, '/home/strakajagr/projects/equine-equalizer')
sys.path.insert(0, '/home/strakajagr/projects/equine-equalizer/backend')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import option_c_inference as oci
from datetime import date

# REPAIR-5-INTERLEAVED-β.1 full substrate-window
oci.FORENSIC_START = date(2022, 1, 1)
oci.FORENSIC_END = date(2026, 5, 17)
oci.OUTPUT_DIR = '/tmp/option_c_predictions_full'
os.makedirs(oci.OUTPUT_DIR, exist_ok=True)

if __name__ == '__main__':
    oci.main()
