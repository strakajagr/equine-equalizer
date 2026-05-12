# Database & Schema Bible

**Document:** database_schema_bible.md
**Phase:** 1 (Bible)
**Status:** DRAFT v1 (convergence-test instance — run2)
**Author:** CC (drafting under verification discipline; QB orchestrated)
**Date:** 2026-05-04
**Locked:** [pending]

**Revision history:**
- v1 (2026-05-04): convergence test draft — second of two independent executions per META_PLAN v6 § 5.3 step 2.

**Tier:** 3 per BIBLE_STRUCTURE_SPEC v3 § 4.1 + META_PLAN v6 § 6.5.

**Anchored on:** META_PLAN v6 (locked) + BIBLE_STRUCTURE_SPEC v3 (locked) + AUDIT_METHODOLOGY v2 (locked) + CONVERGENCE_CRITERIA v2 (locked) + TRIAGE_QUEUE_SPEC v1 (locked).

**Companion verification log:** `_convergence_test/database_schema_bible_run2_verification.md`.

---

## 1. Scope of this bible

This bible is the canonical reference for the Equine Equalizer (EE) database surface area. Its audience is anyone touching schema, repositories, or migrations.

**In scope:**

- The 14 tables defined across `backend/database/schema/schema.sql` and migrations 001 through 011 (per META_PLAN v6 § 2.3 verified inventory).
- The 1 materialized view `trainer_stats` created by migration 008 (per META_PLAN v6 § 2.3).
- The migration runner mechanism: `backend/database/migrations/migrate.py` and the `schema_migrations` tracking table it owns (per META_PLAN v6 § 2.3 + § 7.12).
- JSONB column conventions where present (`feature_importance`, `feature_list`, `hyperparameters`, `exotic_partners` array literal).
- The predictions-table family: legacy `predictions` plus the per-pipeline `wr_predictions`, `pl_predictions`, `ls_predictions` tables (per META_PLAN v6 § 3.2 working hypothesis #6 + Appendix A.4 + § 7.7).
- Migration discipline: the grandfathered 001–011 numbering, the 012-onward `NNN_YYYYMMDD_short_description.sql` format, the duplicate-005 case, and the in-file rollback block convention (per META_PLAN v6 § 7.12).
- UNIQUE constraint conventions across the per-pipeline prediction tables (`UNIQUE(race_id, entry_id, style)` after migrations 010 and 011).
- Foreign key conventions: every prediction row links to `entries` and `races` and `horses`; `entries` link to `races`, `horses`, `trainers`, `jockeys`; `model_versions` is referenced by `model_version_id` from each prediction table.

**Boundary topics covered by other bibles:**

- The repositories that wrap each table — Architecture Overview Bible § 2 and per-pipeline detail in ML Layer Architecture Bible § 4.
- Feature engineering reads against `past_performances` and `workouts` — Feature Provenance Bible § 4.
- Pipelines that write to each table (ingestion, results, inference, retraining) — Data Pipeline Bible § 4.
- HTTP routes that read from the prediction tables (including the legacy `predictions` table) — API & Frontend Bible § 4.
- Calibration metadata fields on `model_versions` — Model Evaluation & Retraining Bible § 4.

**Explicitly out of scope:**

- The Aurora cluster's IAM, networking, parameter group, and backup configuration — those live in Architecture Overview Bible § 3.
- Row-level data quality (e.g., HRN scraper Bug #28's column-shift effect on `results.win_payout`) — Data Pipeline Bible § 4 + § 8.
- Read-side caching, query patterns, or Lambda cold-start behavior touching the database — Architecture Overview Bible § 3 + Data Pipeline Bible § 4.

## 2. Definitions

Terms used throughout this bible. Each is bound to a concrete on-disk artifact or convention; no abstractions.

- **Table.** A persisted relation defined by a `CREATE TABLE` (or `CREATE TABLE IF NOT EXISTS`) statement. EE has 14 such tables.
- **Materialized view.** A persisted relation defined by `CREATE MATERIALIZED VIEW`, populated from a query, and refreshed manually. EE has 1: `trainer_stats` (migration 008).
- **Migration.** A `.sql` file in `backend/database/migrations/` applied by `migrate.py`. Tracked by filename in `schema_migrations`.
- **Schema bootstrap.** `backend/database/schema/schema.sql` — the authoritative description of the tables that migration 001 creates. The bootstrap and migration 001 are byte-identical at audit time (verified). The bootstrap is not part of the migration runner's input and is provided for read-only inspection of the post-001 ground state.
- **JSONB.** PostgreSQL's binary JSON column type. EE uses it for sparse / shape-evolving payloads: `feature_importance`, `feature_list`, `hyperparameters`. Default `'{}'` where present.
- **JSONB shadow.** A field that is logically structured but stored as text or JSONB without a schema. The `notes` column on `model_versions` is a JSONB-shadow text column per EE_CURRENT_STATE_DUMP § 4.1; this bible does not standardize that shape — it is documented as-is.
- **Canonical column.** A column whose meaning the code paths agree on without local re-derivation. `entries.race_id`, `wr_predictions.win_probability`, and `pl_predictions.predicted_ev` are canonical. `past_performances.race_id` is **not** canonical (NULL across all historical rows per data_loader.py docstring; joins use `(race_date, track_code, race_number)` instead).
- **Predictions-table family.** The four logically-similar tables that hold model outputs: legacy `predictions`, plus `wr_predictions`, `pl_predictions`, `ls_predictions`. Migration 005 (`005_three_prediction_tables.sql`) created the per-pipeline replacements; the legacy table was not dropped.
- **Migration runner.** `backend/database/migrations/migrate.py`. A single-file Python entry point that lexically sorts `*.sql` files in its own directory, applies each unapplied file in order, and records its filename in `schema_migrations`.
- **Duplicate-005 case.** The two migration files `005_backfill_pace_delta.sql` and `005_three_prediction_tables.sql` share the numeric prefix. Lexical sort orders them deterministically (`005_backfill_pace_delta.sql` before `005_three_prediction_tables.sql`); the runner treats them as opaque distinct filenames.
- **`schema_migrations` table.** The runner's own bookkeeping table. Created by `migrate.py` (not by a numbered migration). Holds `(migration_id SERIAL, filename UNIQUE NOT NULL, applied_at TIMESTAMPTZ)`. Not counted in the 14-table inventory because it is the runner's own state, not part of the EE schema.
- **W.N entry.** A "What Was Fixed — Do Not Revert" entry in this bible's § 8, formatted as `8.W.<n>` per BIBLE_STRUCTURE_SPEC v3 § 5.5.

## 3. Architecture overview

The database is the single Aurora Serverless PostgreSQL cluster owned by EE. It sits in a private VPC subnet (per META_PLAN v6 § 2.3 + § 7.12). Lambdas and ECS tasks reach it via the VPC; no public endpoint. Credentials are fetched from AWS Secrets Manager at process start (entry `equine-equalizer/db-credentials` per META_PLAN v6 § 2.3).

The runtime topology with respect to the database:

- **Writers.** Three Active inference Lambdas (`equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference`) write to `wr_predictions`, `pl_predictions`, and `ls_predictions` respectively. The results-fetch Lambda writes to `results`. The ingestion Lambda — currently INACTIVE per META_PLAN v6 § 2.3 — historically wrote to `tracks`, `horses`, `trainers`, `jockeys`, `races`, `entries`, `past_performances`, `workouts`. The legacy `equine-inference` Lambda (Active per META_PLAN v6 § 2.3) writes to the legacy `predictions` table. ECS retraining tasks write to `model_versions`.
- **Readers.** Routers in `backend/routers/` read via repository classes in `backend/repositories/`. Each repository wraps a single table or related table cluster. The repository → service → router → frontend layering is asymmetric in EE: routers in EE are thin Lambda handlers (`def get_*` / `def post_*`), not FastAPI dependency-injected route functions; the layer boundary discipline lives in API & Frontend Bible § 5.
- **Connection management.** psycopg2 connections are opened per-Lambda-invocation. No connection pooler is configured at audit time. RDS Data API is not used by EE Python code (verified — `migrate.py` opens psycopg2 directly via the connection string assembled from the secret).
- **Schema bootstrap path.** A fresh database is bootstrapped by running `migrate.py` against an empty cluster: migration 001 creates the 11 base tables; migrations 002–011 then evolve the schema to its current state. `schema.sql` is byte-identical to migration 001 at audit time and serves as a read-only snapshot, not a separate bootstrap path.

The database holds three logical groups of data:

- **Reference data** — `tracks`, `horses`, `trainers`, `jockeys`. Slowly-evolving identity rows.
- **Race-day artifacts** — `races`, `entries`, `past_performances`, `workouts`, `results`. Daily-write tables.
- **Model-output artifacts** — `model_versions`, `predictions`, `wr_predictions`, `pl_predictions`, `ls_predictions`. Daily-write per-inference-Lambda tables plus the model registry.

The `trainer_stats` materialized view is a derived rollup of `past_performances`, refreshed manually (`REFRESH MATERIALIZED VIEW trainer_stats`).

## 4. Canonical objects

Three Python dataclasses in `backend/models/canonical.py` cross the schema boundary as the typed shape of a prediction row. They map onto the per-pipeline prediction tables.

**Note (schema observation).** The Phase 1 spec for this bible references "WRPrediction, PLPrediction, LSPrediction dataclasses." The actual file `backend/models/canonical.py` defines `PLPrediction` (line 351), `LSPrediction` (line 390), and a `Prediction` class (line 428). There is no class named `WRPrediction`. The legacy `Prediction` dataclass is the dataclass currently used by WR-style predictions: it carries `win_probability`, `place_probability`, `show_probability`, plus the LS-enrichment fields (`longshot_prob`, `ensemble_win_prob`, `confidence`) that ride on `wr_predictions` rows. A grep for `class WRPrediction` returns hits only in repository files (`wr_prediction_repository.py:13` defines `class WRPredictionRepository`). This bible documents what exists; the dataclass naming inconsistency is surfaced for tracking, not silently renamed.

### 4.1 `Prediction` (legacy + WR-style superset)

Fields: `entry`, `race_id`, `horse_id`, `prediction_id`, `race_number`, `model_version_id`, `win_probability`, `place_probability`, `show_probability`, `predicted_rank`, `confidence_score`, `is_top_pick`, `is_value_flag`, `morning_line_implied_prob`, `overlay_pct`, `feature_importance` (dict), `recommended_bet_type`, `exotic_partners` (list), `actual_finish`, `was_win`, `was_place`, `was_show`, `exacta_hit`, `trifecta_hit`, `created_at`. Plus enrichment fields: `raw_win_prob`, `rank_score`, `edge_pct`, `kelly_fraction`, `kelly_bet`, `has_workout_data`, `model_used` (default `'core'`), `ensemble_win_prob`, `trajectory_score`, `longshot_prob`, `angle_name`, `angle_posterior`, `angle_ev`, `longshot_alert`, `confidence`. Plus Stream A2 dual-prediction fields: `handicapping_prob`, `market_prob`. Plus Stream E results-aware fields LEFT-JOINed from `results` at read time: `actual_finish_position`, `actual_win_payout`, `actual_place_payout`, `actual_show_payout`, `prediction_outcome`, `flat_bet_pl`.

Maps to the legacy `predictions` table (which it predates) and to `wr_predictions` (where the enrichment fields are persisted as columns).

### 4.2 `PLPrediction`

Fields: `entry`, `race_id`, `horse_id`, `prediction_id`, `race_number`, `model_version_id`, `win_probability`, `predicted_ev`, `confidence_score`, `predicted_rank`, `is_top_pick`, `closing_odds`, `implied_probability`, `edge_pct`, `is_value_bet`, `is_strong_value`, `kelly_fraction`, `kelly_bet_size`, `feature_importance` (dict), `actual_finish`, `was_win`, `bet_profit`, `created_at`. Plus Stream A2: `handicapping_prob`, `market_prob`. Plus Stream E LEFT-JOINed: `actual_finish_position`, `actual_win_payout`, `actual_place_payout`, `actual_show_payout`, `prediction_outcome`, `flat_bet_pl`, `track_code`, `track_name`.

Maps to `pl_predictions`.

### 4.3 `LSPrediction`

Fields: `entry`, `race_id`, `horse_id`, `prediction_id`, `model_version_id`, `final_win_probability`, `longshot_alert`, `confidence`, `kelly_fraction`, `predicted_rank`, `xgb_rank_score`, `rf_longshot_prob`, `lstm_trajectory`, `calibrated_win_prob`, `bayesian_angle_ev`, `angle_description`, `feature_importance` (dict), `actual_finish`, `was_win`, `actual_odds`, `bet_profit`, `created_at`. Plus race-context for the longshot card UI (Bug 3 fix): `race_date`, `race_number`, `track_code`, `post_time`. Plus Stream E LEFT-JOINed: `actual_finish_position`, `actual_win_payout`, `actual_place_payout`, `actual_show_payout`, `prediction_outcome`, `flat_bet_pl`.

Maps to `ls_predictions`.

### 4.4 Other canonical objects relevant to schema reads

`Track`, `Horse`, `Trainer`, `Jockey`, `Workout`, `PastPerformance`, `Entry`, `Race`, `RaceCard`, `Result`, `ModelVersion` — all in `canonical.py`, each mapping to its same-named table. `Entry` contains nested `Horse`, `Trainer`, `Jockey` and a list of `PastPerformance` loaded by repository. `Race` contains `Track` and a list of `Entry`. The bible's tables are documented in their primitive form; the dataclasses' nesting is a repository-time concern.

### 4.5 Per-table inventory

The 14 tables, in schema-source order:

1. **`tracks`** (8 cols, schema.sql:12–22). PK `track_id` UUID. Identity: `track_code` UNIQUE. Reference data; ~11 rows (QUALIFYING_TRACKS).
2. **`horses`** (14 cols including FK self-references, schema.sql:28–44). PK `horse_id` UUID. Self-referencing FKs to `sire_id`, `dam_id`, `dam_sire_id`. `registration_id` UNIQUE.
3. **`trainers`** (5 cols, schema.sql:50–56). PK `trainer_id` UUID.
4. **`jockeys`** (6 cols, schema.sql:62–69). PK `jockey_id` UUID. `is_apprentice` flag.
5. **`races`** (24 cols, schema.sql:75–103). PK `race_id` UUID. UNIQUE `(track_id, race_date, race_number)` and UNIQUE `equibase_race_id`. FK to `tracks`.
6. **`entries`** (26 cols, schema.sql:109–139). PK `entry_id` UUID. UNIQUE `(race_id, horse_id)`. FKs to `races`, `horses`, `trainers`, `jockeys`.
7. **`past_performances`** (91 cols, schema.sql:145–266). PK `pp_id` UUID. UNIQUE `(horse_id, race_date, track_code, race_number)`. FK to `horses`. **`race_id` column is nullable and NULL across all historical rows** (per data_loader.py docstring; joins use composite `(race_date, track_code, race_number)`).
8. **`workouts`** (13 cols, schema.sql:272–287). PK `workout_id` UUID. UNIQUE `(horse_id, workout_date, track_code, distance_furlongs)`. FK to `horses`.
9. **`results`** (25 cols, schema.sql:293–321). PK `result_id` UUID. UNIQUE `entry_id`. FKs to `entries`, `races`, `horses`. Holds payouts for win/place/show/exacta/trifecta/superfecta/daily_double.
10. **`predictions`** (legacy, 23 cols, schema.sql:327–353). PK `prediction_id` UUID. UNIQUE `entry_id`. FKs to `entries`, `races`, `horses`, `model_versions`. Superseded by migration 005's three per-pipeline tables; not dropped. **Documented as Deprecated in § 7.1.**
11. **`model_versions`** (17 cols at audit time, schema.sql:359–377 + migration 005's `model_type` + `flat_bet_roi` + `kelly_roi` + `value_bet_win_rate` columns). PK `model_version_id` UUID. JSONB columns: `feature_list`, `hyperparameters`. Active-model uniqueness enforced by partial unique index `idx_active_model_per_type` on `(model_type) WHERE is_active = true` (migration 005).
12. **`wr_predictions`** (created by migration 005, columns added later). PK `prediction_id` UUID with `gen_random_uuid()` default. UNIQUE `(race_id, entry_id, style)` (migration 011). FKs to `entries`, `races`, `horses`, `model_versions`. Indexes: `idx_wr_predictions_race`, `idx_wr_predictions_date`. JSONB: `feature_importance`. Array: `exotic_partners UUID[]`.
13. **`pl_predictions`** (created by migration 005). PK `prediction_id` UUID. UNIQUE `entry_id` per migration 005's CREATE TABLE; the live constraint at audit time is `UNIQUE(race_id, entry_id, style)` per the WR-aligned pattern (migration 011's preamble references this convention). FKs to `entries`, `races`, `horses`, `model_versions`. Indexes: `idx_pl_predictions_race`, `idx_pl_predictions_value` (partial: `WHERE is_value_bet = true`). JSONB: `feature_importance`.
14. **`ls_predictions`** (created by migration 005, promoted to first-class by migration 010). PK `prediction_id` UUID. UNIQUE `(race_id, entry_id, style)` (migration 010 replaced single-column UNIQUE with this). Migration 010 added `style`, `market_prob`, `edge_pct`, `is_top_pick`, `morning_line_implied_prob`. FKs to `entries`, `races`, `horses`, `model_versions`. Indexes: `idx_ls_predictions_race`, `idx_ls_predictions_alert` (partial: `WHERE longshot_alert = true`). JSONB: `feature_importance`.

**Materialized view.** `trainer_stats` (migration 008) — aggregates per-trainer career stats (total_starts, wins, win_rate, itm, itm_rate, layoff_win_rate, lasix_win_rate, claimed_win_rate) over `past_performances` with `HAVING COUNT(*) >= 5`. Unique index `idx_trainer_stats_name` on `trainer_name`. Refresh is manual.

### 4.6 Migration discipline

Per META_PLAN v6 § 7.12:

- **Numbering format.** Migrations 001–011 keep their existing `NNN_short_description.sql` form. From 012 onward the format becomes `NNN_YYYYMMDD_short_description.sql` where the date is the authoring date. The rename of 001–011 was explicitly waived; both formats coexist as opaque filenames to the runner.
- **The duplicate-005 case.** Two files share the prefix: `005_backfill_pace_delta.sql` (data backfill) and `005_three_prediction_tables.sql` (schema change). Lexical sort places `005_backfill_pace_delta.sql` first because `'b' < 't'`, so the runner applies them in that order deterministically. The data-backfill runs against pre-split schema; the schema split then runs after. The runner sees both as opaque distinct filenames in `schema_migrations`. The forward rule (no new duplicates) takes effect from migration 012.
- **Migration runner mechanism.** `backend/database/migrations/migrate.py` opens a psycopg2 connection (DATABASE_URL env or Secrets Manager `DB_SECRET_ARN`), ensures the `schema_migrations` table exists, computes the set of already-applied filenames from `SELECT filename FROM schema_migrations`, lexically sorts the migrations directory's `*.sql` files, applies each unapplied file inside a single cursor execute, and inserts the filename into `schema_migrations` on success. Failures roll back the transaction and exit non-zero. Seeds in `backend/database/seeds/` are optionally applied via `--seed`; only `tracks.sql` exists at audit time.
- **Rollback format.** Down-block lives in the same migration file, after the up SQL, in a clearly-delimited block. The runner does not auto-execute the down block — rollback is operator-driven. Existing migrations 001–011 do not contain down-blocks; the convention applies forward from 012 onward (per META_PLAN v6 § 7.12 illustrative example).
- **Migration testing.** Non-production database first. Local Postgres is the only available non-production target at audit time; no dev Aurora cluster exists. Aurora-specific behaviors (JSONB serialization quirks, IAM auth) cannot be caught pre-deploy. Phase 5 should add a dev Aurora cluster as a triage-queue item.

### 4.7 JSONB conventions

JSONB columns and their convention:

- **`predictions.feature_importance`** — `{feature_name: importance_score}`. Default unset (NULL).
- **`wr_predictions.feature_importance`** / **`pl_predictions.feature_importance`** / **`ls_predictions.feature_importance`** — same shape; default `'{}'` (migration 005 sets `DEFAULT '{}'`).
- **`model_versions.feature_list`** — list of feature-name strings or feature-name → metadata dict (depends on training-time encoder). Default unset.
- **`model_versions.hyperparameters`** — flat dict of hyperparameter name → value. Default unset.
- **`predictions.exotic_partners` / `wr_predictions.exotic_partners`** — PostgreSQL `UUID[]` array (NOT JSONB). Default `'{}'`.
- **`tracks.surfaces`** — `TEXT[]` (NOT JSONB). Default unset.

The bible does not standardize JSONB shape evolution. Adding a key is forward-compatible; renaming or removing requires a coordinated migration plus reader update.

## 5. Discipline rules

Forbidden Patterns and Common Mistakes scoped to the schema domain. Sub-section IDs are numeric per BIBLE_STRUCTURE_SPEC v3 § 5.5.

### 5.1 Forbidden Pattern: writing to the legacy `predictions` table from new code (locked 2026-05-04)

**Rule.** New inference code MUST NOT INSERT or UPDATE rows in the legacy `predictions` table. The per-pipeline tables (`wr_predictions`, `pl_predictions`, `ls_predictions`) are the canonical homes for new predictions. Reads from `predictions` are tolerated only from the existing legacy router paths until those readers migrate (per § 7.1).

**Rationale.** The legacy table's columns conflate WR + PL + LS shapes, which forces enrichment fields onto a single row that no single inference Lambda fully populates. Migration 005 split the table for a reason; writing back to the legacy form re-introduces the bug.

**FORBIDDEN:**

```python
repo = PredictionRepository(conn)
repo.insert_prediction(entry_id=eid, win_probability=p, ...)
```

**CORRECT:**

```python
repo = WRPredictionRepository(conn)
repo.insert_prediction(entry_id=eid, race_id=rid, style='general', ...)
```

Cross-reference: see § 7.1 (Deprecated entry).

### 5.2 Forbidden Pattern: joining `past_performances` by `race_id` (locked 2026-05-04)

**Rule.** Joins against `past_performances` MUST use the composite `(race_date, track_code, race_number)` key. The `pp.race_id` column is nullable and is NULL across all historical rows (per data_loader.py docstring); a `JOIN ... ON pp.race_id = r.race_id` silently drops every historical row.

**Rationale.** Migrations 006 and 007 explicitly note this — both use the composite-key join because `race_id` is 0% populated. A naive `race_id` join produces empty result sets that look like "no PPs for this horse" rather than a join error.

**FORBIDDEN:**

```sql
SELECT * FROM past_performances pp
JOIN races r ON r.race_id = pp.race_id
WHERE pp.horse_id = $1;
```

**CORRECT:**

```sql
SELECT * FROM past_performances pp
JOIN tracks tk ON tk.track_code = pp.track_code
JOIN races r ON r.track_id = tk.track_id
   AND r.race_date = pp.race_date
   AND r.race_number = pp.race_number
WHERE pp.horse_id = $1;
```

### 5.3 Forbidden Pattern: including dispatch-metadata flags in UNIQUE constraints (locked 2026-05-04)

**Rule.** UNIQUE constraints on prediction tables MUST be `(race_id, entry_id, style)`. They MUST NOT include `model_used` or other per-horse dispatch metadata.

**Rationale.** Migration 011's preamble documents the bug: `model_used` is a per-horse dispatch flag (which model variant ran), not a fact about the horse-in-the-race. Including it in the UNIQUE constraint allowed the same `(race_id, entry_id, style)` to accumulate `'core'` and `'full'` rows when workout data landed between inference runs. 157 races accumulated 427 duplicate rows before the fix. Downstream consumers (LS softmax, ComparePage Cartesian, track_record double-counting) read both variants without filtering. The `model_used` column stays as metadata; the UNIQUE key drops it.

**FORBIDDEN:**

```sql
ALTER TABLE wr_predictions
ADD CONSTRAINT wr_predictions_unique_per_entry_model_style
UNIQUE (race_id, entry_id, model_used, style);
```

**CORRECT:**

```sql
ALTER TABLE wr_predictions
ADD CONSTRAINT wr_predictions_unique_per_entry_style
UNIQUE (race_id, entry_id, style);
```

Cross-reference: see § 8.W.1.

### 5.4 Forbidden Pattern: positional column indexing on Aurora schema results without a header check (locked 2026-05-04)

**Rule.** Code that assumes a column position (e.g., `cols[3]`) without verifying the column header is forbidden in any path that ingests external data into EE tables. The HRN scraper's column-shift bug (Bug #28) is the canonical example: parser code at `hrn_scraper.py:802-804` used positional indexing and silently lost win + daily-double payouts when the upstream page added a column on 2026-04-30.

**Rationale.** Schema-shaped output that is *position-correct* but *header-wrong* propagates into the database without raising. Header-keyed parsing surfaces structure changes as parse failures rather than silent data loss.

**FORBIDDEN:**

```python
win = parse_payout(cells[2])
place = parse_payout(cells[3])
```

**CORRECT:**

```python
header_idx = {h.text.strip(): i for i, h in enumerate(headers)}
win = parse_payout(cells[header_idx['Win']])
place = parse_payout(cells[header_idx['Place']])
```

Cross-reference: data_pipeline_bible:8.W.<n> (canonical home; the discipline lives in the data-pipeline bible because the scraper is the recurrence-prevention layer; this bible cross-references because the schema is what gets corrupted).

### 5.5 Common Mistake: assuming `schema.sql` and migration 001 can drift (locked 2026-05-04)

**Wrong instinct.** "I edited `schema.sql` to add a column; the column is now in the schema."

**Corrected position.** NO. `schema.sql` is a read-only snapshot of post-001 ground state. It is byte-identical to migration 001 at audit time. Editing it in isolation has no effect on any deployed database — only the migration runner applies state. Add new columns via a numbered migration. The bootstrap path runs migrations, not `schema.sql`.

### 5.6 Common Mistake: assuming the duplicate-005 case is a bug to fix (locked 2026-05-04)

**Wrong instinct.** "Two files share number 005; I'll renumber one of them."

**Corrected position.** NO. The duplicate-005 case is grandfathered per META_PLAN v6 § 7.12. Renaming a migration filename changes the key the runner uses to track applied state — `schema_migrations` rows reference the old filename, the renamed file looks unapplied, the runner re-applies it. Both files persist with their original names; the forward rule (no new duplicates) takes effect from migration 012 onward. Triage-queue ratio for "unify the format" is in `PHASE_5_BACKLOG.md`.

### 5.7 Common Mistake: counting `schema_migrations` as one of EE's tables (locked 2026-05-04)

**Wrong instinct.** "EE has 15 tables: the 14 plus `schema_migrations`."

**Corrected position.** NO. `schema_migrations` is the migration runner's own bookkeeping table. It is created by `migrate.py` (function `ensure_migrations_table`), not by any numbered migration, and holds runner state — not EE schema. The 14-table count excludes it. EE_CURRENT_STATE_DUMP § 4.1 lists 15 rows in its tables table because the dump separately enumerates all per-pipeline prediction tables — 11 base + 3 per-pipeline = 14 — but the dump's "15 tables + 1 materialized view" footer count is incorrect. Verified by `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql | sort -u` returning 14 unique names (verification log Claim N3).

## 6. Currently Open

One-line bug list with `PHASE_5_BACKLOG.md` pointers. The triage queue authoritative format lives at TRIAGE_QUEUE_SPEC v1.

- **Bug #28** (HIGH): HRN scraper column-shift since 2026-04-30 corrupts `results.win_payout`, `results.daily_double_payout`, place/show alignment. Canonical home is `data_pipeline_bible:6` (the recurrence prevention is in scraper discipline). Backfill needed after fix. Pointer: `PHASE_5_BACKLOG.md` Phase 5.3.1 per META_PLAN v6 Appendix A.5.
- **Schema-vs-migration drift on `wr_predictions` / `pl_predictions` `style` and `model_used` columns** (UNRESOLVED, surfaced during this drafting): migration 011 references `wr_predictions_unique_per_entry_model_style` constraint and the `style` and `model_used` columns as if they exist, but no committed migration in `001–011` adds them to `wr_predictions`. The columns must have been added by an out-of-band path. Investigation needed: either the columns exist in the live cluster but not in any tracked migration (drift), or migration 011 fails on a fresh bootstrap. Pointer: `PHASE_5_BACKLOG.md` (new entry; verification log Claim N5).
- **No dev Aurora cluster** (MODERATE): per META_PLAN v6 § 7.12, migration testing falls back to local Postgres. Aurora-specific behaviors (JSONB serialization quirks, IAM auth) cannot be caught pre-deploy. Pointer: `PHASE_5_BACKLOG.md` (Phase 5 working agreements decision).
- **`pl_predictions` UNIQUE constraint may not match WR/LS pattern** (LOW, needs verification): migration 005 set `UNIQUE(entry_id)`; migration 011's preamble references the WR-aligned `(race_id, entry_id, style)` pattern as if PL already follows it. Live constraint state needs verification. Pointer: `PHASE_5_BACKLOG.md` (new entry).

## 7. Deprecated

Cross-references to `PHASE_5_BACKLOG.md` entries per META_PLAN v6 § 7.7 + Appendix A.4. This bible is the canonical home for the legacy `predictions` table deprecated entry per BIBLE_STRUCTURE_SPEC v3 § 6.6.

### 7.1 Legacy `predictions` table — superseded but still read

| Field/Module | Canonical Source | Notes |
|---|---|---|
| `predictions` table | `wr_predictions` (per-style WR), `pl_predictions` (P&L), `ls_predictions` (LS); created by migration 005 (`005_three_prediction_tables.sql`) | The legacy `predictions` table was created by `001_initial_schema.sql:327` (verified). Migration 005 created the per-pipeline replacements (verified: zero `DROP TABLE` statements in any migration 001–011). The legacy table currently holds approximately 6,600 rows per dashboard `counts.predictions` at META_PLAN v6 lock (inherited verification claim — Claim 16 in META_PLAN v6 verification log). It still has active readers: `prediction_router.py` (1 import on line 6, plus 3 instantiations of `PredictionRepository` on lines 34, 61, 92 = 4 references total — verified live during this drafting); `race_router.py` (1 import on line 273, plus 1 instantiation on line 277 = 2 references total — verified live during this drafting); `dashboard_router.py` (direct SELECT references per inherited claim, line numbers not re-verified during this drafting); `horse_router.py` (direct SELECT references per inherited claim, line numbers not re-verified during this drafting). Planned removal: Phase 5.X.Y after readers are migrated to the per-pipeline tables. Until removal, new code MUST NOT write to the legacy table per § 5.1; reads are tolerated only from the listed legacy router paths. |

Pointer: `PHASE_5_BACKLOG.md` Phase 5.X.Y (specific phase number to be assigned).

## 8. What Was Fixed — Do Not Revert

Institutional immune memory entries scoped to schema. Numbered W.N per BIBLE_STRUCTURE_SPEC v3 § 5.5.

### 8.W.1 wr_predictions UNIQUE-constraint duplicates (fixed 2026-05-01)

**Symptom.** 157 races accumulated 427 duplicate rows in `wr_predictions`. Downstream consumers (LS softmax, ComparePage Cartesian display, track_record double-counting) read both `'core'` and `'full'` variants without filtering.

**Root cause.** The UNIQUE constraint on `wr_predictions` was `(race_id, entry_id, model_used, style)`. The `model_used` column is a per-horse dispatch flag (which model variant ran for this horse, based on workout availability), not a fact about the horse-in-the-race. When workout data landed between inference runs, the new variant didn't conflict with the old key, so both persisted.

**Fix.** Migration `011_wr_predictions_unique_fix.sql` (2026-05-01) ran cleanup + constraint swap as a single transaction: deleted older duplicates per `(race_id, entry_id, style)` keeping the most recent, then dropped the old UNIQUE and added `wr_predictions_unique_per_entry_style` UNIQUE `(race_id, entry_id, style)`. Pre-state and post-state DO blocks raise on cleanup failure or constraint-installation failure.

**Why this entry exists.** The discipline persists as Forbidden Pattern § 5.3: dispatch-metadata flags do not belong in UNIQUE constraints. Discriminators on UNIQUE keys must be facts about the row's identity, not facts about the path that produced the row.

**Conditional triggers evaluated:**
- if-fix-involved-migration: FIRES. Linked to `backend/database/migrations/011_wr_predictions_unique_fix.sql`.
- if-fix-invalidated-prior-content: DOES NOT FIRE. No prior bible content existed at fix time (pre-Phase-1).
- if-fix-produced-Forbidden-Pattern: FIRES. Cross-reference to `database_schema_bible:5.3`.
- if-fix-touches-multiple-bibles: DOES NOT FIRE. Schema-bible-local; downstream consumers (LS softmax, ComparePage Cartesian) reference this entry but the canonical home is here.

### 8.W.2 ls_predictions promoted to first-class (fixed 2026-05-01)

**Symptom.** `ls_predictions` was a stub table since migration 005. Its `insert_prediction` repo method was never called. LS data was being written as enrichment columns on `wr_predictions` (`longshot_alert`, `longshot_prob`, `ensemble_win_prob`, `confidence`).

**Root cause.** Original architecture treated LS as a wr_predictions enrichment, not a separate model with its own ranking. Tony's revised architecture (2026-05-01) flipped this: LS gets first-class predictions with its own UNIQUE constraint and own ranking.

**Fix.** Migration `010_ls_predictions_first_class.sql` (2026-05-01) added the columns missing for parity (`style` default `'general'`, `market_prob`, `edge_pct`, `is_top_pick`, `morning_line_implied_prob`); dropped the old single-column `UNIQUE(entry_id)` and replaced it with `UNIQUE(race_id, entry_id, style)` to match the WR / PL pattern. Existing rows: 0 (verified empty in migration's preamble), so the constraint switch was safe. Transition policy: LS continues to write the wr_predictions enrichment columns so frontend reads keep working until the read-side cuts over.

**Why this entry exists.** First-class status of a derived/enrichment table is a deliberate architectural escalation. The discipline persists as: the per-pipeline UNIQUE pattern is `(race_id, entry_id, style)` across all three tables (WR, PL, LS); deviations from that pattern are evidence of an architectural mismatch, not a model-shape choice. The transition-policy lesson — "keep the old shape working during the cutover" — also persists as guidance for future first-class promotions.

**Conditional triggers evaluated:**
- if-fix-involved-migration: FIRES. Linked to `backend/database/migrations/010_ls_predictions_first_class.sql`.
- if-fix-invalidated-prior-content: DOES NOT FIRE.
- if-fix-produced-Forbidden-Pattern: FIRES. Cross-reference to `database_schema_bible:5.3` (per-pipeline UNIQUE pattern is enforced as a Forbidden Pattern; W.2 reinforces it).
- if-fix-touches-multiple-bibles: FIRES (advisory). The LS service's read-time enrichment-column dual-write is referenced from `ml_layer_architecture_bible:8` by ID; canonical home is here because the schema constraint is the recurrence-prevention layer.

### 8.W.3 `past_performances.race_id` non-population accepted as design (locked 2026-05-04, not a bug fix)

**Symptom.** `past_performances.race_id` is NULL across all historical rows. Naive `JOIN ... ON pp.race_id = r.race_id` joins return empty.

**Root cause.** Historical PP data is loaded from upstream provider (Equibase chart data) keyed by `(race_date, track_code, race_number)` — the upstream provider does not emit a stable `race_id` for historical races, and EE's race UUIDs are minted per-row at ingestion of the *current* race card, not retroactively for historical context. The data_loader.py docstring documents this explicitly.

**Fix.** Not a fix in the bug-fix sense — the design is intentional. The discipline that persists is: PP joins use the composite key, full stop. Migrations 006 and 007 both follow this discipline (`r.race_date = pp.race_date AND tk.track_code = pp.track_code AND r.race_number = pp.race_number`). Migration 006's comment makes the rationale explicit: "Joined via (race_date, track_code, race_number) because race_id is not populated in past_performances (0%)."

**Why this entry exists.** Without this entry, a future schema change (e.g., backfilling `past_performances.race_id` from a sibling table) would be tempting but would partially-populate the column, creating a foot-gun: some PP rows joinable by `race_id`, most not. Either fully backfill (with verification) or do not backfill at all. The Forbidden Pattern at § 5.2 is the operative recurrence-prevention rule.

**Conditional triggers evaluated:**
- if-fix-involved-migration: DOES NOT FIRE (no fix migration; this entry codifies an existing design discipline).
- if-fix-invalidated-prior-content: DOES NOT FIRE.
- if-fix-produced-Forbidden-Pattern: FIRES. Cross-reference to `database_schema_bible:5.2`.
- if-fix-touches-multiple-bibles: FIRES (advisory). Feature Provenance Bible § 4 references this discipline because all PP-derived features traverse the composite-key join; canonical home is here because the schema column is the artifact.

---

**End of Database & Schema Bible (convergence test instance — run2).**
