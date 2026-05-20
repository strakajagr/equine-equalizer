#!/usr/bin/env python3
"""Date-chunk inference for parallel full-window REPAIR-5-INTERLEAVED-β.1.

Usage: run_chunk_inference.py YYYY-MM-DD YYYY-MM-DD
Output goes to /tmp/option_c_predictions_full/{race_id}.parquet (shared).
Existing parquets substrate-skipped per option_c_inference.py default.
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

start = date.fromisoformat(sys.argv[1])
end = date.fromisoformat(sys.argv[2])

oci.FORENSIC_START = start
oci.FORENSIC_END = end
oci.OUTPUT_DIR = '/tmp/option_c_predictions_full'
os.makedirs(oci.OUTPUT_DIR, exist_ok=True)

if __name__ == '__main__':
    oci.main()
