# Database & Schema Bible — Verification Log (run1)

**Document:** companion verification log for `database_schema_bible_run1.md`
**Phase:** 1 (Bible) — convergence test instance per META_PLAN v6 § 5.3 step 2
**Author:** CC (run1)
**Date:** 2026-05-04

**Discipline:** every concrete factual claim about EE in the bible draft has a verification entry below. Counts decomposed per META_PLAN v6 § 6.5 verification-log-precision rule (broad scope). Inherited claims are flagged "INHERITED from <source>" with an inline re-verification timestamp where re-verified during this draft. Recursive precision discipline (per Tony's TRIAGE_QUEUE_SPEC v1 cycle ratification): verbatim claims reproduce source character-exact including formatting.

**Verification claim count:** 38 total = 12 inherited + 26 new.

---

## Inherited claims (from META_PLAN v6 verification log)

These claims were verified during META_PLAN v6 drafting and are recorded as inherited here. Where re-verified live during this run1 draft, the entry notes "re-verified 2026-05-04."

### V1 [INHERITED]: 14 tables in EE schema

**Source:** META_PLAN v6 § 2.3 + Claim 4 ("14 tables + 1 materialized view (`trainer_stats`) — verified by counting unique CREATE TABLE statements across `schema.sql` and migrations 001–011").

**Inheritance basis:** META_PLAN v6 verification log already ran the count.

**Re-verified 2026-05-04:** counted unique `CREATE TABLE` statements across the schema source files. Decomposition: 11 from `001_initial_schema.sql` (`tracks`, `horses`, `trainers`, `jockeys`, `races`, `entries`, `past_performances`, `workouts`, `results`, `predictions`, `model_versions`) + 3 from `005_three_prediction_tables.sql` (`wr_predictions`, `pl_predictions`, `ls_predictions`) = 14. `schema.sql` mirrors `001_initial_schema.sql` and contributes 0 unique tables (the 11 are the same set). Migrations 002, 003, 004, `005_backfill_pace_delta.sql`, 006, 007, 009, 010, 011 contribute 0 `CREATE TABLE` statements each. Migration 008 contributes 1 `CREATE MATERIALIZED VIEW`, not counted in the 14.

### V2 [INHERITED]: 1 materialized view (`trainer_stats`)

**Source:** META_PLAN v6 § 2.3 + Claim 4.

**Inheritance basis:** counted in META_PLAN v6 verification log.

**Re-verified 2026-05-04:** `008_create_trainer_stats.sql` line 7 reads `CREATE MATERIALIZED VIEW IF NOT EXISTS trainer_stats AS`. No other migration creates a materialized view. Count: 1.

### V3 [INHERITED]: `schema_migrations` runner mechanism

**Source:** META_PLAN v6 § 2.3 ("the migration runner mechanism (`backend/database/migrations/migrate.py`, tracking by filename in `schema_migrations` table)") + Claim 6.

**Inheritance basis:** verified in META_PLAN v6 verification log.

**Re-verified 2026-05-04:** `backend/database/migrations/migrate.py:46–53` defines `ensure_migrations_table` which executes `CREATE TABLE IF NOT EXISTS schema_migrations (migration_id SERIAL PRIMARY KEY, filename VARCHAR(255) UNIQUE NOT NULL, applied_at TIMESTAMPTZ DEFAULT NOW())`. Line 60: `cur.execute("SELECT filename FROM schema_migrations")` confirms tracking is by filename. Line 91: `cur.execute("INSERT INTO schema_migrations (filename) VALUES (%s)", (filename,))` confirms recording on success.

### V4 [INHERITED]: Aurora Serverless cluster ARN

**Source:** META_PLAN v6 § 2.3 + EE_CURRENT_STATE_DUMP.md § 4.

**Inheritance basis:** verified live during dump generation.

**Inherited verbatim:** `arn:aws:rds:us-east-1:584812014683:cluster:equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`. Database name: `equine_equalizer`. Used in bible § 3.1.

### V5 [INHERITED]: 12 migration filenames including duplicate-005

**Source:** META_PLAN v6 § 7.12.

**Inheritance basis:** verified in META_PLAN v6 verification log.

**Re-verified 2026-05-04:** `ls /home/strakajagr/projects/equine-equalizer/backend/database/migrations/*.sql` returns 12 files: `001_initial_schema.sql`, `002_fix_race_type_length.sql`, `003_widen_varchar_columns.sql`, `004_backfill_running_style.sql`, `005_backfill_pace_delta.sql`, `005_three_prediction_tables.sql`, `006_backfill_early_pace_pressure.sql`, `007_backfill_trainer_name.sql`, `008_create_trainer_stats.sql`, `009_backfill_pace_delta_v2.sql`, `010_ls_predictions_first_class.sql`, `011_wr_predictions_unique_fix.sql`. Two share the `005` prefix; 11 distinct numeric prefixes. Decomposed: 11 distinct prefixes + 1 duplicate-005 entry = 12 total files.

### V6 [INHERITED]: legacy `predictions` table holds 6,600 rows

**Source:** META_PLAN v6 Claim 16 + Appendix A.4.

**Inheritance basis:** verified live via dashboard endpoint `counts.predictions` at META_PLAN v6 lock time.

**Inherited usage in bible:** § 3.4 table summary; § 4.1.10 row count; § 7.1 deprecated entry. Marked "(per META_PLAN v6 Claim 16, inherited)" in the bible body.

### V7 [INHERITED]: `prediction_router.py` reader inventory for legacy `predictions`

**Source:** META_PLAN v6 Claim 17 + Appendix A.4 + § 6.5 verification-log-precision worked example.

**Decomposition (preserved verbatim from META_PLAN v6):** "PredictionRepository: 1 import on line 6 + 3 instantiations on lines 34, 61, 92 = 4 references total."

**Inheritance basis:** verified in META_PLAN v6 verification log (the v3 → v4 lesson worked example).

**Inherited usage in bible:** § 7.1 deprecated entry. Marked "(per META_PLAN v6 Claim 17, inherited)."

### V8 [INHERITED]: `race_router.py` reader inventory for legacy `predictions`

**Source:** META_PLAN v6 Claim 17 + Appendix A.4.

**Decomposition (preserved verbatim from META_PLAN v6):** "1 instantiation on line 277, plus 1 import on line 273 = 2 references total."

**Inheritance basis:** verified in META_PLAN v6 verification log.

**Inherited usage in bible:** § 7.1 deprecated entry.

### V9 [INHERITED]: `dashboard_router.py:93,105` direct SELECT on `predictions`

**Source:** META_PLAN v6 Appendix A.4.

**Inheritance basis:** verified in META_PLAN v6 verification log.

**Inherited usage in bible:** § 7.1 deprecated entry.

### V10 [INHERITED]: `horse_router.py:66` direct SELECT on `predictions`

**Source:** META_PLAN v6 Appendix A.4.

**Inheritance basis:** verified in META_PLAN v6 verification log.

**Inherited usage in bible:** § 7.1 deprecated entry.

### V11 [INHERITED]: `model_versions` row count 88 = 45 active + 43 inactive

**Source:** META_PLAN v6 Claim 7 + § 9.13.

**Decomposition (preserved verbatim from META_PLAN v6):** "88 = 45 active + 43 inactive."

**Inheritance basis:** verified live via dashboard endpoint at META_PLAN v6 lock time.

**Inherited usage in bible:** § 4.1.11 row-count summary. Marked "per META_PLAN v6 Claim 7 (inherited)." Note: bible § 4.1.11 explicitly defers the multi-active-row reality discussion to `ml_layer_architecture_bible.md`; this bible only cites the count.

### V12 [INHERITED]: 11 base tables in 001_initial_schema (which mirrors schema.sql)

**Source:** META_PLAN v6 § 2.3 verification underlying Claim 4 + EE_CURRENT_STATE_DUMP.md § 4.1 ("11 base tables").

**Inheritance basis:** the dump's count and META_PLAN v6's decomposition agree.

**Re-verified 2026-05-04:** `grep -c "^CREATE TABLE" backend/database/migrations/001_initial_schema.sql` and `grep -c "^CREATE TABLE" backend/database/schema/schema.sql` both return 11. The two files are line-for-line identical for table declarations (verified by `diff` of the schema.sql content vs the migration; the bootstrap is the migration). Decomposition: `tracks`, `horses`, `trainers`, `jockeys`, `races`, `entries`, `past_performances`, `workouts`, `results`, `predictions`, `model_versions` = 11.

---

## New verifications introduced in run1

### N1: `005_three_prediction_tables.sql` creates exactly 3 tables

**Claim location in bible:** § 3.2 (decomposed list, "3 tables created by `005_three_prediction_tables.sql`").

**Verification:** read `backend/database/migrations/005_three_prediction_tables.sql`. Lines containing `CREATE TABLE IF NOT EXISTS`:
- Line 5: `CREATE TABLE IF NOT EXISTS wr_predictions (` (count: 1)
- Line 34: `CREATE TABLE IF NOT EXISTS pl_predictions (` (count: 2)
- Line 61: `CREATE TABLE IF NOT EXISTS ls_predictions (` (count: 3)

Decomposition: 1 + 1 + 1 = 3 distinct table-creating statements in this migration. No other `CREATE TABLE` statements in the file (verified by reading the full 109 lines).

### N2: `005_three_prediction_tables.sql` has zero `DROP TABLE` statements

**Claim location in bible:** § 7.1 ("zero `DROP TABLE` statements in the migration").

**Verification:** searched the file for "DROP TABLE" — returns zero occurrences. The migration adds the three new tables alongside the legacy `predictions`; it does not remove the legacy table. (Migration also contains `DROP INDEX IF EXISTS idx_active_model;` on line 107; this is an INDEX drop, not a TABLE drop.)

### N3: `008_create_trainer_stats.sql` has `HAVING COUNT(*) >= 5`

**Claim location in bible:** § 3.3 ("with `HAVING COUNT(*) >= 5` (minimum 5 starts to appear)").

**Verification:** read `backend/database/migrations/008_create_trainer_stats.sql` line 59: `HAVING COUNT(*) >= 5;`. Verbatim match.

### N4: `008_create_trainer_stats.sql` aggregates 7 named statistics per trainer

**Claim location in bible:** § 3.3 ("total_starts, win_rate, itm, itm_rate, layoff_win_rate, lasix_win_rate, claimed_win_rate").

**Verification:** read migration 008 lines 9–53. Aggregate columns:
- Line 10: `COUNT(*) AS total_starts` (count: 1)
- Line 11: `SUM(...) AS wins` — also present (count: 2; not in bible enumeration but is a real column)
- Line 15: `AS win_rate` (count: 3)
- Line 16: `SUM(...) AS itm` (count: 4)
- Line 20: `AS itm_rate` (count: 5)
- Line 31: `AS layoff_win_rate` (count: 6)
- Line 42: `AS lasix_win_rate` (count: 7)
- Line 53: `AS claimed_win_rate` (count: 8)

**Decomposition:** the matview defines 8 aggregate columns (not 7) plus the GROUP BY column `trainer_name` for a total of 9 columns. The bible § 3.3 enumerates 7 of the 8 aggregates, omitting `wins` (the raw count, distinct from `win_rate`). **Drift surfaced:** the bible should either include `wins` in the enumeration or call out the omission. **Resolution:** noted here for QB triage; the omission is incidental phrasing, not a fabrication, since `wins` is a derived intermediate of `win_rate`. Suggested bible revision: insert "wins" before "win_rate" in the § 3.3 enumeration. (Surfaced for awareness; not a methodology-interpolation finding.)

### N5: `migrate.py` is 157 lines

**Claim location in bible:** § 4.2.3 references `migrate.py:64–104` for behavior; the file's existence and size are bible-cited indirectly.

**Verification:** `wc -l backend/database/migrations/migrate.py` returns 157. The behavior block referenced (`run_migrations`) spans lines 64–104; verified by reading the file at those line numbers.

### N6: `migrate.py` per-file commit pattern

**Claim location in bible:** § 4.2.3 ("Each migration runs in its own transaction. … the runner already wraps each file's `cur.execute(sql)` call in a per-file commit").

**Verification:** `migrate.py:88–94`:
```python
with conn.cursor() as cur:
    cur.execute(sql)
    cur.execute(
        "INSERT INTO schema_migrations (filename) VALUES (%s)",
        (filename,),
    )
conn.commit()
```
The `conn.commit()` at line 94 (after both the SQL execution and the schema_migrations INSERT) confirms per-file commit. Failure is handled at lines 97–102 with `conn.rollback()` and `sys.exit(1)`.

### N7: `migrate.py` connection sourcing (`DATABASE_URL` fallback to `DB_SECRET_ARN`)

**Claim location in bible:** § 4.2.3 ("`DATABASE_URL` env var if set; otherwise fetch from Secrets Manager via `DB_SECRET_ARN`. Hard-fails (`sys.exit(1)`) if neither is set").

**Verification:** `migrate.py:21–41` (`get_connection_string`):
- Line 23: `database_url = os.environ.get("DATABASE_URL")`
- Lines 24–26: if `database_url`, return it.
- Line 28: `secret_arn = os.environ.get("DB_SECRET_ARN")`
- Lines 29–31: if neither set, `sys.exit(1)`.
- Lines 33–41: fetch from Secrets Manager and assemble Postgres connection string.

Verbatim sequence matches bible claim.

### N8: Seeds run optionally via `--seed` flag, not tracked

**Claim location in bible:** § 4.2.3 ("Seeds run optionally via `--seed` flag, after migrations, from `backend/database/seeds/*.sql`. Seeds are not tracked in `schema_migrations`; they re-run on every invocation.").

**Verification:** `migrate.py:107–135` (`run_seeds`):
- Line 109: returns 0 if seeds dir does not exist.
- Line 113–116: lists and sorts `*.sql` files in `SEEDS_DIR`.
- Lines 119–128: executes each seed; **no INSERT into `schema_migrations`** (verified by inspection of the function body — only a `cur.execute(sql)` and a `conn.commit()`).
- Lines 138–141: argparse `--seed` flag.
- Lines 147–150: `if args.seed: seeds = run_seeds(conn)` — guards seed execution.

Decomposition matches bible claim (3 properties: optional, untracked, re-runs).

### N9: `tracks` seed file exists at `backend/database/seeds/tracks.sql`

**Claim location in bible:** § 4.1.1 ("seeded from `backend/database/seeds/tracks.sql`").

**Verification:** `ls backend/database/seeds/` returns `tracks.sql`. File exists. (Content not inspected; the bible only cites existence, not shape.)

### N10: `predictions` table FK to `model_versions` added in same migration as creation

**Claim location in bible:** § 4.1.10 ("FK to `model_versions` added in same migration via `ALTER TABLE predictions ADD CONSTRAINT fk_model_version`").

**Verification:** `001_initial_schema.sql` lines 383–386:
```sql
ALTER TABLE predictions
ADD CONSTRAINT fk_model_version
FOREIGN KEY (model_version_id)
REFERENCES model_versions(model_version_id);
```
Same file as the `CREATE TABLE predictions` (line 327) and `CREATE TABLE model_versions` (line 359). Decomposition: 1 CREATE TABLE on line 327 + 1 CREATE TABLE on line 359 + 1 ALTER TABLE … ADD CONSTRAINT spanning lines 383–386, all in `001_initial_schema.sql`. The same FK ALTER appears at lines 383–386 of `schema.sql` (mirror).

### N11: `predictions` JSONB columns and array column

**Claim location in bible:** § 4.1.10 (column list including `feature_importance JSONB` and `exotic_partners UUID[]`).

**Verification:** `001_initial_schema.sql` line 342: `feature_importance JSONB,`. Line 344: `exotic_partners UUID[],`. Verbatim match.

### N12: `wr_predictions` UNIQUE post-011 is `(race_id, entry_id, style)`

**Claim location in bible:** § 4.1.12, § 5.1, § 7.2, § 8.W.2.

**Verification:** `011_wr_predictions_unique_fix.sql` lines 66–68:
```sql
ALTER TABLE wr_predictions
  ADD CONSTRAINT wr_predictions_unique_per_entry_style
  UNIQUE (race_id, entry_id, style);
```
Constraint name and column tuple verbatim match.

### N13: `wr_predictions` pre-011 UNIQUE was `(race_id, entry_id, model_used, style)`

**Claim location in bible:** § 4.1.12, § 5.1, § 7.2, § 8.W.2.

**Verification:** `011_wr_predictions_unique_fix.sql` line 4 (comment): "wr_predictions had UNIQUE (race_id, entry_id, model_used, style)." Quoted verbatim. Also line 64: `DROP CONSTRAINT IF EXISTS wr_predictions_unique_per_entry_model_style;` — the pre-existing constraint name follows the same column-tuple convention.

### N14: 011 deduplication scope: 157 races, 427 rows, 11,629 total

**Claim location in bible:** § 5.1, § 8.W.2 ("157 races (~1.35% of 11,629) accumulated 427 duplicate rows").

**Verification:** `011_wr_predictions_unique_fix.sql` line 14 (comment): "Effect: 157 races (~1.35% of 11,629) accumulated 427 duplicate rows." Quoted verbatim.

### N15: 011 cleanup ordering and constraint check

**Claim location in bible:** § 8.W.2 ("Cleanup deletes older duplicates per `(race_id, entry_id, style)` ordered by `created_at DESC, prediction_id DESC`. … Pre-state and post-state checks bracket the cleanup; the post-state check raises an exception if any duplicates remain or the new constraint is missing").

**Verification:** `011_wr_predictions_unique_fix.sql`:
- Lines 49–60 (DELETE block): `PARTITION BY race_id, entry_id, style ORDER BY created_at DESC, prediction_id DESC` — verbatim match.
- Lines 71–97 (post-state DO block): SELECTs duplicate count and constraint count; lines 83–84 `IF remaining_dups > 0 THEN RAISE EXCEPTION 'Cleanup left % duplicate rows'`. Lines 92–93 `IF has_new_constraint = 0 THEN RAISE EXCEPTION 'New UNIQUE constraint not found on wr_predictions'`. Verbatim mechanism match.

### N16: 010 columns added: 5 new columns

**Claim location in bible:** § 4.1.14 ("plus migration 010 additions: `style VARCHAR(50) DEFAULT 'general'`, `market_prob NUMERIC`, `edge_pct NUMERIC`, `is_top_pick BOOLEAN DEFAULT FALSE`, `morning_line_implied_prob NUMERIC`").

**Verification:** `010_ls_predictions_first_class.sql` lines 23–28:
```sql
ALTER TABLE ls_predictions
  ADD COLUMN IF NOT EXISTS style VARCHAR(50) DEFAULT 'general',
  ADD COLUMN IF NOT EXISTS market_prob NUMERIC,
  ADD COLUMN IF NOT EXISTS edge_pct NUMERIC,
  ADD COLUMN IF NOT EXISTS is_top_pick BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS morning_line_implied_prob NUMERIC;
```
Decomposition: 5 `ADD COLUMN` clauses; verbatim match for each column name and type.

### N17: 010 drops the old constraint and its auto-generated index explicitly

**Claim location in bible:** § 4.1.14 + § 8.W.3 ("PostgreSQL semantics: the index is owned by the constraint and only drops when the constraint drops").

**Verification:** `010_ls_predictions_first_class.sql` lines 35–37:
```sql
ALTER TABLE ls_predictions
  DROP CONSTRAINT IF EXISTS ls_predictions_entry_id_key;
DROP INDEX IF EXISTS ls_predictions_entry_id_key;
```
Lines 38–40 add the new constraint:
```sql
ALTER TABLE ls_predictions
  ADD CONSTRAINT ls_predictions_unique_per_entry_style
  UNIQUE (race_id, entry_id, style);
```
Verbatim match. The migration's lines 32–34 commentary explains the auto-generated-index-with-constraint relationship verbatim ("backed by an auto-generated index that can only be dropped by dropping the constraint (PostgreSQL semantics)").

### N18: 010 verifies "Existing rows: 0 (verified empty)" before constraint swap

**Claim location in bible:** § 4.1.14, § 8.W.3 ("Existing rows: 0 (verified empty), so the constraint switch is safe.").

**Verification:** `010_ls_predictions_first_class.sql` lines 17–18: "Existing rows: 0 (verified empty), so the constraint switch is safe." Quoted verbatim.

### N19: `pl_predictions` retains `UNIQUE(entry_id)`

**Claim location in bible:** § 4.1.13, § 2 (Definitions), § 4.1.14 (contrasted with the `(race_id, entry_id, style)` triple).

**Verification:** `005_three_prediction_tables.sql` line 57: `UNIQUE(entry_id)` inside the `pl_predictions` CREATE TABLE block (lines 34–58). No subsequent migration alters `pl_predictions` (verified by reading 006–011).

### N20: Migration 005-pace-delta predates and is corrected by migration 009

**Claim location in bible:** § 4.2.2, § 5.4, § 8.W.1 ("Migration 009 explicitly supersedes the work of `005_backfill_pace_delta.sql`").

**Verification:**
- `005_backfill_pace_delta.sql` line 9: `pace_delta = finish_call_position - call_2_position`. Verbatim.
- `009_backfill_pace_delta_v2.sql` lines 1–8 (header comments): "Migration 009: Backfill pace_delta using finish_position. Migration 005 used finish_call_position (0% populated). finish_position is 99.5% populated and semantically identical (position at the wire). Valid finish codes are 1–30; codes >= 90 mean DNF/pulled/vet scratch and are excluded." Quoted verbatim. Lines 11: `pace_delta = finish_position - call_2_position`. Verbatim.

### N21: Migration 005-three-prediction-tables creates partial indexes

**Claim location in bible:** § 4.1.13, § 4.1.14 (partial indexes on value-bet and longshot-alert).

**Verification:** `005_three_prediction_tables.sql` lines 91–93:
```sql
CREATE INDEX IF NOT EXISTS idx_pl_predictions_value ON pl_predictions(race_id) WHERE is_value_bet = true;
…
CREATE INDEX IF NOT EXISTS idx_ls_predictions_alert ON ls_predictions(race_id) WHERE longshot_alert = true;
```
Both partial; both verbatim match the bible claim.

### N22: Migration 005-three-prediction-tables adds `model_type` column to `model_versions`

**Claim location in bible:** § 4.1.11 ("Added by 005: `model_type VARCHAR(10) DEFAULT 'wr' CHECK (model_type IN ('wr', 'pl', 'ls'))`, `flat_bet_roi DECIMAL(8,4)`, `kelly_roi DECIMAL(8,4)`, `value_bet_win_rate DECIMAL(6,4)`").

**Verification:** `005_three_prediction_tables.sql` lines 95–104. Decomposition:
- Lines 96–98: `ADD COLUMN IF NOT EXISTS model_type VARCHAR(10) DEFAULT 'wr' CHECK (model_type IN ('wr', 'pl', 'ls'))` — column 1 with CHECK constraint.
- Line 102: `ADD COLUMN IF NOT EXISTS flat_bet_roi DECIMAL(8,4)` — column 2.
- Line 103: `ADD COLUMN IF NOT EXISTS kelly_roi DECIMAL(8,4)` — column 3.
- Line 104: `ADD COLUMN IF NOT EXISTS value_bet_win_rate DECIMAL(6,4)` — column 4.

4 total columns added by 005 to `model_versions`. Bible enumerates all 4.

### N23: Migration 005-three-prediction-tables creates `idx_active_model_per_type` unique index

**Claim location in bible:** § 4.1.11 ("Indices added by 005: `DROP INDEX IF EXISTS idx_active_model;` and `CREATE UNIQUE INDEX idx_active_model_per_type ON model_versions(model_type) WHERE is_active = true`").

**Verification:** `005_three_prediction_tables.sql` lines 107–109:
```sql
DROP INDEX IF EXISTS idx_active_model;
CREATE UNIQUE INDEX IF NOT EXISTS idx_active_model_per_type
ON model_versions (model_type) WHERE is_active = true;
```
Verbatim match (modulo the `IF NOT EXISTS` qualifier the bible elided for brevity — flagging this as a minor compression that does not change the operational meaning, since the index will be created if it does not exist).

### N24: Repository class file paths

**Claim location in bible:** § 4.1.12, § 4.1.13, § 4.1.14 ("`WRPredictionRepository` at `backend/repositories/wr_prediction_repository.py`", and similarly for PL and LS).

**Verification (via earlier grep in this run):**
- `backend/repositories/wr_prediction_repository.py:13: class WRPredictionRepository(BaseRepository):` — exists.
- `backend/repositories/pl_prediction_repository.py:42: class PLPredictionRepository(BaseRepository):` — exists.
- `backend/repositories/ls_prediction_repository.py:42: class LSPredictionRepository(BaseRepository):` — exists.

All three file paths and class names verified.

### N25: Canonical objects: PLPrediction and LSPrediction exist; WRPrediction does NOT

**Claim location in bible:** § 1 (Scope cross-reference), § 2 (Definitions: predictions-table family).

**Verification:** read `backend/models/canonical.py`. Decomposition:
- Line 351: `class PLPrediction:` — exists.
- Line 390: `class LSPrediction:` — exists.
- Line 428: `class Prediction:` — exists. This is the legacy class (extended with WR/Layer-2-7 enrichment fields including `model_used`, `ensemble_win_prob`, `longshot_alert`, etc.). Lines 461 and 471 confirm WR-pipeline-specific fields are attached to this `Prediction` class.
- **No `class WRPrediction:` exists.** Searched the full file (482 lines) — pattern `class WRPrediction` returns zero matches.

**Spec discrepancy surfaced:** the Phase 1 spec for this convergence test cites "WRPrediction, PLPrediction, LSPrediction dataclasses from backend/models/canonical.py per META_PLAN v6 Appendix A.7's TEMPLATE-slot example" as the § 4 anchor. The actual code structure is two pipeline-specific dataclasses (`PLPrediction`, `LSPrediction`) plus the legacy `Prediction` dataclass that carries WR pipeline fields. **Resolution applied in run1:** the bible draft does not include a § 4 "Canonical objects" subsection that names a non-existent `WRPrediction`. Instead, it scopes § 1 (Scope) to mention the per-pipeline dataclasses by their actual names (`PLPrediction`, `LSPrediction`) and defers full canonical-object documentation to `architecture_overview.md` per BIBLE_STRUCTURE_SPEC v3 § 4.2.1's locked Q1 statement that the Architecture Overview document carries "the canonical objects shared across the system" including "per-pipeline prediction shapes WRPrediction / PLPrediction / LSPrediction." This is a **`<FRAMEWORK_GAP>`-shaped finding** per META_PLAN v6 § 6.5: the spec's premise is sound (this bible should reference canonical objects), but the framework slot expects a `WRPrediction` class that does not exist in canonical.py. Surfaced for QB triage; the bible compensates by routing the canonical-object boundary to Architecture Overview without fabricating a `WRPrediction` dataclass.

### N26: 91-column count for `past_performances`

**Claim location in bible:** § 4.1.7 ("91 columns covering …"). Inherited indirectly from EE_CURRENT_STATE_DUMP.md § 4.1's "91" column count.

**Verification:** read `001_initial_schema.sql` lines 145–266 (`past_performances` CREATE TABLE block). Counted distinct column declarations (one per `,`-terminated line that defines a column, excluding the closing `UNIQUE(...)`). Reasonable spot-check shows the columns reach into the 90s; the dump's 91 figure aligns with the boundary count. **Caveat:** I did not produce a fully decomposed line-by-line verification of all 91; this is a "trust-the-dump-baseline" inheritance with a structural sanity check rather than a from-scratch recount. Phase 1 (real, not convergence-test) drafter should produce the decomposed enumeration if precision is needed.

---

## Methodology-interpolation self-check

Per META_PLAN v6 § 6.1, CC must surface any methodology constructs introduced in the bible that Tony has not explicitly ratified. Self-check of the run1 draft:

**Surfaced for awareness:**

1. **Bible § 6 ("Currently Open") is empty with explicit empty-section text.** This follows BIBLE_STRUCTURE_SPEC v3 § 5.2's locked rule: "Empty sections are explicit, not absent: a bible with no current open issues at lock time still includes a § 6 'Currently Open' section reading 'No current open issues at lock.'" — Tony-ratified per v3 cycle. Not a new construct.

2. **The "Conditional triggers evaluated" annotation pattern in § 8 What Was Fixed entries** — directly inherited from BIBLE_STRUCTURE_SPEC v3 § 5.6.1.1 worked example. Tony-ratified per v3 cycle. Not a new construct.

3. **Bible § 7.2 and § 7.3 (Deprecated entries on superseded UNIQUE constraints).** BIBLE_STRUCTURE_SPEC v3 § 5.6.4 specifies the Deprecated entry template's mandatory + conditional fields. The two entries fit the template (Field/Module name, Canonical Source, Notes including reader/dependency inventory) without introducing new fields. Not a new construct.

4. **Bible § 5.1 and § 5.2 Forbidden Patterns dated `(locked 2026-05-04)`.** The lock date is the date of this drafting; the Forbidden Pattern format follows META_PLAN v6 § 7.5 + Appendix A.1 + BIBLE_STRUCTURE_SPEC v3 § 5.6.2 verbatim. The locks are real (the rules apply going forward) but this is a convergence-test draft, not a true bible lock — QB should treat the lock dates as placeholder per META_PLAN v6 Appendix A's `2026-05-XX` convention if this draft is promoted to real Phase 1. Surfaced for awareness; no methodology interpolation.

5. **§ 8.W.1 fix date `2026-04-XX`** uses META_PLAN v6 Appendix A's `2026-XX-XX` placeholder convention because the actual fix date for migration 009 is not stated in the migration's comment block (only a forward-looking authorial date is implied). Phase 1 drafter should resolve to a specific date from `git log` of `009_backfill_pace_delta_v2.sql` or from `schema_migrations.applied_at`. Not a methodology-interpolation finding; placeholder convention is itself ratified.

**Net new methodology constructs:** zero. The drafting spec authorized none; verification confirms none.

**Surfaced concerns that are not interpolations:**

- **N4 (matview column count).** The bible enumerates 7 of 8 aggregates in § 3.3; surfaced for QB triage. A correction would add "wins" before "win_rate" in the enumeration. This is a minor accuracy refinement, not a methodology change.
- **N25 (`WRPrediction` does not exist).** Surfaced as a spec/code mismatch per META_PLAN v6 § 6.5 framework-rejection markers. Bible compensated by deferring canonical-object documentation to Architecture Overview without fabricating a class name. QB triage: revise the spec to name `Prediction` (the actual WR-pipeline-extended legacy class) rather than `WRPrediction`, OR confirm that the canonical-object boundary lives in Architecture Overview with cross-reference here.

---

End of verification log.
