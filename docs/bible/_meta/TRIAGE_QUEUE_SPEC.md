# TRIAGE_QUEUE_SPEC.md

**Document:** TRIAGE_QUEUE_SPEC
**Phase:** 0 (Methodology) — Phase 0 deliverable 5 of 5
**Status:** DRAFT v1 (pre-audit)
**Author:** CC (drafting under verification discipline; QB orchestrated and reviewed)
**Date:** 2026-05-04
**Locked:** [pending audit + Tony review + iteration cycles]

**Revision history:**
- v1 (2026-05-04): initial CC draft. Tier 3 per Tony's locked Q2; companion verification log at `_audits/TRIAGE_QUEUE_SPEC_v1_verification.md`.

**Tier:** 3 per META_PLAN v6 § 4.1 + § 6.5. CC-drafted under QB spec; companion verification log required; CC-audited.

**Anchored on:** META_PLAN v6 (locked 2026-05-04), BIBLE_STRUCTURE_SPEC v3 (locked 2026-05-04), AUDIT_METHODOLOGY v2 (locked 2026-05-04), CONVERGENCE_CRITERIA v2 (locked 2026-05-04). Section references throughout this document point to v6 / v3 / v2 / v2 § numbers.

**Methodology-interpolation rule (operative per META_PLAN v6 § 6.1, with v6's expanded scope, grandfathering clause, and pattern-completion check):** This draft does not invent binary tests, cadence rules, completeness criteria, scoring rubrics, severity thresholds, iteration caps, percentage criteria, procedural sequencing rules, or other CC-prescribed methodology constructs Tony has not explicitly ratified. Severity inheritance from META_PLAN v6 § 11 is verbatim; no new severities introduced. v1 surfacing notes in § 11.

**Recursive precision discipline (per Tony's Q3 v1 cycle ratification):** v1 is the third-instance test for the recursive precision pattern (formatting-fidelity-when-claiming-verbatim). Every verbatim claim in v1 reproduces source character-exact INCLUDING formatting (markdown bold, code spans, line breaks, list structure, em-dashes, quotation marks).

---

## 1. Motivation

### 1.1 Why this document exists

TRIAGE_QUEUE_SPEC.md is the fifth and final Phase 0 methodology deliverable. Its job is to specify the format for triage queue entries — the per-entry schema that audit findings adopt when they transfer from audit reports into the active triage queue.

Four prior Phase 0 documents reference this format:

- **META_PLAN v6 § 4.3:** `PHASE_5_BACKLOG.md` table row reads "Cleanup queue work scheduled for Phase 5. Continuously updated through Phase 4. **Format defined by TRIAGE_QUEUE_SPEC.md** (Phase 0 deliverable 5), which therefore must be locked before PHASE_5_BACKLOG.md is created."
- **META_PLAN v6 § 7.8:** "When findings emerge during Phase 1+ audits that aren't addressed inline, they go to `PHASE_5_BACKLOG.md` per the format defined in `TRIAGE_QUEUE_SPEC.md`."
- **META_PLAN v6 § 8.2:** "Every finding from Phase 1+ audits goes to `PHASE_5_BACKLOG.md` in TRIAGE_QUEUE_SPEC.md format. Severity-tagged. Dependency-tracked. Phase-scheduled."
- **META_PLAN v6 Appendix A.5:** Worked-example Bug #28 triage entry that grounds the format. § 7.1 of this document reproduces the worked example character-exact.

Two additional Phase 0 documents produce queue entries:

- **AUDIT_METHODOLOGY v2 § 3:** Phase 1 audit cycle — non-resolved findings transfer to triage queue per this format.
- **CONVERGENCE_CRITERIA v2 § 6.2:** per-bible revision triggers — failing convergence-test workflows produce queue entries identifying which bibles need revision.

TRIAGE_QUEUE_SPEC discharges the format-definition deferral inherited from these documents.

### 1.2 Why entries need a defined format

The triage queue is the bridge between audit findings (transient artifacts of audit cycles) and operational work (deferred resolution scheduled across phases). Without a defined format:

- Cross-cycle entries diverge in structure, making queue-level analysis (severity tally; dependency mapping; phase-schedule view) hard.
- Different audit-CC sessions produce structurally different findings, defeating the audit cycle's reproducibility.
- The transfer to `PHASE_5_BACKLOG.md` (see § 4.3) becomes a manual restructuring rather than a routing operation.

The format is the queue's discipline. TRIAGE_QUEUE_SPEC defines it.

### 1.3 What this document inherits from prior cycles

- **Severity taxonomy:** META_PLAN v6 § 11 verbatim. BLOCKER / MATERIAL / MINOR / STYLE. No new severities introduced; no severity boundary thresholds beyond what § 11 already specifies.
- **Cross-cutting bug rule:** BIBLE_STRUCTURE_SPEC v3 § 5.3. The triage queue does NOT track cross-cutting-bug canonical-home assignments — that's the bibles' mechanism. Triage queue entries are at the audit-finding level; canonical-home lives in the bible.
- **Audit cycle workflow:** META_PLAN v6 § 3.1 + AUDIT_METHODOLOGY v2 § 3.1 (per-bible cycle) + § 3.2 (cross-document audit). Queue entry creation is downstream of audit synthesis.
- **Verification-log precision rule:** META_PLAN v6 § 6.5. Applies to verification log entries for v1's factual claims about Bug #28 / Bug #15 / Bug #24.

Phase 0 documents reference these mechanisms; they do not duplicate the rules.

---

## 2. Scope

### 2.1 What this document specifies

- **Triage queue entry format** (§ 3).
- **Queue lifecycle** — creation, update, transfer to `PHASE_5_BACKLOG.md` (§ 4).
- **Severity tagging and inline-vs-queue boundary** (§ 5).
- **Phase scheduling discipline** — "Phase X.Y" placeholder mechanism (§ 6).
- **Three worked examples** demonstrating the format on real EE bugs (§ 7).

### 2.2 What this document does NOT specify

Per Tony's locked Q1 in v1 cycle, scope is Phase 1+ audit findings only. Not in scope:

- **Phase 0 audit-cycle finding tracking.** Phase 0 audits already operate without a queue — findings resolve within cycle per META_PLAN v6 § 11's threshold (< 5 MATERIAL ∧ zero fabricated ∧ zero methodology-interpolation). Codifying a queue for Phase 0 would be redundant; the cycle already converges per the threshold.
- **Cross-cutting bug tracking.** BIBLE_STRUCTURE_SPEC v3 § 5.3 specifies canonical-home + cross-references for cross-cutting bugs at the bible-corpus level. Triage queue tracking would create triple bookkeeping (bible canonical home + bible cross-references + queue entry) and risks state divergence. The triage queue tracks a finding; the bibles track the prevention.
- **Phase 5 backlog mechanism.** `PHASE_5_BACKLOG.md` is Phase 5's deferred-work tracker. The triage queue feeds into it via explicit transfer (§ 4.3); the file's internal organization is Phase 5's concern, governed by the entry format this document specifies but not by additional discipline this document codifies.
- **Per-bible audit threshold.** Inherited from META_PLAN v6 § 11; not revised here.
- **Audit synthesis discipline.** Specified in AUDIT_METHODOLOGY v2 § 3; queue entry creation is downstream.

### 2.3 Authority chain

Per META_PLAN v6 § 4.1, TRIAGE_QUEUE_SPEC is Tier 3 (CC-drafted with companion verification log). Per Tony's locked Q1 in v1 cycle, scope is Phase 1+ audit findings. Per Tony's locked Q2, real EE bugs (Bug #28, Bug #15, Bug #24) anchor the canonical worked examples.

---

## 3. Queue Entry Format

Each triage queue entry is a structured block with the fields below. The format is text-based (markdown-renderable) per the META_PLAN v6 Appendix A.5 worked-example pattern; structured-data alternatives (JSON / YAML) are deferred to Phase 5 working agreements per META_PLAN v6 § 7.13's deferral pattern.

### 3.1 Mandatory fields

**Phase number** — placeholder format `Phase X.Y[.Z]` per META_PLAN v6 Appendix A.5's worked-example notation. X is the phase (5 for Phase 5 backlog), Y is the sub-phase, Z is the entry sequence within the sub-phase. Real numbering is operator-assigned post-Phase-0; until then, placeholders preserve the format.

**Title** — short descriptor of the finding. Less than one line. Names the bug or finding by short identifier (e.g., "HRN Scraper Bug #28 (column shift)").

**Severity** — one of BLOCKER / MATERIAL / MINOR / STYLE per META_PLAN v6 § 11. The severity reflects the finding at audit-time; severity does not change via queue updates (severity is fixed at finding creation; if reassessment is needed, a new finding entry is created cross-referencing the original).

**Surfaced** — date the finding was first identified, plus the cycle / audit-CC / Phase 1 bible that surfaced it. Format: `<YYYY-MM-DD> (during <surfacing-context>)` per META_PLAN v6 Appendix A.5's pattern.

**Stable-known classification** — applies for bug entries (i.e., findings that document operational defects, not methodology gaps). Values: `provisional` / `stable` / `not-stable` per META_PLAN v6 § 8.1. The classification governs whether the § 8.1 observation-only exception logic applies.

**Manifestation** — how the finding presents in the system. For bugs: DB row symptoms, log signatures, downstream model degradation. For methodology findings: which document section, what content gap. Bullet list or paragraph form.

**Root cause** — what produced the finding. For bugs: code path with file:line reference. For methodology findings: the locked content's misalignment with subsequent verification.

**Dependencies** — entries this entry blocks or is blocked by. Bullet list with cross-references. Format: `Blocks: <entry-id-list>`, `Blocked by: <entry-id-list>`. If no dependencies, state "No dependencies at entry creation."

**Disposition** — phase number where resolution is scheduled. Format: `Fix in Phase X.Y` or `Defer to Phase 5.X.Y`. The disposition is the operator's commitment about when the finding gets resolution work; the actual phase numbering is placeholder until real numbering exists.

**Bible references on resolution** — what bible documents update when the finding is resolved. Bullet list. Format: cross-references per BIBLE_STRUCTURE_SPEC v3 § 7.1 syntax (`<bible>:<section>`).

### 3.2 Conditional fields

**Rollback** — applicable when the finding's resolution involves code or schema changes. Documents what happens if the resolution introduces regression. Format: prose. May read "Standard git revert" or "DB rollback required" or "Non-reversible because <reason>" per the migration discipline in META_PLAN v6 § 7.12.

**Re-classification trigger** — applicable when the stable-known classification is `provisional`. Documents what verification fires the qualifier-drop. Format: prose with cross-reference to the verification trigger.

**Cross-cutting note** — applicable when the finding spans multiple bibles. The triage queue does NOT track cross-cutting canonical-home assignments (per BIBLE_STRUCTURE_SPEC v3 § 5.3); the cross-cutting note documents the bibles affected and points to the bible-level canonical-home entry. The audit finding lives at the queue level; the prevention discipline lives at the bible level.

**Audit-cycle reference** — applicable when the finding traces to a specific audit cycle. Format: `<doc>_v<N>_audit.md § <finding-id>` per META_PLAN v6 § 3.8 audit subdirectory naming convention.

**Operator-verified external source** — applicable when the finding's manifestation references operator-verified external sources (e.g., operator memory files outside the EE codebase). Format: verbatim quote inline per AUDIT_METHODOLOGY v2 § 4.4 operator-verified external source pattern. Includes source location identifier.

### 3.3 Field ordering convention

The mandatory fields appear in the order: Phase number, Title (combined as a header line), Severity, Surfaced, Stable-known classification (for bug entries), Manifestation, Root cause, Dependencies, Disposition, Rollback (if applicable), Bible references on resolution.

Conditional fields (re-classification trigger; cross-cutting note; audit-cycle reference; operator-verified external source) appear after the mandatory fields, before Bible references on resolution.

The convention follows META_PLAN v6 Appendix A.5's worked-example structure. Future entries follow the same ordering for queue-level analyzability.

---

## 4. Queue Lifecycle

### 4.1 Entry creation

A triage queue entry is created when an audit finding is not resolved within its audit cycle.

**Workflow per AUDIT_METHODOLOGY v2 § 3.1:**

1. Audit-CC produces findings in audit report format at `/docs/bible/_audit/<doc>_v<N>_audit.md`.
2. QB synthesizes findings.
3. Findings that resolve within the audit cycle (revise the draft; re-audit; lock) do NOT become queue entries. The audit report records them; the cycle closes.
4. Findings that do NOT resolve within the audit cycle (deferred to a later phase; or surfacing operational defects rather than methodology issues) transfer to triage queue entries.

**Transfer trigger:** the finding is documented in an audit report; QB's synthesis defers resolution to a later phase OR identifies the finding as operational rather than methodology-correctable. At that point, QB authors a queue entry per § 3 format.

**Inline-resolved finding boundary:** a finding is "inline-resolved" when its resolution is a draft revision in the same audit cycle. Specifically (per META_PLAN v6 § 11's threshold pattern):

- Surgical document revisions (text edits, formatting fixes, cross-reference corrections) that the audit-CC's recommendation specifies → inline-resolved; revised draft re-audits; cycle closes; no queue entry.
- Operational defects (bugs in the EE codebase; live-state-vs-bible-content drift) that audit-CC surfaces → not inline-resolved (audit cycles don't fix the codebase); queue entry created.
- Methodology questions Tony decides architecturally → handled per META_PLAN v6 § 6.3 architectural-authority discipline (Tony decides; QB executes); whether the resolution becomes a queue entry depends on whether the resolution is a draft revision (inline) or an operational change (queue entry).

The boundary is not graduated. Each finding is one of: inline-resolved → no queue entry; OR not-inline-resolved → queue entry. The boundary follows from META_PLAN v6 § 8.1 ("findings are not lost. findings are not silently fixed. findings accumulate until Phase 5 schedules them"); the queue is the accumulation.

### 4.2 Entry update

Queue entry updates change status, dependencies, or disposition. Severity does NOT change via update (per § 3.1's note: severity is fixed at finding creation).

**Status values:**

- `open` — the entry is in the queue, awaiting resolution.
- `in-progress` — resolution work has started in the entry's disposed phase.
- `blocked` — resolution is paused pending resolution of a blocking entry (per Dependencies field).
- `resolved` — resolution work completed; bible references on resolution updated.

Status transitions: `open` → `in-progress` → (`blocked` ↔ `in-progress`) → `resolved`.

**Update authority:** QB updates entries during normal phase work. Tony reviews entries in PHASE_5_BACKLOG.md form (post-transfer per § 4.3) for scheduling and architectural calls. Audit-CC sessions do not update entries; audit-CCs produce findings, which become entries via QB synthesis.

**Update discipline:**

- Status changes are dated in the entry (parenthetical "Updated YYYY-MM-DD" appended).
- Dependency changes update the Blocks / Blocked-by lists; if a blocking entry resolves, the blocked entry's status returns to `open` or `in-progress`.
- Disposition changes are explicit (entry's Disposition field updates with a dated note). Disposition is not silently re-assigned across phases.

### 4.3 Transfer to PHASE_5_BACKLOG.md

A triage queue entry transfers to `PHASE_5_BACKLOG.md` when the operator explicitly defers the entry to Phase 5.

**Trigger:** operator decision. Tony reviews queue entries periodically (cadence is a Phase 5 working-agreement decision per META_PLAN v6 § 7.13's deferral pattern); for entries Tony defers to Phase 5, an explicit transfer occurs.

**Mechanism:** the entry is moved (not copied) from the active triage queue to `PHASE_5_BACKLOG.md`. The transfer is explicit to prevent silent state changes; the queue's invariant is "entries are either active or transferred, not both."

**Transfer-time updates:**

- The entry's Disposition field updates from "Defer to Phase 5.X.Y" (active queue's deferral marker) to "Phase 5.X.Y" (Phase 5 backlog's scheduled marker), with the actual phase number assigned (placeholder X.Y filled when real Phase 5 numbering exists).
- A dated transfer note is appended ("Transferred to PHASE_5_BACKLOG.md on YYYY-MM-DD").
- The entry retains its identifier across transfer (no renumbering).

**Reverse transfer:** an entry can return from `PHASE_5_BACKLOG.md` to the active triage queue if the operator decides to escalate (e.g., the bug becomes unbounded and requires immediate attention per META_PLAN v6 § 8.1's exception logic). Reverse transfer is rare; documented with the same dated-note discipline.

The dependency between TRIAGE_QUEUE_SPEC and `PHASE_5_BACKLOG.md` is uni-directional at format level: this document defines the entry format; `PHASE_5_BACKLOG.md` adopts it. `PHASE_5_BACKLOG.md`'s internal organization (sectioning, prioritization, scheduling) is Phase 5's concern.

---

## 5. Severity Tagging and Boundary Discipline

### 5.1 Severity inheritance from META_PLAN v6 § 11

The triage queue's severity values inherit verbatim from META_PLAN v6 § 11. No new severities are introduced by this document.

The severity values:

- **BLOCKER** — fabricated content; lock-blocker per Tony's threshold per META_PLAN v6 § 11.
- **METHODOLOGY-INTERPOLATION** — CC-introduced or QB-introduced methodology Tony hasn't ratified; lock-blocker per Tony's hard rule regardless of MATERIAL count per META_PLAN v6 § 6.1.
- **MATERIAL** — structural issue affecting load-bearing function (methodology coherence; factual accuracy at scale; cross-reference integrity).
- **MINOR** — localized issue, individually small.
- **STYLE** — language polish, presentation choice.

The severity assigned at audit time fixes the entry's severity. Severity does not change via update; if reassessment is needed, a new entry is created cross-referencing the original.

### 5.2 Inline-vs-queue boundary

Not every audit finding becomes a queue entry. The boundary is per § 4.1:

- Surgical document revisions resolve inline (within audit cycle).
- Operational defects surface to queue.
- Methodology questions handled per Tony's architectural discipline.

**The boundary is per finding, not per severity.** A MINOR finding can be inline-resolved (text edit) or queue-bound (operational). A MATERIAL finding can be inline-resolved (load-bearing structural issue with surgical revision) or queue-bound (operational defect requiring code work).

Severity governs Tony's lock threshold per META_PLAN v6 § 11; the inline-vs-queue boundary governs which findings transfer from audit cycles to operational tracking. The two disciplines operate independently.

### 5.3 Phase 0 boundary special case

Phase 0 audits operate without a triage queue per this document's § 2.2 scope statement and Tony's locked Q1 v1 cycle ratification. Phase 0 findings resolve within cycle per META_PLAN v6 § 11's threshold; the triage queue does not exist as a Phase 0 mechanism.

This is not a contradiction with § 5.2's "boundary is per finding, not per severity" — Phase 0 findings have a different audit substrate (methodology documents, not Phase 1 bibles or operational EE state). Phase 0 cycles have empirically converged (per META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 / AUDIT_METHODOLOGY v2 / CONVERGENCE_CRITERIA v2 lock cycles); the queue mechanism is for Phase 1+ where audit volume and operational defect surface area both increase.

---

## 6. Phase Scheduling

Per META_PLAN v6 Appendix A.5's worked-example notation, queue entries use placeholder phase numbers:

- `Phase 5.X.Y` — Phase 5 sub-phase placeholder; X.Y assigned when real Phase 5 numbering exists (post-Phase-0 lock; PHASE_5_BACKLOG.md created per META_PLAN v6 § 8.2 with Bug #28 as first entry).
- `Phase 5.3.1` — example numbered phase per Appendix A.5's Bug #28 worked example.

The placeholder discipline:

- Real numbering is operator-assigned. QB does not assign final phase numbers; QB writes placeholders.
- When real numbering is assigned, queue entries update via § 4.2 entry update discipline (dated note + Disposition field update).
- Cross-references to phase numbers in bibles or other documents use the same placeholder convention. When real numbering is assigned, the cross-references update across the corpus.

Phase number stability: once assigned, phase numbers are stable across the entry's lifetime (renumbering breaks cross-references in bibles).

---

## 7. Worked Examples

### 7.1 Bug #28 — single-bug entry (canonical from META_PLAN v6 Appendix A.5)

The worked example below reproduces META_PLAN v6 Appendix A.5 character-exact, with the operator memory file's verbatim symptom statement preserved per META_PLAN v6 verification log Claim 15c. The example demonstrates the mandatory fields + the conditional `Re-classification trigger` and `Operator-verified external source` fields (the latter via the verbatim memory file quote in Manifestation).

**Reproduction of META_PLAN v6 Appendix A.5:**

```
Phase 5.3.1: HRN Scraper Bug #28 (column shift)

Severity: HIGH (silent data loss; affects all win/DD payouts since 2026-04-30)
Surfaced: 2026-05-03 (during EE_CURRENT_STATE_DUMP generation; per operator
memory file equine-equalizer-bug-28-hrn-scraper.md, the regression was sharp —
2026-04-29 last clean day at 9/10 win-payout success; 2026-04-30 onward all 0/N)

Stable-known classification: provisional. Backfill-feasibility AND DD-pool-extraction
bounded-loss assumptions both pending Phase 1 Data Pipeline Bible audit verification
(per § 8.1).

Root cause: HRN page structure changed circa 2026-04-30 (likely added an icon
column to the payouts table). The parse_payout(N) calls at
backend/services/data_sources/hrn_scraper.py:802-804 (verified) use positional
cell indexing that has been off-by-one ever since.

Manifestation:
  - win_payout is NULL across all results rows from 2026-04-30 onward
  - daily_double_payout is NULL across same range
  - place_payout stores values that should be in win_payout
  - show_payout stores values that should be in place_payout
  - Place, show, and exacta payouts still populate per operator memory file's
    symptom statement
  - DD pool extraction at hrn_scraper.py:814 flagged as "likely has the same
    root cause" — distinct code path from daily_double_payout result-dict
    field; Phase 1 verifies bounded-loss status

Dependencies:
  - Resolution requires HRN page-structure verification (manual: visit a results
    page, confirm column structure)
  - May require parser refactor if HRN structure is now variable-by-page-type
  - Requires backfill of affected results rows after fix deploys (feasibility
    assumed; Phase 1 verifies)
  - DD pool extraction status verification (Phase 1 audit's job)

Disposition: Fix in Phase 5.3 before any Phase 5 work that depends on payout data.

Rollback: Standard git revert if fix introduces regression. No DB rollback needed
(fix re-populates rows that are currently NULL).

Bible references on resolution:
  - Update data_pipeline_bible.md § 7.9 (HRN scraper documentation)
  - Add data_pipeline_bible.md W.N (What Was Fixed entry)
  - Consider new Forbidden Pattern: positional column indexing in scrapers
    without column-header verification
```

**Note on severity classification:** META_PLAN v6 Appendix A.5 uses `Severity: HIGH` rather than the formal severity taxonomy (BLOCKER / MATERIAL / MINOR / STYLE) inherited from § 11. The Appendix A.5 example pre-dates this document's § 5.1 severity inheritance; HIGH is the operator's intuitive classification at the time of authorship. Per § 5.1, future queue entries use the inherited taxonomy. The Appendix A.5 reproduction here preserves the source's severity label (HIGH) per the verbatim discipline; subsequent worked examples (§ 7.2, § 7.3) use the inherited taxonomy.

**Operator-verified external source — Bug #28 memory file verbatim:**

Per META_PLAN v6 verification log Claim 15c, the operator memory file `equine-equalizer-bug-28-hrn-scraper.md` contains the following verbatim passages (reproduced character-exact INCLUDING formatting):

Symptom block (lines 9-10 of memory file):

> "starting 2026-04-30, all results.win_payout and results.daily_double_payout rows are NULL across every track/race scraped via HRN. Place, show, and exacta payouts still populate."

DD pool extraction note (line 30 of memory file):

> "DD pool extraction (hrn_scraper.py:814 'pool' table loop) likely has the same root cause — same site-wide column shift."

The verbatim quotes ground the Manifestation field's "Place, show, and exacta payouts still populate per operator memory file's symptom statement" and "DD pool extraction at hrn_scraper.py:814 flagged as 'likely has the same root cause'" claims. Future Bug #28-related queue updates preserve the verbatim source location (memory file path + line numbers) per the operator-verified external source pattern (AUDIT_METHODOLOGY v2 § 4.4).

### 7.2 Bug #15 — cross-cutting bug entry

Bug #15 is the train/inference feature engineering drift between `model/shared/data_loader.py` (training) and `backend/services/feature_engineering_service.py` (inference). Per META_PLAN v6 § 9.11, the drift produced three calibration bugs in one week (early April 2026). The bug spans multiple bibles — Feature Provenance (canonical home per BIBLE_STRUCTURE_SPEC v3 § 5.3 because the prevention is a feature-engineering pattern) AND ML Layer Architecture (cross-references the canonical home via the calibration bypass discussion).

**The triage queue entry tracks the audit finding, not the cross-cutting canonical-home assignment.** Per § 3.2's `Cross-cutting note` field discipline: the queue entry documents the bibles affected and points to the bible-level canonical-home entry. The bibles' `What Was Fixed` sections track the prevention; the queue tracks the resolution work.

**Worked example:**

```
Phase 5.X.Y: Bug #15 — Train/inference feature engineering drift

Severity: MATERIAL
Surfaced: 2026-04-22 (during gonzo_features extraction work — operator
identified the recurrence pattern across three calibration bugs in one week
per gonzo_features.py:7-11 docstring institutional-memory comment)

Stable-known classification: stable (the drift is a structural reality the
bible documents; the bugs it produced are individually tracked per the
bibles' What Was Fixed sections).

Manifestation:
  - 14 Gonzo Sauce features factored to model/shared/gonzo_features.py
    (Speed (4) + Trajectory (7) + Class (3) = 14 features per gonzo_features.py
    docstring lines 1-28); single shared module prevents drift for that subset
  - Remaining base features still implemented in two parallel locations:
    model/shared/data_loader.py (training) and
    backend/services/feature_engineering_service.py (inference)
  - Manual cross-reference review is the discipline keeping the parallel
    implementations in sync; structural reality, not enforced by code

Root cause: parallel feature engineering implementations; defaults differed,
edge-case handling differed, par-time computation differed in subtle ways
(per META_PLAN v6 § 9.11 description).

Dependencies:
  - Gonzo subset extraction completed 2026-04-22 (closed for the 14
    Gonzo Sauce features only)
  - Remaining base feature extraction is Phase 5.X.Y deferred work
  - Bug #24 calibration bypass downstream of Bug #15 (cross-cutting note
    below)

Disposition: Defer to Phase 5.X.Y for remaining base feature extraction
to a single shared module. The 14 Gonzo Sauce features are already factored
(closed). Remaining base features keep manual-cross-reference discipline
until Phase 5 extraction.

Cross-cutting note:
  - Canonical "What Was Fixed" home per BIBLE_STRUCTURE_SPEC v3 § 5.3:
    feature_provenance_bible.md (prevention discipline is feature-engineering
    pattern). Cross-references from ml_layer_architecture_bible.md and
    model_evaluation_retraining_bible.md.
  - Triage queue tracks the audit-finding-level resolution work.
  - The bible canonical-home entry tracks the prevention discipline.
  - The two disciplines operate independently; the queue entry does NOT
    duplicate the bible's What Was Fixed entry.

Bible references on resolution:
  - Update feature_provenance_bible.md § 4.1 (per-feature provenance) for
    each feature extracted to shared module
  - Update feature_provenance_bible.md § 8.W.<n> (canonical home; existing
    entry for the gonzo extraction; add entry for remaining base extraction
    when complete)
  - Cross-reference updates in ml_layer_architecture_bible.md § 8 and
    model_evaluation_retraining_bible.md § 8
```

### 7.3 Bug #24 — chain bug entry (downstream of Bug #15)

Bug #24 is the calibration bypass at `backend/services/wr_inference_service.py:616-626`. Per META_PLAN v6 § 9.12, the bypass was introduced as a workaround for the chain Bug #15 (train/inference FE drift) → Bug #24 (calibrated 0-PP horse override misranks). The chain creates a dependency: Bug #24's resolution depends on Bug #15's resolution (since re-enabling calibration without first fixing the FE drift would re-introduce Bug #24's misranking).

**The triage queue entry tracks the chain dependency in the Dependencies field.** The format demonstrates how dependency tracking works for chain bugs.

**Worked example:**

```
Phase 5.X.Y: Bug #24 — Calibration bypass at WR inference

Severity: MATERIAL
Surfaced: ~2026-04 (during the gonzo_sauce calibration work that produced
the chain Bug #15 → Bug #24)

Stable-known classification: stable (the bypass is currently in effect; not
unbounded loss).

Manifestation:
  - All WR inference styles bypass calibration at
    backend/services/wr_inference_service.py:616-626 (verified: comment
    block at lines 616-625 reads "All styles (including gonzo_sauce) bypass
    calibration at inference tonight"; bypass operation
    handicapping_probs = ranker_probs.copy() at line 626)
  - Calibration sidecars exist in S3 for gonzo_sauce ranker output but
    are not loaded
  - When isotonic calibration was applied, legitimate-PP horses' calibrated
    probabilities were clipped to ~0; the 1/field_size override for 0-PP
    horses dominated; 0-PP horses ranked at #1

Root cause: chain Bug #15 → Bug #24. The 0-PP override interaction with
calibration (Bug #24) produced misranking at the model output level;
fixing Bug #24 alone (re-enabling calibration without first fixing Bug #15
upstream) would re-introduce Bug #24's misranking.

Dependencies:
  - Blocked by: Bug #15 — Train/inference feature engineering drift
    (remaining base feature extraction; tracked at Phase 5.X.Y per § 7.2)
  - Resolution path: fix Bug #15 root cause first (FE single-source
    extraction for remaining base features), then Bug #24 (0-PP override
    interaction with calibration). Calibration re-enabled after both fixes
    deploy and are validated.

Disposition: Defer to Phase 5.X.Y, after Bug #15 resolution.

Cross-cutting note:
  - Canonical "What Was Fixed" home per BIBLE_STRUCTURE_SPEC v3 § 5.3:
    model_evaluation_retraining_bible.md (prevention discipline is
    calibration-applied-as-process). Cross-references from
    ml_layer_architecture_bible.md.
  - The chain Bug #15 → Bug #24 is documented at both bibles' relevant
    sections; the bibles document the prevention discipline.

Bible references on resolution:
  - Update ml_layer_architecture_bible.md § 4.3 (calibration / bypass state)
  - Update model_evaluation_retraining_bible.md § 4.2 (calibration discipline
    as process)
  - Add model_evaluation_retraining_bible.md § 8.W.<n> (What Was Fixed entry
    for Bug #24, canonical home per § 5.3)
  - Cross-reference from ml_layer_architecture_bible.md § 8

Rollback: Standard git revert if fix introduces regression. Calibration
re-enable should be validated against held-out test data before lock.
```

### 7.4 Worked example summary

The three worked examples demonstrate three patterns:

- **§ 7.1 Bug #28** — single-bug entry; all mandatory fields populated; conditional `Re-classification trigger` (provisional stable-known) and `Operator-verified external source` (memory file verbatim) demonstrated.
- **§ 7.2 Bug #15** — cross-cutting bug entry; the `Cross-cutting note` field demonstrates the BIBLE_STRUCTURE_SPEC v3 § 5.3 distinction (queue entry tracks audit finding; bible canonical home tracks prevention).
- **§ 7.3 Bug #24** — chain bug entry; the `Dependencies` field's `Blocked by` formulation demonstrates dependency tracking for chains.

Future queue entries (Phase 1+ audit findings) follow these patterns. The format is operationally tested against three real EE bugs whose substrate is verified per the v1 verification log.

---

## 8. Open Questions

Surfaced for resolution during Phase 0 iteration. Not blocking TRIAGE_QUEUE_SPEC lock unless audit returns one as critical.

### 8.1 Structured-data alternatives (JSON / YAML)

§ 3 specifies text-based markdown-renderable format per Appendix A.5's worked-example pattern. Whether structured-data alternatives (JSON / YAML for queue-level analysis) should be adopted is a Phase 5 working-agreement decision per META_PLAN v6 § 7.13's deferral pattern. Until then, text format suffices.

### 8.2 Update cadence for entry status

§ 4.2 specifies status transitions but does not specify a cadence (how frequently QB reviews active entries; how Tony's review interval is scheduled). Cadence specification is deferred to Phase 5 working agreements per the same § 7.13 pattern.

### 8.3 Reverse transfer threshold (PHASE_5_BACKLOG.md → active queue)

§ 4.3 specifies reverse transfer is rare. The threshold for "rare" — whether reverse transfer triggers an architectural review (per META_PLAN v6 § 7.10's emergency-deploy pattern of "two within 7 days triggers review") or remains operator-judgment — is not specified here. Deferred to Phase 5 working agreements.

---

## 9. Lock Status

**Document status:** DRAFT v1, pre-audit
**Audit-CC pass:** pending (v1 audit pending after disk write)
**Verification log:** `_audits/TRIAGE_QUEUE_SPEC_v1_verification.md` — covers cross-references to META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 / AUDIT_METHODOLOGY v2 / CONVERGENCE_CRITERIA v2 sections + Bug #28 / #15 / #24 facts + memory file verbatim quotes
**Tony review:** pending (will see post-audit version per workflow discipline)
**Locked:** [pending]

**Phase 0 prerequisites carried over from META_PLAN v6 § 11:**
- All 5 Phase 0 documents pass adversarial audit (Tony's threshold: < 5 MATERIAL findings AND zero fabricated-content findings AND zero methodology-interpolation findings)
- Operating-model convergence test passes (META_PLAN v6 § 5.4)
- EE production code committed to baseline (META_PLAN v6 § 3.1.1)
- `.gitignore` baseline audit performed; findings documented at `_audits/gitignore_baseline_audit.md` (META_PLAN v6 § 7.14)
- `PHASE_5_BACKLOG.md` created with Bug #28 as first entry (META_PLAN v6 § 8.2). TRIAGE_QUEUE_SPEC must lock first per META_PLAN v6 § 4.3.

**Next action:** CC audits v1 per the adversarial scope inherited from META_PLAN v6 § 6.2 + AUDIT_METHODOLOGY v2 § 6 + § 7. QB synthesizes findings.

---

## 10. Changelog

### v1 (initial draft)

Initial CC draft per Tony's locked Q1 (Phase 1+ audit findings only) and Q2 (Tier 3 with companion verification log). Document scope per Q1: triage queue entry format + lifecycle + severity discipline + worked examples on Bug #28, Bug #15, Bug #24. Out of scope: Phase 0 audit-cycle finding tracking; cross-cutting bug tracking (BIBLE_STRUCTURE_SPEC v3 § 5.3); Phase 5 backlog mechanism (PHASE_5_BACKLOG.md's internal organization).

§ 3 specifies the entry format with mandatory + conditional fields. § 4 specifies lifecycle: creation per AUDIT_METHODOLOGY v2 § 3.1's audit-cycle output; update with status transitions and dated-note discipline; transfer to PHASE_5_BACKLOG.md via explicit operator decision. § 5 inherits severity verbatim from META_PLAN v6 § 11; specifies inline-vs-queue boundary. § 6 follows META_PLAN v6 Appendix A.5's placeholder phase-numbering convention. § 7 provides three worked examples on real EE bugs (Bug #28 single-bug; Bug #15 cross-cutting; Bug #24 chain) per Tony's Q2 ratification.

The Bug #28 worked example reproduces META_PLAN v6 Appendix A.5 character-exact including all formatting per Tony's Q3 v1 cycle ratification (third-instance test for the recursive precision pattern). The operator memory file's verbatim symptom block and DD pool extraction note are reproduced character-exact per META_PLAN v6 verification log Claim 15c, demonstrating the operator-verified external source pattern (AUDIT_METHODOLOGY v2 § 4.4).

No new flagging thresholds introduced; severity inherits from META_PLAN v6 § 11. No new methodology constructs introduced beyond what the four locked Phase 0 documents + Tony's v1 cycle drafting spec authorize.

---

## 11. CC Drafting Notes (Self-Check Surfaces)

Per the methodology-interpolation rule, CC reviewed every new construct introduced in v1 against the rule. Items below are surfaced for Tony's awareness; CC's judgment on each is included.

### 11.1 Constructs explicitly authorized by Tony's locked drafting spec

- Tier 3 designation per Tony's Q2 v1 cycle ratification.
- Scope = Phase 1+ audit findings only per Tony's Q1 v1 cycle ratification.
- The required content categories A-J per the drafting spec.
- The 12 required deliverable structure sections (1 through 12) per the drafting spec.
- All cross-references to META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 / AUDIT_METHODOLOGY v2 / CONVERGENCE_CRITERIA v2 sections.
- Severity inheritance from META_PLAN v6 § 11 verbatim.
- Cadence deferrals to Phase 5 (in § 8.1, § 8.2, § 8.3) explicitly authorized by drafting spec's "no methodology-interpolation; defer cadence" discipline.

### 11.2 v1 surfacing notes

CC reviewed every new methodology construct introduced in v1 against the methodology-interpolation rule and the pattern-completion check.

1. **§ 4.1 inline-vs-queue boundary specification.** The drafting spec (requirement B) specified that "non-resolved findings transfer to triage queue" and asked for the threshold. CC defined the boundary as: (a) surgical document revisions inline-resolve; (b) operational defects queue-bound; (c) methodology questions per Tony's architectural discipline. The boundary is per-finding, not per-severity. Pattern-completion check: this operationalizes the drafting spec's framing without introducing new methodology — it follows from META_PLAN v6 § 8.1's "findings are not lost" framing. **Judged acceptable.**

2. **§ 4.2 status values (`open` / `in-progress` / `blocked` / `resolved`).** CC specified four status values as the lifecycle states. The drafting spec (requirement C) specified "how status changes" as required content. The four-value lifecycle is CC's articulation; Tony's spec did not enumerate the values. Pattern-completion check: the four values are the standard issue-tracking lifecycle (open / in-progress / blocked / resolved); they don't introduce new methodology. The framing is operationalization. **Surfaced for Tony's confirmation.** If Tony prefers a different lifecycle (e.g., explicit `deferred` state separate from `blocked`), specify in v2.

3. **§ 4.2 status transitions (`open` → `in-progress` → ...).** The transition arrows describe the standard lifecycle ordering. CC's articulation; not Tony-specified. Pattern-completion check: not new methodology; standard issue-tracking transitions. **Surfaced.**

4. **§ 4.2 update authority statement (QB updates; Tony reviews; audit-CC does not update).** This formalizes the role separation per META_PLAN v6 § 6.1 (Tony / QB / CC roles). Drafting spec did not explicitly authorize this articulation. Pattern-completion check: faithful to META_PLAN v6 § 6.1 roles + § 6.3 architectural-authority discipline; not new methodology. **Judged acceptable.**

5. **§ 5.1 enumeration of severity values including METHODOLOGY-INTERPOLATION as a severity.** The drafting spec stated "Map BLOCKER / MATERIAL / MINOR / STYLE to META_PLAN v6 § 11 verbatim; do NOT introduce new severities." CC included METHODOLOGY-INTERPOLATION as a severity per META_PLAN v6 § 6.1's "lock-blocker per Tony's hard rule regardless of MATERIAL count" framing. Pattern-completion check: METHODOLOGY-INTERPOLATION operates as a severity in the audit threshold (per AUDIT_METHODOLOGY v2 § 3.5 + § 6 prompt template); listing it alongside BLOCKER / MATERIAL / MINOR / STYLE in § 5.1 surfaces the existing severity rather than introducing a new one. **Borderline.** If Tony prefers METHODOLOGY-INTERPOLATION listed only as a finding-classification (not a severity), specify in v2 cycle.

6. **§ 7.1 note on Appendix A.5's `Severity: HIGH` label vs the formal taxonomy.** The Appendix A.5 worked example uses `HIGH` not `MATERIAL`; CC noted the discrepancy with explanation that A.5 pre-dates this document's § 5.1 inheritance and HIGH was the operator's intuitive classification at authorship time. Pattern-completion check: this is documentation of an inherited-from-locked-content discrepancy, not new methodology. § 7.2 and § 7.3 use the inherited taxonomy correctly. **Surfaced.**

7. **§ 7.2 / § 7.3 introduced format conventions for Cross-cutting note + Dependencies (Blocked by) fields.** The drafting spec authorized worked examples for Bug #15 (cross-cutting) and Bug #24 (chain). CC operationalized the demonstrations into Cross-cutting note format and Dependencies "Blocked by" formulation. Pattern-completion check: the field formats follow the entry format spec in § 3.2 (Cross-cutting note conditional field) and § 3.1 (Dependencies field). Worked examples demonstrate the format; not new methodology. **Judged acceptable.**

The methodology-interpolation rule is operative; the discipline of self-surfacing remains. v1 surfaces what's new.

### 11.3 Constructs explicitly NOT drafted (to avoid interpolation)

CC did not draft any of the following — each would have been pattern-completion or methodology-interpolation:

- **New severity values beyond META_PLAN v6 § 11.** Severity inheritance is verbatim.
- **Numerical thresholds for what counts as "operational defect" vs "methodology issue."** The boundary is per-finding judgment per § 4.1.
- **Cadence rules for queue review** — not drafted; deferred to Phase 5 working agreements per § 8.2.
- **Cadence rules for transfer to PHASE_5_BACKLOG.md** — not drafted; trigger is operator decision per § 4.3.
- **Reverse-transfer-frequency threshold** — not drafted; deferred per § 8.3.
- **Numerical ID convention for queue entries** beyond `Phase X.Y[.Z]` placeholder (per Appendix A.5).
- **Structured-data format** (JSON / YAML) — not drafted; deferred to Phase 5 per § 8.1.
- **New letter-prefix conventions** — not drafted (W.N remains the only ratified letter-prefix per BIBLE_STRUCTURE_SPEC v3 § 5.5).
- **Severity boundary thresholds beyond META_PLAN v6 § 11** — not drafted; § 5.2 specifies inline-vs-queue boundary independently of severity.
- **Tiebreaker criteria for cross-cutting bug canonical-home assignment** — not drafted; the queue defers to BIBLE_STRUCTURE_SPEC v3 § 5.3's deferral.
- **Worked examples beyond the three Tony-authorized bugs** (Bug #28, #15, #24) — not drafted; format demonstrated on the three.

The methodology-interpolation rule is operative; CC resisted introducing constructs beyond the drafting spec's authorized scope. The discipline of self-surfacing remains. v1 surfaces what's new.

---

End of TRIAGE_QUEUE_SPEC.md v1.
