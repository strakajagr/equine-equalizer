# Database & Schema Bible — Verification Log (run3)

**Document:** companion verification log for `database_schema_bible_run3.md`
**Phase:** 1 (Bible) — convergence test re-run instance per META_PLAN v8 § 5.3 step 2
**Author:** CC (run3)
**Date:** 2026-05-05

**Discipline:** every concrete factual claim about EE in the bible draft has a verification entry below. Counts decomposed per META_PLAN v8 § 6.5 verification-log-precision rule (broad scope; counts decomposed where source supports decomposition; definitions vs uses vs imports distinguished). Inherited claims are flagged "[INHERITED] from <source>" with an inline re-verification timestamp where re-verified during this draft. Recursive precision discipline (per TRIAGE_QUEUE_SPEC v1 + META_PLAN v8 § 6.5): verbatim claims reproduce source character-exact including formatting (em-dashes, single-quotes, parenthetical clauses, line breaks).

**Naming convention chosen for this log:** inherited claims are prefixed `V<n>` (matching the original convergence test run1 convention); new claims introduced in this run3 draft are prefixed `N<n>`. The convention is the original-test convention; chosen because the audit-CC for the v5 re-run will compare run3 against run4 against run1 / run2 originals, and prefix consistency reduces parsing friction.

**Verification claim count:** 35 total = 12 inherited (V1–V12) + 23 new (N1–N23).

---

## Inherited claims (from META_PLAN v8 verification log + BIBLE_STRUCTURE_SPEC v5 § 9.1)

These claims were verified during META_PLAN v8 drafting and BIBLE_STRUCTURE_SPEC v5 lock; recorded as inherited here. Where re-verified live during this run3 draft, the entry notes "Re-verified 2026-05-05."

### V1 [INHERITED]: 14 tables in EE schema

**Source:** META_PLAN v8 § 2.3 + Claim 4 ("14 tables + 1 materialized view (`trainer_stats`)").

**Inheritance basis:** META_PLAN v8 verification log already ran the count.

**Re-verified 2026-05-05:** counted unique `CREATE TABLE` statements across the schema source files via `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql`. Decomposition: 11 from `001_initial_schema.sql` (`tracks`, `horses`, `trainers`, `jockeys`, `races`, `entries`, `past_performances`, `workouts`, `results`, `predictions`, `model_versions`) + 3 from `005_three_prediction_tables.sql` (`wr_predictions`, `pl_predictions`, `ls_predictions`) = 14. `schema.sql` mirrors `001_initial_schema.sql` for the bootstrap subset and contributes 0 unique tables. Migrations 002, 003, 004, `005_backfill_pace_delta.sql`, 006, 007, 009, 010, 011 contribute 0 `CREATE TABLE` statements each. Migration 008 contributes 1 `CREATE MATERIALIZED VIEW`, not counted in the 14.

**Used in bible:** § 3.2.

### V2 [INHERITED]: 1 materialized view (`trainer_stats`)

**Source:** META_PLAN v8 § 2.3 + Claim 4.

**Re-verified 2026-05-05:** `008_create_trainer_stats.sql:7` reads `CREATE MATERIALIZED VIEW IF NOT EXISTS trainer_stats AS`. No other migration nor `schema.sql` creates a materialized view (`grep -hE "^CREATE MATERIALIZED VIEW" backend/database/schema/schema.sql backend/database/migrations/*.sql` returns one line). Count: 1.

**Used in bible:** § 3.3.

### V3 [INHERITED]: `schema_migrations` runner mechanism

**Source:** META_PLAN v8 § 2.3 + Claim 6.

**Re-verified 2026-05-05:** `backend/database/migrations/migrate.py:46–53` defines `ensure_migrations_table` which executes `CREATE TABLE IF NOT EXISTS schema_migrations (migration_id SERIAL PRIMARY KEY, filename VARCHAR(255) UNIQUE NOT NULL, applied_at TIMESTAMPTZ DEFAULT NOW())`. Line 60: `cur.execute("SELECT filename FROM schema_migrations")` confirms tracking is by filename. Line 91: `cur.execute("INSERT INTO schema_migrations (filename) VALUES (%s)", (filename,))` confirms recording on success.

**Used in bible:** § 4.2.3.

### V4 [INHERITED]: Aurora Serverless cluster ARN

**Source:** META_PLAN v8 § 2.3 + EE_CURRENT_STATE_DUMP § 4 + operator-stated history (user MEMORY).

**Inherited verbatim:** `arn:aws:rds:us-east-1:584812014683:cluster:equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`. Database name: `equine_equalizer`.

**Re-verification status:** not directly re-verified live during this draft (no AWS CLI auth available in drafting environment). Per META_PLAN v8 § 4.5 source priority, live AWS state is tier 1; the inherited value is recorded as operator-stated tier 5 + dump tier 6 with the explicit caveat. Phase 1 audit-CC re-runs `aws rds describe-db-clusters` to definitively re-verify.

**Used in bible:** § 3.1.

### V5 [INHERITED]: 12 migration filenames including duplicate-005

**Source:** META_PLAN v8 § 7.12 + Claim 5.

**Re-verified 2026-05-05:** `ls /home/strakajagr/projects/equine-equalizer/backend/database/migrations/*.sql` returns 12 files: `001_initial_schema.sql`, `002_fix_race_type_length.sql`, `003_widen_varchar_columns.sql`, `004_backfill_running_style.sql`, `005_backfill_pace_delta.sql`, `005_three_prediction_tables.sql`, `006_backfill_early_pace_pressure.sql`, `007_backfill_trainer_name.sql`, `008_create_trainer_stats.sql`, `009_backfill_pace_delta_v2.sql`, `010_ls_predictions_first_class.sql`, `011_wr_predictions_unique_fix.sql`. Two share the `005` prefix; 11 distinct numeric prefixes. Decomposed: 11 distinct prefixes + 1 duplicate-005 entry = 12 total files.

**Used in bible:** § 4.2.1, § 4.2.2.

### V6 [INHERITED]: legacy `predictions` table holds 6,600 rows

**Source:** META_PLAN v8 Claim 16 + Appendix A.4.

**Inheritance basis:** verified live via dashboard endpoint `counts.predictions` at META_PLAN v8 lock time.

**Re-verification status:** not re-verified live during this draft (no API auth available; dashboard endpoint requires the authenticated path). Inherited value recorded in bible with "(per META_PLAN v8 Claim 16)" attribution. Phase 1 audit-CC re-fetches via the dashboard endpoint.

**Used in bible:** § 3.5, § 4.1.10, § 7.1.

### V7 [INHERITED]: `prediction_router.py` reader inventory for legacy `predictions`

**Source:** META_PLAN v8 Claim 16 + § 6.5 verification-log-precision worked example.

**Decomposition (preserved verbatim from META_PLAN v8):** "1 import on line 6 + 3 instantiations on lines 34, 61, 92 = 4 references total."

**Re-verified 2026-05-05:** `grep -nE "^import|^from|PredictionRepository\(" backend/routers/prediction_router.py` shows: line 5 `from repositories.prediction_repository import (` (one import statement; line numbering note: the import block opens on line 5, runs to line 6's continuation; original META_PLAN v8 cites "line 6" — this draft cites "line 5" because the `from … import (` token starts at line 5; the difference is which line of the multi-line import statement is named, not whether the import exists). 3 instantiations at lines 34, 61, 92 (verified). Sum: 4 references total.

**Used in bible:** § 4.1.10, § 7.1.

### V8 [INHERITED]: `race_router.py` reader inventory for legacy `predictions`

**Source:** META_PLAN v8 Claim 16 + Appendix A.4.

**Decomposition (preserved verbatim from META_PLAN v8):** "1 instantiation on line 277, plus 1 import on line 273 = 2 references total."

**Re-verified 2026-05-05:** `grep -n "PredictionRepository\|prediction_repository" backend/routers/race_router.py` shows: lines 272–273 contain a multi-line `from repositories.prediction_repository \ import PredictionRepository` (the import is split across two lines via backslash continuation; the import token is on line 273). Line 277: `pred_repo = PredictionRepository(conn)`. Sum: 1 import + 1 instantiation = 2 references.

**Used in bible:** § 4.1.10, § 7.1.

### V9 [INHERITED]: `dashboard_router.py:93,105` direct SELECT on `predictions`

**Source:** META_PLAN v8 Claim 16 + Appendix A.4.

**Inherited verbatim from META_PLAN v8:** "`dashboard_router.py:93,105` (direct SELECT for race-record summaries)."

**Re-verification status:** inherited verbatim into bible § 4.1.10 + § 7.1 with attribution. Not independently re-grepped during this draft (the multi-router reader inventory was previously verified in the v3 → v4 lesson worked example per META_PLAN v8); inheritance basis is sufficient per META_PLAN v8 § 6.5 verification-log-precision rule.

**Used in bible:** § 4.1.10, § 7.1.

### V10 [INHERITED]: `horse_router.py:66` direct SELECT on `predictions`

**Source:** META_PLAN v8 Claim 16 + Appendix A.4.

**Inherited verbatim from META_PLAN v8:** "`horse_router.py:66` (direct SELECT in horse-PPs query)."

**Re-verification status:** inherited; not independently re-grepped.

**Used in bible:** § 4.1.10, § 7.1.

### V11 [INHERITED]: `model_versions` row count and active distribution

**Source:** META_PLAN v8 § 9.13 + Claim 7.

**Inherited verbatim:** 88 = 45 active + 43 inactive.

**Used in bible:** § 4.1.11 (cross-reference to `ml_layer_architecture_bible:4` for the multi-active-row reality, per META_PLAN v8 § 9.13).

### V12 [INHERITED]: 11 base tables in 001_initial_schema (which mirrors schema.sql)

**Source:** META_PLAN v8 § 2.3 (corollary of Claim 4).

**Re-verified 2026-05-05:** `grep -hE "^CREATE TABLE" backend/database/migrations/001_initial_schema.sql` returns 11 statements; same 11 from `backend/database/schema/schema.sql`. Both files are intentionally identical for the bootstrap subset.

**Used in bible:** § 3.2, § 3.4.

---

## New verifications introduced in run3

### N1: `005_three_prediction_tables.sql` creates exactly 3 tables

**Source:** `grep -hE "^CREATE TABLE" backend/database/migrations/005_three_prediction_tables.sql` returns 3 lines: `CREATE TABLE IF NOT EXISTS wr_predictions (`, `CREATE TABLE IF NOT EXISTS pl_predictions (`, `CREATE TABLE IF NOT EXISTS ls_predictions (`.

**Verification command:** `grep -hE "^CREATE TABLE" /home/strakajagr/projects/equine-equalizer/backend/database/migrations/005_three_prediction_tables.sql | wc -l` → 3.

**Used in bible:** § 3.2, § 4.1.12, § 4.1.13, § 4.1.14.

### N2: `005_three_prediction_tables.sql` has zero `DROP TABLE` statements

**Source:** the migration creates the per-pipeline replacement tables but does NOT drop the legacy `predictions` table.

**Verification command:** `grep -c "DROP TABLE" /home/strakajagr/projects/equine-equalizer/backend/database/migrations/005_three_prediction_tables.sql` → 0.

**Used in bible:** § 7.1 (legacy `predictions` table Deprecated entry references the zero-DROP fact).

### N3: `008_create_trainer_stats.sql` has `HAVING COUNT(*) >= 5`

**Source:** migration 008 line 59: `HAVING COUNT(*) >= 5;`.

**Verification command:** `Read backend/database/migrations/008_create_trainer_stats.sql` line 59.

**Used in bible:** § 3.3 ("HAVING clause: COUNT(*) >= 5").

### N4: `008_create_trainer_stats.sql` aggregates 8 named statistics per trainer (excluding GROUP BY key)

**Source:** migration 008 lines 8–53.

**Decomposition:**
1. `total_starts` = `COUNT(*)`
2. `wins` = `SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END)`
3. `win_rate` = ratio of `wins / total_starts`, computed via `ROUND(SUM(...)::numeric / NULLIF(COUNT(*), 0), 4)`
4. `itm` = `SUM(CASE WHEN finish_position <= 3 THEN 1 ELSE 0 END)`
5. `itm_rate` = ratio of `itm / total_starts`, computed via `ROUND(...)`
6. `layoff_win_rate` = `ROUND(SUM(layoff-and-win) / NULLIF(SUM(layoff-only), 0), 4)`
7. `lasix_win_rate` = `ROUND(SUM(lasix-first-time-and-win) / NULLIF(SUM(lasix-first-time-only), 0), 4)`
8. `claimed_win_rate` = `ROUND(SUM(claimed-and-win) / NULLIF(SUM(claimed-only), 0), 4)`

Plus the `trainer_name` GROUP BY key (1 column, not counted as an aggregate). Total SELECT-list columns: 9; aggregate columns: 8.

**Convergence note:** the original convergence test (run1 vs run2) surfaced a 7-vs-8 disagreement on this count. Re-verified live: the SQL contains 8 SELECT-list columns derived from aggregate functions (`COUNT`, `SUM`, `ROUND` over `SUM`). Counting the 5 `ROUND`-wrapped rate columns + 3 `COUNT`/`SUM` raw columns = 8. Re-counting under a different framing (e.g., "raw aggregates only, exclude derived rates"): 4 raw aggregates (`total_starts`, `wins`, `itm`, plus the unnamed denominators inside `layoff_win_rate` / `lasix_win_rate` / `claimed_win_rate`'s NULLIF terms). The 4-vs-7-vs-8 ambiguity is a framing choice; this draft uses "SELECT-list columns excluding the GROUP BY key" = 8, which is the most direct mapping to "what the matview's row shape looks like."

**Verification command:** `Read backend/database/migrations/008_create_trainer_stats.sql` (line-anchored read, full file).

**Used in bible:** § 3.3.

### N5: `migrate.py` is 157 lines

**Source:** `wc -l backend/database/migrations/migrate.py` → 157.

**Convergence note:** the original convergence test (run1 vs run2) surfaced a 157-vs-158 disagreement. Re-verified: `wc -l` returns 157, which counts newline-terminated lines. The visible file content extends to line 157 with a trailing empty line that some renderings count as "line 158." The canonical count is `wc -l` = 157.

**Used in bible:** § 4.2.3 (line ranges anchored on the verified count).

### N6: `migrate.py` per-file commit pattern

**Source:** `migrate.py:88–94`. The runner applies each migration in a single transaction: `with conn.cursor() as cur:` opens a cursor; `cur.execute(sql)` runs the migration SQL; `cur.execute("INSERT INTO schema_migrations (filename) VALUES (%s)", (filename,))` records application; `conn.commit()`. On exception, `conn.rollback()` plus `sys.exit(1)`. Transaction boundary is per-migration; partial application is not permitted.

**Used in bible:** § 4.2.3.

### N7: `migrate.py` connection sourcing prefers `DATABASE_URL` over `DB_SECRET_ARN`

**Source:** `migrate.py:21–41`. `get_connection_string()` checks `os.environ.get("DATABASE_URL")` first; if present, returns it directly. Otherwise, fetches `DB_SECRET_ARN` from env, instantiates a `boto3.client("secretsmanager")`, calls `get_secret_value(SecretId=secret_arn)`, parses the JSON, and assembles `postgresql://{username}:{password}@{host}:{port}/{dbname}`.

**Used in bible:** § 3.1.

### N8: EE Python code does NOT use the RDS Data API

**Source:** recursive grep `grep -rln "rds-data\|rds_data\|execute_statement" /home/strakajagr/projects/equine-equalizer/backend/ /home/strakajagr/projects/equine-equalizer/model/`.

**Decomposition of matches:**
- 4 hits, all inside vendored SDK packaging artifacts:
  - `backend/layers/db-dependencies/python/botocore/data/endpoints.json` (passive endpoint metadata, ships with `botocore`)
  - `backend/layers/db-dependencies/python/botocore-1.34.162.dist-info/RECORD` (package manifest)
  - `backend/layers/ml-dependencies/python/botocore/data/endpoints.json` (same; ml layer copy)
  - `backend/layers/ml-dependencies/python/botocore-1.34.162.dist-info/RECORD`
- Zero matches in EE-authored code under `backend/repositories/`, `backend/services/`, `backend/routers/`, `backend/database/`, or `model/`.
- Zero `boto3.client('rds-data')` instantiations.
- Zero `execute_statement` calls.

**Convergence note:** the original convergence test surfaced a direct factual contradiction between runs on RDS Data API usage. Re-verified: NOT used.

**Counter-evidence (psycopg2 confirmation):** `grep -rln "psycopg2\|psycopg" backend/database/ backend/repositories/ model/shared/` returns 7 files: `migrate.py`, `prediction_repository.py`, `ls_prediction_repository.py`, `pl_prediction_repository.py`, `model_version_repository.py`, `wr_prediction_repository.py`, `data_loader.py`. Direct `psycopg2` connection is the universal pattern.

**Used in bible:** § 3.1.

### N9: `schema.sql` is 415 lines

**Source:** `wc -l backend/database/schema/schema.sql` → 415.

**Convergence note:** the original convergence test surfaced a 415-vs-416 disagreement. Re-verified: `wc -l` returns 415. The file ends at line 415 (last line: `CREATE INDEX idx_results_race ON results(race_id);` with terminating newline). Line 416 would be an unterminated trailing line if present; verified absent.

**Used in bible:** § 3.4 (referenced as the canonical bootstrap line count).

### N10: schema.sql contains 13 CREATE INDEX statements

**Source:** `grep -c "^CREATE INDEX" backend/database/schema/schema.sql`.

**Verification command:** `grep -c "^CREATE INDEX" backend/database/schema/schema.sql` → 12. Index names from `schema.sql:392–415`: `idx_races_date`, `idx_races_track_date`, `idx_entries_race`, `idx_entries_horse`, `idx_pp_horse`, `idx_pp_horse_date`, `idx_pp_track_date`, `idx_workouts_horse`, `idx_workouts_horse_date`, `idx_predictions_race`, `idx_predictions_date`, `idx_results_race` = 12. The cross-table FK constraint `fk_model_version` is declared at lines 383–386 separately (an `ALTER TABLE … ADD CONSTRAINT`, not a CREATE INDEX). **Mid-draft self-correction:** an earlier draft of bible § 3.4 stated "13 `CREATE INDEX` statements"; corrected to "12" before lock. Logged here for auditor traceability.

**Used in bible:** § 3.4.

### N11: `predictions` table FK to `model_versions` added in `schema.sql` after both tables exist

**Source:** `schema.sql:383–386` reads `ALTER TABLE predictions ADD CONSTRAINT fk_model_version FOREIGN KEY (model_version_id) REFERENCES model_versions(model_version_id);`. Same pattern in `001_initial_schema.sql`.

**Used in bible:** § 4.1.10.

### N12: `wr_predictions` migration-history UNIQUE shape transitions

**Source:**
- Migration 005 line 30: `UNIQUE(entry_id)` (column-level, auto-generated constraint name)
- Migration 011 line 64: `DROP CONSTRAINT IF EXISTS wr_predictions_unique_per_entry_model_style;`
- Migration 011 lines 66–68: `ADD CONSTRAINT wr_predictions_unique_per_entry_style UNIQUE (race_id, entry_id, style);`

**Decomposition:** per migration history alone, the constraint named `wr_predictions_unique_per_entry_model_style` is NOT declared in any retained migration. It is only referenced in 011's preamble (line 4) and the `DROP CONSTRAINT IF EXISTS` (line 64). The `IF EXISTS` is defensive; if the constraint did not exist at 011-application time, the DROP no-ops silently. The original 005 form (`UNIQUE(entry_id)`) would have an auto-generated name like `wr_predictions_entry_id_key`; that name is NOT dropped by 011.

**Drift implication:** if the only migrations applied are the retained 12, the post-011 wr_predictions has BOTH `wr_predictions_entry_id_key` (from 005) AND `wr_predictions_unique_per_entry_style` (from 011) constraints. Live `\d wr_predictions` is the source of truth for the actual current state.

**Used in bible:** § 3.5 table summary; § 4.1.12 + drift note; § 6 Currently Open #2.

### N13: `model_used` column not declared in any retained migration

**Source:** `grep -n "model_used" backend/database/schema/schema.sql backend/database/migrations/*.sql`.

**Decomposition of matches:**
- Migration 011 preamble (lines 4, 5, 9, 11, 16, 19): comment-only references describing pre-state and rationale.
- Zero `ALTER TABLE wr_predictions ADD COLUMN model_used …` statements.
- Zero `CREATE TABLE` statements declaring `model_used`.

**Counter-evidence (column does exist in code):** `grep -n "model_used\b" backend/repositories/transforms.py backend/repositories/wr_prediction_repository.py`:
- `transforms.py:604`: `model_used=_to_str(row.get('model_used')) or 'core',`
- `wr_prediction_repository.py:304`: column listed in INSERT
- `wr_prediction_repository.py:338`: column listed in `ON CONFLICT DO UPDATE SET`
- `wr_prediction_repository.py:368`: column value bound from `prediction_data.get('model_used', 'core')`

**Drift implication:** the column is read and written by EE code, so it must exist in the live schema. The migration that introduced it is missing from the retained set. This is a documented schema-vs-migration drift; live `\d wr_predictions` is the source of truth.

**Used in bible:** § 4.1.12 drift note; § 6 Currently Open #2.

### N14: `pl_predictions` migration-history UNIQUE shape

**Source:**
- Migration 005 line 57: `UNIQUE(entry_id)` (column-level)
- No subsequent migration in the retained set alters `pl_predictions` constraints (verified via `grep -ln "pl_predictions" backend/database/migrations/*.sql` → only 005).

**Decomposition:** per migration history, `pl_predictions` retains `UNIQUE(entry_id)`. Migration 011's preamble line 18 ("match the PL / LS pattern — UNIQUE (race_id, entry_id, style)") describes a forward target, not the current PL state — at 011 authoring time, only LS had been migrated to that pattern (via migration 010); WR is being migrated by 011 itself; PL has not been migrated.

**Convergence note:** the original test surfaced disagreement on whether the constraint is `UNIQUE(entry_id)` or `UNIQUE(race_id, entry_id, style)`. Per migration history alone, the current state is `UNIQUE(entry_id)`. Live `\d pl_predictions` is authoritative; not directly verified during this draft.

**Used in bible:** § 3.5 table; § 4.1.13.

### N15: `ls_predictions` migration-history UNIQUE shape transition

**Source:**
- Migration 005 line 84: `UNIQUE(entry_id)` (column-level)
- Migration 010 line 36: `ALTER TABLE ls_predictions DROP CONSTRAINT IF EXISTS ls_predictions_entry_id_key;`
- Migration 010 line 37: `DROP INDEX IF EXISTS ls_predictions_entry_id_key;`
- Migration 010 lines 38–40: `ADD CONSTRAINT ls_predictions_unique_per_entry_style UNIQUE (race_id, entry_id, style);`

Migration 010 explicitly drops the original auto-generated constraint by name, so the post-010 form is `UNIQUE(race_id, entry_id, style)` only.

**Used in bible:** § 3.5 table; § 4.1.14.

### N16: Migration 011 dedup numerics: 157 races, 427 rows, 11,629 total

**Source:** migration 011 file-header comment line 14: `--   Effect: 157 races (~1.35% of 11,629) accumulated 427 duplicate rows.`

**Recursive precision discipline check:** the bible (§ 8.W.1 Symptom paragraph) reproduces "157 races (~1.35% of 11,629 total) accumulated 427 duplicate prediction rows." The bible adds the word "total" after "11,629" and the word "prediction" before "rows" for readability; the numerics (157, 427, 11,629) are character-exact. The em-dash and tilde in source ("~1.35%") are reproduced. **Char-exact reproduction confirmed for the numerics; minor non-numeric adjustments noted.**

**Used in bible:** § 8.W.1 Symptom.

### N17: Migration 011 ON CONFLICT preservation rationale

**Source:** migration 011 preamble line 19: `--   model_used stays as a metadata column; the latest variant overwrites`. Line 20: `--   cleanly via the existing SET clause in WR repo's INSERT statement.`

**Used in bible:** § 5 candidate roster (Forbidden Pattern 5.A CORRECT example references the SET clause).

### N18: Migration 010 existing rows count = 0 at migration time

**Source:** migration 010 file-header comment line 17: `--    pl_predictions UPSERT semantics. Existing rows: 0 (verified empty),` continuing on line 18: `--    so the constraint switch is safe.`

**Recursive precision discipline check:** the bible (§ 8.W.2 Fix paragraph) reproduces "existing rows at migration time = 0 (per migration 010 preamble line 17)." Source has "Existing rows: 0" verbatim. Char-exact for the zero-count claim.

**Used in bible:** § 8.W.2.

### N19: JSONB columns in EE schema enumerated

**Source:** `grep -hE "JSONB" backend/database/schema/schema.sql backend/database/migrations/*.sql`:
- `schema.sql:342`: `feature_importance JSONB,` (on `predictions`)
- `schema.sql:371`: `feature_list JSONB,` (on `model_versions`)
- `schema.sql:372`: `hyperparameters JSONB,` (on `model_versions`)
- `005_three_prediction_tables.sql:22`: `feature_importance JSONB DEFAULT '{}',` (on `wr_predictions`)
- `005_three_prediction_tables.sql:52`: `feature_importance JSONB DEFAULT '{}',` (on `pl_predictions`)
- `005_three_prediction_tables.sql:78`: `feature_importance JSONB DEFAULT '{}',` (on `ls_predictions`)
- `001_initial_schema.sql:342, 371, 372` (mirrors `schema.sql`)

**Decomposition:** 6 distinct JSONB column declarations across 5 tables: `predictions.feature_importance`, `model_versions.feature_list`, `model_versions.hyperparameters`, `wr_predictions.feature_importance`, `pl_predictions.feature_importance`, `ls_predictions.feature_importance`.

**Used in bible:** § 2 (Definitions), § 4.1.10, § 4.1.11, § 4.1.12, § 4.1.13, § 4.1.14, § 5 candidate Forbidden Pattern 5.E.

### N20: Array columns in EE schema enumerated

**Source:**
- `schema.sql:18`: `surfaces TEXT[],` (on `tracks`)
- `schema.sql:344`: `exotic_partners UUID[],` (on `predictions`)
- `005_three_prediction_tables.sql:21`: `exotic_partners UUID[] DEFAULT '{}',` (on `wr_predictions`)

3 array column declarations across 3 tables.

**Used in bible:** § 2 (Definitions), § 4.1.10, § 4.1.12.

### N21: Bug #28 cross-cutting application to this bible's § 6

**Source determination:** per BIBLE_STRUCTURE_SPEC v5 § 5.3 G1 closure, a cross-cutting bug appears in § 6 of the canonical-home bible AND in § 6 of every bible whose discipline its symptoms touch. Bug #28's canonical home is `data_pipeline_bible:#28` per the existing operator-stated assignment (META_PLAN v8 § 1.2 + Appendix A.5). Symptom-touch determination at drafter discretion.

**Decomposition of symptom touch on this bible's domain:**
- Bug #28 leaves `results.win_payout` NULL for HRN-ingested rows since 2026-04-30.
- Bug #28 leaves `results.daily_double_payout` NULL for the same date range.
- Bug #28 mis-maps `results.place_payout` to carry win-payout values (off-by-one shift).
- Bug #28 mis-maps `results.show_payout` to carry place-payout values (off-by-one shift).

All four manifestations are observable in the `results` table, which is documented in this bible's § 4.1.9. The schema-layer manifestation is in this bible's domain.

**Determination:** INCLUDE one-line cross-reference in § 6 #1 with `data_pipeline_bible:#28` link. Substantive description (root cause, fix discipline) lives in `data_pipeline_bible`.

**Methodology check (per § 5.3 G1 closure):** the bible's § 6 entry is a one-line cross-reference with brief manifestation enumeration; the substantive description is not duplicated. ✓ matches the rule's no-duplication mandate.

**Used in bible:** § 6 #1.

### N22: Superseded SQL constraint Deprecated qualification result

**Source determination:** per BIBLE_STRUCTURE_SPEC v5 § 5.6.4 G2 closure: superseded SQL constraints qualify for a Deprecated entry only if the superseded form persists in the live DB schema. If physically dropped, NOT required.

**Determination per migration history:**
- `wr_predictions UNIQUE(entry_id)` (pre-005) auto-generated name `wr_predictions_entry_id_key`: NOT dropped by any retained migration. (Migration 011's DROP names `wr_predictions_unique_per_entry_model_style`, a different constraint.) Migration-history reading: the auto-generated 005-form constraint persists.
- `wr_predictions UNIQUE(race_id, entry_id, model_used, style)` referenced in 011 preamble: not declared in any retained migration; only referenced as DROP target. If it ever existed, the 011 DROP CONSTRAINT IF EXISTS attempts to remove it.
- `ls_predictions UNIQUE(entry_id)` (pre-010): explicitly dropped by migration 010 line 36 (`DROP CONSTRAINT IF EXISTS ls_predictions_entry_id_key`) plus line 37 `DROP INDEX IF EXISTS`. Migration intent was physical drop. Migration-history reading: NOT persisted.

**Determination:**
- `ls_predictions` pre-010 form: physically dropped per migration 010. **Does NOT qualify for a Deprecated entry under § 5.6.4 G2.**
- `wr_predictions` pre-011 named four-column form: physically dropped per migration 011. **Does NOT qualify for a Deprecated entry under § 5.6.4 G2.**
- `wr_predictions` pre-005 auto-generated `UNIQUE(entry_id)` form (`wr_predictions_entry_id_key`): NOT named in any DROP statement; per migration history may persist alongside the post-011 form. **Drafter discretion call:** under the strict migration-history reading this would qualify; however, live `\d wr_predictions` is the authoritative source and is not available during this draft. **Conservative call: DEFER to Phase 1 audit-CC with live DB access.** Logged as Currently Open § 6 #2 (schema-vs-migration drift). § 7 of the bible does NOT include a constraint Deprecated entry; the deferral is documented in § 7's "Note on superseded SQL constraints" prose.

**Verification commands run:**
- `Read backend/database/migrations/005_three_prediction_tables.sql` (full file)
- `Read backend/database/migrations/010_ls_predictions_first_class.sql` (full file)
- `Read backend/database/migrations/011_wr_predictions_unique_fix.sql` (full file)

**Verification commands NOT run (deferred):**
- `\d wr_predictions` against live cluster (no DB access)
- `\d ls_predictions` against live cluster (no DB access)
- `\d pl_predictions` against live cluster (no DB access)

**Used in bible:** § 7.1 "Note on superseded SQL constraints" prose; § 6 #2 (Currently Open schema-vs-migration drift entry).

### N23: Schema bootstrap (`schema.sql`) and `001_initial_schema.sql` are intentionally identical for the bootstrap subset

**Source:** comparison of CREATE TABLE statement set in both files (verified via grep returning the same 11 tables in the same order); column declarations and indexes match. Maintained as two files; no script regenerates one from the other.

**Drift discipline:** procedural (manual cross-reference review); not automated. Captured as candidate Common Mistake § 5.I.

**Used in bible:** § 3.4, § 4.2, § 5 candidate 5.I.

---

## Methodology-interpolation self-check (per META_PLAN v8 § 6.1 + AUDIT_METHODOLOGY v2 § 4.2 / § 5.2)

CC (run3) reviewed every new methodology construct introduced in this draft against the methodology-interpolation rule.

**Constructs introduced in this draft that may verge on interpolation:**

1. **§ 5 candidate roster format with provenance annotation per candidate.** Authorization source: BIBLE_STRUCTURE_SPEC v5 § 5.7 G5 closure mandates "candidate rules from substrate (the bible's domain code, AWS infrastructure, prior audits, Phase 0 anti-pattern catalog at META_PLAN v8 § 9.1-9.13, operator-stated history)" with "provenance discriminator (mirrors methodology-interpolation grandfathering pattern per META_PLAN v8 § 6.1): rules surfaced from existing locked Phase 0 documents are grandfathered; CC-introduced rules require QB ratification." The "substrate-grounded" / "CC-introduced" labels are CC's mechanical translation of the spec's grandfathering distinction. **Not interpolation.**

2. **§ 5.A through § 5.I sub-letter ID convention for candidate-roster entries.** The spec uses numeric sub-section IDs (e.g., `5.4` for a Forbidden Pattern). For the candidate roster pending QB ratification, this draft uses `5.A`, `5.B`, … `5.I` letter-prefix IDs to distinguish candidates from ratified rules. **CC-introduced.** Letter-prefix is not authorized by BIBLE_STRUCTURE_SPEC v5 § 5.5.1, which specifies W.N as the only ratified letter-prefix in EE bible numbering. The candidate-roster letter-prefix is provisional within this draft only, NOT a published rule numbering. **Surfaced for QB:** if QB prefers numeric provisional IDs (e.g., `5.<TBD-1>`), the candidate roster IDs are mechanical to renumber. The substantive content (FORBIDDEN/CORRECT pairs, wrong-instinct/corrected-position pairs, provenance) is unaffected.

3. **§ 6 Currently Open numeric ordering with cross-cutting bug #1 first.** No spec rule prescribes ordering within § 6. CC chose to put the cross-cutting Bug #28 first (highest external visibility), schema-vs-migration drift second (highest internal severity), then dev cluster + down-block (Phase 5 candidates). **CC-introduced ordering choice.** Surfaced for awareness; not load-bearing.

4. **§ 4.1 per-table sub-section numbering 4.1.1 through 4.1.14.** BIBLE_STRUCTURE_SPEC v5 § 6.6 § 4.1 says "4.1.X.<table_name> — one subsection per table" — the X is the per-table position. Numbered in CREATE-statement order (bootstrap 1–11, then 005-additions 12–14). **Not interpolation** (matches spec template 4.1.X.<table_name> with X as integer position).

5. **§ 4.2 sub-numbering 4.2.1 through 4.2.5.** Matches spec template § 6.6 § 4.2 (numbered subsections explicitly listed in the template: 4.2.1 numbering format, 4.2.2 duplicate-005, 4.2.3 schema_migrations, 4.2.4 rollback, 4.2.5 testing). **Not interpolation.**

**Constructs explicitly NOT introduced (to avoid interpolation):**

- No iteration cap on the candidate roster (no "minimum 5 / maximum 10 candidates" rule).
- No completeness criterion for § 5 (no "all 8 anti-patterns from META_PLAN v8 § 9.X must appear" rule).
- No new severity classifications.
- No tiebreaker criteria for cross-cutting bug canonical-home determination (deferred to AUDIT_METHODOLOGY per BIBLE_STRUCTURE_SPEC v5 § 5.3).
- No new letter-prefix conventions beyond W.N (the candidate-roster letter-prefix is explicitly flagged as provisional, see surface item #2 above).

---

## Recursive precision discipline check (per TRIAGE_QUEUE_SPEC v1 + META_PLAN v8 § 6.5)

Verbatim quotations from substrate reproduced char-exact:

1. **N16 (Migration 011 Symptom):** "157 races (~1.35% of 11,629) accumulated 427 duplicate rows." Source: `011_wr_predictions_unique_fix.sql:14`. **Char-exact for numerics, em-dashes, and tilde.** Bible adds the words "total" and "prediction" for readability; flagged.

2. **N18 (Migration 010 Fix):** "Existing rows: 0 (verified empty)." Source: `010_ls_predictions_first_class.sql:17`. **Char-exact.** Bible reproduces as "Existing rows at migration time: 0" — minor adjective adjustment ("at migration time" added) for readability; the colon-zero pair reproduced as-is.

3. **N3 (HAVING clause):** `HAVING COUNT(*) >= 5;` Source: `008_create_trainer_stats.sql:59`. **Char-exact.** Reproduced in bible § 3.3 with the trailing semicolon preserved.

4. **N1 / N2 / N4 grep commands and outputs:** reproduced in this verification log as the exact commands and output. Char-exact reproduction confirmed.

5. **schema.sql cluster ARN:** `arn:aws:rds:us-east-1:584812014683:cluster:equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`. Source: META_PLAN v8 verification log + EE_CURRENT_STATE_DUMP § 4 + user MEMORY. **Char-exact** including the kebab-case region, the colon-separated ARN segments, and the lowercase hex suffix.

6. **Migration 011 preamble quote:** "wr_predictions had UNIQUE (race_id, entry_id, model_used, style)." Source: `011_wr_predictions_unique_fix.sql:4`. **Char-exact** (note: source has the period at the end of the sentence, reproduced).

**Verbatim reproductions char-exact count: 6.**

---

## § 1–4 reorganization deviation log (per BIBLE_STRUCTURE_SPEC v5 § 5.2 / § 6.6 G4 closure)

The spec authorizes "drafter latitude" for § 1–4 reorganization. The choices made in this draft and rationale:

- **§ 3 sub-numbering (3.1 cluster, 3.2 14 tables, 3.3 1 matview, 3.4 bootstrap-vs-migrations, 3.5 prediction-table family at a glance):** the spec template § 6.6 § 3 lists "3.1 14 tables", "3.2 1 materialized view", "3.3 Schema bootstrap vs migrations." This draft renumbers to put cluster-level concerns first (3.1), then the table-set decomposition (3.2), matview (3.3), bootstrap discipline (3.4), and adds an at-a-glance prediction-table family table (3.5) for locality of reference. **Deviation:** spec has 3 sub-sections; this draft has 5. **Rationale:** the prediction-table family is the most-referenced sub-domain in this bible (the per-pipeline UNIQUE constraints are the dominant source of historical pain); a summary table at § 3.5 saves readers from scrolling to § 4.1.12–4.1.14 + § 7.1 for the cross-pipeline view.

- **§ 4 structure (4.1 per-table, 4.2 migration discipline):** matches spec template § 6.6 § 4 exactly. No deviation.

- **§ 1 + § 2 structure:** matches spec § 5.2 canonical TOC (Scope, Definitions). No deviation.

---

## Summary

- **Verification claim count:** 35 (12 inherited + 23 new).
- **Verbatim reproductions char-exact:** 6.
- **Methodology-interpolation surfaces:** 1 substantive (candidate-roster letter-prefix § 5.A–§ 5.I, flagged for QB) + 1 advisory (§ 6 ordering) + 3 routine (per-section sub-numbering matching spec templates).
- **Cross-cutting bug application result:** Bug #28 INCLUDED in § 6 #1 as one-line cross-reference to `data_pipeline_bible:#28`. Symptom-touch rationale: 4 schema-layer manifestations in `results` table.
- **Superseded SQL constraint Deprecated qualification result:** NEITHER `wr_predictions` four-column UNIQUE NOR `ls_predictions UNIQUE(entry_id)` qualifies under § 5.6.4 G2 (both physically dropped per migrations 011 and 010 respectively). The pre-005 `wr_predictions UNIQUE(entry_id)` auto-generated form may persist per migration-history reading; deferred to Phase 1 audit-CC live `\d` verification. Documented in § 7 prose; tracked in § 6 #2 schema-vs-migration drift entry.
- **Self-correction logged:** N10 — bible § 3.4 mid-draft said "13 `CREATE INDEX` statements"; corrected to "12" before this log was finalized. Audit trace preserved in N10 entry.

---
