# QB DRAFTING SPEC — MODEL EVALUATION & RETRAINING BIBLE (PHASE 1 DELIVERABLE 6)

**Cohort:** Phase 1 Deliverables 4-5-6 (Parallel Cohort, Phase B sequential)
**Bible Number:** 6
**Bible Short:** mer
**Output Path:** `/home/strakajagr/projects/equine-equalizer/docs/bible/model_evaluation_retraining_bible.md`
**Output Version:** v1-draft (pre-corpus-audit), v1 (post-corpus-audit lock)
**Phase A Predecessors:** Feature Provenance Bible (Bible 4, fp) v1-draft + ML Layer Architecture Bible (Bible 5, mla) v1-draft
**Cohort Sequential Position:** Phase B single-CC drafting after Phase A AUTHORIZE-PHASE-B for both predecessors

---

## § 1. FORCING FUNCTION (CANONICAL)

For every model in the EE production model gallery (11 entities M-1 through M-11 inherited from MLA v1-draft § 4.1 ratified roster), the bible must answer:

> **per-model success criteria → retraining triggers → calibration discipline → model artifact version control → deployment gating**

Every dimension of this forcing function must appear as a column in the per-model row schema (§ 5). No dimension may be omitted. No row may have an empty cell in a forcing-function column without explicit UNVERIFIED treatment per § 5 quaternary discipline OR explicit N/A treatment per § 3.3 non-trained-model handling.

---

## § 2. INHERITANCE BUNDLE — READ AT SESSION START

Drafting CC reads the following before any draft authorship. Read order recommended:

### § 2.1 Phase 0 Locks
1. META_PLAN v9
2. BIBLE_STRUCTURE_SPEC v6
3. AUDIT_METHODOLOGY v2-patched
4. CONVERGENCE_CRITERIA v2
5. TRIAGE_QUEUE_SPEC v1

### § 2.2 Phase 1 Locks (Predecessors 1-2-3)
6. `docs/bible/architecture_overview.md` (Architecture Overview v3, LOCKED 2026-05-05)
7. `docs/bible/database_schema_bible.md` (D&S Bible v1-patched-d2, LOCKED 2026-05-06)
8. `docs/bible/data_pipeline_bible.md` (Data Pipeline Bible v1-patched-c, LOCKED 2026-05-06)

### § 2.3 Phase A Cohort Predecessors (v1-draft state, NOT yet locked, corpus-audit-ready)
9. `docs/bible/feature_provenance_bible.md` (FP v1-draft post-revise-pass, AUTHORIZE-PHASE-B 2026-05-06)
10. `docs/bible/ml_layer_architecture_bible.md` (MLA v1-draft, AUTHORIZE-PHASE-B 2026-05-06)

### § 2.4 Cohort Substrate
11. `docs/bible/_meta/QB_HANDOFF_PARALLEL_COHORT_DRAFTING.md`
12. This spec.

**Critical inheritance discipline:** FP and MLA v1-drafts are NOT locked. Cross-references from MER to FP/MLA use forward-only convention `fp:F-N` and `mla:M-N`. Cross-bible cross-reference resolution freezes at corpus-audit gate per Handoff § 6.1. Until corpus-audit, drafting CC may emit cross-references that may need adjustment if FP/MLA undergo UPSTREAM-CORRECTION (per Handoff § 7) at corpus audit. This is expected; corpus audit reconciles.

---

## § 3. SCOPE (RATIFIED Q10)

11 per-model rows mirroring MLA gallery 1:1 with explicit N/A handling for non-trained models.

### § 3.1 Production-Deployed Gallery Inheritance
The 11 production model entities are inherited from MLA v1-draft § 4.1 ratified at SP-1:
- M-1: wp_core (XGBoost binary:logistic — WR Layer 1, no-workout)
- M-2: wp_full (XGBoost binary:logistic — WR Layer 1, workout-aware)
- M-3: rk_core (XGBoost rank:pairwise — WR Layer 2, no-workout)
- M-4: rk_full (XGBoost rank:pairwise — WR Layer 2, workout-aware)
- M-5: pl_core (XGBoost reg:squarederror — PL Layer 1)
- M-6: WR Arithmetic Value Overlay (compute_value_overlay — non-trained)
- M-7: PL Arithmetic EV/Kelly Overlay (compute_ev_and_kelly — non-trained)
- M-8: Random Forest Longshot Classifier (longshot_rf — LS Layer 4)
- M-9: LSTM Form Trajectory (trajectory_lstm — LS Layer 5)
- M-10: Beta-Binomial Bayesian Angle Scorer (LS Layer 6 — non-trained, statistical)
- M-11: Logistic Regression Stacking Ensemble (ensemble — LS Layer 7)

Drafting CC verifies this roster against MLA v1-draft § 4.1 at session start. Any discrepancy (e.g., MLA UPSTREAM-CORRECTION between Phase A v1-draft and MER drafting time) flags in Verification Log § 7.7 for QB triage. Drafting CC does NOT unilaterally add or remove models from the roster.

### § 3.2 Trained Models In Scope (8 entities)
M-1, M-2, M-3, M-4, M-5, M-8, M-9, M-11 are trained models. All forcing-function dimensions apply: success criteria, retraining triggers, calibration discipline, model artifact version control, deployment gating.

### § 3.3 Non-Trained Models — N/A Handling (3 entities)
M-6, M-7 are arithmetic overlays. M-10 is non-trained statistical (Beta-Binomial Bayesian computation). For these models:
- **Success criteria:** APPLIES — even non-trained models have per-output success criteria (e.g., M-6 EV-flag accuracy, M-10 angle-stat-coverage adequacy).
- **Retraining triggers:** N/A for M-6, M-7 (arithmetic — no training cycle). N/A for M-10 (Bayesian posterior auto-updates from upstream `angle_stats` aggregations refresh — no per-model retrain). Each N/A cell carries explicit narrative explaining the non-applicability with substrate citation.
- **Calibration discipline:** APPLIES with caveats — M-10 is calibrated-by-construction (Bayesian posterior); M-6, M-7 do not have calibration in the ML sense, but have parameter discipline (Kelly fraction caps, edge thresholds).
- **Model artifact version control:** APPLIES with caveats — M-6, M-7 have no model_versions registry row; their "version" is the source-code version. M-10 has no registry row; its "version" is the source-code version of `model/angles/scorer.py` plus the `angle_stats` aggregation refresh state.
- **Deployment gating:** APPLIES uniformly — every model has deployment gating (the inference Lambda warm-start path that loads or invokes the model).

### § 3.4 Out of Scope
- Models considered but not deployed to production inference (per MLA Q6 ratification).
- Deprecated/superseded model artifact versions (this bible documents version control discipline, but the version history archaeology of deprecated artifacts is itself a Phase 5 disposition concern — not the version-control discipline itself).
- Per-feature monitoring substrate (per Q11 ratification, FP is canonical home; MER cross-references via `fp:F-N` in narrative).

---

## § 4. SUBSTRATE READ AUTHORIZATION (PER PHASE A Q7 PATTERN)

Drafting CC is authorized to read the following EE codebase substrate domains. Discovery via `list_directory` and `search_files` from EE project root. QB does NOT pre-enumerate paths.

| Domain | Authorized | Notes |
|--------|------------|-------|
| A. Locked Phase 1 bibles | YES | Per § 2.2 inheritance bundle |
| A'. Phase A v1-draft bibles | YES | Per § 2.3 (FP + MLA v1-drafts; NOT locked) |
| B. Feature engineering source code | YES | Discovery via list_directory / search_files (for FP cross-references in narrative) |
| C. Model definition source code | YES | For per-model substrate verification |
| D. Training pipeline scripts | YES | **PRIMARY substrate for retraining-trigger taxonomy discovery (Q12)** |
| E. Inference pipeline scripts | YES | For deployment-gating substrate |
| F. Model artifact metadata | YES | For model artifact version control substrate |
| G. Configuration files | YES | EventBridge schedules, deployment configs |
| H. Live database read | NO | Deferred to credential-authorized cycle |

Drafting CC inventories all paths read in Verification Log § 7.2. Domain D + Domain G are emphasized for retraining-trigger taxonomy discovery per Q12 ratification — substrate-grounded taxonomy with code-line citations is mandatory.

---

## § 5. PER-MODEL ROW SCHEMA

Each model in scope receives one row in § 4.1 of the bible. Row columns:

### § 5.1 M-ID
Inherited from MLA v1-draft. Format: `M-N` where N is 1 through 11. No new IDs introduced; no reuse on deletion.

### § 5.2 Model Name
Verbatim match to MLA v1-draft § 5.2 model name. Cross-reference: `mla:M-N`. No re-authoring of model identifier.

### § 5.3 Success Criteria
Substrate-grounded operational success criteria for the model. Includes:
- **Primary metric** with code-line citation to where it is computed (e.g., backtest script, evaluation harness, monitoring dashboard).
- **Threshold** with substrate citation (e.g., `BACKTEST_BRIER_THRESHOLD = 0.18` at `model/<family>/eval.py:N`).
- **Pass/fail discipline** — what happens when threshold is missed (block deployment, raise alert, log only).

For non-trained models per § 3.3: still applies. M-6 success criterion might be "EV-flag accuracy as measured by `<eval-script>:N`"; M-10 success criterion might be "angle-stat-coverage threshold as measured by `<aggregation-script>:N`".

If substrate does not surface explicit success criteria for a given model, the cell resolves to UNVERIFIED with narrative explaining what substrate would resolve.

### § 5.4 Retraining Triggers
Per Q12 ratification: drafting CC discovers taxonomy from substrate. Cell content includes:
- **Trigger taxonomy entries operative for this model** (e.g., cadence-based: "weekly via EventBridge rule X at `<config>:N`"; drift-based: "feature-distribution-drift threshold Y on feature `fp:F-Z` at `<monitor-script>:N`"; performance-based: "Brier score degradation threshold W at `<eval-script>:N`").
- **Each entry substrate-grounded** with code-line citation OR EventBridge rule name OR config-file declaration.
- **Cross-references to FP** via `fp:F-N` for any feature-distribution-drift triggers per Q11.

For non-trained models per § 3.3: cell resolves to N/A with narrative. M-6, M-7 N/A narrative: "arithmetic — no training cycle". M-10 N/A narrative: "Bayesian posterior auto-updates from upstream angle_stats aggregation refresh per data_pipeline_bible:4.1.7".

If the substrate-discovered taxonomy reveals operational ML discipline gaps (e.g., only cadence-based triggers operative, no drift-monitoring or performance-gating) per Tony Q12 ratification, surface as PHASE_5_BACKLOG_CANDIDATE in narrative per standing instruction.

### § 5.5 Calibration Discipline
Per Q13 ratification: lifetime/operational calibration discipline + architectural-calibration-finding dimension. Cell content includes:
- **Lifetime discipline:** validation cadence, sidecar refresh schedule, monitoring discipline. With code-line citations.
- **Architectural finding dimension:** if MLA § 5.9 calibration state for this model is BYPASS or UNCALIBRATED, MER documents the architectural debt with substrate citation. Cross-references the MLA finding via `mla:M-N` plus MLA § 5.9 / § 5.10 citations.
- **PHASE_5_BACKLOG_CANDIDATE entries:** the calibration discipline candidate group consolidates here. Per Tony Q13 ratification, this is the canonical documentation home for the calibration debt PHASE_5 candidate group (wp_core dead-load + wp_full dead-load + WR styles + post-2026-05-01 ranker-as-probability flip implications).

For non-trained models per § 3.3: M-10 narrative explicitly: "calibrated-by-construction (Bayesian posterior is calibrated by construction)". M-6, M-7 narrative explicitly: "no calibration in ML sense; parameter discipline (Kelly fraction caps, edge thresholds) substituted; documented in § 5.6 Notes".

### § 5.6 Model Artifact Version Control
Substrate-grounded version control discipline for the model artifact. Includes:
- **Version naming convention** (e.g., `<family>_<style>_<timestamp>` per `model/<family>/save_artifact.py:N`).
- **Storage location** (e.g., `s3://equine-model-artifacts/<family>/<filename>` per `architecture_overview:3.4`).
- **model_versions registry interaction** (e.g., new artifact registered with `is_active=true` per `<deploy-script>:N`; old artifact `is_active=false` retained per retention policy at `<config>:N`). Cross-references `database_schema_bible:4.1.11` for `model_versions` table schema.
- **Active-row selection discipline** — how is the active artifact selected at warm-start. Cross-references known issue (88-row registry with 45 simultaneously active under non-deterministic LIMIT 1 — pre-known PHASE_5 candidate per QB-known list).

For non-trained models per § 3.3: M-6, M-7 narrative: "no model_versions registry row; version = source-code version; deployment via Lambda code update". M-10 narrative: "no model_versions registry row; version = source-code version of `model/angles/scorer.py` plus `angle_stats` aggregation refresh state per data_pipeline_bible:4.1.7".

### § 5.7 Deployment Gating
Substrate-grounded deployment-gate discipline. Includes:
- **Pre-deployment checks** (e.g., backtest threshold, smoke test, schema validation). With code-line citations to gate scripts.
- **Deployment mechanism** (e.g., S3 artifact upload + Lambda warm-start refresh + model_versions registry update). With substrate citations.
- **Rollback discipline** (e.g., `is_active` flag flip + Lambda redeploy + S3 retention).
- **Post-deployment monitoring** (e.g., live-prediction sanity checks at `<monitor-script>:N`).

Applies uniformly to all 11 models per § 3.3 (even non-trained models have deployment gating via the inference Lambda warm-start path).

### § 5.8 Calibration Discipline Narrative
**REQUIRED** free-form note for any model with non-trivial calibration discipline (CALIBRATED, BYPASS) per MLA cross-reference. Captures:
- Specific operational cadence with substrate.
- Architectural finding with cross-reference to MLA composition-time state.
- PHASE_5_BACKLOG_CANDIDATE entries inline-flagged per standing instruction.

For models with calibration N/A per § 3.3: brief narrative explaining N/A with substrate.

### § 5.9 Quaternary Status (UNVERIFIED handling)
Each forcing-function column (§ 5.3 through § 5.7) may resolve to one of:
- **VERIFIED** — substrate-grounded with code-line citations.
- **PARTIAL** — partially substrate-grounded; gaps explicit.
- **UNVERIFIED** — substrate not concluded at row authorship; narrative explains.
- **N/A** — non-applicable per § 3.3 non-trained-model handling; narrative explains why.

Per Lesson § 4.11 prediction-precision discipline + Lesson § 4.X (banked) inheritance read-scope discipline + Lesson § 4.13 (banked) low-cost-substrate-verification-at-row-authorship: when substrate verification cost is low, execute at row-authorship. UNVERIFIED is honest substrate-grounded uncertainty; not deferred work.

### § 5.10 Notes
Optional column for hyperparameter snapshot, training-time vs inference-time architectural deltas, retention policy notes, or other Phase 5 disposition cues.

---

## § 6. REQUIRED BIBLE STRUCTURE

```
Model Evaluation & Retraining Bible
v1-draft / v1 / v1-patched-{a,b,c,...}
LOCKED <date> | DRAFT <date>

§ 1. Scope (Q10 11-row gallery mirror with N/A handling)
§ 2. Forcing Function (canonical statement per this spec § 1)
§ 3. Inheritance References (cross-refs to Phase 1 locks + Phase A v1-drafts)
§ 4. Per-Model Evaluation & Retraining Discipline
  § 4.1 Per-Model Rows (one row per gallery model, schema per spec § 5)
    § 4.1.1 M-1 ...
    § 4.1.2 M-2 ...
    ...
    § 4.1.11 M-11 ...
  § 4.2 Retraining Trigger Taxonomy (substrate-discovered per Q12)
    § 4.2.1 Cadence-based triggers (with EventBridge rule citations)
    § 4.2.2 Drift-based triggers (if substrate present)
    § 4.2.3 Performance-based triggers (if substrate present)
    § 4.2.4 Discipline gaps (PHASE_5_BACKLOG_CANDIDATEs)
§ 5. Calibration Discipline Findings Summary
  § 5.1 Lifetime calibration cadence + sidecar refresh discipline
  § 5.2 Architectural calibration debt findings (BYPASS dead-loads, UNCALIBRATED dispersal)
  § 5.3 Post-2026-05-01 ranker-as-probability flip architectural-calibration consolidation
§ 6. Model Artifact Version Control Findings Summary
  § 6.1 Active-row selection discipline (88-row registry with 45 active concern; LIMIT 1 non-determinism)
  § 6.2 Retention policy + deprecation lineage
§ 7. Deployment Gating Findings Summary
  § 7.1 Pre-deployment gate discipline
  § 7.2 Rollback discipline
  § 7.3 Post-deployment monitoring discipline
§ 8. Cross-Reference Index
  § 8.1 mer:M-N → mla:M-N matrix (1:1 inheritance)
  § 8.2 mer:E-N (evaluation criteria entities) and mer:T-N (retraining triggers) for cohort cross-references
  § 8.3 fp:F-N references in narrative columns
§ 9. Verification Log (per spec § 8)
```

Section numbering is fixed per this spec. Drafting CC may add subsections as needed but may not renumber or restructure top-level sections without QB authorization.

**Note on § 8 entity numbering:** per Q9 cross-reference convention, Bible 6 introduces `mer:E-N` (evaluation criteria) and `mer:T-N` (retraining triggers) entity-class IDs. These entities enable downstream Phase 5 cohort bibles to cross-reference Bible 6 entities. Drafting CC enumerates `E-N` and `T-N` IDs as encountered during § 4.1 row authorship and indexes in § 8.2.

---

## § 7. CROSS-REFERENCE CONVENTION (PER PHASE A Q9)

### § 7.1 Forward-Only Two-Tier Convention (Own Bible)
- Internal model-row references: `mer:M-N` (inherited 1:1 from MLA gallery).
- Internal evaluation-criterion references: `mer:E-N`.
- Internal retraining-trigger references: `mer:T-N`.
- Internal section references: `model_evaluation_retraining_bible:§ <section-number>`.

### § 7.2 Cross-Bible References (Cohort)
- To Feature Provenance: `fp:F-N` for feature entities; `feature_provenance_bible:§ <section>` for sections. Used in narrative columns per Q11.
- To ML Layer Architecture: `mla:M-N` for model entities; `ml_layer_architecture_bible:§ <section>` for sections.

### § 7.3 Backward-Compat to Phase 1 Locks
- Architecture Overview: `architecture_overview:§ <section>` (existing pattern).
- D&S Bible: `database_schema_bible:§ <section>` (existing pattern); `database_schema_bible:4.1.<table>` for per-table references.
- Data Pipeline Bible: `data_pipeline_bible:§ <section>` and `data_pipeline_bible:F.<flow-id>` (existing patterns).

---

## § 8. SYNCHRONIZATION POINT PROTOCOL (RATIFIED Q14)

Single-CC SP structure. Operationally analogous to Phase A SP-1/2/3 minus parallel-partner blocking. No partner CC; no blocking discipline; QB resolution is the sole synchronization mechanism.

### § 8.1 SP-A1 — TOC + § 1 Scope
- **Trigger:** Drafting CC has authored Table of Contents and § 1 Scope.
- **Pause action:** Drafting CC stops authoring further sections.
- **Emission to Tony:** Verbatim copy of TOC + § 1, plus self-summary stating: (a) section-numbering scheme used; (b) scope-boundary statement (11-row gallery mirror with N/A handling for non-trained models per Q10); (c) identifier conventions used for cross-references; (d) substrate-discovered retraining-trigger taxonomy preview (per Q12 — what taxonomy categories did substrate surface).
- **Wait condition:** Drafting CC waits for one of {CONTINUE, REVISE} from QB (via Tony).
- **Resume:** On CONTINUE or after revision satisfying QB findings.

### § 8.2 SP-A2 — § 4.1 First 3 Per-Model Rows
- **Trigger:** Drafting CC has authored § 2 (Forcing Function), § 3 (Inheritance References), structural shell of § 4 (per-model discipline section), then the first three per-model rows § 4.1.1 (M-1), § 4.1.2 (M-2), § 4.1.3 (M-3) per schema § 5.
- **Pause action:** Drafting CC stops authoring further rows.
- **Emission to Tony:** Verbatim copy of § 4.1.1, § 4.1.2, § 4.1.3 (full row content per schema § 5), plus self-summary stating: (a) success-criteria substrate citations encountered; (b) retraining-trigger taxonomy entries used for the three rows with substrate citations; (c) calibration discipline cross-references emitted (`mla:M-N` references for architectural findings); (d) any PHASE_5_BACKLOG_CANDIDATE entries inline-flagged.
- **Wait condition:** Drafting CC waits for one of {CONTINUE, REVISE} from QB (via Tony).
- **Resume:** On CONTINUE or after revision satisfying QB findings.

QB-side SP-A2 review specifically verifies:
- Cross-references to MLA M-N forcing functions (composition-time facts) are accurate against MLA v1-draft § 4.1 content.
- Cross-references to FP F-N feature provenance (where present in narrative) align with FP v1-draft § 4.1 content.
- Retraining-trigger taxonomy substrate-grounding with code-line citations.

### § 8.3 SP-A3 — Pre-Corpus-Audit Gate
- **Trigger:** Drafting CC has completed full v1-draft (all sections § 1 through § 9 present, verification log emitted).
- **Pause action:** Drafting CC stops; v1-draft is final.
- **Emission to Tony:** Full v1-draft path on disk, byte count, line count, count of models (M-N count = 11), count of trained vs N/A models, retraining-trigger taxonomy categories surfaced, calibration discipline architectural findings consolidated, count of FAIL/PARTIAL self-audit checks, count of NEW PHASE_5_BACKLOG_CANDIDATE entries surfaced.
- **Wait condition:** Drafting CC awaits SP-A3 disposition. Disposition is AUTHORIZE-CORPUS-AUDIT (Q14 ratification). On AUTHORIZE-CORPUS-AUDIT, Phase B is COMPLETE; corpus audit gate (Q2) initiates with all three v1-drafts (FP, MLA, MER) reading together.
- **Session ends after SP-A3 emission.**

### § 8.4 Discipline
- SP-A1, SP-A2 are NOT blocking on a parallel partner (single-CC drafting). QB resolution is the sole synchronization.
- Drafting CC must NOT modify locked Phase 1 bibles. Findings about locked substrate go in narrative notes flagged for QB UPSTREAM-CORRECTION evaluation per Handoff § 7.
- Drafting CC must NOT modify Phase A v1-drafts. Findings about FP or MLA v1-draft substrate go in narrative notes flagged for QB triage; corpus-audit-gate is the appropriate venue for Phase A v1-draft adjustments per Handoff § 5 / § 6.

---

## § 9. VERIFICATION LOG

Drafting CC emits a Verification Log as § 9 of the bible. Required content:

1. **Inheritance read inventory** — every file from § 2 read, with byte count and read scope (full / TOC + targeted-sections / load-bearing-sections-only). Per Lesson § 4.X (banked): TOC + targeted-section reads on Phase 0 locks suffices when load-bearing content is consulted.
2. **Substrate path inventory** — every code path read under § 4 authorization, with file path, line ranges accessed, purpose. Domain D + Domain G emphasized for retraining-trigger taxonomy substrate.
3. **Self-audit checklist** — § 10 nine-check list with PASS / FAIL / PARTIAL state and rationale per check.
4. **Retraining-trigger taxonomy substrate-grounding inventory** — every taxonomy category surfaced (cadence / drift / performance / other) with code-line citations to substrate.
5. **Calibration discipline architectural-finding consolidation** — the calibration debt PHASE_5_BACKLOG candidate group (wp_core dead-load + wp_full dead-load + WR styles + post-2026-05-01 ranker-as-probability flip) consolidated as canonical Bible 6 finding per Q13 ratification.
6. **Cross-reference inventory** — every `mla:M-N` and `fp:F-N` reference emitted, indexed for corpus-audit verification.
7. **Findings flagged for UPSTREAM-CORRECTION evaluation** — substrate inconsistencies discovered against locked Phase 1 bibles OR against Phase A v1-drafts. Drafting CC does NOT author UPSTREAM-CORRECTION patches.
8. **Roster reconciliation against MLA v1-draft § 4.1** — confirmation that 11-row gallery matches MLA's ratified roster; any discrepancy flagged.

---

## § 10. SELF-AUDIT — 9 CHECKS ACROSS 3 CLUSTERS

Drafting CC executes these checks before SP-A3 emission. Results recorded in Verification Log § 9.3.

### Cluster I — Substrate Verification
1. **Inheritance bundle complete** — all 12 items in § 2 read at session start (Phase 0 locks may be TOC + targeted-section reads per Lesson § 4.X banked; Phase 1 locks + Phase A v1-drafts require full or load-bearing-section reads).
2. **Authorized substrate read** — domains A, A', B, C, D, E, F, G per § 4 read; H not attempted.
3. **Convention identifiers verified at primary source** — model artifact names, EventBridge rule names, success-criteria thresholds, calibration sidecar paths, file paths verified at primary source at row-authorship time (Lesson 3 expansion).

### Cluster II — Content Verification
4. **Forcing function fully served** — every per-model row has all forcing-function columns populated (success criteria / retraining triggers / calibration discipline / version control / deployment gating); zero empty cells without UNVERIFIED or N/A treatment per § 5.9.
5. **Internal consistency** — every mer:M-N corresponds 1:1 to MLA M-N; every mer:E-N referenced internally exists in § 4.1 narrative or § 4.2 taxonomy; every mer:T-N referenced internally exists in § 4.2 taxonomy; every mla:M-N reference is recorded in § 8.1 cross-reference index; every fp:F-N reference is recorded in § 8.3.
6. **Verification claims supported by code-line citations** — every success-criteria threshold, every retraining-trigger taxonomy entry, every calibration sidecar reference has substrate citation per Lesson § 4.11 prediction-precision + Lesson § 4.13 (banked).

### Cluster III — Workflow Verification
7. **SP-A1 and SP-A2 emissions executed with required artifacts** — both pause-emit-resume cycles completed; Verification Log records SP findings received and applied.
8. **Cross-reference convention applied per Q9 / Phase A precedent** — own-bible references use `mer:M-N` / `mer:E-N` / `mer:T-N`; cohort cross-refs use `fp:F-N` / `mla:M-N`; Phase 1 lock cross-refs use existing conventions.
9. **Verification log emitted at v1-draft completion** — § 9 of bible is populated and complete before SP-A3 emission.

Any FAIL or PARTIAL state must be reported to Tony in SP-A3 emission with explanation.

---

## § 11. WRITE DISCIPLINE

Drafting CC writes:
- The bible itself at output path.
- Verification Log as § 9 of the bible.

Drafting CC does NOT write to disk:
- Any locked Phase 1 bible (Architecture Overview, D&S, Data Pipeline).
- Any Phase A v1-draft bible (FP, MLA — even though they're not yet locked).
- Any meta document outside the assigned output.
- Any spec / handoff / audit document.

Per Handoff § 11 and Lesson § 4.12: write authorization bounded to the single output path declared in this spec.

---

## § 12. PHASE 5 BACKLOG CANDIDATE HARVESTING (PER STANDING INSTRUCTION)

Drafting CC surfaces PHASE_5_BACKLOG_CANDIDATE entries inline in row narratives per the standing instruction operative for this cohort. Format per TRIAGE_QUEUE_SPEC v1:
- Severity (HIGH / MEDIUM / LOW)
- Dependencies (any cross-bible cross-references)
- Disposition vocabulary: one of {keep, refactor, replace, kill, autonomous, monitored, scheduled-manual, paid-replacement}
- Brief rationale with code-line citation

Format inline:
```
PHASE_5_BACKLOG_CANDIDATE: severity=<X>; disposition=<Y>; rationale="<brief>"; cite=file:line
```

**Pre-known PHASE_5 candidates this bible CONSOLIDATES rather than re-authors** (per Q13 ratification — Bible 6 is canonical home for calibration discipline candidate group):
- Calibration bypass all WR styles at wr_inference_service.py:616-626
- wp_core dead-load calibration sidecar (lean53 only) at wr_inference_service.py:171-178 + 326-335
- wp_full dead-load calibration sidecar (all 8 styles unconditional) at wr_inference_service.py:205-212 + 326-335
- Post-2026-05-01 ranker-as-probability architectural flip implications

These four are the consolidated calibration discipline candidate group. Bible 6 § 5 documents them as the canonical finding; QB lock-time batch synthesis to PHASE_5_BACKLOG.md applies dedup + consolidation accordingly.

**Pre-known PHASE_5 candidates that may surface in MER-specific scope:**
- 88-row model_versions registry with 45 simultaneously active under non-deterministic LIMIT 1 (selection discipline — surfaces at § 5.6 model artifact version control)
- M-8 RF zero-padded inference HIGH severity (surfaces at § 5.5 calibration discipline cross-reference + § 5.10 narrative — Tony pre-Phase-5 visibility flag stands)

**MER-specific NEW candidate categories drafting CC may surface:**
- Operational ML discipline gaps (per Q12 ratification: if substrate reveals only cadence-based triggers with no drift/performance gating, surface as PHASE_5_BACKLOG_CANDIDATE)
- Deployment-gating gaps (e.g., absent rollback discipline, absent post-deployment monitoring)
- Version control gaps (e.g., no `is_active` flip discipline at deploy time)

---

**END DRAFTING SPEC — MODEL EVALUATION & RETRAINING BIBLE**
