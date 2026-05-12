# Database & Schema Bible v1 Drafting Spec

**Document:** DATABASE_SCHEMA_BIBLE_V1_DRAFTING_SPEC
**Phase:** 1 deliverable 2 of 7 (drafting-order numbering per BIBLE_STRUCTURE_SPEC v6 § 8.2)
**Status:** AUTHORED 2026-05-05 — paste-ready for CC drafting session
**Author:** QB (Database & Schema Bible cycle, 2026-05-05)
**Date:** 2026-05-05

**Spec authorship discipline:** Option 1 with 9 checks operative across 3 clusters per `QB_HANDOFF_DATABASE_SCHEMA_BIBLE_DRAFTING.md` § 3. QB substrate-verification log at this spec's § 11; QB-side handoff cross-reference corrections banked at § 10.

**Anchored on:**
- META_PLAN v9 (LOCKED 2026-05-05)
- BIBLE_STRUCTURE_SPEC v6 (LOCKED 2026-05-05)
- AUDIT_METHODOLOGY v2 (LOCKED 2026-05-04)
- CONVERGENCE_CRITERIA v2 (LOCKED 2026-05-04)
- TRIAGE_QUEUE_SPEC v1 (LOCKED 2026-05-04)
- Architecture Overview v3 (LOCKED 2026-05-05) — canonical references for downstream

---

## Table of contents (this spec)

1. CC paste-prompt — spec body that pastes into a fresh CC session
2. Reference materials and source-priority discipline
3. Operating disciplines CC must follow
4. Prescribed TOC and per-section drafting guidance (substrate-anchored)
5. Verification log structure and per-section content requirements
6. QB self-audit log Section H entries (to be reproduced char-exact in CC's verification log)
7. Bash-grep verification predictions (Check 9 precision)
8. Skip-audit pre-approval determination
9. Iteration expectation
10. Handoff cross-reference corrections (banked Check 1 findings)
11. QB substrate-verification log (Option 1 9-check self-audit)

---

## 1. CC paste-prompt

The block below is the paste-ready CC paste-prompt. Tony copies the text from `### 1.1 Paste-prompt body` through end-of-block into a fresh CC session. Sections 2–11 of this spec are QB-side context that does NOT paste into CC's session — they document the QB's spec authorship discipline for audit-trail purposes.

### 1.1 Paste-prompt body

> You are CC drafting **Database & Schema Bible v1** for the Equine Equalizer (EE) Phase 1 cycle. This is Phase 1 deliverable 2 of 7 (drafting-order numbering per BIBLE_STRUCTURE_SPEC v6 § 8.2). Phase 1 deliverable 1 (Architecture Overview) LOCKED 2026-05-05 and is the canonical references substrate this bible cross-references outward to.
>
> **Output target:** `/home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md` plus companion verification log at `/home/strakajagr/projects/equine-equalizer/docs/bible/_audit/database_schema_bible_v1_verification.md`.
>
> **Tier:** 3 per META_PLAN v9 § 4.1 + § 6.5. **HARD RULE: Drafts without companion verification logs are rejected by QB without audit. The verification log is not optional.**
>
> **Char-exact reproduction discipline does NOT apply** to this draft — full prose authoring latitude per CC drafter paste-prompt boilerplate (BIBLE_STRUCTURE_SPEC v6 + QB handoff § 7.1). Every factual claim requires a verification log entry per Tier 3 discipline.
>
> ---
>
> ### Reference materials (read FIRST, before drafting)
>
> 1. **Architecture Overview v3 LOCKED** at `/home/strakajagr/projects/equine-equalizer/docs/bible/architecture_overview.md` — canonical references for cross-runtime topology this bible cross-references outward to. § 3.3 (RDS PostgreSQL) and § 4.1 (canonical objects) are load-bearing for this bible's Scope and per-table sections.
> 2. **BIBLE_STRUCTURE_SPEC v6 § 6.6** at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` (search for the "### 6.6 database_schema_bible.md" header; the section spans from that header to the next "### 6.7" header) — prescribed TOC, per-section guidance, and conditional triggers. **NORMATIVE for this draft.**
> 3. **BIBLE_STRUCTURE_SPEC v6 § 5.5–§ 5.6** — W.N format, Forbidden Pattern, Common Mistakes, Deprecated entry templates (canonical). Per § 5.5.1 global Bug #N convention, cross-bible bug references use `<bible>:#<bug-id>`.
> 4. **META_PLAN v9 § 4.5** — source-priority hierarchy: Tier 1 (live AWS) > Tier 2 (live API) > Tier 3 (live DB) > Tier 4 (working-tree code post-baseline) > Tier 5 (operator-stated history) > Tier 6 (`EE_CURRENT_STATE_DUMP.md`) > Tier 7 (session logs).
> 5. **META_PLAN v9 § 6.5** — verification log precision rule (counts decomposed; definitions vs uses vs imports distinguished; no compressible aggregations).
> 6. **META_PLAN v9 § 7.3 placeholder-resolution sub-rule** (locked v7) — Phase 1 drafters MUST resolve W.N entry "fixed YYYY-MM-DD" dates via `git log` of the relevant primary source for any real fix. Placeholders only for forward-looking discipline codifications. **Operative for any W.N entry in this bible.**
> 7. **META_PLAN v9 § 7.12** — migration discipline: NNN_short_description.sql for 001–011 (grandfathered); NNN_YYYYMMDD_*.sql from 012+. The duplicate-005 case is documented honestly. Migration runner `backend/database/migrations/migrate.py` tracks applied migrations in `schema_migrations` table by filename (verified). Rollback format: in-file down-block, manual; not auto-run by runner.
> 8. **META_PLAN v9 § 9.13** — multi-active-row reality of `model_versions` (88 = 45 active + 43 inactive; `get_active_model_by_type` selects arbitrary row when multiple match per `model_type`).
> 9. **EE_CURRENT_STATE_DUMP.md** at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/EE_CURRENT_STATE_DUMP.md` — Tier 6 baseline only. **Verify any inherited claim against live state per Lesson 1 (cross-project contamination check) + Lesson 2 (Phase 0 substrate errors).** Cross-project contamination concretely: if a claim references an Aurora cluster, an `equinedatabasestack-*` cluster identifier, or any name suggesting `fantasy-baseball-serverless` provenance, it is suspect — EE uses standalone RDS PostgreSQL `equine-db`, not Aurora.
> 10. **EE codebase at** `/home/strakajagr/projects/equine-equalizer/`. Specifically:
>     - `backend/database/schema/schema.sql` — initial schema (11 CREATE TABLE statements verified by QB)
>     - `backend/database/migrations/001_initial_schema.sql` through `011_wr_predictions_unique_fix.sql` (12 .sql files; 005 duplicate-prefixed)
>     - `backend/database/migrations/migrate.py` — runner (verified: `_get_connection_string()` at function `get_connection_string()` lines 22–43; `schema_migrations` table CREATE in `ensure_migrations_table` function)
>     - `backend/models/canonical.py` — 14 dataclasses (Track, Horse, Trainer, Jockey, Workout, PastPerformance, Entry, Race, RaceCard, Result, ModelVersion, PLPrediction, LSPrediction, Prediction). Per Architecture Overview § 4.1: Race line 255, Entry line 214, PastPerformance line 77, Workout line 58, Result line 296, Prediction line 428.
>     - `backend/repositories/` — repository modules; `model_version_repository.py:100` houses `get_active_model_by_type` per META_PLAN v9 § 9.13 + Architecture Overview Forbidden-Pattern candidate
>     - `backend/services/wr_inference_service.py:616-626` — calibration bypass (comment block 616–625 + bypass operation `handicapping_probs = ranker_probs.copy()` at line 626 per Architecture Overview § 4.1 + META_PLAN v9 § 9.12)
>
> ### Verification discipline (HARD RULE)
>
> - **Live AWS / database / code** prevails over EE_CURRENT_STATE_DUMP per § 4.5 source-priority. Tier 6 is best-available baseline only.
> - **Cross-project contamination check (Lesson 1):** any inherited Tier 6 claim verified against live state with explicit "is this EE schema or bleed from an adjacent project?" test. The Aurora cluster ARN inheritance error in META_PLAN v8 was cross-project bleed from `fantasy-baseball-serverless`; substrate reality (V9 § 2.3) is standalone RDS PostgreSQL `equine-db`. Verification log entries should explicitly cite the verification command run and the source-tier of the resulting claim.
> - **Counts decomposed (META_PLAN v9 § 6.5):** every aggregable count must be broken down into its components in the verification log entry. "14 tables + 1 matview" must be entered as "11 CREATE TABLE in schema.sql + 3 CREATE TABLE in migration 005_three_prediction_tables.sql + 1 CREATE MATERIALIZED VIEW in migration 008_create_trainer_stats.sql = 14 tables + 1 matview." No compressible aggregations.
> - **Methodology-interpolation rule (META_PLAN v9 § 6.1):** CC must NOT invent binary tests, cadence rules, completeness criteria, scoring rubrics, severity thresholds, iteration caps, percentage criteria, procedural sequencing rules, or other CC-prescribed methodology constructs Tony has not explicitly ratified. If verification or drafting reveals a need for such a construct, surface to QB via FRAMEWORK_GAP marker.
> - **Framework-rejection markers (META_PLAN v9 § 6.5):**
>   - `<SPEC_GAP: explanation>` — entire spec premise wrong (e.g., spec asks CC to document a function/table that doesn't exist).
>   - `<FRAMEWORK_GAP: explanation>` — specific framework slot can't be filled because the framework's structure doesn't accommodate the actual content (per Lesson 4: CC fills what fits, marks the gap, lets QB triage; if CC has a candidate reframing, CC presents it as candidate AND cites the substrate that supports OR refutes it).
> - **No fabrication.** If verification cannot confirm a claim, drop the claim or explicitly mark it as unverified-pending-Phase-X. Per META_PLAN v9 § 8.6.
>
> ### Methodology lessons 1–6 (banked from META_PLAN v9 + Architecture Overview cycles; operative as discipline)
>
> 1. **Lesson 1 — Cross-project contamination check.** Verification protocols against Tier 6 (EE_CURRENT_STATE_DUMP.md) include cross-project bleed check, not only stale-EE-state freshness check.
> 2. **Lesson 2 — Phase 1 verification surfaces Phase 0 substrate errors.** Surgical correction to Phase 0 documents is the expected response, not Phase 0 re-lock. (Operationally: if this draft surfaces a Phase 0 substrate error, surface to QB rather than silently working around it.)
> 3. **Lesson 3 (re-expanded) — Drafting specs cite primary verification log claim IDs, not paraphrased restatements.** Discipline applies to claim IDs, count statements, quoted text, attribution paraphrases, prescribed cross-reference section numbers, prescribed definition framing content, audit-CC enumeration completeness, line-number citations (Check 8 makes them line-shift-resistant), and bash-grep prediction precision (Check 9).
> 4. **Lesson 4 — FRAMEWORK_GAP discipline.** Any reframing CC introduces in its draft requires substrate verification. CC surfaces FRAMEWORK_GAP, fills what fits honestly, lets QB triage. If CC has a candidate reframing, present it as candidate AND cite the substrate that supports OR refutes it.
> 5. **Lesson 5 — Per-resource verification when target/state are independent AWS resources.** EventBridge rule State and target Lambda State are independent; documentation cites `aws events list-targets-by-rule` per rule, not `aws events list-rules` aggregate. Operationally for this bible: any claim about how a flow writes a table cross-references Architecture Overview § 3.6 (rule + target State) rather than asserting independently.
> 6. **Lesson 6 — Synthesis verification.** When synthesizing audit-CC findings into upstream-correction scope, the upstream claim is substrate-verified before synthesis routes. Audit-CC's downstream finding does not propagate as upstream truth without QB substrate check. Operationally for this draft: when CC identifies a documentation gap that suggests Architecture Overview or META_PLAN v9 needs correction, surface to QB rather than asserting the upstream needs revision.
>
> ### G-new-2 closure operative (BIBLE_STRUCTURE_SPEC v6 § 6.6 § 4.1 first-sentence qualification)
>
> **§ 4.1 enumeration scope = CREATE TABLE declarations only.** The 1 materialized view (`trainer_stats` from migration 008) lives at § 3, NOT § 4.1. Per § 2 Definitions, the table-vs-matview distinction is explicit; § 4.1 is "Per-table documentation" and matview documentation belongs in § 3.2 (or wherever this draft places matview overview content within § 3) per § 6.6 first-sentence qualification. Do NOT enumerate `trainer_stats` as `4.1.15` or any 4.1.X position.
>
> ### G-new-1 closure operative (candidate-roster numbering)
>
> If § 5 contains a candidate roster pending QB ratification (per § 5.7), use **numeric sub-section IDs** (`5.1`, `5.2`, ...) consistent with § 5.5 ratified-entry convention. **Provisional letter-prefixes (e.g., `5.A`, `5.B`) are NOT authorized.** Candidate status is conveyed by the § 5 header marker `[candidate roster pending QB ratification per § 5.7]`, not by letter-prefix.
>
> ---
>
> ### Prescribed TOC (mandatory per § 5.2 sections 5–8; recommended-strongly per § 5.2 sections 1–4 with drafter latitude per locality of reference)
>
> Per BIBLE_STRUCTURE_SPEC v6 § 6.6:
>
> 1. Scope
> 2. Definitions (table, materialized view, migration, JSONB shadow, canonical column)
> 3. Schema overview
>    - 3.1 14 tables (decomposed list)
>    - 3.2 1 materialized view (`trainer_stats`)
>    - 3.3 Schema bootstrap (`backend/database/schema/schema.sql`) vs migrations
> 4. Schema and migration detail
>    - 4.1 Per-table documentation (CREATE TABLE declarations only — G-new-2 closure)
>      - 4.1.X.<table_name> — one subsection per CREATE TABLE declaration
>    - 4.2 Migration discipline (per META_PLAN v9 § 7.12)
>      - 4.2.1 Numbering format (grandfathered 001–011 + NNN_YYYYMMDD from 012+)
>      - 4.2.2 The duplicate-005 case
>      - 4.2.3 The `schema_migrations` runner mechanism
>      - 4.2.4 Rollback format (in-file down-block, manual not auto-run)
>      - 4.2.5 Migration testing (non-production database first)
> 5. Discipline rules
>    - 5.1 UNIQUE constraints
>    - 5.2 JSONB conventions (where present; what fields, what shapes)
>    - 5.3 Cross-table FK conventions
>    - (additional rules surfaced by CC during § 5 candidate-roster enumeration per § 5.7 workflow; QB ratifies before § 5 locks)
> 6. Currently Open
> 7. Deprecated
>    - 7.1 Legacy `predictions` table (per BIBLE_STRUCTURE_SPEC v6 § 6.6 + Appendix A.4 in META_PLAN; canonical home for the legacy-table deprecated entry)
> 8. What Was Fixed
>
> **§ 5 candidate-roster workflow (per § 5.7):**
> 1. CC drafts § 5 with candidate roster (FORBIDDEN/CORRECT pairs per § 5.6.2; Common Mistakes per § 5.6.3).
> 2. CC produces § 5 verification log delta (Section C entries) enumerating each candidate rule's substrate evidence + provenance (CC-introduced vs grandfathered from prior locked Phase 0/Phase 1 docs).
> 3. CC marks § 5 header `[candidate roster pending QB ratification per § 5.7]`.
> 4. QB reviews + ratifies (this happens in QB's review cycle, between draft submission and audit-CC pass).
>
> ---
>
> ### Per-section content requirements
>
> [See § 4 of `database_schema_bible_v1_drafting_spec.md` — referenced from this paste-prompt by CC reading the spec file. The spec file lives at the same `_meta/` directory and is paste-companion to this prompt.]
>
> Specifically:
>
> **§ 1 Scope (recommended-strongly per § 5.2):**
> - Mandatory: state what this bible documents (table inventory, JSONB conventions, migration discipline, predictions-table family) and what it does NOT (per-flow data movement → `data_pipeline_bible:4.1`; ML feature consumption → `feature_provenance_bible:4`; model registry semantics → `ml_layer_architecture_bible:3.1`; per-route reads → `api_frontend_bible:4.1`).
> - Cross-reference Architecture Overview § 3.3 (RDS PostgreSQL `equine-db` runtime context) and § 4.1 (canonical objects).
> - State source-priority hierarchy (Tier 1 AWS > Tier 3 DB > Tier 4 code; matches META_PLAN v9 § 4.5).
> - Boundary statement: this bible is reference-style (look-up by table or column name); other bibles are flow-narrative or composition-narrative.
>
> **§ 2 Definitions:**
> - Mandatory terms: table, materialized view (with the explicit table-vs-matview distinction operative for § 4.1 enumeration scope per G-new-2), migration, JSONB shadow, canonical column, primary writer, primary reader, schema_migrations table.
> - Cross-reference META_PLAN v9 § 4.5 source-priority for tier-resolution semantics where relevant (e.g., "live DB Tier 3 wins for current row counts").
>
> **§ 3.1 14 tables:**
> - Mandatory: decomposed list per the verified count: **11 CREATE TABLE in `backend/database/schema/schema.sql` + 3 CREATE TABLE in `backend/database/migrations/005_three_prediction_tables.sql` = 14 tables**. Enumerate by name with one-line purpose. Cross-check at draft time via `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql | grep -v "schema_migrations" | wc -l` (expected: 14 plus possibly the `IF NOT EXISTS` patterns; verify count and decompose explicitly per Check 9).
> - The 14 tables (verified by QB substrate read 2026-05-05): tracks, horses, trainers, jockeys, races, entries, past_performances, workouts, results, predictions, model_versions (from schema.sql, 11 tables) + wr_predictions, pl_predictions, ls_predictions (from 005_three_prediction_tables.sql, 3 tables).
> - Note (and document explicitly): the runner-internal `schema_migrations` table is created at runtime by `migrate.py:ensure_migrations_table` (verified: `CREATE TABLE IF NOT EXISTS schema_migrations` inside the `ensure_migrations_table` function). It is NOT enumerated in the 14-table count (it is a runner-internal book-keeping table); document it at § 4.2.3 instead. The "14 tables" count is domain-schema tables only.
>
> **§ 3.2 1 materialized view (`trainer_stats`):**
> - Mandatory: `trainer_stats` matview created by `008_create_trainer_stats.sql` (verified: 1 `CREATE MATERIALIZED VIEW IF NOT EXISTS trainer_stats AS` statement). Aggregates career win/ITM/layoff/Lasix/claimed stats by trainer. Minimum 5 starts required to appear (HAVING COUNT(*) >= 5). UNIQUE INDEX on trainer_name. Refresh manually after large data loads via `REFRESH MATERIALIZED VIEW trainer_stats`.
> - Read by `feature_engineering_service._get_trainer_stats()` (per migration 008's docstring; verify reader inventory at draft time via grep).
> - **Per G-new-2 closure: `trainer_stats` documentation lives in § 3.2 only, NOT in § 4.1.X.** Do not enumerate `trainer_stats` at any 4.1.X position.
>
> **§ 3.3 Schema bootstrap vs migrations:**
> - Mandatory: schema.sql is the initial bootstrap (11 CREATE TABLE + indexes + the predictions ↔ model_versions FK). Migrations are diffs applied to evolve the schema. The runner mechanism: `ensure_migrations_table` creates `schema_migrations` if not present; `get_applied_migrations` returns the set of already-applied filenames; `run_migrations` iterates `sorted(*.sql)` files in the migrations dir and applies any not in `schema_migrations` (verified by QB read of migrate.py).
> - Cross-reference Architecture Overview § 3.3 (psycopg2 direct connections; canonical `_get_connection_string()` at `backend/shared/db.py:13-39`).
>
> **§ 4.1 Per-table documentation (one subsection per CREATE TABLE declaration; matview NOT included):**
>
> Per § 5.6.4 + § 6.6 § 4.1 mandatory fields:
> - Column list with types
> - Primary key
> - Purpose (one paragraph)
> - Primary writers (which Lambda or service writes; cross-reference Architecture Overview § 3.1 Lambda inventory + Lambda-to-flow cross-reference forward to `data_pipeline_bible:4.1` for the per-flow detail)
> - Primary readers (which router or service reads; cross-reference forward to `api_frontend_bible:4.1` for per-route detail)
>
> Conditional fields (with triggers):
> - **If has UNIQUE constraints:** enumerate verbatim from CREATE TABLE / migration ALTER TABLE statements. For tables whose UNIQUE constraint changed via migration (e.g., wr_predictions per migration 011), document the **current** constraint per source-priority Tier 4 (working-tree code post-baseline); per G2 closure, the prior superseded form does NOT require a Deprecated entry IF physically dropped — for wr_predictions, migration 011 explicitly DROPs `wr_predictions_unique_per_entry_model_style` and ADDs `wr_predictions_unique_per_entry_style`, so the prior form is dropped (verified by QB read of migration 011). Document at § 4.1.<wr_predictions> the current constraint; cross-reference migration 011 for the change history; do NOT add a Deprecated entry. (G2 verification log entry: include a verbatim excerpt of migration 011's ALTER TABLE block in CC's verification log Section C, per Check 1 substrate-grounded reframing.)
> - **If has FK constraints:** enumerate (e.g., predictions → model_versions, predictions → entries, predictions → races, predictions → horses; the predictions→model_versions FK is added via standalone `ALTER TABLE predictions ADD CONSTRAINT fk_model_version` block in schema.sql after both tables exist).
> - **If has JSONB columns:** document at § 4.1.<table>; cross-reference § 5.2 JSONB conventions for the shape documentation. JSONB columns verified at draft time:
>   - `predictions.feature_importance` (JSONB) — per schema.sql verified by QB
>   - `wr_predictions.feature_importance` (JSONB DEFAULT '{}') — per migration 005
>   - `pl_predictions.feature_importance` (JSONB DEFAULT '{}') — per migration 005
>   - `ls_predictions.feature_importance` (JSONB DEFAULT '{}') — per migration 005
>   - `model_versions.feature_list` (JSONB) — per schema.sql
>   - `model_versions.hyperparameters` (JSONB) — per schema.sql
>   - **No `model_versions.metadata` column exists** (QB substrate verification 2026-05-05; the QB handoff Section 8.3 incorrectly cited `model_versions.metadata`; the column does NOT exist in schema.sql nor in any verified migration). CC verifies this independently at draft time via `grep -i "metadata" backend/database/schema/schema.sql backend/database/migrations/*.sql`; expected output: zero hits in CREATE TABLE / ALTER TABLE statements for model_versions.
>   - Other JSONB fields surfacing during draft-time substrate verification — enumerate.
> - **If has approximate row count available from live dashboard or DB:** cite count with verification log entry. The legacy `predictions` table count (META_PLAN v9 inheritance: 6,600 rows) requires re-verification at draft time per Lesson 2 cross-project contamination check + § 4.5 Tier 3 source-priority. **CC verifies this via the dashboard endpoint (`GET https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com/dashboard/metrics`, served by `equine-inference` Active Lambda) or via direct SQL if DB credentials available.** If verification fails (Lambda transient error, dashboard schema change), document as "row count last verified <date> via <source>; pending re-verification" and route the gap to PHASE_5_BACKLOG.md per § 7.8 (do NOT fabricate a count). Cross-reference verification log Section C entry.
> - **If has indexes:** enumerate the secondary indexes (e.g., `idx_races_date`, `idx_pp_horse`, etc.) per `CREATE INDEX` statements in schema.sql + migration ALTER INDEX/CREATE INDEX statements. Indexes are referential — index existence is a query-performance discipline; index names are stable identifiers cross-bible references can rely on.
>
> **§ 4.1 enumeration order (recommended-strongly):** numerical/chronological per CREATE TABLE order in (schema.sql first, then migrations by NNN ascending); within schema.sql, the order in the file is: tracks (1), horses (2), trainers (3), jockeys (4), races (5), entries (6), past_performances (7), workouts (8), results (9), predictions (10), model_versions (11). Migration 005 adds: wr_predictions (12), pl_predictions (13), ls_predictions (14). Drafter latitude per § 5.2: drafter MAY reorder by domain grouping (e.g., entity tables first → race-context tables → prediction tables) if locality of reference benefits.
>
> **§ 4.2 Migration discipline:**
> - Per META_PLAN v9 § 7.12 grandfathering rule:
>   - Migrations 001–011 (existing) keep `NNN_short_description.sql` format. **No renaming.** No Phase 0 prerequisite to update.
>   - Migration 012 onward uses `NNN_YYYYMMDD_short_description.sql`. The date in the filename is the date the migration was authored. Bible entry for migration 012 documents the cutover and rationale.
>   - The duplicate-005 case (`005_backfill_pace_delta.sql` and `005_three_prediction_tables.sql`) is an inherited problem; lexical sort orders them deterministically; the runner sees both as opaque distinct filenames per `migrate.py:run_migrations` `sorted(*.sql)` iteration. Phase 1 audit documents it; remediation lives in `PHASE_5_BACKLOG.md`. The forward rule (no new duplicates) applies to Phase 5 onward. **No Phase 0 action.**
> - 12 existing migrations (verified by QB list_directory 2026-05-05): 001_initial_schema.sql, 002_fix_race_type_length.sql, 003_widen_varchar_columns.sql, 004_backfill_running_style.sql, 005_backfill_pace_delta.sql, 005_three_prediction_tables.sql, 006_backfill_early_pace_pressure.sql, 007_backfill_trainer_name.sql, 008_create_trainer_stats.sql, 009_backfill_pace_delta_v2.sql, 010_ls_predictions_first_class.sql, 011_wr_predictions_unique_fix.sql.
> - Decomposition: **12 .sql files = 11 NNN-prefix numbers (001–011) + 1 duplicate-005 file**. Document this decomposition in § 4.2.1 + verification log Section C with the `ls backend/database/migrations/*.sql | wc -l` verification command (expected: 12).
> - § 4.2.3 schema_migrations runner mechanism: document the table CREATE inside `ensure_migrations_table`, the `get_applied_migrations` set semantics, and the `sorted(*.sql)` iteration order in `run_migrations`. Cross-reference verification log Section C entry that quotes the relevant migrate.py lines.
> - § 4.2.4 Rollback format: in-file down-block; runner does NOT auto-execute; rollback is operator-driven. Cite the worked example structure from META_PLAN v9 § 7.12 (the hypothetical migration 012 illustrative example showing up + DOWN MIGRATION blocks).
> - § 4.2.5 Migration testing per META_PLAN v9 § 7.12: non-production database first; "non-production" definition currently is local Postgres matching production engine version (PostgreSQL 16.6) OR a dedicated dev RDS instance (which does NOT currently exist for EE — Phase 5 backlog candidate). Production engine is standalone RDS PostgreSQL 16.6 `equine-db` (NOT Aurora — V9 § 2.3 + Architecture Overview § 3.3).
>
> **§ 5 Discipline rules (sections 5–8 mandatory per § 5.2):**
>
> Per § 5.7 candidate-roster workflow:
> - § 5.1 UNIQUE constraints: candidate Forbidden Pattern surfaced by migration 011's wr_predictions UNIQUE constraint redesign — "Including per-horse dispatch metadata in a UNIQUE constraint when the dispatch is cross-row coherent at the (race, horse) level" (the model_used inclusion produced 427 duplicate rows across 157 races per migration 011's pre-state DO block). Provisionally numbered 5.1.
> - § 5.2 JSONB conventions: JSONB shape documentation per § 4.1 sub-bullet enumeration. Mandatory fields: schema description for each JSONB column (what keys are expected, what types, what defaults). For `model_versions.feature_list`: documents the canonical feature schema for that model version (cross-reference forward to `feature_provenance_bible:4.2` for per-model feature consumption). For `model_versions.hyperparameters`: training-time hyperparameter snapshot. For `predictions.feature_importance` / `wr/pl/ls_predictions.feature_importance`: per-prediction feature importance map (XGBoost SHAP values or similar; verify shape at draft time via sample SELECT or by reading the writer code). Provisionally numbered 5.2.
> - § 5.3 Cross-table FK conventions: candidate Common Mistake — "writing to a child table without verifying parent row exists." UUID FKs throughout; ON DELETE behavior unspecified in schema (default: NO ACTION). Provisionally numbered 5.3.
> - Additional rules surfaced by CC during candidate-roster enumeration: surface per § 5.7 workflow with substrate evidence. CC produces verification log Section C entries enumerating each candidate's substrate provenance (CC-introduced vs grandfathered from prior locked Phase 0 / Architecture Overview content).
>
> **§ 6 Currently Open:**
> - Per BIBLE_STRUCTURE_SPEC v6 § 5.3 cross-cutting bug Currently Open scope rule: bugs whose symptoms touch this bible's domain appear in § 6 as one-line cross-references to canonical-home bible (in `<bible>:#<bug-id>` format). Substantive description lives in canonical-home bible.
> - Bug #28 column-shift symptoms touch the `results` table directly (NULL `win_payout` and `daily_double_payout` since 2026-04-30). Bug #28's canonical home is `data_pipeline_bible:8.W.<n>` (per § 5.3 cross-cutting bug scope rule — the prevention is a data-acquisition discipline, NOT a schema discipline). § 6 in this bible carries a one-line cross-reference: `Bug #28 NULL payout fields in results table — canonical: data_pipeline_bible:#28`.
> - Empty-section explicit rule per § 5.2: if no other Currently Open entries surface, document explicitly with "No additional current open issues at lock."
>
> **§ 7 Deprecated:**
> - § 7.1 Legacy `predictions` table — canonical home for the legacy-table deprecated entry per BIBLE_STRUCTURE_SPEC v6 § 6.6 + META_PLAN v9 Appendix A.4 worked example. Per § 5.6.4 mandatory + conditional fields:
>   - Field/Module name: `predictions` table
>   - Canonical source: `wr_predictions` (per-style WR), `pl_predictions` (P&L), `ls_predictions` (LS enrichment) — created by migration 005 (`005_three_prediction_tables.sql`)
>   - Notes: 6,600 rows at last verification (META_PLAN v9 inheritance; CC re-verifies via dashboard at draft time per Lesson 2). Active readers (per QB substrate read of META_PLAN v9 Appendix A.4): `prediction_router.py` (3 instantiations of PredictionRepository at lines 34, 61, 92, plus 1 import on line 6 = 4 references total), `race_router.py` (1 instantiation on line 277, plus 1 import on line 273 = 2 references total), `dashboard_router.py:93,105` (direct SELECT for race-record summaries), `horse_router.py:66` (direct SELECT in horse-PPs query). **CC re-verifies reader inventory at draft time** per Lesson 2 + § 4.5 Tier 4 source-priority; if inventory has drifted (new readers added; old readers removed), document the drift with verification log Section C entry.
>   - Phase 5 backlog reference: `Phase 5.X.Y` placeholder (per META_PLAN v9 Appendix A lead paragraph scope clause — this is forward-looking discipline; the Phase 5 entry's specific identifier doesn't exist until PHASE_5_BACKLOG.md gains the entry).
>   - Conditional triggers (per § 5.6.1.2 tertiary-state notation):
>     - if-deprecated-thing-has-active-readers: FIRES (4 readers enumerated above)
>     - if-deprecation-is-partial: FIRES (table exists, has active readers; no path slated for immediate removal)
>     - if-deprecation-produced-Forbidden-Pattern: CONDITIONAL — candidate Forbidden Pattern at § 5.X "MUST NOT write to legacy `predictions` table" (writes are blocked by routing all new inference paths to per-pipeline tables; the legacy table is read-only at present). Adjacent prose caveat: the Forbidden Pattern hasn't been explicitly ratified in this bible's § 5 candidate roster yet; QB ratifies during § 5.7 review cycle.
>     - if-deprecated-thing-is-superseded-SQL-constraint-or-schema-element: DOES NOT FIRE (not a constraint; a table). Per § 5.6.4 G2 verification clause: per-table is distinct from per-constraint scope.
>
> **§ 8 What Was Fixed:**
> - § 5.6.1 mandatory + conditional fields. Mandatory Fix date in YYYY-MM-DD form per § 5.2 (G3 closure: discipline codifications without Fix date go to § 5, NOT § 8).
> - **Migration 011's wr_predictions UNIQUE constraint fix is a candidate W.N entry.** Bug name: "wr_predictions UNIQUE constraint included per-horse dispatch metadata that doesn't conflict cross-row, accumulating duplicates." Per § 5.5.1 global Bug #N convention: this surfaces a NEW global Bug #N to assign (Bug #N where N is the next available global identifier; QB confirms N at ratification). Fix date per § 7.3 placeholder-resolution sub-rule: CC runs `git log --format="%cs %s" -- backend/database/migrations/011_wr_predictions_unique_fix.sql` and uses the actual commit date (NOT a placeholder; per § 7.3 the placeholder convention is reserved for forward-looking discipline + Appendix A worked examples).
> - Symptom: 157 races (~1.35% of 11,629) accumulated 427 duplicate rows in wr_predictions; downstream consumers (LS softmax, ComparePage Cartesian, track_record double-counting) read both variants without filtering model_used.
> - Root cause: UNIQUE (race_id, entry_id, model_used, style) included `model_used` (a per-horse dispatch metadata flag set by `WRInferenceService.predict_race` based on workout availability — each horse goes through ONE model variant per inference, never both). When workout data lands between inference runs, the same (race_id, entry_id, style) accumulates a 'core' row AND a 'full' row; the new variant doesn't conflict with the old key, so both persist.
> - Fix: matched the PL / LS pattern — UNIQUE (race_id, entry_id, style). model_used stays as a metadata column; the latest variant overwrites cleanly via the existing SET clause in WR repo's INSERT statement. Cleanup deleted older duplicates per the `ROW_NUMBER() OVER (PARTITION BY race_id, entry_id, style ORDER BY created_at DESC, prediction_id DESC)` query.
> - Why this entry exists: prevents recurrence of "include per-horse dispatch metadata in UNIQUE constraint when the dispatch is cross-row coherent at the (race, horse) level"; this is a schema-design discipline that this bible's § 5 codifies as Forbidden Pattern.
> - Conditional triggers (per § 5.6.1.2 tertiary-state notation):
>   - if-fix-involved-migration: FIRES (migration 011_wr_predictions_unique_fix.sql)
>   - if-fix-invalidated-prior-content: DOES NOT FIRE (no prior bible content existed at fix time — pre-Phase-1)
>   - if-fix-produced-Forbidden-Pattern: FIRES (cross-reference to § 5.1 Forbidden Pattern candidate at § 5.7 workflow)
>   - if-fix-touches-multiple-bibles: DOES NOT FIRE — schema-design discipline is canonically homed in this bible per § 5.3 cross-cutting bug scope rule (no other bible's discipline more directly prevents recurrence).
> - Empty-section explicit rule per § 5.2: if no other W.N entries surface, document explicitly. Migration 011 fix is the candidate v1 W.N entry; additional W.N entries surface as substrate verification reveals other historical bugs whose canonical home is this bible (e.g., the duplicate-005 case is inherited problem, not a fix that was applied; document as Currently Open if relevant, NOT § 8).
>
> ---
>
> ### Companion verification log structure
>
> File location: `/home/strakajagr/projects/equine-equalizer/docs/bible/_audit/database_schema_bible_v1_verification.md` (note: `_audit/` singular per META_PLAN v9 § 3.8; Phase 1 docs live there, NOT in `_meta/_audits/` plural).
>
> Section structure per QB handoff § 7.2:
> - **Section A:** inherited claims from upstream Phase 0 verification logs (META_PLAN v9 verification log entries this draft inherits) with re-verification timestamps
> - **Section B:** inherited claims from prior cycles of THIS bible's verification log (NOT applicable for v1 — first cycle)
> - **Section C:** new V1-N claims with primary citations. Each factual claim about EE has a V1-N entry per Tier 3 discipline.
> - **Section D:** methodology-interpolation self-check (target: ZERO new methodology constructs CC introduces beyond what this spec ratifies). For each new construct CC introduces (terminology, framing, rule), surface here with provenance.
> - **Section E:** pattern-completion check (W.N exclusivity preserved — no new letter-prefixes introduced; numeric IDs honored per § 5.5 + G-new-1)
> - **Section F:** FRAMEWORK_GAP / SPEC_GAP markers (target: ZERO unless surfaced honestly with substrate-cited reframing per Lesson 4)
> - **Section G:** prior-cycle audit findings closure verification (NOT applicable for v1)
> - **Section H:** QB self-audit log (reproduce char-exact from this spec's § 6 — operative for traceability)
> - **Section I:** new entries for surgical patch operations (NOT applicable for v1 — first cycle is full draft, not surgical patch)
>
> ### Substrate-anchored verification claims CC must produce (Section C entries)
>
> Each item below corresponds to a Section C V1-N claim CC must produce in the verification log:
>
> 1. **V1-1: 14 tables decomposed.** Verification command: `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql | grep -v "schema_migrations"`. Expected: 14 distinct table-name matches. Decomposition: 11 from schema.sql (tracks, horses, trainers, jockeys, races, entries, past_performances, workouts, results, predictions, model_versions) + 3 from 005_three_prediction_tables.sql (wr_predictions, pl_predictions, ls_predictions). Targeted vs total distinction (Check 9): the grep above counts ALL CREATE TABLE statements including legitimate ones; the decomposition is what this verification claims, NOT a count of statements being added/changed (this is full draft, no patch).
> 2. **V1-2: 1 materialized view.** Verification command: `grep -hE "^CREATE MATERIALIZED VIEW" backend/database/schema/schema.sql backend/database/migrations/*.sql`. Expected: 1 match (`trainer_stats` from 008_create_trainer_stats.sql).
> 3. **V1-3: 12 migration files; 11 NNN-prefix numbers + 1 duplicate-005.** Verification command: `ls backend/database/migrations/*.sql | wc -l` and `ls backend/database/migrations/*.sql`. Expected: 12 .sql files; the duplicate-005 case is `005_backfill_pace_delta.sql` and `005_three_prediction_tables.sql`.
> 4. **V1-4: schema_migrations runner table is created at runtime by migrate.py.** Verification command: `grep -A 8 "ensure_migrations_table" backend/database/migrations/migrate.py`. Expected: function definition with `CREATE TABLE IF NOT EXISTS schema_migrations` body.
> 5. **V1-5: model_versions JSONB columns.** Verification command: `grep -E "JSONB" backend/database/schema/schema.sql backend/database/migrations/*.sql`. Expected enumeration: model_versions.feature_list (JSONB), model_versions.hyperparameters (JSONB), predictions.feature_importance (JSONB), wr_predictions.feature_importance (JSONB DEFAULT '{}'), pl_predictions.feature_importance (JSONB DEFAULT '{}'), ls_predictions.feature_importance (JSONB DEFAULT '{}'). NO `model_versions.metadata` column. Decomposition: 6 JSONB columns total across 5 tables.
> 6. **V1-6: model_versions.metadata column does NOT exist.** Verification command: `grep -i "metadata" backend/database/schema/schema.sql backend/database/migrations/*.sql | grep -v "^--"`. Expected: zero matches in CREATE/ALTER TABLE statements that target model_versions. (Reason for this V1-N: the QB handoff Section 8.3 incorrectly cited `model_versions.metadata`; per Lesson 1 cross-project contamination check + Check 1 cross-reference accuracy, this needs explicit substrate-grounded refutation in CC's verification log to prevent inheritance into the bible.)
> 7. **V1-7: Migration 011's wr_predictions UNIQUE constraint change is documented.** Verification command: `cat backend/database/migrations/011_wr_predictions_unique_fix.sql | grep -E "(DROP CONSTRAINT|ADD CONSTRAINT)"`. Expected: `DROP CONSTRAINT IF EXISTS wr_predictions_unique_per_entry_model_style` + `ADD CONSTRAINT wr_predictions_unique_per_entry_style UNIQUE (race_id, entry_id, style)`. Per G2: prior superseded form physically dropped → no Deprecated entry needed.
> 8. **V1-8: Migration 011 fix date.** Verification command: `git log --format="%cs %h %s" -- backend/database/migrations/011_wr_predictions_unique_fix.sql | tail -1`. Expected: a YYYY-MM-DD date from `git log` (the commit-date of the migration's first commit). Per § 7.3 placeholder-resolution sub-rule, this date is mandatory for the W.N entry — NO PLACEHOLDER. If git log returns empty (file uncommitted), document that the file is uncommitted and route to operator for commit before bible lock per § 3.1.1.
> 9. **V1-9: Calibration bypass at wr_inference_service.py:616-626.** Verification command: `sed -n '614,628p' backend/services/wr_inference_service.py`. Expected: comment block at lines 616–625 reading "All styles (including gonzo_sauce) bypass calibration at inference tonight" + bypass operation at line 626 `handicapping_probs = ranker_probs.copy()`. (Cross-reference for § 4.1.<predictions> writers section + § 5 calibration discipline cross-reference forward to ml_layer_architecture_bible:4.3.)
> 10. **V1-10: Architecture Overview § 4.1 line numbers for canonical objects (line-shift-resistant via section-anchored citation per Check 8).** Verification command: read `/home/strakajagr/projects/equine-equalizer/docs/bible/architecture_overview.md` § 4.1 ("Race / Entry / PastPerformance / Workout / Result / Prediction (`backend/models/canonical.py`)"). Expected: section content reproduces 14-class verification with line numbers Race=255, Entry=214, PastPerformance=77, Workout=58, Result=296, Prediction=428. **CC cross-references Architecture Overview § 4.1 by section-anchor (`architecture_overview:4.1`) NOT by literal line number, per Check 8.**
> 11. **V1-11: Legacy `predictions` table reader inventory re-verification per Lesson 2.** Verification commands: `grep -nE "(import.*PredictionRepository|PredictionRepository\(|predictions\b)" backend/routers/prediction_router.py backend/routers/race_router.py backend/routers/dashboard_router.py backend/routers/horse_router.py`. Expected: confirms the META_PLAN v9 Appendix A.4 reader inventory or surfaces drift. Decomposition: prediction_router.py 3 instantiations + 1 import = 4 refs; race_router.py 1 instantiation + 1 import = 2 refs; dashboard_router.py 2 SELECT lines (93, 105); horse_router.py 1 SELECT line (66). If inventory drifted, surface in V1-11 with substrate-cited correction.
> 12. **V1-12: Legacy `predictions` table row count.** Verification command: dashboard endpoint GET `https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com/dashboard/metrics`, extract `counts.predictions` field. Expected: an integer ≥ 0 (META_PLAN v9 inheritance: 6,600). If the value drifted from 6,600, surface in V1-12 with verification timestamp; the live count IS the bible value at lock per § 4.5 Tier 2 / Tier 3 source-priority. If endpoint unavailable, route gap to PHASE_5_BACKLOG and document in Section F.
>
> Additional V1-N entries arise from CC's per-table substrate reads — one per (table × FK constraint), one per (JSONB column × shape), one per (migration × purpose), etc. Aim for verification log entries that decompose every aggregable count and cite primary commands.
>
> ### Bash-grep verification predictions (Check 9 precision)
>
> Each prediction below distinguishes targeted-by-this-draft from total-on-disk-after-draft:
>
> - **`grep -c "CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql`** → expected total ≥ 14 (the 14 domain tables; possibly more if `IF NOT EXISTS CREATE TABLE schema_migrations` lines also count, which they do). The targeted-by-this-draft count is **0** (this is full prose authoring, not a patch with prescribed line edits). The total disk count is what the grep returns; CC documents the actual total in V1-1 with explicit decomposition (14 domain + N runner internals).
> - **`grep -c "JSONB" backend/database/schema/schema.sql backend/database/migrations/*.sql`** → expected total ≥ 6 (the 6 JSONB column declarations per V1-5). CC documents the actual total in V1-5 with decomposition. Targeted-by-this-draft: 0.
> - **`grep -c "metadata" backend/database/schema/schema.sql backend/database/migrations/*.sql`** → if there are zero matches in non-comment lines, the V1-6 refutation is verified. If there are matches, surface in Section F as substrate gap and reframe the bible's content to NOT cite `model_versions.metadata`.
> - **`ls backend/database/migrations/*.sql | wc -l`** → expected total = **12** (per V1-3). Targeted-by-this-draft: 0.
> - **`grep -c "Bug #28" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md` (after CC writes draft)** → expected total = **1** (the one cross-reference at § 6 to `data_pipeline_bible:#28`). Targeted-by-this-draft: 1 (CC writes the cross-reference); if total > 1, CC has duplicated the cross-reference (forbidden per § 5.3 no-duplication mandate); CC fixes before submission.
> - **`grep -c "trainer_stats" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md` (after CC writes draft)** → expected total ≥ 1 (matview reference at § 3.2; possibly more if reader inventory section cross-references the matview's reader). Targeted-by-this-draft: ≥ 1. **Critical: zero matches at § 4.1 (G-new-2 closure operative — matview must NOT appear at any 4.1.X position).** CC verifies this explicitly via `awk '/^### 4\.1/,/^### 4\.2/' database_schema_bible.md | grep -c "trainer_stats"` → expected: 0.
>
> ### Skip-audit pre-approval determination
>
> **Skip-audit does NOT apply.** This is initial v1 full-draft authoring, not a surgical-cosmetic patch cycle. Standard Phase 1 cycle process applies per QB handoff § 6.1: CC drafts → QB reviews + spot-checks → audit-CC adversarial pass → iterate to lock against threshold. The 4-condition skip-audit criteria (surgical-cosmetic scope; char-exact reproduction discipline; zero new methodology constructs; zero new substantive content beyond audit-finding closures) do not all hold — full prose authoring includes substantive content beyond audit-finding closures.
>
> ### Iteration expectation
>
> Per Option 1 with 9 checks operative trajectory expectation (QB handoff § 3.4): if audit-CC catches NO new QB drafting-spec error class beyond the 10 banked errors, Option 1 is converging. If audit-CC catches a new QB drafting-spec error class, bank as Check 10 and revise cluster framing if it doesn't fit Substrate / Content / Workflow categorization.
>
> Tony's lock threshold per META_PLAN v9 § 11 + QB handoff § 6.5: zero fabricated content + zero methodology-interpolation findings + < 5 MATERIAL findings + zero un-closed prior-cycle findings. Database & Schema Bible v1 has no prior cycle, so the regression check trivializes; the other 3 conditions apply.
>
> ### Closing reminder for CC
>
> 1. Read all 10 reference materials BEFORE drafting.
> 2. Run substrate verifications per V1-1 through V1-12 BEFORE writing per-section content; populate the verification log Section C as you go.
> 3. Surface FRAMEWORK_GAP / SPEC_GAP markers in Section F with substrate-cited candidate reframing per Lesson 4.
> 4. Reproduce QB self-audit log entries char-exact in Section H per QB handoff § 7.2.
> 5. Numeric sub-section IDs only — no provisional letter-prefixes (G-new-1).
> 6. Matview at § 3 only — never at § 4.1 (G-new-2).
> 7. Decompose every aggregable count per § 6.5 verification log precision rule.
> 8. Cross-references to Architecture Overview use section-anchored format (`architecture_overview:4.1`), NOT literal line numbers (Check 8).
>
> Begin.

---

## 2. Reference materials and source-priority discipline (QB-side)

This section is QB context for spec authorship discipline. Not part of the CC paste-prompt.

The 10 reference materials enumerated in the paste-prompt § "Reference materials" subsection are the load-bearing substrate inputs. Per Lesson 3 (re-expanded), this drafting spec cites primary verification log claim IDs (V1-N format) AND the underlying primary substrate (file paths, grep commands, migration file contents) — NOT paraphrased restatements of META_PLAN or BIBLE_STRUCTURE_SPEC.

Source-priority hierarchy (META_PLAN v9 § 4.5) operative for the bible's content:
1. Live AWS state — for any infrastructure-context claim (e.g., "what runtime is `equine-db`?")
2. Live API endpoints — for runtime data state (e.g., "how many rows in `predictions` at lock?")
3. Live DB state — for data-state claims when Lambda-mediated path unavailable
4. Working-tree code (post-baseline 87dec36) — for "what does the schema/migration declare?"
5. Operator-stated history — for "why decisions were made"
6. EE_CURRENT_STATE_DUMP.md — best-available baseline only; **subject to Lesson 1 cross-project contamination check**
7. Session logs — tertiary

The Database & Schema Bible draws primarily from Tier 4 (working-tree schema.sql + migrations + canonical.py) and Tier 2/3 (live row counts via dashboard or DB). Tier 1 (AWS) is referenced for the RDS instance metadata cross-referenced from Architecture Overview § 3.3.

---

## 3. Operating disciplines CC must follow (QB-side)

Spec authorship discipline ratifies the CC operating disciplines enumerated in the paste-prompt's "Verification discipline" + "Methodology lessons 1–6" subsections. These map to the 9-check Option 1 framework:

- Substrate verification cluster (Checks 1–3): cross-reference accuracy, count/arithmetic accuracy, substrate-grounded reframing
- Content verification cluster (Checks 4–6): definition-framing internal consistency, synthesis verification, audit-CC enumeration completeness
- Workflow verification cluster (Checks 7–9): mid-cycle scope extension narrative discipline, line-shift-resistant citations, bash-grep prediction precision

Each check is operative on QB during this spec authorship; the spec's § 11 (QB substrate-verification log) is the audit-trail.

---

## 4. Prescribed TOC and per-section drafting guidance (QB-side substrate anchors)

The paste-prompt's "Prescribed TOC" + "Per-section content requirements" subsections reproduce BIBLE_STRUCTURE_SPEC v6 § 6.6 normatively. QB substrate anchoring confirms:

| Anchor | Substrate-verified | Source |
|---|---|---|
| 14 tables | ✅ V1-1 | QB read of schema.sql + 005_three_prediction_tables.sql |
| 1 matview (`trainer_stats`) | ✅ V1-2 | QB read of 008_create_trainer_stats.sql |
| 12 migration files (11 NNN + 1 duplicate-005) | ✅ V1-3 | QB list_directory of backend/database/migrations |
| schema_migrations runner | ✅ V1-4 | QB read of migrate.py:ensure_migrations_table |
| 6 JSONB columns across 5 tables | ✅ V1-5 | QB read of schema.sql + 005_three_prediction_tables.sql |
| model_versions.metadata does NOT exist | ✅ V1-6 | QB read of schema.sql + all migrations (no metadata column) |
| Migration 011 wr_predictions UNIQUE swap | ✅ V1-7 | QB read of 011_wr_predictions_unique_fix.sql |
| Migration 011 fix date | ⚠️ V1-8 (CC must run git log) | QB cannot execute git in sandbox |
| Calibration bypass wr_inference_service.py:616-626 | ✅ V1-9 | QB read of wr_inference_service.py |
| canonical.py 14 dataclasses + line numbers | ✅ V1-10 | QB read of canonical.py confirms structure consistent with Architecture Overview § 4.1 |
| Legacy predictions table reader inventory | ⚠️ V1-11 (CC re-verifies) | META_PLAN v9 inheritance per Lesson 2 |
| Legacy predictions row count (~6,600) | ⚠️ V1-12 (CC re-verifies via dashboard) | META_PLAN v9 inheritance |

Items marked ⚠️ are CC-verified at draft time per Tier 2/3 source-priority; QB cannot run them from sandbox.

---

## 5. Verification log structure (QB-side)

The paste-prompt's "Companion verification log structure" subsection prescribes the Section A–I structure per QB handoff § 7.2. QB-side note: Section A inherits from META_PLAN v9 verification log + Architecture Overview v3 verification log; Section B is empty (v1 first cycle); Section C is the new V1-N entries enumerated above; Section D self-audit target ZERO; Section E pattern-completion preserves W.N exclusivity; Section F surfaces gaps with candidate reframing; Section G empty (v1 first cycle); Section H reproduces this spec's § 6 char-exact; Section I empty (full draft, not surgical patch).

---

## 6. QB self-audit log Section H entries (reproduced char-exact in CC's verification log Section H)

The 9 entries below are the Option 1 self-audit log for QB's spec authorship cycle. CC reproduces these char-exact in the verification log Section H per QB handoff § 7.2.

### H1 — Check 1 (cross-reference accuracy) self-audit

**Cross-references prescribed in this spec verified against substrate:**

- BIBLE_STRUCTURE_SPEC v6 § 6.6 → verified by QB direct read 2026-05-05; section spans from `### 6.6 database_schema_bible.md` header to `### 6.7 api_frontend_bible.md` header. Per-section guidance read in full.
- BIBLE_STRUCTURE_SPEC v6 § 5.5 + § 5.6 → verified by QB direct read 2026-05-05; W.N format, Forbidden Pattern, Common Mistakes, Deprecated entry templates confirmed at the cited section IDs.
- META_PLAN v9 § 4.5 → verified; source-priority hierarchy (Tier 1–Tier 7) at this section ID.
- META_PLAN v9 § 6.5 → verified; verification log precision rule at this section ID.
- META_PLAN v9 § 7.3 placeholder-resolution sub-rule → verified; locked v7, sub-rule paragraph in § 7.3.
- META_PLAN v9 § 7.12 → verified; migration discipline at this section ID.
- META_PLAN v9 § 9.13 → verified; multi-active-row reality of model_versions at this section ID.
- Architecture Overview § 3.3 (RDS PostgreSQL) → verified; per QB direct read 2026-05-05.
- Architecture Overview § 4.1 (canonical objects + line numbers) → verified; line numbers Race=255, Entry=214, PastPerformance=77, Workout=58, Result=296, Prediction=428 consistent with QB read of canonical.py.
- Architecture Overview § 3.6 (EventBridge schedule) → cross-referenced in spec for cross-runtime context; not directly cited as load-bearing for this bible.

**Banked Check 1 finding from handoff (carried forward to spec § 10):** QB handoff Section 8.3 cited "META_PLAN v9 § 9.10 + § 9.11 govern JSONB conventions" — VERIFIED INACCURATE. § 9.10 is "current bug list in narrative form" (anti-pattern about Currently Open formatting); § 9.11 is "Pretending feature engineering has one source of truth" (FE drift anti-pattern). Neither addresses JSONB. The actual JSONB conventions live in: (a) schema.sql declarations (substrate Tier 4); (b) BIBLE_STRUCTURE_SPEC v6 § 6.6 § 5.2 prescription (methodology); (c) canonical.py dataclass definitions (substrate Tier 4). Spec corrects the cross-reference: JSONB conventions section guidance cites schema.sql + canonical.py + § 5.2 directly, NOT § 9.10/§ 9.11.

### H2 — Check 2 (count/arithmetic accuracy) self-audit

**Counts decomposed per META_PLAN v9 § 6.5 verification log precision rule:**

- 14 tables = 11 (schema.sql) + 3 (005_three_prediction_tables.sql)
- 1 matview (trainer_stats from 008_create_trainer_stats.sql)
- 12 migration files = 11 NNN-prefix numbers + 1 duplicate-005 file
- 6 JSONB columns = 1 (predictions) + 1 (wr_predictions) + 1 (pl_predictions) + 1 (ls_predictions) + 2 (model_versions.feature_list + model_versions.hyperparameters)
- model_versions has 21 columns at present = 17 base from schema.sql + 4 added by 005 (model_type, flat_bet_roi, kelly_roi, value_bet_win_rate)

Single-source citation: each count statement above traces to a specific V1-N verification log claim CC produces. No multi-paraphrase counts (the v9 § 12.1 8-vs-9 drift pattern explicitly avoided).

### H3 — Check 3 (substrate-grounded reframing) self-audit

**Reframings introduced in this spec are substrate-grounded:**

- Migration 011's pre-state UNIQUE constraint name `wr_predictions_unique_per_entry_model_style` and post-state name `wr_predictions_unique_per_entry_style` — verified by QB direct read of 011_wr_predictions_unique_fix.sql (lines `DROP CONSTRAINT IF EXISTS` + `ADD CONSTRAINT`). Reframing of "what changed" cites primary substrate, not paraphrased.
- Calibration bypass at wr_inference_service.py:616-626 — verified by QB direct read; comment block lines 616–625 + bypass operation at line 626 confirmed. The "All styles (including gonzo_sauce) bypass calibration at inference tonight" prose verified at line 617.
- Predictions-table family canonical resolution — verified: predictions table at schema.sql:CREATE TABLE 10; wr_predictions/pl_predictions/ls_predictions at 005_three_prediction_tables.sql; the predictions↔model_versions FK at schema.sql ALTER TABLE block.

**Banked Check 3 finding from handoff (carried forward to spec § 10):** QB handoff Section 8.3 cited `model_versions.metadata` as a JSONB column. VERIFIED REFUTED — `model_versions` columns per schema.sql + migration 005 ALTER TABLE blocks: model_version_id, version_name, training_date, training_data_start, training_data_end, training_race_count, exacta_hit_rate, trifecta_hit_rate, top1_accuracy, top3_accuracy, calibration_score, feature_list (JSONB), hyperparameters (JSONB), s3_artifact_path, is_active, notes (TEXT), created_at, model_type (added 005), flat_bet_roi (added 005), kelly_roi (added 005), value_bet_win_rate (added 005). 21 columns total; `metadata` does NOT exist. Spec V1-6 is the substrate-grounded refutation entry CC produces.

### H4 — Check 4 (definition-framing internal consistency) self-audit

**Definitions and enumerations reconcile internally:**

- § 2 Definitions enumerated terms (table, materialized view, migration, JSONB shadow, canonical column, primary writer, primary reader, schema_migrations table) match § 3 sub-section enumeration (3.1 14 tables, 3.2 1 matview, 3.3 schema bootstrap vs migrations) and § 4 sub-section enumeration (4.1 per-table, 4.2 migration discipline). The `schema_migrations` table is defined in § 2 AND documented in § 3.3 / § 4.2.3 (runner mechanism); both references converge.
- 14 tables in § 3.1 enumeration matches 14 sub-sections at § 4.1.X (one per CREATE TABLE; matview NOT enumerated per G-new-2 closure).
- § 4.1 first-sentence qualification "CREATE TABLE declarations only" reconciles with § 2's table-vs-matview distinction: matview is defined separately and lives at § 3 only.

No § 2 N-category vs § 3 N-sub-section mismatch (the v2 audit G3 EventBridge omission pattern explicitly avoided).

### H5 — Check 5 (synthesis verification) self-audit

**Synthesis-introduced upstream corrections substrate-verified:**

- The handoff cross-reference inaccuracies (§ 9.10/§ 9.11 govern JSONB; `model_versions.metadata`) are surfaced as QB-side findings (§ 10 + H1/H3) NOT propagated as upstream corrections to META_PLAN v9 / Architecture Overview. Per Lesson 6: the handoff's downstream finding does not propagate as upstream truth without QB substrate check. QB substrate-verified the inaccuracies — no META_PLAN v9 substrate update is needed because META_PLAN v9 itself doesn't make these claims; the handoff is a downstream synthesis artifact that mis-cited section anchors. QB corrects the spec, NOT the upstream documents.

- Bug #28 canonical-home assignment (`data_pipeline_bible:#28`) inherited from META_PLAN v9 § 1.2 + Appendix A.5 + BIBLE_STRUCTURE_SPEC v6 § 5.3 cross-cutting bug scope rule. Per Lesson 6: substrate-verified at QB read of META_PLAN v9 + BIBLE_STRUCTURE_SPEC v6 § 5.3 (cross-cutting bug scope rule explicitly assigns canonical home to "bible whose discipline most directly prevents recurrence" — for Bug #28 column-shift in scraper, prevention is data-acquisition discipline, NOT schema discipline). § 6 cross-reference in this bible follows the canonical-home rule.

### H6 — Check 6 (audit-CC enumeration completeness) self-audit

**No prior audit-CC enumeration to inherit (v1 first cycle).** Per Check 6: when QB inherits a count claim from audit-CC findings, QB grep-verifies the count against current disk state. v1 has no prior audit-CC findings. Forward-looking: when v2 audit-CC enumerates findings, QB substrate-verifies each before re-spec.

For META_PLAN v9 inheritance specifically, the Architecture Overview v1 verification log's Claims A.1–A.8 + V1-N are inherited at H1 cross-reference verification (not enumeration counts CC must verify). The handoff's verification log inheritance does not introduce enumeration counts requiring grep verification at this spec level.

### H7 — Check 7 (mid-cycle scope extensions) self-audit

**No mid-cycle scope extensions in this spec.** The spec authors v1 in a single pass. Forward-looking: if v2/v3 cycles extend scope post-CC-surfacing, QB enumerates ALL verification-log + main-doc sections referencing original scope and updates each per Check 7 discipline.

For this v1 spec specifically, the spec is the initial scope; no Section H/I sub-section updates required.

### H8 — Check 8 (line-shift-resistant citations) self-audit

**Line-number citations replaced with section-anchored citations:**

- `architecture_overview:4.1` for canonical objects, NOT Architecture Overview line numbers
- `architecture_overview:3.3` for RDS PostgreSQL runtime context
- `architecture_overview:3.6` for EventBridge schedule context
- BIBLE_STRUCTURE_SPEC `v6 § 6.6` (section anchor) for the prescribed TOC, NOT BIBLE_STRUCTURE_SPEC line ranges
- META_PLAN `v9 § 7.12` for migration discipline; `v9 § 4.5` for source-priority; `v9 § 9.13` for model_versions multi-active-row reality

Literal line numbers retained ONLY where canonical-substrate identification requires them:
- `wr_inference_service.py:616-626` — calibration bypass spans these lines; per Architecture Overview § 4.1's existing precedent for citing line ranges in source code, this is canonical-substrate citation NOT cross-reference.
- canonical.py line numbers (Race=255, etc.) — cited via Architecture Overview's existing § 4.1 enumeration; CC's bible cross-references Architecture Overview's section anchor, NOT the line numbers directly.
- Reader inventory line numbers in legacy predictions deprecation entry (e.g., prediction_router.py:34, 61, 92) — these are canonical-substrate identification, not cross-reference; line numbers in primary source code are stable identifiers per the v3 final-lock H5 lesson scope (line numbers acceptable when tightly scoped to canonical-substrate identification, NOT cross-reference).
- migration file paths cite the filename, not line numbers (e.g., `005_three_prediction_tables.sql` not `005_three_prediction_tables.sql:32-58`).

Cross-references between bibles use section IDs only; canonical-substrate citations to source code may include line numbers when tightly scoped.

### H9 — Check 9 (bash-grep verification predictions) self-audit

**Prescribed bash-grep predictions distinguish targeted vs total counts:**

Per spec § 7 "Bash-grep verification predictions (Check 9 precision)":

- `grep -c "CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql` → expected total ≥ 14; targeted-by-this-draft count = 0 (full prose authoring, not patch). CC documents actual total in V1-1 with explicit decomposition (14 domain tables + N runner-internal CREATE TABLE statements like `schema_migrations`).
- `grep -c "JSONB" ...` → expected total ≥ 6; targeted = 0.
- `grep -c "metadata" ...` → expected total = 0 in non-comment CREATE/ALTER TABLE contexts; if total > 0, surface in Section F as substrate gap.
- `ls backend/database/migrations/*.sql | wc -l` → expected total = 12; targeted = 0.
- `grep -c "Bug #28" database_schema_bible.md` (post-draft) → expected total = 1 (the single cross-reference at § 6); targeted = 1 (CC writes this one cross-reference).
- `awk '/^### 4\.1/,/^### 4\.2/' database_schema_bible.md | grep -c "trainer_stats"` → expected total = 0 (G-new-2 closure: matview must NOT appear at any 4.1.X position); targeted = 0.

Each prediction precisely scopes the pattern to distinguish "what this draft adds/changes" from "what's on disk." For full-draft authoring (this v1), targeted = 0 for substrate counts (CC verifies existing substrate, doesn't change it); targeted = 1 for newly-authored bible cross-references (Bug #28 cross-ref). The bash-grep predictions for the bible draft itself (post-draft) include precise total expectations CC can run after writing.

---

## 7. Bash-grep verification predictions (Check 9 precision; QB-side reproduced)

Reproduced for traceability. Same content as paste-prompt § "Bash-grep verification predictions (Check 9 precision)" subsection.

---

## 8. Skip-audit pre-approval determination (QB-side)

Skip-audit does NOT apply per spec § 1.1 paste-prompt "Skip-audit pre-approval determination" subsection. Standard Phase 1 cycle process applies.

---

## 9. Iteration expectation (QB-side)

Per Option 1 9-check trajectory expectation, this v1 cycle tests whether the 9-check framework converges. If audit-CC catches no new QB drafting-spec error class, Option 1 is converging. Banked outcomes:

- v1 audit clean against threshold (zero fab + zero methodology-interp + < 5 MATERIAL + zero un-closed) → bible locks v1; Option 1 declared converging at this measurement.
- v1 audit returns ≥ 1 new QB drafting-spec error class beyond the 10 banked → bank as Check 10; revise cluster framing if needed; v2 cycle re-applies the now-10-check framework.
- v1 audit returns 0–4 MATERIAL findings within the existing 9-check coverage → standard surgical-patch cycle; v2 closes findings; the 9-check framework stable.
- v1 audit returns ≥ 5 MATERIAL OR ≥ 1 BLOCKER → REVISE AND RE-AUDIT or SUBSTANTIAL REWORK per QB handoff § 6.5.

---

## 10. Handoff cross-reference corrections (banked Check 1 + Check 3 findings)

QB substrate-verification surfaced 2 cross-reference inaccuracies in the QB handoff document itself. Banked here for transparency; spec content corrects them; future handoff-document cycles can incorporate the corrections.

### 10.1 Handoff Section 8.3: "META_PLAN v9 § 9.10 + § 9.11 govern JSONB conventions"

**STATUS: INACCURATE.** QB direct read of META_PLAN v9 (2026-05-05) confirms:
- § 9.10 is "**The current bug list in narrative form**" — anti-pattern about Currently Open section formatting (open bugs go to triage queue; Currently Open is a numbered list with one-line descriptions and PHASE_5_BACKLOG.md pointers; narrative explanations belong in triage queue entries).
- § 9.11 is "**EE-specific anti-pattern: Pretending feature engineering has one source of truth**" — anti-pattern about FE drift between training-side `model/shared/data_loader.py` and inference-side `backend/services/feature_engineering_service.py`; documents the 14 Gonzo Sauce single-source extraction at `model/shared/gonzo_features.py`.

**Neither section addresses JSONB conventions.** Spec correction: JSONB conventions section guidance cites schema.sql + canonical.py + BIBLE_STRUCTURE_SPEC v6 § 6.6 § 5.2 directly. The actual META_PLAN content that informs JSONB conventions is § 4.5 source-priority (Tier 4 working-tree code is the canonical JSONB shape source).

### 10.2 Handoff Section 8.3: "model_versions.metadata (version-tracking metadata)"

**STATUS: REFUTED.** QB direct read of schema.sql + all 12 migration files (2026-05-05) confirms `model_versions` table columns:

`model_version_id, version_name, training_date, training_data_start, training_data_end, training_race_count, exacta_hit_rate, trifecta_hit_rate, top1_accuracy, top3_accuracy, calibration_score, feature_list (JSONB), hyperparameters (JSONB), s3_artifact_path, is_active, notes (TEXT), created_at, model_type (added by 005), flat_bet_roi (added by 005), kelly_roi (added by 005), value_bet_win_rate (added by 005)`.

21 columns total. **`metadata` is NOT a column.** Closest match: `notes TEXT` — but it's TEXT not JSONB.

Spec correction: V1-6 verification log entry CC produces explicitly refutes the `model_versions.metadata` claim with substrate-cited evidence. The bible's JSONB conventions section enumerates only the 6 actual JSONB columns (`feature_list`, `hyperparameters`, plus `feature_importance` in 4 prediction tables).

---

## 11. QB substrate-verification log (Option 1 9-check self-audit; QB-side authoritative record)

This section is the QB-side authoritative record of substrate verifications run during spec authorship. Sections 6.H1 through 6.H9 reproduce content from this log; Section 11 is the source.

### 11.1 Substrate verifications run by QB

| Anchor | Command (or read) | Result | Used in spec § |
|---|---|---|---|
| Migration directory listing | `dynasty-dugout:list_directory backend/database/migrations` | 12 .sql files + migrate.py; 11 NNN-prefixes + duplicate-005 | § 4.2 + V1-3 |
| schema.sql CREATE TABLE count | direct read of schema.sql | 11 CREATE TABLE statements (tracks, horses, trainers, jockeys, races, entries, past_performances, workouts, results, predictions, model_versions) | § 3.1 + V1-1 |
| 005_three_prediction_tables.sql | direct read | 3 CREATE TABLE (wr_predictions, pl_predictions, ls_predictions) + ALTER TABLE model_versions adding 4 columns | § 3.1 + V1-1 |
| 008_create_trainer_stats.sql | direct read | 1 CREATE MATERIALIZED VIEW (trainer_stats) + UNIQUE INDEX | § 3.2 + V1-2 |
| 011_wr_predictions_unique_fix.sql | direct read | DROP `wr_predictions_unique_per_entry_model_style`; ADD `wr_predictions_unique_per_entry_style UNIQUE (race_id, entry_id, style)` | § 4.1 wr_predictions + V1-7 |
| migrate.py runner mechanism | direct read of `ensure_migrations_table`, `get_applied_migrations`, `run_migrations` | schema_migrations table CREATE at runtime; sorted(*.sql) iteration | § 4.2.3 + V1-4 |
| canonical.py 14 dataclasses | direct read | Track, Horse, Trainer, Jockey, Workout, PastPerformance, Entry, Race, RaceCard, Result, ModelVersion, PLPrediction, LSPrediction, Prediction | § 4.1 cross-references + V1-10 |
| canonical.py line numbers consistent with Architecture Overview § 4.1 | direct read pattern check | Race=255, Entry=214, PastPerformance=77, Workout=58, Result=296, Prediction=428 confirmed | § 4.1 cross-references + V1-10 |
| wr_inference_service.py:616-626 calibration bypass | direct read | Comment block 616-625 + bypass operation at line 626 confirmed; "All styles (including gonzo_sauce) bypass calibration at inference tonight" prose at line 617 | § 4.1 predictions + V1-9 |
| schema.sql JSONB columns | direct read | predictions.feature_importance (JSONB), model_versions.feature_list (JSONB), model_versions.hyperparameters (JSONB) | § 5.2 + V1-5 |
| 005 JSONB columns | direct read | wr/pl/ls_predictions.feature_importance (JSONB DEFAULT '{}') | § 5.2 + V1-5 |
| model_versions.metadata absence | direct read of schema.sql + all migrations | Zero matches for `metadata` in CREATE/ALTER TABLE | § 10.2 + V1-6 |
| Phase 1 audit dir convention | dynasty-dugout:list_directory `_audit/` | _audit/ singular for Phase 1; matches META_PLAN § 3.8 | § 5 + V1 verification log path |

### 11.2 Substrate verifications NOT runnable from QB sandbox (CC verifies)

| Anchor | Why QB cannot verify | CC verification command | Used in spec |
|---|---|---|---|
| Migration 011 git log fix date | bash sandbox lacks /home/strakajagr access | `git log --format="%cs %h %s" -- backend/database/migrations/011_wr_predictions_unique_fix.sql \| tail -1` | V1-8 |
| Live model_versions row counts (88 = 45 + 43) | needs DB credentials or dashboard | Dashboard endpoint or direct SQL | Spec passes via Lesson 2 inheritance + CC re-verifies |
| Live predictions row count (~6,600) | needs dashboard or DB | Dashboard endpoint `/dashboard/metrics` `counts.predictions` | V1-12 |
| Operator memory file `equine-equalizer-bug-28-hrn-scraper.md` | not in /home/strakajagr/projects/equine-equalizer/ tree | Operator-stated; META_PLAN v9 § 1.2 verbatim quote inheritable | Bug #28 cross-reference at § 6 (canonical home is data_pipeline_bible) |

### 11.3 Pattern-completion check (W.N exclusivity)

Spec authoring introduces ZERO new letter-prefixes. W.N remains the only ratified letter-prefix per BIBLE_STRUCTURE_SPEC v6 § 5.5. Cross-reference syntax extensions: NONE introduced beyond the existing `<bible>:#<bug-id>` (per v4 G9 ratification). Numeric sub-section IDs operative for § 5 candidate roster per G-new-1.

### 11.4 Methodology-interpolation self-check

Spec authoring introduces ZERO CC-prescribed methodology constructs Tony has not explicitly ratified. The 9-check framework, 3-cluster organization, 10 banked QB drafting-spec errors, and Lessons 1–6 are all upstream-ratified per QB handoff § 3 + § 4 + § 5. The CONDITIONAL trigger application in § 6.7 / § 7.1 / § 5.6.1.2 (G7 closure) is upstream-ratified. The G-new-1 numeric-IDs-for-candidates rule and G-new-2 CREATE-TABLE-only enumeration scope are both Tony-locked per BIBLE_STRUCTURE_SPEC v6 § 5.7 + § 6.6 § 4.1.

### 11.5 FRAMEWORK_GAP / SPEC_GAP markers

ZERO surfaced in this spec. The handoff cross-reference inaccuracies surfaced in § 10 are downstream-synthesis errors (the handoff document itself), NOT framework-level gaps in the bible's spec premise OR slot structure. They route to the spec's content correction and to a future handoff-document update — NOT to FRAMEWORK_GAP routing.

### 11.6 Distinctness test for new banked checks

This spec does NOT bank any new checks. The 9-check framework remains Substrate (1–3) / Content (4–6) / Workflow (7–9). No Check 10 surfaced during spec authorship. Forward-looking: if v1 audit-CC catches a new QB drafting-spec error class, evaluate whether it fits an existing check's coverage (over-fragmentation risk) or warrants a Check 10 (under-fragmentation risk).

---

**End of Database & Schema Bible v1 Drafting Spec.**

Spec authored under Option 1 with 9 checks operative across 3 clusters. QB substrate-verification log at § 11. Handoff cross-reference corrections banked at § 10. CC paste-prompt at § 1.1.

**Tony's next action:** review this spec. If approved, paste § 1.1 paste-prompt body into a fresh CC session pointed at the EE codebase. CC drafts Database & Schema Bible v1 + companion verification log at the prescribed paths.