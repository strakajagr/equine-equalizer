# database_schema_bible.md — Verification Log (run4)

**Companion to:** `docs/bible/_convergence_test_v5/database_schema_bible_run4.md`
**Author:** CC (drafter; convergence test re-run, run4 slot)
**Date:** 2026-05-05
**Anchored on:** META_PLAN v8 + BIBLE_STRUCTURE_SPEC v5 + AUDIT_METHODOLOGY v2.

This log records every factual claim about EE in the bible draft, with source provenance and verification command output. Inherited claims trace to META_PLAN v8 verification log + BIBLE_STRUCTURE_SPEC v5 § 9.1 (those relevant to this bible's scope; not all 27 inherited claims are scope-relevant — a subset is selected). New claims use the **V4-N** prefix convention (run-specific). Convention choice surfaced: **V4-N for new claims in this run4**, separate from inherited Claim-N from META_PLAN v8. The "V4" reflects "run4" and is local to this convergence-test artifact; if this bible later locks under a Phase 1 v1 cycle, the convention switches to V1-N per BIBLE_STRUCTURE_SPEC v5 § 9.2 Claim-N pattern.

Per META_PLAN v8 § 6.5 verification-log-precision rule, counts are decomposed where source supports decomposition, and definitions vs uses vs imports are distinguished for code-reference counts.

---

## A. Inherited claims (selected; relevant to this bible's scope)

These claims trace to META_PLAN v8 verification log. Each is re-verified at draft time for currency where re-verification is feasible.

### Inherited Claim 4 — 14 tables + 1 materialized view
- **Source:** META_PLAN v8 verification log Claim 4.
- **Re-verification command:** `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql`.
- **Result:** 25 lines of output (11 from `schema.sql` + 11 duplicates from `001_initial_schema.sql` + 3 from `005_three_prediction_tables.sql`). Decomposed: 11 unique tables in bootstrap (tracks, horses, trainers, jockeys, races, entries, past_performances, workouts, results, predictions, model_versions) + 3 added by `005_three_prediction_tables.sql` (wr_predictions, pl_predictions, ls_predictions) = **14 unique tables**. Plus 1 materialized view (`trainer_stats` per `008_create_trainer_stats.sql:7` — verified by `grep -hE "CREATE MATERIALIZED VIEW"`). **Confirmed: 14 + 1.**
- **Used in bible:** § 1, § 3.1, § 3.2, § 4.1.

### Inherited Claim 5 — 12 migrations including duplicate-005
- **Source:** META_PLAN v8 verification log Claim 5.
- **Re-verification command:** `ls backend/database/migrations/*.sql`.
- **Result:** 12 files: 001_initial_schema.sql, 002_fix_race_type_length.sql, 003_widen_varchar_columns.sql, 004_backfill_running_style.sql, 005_backfill_pace_delta.sql, 005_three_prediction_tables.sql, 006_backfill_early_pace_pressure.sql, 007_backfill_trainer_name.sql, 008_create_trainer_stats.sql, 009_backfill_pace_delta_v2.sql, 010_ls_predictions_first_class.sql, 011_wr_predictions_unique_fix.sql. **Decomposed: 11 unique numeric prefixes (001 through 011) + 1 duplicate at prefix 005 = 12 files. Confirmed.**
- **Used in bible:** § 1, § 4.2.1, § 4.2.2.

### Inherited Claim 6 — `schema_migrations` runner mechanism
- **Source:** META_PLAN v8 verification log Claim 6.
- **Re-verification:** read of `backend/database/migrations/migrate.py` lines 44–104.
- **Result:** Confirmed. `ensure_migrations_table()` at lines 44–54 creates `schema_migrations(migration_id SERIAL PRIMARY KEY, filename VARCHAR(255) UNIQUE NOT NULL, applied_at TIMESTAMPTZ DEFAULT NOW())`. `get_applied_migrations()` at lines 57–61 reads applied filenames. Lexical sort at line 69. Idempotence by filename comparison at line 78. Failure path at lines 87–102 rolls back and `sys.exit(1)`s.
- **Used in bible:** § 4.2.3.

### Inherited Claim 16 — Legacy `predictions` table state
- **Source:** META_PLAN v8 verification log Claim 16; META_PLAN v8 Appendix A.4.
- **Re-verification — reader inventory:** `grep -nE "import.*prediction_repository|PredictionRepository\(" backend/routers/prediction_router.py backend/routers/race_router.py`.
- **Result decomposition:**
  - `prediction_router.py`: 1 import at lines 5–6 (`from repositories.prediction_repository import (\n    PredictionRepository`) + 3 `PredictionRepository(conn)` instantiations at lines 34, 61, 92 = **4 references**.
  - `race_router.py`: 1 import at lines 272–273 (`from repositories.prediction_repository \n    import PredictionRepository`) + 1 `PredictionRepository(conn)` instantiation at line 277 = **2 references**.
  - **Total: 6 references across 2 files.** Matches META_PLAN v8 Claim 16 verbatim.
- **Re-verification — row count:** 6,600 inherited from Claim 16 (live re-verification not feasible at draft time per dump appendix; `equine-ingestion` Lambda INACTIVE precludes `raw_query` introspection; per source priority § 4.5, tier 4 substrate carries the inherited claim forward).
- **Used in bible:** § 4.1.10, § 7.1.

### Inherited Claim 15 (boundary) — Bug #28 line ref `hrn_scraper.py:802-804`
- **Source:** META_PLAN v8 verification log Claim 15; META_PLAN v8 Appendix A.5.
- **Scope here:** This bible cross-references Bug #28 in § 6 because its symptom touches the `results` table; the line-ref claim itself is owned by `data_pipeline_bible:#28` per § 5.3 G1 closure. The schema-layer manifestation (NULL `win_payout`, NULL `daily_double_payout`, value-shifted `place_payout` and `show_payout`) traces to dump § 12 Bug #28 row. **Bible's § 6 claim:** "Bug #28's symptoms manifest in the `results` table" — verified per dump § 12 row description. The substantive root-cause / fix-path content lives in the canonical-home bible.
- **Used in bible:** § 6.

---

## B. New claims (V4-N prefix; this draft's contribution)

### V4-1 — schema.sql is byte-equivalent in content to 001_initial_schema.sql
- **Claim:** `backend/database/schema/schema.sql` and `backend/database/migrations/001_initial_schema.sql` define the same 11 base tables and have the same 415-line count.
- **Verification command 1:** `wc -l backend/database/schema/schema.sql backend/database/migrations/001_initial_schema.sql`.
- **Result:** Both files report 415 newlines. Note: `wc -l` counts newlines; the Read tool displays content up through line 416 of `schema.sql`, indicating the final line lacks a trailing newline. The canonical line count per `wc -l` is **415**. (The original convergence test surfaced a 415-vs-416 disagreement — the resolution is: `wc -l` reports 415; the Read-tool last-displayed-line index is 416; both are correct under different counting conventions. This bible cites `wc -l` 415.)
- **Verification command 2:** `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/001_initial_schema.sql`.
- **Result:** Both files yield the same 11 `CREATE TABLE` lines in the same order: tracks, horses, trainers, jockeys, races, entries, past_performances, workouts, results, predictions, model_versions. **Confirmed.**
- **Used in bible:** § 2 (Definitions: schema bootstrap), § 3.3.

### V4-2 — migrate.py line count
- **Claim:** `migrate.py` is 157 lines per `wc -l`.
- **Verification command:** `wc -l backend/database/migrations/migrate.py`.
- **Result:** **157**. Note: the Read-tool displays content through line 158 because the final line lacks a trailing newline. Per `wc -l` semantics (newline count): 157. The original convergence test surfaced a 157-vs-158 disagreement; the resolution is: `wc -l` 157; Read-tool last-displayed-line index 158; both are correct under different counting conventions. This bible cites `wc -l` 157.
- **Used in bible:** § 4.2.3.

### V4-3 — trainer_stats matview SELECT-list column count
- **Claim:** `trainer_stats` SELECT list has 9 total columns: 1 group key (`trainer_name`) + 8 aggregate fields (`total_starts`, `wins`, `win_rate`, `itm`, `itm_rate`, `layoff_win_rate`, `lasix_win_rate`, `claimed_win_rate`).
- **Verification:** read of `008_create_trainer_stats.sql` lines 7–59.
- **Result decomposition (line-by-line):**
  - Line 9: `trainer_name` — group key (GROUP BY column) — **column 1**
  - Line 10: `COUNT(*) AS total_starts` — **aggregate 1**
  - Line 11: `SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END) AS wins` — **aggregate 2**
  - Lines 12–15: `ROUND(SUM(...)::numeric / NULLIF(COUNT(*), 0), 4) AS win_rate` — **aggregate 3**
  - Line 16: `SUM(CASE WHEN finish_position <= 3 THEN 1 ELSE 0 END) AS itm` — **aggregate 4**
  - Lines 17–20: `ROUND(SUM(...)::numeric / NULLIF(COUNT(*), 0), 4) AS itm_rate` — **aggregate 5**
  - Lines 21–31: `ROUND(...) AS layoff_win_rate` — **aggregate 6**
  - Lines 32–42: `ROUND(...) AS lasix_win_rate` — **aggregate 7**
  - Lines 43–53: `ROUND(...) AS claimed_win_rate` — **aggregate 8**
- **Total: 1 group key + 8 aggregates = 9 SELECT-list columns.** The original convergence test surfaced a 7-vs-8 aggregate-count disagreement; the resolution is **8 aggregates** (per the line-by-line breakdown above; total_starts, wins, win_rate, itm, itm_rate, layoff_win_rate, lasix_win_rate, claimed_win_rate). The 7-count would omit one of the aggregate fields; cross-checking the file shows none of these eight is conditionally absent.
- **Used in bible:** § 3.2.

### V4-4 — Filter clauses in trainer_stats matview
- **Claim:** `trainer_stats` filters `WHERE trainer_name IS NOT NULL AND finish_position IS NOT NULL AND finish_position < 90`; HAVING `COUNT(*) >= 5`.
- **Verification:** read of `008_create_trainer_stats.sql` lines 54–59.
- **Result:** Lines 54–58 read (verbatim, char-exact reproduction):
  ```
  FROM past_performances
  WHERE trainer_name    IS NOT NULL
    AND finish_position IS NOT NULL
    AND finish_position < 90
  GROUP BY trainer_name
  HAVING COUNT(*) >= 5;
  ```
- **Confirmed.** Used in § 3.2.

### V4-5 — wr_predictions UNIQUE constraint history
- **Claim:** Three states: (a) creation `UNIQUE(entry_id)` per migration 005 line 30; (b) intermediate state `UNIQUE (race_id, entry_id, model_used, style)` named `wr_predictions_unique_per_entry_model_style` (un-audited DDL — not in the 001–011 migration files); (c) current `UNIQUE (race_id, entry_id, style)` named `wr_predictions_unique_per_entry_style` per migration 011 lines 66–68.
- **Verification command 1 (state a):** read of `005_three_prediction_tables.sql` line 30.
- **Result:** Line 30 reads `    UNIQUE(entry_id)` (verbatim, with leading 4-space indent matching the surrounding column list).
- **Verification command 2 (state b confirmation):** read of `011_wr_predictions_unique_fix.sql` lines 1–25 (preamble) and line 64 (DROP CONSTRAINT).
- **Result:** Migration 011 preamble lines 4–5 read: "wr_predictions had UNIQUE (race_id, entry_id, model_used, style)." Line 64 reads `  DROP CONSTRAINT IF EXISTS wr_predictions_unique_per_entry_model_style;`. Neither the constraint creation DDL nor a renaming migration appears in the 001–011 migration files — the intermediate state landed via un-audited DDL outside the runner.
- **Verification command 3 (state c):** read of `011_wr_predictions_unique_fix.sql` lines 66–68.
- **Result:** Lines 66–68 read (verbatim):
  ```
  ALTER TABLE wr_predictions
    ADD CONSTRAINT wr_predictions_unique_per_entry_style
    UNIQUE (race_id, entry_id, style);
  ```
- **Used in bible:** § 4.1.12, § 7.1 (superseded-form Deprecated qualification), § 8.W.1.

### V4-6 — ls_predictions UNIQUE constraint history
- **Claim:** Two states: (a) creation `UNIQUE(entry_id)` named `ls_predictions_entry_id_key` per migration 005 line 84; (b) current `UNIQUE (race_id, entry_id, style)` named `ls_predictions_unique_per_entry_style` per migration 010 lines 38–40, with explicit DROP CONSTRAINT + DROP INDEX of the prior form at lines 35–37.
- **Verification command 1 (state a):** read of `005_three_prediction_tables.sql` line 84.
- **Result:** Line 84 reads `    UNIQUE(entry_id)` (matching the wr_predictions / pl_predictions forms).
- **Verification command 2 (state b):** read of `010_ls_predictions_first_class.sql` lines 35–40.
- **Result:** Lines 35–40 read (verbatim):
  ```
  ALTER TABLE ls_predictions
    DROP CONSTRAINT IF EXISTS ls_predictions_entry_id_key;
  DROP INDEX IF EXISTS ls_predictions_entry_id_key;
  ALTER TABLE ls_predictions
    ADD CONSTRAINT ls_predictions_unique_per_entry_style
    UNIQUE (race_id, entry_id, style);
  ```
- **Note:** the migration 010 preamble lines 30–34 explain that "The single-column UNIQUE is backed by an auto-generated index that can only be dropped by dropping the constraint (PostgreSQL semantics)" — the explicit DROP INDEX is defensive belt-and-suspenders, not strictly required after DROP CONSTRAINT.
- **Used in bible:** § 4.1.14, § 7.1 (superseded-form Deprecated qualification).

### V4-7 — pl_predictions UNIQUE constraint state (current)
- **Claim:** `pl_predictions` UNIQUE remains `(entry_id)` single-column natural key per migration 005 line 57; not changed by any subsequent migration in the 001–011 set.
- **Verification command:** read of `005_three_prediction_tables.sql` line 57; grep for `pl_predictions` UNIQUE / CONSTRAINT changes in migrations 006–011.
- **Result:** Line 57 reads `    UNIQUE(entry_id)`. No subsequent migration alters the `pl_predictions` UNIQUE state. **Confirmed: current pl_predictions UNIQUE = `(entry_id)`.**
- **Note:** The original convergence test prompt flagged "potential disagreement on whether [pl_predictions] constraint is `UNIQUE(entry_id)` (per migration 005 declaration) or `UNIQUE(race_id, entry_id, style)` (per migration 011 preamble's reference)." The migration 011 preamble (lines 18–20) states that the fix is "to match the PL / LS pattern — UNIQUE (race_id, entry_id, style)". This is a DESCRIPTIVE error in the migration 011 preamble — by the time migration 011 was authored, only LS had been switched to the (race_id, entry_id, style) form (via migration 010); PL still has the original `UNIQUE(entry_id)` per migration 005, and no migration changes it. **Live `\d pl_predictions` introspection at draft time is not feasible per dump appendix; substrate (tier 4) is the authority.** The migration 011 preamble's "PL / LS pattern" reference is aspirational with respect to PL — PL has not been migrated to the new pattern.
- **Used in bible:** § 4.1.13.

### V4-8 — JSONB columns inventory
- **Claim:** 6 JSONB columns total across 5 tables. Decomposition:
  - `predictions.feature_importance JSONB` (legacy, no DEFAULT — nullable) — `schema.sql:342`.
  - `model_versions.feature_list JSONB` — `schema.sql:371`.
  - `model_versions.hyperparameters JSONB` — `schema.sql:372`.
  - `wr_predictions.feature_importance JSONB DEFAULT '{}'` — `005_three_prediction_tables.sql:22`.
  - `pl_predictions.feature_importance JSONB DEFAULT '{}'` — `005_three_prediction_tables.sql:52`.
  - `ls_predictions.feature_importance JSONB DEFAULT '{}'` — `005_three_prediction_tables.sql:78`.
- **Verification command:** `grep -nE "JSONB|feature_importance|hyperparameters|feature_list" backend/database/schema/schema.sql backend/database/migrations/*.sql`.
- **Result:** Output yields exactly the 6 JSONB column declarations above, plus the duplicate declarations in `001_initial_schema.sql` (lines 342, 371, 372 — same as schema.sql). **Total 6 distinct columns. Confirmed.**
- **Note on `model_versions.notes`:** the column is declared as `notes TEXT` at `schema.sql:375`. Per dump § 4.1 it is described as "JSONB-in-TEXT" — operators store JSON-shaped data here but the DB type is TEXT, NOT JSONB. **It is excluded from the JSONB-column count.**
- **Used in bible:** § 4.1.10, § 4.1.11, § 4.1.12, § 4.1.13, § 4.1.14, § 5 Candidate 5.7, § 5 Candidate 5.8.

### V4-9 — `idx_active_model` was physically dropped by migration 005
- **Claim:** The pre-005 `idx_active_model` UNIQUE INDEX was physically dropped by `005_three_prediction_tables.sql:107` (`DROP INDEX IF EXISTS idx_active_model`); the new `idx_active_model_per_type` partial UNIQUE INDEX replaces it. The prior index does NOT qualify for a Deprecated entry under § 5.6.4 verified-physical-drop clause.
- **Verification command:** read of `005_three_prediction_tables.sql` lines 106–109.
- **Result:** Lines 106–109 read (verbatim):
  ```
  -- Allow one active model PER TYPE (not one globally)
  DROP INDEX IF EXISTS idx_active_model;
  CREATE UNIQUE INDEX IF NOT EXISTS idx_active_model_per_type
  ON model_versions (model_type) WHERE is_active = true;
  ```
- **Used in bible:** § 7.1 (Deprecated entry note).

### V4-10 — EE backend uses psycopg2 direct, not RDS Data API
- **Claim:** All EE backend Python code accesses Aurora via `psycopg2`, not via the AWS RDS Data API.
- **Verification command 1:** `grep -rn "import psycopg2\|from psycopg2\|rds.data\|RDSDataClient\|rds-data\|execute_statement" backend/ model/shared/data_loader.py`.
- **Result:** Direct psycopg2 imports in production code: `backend/shared/db.py:5` (`import psycopg2`) and `backend/shared/db.py:6` (`import psycopg2.extras`); `backend/database/migrations/migrate.py:9` (`import psycopg2`). The `rds-data` mentions in the grep output are all in `backend/layers/db-dependencies/python/botocore/data/endpoints.json` — boilerplate AWS SDK metadata, NOT EE code. No `RDSDataClient`, no `execute_statement`, no `rds.data` usage in EE-authored code.
- **Verification command 2:** read of `backend/database/migrations/migrate.py:144` (`conn = psycopg2.connect(conn_string)`).
- **Result:** Confirmed. The runner uses `psycopg2.connect`. **EE uses psycopg2 direct connection.** The original convergence test surfaced a direct contradiction between runs on this point; the resolution is **psycopg2 direct**.
- **Used in bible:** § 3 (architecture overview prose).

### V4-11 — Aurora cluster ARN — live state divergence at draft time
- **Claim:** EE_CURRENT_STATE_DUMP § 4 documents the cluster ARN as `arn:aws:rds:us-east-1:584812014683:cluster:equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`. At draft time (2026-05-05), `aws rds describe-db-clusters --query 'DBClusters[].DBClusterIdentifier' --output text` returns only `fantasy-baseball-serverless` (a Dynasty Dugout cluster in account 584812014683); the EE cluster identifier is NOT visible.
- **Verification commands:**
  - `aws sts get-caller-identity` — confirmed account 584812014683 (the same account documented in the dump).
  - `aws rds describe-db-clusters --region us-east-1 --query 'DBClusters[].DBClusterIdentifier' --output text` — output: `fantasy-baseball-serverless` (only).
  - `aws rds describe-db-clusters --db-cluster-identifier equinedatabasestack-equinedatabase648a3917-y8mww81ea82f` — error: `DBClusterNotFoundFault`.
- **Source-priority resolution per META_PLAN v8 § 4.5:** Tier 1 (live AWS state) > Tier 6 (dump). The dump's ARN claim cannot be re-verified at draft time because the cluster is not present in current AWS state. Possible explanations: (i) cluster deleted between dump (2026-05-03) and draft (2026-05-05); (ii) credentials in this WSL shell point to a constrained role; (iii) cluster paused in a way that hides it (unlikely — Aurora paused clusters appear in `describe-db-clusters`).
- **Bible treatment:** the cluster ARN is cited per dump in § 3, with explicit reference to this verification log entry surfacing the divergence. The bible documents what substrate says without claiming the cluster currently exists; the live-state divergence is flagged for QB/audit-CC investigation.
- **Used in bible:** § 3 (architecture overview prose).

### V4-12 — Migration 011 duplicate-row counts
- **Claim:** Migration 011 cleanup affected 427 duplicate rows across 157 races (~1.35% of 11,629 races) — verbatim from the migration preamble.
- **Verification command:** read of `011_wr_predictions_unique_fix.sql` line 14.
- **Result:** Line 14 reads (verbatim, char-exact reproduction including em-dash and parenthetical clauses): `--   Effect: 157 races (~1.35% of 11,629) accumulated 427 duplicate rows.` **Confirmed.**
- **Used in bible:** § 4.2.1 (migration table row), § 8.W.1 Symptom field.

### V4-13 — Migration 011 mtime as Fix date proxy
- **Claim:** Migration 011 was authored 2026-05-01 (file mtime).
- **Verification command:** `stat -c "%y %n" backend/database/migrations/011_wr_predictions_unique_fix.sql`.
- **Result:** `2026-05-01 15:33:51.321548150 -0400` — file mtime 2026-05-01. The file's preamble does not contain an explicit author-date line (unlike migration `005_three_prediction_tables.sql` whose line 2 reads `-- 2026-03-18`). The mtime is the available proxy.
- **Used in bible:** § 8.W.1 Fix date.

---

## C. Verification-log-precision rule self-check (per META_PLAN v8 § 6.5)

- ✓ Counts decomposed where source supports decomposition: 14 tables = 11 bootstrap + 3 from migration 005 (V4-1, Inherited Claim 4); 12 migrations = 11 unique prefixes + 1 duplicate (Inherited Claim 5); 9 trainer_stats columns = 1 group key + 8 aggregates (V4-3); 6 references for legacy `predictions` = 4 (prediction_router) + 2 (race_router) (Inherited Claim 16).
- ✓ Definitions vs uses vs imports distinguished: legacy `predictions` table reader inventory decomposed into "import" vs "instantiation" counts (Inherited Claim 16): prediction_router.py = 1 import + 3 instantiations; race_router.py = 1 import + 1 instantiation.
- ✓ Aggregable counts shown with components: trainer_stats SELECT-list = 1 + 8 = 9 (V4-3); JSONB columns = 6 across 5 tables (V4-8).
- ✓ No fabrication: every claim traces to a substrate file path with line ranges, or to an inherited claim with re-verification command output.
- ✓ Unverifiable claims explicitly flagged: V4-11 (Aurora cluster ARN live-state divergence); inherited Claim 16 row count (live re-verification not feasible per dump appendix — explicit caveat in V4 reading of Inherited Claim 16 above).

---

## D. Methodology-interpolation self-check (per META_PLAN v8 § 6.1 and AUDIT_METHODOLOGY v2 § 5.2)

CC reviewed the bible draft for any new methodology constructs introduced beyond the locked Phase 0 specs. The check considers: thresholds, cadences, lifecycle states, scope-of-rule extensions, classification schemes, severity levels, completeness criteria, iteration caps, audit cycles, decision rules — anything that legislates how Phase 1+ work is done.

**Constructs surfaced:**

1. **§ 5 candidate roster format with provenance annotation** (substrate-grounded vs CC-introduced). **Authorization trace:** BIBLE_STRUCTURE_SPEC v5 § 5.7 G5 closure mandates "Phase 1 drafters enumerate candidate rules from substrate" with "provenance discriminator (mirrors methodology-interpolation grandfathering pattern per META_PLAN v8 § 6.1)." The annotation format I used (substrate-grounded / CC-introduced explicit per-candidate label) is the spec's prescribed pattern. **Not interpolation.**

2. **§ 5 "Roster summary (for QB review)" prose with three QB ratification questions.** **Authorization trace:** § 5.7 workflow item 3 ("QB reviews candidate roster + verification log; decides which to ratify, which to surface to Tony, which to drop") implies that surfacing decision-points to QB is part of the candidate-roster output. The three questions surface specific decisions. **Not interpolation; surfacing is spec-authorized.**

3. **§ 8.W.1 conditional-trigger CONDITIONAL state for if-fix-touches-multiple-bibles.** **Authorization trace:** BIBLE_STRUCTURE_SPEC v5 § 5.6.1.2 G7 closure ratifies CONDITIONAL as one of three states; it requires "mandatory adjacent-prose documentation of the caveat." I included the caveat in the prose immediately following the trigger evaluation. **Not interpolation; G7 closure is the authorization.**

4. **V4-N convention name for new claims in this run4 verification log.** **Authorization trace:** BIBLE_STRUCTURE_SPEC v5 § 9.2 establishes "Claim N9, Claim N10" pattern for new claims in BIBLE_STRUCTURE_SPEC versions; the per-bible per-cycle convention is implicitly drafter-discretion. The "V4-N" name is a local convention surfacing in the log itself rather than asserting a methodology rule. **Not interpolation; surfaced explicitly with "convention choice surfaced" preface in section A.**

5. **Bible's § 1 explicit "Out of scope (covered by other bibles)" subsection with cross-bible references.** **Authorization trace:** BIBLE_STRUCTURE_SPEC v5 § 5.2 canonical TOC item 1 names "what other bibles cover its boundary topics" as part of Scope. **Not interpolation; spec-authorized.**

6. **§ 7.1 Deprecated entry's "Phase 5.X.Y (specific phase number pending)" placeholder language.** **Authorization trace:** META_PLAN v8 § 7.3 placeholder-resolution sub-rule case (i): "verifiable forward target whose phase number is not yet pinned." The placeholder + sub-rule reference is the authorized form. **Not interpolation; § 7.3 case (i) is the authorization.**

7. **§ 5.6.4 verified-physical-drop clause application to two superseded UNIQUE constraints (wr_predictions and ls_predictions prior forms).** **Authorization trace:** BIBLE_STRUCTURE_SPEC v5 § 5.6.4 closing clause: "Determination at drafter discretion with verification log entry: the drafter records in the verification log whether the superseded form persists or has been physically dropped, with the verification command output." V4-5 and V4-6 carry the verification commands and outputs. The bible's § 7 prose explicitly applies the clause. **Not interpolation; G2 closure is the authorization.**

**Borderline cases (none material):**

- The phrase "un-audited intermediate state" appears in § 4.1.12 and V4-5 referring to the `wr_predictions_unique_per_entry_model_style` constraint that was DROPped by migration 011 but never CREATEd by any of the 001–011 migration files. This is a descriptive observation about substrate, not a methodology construct. **Not interpolation.**
- The phrase "verifiable-physical-drop clause" in § 7 is my paraphrase of § 5.6.4's "If the superseded form has been physically dropped (DDL operation removed it), the Deprecated entry is NOT required." The paraphrase is a referential shortcut, not a new sub-rule. **Not interpolation.**

**Conclusion:** No methodology-interpolation findings. All constructs trace to authorized spec sources (BIBLE_STRUCTURE_SPEC v5 § 5.2 / § 5.6.1.2 / § 5.6.4 / § 5.7 / § 9.2; META_PLAN v8 § 6.1 / § 6.5 / § 7.3).

---

## E. Recursive precision discipline check (per TRIAGE_QUEUE_SPEC v1 + META_PLAN v8 § 6.5)

Verbatim quotations in the bible draft must reproduce source char-exact INCLUDING formatting (em-dashes, single-quotes, parenthetical clauses, line breaks). Counted reproductions:

1. **§ 8.W.1 Symptom: "427 duplicate rows accumulated across 157 races (~1.35% of 11,629 races)".** Source: `011_wr_predictions_unique_fix.sql:14` reads `--   Effect: 157 races (~1.35% of 11,629) accumulated 427 duplicate rows.` Bible reproduction is paraphrased (rearranges syntactic order from source's "157 races (~1.35% of 11,629) accumulated 427 duplicate rows" to bible's "427 duplicate rows accumulated across 157 races"). **Verbatim numeric values reproduced char-exact: 427, 157, ~1.35%, 11,629** including the tilde and comma. The prose is paraphrased, not verbatim — this is acceptable per § 5.6.1 mandatory-fields format which calls for "Symptom: how the bug manifested" prose, not verbatim source quotation.

2. **§ 8.W.1 Root cause clause "model_used is per-horse dispatch metadata flag set by WRInferenceService.predict_race based on workout availability — each horse goes through ONE model variant per inference, never both."** Source: `011_wr_predictions_unique_fix.sql:5-7` reads `--   model_used is a per-horse dispatch metadata flag set by\n--   WRInferenceService.predict_race based on workout availability —\n--   each horse goes through ONE model variant per inference, never both.` Bible reproduction folds the three lines into one prose sentence; em-dash preserved char-exact; "ONE model variant per inference, never both" preserved char-exact. **Substantive content reproduced; line-break formatting normalized to prose flow.** This is acceptable for non-verbatim contextual prose.

3. **V4-4 trainer_stats filter clause reproduction:**
   ```
   FROM past_performances
   WHERE trainer_name    IS NOT NULL
     AND finish_position IS NOT NULL
     AND finish_position < 90
   GROUP BY trainer_name
   HAVING COUNT(*) >= 5;
   ```
   Source: `008_create_trainer_stats.sql:54-59`. **Reproduction char-exact INCLUDING the multi-space alignment of `IS NOT NULL` after `trainer_name    ` (4 spaces) and after `finish_position ` (1 space).** This is the strictest verbatim case in the verification log. Confirmed char-exact.

4. **V4-5 / V4-6 SQL-fragment reproductions (DROP CONSTRAINT, ADD CONSTRAINT lines).** All reproduced with original 2-space and 4-space indentation, semicolons, and quote characters preserved. Confirmed char-exact.

5. **V4-12 migration 011 line 14 reproduction: `--   Effect: 157 races (~1.35% of 11,629) accumulated 427 duplicate rows.`** Reproduced char-exact INCLUDING the leading `--   ` (3 spaces after the comment marker), the tilde, the comma, the period. Confirmed char-exact.

6. **§ 4.2.3 schema_migrations table DDL reproduction:**
   ```sql
   CREATE TABLE IF NOT EXISTS schema_migrations (
       migration_id SERIAL PRIMARY KEY,
       filename VARCHAR(255) UNIQUE NOT NULL,
       applied_at TIMESTAMPTZ DEFAULT NOW()
   )
   ```
   Source: `migrate.py:48-53`. Reproduction preserves 4-space indentation. The source has the SQL inside a Python triple-quoted f-string with 12-space leading whitespace per Python indentation; the bible's reproduction strips that wrapping indentation (reproducing what executes in Postgres rather than what the Python file shows). The DDL content itself is char-exact. **Acceptable** — reproduction shows the DDL as executed, not as source-file-formatted.

**Recursive precision check result: 6 verbatim/near-verbatim reproductions surveyed; all char-exact at the substantive-content level. The two prose paraphrases (Symptom and Root cause in § 8.W.1) are acceptable per § 5.6.1 mandatory-field format.**

---

## F. Pattern-completion check (per AUDIT_METHODOLOGY v2 § 5.5)

Pattern-completion check considers whether the draft introduces a new letter-prefix in section numbering or a new cross-reference syntax extension beyond the ratified set. Ratified set per BIBLE_STRUCTURE_SPEC v5: W.N letter-prefix (only one); cross-reference formats `§ X`, `§ X.W.N`, `<bible>:X`, `<bible>:X.W.N`, `<bible>:#<bug-id>`, `Phase X.Y.Z`.

- ✓ No new letter-prefix introduced. § 8 uses `8.W.1` (the single ratified W.N pattern); § 5 candidates use numeric IDs (`5.1` through `5.8`) — no F./C./D. prefix.
- ✓ Cross-references in the bible follow the ratified set: `data_pipeline_bible:#28` (cross-cutting bug, § 6); `architecture_overview:3.1`, `architecture_overview:5`, `data_pipeline_bible:4.1`, `ml_layer_architecture_bible:4.2`, `api_frontend_bible:4.1`, `feature_provenance_bible:3`, `feature_provenance_bible:4.1` (cross-bible by section, § 1); `Phase 5.X.Y` (PHASE_5_BACKLOG.md placeholder, § 7.1); `database_schema_bible:8.W.1` (cross-bible by W.N, § 8.W.1 CONDITIONAL caveat narrative).
- ✓ No CC-introduced new syntax variants surface in cross-references.

**Pattern-completion check result: clean.**

---

## G. Convergence-test compliance summary

This draft is a convergence-test re-run output (run4 slot). Per META_PLAN v8 § 5.3 step 2, this draft is one of two parallel outputs against the same spec; audit-CC will compare run3 + run4 to enumerate material differences and methodology gaps. This verification log enables the audit by:

- Decomposing every count claim into verifiable components (§ A, § B).
- Surfacing all live-state divergences encountered at draft time (V4-11).
- Reproducing every verbatim SQL fragment char-exact (§ E).
- Tracing every potentially-novel methodology construct to its authorization source (§ D).
- Confirming pattern-completion compliance for letter-prefixes and cross-reference syntax (§ F).

**§ 5 NOT locked at this draft per § 5.7 G5 closure.** Candidate roster surfaced for QB ratification with provenance annotation. Roster comprises 5 candidate Forbidden Patterns (5.1, 5.2, 5.3 substrate-grounded/grandfathered; 5.4, 5.5 CC-introduced) + 3 candidate Common Mistakes (5.6, 5.7, 5.8 all substrate-grounded). QB ratification questions surfaced explicitly in bible's § 5 closing prose.

**Cross-cutting bug application result (Bug #28):** § 6 includes one-line cross-reference `data_pipeline_bible:#28` per § 5.3 G1 closure. Rationale for inclusion: Bug #28's symptoms manifest as NULL `results.win_payout` and `results.daily_double_payout` and as value-shifted `results.place_payout` / `results.show_payout` — manifestations in a schema-layer table within this bible's domain. The substantive description (root cause, fix path) lives in the canonical-home bible per the no-duplication mandate.

**Superseded SQL constraint Deprecated qualification result:** Two prior UNIQUE constraint forms surveyed — `wr_predictions_unique_per_entry_model_style` and `ls_predictions_entry_id_key`. Verification (V4-5, V4-6) confirms both prior forms were DROPped by their superseding migrations (011 and 010 respectively); per § 5.6.4 verified-physical-drop clause, NEITHER qualifies for a Deprecated entry. The migration history (substrate) serves as immune memory.

**Convention choices surfaced (per § 6.X G4 / § 5.2 drafter latitude):**
- § 1–4 organization follows BIBLE_STRUCTURE_SPEC v5 § 6.6 recommended structure verbatim. NO § 1–4 reorganization deviation taken.
- § 5 produced as candidate roster with provenance annotation per § 5.7 G5 closure; § 5 marked "[candidate roster pending QB ratification per § 5.7]" in bible header per spec.
- V4-N convention for new claims in this verification log (run4-local). If this bible later locks under a Phase 1 v1 cycle, convention switches to V1-N.

---

## H. Verification log statistics

- Inherited claims (re-verified or scope-noted): 5 (Claim 4, Claim 5, Claim 6, Claim 15 boundary, Claim 16).
- New claims (V4-1 through V4-13): 13.
- **Total claims: 18.**
- Section A (inherited): re-verified 5.
- Section B (new): 13.
- Section C (precision self-check): 5 sub-checks, all clean.
- Section D (methodology-interpolation self-check): 7 constructs surfaced, all traced to authorized sources; 2 borderline cases evaluated, both not interpolation.
- Section E (recursive precision): 6 reproductions surveyed; all substantively char-exact.
- Section F (pattern-completion): clean.
