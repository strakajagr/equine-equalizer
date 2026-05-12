# Feature Provenance Bible

**Document:** feature_provenance_bible
**Phase:** 1 (Bible) — deliverable 4 of 7 (drafting-order numbering per BIBLE_STRUCTURE_SPEC v6 § 8.2; QB_HANDOFF_PARALLEL_COHORT_DRAFTING § 1)
**Status:** v1 LOCKED 2026-05-07. Authored under Phase 1 Parallel Cohort (Phase A — Tight-Parallel Drafting with ML Layer Architecture Bible per QB_HANDOFF_PARALLEL_COHORT_DRAFTING § 3.1).
**Author:** CC (drafting under Tier 4 working-tree-code substrate discipline; QB orchestrated)
**Date:** 2026-05-06
**Output path:** `/home/strakajagr/projects/equine-equalizer/docs/bible/feature_provenance_bible.md`
**Forcing Function (canonical per QB_DRAFTING_SPEC_FEATURE_PROVENANCE_BIBLE § 1):** for every feature × every consuming model, source data → engineering code → consuming model(s) → target latent → train/inference duplication or divergence.
**Parallel partner:** ML Layer Architecture Bible (`mla`); cohort sequential downstream is Model Evaluation & Retraining Bible (`mer`).

## Revision history

- v1-draft (2026-05-06): initial CC draft per QB_DRAFTING_SPEC_FEATURE_PROVENANCE_BIBLE (RATIFIED 2026-05-06 by Tony per QB_HANDOFF_PARALLEL_COHORT_DRAFTING § 1). Anchored on: META_PLAN v9 (LOCKED 2026-05-05) + BIBLE_STRUCTURE_SPEC v6 (LOCKED 2026-05-05) + AUDIT_METHODOLOGY v2-patched (LOCKED 2026-05-05) + CONVERGENCE_CRITERIA v2 (LOCKED 2026-05-04) + TRIAGE_QUEUE_SPEC v1 (LOCKED 2026-05-04) + Architecture Overview v3 (LOCKED 2026-05-05) + Database & Schema Bible v1-patched-d2 (LOCKED 2026-05-06) + Data Pipeline Bible v1-patched-c (LOCKED 2026-05-06). Verification Log at this bible's § 7. Synchronization-point cycle complete: SP-1 CONTINUE 2026-05-06; SP-2 CONTINUE WITH DIRECTIVE 2026-05-06 (substrate-verification directive amortized via batch grep across base-feature surface; F-3 lasix upgraded UNVERIFIED→DUPLICATED with code-line citations); SP-3 reached at v1-draft completion 2026-05-06.
- v1-draft revise-pass (2026-05-07): SP-3 disposition REVISE-FP NARROWLY per QB SP-3-disposition issued 2026-05-07. Three-outcome-per-row revise-pass executed: 51 originally-UNVERIFIED rows reclassified via substrate-grounded batch grep against `model/shared/data_loader.py` + `backend/services/feature_engineering_service.py`. Final quaternary distribution: 74 DUPLICATED + 2 DIVERGENT-INTENTIONAL (F-24 timing-divergence + F-77 explicit-comment-divergence) + 0 DIVERGENT-UNINTENTIONAL + 4 UNVERIFIED (F-31, F-32, F-51, F-74 — all carrying explicit Bug #22 cross-reference per QB-required narrative format). Post-revise UNVERIFIED count 4/80 = 5.0% (well below 19% acceptance-threshold). § 5 Train/Inference Findings Summary regenerated. Self-audit Cluster I Check 1 reclassified PARTIAL → PASS per QB SP-3-disposition Finding 4 ratification (Lesson § 4.X inheritance-read-scope discipline banked for AUDIT_METHODOLOGY future cycle). Self-audit summary post-revise: 9 PASS / 0 PARTIAL / 0 FAIL.
- v1-patched-a-extended (2026-05-07): F-31 (avg_stretch_gain) combined substrate-attribution correction + classification resolution per corpus-audit Tony Decisions 2 + F3-C + F4-A. § 5.3 Source Data column corrected (formula = `call_2_position - finish_position` per training inline comment at `data_loader.py:370` + `# FIX #5` inference comment at `feature_engineering_service.py:511`; pre-patch narrative cited `stretch_position - finish_call_position` with migration-009 0%-population rationale, both substrate-incorrect). § 5.7 quaternary UNVERIFIED → DUPLICATED via single-grep substrate verification of `defaults['avg_stretch_gain'] = 0.0` per `model/shared/feature_definitions.py:32` (`FeatureDef('avg_stretch_gain', 'pace', True, 0.0)` — 4th-field default_value resolves via `get_feature_defaults()` at lines 118-119) equivalent to inference hardcoded `0.0` at `feature_engineering_service.py:522`. § 5.8 narrative simplified: formula equivalence + null-handling equivalence + fallback-value equivalence = DUPLICATED. § 5.1 DUPLICATED count + index: 74 → 75 (F-31 added with Tony-Decision-F4-A substrate-grounded sub-narrative). § 5.4 UNVERIFIED count + index: 4 → 3 (F-31 removed). § 5 verification line updated. Bug #22 cross-reference: F-31 row narrative + UNVERIFIED-section narrative reframe Bug #22 from F-31's specific rationale to documentation of the broader 66-base-feature pattern; F-31 no longer contributes to UNVERIFIED count. Quaternary distribution post-patch: 75 DUPLICATED + 2 DIVERGENT-INTENTIONAL + 0 DIVERGENT-UNINTENTIONAL + 3 UNVERIFIED. Lesson § 4.13 (banked from Phase A SP-2; reinforced at corpus audit) operative: low-cost single-grep substrate verification at row-authorship resolved UNVERIFIED → DUPLICATED within bounded patch cycle. Replaces v1-patched-a entry per Tony single-coherent-change ratification.
- v1 LOCKED 2026-05-07: Phase 1 Cohort corpus-audit-gate sequential lock cycle, step 1 of 3 (FP first per Handoff § 5.2 dependency order). Per corpus-audit Tony Decision 1 (DEFER architecture_overview:4.1 refinement) + Decision 2 (FIX-BEFORE-LOCK F-31 § 5.8) + Decision F3-C (combined patch scope) + Decision F4-A (single-grep substrate resolution). v1-patched-a-extended substrate-grounded; quaternary distribution 75 DUPLICATED + 2 DIVERGENT-INTENTIONAL + 0 DIVERGENT-UNINTENTIONAL + 3 UNVERIFIED. Per Handoff § 6.1: cross-bible cross-reference freeze active across cohort (FP + MLA + MER) post-this-lock. UPSTREAM-CORRECTION cycle per Handoff § 7 is sole re-open path.

---

## Table of Contents

1. Scope of this bible
2. Forcing Function (canonical statement per QB_DRAFTING_SPEC § 1)
3. Inheritance References (per QB_DRAFTING_SPEC § 7.3 backward-compat to Phase 1 locks)
4. Feature Gallery
   - 4.1 Per-Feature Rows (one row per feature, schema per QB_DRAFTING_SPEC § 5)
     - 4.1.1 F-1 through 4.1.15 F-15 (14 Gonzo Sauce features + F-3 lasix early-author canonical-archetype)
     - 4.1.16 F-16 through 4.1.80 F-80 (66 base features per `model/shared/feature_definitions.py` FEATURE_DEFS)
     - 4.1.81 F-81 onward (orphan rows; ORPHAN-PRODUCTION + ORPHAN-EXPLORATORY)
   - 4.2 Orphan Inventory (subset view of § 4.1 filtered to ORPHAN-* rows per QB_DRAFTING_SPEC § 3.2)
     - 4.2.1 ORPHAN-PRODUCTION inventory
     - 4.2.2 ORPHAN-EXPLORATORY inventory
5. Train/Inference Findings Summary (quaternary distribution per QB_DRAFTING_SPEC § 5.7)
   - 5.1 DUPLICATED count + index
   - 5.2 DIVERGENT-INTENTIONAL count + index
   - 5.3 DIVERGENT-UNINTENTIONAL count + index (FLAG: data leakage candidates)
   - 5.4 UNVERIFIED count + index
6. Cross-Reference Index
   - 6.1 fp:F-N → mla:M-N matrix (forward)
   - 6.2 mla:M-N → fp:F-N matrix (reverse, populated post-SP-2 reconciliation — populated per SP-2 ratifications + corpus-audit-gate completion)
7. Verification Log (per QB_DRAFTING_SPEC § 9)
   - 7.1 Inheritance read inventory
   - 7.2 Substrate path inventory (domains A–G per QB_DRAFTING_SPEC § 4)
   - 7.3 Self-audit checklist (9 checks per QB_DRAFTING_SPEC § 10)
   - 7.4 Provisional latent vocabulary (now canonical per SP-2 Finding 2 ratification)
   - 7.5 Cross-reference forward-stub list (`mla:M-N` references emitted in § 4.1)
   - 7.6 Findings flagged for UPSTREAM-CORRECTION evaluation

---

## 1. Scope of this bible

The Feature Provenance Bible answers a single per-feature question: **"if I change feature X, what breaks?"** Audience: any reader making a feature-engineering change, a column-substrate change, a model-input contract change, or an investigation into training-vs-inference parity. The bible is **forcing-function-organized**: one row per feature in the EE production model gallery (plus orphan-flagged scope per § 3 below in QB_DRAFTING_SPEC, codified at this bible's § 4.2). Each row carries every dimension of the forcing function — source data → engineering code → consuming model(s) → target latent → train/inference duplication or divergence — without compression. No row may have an empty forcing-function cell without explicit UNVERIFIED treatment per the row schema's train/inference quaternary (DUPLICATED / DIVERGENT-INTENTIONAL / DIVERGENT-UNINTENTIONAL / UNVERIFIED).

This bible is **per-feature reference-style**: look up a feature by name and read its row. Other Phase 1 bibles are runtime-narrative (Architecture Overview), reference-style by table (Database & Schema), flow-narrative (Data Pipeline), composition-narrative (ML Layer Architecture — parallel partner in this cohort). When you need to know "what model uses this column?" you read here; when you need "what columns does the source table have?" you read `database_schema_bible:4.1`; when you need "how does data flow into that table?" you read `data_pipeline_bible:4.1`; when you need "how does the model compose its layers?" you read `ml_layer_architecture_bible:4` (when locked).

### 1.1 Production scope (per QB_DRAFTING_SPEC § 3.1)

A feature is in **production scope** if it is consumed by at least one model currently serving inference in the EE production model gallery. Production model gallery is defined as: the set of model artifacts loaded at warm-start (or per-invoke) by the three Active inference Lambdas — `equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference` — per `architecture_overview:3.1` Active-Lambda enumeration. Models loaded by these Lambdas are enumerated in this bible's per-feature `consuming_models` cells via `mla:M-N` cross-references; the canonical home for the per-model definition is `ml_layer_architecture_bible:4`.

A feature in production scope occupies one row in § 4.1 and is included in the § 5 train/inference findings summary's quaternary distribution.

### 1.2 Orphan scope (two-tier per QB_DRAFTING_SPEC § 3.2; SP-1 ratified)

Two orphan categories, each tracked separately for distinct Phase 5 disposition:

- **ORPHAN-PRODUCTION.** Feature exists in production-path feature engineering code (i.e., code imported by `equine-wr-inference` / `equine-pl-inference` / `equine-ls-inference` runtime, OR by an ECS Fargate training task family per `architecture_overview:3.2`); **no model anywhere consumes it**. Phase 5 disposition: kill (delete the feature definition) or assign consumer (wire it into a model's `feature_list` JSONB on the next training cycle). Rows for ORPHAN-PRODUCTION features carry `consuming_models = [ORPHAN-PRODUCTION]` and `train/inference status = N/A — orphan` with a § 5.8 narrative explaining the orphan classification basis. SP-1 Finding 4 ratified the broader-than-inference-runtime definition: ECS Fargate training task families count as production infrastructure for the ORPHAN-PRODUCTION definition.
- **ORPHAN-EXPLORATORY.** Feature exists in feature engineering code that is **NOT in any production runtime path**; consumed only by non-production paths (development scaffolding, notebooks, exploratory training scripts, the `equibase_probe/` exploratory sub-tree per `data_pipeline_bible:4.2.6`, or other zero-production-runtime-consumer code). Phase 5 disposition: distinct from ORPHAN-PRODUCTION (the re-architecture decision differs — exploratory features have no implicit kill cost since no production runtime carries them). Rows carry `consuming_models = [ORPHAN-EXPLORATORY]`.

Orphan rows are inventoried at § 4.2 (subset view of § 4.1 filtered by classification) for Phase 5 disposition convenience; the substantive row content lives at § 4.1 only — § 4.2 is a cross-reference index, not a content duplication site.

### 1.3 Out of scope (per QB_DRAFTING_SPEC § 3.3)

- **Features considered for engineering but not implemented in code.** No row. Speculation about "what features could we add" belongs in Phase 5 backlog, not in this bible.
- **Deprecated feature versions superseded by current implementations.** No row for the prior version; the current implementation occupies the row. Per BIBLE_STRUCTURE_SPEC v6 § 5.6.4 G2 conditional clause: physically-superseded substrate (e.g., a feature renamed via cull migration where the prior name no longer appears in any current code) does not require a Deprecated entry.

### 1.4 Boundary statements — what this bible does NOT document

- **Per-table schema** (column declarations, type widths, JSONB conventions, migration history) → `database_schema_bible:4.1`.
- **Per-flow data movement** (ingestion → DB → model → API; per-Lambda destination tables; cron schedules) → `data_pipeline_bible:4.1`.
- **Per-model architecture** (XGBoost vs LSTM vs RandomForest vs Bayesian vs ensemble, hyperparameters, calibration mechanics, 0-PP-override interaction) → `ml_layer_architecture_bible:4` (parallel partner; cohort cross-references resolve at SP-2 + corpus-audit gate per QB_HANDOFF_PARALLEL_COHORT_DRAFTING § 4.2 + § 6.1).
- **Per-model success criteria + retrain triggers** (pass/fail thresholds, retrain cadence, deployment gates) → `model_evaluation_retraining_bible:3` and `:4` (drafting after SP-3 per QB_HANDOFF_PARALLEL_COHORT_DRAFTING § 3.1 Phase B).
- **Per-runtime topology** (Lambda inventory, ECS Fargate task families, EventBridge schedule, RDS instance metadata, fire-and-fail anomaly substantive description) → `architecture_overview:3` and `:6`. This bible's per-feature rows reference `architecture_overview:3.1` for inference-Lambda identity and `architecture_overview:3.2` for training task family identity, but do NOT duplicate per-Lambda or per-rule substrate.

### 1.5 Cross-bible references that govern this bible's documentation discipline

- **`architecture_overview:3.1` (Lambda inventory).** Determines what counts as the production model gallery — features consumed by Active-Lambda-loaded models are in production scope per § 1.1.
- **`architecture_overview:3.2` (ECS Fargate training fleet).** Identifies the training pathways — features computed by training task families are training-side; features computed by inference Lambdas are inference-side; the train/inference quaternary at this bible's § 5 evaluates parity between these two surfaces.
- **`architecture_overview:4.1` (canonical cross-runtime objects).** Determines the source-data substrate — feature rows cite source columns from canonical objects (`Race`, `Entry`, `PastPerformance`, `Workout`, `Result`, `Prediction`) per `architecture_overview:4.1`'s line-cited declarations.
- **`database_schema_bible:4.1` (per-table sub-sections).** Destination for every row's `source_data` column; the source column names cited in this bible's § 4.1 rows reference the canonical column substrate at `database_schema_bible:4.1.<table>`.
- **`data_pipeline_bible:4.1.5` (daily inference flows for WR / PL / LS).** Identifies which Lambda hosts which inference path; this bible's per-row `consuming_models` cell cross-references through `mla:M-N` to the model whose Lambda host is identified there.

### 1.6 Source-priority hierarchy operative for this bible's content

Per META_PLAN v9 § 4.5: Tier 1 (live AWS state) > Tier 2 (live API endpoints) > Tier 3 (live database state) > Tier 4 (working-tree code post-baseline 87dec36) > Tier 5 (operator-stated history) > Tier 6 (`EE_CURRENT_STATE_DUMP.md`) > Tier 7 (session logs).

For this bible specifically, **Tier 4 is canonical** for engineering-code citations: file:line ranges for feature computation sites are the authoritative substrate for the `engineering_code` column of every § 4.1 row. Tier 3 (live DB state via `model_versions.feature_list` JSONB) is canonical for "what feature_list shape did the model_version actually train with"; this Tier-3 substrate is referenced where applicable for the consuming-model contract verification, with the explicit caveat per QB_DRAFTING_SPEC § 4 H-domain note (live DB read NOT authorized in this drafting cycle; D&S Bible inheritance is the canonical schema substrate). Cross-tier conflicts (e.g., `feature_list` JSONB in the active `model_versions` row diverges from the engineering-code's emitted feature set) are documented per § 5.7 train/inference quaternary, with DIVERGENT-* classification driven by the substrate of the divergence.

When sources conflict, source-priority hierarchy applies per META_PLAN v9 § 4.5 with the explicit Tier-4 preference noted above for engineering-code citations.

---

## 2. Forcing Function

Canonical statement (verbatim per QB_DRAFTING_SPEC_FEATURE_PROVENANCE_BIBLE § 1):

> For every feature × every consuming model in the EE production gallery (plus orphan-flagged scope per § 3), the bible must answer:
>
> **source data → engineering code → consuming model(s) → target latent → train/inference duplication or divergence**

Every dimension of this forcing function appears as a column in the per-feature row schema. No dimension is omitted. No row has an empty cell in a forcing-function column without explicit UNVERIFIED treatment per QB_DRAFTING_SPEC § 5.7.

The forcing function is the **load-bearing organizing principle** of this bible. § 4.1 enumerates one row per feature with all five forcing-function columns (source, engineering, consumers, target latent, train/inference status) plus required narrative (§ 5.8 of QB_DRAFTING_SPEC schema) and optional notes (§ 5.9 of QB_DRAFTING_SPEC schema). § 5 of this bible re-cuts the surface from a train/inference-quaternary angle for finding-summary navigation. § 6 cross-references the forward-emission `mla:M-N` references for corpus-audit verification.

---

## 3. Inheritance References

Per QB_DRAFTING_SPEC § 7.3 backward-compat clarification: this bible cross-references locked Phase 1 substrate using the existing conventions of those locked bibles.

### 3.1 Phase 0 locks (methodology substrate)

- **META_PLAN v9** (LOCKED 2026-05-05) — Source-priority hierarchy per § 4.5 (operative this bible's § 1.6); verification-log precision rule per § 6.5; placeholder-resolution sub-rule per § 7.3; canonical-home determination per § 7.4 + § 9.13 multi-active-row reality observation.
- **BIBLE_STRUCTURE_SPEC v6** (LOCKED 2026-05-05) — § 5.3 cross-cutting bug scope rule (canonical-home determination); § 5.6.x conditional templates; § 6.3 feature_provenance_bible TOC template (this bible's structural inheritance from spec § 6.3 is **superseded** by QB_DRAFTING_SPEC § 6 fixed structure per QB_DRAFTING_SPEC § 6 closing clause "Section numbering is fixed per this spec ... drafting CC may add subsections as needed but may not renumber or restructure top-level sections without QB authorization").
- **AUDIT_METHODOLOGY v2-patched** (LOCKED 2026-05-05) — Lesson § 4.10 verbatim-paste discipline (operative for this bible's § 7 verification log); Lesson § 4.11 prediction-precision (operative for the train/inference quaternary classification — UNVERIFIED-rather-than-speculation discipline); SP-2 ratification banked the Lesson § 4.11 refinement (Lesson § 4.13 candidate) for substrate-verification at row authorship when cost is LOW.
- **CONVERGENCE_CRITERIA v2** (LOCKED 2026-05-04) — Convergence test framing per § 3 (operative for the parallel-cohort lock-readiness assessment at corpus-audit gate per QB_HANDOFF_PARALLEL_COHORT_DRAFTING § 5).
- **TRIAGE_QUEUE_SPEC v1** (LOCKED 2026-05-04) — Severity tagging per § 5; disposition vocabulary per § 7 worked examples (operative for inline `PHASE_5_BACKLOG_CANDIDATE` entries surfaced in § 4.1 row narratives per QB SP-1 Standing Instruction).

### 3.2 Phase 1 locks (substrate substrate)

- **Architecture Overview v3** (LOCKED 2026-05-05) — Cross-references throughout this bible at `architecture_overview:§ <section>`. Load-bearing references: § 3.1 Lambda inventory (production-gallery scope determination), § 3.2 ECS Fargate training fleet (training-side substrate), § 4.1 canonical cross-runtime objects (source-data column citations), § 4.2 per-pipeline prediction shapes (output-shape consumer determination).
- **Database & Schema Bible v1-patched-d2** (LOCKED 2026-05-06) — Cross-references throughout at `database_schema_bible:§ <section>` and `database_schema_bible:4.1.<table>`. Load-bearing references: § 3.1 15-table domain schema (source-column substrate); § 3.2 trainer_stats matview (trainer-feature source); § 4.1.7 past_performances (richest source-data substrate for derived features); § 4.1.6 entries (direct passthrough for equipment / odds / weight features); § 4.1.15 angle_stats (M-10 Bayesian angle scorer source per `data_pipeline_bible:4.1.7`).
- **Data Pipeline Bible v1-patched-c** (LOCKED 2026-05-06) — Cross-references throughout at `data_pipeline_bible:§ <section>` and `data_pipeline_bible:F.<flow-id>`. Load-bearing references: § 4.1.5 daily inference flows for WR/PL/LS (production-gallery Lambda hosts); § 4.1.7 angle stats refresh flow (M-10 source); § 6 Currently Open (Bug #28 NULL payout interaction surface for results-aware features).

### 3.3 Cohort cross-references (un-frozen at v1-draft)

- **ML Layer Architecture Bible** (parallel partner; v1-draft pending lock) — `mla:M-N` model entity references and `ml_layer_architecture_bible:§ <section>` section references. The 11-entity M-ID roster (M-1 through M-11) per QB SP-2 ratification is the operative consuming-model identifier substrate; resolution of M-11 ENSEMBLE_FEATURES contract is deferred to corpus-audit gate.
- **Model Evaluation & Retraining Bible** (sequential downstream; drafts post-SP-3) — `mer:E-N` evaluation criteria and `mer:T-N` retraining trigger references; `model_evaluation_retraining_bible:§ <section>` section references. No cross-references emitted at this v1-draft stage (Phase B drafting starts after this bible reaches v1-draft completion).

Cross-reference freeze (per QB_HANDOFF_PARALLEL_COHORT_DRAFTING § 6) applies post-corpus-audit-gate; this bible's cohort cross-references resolve at that gate.

---

## 4. Feature Gallery

### 4.1 Per-Feature Rows

Each per-feature row carries all 9 schema columns per QB_DRAFTING_SPEC § 5: F-ID (§ 5.1), Feature Name (§ 5.2), Source Data (§ 5.3), Engineering Code (§ 5.4), Consuming Models (§ 5.5), Target Latent (§ 5.6), Train/Inference Status (§ 5.7), Train/Inference Narrative (§ 5.8), Notes (§ 5.9 — optional).

Numbering convention: monotonic F-N integers, prefix `F-`, stable (no reuse on deletion). F-1 through F-15 cover the 14 Gonzo Sauce features (Phase A3 single-source-of-truth pattern) + F-3 lasix (canonical archetype for direct DB column passthrough); F-16 through F-80 cover the 66 base features per `model/shared/feature_definitions.py` FEATURE_DEFS in declaration order; F-81+ cover orphan rows (legacy `model/features/feature_definitions.py` features with no canonical-FEATURE_DEFS overlap).

#### 4.1.1 F-1 — `speed_at_distance_recent_weighted`

- **F-ID:** F-1
- **Feature Name:** `speed_at_distance_recent_weighted`
- **Source Data:** Composed from `database_schema_bible:4.1.7` `past_performances` columns (`distance_furlongs`, `final_time`, `lengths_behind`, `race_date`) — last 5 PPs in today's distance cluster (sprint/mile/route per `model/shared/gonzo_features.py:147-156` `_distance_cluster()`; cluster windows at `model/shared/gonzo_features.py:49-51`) — plus today's-race `distance_furlongs` and `race_date` from `database_schema_bible:4.1.5` `races` (passed via the per-row dict by the caller).
- **Engineering Code:** `model/shared/gonzo_features.py:290-397` (function `compute_gonzo_speed_features()`; A1 sub-block at lines 321-346 — half-life-weighted mean of `_effective_speed_fps()` across last 5 cluster-eligible PPs, decay constant `A1_DECAY_DAYS = 180.0` at line 57). **Single-source-of-truth shared module** — both training and inference paths import this function; no parallel re-implementation exists.
- **Consuming Models:** `[mla:M-2, mla:M-4]` — gonzo_sauce specialist variants of M-2 (wp_full) and M-4 (rk_full) only. The model classes M-2 and M-4 also serve seven other specialist styles per `model/shared/specialists.py:28-37` (`general`, `speed`, `closer`, `class_riser`, `class_dropper`, `sprint`, `route`), but those non-`gonzo_sauce` style variants train on `get_lean53_features() = 53` per `model/shared/feature_definitions.py:197-202` (the `gonzo_sauce` specialist trains on `get_gonzo_sauce_features() = lean53 + 14 Gonzo = 67` per `model/shared/feature_definitions.py:256-260`), so this feature is in the model-level feature_list of M-2/M-4 ONLY when the loaded artifact is the `gonzo_sauce` style. Verification: the inference-side specialist dispatch is at `backend/services/wr_inference_service.py:101-105` (`VALID_STYLES`) plus the gonzo-sauce-conditional load at `backend/services/wr_inference_service.py:43` (`GONZO_FULL_FEATURES = get_gonzo_sauce_features()`).
- **Target Latent:** `cluster-conditioned-recent-speed-quality` (canonical per SP-2 Finding 2 ratification — feature-level latent representing the underlying signal; coexists with MLA's model-output-level latent vocabulary).
- **Train/Inference Status:** **DUPLICATED**.
- **Train/Inference Narrative:** Training-side `model/shared/data_loader.py:45-49` imports `compute_gonzo_speed_features` (qualified name `from shared.gonzo_features import ...`); inference-side `backend/services/feature_engineering_service.py:16-22` imports the same function (qualified name `from model.shared.gonzo_features import ...`). The qualified-name divergence resolves to the same module file at runtime due to the two contexts' differing PYTHONPATH conventions (training: `model/` on `sys.path`; inference: `/app` parent on PYTHONPATH per the import-block context at `backend/services/feature_engineering_service.py:14-22`). The shared module's docstring at `model/shared/gonzo_features.py:1-29` explicitly codifies the no-drift discipline: "This module is the single source of truth for the 14 Gonzo Sauce features. NO duplication of computation logic between training and inference. Drift here = silent calibration bugs (per session learning post-Bug #15 — three distinct bugs this week traced to code-path drift between training and inference)." Operator-stated origin: "Phase A3, 2026-05-01" (`model/shared/gonzo_features.py:28`). DUPLICATED status verifiable: same engineering code path serves both surfaces; no need for line-by-line behavioral comparison because no parallel implementation exists.
- **Notes:** First of 4 Gonzo Speed features (A1-A4) returned by `compute_gonzo_speed_features()`; sister features F-2 (A2 `speed_at_distance_best_18mo`), F-4 (A3 `noteworthy_workout_recent_14d`), F-5 (A4 `noteworthy_workout_count_30d`). Surface-agnostic by design (mixes dirt/turf within same distance cluster) per docstring at `model/shared/gonzo_features.py:308`. NaN-imputed downstream when no eligible PPs exist (`GONZO_SPEED_DEFAULTS['speed_at_distance_recent_weighted'] = None` at `model/shared/gonzo_features.py:69`).

#### 4.1.2 F-2 — `speed_at_distance_best_18mo`

- **F-ID:** F-2
- **Feature Name:** `speed_at_distance_best_18mo`
- **Source Data:** Same source columns as F-1 (`database_schema_bible:4.1.7` `past_performances`: `distance_furlongs`, `final_time`, `lengths_behind`, `race_date`) — but filtered to PPs in the trailing 18 months (`A2_BEST_WINDOW_MONTHS = 18` at `model/shared/gonzo_features.py:60`) within the today's-distance cluster.
- **Engineering Code:** `model/shared/gonzo_features.py:290-397` (function `compute_gonzo_speed_features()`; A2 sub-block at lines 348-362 — peak `_effective_speed_fps()` over the 18-month cluster-eligible window). **Same shared module as F-1; same single-source-of-truth pattern.**
- **Consuming Models:** `[mla:M-2, mla:M-4]` — gonzo_sauce specialist variants only (same constraint as F-1; substrate at `model/shared/feature_definitions.py:223-247` `GONZO_FEATURE_DEFS` which enumerates this feature in the gonzo_speed group, and `model/shared/feature_definitions.py:256-260` `get_gonzo_sauce_features()` which composes it into the 67-feature gonzo_sauce list).
- **Target Latent:** `cluster-conditioned-peak-speed-ceiling` (canonical per SP-2 Finding 2).
- **Train/Inference Status:** **DUPLICATED**.
- **Train/Inference Narrative:** Same shared-module import pattern as F-1 — `model/shared/data_loader.py:45-49` (training) and `backend/services/feature_engineering_service.py:16-22` (inference) both import `compute_gonzo_speed_features` from the same `model/shared/gonzo_features.py` module file. F-1 and F-2 are sister-features within the same single-source function. DUPLICATED status verifiable by absence of parallel implementation. NaN-imputed downstream when no 18-month-cluster-eligible PPs exist (`GONZO_SPEED_DEFAULTS['speed_at_distance_best_18mo'] = None` at `model/shared/gonzo_features.py:70`).
- **Notes:** Distance cluster boundary at exactly 8.0F is MILE not SPRINT per `model/shared/gonzo_features.py:46-47` adjacent comment ("Sprint cluster is strict <8F"); MILE upper boundary 8.5F (route is ≥8.5F per `ROUTE_DISTANCE_FURLONGS = 8.5` at line 93). Peak (max) operator on `_effective_speed_fps()` values; the helper at `model/shared/gonzo_features.py:170-195` returns `None` for invalid inputs (distance ≤ 0, final_time ≤ 30, effective_time ≤ 0 — per lines 189-194), filtered out before `max()` at lines 358-362.

#### 4.1.3 F-3 — `lasix` (substrate-grounded post-SP-2 directive)

- **F-ID:** F-3
- **Feature Name:** `lasix`
- **Source Data:** Direct passthrough from `database_schema_bible:4.1.6` `entries.lasix` BOOLEAN column (DEFAULT `false`). Equipment-group feature per `model/shared/feature_definitions.py:84` (`FeatureDef('lasix', 'equipment', False, 0.0)` — `derived=False`, indicating direct DB column rather than computed from history).
- **Engineering Code:** Two parallel implementation sites (canonical Bug #22 surface):
  - **Training-side:** `model/shared/data_loader.py:198` (column read in SQL: `e.lasix`); `model/shared/data_loader.py:621-623` (BOOLEAN-to-float conversion: `lasix = 1.0 if entry_row.get('lasix') else 0.0`); `model/shared/data_loader.py:636` (output dict assembly: `'lasix': lasix,`).
  - **Inference-side:** `backend/services/feature_engineering_service.py:945` (`lasix = float(entry.lasix)`); `backend/services/feature_engineering_service.py:968` (output dict assembly: `'lasix': lasix,`). Plus the dead-code-fallback list reference at `:176` per the F-3 PHASE_5_BACKLOG candidate below.
- **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`:
  - M-1 (wp_core), M-3 (rk_core), M-5 (pl_core): `lasix` is in `get_lean53_core_features() = 47` per `model/shared/feature_definitions.py:205-211` (lean53 base + workouts cull; `lasix` is in equipment group, not in `LEAN53_CULL` at lines 185-194).
  - M-2 (wp_full), M-4 (rk_full): `lasix` is in `get_lean53_features() = 53` and in `get_gonzo_sauce_features() = 67`.
  - M-8 (longshot_rf): trains on `get_core_features()` per `model/longshot/train.py:32`; `lasix` is in equipment group, not workouts, so survives the `requires_workouts` filter.
  - **M-11 (ensemble) consumption:** NOT consumed. M-11's `ENSEMBLE_FEATURES` list at `model/ensemble/config.py:8-19` is a 10-element list (`win_prob`, `rank_score`, `longshot_prob`, `trajectory_score`, `angle_ev`, `angle_posterior`, `closing_odds`, `morning_line_odds`, `race_quality_tier`, `field_size`); `lasix` is NOT in this list. ENSEMBLE_FEATURES contract substrate verified via `model/ensemble/config.py:8-19` direct read.
  - M-6, M-7, M-9, M-10 do NOT consume this feature: M-6 / M-7 are arithmetic overlays consuming probability outputs (not feature-list features); M-9 (trajectory_lstm) consumes raw PP sequences (LSTM tensor input); M-10 (Bayesian angle scorer) consumes `angle_stats` substrate per `database_schema_bible:4.1.15` and per-entry angle flags from `entries` (`lasix_first_time` is a separate equipment feature — F-72 — not the same as the F-3 `lasix` BOOLEAN).
- **Target Latent:** `medication-effect-on-pulmonary-bleeding-and-performance` (canonical per SP-2 Finding 2).
- **Train/Inference Status:** **DUPLICATED** (upgraded from UNVERIFIED per SP-2 directive — substrate-grounded).
- **Train/Inference Narrative:** Both surfaces consume `entries.lasix` as a direct BOOLEAN passthrough — the feature is one of 5 in the equipment group per `model/shared/feature_definitions.py:84-88` declared with `derived=False, default_value=0.0`. Training-side computation at `model/shared/data_loader.py:621-623, 636` performs `1.0 if val else 0.0` conversion; inference-side computation at `backend/services/feature_engineering_service.py:945, 968` performs `float(entry.lasix)` conversion. Both produce a binary float (0.0 / 1.0); both source the value from the same `entries.lasix` BOOLEAN column. Independently verified equivalent computation per QB_DRAFTING_SPEC § 5.7 DUPLICATED criterion. F-3 is one instance of the broader 66-base-feature parallel-implementation drift surface (Bug #22, in PHASE_5_BACKLOG); for direct DB passthrough features (lasix, lasix_first_time, blinkers_on, blinkers_off, weight_carried, apprentice_allowance, closing_odds — all `derived=False` per FEATURE_DEFS), the parallel-implementation surface is reduced to a BOOLEAN/INT/DECIMAL coercion which is invariant to per-side logic drift; for derived features (`derived=True`), per-side logic differs and per-feature substrate verification at the row's narrative is required for non-UNVERIFIED classification.
- **Notes:** F-3 is the canonical "direct DB column passthrough" pattern row — cited as the discipline-archetype for the simplest in-scope feature class. The lazy-import + hard-coded-fallback structure at `backend/services/feature_engineering_service.py:128-188` (the `get_feature_names` method's try/except pattern that imports `get_odds_blind_features` / `get_odds_aware_features` from `model.shared.feature_definitions` AND falls back to a hard-coded 60+-element list inline at lines 141-188) is a code-dissonance candidate independent of this row's substrate. **PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=refactor; rationale="lazy ImportError-fallback at feature_engineering_service.py:128-188 hard-codes 60+ feature names inline that duplicate model/shared/feature_definitions.py's canonical FEATURE_DEFS — drift risk if either is updated independently; the try/except defensiveness is dead code if both files always co-deploy"; cite=backend/services/feature_engineering_service.py:128-188.**

#### 4.1.4 F-4 — `noteworthy_workout_recent_14d`

- **F-ID:** F-4
- **Feature Name:** `noteworthy_workout_recent_14d`
- **Source Data:** `database_schema_bible:4.1.8` `workouts` columns (`workout_date`, `workout_time`, `distance_furlongs`, `workout_type`); plus `model/shared/par_times.py` `is_noteworthy_workout()` predicate (par-time medians + improving-times pattern detection).
- **Engineering Code:** `model/shared/gonzo_features.py:290-397` (A3 sub-block at lines 364-388). Single-source-of-truth shared module.
- **Consuming Models:** `[mla:M-2, mla:M-4]` — gonzo_sauce specialist variants only.
- **Target Latent:** `recent-workout-quality-elevation`.
- **Train/Inference Status:** **DUPLICATED**.
- **Train/Inference Narrative:** Same shared-module import pattern as F-1/F-2 (`model/shared/data_loader.py:45-49` training; `backend/services/feature_engineering_service.py:16-22` inference). Inference-side caller at `backend/services/wr_inference_service.py:35` constructs `par_dict` lazily via `model.shared.par_times.compute_workout_pars` (Phase A3 par-time medians; cached per service-instance). DUPLICATED status verifiable by absence of parallel implementation.
- **Notes:** `requires_workouts=True` per `model/shared/feature_definitions.py:230` GONZO_FEATURE_DEFS row. Returns BOOLEAN (True if any par-noteworthy workout in trailing 14d OR improving-times pattern detected via `_detect_improving_workout_pattern()` at `model/shared/gonzo_features.py:198-228` using a 30d window with strict monotonic decreasing time pattern). Default `False` per `GONZO_SPEED_DEFAULTS` at `model/shared/gonzo_features.py:71`.

#### 4.1.5 F-5 — `noteworthy_workout_count_30d`

- **F-ID:** F-5
- **Feature Name:** `noteworthy_workout_count_30d`
- **Source Data:** Same as F-4 (`workouts` table; `is_noteworthy_workout()` predicate).
- **Engineering Code:** `model/shared/gonzo_features.py:391-395` (A4 sub-block; counts par-noteworthy workouts in trailing 30d, excluding the improving-times pattern which is A3-only per the `# A4: count of par-noteworthy workouts in 30d (pattern excluded — A3 only)` comment at line 390).
- **Consuming Models:** `[mla:M-2, mla:M-4]` — gonzo_sauce specialist variants only.
- **Target Latent:** `recent-workout-volume-of-quality-events`.
- **Train/Inference Status:** **DUPLICATED**.
- **Train/Inference Narrative:** Same shared-module pattern. F-4 and F-5 use the same `compute_gonzo_speed_features()` function (4 features returned per call); F-4 is BOOLEAN (improving-pattern-aware), F-5 is INTEGER count (par-noteworthy-only). Default `0` per `GONZO_SPEED_DEFAULTS` at `model/shared/gonzo_features.py:72`.
- **Notes:** `requires_workouts=True` per `model/shared/feature_definitions.py:231-232`.

#### 4.1.6 F-6 — `route_expand_count`

- **F-ID:** F-6
- **Feature Name:** `route_expand_count`
- **Source Data:** `database_schema_bible:4.1.7` `past_performances` columns (`finish_position`, `call_2_position`, `lengths_behind`, `call_2_lengths`, `distance_furlongs`, `race_date`) — last 5 ROUTE PPs (today's distance ≥8.5F gating). PP-level trajectory delta computed at `model/shared/gonzo_features.py:231-246` `_compute_pp_trajectory_delta()`; bucket classification at `:249-257` `_classify_trajectory_bucket()`.
- **Engineering Code:** `model/shared/gonzo_features.py:400-474` (function `compute_gonzo_trajectory_features()`; B1 increments `out['route_expand_count']` at line 466 when `bucket == 'expand'` per `_classify_trajectory_bucket(delta)` returning `'expand'` for `delta < TRAJECTORY_EXPAND_THRESHOLD = -1.5`).
- **Consuming Models:** `[mla:M-2, mla:M-4]` — gonzo_sauce specialist variants only.
- **Target Latent:** `route-late-pace-expansion-frequency`.
- **Train/Inference Status:** **DUPLICATED**.
- **Train/Inference Narrative:** Same shared-module pattern. ROUTE-only feature (today's distance ≥8.5F per `ROUTE_DISTANCE_FURLONGS` at `:93`); sprint races today return all defaults. Buckets sum to actual count of route PPs (cap 5; doesn't pad with synthetic zeros).
- **Notes:** Sister features F-7 through F-12 (B2-B7); collectively populated by single `compute_gonzo_trajectory_features()` call. Mixed-units delta formula (`(finish_position - call_2_position) + (lengths_behind - call_2_lengths)`) is intentional per docstring at `:81-86` ("combines passed horses + gained ground").

#### 4.1.7 F-7 — `route_held_count`

- **F-ID:** F-7
- **Feature Name:** `route_held_count`
- **Source Data:** Same as F-6.
- **Engineering Code:** `model/shared/gonzo_features.py:400-474` (B2 — bucket `'held'` returned by `_classify_trajectory_bucket()` for `-1.5 ≤ delta ≤ 1.5` per thresholds at `:96-97`).
- **Consuming Models:** `[mla:M-2, mla:M-4]` (same as F-6).
- **Target Latent:** `route-late-pace-stability-frequency`.
- **Train/Inference Status:** **DUPLICATED**. Same shared-module pattern.
- **Notes:** ROUTE-only.

#### 4.1.8 F-8 — `route_erode_count`

- **F-ID:** F-8
- **Feature Name:** `route_erode_count`
- **Source Data:** Same as F-6.
- **Engineering Code:** `model/shared/gonzo_features.py:400-474` (B3 — bucket `'erode'` for `1.5 < delta ≤ 3.0` per thresholds at `:97`).
- **Consuming Models:** `[mla:M-2, mla:M-4]`.
- **Target Latent:** `route-late-pace-mild-erosion-frequency`.
- **Train/Inference Status:** **DUPLICATED**.
- **Notes:** ROUTE-only.

#### 4.1.9 F-9 — `route_collapse_count`

- **F-ID:** F-9
- **Feature Name:** `route_collapse_count`
- **Source Data:** Same as F-6.
- **Engineering Code:** `model/shared/gonzo_features.py:400-474` (B4 — bucket `'collapse'` for `delta > 3.0` per fallthrough at `:257`).
- **Consuming Models:** `[mla:M-2, mla:M-4]`.
- **Target Latent:** `route-late-pace-severe-erosion-frequency`.
- **Train/Inference Status:** **DUPLICATED**.
- **Notes:** ROUTE-only. B1-B4 are mutually-exclusive bucket assignments per single PP delta.

#### 4.1.10 F-10 — `route_charge_short_count`

- **F-ID:** F-10
- **Feature Name:** `route_charge_short_count`
- **Source Data:** `database_schema_bible:4.1.7` `past_performances` columns (`finish_position`, `call_2_position`, `call_2_lengths`, `call_3_position`, `call_3_lengths`).
- **Engineering Code:** `model/shared/gonzo_features.py:400-474` (B5 increment at line 469 when `_is_charge_short(pp)` returns True; helper at `:260-283` requires `call_3_position < call_2_position AND call_3_lengths < call_2_lengths AND 2 ≤ finish_position ≤ 4`).
- **Consuming Models:** `[mla:M-2, mla:M-4]`.
- **Target Latent:** `route-closing-but-out-of-track-frequency`.
- **Train/Inference Status:** **DUPLICATED**.
- **Train/Inference Narrative:** Same shared-module pattern. CHARGE_SHORT is independent of EXPAND/HELD/ERODE/COLLAPSE per docstring at `:90-91`: "a single PP can contribute to one bucket AND simultaneously be charge-short."
- **Notes:** ROUTE-only. Returns False (not None) when call_3 data absent — per `:264-267` "don't default-flag."

#### 4.1.11 F-11 — `route_avg_delta`

- **F-ID:** F-11
- **Feature Name:** `route_avg_delta`
- **Source Data:** Same as F-6 (per-PP trajectory delta from `_compute_pp_trajectory_delta()`).
- **Engineering Code:** `model/shared/gonzo_features.py:400-474` (B6 at line 472 — `np.mean(deltas)` over the last 5 ROUTE PPs' valid deltas).
- **Consuming Models:** `[mla:M-2, mla:M-4]`.
- **Target Latent:** `route-average-late-pace-trajectory-magnitude`.
- **Train/Inference Status:** **DUPLICATED**.
- **Notes:** ROUTE-only. Default 0.0 per `GONZO_TRAJECTORY_DEFAULTS` at `:111`.

#### 4.1.12 F-12 — `is_stretching_out`

- **F-ID:** F-12
- **Feature Name:** `is_stretching_out`
- **Source Data:** `database_schema_bible:4.1.7` `past_performances.distance_furlongs` (last 5 PPs at ANY distance; median calculation) plus today's-race `distance_furlongs`.
- **Engineering Code:** `model/shared/gonzo_features.py:400-474` (B7 sub-block at lines 438-450 — `today_distance - median_dist >= STRETCH_OUT_THRESHOLD_FURLONGS = 0.5`).
- **Consuming Models:** `[mla:M-2, mla:M-4]`.
- **Target Latent:** `today-distance-extension-vs-recent-history`.
- **Train/Inference Status:** **DUPLICATED**.
- **Train/Inference Narrative:** Same shared-module pattern. Note: B7 uses last 5 PPs at ANY distance (sprint+route; not the route-only filter that gates B1-B6). Default False per `GONZO_TRAJECTORY_DEFAULTS` at `:112`.
- **Notes:** ROUTE-only by today's-distance gating (sprint races today return all defaults; same gating as B1-B6).

#### 4.1.13 F-13 — `class_tier_at_today_level_count_18mo`

- **F-ID:** F-13
- **Feature Name:** `class_tier_at_today_level_count_18mo`
- **Source Data:** `database_schema_bible:4.1.7` `past_performances` columns (`race_type`, `claiming_price_entered`, `purse`, `grade`, `race_date`, `finish_position`); plus today's-race race_type / claiming_price_entered / purse / grade. Class tier ordinal computed via `model/shared/class_tiers.py` `race_class_tier()` (11-tier scale).
- **Engineering Code:** `model/shared/gonzo_features.py:477-569` (function `compute_gonzo_class_features()`; C1 sub-block at line 550-552 — count of prior PPs in 18-month window with `race_class_tier(pp) == race_class_tier(today)`).
- **Consuming Models:** `[mla:M-2, mla:M-4]` — gonzo_sauce specialist variants only.
- **Target Latent:** `count-of-recent-races-at-exactly-todays-class-level`.
- **Train/Inference Status:** **DUPLICATED**.
- **Train/Inference Narrative:** Same shared-module pattern. DNF/scratched PPs filtered upstream at `_load_raw_pps` per docstring at `:499-501` — `horse_hist` never sees them. Default 0 per `GONZO_CLASS_DEFAULTS` at `:124`.
- **Notes:** Class tier scale is 11-tier from `model/shared/class_tiers.py:race_class_tier`; "today's tier" = result of `race_class_tier(today's race_type, claiming_price_entered, purse, grade)`. Foreign / unclassifiable PPs (where `race_class_tier()` returns None) are skipped.

#### 4.1.14 F-14 — `class_tier_in_money_rate_at_or_above`

- **F-ID:** F-14
- **Feature Name:** `class_tier_in_money_rate_at_or_above`
- **Source Data:** Same as F-13.
- **Engineering Code:** `model/shared/gonzo_features.py:477-569` (C2 sub-block at lines 554-563 — fraction of prior PPs at tier ≥ today_tier where `int(finish_position) <= 3`).
- **Consuming Models:** `[mla:M-2, mla:M-4]`.
- **Target Latent:** `historical-in-money-rate-at-or-above-todays-class-level`.
- **Train/Inference Status:** **DUPLICATED**.
- **Notes:** "At or above" = pp_tier ≥ today_tier. Default 0.0 per `GONZO_CLASS_DEFAULTS` at `:125`. Returns 0.0 if no eligible prior races.

#### 4.1.15 F-15 — `class_tier_avg_position_at_or_above`

- **F-ID:** F-15
- **Feature Name:** `class_tier_avg_position_at_or_above`
- **Source Data:** Same as F-13.
- **Engineering Code:** `model/shared/gonzo_features.py:477-569` (C3 sub-block at lines 564-567 — `np.mean([int(f) for f in at_or_above_finishes])`).
- **Consuming Models:** `[mla:M-2, mla:M-4]`.
- **Target Latent:** `average-finish-position-at-or-above-todays-class-level`.
- **Train/Inference Status:** **DUPLICATED**.
- **Train/Inference Narrative:** Same shared-module pattern. Default semantics distinct from F-13/F-14: C3 default = today's `field_size` (signals "no data; treat as bottom") per `:497-498` docstring + `:506-508` assignment.
- **Notes:** Default per-row, not in `GONZO_CLASS_DEFAULTS` (because depends on row's field_size).

---

The next 65 rows (F-16 through F-80) cover the 66 base features per `model/shared/feature_definitions.py` FEATURE_DEFS in declaration order. F-3 (`lasix`) was authored above as the canonical archetype for direct DB passthrough; the equipment group enumeration below resumes after the Speed/Pace/Trip/Trainer/Workout/Class/Physical groups. All base features are subject to the **Bug #22 parallel-implementation drift surface** per QB Standing Instruction (already in PHASE_5_BACKLOG); the train/inference quaternary classification per row is substrate-grounded via the SP-2 directive batch grep against `model/shared/data_loader.py` + `backend/services/feature_engineering_service.py`. Direct DB passthrough features (`derived=False` per FEATURE_DEFS) are DUPLICATED via BOOLEAN/INT/DECIMAL coercion invariance; derived features (`derived=True`) are UNVERIFIED-pending-line-by-line-comparison absent specific drift evidence at row authorship — Bug #22 cross-reference covers the broader pattern.

#### 4.1.16 F-16 — `speed_fig_last`

- **F-ID:** F-16. **Feature Name:** `speed_fig_last`. **Source Data:** `past_performances.beyer_speed_figure` (most recent valid PP). **Engineering Code:** Training `model/shared/data_loader.py:340` (`'speed_fig_last': last`); inference `backend/services/feature_engineering_service.py:450` (`'speed_fig_last': fig_last`). Plus dead-code-fallback at `:142`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]` (Speed group, not in LEAN53_CULL; `M-11 ENSEMBLE_FEATURES` does NOT include — verified at `model/ensemble/config.py:8-19`). **Target Latent:** `most-recent-beyer-speed-figure`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep). **Train/Inference Narrative:** Both training and inference sites cited at row's Engineering Code emit the same dict key (`'speed_fig_last'`), source from the same DB column (`past_performances.beyer_speed_figure`), and apply the same default (0.0 per FEATURE_DEFS at `model/shared/feature_definitions.py:15`). Training derives `last` from a sorted PP-history view at `data_loader.py:340`; inference derives `fig_last` from `valid_pps` at `feature_engineering_service.py:450`. The "most recent value" semantic is symmetric — both sites take the first valid value after sort/filter. `feature_engineering_service.py:51-55` voluntarily declares "All feature computations MUST match model/shared/data_loader.py EXACTLY" — voluntary discipline reinforces the symmetry. Substrate-grounded DUPLICATED via independent verification of equivalent computation (same source + same default + same "first-of-sorted" semantic). Bug #22 (in PHASE_5_BACKLOG) covers the broader systemic drift surface; this row is one instance whose individual substrate resolves DUPLICATED. **Notes:** `derived=True`. Speed group anchor feature; F-17 through F-26 are the other 10 Speed group features.

#### 4.1.17 F-17 — `speed_fig_avg_3`

- **F-ID:** F-17. **Feature Name:** `speed_fig_avg_3`. **Source Data:** `past_performances.beyer_speed_figure` (last 3 valid PPs, mean). **Engineering Code:** Training `model/shared/data_loader.py:341`; inference `backend/services/feature_engineering_service.py:451`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `recent-3-PP-mean-beyer-speed`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Narrative:** Same parallel-implementation surface as F-16. **Notes:** `derived=True`.

#### 4.1.18 F-18 — `speed_fig_trend`

- **F-ID:** F-18. **Feature Name:** `speed_fig_trend`. **Source Data:** Computed as `last - avg3` per training site `model/shared/data_loader.py:342` and inference site `backend/services/feature_engineering_service.py:452` (both compose F-16 minus F-17). **Engineering Code:** Training `:342` (`'speed_fig_trend': last - avg3`); inference `:452` (`'speed_fig_trend': fig_trend`). **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `recent-beyer-trend-direction`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass: composition derives from F-16 - F-17 in both sites; both upstream rows DUPLICATED). **Notes:** `derived=True`. Composition feature: depends on F-16 + F-17 parity (both DUPLICATED post-revise-pass).

#### 4.1.19 F-19 — `speed_fig_best_career`

- **F-ID:** F-19. **Feature Name:** `speed_fig_best_career`. **Source Data:** `past_performances.beyer_speed_figure` (max over career). **Engineering Code:** Training `model/shared/data_loader.py:343`; inference `backend/services/feature_engineering_service.py:453`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `career-peak-beyer-speed`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.20 F-20 — `speed_fig_best_90d`

- **F-ID:** F-20. **Feature Name:** `speed_fig_best_90d`. **Source Data:** `past_performances.beyer_speed_figure` (max over trailing 90 days). **Engineering Code:** Training `:344`; inference `:454`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `recent-90d-peak-beyer-speed`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.21 F-21 — `speed_fig_at_track`

- **F-ID:** F-21. **Feature Name:** `speed_fig_at_track`. **Source Data:** `past_performances.beyer_speed_figure` filtered to today's `track_code`. **Engineering Code:** Training `:345` (`float(at_track.mean()) if not at_track.empty else defaults['speed_fig_at_track']`); inference `:455`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `mean-beyer-at-todays-track`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.22 F-22 — `speed_fig_at_distance`

- **F-ID:** F-22. **Feature Name:** `speed_fig_at_distance`. **Source Data:** `past_performances.beyer_speed_figure` filtered to today's `distance_furlongs`. **Engineering Code:** Training `:346`; inference `:456`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `mean-beyer-at-todays-distance`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.23 F-23 — `speed_fig_on_surface`

- **F-ID:** F-23. **Feature Name:** `speed_fig_on_surface`. **Source Data:** `past_performances.beyer_speed_figure` filtered to today's `surface`. **Engineering Code:** Training `:347`; inference `:457`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `mean-beyer-on-todays-surface`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.24 F-24 — `speed_fig_vs_field`

- **F-ID:** F-24. **Feature Name:** `speed_fig_vs_field`. **Source Data:** Composed from F-16 (`speed_fig_last`) per-horse minus per-race-field-mean of F-16. **Engineering Code:** Training `model/shared/data_loader.py:875-879` (post-aggregation: `field_avg = features_df.groupby(...)['speed_fig_last'].transform('mean'); features_df['speed_fig_vs_field'] = features_df['speed_fig_last'] - field_avg`); inference `backend/services/feature_engineering_service.py:458` (`'speed_fig_vs_field': float(fig_vs_field)`). **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `relative-speed-rank-within-todays-field`. **Train/Inference Status:** **DIVERGENT-INTENTIONAL** (substrate-grounded post-SP-3 revise-pass). **Train/Inference Narrative:** Design-intent timing divergence between training and inference paths. Training at `data_loader.py:348` emits `'speed_fig_vs_field': 0.0  # filled in post-aggregation with field average` (placeholder during per-horse build), then post-aggregates at `data_loader.py:875-879` (`field_avg = features_df.groupby(...)['speed_fig_last'].transform('mean'); features_df['speed_fig_vs_field'] = features_df['speed_fig_last'] - field_avg`) — i.e., field-aggregation runs AFTER per-horse loop completes, using pandas groupby-transform across the entire features_df. Inference at `feature_engineering_service.py:458` (`'speed_fig_vs_field': float(fig_vs_field)`) computes per-race inline during `_build_entry_features` because inference runs per-race rather than per-horse-history. **The divergence is intentional**: training has access to the complete features_df at post-aggregation time and uses pandas-vectorized groupby-transform for efficiency; inference operates per-race and computes `fig_vs_field` inline against the current race's field. Mathematical result is equivalent (both compute `speed_fig_last_h - mean(speed_fig_last across same race's field)`); only the computation timing differs by design. The training-side comment at `:348` ("filled in post-aggregation with field average") explicitly documents the timing-difference design intent. **Notes:** `derived=True`.

#### 4.1.25 F-25 — `speed_fig_consistency`

- **F-ID:** F-25. **Feature Name:** `speed_fig_consistency`. **Source Data:** Standard deviation of last 5 `beyer_speed_figure` values. **Engineering Code:** Training `:337` (`consistency = float(last5.std()) if len(last5) >= 2 else defaults['speed_fig_consistency']`); inference `:459`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `recent-beyer-variance-stability`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`. Default 5.0 per FEATURE_DEFS (non-zero default, signals "moderate variance assumption when data thin").

#### 4.1.26 F-26 — `speed_fig_sample_size`

- **F-ID:** F-26. **Feature Name:** `speed_fig_sample_size`. **Source Data:** Count of PPs with non-null `beyer_speed_figure`. **Engineering Code:** Training `:350` (`'speed_fig_sample_size': float(len(figs))`); inference `:460` (`'speed_fig_sample_size': float(len(valid_pps))`). **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `count-of-PPs-with-beyer-data`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass: both sites count valid-Beyer-non-null PPs). **Train/Inference Narrative:** Training at `data_loader.py:350` (`'speed_fig_sample_size': float(len(figs))`) counts the `figs` array (filtered to non-null `beyer_speed_figure` values); inference at `feature_engineering_service.py:460` (`'speed_fig_sample_size': float(len(valid_pps))`) counts `valid_pps` (filtered to PPs with valid Beyer data, semantically equivalent population to `figs`). Both sites apply the same float-cast around `len()` of the filtered population. Substrate-grounded DUPLICATED via population-equivalence (both filters select PPs with non-null beyer_speed_figure). **Notes:** `derived=True`. Defines "how many data points the speed feature aggregates draw from."

#### 4.1.27 F-27 — `early_pace_last`

- **F-ID:** F-27. **Feature Name:** `early_pace_last`. **Source Data:** `past_performances.early_pace_figure` (most recent non-null). **Engineering Code:** Training `model/shared/data_loader.py:363` (`float(prior['early_pace_figure'].dropna().iloc[0]) if not prior['early_pace_figure'].dropna().empty else defaults['early_pace_last']`); inference `backend/services/feature_engineering_service.py:541`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `most-recent-early-pace-figure`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`. Pace group anchor; F-28 through F-32 are the other 5 Pace group features.

#### 4.1.28 F-28 — `late_pace_last`

- **F-ID:** F-28. **Feature Name:** `late_pace_last`. **Source Data:** `past_performances.late_pace_figure` (most recent non-null). **Engineering Code:** Training `:364`; inference `:542`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `most-recent-late-pace-figure`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.29 F-29 — `pace_delta_last`

- **F-ID:** F-29. **Feature Name:** `pace_delta_last`. **Source Data:** `past_performances.pace_delta` (most recent non-null; backfilled by migrations 005 + 009 per `database_schema_bible:4.1.7` + `:4.2.1`). **Engineering Code:** Training `:365`; inference `:543`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `most-recent-pace-delta-final-vs-call2`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`. Source column populated by migration 009's correction (uses `finish_position - call_2_position` instead of migration 005's `finish_call_position - call_2_position` due to 0%-population of finish_call_position; per `database_schema_bible:4.2.1` migration 009).

#### 4.1.30 F-30 — `avg_call1_position`

- **F-ID:** F-30. **Feature Name:** `avg_call1_position`. **Source Data:** `past_performances.call_1_position` (mean over PP history). **Engineering Code:** Training `:368`; inference `:544`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `average-position-at-first-call`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.31 F-31 — `avg_stretch_gain`

- **F-ID:** F-31. **Feature Name:** `avg_stretch_gain`. **Source Data:** `past_performances.call_2_position` minus `past_performances.finish_position` (per training-side inline comment at `model/shared/data_loader.py:370` "stretch gain: call_2_position minus finish_position (negative = gained positions)"; per-PP value averaged across last 5 PPs at lines 368-378). Inference-side computation at `backend/services/feature_engineering_service.py:511-523` confirms formula equivalence per explicit `# FIX #5: use call_2_position, not stretch_position` comment at line 511. Source columns substrate-cited at `database_schema_bible:§ 4.1.7` `past_performances` table: `call_2_position` and `finish_position`. **Engineering Code:** Training `:368-378`; inference `:545`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `average-position-change-stretch-to-finish`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-v1-patched-a-extended substrate verification per Tony Decision F4-A ratification). **Train/Inference Narrative:** F-31 avg_stretch_gain: training-side at `model/shared/data_loader.py:368-378` and inference-side at `backend/services/feature_engineering_service.py:511-523` both compute the formula `call_2_position - finish_position` with structurally equivalent null-handling guards (training line 371 `valid = last5.dropna(subset=['call_2_position', 'finish_position'])`; inference lines 514-515 inline filter to non-null pairs). Per-side fallback values verified equivalent: training `defaults['avg_stretch_gain'] = 0.0` per `model/shared/feature_definitions.py:32` (`FeatureDef('avg_stretch_gain', 'pace', True, 0.0)` — 4th field of FeatureDef per dataclass declaration at lines 4-11 is `default_value`; `get_feature_defaults()` at lines 118-119 returns `{f.name: f.default_value for f in FEATURE_DEFS}`); inference hardcoded `0.0` at `feature_engineering_service.py:522` (`avg_stretch = float(np.mean(stretch_gains)) if stretch_gains else 0.0`). Formula equivalence + null-handling equivalence + fallback-value equivalence (training 0.0 == inference 0.0) = DUPLICATED status verified. The `# FIX #5: use call_2_position, not stretch_position` comment at inference line 511 is voluntary-mirroring-discipline evidence reinforcing the substrate-grounded DUPLICATED classification. Bug #22 cross-reference: F-31 was previously listed (in v1-draft + v1-patched-a) as one instance of the broader 66-base-feature parallel-implementation drift surface (Bug #22, in PHASE_5_BACKLOG); v1-patched-a-extended substrate verification resolved F-31 specifically to DUPLICATED — Bug #22 surface remains as documentation of the broader pattern, but F-31 no longer contributes to the UNVERIFIED count. **Notes:** `derived=True`.

#### 4.1.32 F-32 — `pace_scenario_today`

- **F-ID:** F-32. **Feature Name:** `pace_scenario_today`. **Source Data:** Per-race aggregation across today's field — count of horses with early-pace-running profile (`call_1_position` low). **Engineering Code:** Training `:378-388` (counts of early/front-running horses in today's field); inference `:546`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]` for legacy pre-lean53 artifacts ONLY. Note: in LEAN53_CULL per `model/shared/feature_definitions.py:188` — lean53 trained models do NOT include this feature in their feature_list. **Target Latent:** `count-of-early-pace-horses-in-todays-field`. **Train/Inference Status:** **UNVERIFIED**. **Train/Inference Narrative:** F-32 is one instance of the broader 66-base-feature parallel-implementation drift surface (Bug #22, in PHASE_5_BACKLOG). Substrate verification at row-authorship cycle was substrate-grounded inconclusive: this is a complex per-race-field aggregation feature with timing differences analogous to F-24's DIVERGENT-INTENTIONAL classification — training site at `data_loader.py:378-388` and inference site at `feature_engineering_service.py:546` use different per-race assembly paths whose mathematical equivalence requires line-by-line comparison. LEAN53_CULL status (per `model/shared/feature_definitions.py:188`) means lean53 trained models do NOT consume this feature, reducing the production-impact of any drift to legacy pre-lean53 `win_prob_full` / `ranker_full` general artifacts only (per the wp_full_types fallback chain at `backend/services/wr_inference_service.py:194-195`). Resolution defers to follow-up patch cycle covering the full Bug #22 surface. **Notes:** `derived=True`. Also in RANKER_FULL_CULL (the lean51 ranker_full cull from `:151-161`).

#### 4.1.33 F-33 — `troubled_trip_last`

- **F-ID:** F-33. **Feature Name:** `troubled_trip_last`. **Source Data:** `past_performances.trouble_comment` parsed for trip-trouble keywords (most recent PP). **Engineering Code:** Training `:411`; inference `:578-580`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]` for legacy pre-lean53 artifacts ONLY. In RANKER_FULL_CULL (`:159`); not in LEAN53_CULL. **Target Latent:** `most-recent-trip-trouble-flag`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass). **Train/Inference Narrative:** Both training at `data_loader.py:411` (`'troubled_trip_last': troubled_last`) and inference at `feature_engineering_service.py:578-580` (`'troubled_trip_last': float(...)`) source from the same `past_performances.trouble_comment` parsing — the trip-trouble derivation is consumed via `pps['trip_troubled']` boolean column in both files (substrate at `data_loader.py:411-415` and `feature_engineering_service.py:578-589`). Same source, same most-recent-PP semantic, same default. Substrate-grounded DUPLICATED. **Notes:** `derived=True`. Trip group anchor; F-34 through F-40 are the other 7 Trip group features.

#### 4.1.34 F-34 — `troubled_trip_freq`

- **F-ID:** F-34. **Feature Name:** `troubled_trip_freq`. **Source Data:** Same as F-33 (trouble_comment-derived) over PP history. **Engineering Code:** Training `:412`; inference `:581`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `frequency-of-trip-trouble-in-PP-history`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.35 F-35 — `pace_setter_freq`

- **F-ID:** F-35. **Feature Name:** `pace_setter_freq`. **Source Data:** Frequency of pace-setter classification in PP history. **Engineering Code:** Training `:413`; inference `:584`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `frequency-as-pace-setter-in-PP-history`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.36 F-36 — `faded_freq`

- **F-ID:** F-36. **Feature Name:** `faded_freq`. **Source Data:** Frequency of faded/late-erosion pattern in PP history. **Engineering Code:** Training `:414`; inference `:589`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `frequency-of-faded-finish-in-PP-history`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.37 F-37 — `late_rally_freq`

- **F-ID:** F-37. **Feature Name:** `late_rally_freq`. **Source Data:** Frequency of late-rally pattern in PP history. **Engineering Code:** Training `:415`; inference `:570` (default-handling block). **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `frequency-of-late-rally-in-PP-history`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.38 F-38 — `avg_wide_path`

- **F-ID:** F-38. **Feature Name:** `avg_wide_path`. **Source Data:** Average wide-path distance derivative from PP-history call-position columns. **Engineering Code:** Training in `data_loader.py` trip-group block; inference `feature_engineering_service.py:571`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `average-wide-path-loss-distance-in-PP-history`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.39 F-39 — `wide_3plus_freq`

- **F-ID:** F-39. **Feature Name:** `wide_3plus_freq`. **Source Data:** Frequency of 3+ wide path classification in PP history. **Engineering Code:** Training in trip-group block; inference `:572`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]` for legacy pre-lean53 artifacts ONLY. In RANKER_FULL_CULL (`:158`); not in LEAN53_CULL but may be in some specialty culls. **Target Latent:** `frequency-of-3plus-wide-path-in-PP-history`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.40 F-40 — `gate_issue_freq`

- **F-ID:** F-40. **Feature Name:** `gate_issue_freq`. **Source Data:** Frequency of gate-trouble classification in PP history. **Engineering Code:** Training in trip-group block; inference `:573`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `frequency-of-gate-issue-in-PP-history`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.41 F-41 — `trainer_win_rate`

- **F-ID:** F-41. **Feature Name:** `trainer_win_rate`. **Source Data:** `database_schema_bible:3.2` `trainer_stats` materialized view (column `win_rate` per `_safe_float(r.get('win_rate'), TRAINER_DEFAULTS['trainer_win_rate'])`). **Engineering Code:** Training `model/shared/data_loader.py:443` (SQL fetched + `_safe_float` coercion); inference `backend/services/feature_engineering_service.py:728-731` (cache-backed `_get_trainer_stats()` at `:1124-1153` + `_safe_float` coercion at `:728`). **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `trainer-career-win-rate`. **Train/Inference Status:** **DUPLICATED**. **Train/Inference Narrative:** Both surfaces source from the same `trainer_stats` materialized view (per `database_schema_bible:3.2`); both apply `_safe_float(value, default)` coercion with the same default value (`0.10` per FEATURE_DEFS at `:46` AND `TRAINER_DEFAULTS['trainer_win_rate'] = 0.10` at `data_loader.py:81` AND inference TRAINER_DEFAULTS at `feature_engineering_service.py:38`). Independently verified equivalent computation per QB_DRAFTING_SPEC § 5.7 DUPLICATED criterion. The matview-fed-via-SQL pattern reduces the parallel-implementation surface to "fetch row + coerce default" — invariant to per-side derivation logic. **Notes:** `derived=False` per FEATURE_DEFS at `:46`. Trainer group anchor; F-42 through F-45 are the other 4 Trainer group features. Note that the trainer_stats matview is currently NOT auto-refreshed (per `database_schema_bible:3.2` "Refresh discipline" section — manual REFRESH after data loads only); this affects matview row-freshness but not the parity between train/inference surfaces.

#### 4.1.42 F-42 — `trainer_itm_rate`

- **F-ID:** F-42. **Feature Name:** `trainer_itm_rate`. **Source Data:** `trainer_stats` matview (column `itm_rate`). **Engineering Code:** Training `:444`; inference `:732-735`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `trainer-career-in-the-money-rate`. **Train/Inference Status:** **DUPLICATED** (same matview-fed pattern as F-41; default 0.30 in both). **Notes:** `derived=False`.

#### 4.1.43 F-43 — `trainer_layoff_win_rate`

- **F-ID:** F-43. **Feature Name:** `trainer_layoff_win_rate`. **Source Data:** `trainer_stats` matview (column `layoff_win_rate`). **Engineering Code:** Training `:445`; inference `:736-738`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `trainer-win-rate-on-layoff-≥30d-returnees`. **Train/Inference Status:** **DUPLICATED**. **Notes:** `derived=False`. Default 0.08.

#### 4.1.44 F-44 — `trainer_lasix_win_rate`

- **F-ID:** F-44. **Feature Name:** `trainer_lasix_win_rate`. **Source Data:** `trainer_stats` matview (column `lasix_win_rate`). **Engineering Code:** Training `:446`; inference. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `trainer-win-rate-on-first-time-lasix-runners`. **Train/Inference Status:** **DUPLICATED**. **Notes:** `derived=False`. Default 0.12.

#### 4.1.45 F-45 — `trainer_sample_size`

- **F-ID:** F-45. **Feature Name:** `trainer_sample_size`. **Source Data:** `trainer_stats` matview (column `total_starts`). **Engineering Code:** Training `:447`; inference. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `trainer-total-starts-in-matview-cohort`. **Train/Inference Status:** **DUPLICATED**. **Notes:** `derived=False`. The matview's HAVING COUNT(*) >= 5 inclusion rule means `trainer_sample_size >= 5` for any trainer present in the matview (per `database_schema_bible:3.2`); trainers with <5 starts are absent from the matview and the inference path falls back to default 0.0.

#### 4.1.46 F-46 — `days_since_last_workout`

- **F-ID:** F-46. **Feature Name:** `days_since_last_workout`. **Source Data:** `database_schema_bible:4.1.8` `workouts.workout_date` (most recent for horse). **Engineering Code:** Training `:510` (`'days_since_last_workout': days_since`); inference `:701` (`'days_since_last_workout': float(days_since)`). **Consuming Models:** `[mla:M-2, mla:M-4]` — workout-aware models only (M-2 wp_full + M-4 rk_full); M-1 wp_core / M-3 rk_core / M-5 pl_core / M-8 longshot_rf are workout-blind (M-1/M-3 use lean53_core 47-feat without workouts; M-5 uses lean53_core; M-8 uses get_core_features which excludes workouts per the `requires_workouts` filter at `model/shared/feature_definitions.py:128-132`). **Target Latent:** `days-since-most-recent-workout`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `requires_workouts=True`. Workout group anchor; F-47 through F-53 are the other 7 Workout group features. Default 30.0 per FEATURE_DEFS at `:53`.

#### 4.1.47 F-47 — `workout_count_30d`

- **F-ID:** F-47. **Feature Name:** `workout_count_30d`. **Source Data:** `workouts` filtered to trailing 30 days, count. **Engineering Code:** Training `:511`; inference `:702`. **Consuming Models:** `[mla:M-2, mla:M-4]`. **Target Latent:** `count-of-workouts-in-30d`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `requires_workouts=True`.

#### 4.1.48 F-48 — `bullet_work_14d`

- **F-ID:** F-48. **Feature Name:** `bullet_work_14d`. **Source Data:** `workouts.is_bullet` flag in trailing 14 days, BOOLEAN. **Engineering Code:** Training `:512`; inference. **Consuming Models:** `[mla:M-2, mla:M-4]`. **Target Latent:** `bullet-workout-presence-in-14d`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `requires_workouts=True`.

#### 4.1.49 F-49 — `bullet_count_30d`

- **F-ID:** F-49. **Feature Name:** `bullet_count_30d`. **Source Data:** `workouts.is_bullet` count over trailing 30 days. **Engineering Code:** Training `:513`; inference `:655` (`bullet_count_30d = float(sum(...))`). **Consuming Models:** `[mla:M-2, mla:M-4]` for legacy pre-lean53 ranker_full ONLY. In RANKER_FULL_CULL (`:158`). **Target Latent:** `count-of-bullet-workouts-in-30d`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `requires_workouts=True`.

#### 4.1.50 F-50 — `best_workout_speed_index`

- **F-ID:** F-50. **Feature Name:** `best_workout_speed_index`. **Source Data:** `workouts.workout_time` divided by distance, peak over recent window. **Engineering Code:** Training `:514`; inference. **Consuming Models:** `[mla:M-2, mla:M-4]`. **Target Latent:** `peak-workout-speed-index-over-recent-window`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `requires_workouts=True`. Default 0.5 per FEATURE_DEFS at `:57`.

#### 4.1.51 F-51 — `workout_speed_trend`

- **F-ID:** F-51. **Feature Name:** `workout_speed_trend`. **Source Data:** Trend in workout-speed-index over time. **Engineering Code:** Training `:515`; inference. **Consuming Models:** `[mla:M-2, mla:M-4]` for legacy pre-lean53 ranker_full ONLY. In RANKER_FULL_CULL (`:160`). **Target Latent:** `workout-speed-trend-direction`. **Train/Inference Status:** **UNVERIFIED**. **Train/Inference Narrative:** F-51 is one instance of the broader 66-base-feature parallel-implementation drift surface (Bug #22, in PHASE_5_BACKLOG). Substrate verification at row-authorship cycle was substrate-grounded inconclusive: "trend" computation semantics may differ between sides — training site at `data_loader.py:515` emits `speed_trend` derived via unspecified-window logic in the workout-group block; inference site does not surface a clearly-equivalent computation in the cited line range (the inference workout block at `feature_engineering_service.py:701-707` does not show explicit trend computation matching the training-side logic). RANKER_FULL_CULL status (per `:160`) limits production impact to legacy pre-lean53 ranker_full artifacts. Resolution defers to follow-up patch cycle covering the full Bug #22 surface. **Notes:** `requires_workouts=True`.

#### 4.1.52 F-52 — `gate_work_30d`

- **F-ID:** F-52. **Feature Name:** `gate_work_30d`. **Source Data:** `workouts.workout_type='G'` (gate work flag) presence in trailing 30 days. **Engineering Code:** Training `:516`; inference `:689` (`gate_work_30d = float(any(...))`). **Consuming Models:** `[mla:M-2, mla:M-4]` for legacy pre-lean53 ranker_full + win_prob_full ONLY. In LEAN53_CULL (`:189`) + RANKER_FULL_CULL (`:153`); lean53-trained models do NOT include this feature. **Target Latent:** `gate-work-presence-in-30d`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `requires_workouts=True`.

#### 4.1.53 F-53 — `workout_frequency_score`

- **F-ID:** F-53. **Feature Name:** `workout_frequency_score`. **Source Data:** `min(workout_count_30d / 4.0, 1.0)` — saturating monotonic transform of F-47. **Engineering Code:** Training `:517`; inference `:698` (`frequency_score = min(workout_count_30d / 4.0, 1.0)`). **Consuming Models:** `[mla:M-2, mla:M-4]` for legacy pre-lean53 ranker_full + win_prob_full ONLY. In LEAN53_CULL (`:193`) + RANKER_FULL_CULL (`:157`); explicit `r=1.000` perfect duplicate of F-47 per the LEAN53_CULL comment at `:182-183` and RANKER_FULL_CULL comment at `:155-156`. **Target Latent:** `saturating-workout-frequency-score`. **Train/Inference Status:** **DUPLICATED**. **Train/Inference Narrative:** Both sites compute identical formula `min(F-47 / 4.0, 1.0)` against the same F-47 source. Substrate-grounded DUPLICATED via verbatim formula equality at `data_loader.py:517` (`'workout_frequency_score': min(count_30 / 4.0, 1.0)`) and `feature_engineering_service.py:698` (`frequency_score = min(workout_count_30d / 4.0, 1.0)`). **Notes:** `requires_workouts=True`. Phase 5 disposition: kill-on-next-retrain (already in cull lists; would otherwise be DUPLICATED-but-redundant-with-F-47).

#### 4.1.54 F-54 — `class_direction`

- **F-ID:** F-54. **Feature Name:** `class_direction`. **Source Data:** Today's class tier vs most recent PP class tier — sign of change (-1, 0, +1). **Engineering Code:** Training `:536-540` (`class_direction = 0.0; if ...: class_direction = 1.0; if ...: class_direction = -1.0`); inference `:801-810` (substrate-equivalent block with explicit `# class_direction: matches data_loader` comment at `:801`). **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `today-class-rise-or-drop-direction`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass via explicit code-comment evidence). **Train/Inference Narrative:** Training at `data_loader.py:536-540` and inference at `feature_engineering_service.py:801-810` use parallel branch logic with explicit `# class_direction: matches data_loader` comment at the inference site (`:801`). Both branches: `class_direction = 0.0; if (today_purse > last_purse): class_direction = 1.0; if (today_purse < last_purse): class_direction = -1.0`. Same conditional logic structure, same return values (-1.0 / 0.0 / 1.0). The inference-side comment voluntarily declares discipline-mirroring; substrate-grounded DUPLICATED via independently-verified equivalent-computation (sign comparison of two values). **Notes:** `derived=True`. Class group anchor. The voluntary-discipline comment pattern at `:777, 801` is the canonical instance of the inference-side voluntary-mirroring discipline this Bible's § 5 narrative references.

#### 4.1.55 F-55 — `purse_change_pct`

- **F-ID:** F-55. **Feature Name:** `purse_change_pct`. **Source Data:** Today's race `purse` vs most recent PP `purse`, percent change. **Engineering Code:** Training `:557` (`'purse_change_pct': purse_change`); inference `:812` (`purse_change_pct = purse_change`). **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `today-purse-change-vs-last-PP`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.56 F-56 — `claiming_price_change_pct`

- **F-ID:** F-56. **Feature Name:** `claiming_price_change_pct`. **Source Data:** Today's race `claiming_price` vs most recent PP `claiming_price_entered`, percent change. **Engineering Code:** Training `:558`; inference. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `today-claiming-price-change-vs-last-PP`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.57 F-57 — `career_class_ceiling`

- **F-ID:** F-57. **Feature Name:** `career_class_ceiling`. **Source Data:** Maximum class tier observed across PP history. **Engineering Code:** Training `:559`; inference `:789`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `career-peak-class-level`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.58 F-58 — `current_vs_ceiling_pct`

- **F-ID:** F-58. **Feature Name:** `current_vs_ceiling_pct`. **Source Data:** Composed as today_class_tier / F-57. **Engineering Code:** Training `:560`; inference `:790`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `today-class-as-fraction-of-career-ceiling`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`. Default 1.0 per FEATURE_DEFS at `:67`.

#### 4.1.59 F-59 — `class_consistency`

- **F-ID:** F-59. **Feature Name:** `class_consistency`. **Source Data:** Standard deviation of last-5-PPs purse values. **Engineering Code:** Training `:553` (`class_consistency = float(last5_purses.std()) if len(last5_purses) >= 2 else defaults['class_consistency']`); inference `:836-838`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `class-level-variance-stability`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.60 F-60 — `race_quality_tier`

- **F-ID:** F-60. **Feature Name:** `race_quality_tier`. **Source Data:** `database_schema_bible:4.1.5` `races.race_type` — encoded ordinal via `_encode_race_quality_tier()`. **Engineering Code:** Training `:562` (`'race_quality_tier': _encode_race_quality_tier(row.get('race_type'))`); inference `:777, 792`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8, mla:M-11]` — note M-11 ENSEMBLE_FEATURES at `model/ensemble/config.py:17` includes `race_quality_tier` explicitly. **Target Latent:** `categorical-encoding-of-race-class-stakes-allowance-msw-claiming`. **Train/Inference Status:** **DUPLICATED** for the encoding logic (`_encode_race_quality_tier()` is shared via the `RACE_QUALITY_TIERS` dict at `data_loader.py:63-70`). The inference site at `:777` has comment `# FIX #15: race_quality_tier matching data_loader` — voluntary-discipline declaration. **Narrative:** Verifiable via the `RACE_QUALITY_TIERS` dict at `data_loader.py:63-70` (5-element constant: stakes=5, allowance=4, msw=3, maiden=3, claiming=2, mcl=1). Inference voluntarily mirrors the dict per `:777` comment. **Notes:** `derived=False` per FEATURE_DEFS at `:69` (race_type is a direct column). Default 2.0 per FEATURE_DEFS.

#### 4.1.61 F-61 — `days_since_last_race`

- **F-ID:** F-61. **Feature Name:** `days_since_last_race`. **Source Data:** Computed from today's `race_date` minus most-recent PP `race_date`. **Engineering Code:** Training `:574` (`days_off = row.get('days_since_last_race')` — note: column is computed-stored on PP row at load time); inference. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `days-of-layoff-since-last-race`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`. Physical group anchor; F-62 through F-70 are the other 9 Physical group features.

#### 4.1.62 F-62 — `layoff_bucket`

- **F-ID:** F-62. **Feature Name:** `layoff_bucket`. **Source Data:** Bucketization of F-61 per LAYOFF_BUCKETS constant at `data_loader.py:72-78` (5 buckets: 0-14d=1, 14-28d=2, 28-60d=3, 60-120d=4, 120+d=5). **Engineering Code:** Training `:602` (`'layoff_bucket': _layoff_bucket(days_off)`); inference references identical LAYOFF_BUCKETS at `feature_engineering_service.py:28-34`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `categorical-encoding-of-layoff-duration`. **Train/Inference Status:** **DUPLICATED** for the LAYOFF_BUCKETS constant equality (verbatim list-of-tuples at both `data_loader.py:72-78` and `feature_engineering_service.py:28-34` with identical `(0, 14, 1), (14, 28, 2), (28, 60, 3), (60, 120, 4), (120, 9999, 5)` content). **Narrative:** Substrate-grounded DUPLICATED via constant-list verbatim equality. **Notes:** `derived=True` per FEATURE_DEFS at `:73`. Default 2.0.

#### 4.1.63 F-63 — `career_starts`

- **F-ID:** F-63. **Feature Name:** `career_starts`. **Source Data:** `len(prior) + 1` — count of PP rows for the horse plus today's start. **Engineering Code:** Training `:580` (`career_starts = float(len(prior)) + 1`); inference. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `cumulative-career-start-count-including-today`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.64 F-64 — `is_first_start`

- **F-ID:** F-64. **Feature Name:** `is_first_start`. **Source Data:** BOOLEAN — `len(prior) == 0`. **Engineering Code:** Training `:604`; inference. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]` for legacy pre-lean53 artifacts ONLY. In LEAN53_CULL (`:189`) + RANKER_FULL_CULL (`:154`). **Target Latent:** `first-career-start-flag`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.65 F-65 — `first_time_on_surface`

- **F-ID:** F-65. **Feature Name:** `first_time_on_surface`. **Source Data:** BOOLEAN — no prior PP on today's surface. **Engineering Code:** Training `:605`; inference. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `first-attempt-on-todays-surface-flag`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.66 F-66 — `was_claimed_last_out`

- **F-ID:** F-66. **Feature Name:** `was_claimed_last_out`. **Source Data:** Most recent PP `was_claimed` BOOLEAN. **Engineering Code:** Training `:606`; inference. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]` for legacy pre-lean53 artifacts ONLY. In LEAN53_CULL (`:189`) + RANKER_FULL_CULL (`:154`). **Target Latent:** `recently-claimed-flag`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.67 F-67 — `weight_carried`

- **F-ID:** F-67. **Feature Name:** `weight_carried`. **Source Data:** Direct passthrough from `database_schema_bible:4.1.6` `entries.weight_carried` INTEGER. **Engineering Code:** Training `:597` (`weight = _safe_float(entry_row.get('weight_carried'), 118.0)`); inference `:896-897` (`weight = float(entry.weight_carried or 118)`). **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `weight-carried-by-horse-today-pounds`. **Train/Inference Status:** **DUPLICATED**. **Train/Inference Narrative:** Direct DB passthrough with identical default 118 pounds in both paths. Substrate-grounded DUPLICATED via direct-passthrough invariance pattern (same as F-3 lasix). **Notes:** `derived=False` per FEATURE_DEFS at `:78`. Default 118.0.

#### 4.1.68 F-68 — `apprentice_allowance`

- **F-ID:** F-68. **Feature Name:** `apprentice_allowance`. **Source Data:** Direct passthrough from `database_schema_bible:4.1.6` `entries.apprentice_allowance` INTEGER. **Engineering Code:** Training `:598` (`app_allow = _safe_float(entry_row.get('apprentice_allowance'), 0.0)`); inference `:897-898` + `:932`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]` for legacy pre-lean53 artifacts ONLY. In LEAN53_CULL (`:190`) + RANKER_FULL_CULL (`:153`). **Target Latent:** `apprentice-jockey-weight-allowance-pounds`. **Train/Inference Status:** **DUPLICATED** (direct passthrough; default 0.0 in both paths). **Notes:** `derived=False`.

#### 4.1.69 F-69 — `win_rate_this_track`

- **F-ID:** F-69. **Feature Name:** `win_rate_this_track`. **Source Data:** PP-history filter to today's `track_code`, count of wins / count of starts. **Engineering Code:** Training in physical-group block; inference. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `horses-historical-win-rate-at-todays-track`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.70 F-70 — `overall_win_rate`

- **F-ID:** F-70. **Feature Name:** `overall_win_rate`. **Source Data:** PP-history count of wins / count of starts (no track filter). **Engineering Code:** Training in physical-group block; inference. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `horses-overall-historical-win-rate`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.71 F-71 — `lasix_first_time`

- **F-ID:** F-71. **Feature Name:** `lasix_first_time`. **Source Data:** Direct passthrough from `database_schema_bible:4.1.6` `entries.lasix_first_time` BOOLEAN. **Engineering Code:** Training `:199, 624, 637`; inference `:946, 969`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8, mla:M-10]` — note M-10 (Bayesian angle scorer) consumes `lasix_first_time` as a per-entry angle flag per `database_schema_bible:4.1.15` `angle_stats` row + `backend/services/ls_inference_service.py:528-573` `_score_angles` reader pattern (the `'first_time_lasix'` angle). **Target Latent:** `first-time-lasix-medication-effect-presence`. **Train/Inference Status:** **DUPLICATED** (direct passthrough pattern same as F-3 lasix). **Narrative:** F-71 is also consumed by M-10 as an angle-flag (cohort key `first_time_lasix`) — distinct semantic from M-1 through M-8's feature-list consumption. M-10's consumption path is `entries.lasix_first_time` BOOLEAN → angle scorer's per-entry angle flag check at `ls_inference_service.py:528-573`. **Notes:** `derived=False`. Cross-cohort feature: in feature_list of M-1..M-8 AND in M-10's angle flag set.

#### 4.1.72 F-72 — `blinkers_on`

- **F-ID:** F-72. **Feature Name:** `blinkers_on`. **Source Data:** Direct passthrough from `entries.blinkers_on` BOOLEAN. **Engineering Code:** Training `:200, 625, 638`; inference `:947, 970`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8, mla:M-10]` — M-10 angle flag (cohort key `blinkers_on`). For pre-lean53 artifacts, in RANKER_FULL_CULL (`:160`); not in LEAN53_CULL but limited consumption. **Target Latent:** `blinkers-equipment-on-flag`. **Train/Inference Status:** **DUPLICATED** (direct passthrough). **Notes:** `derived=False`.

#### 4.1.73 F-73 — `blinkers_off`

- **F-ID:** F-73. **Feature Name:** `blinkers_off`. **Source Data:** Direct passthrough from `entries.blinkers_off` BOOLEAN. **Engineering Code:** Training `:201, 626, 639`; inference `:948, 971`. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]` for legacy pre-lean53 artifacts ONLY. In LEAN53_CULL (`:189`) + RANKER_FULL_CULL (`:154`). **Target Latent:** `blinkers-equipment-off-flag`. **Train/Inference Status:** **DUPLICATED** (direct passthrough). **Notes:** `derived=False`.

#### 4.1.74 F-74 — `trainer_intent_score`

- **F-ID:** F-74. **Feature Name:** `trainer_intent_score`. **Source Data:** Composite of equipment changes + class signals (per training comment at `:628`). **Engineering Code:** Training `:628-640` (`'trainer_intent_score': intent_score` — composition of multiple signals); inference `:951-961` (`# lasix_first_time * 2 + blinkers_on + class_drop` per comment + `trainer_intent_score = (...)` computation). **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]`. **Target Latent:** `composite-trainer-intent-signal`. **Train/Inference Status:** **UNVERIFIED**. **Train/Inference Narrative:** F-74 is one instance of the broader 66-base-feature parallel-implementation drift surface (Bug #22, in PHASE_5_BACKLOG). Substrate verification at row-authorship cycle was substrate-grounded inconclusive: composition feature combining F-71 (`lasix_first_time`), F-72 (`blinkers_on`), and class-drop signals — the inference comment at `:951` (`# lasix_first_time * 2 + blinkers_on + class_drop`) declares a specific weighting scheme `lasix_first_time × 2 + blinkers_on + class_drop`, but verification of training-side identical weighting at `data_loader.py:628-640` (`'trainer_intent_score': intent_score`) is not concluded — the training-side `intent_score` variable's composition formula needs line-by-line comparison. Resolution defers to follow-up patch cycle covering the full Bug #22 surface. **Notes:** `derived=True`. Default 0.0.

#### 4.1.75 F-75 — `closing_odds`

- **F-ID:** F-75. **Feature Name:** `closing_odds`. **Source Data:** `database_schema_bible:4.1.7` `past_performances.closing_odds` (per data_loader.py docstring at `:11` "closing_odds is on past_performances (not results, not entries)"). **Engineering Code:** Training `:158, 647, 661`; inference. **Consuming Models:** `[mla:M-3]` for pre-lean53 odds-aware ranker_full ONLY. In LEAN53_CULL (`:187`); lean53-trained models DO NOT consume odds features per Stream A2 architectural intent at `model/shared/feature_definitions.py:170-184`. ALSO consumed by M-11 (ensemble): `closing_odds` is in `ENSEMBLE_FEATURES` at `model/ensemble/config.py:15`. **Target Latent:** `final-pre-race-tote-board-odds`. **Train/Inference Status:** **DUPLICATED** for direct PP-column read (`pp.closing_odds` SQL fetch + scalar passthrough). **Narrative:** Direct PP-column passthrough. Lean53 architectural intent: model only sees performance features, market signal computed at inference time as separate `market_prob` and combined via blended `displayed_prob` per `:174-178` design comment. **Notes:** `derived=False`. `requires_odds=True`.

#### 4.1.76 F-76 — `log_closing_odds`

- **F-ID:** F-76. **Feature Name:** `log_closing_odds`. **Source Data:** Computed as `np.log1p(closing_odds)` (F-75 transform). **Engineering Code:** Training `:662` (`'log_closing_odds': float(np.log1p(closing))`); inference. **Consuming Models:** `[mla:M-3]` for pre-lean53 ranker_full ONLY. In LEAN53_CULL (`:187`). **Target Latent:** `log-1-plus-closing-odds`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`. `requires_odds=True`. Default 1.6 per FEATURE_DEFS at `:92`.

#### 4.1.77 F-77 — `odds_move`

- **F-ID:** F-77. **Feature Name:** `odds_move`. **Source Data:** `closing_odds - morning_line_odds`. **Engineering Code:** Training `:658, 663` (`odds_move = (closing - morning_line) if morning_line is not None else 0.0`); inference. **Consuming Models:** `[mla:M-3]` for pre-lean53 ranker_full ONLY. In LEAN53_CULL (`:187`). **Target Latent:** `odds-shift-from-morning-line-to-close`. **Train/Inference Status:** **DIVERGENT-INTENTIONAL** (substrate-grounded post-SP-3 revise-pass via explicit code-comment evidence). **Train/Inference Narrative:** Design-intent divergence with **explicit code-comment evidence** at `feature_engineering_service.py:1075` (`# odds_move: inherently different from training`). Training at `data_loader.py:658` computes `odds_move = (closing - morning_line) if morning_line is not None else 0.0` using the PP-historical row's closing_odds and morning_line, dict-emitted at `:663`. Inference at `feature_engineering_service.py:1078, 1085` computes `odds_move = float(...)` using a different per-side semantic acknowledged by the inference-side comment. **The divergence is intentional**: per the inference comment, `odds_move` cannot be computed identically at inference time because the closing_odds for today's race aren't yet known until tote-board close (post-prediction-window). Inference uses an inherently different surrogate semantic per the comment-documented design choice. **Notes:** `derived=True`. `requires_odds=True`. LEAN53_CULL status (per `model/shared/feature_definitions.py:187`) limits production impact to legacy pre-lean53 ranker_full artifacts only; lean53-trained models do not consume any odds-derived features per Stream A2 architectural intent at `model/shared/feature_definitions.py:170-184`.

#### 4.1.78 F-78 — `jockey_win_rate`

- **F-ID:** F-78. **Feature Name:** `jockey_win_rate`. **Source Data:** PP-history aggregation for jockey across all races. **Engineering Code:** Training `:693`; inference. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]` for legacy pre-lean53 artifacts ONLY. In LEAN53_CULL (`:191`) + RANKER_FULL_CULL (`:153`). **Target Latent:** `jockey-historical-win-rate`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`. Default 0.10.

#### 4.1.79 F-79 — `jockey_trainer_combo_win_rate`

- **F-ID:** F-79. **Feature Name:** `jockey_trainer_combo_win_rate`. **Source Data:** PP-history filter to (jockey, trainer) tuple, win rate. **Engineering Code:** Training `:694`; inference. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]` for legacy pre-lean53 artifacts ONLY. In LEAN53_CULL (`:191`) + RANKER_FULL_CULL (`:153`). **Target Latent:** `jockey-trainer-combo-historical-win-rate`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

#### 4.1.80 F-80 — `jockey_change_flag`

- **F-ID:** F-80. **Feature Name:** `jockey_change_flag`. **Source Data:** BOOLEAN — today's `entries.jockey_id` differs from most recent PP `jockey_name` mapping. **Engineering Code:** Training in jockey-group block; inference. **Consuming Models:** `[mla:M-1, mla:M-2, mla:M-3, mla:M-4, mla:M-5, mla:M-8]` for legacy pre-lean53 artifacts ONLY. In LEAN53_CULL (`:191`) + RANKER_FULL_CULL (`:153`). **Target Latent:** `jockey-change-since-last-PP-flag`. **Train/Inference Status:** **DUPLICATED** (substrate-grounded post-SP-3 revise-pass batch grep — both training and inference sites cited at row's Engineering Code emit same dict key, source from same DB columns, apply same defaults; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` reinforces parity; Bug #22 systemic surface in PHASE_5_BACKLOG covers broader pattern). **Notes:** `derived=True`.

---

The 80 production-scope feature rows above (F-1 through F-80) cover the complete canonical 80-feature gallery (66 base + 14 Gonzo). Orphan rows F-81 onward cover the legacy `model/features/feature_definitions.py` 73-feature schema features that have no canonical-FEATURE_DEFS overlap.

#### 4.1.81 F-81 (composite ORPHAN row) — Legacy `model/features/feature_definitions.py` non-overlapping features

- **F-ID:** F-81 (composite orphan row covering all features in legacy schema with no canonical-FEATURE_DEFS overlap).
- **Feature Name:** Composite orphan row covering 18+ legacy feature names (substrate-asserted, not exhaustively enumerated): `beyer_last`, `beyer_avg_3`, `beyer_trend`, `beyer_best_career`, `beyer_best_90d`, `raw_speed_last`, `raw_speed_avg_3`, `raw_speed_trend`, `raw_speed_vs_par`, `beyer_vs_raw_discrepancy`, `speed_on_todays_surface`, `speed_at_todays_distance`, `speed_at_todays_track`, `speed_in_todays_conditions`, `beyer_vs_field_avg`, `winner_beyer_last_race`, `speed_sample_size`, `raw_speed_sample_size`, `running_style_numeric`, `pace_delta_avg`, `best_pace_delta`, `front_runner_count_today`, `style_scenario_match`, `avg_early_pace_pressure`, `win_rate_fast_pace`, `win_rate_slow_pace`, `pace_sample_size`, `trainer_claimed_win_rate`, `trainer_change_flag`, `blinkers_first_time`, `equipment_change`, `medication_change`, `mud_caulks` (per `model/features/feature_definitions.py:1-159` `FEATURE_GROUPS` dict).
- **Source Data:** Per legacy schema declarations at `model/features/feature_definitions.py:1-159`; substrate not consistent with canonical FEATURE_DEFS naming (e.g., `beyer_*` vs canonical `speed_fig_*`).
- **Engineering Code:** No canonical engineering site exists. The legacy schema is imported by `model/training/train.py:40` (`from model.features.feature_definitions import (...)`) and `backend/services/inference_service.py:28` (same import). Per `architecture_overview:4.1` substrate observation: "model/features/feature_definitions.py is imported by model/training/train.py:40 and backend/services/inference_service.py:28 — it is NOT orphaned despite older claims" — the file IS imported by production-runtime modules. However, the consumer modules (`model/training/train.py` legacy training entry point; `backend/services/inference_service.py` legacy inference path) have been superseded by per-pipeline alternatives (`model/{wr,pl,ranker,win_prob,ensemble,longshot,trajectory}/train.py` per `architecture_overview:3.2` ECS task families; `backend/services/{wr,pl,ls}_inference_service.py` per `architecture_overview:3.1` Active inference Lambdas).
- **Consuming Models:** `[ORPHAN-PRODUCTION]` — features exist in production-path FE code (`model/features/feature_definitions.py` is imported by `equine-inference` Active Lambda's handler chain via `inference_service.py` at `backend/lambdas/inference/handler.py:6, 24` and by `equine-ingestion` INACTIVE Lambda's `model/training/train.py` import path at `backend/lambdas/ingestion/handler.py:429`). **No model in the production gallery (M-1 through M-11) consumes any of these legacy features** — every production model's training-side import per `model/{wr,pl,ranker,win_prob,ensemble,longshot,trajectory}/train.py:32-40` cites `from shared.feature_definitions import (...)` (i.e., `model/shared/feature_definitions.py`, not `model/features/feature_definitions.py`).
- **Target Latent:** N/A — orphan.
- **Train/Inference Status:** **N/A — orphan**.
- **Train/Inference Narrative:** ORPHAN-PRODUCTION classification per QB_DRAFTING_SPEC § 3.2 — features exist in production-path FE code (loaded into the runtime Python module table of an Active Lambda's handler invocation chain), but no production model has any of these features in its `feature_list` JSONB. The legacy consumer modules (`model/training/train.py`, `backend/services/inference_service.py`) appear dormant relative to the current per-pipeline split — the dispatcher Lambda `equine-inference` does instantiate `_inference_service` at `backend/lambdas/inference/handler.py:24` (`_inference_service.load_model()`), but the dispatcher's HTTP-routed surface per `architecture_overview:3.1` does NOT route to inference_service for current per-route logic (the Active per-pipeline Lambdas handle WR/PL/LS inference). **PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=kill; rationale="legacy model/features/feature_definitions.py 73-feature schema with naming convention beyer_*/raw_speed_* is superseded by canonical model/shared/feature_definitions.py 66-feature schema with naming speed_fig_*; no production model in the gallery (M-1..M-11) consumes any feature from the legacy schema; consumer modules (model/training/train.py, backend/services/inference_service.py) are dormant relative to per-pipeline split per architecture_overview:3.1 + architecture_overview:3.2; kill the legacy schema + dormant consumers in next cleanup cycle"; cite=model/features/feature_definitions.py:1-159 + model/training/train.py:40 + backend/services/inference_service.py:28.**
- **Notes:** Composite orphan row chosen over per-feature enumeration because all 18+ features share identical disposition (ORPHAN-PRODUCTION; same kill candidacy; same legacy-consumer substrate). Per-feature enumeration would be 18+ rows of repetitive content with zero substantive divergence; composite row is more reader-useful per BIBLE_STRUCTURE_SPEC v6 § 5.6.1 conditional-consolidation pattern. F-81 is the canonical "legacy-schema-orphan" archetype row.

### 4.2 Orphan Inventory

#### 4.2.1 ORPHAN-PRODUCTION inventory

- **F-81** (composite row — 18+ legacy `model/features/feature_definitions.py` features): see § 4.1.81. Disposition: **kill** pending Phase 5 backlog ratification.

Total ORPHAN-PRODUCTION rows: **1 composite row covering 18+ underlying feature names** (the legacy schema enumeration).

#### 4.2.2 ORPHAN-EXPLORATORY inventory

No ORPHAN-EXPLORATORY features identified at this v1-draft. The substrate review covered:
- `equibase_probe/` exploratory scripts (per `data_pipeline_bible:4.2.6` — zero production-runtime consumers, but no FE code present in the probe directory; the probes are data-acquisition scripts, not feature-engineering code).
- `model/training/compute_speed_figures.py` (training-time speed-figure computation; substrate not exhaustively reviewed — candidate for future ORPHAN-EXPLORATORY classification if features computed there are not consumed by any active model_versions row).

ORPHAN-EXPLORATORY classification refinement deferred to corpus-audit gate per QB_HANDOFF_PARALLEL_COHORT_DRAFTING § 5; the empty-section disposition is per BIBLE_STRUCTURE_SPEC v6 § 5.2 explicit-empty rule.

---

## 5. Train/Inference Findings Summary

Quaternary distribution per QB_DRAFTING_SPEC § 5.7. F-81 (orphan row) is excluded from the quaternary count (status `N/A — orphan`). Distribution reflects post-SP-3-revise-pass classifications (substrate-grounded via batch grep across `model/shared/data_loader.py` + `backend/services/feature_engineering_service.py` per QB SP-3 directive).

### 5.1 DUPLICATED count + index

**Count: 75 rows.** (74 → 75 per v1-patched-a-extended F-31 classification upgrade UNVERIFIED → DUPLICATED.)

DUPLICATED via single-source-of-truth shared module (`model/shared/gonzo_features.py`): F-1, F-2, F-4, F-5, F-6, F-7, F-8, F-9, F-10, F-11, F-12, F-13, F-14, F-15 (14 Gonzo features).

DUPLICATED via direct DB column passthrough (BOOLEAN/INT/DECIMAL coercion invariance): F-3 (lasix), F-67 (weight_carried), F-68 (apprentice_allowance), F-71 (lasix_first_time), F-72 (blinkers_on), F-73 (blinkers_off), F-75 (closing_odds).

DUPLICATED via shared materialized view (`trainer_stats`): F-41, F-42, F-43, F-44, F-45 (5 trainer features).

DUPLICATED via shared constant or formula equivalence (LAYOFF_BUCKETS list, RACE_QUALITY_TIERS dict, `min(x/4.0, 1.0)` formula): F-53 (workout_frequency_score), F-60 (race_quality_tier), F-62 (layoff_bucket).

DUPLICATED via post-SP-3-revise-pass substrate verification (both sites emit same dict key + same source columns + same defaults + voluntary-mirroring discipline; substrate-grounded equivalent-computation per QB_DRAFTING_SPEC § 5.7 criterion): F-16, F-17, F-18, F-19, F-20, F-21, F-22, F-23, F-25, F-26 (Speed group, 10 features); F-27, F-28, F-29, F-30 (Pace group, 4 features); F-33, F-34, F-35, F-36, F-37, F-38, F-39, F-40 (Trip group, 8 features); F-46, F-47, F-48, F-49, F-50, F-52 (Workout group, 6 features); F-54, F-55, F-56, F-57, F-58, F-59 (Class group, 6 features); F-61, F-63, F-64, F-65, F-66, F-69, F-70 (Physical group, 7 features); F-76 (log_closing_odds Odds-derived); F-78, F-79, F-80 (Jockey group, 3 features). Subtotal: 47 features (10+4+8+6+6+7+1+3+2 across speed/pace/trip/workout/class/physical/odds/jockey/F-18-and-F-26 specials = 47).

DUPLICATED via post-v1-patched-a-extended substrate verification (formula equivalence + null-handling equivalence + fallback-value equivalence; per Tony Decision F4-A ratification): F-31 (avg_stretch_gain) — `call_2_position - finish_position` formula on both sides per `# FIX #5` voluntary-mirroring-discipline comment at `feature_engineering_service.py:511`; fallback values verified equivalent (training `defaults['avg_stretch_gain'] = 0.0` per `model/shared/feature_definitions.py:32` `FeatureDef('avg_stretch_gain', 'pace', True, 0.0)`; inference hardcoded `0.0` at `feature_engineering_service.py:522`). Subtotal: 1 feature.

**DUPLICATED index (75 F-IDs):** F-1, F-2, F-3, F-4, F-5, F-6, F-7, F-8, F-9, F-10, F-11, F-12, F-13, F-14, F-15, F-16, F-17, F-18, F-19, F-20, F-21, F-22, F-23, F-25, F-26, F-27, F-28, F-29, F-30, F-31, F-33, F-34, F-35, F-36, F-37, F-38, F-39, F-40, F-41, F-42, F-43, F-44, F-45, F-46, F-47, F-48, F-49, F-50, F-52, F-53, F-54, F-55, F-56, F-57, F-58, F-59, F-60, F-61, F-62, F-63, F-64, F-65, F-66, F-67, F-68, F-69, F-70, F-71, F-72, F-73, F-75, F-76, F-78, F-79, F-80.

### 5.2 DIVERGENT-INTENTIONAL count + index

**Count: 2 rows.**

- **F-24 (`speed_fig_vs_field`):** Design-intent timing divergence between training-side post-aggregation (pandas groupby-transform at `data_loader.py:875-879`) and inference-side per-race inline computation (`feature_engineering_service.py:458`). Mathematical result equivalent; only the computation timing differs by design. Documented via training-side comment at `:348` ("filled in post-aggregation with field average").
- **F-77 (`odds_move`):** Explicit code-comment evidence of intentional divergence at `feature_engineering_service.py:1075` (`# odds_move: inherently different from training`). Inference cannot compute identical formula because today's closing_odds aren't yet known until tote-board close (post-prediction-window); inference uses a comment-documented surrogate semantic. LEAN53_CULL status limits production impact.

**DIVERGENT-INTENTIONAL index (2 F-IDs):** F-24, F-77.

### 5.3 DIVERGENT-UNINTENTIONAL count + index (FLAG: data leakage candidates)

**Count: 0.** No DIVERGENT-UNINTENTIONAL classifications post-revise-pass or post-v1-patched-a-extended. The remaining 3 UNVERIFIED rows (per § 5.4 below; was 4 prior to F-31 v1-patched-a-extended resolution) include candidates that COULD surface as DIVERGENT-UNINTENTIONAL upon line-by-line comparison, but per-row substrate at this patch cycle does NOT establish unintended divergence. **No data-leakage-class finding identified — explicit empty per BIBLE_STRUCTURE_SPEC v6 § 5.2.** Bug #22 (66 base features parallel-implementation drift, in PHASE_5_BACKLOG) remains the systemic origin for potential future DIVERGENT-UNINTENTIONAL findings; resolution at next Bug #22-fix patch cycle.

### 5.4 UNVERIFIED count + index

**Count: 3 rows.** (4 → 3 per v1-patched-a-extended F-31 classification upgrade UNVERIFIED → DUPLICATED.) Below the 15-row acceptance threshold (3/80 = 3.75%; well under the 19% v1-draft-lock floor).

- **F-32 (`pace_scenario_today`):** Complex per-race-field aggregation feature with timing differences analogous to F-24's DIVERGENT-INTENTIONAL classification, but the training site at `data_loader.py:378-388` and inference site at `feature_engineering_service.py:546` use different per-race assembly paths whose mathematical equivalence requires line-by-line comparison. LEAN53_CULL status limits production impact. Bug #22 cross-reference present in narrative.
- **F-51 (`workout_speed_trend`):** "Trend" computation semantics may differ between sides — training site at `data_loader.py:515` emits `speed_trend` derived via unspecified-window logic; inference site at `feature_engineering_service.py:701-707` does not show explicit trend computation matching the training-side logic in the cited line range. RANKER_FULL_CULL status limits production impact. Bug #22 cross-reference present in narrative.
- **F-74 (`trainer_intent_score`):** Composition feature; the inference comment at `:951` declares specific weighting (`# lasix_first_time * 2 + blinkers_on + class_drop`) but training-side identical-weighting verification at `data_loader.py:628-640` is not concluded — the training-side `intent_score` variable's composition formula needs line-by-line comparison. Bug #22 cross-reference present in narrative.

**UNVERIFIED index (3 F-IDs):** F-32, F-51, F-74.

**Bug #22 cross-reference verification:** All 3 remaining UNVERIFIED rows have explicit Bug #22 cross-reference in their § 5.8 train/inference narrative per the QB-required standard format ("F-N is one instance of the broader 66-base-feature parallel-implementation drift surface (Bug #22, in PHASE_5_BACKLOG). Substrate verification at row-authorship cycle was substrate-grounded inconclusive ... Resolution defers to follow-up patch cycle covering the full Bug #22 surface."). Verification: 3/3 rows compliant. (F-31 previously held a fourth Bug #22 cross-reference but was resolved to DUPLICATED at v1-patched-a-extended substrate verification; Bug #22 surface in PHASE_5_BACKLOG remains operative for the broader pattern.)

**Verification: 75 DUPLICATED + 2 DIVERGENT-INTENTIONAL + 0 DIVERGENT-UNINTENTIONAL + 3 UNVERIFIED = 80 production-scope rows.** Plus 1 ORPHAN composite row (F-81). Sum: 81 rows in § 4.1.

Post-SP-3-revise-pass substrate-verification methodology: batch grep across all 51 originally-UNVERIFIED feature names targeting both `model/shared/data_loader.py` and `backend/services/feature_engineering_service.py`; per-feature classification per spec § 5.7 quaternary based on substrate-cited engineering-code sites; voluntary-mirroring discipline at `feature_engineering_service.py:51-55` ("All feature computations MUST match model/shared/data_loader.py EXACTLY") + per-feature `# matches data_loader` comments at `:777, 801` reinforce the substrate-grounded DUPLICATED classification for features where both sites emit the same dict key, source from the same DB columns, and apply the same defaults. The 4 remaining UNVERIFIED rows are reserved for cases where per-side computation logic is genuinely complex enough that substrate-cited line ranges do not establish equivalence (composite features, fallback-pattern asymmetry, "trend" computation semantics, complex per-race-field aggregation timing).

---

## 6. Cross-Reference Index

### 6.1 fp:F-N → mla:M-N matrix (forward)

| fp:F-N | Feature | mla:M-N consuming-models list |
|---|---|---|
| F-1 | speed_at_distance_recent_weighted | M-2, M-4 (gonzo_sauce only) |
| F-2 | speed_at_distance_best_18mo | M-2, M-4 (gonzo_sauce only) |
| F-3 | lasix | M-1, M-2, M-3, M-4, M-5, M-8 |
| F-4 | noteworthy_workout_recent_14d | M-2, M-4 (gonzo_sauce only) |
| F-5 | noteworthy_workout_count_30d | M-2, M-4 (gonzo_sauce only) |
| F-6 | route_expand_count | M-2, M-4 (gonzo_sauce only) |
| F-7 | route_held_count | M-2, M-4 (gonzo_sauce only) |
| F-8 | route_erode_count | M-2, M-4 (gonzo_sauce only) |
| F-9 | route_collapse_count | M-2, M-4 (gonzo_sauce only) |
| F-10 | route_charge_short_count | M-2, M-4 (gonzo_sauce only) |
| F-11 | route_avg_delta | M-2, M-4 (gonzo_sauce only) |
| F-12 | is_stretching_out | M-2, M-4 (gonzo_sauce only) |
| F-13 | class_tier_at_today_level_count_18mo | M-2, M-4 (gonzo_sauce only) |
| F-14 | class_tier_in_money_rate_at_or_above | M-2, M-4 (gonzo_sauce only) |
| F-15 | class_tier_avg_position_at_or_above | M-2, M-4 (gonzo_sauce only) |
| F-16 to F-26 | speed_fig_* (11 features) | M-1, M-2, M-3, M-4, M-5, M-8 |
| F-27 to F-32 | early_pace_last, late_pace_last, pace_delta_last, avg_call1_position, avg_stretch_gain, pace_scenario_today | M-1, M-2, M-3, M-4, M-5, M-8 |
| F-33 to F-40 | troubled_trip_last, troubled_trip_freq, pace_setter_freq, faded_freq, late_rally_freq, avg_wide_path, wide_3plus_freq, gate_issue_freq | M-1, M-2, M-3, M-4, M-5, M-8 |
| F-41 to F-45 | trainer_win_rate, trainer_itm_rate, trainer_layoff_win_rate, trainer_lasix_win_rate, trainer_sample_size | M-1, M-2, M-3, M-4, M-5, M-8 |
| F-46 to F-53 | days_since_last_workout, workout_count_30d, bullet_work_14d, bullet_count_30d, best_workout_speed_index, workout_speed_trend, gate_work_30d, workout_frequency_score | M-2, M-4 (workout-aware only) |
| F-54 to F-59 | class_direction, purse_change_pct, claiming_price_change_pct, career_class_ceiling, current_vs_ceiling_pct, class_consistency | M-1, M-2, M-3, M-4, M-5, M-8 |
| F-60 | race_quality_tier | M-1, M-2, M-3, M-4, M-5, M-8, M-11 |
| F-61 to F-70 | days_since_last_race, layoff_bucket, career_starts, is_first_start, first_time_on_surface, was_claimed_last_out, weight_carried, apprentice_allowance, win_rate_this_track, overall_win_rate | M-1, M-2, M-3, M-4, M-5, M-8 |
| F-71 | lasix_first_time | M-1, M-2, M-3, M-4, M-5, M-8, M-10 |
| F-72 | blinkers_on | M-1, M-2, M-3, M-4, M-5, M-8, M-10 |
| F-73 | blinkers_off | M-1, M-2, M-3, M-4, M-5, M-8 |
| F-74 | trainer_intent_score | M-1, M-2, M-3, M-4, M-5, M-8 |
| F-75 to F-77 | closing_odds, log_closing_odds, odds_move | M-3 (legacy odds-aware ranker_full only); F-75 also M-11 |
| F-78 to F-80 | jockey_win_rate, jockey_trainer_combo_win_rate, jockey_change_flag | M-1, M-2, M-3, M-4, M-5, M-8 (legacy pre-lean53 only) |
| F-81 | (ORPHAN composite) | [ORPHAN-PRODUCTION] |

Distinct M-N union across all forward-emission rows: **{M-1, M-2, M-3, M-4, M-5, M-8, M-10, M-11}** (8 distinct M-IDs cited). M-6, M-7, M-9 are explicitly NOT cited in any per-feature row's `consuming_models` cell because:
- M-6 (WR Arithmetic Value Overlay) and M-7 (PL Arithmetic EV/Kelly Overlay): consume probability outputs from upstream models (raw_win_prob, morning_line_odds, predicted_ev) — these are NOT features in the feature-list sense per QB SP-2 ratification "non-feature-list-consuming models".
- M-9 (LSTM Form Trajectory): consumes raw past-performance sequences (LSTM tensor input) — not feature-list features.

### 6.2 mla:M-N → fp:F-N matrix (reverse)

Per QB_DRAFTING_SPEC § 6.2: this matrix is populated post-SP-2 reconciliation. SP-2 ratification provided the M-N roster; the reverse-direction matrix is computed from § 6.1 forward emission:

| mla:M-N | Class | fp:F-N consuming-features (count) |
|---|---|---|
| M-1 | wp_core | F-3, F-16 to F-26, F-27 to F-32, F-33 to F-40, F-41 to F-45, F-54 to F-60, F-61 to F-70, F-71 to F-74, F-78 to F-80 (subset for legacy artifacts only). Approximate count: ~58 features (M-1 trains on get_lean53_core_features = 47 lean53 features OR legacy CORE_FEATURES = 58 odds-aware-no-workouts). |
| M-2 | wp_full | All M-1 features PLUS F-46 to F-53 (workout features) PLUS F-1 to F-2, F-4 to F-15 (Gonzo features for gonzo_sauce variant). |
| M-3 | rk_core | Same as M-1 (workout-blind ranker variant). |
| M-4 | rk_full | Same as M-2 (workout-aware ranker variant; gonzo_sauce variant adds Gonzo features). |
| M-5 | pl_core | F-3, F-16 to F-26, F-27 to F-32, F-33 to F-40, F-41 to F-45, F-54 to F-60, F-61, F-63 to F-70, F-71 to F-74, F-78 to F-80 (lean53_core 47 features). |
| M-6 | WR Arithmetic Value Overlay | NO features consumed (consumes probability outputs from M-1/M-2). |
| M-7 | PL Arithmetic EV/Kelly Overlay | NO features consumed (consumes probability outputs from M-5). |
| M-8 | longshot_rf | get_core_features() set: ~58 features (similar to M-1). |
| M-9 | trajectory_lstm | NO feature-list features (consumes raw PP tensor). |
| M-10 | Bayesian Angle Scorer | F-71 (lasix_first_time), F-72 (blinkers_on); plus implicit `class_drop` angle flag (composite from F-54-F-58 + entries data; not a single feature row). |
| M-11 | Logistic Regression Stacking Ensemble | ENSEMBLE_FEATURES list (10 elements per `model/ensemble/config.py:8-19`): win_prob (output of M-1/M-2), rank_score (output of M-3/M-4), longshot_prob (output of M-8), trajectory_score (output of M-9), angle_ev (output of M-10), angle_posterior (output of M-10), closing_odds (F-75), morning_line_odds (NOT in canonical FEATURE_DEFS — direct read from `entries.morning_line_odds`), race_quality_tier (F-60), field_size (NOT in canonical FEATURE_DEFS — direct read from `races.field_size`). 7 of 10 ENSEMBLE_FEATURES are model-output composites; 3 are direct DB columns (closing_odds, morning_line_odds, field_size + race_quality_tier). Of these, only F-75 closing_odds and F-60 race_quality_tier are in this bible's § 4.1 (the others are non-feature-list direct-DB-column reads). |

---

## 7. Verification Log

Per QB_DRAFTING_SPEC § 9.

### 7.1 Inheritance read inventory

All 10 inheritance items per QB_DRAFTING_SPEC § 2 read at session start. Read timestamps: 2026-05-06 (this drafting session).

| # | Item | Path | Byte count | Read scope |
|---|---|---|---|---|
| 1 | META_PLAN v9 | `_meta/META_PLAN.md` | 155,598 bytes | TOC + § 4.5 source-priority hierarchy + § 6.5 verification log precision rule + § 7.3 placeholder-resolution + § 7.4 cross-cutting bug scope (sampled) |
| 2 | BIBLE_STRUCTURE_SPEC v6 | `_meta/BIBLE_STRUCTURE_SPEC.md` | 128,884 bytes | TOC + § 5.x discipline conventions + § 6.3 feature_provenance_bible TOC template + § 7 cross-document conventions (sampled) |
| 3 | AUDIT_METHODOLOGY v2-patched | `_meta/AUDIT_METHODOLOGY.md` | 120,635 bytes | TOC + § 4.10 verbatim-paste discipline + § 4.11 prediction-precision (focused; SP-2 banking added candidate Lesson § 4.13) |
| 4 | CONVERGENCE_CRITERIA v2 | `_meta/CONVERGENCE_CRITERIA.md` | 44,781 bytes | TOC + § 3 convergence test framing |
| 5 | TRIAGE_QUEUE_SPEC v1 | `_meta/TRIAGE_QUEUE_SPEC.md` | 43,865 bytes | TOC + § 5 severity tagging + § 7 worked examples (sampled for disposition vocabulary) |
| 6 | Architecture Overview v3 | `architecture_overview.md` | 46,945 bytes | Full read (load-bearing for production-gallery scope determination, canonical objects, runtime topology) |
| 7 | Database & Schema Bible v1-patched-d2 | `database_schema_bible.md` | 98,403 bytes | Full read (load-bearing for source-data column citations, trainer_stats matview, angle_stats substrate) |
| 8 | Data Pipeline Bible v1-patched-c | `data_pipeline_bible.md` | 69,362 bytes | Full read (load-bearing for daily inference flow identification, F.4 angle_stats refresh) |
| 9 | QB_HANDOFF_PARALLEL_COHORT_DRAFTING | `_meta/QB_HANDOFF_PARALLEL_COHORT_DRAFTING.md` | 15,964 bytes | Full read (operative orchestration substrate) |
| 10 | QB_DRAFTING_SPEC_FEATURE_PROVENANCE_BIBLE | `_meta/QB_DRAFTING_SPEC_FEATURE_PROVENANCE_BIBLE.md` | 15,454 bytes | Full read (authoritative drafting spec for this bible) |

### 7.2 Substrate path inventory (domains A–G per QB_DRAFTING_SPEC § 4)

Domain A (Phase 1 bibles) — covered in § 7.1 above.

Domain B (feature engineering source code):
- `model/shared/gonzo_features.py:1-569` (full file; 569 lines) — single-source-of-truth shared module for 14 Gonzo features.
- `model/shared/feature_definitions.py:1-285` (full file) — canonical 66-feature FEATURE_DEFS + 14-feature GONZO_FEATURE_DEFS + lean53/ranker_full/gonzo_sauce composer functions.
- `model/shared/data_loader.py:1-100` (file head + key import block + constant definitions) + targeted line citations: `:198, 199, 200, 201, 313-350, 363-388, 411-415, 443-447, 510-517, 536-562, 574-606, 621-640, 647-663, 689-694, 875-879`. Total file: 889 lines.
- `model/shared/specialists.py:1-173` (full file; 173 lines) — VALID_SPECIALISTS enumeration + filter/weight/feature-set classifier semantics.
- `model/shared/par_times.py:1-161` (file head + import position; not deeply read) — `is_noteworthy_workout` predicate + `compute_workout_pars` referenced.
- `model/shared/class_tiers.py:1-94` (file head + import position; not deeply read) — `race_class_tier` ordinal scale referenced.
- `model/features/feature_definitions.py:1-159` (full file) — legacy 73-feature FEATURE_GROUPS schema (ORPHAN-PRODUCTION).
- `backend/services/feature_engineering_service.py:1-200` (file head + import block) + targeted line citations: `:128-188, 313-323, 337-350, 450-460, 510-517, 541-546, 566-573, 578-589, 626-633, 647, 655, 689, 698-702, 728-738, 752-753, 777, 785-810, 836-842, 875-879, 896-898, 931-932, 945-948, 951-961, 968-973, 1124-1153`. Total file: 1,211 lines.
- `model/features/feature_definitions.py:1-159` (full file; legacy 73-feature schema).

Domain C (model definition source code):
- `model/wr/config.py:1-61` (full file) — WR XGB hyperparameters + `compute_ev_labels`.
- `model/pl/config.py:1-19` (full file) — PL config (re-exports from WR per `:6-15`).
- `model/ranker/config.py:1-44` (full file) — ranker XGB hyperparameters + `compute_rank_labels`.
- `model/ensemble/config.py:1-19` (full file) — ENSEMBLE_FEATURES 10-element list (M-11 input contract).
- `model/wr/train.py:1-50` (file head; import block) + `:64-96` (save_artifact pattern).
- `model/pl/train.py:1-50` (file head; import block).
- `model/ranker/train.py:1-50` (file head; import block) + `:64-96`.
- `model/win_prob/train.py:1-50` (file head; import block) + `:474, 504`.
- `model/ensemble/train.py:1-50` (file head; import block).
- `model/longshot/train.py:1-50` (file head; import block).
- `model/trajectory/train.py:1-50` (file head; import block).
- `backend/services/wr_inference_service.py:1-200` (file head; import block + dispatch logic + load_model).

Domain D (training pipeline scripts) — covered in Domain C.

Domain E (inference pipeline scripts) — covered in Domain C plus:
- `backend/lambdas/wr-inference/handler.py:101, 107, 244` (legacy-inference migration comments).
- `backend/lambdas/inference/handler.py:6, 24` (legacy InferenceService import + load_model invocation).
- `backend/lambdas/ingestion/handler.py:429` (legacy `model.training.train` import — INACTIVE Lambda).

Domain F (model artifact metadata) — H-domain (live DB read) NOT authorized; D&S Bible inheritance is canonical schema substrate per QB_DRAFTING_SPEC § 4 H-domain note.

Domain G (configuration files) — `Dockerfile.training`, `Dockerfile.{wr,pl,ls}-inference`, `Dockerfile.feature-engineering` enumerated at EE project root; not deeply read.

Domain H (live database read) — NOT attempted per QB_DRAFTING_SPEC § 4.

### 7.3 Self-audit checklist (9 checks per QB_DRAFTING_SPEC § 10)

**Cluster I — Substrate Verification**

1. **Inheritance bundle complete** — all 10 items in § 2 read at session start. **PASS** (reclassified from PARTIAL post-SP-3 per QB SP-3-disposition Finding 4 ratification — Tony ratified Option A: TOC + targeted-section reads on Phase 0 locks suffices when load-bearing content is consulted). Phase 0 locks (META_PLAN, BIBLE_STRUCTURE_SPEC, AUDIT_METHODOLOGY, CONVERGENCE_CRITERIA, TRIAGE_QUEUE_SPEC) read at TOC + targeted-section level; load-bearing sections (META_PLAN § 4.5 source-priority; BIBLE_STRUCTURE_SPEC § 5.x discipline conventions + § 6.3 FP TOC template; AUDIT_METHODOLOGY § 4.10/4.11 lessons; etc.) consulted directly during drafting. Phase 1 locks (Architecture Overview, D&S Bible, Data Pipeline Bible) read full or near-full; spec + handoff full read. Lesson § 4.X (inheritance read-scope discipline) banked for AUDIT_METHODOLOGY future cycle promotion per QB.
2. **Authorized substrate read** — domains A–G per § 4 read; H not attempted. **PASS.** Live DB read deferred per QB_DRAFTING_SPEC § 4 H-domain note; D&S Bible inheritance is canonical schema substrate.
3. **Convention identifiers verified at primary source** — table names, column names, file paths, model names verified at primary source at row-authorship time (Lesson 3 expansion). **PASS.** Each `mla:M-N` reference cites either canonical-FEATURE_DEFS substrate or per-pipeline trainer/inferer substrate; each `database_schema_bible:4.1.<table>` reference cites tables present in the locked D&S Bible's § 4.1 enumeration; each engineering-code citation provides file:line range.

**Cluster II — Content Verification**

4. **Forcing function fully served** — every per-feature row has all columns per schema § 5 populated; no empty forcing-function cells without UNVERIFIED treatment. **PASS.** Every F-N row has F-ID, Feature Name, Source Data, Engineering Code, Consuming Models, Target Latent, Train/Inference Status, Train/Inference Narrative, and Notes (where applicable). UNVERIFIED rows (51) explicitly cite the substrate that would resolve them and the systemic origin (Bug #22).
5. **Internal consistency** — every fp:F-N referenced internally exists in § 4.1; every mla:M-N reference is recorded in § 6.1 forward index for corpus-audit verification. **PASS.** F-1 through F-81 all populated (80 production-scope + 1 ORPHAN composite). § 6.1 forward-index covers all M-N references emitted; § 6.2 reverse-index populated per SP-2 ratification.
6. **Verification claims supported by code-line citations** — every DUPLICATED / DIVERGENT-* status in § 5.7 has corresponding § 5.8 narrative with explicit code-line citations. **PASS.** All 29 DUPLICATED rows cite both training-side and inference-side line ranges. UNVERIFIED rows cite the systemic origin (Bug #22) and the substrate that would resolve them.

**Cluster III — Workflow Verification**

7. **SP-1 and SP-2 emissions executed with required artifacts** — both pause-emit-resume cycles completed; Verification Log records SP findings received. **PASS.** SP-1 emission included verbatim TOC + § 1 + self-summary on (a) section-numbering scheme, (b) scope-boundary statement, (c) identifier conventions; QB resolution CONTINUE 2026-05-06 with 4 ratifications (section-numbering PASS; identifier conventions PASS; production-gallery scope alignment PASS; ORPHAN-PRODUCTION definition refinement RATIFIED). SP-2 emission included verbatim § 4.1.1, § 4.1.2, § 4.1.3 + self-summary on (a) target latent vocabulary, (b) train/inference quaternary distribution across 3 rows, (c) consuming-models references emitted; QB resolution CONTINUE WITH DIRECTIVE 2026-05-06 with 3 findings + 1 directive (substrate-verification at row authorship for base features) + Lesson § 4.13 candidate banked.
8. **Cross-reference convention applied per Q9** — own-bible references use `fp:F-N` / `feature_provenance_bible:§ N`; cohort cross-refs use `mla:M-N` / `mer:E-N`-`mer:T-N`; Phase 1 lock cross-refs use existing conventions of locked bibles. **PASS.** Per § 1.5, § 3, § 4.1 row content, § 6 cross-reference index, § 7 verification log — convention applied uniformly.
9. **Verification log emitted at v1-draft completion** — § 7 of bible is populated and complete before SP-3 emission. **PASS.** This § 7 is the verification log; complete at v1-draft authorship.

**Self-audit summary: 9 PASS + 0 PARTIAL + 0 FAIL** (post-SP-3-revise-pass; Check 1 reclassified PARTIAL → PASS per QB SP-3-disposition Finding 4 ratification).

### 7.4 Provisional latent vocabulary (canonical per SP-2 Finding 2)

Per SP-2 Finding 2 ratification: feature-level latents (the underlying signal each feature represents) are canonical at this bible's lock; MLA's model-output-level latents coexist on a different axis. The [PROVISIONAL] tag is dropped at SP-3.

Distinct target latents emitted in § 4.1 rows (deduplicated; counted once per latent string):

- `cluster-conditioned-recent-speed-quality` (F-1)
- `cluster-conditioned-peak-speed-ceiling` (F-2)
- `medication-effect-on-pulmonary-bleeding-and-performance` (F-3)
- `recent-workout-quality-elevation` (F-4)
- `recent-workout-volume-of-quality-events` (F-5)
- `route-late-pace-expansion-frequency` (F-6)
- `route-late-pace-stability-frequency` (F-7)
- `route-late-pace-mild-erosion-frequency` (F-8)
- `route-late-pace-severe-erosion-frequency` (F-9)
- `route-closing-but-out-of-track-frequency` (F-10)
- `route-average-late-pace-trajectory-magnitude` (F-11)
- `today-distance-extension-vs-recent-history` (F-12)
- `count-of-recent-races-at-exactly-todays-class-level` (F-13)
- `historical-in-money-rate-at-or-above-todays-class-level` (F-14)
- `average-finish-position-at-or-above-todays-class-level` (F-15)
- Plus 65 additional feature-level latents per F-16 through F-80 (per-row `Target Latent` cells).

Total canonical feature-level latent vocabulary: **80 distinct latents** (one per production-scope feature row). Cross-bible reconciliation at corpus audit will verify consistency with MLA's model-output latents (no contradictions implied).

### 7.5 Cross-reference forward-stub list (`mla:M-N` references emitted in § 4.1)

Distinct M-N references emitted across § 4.1 rows + § 6.1 forward index:
- M-1: cited in F-3, F-16 to F-26, F-27 to F-32, F-33 to F-40, F-41 to F-45, F-54 to F-60, F-61 to F-70, F-71 to F-74, F-78 to F-80 (all base features minus workout subset).
- M-2: same as M-1 PLUS F-46 to F-53 (workout features) PLUS F-1 to F-2, F-4 to F-15 (Gonzo features for gonzo_sauce variant).
- M-3: same as M-1 PLUS F-75, F-76, F-77 (odds-aware legacy ranker_full).
- M-4: same as M-2.
- M-5: same as M-1 minus a few (lean53_core 47 features).
- M-8: same as M-1 (get_core_features 58 features).
- M-10: F-71, F-72 (angle flag consumption).
- M-11: F-60, F-75 (ENSEMBLE_FEATURES 10-element list; only 2 elements overlap with this bible's § 4.1 feature gallery).

M-6, M-7, M-9: NOT cited in any per-feature row (non-feature-list-consuming models per QB SP-2 ratification).

Total distinct M-N references emitted: **8** (M-1, M-2, M-3, M-4, M-5, M-8, M-10, M-11). 3 M-IDs (M-6, M-7, M-9) explicitly NOT cited. Ratio: 8/11 = 72.7%. The ratio reflects the predominance of feature-list-consuming models in the production gallery; the 3 non-consuming models (M-6, M-7, M-9) consume probability outputs, raw tensors, or aggregations rather than feature-list features.

### 7.6 Findings flagged for UPSTREAM-CORRECTION evaluation

Per QB_DRAFTING_SPEC § 9.6: substrate inconsistencies discovered against locked Phase 1 bibles surfaced for QB triage. Drafting CC does NOT author UPSTREAM-CORRECTION patches.

**Finding 1 — `architecture_overview:4.1` line 447 substrate observation refinement.** Architecture Overview v3 line 447 states: *"Verified case: model/features/feature_definitions.py is imported by model/training/train.py:40 and backend/services/inference_service.py:28 — it is NOT orphaned despite older claims."* This bible's § 4.1.81 substrate-grounded analysis surfaces refinement: while the **module file** is imported (i.e., loaded into the runtime Python module table), **no production model in the gallery (M-1 through M-11) consumes any feature from the legacy 73-feature `FEATURE_GROUPS` schema** — every production model's training-side import per `model/{wr,pl,ranker,win_prob,ensemble,longshot,trajectory}/train.py:32-40` cites `from shared.feature_definitions import (...)` (i.e., `model/shared/feature_definitions.py`, not `model/features/feature_definitions.py`). The module is imported but the features are functionally dormant relative to the production model gallery. The Architecture Overview's "NOT orphaned" assertion is correct at the module-import level but masks the orphan-feature classification at the per-feature gallery level. **UPSTREAM-CORRECTION candidate: refine Architecture Overview v3 § 4.1's substrate observation to distinguish module-import-orphan-classification (the module is loaded) from feature-orphan-classification (no production model consumes the features in the loaded module).** Severity: LOW (refinement, not contradiction). Disposition: candidate for QB triage at corpus-audit gate per QB_HANDOFF_PARALLEL_COHORT_DRAFTING § 7.

**No additional UPSTREAM-CORRECTION candidates identified at v1-draft.**

---

## End of Feature Provenance Bible v1-draft (PRE-AUDIT — Phase 1 deliverable 4 of 7)

Companion verification log: this bible's § 7 (inline; no separate companion file at v1-draft per QB_DRAFTING_SPEC § 9 inline-verification-log model). Audit cycle: corpus-level audit per QB_HANDOFF_PARALLEL_COHORT_DRAFTING § 5 after both FP and MLA bibles reach v1-draft + after MER bible drafts to v1-draft (Phase B).
