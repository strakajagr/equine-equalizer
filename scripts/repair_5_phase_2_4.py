#!/usr/bin/env python3
"""REPAIR-5-RESCUE Phase 2-4: continuation of wave-2 post-Phase-1 rename.

Substrate-state at start:
  Wave-2 Phase 1 already complete: 37 rows substrate-clean + renamed via
  derive_model_type + tagged clean_post_repair5_20260519. Phase 2-4 pending.

Substrate-discipline: applies derive_model_type rename + clean-tag append
post-completion of each phase, so verify substrate-actually substrate-matches
canonical model_type names.

Usage: python3 scripts/repair_5_phase_2_4.py
"""
import sys, os, json, time, logging
from datetime import datetime
from pathlib import Path

import boto3

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

REGION = 'us-east-1'
CLUSTER = 'equine-cluster'
TASK_DEF = 'equine-training'
SUBNETS = ['subnet-2f771b21', 'subnet-ac96278d', 'subnet-7951fa1f']
SECURITY_GROUPS = ['sg-9b256ea5']
CLEAN_TAG = 'clean_post_repair5_20260519'

PHASE_PLAN = [
    {'phase': 2, 'description': 'Hybrid C ensemble', 'tasks': [
        {'cmd': ['model/ensemble/train_hybrid_c.py'], 'expects': ['ensemble_hybrid_option_c']},
    ]},
    {'phase': 3, 'description': 'L2 + LSTM + Longshot + WR', 'tasks': [
        {'cmd': ['model/ensemble/train.py'], 'expects': ['ensemble']},
        {'cmd': ['model/trajectory/train.py'], 'expects': ['trajectory_lstm']},
        {'cmd': ['model/longshot/train.py'], 'expects': ['longshot_rf']},
        {'cmd': ['model/wr/train.py'], 'expects': ['wr_base', 'wr_odds']},
    ]},
    {'phase': 4, 'description': 'Singletons', 'tasks': [
        {'cmd': ['model/ranker/train.py'], 'expects': ['ranker_core', 'ranker_full']},
        {'cmd': ['model/win_prob/train.py'], 'expects': ['win_prob_full']},
    ]},
]


def launch_task(cmd):
    ecs = boto3.client('ecs', region_name=REGION)
    resp = ecs.run_task(
        cluster=CLUSTER, taskDefinition=TASK_DEF, launchType='FARGATE', count=1,
        networkConfiguration={'awsvpcConfiguration': {
            'subnets': SUBNETS, 'securityGroups': SECURITY_GROUPS, 'assignPublicIp': 'ENABLED'}},
        overrides={'containerOverrides': [{
            'name': 'training', 'command': cmd,
            'environment': [{'name': 'LEAN_TAG', 'value': 'lean58'}],
        }]},
    )
    if resp.get('failures'):
        raise RuntimeError(f"run_task failed for {cmd}: {resp['failures']}")
    return resp['tasks'][0]['taskArn']


def wait_for_tasks(arns):
    ecs = boto3.client('ecs', region_name=REGION)
    pending = set(arns)
    results = {}
    while pending:
        resp = ecs.describe_tasks(cluster=CLUSTER, tasks=list(pending))
        for t in resp['tasks']:
            if t['lastStatus'] == 'STOPPED':
                ec = None
                for c in t.get('containers', []):
                    if c['name'] == 'training':
                        ec = c.get('exitCode'); break
                results[t['taskArn']] = ec
                pending.discard(t['taskArn'])
                logger.info(f"  STOPPED arn={t['taskArn'][-12:]} exit={ec}")
        if pending: time.sleep(60)
    return results


def get_conn():
    import psycopg2, psycopg2.extras
    sm = boto3.client('secretsmanager', region_name=REGION)
    s = json.loads(sm.get_secret_value(
        SecretId='arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'
    )['SecretString'])
    return psycopg2.connect(host=s['host'], port=s['port'], dbname=s['dbname'],
                            user=s['username'], password=s['password'],
                            cursor_factory=psycopg2.extras.RealDictCursor)


def apply_derive_and_tag(since_ts):
    """Rename model_type via derive_model_type + append clean_tag to notes."""
    sys.path.insert(0, 'model')
    from training.registration import derive_model_type
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT model_version_id, model_type, version_name
            FROM model_versions
            WHERE created_at > %s AND is_active = FALSE
        """, (since_ts,))
        rows = cur.fetchall()
    renames = []
    for r in rows:
        try:
            canonical = derive_model_type(r['version_name'])
            if canonical != r['model_type']:
                renames.append((canonical, r['model_version_id']))
        except ValueError:
            pass
    with conn.cursor() as cur:
        for new_mt, mvid in renames:
            cur.execute("UPDATE model_versions SET model_type=%s WHERE model_version_id=%s",
                        (new_mt, mvid))
        # Tag with clean_post_repair5
        cur.execute("""
            UPDATE model_versions SET notes = COALESCE(notes,'') || E'\nclean_post_repair5_20260519'
            WHERE created_at > %s AND is_active = FALSE
              AND (notes IS NULL OR notes NOT LIKE '%%clean_post_repair5_20260519%%')
        """, (since_ts,))
    conn.commit()
    logger.info(f"  Renamed {len(renames)} rows via derive_model_type + tagged")


def main():
    for phase in PHASE_PLAN:
        logger.info(f"PHASE {phase['phase']}: {phase['description']}")
        phase_start = datetime.utcnow()
        arns = []
        arn_to_task = {}
        for t in phase['tasks']:
            arn = launch_task(t['cmd'])
            arns.append(arn); arn_to_task[arn] = t
            logger.info(f"  launched arn={arn[-12:]} cmd={' '.join(t['cmd'])}")
            time.sleep(2)
        results = wait_for_tasks(arns)
        failed = [a for a, c in results.items() if c != 0]
        if failed:
            for a in failed:
                logger.error(f"  FAILED {arn_to_task[a]['cmd']} exit={results[a]}")
            raise RuntimeError(f"Phase {phase['phase']} failures — HALT")
        # Apply derive + tag for this phase
        apply_derive_and_tag(phase_start.isoformat())
        logger.info(f"Phase {phase['phase']} COMPLETE")
    logger.info("REPAIR-5 Phase 2-4 ALL COMPLETE")


if __name__ == '__main__':
    main()
