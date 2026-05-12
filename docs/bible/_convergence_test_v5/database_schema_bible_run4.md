# Database & Schema Bible

**Document:** database_schema_bible.md
**Phase:** 1 (Bible)
**Status:** DRAFT v1 (pre-audit; convergence-test re-run output, run4 slot)
**Author:** CC (drafting under verification discipline; QB orchestrated)
**Date:** 2026-05-05
**Locked:** [pending — convergence test draft, not a Phase 1 lock cycle]

**Revision history:**
- v1 (2026-05-05): Convergence-test re-run draft against BIBLE_STRUCTURE_SPEC v5 + META_PLAN v8. § 5 produced as candidate roster pending QB ratification per § 5.7 G5 closure.

**Tier:** 3 per META_PLAN v8 § 4.1 + § 6.5.

**Anchored on:** META_PLAN v8 + BIBLE_STRUCTURE_SPEC v5 + AUDIT_METHODOLOGY v2 + TRIAGE_QUEUE_SPEC v1 + CONVERGENCE_CRITERIA v2.

**Companion verification log:** `docs/bible/_convergence_test_v5/database_schema_bible_run4_verification.md`.

---

## 1. Scope of this bible

This bible documents the EE database schema, the migration discipline that evolves it, and the JSONB-shaped conventions that live inside its columns. Its target reader is anyone touching a table definition, writing a repository method, authoring a migration, or reasoning about which DB column a feature value reads from.

**In scope:**
- The 14 base tables (`tracks`, `horses`, `trainers`, `jockeys`, `races`, `entries`, `past_performances`, `workouts`, `results`, `predictions`, `model_versions`, `wr_predictions`, `pl_predictions`, `ls_predictions`) with column lists, primary keys, UNIQUE constraints, FK relationships, JSONB columns, and per-table writer/reader inventories.
- The single materialized view (`trainer_stats`) with its aggregate definition and refresh mechanism.
- The schema bootstrap file (`backend/database/schema/schema.sql`) and its relationship to the 12 migration files in `backend/database/migrations/`.
- The migration runner mechanism (`schema_migrations` table + `migrate.py`).
- Migration discipline (numbering format, duplicate-005 inheritance, rollback format, testing requirement) per META_PLAN v8 § 7.12.
- JSONB column conventions across `model_versions.feature_list`, `model_versions.hyperparameters`, and the four per-pipeline `feature_importance` columns.

**Out of scope (covered by other bibles):**
- The runtime-context view of which Lambdas write each table — see `architecture_overview:3.1` and `data_pipeline_bible:4.1`.
- Per-pipeline inference services that write `wr_predictions` / `pl_predictions` / `ls_predictions` — see `ml_layer_architecture_bible:4.2`.
- The router consumers of legacy `predictions` (HTTP-route surface) — see `api_frontend_bible:4.1`.
- Feature engineering implementations that produce the JSONB shapes stored in `feature_importance` and `feature_list` — see `feature_provenance_bible:3` and `feature_provenance_bible:4.1`.
- Bug #28 canonical entry (HRN scraper column-shift, manifesting as NULL `results.win_payout` and `results.daily_double_payout`) — canonical home is `data_pipeline_bible:#28` per META_PLAN v8 § 7.4 cross-cutting bug scope rule. This bible cross-references in § 6 because the symptom touches the schema layer (see § 5.3 G1 closure).

## 2. Definitions

- **Table.** A persistent relation in the `equine_equalizer` Aurora Serverless PostgreSQL database. Schema is defined either in `backend/database/schema/schema.sql` (bootstrap base) or in a migration file (incremental change).
- **Materialized view (matview).** A physically materialized SELECT result, refreshed on demand. EE has exactly one: `trainer_stats` per migration `008_create_trainer_stats.sql`.
- **Migration.** A SQL file in `backend/database/migrations/` whose application is tracked by filename in the `schema_migrations` table per `migrate.py`. Numbered; idempotent (uses `IF NOT EXISTS` / `IF EXISTS` guards where applicable).
- **Schema bootstrap.** `backend/database/schema/schema.sql`, the original consolidated DDL at project genesis. Identical in content to `001_initial_schema.sql` (verified by line-count and diff: both 415 newlines, both define the same 11 base tables). Used as the consolidated reference; current DB state = `schema.sql` followed by migrations 002–011 applied in lexical order.
- **Canonical column.** A column whose name and semantics are stable across the schema lifetime. Renaming a canonical column is a forbidden migration shape (no rename-without-migration-pair).
- **JSONB shadow.** A JSONB column that holds a structured dict whose keys are themselves a stable contract (e.g., `model_versions.feature_list` storing the feature schema for a model; `feature_importance` storing per-feature gain). The shape is contractual but enforced at the application layer, not by a JSON Schema constraint at the DB layer.
- **UNIQUE-on-natural-key.** A UNIQUE constraint over a tuple of business-meaningful columns (e.g., `entries.UNIQUE(race_id, horse_id)`) — distinct from the synthetic primary key UUID.

## 3. Architecture overview

EE's persistence layer is an Aurora Serverless PostgreSQL cluster (database `equine_equalizer`, cluster ARN per dump: `arn:aws:rds:us-east-1:584812014683:cluster:equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`; see verification log V4-13 on the live-state divergence observed at draft time). All EE backend Python code accesses the DB via `psycopg2` direct connection (verified: `backend/shared/db.py` lines 5–6 import `psycopg2` and `psycopg2.extras`; the `backend/repositories/*.py` modules consume `psycopg2` cursors threaded through a connection pool); EE does NOT use the AWS RDS Data API. The `migrate.py` runner uses `psycopg2.connect` (line 144) to apply migrations.

### 3.1 Tables (14)

Decomposed per `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql`:

| # | Table | Source | Purpose (one line) |
|---|---|---|---|
| 1 | `tracks` | `schema.sql:12` | Track metadata: code, name, surfaces, qualifying flag, min claiming price |
| 2 | `horses` | `schema.sql:28` | Horse identity with self-FK to sire/dam/dam_sire |
| 3 | `trainers` | `schema.sql:50` | Trainer name + license |
| 4 | `jockeys` | `schema.sql:62` | Jockey name + license + apprentice flag |
| 5 | `races` | `schema.sql:75` | Race card metadata: distance, surface, type, grade, conditions |
| 6 | `entries` | `schema.sql:109` | Per-horse-per-race entry with equipment + medication flags |
| 7 | `past_performances` | `schema.sql:145` | Per-horse historical race detail; 91 columns; widest table by columns |
| 8 | `workouts` | `schema.sql:272` | Workout history: date, distance, time, bullet flag |
| 9 | `results` | `schema.sql:293` | Race outcome per entry: finish position, payouts (win/place/show/exacta/trifecta/superfecta/daily_double), call positions |
| 10 | `predictions` | `schema.sql:327` | Legacy single-table predictions; superseded by wr/pl/ls split in migration `005_three_prediction_tables.sql`; not dropped (see § 7.1) |
| 11 | `model_versions` | `schema.sql:359` | Model registry: version_name, training_date, accuracy metrics, feature_list (JSONB), hyperparameters (JSONB), s3_artifact_path, is_active |
| 12 | `wr_predictions` | `005_three_prediction_tables.sql:5` | Win-Rate pipeline predictions; current UNIQUE per migration 011: `(race_id, entry_id, style)` |
| 13 | `pl_predictions` | `005_three_prediction_tables.sql:34` | P&L pipeline predictions with Kelly + edge fields; UNIQUE: `(entry_id)` per migration 005 |
| 14 | `ls_predictions` | `005_three_prediction_tables.sql:61` | Longshot pipeline predictions; promoted to first-class in migration 010; current UNIQUE: `(race_id, entry_id, style)` |

Tables 1–11 are the bootstrap set established by `schema.sql` / `001_initial_schema.sql`. Tables 12–14 were added by `005_three_prediction_tables.sql`.

### 3.2 Materialized view (1)

| Matview | Source | Refresh | Definition |
|---|---|---|---|
| `trainer_stats` | `008_create_trainer_stats.sql:7` | Manual (`REFRESH MATERIALIZED VIEW trainer_stats`) per per-migration comment | Aggregates from `past_performances` GROUP BY `trainer_name` HAVING `COUNT(*) >= 5`. Returns one row per trainer with: 1 group key (`trainer_name`) + 8 aggregate columns (`total_starts`, `wins`, `win_rate`, `itm`, `itm_rate`, `layoff_win_rate`, `lasix_win_rate`, `claimed_win_rate`). Total: 9 SELECT-list columns. UNIQUE INDEX `idx_trainer_stats_name` on `trainer_name`. |

Filter clauses (lines 55–58 of `008_create_trainer_stats.sql`): `WHERE trainer_name IS NOT NULL AND finish_position IS NOT NULL AND finish_position < 90`. The `finish_position < 90` clause excludes scratched/DQ-coded entries that store a sentinel value. Consumed by `feature_engineering_service._get_trainer_stats()` per migration preamble.

### 3.3 Schema bootstrap vs migrations

**Bootstrap (`backend/database/schema/schema.sql`, 415 lines per `wc -l`).** Defines the original 11 tables (1–11 above) plus indices and the ALTER-after-create FK from `predictions.model_version_id` to `model_versions.model_version_id`. This file is byte-equivalent in content to `001_initial_schema.sql` (also 415 lines per `wc -l`); they are two physical copies of the same DDL. The bootstrap exists as a single-file consolidated reference; the migration is what the runner actually applies. **Adding new schema does NOT update `schema.sql` — new schema flows through migrations.**

**Migrations (12 files, 001–011 with duplicate-005).** Listed in § 4.2.1. Applied in lexical sort order by `migrate.py` per § 4.2.3. Each migration's effect is cumulative; the current DB state equals `schema.sql` (or equivalently `001_initial_schema.sql`) followed by migrations 002–011 applied in lexical order. Verification of currently-applied migration set requires querying the live `schema_migrations` table (not feasible at draft time per dump appendix — `equine-ingestion` Lambda is INACTIVE; per-source priority § 4.5, tier 1 governs current state but tier 4 substrate provides the migration code that defines what should be applied).

---

## 4. Schema and migration detail

### 4.1 Per-table documentation

Each subsection documents one table with: column list (or count + reference to source), primary key, UNIQUE constraints, FK relationships, JSONB columns where present, primary writers, primary readers, and approximate row count where available (per dump § 4.1, since live DB introspection is not feasible at draft time).

#### 4.1.1 `tracks`

- Source: `schema.sql:12-22` (8 columns).
- Primary key: `track_id UUID`.
- UNIQUE: `track_code` (single-column).
- FK: none.
- Approximate rows: 11 (per dump § 4.1, the QUALIFYING_TRACKS set).
- Primary writers: ingestion Lambda track-bootstrap path.
- Primary readers: most race/entry/PP queries join via `track_code` or `track_id`.

#### 4.1.2 `horses`

- Source: `schema.sql:28-44` (13 columns).
- Primary key: `horse_id UUID`.
- UNIQUE: `registration_id` (nullable; constraint applies when present).
- FK: self-references `sire_id`, `dam_id`, `dam_sire_id` → `horses(horse_id)`.
- Approximate rows: unknown (dump notes ">50K assumed").
- Primary writers: ingestion (race card + chart parser cascade); `merge_duplicate_horses.py` operational script.
- Primary readers: pervasive — every per-horse query.

#### 4.1.3 `trainers`

- Source: `schema.sql:50-56` (4 columns: `trainer_id`, `trainer_name`, `license_number`, `country` + `created_at`).
- Primary key: `trainer_id UUID`.
- UNIQUE: none (no UNIQUE on `trainer_name`; multiple rows per trainer name observed historically).
- Note: `trainer_stats` matview joins on `past_performances.trainer_name`, NOT on `trainers.trainer_id` — the trainer_stats key is the denormalized name string.

#### 4.1.4 `jockeys`

- Source: `schema.sql:62-69` (5 columns).
- Primary key: `jockey_id UUID`.
- UNIQUE: none.

#### 4.1.5 `races`

- Source: `schema.sql:75-103` (24 columns).
- Primary key: `race_id UUID`.
- UNIQUE: `equibase_race_id` (single-column, nullable) AND `(track_id, race_date, race_number)` (composite natural key).
- FK: `track_id` → `tracks(track_id)`.
- Approximate rows: ~2,611 visible via API over 100 days (per dump § 4.1).

#### 4.1.6 `entries`

- Source: `schema.sql:109-139` (26 columns; equipment + medication flags).
- Primary key: `entry_id UUID`.
- UNIQUE: `(race_id, horse_id)` natural key.
- FK: `race_id` → `races`, `horse_id` → `horses`, `trainer_id` → `trainers`, `jockey_id` → `jockeys` (jockey nullable).
- Approximate rows: ~30K (per dump § 4.1).

#### 4.1.7 `past_performances`

- Source: `schema.sql:145-266` (91 columns; widest table).
- Primary key: `pp_id UUID`.
- UNIQUE: `(horse_id, race_date, track_code, race_number)` natural key.
- FK: `horse_id` → `horses(horse_id)` (NOT NULL); `race_id` → `races(race_id)` (NULLABLE).
- **Important:** `race_id` is NULL for ALL historical rows per `data_loader.py` docstring (per dump § 4.1). This is intentional, not a bug — historical PPs predate `races` row creation. New PPs ingested for current race cards may have `race_id` populated when the PP horse is also entered in a current race; the column is nullable by design. See § 5 candidate Common Mistake on race_id NULL acceptance.
- Approximate rows: unknown (dump notes "~250K+ from training context").

#### 4.1.8 `workouts`

- Source: `schema.sql:272-287` (12 columns).
- Primary key: `workout_id UUID`.
- UNIQUE: `(horse_id, workout_date, track_code, distance_furlongs)` natural key.
- FK: `horse_id` → `horses`.
- Approximate rows: 143K+ (per dump § 4.1, "per data_loader docstring").

#### 4.1.9 `results`

- Source: `schema.sql:293-321` (25 columns).
- Primary key: `result_id UUID`.
- UNIQUE: `(entry_id)` single-column natural key.
- FK: `entry_id` → `entries`, `race_id` → `races`, `horse_id` → `horses`.
- Payout columns: `win_payout`, `place_payout`, `show_payout`, `exacta_payout`, `trifecta_payout`, `superfecta_payout`, `daily_double_payout` — all DECIMAL.
- Bug #28 manifestation: `win_payout` and `daily_double_payout` NULL across all rows from 2026-04-30 onward; `place_payout` stores Win values; `show_payout` stores Place values (per dump § 12 Bug #28 row + memory file). Cross-reference: `data_pipeline_bible:#28`. See § 6 Currently Open.

#### 4.1.10 `predictions` (legacy)

- Source: `schema.sql:327-353` (23 columns).
- Primary key: `prediction_id UUID`.
- UNIQUE: `(entry_id)`.
- JSONB columns: `feature_importance JSONB` (no DEFAULT — nullable; in contrast, the per-pipeline tables 12–14 default to `'{}'`).
- FK: `model_version_id` → `model_versions(model_version_id)` (added via post-create ALTER per `schema.sql:383-386`).
- **Status:** legacy. Superseded by the `wr_predictions` / `pl_predictions` / `ls_predictions` split in `005_three_prediction_tables.sql` (2026-03-18). NOT dropped. See § 7.1 Deprecated entry.
- Approximate rows: 6,600 per META_PLAN v8 verification log Claim 16 (re-verification at draft time not feasible per dump appendix; carried forward from inherited claim).
- Reader inventory (verified 2026-05-05): `prediction_router.py` = 1 import (`prediction_router.py:5-6`) + 3 instantiations (lines 34, 61, 92) = 4 references; `race_router.py` = 1 import (lines 272-273) + 1 instantiation (line 277) = 2 references. Total 6 references across 2 files.

#### 4.1.11 `model_versions`

- Source: `schema.sql:359-377` (17 columns).
- Primary key: `model_version_id UUID`.
- UNIQUE: none on `version_name` (multiple rows per name observed historically per dump § 4.1).
- Subsequent ALTER from `005_three_prediction_tables.sql:96-104` adds: `model_type VARCHAR(10) DEFAULT 'wr' CHECK (model_type IN ('wr', 'pl', 'ls'))`, `flat_bet_roi DECIMAL(8,4)`, `kelly_roi DECIMAL(8,4)`, `value_bet_win_rate DECIMAL(6,4)`. Lines 107–109 of the same migration drop the old `idx_active_model` UNIQUE INDEX and create `idx_active_model_per_type` UNIQUE INDEX `ON model_versions (model_type) WHERE is_active = true` — a partial UNIQUE INDEX permitting one active row per (model_type) value while allowing multiple active rows globally. Multi-active-row reality (45 of 88 rows) per `architecture_overview:5` Forbidden Pattern (cross-bible) is enforced through this partial index plus the (style, specialist) decomposition that lives in `version_name`, NOT in the schema directly.
- JSONB columns:
  - `feature_list JSONB` (line 371). Holds the feature schema for the model. Canonical source of truth for "what features did this model see at training time." Consumed by inference paths to align inputs.
  - `hyperparameters JSONB` (line 372). Holds the trainer's hyperparameters dict.
- TEXT-shaped notes: `notes TEXT` (line 375). Per dump § 4.1 the field is described as "JSONB-in-TEXT" — operators store JSON-shaped data here, but the column type is TEXT. The DB does NOT enforce JSON validity on this column. See § 5 candidate Common Mistake on `notes`-as-JSONB.

#### 4.1.12 `wr_predictions`

- Source: `005_three_prediction_tables.sql:5-31` (26 columns at creation; subsequent migrations have not altered the column list).
- Primary key: `prediction_id UUID DEFAULT gen_random_uuid()`.
- UNIQUE constraint history:
  - At creation (2026-03-18 per migration preamble): `UNIQUE(entry_id)` (single-column, line 30 of `005_three_prediction_tables.sql`).
  - Intermediate state (un-audited DDL — see § 8.W.1 below): `UNIQUE (race_id, entry_id, model_used, style)` named `wr_predictions_unique_per_entry_model_style`. This constraint is the one migration `011_wr_predictions_unique_fix.sql:64` drops; no migration file in the 001–011 set creates it explicitly. The constraint either landed via direct DDL outside the migration runner, or via a lost migration.
  - Current (post-`011_wr_predictions_unique_fix.sql`, 2026-05-01 per file mtime): `UNIQUE (race_id, entry_id, style)` named `wr_predictions_unique_per_entry_style`.
- FK: `entry_id` → `entries`, `race_id` → `races`, `horse_id` → `horses`, `model_version_id` → `model_versions` (nullable).
- JSONB column: `feature_importance JSONB DEFAULT '{}'` (line 22).
- Indices (`005_three_prediction_tables.sql:88-89`): `idx_wr_predictions_race ON wr_predictions(race_id, predicted_rank)`, `idx_wr_predictions_date ON wr_predictions(created_at)`.
- LS-enrichment note: per dump § 10 finding #5, LS data is currently written as second-pass enrichment to `wr_predictions` columns (e.g., `ensemble_win_prob`, `longshot_prob`, `trajectory_score`, `angle_*`, `longshot_alert`, `confidence`); these enrichment columns are NOT in the migration 005 column list and were added by un-audited DDL. The first-class migration to `ls_predictions` per migration 010 has not yet displaced this enrichment-write pattern.

#### 4.1.13 `pl_predictions`

- Source: `005_three_prediction_tables.sql:34-58` (23 columns).
- Primary key: `prediction_id UUID`.
- UNIQUE: `(entry_id)` single-column natural key (line 57). Not changed by any subsequent migration as of the 001–011 set.
- FK: `entry_id` → `entries`, `race_id` → `races`, `horse_id` → `horses`, `model_version_id` → `model_versions`.
- JSONB column: `feature_importance JSONB DEFAULT '{}'` (line 52).
- Indices (`005_three_prediction_tables.sql:90-91`): `idx_pl_predictions_race ON pl_predictions(race_id, predicted_rank)`, `idx_pl_predictions_value ON pl_predictions(race_id) WHERE is_value_bet = true` (partial index).

#### 4.1.14 `ls_predictions`

- Source: `005_three_prediction_tables.sql:61-85` at creation (24 columns); modified by `010_ls_predictions_first_class.sql` (lines 23-28) to add: `style VARCHAR(50) DEFAULT 'general'`, `market_prob NUMERIC`, `edge_pct NUMERIC`, `is_top_pick BOOLEAN DEFAULT FALSE`, `morning_line_implied_prob NUMERIC`. Post-010: 29 columns.
- Primary key: `prediction_id UUID`.
- UNIQUE constraint history:
  - At creation (2026-03-18): `UNIQUE(entry_id)` (single-column, line 84) — auto-named `ls_predictions_entry_id_key` by Postgres.
  - Current (post-`010_ls_predictions_first_class.sql`, 2026-05-01 per file mtime): `UNIQUE (race_id, entry_id, style)` named `ls_predictions_unique_per_entry_style`. Migration 010 lines 36-37 explicitly DROP CONSTRAINT and DROP INDEX before adding the new constraint at lines 38-40 — both the prior constraint and its backing index were physically dropped.
- FK: same set as `wr_predictions` / `pl_predictions`.
- JSONB column: `feature_importance JSONB DEFAULT '{}'` (line 78).
- Indices (`005_three_prediction_tables.sql:92-93`): `idx_ls_predictions_race`, `idx_ls_predictions_alert ON ls_predictions(race_id) WHERE longshot_alert = true` (partial index).
- Migration 010 preamble notes: "Existing rows: 0 (verified empty), so the constraint switch is safe." Per dump § 10 finding #5, even after migration 010 LS reads still go through `wr_predictions` enrichment columns; first-class adoption is in flight.

#### 4.1.15 `trainer_stats` (matview, not a table)

Documented in § 3.2. Not repeated here.

### 4.2 Migration discipline (per META_PLAN v8 § 7.12)

#### 4.2.1 Numbering format

Migrations 001–011 keep the existing `NNN_short_description.sql` format (no date in filename); migration 012 onward will use `NNN_YYYYMMDD_short_description.sql` (date is the date the migration was authored). The grandfathering decision is locked in META_PLAN v8 § 7.12; existing migrations are NOT renamed. The runner is unaffected because it tracks by filename string (see § 4.2.3).

The 12 migration files (verified by `ls backend/database/migrations/*.sql`):

| # | Filename | Authored (mtime, approximate) | Purpose |
|---|---|---|---|
| 001 | `001_initial_schema.sql` | 2026-03-15 | Bootstrap of 11 base tables (byte-equivalent to `schema.sql`) |
| 002 | `002_fix_race_type_length.sql` | 2026-03-15 | VARCHAR widening for `race_type` |
| 003 | `003_widen_varchar_columns.sql` | 2026-03-15 | Further VARCHAR widening |
| 004 | `004_backfill_running_style.sql` | 2026-03-17 | Backfill `running_style` on `past_performances` |
| 005 | `005_backfill_pace_delta.sql` | 2026-03-17 | Backfill `pace_delta` column |
| 005 | `005_three_prediction_tables.sql` | 2026-03-18 | Create `wr_predictions` / `pl_predictions` / `ls_predictions` tables; ALTER `model_versions` adding `model_type` + P&L columns + active-per-type partial UNIQUE INDEX |
| 006 | `006_backfill_early_pace_pressure.sql` | 2026-03-17 | Backfill `early_pace_pressure` |
| 007 | `007_backfill_trainer_name.sql` | 2026-03-17 | Backfill `trainer_name` on `past_performances` |
| 008 | `008_create_trainer_stats.sql` | 2026-03-17 | Create `trainer_stats` MATERIALIZED VIEW |
| 009 | `009_backfill_pace_delta_v2.sql` | 2026-03-17 | Re-do `pace_delta` backfill |
| 010 | `010_ls_predictions_first_class.sql` | 2026-05-01 | Promote `ls_predictions` to first-class: add 5 columns, drop single-column UNIQUE, add `(race_id, entry_id, style)` UNIQUE |
| 011 | `011_wr_predictions_unique_fix.sql` | 2026-05-01 | Fix `wr_predictions` UNIQUE constraint: drop `(race_id, entry_id, model_used, style)` form, add `(race_id, entry_id, style)`; cleanup of 427 duplicate rows across 157 races (~1.35% of 11,629 races) |

Total 12 files. The duplicate-005 case is documented in § 4.2.2.

#### 4.2.2 The duplicate-005 case

Two migration files share number `005`: `005_backfill_pace_delta.sql` (2026-03-17, 12 lines) and `005_three_prediction_tables.sql` (2026-03-18, 109 lines). Both files apply successfully because `migrate.py` tracks applied migrations by **filename**, not by numeric prefix (see § 4.2.3) — the runner sees them as distinct opaque strings, and Python's `sorted()` orders them lexically (so `005_backfill_pace_delta.sql` runs before `005_three_prediction_tables.sql` deterministically).

This is an **inherited problem**, not forward-looking discipline. Per META_PLAN v8 § 7.12: "The forward rule (no new duplicates) applies to Phase 5 onward. No Phase 0 action." Remediation (if desired) lives in `PHASE_5_BACKLOG.md`; renumbering one of the duplicates would be a cosmetic cleanup, not a functional necessity.

#### 4.2.3 The `schema_migrations` runner mechanism

`backend/database/migrations/migrate.py` (157 lines per `wc -l`; the file's last line lacks a trailing newline so the Read tool displays content up through line 158) implements the runner. Key mechanics (line numbers reference the verified file content):

- **Connection acquisition.** Lines 21–41: `get_connection_string()` consults `DATABASE_URL` env var first, then falls back to fetching credentials from AWS Secrets Manager via `DB_SECRET_ARN`. Constructs a `postgresql://` connection string and connects via `psycopg2.connect` (line 144).
- **Tracking table.** Lines 44–54: `ensure_migrations_table()` creates `schema_migrations` if absent. Schema:
  ```sql
  CREATE TABLE IF NOT EXISTS schema_migrations (
      migration_id SERIAL PRIMARY KEY,
      filename VARCHAR(255) UNIQUE NOT NULL,
      applied_at TIMESTAMPTZ DEFAULT NOW()
  )
  ```
  Filename is the UNIQUE key; the runner inserts a row per applied migration.
- **Idempotence.** Lines 57–61: `get_applied_migrations()` returns `{filenames}` from `schema_migrations`. Lines 78–80: each migration filename in lexical order is checked; already-applied migrations log "Skipping already applied" and are not re-executed.
- **Lexical ordering.** Line 69: `sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql"))`. Lexical sort is the only ordering — no numeric or date-based parsing. This is what makes the duplicate-005 case deterministic.
- **Failure handling.** Lines 87–102: if a migration fails, the transaction is rolled back, the failing filename + error + SQL are logged, and the runner exits with `sys.exit(1)`. The `schema_migrations` row is NOT inserted on failure.
- **Seed mode.** Lines 107–135 + 140: `--seed` flag triggers a second pass over `seeds/` if it exists. Seeds are NOT tracked in `schema_migrations`.

The `schema_migrations` table itself is NOT defined in `schema.sql` or in any of the 001–011 migration files; it is created lazily by `ensure_migrations_table()` on first run.

#### 4.2.4 Rollback format (in-file down-block)

META_PLAN v8 § 7.12 specifies the rollback format: down SQL lives in the same migration file after the up SQL, in a clearly-delimited block, NOT auto-executed by the runner. The standard form is:

```sql
-- ============================================
-- DOWN MIGRATION (manual; not auto-run)
-- ============================================
-- <commentary; SQL commented out so it is not accidentally executed>
```

For non-reversible migrations, the down block reads "NON-REVERSIBLE because: <reason>" with a recovery procedure.

**Substrate observation:** None of the existing 001–011 migrations include a down-migration block in the META_PLAN v8 § 7.12 form. Migrations 010 and 011 use `BEGIN; ... COMMIT;` transactional boundaries (and 011 uses `DO $$ ... $$` blocks for pre-state and post-state assertions), but neither carries a commented-out down block. The rollback discipline is forward-looking for migration 012+; existing migrations 001–011 are grandfathered. See § 5 candidate Forbidden Pattern on missing rollback DOWN blocks.

#### 4.2.5 Migration testing (non-production database first)

Per META_PLAN v8 § 7.12: "non-production database first. **'Non-production' definition:** local Postgres instance OR a dedicated dev Aurora cluster (when one exists; one does NOT currently exist for EE)." Until a dev Aurora cluster exists, migrations are tested against local Postgres only — Aurora-specific behaviors (JSONB serialization quirks, IAM auth) cannot be caught pre-deploy. Phase 5 is the cutover for adding a dev Aurora; until then, untested-against-Aurora is elevated risk per Tony's locked language.

---

## 5. Discipline rules

**[candidate roster pending QB ratification per § 5.7 G5 closure]**

Per BIBLE_STRUCTURE_SPEC v5 § 5.7, Phase 1 drafters enumerate candidate Forbidden Patterns and Common Mistakes from substrate (the bible's domain code, AWS infrastructure, prior audits, the META_PLAN v8 § 9.1–9.13 anti-pattern catalog, operator-stated history). The candidate roster surfaces to QB BEFORE § 5 of the bible locks. Provenance discriminator per § 5.7: rules surfaced from existing locked Phase 0 documents (META_PLAN v8 § 9.X anti-patterns; META_PLAN v8 § 7.12 grandfathered migration discipline) are grandfathered; CC-introduced rules require QB ratification.

**For this convergence-test draft, § 5 is NOT locked.** The candidate roster is presented below for QB review. Each candidate is annotated with provenance (substrate-grounded vs CC-introduced) and substrate evidence trace.

### Candidate 5.1 (Forbidden Pattern; substrate-grounded; grandfathered from META_PLAN v8 § 7.12)

**Pattern:** Authoring a new migration (012+) without a rollback DOWN block.

**Substrate evidence:** META_PLAN v8 § 7.12 specifies the rollback format with worked example. The current migration set (001–011) is grandfathered (no DOWN blocks present in any of the 12 files); the rule applies forward-looking from migration 012.

**FORBIDDEN form:**
```sql
-- 012_20260601_add_some_column.sql
ALTER TABLE foo ADD COLUMN bar TEXT;
```

**CORRECT form:**
```sql
-- 012_20260601_add_some_column.sql
ALTER TABLE foo ADD COLUMN bar TEXT;

-- ============================================
-- DOWN MIGRATION (manual; not auto-run)
-- ============================================
-- ALTER TABLE foo DROP COLUMN IF EXISTS bar;
```

**Provenance:** grandfathered from META_PLAN v8 § 7.12.

### Candidate 5.2 (Forbidden Pattern; substrate-grounded; grandfathered from META_PLAN v8 § 7.12)

**Pattern:** Authoring a new migration with a duplicate prefix number.

**Substrate evidence:** META_PLAN v8 § 7.12: "The forward rule (no new duplicates) applies to Phase 5 onward." Inherited duplicate-005 case is documented in § 4.2.2.

**FORBIDDEN form (file added in Phase 5+):**
```
backend/database/migrations/
  ...
  011_wr_predictions_unique_fix.sql
  011_some_other_change.sql       ← DUPLICATE PREFIX, FORBIDDEN
```

**CORRECT form:**
```
backend/database/migrations/
  ...
  011_wr_predictions_unique_fix.sql
  012_20260601_some_other_change.sql
```

**Provenance:** grandfathered from META_PLAN v8 § 7.12.

### Candidate 5.3 (Forbidden Pattern; substrate-grounded)

**Pattern:** Including per-horse dispatch metadata (e.g., `model_used`) in prediction-table UNIQUE constraints.

**Substrate evidence:** Migration `011_wr_predictions_unique_fix.sql` preamble (lines 1–25) explicitly identifies the architectural mistake: `model_used` is per-horse dispatch metadata set by `WRInferenceService.predict_race` based on workout availability — each horse goes through one model variant per inference, never both. Including `model_used` in `wr_predictions_unique_per_entry_model_style` caused 427 duplicate rows across 157 races (~1.35% of 11,629) when the same `(race_id, entry_id, style)` accumulated a `'core'` row AND a `'full'` row across inference runs. The fix replaced the constraint with `(race_id, entry_id, style)`. The discipline applies to all prediction tables: UNIQUE = `(race_id, entry_id, style)` — never include dispatch-metadata flags.

**FORBIDDEN form:**
```sql
ALTER TABLE wr_predictions
  ADD CONSTRAINT wr_predictions_unique_per_entry_model_style
  UNIQUE (race_id, entry_id, model_used, style);
```

**CORRECT form:**
```sql
ALTER TABLE wr_predictions
  ADD CONSTRAINT wr_predictions_unique_per_entry_style
  UNIQUE (race_id, entry_id, style);
```

**Provenance:** substrate-grounded (migration 011 verbatim).

### Candidate 5.4 (Forbidden Pattern; CC-introduced — requires QB ratification)

**Pattern:** Modifying `backend/database/schema/schema.sql` to reflect a new schema state.

**Substrate evidence:** Verified by `wc -l` and `diff` that `schema.sql` (415 lines) is byte-equivalent to `001_initial_schema.sql` (415 lines). Subsequent schema (3 prediction tables, 1 matview, plus column additions) lives ONLY in migrations 002–011 — `schema.sql` was not updated when those migrations landed. The substrate operating model is: `schema.sql` is the consolidated bootstrap reference, NOT a current-state snapshot. The current DB state = `schema.sql` + migrations 002–011 applied in lexical order.

**FORBIDDEN form:** Adding a new `CREATE TABLE` block to `schema.sql` to "document" a new table.

**CORRECT form:** Author a new migration in `backend/database/migrations/`; apply via the runner.

**Provenance:** CC-introduced — META_PLAN v8 § 7.12 prescribes migration discipline but does not explicitly forbid editing `schema.sql`. The pattern is inferable from substrate but should be ratified by QB before lock.

### Candidate 5.5 (Forbidden Pattern; CC-introduced — requires QB ratification)

**Pattern:** Inserting new rows into the legacy `predictions` table.

**Substrate evidence:** § 7.1 Deprecated entry; META_PLAN v8 Appendix A.4. Current readers: `prediction_router.py` (4 references) + `race_router.py` (2 references). No verified writer in current code. The table's row count is fixed at 6,600 (per Claim 16) — superseded by the wr/pl/ls split.

**FORBIDDEN form:**
```python
PredictionRepository(conn).insert_prediction(...)  # writes to legacy `predictions` table
```

**CORRECT form:** route writes through `WRPredictionRepository` / `PLPredictionRepository` / `LSPredictionRepository` (the three migration-005 destinations).

**Provenance:** CC-introduced — META_PLAN v8 documents the table as Deprecated but does not explicitly forbid writes. QB should decide whether this Forbidden Pattern lives here or in `api_frontend_bible:5` (whose discipline more directly enforces router-write discipline).

### Candidate 5.6 (Common Mistake; substrate-grounded)

**Wrong instinct:** "`past_performances.race_id` is a FK column, so I'll add a NOT NULL constraint to enforce referential integrity."

**Corrected position:** NO. `past_performances.race_id` is INTENTIONALLY nullable. Per dump § 4.1, it is NULL for ALL historical rows (training-context PPs predate the corresponding `races` rows). The schema bootstrap at `schema.sql:148` declares the column as `race_id UUID REFERENCES races(race_id)` — no `NOT NULL`. Adding NOT NULL would invalidate the entire historical PP corpus.

**Substrate evidence:** `schema.sql:148`; dump § 4.1.

**Provenance:** substrate-grounded; the spec (G3 closure illustrative example at BIBLE_STRUCTURE_SPEC v5 § 5.6.1 G3 closure narrative) names this as a Common Mistake exemplar.

### Candidate 5.7 (Common Mistake; substrate-grounded)

**Wrong instinct:** "`model_versions.notes` is structured JSON, so I'll parse it like JSONB."

**Corrected position:** NO. The column type is TEXT (`schema.sql:375`: `notes TEXT`). Per dump § 4.1 the field is described as "JSONB-in-TEXT" — operators store JSON-shaped data in it, but the DB enforces no JSON validity. Reads must `json.loads(row['notes'])` defensively (handling parse errors); writes must `json.dumps()` before persisting. The two true JSONB columns on `model_versions` are `feature_list` and `hyperparameters` (lines 371–372).

**Substrate evidence:** `schema.sql:375`; dump § 4.1.

**Provenance:** substrate-grounded.

### Candidate 5.8 (Common Mistake; substrate-grounded)

**Wrong instinct:** "`wr_predictions.feature_importance` defaults to NULL like `predictions.feature_importance`, so I'll handle NULL on read."

**Corrected position:** NO. The legacy `predictions.feature_importance` is `JSONB` with no default (nullable). The three per-pipeline tables — `wr_predictions`, `pl_predictions`, `ls_predictions` — declare `feature_importance JSONB DEFAULT '{}'` at creation (`005_three_prediction_tables.sql:22, 52, 78`). Reads of the per-pipeline tables receive `{}` for unset rows, not NULL. The defaulting asymmetry between legacy and per-pipeline tables is the lesson.

**Substrate evidence:** `schema.sql:342` (legacy, no default); `005_three_prediction_tables.sql:22, 52, 78` (per-pipeline, `DEFAULT '{}'`).

**Provenance:** substrate-grounded.

### Roster summary (for QB review)

- Forbidden Patterns: 5 candidates (5.1, 5.2, 5.3 grandfathered/substrate; 5.4, 5.5 CC-introduced).
- Common Mistakes: 3 candidates (5.6, 5.7, 5.8 all substrate-grounded).

**QB ratification questions:**
1. Should candidate 5.5 (legacy `predictions` table writes) live here or in `api_frontend_bible:5`?
2. Should candidate 5.4 (modifying `schema.sql`) be ratified or dropped as too operational?
3. Is the JSONB-defaulting asymmetry (5.8) substantial enough for a Common Mistake, or is it ordinary defensive-read discipline that doesn't deserve a roster slot?

§ 5 is NOT locked at this draft. Per § 5.7 workflow: CC re-drafts § 5 to match QB's ratified roster after this convergence test concludes.

---

## 6. Currently Open

One open issue at draft time whose symptoms touch the schema layer:

- **Bug #28 (HRN scraper column-shift; canonical home `data_pipeline_bible:#28`).** Symptoms manifest in the `results` table: `win_payout` and `daily_double_payout` columns are NULL across all rows from 2026-04-30 onward; `place_payout` stores Win values; `show_payout` stores Place values. The schema-layer manifestation is a populated-with-wrong-data condition rather than a constraint violation, because `results` columns are nullable and have no CHECK constraints on payout values. Per BIBLE_STRUCTURE_SPEC v5 § 5.3 G1 closure, this bible includes a one-line cross-reference to the canonical home; the substantive description (root cause, fix path, regression-test discipline) lives in `data_pipeline_bible:#28`. Tracked in `PHASE_5_BACKLOG.md` (entry pending Phase 1 scoping per dump § 12; Bug #28 status `NEW (2026-05-03)`).

No other open issues at draft time whose symptoms touch this bible's domain.

---

## 7. Deprecated

### 7.1 Legacy `predictions` table

- **Field/Module name:** the legacy `predictions` table (`schema.sql:327-353`) and the `PredictionRepository` class (`backend/repositories/prediction_repository.py`).
- **Canonical source (replacement):** the three per-pipeline tables `wr_predictions`, `pl_predictions`, `ls_predictions` introduced in `005_three_prediction_tables.sql` (2026-03-18). New code routes prediction writes through `WRPredictionRepository` / `PLPredictionRepository` / `LSPredictionRepository`.
- **Notes:**
  - Approximate row count: 6,600 (per Claim 16 inherited; live re-verification not feasible at draft time).
  - Reader inventory (verified 2026-05-05): 6 references across 2 files. `prediction_router.py`: 1 import (lines 5–6) + 3 instantiations (lines 34, 61, 92) = 4 references. `race_router.py`: 1 import (lines 272–273) + 1 instantiation (line 277) = 2 references.
  - The legacy table was NOT dropped by migration 005; its rows persist alongside the per-pipeline tables.
  - The active-row partial UNIQUE INDEX `idx_active_model_per_type` (added in `005_three_prediction_tables.sql:107-109`) replaced the prior `idx_active_model` UNIQUE INDEX; the prior index was physically dropped via `DROP INDEX IF EXISTS idx_active_model` and so does NOT qualify for a Deprecated entry under § 5.6.4 (per the verified-physical-drop clause; see verification log V4-9).
- **Phase 5 backlog reference:** Phase 5.X.Y (specific phase number pending — `PHASE_5_BACKLOG.md` entry not yet authored; placeholder per META_PLAN v8 § 7.3 placeholder-resolution sub-rule case (i): "verifiable forward target whose phase number is not yet pinned").

### Superseded SQL constraint Deprecated qualification (per § 5.6.4 G2 closure verification)

Two prior UNIQUE constraint forms were superseded during the migration history. Per § 5.6.4: "If the superseded form has been physically dropped (DDL operation removed it), the Deprecated entry is NOT required — the migration history serves as immune memory."

1. **`wr_predictions.UNIQUE(entry_id)` (migration 005, line 30) and `wr_predictions_unique_per_entry_model_style` UNIQUE (race_id, entry_id, model_used, style) (un-audited intermediate state).** Both prior forms were superseded by `011_wr_predictions_unique_fix.sql:63-68`. The migration 005 form's auto-generated index would have been dropped when the intermediate `unique_per_entry_model_style` form was added (PostgreSQL replacement semantics); the intermediate form was DROPped explicitly at `011:64` (`DROP CONSTRAINT IF EXISTS wr_predictions_unique_per_entry_model_style`). Both prior forms are physically dropped from the live schema. **Verification:** read of migration 011 lines 63-68 (substrate); live `\d wr_predictions` introspection not feasible at draft time per dump appendix. Per § 5.6.4 verified-physical-drop clause: **NO Deprecated entry required.**

2. **`ls_predictions.UNIQUE(entry_id)` (migration 005, line 84) named `ls_predictions_entry_id_key`.** Superseded by `010_ls_predictions_first_class.sql:35-40`. Migration 010 lines 36–37 explicitly DROP CONSTRAINT IF EXISTS and DROP INDEX IF EXISTS for the prior form, then ADD CONSTRAINT for the new `ls_predictions_unique_per_entry_style` form. The migration 010 preamble (lines 30–34) explicitly notes: "The single-column UNIQUE is backed by an auto-generated index that can only be dropped by dropping the constraint (PostgreSQL semantics)." The prior form is physically dropped from the live schema. **Verification:** read of migration 010 lines 35–40 (substrate). Per § 5.6.4 verified-physical-drop clause: **NO Deprecated entry required.**

No other Deprecated entries at draft time.

---

## 8. What Was Fixed — Do Not Revert

### 8.W.1: `wr_predictions` UNIQUE constraint architectural fix (fixed 2026-05-01)

**Symptom:** 427 duplicate rows accumulated across 157 races (~1.35% of 11,629 races) in `wr_predictions`. Downstream consumers (LS softmax, ComparePage Cartesian, track_record double-counting) read both variants without filtering on `model_used`, causing inflated counts and inconsistent rankings.

**Root cause:** The intermediate-state UNIQUE constraint `wr_predictions_unique_per_entry_model_style` over `(race_id, entry_id, model_used, style)` included `model_used` — a per-horse dispatch metadata flag set by `WRInferenceService.predict_race` based on workout availability. Each horse goes through ONE model variant per inference (never both), but the `model_used` flag varied across inference runs as workout data landed between runs. The same `(race_id, entry_id, style)` accumulated a `'core'` row AND later a `'full'` row; neither conflicted with the UNIQUE key, so both persisted.

**Fix:** `011_wr_predictions_unique_fix.sql` (migration 011, mtime 2026-05-01). Single-transaction cleanup-plus-constraint-swap. Drops the prior constraint; adds `wr_predictions_unique_per_entry_style UNIQUE (race_id, entry_id, style)` matching the PL/LS pattern. Cleanup deletes older duplicates per `(race_id, entry_id, style)` keeping the most recent by `(created_at DESC, prediction_id DESC)`. Pre-state and post-state assertions in `DO $$ ... $$` blocks fail the transaction if duplicates remain after cleanup or if the new constraint is missing post-ALTER.

**Why this entry exists:** UNIQUE constraints over prediction tables MUST be over the natural-business-key tuple `(race_id, entry_id, style)`. Per-horse dispatch metadata flags (`model_used`, future analogues) are NOT part of the natural key — including them allows duplicate rows to accumulate when dispatch decisions vary between inference runs. The discipline is: prediction-table UNIQUE = `(race_id, entry_id, style)`; dispatch metadata stays as a column, never enters the UNIQUE.

**Conditional triggers evaluated (per § 5.6.1.2 tertiary-state notation):**
- if-fix-involved-migration: **FIRES.** Migration `011_wr_predictions_unique_fix.sql` (file path `backend/database/migrations/011_wr_predictions_unique_fix.sql`, migration number 011).
- if-fix-invalidated-prior-content: **DOES NOT FIRE.** No prior bible content existed at fix time (pre-Phase-0).
- if-fix-produced-Forbidden-Pattern: **FIRES.** Cross-reference to candidate Forbidden Pattern at § 5 Candidate 5.3 (pending QB ratification per § 5.7): "Including per-horse dispatch metadata (e.g., `model_used`) in prediction-table UNIQUE constraints."
- if-fix-touches-multiple-bibles: **CONDITIONAL.** The bug is canonically scoped to the schema bible (the prevention is a schema constraint discipline). Downstream consumers (LS softmax, ComparePage Cartesian, track_record) span `ml_layer_architecture_bible:4.2` (LS pipeline) and `api_frontend_bible:4.1` (ComparePage route). The CONDITIONAL caveat: the schema bible is the canonical home because the Fix is a `ALTER TABLE ... DROP CONSTRAINT ... ADD CONSTRAINT` schema-layer change; the consuming-bible cross-references would be descriptive (where the duplicate-read symptom manifested) rather than canonical (where the prevention discipline lives). No cross-bible W.N entries are created; the consuming bibles may cite this entry as `database_schema_bible:8.W.1` if their own discipline-rule rosters reference the duplicate-read failure mode.

---

## Front-matter footnotes / draft notes

This is a convergence-test re-run draft. § 5 is presented as a candidate roster (not locked) per BIBLE_STRUCTURE_SPEC v5 § 5.7 G5 closure. § 1–4, § 6, § 7, § 8 follow the locked Phase 0 methodology faithfully. The verification log (`database_schema_bible_run4_verification.md`) carries: inherited claims from META_PLAN v8 verification log + BIBLE_STRUCTURE_SPEC v5 § 9.1; new claims V4-1 through V4-13; methodology-interpolation self-check; recursive-precision check.

**Convention choice surfaced (per § 6.X G4 closure):** § 1–4 organization follows the BIBLE_STRUCTURE_SPEC v5 § 6.6 recommended structure verbatim (Scope, Definitions, Architecture overview with 3.1/3.2/3.3 sub-sections, Schema-and-migration detail with 4.1 per-table/4.2 migration-discipline). No § 1–4 reorganization deviation taken.
