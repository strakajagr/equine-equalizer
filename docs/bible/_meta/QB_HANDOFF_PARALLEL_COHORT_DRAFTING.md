# QB HANDOFF: PARALLEL COHORT DRAFTING — PHASE 1 DELIVERABLES 4-5-6

**Document Type:** Meta-orchestration handoff
**Cohort:** Phase 1 Deliverables 4 / 5 / 6
**Status:** RATIFIED 2026-05-06
**Authored by:** QB (chat-output) → write-routed via fresh CC session per § 4.12
**Ratified by:** Tony (Q1–Q4 architectural ratifications)
**Path:** `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/QB_HANDOFF_PARALLEL_COHORT_DRAFTING.md`

---

## § 1. SCOPE

This handoff governs the orchestration of Phase 1 Deliverables 4, 5, and 6, the three load-bearing ML re-architecture bibles for Equine Equalizer:

| # | Bible | Target Path | Forcing Function |
|---|-------|-------------|------------------|
| 4 | Feature Provenance Bible | `docs/bible/feature_provenance_bible.md` | For every feature × every model: source data → engineering code → consuming model(s) → target latent → train/inference duplication-or-divergence |
| 5 | ML Layer Architecture Bible | `docs/bible/ml_layer_architecture_bible.md` | For every model in gallery: type (XGB/LSTM/Bayesian/RF/ensemble), inputs, outputs, position in inference pipeline, target latent, output composition, calibration/bypass state |
| 6 | Model Evaluation & Retraining Bible | `docs/bible/model_evaluation_retraining_bible.md` | Per-model success criteria, retraining triggers, calibration discipline, model artifact version control, deployment gating |

Per BIBLE_STRUCTURE_SPEC v6 § 3.2.1: three separate physical `.md` files at three distinct paths. No merging into a single ML Bible. No single-bible compression of forcing functions.

---

## § 2. INHERITANCE BUNDLE

Every drafting CC session for this cohort reads the following locked substrate at session start. This is the canonical read-set; deviation from it requires QB authorization.

### § 2.1 Phase 0 Locks
- META_PLAN v9
- BIBLE_STRUCTURE_SPEC v6
- AUDIT_METHODOLOGY v2-patched (§ 4.1–4.11 banked; § 4.12 operative pending patch-CC routing)
- CONVERGENCE_CRITERIA v2
- TRIAGE_QUEUE_SPEC v1

### § 2.2 Phase 1 Locks (deliverables 1-2-3)
- Architecture Overview v3 — `docs/bible/architecture_overview.md` (LOCKED 2026-05-05)
- Database & Schema Bible v1-patched-d2 — `docs/bible/database_schema_bible.md` (LOCKED 2026-05-06; 15 domain tables incl. `angle_stats`; matview `trainer_stats`)
- Data Pipeline Bible v1-patched-c — `docs/bible/data_pipeline_bible.md` (LOCKED 2026-05-06; 9 flows; Bug #28 § 8.W.1)

### § 2.3 Active Discipline (operative across all CC sessions in cohort)
- Option 1 with 9 self-audit checks (substrate verification 1-3 / content verification 4-6 / workflow verification 7-9)
- Lessons 1-6 from META_PLAN cycles
- Lesson § 4.8 — Tony ratification mediation
- Lesson § 4.9 — light surface review only on QB review pass
- Lesson § 4.10 — verbatim-paste discipline
- Lesson § 4.11 — prediction-precision lesson
- Lesson § 4.12 — QB does not invoke MCP write tools (operative pending AUDIT_METHODOLOGY patch)
- Lesson 3 expansion — convention identifiers verified at primary source at spec-authorship time

---

## § 3. ORCHESTRATION MODEL — HYBRID PARALLEL (RATIFIED Q1)

### § 3.1 Phase Structure

**Phase A — Tight-Parallel Drafting (Feature Provenance + ML Layer Architecture):**
Two fresh CC sessions draft Bible 4 and Bible 5 concurrently under the shared inheritance bundle (§ 2). Both sessions read identical upstream substrate. QB mediates diff exchange between in-flight drafts at the synchronization points specified in § 4.

**Phase B — Sequential Drafting (Model Evaluation):**
Bible 6 drafts after Bibles 4 AND 5 reach v1-draft stability. Bible 6 drafting CC inherits Bibles 4 and 5 in v1-draft form (not yet locked) plus the standard inheritance bundle.

### § 3.2 Rationale
Feature Provenance and ML Layer Architecture are bi-directionally substrate-coupled: features are model inputs; model topology determines feature relevance; calibration/bypass state in MLA is referenced by FP's train/inference duplication-or-divergence column. Tight parallel with mediated synchronization captures cross-information without serial blocking. Model Evaluation depends on stable substrate from both upstream bibles, hence sequential.

---

## § 4. SYNCHRONIZATION POINTS — CONCRETE (RATIFIED Q1 REFINEMENT)

Three synchronization points govern the Feature Provenance ↔ ML Layer Architecture parallel cycle. Synchronization points are not advisory — drafting CC sessions PAUSE at each point, emit synchronization artifacts to QB, and resume only after QB authorizes continuation. Concrete points eliminate ad-hoc QB judgment about exchange timing.

### § 4.1 Synchronization Point SP-1 — TOC + § 1 Scope
**Trigger:** Both drafting CC sessions complete Table of Contents and § 1 Scope of their respective bibles.
**Artifacts emitted to QB:** TOC + § 1 from both bibles.
**QB action:** Verify cross-reference shape compatibility. Specifically: section-numbering scheme alignment, scope-boundary disjointness, identifier conventions match between FP feature-references and MLA model-references.
**Resolution:** QB returns one of {CONTINUE, REVISE-FP, REVISE-MLA, REVISE-BOTH} with specific findings. CC sessions resume only on CONTINUE or after revision and re-emit.

### § 4.2 Synchronization Point SP-2 — § 4.1 Per-Entity Body
**Trigger:** Both drafting CC sessions complete § 4.1 (per-feature body for FP, per-model body for MLA) covering at least the first three entities in each.
**Artifacts emitted to QB:** § 4.1 first-three-entities from both bibles.
**QB action:** Verify train/inference column in FP § 4.1 reconciles with model input columns in MLA § 4.1. Specifically: every feature listed as a consuming-model-input in FP appears in the corresponding MLA model's input list; every MLA model input has a corresponding FP feature row; train/inference divergence flags in FP match calibration/bypass state in MLA where applicable.
**Resolution:** QB returns one of {CONTINUE, REVISE-FP, REVISE-MLA, REVISE-BOTH} with specific reconciliation findings. CC sessions resume only on CONTINUE or after revision and re-emit.

### § 4.3 Synchronization Point SP-3 — Pre-Model-Evaluation Gate
**Trigger:** Both Feature Provenance and ML Layer Architecture reach v1-draft-stable (drafting complete, all sections present, internal verification log emitted).
**Artifacts emitted to QB:** Full v1-draft of both bibles + verification logs.
**QB action:** Light surface review per Lesson § 4.9. Confirm v1-draft completeness and internal coherence. Authorize Phase B — Model Evaluation drafting.
**Resolution:** QB returns one of {AUTHORIZE-PHASE-B, REVISE-FP, REVISE-MLA, REVISE-BOTH}. Phase B begins only on AUTHORIZE-PHASE-B.

### § 4.4 Synchronization Discipline
- SP-1 and SP-2 are blocking for both drafting CC sessions. One session may not proceed past a synchronization point until the other reaches it.
- SP-3 is blocking for Bible 6 drafting initiation.
- All synchronization-point QB findings are surfaced to Tony for ratification before resolution issues to drafting CCs (per § 4.8 Tony ratification mediation).
- Synchronization-point QB findings that touch already-locked Phase 1 substrate (Architecture Overview v3, D&S Bible, Data Pipeline Bible) trigger UPSTREAM-CORRECTION per § 7.

---

## § 5. AUDIT GATE — CORPUS-LEVEL (RATIFIED Q2)

### § 5.1 Gate Specification
After all three bibles reach v1-draft stability (Phase B complete), a single corpus-level audit cycle runs.

**Audit-CC session:** Single fresh CC session reads all three v1-draft bibles + full inheritance bundle (§ 2). Audit-CC performs adversarial review per AUDIT_METHODOLOGY v2-patched, with explicit cross-bible cross-reference verification as a first-class audit dimension.

**Audit-CC scope:**
- Within-bible audit per AUDIT_METHODOLOGY for each of the three bibles
- Cross-bible cross-reference audit (Feature Provenance ↔ ML Layer Architecture ↔ Model Evaluation)
- Cross-bible cross-reference audit against Phase 1 locks (Architecture Overview v3, D&S Bible v1-patched-d2, Data Pipeline Bible v1-patched-c)

**QB action post-audit:** Synthesize findings across the three bibles into a unified findings document. Surface to Tony for ratification.

### § 5.2 Lock Order (RATIFIED Q2)
Sequential lock in dependency order:
1. Feature Provenance Bible
2. ML Layer Architecture Bible
3. Model Evaluation & Retraining Bible

Each bible locks via its own patch-CC session per § 4.12. QB does not invoke lock writes.

### § 5.3 Lock Versioning
First lock version: `v1` (no patch letter).
If audit-driven revision required before lock: `v1-patched-{a, b, c, …}` per § 7.3 monotonic letter naming.

---

## § 6. CROSS-REFERENCE FREEZE — POST-CORPUS-GATE (RATIFIED Q3)

### § 6.1 Freeze Rule
Cross-references between the three bibles in this cohort, AND cross-references from the three bibles to already-locked Phase 1 substrate, resolve at the corpus-audit gate (§ 5). Once Tony ratifies the post-audit findings synthesis and the sequential lock cycle begins, all cross-references are frozen across the three locks.

### § 6.2 Re-Open Path
The only path to re-open a frozen cross-reference is the UPSTREAM-CORRECTION cycle codified in § 7.

### § 6.3 Implication for Drafting CC Sessions
Drafting CC sessions in Phase A and Phase B (§ 3) work with un-frozen cross-references — synchronization points (§ 4) and corpus audit (§ 5) are the cross-reference resolution mechanisms. Freeze applies post-gate only.

---

## § 7. UPSTREAM-CORRECTION CANONICAL PATTERN (RATIFIED Q4)

Codifies the F.4 round-trip pattern observed in last session's Data Pipeline F.4 → D&S Bible v1-patched-d2 → Data Pipeline v1-patched-c cycle. Promoted to canonical pattern; applies to all future Phase 1+ bible cohorts.

### § 7.1 Trigger Condition (RATIFIED Q4 CLARIFICATION)
UPSTREAM-CORRECTION triggers when, and only when:
> An audit finding on bible A requires a fix that touches a locked bible B's substrate.

UPSTREAM-CORRECTION does NOT trigger when an audit finding on bible A is fixable within bible A's own scope. Within-bible-scope fixes are standard within-bible patches and follow the bible's own patch sequence — not the UPSTREAM-CORRECTION cycle.

The trigger phrase is **"fix touches a locked bible's substrate."** If the substrate of a locked bible must change to incorporate the finding, UPSTREAM-CORRECTION applies. If the locked bible can remain untouched, it does not.

### § 7.2 Cycle Steps
1. Audit on bible A surfaces finding requiring change in already-locked bible B.
2. QB surfaces upstream-change scope to Tony. Tony ratifies upstream-patch scope (Gate 1).
3. QB authors patch-spec for bible B as chat output.
4. Tony paste-routes to fresh patch-CC session (write-authorized per § 4.12). Patch-CC publishes B `vN-patched-{letter}`.
5. QB authors A re-incorporation patch-spec reflecting corrected B as chat output. Tony ratifies re-incorporation scope (Gate 2).
6. Tony paste-routes to fresh patch-CC session. Patch-CC publishes A `vM-patched-{letter}`.
7. Both new versions sit at lock together. UPSTREAM-CORRECTION cycle complete.

### § 7.3 Naming Convention
- `vN-patched-{a, b, c, …}` monotonic per bible.
- Letter sequences are independent across bibles (Bible A's `v1-patched-c` is unrelated to Bible B's `v1-patched-c`).
- Each letter increment corresponds to one ratified patch cycle, regardless of patch origin (within-bible patch vs UPSTREAM-CORRECTION downstream re-incorporation).

### § 7.4 Two-Gate Tony Ratification
- **Gate 1 (Upstream-Patch Scope):** Tony ratifies scope of change to bible B before patch-spec authorship.
- **Gate 2 (Downstream Re-Incorporation Scope):** Tony ratifies scope of A re-incorporation before A patch-spec authorship.
- Both gates are non-bypassable. QB does not unilaterally proceed from Gate 1 to Gate 2; each gate requires explicit Tony ratification.

### § 7.5 Write Discipline
- All patch writes execute in patch-CC sessions (write-authorized).
- QB does not invoke patch writes per § 4.12.
- QB authors patch-specs and patch-CC paste-prompts as chat output. Tony mediates paste-routing.

### § 7.6 Promotion to AUDIT_METHODOLOGY
This § 7 canonical pattern is codified here in the handoff document as immediate operative discipline, AND queued for promotion to AUDIT_METHODOLOGY at the next AUDIT_METHODOLOGY patch cycle. Promotion target: AUDIT_METHODOLOGY § 5 (new section, "UPSTREAM-CORRECTION Canonical Pattern").

### § 7.7 Applicability
Applies to all future Phase 1+ bible cohorts, not just deliverables 4-5-6. Future cohort handoff documents inherit § 7 by reference rather than restating.

---

## § 8. OPEN ITEMS CARRY-FORWARD

The following items are tracked but NOT in scope for this cohort:

| Item | Disposition |
|------|-------------|
| Data Pipeline Bible § 8.W.2 disposition (collapse-or-stand + Bug #N assignment) | Deferred to Phase 5.3.1 fix-time substrate verification |
| equine-ingestion Lambda broken-container-image (CodeArtifactUserFailedException) | Phase 5.X scope; broader than simple Inactive flag |
| Data Pipeline Bible B3 + B5 cosmetic items | Phase 1 cleanup-cycle backlog |
| D&S Bible § 4.1.15 PK/FK/INDEX re-verification | Next credential-authorized cycle |

---

## § 9. PHASE 1 META-CYCLE RATIFICATIONS DEFERRED

The following meta-cycle ratifications are pending and do NOT block this cohort:

| Item | Status |
|------|--------|
| `database_schema_bible:V1-12` cross-reference convention | Deferred ratification |
| QB grep-predicate authoring discipline (3 occurrences last session) | Deferred ratification |
| Verbatim-paste-discipline verlog-growth modeling | Deferred ratification |

---

## § 10. WORKFLOW RECAP — COHORT CYCLE

For operational reference, the cohort cycle proceeds:

1. **(this document)** QB authors handoff. Tony paste-routes to write-authorized CC. CC writes handoff to disk.
2. QB authors drafting specs for Bibles 4 and 5 as chat output.
3. QB authors drafting CC paste-prompts for Bibles 4 and 5 as chat output.
4. Tony paste-routes drafting prompts to TWO fresh CC sessions in parallel. Drafting begins.
5. **SP-1 reached** (§ 4.1). Drafting CCs emit TOC + § 1 to Tony. Tony forwards to QB. QB returns resolution. Drafting resumes per resolution.
6. **SP-2 reached** (§ 4.2). Same exchange pattern. Drafting resumes per resolution.
7. **Both bibles reach v1-draft.** SP-3 reached (§ 4.3). QB authorizes Phase B.
8. QB authors drafting spec for Bible 6 as chat output. QB authors drafting CC paste-prompt.
9. Tony paste-routes to fresh CC. Bible 6 drafts.
10. **All three bibles at v1-draft.** QB authors corpus-level audit-CC paste-prompt as chat output.
11. Tony paste-routes to fresh audit-CC. Audit-CC adversarially reviews all three bibles + cross-bible cross-references.
12. QB synthesizes audit findings, surfaces to Tony for ratification.
13. Tony ratifies findings synthesis.
14. QB authors lock specs / patch specs as appropriate, in dependency order (Feature Provenance → ML Layer Architecture → Model Evaluation).
15. Tony paste-routes to patch-CC sessions. Sequential locks publish.
16. Cross-references freeze (§ 6).
17. Cohort complete. Phase 1 deliverables 4-5-6 LOCKED.

If at any step an audit finding triggers § 7.1 condition ("fix touches a locked bible's substrate"), UPSTREAM-CORRECTION cycle (§ 7) executes before the lock cycle resumes.

---

## § 11. WRITE DISCIPLINE REMINDER

QB does not invoke MCP write tools (write_file, edit_file, create_file, move_file, create_directory) under any circumstances per § 4.12. All disk operations execute in CC sessions (drafting CC, patch CC, audit CC, lock CC) authorized for write. Tony mediates all paste-routing. This handoff document itself is QB chat output; its disk-write executes in a fresh CC session per the spec-write CC paste-prompt accompanying this handoff.

---

**END HANDOFF DOCUMENT**
