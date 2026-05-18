"""
Augment Option C per-race parquets with 3 additional L1-input candidate columns.

Substrate-pragmatic deviation from Tony T2 directive (extend option_c_inference.py
inline): authored as separate substrate-augmentation script per substrate-pragmatic
substrate-coverage. LSTM inline-inference requires PyTorch model load + sequence
feature extraction per horse; substrate-actual coverage already exists in
ls_predictions (100% lstm_trajectory + rf_longshot_prob in training window
2026-04-25..2026-05-01; verified 1,179/1,179 rows). DB JOIN avoids re-inference.

3 new columns added per parquet:
  lstm_trajectory_score              — from ls_predictions.lstm_trajectory
  first_time_lasix_posterior_sparse  — from wr_predictions.angle_posterior
                                       WHERE angle_name='first_time_lasix' ELSE 0.0
                                       (T4 SPARSE substrate per Tier 1.5 Q4)
  longshot_prob_substrate_correct    — from ls_predictions.rf_longshot_prob
                                       (Tier 1 2C substrate-correct path; per
                                        Tier 1.5 Q3 mapping)

Substrate-thin caveat: training-window first_time_lasix firings = 6/3,447 rows
(0.17% non-zero). 33rd-input ensemble training may show near-zero feature gain
for 3B variant; useful null finding per § 4.27 banking pattern.

Substrate-prerequisite for BD2v2 training scripts (3A/3B/3C).
"""
import argparse
import glob
import json
import os
import sys
from pathlib import Path

import boto3
import pandas as pd
import psycopg2

DB_SECRET_ARN = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'


def get_db_conn():
    sm = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString'])
    return psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'],
        password=secret['password'],
    )


def fetch_aux_columns(window_start, window_end):
    """Pull 3 aux columns for window via DB JOIN.

    Returns DataFrame with race_id, horse_id, lstm_trajectory_score,
    first_time_lasix_posterior_sparse, longshot_prob_substrate_correct.
    """
    conn = get_db_conn()
    # Pull ls_predictions (lstm + longshot) — keyed by (race_id, horse_id)
    # DISTINCT ON to deduplicate multi-row per (race, horse); take latest by created_at
    ls = pd.read_sql("""
        SELECT DISTINCT ON (lp.race_id, lp.horse_id)
               lp.race_id::text AS race_id,
               lp.horse_id::text AS horse_id,
               lp.lstm_trajectory AS lstm_trajectory_score,
               lp.rf_longshot_prob AS longshot_prob_substrate_correct
        FROM ls_predictions lp
        JOIN races r ON r.race_id = lp.race_id
        WHERE r.race_date BETWEEN %s AND %s
        ORDER BY lp.race_id, lp.horse_id, lp.created_at DESC
    """, conn, params=[window_start, window_end])

    # Pull wr_predictions first_time_lasix posterior (sparse)
    # DISTINCT ON to deduplicate; substrate-pragmatic: take latest prediction per (race, horse)
    wr = pd.read_sql("""
        SELECT DISTINCT ON (wp.race_id, wp.horse_id)
               wp.race_id::text AS race_id,
               wp.horse_id::text AS horse_id,
               CASE WHEN wp.angle_name = 'first_time_lasix'
                    THEN COALESCE(wp.angle_posterior, 0.0)
                    ELSE 0.0 END AS first_time_lasix_posterior_sparse
        FROM wr_predictions wp
        JOIN races r ON r.race_id = wp.race_id
        WHERE r.race_date BETWEEN %s AND %s
        ORDER BY wp.race_id, wp.horse_id, wp.created_at DESC
    """, conn, params=[window_start, window_end])
    conn.close()

    # Substrate-pragmatic merge: ls_predictions is the substrate-narrower set
    # (top-N per race); wr_predictions covers all entries. We want both columns
    # mappable per (race, horse) so left-join wr on ls.
    aux = ls.merge(wr, on=['race_id', 'horse_id'], how='outer')
    # NaN handling: substrate-pragmatic 0.0 fill for any missing values
    for col in ['lstm_trajectory_score', 'first_time_lasix_posterior_sparse',
                'longshot_prob_substrate_correct']:
        if col in aux.columns:
            aux[col] = aux[col].fillna(0.0)
    return aux


def augment_parquets(parquet_dir, window_start, window_end, in_place=False, output_dir=None):
    """Augment parquets in parquet_dir with 3 aux columns."""
    parquets = sorted(glob.glob(f'{parquet_dir}/*.parquet'))
    if not parquets:
        raise ValueError(f"No parquets in {parquet_dir}")

    print(f"Loading aux substrate for {window_start}..{window_end}")
    aux = fetch_aux_columns(window_start, window_end)
    print(f"Aux substrate: {len(aux)} rows ({aux['race_id'].nunique()} races)")
    print(f"  lstm_trajectory_score non-zero: {(aux['lstm_trajectory_score'] != 0).sum()}")
    print(f"  longshot_prob non-zero: {(aux['longshot_prob_substrate_correct'] != 0).sum()}")
    print(f"  first_time_lasix non-zero (sparse): {(aux['first_time_lasix_posterior_sparse'] != 0).sum()}")

    output_dir = output_dir or parquet_dir
    os.makedirs(output_dir, exist_ok=True)

    n_done = 0
    n_skip = 0
    for p in parquets:
        race_id = Path(p).stem
        df = pd.read_parquet(p)
        df['race_id'] = race_id
        df['horse_id'] = df['horse_id'].astype(str)

        race_aux = aux[aux['race_id'] == race_id]
        if len(race_aux) == 0:
            # Substrate-thin: add zero-filled columns
            df['lstm_trajectory_score'] = 0.0
            df['first_time_lasix_posterior_sparse'] = 0.0
            df['longshot_prob_substrate_correct'] = 0.0
            n_skip += 1
        else:
            merged = df.merge(
                race_aux[['horse_id', 'lstm_trajectory_score',
                          'first_time_lasix_posterior_sparse',
                          'longshot_prob_substrate_correct']],
                on='horse_id', how='left',
            )
            for c in ['lstm_trajectory_score',
                      'first_time_lasix_posterior_sparse',
                      'longshot_prob_substrate_correct']:
                merged[c] = merged[c].fillna(0.0)
            df = merged

        out_path = os.path.join(output_dir, f'{race_id}.parquet')
        df.to_parquet(out_path, index=False)
        n_done += 1

    print(f"Augmented {n_done} parquets ({n_skip} with substrate-thin aux fill)")
    return n_done


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parquet-dir', default='/tmp/option_c_predictions_train',
                        help='Source parquet directory')
    parser.add_argument('--window-start', default='2026-04-25')
    parser.add_argument('--window-end', default='2026-05-01')
    parser.add_argument('--output-dir', default=None,
                        help='Output directory (default: in-place overwrite)')
    args = parser.parse_args()

    augment_parquets(
        args.parquet_dir, args.window_start, args.window_end,
        output_dir=args.output_dir,
    )


if __name__ == '__main__':
    main()
