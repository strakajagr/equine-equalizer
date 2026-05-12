# Database & Schema Bible

**Document:** database_schema_bible.md
**Phase:** 1 (Bible)
**Status:** DRAFT v1 (convergence-test instance — operating-model run1)
**Author:** CC (drafting under verification discipline; QB orchestrated)
**Date:** 2026-05-04
**Locked:** [pending — convergence test, not real Phase 1 lock]

**Revision history:**
- v1 (2026-05-04): convergence test instance run1 per META_PLAN v6 § 5.3 step 2.

**Tier:** 3 per META_PLAN v6 § 4.1 + § 6.5.

**Anchored on:** META_PLAN v6 + BIBLE_STRUCTURE_SPEC v3.

**Companion verification log:** `_convergence_test/database_schema_bible_run1_verification.md`.

---

## 1. Scope of this bible

This bible documents the database surface area of Equine Equalizer (EE):

- The 14 tables defined across `backend/database/schema/schema.sql` and migrations 001–011.
- The single materialized view `trainer_stats` defined in migration 008.
- The migration runner mechanism (`backend/database/migrations/migrate.py`) and the `schema_migrations` tracking table the runner creates at first invocation.
- JSONB conventions as they appear in the schema (currently localized to `model_versions.feature_list`, `model_versions.hyperparameters`, and the `feature_importance` columns on the four predictions tables).
- The predictions-table family: the legacy `predictions` table created in 001 and the per-pipeline replacements `wr_predictions` / `pl_predictions` / `ls_predictions` created in migration 005.
- Migration discipline (numbering format, the duplicate-005 case, rollback format, testing requirement).

What this bible does **not** cover (covered elsewhere):

- Lambda-handler-as-router and route inventory → `api_frontend_bible.md`.
- Daily ingestion / results-fetch / chart parser flows that write these tables → `data_pipeline_bible.md`.
- The model registry's multi-active-row reality (88 = 45 active + 43 inactive) and per-style dispatch on top of `model_versions` → `ml_layer_architecture_bible.md`. This bible documents the table; that bible documents the registry semantics.
- Feature-engineering source columns and the train/inference duplication structural reality → `feature_provenance_bible.md`.
- Aurora cluster topology beyond what the schema dictates (VPC, Secrets Manager wiring, RDS Data API vs psycopg2 paths) → `architecture_overview.md`.

Anchor cross-reference: META_PLAN v6 § 3.2 working hypothesis #6, which scopes this document to the "14 tables + materialized view, migration discipline, JSONB conventions where present, and the predictions-table family."

---

## 2. Definitions

Terminology specific to the schema/migration domain:

- **Table** — a `CREATE TABLE` statement that has been applied via `backend/database/migrations/migrate.py`. A `CREATE TABLE` in `schema.sql` that has not been applied via the runner is bootstrap-only.
- **Materialized view** — a stored result-set materialization. `trainer_stats` is the only materialized view in the schema. Refresh is manual, not automatic; `REFRESH MATERIALIZED VIEW trainer_stats` must be issued by the operator after large data loads.
- **Migration** — a numbered SQL file under `backend/database/migrations/*.sql`. Naming for 001–011 is `NNN_short_description.sql` (grandfathered per META_PLAN v6 § 7.12). Naming from 012 onward is `NNN_YYYYMMDD_short_description.sql`.
- **Migration runner** — the Python script `backend/database/migrations/migrate.py` that iterates SQL files in lexical order, applies any not yet recorded in `schema_migrations`, and records the filename on success.
- **Tracking table** — `schema_migrations`, created at first invocation of the runner with the schema `(migration_id SERIAL PRIMARY KEY, filename VARCHAR(255) UNIQUE NOT NULL, applied_at TIMESTAMPTZ DEFAULT NOW())`.
- **Bootstrap script** — `backend/database/schema/schema.sql`. A from-scratch installation of the post-001 schema. NOT applied by the runner. It exists as a single-shot reference; the runner's `001_initial_schema.sql` is the authoritative bootstrap path.
- **JSONB column** — a PostgreSQL JSONB column. EE has six in the schema as of 011: `model_versions.feature_list`, `model_versions.hyperparameters`, and `feature_importance` on each of `predictions`, `wr_predictions`, `pl_predictions`, `ls_predictions`.
- **Predictions-table family** — the four tables currently storing prediction rows: the legacy `predictions` table from 001 plus the three per-pipeline tables (`wr_predictions`, `pl_predictions`, `ls_predictions`) from migration 005, with subsequent shape changes in migrations 010 and 011.
- **Per-pipeline predictions table** — one of `wr_predictions` / `pl_predictions` / `ls_predictions`. Each is written by exactly one inference Lambda's repository class.
- **Canonical UNIQUE pattern** (post-011) — `UNIQUE (race_id, entry_id, style)` on the per-pipeline predictions tables. `wr_predictions` and `ls_predictions` arrived at this shape in 011 and 010 respectively. `pl_predictions` retains `UNIQUE(entry_id)`.

---

## 3. Architecture overview

### 3.1 The database in EE's runtime topology

The EE database is a single Aurora Serverless v1 PostgreSQL cluster owned by the `DatabaseStack` CDK stack (per `EE_CURRENT_STATE_DUMP.md` § 13). Cluster ARN: `arn:aws:rds:us-east-1:584812014683:cluster:equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`. Database name: `equine_equalizer`.

The cluster lives in the EE VPC's private subnets. Connectivity into the cluster is via:
1. **psycopg2 over the standard Postgres protocol** — used by `migrate.py` and by Lambda functions that connect through the VPC. Credentials come from `equine-equalizer/db-credentials` in Secrets Manager, fetched per `migrate.py`'s `get_connection_string()` (which falls back to `DATABASE_URL` if set).
2. **RDS Data API** — used by Lambda paths that don't open VPC connections (verification deferred to `architecture_overview.md`; this bible names the existence of two paths but does not enumerate which Lambda uses which).

The schema is installed and evolved by the migration runner exclusively. There is no ORM-managed migration system (no Alembic, no Prisma, no SQLAlchemy migrations). The runner is intentionally minimal: read SQL files, sort lexically, execute pending ones in order, record filenames in `schema_migrations`.

### 3.2 The 14 tables (decomposed list)

The 14-table count is verified by counting unique `CREATE TABLE` statements across `schema.sql` and migrations 001–011 (per META_PLAN v6 Claim 4, inherited; re-verified in this draft's verification log):

11 tables created by `001_initial_schema.sql` (which mirrors `schema.sql` line-for-line):

1. `tracks`
2. `horses`
3. `trainers`
4. `jockeys`
5. `races`
6. `entries`
7. `past_performances`
8. `workouts`
9. `results`
10. `predictions`
11. `model_versions`

3 tables created by `005_three_prediction_tables.sql`:

12. `wr_predictions`
13. `pl_predictions`
14. `ls_predictions`

Subtotal: 11 + 3 = 14 tables.

Plus 1 materialized view created by `008_create_trainer_stats.sql`:

- `trainer_stats`

Plus 1 runtime-created tracking table (created by the runner, not by a migration file): `schema_migrations`. This table is real but is not part of the 14-table count because it is not declared in any migration file — it is created on first runner invocation. It is documented in § 4.2.3.

### 3.3 The materialized view: `trainer_stats`

A single materialized view exists. Defined in migration 008. Aggregates career career-level stats (total_starts, win_rate, itm, itm_rate, layoff_win_rate, lasix_win_rate, claimed_win_rate) per `trainer_name` from `past_performances`, with `HAVING COUNT(*) >= 5` (minimum 5 starts to appear). Refresh is manual.

### 3.4 The predictions-table family

EE has four tables that store predictions. The legacy table came first; the per-pipeline split was layered on without dropping the legacy table.

| Table | Created by | Population state | Status |
|---|---|---|---|
| `predictions` | 001 | ~6,600 rows (per META_PLAN v6 Claim 16, inherited) | Legacy — superseded but still read. See § 7.1. |
| `wr_predictions` | 005 | populated daily by WR inference | Active. UNIQUE shape changed in 011. |
| `pl_predictions` | 005 | populated daily by PL inference | Active. |
| `ls_predictions` | 005 | populated since Phase A3 (~May 2026) | Active. UNIQUE shape changed in 010 (first-class promotion). |

This is the structural reality META_PLAN v6 § 3.2 working hypothesis #6 anchors: per-pipeline tables exist without the legacy table being dropped, and each per-pipeline table is owned by exactly one inference Lambda.

### 3.5 JSONB conventions where present

JSONB columns in the schema (six total):

- `model_versions.feature_list` — the list of features used by the model. Default empty.
- `model_versions.hyperparameters` — the model's training hyperparameters. Default empty.
- `predictions.feature_importance` — per-prediction feature importances. JSONB (no default).
- `wr_predictions.feature_importance` — `DEFAULT '{}'` per migration 005.
- `pl_predictions.feature_importance` — `DEFAULT '{}'` per migration 005.
- `ls_predictions.feature_importance` — `DEFAULT '{}'` per migration 005.

Two conventions apply:

1. **JSONB columns default to `'{}'` (empty object) on the predictions tables** so reads do not encounter NULL when feature importance was not produced. The legacy `predictions.feature_importance` does not have this default — JSONB NULLs are possible there.
2. **Per-prediction shape is opaque to the schema.** The schema does not encode keys; the keys are determined by the model that wrote the row. Repos serialize and deserialize at the boundary; the bible does not enumerate the key set per model (that lives in `feature_provenance_bible.md` § 4 if needed).

No JSONB shadow patterns (a JSONB blob whose keys mirror columns elsewhere) exist in the EE schema as of 011.

---

## 4. Schema and migration detail

### 4.1 Per-table documentation

Each subsection documents one table: column list with types, primary key, purpose, primary writers, primary readers, UNIQUE constraints, and FK constraints. Approximate row counts are cited from the live dashboard endpoint (`gb5qlfy10h.execute-api.us-east-1.amazonaws.com/dashboard/metrics`) where META_PLAN's verification log carried the inheritance.

#### 4.1.1 `tracks`

- **Source:** schema.sql / `001_initial_schema.sql`
- **Columns:** `track_id UUID PK`, `track_code VARCHAR(10) UNIQUE NOT NULL`, `track_name VARCHAR(100) NOT NULL`, `location VARCHAR(100)`, `timezone VARCHAR(50) DEFAULT 'America/New_York'`, `surfaces TEXT[]`, `is_qualifying BOOLEAN DEFAULT false`, `min_claiming_price INTEGER`, `created_at TIMESTAMPTZ DEFAULT NOW()`.
- **Purpose:** track metadata (code, name, surfaces array, MIN_CLAIMING_PRICE for qualifying-track gating).
- **UNIQUE:** `track_code`.
- **FKs in:** `races.track_id` references this table.
- **Writers:** seeded from `backend/database/seeds/tracks.sql`; ingestion path may upsert.
- **Readers:** `data_pipeline_bible.md` flow-level docs; cross-referenced by repositories that resolve `track_code` ↔ `track_id`.

#### 4.1.2 `horses`

- **Source:** schema.sql / 001
- **Columns:** `horse_id UUID PK`, `registration_id VARCHAR(50) UNIQUE`, `horse_name VARCHAR(100) NOT NULL`, sire/dam/dam_sire as `VARCHAR(100)` plus self-referential `UUID REFERENCES horses(horse_id)` for `sire_id` / `dam_id` / `dam_sire_id`, `foaling_date DATE`, `country_of_origin VARCHAR(10) DEFAULT 'USA'`, `sex VARCHAR(10)`, `color VARCHAR(50)`, `created_at` / `updated_at` TIMESTAMPTZ.
- **Purpose:** horse identity and pedigree.
- **UNIQUE:** `registration_id`.
- **FKs in:** `entries.horse_id`, `past_performances.horse_id`, `workouts.horse_id`, `results.horse_id`, `predictions.horse_id`, `wr_predictions.horse_id`, `pl_predictions.horse_id`, `ls_predictions.horse_id`. Self-FK on sire/dam/dam_sire for pedigree linkage.
- **Writers:** ingestion path (HRN scraper).
- **Readers:** all repositories that load entries with horse data; feature-engineering paths.

#### 4.1.3 `trainers`

- **Source:** schema.sql / 001
- **Columns:** `trainer_id UUID PK`, `trainer_name VARCHAR(100) NOT NULL`, `license_number VARCHAR(50)`, `country VARCHAR(10) DEFAULT 'USA'`, `created_at TIMESTAMPTZ`.
- **Purpose:** trainer roster.
- **FKs in:** `entries.trainer_id`.
- **Writers:** ingestion path.
- **Readers:** entries-load repositories; trainer-feature-engineering path.

#### 4.1.4 `jockeys`

- **Source:** schema.sql / 001
- **Columns:** `jockey_id UUID PK`, `jockey_name VARCHAR(100) NOT NULL`, `license_number VARCHAR(50)`, `country VARCHAR(10) DEFAULT 'USA'`, `is_apprentice BOOLEAN DEFAULT false`, `created_at TIMESTAMPTZ`.
- **Purpose:** jockey roster.
- **FKs in:** `entries.jockey_id` (nullable; some races have an unsettled jockey at entry time).
- **Writers:** ingestion path.
- **Readers:** entries-load repositories.

#### 4.1.5 `races`

- **Source:** schema.sql / 001 (with VARCHAR widening in 002 + 003)
- **Columns:** `race_id UUID PK`, `track_id UUID NOT NULL REFERENCES tracks(track_id)`, `race_date DATE NOT NULL`, `race_number INTEGER NOT NULL`, `post_time TIMESTAMPTZ`, `distance_furlongs DECIMAL(4,1) NOT NULL`, `surface VARCHAR(50)` (widened in 003), `race_type VARCHAR(50)` (widened in 002, re-asserted in 003), `grade INTEGER`, `race_name VARCHAR(200)`, `purse INTEGER`, `claiming_price INTEGER`, `conditions TEXT`, `field_size INTEGER`, `rail_position DECIMAL(4,1)`, `track_condition VARCHAR(50)`, `moisture_level VARCHAR(50)`, `track_variant INTEGER`, `going_stick_reading DECIMAL(4,2)`, `temperature INTEGER`, `weather_conditions VARCHAR(100)`, `wind_speed INTEGER`, `wind_direction VARCHAR(20)`, `off_turf BOOLEAN DEFAULT false`, `equibase_race_id VARCHAR(100) UNIQUE`, `created_at TIMESTAMPTZ`.
- **Purpose:** race card metadata.
- **UNIQUE:** `(track_id, race_date, race_number)` and `equibase_race_id`.
- **FKs in:** `entries.race_id`, `past_performances.race_id` (NULLable; populated only for current-card rows), `results.race_id`, `predictions.race_id`, `wr_predictions.race_id`, `pl_predictions.race_id`, `ls_predictions.race_id`.
- **Writers:** ingestion path; chart-parser path.
- **Readers:** every repository.
- **Approximate rows:** ~2,611 visible via API for a 100-day window per dump § 4.1 (inherited).

#### 4.1.6 `entries`

- **Source:** schema.sql / 001 (with `program_number` widened in 003)
- **Columns:** `entry_id UUID PK`, `race_id UUID NOT NULL REFERENCES races(race_id)`, `horse_id UUID NOT NULL REFERENCES horses(horse_id)`, `trainer_id UUID NOT NULL REFERENCES trainers(trainer_id)`, `jockey_id UUID REFERENCES jockeys(jockey_id)`, `post_position INTEGER NOT NULL`, `program_number VARCHAR(10)`, `morning_line_odds DECIMAL(8,2)`, `weight_carried INTEGER`, `allowance_weight INTEGER DEFAULT 0`, `apprentice_allowance INTEGER DEFAULT 0`, plus 12 BOOLEAN flags for medication/equipment (`lasix`, `lasix_first_time`, `bute`, `blinkers_on`, `blinkers_off`, `blinkers_first_time`, `tongue_tie`, `bar_shoes`, `front_bandages`, `mud_caulks`, `equipment_change_from_last`, `medication_change_from_last`), `is_scratched BOOLEAN`, `scratch_reason VARCHAR(200)`, `is_entry BOOLEAN`, `created_at` / `updated_at`.
- **Purpose:** per-horse-per-race entry record.
- **UNIQUE:** `(race_id, horse_id)`.
- **FKs in:** `results.entry_id`, `predictions.entry_id`, `wr_predictions.entry_id`, `pl_predictions.entry_id`, `ls_predictions.entry_id`.
- **Approximate rows:** ~30K per dump § 4.1 (inherited).

#### 4.1.7 `past_performances`

- **Source:** schema.sql / 001 (multiple VARCHAR widenings in 003; backfills in 004, 005-pace-delta, 006, 007, 009)
- **Columns:** 91 columns covering race identification, conditions, connections, medication/equipment, post-and-finish, speed figures, leader fractional times, this-horse fractional times, running positions at each call, pace (early/late/delta/scenario/style/pressure), race context, and free-text comments. `pp_id UUID PK`, `horse_id UUID NOT NULL REFERENCES horses(horse_id)`, `race_id UUID REFERENCES races(race_id)`. Notable: `race_id` is NULL for the vast majority of historical rows (per dump § 4.1's docstring reference).
- **Purpose:** per-horse historical race detail. Largest table by column count.
- **UNIQUE:** `(horse_id, race_date, track_code, race_number)`.
- **FKs in:** none directly. Its `race_id` FK is the only outgoing reference.
- **Writers:** ingestion path; backfill migrations populate computed columns.
- **Readers:** training-side `model/shared/data_loader.py`; inference-side `backend/services/feature_engineering_service.py`; trainer_stats matview; the `_get_trainer_stats` service.
- **Approximate rows:** ~250K+ per dump (inherited; not independently verified).

#### 4.1.8 `workouts`

- **Source:** schema.sql / 001 (VARCHAR widenings in 003)
- **Columns:** `workout_id UUID PK`, `horse_id UUID NOT NULL REFERENCES horses(horse_id)`, `workout_date DATE NOT NULL`, `track_code VARCHAR(10) NOT NULL`, `distance_furlongs DECIMAL(4,1) NOT NULL`, `workout_time DECIMAL(6,2) NOT NULL`, `is_bullet BOOLEAN`, `track_condition VARCHAR(50)`, `workout_type VARCHAR(50)`, `rank_on_day INTEGER`, `total_works_on_day INTEGER`, `exercise_rider VARCHAR(100)`, `created_at TIMESTAMPTZ`.
- **Purpose:** workout history.
- **UNIQUE:** `(horse_id, workout_date, track_code, distance_furlongs)`.
- **Writers:** NYRA workout scrape path → S3 → `equine-ingestion` action `load_workouts_from_s3`.
- **Readers:** workout-aware feature engineering; the `model_used` dispatch logic (workout availability triggers the `full` variant per migration 011 commentary).
- **Approximate rows:** 143K+ per dump (inherited).

#### 4.1.9 `results`

- **Source:** schema.sql / 001
- **Columns:** `result_id UUID PK`, `entry_id UUID NOT NULL REFERENCES entries(entry_id)`, `race_id UUID NOT NULL REFERENCES races(race_id)`, `horse_id UUID NOT NULL REFERENCES horses(horse_id)`, `finish_position INTEGER NOT NULL`, `official_finish INTEGER NOT NULL`, `is_disqualified BOOLEAN`, `dq_from INTEGER`, `dq_to INTEGER`, `lengths_behind DECIMAL(5,2)`, `final_time DECIMAL(6,2)`, `beyer_speed_figure INTEGER`, call/stretch positions and lengths, payouts (`win_payout`, `place_payout`, `show_payout`, `exacta_payout`, `trifecta_payout`, `superfecta_payout`, `daily_double_payout`), `created_at`.
- **Purpose:** per-entry race outcome with payouts.
- **UNIQUE:** `entry_id` (one result row per entry).
- **Writers:** results-fetch flow (HRN); chart-parser path.
- **Readers:** `EvaluationService.record_results`; predictions-results join paths in router code; Stream E results-aware fields LEFT-JOIN this table at read time per `canonical.py`'s LSPrediction/PLPrediction/Prediction comments.
- **Bug context:** Bug #28 (HRN scraper off-by-one column shift) NULLs `win_payout` and `daily_double_payout` for results since 2026-04-30 — handled in `data_pipeline_bible.md`'s What Was Fixed section once fixed.

#### 4.1.10 `predictions` (legacy)

- **Source:** schema.sql / 001; FK to `model_versions` added in same migration via `ALTER TABLE predictions ADD CONSTRAINT fk_model_version`.
- **Columns:** `prediction_id UUID PK`, `entry_id UUID NOT NULL REFERENCES entries(entry_id)`, `race_id UUID NOT NULL REFERENCES races(race_id)`, `horse_id UUID NOT NULL REFERENCES horses(horse_id)`, `model_version_id UUID REFERENCES model_versions(model_version_id)`, `win_probability DECIMAL(6,4)`, `place_probability DECIMAL(6,4)`, `show_probability DECIMAL(6,4)`, `predicted_rank INTEGER`, `confidence_score DECIMAL(6,4)`, `is_top_pick BOOLEAN`, `is_value_flag BOOLEAN`, `morning_line_implied_prob DECIMAL(6,4)`, `overlay_pct DECIMAL(6,4)`, `feature_importance JSONB`, `recommended_bet_type VARCHAR(50)`, `exotic_partners UUID[]`, `actual_finish INTEGER`, `was_win` / `was_place` / `was_show` BOOLEAN, `exacta_hit` / `trifecta_hit` BOOLEAN, `created_at`.
- **Purpose:** original single-table predictions; superseded by the per-pipeline split in 005.
- **UNIQUE:** `entry_id`.
- **Status:** **Deprecated.** See § 7.1 for the full deprecation entry.
- **Approximate rows:** 6,600 (per META_PLAN v6 Claim 16, inherited).

#### 4.1.11 `model_versions`

- **Source:** schema.sql / 001; `model_type` column + ROI columns added in 005.
- **Columns:** `model_version_id UUID PK`, `version_name VARCHAR(50) NOT NULL`, `training_date TIMESTAMPTZ NOT NULL`, `training_data_start DATE NOT NULL`, `training_data_end DATE NOT NULL`, `training_race_count INTEGER`, `exacta_hit_rate DECIMAL(6,4)`, `trifecta_hit_rate DECIMAL(6,4)`, `top1_accuracy DECIMAL(6,4)`, `top3_accuracy DECIMAL(6,4)`, `calibration_score DECIMAL(6,4)`, `feature_list JSONB`, `hyperparameters JSONB`, `s3_artifact_path VARCHAR(500)`, `is_active BOOLEAN DEFAULT false`, `notes TEXT`, `created_at TIMESTAMPTZ`. Added by 005: `model_type VARCHAR(10) DEFAULT 'wr' CHECK (model_type IN ('wr', 'pl', 'ls'))`, `flat_bet_roi DECIMAL(8,4)`, `kelly_roi DECIMAL(8,4)`, `value_bet_win_rate DECIMAL(6,4)`.
- **Indices added by 005:** `DROP INDEX IF EXISTS idx_active_model;` and `CREATE UNIQUE INDEX idx_active_model_per_type ON model_versions(model_type) WHERE is_active = true`. The unique-active-per-type guarantee was the migration's intent; the multi-active-row reality (88 = 45 active + 43 inactive per META_PLAN v6 § 9.13) is a registry-semantics topic for `ml_layer_architecture_bible.md`, not this bible.
- **JSONB shape:** `feature_list` and `hyperparameters` are opaque to the schema; per-row keys are model-specific.
- **Writers:** training pipeline (`equine-training-*` ECS task families) on training completion.
- **Readers:** the four predictions-table writers; dashboard endpoints for the registry view.
- **Approximate rows:** 88 (45 active + 43 inactive) per META_PLAN v6 Claim 7 (inherited).

#### 4.1.12 `wr_predictions`

- **Source:** migration 005; UNIQUE constraint reshaped in migration 011.
- **Columns:** `prediction_id UUID PK DEFAULT gen_random_uuid()`, `entry_id UUID NOT NULL REFERENCES entries(entry_id)`, `race_id UUID NOT NULL REFERENCES races(race_id)`, `horse_id UUID NOT NULL REFERENCES horses(horse_id)`, `model_version_id UUID REFERENCES model_versions(model_version_id)`, `win_probability DECIMAL(6,4)`, `place_probability DECIMAL(6,4)`, `show_probability DECIMAL(6,4)`, `predicted_rank INTEGER`, `confidence_score DECIMAL(8,4)`, `is_top_pick BOOLEAN DEFAULT FALSE`, `morning_line_implied_prob DECIMAL(6,4)`, `overlay_pct DECIMAL(6,4)`, `is_value_flag BOOLEAN DEFAULT FALSE`, `recommended_bet_type VARCHAR(20)`, `exotic_partners UUID[] DEFAULT '{}'`, `feature_importance JSONB DEFAULT '{}'`, `actual_finish INTEGER`, `was_win BOOLEAN`, `was_place BOOLEAN`, `was_show BOOLEAN`, `exacta_hit BOOLEAN`, `trifecta_hit BOOLEAN`, `created_at TIMESTAMPTZ DEFAULT NOW()`. Plus a `style` column and a `model_used` column referenced in 011's commentary (the constraint reshape; see § 8.W.2).
- **UNIQUE (post-011):** `wr_predictions_unique_per_entry_style` on `(race_id, entry_id, style)`. The pre-011 constraint was `(race_id, entry_id, model_used, style)` — the `model_used` inclusion was the architectural mistake migration 011 corrected.
- **Indices:** `idx_wr_predictions_race ON (race_id, predicted_rank)`, `idx_wr_predictions_date ON (created_at)`.
- **Writers:** `WRPredictionRepository` at `backend/repositories/wr_prediction_repository.py` (called by `equine-wr-inference` Lambda).
- **Readers:** WR result endpoints; LS service reads WR predictions and writes enrichment columns; ComparePage; track_record endpoints.

#### 4.1.13 `pl_predictions`

- **Source:** migration 005.
- **Columns:** `prediction_id UUID PK DEFAULT gen_random_uuid()`, `entry_id`, `race_id`, `horse_id`, `model_version_id`, `win_probability DECIMAL(6,4)`, `predicted_ev DECIMAL(8,4)`, `confidence_score DECIMAL(8,4)`, `predicted_rank INTEGER`, `is_top_pick BOOLEAN DEFAULT FALSE`, `closing_odds DECIMAL(8,2)`, `implied_probability DECIMAL(6,4)`, `edge_pct DECIMAL(6,4)`, `is_value_bet BOOLEAN DEFAULT FALSE`, `is_strong_value BOOLEAN DEFAULT FALSE`, `kelly_fraction DECIMAL(6,4)`, `kelly_bet_size DECIMAL(8,2)`, `feature_importance JSONB DEFAULT '{}'`, `actual_finish INTEGER`, `was_win BOOLEAN`, `bet_profit DECIMAL(8,2)`, `created_at`.
- **UNIQUE:** `(entry_id)` per migration 005. (Distinct from `wr_predictions` and `ls_predictions` which use the `(race_id, entry_id, style)` triple post-011/010.)
- **Indices:** `idx_pl_predictions_race ON (race_id, predicted_rank)`, partial index `idx_pl_predictions_value ON (race_id) WHERE is_value_bet = true`.
- **Writers:** `PLPredictionRepository` at `backend/repositories/pl_prediction_repository.py` (called by `equine-pl-inference` Lambda).
- **Readers:** PL result endpoints; the dual-prediction (`handicapping_prob` / `market_prob`) read paths surfaced via API per the canonical PLPrediction dataclass.

#### 4.1.14 `ls_predictions`

- **Source:** migration 005 (stub); reshaped to first-class in migration 010.
- **Columns (post-010):** the original migration 005 columns (`prediction_id`, `entry_id`, `race_id`, `horse_id`, `model_version_id`, `final_win_probability DECIMAL(6,4)`, `longshot_alert BOOLEAN`, `confidence VARCHAR(10)`, `kelly_fraction`, `predicted_rank`, `xgb_rank_score DECIMAL(8,4)`, `rf_longshot_prob`, `lstm_trajectory`, `calibrated_win_prob`, `bayesian_angle_ev DECIMAL(8,4)`, `angle_description TEXT`, `feature_importance JSONB`, `actual_finish`, `was_win`, `actual_odds`, `bet_profit`, `created_at`) plus migration 010 additions: `style VARCHAR(50) DEFAULT 'general'`, `market_prob NUMERIC`, `edge_pct NUMERIC`, `is_top_pick BOOLEAN DEFAULT FALSE`, `morning_line_implied_prob NUMERIC`.
- **UNIQUE (post-010):** `ls_predictions_unique_per_entry_style` on `(race_id, entry_id, style)`. The pre-010 constraint was the auto-generated `ls_predictions_entry_id_key` from the `UNIQUE(entry_id)` declaration; 010 dropped it explicitly (per its `DROP CONSTRAINT IF EXISTS ls_predictions_entry_id_key; DROP INDEX IF EXISTS ls_predictions_entry_id_key;` block).
- **Indices:** `idx_ls_predictions_race ON (race_id, predicted_rank)`, partial index `idx_ls_predictions_alert ON (race_id) WHERE longshot_alert = true`.
- **Writers:** `LSPredictionRepository` at `backend/repositories/ls_prediction_repository.py` (called by `equine-ls-inference` Lambda).
- **Readers:** longshot alert UI; LS service also writes enrichment columns onto `wr_predictions` per migration 010's commentary, so transitional reads still hit `wr_predictions`.
- **Population state:** populated since Phase A3 / migration 010 (2026-05-01); migration 010 explicitly notes "Existing rows: 0 (verified empty)" at constraint-swap time.

### 4.2 Migration discipline (per META_PLAN v6 § 7.12)

#### 4.2.1 Numbering format

Migrations 001–011 keep their existing `NNN_short_description.sql` format. This is grandfathered per Tony's locked decision in META_PLAN v6 § 7.12; no Phase 0 prerequisite to rename them. The 12 migration files (one duplicate-005, see § 4.2.2) by filename:

```
001_initial_schema.sql
002_fix_race_type_length.sql
003_widen_varchar_columns.sql
004_backfill_running_style.sql
005_backfill_pace_delta.sql
005_three_prediction_tables.sql
006_backfill_early_pace_pressure.sql
007_backfill_trainer_name.sql
008_create_trainer_stats.sql
009_backfill_pace_delta_v2.sql
010_ls_predictions_first_class.sql
011_wr_predictions_unique_fix.sql
```

Migration **012 onward** uses the `NNN_YYYYMMDD_short_description.sql` format. The date in the filename is the date the migration was authored. The cutover is documented in this section. As of this draft, no 012 has been authored; the format is forward-only discipline.

#### 4.2.2 The duplicate-005 case

`005_backfill_pace_delta.sql` and `005_three_prediction_tables.sql` share the `005` prefix. This is an inherited problem; Phase 1 documents it but does not remediate it. Operational notes:

- Lexical sort orders them deterministically: `005_backfill_pace_delta.sql` precedes `005_three_prediction_tables.sql` alphabetically (`b` < `t`).
- The runner sees both as opaque distinct filenames; the `schema_migrations.filename` UNIQUE column accepts both.
- Migration 009 explicitly supersedes the work of `005_backfill_pace_delta.sql` because the original used `finish_call_position` (0% populated). 009's comment block documents the correction.
- The forward rule (no new duplicates) applies to migration 012 onward. Remediation for the existing duplicate lives in `PHASE_5_BACKLOG.md` (Phase 5.X.Y; specific phase number assigned at backlog-entry time per META_PLAN v6 § 7.7 + § 9.9).

#### 4.2.3 The `schema_migrations` runner mechanism

The runner (`backend/database/migrations/migrate.py`) tracks applied migrations by filename:

```python
CREATE TABLE IF NOT EXISTS schema_migrations (
    migration_id SERIAL PRIMARY KEY,
    filename VARCHAR(255) UNIQUE NOT NULL,
    applied_at TIMESTAMPTZ DEFAULT NOW()
)
```

Behavior (per `migrate.py:64–104`):

1. `ensure_migrations_table(conn)` — `CREATE TABLE IF NOT EXISTS` on first run; idempotent thereafter.
2. `get_applied_migrations(conn)` — returns the set of filenames already in `schema_migrations`.
3. Iterate `os.listdir(MIGRATIONS_DIR)` in `sorted()` order, filter to `*.sql`, skip those already applied, execute the rest in a single transaction per file plus an INSERT of the filename into `schema_migrations`. On exception: rollback, log the failing SQL, `sys.exit(1)`.

Key properties:

- **Tracking is by filename, not by content hash.** Renaming a migration after it has been applied makes it look unapplied; the runner will attempt to re-apply it. Don't rename applied migrations.
- **Each migration runs in its own transaction.** Migrations 010 and 011 wrap their bodies in explicit `BEGIN; … COMMIT;` blocks — that pattern is allowed but not required by the runner (the runner already wraps each file's `cur.execute(sql)` call in a per-file commit).
- **Seeds run optionally** via `--seed` flag, after migrations, from `backend/database/seeds/*.sql`. Seeds are not tracked in `schema_migrations`; they re-run on every invocation.
- **Connection sourcing:** `DATABASE_URL` env var if set; otherwise fetch from Secrets Manager via `DB_SECRET_ARN`. Hard-fails (`sys.exit(1)`) if neither is set.
- **`schema_migrations` is not part of the 14-table count** in § 3.2 because it is created by the runner at first invocation, not by a migration file.

#### 4.2.4 Rollback format (in-file down-block)

Per META_PLAN v6 § 7.12: rollback SQL lives in the same migration file as the up SQL, in a clearly delimited block, after the up SQL. The runner does NOT auto-execute the down block; rollback is operator-driven.

For non-reversible migrations, the down block reads `-- NON-REVERSIBLE because: <reason>` plus a recovery procedure. **None of migrations 001–011 carry an explicit down block.** This is a Phase 5 remediation candidate, tracked in `PHASE_5_BACKLOG.md` per META_PLAN v6 § 7.7. From migration 012 onward, the down-block requirement is enforced.

Illustrative full migration shape (hypothetical 012; not yet authored) is given verbatim in META_PLAN v6 § 7.12; this bible references that hypothetical example without re-pasting it.

#### 4.2.5 Migration testing (non-production database first)

Per META_PLAN v6 § 7.12: migrations are tested against a non-production database before deploy. "Non-production" means a local Postgres instance OR a dedicated dev Aurora cluster (one does **not** currently exist for EE). Until a dev Aurora exists, migrations are tested against local Postgres only — Aurora-specific behaviors (JSONB serialization quirks, IAM auth) cannot be caught pre-deploy. Phase 5 should add a dev Aurora cluster as a triage-queue item; until then, the rule has reduced enforcement and untested-against-Aurora is elevated risk.

Per META_PLAN v6 § 7.13's Layer 1 deploy gating: untested migrations against production are forbidden under any condition (including emergency hotfix). The rule does **not** waive under the emergency hotfix carve-out.

---

## 5. Discipline rules

Forbidden Patterns and Common Mistakes specific to the schema/migration domain. Sub-section numeric IDs per BIBLE_STRUCTURE_SPEC v3 § 5.5.

### 5.1 (Forbidden Pattern) Including dispatch metadata in UNIQUE constraints (locked 2026-05-04)

`UNIQUE` constraints on the per-pipeline predictions tables MUST be expressed in terms of stable identity columns (`race_id`, `entry_id`, `style`), NOT in terms of per-call dispatch metadata (`model_used`, model variant flags, transient routing decisions).

Rationale: the `model_used` column in `wr_predictions` was a per-horse dispatch flag set by `WRInferenceService.predict_race` based on workout availability. Each horse goes through ONE model variant per inference, never both — so `model_used` looks like a UNIQUE-eligible column. But when workout data lands between inference runs, the same `(race_id, entry_id, style)` accumulates a `core` row AND a `full` row; the new variant doesn't conflict with the old key because `model_used` differs, so both persist. 157 races (~1.35% of 11,629) accumulated 427 duplicate rows before migration 011 fixed it. See § 8.W.2 for the full bug entry.

**FORBIDDEN:**

```sql
ALTER TABLE wr_predictions
  ADD CONSTRAINT wr_predictions_unique_per_entry_model_style
  UNIQUE (race_id, entry_id, model_used, style);
-- model_used differs across calls; UPSERT cannot deduplicate.
```

**CORRECT:**

```sql
ALTER TABLE wr_predictions
  ADD CONSTRAINT wr_predictions_unique_per_entry_style
  UNIQUE (race_id, entry_id, style);
-- model_used remains as metadata; latest variant overwrites cleanly via INSERT … SET.
```

### 5.2 (Forbidden Pattern) Renaming applied migrations (locked 2026-05-04)

The runner tracks applied migrations by **filename**, not by content hash. Renaming a migration after it has been applied makes the migration appear unapplied; the runner will attempt to re-apply it on the next run. For 005-vs-005 the lexical sort happens to give a deterministic order, but a rename of any 001–011 file would force re-application.

Rationale: `migrate.py:60` reads `SELECT filename FROM schema_migrations`; the comparison is `if filename in applied_set`. No checksum, no content comparison. The whole tracking discipline depends on filename stability post-application.

**FORBIDDEN:**

```bash
# After 010 has been applied to production:
git mv backend/database/migrations/010_ls_predictions_first_class.sql \
       backend/database/migrations/010_20260501_ls_first_class.sql
# The runner now sees 010_20260501_ls_first_class.sql as unapplied
# and tries to run it; CREATE TABLE IF NOT EXISTS saves you here, but
# any non-idempotent migration (DROP CONSTRAINT, INSERT) re-runs and corrupts state.
```

**CORRECT:**

```bash
# Don't rename. If unification of format is desired, that's optional Phase 5+
# cleanup per META_PLAN v6 § 7.12 (which explicitly grandfathers 001–011).
# For new migrations from 012 onward, use the new format from the start.
```

### 5.3 (Common Mistake) "I'll add a JSONB column to mirror these other columns for flexibility" (logged 2026-05-04)

**Wrong instinct:** "This data has a few optional fields and I want flexibility, so I'll JSONB-blob it next to the proper columns and let readers parse as needed."

**Corrected position:** NO. JSONB shadow columns hide schema drift behind opaque blobs. EE's existing JSONB columns are scoped tightly (per-prediction `feature_importance`, per-model `feature_list`/`hyperparameters`) — they capture model-specific structures whose keys legitimately vary by model. They are NOT a substitute for declared columns when the column structure is stable. Add real columns; widen them later if needed (003 widened many in one shot — that's the pattern). Reserve JSONB for the per-row-variable case.

### 5.4 (Common Mistake) "I'll backfill from `finish_call_position` since that's the canonical end-of-race position" (logged 2026-05-04)

**Wrong instinct:** "The schema has `finish_call_position` and that's what every chart-parsing reference talks about, so the backfill should join on it."

**Corrected position:** NO. `finish_call_position` is 0% populated in the historical `past_performances` rows; `finish_position` is 99.5% populated and semantically identical (position at the wire). Migration 005's `005_backfill_pace_delta.sql` made the wrong choice and migration 009 had to redo it. Prefer the high-coverage column when computing backfills; verify population rates before writing the UPDATE. See § 8.W.1.

---

## 6. Currently Open

No current open issues against the schema layer at lock. (The schema/migration domain inherits zero open bugs from the Phase 0 substrate — Bug #28 is a scraper / data-acquisition bug, canonically homed in `data_pipeline_bible.md`. It does not call into question any schema or migration discipline rule.)

---

## 7. Deprecated

### 7.1 Legacy `predictions` table — superseded but still read

| Field/Module | Canonical Source | Notes |
|---|---|---|
| `predictions` table | `wr_predictions` (per-style WR), `pl_predictions` (P&L), `ls_predictions` (LS); created by migration 005 | The legacy `predictions` table was created by `001_initial_schema.sql` (verified). Migration 005 (`005_three_prediction_tables.sql`) created `wr_predictions`, `pl_predictions`, `ls_predictions` as the per-pipeline replacement (verified: zero `DROP TABLE` statements in the migration). The legacy table currently holds 6,600 rows (per META_PLAN v6 Claim 16, inherited). It still has active readers: `prediction_router.py` (3 instantiations of `PredictionRepository` at lines 34, 61, 92, plus 1 import on line 6 = 4 references total per META_PLAN v6 Claim 17, inherited), `race_router.py` (1 instantiation on line 277, plus 1 import on line 273 = 2 references total per META_PLAN v6 Claim 17, inherited), `dashboard_router.py:93,105` (direct SELECT for race-record summaries), `horse_router.py:66` (direct SELECT in horse-PPs query). Planned removal: Phase 5.X.Y (specific phase number assigned at backlog-entry time) after readers are migrated to the per-pipeline tables. Until removal, new code MUST NOT write to the legacy table; reads are tolerated only from the legacy router paths. |

Conditional triggers evaluated:
- if-deprecated-thing-has-active-readers: FIRES. Reader inventory enumerated above.
- if-deprecation-is-partial: FIRES. The legacy table exists and is still read by the four router paths above. The dependency chain to remove it: migrate each reader to the per-pipeline table → confirm zero readers via grep → drop the table in a future migration.
- if-deprecation-produced-Forbidden-Pattern: FIRES (latent). Phase 5.X.Y when readers are migrated should produce a Forbidden Pattern: "MUST NOT write to legacy `predictions` table." Not yet a locked Forbidden Pattern because the legacy table is still actively read; the prohibition applies only on the write path now.

### 7.2 Pre-011 `wr_predictions` UNIQUE constraint shape — superseded

| Field/Module | Canonical Source | Notes |
|---|---|---|
| `wr_predictions_unique_per_entry_model_style` constraint | `wr_predictions_unique_per_entry_style` (post-011) | The pre-011 UNIQUE was `(race_id, entry_id, model_used, style)`. Migration 011 dropped this and added `(race_id, entry_id, style)` after deduplicating 427 rows across 157 races. The pre-011 shape MUST NOT be re-introduced; see § 5.1 Forbidden Pattern. Cross-reference: § 8.W.2. |

### 7.3 Pre-010 `ls_predictions` `UNIQUE(entry_id)` — superseded

| Field/Module | Canonical Source | Notes |
|---|---|---|
| `ls_predictions_entry_id_key` constraint (auto-generated) | `ls_predictions_unique_per_entry_style` on `(race_id, entry_id, style)` | The pre-010 constraint was a single-column `UNIQUE(entry_id)` declared inline at migration 005 stub time. Migration 010 dropped it (table verified empty before swap) and added the standard `(race_id, entry_id, style)` triple matching the wr/pl pattern. The single-column UNIQUE MUST NOT be re-introduced. Cross-reference: § 8.W.3. |

---

## 8. What Was Fixed — Do Not Revert

Institutional immune memory entries for bugs in the schema/migration domain. W.N letter-prefix per BIBLE_STRUCTURE_SPEC v3 § 5.5; sub-numbered as `8.W.<n>` per § 5.5.

### 8.W.1: pace_delta backfill keyed on the wrong end-of-race column (fixed 2026-04-XX, migration 009)

**Symptom:** After running migration 005's `005_backfill_pace_delta.sql`, `pace_delta` remained NULL for the vast majority of historical `past_performances` rows. Pace-aware feature engineering downstream lost a significant portion of its training signal.

**Root cause:** `005_backfill_pace_delta.sql` computed `pace_delta = finish_call_position - call_2_position`. The `finish_call_position` column is 0% populated in historical rows. The semantically identical `finish_position` column is 99.5% populated. The backfill ran, found `finish_call_position IS NOT NULL` matched almost no rows, and silently completed with most rows still NULL.

**Fix:** `009_backfill_pace_delta_v2.sql` re-keyed the backfill on `finish_position`, with bounded ranges (`call_2_position BETWEEN 1 AND 99`, `finish_position BETWEEN 1 AND 89` to exclude DNF/pulled/vet-scratch codes ≥ 90).

**Why this entry exists:** The lesson is the column-population check, not the formula. A future backfill author MUST verify population rates of every column referenced in the WHERE clause before authoring the UPDATE. The Common Mistake at § 5.4 captures this discipline in instinct form.

Conditional triggers evaluated:
- if-fix-involved-migration: FIRES. Migration `009_backfill_pace_delta_v2.sql` (path: `backend/database/migrations/009_backfill_pace_delta_v2.sql`).
- if-fix-invalidated-prior-bible-content: DOES NOT FIRE. No prior bible content existed at fix time (pre-Phase-0).
- if-fix-produced-Forbidden-Pattern: DOES NOT FIRE. The lesson is captured as a Common Mistake (§ 5.4) rather than a Forbidden Pattern because the wrong instinct is procedural, not structural.
- if-fix-touches-multiple-bibles: DOES NOT FIRE. Schema-internal.

### 8.W.2: `wr_predictions` duplicate rows from `model_used` in UNIQUE constraint (fixed 2026-05-XX, migration 011)

**Symptom:** 157 races (~1.35% of 11,629) accumulated 427 duplicate rows in `wr_predictions`. Downstream consumers — LS softmax, ComparePage Cartesian, track_record double-counting — read both `core` and `full` variants per `(race_id, entry_id, style)` without filtering on `model_used`, producing inflated and inconsistent outputs.

**Root cause:** The UNIQUE constraint on `wr_predictions` was `(race_id, entry_id, model_used, style)`. `model_used` is a per-horse dispatch metadata flag set by `WRInferenceService.predict_race` based on workout availability. Each horse goes through ONE model variant per inference. But when workout data lands between inference runs, the same `(race_id, entry_id, style)` accumulates a `core` row from the first run and a `full` row from the second run — they differ on `model_used`, so the UNIQUE constraint does not collapse them; both persist.

**Fix:** Migration `011_wr_predictions_unique_fix.sql` runs cleanup + constraint swap as a single transaction. Cleanup deletes older duplicates per `(race_id, entry_id, style)` ordered by `created_at DESC, prediction_id DESC`. Constraint swap drops `wr_predictions_unique_per_entry_model_style` and adds `wr_predictions_unique_per_entry_style` on `(race_id, entry_id, style)`. Pre-state and post-state checks bracket the cleanup; the post-state check raises an exception if any duplicates remain or the new constraint is missing, aborting the transaction.

**Why this entry exists:** The lesson is the locked Forbidden Pattern at § 5.1 — UNIQUE constraints on the per-pipeline predictions tables MUST be expressed in terms of stable identity columns, not per-call dispatch metadata. Including `model_used` in the UNIQUE looked correct because each inference call sets exactly one variant; the architectural mistake was treating per-call dispatch as identity.

Conditional triggers evaluated:
- if-fix-involved-migration: FIRES. Migration `011_wr_predictions_unique_fix.sql` (path: `backend/database/migrations/011_wr_predictions_unique_fix.sql`).
- if-fix-invalidated-prior-bible-content: DOES NOT FIRE (pre-Phase-0).
- if-fix-produced-Forbidden-Pattern: FIRES. § 5.1 in this bible.
- if-fix-touches-multiple-bibles: PARTIAL. The bug's downstream symptoms manifested in API/Frontend (ComparePage Cartesian) and in ML inference (LS softmax double-counting), but the canonical home is here per § 5.3 cross-cutting bug scope rule — the discipline that prevents recurrence is a schema-layer constraint discipline, not a router or inference discipline.

### 8.W.3: `ls_predictions` `UNIQUE(entry_id)` blocked style differentiation (fixed 2026-05-01, migration 010)

**Symptom:** `ls_predictions` had been an orphan table since the LS service was introduced — its `insert_prediction` repo method had never been called; LS data was being written as enrichment columns on `wr_predictions` (e.g., `longshot_alert`, `longshot_prob`, `ensemble_win_prob`). Tony's revised architecture (2026-05-01) treated LS as a first-class model with its own ranking, requiring the table to accept rows from the LS inference path. The pre-existing `UNIQUE(entry_id)` constraint precluded the `(race_id, entry_id, style)` UPSERT pattern used by the wr/pl per-pipeline tables.

**Root cause:** The original migration 005 stub declared `ls_predictions.entry_id` with a `UNIQUE` keyword inline. In PostgreSQL, that auto-generates an index named `ls_predictions_entry_id_key`. The single-column UNIQUE permitted only one row per entry, with no style differentiation.

**Fix:** `010_ls_predictions_first_class.sql` adds the columns missing for first-class parity (`style`, `market_prob`, `edge_pct`, `is_top_pick`, `morning_line_implied_prob`), then drops the pre-existing constraint plus its auto-generated index (PostgreSQL semantics: the index is owned by the constraint and only drops when the constraint drops), then adds the standard `(race_id, entry_id, style)` triple. Existing rows: 0 (verified empty before swap), so the constraint switch was safe.

**Why this entry exists:** Two lessons. First, the canonical UNIQUE pattern on per-pipeline predictions tables is `(race_id, entry_id, style)` — see § 5.1's broader rule and § 7.3's deprecated entry. Second, when an inline column-level `UNIQUE` keyword auto-generates an index, that index can ONLY be dropped by dropping the constraint itself; future alterations of the column should account for that ownership chain (the migration's explicit `DROP CONSTRAINT IF EXISTS … DROP INDEX IF EXISTS …` block is the safe form).

Conditional triggers evaluated:
- if-fix-involved-migration: FIRES. Migration `010_ls_predictions_first_class.sql` (path: `backend/database/migrations/010_ls_predictions_first_class.sql`).
- if-fix-invalidated-prior-bible-content: DOES NOT FIRE (pre-Phase-0).
- if-fix-produced-Forbidden-Pattern: PARTIAL. Generalized into the broader § 5.1 pattern (with the `wr_predictions` case as the primary anchor). The single-column-UNIQUE-on-entry_id form is captured by the deprecated entry at § 7.3.
- if-fix-touches-multiple-bibles: DOES NOT FIRE. Schema-internal at the constraint layer, even though LS inference behavior at higher layers depends on it.

---

End of Database & Schema Bible draft v1 (convergence test instance run1).
