# architecture_overview v1 — Verification Log

Companion log to `architecture_overview.md` v1 (DRAFT, 2026-05-05). Tier 3 verification discipline per META_PLAN v8 § 6.5. Companion-log requirement is a hard rule per META_PLAN v8 § 6.5 (not optional).

Author: CC. Date: 2026-05-05. Re-verification timestamp: 2026-05-05T18:59:17Z (single-session re-verification window).

---

## Section A — Inherited claims from META_PLAN v8 verification log (re-verified 2026-05-05; not re-derived)

Each entry: META_PLAN v8 Claim ID → Architecture Overview section consuming the claim → re-verification command → live result 2026-05-05 → status (CONFIRMED / DRIFTED / REFUTED).

### A.1 Claim 1 — 8 Lambda functions, 5 Active + 3 INACTIVE
- Consumed at: § 3.1
- Re-verification: `aws lambda list-functions --query 'Functions[?starts_with(FunctionName, \`equine\`)].FunctionName' --output text` + `aws lambda get-function --function-name <each> --query 'Configuration.[State,StateReason,LastModified]'`
- Result 2026-05-05T18:59Z: 8 functions present. **Active (5):** `equine-inference`, `equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference`, `equine-nyra-workouts`. **Inactive (3):** `equine-ingestion`, `equine-feature-engineering`, `equine-results` — all with `StateReason = "The function is trying to use a deleted image."` All 3 INACTIVE last-modified 2026-05-02 (the most recent CDK redeploy).
- Status: **CONFIRMED**.

### A.2 Claim 3 — 13 EventBridge rules, 10 ENABLED + 3 DISABLED
- Consumed at: § 3.6
- Re-verification: `aws events list-rules --query 'Rules[?starts_with(Name, \`equine\`)].[Name,State,ScheduleExpression]' --output text | sort`
- Result 2026-05-05T18:59Z: 13 rules. **ENABLED (10):** `equine-angle-stats-nightly` `cron(15 2 * * ? *)`, `equine-daily-retrain-full` `cron(30 2 * * ? *)`, `equine-fetch-results-nightly` `cron(30 1 * * ? *)`, `equine-ingestion-daily` `cron(0 11 * * ? *)`, `equine-ls-inference-daily` `cron(40 12 * * ? *)`, `equine-nyra-workouts-daily` `cron(0 10 * * ? *)`, `equine-pl-inference-daily` `cron(35 12 * * ? *)`, `equine-results-daily` `cron(0 4 * * ? *)`, `equine-weekly-retrain-wr` `cron(0 4 ? * MON *)`, `equine-wr-inference-daily` `cron(30 12 * * ? *)`. **DISABLED (3):** `equine-feature-engineering-daily`, `equine-inference-daily`, `equine-weekly-retrain-pl`.
- Status: **CONFIRMED**.

### A.3 Claim 8 — 41 API Gateway v2 routes
- Consumed at: § 3.5
- Re-verification: `aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100 --output json | python3 -c "import sys,json; d=json.load(sys.stdin); print('items:', len(d['Items']))"` (note: `--max-results 100` necessary; default pagination at 25-per-page split the result into two pages of 25 + 16 in initial query, an artifact of AWS CLI pagination not a count discrepancy).
- Result 2026-05-05T18:59Z: `items: 41 / next: none`.
- Status: **CONFIRMED**.

### A.4 Claim 17 — 5 ECR images in CDK-managed assets repository
- Consumed at: § 3.7
- Re-verification: `aws ecr describe-images --repository-name cdk-hnb659fds-container-assets-584812014683-us-east-1 --query 'length(imageDetails)' --output text`
- Result 2026-05-05T18:59Z: `5`. Image hashes: `6954a22ade…`, `b3c8ab1d55…`, `b16e34600d…`, `cca88c50cf…`, `f89865aeaa…` (truncated).
- Status: **CONFIRMED**. The 5 surviving image hashes correspond to the 5 Active Lambdas' deployed images (one image per Active Lambda, matching the CDK asset-per-Image-Function pattern). The 3 INACTIVE Lambdas' deployed-image hashes have been culled, producing the "deleted image" StateReason at § 3.1.

### A.5 Claim 18 — 4 S3 buckets enumerated by name
- Consumed at: § 3.4
- Re-verification: `aws s3api list-buckets --query 'Buckets[?starts_with(Name, \`equine\`)].Name' --output text`
- Result 2026-05-05T18:59Z: `equine-frontend equine-model-artifacts equine-processed-data equine-raw-data` (4 buckets).
- Status: **CONFIRMED**.

### A.6 Claim 19 — 3 Secrets Manager entries enumerated by name
- Consumed at: § 3.8
- Re-verification: `aws secretsmanager list-secrets --query 'SecretList[?starts_with(Name, \`equine\`)].Name' --output text`
- Result 2026-05-05T18:59Z: `equine-equalizer/db-credentials equine-equalizer/2captcha-api-key equine-equalizer/brightdata-api-key` (3 secrets).
- Status: **CONFIRMED**.

### A.7 Claim 20 — 5 ECS task definition families enumerated by name
- Consumed at: § 3.2
- Re-verification: `aws ecs list-task-definition-families --query 'families[?starts_with(@, \`equine\`)]' --output text`
- Result 2026-05-05T18:59Z: `equine-training equine-training-daily-full equine-training-manual equine-training-pl equine-training-win-prob` (5 families).
- Status: **CONFIRMED**.

### A.8 Aurora cluster ARN (`arn:aws:rds:us-east-1:584812014683:cluster:equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`)
- Consumed at: § 3.3
- Re-verification: `aws rds describe-db-clusters --db-cluster-identifier equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`
- Result 2026-05-05T18:59Z: `An error occurred (DBClusterNotFoundFault) when calling the DescribeDBClusters operation: DBCluster equinedatabasestack-equinedatabase648a3917-y8mww81ea82f not found.` Broader query `aws rds describe-db-clusters --query 'DBClusters[].[DBClusterIdentifier,DBClusterArn,Engine,EngineVersion,Status]' --output text` returns ONE cluster: `fantasy-baseball-serverless aurora-postgresql 16.11 available` (a different project entirely; not EE). EE has NO Aurora cluster.
- Status: **REFUTED.** META_PLAN v8 verification log inherited claim is wrong. Live AWS state shows EE uses a **standalone RDS PostgreSQL instance** named `equine-db` (not Aurora, not Aurora Serverless, not part of any cluster):
  - DB instance ARN: `arn:aws:rds:us-east-1:584812014683:db:equine-db`
  - Engine: `postgres` 16.6 (not `aurora-postgresql`)
  - Instance class: `db.t4g.micro`
  - Endpoint: `equine-db.cgtuh834bttd.us-east-1.rds.amazonaws.com:5432`
  - DBName: `equine_equalizer`
  - DBClusterIdentifier: `None` (standalone instance, not in a cluster)
- Per META_PLAN v8 § 4.5 source-priority: Tier 1 (live AWS state) governs over Tier 6 (inherited dump-derived claim). Architecture Overview § 3.3 documents the actual substrate. FRAMEWORK_GAP marker surfaced at § 3.3 + Section E.1 below. Recommended action: QB ratifies the override + retroactively corrects META_PLAN v8 verification log entry. Source of inherited error is likely `EE_CURRENT_STATE_DUMP.md` (which has been wrong about multiple facts per META_PLAN v8 § 4.5 Tier 6 caveat).

### A.9 API Gateway v2 ID (`gb5qlfy10h`)
- Consumed at: § 3.5
- Re-verification: `aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100` returns valid response with 41 items (no `NotFoundException`); confirms the ID is valid.
- Result 2026-05-05T18:59Z: ID confirmed valid.
- Status: **CONFIRMED**.

### A.10 SNS topic name (`equine-equalizer-alerts`)
- Consumed at: § 3.8
- Re-verification: `aws sns list-topics --query 'Topics[?contains(TopicArn, \`equine\`)].TopicArn' --output text`
- Result 2026-05-05T18:59Z: `arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts`. One subscriber: `email tonyragano@gmail.com`.
- Status: **CONFIRMED**.

### A.11 ECS cluster name (`equine-cluster`)
- Consumed at: § 3.2
- Re-verification: `aws ecs describe-clusters --clusters equine-cluster --query 'clusters[].[clusterName,status]' --output text`
- Result 2026-05-05T18:59Z: `equine-cluster ACTIVE`.
- Status: **CONFIRMED**.

**Section A summary:** 11 inherited claims re-verified; **10 CONFIRMED, 1 REFUTED** (Claim A.8 Aurora cluster ARN). Refutation drives the Section E.1 FRAMEWORK_GAP marker.

---

## Section B — New claims introduced in Architecture Overview v1

### V1-1 — `backend/models/canonical.py` exists at expected path with 14 classes
- Consumed at: § 2 + § 4.1 + § 4.2
- Source: `grep -nE "^class " backend/models/canonical.py` 2026-05-05T18:58Z
- Result: 14 classes present:
  - `Track` (line 7), `Horse` (line 20), `Trainer` (line 39), `Jockey` (line 48), `Workout` (line 58), `PastPerformance` (line 77), `Entry` (line 214), `Race` (line 255), `RaceCard` (line 289), `Result` (line 296), `ModelVersion` (line 326), `PLPrediction` (line 351), `LSPrediction` (line 390), `Prediction` (line 428).
- Total file size: 481 lines (`wc -l`).

### V1-2 — WRPrediction class is ABSENT from `backend/models/canonical.py`
- Consumed at: § 4.2 + Section E.2 FRAMEWORK_GAP marker
- Source: `grep -nE "^class WRPrediction" backend/models/canonical.py; echo "exit: $?"` 2026-05-05T18:58Z
- Result: zero matches; exit code 1.
- Status: HONESTLY DOCUMENTED ABSENT per META_PLAN v8 § 8.6 no-fabrication discipline. § 4.2 documents 2 per-pipeline shapes (PLPrediction, LSPrediction) and surfaces FRAMEWORK_GAP marker for QB ratification of either: (a) canonicalize-WRPrediction Phase 5 work, (b) document-WR-uses-base-Prediction-and-update-spec, or (c) Phase-5-architectural-cleanup with WR-shape-decision deferred. WR pipeline (`equine-wr-inference` Lambda) currently appears to use base `Prediction` class (line 428) or constructs DB row shape inline; substantive WR-shape-pattern documentation is `ml_layer_architecture_bible:4.2` responsibility.

### V1-3 — PLPrediction at line 351, LSPrediction at line 390, Prediction at line 428
- Consumed at: § 4.1 (Prediction) + § 4.2 (PLPrediction, LSPrediction)
- Source: `grep -nE "^class (PLPrediction|LSPrediction|Prediction)\b" backend/models/canonical.py` 2026-05-05T18:58Z
- Result: matches META_PLAN v8 verification log line numbers exactly. Re-verification confirms.

### V1-4 — psycopg2 direct connections (NOT RDS Data API)
- Consumed at: § 3.3
- Source A (negative grep — RDS Data API absent): `grep -rn "rds_data\|boto3.*rds-data\|RDSDataService" backend/` 2026-05-05T18:58Z. Result: no matches in production source (one match in vendored layer for psycopg2 string `RDSDataService` is N/A; production-code matches: zero).
- Source B (positive grep — psycopg2 imports present): `grep -rn "import psycopg2" backend/` 2026-05-05T18:58Z. Result:
  - `backend/shared/db.py:5: import psycopg2`
  - `backend/shared/db.py:6: import psycopg2.extras`
  - `backend/database/migrations/migrate.py:9: import psycopg2`
  - (plus matches in bundled Lambda layers `backend/layers/db-dependencies/python/psycopg2/` and `backend/layers/ml-dependencies/python/psycopg2/` — these are vendored psycopg2 itself, expected.)
- Source C (DB connection construction): `backend/shared/db.py:13-37` constructs connection string from Secrets Manager (`DB_SECRET_ARN`) or `DATABASE_URL` env var; `backend/shared/db.py:59` calls `psycopg2.connect(...)`.
- Result: **EE uses psycopg2 direct connections.** Connection mechanism is direct DB-network not RDS Data API.

### V1-5 — Secrets Manager consumer enumeration
- Consumed at: § 3.8
- Source: `grep -rln "2captcha\|brightdata\|BRIGHTDATA\|2CAPTCHA" /home/strakajagr/projects/equine-equalizer/` (excluding `node_modules`, `.git`) 2026-05-05T18:58Z
- Result for **2captcha**: 5 file matches in `equibase_probe/option_b_probe.py` (line 31: `SECRET_ID = "equine-equalizer/2captcha-api-key"`; lines 58, 72, 79, 100: 2captcha API URL references). All matches are in `equibase_probe/` directory (probe scripts; standalone investigation tooling, not part of any deployed Lambda or ECS task image).
- Result for **brightdata**: matches in `equibase_probe/` directory only + documentation files (`docs/bible/_meta/EE_CURRENT_STATE_DUMP.md`, `META_PLAN.md`, etc.). No production-Lambda or ECS-task-image consumers.
- Result for **db-credentials**: consumed at `backend/shared/db.py:13-37` (canonical DB connection module); referenced indirectly via `DB_SECRET_ARN` env var in all 5 Active Lambdas (verified `aws lambda get-function-configuration --function-name equine-inference --query 'Environment.Variables'` shows `DB_SECRET_ARN: arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials-7CD7Mt`).
- Refinement of META_PLAN v8 § 2.3 claim: META_PLAN v8 said "zero consumers" for 2captcha + brightdata. Strict reading: zero **production-Lambda** consumers (correct) + non-zero **probe-script + documentation** consumers (refinement). Architecture Overview § 3.8 documents the refinement explicitly.

### V1-6 — Cross-references to subsequent Phase 1 bibles are forward-looking
- Consumed at: § 1 + § 4.3 + throughout § 3 cross-reference cells
- Source: `ls /home/strakajagr/projects/equine-equalizer/docs/bible/*.md` 2026-05-05T18:58Z
- Result: at lock time of v1, only `architecture_overview.md` (this draft) exists in `/docs/bible/`. The 6 target bibles do not yet exist. Cross-reference syntax follows BIBLE_STRUCTURE_SPEC v6 § 7.1.1 (`<bible-shortname>:<section-id>` form). At Phase-1-lock-of-all-bibles time, all forward-references resolve. Documented as a forward-reference disclaimer in § 4.3 INDEX.
- Status: NON-BLOCKING per BIBLE_STRUCTURE_SPEC v6 § 8.2 sequencing — Architecture Overview drafts FIRST and serves as the navigation hub the subsequent bibles populate.

### V1-7 — ECS Fargate cluster name `equine-cluster` (re-verification)
- Consumed at: § 3.2
- Source: `aws ecs describe-clusters --clusters equine-cluster --query 'clusters[].[clusterName,status]' --output text` 2026-05-05T18:59Z
- Result: `equine-cluster ACTIVE`.

### V1-8 — Named ECR repositories used by EE
- Consumed at: § 3.7
- Source: `aws ecr describe-repositories --query 'repositories[?starts_with(repositoryName, \`equine\`)].[repositoryName,repositoryUri]' --output text` 2026-05-05T18:59Z
- Result: 3 named repositories — `equine-training`, `equine-nyra-workouts`, `equine-equibase-acquisition`. Plus 1 CDK-managed assets repository (separate naming pattern; verified at A.4).

### V1-9 — Lambda memory and timeout configuration
- Consumed at: § 3.1
- Source: `aws lambda get-function-configuration --function-name <each> --query '[FunctionName,MemorySize,Timeout,PackageType]'` 2026-05-05T18:59Z
- Result: All 8 Lambdas are `PackageType = Image`. Memory/timeout per § 3.1 tables. `equine-ingestion` is the largest (2048 MB, 900 s timeout) consistent with its scrape-and-load workload. The 3 inference Lambdas (`equine-{wr,pl,ls}-inference`) and `equine-inference` (dispatcher) each at 1024 MB / 300 s. Smaller Lambdas (`equine-nyra-workouts`, `equine-feature-engineering`, `equine-results`) at 512 MB / 300 s.

### V1-10 — equine-ingestion-daily (ENABLED) targets INACTIVE equine-ingestion Lambda
- Consumed at: § 3.6 anomaly note + § 5.1 Forbidden Pattern candidate + § 6 Currently Open
- Source: `aws events list-targets-by-rule --rule equine-ingestion-daily --query 'Targets[].[Id,Arn]' --output text` 2026-05-05T18:59Z
- Result: `Target0  arn:aws:lambda:us-east-1:584812014683:function:equine-ingestion`. Combined with A.1 result (`equine-ingestion` is INACTIVE) → fire-and-fail pattern confirmed. Same pattern applies to `equine-results-daily` (ENABLED) → `equine-results` (INACTIVE) by symmetric reasoning; not directly re-verified at this lock but inferred from A.1 + A.2 (both rules ENABLED, both target Lambdas INACTIVE).

### V1-11 — RDS instance `equine-db` substantive characteristics (drives A.8 REFUTATION)
- Consumed at: § 3.3
- Source: `aws rds describe-db-instances --db-instance-identifier equine-db --query 'DBInstances[].[DBInstanceIdentifier,DBInstanceArn,Engine,EngineVersion,DBInstanceClass,Endpoint.Address,Endpoint.Port,DBInstanceStatus,DBClusterIdentifier]' --output text` 2026-05-05T18:59Z
- Result: `equine-db arn:aws:rds:us-east-1:584812014683:db:equine-db postgres 16.6 db.t4g.micro equine-db.cgtuh834bttd.us-east-1.rds.amazonaws.com 5432 available None`. `DBClusterIdentifier = None` confirms standalone instance. Endpoint stored in `equine-equalizer/db-credentials` Secrets Manager entry (verified by `aws secretsmanager get-secret-value` → `host: equine-db.cgtuh834bttd.us-east-1.rds.amazonaws.com / engine: postgres / port: 5432 / dbname: equine_equalizer`).

### V1-12 — SNS subscriber count
- Consumed at: § 3.8
- Source: `aws sns list-subscriptions-by-topic --topic-arn arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts --query 'Subscriptions[].[Protocol,Endpoint,SubscriptionArn]' --output text` 2026-05-05T18:59Z
- Result: 1 subscriber: `email tonyragano@gmail.com arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts:02fccc90-97e0-4891-b4f7-068d37ff3eb6`.

**Section B summary:** 12 new V1-N claims documented with full source citation + 2026-05-05 timestamp. All claims grounded in Tier 1 (live AWS state) or Tier 4 (working-tree code post-baseline 87dec36) per META_PLAN v8 § 4.5 source-priority hierarchy.

---

## Section C — Methodology-interpolation self-check

Per META_PLAN v8 § 6.1 + BIBLE_STRUCTURE_SPEC v6 § 12.1 grandfathered constructs list. Drafter audits this draft for net new methodology constructs:

- **Net new methodology constructs introduced in v1 draft: ZERO.**
- **Pattern-completion check trivially satisfied:**
  - No new letter-prefixes (W.N exclusivity preserved per BIBLE_STRUCTURE_SPEC v6 § 5.5.1 + G-new-1 closure).
  - § 5 candidate-roster IDs use numeric sub-section IDs (`5.1`, `5.2`) per G-new-1 closure; no provisional letter-prefixes.
  - § 8 W.N format would be applied only when a § 8 entry is canonical here (none at lock).
  - Cross-reference vocabulary (`<bible>:<section-id>`) follows BIBLE_STRUCTURE_SPEC v6 § 7.1.1; no new vocabulary introduced.
- **Candidate Discipline rules surfaced (§ 5.1 + § 5.2) are NOT new methodology constructs.** They are substrate-grounded surfaces of pre-existing methodology (META_PLAN v8 § 4.5 source-priority discipline + § 6.5 verification-log precision rule). Per § 5.7 convergence rule, candidate roster awaits QB ratification before becoming part of the bible's discipline rule set.

Grandfathering clause confirmed operative: pre-existing methodology constructs from META_PLAN v8 + BIBLE_STRUCTURE_SPEC v6 (e.g., source-priority hierarchy, W.N convention, decomposition discipline, FRAMEWORK_GAP / SPEC_GAP markers, no-fabrication rule, cross-reference syntax) are inherited; CC introduced none.

---

## Section D — Pattern-completion check

Per AUDIT_METHODOLOGY v2 § 5.5.

- **Letter-prefix exclusivity preserved.** W.N is the only letter-prefix used in BIBLE_STRUCTURE_SPEC-prescribed structure (§ 8 What Was Fixed entries). No § 8 entries at lock; no W.N entries introduced.
- **§ 5 candidate-roster numeric IDs.** § 5.1 + § 5.2 use numeric sub-section IDs per G-new-1 closure. No provisional letter-prefixes (e.g., `5.A`, `5.B`) introduced.
- **§ 8 W.N format preserved.** If § 8 entries were introduced (none at lock), they would follow `8.W.<n>` format with mandatory Fix date YYYY-MM-DD per BIBLE_STRUCTURE_SPEC v6 § 5.6.1 + § 5.6.1.2.
- **Decomposition discipline applied.** "8 Lambdas = 5 Active + 3 INACTIVE" (§ 3.1), "13 EventBridge rules = 10 ENABLED + 3 DISABLED" (§ 3.6), "5 ECS task families enumerated by name" (§ 3.2), "4 S3 buckets enumerated by name" (§ 3.4), "3 Secrets enumerated by name" (§ 3.8), "5 ECR images in CDK-managed assets repository (separate from 3 named ECR repositories)" (§ 3.7). Counts decomposed where applicable per META_PLAN v8 § 6.5 verification-log precision rule.
- **G-new-2 inheritance pattern applied (not adopted as-is).** G-new-2 (database_schema_bible-specific: § 4.1 enumerates `CREATE TABLE` declarations only, matviews documented at § 3 only) does not apply directly to Architecture Overview (which doesn't enumerate tables or matviews). Inheritance pattern honored: each enumerated structural set names its scope explicitly (e.g., § 3.7 distinguishes "named ECR repositories" from "CDK-managed assets repository"; § 3.1 distinguishes Active vs Inactive). No subsetting drift.

Pattern-completion check **PASS**.

---

## Section E — FRAMEWORK_GAP / SPEC_GAP markers

Drafter surfaces 2 FRAMEWORK_GAP markers in v1 draft. Zero SPEC_GAP markers (the spec's overall premise — that EE has the runtime contexts it has — is intact; only specific-slot mismatches surface as FRAMEWORK_GAPs).

### E.1 FRAMEWORK_GAP — § 3.3 Aurora-vs-standalone-Postgres
- **Marker location:** § 3.3 of `architecture_overview.md`.
- **Explanation:** BIBLE_STRUCTURE_SPEC v6 § 6.1 + drafting spec § 3.3 nominally label this slot "Aurora Serverless cluster" with cluster ARN inherited from META_PLAN v8 verification log (`arn:aws:rds:us-east-1:584812014683:cluster:equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`). Live AWS verification 2026-05-05 (`aws rds describe-db-clusters --db-cluster-identifier equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`) returns `DBClusterNotFoundFault`. The EE database is a **standalone RDS PostgreSQL 16.6 instance** (`equine-db`, db.t4g.micro), not an Aurora cluster. Per META_PLAN v8 § 4.5 source-priority, Tier 1 (live AWS state) governs over Tier 6 (inherited dump-derived claim).
- **Drafter's fill-what-fits behavior:** § 3.3 retitled "RDS PostgreSQL instance (`equine-db`)" reflecting actual substrate. Section content documents the standalone instance characteristics (engine, version, instance class, endpoint, db-name, status). Cross-reference to `database_schema_bible:3` for table inventory preserved (the database-content cross-reference is engine-agnostic).
- **Request to QB:** ratify the override + retroactively correct META_PLAN v8 verification log entry for "Aurora cluster ARN" claim. Source of inherited error is likely `EE_CURRENT_STATE_DUMP.md` (Tier 6 has been wrong about multiple facts per META_PLAN v8 § 4.5 caveat). Recommended retroactive-correction action: update META_PLAN v8 verification log to mark the Aurora claim REFUTED and replace with the V1-11 standalone-Postgres claim from this verification log.

### E.2 FRAMEWORK_GAP — § 4.2 WRPrediction class absence
- **Marker location:** § 4.2 of `architecture_overview.md`.
- **Explanation:** Drafting spec § 4.2 mandates documentation of **3 per-pipeline prediction shapes (WRPrediction / PLPrediction / LSPrediction)**. Live verification 2026-05-05 (`grep -nE "^class WRPrediction" backend/models/canonical.py`) returns zero matches / exit code 1. Only PLPrediction (line 351) and LSPrediction (line 390) exist as per-pipeline classes. The base `Prediction` class (line 428) exists. WRPrediction is absent.
- **Drafter's fill-what-fits behavior:** § 4.2 documents 2 per-pipeline shapes (PLPrediction, LSPrediction) honestly per META_PLAN v8 § 8.6 no-fabrication discipline. Drafter does NOT invent WRPrediction. § 4.2 explicitly notes the absence and surfaces architectural-dissonance hypothesis: WR pipeline (`equine-wr-inference` Lambda) currently appears to use base `Prediction` class or constructs DB row shape inline; substantive investigation deferred to `ml_layer_architecture_bible:4.2`.
- **Request to QB:** triage among three resolutions:
  1. **Canonicalize-WRPrediction** Phase 5 work — adds `WRPrediction` class to `backend/models/canonical.py` for symmetry with PL/LS; touches `equine-wr-inference` Lambda + `wr_predictions` table consumer code.
  2. **Document-WR-uses-base-Prediction-and-update-spec** — drafting spec corrected to state "2 per-pipeline shapes (PL, LS) + WR uses base `Prediction`"; no code change.
  3. **Phase-5-architectural-cleanup-with-WR-shape-decision-deferred** — disposition deferred to `ml_layer_architecture_bible:4.2` drafting cycle (which has fuller WR pipeline visibility); v1 of Architecture Overview locks with the FRAMEWORK_GAP unresolved but documented.
- Drafter recommends option 2 or 3 for v1 lock; option 1 is substantive code work outside Phase 1 scope.

---

## Verification log claim count summary

- **Section A inherited claims re-verified:** 11 (10 CONFIRMED, 1 REFUTED — A.8 Aurora cluster).
- **Section B new V1-N claims documented:** 12.
- **Section C net new methodology constructs:** 0.
- **Section D pattern-completion check:** PASS.
- **Section E FRAMEWORK_GAP / SPEC_GAP markers:** 2 FRAMEWORK_GAP (E.1 Aurora-vs-Postgres, E.2 WRPrediction absence). 0 SPEC_GAP.
- **Total verifiable substantive claims:** 23.
