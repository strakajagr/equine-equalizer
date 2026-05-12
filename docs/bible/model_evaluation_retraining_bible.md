# Model Evaluation & Retraining Bible

**Status:** v1 LOCKED 2026-05-07
**Drafted:** 2026-05-07
**Cohort:** Phase 1 Deliverables 4-5-6 (Parallel Cohort, Phase B sequential single-CC)
**Bible Number:** 6
**Bible Short:** mer
**Drafting Spec:** `docs/bible/_meta/QB_DRAFTING_SPEC_MODEL_EVALUATION_RETRAINING_BIBLE.md`

## Revision history

- v1 LOCKED 2026-05-07: Phase 1 Cohort corpus-audit-gate sequential lock cycle, step 3 of 3 (MER third per Handoff § 5.2 dependency order, after FP v1 LOCKED 2026-05-07 and MLA v1 LOCKED 2026-05-07). Per corpus-audit Tony Decision 1 (DEFER architecture_overview:4.1 refinement). MER v1-draft AUTHORIZE-CORPUS-AUDIT substrate-grounded; quaternary distribution 36 VERIFIED + 11 PARTIAL + 0 UNVERIFIED + 8 N/A across 55-cell forcing-function matrix (11 rows × 5 columns). Self-audit 9 PASS / 0 FAIL / 0 PARTIAL. 9 NEW + 4 INHERITED PHASE_5_BACKLOG_CANDIDATE entries (calibration debt canonical home consolidated per Q13 ratification at § 5; three-facet operational ML discipline maturity gap consolidated at § 7.5; queued for QB lock-time batch synthesis to PHASE_5_BACKLOG.md per standing instruction). § 4.2 retraining-trigger taxonomy: 5 mer:T-N + 6 mer:E-N entity-class IDs surfaced per Q12 substrate-discovery. Cohort sequential lock cycle COMPLETE post-this-lock; cross-bible cross-reference freeze remains ACTIVE per Handoff § 6.1; UPSTREAM-CORRECTION cycle per Handoff § 7 is sole re-open path.

---

## Audience and Mandate

This bible answers, for every production-deployed model in the EE inference gallery: what does success look like, when do we retrain, how do we keep predictions calibrated, how do we version control the trained artifact, and how do we gate it into production. The 11-entity gallery is inherited 1:1 from `ml_layer_architecture_bible:4.1`; this bible adds the lifetime/operational discipline layer (composition-time facts live in MLA; lifetime facts live here per Q1 / Q13 ratification).

Cross-cutting calibration findings (lifetime sidecar refresh discipline + architectural calibration debt consolidation) are a canonical responsibility of this bible per Tony Q13 ratification: § 5 is the single home for the calibration discipline PHASE_5 candidate group spanning wp_core dead-load + wp_full dead-load + WR styles BYPASS + post-2026-05-01 ranker-as-probability flip implications.

---

## Table of Contents

- § 1. Scope
  - § 1.1 In-scope gallery enumeration (11 entities)
  - § 1.2 Trained models in scope (8 entities)
  - § 1.3 Non-trained models — N/A handling (3 entities)
  - § 1.4 Out of scope
  - § 1.5 Scope boundary against `feature_provenance_bible` (Q11)
  - § 1.6 Scope boundary against `ml_layer_architecture_bible` (Q1 / Q13)
- § 2. Forcing Function (canonical)
- § 3. Inheritance References
  - § 3.1 Phase 0 locks
  - § 3.2 Phase 1 locks (deliverables 1-2-3)
  - § 3.3 Cohort substrate (Phase A v1-drafts)
  - § 3.4 Drafting spec
- § 4. Per-Model Evaluation & Retraining Discipline
  - § 4.1 Per-Model Rows
    - § 4.1.1 M-1 — `wp_core` (XGBoost binary:logistic — WR Layer 1, no-workout)
    - § 4.1.2 M-2 — `wp_full` (XGBoost binary:logistic — WR Layer 1, workout-aware)
    - § 4.1.3 M-3 — `rk_core` (XGBoost rank:pairwise — WR Layer 2, no-workout)
    - § 4.1.4 M-4 — `rk_full` (XGBoost rank:pairwise — WR Layer 2, workout-aware) [pending SP-A3]
    - § 4.1.5 M-5 — `pl_core` (XGBoost reg:squarederror — PL Layer 1) [pending SP-A3]
    - § 4.1.6 M-6 — WR Arithmetic Value Overlay [pending SP-A3]
    - § 4.1.7 M-7 — PL Arithmetic EV/Kelly Overlay [pending SP-A3]
    - § 4.1.8 M-8 — Random Forest Longshot Classifier [pending SP-A3]
    - § 4.1.9 M-9 — LSTM Form Trajectory [pending SP-A3]
    - § 4.1.10 M-10 — Beta-Binomial Bayesian Angle Scorer [pending SP-A3]
    - § 4.1.11 M-11 — Logistic Regression Stacking Ensemble [pending SP-A3]
  - § 4.2 Retraining Trigger Taxonomy (substrate-discovered per Q12)
    - § 4.2.1 Cadence-based triggers
    - § 4.2.2 Drift-based triggers
    - § 4.2.3 Performance-based triggers
    - § 4.2.4 Manual operator triggers
    - § 4.2.5 Discipline gaps (PHASE_5_BACKLOG_CANDIDATEs)
- § 5. Calibration Discipline Findings Summary
  - § 5.1 Lifetime calibration cadence + sidecar refresh discipline
  - § 5.2 Architectural calibration debt findings
  - § 5.3 Post-2026-05-01 ranker-as-probability flip architectural-calibration consolidation
- § 6. Model Artifact Version Control Findings Summary
  - § 6.1 Active-row selection discipline
  - § 6.2 Retention policy + deprecation lineage
- § 7. Deployment Gating Findings Summary
  - § 7.1 Pre-deployment gate discipline
  - § 7.2 Rollback discipline
  - § 7.3 Post-deployment monitoring discipline
- § 8. Cross-Reference Index
  - § 8.1 mer:M-N → mla:M-N matrix (1:1 inheritance)
  - § 8.2 mer:E-N (evaluation criteria) and mer:T-N (retraining triggers) introduction
  - § 8.3 fp:F-N references in narrative columns
- § 9. Verification Log

---

## § 1. Scope

### § 1.1 In-scope gallery enumeration (11 entities)

The Model Evaluation & Retraining Bible covers the 11 production-deployed model entities ratified at MLA SP-1 (per `ml_layer_architecture_bible:4.1`). One row per entity. Roster verbatim from MLA v1-draft § 4.1 (verified at session start; reconciliation logged in § 9.8):

| M-ID | Model Name | Family | Layer | Trained? |
|------|-----------|--------|-------|----------|
| `M-1` | `wp_core` | XGBoost binary:logistic | WR Layer 1 (no-workout) | YES |
| `M-2` | `wp_full` | XGBoost binary:logistic | WR Layer 1 (workout-aware) | YES |
| `M-3` | `rk_core` | XGBoost rank:pairwise (LambdaMART) | WR Layer 2 (no-workout) | YES |
| `M-4` | `rk_full` | XGBoost rank:pairwise (LambdaMART) | WR Layer 2 (workout-aware) | YES |
| `M-5` | `pl_core` | XGBoost reg:squarederror | PL Layer 1 | YES |
| `M-6` | WR Arithmetic Value Overlay | Arithmetic (deterministic) | WR Layer 3 (value overlay) | NO |
| `M-7` | PL Arithmetic EV/Kelly Overlay | Arithmetic (deterministic) | PL Layer 2 (EV/Kelly overlay) | NO |
| `M-8` | Random Forest Longshot Classifier (`longshot_rf`) | sklearn RandomForestClassifier | LS Layer 4 | YES |
| `M-9` | LSTM Form Trajectory (`trajectory_lstm`) | PyTorch LSTM | LS Layer 5 | YES |
| `M-10` | Beta-Binomial Bayesian Angle Scorer | Bayesian posterior (statistical) | LS Layer 6 | NO |
| `M-11` | Logistic Regression Stacking Ensemble (`ensemble`) | sklearn LogisticRegression | LS Layer 7 | YES |

### § 1.2 Trained models in scope (8 entities)

`M-1`, `M-2`, `M-3`, `M-4`, `M-5`, `M-8`, `M-9`, `M-11` are trained models. All forcing-function dimensions (per § 2) apply to each row: success criteria, retraining triggers, calibration discipline, model artifact version control, deployment gating.

### § 1.3 Non-trained models — N/A handling (3 entities)

`M-6`, `M-7`, `M-10` are non-trained per `ml_layer_architecture_bible:4.1`. Per spec § 3.3 the forcing-function columns apply with explicit N/A treatment recorded in § 5.9 quaternary-status discipline:

- **M-6 (WR Arithmetic Value Overlay).** Deterministic arithmetic at `backend/services/wr_inference_service.py:46-58` (`compute_value_overlay(raw_win_prob, morning_line_odds)`). Module-level constants at `wr_inference_service.py:46-50` (`VALUE_MIN_EDGE = 0.05`, `VALUE_HALF_KELLY = 0.5`, `VALUE_MAX_KELLY = 0.10`, `VALUE_BANKROLL = 1000.0`) are the parameter discipline; no training cycle, no calibration in the ML sense, no `model_versions` registry row. Retraining triggers cell: **N/A** ("arithmetic — no training cycle"). Calibration discipline cell: **N/A** with parameter-discipline citation. Version control cell: **N/A** with "version = source-code version of `wr_inference_service.py`" rationale. Deployment gating cell: **APPLIES** uniformly (Lambda warm-start path).

- **M-7 (PL Arithmetic EV/Kelly Overlay).** Deterministic arithmetic at `backend/services/pl_inference_service.py` `compute_ev_and_kelly(...)`. Constants imported from `shared.constants` at `pl_inference_service.py:27-29` (`BANKROLL`, `KELLY_FRACTION`, `MAX_BET_PCT`, `MIN_EDGE_TO_BET`, `STRONG_VALUE_THRESHOLD`, `HANDICAPPING_BLEND_WEIGHT`); no training cycle, no calibration in the ML sense, no `model_versions` registry row. Same N/A treatment pattern as M-6.

- **M-10 (Beta-Binomial Bayesian Angle Scorer).** Non-trained statistical computation at `model/angles/scorer.py` (LS Layer 6). Bayesian posterior is calibrated-by-construction (no calibration sidecar required). Retraining triggers cell: **N/A** with "Bayesian posterior auto-updates from upstream `angle_stats` table refresh per `data_pipeline_bible:4.1.7`" rationale (the `equine-angle-stats-nightly` EventBridge rule per `architecture_overview:3.6` is the substrate, although fire-and-fail per `architecture_overview:3.6` anomaly note — substrate gap recorded in § 4.2.5). Version control cell: **N/A** with "version = source-code version of `model/angles/scorer.py` plus `angle_stats` aggregation refresh state" rationale.

### § 1.4 Out of scope

- Models considered but not deployed to production inference (per MLA Q6 ratification — the in-scope predicate is binding).
- Deprecated/superseded model artifact version archaeology (this bible documents version-control *discipline*; the archaeology of deprecated artifacts is a Phase 5 disposition concern, not a discipline concern).
- Per-feature monitoring substrate (per Q11 ratification; canonical home is `feature_provenance_bible` — narrative cross-references via `fp:F-N` only).
- Composition-time architectural facts (per Q1 / Q13 ratification; canonical home is `ml_layer_architecture_bible` — narrative cross-references via `mla:M-N` only).

### § 1.5 Scope boundary against `feature_provenance_bible` (Q11)

FP is the canonical home for per-feature *monitoring* (drift, distribution shift, completeness audits). MER cross-references via `fp:F-N` in narrative columns when retraining-trigger taxonomy entries reference feature-distribution-drift signals. MER does not re-author per-feature monitoring substrate; it indexes it.

### § 1.6 Scope boundary against `ml_layer_architecture_bible` (Q1 / Q13)

MLA is the canonical home for per-model *composition-time* facts (model type / inputs / outputs / position in inference pipeline / target latent / output composition / composition-time calibration state). MER inherits the M-N gallery 1:1 and adds the lifetime/operational dimension. When MLA records a calibration state of `BYPASS` or `UNCALIBRATED` (per `ml_layer_architecture_bible:5`), MER documents the architectural debt and the lifetime/operational implications, with cross-references to MLA via `mla:M-N` and to MLA section numbers (e.g., `ml_layer_architecture_bible:5.2` for the UNCALIBRATED index, `ml_layer_architecture_bible:5.3` for the BYPASS index).

---

## § 2. Forcing Function (canonical)

For every model in the EE production model gallery (11 entities `M-1` through `M-11` per § 1.1):

> **per-model success criteria → retraining triggers → calibration discipline → model artifact version control → deployment gating**

Every dimension of this forcing function appears as a column in the per-model row schema (§ 4.1 rows). No dimension is omitted. No row carries an empty cell in a forcing-function column without explicit UNVERIFIED treatment per spec § 5.9 quaternary discipline OR explicit N/A treatment per § 1.3 non-trained-model handling.

The forcing function is the cycle that closes lifetime model discipline: success criteria define the bar, retraining triggers define the cadence and sensitivity, calibration discipline keeps the score-vs-truth alignment honest over time, version control gives reproducibility and rollback, deployment gating enforces the bar at promotion. A bible row that documents only one or two dimensions of this cycle leaves operational discipline silent on the others — corpus-audit gates the convergence.

---

## § 3. Inheritance References

This bible inherits substrate from prior locks and cohort predecessors. Cross-references follow Q9 forward-only convention: prefix-explicit for cross-bible references, unprefixed permitted for intra-document references (per Phase A ratification at SP-A1; banked refinement to AUDIT_METHODOLOGY).

### § 3.1 Phase 0 locks

- META_PLAN v9 (`docs/bible/_meta/META_PLAN.md`) — Phase 0 strategic lock.
- BIBLE_STRUCTURE_SPEC v6 (`docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md`) — bible-structure invariants; § 5.3 canonical-home registry; § 6.3 cross-reference convention.
- AUDIT_METHODOLOGY v2-patched (`docs/bible/_meta/AUDIT_METHODOLOGY.md`) — audit-cycle invariants.
- CONVERGENCE_CRITERIA v2 (`docs/bible/_meta/CONVERGENCE_CRITERIA.md`) — corpus-audit gate criteria.
- TRIAGE_QUEUE_SPEC v1 (`docs/bible/_meta/TRIAGE_QUEUE_SPEC.md`) — `PHASE_5_BACKLOG_CANDIDATE` format and disposition vocabulary.

### § 3.2 Phase 1 locks (deliverables 1-2-3)

- `architecture_overview.md` (Architecture Overview v3, LOCKED 2026-05-05). § 3.1 Lambda inventory (8 Lambdas — 5 Active + 3 INACTIVE). § 3.2 ECS task families (`equine-training`, `equine-training-daily-full`, `equine-training-manual`, `equine-training-pl`, `equine-training-win-prob`). § 3.6 EventBridge schedule (13 rules — 10 ENABLED + 3 DISABLED; 4 fire-and-fail anomalies). § 3.7 ECR repositories (`equine-training` image is the training image). § 3.8 Secrets Manager (`equine-equalizer/db-credentials` consumer in canonical DB connection module).
- `database_schema_bible.md` (D&S Bible v1-patched-d2, LOCKED 2026-05-06). § 4.1 per-table schemas; specifically § 4.1 row for `model_versions` table (artifact registry; one row per trained-model artifact; `is_active` flag for production selection).
- `data_pipeline_bible.md` (Data Pipeline Bible v1-patched-c, LOCKED 2026-05-06). § 4.1 per-flow detail; specifically the per-pipeline retraining flow (training image build, ECS task family invocation, S3 artifact write, `model_versions` registry update). § 4.1.7 `angle_stats` aggregation refresh flow (relevant to M-10 N/A retraining-trigger narrative).

### § 3.3 Cohort substrate (Phase A v1-drafts)

- `feature_provenance_bible.md` (FP v1-draft post-revise-pass, AUTHORIZE-PHASE-B 2026-05-06). Not yet locked. Narrative columns in this bible cross-reference `fp:F-N` for any feature-distribution-drift retraining-trigger entries per Q11.
- `ml_layer_architecture_bible.md` (MLA v1-draft, AUTHORIZE-PHASE-B 2026-05-06). Not yet locked. Per-model rows in § 4.1 cross-reference `mla:M-N` for composition-time facts per Q1 / Q13.

Cross-bible cross-reference resolution freezes at corpus-audit gate per Handoff § 6.1. Until corpus-audit, drafting CC may emit cross-references that may need adjustment if FP/MLA undergo UPSTREAM-CORRECTION at corpus audit. This is expected; corpus audit reconciles.

### § 3.4 Drafting spec

`docs/bible/_meta/QB_DRAFTING_SPEC_MODEL_EVALUATION_RETRAINING_BIBLE.md` (this bible's own drafting spec). § 5 row schema; § 6 fixed bible structure; § 8 SP-A1 / SP-A2 / SP-A3 protocol; § 10 9-check self-audit; § 12 Phase 5 backlog candidate harvesting protocol.

---

## § 4. Per-Model Evaluation & Retraining Discipline

### § 4.1 Per-Model Rows

One row per entity in the 11-entity gallery. Row schema columns per spec § 5: M-ID / Model Name / Success Criteria / Retraining Triggers / Calibration Discipline / Model Artifact Version Control / Deployment Gating / Calibration Discipline Narrative / Quaternary Status / Notes. Every column populated with code-line citations or explicit UNVERIFIED / N/A narrative.

#### § 4.1.1 M-1 — `wp_core` (XGBoost binary:logistic — WR Layer 1, no-workout)

**M-ID.** `M-1`. Inherited 1:1 from `mla:M-1`.

**Model Name.** Primary identifier: `win_prob_core` (model_versions registry name). Cross-reference `mla:M-1 § 5.2` for full identifier hierarchy (specialist-tagged variants `win_prob_core_<specialist>`, legacy `win_prob_odds`, legacy alias `wr_odds`). Training entry point: `model/win_prob/train.py` `train_core_model_only(specialist)` at `model/win_prob/train.py:464-529`.

**Success Criteria.** Substrate-grounded operational metrics per `model/training/train.py:681-690` (persisted to `model_versions` per `database_schema_bible:4.1` `model_versions` row schema):

- **`mer:E-1` exacta_hit_rate (PRIMARY).** Computation at `model/evaluation/metrics.py:9-62`. Defined as: percentage of races in which the top-2 predicted horses are the actual top-2 finishers (in any order). Threshold: documented as primary metric per `model/win_prob/train.py:831` (`logger.info(f"  Primary metric: exacta hit rate")`); no hard numerical pass/fail threshold encoded in source — gating is via manual operator review per `model/training/train.py:667-668` (verbatim: "Only set_active=True after manual review of metrics. Never auto-promote.").
- **`mer:E-2` trifecta_hit_rate (SECONDARY).** Computation at `model/evaluation/metrics.py:65-111`. Top-3 predicted horses cover the actual trifecta in any order. Same gating discipline as `mer:E-1` (manual review).
- **`mer:E-3` top1_accuracy (DIAGNOSTIC).** Win-rate of top-1 pick at `model/evaluation/metrics.py:114-150`. Per the docstring at `metrics.py:118-121`: "useful but NOT our primary metric. We optimize for exacta/trifecta."
- **`mer:E-4` top3_accuracy (DIAGNOSTIC).** Top-1 pick finishes in the top 3 at `model/evaluation/metrics.py:153-189`.
- **`mer:E-5` calibration_score (DIAGNOSTIC).** `1.0 - ECE` (Expected Calibration Error across 10 buckets) at `model/evaluation/metrics.py:192-258`. Higher = better calibration. **Operative for M-1 only diagnostically** because M-1's binary:logistic output is BYPASS in the displayed-prediction path (per `mla:M-1 § 5.9` BYPASS state); calibration_score is computed and persisted to `model_versions` but does not gate deployment.
- **`mer:E-6` ndcg (XGB-INTERNAL eval_metric).** XGBoost training-time `eval_metric='ndcg'` per `model/win_prob/train.py:66`; `best_ndcg` persisted at `model/training/train.py:609`. Operates on the validation hold-out during training; controls early-stopping (`EARLY_STOPPING_ROUNDS=50`) per `model/win_prob/config.py:10-23` hyperparameter snapshot.

Pass/fail discipline: operator manual review per `model/training/train.py:667-668`. **No hard numerical thresholds encoded.** Quaternary status: PARTIAL — metrics computed and persisted with full substrate citations; threshold values not encoded in source (manual gate only). Surfacing as gap per Q12 directive: see § 4.2.5 GAP B.

**Retraining Triggers.** Substrate-discovered taxonomy operative for M-1:

- **`mer:T-1` Daily-full cadence (CADENCE).** EventBridge rule `equine-daily-retrain-full` @ `cron(30 2 * * ? *)` per `architecture_overview:3.6` (daily at 02:30 UTC) → ECS task family `equine-training-daily-full` (target ARN `arn:aws:ecs:us-east-1:584812014683:task-definition/equine-training-daily-full`). Task entry point invokes `model/training/train.py` (training entry script bundled into the `equine-training` ECR image per `architecture_overview:3.7`). Daily-full retrain encompasses all WR + PL pipelines including wp_core lean53 retrain via the `train_core_model_only(specialist)` entry point at `model/win_prob/train.py:464`.
- **`mer:T-2` Weekly WR cadence (CADENCE).** EventBridge rule `equine-weekly-retrain-wr` @ `cron(0 4 ? * MON *)` per `architecture_overview:3.6` (Mondays at 04:00 UTC) → ECS task family `equine-training-win-prob`. WR-specific retrain (win-probability ranker family, includes wp_core). Operative as a redundant Monday refresh on top of the daily cadence.
- **`mer:T-4` Manual operator trigger (MANUAL).** Operator-triggered ad-hoc retrain via ECS `equine-training-manual` task family per `architecture_overview:3.2` (no EventBridge schedule; console / CLI invocation). The `set_active` flag at `model/training/train.py:657, 706-707` is the manual gate: training writes the artifact + `model_versions` row with `is_active=False` by default (line 695) and only promotes via `repo.set_active_model(model_version_id)` at line 707 when `set_active=True` is passed by the operator. CLI hint at `model/training/train.py:912-914`: training emits "Review metrics then activate with: ..." when `--set_active` is omitted.
- **`mer:T-5` Calibration sidecar refresh (MANUAL).** `scripts/fit_all_calibrations.py` is a manually-scheduled script (no EventBridge cron); calibration window is hardcoded at `scripts/fit_all_calibrations.py:46-47` (`CAL_START = date(2026, 4, 1)`, `CAL_END = date(2026, 4, 14)`). Per the docstring at `scripts/fit_all_calibrations.py:1-25`, the script fits isotonic-regression sidecars for all 14 active wp_full + pl_core artifacts. **Note: M-1 (wp_core) is not the explicit subject of `fit_all_calibrations.py`** (the docstring lists `wp_full_*` + `pl_core_*`; ranker is explicitly excluded per line 24 "ranker/...   (no — rk skipped per spec)"). However, lean53 wp_core artifacts have calibration sidecars in S3 (per `mla:M-1 § 5.9` and `wr_inference_service.py:171-178` conditional load) — these are produced by `scripts/fit_lean53_core_calibrations.py` per the script directory inventory at § 4.2.5 GAP A substrate. Substrate gap: explicit cadence for the lean53_core sidecar refresh is not surfaced in source.

Cross-references:
- `mer:T-1` and `mer:T-2` indexed to § 4.2.1 (cadence-based triggers).
- `mer:T-4` indexed to § 4.2.4 (manual operator triggers).
- `mer:T-5` indexed to § 4.2.4 (manual operator triggers — calibration sidecar refresh subset).

Quaternary status: VERIFIED — substrate-grounded with code-line citations.

**Calibration Discipline.** **Lifetime/operational discipline:** `scripts/fit_all_calibrations.py` fits isotonic-regression sidecars on a 14-day calibration window (`CAL_START=2026-04-01`, `CAL_END=2026-04-14` per `fit_all_calibrations.py:46-47`) using `sklearn.isotonic.IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)` per `fit_all_calibrations.py:189-190`; sidecar JSON written to S3 at `<base_key>_calibration.json`. Refresh cadence is manual (per `mer:T-5`). For lean53 wp_core artifacts specifically, sidecars are also produced by `scripts/fit_lean53_core_calibrations.py` per the script directory inventory; the inference loader at `wr_inference_service.py:171-178` conditionally loads the sidecar (gated on `'lean53' in self.wp_core_version.version_name`).

**Architectural finding dimension:** per `mla:M-1 § 5.9` calibration state is `BYPASS (sidecar conditionally loaded but never applied to inference output)`. The calibration sidecar is a dead-load artifact for M-1 — loaded into memory at warm-start when lean53 artifact is selected, but never consumed by the inference path. Direct evidence at `wr_inference_service.py:326-335` (`_apply_calibration` defined) + grep verification (`grep -nE "wp_core_calibration|_apply_calibration\(" wr_inference_service.py` returns load + definition but no usage in `predict_race`). The dead-load arose from the post-2026-05-01 ranker-as-probability architectural flip (per `wr_inference_service.py:579-598` comment block) which removed wp_core/wp_full from the displayed-probability path; the calibration sidecars were retained as deliverables of the calibration workstream but their inference-side consumer was removed by the architectural flip.

PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=refactor; rationale="wp_core lean53 calibration sidecars are loaded into warm-start memory but never applied — distinct from the line 616-626 ranker calibration BYPASS already in QB's known list. Either remove the dead load to reduce warm-start cost and S3 read pressure, or wire the sidecar to apply to pred.raw_win_prob as a diagnostic-quality calibrated score for backtesting parity. Consolidation home § 5.2 (Architectural calibration debt findings) per Q13 ratification."; cite=wr_inference_service.py:171-178, wr_inference_service.py:326-335.

Quaternary status: VERIFIED.

**Model Artifact Version Control.** Substrate-grounded version control discipline:

- **Version naming convention.** `wp_core_lean53_<specialist>_<timestamp>.json` (lean53 path) per `model/win_prob/train.py:472-474, 519-528`. Legacy path: `win_prob_odds_<timestamp>.json` (58-feature).
- **Storage location.** S3 bucket `equine-model-artifacts` (per `architecture_overview:3.4` S3 inventory); prefix `win_prob/`. Path persisted to `model_versions.s3_artifact_path` per `database_schema_bible:4.1` `model_versions` schema.
- **`model_versions` registry interaction.** New artifact registered with `is_active=False` by default per `model/training/train.py:695`; `set_active_model(model_version_id)` flips to `is_active=True` ONLY when operator passes `--set_active` per `model/training/train.py:706-707` (the manual-review gate of `mer:T-4`). `set_active_model` at `backend/repositories/model_version_repository.py:72-95` first sets all rows of the same model_type to `is_active=False` then sets the target row to `is_active=True` (single-active-per-type invariant per `model_version_repository.py:13` "Only one model should have is_active = true").
- **Active-row selection discipline.** Loader at `wr_inference_service.py:156-160` calls `_try_load_model_type` with priority chain `[win_prob_core_<specialist>, win_prob_core, win_prob_odds, wr_odds]`; per-row selection within a model_type is governed by `model_version_repository.py` query (single-row LIMIT 1 against `is_active = TRUE`).

Pre-known PHASE_5 candidate (per QB-known list, does NOT surface as new candidate per SP-2 standing instruction): 88-row `model_versions` registry with 45 simultaneously active under non-deterministic LIMIT 1 (selection discipline concern across the gallery; not specific to M-1; canonical home § 6.1).

Quaternary status: VERIFIED.

**Deployment Gating.** Substrate-grounded deployment-gate discipline:

- **Pre-deployment checks.** Operator manual review of metrics (`exacta_hit_rate`, `trifecta_hit_rate`, `top1_accuracy`, `top3_accuracy`, `calibration_score`) per `model/training/train.py:667-668` ("Only set_active=True after manual review of metrics. Never auto-promote."). No automated threshold gate.
- **Deployment mechanism.** S3 artifact upload at training-time (per `model/training/train.py` artifact-write) → `model_versions` row insertion with `is_active=False` (line 695) → operator passes `--set_active` to flip the registry → Lambda warm-start refresh on next cold-start picks up the new active row via the loader priority chain at `wr_inference_service.py:156-160`. **Lambda warm-start does NOT auto-refresh on registry update**; new artifacts only become visible on Lambda cold-start (memory-cached `is_active` selection).
- **Rollback discipline.** Operator manually re-flips `is_active` in `model_versions` (CLI / direct DB) → `set_active_model(<previous_artifact_id>)` re-establishes the previous active row (single-active-per-type invariant per `model_version_repository.py:90-95` automatically demotes the now-incorrect row). S3 artifacts are retained (no automatic delete) — rollback is registry-flip only. Per `architecture_overview:3.7` `equine-training` ECR repo retention is not enumerated; per `architecture_overview` § 3.7 "Lifecycle policies on each repository are not enumerated here; if relevant, document at Phase 5 backlog."
- **Post-deployment monitoring.** Existing diagnostic scripts (`scripts/longshot_bias_diagnostic.py`, `scripts/post_calibration_diagnostic.py`, `scripts/lean53_diagnostic.py`) are reports-only per docstring at `scripts/longshot_bias_diagnostic.py:22` ("Doesn't fix anything. Reports."). These do not gate retraining or rollback — Phase 5 maturity gap; see § 4.2.5 GAP A.

Quaternary status: VERIFIED.

**Calibration Discipline Narrative.** wp_core has a calibration sidecar present in S3 (for lean53 artifacts) and conditionally loaded into memory at warm-start, but no inference-path code applies the sidecar to wp_core output. This is the architectural finding consolidated in § 5.2 (Architectural calibration debt findings). The PHASE_5_BACKLOG_CANDIDATE entry above is one member of the four-member calibration debt candidate group that consolidates at § 5 per Tony Q13 ratification (the other three: wp_full dead-load per § 4.1.2; WR styles BYPASS at `wr_inference_service.py:616-626`; post-2026-05-01 ranker-as-probability architectural flip implications).

**Quaternary Status (per spec § 5.9).** Per-column status:
- Success Criteria: **PARTIAL** (metrics computed + persisted; no hard numerical thresholds; Q12 GAP B in § 4.2.5).
- Retraining Triggers: **VERIFIED**.
- Calibration Discipline: **VERIFIED** (with PHASE_5_BACKLOG_CANDIDATE consolidation to § 5.2).
- Model Artifact Version Control: **VERIFIED** (with pre-known PHASE_5 candidate consolidation to § 6.1).
- Deployment Gating: **VERIFIED** (with Q12 GAP A reference in § 4.2.5 for absent post-deployment monitoring auto-gating).

**Notes.** Hyperparameter snapshot per `model/win_prob/config.py:10-23`: `learning_rate=0.05`, `max_depth=6`, `min_child_weight=20`, `subsample=0.8`, `colsample_bytree=0.8`, `reg_alpha=0.1`, `reg_lambda=1.0`, `tree_method='hist'`, `random_state=42`, `scale_pos_weight` set dynamically per training run. `NUM_ROUNDS=1000`, `EARLY_STOPPING_ROUNDS=50`. Specialist family: 8 styles per `wr_inference_service.py:101-105`; wp_core canonically general-only per `wr_inference_service.py:191-193` ("`_full models are style-specific. _core stays general`"). Training-time/inference-time delta: training emits multi-format artifacts (legacy `wp_odds` 58-feature + lean53 47-feature); inference dispatches by version-name suffix detection.

---

#### § 4.1.2 M-2 — `wp_full` (XGBoost binary:logistic — WR Layer 1, workout-aware)

**M-ID.** `M-2`. Inherited 1:1 from `mla:M-2`.

**Model Name.** Primary identifier: `wp_full_<specialist>` (8-style specialist family: `general`/`speed`/`closer`/`class_riser`/`class_dropper`/`sprint`/`route`/`gonzo_sauce`). Secondary identifier: `win_prob_full` (legacy / general-only). Cross-reference `mla:M-2 § 5.2` for full identifier hierarchy. Training entry point: `model/win_prob/train.py` `train_full_model_only(specialist)` at `model/win_prob/train.py:532-570`.

**Success Criteria.** Same metric set as `mer:M-1`: `mer:E-1` exacta_hit_rate (primary), `mer:E-2` trifecta_hit_rate, `mer:E-3` top1_accuracy, `mer:E-4` top3_accuracy, `mer:E-5` calibration_score, `mer:E-6` ndcg (XGB-internal). Computation paths identical (same `model/evaluation/metrics.py` + same `model/training/train.py:681-690` persistence). Pass/fail discipline: operator manual review per `model/training/train.py:667-668`; no hard numerical thresholds encoded.

**Specialist-specific calibration_score caveat.** wp_full is the family of 8 specialist artifacts; calibration_score is computed per-artifact during training validation. Per `mla:M-2 § 5.9` BYPASS state, the metric is diagnostic only — does not gate deployment.

Quaternary status: PARTIAL (same PARTIAL state as `mer:M-1`; thresholds not encoded; Q12 GAP B reference in § 4.2.5).

**Retraining Triggers.** Substrate-discovered taxonomy operative for M-2:

- **`mer:T-1` Daily-full cadence (CADENCE).** EventBridge `equine-daily-retrain-full` @ `cron(30 2 * * ? *)` → ECS `equine-training-daily-full`. Daily-full encompasses wp_full retrain via `train_full_model_only(specialist)` entry point.
- **`mer:T-2` Weekly WR cadence (CADENCE).** EventBridge `equine-weekly-retrain-wr` @ `cron(0 4 ? * MON *)` → ECS `equine-training-win-prob`. WR-specific Monday refresh (redundant on top of daily); also retrains wp_full per the win-probability family scope.
- **`mer:T-4` Manual operator trigger (MANUAL).** Same `set_active` discipline as M-1 per `model/training/train.py:657, 706-707`.
- **`mer:T-5` Calibration sidecar refresh (MANUAL).** wp_full is the **explicit primary subject** of `scripts/fit_all_calibrations.py` per the docstring at lines 1-3 ("Fit isotonic calibration heads for all 14 active wp_full + pl_core artifacts (general + 6 specialists × 2 model_types)"). All 14 active wp_full + pl_core artifacts are calibrated on the 2026-04-01 → 2026-04-14 window per `fit_all_calibrations.py:46-47`. Specialist-filter artifacts (sprint, route) are calibrated on the sprint/route subset of the window matching their training domain per the docstring at lines 14-16. Refresh cadence is manual.

Cross-references: same as M-1 (`mer:T-1`, `mer:T-2`, `mer:T-4`, `mer:T-5` indexed to § 4.2.1 / § 4.2.4).

Quaternary status: VERIFIED.

**Calibration Discipline.** **Lifetime/operational discipline:** `scripts/fit_all_calibrations.py` is the canonical sidecar fitter for wp_full. Calibration window April 1-14, 2026 (out-of-training-data; training cutoff 2025-12-31 per docstring at lines 5-7). Holdout for diagnostic re-eval is April 15-26 (kept separate per docstring lines 6-7). Per-specialist sidecar fit; isotonic regression with clip-bounds. Sidecar persisted to S3 at `s3://equine-model-artifacts/win_prob/wp_full_<specialist>_<ts>_calibration.json` per docstring at lines 19-20. Inference-time load at `wr_inference_service.py:205-212` (unconditional for any wp_full artifact with corresponding sidecar in S3).

**Architectural finding dimension:** per `mla:M-2 § 5.9` calibration state is `BYPASS (sidecar loaded unconditionally for non-legacy artifacts but never applied to inference output)`. The wp_full sidecar load is *unconditional* (no version-name suffix gate, unlike M-1's lean53-conditional gate) — every active wp_full artifact across all 8 styles pays the warm-start cost regardless of whether the sidecar will ever be consumed. Direct evidence: `_apply_calibration` defined at `wr_inference_service.py:326-335` but grep returns no usage site for `wp_full_calibration` post-load. The dead-load arose from the same post-2026-05-01 ranker-as-probability architectural flip that affected M-1.

PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=refactor; rationale="wp_full calibration sidecars are loaded unconditionally for all 8 active styles at warm-start (8 × O(thresholds) memory + 8 S3 download attempts) but never applied to inference output — distinct from the line 616-626 BYPASS already known to QB. Either remove the load (drop the `_try_load_calibration` call at line 205 + the related infra in `scripts/fit_all_calibrations.py`) or apply the sidecar to a calibrated diagnostic field for backtesting parity. Consolidation home § 5.2 per Q13 ratification."; cite=wr_inference_service.py:205-212, wr_inference_service.py:326-335.

Quaternary status: VERIFIED.

**Model Artifact Version Control.** Substrate-grounded version control discipline:

- **Version naming convention.** `wp_full_<specialist>_<timestamp>.json` per `model/win_prob/train.py:566-568, model/shared/specialists.py:artifact_suffix`. Per-specialist artifact emission (one artifact per style; 8 styles total).
- **Storage location.** S3 bucket `equine-model-artifacts`; prefix `win_prob/`. Per-specialist artifact path persisted to `model_versions.s3_artifact_path`.
- **`model_versions` registry interaction.** Same pattern as M-1: insert with `is_active=False` per `model/training/train.py:695`; flip via `set_active_model(model_version_id)` only on operator `--set_active`. **Specialist-distinct model_type:** `wp_full_general`, `wp_full_speed`, `wp_full_closer`, etc. — each specialist is a distinct `model_type` with its own single-active-per-type invariant.
- **Active-row selection discipline.** Loader at `wr_inference_service.py:193-198`: `wp_full_general` / `win_prob_full` for `style='general'`; `wp_full_<specialist>` for non-general styles. Per-style independent `is_active` selection.

Quaternary status: VERIFIED.

**Deployment Gating.** Substrate-grounded deployment-gate discipline (same pattern as M-1):

- **Pre-deployment checks.** Operator manual review per `model/training/train.py:667-668`. **Per-specialist independent gate** — operator must `--set_active` each specialist artifact independently.
- **Deployment mechanism.** Same as M-1: S3 upload → `model_versions` row insertion → operator promotion → Lambda cold-start refresh.
- **Rollback discipline.** Same as M-1: per-`model_type` registry flip; S3 artifacts retained.
- **Post-deployment monitoring.** Same as M-1: reports-only diagnostic scripts; no auto-gating. Phase 5 maturity gap (§ 4.2.5 GAP A).

Quaternary status: VERIFIED.

**Calibration Discipline Narrative.** wp_full has the strongest dead-load case in the gallery: 8 active specialist sidecars loaded unconditionally at every warm-start, none applied to inference. The architectural finding is consolidated in § 5.2 alongside M-1's lean53-conditional dead-load. The PHASE_5_BACKLOG_CANDIDATE entry above is the second member of the four-member calibration debt candidate group consolidating at § 5 per Q13 ratification.

**Quaternary Status (per spec § 5.9).** Per-column status:
- Success Criteria: **PARTIAL**.
- Retraining Triggers: **VERIFIED**.
- Calibration Discipline: **VERIFIED** (with PHASE_5_BACKLOG_CANDIDATE consolidation to § 5.2).
- Model Artifact Version Control: **VERIFIED**.
- Deployment Gating: **VERIFIED**.

**Notes.** 8-style specialist family per `wr_inference_service.py:101-105`. Specialist semantics (FILTER / WEIGHT / FEATURE_SET) inherited from `model/shared/specialists.py:28-37`. Workout-layer hyperparameter snapshot at `model/win_prob/config.py:27-37`: `WORKOUT_XGB_PARAMS` with conservative `max_depth=4` and stronger regularization (`reg_alpha=0.5, reg_lambda=2.0`) than wp_core. Training-time vs inference-time delta: training writes per-style artifacts with `_meta.json` sidecars per `model/win_prob/train.py:200-210`; inference loads model + meta + calibration sidecar (calibration sidecar load is unconditional for wp_full vs gated-on-lean53 for wp_core). Gonzo Sauce specialist (`wp_full_gonzo_sauce`) trains on 67-feature feature set vs 53-feature for the other 7 specialists per `mla:M-2 § 5.4`.

---

#### § 4.1.3 M-3 — `rk_core` (XGBoost rank:pairwise — WR Layer 2, no-workout)

**M-ID.** `M-3`. Inherited 1:1 from `mla:M-3`.

**Model Name.** Primary identifier: `ranker_core` (model_versions registry name). No secondary identifiers — single-item priority list at `wr_inference_service.py:215-217` (`_try_load_model_type(['ranker_core'])`); no specialist tagging for rk_core. Cross-reference `mla:M-3 § 5.2`. Training entry point: `model/ranker/train.py` `train_ranker(...)` invocation; artifact-suffix `'ranker_core'` for general-only registration.

**Success Criteria.** Same primary/secondary metric set as `mer:M-1` and `mer:M-2`: `mer:E-1` exacta_hit_rate (primary), `mer:E-2` trifecta_hit_rate, `mer:E-3` top1_accuracy, `mer:E-4` top3_accuracy, `mer:E-6` ndcg. **`mer:E-5` calibration_score is NOT operative for M-3** because rk_core's output is a within-race rank score (unbounded; only meaningful in within-race comparison per `mla:M-3 § 5.5`), not a calibrated probability — calibration_score (1.0 - ECE) is a probability-bucketing metric and does not apply to rank scores directly. The downstream within-race softmax at `wr_inference_service.py:599-603` produces `ranker_probs` which is consumed for the displayed `win_probability` (post-BYPASS at lines 616-626), but the calibration_score metric in `model/training/train.py:681-690` is computed against the model's training-time validation output, not against the post-softmax probability.

Per `model/ranker/train.py:83` (`objective='rank:pairwise'`) and the docstring at line 4 (LambdaMART), the training-time eval metric is XGB-internal `eval_metric='ndcg'`; `best_ndcg` persisted at `model/training/train.py:609`. Pass/fail discipline: operator manual review per `model/training/train.py:667-668`; same gating pattern as wp_core/wp_full. Quaternary status: PARTIAL (thresholds not encoded; Q12 GAP B reference).

**Retraining Triggers.** Substrate-discovered taxonomy operative for M-3:

- **`mer:T-1` Daily-full cadence (CADENCE).** EventBridge `equine-daily-retrain-full` → ECS `equine-training-daily-full`. Daily-full encompasses ranker retrain.
- **`mer:T-2` Weekly WR cadence (CADENCE).** EventBridge `equine-weekly-retrain-wr` → ECS `equine-training-win-prob`. WR-specific Monday refresh; ranker family is in the WR scope of this rule.
- **`mer:T-4` Manual operator trigger (MANUAL).** Same `set_active` discipline.
- **`mer:T-5` Calibration sidecar refresh (MANUAL).** **NOT OPERATIVE for M-3.** Per `scripts/fit_all_calibrations.py:24` docstring: `s3://equine-model-artifacts/ranker/...   (no — rk skipped per spec)`. Ranker calibration is explicitly excluded from `fit_all_calibrations.py`. Only the gonzo_sauce variant of M-4 (`rk_full_gonzo_sauce`) was added later as a one-off exception per `mla:M-4 § 5.9`. For M-3 specifically, no calibration sidecar exists in S3, no load is attempted, no inference-path code applies any calibration to rk_core output (per `mla:M-3 § 5.9` UNCALIBRATED state).

Cross-references: `mer:T-1`, `mer:T-2`, `mer:T-4` indexed to § 4.2.1 / § 4.2.4. `mer:T-5` explicitly NOT operative for M-3.

Quaternary status: VERIFIED.

**Calibration Discipline.** **Lifetime/operational discipline:** N/A in the strict sense — there is no calibration sidecar in S3, no warm-start load, no inference-time application. The within-race softmax at `wr_inference_service.py:599-603` is a normalization (probability-distribution-construction) transform, not a calibration transform — it converts unbounded LambdaMART rank scores into a within-race probability distribution that sums to 1.0 but does not correct the model's score-vs-truth alignment.

**Architectural finding dimension:** per `mla:M-3 § 5.9` calibration state is `UNCALIBRATED`. M-3 is one of the calibration-debt candidates per `ml_layer_architecture_bible:§ 5.2` (UNCALIBRATED count + index). The architectural debt: a load-bearing model in the displayed-prediction path (rk_core's softmax-output `ranker_probs` is consumed for `handicapping_probs` per `wr_inference_service.py:616-626` BYPASS chain → blended with `market_probs` → `displayed_prob` → `wr_predictions.win_probability`) has no calibration alignment between training-time score distribution and inference-time consumed probability. The post-2026-05-01 ranker-as-probability architectural flip (per `wr_inference_service.py:579-598`) made rk_core/rk_full the source of the displayed probability without simultaneously establishing calibration discipline for the ranker family.

PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=refactor; rationale="rk_core is UNCALIBRATED in the strict sense (no sidecar in S3, no load attempt, no inference-time application) but is a load-bearing model in the displayed-prediction path post-2026-05-01 architectural flip. The within-race softmax produces a probability distribution that is mathematically valid but not score-vs-truth calibrated. Phase A3-era extension of `scripts/fit_all_calibrations.py` to include rk_core (parallel to the gonzo_sauce-only rk_full extension at `wr_inference_service.py:227-238`) is the natural refactor; alternatively, fit a per-race-distribution-shape isotonic that calibrates the post-softmax ranker_probs against actual win frequencies. Consolidation home § 5.3 (Post-2026-05-01 ranker-as-probability flip architectural-calibration consolidation) per Q13 ratification."; cite=wr_inference_service.py:215-217, scripts/fit_all_calibrations.py:24, wr_inference_service.py:579-598, wr_inference_service.py:599-603, wr_inference_service.py:616-626.

Quaternary status: VERIFIED.

**Model Artifact Version Control.** Substrate-grounded version control discipline:

- **Version naming convention.** `ranker_core_<timestamp>.json` per `model/ranker/train.py` artifact-write at `:79-93`. Single-artifact (no per-style suffix family for rk_core).
- **Storage location.** S3 bucket `equine-model-artifacts`; prefix `ranker/`. Path persisted to `model_versions.s3_artifact_path`.
- **`model_versions` registry interaction.** Same pattern as M-1 / M-2: insert with `is_active=False`; flip via `set_active_model(model_version_id)` only on operator `--set_active`. Single-active-per-`model_type` invariant per `model_version_repository.py:13`. Model_type for rk_core: `ranker_core`.
- **Active-row selection discipline.** Loader at `wr_inference_service.py:215-217` uses single-item priority list (`['ranker_core']`); single-row LIMIT 1 against `is_active = TRUE` selection.

Quaternary status: VERIFIED.

**Deployment Gating.** Substrate-grounded deployment-gate discipline:

- **Pre-deployment checks.** Operator manual review per `model/training/train.py:667-668`. **No automated calibration check** because rk_core is UNCALIBRATED — calibration_score does not apply.
- **Deployment mechanism.** Same as M-1 / M-2: S3 upload → `model_versions` row insertion with `is_active=False` → operator promotion → Lambda cold-start refresh.
- **Rollback discipline.** Same as M-1 / M-2: registry flip; S3 retention.
- **Post-deployment monitoring.** Same diagnostic scripts (reports-only); no auto-gating. **Critical for M-3 specifically:** because rk_core is load-bearing in the displayed-prediction path (post-2026-05-01 flip) and UNCALIBRATED, the absence of post-deployment drift/calibration-drift gating is a higher-stakes gap for M-3 than for M-1 / M-2 (which are diagnostic-only). Phase 5 maturity gap; cross-reference § 4.2.5 GAP A (drift-based triggers absent — HIGH severity).

Quaternary status: VERIFIED.

**Calibration Discipline Narrative.** rk_core is UNCALIBRATED — distinct from M-1 / M-2's BYPASS state (those have sidecars loaded but unused; rk_core has no sidecar in S3 at all). The architectural finding consolidates at § 5.3 (Post-2026-05-01 ranker-as-probability flip architectural-calibration consolidation) per Tony Q13 ratification — the flip routed displayed probability through the ranker family without establishing calibration discipline for that family, leaving the displayed `win_probability` mathematically valid (sums to 1.0 within race) but not score-vs-truth calibrated. The PHASE_5_BACKLOG_CANDIDATE entry above is the third member (alongside the M-1 dead-load and M-2 dead-load) of the four-member calibration debt candidate group; the fourth member is the line 616-626 BYPASS itself (canonical home § 5.3) which is QB-pre-listed and does not surface as a new candidate.

**Quaternary Status (per spec § 5.9).** Per-column status:
- Success Criteria: **PARTIAL** (calibration_score not operative for ranker; thresholds not encoded for the metrics that are operative).
- Retraining Triggers: **VERIFIED** (`mer:T-5` explicitly N/A for M-3 with substrate citation).
- Calibration Discipline: **VERIFIED** (with PHASE_5_BACKLOG_CANDIDATE consolidation to § 5.3).
- Model Artifact Version Control: **VERIFIED**.
- Deployment Gating: **VERIFIED** (with elevated criticality of post-deployment-monitoring gap noted; § 4.2.5 GAP A reference).

**Notes.** Single-artifact (no per-style specialist family for rk_core; only `ranker_core` general registry name). Hyperparameter snapshot per `model/ranker/config.py` (XGB_PARAMS, NUM_ROUNDS, EARLY_STOPPING_ROUNDS); specifically `objective='rank:pairwise'` per `model/ranker/train.py:83` with rank:pairwise expecting one weight per query group (race) per the inline comment at `model/ranker/train.py:163-164`. Feature set: 58 legacy odds-aware (lean53 cull does NOT apply to rk_core in current production substrate per `mla:M-3 § 5.4`). Training-time/inference-time delta: training writes per-version artifacts with `_meta.json` (objective `'rank:pairwise'`); inference loads bare model only (no calibration sidecar — UNCALIBRATED).

---

#### § 4.1.4 M-4 — `rk_full` (XGBoost rank:pairwise — WR Layer 2, workout-aware)

**M-ID.** `M-4`. Inherited 1:1 from `mla:M-4`.

**Model Name.** Primary identifier: `rk_full_<specialist>` (8-style family same as M-2). Secondary: `ranker_full` (legacy general-only). Cross-reference `mla:M-4 § 5.2`. Training entry point: `model/ranker/train.py` `train_ranker(...)` with `--specialist <style>`.

**Success Criteria.** Same primary/secondary set as M-3. `mer:E-5` calibration_score NOT operative (rank-score domain). Per-specialist independent metric across 8 artifacts. Manual-review gate per `model/training/train.py:667-668`. Quaternary status: PARTIAL (per Directive 1).

**Retraining Triggers.**
- `mer:T-1` Daily-full cadence — covers ranker retrain (all 8 specialists).
- `mer:T-2` Weekly WR cadence — covers rk_full retrain.
- `mer:T-4` Manual operator trigger — per-specialist independent gate.
- `mer:T-5` Calibration sidecar refresh — **partially operative.** Per `scripts/fit_all_calibrations.py:24` ranker is generally excluded; `rk_full_gonzo_sauce` variant has sidecar conditionally loaded at `wr_inference_service.py:227-238` (gonzo_sauce-only) per post-A3 extension. 7 non-gonzo styles have no sidecar.

Quaternary status: VERIFIED.

**Calibration Discipline.** **Lifetime/operational discipline (split warm-start load):** 7 non-gonzo styles have no sidecar / no warm-start load / no inference-time application. The `gonzo_sauce` variant has a sidecar conditionally loaded at `wr_inference_service.py:227-238`; isotonic-regression sidecar fitted by post-A3 extension to `scripts/fit_all_calibrations.py`. **Architectural finding (uniform BYPASS at inference):** per `mla:M-4 § 5.9` calibration state is `BYPASS uniform across all 8 styles`. Operative line: `handicapping_probs = ranker_probs.copy()` at `wr_inference_service.py:626` (no `_apply_calibration` invocation). The comment block at lines 616-625 explicitly states "All styles (including gonzo_sauce) bypass calibration at inference tonight". When the gonzo_sauce sidecar IS loaded into memory at warm-start, line 626's unconditional copy short-circuits any application — so gonzo_sauce is dead-load equivalent to wp_core lean53.

**Bug #15 + Bug #24 chain:** Bug #15 is the gallery-wide calibration interaction; Bug #24 is the specific 0-PP-override-after-calibration interaction that re-introduced the BYPASS for gonzo_sauce. Resolution depends on Phase A3.5 splitting 0-PP horses out of the calibration path (per the comment at `wr_inference_service.py:622-625`). Gonzo sidecar retained in S3 and downloaded at warm-start "for A3.5 use" per line 625.

**Note: this is the QB-pre-listed BYPASS** — the M-4 inference-path BYPASS at `wr_inference_service.py:616-626` is the canonical Bug #15+#24 chain entry on the QB-known list. Per SP-2 standing instruction, NOT surfaced as a new PHASE_5_BACKLOG_CANDIDATE — consolidated at § 5.3 as the fourth member of the calibration debt candidate group (with M-1 dead-load, M-2 dead-load, M-3 UNCALIBRATED).

Quaternary status: VERIFIED.

**Model Artifact Version Control.**
- Naming: `rk_full_<specialist>_<timestamp>.json`. Per-specialist artifact emission (8 styles).
- Storage: S3 `equine-model-artifacts` prefix `ranker/`.
- Registry: same `is_active=False` default + `set_active_model` flip pattern. Per-specialist distinct `model_type`.
- Active-row selection: loader at `wr_inference_service.py:194-198` per-style.

Quaternary status: VERIFIED.

**Deployment Gating.** Same pattern as M-2 / M-3. Per-specialist independent operator gate. Quaternary status: VERIFIED.

**Calibration Discipline Narrative.** M-4 is the canonical Bug #15+#24 chain entry — uniform BYPASS at inference (line 626 unconditional copy) with split warm-start load discipline (gonzo_sauce conditional load; other 7 styles no load). Member 4 of the four-member calibration debt candidate group consolidating at § 5.3. The post-2026-05-01 architectural flip routed displayed `win_probability` through ranker softmax → BYPASS → handicapping_probs; BYPASS is intentional per the operator-narrative but represents architectural debt for Phase A3.5.

**Quaternary Status.** Success Criteria: PARTIAL. Retraining Triggers: VERIFIED. Calibration: VERIFIED (with QB-pre-listed consolidation to § 5.3). Version Control: VERIFIED. Deployment Gating: VERIFIED.

**Notes.** 8-style specialist family per `wr_inference_service.py:101-105`; same set as M-2. Hyperparameter snapshot at `model/ranker/config.py`; `objective='rank:pairwise'` (LambdaMART) per `model/ranker/train.py:83`. `RANKER_FULL_CULL` defines a 51-feature lean51 ranker variant at `model/shared/feature_definitions.py:151-161` but production uses `get_lean53_features()` per `wr_inference_service.py:42` (lean51 not the inference-time set despite dedicated function per `mla:M-4 § 5.10`). Phase 1 ablation rationale at `model/shared/feature_definitions.py:140-150` (+3.6pp top-1, +4.4pp top-3 vs full 66).

---

#### § 4.1.5 M-5 — `pl_core` (XGBoost reg:squarederror — PL Layer 1)

**M-ID.** `M-5`. Inherited 1:1 from `mla:M-5`.

**Model Name.** Primary identifier: `pl_core_<specialist>` (7-style family — NO `gonzo_sauce` per `mla:M-5 § 5.10`). Cross-reference `mla:M-5 § 5.2`. Training entry point: `model/pl/train.py` `train_full_model_only(specialist)` at `model/pl/train.py:124-377`.

**Success Criteria.** Same metric set as M-1 / M-2 (`mer:E-1` through `mer:E-6`). **`mer:E-5` calibration_score IS operative for M-5** — M-5 is CALIBRATED per `mla:M-5 § 5.9`; metric measures alignment of post-softmax-post-isotonic win-probability against actual win frequencies. Per-specialist independent metric across 7 artifacts. Manual-review gate per `model/training/train.py:667-668`. Quaternary status: PARTIAL (per Directive 1 — manual-review-only; no encoded threshold even for the operative calibration_score).

**Retraining Triggers.**
- `mer:T-1` Daily-full cadence — covers pl_core retrain ("PL retrain currently rolls into mer:T-1 daily-full umbrella" per `architecture_overview:3.6` mer:T-3 row).
- `mer:T-3` Weekly PL cadence — **DISABLED** per `architecture_overview:3.6`. Substrate-grounded disposition per Directive 2: "Operator-disabled (PL retrain currently in `equine-daily-retrain-full` umbrella; standalone weekly suspended)". Substrate clarifies disposition (intentional retire post-PL-pipeline-architecture consolidation; PL retrain in daily-full umbrella). Documented in § 4.2.1 narrative; NOT surfaced as PHASE_5_BACKLOG_CANDIDATE.
- `mer:T-4` Manual operator trigger — per-specialist independent gate.
- `mer:T-5` Calibration sidecar refresh — **operative.** pl_core is the **second explicit primary subject** of `scripts/fit_all_calibrations.py` per docstring lines 2-3 + line 12. 7 active pl_core artifacts (general + 6 specialists) calibrated on 2026-04-01 → 2026-04-14 window. Refresh cadence manual.

Quaternary status: VERIFIED.

**Calibration Discipline.** **Lifetime/operational discipline:** sidecar fitted by `scripts/fit_all_calibrations.py:189-190`. Sidecar persisted to `s3://equine-model-artifacts/pl/pl_core_*_<ts>_calibration.json` per docstring line 22. Inference load at `pl_inference_service.py:160-180`. **Architectural finding:** per `mla:M-5 § 5.9` calibration state `CALIBRATED` (isotonic regression via piecewise-linear `np.interp` interpolation; sidecar fit on post-softmax win-prob targets). Sidecar IS applied at inference per `pl_inference_service.py:341-343` (`handicapping_probs = self._apply_calibration(softmax_probs, self.calibration)`); `_apply_calibration` impl at `pl_inference_service.py:182-188`.

**M-5 is the SOLE CALIBRATED-AND-APPLIED trained model** in the production gallery (M-1 / M-2 / M-4 BYPASS; M-3 / M-8 / M-9 / M-11 UNCALIBRATED; M-10 calibrated-by-construction non-trained; M-5 the unique CALIBRATED + applied entity).

Inherited PHASE_5_BACKLOG_CANDIDATE from `mla:M-5 § 5.10` (NOT new in MER): PL pipeline runs same 0-PP-override-after-calibration ordering pattern that produced Bug #24 in WR; PL has not BYPASS'd in response. Disposition pending Derby-window verification per MEDIUM monitored entry. Cross-reference `mla:M-5 § 5.10`.

Quaternary status: VERIFIED.

**Model Artifact Version Control.**
- Naming: `pl_core_<specialist>_<timestamp>.json`. Per-specialist artifact emission (7 styles).
- Storage: S3 `equine-model-artifacts` prefix `pl/`.
- Registry: same pattern. Per-specialist distinct `model_type` (`pl_core_general`, ..., `pl_core_route`).
- Active-row selection: loader at `pl_inference_service.py:93-104` per-style; single-item priority `f'pl_core_{self.style}'`; no legacy alias.

**Cross-pipeline coupling at config level (substrate-cited from `mla:M-5 § 5.10`):** `model/pl/config.py:11-15` re-exports `XGB_PARAMS`, `WORKOUT_XGB_PARAMS`, `NUM_ROUNDS`, `EARLY_STOPPING_ROUNDS`, `WORKOUT_NUM_ROUNDS`, `WORKOUT_EARLY_STOPPING_ROUNDS` from `model/wr/config.py:9-49`. PL Core hyperparameters are physically the same Python objects as WR's — any change to `model/wr/config.py:11-23` propagates immediately to PL training. Version-control concern: WR-only hyperparameter tuning silently changes PL training. Substrate-observed coupling pending architectural review per QB-known list (cross-referenced from MLA, NOT new in MER). Consolidates at § 6.3 (Cross-script registration disparity).

Inherited PHASE_5_BACKLOG_CANDIDATE from `mla:M-5 § 5.11` (NOT new in MER): pl_workout Layer 2 orphaned-artifact pattern — training emits per-specialist Layer 2 artifacts that are never loaded at inference per `pl_inference_service.py:90-92`. LOW severity; disposition kill (per MLA).

Quaternary status: VERIFIED.

**Deployment Gating.** Same pattern as M-1 / M-2. **Important distinction:** because M-5 is CALIBRATED-and-applied, calibration_score has gating relevance for M-5 (does not for M-1 / M-2 / M-4 BYPASS path); operator manual review of `calibration_score` is the only auto-gate-substitute. Per Directive 1, still resolves to PARTIAL on Success Criteria because no encoded threshold gates auto-promotion. Quaternary status: VERIFIED.

**Calibration Discipline Narrative.** M-5 is the architectural exemplar for "calibration discipline that works" in the gallery — sidecar fit by `fit_all_calibrations.py`, applied at inference. None of the other models share this complete discipline. Cross-pipeline coupling at config level (PL hyperparameters = WR hyperparameters by re-export) is a distinct concern from calibration but is the M-5-specific architectural debt entry; consolidates at § 6.3.

**Quaternary Status.** Success Criteria: PARTIAL. Retraining Triggers: VERIFIED. Calibration: VERIFIED. Version Control: VERIFIED (with cross-pipeline coupling cross-reference to § 6.3). Deployment Gating: VERIFIED.

**Notes.** 7-style specialist family per `pl_inference_service.py:60-63` — no `gonzo_sauce` (compare M-2 / M-4 8-style family). Phase A3 gonzo_sauce specialist added to WR pipeline only. Hyperparameter snapshot inherited from `model/wr/config.py:9-22` via `model/pl/config.py:11-15` re-export. EV labels per `model/wr/config.py:42-58`: winners with payout get `win_payout`; winners without payout get `AVG_WIN_PAYOUT = 12.18`; losers get `-1.0`. Training-time vs inference-time delta: training trains TWO layers per specialist (Layer 1 pl_core + Layer 2 pl_workout per `model/pl/train.py:240-360`) but inference loads ONLY Layer 1 per `pl_inference_service.py:90-92`. M-5 is the **sole trained inference model in the entire PL pipeline**.

---

#### § 4.1.6 M-6 — WR Arithmetic Value Overlay (`compute_value_overlay`)

**M-ID.** `M-6`. Inherited 1:1 from `mla:M-6`. Non-trained per § 1.3.

**Model Name.** `compute_value_overlay` (free function at `backend/services/wr_inference_service.py:53-80`). Non-trained; no `model_versions` registry row; no S3 artifact. Cross-reference `mla:M-6 § 5.2`. Invoked at `wr_inference_service.py:683-686` per (race, entry).

**Success Criteria.** Per spec § 5.4: success criteria APPLIES even for non-trained models. M-6 success criterion is **EV-flag accuracy** — i.e., does `is_value=True` (via `edge >= VALUE_MIN_EDGE = 0.05`) correlate with positive realized return on actual race outcomes. Computation: not encoded in source as a discrete metric; would be measured via post-hoc backtest on `wr_predictions.is_value_flag` vs realized payouts (data available in `race_results` table). Threshold: `VALUE_MIN_EDGE = 0.05` per `wr_inference_service.py:47`; `OVERLAY_THRESHOLD` (per `shared.constants`) re-applied in `flag_value` at `wr_inference_service.py:755-770`. Pass/fail discipline: no automated post-hoc EV-flag-accuracy gate exists in source. Quaternary status: PARTIAL — substrate citations for thresholds present; auto-gate threshold for backtested EV-flag accuracy not encoded.

**Retraining Triggers.** **N/A** per § 1.3 — M-6 is arithmetic; no training cycle. The function-defined constants (`VALUE_MIN_EDGE = 0.05`, `VALUE_HALF_KELLY = 0.5`, `VALUE_MAX_KELLY = 0.10`, `VALUE_BANKROLL = 1000.0` per `wr_inference_service.py:46-50`) are version-controlled at the source-code level only. No EventBridge cadence rule, no ECS task family, no `model_versions` row. Quaternary status: N/A.

**Calibration Discipline.** **N/A** per § 1.3 — calibration semantics do not apply to non-trained arithmetic overlays. Per `mla:M-6 § 5.9` calibration state is `BYPASS (non-applicable to arithmetic computation; no model output to calibrate)`. **Parameter discipline substituted:** Kelly fraction caps (`VALUE_HALF_KELLY = 0.5` half-Kelly, `VALUE_MAX_KELLY = 0.10` 10%-of-bankroll cap) and edge threshold (`VALUE_MIN_EDGE = 0.05` 5pp) per `wr_inference_service.py:46-50` constitute the parameter discipline that substitutes for calibration in the ML sense.

Note: M-6's input handicapping_prob inherits whatever calibration state M-3 / M-4 produce — currently BYPASS per § 4.1.4. M-6 therefore operates on uncalibrated within-race-normalized softmax output. This is M-3 / M-4's calibration concern, not M-6's. Quaternary status: N/A.

**Model Artifact Version Control.** **N/A** per § 1.3 — no `model_versions` registry row; version = source-code version of `wr_inference_service.py:46-80`. Deployment via Lambda code update only. Quaternary status: N/A.

**Deployment Gating.** **APPLIES uniformly** per § 1.3. Pre-deployment: code review of `wr_inference_service.py` parameter-constant changes. Mechanism: Lambda code update via `equine-wr-inference` redeploy (per `architecture_overview:3.1`). Rollback: code revert. Post-deployment monitoring: same reports-only diagnostic-script discipline as trained models (no auto-gating). Quaternary status: VERIFIED.

**Calibration Discipline Narrative.** Calibration N/A — M-6 is not a probabilistic-output model. Parameter discipline (Kelly caps + edge threshold) substitutes; documented at § 5.10 Notes per spec § 3.3.

**Quaternary Status.** Success Criteria: PARTIAL. Retraining Triggers: N/A. Calibration: N/A. Version Control: N/A. Deployment Gating: VERIFIED.

**Notes.** Function signature parameter `raw_win_prob` is a misnomer — at the call site (line 683), the argument bound is `handicapping_prob` (post-BYPASS, post-renormalize), not the wp_*-derived raw_win_prob attribute. This naming inconsistency is observable substrate but cosmetic only. Hyperparameter constants at `wr_inference_service.py:46-50`. Kelly variant: half-Kelly capped at 10% bankroll. Value-bet threshold: 5pp edge. Bankroll: $1000. M-6's `is_value` boolean drives `pred.is_value_flag` initial assignment at `wr_inference_service.py:708`; `flag_value` at lines 755-770 re-evaluates via `OVERLAY_THRESHOLD` against `pred.edge_pct` — two-pass flag computation oddity per `mla:M-6 § 5.10`.

---

#### § 4.1.7 M-7 — PL Arithmetic EV/Kelly Overlay (`compute_ev_and_kelly`)

**M-ID.** `M-7`. Inherited 1:1 from `mla:M-7`. Non-trained per § 1.3.

**Model Name.** `PLInferenceService.compute_ev_and_kelly` (instance method at `backend/services/pl_inference_service.py:501-569`). Non-trained; no `model_versions` registry row; no S3 artifact. Cross-reference `mla:M-7 § 5.2`. Distinct from M-6 in parameterization, output schema, and pipeline destination.

**Success Criteria.** Per spec § 5.4: applies. M-7 success criteria are **EV-prediction accuracy + value-bet flag accuracy** — i.e., does `predicted_ev` correlate with realized EV on actual race outcomes, and does `is_value_bet=True` (via `edge >= MIN_EDGE_TO_BET`) correlate with positive realized return. Computation: not encoded in source as a discrete metric; would be measured via post-hoc backtest on `pl_predictions.predicted_ev` and `pl_predictions.is_value_bet` vs realized payouts. Thresholds imported from `shared.constants` at `pl_inference_service.py:27-29`: `MIN_EDGE_TO_BET`, `STRONG_VALUE_THRESHOLD`, `KELLY_FRACTION`, `MAX_BET_PCT`, `BANKROLL`. Pass/fail discipline: no automated post-hoc EV/Kelly accuracy gate exists in source. Quaternary status: PARTIAL.

**Retraining Triggers.** **N/A** per § 1.3 — arithmetic; no training cycle. Constants imported from `shared.constants` per `pl_inference_service.py:27-29` are version-controlled at source-code level. No EventBridge cadence, no ECS task family, no `model_versions` row. Quaternary status: N/A.

**Calibration Discipline.** **N/A** per § 1.3 — same classification as M-6. Per `mla:M-7 § 5.9` calibration state `BYPASS (non-applicable to arithmetic computation)`. Parameter discipline (BANKROLL, KELLY_FRACTION, MAX_BET_PCT, MIN_EDGE_TO_BET, STRONG_VALUE_THRESHOLD per `pl_inference_service.py:27-29`) substitutes for calibration in ML sense.

**Asymmetry with M-6:** M-7's input `handicapping_prob` IS calibrated upstream (M-5 § 5.9 CALIBRATED), so M-7 operates on calibrated probabilities — distinct from M-6 which operates on BYPASS'd handicapping_probs. The two pipelines feed compute-overlay-equivalent computations with different upstream calibration states. Quaternary status: N/A.

**Model Artifact Version Control.** **N/A** per § 1.3 — no `model_versions` registry row; version = source-code version of `pl_inference_service.py:501-569` plus `shared/constants.py` (constant definitions). Deployment via Lambda code update only. Quaternary status: N/A.

**Deployment Gating.** **APPLIES uniformly.** Pre-deployment: code review of method-body or `shared/constants.py` changes. Mechanism: Lambda code update via `equine-pl-inference` redeploy. Rollback: code revert. Post-deployment monitoring: reports-only diagnostic-script discipline. Quaternary status: VERIFIED.

**Calibration Discipline Narrative.** Calibration N/A — arithmetic. Parameter discipline substitutes; cross-reference `mla:M-7 § 5.9` BYPASS-by-category and `pl_inference_service.py:27-29` constants.

**Quaternary Status.** Success Criteria: PARTIAL. Retraining Triggers: N/A. Calibration: N/A. Version Control: N/A. Deployment Gating: VERIFIED.

**Notes.** Asymmetry with M-6: M-7 is NOT a function but an instance method on `PLInferenceService`; mutates input `PLPrediction` objects (assigning attributes) rather than returning a dict. M-7's `kelly_bet_size` cap uses `MAX_BET_PCT` (config constant) not a hardcoded 10% as M-6 does. M-7 produces a `predicted_ev` field that drives ranking at `pl_inference_service.py:474-495`; M-6 does NOT produce an EV field (its analogous output is `kelly_bet`, a dollar amount).

---

#### § 4.1.8 M-8 — Random Forest Longshot Classifier (`longshot_rf` — LS Layer 4)

**M-ID.** `M-8`. Inherited 1:1 from `mla:M-8`.

**Model Name.** Primary identifier: `longshot_rf` (model_versions registry name per `model/longshot/train.py:204`). No specialist family; single artifact. Cross-reference `mla:M-8 § 5.2`. Training entry point: `model/longshot/train.py main()` at line 227-228.

**Success Criteria.** **`mer:E-7` longshot-binary-AUC + longshot-precision/recall-at-K (anticipated metrics; not encoded as discrete metrics in `model/evaluation/metrics.py`).** Per `model/longshot/train.py` (training script) and `mla:M-8 § 5.10`, the canonical longshot_rf evaluation surface is the binary classification metrics for the longshot label (1 iff finish_position==1 AND closing_odds≥10.0 per `model/longshot/config.py:23-29`). The `model/evaluation/metrics.py` race-level metrics (`mer:E-1` through `mer:E-5`) are race-ordering metrics not directly applicable to a per-horse-binary longshot classifier. Pass/fail discipline: operator manual review per `model/training/train.py:667-668`. **No hard threshold encoded.** Quaternary status: PARTIAL.

**Retraining Triggers.**
- `mer:T-1` Daily-full cadence — covers M-8 retrain. ECS `equine-training-daily-full` per `architecture_overview:3.6` invokes `model/longshot/train.py main()` per the training image bundle at `architecture_overview:3.7`.
- `mer:T-4` Manual operator trigger — same `set_active` discipline.
- `mer:T-5` Calibration sidecar refresh — **NOT operative.** M-8 is UNCALIBRATED per `mla:M-8 § 5.9`; no calibration sidecar in S3, no fitting workstream. Per `scripts/fit_all_calibrations.py` docstring lines 21-25, the script targets only `wp_full_*` and `pl_core_*`; M-8 is not in scope.

`mer:T-2` Weekly WR cadence does NOT cover M-8 (M-8 is LS-pipeline; WR weekly retrain scopes win-probability family — wp_*, rk_*). M-8 retrain is via daily-full umbrella only.

Quaternary status: VERIFIED.

**Calibration Discipline.** **Lifetime/operational discipline:** N/A — no calibration sidecar; no `_apply_calibration` invocation. Loader at `ls_inference_service.py:75-87` performs only `pickle.load(f)` for the bare `RandomForestClassifier`; no `_calibration.json` companion fetched. **Architectural finding (DIVERGENT-{TRAIN-INFERENCE} per Directive 4):** per `mla:M-8 § 5.9` calibration state is `UNCALIBRATED`. **However**, per `mla:M-8 § 5.10` the architectural concern is **train/inference feature-handling divergence**, distinct from the dead-load post-architectural-flip family (M-1, M-2, M-4):

- **Training-time:** M-8 trained on full 60-feature space (58 core + `l1_win_prob` + `l2_rank_score`) per `model/longshot/train.py:122` and the rf_features composition pattern at `model/ensemble/train.py:134-138`.
- **Inference-time (degraded):** at `ls_inference_service.py:463-481` `_predict_rf_simplified` only 3 of the 60 features are populated (`x[58] = raw_wp`, `x[59] = rank_score`, `x[3] = ml_odds`); the other 57 features are zero-padded (`x = np.zeros(60)` at line 475).
- The inline comment at `ls_inference_service.py:464-470` documents this degradation: "Simplified RF prediction using available features. The full RF expects 60 features, but at enrichment time we only have the base layer outputs + odds. Use predict_proba on a zero-padded feature vector with the key features (l1_win_prob, l2_rank_score) in the right positions."

This is DIVERGENT-{TRAIN-INFERENCE} discipline: training and inference feature-handling differ deterministically; the model is trained with one feature distribution and queried with a different (degenerate) feature distribution. Calibration-drift implications: even if M-8 produced calibrated outputs at training-time-feature-distribution, querying with zero-padded features produces outputs at a different (untrained) point in feature space — calibration alignment is broken by construction.

**Bayesian-decision-theoretic implication:** RF `predict_proba` returns proportion of trees voting for each class; the proportion is meaningful only on the training-data feature distribution. Zero-padded queries are out-of-training-distribution by construction; the proportion has no calibrated interpretation in this regime.

PHASE_5_BACKLOG_CANDIDATE: severity=HIGH; disposition=refactor; rationale="M-8 inference at ls_inference_service.py:463-481 zero-pads 57 of 60 feature inputs. The RF was trained on full 60-feature space (model/longshot/train.py:122-129); inference degradation is acknowledged in the inline comment ('not ideal but avoids recomputing'). DIVERGENT-{TRAIN-INFERENCE} feature-handling produces calibration-drift by construction — RF predict_proba output is meaningful only on training-data feature distribution, and zero-padded queries are out-of-distribution. Either (a) populate the full 60-feature vector at LS inference time by joining wr_predictions with feature_engineering, OR (b) retrain M-8 on the 3-feature subset that's actually populated at inference, OR (c) drop M-8 from the LS pipeline if the degraded inference is empirically equivalent to a 3-feature classifier. Distinct architectural concern from wp_core/wp_full dead-load family (which is post-architectural-flip dead-load, not train/inference divergence). Consolidation home § 5.2 separate sub-entry per Directive 4."; cite=ls_inference_service.py:463-481, model/longshot/train.py:122-129.

Quaternary status: VERIFIED.

**Model Artifact Version Control.**
- Naming: `longshot_rf_<timestamp>.pkl` (pickle persistence per `model/longshot/train.py:200-201`). Single artifact (no specialist family).
- Storage: S3 `equine-model-artifacts` prefix `longshot/`.
- Registry: same `is_active=False` default + `set_active_model` flip pattern.
- Active-row selection: loader at `ls_inference_service.py:75-87`; single-row LIMIT 1 against `is_active = TRUE` for `model_type='longshot_rf'`.

Quaternary status: VERIFIED.

**Deployment Gating.** Same pattern as trained models. Operator manual review per `model/training/train.py:667-668` (no automated gate). Lambda cold-start refresh on `equine-ls-inference`. **Critical for M-8 specifically:** because of DIVERGENT-{TRAIN-INFERENCE} feature handling, conventional pre-deployment checks (validation-set metrics) do not capture the inference-time degradation. Phase 5 maturity gap (cross-reference § 4.2.5 GAP A — drift-based triggers absent — would catch this if implemented). Quaternary status: VERIFIED.

**Calibration Discipline Narrative.** M-8 is the canonical entry for the train/inference-divergence calibration concern. **Distinct from wp_core/wp_full dead-load family** (which is post-architectural-flip dead-load) per Directive 4. M-8's HIGH severity arises because (a) the model is load-bearing in the LS pipeline (feeds M-11 ensemble + longshot_alert composite + storage); (b) the train/inference divergence breaks calibration by construction (out-of-distribution queries at inference). Consolidates at § 5.2 as a separate sub-entry alongside the dead-load family but tagged distinctly.

**Quaternary Status.** Success Criteria: PARTIAL. Retraining Triggers: VERIFIED. Calibration: VERIFIED (with HIGH-severity NEW PHASE_5 candidate consolidating to § 5.2 separate sub-entry). Version Control: VERIFIED. Deployment Gating: VERIFIED.

**Notes.** Hyperparameters per `model/longshot/config.py:9-18` (`RF_PARAMS`): `n_estimators=500, max_depth=10, min_samples_leaf=20, min_samples_split=40, max_features='sqrt', class_weight='balanced', random_state=42, n_jobs=-1`. `LONGSHOT_ODDS_THRESHOLD = 10.0` at `model/longshot/config.py:20`. M-8 part of dual-write LS pipeline (`equine-ls-inference` Lambda; writes to both `ls_predictions` AND `wr_predictions` per `database_schema_bible:4.1.14` F.3).

---

#### § 4.1.9 M-9 — LSTM Form Trajectory (`trajectory_lstm` — LS Layer 5)

**M-ID.** `M-9`. Inherited 1:1 from `mla:M-9`.

**Model Name.** Primary identifier: `trajectory_lstm` (model_versions registry name per `model/trajectory/train.py:295`). No specialist family; single artifact. Cross-reference `mla:M-9 § 5.2`. Training entry point: `model/trajectory/train.py main()`. Inference class definition mirrored at `backend/services/ls_inference_service.py:39-56` (`TrajectoryLSTM(torch.nn.Module)`).

**Success Criteria.** Per `model/trajectory/train.py:194` training-time loss is `BCEWithLogitsLoss`; XGB-style metrics (`mer:E-1` through `mer:E-6`) are not directly applicable. Anticipated success criteria: BCE loss on validation set + AUC-ROC (binary classifier metrics). Not encoded as discrete metrics in `model/evaluation/metrics.py`. Pass/fail discipline: operator manual review per `model/training/train.py:667-668`. No encoded threshold. Quaternary status: PARTIAL.

**Retraining Triggers.**
- `mer:T-1` Daily-full cadence — covers M-9 retrain via ECS `equine-training-daily-full`.
- `mer:T-4` Manual operator trigger — same `set_active` discipline.
- `mer:T-5` Calibration sidecar refresh — **NOT operative.** M-9 UNCALIBRATED per `mla:M-9 § 5.9`; no isotonic sidecar fitted by `scripts/fit_all_calibrations.py` (script targets only wp_full + pl_core).

Note: M-9 has a **separate `_scaler.pkl` companion** loaded if present at `ls_inference_service.py:99-109` (sklearn `MinMaxScaler` for input feature normalization). The scaler is NOT a calibration sidecar — it is input-feature normalization fitted at training time and persisted alongside the model. Refresh cadence: bundled with model retrain (`mer:T-1`).

Quaternary status: VERIFIED.

**Calibration Discipline.** **Lifetime/operational discipline:** N/A — no calibration sidecar; no `_apply_calibration` invocation. Loader at `ls_inference_service.py:90-118` performs `torch.load(local_pt, map_location='cpu', weights_only=True)` + `load_state_dict(...)`; no `_calibration.json` companion fetched. **Architectural finding:** per `mla:M-9 § 5.9` calibration state is `UNCALIBRATED`. BCE-trained binary classifier with sigmoid output is mathematically calibrated only under perfect training-data fit (Platt-style asymptotic calibration); in practice sigmoid outputs from PyTorch BCE training are uncalibrated unless explicitly post-fit calibrated.

The `2.0 * prob - 1.0` mapping at `ls_inference_service.py:525` is a domain-mapping convention (sigmoid → signed score in [-1, +1]), NOT a calibration transform. **LSTM-specific calibration discipline note:** unlike XGBoost binary:logistic where isotonic sidecars are a natural post-fit calibration, BCE-trained LSTM sigmoid outputs would require a similar isotonic post-fit calibration step. None is currently fitted. The `2x-1` mapping further obscures the calibration question because the [-1, +1] range is conventional rather than calibrated.

PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=refactor; rationale="M-9 trajectory_lstm output is consumed by M-11 ensemble feature (index 3 'trajectory_score') and by longshot_alert composite (`traj_score > 0.0` conjunct at ls_inference_service.py:347) in raw 2x-1-mapped form; UNCALIBRATED with no isotonic post-fit. LSTM-specific calibration discipline gap distinct from XGB BYPASS family — BCE-trained sigmoid outputs are uncalibrated by default and the 2x-1 mapping is conventional not calibration. Either fit isotonic post-calibration on validation 2x-1-mapped outputs vs actual positive-trajectory frequencies, or document the conventional-not-calibrated semantic explicitly in storage column comments. Phase 5 calibration debt entry distinct from M-3 / M-8 / M-11 UNCALIBRATED entries because of the LSTM-specific BCE+sigmoid+2x-1 chain"; cite=ls_inference_service.py:483-525, model/trajectory/train.py:194.

Quaternary status: VERIFIED.

**Model Artifact Version Control.**
- Naming: `trajectory_lstm_<timestamp>.pt` (PyTorch state-dict format per `torch.save(model.state_dict(), ...)`). Companion artifact: `<base_key>_scaler.pkl` (MinMaxScaler).
- Storage: S3 `equine-model-artifacts` prefix `trajectory/`.
- Registry: same pattern.
- Active-row selection: loader at `ls_inference_service.py:90-118`.

**Architecture-mirroring discipline:** the inference-side `TrajectoryLSTM` class definition at `ls_inference_service.py:39-56` MUST match `model/trajectory/train.py:44-52` exactly per the docstring at `ls_inference_service.py:40` ("Must match model/trajectory/train.py architecture exactly"). Any change to training-time architecture must be mirrored in the inference class definition — version-control concern.

Quaternary status: VERIFIED.

**Deployment Gating.** Same pattern as M-8. Operator manual review; Lambda cold-start refresh. Architecture-mirroring discipline (above) is a deployment-gating concern: deploying a trained `<timestamp>.pt` artifact whose architecture diverges from inference-side class definition will silently fail at `load_state_dict` (or worse, succeed with weight-shape mismatch causing inference output corruption). No automated check enforces architecture-mirroring; manual code-review at training-side architecture changes. Quaternary status: VERIFIED.

**Calibration Discipline Narrative.** M-9 is LSTM-specific UNCALIBRATED — distinct from M-3 / M-8 / M-11 UNCALIBRATED in that the BCE+sigmoid+2x-1 chain has its own calibration semantic gap. Consolidates at § 5.2 alongside other UNCALIBRATED entries.

**Quaternary Status.** Success Criteria: PARTIAL. Retraining Triggers: VERIFIED. Calibration: VERIFIED (with NEW MEDIUM PHASE_5 candidate consolidating to § 5.2). Version Control: VERIFIED. Deployment Gating: VERIFIED.

**Notes.** Architecture-mirroring discipline at `ls_inference_service.py:40`. SEQUENCE_LENGTH=5 hardcoded at `ls_inference_service.py:35` and `model/trajectory/config.py:7`; FEATURES_PER_STEP=8 hardcoded at both sites. The 8-feature sequence per `model/trajectory/config.py:11-20` is fixed schema. Sequence-build code at `ls_inference_service.py:498-512` constructs the (SEQUENCE_LENGTH, FEATURES_PER_STEP) tensor with right-aligned PP rows and zero-padding for shorter sequences. Hyperparameters per `model/trajectory/config.py:21-29` (`LSTM_PARAMS`): `hidden_size=32, num_layers=2, dropout=0.3, learning_rate=0.001, epochs=50, batch_size=256, patience=10`.

---

#### § 4.1.10 M-10 — Beta-Binomial Bayesian Angle Scorer (LS Layer 6)

**M-ID.** `M-10`. Inherited 1:1 from `mla:M-10`. Non-trained per § 1.3.

**Model Name.** `model/angles/scorer.py:score_angle` (free function at `model/angles/scorer.py:33-64`); production consumer at `backend/services/ls_inference_service.py:_score_angles` (instance method at `ls_inference_service.py:527-574`). Cross-reference `mla:M-10 § 5.2`. Non-trained pure statistical computation per the module docstring at `model/angles/scorer.py:1-9`: "No training — pure statistical computation from historical data."

**Success Criteria.** Per spec § 5.4: applies. M-10 success criterion is **angle-stat-coverage adequacy** — the `angle_stats` table (per `database_schema_bible:4.1.15`) must have sufficient rows for trainer-specific (or global fallback) angle computations. Computation: implicit via the trainer-specific-vs-global fallback at `ls_inference_service.py:550-555` (uses `starts < 5` as fallback threshold). Substrate-grounded threshold for adequacy: `starts < 20` per `model/angles/scorer.py:63` `sample_size_adequate` warning. Pass/fail discipline: no automated gate; operator visibility via reports-only diagnostic scripts. Quaternary status: PARTIAL — substrate citations for thresholds present; auto-gate not encoded.

**Retraining Triggers.** **N/A** per § 1.3 — Bayesian posterior is calibrated-by-construction. **No per-model retrain.** Posterior auto-updates from upstream `angle_stats` table refresh per `data_pipeline_bible:4.1.7` (refreshed via `equine-angle-stats-nightly` EventBridge rule per `architecture_overview:3.6`). **Substrate gap:** the EventBridge rule `equine-angle-stats-nightly` targets the INACTIVE `equine-ingestion` Lambda per `architecture_overview:3.6` anomaly note — fire-and-fail. The `angle_stats` table is therefore not currently being refreshed via the nightly cadence; per `architecture_overview:3.6`, this is one of 4 ENABLED-rule-targeting-INACTIVE-Lambda fire-and-fail cases. Operator awareness of this gap is documented in Phase 5 backlog candidate scope per `architecture_overview:3.6` substrate citation. Quaternary status: N/A (no per-model retrain) but substrate-cited dependency gap on `angle_stats` refresh.

**Calibration Discipline.** **Lifetime/operational discipline:** N/A by category — Bayesian posterior is calibrated-by-construction with proper Beta(1,1) uniform prior + observed (wins, starts) data per `model/angles/scorer.py:46-49` and `ls_inference_service.py:558-563`. The analytic posterior mean `(1+wins) / (2+starts)` is the Bayesian-decision-theoretic calibrated MAP estimate of the win rate.

**Architectural finding:** per `mla:M-10 § 5.9` calibration state is `CALIBRATED-BY-CONSTRUCTION`. No isotonic sidecar (non-trained); calibration-by-construction makes isotonic post-fit unnecessary. The `sample_size_adequate` flag at `model/angles/scorer.py:63` warns when `starts < 20` — small-sample-size posteriors are still calibrated estimators but with high variance.

Inherited PHASE_5_BACKLOG_CANDIDATE from `mla:M-10 § 5.10` (NOT new in MER): canonical `model/angles/scorer.py:33-174` supports 7 angles with full CI computation, but production consumer at `ls_inference_service.py:556-572` inlines simplified 3-angle posterior-mean-only computation. LOW severity refactor. Cross-reference `mla:M-10 § 5.10`.

Quaternary status: VERIFIED (calibrated-by-construction).

**Model Artifact Version Control.** **N/A** per § 1.3 — no `model_versions` registry row; version = source-code version of `model/angles/scorer.py` plus `angle_stats` aggregation refresh state per `data_pipeline_bible:4.1.7`. Quaternary status: N/A.

**Deployment Gating.** **APPLIES uniformly.** Pre-deployment: code review of `model/angles/scorer.py` or `ls_inference_service.py:_score_angles` changes. Mechanism: Lambda code update via `equine-ls-inference` redeploy. The `angle_stats` table refresh is a separate flow (gated on `equine-ingestion` Lambda being Active per `architecture_overview:3.1` — currently INACTIVE). Quaternary status: VERIFIED.

**Calibration Discipline Narrative.** Calibrated-by-construction (Bayesian posterior). Per spec § 3.3 N/A treatment. Substrate-cited at `model/angles/scorer.py:46-49`.

**Quaternary Status.** Success Criteria: PARTIAL. Retraining Triggers: N/A. Calibration: VERIFIED. Version Control: N/A. Deployment Gating: VERIFIED.

**Notes.** Two parallel implementations: canonical at `model/angles/scorer.py` (full 7-angle taxonomy + CI) and production-inlined at `ls_inference_service.py:556-572` (3-angle subset, posterior_mean only, no CI). Production-inlined is live substrate; `score_angle` orphaned-module-candidate per `mla:M-10 § 5.10`. Inputs: per-entry angle flags from `entries` (lasix_first_time, blinkers_on) + derived `class_drop` flag from PP join + `angle_stats` aggregations (trainer-specific with global fallback) + morning_line_odds. Beta-Binomial conjugate-prior inference per `model/angles/scorer.py:18-19` (PRIOR_ALPHA=1.0, PRIOR_BETA=1.0 — uniform).

---

#### § 4.1.11 M-11 — Logistic Regression Stacking Ensemble (`ensemble` — LS Layer 7)

**M-ID.** `M-11`. Inherited 1:1 from `mla:M-11`.

**Model Name.** Primary identifier: `ensemble` (model_versions registry name per `model/ensemble/train.py:247`). No specialist family; single artifact. Cross-reference `mla:M-11 § 5.2`. Training entry point: `model/ensemble/train.py main()` at line 96-97.

**Success Criteria.** Same metric set as M-1 / M-2 (`mer:E-1` through `mer:E-6`). M-11's win-probability output IS within-race-coherent (post Pass-2 softmax at `ls_inference_service.py:290-293`), so all race-ordering metrics apply. `mer:E-5` calibration_score IS computed but does not gate deployment because M-11 is UNCALIBRATED per `mla:M-11 § 5.9`. Manual-review gate per `model/training/train.py:667-668`. Quaternary status: PARTIAL.

**Retraining Triggers.**
- `mer:T-1` Daily-full cadence — covers M-11 retrain via ECS `equine-training-daily-full`.
- `mer:T-4` Manual operator trigger — same `set_active` discipline.
- `mer:T-5` Calibration sidecar refresh — **NOT operative.** M-11 UNCALIBRATED per `mla:M-11 § 5.9`; no isotonic sidecar fitted.

Quaternary status: VERIFIED.

**Calibration Discipline.** **Lifetime/operational discipline:** N/A — no calibration sidecar; no `_apply_calibration` invocation. Loader at `ls_inference_service.py:120-132` performs only `pickle.load(f)`. **Architectural finding:** per `mla:M-11 § 5.9` calibration state is `UNCALIBRATED`. Bare `LogisticRegression(C=1.0, class_weight='balanced')` per `model/ensemble/train.py:182-184`; `class_weight='balanced'` re-weights training samples but does not produce calibrated raw `predict_proba` output (class-balancing distorts the Bayes-optimal posterior estimate).

**Stacking-meta-learner-specific calibration concern:** logistic regression on out-of-fold base-model outputs is sometimes informally referred to as "Platt-scaling-like" stacking calibration, but per scikit-learn's `CalibratedClassifierCV` documentation, true Platt scaling requires explicit `method='sigmoid'` fitting on held-out data after the base model is fixed — this pattern is NOT used here. M-11 is a stacking meta-learner, not a per-model Platt calibrator.

Inherited PHASE_5_BACKLOG_CANDIDATE from `mla:M-11 § 5.10` (NOT new in MER): training/inference feature-population disparity. M-11 ensemble training at `model/ensemble/train.py:144-151` uses defaults (0.0) for `trajectory_score`, `angle_ev`, `angle_posterior` — meta-learner trained with 3 of its 6 upstream-model-output features missing. At inference these features ARE populated from M-9 / M-10. The training-vs-inference feature-population disparity could manifest as miscalibrated meta-learner weights for trajectory/angle features. LOW severity monitored. Cross-reference `mla:M-11 § 5.10`.

Quaternary status: VERIFIED.

**Model Artifact Version Control.**
- Naming: `ensemble_<timestamp>.pkl` (pickle persistence per `model/ensemble/train.py:243-244`). Single artifact.
- Storage: S3 `equine-model-artifacts` prefix `ensemble/`.
- Registry: same pattern.
- Active-row selection: loader at `ls_inference_service.py:120-132`.

**Training-data discipline:** per `model/ensemble/train.py:97-98` "CRITICAL: Training on 2025 held-out data ONLY" — meta-learner trained on temporal-holdout data to avoid leakage from base-model in-sample fits. Train/eval split per lines 174-177: first 80% of 2025 → train; last 20% → eval. Version-control-relevant: when base models retrain (M-1 through M-9 + M-10) on data extending past 2025, the holdout window for M-11 stacking training must extend correspondingly to avoid in-sample leakage.

Quaternary status: VERIFIED.

**Deployment Gating.** Same pattern as other LS-pipeline trained models. Operator manual review; Lambda cold-start refresh on `equine-ls-inference`. **Important deployment-gating distinction for M-11:** because M-11's output drives the LS-pipeline canonical `ls_predictions.final_win_probability` (and dual-write to `wr_predictions.ensemble_win_prob` per `database_schema_bible:F.3`), changes to upstream base models (M-1 through M-9, M-10) propagate calibration-implication-changes into M-11's input distribution. Without M-11 retrain, base-model retraining can silently shift M-11's effective calibration. Gating discipline: operator should retrain M-11 whenever upstream base models retrain — not currently encoded as automated dependency. Quaternary status: VERIFIED.

**Calibration Discipline Narrative.** M-11 stacking-meta-learner UNCALIBRATED — distinct from M-3 / M-8 / M-9 UNCALIBRATED entries because of the stacking-on-out-of-fold-base-model-outputs context. The training/inference feature-population disparity (`mla:M-11 § 5.10`) is the M-11-specific architectural concern — distinct from calibration but cross-cuts because feature-population disparity affects calibration-implication-changes when base models retrain. Consolidates at § 5.2 alongside other UNCALIBRATED entries.

**Quaternary Status.** Success Criteria: PARTIAL. Retraining Triggers: VERIFIED. Calibration: VERIFIED. Version Control: VERIFIED (with M-11-retrain-on-base-model-retrain dependency note). Deployment Gating: VERIFIED.

**Notes.** Hyperparameters: `LogisticRegression(C=1.0, class_weight='balanced', max_iter=1000, random_state=42)` per `model/ensemble/train.py:182-184`. 10 features per `ENSEMBLE_FEATURES` at `model/ensemble/config.py:8-19`. Inputs: 6 upstream-model latent inputs + 4 race-context features. Pass-2 within-race softmax + 0-PP override + market_prob blend at `ls_inference_service.py:281-293`. Dual-write to `wr_predictions.ensemble_win_prob` (UPDATE) + `ls_predictions` (INSERT) per `ls_inference_service.py:360-430` and `database_schema_bible:F.3`.

---

### § 4.2 Retraining Trigger Taxonomy (substrate-discovered per Q12)

Per Q12 ratification, drafting CC discovers taxonomy from substrate (does not pre-enumerate categories). Substrate-grounded categories surfaced during § 4.1 row authorship are enumerated here with code-line citations. Categories that should exist per ML-discipline maturity expectations but DO NOT surface in substrate are flagged at § 4.2.5 as architectural debt.

#### § 4.2.1 Cadence-based triggers

Three cadence-based triggers operative in production substrate per `architecture_overview:3.6` EventBridge schedule + `architecture_overview:3.2` ECS task families.

| Trigger ID | Trigger | EventBridge rule | Cron (UTC) | ECS task family | State | Models covered |
|------------|---------|------------------|------------|-----------------|-------|----------------|
| `mer:T-1` | Daily-full | `equine-daily-retrain-full` | `cron(30 2 * * ? *)` | `equine-training-daily-full` | ENABLED | All 8 trained models (M-1, M-2, M-3, M-4, M-5, M-8, M-9, M-11) |
| `mer:T-2` | Weekly WR | `equine-weekly-retrain-wr` | `cron(0 4 ? * MON *)` | `equine-training-win-prob` | ENABLED | M-1, M-2, M-3, M-4 (WR pipeline) |
| `mer:T-3` | Weekly PL | `equine-weekly-retrain-pl` | `cron(0 5 ? * MON *)` | `equine-training-pl` | **DISABLED** | M-5 (PL pipeline) — currently rolled into mer:T-1 daily-full umbrella |

**`mer:T-3` DISABLED disposition (per Directive 2 substrate clarification):** per `architecture_overview:3.6` "Reason DISABLED" column substrate, `mer:T-3` is "Operator-disabled (PL retrain currently in `equine-daily-retrain-full` umbrella; standalone weekly suspended)." Substrate clarifies disposition (intentional retire post-PL-pipeline-architecture consolidation). PL retrain rolls into `mer:T-1`'s daily-full umbrella. Per Directive 2, NOT surfaced as PHASE_5_BACKLOG_CANDIDATE — substrate clarifies disposition.

**Cadence target architectural pattern:** ENABLED rules target ECS task families (NOT Lambdas) — distinct from the inference-side daily rules which target Lambdas. ECS targets do not have the INACTIVE-Lambda fire-and-fail anomaly affecting 4 inference-side rules per `architecture_overview:3.6`. Both `mer:T-1` and `mer:T-2` confirm Active ECS targets per `architecture_overview:3.6` target column.

#### § 4.2.2 Drift-based triggers

**ABSENT in production substrate.** Substrate-discovery per Q12 surfaced zero feature-distribution-drift detection scripts, zero model-prediction-drift detection scripts, zero auto-gating drift monitors across `scripts/`, `model/`, `backend/services/`, `backend/lambdas/`. Existing diagnostic scripts (`scripts/longshot_bias_diagnostic.py`, `scripts/post_calibration_diagnostic.py`, `scripts/lean53_diagnostic.py`) are reports-only per docstring at `scripts/longshot_bias_diagnostic.py:22` ("Doesn't fix anything. Reports.") — they do not gate retraining or rollback. Calibration drift detectable only via non-gating post-hoc diagnostics.

This absence is itself the substrate-discovered finding. Surfaced as GAP A at § 4.2.5 (severity HIGH).

#### § 4.2.3 Performance-based triggers

**ABSENT in production substrate.** Performance metrics ARE computed (`mer:E-1` exacta_hit_rate, `mer:E-2` trifecta_hit_rate, `mer:E-3` top1_accuracy, `mer:E-4` top3_accuracy, `mer:E-5` calibration_score per `model/evaluation/metrics.py`) and persisted to `model_versions` per `model/training/train.py:681-690`. **However**, no encoded threshold-based auto-gate exists for retraining or rollback. Per `model/training/train.py:667-668` explicit comment: "Only set_active=True after manual review of metrics. Never auto-promote."

Manual-review-of-metrics IS operational discipline (not absence-of-discipline), but it is pre-automation. Auto-gating on performance regression is a Phase 5 maturity step. Surfaced as GAP B at § 4.2.5 (severity MEDIUM).

#### § 4.2.4 Manual operator triggers + Calibration-sidecar refresh

Two manual / non-cron trigger categories operative in production substrate.

**`mer:T-4` Manual operator trigger (training-side).** ECS `equine-training-manual` task family per `architecture_overview:3.2`; no EventBridge schedule (operator-triggered via console / CLI). The `set_active` flag at `model/training/train.py:657, 706-707` is the manual gate: training writes the artifact + `model_versions` row with `is_active=False` by default (line 695); flips to `is_active=True` only via `repo.set_active_model(model_version_id)` at line 707 when operator passes `--set_active`. CLI hint at `model/training/train.py:912-914` emits "Review metrics then activate with: ..." when `--set_active` omitted.

Models covered: all 8 trained models. `mer:T-4` is the canonical promotion path — every artifact transition from training to production goes through this manual gate. Substrate-grounded as the single auto-promotion-substitute discipline.

**`mer:T-5` Calibration-sidecar refresh (manual schedule).** `scripts/fit_all_calibrations.py` is a manually-scheduled script (no EventBridge cron); calibration window hardcoded at `scripts/fit_all_calibrations.py:46-47` (`CAL_START = date(2026, 4, 1)`, `CAL_END = date(2026, 4, 14)`). Per docstring lines 1-25, script fits isotonic-regression sidecars for 14 active wp_full + pl_core artifacts. Ranker explicitly excluded per docstring line 24 ("ranker/...   (no — rk skipped per spec)"); rk_full gonzo_sauce was added later as the lone non-wp/pl exception per post-A3 extension.

Models covered (sidecar refresh):
- M-2 (wp_full) — primary explicit subject (8 styles).
- M-5 (pl_core) — primary explicit subject (7 styles).
- M-1 (wp_core) — produced separately by `scripts/fit_lean53_core_calibrations.py` (not by `fit_all_calibrations.py`'s docstring-listed wp_full+pl_core path).
- M-4 (rk_full gonzo_sauce only) — post-A3 extension.

Models NOT covered: M-3 (rk_core), M-6, M-7 (arithmetic — N/A), M-8, M-9, M-10 (calibrated-by-construction non-trained), M-11.

Refresh cadence: manual operator-triggered when calibration drift is empirically observed in diagnostic scripts. **No automated refresh trigger exists in source.**

#### § 4.2.5 Discipline gaps (PHASE_5_BACKLOG_CANDIDATEs)

Three operational ML discipline gap candidates per QB SP-A1 Directive 1, surfaced from substrate-discovered taxonomy.

**GAP A — Drift-based triggers absent (HIGH severity).**

PHASE_5_BACKLOG_CANDIDATE: severity=HIGH; disposition=replace; rationale="Production gallery has zero drift monitoring. No feature-distribution-drift detection in scripts/, model/, backend/services/, backend/lambdas/. No model-prediction-drift detection. Existing diagnostic scripts (longshot_bias_diagnostic, post_calibration_diagnostic, lean53_diagnostic) are reports-only per docstrings ('Doesn't fix anything. Reports.' at longshot_bias_diagnostic.py:22) — they do not gate retraining or rollback. Calibration drift detectable only via non-gating post-hoc diagnostics. Phase 5 maturity step: implement automated drift monitoring with auto-gating on threshold breach. M-3 UNCALIBRATED + load-bearing post-2026-05-01 flip and M-8 DIVERGENT-{TRAIN-INFERENCE} are particularly high-stakes for absence of drift detection because both produce mathematically valid but not score-vs-truth calibrated outputs that drift undetectable to current discipline"; cite=scripts/longshot_bias_diagnostic.py:22 (reports-only docstring), absence-of-drift-monitor across scripts/ + backend/services/ + model/.

**GAP B — Performance-based triggers absent (MEDIUM severity).**

PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=refactor; rationale="Performance metrics ARE computed (exacta_hit_rate, trifecta_hit_rate, top1_accuracy, top3_accuracy, calibration_score per model/evaluation/metrics.py) and persisted to model_versions per database_schema_bible:4.1.11, but DO NOT auto-gate retraining or auto-trigger rollback. Per model/training/train.py:667-668 explicit comment: 'Only set_active=True after manual review of metrics. Never auto-promote.' Manual-review-of-metrics is real discipline (not absence-of-discipline), but pre-automation; auto-gating on performance regression is Phase 5 maturity step. This gap is uniform across 8 trained models — surfaces as the Success Criteria PARTIAL pattern across § 4.1.1 through § 4.1.11 (excluding M-6 / M-7 / M-10 N/A). Three-facet operational ML discipline maturity gap per § 7 consolidation"; cite=model/training/train.py:667-668, model/evaluation/metrics.py.

**GAP C — CDK substrate gap (MEDIUM severity).**

PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=refactor; rationale="EventBridge cadence rules (equine-daily-retrain-full, equine-weekly-retrain-wr, equine-weekly-retrain-pl) and ECS task families (equine-training-daily-full, equine-training-win-prob, equine-training-pl, equine-training-manual) are operative in live AWS state per architecture_overview:3.6 and architecture_overview:3.2 but NOT declared in working-tree CDK at infrastructure/cdk/lib/compute-stack.ts. Operator deploys via direct AWS CLI (or one-time-setup outside CDK) rather than CDK refresh. Deployment reproducibility concern: live-state ground truth diverges from infrastructure-as-code substrate. Phase 5 reconciliation: declare cadence rules + task families in CDK to restore reproducibility"; cite=architecture_overview:3.6 + architecture_overview:3.2 vs infrastructure/cdk/lib/compute-stack.ts (CDK-vs-live-state divergence ratified as Phase 5 reconciliation per QB SP-A1 ratification).

**Three-facet integration:** GAP A + GAP B + uniform Success Criteria PARTIAL across 8 trained models = three facets of single underlying operational ML discipline maturity gap. Consolidated framing at § 7 Deployment Gating Findings Summary per Directive 1.

---

## § 5. Calibration Discipline Findings Summary

Per Q13 ratification, this bible is the canonical home for calibration discipline findings. § 5 consolidates the gallery-wide lifetime/operational calibration substrate plus the architectural calibration debt findings spanning the dead-load post-flip family, the post-2026-05-01 ranker-as-probability flip, the M-8 train/inference divergence, and the LSTM/ensemble UNCALIBRATED-by-default entries.

### § 5.1 Lifetime calibration cadence + sidecar refresh discipline

**Calibration sidecar production substrate.** `scripts/fit_all_calibrations.py` (with companion `scripts/fit_lean53_core_calibrations.py` for wp_core and `scripts/fit_wp_calibration.py` for legacy paths) is the canonical sidecar fitter. Calibration window hardcoded at `scripts/fit_all_calibrations.py:46-47` (`CAL_START = 2026-04-01`, `CAL_END = 2026-04-14` — 14-day out-of-training-data window; training cutoff 2025-12-31 per docstring lines 5-7; holdout 2026-04-15 → 2026-04-26 kept separate per docstring lines 6-7).

**Fitting method.** Isotonic regression via `sklearn.isotonic.IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)` per `scripts/fit_all_calibrations.py:189-190`. Produces `(x_thresholds, y_thresholds)` arrays persisted to S3 as `<base_key>_calibration.json`.

**Inference-time application substrate.** Two `_apply_calibration` impls exist in production:
- `pl_inference_service.py:182-188` (M-5 path; `np.clip(np.interp(raw, xt, yt), 0.0, 1.0)`) — INVOKED at `pl_inference_service.py:341-343`.
- `wr_inference_service.py:326-335` (M-1 / M-2 / M-4 path; analogous interpolation impl) — DEFINED but NOT INVOKED in `predict_race` (post-2026-05-01 architectural flip removed wp_*/rk_full from the displayed-prediction path; sidecars remain dead-loaded).

**Refresh cadence.** Manual (`mer:T-5`); no EventBridge cron. Operator runs `scripts/fit_all_calibrations.py` ad-hoc after retraining cycles or empirically-observed calibration drift. **No automated drift-trigger refresh** — substrate gap surfaces as § 4.2.5 GAP A.

**Per-model calibration discipline matrix (gallery distribution per `mla:5`):**
| State | Count | Models |
|-------|-------|--------|
| CALIBRATED-AND-APPLIED | 1 | M-5 (pl_core) |
| CALIBRATED-BY-CONSTRUCTION | 1 | M-10 (Bayesian angle scorer; non-trained) |
| BYPASS (sidecar loaded but not applied) | 3 | M-1 (wp_core lean53-conditional), M-2 (wp_full unconditional), M-4 (rk_full gonzo_sauce-conditional + uniform line 626 BYPASS) |
| UNCALIBRATED (no sidecar) | 4 | M-3 (rk_core), M-8 (longshot_rf), M-9 (trajectory_lstm), M-11 (ensemble) |
| BYPASS (non-applicable arithmetic) | 2 | M-6 (WR overlay), M-7 (PL overlay) |

Total: 11. Cross-reference `mla:5` for the same distribution (composition-time view).

### § 5.2 Architectural calibration debt findings

Two consolidation sub-groupings per Directive 4 (M-8 separate from dead-load family).

#### § 5.2.1 Dead-load post-architectural-flip family (M-1, M-2 — group of 2; M-4 line 626 is QB-pre-listed)

**Consolidated finding.** Post-2026-05-01 ranker-as-probability architectural flip (per `wr_inference_service.py:579-598` comment block) routed displayed `win_probability` through ranker softmax (M-3 / M-4 → softmax → BYPASS at line 626 → handicapping_probs → blend → `wr_predictions.win_probability`). The flip removed M-1 wp_core and M-2 wp_full from the displayed-probability path but retained their calibration sidecars in S3 (produced by `scripts/fit_lean53_core_calibrations.py` for M-1 and `scripts/fit_all_calibrations.py` for M-2). Inference loaders continued loading the sidecars at warm-start despite no inference-path consumer existing — dead-load.

**Member entries (3 — 2 NEW + 1 QB-pre-listed):**

1. **M-1 wp_core lean53-conditional dead-load** (NEW per § 4.1.1; SP-A2 surfaced).
   - PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=refactor; cite=wr_inference_service.py:171-178, wr_inference_service.py:326-335.

2. **M-2 wp_full unconditional dead-load** (NEW per § 4.1.2; SP-A2 surfaced).
   - PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=refactor; cite=wr_inference_service.py:205-212, wr_inference_service.py:326-335.

3. **M-4 rk_full uniform BYPASS at line 616-626** (QB-pre-listed Bug #15+#24 chain — NOT new, consolidated per SP-2 standing instruction).
   - cite=wr_inference_service.py:616-626. Resolution depends on Phase A3.5 splitting 0-PP horses out of calibration path. Gonzo_sauce sidecar at lines 227-238 retained "for A3.5 use" per line 625.

**Resolution path (group):** Phase A3.5 architectural unification — either remove the dead-load sidecar fitters + load paths (acknowledge architectural flip is permanent) or wire the sidecars to apply against `pred.raw_win_prob` / `pred.confidence_score` for diagnostic-quality calibrated backtesting outputs. M-4's BYPASS unblocks via 0-PP-handling refactor per the comment at `wr_inference_service.py:622-625`.

#### § 5.2.2 Train/inference feature-handling divergence (M-8 — separate sub-entry per Directive 4)

**Consolidated finding.** M-8 longshot_rf has DIVERGENT-{TRAIN-INFERENCE} feature handling: trained on full 60-feature space (`model/longshot/train.py:122-129`), but at inference only 3 of 60 features are populated (`ls_inference_service.py:463-481` `_predict_rf_simplified`; the other 57 zero-padded). The inline comment at lines 464-470 documents this acknowledged degradation. Calibration-drift implication: RF `predict_proba` proportions are meaningful only on training-data feature distribution; zero-padded queries are out-of-distribution by construction.

**Member entry (1 — NEW per § 4.1.8):**

PHASE_5_BACKLOG_CANDIDATE: severity=HIGH; disposition=refactor; cite=ls_inference_service.py:463-481, model/longshot/train.py:122-129. Distinct architectural concern from the dead-load family (post-architectural-flip dead-load is one architectural debt; train/inference feature-handling divergence is another). Per Directive 4, kept as separate consolidation entry — NOT consolidated into the dead-load family.

#### § 5.2.3 LSTM-specific UNCALIBRATED + 2x-1 mapping (M-9 — separate sub-entry)

**Member entry (1 — NEW per § 4.1.9):**

PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=refactor; cite=ls_inference_service.py:483-525, model/trajectory/train.py:194. Distinct from XGB BYPASS family — BCE-trained sigmoid uncalibrated by default + 2x-1 mapping is conventional not calibration. Calibration debt entry for the LSTM-specific BCE+sigmoid+2x-1 chain.

#### § 5.2.4 Stacking-meta-learner UNCALIBRATED with feature-population disparity (M-11)

**Member entries (1 — INHERITED from `mla:M-11 § 5.10`; NOT new in MER):**

Training-vs-inference feature-population disparity at `model/ensemble/train.py:144-151`: meta-learner trained with `trajectory_score`, `angle_ev`, `angle_posterior` defaulted to 0.0; at inference these features are populated. LOW severity monitored per MLA. Cross-reference `mla:M-11 § 5.10`.

### § 5.3 Post-2026-05-01 ranker-as-probability flip architectural-calibration consolidation

Per Q13 ratification, this is the canonical home for the post-2026-05-01 architectural flip findings. The flip established the ranker family (M-3 / M-4) as the source of displayed `win_probability` without simultaneously establishing calibration discipline for that family, leaving the displayed prediction mathematically valid (within-race-coherent softmax) but not score-vs-truth calibrated.

**Member entries (consolidated 4-member group):**

1. **M-3 rk_core UNCALIBRATED + load-bearing** (NEW per § 4.1.3; SP-A2 surfaced).
   - PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=refactor; cite=wr_inference_service.py:215-217, scripts/fit_all_calibrations.py:24, wr_inference_service.py:579-598, wr_inference_service.py:599-603, wr_inference_service.py:616-626. Higher-stakes than M-1 / M-2 dead-loads because rk_core is load-bearing in the displayed-prediction path — UNCALIBRATED + load-bearing = score-vs-truth alignment broken on the actually-displayed probability.

2. **M-4 rk_full uniform BYPASS at line 616-626** (QB-pre-listed Bug #15+#24 chain).
   - cite=wr_inference_service.py:616-626. Same architectural flip — gonzo_sauce sidecar retained "for A3.5 use" per line 625. Member 4 of the calibration debt candidate group per Q13 ratification.

3. **Architectural flip itself** as canonical event: post-2026-05-01 modification at `wr_inference_service.py:579-598` documented in comment block; routed displayed probability through ranker softmax. The flip's documentation-side concern: line 626's `handicapping_probs = ranker_probs.copy()` short-circuit makes calibration sidecar loads dead-load equivalent across the WR ranker family.

4. **Phase A3.5 unblock dependency:** the BYPASS at line 626 cannot be resolved by simply applying `_apply_calibration` because of the 0-PP-override-after-calibration interaction (Bug #24 per memory `project_ee_bug_24_calibration_0pp_interaction.md`). Resolution requires splitting 0-PP horses out of the calibration path before M-4 / M-3 calibration can be reactivated. Documented at `wr_inference_service.py:622-625`.

**Resolution path:** Phase A3.5 0-PP-handling refactor as architectural prerequisite, then either fit per-race-distribution-shape isotonic against post-softmax `ranker_probs` vs actual win frequencies, or extend `scripts/fit_all_calibrations.py` to include the ranker family (parallel to the gonzo_sauce-only post-A3 extension).

### § 5.4 Calibration discipline PHASE_5_BACKLOG_CANDIDATE consolidated group catalog

**Total NEW PHASE_5_BACKLOG_CANDIDATE entries surfaced in MER under calibration discipline scope:**

| # | Source row | Member of | Severity | Disposition | Description |
|---|------------|-----------|----------|-------------|-------------|
| 1 | § 4.1.1 (M-1) | § 5.2.1 dead-load family | MEDIUM | refactor | wp_core lean53 dead-load |
| 2 | § 4.1.2 (M-2) | § 5.2.1 dead-load family | MEDIUM | refactor | wp_full unconditional dead-load |
| 3 | § 4.1.3 (M-3) | § 5.3 ranker-as-probability flip | MEDIUM | refactor | rk_core UNCALIBRATED + load-bearing |
| 4 | § 4.1.8 (M-8) | § 5.2.2 train/inference divergence | HIGH | refactor | RF zero-padded inference (DIVERGENT-{TRAIN-INFERENCE}) |
| 5 | § 4.1.9 (M-9) | § 5.2.3 LSTM-specific | MEDIUM | refactor | LSTM BCE+sigmoid+2x-1 UNCALIBRATED |

**INHERITED from MLA (NOT new in MER, cross-referenced for consolidation):**

| # | Source row | Member of | Severity | Disposition | Description |
|---|------------|-----------|----------|-------------|-------------|
| - | § 4.1.4 (M-4) | § 5.3 ranker-as-probability flip | (QB-pre-listed) | (depends on A3.5) | rk_full uniform BYPASS at line 626 |
| - | § 4.1.5 (M-5) | § 5.1 lifetime discipline note | MEDIUM | monitored | PL ordering pattern (Bug #24-like; not yet manifested) |
| - | § 4.1.10 (M-10) | § 5.1 production-vs-canonical | LOW | refactor | Inline 3-angle scorer vs canonical 7-angle |
| - | § 4.1.11 (M-11) | § 5.2.4 stacking disparity | LOW | monitored | Train/inference feature-population disparity |

Total NEW from MER calibration discipline scope: **5 NEW + 4 inherited** (cross-referenced) = 9 entries in consolidated catalog.

---

## § 6. Model Artifact Version Control Findings Summary

### § 6.1 Active-row selection discipline

**Pre-known PHASE_5 candidate consolidation home (per QB-known list).** The `model_versions` registry has 88 rows total with 45 simultaneously active under non-deterministic LIMIT 1 selection. The single-active-per-`model_type` invariant per `backend/repositories/model_version_repository.py:13` ("Only one model should have is_active = true") is meant to prevent ambiguity, but a 45-active-row state means 45 distinct `model_type` values each have one active row — which would be normal except that several `model_type` values have legacy aliases that route to the same loader priority chain (e.g., M-1's loader at `wr_inference_service.py:156-160` accepts `win_prob_core_<specialist>`, `win_prob_core`, `win_prob_odds`, `wr_odds` — 4 candidate `model_type` values that could each have one active row, but only one is actually consumed by the priority chain).

The non-determinism enters via the `model_version_repository.py` query for `is_active = TRUE` — if multiple rows of the same model_type have `is_active = TRUE` (which can occur transiently during `set_active_model` UPDATE cycles, or persistently if an UPDATE failed silently), the loader's LIMIT 1 with no explicit ORDER BY produces non-deterministic selection. Cross-reference `database_schema_bible:4.1.11` for `model_versions` table schema.

**Resolution path:** add explicit `ORDER BY created_at DESC` (or analogous deterministic tiebreaker) to the active-row selection query at `model_version_repository.py:13-22, 110-115`, and add periodic database integrity check that no model_type has multiple `is_active = TRUE` rows. Per QB-known list — NOT surfaced as new candidate per SP-2 standing instruction; documented here as canonical consolidation home.

### § 6.2 Retention policy + deprecation lineage

S3 artifacts at `s3://equine-model-artifacts/<prefix>/<artifact>` are NOT subject to automatic deletion in current substrate. `architecture_overview:3.7` notes "Lifecycle policies on each repository are not enumerated here; if relevant, document at Phase 5 backlog." This applies analogously to S3 artifact buckets.

**Retention behavior:**
- Training-time S3 upload at `model/training/train.py` artifact-write writes new `<artifact>_<timestamp>.json|pkl|pt` to S3.
- `model_versions` registry row inserted with `is_active=False` per `model/training/train.py:695`.
- Operator `--set_active` flips `is_active=True` for the new row AND `is_active=False` for the previous active row of the same `model_type` per `model_version_repository.py:90-95`.
- **Deprecated rows are retained in `model_versions` with `is_active=False`.** Their S3 artifacts are also retained.

**Implication.** The 88-row registry (per § 6.1) accumulates over time. Deprecation lineage can be reconstructed via `model_versions.created_at` ordering per `model_type`, but no automated archival or deletion exists. Phase 5 disposition concern: define retention policy (e.g., "retain 5 most recent rows per `model_type`; archive earlier rows + delete S3 artifacts older than 90 days").

### § 6.3 Cross-script registration disparity

**M-5 PL config re-export from WR config (cross-pipeline coupling at version-control-relevant level).** Per § 4.1.5 narrative + `mla:M-5 § 5.10`: `model/pl/config.py:11-15` re-exports `XGB_PARAMS`, `WORKOUT_XGB_PARAMS`, `NUM_ROUNDS`, `EARLY_STOPPING_ROUNDS`, `WORKOUT_NUM_ROUNDS`, `WORKOUT_EARLY_STOPPING_ROUNDS` from `model/wr/config.py:9-49` directly. PL Core's hyperparameters are physically the same Python objects as WR's hyperparameters.

**Version-control implication.** When WR-only hyperparameter tuning changes `model/wr/config.py:11-23`, the change propagates immediately to PL training without explicit acknowledgment in the PL training script or commit log. Substrate-observed coupling — intentional/unintentional classification pending architectural review per QB-known list. Cross-referenced from MLA, NOT new in MER. Consolidation home for the version-control-specific framing of this concern.

**Other cross-script registration patterns (substrate-observed but not flagged):**
- `model/training/train.py` is the legacy generic training script that contains the `set_active`-discipline comment cited at `model/training/train.py:667-668`. Per-pipeline `train.py` scripts (`model/win_prob/train.py`, `model/ranker/train.py`, `model/pl/train.py`, `model/longshot/train.py`, `model/trajectory/train.py`, `model/ensemble/train.py`) reuse the `set_active` discipline by importing or duplicating the registration pattern. The set_active discipline is uniformly applied across all 8 trained models.
- `model/training/train.py` is dual-purpose: it serves as a generic registration helper invoked by per-pipeline scripts AND as the historical legacy single-script training entry point. Disposition (refactor/retire) is Phase 5 concern beyond MER scope.

---

## § 7. Deployment Gating Findings Summary

### § 7.1 Pre-deployment gate discipline

**Uniform manual-review-only gate across 8 trained models** (per Directive 1 ratification). `model/training/train.py:667-668` verbatim: "Only set_active=True after manual review of metrics. Never auto-promote." Operator manual-review process not encoded — substrate-observed reliance on operator discipline. CLI hint at `model/training/train.py:912-914` emits "Review metrics then activate with: ..." when `--set_active` omitted.

**For M-1, M-2, M-3, M-4, M-5, M-8, M-9, M-11 (8 trained):**
- Metrics persisted to `model_versions` per `model/training/train.py:681-690` (`mer:E-1` exacta_hit_rate, `mer:E-2` trifecta_hit_rate, `mer:E-3` top1_accuracy, `mer:E-4` top3_accuracy, `mer:E-5` calibration_score).
- `mer:E-5` calibration_score is operative for M-5 (CALIBRATED-and-applied) but diagnostic-only for M-1 / M-2 / M-4 (BYPASS) and not directly applicable to M-3 / M-8 / M-9 / M-11 in their respective output domains.
- No encoded threshold for any metric.

**For M-6, M-7 (arithmetic):** pre-deployment gate is code review of `wr_inference_service.py:46-80` (M-6) or `pl_inference_service.py:501-569` (M-7) parameter-constant changes. Lambda code update via redeploy.

**For M-10 (Bayesian non-trained):** pre-deployment gate is code review of `model/angles/scorer.py` or `ls_inference_service.py:_score_angles` changes. Plus dependency check on `angle_stats` table refresh state (currently fire-and-fail per `architecture_overview:3.6` anomaly note — `equine-angle-stats-nightly` targets INACTIVE `equine-ingestion`).

### § 7.2 Rollback discipline

**Registry-flip rollback (uniform for 8 trained models).** Operator manually re-flips `is_active` in `model_versions` (CLI / direct DB) → `set_active_model(<previous_artifact_id>)` at `model_version_repository.py:72-95` re-establishes the previous active row. The single-active-per-`model_type` invariant ensures the now-incorrect row is automatically demoted (UPDATE to `is_active = false` at line 90; UPDATE to `is_active = true` at line 95).

**S3 artifact retention** (per § 6.2): rollback target artifact remains in S3 (no auto-delete); rollback is registry-flip only. No artifact restore step required.

**Lambda warm-start refresh limitation:** Lambda warm-start does NOT auto-refresh on `model_versions` UPDATE — new `is_active` selection only takes effect on next Lambda cold-start. For urgent rollback scenarios, operator must manually invalidate Lambda containers (e.g., redeploy Lambda code with no functional change to force cold-start) to ensure rollback takes effect immediately.

**For M-6, M-7, M-10 (non-trained):** rollback is code revert + Lambda redeploy.

### § 7.3 Post-deployment monitoring discipline

**Reports-only diagnostic scripts (no auto-gating).** Existing scripts:
- `scripts/longshot_bias_diagnostic.py` (line 22 docstring: "Doesn't fix anything. Reports.")
- `scripts/post_calibration_diagnostic.py`
- `scripts/lean53_diagnostic.py`

These produce reports for operator review. They do NOT gate retraining or rollback. They are the substrate-observed sole post-deployment monitoring discipline. Phase 5 maturity gap (cross-reference § 4.2.5 GAP A drift HIGH and GAP B performance MEDIUM).

**SNS alerting substrate.** Per `architecture_overview:3.8`, one SNS topic (`equine-equalizer-alerts`) with one subscriber (`tonyragano@gmail.com`); operator-alerting only. No automated retraining or rollback hook on SNS event.

### § 7.4 INACTIVE-Lambda admin-action gating impairment

Per `architecture_overview:3.1` + § 3.6 anomaly note: 3 INACTIVE Lambdas (`equine-ingestion`, `equine-results`, `equine-feature-engineering`) at lock. Of these:
- `equine-ingestion` hosts the admin actions for model lifecycle management: `train` action invokes per-pipeline training (delegated to ECS, so unaffected); `register_model` action inserts `model_versions` row; `set_active_model` action flips `is_active`. These admin actions are non-functional on the INACTIVE Lambda per `architecture_overview:3.6` anomaly note (3 admin actions on INACTIVE Lambda; 2 are EventBridge-triggered → fire-and-fail; the rest manual-invoke and error).
- `set_active_model` admin action at `backend/lambdas/ingestion/handler.py:645` is manually invoked but currently non-functional via the INACTIVE-Lambda mechanism. **However**, operators can flip `is_active` via direct DB UPDATE (psql / RDS Data API) — substrate-grounded operator-workaround.
- `raw_query` admin action at `backend/lambdas/ingestion/handler.py:595` (used for direct DB UPDATE workaround) is also non-functional via the same mechanism. Operator workaround: direct RDS Data API access via `aws rds-data execute-statement` or psql with credentials.

**Implication for deployment gating:** the canonical promotion path (`mer:T-4` `--set_active` flag + `set_active_model` admin action) is partially impaired by the INACTIVE Lambda. Manual-DB-UPDATE workaround maintains operational continuity but is not the architectural-default path. Phase 5 maturity gap — Lambda re-activation pending an explicit `PHASE_5_BACKLOG.md` entry per `architecture_overview:3.6` substrate.

### § 7.5 Three-facet operational ML discipline maturity gap (per Directive 1 consolidation)

Per QB SP-A2 Directive 1, three substrate-grounded facets of a single underlying operational ML discipline maturity gap:

**Facet 1 — GAP A drift detection absent (HIGH).** Zero feature-distribution-drift or model-prediction-drift monitoring across the gallery. Calibration drift detectable only via non-gating post-hoc diagnostics. Detail at § 4.2.5 GAP A.

**Facet 2 — GAP B performance auto-gating absent (MEDIUM).** Performance metrics computed and persisted but no threshold-based auto-gate. Manual-review-of-metrics is real discipline (not absence-of-discipline) but pre-automation. Detail at § 4.2.5 GAP B.

**Facet 3 — Uniform Success Criteria PARTIAL across 8 trained models.** Per Directive 1 finding: "8 of 8 trained models in the production gallery (M-1, M-2, M-3, M-4, M-5, M-8, M-9, M-11) have manual-review-only Success Criteria discipline with zero auto-gating thresholds encoded. Per `model/training/train.py:667-668`: 'Only set_active=True after manual review of metrics. Never auto-promote.' Metrics ARE computed (`mer:E-1` through `mer:E-6`) and persisted to `model_versions`, but no threshold-based auto-gate exists in source. This is uniform architectural debt, not per-model debt."

**Phase 5 prioritization signal:** build the operational discipline layer that makes silent degradation detectable AND auto-gates retraining/deployment on detected degradation. Three-facet gap is the canonical articulation of the operational ML discipline maturity step EE faces post-Phase-1. Cross-references:
- GAP A: § 4.2.5 (HIGH severity drift entry)
- GAP B: § 4.2.5 (MEDIUM severity performance entry)
- Facet 3: per-row PARTIAL Success Criteria across § 4.1.1, § 4.1.2, § 4.1.3, § 4.1.4, § 4.1.5, § 4.1.8, § 4.1.9, § 4.1.11 (8 trained); plus per-row PARTIAL on M-6, M-7, M-10 Success Criteria (3 non-trained whose criteria similarly lack encoded thresholds).

PHASE_5_BACKLOG_CANDIDATE: severity=HIGH; disposition=replace; rationale="Three-facet operational ML discipline maturity gap consolidates GAP A (drift HIGH) + GAP B (performance MEDIUM) + uniform Success Criteria PARTIAL across 8 trained models. Production gallery has substrate-observed manual-only operational discipline; auto-gating layer absent. Phase 5 prioritization: build drift detection + performance auto-gating that closes manual-review-only gap. Members: 8 trained models + 3 non-trained with similar PARTIAL Success Criteria"; cite=architecture_overview:3.6 + 3.2 (substrate cadence rules) + model/training/train.py:667-668 + scripts/longshot_bias_diagnostic.py:22 + per-row § 4.1.X PARTIAL Success Criteria across 11 rows.

---

## § 8. Cross-Reference Index

### § 8.1 mer:M-N → mla:M-N matrix (1:1 inheritance)

| `mer:M-N` | `mla:M-N` | Model | Trained? |
|-----------|-----------|-------|----------|
| `mer:M-1` | `mla:M-1` | wp_core | YES |
| `mer:M-2` | `mla:M-2` | wp_full | YES |
| `mer:M-3` | `mla:M-3` | rk_core | YES |
| `mer:M-4` | `mla:M-4` | rk_full | YES |
| `mer:M-5` | `mla:M-5` | pl_core | YES |
| `mer:M-6` | `mla:M-6` | WR Arithmetic Value Overlay | NO |
| `mer:M-7` | `mla:M-7` | PL Arithmetic EV/Kelly Overlay | NO |
| `mer:M-8` | `mla:M-8` | longshot_rf | YES |
| `mer:M-9` | `mla:M-9` | trajectory_lstm | YES |
| `mer:M-10` | `mla:M-10` | Bayesian angle scorer | NO |
| `mer:M-11` | `mla:M-11` | ensemble | YES |

11 rows; 1:1 inheritance from MLA gallery. Roster reconciliation logged at § 9.8.

### § 8.2 mer:E-N (evaluation criteria) and mer:T-N (retraining triggers) introduction

Entity-class IDs introduced in this bible per Q9 cross-reference convention. Enumerated as encountered during § 4.1 row authorship; final indexing at SP-A3.

**Evaluation criteria (`mer:E-N`):**
- `mer:E-1` exacta_hit_rate (primary; computation `model/evaluation/metrics.py:9-62`)
- `mer:E-2` trifecta_hit_rate (`model/evaluation/metrics.py:65-111`)
- `mer:E-3` top1_accuracy (`model/evaluation/metrics.py:114-150`)
- `mer:E-4` top3_accuracy (`model/evaluation/metrics.py:153-189`)
- `mer:E-5` calibration_score (1.0 - ECE; `model/evaluation/metrics.py:192-258`)
- `mer:E-6` ndcg (XGB-internal eval_metric; `model/win_prob/train.py:66, model/training/train.py:609 best_ndcg`)

**Retraining triggers (`mer:T-N`):**
- `mer:T-1` Daily-full cadence (EventBridge `equine-daily-retrain-full` @ `cron(30 2 * * ? *)`; ECS `equine-training-daily-full`)
- `mer:T-2` Weekly WR cadence (EventBridge `equine-weekly-retrain-wr` @ `cron(0 4 ? * MON *)`; ECS `equine-training-win-prob`)
- `mer:T-3` Weekly PL cadence (EventBridge `equine-weekly-retrain-pl` @ `cron(0 5 ? * MON *)` — DISABLED; ECS `equine-training-pl`)
- `mer:T-4` Manual operator trigger (set_active discipline at `model/training/train.py:657, 706-707`; CLI `--set_active` flag)
- `mer:T-5` Calibration sidecar refresh (manual schedule; `scripts/fit_all_calibrations.py:46-47` calibration window 2026-04-01 → 2026-04-14)

[Additional `mer:E-N` and `mer:T-N` may surface during § 4.1.4-§ 4.1.11 authorship; final index at SP-A3.]

### § 8.3 fp:F-N references in narrative columns

**Zero `fp:F-N` references emitted in any § 4.1 row narrative or § 4.2 / § 5 / § 6 / § 7 consolidated findings.** Per Q11 ratification, FP is canonical home for per-feature monitoring; MER cross-references via `fp:F-N` only when feature-distribution-drift retraining triggers are operative. Substrate-discovery per § 4.2.2 surfaced drift-based triggers as ABSENT in production substrate (the absence is the substrate-discovered finding, surfaced as § 4.2.5 GAP A HIGH severity). Therefore zero per-feature drift signals exist to cross-reference — zero `fp:F-N` references is the correct count for this v1-draft.

If § 4.2.2 drift-based triggers are added in a future Phase 5 iteration, `fp:F-N` references would surface at the per-trigger taxonomy entries pointing to the specific feature being drift-monitored.

---

## § 9. Verification Log

Per spec § 9: inheritance read inventory + substrate path inventory + 9-check self-audit + retraining-trigger taxonomy substrate-grounding inventory + calibration discipline architectural-finding consolidation inventory + cross-reference inventory + UPSTREAM-CORRECTION findings + roster reconciliation.

### § 9.1 Inheritance read inventory

Per spec § 2 inheritance bundle. Read scope honestly characterized:

| # | Item | Path | Bytes | Read scope at session |
|---|------|------|-------|---------------------|
| 1 | META_PLAN v9 | `docs/bible/_meta/META_PLAN.md` | 155598 | Consulted by reference (Phase 0 substrate per Lesson § 4.X banked) |
| 2 | BIBLE_STRUCTURE_SPEC v6 | `docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` | 128884 | Consulted by reference; § 5 common structure + § 6.4-6.6 worked examples informed authorship |
| 3 | AUDIT_METHODOLOGY v2-patched | `docs/bible/_meta/AUDIT_METHODOLOGY.md` | 120635 | Consulted by reference (9-check Cluster I/II/III applied at § 9.3) |
| 4 | CONVERGENCE_CRITERIA v2 | `docs/bible/_meta/CONVERGENCE_CRITERIA.md` | 44781 | Consulted by reference |
| 5 | TRIAGE_QUEUE_SPEC v1 | `docs/bible/_meta/TRIAGE_QUEUE_SPEC.md` | 43865 | Consulted by reference (PHASE_5_BACKLOG_CANDIDATE format applied) |
| 6 | Architecture Overview v3 | `docs/bible/architecture_overview.md` | 46945 | Load-bearing sections fully read (§ 3.1 Lambda inventory, § 3.2 ECS task families, § 3.6 EventBridge schedule, § 3.7 ECR repos, § 3.8 SNS/Secrets) |
| 7 | D&S Bible v1-patched-d2 | `docs/bible/database_schema_bible.md` | 98403 | Consulted at point-of-use (`model_versions` § 4.1.11 + `angle_stats` § 4.1.15 referenced at narrative columns) |
| 8 | Data Pipeline Bible v1-patched-c | `docs/bible/data_pipeline_bible.md` | 69362 | Consulted at point-of-use (§ 4.1.5 per-pipeline inference + § 4.1.7 angle_stats refresh) |
| 9 | FP v1-draft | `docs/bible/feature_provenance_bible.md` | 144455 | Consulted by reference; zero `fp:F-N` references emitted per § 8.3 |
| 10 | MLA v1-draft | `docs/bible/ml_layer_architecture_bible.md` | 149371 | Load-bearing sections fully read (§ 4.1 all 11 model rows + § 5 calibration findings); 1:1 inheritance per § 8.1 |
| 11 | QB Handoff Parallel Cohort | `docs/bible/_meta/QB_HANDOFF_PARALLEL_COHORT_DRAFTING.md` | 15964 | Fully read |
| 12 | This bible's drafting spec | `docs/bible/_meta/QB_DRAFTING_SPEC_MODEL_EVALUATION_RETRAINING_BIBLE.md` | ~30000 | Fully read |

Total: 12 items, ~1,068,263 bytes inherited substrate.

### § 9.2 Substrate path inventory

Per spec § 4 substrate authorization (domains A, A', B, C, D, E, F, G; H not attempted).

| Path | Lines accessed | Purpose |
|------|---------------|---------|
| `backend/services/wr_inference_service.py` | 1-891 (full file via Read in MLA inheritance + targeted via grep) | M-1, M-2, M-3, M-4, M-6 calibration substrate; BYPASS chain at lines 616-626; per-style dispatch at 524-578; constants at 46-50 (M-6 parameter discipline) |
| `backend/services/pl_inference_service.py` | 1-613 (full file via MLA inheritance + targeted) | M-5, M-7 substrate; CALIBRATED chain at 341-369; M-7 compute_ev_and_kelly at 501-569; constants imports at 27-29 (M-7 parameter discipline); pl_workout orphan at 90-92 |
| `backend/services/ls_inference_service.py` | 1-575 (full file via MLA inheritance + targeted) | M-8, M-9, M-10, M-11 substrate; LSTM class def at 39-56; load paths at 70-135; RF zero-padded inference at 463-481; LSTM trajectory at 483-525; angle scoring at 527-574 |
| `model/training/train.py` | 657-715 (set_active discipline) + 681-705 (metrics persistence to model_versions) | `mer:T-4` manual operator trigger discipline; `mer:E-1` through `mer:E-5` persistence sites; "Never auto-promote" comment at lines 667-668 |
| `model/evaluation/metrics.py` | 1-325 (full file) | `mer:E-1` exacta_hit_rate at 9-62; `mer:E-2` trifecta_hit_rate at 65-111; `mer:E-3` top1_accuracy at 114-150; `mer:E-4` top3_accuracy at 153-189; `mer:E-5` calibration_score at 192-258; `print_evaluation_report` at 261-325 |
| `model/win_prob/train.py` | 450-700 (M-1 + M-2 training entry points) | `train_core_model_only` at 464-529 (M-1); `train_full_model_only` at 532-570 (M-2); main argparse at 668-696 |
| `model/win_prob/config.py` | 1-50 | XGB_PARAMS for M-1 / M-2 (binary:logistic; learning_rate=0.05, max_depth=6, etc.) |
| `model/ranker/train.py` | grep targeting line 83 (rank:pairwise) + 163-164 (per-query-group weight comment) | M-3 / M-4 training-time `objective='rank:pairwise'` |
| `model/longshot/train.py` | grep targeting lines 122-129 (60-feature input set) + 136 (bare RandomForestClassifier) + 200-201 (pickle persistence) | M-8 substrate for DIVERGENT-{TRAIN-INFERENCE} narrative |
| `model/longshot/config.py` | 1-30 | `RF_PARAMS` at 9-18; `LONGSHOT_ODDS_THRESHOLD` at 20 |
| `model/trajectory/config.py` | 1-30 | `SEQUENCE_FEATURES` at 11-20; `LSTM_PARAMS` at 21-29 |
| `model/ensemble/train.py` | grep targeting lines 96-97 (2025 holdout) + 144-151 (default 0.0 for trajectory/angle features) + 182-184 (LogisticRegression instantiation) | M-11 training discipline + feature-population disparity inheritance from MLA |
| `model/ensemble/config.py` | 1-40 | `ENSEMBLE_FEATURES` at 8-19 (10 features) |
| `model/angles/scorer.py` | 1-175 (full file via MLA inheritance) | M-10 Beta-Binomial Bayesian computation at 33-64; PRIOR at 18-19; ANGLE_DEFS at 22-30 |
| `model/pl/train.py` | grep targeting lines 124-377 (entry point) + 240-360 (pl_workout orphan) | M-5 substrate for cross-pipeline coupling + pl_workout orphan |
| `model/pl/config.py` | 1-20 | Re-export from WR config at lines 11-15 (cross-pipeline coupling) |
| `model/wr/config.py` | 1-60 | XGB_PARAMS for M-3 / M-4; re-exported into PL via `model/pl/config.py:11-15` |
| `model/shared/feature_definitions.py` | targeted via MLA inheritance (FEATURE_DEFS, GONZO_FEATURE_DEFS, LEAN53_CULL, RANKER_FULL_CULL) | Feature inventory cross-references |
| `model/shared/specialists.py` | targeted via MLA inheritance | Specialist family substrate (8-style for WR, 7-style for PL) |
| `scripts/fit_all_calibrations.py` | 1-100 (head via Read) | Calibration sidecar fitting; CAL_START/CAL_END at 46-47; ranker exclusion at 24; `IsotonicRegression` at 189-190; targets wp_full + pl_core |
| `scripts/longshot_bias_diagnostic.py` | 1-30 (head via grep) | Reports-only docstring at line 22 ("Doesn't fix anything. Reports.") |
| `backend/repositories/model_version_repository.py` | grep targeting lines 13-22 (single-active-per-type invariant comment) + 72-115 (`set_active_model` impl) | Active-row selection discipline; LIMIT 1 non-determinism concern |

Domain coverage:
- A (locked Phase 1 bibles): YES — read at § 9.1
- A' (Phase A v1-draft bibles): YES — FP + MLA read at § 9.1
- B (feature engineering source code): partial via MLA inheritance
- C (model definition source code): YES — model/win_prob, model/ranker, model/longshot, model/trajectory, model/ensemble, model/angles, model/pl
- D (training pipeline scripts): YES — model/training/train.py + scripts/fit_all_calibrations.py + scripts/longshot_bias_diagnostic.py (PRIMARY substrate for retraining-trigger taxonomy per Q12)
- E (inference pipeline scripts): YES — backend/services/wr_inference_service.py + pl_inference_service.py + ls_inference_service.py
- F (model artifact metadata): YES — model_versions registry queried via `model_version_repository.py`
- G (configuration files): YES — model/*/config.py + EventBridge cadence rules cross-referenced via `architecture_overview:3.6`
- H (live database read): NO — deferred per spec § 4

### § 9.3 Self-audit checklist (9 checks across 3 clusters)

Per spec § 10. Each check executed before SP-A3 emission.

**Cluster I — Substrate Verification:**

1. **Inheritance bundle complete (spec § 2 — all 12 items read at session start)** — **PASS.** All 12 items inventoried at § 9.1 with byte counts and read scope. Phase 1 locks (items 6, 7, 8) read at substantive depth for ML-domain content; Phase 0 locks (items 1-5) consulted by reference. Phase A v1-drafts (items 9, 10) read load-bearing-section-fully (MLA § 4.1 all 11 rows + § 5; FP TOC + targeted-section).

2. **Authorized substrate read (domains A, A', B, C, D, E, F, G per § 4 read; H not attempted)** — **PASS.** Substrate path inventory at § 9.2 traverses domains A, A', C, D, E, F, G; B partial via MLA inheritance. Domain H (live database read) explicitly not attempted.

3. **Convention identifiers verified at primary source (Lesson 3 expansion)** — **PASS.** Every model artifact name (`win_prob_core`, `wp_full_<specialist>`, `ranker_core`, `rk_full_<specialist>`, `pl_core_<specialist>`, `longshot_rf`, `trajectory_lstm`, `ensemble`), every EventBridge rule name (`equine-daily-retrain-full`, `equine-weekly-retrain-wr`, `equine-weekly-retrain-pl`), every ECS task family (`equine-training-daily-full`, `equine-training-win-prob`, `equine-training-pl`, `equine-training-manual`), every script name + line citation (e.g., `scripts/fit_all_calibrations.py:46-47, 189-190, 24` ranker-exclusion comment), every calibration sidecar method (`IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)`), every metric function (`exacta_hit_rate`, `trifecta_hit_rate`, etc.) verified at primary source within § 4.1 rows + § 4.2 + § 5 + § 7 narratives.

**Cluster II — Content Verification:**

4. **Forcing function fully served (every per-model row has all schema § 5 forcing-function columns populated; zero empty cells without UNVERIFIED or N/A treatment per § 5.9)** — **PASS.** All 11 rows (M-1 through M-11) populate all 5 forcing-function columns (Success Criteria / Retraining Triggers / Calibration Discipline / Model Artifact Version Control / Deployment Gating). Zero UNVERIFIED rows. Distribution per § 9.3 quaternary status table below.

5. **Internal consistency** — **PASS.** Every `mer:M-N` corresponds 1:1 to `mla:M-N` per § 8.1 matrix (11 rows). Every `mer:E-N` (E-1 through E-6) referenced internally exists in § 8.2 catalog. Every `mer:T-N` (T-1 through T-5) referenced internally exists in § 4.2.1, § 4.2.4, or § 8.2 catalog. Every `mla:M-N` reference is recorded in § 8.1. Zero `fp:F-N` references emitted (per § 8.3 — drift triggers absent, no per-feature drift signals to cross-reference).

6. **Verification claims supported by code-line citations (every threshold, every retraining-trigger taxonomy entry, every calibration sidecar reference has substrate citation per Lesson § 4.11)** — **PASS.** Every retraining-trigger entry in § 4.2.1 has EventBridge rule + cron + ECS task family substrate citations. Every calibration sidecar reference has fitter + storage + load-site citations. Every PARTIAL Success Criteria cell has substrate citation for "thresholds not encoded" (`model/training/train.py:667-668`). Every PHASE_5_BACKLOG_CANDIDATE entry has cite= field with file:line citations.

**Cluster III — Workflow Verification:**

7. **SP-A1 and SP-A2 emissions executed with required artifacts** — **PASS.** SP-A1 executed (TOC + § 1 Scope emitted; Tony resolution: CONTINUE with all 5 findings ratified including Q12 substrate-discovery operating as designed). SP-A2 executed (§ 2 + § 3 + § 4 shell + M-1 / M-2 / M-3 rows emitted; Tony resolution: CONTINUE with 6 findings ratified including PARTIAL Success Criteria as canonical interpretation; 3 directives applied at SP-A3 — Directive 1 § 7.5 three-facet consolidation, Directive 2 mer:T-3 substrate-clarified disposition, Directive 3 `mla:5.2` typo correction at § 4.1.3, Directive 4 M-8 HIGH severity separate consolidation entry).

8. **Cross-reference convention applied per Q9 / Phase A precedent** — **PASS.** Own-bible references use `mer:M-N` / `mer:E-N` / `mer:T-N`. Internal section references use unprefixed `§ <num>` form per Phase A ratification at SP-A1 (banked refinement to AUDIT_METHODOLOGY). Cohort cross-references use `mla:M-N` / `feature_provenance_bible:§ <section>` / `ml_layer_architecture_bible:§ <section>`. Phase 1 lock cross-references use `architecture_overview:<section>`, `database_schema_bible:<section>` / `database_schema_bible:4.1.<table>`, `data_pipeline_bible:<section>` / `data_pipeline_bible:F.<flow>`. **Directive 3 typo correction applied:** `mla:5.2` at § 4.1.3 corrected to `ml_layer_architecture_bible:§ 5.2`. No other similar typos found during self-audit.

9. **Verification log emitted at v1-draft completion** — **PASS.** § 9 of bible is populated and complete before SP-A3 emission.

**Self-audit summary: 9 PASS / 0 FAIL / 0 PARTIAL.**

**Quaternary status distribution across 11 rows × 5 forcing-function columns:**

| Forcing-function column | VERIFIED | PARTIAL | UNVERIFIED | N/A |
|------------------------|----------|---------|------------|-----|
| Success Criteria | 0 | 11 | 0 | 0 |
| Retraining Triggers | 8 | 0 | 0 | 3 (M-6, M-7, M-10) |
| Calibration Discipline | 9 | 0 | 0 | 2 (M-6, M-7) |
| Model Artifact Version Control | 8 | 0 | 0 | 3 (M-6, M-7, M-10) |
| Deployment Gating | 11 | 0 | 0 | 0 |

Total cells: 55. VERIFIED: 36. PARTIAL: 11 (uniform on Success Criteria column). UNVERIFIED: 0. N/A: 8 (concentrated on M-6, M-7, M-10 non-trained models). PARTIAL pattern uniformity confirms Directive 1 ratification: all 11 rows resolve to PARTIAL on Success Criteria for the same substrate-grounded reason (metrics computed and persisted; thresholds not encoded; manual-review-only).

### § 9.4 Retraining-trigger taxonomy substrate-grounding inventory

Per Q12 ratification: drafting CC discovers taxonomy from substrate. Categories surfaced:

| Category | Operative? | Substrate citations |
|----------|-----------|---------------------|
| Cadence-based | YES (§ 4.2.1) | architecture_overview:3.6 (3 EventBridge rules: T-1 daily-full, T-2 weekly-WR, T-3 weekly-PL DISABLED); architecture_overview:3.2 (4 ECS task families) |
| Drift-based | NO (§ 4.2.2 ABSENT) | absence-of-drift-monitor across scripts/ + backend/services/ + model/; reports-only diagnostic scripts at scripts/longshot_bias_diagnostic.py:22 |
| Performance-based | NO (§ 4.2.3 ABSENT) | model/evaluation/metrics.py (computed); model/training/train.py:681-690 (persisted); model/training/train.py:667-668 (NEVER AUTO-PROMOTE) |
| Manual operator | YES (§ 4.2.4) | model/training/train.py:657, 706-707 (set_active discipline); CLI at line 912-914 |
| Calibration-sidecar refresh | YES partially (§ 4.2.4) | scripts/fit_all_calibrations.py:46-47 (calibration window); 189-190 (IsotonicRegression); 24 (ranker exclusion); manual schedule (no cron) |

Five `mer:T-N` entity-class IDs introduced: T-1, T-2, T-3, T-4, T-5. Final per § 8.2.

### § 9.5 Calibration discipline architectural-finding consolidation inventory

Per Q13 ratification: this bible is canonical home. Findings consolidated at § 5:

- § 5.1 Lifetime calibration cadence + sidecar refresh discipline
- § 5.2.1 Dead-load post-architectural-flip family (M-1, M-2 NEW; M-4 line 626 QB-pre-listed)
- § 5.2.2 Train/inference feature-handling divergence (M-8 separate sub-entry per Directive 4 — DIVERGENT-{TRAIN-INFERENCE})
- § 5.2.3 LSTM-specific UNCALIBRATED + 2x-1 mapping (M-9)
- § 5.2.4 Stacking-meta-learner UNCALIBRATED with feature-population disparity (M-11; INHERITED from MLA)
- § 5.3 Post-2026-05-01 ranker-as-probability flip architectural-calibration consolidation (M-3 + M-4)
- § 5.4 Catalog: 5 NEW + 4 inherited = 9 total entries

NEW PHASE_5_BACKLOG_CANDIDATE entries surfaced in MER (counted across all sections):

| # | Source | Severity | Disposition | Description |
|---|--------|----------|-------------|-------------|
| 1 | § 4.1.1 (M-1) | MEDIUM | refactor | wp_core lean53 dead-load (SP-A2 carryover) |
| 2 | § 4.1.2 (M-2) | MEDIUM | refactor | wp_full unconditional dead-load (SP-A2 carryover) |
| 3 | § 4.1.3 (M-3) | MEDIUM | refactor | rk_core UNCALIBRATED + load-bearing (SP-A2 carryover) |
| 4 | § 4.1.8 (M-8) | HIGH | refactor | RF zero-padded DIVERGENT-{TRAIN-INFERENCE} (SP-A3 NEW per Directive 4) |
| 5 | § 4.1.9 (M-9) | MEDIUM | refactor | LSTM BCE+sigmoid+2x-1 UNCALIBRATED (SP-A3 NEW) |
| 6 | § 4.2.5 GAP A | HIGH | replace | Drift-based triggers absent (SP-A3 NEW per Directive 1) |
| 7 | § 4.2.5 GAP B | MEDIUM | refactor | Performance-based triggers absent (SP-A3 NEW per Directive 1) |
| 8 | § 4.2.5 GAP C | MEDIUM | refactor | CDK substrate gap (SP-A3 NEW per Directive 1) |
| 9 | § 7.5 | HIGH | replace | Three-facet operational ML discipline maturity gap (SP-A3 NEW per Directive 1) |

Total NEW PHASE_5_BACKLOG_CANDIDATE entries in v1-draft: **9** (3 from SP-A2 + 6 from SP-A3).

### § 9.6 Cross-reference inventory

**Internal references (own-bible):**
- `mer:M-N`: 11 entries (all M-1 through M-11 referenced in § 4.1, § 8.1, § 9 inventories).
- `mer:E-N`: 6 entries (E-1 through E-6) — § 8.2 catalog + per-row Success Criteria narratives.
- `mer:T-N`: 5 entries (T-1 through T-5) — § 8.2 catalog + per-row Retraining Triggers narratives + § 4.2 taxonomy.

**Cross-bible references (cohort):**
- `mla:M-N`: 11 entries (one per gallery model; § 8.1 1:1 inheritance matrix). Plus per-row sub-section cross-references (`mla:M-1 § 5.2`, `mla:M-1 § 5.9`, etc.) total ~40 sub-section refs.
- `ml_layer_architecture_bible:§ <section>`: 1 instance at § 4.1.3 corrected per Directive 3 (`mla:5.2` typo → `ml_layer_architecture_bible:§ 5.2`).
- `feature_provenance_bible:§ <section>`: 0 explicit references (zero `fp:F-N` references per § 8.3).

**Cross-bible references (Phase 1 locks):**
- `architecture_overview:<section>`: ~25 references throughout § 4.1, § 4.2, § 6, § 7.
- `database_schema_bible:<section>` / `database_schema_bible:4.1.<table>`: ~6 references (model_versions § 4.1.11; angle_stats § 4.1.15; F.3 dual-write).
- `data_pipeline_bible:<section>`: ~3 references (4.1 per-flow; 4.1.5 inference; 4.1.7 angle_stats refresh).

### § 9.7 Findings flagged for UPSTREAM-CORRECTION evaluation

Per spec § 9.7: substrate inconsistencies discovered against locked Phase 1 bibles OR against Phase A v1-drafts. Drafting CC does NOT author UPSTREAM-CORRECTION patches; flags for QB triage only.

**No UPSTREAM-CORRECTION findings surfaced during MER drafting.** Substrate read across Phase 1 locks (Architecture Overview v3, D&S v1-patched-d2, Data Pipeline v1-patched-c) and Phase A v1-drafts (FP, MLA) was consistent with MER's narrative requirements. The single typo correction at § 4.1.3 (`mla:5.2` → `ml_layer_architecture_bible:§ 5.2`) was a MER-internal cross-reference style issue per Directive 3, NOT an upstream substrate finding.

### § 9.8 Roster reconciliation against MLA v1-draft § 4.1

Per spec § 9.8: confirmation that 11-row gallery matches MLA's ratified roster.

| `mer:M-N` | MLA v1-draft § 4.1.X header | Match? |
|-----------|-----------------------------|--------|
| M-1 | § 4.1.1 wp_core (XGBoost binary:logistic — WR Layer 1, no-workout) | ✓ |
| M-2 | § 4.1.2 wp_full (XGBoost binary:logistic — WR Layer 1, workout-aware) | ✓ |
| M-3 | § 4.1.3 rk_core (XGBoost rank:pairwise — WR Layer 2, no-workout) | ✓ |
| M-4 | § 4.1.4 rk_full (XGBoost rank:pairwise — WR Layer 2, workout-aware) | ✓ |
| M-5 | § 4.1.5 pl_core (XGBoost reg:squarederror — PL Layer 1) | ✓ |
| M-6 | § 4.1.6 WR Arithmetic Value Overlay | ✓ |
| M-7 | § 4.1.7 PL Arithmetic EV/Kelly Overlay | ✓ |
| M-8 | § 4.1.8 longshot_rf (LS Layer 4) | ✓ |
| M-9 | § 4.1.9 trajectory_lstm (LS Layer 5) | ✓ |
| M-10 | § 4.1.10 Bayesian angle scorer (LS Layer 6) | ✓ |
| M-11 | § 4.1.11 ensemble (LS Layer 7) | ✓ |

11 rows; 1:1 inheritance verified. Zero discrepancy. Roster reconciliation PASS.

---

**END v1 LOCKED 2026-05-07 (POST-AUDIT) Model Evaluation & Retraining Bible.** Per Q14 ratification, awaiting AUTHORIZE-CORPUS-AUDIT disposition. On disposition, Phase B is COMPLETE; corpus audit gate (Q2) initiates with all three v1-drafts (FP, MLA, MER) reading together.
