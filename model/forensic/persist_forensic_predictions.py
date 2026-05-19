"""
Persist BD3v2 forensic-window predictions to hybrid_c_predictions schema per T-A3.

Schema-coherent insert: race_id (UUID) + horse_id (TEXT) + ensemble_version (varchar)
                       + hybrid_c_win_probability (numeric) + predicted_at (timestamp)
                       + l1_input_count (integer).
UNIQUE constraint on (race_id, horse_id, ensemble_version): ON CONFLICT DO NOTHING
(UNFUCK-1 Step B; substrate-protect against re-write contamination per
AS-OF leakage finding — re-runs should use new ensemble_version tag).
"""

import argparse
import json
from pathlib import Path

import boto3
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


DB_SECRET_ARN = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'


def get_db_conn():
    sm = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString'])
    return psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'], password=secret['password'],
    )


def persist(parquet_path, l1_input_count=None):
    df = pd.read_parquet(parquet_path)
    print(f"Persisting {len(df)} predictions from {Path(parquet_path).name}")

    df['horse_id'] = df['horse_id'].astype(str)
    df['l1_input_count'] = l1_input_count if l1_input_count is not None else 0

    rows = [
        (r['race_id'], r['horse_id'], r['ensemble_version'],
         float(r['win_probability']), r['predicted_at'], int(r['l1_input_count']))
        for _, r in df.iterrows()
    ]

    conn = get_db_conn()
    cur = conn.cursor()
    execute_values(cur, """
        INSERT INTO hybrid_c_predictions
            (race_id, horse_id, ensemble_version, hybrid_c_win_probability,
             predicted_at, l1_input_count)
        VALUES %s
        ON CONFLICT (race_id, horse_id, ensemble_version) DO NOTHING
    """, rows)
    conn.commit()

    ensemble_version = df['ensemble_version'].iloc[0]
    cur.execute("""
        SELECT COUNT(*) FROM hybrid_c_predictions
        WHERE ensemble_version = %s
    """, [ensemble_version])
    persisted_count = cur.fetchone()[0]
    conn.close()

    print(f"  Persisted ensemble_version={ensemble_version}: {persisted_count} rows in DB")
    return persisted_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parquet', required=True)
    parser.add_argument('--l1-input-count', type=int, default=None)
    args = parser.parse_args()
    persist(args.parquet, args.l1_input_count)


if __name__ == '__main__':
    main()
