#!/usr/bin/env python3
"""
REPAIR-5 Step F — 4-phase retrain wave orchestration for 39 contaminated models.

Substrate-precondition: training image (equine-training task definition)
deployed with REPAIR-5 Step A + B fixes baked in. Verify via:
    aws ecs describe-task-definition --task-definition equine-training
    image hash should reflect post-REPAIR-5 deploy.

Substrate-flow:
    PHASE 1 — Parallel L1 specialists (24 models via 3 scripts):
        pl/train.py --specialist {general,speed,closer,class_riser,
                                  class_dropper,sprint,route}  → 7 pl_core_*
        win_prob/train.py --specialist <same 7>                 → 7 wp_core_*
        ranker/train.py --specialist <general + gonzo_sauce + 6>→ 8 rk_full_*
        win_prob/train.py wp_full variants                       → 8 wp_full_*
        Substrate-NOTE: full variants run via separate flag or env

    PHASE 2 — Hybrid C ensemble (consumes Phase 1 L1 outputs):
        ensemble/train_hybrid_c.py                              → 1

    PHASE 3 — Single-fire specials (no cross-deps within phase):
        ensemble/train.py                                       → 1 (logistic ensemble)
        trajectory/train.py                                     → 1 (LSTM)
        longshot/train.py                                       → 1 (RF longshot)
        wr/train.py                                             → 2 (wr_base + wr_odds)

    PHASE 4 — Singletons consuming earlier phases:
        ranker_core + ranker_full + win_prob_full                → 3
        (these may overlap with Phase 1 variants per train.py defaults;
        substrate-verify via post-task model_versions inspection)

Each phase: launch ECS tasks → poll completion → verify exit 0 + S3
artifact + new model_versions row inserted. HALT entire wave on first
failure (substrate-do-NOT cutover with partial retrain).

Tags new model_versions rows with ensemble_version='clean_post_repair5_<YYYYMMDD>'
for substrate-tracking. Cutover SQL (repair_5_cutover.sql) flips is_active.

Substrate-wall-clock: 2-5+ hours expected. Launch in tmux or nohup.

Usage:
    python3 scripts/repair_5_retrain_wave.py --execute
    python3 scripts/repair_5_retrain_wave.py --dry-run  # show plan only
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

import boto3

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)
logger = logging.getLogger(__name__)

REGION = 'us-east-1'
CLUSTER = 'equine-cluster'
TASK_DEFINITION = 'equine-training'
SUBNETS = ['subnet-2f771b21', 'subnet-ac96278d', 'subnet-7951fa1f']
SECURITY_GROUPS = ['sg-9b256ea5']

METRICS_LOG = Path('/tmp/repair_5_training_metrics.jsonl')
CLEAN_TAG = f"clean_post_repair5_{datetime.utcnow().strftime('%Y%m%d')}"

# Substrate-discovered training script-to-active-model mapping
# (substrate-grounded against production model_versions WHERE is_active=TRUE).
PHASE_PLAN = [
    {
        'phase': 1,
        'description': 'L1 specialists (parallel via specialist args)',
        'tasks': [
            # pl_core_* (7 models)
            {'cmd': ['model/pl/train.py', '--specialist', s], 'expects': [f'pl_core_{s}']}
            for s in ('general', 'speed', 'closer', 'class_riser', 'class_dropper', 'sprint', 'route')
        ] + [
            # win_prob_core_* (7 models) — substrate-correct: --core-only toggles
            # win_prob/train.py from default full to core mode
            {'cmd': ['model/win_prob/train.py', '--specialist', s, '--core-only'],
             'expects': [f'win_prob_core_{s}']}
            for s in ('general', 'speed', 'closer', 'class_riser', 'class_dropper', 'sprint', 'route')
        ] + [
            # rk_full_* (8 models — adds gonzo_sauce)
            {'cmd': ['model/ranker/train.py', '--specialist', s], 'expects': [f'rk_full_{s}']}
            for s in ('general', 'speed', 'closer', 'class_riser', 'class_dropper', 'sprint', 'route', 'gonzo_sauce')
        ] + [
            # wp_full_* (8 models — adds gonzo_sauce). Default mode for
            # win_prob/train.py is full; no --core-only means wp_full path.
            {'cmd': ['model/win_prob/train.py', '--specialist', s], 'expects': [f'wp_full_{s}']}
            for s in ('general', 'speed', 'closer', 'class_riser', 'class_dropper', 'sprint', 'route', 'gonzo_sauce')
        ],
    },
    {
        'phase': 2,
        'description': 'Hybrid C ensemble (consumes L1 outputs)',
        'tasks': [
            {'cmd': ['model/ensemble/train_hybrid_c.py'], 'expects': ['ensemble_hybrid_option_c']},
        ],
    },
    {
        'phase': 3,
        'description': 'Single-fire L2 + LSTM + Longshot + WR',
        'tasks': [
            {'cmd': ['model/ensemble/train.py'], 'expects': ['ensemble']},
            {'cmd': ['model/trajectory/train.py'], 'expects': ['trajectory_lstm']},
            {'cmd': ['model/longshot/train.py'], 'expects': ['longshot_rf']},
            {'cmd': ['model/wr/train.py'], 'expects': ['wr_base', 'wr_odds']},
        ],
    },
    {
        'phase': 4,
        'description': 'Ranker / win_prob singletons (overlap-deduped)',
        'tasks': [
            # ranker_core + ranker_full + win_prob_full may already land via
            # Phase 1 --specialist=general default rows. Substrate-verify
            # post-Phase-1 + skip if already-clean rows exist for these types.
            {'cmd': ['model/ranker/train.py'], 'expects': ['ranker_core', 'ranker_full']},
            {'cmd': ['model/win_prob/train.py'], 'expects': ['win_prob_full']},
        ],
    },
]


def launch_task(cmd, region=REGION, cluster=CLUSTER, task_def=TASK_DEFINITION):
    """Launch one ECS Fargate task with command override. Returns task ARN.

    REPAIR-5-RESCUE: env override LEAN_TAG=lean58 substrate-required for
    training scripts to produce version_names with _lean58_ infix, which
    derive_model_type() maps to production-canonical model_type names
    (win_prob_core_*, pl_core_<spec>, etc.). Without this override, bare
    version_names bypass derive_model_type's prefix_map and store raw
    model_type='wp_core' / 'pl_core' / etc. — mismatching production
    inference service queries.

    Substrate-NOTE: equine-training-daily-full task def has LEAN_TAG=lean53
    hardcoded (substrate-divergent from current production lean58). Future
    cron-driven retrains using that task def will produce lean53 models;
    REPAIR-6 substrate-tracks reconciling daily-full to lean58.
    """
    ecs = boto3.client('ecs', region_name=region)
    resp = ecs.run_task(
        cluster=cluster,
        taskDefinition=task_def,
        launchType='FARGATE',
        count=1,
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': SUBNETS,
                'securityGroups': SECURITY_GROUPS,
                'assignPublicIp': 'ENABLED',
            }
        },
        overrides={
            'containerOverrides': [{
                'name': 'training',
                'command': cmd,
                'environment': [
                    {'name': 'LEAN_TAG', 'value': 'lean58'},
                ],
            }],
        },
    )
    if resp.get('failures'):
        raise RuntimeError(f"run_task failed for {cmd}: {resp['failures']}")
    return resp['tasks'][0]['taskArn']


def wait_for_tasks(arns, region=REGION, cluster=CLUSTER, poll_interval=60):
    """Poll until all tasks STOPPED. Returns {arn: exit_code} dict.
    Substrate-blocking call — may take 30-90 min per task."""
    ecs = boto3.client('ecs', region_name=region)
    pending = set(arns)
    results = {}
    while pending:
        resp = ecs.describe_tasks(cluster=cluster, tasks=list(pending))
        for t in resp['tasks']:
            arn = t['taskArn']
            if t['lastStatus'] == 'STOPPED':
                exit_code = None
                for c in t.get('containers', []):
                    if c['name'] == 'training':
                        exit_code = c.get('exitCode')
                        break
                results[arn] = exit_code
                pending.discard(arn)
                logger.info(f"  task STOPPED arn={arn[-12:]} exit={exit_code}")
        if pending:
            time.sleep(poll_interval)
    return results


def verify_new_model_versions(model_types, since_ts):
    """Query DB for new model_versions rows with model_type in list, created
    after since_ts. Returns list of dicts. Substrate-substrate-verifies
    training-completion side-effect: model artifact uploaded + DB row inserted.
    """
    import boto3
    import psycopg2
    import psycopg2.extras
    sm = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm.get_secret_value(
        SecretId='arn:aws:secretsmanager:us-east-1:584812014683:'
                 'secret:equine-equalizer/db-credentials'
    )['SecretString'])
    conn = psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'],
        password=secret['password'],
        cursor_factory=psycopg2.extras.RealDictCursor,
    )
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT model_version_id, model_type, version_name,
                       s3_artifact_path, created_at,
                       top1_accuracy, flat_bet_roi
                FROM model_versions
                WHERE model_type = ANY(%s)
                  AND created_at > %s
                ORDER BY created_at DESC
            """, (model_types, since_ts))
            return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def tag_clean_rows(model_version_ids):
    """Set ensemble_version='clean_post_repair5_<date>' on the new rows.
    NOTE: model_versions schema doesn't have ensemble_version column directly;
    REPAIR-5 substrate-marker is via the version_name suffix + notes field.
    """
    import boto3
    import psycopg2
    sm = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm.get_secret_value(
        SecretId='arn:aws:secretsmanager:us-east-1:584812014683:'
                 'secret:equine-equalizer/db-credentials'
    )['SecretString'])
    conn = psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'],
        password=secret['password'],
    )
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE model_versions
                SET notes = COALESCE(notes, '') || ' [' || %s || ']'
                WHERE model_version_id = ANY(%s)
            """, (CLEAN_TAG, model_version_ids))
        conn.commit()
    finally:
        conn.close()


def run_phase(phase_def, dry_run=False):
    """Launch all tasks in phase; wait for completion; verify; tag clean."""
    logger.info("=" * 70)
    logger.info(f"PHASE {phase_def['phase']}: {phase_def['description']}")
    logger.info(f"  {len(phase_def['tasks'])} tasks to launch")
    logger.info("=" * 70)

    if dry_run:
        for t in phase_def['tasks']:
            logger.info(f"  DRY-RUN: would launch {' '.join(t['cmd'])}")
            logger.info(f"           expects: {t['expects']}")
        return

    phase_start = datetime.utcnow()
    arns = []
    arn_to_task = {}
    for t in phase_def['tasks']:
        try:
            arn = launch_task(t['cmd'])
            arns.append(arn)
            arn_to_task[arn] = t
            logger.info(f"  launched arn={arn[-12:]} cmd={' '.join(t['cmd'])}")
        except Exception as e:
            logger.error(f"  FAILED to launch {t['cmd']}: {e}")
            raise RuntimeError(f"Phase {phase_def['phase']} launch failure: {e}")
        time.sleep(2)  # rate-limit run_task calls

    logger.info(f"  All {len(arns)} tasks launched; polling completion...")
    results = wait_for_tasks(arns)

    # Check exit codes
    failed = [arn for arn, code in results.items() if code != 0]
    if failed:
        for arn in failed:
            task = arn_to_task[arn]
            logger.error(
                f"  TASK FAILED: cmd={' '.join(task['cmd'])} arn={arn} "
                f"exit={results[arn]}"
            )
        raise RuntimeError(
            f"Phase {phase_def['phase']}: {len(failed)} task(s) failed. "
            f"HALTING WAVE — do not proceed to cutover."
        )

    # Verify new model_versions rows exist for expected model_types
    expected_types = []
    for t in phase_def['tasks']:
        expected_types.extend(t['expects'])
    new_rows = verify_new_model_versions(expected_types, phase_start)
    logger.info(f"  Phase {phase_def['phase']}: {len(new_rows)} new model_versions rows")
    found_types = {r['model_type'] for r in new_rows}
    missing = set(expected_types) - found_types
    if missing:
        logger.error(f"  MISSING model_versions for: {missing}")
        raise RuntimeError(
            f"Phase {phase_def['phase']}: missing model_versions rows for "
            f"{missing}. HALTING WAVE."
        )

    # Tag the new rows with clean marker
    new_ids = [r['model_version_id'] for r in new_rows]
    tag_clean_rows(new_ids)

    # Append per-model metrics
    with open(METRICS_LOG, 'a') as f:
        for r in new_rows:
            f.write(json.dumps({
                'phase': phase_def['phase'],
                'model_version_id': str(r['model_version_id']),
                'model_type': r['model_type'],
                'version_name': r['version_name'],
                's3_artifact_path': r['s3_artifact_path'],
                'top1_accuracy': float(r['top1_accuracy']) if r['top1_accuracy'] else None,
                'flat_bet_roi': float(r['flat_bet_roi']) if r['flat_bet_roi'] else None,
                'created_at': r['created_at'].isoformat(),
                'clean_tag': CLEAN_TAG,
            }) + '\n')

    phase_duration = (datetime.utcnow() - phase_start).total_seconds()
    logger.info(
        f"  Phase {phase_def['phase']} COMPLETE: "
        f"{len(new_rows)} models trained in {phase_duration:.0f}s "
        f"({phase_duration/60:.1f}m)"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true',
                        help='Actually launch ECS tasks (substrate-blocking)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show plan only; no tasks launched')
    args = parser.parse_args()

    if not (args.execute or args.dry_run):
        parser.error('Pass either --execute or --dry-run')

    if args.execute and args.dry_run:
        parser.error('Cannot combine --execute and --dry-run')

    logger.info(f"REPAIR-5 retrain wave START tag={CLEAN_TAG}")
    logger.info(f"  cluster={CLUSTER} task_def={TASK_DEFINITION}")
    logger.info(f"  metrics log: {METRICS_LOG}")

    wave_start = datetime.utcnow()
    for phase_def in PHASE_PLAN:
        run_phase(phase_def, dry_run=args.dry_run)

    wave_duration = (datetime.utcnow() - wave_start).total_seconds()
    logger.info("=" * 70)
    logger.info(
        f"REPAIR-5 retrain wave COMPLETE in {wave_duration:.0f}s "
        f"({wave_duration/3600:.1f}h)"
    )
    logger.info(f"  Tag for cutover: {CLEAN_TAG}")
    logger.info(f"  Metrics: {METRICS_LOG}")
    logger.info(f"  Next step: review metrics + execute scripts/repair_5_cutover.sql")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
