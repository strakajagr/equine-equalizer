# CONVERGENCE_CRITERIA.md

**Document:** CONVERGENCE_CRITERIA
**Phase:** 0 (Methodology) — Phase 0 deliverable 4 of 5
**Status:** DRAFT v2 (pre-audit)
**Author:** QB (drafting under verification discipline; Tony orchestrated and reviewed)
**Date:** 2026-05-04
**Locked:** [pending audit + Tony review + iteration cycles]

**Revision history:**
- v1 (2026-05-04): initial QB draft. Tier 1 per Tony's locked Q2; no companion verification log per the tier model.
- v2 (2026-05-04): post-v1-audit surgical patch pass integrating Tony's three locked decisions (Q1 Option B addressing MATERIALs + tightly coupled MINORs; Q2 surgical fix + changelog note for recursive precision pattern with no formal codification yet; Q3 QB drafting spec error disclosure in v2 changelog). STYLE Finding 5 deferred to Phase 1 opportunistic per Tony's Q1.

**Tier:** 1 per META_PLAN v6 § 4.1 + § 6.5 (per Tony's locked Q2 in the v1 cycle: QB-drafted; abstract success criteria; no EE-specific factual claims; no companion verification log).

**Anchored on:** META_PLAN v6 (locked 2026-05-04), BIBLE_STRUCTURE_SPEC v3 (locked 2026-05-04), AUDIT_METHODOLOGY v2 (locked 2026-05-04). Section references throughout this document point to v6 / v3 / v2 § numbers.

**Methodology-interpolation rule (operative per META_PLAN v6 § 6.1, with v6's expanded scope, grandfathering clause, and pattern-completion check applied symmetrically to QB-drafted content):** This draft does not invent binary tests, cadence rules, completeness criteria, scoring rubrics, severity thresholds, iteration caps, percentage criteria, procedural sequencing rules, or other QB-prescribed methodology constructs Tony has not explicitly ratified. The provenance discriminator (QB-drafted vs Tony-ratified) governs; Tier 1 designation does not exempt QB from the rule. v1 surfacing notes in § 10.

---

## 1. Motivation

### 1.1 Why this document exists

CONVERGENCE_CRITERIA.md is the fourth Phase 0 methodology deliverable. Its job is to operationalize the Phase 1 convergence test specified in META_PLAN v6 § 3.2.1. BIBLE_STRUCTURE_SPEC v3 § 8.4 explicitly defers specific success criteria for the test to this document ("Specific success criteria deferred to CONVERGENCE_CRITERIA.md"). CONVERGENCE_CRITERIA discharges that deferral. AUDIT_METHODOLOGY v2 § 3.2 + § 7 reference the convergence test indirectly through the cross-document audit's convergence-test integration, but do not formally defer convergence-test success criteria here; the deferral is uniquely from BIBLE_STRUCTURE_SPEC v3 § 8.4.

The convergence test is the Phase 1 exit criterion that determines whether the locked Phase 1 corpus is fit for its purpose. Per META_PLAN v6 § 3.2.1, Phase 1 exists to make ML re-architecture tractable; the test verifies that the locked corpus actually does so. A bible that thoroughly documents the current code and infrastructure but does not directly support evaluate / rebuild / retrain workflows would be the wrong bible (per v6 § 3.2.1's framing rationale).

### 1.2 Why criteria must be precise

The Phase 1 corpus is produced by multiple parallel CC sessions (per BIBLE_STRUCTURE_SPEC v3 § 8.2 recommended drafting order). The convergence test is executed by a fresh CC session given the locked corpus. The test's output (a plan for evaluate / rebuild / retrain) is judged against success criteria. If the criteria are judgment-dependent in a way that two readers could apply differently, the test does not converge — different test executions return different verdicts on the same locked corpus, and the corpus's lock-readiness becomes irreproducible.

The recursive principle: CONVERGENCE_CRITERIA specifies criteria for success; its own criteria must themselves be precise enough that two independent readers reach the same verdict. The document fails its own purpose if it does not satisfy this.

### 1.3 Why now

Phase 0 deliverables 1-3 (META_PLAN v6, BIBLE_STRUCTURE_SPEC v3, AUDIT_METHODOLOGY v2) are locked. CONVERGENCE_CRITERIA is deliverable 4. After this document locks, only TRIAGE_QUEUE_SPEC.md (deliverable 5) remains before Phase 0 completes and Phase 1 drafting can begin. The convergence test specified here governs Phase 1's exit; the criteria must be in place before Phase 1 begins so that bible drafters know what their corpus must support.

---

## 2. Scope

### 2.1 What this document specifies

- **Phase 1 convergence test PASS / FAIL / PARTIAL conditions** (per META_PLAN v6 § 3.2.1's locked test framing).
- **Success criteria for the three workflows** the test exercises: evaluate, rebuild, retrain.
- **Plan production criteria** — what it means for a fresh CC session to "produce" a plan based on the locked corpus.
- **Plan-based-on-bible criteria** — what it means for the produced plan to be grounded in the locked corpus.
- **Post-test action triggers** — what happens after PASS / FAIL / PARTIAL.

### 2.2 What this document does NOT specify

- **Phase 0 audit-cycle convergence.** Already specified in META_PLAN v6 § 11 (Tony's threshold: < 5 MATERIAL ∧ zero fabricated ∧ zero methodology-interpolation findings to lock per Phase 0 audit cycle). Redundant codification creates dual sources; CONVERGENCE_CRITERIA does not restate or revise the Phase 0 threshold.
- **Phase 2 / Phase 3 / Phase 4 convergence.** Deferred to phase entry per the AUDIT_METHODOLOGY v2 § 2.2 pattern. If those phases want to inherit the convergence-test pattern from this document, they reference it as a worked example.
- **Per-bible audit threshold.** Inherited from META_PLAN v6 § 11 + AUDIT_METHODOLOGY v2 § 3.5; not revised here.
- **What bible content goes where.** Specified in BIBLE_STRUCTURE_SPEC v3.
- **How to audit.** Specified in AUDIT_METHODOLOGY v2.
- **How to format triage queue findings.** Specified in TRIAGE_QUEUE_SPEC.md (Phase 0 deliverable 5).
- **Cadence specifications (test-execution count, retry frequency, escalation thresholds).** Deferred to Phase 5 working agreements per META_PLAN v6 § 7.13's pattern. CONVERGENCE_CRITERIA states the deferral explicitly in § 6.3.

### 2.3 Authority chain

Per META_PLAN v6 § 4.1, CONVERGENCE_CRITERIA is the only Phase 0 document whose tier is determined pre-hoc per § 6.5; per Tony's locked Q2 in the v1 cycle, the determination is Tier 1 (QB-drafted, abstract criteria, no companion verification log). Per Tony's locked Q1, scope is the Phase 1 convergence test only.

---

## 3. The Phase 1 convergence test (operationalized)

### 3.1 Test framing (per META_PLAN v6 § 3.2.1)

META_PLAN v6 § 3.2.1 specifies the Phase 1 convergence test verbatim:

> **Convergence test for the Phase 1 inventory:** any Phase 1 document inventory BIBLE_STRUCTURE_SPEC.md produces must be auditable against the question: "given this inventory, can a fresh CC session evaluate, rebuild, or retrain a model in the gallery?" If the answer is no for any of the three workflows, the inventory has not satisfied the forcing function and must be revised.

CONVERGENCE_CRITERIA operationalizes this test by specifying what "evaluate," "rebuild," and "retrain" mean as workflows, what makes a fresh CC session's plan "actionable," and what conditions classify the test's verdict as PASS / FAIL / PARTIAL.

### 3.2 Test invocation

The test is invoked when Phase 1 has produced the seven locked bibles (per BIBLE_STRUCTURE_SPEC v3 § 4.1) and the cross-document consistency audit has passed (per AUDIT_METHODOLOGY v2 § 3.2 + § 7).

A **fresh CC session** is invoked. "Fresh" means: no prior context beyond (a) the locked Phase 1 corpus + Phase 0 methodology documents at `/docs/bible/` and `/docs/bible/_meta/` and (b) the test request. The CC session has access to the EE codebase at `/home/strakajagr/projects/equine-equalizer/` and to live AWS state, but the test is whether the bible alone is sufficient to produce the plan; access to the codebase / AWS state is for verification of the plan's bible-traced content, not for plan content itself. (Per § 3.5 below: a plan that requires reading the codebase to be coherent fails the "based on the bible" criterion.)

The test request takes one of three forms (per § 3.3 below). Each form is exercised independently as a separate fresh CC session. The convergence test's verdict aggregates across the three.

### 3.3 The three workflows

The three workflows correspond to META_PLAN v6 § 3.2.1's three forcing functions:

1. **Evaluate workflow.** Test request: "Evaluate model X in the gallery against its success criteria. Produce a plan for the evaluation." X is a specific model identified by canonical reference (per BIBLE_STRUCTURE_SPEC v3 § 7.1 cross-reference syntax — e.g., `ml_layer_architecture_bible:4.1.<version_name>`).

2. **Rebuild workflow.** Test request: "Rebuild model X (or design a new ML layer Y plugging into the gallery). Produce a plan for the rebuild / new layer." X / Y is identified by canonical reference or by description; the plan's job is to specify the architecture decisions, feature inputs, pipeline position, and composition with existing models.

3. **Retrain workflow.** Test request: "Retrain model X with a new training cycle. Produce a plan for the retrain." X is identified by canonical reference; the plan's job is to specify the retraining trigger, feature set, data window, training pipeline, and deployment gating.

Each workflow exercises a distinct subset of the locked corpus. Per BIBLE_STRUCTURE_SPEC v3 § 4.1 + § 4.3:

- **Evaluate** exercises primarily the Model Evaluation & Retraining Bible (per-model success criteria; current values; retraining triggers) plus cross-references to ML Layer Architecture Bible (model composition) and Database & Schema Bible (data sources).
- **Rebuild** exercises primarily the ML Layer Architecture Bible (model gallery; composition; calibration state) plus cross-references to Feature Provenance Bible (feature inputs) and Architecture Overview (pipeline position).
- **Retrain** exercises primarily the Feature Provenance Bible (current feature schema) and Model Evaluation & Retraining Bible (retraining triggers; deployment gating) plus cross-references to Data Pipeline Bible (training data flows) and Database & Schema Bible (training data sources).

### 3.4 Plan production criteria

A fresh CC session "produces" a plan when:

- The CC session has read the locked corpus (Phase 1 bibles + Phase 0 methodology documents) sufficient to ground the plan.
- The CC session emits the plan as text output, in a single production cycle (no "to be continued" or "draft pending further analysis" state).
- The plan is internally coherent (reads as continuous prose, structured sections, or enumerated steps — format choice is delegated to the CC session per Tony's drafting-spec deferral).
- The plan addresses the test request directly. A plan that punts to "operator should investigate" without specifying what to investigate fails this criterion.

The criteria do not specify a tool-call iteration count, time budget, or other cadence. Cadence specification is deferred to Phase 5 working agreements per § 6.3.

### 3.5 Plan-based-on-bible criteria

The plan is "based on the bible" when:

- **Cross-references resolve.** Every cross-reference in the plan to a Phase 1 bible section (per BIBLE_STRUCTURE_SPEC v3 § 7.1 syntax) resolves to an actual section in the cited bible. Mechanical check: each `<bible_name>:<section_id>` reference has a corresponding section header in `/docs/bible/<bible_name>.md`.
- **No external context required.** The plan is coherent without requiring the reader to consult the EE codebase, dump, AWS state, or other extra-bible material. (This does not preclude the plan from RECOMMENDING external verification as a next step — that's appropriate plan content. It precludes the plan from REQUIRING external context to be itself coherent.)
- **Content traces to bible content.** Specific facts in the plan (model names, feature lists, file paths, line numbers, dates, counts) trace to a specific bible section that contains those facts. Mechanical check: each concrete claim in the plan is paired with a bible cross-reference; the cited bible section contains the claim.
- **No methodology-interpolation.** The plan does not introduce new methodology rules, success thresholds, or evaluation criteria beyond what the locked corpus contains. Per AUDIT_METHODOLOGY v2 § 4.2's prophylactic check, methodology constructs in the plan must trace to META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 / AUDIT_METHODOLOGY v2 / Phase 1 bible content.
- **No fabricated content.** Per AUDIT_METHODOLOGY v2 § 4.1's prophylactic check, every concrete claim in the plan is verifiable against a specific bible section; no claims that contradict the bible.

The mechanical checks above are the precision floor: the plan can be evaluated as based-on-the-bible by a reader who follows the cross-references and verifies each. Two readers applying these checks to the same plan reach the same verdict.

---

## 4. Per-workflow success criteria

### 4.1 Actionable evaluate plan

An evaluate plan is **actionable** when it satisfies all of the following:

- **Identifies the model under evaluation by canonical reference.** The plan cites the model's `ml_layer_architecture_bible:4.1.<version_name>` (or analogous per-model section) per BIBLE_STRUCTURE_SPEC v3 § 6.4 § 4.1's per-model detail format.
- **Cites the success criteria the model is being evaluated against.** Cross-reference to Model Evaluation & Retraining Bible's per-model success criteria sub-section (per BIBLE_STRUCTURE_SPEC v3 § 6.5 § 3 framing of "per-model success criteria").
- **Specifies what data to query for current values.** Cross-reference to Database & Schema Bible's relevant table(s) or to live API endpoints documented in the Architecture Overview / API & Frontend Bible.
- **Reaches a pass/fail conclusion against the cited criteria.** The plan does not stop at "here is the data to query"; it states the conclusion the evaluator should draw from the data, conditional on what the data shows.
- **Recommends a next action.** "Continue without changes," "schedule retrain," "deprecate," "investigate symptom X" — with rationale grounded in the bible's content.

The plan does NOT need to predict the actual result of the evaluation (a plan is not an execution). It needs to specify what the execution would do and how the execution's output would map to a conclusion.

### 4.2 Actionable rebuild plan

A rebuild plan is **actionable** when it satisfies all of the following:

- **Identifies the model architecture decisions.** Type (XGBoost / LSTM / RandomForest / Bayesian / logistic regression ensemble per ML Layer Architecture Bible § 4 patterns), inputs, outputs, hyperparameters where the bible specifies them.
- **Cites the required features.** Cross-reference to Feature Provenance Bible's per-feature provenance entries for each input feature; the plan does not list features by name without grounding them in the Feature Provenance Bible.
- **Specifies pipeline position.** Where the new or rebuilt layer plugs into the inference pipeline per ML Layer Architecture Bible § 4.2's per-pipeline composition.
- **Specifies composition with existing models.** How the new layer's outputs combine with other layers' outputs per the bible's ensemble / composition patterns.
- **Specifies the training pipeline.** Which training script, which Lambda or ECS task family, which data sources — cross-references to Data Pipeline Bible and Architecture Overview.
- **Specifies success criteria for the new or rebuilt layer.** Cross-reference to Model Evaluation & Retraining Bible's success criteria patterns.

The plan addresses the rebuild as a complete spec: a Phase 5 implementer reading the plan can begin execution without further architectural research within the bible-spanned scope.

### 4.3 Actionable retrain plan

A retrain plan is **actionable** when it satisfies all of the following:

- **Identifies the retraining trigger.** Data drift / performance degradation / scheduled retrain / new feature schema — cross-reference to Model Evaluation & Retraining Bible's retraining-trigger taxonomy (per BIBLE_STRUCTURE_SPEC v3 § 6.5 § 4.1's enumeration).
- **Cites the feature set being trained on.** Cross-reference to Feature Provenance Bible's per-model feature consumption (the model_versions.feature_list JSONB documented per BIBLE_STRUCTURE_SPEC v3 § 6.3 § 4.2). If the retrain involves a feature schema change, the plan documents the schema delta and cross-references the Feature Provenance Bible's per-feature provenance for each new or changed feature.
- **Specifies the data window.** Training data range — what to include, what to exclude — grounded in Data Pipeline Bible's data-acquisition state.
- **Specifies the training pipeline.** Which training script (per Architecture Overview's ECS task family inventory), which artifacts produced (per Model Evaluation & Retraining Bible's S3 artifact paths).
- **Specifies deployment gating.** What must be true for the new artifact to ship to production — cross-reference to Model Evaluation & Retraining Bible § 4.4 deployment gating discipline.
- **Cross-references calibration discipline.** If the retrain affects calibration (sidecar fitting, bypass state), the plan cross-references ML Layer Architecture Bible § 4.3 (calibration / bypass state) and Model Evaluation & Retraining Bible § 4.2 (calibration discipline as process).

The plan addresses the retrain as a complete operational sequence: a Phase 5 implementer reading the plan knows what triggered the retrain, what the retrain will produce, and what gates the deployment.

### 4.4 What "actionable" does NOT mean

To preserve the recursive precision check, "actionable" is bounded by what the bible itself supports. The plan need not:

- Predict execution results.
- Specify implementation details below the bible's documented granularity.
- Resolve open questions the bible itself flags as Phase 5 decisions.
- Substitute for verification the bible directs to external systems (live AWS, dashboard endpoints, code reads).

A plan that punts to "operator decides X" where X is a Phase 5 working-agreement decision per the bible's own framing is not failing the actionable criterion — it's correctly inheriting the deferral. Conversely, a plan that punts to "operator decides X" where X is a question the bible answers explicitly fails the actionable criterion.

The audit-CC's check (per AUDIT_METHODOLOGY v2 § 5) on the plan determines whether punts are correct deferrals or unjustified handoffs. The cross-reference target adjudicates: a punt is a correct deferral when the cited deferral target is a Tony-locked Phase 5 working-agreement deferral (per META_PLAN v6 § 7.13's pattern).

---

## 5. PASS / FAIL / PARTIAL conditions

### 5.1 PASS conditions

The Phase 1 convergence test PASSES when **all three workflows** (evaluate, rebuild, retrain) produce actionable plans satisfying the criteria in § 3.4 + § 3.5 + § 4. Specifically:

- Each of the three plans is produced per § 3.4 (fresh CC session; single production cycle; coherent text).
- Each of the three plans is based on the bible per § 3.5 (cross-references resolve; no external context required; content traces to bible; no methodology-interpolation; no fabricated content).
- Each of the three plans is actionable per the relevant § 4 sub-section (evaluate per § 4.1; rebuild per § 4.2; retrain per § 4.3).

### 5.2 FAIL conditions

The Phase 1 convergence test FAILS when **none of the three workflows** produces an actionable plan. None of the three plans satisfies all of § 3.4 + § 3.5 + § 4. A FAIL verdict implies the locked corpus has fundamental gaps — not surgical issues with one or two bibles, but structural deficiencies that prevent any workflow from converging.

A FAIL verdict triggers a corpus-level reassessment per § 6.2.3, not surgical per-bible revision.

### 5.3 PARTIAL conditions

The Phase 1 convergence test is PARTIAL when **at least one workflow passes AND at least one workflow fails**. Some workflows produce actionable plans; others do not. Partial-pass triggers per-bible revision for the failing workflows per § 6.2.

### 5.4 Aggregation across the three workflows

The verdict aggregation is mechanical — three workflows, each independently scored as pass / fail per § 5.1's criteria, then aggregated:

- 3 of 3 workflows pass → PASS.
- At least 1 of 3 passes AND at least 1 of 3 fails → PARTIAL.
- 0 of 3 workflows pass → FAIL.

The aggregation does not introduce thresholds beyond the qualitative classification. Two readers applying the per-workflow criteria reach the same per-workflow verdicts and therefore the same aggregated verdict.

### 5.5 Per-workflow scoring discipline

Per the criteria's all-must-be-satisfied framing in § 3.4 + § 3.5 + § 4, each criterion is independently necessary for a workflow to pass. The per-workflow scoring is therefore not graduated — a workflow either satisfies the conjunction of its criteria (pass) or it does not (fail). PARTIAL exists only at the aggregation level (across workflows per § 5.4), not within a single workflow.

This discipline preserves the recursive precision check: a single workflow's scoring is mechanically determinable from the criteria's conjunction; the aggregation across workflows is mechanically determinable from the per-workflow verdicts.

---

## 6. Post-test actions

### 6.1 PASS

When the convergence test verdict is PASS, the Phase 1 corpus is verified fit for purpose per META_PLAN v6 § 3.2.1. Phase 1 is ready to lock as a corpus.

**Phase 1 corpus lock conditions** (per the cumulative locked Phase 0 framework):

1. All seven Phase 1 bibles individually locked (per AUDIT_METHODOLOGY v2 § 3.1's per-bible cycle).
2. Cross-document consistency audit passed (per AUDIT_METHODOLOGY v2 § 3.2 + § 7).
3. Convergence test verdict is PASS (per § 5.1 above).

When all three conditions hold, Phase 1 is locked as a corpus. Phase 2 entry conditions (per META_PLAN v6 § 3.3) can then be evaluated.

### 6.2 FAIL or PARTIAL

When the convergence test verdict is PARTIAL or FAIL, per-bible revision is triggered for the failing workflow(s).

#### 6.2.1 PARTIAL — workflow-to-bible mapping

The failing workflow implicates a specific subset of the seven Phase 1 bibles per the forcing-function mapping (from BIBLE_STRUCTURE_SPEC v3 § 4.1 + § 4.3):

- **Evaluate workflow fails →** the Model Evaluation & Retraining Bible is the primary candidate for revision (per its forcing-function mandate to answer "is the model still working, when do I retrain it, what gates deployment?"). Cross-references to ML Layer Architecture Bible (model composition) and Database & Schema Bible (data sources) are secondary; revision to those bibles is triggered only if the audit identifies the failure root in their content.

- **Rebuild workflow fails →** the ML Layer Architecture Bible is the primary candidate for revision (per its forcing-function mandate to answer "if I add a new ML layer, where does it plug in?"). Cross-references to Feature Provenance Bible (feature inputs) and Architecture Overview (pipeline position) are secondary.

- **Retrain workflow fails →** the Feature Provenance Bible OR the Model Evaluation & Retraining Bible is the primary candidate for revision (both bibles are load-bearing for the retrain workflow per their forcing functions). Tony decides per the failure mode which bible's revision is the corrective.

The audit-CC executing the convergence test identifies which specific criterion(a) the failing workflow's plan violated. The violated criterion(a) traces to the bible section the criterion drew from; that bible is the revision candidate.

#### 6.2.2 PARTIAL — re-test cadence

After per-bible revision, the convergence test re-runs against the revised corpus. The cadence specification (how many test runs before escalation; whether test re-runs are full three-workflow tests or targeted to the previously-failing workflow) is **explicitly NOT specified** here per § 6.3.

#### 6.2.3 FAIL — corpus-level reassessment

When the verdict is FAIL (zero of three workflows pass), the failure is structural rather than surgical. Per-bible revision for individual bibles is unlikely to resolve a corpus-level failure; the audit's findings will surface architectural issues (corpus inventory missing a bible; forcing functions inadequately served; cross-bible references broken at scale; etc.).

QB surfaces the FAIL verdict to Tony. Tony decides whether to (a) trigger BIBLE_STRUCTURE_SPEC revision (if the corpus inventory is the root issue), (b) trigger META_PLAN revision (if the forcing-function specification is the root issue), or (c) treat the FAIL as a per-bible-revision cluster requiring multi-bible coordinated revision.

A FAIL verdict is rare and serious. It indicates Phase 0 methodology produced a Phase 1 corpus inventory that does not satisfy its own forcing functions — which would be a methodology gap surfaceable to Tony with proposed methodology resolutions per META_PLAN v6 § 6.3 architectural authority discipline.

### 6.3 Iteration discipline (cadence deferred)

CONVERGENCE_CRITERIA does not specify:

- How many convergence test runs constitute "repeated failure on the same dimension" before escalation.
- How frequently test runs occur during PARTIAL → revision → re-test cycles.
- Time budget per test execution.
- Whether test re-runs after revision are full three-workflow tests or targeted to the previously-failing workflows.

These are all cadence-shaped specifications. Per META_PLAN v6 § 7.13's deferral pattern (commit cadence, audit cadence, Layer 1 physical form all deferred to Phase 5 working agreements), CONVERGENCE_CRITERIA defers cadence specifications to Phase 5 working agreements. Until Phase 5 working agreements are designed, test-execution cadence is QB's call surfaced to Tony per the methodology-interpolation rule's avoidance-of-CC-prescribed-cadence-rules discipline.

The deferral is symmetric to AUDIT_METHODOLOGY v2 § 8.2 (cross-document audit re-trigger cadence after per-bible revision deferred to Phase 1 working agreements once 2-3 bibles draft and patterns emerge). Both deferrals reflect the same principle: cadence specifications belong to operational phase entry, not to the methodology codified in Phase 0.

---

## 7. Open questions

Surfaced for resolution during Phase 0 iteration. Not blocking CONVERGENCE_CRITERIA lock unless audit returns one as critical.

### 7.1 Plan format granularity

§ 3.4 specifies the plan emerges as text in a single production cycle but does not prescribe a specific format (continuous prose / structured sections / enumerated steps). Whether Phase 1 working agreements should standardize a format is deferred. The non-prescription is intentional: format is a presentation choice, not a load-bearing methodology construct, and the per-workflow criteria in § 4 specify content requirements that any reasonable format can satisfy.

### 7.2 Test-execution by audit-CC vs. by drafting-cycle CC

The convergence test invokes a "fresh CC session" (per § 3.2). Whether this CC session is methodologically distinct from the audit-CCs that conduct per-bible audits (per AUDIT_METHODOLOGY v2 § 3.1) is not specified here. In practice, both fresh CC sessions execute against the locked corpus; the test-execution session is fresh in the same sense audit-CC sessions are fresh.

The non-distinction is intentional: the convergence test's value is in evaluating the corpus's fitness for the three workflows, not in the specific identity of the executing CC session.

### 7.3 Convergence test re-run after Phase 1 corpus lock

Whether the convergence test re-runs after Phase 1 corpus lock + drift detection (e.g., periodic re-execution to detect bible-corpus drift from code) is a Phase 5 working-agreement decision per the same deferral pattern as audit cadence. Not specified here.

---

## 8. Lock Status

**Document status:** DRAFT v2, pre-audit
**Audit-CC pass:** pending (v2 audit pending after disk write)
**Verification log:** N/A per Tier 1 designation (Tony's locked Q2; carried forward from v1)
**Tony review:** pending (will see post-audit version per workflow discipline)
**Locked:** [pending]

**Phase 0 prerequisites carried over from META_PLAN v6 § 11:**
- All 5 Phase 0 documents pass adversarial audit (Tony's threshold: < 5 MATERIAL findings AND zero fabricated-content findings AND zero methodology-interpolation findings)
- Operating-model convergence test passes (META_PLAN v6 § 5.4) — note this is the Phase 0 convergence test, distinct from the Phase 1 convergence test specified in this document
- EE production code committed to baseline (META_PLAN v6 § 3.1.1)
- `.gitignore` baseline audit performed; findings documented at `_audits/gitignore_baseline_audit.md` (META_PLAN v6 § 7.14)
- `PHASE_5_BACKLOG.md` created with Bug #28 as first entry (META_PLAN v6 § 8.2)

**Next action:** CC audits v2 per the adversarial scope inherited from META_PLAN v6 § 6.2 + AUDIT_METHODOLOGY v2 § 6 + § 7. QB synthesizes findings.

---

## 9. Changelog

### v1 → v2

**MATERIAL fixes (v1 audit findings):**

- **Finding 1 — § 1.1 cross-reference to AUDIT_METHODOLOGY v2 § 8.4.** v1 § 1.1 cited "AUDIT_METHODOLOGY v2 § 8.4 (parallel deferral noted via the cross-document audit's convergence test application)" as a parallel deferral source alongside BIBLE_STRUCTURE_SPEC v3 § 8.4. v1 audit verified AUDIT_METHODOLOGY v2 § 8 has only § 8.1, § 8.2, § 8.3 — § 8.4 does not exist. The characterization of AUDIT_METHODOLOGY v2 as deferring "specific success criteria" was also incorrect; AUDIT_METHODOLOGY v2 § 8.2 defers cross-document audit re-trigger CADENCE (not convergence-test criteria) to Phase 1 working agreements. v2 drops the AUDIT_METHODOLOGY v2 § 8.4 reference. v2 § 1.1 now relies solely on BIBLE_STRUCTURE_SPEC v3 § 8.4 as the single deferral source, and notes that AUDIT_METHODOLOGY v2 § 3.2 + § 7 reference the convergence test indirectly (without formally deferring criteria).

- **Finding 2 — § 3.1 verbatim block bold formatting drop.** v1 § 3.1's verbatim claim ("META_PLAN v6 § 3.2.1 specifies the Phase 1 convergence test verbatim:") was followed by a block quote that dropped the bold markdown on "**Convergence test for the Phase 1 inventory:**". v1 audit verified the source (META_PLAN v6 line 245) has bold formatting on the section-header phrase. v2 re-adds the bold markdown to restore character-exact source reproduction including formatting fidelity. One-character-pair fix (`**...**` re-added).

**MINOR fixes (tightly coupled to MATERIALs in pedagogical purpose, per Tony's Q1 Option B):**

- **Finding 3 — § 3.4 single-production-cycle cadence chosen without § 10 surfacing.** Tony's drafting spec D listed two options for the plan production criterion ("N tool-call iterations" OR "single read-then-write workflow"), with framing "Tony's call on cadence specification." v1 chose option (b) without surfacing the choice in § 10. v2 adds § 10.2 surfacing note item 6 documenting the option choice and surfacing for Tony's ratification.

- **Finding 4 — § 5.5 binary scoring discipline borderline framing.** v1's § 5.5 framing "fails any one criterion" paralleled v4 § 9.13's caught binary test ("Removing any one converts to FORBIDDEN"). The substance (binary scoring per the conjunction of criteria) follows from Tony's spec F language; the framing was the issue. v2 rephrases to "each criterion is independently necessary" / "satisfies the conjunction of its criteria (pass) or it does not (fail)." Substance preserved; v4-§-9.13 framing parallel removed.

**STYLE deferral (per Tony's Q1 Option B):**

- **Finding 5 — § 3.4 + § 4.4 punt-handling binary framing.** Deferred to Phase 1 opportunistic per Tony's Q1 Option B + the methodology-interpolation principle (don't pre-empt cycles that haven't run with theoretical optimizations). v2 leaves § 3.4 and § 4.4 unchanged.

**Methodology lesson candidate banked (per Tony's Q2 ratification):**

The recursive precision pattern caught at AUDIT_METHODOLOGY v1 Finding 1 (paraphrase-as-verbatim) and CONVERGENCE_CRITERIA v1 Finding 2 (formatting-as-not-verbatim) is the same class of finding across two consecutive Phase 0 documents. Generalization candidate: ALL Phase 0 documents that quote locked source material must reproduce source character-exact INCLUDING formatting (markdown bold, italics, code spans, line breaks, bullet structure) when claiming verbatim. Currently TWO instances; per Tony's Q2, NO formal codification in AUDIT_METHODOLOGY v3 yet (premature with two instances; codify if THIRD instance recurs in TRIAGE_QUEUE_SPEC v1 audit). Banked here for v3 cycle's consideration.

**QB drafting spec error disclosure (per Tony's Q3 ratification):**

The CONVERGENCE_CRITERIA v1 drafting spec asserted a cross-reference to "AUDIT_METHODOLOGY v2 § 8.4 (cross-document audit deferral)" as a parallel deferral source. v1 inherited the spec error without verifying that § 8.4 exists in AUDIT_METHODOLOGY v2. v1 audit caught the orphaned reference; v2 corrects by dropping it.

The QB drafting spec error (asserting an § 8.4 reference that doesn't exist in the cited locked document) is documented here to establish symmetric documentation precedent: QB drafting specs are subject to the same cross-reference verification rigor as CC drafts. QB lapses get equivalent documentation to CC errors. Discipline asymmetry — flagging CC interpolation while not flagging QB spec errors — would compromise the methodology-interpolation rule's symmetric application across roles. Per META_PLAN v6 § 6.1's grandfathering clause's provenance discriminator (CC-introduced vs QB-drafted), the discriminator captures provenance, not role-favored treatment; both QB-introduced and CC-introduced errors are flaggable.

The v1 cycle's "Tony's locked decision based on a wrong premise" instance per META_PLAN v6 § 3.1 edge case enumeration applies here: the drafting spec asserted a premise (existence of AUDIT_METHODOLOGY v2 § 8.4) that turned out to be false on verification. v1 audit surfaced the contradiction; v2 applies the verified-fact reframing rather than silent compliance.

**Net new methodology constructs in v2: ZERO.** All v2 changes are surgical patches per audit-CC's Findings 1, 2, 3, 4 recommendations + Tony's three locked decisions (Q1 Option B + Q2 + Q3). The recursive precision pattern is BANKED in changelog as a methodology lesson candidate, not codified as a formal rule (per Tony's Q2 ratification — codify if third instance recurs in TRIAGE_QUEUE_SPEC v1).

**Retained from v1 unchanged:**

Front matter (revised for v2 metadata), § 1 (except § 1.1 first paragraph for Finding 1), § 2, § 3 (except § 3.1 verbatim block for Finding 2), § 4, § 5 (except § 5.5 for Finding 4), § 6, § 7, § 8, § 10 (except § 10.2 added item 6 for Finding 3). No verification log per Tier 1 designation (carried forward from v1).

### v1 (initial draft)

Initial QB draft per Tony's locked Q1 (Phase 1 convergence test only) and locked Q2 (Tier 1; abstract criteria; no companion verification log; no EE-specific worked examples).

Document scope per Q1: Phase 1 convergence test PASS / FAIL / PARTIAL conditions; per-workflow success criteria for evaluate / rebuild / retrain; plan production criteria; plan-based-on-bible criteria; post-test action triggers. Out of scope: Phase 0 audit-cycle convergence (already in META_PLAN v6 § 11); Phase 2-4 convergence (deferred to phase entry); per-bible audit threshold (inherited from META_PLAN v6 § 11); bible content / audit methodology / triage queue format (covered by BIBLE_STRUCTURE_SPEC v3 / AUDIT_METHODOLOGY v2 / TRIAGE_QUEUE_SPEC respectively).

§ 3 operationalizes META_PLAN v6 § 3.2.1's locked test framing into invocation, three workflows, plan production criteria, and plan-based-on-bible criteria. § 4 specifies per-workflow success criteria for the three workflows (evaluate, rebuild, retrain), each cross-referencing the relevant Phase 1 bibles per BIBLE_STRUCTURE_SPEC v3 § 4.1 + § 4.3 forcing-function mapping. § 5 aggregates the per-workflow verdicts into the PASS / FAIL / PARTIAL classifications. § 6 specifies post-test action triggers including the BIBLE_STRUCTURE_SPEC v3-based workflow-to-bible revision mapping and the explicit cadence deferral to Phase 5.

No new flagging thresholds introduced; thresholds inherited from META_PLAN v6 § 11. No new methodology constructs introduced beyond what META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 / AUDIT_METHODOLOGY v2 / Tony's locked drafting spec for this document explicitly authorize. The methodology-interpolation rule applies symmetrically to QB-drafted content (Tier 1 designation does not exempt QB from the rule); v1 surfacing notes in § 10.

---

## 10. QB Drafting Notes (Self-Check Surfaces)

Per the methodology-interpolation rule, QB reviewed every new construct introduced in v1 against the rule. Items below are surfaced for Tony's awareness; QB's judgment on each is included.

### 10.1 Constructs explicitly authorized by Tony's locked drafting spec

- Tier 1 designation per Tony's Q2 v1 cycle ratification.
- Scope = Phase 1 convergence test only per Tony's Q1 v1 cycle ratification.
- The seven required content categories (A through I) per the drafting spec's "REQUIRED CONTENT" enumeration.
- The eleven required deliverable structure sections (1 through 11) per the drafting spec's "REQUIRED DELIVERABLE STRUCTURE."
- All cross-references to META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 / AUDIT_METHODOLOGY v2 sections.
- Threshold language inherited from META_PLAN v6 § 11.
- Edge case enumeration patterns inherited from prior Phase 0 documents.
- The cadence deferral to Phase 5 (per § 6.3) explicitly authorized by drafting requirement I.

### 10.2 v1 surfacing notes

QB reviewed every new methodology construct introduced in v1 against the methodology-interpolation rule and the pattern-completion check.

1. **§ 5.4 verdict aggregation as "3 of 3 / at least 1 of 3 / 0 of 3" qualitative classification.** The drafting spec specified PASS / FAIL / PARTIAL but did not specify the boundary between PARTIAL and FAIL precisely. QB chose a qualitative-not-numerical aggregation: PASS = all pass; PARTIAL = at least one passes AND at least one fails; FAIL = none pass. Pattern-completion check: this is the most parsimonious classification consistent with the drafting spec's three categories. Avoids percentage criteria (e.g., "≥ 67% pass = PARTIAL") which would be methodology-interpolation. **Surfaced for Tony's confirmation.** If Tony prefers a different boundary (e.g., "FAIL when 2 of 3 fail" rather than "FAIL when all fail"), specify in v2 cycle.

2. **§ 5.5 per-workflow scoring discipline ("not graduated within a single workflow").** QB stated explicitly that within a single workflow's scoring, there is no "mostly passes" — pass or fail per the criteria. Pattern-completion check: this preserves the recursive precision check (criteria mechanically determinable). Drafting spec's framing of per-workflow criteria with all-must-be-satisfied implies the binary scoring; § 5.5 surfaces it explicitly. **Borderline.** This is a binary test (pass/fail per criterion). Whether Tony has implicitly authorized this binary by specifying the criteria "the plan is actionable when it satisfies all of the following" is the question. QB's judgment: the binary follows from the criteria's framing, not from new methodology — but surfacing for Tony's awareness in case the binary requires explicit ratification.

3. **§ 4.4 "What 'actionable' does NOT mean."** QB added this subsection to clarify the boundary of the actionable criterion (specifically, that a plan correctly inheriting Tony-ratified Phase 5 deferrals is not failing the actionable criterion). Pattern-completion check: this is bounding the criterion against the methodology-interpolation rule's deferral discipline (per META_PLAN v6 § 7.13's pattern). Not introducing new methodology; clarifying scope. **Judged acceptable.**

4. **§ 6.2.3 FAIL escalation framing ("structural rather than surgical").** QB framed the FAIL verdict's response as escalation to Tony with three resolution options (BIBLE_STRUCTURE_SPEC revision; META_PLAN revision; multi-bible coordinated revision). Pattern-completion check: the three options trace to META_PLAN v6 § 6.3's architectural authority discipline (Tony decides architectural calls; QB surfaces with proposed resolutions). Not introducing new methodology; restating the existing escalation pattern in the FAIL verdict's specific context. **Judged acceptable.**

5. **§ 3.5's mechanical-check enumeration ("cross-references resolve / no external context required / content traces").** QB framed the plan-based-on-bible criteria as mechanical checks per the drafting spec's E requirement. Pattern-completion check: each mechanical check directly maps to a drafting spec sub-requirement (E.1-E.4). Not introducing new methodology; operationalizing the spec's enumeration into checkable conditions. **Judged acceptable.**

6. **§ 3.4 "single production cycle" cadence chosen from spec D's two enumerated options (added v2 per v1 audit Finding 3).** Tony's drafting spec D listed two options for the plan production criterion: "produces the plan within N tool-call iterations" OR "produces the plan in single read-then-write workflow" — with framing "Tony's call on cadence specification." v1 chose option (b) "single read-then-write workflow" and emitted the choice in § 3.4 as "single production cycle (no 'to be continued' or 'draft pending further analysis' state)." Pattern-completion check: the choice is from Tony's enumerated options — within the spec's authorized scope. The choice is not interpolation in the strict sense (it's an option Tony listed); the surfacing of the choice for Tony's ratification IS the discipline. v2 closes v1's surfacing gap. **Surfaced for Tony's ratification of the pick.** If Tony prefers option (a) "N tool-call iterations" or wants to clarify whether the choice is QB-authorized within enumerated options vs. requires explicit Tony pick, specify in v3 cycle.

The methodology-interpolation rule is operative; the discipline of self-surfacing remains. v1 + v2 surface what's new.

### 10.3 Constructs explicitly NOT drafted (to avoid interpolation)

QB did not draft any of the following — each would have been pattern-completion or methodology-interpolation:

- **Numerical thresholds for what counts as "actionable"** (e.g., "plan must have ≥ N elements") — not drafted; criteria specified abstractly per drafting spec.
- **Percentage criteria for what counts as "based on the bible"** (e.g., "≥ 90% of cited references must resolve") — not drafted; mechanical check is per-reference (each must resolve), not aggregate.
- **Cadence rules for test-execution count** — not drafted; deferred to Phase 5 per § 6.3.
- **Severity thresholds for FAIL vs PARTIAL distinction beyond aggregate pass count** — not drafted; classification is qualitative per § 5.4 (3/3 PASS; 1-2/3 PARTIAL; 0/3 FAIL).
- **Iteration cap on convergence test re-runs** — not drafted; deferred to Phase 5 per § 6.3.
- **Re-test scope rules** (full three-workflow vs. targeted-to-failing-workflow) — not drafted; deferred to Phase 5 per § 6.3.
- **Time budget per test execution** — not drafted; deferred to Phase 5 per § 6.3.
- **Plan format mandates** (continuous prose / structured / enumerated) — not drafted; format choice delegated to test-execution CC session per § 3.4.
- **New letter-prefix conventions** — not drafted (W.N remains the only ratified prefix per BIBLE_STRUCTURE_SPEC v3 § 5.5).
- **EE-specific worked examples** — not drafted per Tony's Q2 Tier 1 ratification (worked examples would require EE codebase verification, which Tier 1 does not require).
- **Tiebreaker criteria for the workflow-to-bible mapping (§ 6.2.1)** — not drafted; the "Tony decides per the failure mode" framing for the retrain-workflow ambiguity (Feature Provenance vs Model Evaluation & Retraining Bible) defers per META_PLAN v6 § 8.3 decision-deferral discipline.
- **Convergence-test execution cadence after Phase 1 corpus lock** — not drafted; surfaced as Open Question 7.3.

The methodology-interpolation rule is operative; QB resisted introducing constructs beyond the drafting spec's authorized scope. The discipline of self-surfacing remains. v1 surfaces what's new.

---

End of CONVERGENCE_CRITERIA.md v2.
