# architecture_overview v2 — Verification Log

Companion log to `architecture_overview.md` v2 (DRAFT, 2026-05-05). Tier 3 verification discipline per META_PLAN v9 § 6.5. Companion-log requirement is a hard rule per META_PLAN v9 § 6.5 (not optional).

Author: CC. Date: 2026-05-05. Re-verification timestamp: 2026-05-05T19:30Z (single-session re-verification window).

Substrate inheritance: META_PLAN v9 (locked 2026-05-05; companion verification log `_audits/META_PLAN_v9_verification.md`) + BIBLE_STRUCTURE_SPEC v6 (locked 2026-05-05) + Architecture Overview v1 verification log (`_audit/architecture_overview_v1_verification.md`) + v1 audit findings (20 findings: 2 BLOCKER + 8 MATERIAL + 10 MINOR).

---

## Section A — Inherited claims from META_PLAN v9 verification log

Re-verified 2026-05-05; primary substrate for v2's RDS framing + 5/3 Lambda decomposition + 10/3 EventBridge decomposition + ECS / S3 / ECR / SNS / Secrets / API Gateway counts.

### A.M9-1 — META_PLAN v9 V9-1.D substrate replacement (RDS PostgreSQL standalone)
- Consumed at: § 3.3
- Source: META_PLAN v9 § 2.3 (corrected bullet) + V9-1.D verification log entry, primary citation Architecture Overview v1 verification log Claim V1-11 + Claim A.8.
- Re-verification 2026-05-05: `aws rds describe-db-instances --db-instance-identifier equine-db --query 'DBInstances[].[DBInstanceIdentifier,DBInstanceArn,Engine,EngineVersion,DBInstanceClass,Endpoint.Address,Endpoint.Port,DBInstanceStatus,DBClusterIdentifier]' --output text`
- Result: `equine-db arn:aws:rds:us-east-1:584812014683:db:equine-db postgres 16.6 db.t4g.micro equine-db.cgtuh834bttd.us-east-1.rds.amazonaws.com 5432 available None`
- Status: **CONFIRMED**. v2 § 3.3 inherits cleanly.

### A.M9-2 — META_PLAN v9 inheritance of 8-Lambda + 13-EventBridge + 41-route + 4-S3 + 3-ECR-named + 5-CDK-image + 5-ECS-family + 3-Secrets counts
- Consumed at: § 3.1, § 3.2, § 3.4-3.8
- Source: META_PLAN v9 § 2.3 enumeration (inherited from v8 unchanged; META_PLAN v8 inherited these counts from META_PLAN v6 verification log Claims 1, 3, 8, 17, 18, 19, 20).
- Status: **CONFIRMED** (per Section C V2-N entries below for fresh per-resource verification).

---

## Section B — Inherited claims from Architecture Overview v1 verification log

Re-verified 2026-05-05. The 12 V1-N claims + 11 inherited Section A claims from v1 (with A.8 REFUTED status preserved per META_PLAN v9 substrate correction).

### B.A1 (was v1 A.1) — 8 Lambdas, 5 Active + 3 Inactive
- Consumed at: § 3.1
- Re-verification: `aws lambda get-function-configuration --function-name <each>` for all 8.
- Result 2026-05-05: 8 functions present. **Active (5):** `equine-inference`, `equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference`, `equine-nyra-workouts`. **Inactive (3):** `equine-ingestion`, `equine-feature-engineering`, `equine-results` — all with `StateReason = "The function is trying to use a deleted image."` All 3 INACTIVE last-modified 2026-05-02.
- Status: **CONFIRMED**.

### B.A2 (was v1 A.2) — 13 EventBridge rules, 10 ENABLED + 3 DISABLED
- Consumed at: § 3.6
- Re-verification: `aws events list-rules --query 'Rules[?starts_with(Name, \`equine\`)].[Name,State,ScheduleExpression]' --output text | sort`
- Result 2026-05-05: 13 rules in expected ENABLED/DISABLED partition. Cron expressions match v1 enumeration.
- Status: **CONFIRMED**.

### B.A3 (was v1 A.3) — 41 API Gateway v2 routes
- Consumed at: § 3.5
- Re-verification: `aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100 --output json | python3 -c "import sys,json; d=json.load(sys.stdin); print('routes:', len(d.get('Items', [])))"`
- Result 2026-05-05: `routes: 41`.
- Status: **CONFIRMED**.

### B.A4 (was v1 A.4) — 5 ECR images in CDK-managed assets repository
- Consumed at: § 3.7
- Re-verification: `aws ecr describe-images --repository-name cdk-hnb659fds-container-assets-584812014683-us-east-1 --query 'length(imageDetails)' --output text`
- Result 2026-05-05: `5`.
- Status: **CONFIRMED**.

### B.A5 (was v1 A.5) — 4 S3 buckets enumerated by name
- Consumed at: § 3.4
- Re-verification: `aws s3api list-buckets --query 'Buckets[?starts_with(Name, \`equine\`)].Name' --output text`
- Result 2026-05-05: `equine-frontend equine-model-artifacts equine-processed-data equine-raw-data` (4 buckets).
- Status: **CONFIRMED**.

### B.A6 (was v1 A.6) — 3 Secrets Manager entries enumerated by name
- Consumed at: § 3.8
- Re-verification: `aws secretsmanager list-secrets --query 'SecretList[?starts_with(Name, \`equine\`)].Name' --output text`
- Result 2026-05-05: `equine-equalizer/db-credentials equine-equalizer/2captcha-api-key equine-equalizer/brightdata-api-key` (3 secrets).
- Status: **CONFIRMED**.

### B.A7 (was v1 A.7) — 5 ECS task definition families enumerated by name
- Consumed at: § 3.2
- Re-verification: `aws ecs list-task-definition-families --query 'families[?starts_with(@, \`equine\`)]' --output text`
- Result 2026-05-05: `equine-training equine-training-daily-full equine-training-manual equine-training-pl equine-training-win-prob` (5 families).
- Status: **CONFIRMED**.

### B.A8 (was v1 A.8) — Aurora cluster ARN REFUTED status preserved
- Consumed at: not in v2 body (substrate corrected upstream in META_PLAN v9 V9-1.D); preserved here for inheritance traceability.
- Re-verification: `aws rds describe-db-clusters --db-cluster-identifier equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`
- Result 2026-05-05: `An error occurred (DBClusterNotFoundFault) when calling the DescribeDBClusters operation: DBCluster equinedatabasestack-equinedatabase648a3917-y8mww81ea82f not found.`
- Status: **REFUTED** (status preserved from v1; META_PLAN v9 § 2.3 + § 7.12 + § 9.2 corrected upstream).

### B.A9 (was v1 A.9) — API Gateway v2 ID `gb5qlfy10h`
- Consumed at: § 3.5
- Re-verification: API ID confirmed valid via successful `aws apigatewayv2 get-routes` query (no `NotFoundException`).
- Status: **CONFIRMED**.

### B.A10 (was v1 A.10) — SNS topic name `equine-equalizer-alerts`
- Consumed at: § 3.8
- Re-verification: `aws sns list-topics --query 'Topics[?contains(TopicArn, \`equine\`)].TopicArn' --output text`
- Result 2026-05-05: `arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts`. One subscriber: `email tonyragano@gmail.com`.
- Status: **CONFIRMED**.

### B.A11 (was v1 A.11) — ECS cluster name `equine-cluster`
- Consumed at: § 3.2
- Re-verification: `aws ecs describe-clusters --clusters equine-cluster --query 'clusters[].[clusterName,status]' --output text`
- Result 2026-05-05: `equine-cluster ACTIVE`.
- Status: **CONFIRMED**.

### B.V1-1 — `backend/models/canonical.py` exists with 14 classes at expected lines
- Consumed at: § 2 + § 4.1 + § 4.2
- Re-verification: `grep -nE "^class " backend/models/canonical.py`
- Result 2026-05-05: 14 classes — Track:7, Horse:20, Trainer:39, Jockey:48, Workout:58, PastPerformance:77, Entry:214, Race:255, RaceCard:289, Result:296, ModelVersion:326, PLPrediction:351, LSPrediction:390, Prediction:428. Total file 481 lines.
- Status: **CONFIRMED**.

### B.V1-2 — WRPrediction class is ABSENT (preserved as historical fact; v2 reframes substantively per F14 resolution at V2-N below)
- Consumed at: § 4.2 (substantive reframing)
- Re-verification: `grep -nE "^class WRPrediction" backend/models/canonical.py; echo "exit: $?"`
- Result 2026-05-05: zero matches; exit code 1.
- Status: **CONFIRMED ABSENT**. v2 § 4.2 documents the substrate-correct framing per F14 (three independently-defined dataclasses, no inheritance, base `Prediction` is WR's shape with dynamic-attribute-attached enrichment per V2-N below).

### B.V1-3 — PLPrediction at line 351, LSPrediction at line 390, Prediction at line 428
- Consumed at: § 4.1 (Prediction) + § 4.2 (PLPrediction, LSPrediction)
- Re-verification: included in V1-1 grep above; lines confirmed.
- Status: **CONFIRMED**.

### B.V1-4 — psycopg2 direct connections (NOT RDS Data API)
- Consumed at: § 3.3 + § 3.8
- Re-verification: `grep -rn "rds_data\|boto3.*rds-data\|RDSDataService" backend/` (no production matches) + `grep -rn "import psycopg2" backend/` (matches in `backend/shared/db.py:5-6`, `backend/database/migrations/migrate.py:9`, vendored layers).
- Status: **CONFIRMED**. v2 § 3.3 also corrects the line-range to `13-39` (was `13-37` in v1) per F6 resolution — see V2-N below.

### B.V1-5 — Secrets Manager consumer enumeration (zero production-Lambda consumers for 2captcha + brightdata)
- Consumed at: § 3.8
- Status: **CONFIRMED** (v1 evidence preserved; not re-grep'd in v2 cycle since not affected by audit findings).

### B.V1-6 — Cross-references to subsequent Phase 1 bibles are forward-looking
- Consumed at: § 1 + § 4.3 + throughout § 3 cross-reference cells
- Re-verification: `ls /home/strakajagr/projects/equine-equalizer/docs/bible/*.md` 2026-05-05 still shows only `architecture_overview.md` (this draft) + `PHASE_5_BACKLOG.md`. The 6 target bibles do not yet exist.
- Status: **CONFIRMED forward-looking**. Documented as a forward-reference disclaimer in § 4.3 INDEX.

### B.V1-7 — ECS Fargate cluster name `equine-cluster`
- Consumed at: § 3.2
- See B.A11.
- Status: **CONFIRMED**.

### B.V1-8 — Named ECR repositories used by EE
- Consumed at: § 3.7
- Re-verification: `aws ecr describe-repositories --query 'repositories[?starts_with(repositoryName, \`equine\`)].repositoryName' --output text`
- Result 2026-05-05: `equine-training equine-nyra-workouts equine-equibase-acquisition` (3 named) + 1 CDK-managed (separate repo per A4).
- Status: **CONFIRMED**.

### B.V1-9 — Lambda memory and timeout configuration
- Consumed at: § 3.1 (tables)
- Re-verification: per-Lambda `aws lambda get-function-configuration --function-name <each>` (see V2-1 below for full re-decomposition with PackageType).
- Status: **CONFIRMED**. Memory/timeout per § 3.1 tables; all `PackageType = Image`.

### B.V1-10 — equine-ingestion-daily (ENABLED) targets INACTIVE equine-ingestion
- Consumed at: § 3.6 anomaly note + § 5.1 substrate provenance + § 6 Currently Open
- Re-verification: `aws events list-targets-by-rule --rule equine-ingestion-daily` returned `Target0 arn:aws:lambda:us-east-1:584812014683:function:equine-ingestion`. Combined with B.A1 (`equine-ingestion` is INACTIVE) → fire-and-fail confirmed.
- Status: **CONFIRMED**. v2 expands this finding per V2-2 below (3 additional rules also fire-and-fail; per v1 audit F1+F2+F3 BLOCKER/MATERIAL findings).

### B.V1-11 — RDS instance `equine-db` substantive characteristics
- Consumed at: § 3.3
- See A.M9-1.
- Status: **CONFIRMED**.

### B.V1-12 — SNS subscriber count
- Consumed at: § 3.8
- Re-verification: `aws sns list-subscriptions-by-topic --topic-arn arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts --query 'Subscriptions[].[Protocol,Endpoint]' --output text`
- Result 2026-05-05: `email tonyragano@gmail.com` (1 subscriber).
- Status: **CONFIRMED**.

**Section B summary:** 23 inherited claims re-verified (11 Section A from v1 + 12 V1-N). Status: 22 CONFIRMED, 1 REFUTED (B.A8 Aurora cluster — REFUTED status preserved; substrate corrected upstream in META_PLAN v9).

---

## Section C — New V2-N claims

### V2-1 — Per-Lambda configuration re-decomposition (8 Lambdas)
- Consumed at: § 3.1 (Active + Inactive tables)
- Source: `aws lambda get-function-configuration --function-name <each> --query '[FunctionName,State,StateReason,MemorySize,Timeout,LastModified,PackageType]' --output text` 2026-05-05T19:30Z
- Result (decomposed per Lambda):
  - `equine-inference Active None 1024 300 2026-05-02T15:45:11.000+0000 Image`
  - `equine-wr-inference Active None 1024 300 2026-05-02T15:45:10.000+0000 Image`
  - `equine-pl-inference Active None 1024 300 2026-05-02T15:45:11.000+0000 Image`
  - `equine-ls-inference Active None 1024 300 2026-05-02T15:45:11.000+0000 Image`
  - `equine-nyra-workouts Active None 512 300 2026-04-27T22:11:00.105+0000 Image`
  - `equine-ingestion Inactive "The function is trying to use a deleted image." 2048 900 2026-05-02T15:45:37.000+0000 Image`
  - `equine-feature-engineering Inactive "The function is trying to use a deleted image." 512 300 2026-05-02T15:45:11.000+0000 Image`
  - `equine-results Inactive "The function is trying to use a deleted image." 512 300 2026-05-02T15:45:11.000+0000 Image`
- Decomposition: 8 Lambdas = 5 Active (`equine-inference`, `equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference`, `equine-nyra-workouts`) + 3 Inactive (`equine-ingestion`, `equine-feature-engineering`, `equine-results`).
- All 3 Inactive last-modified 2026-05-02 (matches "the most recent CDK redeploy that culled their images").

### V2-2 — Per-EventBridge-rule target enumeration (13 rules; Lesson 5 in active operation)
- Consumed at: § 3.6 (ENABLED + DISABLED tables) + § 3.6 anomaly note + § 5.1 substrate provenance + § 5.2 substrate provenance + § 6 Currently Open
- Source: `aws events list-targets-by-rule --rule <each> --query 'Targets[].[Id,Arn,Input,EcsParameters.TaskDefinitionArn]' --output text` 2026-05-05T19:30Z (13 separate commands, one per rule)
- Result (decomposed per rule):

ENABLED rules (10):

- `equine-angle-stats-nightly` cron(15 2 * * ? *) → `arn:aws:lambda:us-east-1:584812014683:function:equine-ingestion` (INACTIVE per V2-1) with `Input = {"action":"refresh_angle_stats"}` — **fire-and-fail** (case 1 of 4)
- `equine-daily-retrain-full` cron(30 2 * * ? *) → `arn:aws:ecs:us-east-1:584812014683:cluster/equine-cluster` with `EcsParameters.TaskDefinitionArn = arn:aws:ecs:us-east-1:584812014683:task-definition/equine-training-daily-full`
- `equine-fetch-results-nightly` cron(30 1 * * ? *) → `arn:aws:lambda:us-east-1:584812014683:function:equine-ingestion` (INACTIVE per V2-1) — **fire-and-fail** (case 2 of 4)
- `equine-ingestion-daily` cron(0 11 * * ? *) → `arn:aws:lambda:us-east-1:584812014683:function:equine-ingestion` (INACTIVE per V2-1) — **fire-and-fail** (case 3 of 4)
- `equine-ls-inference-daily` cron(40 12 * * ? *) → `arn:aws:lambda:us-east-1:584812014683:function:equine-ls-inference` (Active per V2-1)
- `equine-nyra-workouts-daily` cron(0 10 * * ? *) → `arn:aws:lambda:us-east-1:584812014683:function:equine-nyra-workouts` (Active per V2-1) with `Input = {}`
- `equine-pl-inference-daily` cron(35 12 * * ? *) → `arn:aws:lambda:us-east-1:584812014683:function:equine-pl-inference` (Active per V2-1)
- `equine-results-daily` cron(0 4 * * ? *) → `arn:aws:lambda:us-east-1:584812014683:function:equine-results` (INACTIVE per V2-1) — **fire-and-fail** (case 4 of 4)
- `equine-weekly-retrain-wr` cron(0 4 ? * MON *) → `arn:aws:ecs:us-east-1:584812014683:cluster/equine-cluster` with `EcsParameters.TaskDefinitionArn = arn:aws:ecs:us-east-1:584812014683:task-definition/equine-training-win-prob`
- `equine-wr-inference-daily` cron(30 12 * * ? *) → `arn:aws:lambda:us-east-1:584812014683:function:equine-wr-inference` (Active per V2-1)

DISABLED rules (3):

- `equine-feature-engineering-daily` cron(0 12 * * ? *) → **zero current targets** (empty Targets list)
- `equine-inference-daily` cron(30 12 * * ? *) → **zero current targets** (empty Targets list)
- `equine-weekly-retrain-pl` cron(0 5 ? * MON *) → `arn:aws:ecs:us-east-1:584812014683:cluster/equine-cluster` with `EcsParameters.TaskDefinitionArn = arn:aws:ecs:us-east-1:584812014683:task-definition/equine-training-pl`

- **Decomposition**: 13 rules = 10 ENABLED + 3 DISABLED. Of the 10 ENABLED, 4 target INACTIVE Lambdas (3 → `equine-ingestion`, 1 → `equine-results`); 4 target Active Lambdas; 2 target ECS task families. Of the 3 DISABLED, 2 have zero current targets, 1 targets an ECS task family.
- Closes v1 audit F1 BLOCKER (`equine-angle-stats-nightly` target was mis-attributed to `equine-inference` in v1; actual target verified `equine-ingestion`), F2 BLOCKER (`equine-fetch-results-nightly` target was vague + wrong in v1; actual target verified `equine-ingestion`), F3 MATERIAL (anomaly count 2 → 4), F15 MATERIAL (§ 6 arithmetic 2-rules-3-Lambdas → 4-rules-2-Lambdas).

### V2-3 — `equine-inference` handler dispatch logic (closes v1 audit F4)
- Consumed at: § 3.1 Active table — `equine-inference` row
- Source: `grep -nE "def lambda_handler|action ==|path ==|^if |^    if " backend/lambdas/inference/handler.py` 2026-05-05
- Result: equine-inference handler dispatches by:
  - HTTP path/method: `/health` (line 74), `/dashboard/metrics` (78), `/races/available-dates` (84), `/races/today` (90), `/predictions/run` POST (94) + GET (98), `/races/<id>/detail` (102), race-card path (109), horse-pp path (120), `/predictions/value` (129), `/predictions/today` (134), unified path (145), pred-date path (160), race-date path (174)
  - EventBridge: `event['source'] == 'aws.events'` (line 55) → `service.run_daily_predictions(date.today())`
  - Batch from ingestion: `event['source'] == 'batch'` (line 64) → `service.run_daily_predictions(target_date)`
- **Negative finding**: `grep -nE "raw_query|set_active_model|refresh_angle_stats" backend/lambdas/inference/handler.py` returns zero matches. Those three admin actions are NOT handled by `equine-inference`.
- Closes v1 audit F4 MATERIAL (admin actions mis-attributed to `equine-inference` in v1; actually handled by `equine-ingestion` per V2-4 below).

### V2-4 — Admin actions hosted on `equine-ingestion` (INACTIVE) per `backend/lambdas/ingestion/handler.py`
- Consumed at: § 3.1 Inactive table — `equine-ingestion` row + § 6 Currently Open
- Source: `grep -nE "if action ==" backend/lambdas/ingestion/handler.py` 2026-05-05
- Result:
  - `if action == 'refresh_angle_stats':` at line 94
  - `if action == 'raw_query':` at line 595
  - `if action == 'set_active_model':` at line 645
- Decomposition: 3 admin actions hosted on `equine-ingestion`. Combined with V2-1 (`equine-ingestion` is INACTIVE), all 3 admin actions are currently non-functional. The `refresh_angle_stats` action is also EventBridge-triggered (per V2-2 `equine-angle-stats-nightly` rule) → fire-and-fail; `raw_query` and `set_active_model` are manually invoked → simply error on manual invoke.

### V2-5 — `backend/shared/db.py` `_get_connection_string()` line range 13–39 (closes v1 audit F6)
- Consumed at: § 3.3 + § 3.8
- Source: `sed -n '35,42p' backend/shared/db.py` 2026-05-05 confirms the f-string `return` statement begins on line 35 and ends with the closing paren `)` on line 39. Function `_get_connection_string()` opens at line 13 with `def _get_connection_string() -> str:`.
- Result: function spans lines 13–39 (not 13–37 as in v1).
- Closes v1 audit F6 MINOR.

### V2-6 — Canonical `Prediction` / `PLPrediction` / `LSPrediction` are independently-defined dataclasses (no inheritance) — closes v1 audit F14
- Consumed at: § 4.2
- Source: `grep -E "^class (PLPrediction|LSPrediction|Prediction)\(" backend/models/canonical.py` 2026-05-05 returns zero matches with parenthesized base-class lists. All three are bare `class X:` definitions per `grep -nE "^class (PLPrediction|LSPrediction|Prediction)\b" backend/models/canonical.py`:
  - `351:class PLPrediction:`
  - `390:class LSPrediction:`
  - `428:class Prediction:`
- Decomposition: 3 dataclasses, 0 inheritance edges between them. Field counts (per disk reading 2026-05-05):
  - base `Prediction` (lines 428-450+): ~21 canonical fields (`entry`, `race_id`, `horse_id`, `prediction_id`, `race_number`, `model_version_id`, `win_probability`, `place_probability`, `show_probability`, `predicted_rank`, `confidence_score`, `is_top_pick`, `is_value_flag`, `morning_line_implied_prob`, `overlay_pct`, `feature_importance`, `recommended_bet_type`, `exotic_partners`, `actual_finish`, `was_win`, `was_place`, ...).
  - `PLPrediction` (lines 351-386): ~26 canonical fields (`entry`, `race_id`, `horse_id`, `prediction_id`, `race_number`, `model_version_id`, `win_probability`, `predicted_ev`, `confidence_score`, `predicted_rank`, `is_top_pick`, `closing_odds`, `implied_probability`, `edge_pct`, `is_value_bet`, `is_strong_value`, `kelly_fraction`, `kelly_bet_size`, `feature_importance`, `actual_finish`, `was_win`, `bet_profit`, `created_at`, `handicapping_prob`, `market_prob`, Stream E fields).
  - `LSPrediction` (lines 390-424): ~25 canonical fields (`entry`, `race_id`, `horse_id`, `prediction_id`, `model_version_id`, `final_win_probability`, `longshot_alert`, `confidence`, `kelly_fraction`, `predicted_rank`, `xgb_rank_score`, `rf_longshot_prob`, `lstm_trajectory`, `calibrated_win_prob`, `bayesian_angle_ev`, `angle_description`, `feature_importance`, `actual_finish`, `was_win`, `actual_odds`, `bet_profit`, `created_at`, race-context fields, Stream E fields).
- Closes v1 audit F14 MATERIAL (substrate-correct framing baked into v2 § 4.2).

### V2-7 — WR pipeline dynamic attribute attachment at `backend/services/wr_inference_service.py:718-730`
- Consumed at: § 3.1 (`equine-wr-inference` row note) + § 4.2 (substantive evidence) + § 4.2 architectural-dissonance paragraph
- Source: `sed -n '716,733p' backend/services/wr_inference_service.py` 2026-05-05
- Result: 9 attributes attached to `pred` (a `Prediction` instance instantiated at line 693) via dynamic attribute assignment:
  - line 718: `pred.raw_win_prob = round(float(raw_probs[idx]), 4)`
  - line 719: `pred.handicapping_prob = round(handicapping_prob, 4)`
  - lines 720-722: `pred.market_prob = (round(market_prob, 4) if market_prob is not None else None)`
  - lines 723-725: `pred.edge_pct = (round(edge_pct, 4) if edge_pct is not None else None)`
  - line 726: `pred.rank_score = round(float(rank_scores[idx]), 4)`
  - line 727: `pred.kelly_fraction = value['kelly_fraction']`
  - line 728: `pred.kelly_bet = value['kelly_bet']`
  - line 729: `pred.has_workout_data = bool(has_workout[idx])`
  - line 730: `pred.model_used = model_used[idx]`
- Decomposition: 9 dynamic attribute assignments + 1 instantiation (`Prediction(...)` at line 693) + 1 list append (`predictions.append(pred)` at line 731). The 9 attached fields are NOT in the `Prediction` dataclass schema (verified by reading lines 428-450+; `raw_win_prob`, `handicapping_prob`, `market_prob`, `edge_pct`, `rank_score`, `kelly_fraction`, `kelly_bet`, `has_workout_data`, `model_used` not present in canonical class definition).
- WR pipeline `predict_race(...)` returns `list[Prediction]` per `wr_inference_service.py:497-499` — same `Prediction` type the inner loop instantiates.
- Substantive evidence for v2 § 4.2 architectural-dissonance paragraph (WR storage path consumes a hybrid object: canonical fields + dynamically-attached non-canonical fields).

### V2-8 — `equine-equibase-acquisition` ECR repository disposition (closes v1 audit F18)
- Consumed at: § 3.7 (third row) + § 7 Deprecated empty-section explicit qualifier
- Source A — image inventory: `aws ecr describe-images --repository-name equine-equibase-acquisition --query 'imageDetails[].[imagePushedAt]' --output text` 2026-05-05.
- Result A: 10 image push timestamps, all dated 2026-04-27 (range: 19:10:16 to 21:33:59 UTC-04:00). 10 images present in repository.
- Source B — production code reader inventory: `grep -rln "equine-equibase-acquisition" /home/strakajagr/projects/equine-equalizer/backend/ /home/strakajagr/projects/equine-equalizer/infrastructure/ 2>/dev/null` 2026-05-05.
- Result B: zero matches in `backend/` or `infrastructure/`. Broader search (`grep -rln "equine-equibase-acquisition" /home/strakajagr/projects/equine-equalizer/`) returns matches only in documentation files (`docs/bible/_meta/META_PLAN.md`, `docs/bible/architecture_overview.md`, `docs/bible/_meta/EE_CURRENT_STATE_DUMP.md`, `docs/bible/_audit/architecture_overview_v1_verification.md`).
- Decomposition: 10 images + 0 production code readers. Repository is orphaned in production code per Tier 4 substrate (working-tree post-baseline). v2 § 3.7 documents the verified counts + flags Phase 5 disposition pending a `PHASE_5_BACKLOG.md` entry. Hedge language ("planned-or-historical") replaced with verified facts.
- Closes v1 audit F18 MINOR.

### V2-9 — Deliverable numbering follows BIBLE_STRUCTURE_SPEC v6 § 8.2 drafting order, not § 4.1 inventory order (closes v1 audit F10)
- Consumed at: § 4.3 INDEX
- Source: BIBLE_STRUCTURE_SPEC v6 § 4.1 (inventory) + § 8.2 (drafting order) read 2026-05-05.
- Result: § 4.1 inventory order is `architecture_overview` (#1), `data_pipeline_bible` (#2), `feature_provenance_bible` (#3), `ml_layer_architecture_bible` (#4), `model_evaluation_retraining_bible` (#5), `database_schema_bible` (#6), `api_frontend_bible` (#7). § 8.2 drafting order is Architecture Overview first → Database & Schema second → Data Pipeline third → 3 ML bibles in parallel cohort (positions 4-6) → API & Frontend last (#7).
- v2 deliverable numbering uses § 8.2 drafting order: AO=1, DS=2, DP=3, FP=4, MLA=5, MER=6, API=7. Total 7 deliverables; numbering is contiguous; arithmetic adds up (1+1+1+3+1=7 with 3 ML bibles individually numbered 4, 5, 6 — not compressed under "4 of 7" as v1 did).
- Divergence between § 4.1 inventory order and § 8.2 drafting order surfaced explicitly in § 4.3 INDEX prose. v2 deliberately uses § 8.2 drafting order (the more reader-useful framing for "what's been drafted vs what remains").
- Closes v1 audit F10 MATERIAL.

### V2-10 — Bug #15 canonical home is `feature_provenance_bible` per BIBLE_STRUCTURE_SPEC v6 § 6.3 (closes v1 audit F13)
- Consumed at: § 4.3 INDEX navigation paths (Bug #15 / Bug #24 path corrected)
- Source: BIBLE_STRUCTURE_SPEC v6 § 6.3 line 656 read 2026-05-05: `8. What Was Fixed (canonical home for Bug #15 chain since the prevention is a feature-engineering pattern per META_PLAN v6 § 7.4)`.
- Result: Bug #15's canonical home is `feature_provenance_bible` (cross-reference syntax `feature_provenance_bible:#15`); calibration *mechanics* live at `ml_layer_architecture_bible:4.3` separately. v2 § 4.3 navigation path distinguishes the two routings (Bug #15 manifestation → feature_provenance; calibration mechanics → ml_layer).
- Closes v1 audit F13 MINOR.

### V2-11 — § 5 candidate-roster marker replaced with locked status (closes v1 audit F9)
- Consumed at: § 5 header marker
- Source: drafting-spec authorization carrying audit prompt's QB ratification statement.
- Result: v1 marker `[candidate roster pending QB ratification per § 5.7]` replaced with `[Locked 2026-05-05 per § 5.7 convergence rule + Tony's ratification of Architecture Overview v1 audit triage]`.
- Closes v1 audit F9 MINOR.

### V2-12 — § 5.1 + § 5.2 lock dates added (closes v1 audit F7)
- Consumed at: § 5.1 + § 5.2 section headers
- Source: drafting-spec authorization.
- Result:
  - § 5.1 header: `### 5.1 Forbidden Pattern: Documenting a Lambda's role without verifying its current State (locked 2026-05-05)`
  - § 5.2 header: `### 5.2 Common Mistake: Documenting an EventBridge rule's behavior without cross-referencing target State (locked 2026-05-05)`
- Both headers carry the `(locked 2026-05-05)` parenthetical per BIBLE_STRUCTURE_SPEC v6 § 5.4 + § 5.6.2 / § 5.6.3 mandatory-fields requirement; `(candidate)` qualifier dropped.
- Closes v1 audit F7 MATERIAL.

### V2-13 — § 5.2 rewritten in canonical "wrong instinct → corrected position" form per BIBLE_STRUCTURE_SPEC v6 § 5.6.3 (closes v1 audit F8 + F19)
- Consumed at: § 5.2 body
- Source: drafting-spec authorization + BIBLE_STRUCTURE_SPEC v6 § 5.6.3 mandatory fields.
- Result: § 5.2 body uses canonical Common Mistake template form — `**Wrong instinct:** "the cron is ENABLED, so the daily job runs."` paired with `**Corrected position:** NO. EventBridge rule State and Lambda State are independent...`. Substrate provenance preserved as final paragraph.
- Closes v1 audit F8 MATERIAL + F19 MINOR (the wrong-instinct quotation IS the worked example).

### V2-14 — § 5.1 FORBIDDEN code block expanded to 4 lines per META_PLAN v9 § 9.6 (closes v1 audit F11)
- Consumed at: § 5.1 FORBIDDEN code example
- Source: drafting-spec authorization + META_PLAN v9 § 9.6 (3-8 lines per side rule).
- Result: v1 FORBIDDEN was 1 line (violated 3-line floor); v2 FORBIDDEN is 4 lines (multi-line bible-section excerpt documenting rule + cron + downstream-effect + operational expectation without verifying State). CORRECT side preserved at 5 lines (compliant in both versions).
- Closes v1 audit F11 MINOR.

### V2-15 — § 5.1 substrate provenance updated for 4 fire-and-fail rules (closes v1 audit F17)
- Consumed at: § 5.1 substrate-provenance paragraph
- Source: V2-2 (per-rule target verification) for the 4 fire-and-fail enumeration.
- Result: § 5.1 substrate provenance enumerates all 4 fire-and-fail rules (`equine-ingestion-daily`, `equine-fetch-results-nightly`, `equine-angle-stats-nightly` → `equine-ingestion`; `equine-results-daily` → `equine-results`) with cross-reference to V2-N entries for fresh `aws events list-targets-by-rule` decomposition + 2026-05-05 timestamp. v1 cited "observed at lock for 2 rules"; v2 cites 4 rules.
- Closes v1 audit F17 MINOR.

### V2-16 — § 2 Definition of "Runtime context" widened to cover all 8 AWS resource classes (closes v1 audit F12)
- Consumed at: § 2 first definition entry
- Source: drafting-spec authorization + v1 audit F12 evidence (definition vs § 3 enumeration internal contradiction).
- Result: v1 definition restricted "runtime context" to 4 execution environments (Lambda, ECS Fargate, RDS, API Gateway); v2 widens to 8 AWS resource classes covering compute (Lambda, ECS Fargate), data (RDS PostgreSQL, S3), connectivity (API Gateway v2), config/secrets (Secrets Manager), messaging (SNS), image registry (ECR). Matches § 3.1 through § 3.8 enumeration. Reader-facing ambiguity resolved.
- Closes v1 audit F12 MINOR.

### V2-17 — § 3.4 model-artifact-layout citation corrected (closes v1 audit F5)
- Consumed at: § 3.4 `equine-model-artifacts` row
- Source: BIBLE_STRUCTURE_SPEC v6 line 804 read 2026-05-05: `4.3.2 S3 artifact paths (s3://equine-model-artifacts/<family>/<version>.json)`. Drafting spec Option A recommendation.
- Result: v1 cited `per META_PLAN v8 § 7.10` (which is "Commit-Before-Deploy Discipline", not model-registry layout — broken cross-reference). v2 cites `per BIBLE_STRUCTURE_SPEC v6 § 6.4 (the ml_layer_architecture_bible.md template's § 4.3.2 S3 artifact paths sub-section)`. Substantive home will be `ml_layer_architecture_bible:4.3` once that drafts.
- Closes v1 audit F5 MATERIAL.

### V2-18 — § 3.1 temporal scoping paragraph added (closes v1 audit F20)
- Consumed at: § 3.1 paragraph immediately following the Inactive table
- Source: META_PLAN v9 § 4.5 worked-example pattern (AWS Tier 1 vs DB Tier 3 temporal scoping).
- Result: paragraph added explaining production rows from before deactivation date (2026-05-02) are real and were correctly produced when Lambdas were Active; current State is INACTIVE; both facts coexist with explicit temporal scoping. AWS Tier 1 governs current-state assertions; DB Tier 3 governs historical-evidence assertions.
- Closes v1 audit F20 MINOR.

### V2-19 — § 4.3 INDEX navigation paths walked as concrete debugging scenarios (closes v1 audit F16)
- Consumed at: § 4.3 INDEX "Common navigation paths" section
- Source: drafting-spec authorization.
- Result: 3 of the 8 navigation paths walked as concrete reader-scenarios in 3-4 sentences each: "I'm investigating why yesterday's pipeline produced no predictions" (3 steps), "I'm chasing a 'function trying to use deleted image' alert" (3 steps), "I'm onboarding to EE" (4 steps). Remaining 5 paths preserved as one-liners.
- Closes v1 audit F16 MINOR.

### V2-20 — § 6 Currently Open arithmetic-corrected per F15 substrate evidence
- Consumed at: § 6 Currently Open
- Source: V2-2 (per-rule target verification).
- Result: v1 stated "2 ENABLED rules target 3 INACTIVE Lambdas" (arithmetically inconsistent). v2 states "4 ENABLED EventBridge rules target 2 INACTIVE Lambdas" with full per-rule decomposition: 3 rules → `equine-ingestion` (INACTIVE); 1 rule → `equine-results` (INACTIVE); third INACTIVE Lambda `equine-feature-engineering` not targeted by any ENABLED rule. Two additional admin actions on `equine-ingestion` (raw_query, set_active_model) also non-functional via the same INACTIVE-Lambda mechanism, but invoked manually rather than EventBridge-triggered.
- Closes v1 audit F15 MATERIAL.

**Section C summary:** 20 V2-N entries documented with full source citation + 2026-05-05 timestamp. All claims grounded in Tier 1 (live AWS state) or Tier 4 (working-tree code post-baseline 87dec36) per META_PLAN v9 § 4.5 source-priority hierarchy. Per Lesson 5, V2-2 alone documents 13 separate `aws events list-targets-by-rule` commands (one per rule).

---

## Section D — Methodology-interpolation self-check

Per META_PLAN v9 § 6.1 + BIBLE_STRUCTURE_SPEC v6 § 12.1 grandfathered constructs list. Drafter audits this draft for net new methodology constructs:

- **Net new methodology constructs introduced in v2 draft: ZERO.**
- **Pattern-completion check trivially satisfied:**
  - No new letter-prefixes (W.N exclusivity preserved per BIBLE_STRUCTURE_SPEC v6 § 5.5.1 + G-new-1 closure).
  - § 5 ratified-rule IDs use numeric sub-section IDs (`5.1`, `5.2`) per G-new-1 closure; no provisional letter-prefixes.
  - § 8 W.N format would be applied only when a § 8 entry is canonical here (none at v2 lock).
  - Cross-reference vocabulary (`<bible>:<section-id>` and `<bible>:#<bug-id>`) follows BIBLE_STRUCTURE_SPEC v6 § 7.1.1 + § 5.5.1 G9 closure; no new vocabulary introduced.
- **Ratified Discipline rules (§ 5.1 + § 5.2) are NOT new methodology constructs.** They are substrate-grounded surfaces of pre-existing methodology (META_PLAN v9 § 4.5 source-priority discipline + § 6.5 verification-log precision rule), ratified by Tony 2026-05-05 per audit prompt + drafting spec.
- **Methodology lessons 1-6 are operative discipline (banked, not codified).** v2 applies them as discipline (Lesson 1 cross-project contamination check applied via re-running all AWS commands fresh; Lesson 2 substrate-error surfacing applied — none surfaced; Lesson 3 primary-citation discipline applied throughout V2-N entries; Lesson 4 substrate-grounded reframing applied in § 4.2; Lesson 5 EventBridge per-rule list-targets-by-rule applied in V2-2; Lesson 6 banked for future AUDIT_METHODOLOGY codification). Discipline application is operative, not codified — v2 does NOT promote any of the 6 lessons to formal methodology rule with normative shape.

Grandfathering clause confirmed operative: pre-existing methodology constructs from META_PLAN v9 + BIBLE_STRUCTURE_SPEC v6 (e.g., source-priority hierarchy, W.N convention, decomposition discipline, FRAMEWORK_GAP / SPEC_GAP markers, no-fabrication rule, cross-reference syntax) are inherited; CC introduced none.

---

## Section E — Pattern-completion check

Per AUDIT_METHODOLOGY v2 § 5.5.

- **Letter-prefix exclusivity preserved.** W.N is the only letter-prefix used in BIBLE_STRUCTURE_SPEC-prescribed structure (§ 8 What Was Fixed entries). No § 8 entries at v2 lock; no W.N entries introduced.
- **§ 5 ratified-rule numeric IDs.** § 5.1 + § 5.2 use numeric sub-section IDs per G-new-1 closure. No provisional letter-prefixes (e.g., `5.A`, `5.B`) introduced.
- **§ 8 W.N format preserved.** If § 8 entries were introduced (none at v2 lock), they would follow `8.W.<n>` format with mandatory Fix date YYYY-MM-DD per BIBLE_STRUCTURE_SPEC v6 § 5.6.1 + § 5.6.1.2.
- **Decomposition discipline applied.** "8 Lambdas = 5 Active + 3 Inactive" (§ 3.1; V2-1 entry). "13 EventBridge rules = 10 ENABLED + 3 DISABLED" (§ 3.6; V2-2 entry). "5 ECS task families enumerated by name" (§ 3.2; B.A7). "4 S3 buckets enumerated by name" (§ 3.4; B.A5). "3 Secrets enumerated by name" (§ 3.8; B.A6). "5 ECR images in CDK-managed assets repository (separate from 3 named ECR repositories)" (§ 3.7; B.A4 + B.V1-8). "Of the 10 ENABLED rules, 4 target INACTIVE Lambdas (3 → equine-ingestion, 1 → equine-results), 4 target Active Lambdas, 2 target ECS task families" (§ 3.6 anomaly note + § 6 Currently Open; V2-2 + V2-20). "10 equine-equibase-acquisition images + 0 production code readers" (§ 3.7 third row; V2-8). "9 dynamic attribute attachments + 1 instantiation + 1 list append at wr_inference_service.py:693-731" (§ 4.2; V2-7). All counts decomposed where applicable per META_PLAN v9 § 6.5 verification-log precision rule.
- **G-new-2 inheritance pattern applied (not adopted as-is).** G-new-2 (database_schema_bible-specific: § 4.1 enumerates `CREATE TABLE` declarations only, matviews documented at § 3 only) does not apply directly to Architecture Overview (which doesn't enumerate tables or matviews). Inheritance pattern honored: each enumerated structural set names its scope explicitly (e.g., § 3.7 distinguishes "named ECR repositories" from "CDK-managed assets repository"; § 3.1 distinguishes Active vs Inactive; § 3.6 distinguishes ENABLED vs DISABLED + 4 fire-and-fail vs 6 healthy targets within ENABLED). No subsetting drift.

Pattern-completion check **PASS**.

---

## Section F — FRAMEWORK_GAP / SPEC_GAP markers

Drafter surfaces ZERO FRAMEWORK_GAP markers + ZERO SPEC_GAP markers in v2 draft.

- v1's E.1 (Aurora-vs-standalone-Postgres) closed by META_PLAN v9 V9-1.D substrate replacement. v2 inherits cleanly with no FRAMEWORK_GAP needed.
- v1's E.2 (WRPrediction class absence) closed by F14 substrate-correct reframing baked into v2 § 4.2 (three independently-defined dataclasses; base `Prediction` is WR's shape with dynamic attribute attachment; PL/LS are independently-defined per-pipeline shapes with their own field sets).
- No new gaps surfaced during v2 drafting. The spec's overall premise (EE has the runtime contexts it has, the canonical objects it has, the cross-bible navigation pattern BIBLE_STRUCTURE_SPEC v6 prescribes) is intact.

---

## Section G — v1 audit findings closure verification

Each of the 20 v1 findings (F1-F20 from `_audit/architecture_overview_v1_audit.md`) gets a closure verification entry. Format: finding ID + v1 audit-CC severity + v2 resolution method + V2-N verification log entry citation.

| v1 finding | Severity | Resolution method | V2-N entry | Closure status |
|---|---|---|---|---|
| F1 | BLOCKER | `equine-angle-stats-nightly` target corrected from `equine-inference` to `equine-ingestion` (INACTIVE) with `Input = {"action":"refresh_angle_stats"}` per fresh `aws events list-targets-by-rule`; row marked fire-and-fail in § 3.6 ENABLED table | V2-2 | **CLOSED** |
| F2 | BLOCKER | `equine-fetch-results-nightly` target corrected from vague "(see results-daily; one is legacy)" to `equine-ingestion` (INACTIVE) per fresh `aws events list-targets-by-rule`; row marked fire-and-fail in § 3.6 ENABLED table | V2-2 | **CLOSED** |
| F3 | MATERIAL | § 3.6 anomaly note restated: "Four cases at lock — three rules target equine-ingestion (INACTIVE), one rule targets equine-results (INACTIVE)" with full per-rule enumeration | V2-2, V2-20 | **CLOSED** |
| F4 | MATERIAL | `equine-inference` role description rewritten from primary code (`backend/lambdas/inference/handler.py`): HTTP-path-based router for dashboard + prediction-trigger endpoints + EventBridge `aws.events` daily-prediction trigger + `batch` source from ingestion. Admin-action enumeration RELOCATED to `equine-ingestion` INACTIVE row with non-functional note | V2-3, V2-4 | **CLOSED** |
| F5 | MATERIAL | § 3.4 `equine-model-artifacts` row citation corrected from `META_PLAN v8 § 7.10` to `BIBLE_STRUCTURE_SPEC v6 § 6.4` (the correct authority for S3 artifact-path layout) | V2-17 | **CLOSED** |
| F6 | MINOR | `backend/shared/db.py:13-37` corrected to `backend/shared/db.py:13-39` in both § 3.3 and § 3.8 citations | V2-5 | **CLOSED** |
| F7 | MATERIAL | Lock-date parentheticals `(locked 2026-05-05)` added to § 5.1 + § 5.2 headers; `(candidate)` qualifier dropped | V2-12 | **CLOSED** |
| F8 | MATERIAL | § 5.2 body rewritten in canonical Common Mistake "wrong instinct → corrected position" form per BIBLE_STRUCTURE_SPEC v6 § 5.6.3 | V2-13 | **CLOSED** |
| F9 | MINOR | § 5 candidate-roster marker replaced with `[Locked 2026-05-05 per § 5.7 convergence rule + Tony's ratification of Architecture Overview v1 audit triage]` | V2-11 | **CLOSED** |
| F10 | MATERIAL | § 4.3 INDEX deliverable numbering corrected to AO=1, DS=2, DP=3, FP=4, MLA=5, MER=6, API=7 (drafting-order numbering per § 8.2; arithmetic 1+1+1+3+1=7 with ML cohort individually numbered, not compressed under "4 of 7") | V2-9 | **CLOSED** |
| F11 | MINOR | § 5.1 FORBIDDEN code block expanded to 4 lines (multi-line bible-section excerpt) per META_PLAN v9 § 9.6 3-line floor | V2-14 | **CLOSED** |
| F12 | MINOR | § 2 "Runtime context" definition widened to cover all 8 AWS resource classes (compute / data / connectivity / config-secrets / messaging / image-registry); matches § 3.1 through § 3.8 enumeration | V2-16 | **CLOSED** |
| F13 | MINOR | § 4.3 INDEX navigation path for Bug #15 / Bug #24 split: Bug #15 manifestation routes to `feature_provenance_bible:#15` (canonical home per BIBLE_STRUCTURE_SPEC v6 § 6.3); calibration mechanics route to `ml_layer_architecture_bible:4.3` separately | V2-10 | **CLOSED** |
| F14 | MATERIAL | § 4.2 substrate-correct reframing: three independently-defined dataclasses (no Python inheritance); base `Prediction` is WR's shape with dynamic attribute attachment at `wr_inference_service.py:718-730`; `PLPrediction` and `LSPrediction` are independently-defined per-pipeline shapes with their own field sets. Architectural-dissonance paragraph surfaces hybrid-object storage path for QB awareness | V2-6, V2-7 | **CLOSED** |
| F15 | MATERIAL | § 6 Currently Open restated arithmetically-correct: "4 ENABLED EventBridge rules target 2 INACTIVE Lambdas" with full per-rule enumeration + manual-invoke admin-action note | V2-2, V2-20 | **CLOSED** |
| F16 | MINOR | § 4.3 INDEX 3 navigation paths walked as concrete debugging scenarios in 3-4 sentences each; remaining 5 paths preserved as one-liners | V2-19 | **CLOSED** |
| F17 | MINOR | § 5.1 substrate provenance updated to enumerate all 4 fire-and-fail rules with cross-reference to V2-N for fresh `list-targets-by-rule` decomposition | V2-15 | **CLOSED** |
| F18 | MINOR | § 3.7 `equine-equibase-acquisition` row hedge ("planned-or-historical") replaced with verified facts (10 images all pushed 2026-04-27; 0 production code readers; Phase 5 disposition pending) | V2-8 | **CLOSED** |
| F19 | MINOR | § 5.2 worked example provided naturally by F8 rewrite (the wrong-instinct quotation IS the example) | V2-13 | **CLOSED** |
| F20 | MINOR | § 3.1 temporal-scoping paragraph added per META_PLAN v9 § 4.5 worked-example pattern (AWS Tier 1 current state + DB Tier 3 historical evidence with explicit temporal scoping) | V2-18 | **CLOSED** |

**Section G summary:** 20 of 20 v1 audit findings CLOSED in v2. 2 BLOCKERs closed (F1, F2 via fresh `list-targets-by-rule` per Lesson 5). 8 MATERIALs closed. 10 MINORs closed.

---

## Verification log claim count summary

- **Section A inherited claims (META_PLAN v9):** 2 entries (A.M9-1 substrate replacement, A.M9-2 inherited counts).
- **Section B inherited claims (Architecture Overview v1):** 23 entries (11 from v1 Section A re-verified including B.A8 REFUTED-status preserved + 12 V1-N entries).
- **Section C new V2-N claims:** 20 entries (V2-1 through V2-20). V2-2 alone documents 13 separate per-rule `aws events list-targets-by-rule` commands per Lesson 5.
- **Section D net new methodology constructs:** 0.
- **Section E pattern-completion check:** PASS.
- **Section F FRAMEWORK_GAP / SPEC_GAP markers:** 0 FRAMEWORK_GAP, 0 SPEC_GAP.
- **Section G v1-audit-finding closure:** 20 of 20 CLOSED (2 BLOCKER + 8 MATERIAL + 10 MINOR).
- **Total verifiable substantive claims:** 45 (2 + 23 + 20).

---

**End of Architecture Overview v2 verification log.**
