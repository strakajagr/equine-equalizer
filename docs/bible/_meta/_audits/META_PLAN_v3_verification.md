# META_PLAN v3 — Verification Log

**Document:** META_PLAN_v3_verification
**Companion to:** META_PLAN.md v3
**Author:** CC (drafting under verification discipline)
**Date:** 2026-05-03
**Purpose:** Per-claim verification record. Every factual claim about EE in v3 is recorded here with evidence. v2's worst failures were fabricated content in Tier 1 framing; this log is the safeguard.

**Verification methodology:**
- "Live AWS" = `aws` CLI against the operator's AWS account (584812014683)
- "Live API" = HTTPS request against `https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com`
- "Codebase" = file read against working tree at `/home/strakajagr/projects/equine-equalizer/`
- "Runtime test" = Python interpreter executing the actual module to observe runtime values
- "Dump-only" = inherited from `EE_CURRENT_STATE_DUMP.md` without independent verification (these are explicitly flagged in v3)

---

## Claim 1: Lambda function count

**Claim:** EE has 8 Lambda functions.
**Document location:** v3 § 1.3, § 2.3
**What was checked:** `aws lambda list-functions --query 'Functions[?starts_with(FunctionName, \`equine\`)].FunctionName' --output text`
**What was found:** 8 functions: equine-feature-engineering, equine-inference, equine-ingestion, equine-ls-inference, equine-nyra-workouts, equine-pl-inference, equine-results, equine-wr-inference
**Survived:** Yes
**Action:** Included as-is

## Claim 2: INACTIVE Lambda count and identities

**Claim:** Three Lambda functions are currently INACTIVE: `equine-ingestion`, `equine-feature-engineering`, `equine-results`.
**Document location:** v3 § 2.3
**What was checked:** `aws lambda get-function --function-name <fn> --query 'Configuration.State'` for each of the 8 functions
**What was found:**
- equine-ingestion: Inactive (StateReason: "The function is trying to use a deleted image.")
- equine-feature-engineering: Inactive (same StateReason)
- equine-results: Inactive (same StateReason)
- equine-inference, equine-wr-inference, equine-pl-inference, equine-ls-inference, equine-nyra-workouts: Active
**Survived:** Yes
**Action:** Included as-is. **This corrects v2 which claimed 2 INACTIVE; the dump (§ 6.1) only listed equine-ingestion, missing the other two. The v2 audit caught feature-engineering but missed equine-results. v3's verification adds equine-results.**

## Claim 3: EventBridge rule count and disabled count

**Claim:** 13 EventBridge rules total, 3 disabled.
**Document location:** v3 § 1.3, § 2.3
**What was checked:** `aws events list-rules --name-prefix equine --query 'Rules[].[Name,State]' --output text`
**What was found:** 13 rules total. ENABLED (10): angle-stats-nightly, daily-retrain-full, fetch-results-nightly, ingestion-daily, ls-inference-daily, nyra-workouts-daily, pl-inference-daily, results-daily, weekly-retrain-wr, wr-inference-daily. DISABLED (3): feature-engineering-daily, inference-daily, weekly-retrain-pl.
**Survived:** Yes
**Action:** Included as-is. (Confirms v2's correction of v1's "5 disabled" error.)

## Claim 4: Database table count

**Claim:** 14 tables + 1 materialized view.
**Document location:** v3 § 1.3, § 2.3
**What was checked:** `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql | sed 's/CREATE TABLE \(IF NOT EXISTS \)\?//' | awk '{print $1}' | sort -u`
**What was found:** 14 unique table names: entries, horses, jockeys, ls_predictions, model_versions, past_performances, pl_predictions, predictions, races, results, tracks, trainers, workouts, wr_predictions. Plus 1 `CREATE MATERIALIZED VIEW IF NOT EXISTS trainer_stats` in migration 008.
**Survived:** Yes
**Action:** Included as-is

## Claim 5: Migration filename format and duplicate-005 case

**Claim:** All 12 existing migrations use `NNN_short_description.sql` format (no date in name); 005 is duplicated.
**Document location:** v3 § 7.12
**What was checked:** `find backend/database/migrations -name "*.sql" | sort`
**What was found:** 12 files: 001_initial_schema.sql, 002_fix_race_type_length.sql, 003_widen_varchar_columns.sql, 004_backfill_running_style.sql, **005_backfill_pace_delta.sql**, **005_three_prediction_tables.sql**, 006_backfill_early_pace_pressure.sql, 007_backfill_trainer_name.sql, 008_create_trainer_stats.sql, 009_backfill_pace_delta_v2.sql, 010_ls_predictions_first_class.sql, 011_wr_predictions_unique_fix.sql
**Survived:** Yes
**Action:** Included. v3 § 7.12 prescribes grandfathering per Tony's Q1 answer; new format `NNN_YYYYMMDD_short_description.sql` from 012+; bible entry for migration 012 documents the cutover.

## Claim 6: Migration runner mechanism

**Claim:** `migrate.py` tracks applied migrations by filename in a `schema_migrations` table.
**Document location:** v3 § 7.12
**What was checked:** Read `backend/database/migrations/migrate.py` lines 44-72
**What was found:**
```
CREATE TABLE IF NOT EXISTS schema_migrations (
    migration_id SERIAL PRIMARY KEY,
    filename VARCHAR(255) UNIQUE NOT NULL,
    applied_at TIMESTAMPTZ DEFAULT NOW()
)
```
And `get_applied_migrations(conn)` returns set of filenames; `run_migrations` iterates `sorted(... .sql files)` and skips filenames in the applied set.
**Survived:** Yes
**Action:** Included. Confirms grandfathering compatibility — runner sees both legacy `005_three_prediction_tables.sql` and future `012_20260601_add_X.sql` as filenames; both work.

## Claim 7: Model registry counts (88 entries, 45 active)

**Claim:** 88 entries in `model_versions`; 45 simultaneously active.
**Document location:** v3 § 1.3, § 9.13
**What was checked:** `curl https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com/dashboard/metrics`, parse `model_history` array; count entries where `is_active == True`
**What was found:** Total: 88. Active: 45. (Active model: `rk_full_gonzo_sauce_20260502_0452`.)
**Survived:** Yes
**Action:** Included as-is. (Verification path: dashboard endpoint, which queries `model_versions` directly. Live confirmation, not dump-only.)

## Claim 8: API Gateway route count

**Claim:** 41 routes on API Gateway v2 (`gb5qlfy10h`).
**Document location:** v3 § 3.2 hypothesis #6
**What was checked:** `aws apigatewayv2 get-routes --api-id gb5qlfy10h --query 'Items[].RouteKey' --output text | tr '\t' '\n' | wc -l`
**What was found:** 41
**Survived:** Yes
**Action:** Included as-is

## Claim 9: `get_active_model_by_type` signature

**Claim:** The function takes only `model_type: str`. No `_and_style` variant exists.
**Document location:** v3 § 9.13, Appendix A.1
**What was checked:** `grep -nE "^def get_active|def get_active_model" backend/repositories/model_version_repository.py` and read lines 100-115
**What was found:**
```python
def get_active_model_by_type(
    self, model_type: str
) -> Optional[ModelVersion]:
```
Only `get_active_model_by_type` exists. Docstring says `model_type must be 'wr', 'pl', or 'ls'`. Callers: `pl_inference_service.py:96`, `ls_inference_service.py:139`, `wr_inference_service.py:269` — all pass only `model_type`.
**Survived:** Partial — function exists but with the limited signature.
**Action:** v3 § 9.13 and A.1 rewritten honestly: the FORBIDDEN example shows the current call pattern; the CORRECT example notes that a `style`-aware variant does not yet exist and is Phase 5 work. **No fabricated function name in v3.**

## Claim 10: `model/features/feature_definitions.py` — runtime state

**Claim:** ALL_FEATURES is populated to 73 at runtime; the file is NOT orphaned; it is imported by two production paths.
**Document location:** v3 § 7.7 + Appendix A.4 (replaced example with `predictions` legacy table)
**What was checked:**
1. Runtime test: `cd /home/strakajagr/projects/equine-equalizer && python3 -c "from model.features.feature_definitions import ALL_FEATURES, FEATURE_COUNT; print(len(ALL_FEATURES), FEATURE_COUNT)"`
2. Import grep: `grep -rn "from.*model.features.feature_definitions" --include="*.py"`
**What was found:**
1. Runtime: `ALL_FEATURES count: 73`, `FEATURE_COUNT: 73`. The `ALL_FEATURES = []` is initialization only; lines 141-142 populate via `for group in FEATURE_GROUPS.values(): ALL_FEATURES.extend(group['features'])`.
2. Imports: `model/training/train.py:40` AND `backend/services/inference_service.py:28`.
**Survived:** No — v2 / dump claim is false.
**Action:** **DROPPED. The dump's "ALL_FEATURES = [] is empty" is wrong. v3 Appendix A.4 uses a different deprecated example: the legacy `predictions` table (see Claim 16). v3 § 7.7 references the new example.**

## Claim 11: `.gitignore` already contains deploy artifacts

**Claim:** `.frontend-bucket`, `.cf-distribution-id`, `cdk-outputs.json`, `frontend/.env.production` are all already in `.gitignore`.
**Document location:** v3 § 7.14 (gitignore baseline)
**What was checked:** `cat /home/strakajagr/projects/equine-equalizer/.gitignore`
**What was found:** End of file contains:
```
# Deployment artifacts (machine-specific)
.frontend-bucket
.cf-distribution-id
cdk-outputs.json
frontend/.env.production
```
**Survived:** Yes — but the v2 audit (Q2.2) and Tony's Q4 instruction were both based on the assumption that these were NOT gitignored. **This is a v2 audit error — the audit's grep output actually showed the entries; the audit-CC misread it.**
**Action:** v3 § 7.14 documents this as already-established baseline rather than as a new Phase 0 prerequisite. The Phase 0 task becomes "audit deploy scripts for any artifacts NOT yet covered" rather than "add the known ones."

## Claim 12: Deploy script artifact writes

**Claim:** `scripts/deploy-backend.sh:243` writes `.frontend-bucket`; line 262 writes `.cf-distribution-id`; line 229 writes `frontend/.env.production`.
**Document location:** v3 § 7.14
**What was checked:** `grep -nE "\\s>\\s|\\s>>\\s" scripts/deploy-backend.sh scripts/deploy-frontend.sh deploy_all.sh`
**What was found:** Confirmed at the cited lines. No other artifact writes found in the deploy scripts beyond log redirects.
**Survived:** Yes
**Action:** Included; v3 § 7.14 references these as the canonical write sites.

## Claim 13: DD bible line count

**Claim:** DD bible is 2,578 lines.
**Document location:** v3 § 1.2
**What was checked:** `wc -l /home/strakajagr/projects/dynasty-dugout/ARCHITECTURE_BIBLE.md`
**What was found:** 2578
**Survived:** Yes
**Action:** Included as-is

## Claim 14: DD bible section names

**Claim:** DD § 18 = "What Was Fixed — Do Not Revert"; § 19 = "Common Mistakes to Avoid"; § 20 = "Forbidden Patterns (locked 2026-04-21)"; § 21 = "Deprecated Fields (Phase B Cleanup Queue)".
**Document location:** v3 § 7.4, § 7.5, § 7.6, § 7.7
**What was checked:** `grep -nE "^## (18|19|20|21)\\." ARCHITECTURE_BIBLE.md`
**What was found:**
- L2160: `## 18. WHAT WAS FIXED — DO NOT REVERT`
- L2258: `## 19. COMMON MISTAKES TO AVOID`
- L2394: `## 20. FORBIDDEN PATTERNS (locked 2026-04-21)`
- L2456: `## 21. DEPRECATED FIELDS (PHASE B CLEANUP QUEUE)`
**Survived:** Yes
**Action:** Included as-is

## Claim 15: Bug #28 line reference

**Claim:** HRN scraper Bug #28 manifests at `backend/services/data_sources/hrn_scraper.py:802-804` in `parse_payout(N)` calls.
**Document location:** v3 Appendix A.5
**What was checked:** Read lines 795-815 of `hrn_scraper.py`
**What was found:** Lines 802-804:
```python
'win_payout':      parse_payout(1),
'place_payout':    parse_payout(2),
'show_payout':     parse_payout(3),
```
**Survived:** Yes
**Action:** Included as-is. Note: there is no in-code `Bug #28` comment yet (verified via grep); the bug is documented in operator memory file `equine-equalizer-bug-28-hrn-scraper.md` only. v3 calls this out in the relevant section.

## Claim 16: Legacy `predictions` table — replacement for A.4 example

**Claim:** The legacy `predictions` table exists, was NOT dropped by migration 005, has 6,600 rows per dashboard, and has active callers via `prediction_router.py` and `race_router.py`.
**Document location:** v3 Appendix A.4
**What was checked:**
1. `grep -nE "CREATE TABLE.*predictions" schema.sql migrations/*.sql` and `grep -nE "DROP TABLE" migrations/*.sql`
2. Dashboard counts block: `predictions: 6600`
3. Caller grep: `grep -rn "PredictionRepository\(" backend/routers/`
**What was found:**
1. CREATE TABLE predictions in `001_initial_schema.sql:327` and `schema/schema.sql:327`. Migration 005 creates wr/pl/ls_predictions tables but contains zero `DROP TABLE` statements. Verified.
2. `predictions: 6600` rows per live dashboard counts.
3. `PredictionRepository(conn)` instantiated in `prediction_router.py:34, 61, 92` (4 references including the import) and `race_router.py:277` (with import on line 273). Plus `dashboard_router.py:93,105` and `horse_router.py:66` SELECT directly from `predictions`.
**Survived:** Yes
**Action:** Used as Appendix A.4 deprecated-field-tracker example. Replaces the v2 (false) `model/features/feature_definitions.py` example.

## Claim 17: ECR image count in CDK assets bucket

**Claim:** `cdk-hnb659fds-container-assets-584812014683-us-east-1` has 5 images (the tag `equine-ingestion` references is no longer present, per dump § 6.4).
**Document location:** v3 § 2.3 (in passing, as part of "Disabled-but-existing infrastructure" inventory)
**What was checked:** `aws ecr list-images --repository-name cdk-hnb659fds-container-assets-584812014683-us-east-1 --query 'length(imageIds)'`
**What was found:** 5
**Survived:** Yes
**Action:** Included as supporting evidence for INACTIVE Lambda state. Note: the dump's claim that the tag `equine-ingestion` references is missing is consistent with the AWS-reported state ("The function is trying to use a deleted image"). Cannot verify the missing-tag specifics from outside without the original tag string, but the inactive state is consistent with the dump's explanation.

## Claim 18: S3 bucket count

**Claim:** 4 EE-related S3 buckets.
**Document location:** v3 § 2.3
**What was checked:** `aws s3 ls | grep equine`
**What was found:** equine-frontend, equine-model-artifacts, equine-processed-data, equine-raw-data (all created 2026-03-15)
**Survived:** Yes
**Action:** Included as-is

## Claim 19: Secrets Manager entries

**Claim:** 3 EE-related secrets: `db-credentials`, `2captcha-api-key`, `brightdata-api-key`. The latter two have no code consumers.
**Document location:** v3 § 2.3
**What was checked:**
1. `aws secretsmanager list-secrets --query 'SecretList[?starts_with(Name, \`equine\`)].Name' --output text`
2. `grep -rn "2captcha\|brightdata" backend model scripts --include="*.py"`
**What was found:**
1. equine-equalizer/db-credentials, equine-equalizer/2captcha-api-key, equine-equalizer/brightdata-api-key
2. Zero hits for 2captcha or brightdata in `backend/`, `model/`, or `scripts/` Python.
**Survived:** Yes
**Action:** Included as-is

## Claim 20: ECS task definition families

**Claim (revised from dump):** 5 ECS task families exist starting with `equine`: `equine-training`, `equine-training-daily-full`, `equine-training-manual`, `equine-training-pl`, `equine-training-win-prob`. The dump (§ 6.2) listed 3 — it missed `equine-training` and `equine-training-win-prob`.
**Document location:** v3 § 1.3 (mentioned only generically as "ECS Fargate training fleet")
**What was checked:** `aws ecs list-task-definition-families --query 'families[?starts_with(@, \`equine\`)]' --output text`
**What was found:** 5 families as listed.
**Survived:** Yes — but reveals the dump is again incomplete.
**Action:** v3 keeps the generic phrasing "ECS Fargate training fleet" rather than commit to a count, since "active vs. retired families" requires deeper inspection. Flagged as a Phase 1 audit target for the ML Stack Bible.

## Claim 21: Phase duration arithmetic

**Claim:** Per-phase highs sum to 19 weeks (4+8+2+2+3), not 17 as v2 claimed.
**Document location:** v3 § 3.7
**What was checked:** Re-summed v2's per-phase ranges: Phase 0 (2-4) + Phase 1 (4-8) + Phase 2 (1-2) + Phase 3 (1-2) + Phase 4 (1-3)
**What was found:** Low: 2+4+1+1+1 = 9. High: 4+8+2+2+3 = 19.
**Survived:** Yes
**Action:** v3 § 3.7 corrected to 9–19 weeks. Acknowledged in v2→v3 changelog.

## Claim 22: Git state confirms uncommitted-deploy practice

**Claim:** EE git history is one day in March 2026; production code has been deployed without commits since then.
**Document location:** v3 § 1.2 (root cause framing)
**What was checked:** `git log -1 --format="%h %ad %s" --date=short` and `git status --porcelain | wc -l`
**What was found:**
- Last commit: `2a3d758 2026-03-15 Widen VARCHAR columns and isolate per-race DB connections`
- Working tree: 28+ modified files plus untracked `Dockerfile.ls-inference`
**Survived:** Yes
**Action:** Included as-is. Reinforces the rationale for § 7.10's commit-before-deploy hard rule and § 3.1.1's pre-Phase-1 baseline commit.

## Claim 23: DD bible structural facts cited in Motivation

**Claim:** DD is multi-runtime (Lambda + Node.js EC2 draft server + worker_package + frontend) with multiple canonical objects (Player, League, financial, pricing, etc.).
**Document location:** v3 § 1.4
**What was checked:** `grep -nE "draft-server|EC2|websocket" ARCHITECTURE_BIBLE.md` plus § 4 (Canonical Player), § 4.5 (Contract/Financial), § 5 (Canonical League), § 10 (Pricing) headings
**What was found:**
- L418: `| Draft Server | Node.js / Express / Socket.io | Runs on EC2, draft.dynasty-dugout.com |`
- L1768: `Draft Server (EC2 Node.js/Express/Socket.io — in-memory state + DB persistence)`
- L2161: `├── draft-server/                      # Node.js WebSocket server (EC2)`
- Sections § 4 (canonical Player), § 4.5 (canonical Financial), § 5 (canonical League), § 10 (canonical Pricing) all present.
**Survived:** Yes
**Action:** Included as-is

---

## Verification summary

**Total claims documented:** 23
**Survived as-is:** 19
**Survived with modification:** 1 (Claim 20 — dump miscount, v3 keeps generic phrasing)
**Survived but reveals upstream error:** 2 (Claim 2 — v2's INACTIVE count was wrong; Claim 11 — v2 audit's gitignore-gap claim was wrong)
**Dropped:** 1 (Claim 10 — `model/features/feature_definitions.py` "orphan" example was false; replaced with Claim 16 in A.4)

**Architectural questions surfaced for QB attention:**

1. **Tony's Q4 instruction is partially based on a false premise.** v2 audit Finding Q2.2 claimed `.cf-distribution-id` and `.frontend-bucket` were not gitignored. Verification (Claim 11) shows they ARE gitignored. Tony's Q4 said "add to .gitignore as Phase 0 prerequisite" — but this is already done. v3 § 7.14 documents the actual state: `.gitignore` was established at initial commit (2026-03-15) and already contains the deploy artifacts. The Phase 0 task becomes "audit deploy scripts for any *new* artifacts not yet covered," not "add the known ones." Surfacing this so Tony knows v3 is integrating the verified state, not the assumed state.

2. **The dump's ECS task-family inventory is incomplete (Claim 20).** Dump § 6.2 listed 3 families; live AWS shows 5. v3 keeps generic phrasing rather than re-asserting a number. This is informational — Phase 1's ML Stack Bible audit will need to enumerate the active vs retired families.

3. **The dump's INACTIVE Lambda inventory is incomplete (Claim 2).** Dump § 6.1 named only `equine-ingestion` as INACTIVE; v2 audit added `equine-feature-engineering`; v3 verification adds `equine-results`. Three INACTIVE total. The v2 audit-CC missed `equine-results` despite running `aws lambda get-function` — at the time only the two were checked. v3 ran the full sweep. Methodology takeaway: future audit-CC prompts should explicitly require running the inventory query against ALL 8 Lambdas, not spot-checking.

4. **No in-code Bug #28 marker exists yet.** Bug #28 is documented in operator memory file only. v3 references this honestly. A reasonable Phase 5 remediation step is to add an in-code comment at `hrn_scraper.py:800` referencing the bug + the Phase 5 backlog entry, so the bug becomes greppable.

5. **Dashboard endpoint is a viable verification path.** Despite `equine-ingestion` being INACTIVE, the dashboard endpoint (`/dashboard/metrics`) is served by `equine-inference` which is Active — so model registry counts ARE verifiable via API even when ingestion is dead. v3 § 4.5 source-priority hierarchy documents this as "live API" tier where applicable.

**No fabricated content in v3.** Every concrete claim has a verification entry above. Every claim that could not be verified has been dropped, replaced, or explicitly flagged.
