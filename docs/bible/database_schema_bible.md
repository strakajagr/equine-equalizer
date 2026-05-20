# Database & Schema Bible

**Document:** database_schema_bible
**Phase:** 1 (Bible) — deliverable 2 of 7 (drafting-order numbering per BIBLE_STRUCTURE_SPEC v6 § 8.2)
**Status:** LOCKED v1-patched-e (2026-05-12) — Phase A D6 bundled bible patches per F.4 surgical-patch pattern under Tier 2 ceremony cap; 1 patch landed (DS-1 workouts source-column schema-evolution candidate per Phase A handoff § 2.13; DS-2 matcher-Lambda sparse-invocation flag routed to architecture_overview § 3.12 AO-3 per best-practice — architectural/operational rather than schema-shape); supersedes LOCKED v1-patched-d3 (2026-05-11)
**Author:** CC (v1-patched-d2: drafting under Tier 3 verification discipline; v1-patched-d3: drafting under EE Bible Upstream-Correction Cycle sub-cycle 4 of 4 per R10 Option A 4th sub-cycle authorization — terminal sub-cycle; QB orchestrated)
**Date:** 2026-05-05
**Locked:** 2026-05-11 (v1-patched-d3 via cross-bible re-lock ceremony at parent EE Bible Upstream-Correction Cycle exit per R14.3 Option B + R36 Option A; v1-patched-d2 2026-05-05; v1-patched-d1 patch closed D-1 MINOR; v1-patched-d2 re-audit verdict READY FOR LOCK; v1-patched-d3 cohort-locked audit-CC RATIFY disposition per D1 + D2 + D3 sub-cycle 4 outputs)

**Revision history:**
- v1-patched-e (2026-05-12): Phase A D6 bundled bible patches dispatch. **Override disclosure (Q5 ratification):** D6 surgical patches per F.4 pattern under Tier 2 ceremony cap per Phase A entry directive. UC § 7.2 step 4 per-bible patch-CC convention explicitly overridden by ceremony cap. Rationale: D6 documents Phase A operational findings into bibles per Phase A re-dispatch venue (R14.2 Option A scope); not a running cross-bible-cross-reference-freeze UC cycle. Letter bump d3 → e clean break from d-series (d-series concluded as terminal sub-cycle of parent UC cycle at 2026-05-11; new letter for new dispatch class). **1 patch applied** per Phase A handoff `docs/operations/PHASE_A_HANDOFF_2026-05-12.md` § 2.13: DS-1 NEW workouts source-column schema-evolution candidate note at § 4.1.8 + entry in § 6 Currently Open. **DS-2 routing decision** per CC venue determination: matcher-Lambda sparse-invocation flag (per Phase A handoff § 2.12) routed AWAY from database_schema_bible to architecture_overview § 3.12 AO-3 ORPHAN consolidated subsection (Appendix B) — content is architectural/operational (matcher Lambda invocation cadence + Phase B classification candidate), not schema-shape. Cross-bible cross-reference created: § 6 Currently Open new entry cross-links `data_pipeline_bible:4.4` (operational source inventory; D6 v1-patched-e patch). Cross-bible cross-reference freeze status: NOT re-engaged for D6 (Tier 2 ceremony cap pattern); per-bible audit-CC tier not invoked at D6 scope.
- v1 (2026-05-05): initial CC draft per `database_schema_bible_v1_drafting_spec.md` (QB-authored, paste-ready 2026-05-05). Companion verification log at `_audit/database_schema_bible_v1_verification.md`. Tier: 3 per META_PLAN v9 § 4.1 + § 6.5.
- v1-patched (2026-05-05): surgical patch per Tony's ratifications on 2026-05-05 covering audit-CC findings D-3.1 BLOCKER + D-1.1 + D-1.2 + D-4.1 + D-4.2 + D-8 + D-9 + D-10 + Q1 + Q2.d + Q3.1 + Q3.2 + Q3.3.c. See `database_schema_bible_v1_audit.md` for the audit driving this patch and `_meta/database_schema_bible_v1_drafting_spec.md` for the original drafting spec.
- v1-patched-d1 (2026-05-05): single-line surgical patch per Tony's D1.a ratification on 2026-05-05 covering re-audit-CC finding D-1 (stale § 5.3 cross-reference at § 5 lead paragraph). See `database_schema_bible_v1_reaudit.md` Section D for the finding driving this patch.
- v1-patched-d2 (2026-05-06): surgical patch landing `angle_stats` substrate per UPSTREAM-CORRECTION class routing from Data Pipeline Bible v1-patched-a verification log § F.4 (Tony ratified 2026-05-06). § 3.1 enumeration updated 14-table → 15-table; new § 4.1.15 sub-section codifies `angle_stats` schema (column list + types + constraints) per § 5.6.4 mandatory + conditional fields. PHASE 1 empirical substrate captured live from production DB (or asserted-from-handler-INSERT-tuples-not-empirically-verified per CC's PHASE 1 Approach disposition). § 6 Currently Open updated per § 5.3 + § 6.1 convention if applicable. Bible re-locks at v1-patched-d2 LOCKED via subsequent lock-CC paste-prompt; Data Pipeline Bible's § 4.1.7 cross-reference + verification log § F.4 re-ratify in a separate small Data Pipeline patch cycle after this lock.
- v1-patched-d2 LOCKED (2026-05-06): Phase 1 deliverable 2 of 7 re-LOCKED. UPSTREAM-CORRECTION patch closing F.4 from Data Pipeline Bible v1-patched-a verification log. `angle_stats` substrate landed at § 3.1 enumeration (14-table → 15-table) + new § 4.1.15 sub-section (column substrate asserted-from-INSERT-tuples per PHASE 1 Approach B fallback; PK/FK/JSONB/INDEX substrate asserted-disposition-pending-credential-authorized-cycle) + § 6 Currently Open entry (formalization-via-migration is Phase 5 backlog scope; re-verification at next credential-authorized cycle is follow-up patch entry, not lock-blocking). Skip-audit ratified by Tony per the UPSTREAM-CORRECTION class scope. Bible joins Architecture Overview v3 LOCKED (2026-05-05) + Data Pipeline Bible v1-patched-b LOCKED (2026-05-06) as locked Phase 1 substrate; D&S Bible re-lock supersedes the v1-patched-d1 LOCKED state (2026-05-05).

- v1-patched-d3 (2026-05-11): UPSTREAM-CORRECTION patch cycle Database & Schema Bible UC (sub-cycle 4 of 4 under parent EE Bible Upstream-Correction Cycle, per R10 Option A 4th sub-cycle authorization 2026-05-11 — **terminal sub-cycle**). Scope per R14.3 Option B: Aurora-residual scan + cross-bible re-lock ceremony substrate preparation. **3 patches applied (Pattern A bundle D1+D2+D3):** D1 Aurora-residual scan in this bible's body — A3-class **VERIFY-ONLY-CLEAN disposition** (per grep -n -i -E 'aurora|cluster|dbcluster' against this bible's body 2026-05-11T15:16:40Z UTC returned 1 match at § 3.3 line 159: substrate-correct denial-of-Aurora claim "NOT an Aurora cluster" reinforcing v3-patched-b § 3.3 substrate-correct standalone-Postgres claim + V28 RDS substrate confirmation `aws rds describe-db-instances` returning equine-db Engine postgres 16.6 + DBClusterIdentifier null + `aws rds describe-db-clusters` returning empty equine cluster list; legitimate substrate-correct narrative PRESERVED per § 4.17 banked Lesson; no surgical row patches required); D2 § 1.3 cross-bible cross-reference index refresh — **NOT APPLICABLE** (this bible has no § 1.3 sub-section per BIBLE_STRUCTURE_SPEC v6 § 8.2 structural variation; ToC scan verified 2026-05-11T15:16:40Z UTC; cross-bible cross-references are embedded inline within § 1.X narrative + per-table § 4.1.X cross-references, NOT enumerated in a dedicated § 1.3 sub-section); D3 cross-bible re-lock ceremony substrate preparation — header status + revision history + footer updated to reflect v1-patched-d3 DRAFT state pending cohort-locked audit-CC dispatch + cross-bible re-lock ceremony scope disclosure. **B5 naming convention** per ratification: v1-patched-d2 → v1-patched-d3 sub-letter continuation follows v1-patched-d1 → v1-patched-d2 precedent (single letter then digit suffix as sub-letter continuation; d3 fits substrate convention; no naming-ratification halt triggered). Sub-cycle 4 is terminal sub-cycle of parent cycle; cohort-locked audit-CC dispatch is next QB output after SP-4 ratification per amended R15 ("cohort-locked audit-CC dispatches after all-in-cycle-drafting-complete (after sub-cycle 4 close)"). Cross-bible cross-reference freeze: LIFTED via Tony Option α 2026-05-09 (parent EE Bible Upstream-Correction Cycle scope); **freeze re-locks at sub-cycle 4 close as part of cross-bible re-lock ceremony per R14.3 Option B** — re-lock ceremony fires at cohort-locked audit-CC PASS + Tony lock disposition; sub-cycle 4 drafting prepares re-lock ceremony substrate but does NOT execute re-lock. Companion verification log NEW: `_audit/database_schema_bible_v1_patched_d3_verification.md` (DRAFT pending cohort-locked audit-CC per amended R15; V28 substrate-stability re-confirmation; Aurora-residual scan determination per D1; sub-cycle 4 terminal-cycle documentation). v1-patched-d2 lock-state companion verification log preserved verbatim per banked Lesson § 4.17 (locked bibles preserve drafting-time historical context); only v1-patched-d2 → v1-patched-d3 delta captured in NEW log per surgical-cosmetic-patch convention precedent (v1-patched-d2 was itself a surgical UPSTREAM-CORRECTION close cycle precedent). **v1-patched-d3 lock posture: pending cohort-locked audit-CC dispatch + Tony lock disposition at cross-bible re-lock ceremony.**

**Anchored on:** META_PLAN v9 (LOCKED 2026-05-05) + BIBLE_STRUCTURE_SPEC v6 (LOCKED 2026-05-05) + Architecture Overview v3 (LOCKED 2026-05-05).

**Companion verification log:** `_audit/database_schema_bible_v1_verification.md`.

---

## 1. Scope of this bible

Database & Schema Bible answers: **"what tables exist, what columns are canonical, how do migrations work, what JSONB conventions apply?"** Audience: anyone touching schema, repositories, migrations, or repository SQL — including operators reading raw SQL during incident triage and Phase 1+ drafters cross-referencing per-table writers/readers.

This bible is **reference-style** (look up by table or column name). Other bibles are flow-narrative (e.g., `data_pipeline_bible:4.1` walks per-flow data movement) or composition-narrative (e.g., `ml_layer_architecture_bible:4` composes ranker → calibrator → override stages). When you need to know "what columns does `past_performances` have?" you read here; when you need "how does the daily LS inference write to `ls_predictions`?" you read `data_pipeline_bible:4.1`.

**Boundary statements — what this bible documents:**
- Domain-schema table inventory (15 tables) + 1 materialized view, with per-table column lists, primary keys, UNIQUE / FK / index declarations, and JSONB column shapes (§ 3, § 4.1).
- Migration discipline — file-naming format, the duplicate-005 case, the runner-internal `schema_migrations` mechanism, rollback format, and migration-testing posture (§ 4.2).
- JSONB conventions, UNIQUE-constraint design rules, and cross-table FK conventions surfaced from substrate analysis (§ 5).

**Boundary statements — what this bible does NOT document:**
- Per-flow data movement (which Lambda or ECS task writes which table, on what schedule, with what error-handling discipline) → `data_pipeline_bible:4.1`.
- Per-feature consumption from the schema (which model uses which column; what training-vs-inference parity guarantees apply per column) → `feature_provenance_bible:4`.
- Model-registry semantics (active-row selection, multi-active-row reality of `model_versions` per META_PLAN v9 § 9.13, calibration-sidecar S3 layout) → `ml_layer_architecture_bible:3.1` for registry; `ml_layer_architecture_bible:4.3` for calibration.
- Per-route reads (which HTTP route reads which table, response-shape contracts) → `api_frontend_bible:4.1`.
- Per-runtime topology (Lambda ↔ table writer mapping, EventBridge schedule, RDS instance metadata) → `architecture_overview:3.1` (Lambda inventory), `architecture_overview:3.3` (RDS), `architecture_overview:3.6` (EventBridge).

When sources conflict, source-priority hierarchy applies per META_PLAN v9 § 4.5: Tier 1 (live AWS state) > Tier 2 (live API endpoints) > Tier 3 (live database state) > Tier 4 (working-tree code post-baseline 87dec36) > Tier 5 (operator-stated history) > Tier 6 (`EE_CURRENT_STATE_DUMP.md` baseline) > Tier 7 (session logs). For this bible's content specifically, Tier 4 (working-tree `backend/database/schema/schema.sql` + `backend/database/migrations/*.sql`) is the canonical source for declared schema; Tier 2/3 (dashboard endpoint and live DB) is canonical for row counts; Tier 1 (`equine-db` instance metadata) is canonical for engine/version/runtime context (cross-referenced from `architecture_overview:3.3`, not duplicated here).

Cross-cutting topics that span multiple bibles cite the canonical-home bible per BIBLE_STRUCTURE_SPEC v6 § 5.3. Schema-design discipline (e.g., the migration 011 UNIQUE-constraint design lesson) is canonically homed here; per-column feature-provenance discipline is canonically homed in `feature_provenance_bible`; data-acquisition discipline (e.g., HRN scraper column-shift bug producing NULL `results.win_payout`) is canonically homed in `data_pipeline_bible`.

---

## 2. Definitions

Terminology specific to this bible's domain. Acronyms defined elsewhere (WR / PL / LS, Gonzo Sauce, Active vs Inactive Lambda) are referenced from `architecture_overview:2`, not redefined here.

- **Table.** A PostgreSQL relation declared via `CREATE TABLE`. Persistent storage for one row per domain entity. EE has 15 domain tables (§ 3.1). Tables are distinct from materialized views: a table holds its own rows; a materialized view holds rows derived from a query against other tables, refreshed on demand.
- **Materialized view.** A PostgreSQL relation declared via `CREATE MATERIALIZED VIEW`. Stores the result of a query against base tables. Unlike a view, the rows are physically stored and queryable without re-executing the underlying query; unlike a table, the rows must be refreshed manually (`REFRESH MATERIALIZED VIEW <name>`) when the base tables change. EE has 1 materialized view: `trainer_stats` (§ 3.2). **This table-vs-matview distinction governs § 4.1 enumeration scope: § 4.1 enumerates `CREATE TABLE` declarations only. The matview is documented at § 3.2, not at any § 4.1.X position.**
- **Migration.** A `.sql` file in `backend/database/migrations/` that evolves the schema from one declared state to the next. Migrations are applied in lexical-sort order by the runner (§ 4.2.3) and tracked by filename in the runner-internal `schema_migrations` table. EE has 12 migration files at lock (§ 4.2.1).
- **JSONB shadow.** A semi-structured payload stored in a JSONB column whose shape is declared by the writing code (Tier 4 substrate) rather than by the schema's column definition. The schema declares the column type as `JSONB` and optionally a default (e.g., `JSONB DEFAULT '{}'`); the actual key set, value types, and shape conventions live in the producing code. EE has 6 JSONB columns across 5 tables (§ 5.2). Reading the JSONB shape requires reading the writer (e.g., `wr_inference_service.py` for `wr_predictions.feature_importance`).
- **Canonical column.** A column whose semantic meaning, type, and downstream contract are stable across writers and readers. Canonical columns appear unchanged in the corresponding `backend/models/canonical.py` dataclass (per `architecture_overview:4.1`). Non-canonical columns may exist as denormalization aids (e.g., `past_performances.trainer_name` is denormalized from `trainers.trainer_name` via FK chain — backfilled by migration 007).
- **Primary writer.** The Lambda function or service module that produces rows in a given table during normal production operation. Some tables have one primary writer (e.g., `wr_predictions` written by `equine-wr-inference` Lambda); others have multiple paths (e.g., `model_versions` written by training tasks AND by manual operator scripts via the ingestion Lambda's admin actions).
- **Primary reader.** The router or service module that consumes rows from a given table during normal production operation. Per § 1's boundary statement, per-route reader detail belongs to `api_frontend_bible:4.1`; this bible enumerates primary readers at the module level (e.g., "primary reader: `dashboard_router.py` for race-record summaries; per-route detail at `api_frontend_bible:4.1`").
- **`schema_migrations` table.** Runner-internal book-keeping table created at first runner invocation by `migrate.py:ensure_migrations_table`. Holds one row per applied migration filename. NOT enumerated in the 15-table domain count — it is infrastructure, not domain. Documented at § 4.2.3.

When sources conflict, source-priority hierarchy applies per META_PLAN v9 § 4.5 (see § 1).

---

## 3. Schema overview

### 3.1 15 domain tables (decomposed list)

EE's domain schema declares **15 tables**, decomposed as **11 in `backend/database/schema/schema.sql` + 3 in `backend/database/migrations/005_three_prediction_tables.sql` + 1 created out-of-band (no tracked migration declares it at lock)** (verified 2026-05-05 for the 11+3 in tracked sources per companion verification log claims V1-1 + V1-1a; the +1 out-of-band table `angle_stats` surfaced via Data Pipeline Bible v1-patched-a verification log § F.4 UPSTREAM-CORRECTION class and is documented at § 4.1.15 + companion verification log Section C V1-18 / V1-19 / V1-20 of this bible's v1-patched-d2 patch cycle). See § 3.3 for the relationship between `schema.sql` and `001_initial_schema.sql`.

**11 tables in `backend/database/schema/schema.sql`** (CREATE TABLE order):

| # | Table | Purpose |
|---|---|---|
| 1 | `tracks` | Reference: physical racetracks (track code, name, location, surfaces, claiming-price floor). |
| 2 | `horses` | Reference: individual horses with pedigree (sire/dam/dam_sire) and registration. Self-referential FKs allow ancestor lookup. |
| 3 | `trainers` | Reference: trainer entities (name, license number, country). |
| 4 | `jockeys` | Reference: jockey entities (name, license number, apprentice flag). |
| 5 | `races` | One row per scheduled race (track, date, race number, distance, surface, conditions, weather, going-stick reading). |
| 6 | `entries` | One row per (race, horse) tuple — a horse entered in a race (jockey, trainer, post position, weight, equipment/medication, scratched flag). |
| 7 | `past_performances` | Historical PP-line data: a horse's prior race result with conditions, fractional times, running-style derivatives, denormalized trainer name. The richest table in the schema (~70 columns). |
| 8 | `workouts` | Logged workout times for a horse (track, date, distance, time, surface, condition, bullet-of-day flag). |
| 9 | `results` | Settled-race finish data per entry (finish position, lengths behind, fractional positions, payouts including win/place/show/exacta/trifecta/superfecta/daily double). |
| 10 | `predictions` | Legacy predictions table (per-entry win/place/show probability, confidence, value flags, JSONB feature importance). Now superseded by per-pipeline tables in migration 005. See § 7.1. |
| 11 | `model_versions` | Model registry: per-version metadata, training window, evaluation metrics, JSONB feature list / hyperparameters, S3 artifact path, active flag. Per-`model_type` active-row semantics added by migration 005 (one active row per type, not one globally). |

**3 tables in `backend/database/migrations/005_three_prediction_tables.sql`** (the "three prediction tables", added 2026-03-18):

| # | Table | Purpose |
|---|---|---|
| 12 | `wr_predictions` | WR (win-and-rank) per-entry inference output: win/place/show probability, predicted rank, value flag, JSONB feature importance, ground-truth back-fill columns. |
| 13 | `pl_predictions` | PL (place-and-show) per-entry inference output: win probability, predicted EV, edge-pct, kelly fraction, value flags. |
| 14 | `ls_predictions` | LS (longshot) per-entry inference output: ensemble win probability, longshot-alert flag, multi-component scores (XGB rank, RF longshot prob, LSTM trajectory, calibrated win prob, Bayesian angle EV). Migration 010 added first-class columns and replaced the entry-id-only UNIQUE with `(race_id, entry_id, style)`.

**1 table created out-of-band (no tracked migration declares it at lock):**

| # | Table | Purpose |
|---|---|---|
| 15 | `angle_stats` | Pre-computed Bayesian-angle wins/starts aggregations per (angle_name, trainer_name, track_code) tuple, written by `equine-ingestion` Lambda's `refresh_angle_stats` action (`backend/lambdas/ingestion/handler.py:94-188`) via DELETE + 6× INSERT cycle, read by `equine-ls-inference` service module (`backend/services/ls_inference_service.py:528-573`) for per-entry angle scoring. Surfaced via Data Pipeline Bible v1-patched-a verification log § F.4 UPSTREAM-CORRECTION class. See § 4.1.15. |

**Runner-internal table (NOT enumerated in the 15):** `schema_migrations` is created at runtime by `backend/database/migrations/migrate.py:ensure_migrations_table` (see § 4.2.3). It is infrastructure for the migration runner, not domain schema, so does not count in § 3.1's enumeration.

### 3.2 1 materialized view (`trainer_stats`)

EE declares **1 materialized view: `trainer_stats`**, created by `backend/database/migrations/008_create_trainer_stats.sql` (verified 2026-05-05; companion verification log claim V1-2).

**Purpose.** Aggregates career win-rate, in-the-money rate, layoff (≥30 days off) win-rate, Lasix-first-time win-rate, and claimed-horse win-rate by trainer name, computed from `past_performances`. Used as a feature input by the inference-side feature-engineering service.

**Definition (from migration 008):**

```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS trainer_stats AS
SELECT
    trainer_name,
    COUNT(*) AS total_starts,
    SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END) AS wins,
    ROUND(SUM(...)::numeric / NULLIF(COUNT(*), 0), 4) AS win_rate,
    SUM(CASE WHEN finish_position <= 3 THEN 1 ELSE 0 END) AS itm,
    -- (itm_rate, layoff_win_rate, lasix_win_rate, claimed_win_rate omitted for brevity)
FROM past_performances
WHERE trainer_name IS NOT NULL
  AND finish_position IS NOT NULL
  AND finish_position < 90
GROUP BY trainer_name
HAVING COUNT(*) >= 5;

CREATE UNIQUE INDEX IF NOT EXISTS idx_trainer_stats_name
    ON trainer_stats (trainer_name);
```

**Inclusion rule.** A trainer must have at least 5 starts in `past_performances` to appear in the view (`HAVING COUNT(*) >= 5`).

**Exclusion rule.** Rows with `finish_position` NULL or ≥ 90 are excluded from the aggregations. Codes 1–30 are valid finishes; codes ≥ 90 mean DNF / pulled / vet scratch (per migration 009 documentation; consistent here for DNF exclusion).

**UNIQUE INDEX.** `idx_trainer_stats_name` on `trainer_name` enables `REFRESH MATERIALIZED VIEW CONCURRENTLY trainer_stats` if needed (PostgreSQL requires a UNIQUE index for concurrent refresh).

**Refresh discipline.** Manual: `REFRESH MATERIALIZED VIEW trainer_stats` after large data loads (per migration 008's preamble). The view does NOT auto-update when `past_performances` is INSERT'ed into; staleness drifts with each new PP row. There is no automated refresh schedule at lock — disposition is operator-driven; per-flow refresh integration into the daily ingestion pipeline is candidate Phase 5 work.

**Primary reader.** `feature_engineering_service._get_trainer_stats()` at `backend/services/feature_engineering_service.py:1124` (verified 2026-05-05); the function caches per-trainer stats in `self._trainer_stats_cache` (initialized at line 61) and queries the matview directly (`SELECT ... FROM trainer_stats WHERE trainer_name = %s`).

**Per § 2 table-vs-matview distinction: `trainer_stats` is documented at § 3.2 only. It does NOT appear at any § 4.1.X position. § 4.1 enumerates `CREATE TABLE` declarations only.** (Closes G-new-2 per drafting spec.)

### 3.3 Schema bootstrap (`backend/database/schema/schema.sql`) vs migrations

EE's schema state is the union of two sources:

1. **Bootstrap source: `backend/database/schema/schema.sql`** — declarative initial schema (extensions, 11 CREATE TABLE statements, the `predictions ↔ model_versions` FK constraint, 12 secondary indexes). 415 lines at lock.
2. **Migration source: `backend/database/migrations/*.sql`** — 12 sequenced files that evolve the schema from the initial state. The runner (`migrate.py`) tracks applied migrations in the `schema_migrations` table by filename and applies any unapplied file in lexical-sort order (§ 4.2.3).

**Bootstrap-vs-migration relationship (substrate observation, 2026-05-05).** `backend/database/schema/schema.sql` and `backend/database/migrations/001_initial_schema.sql` are **byte-identical** (`diff` returns empty; both are 415 lines; verified 2026-05-05; companion verification log claim V1-1a). Any of three operational interpretations are consistent with the substrate:

- The schema.sql file is a reference snapshot of the post-001 state for tooling that wants to run `psql -f schema.sql` against a fresh DB.
- The 001 migration file is the migration-runner-compatible packaging of schema.sql, so the runner's `schema_migrations` table records `001_initial_schema.sql` as the bootstrap entry.
- Both files coexist as parallel sources of the same content; whichever is canonical is determined by which file the deployment process actually executes.

Per § 4.5 source-priority Tier 4, the working-tree's declared schema is the union of these files plus the 11 subsequent migrations (002–011). The `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql` command returns **25 statements** (11 in schema.sql + 11 mirrored in 001_initial_schema.sql + 3 in 005_three_prediction_tables.sql); the count of **distinct domain tables is 14** (the union as a set; schema.sql and 001_initial_schema.sql declare the same 11 tables in identical text). See verification log V1-1 + V1-1a for the decomposition.

**Bootstrap-load discipline.** Either file may serve as the bootstrap source. If the runner is invoked against an empty database, applying 001_initial_schema.sql via the runner records the filename in `schema_migrations` and produces the same schema state as `psql -f schema.sql`. The runner is the canonical path for production loads; `psql -f schema.sql` is a developer-environment convenience.

**Connection mechanism.** EE uses **psycopg2 direct connections** (NOT the RDS Data API). Connection string is constructed in `backend/shared/db.py` from Secrets Manager (`DB_SECRET_ARN`) or `DATABASE_URL` env-var fallback. Cross-reference `architecture_overview:3.3` for the canonical RDS instance metadata (engine `postgres`, version `16.6`, instance class `db.t4g.micro`, endpoint `equine-db.cgtuh834bttd.us-east-1.rds.amazonaws.com:5432`, database `equine_equalizer`, NOT an Aurora cluster).

---

## 4. Schema and migration detail

### 4.1 Per-table documentation

One sub-section per `CREATE TABLE` declaration. Enumeration order: schema.sql declaration order (1–11), then migration 005 declaration order (12–14). The materialized view (named at § 3.2) is documented there only, NOT at any § 4.1.X position (per § 2 table-vs-matview distinction; G-new-2 closure).

For each table: column list with types, primary key, UNIQUE constraints (where present), FK constraints (where present), JSONB columns (where present, with cross-reference to § 5.2), secondary indexes (where present), purpose, primary writers, primary readers.

#### 4.1.1 `tracks`

**Columns:**

| Column | Type | Notes |
|---|---|---|
| `track_id` | UUID | PK, default `uuid_generate_v4()` |
| `track_code` | VARCHAR(10) | UNIQUE NOT NULL |
| `track_name` | VARCHAR(100) | NOT NULL |
| `location` | VARCHAR(100) | |
| `timezone` | VARCHAR(50) | DEFAULT `'America/New_York'` |
| `surfaces` | TEXT[] | PostgreSQL array |
| `is_qualifying` | BOOLEAN | DEFAULT `false` |
| `min_claiming_price` | INTEGER | |
| `created_at` | TIMESTAMPTZ | DEFAULT `NOW()` |

**Primary key:** `track_id` (UUID).

**UNIQUE constraints:** `track_code` (single-column UNIQUE).

**Purpose.** Reference table for physical racetracks. Used as the FK target for `races.track_id` and indirectly (via `races`) for `past_performances`, `entries`, etc. The `surfaces` array enumerates available surfaces (e.g., `{'dirt','turf','synthetic'}`); `is_qualifying` flags tracks whose race results EE treats as qualifying for inclusion in production training data.

**Primary writers.** Bootstrap data loaded via seed scripts; ongoing additions via the ingestion Lambda's admin-action surface (`equine-ingestion` is INACTIVE at lock per `architecture_overview:3.1`, so additions to `tracks` are currently non-functional via that path).

**Primary readers.** Reference lookups across the schema; specifically `race_repository.py` joins `tracks` for track-context resolution, and frontend dashboard routes filter race lists by track. Per-route detail at `api_frontend_bible:4.1`.

#### 4.1.2 `horses`

**Columns:**

| Column | Type | Notes |
|---|---|---|
| `horse_id` | UUID | PK, default `uuid_generate_v4()` |
| `registration_id` | VARCHAR(50) | UNIQUE |
| `horse_name` | VARCHAR(100) | NOT NULL |
| `sire`, `dam`, `dam_sire` | VARCHAR(100) | Pedigree text fields |
| `sire_id`, `dam_id`, `dam_sire_id` | UUID | Self-referential FKs to `horses(horse_id)` |
| `foaling_date` | DATE | |
| `country_of_origin` | VARCHAR(10) | DEFAULT `'USA'` |
| `sex`, `color` | VARCHAR(10/50) | |
| `created_at`, `updated_at` | TIMESTAMPTZ | DEFAULT `NOW()` |

**Primary key:** `horse_id` (UUID).

**UNIQUE constraints:** `registration_id` (single-column UNIQUE).

**FK constraints:** `sire_id`, `dam_id`, `dam_sire_id` are self-referential FKs to `horses(horse_id)` (allowing pedigree lookup without joins to a pedigree table).

**Purpose.** Reference table for individual horses with pedigree pointers. The text fields `sire` / `dam` / `dam_sire` hold human-readable names; the corresponding `_id` columns hold UUID FKs when the ancestor is itself in the horses table (e.g., when both a horse and its sire have run in EE-tracked races).

**Primary writers.** Ingestion pipelines populate `horses` from Equibase race-card and PP fetches.

**Primary readers.** Cross-referenced from `entries`, `past_performances`, `workouts`, `results`, all prediction tables. Per-route detail at `api_frontend_bible:4.1`.

#### 4.1.3 `trainers`

**Columns:**

| Column | Type | Notes |
|---|---|---|
| `trainer_id` | UUID | PK, default `uuid_generate_v4()` |
| `trainer_name` | VARCHAR(100) | NOT NULL |
| `license_number` | VARCHAR(50) | |
| `country` | VARCHAR(10) | DEFAULT `'USA'` |
| `created_at` | TIMESTAMPTZ | DEFAULT `NOW()` |

**Primary key:** `trainer_id` (UUID).

**UNIQUE constraints:** None declared.

**Purpose.** Reference table for trainer entities. Note: `trainer_name` is also denormalized into `past_performances.trainer_name` for query performance — backfilled by migration 007 via the join path PP → entries → races → trainers (per `007_backfill_trainer_name.sql` preamble).

**Primary writers.** Ingestion pipelines from Equibase data.

**Primary readers.** `entries.trainer_id` FK target; the trainer-statistics matview (§ 3.2) aggregates by `past_performances.trainer_name`, NOT by `trainers.trainer_id` directly — the join is denormalized for performance.

#### 4.1.4 `jockeys`

**Columns:**

| Column | Type | Notes |
|---|---|---|
| `jockey_id` | UUID | PK, default `uuid_generate_v4()` |
| `jockey_name` | VARCHAR(100) | NOT NULL |
| `license_number` | VARCHAR(50) | |
| `country` | VARCHAR(10) | DEFAULT `'USA'` |
| `is_apprentice` | BOOLEAN | DEFAULT `false` |
| `created_at` | TIMESTAMPTZ | DEFAULT `NOW()` |

**Primary key:** `jockey_id` (UUID).

**UNIQUE constraints:** None declared.

**Purpose.** Reference table for jockey entities. The `is_apprentice` flag drives the apprentice-allowance logic in `entries.apprentice_allowance`.

**Primary writers.** Ingestion pipelines from Equibase data.

**Primary readers.** `entries.jockey_id` FK target.

#### 4.1.5 `races`

**Columns (24 columns):**

| Column | Type | Notes |
|---|---|---|
| `race_id` | UUID | PK, default `uuid_generate_v4()` |
| `track_id` | UUID | NOT NULL, FK to `tracks(track_id)` |
| `race_date` | DATE | NOT NULL |
| `race_number` | INTEGER | NOT NULL |
| `post_time` | TIMESTAMPTZ | |
| `distance_furlongs` | DECIMAL(4,1) | NOT NULL |
| `surface` | VARCHAR(20) | NOT NULL |
| `race_type` | VARCHAR(20) | NOT NULL — widened by migration 002 from initial declaration to handle long values (e.g., `allowance_optional_claiming` at 28 chars). See § 8.W.2. |
| `grade`, `purse`, `claiming_price` | INTEGER | |
| `race_name`, `conditions` | VARCHAR(200) / TEXT | |
| `field_size` | INTEGER | |
| `rail_position`, `going_stick_reading` | DECIMAL(4,1) / DECIMAL(4,2) | |
| `track_condition`, `moisture_level`, `weather_conditions`, `wind_direction` | VARCHAR(10–50) | |
| `track_variant`, `temperature`, `wind_speed` | INTEGER | |
| `off_turf` | BOOLEAN | DEFAULT `false` |
| `equibase_race_id` | VARCHAR(100) | UNIQUE |
| `created_at` | TIMESTAMPTZ | DEFAULT `NOW()` |

**Primary key:** `race_id` (UUID).

**UNIQUE constraints:** `equibase_race_id` (single-column UNIQUE), and the natural-key composite `UNIQUE(track_id, race_date, race_number)`.

**FK constraints:** `track_id` → `tracks(track_id)`.

**Secondary indexes:** `idx_races_date` on `(race_date)`, `idx_races_track_date` on `(track_id, race_date)`.

**Purpose.** One row per scheduled race. The natural-key UNIQUE `(track_id, race_date, race_number)` enforces that a track cannot run two race-numbered-N races on the same date. The Equibase-side identifier is preserved in `equibase_race_id` for cross-source joins.

**Primary writers.** Ingestion pipelines from Equibase race-card fetches (the `equine-ingestion` Lambda is INACTIVE at lock per `architecture_overview:3.1`; daily race-card ingestion fires-and-fails — see `architecture_overview:6` Currently Open).

**Primary readers.** Cross-referenced from all race-context tables; consumed directly by all 3 inference services and by dashboard/race-detail HTTP routes. Per-route detail at `api_frontend_bible:4.1`.

#### 4.1.6 `entries`

**Columns (28 columns):**

| Column | Type | Notes |
|---|---|---|
| `entry_id` | UUID | PK, default `uuid_generate_v4()` |
| `race_id` | UUID | NOT NULL, FK to `races(race_id)` |
| `horse_id` | UUID | NOT NULL, FK to `horses(horse_id)` |
| `trainer_id` | UUID | NOT NULL, FK to `trainers(trainer_id)` |
| `jockey_id` | UUID | FK to `jockeys(jockey_id)` (nullable) |
| `post_position` | INTEGER | NOT NULL |
| `program_number` | VARCHAR(5) | |
| `morning_line_odds` | DECIMAL(8,2) | |
| `weight_carried`, `allowance_weight`, `apprentice_allowance` | INTEGER | |
| `lasix`, `lasix_first_time`, `bute` | BOOLEAN | DEFAULT `false` |
| `blinkers_on`, `blinkers_off`, `blinkers_first_time`, `tongue_tie`, `bar_shoes`, `front_bandages`, `mud_caulks` | BOOLEAN | DEFAULT `false` |
| `equipment_change_from_last`, `medication_change_from_last` | BOOLEAN | DEFAULT `false` |
| `is_scratched` | BOOLEAN | DEFAULT `false` |
| `scratch_reason` | VARCHAR(200) | |
| `is_entry` | BOOLEAN | DEFAULT `false` (the racing-form "coupled entry" flag, distinct from `is_scratched`) |
| `created_at`, `updated_at` | TIMESTAMPTZ | DEFAULT `NOW()` |

**Primary key:** `entry_id` (UUID).

**UNIQUE constraints:** `UNIQUE(race_id, horse_id)` — one row per (race, horse) tuple. A horse cannot be entered twice in the same race.

**FK constraints:** `race_id` → `races(race_id)`; `horse_id` → `horses(horse_id)`; `trainer_id` → `trainers(trainer_id)`; `jockey_id` → `jockeys(jockey_id)` (nullable).

**Secondary indexes:** `idx_entries_race` on `(race_id)`, `idx_entries_horse` on `(horse_id)`.

**Purpose.** One row per (race, horse) entry — captures the "this horse will race in this race" record with all per-entry connection data (jockey, trainer, weight, equipment, medication, scratched flag). Fields like `blinkers_first_time`, `lasix_first_time`, `equipment_change_from_last` carry handicapping signal that downstream feature engineering consumes.

**Primary writers.** Ingestion pipelines from Equibase race-card fetches. Scratch updates also flow through this table.

**Primary readers.** All 3 inference services (`equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference` per `architecture_overview:3.1`) consume entries via `entry_repository.py`. Frontend race-detail routes also read entries. Per-route detail at `api_frontend_bible:4.1`.

#### 4.1.7 `past_performances`

**Columns (~70 columns).** This is the richest table in the schema. Selected canonical columns (full list at `backend/database/schema/schema.sql:145-266`):

- **Identity:** `pp_id` (PK UUID), `horse_id` (FK to `horses`, NOT NULL), `race_id` (FK to `races`, nullable — populated for current entries' PPs only).
- **Race identification (denormalized, since not all PPs link to an EE-tracked race):** `race_date` (NOT NULL), `track_code`, `race_number`, `race_start_number`.
- **Race conditions:** `distance_furlongs`, `surface`, `race_type`, `claiming_price_entered`, `claiming_price_taken`, `was_claimed`, `purse`, `field_size`, `track_condition`, `moisture_level`, `track_variant`, `going_stick_reading`, `temperature`, `weather_conditions`, `wind_speed`, `wind_direction`, `off_turf`.
- **Connections:** `jockey_name`, `trainer_name` (denormalized; backfilled by migration 007), `previous_trainer`, `trainer_change`, `jockey_change`, `apprentice_allowance`, `weight_carried`.
- **Medication / Equipment:** `lasix`, `lasix_first_time`, `bute`, `blinkers_on/off/first_time`, `tongue_tie`, `bar_shoes`, `front_bandages`, `mud_caulks`, `equipment_change_from_last`, `medication_change_from_last`.
- **Post and finish:** `post_position`, `finish_position`, `official_finish`, `lengths_behind`, `is_disqualified`, `photo_finish`, `nose_bob`, `disqualification_involved`, `stewards_inquiry`.
- **Speed figures:** `beyer_speed_figure`, `timeform_rating`, `equibase_speed_figure`, `winner_beyer`, `field_average_beyer`.
- **Leader fractional times:** `fraction_1`, `fraction_2`, `fraction_3`, `final_time`.
- **This horse's own fractionals:** `horse_fraction_1`, `horse_fraction_2`, `horse_fraction_3`.
- **Running positions at each call:** `call_1_position`, `call_1_lengths`, `call_2_position`, `call_2_lengths`, `call_3_position`, `call_3_lengths`, `stretch_position`, `stretch_lengths`, `finish_call_position`.
- **Pace (computed-stored):** `early_pace_figure`, `late_pace_figure`, `pace_delta` (backfilled by migration 005's pace-delta script + corrected by migration 009 to use `finish_position` instead of `finish_call_position`), `pace_scenario`, `running_style` (backfilled by migration 004; widened to VARCHAR(30) by migration 003), `early_pace_pressure` (backfilled by migration 006).
- **Race context:** `winner_name`, `second_name`, `third_name`, `winner_time`, `closing_odds`, `morning_line_that_day`, `was_favorite`, `odds_rank_in_field`, `class_rating`, `days_since_last_race`.
- **Comments:** `comment` (TEXT), `trouble_comment` (TEXT).

**Primary key:** `pp_id` (UUID).

**UNIQUE constraints:** `UNIQUE(horse_id, race_date, track_code, race_number)`. A horse has at most one PP row for a (race_date, track_code, race_number) tuple.

**FK constraints:** `horse_id` → `horses(horse_id)` NOT NULL; `race_id` → `races(race_id)` (nullable — denormalization allows PPs from races EE doesn't have full coverage of).

**Secondary indexes:** `idx_pp_horse` on `(horse_id)`, `idx_pp_horse_date` on `(horse_id, race_date DESC)`, `idx_pp_track_date` on `(track_code, race_date)`.

**Purpose.** Historical PP data — the substrate for feature engineering. The denormalized columns (`trainer_name`, `track_code`, `race_date`) allow querying without joins for performance-critical inference paths. Several columns are **computed-stored** (pace_delta, running_style, early_pace_pressure) and were populated by backfill migrations (004, 005's `005_backfill_pace_delta.sql`, 006, 009 — migration 009 superseded migration 005's pace_delta backfill because `finish_call_position` was 0%-populated; see § 4.2.1 + § 4.2.2 duplicate-005 case).

**Primary writers.** Ingestion pipelines from Equibase PP fetches (via `equine-ingestion` INACTIVE Lambda — daily fetches fire-and-fail per `architecture_overview:6`).

**Primary readers.** `feature_engineering_service.py` (the dominant consumer; ~70 columns drive feature derivation); `past_performance_repository.py`. The matview at § 3.2 aggregates from this table. Per-route detail at `api_frontend_bible:4.1`.

#### 4.1.8 `workouts`

**Columns:**

| Column | Type | Notes |
|---|---|---|
| `workout_id` | UUID | PK, default `uuid_generate_v4()` |
| `horse_id` | UUID | NOT NULL, FK to `horses(horse_id)` |
| `workout_date` | DATE | NOT NULL |
| `track_code` | VARCHAR(10) | NOT NULL |
| `distance_furlongs` | DECIMAL(4,1) | NOT NULL |
| `workout_time` | DECIMAL(6,2) | NOT NULL |
| `is_bullet` | BOOLEAN | DEFAULT `false` |
| `track_condition`, `workout_type` | VARCHAR(20) | |
| `rank_on_day`, `total_works_on_day` | INTEGER | |
| `exercise_rider` | VARCHAR(100) | |
| `created_at` | TIMESTAMPTZ | DEFAULT `NOW()` |

**Primary key:** `workout_id` (UUID).

**UNIQUE constraints:** `UNIQUE(horse_id, workout_date, track_code, distance_furlongs)`. A horse has at most one workout row for a (date, track, distance) tuple.

**FK constraints:** `horse_id` → `horses(horse_id)` NOT NULL.

**Secondary indexes:** `idx_workouts_horse` on `(horse_id)`, `idx_workouts_horse_date` on `(horse_id, workout_date DESC)`.

**Purpose.** Logged workout data — drives the WR pipeline's `has_workout_data` model dispatch flag (workout availability gates the `core` vs `full` WR variant per migration 011's preamble).

**Primary writers.** `equine-nyra-workouts` Lambda (Active per `architecture_overview:3.1`) for NYRA tracks; HRN scraper is currently broken (per `architecture_overview` Bug #7 reference; canonical home `data_pipeline_bible`).

**Primary readers.** `feature_engineering_service.py` (workout-recency features); `workout_repository.py`; the WR inference path consults workout availability for model dispatch.

**Schema-evolution candidate (DS-1 D6 v1-patched-e patch per Phase A handoff § 2.13).** The `workouts` table has no `source` column. Two daily producers feed this table via the shared `s3://equine-raw-data/workout-loads/` S3 prefix (per `data_pipeline_bible:4.4` operational source inventory): Source 3 NYRA Lambda (16:00 UTC; `*_nyra_*.json` S3 path infix) + Source 4 Equibase sibling-repo cron (07:00 UTC; non-infix S3 path). Producer attribution at the DB-row level requires substrate archaeology (S3 listing filtered to NYRA-infix vs non-NYRA-infix per A.6.f investigation). A `source VARCHAR` column on `workouts` (values like `'nyra'` / `'equibase'` / `'manual'`) would enable single-SQL-query producer attribution for future investigations. **Disposition.** D6 documentation only; implementation deferred (schema migration scope; not in Phase A). Tracked at § 6 Currently Open below.

#### 4.1.9 `results`

**Columns:**

| Column | Type | Notes |
|---|---|---|
| `result_id` | UUID | PK, default `uuid_generate_v4()` |
| `entry_id` | UUID | NOT NULL, FK to `entries(entry_id)` |
| `race_id` | UUID | NOT NULL, FK to `races(race_id)` |
| `horse_id` | UUID | NOT NULL, FK to `horses(horse_id)` |
| `finish_position` | INTEGER | NOT NULL |
| `official_finish` | INTEGER | NOT NULL |
| `is_disqualified` | BOOLEAN | DEFAULT `false` |
| `dq_from`, `dq_to` | INTEGER | DQ position swap |
| `lengths_behind`, `final_time` | DECIMAL(5,2) / DECIMAL(6,2) | |
| `beyer_speed_figure` | INTEGER | |
| `call_1_position`, `call_1_lengths`, `call_2_position`, `call_2_lengths`, `stretch_position`, `stretch_lengths` | INTEGER / DECIMAL(5,2) | |
| `win_payout`, `place_payout`, `show_payout` | DECIMAL(8,2) | |
| `exacta_payout`, `trifecta_payout`, `superfecta_payout`, `daily_double_payout` | DECIMAL(10,2) | |
| `created_at` | TIMESTAMPTZ | DEFAULT `NOW()` |

**Primary key:** `result_id` (UUID).

**UNIQUE constraints:** `UNIQUE(entry_id)` — one result row per entry.

**FK constraints:** `entry_id` → `entries(entry_id)` NOT NULL; `race_id` → `races(race_id)` NOT NULL; `horse_id` → `horses(horse_id)` NOT NULL.

**Secondary indexes:** `idx_results_race` on `(race_id)`.

**Purpose.** Settled-race finish data per entry. Records final finish (with DQ-handling via `dq_from`/`dq_to` for swap-tracking), beaten lengths, fractional positions at calls, and pari-mutuel payouts. The win/place/show/exacta/trifecta/superfecta/daily-double payout columns are populated from chart-parser output.

**Primary writers.** `equine-results` Lambda (INACTIVE at lock per `architecture_overview:3.1` — daily results fetch fires-and-fails per `architecture_overview:6` Currently Open). Production rows pre-2026-05-02 (the deactivation date) are valid. The `chart_parser.py` service module performs the actual chart parsing and INSERT logic.

**Primary readers.** Dashboard summaries (race-record counts), prediction-evaluation paths that join predictions to actuals, frontend results detail routes. Per-route detail at `api_frontend_bible:4.1`.

**Currently Open touching this table.** A cross-cutting bug (canonical home `data_pipeline_bible:#28`) currently produces NULL `results.win_payout` and `results.daily_double_payout` values for rows added since 2026-04-30 due to an HRN scraper column-shift defect. See § 6 for the cross-reference; canonical home is `data_pipeline_bible` because the prevention is a data-acquisition discipline, not a schema discipline (per BIBLE_STRUCTURE_SPEC v6 § 5.3 cross-cutting bug scope rule).

#### 4.1.10 `predictions` (legacy)

**Columns:**

| Column | Type | Notes |
|---|---|---|
| `prediction_id` | UUID | PK, default `uuid_generate_v4()` |
| `entry_id` | UUID | NOT NULL, FK to `entries(entry_id)` |
| `race_id` | UUID | NOT NULL, FK to `races(race_id)` |
| `horse_id` | UUID | NOT NULL, FK to `horses(horse_id)` |
| `model_version_id` | UUID | FK to `model_versions(model_version_id)` (added via standalone ALTER TABLE block at schema.sql:383-386 after both tables exist) |
| `win_probability`, `place_probability`, `show_probability`, `confidence_score`, `morning_line_implied_prob`, `overlay_pct` | DECIMAL(6,4) | |
| `predicted_rank`, `actual_finish` | INTEGER | |
| `is_top_pick`, `is_value_flag`, `was_win`, `was_place`, `was_show`, `exacta_hit`, `trifecta_hit` | BOOLEAN | |
| `feature_importance` | **JSONB** | See § 5.2 |
| `recommended_bet_type` | VARCHAR(50) | |
| `exotic_partners` | UUID[] | |
| `created_at` | TIMESTAMPTZ | DEFAULT `NOW()` |

**Primary key:** `prediction_id` (UUID).

**UNIQUE constraints:** `UNIQUE(entry_id)` — one prediction row per entry.

**FK constraints:** `entry_id` → `entries(entry_id)` NOT NULL; `race_id` → `races(race_id)` NOT NULL; `horse_id` → `horses(horse_id)` NOT NULL; `model_version_id` → `model_versions(model_version_id)` (declared in a standalone `ALTER TABLE predictions ADD CONSTRAINT fk_model_version` block at `backend/database/schema/schema.sql:383-386` — placed AFTER both `predictions` and `model_versions` are declared because PostgreSQL requires the FK target to exist at constraint-creation time).

**JSONB columns:** `feature_importance` JSONB (NULL allowed; no DEFAULT). Shape per § 5.2.

**Secondary indexes:** `idx_predictions_race` on `(race_id)`, `idx_predictions_date` on `(created_at)`.

**Purpose.** Legacy per-entry predictions table — the original "one model writes one row per entry" design before the per-pipeline split (migration 005). Produces the "general" prediction shape: win/place/show probability, predicted rank, confidence, value-flag, JSONB feature importance, and back-fill columns for ground-truth (`actual_finish`, `was_win`, `was_place`, `was_show`, `exacta_hit`, `trifecta_hit`).

**Status: legacy / deprecated** — see § 7.1. Live row count at lock: **6,600 rows** (verified 2026-05-05 via `GET /dashboard/metrics` `counts.predictions` = 6600; companion verification log claim V1-12).

**Primary writers.** Production write paths now route to per-pipeline tables (`wr_predictions`, `pl_predictions`, `ls_predictions`); the legacy `predictions` table is read-only at present (no production code path INSERTs to it; verification log claim V1-11 inventory check did not surface a production INSERT path).

**Primary readers.** Active readers: `prediction_router.py`, `race_router.py`, `dashboard_router.py`, `horse_router.py` plus the `prediction_repository.py` module. Per-route detail with import + instantiation + SELECT decomposition deferred to `api_frontend_bible:4.1`.

#### 4.1.11 `model_versions`

**Columns (21 columns at lock):** 17 declared in `schema.sql` + 4 added by migration 005 ALTER TABLE.

| Column | Type | Notes |
|---|---|---|
| `model_version_id` | UUID | PK, default `uuid_generate_v4()` |
| `version_name` | VARCHAR(50) | NOT NULL |
| `training_date` | TIMESTAMPTZ | NOT NULL |
| `training_data_start`, `training_data_end` | DATE | NOT NULL |
| `training_race_count` | INTEGER | |
| `exacta_hit_rate`, `trifecta_hit_rate`, `top1_accuracy`, `top3_accuracy`, `calibration_score` | DECIMAL(6,4) | Evaluation metrics |
| `feature_list` | **JSONB** | See § 5.2 |
| `hyperparameters` | **JSONB** | See § 5.2 |
| `s3_artifact_path` | VARCHAR(500) | Layout `s3://equine-model-artifacts/<family>/<version>.json` per `architecture_overview:3.4` |
| `is_active` | BOOLEAN | DEFAULT `false` |
| `notes` | TEXT | (NOT JSONB; the closest match to "metadata" but plain TEXT) |
| `created_at` | TIMESTAMPTZ | DEFAULT `NOW()` |
| `model_type` | VARCHAR(10) | DEFAULT `'wr'`, CHECK in `('wr','pl','ls')` — added by migration 005 |
| `flat_bet_roi`, `kelly_roi`, `value_bet_win_rate` | DECIMAL(8,4) / DECIMAL(8,4) / DECIMAL(6,4) | Added by migration 005 (PL-specific evaluation metrics) |

**Primary key:** `model_version_id` (UUID).

**UNIQUE constraints:** None at the table level. Migration 005 adds a partial UNIQUE INDEX `idx_active_model_per_type ON model_versions (model_type) WHERE is_active = true` (replacing a globally-active `idx_active_model` index that pre-dated the per-type architecture). The partial-UNIQUE intent is "at most one active row per `model_type`"; per META_PLAN v9 § 9.13 the live table currently holds 88 model_version rows = 45 active + 43 inactive, with multiple active rows per `model_type` despite the partial-UNIQUE — see § 6 Currently Open.

**FK constraints:** None outbound (this is the registry table; FKs target it from `predictions`, `wr_predictions`, `pl_predictions`, `ls_predictions`).

**JSONB columns:** `feature_list` JSONB (the canonical feature schema for the model version); `hyperparameters` JSONB (training-time hyperparameter snapshot). Shapes per § 5.2.

**Note on a refuted column.** `model_versions.metadata` does **NOT** exist as a column. A prior synthesis reference (banked in `database_schema_bible_v1_drafting_spec.md` § 10.2) had cited `model_versions.metadata` as a JSONB column; substrate verification (companion verification log claim V1-6) confirms the closest match is `notes` (TEXT, not JSONB). The 21-column enumeration above is the canonical state.

**Purpose.** Model registry: per-version metadata, training window, evaluation metrics (per-pipeline split via `model_type` + the PL-specific ROI columns), JSONB feature list and hyperparameters, S3 artifact path. The `is_active` flag is consulted by the inference Lambdas at warm-start to discover the active model per pipeline.

**Primary writers.** ECS Fargate training tasks (per `architecture_overview:3.2`) on training completion (`insert_model_version` at `model_version_repository.py:42`); operator-driven `set_active_model` admin action via the ingestion Lambda (`backend/lambdas/ingestion/handler.py:645` — non-functional at lock since `equine-ingestion` is INACTIVE).

**Primary readers.** All 3 inference services (`wr_inference_service.py`, `pl_inference_service.py`, `ls_inference_service.py`); `dashboard_router.py` (model-status surfaces); the legacy `inference_service.py`. The active-model selection is `get_active_model_by_type` at `model_version_repository.py:100` — per META_PLAN v9 § 9.13, this function selects an arbitrary row when multiple match a given `model_type` (no deterministic tiebreaker), surfacing the multi-active-row reality referenced in § 6.

#### 4.1.12 `wr_predictions`

**Columns:** 22 columns declared in migration 005 (`backend/database/migrations/005_three_prediction_tables.sql:5-31`):

| Column | Type | Notes |
|---|---|---|
| `prediction_id` | UUID | PK, default `gen_random_uuid()` |
| `entry_id` | UUID | NOT NULL, FK to `entries(entry_id)` |
| `race_id` | UUID | NOT NULL, FK to `races(race_id)` |
| `horse_id` | UUID | NOT NULL, FK to `horses(horse_id)` |
| `model_version_id` | UUID | FK to `model_versions(model_version_id)` |
| `win_probability`, `place_probability`, `show_probability`, `morning_line_implied_prob`, `overlay_pct` | DECIMAL(6,4) | |
| `predicted_rank`, `actual_finish` | INTEGER | |
| `confidence_score` | DECIMAL(8,4) | |
| `is_top_pick`, `is_value_flag`, `was_win`, `was_place`, `was_show`, `exacta_hit`, `trifecta_hit` | BOOLEAN | DEFAULT `FALSE` |
| `recommended_bet_type` | VARCHAR(20) | |
| `exotic_partners` | UUID[] | DEFAULT `'{}'` |
| `feature_importance` | **JSONB** | DEFAULT `'{}'` — see § 5.2 |
| `created_at` | TIMESTAMPTZ | DEFAULT `NOW()` |

Plus columns implied by the migration 011 UNIQUE constraint that are NOT declared in migration 005's CREATE TABLE: a `style` column and a `model_used` column. These columns must exist on the live table at lock for migration 011's UNIQUE `(race_id, entry_id, style)` to apply; their CREATE statements are not preserved in any of the 12 tracked migration files. See verification log V1-7a for the substrate observation. **Implication for this bible:** the working-tree migration history is incomplete relative to the live schema (Tier 4 substrate gap); production schema state for `wr_predictions` includes columns added by an out-of-band script not preserved as a tracked migration file.

**Primary key:** `prediction_id` (UUID).

**UNIQUE constraints (current, post-migration 011):** `UNIQUE(race_id, entry_id, style)` named `wr_predictions_unique_per_entry_style` (added by migration 011 line 67). The migration 011 preamble declares the prior form was `UNIQUE(race_id, entry_id, model_used, style)` named `wr_predictions_unique_per_entry_model_style`, which migration 011 explicitly DROPs (line 64) — see § 8.W.1. Per BIBLE_STRUCTURE_SPEC v6 § 5.6.4 G2 conditional clause: the prior form is **physically dropped** (DROP CONSTRAINT), so no Deprecated entry is required; migration 011 itself serves as immune memory.

The migration-005 CREATE TABLE statement declares an inline `UNIQUE(entry_id)` constraint (line 30); this single-column UNIQUE was superseded by the multi-column form at some point between migration 005 (2026-03-18) and migration 011, via an out-of-band script not preserved as a tracked migration. Migration 011's `DROP CONSTRAINT IF EXISTS wr_predictions_unique_per_entry_model_style` is idempotent and works whether or not the named prior constraint existed — so the migration applies cleanly regardless of the intermediate-state ambiguity.

**FK constraints:** `entry_id` → `entries(entry_id)` NOT NULL; `race_id` → `races(race_id)` NOT NULL; `horse_id` → `horses(horse_id)` NOT NULL; `model_version_id` → `model_versions(model_version_id)` (nullable per migration 005 line 10).

**JSONB columns:** `feature_importance` JSONB DEFAULT `'{}'`. Shape per § 5.2.

**Secondary indexes:** `idx_wr_predictions_race` on `(race_id, predicted_rank)` (migration 005:88); `idx_wr_predictions_date` on `(created_at)` (migration 005:89).

**Purpose.** WR (win-and-rank) per-entry inference output: ranking probability, predicted rank, value flag, JSONB feature importance, ground-truth back-fill columns. The `style` column carries the per-style variant (the WR pipeline runs multiple styles per race; one row per (race, entry, style) tuple post-migration-011). The `model_used` column is per-horse dispatch metadata (the WR service chooses `core` vs `full` based on workout availability — per migration 011 preamble; see § 5.1).

**Primary writers.** `equine-wr-inference` Lambda (Active per `architecture_overview:3.1`); the SQL INSERT lives at `wr_prediction_repository.py:293` with `ON CONFLICT (race_id, entry_id, style) DO UPDATE SET ...` upsert semantics (matching the post-migration-011 UNIQUE).

**Primary readers.** `wr_prediction_repository.py` for the WR-specific repo surface. Cross-table reads from `ls_prediction_repository.py:262` (`get_longshot_alerts_by_date` — `FROM wr_predictions p`) and `ls_prediction_repository.py:374` (`get_track_record` — `FROM wr_predictions p`); these methods read `wr_predictions` despite living in the LSPredictionRepository class because LS data is currently second-pass enrichment on `wr_predictions` columns (per migration 010 preamble + verification log F.3). Migration 011 preamble names downstream LS softmax + ComparePage Cartesian + track_record consumers as the duplicate-row consumers fixed by § 8.W.1. Per-route detail at `api_frontend_bible:4.1`.

#### 4.1.13 `pl_predictions`

**Columns:** 21 columns declared in migration 005 (`005_three_prediction_tables.sql:34-58`):

| Column | Type | Notes |
|---|---|---|
| `prediction_id` | UUID | PK, default `gen_random_uuid()` |
| `entry_id` | UUID | NOT NULL, FK to `entries(entry_id)` |
| `race_id` | UUID | NOT NULL, FK to `races(race_id)` |
| `horse_id` | UUID | NOT NULL, FK to `horses(horse_id)` |
| `model_version_id` | UUID | FK to `model_versions(model_version_id)` |
| `win_probability`, `closing_odds`, `implied_probability`, `edge_pct`, `kelly_fraction` | DECIMAL(6,4) / DECIMAL(8,2) | |
| `predicted_ev`, `confidence_score`, `kelly_bet_size` | DECIMAL(8,4) / DECIMAL(8,2) | |
| `predicted_rank`, `actual_finish` | INTEGER | |
| `is_top_pick`, `is_value_bet`, `is_strong_value`, `was_win` | BOOLEAN | DEFAULT `FALSE` |
| `bet_profit` | DECIMAL(8,2) | |
| `feature_importance` | **JSONB** | DEFAULT `'{}'` — see § 5.2 |
| `created_at` | TIMESTAMPTZ | DEFAULT `NOW()` |

**Primary key:** `prediction_id` (UUID).

**UNIQUE constraints (current).** Migration 005's CREATE TABLE declares inline `UNIQUE(entry_id)` (line 57). The live table state at lock includes a `style` column (per migration 010 preamble, which says "matches wr_predictions / pl_predictions" pattern) and a `(race_id, entry_id, style)` UNIQUE constraint — the `pl_prediction_repository.py:272` INSERT uses `ON CONFLICT (race_id, entry_id, style) DO UPDATE SET ...` matching that pattern. The transition from the migration-005 single-column form to the multi-column form is not preserved as a tracked migration (parallel to the `wr_predictions` substrate gap noted at § 4.1.12). See verification log V1-7b.

**FK constraints:** `entry_id` → `entries(entry_id)` NOT NULL; `race_id` → `races(race_id)` NOT NULL; `horse_id` → `horses(horse_id)` NOT NULL; `model_version_id` → `model_versions(model_version_id)`.

**JSONB columns:** `feature_importance` JSONB DEFAULT `'{}'`.

**Secondary indexes:** `idx_pl_predictions_race` on `(race_id, predicted_rank)` (migration 005:90); `idx_pl_predictions_value` on `(race_id) WHERE is_value_bet = true` (migration 005:91 — partial index on value-bet rows only).

**Purpose.** PL (place-and-show) per-entry inference output: win probability, predicted EV, edge-pct, kelly fraction, value-bet flags. Stream E results-aware columns (`actual_finish`, `was_win`, `bet_profit`) carry post-race ground-truth for backtesting.

**Primary writers.** `equine-pl-inference` Lambda (Active per `architecture_overview:3.1`); the SQL INSERT lives at `pl_prediction_repository.py:255` with `ON CONFLICT (race_id, entry_id, style) DO UPDATE SET ...` upsert semantics.

**Primary readers.** `pl_prediction_repository.py` for the PL-specific repo surface. Per-route detail at `api_frontend_bible:4.1`.

#### 4.1.14 `ls_predictions`

**Columns:** 21 columns declared in migration 005 (`005_three_prediction_tables.sql:61-85`) plus 5 added by migration 010 (`010_ls_predictions_first_class.sql:23-28`):

Migration 005 columns:

| Column | Type | Notes |
|---|---|---|
| `prediction_id` | UUID | PK, default `gen_random_uuid()` |
| `entry_id` | UUID | NOT NULL, FK to `entries(entry_id)` |
| `race_id` | UUID | NOT NULL, FK to `races(race_id)` |
| `horse_id` | UUID | NOT NULL, FK to `horses(horse_id)` |
| `model_version_id` | UUID | FK to `model_versions(model_version_id)` |
| `final_win_probability`, `kelly_fraction`, `rf_longshot_prob`, `lstm_trajectory`, `calibrated_win_prob` | DECIMAL(6,4) | |
| `xgb_rank_score`, `bayesian_angle_ev`, `actual_odds`, `bet_profit` | DECIMAL(8,4) / DECIMAL(8,2) | |
| `predicted_rank`, `actual_finish` | INTEGER | |
| `longshot_alert`, `was_win` | BOOLEAN | DEFAULT `FALSE` |
| `confidence` | VARCHAR(10) | |
| `angle_description` | TEXT | |
| `feature_importance` | **JSONB** | DEFAULT `'{}'` — see § 5.2 |
| `created_at` | TIMESTAMPTZ | DEFAULT `NOW()` |

Migration 010 additions:

| Column | Type | Notes |
|---|---|---|
| `style` | VARCHAR(50) | DEFAULT `'general'` |
| `market_prob`, `edge_pct`, `morning_line_implied_prob` | NUMERIC | |
| `is_top_pick` | BOOLEAN | DEFAULT `FALSE` |

**Primary key:** `prediction_id` (UUID).

**UNIQUE constraints (current, post-migration 010):** `UNIQUE(race_id, entry_id, style)` named `ls_predictions_unique_per_entry_style` (added by migration 010 lines 38-40). The prior form (`UNIQUE(entry_id)` from migration 005, backed by auto-generated index `ls_predictions_entry_id_key`) was DROP'd by migration 010 lines 35-37. Per § 5.6.4 G2: the prior form is physically dropped, so no Deprecated entry is required; migration 010 serves as immune memory.

Migration 010 preamble notes that at the time of the migration (2026-05-01), `ls_predictions` held zero rows ("Existing rows: 0 (verified empty)"), so the constraint switch was safe.

**FK constraints:** Same as 005-time: `entry_id` → `entries(entry_id)`; `race_id` → `races(race_id)`; `horse_id` → `horses(horse_id)`; `model_version_id` → `model_versions(model_version_id)`.

**JSONB columns:** `feature_importance` JSONB DEFAULT `'{}'`.

**Secondary indexes:** `idx_ls_predictions_race` on `(race_id, predicted_rank)` (migration 005:92); `idx_ls_predictions_alert` on `(race_id) WHERE longshot_alert = true` (migration 005:93 — partial index on alert rows only).

**Purpose.** LS (longshot) per-entry inference output: ensemble win probability, longshot-alert flag, multi-component scores (XGB rank, RF longshot prob, LSTM trajectory, calibrated win prob, Bayesian angle EV), market-prob / edge-pct columns added by migration 010 for first-class parity with `wr_predictions` / `pl_predictions`.

**Primary writers.** `equine-ls-inference` Lambda (Active per `architecture_overview:3.1`). The actual production INSERT path is in `ls_inference_service.py:388-401` with `ON CONFLICT (race_id, entry_id, style) DO UPDATE SET ...` matching the post-migration-010 constraint. Note: the legacy `ls_prediction_repository.py:282 insert_prediction` method declares `ON CONFLICT (entry_id)` which does not match the current UNIQUE constraint; per migration 010's preamble, that repo method "has never been called" — so the stale ON CONFLICT clause is dead code, not an active bug. Surfacing for code-cleanup awareness; not a schema-discipline issue.

**Primary readers.** `ls_prediction_repository.py`. Read methods that query `ls_predictions` directly: `get_predictions_by_race` (line 98), `get_predictions_by_date` (line 158), `get_todays_predictions` (delegates to by-date). Read methods on the same class that query `wr_predictions` instead (the LS-as-enrichment-on-wr_predictions pattern per migration 010 preamble): `get_longshot_alerts_by_date` (line 262), `get_track_record` (line 374). Writer: `insert_prediction` (line 282) is dead code per migration 010 preamble's note. Per-route detail at `api_frontend_bible:4.1`.

#### 4.1.15 `angle_stats`

**Substrate-capture provenance.** This sub-section codifies the `angle_stats` table as it exists in production at the v1-patched-d2 patch cycle (2026-05-06). The table was surfaced via Data Pipeline Bible v1-patched-a verification log § F.4 (UPSTREAM-CORRECTION class FRAMEWORK_GAP, Tony-ratified 2026-05-06): production handler at `backend/lambdas/ingestion/handler.py:94-188` writes the table via DELETE + 6× INSERT cycle, but the table is NOT declared in `backend/database/schema/schema.sql` or in any of the 12 tracked migration files (`001`–`011`, including the duplicate-005 case per § 4.2.2). The whole table was created out-of-band — structurally analogous to F.2's `wr_predictions` / `pl_predictions` out-of-band ALTER pattern documented at § 4.1.12 / § 4.1.13, but worse in scope (the entire table, not just additive columns).

**Empirical-substrate disposition (PHASE 1 of patch cycle).** Live DB column-list capture via `equine-ingestion` Lambda's `raw_query` action was attempted; the Lambda's container image is in Inactive state at the patch cycle (`aws lambda get-function --function-name equine-ingestion` returns `State: Inactive` + `LastUpdateStatus: Successful` + `LastModified: 2026-05-02T15:45:37+0000`; subsequent invocation returns `CodeArtifactUserFailedException: Lambda cannot initialize the provided container image`). No alternative DB-credentialed path was reachable in the patch CC environment (the other Active Lambdas — `equine-inference` family — use HTTP routing without an arbitrary-SELECT action surface; the public API endpoint exposes only race / prediction routes). Schema substrate below is therefore **asserted-from-handler-INSERT-tuples-not-empirically-verified** per the patch-spec PHASE 1 Approach B fallback discipline. Re-verification at the next credential-authorized cycle when the `equine-ingestion` Lambda is repaired or an alternative DB-query path is wired up. Companion verification log entries V1-18 / V1-19 / V1-20 carry the verbatim PHASE 1 substrate.

**Columns (asserted from handler.py INSERT tuples lines 100, 112, 123, 136, 147, 165 + reader query patterns at `ls_inference_service.py:547-553`).** All 6 INSERT statements share an identical 5-column tuple form `INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts) SELECT ...`:

| Column | Type (asserted) | Notes |
|---|---|---|
| `angle_name` | TEXT or VARCHAR | NOT NULL (asserted; every INSERT writes a literal angle key — `'first_time_lasix'` / `'blinkers_on'` / `'class_drop'`). Reader uses `WHERE angle_name = %s` exact-match. |
| `trainer_name` | TEXT or VARCHAR | Nullable. Six INSERT statements split per-angle into two arms: a trainer-specific arm (`SELECT '<angle>', pp.trainer_name, NULL, ...`) and a global aggregation arm (`SELECT '<angle>', NULL, NULL, ...`). Reader at `ls_inference_service.py:547` falls back from `WHERE angle_name = %s AND trainer_name = %s` (trainer-specific) to `WHERE angle_name = %s AND trainer_name IS NULL` (global) when the trainer-specific row's `starts < 5`. |
| `track_code` | TEXT / VARCHAR / CHAR | Nullable. Always written as literal NULL in all 6 INSERT statements at this patch cycle. The column exists in the INSERT tuple form but no current writer path populates it; substrate suggests provision for future track-specific aggregations. |
| `wins` | INTEGER (asserted) | Source: `COUNT(*) FILTER (WHERE pp.finish_position = 1)` — the count of finishes where `past_performances.finish_position = 1`. Always non-negative. |
| `starts` | INTEGER (asserted) | Source: `COUNT(*)` — the total starts in the angle / trainer / global cohort. Reader uses `int(stats.get('starts', 0))` and `int(stats['starts'])` casts at `ls_inference_service.py:548-549, 558` confirming integer semantics. The cohort filter `HAVING COUNT(*) >= 5` (in the trainer-specific arms) means trainer-specific rows always have `starts >= 5`. |

**Primary key (substrate disposition).** Cannot be empirically determined from handler.py / reader.py substrate alone. The handler uses a `DELETE FROM angle_stats` followed by 6 unconditional `INSERT` cycles per refresh — no `ON CONFLICT` clause, so the writer does not depend on a specific UNIQUE constraint structure. Two structurally-plausible forms: (1) auto-increment surrogate key (`id SERIAL PRIMARY KEY` typical of out-of-band table creation); (2) composite key `(angle_name, trainer_name, track_code)` matching the read-query pattern. Either is consistent with the writer + reader code. Re-verification pending a credential-authorized DB-introspection cycle.

**FK constraints (substrate disposition).** None inferable from handler.py / reader.py. The `trainer_name` column is denormalized text (matches the pattern of `past_performances.trainer_name` per § 4.1.7 — denormalized from `trainers.trainer_name` via FK chain, backfilled by migration 007); a FK to `trainers(trainer_name)` is plausible but unverified. `track_code` is plausibly a FK to `tracks(track_code)` but the column is always NULL at this patch cycle so any declared FK has no current enforcement bearing. Re-verification pending credential-authorized cycle.

**JSONB columns.** None inferable from substrate. No JSONB column would be expected for an aggregations-cache table.

**Secondary indexes (substrate disposition).** Cannot be empirically determined. The reader queries `angle_stats` with `WHERE angle_name = %s AND trainer_name = %s` (trainer-specific path, `ls_inference_service.py:547`) and `WHERE angle_name = %s AND trainer_name IS NULL` (global path, line 553), so a covering index on `(angle_name, trainer_name)` would be performance-relevant. Whether such an index is declared on the production table is unverified at this patch cycle. Re-verification pending credential-authorized cycle.

**Purpose.** Pre-computed Bayesian-angle wins/starts aggregations per (angle_name, trainer_name, track_code) tuple, used as a feature input by the LS inference path's per-entry angle scoring. Supports two cohort levels: per-trainer (with `HAVING COUNT(*) >= 5` minimum-starts threshold matching the same threshold used by the `trainer_stats` materialized view per § 3.2 inclusion rule) and global (no minimum-starts threshold, all-trainers aggregation). Three angle types currently populated: `first_time_lasix`, `blinkers_on`, `class_drop`. Refresh discipline: full DELETE + INSERT rebuild on each `refresh_angle_stats` action invocation (no incremental upsert path).

**Primary writers.** `equine-ingestion` Lambda action `refresh_angle_stats` at `backend/lambdas/ingestion/handler.py:94-188`. The handler executes a single DELETE on the table followed by 6 INSERTs (3 angles × 2 cohort levels = 6 INSERT statements), then a final `SELECT COUNT(*)` to confirm the post-refresh row count. Refresh cadence: action-driven, not scheduled — the action is invoked on operator demand or as part of an upstream pipeline trigger. Per-flow detail at `data_pipeline_bible:4.1.7` (the canonical home for the refresh_angle_stats flow's data-acquisition discipline).

**Primary readers.** `ls_inference_service._score_angles` at `backend/services/ls_inference_service.py:528-573`. The reader iterates over the per-entry angle flags (`row.get('lasix_first_time')`, `row.get('blinkers_on')`, `row.get('class_drop')`), then for each active angle queries `angle_stats` first with the trainer-specific WHERE clause and falls back to the global WHERE clause if the trainer-specific row has `starts < 5`. The wins/starts pair is consumed as Beta-distribution posterior parameters (`post_a = 1.0 + wins`; `post_b = 1.0 + (starts - wins)`) feeding an EV-based per-angle score selection. Per-route detail at `api_frontend_bible:4.1` (the LS-side route that consumes this score).

**Cross-references.**
- `data_pipeline_bible:4.1.7` — canonical home for the `refresh_angle_stats` flow's data-acquisition discipline (writer-side flow detail).
- `data_pipeline_bible` verification log § F.4 — UPSTREAM-CORRECTION class FRAMEWORK_GAP that surfaced this table's out-of-band substrate; routing ratified by Tony 2026-05-06 to the D&S Bible v1-patched-d2 patch cycle.
- `feature_provenance_bible` (when drafted) — the per-feature consumption substrate (which angle scores feed which model column) belongs there per § 1 boundary statement.
- This bible's § 6 (Currently Open) for the open formalization-via-migration backlog disposition.

**Conditional triggers (per BIBLE_STRUCTURE_SPEC v6 § 5.6.4):**
- **if-table-was-created-out-of-band (no tracked migration): FIRES.** `angle_stats` was created out-of-band; no tracked migration declares this table at lock. Surfaced via Data Pipeline Bible v1-patched-a verification log § F.4 (UPSTREAM-CORRECTION class). This sub-section codifies the substrate at lock time. Future migration formalization (a new `NNN_YYYYMMDD_*.sql` file declaring the CREATE TABLE statement matching the live-DB column list once that's empirically captured) is Phase 5 backlog scope; the candidate disposition is the "document the table-as-it-IS-in-production at lock + defer formalization" route per the analogous F.2 disposition for `wr_predictions` / `pl_predictions` out-of-band ALTER columns.
- **if-table-has-out-of-band-column-additions (analog to F.2): N/A.** No PHASE 1 substrate surfaces additional columns beyond the 5-tuple INSERT form. (At credential-authorized re-verification, if the live DB's column list extends beyond the 5 columns above — e.g., a surrogate `id` key or a `created_at` audit column — that surfaces as a new substrate observation rather than retroactively-applied F.2-style flag.)
- **if-table-participates-in-cross-cutting-bug-at-lock: DOES NOT FIRE.** No current open bug references `angle_stats` per audit-CC v1-patched-a finding A3 + this patch cycle's PHASE 1 substrate sweep.
- **if-table-has-known-schema-vs-handler-drift: CONDITIONAL.** PHASE 1 Empirical Check 1 substrate (the 5-column INSERT tuple form) matches the reader's WHERE-clause column references (`angle_name`, `trainer_name`) — no observable drift between writer + reader at this patch cycle. Whether the live DB's actual column list matches the 5-column inferred form is unverified pending credential-authorized cycle; if drift surfaces, it gets a follow-up patch entry. Adjacent-prose caveat: the conditional fires "soft" because the verification is incomplete, not because drift is established — distinct from a hard FIRES which would require empirically-confirmed drift.

### 4.2 Migration discipline (per META_PLAN v9 § 7.12)

Migration discipline operative at lock per META_PLAN v9 § 7.12 + verification log claim V1-3.

#### 4.2.1 Numbering format (grandfathered 001–011 + NNN_YYYYMMDD from 012+)

Migration files in `backend/database/migrations/` follow two filename formats per META_PLAN v9 § 7.12:

- **Migrations 001–011 (grandfathered):** `NNN_short_description.sql` — three-digit prefix + underscore + short_description + `.sql`. No date in filename. **No renaming**; the existing 12 files keep this format. Phase 0 deliberately did not rename them.
- **Migrations 012 onward:** `NNN_YYYYMMDD_short_description.sql` — three-digit prefix + underscore + ISO date + underscore + short_description + `.sql`. The date in the filename is the date the migration was authored. The first migration to use this format documents the cutover and rationale in its preamble.

**12 migration files at lock** (verified 2026-05-05; companion verification log claim V1-3):

| # | Filename | Purpose |
|---|---|---|
| 1 | `001_initial_schema.sql` | Initial schema mirror of `schema.sql` (byte-identical per § 3.3). 11 CREATE TABLE statements. |
| 2 | `002_fix_race_type_length.sql` | Widen `races.race_type` and `past_performances.race_type` from VARCHAR(20) to handle long values like `allowance_optional_claiming` (28 chars). See § 8.W.2. |
| 3 | `003_widen_varchar_columns.sql` | Widen additional VARCHAR columns that received longer-than-declared values from real-world race data (e.g., `running_style` to VARCHAR(30)). |
| 4 | `004_backfill_running_style.sql` | Backfill `past_performances.running_style` from `call_1_position` per the `RUNNING_STYLE_THRESHOLDS` constant in `constants.py`. Stores the value rather than computing on-the-fly to enable SQL-level filtering. |
| 5 | `005_backfill_pace_delta.sql` | Compute `past_performances.pace_delta` as `finish_call_position - call_2_position`. (Subsequently corrected by migration 009 because `finish_call_position` was 0%-populated; see migration 009.) |
| 6 | `005_three_prediction_tables.sql` | Create `wr_predictions`, `pl_predictions`, `ls_predictions`; ALTER `model_versions` to add `model_type` + 3 PL-evaluation columns; replace global `idx_active_model` with per-type partial UNIQUE INDEX. (Authored 2026-03-18 per file preamble.) |
| 7 | `006_backfill_early_pace_pressure.sql` | Compute `past_performances.early_pace_pressure` per race (count of horses at `call_1_position <= 3` in the same race). Joined via `(race_date, track_code, race_number)` because `race_id` is not populated in `past_performances` (0%). |
| 8 | `007_backfill_trainer_name.sql` | Backfill `past_performances.trainer_name` denormalization via the join path PP → entries → races → trainers. |
| 9 | `008_create_trainer_stats.sql` | Create the `trainer_stats` materialized view (§ 3.2). |
| 10 | `009_backfill_pace_delta_v2.sql` | Re-backfill `pace_delta` using `finish_position` (99.5% populated) instead of `finish_call_position` (0% populated). Excludes finish codes ≥ 90 (DNF/pulled/vet scratch). |
| 11 | `010_ls_predictions_first_class.sql` | Add `style`, `market_prob`, `edge_pct`, `is_top_pick`, `morning_line_implied_prob` columns to `ls_predictions`; replace `UNIQUE(entry_id)` with `UNIQUE(race_id, entry_id, style)`. |
| 12 | `011_wr_predictions_unique_fix.sql` | Cleanup of 427 duplicate `wr_predictions` rows + replace `UNIQUE(race_id, entry_id, model_used, style)` with `UNIQUE(race_id, entry_id, style)`. See § 8.W.1. |

**File-count decomposition.** **12 .sql files = 11 NNN-prefix numbers (001–011) + 1 duplicate-005 file** (the `005_backfill_pace_delta.sql` and `005_three_prediction_tables.sql` pair share the `005_` prefix). See § 4.2.2.

#### 4.2.2 The duplicate-005 case

Two migration files share the `005_` prefix:

- `005_backfill_pace_delta.sql` (data-backfill: compute `pace_delta` as `finish_call_position - call_2_position`).
- `005_three_prediction_tables.sql` (schema-evolution: create `wr_predictions`, `pl_predictions`, `ls_predictions`; ALTER `model_versions`).

This is an **inherited problem** — the duplicate prefix was introduced when the per-pipeline split (May 2025-era thinking, authored 2026-03-18) overlapped a backfill that had already taken the `005_` slot. Phase 1 documents the case honestly; remediation is Phase 5 work pending an explicit `PHASE_5_BACKLOG.md` entry.

**Operational impact.** Lexical sort orders the two files deterministically: `005_backfill_pace_delta.sql` < `005_three_prediction_tables.sql` (alphabetical on the suffix after `005_`). The runner (`migrate.py:run_migrations`) iterates `sorted(*.sql)` and applies each file in lexical order — so the backfill applies first, then the three-prediction-tables migration. Both files are tracked as opaque distinct filenames in the `schema_migrations` runner table (one row per filename, per `migrate.py:90-93`).

**Forward rule (Phase 5 onward).** No new migrations may share an NNN-prefix with an existing migration. The new `NNN_YYYYMMDD_*.sql` format from migration 012+ trivially prevents recurrence: the date component disambiguates same-day siblings via prefix uniqueness.

#### 4.2.3 The `schema_migrations` runner mechanism

The migration runner is `backend/database/migrations/migrate.py`. It is invoked manually (or via CI) against an environment whose connection details are resolved by `get_connection_string()` (lines 21–43): from `DATABASE_URL` env var if set, otherwise from Secrets Manager via `DB_SECRET_ARN`.

**`schema_migrations` table.** Created at runtime by `ensure_migrations_table` (lines 44–54):

```python
CREATE TABLE IF NOT EXISTS schema_migrations (
    migration_id SERIAL PRIMARY KEY,
    filename VARCHAR(255) UNIQUE NOT NULL,
    applied_at TIMESTAMPTZ DEFAULT NOW()
)
```

This table is runner-internal book-keeping. It is NOT a domain table and is NOT enumerated in the 15-table count at § 3.1.

**Application loop.** `run_migrations` (lines 64–104):

1. `ensure_migrations_table` (line 66) — idempotent CREATE.
2. `get_applied_migrations(conn)` (line 67) — `SELECT filename FROM schema_migrations`, returns a set.
3. `sql_files = sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql"))` (lines 69–72) — lexical sort.
4. For each filename: skip if in the applied set; otherwise `cur.execute(sql)` then `INSERT INTO schema_migrations (filename) VALUES (%s)` then `conn.commit()` (lines 88–94). On exception: `conn.rollback()` then `sys.exit(1)` (lines 97–102) — fail-fast.

**Idempotency.** Because the runner skips applied filenames, repeated runs on the same DB state are safe. The fail-fast behavior (`sys.exit(1)` on exception) ensures partial migrations are surfaced rather than silently skipped on the next run.

#### 4.2.4 Rollback format (in-file down-block, manual)

Per META_PLAN v9 § 7.12: rollback SQL lives in the **same migration file**, after the up SQL, in a clearly-delimited block. The migration runner does NOT auto-execute the down block. Rollback is operator-driven. The bible entry references the migration file; it does not duplicate the rollback SQL.

If rollback is not feasible (e.g., a migration that DROP'd a column with data), the migration's preamble documents the irreversibility explicitly per META_PLAN v9 § 7.12 worked example for non-reversible migrations.

**Current state of in-file down-blocks at lock.** The 12 existing migrations (001–011) do not consistently include explicit `-- DOWN MIGRATION` blocks; rollback paths are operator-knowledge rather than file-encoded. Migration 010 and 011 wrap their schema mutations in `BEGIN; ... COMMIT;` transaction blocks (each with post-state validation `RAISE EXCEPTION` clauses that abort the transaction on validation failure) — this is per-migration safety, not a rollback path. The forward rule for migration 012+ codifies the down-block convention.

#### 4.2.5 Migration testing (non-production database first)

Per META_PLAN v9 § 7.12: migrations are tested against a **non-production database first**, then applied to production.

**Definition of "non-production" at lock.** Two paths:

1. **Local PostgreSQL matching production engine version** (PostgreSQL 16.6 per `architecture_overview:3.3`). The operator runs `migrate.py` against a local Docker'd or installed `postgres:16.6` instance with a representative schema-bootstrap.
2. **Dedicated dev RDS instance.** This **does NOT currently exist** for EE — there is no `equine-db-dev` RDS instance at lock (verified absent via `architecture_overview:3.3` enumeration of one RDS instance only). Provisioning a dev RDS instance is candidate Phase 5 work pending an explicit `PHASE_5_BACKLOG.md` entry.

**Production target.** Cross-reference `architecture_overview:3.3` for the canonical RDS instance metadata (engine version, instance class, endpoint, database name); this bible does not duplicate the metadata.

---

## 5. Discipline rules

Numeric sub-section IDs per BIBLE_STRUCTURE_SPEC v6 § 5.7 closing-clause embed (G-new-1).

Two rules surfaced from substrate analysis (the schema files + migration files + repository writer code) and ratified by Tony on 2026-05-05. A third candidate (Common Mistake about producer-side parent-row verification before child INSERTs) was moved to data_pipeline_bible's candidate roster per the forward-deferral note at end of § 5 below.

### 5.1 Forbidden Pattern: Including per-row dispatch metadata in a UNIQUE constraint when the dispatch is cross-row coherent at a coarser key

**Rule.** A UNIQUE constraint on a per-entry table MUST NOT include a column that is per-row dispatch metadata (a value chosen by the producer based on per-row conditions, where the dispatch decision is intended to be deterministic given a coarser key) when the dispatch metadata can change between producer invocations for the same coarser-key tuple. Including such a column in the UNIQUE constraint allows multiple rows to coexist for the same coarser-key tuple — defeating the constraint's purpose.

**Rationale.** Migration 011 fixed this exact mistake on `wr_predictions`: the prior UNIQUE was `(race_id, entry_id, model_used, style)`. The `model_used` column is per-horse dispatch metadata — `WRInferenceService.predict_race` selects between `core` and `full` model variants based on workout availability per horse, so each horse goes through ONE model variant per inference, never both. But when workout data lands between inference runs, the same `(race_id, entry_id, style)` accumulates a `core` row from the first run AND a `full` row from the second run; the new variant doesn't conflict with the old key, so both persist. **Effect: 157 races (~1.35% of 11,629) accumulated 427 duplicate rows. Downstream consumers (LS softmax, ComparePage Cartesian, track_record double-counting) read both variants without filtering** `model_used`. See § 8.W.1.

**FORBIDDEN example (the migration-011-pre-state pattern):**

```sql
ALTER TABLE wr_predictions
  ADD CONSTRAINT wr_predictions_unique_per_entry_model_style
  UNIQUE (race_id, entry_id, model_used, style);
-- model_used is producer-side dispatch metadata, NOT a coherent
-- distinguishing key. Same horse can have core then full row;
-- both persist; downstream reads both without filtering.
```

**CORRECT example (the migration-011-post-state pattern; matches PL / LS):**

```sql
ALTER TABLE wr_predictions
  ADD CONSTRAINT wr_predictions_unique_per_entry_style
  UNIQUE (race_id, entry_id, style);
-- model_used remains a metadata column on the row; the latest
-- variant overwrites the prior via the upsert ON CONFLICT clause.
```

**Substrate provenance.** Migration 011 preamble (`backend/database/migrations/011_wr_predictions_unique_fix.sql:3-21`); the substrate-grounded duplicate-row count (427 across 157 races) at lines 14; the post-state ALTER TABLE at lines 63-68; the Symptom / Root cause / Fix breakdown at § 8.W.1.

### 5.2 JSONB conventions — schemas live in writer code

**Rule.** A JSONB column declares only the column type and (optionally) a default at the schema level. The actual key set, value types, and shape conventions live in the producing code (Tier 4 substrate). Code that reads a JSONB column MUST consult the writer code to understand the shape; code that writes a JSONB column MUST update both the writer code AND any downstream readers if the shape changes. The schema cannot be relied upon to enforce or document JSONB shape.

**Rationale.** EE's 6 JSONB columns each have shape conventions that are not visible from the schema. Consumers reading them by inspection-of-keys are coupled to writer behavior; consumers reading by key alone (`payload['feature_x']`) without consulting the writer can silently break when the writer renames a key.

**6 JSONB columns at lock** (verified 2026-05-05; companion verification log claim V1-5):

| Column | Schema declaration | Source | Shape (writer-defined) |
|---|---|---|---|
| `predictions.feature_importance` | JSONB (no default) | `schema.sql:342` | Per-prediction feature-importance map. Shape determined by the legacy `predictions` writer (no production writer at lock — table is read-only; pre-deprecation shape was a string→float map of feature_name → importance score). |
| `wr_predictions.feature_importance` | JSONB DEFAULT `'{}'` | `005_three_prediction_tables.sql:22` | Per-prediction feature-importance map. Shape produced by the WR pipeline. |
| `pl_predictions.feature_importance` | JSONB DEFAULT `'{}'` | `005_three_prediction_tables.sql:52` | Per-prediction feature-importance map. Shape produced by the PL pipeline. |
| `ls_predictions.feature_importance` | JSONB DEFAULT `'{}'` | `005_three_prediction_tables.sql:78` | Per-prediction feature-importance map. Shape produced by the LS pipeline. |
| `model_versions.feature_list` | JSONB (no default) | `schema.sql:371` | Canonical feature schema for the model version. Cross-reference forward to `feature_provenance_bible:4.2` for the per-model feature consumption contract — that bible is the canonical home for "what feature_list shape does each model version produce." |
| `model_versions.hyperparameters` | JSONB (no default) | `schema.sql:372` | Training-time hyperparameter snapshot. Cross-reference `model_evaluation_retraining_bible` for retrain-discipline implications of hyperparameter changes. |

**Refuted column.** A prior synthesis reference (banked in drafting spec § 10.2) cited `model_versions.metadata` as a JSONB column. Substrate verification (V1-6) confirms no such column exists; the closest match is `notes` TEXT (not JSONB). § 4.1.11 documents the canonical 21-column state.

**FORBIDDEN example:**

```python
# Reader code that assumes a feature_importance shape
# without consulting the writer:
payload = row['feature_importance']
score = payload['win_prob_drift']  # may not exist; writer
                                    # may have renamed it
```

**CORRECT example:**

```python
# Reader code that defends against shape evolution:
payload = row['feature_importance'] or {}
score = payload.get('win_prob_drift')  # safe; explicit None
                                        # propagation
# Writer changes are coordinated:
# update writer, search-grep all readers, update each.
```

**Substrate provenance.** `schema.sql:342, 371, 372` (3 declarations); `005_three_prediction_tables.sql:22, 52, 78` (3 declarations); `001_initial_schema.sql` mirrors schema.sql per § 3.3. The 6 JSONB columns enumerated above match `grep -hnE "JSONB" backend/database/schema/schema.sql backend/database/migrations/*.sql` output (verification log V1-5).

**Forward deferral note (Tony's Q3.3.c ratification 2026-05-05).** A candidate Common Mistake about producer-side parent-row verification before child INSERTs is canonically homed in `data_pipeline_bible:5` per BIBLE_STRUCTURE_SPEC v6 § 5.3 cross-cutting bug scope rule (the producer-side discipline is canonically homed where the producer's flow lives). Candidate-roster status pending data_pipeline_bible drafting cycle.

---

## 6. Currently Open

Cross-cutting bug whose symptoms touch this bible's domain (per BIBLE_STRUCTURE_SPEC v6 § 5.3):

- **Bug #28 NULL payout fields in `results` table — canonical: `data_pipeline_bible:#28`.** Symptom touching this bible: `results.win_payout` and `results.daily_double_payout` are NULL for rows produced since 2026-04-30 due to an HRN scraper column-shift defect. Substantive description (root cause, prevention discipline, operator memory) lives in `data_pipeline_bible` because the prevention is a data-acquisition discipline (column-position validation in the scraper), NOT a schema discipline.

Schema-canonically-homed open issue surfaced via § 4.1.11 substrate observation:

- **Multi-active-row reality of `model_versions` (per META_PLAN v9 § 9.13).** The partial UNIQUE INDEX `idx_active_model_per_type ON model_versions (model_type) WHERE is_active = true` (added by migration 005:108) declares the intent "at most one active row per `model_type`." Live state at lock holds 88 model_version rows = 45 active + 43 inactive (per META_PLAN v9 § 9.13 inheritance), with multiple active rows per `model_type` in violation of the partial-UNIQUE intent. The function `get_active_model_by_type` at `model_version_repository.py:100` selects an arbitrary row when multiple match — surfacing the mismatch between schema intent and live state. Disposition: investigate whether the partial UNIQUE INDEX is enforcing as expected (PostgreSQL partial unique indexes enforce only on rows matching the WHERE clause; if the live data violates, either the index was created post-violation without backfill cleanup, or there's a path that bypasses the index — for example, by direct UPDATE setting `is_active = true` on a row that already has another active sibling). Phase 5 backlog candidate; operator-stated determination of root cause + cleanup pending an explicit `PHASE_5_BACKLOG.md` entry.
- **`workouts.source` column schema-evolution candidate (DS-1 D6 v1-patched-e per Phase A handoff § 2.13).** The `workouts` table currently has no `source` column. Two daily producers (Source 3 NYRA Lambda + Source 4 Equibase sibling-repo per `data_pipeline_bible:4.4`) write to this table via shared S3 prefix → `equine-ingestion` Lambda's `load_workouts_from_s3` action. Producer attribution at DB-row level requires substrate archaeology (S3 prefix listing filtered to NYRA-infix vs non-NYRA-infix). Proposed enhancement: add `source VARCHAR` column with values like `'nyra'` / `'equibase'` / `'manual'`. Migration scope: new `NNN_YYYYMMDD_add_workouts_source.sql` declaring `ALTER TABLE workouts ADD COLUMN source VARCHAR(20)` + backfill logic (NYRA-infix S3 objects → `'nyra'`; non-infix → `'equibase'`). Substantive description at § 4.1.8; cross-reference `data_pipeline_bible:4.4` for operational source inventory. **Disposition.** Phase 5 backlog candidate; implementation deferred (schema migration scope; not in Phase A).
- **`angle_stats` table created out-of-band (no tracked migration declares it at lock); see § 4.1.15 substrate.** Surfaced via Data Pipeline Bible v1-patched-a verification log § F.4 (UPSTREAM-CORRECTION class FRAMEWORK_GAP, Tony-ratified 2026-05-06 with routing to this bible's v1-patched-d2 patch cycle). § 4.1.15 codifies the table-as-it-IS-in-production via PHASE 1 Approach B substrate (handler.py INSERT-tuple-asserted column list — live-DB introspection blocked at this patch cycle by the `equine-ingestion` Lambda's Inactive container-image state). Formalization-via-migration (a new `NNN_YYYYMMDD_*.sql` file declaring the CREATE TABLE statement matching the live-DB column list once that's empirically captured) is Phase 5 backlog scope; this bible documents the table-as-it-IS-in-production at lock per the analogous F.2 disposition for `wr_predictions` / `pl_predictions` out-of-band ALTER columns. Disposition: Phase 5 backlog candidate; pending explicit `PHASE_5_BACKLOG.md` entry. Re-verification of the column list / PK / FK / index substrate at the next credential-authorized cycle (when the `equine-ingestion` Lambda is repaired or an alternative DB-introspection path is wired up) lands as a follow-up small patch entry rather than blocking this lock.

No additional current open issues at lock canonically homed in this bible's domain.

---

## 7. Deprecated

### 7.1 Legacy `predictions` table

- **Field/Module name:** `predictions` table.
- **Canonical source:** `wr_predictions` (per-style WR), `pl_predictions` (P&L), `ls_predictions` (LS enrichment) — created by migration 005 (`005_three_prediction_tables.sql`).
- **Notes:** **6,600 rows at last verification 2026-05-05** (companion verification log claim V1-12; verified via `GET /dashboard/metrics` `counts.predictions` field served by `equine-inference` Active Lambda per `architecture_overview:3.1`). Active readers: `prediction_router.py`, `race_router.py`, `dashboard_router.py`, `horse_router.py` plus the `prediction_repository.py` module. Per-route detail with import + instantiation + SELECT decomposition deferred to `api_frontend_bible:4.1`.

  No production INSERT path writes to the legacy `predictions` table at lock; per-pipeline writes route to `wr_predictions` / `pl_predictions` / `ls_predictions`.

- **Phase 5 backlog reference:** `Phase 5.X.Y` (placeholder; the specific PHASE_5_BACKLOG.md entry does not exist until that document gains the entry per META_PLAN v9 Appendix A lead-paragraph scope clause).

- **Conditional triggers (per BIBLE_STRUCTURE_SPEC v6 § 5.6.1.2 tertiary-state notation):**
  - **if-deprecated-thing-has-active-readers: FIRES.** 4 router files named above (prediction_router.py, race_router.py, dashboard_router.py, horse_router.py); per-route detail at `api_frontend_bible:4.1`.
  - **if-deprecation-is-partial: FIRES.** The table exists and has active readers; no path slated for immediate removal. The deprecation is partial in the sense that production writes have stopped (routed to per-pipeline tables) but reads continue.
  - **if-deprecation-produced-Forbidden-Pattern: CONDITIONAL.** A candidate Forbidden Pattern "MUST NOT write to legacy `predictions` table" would belong at § 5.X if ratified; at this draft's lock, no production code path INSERTs to the table (verified by V1-11 inventory which surfaced 0 INSERT references in routers; further verification of `prediction_repository.py` writer-side state is candidate Phase 5 work). The candidate Forbidden Pattern has NOT been ratified in this bible's § 5 candidate roster — adjacent prose caveat: the prevention rule is implicit (no production code currently writes; the discipline is enforced by absence rather than declaration), so promoting it to a § 5 entry is QB's call during § 5.7 ratification rather than this draft's prerogative.
  - **if-deprecated-thing-is-superseded-SQL-constraint-or-schema-element: DOES NOT FIRE.** This is a deprecated table, not a superseded constraint. (Per BIBLE_STRUCTURE_SPEC v6 § 5.6.4 G2 verification clause: per-table deprecation is distinct from per-constraint scope; the G2 clause governs per-constraint deprecation only.)

---

## 8. What Was Fixed — Do Not Revert

### 8.W.1 wr_predictions UNIQUE constraint included per-horse dispatch metadata, accumulating duplicates (Bug #N TBD; fixed 2026-05-04)

**Bug #N assignment.** This W.N entry surfaces a NEW global Bug #N per BIBLE_STRUCTURE_SPEC v6 § 5.5.1; the global identifier is assigned by QB at ratification (the next available global Bug #N after the existing assignments — Bug #7, #15, #22, #24, #25, #28 are in use at lock per `architecture_overview:1` and METAL_PLAN v9 § 1.2). Pending QB ratification, the entry is identified locally as `8.W.1`.

**Fix date: 2026-05-04** (per `git log --format="%cs %h %s" -- backend/database/migrations/011_wr_predictions_unique_fix.sql | tail -1`, returning `2026-05-04 87dec36 Pre-bible baseline commit ...`). The git history of this repository was bootstrapped at commit `87dec36` ("Pre-bible baseline commit") on 2026-05-04, which captured pre-existing files — meaning the migration file existed before the baseline was committed. Per META_PLAN v9 § 7.3 placeholder-resolution sub-rule: the date returned by `git log` is the canonical W.N Fix date for placeholder-resolution purposes; the operator-historical authoring date for the migration itself predates 2026-05-04 but is not git-recoverable from this repository's history. See verification log V1-8 for the substrate detail.

**Symptom.** 157 races (~1.35% of 11,629) accumulated 427 duplicate rows in `wr_predictions`. Downstream consumers — LS softmax (which reads `wr_predictions` for its ensemble component), the ComparePage frontend (Cartesian-product join across model variants), and `track_record` (race-record double-counting) — read both row-variants per (race, entry, style) tuple without filtering on `model_used`, producing incorrect aggregates.

**Root cause.** The wr_predictions UNIQUE constraint was `UNIQUE(race_id, entry_id, model_used, style)` named `wr_predictions_unique_per_entry_model_style`. The `model_used` column is per-horse dispatch metadata: `WRInferenceService.predict_race` selects between `core` and `full` model variants per horse based on workout availability — each horse goes through ONE model variant per inference, never both. When workout data lands between inference runs, the same `(race_id, entry_id, style)` accumulates a `core` row from the first run AND a `full` row from the second run; the new variant doesn't conflict with the old key (different `model_used`), so both persist.

**Fix.** Migration 011 (`011_wr_predictions_unique_fix.sql`):

1. **Cleanup** (lines 49-60): `DELETE FROM wr_predictions WHERE prediction_id IN (...)` deletes all-but-one per `(race_id, entry_id, style)` tuple, keeping the most recent row per tuple via `ROW_NUMBER() OVER (PARTITION BY race_id, entry_id, style ORDER BY created_at DESC, prediction_id DESC)`.
2. **Constraint swap** (lines 63-68): `DROP CONSTRAINT IF EXISTS wr_predictions_unique_per_entry_model_style; ADD CONSTRAINT wr_predictions_unique_per_entry_style UNIQUE (race_id, entry_id, style)`. This matches the PL / LS pattern. `model_used` stays as a non-key metadata column; the latest variant overwrites cleanly via the existing `ON CONFLICT (race_id, entry_id, style) DO UPDATE SET ...` upsert in `wr_prediction_repository.py:293-313`.
3. **Post-state validation** (lines 71-97): wrapped in a `DO $$ ... $$` block that asserts zero remaining duplicates AND the new constraint is present in `pg_constraint`; on failure, `RAISE EXCEPTION` aborts the transaction. The cleanup + swap run as a SINGLE transaction (`BEGIN; ... COMMIT;`); PostgreSQL acquires `ACCESS EXCLUSIVE` on `wr_predictions` during the ALTER TABLE, so concurrent WR inference INSERTs either wait on the lock or are aborted (their retry logic handles either case).

**Why this entry exists.** Prevents recurrence of the "include per-horse dispatch metadata in UNIQUE constraint when the dispatch is cross-row coherent at the (race, horse) level" pattern — captured as candidate Forbidden Pattern at § 5.1. The schema-design discipline this entry codifies is: a UNIQUE constraint must enforce business-meaningful uniqueness, not the cardinality of producer-side dispatch decisions. When a column appears in a UNIQUE constraint, ask: "Can the producer write two rows for the same coarser-key tuple, where the only difference is this column?" If yes, the column does not belong in the UNIQUE constraint.

**Conditional triggers (per BIBLE_STRUCTURE_SPEC v6 § 5.6.1.2 tertiary-state notation):**

- **if-fix-involved-migration: FIRES.** Migration `011_wr_predictions_unique_fix.sql`.
- **if-fix-invalidated-prior-content: DOES NOT FIRE.** No prior bible content existed at fix time (pre-Phase-1).
- **if-fix-produced-Forbidden-Pattern: FIRES.** Cross-reference to candidate § 5.1 Forbidden Pattern (pending QB ratification per § 5.7 workflow).
- **if-fix-touches-multiple-bibles: DOES NOT FIRE.** Schema-design discipline is canonically homed in this bible per BIBLE_STRUCTURE_SPEC v6 § 5.3 cross-cutting bug scope rule (no other bible's discipline more directly prevents recurrence; the producer-side `WRInferenceService.predict_race` dispatch is downstream of the schema-design choice).

### 8.W.2 races.race_type VARCHAR(20) too short for canonical race-type strings (no global Bug #N; fixed 2026-03-15)

**Bug #N assignment.** No global Bug #N assigned at lock — this is a schema-mechanics fix that pre-dates the Bug #N convention's explicit operationalization (per BIBLE_STRUCTURE_SPEC v6 § 5.5.1 "the convention is monotonic and never reused: Bug #1, Bug #2, ..."; pre-convention fixes don't retroactively get assigned). Identified locally as `8.W.2`.

**Fix date: 2026-03-15** (per `git log --format="%cs %h %s" -- backend/database/migrations/002_fix_race_type_length.sql`, returning `2026-03-15 d93c4c4 Fix post_time TIMESTAMPTZ, race_type length, and connection isolation`). Per META_PLAN v9 § 7.3 placeholder-resolution sub-rule, this is the canonical W.N Fix date — the actual descriptive commit `d93c4c4` is git-recoverable for migration 002, distinct from the baseline-commit-only history of migration 011 (8.W.1). Audit-CC's substrate sweep across all 12 migrations confirmed migrations 001/002/003 have real 2026-03-15 commit dates while migrations 004-011 only have the baseline commit; verification log V1-8 carries the verbatim per-migration sweep.

**Symptom.** Inserts to `races.race_type` failed when the canonical race-type string `allowance_optional_claiming` (28 chars) exceeded the original VARCHAR(20) declaration. Same error class on `past_performances.race_type`.

**Root cause.** The initial VARCHAR(20) declaration in `schema.sql` did not anticipate the longest canonical race-type strings.

**Fix.** Migration `002_fix_race_type_length.sql` widened both columns to VARCHAR(30). Migration 003 subsequently widened additional VARCHAR columns (e.g., `running_style`) for the same class of issue.

**Why this entry exists.** Prevents the recurring pattern "declare VARCHAR(N) without surveying the actual canonical value-space first." Phase 1 schemas should default to VARCHAR(50)+ for any column whose value-space is curated text (codes, types, descriptions) unless there is a concrete length-cap rationale.

**Conditional triggers:**

- **if-fix-involved-migration: FIRES.** Migration `002_fix_race_type_length.sql` (and migration 003 for the additional widenings).
- **if-fix-invalidated-prior-content: DOES NOT FIRE.** No prior bible content existed at fix time.
- **if-fix-produced-Forbidden-Pattern: DOES NOT FIRE.** This is a column-sizing discipline (recommendation, not absolute rule); it does not produce a § 5 Forbidden Pattern. Documented as a discipline observation in this W.N entry.
- **if-fix-touches-multiple-bibles: DOES NOT FIRE.** Schema-mechanics canonically homed here.

---

## End of Database & Schema Bible v1-patched-e (LOCKED — Phase 1 deliverable 2 of 7; locked 2026-05-12 via Phase A D6 bundled bible patches dispatch under Tier 2 ceremony cap; supersedes v1-patched-d3 2026-05-11). 1 D6 patch applied: DS-1 NEW workouts source-column schema-evolution candidate at § 4.1.8 + entry in § 6 Currently Open. DS-2 matcher-Lambda sparse-invocation flag routed to `architecture_overview:3.12` AO-3 ORPHAN consolidated subsection Appendix B per best-practice (architectural/operational, not schema-shape). UC § 7.2 step 4 per-bible patch-CC convention overridden by Phase A entry directive ceremony cap; override disclosure per revision-history v1-patched-e entry above. Cross-bible cross-reference freeze NOT re-engaged for D6 (Tier 2 ceremony cap pattern). v1-patched-d3 footer historical content preserved below for substrate-evolution audit trail per banked Lesson § 4.17.

### v1-patched-d3 footer (historical retention per Lesson § 4.17)

## End of Database & Schema Bible v1-patched-d3 (LOCKED — Phase 1 deliverable 2 of 7; locked 2026-05-11 via cross-bible re-lock ceremony at parent EE Bible Upstream-Correction Cycle exit; terminal sub-cycle of parent cycle). Cross-bible cross-reference freeze re-engaged 2026-05-11; cohort coherent post-cycle exit (7-bible Phase 1 cohort per architecture_overview footer enumeration). Re-lock ceremony substrate appendix preserved per banked Lesson § 4.17.

Companion verification log NEW: `_audit/database_schema_bible_v1_patched_d3_verification.md` (DRAFT pending cohort-locked audit-CC per amended R15; V28 substrate-stability re-confirmation 2026-05-11T15:16:40Z UTC; Aurora-residual scan determination per D1 — VERIFY-ONLY-CLEAN; sub-cycle 4 of 4 terminal-cycle documentation). v1-patched-d2 lock-state companion verification log at `_audit/database_schema_bible_v1_verification.md` preserved verbatim per banked Lesson § 4.17 (locked bibles preserve drafting-time historical context); only v1-patched-d2 → v1-patched-d3 delta captured in NEW log per surgical-cosmetic-patch convention. Audit driving v1-patched-d2: `_audit/database_schema_bible_v1_audit.md` (preserved).

---

## Cross-bible re-lock ceremony substrate (per D3; sub-cycle 4 of 4 of parent EE Bible Upstream-Correction Cycle)

**Substrate readiness assessment at v1-patched-d3 SP-4-drafting-complete (2026-05-11):**

All 4 parent-cycle sub-cycle drafts saved on disk and pending cohort-locked audit-CC ratification:

| Sub-cycle | Bible | Draft state | Save location | Cascade integrity |
|---|---|---|---|---|
| 1 of 4 | Architecture Overview | DRAFT v3-patched-b (2026-05-11) | `docs/bible/architecture_overview.md` | 31 deltas + 3 NEW sections (§ 3.9 + § 3.10 + § 3.11); 6 patches A1+A2+A3+A4+A5+A6 (A3 verify-only-clean); audit tier per § 4.21 escalation = fresh audit-CC |
| 1.5 of 4 | API & Frontend Bible | DRAFT v1-patched-a (2026-05-11) | `docs/bible/api_frontend_bible.md` | 16 deltas; 5 patches B1+B2+B3+B4+B5; 3/3 cross-reference cascade integrity PASS; no NEW sections |
| 2 of 4 | Data Pipeline Bible | DRAFT v1-patched-d (2026-05-11) | `docs/bible/data_pipeline_bible.md` | 13 deltas; 7 patches C1+C2+C3+C4+C5+C6+C7; 5/5 cross-reference cascade integrity PASS; Finding 1 partial-closure (§ 4.1.4 closed; § 4.2.4 deferred) |
| 4 of 4 | Database & Schema Bible (this bible) | DRAFT v1-patched-d3 (2026-05-11) | `docs/bible/database_schema_bible.md` | Minimal 3-patch sub-cycle: D1 Aurora-residual verify-only-clean + D2 § 1.3 not-applicable + D3 re-lock ceremony substrate prep; LOW cascade depth |

**Cross-bible cross-reference freeze status at SP-4-drafting-complete:** LIFTED via Tony Option α 2026-05-09 (parent cycle scope); freeze re-locks at sub-cycle 4 close as part of cross-bible re-lock ceremony per R14.3 Option B ratification 2026-05-11.

**Re-lock target state (post-audit-CC-PASS + Tony lock disposition):** 4 bibles re-locked simultaneously in a single ceremony — Architecture Overview v3-patched-b LOCKED + API & Frontend Bible v1-patched-a LOCKED + Data Pipeline Bible v1-patched-d LOCKED + Database & Schema Bible v1-patched-d3 LOCKED. Cross-bible cross-reference freeze re-ratified at re-lock per cohort Handoff § 6.1-class discipline.

**Parent cycle exit conditions at re-lock:** EE Bible Upstream-Correction Cycle exits clean at the cross-bible re-lock ceremony. Deferred dispositions documented at cycle exit:
- § 4.2 Data Acquisition Honesty Protocol refresh in `data_pipeline_bible:4.2` → deferred to Phase A re-dispatch venue per R14.2 Option A scope exclusion (Finding 1 § 4.2.4 partial-closure component).
- Substrate-stale claims outside sub-cycle 2 C1-C7 scope in `data_pipeline_bible` § 3 + § 4.1.3 → deferred per R26 Option A drafting CC recommendation (sub-cycle 2 audit-CC absorbs as audit findings; subsequent patch cycle absorbs).
- 5.3.N+16 PHASE_5_BACKLOG candidate (CDK Bootstrap ECR lifecycle override) → formalization deferred to OCRC D7 territory or CDK reconciliation cycle entry per `architecture_overview:3.11.1` forward-reference.
- § 9.1 + § 9.2 CANDIDATE forbidden pattern + common mistake in `api_frontend_bible` → cohort-locked audit-CC verifies retain-CANDIDATE disposition; future cycle ratifies permanent-or-CANDIDATE.

**Cohort handoff:** Cohort-locked audit-CC is next QB output post-SP-4 ratification per amended R15. Audit scope: end-to-end coherence verification across all 4 sub-cycle drafts; cross-bible cross-reference cascade integrity; banking supersession discipline (F9 RETIRED + F22 supersedes; F19 RETIRED + F23 supersedes); R8 Option B retention discipline application across § 5.1 + § 5.2 + § 6 + per-flow narratives + admin-action surface impact; B5 naming convention (v3-patched-b + v1-patched-a + v1-patched-d + v1-patched-d3); Aurora-residual scan determination (D1 verify-only-clean); cross-bible re-lock ceremony substrate readiness.

**END Database & Schema Bible v1-patched-d3 DRAFT 2026-05-11 — sub-cycle 4 of 4 of parent EE Bible Upstream-Correction Cycle terminal sub-cycle.**
