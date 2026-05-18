"""
4G Imitation learning STUB per T-B2.

Substrate-availability check at runtime: if sharp-bettor / handicapper-bet
substrate absent in DB, halt-and-document with substrate-absent finding.
Scaffolding preserved for future Tony substrate-acquisition adjudication.

Per Tier 1.5 Q10 + BD3 Phase 1 substrate-discovery: NO bet/wager/handicapper
tables exist in current substrate. 4G implementation deferred.
"""

import argparse
import json

import boto3
import psycopg2


DB_SECRET_ARN = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'


def get_db_conn():
    sm_client = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm_client.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString'])
    return psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'], password=secret['password'],
    )


def substrate_availability_check():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema='public'
          AND (table_name ILIKE '%bet%' OR table_name ILIKE '%wager%'
               OR table_name ILIKE '%handicapper%' OR table_name ILIKE '%bettor%')
    """)
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return False, []
    return True, [r[0] for r in rows]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    available, tables = substrate_availability_check()
    if not available:
        result = {
            'verdict': 'substrate-absent (4G build-blocked per T-B2)',
            'message': 'No bet/wager/handicapper/bettor tables in DB. '
                       'Scaffolding preserved for future Tony substrate-acquisition adjudication.',
            'tables_found': [],
        }
    else:
        result = {
            'verdict': 'substrate-acquired (4G implementation TBD per future Tony adjudication)',
            'tables_found': tables,
        }
    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"4G verdict: {result['verdict']}")
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
