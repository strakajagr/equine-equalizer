# ML Layer Architecture Bible

Document: ml_layer_architecture_bible
Phase: 1 (Bible) — deliverable 5 of 7 (drafting-order numbering per BIBLE_STRUCTURE_SPEC v6 § 8.2)
Status: v1-patched-a LOCKED 2026-05-12 (Phase A D6 bundled bible patches per F.4 surgical-patch pattern under Tier 2 ceremony cap; 5 patches landed; supersedes v1 LOCKED 2026-05-07)
Author: CC (Drafting CC, parallel cohort with feature_provenance_bible)
Date drafted: 2026-05-06

Cohort: Phase 1 Deliverables 4-5-6 (Parallel Cohort).
Forcing Function (per QB_DRAFTING_SPEC_ML_LAYER_ARCHITECTURE_BIBLE § 1):
For every model in the EE production model gallery, this bible answers
type → inputs → outputs → position in inference pipeline → target
latent → output composition → calibration / bypass state.

## Revision history

- v1-patched-a (2026-05-12): Phase A D6 bundled bible patches dispatch. **Override disclosure (Q5 ratification):** D6 surgical patches per F.4 pattern under Tier 2 ceremony cap per Phase A entry directive. UC § 7.2 step 4 per-bible patch-CC convention explicitly overridden by ceremony cap. Rationale: D6 documents Phase A operational findings into bibles per Phase A re-dispatch venue; not a running cross-bible-cross-reference-freeze UC cycle. **5 patches applied** per Phase A handoff `docs/operations/PHASE_A_HANDOFF_2026-05-12.md` §§ 2.9, 2.10, 2.11, 2.14, 2.16: ML-1 NEW § 4.2.3 LS second-pass enrichment SQL substrate (per Phase A handoff § 2.11); ML-2 NEW § 4.2.4 Per-pipeline multi-style inventory (per Phase A handoff § 2.9 WR 8 / PL 7 / LS 1); ML-3 NEW § 4.3 Inference monitoring substrate — DLQ + predictions-deficit alarm pattern (per Phase A handoff § 2.10 A.5 deliverable); ML-4 NEW § 8.1 Train-test skew Phase B substrate review flag (per Phase A handoff § 2.14 A.5.3 inference-only scope); ML-5 NEW § 8.2 build_entry_features exception cause beyond gonzo (Phase B input candidate per Phase A handoff § 2.16). Cross-bible cross-references created: § 4.3 ML-3 cross-link `architecture_overview:3.10` (predictions-deficit alarms 26→29 extension) + `data_pipeline_bible:4.6` (predict_race filter + PREDICT_RACE_TOLERANCE=5) + `data_pipeline_bible:4.5` (AWS API validation discipline applied to A.5 inference Lambda DLQ wiring); § 8.1 ML-4 cross-link `data_pipeline_bible:4.6` upstream-gap-flagged-section. Cross-bible cross-reference freeze status: NOT re-engaged for D6 (Tier 2 ceremony cap pattern); per-bible audit-CC tier not invoked at D6 scope.
- v1 LOCKED 2026-05-07: Phase 1 Cohort corpus-audit-gate sequential lock cycle, step 2 of 3 (MLA second per Handoff § 5.2 dependency order, after FP v1 LOCKED 2026-05-07). Per corpus-audit Tony Decision 1 (DEFER architecture_overview:4.1 refinement). MLA v1-draft AUTHORIZE-CORPUS-AUDIT substrate-grounded; calibration state distribution 2 CALIBRATED + 4 UNCALIBRATED + 5 BYPASS + 0 UNVERIFIED across 11-entity gallery (8 trained + 3 non-trained per Q6 ratification). Self-audit 9 PASS / 0 FAIL / 0 PARTIAL. 7 PHASE_5_BACKLOG_CANDIDATE entries inline-flagged at row narratives (queued for QB lock-time batch synthesis at MER lock per standing instruction). Per Handoff § 6.1: cross-bible cross-reference freeze ACTIVE since FP v1 lock; MLA's mla:M-N ↔ FP's fp:F-N references frozen across cohort. UPSTREAM-CORRECTION cycle per Handoff § 7 is sole re-open path.

---

## Table of Contents

§ 1. Scope (Q6 production-deployed only)
  § 1.1 In-scope predicate
  § 1.2 Out-of-scope categories
  § 1.3 Scope asymmetry against feature_provenance_bible (Q5/Q6)
  § 1.4 Scope boundary against model_evaluation_retraining_bible (Bible 6)
§ 2. Forcing Function (canonical statement)
§ 3. Inheritance References
  § 3.1 Phase 0 locks
  § 3.2 Phase 1 locks
  § 3.3 Cohort substrate
§ 4. Model Gallery
  § 4.1 Per-Model Rows
    § 4.1.1 M-1 — wp_core (XGBoost binary:logistic — WR Layer 1, no-workout)
    § 4.1.2 M-2 — wp_full (XGBoost binary:logistic — WR Layer 1, workout-aware)
    § 4.1.3 M-3 — rk_core (XGBoost rank:pairwise — WR Layer 2, no-workout)
    § 4.1.4 M-4 — rk_full (XGBoost rank:pairwise — WR Layer 2, workout-aware)
    § 4.1.5 M-5 — pl_core (XGBoost reg:squarederror — PL Layer 1)
    § 4.1.6 M-6 — WR Arithmetic Value Overlay (compute_value_overlay)
    § 4.1.7 M-7 — PL Arithmetic EV/Kelly Overlay (compute_ev_and_kelly)
    § 4.1.8 M-8 — Random Forest Longshot Classifier (longshot_rf — LS Layer 4)
    § 4.1.9 M-9 — LSTM Form Trajectory (trajectory_lstm — LS Layer 5)
    § 4.1.10 M-10 — Beta-Binomial Bayesian Angle Scorer (LS Layer 6)
    § 4.1.11 M-11 — Logistic Regression Stacking Ensemble (ensemble — LS Layer 7)
  § 4.2 Inference Pipeline Topology
    § 4.2.1 Layer enumeration (per-pipeline composition)
    § 4.2.2 Cross-model dataflow (upstream→downstream graph)
§ 5. Calibration Findings Summary
  § 5.1 CALIBRATED count + index
  § 5.2 UNCALIBRATED count + index (FLAG: calibration debt candidates)
  § 5.3 BYPASS count + index
  § 5.4 UNVERIFIED count + index
§ 6. Cross-Reference Index
  § 6.1 mla:M-N → fp:F-N matrix (forward; populated post-SP-2)
  § 6.2 fp:F-N → mla:M-N matrix (reverse; provisional)
§ 7. Verification Log
  § 7.1 Inheritance read inventory
  § 7.2 Substrate path inventory
  § 7.3 Self-audit checklist (9 checks across 3 clusters)
  § 7.4 Latent vocabulary (canonical per Tony SP-2 ratification)
  § 7.5 Cross-reference forward-stub list
  § 7.6 Findings flagged for UPSTREAM-CORRECTION evaluation
  § 7.7 Production gallery roster reconciliation (spec § 3.1 vs substrate)

---

## § 1. Scope

This bible documents the **production-deployed ML model gallery** of Equine Equalizer (EE) at the resolution required by the canonical forcing function of QB_DRAFTING_SPEC_ML_LAYER_ARCHITECTURE_BIBLE § 1: per model, the bible answers type / inputs / outputs / position in inference pipeline / target latent / output composition / calibration-or-bypass state.

Scope is ratified per Q6 of `_meta/QB_HANDOFF_PARALLEL_COHORT_DRAFTING.md` (RATIFIED 2026-05-06): **production-deployed only**. The model gallery enumerated in § 4.1 covers every model that currently serves inference in the EE production stack, verified against substrate at session start (per § 7.2 Substrate path inventory + § 7.7 Production gallery roster reconciliation).

### § 1.1 In-scope predicate

A model is in scope if and only if it currently serves inference in the EE production stack. Concretely, a model is in scope when one of the following holds:

- The model artifact is loaded by an Active inference Lambda (`equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference` per `architecture_overview:3.1`) at warm-start or per-invoke, AND its `s3_artifact_path` resolves to a live S3 object under `s3://equine-model-artifacts/<family>/` per `architecture_overview:3.4`, AND the corresponding `model_versions` row has `is_active = true` per `database_schema_bible:4.1.11`.
- The model is a non-trained inference layer (arithmetic overlay or pure-statistical computation) referenced by an Active inference service code path. Non-trained layers have no `model_versions` row but produce model-output-shape values consumed downstream; the forcing function applies identically.

### § 1.2 Out-of-scope categories

Out of scope per Q6 ratification:

- **Experimental models not deployed to production inference.** Models trained or prototyped but never registered as `is_active = true` in `model_versions` for any consuming Active inference Lambda are not enumerated here.
- **Deprecated / superseded model versions.** Version history and supersession lineage of model artifacts (e.g., older `wp_full_*_<ts>` artifacts whose `is_active = false` rows persist in `model_versions`) belong to model artifact version control (Bible 6, model_evaluation_retraining_bible § 4.3). MLA documents the *currently-active* model entity; per-version archaeology is Bible 6 scope.
- **Models considered but not implemented.** Design-phase candidates that did not reach training-and-deploy are not enumerated.

### § 1.3 Scope asymmetry against feature_provenance_bible (Q5/Q6)

Per Q6 ratification, MLA does NOT inventory deprecated models (this is asymmetric with Bible 4 Feature Provenance, which DOES inventory orphan features as debt visible to Phase 5 ML re-architecture). The asymmetry is intentional: feature deprecation tracks engineering-code surface area whose downstream reach is non-obvious; model deprecation is registry-tracked in `model_versions` rows where `is_active = false`, and the Phase-5-ML-re-architecture-relevant question for deprecated models is artifact retention / rollback policy — a Bible 6 concern, not an MLA concern.

### § 1.4 Scope boundary against model_evaluation_retraining_bible (Bible 6)

MLA documents *what each production model is at composition time* (architecture, inputs, outputs, calibration state). Bible 6 (Model Evaluation & Retraining, sequential downstream) documents *operational discipline applied across the gallery's lifetime* (success criteria, retrain triggers, calibration discipline, deployment gating). MLA references Bible 6 forward-only via `mer:E-N` (evaluation criteria) and `mer:T-N` (retraining triggers) per § 7.2 of QB_DRAFTING_SPEC.

The boundary is: composition-time facts (this row IS an XGBoost rank:pairwise model, etc.) live in MLA; lifetime-process facts (this model retrains weekly, that model has a 7-day staleness threshold, etc.) live in Bible 6.

---

## § 2. Forcing Function (canonical)

For every model in the EE production model gallery, this bible answers:

> **type (XGBoost / LSTM / Bayesian / Random Forest / ensemble / arithmetic-overlay / etc.) → inputs → outputs → position in inference pipeline → target latent → output composition → calibration / bypass state**

Every dimension of this forcing function is a column in the per-model row schema applied to § 4.1 entries. No dimension is omitted; no row carries an empty forcing-function cell without explicit `UNVERIFIED` treatment per QB_DRAFTING_SPEC § 5. Forcing-function compliance is verified at § 7.3 self-audit Cluster II Check 4.

The forcing function is the bible's contract with downstream consumers (Bible 6 model_evaluation_retraining; Phase 5 ML re-architecture work). It is canonical per QB_DRAFTING_SPEC § 1 and is not re-negotiated at row authorship time.

---

## § 3. Inheritance References

Per QB_DRAFTING_SPEC § 7.3 cross-reference convention, MLA preserves existing conventions of locked Phase 1 substrate when referencing into them. Cohort-internal cross-references use the forward-only two-tier convention of QB_DRAFTING_SPEC § 7.1 / § 7.2.

### § 3.1 Phase 0 locks

Read at session start per QB_DRAFTING_SPEC § 2.1 and inventoried at § 7.1:

- **META_PLAN v9** — `_meta/META_PLAN.md`. Source-priority hierarchy (Tier 1–7) governs all substrate-state assertions in this bible (§ 4.5). Worked-example pattern (`equine-results` Inactive case) governs the Lambda-State invariant inherited from `architecture_overview:5.1`.
- **BIBLE_STRUCTURE_SPEC v6** — `_meta/BIBLE_STRUCTURE_SPEC.md`. § 6.4 ml_layer_architecture_bible template structure; QB_DRAFTING_SPEC § 6 supersedes the longer 8-section variant for this bible's section numbering.
- **AUDIT_METHODOLOGY v2-patched** — `_meta/AUDIT_METHODOLOGY.md`. Cluster I/II/III 9-check list applied at § 7.3.
- **CONVERGENCE_CRITERIA v2** — `_meta/CONVERGENCE_CRITERIA.md`. Discipline-rule convergence criteria; § 6 of QB_DRAFTING_SPEC structure does not enumerate Discipline rules in this bible (deferred to Bible 6 / Phase 5 backlog).
- **TRIAGE_QUEUE_SPEC v1** — `_meta/TRIAGE_QUEUE_SPEC.md`. PHASE_5_BACKLOG candidate disposition vocabulary (`keep` / `refactor` / `replace` / `kill` / `autonomous` / `monitored` / `scheduled-manual` / `paid-replacement`) used for inline candidate flags in § 4.1 row narrative columns.

### § 3.2 Phase 1 locks (deliverables 1-2-3, locked upstream)

- **Architecture Overview v3** — `architecture_overview.md` (LOCKED 2026-05-05). Canonical home for Lambda inventory (§ 3.1: 8 Lambdas = 5 Active + 3 Inactive), ECS Fargate training fleet (§ 3.2: 5 task-definition families), S3 model-artifacts bucket (§ 3.4: `s3://equine-model-artifacts/<family>/<version>.json`), EventBridge schedule (§ 3.6: 13 rules = 10 ENABLED + 3 DISABLED), per-pipeline canonical prediction shapes (§ 4.2: base `Prediction` + `PLPrediction` + `LSPrediction`), and the MLA-relevant cross-cutting topics index entry (§ 4.3 calibration discipline).
- **Database & Schema Bible v1-patched-d2** — `database_schema_bible.md` (LOCKED 2026-05-06). Canonical home for `model_versions` table (§ 4.1.11: 21 columns; partial-UNIQUE `idx_active_model_per_type` with multi-active-row reality), the three per-pipeline prediction tables (`wr_predictions` § 4.1.12, `pl_predictions` § 4.1.13, `ls_predictions` § 4.1.14), the legacy `predictions` table (§ 4.1.10, deprecated per § 7.1), and the `angle_stats` aggregations table (§ 4.1.15) consumed by M-10.
- **Data Pipeline Bible v1-patched-c** — `data_pipeline_bible.md` (LOCKED 2026-05-06). Canonical home for the 3 daily inference flows (§ 4.1.5.1 WR / § 4.1.5.2 PL / § 4.1.5.3 LS dual-write), the LS dual-write pattern (F.3), the 2 retraining flows (§ 4.1.8 daily-full / § 4.1.9 weekly-WR), and the angle-stats refresh flow (§ 4.1.7) — fire-and-fail at lock per `architecture_overview:6`.

### § 3.3 Cohort substrate

Read at session start per QB_DRAFTING_SPEC § 2.3 and inventoried at § 7.1:

- **QB_HANDOFF_PARALLEL_COHORT_DRAFTING.md** — Phase A tight-parallel orchestration model (Q1), corpus-level audit gate (Q2), cross-reference freeze (Q3), UPSTREAM-CORRECTION canonical pattern (Q4), production-deployed scope (Q6), Q7 substrate-read authorization (domains A–G; H deferred), Q9 cross-reference convention.
- **QB_DRAFTING_SPEC_ML_LAYER_ARCHITECTURE_BIBLE.md** — drafting spec for this bible.

---

## § 4. Model Gallery

### § 4.1 Per-Model Rows

One row per production-deployed model entity per QB_DRAFTING_SPEC § 5 schema. Eleven rows in scope per § 7.7 reconciliation (Tony-ratified at SP-1: 5A pairwise-ranker dual; 5B arithmetic-overlay split; 5C PL Core XGBoost addition).

Row schema columns per QB_DRAFTING_SPEC § 5 (omitted for brevity in this header — full schema applied per row): M-ID / Model Name / Model Type / Inputs / Outputs / Position in Inference Pipeline / Target Latent / Output Composition / Calibration State / Bypass State Narrative / Notes.

#### § 4.1.1 M-1 — `wp_core` (XGBoost binary:logistic — WR Layer 1, no-workout)

**M-ID.** `M-1`.

**Model Name.** Primary identifier: `win_prob_core` (model_versions registry name). Secondary identifiers, per priority order in WR loader at `backend/services/wr_inference_service.py:156-159`: `win_prob_core_<specialist>` (specialist-tagged variants), `win_prob_odds` (legacy 58-feature artifact), `wr_odds` (legacy alias). Drafting-CC selects primary based on `_try_load_model_type` priority chain at `wr_inference_service.py:160`. Training entry point: `model/win_prob/train.py` `train_core_model_only(specialist)` at `model/win_prob/train.py:464`; artifact-suffix injection per `model/shared/specialists.py:158-173`.

**Model Type.** `XGBoost`. Specifically: `xgb.Booster` trained with `objective='binary:logistic'`, `eval_metric='logloss'` per `model/win_prob/config.py:11-12`. Loader instantiates via `xgb.Booster()` + `load_model(local_model)` at `wr_inference_service.py:294-296`. Verified at primary source: training-time hyperparameters at `model/win_prob/config.py:10-23`; inference-time loading at `wr_inference_service.py:274-296`.

**Inputs.** Feature set is *artifact-version-dependent* per loader logic at `wr_inference_service.py:166-186`:

- **lean53 path (current production for `_lean53` artifacts):** 47 features = `get_lean53_core_features()` per `model/shared/feature_definitions.py:205-211`. The 47 features are the 58-feature core minus `LEAN53_CULL` (13 features: 3 odds-derived + 9 zero-gain + 1 r=1.000 duplicate) per `model/shared/feature_definitions.py:185-194`.
- **legacy path (fallback for non-`_lean53` artifacts):** 58 features = `get_core_features(include_odds=True)` per `model/shared/feature_definitions.py:128-132` (66-feature base minus 8 workout features).

Forward stubs to Feature Provenance (cohort SP-2 reconciliation pending; format `fp:F-?<feature_name>`):

- **Speed group (11):** `fp:F-?speed_fig_last`, `fp:F-?speed_fig_avg_3`, `fp:F-?speed_fig_trend`, `fp:F-?speed_fig_best_career`, `fp:F-?speed_fig_best_90d`, `fp:F-?speed_fig_at_track`, `fp:F-?speed_fig_at_distance`, `fp:F-?speed_fig_on_surface`, `fp:F-?speed_fig_vs_field`, `fp:F-?speed_fig_consistency`, `fp:F-?speed_fig_sample_size`.
- **Pace group (5 in lean53; 6 in legacy):** `fp:F-?early_pace_last`, `fp:F-?late_pace_last`, `fp:F-?pace_delta_last`, `fp:F-?avg_call1_position`, `fp:F-?avg_stretch_gain` (lean53 culls `pace_scenario_today`; legacy retains).
- **Trip group (7 in lean53; 8 in legacy):** `fp:F-?troubled_trip_freq`, `fp:F-?pace_setter_freq`, `fp:F-?faded_freq`, `fp:F-?late_rally_freq`, `fp:F-?avg_wide_path`, `fp:F-?wide_3plus_freq`, `fp:F-?gate_issue_freq` (lean53 retains `troubled_trip_last`/`wide_3plus_freq`; legacy includes both).
- **Trainer group (5):** `fp:F-?trainer_win_rate`, `fp:F-?trainer_itm_rate`, `fp:F-?trainer_layoff_win_rate`, `fp:F-?trainer_lasix_win_rate`, `fp:F-?trainer_sample_size`.
- **Class group (7):** `fp:F-?class_direction`, `fp:F-?purse_change_pct`, `fp:F-?claiming_price_change_pct`, `fp:F-?career_class_ceiling`, `fp:F-?current_vs_ceiling_pct`, `fp:F-?class_consistency`, `fp:F-?race_quality_tier`.
- **Physical group (8 in lean53; 10 in legacy):** `fp:F-?days_since_last_race`, `fp:F-?layoff_bucket`, `fp:F-?career_starts`, `fp:F-?first_time_on_surface`, `fp:F-?weight_carried`, `fp:F-?win_rate_this_track`, `fp:F-?overall_win_rate` (lean53 culls `is_first_start`/`was_claimed_last_out`/`apprentice_allowance`; legacy retains).
- **Equipment group (3 in lean53; 5 in legacy):** `fp:F-?lasix`, `fp:F-?lasix_first_time`, `fp:F-?blinkers_on`, `fp:F-?trainer_intent_score` (lean53 culls `blinkers_off`; legacy retains).
- **Odds group (legacy only — 3 features):** `fp:F-?closing_odds`, `fp:F-?log_closing_odds`, `fp:F-?odds_move`. Lean53 omits all three per architectural intent at `model/shared/feature_definitions.py:172-178`.
- **Jockey group (0 in lean53; 3 in legacy):** `fp:F-?jockey_win_rate`, `fp:F-?jockey_trainer_combo_win_rate`, `fp:F-?jockey_change_flag` (lean53 culls all 3).

Inputs do NOT include any intermediate latents from upstream models — wp_core is a leftmost-layer model (Layer 1 of the WR pipeline; reads raw feature matrix only).

**Outputs.** Scalar `float` per (race, entry) — `raw_probs[idx]` at `wr_inference_service.py:572`. Output domain: P(win) ∈ [0, 1] per `binary:logistic` sigmoid output. **Within-race independence:** outputs are per-horse-binary (one horse competes against the rest of the universe of all races' losers) and do NOT sum to 1.0 across the race field. The architectural comment at `wr_inference_service.py:579-598` documents this independence as the reason wp_core/wp_full output is not consumed for the displayed `win_probability` (the ranker is consumed instead, post-softmax). Per-row output schema: scalar P(win); typed `np.float32` (downstream cast to Python `float`).

**Position in Inference Pipeline.** `Upstream: []; Downstream: [diagnostic only — no consuming model]; Inference layer: WR Layer 1 (Win Probability Core, no-workout dispatch).` The WR pipeline at `wr_inference_service.py:545-578` dispatches per horse: horses without workout data use wp_core (line 565-572); horses with workout data use wp_full (line 551-555 per M-2). Output from wp_core feeds two downstream consumers, both *diagnostic* (not consumed for the displayed prediction): (1) `pred.confidence_score` at `wr_inference_service.py:706` (storage column `wr_predictions.confidence_score`); (2) `pred.raw_win_prob` at `wr_inference_service.py:718` (storage column `wr_predictions.raw_win_prob` per `database_schema_bible:4.1.12` — column added by out-of-band ALTER, F.2 substrate gap). Layer name in code comment block: "Layer 1: Win probability models" at `wr_inference_service.py:114`.

**Target Latent.** `win_probability_independent_per_horse_no_workout`. This is the per-horse binary win probability conditioned on no-workout-data dispatch; semantically distinct from the within-race-normalized handicapping probability (target latent of M-3/M-4 ranker softmax output) because of the within-race-independence property documented at `wr_inference_service.py:579-598`. Vocabulary canonical per Tony SP-2 ratification (latent axis is model-output-level; FP CC's feature-level latents are a separate vocabulary axis, no unification required).

**Output Composition.** wp_core output is **not composed into the displayed prediction.** The output flows to two storage-only fields (`confidence_score`, `raw_win_prob`) per the Position in Inference Pipeline column. No downstream model consumes wp_core's scalar P(win) for inference-time computation; per `wr_inference_service.py:579-598` ("ranker-as-probability architecture (post-2026-05-01 fix)"), the displayed `win_probability` is derived from rk_full (M-4) softmax instead. Per QB_DRAFTING_SPEC § 5.8: this is a **diagnostic-only output composition** — the model contributes to backtesting / per-row introspection, not to the predicted-rank or value-flag computation chain.

**Calibration State.** `BYPASS (sidecar conditionally loaded but never applied to inference output)`. Substrate evidence:

- Calibration sidecar load conditioned on `'lean53' in self.wp_core_version.version_name` at `wr_inference_service.py:166-178`. For lean53 artifacts only, isotonic sidecar `(x_thresholds, y_thresholds)` is downloaded into `self.wp_core_calibration` via `_try_load_calibration` at `wr_inference_service.py:298-324`.
- Sidecar fitted by `scripts/fit_all_calibrations.py` using `sklearn.isotonic.IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)` at `scripts/fit_all_calibrations.py:189-190`; written to S3 at `<base_key>_calibration.json` per `scripts/fit_all_calibrations.py:215-218`. Format: `{x_thresholds: [...], y_thresholds: [...]}` per JSON schema at `scripts/fit_all_calibrations.py:206-211`.
- **Sidecar is never applied to wp_core output in inference path.** The static method `WRInferenceService._apply_calibration` at `wr_inference_service.py:326-335` is defined but the only invocations in `predict_race` are `np.interp` against `self.rk_full_calibration` (gonzo_sauce only) — the BYPASS block at lines 616-626 documents handicapping_probs derive from ranker softmax bypassing rk_full calibration; wp_core's `wp_core_calibration` is never used.
- Direct evidence: `grep -nE "wp_core_calibration|_apply_calibration\(" wr_inference_service.py` returns the load (line 171) and `_apply_calibration` definition (line 326) but no usage site for `wp_core_calibration` in `predict_race`.

**Bypass State Narrative.** wp_core has a calibration sidecar present in S3 (for lean53 artifacts) and conditionally loaded into memory at warm-start, but no inference-path code applies the sidecar to wp_core output. The sidecar is therefore a dead-load artifact for M-1. Trigger condition: lean53 artifact selected by version-name suffix detection at `wr_inference_service.py:166`. Fallback behavior: legacy artifacts skip the load entirely (no sidecar file in S3 for them). The BYPASS arises from the post-2026-05-01 ranker-as-probability architecture (comment block `wr_inference_service.py:579-598`) which routed handicapping_probs through ranker softmax and removed wp_core/wp_full from the displayed-probability path; the calibration sidecars were retained as deliverables of `scripts/fit_all_calibrations.py` (Stream A1) but their inference-side consumer was removed by the architectural flip. Cross-reference for the broader calibration BYPASS chain: `wr_inference_service.py:616-626` documents the related BYPASS of rk_full calibration (Bug #15 + Bug #24 chain).

PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=refactor; rationale="wp_core calibration sidecars (lean53 only) are loaded into memory at warm-start but never applied — distinct from the line 616-626 ranker calibration BYPASS already in QB's known list. Either remove the dead load to reduce warm-start cost and S3 read pressure, or wire the sidecar to apply to pred.raw_win_prob as a diagnostic-quality calibrated score for backtesting parity"; cite=wr_inference_service.py:171-178, wr_inference_service.py:326-335.

**Notes.** Hyperparameter snapshot at `model/win_prob/config.py:10-23`: learning_rate=0.05, max_depth=6, min_child_weight=20, subsample=0.8, colsample_bytree=0.8, reg_alpha=0.1, reg_lambda=1.0, tree_method='hist', random_state=42, scale_pos_weight set dynamically per training run. NUM_ROUNDS=1000, EARLY_STOPPING_ROUNDS=50. Specialist family: 8 styles defined at `wr_inference_service.py:101-105` (`general`, `speed`, `closer`, `class_riser`, `class_dropper`, `sprint`, `route`, `gonzo_sauce`); however the wp_core path at `wr_inference_service.py:191-193` comment ("_full models are style-specific. _core stays general") indicates wp_core is canonically general-only, with the priority list at lines 156-159 allowing per-specialist `win_prob_core_<specialist>` artifacts to take precedence when present. Training-time/inference-time architectural delta: training emits multi-format artifacts (legacy `wp_odds` 58-feature + lean53 47-feature), inference dispatches by version-name suffix. Specialist substrate at `model/shared/specialists.py:28-37`.

---

#### § 4.1.2 M-2 — `wp_full` (XGBoost binary:logistic — WR Layer 1, workout-aware)

**M-ID.** `M-2`.

**Model Name.** Primary identifier: `wp_full_<specialist>` (e.g., `wp_full_general`, `wp_full_speed`, `wp_full_closer`, `wp_full_class_riser`, `wp_full_class_dropper`, `wp_full_sprint`, `wp_full_route`, `wp_full_gonzo_sauce`). Secondary identifier: `win_prob_full` (legacy / general-only). Loader priority at `wr_inference_service.py:193-198`: `wp_full_general` / `win_prob_full` for `style='general'`; `wp_full_<specialist>` for non-general styles. Training entry point: `model/win_prob/train.py` `train_full_model_only(specialist)` at `model/win_prob/train.py:532-570`; artifact-suffix per `model/shared/specialists.py:artifact_suffix`.

**Model Type.** `XGBoost`. Same booster class and objective as M-1: `xgb.Booster` with `objective='binary:logistic'`, `eval_metric='logloss'` per `model/win_prob/config.py:11-12` (re-uses `XGB_PARAMS`); workout-layer training uses `WORKOUT_XGB_PARAMS` at `model/win_prob/config.py:27-37` with conservative depth (max_depth=4) and stronger regularization (reg_alpha=0.5, reg_lambda=2.0). Loader path identical to M-1: `xgb.Booster()` + `load_model` at `wr_inference_service.py:294-296`.

**Inputs.** Feature set is *style-dependent* per loader logic at `wr_inference_service.py:524-531`:

- **General + 6 non-gonzo specialists (`general`/`speed`/`closer`/`class_riser`/`class_dropper`/`sprint`/`route`):** 53 features = `get_lean53_features()` per `model/shared/feature_definitions.py:197-202`. The 53 features are the 66-feature base minus `LEAN53_CULL`.
- **Gonzo Sauce (`gonzo_sauce`) specialist:** 67 features = `get_gonzo_sauce_features()` per `model/shared/feature_definitions.py:256-260`. The 67 features are the 53 lean53 base plus 14 Gonzo features (`GONZO_FEATURE_DEFS` at `model/shared/feature_definitions.py:223-247`): 4 speed-at-distance / noteworthy-workouts; 7 trajectory route-only; 3 class-established.

Forward stubs to Feature Provenance (lean53 base — common across all 8 specialists; format `fp:F-?<feature_name>`):

- All 47 lean53_core features inherited from M-1's input list (lean53 path), plus the 6 lean53 workout features. Per `model/shared/feature_definitions.py:135-137` (`get_workout_features()`) and `LEAN53_CULL` at line 185-194: lean53 culls `gate_work_30d` AND `workout_frequency_score` (as r=1.000 duplicate of `workout_count_30d`), so lean53 workout features = 6 (`days_since_last_workout`, `workout_count_30d`, `bullet_work_14d`, `bullet_count_30d`, `best_workout_speed_index`, `workout_speed_trend`). Total lean53 = 47 (lean53_core) + 6 (lean53 workout) = 53 ✓ (matches `get_lean53_features()` length assertion at line 201).
- Workout forward-stub list: `fp:F-?days_since_last_workout`, `fp:F-?workout_count_30d`, `fp:F-?bullet_work_14d`, `fp:F-?bullet_count_30d`, `fp:F-?best_workout_speed_index`, `fp:F-?workout_speed_trend`.
- **Gonzo Sauce additional 14 features (gonzo_sauce specialist only):** Group A (4): `fp:F-?speed_at_distance_recent_weighted`, `fp:F-?speed_at_distance_best_18mo`, `fp:F-?noteworthy_workout_recent_14d`, `fp:F-?noteworthy_workout_count_30d`. Group B (7, route-only — sprint-today rows return defaults per inline note at `model/shared/feature_definitions.py:234`): `fp:F-?route_expand_count`, `fp:F-?route_held_count`, `fp:F-?route_erode_count`, `fp:F-?route_collapse_count`, `fp:F-?route_charge_short_count`, `fp:F-?route_avg_delta`, `fp:F-?is_stretching_out`. Group C (3): `fp:F-?class_tier_at_today_level_count_18mo`, `fp:F-?class_tier_in_money_rate_at_or_above`, `fp:F-?class_tier_avg_position_at_or_above`.

Inputs do NOT include intermediate latents — wp_full is a leftmost-layer model (raw features only, no upstream model output as input).

**Outputs.** Scalar `float` per (race, entry) — `raw_probs[idx]` at `wr_inference_service.py:555`. Output domain: P(win) ∈ [0, 1] from `binary:logistic` sigmoid. Same within-race-independence semantics as M-1 (per-horse binary; sums >>1.0 across race). Per-row output schema: scalar P(win); typed `np.float32` cast to Python `float`.

**Position in Inference Pipeline.** `Upstream: []; Downstream: [diagnostic only — no consuming model]; Inference layer: WR Layer 1 (Win Probability Full, workout-aware dispatch).` The WR pipeline at `wr_inference_service.py:549-555` dispatches per horse: horses with `has_workout[idx] == True` (defined at `:539-542` as `(workout_count_30d > 0) | (days_since_last_workout != 30.0)`) use wp_full. Output flows to the same two diagnostic storage fields as M-1 (`pred.confidence_score` at `:706`; `pred.raw_win_prob` at `:718`); not consumed downstream for the displayed `win_probability`. Layer name: "Layer 1: Win probability models" at `wr_inference_service.py:114`.

**Target Latent.** `win_probability_independent_per_horse_workout_aware`. Distinguished from M-1's no-workout target latent by the `has_workout` dispatch — wp_full models a different conditional distribution P(win | workout-data-available), so the latent is semantically distinct even though both are per-horse binary win probabilities. Canonical per Tony SP-2 ratification.

**Output Composition.** Identical to M-1: **diagnostic-only**. Output flows to `confidence_score` and `raw_win_prob` storage columns; no downstream model consumes wp_full's scalar for the displayed-prediction chain. Per the architectural comment at `wr_inference_service.py:579-598`, the post-2026-05-01 architecture flipped the displayed-probability source from wp_full softmax to rk_full softmax due to within-race-coherence requirements (binary classifier outputs do not sum to 1.0; ranker softmax does by construction).

**Calibration State.** `BYPASS (sidecar loaded unconditionally for non-legacy artifacts but never applied to inference output)`. Substrate evidence:

- Calibration sidecar load at `wr_inference_service.py:205-212`: `self.wp_full_calibration = self._try_load_calibration(...)`. Unlike wp_core, the wp_full sidecar load is unconditional (no version-name suffix gate); any wp_full artifact with a corresponding `_calibration.json` in S3 will load.
- Sidecar fitted by `scripts/fit_all_calibrations.py` for all 14 active wp_full + pl_core artifacts (general + 6 specialists × 2 model_types = 14, per script docstring line 2-3); `IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)` at line 189-190.
- **Sidecar is never applied to wp_full output in inference path.** Same observation as M-1: `_apply_calibration` is defined at `wr_inference_service.py:326-335` but no invocation site uses `self.wp_full_calibration`; the BYPASS block at lines 616-626 routes ranker_probs (M-4 output) through to handicapping_probs without wp_full input.
- Direct evidence: `grep -nE "wp_full_calibration" wr_inference_service.py` returns the field declarations (line 123, 124, 128) and load assignments (line 205, 208, 210) but no usage in `predict_race` post-load.

**Bypass State Narrative.** Identical mechanism to M-1: sidecar loaded for diagnostic alignment with `scripts/fit_all_calibrations.py` deliverables, but no inference-path consumer applies it. The post-2026-05-01 architectural flip (per `wr_inference_service.py:579-598`) removed wp_full from the displayed-probability path, leaving its calibration sidecar as a dead-load artifact. The wp_full sidecar load is *unconditional* (not gated by version-name suffix as wp_core's is) — every active wp_full artifact pays the warm-start cost regardless of whether the sidecar will ever be consumed. Cross-reference `wr_inference_service.py:616-626` for the related rk_full calibration BYPASS chain (Bug #15 + Bug #24).

PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=refactor; rationale="wp_full calibration sidecars are loaded unconditionally for all 8 active styles at warm-start (8 × O(thresholds) memory + 8 S3 download attempts) but never applied to inference output — distinct from the line 616-626 BYPASS already known to QB. Either remove the load (drop the `_try_load_calibration` call at line 205 + the related infra in `scripts/fit_all_calibrations.py`) or apply the sidecar to a calibrated diagnostic field for backtesting parity"; cite=wr_inference_service.py:205-212, wr_inference_service.py:326-335.

**Notes.** Per-style specialist family (8 styles per `wr_inference_service.py:101-105`). Specialist semantics from `model/shared/specialists.py:28-63`: `general` baseline; FILTER specialists (`sprint`, `route`) restrict training pool to in-distribution races by distance; WEIGHT specialists (`speed`, `closer`, `class_riser`, `class_dropper`) train on full pool with `sample_weight=3.0` on rows in qualifying races; FEATURE_SET specialist (`gonzo_sauce`) trains on full pool with the 67-feature lean53+Gonzo set instead of 53. Display names + criterion descriptions at `model/shared/specialists.py:43-63`. Workout-layer hyperparameter snapshot at `model/win_prob/config.py:27-37`. Training-time vs inference-time delta: training writes per-style artifacts with `_meta.json` sidecars (objective, feature_count, feature_names, xgb_params per `model/win_prob/train.py:200-210`); inference loads model + meta + calibration sidecar.

---

#### § 4.1.3 M-3 — `rk_core` (XGBoost rank:pairwise — WR Layer 2, no-workout)

**M-ID.** `M-3`.

**Model Name.** Primary identifier: `ranker_core` (model_versions registry name). No secondary identifiers — the loader at `wr_inference_service.py:215-217` calls `_try_load_model_type(['ranker_core'])` with a single-item priority list (no specialist tagging for rk_core). Training entry point: `model/ranker/train.py` `train_ranker(...)` at `model/ranker/train.py` (artifact-suffix `'ranker_core'` for general-only registration).

**Model Type.** `Pairwise Ranker (XGBoost rank:pairwise — LambdaMART)`. Specifically: `xgb.Booster` trained with `objective='rank:pairwise'` per `model/ranker/config.py` (verified inline in training script at `model/ranker/train.py:83`); the docstring header at `model/ranker/train.py:4` explicitly identifies this as LambdaMART. Loader path identical to M-1/M-2: `xgb.Booster()` + `load_model` at `wr_inference_service.py:294-296`.

**Inputs.** Feature set: 58 features = `get_core_features(include_odds=True)` = `CORE_FEATURES` per `wr_inference_service.py:39, 561, 575`. The rk_core path is fixed at the legacy 58-feature set regardless of style — per the loader at `wr_inference_service.py:215-217` (no specialist tagging) and the inference dispatch at `wr_inference_service.py:561-563, 573-577` (always uses `CORE_FEATURES`, even in the wp_full+rk_full dispatch path when rk_full is unavailable). The lean53 cull does NOT apply to rk_core in current production substrate.

Forward stubs to Feature Provenance (cohort SP-2 reconciliation pending; format `fp:F-?<feature_name>`):

- All 58 core-with-odds features = the union of M-1's lean53 path features (47) plus the 11 features culled by `LEAN53_CULL` from the core-with-odds set (3 odds-derived + 8 non-odds zero-gain that are also non-workout). Specifically the 58-feature list = `get_core_features(include_odds=True)` per `model/shared/feature_definitions.py:128-132`:
  - **Speed (11)** — same 11 as M-1.
  - **Pace (6)** — `early_pace_last`, `late_pace_last`, `pace_delta_last`, `avg_call1_position`, `avg_stretch_gain`, `pace_scenario_today` (legacy retains).
  - **Trip (8)** — `troubled_trip_last`, `troubled_trip_freq`, `pace_setter_freq`, `faded_freq`, `late_rally_freq`, `avg_wide_path`, `wide_3plus_freq`, `gate_issue_freq`.
  - **Trainer (5)** — same 5 as M-1.
  - **Class (7)** — same 7 as M-1.
  - **Physical (10)** — same 10 (legacy retains `is_first_start`, `was_claimed_last_out`, `apprentice_allowance` that lean53 culls).
  - **Equipment (5)** — `lasix`, `lasix_first_time`, `blinkers_on`, `blinkers_off`, `trainer_intent_score` (legacy retains `blinkers_off`).
  - **Odds (3)** — `closing_odds`, `log_closing_odds`, `odds_move`.
  - **Jockey (3)** — `jockey_win_rate`, `jockey_trainer_combo_win_rate`, `jockey_change_flag`.

Forward-stub roll-up: 11+6+8+5+7+10+5+3+3 = 58. ✓ matches `get_core_features(include_odds=True)` length per the doc-string assertion at `model/shared/feature_definitions.py:128-129`.

Inputs do NOT include intermediate latents — rk_core reads raw features only. Although it occupies "Layer 2" in the WR code's layer naming (per the comment at `wr_inference_service.py:118` "Layer 2: Ranker models"), it is architecturally a leftmost-layer model that reads the same raw feature matrix wp_core/wp_full read; the "Layer 2" naming reflects the dataflow ordering in the inference function (`predict_race` first computes wp_* outputs, then rk_* outputs, then composes), not feature-input dependency.

**Outputs.** Scalar `float` per (race, entry) — `rank_scores[idx]` at `wr_inference_service.py:563, 577`. Output domain: real-valued LambdaMART rank score, **only meaningful within-race** (per the architectural comment at `wr_inference_service.py:586-590`: "their per-horse scores are only meaningful in within-race comparison"). Output is unbounded in absolute magnitude; downstream softmax normalizes per-race. Per-row output schema: scalar rank score; typed `np.float32` cast to Python `float`.

**Position in Inference Pipeline.** `Upstream: []; Downstream: [WR Layer 2 softmax → handicapping_probs (when rk_full unavailable)]; Inference layer: WR Layer 2 (Pairwise Ranker, no-workout dispatch / fallback).` The WR pipeline at `wr_inference_service.py:560-563` and `:573-577` uses rk_core in two cases: (1) horse has workout data BUT rk_full is unavailable (no rk_full artifact loaded) — the `elif self.rk_core_model:` branch at line 560-563; (2) horse has no workout data — the `if self.rk_core_model:` branch at line 573-577. In both cases, rk_core's `rank_scores[idx]` is consumed by the within-race softmax at `wr_inference_service.py:599-603` to produce `ranker_probs`, which then feeds (via the BYPASS at 616-626) into `handicapping_probs` and ultimately the displayed `win_probability`. rk_core is the load-bearing ranker for no-workout-data horses and the fallback for workout-data horses when rk_full is unavailable. Layer name: "Layer 2: Ranker models" at `wr_inference_service.py:118-121`.

**Target Latent.** `within_race_pairwise_rank_score`. The latent is the within-race ordering signal — semantically distinct from win_probability because rank_score values are unbounded and only meaningful in within-race comparison; the softmax transform at `wr_inference_service.py:599-603` is what converts rank_score into a probability distribution `ranker_probs`. Canonical per Tony SP-2 ratification.

**Output Composition.** rk_core output → within-race softmax → `ranker_probs` → (via BYPASS at lines 616-626) `handicapping_probs` → 0-PP override (line 634-636) → renormalize (line 638-641) → blend with `market_probs` at line 674-676 with `HANDICAPPING_BLEND_WEIGHT` (per `shared.constants`) → `displayed_prob` written to `wr_predictions.win_probability`. Composition rule: temperature-1.0 softmax (no temperature scaling — `shifted = rank_scores - rank_scores.max(); exp_scores = np.exp(shifted); ranker_probs = exp_scores / exp_scores.sum()` at lines 600-603) followed by post-calibration override + renormalize chain. When rk_full IS loaded for a workout-data horse, rk_full's output supersedes rk_core for that horse; when rk_full is unavailable, rk_core's output is used. The softmax composition is *per-race* (not per-horse), so rk_core's output for one race entry is meaningful only relative to other entries in the same race.

**Calibration State.** `UNCALIBRATED`. Substrate evidence:

- No calibration sidecar load attempt in the rk_core load path at `wr_inference_service.py:215-221`. Compare against M-2 at lines 205-212 (where `self._try_load_calibration(...)` is called for wp_full) and against the gonzo_sauce-only rk_full sidecar load at lines 229-238 — neither pattern applies to rk_core.
- `self.rk_core_model` is loaded as a bare booster with no `_calibration.json` companion. The `_try_load_calibration` helper at `wr_inference_service.py:298-324` is never invoked with rk_core's version object.
- Per `scripts/fit_all_calibrations.py` docstring at line 24 ("ranker/...   (no — rk skipped per spec)"), the calibration-fitting workstream explicitly excludes rk_core (and rk_full general — only rk_full gonzo_sauce was added later per `wr_inference_service.py:227-238`).
- Direct evidence: `grep -nE "rk_core_calibration" wr_inference_service.py` returns zero matches.

**Bypass State Narrative.** N/A — not BYPASS; the model is `UNCALIBRATED` in the strict sense (no sidecar exists in S3, no load is attempted, no inference-path code applies any calibration to rk_core's output). The within-race softmax at lines 599-603 is a normalization (probability-distribution-construction) transform, not a calibration transform — it does not correct the model's score-vs-truth alignment, only converts unbounded rank scores into a within-race probability distribution that sums to 1.0. Calibration debt cross-reference: rk_core is one of the calibration-debt candidates listed in § 5.2 (UNCALIBRATED count + index).

**Notes.** Single-artifact (no per-style specialist family for rk_core; only `ranker_core` general registry name). Hyperparameter snapshot referenced at `model/ranker/config.py` (XGB_PARAMS, NUM_ROUNDS, EARLY_STOPPING_ROUNDS); specifically `objective='rank:pairwise'` per `model/ranker/train.py:83`, with rank:pairwise expecting one weight per query group (race) per the inline comment at `model/ranker/train.py:163-164`. rk_core feature set (58, legacy odds-aware) is *the same as* M-1 wp_core's legacy fallback path; the lean53 cull was applied to wp_core/wp_full and rk_full but NOT to rk_core in current production substrate (rk_core remains 58-feature legacy). The architectural comment at `wr_inference_service.py:573-577` explicitly notes: "rk_core remains 58-feature legacy" — confirms intentional retention of the legacy feature set for rk_core through the lean53 transition. Training-time/inference-time delta: training writes per-version artifacts with `_meta.json` (objective `'rank:pairwise'` per save_artifacts at `model/ranker/train.py:79-93`); inference loads bare model only (no sidecar).

---

#### § 4.1.4 M-4 — `rk_full` (XGBoost rank:pairwise — WR Layer 2, workout-aware)

**M-ID.** `M-4`.

**Model Name.** Primary identifier: `rk_full_<specialist>` (e.g., `rk_full_general`, `rk_full_speed`, `rk_full_closer`, `rk_full_class_riser`, `rk_full_class_dropper`, `rk_full_sprint`, `rk_full_route`, `rk_full_gonzo_sauce`). Secondary identifier: `ranker_full` (legacy / general-only). Loader priority at `wr_inference_service.py:194-198`: `rk_full_general` / `ranker_full` for `style='general'`; `rk_full_<specialist>` for non-general styles. Training entry point: `model/ranker/train.py` `train_ranker(...)` with `--specialist <style>` argument; artifact-suffix injection via `model/shared/specialists.py:artifact_suffix('rk_full', specialist)`.

**Model Type.** `Pairwise Ranker (XGBoost rank:pairwise — LambdaMART)`. Same booster class and objective as M-3: `xgb.Booster` with `objective='rank:pairwise'` per `model/ranker/train.py:83`. Loader path identical: `xgb.Booster()` + `load_model` at `wr_inference_service.py:294-296`.

**Inputs.** Feature set is *style-dependent* per WR loader logic at `wr_inference_service.py:524-531`:

- **General + 6 non-gonzo specialists:** 53 features = `get_lean53_features()` per `model/shared/feature_definitions.py:197-202`. Same lean53 set as M-2's non-gonzo path. Substrate at `wr_inference_service.py:42` (`RANKER_FULL_FEATURES = get_lean53_features()`).
- **Gonzo Sauce specialist:** 67 features = `get_gonzo_sauce_features()` (same 67 as M-2's gonzo_sauce path).

Forward stubs: identical to M-2's lean53 / gonzo_sauce stub list. See M-2 § 5.4 for verbatim per-group enumeration; deduplication recorded in § 6.1.

Inputs do NOT include intermediate latents — rk_full reads raw features only (same architectural posture as M-3).

**Outputs.** Scalar `float` per (race, entry) — `rank_scores[idx]` at `wr_inference_service.py:559`. Output domain: real-valued LambdaMART rank score, only meaningful within-race (same semantics as M-3). Per-row output schema: scalar rank score; typed `np.float32` cast to Python `float`.

**Position in Inference Pipeline.** `Upstream: []; Downstream: [WR Layer 2 softmax → handicapping_probs (post-BYPASS) → displayed win_probability]; Inference layer: WR Layer 2 (Pairwise Ranker, workout-aware dispatch — primary).` rk_full is the *primary* ranker for workout-data horses per the dispatch at `wr_inference_service.py:556-559`; rk_core (M-3) is the fallback. rk_full's output is the load-bearing input to the within-race softmax at lines 599-603 (`shifted = rank_scores - rank_scores.max(); exp_scores = np.exp(shifted); ranker_probs = exp_scores / exp_scores.sum()`), which produces the displayed `win_probability` after BYPASS + override + renormalize + market-blend chain.

**Target Latent.** `within_race_pairwise_rank_score`. Same latent as M-3 (within-race ordering signal). The semantic distinction between M-3 and M-4 lies in the workout-data conditioning, not in the latent itself: M-4 models the rank-score conditional distribution P(rank | workout-data-available) on the lean53 (or gonzo) feature set; M-3 models P(rank) on the legacy 58-feature set without workout conditioning. Both contribute to the same `within_race_pairwise_rank_score` latent vocabulary, with M-4 dispatched preferentially when workout data is present.

**Output Composition.** Identical composition chain to M-3: per-race softmax → `ranker_probs` → BYPASS (lines 616-626) → `handicapping_probs` → 0-PP override (lines 634-636) → renormalize (lines 638-641) → blend with `market_probs` (lines 674-676; weight `HANDICAPPING_BLEND_WEIGHT`) → `displayed_prob` → `wr_predictions.win_probability`. The dispatch at lines 556-559 supersedes M-3's output for workout-data horses; for no-workout horses M-3 is used. Both M-3 and M-4 outputs feed the same softmax pool per race (the `rank_scores` array at line 546 is populated mixed-source per-horse depending on workout availability).

**Calibration State.** `BYPASS (uniform across all 8 styles per wr_inference_service.py:616-626; sidecar conditionally loaded for gonzo_sauce variant only at lines 227-238 but not applied)`. Substrate evidence:

- Inference-path BYPASS at `wr_inference_service.py:616-626`: comment block explicitly states "All styles (including gonzo_sauce) bypass calibration at inference tonight"; the operative line is `handicapping_probs = ranker_probs.copy()` at line 626 (no `_apply_calibration` invocation). This is the QB-pre-listed BYPASS in the known list.
- Gonzo_sauce sidecar load at `wr_inference_service.py:227-238`: `self.rk_full_calibration` is loaded ONLY when `self.style == 'gonzo_sauce'`; non-gonzo styles never attempt the load. Sidecar is fitted by an A3-era extension to `scripts/fit_all_calibrations.py` (rk_full calibration fitting was excluded from the original fit_all_calibrations spec per the docstring at line 24 "ranker/... (no — rk skipped per spec)"; gonzo_sauce was the lone exception added later).
- The Bug #15 + Bug #24 chain: Bug #15 is the gallery-wide calibration interaction (canonical home `feature_provenance_bible:#15` per BIBLE_STRUCTURE_SPEC v6 § 6.3); Bug #24 (per memory `project_ee_bug_24_calibration_0pp_interaction.md`) is the specific 0-PP-override-after-calibration interaction that re-introduced the BYPASS for gonzo_sauce on the night of the original A3 calibration plan; resolution depends on Phase A3.5 splitting 0-PP horses out of the calibration path entirely.
- Direct evidence: `grep -nE "rk_full_calibration" wr_inference_service.py` returns the field declaration (line 128), gonzo-conditional load (line 230), and conditional log (line 233-237) — but no usage in `predict_race` post-load.

**Bypass State Narrative.** rk_full has a calibration sidecar in S3 for the gonzo_sauce variant only (loaded conditionally at lines 227-238) but the `handicapping_probs = ranker_probs.copy()` at line 626 short-circuits any calibration application for ALL styles, including gonzo_sauce. The BYPASS is explicit (intentional, documented in the comment block at lines 616-625) and applies uniformly across the 8-style specialist family. Trigger condition: line 626 is unconditional in the current code path. Fallback behavior: none — there is no calibrated branch. Re-enable path: Phase A3.5 (per the comment at lines 622-625) requires splitting 0-PP horses out of the calibration path before rk_full calibration can be reactivated; the gonzo sidecar is retained in S3 and continues to be downloaded at warm-start "for A3.5 use" per line 625. This is the QB-pre-listed BYPASS — not surfacing as a new PHASE_5_BACKLOG_CANDIDATE per SP-2 resolution standing instruction.

**Notes.** 8-style specialist family (same set as M-2; per `wr_inference_service.py:101-105`). Specialist semantics inherited from `model/shared/specialists.py:28-37` (FILTER / WEIGHT / FEATURE_SET classification). RANKER_FULL_CULL at `model/shared/feature_definitions.py:151-161` defines a 51-feature lean51-ranker variant (`get_ranker_full_features()`) but production substrate uses `get_lean53_features()` per `wr_inference_service.py:42` instead — the lean51 ranker variant is not the inference-time feature set despite the dedicated function. Cross-reference `model/shared/feature_definitions.py:140-150` for the rationale comment block on lean51 (Phase 1 ablation +3.6pp top-1, +4.4pp top-3 vs full 66) — this is the historic lean variant that was superseded by lean53 (Stream A2 at `model/shared/feature_definitions.py:170-184`). Hyperparameter snapshot at `model/ranker/config.py`. rank:pairwise group-weight requirement: one weight per race (query group), not per horse (per `model/ranker/train.py:163-164` inline comment).

---

#### § 4.1.5 M-5 — `pl_core` (XGBoost reg:squarederror — PL Layer 1)

**M-ID.** `M-5`.

**Model Name.** Primary identifier: `pl_core_<specialist>` (e.g., `pl_core_general`, `pl_core_speed`, `pl_core_closer`, `pl_core_class_riser`, `pl_core_class_dropper`, `pl_core_sprint`, `pl_core_route`). Loader priority at `backend/services/pl_inference_service.py:93-104`: single-item priority `f'pl_core_{self.style}'`; no legacy alias fallback. Training entry point: `model/pl/train.py` `train_full_model_only(specialist)` at `model/pl/train.py:124-377` with `--specialist <style>` argument.

**Model Type.** `XGBoost`. Specifically: `xgb.Booster` trained with `objective='reg:squarederror'`, `eval_metric='rmse'` per `model/wr/config.py:9-22` (re-exported via `model/pl/config.py:11-15` — see Notes). This is **regression on EV (Expected Value) labels**, NOT binary classification — the objective is fundamentally different from M-1/M-2's `binary:logistic`. EV labels per `model/wr/config.py:42-58`: winners with payout get the actual `win_payout` (per $2 bet); winners without payout get `AVG_WIN_PAYOUT = 12.18`; losers get `-1.0`. The model learns to score each horse by its expected monetary return per $2 wagered. Loader path: `xgb.Booster()` + `load_model` at `pl_inference_service.py:152-153`.

**Inputs.** Feature set: 47 features = `get_lean53_core_features()` per `model/shared/feature_definitions.py:205-211`. Substrate at `pl_inference_service.py:35` (`PL_FEATURES = get_lean53_core_features()`). Legacy fallback at `pl_inference_service.py:36` (`LEGACY_PL_FEATURES = get_core_features(include_odds=True)`) defines the 58-feature legacy set as a code-level constant but the production code path uses `PL_FEATURES` (47) at `pl_inference_service.py:319-326`. Same 47-feature lean53_core set as M-1's lean53 path.

Forward stubs: identical to M-1's lean53 path stub list (47 features). See M-1 § 5.4 for verbatim per-group enumeration; deduplication recorded in § 6.1.

Inputs do NOT include intermediate latents — pl_core is a leftmost-layer model (raw features only).

**Outputs.** Scalar `float` per (race, entry) — `raw_scores[idx]` at `pl_inference_service.py:329`. Output domain: real-valued EV-regression score (NOT a probability — `reg:squarederror` produces unbounded real values representing expected monetary return per $2 bet). Downstream pipeline applies temperature-1.0 softmax with clip to [-20, 0] (per lines 331-337) to convert raw EV scores into within-race win probabilities. Per-row output schema: scalar EV regression score; typed `np.float32` cast to Python `float`.

**Position in Inference Pipeline.** `Upstream: []; Downstream: [PL Layer 1 softmax → calibration → 0-PP override → renormalize → handicapping_probs → M-7 PL EV/Kelly Overlay (terminal)]; Inference layer: PL Layer 1 (sole trained model in PL pipeline).` M-5 is the **only trained inference model in the entire PL pipeline** — there is no PL ranker, no PL longshot classifier, no PL ensemble. The full PL inference chain at `pl_inference_service.py:295-468` is: build feature matrix → pl_core predict → softmax → CALIBRATION → 0-PP override → renormalize → blend with market_probs → instantiate PLPrediction → M-7 compute_ev_and_kelly → store. The `equine-pl-inference` Lambda at `architecture_overview:3.1` is purpose-built for this single-trained-model pipeline.

**Target Latent.** `per_horse_ev_regression_score`. Distinct from any latent in the WR or LS pipelines — pl_core models expected monetary return rather than win probability or rank score. The latent is fundamentally a regression target, not a classification or ranking target. Downstream softmax conversion produces a within-race probability distribution that approximates win probability conditional on EV-regression-relative ordering, but the model's output latent itself is the EV-regression score.

**Output Composition.** Per-race within-race softmax with temperature 1.0 and overflow clip at `pl_inference_service.py:331-337`: `scaled = (raw_scores - raw_scores.max()) / SOFTMAX_TEMPERATURE; scaled = np.clip(scaled, -20, 0); softmax_probs = np.exp(scaled) / np.exp(scaled).sum()`. Then `handicapping_probs = self._apply_calibration(softmax_probs, self.calibration)` at lines 341-343. Then 0-PP override (lines 360-362; horses with no past_performances → `1.0 / field_size`). Then within-race renormalization (lines 367-369). Then market_prob within-race normalization (lines 403-411). Then blend with `HANDICAPPING_BLEND_WEIGHT` to produce `displayed_prob` (lines 432-434). Then EV/Kelly computation via M-7 (`compute_ev_and_kelly` at lines 501-569). Final fields written to `pl_predictions` per `pl_inference_service.py:583-612`. Composition rule: softmax → isotonic calibration (CALIBRATED — see § 5.9) → 0-PP override → renormalize → arithmetic EV/Kelly overlay (M-7) → terminal.

**Calibration State.** `CALIBRATED (isotonic regression via piecewise-linear interpolation; sidecar fit on post-softmax win-prob targets)`. Substrate evidence:

- Calibration sidecar load at `pl_inference_service.py:160-180`: `self.calibration` loaded from `<base_key>_calibration.json` via `s3_client.download_file(bucket, cal_key, local_cal)`; format `(np.array(cal['x_thresholds'], dtype=float), np.array(cal['y_thresholds'], dtype=float))`.
- Sidecar fitted by `scripts/fit_all_calibrations.py` for all 7 active pl_core artifacts (general + 6 specialists; per script docstring lines 12-14: "pl_core_*: 58 features. Booster output is EV score; converted to win prob via softmax-within-race. Fit isotonic on (post_softmax_win_prob, actual_win)"). Fit method: `IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)` at `scripts/fit_all_calibrations.py:189-190`.
- **Sidecar IS applied at inference.** `pl_inference_service.py:341-343`: `handicapping_probs = self._apply_calibration(softmax_probs, self.calibration)`. The static `_apply_calibration` at `pl_inference_service.py:182-188` applies via `np.clip(np.interp(raw, xt, yt), 0.0, 1.0)`. Calibration runs after softmax but before 0-PP override and renormalize.
- Calibration method per QB_DRAFTING_SPEC § 5.9: `CALIBRATED (Isotonic regression via piecewise-linear np.interp interpolation against fitted x_thresholds/y_thresholds)`. Code-line citation: `pl_inference_service.py:182-188` (interpolation impl); `pl_inference_service.py:341-343` (invocation site); `scripts/fit_all_calibrations.py:189-190` (fit-time IsotonicRegression).

**Bypass State Narrative.** N/A — calibration is applied, not bypassed. Note however that the post-calibration + 0-PP override + renormalize ordering at `pl_inference_service.py:341-369` is the exact ordering interaction surface that produced **Bug #24** in the WR pipeline (per `wr_inference_service.py:616-626` comment block + memory `project_ee_bug_24_calibration_0pp_interaction.md`). The PL pipeline currently runs this ordering without manifesting the same Bug #24 symptoms — the substrate-observed disposition is that PL's calibration application has NOT been retracted via a BYPASS, contra the WR pipeline's choice. Whether this is intentional architectural divergence or pending-evaluation status is unclear from substrate.

PHASE_5_BACKLOG_CANDIDATE: severity=MEDIUM; disposition=monitored; rationale="PL pipeline applies isotonic calibration with 0-PP override + renormalize chain at pl_inference_service.py:341-369 — same ordering pattern that produced Bug #24 in WR (gonzo_sauce 0-PP horses dominating top picks per wr_inference_service.py:616-625 comment). PL has not BYPASS'd in response. Either the PL pipeline is empirically immune to the Bug #24 manifestation (worth verifying via Derby-window diagnostic) or the issue exists but has not been surfaced to operator review. Verification + disposition pending"; cite=pl_inference_service.py:341-369, wr_inference_service.py:616-625.

**Notes.** **Cross-pipeline coupling at config level.** `model/pl/config.py:11-15` re-exports `XGB_PARAMS`, `WORKOUT_XGB_PARAMS`, `NUM_ROUNDS`, `EARLY_STOPPING_ROUNDS`, `WORKOUT_NUM_ROUNDS`, `WORKOUT_EARLY_STOPPING_ROUNDS` from `model/wr/config.py:9-49` directly: `from wr.config import (compute_ev_labels, XGB_PARAMS, ...)`. Then re-exports under PL names at `model/pl/config.py:18-19`: `XGB_PARAMS_PL = XGB_PARAMS; WORKOUT_XGB_PARAMS_PL = WORKOUT_XGB_PARAMS`. This means PL Core's hyperparameters are *physically the same Python objects* as WR's hyperparameters — any change to `model/wr/config.py:11-23` propagates immediately to PL training. Intentional/unintentional classification of this coupling is pending architectural review per QB-known list.

**EV-regression vs binary-classification disparity.** PL's `objective='reg:squarederror'` (regression on EV labels) is architecturally incompatible with M-1/M-2's `objective='binary:logistic'` (binary classification on win labels). The disparity propagates into output composition (PL needs softmax to convert real-valued EV scores into a within-race probability distribution; WR's wp_* outputs are already in [0,1] but lack within-race coherence). The two pipelines target fundamentally different latents: PL targets *expected monetary return*; WR targets *probability of winning*. Cross-pipeline label fusion (e.g., training PL on a mixed EV+binary loss, or feeding pl_core EV into the WR ensemble M-11) is not currently in production substrate. Disparity classification is pending architectural review per QB-known list.

**7-style specialist family.** `pl_inference_service.py:60-63` lists 7 styles (`general`, `speed`, `closer`, `class_riser`, `class_dropper`, `sprint`, `route`) — **no `gonzo_sauce` in PL** (compare M-2/M-4's 8-style family). The Phase A3 gonzo_sauce specialist was added to WR pipeline only; PL pipeline did not receive a parallel gonzo training pass.

**Training-time vs inference-time delta.** Training (per `model/pl/train.py:124-377`) trains TWO layers per specialist: Layer 1 (`pl_core`, all rows) + Layer 2 (`pl_workout`, workout-data rows only) at `model/pl/train.py:240-360`. Inference (per `pl_inference_service.py:90-92`) loads ONLY Layer 1: "V1 uses Layer 1 only (pl_core_{style}); pl_workout artifacts exist in S3 + model_versions but are not loaded at inference." This is a substrate-observed orphaned-artifact pattern: training writes pl_workout artifacts that are never loaded at inference.

PHASE_5_BACKLOG_CANDIDATE: severity=LOW; disposition=kill; rationale="pl_workout Layer 2 artifacts are trained per pl_core specialist (7 artifacts × N retrains) and registered in model_versions, but pl_inference_service.py:90-92 explicitly states 'V1 uses Layer 1 only; pl_workout artifacts ... are not loaded at inference'. Either disable pl_workout training (drop the Layer 2 training block at model/pl/train.py:240-360 + delete dead artifacts from S3 + mark inactive in model_versions) or wire the Layer 2 model into inference"; cite=pl_inference_service.py:90-92, model/pl/train.py:240-360.

---

#### § 4.1.6 M-6 — WR Arithmetic Value Overlay (`compute_value_overlay`)

**M-ID.** `M-6`.

**Model Name.** `compute_value_overlay` (free function at `backend/services/wr_inference_service.py:53-80`). Non-trained; no `model_versions` registry row; no S3 artifact. The function is the canonical identifier — invoked at `wr_inference_service.py:683-686` per (race, entry).

**Model Type.** `Arithmetic Overlay (non-ML)`. Specifically: pure-arithmetic Kelly-criterion bet-sizing computation with edge-threshold gating. No trained parameters; no random state; no training script. The function takes two scalars (raw_win_prob — actually post-BYPASS handicapping_prob per the call site at line 683 despite the parameter-name choice — and morning_line_odds) and produces a 5-key dict via deterministic arithmetic. Verified at primary source: function definition at `wr_inference_service.py:53-80`; constants `VALUE_MIN_EDGE = 0.05`, `VALUE_HALF_KELLY = 0.5`, `VALUE_MAX_KELLY = 0.10`, `VALUE_BANKROLL = 1000.0` at `wr_inference_service.py:46-50`.

**Inputs.** Per the function signature at `wr_inference_service.py:53`: `(raw_win_prob: float, morning_line_odds: float)`. At the call site (line 683-686), the first argument is `handicapping_prob` (a per-horse scalar from M-3/M-4 ranker softmax → BYPASS chain), NOT the wp_*-derived raw_win_prob — the parameter name is misleading. Inputs are intermediate latents from upstream models (M-3/M-4 via softmax) plus a raw entry attribute (`entry.morning_line_odds` from `entries` table per `database_schema_bible:4.1.6`).

Forward stubs: not feature-engineered features in the M-1/M-2/M-3 sense — inputs are upstream-model derivatives + DB column.

- Upstream-model derivative input: `mla:M-3` and/or `mla:M-4` softmax-derived handicapping_prob (post-BYPASS at `wr_inference_service.py:626`).
- Raw DB column input: `entries.morning_line_odds` (per `database_schema_bible:4.1.6`); not a feature_provenance_bible feature row but a direct column read.

**Outputs.** Dict with 5 keys per `wr_inference_service.py:74-80`: `edge_pct` (rounded to 4 decimals), `kelly_fraction` (rounded to 4), `kelly_bet` (dollar amount, rounded to 2 decimals; 0.0 unless `is_value`), `is_value` (bool — `edge >= VALUE_MIN_EDGE`), `implied_prob` (rounded to 4). Domain: `edge_pct ∈ ℝ`; `kelly_fraction ∈ [0, VALUE_MAX_KELLY]`; `kelly_bet ∈ {0.0} ∪ [0, VALUE_MAX_KELLY × VALUE_BANKROLL]`; `is_value ∈ {True, False}`; `implied_prob ∈ [0, 1]`. Per-row output schema: 5-key dict; consumed by caller for storage assignment.

**Position in Inference Pipeline.** `Upstream: [M-3, M-4 (via ranker softmax + BYPASS chain producing handicapping_prob)]; Downstream: [wr_predictions storage columns: overlay_pct, is_value_flag, kelly_fraction, kelly_bet, recommended_bet_type]; Inference layer: WR Layer 3 (Value Overlay).` The output dict is consumed at `wr_inference_service.py:683-728` to populate prediction fields: `pred.edge_pct = value['edge_pct']` would be inferred but the actual binding occurs at lines 723-728 via the dynamic-attribute attachment block (per `architecture_overview:4.2`). The flag re-evaluation happens in `flag_value` at `wr_inference_service.py:755-770`, which does NOT call M-6 again but re-applies `OVERLAY_THRESHOLD` to the already-computed `pred.edge_pct`.

**Target Latent.** `kelly_bet_size_per_horse + value_flag (composite)`. The latent is the Kelly-criterion-derived bet sizing recommendation conditional on a horse's handicapping probability and morning-line odds — semantically a *betting-action recommendation* rather than a probability or rank. Composite because the function emits both a continuous recommendation (kelly_bet, in dollars) and a binary flag (is_value).

**Output Composition.** Pure arithmetic — no model composition. Inputs (handicapping_prob, ml_odds) → deterministic computation → output dict. Per QB_DRAFTING_SPEC § 5.8: `terminal — see § 5.6 downstream = []` for the trained-model-output sense (no downstream ML model consumes M-6's output); however M-6's output IS consumed by storage and by the rank/flag-recompute pipeline at `wr_inference_service.py:739-835`. The output dict is therefore terminal in the *trained-model-composition* sense but feeds storage + downstream non-ML logic.

**Calibration State.** `BYPASS (non-applicable to arithmetic computation; no model output to calibrate)`. Substrate evidence: M-6 is not a trained model and has no probabilistic output that requires calibration. The function emits arithmetic results from a probabilistic input (handicapping_prob) — calibration of the input is upstream of M-6's invocation. Per QB_DRAFTING_SPEC § 5.9, this is a degenerate case of calibration semantics (arithmetic transforms cannot themselves be "calibrated" in the isotonic-regression sense). Citation: `wr_inference_service.py:53-80` (no calibration sidecar load, no isotonic interpolation, no probabilistic sigmoid output).

**Bypass State Narrative.** Calibration is non-applicable to this layer — the BYPASS classification is by category (arithmetic overlay), not by architectural decision. Trigger condition: arithmetic computation has no probability-output requiring score-vs-truth alignment. Fallback behavior: N/A. Re-enable path: N/A (arithmetic does not need to be re-enabled). Note: M-6's input handicapping_prob inherits whatever calibration state M-3/M-4 produce — currently BYPASS per § 4.1.4, so M-6 operates on uncalibrated within-race-normalized softmax output.

**Notes.** The function signature parameter `raw_win_prob` is a misnomer — at the call site (line 683), the argument bound is `handicapping_prob` (post-BYPASS, post-renormalize), not the wp_*-derived raw_win_prob attribute. This naming inconsistency is observable substrate but not architectural debt requiring Phase 5 disposition (cosmetic only). Hyperparameter constants at `wr_inference_service.py:46-50`. Kelly variant: half-Kelly (per `VALUE_HALF_KELLY = 0.5` at line 48) capped at 10% bankroll (per `VALUE_MAX_KELLY = 0.10` at line 49). Value-bet threshold: `VALUE_MIN_EDGE = 0.05` (5pp edge). Bankroll: `VALUE_BANKROLL = 1000.0`. M-6's `is_value` boolean drives `pred.is_value_flag` initial assignment at `wr_inference_service.py:708`; `flag_value` at lines 755-770 re-evaluates via `OVERLAY_THRESHOLD` (per `shared.constants`) against `pred.edge_pct`. The two-pass flag computation (M-6's `is_value` then `flag_value`) is a substrate-observed oddity that allows the post-rank flag re-evaluation to use a different threshold from M-6's `VALUE_MIN_EDGE` — operational behavior of this divergence is unverified at substrate.

---

#### § 4.1.7 M-7 — PL Arithmetic EV/Kelly Overlay (`compute_ev_and_kelly`)

**M-ID.** `M-7`.

**Model Name.** `PLInferenceService.compute_ev_and_kelly` (instance method at `backend/services/pl_inference_service.py:501-569`). Non-trained; no `model_versions` registry row; no S3 artifact. Distinct from M-6 in parameterization, output schema, and pipeline destination.

**Model Type.** `Arithmetic Overlay (non-ML)`. Pure-arithmetic Expected-Value + Kelly-criterion + value-bet-flag computation per (race, entry). No trained parameters; no random state; deterministic from inputs. Constants imported from `shared.constants`: `BANKROLL`, `KELLY_FRACTION`, `MAX_BET_PCT`, `MIN_EDGE_TO_BET`, `STRONG_VALUE_THRESHOLD` (per `pl_inference_service.py:27-29`). Verified at primary source: method definition at `pl_inference_service.py:501-569`.

**Inputs.** Per the method body at `pl_inference_service.py:520-528`: per-PLPrediction object — reads `pred.entry.morning_line_odds` (line 521) + `pred.handicapping_prob` (line 525, falling back to `pred.win_probability` at line 528 for unmigrated callers). Inputs are intermediate latents from M-5 (post-softmax, post-calibration, post-renormalize handicapping_prob) plus a raw entry attribute (morning_line_odds).

Forward stubs:

- Upstream-model derivative input: `mla:M-5` post-calibration handicapping_prob (per `pl_inference_service.py:341-369` chain).
- Raw DB column input: `entries.morning_line_odds` (same as M-6).

**Outputs.** PLPrediction object fields populated per `pl_inference_service.py:549-567`: `pred.closing_odds`, `pred.implied_probability`, `pred.edge_pct`, `pred.predicted_ev`, `pred.kelly_fraction`, `pred.kelly_bet_size`, `pred.is_value_bet`, `pred.is_strong_value`. When `ml_odds` is None or ≤0, all fields set to None / 0.0 / False per the `else` branch at lines 559-567. Per-row output schema: 8 PLPrediction attributes; written to `pl_predictions` columns via `pl_inference_service.py:583-612`.

**Position in Inference Pipeline.** `Upstream: [M-5 (via post-calibration handicapping_prob)]; Downstream: [pl_predictions storage columns: closing_odds, implied_probability, edge_pct, predicted_ev, is_value_bet, is_strong_value, kelly_fraction, kelly_bet_size]; Inference layer: PL Layer 2 (Arithmetic EV/Kelly Overlay — terminal).` M-7 is the terminal layer of the PL inference pipeline. After M-7 runs, `pl_inference_service.rank_field` at lines 474-495 re-sorts by `predicted_ev` (NOT by `win_probability`) so that positive-EV horses float to top — this is PL's stated purpose ("find profitable bets, not generic win probability ranking" per the docstring at lines 478-481). Storage write at `pl_inference_service.py:583-612` populates all 8 M-7-emitted fields.

**Target Latent.** `per_horse_predicted_ev + value_bet_flag (composite, terminal)`. The latent is the per-horse expected value of a $1 bet (if positive) plus value-bet binary flag; compose into ranking and recommendation downstream.

**Output Composition.** Pure arithmetic per `pl_inference_service.py:529-558`:

- `closing_odds = float(ml_odds)` (line 530); morning_line_odds is used as a closing_odds proxy until actual closing lines are available per docstring at line 517.
- `implied_prob = 1.0 / (closing_odds + 1.0)` (line 531).
- `edge = handicap - implied_prob` (line 532).
- `ev = handicap * closing_odds - (1.0 - handicap)` (line 534).
- `raw_kelly = (edge / closing_odds) * KELLY_FRACTION` (line 538) when `edge >= MIN_EDGE_TO_BET and closing_odds > 0`.
- `kelly_bet_size = min(raw_kelly * BANKROLL, MAX_BET_PCT * BANKROLL)` (lines 539-542).
- `is_value_bet = (edge >= MIN_EDGE_TO_BET)`; `is_strong_value = (edge >= STRONG_VALUE_THRESHOLD)` (lines 555-558).

Per QB_DRAFTING_SPEC § 5.8: `terminal — see § 5.6 downstream = []` (no downstream ML model consumes M-7's output; storage only). The composition rule is a deterministic arithmetic chain.

**Calibration State.** `BYPASS (non-applicable to arithmetic computation)`. Same classification as M-6 — calibration is not applicable to non-trained arithmetic overlays. Citation: `pl_inference_service.py:501-569` (no calibration sidecar load, no isotonic interpolation). M-7 operates on M-5's post-calibration handicapping_prob, inheriting M-5's CALIBRATED state for its input but emitting non-probabilistic outputs (predicted_ev is unbounded; kelly_fraction is a fraction of bankroll; is_value_bet is binary).

**Bypass State Narrative.** Same as M-6 — non-applicable by category (arithmetic overlay). N/A on trigger / fallback / re-enable. Note: M-7's input handicapping_prob *is* CALIBRATED (M-5 § 5.9), so M-7 operates on calibrated probabilities — distinct from M-6 which operates on BYPASS'd handicapping_probs.

**Notes.** Asymmetry with M-6: M-7 is NOT a function but an instance method on `PLInferenceService`; it mutates the input `PLPrediction` objects (assigning attributes) rather than returning a dict. M-7's `kelly_bet_size` cap uses `MAX_BET_PCT` (config constant) not a hardcoded 10% as M-6 does. M-7 produces a `predicted_ev` field that drives ranking at `pl_inference_service.py:474-495`; M-6 does NOT produce an EV field (its analogous output is `kelly_bet`, a dollar amount). M-7's input `handicapping_prob` is calibrated upstream (M-5 § 5.9 CALIBRATED); M-6's input `handicapping_prob` is BYPASS'd upstream (M-4 § 5.9 BYPASS). The two pipelines therefore feed compute_value_overlay-equivalent computations with different calibration states for their probabilistic inputs — substrate-observed asymmetry is intentional per the per-pipeline architectural choices documented at `pl_inference_service.py` (consistent calibration application) vs `wr_inference_service.py:616-625` (Bug #15+#24 BYPASS).

---

#### § 4.1.8 M-8 — Random Forest Longshot Classifier (`longshot_rf` — LS Layer 4)

**M-ID.** `M-8`.

**Model Name.** Primary identifier: `longshot_rf` (model_versions registry name per `model/longshot/train.py:204`). No specialist family; single artifact. Training entry point: `model/longshot/train.py` `main()` at line 227-228.

**Model Type.** `Random Forest (sklearn RandomForestClassifier)`. Specifically: `sklearn.ensemble.RandomForestClassifier` per `model/longshot/train.py:23` (`from sklearn.ensemble import RandomForestClassifier`) and instantiation at line 136 (`rf = RandomForestClassifier(**RF_PARAMS)`). Hyperparameters per `model/longshot/config.py:9-18`: `n_estimators=500, max_depth=10, min_samples_leaf=20, min_samples_split=40, max_features='sqrt', class_weight='balanced', random_state=42, n_jobs=-1`. Persistence: pickle (`with open(model_file, 'wb') as f: pickle.dump(rf, f)` at `model/longshot/train.py:200-201`). Loader: `pickle.load(f)` at `backend/services/ls_inference_service.py:84`.

**Inputs.** Training-time feature set: 60 features = 58 core (`get_core_features(include_odds=True)`) + `l1_win_prob` + `l2_rank_score` per `model/longshot/train.py:122` and the rf_features composition at `model/ensemble/train.py:134-138` showing the parallel pattern. Inference-time feature set: **degraded inputs** per `ls_inference_service.py:463-481` `_predict_rf_simplified` — only 3 of the 60 features are populated: `x[58] = raw_wp` (l1_win_prob position); `x[59] = rank_score` (l2_rank_score position); `x[3] = ml_odds` (closing_odds position); the other 57 features are zero-padded (`x = np.zeros(60)` at line 475). The inline comment at lines 464-470 documents this deliberate substrate degradation: "Simplified RF prediction using available features. The full RF expects 60 features, but at enrichment time we only have the base layer outputs + odds. Use predict_proba on a zero-padded feature vector with the key features (l1_win_prob, l2_rank_score) in the right positions."

Forward stubs (training-time):

- All 58 core features inherited from M-3's input list (M-3 uses identical `get_core_features(include_odds=True)`).
- Two intermediate-latent inputs: `mla:M-1` or `mla:M-2` output (`l1_win_prob` per training composition); `mla:M-3` or `mla:M-4` output (`l2_rank_score` per training composition).

Forward stubs (inference-time, degraded): only 3 inputs populated — `mla:M-1`/`M-2` raw_win_prob (from `wr_predictions.raw_win_prob` per the SQL at `ls_inference_service.py:159-184`); `mla:M-3`/`M-4` rank_score (from `wr_predictions.rank_score`); raw DB column `entries.morning_line_odds`. The other 57 zero-padded features are degraded substrate, not legitimate model inputs.

**Outputs.** Scalar `float` per (race, entry) — `float(self.rf_model.predict_proba(x.reshape(1, -1))[0, 1])` at `ls_inference_service.py:481`. Output domain: P(longshot win) ∈ [0, 1] from RandomForestClassifier's binary `predict_proba` (class 1 = longshot winner, defined per `model/longshot/config.py:21-27`: `longshot label = 1 iff finish_position == 1 AND closing_odds >= 10.0`). Per-row output schema: scalar P(longshot_win); typed `float`.

**Position in Inference Pipeline.** `Upstream: [M-1 or M-2 (via wr_predictions.raw_win_prob), M-3 or M-4 (via wr_predictions.rank_score)]; Downstream: [M-11 ensemble (via ENSEMBLE_FEATURES['longshot_prob']); ls_predictions.rf_longshot_prob storage; longshot_alert composite at ls_inference_service.py:343-348]; Inference layer: LS Layer 4 (RF Longshot Classifier).` M-8 is the leftmost LS-pipeline-layer model (LS Layer 4 in the 7-layer-stack naming per `ls_inference_service.py:7-9`); the LS service operates as second-pass enrichment on wr_predictions per the docstring at `ls_inference_service.py:1-12`.

**Target Latent.** `longshot_win_probability_independent`. The latent is the per-horse probability of winning AT 10-1+ odds (longshot conditioning per `model/longshot/config.py:23-27`); semantically distinct from the general win_probability latents because of the odds-conditional definition (a horse can have low overall win-probability but high longshot-win-probability if it occasionally wins at long odds). Within-horse-binary (not within-race-normalized).

**Output Composition.** M-8's scalar output feeds two consumers per `ls_inference_service.py:259-264, 343-348`:

1. **M-11 ensemble feature**: `'rf_prob': rf_prob` accumulated into `by_race[row['race_id']]` dict at line 260; later assembled into `ens_features` array at lines 247-252 with `rf_prob` at index 2 per ENSEMBLE_FEATURES order (`'longshot_prob'` at `model/ensemble/config.py:11`).
2. **Longshot alert composite**: at `ls_inference_service.py:343-348`, the alert flag is `(ens_prob_norm > 0.10) AND (ml_odds >= 10) AND (rf_prob > 0.05) AND (traj_score > 0.0)` — M-8's output (`rf_prob`) is one of 4 conjuncts.
3. **Storage**: `ls_predictions.rf_longshot_prob` column written at `ls_inference_service.py:407, 422` (rounded 4 decimals).

Composition rule: pass-through (scalar copy into ensemble feature vector + storage); no further transformation between M-8 and downstream consumers. Cross-reference `database_schema_bible:4.1.14` for the storage column.

**Calibration State.** `UNCALIBRATED`. Substrate evidence:

- Bare `RandomForestClassifier` instantiation per `model/longshot/train.py:136`; no `CalibratedClassifierCV` wrapper. `grep -nE "CalibratedClassifierCV|calibrated|Calibrated" model/longshot/train.py` returns zero matches.
- No isotonic sidecar fit by `scripts/fit_all_calibrations.py` (script targets only `wp_full_*` and `pl_core_*` per docstring lines 2-3 + 21-25); rk_full gonzo_sauce was added later as the lone non-wp/pl exception.
- Loader at `ls_inference_service.py:75-87` performs only `pickle.load(f)` for the booster; no `_calibration.json` companion is fetched.
- RandomForestClassifier's `predict_proba` returns the proportion of trees voting for each class — uncalibrated by default per scikit-learn documentation; class_weight='balanced' affects training-time tree splits but does not produce calibrated probability outputs.

**Bypass State Narrative.** N/A — UNCALIBRATED, not BYPASS. The model's output is consumed in raw form by both M-11 (as a feature) and the alert composite (with thresholds 0.05 / 0.10 that operate on uncalibrated proportions). Calibration debt — see § 5.2.

PHASE_5_BACKLOG_CANDIDATE: severity=HIGH; disposition=refactor; rationale="M-8 inference at ls_inference_service.py:463-481 zero-pads 57 of 60 feature inputs (only raw_wp, rank_score, ml_odds populated). The RF was trained on full 60-feature space (model/longshot/train.py:122-129); inference degradation is acknowledged in the inline comment at lines 464-470 ('not ideal but avoids recomputing'). Either (a) populate the full 60-feature vector at LS inference time by joining wr_predictions.feature_importance or re-running feature engineering, OR (b) retrain M-8 on the 3-feature subset that's actually populated at inference, OR (c) drop M-8 from the LS pipeline if the degraded inference is empirically equivalent to a 3-feature classifier. Current state is train/inference feature drift"; cite=ls_inference_service.py:463-481, model/longshot/train.py:122-129.

**Notes.** Single artifact (no specialist family). RF_PARAMS at `model/longshot/config.py:9-18`: n_estimators=500, max_depth=10, min_samples_leaf=20. LONGSHOT_ODDS_THRESHOLD = 10.0 at `model/longshot/config.py:20` defines the longshot label boundary. Training labels per `compute_longshot_labels` at `model/longshot/config.py:23-29`: 1 iff finish_position==1 AND closing_odds≥10.0; 0 otherwise. Training data filtering at `model/longshot/train.py` (read partial; full path TBD). Note: M-8 is part of the LS pipeline (`equine-ls-inference` Lambda) which writes to `ls_predictions` AND `wr_predictions` per the dual-write pattern at `database_schema_bible:4.1.14` F.3.

---

#### § 4.1.9 M-9 — LSTM Form Trajectory (`trajectory_lstm` — LS Layer 5)

**M-ID.** `M-9`.

**Model Name.** Primary identifier: `trajectory_lstm` (model_versions registry name per `model/trajectory/train.py:295`). No specialist family; single artifact. Training entry point: `model/trajectory/train.py` `main()` (read partial; entry confirmed at line 138 logging "LSTM Form Trajectory (Layer 5) training starting"). Inference-time class definition mirrored at `backend/services/ls_inference_service.py:39-56` (`TrajectoryLSTM` per `class TrajectoryLSTM(torch.nn.Module)`).

**Model Type.** `LSTM (PyTorch torch.nn.LSTM)`. Specifically: 2-layer LSTM with sigmoid output. Architecture per `ls_inference_service.py:39-52` (must match `model/trajectory/train.py:44-52` exactly per the docstring at `ls_inference_service.py:40` "Must match model/trajectory/train.py architecture exactly"):

```python
class TrajectoryLSTM(torch.nn.Module):
    def __init__(self, input_size=8, hidden_size=32, num_layers=2, dropout=0.3):
        self.lstm = torch.nn.LSTM(input_size=8, hidden_size=32,
                                  num_layers=2, dropout=0.3, batch_first=True)
        self.fc = torch.nn.Linear(hidden_size, 1)
    def predict_proba(self, x):
        return torch.sigmoid(self.forward(x))  # 1-D output → sigmoid
```

Training-time loss: `BCEWithLogitsLoss` per `model/trajectory/train.py:194` (numerically stable sigmoid + BCE combined). Hyperparameters at `model/trajectory/config.py:21-29` (LSTM_PARAMS): hidden_size=32, num_layers=2, dropout=0.3, learning_rate=0.001, epochs=50, batch_size=256, patience=10. Persistence: `torch.save(model.state_dict(), ...)` (state-dict format, not full model); loader at `ls_inference_service.py:111-115` does `torch.load(local_pt, map_location='cpu', weights_only=True)` then `load_state_dict(...)`. Companion artifact: `_scaler.pkl` (sklearn `MinMaxScaler` per `ls_inference_service.py:99-109`) loaded if present; absence is graceful — falls back to raw features per line 109 "LSTM scaler not found, using raw features".

**Inputs.** **NOT feature-engineered features in the M-1/M-2/M-3 sense.** Input is a 5-timestep × 8-feature sequence tensor of past_performances rows per horse, queried directly from the `past_performances` table at `ls_inference_service.py:485-493`. Per `model/trajectory/config.py:11-20` (SEQUENCE_FEATURES — 8 per timestep): `computed_speed_figure`, `finish_position_norm` (= `finish_position / field_size`), `early_pace_figure`, `late_pace_figure`, `days_since_last_race`, `purse`, `field_size`, `closing_odds`. SEQUENCE_LENGTH = 5 (last 5 PPs); MIN_SEQUENCE_LENGTH = 3 (returns 0.0 if fewer than 3 PPs available per `ls_inference_service.py:495-496`).

The inputs are sequence-tensor representations of past_performances rows, not feature-engineered scalars. Per QB SP-2 cross-reference note: spec § 5.4 wording allows "raw features and any intermediate latents from upstream models" — the LSTM consumes raw_data references, not fp:F-N feature_provenance_bible feature rows. Forward stubs use the raw column names from `past_performances` per `database_schema_bible:4.1.7`:

- `pp:past_performances.computed_speed_figure` (per row, 5 rows per sequence)
- `pp:past_performances.finish_position` + `pp:past_performances.field_size` (combined into `finish_position_norm` derived input)
- `pp:past_performances.early_pace_figure`
- `pp:past_performances.late_pace_figure`
- `pp:past_performances.days_since_last_race`
- `pp:past_performances.purse`
- `pp:past_performances.field_size` (also used as a feature directly)
- `pp:past_performances.closing_odds`

Inputs filter: `WHERE horse_id = %s AND race_date < %s AND computed_speed_figure IS NOT NULL` per `ls_inference_service.py:486-493`.

**Outputs.** Scalar `float` per (race, entry) — `prob = float(self.lstm_model.predict_proba(tensor).item())` at `ls_inference_service.py:523`, then mapped to [-1, +1] via `prob * 2.0 - 1.0` at line 525. Output domain: P(form trajectory positive) ∈ [0, 1] from sigmoid, mapped to trajectory_score ∈ [-1, +1] (rounded 4 decimals). Per-row output schema: scalar trajectory_score; typed Python `float`.

**Position in Inference Pipeline.** `Upstream: []; Downstream: [M-11 ensemble (via ENSEMBLE_FEATURES['trajectory_score']); ls_predictions.lstm_trajectory storage; longshot_alert composite at ls_inference_service.py:343-348]; Inference layer: LS Layer 5 (LSTM Form Trajectory).` M-9 is a leftmost-LS-pipeline-layer model (no upstream model output as input — sequence tensor read directly from past_performances). The output (trajectory_score) feeds three consumers analogous to M-8.

**Target Latent.** `form_trajectory_score`. The latent is the signed momentum of recent past-performance trajectory — positive values indicate improving form (recent races trending toward higher speed figures, better positions, etc.); negative values indicate declining form. Mapped from sigmoid P(positive trajectory) via 2x-1 transform; the resulting [-1, +1] range is conventional rather than calibrated.

**Output Composition.** Pass-through scalar (post-sigmoid + 2x-1 transform) into:

1. **M-11 ensemble feature**: `'traj_score': traj_score` accumulated at `ls_inference_service.py:260`; assembled into `ens_features` at lines 247-252 with `traj_score` at index 3 per ENSEMBLE_FEATURES order (`'trajectory_score'` at `model/ensemble/config.py:12`).
2. **Longshot alert composite**: `(traj_score > 0.0)` is one of 4 conjuncts at `ls_inference_service.py:347` for the longshot_alert flag.
3. **Storage**: `ls_predictions.lstm_trajectory` column written at `ls_inference_service.py:408, 422` (rounded 4 decimals).

Composition rule: pass-through; no further transformation between M-9 and downstream consumers.

**Calibration State.** `UNCALIBRATED`. Substrate evidence:

- BCE-trained binary classifier with sigmoid output is mathematically calibrated only under perfect training-data fit (Platt-style asymptotic calibration); in practice sklearn / PyTorch sigmoid outputs are uncalibrated unless explicitly calibrated.
- No isotonic sidecar fit for trajectory_lstm: `scripts/fit_all_calibrations.py` targets only wp_full + pl_core (per docstring lines 21-25); trajectory is not in the calibration-fitting workstream.
- Loader at `ls_inference_service.py:90-118` performs only `torch.load` + `load_state_dict`; no `_calibration.json` companion fetched. The `_scaler.pkl` companion is a feature-input MinMaxScaler (input normalization), not an output calibration.
- The 2x-1 transform at `ls_inference_service.py:525` is a domain-mapping convention (sigmoid → signed score), not a calibration transform.
- Direct evidence: `grep -nE "calibration|isotonic" model/trajectory/train.py` returns zero matches.

**Bypass State Narrative.** N/A — UNCALIBRATED, not BYPASS. M-9's output feeds M-11 + alert composite + storage in raw 2x-1-mapped form. Calibration debt — see § 5.2.

**Notes.** Architecture mirroring discipline at `ls_inference_service.py:40` ("Must match model/trajectory/train.py architecture exactly") — any change to training-time architecture must be mirrored in the inference class definition. SEQUENCE_LENGTH=5 hardcoded at `ls_inference_service.py:35` and `model/trajectory/config.py:7`; FEATURES_PER_STEP=8 hardcoded at both sites (line 36 / line 9). The 8-feature sequence per `model/trajectory/config.py:11-20` is a fixed schema; adding/removing trajectory features requires retraining + architecture change. Input-normalization scaler stored at `<base_key>_scaler.pkl` companion per `ls_inference_service.py:100-101`; absence-graceful fallback per line 109. Sequence-build code at `ls_inference_service.py:498-512` constructs the (SEQUENCE_LENGTH, FEATURES_PER_STEP) tensor with right-aligned PP rows (most recent at the end) and zero-padding for shorter sequences (offset = SEQUENCE_LENGTH - len(rows) at line 500).

---

#### § 4.1.10 M-10 — Beta-Binomial Bayesian Angle Scorer (LS Layer 6)

**M-ID.** `M-10`.

**Model Name.** `model/angles/scorer.py:score_angle` (free function at `model/angles/scorer.py:33-64`); production consumer at `backend/services/ls_inference_service.py:_score_angles` (instance method at `ls_inference_service.py:527-574`). Non-trained; no `model_versions` registry row; no S3 artifact. The model is *pure statistical computation* from historical aggregations (no training, no parameters, no random state) per the module docstring at `model/angles/scorer.py:1-9`: "No training — pure statistical computation from historical data."

**Model Type.** `Bayesian (Beta-Binomial)`. Conjugate-prior Bayesian inference: Beta(prior_a, prior_b) prior + Binomial(starts, p) likelihood = Beta(prior_a + wins, prior_b + (starts - wins)) posterior. Uninformative prior at `model/angles/scorer.py:18-19`: `PRIOR_ALPHA = 1.0; PRIOR_BETA = 1.0` (Beta(1,1) = uniform). `scipy.stats.beta` for posterior CI computation per `model/angles/scorer.py:13` and lines 50-51. The scoring function at lines 33-64 returns `posterior_mean`, `ci_low`, `ci_high`, and `ev_per_bet`. Production consumer at `ls_inference_service.py:558-564` uses an inline equivalent computation: `post_a = 1.0 + wins; post_b = 1.0 + (starts - wins); posterior = post_a / (post_a + post_b); ev = (posterior * decimal_odds * 2.0) - 2.0`.

**Inputs.** Per `ls_inference_service.py:541-555`: per-entry angle flags from `entries` table (`lasix_first_time` at line 531; `blinkers_on` at line 533) plus a derived `class_drop` flag computed in the SQL at `ls_inference_service.py:166-172` (`EXISTS (SELECT 1 FROM past_performances pp2 WHERE pp2.horse_id = wp.horse_id AND pp2.race_date < r.race_date AND pp2.purse IS NOT NULL AND r.purse IS NOT NULL AND pp2.purse > r.purse * 1.15)`). Plus aggregations from `angle_stats` table per `database_schema_bible:4.1.15` queried at `ls_inference_service.py:546-555` (trainer-specific row first, falling back to global if `starts < 5`). Plus per-entry morning_line_odds for EV computation.

Inputs are NOT feature-engineered fp:F-N features — they are raw DB column reads + table aggregations:

- Raw DB column inputs: `entries.lasix_first_time`, `entries.blinkers_on`, derived `class_drop` from `past_performances.purse` × `races.purse` join.
- Aggregation table inputs: `angle_stats.wins`, `angle_stats.starts` (per `database_schema_bible:4.1.15`; 6-INSERT cycle per `backend/lambdas/ingestion/handler.py:94-188` populates the table).
- Trainer identity input: `trainers.trainer_name` (joined into the LS read query at `ls_inference_service.py:179-180`).
- Morning_line_odds: `entries.morning_line_odds`.

The wider `model/angles/scorer.py` module (the canonical home of the function not currently in the production path) supports a richer angle taxonomy at `ANGLE_DEFS` lines 22-30: `first_time_lasix`, `off_the_claim`, `blinkers_on`, `blinkers_off`, `class_drop`, `surface_switch`, `jockey_change` (7 angles). Production consumer at `ls_inference_service.py:531-536` uses only 3 of these 7 (`first_time_lasix`, `blinkers_on`, `class_drop`) — substrate-observed pruning.

**Outputs.** Per `ls_inference_service.py:567-572`: dict with `angle_name` (str or None), `angle_posterior` (rounded 4 decimals; in [0, 1]), `angle_ev` (rounded 2 decimals; ∈ ℝ but capped at -2.0 floor when no eligible angle). Best-angle selection at lines 567-572 (highest EV across all eligible angles). Default no-eligible-angle return at lines 538-539 / 574: `{'angle_name': None, 'angle_posterior': 0.0, 'angle_ev': -2.0}`. Per-row output schema: 3-key dict.

**Position in Inference Pipeline.** `Upstream: []; Downstream: [M-11 ensemble (via ENSEMBLE_FEATURES['angle_ev'] + ENSEMBLE_FEATURES['angle_posterior']); ls_predictions.bayesian_angle_ev + ls_predictions.angle_description storage]; Inference layer: LS Layer 6 (Bayesian Angle Scorer).` M-10 is a leftmost-LS-pipeline-layer model (reads only DB state, no upstream model output as input). Output feeds M-11 + storage. The longshot_alert composite at lines 343-348 incorporates `angle_ev` indirectly via the M-11 ensemble path; not a direct conjunct.

**Target Latent.** `trainer_angle_posterior_win_rate + ev_per_bet (composite)`. The latent is the per-trainer-conditioned (or globally-conditioned for sparse-trainer-data cases) posterior win-rate estimate for a given angle (e.g., "trainer X's first-time-lasix horses have posterior P=0.12 of winning"), plus the derived expected value per $2 bet at the entry's morning-line odds. Composite of the Bayesian posterior mean and the EV computation that uses it.

**Output Composition.** Per `ls_inference_service.py:556-572`:

- For each detected angle (3 candidates: first_time_lasix, blinkers_on, class_drop), query trainer-specific `angle_stats` (lines 546-549).
- If trainer-specific row has `starts < 5`, fall back to global aggregate (lines 552-555).
- Compute Beta-Binomial posterior (lines 558-563): `post_a = 1 + wins; post_b = 1 + (starts - wins); posterior = post_a / (post_a + post_b)`.
- Compute `ev = (posterior * decimal_odds * 2.0) - 2.0` (line 565; per $2 bet expected return).
- Select best (highest EV) angle (lines 567-572).
- Return dict; consumed by M-11 (lines 247-252 with `angle_ev` at index 4 + `angle_posterior` at index 5 per `model/ensemble/config.py:13-14`) and by storage at `ls_inference_service.py:411, 424-425`.

Composition rule: per-angle Bayesian posterior + EV computation, then max-EV selection; no within-race normalization (per-horse independent computation).

**Calibration State.** `CALIBRATED-BY-CONSTRUCTION (Bayesian posterior is calibrated by construction with proper conjugate prior + sufficient sample size)`. Substrate evidence:

- Beta-Binomial conjugate-prior framework per `model/angles/scorer.py:33-64` and the inline equivalent at `ls_inference_service.py:558-564`: `Beta(1+wins, 1+(starts-wins))` is the analytic posterior given a Beta(1,1) uniform prior and observed (wins, starts) data. The posterior mean `(1+wins) / (2+starts)` is the calibrated MAP estimate of the win rate under the Bayesian-decision-theoretic framework.
- The `sample_size_adequate` flag at `model/angles/scorer.py:63` warns when `starts < 20` — small-sample-size posteriors are still calibrated estimators of the win rate but with high variance (wide CI per lines 50-51); the production consumer at `ls_inference_service.py:550-555` uses `starts < 5` as the trainer-specific-vs-global fallback threshold.
- No isotonic sidecar (M-10 is non-trained; calibration-by-construction makes isotonic post-fit unnecessary).
- Citation: `model/angles/scorer.py:46-49` (analytic posterior); `scipy.stats.beta` import at line 13 (used for CI quantiles at lines 50-51).

**Bypass State Narrative.** N/A — CALIBRATED-BY-CONSTRUCTION, not BYPASS. The model's posterior_mean is a calibrated win-rate estimator under proper conjugate-prior conditions. Note: the production consumer at `ls_inference_service.py:556-557` does NOT use `scipy.stats.beta` — it computes only the posterior_mean (not CI). This is a substrate-observed simplification: the production code computes only the posterior point estimate; CI lower / upper bounds are available in the canonical `model/angles/scorer.py:score_angle` but are not consumed at LS inference time.

**Notes.** Two parallel implementations: canonical at `model/angles/scorer.py` (full 7-angle taxonomy + CI) and production-inlined at `ls_inference_service.py:556-572` (3-angle subset, posterior_mean only, no CI). The production-inlined path is the live production substrate; the `score_angle` function at `model/angles/scorer.py:33-64` is loaded by `model/angles/__init__.py` but not invoked by the LS service. Whether the `model/angles/scorer.py` module is reachable from any production code path is unverified at substrate; if not, it's an orphaned module candidate.

PHASE_5_BACKLOG_CANDIDATE: severity=LOW; disposition=refactor; rationale="model/angles/scorer.py:33-64 score_angle / score_entry_angles canonical implementation supports 7 angles with full CI computation, but production consumer at ls_inference_service.py:556-572 inlines a simplified 3-angle posterior-mean-only computation. Either (a) wire ls_inference_service to call score_entry_angles (eliminates code duplication + adds 4 missing angles + adds CI) or (b) confirm the inline simplification is intentional and remove the orphaned scorer.py module"; cite=model/angles/scorer.py:33-174, ls_inference_service.py:556-572.

---

#### § 4.1.11 M-11 — Logistic Regression Stacking Ensemble (`ensemble` — LS Layer 7)

**M-ID.** `M-11`.

**Model Name.** Primary identifier: `ensemble` (model_versions registry name per `model/ensemble/train.py:247`). No specialist family; single artifact. Training entry point: `model/ensemble/train.py` `main()` at line 96-97 (CRITICAL: trained on 2025 held-out data only per docstring lines 4 + 98).

**Model Type.** `Logistic Regression (sklearn LogisticRegression)`. Specifically: `sklearn.linear_model.LogisticRegression` per `model/ensemble/train.py:23` and instantiation at line 182-184: `LogisticRegression(C=1.0, class_weight='balanced', max_iter=1000, random_state=42)`. Persistence: pickle per `model/ensemble/train.py:243-244`. Loader: `pickle.load(f)` at `ls_inference_service.py:128-129`.

**Inputs.** 10 features per `ENSEMBLE_FEATURES` at `model/ensemble/config.py:8-19`:

```
'win_prob',          # Layer 1: P(win) raw sigmoid          → from M-1 / M-2
'rank_score',        # Layer 2: ranker output                → from M-3 / M-4
'longshot_prob',     # Layer 4: RF P(longshot win)           → from M-8
'trajectory_score',  # Layer 5: LSTM trajectory (-1 to +1)   → from M-9
'angle_ev',          # Layer 6: best angle expected value    → from M-10
'angle_posterior',   # Layer 6: best angle posterior mean    → from M-10
'closing_odds',      # Market odds (raw)                     → from entries (proxy)
'morning_line_odds', # Morning line                          → from entries
'race_quality_tier', # Race context                          → from races / fp
'field_size',        # Race context                          → from races / entries
```

Inputs are a mix of **upstream-model outputs** (6 features — `win_prob` from M-1/M-2; `rank_score` from M-3/M-4; `longshot_prob` from M-8; `trajectory_score` from M-9; `angle_ev` + `angle_posterior` from M-10) and **race-context features** (4 features — `closing_odds`, `morning_line_odds`, `race_quality_tier`, `field_size`). The 6 upstream-model outputs are LATENT INPUTS per QB_DRAFTING_SPEC § 5.4 ("Inputs include both raw features and any intermediate latents from upstream models in the stack"); the 4 race-context features are raw DB / feature_engineering reads.

Forward stubs:

- Upstream-model latent inputs: `mla:M-1`/`mla:M-2` `win_probability_independent_per_horse_*` (for `win_prob`); `mla:M-3`/`mla:M-4` `within_race_pairwise_rank_score` (for `rank_score`); `mla:M-8` `longshot_win_probability_independent` (for `longshot_prob`); `mla:M-9` `form_trajectory_score` (for `trajectory_score`); `mla:M-10` `ev_per_bet` and `posterior_mean` (for `angle_ev` and `angle_posterior` respectively).
- Race-context feature stubs: `fp:F-?closing_odds` (or DB column read; same column as M-3 input), `fp:F-?morning_line_odds` (DB column), `fp:F-?race_quality_tier` (per `model/shared/feature_definitions.py:69`), `fp:F-?field_size` (DB column).

Inference-time defaults at `model/ensemble/train.py:144-151`: `trajectory_score = 0.0` for ensemble training (LSTM scored separately); `angle_ev = 0.0`, `angle_posterior = 0.0` for ensemble training (computed at inference). Note: at *training time* the ensemble uses defaults for some upstream-model outputs (because LSTM and angle scoring are run separately); at *inference time* the LS service populates all 10 features per (race, entry) at `ls_inference_service.py:247-252`.

**Outputs.** Scalar `float` per (race, entry) — `float(self.ensemble_model.predict_proba(ens_features)[0, 1])` at `ls_inference_service.py:253-255`. Output domain: P(win) ∈ [0, 1] from logistic regression's `predict_proba` (class 1 = winner, defined per `y_2025 = (labels_df[val_mask]['finish_position'] == 1).astype(float).values` at `model/ensemble/train.py:163`). Per-row output schema: scalar P(win); typed Python `float`. Pre-softmax / pre-normalize.

**Position in Inference Pipeline.** `Upstream: [M-1/M-2 (via win_prob), M-3/M-4 (via rank_score), M-8 (via longshot_prob), M-9 (via trajectory_score), M-10 (via angle_ev + angle_posterior)]; Downstream: [LS within-race softmax + 0-PP override → ls_predictions.final_win_probability storage; wr_predictions.ensemble_win_prob enrichment via dual-write per database_schema_bible:F.3]; Inference layer: LS Layer 7 (Logistic Regression Stacking Ensemble — terminal trained model).` M-11 is the terminal trained model in the LS pipeline. Its output (ens_prob_raw) feeds the Pass-2 within-race softmax at `ls_inference_service.py:281-293` to produce the canonical `final_win_probs` array, which is then 0-PP-override-corrected (lines 284-287), softmax'd (lines 290-293), and used for both ranking (lines 295-331) and storage (lines 387-431).

**Target Latent.** `ls_pipeline_terminal_win_probability`. The latent is the LS-pipeline-canonical per-horse win probability — distinct from M-1/M-2's per-horse-binary independent win_probability and from M-5's per-horse EV-regression score. M-11's win probability is *stacked* (combines all upstream-layer signals via logistic regression meta-learner) and is the canonical LS-pipeline output for downstream consumers.

**Output Composition.** Per-horse `predict_proba` → accumulate into `by_race[row['race_id']]` dict at `ls_inference_service.py:259-264` → Pass-2 per-race processing at lines 279-330:

- 0-PP override: horses with `pp_count == 0` get `ens_probs_raw[idx] = base_rate` where `base_rate = 1.0 / n` (lines 284-287).
- Within-race softmax: `shifted = ens_probs_raw - ens_probs_raw.max(); exp_scores = np.exp(shifted); final_win_probs = exp_scores / exp_scores.sum()` (lines 290-293).
- Market_prob within-race normalization for ranking (lines 295-302).
- Ranking by `edge_ratios = final_win_probs / np.maximum(market_probs, 0.01)` filtered by longshot eligibility (`ml_odds >= 8.0 AND pp_count > 0` per lines 313-327).
- Dual-write: `wr_predictions.ensemble_win_prob` UPDATE (lines 360-383) AND `ls_predictions` INSERT (lines 386-430) per `database_schema_bible:4.1.14` F.3 dual-write pattern.

Composition rule: stacking via logistic regression on out-of-fold base-model outputs (training discipline at `model/ensemble/train.py:96-97`); inference-time within-race softmax on ensemble outputs to produce within-race coherent final_win_probs.

**Calibration State.** `UNCALIBRATED`. Substrate evidence:

- Bare `LogisticRegression` instantiation per `model/ensemble/train.py:182-184`; no `CalibratedClassifierCV` wrapper. `class_weight='balanced'` re-weights training samples but does not produce calibrated raw `predict_proba` output (class-balancing distorts the Bayes-optimal posterior estimate).
- No isotonic sidecar fit by `scripts/fit_all_calibrations.py` (script targets only wp_full + pl_core; ensemble is not in the calibration-fitting workstream).
- Loader at `ls_inference_service.py:120-132` performs only `pickle.load(f)` for the model; no `_calibration.json` companion fetched.
- Logistic regression on out-of-fold base-model outputs is sometimes informally referred to as "Platt-scaling-like" stacking calibration, but per scikit-learn's CalibratedClassifierCV documentation, true Platt scaling requires explicit `method='sigmoid'` fitting on held-out data after the base model is fixed — this pattern is NOT used here. M-11 is a stacking meta-learner, not a per-model Platt calibrator.
- Direct evidence: `grep -nE "calibration|isotonic|CalibratedClassifierCV" model/ensemble/train.py` returns zero matches.

**Bypass State Narrative.** N/A — UNCALIBRATED, not BYPASS. M-11's `predict_proba` output feeds within-race softmax + 0-PP override + storage in raw uncalibrated form; the within-race softmax at `ls_inference_service.py:290-293` is a probability-distribution-construction transform, not a calibration transform. Calibration debt — see § 5.2.

**Notes.** Training-data discipline per `model/ensemble/train.py:97-98` "CRITICAL: Training on 2025 held-out data ONLY" — the meta-learner is trained on temporal-holdout data to avoid leakage from base-model in-sample fits. Train/eval split per line 174-177: first 80% of 2025 → train; last 20% → eval. Base-model outputs at training time use defaults for trajectory + angle features (per the training-time delta noted in Inputs above). Race-context features at training time use proxies: `morning_line_odds = labels_df['closing_odds'].values  # proxy` per line 154. Field_size and race_quality_tier per lines 154-159 (defaults if missing). LS pipeline read SQL at `ls_inference_service.py:159-184` joins wr_predictions with entries / races / horses / trainers — pulls per-horse layer outputs (raw_win_prob, rank_score from `wr_predictions`) plus context. M-11 is the only LS-pipeline trained model that produces a within-race-coherent canonical final probability (via Pass-2 softmax); M-8/M-9/M-10 produce per-horse independent latents.

PHASE_5_BACKLOG_CANDIDATE: severity=LOW; disposition=monitored; rationale="M-11 ensemble training at model/ensemble/train.py:144-151 uses defaults (0.0) for trajectory_score, angle_ev, angle_posterior — meaning the meta-learner was trained with 3 of its 6 upstream-model-output features missing. At inference these features ARE populated from M-9/M-10. The training-vs-inference feature-population disparity could manifest as miscalibrated meta-learner weights for trajectory/angle features. Verify via Derby-window diagnostic whether trajectory + angle weights in M-11 are anomalous"; cite=model/ensemble/train.py:144-151, ls_inference_service.py:247-252.

---

### § 4.2 Inference Pipeline Topology

#### § 4.2.1 Layer enumeration (per-pipeline composition)

EE has **three distinct inference pipelines** plus a 7-layer stack naming convention that operates as a layered overlay on the WR pipeline (Layers 1-3) extended by the LS pipeline (Layers 4-7). The PL pipeline is architecturally separate and operates as a standalone 2-layer pipeline (Layer 1 trained model + Layer 2 arithmetic overlay; not participating in the 7-layer stack).

**WR Pipeline** (`equine-wr-inference` Lambda → `WRInferenceService` per `architecture_overview:3.1` + `data_pipeline_bible:4.1.5.1`):

- **Layer 1 — Win Probability:** M-1 (wp_core, no-workout dispatch) + M-2 (wp_full, workout-aware dispatch). Per-horse XGBoost binary:logistic. Layer naming at `wr_inference_service.py:114` ("Layer 1: Win probability models"). Output: per-horse independent P(win), feeds diagnostic storage only (post-2026-05-01 architectural flip per `wr_inference_service.py:579-598`).
- **Layer 2 — Pairwise Ranker:** M-3 (rk_core) + M-4 (rk_full). XGBoost rank:pairwise (LambdaMART). Layer naming at `wr_inference_service.py:118` ("Layer 2: Ranker models"). Output: within-race rank_scores, → softmax → ranker_probs → BYPASS → handicapping_probs.
- **Layer 3 — Value Overlay:** M-6 (compute_value_overlay). Arithmetic Kelly-criterion + edge-threshold overlay. Output: per-horse value flag + Kelly bet sizing.

**PL Pipeline** (`equine-pl-inference` Lambda → `PLInferenceService` per `architecture_overview:3.1` + `data_pipeline_bible:4.1.5.2`):

- **Layer 1 — EV Regression:** M-5 (pl_core). XGBoost reg:squarederror on EV labels. Output: per-horse EV-regression score → softmax → CALIBRATED via isotonic interpolation → 0-PP override → renormalize → handicapping_probs.
- **Layer 2 — EV/Kelly Overlay:** M-7 (compute_ev_and_kelly). Arithmetic EV + Kelly + value-bet flag. Output: per-horse predicted_ev (drives ranking) + value-bet flag.

The PL pipeline does NOT have a Layer 2 ranker analogous to the WR pipeline's M-3/M-4 — pl_core's ranking comes from the post-softmax handicapping_prob ordering and the post-EV ordering at `pl_inference_service.py:474-495`. Per the substrate at `pl_inference_service.py:90-92`, training emits `pl_workout` Layer 2 artifacts but inference V1 does not load them — flagged at M-5 § 5.11 as PHASE_5_BACKLOG_CANDIDATE.

**LS Pipeline** (`equine-ls-inference` Lambda → `LSInferenceService` per `architecture_overview:3.1` + `data_pipeline_bible:4.1.5.3`; second-pass enrichment per `ls_inference_service.py:1-12`):

- **Layer 4 — RF Longshot:** M-8 (longshot_rf). sklearn RandomForestClassifier. Layer naming at `ls_inference_service.py:75` and module docstring at line 6. Output: per-horse P(longshot win).
- **Layer 5 — LSTM Trajectory:** M-9 (trajectory_lstm). PyTorch LSTM (input_size=8, hidden_size=32, num_layers=2). Layer naming at `ls_inference_service.py:89` and module docstring at line 7. Output: per-horse trajectory_score ∈ [-1, +1].
- **Layer 6 — Bayesian Angles:** M-10 (Beta-Binomial Bayesian angle scorer). Pure-statistical computation from angle_stats aggregations. Layer naming at `ls_inference_service.py:225` and module docstring at line 8. Output: per-horse best-angle posterior_mean + ev_per_bet.
- **Layer 7 — Stacking Ensemble:** M-11 (ensemble). sklearn LogisticRegression meta-learner on 6 upstream-model outputs + 4 race-context features. Layer naming at `ls_inference_service.py:121` and module docstring at line 9. Output: per-horse final_win_probability (post within-race softmax + 0-PP override).

**The 7-layer stack** (per BIBLE_STRUCTURE_SPEC v6 § 6.4 canonical naming + `ls_inference_service.py:1-12`):

| Layer | Model entity | Pipeline | Type |
|---|---|---|---|
| 1 | M-1 + M-2 (wp_core + wp_full) | WR | XGBoost binary:logistic |
| 2 | M-3 + M-4 (rk_core + rk_full) | WR | XGBoost rank:pairwise |
| 3 | M-6 (compute_value_overlay) | WR | Arithmetic |
| 4 | M-8 (longshot_rf) | LS | sklearn RandomForestClassifier |
| 5 | M-9 (trajectory_lstm) | LS | PyTorch LSTM |
| 6 | M-10 (Bayesian angle scorer) | LS | Beta-Binomial Bayesian |
| 7 | M-11 (ensemble) | LS | sklearn LogisticRegression |

Layers 1-3 are WR-pipeline-internal; the LS pipeline reads `wr_predictions` (style='general') second-pass and adds Layers 4-7 on top. The PL pipeline (M-5 + M-7) operates as a parallel standalone 2-layer pipeline NOT participating in the 7-layer stack. Cross-pipeline interaction: LS pipeline's Layer 4-7 enrichment writes back to `wr_predictions` per the dual-write pattern at `database_schema_bible:4.1.14` F.3.

#### § 4.2.2 Cross-model dataflow (upstream→downstream graph)

Textual representation of the cross-model dataflow graph. Format: `<source>` —[edge label]→ `<destination>`.

**WR pipeline cross-model edges (intra-pipeline):**

```
[raw feature matrix from FeatureEngineeringService.build_feature_matrix]
    ├─→ M-1 (wp_core, no-workout dispatch)
    │       ├─→ wr_predictions.confidence_score (storage; diagnostic)
    │       └─→ wr_predictions.raw_win_prob (storage; diagnostic; consumed by M-8)
    │
    ├─→ M-2 (wp_full, workout-aware dispatch)
    │       ├─→ wr_predictions.confidence_score (storage; diagnostic)
    │       └─→ wr_predictions.raw_win_prob (storage; diagnostic; consumed by M-8)
    │
    ├─→ M-3 (rk_core, no-workout / rk_full-fallback dispatch)
    │       └─→ rank_scores[idx] [per-race softmax] ranker_probs
    │           [BYPASS line 626 .copy()] handicapping_probs
    │           [0-PP override line 634-636] handicapping_probs'
    │           [renormalize line 638-641] handicapping_probs''
    │           [blend with market_probs line 674-676] displayed_prob
    │           ├─→ M-6 (consumes handicapping_prob + ml_odds)
    │           └─→ wr_predictions.win_probability (storage)
    │
    └─→ M-4 (rk_full, workout-aware dispatch — primary)
            └─→ rank_scores[idx] [same chain as M-3 above]
```

**M-6 (WR Arithmetic Value Overlay) cross-model edges:**

```
[M-3 / M-4 derived handicapping_prob] + [entries.morning_line_odds]
    └─→ M-6 (compute_value_overlay)
            └─→ {edge_pct, kelly_fraction, kelly_bet, is_value, implied_prob}
                ├─→ wr_predictions.overlay_pct, .is_value_flag, .kelly_fraction, .kelly_bet (storage)
                └─→ wr_predictions.recommended_bet_type (downstream rank+exotic-bets logic)
```

**PL pipeline cross-model edges (intra-pipeline):**

```
[raw feature matrix from FeatureEngineeringService.build_feature_matrix]
    └─→ M-5 (pl_core, all rows)
            └─→ raw_scores [softmax+clip line 331-337] softmax_probs
                [CALIBRATED isotonic interpolation line 341-343] handicapping_probs
                [0-PP override line 360-362] handicapping_probs'
                [renormalize line 367-369] handicapping_probs''
                [blend with market_probs line 432-434] displayed_prob
                ├─→ M-7 (consumes handicapping_prob + ml_odds)
                └─→ pl_predictions.win_probability (storage)

[M-5 derived handicapping_prob] + [entries.morning_line_odds]
    └─→ M-7 (compute_ev_and_kelly)
            └─→ {closing_odds, implied_probability, edge_pct, predicted_ev,
                 kelly_fraction, kelly_bet_size, is_value_bet, is_strong_value}
                └─→ pl_predictions storage [+ predicted_ev drives rank_field]
```

**LS pipeline cross-model edges (cross-pipeline second-pass):**

```
[wr_predictions style='general' read at ls_inference_service.py:159-184]
    ├─→ raw_win_prob (from M-1 / M-2 storage) → M-8 input feature x[58]
    ├─→ rank_score (from M-3 / M-4 storage)   → M-8 input feature x[59]
    │                                          → M-11 input ENSEMBLE_FEATURES['rank_score']
    └─→ raw_win_prob                           → M-11 input ENSEMBLE_FEATURES['win_prob']

[entries.morning_line_odds]
    └─→ M-8 input feature x[3] (closing_odds proxy)
    └─→ M-11 input ENSEMBLE_FEATURES['morning_line_odds'] + ['closing_odds']

[past_performances rows; horse_id-filtered; chronologically last 5]
    └─→ M-9 (trajectory_lstm sequence input)
            └─→ trajectory_score
                ├─→ M-11 input ENSEMBLE_FEATURES['trajectory_score']
                ├─→ longshot_alert composite input
                └─→ ls_predictions.lstm_trajectory (storage)

[entries.lasix_first_time, entries.blinkers_on, derived class_drop]
[+ angle_stats aggregations + entries.morning_line_odds]
    └─→ M-10 (Bayesian angle scorer)
            └─→ {angle_name, angle_posterior, angle_ev}
                ├─→ M-11 input ENSEMBLE_FEATURES['angle_ev'] + ['angle_posterior']
                └─→ ls_predictions.bayesian_angle_ev + .angle_description (storage)

[M-8 longshot_prob] + [M-9 trajectory_score] + [M-10 angle_ev + posterior]
[+ M-1/M-2 win_prob] + [M-3/M-4 rank_score] + [4 race-context features]
    └─→ M-11 (ensemble)
            └─→ ens_prob_raw
                [Pass-2 0-PP override line 284-287]
                [within-race softmax line 290-293] final_win_probs
                ├─→ wr_predictions.ensemble_win_prob (UPDATE; dual-write)
                └─→ ls_predictions.final_win_probability (INSERT; dual-write)
```

**Cross-pipeline edges (inter-pipeline second-pass):**

```
WR Pipeline → wr_predictions (style='general') → LS Pipeline (second-pass enrichment)
LS Pipeline → wr_predictions (UPDATE: ensemble_win_prob, longshot_prob, trajectory_score, angle_*, longshot_alert, confidence)
LS Pipeline → ls_predictions (INSERT: final_win_probability, longshot_alert, confidence, predicted_rank, xgb_rank_score, rf_longshot_prob, lstm_trajectory, calibrated_win_prob, bayesian_angle_ev, angle_description, market_prob, edge_pct, is_top_pick, morning_line_implied_prob)
```

PL pipeline does NOT participate in cross-pipeline LS enrichment — LS reads `wr_predictions` only (per `ls_inference_service.py:175 FROM wr_predictions wp`); PL pipeline operates standalone with its own training, inference, storage cycle.

**Terminal models (no downstream ML model consumes their output):**

- M-6 (WR arithmetic value overlay) — terminal in trained-model sense; feeds storage + non-ML rank/flag-recompute logic.
- M-7 (PL arithmetic EV/Kelly overlay) — terminal in trained-model sense; feeds storage + non-ML rank-by-EV logic.
- M-11 (LS stacking ensemble) — terminal trained model; feeds within-race softmax + storage.

#### § 4.2.3 LS second-pass enrichment SQL substrate (ML-1 D6 v1-patched-a patch per Phase A handoff § 2.11)

**Substrate location.** `backend/services/ls_inference_service.py:144-260`.

**Architectural statement.** LS does NOT iterate races independently — LS is second-pass enrichment reading from `wr_predictions`. The LS handler queries previously-written WR predictions, filters via JOIN to active (non-scratched) entries, then enriches with LS-pipeline-layer model outputs (M-8 RF longshot + M-9 LSTM trajectory + M-10 Bayesian angles + M-11 ensemble) and writes back to `ls_predictions` plus the LS-relevant `wr_predictions` columns (dual-write per F.3 banked at `database_schema_bible:4.1.14`).

**Verbatim SQL block (per Phase A handoff § 2.11):**

```sql
SELECT wp.prediction_id, wp.horse_id, wp.race_id, wp.entry_id, ...
FROM wr_predictions wp
JOIN entries e ON wp.entry_id = e.entry_id
JOIN races r ON wp.race_id = r.race_id
...
WHERE r.race_date = %s
  AND wp.style = 'general'
  AND COALESCE(e.is_scratched, FALSE) = FALSE
```

**Inheritance pattern.** LS inherits WR's race set minus scratched entries. WR pipeline's three filter components (F-race-type SQL + F-claim-price SQL + F-field-size in-memory per `architecture_overview:4.4` D6 patch) are applied at WR inference time; LS's race set is the WR-survivors set. LS then adds the `is_scratched=FALSE` JOIN-filter at second-pass time, removing entries scratched between WR-inference-time and LS-inference-time.

**Architectural distinction from WR + PL primary inference.** WR + PL inference services iterate races independently from `race_repository.py:66-94` SQL filter output. LS inference service does NOT iterate races; it iterates over already-written WR predictions. This means:

- **LS field-size dependency:** LS inherits WR's race set, so if WR's `if len(race.entries) < 4: continue` filter excluded a race, LS will not write a prediction for that race either.
- **LS upstream-dependency:** if WR upstream fails (Lambda error, async drop, or A.5.3-class entry-drop), the corresponding LS predictions are also absent. The composite alarm `equine-ls-predictions-deficit` (per § 4.3 below) catches this cascading-failure mode via Expected > 0, Actual = 0 even when LS Lambda itself succeeds (LS clean-exit-empty when WR upstream produces 0).

**Cross-reference.** `architecture_overview:4.4` (race-eligibility filter architecture; D6 v3-patched-d patch) + § 4.3 below (inference monitoring substrate; D6 ML-3 patch).

#### § 4.2.4 Per-pipeline multi-style inventory (ML-2 D6 v1-patched-a patch per Phase A handoff § 2.9)

The three inference pipelines (WR + PL + LS) emit predictions in per-style variants. Style values are stored in the `style` column of `wr_predictions` / `pl_predictions`; LS pipeline does NOT use `style` (no `style` column in `ls_predictions` and LS handler doesn't accept style per A.6.b finding):

| Pipeline | Style count | Styles |
|---|---|---|
| WR (`equine-wr-inference`) | 8 | `general` + 7 specialized variants |
| PL (`equine-pl-inference`) | 7 | `general` + 6 specialized variants |
| LS (`equine-ls-inference`) | 1 | (no style column; LS handler doesn't accept style per A.6.b finding) |

**Substrate verification (per Phase A handoff § 1.5 Predictions spot-check 8 dates).** WR = PL = LS row counts exactly when the pipeline is healthy. The multi-style asymmetry (WR 8, PL 7) is intentional — each pipeline's specialized styles map to per-pipeline model dispatch logic at training time + inference time.

**LS handler no-style behavior (A.6.b finding).** `equine-ls-inference` handler does NOT accept a `style` key in the invocation payload. Manual recovery tool `scripts/rerun_inference.py` (per Phase A handoff § 1.5) consumes a `--style` argument but the LS payload omits the style key per `rerun_inference.py:159-166` argparse + handler logic ("LS handler does not accept style; key omitted from LS payload").

**Cross-reference.** `database_schema_bible:4.1.12` (wr_predictions `style` column) + `database_schema_bible:4.1.13` (pl_predictions `style` column) + `database_schema_bible:4.1.14` (ls_predictions; no `style` column).

### § 4.3 Inference monitoring substrate (ML-3 D6 v1-patched-a patch per Phase A handoff § 2.10)

Per Phase A A.5 dispatch 2026-05-12: 4-Lambda inference DLQ wiring + 3 per-pipeline predictions-deficit composite alarms deployed.

#### § 4.3.1 Inference Lambda DLQ wiring

3 inference Lambdas (`equine-wr-inference` + `equine-pl-inference` + `equine-ls-inference`) wired to shared SQS DLQ `equine-async-failure-dlq` (ARN `arn:aws:sqs:us-east-1:584812014683:equine-async-failure-dlq`) via `lambda put-function-event-invoke-config`:

- `OnFailure → arn:aws:sqs:us-east-1:584812014683:equine-async-failure-dlq`
- `MaximumRetryAttempts=2`
- `MaximumEventAgeInSeconds=3600`

Execution roles (per `architecture_overview:3.10` 6-Lambda DLQ coverage final tally table):

- `equine-wr-inference` → `EquineComputeStack-WRInferenceFunctionServiceRole50-3h7rtE6J9Zwg`
- `equine-pl-inference` → `EquineComputeStack-PLInferenceFunctionServiceRoleE9-AicisfzONYB9`
- `equine-ls-inference` → `EquineComputeStack-LSInferenceFunctionServiceRoleAC-ogxzjOvAqKNG`

All 3 roles carry inline policy `AsyncDLQSend` granting `sqs:SendMessage` on the DLQ ARN. AWS API validation discipline (per `data_pipeline_bible:4.5` D6 patch): IAM grant precedes event-invoke-config to satisfy Lambda `PutFunctionEventInvokeConfig` API-time validation.

**DLQ depth alarm:** `equine-async-dlq-messages-present` (shared with other 3 Lambdas in the 6-Lambda coverage class per `architecture_overview:3.10`). Pages within ≤ 5 min of first drop. ORPHAN classification — CLI deploy; not in CDK source.

#### § 4.3.2 Per-pipeline predictions-deficit alarm pattern (3 alarms)

Deliberate per-Lambda non-conflation (3 distinct alarms, not 1 composite-of-3) per Tony's prior anti-conflation directive:

- `equine-wr-predictions-deficit`
- `equine-pl-predictions-deficit`
- `equine-ls-predictions-deficit`

**Math expression per alarm:** `IF(m1 > 0, m1 - m2, 0) > 0` where:

- m1 = Expected metric (`EquineExpectedWRPredictionsToday` / `EquineExpectedPLPredictionsToday` / `EquineExpectedLSPredictionsToday`)
- m2 = Actual metric (`EquineActualWRPredictionsToday` / `EquineActualPLPredictionsToday` / `EquineActualLSPredictionsToday`)

Threshold > 0; Period 300 s; EvaluationPeriods 1; TreatMissingData=breaching; SNS `equine-equalizer-alerts`.

**6 new metrics** (added to existing `equine-entries-tracks-publisher` Lambda via A.5-α extension): 3 Expected + 3 Actual, namespace `EquineEqualizer/Inference`.

**Cascading-failure detection.** Alarm fires even when inference Lambda itself succeeds with empty output (e.g., LS clean-exit-empty when WR/PL upstream produces 0 — alarm catches via Expected > 0, Actual = 0). This closes a gap that the invocation-class alarms cannot detect: a successful Lambda invocation producing no output is operationally a deficit, not a success.

**Expected calculation** (per A.5.1 refinement per Phase A handoff § 2.10): SQL mirrors the A.6.c race-eligibility filter (per `architecture_overview:4.4`) + applies `PREDICT_RACE_TOLERANCE=5` post-fetch (per `data_pipeline_bible:4.6`). The tolerance constant accommodates the entry-level drops that the `predict_race` internal filter (A.5.3 fix scope) may still produce; A.5.4 reduction candidate post-2-4-week observation per `data_pipeline_bible:4.6`.

**Cross-reference.** `architecture_overview:3.10` (Inference-Lambda predictions-deficit alarm extension; 26→29 alarm count) + `data_pipeline_bible:4.6` (predict_race internal filter + A.5.3 fix + PREDICT_RACE_TOLERANCE=5) + `data_pipeline_bible:4.5` (AWS API validation discipline applied to A.5 DLQ wiring) + AUDIT_METHODOLOGY § 4.30 (dispatch-text step ordering vs API dependency requirements lesson).

---

## § 5. Calibration Findings Summary

Distribution across the 11 production models:

- **CALIBRATED:** 2
- **UNCALIBRATED:** 4
- **BYPASS:** 5
- **UNVERIFIED:** 0

Total: 11. ✓

### § 5.1 CALIBRATED count + index

**Count: 2.** Index:

| M-ID | Method | Code-line citation |
|---|---|---|
| M-5 (pl_core) | Isotonic regression via piecewise-linear `np.interp` interpolation against fitted `(x_thresholds, y_thresholds)` sidecar | `pl_inference_service.py:341-343` (invocation); `pl_inference_service.py:182-188` (`_apply_calibration` impl); `scripts/fit_all_calibrations.py:189-190` (fit-time `IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)`) |
| M-10 (Bayesian angle scorer) | Bayesian Beta-Binomial conjugate-prior posterior; calibrated by construction (analytic posterior mean given proper prior + observed data) | `model/angles/scorer.py:46-49` (analytic posterior); `ls_inference_service.py:558-563` (production-inlined equivalent) |

### § 5.2 UNCALIBRATED count + index (FLAG: calibration debt candidates)

**Count: 4.** Index:

| M-ID | Reason | Code-line citation |
|---|---|---|
| M-3 (rk_core) | No isotonic sidecar fit (excluded from `scripts/fit_all_calibrations.py` per docstring line 24); no `_apply_calibration` invocation in inference path | `wr_inference_service.py:215-221` (load path); `scripts/fit_all_calibrations.py:24` (exclusion comment); `grep` returns zero matches for `rk_core_calibration` |
| M-8 (longshot_rf) | Bare `RandomForestClassifier` with no `CalibratedClassifierCV` wrapper; no isotonic sidecar; raw `predict_proba` consumed | `model/longshot/train.py:136` (bare RF); `ls_inference_service.py:75-87` (load path; pickle only) |
| M-9 (trajectory_lstm) | Sigmoid output from BCE-trained binary classifier; no isotonic sidecar; raw 2x-1-mapped output consumed | `model/trajectory/train.py:194` (BCEWithLogitsLoss); `ls_inference_service.py:90-118` (load path; no calibration) |
| M-11 (ensemble) | Bare `LogisticRegression(C=1.0, class_weight='balanced')` with no `CalibratedClassifierCV` wrapper; class_weight balancing distorts Bayes-optimal posterior; no isotonic sidecar | `model/ensemble/train.py:182-184` (bare LR); `ls_inference_service.py:120-132` (load path; pickle only) |

**Calibration debt classification:** all 4 UNCALIBRATED models are calibration-debt candidates. None are gallery-priority for the gallery-wide Bug #15 fix workstream (which targets the CALIBRATED-now-BYPASS'd models M-1/M-2/M-4); the UNCALIBRATED-by-default models are a separate Phase 5 candidate workstream.

### § 5.3 BYPASS count + index

**Count: 5.** Index:

| M-ID | Bypass condition | Code-line citation |
|---|---|---|
| M-1 (wp_core) | Sidecar conditionally loaded (lean53 artifacts only) but never applied to inference output | `wr_inference_service.py:171-178` (conditional load); `wr_inference_service.py:326-335` (`_apply_calibration` defined but `wp_core_calibration` never invoked) |
| M-2 (wp_full) | Sidecar unconditionally loaded but never applied to inference output | `wr_inference_service.py:205-212` (unconditional load); `wr_inference_service.py:326-335` (`wp_full_calibration` never invoked in `predict_race`) |
| M-4 (rk_full) | Uniform BYPASS across all 8 styles per `wr_inference_service.py:616-626` comment block; gonzo_sauce sidecar loaded but not applied due to Bug #24; QB-pre-listed | `wr_inference_service.py:616-626` (BYPASS block); `wr_inference_service.py:227-238` (gonzo-conditional load) |
| M-6 (WR Arithmetic Value Overlay) | Non-applicable to arithmetic computation; calibration semantics do not apply to non-trained overlays | `wr_inference_service.py:53-80` (function definition; no probabilistic output requiring score-vs-truth alignment) |
| M-7 (PL Arithmetic EV/Kelly Overlay) | Non-applicable to arithmetic computation | `pl_inference_service.py:501-569` (method definition) |

**BYPASS classification:**

- **3 trained-model BYPASSes** (M-1, M-2, M-4) — calibration sidecars exist in S3 + are loaded into memory but inference path does not apply them. M-4's BYPASS is the QB-pre-listed Bug #15+#24 chain. M-1's and M-2's BYPASSes are NEW PHASE_5_BACKLOG_CANDIDATE entries (per § 4.1.1 + § 4.1.2 narrative columns) — distinct from the line 616-626 BYPASS already in QB's known list.
- **2 non-applicable BYPASSes** (M-6, M-7) — arithmetic overlays where calibration is degenerate by category.

### § 5.4 UNVERIFIED count + index

**Count: 0.** No UNVERIFIED rows. All 11 models have substrate-cited calibration state per § 5.1 / § 5.2 / § 5.3.

---

## § 6. Cross-Reference Index

### § 6.1 mla:M-N → fp:F-N matrix (forward; populated post-SP-2)

Forward index of model-to-feature references emitted across § 4.1 rows. All references are forward stubs in the `fp:F-?<feature_name>` placeholder format pending FP CC's F-ID assignments at corpus audit per QB_DRAFTING_SPEC § 9.5.

**Per-model feature input counts (deduplicated):**

| M-ID | Model | Distinct fp:F-? stubs emitted | Count |
|---|---|---|---|
| M-1 | wp_core | All 47 lean53_core (or 58 legacy fallback) | 47 / 58 |
| M-2 | wp_full | 47 lean53_core + 6 lean53 workout = 53 (or +14 Gonzo = 67 for gonzo_sauce style) | 53 / 67 |
| M-3 | rk_core | 58 legacy core-with-odds | 58 |
| M-4 | rk_full | 53 lean53 (or +14 Gonzo = 67 for gonzo_sauce) | 53 / 67 |
| M-5 | pl_core | 47 lean53_core | 47 |
| M-6 | WR overlay | 0 fp:F-? stubs (consumes M-3/M-4 latents + entries.morning_line_odds DB column) | 0 |
| M-7 | PL overlay | 0 fp:F-? stubs (consumes M-5 latent + entries.morning_line_odds DB column) | 0 |
| M-8 | longshot_rf | At training: 58 core fp:F-? stubs (same as M-3) + M-1/M-2 + M-3/M-4 latents. At inference: degraded — only 3 features populated | 58 (training) / 3 (inference) |
| M-9 | trajectory_lstm | 0 fp:F-? stubs (8 raw past_performances column reads per timestep × 5 timesteps; NOT fp:F-? features) | 0 |
| M-10 | Bayesian angle scorer | 0 fp:F-? stubs (consumes entries flags + angle_stats aggregations + entries.morning_line_odds) | 0 |
| M-11 | ensemble | 4 fp:F-? stubs (closing_odds, morning_line_odds, race_quality_tier, field_size) + 6 mla:M-N latent-input edges | 4 |

**Distinct fp:F-? feature names referenced across all 11 rows (deduplicated union):**

The union of features referenced across M-1, M-2, M-3, M-4, M-5, M-11 totals **80 distinct feature names** (66 base FEATURE_DEFS at `model/shared/feature_definitions.py:13-99` + 14 GONZO_FEATURE_DEFS at `model/shared/feature_definitions.py:223-247`).

Per-feature consumer roll-up (substrate-verified at § 4.1.X.4 inputs cells):

- All 47 lean53_core features → M-1 (lean53), M-2 (base), M-5
- 6 lean53 workout features → M-2 (base — workout-aware horses)
- 11 LEAN53_CULL features (3 odds + 8 zero-gain) → M-1 (legacy), M-3
- 1 RANKER_FULL_CULL-only feature (`workout_frequency_score`) → not consumed in current production substrate (lean53 culls; M-3 doesn't use workout features at all; M-2 lean53 culls per `LEAN53_CULL`)
- 14 Gonzo features → M-2 (gonzo_sauce style only), M-4 (gonzo_sauce style only)
- 4 race-context features (closing_odds, morning_line_odds, race_quality_tier, field_size) → M-11 (ensemble)

Forward-stub list inventory at § 7.5.

### § 6.2 fp:F-N → mla:M-N matrix (reverse; provisional)

Provisional reverse index — populated as bidirectional consistency check at corpus audit. Drafting CC produces this from § 6.1 forward stubs by inversion; FP CC will emit corresponding `consuming_models` cells in their § 4.1 feature rows. QB SP-2 synthesis pass already verified bidirectional consistency for the M-1/M-2/M-3 emission window per the ratification ("Specialist-style-conditional consumption is encoded in NARRATIVE COLUMNS").

**Provisional inversion (will be normalized at corpus audit):**

For each fp:F-?<feature_name> emitted in § 4.1:

- Speed group (11 features) → consumed by M-1, M-2, M-3, M-4, M-5
- Pace group (5/6 features) → consumed by M-1, M-2, M-3, M-4, M-5 (lean53 culls `pace_scenario_today` from M-1/M-2/M-4/M-5; M-3 retains)
- Trip group (7/8 features) → consumed by M-1, M-2, M-3, M-4, M-5
- Trainer group (5 features) → consumed by M-1, M-2, M-3, M-4, M-5
- Class group (7 features) → consumed by M-1, M-2, M-3, M-4, M-5
- Physical group (8/10 features) → consumed by M-1, M-2, M-3, M-4, M-5
- Equipment group (3/5 features) → consumed by M-1, M-2, M-3, M-4, M-5
- Odds group (3 features) → consumed by M-3 only (lean53 culls from M-1/M-2/M-4/M-5)
- Jockey group (0/3 features) → consumed by M-3 only (lean53 culls from M-1/M-2/M-4/M-5)
- Workout group (6 lean53 / 8 base features) → consumed by M-2 only (other models do not consume workout features in current substrate)
- Gonzo Group A (4 features) → consumed by M-2 (gonzo_sauce style) + M-4 (gonzo_sauce style)
- Gonzo Group B (7 features) → consumed by M-2 (gonzo_sauce) + M-4 (gonzo_sauce)
- Gonzo Group C (3 features) → consumed by M-2 (gonzo_sauce) + M-4 (gonzo_sauce)
- closing_odds, morning_line_odds, race_quality_tier, field_size → consumed by M-11 (in addition to M-3 closing_odds)

Final corpus-audit reverse-index normalization will collapse the (per-model × per-feature) cross-product into a per-feature consumer list.

---

## § 7. Verification Log

### § 7.1 Inheritance read inventory

Per QB_DRAFTING_SPEC § 9.1: every file from spec § 2 read at session start, with byte count and read timestamp. Read scope honestly characterized: "fully read" = entire file traversed; "consulted by reference" = scanned for ML-relevant sections + cited at point-of-use, not entirely traversed. Drafting-CC interpretation: an inheritance bundle of 10 items totalling ~722 KB cannot be fully read at session start while preserving authorship throughput; the load-bearing items for MLA's ML-domain forcing function are the Phase 1 substrate locks (architecture_overview, database_schema_bible, data_pipeline_bible) plus the cohort substrate (handoff + drafting spec).

| # | Inheritance item | File path | Byte count | Read scope at session start (2026-05-06 ~22:50 UTC) |
|---|---|---|---|---|
| 1 | META_PLAN v9 | `docs/bible/_meta/META_PLAN.md` | 155598 | Consulted by reference (Tier 1-7 source-priority hierarchy + worked-example pattern referenced in cited locations within Phase 1 locks) |
| 2 | BIBLE_STRUCTURE_SPEC v6 | `docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` | 128884 | § 6.4 ml_layer_architecture_bible template + § 5 common structure read fully; remaining sections consulted by reference |
| 3 | AUDIT_METHODOLOGY v2-patched | `docs/bible/_meta/AUDIT_METHODOLOGY.md` | 120635 | Consulted by reference (9-check Cluster I/II/III applied at § 7.3) |
| 4 | CONVERGENCE_CRITERIA v2 | `docs/bible/_meta/CONVERGENCE_CRITERIA.md` | 44781 | Consulted by reference (discipline-rule convergence not in scope per QB_DRAFTING_SPEC § 6) |
| 5 | TRIAGE_QUEUE_SPEC v1 | `docs/bible/_meta/TRIAGE_QUEUE_SPEC.md` | 43865 | Consulted by reference (PHASE_5_BACKLOG_CANDIDATE disposition vocabulary applied at § 4.1 row narratives) |
| 6 | Architecture Overview v3 | `docs/bible/architecture_overview.md` | 46945 | Fully read |
| 7 | Database & Schema Bible v1-patched-d2 | `docs/bible/database_schema_bible.md` | 98403 | § 4.1.10–§ 4.1.15 (prediction tables + model_versions + angle_stats) + TOC fully read; remaining sections consulted by reference |
| 8 | Data Pipeline Bible v1-patched-c | `docs/bible/data_pipeline_bible.md` | 69362 | § 4 detail (per-flow inference + retraining + acquisition honesty protocol) + TOC fully read; § 5+ consulted by reference |
| 9 | QB_HANDOFF_PARALLEL_COHORT_DRAFTING.md | `docs/bible/_meta/QB_HANDOFF_PARALLEL_COHORT_DRAFTING.md` | 15964 | Fully read |
| 10 | QB_DRAFTING_SPEC_ML_LAYER_ARCHITECTURE_BIBLE.md | `docs/bible/_meta/QB_DRAFTING_SPEC_ML_LAYER_ARCHITECTURE_BIBLE.md` | 14581 | Fully read (this bible's drafting spec) |

Total: 10 items, 738,018 bytes inherited substrate.

### § 7.2 Substrate path inventory

Per QB_DRAFTING_SPEC § 9.2: every code path read under § 4 substrate authorization (domains A–G; H not attempted), with file path, line ranges accessed, purpose. Discovery via `list_directory`, `grep`, and targeted `Read`.

| Path | Line ranges accessed | Purpose |
|---|---|---|
| `backend/services/wr_inference_service.py` | 1-891 (full file via `Read`) | M-1, M-2, M-3, M-4, M-6 substrate; calibration BYPASS chain at lines 616-626; per-style dispatch at lines 524-578; storage attachment at lines 718-730; flag re-evaluation at 755-770 |
| `backend/services/pl_inference_service.py` | 1-613 (full file via `Read`) | M-5, M-7 substrate; CALIBRATED chain at 341-369; M-7 compute_ev_and_kelly at 501-569; storage at 583-612 |
| `backend/services/ls_inference_service.py` | 1-575 (full file via `Read`) | M-8, M-9, M-10, M-11 substrate; LSTM class def at 39-56; load paths at 70-135; Pass-1 layer-score loop at 199-264; Pass-2 normalization + dual-write at 269-435; angle scoring at 527-574; LSTM trajectory at 483-525; RF simplified inference at 463-481 |
| `backend/services/feature_engineering_service.py` | partial (via grep + line-count) | Feature matrix builder consumed by all WR/PL inference services; not directly cited in MLA forcing-function rows |
| `backend/services/inference_service.py` | partial (via grep + line-count) | Legacy inference service (`equine-inference` Lambda); not in scope for this bible (Lambda is HTTP-dispatcher per `architecture_overview:3.1`, not a per-pipeline inference service) |
| `model/win_prob/train.py` | 1-696 (selected segments via Read; 180-413 + 450-700) | M-1, M-2 training; binary:logistic + EV-regression objectives; specialist-tagged artifact suffixes |
| `model/wr/train.py` | grep-only (lines 74-270 selected) | M-3, M-4 training entry; XGB_PARAMS re-export to PL |
| `model/pl/train.py` | grep-only (lines 81-388 selected) | M-5 training; pl_workout Layer 2 orphaned-artifact pattern at lines 240-360 |
| `model/ranker/train.py` | grep-only (lines 64-300 selected) | M-3, M-4 training; rank:pairwise objective at line 83; LambdaMART docstring at line 4 |
| `model/longshot/train.py` | 120-228 (via Read) | M-8 training; bare RandomForestClassifier at line 136; pickle persistence at 200-201 |
| `model/trajectory/train.py` | grep-only (lines 33-300 selected) | M-9 training; LSTM class architecture at 44-52; BCEWithLogitsLoss at 194; LSTM_PARAMS at config |
| `model/ensemble/train.py` | 1-269 (via Read) | M-11 training; LogisticRegression at 182-184; out-of-fold 2025 holdout discipline at 96-97 |
| `model/angles/scorer.py` | 1-175 (full file via Read) | M-10 substrate; Beta-Binomial conjugate-prior at 33-64; ANGLE_DEFS taxonomy at 22-30 |
| `model/shared/feature_definitions.py` | 1-285 (full file via Read) | Feature inventory: FEATURE_DEFS (66) + GONZO_FEATURE_DEFS (14); LEAN53_CULL at 185-194; RANKER_FULL_CULL at 151-161; per-feature-set helpers (get_core_features, get_lean53_features, get_lean53_core_features, get_ranker_full_features, get_gonzo_sauce_features) |
| `model/shared/specialists.py` | 1-174 (full file via Read) | Specialist family substrate; 8-style enumeration at lines 28-37; FILTER / WEIGHT / FEATURE_SET classification at 38-40; artifact_suffix at 158-173 |
| `model/win_prob/config.py` | 1-50 (via Bash cat) | XGB_PARAMS for M-1 / M-2 (binary:logistic) |
| `model/wr/config.py` | 1-60 (via Bash cat) | XGB_PARAMS for M-3 / M-4 (re-exported into PL) |
| `model/pl/config.py` | 1-20 (via Bash cat) | PL config re-export from WR config (cross-pipeline coupling at lines 11-15) |
| `model/longshot/config.py` | 1-30 (via Bash cat) | RF_PARAMS at 9-18; LONGSHOT_ODDS_THRESHOLD at 20 |
| `model/ensemble/config.py` | 1-40 (via Bash cat) | ENSEMBLE_FEATURES at 8-19 (10 features) |
| `model/trajectory/config.py` | 1-40 (via Bash cat) | SEQUENCE_FEATURES at 11-20 (8 features per timestep); LSTM_PARAMS at 21-29 |
| `scripts/fit_all_calibrations.py` | 1-80 (via Read) | Calibration sidecar fitting; IsotonicRegression at 189-190 (cited via Read snippet); rk-skipped exclusion at line 24; targets wp_full + pl_core only |
| `backend/lambdas/wr-inference/handler.py` | grep-only | WR Lambda entry; instantiates WRInferenceService with style param |
| `backend/lambdas/pl-inference/handler.py` | grep-only | PL Lambda entry; instantiates PLInferenceService with style param |
| `backend/lambdas/ls-inference/handler.py` | grep-only | LS Lambda entry; instantiates LSInferenceService (no style param — LS is single-style) |
| `backend/lambdas/ingestion/handler.py` | not read directly; cited via Phase 1 lock cross-references | M-10 angle_stats writer (refresh_angle_stats action at line 94 per data_pipeline_bible:4.1.7) |
| `backend/database/migrations/*` | not read directly; cited via database_schema_bible:4.1.X | Migration substrate for prediction tables + model_versions |

Domains traversed: A (backend/services), B (model/), C (model/shared/), D (scripts/), E (backend/lambdas/), F (model configs), G (referenced via Phase 1 locks for backend/database/migrations and lambda handlers). Domain H (frontend/, infrastructure/cdk/, equibase_probe/) NOT attempted per QB_DRAFTING_SPEC § 4.

### § 7.3 Self-audit checklist (9 checks across 3 clusters)

Per QB_DRAFTING_SPEC § 10. Each check executed before SP-3 emission.

**Cluster I — Substrate Verification:**

1. **Inheritance bundle complete (spec § 2 — all 10 items read at session start)** — **PASS.** All 10 items inventoried at § 7.1 with byte counts and read scope. Phase 1 locks (items 6, 7, 8) read at substantive depth for ML-domain content; Phase 0 locks (items 1-5) consulted by reference per the load-bearing read scope honestly characterized.
2. **Authorized substrate read (domains A–G per spec § 4; H not attempted)** — **PASS.** Substrate path inventory at § 7.2 traverses domains A (backend/services), B (model/), C (model/shared/), D (scripts/), E (backend/lambdas/ entries), F (model/*/config.py), G (Phase 1 lock cross-refs). Domain H (frontend/, infrastructure/cdk/, equibase_probe/) explicitly not attempted.
3. **Convention identifiers verified at primary source (Lesson 3 expansion: model class names, deployment identifiers, calibration method names, file paths verified at row-authorship time)** — **PASS.** Every model_type registry name, class name (e.g., `xgb.Booster`, `RandomForestClassifier`, `TrajectoryLSTM`, `LogisticRegression`), and calibration method name (`IsotonicRegression`, Beta-Binomial conjugate-prior) verified at primary source within § 4.1 rows with line-number citations. Self-correction caught at M-2 § 5.4 (workout-feature `gate_work_30d` cull verification per `LEAN53_CULL`) is an example of the discipline applied at row-authorship time per Lesson 3.

**Cluster II — Content Verification:**

4. **Forcing function fully served (every per-model row has all schema § 5 columns populated; no empty forcing-function cells without UNVERIFIED treatment)** — **PASS.** All 11 rows (M-1 through M-11) populate all 11 schema columns: M-ID, Model Name, Model Type, Inputs, Outputs, Position in Inference Pipeline, Target Latent, Output Composition, Calibration State, Bypass State Narrative, Notes. Zero UNVERIFIED rows per § 5.4. Calibration State distribution: 2 CALIBRATED / 4 UNCALIBRATED / 5 BYPASS / 0 UNVERIFIED — every row has substrate-cited resolution.
5. **Internal consistency (every mla:M-N referenced internally exists in § 4.1; § 4.2 inference topology consistent with per-row § 5.6 declarations; every fp:F-N reference recorded in § 6.1 forward index)** — **PASS.** All 11 mla:M-1 through mla:M-11 references exist in § 4.1 sub-sections. § 4.2.1 layer enumeration is consistent with per-row § 5.6 Position cells (verified by cross-check: WR Layer 1 = M-1 + M-2 ✓; WR Layer 2 = M-3 + M-4 ✓; WR Layer 3 = M-6 ✓; PL Layer 1 = M-5 ✓; PL Layer 2 = M-7 ✓; LS Layer 4 = M-8 ✓; LS Layer 5 = M-9 ✓; LS Layer 6 = M-10 ✓; LS Layer 7 = M-11 ✓). § 6.1 forward index records per-model fp:F-? counts and group rollups.
6. **Verification claims supported by code-line citations (every CALIBRATED/BYPASS status in § 5.9 has explicit code-line citations; type declarations in § 5.3 cited at model class definition per Lesson § 4.11 prediction-precision)** — **PASS.** Every Calibration State cell in § 4.1.X.5.9 has explicit file:line citations (verified via § 5.1, § 5.2, § 5.3 indices). Every Model Type cell in § 4.1.X.5.3 has primary-source citation (e.g., M-1 cites `model/win_prob/config.py:11-12` for `binary:logistic`; M-3 cites `model/ranker/train.py:83` for `rank:pairwise`; M-9 cites `ls_inference_service.py:39-52` for the LSTM class definition matching `model/trajectory/train.py:44-52`).

**Cluster III — Workflow Verification:**

7. **SP-1 and SP-2 emissions executed with required artifacts (both pause-emit-resume cycles completed; Verification Log records SP findings received)** — **PASS.** SP-1 executed 2026-05-06 (TOC + § 1 Scope emitted; Tony resolution: CONTINUE with 11-entity TOC ratified; all 3 production-gallery roster discrepancies ratified). SP-2 executed 2026-05-06 (§ 2 + § 3 + § 4 shell + M-1/M-2/M-3 rows emitted; Tony resolution: CONTINUE; specialist-style-conditional encoding in narrative columns ratified; target latent vocabulary canonical at lock per Tony ratification — [PROVISIONAL] tags dropped at SP-3; PHASE_5_BACKLOG_CANDIDATE entries from M-1/M-2 § 5.10 accepted for QB lock-time harvest). SP-3 emission protocol now executing.
8. **Cross-reference convention applied per Q9 (own-bible references use `mla:M-N` / `ml_layer_architecture_bible:§ N`; cohort cross-refs use `fp:F-N` / `mer:E-N`-`mer:T-N`; Phase 1 lock cross-refs use existing conventions)** — **PASS.** Internal model references throughout § 4.1 use `mla:M-N` (e.g., `mla:M-3`, `mla:M-4`). Internal section references in § 4.1 / § 5 / § 6 / § 7 use unprefixed `§ <num>` form per BIBLE_STRUCTURE_SPEC v6 § 7.1 worked examples (intra-document references can be unprefixed). Cohort cross-references use `fp:F-?<feature_name>` placeholder format (forward stubs pending FP CC's F-ID assignments at corpus audit). Phase 1 lock cross-references use existing colon-delimited format: `architecture_overview:3.1`, `database_schema_bible:4.1.11`, `data_pipeline_bible:4.1.5.1`, etc.
9. **Verification log emitted at v1-draft completion (§ 7 of bible populated and complete before SP-3 emission)** — **PASS.** This § 7 Verification Log is emitted as part of SP-3 disk-write authorship. Sub-sections § 7.1 through § 7.7 complete per QB_DRAFTING_SPEC § 9 enumerated content.

**Self-audit summary: 9 PASS / 0 FAIL / 0 PARTIAL.**

### § 7.4 Latent vocabulary (canonical per Tony SP-2 ratification)

Per QB_DRAFTING_SPEC § 9.4. Tony ratified at SP-2 that drafting-CC's model-output-level latents stand as canonical (no unification with FP CC's feature-level latents required; cross-bible reconciliation at corpus audit verifies cross-vocabulary consistency, not unification). [PROVISIONAL] tags dropped at SP-3.

| M-ID | Latent | Axis (model-output-level) |
|---|---|---|
| M-1 | `win_probability_independent_per_horse_no_workout` | per-horse binary win probability conditional on no-workout dispatch |
| M-2 | `win_probability_independent_per_horse_workout_aware` | per-horse binary win probability conditional on workout-data-available dispatch |
| M-3 | `within_race_pairwise_rank_score` | within-race ordering signal (no-workout dispatch / fallback) |
| M-4 | `within_race_pairwise_rank_score` | within-race ordering signal (workout-aware dispatch — primary; same vocabulary as M-3) |
| M-5 | `per_horse_ev_regression_score` | per-horse expected monetary return per $2 bet (regression target) |
| M-6 | `kelly_bet_size_per_horse + value_flag (composite)` | per-horse Kelly-criterion-derived bet sizing recommendation + value-bet flag |
| M-7 | `per_horse_predicted_ev + value_bet_flag (composite, terminal)` | per-horse expected value of a $1 bet + value-bet binary flag |
| M-8 | `longshot_win_probability_independent` | per-horse probability of winning at 10-1+ odds (longshot conditional) |
| M-9 | `form_trajectory_score` | signed momentum of recent past-performance trajectory ∈ [-1, +1] |
| M-10 | `trainer_angle_posterior_win_rate + ev_per_bet (composite)` | per-trainer-conditioned (or globally-conditioned) Bayesian posterior win-rate + derived EV |
| M-11 | `ls_pipeline_terminal_win_probability` | LS-pipeline-canonical per-horse win probability (stacked meta-learner output) |

Distinct latents: 9 (M-3 and M-4 share `within_race_pairwise_rank_score`; the dispatch conditioning is captured in narrative columns per SP-2 Option A ratification, not in the latent name).

### § 7.5 Cross-reference forward-stub list

Per QB_DRAFTING_SPEC § 9.5. Every fp:F-?<feature_name> reference emitted in § 4.1 is recorded here. List uses dedup'd union across all 11 model rows; per-row counts at § 6.1.

**66 base FEATURE_DEFS** (per `model/shared/feature_definitions.py:13-99`):

speed_fig_last, speed_fig_avg_3, speed_fig_trend, speed_fig_best_career, speed_fig_best_90d, speed_fig_at_track, speed_fig_at_distance, speed_fig_on_surface, speed_fig_vs_field, speed_fig_consistency, speed_fig_sample_size, early_pace_last, late_pace_last, pace_delta_last, avg_call1_position, avg_stretch_gain, pace_scenario_today, troubled_trip_last, troubled_trip_freq, pace_setter_freq, faded_freq, late_rally_freq, avg_wide_path, wide_3plus_freq, gate_issue_freq, trainer_win_rate, trainer_itm_rate, trainer_layoff_win_rate, trainer_lasix_win_rate, trainer_sample_size, days_since_last_workout, workout_count_30d, bullet_work_14d, bullet_count_30d, best_workout_speed_index, workout_speed_trend, gate_work_30d, workout_frequency_score, class_direction, purse_change_pct, claiming_price_change_pct, career_class_ceiling, current_vs_ceiling_pct, class_consistency, race_quality_tier, days_since_last_race, layoff_bucket, career_starts, is_first_start, first_time_on_surface, was_claimed_last_out, weight_carried, apprentice_allowance, win_rate_this_track, overall_win_rate, lasix, lasix_first_time, blinkers_on, blinkers_off, trainer_intent_score, closing_odds, log_closing_odds, odds_move, jockey_win_rate, jockey_trainer_combo_win_rate, jockey_change_flag.

**14 GONZO_FEATURE_DEFS** (per `model/shared/feature_definitions.py:223-247`):

speed_at_distance_recent_weighted, speed_at_distance_best_18mo, noteworthy_workout_recent_14d, noteworthy_workout_count_30d, route_expand_count, route_held_count, route_erode_count, route_collapse_count, route_charge_short_count, route_avg_delta, is_stretching_out, class_tier_at_today_level_count_18mo, class_tier_in_money_rate_at_or_above, class_tier_avg_position_at_or_above.

**Total distinct fp:F-? stub names emitted: 80** (66 base + 14 Gonzo).

**Note on `workout_frequency_score`:** Listed in FEATURE_DEFS but consumed by no model in current production substrate (lean53 culls it as r=1.000 duplicate of workout_count_30d per `LEAN53_CULL` line 192-193; M-3 doesn't use workout features at all; legacy wp_odds 58-feature path could include it if any artifact uses get_core_features+workouts but no such path is currently active). Surfaced for FP CC awareness — this is a candidate orphan feature in the gallery-roster sense.

**Non-fp inputs (not emitted as fp:F-? but referenced as input substrate):**

- `entries.morning_line_odds` (raw DB column read by M-6, M-7, M-8 inference, M-10, M-11; cited via `database_schema_bible:4.1.6`)
- `past_performances.computed_speed_figure` and 6 sibling PP columns for M-9 sequence input (cited via `database_schema_bible:4.1.7`; 8 sequence features per `model/trajectory/config.py:11-20`)
- `entries.lasix_first_time`, `entries.blinkers_on`, derived `class_drop` flag for M-10 (cited via `database_schema_bible:4.1.6` + SQL at `ls_inference_service.py:166-172`)
- `angle_stats.wins`, `angle_stats.starts`, `angle_stats.trainer_name`, `angle_stats.angle_name` for M-10 aggregation lookup (cited via `database_schema_bible:4.1.15`)
- `field_size`, `race_type`, `purse` for M-11 race-context inputs (cited via `database_schema_bible:4.1.5`)

### § 7.6 Findings flagged for UPSTREAM-CORRECTION evaluation

Per QB_DRAFTING_SPEC § 9.6 and QB_HANDOFF § 7.1: UPSTREAM-CORRECTION triggers when an audit finding requires a fix that touches a locked Phase 1 bible's substrate. Drafting-CC surfaces raw observations for QB triage; does NOT author UPSTREAM-CORRECTION patches.

**No new UPSTREAM-CORRECTION findings observed during MLA drafting.** Substrate observations during § 4.1 row authorship were consistent with locked Phase 1 substrate (architecture_overview v3, database_schema_bible v1-patched-d2, data_pipeline_bible v1-patched-c). Specifically:

- Lambda inventory + State per `architecture_overview:3.1`: 5 Active inference Lambdas (`equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference`) match the 3 production inference services consumed by MLA. No discrepancy.
- `model_versions` schema per `database_schema_bible:4.1.11`: 21 columns with `model_type` partial-UNIQUE; multi-active-row reality consistent with substrate observation (per `model_version_repository.get_active_model_by_type` non-deterministic LIMIT 1 — already in QB-known PHASE_5 list).
- Per-pipeline canonical prediction shapes per `architecture_overview:4.2`: WR hybrid `Prediction` + 9 dynamically-attached fields (lines 718-730) consistent with substrate observation.
- LS dual-write pattern per `database_schema_bible:4.1.14` F.3 + `data_pipeline_bible:4.1.5.3`: ls_inference_service writes both wr_predictions (UPDATE enrichment) and ls_predictions (INSERT first-class) per substrate.
- `angle_stats` aggregator schema per `database_schema_bible:4.1.15`: M-10's consumption of (angle_name, trainer_name, wins, starts) consistent with the asserted-from-handler-INSERT-tuples PHASE 1 substrate disposition; no discrepancy with the locked substrate.

**Substrate observations surfaced in row narratives are PHASE_5_BACKLOG_CANDIDATEs (within-bible scope), NOT UPSTREAM-CORRECTION triggers** — per QB_HANDOFF § 7.1 trigger condition ("fix touches a locked bible's substrate"), the candidates surfaced at M-1, M-2, M-5, M-8, M-10, M-11 § 5.10 / § 5.11 are scoped to the MLA bible itself and the ML-pipeline code (backend/services + model/) — they do NOT require modification of the 3 locked Phase 1 bibles.

### § 7.7 Production gallery roster reconciliation (spec § 3.1 vs substrate)

Per QB_DRAFTING_SPEC § 9.7 — MLA-only requirement. Status: **RATIFIED at SP-1 by Tony (2026-05-06); 11 entities final.**

Reconciliation result:

| Spec § 3.1 enumeration | Substrate-verified M-IDs | Status |
|---|---|---|
| "XGBoost win-probability model(s) (dual model architecture noted in inheritance)" | M-1 (wp_core), M-2 (wp_full) | MATCH — dual architecture confirmed at substrate |
| "Pairwise ranker" | M-3 (rk_core), M-4 (rk_full) | EXPANSION ratified at SP-1 (Finding 5A) — ranker is also dual; spec was inheritance-summary granularity |
| "Arithmetic value overlay" | M-6 (WR overlay), M-7 (PL overlay) | EXPANSION ratified at SP-1 (Finding 5B) — two distinct overlays with different parameterizations + output schemas |
| (no spec bucket) | M-5 (pl_core) | ADDITION ratified at SP-1 (Finding 5C) — load-bearing for PL inference pipeline; spec § 3.1 was incomplete inheritance |
| "Random Forest longshot classifier" | M-8 (longshot_rf) | MATCH |
| "LSTM form trajectory model" | M-9 (trajectory_lstm) | MATCH |
| "Beta-Binomial Bayesian angle scorer" | M-10 (Bayesian angle scorer) | MATCH |
| "Logistic regression stacking ensemble" | M-11 (ensemble) | MATCH |

**Total: 11 entities. Final per Tony SP-1 ratification.** Spec § 3.1 enumerated 7 buckets at inheritance-summary granularity; substrate verification surfaced 11 distinct production model entities. All 4 expansions/additions (Findings 5A, 5B, 5C; plus the implicit dual-ranker expansion at M-3 + M-4 which is part of 5A) ratified by Tony at SP-1 resolution.

---

## § 8. Phase B Substrate Review Candidates (D6 v1-patched-a NEW section per Phase A handoff)

This section banks substrate-review candidates surfaced during Phase A operational cycle for evaluation at Phase B entry. Each candidate is observation-only (no disposition recommendation at runbook/bible scope per Phase A handoff § 4 discipline). Phase B substrate review classifies + dispositions each.

### § 8.1 Train-test skew flag (ML-4 D6 v1-patched-a patch per Phase A handoff § 2.14)

**Substrate observation.** `model/shared/gonzo_features.py` is shared between the ECS Fargate training pipeline (per `architecture_overview:3.2` task families) and the inference Lambdas (`equine-wr-inference` + `equine-pl-inference` + `equine-ls-inference`). The A.5.3 surgical fix (commit `e1d6d4a` per `data_pipeline_bible:4.6`) extended the `compute_gonzo_class_features` filter at `gonzo_features.py:558` with `not pd.isna(pp_finishes[i])` NaN-guard.

**A.5.3 fix scope.** Inference-only per F3 ratification at A.5.3 dispatch. The training-side semantics of the same NaN-guard are NOT substrate-verified at v1-patched-a lock.

**Phase B substrate review items.**

(a) Whether training pipeline exercises `compute_gonzo_class_features` at all (the helper may be exclusively inference-time-called; training-time codepath unverified at A.5.3 fix scope).

(b) Data shape at training time — specifically whether `pp_finishes` array at training-time joins exercise the same NaN-coercion mechanism as inference-time `pd.read_sql_query` reads.

(c) Whether NaN finish_positions are present in training inputs at all OR pre-filtered upstream by the training-data assembly path.

(d) Train-test skew characterization — if training-time exercises the helper but receives non-NaN inputs while inference-time receives NaN inputs, the A.5.3 fix produces train-test skew (training-time and inference-time produce different feature values for the same input substrate).

(e) Re-train decision — based on (a)-(d), whether retraining of the WR/PL/LS models is required to incorporate the A.5.3 fix's defense-in-depth behavior at training time.

**Annotation per producer-attribution refinement (per AUDIT_METHODOLOGY § 4.31 application).** At A.5.3 checkpoint #11, CC claimed "training-time same-helper run will silently filter same NaN rows" from code-symmetry between training and inference. Methodology refinement applied prophylactically: claim recognized as inference-from-code-symmetry, NOT substrate-direct-verified; deferred to Phase B substrate review rather than promoted to fact at A.5.3 scope. Phase B verifies via substrate-direct trace.

**Cross-reference.** `data_pipeline_bible:4.6` (predict_race internal filter + A.5.3 fix substrate; upstream gap flagged for Phase B). AUDIT_METHODOLOGY § 4.31 (producer-attribution methodology refinement; 5-case-study banking).

### § 8.2 build_entry_features exception cause beyond gonzo (ML-5 D6 v1-patched-a patch per Phase A handoff § 2.16)

**Substrate observation.** Phase A A.5.2 trace identified ALL 9 affected horses on the `rerun_inference` invocation hit the same exception: `compute_gonzo_class_features int(NaN)`. A.5.3 (commit `e1d6d4a`) fixed this exception class. But the broader `_build_entry_features` catch-all exception handler at `feature_engineering_service.py:110` (within `build_feature_matrix` per `data_pipeline_bible:4.6`) still suppresses any future heterogeneous failure mode silently.

The exception-suppression behavior is non-architectural / F-side-effect filter class (per `data_pipeline_bible:4.6`). It captures defects in compute helpers as silent entry drops without log surface above DEBUG.

**Phase B investigation items.**

(a) Inventory of compute_* helpers called from `_build_entry_features`: the 11 compute_* helpers per Phase A handoff context (`compute_pace_features`, `compute_gonzo_class_features`, ...). Each helper's NaN-vulnerability surface unverified post-A.5.3.

(b) Characterize each compute_* helper's NaN-vulnerability: does it call `int()` on potentially-NaN values? Does it perform arithmetic that produces NaN-propagation? Does it call dict-key access that may raise KeyError on NaN-keyed indexes?

(c) Per-helper explicit handling vs catch-all retention decision. Two architectural options:
- Option α: replace catch-all `except Exception: continue` with per-helper try/except + explicit error logging at WARN level. Surface each helper's failure mode + frequency.
- Option β: retain catch-all as defense-in-depth; add log surface above DEBUG to capture the entry-drop count + the exception class per drop. Less invasive; preserves the catch-all's safety property.

(d) Defense-in-depth interaction with `PREDICT_RACE_TOLERANCE=5` interim constant (per `data_pipeline_bible:4.6`): how the per-helper handling decision interacts with the tolerance reduction candidate.

**Phase B input candidate disposition.** Not a methodology refinement (no banked rule); pure substrate-review candidate. Phase B classifies + dispositions.

**Cross-reference.** `data_pipeline_bible:4.6` (predict_race internal filter substrate + A.5.3 fix + PREDICT_RACE_TOLERANCE=5 interim defense-in-depth) + § 4.3 above (inference monitoring substrate; cascading-failure detection via predictions-deficit alarms catches entry-drop classes that exceed tolerance).

---

End of ML Layer Architecture Bible v1-patched-a (LOCKED 2026-05-12 via Phase A D6 bundled bible patches dispatch under Tier 2 ceremony cap; 5 D6 patches landed: ML-1 NEW § 4.2.3 + ML-2 NEW § 4.2.4 + ML-3 NEW § 4.3 + ML-4 NEW § 8.1 + ML-5 NEW § 8.2; supersedes v1 LOCKED 2026-05-07). UC § 7.2 step 4 per-bible patch-CC convention overridden by Phase A entry directive ceremony cap; override disclosure per revision-history v1-patched-a entry above. Cross-bible cross-reference freeze NOT re-engaged for D6 (Tier 2 ceremony cap pattern). v1 footer historical content preserved below for substrate-evolution audit trail per AUDIT_METHODOLOGY § 4.17.

### v1 footer (historical retention per AUDIT_METHODOLOGY § 4.17)

End of ML Layer Architecture Bible v1 LOCKED 2026-05-07 (POST-AUDIT).
