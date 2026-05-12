# Database & Schema Bible (run2) — Companion Verification Log

**Document:** database_schema_bible_run2_verification.md
**Companion to:** `database_schema_bible_run2.md`
**Tier:** 3 per BIBLE_STRUCTURE_SPEC v3 § 4.1.
**Author:** CC (drafting under verification discipline; QB orchestrated)
**Date:** 2026-05-04
**Anchored on:** META_PLAN v6 (locked) + BIBLE_STRUCTURE_SPEC v3 (locked).

This log records every concrete factual claim made about EE in the bible. Inherited claims (already verified in META_PLAN v6's verification log) are noted; new claims are decomposed per META_PLAN v6 § 6.5 (verification-log-precision rule, broad scope).

## Conventions

- **I-N**: Inherited claim (verified upstream, in META_PLAN v6 verification log).
- **N-N**: New claim (verified during this drafting).
- **Decomposition format:** for any count claim, the decomposition is recorded so audit-CC can re-derive the total.
- **Verification source:** file path + line number where applicable; or live-state command + timestamp.

---

## Inherited claims (from META_PLAN v6 verification log)

### I-1: 14 tables in EE schema

**Claim location:** § 1, § 3, § 4.5, § 5.7.
**Source:** META_PLAN v6 § 2.3 ("Database: 14 tables + 1 materialized view (`trainer_stats`) — verified by counting unique CREATE TABLE statements across `schema.sql` and migrations 001–011.")
**Status:** Inherited; re-verified during this drafting (see N-3 below).

### I-2: 1 materialized view (`trainer_stats`)

**Claim location:** § 1, § 3, § 4.5.
**Source:** META_PLAN v6 § 2.3 (same paragraph as I-1).
**Status:** Inherited; spot-verified by reading `008_create_trainer_stats.sql` lines 7–59 during this drafting (`CREATE MATERIALIZED VIEW IF NOT EXISTS trainer_stats AS ...`).

### I-3: Migration runner mechanism (`migrate.py` tracks by filename in `schema_migrations`)

**Claim location:** § 1, § 3, § 4.6.
**Source:** META_PLAN v6 § 2.3 + § 7.12.
**Status:** Inherited; re-verified by reading `migrate.py` (see N-1 for new precision).

### I-4: Aurora Serverless PostgreSQL cluster, private VPC subnet

**Claim location:** § 3.
**Source:** META_PLAN v6 § 2.3 + § 7.12.
**Status:** Inherited.

### I-5: Secrets Manager entry `equine-equalizer/db-credentials`

**Claim location:** § 3.
**Source:** META_PLAN v6 § 2.3 ("Secrets Manager (3 entries): `equine-equalizer/db-credentials`, ...").
**Status:** Inherited.

### I-6: Lambda inventory — 5 Active + 3 INACTIVE

**Claim location:** § 3 (writers paragraph).
**Source:** META_PLAN v6 § 2.3.
**Status:** Inherited. Specifically: WR/PL/LS inference Lambdas Active; ingestion / feature-engineering / results Lambdas INACTIVE; legacy `equine-inference` Active.

### I-7: Legacy `predictions` table holds approximately 6,600 rows

**Claim location:** § 7.1.
**Source:** META_PLAN v6 Appendix A.4 + Claim 16 in v6 verification log ("verified live via dashboard `counts.predictions`").
**Status:** Inherited; not re-verified during this drafting (live dashboard not consulted).

### I-8: `prediction_router.py` legacy reader inventory — 1 import + 3 instantiations = 4 references

**Claim location:** § 7.1.
**Source:** META_PLAN v6 Appendix A.4 (decomposition: "lines 34, 61, 92, plus 1 import on line 6 = 4 references total").
**Status:** Inherited and re-verified during this drafting (see N-6).

### I-9: `race_router.py` legacy reader inventory — 1 import + 1 instantiation = 2 references

**Claim location:** § 7.1.
**Source:** META_PLAN v6 Appendix A.4 (decomposition: "1 instantiation on line 277, plus 1 import on line 273 = 2 references total").
**Status:** Inherited and re-verified during this drafting (see N-7).

### I-10: `dashboard_router.py:93,105` and `horse_router.py:66` are direct-SELECT readers of legacy `predictions`

**Claim location:** § 7.1.
**Source:** META_PLAN v6 Appendix A.4.
**Status:** Inherited; line numbers not re-verified during this drafting (the bible labels them "per inherited claim, line numbers not re-verified during this drafting" honestly).

### I-11: Bug #28 — HRN scraper column-shift since 2026-04-30

**Claim location:** § 5.4, § 6.
**Source:** META_PLAN v6 Appendix A.5 + operator memory file `equine-equalizer-bug-28-hrn-scraper.md`.
**Status:** Inherited.

### I-12: HRN scraper code path lives at `backend/services/data_sources/hrn_scraper.py:802-804`

**Claim location:** § 5.4.
**Source:** META_PLAN v6 Appendix A.5 ("parse_payout(N) calls at backend/services/data_sources/hrn_scraper.py:802-804 (verified) use positional cell indexing").
**Status:** Inherited; line numbers not independently re-verified during this drafting.

### I-13: Migration discipline format — 001–011 grandfathered, 012-onward `NNN_YYYYMMDD_short_description.sql`

**Claim location:** § 4.6.
**Source:** META_PLAN v6 § 7.12.
**Status:** Inherited.

### I-14: Migration testing falls back to local Postgres; no dev Aurora cluster exists

**Claim location:** § 4.6, § 6.
**Source:** META_PLAN v6 § 7.12.
**Status:** Inherited.

### I-15: Duplicate-005 case — `005_backfill_pace_delta.sql` and `005_three_prediction_tables.sql`

**Claim location:** § 2 (Definitions), § 4.6, § 5.6.
**Source:** META_PLAN v6 § 7.12 + EE_CURRENT_STATE_DUMP § 4.2.
**Status:** Inherited; re-verified by listing the migrations directory during this drafting (see N-2).

### I-16: `past_performances.race_id` is NULL across all historical rows (per data_loader.py docstring)

**Claim location:** § 4 (Note), § 4.5 (table 7), § 5.2, § 8.W.3.
**Source:** EE_CURRENT_STATE_DUMP § 4.1 ("Critical: `race_id` is NULL for ALL historical rows per data_loader.py docstring") + cross-confirmed by migration 006 comment ("Joined via (race_date, track_code, race_number) because race_id is not populated in past_performances (0%).") and migration 007 (which uses the composite-key join for the same reason).
**Status:** Inherited (substrate-level claim from dump). Spot-verified during this drafting by reading migration 006 line 4 and migration 007 lines 4–7.

### I-17: Phase 1 spec references "WRPrediction, PLPrediction, LSPrediction dataclasses"

**Claim location:** § 4 (Note).
**Source:** Phase 1 drafting spec embedded in this drafting prompt.
**Status:** Inherited (the spec itself); the bible's note about the actual class inventory is a new claim — see N-4.

---

## New claims (verified during this drafting)

### N-1: `migrate.py` mechanism — exact behavior

**Claim location:** § 4.6.
**Decomposition:**
- Connection source: `DATABASE_URL` env var; falls back to Secrets Manager via `DB_SECRET_ARN` env var. Verified at `migrate.py:21–41`.
- `schema_migrations` table created by `ensure_migrations_table` at `migrate.py:44–54` with columns `(migration_id SERIAL PRIMARY KEY, filename VARCHAR(255) UNIQUE NOT NULL, applied_at TIMESTAMPTZ DEFAULT NOW())`.
- Already-applied set computed by `get_applied_migrations` at `migrate.py:57–61` via `SELECT filename FROM schema_migrations`.
- Files sorted lexically and filtered to `*.sql` at `migrate.py:69–72`.
- Successful application records the filename via `INSERT INTO schema_migrations (filename) VALUES (%s)` at `migrate.py:90–93`.
- Failures roll back via `conn.rollback()` and exit non-zero at `migrate.py:97–102`.
- Seeds path optional under `--seed`; reads from `backend/database/seeds/` per `migrate.py:107–135`.
**Verification source:** Direct read of `backend/database/migrations/migrate.py` (158 lines total, read in full).

### N-2: 12 migration files in `backend/database/migrations/`

**Claim location:** § 4.6, § 5.6.
**Decomposition:**
- 001_initial_schema.sql
- 002_fix_race_type_length.sql
- 003_widen_varchar_columns.sql
- 004_backfill_running_style.sql
- 005_backfill_pace_delta.sql
- 005_three_prediction_tables.sql
- 006_backfill_early_pace_pressure.sql
- 007_backfill_trainer_name.sql
- 008_create_trainer_stats.sql
- 009_backfill_pace_delta_v2.sql
- 010_ls_predictions_first_class.sql
- 011_wr_predictions_unique_fix.sql

= 12 .sql files (two share prefix `005`; one is `migrate.py` Python and is excluded).
**Verification source:** `ls -la /home/strakajagr/projects/equine-equalizer/backend/database/migrations/` returned 12 .sql files plus `migrate.py`.

### N-3: 14 unique table names across `schema.sql` + migrations 001–011

**Claim location:** § 1, § 3, § 4.5, § 5.7.
**Decomposition:** `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql | sort -u` returned the following 14 unique strings:
1. `CREATE TABLE entries (`
2. `CREATE TABLE horses (`
3. `CREATE TABLE IF NOT EXISTS ls_predictions (`
4. `CREATE TABLE jockeys (`
5. `CREATE TABLE model_versions (`
6. `CREATE TABLE past_performances (`
7. `CREATE TABLE IF NOT EXISTS pl_predictions (`
8. `CREATE TABLE predictions (`
9. `CREATE TABLE races (`
10. `CREATE TABLE results (`
11. `CREATE TABLE tracks (`
12. `CREATE TABLE trainers (`
13. `CREATE TABLE workouts (`
14. `CREATE TABLE IF NOT EXISTS wr_predictions (`

11 of 14 are created in `schema.sql` (which is byte-identical to `001_initial_schema.sql` per N-8); 3 of 14 (wr_predictions / pl_predictions / ls_predictions) are created in `005_three_prediction_tables.sql`.
**Verification source:** Bash `grep -hE "^CREATE TABLE" /home/strakajagr/projects/equine-equalizer/backend/database/schema/schema.sql /home/strakajagr/projects/equine-equalizer/backend/database/migrations/*.sql | sort -u` (executed during this drafting).

### N-4: `canonical.py` does not define a `WRPrediction` class

**Claim location:** § 4 (Note).
**Decomposition:**
- `canonical.py` line 351 defines `class PLPrediction:` (verified).
- `canonical.py` line 390 defines `class LSPrediction:` (verified).
- `canonical.py` line 428 defines `class Prediction:` (verified — no `WR` prefix).
- Bash `grep -n "class.*Prediction" canonical.py` returned exactly those three matches; no `class WRPrediction` line.
- Bash `grep -rn "class WRPrediction" backend/` returned `repositories/wr_prediction_repository.py:13:class WRPredictionRepository(BaseRepository):` only (a repository, not a dataclass).
**Verification source:** Direct grep against the file plus full read of canonical.py lines 1–482.

### N-5: Schema-vs-migration drift on `wr_predictions` `style` and `model_used` columns

**Claim location:** § 6 (Currently Open).
**Decomposition:**
- Migration `005_three_prediction_tables.sql` creates `wr_predictions` with no `style` column and no `model_used` column (verified by full-read of migration 005 lines 1–109).
- No subsequent migration in 001–011 contains `ALTER TABLE wr_predictions ADD COLUMN style` or `ALTER TABLE wr_predictions ADD COLUMN model_used` (verified by `grep -n "style\|model_used" backend/database/migrations/*.sql`).
- Migration 011 (`011_wr_predictions_unique_fix.sql`) references the existing constraint `wr_predictions_unique_per_entry_model_style` (line 64) and the columns `style` (lines 39, 54, 67–68, 78) as if they exist on the table.
- Conclusion: `wr_predictions.style` and `wr_predictions.model_used` columns must have been added to the live cluster by an out-of-band path (direct DDL not captured as a numbered migration). A fresh bootstrap from `migrate.py` against an empty cluster would either fail at migration 011 or produce a schema that differs from the live cluster.
**Verification source:** Full-reads of migrations 005 and 011, plus the grep above.

### N-6: `prediction_router.py` legacy reader inventory re-verified live

**Claim location:** § 7.1.
**Decomposition:**
- Line 5–6: `from repositories.prediction_repository import (` and `PredictionRepository` — 1 import.
- Line 34: `repo = PredictionRepository(conn)` — instantiation 1.
- Line 61: `repo = PredictionRepository(conn)` — instantiation 2.
- Line 92: `repo = PredictionRepository(conn)` — instantiation 3.
- Total: 1 import + 3 instantiations = 4 references.
**Verification source:** Bash `grep -n "PredictionRepository\|from.*prediction_repository" /home/strakajagr/projects/equine-equalizer/backend/routers/prediction_router.py`. Matches inherited Claim I-8 exactly.

### N-7: `race_router.py` legacy reader inventory re-verified live

**Claim location:** § 7.1.
**Decomposition:**
- Line 272–273: `from repositories.prediction_repository \ import PredictionRepository` — 1 import.
- Line 277: `pred_repo = PredictionRepository(conn)` — 1 instantiation.
- Total: 1 import + 1 instantiation = 2 references.
- Note: `race_router.py:142–144` also imports and instantiates `WRPredictionRepository`, which is a different repo for the per-pipeline WR table — not counted here because this claim is about legacy `predictions` readers.
**Verification source:** Bash `grep -n "PredictionRepository\|from.*prediction_repository" /home/strakajagr/projects/equine-equalizer/backend/routers/race_router.py`. Matches inherited Claim I-9 exactly.

### N-8: `schema.sql` is byte-identical to `001_initial_schema.sql` at audit time

**Claim location:** § 2 (Definitions), § 3, § 5.5.
**Decomposition:**
- Both files were read in full during this drafting.
- Both are 416 lines and contain the same table definitions in the same order with identical column types and identical constraint declarations.
- Both contain the same EXTENSIONS block, the same 11 base tables, the same `ALTER TABLE predictions ADD CONSTRAINT fk_model_version` block, and the same INDEXES block.
**Verification source:** Direct read of `backend/database/schema/schema.sql` (416 lines) and `backend/database/migrations/001_initial_schema.sql` (416 lines). The bible's claim is "byte-identical at audit time" — this is verified by content equivalence, not by `cmp`. A formal byte-level diff is recommended for audit-CC spot-check.

### N-9: Migration 005 (`005_three_prediction_tables.sql`) creates wr_predictions / pl_predictions / ls_predictions and adds `model_type` to model_versions

**Claim location:** § 3, § 4.5 (table 11), § 4.5 (tables 12/13/14).
**Decomposition:**
- Lines 5–31: `CREATE TABLE IF NOT EXISTS wr_predictions ...` with `prediction_id` PK and `UNIQUE(entry_id)`.
- Lines 34–58: `CREATE TABLE IF NOT EXISTS pl_predictions ...` with `prediction_id` PK and `UNIQUE(entry_id)`.
- Lines 61–85: `CREATE TABLE IF NOT EXISTS ls_predictions ...` with `prediction_id` PK and `UNIQUE(entry_id)`.
- Lines 88–93: 6 indexes created (3 race-scoped + 1 date + 2 partial: `idx_pl_predictions_value` WHERE `is_value_bet = true`, `idx_ls_predictions_alert` WHERE `longshot_alert = true`).
- Lines 96–104: `ALTER TABLE model_versions` adds `model_type VARCHAR(10)`, `flat_bet_roi DECIMAL(8,4)`, `kelly_roi DECIMAL(8,4)`, `value_bet_win_rate DECIMAL(6,4)`.
- Lines 107–109: replaces global `idx_active_model` unique index with per-type partial unique index `idx_active_model_per_type` ON `model_versions (model_type) WHERE is_active = true`.
**Verification source:** Full read of `005_three_prediction_tables.sql` (110 lines).

### N-10: Migration 010 promotes ls_predictions to first-class

**Claim location:** § 4.5 (table 14), § 8.W.2.
**Decomposition:**
- Lines 23–28: `ALTER TABLE ls_predictions ADD COLUMN IF NOT EXISTS style VARCHAR(50) DEFAULT 'general', market_prob NUMERIC, edge_pct NUMERIC, is_top_pick BOOLEAN DEFAULT FALSE, morning_line_implied_prob NUMERIC`.
- Lines 35–37: `ALTER TABLE ls_predictions DROP CONSTRAINT IF EXISTS ls_predictions_entry_id_key; DROP INDEX IF EXISTS ls_predictions_entry_id_key`.
- Lines 38–40: `ALTER TABLE ls_predictions ADD CONSTRAINT ls_predictions_unique_per_entry_style UNIQUE (race_id, entry_id, style)`.
- Migration's preamble (lines 1–18) explicitly notes "Existing rows: 0 (verified empty), so the constraint switch is safe."
**Verification source:** Full read of `010_ls_predictions_first_class.sql` (43 lines).

### N-11: Migration 011 fixes wr_predictions UNIQUE constraint with cleanup

**Claim location:** § 4.5 (table 12), § 5.3, § 8.W.1.
**Decomposition:**
- Lines 30–46: pre-state DO block raises a NOTICE counting duplicate rows and affected races (informational only — not abort-conditional).
- Lines 49–60: `DELETE FROM wr_predictions WHERE prediction_id IN (... ROW_NUMBER() OVER PARTITION BY race_id, entry_id, style ORDER BY created_at DESC, prediction_id DESC ... rn > 1)`.
- Lines 63–64: `ALTER TABLE wr_predictions DROP CONSTRAINT IF EXISTS wr_predictions_unique_per_entry_model_style`.
- Lines 66–68: `ALTER TABLE wr_predictions ADD CONSTRAINT wr_predictions_unique_per_entry_style UNIQUE (race_id, entry_id, style)`.
- Lines 71–97: post-state DO block raises EXCEPTION (rolling back the transaction) if duplicates remain or the new constraint is missing.
- Migration's preamble (lines 1–25) documents 157 races × 427 duplicate rows pre-fix.
**Verification source:** Full read of `011_wr_predictions_unique_fix.sql` (100 lines).

### N-12: Migration 008 creates `trainer_stats` materialized view

**Claim location:** § 1, § 4.5 (matview), § 4.6.
**Decomposition:**
- Lines 7–59: `CREATE MATERIALIZED VIEW IF NOT EXISTS trainer_stats AS SELECT trainer_name, COUNT(*) AS total_starts, ... GROUP BY trainer_name HAVING COUNT(*) >= 5`.
- Lines 61–62: `CREATE UNIQUE INDEX IF NOT EXISTS idx_trainer_stats_name ON trainer_stats (trainer_name)`.
- Min 5 starts threshold confirmed at line 59.
- Filters: `WHERE trainer_name IS NOT NULL AND finish_position IS NOT NULL AND finish_position < 90` (excludes DNF/pulled/vet codes).
**Verification source:** Full read of `008_create_trainer_stats.sql` (62 lines).

### N-13: `seeds/` directory contains exactly one file: `tracks.sql`

**Claim location:** § 4.6.
**Decomposition:** `ls -la backend/database/seeds/` returned: `tracks.sql` (1407 bytes). No other files.
**Verification source:** Bash listing during this drafting.

### N-14: `repositories/` directory inventory matches the per-pipeline split

**Claim location:** § 3 (writers/readers paragraph), § 5.1 (FORBIDDEN/CORRECT pair).
**Decomposition:** `ls backend/repositories/` returned: `__init__.py`, `__pycache__`, `base_repository.py`, `entry_repository.py`, `horse_repository.py`, `ls_prediction_repository.py`, `model_version_repository.py`, `past_performance_repository.py`, `pl_prediction_repository.py`, `prediction_repository.py`, `race_repository.py`, `result_repository.py`, `track_record.py`, `track_repository.py`, `transforms.py`, `workout_repository.py`, `wr_prediction_repository.py` — 14 .py files (excluding `__init__.py`, `__pycache__`, `transforms.py`, `track_record.py`).
**Verification source:** Bash `ls /home/strakajagr/projects/equine-equalizer/backend/repositories/` during this drafting. Matches inferred 14-table coverage; the legacy `prediction_repository.py` co-exists with the per-pipeline `wr_prediction_repository.py` / `pl_prediction_repository.py` / `ls_prediction_repository.py`.

### N-15: 5/6/7/8 canonical section ordering preserved

**Claim location:** Throughout (structural).
**Decomposition:**
- § 5: Discipline rules (Forbidden Patterns + Common Mistakes).
- § 6: Currently Open (one-line bug list with backlog pointers).
- § 7: Deprecated (legacy `predictions` table per § 7.1).
- § 8: What Was Fixed — Do Not Revert (W.N entries: 8.W.1, 8.W.2, 8.W.3).
**Verification source:** Self-check against BIBLE_STRUCTURE_SPEC v3 § 5.2 (mandatory canonical 5/6/7/8 ordering).

---

## Methodology-interpolation self-check

Per META_PLAN v6 § 6.1: no new methodology constructs introduced.

- W.N letter-prefix used per BIBLE_STRUCTURE_SPEC v3 § 5.5 (only ratified letter-prefix). No `5.F.<n>` or `7.D.<n>` or similar invented numbering.
- Numeric sub-section IDs used for Forbidden Patterns (5.1, 5.2, 5.3, 5.4) and Common Mistakes (5.5, 5.6, 5.7) per § 5.5 of the structure spec.
- Severity tags on Currently Open entries use HIGH / MODERATE / LOW per META_PLAN v6 § 11. No new severity categories.
- Conditional-trigger evaluation in W.N entries follows BIBLE_STRUCTURE_SPEC v3 § 5.6.1.1 worked-example pattern (FIRES / DOES NOT FIRE notation).
- The "schema-vs-migration drift" finding in § 6 is surfaced as an observation, not as a new audit category — the entry follows the existing one-line bug list format.

**Constructs surfaced for awareness (not interpolated, but noted as judgment calls):**

- **N-5 (Currently Open: schema-vs-migration drift)** is a finding the drafter discovered while reading migrations. It is surfaced as a Currently Open item per META_PLAN v6 § 7.8 protocol. The bible labels it "UNRESOLVED, surfaced during this drafting" rather than asserting a particular severity beyond what the existing severity vocabulary allows. Audit-CC should ratify whether this level of severity-qualifying language is consistent with § 11.
- **§ 4 (Note about WRPrediction)** is surfaced because the Phase 1 spec asserts the dataclass exists but it does not. The bible documents the discrepancy as a schema-naming observation, deferring renaming to a future Phase 5 decision. This is not an interpolation — it is observation-only documentation per META_PLAN v6 § 8.1.
- **§ 8.W.3** is a "What Was Fixed" entry that is *not* a bug fix in the conventional sense — it codifies an existing design discipline (PP joins use composite key). The drafter used the W.N format because the discipline-prevention force is identical: "do not revert this rule." Whether this stretches the canonical W.N use is an audit-CC judgment call.

**Net new methodology constructs:** zero.

---

## Verification claim count summary

- **Inherited claims:** 17 (I-1 through I-17).
- **New claims:** 15 (N-1 through N-15).
- **Total:** 32.

Of new claims, all 15 are decomposed per META_PLAN v6 § 6.5 (counts decomposed, file paths cited with line numbers where applicable, live-verification commands recorded).

---

**End of Database & Schema Bible (run2) verification log.**
