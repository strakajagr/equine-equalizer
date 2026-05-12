# QB Handoff: Database & Schema Bible Drafting Spec Authorship

**Document:** QB_HANDOFF_DATABASE_SCHEMA_BIBLE_DRAFTING
**Phase:** 1 deliverable 2 of 7 preparation
**Status:** ACTIVE handoff for fresh QB session
**Author:** QB (Architecture Overview cycle, 2026-05-05)
**Date:** 2026-05-05

**Purpose:** Comprehensive context handoff from the Architecture Overview Phase 1 cycle (LOCKED 2026-05-05) to the fresh QB session beginning Database & Schema Bible drafting spec authorship as Phase 1 deliverable 2 of 7. Captures: methodology state, lock state, banked failure modes, standing process patterns, and Database & Schema Bible-specific drafting context. The fresh QB session opens this document FIRST before any other work.

---

## 1. Phase 0 / Phase 1 substrate state (as of 2026-05-05)

### 1.1 Phase 0 LOCKED deliverables

5 of 5 Phase 0 methodology documents LOCKED:

- **META_PLAN v9** (LOCKED 2026-05-05) at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/META_PLAN.md`. Companion verification log at `_audits/META_PLAN_v9_verification.md`.
- **BIBLE_STRUCTURE_SPEC v6** (LOCKED 2026-05-05) at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md`. Companion verification log at `_audits/BIBLE_STRUCTURE_SPEC_v6_verification.md`.
- **AUDIT_METHODOLOGY v2** (LOCKED 2026-05-04) at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/AUDIT_METHODOLOGY.md`.
- **CONVERGENCE_CRITERIA v2** (LOCKED 2026-05-04) at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/CONVERGENCE_CRITERIA.md`.
- **TRIAGE_QUEUE_SPEC v1** (LOCKED 2026-05-04) at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/TRIAGE_QUEUE_SPEC.md`.

### 1.2 Phase 1 progress

- **Deliverable 1 of 7 — Architecture Overview:** LOCKED v3 2026-05-05. 3-cycle audit history (v1: 20 findings; v2: 8 findings; v3: 5 findings; v3 final-lock surgical patch 5 findings closed without re-audit per skip-audit pre-approval). Companion verification log at `_audit/architecture_overview_v3_verification.md` (56 substantive claims; v1 + v2 verification logs preserved for audit-trail).
- **Deliverable 2 of 7 — Database & Schema Bible:** drafting spec authorship in progress (this fresh QB session's deliverable).
- **Deliverables 3-7:** not yet started; drafting order per BIBLE_STRUCTURE_SPEC v6 § 8.2.

### 1.3 Substrate corrections from Phase 1 cycle 1 (load-bearing for downstream)

**META_PLAN v9 Aurora correction.** Architecture Overview v1 verification log Claim A.8 REFUTED the inherited Aurora cluster ARN claim (`equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`) via `aws rds describe-db-clusters` returning `DBClusterNotFoundFault`. Substrate reality (V1-11): EE uses standalone RDS PostgreSQL 16.6 instance `equine-db` (`db.t4g.micro`, endpoint `equine-db.cgtuh834bttd.us-east-1.rds.amazonaws.com:5432`, `DBClusterIdentifier=None`). Source of inherited error: cross-project contamination from `fantasy-baseball-serverless` Aurora cluster ARN bleeding into `EE_CURRENT_STATE_DUMP.md` (Tier 6). Per META_PLAN v9 § 4.5 source-priority, Tier 1 (live AWS state) governs over Tier 6. v9 corrects three body locations + metadata hygiene; LOCKED 2026-05-05.

**Cross-project dump contamination methodology lesson (Lesson 1, banked META_PLAN v9 cycle).** Tier 6 verification mandate includes cross-project contamination check, not just freshness check. The Aurora ARN inherited from `EE_CURRENT_STATE_DUMP.md` was not stale EE state; it was content from a different project (`fantasy-baseball-serverless`). Verification protocols against Tier 6 must check for cross-project bleed, not only stale-EE-state. **Operative discipline for Database & Schema Bible:** any inherited claim from EE_CURRENT_STATE_DUMP.md re-verified against live state (PostgreSQL `\dt` for table count; live AWS for any infrastructure claim) with cross-project contamination check.

---

## 2. Architecture Overview lock state — canonical references for downstream bibles

Architecture Overview is the **bible-corpus-level entry point + navigation hub**. § 4.3 IS the bible-corpus INDEX; no separate `BIBLE_INDEX.md`. Every other Phase 1 bible's Scope section cross-references back here for system topology. Database & Schema Bible inherits these canonical references:

### 2.1 § 3.x Runtime topology (canonical home for cross-runtime invariants)

- **§ 3.1 Lambda inventory:** 8 Lambdas = 5 Active + 3 INACTIVE (verified live 2026-05-05). Active: `equine-inference` (HTTP-path-based dispatcher), `equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference`, `equine-nyra-workouts`. INACTIVE: `equine-ingestion` (25-action handler at `backend/lambdas/ingestion/handler.py`), `equine-feature-engineering`, `equine-results`. Database & Schema Bible cross-references `architecture_overview:3.1` for any Lambda-State-conditional documentation.
- **§ 3.3 RDS PostgreSQL `equine-db`:** standalone instance (NOT Aurora). Connection mechanism: psycopg2 direct, `backend/shared/db.py:13-39` for `_get_connection_string()`. Database & Schema Bible's connection-mechanism documentation cross-references `architecture_overview:3.3` rather than re-establishing.
- **§ 3.6 EventBridge schedule:** 13 rules = 10 ENABLED (4 fire-and-fail + 4 active-Lambda + 2 ECS) + 3 DISABLED. Per-rule `aws events list-targets-by-rule` substrate verified (Lesson 5 non-negotiable). Database & Schema Bible references `architecture_overview:3.6` for any cron-flow schedule context.

### 2.2 § 4.x Canonical objects (cross-runtime data shapes)

- **§ 4.1 Race / Entry / PastPerformance / Workout / Result / Prediction:** core 6 canonical objects in `backend/models/canonical.py`. Adjacent classes (Track, Horse, Trainer, Jockey, RaceCard, ModelVersion) documented as scope-supporting. Database & Schema Bible's per-table canonical schema docs cross-reference `architecture_overview:4.1` for the cross-runtime-shape boundary.
- **§ 4.2 Per-pipeline prediction shapes:** three INDEPENDENTLY-DEFINED dataclasses (NO Python inheritance). PLPrediction (line 351, ~26 fields), LSPrediction (line 390, ~25 fields), base Prediction (line 428, ~21 fields + 9 dynamic attributes attached at `backend/services/wr_inference_service.py:718-730` for WR pipeline). Architectural dissonance (WR storage = canonical + dynamic = hybrid; less type-safe than PL/LS) deferred to `ml_layer_architecture_bible:4.2.1` Phase 5 disposition.

### 2.3 § 5.x Discipline rules (ratified)

- **§ 5.1 Forbidden Pattern:** Documenting a Lambda's role without verifying its current State (locked 2026-05-05).
- **§ 5.2 Common Mistake:** Documenting an EventBridge rule's behavior without cross-referencing target State (locked 2026-05-05).

Database & Schema Bible's § 5 discipline rules will surface domain-specific patterns (e.g., JSONB shape documentation discipline, migration runner mechanics, predictions-table family canonical resolution).

### 2.4 § 6 Currently Open (one substantive entry)

Fire-and-fail anomaly: 4 ENABLED EventBridge rules target 2 INACTIVE Lambdas. Database & Schema Bible's § 6 will likely have its own Currently Open entries (e.g., Bug #28 column-shift if still pending verification).

### 2.5 § 4.3 INDEX (forward-references resolving when bibles lock)

7 bibles with deliverable numbers per § 8.2 drafting order:
1. `architecture_overview.md` (LOCKED)
2. `database_schema_bible.md` (drafting now)
3. `data_pipeline_bible.md`
4. `feature_provenance_bible.md`
5. `ml_layer_architecture_bible.md`
6. `model_evaluation_retraining_bible.md`
7. `api_frontend_bible.md`

(BIBLE_STRUCTURE_SPEC v6 § 4.1 inventory order differs — § 4.1 lists Database & Schema as #6. Architecture Overview § 4.3 surfaces this divergence honestly.)

---

## 3. Option 1 self-audit framework — 9 checks across 3 clusters

**Framework origin:** Option 1 was ratified 2026-05-05 after the v2 audit cycle surfaced the recurring QB drafting-spec error pattern. Each subsequent cycle (v2 final, v3, v3 extension, v3 final-lock) added new checks as new failure modes emerged. Total 10 QB drafting-spec errors banked across 3 cycles produced 9 checks across 3 clusters.

**Operating principle:** QB performs all 9 substrate-grounded checks BEFORE sending any drafting spec to CC. If any check surfaces a question, QB resolves via direct substrate verification (not by deferring to CC drafter or to audit-CC adversarial review).

### 3.1 Substrate verification cluster (Checks 1-3)

Concerns whether QB's prescribed claims hold against primary sources.

**Check 1 — Cross-reference accuracy (origin: v1 F5 + v2 G1 BLOCKER + v2 G7 STYLE).** Every prescribed cross-reference section number verified against current substrate via direct read. Section boundaries confirmed (not just "line N has content X" but "line N falls inside section Y spanning lines A-B"). Self-audit log cites verification command or read.

**Check 2 — Count/arithmetic accuracy (origin: v1 F10 + v2 G2 MATERIAL).** Every count claim decomposed and verified. Single-source citation: one primary count statement; others derive/cite. Multi-paraphrase counts (the v9 § 12.1 8-vs-9 drift pattern) explicitly forbidden.

**Check 3 — Substrate-grounded reframing (origin: v1 F14 reframing assertion).** Any QB-introduced reframing of substrate (vs char-exact reproduction of audit-CC evidence) verified against primary source. QB has read primary source confirming reframing claim.

### 3.2 Content verification cluster (Checks 4-6)

Concerns whether QB's prescribed content is internally consistent and complete against audit-CC findings.

**Check 4 — Definition-framing internal consistency (origin: v2 G3 MATERIAL).** When prescribing definitions or enumerations, verify internal consistency against adjacent enumerations. § 2 N-category list vs § 3 N-sub-section enumeration must reconcile or surface mismatch explicitly.

**Check 5 — Synthesis verification (origin: META_PLAN v9 cycle upstream-correction synthesis error; banked Lesson 6).** When QB synthesizes audit-CC findings into upstream corrections or path decisions, upstream claim is substrate-verified before synthesis routes. Audit-CC's downstream finding doesn't propagate as upstream truth without QB substrate check.

**Check 6 — Audit-CC enumeration completeness (origin: v3 cycle CC-surfaced 2 G4 instances missed by v2 audit-CC).** When QB inherits any count claim from audit-CC findings ("4 instances of pattern X"), QB grep-verifies the count against current disk state at spec-authorship. Audit-CC enumeration gaps are propagable through QB drafting-spec scope; grep verification at QB-side closes the gap.

### 3.3 Workflow verification cluster (Checks 7-9)

Concerns whether QB's spec-authorship workflow itself produces verification surface that survives execution and remains accurate.

**Check 7 — Mid-cycle scope extensions touch all narrative-referencing sections (origin: v3 final-lock H1 MATERIAL).** When extending a spec mid-cycle (e.g., post-CC-surfacing), enumerate ALL verification-log + main-doc sections that reference the original scope; update each. Don't assume Section H/I update suffices.

**Check 8 — Line-shift-resistant citations replace literal line numbers (origin: v3 final-lock H5 MINOR).** When prescribing line numbers in verification log entries, prefer line-shift-resistant citations: section anchors (e.g., "§ 3.6 paragraph immediately preceding ENABLED table"), quoted content prefixes, or bash-grep regex patterns. Literal line numbers acceptable only when tightly scoped to a specific operation's old_str/new_str pair where char-exact matching is required.

**Check 9 — Bash-grep verification predictions distinguish targeted vs total counts (origin: v3 final-lock note-1 + note-2 spec-prediction errors).** When prescribing bash-grep verifications, separate the count of pattern-instances-being-changed-by-this-patch from the count of pattern-instances-on-disk-after-patch. The former is what the spec controls; the latter is what `grep -c` returns. Don't predict "expected = N" when N was the patch scope but the disk includes pre-existing legitimate instances of the same pattern. Either count both, or scope the predicted pattern more precisely (regex including surrounding context that distinguishes targeted from pre-existing).

### 3.4 Method-validity self-check discipline

Each new banked check passes a distinctness test against existing checks: "Would Check K catch this failure mode?" Across 9 checks, every banked check has been verified distinct (no Check K' duplicates Check K's coverage). Over-fragmentation (every error class becomes its own check) and under-fragmentation (multiple distinct failure modes folded into one check) are both failure modes; the cluster framing (3 clusters × ~3 checks each) prevents both.

**Trajectory expectation for Database & Schema Bible v1 cycle:**
- If audit-CC catches NO new QB drafting-spec error class (only CC-content findings or audit-CC adversarial finds in CC's prose), Option 1 with 9 checks is converging.
- If audit-CC catches a new QB drafting-spec error class not covered by Checks 1-9, bank as Check 10 + revise cluster framing if it doesn't fit substrate/content/workflow categorization.

---

## 4. 10 banked QB drafting-spec errors (with classifications)

Comprehensive enumeration across 3 audit cycles.

### v1 audit cycle (4 errors)

1. **F5 broken cross-reference** — META_PLAN § 7.10 cited as model-registry layout; § 7.10 is "Commit-Before-Deploy Discipline." Class: Check 1 (cross-reference accuracy).
2. **F10 deliverable-numbering arithmetic error** — 3 ML bibles each numbered "4 of 7"; arithmetic doesn't add to 7. Class: Check 2 (count/arithmetic accuracy).
3. **F14 PL/LS-as-specializations reframing assertion** — substrate showed PL/LS are independently-defined dataclasses with no Python inheritance. Class: Check 3 (substrate-grounded reframing).
4. **Upstream-correction synthesis error during v9 path-decision** — META_PLAN v8's Aurora claim was not substrate-verified before scoping v9 path. Class: Check 5 (synthesis verification).

### v2 audit cycle (3 errors)

5. **G1 BLOCKER broken cross-reference** — BIBLE_STRUCTURE_SPEC v6 § 6.4 cited; substrate at § 6.5. Class: Check 1.
6. **G2 MATERIAL undercount** — equine-ingestion described as 3 admin actions; substrate showed 25 action handlers. Class: Check 2.
7. **G3 MATERIAL definition-framing missing EventBridge** — § 2 listed 6 categories covering 8 services; § 3 enumerated 8 sub-sections with EventBridge omitted. Class: Check 4 (definition-framing internal consistency).

### v3 audit cycle (3 errors, including v3 final-lock cycle)

8. **H1 MATERIAL post-extension verification-log narrative staleness** — Section G G4 closure entry not updated after v3 extension added Operations 9 + 10. Class: Check 7 (mid-cycle scope extension narrative discipline).
9. **H5 MINOR patch-induced line-number drift** — Section G entries cited line numbers off-by-one from disk state after revision history bullet insertion. Class: Check 8 (line-shift-resistant citations).
10. **Note-1 + Note-2 bash-grep prediction conflation** — spec predicted `grep -c "at v2 lock" → 0` and `grep -c "at lock" → 5`; disk reality 1 (in v3 revision history narrative) and 13 (5 H2 + 8 pre-existing). Class: Check 9 (bash-grep prediction precision).

---

## 5. Methodology lessons 1-6 (active discipline; Lesson 3 expanded)

Banked from META_PLAN v9 cycle + Architecture Overview cycle. Operative as discipline for Database & Schema Bible cycle; will be codified into AUDIT_METHODOLOGY future cycle once additional Phase 1 cycles surface convergence.

**Lesson 1** — Tier 6 verification mandate includes cross-project contamination check, not just freshness check.

**Lesson 2** — Phase 1 verification surfaces Phase 0 substrate errors; surgical correction to Phase 0 documents is expected response.

**Lesson 3 (re-expanded)** — Drafting specs cite primary verification log claim IDs, not paraphrased restatements. Discipline applies broadly: claim IDs, count statements, quoted text, attribution paraphrases, prescribed cross-reference section numbers, prescribed definition framing content, audit-CC enumeration completeness, line-number citations (Check 8 makes them line-shift-resistant), and bash-grep prediction precision (Check 9).

**Lesson 4** — Any FRAMEWORK_GAP reframing in CC's draft requires substrate verification before CC asserts it. CC surfaces FRAMEWORK_GAP, fills what fits honestly, lets QB triage. If CC has a candidate reframing, CC presents it as candidate AND cites the substrate that supports OR refutes it.

**Lesson 5** — EventBridge documentation cites `aws events list-targets-by-rule` output per rule, not `aws events list-rules` output alone. Target and State are independent AWS resources.

**Lesson 6** — QB synthesis of audit findings into upstream-correction scope requires substrate verification of upstream claim.

---

## 6. Phase 1 cycle process

### 6.1 Standard cycle steps

1. **Spec authorship (QB):** under Option 1 with 9 checks operative; substrate verifications run before spec goes to CC.
2. **CC drafts + verification log:** char-exact reproduction discipline; verification log is mandatory companion (Tier 3).
3. **QB reviews + spot-checks:** reads draft fully; spot-checks 4-6 verification log entries against primary substrate.
4. **Audit-CC adversarial review:** fresh CC session; standard 6 adversarial questions per META_PLAN v9 § 6.2 + Phase 1 checklist additions + lesson-1-6 verification + threshold judgment.
5. **Iterate to lock:** v2/v3/etc. cycles until threshold met.

### 6.2 Skip-audit pre-approval pattern (4 conditions)

Surgical-cosmetic patches qualify for skip-audit when ALL of these hold:
- Scope is confined to corrections + cosmetic improvements
- Char-exact reproduction discipline operative
- Zero new methodology constructs introduced
- Zero new substantive content beyond audit-finding closures

Skip-audit pre-approval can also be granted by audit-CC explicitly in an audit closing recommendation (e.g., v3 final-lock cycle).

### 6.3 Substrate-correction patches absorbed into surgical-cosmetic cycles

When Phase 1 verification surfaces Phase 0 substrate errors (per Lesson 2), the correction is applied as a surgical patch to the Phase 0 document (e.g., META_PLAN v8 → v9 Aurora correction). This is Path C scope: substrate correction + metadata hygiene + revision history. Skip-audit pre-approval typically holds for these cycles when Path C scope is preserved and char-exact discipline operative.

### 6.4 BLOCKER findings always trigger fresh adversarial review

No skip-audit on BLOCKER cycles. v3 cycle was REVISE AND RE-AUDIT path because of G1 BLOCKER classification, even though surface area was small. Audit-CC re-pass on v3 patched draft was non-negotiable.

### 6.5 Tony's hard threshold (reaffirmed; non-negotiable)

For LOCK AFTER MINOR REVISIONS path:
- **Zero fabricated content** (hard fail regardless of count)
- **Zero methodology-interpolation** findings (hard fail regardless of count, per META_PLAN v9 § 6.1)
- **< 5 MATERIAL** findings
- **Zero un-closed prior-cycle findings** (regression check)

If any condition fails: REVISE AND RE-AUDIT (≥ 5 MATERIAL OR fabricated OR methodology-interpolation OR un-closed) or SUBSTANTIAL REWORK (≥ 1 BLOCKER OR ≥ 10 MATERIAL).

---

## 7. Standing CC paste-prompt patterns

### 7.1 CC drafter paste-prompt boilerplate

Every CC drafting paste-prompt includes:

> Execute exactly the prescribed operations; do not extend scope; surface adjacent surfaces, prediction inaccuracies, and substrate observations during verification for QB awareness. Char-exact reproduction discipline operative for surgical patches; full prose authoring latitude for substantive drafts (with all factual claims requiring verification log entries per Tier 3 discipline).

### 7.2 CC verification log structure

Mandatory companion for every Tier 3 deliverable:
- **Section A:** inherited claims from upstream Phase 0 verification logs (re-verification timestamps).
- **Section B:** inherited claims from prior cycles of THIS bible's verification logs (if any).
- **Section C:** new V<N>-N claims with primary citations.
- **Section D:** methodology-interpolation self-check (target: ZERO).
- **Section E:** pattern-completion check (W.N exclusivity preserved; numeric IDs honored).
- **Section F:** FRAMEWORK_GAP / SPEC_GAP markers (target: ZERO unless surfaced honestly).
- **Section G:** prior-cycle audit findings closure verification (regression check) for cycles ≥ 2.
- **Section H:** QB self-audit log (banked starting v3 cycle; reproduces QB's spec-authorship verifications descriptively).
- **Section I:** new entries for surgical patch operations (when applicable).

### 7.3 Audit-CC paste-prompt boilerplate

Every audit-CC paste-prompt includes:
- Project context (EE description; phase state; QB/CC/audit-CC roles)
- Reference materials (drafted document + verification log + prior audits + Phase 0 substrate)
- Verification discipline (HARD RULE: prefer live state over verification log claims; spot-check verification entries)
- 6 adversarial questions per META_PLAN v9 § 6.2
- Phase 1 checklist additions (G8 fix-date discipline; G-new-1 numeric candidate IDs; G-new-2 inheritance pattern)
- Lesson 1-6 application correctness checks
- Threshold context with explicit anti-threshold-gaming caution

---

## 8. Database & Schema Bible-specific drafting context

### 8.1 BIBLE_STRUCTURE_SPEC v6 § 6.6 prescribes the template

Located at lines 856-927 of BIBLE_STRUCTURE_SPEC.md (verified by QB read 2026-05-05). Key sections:
- § 1 Scope, § 2 Definitions, § 3 Schema overview (table inventory, materialized view, migration runner, predictions-table family), § 4 Per-table canonical schema docs (4.1.<table_name> sub-sections), § 5 Discipline rules, § 6 Currently Open, § 7 Deprecated, § 8 What Was Fixed.
- **G-new-2 closure operative:** § 4.1 enumeration scope = CREATE TABLE declarations only. Materialized view (1 matview) lives at § 3, NOT § 4.1.

### 8.2 META_PLAN v9 § 7.12 governs migration discipline

Migration filename convention: `NNN_short_description.sql` for migrations 001-011 (grandfathered); `NNN_YYYYMMDD_*.sql` from 012+ (going forward). Database & Schema Bible documents:
- Migration runner mechanism (`schema_migrations` table + `backend/database/migrations/migrate.py`)
- 11 existing migrations enumerated (with the duplicate-005 case documented honestly)
- Migration discipline going forward (file naming + running + rollback)

### 8.3 META_PLAN v9 § 9.10 + § 9.11 govern JSONB conventions

Database & Schema Bible documents JSONB shape conventions for:
- `model_versions.feature_list` (canonical feature schema per model)
- `model_versions.hyperparameters` (training-time hyperparameter snapshot)
- `model_versions.metadata` (version-tracking metadata)
- Other JSONB fields surfacing during substrate verification

### 8.4 14 tables + 1 matview verified count (re-verification mandate)

QB at spec-authorship runs `psql ... -c "\dt"` against `equine-db` to re-verify table count. Decomposition expected: 14 CREATE TABLE entries + 1 matview. Per Lesson 1, cross-project contamination check at re-verification: confirm tables are EE schema, not bleed from any adjacent project.

### 8.5 Predictions-table family canonical resolution required

Database & Schema Bible documents the predictions-table family:
- Legacy `predictions` table (created by `001_initial_schema.sql:327`; 6,600 rows; superseded by per-pipeline tables but NOT dropped; active readers in `prediction_router.py`, `race_router.py`, `dashboard_router.py`, `horse_router.py`)
- Per-pipeline replacements created by migration 005 (`005_three_prediction_tables.sql`): `wr_predictions`, `pl_predictions`, `ls_predictions`
- Cross-reference Architecture Overview § 4.2 for the per-pipeline dataclass shapes (PLPrediction, LSPrediction, base Prediction with WR dynamic-attribute attachment)
- Deprecated entry at § 7 for legacy `predictions` table (per BIBLE_STRUCTURE_SPEC v6 § 5.6.4 Deprecated entry template)

### 8.6 model_versions registry per META_PLAN v9 verification log

88 rows = 45 active + 43 inactive (verified live via dashboard endpoint per META_PLAN v9 Claim 7). Multi-active-row reality (per META_PLAN v9 § 9.13): the 45 active rows span (model_type, style, specialist) combinations; current `get_active_model_by_type` selection function takes only `model_type` → `LIMIT 1` returns arbitrary row when multiple match. Database & Schema Bible documents the `model_versions` table; substantive selection-function disposition belongs to `ml_layer_architecture_bible:3.1` (model registry semantics).

### 8.7 W.N entries cite global Bug #N convention

Per BIBLE_STRUCTURE_SPEC v6 § 5.5.1: bugs assigned canonical global Bug #N at discovery time; cross-bible references use `<bible>:#<bug-id>` format. Database & Schema Bible's § 8 W.N entries cite global Bug #N (e.g., "Bug #28" for HRN scraper column shift) even though the canonical home for Bug #28 is `data_pipeline_bible:8.W.<n>` (per § 5.3 cross-cutting bug scope rule — Bug #28's prevention is a data-acquisition discipline, not a schema discipline).

---

## 9. Substrate verifications required before Database & Schema Bible spec authorship

QB substrate-verification overhead estimate: 30-45 min minimum (per Option 1 with 9 checks); may scale to 45-60 min for substrate-heavy spec.

### 9.1 Per Check 1 (cross-reference accuracy)

- BIBLE_STRUCTURE_SPEC v6 § 6.6 — full read for prescribed TOC + per-section guidance + cross-references
- META_PLAN v9 § 7.12 — migration discipline cross-references (verify section content matches what spec will prescribe)
- META_PLAN v9 § 9.10 + § 9.11 — JSONB conventions
- BIBLE_STRUCTURE_SPEC v6 § 5.5 + § 5.6 — W.N format + Forbidden Pattern + Common Mistakes templates
- Architecture Overview § 4.1 line numbers (for cross-references to canonical objects: Race line 255, Entry line 214, PastPerformance line 77, Workout line 58, Result line 296, Prediction line 428)

### 9.2 Per Check 2 (count accuracy)

- 14 tables + 1 matview (re-verify via `\dt` against equine-db — primary citation)
- Migration count (currently 011) — re-verify via `ls /home/strakajagr/projects/equine-equalizer/backend/database/migrations/`
- Predictions-table family (legacy + 3 per-pipeline = 4 tables) — re-verify via `\d wr_predictions \d pl_predictions \d ls_predictions \d predictions`
- model_versions row counts (88 = 45 active + 43 inactive) — re-verify via dashboard endpoint or direct SQL
- legacy `predictions` table row count (6,600 per META_PLAN v9 inheritance) — re-verify via `SELECT COUNT(*) FROM predictions`

### 9.3 Per Check 3 (substrate-grounded reframing)

- Bug #28 column-shift status — re-verify symptom statement against operator memory file at `equine-equalizer-bug-28-hrn-scraper.md`
- Bug #15 → Bug #24 chain at calibration bypass — re-verify lines 616-626 of `wr_inference_service.py`
- JSONB canonical patterns (`model_versions.feature_list`, `model_versions.hyperparameters`, `model_versions.metadata`) — re-verify schema + sample row
- Migration 005 duplicate case — re-verify via migration directory listing + git log

### 9.4 Per Check 4 (definition-framing internal consistency)

- Database & Schema Bible § 2 Definitions vs § 3 + § 4 enumeration consistency check (similar to Architecture Overview's 9-services-7-categories pattern; verify all definitions reconcile against enumerated tables/concepts)

### 9.5 Per Check 9 (bash-grep prediction precision)

- Each prescribed bash-grep verification scoped with discriminating context regex; not bare pattern counts
- For each predicted count, QB explicitly distinguishes targeted-by-this-patch vs total-on-disk-after-patch

---

## 10. CC handoff to fresh QB session

**Action sequence for fresh QB session:**

1. **Read this handoff document** at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/QB_HANDOFF_DATABASE_SCHEMA_BIBLE_DRAFTING.md` FIRST.
2. **Read Architecture Overview LOCKED state** at `/home/strakajagr/projects/equine-equalizer/docs/bible/architecture_overview.md` for canonical references.
3. **Read BIBLE_STRUCTURE_SPEC v6 § 6.6** at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` lines 856-927 for the Database & Schema Bible template.
4. **Read META_PLAN v9 § 7.12 + § 9.10 + § 9.11** for migration + JSONB substrate.
5. **Run substrate verifications** per Section 9 of this handoff (~30-45 min).
6. **Author Database & Schema Bible drafting spec** under Option 1 with 9 checks operative + Check 8 line-shift-resistant citations + Check 7 extension-anticipation discipline + Check 9 bash-grep prediction precision.
7. **QB self-audit log Section H** entries reproduced in spec for traceability.
8. **Spec output target:** paste-ready CC paste-prompt (CC drafts + produces verification log).
9. **Standard Phase 1 cycle process** applies: CC drafts → QB reviews → audit-CC adversarial pass → iterate to lock against threshold.

---

## 11. Standing observations for AUDIT_METHODOLOGY future cycle

When AUDIT_METHODOLOGY next cycles, codify:
- 9-check Option 1 framework as formal "QB drafting-and-synthesis discipline" rules
- 3-cluster organization (Substrate / Content / Workflow)
- Method-validity self-check discipline (distinctness test for new banked checks)
- Cluster-framing makes checklist scannable rather than enumerable
- Pattern-completion check operative on letter-prefixes (W.N exclusivity)
- Skip-audit pre-approval 4-condition pattern formalized

10 banked QB drafting-spec errors with classifications serve as the worked-examples corpus for the codification.

---

**End of QB Handoff: Database & Schema Bible Drafting Spec Authorship.**

Fresh QB session opens this document, then proceeds to substrate verifications + spec authorship. Architecture Overview LOCKED 2026-05-05; Phase 1 cycle 2 begins.
