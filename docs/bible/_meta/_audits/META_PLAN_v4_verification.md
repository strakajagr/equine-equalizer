# META_PLAN v4 — Verification Log

**Document:** META_PLAN_v4_verification
**Companion to:** META_PLAN.md v4
**Author:** CC (drafting under verification discipline)
**Date:** 2026-05-04
**Purpose:** Per-claim verification record. Every factual claim about EE in v4 has an entry here with evidence. v4's lesson over v3: counts must be **decomposed** so a downstream reader cannot compress them with judgment. v3's BLOCKER (A.4 "4 instantiations") originated in a v3 log entry that read "4 references including the import" — phrasing that allowed compression. v4 entries are written with that compression-resistance in mind.

**Verification methodology:**
- "Live AWS" = `aws` CLI against operator's account 584812014683
- "Live API" = HTTPS request against `https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com`
- "Codebase" = file read against working tree at `/home/strakajagr/projects/equine-equalizer/`
- "Runtime test" = Python interpreter executing the actual module
- "Operator memory" = file read against `~/.claude/projects/-home-strakajagr/memory/<filename>.md`
- "Inherited from v3 log Claim N — re-verified [date]" = entry imported from `META_PLAN_v3_verification.md` and re-run; value confirmed unchanged

**Verification log precision rule (locked v4):**
Counts are decomposed into definitions / instantiations / imports / uses, never aggregated as "N references including..." that can be compressed by a reader. Anything aggregable is shown both as components and as a sum.

---

## Claim 1: Lambda function count

**Claim:** EE has 8 Lambda functions.
**Document location:** v4 § 1.3, § 2.3
**What was checked (re-verified 2026-05-04):** `aws lambda list-functions --query 'Functions[?starts_with(FunctionName, \`equine\`)].FunctionName' --output text`
**What was found:** 8 functions: equine-feature-engineering, equine-inference, equine-ingestion, equine-ls-inference, equine-nyra-workouts, equine-pl-inference, equine-results, equine-wr-inference
**Survived:** Yes
**Action:** Inherited from v3 log Claim 1 — re-verified 2026-05-04

## Claim 2: INACTIVE Lambda count and identities

**Claim:** Three Lambda functions are INACTIVE: `equine-ingestion`, `equine-feature-engineering`, `equine-results`. Five are Active: `equine-inference`, `equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference`, `equine-nyra-workouts`.
**Document location:** v4 § 2.3
**What was checked (re-verified 2026-05-04):** `aws lambda get-function --function-name <fn> --query 'Configuration.[State,StateReason]' --output text` for each of the 8 functions
**What was found:**
- equine-feature-engineering: Inactive | The function is trying to use a deleted image.
- equine-inference: Active | None
- equine-ingestion: Inactive | The function is trying to use a deleted image.
- equine-ls-inference: Active | None
- equine-nyra-workouts: Active | None
- equine-pl-inference: Active | None
- equine-results: Inactive | The function is trying to use a deleted image.
- equine-wr-inference: Active | None

Decomposed: 3 INACTIVE + 5 Active = 8 total.
**Survived:** Yes
**Action:** Inherited from v3 log Claim 2 — re-verified 2026-05-04

## Claim 3: EventBridge rule count and disabled count

**Claim:** 13 EventBridge rules total, 3 DISABLED + 10 ENABLED.
**Document location:** v4 § 1.3, § 2.3
**What was checked (re-verified 2026-05-04):** `aws events list-rules --name-prefix equine --query 'Rules[].[Name,State]' --output text`
**What was found:** 13 rules. ENABLED (10): equine-angle-stats-nightly, equine-daily-retrain-full, equine-fetch-results-nightly, equine-ingestion-daily, equine-ls-inference-daily, equine-nyra-workouts-daily, equine-pl-inference-daily, equine-results-daily, equine-weekly-retrain-wr, equine-wr-inference-daily. DISABLED (3): equine-feature-engineering-daily, equine-inference-daily, equine-weekly-retrain-pl.

Decomposed: 10 ENABLED + 3 DISABLED = 13 total.
**Survived:** Yes
**Action:** Inherited from v3 log Claim 3 — re-verified 2026-05-04 with full live names (v3 log dropped the `equine-` prefix; v4 records the full names since that's what AWS actually returns).

## Claim 4: Database table count

**Claim:** 14 tables + 1 materialized view.
**Document location:** v4 § 1.3, § 2.3
**What was checked:** `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql | sed 's/CREATE TABLE \(IF NOT EXISTS \)\?//' | awk '{print $1}' | sort -u`
**What was found:** 14 unique table names: entries, horses, jockeys, ls_predictions, model_versions, past_performances, pl_predictions, predictions, races, results, tracks, trainers, workouts, wr_predictions. Plus 1 `CREATE MATERIALIZED VIEW IF NOT EXISTS trainer_stats` in migration 008.

Decomposed: 14 tables + 1 matview = 15 schema objects.
**Survived:** Yes
**Action:** Inherited from v3 log Claim 4 — re-verified

## Claim 5: Migration filename format and duplicate-005 case

**Claim:** All 12 existing migrations use `NNN_short_description.sql` format (no date in name); 005 is duplicated.
**Document location:** v4 § 7.12
**What was checked (re-verified 2026-05-04):** `find backend/database/migrations -name "*.sql" | sort`
**What was found:** 12 files: 001_initial_schema.sql, 002_fix_race_type_length.sql, 003_widen_varchar_columns.sql, 004_backfill_running_style.sql, **005_backfill_pace_delta.sql**, **005_three_prediction_tables.sql** (duplicate-005), 006_backfill_early_pace_pressure.sql, 007_backfill_trainer_name.sql, 008_create_trainer_stats.sql, 009_backfill_pace_delta_v2.sql, 010_ls_predictions_first_class.sql, 011_wr_predictions_unique_fix.sql.

Decomposed: 12 migration files; 11 unique sequence numbers; sequence 005 has 2 files.
**Survived:** Yes
**Action:** Inherited from v3 log Claim 5 — re-verified

## Claim 6: Migration runner mechanism

**Claim:** `migrate.py` tracks applied migrations by filename in a `schema_migrations` table.
**Document location:** v4 § 7.12
**What was checked:** Read `backend/database/migrations/migrate.py` lines 44–95
**What was found:** Schema creation includes `filename VARCHAR(255) UNIQUE NOT NULL`; `get_applied_migrations(conn)` returns set of filenames; `run_migrations` iterates `sorted(... .sql files)` and skips filenames in the applied set; on success, `INSERT INTO schema_migrations (filename) VALUES (%s)`.
**Survived:** Yes
**Action:** Inherited from v3 log Claim 6 — re-verified

## Claim 7: Model registry counts (88 total, 45 active)

**Claim:** 88 entries in `model_versions`; 45 simultaneously active.
**Document location:** v4 § 1.3, § 9.13, A.1
**What was checked (re-verified 2026-05-04):** `curl https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com/dashboard/metrics`, parse `model_history`; count entries where `is_active == True`
**What was found:** total: 88, active: 45.

Decomposed: 45 is_active=TRUE + 43 is_active=FALSE = 88 total.
**Survived:** Yes
**Action:** Inherited from v3 log Claim 7 — re-verified

## Claim 8: API Gateway route count

**Claim:** 41 routes on API Gateway v2 `gb5qlfy10h`.
**Document location:** v4 § 8.5 (referenced in route-behavior context)
**What was checked (re-verified 2026-05-04):** `aws apigatewayv2 get-routes --api-id gb5qlfy10h --query 'Items[].RouteKey' --output text | tr '\t' '\n' | wc -l` → 41. (Note: `--query 'length(Items)'` returns paginated values "25" and "16"; 25 + 16 = 41, matching the route-key count.)
**What was found:** 41 routes
**Survived:** Yes
**Action:** Inherited from v3 log Claim 8 — re-verified with explicit decomposition of paginated response.

## Claim 9: `get_active_model_by_type` signature and SQL

**Claim:** Function takes only `model_type: str`. Body is `WHERE is_active = true AND model_type = %s LIMIT 1`. No `_and_style` variant exists.
**Document location:** v4 § 9.13, Appendix A.1
**What was checked (re-verified 2026-05-04):** `grep -n "get_active_model" backend/repositories/model_version_repository.py` and read lines 100–115
**What was found:**
```python
def get_active_model_by_type(
    self, model_type: str
) -> Optional[ModelVersion]:
    """
    Get the active model for a specific type.
    model_type must be 'wr', 'pl', or 'ls'.
    Returns None if no active model of that type.
    """
    row = self._query_one(
        """SELECT * FROM model_versions
           WHERE is_active = true
           AND model_type = %s
           LIMIT 1""",
        (model_type,)
    )
```

Decomposed: 1 function with 1 parameter (`model_type`); 0 style-aware variants.

Callers (verified): `pl_inference_service.py:96`, `ls_inference_service.py:139`, `wr_inference_service.py:269` — all pass only `model_type`.
**Survived:** Yes
**Action:** Inherited from v3 log Claim 9 — re-verified

## Claim 10: `model/features/feature_definitions.py` runtime state

**Claim:** ALL_FEATURES is populated to 73 at runtime; not orphaned; imported by 2 production paths.
**Document location:** v4 § 4.5 (cross-tier example)
**What was checked (re-verified 2026-05-04):**
1. Runtime: `cd /home/strakajagr/projects/equine-equalizer && python3 -c "from model.features.feature_definitions import ALL_FEATURES, FEATURE_COUNT; print(len(ALL_FEATURES), FEATURE_COUNT)"`
2. Import grep: `grep -rn "from.*model.features.feature_definitions" --include="*.py"`
**What was found:**
1. Runtime: `73 73` — `len(ALL_FEATURES) == 73`, `FEATURE_COUNT == 73`
2. Imports: 2 lines — `model/training/train.py:40` AND `backend/services/inference_service.py:28`

Decomposed: 1 module + 2 import sites + 73 populated feature names.
**Survived:** Yes
**Action:** Inherited from v3 log Claim 10 — re-verified

## Claim 11: `.gitignore` already contains deploy artifacts

**Claim:** `.frontend-bucket`, `.cf-distribution-id`, `cdk-outputs.json`, `frontend/.env.production` are all already in `.gitignore`.
**Document location:** v4 § 7.14
**What was checked (re-verified 2026-05-04):** `cat /home/strakajagr/projects/equine-equalizer/.gitignore | tail -25`
**What was found:** End of file contains:
```
# Deployment artifacts (machine-specific)
.frontend-bucket
.cf-distribution-id
cdk-outputs.json
frontend/.env.production
```
**Survived:** Yes
**Action:** Inherited from v3 log Claim 11 — re-verified. v3 cycle surfaced that v2 audit Q2.2 was wrong; Tony ratified the v3 reframing in the v4 cycle (operator memory: per Tony's verbatim "Reframing is correct because facts on the ground decided it").

## Claim 12: Deploy script artifact writes

**Claim:** `scripts/deploy-backend.sh:243` writes `.frontend-bucket`; line 262 writes `.cf-distribution-id`; line 229 writes `frontend/.env.production`.
**Document location:** v4 § 7.14
**What was checked:** `grep -nE "\\s>\\s|\\s>>\\s" scripts/deploy-backend.sh scripts/deploy-frontend.sh deploy_all.sh`
**What was found:** Confirmed at the cited lines (no other artifact writes beyond log redirects).
**Survived:** Yes
**Action:** Inherited from v3 log Claim 12 — re-verified

## Claim 13: DD bible line count

**Claim:** DD bible is 2,578 lines.
**Document location:** v4 § 1.2, § 3.2
**What was checked (re-verified 2026-05-04):** `wc -l /home/strakajagr/projects/dynasty-dugout/ARCHITECTURE_BIBLE.md`
**What was found:** 2578
**Survived:** Yes
**Action:** Inherited from v3 log Claim 13 — re-verified

## Claim 14: DD bible section names — What Was Fixed / Common Mistakes / Forbidden Patterns / Deprecated Fields

**Claim:** DD § 18 = "What Was Fixed — Do Not Revert" at L2160; § 19 = "Common Mistakes to Avoid" at L2258; § 20 = "Forbidden Patterns (locked 2026-04-21)" at L2394; § 21 = "Deprecated Fields (Phase B Cleanup Queue)" at L2456.
**Document location:** v4 § 1.4 (line numbers cited in prose)
**What was checked (re-verified 2026-05-04):** `grep -nE "^## (18|19|20|21)\\." ARCHITECTURE_BIBLE.md`
**What was found:**
- L2160: `## 18. WHAT WAS FIXED — DO NOT REVERT`
- L2258: `## 19. COMMON MISTAKES TO AVOID`
- L2394: `## 20. FORBIDDEN PATTERNS (locked 2026-04-21)`
- L2456: `## 21. DEPRECATED FIELDS (PHASE B CLEANUP QUEUE)`
**Survived:** Yes
**Action:** Inherited from v3 log Claim 14 — re-verified, line numbers added to v4 § 1.4 to make the citation specific

## Claim 14b (NEW in v4): DD bible canonical-object section numbers and lines

**Claim:** DD § 4 = "THE CANONICAL PLAYER OBJECT" at L590; § 4.5 = "CONTRACT, SALARY, AND KEEPER RULES" (the "Financial" canonical area) at L800; § 5 = "THE CANONICAL LEAGUE OBJECT" at L1365; § 10 = "PRICING ENGINE" at L1657. v4 § 1.4 cites these section-number-to-canonical-object mappings.
**Document location:** v4 § 1.4
**What was checked:** `grep -nE "^## (4|5|10)\\." /home/strakajagr/projects/dynasty-dugout/ARCHITECTURE_BIBLE.md`
**What was found:**
- L590: `## 4. THE CANONICAL PLAYER OBJECT`
- L800: `## 4.5 CONTRACT, SALARY, AND KEEPER RULES`
- L1365: `## 5. THE CANONICAL LEAGUE OBJECT`
- L1657: `## 10. PRICING ENGINE`

Decomposed: 4 section heads, 4 line numbers, 4 canonical-object names. Each mapping verified individually.
**Survived:** Yes
**Action:** New in v4 (closes v3 audit Question 1.5 — "DD section numbers cited without verification entry"). Note: § 4.5 is labeled "CONTRACT, SALARY, AND KEEPER RULES" in DD; v3 + v4 prose refer to it as "Financial" because the contract/salary/keeper rules are the canonical financial domain in DD. v4 § 1.4 spells it out: "Contract-Salary-Keeper 'Financial'" to bridge the labels honestly.

## Claim 15: Bug #28 line reference

**Claim:** HRN scraper Bug #28 manifests at `backend/services/data_sources/hrn_scraper.py:802-804` in `parse_payout(N)` calls.
**Document location:** v4 § 1.2, Appendix A.5
**What was checked:** Read lines 795–815 of `hrn_scraper.py`
**What was found:** Lines 802–804:
```python
'win_payout':      parse_payout(1),
'place_payout':    parse_payout(2),
'show_payout':     parse_payout(3),
```
**Survived:** Yes
**Action:** Inherited from v3 log Claim 15 — re-verified. v4 § 1.2 also notes "no in-code Bug #28 marker exists yet" — verified by grep "Bug #28" returning zero hits in `hrn_scraper.py`.

## Claim 15b (NEW in v4): Bug #28 timing — silent-failure window

**Claim:** Bug #28 was discovered 2026-05-03; sharp regression beginning 2026-04-30; silent-failure window between regression and discovery is at least three days.
**Document location:** v4 § 1.2
**What was checked:** Read operator memory file `~/.claude/projects/-home-strakajagr/memory/equine-equalizer-bug-28-hrn-scraper.md`
**What was found:** Memory file states "discovered 2026-05-03" in the header. Diagnostic table reads:
- 2026-04-25: 9/9 win_payout ✅, 9/9 dd_payout ✅
- 2026-04-29: 9/10 win_payout ✅, 8/10 dd_payout
- **2026-04-30: 0/7 ❌, 0/7 ❌**
- **2026-05-01: 0/11 ❌, 0/11 ❌**
- **2026-05-02: 0/12 ❌, 0/12 ❌**

Decomposed: 4 diagnostic dates; 1 last-clean date (2026-04-29); 3 fully-broken dates (2026-04-30 / 05-01 / 05-02); 1 discovery date (2026-05-03). Window from regression to discovery: 2026-04-30 → 2026-05-03 = 3 calendar days minimum. v4 § 1.2 states "at least three days" matching this lower bound.
**Survived:** Yes
**Action:** New in v4 (closes v3 audit Question 1.5 / Q1 — "Bug #28 'failed silently for at least three days' not in verification log").

## Claim 16: Legacy `predictions` table — replacement for A.4 example (CORRECTED in v4)

**Claim:** The legacy `predictions` table exists at `001_initial_schema.sql:327`; was NOT dropped by migration 005 (zero `DROP TABLE` statements in the migration); has 6,600 rows per dashboard `counts.predictions`; has active callers via `prediction_router.py` and `race_router.py` and direct-SELECT readers in `dashboard_router.py` and `horse_router.py`.

**v4 correction over v3:** count of `PredictionRepository` references in `prediction_router.py` is precisely:
- **3 instantiations** at lines 34, 61, 92 (verified via `grep -n "PredictionRepository(" backend/routers/prediction_router.py` returning exactly those three lines plus the import)
- **1 import** at line 6 (`PredictionRepository` listed in the from-import block)
- **= 4 references total**

v3 log entry compressed this as "4 references including the import," which the v3 main doc inflated to "4 instantiations." v4 entry decomposes the count so no compression is possible.

**Document location:** v4 Appendix A.4
**What was checked (re-verified 2026-05-04):**
1. `grep -n "PredictionRepository" backend/routers/prediction_router.py` → 4 lines: `:6:    PredictionRepository`, `:34:            repo = PredictionRepository(conn)`, `:61:            repo = PredictionRepository(conn)`, `:92:            repo = PredictionRepository(conn)`
2. `grep -nE "DROP TABLE" backend/database/migrations/005_three_prediction_tables.sql` → no matches
3. `grep -nE "CREATE TABLE.*predictions" backend/database/schema/schema.sql backend/database/migrations/001_initial_schema.sql` → both files have `CREATE TABLE predictions (` at line 327
4. `curl /dashboard/metrics` → `counts.predictions: 6600`
5. `grep -n "PredictionRepository" backend/routers/race_router.py` → 1 import (line 273) + 1 instantiation (line 277) = 2 references; v4 A.4 records as "1 instantiation, plus 1 import on line 273"
6. `grep -n "FROM predictions" backend/routers/dashboard_router.py backend/routers/horse_router.py` → `dashboard_router.py:93,105` and `horse_router.py:66`

**What was found:**
- predictions table CREATE: `001_initial_schema.sql:327` and `schema/schema.sql:327`
- DROP TABLE in migration 005: 0
- Live `counts.predictions`: 6600
- prediction_router.py: 1 import (line 6) + 3 instantiations (34, 61, 92) = 4 references
- race_router.py: 1 import (line 273) + 1 instantiation (line 277) = 2 references
- dashboard_router.py: 2 direct SELECT (lines 93, 105)
- horse_router.py: 1 direct SELECT (line 66)

Decomposed total reader surface: 6 reference sites (4 + 2) + 3 direct SELECTs = 9 distinct read paths.
**Survived:** Yes
**Action:** Modified from v3 log Claim 16. v3 phrasing "4 references including the import" → v4 phrasing "1 import + 3 instantiations = 4 references." This closes the BLOCKER F1 root cause: the loose phrasing in v3 enabled the main-doc inflation.

## Claim 17: ECR image count in CDK assets bucket

**Claim:** `cdk-hnb659fds-container-assets-584812014683-us-east-1` has 5 images.
**Document location:** v4 § 2.3
**What was checked (re-verified 2026-05-04):** `aws ecr list-images --repository-name cdk-hnb659fds-container-assets-584812014683-us-east-1 --query 'length(imageIds)' --output text`
**What was found:** 5
**Survived:** Yes
**Action:** Inherited from v3 log Claim 17 — re-verified

## Claim 18: S3 bucket count

**Claim:** 4 EE-related S3 buckets.
**Document location:** v4 § 2.3
**What was checked (re-verified 2026-05-04):** `aws s3 ls | grep equine`
**What was found:** 4 buckets, all created 2026-03-15: equine-frontend, equine-model-artifacts, equine-processed-data, equine-raw-data
**Survived:** Yes
**Action:** Inherited from v3 log Claim 18 — re-verified

## Claim 19: Secrets Manager entries

**Claim:** 3 EE-related secrets; 2 of the 3 (`2captcha-api-key`, `brightdata-api-key`) have zero code consumers.
**Document location:** v4 § 2.3
**What was checked (re-verified 2026-05-04):**
1. `aws secretsmanager list-secrets --query 'SecretList[?starts_with(Name, \`equine\`)].Name' --output text`
2. `grep -rn "2captcha\|brightdata" backend model scripts --include="*.py"`
**What was found:**
1. equine-equalizer/db-credentials, equine-equalizer/2captcha-api-key, equine-equalizer/brightdata-api-key
2. Zero hits in backend/model/scripts Python.

Decomposed: 3 secrets (1 used + 2 unused).
**Survived:** Yes
**Action:** Inherited from v3 log Claim 19 — re-verified

## Claim 20: ECS task definition families

**Claim:** 5 ECS task families starting with `equine`. Dump (§ 6.2) listed 3.
**Document location:** v4 § 2.3 (mentioned generically as "ECS Fargate training fleet")
**What was checked (re-verified 2026-05-04):** `aws ecs list-task-definition-families --query 'families[?starts_with(@, \`equine\`)]' --output text`
**What was found:** equine-training, equine-training-daily-full, equine-training-manual, equine-training-pl, equine-training-win-prob

Decomposed: 5 families; 2 missing-from-dump (equine-training, equine-training-win-prob).
**Survived:** Yes — reveals dump incompleteness (Phase 1 ML Stack Bible to enumerate active vs retired)
**Action:** Inherited from v3 log Claim 20 — re-verified

## Claim 21: Phase duration arithmetic

**Claim:** Per-phase highs sum to 19 weeks (4+8+2+2+3); lows sum to 9 (2+4+1+1+1).
**Document location:** v4 § 3.7
**What was checked:** Re-summed per-phase ranges from §§ 3.1–3.5: Phase 0 (2–4) + Phase 1 (4–8) + Phase 2 (1–2) + Phase 3 (1–2) + Phase 4 (1–3)
**What was found:** Low: 2+4+1+1+1 = 9. High: 4+8+2+2+3 = 19.

Decomposed: 5 per-phase ranges, summed at endpoints, both endpoints checked separately.
**Survived:** Yes
**Action:** Inherited from v3 log Claim 21 — re-verified arithmetic

## Claim 22: Git state confirms uncommitted-deploy practice (UPDATED in v4)

**Claim:** EE last commit is one March 2026 entry; production code has been deployed without commits since then.

**v4 update:** `git status --porcelain` count of working-tree entries is **103 lines** (re-verified 2026-05-04). v3 log Claim 22 said "28+ modified files plus untracked Dockerfile.ls-inference" — technically still satisfied (103 ≥ 28) but the precise current count is 103. v4 § 1.1 and § 1.3 cite "103 modified-or-untracked entries" instead of "28+."

**Document location:** v4 § 1.1 (Motivation), § 1.3 (structural problem)
**What was checked (re-verified 2026-05-04):**
- `git log -1 --format="%h %ad %s" --date=short` → `2a3d758 2026-03-15 Widen VARCHAR columns and isolate per-race DB connections`
- `git status --porcelain | wc -l` → `103`
**What was found:** Same last-commit line; 103 working-tree entries (modified + untracked aggregate).
**Survived:** Yes
**Action:** Updated from v3 log Claim 22. The "+" in v3's "28+" was a precision-resistant phrasing; v4 records the exact current value with the date of measurement.

## Claim 23: DD bible structural facts cited in Motivation

**Claim:** DD is multi-runtime (Lambda + Node.js EC2 draft server + worker_package + frontend) with multiple canonical objects.
**Document location:** v4 § 1.4
**What was checked:** `grep -nE "draft-server|EC2|websocket" ARCHITECTURE_BIBLE.md` plus the section heads (verified separately in Claim 14b)
**What was found:**
- L418: `| Draft Server | Node.js / Express / Socket.io | Runs on EC2, draft.dynasty-dugout.com |`
- L1768: `Draft Server (EC2 Node.js/Express/Socket.io — in-memory state + DB persistence)`
- L2161: `├── draft-server/                      # Node.js WebSocket server (EC2)`
- Sections § 4 / § 4.5 / § 5 / § 10 verified at exact lines per Claim 14b.
**Survived:** Yes
**Action:** Inherited from v3 log Claim 23 — re-verified, with section-number mapping now formalized in Claim 14b.

## Claim 24 (NEW in v4): "14 Gonzo Sauce features" count

**Claim:** EE has 14 Gonzo Sauce features factored to a single shared module `model/shared/gonzo_features.py`.
**Document location:** v4 § 1.2, § 9.11, A.3
**What was checked:** Read `model/shared/gonzo_features.py` lines 1–28 (module docstring) and grep for `^def compute_gonzo`
**What was found:** Docstring at lines 13–26 enumerates the public API and feature names:
```
Public API (3 functions):
  compute_gonzo_speed_features(horse_hist, row, workouts_by_horse, par_dict)
  compute_gonzo_trajectory_features(horse_hist, row)
  compute_gonzo_class_features(horse_hist, row)

Each returns a dict with the keys for its feature group:
  Speed (4):       speed_at_distance_recent_weighted, speed_at_distance_best_18mo,
                   noteworthy_workout_recent_14d, noteworthy_workout_count_30d
  Trajectory (7):  route_expand_count, route_held_count, route_erode_count,
                   route_collapse_count, route_charge_short_count,
                   route_avg_delta, is_stretching_out
  Class (3):       class_tier_at_today_level_count_18mo,
                   class_tier_in_money_rate_at_or_above,
                   class_tier_avg_position_at_or_above
```

Grep `^def compute_gonzo` returns 3 functions.

Decomposed: 4 Speed + 7 Trajectory + 3 Class = 14 features; 3 public functions; 1 module file.
**Survived:** Yes
**Action:** New in v4 (closes v3 audit Q1.7 — "14 Gonzo Sauce features stated four times without verification log entry").

## Claim 25 (NEW in v4): "Three calibration bugs in one week" claim

**Claim:** v4 § 1.2 states "three calibration bugs in one week traced to silent code-path drift between training and inference."
**Document location:** v4 § 1.2, A.3
**What was checked:** Read `model/shared/gonzo_features.py:7-11`
**What was found:** Docstring text:
```
This module is the single source of truth for the 14 Gonzo Sauce features.
NO duplication of computation logic between training and inference. Drift
here = silent calibration bugs (per session learning post-Bug #15 — three
distinct bugs this week traced to code-path drift between training and
inference).
```

The "three distinct bugs this week" phrase is in the file's institutional-memory comment, written at extraction time. v4 cites this docstring as the verification source.

Decomposed: 1 source (file docstring); 1 quote ("three distinct bugs this week"); attribution context "post-Bug #15."
**Survived:** Yes (verified-from-file rather than from operator memory; the file docstring is itself the institutional record)
**Action:** New in v4 (closes v3 audit Q1.6 — "three calibration bugs in one week — no log entry").

## Claim 26 (NEW in v4): Calibration bypass at `wr_inference_service.py:616-628` — "for ALL styles"

**Claim:** v4 § 1.2 and § 9.12 state the calibration bypass affects "ALL styles." v4 § 9.12 quotes the inline comment exactly.
**Document location:** v4 § 1.2, § 9.12, A.2
**What was checked:** Read `backend/services/wr_inference_service.py` lines 615–629
**What was found:** Lines 616–625:
```
# ── Calibration BYPASS (BUG #15 + BUG #24) ────────────────────────
# All styles (including gonzo_sauce) bypass calibration at inference
# tonight. Original Phase A3 plan was to apply gonzo's fitted
# ranker calibration here, but that surfaced Bug #24: isotonic
# mapping of legitimate-PP horses' ranker_probs (≈ base_rate) to
# near-zero, then 0-PP override at 1/field_size dominates after
# renormalize → 0-PP horses become top picks (Wonder Dean JPN at #1
# in Derby smoke test). Gonzo joins the legacy bypass until the
# Phase A3.5 fix splits 0-PP horses out of the calibration path
# entirely. Calibration sidecar remains in S3 for A3.5 use.
```

Followed at line 626 by:
```python
handicapping_probs = ranker_probs.copy()
```

The comment block explicitly states "All styles (including gonzo_sauce) bypass" — confirming the "ALL styles" claim. The next executable statement copies raw ranker_probs without calibrator application.

Decomposed: 1 comment block at lines 616–625 + 1 executable line (626) = 11 lines of code area; "All styles" appears verbatim once; "gonzo_sauce" called out as included.
**Survived:** Yes
**Action:** New in v4 (closes v3 audit Q1 coverage gap — "calibration bypass at `wr_inference_service.py:616-628` 'for ALL styles' — code re-verified but no log entry").

## Claim 27 (NEW in v4): `gonzo_features.py` import sites

**Claim:** A.3 states the module is imported by both `model/shared/data_loader.py:45` and `backend/services/feature_engineering_service.py:16`.
**Document location:** v4 Appendix A.3
**What was checked:** `grep -n "gonzo_features" model/shared/data_loader.py backend/services/feature_engineering_service.py`
**What was found:**
- `model/shared/data_loader.py:45:from shared.gonzo_features import (`
- `backend/services/feature_engineering_service.py:16:from model.shared.gonzo_features import (`

Decomposed: 2 import sites; 1 module imported; both training and inference paths represented.
**Survived:** Yes
**Action:** New in v4 (closes v3 audit coverage gap — A.3's "imported by both" claim now backed)

---

## Verification summary

**Total claims documented:** 27 (23 inherited from v3 + 4 new + 1 corrected for precision)
**Survived as-is (re-verified live 2026-05-04):** 22
**Modified for precision per v4 lesson:** 2 (Claim 16 — count decomposed; Claim 22 — 28+ → 103)
**Updated to add line numbers / specific citations:** 1 (Claim 14 → Claim 14b spinoff)
**New v4 claims (close v3 coverage gaps):** 5 (14b, 15b, 24, 25, 26, 27 — note 14b was a spinoff so the new-only count is 5)
**Dropped:** 0
**Architectural questions surfaced:** 0 new in v4 cycle; 1 from v3 cycle (Tony's Q4 reframing) was ratified in this cycle.

**Verification-log precision rule (locked v4):**

The v3 → v4 BLOCKER root cause was Claim 16's loose phrasing "4 references including the import," which the main-doc drafter compressed to "4 instantiations." v4 closes this by:

1. Decomposing every count: imports + instantiations + uses + definitions, not aggregated unless the components are also shown.
2. Distinguishing definitions (where the symbol is declared) from uses (where the symbol is invoked) from imports (where the symbol is brought into scope).
3. Where a sum is given, both the sum and the components must be present.

This rule applies to every Tier 3 verification log going forward (BIBLE_STRUCTURE_SPEC, AUDIT_METHODOLOGY, TRIAGE_QUEUE_SPEC, all Phase 1 bibles).

**No fabricated content in v4.** Every concrete claim has a verification entry above with decomposed counts. Every claim that could not be verified has been dropped, replaced, or explicitly flagged.
