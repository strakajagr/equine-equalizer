# QB DRAFTING SPEC — ML LAYER ARCHITECTURE BIBLE (PHASE 1 DELIVERABLE 5)

**Cohort:** Phase 1 Deliverables 4-5-6 (Parallel Cohort)
**Bible Number:** 5
**Bible Short:** mla
**Output Path:** `/home/strakajagr/projects/equine-equalizer/docs/bible/ml_layer_architecture_bible.md`
**Output Version:** v1-draft (pre-audit), v1 (post-audit lock)
**Parallel Partner:** Feature Provenance Bible (Bible 4, fp)
**Sequential Downstream:** Model Evaluation & Retraining Bible (Bible 6, mer)

---

## § 1. FORCING FUNCTION (CANONICAL)

For every model in the EE production model gallery, the bible must answer:

> **type (XGB / LSTM / Bayesian / RF / ensemble / etc.) → inputs → outputs → position in inference pipeline → target latent → output composition → calibration / bypass state**

Every dimension of this forcing function must appear as a column in the per-model row schema (§ 5). No dimension may be omitted. No row may have an empty cell in a forcing-function column without explicit UNVERIFIED treatment per § 5.

---

## § 2. INHERITANCE BUNDLE — READ AT SESSION START

Identical to Bible 4 spec § 2. Read at session start before any draft authorship.

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

## § 3. SCOPE (RATIFIED Q6)

Production-deployed only.

### § 3.1 Production-Deployed Scope
A model is in scope if and only if it currently serves inference in the EE production stack. The production model gallery includes (subject to drafting CC verification at primary source):
- XGBoost win-probability model(s) (dual model architecture noted in inheritance)
- Pairwise ranker
- Arithmetic value overlay
- Random Forest longshot classifier
- LSTM form trajectory model
- Beta-Binomial Bayesian angle scorer
- Logistic regression stacking ensemble

Drafting CC verifies the gallery roster against substrate (model artifact metadata, inference pipeline scripts, deployment configs per § 4) at session start. Discrepancies between this enumeration and substrate are flagged in Verification Log § 9.6 for QB triage — drafting CC does NOT unilaterally add or remove models from the gallery.

### § 3.2 Out of Scope
- Experimental models not deployed to production inference.
- Deprecated / superseded model versions (these belong in Bible 6 model artifact version control, not MLA).
- Models considered but not implemented.

### § 3.3 Asymmetry With Bible 4 (Q5/Q6)
Bible 4 inventories orphan features (debt visible to Phase 5 ML re-architecture). Bible 5 does NOT inventory deprecated models — version history and supersession lineage are model artifact concerns, scoped to Bible 6 (Model Evaluation & Retraining). This asymmetry is by design per Q6 ratification.

---

## § 4. SUBSTRATE READ AUTHORIZATION (RATIFIED Q7)

Identical to Bible 4 spec § 4. Domains A–G authorized; H deferred. Discovery via `list_directory` and `search_files`. Path inventory in Verification Log § 9.2.

---

## § 5. PER-MODEL ROW SCHEMA

Each model in scope receives one row in § 4.1 of the bible. Row columns:

### § 5.1 M-ID
Monotonic integer, prefix `M-` (e.g., `M-1`, `M-2`, `M-7`). Stable across the bible. No reuse on deletion.

### § 5.2 Model Name
Canonical identifier matching the name used in code (class name, model artifact name, or deployment identifier). Verbatim match required. If multiple identifiers exist for the same model across substrate (class name vs deployment name), all are listed with primary identifier flagged.

### § 5.3 Model Type
One of: `XGBoost` | `Random Forest` | `LSTM` | `Bayesian (Beta-Binomial)` | `Bayesian (other — specify)` | `Logistic Regression` | `Pairwise Ranker (specify algorithm)` | `Arithmetic Overlay (non-ML)` | `Ensemble (specify composition)` | `Other (specify)`. Drafting CC verifies type at primary source (model class definition or training script).

### § 5.4 Inputs
List of `fp:F-N` references for every feature this model consumes. Drafting CC produces this list provisionally (forward stubs) before SP-2; SP-2 reconciles with FP § 4.1 for bidirectional consistency. Inputs include both raw features and any intermediate latents from upstream models in the stack.

### § 5.5 Outputs
Output schema. What does this model produce? Examples: scalar probability ∈ [0,1], rank score, log-odds, vector of class probabilities, latent embedding vector (specify dimensionality). Each output dimension explicitly typed.

### § 5.6 Position in Inference Pipeline
Where this model sits in the 7-layer ML stack. Specify upstream models (whose outputs this model consumes) and downstream models (which models consume this model's outputs). Format: `Upstream: [M-X, M-Y]; Downstream: [M-Z]; Inference layer: <layer-name>`. Layer name discovered from inference pipeline scripts.

### § 5.7 Target Latent
The latent variable this model models or contributes to. Vocabulary shared with Bible 4 § 5.6 — reconciled at SP-2. Examples: `win_probability`, `form_trajectory`, `longshot_signal`, `pairwise_rank_score`, `final_value_score`. Before SP-2: provisional vocabulary marked `[PROVISIONAL]`.

### § 5.8 Output Composition
How this model's outputs combine with other models' outputs in the inference pipeline. For ensembles: composition rule (weighted average, stacking, voting, etc.) with explicit weights / hyperparameters where applicable. For non-ensemble models whose outputs are directly consumed downstream: pass-through note. For terminal models (final output to user / decision): `terminal — see § 5.6 downstream = []`.

### § 5.9 Calibration State
One of: `CALIBRATED (specify method)` | `UNCALIBRATED` | `BYPASS (specify condition)` | `UNVERIFIED`.
- CALIBRATED: model outputs are calibrated probabilities or scores. Specify calibration method (Platt scaling, isotonic regression, Bayesian posterior, etc.) and code-line citation.
- UNCALIBRATED: outputs are raw model scores not transformed to calibrated probabilities. Code-line citation for inference path showing absence of calibration.
- BYPASS: model is conditionally bypassed in inference (e.g., "bypassed when confidence < threshold X"). Specify bypass condition with code-line citation.
- UNVERIFIED: drafting CC cannot conclude from substrate. Honest uncertainty.

### § 5.10 Bypass State Narrative
**REQUIRED** free-form note for any model with BYPASS in § 5.9, OR any model with conditional inference behavior. Specify trigger condition, fallback behavior, and code-line citations. For non-bypass models: `N/A — always invoked in inference`.

### § 5.11 Notes
Optional column for hyperparameter snapshot, training-time vs inference-time architectural deltas, or other Phase 5 disposition cues.

---

## § 6. REQUIRED BIBLE STRUCTURE
ML Layer Architecture Bible
v1-draft / v1 / v1-patched-{a,b,c,...}
LOCKED <date> | DRAFT <date>
§ 1. Scope (Q6 production-deployed only)
§ 2. Forcing Function (canonical statement per this spec § 1)
§ 3. Inheritance References (cross-refs to Phase 1 locks per Q9)
§ 4. Model Gallery
§ 4.1 Per-Model Rows (one row per production model, schema per spec § 5)
§ 4.1.1 M-1 ...
§ 4.1.2 M-2 ...
...
§ 4.2 Inference Pipeline Topology
§ 4.2.1 Layer enumeration (the 7-layer stack at canonical resolution)
§ 4.2.2 Cross-model dataflow diagram (textual; upstream→downstream graph)
§ 5. Calibration Findings Summary
§ 5.1 CALIBRATED count + index (with method per row)
§ 5.2 UNCALIBRATED count + index (FLAG: calibration debt candidates)
§ 5.3 BYPASS count + index (with condition per row)
§ 5.4 UNVERIFIED count + index
§ 6. Cross-Reference Index
§ 6.1 mla:M-N → fp:F-N matrix (forward, populated post-SP-2)
§ 6.2 fp:F-N → mla:M-N matrix (reverse — provisional, validated at corpus audit)
§ 7. Verification Log (per spec § 9)

Section numbering is fixed per this spec.

---

## § 7. CROSS-REFERENCE CONVENTION (RATIFIED Q9)

### § 7.1 Forward-Only Two-Tier Convention (Own Bible)
- Internal model references: `mla:M-N`
- Internal section references: `ml_layer_architecture_bible:§ <section-number>`

### § 7.2 Cross-Bible References (Cohort)
- To Feature Provenance: `fp:F-N` for feature entities; `feature_provenance_bible:§ <section>` for sections.
- To Model Evaluation & Retraining: `mer:E-N` for evaluation criteria; `mer:T-N` for retraining triggers; `model_evaluation_retraining_bible:§ <section>` for sections.

### § 7.3 Backward-Compat to Phase 1 Locks
Identical to Bible 4 spec § 7.3. Existing conventions of locked bibles preserved.

---

## § 8. SYNCHRONIZATION POINT PROTOCOL

Per Handoff § 4. Drafting CC PAUSES at SP-1 and SP-2, EMITS specified artifacts, RESUMES only on QB authorization (mediated by Tony).

### § 8.1 SP-1 — TOC + § 1 Scope
- **Trigger:** Drafting CC has authored the bible's Table of Contents and § 1 Scope.
- **Pause action:** Drafting CC stops authoring further sections.
- **Emission to Tony:** Verbatim copy of TOC + § 1, plus a brief self-summary stating: "(a) section-numbering scheme used, (b) scope-boundary statement, (c) identifier conventions used for cross-references, (d) production-deployed gallery roster discovered at substrate."
- **Wait condition:** Drafting CC waits for one of {CONTINUE, REVISE-FP, REVISE-MLA, REVISE-BOTH} from QB (via Tony).
- **Resume:** On CONTINUE or after revision satisfying QB findings.

### § 8.2 SP-2 — § 4.1 First Three Entities
- **Trigger:** Drafting CC has authored § 4.1 (Per-Model Rows) covering at least the first three models.
- **Pause action:** Drafting CC stops authoring further models.
- **Emission to Tony:** Verbatim copy of § 4.1.1, § 4.1.2, § 4.1.3 (full row content per schema § 5), plus a brief self-summary stating: "(a) target latent vocabulary used, (b) calibration state distribution across the three rows, (c) inputs references emitted (`fp:F-N` list)."
- **Wait condition:** Drafting CC waits for one of {CONTINUE, REVISE-FP, REVISE-MLA, REVISE-BOTH} from QB (via Tony).
- **Resume:** On CONTINUE or after revision satisfying QB findings.

### § 8.3 SP-3 — Pre-Model-Evaluation Gate
- **Trigger:** Drafting CC has completed full v1-draft (all sections § 1 through § 7 present, verification log emitted).
- **Pause action:** Drafting CC stops; v1-draft is final from this CC's perspective.
- **Emission to Tony:** Full v1-draft path on disk, byte count, line count, verification log per § 9.
- **Wait condition:** SP-3 disposition. Phase B (Bible 6) is gated on QB authorization, not on this drafting CC. Session ends after SP-3 emission.

### § 8.4 Discipline
Identical to Bible 4 spec § 8.4. SP-1 / SP-2 blocking; no speculation about parallel partner; no modification to locked Phase 1 substrate.

---

## § 9. VERIFICATION LOG

Drafting CC emits a Verification Log as § 7 of the bible. Required content:

1. **Inheritance read inventory** — every file from § 2 read, byte count, read timestamp.
2. **Substrate path inventory** — every code path read under § 4 authorization, with file path, line ranges accessed, purpose.
3. **Self-audit checklist** — § 10 nine-check list with PASS / FAIL / PARTIAL state and rationale.
4. **Provisional latent vocabulary** — list of target_latent values used in § 4.1 with note flagging awaiting SP-2 reconciliation.
5. **Cross-reference forward-stub list** — every `fp:F-N` reference emitted in § 4.1.
6. **Findings flagged for UPSTREAM-CORRECTION evaluation** — substrate inconsistencies discovered against locked Phase 1 bibles, surfaced as raw observations for QB triage. Drafting CC does NOT author UPSTREAM-CORRECTION patches.
7. **Production gallery roster reconciliation** — comparison of spec § 3.1 enumerated roster vs substrate-discovered roster; discrepancies flagged.

---

## § 10. SELF-AUDIT — 9 CHECKS ACROSS 3 CLUSTERS

Drafting CC executes these checks before SP-3 emission. Results recorded in Verification Log § 9.3.

### Cluster I — Substrate Verification
1. **Inheritance bundle complete** — all 10 items in § 2 read at session start.
2. **Authorized substrate read** — domains A–G per § 4 read; H not attempted.
3. **Convention identifiers verified at primary source** — model class names, deployment identifiers, calibration method names, file paths verified at primary source at row-authorship time (Lesson 3 expansion).

### Cluster II — Content Verification
4. **Forcing function fully served** — every per-model row has all columns per schema § 5 populated; no empty forcing-function cells without UNVERIFIED treatment.
5. **Internal consistency** — every mla:M-N referenced internally exists in § 4.1; § 4.2 inference pipeline topology consistent with per-row § 5.6 declarations; every fp:F-N reference recorded in § 6.1 forward index.
6. **Verification claims supported by code-line citations** — every CALIBRATED / BYPASS status in § 5.9 has explicit code-line citations; type declarations in § 5.3 cited at model class definition (Lesson § 4.11 prediction-precision).

### Cluster III — Workflow Verification
7. **SP-1 and SP-2 emissions executed with required artifacts** — both pause-emit-resume cycles completed; Verification Log records SP findings received.
8. **Cross-reference convention applied per Q9** — own-bible references use `mla:M-N` / `ml_layer_architecture_bible:§ N`; cohort cross-refs use `fp:F-N` / `mer:E-N`-`mer:T-N`; Phase 1 lock cross-refs use existing conventions of locked bibles.
9. **Verification log emitted at v1-draft completion** — § 7 of bible is populated and complete before SP-3 emission.

Any FAIL or PARTIAL state must be reported to Tony in SP-3 emission with explanation.

---

## § 11. WRITE DISCIPLINE

Drafting CC writes:
- The bible itself at output path.
- Verification Log as § 7 of the bible.

Drafting CC does NOT write to disk:
- Any locked Phase 1 bible.
- Any meta document outside the assigned output.
- Any spec / handoff / audit document.
- Bible 4 (Feature Provenance) — that is the parallel partner CC's scope.

Per Handoff § 11 and Lesson § 4.12: write authorization bounded to the single output path declared in this spec.

---

**END DRAFTING SPEC — ML LAYER ARCHITECTURE BIBLE**
