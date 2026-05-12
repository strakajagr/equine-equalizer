# PHASE_5_BACKLOG.md

**Document:** PHASE_5_BACKLOG
**Status:** ACTIVE (Phase 5 cleanup queue; continuously updated through Phase 4 per META_PLAN v6 § 4.3)
**Created:** 2026-05-04 (Phase 0 exit prerequisite per META_PLAN v6 § 8.2)
**Format:** per TRIAGE_QUEUE_SPEC v1 (locked 2026-05-04)

**Purpose:** This file is Phase 5's deferred-work tracker. Findings from Phase 1+ audits that operator defers to Phase 5 transfer here from the active triage queue per TRIAGE_QUEUE_SPEC v1 § 4.3. Bugs surfaced before Phase 1 (e.g., Bug #28 surfaced during EE_CURRENT_STATE_DUMP generation) enter directly per the Phase 0 exit-prerequisite seed.

**Format:** entries follow TRIAGE_QUEUE_SPEC v1 § 3 (mandatory + conditional fields). The active triage queue feeds into this file via explicit transfer per § 4.3; this file's internal organization (sectioning, prioritization, scheduling) is Phase 5's concern, governed by the entry format but not by additional discipline TRIAGE_QUEUE_SPEC codifies.

**Severity taxonomy:** TRIAGE_QUEUE_SPEC v1 (HIGH / MEDIUM / LOW; Phase 0 spec, currently DRAFT pre-audit per AUDIT_METHODOLOGY v3 § 9) authoritative for ALL entries; vocabulary uniformly applied across Phase 5.3.1 through Phase 5.3.N. Phase 5.3.1 seed entry re-tagged to TRIAGE_QUEUE_SPEC v1 vocabulary 2026-05-08 per AUDIT_METHODOLOGY v3 § 8.4 ratified strategy (c.2); original META_PLAN v6 § 11 vocabulary (BLOCKER / MATERIAL / MINOR / STYLE) preserved in parenthetical annotation on Phase 5.3.1 entry per § 4.17 locked-content preservation discipline. METHODOLOGY-INTERPOLATION applies to methodology drafts only; not used in this file (operational entries).

---

## Entries

### Phase 5.3.1: HRN Scraper Bug #28 (column shift)

**Severity:** HIGH (historically: MATERIAL per META_PLAN v6 § 11 vocabulary; re-tagged 2026-05-08 per AUDIT_METHODOLOGY v3 § 8.4 ratified strategy (c.2)) (silent data loss; affects all win/DD payouts since 2026-04-30; structural failure in data acquisition layer per META_PLAN v6 § 7.9)

**Surfaced:** 2026-05-03 (during EE_CURRENT_STATE_DUMP generation; per operator memory file `equine-equalizer-bug-28-hrn-scraper.md`, the regression was sharp — 2026-04-29 last clean day at 9/10 win-payout success; 2026-04-30 onward all 0/N)

**Stable-known classification:** provisional. Backfill-feasibility AND DD-pool-extraction bounded-loss assumptions both pending Phase 1 Data Pipeline Bible audit verification (per META_PLAN v6 § 8.1).

**Root cause:** HRN page structure changed circa 2026-04-30 (likely added an icon column to the payouts table). The `parse_payout(N)` calls at `backend/services/data_sources/hrn_scraper.py:802-804` (verified) use positional cell indexing that has been off-by-one ever since.

**Manifestation:**
- `win_payout` is NULL across all results rows from 2026-04-30 onward
- `daily_double_payout` is NULL across same range
- `place_payout` stores values that should be in `win_payout`
- `show_payout` stores values that should be in `place_payout`
- Place, show, and exacta payouts still populate per operator memory file's symptom statement
- DD pool extraction at `hrn_scraper.py:814` flagged as "likely has the same root cause" — distinct code path from `daily_double_payout` result-dict field; Phase 1 verifies bounded-loss status

**Operator-verified external source:** the operator memory file `equine-equalizer-bug-28-hrn-scraper.md` contains the following verbatim passages per META_PLAN v6 verification log Claim 15c:

> "starting 2026-04-30, all results.win_payout and results.daily_double_payout rows are NULL across every track/race scraped via HRN. Place, show, and exacta payouts still populate."

> "DD pool extraction (hrn_scraper.py:814 'pool' table loop) likely has the same root cause — same site-wide column shift."

**Dependencies:**
- Resolution requires HRN page-structure verification (manual: visit a results page, confirm column structure)
- May require parser refactor if HRN structure is now variable-by-page-type
- Requires backfill of affected results rows after fix deploys (feasibility assumed; Phase 1 verifies)
- DD pool extraction status verification (Phase 1 Data Pipeline Bible audit's job)

No queue entries currently block or are blocked by Bug #28 (this is the seed entry).

**Re-classification trigger:** if Phase 1 Data Pipeline Bible audit verifies backfill is feasible AND DD pool extraction is bounded, the provisional qualifier drops at audit-lock time. If the audit verifies backfill is NOT feasible (or DD pool extraction reveals additional uncovered loss), Bug #28 re-classifies as either (a) "known but not stable" — § 8.1 exception logic could trigger if operator chooses to escalate, or (b) "stable known with permanent loss" — affected window's data unrecoverable, bible documents the data gap as permanent feature of historical record. Phase 1 audit's classification call is the lock-trigger.

**Audit-cycle reference:** N/A — Bug #28 surfaced pre-Phase-1 during EE_CURRENT_STATE_DUMP generation, not during a Phase 1+ audit cycle. Documented in META_PLAN v6 § 1.2 + § 8.1 + Appendix A.5 as the canonical seed entry for this file.

**Disposition:** Fix in Phase 5.3 before any Phase 5 work that depends on payout data.

**Rollback:** Standard git revert if fix introduces regression. No DB rollback needed (fix re-populates rows that are currently NULL).

**Bible references on resolution:**
- Update `data_pipeline_bible.md` § 7.9 (HRN scraper documentation)
- Add `data_pipeline_bible.md` § 8.W.<n> (What Was Fixed entry; canonical home per BIBLE_STRUCTURE_SPEC v3 § 5.3)
- Consider new Forbidden Pattern: positional column indexing in scrapers without column-header verification

**Status:** open
**Created:** 2026-05-04

---

<!-- Batch synthesis 2026-05-07: 23 entries surfaced across Phase 1 Cohort lock cycle (FP/MLA/MER deliverables 4-5-6). Per Tony Q18-Q21 ratifications: substrate-discovered numbering (continuing monotonically from Phase 5.3.1), Q19-A consolidated calibration discipline group (single entry referencing canonical home model_evaluation_retraining_bible:§ 5.2 + § 5.3), Q20-C three individual operational ML discipline gap entries (no composite), Q21 retroactive metadata-bundle cleanup entry. Cumulative locked-bible substrate at synthesis time: 449,120 bytes / 3,190 lines. Cross-bible cross-reference freeze ACTIVE per Handoff § 6.1. Severity vocabulary in batch entries follows TRIAGE_QUEUE_SPEC v1 § 3 per file header line 6 declaration; existing Phase 5.3.1 entry uses META_PLAN v6 § 11 vocabulary per file header line 12 — vocabulary inconsistency flagged for QB awareness, existing entry preserved verbatim. -->

### Phase 5.3.2: Calibration Discipline Candidate Group (consolidated)

**Severity:** MEDIUM  
**Disposition:** refactor  
**Cite:** model_evaluation_retraining_bible:§ 5.2 + § 5.3

**Description:** Calibration discipline candidate group — six tightly-coupled members tracked at canonical home model_evaluation_retraining_bible:§ 5.2 + § 5.3 per Q13 ratification. Members documented in canonical home (NOT enumerated here per Q19-A consolidation): (1) wp_core dead-load (mer:M-1; mla:M-1); (2) wp_full dead-load (mer:M-2; mla:M-2); (3) WR styles BYPASS at backend/services/wr_inference_service.py:616-626 (mla:M-4); (4) Post-2026-05-01 ranker-as-probability flip (architectural event; mer:M-3 + mer:M-4); (5) M-3 rk_core UNCALIBRATED + load-bearing (mer:M-3); (6) M-9 LSTM 2x-1 transform UNCALIBRATED (mer:M-9). Phase 5 scope: single coherent refactor workstream; calibration discipline canonical-home consolidation per Q13 ratification.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; Q19-A consolidation)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.3: M-8 RF Zero-Padded Inference (DIVERGENT-{TRAIN-INFERENCE})

**Severity:** HIGH  
**Disposition:** refactor  
**Cite:** ml_layer_architecture_bible:§ 5.10 + model_evaluation_retraining_bible:§ 4.1.8 + § 5.2.2

**Description:** M-8 longshot_rf RF zero-padded inference DIVERGENT-{TRAIN-INFERENCE}. Training uses 60-feature vector at model/longshot/train.py:115-140; inference at backend/services/ls_inference_service.py:463-481 zero-pads to 60-feature vector with only base-layer outputs + odds available at enrichment time. Distinct architectural class from calibration discipline group (train/inference feature-handling divergence, not calibration-sidecar invocation). Standalone HIGH severity per Q19 / Directive 4 (NOT consolidated into calibration group). Phase 5 scope: refactor inference path to align with training feature space OR refactor training to align with inference enrichment-time feature space.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; Q19 standalone)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.4: M-11 Ensemble Training/Inference Feature-Population Disparity

**Severity:** LOW  
**Disposition:** monitored  
**Cite:** ml_layer_architecture_bible:§ 5.11 + model_evaluation_retraining_bible:§ 5.2.4

**Description:** ensemble (LogReg stacking, LS Layer 7) feature-population disparity between training and inference. Training feature-population at model/ensemble/config.py ENSEMBLE_FEATURES 10-element list; inference feature-population at backend/services/ls_inference_service.py may differ in field availability or default-value handling.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.5: M-5 PL Core Re-Export of WR Config (cross-pipeline coupling)

**Severity:** LOW  
**Disposition:** monitored  
**Cite:** ml_layer_architecture_bible:§ 5.5 (M-5)

**Description:** M-5 pl_core (XGB reg:squarederror, PL Layer 1) imports XGB_PARAMS via re-export from model/pl/config.py:11-15 → model/wr/config.py:9. Cross-pipeline coupling: PL pipeline EV regression depends on WR pipeline binary classification config. Phase 5 scope: architectural review of WR/PL config coupling; consider PL standalone config.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.6: M-5 PL Core EV-Regression vs Binary-Classification Disparity

**Severity:** LOW  
**Disposition:** monitored  
**Cite:** ml_layer_architecture_bible:§ 5.5 (M-5)

**Description:** M-5 inherits XGB_PARAMS from WR config but uses reg:squarederror objective for EV regression while WR uses binary:logistic. Parameter space overlap is partial (reg-specific params not declared); inherited binary-specific params (e.g., scale_pos_weight) may be no-op for regression. Phase 5 scope: architectural review of inherited config semantics for cross-objective use.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.7: M-5 PL Bug #24 Ordering (pre-known)

**Severity:** MEDIUM  
**Disposition:** monitored  
**Cite:** ml_layer_architecture_bible:§ 5.5 (M-5) + Bug #24 catalog

**Description:** PL pipeline ordering issue per Bug #24. PRE-KNOWN; pre-existing PHASE_5_BACKLOG candidate elevated for canonical citation in cohort entries.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; pre-known elevated)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.8: M-5 pl_workout Layer 2 Orphans (pre-known)

**Severity:** LOW  
**Disposition:** kill  
**Cite:** ml_layer_architecture_bible:§ 7.5 (M-5 pl_workout)

**Description:** PL pipeline pl_workout Layer 2 orphan features. PRE-KNOWN; pre-existing PHASE_5_BACKLOG candidate elevated for canonical citation in cohort entries.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; pre-known elevated)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.9: M-10 angles/scorer.py Orphans (pre-known)

**Severity:** LOW  
**Disposition:** refactor  
**Cite:** ml_layer_architecture_bible:§ 5.10 (M-10) + model_evaluation_retraining_bible:§ 9.5 (inherited M-10 entry)

**Description:** M-10 Beta-Binomial Bayesian angle scorer at model/angles/scorer.py inline-3-angle vs canonical-7-angle disparity. PRE-KNOWN; pre-existing PHASE_5_BACKLOG candidate elevated for canonical citation in cohort entries.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; pre-known elevated)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.10: F-81 Legacy Schema Kill

**Severity:** MEDIUM  
**Disposition:** kill  
**Cite:** feature_provenance_bible:§ 4.1.81 + § 7.6 Finding 1

**Description:** F-81 ORPHAN-PRODUCTION composite covering 18+ legacy feature names from model/features/feature_definitions.py FEATURE_GROUPS schema. Sound compression per BIBLE_STRUCTURE_SPEC v6 § 5.6.1 conditional-consolidation pattern; legacy schema kill candidate at next cleanup cycle (already in cull lists; consumed by no production model in M-1..M-11 gallery).

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.11: feature_engineering_service.py Lazy-Import Drift

**Severity:** MEDIUM  
**Disposition:** refactor  
**Cite:** feature_provenance_bible:§ 4 (multiple rows reference this lazy-import region)

**Description:** backend/services/feature_engineering_service.py:128-188 lazy-import pattern for feature engineering modules. Architectural drift surface — lazy imports complicate type-safety, hot-reload, and import-graph analysis. Phase 5 scope: refactor lazy imports to module-top imports; assess hot-reload regression risk.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.12: GAP A — Drift-Based Triggers Absent (Q20-C)

**Severity:** HIGH  
**Disposition:** replace  
**Cite:** model_evaluation_retraining_bible:§ 4.2.5 GAP A + § 7.5 three-facet consolidation narrative

**Description:** Drift-based retraining triggers absent across entire Phase 1 model gallery. No drift monitor in scripts/, model/, backend/services/, or backend/lambdas/. Negative-claim verified at corpus-audit Step 7 spot-check (scripts/ inventory shows only diagnostic scripts; no drift monitor). Operational ML discipline maturity gap — Facet A. Phase 5 scope: build drift monitoring layer; integrate with retraining trigger taxonomy as new mer:T-6 (or equivalent) entity-class.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; Q20-C individual entry)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.13: GAP B — Performance-Based Triggers Absent (Q20-C)

**Severity:** MEDIUM  
**Disposition:** refactor  
**Cite:** model_evaluation_retraining_bible:§ 4.2.5 GAP B + § 7.5 three-facet consolidation narrative

**Description:** Performance-based retraining triggers absent across entire Phase 1 model gallery. No auto-gating thresholds in deployment pipeline. Negative-claim verified at corpus-audit Step 7 spot-check (grep returned only model/training/train.py:668 metrics.; no auto-promote). Operational ML discipline maturity gap — Facet B. Phase 5 scope: define auto-gating thresholds per model; integrate with deployment gating evaluation criterion.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; Q20-C individual entry)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.14: GAP C — CDK Substrate Gap (Q20-C)

**Severity:** MEDIUM  
**Disposition:** refactor  
**Cite:** model_evaluation_retraining_bible:§ 4.2.5 GAP C + § 7.5 three-facet consolidation narrative

**Description:** CDK infrastructure stack does not declare retraining cadence rules. Negative-claim verified at corpus-audit Step 7 spot-check (grep against infrastructure/cdk/lib/compute-stack.ts for "equine-daily-retrain|equine-weekly-retrain|equine-training-daily-full|equine-training-win-prob" returned 0 matches). Cadence rules currently maintained out-of-band of CDK. Operational ML discipline maturity gap — Facet C. Phase 5 scope: declare retraining cadence rules in CDK substrate; reconcile with EventBridge schedule per architecture_overview:3.6.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; Q20-C individual entry)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.15: 88-Row model_versions Registry Selection Discipline (pre-known cross-cohort)

**Severity:** MEDIUM  
**Disposition:** refactor  
**Cite:** database_schema_bible:§ 4.1.11 model_versions

**Description:** model_versions table has 88 rows with 45 active. Selection discipline gap; many INACTIVE entries with deleted artifacts.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; pre-known cross-cohort)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.16: Legacy predictions Table — 4 Readers, No Writer (pre-known cross-cohort)

**Severity:** MEDIUM  
**Disposition:** kill  
**Cite:** database_schema_bible:§ 4.1.X predictions table

**Description:** Legacy predictions table has 4 readers in production code but no writer. Deprecation candidate.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; pre-known cross-cohort)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.17: 3 INACTIVE Lambdas with Deleted ECR Images (pre-known cross-cohort)

**Severity:** LOW  
**Disposition:** kill  
**Cite:** architecture_overview:§ 3.1 Lambda inventory

**Description:** 3 Lambda functions in INACTIVE state with deleted ECR container images. Lifecycle cleanup; AWS resources holding metadata for non-functional infrastructure.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; pre-known cross-cohort)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.18: 2 Secrets Manager Entries with Zero Consumers (pre-known cross-cohort)

**Severity:** LOW  
**Disposition:** kill  
**Cite:** architecture_overview:§ 3.X Secrets Manager inventory

**Description:** 2 AWS Secrets Manager entries with zero consumers in production code. Deprecation candidate.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; pre-known cross-cohort)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.19: Duplicate-005 Migration Filenames (pre-known cross-cohort)

**Severity:** LOW  
**Disposition:** refactor  
**Cite:** database_schema_bible:§ X migration history

**Description:** Two migration files with duplicate "005" prefix. Forward discipline issue; migration ordering ambiguity.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; pre-known cross-cohort)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.20: equine-ingestion Broken Container — CodeArtifactUserFailedException (pre-known cross-cohort)

**Severity:** MEDIUM  
**Disposition:** replace  
**Cite:** architecture_overview:§ 3.1 + data_pipeline_bible:§ X.Y

**Description:** equine-ingestion Lambda container has broken CodeArtifactUserFailedException at build time. Container health gap.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; pre-known cross-cohort)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.21: architecture_overview:4.1 Line 447 Refinement (NEW from corpus audit)

**Severity:** LOW  
**Disposition:** refactor  
**Cite:** architecture_overview:§ 4.1 line 447 + feature_provenance_bible:§ 4.1.81 + § 7.6 Finding 1

**Description:** architecture_overview:4.1 line 447 "NOT orphaned" assertion is correct at module-import level (model/features/feature_definitions.py IS imported by training and inference services) but masks the orphan-feature classification at the per-feature gallery level — no production model in M-1..M-11 consumes any feature from the legacy 73-feature FEATURE_GROUPS schema. Refinement: distinguish module-import-orphan vs feature-orphan classification. Per Tony Decision 1 (DEFER) ratification, deferred from corpus-audit gate to next architecture_overview patch cycle.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; corpus-audit Decision 1 DEFER)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.22: Bug #25 Catalog Gap at F-76 (NEW from corpus audit)

**Severity:** LOW  
**Disposition:** refactor  
**Cite:** feature_engineering_service.py:1073 + feature_provenance_bible:§ 4.1.76

**Description:** F-76 (log_closing_odds) DUPLICATED narrative does not cite Bug #25 despite substrate operativity at backend/services/feature_engineering_service.py:1073 ("# FIX #25: np.log1p, not np.log"). Bug #25 cross-reference would strengthen F-76 substrate-grounding without changing classification. Bug #25 catalog gap candidate at next FP patch cycle.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; corpus-audit NEW finding)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.23: workout_frequency_score Classification Ambiguity (NEW from corpus audit)

**Severity:** LOW  
**Disposition:** monitored  
**Cite:** ml_layer_architecture_bible:§ 7.5 Note + feature_provenance_bible:§ 4.1.53 + § 4.1.81

**Description:** workout_frequency_score classification ambiguity. MLA § 7.5 flags as candidate orphan ("consumed by no model in current production substrate"); FP F-53 classifies DUPLICATED with consuming_models = [mla:M-2, mla:M-4] for legacy pre-lean53 ranker_full + win_prob_full ONLY. Substrate ambiguity requires live DB read on model_versions.is_active to determine if any legacy artifacts are currently active. Phase 5 scope: pending credential-authorized live-DB-state resolution.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; corpus-audit NEW finding)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.24: FP Footer Staleness + Drafting-CC Metadata-Bundle Retroactive Cleanup (NEW from lock cycle)

**Severity:** LOW (composite of STYLE-class FP footer + retroactive standardization)  
**Disposition:** refactor  
**Cite:** feature_provenance_bible:line 883 (stale "v1-draft (PRE-AUDIT)" footer designation post-lock); ml_layer_architecture_bible:line 1105 (cohort-uniform metadata bundle established at lock); model_evaluation_retraining_bible:line 1200 (cohort-uniform metadata bundle established at lock)

**Description:** Phase 1 cohort drafting-CC metadata-bundle inconsistency. Three patterns observed across FP/MLA/MER drafting: FP rich (revision history populated; "## End of FP v1-draft (PRE-AUDIT — Phase 1 deliverable 4 of 7)" structured footer); MLA minimal (no revision history block; "End of ML Layer Architecture Bible v1-draft." plain-text footer); MER hybrid (no revision history block; bold-leading + trailing narrative footer). Lock-CC three-element metadata bundle (header status + revision history block + end-of-document footer) authorization addressed prospective MLA/MER pattern at lock time per Tony hybrid Option B-for-MLA/MER ratification, but FP footer (locked v1-draft state designation, now stale post-AUDIT) was deferred to PHASE_5_BACKLOG per Tony Option D-for-FP ratification. This entry tracks retroactive standardization of all locked Phase 1 bibles to consistent metadata structure. AUDIT_METHODOLOGY future-cycle Lesson candidate banked separately for paste-prompt mandate (drafting-CC metadata-bundle initialization specification) — does NOT live in PHASE_5_BACKLOG. Phase 5 scope: retroactive cleanup of FP footer at next FP patch cycle, batched with any future content patches; standardize all locked Phase 1 bibles to consistent metadata structure.

**Surfaced:** 2026-05-07 (Phase 1 Cohort batch synthesis; Q21 retroactive cleanup entry)  
**Status:** open  
**Created:** 2026-05-07

---

### Phase 5.3.25: UC-2 PL Value-Bets 3-Source Mismatch (production bug)

**Severity:** HIGH  
**Disposition:** refactor  
**Cite:** api_frontend_bible:§ 10.2 + api_frontend_bible_v1_verification.md V1-16 + V1-19

**Description:** PL value-bet prediction surface non-functional in production. API Gateway route is `/pl/predictions/value`; Lambda dispatch (in `equine-pl-inference` handler) is `/pl/predictions/value-bets`; FE call (per V1-19 client.ts substrate) targets `/pl/predictions/value-bets` (no API Gateway route). FE call returns 404 because API Gateway route is `value` and FE is calling `value-bets`. User-facing PL value-bet prediction feature broken in production. Resolution alternatives: (a) rename API Gateway route from `/pl/predictions/value` to `/pl/predictions/value-bets` (align gateway with handler + FE); (b) rename Lambda dispatch from `/pl/predictions/value-bets` to `/pl/predictions/value` and rename FE call site to match (align handler + FE with gateway); (c) keep substrate as-is and document non-functional surface — operator decision at Phase 5 work cycle.

**Surfaced:** 2026-05-07 (API & Frontend Bible v1 drafting cycle V1-16 + V1-19 substrate verification; Tier 1 AWS Gateway state vs Tier 4 FE client.ts working-tree code 3-source divergence)  
**Status:** open  
**Created:** 2026-05-08

---

### Phase 5.3.26: UC-3 /wr/health + /ls/health 404 Fall-Through

**Severity:** MEDIUM  
**Disposition:** refactor  
**Cite:** api_frontend_bible:§ 10.3 + api_frontend_bible_v1_verification.md V1-15 + V1-17

**Description:** Two API Gateway routes deployed without Lambda dispatch. `/wr/health` + `/ls/health` exist as API Gateway integration targets (per V1-15 + V1-17 Tier 1 substrate); neither `equine-wr-inference` nor `equine-ls-inference` has a dispatch handler for these paths; both routes 404 fall-through. Per-pipeline health endpoint inconsistency vs `equine-inference` `/health` (which IS handled). STATUS = PRODUCTION at v1 lock per Posture A deployment-state semantic (routes deployed and reachable, even though 404). Resolution alternatives: (a) add Lambda dispatch for `/wr/health` + `/ls/health` (uniform per-pipeline health endpoint pattern matching `/health` on `equine-inference`); (b) remove API Gateway routes (clean up unreachable substrate); (c) keep substrate as-is — operator decision at Phase 5 work cycle.

**Surfaced:** 2026-05-07 (API & Frontend Bible v1 drafting cycle V1-15 + V1-17 substrate verification; Tier 1 AWS Gateway state)  
**Status:** open  
**Created:** 2026-05-08

---

### Phase 5.3.27: Audit Meta-Documents for Stale _meta/PHASE_5_BACKLOG.md Path References

**Severity:** LOW  
**Disposition:** refactor

**Description:** Audit meta-documents for stale _meta/PHASE_5_BACKLOG.md path references; correct to docs/bible/PHASE_5_BACKLOG.md.

**Surfaced:** 2026-05-08 (AUDIT_METHODOLOGY meta-cycle dispatch; Q8 ratification)  
**Status:** open  
**Created:** 2026-05-08

---
