# Database & Schema Bible

**Document:** database_schema_bible
**Phase:** 1 (Bible)
**Status:** DRAFT v1 (pre-audit) — convergence test re-run instance per META_PLAN v8 § 5.3
**Author:** CC (drafting under verification discipline; QB orchestrated)
**Date:** 2026-05-05
**Locked:** [pending]

**Revision history:**
- v1 (2026-05-05): initial draft for v5 convergence test re-run (run3 slot)

**Tier:** 3 per META_PLAN v8 § 4.1 + § 6.5.

**Anchored on:** META_PLAN v8 (LOCKED 2026-05-05) + BIBLE_STRUCTURE_SPEC v5 (LOCKED 2026-05-05).

**Companion verification log:** `_convergence_test_v5/database_schema_bible_run3_verification.md`.

---

## 1. Scope of this bible

This bible documents EE's persistent storage layer:

- The Aurora Serverless PostgreSQL cluster that holds all production data.
- The 14 tables and 1 materialized view that constitute the live schema.
- The bootstrap file (`backend/database/schema/schema.sql`) and the migration sequence (`backend/database/migrations/`) that produce that schema.
- The `schema_migrations` runner mechanism (`backend/database/migrations/migrate.py`) that applies migrations.
- JSONB and array column conventions in places where they appear.
- UNIQUE / FK constraint shape across the prediction-table family.

What this bible does **not** document:

- **What writes the rows** — the data-flow side (HRN scraper, NYRA scraper, Equibase chart parser, ingestion Lambda, training-time DB writes) belongs in `data_pipeline_bible:3` and `data_pipeline_bible:4`.
- **What reads the rows for inference** — the per-pipeline inference services (WR / PL / LS) that compute predictions and write `wr_predictions` / `pl_predictions` / `ls_predictions` belong in `ml_layer_architecture_bible:4`.
- **What reads the rows for the API** — the routers that translate HTTP requests into repo calls live in `api_frontend_bible:4`.
- **The semantics of feature columns** — what `pace_delta` means, why `running_style` is computed the way it is, etc., live in `feature_provenance_bible:4`.
- **AWS-level Aurora configuration** — IAM, ACUs, parameter groups, snapshot policy live in `architecture_overview:3.3`.

The dividing line is intentional: this bible answers "what is the shape of the schema, and how does the migration discipline work?" Other bibles answer "who writes/reads what for which purpose."

---

## 2. Definitions

- **Table:** a `CREATE TABLE` declaration in the live Aurora schema. EE has 14.
- **Materialized view:** a `CREATE MATERIALIZED VIEW` declaration; the result is persisted on disk and refreshed manually. EE has 1 (`trainer_stats`).
- **Schema bootstrap:** `backend/database/schema/schema.sql`, the canonical fresh-cluster bring-up file. Mirrors migration `001_initial_schema.sql`. Does NOT replay subsequent migrations; a fresh cluster runs `schema.sql` and then the migration runner from 001 onward (the runner skips 001 because filename matching is exact and `schema_migrations` is empty on a new cluster — but the bootstrap file's content is identical to 001 so the schema converges).
- **Migration:** a numbered `.sql` file in `backend/database/migrations/`. Applied in lexical filename order by the runner.
- **Migration runner:** `backend/database/migrations/migrate.py`, a Python/`psycopg2` script that tracks applied migrations by filename in the `schema_migrations` table.
- **JSONB column:** a column declared with PostgreSQL's `JSONB` type. EE uses JSONB for `feature_importance` (per-prediction), `feature_list` (per-model-version), and `hyperparameters` (per-model-version).
- **Array column:** a column declared with `[]`-suffix type. EE uses `UUID[]` for `predictions.exotic_partners` / `wr_predictions.exotic_partners` and `TEXT[]` for `tracks.surfaces`.
- **Canonical column:** a column whose name and type appear in `backend/models/canonical.py` dataclass fields. The dataclass row mirrors the table row 1:1 for shared columns.
- **Prediction-table family:** the trio `wr_predictions` / `pl_predictions` / `ls_predictions`, plus the legacy `predictions` table that pre-dates the split.

---

## 3. Architecture overview

This bible's slice of EE: what is on disk in Aurora, and how it got there.

### 3.1 The cluster

EE runs against an Aurora Serverless v2 PostgreSQL cluster.

- **Cluster ARN (operator-stated, per META_PLAN v8 verification log Claim and EE_CURRENT_STATE_DUMP § 4):** `arn:aws:rds:us-east-1:584812014683:cluster:equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`
- **Database name:** `equine_equalizer`
- **Connection mode:** Python clients use `psycopg2` directly via `DATABASE_URL` (env var) or via username/password/host/port/dbname fetched from AWS Secrets Manager (`DB_SECRET_ARN`). EE Python code does NOT use the RDS Data API — verified by recursive grep across `backend/` and `model/` (the only `rds-data` matches are inside vendored `botocore/data/endpoints.json` and `botocore`'s package metadata, both passive SDK packaging artifacts; no `boto3.client('rds-data')` and no `execute_statement` call is present in EE code).
- **Cluster-level configuration** (ACUs, parameter groups, IAM auth, snapshot policy): not in scope here; see `architecture_overview:3.3`.

### 3.2 The 14 tables (decomposed list)

Verified by `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql` and de-duplicating across the bootstrap-vs-migration overlap.

Bootstrap (11 tables, declared in both `schema.sql` and `001_initial_schema.sql`; the two files are intentionally identical for the bootstrap subset):

1. `tracks`
2. `horses`
3. `trainers`
4. `jockeys`
5. `races`
6. `entries`
7. `past_performances`
8. `workouts`
9. `results`
10. `predictions` (the legacy prediction table; superseded but not dropped — see § 4.1.10 + § 7.1)
11. `model_versions`

Added by migration 005 (`005_three_prediction_tables.sql`, the second of the duplicate-005 pair):

12. `wr_predictions`
13. `pl_predictions`
14. `ls_predictions`

Total: 11 + 3 = 14. The post-005 trio replaces the role of `predictions` for new code paths; the legacy `predictions` table persists with active readers (per § 7.1).

`schema_migrations` is the runner's bookkeeping table; it is created by `migrate.py:46–53` (CREATE IF NOT EXISTS), not declared in `schema.sql` or any retained migration. It is **not counted** among the 14 (per common-mistakes convention; see § 5 candidate roster).

### 3.3 The 1 materialized view: `trainer_stats`

Created by migration 008 (`008_create_trainer_stats.sql:7`). Aggregates from `past_performances` keyed by `trainer_name`.

- **Group key:** `trainer_name` (1 column)
- **Aggregate columns (8):** `total_starts`, `wins`, `win_rate`, `itm`, `itm_rate`, `layoff_win_rate`, `lasix_win_rate`, `claimed_win_rate`
- **HAVING clause:** `COUNT(*) >= 5` (the 5-start minimum threshold for inclusion)
- **Read by:** `backend/services/feature_engineering_service.py` `_get_trainer_stats()` (per migration 008 file-header comment)
- **Refresh:** manual via `REFRESH MATERIALIZED VIEW trainer_stats` per the migration's file-header comment. No automated refresh.
- **Unique index:** `idx_trainer_stats_name` on `(trainer_name)` per migration 008 lines 61–62.

### 3.4 Schema bootstrap vs migrations

Two distinct artifacts coexist:

- `backend/database/schema/schema.sql` (415 lines verified via `wc -l`): the canonical fresh-cluster bring-up file. Contains the 11 bootstrap tables, the cross-table FK from `predictions` to `model_versions`, and 12 `CREATE INDEX` statements.
- `backend/database/migrations/*.sql` (12 files): incremental schema and data evolutions, applied in filename-lexical order by the runner.

`schema.sql` and `001_initial_schema.sql` are intentionally identical for the bootstrap subset. The duplication is by design: a fresh dev cluster can be brought up by running `schema.sql` directly without invoking the runner. Production-style deploys apply migrations from 001 onward; the runner sees `001_initial_schema.sql` as the first migration and records it as applied.

### 3.5 The prediction-table family at a glance

| Table | Created by | Current UNIQUE (per migration history) | Active writers | Active readers |
|---|---|---|---|---|
| `predictions` (legacy) | 001 / `schema.sql` | `UNIQUE(entry_id)` | none in new code; legacy only | `prediction_router.py`, `race_router.py`, `dashboard_router.py`, `horse_router.py` (per § 7.1) |
| `wr_predictions` | 005 (three_prediction_tables) | `UNIQUE(race_id, entry_id, style)` after 011 | WR inference service | WR routers; LS for enrichment reads |
| `pl_predictions` | 005 (three_prediction_tables) | `UNIQUE(entry_id)` per 005; no subsequent migration in retained set | PL inference service | PL routers |
| `ls_predictions` | 005 (three_prediction_tables) | `UNIQUE(race_id, entry_id, style)` after 010 | LS inference service (post-010) | LS routers |

Per-pipeline inference writers and readers are documented in `ml_layer_architecture_bible:4` and `api_frontend_bible:4`. This bible documents only the schema shape.

---

## 4. Schema and migration detail

### 4.1 Per-table documentation

One sub-section per table. Column lists are summarized to the load-bearing columns; the source of truth for column names and types is `schema.sql` and the migrations themselves (no duplication).

#### 4.1.1 `tracks`

- **Purpose:** registry of racetracks. Seeded from `backend/database/seeds/tracks.sql` via `migrate.py --seed`.
- **PK:** `track_id UUID`
- **Notable columns:** `track_code VARCHAR(10) UNIQUE NOT NULL`, `surfaces TEXT[]`, `is_qualifying BOOLEAN DEFAULT false`
- **UNIQUE constraints:** `track_code` (column-level); `equibase_race_id` (in `races`, not here — noted to avoid confusion)
- **Primary writers:** `migrate.py --seed`; ingestion paths that resolve track codes
- **Primary readers:** every router that joins to `races`

#### 4.1.2 `horses`

- **Purpose:** horse registry with breeding pedigree.
- **PK:** `horse_id UUID`
- **Notable columns:** `registration_id VARCHAR(50) UNIQUE`, self-referential FKs `sire_id` / `dam_id` / `dam_sire_id` to other horse rows
- **Primary writers:** ingestion (HRN scraper resolves names to horse rows)
- **Primary readers:** entries / past_performances / workouts joins

#### 4.1.3 `trainers`

- **Purpose:** trainer registry.
- **PK:** `trainer_id UUID`
- **Notable columns:** `trainer_name VARCHAR(100) NOT NULL` (no UNIQUE — name collisions tolerated; `license_number` is the distinguishing field but is nullable)

#### 4.1.4 `jockeys`

- **Purpose:** jockey registry.
- **PK:** `jockey_id UUID`
- **Notable columns:** `is_apprentice BOOLEAN DEFAULT false`

#### 4.1.5 `races`

- **Purpose:** per-race-card row (one per race, identified by track + date + race number).
- **PK:** `race_id UUID`
- **Composite UNIQUE:** `(track_id, race_date, race_number)`; column-level UNIQUE on `equibase_race_id`
- **Notable columns:** `distance_furlongs DECIMAL(4,1) NOT NULL`, `surface VARCHAR(20) NOT NULL`, `race_type VARCHAR(20) NOT NULL` (widened by migration 002 from a shorter VARCHAR; see § 4.2 cutover discussion), weather columns

#### 4.1.6 `entries`

- **Purpose:** one row per (race, horse) pairing — the program of who is running.
- **PK:** `entry_id UUID`
- **Composite UNIQUE:** `(race_id, horse_id)`
- **Notable columns:** `morning_line_odds DECIMAL(8,2)`, `is_scratched BOOLEAN DEFAULT false`, equipment-change boolean cluster

#### 4.1.7 `past_performances`

- **Purpose:** per-horse historical race row. Each row is one race a horse has run. **Note:** `race_id` here is FK-nullable — historical rows have `race_id IS NULL` because the historical race may not have a corresponding `races` row (the bibliographic grain is `(horse_id, race_date, track_code, race_number)`, not `race_id`).
- **PK:** `pp_id UUID`
- **Composite UNIQUE:** `(horse_id, race_date, track_code, race_number)`
- **JSONB columns:** none on this table
- **Pace columns** added by progressive migrations:
  - `running_style VARCHAR(20)` declared in 001 (line 245); widened to `VARCHAR(30)` by migration 003 (line 25); backfilled by migration 004
  - `pace_delta DECIMAL(6,2)` backfilled by migration 005 (`005_backfill_pace_delta.sql`, the first of the duplicate-005 pair) and re-backfilled by migration 009 (correctness fix)
  - `early_pace_pressure INTEGER` backfilled by migration 006
  - `trainer_name VARCHAR(100)` backfilled by migration 007 (this column was in the original 001 declaration as nullable)

#### 4.1.8 `workouts`

- **Purpose:** per-horse workout-day row.
- **PK:** `workout_id UUID`
- **Composite UNIQUE:** `(horse_id, workout_date, track_code, distance_furlongs)`
- **Notable columns:** `is_bullet BOOLEAN DEFAULT false`, `rank_on_day INTEGER`

#### 4.1.9 `results`

- **Purpose:** per-entry post-race-result row. One row per entry that finished (or scratched-with-result).
- **PK:** `result_id UUID`
- **UNIQUE:** `(entry_id)` — one result per entry
- **Notable columns:** `finish_position INTEGER NOT NULL`, payout columns: `win_payout DECIMAL(8,2)`, `place_payout DECIMAL(8,2)`, `show_payout DECIMAL(8,2)`, `exacta_payout`, `trifecta_payout`, `superfecta_payout`, `daily_double_payout`
- **Currently-open caveat:** Bug #28 (cross-cutting; canonical home `data_pipeline_bible:#28`) leaves `win_payout` and `daily_double_payout` NULL for rows ingested via the HRN scraper since 2026-04-30, with `place_payout` / `show_payout` carrying off-by-one mis-mapped values. See § 6 cross-reference.

#### 4.1.10 `predictions` (legacy)

- **Purpose:** the original (pre-005) prediction table. Holds pre-2026-03-18 rows and continues to receive some legacy writes from older code paths.
- **PK:** `prediction_id UUID`
- **UNIQUE:** `(entry_id)`
- **JSONB:** `feature_importance JSONB`
- **Array:** `exotic_partners UUID[]`
- **FK:** `model_version_id` to `model_versions` (added as a separate `ALTER TABLE … ADD CONSTRAINT fk_model_version` after both tables exist; see `schema.sql:383–386`)
- **Row count (per META_PLAN v8 Claim 16, dashboard `counts.predictions`):** 6,600
- **Reader inventory (per META_PLAN v8 Claim 16; re-verified live via grep at draft time):**
  - `prediction_router.py`: 1 import (line 5) + 3 instantiations (lines 34, 61, 92) = 4 references
  - `race_router.py`: 1 import (lines 272–273) + 1 instantiation (line 277) = 2 references
  - `dashboard_router.py:93,105` (direct SELECT)
  - `horse_router.py:66` (direct SELECT)
- **Deprecation status:** see § 7.1.

#### 4.1.11 `model_versions`

- **Purpose:** registry of trained model artifacts.
- **PK:** `model_version_id UUID`
- **JSONB columns:** `feature_list`, `hyperparameters`
- **Active-row index:** migration 005 dropped the global `idx_active_model` and added `idx_active_model_per_type` as a partial unique index `ON model_versions (model_type) WHERE is_active = true`. **Operationally relevant:** this enforces "at most one active row per `model_type`" but says nothing about (style, specialist) — see `ml_layer_architecture_bible:4` for the multi-active-row reality (45 active across 88 rows per META_PLAN v8 § 9.13).
- **Added by 005:** `model_type VARCHAR(10) DEFAULT 'wr' CHECK (model_type IN ('wr', 'pl', 'ls'))`, `flat_bet_roi DECIMAL(8,4)`, `kelly_roi DECIMAL(8,4)`, `value_bet_win_rate DECIMAL(6,4)`

#### 4.1.12 `wr_predictions`

- **Purpose:** per-entry per-style WR (win-rate) prediction row.
- **Created:** migration 005 (`005_three_prediction_tables.sql:5–31`)
- **PK:** `prediction_id UUID`
- **UNIQUE per migration history:** declared as `UNIQUE(entry_id)` in migration 005; migration 011 replaces it with `UNIQUE(race_id, entry_id, style)` named `wr_predictions_unique_per_entry_style`. **Schema-vs-migration drift note:** migration 011's preamble (line 4) describes the pre-state as `UNIQUE (race_id, entry_id, model_used, style)`, which is NOT what migration 005 declares. Neither the `model_used` column nor the four-column UNIQUE constraint named `wr_predictions_unique_per_entry_model_style` (referenced in 011's `DROP CONSTRAINT IF EXISTS`, line 64) is declared in any retained migration. The `model_used` column is read by `transforms.py:604` and `wr_prediction_repository.py:304/338/368`, so it does exist in the live schema; the migration that added it is missing from the retained set. Live DB introspection (`\d wr_predictions`) is the source of truth for current state. See § 6 Currently Open for tracking.
- **JSONB:** `feature_importance JSONB DEFAULT '{}'`
- **Array:** `exotic_partners UUID[] DEFAULT '{}'`
- **Outcome columns:** `actual_finish`, `was_win`, `was_place`, `was_show`, `exacta_hit`, `trifecta_hit` (post-race backfill from `results`)

#### 4.1.13 `pl_predictions`

- **Purpose:** per-entry P&L (profit-and-loss / value-betting) prediction row.
- **Created:** migration 005 (`005_three_prediction_tables.sql:34–58`)
- **PK:** `prediction_id UUID`
- **UNIQUE per migration history:** `UNIQUE(entry_id)`. No subsequent migration in the retained set changes this. Migration 011's preamble (line 18) refers to a "PL / LS pattern — UNIQUE (race_id, entry_id, style)"; per migration history that pattern applies to LS (after 010) and WR (after 011), not PL. PL retains the single-column UNIQUE per migration history. Live DB state authoritative; flagged in § 6.
- **JSONB:** `feature_importance JSONB DEFAULT '{}'`
- **Notable columns:** `closing_odds`, `implied_probability`, `edge_pct`, `is_value_bet BOOLEAN`, `kelly_fraction`, `kelly_bet_size`

#### 4.1.14 `ls_predictions`

- **Purpose:** per-entry per-style LS (longshot / 7-layer ensemble) prediction row.
- **Created:** migration 005 (`005_three_prediction_tables.sql:61–85`) as a stub.
- **Promoted to first-class:** migration 010 (`010_ls_predictions_first_class.sql`) added columns `style VARCHAR(50) DEFAULT 'general'`, `market_prob NUMERIC`, `edge_pct NUMERIC`, `is_top_pick BOOLEAN DEFAULT FALSE`, `morning_line_implied_prob NUMERIC`; replaced `UNIQUE(entry_id)` with `UNIQUE(race_id, entry_id, style)` named `ls_predictions_unique_per_entry_style`. Existing rows at migration time: 0 (per migration 010 file-header comment line 17).
- **JSONB:** `feature_importance JSONB DEFAULT '{}'`
- **Notable columns:** `xgb_rank_score`, `rf_longshot_prob`, `lstm_trajectory`, `calibrated_win_prob`, `bayesian_angle_ev`, `angle_description TEXT` (the seven LS layers are documented in `ml_layer_architecture_bible:4`).

### 4.2 Migration discipline (per META_PLAN v8 § 7.12)

#### 4.2.1 Numbering format (grandfathered 001–011 + NNN_YYYYMMDD from 012+)

Per META_PLAN v8 § 7.12: migrations 001–011 keep the existing `NNN_short_description.sql` format (no rename, grandfathered). Migration 012 onward will use `NNN_YYYYMMDD_short_description.sql`; the date is the date the migration was authored. As of 2026-05-05, migration 012 has not been authored — only 001–011 exist (with the duplicate-005 pair, see § 4.2.2).

The 12 retained migration files (per `ls backend/database/migrations/*.sql`):

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

#### 4.2.2 The duplicate-005 case

Two files share the `005_` prefix: `005_backfill_pace_delta.sql` (data backfill) and `005_three_prediction_tables.sql` (schema additions for the per-pipeline tables).

**Operational characteristics:**

- The migration runner (`migrate.py:69–72`) lists `*.sql` filenames via `os.listdir` then `sorted()`. Lexical sort orders the duplicate pair deterministically: `005_backfill_pace_delta.sql` precedes `005_three_prediction_tables.sql` alphabetically (`b` < `t`).
- The runner records each filename independently in `schema_migrations.filename` (which has a `UNIQUE NOT NULL` constraint per migrate.py:50). The two filenames are distinct strings; the runner sees them as opaque distinct entries, not as a "duplicate."
- The duplicate is an inherited artifact of the pre-Phase-0 development pace, not a runner bug. Per META_PLAN v8 § 7.12, the forward rule (no new duplicates) applies to Phase 5 onward; remediation lives in `PHASE_5_BACKLOG.md`.

#### 4.2.3 The `schema_migrations` runner mechanism

`migrate.py:44–61` defines two helper functions:

- `ensure_migrations_table(conn)` (lines 44–54): executes `CREATE TABLE IF NOT EXISTS schema_migrations (migration_id SERIAL PRIMARY KEY, filename VARCHAR(255) UNIQUE NOT NULL, applied_at TIMESTAMPTZ DEFAULT NOW())`.
- `get_applied_migrations(conn)` (lines 57–61): returns the set of filenames already present in `schema_migrations`.

`run_migrations` (lines 64–104) iterates the lexically sorted `*.sql` files, skips those already in the applied set, and for each pending migration: runs the SQL inside a single transaction, then `INSERT INTO schema_migrations (filename) VALUES (%s)` and `commit`. On exception: `rollback` and `sys.exit(1)`. The transaction boundary is per-migration; partial application is not permitted.

`schema_migrations` is bookkeeping — not part of the EE domain schema. It is created on demand by `ensure_migrations_table` rather than declared in `schema.sql` or any retained migration.

#### 4.2.4 Rollback format (in-file down-block)

Per META_PLAN v8 § 7.12: rollback SQL lives in the **same migration file**, after the up SQL, in a clearly-delimited comment block. The runner does NOT auto-execute the down block. Rollback is operator-driven.

Of the 12 retained migrations, none currently carries an explicit down-block. The down-block convention is forward-looking (META_PLAN v8 § 7.12's illustrative example is hypothetical migration 012). For non-reversible migrations, the down-block reads: "NON-REVERSIBLE because: <reason>" plus a recovery-procedure list (per META_PLAN v8 § 7.12 illustrative form).

#### 4.2.5 Migration testing

Per META_PLAN v8 § 7.12: non-production database first. EE does not currently have a dev Aurora cluster — migrations are tested against local Postgres only. Aurora-specific behaviors (JSONB serialization, IAM auth interactions) cannot be caught pre-deploy until a dev Aurora exists. Tracked as Phase 5 work per META_PLAN v8 § 7.12. See § 6.

---

## 5. Discipline rules

**[candidate roster pending QB ratification per § 5.7]**

The rule roster below is enumerated from substrate per BIBLE_STRUCTURE_SPEC v5 § 5.7 G5 closure. **§ 5 of this bible does not lock as part of this convergence test draft.** QB ratification of the roster (per § 5.7 step 3) precedes lock; CC re-drafts to match the ratified roster (step 4) before § 5 locks (step 5).

Each candidate carries provenance annotation distinguishing **substrate-grounded** (sourced from EE code, AWS infrastructure, prior audits, or Phase 0 anti-pattern catalog at META_PLAN v8 § 9.1–9.13) from **CC-introduced** (drafter inference flagged for Tony / QB ratification).

Candidate types: Forbidden Patterns (sub-section 5.X) and Common Mistakes (sub-section 5.X) per § 5.6.2 and § 5.6.3.

### Candidate 5.A (Forbidden Pattern): Including dispatch metadata in UNIQUE constraints (locked TBD)

**Substrate-grounded.** Source: migration 011's preamble (lines 1–25) plus the 157-races / 427-rows post-mortem in line 14. The pre-011 wr_predictions UNIQUE included `model_used`, a per-horse dispatch-metadata flag set by `WRInferenceService.predict_race` based on workout availability. Same `(race_id, entry_id, style)` accumulated `'core'` and `'full'` rows; the new variant did not conflict with the old key, so both persisted; downstream consumers double-counted.

- **Rationale:** dispatch metadata records WHICH variant ran; UNIQUE constraints describe the bibliographic grain of the row. Mixing the two creates duplicates that are silent under the constraint.
- **FORBIDDEN:**
  ```sql
  ALTER TABLE wr_predictions
    ADD CONSTRAINT wr_predictions_unique_per_entry_model_style
    UNIQUE (race_id, entry_id, model_used, style);
  ```
- **CORRECT:**
  ```sql
  ALTER TABLE wr_predictions
    ADD CONSTRAINT wr_predictions_unique_per_entry_style
    UNIQUE (race_id, entry_id, style);
  -- model_used remains as a metadata column; the latest variant overwrites
  -- via the ON CONFLICT … DO UPDATE SET clause.
  ```
- **Cross-reference:** § 8.W.1 (the migration 011 fix).

### Candidate 5.B (Forbidden Pattern): Renaming an applied migration filename (locked TBD)

**Substrate-grounded** (anchored in META_PLAN v8 § 7.12 Tony-ratified grandfathering rule). The migration runner tracks applied migrations by filename. Renaming a file that has been applied causes the runner to see the renamed file as unapplied and re-run it; non-idempotent migrations (DROP CONSTRAINT, INSERT, ALTER TABLE without IF EXISTS) corrupt state on re-run.

- **Rationale:** META_PLAN v8 § 7.12 grandfathers 001–011 to existing format; renames are a Phase 5 unification option, not a Phase 0 activity. The cost of renaming an applied migration in production is silent re-execution of arbitrary DDL.
- **FORBIDDEN:** renaming `010_ls_predictions_first_class.sql` to `010_20260501_ls_first_class.sql` after it has been recorded in `schema_migrations`.
- **CORRECT:** new migrations from 012 onward use the new format; existing 001–011 stay as-is.

### Candidate 5.C (Forbidden Pattern): Writing to the legacy `predictions` table from new code (locked TBD)

**Substrate-grounded** (anchored in META_PLAN v8 Appendix A.4 + § 7.7 Deprecated). Migration 005 created `wr_predictions` / `pl_predictions` / `ls_predictions` as the per-pipeline replacement for the legacy `predictions` table. Migration 005 contains zero `DROP TABLE` statements (verifiable via grep on the file); the legacy table persists with active readers for legacy router paths. New code paths writing to `predictions` re-introduce the cross-pipeline ambiguity that the per-pipeline tables exist to eliminate.

- **Rationale:** the per-pipeline tables (`wr_predictions` / `pl_predictions` / `ls_predictions`) carry pipeline-specific columns (`closing_odds` / `kelly_fraction` for PL; `xgb_rank_score` / `lstm_trajectory` / `bayesian_angle_ev` for LS) that the legacy `predictions` does not. Writing to `predictions` from a new pipeline drops those columns silently.
- **FORBIDDEN:** `INSERT INTO predictions (...)` from any new code path.
- **CORRECT:** route writes to `wr_predictions`, `pl_predictions`, or `ls_predictions` per pipeline. Reads from the legacy table are tolerated only via the legacy router paths (per § 7.1).

### Candidate 5.D (Forbidden Pattern): Joining `past_performances` by `race_id` without `IS NOT NULL` guard (locked TBD)

**Substrate-grounded.** `past_performances.race_id` is FK-nullable per `schema.sql:148`. Historical rows have `race_id IS NULL` because the historical race may not have a corresponding `races` row (the bibliographic grain is `(horse_id, race_date, track_code, race_number)`, not `race_id`). A naive INNER JOIN on `race_id` silently drops historical rows.

- **Rationale:** the column exists for forward-coupling when the historical race happens to have a present-day `races` row; it is opportunistic, not invariant. Code that treats `race_id` as guaranteed-non-null on `past_performances` produces silently truncated training sets.
- **FORBIDDEN:**
  ```sql
  SELECT pp.* FROM past_performances pp
  JOIN races r ON pp.race_id = r.race_id;  -- silently drops null-race_id rows
  ```
- **CORRECT:** join on the natural grain (`pp.horse_id`, `pp.race_date`, `pp.track_code`, `pp.race_number`) when historical rows are required; or filter explicitly with `WHERE pp.race_id IS NOT NULL` when only present-day-linked rows are wanted.

### Candidate 5.E (Forbidden Pattern): Adding a JSONB column to "stay flexible" without a documented schema (locked TBD)

**Substrate-grounded** (anchored in EE's existing JSONB use: `predictions.feature_importance`, `wr_predictions.feature_importance`, `pl_predictions.feature_importance`, `ls_predictions.feature_importance`, `model_versions.feature_list`, `model_versions.hyperparameters`). Each existing JSONB column is a known shape (e.g., `feature_importance` is a `{feature_name: weight}` dict). New JSONB columns without a documented shape become "drawer of unknowns" — readers have no contract, writers have no constraint.

- **Rationale:** JSONB is the right type when a heterogeneous shape is required (per-model feature_list varies); it is the wrong type when a flat column would suffice. Default to flat columns; reserve JSONB for shapes that cannot be flattened. Where JSONB is used, document the shape in this bible's per-table sub-section.
- **FORBIDDEN:** `ALTER TABLE wr_predictions ADD COLUMN extras JSONB;` (no documented shape, no rationale).
- **CORRECT:** flat columns by default; JSONB only with bible documentation of the shape.

### Candidate 5.F (Common Mistake): "I'll count `schema_migrations` as one of EE's tables" (locked TBD)

**CC-introduced** (substrate-derivable from the runner mechanism, but no operator-stated rationale). `schema_migrations` is created by `migrate.py:46–53`, not declared in `schema.sql` or any retained migration. It is bookkeeping for the runner, not part of the EE domain schema. Counting it inflates the table total to 15.

- Wrong instinct: "There are 15 tables — I see 14 plus `schema_migrations`."
- Corrected position: 14. `schema_migrations` is the runner's bookkeeping; per META_PLAN v8 Claim 4 the canonical count is 14 + 1 matview, and `schema_migrations` is excluded.

### Candidate 5.G (Common Mistake): "The duplicate-005 pair is a bug to fix" (locked TBD)

**Substrate-grounded** (anchored in META_PLAN v8 § 7.12). The duplicate-005 pair is an inherited artifact, NOT a runner-correctness bug. The runner records each filename independently per `migrate.py:50`'s `UNIQUE NOT NULL` on `schema_migrations.filename`; two distinct strings = two distinct entries.

- Wrong instinct: "We need to rename one of the 005 files to fix the duplicate."
- Corrected position: NO. Per META_PLAN v8 § 7.12, the rule is forward-only (no new duplicates from 012 onward). The existing pair runs deterministically (lexical sort puts `005_backfill_pace_delta.sql` before `005_three_prediction_tables.sql`). Renaming would re-trigger application (Forbidden Pattern 5.B). Optional Phase 5 cleanup, not Phase 0 work.

### Candidate 5.H (Common Mistake): "I'll backfill `pace_delta` from `finish_call_position` since that's the canonical end-of-race column" (locked TBD)

**Substrate-grounded** (anchored in the migration 005 → migration 009 re-backfill pair). Migration 005 (`005_backfill_pace_delta.sql`) computed `pace_delta` from one end-of-race column; migration 009 (`009_backfill_pace_delta_v2.sql`) re-backfilled it after the canonical column choice was corrected. The rationale is documented in the migration files.

- Wrong instinct: "I'll use `finish_call_position` as the end-of-race position for pace_delta computation."
- Corrected position: see migration 009's preamble for the canonical end-of-race column. The two-step backfill exists because the first attempt picked the wrong column.

### Candidate 5.I (Common Mistake): "`schema.sql` is generated from migrations, so they can't drift" (locked TBD)

**CC-introduced.** `schema.sql` and `001_initial_schema.sql` are intentionally identical — but they are maintained as two independent files, not derived. There is no script that regenerates one from the other. Drift is possible if a hand-edit lands in one and not the other; the discipline of keeping them aligned is procedural.

- Wrong instinct: "If I change `schema.sql` I don't need to also change `001_initial_schema.sql`; they're equivalent."
- Corrected position: they are TWO files. Hand-editing one and not the other produces drift. Bootstrap-vs-001 alignment is enforced by manual review.

---

## 6. Currently Open

1. **Bug #28 (HRN scraper column-shift) — cross-reference to canonical home `data_pipeline_bible:#28`.** Per BIBLE_STRUCTURE_SPEC v5 § 5.3 G1 closure: Bug #28's symptoms manifest in the `results` table (NULL `win_payout` and `daily_double_payout`, off-by-one mis-mapped `place_payout` / `show_payout`) for rows ingested via the HRN scraper since 2026-04-30. The schema-layer manifestation is observable in this bible's domain (the `results` table per § 4.1.9), so a one-line cross-reference appears here per the cross-cutting bug Currently Open scope rule. The substantive description, root cause, and fix discipline live in `data_pipeline_bible:#28`. Tracked in `PHASE_5_BACKLOG.md` Phase 5.3.1 per META_PLAN v8 Appendix A.5.

2. **wr_predictions schema-vs-migration drift (`model_used` column origin missing).** The `model_used` column is referenced by migration 011's preamble (line 4) and read by `transforms.py:604` and `wr_prediction_repository.py:304/338/368`, but is not declared in any retained migration. Live DB introspection is the source of truth for current shape; the migration that added the column is unaccounted for in the retained set. Tracked for Phase 1 audit-CC verification against live `\d wr_predictions`. Triage candidate for `PHASE_5_BACKLOG.md`.

3. **Dev Aurora cluster does not exist; migrations tested against local Postgres only.** Per META_PLAN v8 § 7.12: Aurora-specific behaviors (JSONB serialization, IAM auth) cannot be caught pre-deploy until a dev Aurora is provisioned. Phase 5 triage candidate.

4. **No migration carries an explicit down-block.** The down-block convention (per META_PLAN v8 § 7.12) is forward-looking; existing 001–011 do not have one. Rollback is currently "git revert + manual cleanup" per migration. Phase 5 triage candidate.

---

## 7. Deprecated

### 7.1 Legacy `predictions` table — superseded but still read

| Field/Module | Canonical Source | Notes |
|---|---|---|
| `predictions` table | `wr_predictions` (per-style WR), `pl_predictions` (P&L), `ls_predictions` (LS enrichment); created by migration 005 (`005_three_prediction_tables.sql`) | The legacy `predictions` table was created by `001_initial_schema.sql:327` (verified by line-anchored read) and mirrored in `schema.sql:327`. Migration 005 created `wr_predictions`, `pl_predictions`, `ls_predictions` as the per-pipeline replacement (verified: zero `DROP TABLE` statements in `005_three_prediction_tables.sql`). The legacy table currently holds 6,600 rows (per META_PLAN v8 Claim 16, dashboard `counts.predictions`). It still has active readers: `prediction_router.py` (3 instantiations of `PredictionRepository` at lines 34, 61, 92, plus 1 import at line 5 = 4 references total), `race_router.py` (1 instantiation at line 277, plus 1 import at lines 272–273 = 2 references total), `dashboard_router.py:93,105` (direct SELECT for race-record summaries), `horse_router.py:66` (direct SELECT in horse-PPs query). Planned removal: Phase 5.X.Y after readers are migrated to the per-pipeline tables. Until removal, new code MUST NOT write to the legacy table (see candidate Forbidden Pattern 5.C); reads are tolerated only from the legacy router paths. |

**Note on superseded SQL constraints (per BIBLE_STRUCTURE_SPEC v5 § 5.6.4 G2 closure):**

Two prior UNIQUE constraint forms have been superseded by later migrations:

- `wr_predictions UNIQUE(entry_id)` (migration 005) → replaced by `UNIQUE(race_id, entry_id, style)` (migration 011).
- `ls_predictions UNIQUE(entry_id)` (migration 005) → replaced by `UNIQUE(race_id, entry_id, style)` (migration 010).

Per § 5.6.4 G2 closure, superseded SQL constraints qualify for a Deprecated entry **only if the superseded form persists** in the live DB schema. Migration 010 (line 36) explicitly issues `ALTER TABLE ls_predictions DROP CONSTRAINT IF EXISTS ls_predictions_entry_id_key`; migration 011 (line 64) explicitly issues `ALTER TABLE wr_predictions DROP CONSTRAINT IF EXISTS wr_predictions_unique_per_entry_model_style`. Both DROP statements were executed transactionally with the constraint replacements; the migration intent was to drop. Per the spec's "If physically dropped, NOT required — migration history is sufficient immune memory" clause, **neither superseded form qualifies for a Deprecated entry under the migration-history reading.**

The honest caveat (per drafter discretion + verification log entry per § 5.6.4 closing clause): live DB introspection (`\d wr_predictions` and `\d ls_predictions`) was not performed during this draft (no DB access from the drafting environment). If live introspection reveals that an auto-generated index from a pre-005 form (e.g., `wr_predictions_entry_id_key`) still persists alongside the post-011 constraint, the superseded form does qualify and a Deprecated entry is added. This determination is deferred to Phase 1 audit-CC verification with live DB access.

---

## 8. What Was Fixed — Do Not Revert

### 8.W.1: `wr_predictions` UNIQUE-constraint duplicate accumulation (fixed 2026-05-XX, migration 011)

**Symptom:** 157 races (~1.35% of 11,629 total) accumulated 427 duplicate prediction rows. Downstream consumers (LS softmax, ComparePage Cartesian, track_record double-counting) read both the `'core'` and `'full'` model_used variants without filtering, producing inflated counts and incorrect ensemble inputs. (Numbers quoted verbatim from migration 011 file-header comment line 14.)

**Root cause:** the pre-011 `wr_predictions` UNIQUE constraint included `model_used`, a per-horse dispatch metadata flag set by `WRInferenceService.predict_race` based on workout availability. Each horse goes through ONE model variant per inference, but when workout data lands between inference runs, the same `(race_id, entry_id, style)` accumulates a `'core'` row from the first run AND a `'full'` row from the second run. The four-column UNIQUE did not detect the conflict; both rows persisted. (Quoted from migration 011 preamble lines 4–17, verbatim where in quotes.)

**Fix:** migration 011 (`011_wr_predictions_unique_fix.sql`) ran a single transaction containing: (1) DELETE of older duplicates per `(race_id, entry_id, style)` partition, keeping the most recent by `created_at DESC, prediction_id DESC`; (2) `ALTER TABLE wr_predictions DROP CONSTRAINT IF EXISTS wr_predictions_unique_per_entry_model_style`; (3) `ALTER TABLE wr_predictions ADD CONSTRAINT wr_predictions_unique_per_entry_style UNIQUE (race_id, entry_id, style)`; (4) post-state checks via two `DO $$ … $$` blocks that `RAISE EXCEPTION` if the dedup left residual duplicates or if the new constraint is not present in `pg_constraint`. (Reproduced from migration 011 lines 27–99.)

**Why this entry exists:** dispatch metadata flags (`model_used`) record which variant ran; UNIQUE constraints describe the bibliographic grain of the row. Mixing the two creates duplicates that are silent under the constraint and propagate to downstream consumers. The discipline (candidate Forbidden Pattern § 5.A above): UNIQUE constraints over the per-pipeline prediction tables use `(race_id, entry_id, style)` only; dispatch metadata stays as plain columns.

**Conditional triggers evaluated (per BIBLE_STRUCTURE_SPEC v5 § 5.6.1.2 tertiary-state notation):**

- **if-fix-involved-migration:** FIRES. Migration 011 (`backend/database/migrations/011_wr_predictions_unique_fix.sql`).
- **if-fix-invalidated-prior-content:** DOES NOT FIRE. No prior bible content existed at fix time (pre-Phase-1).
- **if-fix-produced-Forbidden-Pattern:** FIRES. Cross-reference to candidate Forbidden Pattern § 5.A "Including dispatch metadata in UNIQUE constraints" (pending QB ratification per § 5.7).
- **if-fix-touches-multiple-bibles:** CONDITIONAL. The fix is schema-layer (canonical home: this bible) but its effects ripple through `ml_layer_architecture_bible:4` (the WR inference service writes the rows) and `api_frontend_bible:4` (downstream consumers that double-counted). The CONDITIONAL caveat: the cross-references describe where the symptoms manifested (LS softmax, ComparePage Cartesian, track_record double-count); the canonical entry — including Symptom, Root cause, Fix, and Why — lives only here per the cross-cutting bug scope rule's no-duplication mandate.

### 8.W.2: `ls_predictions` promoted from stub to first-class with style-aware UNIQUE (fixed 2026-05-01, migration 010)

**Symptom:** `ls_predictions` had been an orphan since the LS service was introduced. The `insert_prediction` repo method was never called; LS data was written as enrichment columns on `wr_predictions` (`longshot_alert`, `longshot_prob`, `ensemble_win_prob`, etc.). When Tony's revised architecture (2026-05-01 per migration 010 preamble line 8) elevated LS to a first-class model with its own ranking, the existing schema lacked the columns needed for parity with `wr_predictions` (no `style`, no `market_prob`, no `edge_pct`, no `is_top_pick`, no `morning_line_implied_prob`) and the single-column `UNIQUE(entry_id)` precluded style differentiation.

**Root cause:** the original 005-era declaration of `ls_predictions` was a stub (per migration 005 line 60-comment `LS Predictions (stub)`). The schema was authored before LS was a first-class pipeline.

**Fix:** migration 010 (`010_ls_predictions_first_class.sql`) ran a single transaction containing: (1) `ALTER TABLE ls_predictions ADD COLUMN IF NOT EXISTS` for `style VARCHAR(50) DEFAULT 'general'`, `market_prob NUMERIC`, `edge_pct NUMERIC`, `is_top_pick BOOLEAN DEFAULT FALSE`, `morning_line_implied_prob NUMERIC`; (2) `ALTER TABLE ls_predictions DROP CONSTRAINT IF EXISTS ls_predictions_entry_id_key` plus `DROP INDEX IF EXISTS ls_predictions_entry_id_key`; (3) `ALTER TABLE ls_predictions ADD CONSTRAINT ls_predictions_unique_per_entry_style UNIQUE (race_id, entry_id, style)`. The constraint switch was safe because existing rows at migration time = 0 (per migration 010 preamble line 17).

**Why this entry exists:** when a stub table is promoted to a first-class member of a family, both the column shape and the UNIQUE shape are part of the promotion. Either alone is incomplete: column-only leaves the constraint blocking multi-style writes; constraint-only leaves the rows shapeless. Promotions are atomic.

**Conditional triggers evaluated:**

- **if-fix-involved-migration:** FIRES. Migration 010 (`backend/database/migrations/010_ls_predictions_first_class.sql`).
- **if-fix-invalidated-prior-content:** DOES NOT FIRE. No prior bible content existed at fix time.
- **if-fix-produced-Forbidden-Pattern:** DOES NOT FIRE. The fix established a forward-going shape rather than codifying a prohibition.
- **if-fix-touches-multiple-bibles:** CONDITIONAL. Schema-layer fix (canonical home: this bible) with downstream implications for `ml_layer_architecture_bible:4` (LS pipeline now writes to `ls_predictions` in addition to continuing the `wr_predictions` enrichment). The CONDITIONAL caveat: the LS pipeline transition mode — writing to both `ls_predictions` and the WR-enrichment columns simultaneously to keep frontend reads working — is documented in `ml_layer_architecture_bible:4`, not here. The schema-layer entry covers the table shape only.

### 8.W.3: `pace_delta` backfill keyed on the wrong end-of-race column (fixed via migration 009, date per migration filename)

**Symptom:** initial `pace_delta` values computed by migration 005 (`005_backfill_pace_delta.sql`, the first of the duplicate-005 pair) were systematically incorrect because the end-of-race position column choice did not match the canonical definition.

**Root cause:** the column used by 005 for the end-of-race position differed from the canonical column (precise pre-005 vs post-009 column identification is in the migration files; the 009 file's preamble names the corrected column per the operator's revised definition).

**Fix:** migration 009 (`009_backfill_pace_delta_v2.sql`) re-backfills `past_performances.pace_delta` from the corrected source column.

**Why this entry exists:** the `pace_delta` feature is consumed by training and inference paths. A silently miscomputed feature degrades model performance without signaling the cause. The discipline (candidate Common Mistake § 5.H above): when adding or backfilling a derived feature, document which source column drives the derivation in the migration file's preamble. Future re-backfills then have an explicit reference point.

**Conditional triggers evaluated:**

- **if-fix-involved-migration:** FIRES. Migration 009 (`backend/database/migrations/009_backfill_pace_delta_v2.sql`).
- **if-fix-invalidated-prior-content:** DOES NOT FIRE. No prior bible content at fix time.
- **if-fix-produced-Forbidden-Pattern:** DOES NOT FIRE (no Forbidden Pattern produced). The fix produced candidate Common Mistake § 5.H ("I'll backfill from `finish_call_position`...").
- **if-fix-touches-multiple-bibles:** CONDITIONAL. The schema-layer fix is local to `past_performances`; the feature semantics affect `feature_provenance_bible:4` (pace_delta is a documented feature) and `ml_layer_architecture_bible:4` (training data quality). The CONDITIONAL caveat: the pace_delta semantics — what it represents, why the corrected column is canonical — live in `feature_provenance_bible:4`. The schema-layer entry covers the backfill mechanics only.

---
