# Convergence Test Audit — Operating Model Convergence Test (Phase 0 § 5.3 step 3)

**Audit subject:** operating-model convergence test for Phase 0 methodology (META_PLAN v6 § 5.3 step 3)
**Audit-CC role:** third fresh CC session — no involvement in run1 or run2 drafting
**Threshold per § 5.3:** identify all material differences between run1 and run2; surface anything borderline as material per the explicit instruction "When borderline, audit-CC flags as material and lets Tony decide"
**Date:** 2026-05-04
**Inputs:**
- `_convergence_test/database_schema_bible_run1.md` (512 lines)
- `_convergence_test/database_schema_bible_run1_verification.md` (414 lines)
- `_convergence_test/database_schema_bible_run2.md` (350 lines)
- `_convergence_test/database_schema_bible_run2_verification.md` (333 lines)
**References (Phase 0 locked):**
- META_PLAN v6 (`_meta/META_PLAN.md`)
- BIBLE_STRUCTURE_SPEC v3 (`_meta/BIBLE_STRUCTURE_SPEC.md`)
- AUDIT_METHODOLOGY v2 (`_meta/AUDIT_METHODOLOGY.md`)
- CONVERGENCE_CRITERIA v2 (`_meta/CONVERGENCE_CRITERIA.md`)
- TRIAGE_QUEUE_SPEC v1 (`_meta/TRIAGE_QUEUE_SPEC.md`)

---

## Summary verdict: **DIVERGED — significant material divergence; methodology gaps surfaced**

Run1 and run2 produced structurally non-equivalent output across multiple dimensions. The convergence test passes in the sense that audit-CC reliably catches the divergences (per § 5.3 step 5: "If material differences exist that audit-CC reliably caught, methodology is converged"). But the **kind and volume** of divergence — including direct factual contradictions and wholly disjoint Forbidden-Pattern inventories — strongly suggests methodology gaps that Phase 0 documents do not currently close. Specifically:

- BIBLE_STRUCTURE_SPEC v3 § 6.6's "Recommended TOC" is treated very differently by the two runs. Run1 follows it closely; run2 reorganizes § 4 around canonical objects and JSONB conventions.
- Section 5 (Discipline rules) has near-zero overlap between runs (1 of 4 + 1 of 7 entries shared). The methodology authorizes the Phase 1 drafter to surface Forbidden Patterns and Common Mistakes from the substrate, but provides no scoping rule to converge two drafters on the same set.
- Section 6 (Currently Open) has direct disagreement on whether Bug #28 belongs there at all.
- Section 8 (W.N entries) has disjoint W.N rosters: run1 includes pace_delta backfill and excludes past_performances.race_id; run2 does the opposite.

This is not silent drift — audit-CC can list every divergence with citations — so the test's primary failure mode (audit-CC failing to catch material differences) is not realized. But the volume of divergence indicates that the Phase 0 methodology under-constrains Phase 1 drafting in ways that Tony should decide to either accept or close before Phase 1 begins in earnest.

**Recommendation:** revise Phase 0 documents (specifically BIBLE_STRUCTURE_SPEC v3 § 5.5 / § 5.6 / § 6.6 and META_PLAN v6 § 7.4 / § 7.5 / § 7.6) to address the surfaced gaps before re-running the test. See **Methodology-gap findings** below.

---

## Per-question findings

### Q1 — Section structure

**Both runs have all 8 required sections** per BIBLE_STRUCTURE_SPEC v3 § 5.2 + § 6.6 (`Scope`, `Definitions`, `Architecture overview`, domain-specific § 4, `Discipline rules`, `Currently Open`, `Deprecated`, `What Was Fixed`).

**Both runs use the canonical 5/6/7/8 ordering** (mandatory per § 5.2). Run2's verification log N-15 explicitly self-checks this; run1 does not state it but complies.

**Section header formats are similar but not identical**:
- Both use top-level `## N. Title` headers.
- Run1 uses `### N.X.Y` for tertiary headings (e.g., `### 4.2.3 The schema_migrations runner mechanism`); run2 uses bolded inline text (e.g., `- **Tracking is by filename, not by content hash.**`).
- Both follow the spec § 5.5 W.N-only-letter-prefix discipline.

**Substantive structural divergence (MATERIAL):**

The spec § 6.6 Recommended TOC for `database_schema_bible.md` says:

```
3. Schema overview (3.1 14 tables, 3.2 1 matview, 3.3 schema bootstrap vs migrations)
4. Schema and migration detail (4.1 per-table docs, 4.2 migration discipline)
5. Discipline rules (5.1 UNIQUE, 5.2 JSONB, 5.3 cross-table FK)
```

- **Run1** follows this closely: § 3 architecture overview with 5 sub-sections (3.1 runtime topology, 3.2 14 tables decomposed list, 3.3 matview, 3.4 predictions-table family, 3.5 JSONB conventions); § 4 with 4.1.1–4.1.14 per-table documentation and 4.2.1–4.2.5 migration discipline; § 5 with 4 entries (UNIQUE Forbidden, renaming-applied-migrations Forbidden, JSONB shadow Common Mistake, pace_delta Common Mistake).
- **Run2** deviates: § 4 is renamed "Canonical objects" with 4.1 `Prediction`, 4.2 `PLPrediction`, 4.3 `LSPrediction`, 4.4 other canonical objects, 4.5 per-table inventory (compact), 4.6 migration discipline, 4.7 JSONB conventions. § 5 has 7 entries (4 Forbidden + 3 Common Mistake).

This means the two drafters interpreted § 6.6's "Recommended TOC" with materially different latitude — even though both technically comply with § 5.2's mandatory 5/6/7/8 ordering.

### Q2 — Factual claims (the core convergence question)

**Convergent factual claims:**
- 14 tables: both runs identify the same 14 tables (✓).
- 1 materialized view = `trainer_stats` (migration 008): ✓.
- Migration runner = `backend/database/migrations/migrate.py` + `schema_migrations` tracking table: ✓.
- 12 migration filenames including duplicate-005: ✓.
- Predictions-table family = legacy `predictions` + `wr_predictions` + `pl_predictions` + `ls_predictions`: ✓.
- Aurora cluster ARN (run1 quotes `arn:aws:rds:us-east-1:584812014683:cluster:equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`; run2 references the same cluster via META_PLAN v6 § 2.3): ✓.
- Legacy `predictions` row count = 6,600 (inherited): ✓.
- `prediction_router.py` reader inventory = 4 references (1 import + 3 instantiations on lines 6, 34, 61, 92): ✓.
- `race_router.py` reader inventory = 2 references (1 import + 1 instantiation on lines 273, 277): ✓.
- canonical.py class line numbers (`PLPrediction:351`, `LSPrediction:390`, `Prediction:428`): ✓.
- Both correctly note that `WRPrediction` does NOT exist as a class in canonical.py: ✓ (both surface this explicitly).
- Pre-011 wr_predictions UNIQUE was `(race_id, entry_id, model_used, style)`: ✓.
- Post-011 wr_predictions UNIQUE constraint name `wr_predictions_unique_per_entry_style` on `(race_id, entry_id, style)`: ✓.
- Migration 011 deduplication scope = 157 races × 427 rows / ~1.35% of 11,629: ✓ (both verbatim from migration 011's preamble).
- Migration 010 added 5 columns to ls_predictions (`style`, `market_prob`, `edge_pct`, `is_top_pick`, `morning_line_implied_prob`): ✓.
- Migration 010 verified empty before swap ("Existing rows: 0"): ✓.

**Divergent factual claims (MATERIAL):**

| # | Claim | Run1 | Run2 | Notes |
|---|---|---|---|---|
| F1 | `migrate.py` line count | **157** lines (verification N5: `wc -l ... returns 157`) | **158** lines (verification N-1: "158 lines total, read in full") | Audit-CC verified live: `wc -l` returns 157. Run2 is wrong by one. |
| F2 | `pl_predictions` UNIQUE constraint | "UNIQUE: (entry_id) per migration 005" — taken at face value (§ 4.1.13, § 4.1.14, verification N19) | "the live constraint at audit time is UNIQUE(race_id, entry_id, style) per the WR-aligned pattern (migration 011's preamble references this convention)" + Currently Open entry flagging the discrepancy (§ 4.5 table 13, § 6) | DIRECT DISAGREEMENT on whether `pl_predictions` currently has `UNIQUE(entry_id)` or `UNIQUE(race_id, entry_id, style)`. Audit-CC verified migration 005 declares `UNIQUE(entry_id)` at line 57; no migration 006-011 alters `pl_predictions`. But migration 011 line 18 says "match the PL / LS pattern — UNIQUE (race_id, entry_id, style)" implying PL already has it. Run2 catches this drift; Run1 misses it. |
| F3 | `wr_predictions.style` and `wr_predictions.model_used` columns — schema-vs-migration drift | § 4.1.12 acknowledges "a `style` column and a `model_used` column referenced in 011's commentary" but does not surface that no migration adds them | § 6 Currently Open explicitly flags as drift: "no committed migration in 001–011 adds them to wr_predictions" + verification N-5 documents the grep proof | MATERIAL. Audit-CC verified: `grep "ALTER TABLE wr_predictions ADD COLUMN" migrations/*.sql` returns nothing for `style`/`model_used`. Migration 011 references both columns as if they exist. Run2 catches this drift; Run1 misses it. |
| F4 | RDS Data API usage | § 3.1: "RDS Data API — used by Lambda paths that don't open VPC connections (verification deferred to architecture_overview.md)" | § 3: "RDS Data API is not used by EE Python code (verified — migrate.py opens psycopg2 directly via the connection string assembled from the secret)" | DIRECT FACTUAL CONTRADICTION. Both use hedge language (run1: "verification deferred"; run2: "verified"), but the assertions are contradictory. Tony to adjudicate. |
| F5 | `trainer_stats` matview aggregate column count | § 3.3: 7 enumerated (`total_starts, win_rate, itm, itm_rate, layoff_win_rate, lasix_win_rate, claimed_win_rate`); verification N4 self-flags the omission of `wins` | § 4.5 (matview) and § 8.W (none here, but cited indirectly): 8 enumerated (`total_starts, wins, win_rate, itm, itm_rate, layoff_win_rate, lasix_win_rate, claimed_win_rate`) | Run2 is correct (8 aggregates per migration 008 lines 9–53). Run1 is incomplete; its verification log surfaces the omission honestly. Material per § 5.3 ("a factual claim about EE that differs"). |
| F6 | `schema.sql` line count | Not stated in run1 | "Both files are 416 lines" (verification N-8) | Audit-CC verified: `wc -l schema.sql` returns 415, not 416. Run2 is wrong by one. (Run1 didn't claim, so no run1-vs-run2 disagreement, but Run2 has an independently-incorrect claim.) |
| F7 | `trainer_stats` materialized view filter / index | § 3.3: no mention of WHERE filter or supporting unique index | § 4.5 matview note: "Unique index `idx_trainer_stats_name` on `trainer_name`"; verification N-12 documents `WHERE trainer_name IS NOT NULL AND finish_position IS NOT NULL AND finish_position < 90` | Run2 documents more; Run1 omits. Both could be correct (different scope choices), but the omission/inclusion is a scope claim that differs. |
| F8 | Migration 011 fix date | § 8.W.2: "fixed 2026-05-XX" (placeholder per META_PLAN v6 Appendix A convention) | § 8.W.1: "fixed 2026-05-01" (committed date) | Both runs trust the same source; Run1 uses placeholder, Run2 commits. Material because the dates appear in lock-point footer text where consistency matters. |
| F9 | Migration 009 fix date | § 8.W.1: "fixed 2026-04-XX" (placeholder) | (entire entry absent from run2 § 8) | Run2 omits the W.N entry entirely (see Q4 below). |
| F10 | Lambda inventory in architecture overview | Run1 does not enumerate Lambdas in § 3 | § 3: "WR/PL/LS inference Lambdas Active; ingestion / feature-engineering / results Lambdas INACTIVE; legacy `equine-inference` Active" | Run2 includes a Lambda inventory in § 3. Run1 defers. Material (a scope claim that differs). |

**Canonical objects (§ 4) — major structural divergence:**
- Run1: defers canonical-object documentation to `architecture_overview.md` per BIBLE_STRUCTURE_SPEC v3 § 4.2.1's locked Q1 statement; mentions `PLPrediction` and `LSPrediction` only briefly (in § 1 scope and § 4.1.13 reader notes).
- Run2: dedicates § 4.1–4.4 to canonical-object documentation in this bible, with full field enumerations for `Prediction`, `PLPrediction`, `LSPrediction`.

Both runs surface the WRPrediction-doesn't-exist finding with consistent evidence. But run2 documents the dataclasses **here**, while run1 says they belong in Architecture Overview. This is a MATERIAL scope-claim divergence: where the canonical-object boundary lives.

### Q3 — Rule statements and cross-references

**Forbidden Patterns and Common Mistakes — minimal overlap:**

| Run1 | Run2 | Match? |
|---|---|---|
| 5.1 Forbidden: dispatch metadata in UNIQUE | 5.3 Forbidden: dispatch metadata in UNIQUE | ✓ same rule, different sub-section ID |
| 5.2 Forbidden: renaming applied migrations | 5.6 Common Mistake: duplicate-005 not a bug to fix (touches renaming) | partial — different forcing function classification |
| 5.3 Common Mistake: JSONB shadow columns | (absent) | run2 doesn't include this rule |
| 5.4 Common Mistake: pace_delta finish_call_position | (absent) | run2 doesn't include this rule |
| (absent) | 5.1 Forbidden: writing to legacy `predictions` table | run1 doesn't include this rule |
| (absent) | 5.2 Forbidden: joining `past_performances` by `race_id` | run1 doesn't include this rule |
| (absent) | 5.4 Forbidden: positional column indexing without header check | run1 doesn't include this rule |
| (absent) | 5.5 Common Mistake: `schema.sql` and migration 001 drift | run1 doesn't include this rule |
| (absent) | 5.7 Common Mistake: counting `schema_migrations` as 15th table | run1 doesn't include this rule |

**Total**: Run1 has 4 entries; Run2 has 7 entries. **One rule overlaps** (UNIQUE-dispatch-metadata, with different sub-section IDs).

This is a major rule-statement divergence. Both runs' choices are defensible against the spec — the spec authorizes Phase 1 drafters to surface Forbidden Patterns from the substrate — but the methodology provides no convergence rule. Two CCs given the same spec produced wholly disjoint discipline rosters.

**Cross-reference divergence (MATERIAL — per § 5.3 explicit material category "A cross-reference to a different bible section"):**

| Citation | Run1 | Run2 |
|---|---|---|
| Where § 8.W (UNIQUE bug) cross-refs the Forbidden Pattern | § 5.1 | § 5.3 |
| Where § 8.W (LS first-class) cross-refs the Forbidden Pattern | § 5.1 | § 5.3 |
| Where § 7.2 (pre-011 UNIQUE) cross-refs the Forbidden Pattern | § 5.1 | (no equivalent § 7.2 in run2) |
| Where § 5 cross-refs the canonical W.N entry | § 5.1 → § 8.W.2 | § 5.3 → § 8.W.1 |

The W.N numbering is also reordered: Run1's 8.W.2 == Run2's 8.W.1 (both wr_predictions UNIQUE fix). So the "see § 8.W.<n>" pointers, even when correct in their own bible, do not match between runs. This is exactly the cross-reference-divergence material category.

**Cross-reference to other bibles — naming convention divergence:**
- Run1 uses snake_case .md filenames: `architecture_overview.md`, `data_pipeline_bible.md`, `feature_provenance_bible.md`, `ml_layer_architecture_bible.md`, `api_frontend_bible.md`.
- Run2 uses Title Case prose: "Architecture Overview Bible § 3", "Data Pipeline Bible § 4", "Feature Provenance Bible § 4", "ML Layer Architecture Bible § 4", "API & Frontend Bible § 4".

BIBLE_STRUCTURE_SPEC v3 § 7.1 prescribes the canonical syntax: `<bible_name>:<section_id>` (e.g., `feature_provenance_bible:8.W.7`). **Both runs deviate** from the canonical syntax in different directions. Material — and a methodology gap (the spec form is not yet adopted in either drafter's habit).

**Migration discipline rules — convergent:**
- Both agree on 001–011 grandfathering + NNN_YYYYMMDD format from 012+.
- Both agree on the duplicate-005 case and lexical sort.
- Both agree on the in-file rollback block convention.
- Both agree on local-Postgres-only testing and no dev Aurora cluster.

### Q4 — Currently Open + Deprecated + What Was Fixed

#### Currently Open (§ 6) — DIRECT DISAGREEMENT

| Run | Content |
|---|---|
| Run1 | "No current open issues against the schema layer at lock. (Bug #28 is a scraper / data-acquisition bug, canonically homed in `data_pipeline_bible.md`. It does not call into question any schema or migration discipline rule.)" |
| Run2 | 4 open items: Bug #28 (HIGH); schema-vs-migration drift on style/model_used columns (UNRESOLVED); no dev Aurora cluster (MODERATE); pl_predictions UNIQUE may not match WR/LS pattern (LOW). |

**MATERIAL.** This is exactly the spec's "scope claim that differs" material category. Run1 interprets the cross-cutting-bug-canonical-home rule (BIBLE_STRUCTURE_SPEC v3 § 5.3) as excluding Bug #28 from this bible's Currently Open entirely. Run2 interprets it as including Bug #28 here with a cross-reference to the canonical home in `data_pipeline_bible:6`.

This is a **methodology gap**: § 5.3 cross-cutting-bug rule says canonical W.N entries are non-duplicated, but it does not say whether **Currently Open** entries are also non-duplicated, or whether non-canonical-home bibles should mention the bug at all. Both interpretations are defensible.

The spec § 6.6 "Recommended TOC" + § 4.2.3 say this bible covers "the migration runner mechanism" and touches scraper-effects-on-schema, but doesn't legislate Currently Open scope.

#### Deprecated (§ 7) — RUN1 HAS THREE; RUN2 HAS ONE

| Run | Entries |
|---|---|
| Run1 | 7.1 legacy `predictions` table, 7.2 pre-011 `wr_predictions` UNIQUE shape, 7.3 pre-010 `ls_predictions` UNIQUE(entry_id) |
| Run2 | 7.1 legacy `predictions` table only |

**MATERIAL.** Run1 includes superseded UNIQUE constraints as Deprecated entries; Run2 does not. Both are defensible: BIBLE_STRUCTURE_SPEC v3 § 5.6.4's Deprecated entry template is field-agnostic about whether superseded constraints qualify. Run1 reads Deprecated broadly (any superseded thing); Run2 reads narrowly (only currently-deprecated-but-still-readable Field/Module entries with active readers).

This is a methodology gap: § 5.6.4 and META_PLAN v6 § 7.7 don't define whether superseded SQL constraints (which have no "active readers" because they no longer exist on the table) get § 7 entries.

#### What Was Fixed (§ 8) — DISJOINT W.N ROSTERS

| Slot | Run1 | Run2 |
|---|---|---|
| 8.W.1 | pace_delta backfill (migration 009) — fixed 2026-04-XX | wr_predictions UNIQUE (migration 011) — fixed 2026-05-01 |
| 8.W.2 | wr_predictions UNIQUE (migration 011) — fixed 2026-05-XX | ls_predictions first-class (migration 010) — fixed 2026-05-01 |
| 8.W.3 | ls_predictions first-class (migration 010) — fixed 2026-05-01 | past_performances.race_id NULL (locked 2026-05-04, not a bug fix) |

**MATERIAL** in two ways:

1. **Disjoint roster**: Run1 has 3 entries; Run2 has 3 entries; only 2 of 3 overlap (UNIQUE fix and LS first-class). Run1 has pace_delta (8.W.1); Run2 has past_performances.race_id (8.W.3).
2. **Numbering reordering**: For the two overlapping fixes, the 8.W.<n> identifiers don't match between runs.

**Methodology-interpolation flag:**

Run2's 8.W.3 (past_performances.race_id NULL) is **not a bug fix** — Run2 itself acknowledges this in its verification log methodology-interpolation self-check ("a 'What Was Fixed' entry that is *not* a bug fix in the conventional sense — it codifies an existing design discipline"). Per BIBLE_STRUCTURE_SPEC v3 § 5.6.1's W.N entry template ("**Mandatory fields:** Bug name or short description; Fix date (YYYY-MM-DD); Symptom; Root cause; Fix; Why this entry exists"), the format requires a fix and a fix date. Run2's 8.W.3 has no fix date — it has "(locked 2026-05-04)" which is the entry-locked date, not a bug-fix date. This is borderline interpolation; Run2 self-flags the borderline judgment call.

Run1's 8.W.1 (pace_delta backfill) IS a real bug fix (migration 009 corrects migration 005-pace-delta). Run2 does not include it.

Both runs include the conditional-trigger evaluation pattern with FIRES / DOES NOT FIRE annotations per BIBLE_STRUCTURE_SPEC v3 § 5.6.1.1 worked example. Run1 uses "PARTIAL" once (§ 8.W.3 — if-fix-touches-multiple-bibles); Run2 uses "FIRES (advisory)" twice. Neither is a strict binary FIRES/DOES NOT FIRE state, but the spec § 5.6.1.1 doesn't actually mandate binary-only — both runs' adaptations are within the format's spirit.

### Q5 — Verification log structure

**Total claim count differs:**
- Run1: 38 total = 12 inherited (V1–V12) + 26 new (N1–N26).
- Run2: 32 total = 17 inherited (I-1 through I-17) + 15 new (N-1 through N-15).

**Inherited-vs-new distinction:** both runs distinguish them with a header section break. Run1 uses `V<n>` prefix for inherited; Run2 uses `I-<n>`. Both use `N<n>` for new (Run1: `N<n>`; Run2: `N-<n>`). Format-cosmetic divergence, not material.

**Verification-log-precision rule applications (decomposed counts):** both runs decompose claim counts. Run1's V7 decomposes the prediction_router.py reader inventory verbatim from META_PLAN v6 ("PredictionRepository: 1 import on line 6 + 3 instantiations on lines 34, 61, 92 = 4 references total"). Run2's I-8 + N-6 do the same. Both follow META_PLAN v6 § 6.5's verification-log-precision rule.

**File paths / line numbers in verification entries:** convergent on the major shared claims (canonical.py:351/390/428; prediction_router.py:6/34/61/92; race_router.py:273/277). Diverge on line ranges within `migrate.py` because the two CCs read different code blocks for different evidence (Run1 emphasizes lines 64–104, 88–94; Run2 emphasizes lines 21–41, 44–54, 57–61, 69–72, 90–93, 97–102, 107–135). Both are correct line ranges within the same file; different scoping choices.

**Inherited-claim selection differs (MATERIAL):**
- Run1 lists 12 inherited claims, all about the database/migrations.
- Run2 lists 17 inherited claims, including ones run1 didn't carry (Aurora cluster ARN as separate I-4, Secrets Manager entry as separate I-5, Lambda inventory as I-6, Bug #28 as I-11/I-12, migration discipline format as separate I-13). Run2 partitions META_PLAN v6's verification log differently and counts more facts as inherited.

**Verification-log line-count (live-verified by audit-CC):**
- migrate.py = 157 lines (run1's V7/N5 correct; run2's N-1 wrong by 1).
- schema.sql = 415 lines (run2's N-8 wrong by 1; run1 doesn't claim).

These two line-count errors in run2 are **factual claims that audit-CC reliably caught** — exactly the convergence-test pass criterion.

### Q6 — Methodology interpolation

Per META_PLAN v6 § 6.1, CC must surface any methodology constructs introduced that Tony has not explicitly ratified.

**No new methodology constructs introduced by either run** in the strict sense — neither invents a new severity scheme, a new letter prefix beyond W.N, or a new section type. Both pass the basic interpolation check.

**Borderline interpolations surfaced by run2 itself:**

1. **Run2's 8.W.3** codifies a design discipline that is not a bug fix. Run2's verification log methodology-interpolation self-check explicitly flags this as a judgment call: "Whether this stretches the canonical W.N use is an audit-CC judgment call." Audit-CC ratifies: this DOES stretch the canonical W.N format. The W.N template (BIBLE_STRUCTURE_SPEC v3 § 5.6.1) mandates "Fix date (YYYY-MM-DD)" — Run2's 8.W.3 has "locked 2026-05-04" which is not a fix date but an entry-creation date. **Material methodology gap surfaced**: the spec doesn't authorize "discipline codification" entries in § 8; if Tony wants such entries, the template needs explicit authorization.

2. **Run2's Currently Open severity tags** (HIGH / MODERATE / LOW) are drawn from META_PLAN v6 § 11 / TRIAGE_QUEUE_SPEC v1; Run2's verification log self-checks this against § 11 and finds compliance. Audit-CC ratifies: severities are pre-existing, not interpolated.

3. **Run2's "FIRES (advisory)"** state for conditional triggers is a variant of FIRES that the worked example § 5.6.1.1 does not enumerate. The same applies to Run1's "PARTIAL" state. Both runs adapted the binary FIRES/DOES NOT FIRE pattern to a 3-state form. Methodology gap: the worked example shows binary, but neither bible spec nor META_PLAN explicitly forbids tertiary states. Tony to ratify.

**No interpolation findings from Run1's self-check** beyond the same N25 framework-gap finding (WRPrediction doesn't exist) which run2 also surfaces.

**Recursive precision discipline (verbatim claim formatting):**

Both runs produce verbatim-quoted SQL fragments (`UNIQUE (race_id, entry_id, style)`, `DROP CONSTRAINT IF EXISTS …`, `HAVING COUNT(*) >= 5`) with character-exact reproduction of the source. Spot-check by audit-CC against migrations 005, 008, 010, 011 confirms compliance.

**One precision deviation noted by Run1's verification N23:** the bible elides the `IF NOT EXISTS` qualifier from the `CREATE UNIQUE INDEX idx_active_model_per_type` statement when quoting it in § 4.1.11. Run1's verification log surfaces this as "a minor compression that does not change the operational meaning." Per recursive precision discipline (TRIAGE_QUEUE_SPEC v1), verbatim claims must reproduce source character-exact. Run1 self-flagged the deviation; technically still a deviation. Run2 does not quote this statement, so cannot be compared.

---

## Material-difference enumeration (consolidated, with citations)

In order of severity (by audit-CC judgment; Tony adjudicates):

**M1. Direct factual contradiction on RDS Data API usage.** Run1 § 3.1: "RDS Data API — used by Lambda paths that don't open VPC connections (verification deferred)." Run2 § 3: "RDS Data API is not used by EE Python code (verified — migrate.py opens psycopg2 directly)." → Need code-level adjudication outside this bible's scope.

**M2. Schema-vs-migration drift on `wr_predictions.style` and `wr_predictions.model_used`.** Run2 § 6 (Currently Open) and verification N-5 surface this; Run1 § 4.1.12 acknowledges the columns but does not surface the drift. **Audit-CC verified live**: no migration 001–011 adds these columns to wr_predictions; migration 011 references them (lines 39, 54, 64, 67–68, 78). Run2 catches; Run1 misses.

**M3. `pl_predictions` UNIQUE constraint state.** Run1 § 4.1.13 and verification N19 assert `UNIQUE(entry_id)` (per migration 005 declaration). Run2 § 4.5 and § 6 surface the discrepancy: migration 011's preamble line 18 ("match the PL / LS pattern — UNIQUE (race_id, entry_id, style)") implies PL already has the (race_id, entry_id, style) form, but no migration establishes it. Run2 catches; Run1 misses.

**M4. `migrate.py` line count.** Run1 V5/N5: 157 (audit-CC live-verified: 157). Run2 N-1: 158. Run2 wrong.

**M5. `schema.sql` line count.** Run2 N-8: 416 (audit-CC live-verified: 415). Run1 makes no line-count claim. Run2 wrong by 1.

**M6. `trainer_stats` matview aggregate count.** Run1 § 3.3: 7 aggregates enumerated (omits `wins`); verification N4 self-flags. Run2 § 4.5: 8 aggregates enumerated. Run2 correct; Run1 incomplete.

**M7. § 6 Currently Open scope.** Run1: empty ("No current open issues..."). Run2: 4 entries including Bug #28 cross-referenced to data_pipeline_bible. Disagree on whether non-canonical-home bibles list cross-cutting bugs in Currently Open.

**M8. § 7 Deprecated count.** Run1: 3 entries (7.1 legacy predictions + 7.2 pre-011 wr_predictions UNIQUE + 7.3 pre-010 ls_predictions UNIQUE). Run2: 1 entry (7.1 legacy predictions only). Disagree on whether superseded SQL constraints qualify.

**M9. § 8 What Was Fixed roster.** Run1: pace_delta + wr_predictions UNIQUE + ls_predictions first-class. Run2: wr_predictions UNIQUE + ls_predictions first-class + past_performances.race_id NULL. Pace_delta in run1 only; past_performances.race_id in run2 only.

**M10. § 8.W.<n> numbering reordering.** Run1's 8.W.1 = pace_delta (migration 009); Run2's 8.W.1 = wr_predictions UNIQUE (migration 011). Same fact occupies different W.N slots between runs.

**M11. Section-5 discipline rule rosters.** Run1: 4 rules (5.1, 5.2, 5.3, 5.4). Run2: 7 rules (5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7). Only 1 rule overlaps (UNIQUE-dispatch-metadata at run1 5.1 = run2 5.3). 5 of run2's rules absent from run1; 3 of run1's rules absent from run2.

**M12. Section-4 organizing principle.** Run1: § 4 = "Schema and migration detail" (per-table + migration discipline). Run2: § 4 = "Canonical objects" (dataclasses + per-table inventory + migration discipline + JSONB). Different framing of the domain-specific § 4 sub-section.

**M13. Canonical-object boundary (where do PLPrediction / LSPrediction dataclasses live?).** Run1: defers to architecture_overview.md per BIBLE_STRUCTURE_SPEC v3 § 4.2.1. Run2: documents them in this bible at § 4.1–4.4.

**M14. § 8 W.<n> cross-reference targets.** "see § 8.W.X" pointers refer to different fix entries between runs because the W.<n> numbering is reordered (per M10).

**M15. § 5 cross-references to W.<n>.** Run1 § 5.1 → § 8.W.2. Run2 § 5.3 → § 8.W.1. Same rule, different cross-references.

**M16. Bible-name cross-reference syntax.** Run1: snake_case `.md` filenames (`feature_provenance_bible.md`). Run2: Title Case prose ("Feature Provenance Bible § 4"). BIBLE_STRUCTURE_SPEC v3 § 7.1 prescribes `<bible_name>:<section_id>`. Both deviate in different directions.

**M17. JSONB shadow definition.** Run1 § 3.5: "No JSONB shadow patterns (a JSONB blob whose keys mirror columns elsewhere) exist in the EE schema as of 011." Run2 § 2 (Definitions): defines JSONB shadow as "logically structured but stored as text or JSONB without a schema" and identifies `model_versions.notes` as a JSONB-shadow text column. Definitions disagree.

**M18. Migration 011 fix date format.** Run1 § 8.W.2: "fixed 2026-05-XX" (placeholder). Run2 § 8.W.1: "fixed 2026-05-01" (committed). Run1 follows META_PLAN v6 Appendix A's `2026-05-XX` placeholder convention conservatively; Run2 commits.

**M19. Lambda inventory in architecture overview.** Run1 § 3 omits Lambda enumeration. Run2 § 3 enumerates 5 Active + 3 INACTIVE Lambdas with names. Scope claim differs.

**M20. `trainer_stats` index documentation.** Run1: omits `idx_trainer_stats_name` unique index. Run2: documents it. Scope differs.

**M21. Verification log inherited-claim count.** Run1: 12 inherited. Run2: 17 inherited. Different partitioning of META_PLAN v6's verification log.

**Total material differences: 21.**

---

## Non-material-difference enumeration (briefly)

The following differences are surfaced for awareness but classified as **non-material** per § 5.3:

- **NM1.** `V<n>` vs `I-<n>` prefix for inherited verification claims (cosmetic).
- **NM2.** `N<n>` vs `N-<n>` prefix for new verification claims (cosmetic).
- **NM3.** Per-table column lists in run1 § 4.1.X are exhaustive; run2 § 4.5 is compact (different illustrative-example depth, both concrete and accurate).
- **NM4.** Run2's tertiary headings use bolded inline text; run1's use `### N.X.Y` headings (paragraph-structure variation).
- **NM5.** Different ordering of WR/PL/LS table mentions in scope (Run1 lists wr/pl/ls; Run2 lists pred-table-family then per-table inventory in different sequence). No canonical order specified.
- **NM6.** Migration runner mechanism — both runs cite the same code, Run1 emphasizes lines 64–104 (run_migrations function); Run2 cites multiple per-function ranges. Equivalent coverage of the same source.
- **NM7.** Run2 defines a "JSONB shadow" term; Run1 doesn't (asymmetric definitional inventory). Definitional asymmetry only — not the same as M17 (which is a definition disagreement on the same term).

---

## Methodology-gap findings (Phase 0 documents need revision)

These gaps surfaced as "the spec was ambiguous enough that the two runs interpreted it differently" — § 5.3 step 5 explicitly flags these as Phase 0 revision triggers.

**G1. BIBLE_STRUCTURE_SPEC v3 § 5.3 cross-cutting-bug-canonical-home rule does not specify Currently Open scope.**
- Symptom: M7 (Run1 omits Bug #28 from § 6; Run2 includes it with cross-reference).
- Recommended revision: extend § 5.3 to address whether non-canonical-home bibles list cross-cutting open bugs in their § 6.

**G2. BIBLE_STRUCTURE_SPEC v3 § 5.6.4 Deprecated entry template does not specify whether superseded SQL constraints qualify as Deprecated entries.**
- Symptom: M8 (Run1 includes 7.2 + 7.3; Run2 omits them).
- Recommended revision: clarify in § 5.6.4 conditional fields whether "supersededDDL-state" entries get Deprecated rows.

**G3. BIBLE_STRUCTURE_SPEC v3 § 5.6.1 W.N entry template does not authorize "discipline codification" entries that lack a fix date.**
- Symptom: Run2's 8.W.3 (past_performances.race_id NULL acceptance) is not a bug fix — it has "locked 2026-05-04" instead of "fixed YYYY-MM-DD".
- Recommended revision: either explicitly authorize a "Locked Discipline (no fix)" sub-pattern under W.N or confine § 8 to true bug-fix entries and route non-bug-fix discipline codifications to § 5 (Discipline rules).

**G4. BIBLE_STRUCTURE_SPEC v3 § 6.6 "Recommended TOC" is interpreted with materially different latitude.**
- Symptom: M12 + M13 (Run1 follows TOC closely; Run2 reorganizes § 4 around canonical objects).
- Recommended revision: tighten "Recommended TOC" → "Required TOC for § 4" OR explicitly authorize alternative § 4 framings with criteria.

**G5. BIBLE_STRUCTURE_SPEC v3 § 5 (Discipline rules) does not specify a convergence rule on rule rosters.**
- Symptom: M11 (4 vs 7 entries; only 1 of 4 / 1 of 7 overlap).
- Recommended revision: either provide a recommended-strongly minimum rule list per bible, or require Phase 1 drafters to enumerate candidate rules from the substrate and surface choices to QB for ratification before locking § 5. (The current convergence test mode of "two CCs invent disjoint rule sets" is the silent-drift failure mode.)

**G6. BIBLE_STRUCTURE_SPEC v3 § 7.1 Cross-reference syntax (`<bible_name>:<section_id>`) is not adopted in either run's drafting habit.**
- Symptom: M16 (Run1: snake_case .md; Run2: Title Case prose).
- Recommended revision: surface § 7.1 in the Phase 1 drafting spec or in the per-bible template's "Cross-references to other bibles" guidance, with a worked example for each cross-reference type.

**G7. BIBLE_STRUCTURE_SPEC v3 § 5.6.1.1 worked example uses binary FIRES / DOES NOT FIRE; both runs needed a tertiary state.**
- Symptom: Run1 uses "PARTIAL"; Run2 uses "FIRES (advisory)".
- Recommended revision: either explicitly authorize a tertiary state (with semantics) or clarify how the binary should resolve borderline cases.

**G8. META_PLAN v6 Appendix A's `YYYY-XX-XX` placeholder convention is interpreted differently between conservative-uses-placeholder and commit-to-actual-date drafters.**
- Symptom: M18 (Run1 "fixed 2026-05-XX"; Run2 "fixed 2026-05-01").
- Recommended revision: clarify whether Phase 1 drafters MUST resolve the placeholder via `git log` of the migration file before locking, or whether placeholder is the safe default until lock.

**G9. The W.<n> numbering convention is unstable across CC executions.**
- Symptom: M10 (run1's 8.W.1 ≠ run2's 8.W.1 even though both are correct in their bibles).
- Recommended revision: either (a) prescribe a canonical W.N ordering rule (e.g., chronological by fix date; alphabetical by bug name) so two CCs converge on the same numbering, or (b) acknowledge in BIBLE_STRUCTURE_SPEC v3 that W.N numbering is bible-local and cross-bible references rely on stable identifiers minted at lock time. (Currently the convention says only that W.N is special because it's grep-stable across bibles — the numbering itself is not stabilized.)

---

## Recursive precision discipline check

**Result: substantially compliant in both runs, with one minor deviation in run1.**

Both runs reproduce verbatim SQL fragments (`UNIQUE (race_id, entry_id, style)`, `DROP CONSTRAINT IF EXISTS …`, `HAVING COUNT(*) >= 5`, `PARTITION BY race_id, entry_id, style ORDER BY created_at DESC, prediction_id DESC`) with character-exact source fidelity. Spot-checked by audit-CC against migrations 005/008/010/011.

**Run1 deviation (self-flagged in N23):** elision of `IF NOT EXISTS` from the `CREATE UNIQUE INDEX idx_active_model_per_type` quote in § 4.1.11. Per TRIAGE_QUEUE_SPEC v1's recursive-precision-discipline lesson, verbatim claims must reproduce source character-exact. Run1's verification log surfaces this honestly.

**Run2:** does not quote this statement in a way that exposes deviation.

The 3 verbatim quoted comments from migration 011 ("157 races (~1.35% of 11,629)..."; "model_used is a per-horse dispatch metadata flag"; etc.) are character-exact in both runs.

**Net assessment:** recursive precision discipline holds; 1 minor self-flagged elision in run1; no deviations in run2.

---

## Recommendation

**Verdict: methodology revision needed before Phase 0 closes.**

Per META_PLAN v6 § 5.4: "If § 5.3 surfaces gaps, the affected Phase 0 documents revise and re-lock. The test re-runs."

The convergence test catches material differences reliably (audit-CC enumerates 21 + 9 methodology gaps with citations), so the **adversarial audit role** is functioning as designed. But the **input methodology** under-constrains Phase 1 drafting in 9 specific ways (G1–G9) that Phase 0 documents currently do not address. These gaps are not subtle — they include direct factual contradictions (M1: RDS Data API yes/no), disjoint discipline rule rosters (M11: 1 of 4 / 1 of 7 overlap), and divergent interpretations of which W.N entries belong in § 8 (M9 + G3).

**Recommended Phase 0 revisions:**

1. **BIBLE_STRUCTURE_SPEC v3 → v4** to address G1, G2, G3, G4, G5, G6, G7, G9. Specifically:
   - § 5.3: extend cross-cutting-bug rule to address Currently Open scope.
   - § 5.6.4: clarify whether superseded SQL constraints qualify.
   - § 5.6.1: explicitly authorize or forbid non-bug-fix W.N entries.
   - § 6.6: tighten § 4 framing for `database_schema_bible.md`.
   - § 5: add convergence rule on discipline rosters (or surface-to-QB protocol).
   - § 7.1: integrate cross-reference syntax into drafting spec template.
   - § 5.6.1.1: clarify binary vs tertiary FIRES state.
   - W.N numbering convention stabilization.

2. **META_PLAN v6 → v7** to address G8: clarify placeholder-date resolution discipline at Phase 1 lock.

3. **Re-run § 5.3 convergence test** after revisions on the same Database & Schema Bible spec. If gaps re-surface, escalate per § 5.3 "Iteration escalation" rule.

**Alternative path (if Tony judges the gaps acceptable):** ratify the present divergence as within-tolerance — i.e., declare that two CCs producing structurally non-equivalent output is OK because audit-CC catches the differences reliably. This is consistent with § 5.1's locked language: "Three CCs given the same spec do not need to produce identical bible files. They need to produce structurally equivalent execution: same target questions answered, same depth of investigation, same format adherence." The two runs **do** answer the same target questions with similar depth, but their format adherence diverges — interpretation of the "Recommended TOC" differs enough that a reader picking up run1 and run2 sees materially different structures. Tony to decide whether this is structural-equivalence or drift.

**Audit-CC's recommendation:** surface all 21 material differences and 9 methodology gaps to QB, with G3 (W.N for non-bug entries), G4 (§ 4 framing), G5 (rule roster convergence), and G9 (W.N numbering stabilization) as the highest-priority revisions. The remaining gaps (G1, G2, G6, G7, G8) are clarifications that are easier to fold into a v4 / v7 revision pass than to re-litigate post-Phase-1.

---

**End of convergence test audit.**
