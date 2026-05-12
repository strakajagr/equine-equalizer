# Database & Schema Bible v1 — Companion Verification Log

**Document:** database_schema_bible_v1_verification
**Phase:** 1 (Bible) — companion log for deliverable 2 of 7
**Status:** LOCKED v1-patched-d2 (2026-05-06) — companion log for Phase 1 deliverable 2 of 7 LOCKED; UPSTREAM-CORRECTION close from Data Pipeline Bible v1-patched-a F.4
**Author:** CC (drafting under Tier 3 verification discipline; QB orchestrated)
**Date:** 2026-05-05
**Locked:** 2026-05-05

**Revision history:**
- v1 (2026-05-05): initial CC verification log alongside the v1 bible draft.
- v1-patched (2026-05-05): surgical patch per Tony's ratifications on 2026-05-05 covering audit-CC findings D-3.1 BLOCKER + D-1.1 + D-1.2 + D-4.1 + D-4.2 + D-8 + D-9 + D-10 + Q1 + Q2.d + Q3.1 + Q3.2 + Q3.3.c. See `database_schema_bible_v1_audit.md` for the audit driving this patch and `_meta/database_schema_bible_v1_drafting_spec.md` for the original drafting spec.
- v1-patched-d1 (2026-05-05): single-line surgical patch per Tony's D1.a ratification on 2026-05-05 covering re-audit-CC finding D-1 (stale § 5.3 cross-reference at § 5 lead paragraph). See `database_schema_bible_v1_reaudit.md` Section D for the finding driving this patch.
- v1-patched-d2 (2026-05-06): surgical patch landing `angle_stats` substrate per UPSTREAM-CORRECTION from Data Pipeline Bible v1-patched-a verification log § F.4 (Tony ratified 2026-05-06). New Section C V1-N entries V1-18 + V1-19 + V1-20 document `angle_stats` schema substrate (PHASE 1 Empirical Checks 1 + 2 + 3; Approach B fallback used for Empirical Check 1 because the only Lambda with a `raw_query` action — `equine-ingestion` — is in Inactive container-image state at this patch cycle). See bible v1-patched-d2 revision-history bullet for cross-reference + threshold-condition summary.
- v1-patched-d2 LOCKED (2026-05-06): companion log for Phase 1 deliverable 2 of 7 re-LOCKED. See bible v1-patched-d2 LOCKED revision-history bullet for substrate provenance + threshold-condition summary. Section C V1-18 + V1-19 + V1-20 capture `angle_stats` substrate (PHASE 1 Empirical Checks 1 + 2 + 3); V1-18 documents Approach A failure (equine-ingestion Lambda Inactive + broken container image) + Approach B fallback (handler.py:90-188 verbatim 110-line paste).

**Tier:** 3 per META_PLAN v9 § 4.1 + § 6.5.

**Anchored on:** META_PLAN v9 (LOCKED 2026-05-05) + BIBLE_STRUCTURE_SPEC v6 (LOCKED 2026-05-05) + Architecture Overview v3 (LOCKED 2026-05-05).

**Companion bible:** `database_schema_bible.md`.

**Drafting spec:** `_meta/database_schema_bible_v1_drafting_spec.md` (QB-authored 2026-05-05).

**Section structure** per QB handoff § 7.2 (paste-prompt § "Companion verification log structure" subsection):

- **Section A:** inherited claims from upstream Phase 0 verification logs with re-verification timestamps.
- **Section B:** inherited claims from prior cycles of THIS bible's verification log (NOT applicable for v1 — first cycle).
- **Section C:** new V1-N claims with primary citations.
- **Section D:** methodology-interpolation self-check.
- **Section E:** pattern-completion check (W.N exclusivity preserved; numeric IDs honored).
- **Section F:** FRAMEWORK_GAP / SPEC_GAP markers.
- **Section G:** prior-cycle audit findings closure verification (NOT applicable for v1).
- **Section H:** QB self-audit log (char-exact reproduction of drafting spec § 6 H1–H9).
- **Section I:** new entries for surgical patch operations (NOT applicable for v1 — full draft, not surgical patch).

---

## Section A: Inherited claims from upstream Phase 0 verification logs

The Database & Schema Bible v1 inherits substrate from META_PLAN v9 + Architecture Overview v3. Re-verification timestamps below confirm the inherited claims remain accurate as of 2026-05-05 draft time.

### A.1 META_PLAN v9 § 9.13: model_versions multi-active-row reality (88 = 45 active + 43 inactive)

Inherited from META_PLAN v9 § 9.13. Substrate detail: the partial UNIQUE INDEX `idx_active_model_per_type` declares "at most one active row per `model_type`" intent, but live state has multiple active rows per `model_type`. The selection function `get_active_model_by_type` at `model_version_repository.py:100` returns an arbitrary row when multiple match.

Re-verification 2026-05-05: no live DB query was run from this draft session (the substrate claim is upstream-locked at META_PLAN v9). The claim is referenced in `database_schema_bible:4.1.11` and `database_schema_bible:6` as a Currently Open issue with "(per META_PLAN v9 § 9.13 inheritance)" annotation. Disposition pending Phase 5 backlog entry.

### A.2 META_PLAN v9 § 7.12: migration discipline (grandfathered 001–011 + NNN_YYYYMMDD from 012+)

Inherited from META_PLAN v9 § 7.12. Substrate detail: 12 existing migration files keep `NNN_short_description.sql`; from migration 012+ filename format is `NNN_YYYYMMDD_short_description.sql`. The duplicate-005 case is documented as inherited problem; remediation is Phase 5 work.

Re-verification 2026-05-05: confirmed via direct `ls backend/database/migrations/*.sql` (12 files; matches V1-3). Documented in `database_schema_bible:4.2`.

### A.3 META_PLAN v9 § 4.5: source-priority hierarchy (Tier 1 AWS > Tier 2 API > Tier 3 DB > Tier 4 working-tree code post-baseline > Tier 5 operator-stated > Tier 6 EE_CURRENT_STATE_DUMP > Tier 7 session logs)

Inherited from META_PLAN v9 § 4.5. Substrate detail: the 7-tier hierarchy governs source-of-truth resolution when sources conflict.

Re-verification 2026-05-05: the hierarchy is stated normatively in `database_schema_bible:1` and applied throughout (e.g., V1-1 + V1-1a use Tier 4 working-tree substrate; V1-12 uses Tier 2 dashboard endpoint).

### A.4 Architecture Overview v3 § 3.3: standalone RDS PostgreSQL `equine-db` (NOT Aurora)

Inherited from Architecture Overview v3 § 3.3 (which inherits from Architecture Overview v1 verification log Claim A.8 + the Aurora REFUTATION corrected upstream in META_PLAN v9 per V9-1.D substrate replacement).

Re-verification 2026-05-05: cross-referenced from `database_schema_bible:3.3` and `database_schema_bible:4.2.5`. Per Lesson 1 cross-project contamination check: the prior Aurora-cluster-ARN claim was cross-project bleed from `fantasy-baseball-serverless`; the EE substrate is standalone RDS PostgreSQL 16.6 `equine-db` (`db.t4g.micro`, endpoint `equine-db.cgtuh834bttd.us-east-1.rds.amazonaws.com:5432`, database `equine_equalizer`, DBClusterIdentifier `None`). Documented in this bible by section-anchor cross-reference, not duplicated.

### A.5 Architecture Overview v3 § 4.1: canonical objects with line numbers (Race=255, Entry=214, PastPerformance=77, Workout=58, Result=296, Prediction=428)

Inherited from Architecture Overview v3 § 4.1.

Re-verification 2026-05-05: this bible cross-references Architecture Overview § 4.1 via section-anchor (`architecture_overview:4.1`) per Check 8 line-shift-resistant citations. Literal canonical.py line numbers are NOT cited directly in this bible's body — they are referenced via Architecture Overview's existing § 4.1 enumeration. See V1-10 below.

### A.6 Architecture Overview v3 § 3.1: Lambda inventory (5 Active + 3 Inactive); fire-and-fail anomaly (4 ENABLED rules → 2 INACTIVE Lambdas)

Inherited from Architecture Overview v3 § 3.1 + § 3.6 + § 6.

Re-verification 2026-05-05: this bible's per-table primary-writer enumerations cite Lambda Active/INACTIVE state via cross-reference to `architecture_overview:3.1` and `architecture_overview:6`, not duplicated. The fire-and-fail anomaly affects this bible's § 4.1.5 (`races`), § 4.1.6 (`entries`), § 4.1.7 (`past_performances`), § 4.1.9 (`results`) which depend on the INACTIVE `equine-ingestion` and `equine-results` Lambdas.

---

## Section B: Inherited claims from prior cycles of this bible's verification log

**NOT APPLICABLE for v1 — first cycle.**

---

## Section C: New V1-N claims with primary citations

Each factual claim about EE in `database_schema_bible.md` traces to a V1-N entry below. Counts decomposed per META_PLAN v9 § 6.5 verification log precision rule (definitions vs uses vs imports distinguished; no compressible aggregations).

### V1-1: 14 distinct domain tables decomposed

**Claim:** EE's domain schema declares 14 distinct domain tables = 11 in `backend/database/schema/schema.sql` + 3 in `backend/database/migrations/005_three_prediction_tables.sql`.

**Verification command:**

```
grep -hnE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql
```

**Verification output (2026-05-05):**

- `backend/database/schema/schema.sql`: 11 CREATE TABLE statements at lines 12, 28, 50, 62, 75, 109, 145, 272, 293, 327, 359 — tracks (1), horses (2), trainers (3), jockeys (4), races (5), entries (6), past_performances (7), workouts (8), results (9), predictions (10), model_versions (11).
- `backend/database/migrations/001_initial_schema.sql`: 11 CREATE TABLE statements at the same line numbers (byte-identical mirror of schema.sql; see V1-1a).
- `backend/database/migrations/005_three_prediction_tables.sql`: 3 CREATE TABLE IF NOT EXISTS statements at lines 5, 34, 61 — wr_predictions (12), pl_predictions (13), ls_predictions (14).
- All other migration files (002, 003, 004, 005_backfill_pace_delta, 006, 007, 008, 009, 010, 011): 0 CREATE TABLE statements each.

**Decomposition:** 11 (schema.sql) + 11 (001 mirror) + 3 (005_three_prediction_tables) = **25 CREATE TABLE statements on disk; 14 distinct domain tables as the union (set), since schema.sql and 001_initial_schema.sql declare the same 11 tables in identical text** (per V1-1a). The V1-1 decomposition for this bible's § 3.1 statement is **11 (schema.sql) + 3 (005_three_prediction_tables) = 14 distinct domain tables**.

**Targeted vs total distinction (Check 9):** total disk count = 25 statements; distinct domain table count = 14; this draft's bible-text additions touch 14 § 4.1.X sub-sections (one per distinct domain table). Targeted-by-this-draft change to substrate = 0 (full prose authoring; substrate verified, not changed).

**Source-tier:** Tier 4 (working-tree code post-baseline 87dec36).

### V1-1a: schema.sql and 001_initial_schema.sql are byte-identical (substrate observation surfaced during V1-1)

**Claim:** `backend/database/schema/schema.sql` and `backend/database/migrations/001_initial_schema.sql` are byte-identical mirrors at lock.

**Verification command:**

```
diff backend/database/schema/schema.sql backend/database/migrations/001_initial_schema.sql ; echo "DIFF EXIT: $?"
wc -l backend/database/schema/schema.sql backend/database/migrations/001_initial_schema.sql
```

**Verification output (2026-05-05):**

- `diff` produces empty output (no differences).
- `DIFF EXIT: 0` (success exit code = files identical).
- `wc -l`: 415 lines each.

**Decomposition:** 415-line file in two locations; 11 CREATE TABLE per file; 0 differences.

**Implication for V1-1:** the QB drafting spec's `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql | grep -v "schema_migrations" | wc -l` predicted "expected: 14 plus possibly the `IF NOT EXISTS` patterns" — actual is 25 (11+11+3). The 14-distinct-table claim still holds as the union; the QB spec's grep prediction undercounted by not accounting for the schema.sql ↔ 001_initial_schema.sql byte-identity. Documented in this bible at § 3.3 with three operational interpretations (reference snapshot / runner-compatible packaging / parallel-source coexistence). Surfaced to QB in Section F as candidate FRAMEWORK_GAP G-new-3 with substrate-cited reframing.

**Source-tier:** Tier 4.

### V1-2: 1 materialized view (`trainer_stats`)

**Claim:** EE declares 1 materialized view named `trainer_stats`, created by `008_create_trainer_stats.sql`.

**Verification command:**

```
grep -hnE "^CREATE MATERIALIZED VIEW" backend/database/schema/schema.sql backend/database/migrations/*.sql
grep -lE "^CREATE MATERIALIZED VIEW" backend/database/schema/schema.sql backend/database/migrations/*.sql
```

**Verification output (2026-05-05):**

- 1 match at `backend/database/migrations/008_create_trainer_stats.sql:7` — `CREATE MATERIALIZED VIEW IF NOT EXISTS trainer_stats AS`.
- File-level: 1 file contains `CREATE MATERIALIZED VIEW` (`008_create_trainer_stats.sql`).

**Decomposition:** 1 declaration in 1 file. Zero matches in `schema.sql` or any other migration file.

**Source-tier:** Tier 4.

### V1-3: 12 migration files (11 NNN-prefix numbers + 1 duplicate-005)

**Claim:** `backend/database/migrations/` contains 12 `.sql` files at lock; the 12 files comprise 11 NNN-prefix numbers (001–011) + 1 duplicate-005 case.

**Verification command:**

```
ls backend/database/migrations/*.sql | wc -l
ls backend/database/migrations/*.sql
```

**Verification output (2026-05-05):**

- `wc -l` = **12**.
- Filename listing: 001_initial_schema.sql, 002_fix_race_type_length.sql, 003_widen_varchar_columns.sql, 004_backfill_running_style.sql, **005_backfill_pace_delta.sql**, **005_three_prediction_tables.sql**, 006_backfill_early_pace_pressure.sql, 007_backfill_trainer_name.sql, 008_create_trainer_stats.sql, 009_backfill_pace_delta_v2.sql, 010_ls_predictions_first_class.sql, 011_wr_predictions_unique_fix.sql.

**Decomposition:** 12 files = 11 NNN-prefix numbers (001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011) + 1 duplicate-005 sibling (`005_backfill_pace_delta.sql` and `005_three_prediction_tables.sql` both share NNN=005).

**Source-tier:** Tier 4.

### V1-4: schema_migrations runner table created at runtime by migrate.py

**Claim:** The `schema_migrations` book-keeping table is created at runtime by `backend/database/migrations/migrate.py:ensure_migrations_table` and is NOT a domain table.

**Verification command:**

```
grep -A 8 "ensure_migrations_table" backend/database/migrations/migrate.py
```

**Verification output (2026-05-05):**

```python
def ensure_migrations_table(conn):
    """Create schema_migrations table if it doesn't exist."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                migration_id SERIAL PRIMARY KEY,
                filename VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMPTZ DEFAULT NOW()
            )
```

Plus the call site at `migrate.py:66` (inside `run_migrations`). Plus `get_applied_migrations` at lines 57–61 (`SELECT filename FROM schema_migrations`). Plus the INSERT after each successful migration at `migrate.py:90-93` (`INSERT INTO schema_migrations (filename) VALUES (%s)`).

**Decomposition:** 1 CREATE TABLE statement (idempotent, `IF NOT EXISTS`) + 1 SELECT query + 1 INSERT statement, all inside `migrate.py`. Zero domain-table CREATE; this is runner infrastructure.

**Source-tier:** Tier 4.

### V1-5: 6 JSONB columns across 5 tables

**Claim:** EE has 6 JSONB column declarations across 5 tables.

**Verification command:**

```
grep -hnE "JSONB" backend/database/schema/schema.sql backend/database/migrations/*.sql
```

**Verification output (2026-05-05):**

- `backend/database/schema/schema.sql:342`: `feature_importance JSONB,` (in `predictions` table)
- `backend/database/schema/schema.sql:371`: `feature_list JSONB,` (in `model_versions` table)
- `backend/database/schema/schema.sql:372`: `hyperparameters JSONB,` (in `model_versions` table)
- `backend/database/migrations/001_initial_schema.sql:342, 371, 372`: same 3 declarations (byte-identical mirror per V1-1a)
- `backend/database/migrations/005_three_prediction_tables.sql:22`: `feature_importance JSONB DEFAULT '{}',` (in `wr_predictions` table)
- `backend/database/migrations/005_three_prediction_tables.sql:52`: `feature_importance JSONB DEFAULT '{}',` (in `pl_predictions` table)
- `backend/database/migrations/005_three_prediction_tables.sql:78`: `feature_importance JSONB DEFAULT '{}',` (in `ls_predictions` table)

**Decomposition:** 9 JSONB declarations on disk (3 in schema.sql + 3 mirrored in 001_initial_schema.sql + 3 in 005_three_prediction_tables.sql). **6 distinct JSONB columns as the union (set):** `predictions.feature_importance`, `model_versions.feature_list`, `model_versions.hyperparameters`, `wr_predictions.feature_importance`, `pl_predictions.feature_importance`, `ls_predictions.feature_importance`.

**Decomposition by table:** 5 tables hold these 6 columns — `predictions` (1), `model_versions` (2), `wr_predictions` (1), `pl_predictions` (1), `ls_predictions` (1). 1+2+1+1+1=6.

**Source-tier:** Tier 4.

### V1-6: model_versions.metadata column does NOT exist (refutation entry)

**Claim:** `model_versions.metadata` is NOT a column. The closest match is `notes TEXT` (not JSONB).

**Verification command:**

```
grep -inE "metadata" backend/database/schema/schema.sql backend/database/migrations/*.sql | head -50
```

**Verification output (2026-05-05):**

- `backend/database/migrations/011_wr_predictions_unique_fix.sql:5`: `--   model_used is a per-horse dispatch metadata flag set by` (SQL comment, narrative prose; not a column declaration)
- `backend/database/migrations/011_wr_predictions_unique_fix.sql:19`: `--   model_used stays as a metadata column; the latest variant overwrites` (SQL comment, narrative prose; not a column declaration)

**Zero matches** in CREATE TABLE / ALTER TABLE statements that declare a `metadata` column. The 2 hits are both inside SQL comments referring to `model_used` as "metadata flag" — narrative description, not a column.

**Decomposition:** 0 CREATE/ALTER TABLE declarations of any column named `metadata`; 2 comment-prose hits (both in migration 011, both referring to the `model_used` column as "metadata flag").

**Refutation provenance:** the prior synthesis reference banked at drafting spec § 10.2 cited `model_versions.metadata` as a JSONB column. Per Lesson 1 cross-project contamination check + Check 1 cross-reference accuracy, this is substrate-grounded refuted. The canonical 21-column `model_versions` state is documented in `database_schema_bible:4.1.11`.

**Source-tier:** Tier 4.

### V1-7: Migration 011's wr_predictions UNIQUE constraint swap

**Claim:** Migration 011 DROPs `wr_predictions_unique_per_entry_model_style` and ADDs `wr_predictions_unique_per_entry_style UNIQUE (race_id, entry_id, style)`.

**Verification command:**

```
grep -nE "(DROP CONSTRAINT|ADD CONSTRAINT)" backend/database/migrations/011_wr_predictions_unique_fix.sql
```

**Verification output (2026-05-05):**

- `backend/database/migrations/011_wr_predictions_unique_fix.sql:64`: `  DROP CONSTRAINT IF EXISTS wr_predictions_unique_per_entry_model_style;`
- `backend/database/migrations/011_wr_predictions_unique_fix.sql:67`: `  ADD CONSTRAINT wr_predictions_unique_per_entry_style`
- followed at line 68 by `  UNIQUE (race_id, entry_id, style);`

**Decomposition:** 1 DROP CONSTRAINT (idempotent, `IF EXISTS`) + 1 ADD CONSTRAINT, in a single transaction with cleanup (lines 49-60) and post-state validation (lines 71-97).

**Per BIBLE_STRUCTURE_SPEC v6 § 5.6.4 G2:** the prior superseded form is physically dropped → no Deprecated entry required. Documented in `database_schema_bible:4.1.12` and § 8.W.1.

**Source-tier:** Tier 4.

### V1-7a: wr_predictions `style` and `model_used` columns are not declared in any tracked migration (substrate gap)

**Claim:** Migration 011's UNIQUE constraint references `style` and `model_used` columns. Neither column is declared in migration 005's `wr_predictions` CREATE TABLE statement (which is the canonical declaration in tracked sources). No tracked migration in the working tree declares them. The columns must exist on the live table for migration 011 to apply, implying an out-of-band script populated them.

**Verification command:**

```
grep -nE "(wr_predictions_unique|wr_predictions ADD COLUMN.*style|wr_predictions ADD COLUMN.*model_used)" backend/database/migrations/*.sql
```

**Verification output (2026-05-05):** zero hits for `wr_predictions ADD COLUMN style` or `wr_predictions ADD COLUMN model_used` in any tracked migration. Migration 005's CREATE TABLE for `wr_predictions` (lines 5-31) does not declare `style` or `model_used`. Migration 010 ADDs `style` to `ls_predictions` only (not `wr_predictions`). Migration 011 references the columns as if they exist (in the UNIQUE constraint and the cleanup `PARTITION BY race_id, entry_id, style` query) but does not declare them.

**Decomposition:** 0 tracked migrations declare `wr_predictions.style`; 0 tracked migrations declare `wr_predictions.model_used`. Migration 011 idempotent DROP CONSTRAINT (`IF EXISTS`) handles the case whether or not the prior named constraint pre-existed.

**Implication for this bible:** the working-tree migration history is incomplete relative to the live schema. Documented in `database_schema_bible:4.1.12`. Surfaced to QB in Section F as candidate FRAMEWORK_GAP G-new-4.

**Source-tier:** Tier 4 (working-tree code) compared against implicit Tier 3 (live DB) via migration-applies-cleanly inference.

### V1-7b: pl_predictions `style` column not declared in tracked migrations; live UNIQUE constraint uses (race_id, entry_id, style)

**Claim:** Parallel substrate gap to V1-7a for `pl_predictions`. Migration 005's CREATE TABLE for `pl_predictions` (lines 34-58) does not declare `style`. The repository writer at `backend/repositories/pl_prediction_repository.py:272` uses `ON CONFLICT (race_id, entry_id, style) DO UPDATE SET ...` upsert syntax, implying the live UNIQUE constraint is `(race_id, entry_id, style)` (since `ON CONFLICT (cols)` requires a matching UNIQUE INDEX or PK in PostgreSQL).

**Verification command:**

```
grep -nE "ON CONFLICT" backend/repositories/pl_prediction_repository.py
grep -nE "pl_predictions ADD COLUMN.*style" backend/database/migrations/*.sql
```

**Verification output (2026-05-05):**

- `backend/repositories/pl_prediction_repository.py:272`: `ON CONFLICT (race_id, entry_id, style) DO UPDATE SET`
- `grep`: zero matches for `pl_predictions ADD COLUMN style` in any tracked migration.

**Decomposition:** 1 ON CONFLICT clause uses `(race_id, entry_id, style)` in the producer; 0 tracked migrations declare `pl_predictions.style`. Migration 005's CREATE TABLE has inline `UNIQUE(entry_id)` (line 57) only; the live state's multi-column UNIQUE is from an out-of-band script.

**Source-tier:** Tier 4 (working-tree code).

### V1-8: Migration fix dates per per-migration git log substrate sweep (rewritten in v1-patched per audit-CC D-3.1 BLOCKER finding)

**Claim:** The W.N Fix date for each migration W.N entry is the actual git-log commit date of the migration file per META_PLAN v9 § 7.3 placeholder-resolution sub-rule. For Database & Schema Bible v1: 8.W.1 (migration 011) Fix date = 2026-05-04 (baseline commit only); 8.W.2 (migration 002) Fix date = 2026-03-15 (descriptive commit `d93c4c4`).

**Verbatim verification command + output (audit-CC re-run, audit-CC's substrate sweep, 2026-05-05):**

```
$ for f in backend/database/migrations/*.sql; do printf "%s\t" "$(basename $f)"; git log --format="%cs %h %s" -- "$f" | head -1; done
001_initial_schema.sql	2026-03-15 0bb2a6d Initial commit — complete Equine Equalizer application
002_fix_race_type_length.sql	2026-03-15 d93c4c4 Fix post_time TIMESTAMPTZ, race_type length, and connection isolation
003_widen_varchar_columns.sql	2026-03-15 2a3d758 Widen VARCHAR columns and isolate per-race DB connections
004_backfill_running_style.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
005_backfill_pace_delta.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
005_three_prediction_tables.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
006_backfill_early_pace_pressure.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
007_backfill_trainer_name.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
008_create_trainer_stats.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
009_backfill_pace_delta_v2.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
010_ls_predictions_first_class.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
011_wr_predictions_unique_fix.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
```

**Decomposition (12 migration files):**

- **3 migrations (001, 002, 003)** have real, descriptive commit dates from 2026-03-15:
  - `001_initial_schema.sql` — `2026-03-15 0bb2a6d Initial commit — complete Equine Equalizer application`
  - `002_fix_race_type_length.sql` — `2026-03-15 d93c4c4 Fix post_time TIMESTAMPTZ, race_type length, and connection isolation`
  - `003_widen_varchar_columns.sql` — `2026-03-15 2a3d758 Widen VARCHAR columns and isolate per-race DB connections`
- **9 migrations (004 through 011)** have only the baseline commit `87dec36` dated `2026-05-04` ("Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.").

**Per META_PLAN v9 § 7.3 placeholder-resolution sub-rule application:**

- **8.W.1 (migration 011) Fix date = 2026-05-04.** The baseline commit `87dec36` is the only commit affecting `011_wr_predictions_unique_fix.sql`; per § 7.3, the canonical W.N Fix date is the git-log commit date.
- **8.W.2 (migration 002) Fix date = 2026-03-15.** Migration 002 has a real, descriptive commit `d93c4c4` dated 2026-03-15 ("Fix post_time TIMESTAMPTZ, race_type length, and connection isolation"); per § 7.3, this is the canonical W.N Fix date — NOT the baseline commit.

**Provenance of v1-patched rewrite.** v1's V1-8 entry asserted that migration 002's `git log` returned the same baseline-commit date as migration 011 ("Same date applies to 8.W.2 ..."). Audit-CC's independent re-run showed migration 002 returns the descriptive commit `d93c4c4` dated 2026-03-15, NOT the baseline. Per audit-CC's D-3.1 BLOCKER finding (`database_schema_bible_v1_audit.md`), the v1 V1-8 parity assertion was fabricated (the command was either not run for migration 002 or the output was misreported). Per Tony's ratification 2026-05-05, this entry is rewritten in-place with the verbatim per-migration sweep output and the bible's § 8.W.2 Fix date is corrected from 2026-05-04 to 2026-03-15. Lesson 13 (verbatim-paste discipline) banked in AUDIT_METHODOLOGY.md.

**Source-tier:** Tier 4 (git log of the working tree post-baseline 87dec36).

### V1-9: Calibration bypass at wr_inference_service.py:616-626

**Claim:** Calibration bypass comment block at lines 616–625 + bypass operation at line 626.

**Verification command:**

```
sed -n '614,628p' backend/services/wr_inference_service.py
```

**Verification output (2026-05-05):**

```
614            pp_counts = {r['hid']: r['n'] for r in cur.fetchall()}
615
616        # ── Calibration BYPASS (BUG #15 + BUG #24) ────────────────────────
617        # All styles (including gonzo_sauce) bypass calibration at inference
618        # tonight. Original Phase A3 plan was to apply gonzo's fitted
619        # ranker calibration here, but that surfaced Bug #24: isotonic
620        # mapping of legitimate-PP horses' ranker_probs (≈ base_rate) to
621        # near-zero, then 0-PP override at 1/field_size dominates after
622        # renormalize → 0-PP horses become top picks (Wonder Dean JPN at #1
623        # in Derby smoke test). Gonzo joins the legacy bypass until the
624        # Phase A3.5 fix splits 0-PP horses out of the calibration path
625        # entirely. Calibration sidecar remains in S3 for A3.5 use.
626        handicapping_probs = ranker_probs.copy()
627
628        # ── Patch (β): 0-PP override AFTER calibration ────────────────────
```

**Decomposition:** 10-line comment block (lines 616–625) + 1-line bypass operation (line 626). Confirmed prose at line 617: "All styles (including gonzo_sauce) bypass calibration at inference".

**Cross-reference:** This bible references the calibration mechanism at `database_schema_bible:4.1.10` (legacy `predictions` table) and § 4.1.12 (`wr_predictions` writer side); calibration semantics canonical home is `ml_layer_architecture_bible:4.3` per `architecture_overview:4.3`.

**Source-tier:** Tier 4.

### V1-10: Architecture Overview § 4.1 canonical objects line numbers (cross-referenced via section-anchor per Check 8)

**Claim:** Architecture Overview v3 § 4.1 enumerates 6 canonical objects with line numbers Race=255, Entry=214, PastPerformance=77, Workout=58, Result=296, Prediction=428.

**Verification command:** direct read of `/home/strakajagr/projects/equine-equalizer/docs/bible/architecture_overview.md` § 4.1.

**Verification output (2026-05-05):** confirmed at `architecture_overview:4.1` table — Race=255, Entry=214, PastPerformance=77, Workout=58, Result=296, Prediction=428.

**Decomposition:** 6 canonical objects enumerated; line numbers cited via Architecture Overview's existing § 4.1 enumeration. **This bible cross-references via section-anchor (`architecture_overview:4.1`) NOT by literal line number per Check 8 line-shift-resistant citations.** Per H8 self-audit, literal line numbers are retained ONLY where canonical-substrate identification requires them (e.g., this bible's substrate verification log entry V1-9 cites `wr_inference_service.py:616-626`). Cross-references to other bibles use section IDs only.

**Source-tier:** Tier 5 (operator-stated, since the canonical references substrate is an upstream-locked bible's enumeration).

### V1-11: Legacy `predictions` table reader inventory re-verification

**Claim:** Legacy `predictions` table active readers are: prediction_router.py (1 import + 3 instantiations = 4 refs), race_router.py (1 import + 1 instantiation = 2 refs), dashboard_router.py (2 SELECTs at lines 93, 105), horse_router.py (1 SELECT at line 66).

**Verification command:**

```
grep -nE "(import.*PredictionRepository|PredictionRepository\(|FROM predictions\b)" \
  backend/routers/prediction_router.py \
  backend/routers/race_router.py \
  backend/routers/dashboard_router.py \
  backend/routers/horse_router.py

grep -nE "PredictionRepository" backend/routers/prediction_router.py
```

**Verification output (2026-05-05):**

- `backend/routers/prediction_router.py:6`: import (`PredictionRepository` import line)
- `backend/routers/prediction_router.py:34, 61, 92`: three `repo = PredictionRepository(conn)` instantiations
- `backend/routers/race_router.py:273`: import (`PredictionRepository` import line)
- `backend/routers/race_router.py:277`: `pred_repo = PredictionRepository(conn)` instantiation
- `backend/routers/race_router.py:143, 144`: separate `WRPredictionRepository` import + instantiation (NOT a legacy `predictions` reference; documented separately as a per-style WR reader)
- `backend/routers/dashboard_router.py:93`: `(SELECT COUNT(*) FROM predictions)` direct SELECT
- `backend/routers/dashboard_router.py:105`: `FROM predictions p` direct SELECT (race-record summary)
- `backend/routers/horse_router.py:66`: `FROM predictions p` direct SELECT (horse-PPs query)

**Decomposition:**

- prediction_router.py: 1 import + 3 instantiations = **4 references**
- race_router.py: 1 import + 1 instantiation = **2 references** (plus 2 separate WRPredictionRepository refs at lines 143, 144 which are distinct readers of `wr_predictions`, NOT the legacy table)
- dashboard_router.py: 2 SELECT statements (lines 93, 105) = **2 references**
- horse_router.py: 1 SELECT statement (line 66) = **1 reference**
- Total reader-side refs: 4+2+2+1 = **9 references across 4 router files**

**Drift check:** META_PLAN v9 Appendix A.4 inheritance enumerated the same 4 router files with the same line numbers. **No drift.** The inventory at lock matches the inherited inventory.

**Source-tier:** Tier 4.

### V1-12: Legacy `predictions` table row count (live API verification)

**Claim:** Legacy `predictions` table holds 6,600 rows at lock (verified 2026-05-05 via dashboard endpoint).

**Verification command:**

```
GET https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com/dashboard/metrics
```

**Verification output (2026-05-05):**

```json
"counts": {
  "races": 25051,
  "horses": 43745,
  "entries": 198390,
  "results": 196316,
  "past_performances": 196262,
  "predictions": 6600,
  "earliest_date": "2022-01-01",
  "latest_date": "2026-05-03"
}
```

**Decomposition:** `counts.predictions` = **6600** (matches META_PLAN v9 inheritance exactly). Other counts surfaced in same response (races=25051, horses=43745, entries=198390, results=196316, past_performances=196262) are not directly cited in this bible's body but corroborate the dashboard's general health and the `equine-inference` Lambda's Active state per `architecture_overview:3.1`. Date range: 2022-01-01 through 2026-05-03 (latest race covered).

**Source-tier:** Tier 2 (live API endpoint via `equine-inference` Active Lambda).

### V1-13: trainer_stats matview reader is feature_engineering_service._get_trainer_stats

**Claim:** The `trainer_stats` materialized view's primary reader is `feature_engineering_service._get_trainer_stats()` at `backend/services/feature_engineering_service.py:1124`.

**Verification command:**

```
grep -n "trainer_stats\|_get_trainer_stats" backend/services/feature_engineering_service.py
```

**Verification output (2026-05-05):**

- `backend/services/feature_engineering_service.py:61`: `self._trainer_stats_cache: dict = {}` (cache initialization in service `__init__`)
- `backend/services/feature_engineering_service.py:724`: `stats = self._get_trainer_stats(trainer_name)` (call site)
- `backend/services/feature_engineering_service.py:1124`: `def _get_trainer_stats(` (method definition)
- `backend/services/feature_engineering_service.py:1130, 1131`: cache hit-check logic
- `backend/services/feature_engineering_service.py:1142`: `   FROM trainer_stats` (SQL FROM clause)
- `backend/services/feature_engineering_service.py:1146`: cache populate
- `backend/services/feature_engineering_service.py:1150-1153`: log + None fallback on lookup failure

**Decomposition:** 1 method definition (line 1124) + 1 call site (line 724) + 1 SQL FROM trainer_stats clause (line 1142) + cache management (lines 61, 1130, 1131, 1146, 1153). Single reader; no other production code path queries `trainer_stats`.

**Source-tier:** Tier 4.

### V1-14: ls_prediction_repository.py:insert_prediction has stale ON CONFLICT clause (dead code per migration 010)

**Claim:** The `insert_prediction` method at `backend/repositories/ls_prediction_repository.py:282` declares `ON CONFLICT (entry_id) DO UPDATE SET ...` (line 301), which does NOT match the post-migration-010 UNIQUE constraint `(race_id, entry_id, style)`. Per migration 010 preamble, the method has never been called — so the stale clause is dead code, not an active bug.

**Verification command:**

```
grep -nE "INSERT INTO|ON CONFLICT" backend/repositories/ls_prediction_repository.py
```

**Verification output (2026-05-05):**

- `backend/repositories/ls_prediction_repository.py:287`: `INSERT INTO ls_predictions (`
- `backend/repositories/ls_prediction_repository.py:301`: `ON CONFLICT (entry_id) DO UPDATE SET`
- Migration 010 preamble (line 5): "ls_predictions has been an orphan since the LS service was introduced. Its `insert_prediction` repo method has never been called; LS data has been written as enrichment columns on wr_predictions ..."
- The actual production write path is `backend/services/ls_inference_service.py:388-401` which uses `ON CONFLICT (race_id, entry_id, style) DO UPDATE SET ...` (matches post-migration-010 constraint).

**Decomposition:** 1 stale ON CONFLICT clause in dead repo code (line 301); 1 correct ON CONFLICT clause in production service code (`ls_inference_service.py:401`). Documented in `database_schema_bible:4.1.14` as a code-cleanup observation, NOT a schema-discipline issue.

**Source-tier:** Tier 4.

### V1-15: Per-pipeline prediction repo writers match canonical UNIQUE patterns

**Claim:** The three per-pipeline prediction repos use upsert ON CONFLICT clauses matching their tables' current UNIQUE constraints.

**Verification command:**

```
grep -nE "INSERT INTO|ON CONFLICT|UPDATE " \
  backend/repositories/wr_prediction_repository.py \
  backend/repositories/pl_prediction_repository.py \
  backend/repositories/ls_prediction_repository.py
```

**Verification output (2026-05-05):**

- `wr_prediction_repository.py:293`: `INSERT INTO wr_predictions (` ; line 313: `ON CONFLICT (race_id, entry_id, style) DO UPDATE SET` (matches post-migration-011)
- `pl_prediction_repository.py:255`: `INSERT INTO pl_predictions (` ; line 272: `ON CONFLICT (race_id, entry_id, style) DO UPDATE SET` (matches live state per V1-7b)
- `ls_prediction_repository.py:287`: `INSERT INTO ls_predictions (` ; line 301: `ON CONFLICT (entry_id) DO UPDATE SET` (STALE per V1-14; live ls writes go through `ls_inference_service.py:388-401`)

**Decomposition:** 3 INSERT INTO clauses across 3 repos (1 per per-pipeline table); 3 ON CONFLICT clauses; 2 match current schema (wr, pl); 1 is stale dead code (ls repo). The actual ls production write path is in the service layer, not the repo layer.

**Source-tier:** Tier 4.

### V1-16: Bug #28 cross-reference at § 6 (single occurrence)

**Claim:** This bible's § 6 contains exactly one `Bug #28` cross-reference, formatted as `Bug #28 NULL payout fields in results table — canonical: data_pipeline_bible:#28`.

**Verification command:**

```
grep -c "Bug #28" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
```

**Expected output:** 1 (the single cross-reference at § 6).

**Actual output (post-draft 2026-05-05):** 1. ✅ Pass.

**Pre-edit state:** 2 occurrences (the second was at § 4.1.9 `results` table's "Currently Open touching this table" block; identified during post-draft Check 9 verification and rephrased to point to § 6 without literal "Bug #28" prose).

**Per Check 9 bash-grep prediction precision:** total = 1, targeted-by-this-draft = 1 (CC writes the single cross-reference at § 6). If total > 1 in a future draft, that would be a duplication forbidden by BIBLE_STRUCTURE_SPEC v6 § 5.3.

**Source-tier:** Tier 4 (this draft's own text).

### V1-17: G-new-2 closure verified — `trainer_stats` does NOT appear at any § 4.1.X position

**Claim:** Per G-new-2 closure operative (drafting spec § 1.1 paste-prompt), the materialized view `trainer_stats` is documented at § 3.2 only and does NOT appear at any § 4.1.X position.

**Verification command:**

```
awk '/^### 4\.1/,/^### 4\.2/' /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md \
  | grep -c "trainer_stats"
```

**Expected output:** 0 (zero hits in the § 4.1 region).

**Actual output (post-draft 2026-05-05):** 0. ✅ Pass.

**Pre-edit state:** 3 occurrences in the § 4.1 region (1 at the § 4.1 disclaimer paragraph; 1 at § 4.1.3 `trainers` reader prose; 1 at § 4.1.7 `past_performances` reader prose). Identified during post-draft Check 9 verification; rephrased each occurrence to refer to "the materialized view (§ 3.2)" / "the matview at § 3.2" / "trainer-statistics matview (§ 3.2)" forms that preserve the cross-reference without using the literal `trainer_stats` substring inside the § 4.1 region. The matview's name `trainer_stats` is preserved in § 3.2 (the canonical home), in § 4.2.1 (the migration enumeration row), and in cross-references outside the § 4.1 region.

**Total `trainer_stats` references in the bible (verified post-edit 2026-05-05):** 11 (all outside § 4.1 — at § 3.2, § 4.2.1, the V1-13 verification log entry, etc.).

**Per Check 9:** the G-new-2 closure explicitly mandates 0 hits at § 4.1.X for `trainer_stats`. If non-zero, the draft violates G-new-2.

**Source-tier:** Tier 4 (this draft's own text).

### V1-18: `angle_stats` column-list substrate (asserted-from-handler-INSERT-tuples-not-empirically-verified per PHASE 1 Approach B fallback)

**Claim:** The `angle_stats` table columns referenced by all 6 production INSERT statements at `backend/lambdas/ingestion/handler.py:94-188` are `(angle_name, trainer_name, track_code, wins, starts)`, with types asserted from INSERT-tuple-substrate and reader query patterns.

**Verification command (PHASE 1 Approach A — ATTEMPTED, FAILED):**

```
$ aws lambda get-function --function-name equine-ingestion --query "Configuration.{State:State,LastUpdateStatus:LastUpdateStatus,PackageType:PackageType,LastModified:LastModified}" --output json
{
    "State": "Inactive",
    "LastUpdateStatus": "Successful",
    "PackageType": "Image",
    "LastModified": "2026-05-02T15:45:37.000+0000"
}

$ aws lambda invoke --function-name equine-ingestion --cli-binary-format raw-in-base64-out --payload file:///tmp/payload_cols.json /tmp/out_cols.json
An error occurred (CodeArtifactUserFailedException) when calling the Invoke operation: ERROR: Lambda cannot initialize the provided container image. Verify the image.
```

**Approach A disposition:** the only Lambda with a `raw_query` action surface (per `grep -l "raw_query" backend/lambdas/*/handler.py` returning `backend/lambdas/ingestion/handler.py` only) is `equine-ingestion`, which is in Inactive state with a broken container image at this patch cycle. The other Active Lambdas (`equine-inference` family) use HTTP route dispatch without an arbitrary-SELECT action surface (verified via `grep "raw_query" backend/lambdas/inference/handler.py` returning zero matches; the inference handler at `backend/lambdas/inference/handler.py:43-71` dispatches on `path` / `method`, not on `event['action']`). The public API endpoint exposes only race / prediction routes, not arbitrary SQL. Approach A cannot be completed in this patch CC environment.

**Verification command (PHASE 1 Approach B — fallback, run from working tree 2026-05-06):**

```
$ sed -n '90,200p' /home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py
                })
            }

    # ── Refresh angle_stats table ──
    if action == 'refresh_angle_stats':
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM angle_stats")
                    cur.execute("""
                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
                        SELECT 'first_time_lasix', pp.trainer_name, NULL,
                          COUNT(*) FILTER (WHERE pp.finish_position = 1),
                          COUNT(*)
                        FROM past_performances pp
                        JOIN entries e ON pp.horse_id = e.horse_id
                        WHERE e.lasix_first_time = true
                          AND pp.finish_position IS NOT NULL AND pp.finish_position < 90
                        GROUP BY pp.trainer_name
                        HAVING COUNT(*) >= 5
                    """)
                    cur.execute("""
                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
                        SELECT 'first_time_lasix', NULL, NULL,
                          COUNT(*) FILTER (WHERE pp.finish_position = 1),
                          COUNT(*)
                        FROM past_performances pp
                        JOIN entries e ON pp.horse_id = e.horse_id
                        WHERE e.lasix_first_time = true
                          AND pp.finish_position IS NOT NULL AND pp.finish_position < 90
                    """)
                    # blinkers_on trainer-specific
                    cur.execute("""
                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
                        SELECT 'blinkers_on', pp.trainer_name, NULL,
                          COUNT(*) FILTER (WHERE pp.finish_position = 1),
                          COUNT(*)
                        FROM past_performances pp
                        JOIN entries e ON pp.horse_id = e.horse_id
                        WHERE e.blinkers_on = true
                          AND pp.trainer_name IS NOT NULL
                          AND pp.finish_position IS NOT NULL AND pp.finish_position < 90
                        GROUP BY pp.trainer_name
                        HAVING COUNT(*) >= 5
                    """)
                    cur.execute("""
                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
                        SELECT 'blinkers_on', NULL, NULL,
                          COUNT(*) FILTER (WHERE pp.finish_position = 1),
                          COUNT(*)
                        FROM past_performances pp
                        JOIN entries e ON pp.horse_id = e.horse_id
                        WHERE e.blinkers_on = true
                          AND pp.finish_position IS NOT NULL AND pp.finish_position < 90
                    """)
                    # class_drop trainer-specific
                    cur.execute("""
                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
                        SELECT 'class_drop', pp.trainer_name, NULL,
                          COUNT(*) FILTER (WHERE pp.finish_position = 1),
                          COUNT(*)
                        FROM past_performances pp
                        WHERE pp.purse IS NOT NULL
                          AND pp.trainer_name IS NOT NULL
                          AND pp.finish_position IS NOT NULL AND pp.finish_position < 90
                          AND EXISTS (
                            SELECT 1 FROM past_performances pp2
                            WHERE pp2.horse_id = pp.horse_id
                              AND pp2.race_date < pp.race_date
                              AND pp2.purse > pp.purse * 1.15
                          )
                        GROUP BY pp.trainer_name
                        HAVING COUNT(*) >= 5
                    """)
                    cur.execute("""
                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
                        SELECT 'class_drop', NULL, NULL,
                          COUNT(*) FILTER (WHERE pp.finish_position = 1),
                          COUNT(*)
                        FROM past_performances pp
                        WHERE pp.purse IS NOT NULL
                          AND pp.finish_position IS NOT NULL AND pp.finish_position < 90
                          AND EXISTS (
                            SELECT 1 FROM past_performances pp2
                            WHERE pp2.horse_id = pp.horse_id
                              AND pp2.race_date < pp.race_date
                              AND pp2.purse > pp.purse * 1.15
                          )
                    """)
                conn.commit()
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) as cnt FROM angle_stats")
                    count = cur.fetchone()
            return {'statusCode': 200, 'body': json.dumps({
                'refreshed': True, 'rows': count['cnt'] if isinstance(count, dict) else count[0]})}
        except Exception as e:
            logger.error(f"refresh_angle_stats failed: {e}", exc_info=True)
            return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
```

**Decomposition (per Approach B substrate):**

- 1 DELETE statement at line 98: `DELETE FROM angle_stats` (full-table wipe; no WHERE clause).
- 6 INSERT statements at lines 100, 112, 123, 136, 147, 165 — all using identical 5-column tuple form `INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts) SELECT ...`.
- 1 SELECT COUNT(*) at line 181: `SELECT COUNT(*) as cnt FROM angle_stats` (post-refresh row-count confirmation).
- Column types **asserted** (not empirically verified): `angle_name` TEXT/VARCHAR (literal angle keys 'first_time_lasix' / 'blinkers_on' / 'class_drop'); `trainer_name` TEXT/VARCHAR nullable (denormalized from `past_performances.trainer_name` per § 4.1.7 pattern; NULL written for the global-aggregation arm); `track_code` TEXT/VARCHAR/CHAR nullable (always NULL in current INSERT paths; column exists in the tuple form for forward-compatibility); `wins` INTEGER (`COUNT(*) FILTER (WHERE pp.finish_position = 1)`); `starts` INTEGER (`COUNT(*)`).
- PK / FK / UNIQUE / INDEX substrate **NOT extractable from handler.py + reader.py alone**; pending credential-authorized cycle.

**Reader-side substrate (corroborates column list):**

```
$ grep -A 4 "SELECT wins, starts FROM angle_stats" /home/strakajagr/projects/equine-equalizer/backend/services/ls_inference_service.py
                "SELECT wins, starts FROM angle_stats "
                "WHERE angle_name = %s AND trainer_name = %s",
                (angle, trainer_name))
            if not stats or int(stats.get('starts', 0)) < 5:
                # Fall back to global
--
                "SELECT wins, starts FROM angle_stats "
                "WHERE angle_name = %s AND trainer_name IS NULL",
                (angle,))
```

The reader exact-matches `angle_name` + `trainer_name` (or `trainer_name IS NULL` for the global arm). This corroborates the column-list substrate from the writer side.

**Bible content consuming this substrate:** § 3.1 third group (out-of-band tables) entry; § 4.1.15 Columns table + Primary writers + Primary readers paragraphs; § 6 Currently Open formalization-via-migration entry.

**Source-tier:** Tier 4 (working-tree code post-baseline 87dec36) for the asserted column list; Tier 3 (live database state) **NOT verified** at this patch cycle — pending credential-authorized cycle for type / constraint / index re-verification.

### V1-19: `angle_stats` out-of-band substrate confirmation (zero matches in tracked schema sources)

**Claim:** The `angle_stats` table is NOT declared in `backend/database/schema/schema.sql` and NOT declared in any of the 12 tracked migration files at `backend/database/migrations/*.sql`. This confirms the F.4 substrate from Data Pipeline Bible v1-patched-a verification log is still operative at the v1-patched-d2 patch cycle (2026-05-06).

**Verification command (run from working tree 2026-05-06):**

```
$ grep -rn "angle_stats" /home/strakajagr/projects/equine-equalizer/backend/database/
$ echo $?
1
```

**Verification output:** zero matches. Grep exit code 1 = no matches found. The `backend/database/` tree (`schema/schema.sql` + 12 migration files in `migrations/`) does not reference `angle_stats` in any form.

**Pre-patch bible state confirmation:**

```
$ grep -n -i "angle_stats\|angle.stats" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
$ echo $?
1
```

(Run before the v1-patched-d2 edits applied; zero matches = the bible at v1-patched-d1 lock did not reference `angle_stats`.)

**Decomposition:**

- `schema.sql`: 0 matches (the file declares 11 tables per V1-1; `angle_stats` is not among them).
- `migrations/*.sql`: 0 matches across all 12 migration files (001 through 011 + the duplicate-005 sibling per V1-3).
- Pre-patch `database_schema_bible.md`: 0 matches at v1-patched-d1 lock (confirms the patch is adding new content, not modifying existing).

**Implication:** the table was created out-of-band — neither in the tracked schema bootstrap file nor in any tracked migration. This is the F.4 substrate as ratified by Tony 2026-05-06: the upstream Data Pipeline Bible v1-patched-a verification log § F.4 surfaced this gap, and the routing decision (UPSTREAM-CORRECTION class) lands the substrate-capture in this bible's v1-patched-d2 patch cycle.

**Bible content consuming this substrate:** § 3.1 third group prose (`out-of-band; no tracked migration declares it at lock`); § 4.1.15 Substrate-capture provenance paragraph; § 6 Currently Open formalization-via-migration entry.

**Source-tier:** Tier 4.

### V1-20: `angle_stats` handler-substrate confirmation (≥ 10 matches at handler.py)

**Claim:** Production handler at `backend/lambdas/ingestion/handler.py` references `angle_stats` extensively (≥ 10 grep matches), confirming the primary-writer substrate per audit-CC v1-patched-a finding A3.

**Verification command (run from working tree 2026-05-06):**

```
$ grep -n "angle_stats" /home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py
93:    # ── Refresh angle_stats table ──
94:    if action == 'refresh_angle_stats':
98:                    cur.execute("DELETE FROM angle_stats")
100:                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
112:                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
123:                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
136:                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
147:                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
165:                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
181:                    cur.execute("SELECT COUNT(*) as cnt FROM angle_stats")
186:            logger.error(f"refresh_angle_stats failed: {e}", exc_info=True)
```

**Decomposition:** 11 grep matches at handler.py = 1 section comment (line 93) + 1 action-dispatch conditional (line 94) + 1 DELETE (line 98) + 6 INSERTs (lines 100, 112, 123, 136, 147, 165) + 1 SELECT COUNT(*) (line 181) + 1 error-log message (line 186). Exceeds the ≥ 10 threshold; confirms primary-writer substrate.

**Reader-side handler substrate (cross-corroborated):**

```
$ grep -rn "angle_stats" /home/strakajagr/projects/equine-equalizer/backend/ | grep -v "lambdas/ingestion/handler.py"
backend/services/ls_inference_service.py:528:        """Check angle flags and query angle_stats."""
backend/services/ls_inference_service.py:547:                "SELECT wins, starts FROM angle_stats "
backend/services/ls_inference_service.py:553:                    "SELECT wins, starts FROM angle_stats "
```

3 matches at `ls_inference_service.py` confirm the primary-reader substrate (§ 4.1.15 Primary readers paragraph).

**Bible content consuming this substrate:** § 3.1 third group purpose-prose; § 4.1.15 Primary writers + Primary readers + Cross-references paragraphs.

**Source-tier:** Tier 4.

---

## Section D: Methodology-interpolation self-check

**Target: ZERO new methodology constructs CC introduces beyond what this spec / upstream documents ratify.**

**v1 self-check (initial draft): claimed ZERO. Audit-CC D-1 finding refuted with 2 MATERIAL + 1 MINOR methodology-interpolation findings (D-1.1, D-1.2, D-1.3).**

**v1-patched self-check (post-patch independent re-scan, 2026-05-05): ZERO.**

The patched draft removes the three methodology-interpolations audit-CC flagged:

- **D-1.1 § 4.2.1 procedural sequencing** ("the per-author discipline ensures the next NNN slot is consulted (via `ls backend/database/migrations/`) before a filename is committed") — DELETED in V1-patch-2. Verified absent post-patch via `grep -nE "ls backend/database/migrations" database_schema_bible.md` returning zero matches (V1-patch-9).
- **D-1.2 § 4.2.4 procedural rollback workflow** ("manually executes the down-block SQL ... then manually `DELETE FROM schema_migrations`") — DELETED in V1-patch-3. Verified absent post-patch via `grep -nE "DELETE FROM schema_migrations" database_schema_bible.md` returning zero matches (V1-patch-9).
- **D-1.3 § 5.3 borderline-procedural last paragraph** ("Document the absence of `ON DELETE CASCADE` explicitly; if cascading deletes are desired, add them via migration with explicit reasoning in the migration preamble") — RESOLVED via Q3.3.c (entire § 5.3 deleted; replaced with forward-deferral note pointing to `data_pipeline_bible:5`). Verified absent post-patch via § 5 sub-section sweep returning § 5.1 + § 5.2 only (V1-patch-9).

Every methodology construct retained in the patched draft traces to an upstream-locked source:

- **9-check Option 1 framework + 3-cluster organization** — ratified in QB handoff § 3 + § 4 (upstream of this draft, locked 2026-05-05).
- **Lessons 1–6 (cross-project contamination, Phase 0 substrate-error pattern, primary-claim-ID citations, FRAMEWORK_GAP discipline, per-resource verification, synthesis verification)** — banked from META_PLAN v9 + Architecture Overview v3 cycles, ratified by Tony per QB handoff § 5.
- **G-new-1 (numeric sub-section IDs for candidate roster)** — Tony-locked per BIBLE_STRUCTURE_SPEC v6 § 5.7.
- **G-new-2 (CREATE TABLE-only enumeration scope at § 4.1)** — Tony-locked per BIBLE_STRUCTURE_SPEC v6 § 6.6 § 4.1 first-sentence qualification.
- **Tertiary-state notation (FIRES / DOES NOT FIRE / CONDITIONAL with adjacent-prose caveat)** — Tony-locked per BIBLE_STRUCTURE_SPEC v6 § 5.6.1.2 G7 closure. Used in `database_schema_bible:7.1` (Deprecated) and `database_schema_bible:8.W.1` + § 8.W.2 (What Was Fixed).
- **Source-priority hierarchy (Tier 1–7)** — Tony-locked per META_PLAN v9 § 4.5.
- **W.N format + section IDs** — Tony-locked per BIBLE_STRUCTURE_SPEC v6 § 5.5.
- **§ 5.7 candidate roster workflow** — Tony-locked per BIBLE_STRUCTURE_SPEC v6 § 5.7. The § 5 candidate roster header marker has been removed in v1-patched (Q3.1 + Q3.2 ratifications); § 5.1 + § 5.2 are now ratified rules; § 5.3 was deleted with forward-deferral to `data_pipeline_bible:5` (Q3.3.c).

**No CC-introduced binary tests.** The 8.W.1 + 8.W.2 entries use FIRES / DOES NOT FIRE / CONDITIONAL exactly as specified by § 5.6.1.2 — no new states added.

**No CC-prescribed cadence rules.** This draft does not assert refresh schedules, rebuild cadences, or audit cycles beyond what META_PLAN v9 + BIBLE_STRUCTURE_SPEC v6 ratify. The `trainer_stats` matview refresh discipline section explicitly says "manual ... no automated refresh schedule at lock — disposition is operator-driven; per-flow refresh integration into the daily ingestion pipeline is candidate Phase 5 work" rather than CC prescribing a cadence.

**No CC-prescribed completeness criteria.** Per-table sections enumerate substrate-grounded fields (column list, PK, UNIQUE, FK, indexes, JSONB, purpose, primary writers, primary readers); these match BIBLE_STRUCTURE_SPEC v6 § 6.6 mandatory + conditional fields exactly.

**No CC-prescribed severity thresholds.** Bug #28 is referenced as cross-cutting (canonical home elsewhere); the multi-active-row issue at § 6 is surfaced as Currently Open with substrate-grounded descriptive language, not assigned a CC-prescribed severity tier.

**No CC-prescribed iteration caps or percentage criteria.** This draft makes no quantitative completeness claims beyond substrate-grounded counts (14 tables, 1 matview, 12 migrations, 6 JSONB columns, 25 CREATE TABLE statements on disk, 6,600 row count).

---

## Section E: Pattern-completion check (W.N exclusivity preserved; numeric IDs honored per § 5.5 + G-new-1)

**Self-check result: ZERO new letter-prefixes; numeric IDs honored throughout.**

- **W.N exclusivity:** § 8 entries use `8.W.1` and `8.W.2` per BIBLE_STRUCTURE_SPEC v6 § 5.5 (the only ratified letter-prefix in EE bible numbering).
- **Forbidden Pattern at § 5.1:** numeric ID `5.1` (NOT `5.F.1` or `5.A` or any other letter-prefix); ratified in v1-patched per Q3.1.
- **JSONB conventions at § 5.2:** numeric ID `5.2` (NOT `5.J.1`); ratified in v1-patched per Q3.2.
- **Deprecated entry at § 7.1:** numeric ID `7.1` (NOT `7.D.1`).
- **§ 5 candidate roster header marker:** REMOVED in v1-patched per Q3.1 + Q3.2 ratifications (markers no longer needed once candidates are ratified). § 5.3 deleted entirely per Q3.3.c with forward-deferral note to `data_pipeline_bible:5`. G-new-1 closure operative throughout.
- **Cross-bible bug references:** use `<bible>:#<bug-id>` per BIBLE_STRUCTURE_SPEC v6 § 5.5.1 — e.g., `data_pipeline_bible:#28` at § 6.

**No new section-numbering letter-prefixes introduced.** No new cross-reference syntax extensions introduced.

---

## Section F: FRAMEWORK_GAP / SPEC_GAP markers

**Three FRAMEWORK_GAP markers (F.1 / F.2 / F.3) surfaced honestly with substrate-cited candidate reframing per Lesson 4. All three Tony-ratified 2026-05-05.** No SPEC_GAP markers (the spec's premise is sound; the gaps surfaced are framework-slot mismatches, not invalidation of the spec).

### F.1 <FRAMEWORK_GAP: schema.sql ↔ 001_initial_schema.sql byte-identity not anticipated by spec V1-1 grep prediction>

**Substrate (per V1-1a):** The spec § 1.1 paste-prompt's V1-1 verification command `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql | grep -v "schema_migrations" | wc -l` expects "14 plus possibly the `IF NOT EXISTS` patterns; verify count and decompose explicitly per Check 9." The actual count is 25 CREATE TABLE statements on disk because `schema.sql` and `001_initial_schema.sql` are byte-identical (`diff` returns empty; both are 415 lines).

**Reframing candidate (CC-presented; substrate-cited):** The spec's "11 in schema.sql + 3 in 005 = 14" decomposition is correct *as a count of distinct domain tables*. A precise restatement: "11 distinct domain tables declared in schema.sql (mirrored byte-identically in `001_initial_schema.sql`, so 22 statements on disk) + 3 distinct domain tables declared in `005_three_prediction_tables.sql` = 14 distinct domain tables; total CREATE TABLE statements on disk = 25." Documented in this bible at § 3.3 with three operational interpretations of the schema.sql ↔ 001 mirror (reference snapshot / runner-compatible packaging / parallel-source coexistence).

**Resolution requested from QB:** confirm that the 14-distinct-domain-table count is the canonical claim and the 25-on-disk count is supplementary substrate detail (not contradictory). If QB wants V1-1's grep prediction updated in the spec for future cycles to handle the byte-identity case, that's a spec-side correction; this draft documents the substrate accurately.

**Substrate citation supporting the reframing:** `diff /home/strakajagr/projects/equine-equalizer/backend/database/schema/schema.sql /home/strakajagr/projects/equine-equalizer/backend/database/migrations/001_initial_schema.sql ; echo "DIFF EXIT: $?"` returns empty + exit code 0 (V1-1a). `wc -l` on both files returns 415 lines each.

**Substrate citation refuting alternative reframings:** the count of "14 distinct CREATE TABLE statements" (a possible alternative) is NOT supported by substrate; there are 25 statements on disk. The substrate supports "14 distinct domain table names" as the union (set), not as a statement count.

**Tony ratification 2026-05-05:** Tony ratified F.1 on 2026-05-05; bible content stands; prediction-precision lesson banked in AUDIT_METHODOLOGY.md.

### F.2 <FRAMEWORK_GAP: wr_predictions / pl_predictions style + model_used columns not declared in tracked migrations>

**Substrate (per V1-7a + V1-7b):** Migration 011's UNIQUE constraint on `wr_predictions` references `style` and `model_used` columns. Migration 005's CREATE TABLE for `wr_predictions` does not declare them. No tracked migration in `backend/database/migrations/` declares `wr_predictions ADD COLUMN style` or `wr_predictions ADD COLUMN model_used`. Migration 010 declares `style` for `ls_predictions` only. The same gap exists for `pl_predictions.style` (per V1-7b: `pl_prediction_repository.py:272` uses `ON CONFLICT (race_id, entry_id, style)` upsert syntax, requiring the column and a matching UNIQUE constraint to exist on the live table).

**Reframing candidate (CC-presented; substrate-cited):** The working-tree migration history is incomplete relative to the live schema. There is at least one out-of-band script that ALTER'd `wr_predictions` and `pl_predictions` to add the `style` and `model_used` columns + replace the inline `UNIQUE(entry_id)` with a multi-column UNIQUE — and the script was applied to production but never committed as a migration file. Migration 011 still applies cleanly because its DROP CONSTRAINT is `IF EXISTS` (idempotent) and its post-state validation only checks for the new constraint's existence, not the prior constraint's exact form.

**Resolution requested from QB:** confirm whether (a) this should be documented as a Currently Open issue in this bible's § 6 (operator-historical schema drift; missing migration files for tracked schema state); (b) routed to PHASE_5_BACKLOG.md as remediation work (commit the missing schema state as a backfill migration with name prefix higher than 011); or (c) accepted as a known-substrate-gap noted only in the verification log without bible-text surfacing beyond the existing § 4.1.12 + § 4.1.13 prose. This draft's current treatment is (c): the substrate gap is noted in § 4.1.12 + § 4.1.13 prose with neutral language ("via an out-of-band script not preserved as a tracked migration") and surfaced here in Section F for QB triage.

**Substrate citation supporting the reframing:** V1-7a's grep output (zero `ADD COLUMN style|model_used` in migrations); V1-7b's grep output (`pl_prediction_repository.py:272` uses `ON CONFLICT (race_id, entry_id, style)`).

**Substrate citation refuting the alternative "the bible should not document the gap":** per META_PLAN v9 § 8.6 no-fabrication rule, the bible cannot describe `wr_predictions` columns that don't exist in tracked sources without acknowledging the source-tier mismatch. Documenting the gap honestly (neutral language at § 4.1.12 + Section F surfacing) preserves verification log integrity.

**Tony ratification 2026-05-05:** Tony ratified Option C on 2026-05-05; bible content stands; queued for PHASE_5_BACKLOG.md addition at Phase 0 exit alongside Bug #28 first-entry.

### F.3 <FRAMEWORK_GAP: ls_prediction_repository.py cross-table read pattern (LS class methods reading FROM wr_predictions)>

**Substrate (audit-CC's V1-14 finding + audit-CC re-verification 2026-05-05):**

```
$ grep -nE "FROM wr_predictions|FROM ls_predictions" backend/repositories/ls_prediction_repository.py
98:               FROM ls_predictions p
158:               FROM ls_predictions p
262:               FROM wr_predictions p
374:               FROM wr_predictions p
```

The `LSPredictionRepository` class (defined at `ls_prediction_repository.py:42`) contains 4 methods that issue read queries against the database. Two read FROM `ls_predictions` (`get_predictions_by_race` line 50; `get_predictions_by_date` line 115); two read FROM `wr_predictions` (`get_longshot_alerts_by_date` line 184; `get_track_record` line 345). Plus the dead-code `insert_prediction` (line 282) which inserts into `ls_predictions` with a stale `ON CONFLICT (entry_id)` clause that doesn't match the post-migration-010 UNIQUE constraint.

The class docstring at lines 199-204 explicitly notes: "LS data is written as second-pass enrichment to wr_predictions columns (ensemble_win_prob, longshot_prob, trajectory_score, angle_*, longshot_alert, confidence) — not to a separate ls_predictions table. Columns are aliased here to match the LSPrediction dataclass schema so _build_ls_prediction_list works unchanged."

**Reframing candidate (CC-presented; substrate-cited):** the bible's per-table reader-inventory frame assumes one repository module ↔ one table. The LS repo violates this: it reads from two tables. The bible's v1 § 4.1.14 Primary readers compressed this as "(read methods; insert_prediction is dead per above)" — too oblique. The patched § 4.1.14 enumerates per-method read targets with line citations. Symmetrically, § 4.1.12 (wr_predictions) acknowledges LSPredictionRepository's cross-table reads at lines 262 and 374.

**Substrate citation supporting the reframing:** the grep output above (4 read clauses + 1 INSERT clause across 1 file) and the docstring at lines 199-204 (explanation of why LS reads from wr_predictions in two methods).

**Substrate citation refuting alternative reframings:** the alternative "list LSPredictionRepository as a wr_predictions reader without enumerating which methods" is too compressed (does not surface that 2 of 4 active methods read wr_predictions); the alternative "refactor the LS repo so it does not read wr_predictions" is a Phase 5 disposition, not a documentation correction.

**Tony ratification 2026-05-05:** Tony ratified R2.3.a + queue for PHASE_5_BACKLOG.md on 2026-05-05. Bible documents the substrate observation at § 4.1.12 + § 4.1.14; F.3 queues for PHASE_5_BACKLOG.md addition at Phase 0 exit alongside Bug #28 first-entry, F.2, and any other Phase 1 cycle-surfaced entries. Phase 5 disposition: refactor LS reads or create separate repo for the enrichment-read pattern.

---

## Section G: Prior-cycle audit findings closure verification

**NOT APPLICABLE for v1 — first cycle.**

---

## Section H: QB self-audit log (char-exact reproduction of drafting spec § 6 H1–H9)

The 9 entries below reproduce the QB self-audit log from `database_schema_bible_v1_drafting_spec.md` § 6 char-exact per QB handoff § 7.2.

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

## Section I: New entries for surgical patch operations

**APPLICABLE in v1-patched.** Eight V1-patch-N entries below cover the patch operations applied 2026-05-05 per Tony's ratifications. Each entry pastes verbatim command output per Lesson 13 (verbatim-paste discipline; banked in AUDIT_METHODOLOGY.md as § 4.10).

### V1-patch-1: D-3.1 BLOCKER fix substrate sweep (per-migration git log)

**Patch operation:** Bible § 8.W.2 Fix date corrected from 2026-05-04 to 2026-03-15. Verification log Section C V1-8 entry rewritten in-place to replace v1's parity-assertion-with-fabrication-pattern with the verbatim per-migration substrate sweep.

**Verbatim verification command + output (run from working tree 2026-05-05):**

```
$ for f in backend/database/migrations/*.sql; do printf "%s\t" "$(basename $f)"; git log --format="%cs %h %s" -- "$f" | head -1; done
001_initial_schema.sql	2026-03-15 0bb2a6d Initial commit — complete Equine Equalizer application
002_fix_race_type_length.sql	2026-03-15 d93c4c4 Fix post_time TIMESTAMPTZ, race_type length, and connection isolation
003_widen_varchar_columns.sql	2026-03-15 2a3d758 Widen VARCHAR columns and isolate per-race DB connections
004_backfill_running_style.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
005_backfill_pace_delta.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
005_three_prediction_tables.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
006_backfill_early_pace_pressure.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
007_backfill_trainer_name.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
008_create_trainer_stats.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
009_backfill_pace_delta_v2.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
010_ls_predictions_first_class.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
011_wr_predictions_unique_fix.sql	2026-05-04 87dec36 Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved.
```

**Decomposition (12 migration files):** 3 migrations (001, 002, 003) with real 2026-03-15 commits + 9 migrations (004 through 011) with baseline-commit-only 2026-05-04 = 12. Migration 002's commit `d93c4c4` is descriptive ("Fix post_time TIMESTAMPTZ, race_type length, and connection isolation") and predates the baseline commit by ~7 weeks; 8.W.2 Fix date = 2026-03-15 per META_PLAN v9 § 7.3.

**Cite for cross-reference:** `database_schema_bible_v1_audit.md` § B (V1-8 DRIFT finding) + § D (D-3.1 BLOCKER).

**Source-tier:** Tier 4 (git log of the working tree post-baseline 87dec36).

### V1-patch-2: D-1.1 § 4.2.1 procedural-sequencing prose deletion

**Patch operation:** § 4.2.1 "Forward rule (Phase 5 onward)" paragraph trimmed to remove CC-introduced procedural sequencing.

**Verbatim deleted prose (audit-CC D-1.1 quote):**

> "the per-author discipline ensures the next NNN slot is consulted (via `ls backend/database/migrations/`) before a filename is committed."

**Verbatim retained prose:**

> "Forward rule (Phase 5 onward). No new migrations may share an NNN-prefix with an existing migration. The new `NNN_YYYYMMDD_*.sql` format from migration 012+ trivially prevents recurrence: the date component disambiguates same-day siblings via prefix uniqueness."

**Cite for cross-reference:** `database_schema_bible_v1_audit.md` § D-1.1; META_PLAN v9 § 6.1 (methodology-interpolation rule, named pattern: procedural sequencing rules); META_PLAN v9 § 7.12 (the rule is "no new duplicates"; enforcement mechanism is unspecified upstream).

**Source-tier:** Tier 4 (this draft's own text post-patch).

### V1-patch-3: D-1.2 § 4.2.4 rollback-workflow procedural-sequencing prose deletion

**Patch operation:** § 4.2.4 rewritten to retain only what META_PLAN v9 § 7.12 lines 864-867 actually prescribe.

**Verbatim deleted prose (audit-CC D-1.2 quote):**

> "Each migration file may include an in-file down-block — typically a comment-delimited section labeled `-- DOWN MIGRATION` or similar that documents the inverse SQL operations.
> If a migration must be rolled back: the operator manually executes the down-block SQL against the affected database; then manually `DELETE FROM schema_migrations WHERE filename = '<rolled-back-file>'` so the next run can re-apply it (or so it's not re-applied if the rollback is permanent).
> If rollback is not feasible (e.g., a migration that DROP'd a column with data): the migration's preamble documents the irreversibility explicitly."

**Verbatim retained prose (post-patch):**

> "Per META_PLAN v9 § 7.12: rollback SQL lives in the **same migration file**, after the up SQL, in a clearly-delimited block. The migration runner does NOT auto-execute the down block. Rollback is operator-driven. The bible entry references the migration file; it does not duplicate the rollback SQL.
>
> If rollback is not feasible (e.g., a migration that DROP'd a column with data), the migration's preamble documents the irreversibility explicitly per META_PLAN v9 § 7.12 worked example for non-reversible migrations."

**Cite for cross-reference:** `database_schema_bible_v1_audit.md` § D-1.2; META_PLAN v9 § 6.1 + § 7.12 (lines 864-867).

**Source-tier:** Tier 4.

### V1-patch-4: R2.2.b § 4.1.X + § 7.1 reader-inventory compression

**Patch operation:** Per-table reader inventories at § 4.1.X defer router-level detail to `api_frontend_bible:4.1`; § 7.1 (Deprecated `predictions` table) compressed symmetrically.

**Verbatim before/after for § 7.1 (the most verbose v1 reader-enumeration):**

BEFORE (v1):

> "**Active readers re-verified 2026-05-05** (companion verification log claim V1-11):
>   - `prediction_router.py` — 1 import (line 6) + 3 `PredictionRepository(conn)` instantiations (lines 34, 61, 92) = 4 references total
>   - `race_router.py` — 1 import (line 273) + 1 instantiation (line 277) = 2 references total
>   - `dashboard_router.py:93,105` — 2 direct `FROM predictions` SELECT clauses (line 93 `(SELECT COUNT(*) FROM predictions)` produces the dashboard `counts.predictions` field; line 105 `FROM predictions p` for race-record summary)
>   - `horse_router.py:66` — 1 direct `FROM predictions p` SELECT in horse-PPs query
>
>   Plus the `prediction_repository.py` module which the routers import (1 reference internal to the module file itself, not counted in the consumer-side enumeration)."

AFTER (v1-patched):

> "Active readers: `prediction_router.py`, `race_router.py`, `dashboard_router.py`, `horse_router.py` plus the `prediction_repository.py` module. Per-route detail with import + instantiation + SELECT decomposition deferred to `api_frontend_bible:4.1`."

**Verbatim before/after for § 4.1.12 (representative § 4.1.X compression, with R2.3.a F.3 LS cross-table substrate added per Tony's ratification):**

BEFORE (v1):

> "**Primary readers.** `race_router.py` (per V1-11 inventory: 1 import at line 143 + 1 instantiation at line 144 — `WRPredictionRepository`, distinct from the legacy `PredictionRepository`); `wr_prediction_repository.py`; downstream LS softmax + ComparePage Cartesian + track_record consumers (per migration 011 preamble — these were the duplicate-row consumers that produced the 2026-04 incident, fixed by § 8.W.1). Per-route detail at `api_frontend_bible:4.1`."

AFTER (v1-patched):

> "**Primary readers.** `wr_prediction_repository.py` for the WR-specific repo surface. Cross-table reads from `ls_prediction_repository.py:262` (`get_longshot_alerts_by_date` — `FROM wr_predictions p`) and `ls_prediction_repository.py:374` (`get_track_record` — `FROM wr_predictions p`); these methods read `wr_predictions` despite living in the LSPredictionRepository class because LS data is currently second-pass enrichment on `wr_predictions` columns (per migration 010 preamble + verification log F.3). Migration 011 preamble names downstream LS softmax + ComparePage Cartesian + track_record consumers as the duplicate-row consumers fixed by § 8.W.1. Per-route detail at `api_frontend_bible:4.1`."

**Cite for cross-reference:** `database_schema_bible_v1_audit.md` § D-4.1 + § D-4.2; § 1 boundary statement ("per-route detail at api_frontend_bible:4.1").

**Source-tier:** Tier 4.

### V1-patch-5: R2.3.a F.3 LS cross-table read pattern documentation

**Patch operation:** F.3 added to verification log Section F (above) with substrate citation; § 4.1.12 + § 4.1.14 prose updated with concrete line citations (audit-CC D-8 finding addressed).

**Verbatim verification command + output (run 2026-05-05):**

```
$ grep -nE "FROM wr_predictions|FROM ls_predictions" backend/repositories/ls_prediction_repository.py
98:               FROM ls_predictions p
158:               FROM ls_predictions p
262:               FROM wr_predictions p
374:               FROM wr_predictions p
```

**Decomposition:** 4 read clauses across 1 file. 2 read FROM `ls_predictions` (lines 98, 158 — `get_predictions_by_race`, `get_predictions_by_date`). 2 read FROM `wr_predictions` (lines 262, 374 — `get_longshot_alerts_by_date`, `get_track_record`). Plus the dead-code `insert_prediction` at line 282 with stale `ON CONFLICT (entry_id)` (per V1-14).

**Cite for cross-reference:** `database_schema_bible_v1_audit.md` § D-8; bible § 4.1.12 (wr_predictions readers, post-patch) + § 4.1.14 (ls_predictions readers, post-patch); migration 010 preamble lines 1-18 (the LS-as-enrichment-on-wr_predictions architectural rationale).

**Source-tier:** Tier 4.

### V1-patch-6: D-9 § 4.2.5 self-contradiction removal

**Patch operation:** § 4.2.5 "Production target" sentence trimmed to remove duplicated RDS metadata and resolve the self-contradiction with the cross-reference.

**Verbatim before (v1):**

> "**Production target.** The standalone RDS PostgreSQL 16.6 instance `equine-db` (instance class `db.t4g.micro`, endpoint `equine-db.cgtuh834bttd.us-east-1.rds.amazonaws.com:5432`, database `equine_equalizer`). Cross-reference `architecture_overview:3.3` for the canonical instance metadata; this bible does not duplicate the metadata."

**Verbatim after (v1-patched):**

> "**Production target.** Cross-reference `architecture_overview:3.3` for the canonical RDS instance metadata (engine version, instance class, endpoint, database name); this bible does not duplicate the metadata."

**Cite for cross-reference:** `database_schema_bible_v1_audit.md` § D-9; bible § 1 boundary statement ("Per-runtime topology... → architecture_overview:3.3"); `architecture_overview:3.3` lines 105-111 (the canonical metadata enumeration that v1's § 4.2.5 was duplicating).

**Source-tier:** Tier 4.

### V1-patch-7: D-10 § 4.1.7 backfill enumeration completeness

**Patch operation:** § 4.1.7 backfill-migration enumeration corrected from "(004, 006, 009)" to "(004, 005's `005_backfill_pace_delta.sql`, 006, 009 — migration 009 superseded migration 005's pace_delta backfill because `finish_call_position` was 0%-populated; see § 4.2.1 + § 4.2.2 duplicate-005 case)".

**Verbatim verification command + output (migration 005 preamble; run 2026-05-05):**

```
$ head -6 backend/database/migrations/005_backfill_pace_delta.sql
-- Migration 005: Compute pace_delta from position change
-- pace_delta = finish_call_position - call_2_position
-- Negative = gained positions (good), consistent with the
-- existing convention where negative = accelerated.
-- Example: call_2=4, finish=1 → 1-4 = -3 (gained 3 spots)
-- transforms.py fallback now also uses this formula.
```

**Verbatim verification command + output (migration 009 preamble; run 2026-05-05):**

```
$ head -6 backend/database/migrations/009_backfill_pace_delta_v2.sql
-- Migration 009: Backfill pace_delta using finish_position
-- Migration 005 used finish_call_position (0% populated).
-- finish_position is 99.5% populated and semantically identical
-- (position at the wire). Valid finish codes are 1–30; codes >= 90
-- mean DNF/pulled/vet scratch and are excluded.
-- pace_delta = finish_position - call_2_position
```

**Decomposition:** Migration 005's preamble line 2 reads `pace_delta = finish_call_position - call_2_position`; migration 009's preamble line 2-3 reads "Migration 005 used finish_call_position (0% populated). finish_position is 99.5% populated and semantically identical." Migration 009 supersedes migration 005's pace_delta backfill due to the 0%-vs-99.5% column-population delta.

**Cite for cross-reference:** `database_schema_bible_v1_audit.md` § D-10; bible § 4.2.1 (migration enumeration) + § 4.2.2 (duplicate-005 case).

**Source-tier:** Tier 4.

### V1-patch-8: Q3.3.c § 5.3 deletion + forward-deferral note

**Patch operation:** § 5.3 (Common Mistake "writing to a child table without verifying parent row exists") deleted entirely; replaced with forward-deferral note pointing to `data_pipeline_bible:5`. § 5 lead paragraph updated from "three rules" to "two rules" + forward-deferral note. § 5.1 + § 5.2 title suffixes "(candidate; pending QB ratification)" removed per Q3.1 + Q3.2 ratifications. § 5 header marker `[candidate roster pending QB ratification per § 5.7]` removed.

**Verbatim deleted section (entire § 5.3 of v1):**

> "### 5.3 Common Mistake: writing to a child table without verifying parent row exists (candidate; pending QB ratification)
>
> **Wrong instinct:** *"the FK constraint will catch missing parents."*
>
> **Corrected position:** NO — but for a subtler reason than "the FK won't catch it." EE's FK constraints DO enforce parent presence at INSERT time (PostgreSQL default `NO ACTION` on foreign keys). The mistake is treating FK violation as the discoverability mechanism: the FK violation throws at INSERT, but the corrupted application state is the root issue. The `parent missing` condition is typically a symptom of a producer-order bug (an ingestion path that should have INSERT'd into `tracks` before `races`, into `races` before `entries`, etc.). Defensively asserting the parent exists at the producer (e.g., `INSERT ... ON CONFLICT DO NOTHING` for the parent first, then the child) makes the root cause visible at the producer layer rather than discoverable only via FK violation in production. EE uses UUID primary keys throughout; ON DELETE behavior is unspecified at the schema level (PostgreSQL default `NO ACTION`), so deletions of parent rows with extant children fail at DELETE time — operators relying on cascading deletes will be surprised. Document the absence of `ON DELETE CASCADE` explicitly; if cascading deletes are desired, add them via migration with explicit reasoning in the migration preamble.
>
> **Substrate provenance.** Per-table FK enumeration at § 4.1.5 / § 4.1.6 / § 4.1.7 / § 4.1.8 / § 4.1.9 / § 4.1.10 / § 4.1.12 / § 4.1.13 / § 4.1.14 — every FK in the schema declares `REFERENCES <parent>(<col>)` without an `ON DELETE` clause; PostgreSQL default is `NO ACTION`. The "verify parent exists" instinct mismatch is observable in the ingestion-side code patterns (per `data_pipeline_bible:4.1` once that drafts)."

**Verbatim replacement (post-patch):**

> "**Forward deferral note (Tony's Q3.3.c ratification 2026-05-05).** A candidate Common Mistake about producer-side parent-row verification before child INSERTs is canonically homed in `data_pipeline_bible:5` per BIBLE_STRUCTURE_SPEC v6 § 5.3 cross-cutting bug scope rule (the producer-side discipline is canonically homed where the producer's flow lives). Candidate-roster status pending data_pipeline_bible drafting cycle."

**Cite for cross-reference:** Tony's Q3.3.c ratification 2026-05-05; BIBLE_STRUCTURE_SPEC v6 § 5.3 (cross-cutting bug scope rule); audit-CC D-1.3 borderline finding (resolved by section deletion).

**Source-tier:** Tier 4 (this draft's own text post-patch).

### V1-patch-9: Step 6 post-patch verification sweep

**Patch operation:** independent re-verification across the patched bible draft confirms the patch surface is consistent. Verbatim outputs from each prescribed sweep command:

```
$ grep -c "Bug #28" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
1
```

```
$ awk '/^### 4\.1/,/^### 4\.2/' /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md | grep -c "trainer_stats"
0
```

```
$ grep -c "candidate; pending QB ratification" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
0
```

```
$ grep -nE "^### 5\." /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
729:### 5.1 Forbidden Pattern: Including per-row dispatch metadata in a UNIQUE constraint when the dispatch is cross-row coherent at a coarser key
758:### 5.2 JSONB conventions — schemas live in writer code
```

```
$ grep -nE "2026-05-04" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
840:### 8.W.1 wr_predictions UNIQUE constraint included per-horse dispatch metadata, accumulating duplicates (Bug #N TBD; fixed 2026-05-04)
844:**Fix date: 2026-05-04** (per `git log --format="%cs %h %s" -- backend/database/migrations/011_wr_predictions_unique_fix.sql | tail -1`, returning `2026-05-04 87dec36 Pre-bible baseline commit ...`). The git history of this repository was bootstrapped at commit `87dec36` ("Pre-bible baseline commit") on 2026-05-04, which captured pre-existing files — meaning the migration file existed before the baseline was committed. Per META_PLAN v9 § 7.3 placeholder-resolution sub-rule: the date returned by `git log` is the canonical W.N Fix date for placeholder-resolution purposes; the operator-historical authoring date for the migration itself predates 2026-05-04 but is not git-recoverable from this repository's history. See verification log V1-8 for the substrate detail.
```

```
$ grep -nE "DELETE FROM schema_migrations" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
$ echo $?
1
```

```
$ grep -nE "ls backend/database/migrations" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
$ echo $?
1
```

**Decomposition (per Step 6 expected outputs):**

- `Bug #28` count = **1** ✅ (the cross-reference at § 6 unchanged).
- `trainer_stats` in § 4.1 region = **0** ✅ (G-new-2 closure preserved).
- `candidate; pending QB ratification` count = **0** ✅ (Q3.1 + Q3.2 ratified; markers removed; § 5.3 deleted entirely).
- § 5 sub-section headers = **§ 5.1 + § 5.2 only** ✅ (§ 5.3 deleted per Q3.3.c).
- `2026-05-04` occurrences = **2** (both at § 8.W.1; correct per V1-8 substrate — the migration 011 fix date IS 2026-05-04 per its baseline-commit-only history). § 8.W.2 no longer cites 2026-05-04 ✅ (corrected to 2026-03-15 per D-3.1 fix).
- `DELETE FROM schema_migrations` count = **0** ✅ (D-1.2 deleted the procedural-sequencing prose; grep exit 1 = no matches).
- `ls backend/database/migrations` count = **0** ✅ (D-1.1 deleted the procedural-sequencing prose; grep exit 1 = no matches).

**Cite for cross-reference:** the patch-spec's Step 6 prescribed sweeps; this entry confirms each sweep passes its expected output.

**Source-tier:** Tier 4 (this draft's own text post-patch).

### V1-patch-10: AUDIT_METHODOLOGY.md lesson banking — labeling vocabulary substrate observation

**Patch operation:** Three lessons banked in AUDIT_METHODOLOGY.md per the patch-spec's Step 4 instruction (Lessons 11/12/13 + the F.1 prediction-precision lesson).

**Substrate observation (audit-CC labeling vocabulary mismatch):** AUDIT_METHODOLOGY.md uses § 4.X = Lesson X numbering (§ 4.1 = Lesson 1 through § 4.7 = Lesson 7 in the v2-locked file). The patch-spec referenced "Lesson 11 + Lesson 12 + Lesson 13" as the labels for the lessons to bank. Banking at § 4.11 / § 4.12 / § 4.13 would leave § 4.8 / § 4.9 / § 4.10 as numbering gaps — inconsistent with the file's existing convention.

Per the patch-spec's "Do NOT invent a structure" + "lessons-banked subsection if such exists" + "honoring the file's existing structure" guidance, lessons banked at the next-sequential slots § 4.8, § 4.9, § 4.10, § 4.11 (for the four lessons total: Lesson 11/12/13 content + the F.1 prediction-precision lesson). The label-vocabulary mismatch (the patch-spec said "11/12/13" but the file's numbering starts the new slots at 8) is a substrate observation, not a methodology-interpolation: the file's § 4.X = Lesson X convention is Tony-locked from prior cycles, and using the next-sequential slots honors that convention.

If Tony intended different numbering (e.g., explicit "Lesson 11/12/13" labels that skip slots 4.8/4.9/4.10 in the file), surface for re-spec; absent such direction, the next-sequential banking is the interpretation that minimizes invention.

**Cite for cross-reference:** patch-spec Step 4 ("Add Lesson 13 to the appropriate section ... otherwise append a new entry honoring the file's existing structure"); AUDIT_METHODOLOGY.md § 4 introductory paragraph ("seven lessons below appear in the empirical sequence of their introduction"); META_PLAN v9 § 6.1 (methodology-interpolation rule, no-invention discipline).

**Source-tier:** Tier 4 (this draft's own text post-patch); Tier 5 (the patch-spec's labeling vocabulary).

### V1-patch-11: D-1 stale § 5.3 cross-reference correction (v1-patched-d1 surgical patch)

**Patch operation:** Bible § 5 lead paragraph at line 727 — substring "§ 5.3 forward-deferral note below" replaced with "the forward-deferral note at end of § 5 below". Closes re-audit-CC's MINOR D-1 finding per Tony's D1.a ratification on 2026-05-05.

**Verbatim pre-state grep output (run before applying the edit, 2026-05-05):**

```
$ grep -nE "5\.3 forward-deferral note below" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
727:Two rules surfaced from substrate analysis (the schema files + migration files + repository writer code) and ratified by Tony on 2026-05-05. A third candidate (Common Mistake about producer-side parent-row verification before child INSERTs) was moved to data_pipeline_bible's candidate roster per § 5.3 forward-deferral note below.
```

**Verbatim post-state grep output (run after applying the edit, 2026-05-05):**

```
$ grep -nE "5\.3 forward-deferral note below" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
$ echo $?
1
```

```
$ grep -nE "the forward-deferral note at end of § 5 below" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
727:Two rules surfaced from substrate analysis (the schema files + migration files + repository writer code) and ratified by Tony on 2026-05-05. A third candidate (Common Mistake about producer-side parent-row verification before child INSERTs) was moved to data_pipeline_bible's candidate roster per the forward-deferral note at end of § 5 below.
```

**Decomposition:** 1 pre-state match at line 727; 0 post-state matches for the stale pattern (grep exit 1 = no matches); 1 post-state match for the replacement pattern at line 727. Single-line in-place substring replacement.

**Cite for cross-reference:** `database_schema_bible_v1_reaudit.md` Section D D-1 finding (closure recommendation Option (a) — descriptive replacement); Tony's D1.a ratification 2026-05-05.

**Source-tier:** Tier 4 (working-tree bible draft post-patch).

---

## End of Companion Verification Log

Companion bible: `database_schema_bible.md`.

V1-N total: 17 entries (V1-1 through V1-17, including the V1-1a / V1-7a / V1-7b sub-claims that decompose substrate detail; V1-8 rewritten in-place per audit-CC D-3.1 BLOCKER + Tony ratification 2026-05-05).
Section F entries: 3 FRAMEWORK_GAP markers (F.1 schema.sql ↔ 001 byte-identity; F.2 wr_predictions / pl_predictions style + model_used columns gap; F.3 LS cross-table read pattern). All three Tony-ratified 2026-05-05.
Section H entries: 9 (H1–H9 reproduced char-exact from drafting spec § 6; unchanged in v1-patched).
Section I entries: 11 (V1-patch-1 through V1-patch-11) covering the v1-patched + v1-patched-d1 surgical-patch operations.
Section A inherited claims: 6 (A.1–A.6 from META_PLAN v9 + Architecture Overview v3).
Sections B / G: NOT APPLICABLE for v1 first cycle full draft + within-cycle surgical patches.
