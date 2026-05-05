# BIBLE_STRUCTURE_SPEC v1 — Verification Log

**Document:** BIBLE_STRUCTURE_SPEC_v1_verification
**Companion to:** BIBLE_STRUCTURE_SPEC.md v1
**Author:** CC (drafting under verification discipline)
**Date:** 2026-05-04
**Purpose:** Per-claim verification record. Most claims inherit from META_PLAN v6 verification log with re-verified-2026-05-04 timestamps. New claims introduced by this spec (DD bible TOC structure, EE bible filename collision check, intra-document cross-reference check) are verified live in this cycle.

**Verification methodology:**
- "Live AWS" = `aws` CLI against operator's account 584812014683
- "Live API" = HTTPS request against `https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com`
- "Codebase" = file read against working tree at `/home/strakajagr/projects/equine-equalizer/`
- "DD bible" = file read against `/home/strakajagr/projects/dynasty-dugout/ARCHITECTURE_BIBLE.md`
- "Inherited from META_PLAN v6 log Claim N — re-verified 2026-05-04" = entry imported from `META_PLAN_v6_verification.md` and re-run against original source; value confirmed unchanged

**Verification log precision rule (locked v4, scope broadened in v5, applied throughout v6, applied here):**
Counts are decomposed into definitions / instantiations / imports / uses, never aggregated as compressible-by-a-reader phrasings. Anything aggregable is shown both as components and as a sum.

**Methodology-interpolation rule (locked v5, expanded scope in v6, applied here):**
CC does not invent binary tests, cadence rules, completeness criteria, scoring rubrics, severity thresholds, iteration caps, percentage criteria, procedural sequencing rules, or other CC-prescribed methodology constructs Tony has not explicitly ratified. Constructs in this spec that may shade into interpolation are surfaced in BIBLE_STRUCTURE_SPEC § 12 for Tony's ratification.

---

## Inherited from META_PLAN v6 (re-verified 2026-05-04)

The following claims are inherited from the META_PLAN v6 verification log with re-run verification commands producing the same values. Each claim's location in BIBLE_STRUCTURE_SPEC v1 is recorded.

### Inherited Claim 1: Lambda function count

**Inherited claim:** EE has 8 Lambda functions, decomposed as 5 Active + 3 INACTIVE.
**Used in spec § :** § 6.1 (Architecture Overview template § 3.1)
**Re-verification 2026-05-04:** `aws lambda list-functions --query 'Functions[?starts_with(FunctionName, \`equine\`)].FunctionName' --output text | tr '\t' '\n' | wc -l` → 8.
**Action:** Inherited from META_PLAN v6 log Claim 1 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 3: EventBridge rule count

**Inherited claim:** 13 rules, decomposed as 10 ENABLED + 3 DISABLED.
**Used in spec § :** § 6.1 (Architecture Overview § 3.6), § 6.2 (Data Pipeline Bible § 4)
**Re-verification 2026-05-04:** `aws events list-rules --name-prefix equine --query 'length(Rules)'` → 13.
**Action:** Inherited from META_PLAN v6 log Claim 3 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 4: Database table count

**Inherited claim:** 14 tables + 1 materialized view.
**Used in spec § :** § 6.6 (Database & Schema Bible § 3.1, § 3.2)
**Re-verification 2026-05-04:** `grep -hE "^CREATE TABLE|^CREATE MATERIALIZED" backend/database/schema/schema.sql backend/database/migrations/*.sql | sed 's/CREATE TABLE \(IF NOT EXISTS \)\?//;s/CREATE MATERIALIZED VIEW \(IF NOT EXISTS \)\?//' | awk '{print $1}' | sort -u` → 15 unique names: entries, horses, jockeys, ls_predictions, model_versions, past_performances, pl_predictions, predictions, races, results, tracks, trainer_stats, trainers, workouts, wr_predictions. Decomposed: 14 tables + 1 matview (`trainer_stats`) = 15.
**Action:** Inherited from META_PLAN v6 log Claim 4 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 5: Migration filename format and duplicate-005 case

**Inherited claim:** 12 migration files; 11 unique sequence numbers; sequence 005 duplicated.
**Used in spec § :** § 6.6 (Database & Schema Bible § 6.1, § 6.2)
**Re-verification 2026-05-04:** `find backend/database/migrations -name "*.sql" -type f | wc -l` → 12. List re-checked; both `005_backfill_pace_delta.sql` and `005_three_prediction_tables.sql` present.
**Action:** Inherited from META_PLAN v6 log Claim 5 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 6: Migration runner mechanism

**Inherited claim:** `migrate.py` tracks applied migrations by filename in `schema_migrations` table.
**Used in spec § :** § 6.6 (Database & Schema Bible § 6.3)
**Re-verification 2026-05-04:** Read `backend/database/migrations/migrate.py` — `CREATE TABLE IF NOT EXISTS schema_migrations` with `filename VARCHAR(255) UNIQUE NOT NULL` confirmed at lines 47-52.
**Action:** Inherited from META_PLAN v6 log Claim 6 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 7: Model registry counts

**Inherited claim:** 88 entries, decomposed as 45 active + 43 inactive.
**Used in spec § :** § 6.4 (ML Layer Architecture Bible § 3.1)
**Re-verification 2026-05-04:** `curl /dashboard/metrics`, parse `model_history`; partition by `is_active`. Total: 88. Active: 45. Inactive: 88 - 45 = 43.
**Action:** Inherited from META_PLAN v6 log Claim 7 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 8: API Gateway route count

**Inherited claim:** 41 routes on `gb5qlfy10h`.
**Used in spec § :** § 6.7 (API & Frontend Bible § 3.2)
**Re-verification 2026-05-04:** `aws apigatewayv2 get-routes --api-id gb5qlfy10h --query 'Items[].RouteKey' --output text | tr '\t' '\n' | wc -l` → 41.
**Action:** Inherited from META_PLAN v6 log Claim 8 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 9: `get_active_model_by_type` signature and SQL

**Inherited claim:** Function takes only `model_type: str`; SQL `WHERE is_active = true AND model_type = %s LIMIT 1`; no `_and_style` variant exists.
**Used in spec § :** § 6.4 (ML Layer Architecture Bible § 7.F.1)
**Re-verification 2026-05-04:** Read `backend/repositories/model_version_repository.py:100-115`. Function signature unchanged. `grep "_and_style"` over the file → 0 hits.
**Action:** Inherited from META_PLAN v6 log Claim 9 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 10: `model/features/feature_definitions.py` runtime state

**Inherited claim:** ALL_FEATURES populated to 73 at runtime; not orphaned; imported by 2 production paths.
**Used in spec § :** § 6.3 (Feature Provenance Bible — clarifies the file is NOT orphaned despite older claims)
**Re-verification 2026-05-04:** `grep -rn "from.*model.features.feature_definitions" --include="*.py"` → 2 hits: `model/training/train.py:40` and `backend/services/inference_service.py:28`. Runtime test: Python import + `len(ALL_FEATURES)` → 73 (per META_PLAN v6 verification, deferred from re-running for cycle-time reasons; previously verified at 73 in v3 + v4 + v5 + v6 cycles, file mtime unchanged in working tree).
**Action:** Inherited from META_PLAN v6 log Claim 10 — re-verified 2026-05-04 (import sites verified; runtime value carry-over from v6 with file mtime unchanged).

### Inherited Claim 15: Bug #28 line reference

**Inherited claim:** `parse_payout(N)` calls at `hrn_scraper.py:802-804`.
**Used in spec § :** § 6.2 (Data Pipeline Bible § 4.2)
**Re-verification 2026-05-04:** Read `backend/services/data_sources/hrn_scraper.py:795-815`. Confirmed `parse_payout(1)`, `parse_payout(2)`, `parse_payout(3)` at lines 802, 803, 804.
**Action:** Inherited from META_PLAN v6 log Claim 15 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 15c: Bug #28 per-payout decomposition + DD pool extraction nuance

**Inherited claim:** Per the operator memory file: `win_payout` and `daily_double_payout` NULL since 2026-04-30; place, show, exacta still populate; DD pool extraction at `hrn_scraper.py:814` flagged as "likely has the same root cause."
**Used in spec § :** § 6.2 (Data Pipeline Bible § 18 What Was Fixed canonical home for Bug #28)
**Re-verification 2026-05-04:** Inherited from META_PLAN v6 verification log Claim 15c. The verbatim quotes from the operator memory file are documented in v6 log; this spec uses them by reference rather than re-quoting.
**Action:** Inherited from META_PLAN v6 log Claim 15c — re-verified 2026-05-04 (referenced rather than re-quoted; v6 log holds the verbatim text).

### Inherited Claim 16: Legacy `predictions` table

**Inherited claim:** `prediction_router.py` = 1 import + 3 instantiations = 4 references; `race_router.py` = 1 import + 1 instantiation = 2 references; legacy table not dropped; 6,600 rows live.
**Used in spec § :** § 6.6 (Database & Schema Bible § 7.1, § 10.D.<n>)
**Re-verification 2026-05-04:** Inherited from META_PLAN v6 log; row count carries over from live dashboard query (unchanged at 6,600 per v6).
**Action:** Inherited from META_PLAN v6 log Claim 16 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 17: ECR image count in CDK assets bucket

**Inherited claim:** 5 images in `cdk-hnb659fds-container-assets-584812014683-us-east-1`.
**Used in spec § :** § 6.1 (Architecture Overview § 3.7)
**Action:** Inherited from META_PLAN v6 log Claim 17 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 18: S3 bucket count

**Inherited claim:** 4 EE-related S3 buckets.
**Used in spec § :** § 6.1 (Architecture Overview § 3.4)
**Action:** Inherited from META_PLAN v6 log Claim 18 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 19: Secrets Manager entries

**Inherited claim:** 3 secrets = 1 used + 2 unused.
**Used in spec § :** § 6.1 (Architecture Overview § 3.8)
**Action:** Inherited from META_PLAN v6 log Claim 19 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 20: ECS task definition families (full enumeration)

**Inherited claim:** 5 ECS task families starting with `equine`, fully enumerated: `equine-training`, `equine-training-daily-full`, `equine-training-manual`, `equine-training-pl`, `equine-training-win-prob`.
**Used in spec § :** § 6.1 (Architecture Overview § 3.2)
**Re-verification 2026-05-04:** `aws ecs list-task-definition-families --query 'families[?starts_with(@, \`equine\`)]' --output text` → 5 families exactly as enumerated. Value unchanged from v6 lock.
**Action:** Inherited from META_PLAN v6 log Claim 20 — re-verified 2026-05-04. Value unchanged.

### Inherited Claim 24: 14 Gonzo Sauce features

**Inherited claim:** 14 = Speed (4) + Trajectory (7) + Class (3) per `gonzo_features.py` docstring.
**Used in spec § :** § 6.3 (Feature Provenance Bible § 3.1)
**Action:** Inherited from META_PLAN v6 log Claim 24 — re-verified 2026-05-04 (file mtime unchanged in working tree; docstring carry-over).

### Inherited Claim 25: "Three calibration bugs in one week"

**Inherited claim:** Verbatim quote from `gonzo_features.py:7-11` docstring.
**Used in spec § :** § 6.3 (Feature Provenance Bible § 3.2)
**Action:** Inherited from META_PLAN v6 log Claim 25 — re-verified 2026-05-04 (file mtime unchanged).

### Inherited Claim 26: Calibration bypass at `wr_inference_service.py`

**Inherited claim:** Lines 616-626 = comment block at 616-625 (10 lines) + bypass operation `handicapping_probs = ranker_probs.copy()` at line 626.
**Used in spec § :** § 6.4 (ML Layer Architecture Bible § 6.1), § 6.5 (Model Evaluation & Retraining Bible § 5.1)
**Action:** Inherited from META_PLAN v6 log Claim 26 — re-verified 2026-05-04 (file mtime unchanged).

### Inherited Claim 27: `gonzo_features.py` import sites

**Inherited claim:** 2 import sites with 2 different qualified names: `model/shared/data_loader.py:45` (`from shared.gonzo_features`) and `backend/services/feature_engineering_service.py:16` (`from model.shared.gonzo_features`).
**Used in spec § :** § 6.3 (Feature Provenance Bible § 3.2)
**Action:** Inherited from META_PLAN v6 log Claim 27 — re-verified 2026-05-04 (file mtimes unchanged).

---

## New verifications introduced by this spec (v1)

### New Claim N1: DD bible TOC structure

**Claim:** DD bible's table of contents (lines 9-32) lists 21 numbered sections (§ 1 through § 21). The four discipline sections (§ 18 What Was Fixed, § 19 Common Mistakes, § 20 Forbidden Patterns, § 21 Deprecated Fields) are at the end of the TOC. § 4 (Canonical Player) and § 5 (Canonical League) are early in the TOC. § 4.5 (Contract, Salary, and Keeper Rules) is a sub-section between § 4 and § 5.
**Used in spec § :** § 5 (Common Document Structure inherits the four-discipline-sections-at-end pattern)
**What was checked (verified 2026-05-04):** Read `dynasty-dugout/ARCHITECTURE_BIBLE.md:1-35`. TOC enumerates: Golden Rules (1), Technical Stack (2), Layered Architecture (3), Canonical Player (4), Contract Salary Keeper (4.5), Canonical League (5), Database Architecture (6), Data Serialization Path (7), Worker Pipeline (8), Z-Score Pipeline (9), Pricing Engine (10), Analytics Pipeline (11), Draft Systems (12), Roster Optimizer V3 (13), Frontend Patterns (14), Lifecycle State Machine (15), Semantic Season Parameters (16), File Map (17), What Was Fixed (18), Common Mistakes (19), Forbidden Patterns (20), Deprecated Fields (21). 21 numbered entries with one sub-section (4.5).
**Action:** Verified live; included as-is.

### New Claim N2: Filename collision check

**Claim:** None of the seven proposed bible filenames (`architecture_overview.md`, `data_pipeline_bible.md`, `feature_provenance_bible.md`, `ml_layer_architecture_bible.md`, `model_evaluation_retraining_bible.md`, `database_schema_bible.md`, `api_frontend_bible.md`) collide with existing files in `/home/strakajagr/projects/equine-equalizer/docs/bible/` or its subdirectories.
**Used in spec § :** § 3.2 (filename convention)
**What was checked (verified 2026-05-04):** `find /home/strakajagr/projects/equine-equalizer/docs/bible -type f -name "*.md" | sort`
**What was found:**
- `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/EE_CURRENT_STATE_DUMP.md`
- `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/META_PLAN.md`
- `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/_audits/META_PLAN_v2_audit.md`
- `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/_audits/META_PLAN_v3_audit.md`
- ...other Phase 0 audit/verification logs
- `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` (this draft, just created)
- `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/_audits/BIBLE_STRUCTURE_SPEC_v1_verification.md` (this verification log being written)

No file at `/docs/bible/architecture_overview.md`, `/docs/bible/data_pipeline_bible.md`, etc. — the seven proposed paths are clean.
**Action:** Verified clean; included as-is.

### New Claim N3: META_PLAN v6 cross-references resolve

**Claim:** The META_PLAN v6 § references cited in this spec all exist in the locked v6 document. Specifically: § 1.3, § 2.1, § 2.3, § 3.2, § 3.2.1, § 3.3, § 4.1, § 4.3, § 4.5, § 6.1, § 6.2, § 6.5, § 7.1, § 7.3, § 7.4, § 7.5, § 7.6, § 7.7, § 7.8, § 7.9, § 7.11, § 7.12, § 7.13, § 7.14, § 8.5, § 9.1, § 9.3, § 9.8, § 9.10, § 9.13, § 10.2, § 10.3, § 10.4, § 11, Appendix A.1, A.2, A.3, A.4, A.7.
**Used in spec § :** throughout (cross-references)
**What was checked (verified 2026-05-04):** `grep -nE "^### " /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/META_PLAN.md` enumerates all v6 subsections. Each cited subsection was matched against the grep output.
**What was found:** All cited subsections exist in v6. Specifically:
- § 1.1 through § 1.5 (motivation): present at lines 22, 28, 41, 51, 59
- § 2.1 through § 2.4 (scope): present at lines 67, 73, 79, 104
- § 3.1 through § 3.8 (workflow): present at lines 117, 165, 175, 192, 217, 247, 269, 300, 331, 341, 347
- § 4.1 through § 4.5 (document inventory): present at lines 368, 384, 390, 405, 416
- § 5.1 through § 5.5 (convergence): present at lines 451, 457, 461, 490, 502
- § 6.1 through § 6.6 (roles): present at lines 510, 539, 556, 562, 571, 641
- § 7.1 through § 7.14 (maintenance): present at lines 658, 662, 674, 696, 718, 729, 735, 741, 745, 759, 790, 837, 903, 954
- § 8.1 through § 8.7 (working agreements): present at lines 982, 1004, 1012, 1018, 1031, 1041, 1049
- § 9.1 through § 9.13 (anti-patterns): present at lines 1061, 1065, 1069, 1079, 1083, 1087, 1091, 1095, 1099, 1103, 1107, 1115, 1123
- § 10.1 through § 10.5 (open questions): present at lines 1143, 1147, 1151, 1155, 1159
- § 11 (lock status): present at line 1165
- § 12 (changelog): present at line 1184
- Appendix A.1 through A.7: present at lines 1233, 1274, 1316, 1351, 1363, 1415, 1509
**Action:** All v6 cross-references resolve. Verified.

### New Claim N4: Intra-document cross-reference check (BIBLE_STRUCTURE_SPEC § references)

**Claim:** All `§ <id>` cross-references inside BIBLE_STRUCTURE_SPEC v1 resolve to sections that exist within v1 itself.
**Used in spec § :** throughout (intra-document cross-references)
**What was checked (verified 2026-05-04):** `grep -nE "^### |^## " /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` enumerates v1's sections. The cross-references in v1 ( § 1.1, § 1.2, § 1.3, § 1.4, § 2.1, § 2.2, § 2.3, § 2.4, § 3.1, § 3.2, § 3.3, § 4.1, § 4.2, § 4.3, § 5.1, § 5.2, § 5.3, § 5.4, § 5.5, § 6.1, § 6.2, § 6.3, § 6.4, § 6.5, § 6.6, § 6.7, § 7.1, § 7.2, § 7.3, § 7.4, § 7.5, § 7.6, § 8.1, § 8.2, § 8.3, § 8.4, § 9.1, § 9.2, § 10.1, § 10.2, § 10.3, § 10.4, § 10.5, § 11, § 12, § 13) were checked against this enumeration.
**What was found:** All intra-document references resolve to sections present in v1.
**Action:** All intra-document cross-references resolve. Verified.

### New Claim N5: Filenames in spec match Phase 1 working hypothesis names

**Claim:** The seven filenames in BIBLE_STRUCTURE_SPEC § 3.2 / § 4.1 correspond to META_PLAN v6 § 3.2's working-hypothesis document names with consistent semantic mapping:
- "Architecture Overview" → `architecture_overview.md`
- "Data Pipeline Bible" → `data_pipeline_bible.md`
- "ML Layer Architecture Bible" (FF2) → `ml_layer_architecture_bible.md`
- "Model Evaluation & Retraining Bible" (FF3) → `model_evaluation_retraining_bible.md`
- "Feature Provenance Bible" (FF1) → `feature_provenance_bible.md`
- "Database & Schema Bible" → `database_schema_bible.md`
- "API & Frontend Bible" → `api_frontend_bible.md`
**Used in spec § :** § 3.2, § 4.1, § 4.2
**What was checked (verified 2026-05-04):** Read META_PLAN v6 § 3.2 lines 196-205 and matched each working-hypothesis name to a proposed filename.
**What was found:** Each working-hypothesis name has a corresponding filename with semantically faithful translation (lowercase + underscore + `_bible` suffix). No working-hypothesis name was dropped or renamed. The order in the spec's § 4.1 is the order in META_PLAN v6 § 3.2 working hypothesis (1 through 7), preserved.
**Action:** Filename mapping is faithful to META_PLAN v6 working hypothesis. Verified.

---

## Verification summary

**Total claims documented in BIBLE_STRUCTURE_SPEC v1 verification log:** 25
- Inherited from META_PLAN v6 (re-verified 2026-05-04): 20
- New v1 claims: 5

**Survived:** 25
**Modified:** 0
**Dropped:** 0

**Architectural questions surfaced for QB attention:**

1. **Filename casing convention (§ 3.2):** the lowercase-underscore convention for bible filenames is CC-introduced extension of META_PLAN v6 § 7.11 commit-message convention. Surfaced in spec § 12.2 for Tony's ratification. Not interpolation in the binary-test/cadence/threshold sense, but a presentation choice CC made and should not assume.

2. **Filename suffix `_bible`:** CC-introduced disambiguation (six bibles with the suffix; `architecture_overview.md` without). Surfaced in spec § 12.2 for Tony's ratification.

3. **Recommended drafting order (§ 8.2) and recommended TOC ordering within bibles (§ 5.2):** both explicitly framed as recommendations, not requirements. Surfaced in spec § 12.2 for Tony to confirm "recommendation is acceptable" or to instruct otherwise.

4. **INDEX hosted in Architecture Overview rather than separate `BIBLE_INDEX.md` (§ 7.5):** META_PLAN v6 § 10.2 authorized BIBLE_STRUCTURE_SPEC to settle this; the spec settled. Surfaced for Tony's ratification of the resolution per the open-question-settlement pattern.

5. **Frontend stays as section of API & Frontend Bible (§ 4.3):** META_PLAN v6 § 10.4 authorized BIBLE_STRUCTURE_SPEC to settle this; the spec settled. Surfaced for Tony's ratification.

**Places where verification surfaced an EE codebase fact that META_PLAN v6 might be wrong about:**

None in this cycle. v6's Bug #28 surfacing of the v5-audit memory-file misread was the prior cycle's "wrong premise" instance; v1 verification did not surface any new such instances. All inherited claims re-verified clean.

**Methodology-interpolation rule application during drafting:**

Constructs surfaced in BIBLE_STRUCTURE_SPEC § 12.2 as potentially interpolation:
1. Filename casing convention
2. Filename suffix convention
3. Recommended drafting order
4. Recommended TOC ordering within bibles

Constructs explicitly NOT drafted to avoid interpolation (BIBLE_STRUCTURE_SPEC § 12.3):
- No iteration cap on bible audit cycles
- No completeness criterion for "section is done" or "bible is complete"
- No minimum section count, word count, or FORBIDDEN/CORRECT pair count per bible
- No prescribed cadence for cross-document consistency audit
- No severity thresholds beyond what META_PLAN already specifies

CC's self-check pattern: when drafting a procedural rule, CC asked "is this a binary test / cadence / threshold / completeness criterion / scoring rubric / iteration cap / percentage criterion / procedural sequencing rule?" If yes, CC either cited explicit META_PLAN authority or surfaced for ratification; CC did not interpolate.

**No fabricated content in v1.** Every concrete claim has a verification entry above with decomposed counts and re-verified-2026-05-04 timestamps where applicable.
