# OCRC D1 — Resource Inventory

**Cycle ID:** OCRC_2026-05-09
**Cycle Class:** Operational Catastrophe Recovery Cycle (first instantiation)
**Deliverable:** D1 — Resource Enumeration Pass with 4-source triangulation + classification taxonomy + HRN workouts producer hunt + substrate verification at first reference
**Status:** DRAFT — S1 drafting CC output; S2 audit CC pending dispatch (fresh-conversation-per-session per OCR-Q5)
**Methodology:** AUDIT_METHODOLOGY v3 (locked 2026-05-08) + OCRC handoff (ratified 2026-05-09)
**Drafted-by:** S1 drafting CC, OCRC dispatch sequence S1
**Lock time of substrate reads:** 2026-05-09 UTC (AWS API responses tagged VERIFIED-at-S1)
**Tony SP-gate ratification:** 2026-05-09 (V1–V8 + R1–R7 + Q1–Q5 + OCRC scope expansion D9 + D10)

**Forward-reference index:**
- D2 (cron-payload audit) — disambiguates V6 InputTransformer drift; inspects backend/lambdas/ingestion/handler.py for `USE_TODAY_MINUS_1` sentinel interpretation; post-restoration CloudWatch log analysis for equine-fetch-results-nightly firings since 2026-05-09 04:37 UTC
- D4 (equine-results + equine-feature-engineering restoration) — closes 5.3.17 fully; inherits ECR existence verification residual from OCRC D1 V2/V3
- D7 (closure proposals + new defect formalization) — formalizes C1 PARTIAL / C2 / C3 closures + assigns concrete Phase 5.3.N+ numbering for the 15 candidates surfaced here
- D9 (CloudWatch alarms deployment) — closes 5.3.N+11 alarms-gap upon completion; 2-tier; sequenced after D5
- D10 (equine-fetch-results-nightly Input fix) — surgical EventBridge rule edit OR handler default-date logic change per D2 disambiguation; 3-tier; sequenced after D2

---

## 1. Substrate Verification Confirmations (V1–V8)

V1–V8 ratified at SP gate 2026-05-09. Re-confirmed at S1 via expanded enumeration substrate; no drift from ratified report. Summary:

| Item | Inherited claim | Ground truth at S1 | Drift |
|---|---|---|---|
| V1 | equine-ingestion Active 2026-05-09 ~04:37 UTC | State=Active, LastModified=2026-05-09T04:37:39 UTC, LastUpdateStatus=Successful, ImageUri=…cdk-hnb659fds-…:1ac0a1893ba3… | CONFIRMED |
| V2 | equine-results INACTIVE; ECR image restored as CDK side-effect; awaits update-function-code | State=Inactive, StateReason="The function is trying to use a deleted image.", LastModified=2026-05-02T15:45:11 UTC, ImageUri=…:9f2ce334… | CONFIRMED on State + needs update-function-code; **residual** ECR existence verification of SHA `9f2ce334…` deferred to D4 |
| V3 | equine-feature-engineering INACTIVE; same disposition as V2 | Same pattern; ImageUri=…:2d12b9cd… | CONFIRMED + same residual deferred to D4 |
| V4 | 5 Active Lambdas (equine-nyra-workouts + equine-pl-inference + equine-wr-inference + equine-ls-inference + equine-inference) | All 5 Active; 4 share LastModified 2026-05-02T15:45:10–11 UTC (cohort redeploy); equine-nyra-workouts LastModified 2026-04-27T22:11 with custom ECR repo `equine-nyra-workouts:v1-1777327653` | CONFIRMED |
| V5 | architecture_overview § 3.6: 13 / 10 ENABLED / 3 DISABLED. Phase A D1 § 1.3: 12 / 10 ENABLED / 2 DISABLED (with 3 DISABLED named) | 13 rules / 10 ENABLED / 3 DISABLED (matches architecture_overview byte-for-byte on per-rule State + cron expressions) | architecture_overview CONFIRMED. Phase A D1 § 1.3 SUBSTRATE-CORRECT-CLAIM-WRONG (internal counting typo: narrative names 3 DISABLED but totals 2). Phase A D1 frozen per OCRC handoff § 2.1 — no retroactive correction. |
| V6 | OCRC handoff § 2.4 / CC Step 4 report: "Input=null routes to fetch_daily_entries(today) instead of fetch_results(yesterday)"; architecture_overview § 3.6: "No Input override" | InputTransformer present with InputPathsMap `{"time":"$.time"}` + InputTemplate `{"action":"fetch_results","date":"USE_TODAY_MINUS_1"}` | **MATERIAL DRIFT** — both inherited claims wrong against ground truth. Disposition: deferred to D2 cron-payload audit per Tony Q5 ratification 2026-05-09; surgical fix is D10 territory. See § 2.3 V6 priority-finding block below. |
| V7 | PHASE_5_BACKLOG 27 entries (5.3.1 through 5.3.27) | 27 entries verified; identifier sequence monotonic with no gaps; vocabulary uniformity per § 8.4 confirmed (HIGH/MEDIUM/LOW per TRIAGE_QUEUE_SPEC v1; Phase 5.3.1 carries historical META_PLAN v6 § 11 vocabulary preserved per § 4.17) | CONFIRMED |
| V8 | 7 Phase 1 bibles LOCKED + AUDIT_METHODOLOGY v3 LOCKED + META_PLAN v9 + BIBLE_STRUCTURE_SPEC v6 LOCKED + cross-bible cross-reference freeze ACTIVE + CONVERGENCE_CRITERIA v2 + TRIAGE_QUEUE_SPEC v1 DRAFT pre-audit | All 12 artifacts' Status fields verbatim-confirmed; cross-bible cross-reference freeze ACTIVE per api_frontend_bible.md v1 LOCKED 2026-05-08 attestation | CONFIRMED |

---

## 2. Resource Enumeration (E1–E4 with Classification Taxonomy)

**Classification legend.** ACTIVE = present in AWS (E1) + declared in CDK (E3) + supported by repo code (E4); ORPHAN = present in AWS (E1) but not in CDK (E3); CDK-DRIFT-AURORA = CDK source diverges from live AWS state; DEPRECATED-candidate = present somewhere but disposition is to remove per bible/code; DEAD = repo only (not in AWS). Sources of evidence per resource: E1 (AWS API), E2 (CloudFormation), E3 (CDK source `infrastructure/cdk/lib/`), E4 (repository code).

**Substrate-verification-methodology-warning:** S2 audit re-enumeration observed CFN resource counts of 138/35/4/8 across the 4 Equine* stacks (EquineComputeStack/EquineDatabaseStack/EquineStorageStack/EquineFrontendStack respectively) vs S1 enumeration 143/33/3/8. Counts are derivable from per-resource tables in subsections § 2.1 onward by tallying CFN logical IDs; artifact does not document explicit aggregate counts. Probable cause of discrepancy: enumeration methodology difference (CDKMetadata + Permissions counted differently between S1 and S2 re-enumeration approaches). Counts are not classification-bearing; classification taxonomy unaffected. Documented as warning, not patched, per Tony Decision 1 ratification 2026-05-09.

### 2.1 Compute — Lambdas (8 functions)

| Lambda | E1 (state, ImageUri repo) | E2 (CFN logical ID) | E3 (CDK declaration) | E4 (handler) | Class |
|---|---|---|---|---|---|
| equine-ingestion | Active; cdk-hnb659fds-…:1ac0a1893ba3… | EquineComputeStack/IngestionFunction3919F32A | compute-stack.ts:82 | backend/lambdas/ingestion/handler.py | ACTIVE |
| equine-feature-engineering | Inactive (deleted-image); cdk-hnb659fds-…:2d12b9cd… | EquineComputeStack/FeatureEngineeringFunctionF0DBF8F0 | compute-stack.ts:101 | backend/lambdas/feature-engineering/handler.py | ACTIVE (Inactive State; CDK-current; D4 restoration pending) |
| equine-inference | Active; cdk-hnb659fds-…:6954a22a… | EquineComputeStack/InferenceFunction179229EB | compute-stack.ts:119 | backend/lambdas/inference/handler.py | ACTIVE |
| equine-results | Inactive (deleted-image); cdk-hnb659fds-…:9f2ce334… | EquineComputeStack/ResultsFunctionEC5CB6A5 | compute-stack.ts:137 | backend/lambdas/results/handler.py | ACTIVE (Inactive State; CDK-current; D4 restoration pending) |
| equine-wr-inference | Active; cdk-hnb659fds-…:f89865ae… | EquineComputeStack/WRInferenceFunctionEDB66B65 | compute-stack.ts:153 | backend/lambdas/wr-inference/handler.py | ACTIVE |
| equine-pl-inference | Active; cdk-hnb659fds-…:cca88c50… | EquineComputeStack/PLInferenceFunctionD15A7DB1 | compute-stack.ts:168 | backend/lambdas/pl-inference/handler.py | ACTIVE |
| equine-ls-inference | Active; cdk-hnb659fds-…:b3c8ab1d… | EquineComputeStack/LSInferenceFunction65ADF816 | compute-stack.ts:183 | backend/lambdas/ls-inference/handler.py | ACTIVE |
| **equine-nyra-workouts** | Active; **equine-nyra-workouts:v1-1777327653** (custom ECR repo, NOT cdk assets) | **NOT in any equine stack** | **NOT in CDK** | backend/lambdas/nyra-workouts/handler.py + Dockerfile.nyra-workouts | **ORPHAN** — see 5.3.N+7 |

Closure candidate flag: equine-ingestion → C1 PARTIAL (5.3.17); equine-results + equine-feature-engineering → C1 deferred to D4.

### 2.2 Compute — ECS

**Cluster + task families:**

| Resource | E1 | E2 | E3 | E4 | Class |
|---|---|---|---|---|---|
| equine-cluster (ECS) | ACTIVE | EquineComputeStack/EquineClusterC76AB066 | compute-stack.ts:348 | — | ACTIVE |
| equine-training task family (rev :49 + :106) | ACTIVE | EquineComputeStack/TrainingTaskDefA6142A22 = arn:…/equine-training:106 | compute-stack.ts:353 (`family: 'equine-training'`) | Dockerfile.training + model/ | ACTIVE |
| **equine-training-daily-full** (8 revisions: :1–:8) | ACTIVE; 8 registered revisions | NOT in CFN | NOT in CDK | not referenced in repo | **ORPHAN** — production-active (cited by ENABLED rule equine-daily-retrain-full) — see 5.3.N+6 |
| **equine-training-pl** (3 revisions) | ACTIVE | NOT in CFN | NOT in CDK | not referenced | **ORPHAN** — see 5.3.N+6 |
| **equine-training-win-prob** (3 revisions) | ACTIVE | NOT in CFN | NOT in CDK | not referenced | **ORPHAN** — production-active (cited by ENABLED rule equine-weekly-retrain-wr) — see 5.3.N+6 |
| **equine-training-manual** (1 revision) | ACTIVE | NOT in CFN | NOT in CDK | not referenced | **ORPHAN** — manual-invoke only — see 5.3.N+6 |
| **equibase-probe** + 3 variants (8 revisions total: equibase-probe:1–4, equibase-probe-optiona2:1–2, equibase-probe-optionb:1, equibase-probe-optiond:1–2) | ACTIVE registrations | NOT in CFN | NOT in CDK | equibase_probe/Dockerfile* (4) + 4 probe-script files | **DEPRECATED-candidate** — zero production consumers; bible § 4.2.6 cohort — see 5.3.N+8 |

**ECS services in equine-cluster:** 0 services. **ECS tasks RUNNING/STOPPED:** 0 within 1h retention.

### 2.3 Compute — EventBridge rules (13 rules)

#### CDK-declared rules (7)

| Rule | E1 (State, cron) | E2 (CFN) | E3 (CDK) | E4 (handler) | Class |
|---|---|---|---|---|---|
| equine-ingestion-daily | ENABLED, cron(0 11 * * ? *) | EquineComputeStack/IngestionSchedule30858612 | compute-stack.ts:258 | ingestion handler default-case dispatch | ACTIVE |
| equine-feature-engineering-daily | DISABLED (0 targets), cron(0 12 * * ? *) | EquineComputeStack/FeatureEngineeringSchedule7F539069 | compute-stack.ts:273 (`enabled: false` with note) | feature-engineering handler | ACTIVE-DISABLED-by-design |
| equine-inference-daily | DISABLED (0 targets), cron(30 12 * * ? *) | EquineComputeStack/InferenceSchedule5C041DFE | compute-stack.ts:293 (`enabled: false` with note) | inference handler | ACTIVE-DISABLED-by-design |
| equine-wr-inference-daily | ENABLED, cron(30 12 * * ? *) | EquineComputeStack/WRInferenceSchedule6200FA2D | compute-stack.ts:304 | wr-inference handler | ACTIVE |
| equine-pl-inference-daily | ENABLED, cron(35 12 * * ? *) | EquineComputeStack/PLInferenceSchedule475AC520 | compute-stack.ts:314 | pl-inference handler | ACTIVE |
| equine-ls-inference-daily | ENABLED, cron(40 12 * * ? *) | EquineComputeStack/LSInferenceScheduleF6FF3A6B | compute-stack.ts:324 | ls-inference handler | ACTIVE |
| equine-results-daily | ENABLED, cron(0 4 * * ? *) | EquineComputeStack/ResultsScheduleD05923C4 | compute-stack.ts:334 | results handler | ACTIVE |

#### Out-of-band rules (6)

| Rule | E1 (State, cron, target) | E2 | E3 | Class |
|---|---|---|---|---|
| **equine-angle-stats-nightly** | ENABLED, cron(15 2 * * ? *), Lambda equine-ingestion, Input=`{"action":"refresh_angle_stats"}` | NOT in CFN | NOT in CDK | ORPHAN — see 5.3.N+5 |
| **equine-fetch-results-nightly** | ENABLED, cron(30 1 * * ? *), Lambda equine-ingestion, **InputTransformer (see V6 priority-finding block below)** | NOT in CFN | NOT in CDK | ORPHAN + V6 priority finding — see 5.3.N+5 + D10 |
| **equine-nyra-workouts-daily** | ENABLED, cron(0 10 * * ? *), Lambda equine-nyra-workouts, Input=`{}` | NOT in CFN | NOT in CDK | ORPHAN — paired with orphan Lambda — see 5.3.N+5 |
| **equine-daily-retrain-full** | ENABLED, cron(30 2 * * ? *), ECS task family equine-training-daily-full (RoleArn: equine-events-ecs-role) | NOT in CFN | NOT in CDK | ORPHAN — drives daily retrain via orphan task family — see 5.3.N+5 |
| **equine-weekly-retrain-wr** | ENABLED, cron(0 4 ? * MON *), ECS task family equine-training-win-prob | NOT in CFN | NOT in CDK | ORPHAN — drives weekly WR retrain — see 5.3.N+5 |
| **equine-weekly-retrain-pl** | DISABLED, cron(0 5 ? * MON *), ECS task family equine-training-pl | NOT in CFN | NOT in CDK | ORPHAN — currently dormant — see 5.3.N+5 |

#### V6 priority-finding block — equine-fetch-results-nightly InputTransformer drift

Per Tony Q5 ratification 2026-05-09: explicit InputTransformer JSON dump + drift-status flag + forward-reference to D2 disambiguation + forward-reference to OCRC D10 scope expansion.

**Ground truth (verified at S1 2026-05-09):**

```json
{
  "Targets": [{
    "Id": "fetch-results",
    "Arn": "arn:aws:lambda:us-east-1:584812014683:function:equine-ingestion",
    "InputTransformer": {
      "InputPathsMap": { "time": "$.time" },
      "InputTemplate": "{\"action\":\"fetch_results\",\"date\":\"USE_TODAY_MINUS_1\"}"
    }
  }]
}
```

**Drift status:** MATERIAL DRIFT against two inherited claims:
1. OCRC handoff § 2.4 (sourced from CC Step 4 report; tagged VERIFIED-this-session): "Input=null routes to fetch_daily_entries(today) instead of fetch_results(yesterday)" — wrong (Input is NOT null; routes to action=fetch_results with sentinel `USE_TODAY_MINUS_1`).
2. architecture_overview v3-patched-a § 3.6: "No `Input` override" — wrong.

**Substrate-correct facts:**
- action = `fetch_results` (NOT default-case dispatch)
- date = literal string `USE_TODAY_MINUS_1` (EventBridge passes verbatim; no built-in date arithmetic — sentinel must be interpreted handler-side)
- InputPathsMap `{"time":"$.time"}` is dead (no `<time>` placeholder appears in InputTemplate; harmless residue)

**Three drift hypotheses (cannot disambiguate at S1):**
- (a) Recent change between architecture_overview lock (2026-05-08) and S1 (2026-05-09); possibly added by Phase A informal recovery work
- (b) Bible staleness — InputTransformer existed at 2026-05-08 and architecture_overview missed it
- (c) Inheritance error — CC Step 4 report observed Input=null at a moment when InputTransformer was absent; subsequent addition

**D2 disambiguation scope (forward-reference):** D2 cron-payload audit will resolve via:
- CloudTrail UpdateRule lookup for the InputTransformer addition timestamp + principal
- Handler code inspection at backend/lambdas/ingestion/handler.py for `USE_TODAY_MINUS_1` sentinel interpretation
- Post-restoration CloudWatch log analysis for equine-fetch-results-nightly firings since 2026-05-09 04:37 UTC (i.e., the 01:30 UTC firing on 2026-05-10 should produce the first observable post-restoration log entry)

**D10 scope (forward-reference):** Surgical fix path chosen at D10 drafting CC per D2 disambiguation. Candidate paths:
- Path A: EventBridge rule edit — replace `USE_TODAY_MINUS_1` literal with EventBridge expression (NB: EventBridge does not support date arithmetic in InputTransformer; this path requires a different mechanism)
- Path B: Handler default-date logic change — interpret `USE_TODAY_MINUS_1` as sentinel for `(date.today() - timedelta(days=1))`
- Path C: Both (rule edit + handler logic update for defensive parsing)

D10 = 3-tier ceremony (drafting + audit + lock), sequenced after D2 cron-payload audit lands.

**Provenance:** Inherited claim sourced from prior CC Step 4 report (referenced in OCRC handoff § 2.4 + § 7); ground-truth substrate at S1 captured 2026-05-09. Phase A D1 frozen per OCRC handoff § 2.1 — no retroactive correction.

### 2.4 Identity — IAM roles (14 equine-related)

| Role | E1 | E2 | Class |
|---|---|---|---|
| EquineComputeStack-IngestionFunctionServiceRoleBEA1-XH5nDS6UEvc3 | ACTIVE | EquineComputeStack/IngestionFunctionServiceRoleBEA1F260 | ACTIVE |
| EquineComputeStack-FeatureEngineeringFunctionServic-4OUmSGzKiPj3 | ACTIVE | EquineComputeStack/FeatureEngineeringFunctionServiceRoleB2747CEE | ACTIVE |
| EquineComputeStack-InferenceFunctionServiceRoleF565-TAhSSfozmLIs | ACTIVE | EquineComputeStack/InferenceFunctionServiceRoleF5654FD2 | ACTIVE |
| EquineComputeStack-ResultsFunctionServiceRoleD637EE-oHseSEGvKf3M | ACTIVE | EquineComputeStack/ResultsFunctionServiceRoleD637EE07 | ACTIVE |
| EquineComputeStack-WRInferenceFunctionServiceRole50-3h7rtE6J9Zwg | ACTIVE | EquineComputeStack/WRInferenceFunctionServiceRole50D13D15 | ACTIVE |
| EquineComputeStack-PLInferenceFunctionServiceRoleE9-AicisfzONYB9 | ACTIVE | EquineComputeStack/PLInferenceFunctionServiceRoleE9A41CE3 | ACTIVE |
| EquineComputeStack-LSInferenceFunctionServiceRoleAC-ogxzjOvAqKNG | ACTIVE | EquineComputeStack/LSInferenceFunctionServiceRoleAC72614A | ACTIVE |
| EquineComputeStack-TrainingTaskDefExecutionRoleFBAB-mKlgVT6egYqA | ACTIVE | EquineComputeStack/TrainingTaskDefExecutionRoleFBAB754F | ACTIVE (training execution role for `equine-training` task family) |
| EquineComputeStack-TrainingTaskDefTaskRoleAE236559-mn4wUZ6A6zTi | ACTIVE | EquineComputeStack/TrainingTaskDefTaskRoleAE236559 | ACTIVE (training task role for `equine-training` task family) |
| EquineDatabaseStack-CustomVpcRestrictDefaultSGCusto-xMaK9TFuSWm8 | ACTIVE | EquineDatabaseStack (CDK custom resource) | ACTIVE |
| EquineFrontendStack-CustomS3AutoDeleteObjectsCustom-FmFm6gvMixWe | ACTIVE | EquineFrontendStack (CDK custom resource) | ACTIVE |
| **equine-events-ecs-role** | ACTIVE; used by EventBridge → ECS task targets per E1 list-targets RoleArn (equine-daily-retrain-full / equine-weekly-retrain-pl / equine-weekly-retrain-wr) | NOT in CFN | **ORPHAN** — see 5.3.N+14 |
| **equine-nyra-workouts-role** | ACTIVE; used by orphan Lambda equine-nyra-workouts | NOT in CFN | **ORPHAN** — see 5.3.N+14 |
| **equine-training-task-role** | ACTIVE; purpose unverified (not used by any deployed Lambda; candidate consumer = orphan ECS task families' override task role) | NOT in CFN | **ORPHAN** — see 5.3.N+14 |

### 2.5 Storage — S3 buckets (4)

| Bucket | E1 | E2 | E3 | Class |
|---|---|---|---|---|
| equine-frontend | ACTIVE | EquineFrontendStack/FrontendBucketEFE2E19C | frontend-stack.ts:20 | ACTIVE |
| equine-model-artifacts | ACTIVE | EquineStorageStack/ModelArtifactsBucket80ACAD84 | storage-stack.ts:40 | ACTIVE |
| equine-processed-data | ACTIVE | EquineStorageStack/ProcessedDataBucket4E25D3B7 | storage-stack.ts:32 | ACTIVE |
| equine-raw-data | ACTIVE | EquineStorageStack/RawDataBucket57F26C03 | storage-stack.ts:14 | ACTIVE (writes by ingestion + producer-identified for workout-loads/ — see § 3) |

### 2.6 Database — RDS

| Resource | E1 | E2 | E3 | Class |
|---|---|---|---|---|
| RDS database `equine-db` | Per architecture_overview v3-patched-a § 3.3: standalone instance with `DBClusterIdentifier: None`; Engine postgres 16.6; not part of an RDS cluster | EquineDatabaseStack/EquineDatabase648A3917 (`AWS::RDS::DBCluster`) + EquineDatabaseStack/EquineDatabaseWriterF01B062C (`AWS::RDS::DBInstance`) | database-stack.ts:52 declares `rds.DatabaseCluster` Aurora | **CDK-DRIFT-AURORA** — CDK source + CFN both declare cluster; live AWS state per architecture_overview reports standalone instance. Cluster apparently deleted out-of-band; CFN drift not reconciled. Documented in architecture_overview as REFUTED Aurora claim 2026-05-05. — see 5.3.N+15 |
| equine-equalizer/db-credentials (Secret) | ACTIVE; consumed by 7 Lambda service roles + training task role | EquineDatabaseStack/EquineDatabaseStackEquineDatabaseSecretB140275E… | database-stack.ts:57 | ACTIVE |

### 2.7 Container registries — ECR

| Repo | E1 | E2 | E3 | Class |
|---|---|---|---|---|
| cdk-hnb659fds-container-assets-584812014683-us-east-1 | ACTIVE; immutable; CDK-managed | bootstrap (CDKToolkit stack) | implicit via `lambda.DockerImageCode.fromImageAsset` + `ecs.ContainerImage.fromAsset` | ACTIVE |
| **equine-training** (custom; created 2026-03-19) | ACTIVE registration; mutable | NOT in equine stacks | NOT in CDK (CDK uses `fromAsset` → CDK assets repo, not this custom repo) | **ORPHAN** — zero production consumers traced via E1 + repo grep — see 5.3.N+10 |
| **equine-nyra-workouts** (custom; created 2026-04-27) | ACTIVE; mutable; consumed by orphan Lambda equine-nyra-workouts (ImageUri tag `v1-1777327653`) | NOT in CFN | NOT in CDK | **ORPHAN** — paired with 5.3.N+7 |
| **equine-equibase-acquisition** (custom; created 2026-04-27; 10 images all 2026-04-27) | ACTIVE registration; mutable | NOT in CFN | NOT in CDK | **DEPRECATED-candidate** — zero production consumers per architecture_overview § 3.7; verified at S1 via grep returning 0 matches in backend/ + infrastructure/ + scripts/ — see 5.3.N+9 |

### 2.8 Logs — CloudWatch log groups

| Log group | E1 | E2 | E3 | Class |
|---|---|---|---|---|
| /aws/lambda/equine-ingestion | ACTIVE; 30-day retention; 108518 bytes stored | EquineComputeStack/IngestionFunctionLogGroup435CD50B | implicit via Lambda declaration | ACTIVE |
| /aws/lambda/equine-feature-engineering | ACTIVE; 30-day retention; 1203 bytes | EquineComputeStack/FeatureEngineeringFunctionLogGroup41531B96 | implicit | ACTIVE |
| /aws/lambda/equine-inference | ACTIVE; 30-day; 119711 bytes | EquineComputeStack/InferenceFunctionLogGroupF2643D81 | implicit | ACTIVE |
| /aws/lambda/equine-results | ACTIVE; 30-day; 12175 bytes | EquineComputeStack/ResultsFunctionLogGroup306921EA | implicit | ACTIVE |
| /aws/lambda/equine-wr-inference | ACTIVE; 30-day; 853978 bytes | EquineComputeStack/WRInferenceFunctionLogGroupA76BCECA | implicit | ACTIVE |
| /aws/lambda/equine-pl-inference | ACTIVE; 30-day; 356614 bytes | EquineComputeStack/PLInferenceFunctionLogGroup493CEFB5 | implicit | ACTIVE |
| /aws/lambda/equine-ls-inference | ACTIVE; 30-day; 830285 bytes | EquineComputeStack/LSInferenceFunctionLogGroup3203B0A8 | implicit | ACTIVE |
| **/aws/lambda/equine-nyra-workouts** | ACTIVE; **null retention (default = never expire)**; 49801 bytes | NOT in CFN | NOT in CDK | **ORPHAN** — paired with orphan Lambda |
| /ecs/equine-training | ACTIVE; 14-day retention | EquineComputeStack/TrainingLogGroupC4813E5E | compute-stack.ts:369 | ACTIVE |

### 2.9 Messaging + Alerting

| Resource | E1 | E2 | E3 | Class |
|---|---|---|---|---|
| **SNS topic equine-equalizer-alerts** | ACTIVE; 1 email subscription (tonyragano@gmail.com) | NOT in CFN | NOT in CDK | **ORPHAN** — out-of-band — see 5.3.N+13 |
| **CloudWatch metric alarms (equine-tagged)** | **0 alarms** | — | — | **MISSING** — no operational health monitoring on any of: 8 Lambdas, 13 EventBridge rules, ECS cluster, ECS task families, RDS database. SNS topic exists but has no producer. — see 5.3.N+11 |
| CloudWatch composite alarms (equine) | 0 | — | — | MISSING |

**D9 forward-reference (OCRC scope expansion ratification 2026-05-09):** D9 deploys CloudWatch alarms for all 8 equine Lambdas (Errors + Throttles + IteratorAge as applicable) plus a cron-firing alarm on equine-fetch-results-nightly post-D10 Input fix. 2-tier ceremony, sequenced after D5 NYRA cron timing fix lands. D9 closes 5.3.N+11.

### 2.10 Other Secrets

| Secret | E1 | E2 | E3 | Class |
|---|---|---|---|---|
| equine-equalizer/2captcha-api-key | ACTIVE; last-changed 2026-04-27; production-Lambda consumer count = 0 (verified via repo grep + IAM analysis) | NOT in CFN | NOT in CDK | **ORPHAN + DEPRECATED-candidate** — Phase 5.3.18 entry; consumed only by equibase_probe/option_b_probe.py:31 |
| equine-equalizer/brightdata-api-key | ACTIVE; last-changed 2026-04-27; production-Lambda consumer count = 0 | NOT in CFN | NOT in CDK | **ORPHAN + DEPRECATED-candidate** — Phase 5.3.18 entry; consumed only by equibase_probe/ |

### 2.11 Repo-only / DEPRECATED-candidate cohort

- `model/` directory (14 ML pipeline subdirs: angles, artifacts, ensemble, evaluation, features, longshot, ls, pl, ranker, shared, training, trajectory, win_prob, wr): consumed by ECS training task `equine-training:106` via Dockerfile.training. **ACTIVE-by-consumption.**
- `scripts/` (22 entries; diagnostic/training/admin scripts): no production runtime; manual-invoke local execution. **ACTIVE-by-discretion** (not DEAD; not in AWS substrate).
- `equibase_probe/` (4 Dockerfiles + 4 probe-script files): paired with the 4 orphan ECS task families + 2captcha + brightdata secrets + equine-equibase-acquisition ECR repo. **DEPRECATED-candidate-cohort** — see 5.3.N+8 + 5.3.N+9.
- `Dockerfile.feature-engineering` + `backend/lambdas/feature-engineering/Dockerfile`: code path correct; Lambda is currently INACTIVE pending D4 restoration; not DEAD.

---

## 3. HRN Workouts Producer Hunt — CLOSED (Q3 ratification 2026-05-09)

**Disposition: H3a IDENTIFIED.** Tony self-attestation 2026-05-09 collapses the prior H3b NARROWED finding to H3a IDENTIFIED.

**Producer:** Tony local machine scheduled job with assumed-role credentials for equine-ingestion role.

**Closing-evidence:**

```
closed-by: OCRC D1 R4 producer hunt + Tony self-attestation 2026-05-09
verification: producer = Tony local machine scheduled job with assumed-role
              credentials; consistent with continuation-during-Lambda-Inactive-window
              evidence (workout-loads files at ~07:00 UTC daily through 2026-05-02 →
              2026-05-09 fire-and-fail window when equine-ingestion Lambda was
              INACTIVE; ruling out Lambda-as-producer); consistent with
              CloudTrail Event History paired AssumeRole events at ~07:01 UTC daily
              with User=null Source=sts.amazonaws.com (consistent with
              external-principal assume-role pattern)
ratified-by: [Tony pending; D7 drafting CC formalizes per P-Q3 individual ratification]
```

**Severity:** LOW (downgraded from MEDIUM per Tony Q3 ratification).

**Bridging note:** Producer is documented out-of-band substrate. Migration-to-in-cohort-IaC OR explicit-acceptance disposition deferred to future CDK reconciliation cycle (separate cycle post-OCRC + post-Phase-A; aligns with 5.3.N+5 / 5.3.N+6 / 5.3.N+7 / 5.3.N+10 / 5.3.N+13 / 5.3.N+14 cohort which collectively constitute the CDK-source-vs-live-AWS-state drift surface).

**Supporting substrate recap (for D7 closure formalization):**
- `s3://equine-raw-data/workout-loads/` shows daily files matching `{date_str}_{HHMMSS}.json` at ~07:00 UTC for 2026-04-28 → 2026-05-09 (12 consecutive days; 0.83–1.20 MB each).
- 2026-05-09 file (1.01 MB at 07:00:57 UTC) PUT after equine-ingestion was restored at 04:37 UTC, but the 12-day series spans the full Lambda-INACTIVE window — confirming the producer is independent of the Lambda runtime.
- CloudTrail Event History shows paired AssumeRole events at 2026-05-09T03:01:01 UTC-04:00 (= 07:01:01 UTC) on the equine-ingestion role; Source=`sts.amazonaws.com`, User=null (principal masked at default field set; Tony self-attestation supplies identity).
- Ruled out by enumeration: CodeBuild (no equine project); ECS (0 services, 0 tasks); EC2 (0 equine instances); Lambda (no non-equine Lambda using equine-ingestion role per E1).

This finding subsumes Phase A D1 § 6.4 candidate 5.3.N+3 (Undocumented HRN Workout Producer); 5.3.N+3 closure-ready upon D7 formalization.

---

## 4. Closure Candidate Drafts (D7 input)

### 4.1 C1 — Phase 5.3.17 PARTIAL closure (equine-ingestion only)

Per Tony Q2 ratification: PARTIAL closure for equine-ingestion only; FULL 5.3.17 closure deferred to D4 completion.

```
closed-by (PARTIAL, equine-ingestion only):
  Phase A informal recovery 2026-05-09 04:37 UTC
  + docs/operations/SOURCE_STATUS_AUDIT_2026-05-08.md § 1.3 (frozen pre-recovery state)
  + OCRC D1 V1 verification at S1 2026-05-09
  + CloudTrail UpdateFunctionCode20150331v2 by root user at 2026-05-09T04:37:40 UTC (= 00:37:40 EDT, UTC-04:00)
    (Tony manual restore; visible in CloudTrail Event History)
verification:
  aws lambda get-function --function-name equine-ingestion returns
  State=Active LastModified=2026-05-09T04:37:39 UTC LastUpdateStatus=Successful at S1
ratified-by: [Tony pending; D7 drafting CC formalizes per P-Q3]
```

FULL closure of 5.3.17 (covering equine-results + equine-feature-engineering): deferred to D4 restoration completion. Closing-evidence draft inheriting from D4 LANDED state.

### 4.2 C2 — Phase 5.3.18 enumeration confirmed

Both Secrets Manager entries (2captcha + brightdata) confirmed at S1. Production-Lambda consumer count = 0. Disposition recommendation depends on equibase_probe DEPRECATED-candidate-cohort decision per 5.3.N+8.

```
closed-by (kill disposition, contingent on equibase_probe cohort kill):
  OCRC D1 V8 verification at S1 2026-05-09
  + repo grep returning 0 production-Lambda consumers
verification:
  consumer enumeration via repo grep + IAM policy analysis returns
  equibase_probe/option_b_probe.py + option_d_probe.py as sole consumers;
  zero production-Lambda consumers (verified via aws iam list-attached-role-policies
  for 7 deployed-Lambda service roles + grep -rln '2captcha\|brightdata'
  backend/ infrastructure/ scripts/ equibase_probe/ returns matches only
  in equibase_probe/).
ratified-by: [Tony pending; D7 drafting CC formalizes; P-Q3]

NOTE: Closure disposition (kill / retain / paid-promote / scheduled-manual) depends on
equibase_probe/ DEPRECATED-candidate-cohort decision per bible § 4.2.6. Phase 5.3.18
closure may co-bundle with 5.3.N+8 (equibase-probe ECS task families) + 5.3.N+9
(equine-equibase-acquisition ECR repo) in a single cohort-disposition decision.
```

### 4.3 C3 — Phase 5.3.20 FULL closure

```
closed-by:
  Phase A informal recovery 2026-05-09 04:37 UTC
  + docs/operations/PHASE_A_SUSPENSION_NOTE_2026-05-09.md § 1
  + CC Step 4 report (operational verification)
  + OCRC D1 V1 verification at S1 2026-05-09
verification:
  aws lambda get-function --function-name equine-ingestion returns
  State=Active LastUpdateStatus=Successful ImageUri=…1ac0a1893ba3… at S1 2026-05-09;
  CC Step 4 report documented raw_query SELECT 1 success +
  fetch_daily_entries(today) success + 320 entries landed for 2026-05-09
ratified-by: [Tony pending; D7 drafting CC formalizes per P-Q3]
```

---

## 5. New Defect Candidates (Phase 5.3.N+ placeholders per Q1)

Monotonic 5.3.N+ numbering inheriting from Phase A D1 § 6.4. Final concrete IDs assigned at D7 drafting CC + Tony individual ratification per P-Q3.

### 5.1 Inherited from Phase A D1 § 6.4 (4 candidates)

| Placeholder | Title | Severity | Source |
|---|---|---|---|
| 5.3.N+1 | NYRA Workout Cron Capture-Time Defect | HIGH | Phase A D1 § 6.4 |
| 5.3.N+2 | Schema Drift in `equine-ingestion` Image SQL | MEDIUM | Phase A D1 § 6.4 |
| 5.3.N+3 | Undocumented HRN Workouts Producer | LOW (downgraded from MEDIUM per Q3 2026-05-09) | Phase A D1 § 6.4; **OCRC D1 § 3 supplies closing-evidence** |
| 5.3.N+4 | HRN Entries Cron Capture-Time Risk (analogue) | LOW pending confirmation | Phase A D1 § 6.4 |

### 5.2 Surfaced by OCRC D1 (11 candidates)

Per Tony Q4 ratification: separate per-resource candidates; composite "CDK substrate drift" framing deferred to D7 drafting CC + Tony individual ratification.

| Placeholder | Title | Severity | Closing condition | Owner cycle |
|---|---|---|---|---|
| 5.3.N+5 | **6 EventBridge rules out-of-band** (equine-angle-stats-nightly, equine-fetch-results-nightly, equine-nyra-workouts-daily, equine-daily-retrain-full, equine-weekly-retrain-pl, equine-weekly-retrain-wr) — created out-of-band; not in CDK source nor CFN. | MEDIUM | (a) Reconcile to CDK + redeploy, OR (b) document as accepted-out-of-band in bible with provenance trail. | Separate CDK-reconciliation cycle post-OCRC + post-Phase-A |
| 5.3.N+6 | **4 ECS task families out-of-band** (equine-training-{daily-full,pl,win-prob,manual}) — production-active (driving daily + weekly retrains via orphan EventBridge rules) but not declared in CDK source. | MEDIUM | Same as 5.3.N+5 disposition. | Same |
| 5.3.N+7 | **equine-nyra-workouts triple out-of-band** (Lambda + IAM role `equine-nyra-workouts-role` + ECR repo `equine-nyra-workouts:v1-…`) — created out-of-band 2026-04-27; fully production-functional but not in any equine CDK stack. | MEDIUM | Same | Same |
| 5.3.N+8 | **4 equibase-probe ECS task families registered without service** — no scheduled task, no service, no production runtime; cohort-coordinated with equibase_probe/ Dockerfiles + 4 probe-script files in repo + 2captcha + brightdata secrets. | LOW | Tony disposition per bible § 4.2.6 (kill / paid-replacement / scheduled-manual). | Separate cycle (potential co-bundle with 5.3.18) |
| 5.3.N+9 | **equine-equibase-acquisition ECR repo** (10 images, 2026-04-27) with zero production consumers — already partially documented at architecture_overview § 3.7 but not yet a PHASE_5_BACKLOG entry. | LOW | Lifecycle policy + delete-or-keep ratified. | Bundled with 5.3.N+8 |
| 5.3.N+10 | **equine-training ECR repo out-of-band** — custom repo (2026-03-19) NOT consumed by CDK (CDK uses `fromAsset` → CDK assets repo); zero production consumers traced. | LOW | Investigate + kill if confirmed orphan. | Same as 5.3.N+5 |
| 5.3.N+11 | **0 CloudWatch alarms on any equine resource** — no operational health alarms on any of the 8 Lambdas, 13 EventBridge rules, ECS cluster/task families, or RDS database. SNS topic + email subscription exists but has no producer. Operational health monitoring gap matches Phase A suspension note candidate 5 (QB-tier prophylactic checks) and broader operational-health-monitoring methodology gap. | MEDIUM | **D9 deploys minimum alarm set; closes 5.3.N+11 upon completion** (forward-reference per OCRC scope expansion ratification 2026-05-09). | OCRC D9 (in-scope post-expansion) |
| 5.3.N+12 | **0 CloudTrail trails configured account-wide** — Management Events available only via CloudTrail Event History (90-day, no programmatic projection); Data Events not available; cannot solve V6 InputTransformer drift origin nor finer-grain producer hunts at S1 scope. Banking observation candidate (CloudTrail Data Events as methodology infrastructure). | MEDIUM | Either (a) configure trail with management + data event selectors for equine resources, or (b) accept the gap and document in operational reliability bible. | Methodology infrastructure cycle (adjacent to OCRC banking observation candidate) |
| 5.3.N+13 | **SNS topic equine-equalizer-alerts + email subscription out-of-band** — not declared in any CDK stack; created outside infrastructure-as-code. | LOW | Same as 5.3.N+5. | Bundled |
| 5.3.N+14 | **3 IAM roles out-of-band** (equine-events-ecs-role, equine-nyra-workouts-role, equine-training-task-role) — production-active but not declared in CDK. | LOW | Same as 5.3.N+5. | Bundled |
| 5.3.N+15 | **CDK source declares Aurora cluster but live RDS is standalone instance equine-db** — database-stack.ts:52 declares `rds.DatabaseCluster`; CFN reflects DBCluster + Writer DBInstance; live AWS state per architecture_overview v3-patched-a § 3.3 reports `DBClusterIdentifier: None` (standalone instance). Substantial CDK-source-vs-live-state drift; documented as REFUTED in architecture_overview but not currently a PHASE_5_BACKLOG entry. | MEDIUM | (a) Reconcile CDK to standalone-instance pattern + redeploy, OR (b) document explicitly in bible as accepted out-of-band substitution + close. | Separate CDK-reconciliation cycle |

---

## 6. OCRC Scope Expansion — D9 + D10 Forward-References

Per Tony ratification 2026-05-09, OCRC scope expanded with two additional deliverables:

### 6.1 D9 — CloudWatch alarms deployment

- **Scope:** alarms for all 8 equine Lambdas (Errors + Throttles + IteratorAge as applicable) + cron-firing alarm on equine-fetch-results-nightly (post-D10 Input fix verifies firing works).
- **Tier:** 2-tier (drafting + audit).
- **Sequencing:** post-D5 (NYRA cron timing fix lands).
- **Closes:** 5.3.N+11.

### 6.2 D10 — equine-fetch-results-nightly Input fix

- **Scope:** surgical fix to resolve V6 InputTransformer `USE_TODAY_MINUS_1` sentinel handling. Fix path chosen at D10 drafting CC per D2 disambiguation (Path A EventBridge rule edit / Path B handler default-date logic / Path C both).
- **Tier:** 3-tier (drafting + audit + lock).
- **Sequencing:** post-D2 (cron-payload audit lands).
- **Closes:** V6 priority-finding drift (§ 2.3 above).

These additions update the OCRC handoff § 3.1 deliverable enumeration. D8 close-out summary will incorporate D9 + D10 LANDED state into exit gate.

---

## 7. SP Gate Sign-off

V1–V8 + R1–R7 ratified by Tony at SP gate 2026-05-09. Synthesis directives Q1–Q5 + OCRC scope expansion D9 + D10 ratified 2026-05-09. S1 drafting CC dispatch complete; awaiting S2 audit CC dispatch (fresh-conversation-per-session per OCR-Q5).

**S2 audit CC dispatch instructions:** adversarial re-enumeration + classification spot-check + audit of HRN producer closure + audit of V6 priority-finding format compliance with Q5 spec + audit of 5.3.N+ defect candidate severity assignments + audit of D9/D10 forward-reference accuracy.

---

**End of OCRC D1 — Resource Inventory — 2026-05-09.**
