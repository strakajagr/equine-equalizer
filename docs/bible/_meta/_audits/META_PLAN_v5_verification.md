# META_PLAN v5 — Verification Log

**Document:** META_PLAN_v5_verification
**Companion to:** META_PLAN.md v5
**Author:** CC (drafting under verification discipline)
**Date:** 2026-05-04
**Purpose:** Per-claim verification record. v5 applies the verification-log-precision rule (§ 6.5) broadly — to every aggregable count, not only code-reference counts. Tony's locked decision in the v5 cycle: Option B (broad sweep). v5 also corrects v4's calibration bypass line range and adds a Derby Day 2026 source-authority annotation.

**Verification methodology:**
- "Live AWS" = `aws` CLI against operator's account 584812014683
- "Live API" = HTTPS request against `https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com`
- "Codebase" = file read against working tree at `/home/strakajagr/projects/equine-equalizer/`
- "Runtime test" = Python interpreter executing the actual module
- "Operator memory" = file read against `~/.claude/projects/-home-strakajagr/memory/<filename>.md`
- "Operator-stated" = claim sourced from Tony's verbal/written framing in this drafting cycle's spec; verified against operator framing, NOT against primary code/AWS/DB source. Per § 4.5 source-priority tier 5.
- "Inherited from v4 log Claim N — re-verified [date]" = entry imported from `META_PLAN_v4_verification.md` and re-run; value confirmed unchanged

**Verification log precision rule (locked v4, scope broadened in v5):**
Counts are decomposed into definitions / instantiations / imports / uses, never aggregated as "N references including..." that can be compressed by a reader. Anything aggregable is shown both as components and as a sum. **Scope (per Tony's v5 cycle decision):** rule applies broadly, not narrowly to code-reference counts. Working-tree status, model registry, EventBridge rules, Lambdas — all decomposed in v5.

---

## Claim 1: Lambda function count

**Claim:** EE has 8 Lambda functions, decomposed as 5 Active + 3 INACTIVE.
**Document location:** v5 § 1.3, § 2.3
**What was checked (re-verified 2026-05-04):** `aws lambda list-functions --query 'Functions[?starts_with(FunctionName, \`equine\`)].FunctionName' --output text` (count) and `aws lambda get-function --function-name <fn> --query 'Configuration.State'` for each
**What was found:** 8 functions total. Active (5): equine-inference, equine-wr-inference, equine-pl-inference, equine-ls-inference, equine-nyra-workouts. INACTIVE (3): equine-ingestion, equine-feature-engineering, equine-results.

Decomposed: 5 Active + 3 INACTIVE = 8 total.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 1 + 2 — merged here with explicit decomposition

## Claim 3: EventBridge rule count

**Claim:** 13 EventBridge rules, decomposed as 10 ENABLED + 3 DISABLED.
**Document location:** v5 § 1.3, § 2.3
**What was checked (re-verified 2026-05-04):** `aws events list-rules --name-prefix equine --query 'Rules[].[Name,State]' --output text`
**What was found:**
- ENABLED (10): equine-angle-stats-nightly, equine-daily-retrain-full, equine-fetch-results-nightly, equine-ingestion-daily, equine-ls-inference-daily, equine-nyra-workouts-daily, equine-pl-inference-daily, equine-results-daily, equine-weekly-retrain-wr, equine-wr-inference-daily.
- DISABLED (3): equine-feature-engineering-daily, equine-inference-daily, equine-weekly-retrain-pl.

Decomposed: 10 ENABLED + 3 DISABLED = 13 total. Both lists fully enumerated in § 2.3.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 3 — re-verified

## Claim 4: Database table count

**Claim:** 14 tables + 1 materialized view.
**Document location:** v5 § 1.3, § 2.3
**What was checked:** `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql | sed 's/CREATE TABLE \(IF NOT EXISTS \)\?//' | awk '{print $1}' | sort -u`
**What was found:** 14 unique table names; plus 1 materialized view (`trainer_stats`) in migration 008.

Decomposed: 14 tables + 1 matview = 15 schema objects.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 4 — re-verified

## Claim 5: Migration filename format and duplicate-005 case

**Claim:** All 12 existing migrations use `NNN_short_description.sql` format; sequence 005 has 2 files (the duplicate).
**Document location:** v5 § 7.12
**What was checked:** `find backend/database/migrations -name "*.sql" | sort`
**What was found:** 12 files; 11 unique sequence numbers; sequence 005 has 2 files (`005_backfill_pace_delta.sql` and `005_three_prediction_tables.sql`).

Decomposed: 12 files = 11 unique-numbered + 1 duplicate at sequence 005.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 5 — re-verified

## Claim 6: Migration runner mechanism

**Claim:** `migrate.py` tracks applied migrations by filename in a `schema_migrations` table.
**Document location:** v5 § 7.12
**What was checked:** Read `backend/database/migrations/migrate.py` lines 44–95
**What was found:** Schema creation includes `filename VARCHAR(255) UNIQUE NOT NULL`; tracking is by filename string.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 6 — re-verified

## Claim 7: Model registry counts (UPDATED v5 — broad-sweep precision)

**Claim:** 88 entries in `model_versions`, decomposed as 45 active + 43 inactive.
**Document location:** v5 § 1.3, § 9.13, A.1
**What was checked (re-verified 2026-05-04):** `curl https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com/dashboard/metrics`, parse `model_history`; partition by `is_active`
**What was found:** total=88, active=45, inactive=43, sum_check=88 (verified active + inactive == total).

Decomposed: 88 = 45 (is_active=TRUE) + 43 (is_active=FALSE). Sum verified by partition arithmetic.
**Survived:** Yes
**Action:** Modified from v4 log Claim 7. v4 phrasing "88 entries; 45 simultaneously active" implied 43 inactive. v5 makes both components explicit: "88 = 45 active + 43 inactive." Per Tony's v5 cycle decision (broad sweep).

## Claim 8: API Gateway route count

**Claim:** 41 routes on API Gateway v2 `gb5qlfy10h`.
**Document location:** v5 § 8.5 (referenced in route-behavior context)
**What was checked (re-verified 2026-05-04):** `aws apigatewayv2 get-routes --api-id gb5qlfy10h --query 'Items[].RouteKey' --output text | tr '\t' '\n' | wc -l` → 41
**What was found:** 41 routes
**Survived:** Yes
**Action:** Inherited from v4 log Claim 8 — re-verified

## Claim 9: `get_active_model_by_type` signature and SQL

**Claim:** Function takes only `model_type: str`. Body is `WHERE is_active = true AND model_type = %s LIMIT 1`. No `_and_style` variant exists.
**Document location:** v5 § 9.13, Appendix A.1
**What was checked:** Read `backend/repositories/model_version_repository.py` lines 100–115
**What was found:** Signature and SQL match. 1 function with 1 parameter; 0 style-aware variants. Callers at `pl_inference_service.py:96`, `ls_inference_service.py:139`, `wr_inference_service.py:269` all pass only `model_type`.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 9 — re-verified

## Claim 10: `model/features/feature_definitions.py` runtime state

**Claim:** ALL_FEATURES is populated to 73 at runtime; not orphaned; imported by 2 production paths.
**Document location:** v5 § 4.5 (cross-tier example reference)
**What was checked:** Runtime `len(ALL_FEATURES) == 73`; imports at `model/training/train.py:40` AND `backend/services/inference_service.py:28`.
**What was found:** Decomposed: 1 module + 2 import sites + 73 populated feature names.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 10 — re-verified

## Claim 11: `.gitignore` already contains deploy artifacts

**Claim:** Four artifacts already in `.gitignore`: `.frontend-bucket`, `.cf-distribution-id`, `cdk-outputs.json`, `frontend/.env.production`.
**Document location:** v5 § 7.14
**What was checked:** `cat .gitignore | tail -25`
**What was found:** All four present in the "Deployment artifacts (machine-specific)" block.

Decomposed: 4 artifacts named + 4 lines in the relevant gitignore block + 1 section comment = 5 lines.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 11 — re-verified. Tony ratified the v3 reframing in the v4 cycle (operator memory).

## Claim 12: Deploy script artifact writes

**Claim:** `scripts/deploy-backend.sh:243` writes `.frontend-bucket`; line 262 writes `.cf-distribution-id`; line 229 writes `frontend/.env.production`.
**Document location:** v5 § 7.14
**What was checked:** `grep -nE "\\s>\\s|\\s>>\\s" scripts/deploy-backend.sh scripts/deploy-frontend.sh deploy_all.sh`
**What was found:** Confirmed at the cited lines.

Decomposed: 3 cited write lines, all in `deploy-backend.sh`. No other artifact writes beyond log redirects across the three deploy scripts.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 12 — re-verified

## Claim 13: DD bible line count

**Claim:** DD bible is 2,578 lines.
**Document location:** v5 § 1.2, § 3.2
**What was checked:** `wc -l /home/strakajagr/projects/dynasty-dugout/ARCHITECTURE_BIBLE.md`
**What was found:** 2578
**Survived:** Yes
**Action:** Inherited from v4 log Claim 13 — re-verified

## Claim 14: DD bible "What Was Fixed / Common Mistakes / Forbidden Patterns / Deprecated Fields" section heads

**Claim:** DD § 18 at L2160; § 19 at L2258; § 20 at L2394; § 21 at L2456.
**Document location:** v5 § 1.4
**What was checked:** `grep -nE "^## (18|19|20|21)\\." ARCHITECTURE_BIBLE.md`
**What was found:** All four section heads at the cited lines, with cited labels.

Decomposed: 4 section heads + 4 line numbers + 4 section names. Each mapping verified individually.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 14 — re-verified

## Claim 14b: DD bible canonical-object section numbers and lines

**Claim:** DD § 4 = "THE CANONICAL PLAYER OBJECT" at L590; § 4.5 = "CONTRACT, SALARY, AND KEEPER RULES" at L800; § 5 = "THE CANONICAL LEAGUE OBJECT" at L1365; § 10 = "PRICING ENGINE" at L1657.
**Document location:** v5 § 1.4
**What was checked:** `grep -nE "^## (4\\.|5\\.|10\\.)" ARCHITECTURE_BIBLE.md`
**What was found:** All four section heads at the cited lines.

Decomposed: 4 section heads + 4 line numbers + 4 canonical-object names. Note: § 4.5 is labeled "CONTRACT, SALARY, AND KEEPER RULES" in DD; v3/v4/v5 prose refers to it as "Financial" because the contract/salary/keeper rules are the canonical financial domain in DD. Disclosure preserved.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 14b — re-verified

## Claim 15: Bug #28 line reference

**Claim:** Bug #28 manifests at `backend/services/data_sources/hrn_scraper.py:802-804` in `parse_payout(N)` calls.
**Document location:** v5 § 1.2, Appendix A.5
**What was checked:** Read lines 795–815 of `hrn_scraper.py`
**What was found:** Lines 802–804 contain `parse_payout(1)`, `parse_payout(2)`, `parse_payout(3)` for win/place/show.

Decomposed: 3 cited lines, 3 distinct payout fields, 3 parse_payout calls.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 15 — re-verified

## Claim 15b: Bug #28 silent-failure window

**Claim:** Bug #28 was discovered 2026-05-03; sharp regression beginning 2026-04-30; silent-failure window between regression and discovery is at least three days.
**Document location:** v5 § 1.2
**What was checked:** Read operator memory file
**What was found:** Discovery 2026-05-03; last clean 2026-04-29 (9/10 win-payout success); 2026-04-30 / 2026-05-01 / 2026-05-02 all 0/N.

Decomposed: 4 diagnostic dates; 1 last-clean (2026-04-29); 3 broken (2026-04-30 / 05-01 / 05-02); 1 discovery (2026-05-03). Window 2026-04-30 → 2026-05-03 = 3 calendar days minimum.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 15b — re-verified

## Claim 16: Legacy `predictions` table — A.4 example with broad-sweep decomposition

**Claim:** v5 maintains v4's decomposition for `prediction_router.py` (3 instantiations + 1 import = 4 references) and v5 adds the sum on `race_router.py` (1 instantiation + 1 import = 2 references). Legacy table created at `001_initial_schema.sql:327`; not dropped by migration 005; 6,600 rows live; readers in 4 router modules.
**Document location:** v5 Appendix A.4
**What was checked (re-verified 2026-05-04):**
1. `grep -n "PredictionRepository" backend/routers/prediction_router.py` → 4 lines: import (line 6) + 3 instantiations (lines 34, 61, 92)
2. `grep -nE "PredictionRepository" backend/routers/race_router.py` → 2 references: import on line 273 + instantiation on line 277
3. `grep -nE "DROP TABLE" backend/database/migrations/005_three_prediction_tables.sql` → 0 matches
4. Live `counts.predictions` → 6600
5. Direct SELECT readers: `dashboard_router.py:93,105` (2 sites) + `horse_router.py:66` (1 site)

**What was found:**
- prediction_router.py: 1 import (line 6) + 3 instantiations (34, 61, 92) = 4 references
- race_router.py: 1 import (line 273) + 1 instantiation (line 277) = 2 references
- Direct SELECTs: 2 in dashboard_router.py + 1 in horse_router.py = 3 SELECT sites
- Total reader surface: 4 + 2 + 3 = 9 distinct read paths
- predictions table CREATE at `001_initial_schema.sql:327` (verified)
- Live row count: 6,600

Decomposed: 6 reference sites (PredictionRepository) + 3 direct-SELECT sites = 9 read paths total.
**Survived:** Yes
**Action:** Modified from v4 log Claim 16. v5 adds explicit sum on race_router.py to match prediction_router.py's pattern. Per Tony's v5 cycle decision (broad sweep + match patterns).

## Claim 17: ECR image count in CDK assets bucket

**Claim:** `cdk-hnb659fds-container-assets-584812014683-us-east-1` has 5 images.
**Document location:** v5 § 2.3
**What was checked:** `aws ecr list-images --repository-name cdk-hnb659fds-container-assets-584812014683-us-east-1 --query 'length(imageIds)' --output text`
**What was found:** 5
**Survived:** Yes
**Action:** Inherited from v4 log Claim 17 — re-verified

## Claim 18: S3 bucket count

**Claim:** 4 EE-related S3 buckets.
**Document location:** v5 § 2.3
**What was checked:** `aws s3 ls | grep equine`
**What was found:** 4 buckets, all created 2026-03-15.

Decomposed: 4 buckets named in § 2.3.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 18 — re-verified

## Claim 19: Secrets Manager entries

**Claim:** 3 secrets, decomposed as 1 used (`db-credentials`) + 2 unused (`2captcha-api-key`, `brightdata-api-key`).
**Document location:** v5 § 2.3
**What was checked:** Secrets list + grep for consumers in backend/model/scripts.
**What was found:** 3 secrets; 0 hits for 2captcha or brightdata in Python code under those directories.

Decomposed: 3 secrets = 1 used + 2 unused (zero code consumers each).
**Survived:** Yes
**Action:** Inherited from v4 log Claim 19 — re-verified

## Claim 20: ECS task definition families

**Claim:** 5 ECS task families starting with `equine`.
**Document location:** v5 § 2.3
**What was checked:** `aws ecs list-task-definition-families`
**What was found:** equine-training, equine-training-daily-full, equine-training-manual, equine-training-pl, equine-training-win-prob.

Decomposed: 5 families; 2 missing-from-dump (equine-training, equine-training-win-prob).
**Survived:** Yes
**Action:** Inherited from v4 log Claim 20 — re-verified

## Claim 21: Phase duration arithmetic

**Claim:** Per-phase highs sum to 19 weeks (4+8+2+2+3); lows sum to 9 weeks (2+4+1+1+1).
**Document location:** v5 § 3.7
**What was checked:** Re-summed per-phase ranges from §§ 3.1–3.5.
**What was found:** Low: 2+4+1+1+1 = 9. High: 4+8+2+2+3 = 19.

Decomposed: 5 per-phase ranges; both endpoints checked separately.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 21 — re-verified

## Claim 22: Git working-tree state (UPDATED v5 — broad-sweep precision)

**Claim:** EE working tree currently has 103 entries, decomposed as 74 untracked + 29 modified. Last commit `2a3d758` 2026-03-15.
**Document location:** v5 § 1.1, § 1.3
**What was checked (re-verified 2026-05-04):**
1. `git log -1 --format="%h %ad %s" --date=short` → `2a3d758 2026-03-15 Widen VARCHAR columns and isolate per-race DB connections`
2. `git status --porcelain | wc -l` → 103
3. `git status --porcelain | awk '{print $1}' | sort | uniq -c` → `74 ??` (untracked) + `29 M` (modified)

**What was found:**
- Last commit hash: 2a3d758
- Last commit date: 2026-03-15
- Total entries: 103
- Decomposed: 74 untracked + 29 modified = 103 (sum verified)

**Survived:** Yes
**Action:** Modified from v4 log Claim 22. v4 phrasing "103 modified-or-untracked entries (modified + untracked aggregate)" was an aggregate that didn't decompose. v5 decomposes explicitly per Tony's v5 cycle decision (broad sweep). Status-code mapping: `??` is the porcelain code for untracked; `M ` (M followed by space) is the code for modified-and-not-staged-or-staged-and-modified-since.

## Claim 23: DD bible structural facts

**Claim:** DD is multi-runtime (Lambda + Node.js EC2 draft server + worker_package + frontend) with multiple canonical objects.
**Document location:** v5 § 1.4
**What was checked:** `grep -nE "draft-server|EC2|websocket" ARCHITECTURE_BIBLE.md` plus § 4 / § 4.5 / § 5 / § 10 verifications in Claim 14b.
**What was found:** EC2 references at L418, L1768, L2161; canonical objects at the four section numbers per Claim 14b.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 23 — re-verified

## Claim 24: "14 Gonzo Sauce features" count (re-verified v5)

**Claim:** EE has 14 Gonzo Sauce features factored to a single shared module `model/shared/gonzo_features.py`.
**Document location:** v5 § 1.2, § 9.11, A.3
**What was checked:** Read `model/shared/gonzo_features.py` docstring (lines 1–28) and `grep "^def compute_gonzo"`.
**What was found:** Docstring decomposes Speed (4) + Trajectory (7) + Class (3) = 14 features. Three public functions at lines 290 / 400 / 477.

Decomposed: 4 Speed + 7 Trajectory + 3 Class = 14 features; 3 public functions; 1 module file.
**Survived:** Yes
**Action:** Inherited from v4 log Claim 24 — re-verified

## Claim 25: "Three calibration bugs in one week" claim

**Claim:** v5 § 1.2 states "three calibration bugs in one week traced to silent code-path drift between training and inference."
**Document location:** v5 § 1.2, A.3
**What was checked:** Read `model/shared/gonzo_features.py:7-11`
**What was found:** Docstring text "three distinct bugs this week traced to code-path drift between training and inference" — verbatim attribution.

Decomposed: 1 source (file docstring); 1 verbatim quote; attribution context "post-Bug #15."
**Survived:** Yes
**Action:** Inherited from v4 log Claim 25 — re-verified

## Claim 26: Calibration bypass at `wr_inference_service.py` (CORRECTED v5 — line range)

**Claim:** v5 cites the calibration bypass at `wr_inference_service.py:616-626`, decomposed as 10-line comment block (lines 616–625) + 1-line bypass operation (line 626). v4 incorrectly cited "616-628"; v5 corrects.
**Document location:** v5 § 1.2, § 9.12, A.2, plus this log Claim 26
**What was checked (re-verified 2026-05-04):** Read lines 614–632 of `backend/services/wr_inference_service.py`
**What was found:**
- Line 614: previous code (`pp_counts` dict comprehension)
- Line 615: blank
- **Lines 616–625: comment block (10 lines)** — opens with "── Calibration BYPASS (BUG #15 + BUG #24) ──" and explicitly states "All styles (including gonzo_sauce) bypass calibration at inference tonight"
- **Line 626: bypass operation** — `handicapping_probs = ranker_probs.copy()`
- Line 627: blank
- Line 628: start of unrelated "── Patch (β): 0-PP override AFTER calibration ──" comment block
- Lines 629+: 0-PP override comment continues

Decomposed: bypass-related code spans lines 616–626 = 10-line comment block + 1-line bypass operation = 11 lines total. Lines 627–628 are blank + start of a different (post-calibration) comment block; v4's "616-628" range erroneously included those 2 lines. v5 corrects to 616–626.
**Survived:** Yes (after correction)
**Action:** Modified from v4 log Claim 26. v4 cited "lines 616–628" (off by 2 lines on the upper bound); v5 corrects to 616–626 with explicit 10+1 line decomposition. All main-doc references (§ 1.2, § 9.12, A.2) updated to match.

## Claim 27: `gonzo_features.py` import sites

**Claim:** `model/shared/data_loader.py:45` imports gonzo_features as `from shared.gonzo_features import (`; `backend/services/feature_engineering_service.py:16` imports as `from model.shared.gonzo_features import (`. Different qualified names.
**Document location:** v5 Appendix A.3
**What was checked:** `grep -n "gonzo_features" model/shared/data_loader.py backend/services/feature_engineering_service.py`
**What was found:** Both forms present at the cited lines.

Decomposed: 2 import sites; 1 module imported; 2 different qualified import names (implies different `sys.path` configurations in training vs inference contexts).
**Survived:** Yes
**Action:** Inherited from v4 log Claim 27 — re-verified

## Claim 28 (NEW v5): Derby Day 2026 counterfactual loss claim

**Claim:** v5 § 3.2.1 cites Derby Day 2026 evidence: "counterfactual loss roughly $-108 against operator's actual roughly $-150; no model picked the Derby winner; gonzo style produced predictions identical to general style at rank=1."
**Document location:** v5 § 3.2.1
**What was checked:**
1. Search operator memory directory for Derby-related files: `ls ~/.claude/projects/-home-strakajagr/memory/ | grep -i derby` → no specific Derby file
2. Search session logs: `grep -nE "(derby|Derby|counterfactual|108|150|gonzo.*general|rank=1)" docs/sessions/SESSION_005.md` → 1 hit on "Derby Day Easter Egg" (UI styling, not analysis)
3. Operator memory file `equine-equalizer-bug-28-hrn-scraper.md` references "Derby Day counterfactual analysis" but does NOT cite specific dollar amounts.
4. Code comment at `wr_inference_service.py:622` references "Wonder Dean JPN at #1 in Derby smoke test" — corroborates the gonzo-vs-general rank-1 issue but not the dollar amounts.

**What was found:**
- The specific dollar amounts (~$-108 and ~$-150) cannot be verified against any primary source (code, AWS, DB, operator memory file, session logs) accessible at audit time.
- The "no model picked the Derby winner" and "gonzo == general at rank=1" claims have indirect corroboration from the wr_inference_service.py:622 code comment ("Wonder Dean JPN at #1 in Derby smoke test").
- The lived-experience direction of the claim (model gallery is underperforming; re-architecture warranted) is operator-stated framing for the v5 cycle's drafting spec.

**Survived:** Partial. **Source authority:** operator-stated (per § 4.5 tier 5). The forcing-function rationale in § 3.2.1 does not depend on the exact dollar amounts being verified at primary-source granularity — it depends on the operator's lived-experience claim. v5 § 3.2.1 prose explicitly flags this: "operator-stated; not independently verified at primary-source granularity, but the lived-experience direction is the operative fact for this design constraint."
**Action:** New in v5. Recorded with explicit operator-stated annotation per the no-fabrication discipline (§ 8.6). Phase 1 audits may verify these amounts against operator's bet records or Derby-day session log if such evidence exists; until then, treat as operator-stated rather than verified.

---

## Verification summary

**Total claims documented:** 28 (27 inherited from v4 + 1 new for Derby Day; 3 modified for v5 broad-sweep precision: Claims 7, 22, 26 — Claim 16 also updated for parallel decomposition)
**Survived as-is (re-verified live 2026-05-04):** 23
**Modified for v5 broad-sweep precision:** 4 (Claim 7 model registry decomposed; Claim 16 race_router.py sum added; Claim 22 working-tree decomposed; Claim 26 line range corrected and decomposed)
**New v5 claim:** 1 (Claim 28 — Derby Day counterfactual, operator-stated annotation)
**Dropped:** 0
**Architectural questions surfaced:** 0 new in v5 cycle. Tony's three architectural decisions in this cycle (precision-rule scope: broad; tier-migration: pre-hoc; Layer 1 form: deferred) are all integrated into the main doc.

**Verification log precision rule scope (locked v5 per Tony's Option B):**

The rule applies broadly — to any aggregable count anywhere in a Tier 3 document, not only to code-reference counts that look like the v3 BLOCKER pattern. v5 demonstrates application across:
- Code-reference counts (Claim 16: prediction_router.py and race_router.py sums)
- Working-tree status (Claim 22: 74 untracked + 29 modified = 103)
- Model registry (Claim 7: 88 = 45 active + 43 inactive)
- EventBridge rules (Claim 3: 13 = 10 ENABLED + 3 DISABLED)
- Lambdas (Claim 1: 8 = 5 Active + 3 INACTIVE)
- Migrations (Claim 5: 12 = 11 unique + 1 duplicate at sequence 005)
- Calibration bypass code (Claim 26: 11 lines = 10 comment + 1 operation)
- Secrets (Claim 19: 3 = 1 used + 2 unused)

When in doubt, decompose; over-decomposition costs verification-log length but never costs accuracy.

**Methodology-interpolation rule (operative immediately, formal codification in AUDIT_METHODOLOGY.md):**

CC does not invent binary tests, cadence rules, completeness criteria, or scoring rubrics that Tony has not explicitly ratified. v5 corrects v4's instance (§ 9.13 "Removing any one converts to FORBIDDEN" → descriptive prose). v5 also drops v4's surviving "3-5 per heavy session, not 20" cadence in § 7.10 — a milder echo of the same pattern. The rule is now in § 6.1 as a CC-role bullet.

**No fabricated content in v5.** Every concrete claim has a verification entry above with decomposed counts. Every operator-stated claim is explicitly annotated as such.
