# QB DRAFTING SPEC — FEATURE PROVENANCE BIBLE (PHASE 1 DELIVERABLE 4)

**Cohort:** Phase 1 Deliverables 4-5-6 (Parallel Cohort)
**Bible Number:** 4
**Bible Short:** fp
**Output Path:** `/home/strakajagr/projects/equine-equalizer/docs/bible/feature_provenance_bible.md`
**Output Version:** v1-draft (pre-audit), v1 (post-audit lock)
**Parallel Partner:** ML Layer Architecture Bible (Bible 5, mla)
**Sequential Downstream:** Model Evaluation & Retraining Bible (Bible 6, mer)

---

## § 1. FORCING FUNCTION (CANONICAL)

For every feature × every consuming model in the EE production gallery (plus orphan-flagged scope per § 3), the bible must answer:

> **source data → engineering code → consuming model(s) → target latent → train/inference duplication or divergence**

Every dimension of this forcing function must appear as a column in the per-feature row schema (§ 5). No dimension may be omitted. No row may have an empty cell in a forcing-function column without explicit UNVERIFIED treatment per § 5.7.

---

## § 2. INHERITANCE BUNDLE — READ AT SESSION START

Drafting CC reads the following before any draft authorship. Read order recommended:

### § 2.1 Phase 0 Locks
1. META_PLAN v9
2. BIBLE_STRUCTURE_SPEC v6
3. AUDIT_METHODOLOGY v2-patched
4. CONVERGENCE_CRITERIA v2
5. TRIAGE_QUEUE_SPEC v1

### § 2.2 Phase 1 Locks
6. `docs/bible/architecture_overview.md` (Architecture Overview v3)
7. `docs/bible/database_schema_bible.md` (D&S Bible v1-patched-d2)
8. `docs/bible/data_pipeline_bible.md` (Data Pipeline Bible v1-patched-c)

### § 2.3 Cohort Substrate
9. `docs/bible/_meta/QB_HANDOFF_PARALLEL_COHORT_DRAFTING.md`
10. This spec.

---

## § 3. SCOPE (RATIFIED Q5)

Production + orphan-flagged with two-tier orphan classification.

### § 3.1 Production Scope
A feature is in production scope if it is consumed by at least one model currently serving inference in the EE production model gallery.

### § 3.2 Orphan Scope (Two-Tier)
- **ORPHAN-PRODUCTION:** Feature exists in feature engineering code; no model anywhere consumes it. Phase 5 disposition: kill or assign consumer.
- **ORPHAN-EXPLORATORY:** Feature exists in feature engineering code; consumed only by non-production paths (development scaffolding, notebooks, exploratory training scripts). Phase 5 disposition: distinct from ORPHAN-PRODUCTION; classification preserved for re-architecture.

Orphan rows use `consuming_models = [ORPHAN-PRODUCTION]` or `[ORPHAN-EXPLORATORY]`. Train/inference column (§ 5.7) is `N/A — orphan` with narrative note explaining classification basis.

### § 3.3 Out of Scope
- Features considered for engineering but not implemented in code (no row).
- Deprecated feature versions superseded by current implementations (no row; current implementation only).

---

## § 4. SUBSTRATE READ AUTHORIZATION (RATIFIED Q7)

Drafting CC is authorized to read the following EE codebase substrate domains. Discovery via `list_directory` and `search_files` from EE project root. QB does NOT pre-enumerate paths.

| Domain | Authorized | Notes |
|--------|------------|-------|
| A. Locked Phase 1 bibles | YES | Per § 2 inheritance bundle |
| B. Feature engineering source code | YES | Discover via list_directory / search_files |
| C. Model definition source code | YES | Class definitions, hyperparameter configs |
| D. Training pipeline scripts | YES | Discover paths |
| E. Inference pipeline scripts | YES | Production serving paths |
| F. Model artifact metadata | YES | Model store entries, training timestamps, version tags |
| G. Configuration files | YES | Feature flags, deployment configs |
| H. Live database read | NO | Deferred to credential-authorized cycle; D&S Bible inheritance is canonical schema substrate |

Drafting CC inventories all paths read in the Verification Log (§ 9).

---

## § 5. PER-FEATURE ROW SCHEMA

Each feature in scope receives one row in § 4.1 of the bible. Row columns:

### § 5.1 F-ID
Monotonic integer, prefix `F-` (e.g., `F-1`, `F-2`, `F-23`). Stable across the bible. No reuse on deletion.

### § 5.2 Feature Name
Canonical identifier matching the name used in engineering code. Verbatim match required — no reformatting, no clarifying renames.

### § 5.3 Source Data
Source table(s) and column(s) feeding this feature. Reference D&S Bible v1-patched-d2 entities using existing convention (per Q9 backward-compat clarification): e.g., `database_schema_bible:§ 4.1.3` for the table, with explicit column name. Multiple source columns listed comma-separated.

### § 5.4 Engineering Code
File path + line range citation showing where this feature is computed. Format: `<repo-relative path>:<start_line>-<end_line>`. Example: `feature_eng/rolling.py:142-187`. Multiple engineering sites cited if feature is computed in multiple places (likely a finding flagged in narrative).

### § 5.5 Consuming Models
List of `mla:M-N` references for every production model consuming this feature. For orphan features per § 3.2, single-element list `[ORPHAN-PRODUCTION]` or `[ORPHAN-EXPLORATORY]`.

### § 5.6 Target Latent
The latent variable this feature contributes to in the ML stack. Examples: `win_probability`, `form_trajectory`, `longshot_signal`, `pairwise_rank_score`. Drafting CC discovers latent vocabulary from MLA's parallel draft via SP-2 reconciliation; before SP-2, uses placeholder vocabulary marked `[PROVISIONAL]` with note for SP-2 reconciliation.

### § 5.7 Train/Inference Status (RATIFIED Q8 — QUATERNARY)
One of:
- **DUPLICATED** — Feature computed identically in training and inference paths. Verification: same engineering code path serves both, OR independently verified equivalent computation.
- **DIVERGENT-INTENTIONAL** — Training and inference compute differently by design. Common case: training uses ground-truth historical data; inference uses real-time approximation. Verified intentional.
- **DIVERGENT-UNINTENTIONAL** — Training and inference compute differently and divergence is unintended. **HIGHEST-STAKES FINDING** — data leakage candidate.
- **UNVERIFIED** — Drafting CC cannot conclude from substrate alone whether training and inference duplicate or diverge. Honest uncertainty per Lesson § 4.11.

### § 5.8 Train/Inference Narrative
**REQUIRED** free-form note. For DUPLICATED: brief verification statement with code-line citations for both paths. For DIVERGENT-*: specific divergence description with code-line citations for both paths and explicit divergence characterization (window size, computation logic, data source, etc.). For UNVERIFIED: explanation of why verification could not be concluded and what substrate would resolve it.

Example: "Training computes feature over 90-day rolling window at `feature_eng/rolling.py:142`; inference computes over 30-day window at `inference/realtime.py:88`. Window mismatch unintended per absence of design comment in either site. DIVERGENT-UNINTENTIONAL."

### § 5.9 Notes
Optional free-form column for orphan rationale, multi-site engineering, version-supersession context, or other Phase 5 disposition cues.

---

## § 6. REQUIRED BIBLE STRUCTURE
Feature Provenance Bible
v1-draft / v1 / v1-patched-{a,b,c,...}
LOCKED <date> | DRAFT <date>
§ 1. Scope (Q5 two-tier orphan-flagged production)
§ 2. Forcing Function (canonical statement per this spec § 1)
§ 3. Inheritance References (cross-refs to Phase 1 locks per Q9)
§ 4. Feature Gallery
§ 4.1 Per-Feature Rows (one row per feature, schema per spec § 5)
§ 4.1.1 F-1 ...
§ 4.1.2 F-2 ...
...
§ 4.2 Orphan Inventory (subset view of § 4.1 filtered to ORPHAN-* rows)
§ 4.2.1 ORPHAN-PRODUCTION inventory
§ 4.2.2 ORPHAN-EXPLORATORY inventory
§ 5. Train/Inference Findings Summary
§ 5.1 DUPLICATED count + index
§ 5.2 DIVERGENT-INTENTIONAL count + index
§ 5.3 DIVERGENT-UNINTENTIONAL count + index (FLAG: data leakage candidates)
§ 5.4 UNVERIFIED count + index
§ 6. Cross-Reference Index
§ 6.1 fp:F-N → mla:M-N matrix (forward)
§ 6.2 mla:M-N → fp:F-N matrix (reverse, populated post-SP-2)
§ 7. Verification Log (per spec § 9)

Section numbering is fixed per this spec. Drafting CC may add subsections as needed but may not renumber or restructure top-level sections without QB authorization.

---

## § 7. CROSS-REFERENCE CONVENTION (RATIFIED Q9)

### § 7.1 Forward-Only Two-Tier Convention (Own Bible)
- Internal feature references: `fp:F-N`
- Internal section references: `feature_provenance_bible:§ <section-number>`

### § 7.2 Cross-Bible References (Cohort)
- To ML Layer Architecture: `mla:M-N` for model entities; `ml_layer_architecture_bible:§ <section>` for sections.
- To Model Evaluation & Retraining: `mer:E-N` for evaluation criteria; `mer:T-N` for retraining triggers; `model_evaluation_retraining_bible:§ <section>` for sections.

### § 7.3 Backward-Compat to Phase 1 Locks
Cohort bibles use locked bibles' existing conventions:
- Architecture Overview: `architecture_overview:§ <section>` (existing pattern).
- D&S Bible: `database_schema_bible:§ <section>` (existing pattern). Entity-class IDs not used for D&S Bible per current convention.
- Data Pipeline Bible: `data_pipeline_bible:§ <section>` and `data_pipeline_bible:F.<flow-id>` (existing pattern).

---

## § 8. SYNCHRONIZATION POINT PROTOCOL

Per Handoff § 4. Drafting CC PAUSES at SP-1 and SP-2, EMITS specified artifacts, RESUMES only on QB authorization (mediated by Tony).

### § 8.1 SP-1 — TOC + § 1 Scope
- **Trigger:** Drafting CC has authored the bible's Table of Contents and § 1 Scope.
- **Pause action:** Drafting CC stops authoring further sections.
- **Emission to Tony:** Verbatim copy of TOC + § 1, plus a brief self-summary stating: "(a) section-numbering scheme used, (b) scope-boundary statement, (c) identifier conventions used for cross-references."
- **Wait condition:** Drafting CC waits for one of {CONTINUE, REVISE-FP, REVISE-MLA, REVISE-BOTH} from QB (via Tony).
- **Resume:** On CONTINUE or after revision satisfying QB findings.

### § 8.2 SP-2 — § 4.1 First Three Entities
- **Trigger:** Drafting CC has authored § 4.1 (Per-Feature Rows) covering at least the first three features.
- **Pause action:** Drafting CC stops authoring further features.
- **Emission to Tony:** Verbatim copy of § 4.1.1, § 4.1.2, § 4.1.3 (full row content per schema § 5), plus a brief self-summary stating: "(a) target latent vocabulary used, (b) train/inference quaternary distribution across the three rows, (c) consuming-models references emitted (`mla:M-N` list)."
- **Wait condition:** Drafting CC waits for one of {CONTINUE, REVISE-FP, REVISE-MLA, REVISE-BOTH} from QB (via Tony).
- **Resume:** On CONTINUE or after revision satisfying QB findings.

### § 8.3 SP-3 — Pre-Model-Evaluation Gate
- **Trigger:** Drafting CC has completed full v1-draft (all sections § 1 through § 7 present, verification log emitted).
- **Pause action:** Drafting CC stops; v1-draft is final from this CC's perspective.
- **Emission to Tony:** Full v1-draft path on disk, byte count, line count, and verification log per § 9.
- **Wait condition:** Drafting CC awaits SP-3 disposition. Phase B (Bible 6 drafting) is gated on QB authorization, not on this drafting CC. This drafting CC's session ends after SP-3 emission.

### § 8.4 Discipline
- SP-1 and SP-2 are blocking for both parallel drafting CCs (per handoff § 4.4). Bible 4 CC may not pass SP-1 until Bible 5 CC also reaches SP-1, and vice versa. The QB resolution is the un-block.
- Drafting CC must NOT speculate about parallel partner's content. SP findings flow only through QB.
- Drafting CC must NOT modify locked Phase 1 bibles. Findings about locked substrate go in narrative notes flagged for QB UPSTREAM-CORRECTION evaluation per Handoff § 7.

---

## § 9. VERIFICATION LOG

Drafting CC emits a Verification Log as § 7 of the bible. Required content:

1. **Inheritance read inventory** — every file from § 2 read, with byte count and read timestamp.
2. **Substrate path inventory** — every code path read under § 4 authorization, with file path, line ranges accessed, and purpose (e.g., "feature_eng/rolling.py:142-187 — verified F-23 engineering site").
3. **Self-audit checklist** — § 10 nine-check list with PASS / FAIL / PARTIAL state and rationale per check.
4. **Provisional latent vocabulary** — list of target_latent values used in § 4.1 with note flagging vocabulary as awaiting SP-2 reconciliation with MLA.
5. **Cross-reference forward-stub list** — every `mla:M-N` reference emitted in § 4.1 (drafting CC does not know if these resolve until corpus audit; stub list enables corpus-audit cross-reference verification).
6. **Findings flagged for UPSTREAM-CORRECTION evaluation** — any substrate inconsistencies discovered against locked Phase 1 bibles (D&S, Data Pipeline, Architecture Overview), surfaced as raw observations for QB triage. Drafting CC does NOT author UPSTREAM-CORRECTION patches.

---

## § 10. SELF-AUDIT — 9 CHECKS ACROSS 3 CLUSTERS

Drafting CC executes these checks before SP-3 emission. Results recorded in Verification Log § 9.3.

### Cluster I — Substrate Verification
1. **Inheritance bundle complete** — all 10 items in § 2 read at session start.
2. **Authorized substrate read** — domains A–G per § 4 read; H not attempted.
3. **Convention identifiers verified at primary source** — table names, column names, file paths, model names verified at primary source at row-authorship time (Lesson 3 expansion).

### Cluster II — Content Verification
4. **Forcing function fully served** — every per-feature row has all columns per schema § 5 populated; no empty forcing-function cells without UNVERIFIED treatment.
5. **Internal consistency** — every fp:F-N referenced internally exists in § 4.1; every mla:M-N reference is recorded in § 6.1 forward index for corpus-audit verification.
6. **Verification claims supported by code-line citations** — every DUPLICATED / DIVERGENT-* status in § 5.7 has corresponding § 5.8 narrative with explicit code-line citations (Lesson § 4.11 prediction-precision).

### Cluster III — Workflow Verification
7. **SP-1 and SP-2 emissions executed with required artifacts** — both pause-emit-resume cycles completed; Verification Log records SP findings received.
8. **Cross-reference convention applied per Q9** — own-bible references use `fp:F-N` / `feature_provenance_bible:§ N`; cohort cross-refs use `mla:M-N` / `mer:E-N`-`mer:T-N`; Phase 1 lock cross-refs use existing conventions of locked bibles.
9. **Verification log emitted at v1-draft completion** — § 7 of bible is populated and complete before SP-3 emission.

Any FAIL or PARTIAL state must be reported to Tony in SP-3 emission with explanation. Drafting CC does not unilaterally remediate failures.

---

## § 11. WRITE DISCIPLINE

Drafting CC writes:
- The bible itself at output path (§ output path declaration above).
- Verification Log as § 7 of the bible (not a separate file).

Drafting CC does NOT write to disk:
- Any locked Phase 1 bible (no modifications to locked substrate).
- Any meta document outside the assigned output.
- Any spec / handoff / audit document.

Per Handoff § 11 and Lesson § 4.12: QB does not invoke MCP write tools. This drafting CC IS authorized to write its assigned bible. Write authorization is bounded to the single output path declared in this spec.

---

**END DRAFTING SPEC — FEATURE PROVENANCE BIBLE**
