# REPAIR-5 §4 Retrain — RESUME MARKER

**Created:** 2026-05-20 15:08Z by CC
**Status:** 5 ECS Fargate retrains LAUNCHED + PL bug FIXED + committed. Per-model cutover + commit + verification deferred to next session.

## Where we are

### Done this session
- All 5 ECS training tasks launched on PUBLIC subnets (first launch failed: ECR auth timeout on private subnets — no NAT/VPC endpoints; re-launched on public with `assignPublicIp=ENABLED`).
- PL `NoneType` bug root-caused + fixed: `pl_prediction_repository.py:insert_prediction` returns None on `ON CONFLICT DO NOTHING` when row already exists. Committed in `821eae2`. **Lambda image rebuild required to take effect in prod** — deferred to next CDK deploy wave.

### Branch
`repair-5-clean-deploy` @ `821eae2` on `/home/strakajagr/projects/equine-equalizer`.

### Active training tasks (5 ECS tasks, may still be running)

Pin file: `/tmp/repair5_retrain_task_arns_v2_20260520_110648.txt`

| trainer | task_id | produces |
|---|---|---|
| `model/ensemble/train.py` | `c77862f0e0bb41c098638abe5ae7b23f` | `ensemble` |
| `model/longshot/train.py` | `006813804f5f469c99ebf07ccae5fcff` | `longshot_rf` |
| `model/wr/train.py` | `6d404ff690d445b8b34387517ef8bdfb` | `wr_base` + `wr_odds` (Layer 1 core, both odds-blind + odds-aware) |
| `model/ranker/train.py` | `bcdb86d78d61492aa6f34d0b8104d484` | `ranker_core` + `ranker_full` (full bootstrap) |
| `model/win_prob/train.py` | `5fd7e841f85c447badbd4419ca6d61e9` | `win_prob_full` + win_prob_core (full bootstrap) |

Check status:
```bash
aws ecs describe-tasks --cluster equine-cluster --tasks <ALL TASK IDS ABOVE> \
  --query 'tasks[*].[startedBy,lastStatus,stopCode,containers[0].exitCode,stoppedAt]' --output text
```

Tail logs:
```bash
aws logs tail /ecs/equine-training --since 2h --follow
```

## What needs to happen next session

### Step 1 — verify each task succeeded
For each task:
- `lastStatus == STOPPED`
- `containers[0].exitCode == 0`
- ECS log group `/ecs/equine-training` shows successful training completion + S3 upload + model_versions registration

If any task failed → diagnose from logs, rerun if recoverable.

### Step 2 — per-model EVAL gate
Each new training registers a row in `model_versions` at `is_active = FALSE` with version_name like `<prefix>_<YYYYMMDD>_<HHMM>`. Compare EVAL metrics vs the current active baseline:

```sql
SELECT version_name, training_metadata->>'top1_accuracy', training_metadata->>'flat_bet_roi',
       training_metadata->>'kelly_roi', is_active, created_at
FROM model_versions
WHERE model_type = '<TARGET>'
ORDER BY created_at DESC LIMIT 5;
```

Targets and current-active baselines (captured 2026-05-20):
| model_type | currently active version | active mvid |
|---|---|---|
| ensemble | `ensemble_20260322_0649` | (query for mvid) |
| longshot_rf | `longshot_rf_20260322_0441` | |
| wr_base | `v_base_core_20260513_0259` | |
| wr_odds | `v_odds_core_20260513_0259` | |
| ranker_core | `rk_core_20260513_0323` | |
| ranker_full | `rk_full_20260429_0318` (51 feats, legacy pre-style-split) | |
| win_prob_full | `wp_odds_20260513_0126` | |

### Step 3 — per-model cutover (transactional with rollback SQL captured first)

For each model_type where the new training PASSED the EVAL gate:

```sql
-- ROLLBACK SQL (save to /tmp/repair5_cutover_rollback_<model>_<ts>.sql FIRST)
BEGIN;
UPDATE model_versions SET is_active = TRUE  WHERE model_version_id = '<OLD_ACTIVE_MVID>';
UPDATE model_versions SET is_active = FALSE WHERE model_version_id = '<NEW_MVID>';
COMMIT;

-- CUTOVER SQL
BEGIN;
UPDATE model_versions SET is_active = FALSE WHERE model_version_id = '<OLD_ACTIVE_MVID>';
UPDATE model_versions SET is_active = TRUE  WHERE model_version_id = '<NEW_MVID>';
COMMIT;
```

### Step 4 — per-model commit

```bash
git commit -m "REPAIR-5 §4: cutover <model_type> → <new_version_name>
EVAL gate PASS (top1=… vs baseline=…); rollback SQL at /tmp/...
"
```

### Step 5 — verify contamination = 0

```sql
-- Goal: 1 active row per model_type, no contaminated legacy active
SELECT model_type, version_name, created_at::text
FROM model_versions
WHERE model_type IN ('ensemble','longshot_rf','wr_base','wr_odds',
                     'ranker_core','ranker_full','win_prob_full')
  AND is_active = TRUE
ORDER BY model_type;
```

All version_name values should be the new training timestamps (post 2026-05-20 ~11:06 ET), not the 2026-03-22 / 2026-04-29 / 2026-05-13 legacy ones.

### Step 6 — deploy PL fix
The PL `NoneType` fix in `pl_prediction_repository.py` (commit `821eae2`) needs a Lambda image rebuild. Run `cdk deploy EquineComputeStack` — the diff should be: PL Lambda ImageUri swap only (just like resurrection deploy earlier today). Then re-smoke PL on a real odds-substrate race; confirm predictions land without NoneType.

### Step 7 — re-enable EventBridge retrain rules + final smoke
Per original dispatch §5. EventBridge rules for daily retrain may have been disabled — verify and re-enable. Final WR/PL/LS smoke + Hybrid C integration test.

### Step 8 — final tag
`git tag REPAIR-5-FULL-CLOSURE-COMPLETE && git push --tags`

## Known followups still open
1. `cdk deploy` to ship PL fix (commit `821eae2`)
2. PL calibration sidecar 404s for `wp_full_lean58_20260519_2006` + `pl_core_lean58_20260519_2023` — pre-existing, low impact
3. `ranker_full` 51-feat legacy artifact will be superseded once the ranker retrain lands
4. Push scraper repo (`/home/strakajagr/equibase_scraper/`) to a remote
5. Dynasty-Dugout uncommitted work — needs its own QB-CC dispatch
6. EE main repo: `repair-5-clean-deploy` branch is 42+ commits ahead of `origin/main` — eventually need to merge / push when stable
