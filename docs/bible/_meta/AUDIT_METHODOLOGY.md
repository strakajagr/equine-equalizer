# AUDIT_METHODOLOGY.md

**Document:** AUDIT_METHODOLOGY
**Phase:** 0 (Methodology) — Phase 0 deliverable 3 of 5
**Status:** LOCKED v3-patched-h (2026-05-19)
**Author:** CC (drafting under verification discipline; QB orchestrated and reviewed)
**Date:** 2026-05-08
**Locked:** 2026-05-08 (Tony ratification chain: Q1–Q8 + R1–R8 + R8.a + R8.b + R9–R12 + 11 finding ratifications + L1–L6)
**Audit completion:** SP-A3 2026-05-08; 11 findings delivered (2 BLOCKER, 4 MATERIAL, 5 MINOR/STYLE); 10 surgical patches + 1 wontfix-with-parenthetical applied at SP-A4

**Revision history:**
- v1 (2026-05-04): initial CC draft. Companion verification log at `_audits/AUDIT_METHODOLOGY_v1_verification.md`.
- v2 (2026-05-04): post-v1-audit surgical patch pass integrating Tony's three locked decisions (Q1: Option B addressing MATERIALs + tightly coupled MINORs; Q2a: Option (a) verbatim from source for § 4.6 quote attributions; Q2b: verification log delta with Claim 42 confirming verbatim accuracy). Companion verification log at `_audits/AUDIT_METHODOLOGY_v2_verification.md` inherits v1's 41 claims with re-verified-2026-05-04 timestamps and adds 1 new claim (Claim 42 — verbatim attribution of v2 audit Q2.2 + Tony's Q4 in § 4.6).
- v2-patched (2026-05-05): four lessons banked in § 4 (Lessons § 4.8 / § 4.9 / § 4.10 / § 4.11) emerged from the Database & Schema Bible v1 cycle (drafting + audit + Tony ratifications 2026-05-05). Lessons cover: § 4.8 QB substrate findings during spec authorship require Tony ratification; § 4.9 QB review pass is light surface only; § 4.10 verbatim-paste discipline for V1-N entries; § 4.11 grep predictions against bootstrap-mirror file unions. Each lesson follows the existing four-element structure (abstract rule + worked example + cross-references + audit-CC prophylactic check template). Banked at next-sequential slots per the file's § 4.X = Lesson X convention; the patch-spec referenced "Lesson 11/12/13" as labels but the file's slot numbering starts continuation at § 4.8. Substrate observation surfaced in `database_schema_bible_v1_verification.md` Section I V1-patch-10.
- v3 (2026-05-08): AUDIT_METHODOLOGY meta-cycle (post-Phase-1 dispatch sequence 4 of 4). 21 promotion-queue items + 3 awareness-item dispositions integrated. Cycle ratifications captured Q1–Q8 + R1–R8 + R8.a + R8.b by Tony 2026-05-08. New content: § 4.12–§ 4.24 (13 new lessons); § 5.8–§ 5.9 (2 new audit-CC prophylactic checks); § 12 (new section — 5 QB Self-Audit Checks); § 8.4–§ 8.5 (queue item 21 Reconciliation Strategies + Candidate #6 Standardization, landed under § 8 Open Questions per R8 substrate-grounded landing); § 10 changelog v3 entry; revision-history block per spec § 8 metadata-bundle requirement targeting § 10 (R8.b); end-of-document footer. Phase 0 anchor versions updated from META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 to META_PLAN v9 / BIBLE_STRUCTURE_SPEC v6 throughout. Three-element metadata bundle initialized at v1-draft authorship (header status field above; revision-history block here; end-of-document footer below). Operational precedent banking (v3 authorship, 2026-05-08): Lesson § 4.12 bounded-authorization discipline confirmed operating cleanly at drafting CC + audit CC + patch CC tiers across six post-Phase-0 cycle classes (Database & Schema, Data Pipeline, parallel cohort, API & Frontend, UC-1, PHASE_5_BACKLOG additions). Positive operational evidence; no methodology amendment required.
- v3-patched-h (2026-05-19): REPAIR-4 dispatch — § 4.38 (AS-OF discipline on per-row historical aggregates at race-fire-time inference; D4 case study) + § 4.39 (aggregate-without-timestamp tables substrate-leak at backtest/training replay; angle_stats C.5 case study) + § 5.10 (pre-fix discovery comprehensiveness check; Lessons § 4.38 + § 4.39 codified as audit-CC prophylactic check template). Pattern: substrate-divergent findings discovered during β arc supp-2 investigation; substrate-fix dispatch (REPAIR-4) executed 11 Tier-1 + Tier-2 surgical fixes across inference services + repositories + ingestion handler; new migration `012_angle_stats_history.sql` applied to production. Tier 3 surgical patch under REPAIR-4 dispatch ceremony cap; same Q5 ratification pattern as v3-patched-b through v3-patched-g.

- v3-patched-g (2026-05-18): Substrate-additive codification — § 4.32 Case Study 6 extensions (recursive validation events #6 + #7 + #8 + #9; multi-instance accrual substrate-emphatic for sub-pattern B prophylactic check refinement) + § 4.36 codification queue Item 5 single-instance banking annotation. Pattern: QB dispatch authoring decoupled from CC verbatim substrate-evidence at authoring time (substrate-emphatic 4-event multi-instance accrual this Tier 3 prerequisite execution arc); CC Phase 1 substrate-discovery surfaced divergence each event. Sub-pattern B prophylactic-check extension: at dispatch authoring time, QB MUST cite verbatim CC substrate-evidence basis OR explicitly authorize substrate-discovery sub-phase. § 4.32 Case Study 6 events #6-#9 verbatim per Tier 3 dispatch substrate-evidence. Same Q5 ratification pattern as v3-patched-b/c/d/e/f.
- v3-patched-f (2026-05-17): Substrate-additive codification — § 4.32 Case Study 6 extensions (recursive validation events #4 + #5; sub-patterns B + C codified) + § 4.37 (alarm authoring publisher-cadence × evaluation-period × TreatMissingData coherence per SP-ENTRIES-ALARM-CONFIG-FIX session evidence). Preserves committed v3-patched-e Option α substrate (§ 4.34 forensic-gate activation discipline + § 4.35 CC estimate substrate-untrustworthiness + § 4.36 AUC↑ + ROI↓ calibration degradation + § 4.32 Case Study 6 events #1-#3 + sub-pattern A); adds substrate-banking candidates that didn't codify in v3-patched-e cycle. Tier 2 surgical F.4 patch under Phase A entry directive ceremony cap; UC § 7.2 step 4 per-bible patch-CC convention explicitly overridden. Same Q5 ratification pattern as v3-patched-b/c/d/e.
- v3-patched-e (2026-05-17): Tier 1 session codification — § 4.32 Case Study 6 (stale-session-memory authoring discipline; 3 recursive validation events captured) + § 4.34 (forensic-gate activation discipline; folds banking candidate C per Tony Option α adjudication Phase 1 substrate-discovery) + § 4.35 (CC wall-clock + cost estimate substrate-untrustworthiness) + § 4.36 (AUC↑ + ROI↓ calibration degradation). Tier 2 surgical F.4 patch under Phase A entry directive ceremony cap; UC § 7.2 step 4 per-bible patch-CC convention explicitly overridden for bulk-mutation scope. Same Q5 ratification pattern as v3-patched-b/c/d. Sibling-CC SP-§4.33-TRAINING-SCRIPT-REGISTRATION-FIX bundled into v3-patched-d + §4.33 baseline commit per Tony Option (b) adjudication. § 4.34 verbatim content codified per Phase 1 substrate-discovery surfaced § 4.33 cross-reference expectation (Option α); § 4.34 placeholder approach rejected to avoid internal cross-reference inconsistency.
- v3-patched-d (2026-05-12): Phase A AMCS5 dispatch — § 4.32 Worked example expansion with Case Study 5 (parallel-dispatch source-state interaction) + Abstract rule extension (parallel-dispatch authorization under Directive 2 requires inter-dispatch source-state interaction analysis) + Audit-CC prophylactic check template extension (parallel-dispatch source-state interaction verification check). **Override disclosure (Q5 ratification preserved):** Tier 2 surgical F.4 patch under Phase A entry directive ceremony cap. UC § 7.2 step 4 per-bible patch-CC convention explicitly overridden by ceremony cap. **1 patch applied** with three sub-components: (a) Abstract rule extended with parallel-dispatch source-state interaction analysis requirement per Tony Decision 4 verbatim ratification language; (b) Worked example expanded to 5 case studies (Case Study 5 = E3 Step 2 + E4 Step 2 cdk source conflict caught at CC pre-execution); (c) Audit-CC prophylactic check template extended with parallel-dispatch source-state interaction verification check item. Banking queue stays at 6 per Tony adjudication; Case Study 5 expansion does NOT inflate queue (expansion of existing § 4.32, not new refinement). Cross-references preserved: § 4.31 producer-attribution refinement; § 4.33/§ 4.34 banking candidates (codification deferred to Phase A close-out).
- v3-patched-c (2026-05-12): Phase A AMCS4 dispatch — § 4.32 Worked example expansion with Case Study 4 (QB-side framing-inheritance across multiple dispatch turns) + Audit-CC prophylactic check template extension (QB-side dispatch authoring discipline check). **Override disclosure (Q5 ratification preserved):** Tier 2 surgical F.4 patch under Phase A entry directive ceremony cap. UC § 7.2 step 4 per-bible patch-CC convention explicitly overridden by ceremony cap. **1 patch applied:** Case Study 4 appended to § 4.32 Worked example (4-case-study banking; refinement applies recursively to QB-side dispatch authoring, not just at-handoff or at-CC-diagnostic). Cross-references: § 4.31 producer-attribution refinement (recursive application); § 4.33 change-event-boundary-investigation refinement (codification deferred to Phase A close-out per Tony banking cadence); § 4.34 alarms-encoding-design-state-expectations refinement (codification deferred to Phase A close-out). Banking queue stays at 6 per Tony adjudication; Case Study 4 expansion does NOT inflate queue (expansion of existing § 4.32, not new refinement).
- v3-patched-b (2026-05-12): Phase A AUDIT_METHODOLOGY patch dispatch — § 4.32 lesson banking handoff-authoring-without-substrate-verification methodology refinement per Tony CANDIDATE-this-session ratification. **Override disclosure (Q5 ratification preserved from D6 precedent):** Tier 2 surgical F.4 patch under Phase A entry directive ceremony cap. UC § 7.2 step 4 per-bible patch-CC convention explicitly overridden by ceremony cap. **1 patch applied:** new § 4.32 entry under existing 4-element convention (Abstract rule / Worked example / Cross-references / Audit-CC prophylactic check template); 3 case studies banked verbatim (D6 V1 catastrophic substrate divergence; D6 Appendix A1 substrate-incorrect classification near-miss; E1 Path 2 V1 CAPTCHA-solver scope propagation). Cross-references created: § 4.32 cross-links § 4.27 (producer-attribution refinement applies to D6 Appendix A1 case study); § 4.32 cross-links § 4.29 (QB-framing-not-substrate-verified applies to E1 Path 2 V1 case study). Cross-bible cross-reference freeze status: NOT re-engaged for AMP (Tier 2 ceremony cap pattern).
- v3-patched-a (2026-05-12): Phase A D6 bundled bible patches dispatch — 7 new methodology lessons banked from Phase A operational cycle (A.5 / A.5.1 / A.5.2 / A.5.3 / A.5-ext / A.6.a–f / D2 / D3 / D4 dispatch sequence). New content: § 4.25–§ 4.31 (7 new lessons appended to § 4 Methodology Lessons Catalog). **Override disclosure (Q5 ratification):** D6 surgical patches per F.4 pattern under Tier 2 ceremony cap per Phase A entry directive. UC § 7.2 step 4 per-bible patch-CC convention explicitly overridden by ceremony cap. Rationale: D6 documents Phase A operational findings into bibles per Phase A re-dispatch venue (R14.2 Option A scope); not a running cross-bible-cross-reference-freeze UC cycle. Override disclosure preserves UC-ceremony precedent for future cycles. § 4 entry convention preserved (4-element structure: Abstract rule + Worked example + Cross-references + Audit-CC prophylactic check template). Cross-bible cross-references created: § 4.27 cross-links § 4.31; § 4.30 cross-links data_pipeline_bible:4.5 (AWS API validation discipline). Substrate source: `docs/operations/PHASE_A_HANDOFF_2026-05-12.md` § 2.1, § 2.2, § 6.2.

**Tier:** 3 per META_PLAN v9 § 4.1 + § 6.5. CC-drafted under QB spec; companion verification log required; CC-audited.

**Anchored on:** META_PLAN v9 (locked 2026-05-05, current Phase 0 lock) and BIBLE_STRUCTURE_SPEC v6 (locked 2026-05-05, current Phase 0 lock). Section references throughout this document point to v9 / v6 § numbers. Historical worked examples in § 4 cite specific past versions (META_PLAN v3 audit, BIBLE_STRUCTURE_SPEC v1 audit, etc.) when referencing the specific cycle in which a lesson originated; those historical citations are immutable. Lock dates substrate-verified at patch CC tier 2026-05-08 against META_PLAN v9 + BIBLE_STRUCTURE_SPEC v6 Status fields.

**Methodology-interpolation rule (operative per META_PLAN v9 § 6.1, with v9's expanded scope and grandfathering clause; pattern-completion check operative per BIBLE_STRUCTURE_SPEC v1 audit lesson):** This draft does not invent binary tests, cadence rules, completeness criteria, scoring rubrics, severity thresholds, iteration caps, percentage criteria, procedural sequencing rules, or other CC-prescribed methodology constructs Tony has not explicitly ratified. Pattern-completion interpolation check operative; v1 surfacing notes in § 11.

---

## 1. Motivation

### 1.1 Why this document exists

AUDIT_METHODOLOGY.md is the third Phase 0 methodology deliverable. Its job is to give Phase 1 audit-CCs the prophylactic checks empirically learned across nine Phase 0 audit cycles (META_PLAN v1→v6, six cycles; BIBLE_STRUCTURE_SPEC v1→v3, three cycles), plus the Phase 1-specific cycle workflow that takes a CC-drafted Phase 1 bible from initial draft to lock.

Phase 0's audit cycle pattern emerged organically across those nine cycles: the v3 BLOCKER taught the verification-log-precision rule; the v3 / v4 / v5 / v6 cycles taught the methodology-interpolation rule with progressive scope expansion and grandfathering; the BIBLE_STRUCTURE_SPEC v1 / v2 cycles taught the pattern-completion check and the TOC contradiction class. AUDIT_METHODOLOGY codifies these lessons so that fresh Phase 1 audit-CCs apply them from cycle 1 rather than re-discovering them across multiple cycles.

The document is load-bearing for Phase 1 in the same way that META_PLAN v9 is load-bearing for Phase 0: a Phase 1 audit-CC handed only the six adversarial questions (META_PLAN v9 § 6.2) without the prophylactic checks below would re-introduce class-of-failure patterns Phase 0 already paid for.

### 1.2 Why now

Phase 1 begins after all five Phase 0 documents lock. Phase 1 produces seven bible documents (per BIBLE_STRUCTURE_SPEC v6 § 4.1) under Tier 3 discipline; each goes through its own audit cycle; multiple CC sessions may execute in parallel. AUDIT_METHODOLOGY ensures consistent audit discipline across those parallel cycles.

### 1.3 The Phase 0 audit cycle as worked example

Per Tony's locked Q1 in this document's drafting spec, AUDIT_METHODOLOGY is scoped to Phase 1 audits only. Phase 0 audit cycles have empirically converged across nine cycles; their lessons are codified and internalized. Phase 2-4 audit methodologies operate against different criteria, source material, and convergence definitions; they live where they're operational, defined when those phases begin. If they want to inherit Phase 0's audit cycle pattern, they reference META_PLAN v9 and BIBLE_STRUCTURE_SPEC v6 directly as worked examples.

This document treats Phase 0's nine audit cycles as the empirical substrate from which Phase 1 audit-CC discipline is derived. Worked examples in § 4 reference specific Phase 0 cycle findings; those references serve a pedagogical purpose, not an authority one.

---

## 2. Scope

### 2.1 What this document specifies

- **Phase 1 per-bible audit cycle** — the audit cycle for each individual Phase 1 bible (per META_PLAN v9 § 3.1's locked workflow + BIBLE_STRUCTURE_SPEC v6 § 8.3's per-bible cycle, as applied to Phase 1 documents).
- **Phase 1 cross-document consistency audit** — the audit per META_PLAN v9 § 3.3 that runs after all individual bibles lock, verifying internal consistency across the corpus.
- **Audit-CC prophylactic check templates** — prophylactic checks derived from the empirically grounded Phase 0 lessons plus this cycle's two new audit-CC checks (§ 5.8–§ 5.9), each with abstract rule statement, worked example, cross-references to origin sections, and check template form for paste-ready integration into Phase 1 audit prompts.
- **QB Self-Audit Checks** — five QB-tier self-audit checks codified in § 12, applying to QB's own meta-cycle authorship discipline (estimation calibration, self-describing authorization redundancy detection, paste-prompt transit-truncation discipline, within-message placeholder discipline, meta-document state claim substrate verification).
- **Phase 1 audit-CC prompt template** — paste-ready structure incorporating all seven prophylactic checks plus the six adversarial questions from META_PLAN v9 § 6.2.
- **Cross-document consistency audit prompt template** — paste-ready structure for the cross-document audit per META_PLAN v9 § 3.3, addressing the three cross-document questions.

### 2.2 What this document does NOT specify

- **Phase 0 audit methodology** — already empirically settled across the nine cycles documented above; not re-codified here.
- **Phase 2 adversarial bible audit methodology** — Phase 2 operates against the locked corpus (not against drafts), with different criteria (does the bible match the code?). Phase 2 methodology is deferred to Phase 2 entry. If Phase 2 wants to inherit Phase 0's audit cycle pattern, it references this document and META_PLAN v9 / BIBLE_STRUCTURE_SPEC v6 directly.
- **Phase 3 predictive concept inventory audit methodology** — deferred to Phase 3 entry.
- **Phase 4 gap analysis audit methodology** — deferred to Phase 4 entry.
- **What bible content goes where** — that's BIBLE_STRUCTURE_SPEC v6.
- **What success looks like for each phase** — that's CONVERGENCE_CRITERIA.md (Phase 0 deliverable 4).
- **Format for findings discovered during audit** — that's TRIAGE_QUEUE_SPEC.md (Phase 0 deliverable 5).
- **New methodology constructs not present in META_PLAN v9 or BIBLE_STRUCTURE_SPEC v6** — per the methodology-interpolation rule (§ 4.2 below), this document codifies methodology already locked in those documents; it does not extend or generalize them.

### 2.3 Authority chain

Per META_PLAN v9 § 4.1, AUDIT_METHODOLOGY is Tier 3; CC drafts under QB spec with companion verification log; audit-CC verifies. Per Tony's locked Q1 in this document's drafting spec, scope is Phase 1 audits only — both per-bible and cross-document. Per Tony's locked Q2, each methodology lesson is presented with an abstract rule statement, at least one worked example from Phase 0 cycles, cross-references to origin sections, and an audit-CC prophylactic check template.

---

## 3. Phase 1 Audit Cycle Workflow

### 3.1 Per-bible audit cycle

The per-bible audit cycle for each of the seven Phase 1 bibles (per BIBLE_STRUCTURE_SPEC v6 § 4.1) follows META_PLAN v9 § 3.1's locked Phase 0 per-deliverable cycle, with the per-document drafting authority determined per META_PLAN v9 § 6.5 (all Phase 1 bibles are Tier 3 per § 4.1 + § 6.5). BIBLE_STRUCTURE_SPEC v6 § 8.3 restates the cycle for Phase 1; the steps below cite both authorities.

**Steps (per META_PLAN v9 § 3.1 + BIBLE_STRUCTURE_SPEC v6 § 8.3):**

1. QB writes Phase 1 spec (target questions, format, depth bar, source-priority rules per META_PLAN v9 § 4.5, output location, explicit verification discipline including the methodology-interpolation rule per META_PLAN v9 § 6.1 and the verification-log precision rule per META_PLAN v9 § 6.5).
2. CC drafts the bible AND produces the companion verification log. Every factual claim about EE has a verification entry. **Per META_PLAN v9 § 6.5 hard rule, Tier 3 drafts that omit a companion verification log are rejected by QB without audit; the verification log is not optional.**
3. QB reads draft fully (synthesizing). QB skims verification log to spot-check entries.
4. QB writes audit-CC prompt incorporating: the six adversarial questions per META_PLAN v9 § 6.2, the prophylactic checks per § 5 of this document, the verification-against-live-system mandate, and the regression check for prior-cycle findings if vN ≥ 2.
5. QB runs audit-CC fresh.
6. Audit findings return; QB synthesizes.
7. If routine: QB re-specs/re-drafts, re-runs, repeats steps 3-6.
8. If architectural: QB surfaces to Tony with proposed resolutions and tradeoffs; Tony decides.
9. Repeat until audit clean per § 3.5's threshold.
10. Bible locks.

**Edge cases inherited from META_PLAN v9 § 3.1 (each operative for Phase 1 audits):**

- **CC↔audit-CC disagreement.** Default: audit-CC wins. If QB judges the audit-CC finding itself questionable, QB may run a third fresh CC session to adjudicate (last resort).
- **Audit-CC error.** Audit-CCs can be wrong. When verification contradicts an audit-CC finding, QB surfaces both: the original audit finding AND the contrary verification, and Tony decides whether the audit-CC needs the methodology refined or whether the draft missed something.
- **Tony's locked decision based on a wrong premise.** When verification surfaces that a Tony-locked decision was based on a premise that turns out to be false, CC does NOT silently revise — CC surfaces the contradiction to QB → Tony with the verified facts. Tony ratifies the reframing or holds the original. (Pattern invoked twice in Phase 0 cycles; codified as Lesson 6 in § 4.6.)
- **CC methodology-interpolation pattern.** CC has a recurring failure mode of extending Tony's locked answers with adjacent policy CC believes follows from the answer. The methodology-interpolation rule (§ 4.2) governs.
- **Post-lock revision.** If a Phase 1 bible locks, then weeks later a finding contradicts locked content, the procedure per META_PLAN v9 § 3.1 applies: QB surfaces to Tony; default is revise the locked document and trigger re-audit + dependent-document re-validation.
- **Audit findings with downstream consequences.** When audit-CC surfaces a fact that contradicts not just the audited document but the upstream substrate, the procedure is: revise the audited document to use the verified fact, flag the substrate inaccuracy for downstream correction, note the discrepancy in the document's revision history.

**Phase 1 drafting order (recommended per BIBLE_STRUCTURE_SPEC v6 § 8.2):** Architecture Overview first; Database & Schema second; Data Pipeline third; the three ML bibles in parallel; API & Frontend last. Recommended, not mandatory.

### 3.2 Cross-document consistency audit

After all seven Phase 1 bibles lock individually, a cross-document consistency audit runs per META_PLAN v9 § 3.3. The cross-document audit is governed by three additional questions appended to the six adversarial questions of META_PLAN v9 § 6.2:

1. Does the bible say something the code does not do?
2. Does the code do something the bible does not say?
3. Where do bible documents contradict each other across files?

Note: questions 1 and 2 are framed at META_PLAN v9 § 3.3 in Phase-2 language ("the bible" treated as the locked corpus); for Phase 1's cross-document audit (which runs after individual Phase 1 bibles lock but before the Phase 2 adversarial bible audit per META_PLAN v9 § 3.3's separate scope), these three questions are scoped to **internal cross-document consistency** rather than full code-vs-bible reconciliation. Code-vs-bible reconciliation at full Phase 2 scope is deferred to Phase 2.

**Cross-document audit deliverable structure (per META_PLAN v9 § 3.3):**

- One cross-document audit report at `/docs/bible/_audit/cross_document_audit.md`.
- Per-bible audit reports already exist at `/docs/bible/_audit/<bible_doc_name>_audit.md` from individual cycles.
- The cross-document audit reads all per-document audit reports as input; it is a separate fresh CC session.

**Cross-document audit threshold:** the same threshold as per-bible audits (§ 3.5 below). Findings that surface cross-document contradictions are MATERIAL by their nature when they require a bible to revise; MINOR when they're style or convention drift.

**Per-bible re-revision trigger:** per META_PLAN v9 § 3.3, "if a per-document audit returns >5 MATERIAL findings, that document goes back to Phase 1 revision before the cross-document audit runs." Cross-document audit does not run until all individual bibles meet Tony's threshold.

### 3.3 Audit-CC paste-ready prompt structure

Audit prompts must be paste-ready per META_PLAN v9 § 8.4. The Phase 1 audit-CC prompt template is in § 6 below; the cross-document audit-CC prompt template is in § 7. Both extend META_PLAN v9 Appendix A.6's working example.

Each prompt's structure (standardized per META_PLAN v9 § 8.4):

- Project context (what EE is, what this document is, where it sits in the phase sequence)
- The roles in this project (Tony, QB, CC)
- The audit workflow (every Phase 1 deliverable goes through adversarial CC audit before Tony reviews)
- Reference materials (DD bible, EE current state dump, live AWS, live API endpoints, EE codebase)
- Verification discipline (HARD RULE: live state preferred over dump; precision rule applied broadly; no fabrication)
- The draft (path on disk or inline)
- Companion verification log (if Tier 3; instruction to spot-check)
- Adversarial task: six adversarial questions per META_PLAN v9 § 6.2 plus document-type-specific adversarial checks
- Prophylactic checks per § 5 of this document
- Regression check (for vN ≥ 2)
- Output format (standardized findings structure)
- Severity assessment (BLOCKER / MATERIAL / MINOR / STYLE)
- Threshold context (per § 3.5)
- Recommendation form (lock as-is / lock after specific minor revisions / revise and re-audit / substantial rework)

### 3.4 Verification log requirements for Phase 1 bibles

Every Phase 1 bible draft is Tier 3 per BIBLE_STRUCTURE_SPEC v6 § 4.1; therefore every Phase 1 bible draft has a companion verification log per META_PLAN v9 § 6.5. The verification log:

- Lives at `/docs/bible/_audit/<bible_doc_name>_v<N>_verification.md` per BIBLE_STRUCTURE_SPEC v6 § 5.1's front matter pattern.
- Has one entry per concrete factual claim about EE.
- Distinguishes inherited claims (already verified in META_PLAN v9 / BIBLE_STRUCTURE_SPEC v6 verification logs) from new claims (introduced by this Phase 1 bible).
- Applies the verification-log precision rule per META_PLAN v9 § 6.5 (counts decomposed; definitions vs uses vs imports distinguished; aggregable counts explicitly aggregated). The full lesson is captured as Lesson 1 in § 4.1 below.
- Includes operator-verified external source quotes verbatim where applicable per META_PLAN v9 verification log Claim 15c pattern. The full lesson is captured as Lesson 4 in § 4.4 below.

The audit-CC reads both the draft and the verification log; verifies a sample of verification claims against live state; reports any verification-log entries that don't hold up.

### 3.5 Tony's threshold for lock per audit cycle

A Phase 1 bible locks when its audit returns:

- **< 5 MATERIAL findings** AND
- **zero fabricated-content findings** AND
- **zero methodology-interpolation findings (post-grandfathering)**

This threshold is inherited verbatim from META_PLAN v9 § 11 (Lock Status), where it has been operative across nine Phase 0 audit cycles. Per Tony's hard rule (per META_PLAN v9 § 6.1 + audit history): methodology-interpolation findings fail the lock regardless of count.

**MATERIAL/MINOR distinction (per META_PLAN v9 Appendix A.6):** "A 'missing example' is probably MINOR. A 'the maintenance protocol has an enforcement gap' is probably MATERIAL. A 'CC-interpolated binary test that Tony hasn't ratified' is MATERIAL by its nature per the methodology-interpolation rule."

**Audit-CC must apply the distinction honestly.** Per META_PLAN v9 Appendix A.6: "Tony has explicitly cautioned against threshold-gaming. The operator values surfacing problems over reassurance." If an audit-CC finds few flaws, the bar is wrong — re-read more skeptically.

**No new flagging thresholds are introduced by this document.** Each prophylactic check below states what to look for, how to recognize the pattern, and how to flag — but the threshold for flagging is delegated to Tony's existing < 5 MATERIAL threshold or to the methodology-interpolation rule's lock-blocker classification.

---

## 4. Methodology Lessons Catalog

The lessons below appear in the empirical sequence of their introduction across Phase 0 cycles + post-Phase-0 cycles. Order is preserved to document the discipline's evolution. Each lesson has the same four required structural elements (per Tony's locked drafting requirements): abstract rule statement, worked example from cycle history, cross-references to origin sections (META_PLAN / BIBLE_STRUCTURE_SPEC / cycle-specific origin documents), and an audit-CC prophylactic check template.

§ 4.1–§ 4.7: original seven lessons codified in v1 (empirically grounded across Phase 0 cycles).
§ 4.8–§ 4.11: four lessons banked at v2-patched (Database & Schema Bible v1 cycle, 2026-05-05).
§ 4.12–§ 4.24: thirteen lessons banked at v3 (AUDIT_METHODOLOGY meta-cycle, 2026-05-08).

### 4.1 Verification-log precision rule

#### Abstract rule

Verification log entries must be precise about what was counted, in a form that cannot be compressed by readers. Specifically:

- Counts must be decomposed where the source supports decomposition (e.g., "3 instantiations + 1 import = 4 references," not "4 references including the import").
- Claims must distinguish definitions vs uses vs imports.
- Anything aggregable must be aggregated explicitly so a reader cannot compress with judgment.

The rule applies broadly — to any aggregable count anywhere in a Tier 3 document, not only to code-reference counts that look like the v3 BLOCKER pattern. When in doubt, decompose; over-decomposition costs verification-log length but never costs accuracy.

#### Worked example

The rule emerged from META_PLAN v3 → v4 (BLOCKER F1; broad-sweep scope locked in v5 cycle).

**v3 verification log entry (loose form):** "PredictionRepository instantiated in prediction_router.py:34, 61, 92 (4 references including the import)."

**v3 main doc (compressed):** "prediction_router.py (4 instantiations of PredictionRepository)."

The v3 audit caught the inflation as the BLOCKER F1 finding: A.4 said "4 instantiations" — actual count was 3 instantiations + 1 import. The "4 instantiations" was a compression of the verification log's loose phrasing into a count error in the main document. The v3 audit fix:

**v4 verification log entry (decomposed):** "PredictionRepository: 1 import on line 6 + 3 instantiations on lines 34, 61, 92 = 4 references total."

**v4 main doc (carries the decomposition):** "3 instantiations of PredictionRepository at lines 34, 61, 92, plus 1 import on line 6 = 4 references total."

The v3 phrasing allowed a downstream reader to compress "4 references including the import" into "4 instantiations" by judgment. The v4 phrasing makes the components explicit; no compression is possible without altering the count visibly.

The v5 cycle locked broad-sweep scope (per Tony's locked decision in v5 cycle): the rule applies broadly. v5 applied it to working-tree status counts (74 untracked + 29 modified = 103 per META_PLAN v9 verification log Claim 22), model registry counts (88 = 45 active + 43 inactive per Claim 7), EventBridge rules (13 = 10 ENABLED + 3 DISABLED), and Lambda counts (8 = 5 Active + 3 INACTIVE). The v6 cycle extended to ECS task families enumerated by name (5 named in META_PLAN v9 § 2.3 per Claim 20).

#### Cross-references

- **Rule statement:** META_PLAN v9 § 6.5 ("Verification log precision rule").
- **Decomposition examples in main doc:** META_PLAN v9 § 1.1 (working-tree state — content preserved at this anchor across v6→v9), § 1.3 (registry / Lambda / EventBridge), § 2.3 (ECS task families), § 9.13 (registry multi-active-row), Appendix A.4 (legacy `predictions` references).
- **BLOCKER finding:** META_PLAN v3 audit (severity table, F1).
- **Rule introduction:** META_PLAN v4 (per § 6.5's rule body and the v4 changelog).
- **Broad-sweep ratification:** META_PLAN v5 cycle (per Tony's locked decision; v9 § 6.5 carries the locked language inherited from v6).
- **v6 application to enumeration:** META_PLAN v9 § 12.4 ("Methodology lesson recorded (v5 → v6)" subsection within v5→v6 changelog; MINOR #6 — ECS task families fully enumerated).

#### Audit-CC prophylactic check template

For any aggregable count in the audited document, verify:

1. **The count is decomposed where the source supports decomposition.** A claim like "8 Lambdas" should appear as "8 = 5 Active + 3 INACTIVE" if the source distinguishes states. A claim like "13 EventBridge rules" should appear as "13 = 10 ENABLED + 3 DISABLED."
2. **The decomposition matches the source.** No inflation (4 → 4 instantiations when 1 was an import). No compression (88 = 45 active + 43 inactive → "88 active models").
3. **"Definitions vs uses vs imports" or analogous distinctions are explicit** for code-reference counts.
4. **Sum is shown** when the decomposition includes multiple parts (e.g., "3 + 1 = 4").

Flag as MATERIAL if a count is presented compressibly when the source supports decomposition.

Flag as **fabricated content** (lock-blocker) if a decomposition's components don't add to the stated total OR if a count contradicts the source it cites.

### 4.2 Methodology-interpolation rule with named patterns + catch-all + grandfathering clause

#### Abstract rule

CC does not invent binary tests, cadence rules, completeness criteria, scoring rubrics, severity thresholds, iteration caps, percentage criteria, procedural sequencing rules, or other CC-prescribed methodology constructs Tony has not explicitly ratified.

The named patterns are illustrative, not exhaustive; the catch-all clause ("or other CC-prescribed methodology constructs Tony has not explicitly ratified") covers what is not named.

**Grandfathering clause:** Pre-existing methodology constructs from earlier cycles' QB drafts are grandfathered; CC-introduced content from prior cycles is subject to retroactive sweep at rule introduction. "Pre-existing" means content that existed in any version prior to the cycle in which the rule was introduced. The boundary is computable, not judgment-dependent — provenance (CC-introduced vs QB-drafted) is the discriminator, not the operator's recall of what was ratified.

The methodology-interpolation rule landed in cycle 5 (META_PLAN v5); v6's retroactive sweep covered v1-v4 CC-introduced content and treated v1-v4 QB-drafted content as grandfathered.

#### Worked examples (multiple, showing the rule's range)

The rule was introduced in META_PLAN v5 → v6 cycles after multiple instances of CC interpolation surfaced and were dropped in successive cycles:

**Worked example 1: v3 § 7.10 "Steps 5 and 6 happen in the same working session."**

The v3 cycle introduced this sentence as a CC-drafted cadence rule for the Phase 0 per-deliverable cycle. The v3 audit caught it as MATERIAL #3: "§ 7.10 'Steps 5 and 6 happen in the same working session' is CC-interpolated policy not in Tony's locked language." The v3 audit's reasoning: "v3 introduces operator policy ('same working session') in a section that also includes Tony's verbatim locked language. A reader can't easily tell which sentences are Tony's locked rules vs which are CC's interpolated framing." v4 dropped the sentence.

**Worked example 2: v4 § 9.13 "Removing any one converts the documentation back to the FORBIDDEN form."**

The v4 cycle introduced this binary test in the model-registry multi-active-row anti-pattern's CORRECT form (META_PLAN § 9.13). The v4 audit caught it (Question 1 finding 3 / Question 3 finding 3 / Severity table #5): "This is a methodology assertion (CC-prescribed), not factual claim. But it's stated as a rule. There's no verification log entry because there's nothing to verify — but the claim functions as a binary criterion on documentation acceptability. Tony hasn't ratified that the three-piece test is binary. CC interpolated this as the sharpening pattern." v5 replaced the binary test with descriptive prose.

**Worked example 3: v5 audit M-1 — § 5.3 / § 3.1 "3 consecutive iterations" iteration cap (retroactive sweep).**

The v3 cycle introduced "Iteration cap: if the convergence test fails on the same dimension in 3 consecutive iterations, QB escalates to Tony for protocol revision rather than continuing to iterate." The specific number "3" was CC-chosen in v3 cycle; the v3 drafting spec used "3" as the spec-writer's example number, not Tony's locked verbatim. The construct survived v3, v4, and v5 drafts without being caught.

The methodology-interpolation rule landed in v5 cycle (per the v5 changelog). The v5 audit explicitly performed a retroactive sweep of v1-v4 CC-introduced content; the sweep caught the v3-cycle iteration cap. Per Tony's bar (methodology-interpolation findings fail regardless of count), this was a hard fail. v6 cadence-neutralized the language: "if the convergence test fails repeatedly on the same dimension, QB escalates to Tony for protocol revision rather than continuing to iterate. The specific count threshold for 'repeatedly' is operator judgment; cadence specification (including any numerical iteration cap) is a Phase 5 working-agreements decision." All cadence-shaped decisions defer to Phase 5 uniformly.

The v5 catch demonstrated three properties of the rule:

1. The rule applies broadly across construct types (binary tests, cadence rules, iteration caps).
2. Pattern-completion check applies recursively (see Lesson 5).
3. Methodology rules introduced in cycle N must include explicit retroactive sweep in cycle N+1's audit (see Lesson 3).

#### Cross-references

- **Rule statement with named patterns + catch-all:** META_PLAN v9 § 6.1 (CC role definition).
- **Grandfathering clause:** META_PLAN v9 § 6.1 (the "Grandfathering clause" paragraph).
- **v3 catch and resolution:** META_PLAN v3 audit (severity table #3); META_PLAN v4 changelog (drop confirmed in v3 finding regression check).
- **v4 catch and resolution:** META_PLAN v4 audit (Question 1 finding 3 / Question 3 finding 3 / Severity table #5); META_PLAN v5 (replacement with descriptive prose, per v5 changelog).
- **v5 catch and resolution:** META_PLAN v5 audit M-1 finding (Methodology-interpolation rule self-application section); META_PLAN v9 § 12.4 (M-1 cadence-neutralized in v5→v6 changelog).
- **v6 clean lock:** META_PLAN v6 audit (Methodology-interpolation findings: ZERO post-grandfathering).

#### Audit-CC prophylactic check template

For any methodology construct in the audited document, verify it traces back to one of:

1. Tony's locked instructions in a drafting spec for this document, OR
2. META_PLAN v9 or earlier locked Phase 0 documents (with content authored by Tony or by QB and ratified by Tony), OR
3. Operator-stated rationale per source-priority tier 5 (META_PLAN v9 § 4.5).

If the construct does not trace to one of those three, flag as **methodology-interpolation finding**.

Methodology-interpolation findings are MATERIAL by their nature per the methodology-interpolation rule (META_PLAN v9 § 6.1) and **lock-blockers regardless of count** per Tony's hard rule.

**How to recognize the pattern:**

- A construct stated as a rule but with no source citation.
- A numerical threshold (e.g., "3 consecutive iterations") in the audited document not present in the drafting spec or locked source.
- A binary test ("removing any one converts X to Y") asserting acceptability criteria not present in source.
- A cadence specification ("typically 3-5 per session," "every Thursday") not present in source.
- A procedural sequencing rule ("Step A must precede Step B") not present in source.
- A scoring rubric or percentage criterion ("if >50% of X applies, Y") not present in source.
- Generally: if the construct shapes how a future CC executes the methodology AND it's not in the source, suspect interpolation.

**How to flag:** in the audit report's severity table, mark severity as **METHODOLOGY-INTERPOLATION (lock-blocker)** with citation to the audited document's section and quotation of the interpolated language. Provide the resolution recommendation: either (a) Tony explicitly ratifies the construct in the next drafting spec, or (b) the construct is dropped or replaced with cadence-neutral / operator-judgment-deferred language.

### 4.3 Audit-CC retroactive sweep discipline

#### Abstract rule

When a new methodology rule lands in cycle N, the audit-CC spec for cycle N+1 must explicitly include "sweep prior content for instances of this pattern" as a required adversarial check. The rule itself does not enforce its own retroactive application — the audit spec does.

The retroactive sweep is bounded by the grandfathering clause (per Lesson 2): covers v1 through v(N-1) CC-introduced content; treats v1 through v(N-1) QB-drafted content as grandfathered.

The discriminator is provenance (CC-introduced vs QB-drafted), not the operator's recall of what was ratified.

#### Worked example

The lesson emerged from META_PLAN v5 → v6 (v5 audit's M-1 finding catching the v3-cycle iteration cap).

The methodology-interpolation rule landed in v5 cycle. The v3-cycle "3 consecutive iterations" iteration cap survived through v3, v4, and v5 drafts without being caught; the v3 audit and v4 audit both ran without retroactive sweep instructions for this rule (the rule did not yet exist in v3/v4 cycles).

The v5 audit's M-1 finding caught the v3-cycle iteration cap. The catch was explicit retroactive sweep: the v5 audit's "Methodology-interpolation rule self-application" section covered v1-v4 CC-introduced content for instances of the pattern (binary tests, cadence rules, completeness criteria, scoring rubrics — the rule's named patterns at v5). The v3-cycle iteration cap was caught because the sweep was scoped to cover prior cycles' CC-introduced content; it would not have been caught by a sweep scoped only to v5-cycle drafting compliance.

Key observation from the v5 → v6 transition (per META_PLAN v9 § 12.4 "Methodology lesson recorded (v5 → v6)" within v5→v6 changelog):

> The v5 audit's M-1 finding revealed that methodology rules introduced mid-cycle do not enforce their own retroactive application. The audit must explicitly include retroactive sweep in its scope when a new rule lands. This becomes a discipline that AUDIT_METHODOLOGY.md (Phase 0 doc 3) must codify: when a new methodology rule is introduced in cycle N, the audit-CC spec for cycle N+1 explicitly includes "sweep prior content for instances of this pattern" as a required adversarial check. The rule itself doesn't enforce its own retroactive application — the audit spec does.

The v6 audit applied the rule retroactively + verified the v5-introduced rule's prior-content sweep was complete. The v6 audit's "Methodology-interpolation rule self-application" section explicitly enumerates grandfathered content (v1-v4 QB-drafted) and sweep-eligible content (v1-v4 CC-introduced) and confirmed zero CC-introduced violations remained post-grandfathering.

#### Cross-references

- **The v5 audit's catch:** META_PLAN v5 audit M-1 finding ("Methodology-interpolation rule self-application" section).
- **The grandfathering clause that bounds the sweep:** META_PLAN v9 § 6.1 (per Tony's locked v6 spec language preserved through v9).
- **v6's verification of correct sweep application:** META_PLAN v6 audit (Methodology-interpolation rule self-application section + Grandfathering clause check section).
- **v6 changelog's banking the lesson for AUDIT_METHODOLOGY:** META_PLAN v9 § 12.4 ("Methodology lesson recorded (v5 → v6)" subsection within v5→v6 changelog).

#### Audit-CC prophylactic check template

When the audited document is the first cycle after a new methodology rule lands:

1. **Verify the audit-CC spec for this cycle includes retroactive sweep covering all prior CC-introduced content.** The spec must explicitly enumerate the prior cycles to be swept (e.g., "sweep v1-v(N-1) CC-introduced content for instances of [rule pattern]").
2. **Verify the spec's retroactive sweep instruction was followed.** The audit report should have a section enumerating each candidate prior-cycle construct against the rule.
3. **Verify all flagged prior-cycle constructs map to either pre-rule grandfathered or post-rule sweep-eligible per the grandfathering clause's provenance discriminator.** Constructs flagged as grandfathered should have provenance noted ("v1 § X.Y, drafted by QB in v1 cycle"); constructs flagged as sweep-eligible should have provenance noted ("v3 § X.Y, CC-introduced in v3 cycle").

Flag as MATERIAL if retroactive sweep was skipped or scoped incorrectly (e.g., scoped only to current-cycle drafting compliance, missing prior cycles).

When the audited document is NOT the first cycle after a new rule lands (i.e., the rule is already several cycles old), retroactive sweep is performed once at rule introduction and not re-run; the prior sweep's findings are inherited. Verify the inheritance is documented.

### 4.4 Operator-verified external source pattern

#### Abstract rule

When verification depends on a source outside audit-CC's MCP scope (operator memory files, external systems, oral histories), the audit prompt must quote the verbatim source inline so audit-CC doesn't flag operator-verified content as unverifiable. Operator verification is a separate substrate provided by Tony; audit-CC's job is to verify the document's prose accurately reflects the operator-verified source, not to re-verify the source itself.

Two failure modes the rule prevents:

1. **Audit-CC flags operator-verified content as unverifiable** because audit-CC cannot read the source. (Without the verbatim quote inline, audit-CC has no way to verify the document's claim.)
2. **Audit-CC silently complies with a source mischaracterization** because the source is not directly available for audit-CC to check the characterization against. (Without the verbatim quote inline, audit-CC may default to accepting the audit-cycle's previously stated characterization even when that characterization was wrong.)

#### Worked example

The pattern emerged from META_PLAN v5 → v6 cycle (Bug #28 exacta payout claim verification).

**v5 cycle:** The v5 audit examined § 8.1's Bug #28 case study and characterized the operator memory file `equine-equalizer-bug-28-hrn-scraper.md` as "silent on exacta payout status." The v5 audit's recommendation was to soften the bounded-loss claim to remove the exacta-still-populates assertion. The v5 audit-CC could not directly read the operator memory file (it lives at `~/.claude/projects/-home-strakajagr/memory/`, outside the EE codebase). The "silent on exacta" characterization was an inference, not a verification.

**v6 cycle:** Tony's MINOR #5 instruction in the v6 spec was to "soften the exacta claim" based on the v5 audit's characterization. The v6 cycle's audit-CC prompt included an "OPERATOR-VERIFIED EXTERNAL SOURCE" block that quoted verbatim from the memory file: **"Place, show, and exacta payouts still populate."** This verbatim quote made the v5 audit's characterization checkable. The v6 audit-CC's "Operator-verified external source check" section verified that v6's prose was faithful to the verbatim source.

The v6 cycle's verbatim block also flagged a nuance the memory file did include: "DD pool extraction at hrn_scraper.py:814 likely has the same root cause" — distinct from the `daily_double_payout` field already accounted for in the result-dict. v6 preserved this distinction; the v5 audit-CC's characterization of "silent on exacta" failed to surface either the place/show/exacta still-populates statement OR the DD-pool-extraction nuance.

The v6 audit's verdict (per the verification log Claim 15c entry): "the v5 audit-CC's characterization that the memory file was 'silent on exacta status' was itself wrong — the file explicitly states 'Place, show, and exacta payouts still populate.' This is a 'Tony's locked decision based on a wrong premise' instance per § 3.1's edge case enumeration; v6 surfaces it and applies the verified-fact reframing rather than silently complying with the v5-audit-inferred softening that contradicts the source."

#### Cross-references

- **Edge case enumeration:** META_PLAN v9 § 3.1 ("Audit-CC error" + "Tony's locked decision based on a wrong premise" patterns).
- **Bug #28 case study with the verbatim quote:** META_PLAN v9 § 8.1 (the "provisional stable-known classification" paragraph quoting "Place, show, and exacta payouts still populate").
- **Verbatim source verification log entry:** META_PLAN v6 verification log Claim 15c (the operator-verified external source).
- **v6 audit's operator-verified-source check section:** META_PLAN v6 audit (Operator-verified external source check section).
- **v6 spec's authorization of the contingency:** META_PLAN v6 verification log Claim 15c (citing Tony's v6 spec: "If the memory file makes statements about exacta status that contradict this softening, flag in the verification log").

#### Audit-CC prophylactic check template

When the audited document references an external source outside MCP scope (operator memory files, external dashboards, oral histories):

1. **Verify the audit prompt provides the verbatim operator-verified quote inline.** The quote should be in a clearly-delimited block (e.g., "OPERATOR-VERIFIED EXTERNAL SOURCE:" with the verbatim text). Without the verbatim inline, audit-CC cannot perform the check.
2. **Verify the document's prose accurately reflects the verbatim source without extension.** "Extension beyond the source" includes: claiming additional populating fields the source doesn't name; conflating distinct code paths the source distinguishes; softening or strengthening a source's characterization beyond what the verbatim states.
3. **Verify any nuance the source flags is preserved in the document's prose.** If the source flags a related-but-distinct issue (e.g., "DD pool extraction likely has the same root cause"), the document's prose must preserve the distinction.

Flag if:
- The audited document references an external source without the audit prompt providing operator verification → MATERIAL (verification gap).
- The document extends beyond what the verbatim source states → MATERIAL or fabricated-content depending on severity (extension that contradicts source = fabricated; extension that strengthens beyond source = MATERIAL).
- The document silently softens a source's claim per a prior audit-CC's characterization that the verbatim source contradicts → surface as a "Tony's locked decision based on a wrong premise" pattern (see Lesson 6) and recommend reframing.

### 4.5 Pattern-completion interpolation pattern

#### Abstract rule

When a methodology rule establishes a pattern (e.g., W.N for one entry type), CC may extend the pattern to adjacent cases (F.N, C.N, D.N) without recognizing the extension as interpolation. **Pattern parallelism does NOT constitute ratification.** Each prefix or convention extension must be individually ratified by Tony in a drafting spec or earlier locked methodology document.

The audit-CC prophylactic check is mechanical: grep for any letter-prefix or numeric-prefix conventions; verify each individual prefix is independently ratified.

The pattern-completion check is a recursive application of the methodology-interpolation rule (Lesson 2) to convention extensions. It surfaces a class of interpolation that's easy to miss because it feels like consistency rather than invention.

#### Worked example

The lesson emerged from BIBLE_STRUCTURE_SPEC v1 → v2 cycle.

**v1 cycle:** BIBLE_STRUCTURE_SPEC v1 § 5.5 introduced a unified F.N / C.N / D.N convention extending META_PLAN v6's ratified W.N pattern to three additional discipline-rule entry types (Forbidden Patterns as F.N, Common Mistakes as C.N, Deprecated as D.N).

**v1 audit:** Audit-CC's catch (per the v1 audit's "Methodology-interpolation rule self-application" section): "The F.N / C.N / D.N convention is a CC-introduced naming-convention extension of META_PLAN's W.N pattern. It is a methodology construct (it shapes how every Phase 1 bible numbers its discipline-rule entries; downstream commit messages, cross-references, and audit-CC verification rely on it) that Tony has not ratified."

The audit's grep over META_PLAN v6 returned zero F./C./D. hits; only W.N is ratified. META_PLAN v6 Appendix A.1 (Forbidden Pattern worked example) labels its example as `6.4 ...` using a sub-section numeric ID, NOT `F.N`. META_PLAN v6 Appendix A.4 (Deprecated) labels its example `21.1 ...`, NOT `D.N`. META_PLAN v6 § 9.1-9.13 anti-patterns use `9.X` numeric subsections, NOT `C.N`.

**v2 cycle:** Per Tony's Option B in the v1 cycle response, BIBLE_STRUCTURE_SPEC v2 dropped the F.N / C.N / D.N extensions and used sub-section numeric IDs throughout (matching DD bible's existing convention). W.N was retained as the only letter-prefix because the cross-bible bug-tracking forcing function (per META_PLAN v9 § 7.11 commit-message convention; a grep over `git log` for `W.7` retrieves every commit related to that immune-memory entry across all bibles) justifies the asymmetry.

**v3 cycle:** BIBLE_STRUCTURE_SPEC v3 § 5.5 carries the locked convention: "The W.N letter-prefix convention is the **only** letter-prefix in EE bible numbering: What Was Fixed entries require cross-bible-trackable identifiers because cross-cutting bugs (per § 5.3 canonical-home rule) reference each other across bibles, and a grep over `git log` for `W.7` retrieves every commit related to that immune-memory entry across all bibles per META_PLAN v9 § 7.11 commit-message convention." (Convention preserved through BIBLE_STRUCTURE_SPEC v6 § 5.5.)

#### Cross-references

- **v1 catch:** BIBLE_STRUCTURE_SPEC v1 audit (severity table #5; Methodology-interpolation rule self-application section).
- **Tony's Option B resolution:** BIBLE_STRUCTURE_SPEC v1 audit (Recommendation #5 with both Option A and Option B); BIBLE_STRUCTURE_SPEC v2 changelog ("M-1 — F.N / C.N / D.N naming convention extension dropped per Tony's Option B").
- **v2 post-Option-B convention:** BIBLE_STRUCTURE_SPEC v2 § 5.5.
- **v3 locked convention preserved through v6:** BIBLE_STRUCTURE_SPEC v6 § 5.5 and § 7.2.
- **v3 changelog banking the lesson for AUDIT_METHODOLOGY:** BIBLE_STRUCTURE_SPEC v3 § 13 (v1 → v2 changelog "Methodology-interpolation finding resolved" subsection: "Pattern-completion interpolation lesson banked for AUDIT_METHODOLOGY.md") — historical citation; content carried forward through v6.

#### Audit-CC prophylactic check template

For any letter-prefix or numeric-prefix convention introduced or referenced in the audited document:

1. **Grep for letter-prefix patterns.** Search for `[A-Z]\.[0-9]` or `[A-Z]\.<n>` patterns within the document's section numbering and cross-reference syntax. Enumerate each unique prefix.
2. **For each prefix found, verify the prefix is named in META_PLAN v9, BIBLE_STRUCTURE_SPEC v6, or a Tony-locked drafting spec for this document.** Independently — pattern parallelism does NOT satisfy ratification. If W.N is ratified, that does NOT ratify F.N or C.N or D.N.
3. **For each unratified prefix, flag as methodology-interpolation finding.** The flagging severity is METHODOLOGY-INTERPOLATION (lock-blocker per Tony's hard rule).

The check applies to:
- Section-numbering letter prefixes (e.g., `5.W.<n>`, `5.F.<n>`, `7.D.<n>`).
- Cross-reference syntax extensions (e.g., adding `<bible>:5.F.<n>` to a convention that previously only supported `<bible>:5.<n>`).
- Numeric-prefix conventions (e.g., introducing a new numbered series like "X-1, X-2, X-3" parallel to an existing series).
- Generally: any extension of an existing named pattern to adjacent cases.

The check does NOT apply to:
- Section IDs that are pure numeric subsections of existing sections (e.g., `5.4` for the fourth subsection of section 5; that's not a new prefix, it's the existing numeric convention).
- References to ratified prefixes used within their established scope (e.g., citing `8.W.3` in a Phase 1 bible where W.N is ratified).

### 4.6 "Tony's locked decision based on a wrong premise" pattern

#### Abstract rule

When verification surfaces that a premise underlying a Tony-locked decision is false, CC surfaces the contradiction to QB rather than silently revising. Two QB-side actions follow:

1. Surface to Tony with the verified facts.
2. Tony ratifies the reframing or holds the original.

The pattern protects against silent compliance with locked decisions whose premises have failed verification. It is bidirectional: applies to Tony's instructions AND to prior audit recommendations.

The pattern has been invoked twice in Phase 0 cycles, once per cycle group, indicating it is a recurring procedural type rather than a one-off edge case.

#### Worked examples (both invocations)

**Invocation 1: v3 cycle — gitignore artifacts.**

Tony's Q4 in the v3 cycle was based on v2 audit's claim that deploy artifacts were not gitignored.

v2 audit Question 2 finding 2 (verbatim, line 47):

> 2. **§ 7.10 git-status-clean rule has practical conflict with deploy artifacts.** `.cf-distribution-id` and `.frontend-bucket` are not in `.gitignore` (verified). Both files exist on disk (verified). They are written by `scripts/deploy-backend.sh:243` and `:262`. After every deploy, `git status` would show modifications, blocking the next "git status clean" gate per § 7.10.

Tony's Q4 (verbatim, v2 audit lines 237-241):

> **Q4 — Deploy artifacts: gitignore as Phase 0 prerequisite.**
> - Add `.cf-distribution-id` and `.frontend-bucket` to `.gitignore`
> - Audit deploy scripts for other untracked artifacts during Phase 0; add all to `.gitignore` in one sweep
> - Document in v3 § 7 that the `.gitignore` was established at Phase 0 baseline along with rationale
> - Deploy artifacts have no business in commits — they're cached infrastructure identifiers, not source state

v3 verification revealed the artifacts were already covered. The current `.gitignore` already excluded `.frontend-bucket`, `.cf-distribution-id`, `cdk-outputs.json`, and `frontend/.env.production` (per META_PLAN v9 § 7.14 verbatim). v3 § 7.14 surfaced the contradiction in the verification log (Claim 11) and reframed the prerequisite: dropped the "add to gitignore" step (already done); kept the "audit deploy scripts for any uncovered artifacts" step. Tony ratified the reframing in the v4 cycle.

**Invocation 2: v6 cycle — Bug #28 exacta payout claim.**

Tony's MINOR #5 in the v6 cycle was based on v5 audit's claim that the operator memory file was "silent on exacta payout status." Tony's MINOR #5 directed: "soften the exacta claim per the v5 audit's characterization."

v6 verification (with the operator memory file's verbatim quote provided in the v6 audit-CC prompt's OPERATOR-VERIFIED EXTERNAL SOURCE block) revealed the memory file's symptom statement explicitly reads "Place, show, and exacta payouts still populate." v6 § 8.1 applied a reframing faithful to the source: kept the place/show/exacta still-populate claim AND added the DD-pool-extraction nuance the memory file does flag ("DD pool extraction at hrn_scraper.py:814 likely has the same root cause" — distinct from `daily_double_payout` already accounted for in the result-dict). v6 verification log Claim 15c surfaced the contradiction explicitly. The v6 audit's "Operator-verified external source check" section verified the reframing was faithful to the source.

Per META_PLAN v9 § 12.4 ("Methodology lesson recorded (v5 → v6)" within v5→v6 changelog): "The 'Tony's locked decision based on a wrong premise' edge case in § 3.1 has been invoked twice now (Q4 in v3, MINOR #5 in v6). The pattern is robust: when verification contradicts a Tony-locked decision, surface to QB → Tony rather than silently complying. v6 surfaces; the resulting reframing is faithful to the verified source."

#### Cross-references

- **Edge case enumeration:** META_PLAN v9 § 3.1 ("Tony's locked decision based on a wrong premise" pattern).
- **v3 invocation (gitignore):** META_PLAN v3 verification log Claim 11; META_PLAN v3 audit (additional adversarial finding "D. v3 reframing of Tony's Q4"); META_PLAN v9 § 7.14 (post-reframing locked content).
- **v6 invocation (exacta):** META_PLAN v6 verification log Claim 15c; META_PLAN v9 § 8.1 (post-reframing locked content); META_PLAN v6 audit (Operator-verified external source check section).
- **v6 changelog's pattern recognition:** META_PLAN v9 § 12.4 ("Methodology lesson recorded (v5 → v6)" within v5→v6 changelog).

#### Audit-CC prophylactic check template

When verification of any audited claim surfaces that a Tony-locked premise underlying the claim is false:

1. **Audit-CC surfaces both: the original locked decision's premise AND the contrary verified facts.** The audit report includes the verbatim Tony-locked language, the verbatim source contradicting it, and a recommendation pathway.
2. **Audit-CC does NOT silently apply the audit recommendation when the recommendation's premise is contradicted by verification.** If the previous-cycle audit recommended X based on premise P, and verification reveals P is false, the recommendation X is not automatic; it requires re-grounding against the verified premise.
3. **The pattern is bidirectional.** It applies to:
   - Tony's instructions in the drafting spec (a Tony-locked instruction based on a wrong premise).
   - Prior audit recommendations the current draft is supposed to address (a prior-audit-recommended fix based on a wrong premise).

Flag the finding type as **"Tony's locked decision based on a wrong premise"**, severity MATERIAL by its nature. Resolution path: surface to QB → Tony for explicit ratification of the reframing (or holding of the original). Do NOT pre-apply the reframing in the audit report; the audit report surfaces the contradiction and lets Tony decide.

### 4.7 TOC contradiction class (architectural insight)

#### Abstract rule

When shared templates reference per-document sections by number, audit-CC's prophylactic check should include verifying that all per-document templates use the same canonical section numbering for the referenced positions. Extracting shared templates creates reference dependencies on canonical section numbers that per-document templates may deviate from. Deviations break shared-template cross-references.

The pattern is structural: shared template prose says "section X is a Forbidden Pattern at sub-position X.<n>"; per-document templates may place "section X" at different absolute positions; cross-references resolve inconsistently.

#### Worked examples

The pattern emerged from BIBLE_STRUCTURE_SPEC v1 → v2 → v3 cycles as a recurring contradiction class.

**v1 catch: 8-vs-18 What Was Fixed numbering inconsistency.**

BIBLE_STRUCTURE_SPEC v1 § 5.2 recommended TOC placed What Was Fixed at position 8 ("8. What Was Fixed — Do Not Revert"). BIBLE_STRUCTURE_SPEC v1 § 5.5 example used position 18 ("section 18 if section 18 is What Was Fixed" and cross-bible reference example `feature_provenance_bible:18.W.7`).

The number 18 originated from DD bible § 18 (DD's What Was Fixed section number) but DD has 21 sections in a single file; EE bibles have ~8-10 sections each, so position 18 was structurally impossible (or required huge gap-jumping).

v1 per-document templates split: § 6.2 data_pipeline TOC used 18 ("8. Deprecated" then "18. What Was Fixed"); § 6.1 architecture_overview used 8. Six of seven templates used 18; § 6.1 used 8; § 5.2 said 8.

The v1 audit's catch (severity table #4): "Pick one canonical position for What Was Fixed across all bibles and apply consistently. Recommendation: position 8." v2 implemented MATERIAL #2 — What Was Fixed positioned at section 8 across all instances.

**v2 catch: 5-vs-7 Discipline-rules section deviation.**

BIBLE_STRUCTURE_SPEC v2 § 5.2 recommended TOC placed Discipline rules at section 5. BIBLE_STRUCTURE_SPEC v2 § 5.6.2's example referenced Discipline rules at section 5 of the ML Layer Architecture Bible: "a Forbidden Pattern at section 5 of the ML Layer Architecture Bible is `ml_layer_architecture_bible:5.4`".

v2 per-document templates had three deviations: § 6.3 feature_provenance, § 6.4 ml_layer_architecture, and § 6.5 model_evaluation_retraining placed Discipline rules at section 7 (not 5). Internal contradiction: § 5.6.2's example assumed section 5 across all bibles; § 6.4's TOC placed Discipline rules at section 7. Two readers (one looking at § 5.6.2, one looking at § 6.4) would assign the same Forbidden Pattern different identifiers.

The v2 audit's catch (Question 4 / severity table MATERIAL #1): "§ 5.2 recommended TOC vs § 6.X actual TOCs Discipline-rules-section deviation. Same contradiction class as v1's 'What Was Fixed at 8 vs 18' — load-bearing because § 5.6.2's example assumes section 5 across all bibles, but § 6.X TOCs use varying numbers."

**v3 resolution:** Per Tony's Option I in the v3 cycle, all seven per-document templates were renumbered to match § 5.2's canonical 5/6/7/8 ordering. v3 § 5.2 strengthened the language: "**mandatory for sections 5–8** (per Tony's v3-cycle Finding 1 ratification); domain-specific sections at positions 1–4 may be reorganized per locality of reference." Future drafters of new bibles must conform. Convention preserved through BIBLE_STRUCTURE_SPEC v6 § 5.2.

The v2 audit's banking statement (per the v2 → v3 changelog "Methodology lessons recorded" subsection): "When shared templates reference per-document sections by number, audit-CC's prophylactic check should include: 'verify all per-document templates use the same canonical section numbering for the referenced positions; deviations break shared-template cross-references.' This is a special case of the broader contradiction-detection question (META_PLAN v9 § 6.2 Q4) but worth naming explicitly given the recurrence across both v1 and v2 audits."

#### Cross-references

- **v1 catch (8-vs-18):** BIBLE_STRUCTURE_SPEC v1 audit (Question 4 finding 1; severity table #4).
- **v1 → v2 resolution:** BIBLE_STRUCTURE_SPEC v2 changelog (M-2: What Was Fixed positioned at section 8).
- **v2 catch (5-vs-7):** BIBLE_STRUCTURE_SPEC v2 audit (Question 4 finding 1; severity table MATERIAL #1).
- **v2 → v3 resolution + lesson banking:** BIBLE_STRUCTURE_SPEC v3 § 5.2 (canonical 5/6/7/8 mandate, preserved at BIBLE_STRUCTURE_SPEC v6 § 5.2); BIBLE_STRUCTURE_SPEC v3 § 13 (v2 → v3 changelog "Methodology lessons recorded" subsection — historical citation).
- **v3 locked canonical mandate:** BIBLE_STRUCTURE_SPEC v6 § 5.2 + § 5.6 (canonical templates depending on stable numbering); BIBLE_STRUCTURE_SPEC v6 § 6.1-§ 6.7 (all seven per-document templates conforming).
- **v3 audit confirmation:** BIBLE_STRUCTURE_SPEC v3 audit (Cross-reference integrity check section + regression check confirming all 7 templates verified at canonical 5/6/7/8 ordering).

#### Audit-CC prophylactic check template

When the audited document contains shared templates referencing per-document sections by number:

1. **Verify all per-document templates use the same canonical section numbering for the referenced positions.** Enumerate the per-document templates; check each one's numbering against the shared template's expected positions.
2. **Verify cross-references between shared templates and per-document templates resolve consistently.** Pick a representative cross-reference (e.g., "section 5 of the ML Layer Architecture Bible is `ml_layer_architecture_bible:5.4`") and verify the section actually exists at that position in the per-document template.
3. **Verify renumbering or restructuring does not break prior cross-references.** If the document renumbered sections in this version, every cross-reference to those sections (in this document and in adjacent locked documents) resolves to the new numbering.

Flag as MATERIAL if:
- Any per-document template deviates from the shared template's expected numbering.
- A shared-template cross-reference fails to resolve in any per-document template.
- Renumbering broke a prior cross-reference that was resolving correctly.

The check is mechanical: for the seven Phase 1 bibles, grep each bible's actual draft for canonical section headers (e.g., `^### 5.* Discipline rules`, `^### 6.* Currently Open`, `^### 7.* Deprecated`, `^### 8.* What Was Fixed`); verify all seven drafts have the same absolute positions for these four sections. (The mechanical grep target is the bible drafts at `/docs/bible/<bible>.md`, not BIBLE_STRUCTURE_SPEC v6's per-document templates at v6 § 6.X — those templates are the spec the drafts should conform to.)

### 4.8 QB substrate findings during spec authorship require Tony ratification before spec corrections

#### Abstract rule

When QB encounters substrate gaps or contradictions during drafting-spec authorship (e.g., a referenced upstream document's claim is contradicted by primary-source verification), QB does NOT silently correct the spec. QB surfaces the finding to Tony with verified facts and proposed reframings; Tony ratifies the correction or holds the original. The spec then carries the ratified resolution.

The pattern protects against silent QB-side compliance with upstream errors AND against silent QB-side correction of upstream content that may be intentional. Substrate verification surfaces the candidate; Tony's ratification governs the resolution.

The pattern is a specific application of Lesson 6 (Lesson 4.6: "Tony's locked decision based on a wrong premise") to the QB drafting-spec authorship phase: QB substrate findings during spec authorship route the same way as audit-CC findings against locked content — through Tony ratification, not silent correction.

#### Worked example

The lesson emerged from the Database & Schema Bible v1 drafting cycle (2026-05-05).

QB authoring the v1 drafting spec encountered two substrate gaps in upstream documents:

- The QB handoff Section 8.3 cited "META_PLAN v9 § 9.10 + § 9.11 govern JSONB conventions." QB substrate verification (direct read of v9 § 9.10 + § 9.11) refuted this — § 9.10 is "current bug list in narrative form" anti-pattern; § 9.11 is the FE-drift anti-pattern. Neither addresses JSONB.
- The QB handoff Section 8.3 cited `model_versions.metadata` as a JSONB column. QB substrate verification (direct read of schema.sql + all 12 migrations) refuted this — `metadata` is not a column.

Per this lesson, QB did NOT silently correct the handoff. QB:
1. Banked both substrate findings in the drafting spec's § 10 (Handoff cross-reference corrections section).
2. Authored the spec content to cite correct upstream sections (schema.sql + canonical.py + § 5.2 directly for JSONB; the V1-6 substrate-grounded refutation entry for the metadata claim).
3. Surfaced the handoff cross-reference inaccuracies as QB-side findings with explicit "Banked here for transparency; spec content corrects them; future handoff-document cycles can incorporate the corrections" language.

The Database & Schema Bible v1 cycle's H1 + H3 self-audit log entries record the substrate-grounded refutation discipline; the v1-cycle drafting CC's verification log V1-6 entry carries the substrate-cited refutation forward.

#### Cross-references

- **Origin cycle:** Database & Schema Bible v1 drafting (2026-05-05).
- **Banking location:** Database & Schema Bible v1 drafting spec § 10 (Handoff cross-reference corrections section).
- **Substrate-grounded refutation entry:** Database & Schema Bible v1 verification log V1-6.
- **H1 / H3 self-audit log:** Database & Schema Bible v1 drafting spec § 6 H1 / H3 entries (cross-reference accuracy + substrate-grounded reframing self-audits).

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible's drafting spec or the bible itself:

1. **Identify any QB substrate findings against upstream documents** (statements in the spec or bible that contradict an upstream source's claims).
2. **Verify the QB substrate finding's resolution traces to Tony ratification, not silent correction.** Look for: "Banked at § X.Y for transparency; spec content corrects the cite" or "Tony ratified the reframing on YYYY-MM-DD" or equivalent ratification markers.
3. **Flag as MATERIAL if** a QB-introduced spec correction contradicts an upstream document's claim AND there is no Tony-ratification marker; AND the correction was not surfaced to Tony for explicit ratification.

The check is bidirectional: applies to QB-corrects-upstream patterns AND QB-extends-upstream patterns.

### 4.9 QB review pass is light surface review only; substrate verification is audit-CC's job

#### Abstract rule

QB's review pass on a CC-drafted Tier 3 deliverable is a light surface review (synthesizing) rather than a substrate verification. QB reads the draft fully to check structural coherence, ratification compliance, and spec adherence. QB skims the verification log to spot-check entries for obvious anomalies. QB does NOT independently re-run every verification command; that is audit-CC's adversarial job.

The two roles are deliberately separated:

- **QB review pass:** light surface — sufficient to catch egregious drift but not designed to catch fabricated verification log entries that pass surface inspection.
- **Audit-CC adversarial pass:** independent re-verification — designed to catch fabricated entries by re-running every command and comparing actual output to claimed output.

The lesson protects against the failure mode where QB performs deeper review than the role specifies, then accepts a deliverable as audit-clean by mistake. QB's lighter touch is by design; audit-CC's adversarial pass is what catches fabrication.

#### Worked example

The lesson emerged from the Database & Schema Bible v1 audit cycle (2026-05-05).

The drafting CC's V1-8 verification log entry asserted: "Same date applies to 8.W.2 (migration 002 fix): `git log --format=\"%cs %h %s\" -- backend/database/migrations/002_fix_race_type_length.sql | tail -1` returns the same `2026-05-04 87dec36 Pre-bible baseline commit ...` entry."

QB's review pass on the verification log spot-checked V1-N entries for anomalies but did not re-run every `git log` command. The V1-8 parity assertion passed QB's surface review. Audit-CC's adversarial pass re-ran the command and surfaced the DRIFT: migration 002 actually returns `2026-03-15 d93c4c4 Fix post_time TIMESTAMPTZ, race_type length, and connection isolation`. The drafting CC either did not run the command for migration 002 or summarized the output without verbatim paste; the V1-8 parity assertion was fabricated and passed QB review without catching the fabrication.

This case demonstrates the role separation worked as designed:

- QB review pass: surfaced no anomaly (the assertion was internally consistent and the substrate-finding language was plausible).
- Audit-CC adversarial pass: caught the BLOCKER finding by independently re-running the command.

The lesson banks: QB review pass is sized correctly when audit-CC catches fabrication that QB does not. If QB review pass started catching fabrication, that would suggest audit-CC's adversarial scope is mis-sized (audit-CC is the role designed for this catch).

#### Cross-references

- **Origin cycle:** Database & Schema Bible v1 audit cycle (2026-05-05).
- **D-3.1 BLOCKER finding:** `database_schema_bible_v1_audit.md` § B (V1-8 DRIFT) + § D-3.1 (no-fabrication BLOCKER).
- **Role separation:** META_PLAN v9 § 6.5 (Tier 3 workflow): "QB reads draft fully (synthesizing). QB skims verification log to spot-check entries. ... CC audits. Audit-CC reads both the draft and the verification log; verifies a sample of verification claims against live state."

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible's verification log:

1. **Re-run every V1-N verification command independently.** Do not trust the verification log's reported output; treat it as a claim to verify.
2. **For each command, compare actual output to claimed output.** DRIFT findings emerge from the comparison.
3. **For commands that cannot run from the audit-CC sandbox (e.g., live API, AWS state), surface as UNVERIFIABLE-FROM-WORKING-TREE rather than asserting PASS by default.**

The check is mechanical: per V1-N entry, re-run + compare. The role's value is the independence — audit-CC has no investment in V1-N entries returning the values they reported.

### 4.10 Verbatim-paste discipline for V1-N entries

#### Abstract rule

Drafting CC must paste verbatim command output for every V1-N entry in a Tier 3 verification log. Verbatim paste means: raw `grep` / `git log` / `sed` / `wc` / `diff` / `WebFetch` output as it appears on stdout, with no summarization, no paraphrasing, no "returns the expected output" assertions in place of the actual output.

Summarization of command output is treated as fabrication-class risk: the drafting CC may report a verification command's "expected" output without actually running the command, and the summarization passes light review because it is plausible. Audit-CC catches it on adversarial re-run; but the verbatim-paste discipline prevents the fabrication from entering the verification log in the first place.

The rule is a specific extension of the verification-log-precision rule (Lesson 1, § 4.1) to the substrate of the verification command itself: counts must be decomposed; AND command outputs must be pasted verbatim, not summarized.

The rule's scope is explicitly CC-tier (V1-N verification log entries authored by drafting CC). The QB-tier sibling discipline — verbatim-paste of substrate quotation in QB chat output — is codified separately at § 4.19.

#### Worked example

The lesson emerged from the Database & Schema Bible v1 audit cycle (2026-05-05) — same case as Lesson § 4.9.

The drafting CC's V1-8 verification log entry asserted that migration 002's `git log` returned the same baseline-commit date as migration 011. The assertion was a summarization ("returns the same ... entry") rather than a verbatim paste. Had the drafting CC pasted the verbatim output of `git log --format="%cs %h %s" -- backend/database/migrations/002_fix_race_type_length.sql`, the actual output (`2026-03-15 d93c4c4 Fix post_time TIMESTAMPTZ, race_type length, and connection isolation`) would have been visible in the verification log; the parity assertion against migration 011's baseline-commit date would have been visibly contradicted by the verbatim text.

The summarization-without-verbatim-paste pattern enabled the fabrication. Audit-CC caught the BLOCKER on adversarial re-run; the verbatim-paste discipline (banked here as Lesson § 4.10) prevents future drafting CCs from making the same error class.

The discipline integrates with existing META_PLAN v9 § 6.5 (verification log precision rule) + § 8.6 (no-fabrication rule); explicit lesson-level codification reinforces the discipline across remaining 5 Phase 1 bibles.

Forward rule for drafting specs:

> Drafting specs MUST require CC to paste verbatim command output (raw `grep` / `git log` / `sed` / `wc` / `diff` / `WebFetch` / `cat` output as it appears on stdout) for every V1-N entry. Summarization of command output is treated as fabrication-class risk.

#### Cross-references

- **Origin cycle:** Database & Schema Bible v1 audit cycle (2026-05-05).
- **D-3.1 BLOCKER finding:** `database_schema_bible_v1_audit.md` § D-3.1.
- **v1-patched V1-8 rewrite:** `database_schema_bible_v1_verification.md` Section C V1-8 (rewritten with verbatim per-migration sweep) + Section I V1-patch-1 (verbatim sweep + decomposition).
- **Existing META_PLAN coverage:** v9 § 6.5 (verification log precision rule) + § 8.6 (no-fabrication rule). This lesson reinforces the discipline at the substrate level (verbatim command output) where v9 covered the surface level (decomposed counts + no-fabrication).
- **QB-tier sibling:** § 4.19 (QB-tier paste-verbatim discipline reinforcement — substrate quotation in QB chat output).

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible's verification log:

1. **For each V1-N entry, verify the verification command's output is pasted verbatim** (not summarized). Look for: raw multi-line `grep` output with line numbers; raw `git log` output with commit hashes and messages; raw `wc` / `diff` exit codes; etc.
2. **Flag as MATERIAL** if a V1-N entry asserts a command's output without pasting the verbatim text. ("Returns the expected output" / "matches the prediction" / "confirms the claim" without raw output is the pattern to flag.)
3. **Flag as fabricated content (BLOCKER)** if the asserted output, when re-run, differs from the verbatim actual output. Lesson § 4.9 (audit-CC adversarial pass) catches this class.

The check is mechanical: per V1-N entry, look for verbatim raw command output. Absence of verbatim paste is a signal to re-run the command and compare.

### 4.11 V1-N grep predictions against `schema.sql` + `migrations/*.sql` must account for byte-identity edge cases

#### Abstract rule

Drafting specs that prescribe `grep` against `schema.sql` plus `migrations/*.sql` for V1-N substrate verification predictions must account for the possibility that some files in the union are byte-identical mirrors. Specifically: if `schema.sql` and `001_initial_schema.sql` (or analogous bootstrap-mirror pairs) are byte-identical, the union's grep returns 2x the count of distinct declarations rather than 1x.

The lesson is narrow but recurrent: every Tier 3 drafting spec that prescribes a grep across multiple files containing potentially-overlapping content should distinguish between (a) the count of distinct domain entities and (b) the count of grep matches on disk. Predictions should explicitly enumerate both.

#### Worked example

The lesson emerged from the Database & Schema Bible v1 cycle (2026-05-05).

The v1 drafting spec V1-1 verification command was:

```
grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql | grep -v "schema_migrations" | wc -l
```

The spec predicted "expected: 14 plus possibly the `IF NOT EXISTS` patterns; verify count and decompose explicitly per Check 9."

Independent re-run during drafting verification (V1-1 + V1-1a in the verification log) returned **25 statements** (11 in schema.sql + 11 mirrored in 001_initial_schema.sql + 3 in 005_three_prediction_tables.sql). Audit-CC re-ran and confirmed 25.

The discrepancy: the v1 spec did not anticipate that `schema.sql` and `001_initial_schema.sql` were byte-identical (`diff` returns empty exit 0; both files 415 lines). The 14-distinct-domain-table claim still holds (the union is 14 names), but the grep yields 25 statements due to the bootstrap-mirror pair.

The drafting CC surfaced the gap as FRAMEWORK_GAP F.1 in the v1 verification log Section F with substrate-cited candidate reframing per Lesson 4. Tony ratified F.1 on 2026-05-05; bible content stands; this lesson is banked here for future drafting specs that prescribe similar grep verifications.

Forward rule for drafting specs:

> When prescribing a grep across `schema.sql` plus `migrations/*.sql` (or analogous unions where bootstrap-mirror pairs may exist), the V1-N prediction enumerates BOTH the count of distinct declarations AND the count of grep matches on disk. Both numbers are reported; the relationship between them (1:1, 2:1 due to mirror, etc.) is documented.

#### Cross-references

- **Origin cycle:** Database & Schema Bible v1 cycle (2026-05-05).
- **F.1 surfacing:** `database_schema_bible_v1_verification.md` Section F F.1.
- **Tony ratification:** Tony's Q1 2026-05-05 (bible content stands; lesson banked here).
- **Drafting-spec grep prediction:** `database_schema_bible_v1_drafting_spec.md` § 7 (V1-1 prediction).

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible's drafting spec for V1-N grep predictions:

1. **For each V1-N grep that targets a union of files (e.g., `schema.sql` + `migrations/*.sql`), verify the prediction enumerates both distinct-entity count and on-disk-match count.**
2. **Flag as MINOR if the prediction enumerates only one count without distinguishing.** The drafting CC should surface the byte-identity case as FRAMEWORK_GAP if it surfaces during substrate verification.
3. **Flag as MATERIAL if the prediction's expected output is contradicted by independent re-run AND the drafting CC did not surface the discrepancy as FRAMEWORK_GAP.**

The check applies to grep / wc / awk predictions across file unions; it does not apply to single-file commands.

### 4.12 Low-cost substrate verification at row-authorship (execute, don't defer)

*Banked: Phase 1 Cohort parallel-cohort handoff, 2026-05-08*

#### Abstract rule

When drafting CC (or any CC tier authoring substrate-grounded content) encounters a row-by-row authorship task where the substrate verification cost for an individual row is low relative to the cost of deferring to a later audit cycle, drafting CC executes the verification at row-authorship rather than deferring. "Low-cost" means the verification is a single grep, single file read, single git log, or analogous O(1) command — work that can be performed inline during authorship without disrupting flow. "High-cost" means full multi-file re-runs, full database queries, or other operations whose cost warrants defer-to-audit-CC scope.

The discipline is bounded-authorization compatible: drafting CC executes substrate verification only within its authorized read scope. The lesson does not expand authorization; it changes execution timing within already-authorized scope from "defer until audit" to "execute at row-authorship."

The lesson protects against the pattern where drafting CC accumulates ungrounded rows in a draft and relies on audit-CC to catch substrate gaps retroactively. Audit-CC is the adversarial-detection role; row-authorship verification is the prevention role. Both are required. When drafting CC defers low-cost verifications, audit-CC catches preventable errors and the cycle's finding count inflates with errors that should never have entered the draft.

The discipline is operative across all bounded-authorization tiers (drafting CC, audit CC, patch CC) per Lesson § 4.12 itself — see § 12.5 QB Self-Audit Check 5 generalization for QB-tier substrate verification mandate at meta-document state claims.

#### Worked example

The lesson emerged across the Phase 1 Cohort cycles (Architecture Overview, Database & Schema, Data Pipeline, Feature Provenance, ML Layer Architecture, Model Evaluation & Retraining, API & Frontend) and was banked at the parallel-cohort handoff (2026-05-08). Across multiple cycles, per-row substrate questions ("does this column exist? does this file path resolve? does this function signature match the latest signature?") were observably resolvable at row-authorship time via single-command verification but were observed deferred to audit-CC re-run. The pattern surfaced enough times to be banked as a discipline at the parallel-cohort handoff: drafting CC executes, doesn't defer.

The discipline contrasts with high-cost cases where defer-to-audit-CC is appropriate (e.g., full live-AWS state re-verification, full database query against live tables) — those genuinely warrant audit-CC's adversarial scope.

#### Cross-references

- **Origin:** Phase 1 Cohort parallel-cohort handoff (2026-05-08).
- **Related:** § 4.9 (QB review pass is light surface review only); § 4.10 (verbatim-paste discipline for V1-N entries); § 12.5 (QB Self-Audit Check 5 — meta-document state claim substrate verification, parallel discipline at QB tier).

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible's verification log:

1. **Identify rows in the bible that depend on low-cost-verifiable substrate** (single grep, single file read, single git log, single function-signature lookup).
2. **Verify the corresponding V1-N entry executed the verification at row-authorship** rather than asserting "verified by audit-CC re-run" or deferring with placeholder language.
3. **Flag as MINOR if** row-authorship verification was deferred without substrate-cost justification (i.e., the verification was low-cost and could have been executed inline).
4. **Flag as MATERIAL if** the deferred verification surfaces a substrate gap (the row's claim doesn't hold) that drafting CC could have caught at authorship.

The check is bounded by the four-element-structure verification: where § 4.X embedded checks already cover substrate verification, this check adds the timing dimension (when, not whether).

### 4.13 Inheritance read-scope discipline

*Banked: Phase 1 Cohort parallel-cohort handoff, 2026-05-08*

#### Abstract rule

When CC (drafting CC, audit CC, patch CC) is dispatched with a bounded read scope on Phase 0 locked documents, the operational read pattern is: TOC + targeted-section reads on Phase 0 locks suffice when load-bearing content is consulted. Full sequential read of every Phase 0 lock is neither required by spec nor efficient. The pattern is: read TOC; identify load-bearing sections per the dispatch's substrate-citation needs; read those sections targeted; do not exhaustively read the rest of the document.

The discipline applies symmetrically: CC must read load-bearing content (rather than skim) when it is consulted, but does not read non-load-bearing content speculatively.

The discipline integrates with the bounded-authorization clause (per Lesson § 4.12 codification): out-of-scope substrate is not read at all; in-scope substrate is read targeted, not exhaustively.

#### Worked example

The lesson emerged across the Phase 1 Cohort cycles (parallel-cohort handoff, 2026-05-08). Across drafting-CC cycles for the seven Phase 1 bibles, drafting CC sessions that exhaustively read every Phase 0 lock (META_PLAN, BIBLE_STRUCTURE_SPEC, AUDIT_METHODOLOGY, CONVERGENCE_CRITERIA, TRIAGE_QUEUE_SPEC) consumed substrate-read context for content the cycle's authorship work did not reference; sessions that read TOC + targeted sections covered load-bearing content with substantially less read-budget consumption and produced equivalent draft quality.

The discipline was banked at the parallel-cohort handoff with the principle: TOC + targeted-section reads on Phase 0 locks suffice when load-bearing content is consulted. Sessions that consult content not flagged as load-bearing should still read targeted; speculative full-document reads are an audit-CC anti-pattern when scoped to content the audit does not require.

The lesson is narrow but cumulative — across many cycles it materially affects context budget, and across many parallel cycles it materially affects total CC context-window pressure.

#### Cross-references

- **Origin:** Phase 1 Cohort parallel-cohort handoff (2026-05-08).
- **Related:** § 4.12 (low-cost substrate verification at row-authorship — both lessons govern targeted vs exhaustive substrate engagement).

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible's drafting cycle:

1. **Identify the substrate-read scope authorized in the drafting spec.** The spec's substrate-authorization clause names which Phase 0 locks (and which other documents) drafting CC was authorized to read.
2. **Verify drafting CC's reads were targeted to load-bearing content.** Look for evidence that drafting CC read TOC + specific sections, rather than full sequential reads. Read patterns are observable in drafting CC's interim reports (citation patterns, section references made).
3. **Flag as STYLE if** drafting CC exhaustively read in-scope substrate that the cycle's authorship work did not consult. (Not a methodology violation; an efficiency observation.)
4. **Flag as MATERIAL if** drafting CC read out-of-scope substrate (content not authorized in the drafting spec). This is a bounded-authorization violation, distinct from inheritance read-scope discipline.

The check is bounded by what audit-CC can observe in interim reports and verification logs; full read-pattern reconstruction is not always possible.

### 4.14 Intra-document section reference convention (prefix-explicit for cross-bible; unprefixed permitted intra-document)

*Banked: Phase 1 Cohort parallel-cohort handoff, 2026-05-08*

#### Abstract rule

Section references within a bible (intra-document) may use unprefixed form: `§ 5.4` resolves to "this document's § 5.4." Section references across bibles (cross-bible) must use prefix-explicit form: `bible_name:5.4` or `BIBLE_STRUCTURE_SPEC v6 § 5.4` (with version anchor when citing locked authority).

The convention prevents ambiguity: a Phase 1 bible's body that says "per § 5.4" without prefix should always resolve to the same bible's § 5.4; cross-bible references require explicit naming so the reference target is unambiguous regardless of where the reading session has scrolled to.

The convention is operative across the corpus; per-document templates and shared templates both follow it.

#### Worked example

The lesson emerged across multiple Phase 1 Cohort cycles where ambiguous mid-document references ("per § 5.4" in a context where multiple bibles were under discussion) caused audit-CC and patch-CC to pause and resolve. The discipline was banked at the parallel-cohort handoff: prefix-explicit for cross-bible (the dominant case in cross-cutting content); unprefixed permitted for intra-document (the dominant case in single-bible body content).

The convention pairs with the W.N letter-prefix convention (per § 4.5 and BIBLE_STRUCTURE_SPEC v6 § 5.5): cross-bible bug references already require `bible_name:8.W.<n>` form; the broader rule generalizes the cross-bible-prefix mandate to all section references that cross document boundaries.

#### Cross-references

- **Origin:** Phase 1 Cohort parallel-cohort handoff (2026-05-08).
- **W.N letter-prefix convention (cross-bible bug-tracking forcing function):** BIBLE_STRUCTURE_SPEC v6 § 5.5; META_PLAN v9 § 7.11.
- **Related:** § 4.5 (Pattern-completion interpolation pattern — the W.N convention's authorization scope).

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible's body content and cross-references:

1. **Grep all section references in the bible body for unprefixed forms** (`§ <n>.<n>` or analogous).
2. **For each unprefixed reference, verify the target section exists in the same bible** (intra-document resolution).
3. **For each cross-bible reference, verify it uses prefix-explicit form** (`bible_name:<n>.<n>` or `BIBLE_NAME v<N> § <n>.<n>`).
4. **Flag as MINOR if** an intra-document reference is incorrectly prefix-explicit (style inconsistency, not a load-bearing failure).
5. **Flag as MATERIAL if** a cross-bible reference uses unprefixed form (audit-CC cannot trivially resolve to the correct target document; readers face same ambiguity).

The check is mechanical for the intra-document-resolution direction; the cross-bible-reference direction requires audit-CC to verify against the seven-bible corpus enumeration.

### 4.15 Composite-row treatment for orphan classes (per BIBLE_STRUCTURE_SPEC v6 § 5.6.1.2 tertiary-state notation; CONDITIONAL discipline applied at row-level rather than W.N-trigger-level)

*Banked: Phase 1 Cohort parallel-cohort handoff, 2026-05-08*

#### Abstract rule

When a bible's per-document content includes a small number of rows that don't fit cleanly into the document's primary class taxonomy ("orphan rows"), the rows receive composite-row treatment: explicit classification + provenance + scope-statement for audit traceability, rather than being silently absorbed into a misleading parent class. The pattern parallels BIBLE_STRUCTURE_SPEC v6 § 5.6.1.2's tertiary-state notation CONDITIONAL discipline (where a trigger that applies with an explicit caveat requires the drafter to document the caveat in adjacent prose, rather than escape-hatching to a soft classification).

Orphan rows are common at the boundaries of taxonomies (e.g., a feature whose category is "experimental, not yet classified"); composite-row treatment surfaces the orphan status rather than forcing fit. The discipline trades a small amount of structural irregularity for explicit auditability.

#### Worked example

The lesson emerged from FP cycle (Feature Provenance Bible). FP's row F-81 was an ORPHAN composite — a feature row that did not fit the bible's primary Speed (4) + Trajectory (7) + Class (3) decomposition for the 14 Gonzo Sauce features. Rather than silently mapping F-81 to one of the existing classes, FP's drafting CC authored F-81 with an explicit composite-row structure: `Class: ORPHAN | Provenance: <cycle citation> | Scope: <explicit narrowing>`. Audit-CC could trace the orphan status; future cycles can re-classify or maintain orphan status with full provenance.

The pattern is BIBLE_STRUCTURE_SPEC v6 § 5.6.1.2's tertiary-state CONDITIONAL discipline applied at row-level rather than W.N-trigger-level: where § 5.6.1.2's CONDITIONAL state mandates adjacent-prose documentation of the caveat to prevent the tertiary state from becoming an escape hatch, composite-row treatment mandates explicit classification + provenance + scope-statement to prevent the orphan-row pattern from becoming a soft-classification escape hatch.

#### Cross-references

- **Origin:** Phase 1 Cohort parallel-cohort handoff (2026-05-08); FP cycle (F-81 ORPHAN composite).
- **Tertiary-state notation parallel:** BIBLE_STRUCTURE_SPEC v6 § 5.6.1.2 (CONDITIONAL state's adjacent-prose mandate parallels composite-row's explicit-classification + provenance + scope-statement mandate).

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible whose primary class taxonomy is being applied at row level:

1. **Identify rows that fall outside the primary class taxonomy.** Compare each row's classification to the bible's stated class enumeration.
2. **For orphan rows, verify composite-row treatment is applied** — explicit classification (e.g., `ORPHAN`), provenance (which cycle introduced or surfaced the orphan status), and scope-statement (what makes this row orphan rather than fitting an existing class).
3. **Flag as MATERIAL if** an orphan row is silently mapped to an established class without composite-row treatment, particularly if the misclassification affects downstream cross-references.
4. **Flag as MINOR if** an orphan row carries composite-row treatment without all three elements (classification + provenance + scope-statement).

### 4.16 Lock-CC three-element metadata bundle (header status field + revision history block + end-of-document footer)

*Banked: Phase 1 Cohort parallel-cohort handoff, 2026-05-08*

#### Abstract rule

When a Phase 1 (or Phase 0) document reaches lock-CC tier, lock-CC ensures the document carries a three-element metadata bundle:

1. **Header status field** at top of document: Status (LOCKED / DRAFT vN), Authorship date, Owner ratification, Lock state transitions.
2. **Revision history block** post-header: chronological record of vN transitions with date, scope of change, ratification owner per version.
3. **End-of-document footer**: Lock-state confirmation, Authorship CC tier (drafting CC), Audit CC tier, Patch CC tier (if patch dispatched), Lock CC tier, Ratification owner.

The three-element bundle ensures every locked document carries authoritative metadata in three load-bearing locations, enabling readers to identify version-state, history, and lock status from any of three vantage points without cross-document lookup.

The bundle is initialized at v1-draft authorship per § 4.18 (drafting-CC paste-prompts must mandate metadata-bundle initialization at v1-draft authorship), but lock-CC is responsible for finalizing the three elements at lock tier — populating audit/patch/lock CC tier fields, transitioning Lock state from DRAFT to LOCKED, finalizing revision-history entry for the lock cycle.

The bundle is metadata, not content — see § 4.17 for the locked-document-content preservation rule (drafting-time historical context preserved; metadata transitions permitted).

#### Worked example

The lesson emerged across the Phase 1 Cohort cycles. Three patterns were observed across the seven Phase 1 bible cycles: FP (Feature Provenance) cycle had a rich metadata bundle from drafting CC's v1 authorship; MLA (ML Layer Architecture) cycle had a minimal bundle requiring lock-CC supplementation; MER (Model Evaluation & Retraining) cycle had a hybrid bundle. The variance indicated standardization was needed; the parallel-cohort handoff banked the standardization mandate.

#### Cross-references

- **Origin:** Phase 1 Cohort parallel-cohort handoff (2026-05-08).
- **v1-draft mandate sibling:** § 4.18 (drafting-CC paste-prompts must mandate metadata-bundle initialization at v1-draft authorship).
- **Locked-content preservation sibling:** § 4.17 (locked bibles preserve drafting-time historical context in narrative sections).
- **Inaugural application:** AUDIT_METHODOLOGY v3 itself initializes the three-element bundle (header status field at top of this document; revision history block at top of this document; end-of-document footer at end of this document — see end-of-document footer for reference (immediately following § 12)).

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible at lock tier (or drafting tier with bundle-initialization requirement):

1. **Verify header status field exists** at top of document with Status, Authorship date, Owner ratification, Lock state. Flag missing or partial fields.
2. **Verify revision history block exists** post-header with chronological record of vN transitions. Flag missing block; flag missing per-version date/scope/ratification fields.
3. **Verify end-of-document footer exists** with lock-state confirmation, authorship CC tier, audit/patch/lock CC tier fields, ratification owner. Flag missing footer; flag missing fields.
4. **Flag as MATERIAL if** any element of the three-element bundle is absent at lock tier.
5. **Flag as MINOR if** all three elements exist but one or more sub-fields is missing or stale.

### 4.17 Locked bibles preserve drafting-time historical context in narrative sections; lock-CC scope distinguishes metadata vs content

*Banked: Phase 1 Cohort parallel-cohort handoff, 2026-05-08*

#### Abstract rule

When lock-CC tier promotes a document from DRAFT to LOCKED, lock-CC does NOT retroactively rewrite drafting-time content. Narrative sections, scope statements, framework descriptions, contextual references — the document's body content — are preserved verbatim from the drafting cycle. Lock-CC's scope is metadata transitions (Status field, Lock state designation, footer population, revision-history entry for the lock cycle) and surgical patches if audit-CC findings warrant them; not retroactive rewriting of content that was authored at drafting-time and reflects drafting-time substrate state.

The distinction is sharp:

- **Metadata** (lock-CC may transition): version-state designations, lock-state markers, footer fields, revision-history entries, header date fields.
- **Content** (lock-CC preserves): narrative descriptions, contextual references, drafting-time framework citations, worked examples, cross-references that resolved at drafting time.

The preservation rule protects against the failure mode where lock-CC, acting under "make this document lock-ready" mandate, rewrites drafting-time content in ways that lose the document's historical-evolution traceability. Drafting-time content carries the cycle's authorship state; preserving it across lock tier preserves the document's audit-trail.

#### Worked example

The lesson emerged across the Phase 1 Cohort cycles. Lock-CC tier observed in some cycles (FP, others) attempted to rewrite drafting-time framework citations to current Phase 0 lock versions retroactively, which obscured the drafting cycle's actual citation state. The parallel-cohort handoff banked the discipline: lock-CC preserves drafting-time content; cross-reference re-validation at version-bump (e.g., META_PLAN v6→v9) is in-scope for drafting CC at v(N+1) authorship, not for lock-CC at vN lock tier.

#### Cross-references

- **Origin:** Phase 1 Cohort parallel-cohort handoff (2026-05-08).
- **Three-element metadata bundle sibling:** § 4.16 (lock-CC's metadata-transition scope).
- **Drafting CC mandate sibling:** § 4.18 (drafting CC initializes bundle).

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible at lock tier (or post-lock surveillance):

1. **For each section beyond the metadata bundle, verify drafting-time content is preserved.** Compare lock-tier text against drafting-time text (where drafting-time text is recoverable from interim deliverables).
2. **Distinguish content rewrites from cross-reference re-validation updates.** The latter is in-scope for next-cycle drafting CC; lock-CC does not perform retroactive cross-reference updates as part of lock tier.
3. **Flag as MATERIAL if** lock-CC retroactively rewrote drafting-time content (narrative sections, scope statements, framework descriptions) at lock tier.
4. **Flag as MINOR if** lock-CC's metadata transitions touch fields that arguably belong to content rather than metadata (e.g., scope-statement language that reads as content but is structured as metadata).

### 4.18 Drafting-CC paste-prompts must mandate metadata-bundle initialization at v1-draft authorship

*Banked: Phase 1 Cohort parallel-cohort handoff, 2026-05-08*

#### Abstract rule

When QB authors a drafting-CC paste-prompt for a Phase 1 (or Phase 0) bible cycle, the paste-prompt must explicitly mandate three-element metadata bundle initialization at v1-draft authorship. Drafting CC initializes the header status field skeleton, the revision history block skeleton, and the end-of-document footer skeleton at v1-draft tier; lock-CC populates the final values at lock tier (per § 4.16).

The mandate is structural: drafting CC does not author metadata bundle content speculatively; QB's paste-prompt explicitly directs initialization. Without the explicit mandate, drafting CCs produce variable bundle states (the FP-rich / MLA-minimal / MER-hybrid pattern observed across the Phase 1 Cohort), which creates lock-CC tier rework.

The mandate complements but does not duplicate § 4.16's lock-CC scope: drafting CC initializes; lock-CC finalizes; both tiers are required.

#### Worked example

The lesson emerged across the Phase 1 Cohort cycles. Three observed patterns:

- **FP-rich** (Feature Provenance Bible): drafting CC initialized full bundle skeleton with rich metadata at v1-draft; lock-CC's finalization scope was minimal.
- **MLA-minimal** (ML Layer Architecture Bible): drafting CC initialized only header status field; lock-CC's finalization scope included authoring revision-history block and footer from scratch.
- **MER-hybrid** (Model Evaluation & Retraining Bible): drafting CC initialized header + footer; lock-CC's finalization scope included authoring revision-history block from scratch.

The variance indicated standardization was needed at the QB-paste-prompt-authorship surface. The parallel-cohort handoff banked the mandate: drafting-CC paste-prompts for future cycles MUST direct three-element bundle initialization at v1-draft tier. The mandate is operative on the AUDIT_METHODOLOGY v3 cycle itself (this document's drafting CC initializes the bundle per spec § 8 metadata bundle requirements; see § 12 footer for reference).

#### Cross-references

- **Origin:** Phase 1 Cohort parallel-cohort handoff (2026-05-08).
- **Lock-CC scope sibling:** § 4.16 (lock-CC three-element metadata bundle finalization).
- **Locked-content preservation sibling:** § 4.17.
- **Inaugural application:** AUDIT_METHODOLOGY v3 drafting cycle (this document) — drafting CC initialized header + revision-history + footer per § 8 of v3 drafting spec.

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible's drafting cycle:

1. **Examine the drafting-CC paste-prompt** for explicit metadata-bundle-initialization mandate.
2. **Verify drafting CC initialized all three bundle elements at v1-draft tier** (header status field skeleton, revision history block skeleton, end-of-document footer skeleton).
3. **Flag as MATERIAL if** the paste-prompt did not mandate initialization AND drafting CC did not initialize, leaving lock-CC to author all three elements from scratch.
4. **Flag as MINOR if** the paste-prompt mandated initialization but drafting CC partially initialized (e.g., header only, missing revision-history or footer).

### 4.19 QB paste-verbatim discipline reinforcement (QB-tier paste operation: substrate quotation in QB chat output)

*Banked: Phase 1 Cohort parallel-cohort handoff (PHASE_5_BACKLOG.md reconciliation cycle), 2026-05-08*

See § 4.10 for the CC-tier sibling discipline (V1-N verification log entries); this lesson covers the QB-tier paste operation (substrate quotation in QB chat output).

#### Abstract rule

When QB pastes substrate content into chat output (e.g., quoting a line from a Phase 0 lock, citing a verbatim entry from a verification log, reproducing a row from a meta-document), QB pastes the entire line verbatim — not the substantive-content portion only. Partial-line paste, even when the omitted portion is plausibly redundant or contextually obvious, breaks the verbatim-paste discipline that is foundational to substrate-grounded reasoning across the QB orchestration tier.

The rule's scope is QB-tier; the CC-tier sibling discipline (V1-N verification log entries) is at § 4.10. Both lessons share the principle (verbatim paste of substrate content) but apply at different tiers and to different artifact types: § 4.10 governs CC-authored verification log entries; § 4.19 governs QB-authored chat output.

The discipline integrates with QB Self-Audit Check 5 generalization (§ 12.5): meta-document state claims must be substrate-verified at first cycle reference; the reinforcement is that the substrate-verified content is paste-quoted verbatim, not summarized.

#### Worked example

The lesson emerged from the PHASE_5_BACKLOG.md reconciliation cycle (a sub-cycle of the Phase 1 Cohort sequence). QB pasting a line from PHASE_5_BACKLOG.md to surface backlog-vocabulary content paste-quoted only the substantive-content portion of the line, omitting structural metadata (entry ID, severity tag, date stamp) that was contextually unambiguous to QB but load-bearing to the reconciliation cycle. The omitted metadata was the discriminator the reconciliation cycle needed to disambiguate Phase 5.3.1 seed (META_PLAN v6 § 11 vocabulary) from Phase 5.3.2-5.3.26 (TRIAGE_QUEUE_SPEC v1 vocabulary).

The discipline was banked: paste entire line verbatim, not substantive-content portion only. The lesson reinforces § 4.10 at QB tier without duplicating the CC-tier rule.

#### Cross-references

- **Origin:** Phase 1 Cohort parallel-cohort handoff, PHASE_5_BACKLOG.md reconciliation cycle (2026-05-08).
- **CC-tier sibling:** § 4.10 (Verbatim-paste discipline for V1-N entries).
- **Related QB Self-Audit Check:** § 12.5 (meta-document state claim substrate verification).

#### Audit-CC prophylactic check template

When auditing a QB-authored cycle artifact (handoff document, drafting spec, paste-prompt) that quotes substrate content:

1. **For each verbatim-quoted substrate line, verify the entire line was paste-quoted, not the substantive-content portion only.** Look for: line-prefix metadata (entry IDs, severity tags, dates) preserved in the quote.
2. **Flag as MATERIAL if** a partial-line paste affected the cycle's reasoning (e.g., omitted metadata that was the discriminator for a downstream decision).
3. **Flag as MINOR if** a partial-line paste did not affect cycle reasoning but breaks the verbatim discipline (style + reinforcement).

### 4.20 Pattern A bundling default + Pattern B exception

*Banked: API & Frontend Bible cycle, 2026-05-08*

#### Abstract rule

QB bundles content-authoring step with the adjacent spec-write CC paste-prompt step in the same chat turn by default (Pattern A). Deferring content-authoring to a separate chat turn ahead of the spec-write paste-prompt creates a drift surface: if Tony does not respond between turns, or responds with non-ratification, the content authored in the deferred turn risks bypassing ratification gates (the wrapper paste-prompt may not catch unratified content if it was authored ahead).

Pattern B (defer content-authoring to a separate turn) is the exception, applied when QB explicitly flags amendment-likely content: novel structural questions (where Tony's ratification surface is large and amendments are anticipated), unverified substrate claims (where pre-paste verification is needed), low-confidence content (where QB seeks alignment before paste-prompt commitment).

The default is Pattern A; Pattern B applies when QB explicitly justifies the deferral.

#### Worked example

The lesson emerged from the API & Frontend Bible cycle (2026-05-08). Step 5 of the cycle's spec-write process drifted: QB authored content for the spec in one chat turn with explicit deferral language ("I'll author the next portion in the following turn"), and Tony bypassed via direct paste using § 15 self-described authorization. The bypass left the cycle's ledger off-by-one (the wrapper paste-prompt at Step 5 was not exercised because § 15 self-authorization made it redundant).

The lesson banks the default: bundle content-authoring with adjacent spec-write paste-prompt in the same chat turn. The Pattern B exception is reserved for explicitly flagged cases.

#### Cross-references

- **Origin:** API & Frontend Bible cycle, 2026-05-08; Step 5 ledger off-by-one drift.
- **Related QB Self-Audit Check:** § 6.2 (self-describing authorization redundancy detection — the § 15 self-authorization that made the Step 5 wrapper redundant).

#### Audit-CC prophylactic check template

When auditing a QB-authored cycle's chat-turn structure (where reconstructable):

1. **For each content-authoring step, verify it was bundled with the adjacent spec-write CC paste-prompt step in the same chat turn (Pattern A default).**
2. **For deferred-authoring (Pattern B) instances, verify QB explicitly flagged the deferral with justification** (novel structural question, unverified substrate, low-confidence content).
3. **Flag as MINOR if** a deferred-authoring instance lacks Pattern B justification.
4. **Flag as MATERIAL if** the deferral resulted in a bypass of ratification gates (wrapper paste-prompt rendered redundant; off-by-one ledger drift; etc.).

### 4.21 UC-cycle audit-scope methodology lesson (UPSTREAM-CORRECTION cycle scope determines audit cycle requirement)

*Banked: UC-1 cycle, 2026-05-08*

#### Abstract rule

UPSTREAM-CORRECTION (UC) cycles are post-lock surgical patches to a locked Phase 1 (or Phase 0) document, scoped to address upstream substrate drift surfaced after lock. The cycle's scope determines the audit cycle requirement:

- **Surgical row patch** (single locus + substrate-grounded; e.g., a single § X.Y row's content amended per upstream evidence): QB-audit synthesis tier suffices. QB synthesizes the patch's audit findings from the patch CC's interim outputs; no fresh audit-CC session required.
- **Section-scope or wider** (multiple loci; cross-reference cascade; methodology-shape changes): fresh audit-CC session required. The wider scope's adversarial verification needs the independent eye of a fresh CC session.

The discriminator is scope, not patch type. A surgical row patch with substrate-grounded single-locus changes is light-audit-tier; anything wider is audit-CC-tier.

#### Worked example

The lesson emerged from the UC-1 cycle (Architecture Overview v3-patched-a, 2026-05-08). UC-1 was a surgical row patch to § 3.1 equine-inference Lambda role drift, with single-locus substrate-grounded changes per V1-14 substrate evidence. The cycle dispatched under bounded authorization, applied the patch, and reached audit tier. The audit-tier dispatch ratified Q5 Option C (QB-audit synthesis tier) over Q5 Option B (fresh audit-CC); QB-audit's 4/4 PASS validated the lighter audit tier as appropriate for surgical scope.

Had UC-1's scope been section-wide (e.g., affecting multiple subsections within § 3, or cascading to other documents' cross-references), the lighter audit tier would have been mis-sized; fresh audit-CC dispatch would have been the appropriate tier.

#### Cross-references

- **Origin:** UC-1 cycle, 2026-05-08; Q5 ratification (Option C QB-audit synthesis tier).
- **Worked example artifact:** Architecture Overview v3-patched-a (locked 2026-05-08); V1-14 substrate evidence.

#### Audit-CC prophylactic check template

When evaluating an UPSTREAM-CORRECTION cycle's audit-tier appropriateness (post-lock):

1. **Identify the patch scope.** Single locus + substrate-grounded = surgical row patch; multiple loci OR cross-reference cascade OR methodology-shape change = section-scope or wider.
2. **For surgical row patches, verify audit-tier was QB-audit synthesis tier** (QB synthesized findings from patch CC's interim outputs).
3. **For section-scope or wider, verify a fresh audit-CC session was dispatched.**
4. **Flag as MATERIAL if** a section-scope-or-wider UC-cycle was audited at QB-audit synthesis tier (under-sized audit). Flag as MINOR if a surgical row patch was audited at fresh audit-CC tier (over-sized audit, but defensible).

### 4.22 Two-tier cross-reference convention codification (carried-forward deferral from parallel cohort)

*Carried-forward deferral from parallel cohort, codified at 2026-05-08*

#### Abstract rule

Cross-reference notation operates at two tiers: tier 1 (intra-document) uses unprefixed `§ X.Y` form; tier 2 (cross-bible) uses prefix-explicit `bible_name:X.Y` form. The two-tier convention is the formal codification of the discipline introduced at § 4.14 (intra-document section reference convention).

This lesson carries forward the deferral from the parallel cohort's Q9 (cross-reference convention codification): the convention was operative across cycles before formal codification; this lesson codifies it. The two-tier framing aligns the convention with the existing W.N letter-prefix convention's tier separation (W.N references are inherently cross-bible per the bug-tracking forcing function; intra-bible W.N references are within-document numeric subsections).

The two-tier convention extends to: cross-bible bug references (`bible_name:8.W.<n>` always), cross-bible section references (`bible_name:5.4` always), intra-bible section references (`§ 5.4` permitted unprefixed), intra-bible subsection references (`§ 4.6.2` permitted unprefixed within § 4.6's parent).

#### Worked example

The lesson was originally surfaced in the parallel-cohort cycle as Q9 (cross-reference convention codification deferral). The deferral propagated across multiple cycles (Database & Schema, Data Pipeline, Feature Provenance) without formal codification, though the convention was operatively followed. The AUDIT_METHODOLOGY v3 meta-cycle banks the codification per this lesson.

#### Cross-references

- **Origin:** Parallel-cohort cycle Q9 deferral, carried forward across multiple Phase 1 cycles, codified at AUDIT_METHODOLOGY v3 (2026-05-08).
- **Companion lesson:** § 4.14 (intra-document section reference convention).
- **W.N letter-prefix convention:** BIBLE_STRUCTURE_SPEC v6 § 5.5; META_PLAN v9 § 7.11.

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible's cross-references:

1. **Categorize each reference as tier 1 (intra-document) or tier 2 (cross-bible).**
2. **Verify tier 1 references use unprefixed form** (or are explicitly prefix-formatted with no semantic loss).
3. **Verify tier 2 references use prefix-explicit form** (`bible_name:X.Y` or `BIBLE_NAME v<N> § X.Y`).
4. **Flag mixed-tier inconsistencies** as MINOR; flag tier 2 unprefixed references as MATERIAL (resolution ambiguity).

### 4.23 database_schema_bible:V1-12 verification-log-claim-ID convention (carried-forward deferral from Database & Schema Bible cycle)

*Carried-forward deferral from Database & Schema Bible cycle, codified at 2026-05-08*

#### Abstract rule

Verification log claim IDs follow the convention `V<bible_version>-<claim_number>` (e.g., `V1-12` for the 12th claim in v1's verification log). Cross-bible references to verification log claims use prefix-explicit form: `bible_name:V<n>-<m>` (e.g., `database_schema_bible:V1-12`).

The convention was operative in the Database & Schema Bible v1 cycle but had not been formally codified at AUDIT_METHODOLOGY tier; this lesson carries forward the codification deferral.

The claim-ID convention pairs with § 4.10 (verbatim-paste discipline for V1-N entries): V1-N entries are addressable by claim ID; claim IDs are the audit-CC's reference handle to specific verification claims. Cross-bible audit reports cite verification log claims by claim ID; the prefix-explicit form per § 4.22 (two-tier cross-reference convention) is mandatory.

#### Worked example

The lesson originally surfaced in the Database & Schema Bible v1 cycle when audit-CC's report cited V1-N entries by claim ID (e.g., "V1-12 substrate evidence cited") and the convention was operative. The codification was deferred at the cycle's lock and carried forward; AUDIT_METHODOLOGY v3 banks the codification per this lesson.

The convention is also operative across the Phase 1 Cohort cycles (each bible's verification log uses the V<bible_version>-<claim_number> format).

#### Cross-references

- **Origin:** Database & Schema Bible v1 cycle, deferral carried forward across Phase 1 Cohort cycles, codified at AUDIT_METHODOLOGY v3 (2026-05-08).
- **Companion lessons:** § 4.10 (Verbatim-paste discipline for V1-N entries); § 4.22 (two-tier cross-reference convention codification).

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible's verification log:

1. **Verify claim IDs follow `V<bible_version>-<claim_number>` format** consistently throughout the log.
2. **For cross-bible audit reports citing verification log claims, verify prefix-explicit form** (`bible_name:V<n>-<m>`).
3. **Flag as MINOR** if claim ID format deviates within a single verification log (style inconsistency).
4. **Flag as MATERIAL** if a cross-bible audit cites a verification log claim without prefix-explicit form (resolution ambiguity at audit-trail).

### 4.24 Verbatim-paste verlog-growth modeling (carried-forward deferral from prior cycle)

*Carried-forward deferral from prior cycle, codified at 2026-05-08*

#### Abstract rule

Verbatim-paste discipline (§ 4.10 CC-tier; § 4.19 QB-tier) increases verification log size relative to summarization-based logs. Drafting specs that mandate verbatim-paste must model expected verlog (verification log) growth at spec authorship: predicted verlog size = baseline summarization size × verbosity multiplier (typically 1.5x–3x depending on command output verbosity).

The modeling is operational, not methodology-prescriptive: drafting specs allocate verlog read-budget per the predicted size; QB and audit-CC anticipate the larger reads. The lesson protects against the failure mode where a drafting spec mandates verbatim-paste but does not model the resulting verlog growth, leaving downstream audit cycles surprised by read-budget consumption.

The modeling does not introduce a methodology threshold; it is a planning aid for cycle resource allocation.

#### Worked example

The lesson originally surfaced in a prior cycle (specific cycle attribution carried forward as deferral, not substrate-verified at this codification tier per Lesson § 4.12 generalization — the substrate evidence is the cycle artifacts themselves). Verbatim-paste-mandated cycles produced verification logs 1.5x–3x larger than summarization-based predecessors. The growth pattern was banked as a planning consideration; the codification was deferred and carried forward.

The lesson does not prescribe a specific verbosity multiplier — the multiplier varies per cycle's command-mix. Drafting CC at spec-write tier estimates per the cycle's expected V1-N entry count and per-entry command-output size.

#### Cross-references

- **Origin:** Prior cycle deferral (specific origin carried forward without substrate verification at this codification tier), codified at AUDIT_METHODOLOGY v3 (2026-05-08).
- **CC-tier verbatim-paste discipline:** § 4.10.
- **QB-tier verbatim-paste discipline:** § 4.19.

#### Audit-CC prophylactic check template

When auditing a Phase 1 bible's drafting cycle resource allocation:

1. **Verify the drafting spec models expected verlog growth** when verbatim-paste is mandated. Look for: predicted verlog line count, baseline-vs-verbatim multiplier estimate, read-budget allocation.
2. **Flag as MINOR if** the drafting spec mandates verbatim-paste without verlog-growth modeling (planning gap; not a methodology violation).
3. **Flag as STYLE if** the modeling is present but the multiplier estimate diverged materially from actual (post-cycle observation, not pre-cycle predictability).

The check applies to drafting specs that mandate verbatim-paste; it does not apply to specs that do not require verbatim-paste.

§ 4.25–§ 4.31: seven lessons banked at v3-patched-a (Phase A D6 bundled bible patches dispatch, 2026-05-12; substrate `docs/operations/PHASE_A_HANDOFF_2026-05-12.md` §§ 2.1 / 2.2 / 6.2).

### 4.25 Code-passes-review-without-implementation-reality-verified (script vs service summary-dict)

#### Abstract rule

A script's read-key assumption can pass code review (and even tests) when the service-summary-dict structure isn't independently verified at script-write-time. When a script consumes a service-returned summary dict, the read-key set must be verified to match the service's actual return-key set at the implementation site, not the script-author's assumption.

#### Worked example

Phase A D2 backfill script (`scripts/backfill_d2.py`) was authored expecting `result.get("entries_inserted")` and `result.get("count")` keys from the IngestionService summary; the service actually returned the `races_stored` key. The script reported "Entries=0" for runs that did write rows. Caught at A.6.b bundle troubleshooting (drafting CC tier review against operator-supplied run-log output); fix substituted `result.get("races_stored", 0)`. The cosmetic "0 entries" output masked successful operation — operator confusion at run-time was the only signal.

#### Cross-references

- **Phase A handoff substrate:** `docs/operations/PHASE_A_HANDOFF_2026-05-12.md` § 2.1 pattern entry 1.
- **Dispatch report:** A.6.b bundle (drafting CC + Tony saved-diff review).
- **Substrate file:** `scripts/backfill_d2.py` (current state post-A.6.b fix).

#### Audit-CC prophylactic check template

When the audited document references a script that reads from a service-returned summary-dict:

1. **Verify both substrates: script read-key calls + service return-dict keys at implementation site.** Both required; script-side alone is insufficient.
2. **Enumerate `result.get("X")` patterns in the script.** Cross-check against the service's documented or implementation-grounded return-key set.
3. **Flag MATERIAL** when read-key/return-key mismatch detected and the script's behavior depends on the mismatched key (script writes successful when key missing → cosmetic-only bug; script raises or zero-paths through critical logic → MATERIAL substrate defect).

### 4.26 Documentation-not-substrate-grounded (function docstring vs implementation divergence)

#### Abstract rule

Function docstrings can drift from implementation. Callers reading docstrings to determine return-tuple structure or function signature may mis-unpack returns, producing TypeError or silent shape-mismatch errors. When the audited document references a function's behavior, the reference must trace to implementation substrate, not to docstring.

#### Worked example

`backend/lambdas/nyra-workouts/handler.py` `fetch_track_page` and `parse_nyra_html` docstrings claimed singular returns; implementation returned 2-tuples. The Phase A D2 backfill script called `html = nyra_handler.fetch_track_page(...)` and received a tuple, producing `TypeError: expected string or bytes-like object, got 'tuple'`. A.6.a diagnostic surfaced the V-N2 caller-side tuple-unpack mismatch; A.6.b bundle fix substituted `url, html = nyra_handler.fetch_track_page(...)` + `rows, stats = nyra_handler.parse_nyra_html(...)`.

#### Cross-references

- **Phase A handoff substrate:** `docs/operations/PHASE_A_HANDOFF_2026-05-12.md` § 2.1 pattern entry 2.
- **Dispatch reports:** A.6.a (TypeError diagnostic) + A.6.b (fix bundle).
- **Substrate file:** `backend/lambdas/nyra-workouts/handler.py` (docstring-vs-implementation divergence preserved post-A.6.b; D6 documentation candidate per Phase A handoff).

#### Audit-CC prophylactic check template

When the audited document references a function by docstring-described signature:

1. **Verify the docstring's return-shape claim against the implementation's `return` statement(s).** The implementation is canonical; docstring may be stale.
2. **For cross-module callers** (script, Lambda, service-layer caller): verify the caller-side unpack pattern matches the implementation's return shape, not the docstring's claim.
3. **Flag MATERIAL** for docstring-implementation divergence when downstream callers rely on the divergent claim.

### 4.27 Inference-promoted-to-substrate-fact-without-Tony-confirmation (A.6.d case study)

#### Abstract rule

When operational behavior is inferred from substrate evidence (S3 writes, IAM role usage patterns, log-line timestamps, code-symmetry between training and inference), the inference must be flagged as inference in the audited document — not propagated as substrate-verified fact. Per Phase A producer-attribution methodology refinement (§ 4.31 below), explicit Tony confirmation or substrate-direct verification is required to promote operational-signal inference to operational reality.

#### Worked example

Phase A A.6.d CC report inferred "Tony's local HRN scrape ~4000 rows/day" from log signals + OCRC IAM-role attribution (E1 substrate at v3-patched-b § 3.9). Tony flagged the inference as not-verified. A.6.f verification surfaced the actual producer: `/home/strakajagr/equibase_scraper/run_daily_refresh.sh` — sibling repo on Tony's local machine, Equibase scraper, not HRN. The "~4000 rows/day" volume claim was also misread — the Lambda `inserted=N` log value is records-processed-from-JSON, not net-new-DB-inserts; UPSERT collapse yields ~12-22% of file volume as net-new rows (per A.6.f investigation). Producer-attribution at IAM-role level (OCRC-class finding) does NOT establish operational-producer attribution.

#### Cross-references

- **Phase A handoff substrate:** `docs/operations/PHASE_A_HANDOFF_2026-05-12.md` § 2.1 pattern entry 3.
- **Methodology refinement banking:** § 4.31 below (5-case-study catalog including this instance).
- **Dispatch reports:** A.6.d (CC inference) + A.6.f (Tony-flagged verification surfacing actual producer).
- **Substrate file (actual producer):** `/home/strakajagr/equibase_scraper/run_daily_refresh.sh` (sibling repo).

#### Audit-CC prophylactic check template

When the audited document characterizes operational behavior (daily producer attribution, schedule timing, throughput volumes, data-flow attribution):

1. **Classify each claim**: substrate-direct-verified (cron-defined schedule citation; function-source-code citation; DB-direct row count; live-AWS API response) vs operational-signal-inference (S3 write pattern; log-line timestamp; IAM-role attribution; code-symmetry between training and inference).
2. **For inference-class claims**: verify the document flags the claim as inference (e.g., "operationally inferred from log signal X" rather than "operationally Y"). Operational-signal-inference presented as fact without explicit flagging triggers the rule.
3. **Flag MATERIAL** for inference-presented-as-fact without explicit inference-flagging OR Tony-confirmation citation.

Per § 4.31, IAM-role attribution alone does not establish producer attribution at operational layer (multiple operational actors can consume a shared IAM role).

### 4.28 Dispatch-text-framing-inherited-from-session-memory-not-substrate-verified (HRN CAPTCHA case study)

#### Abstract rule

Framing carried over from prior cycles into dispatch text without substrate re-verification can propagate stale or wrong claims. Session-memory inheritance (CC's recall of prior-cycle claims) does not constitute substrate verification. Dispatch-text framing must trace to substrate at dispatch-authorship time, not to memory.

#### Worked example

Phase A pre-A.6.d framing assumed CAPTCHA-gating on the HRN workouts scraper at `backend/services/data_sources/hrn_workout_scraper.py:66`. Substrate inspection 2026-05-12 (during A.6.d → A.6.f investigation) proved "no CAPTCHA or bot-protection" at the cited location. The CAPTCHA framing had been inherited from session memory of an earlier Bug #7 disposition cycle, never re-verified at A.6.d dispatch authorship. The framing propagated through QB → CC dispatch text into A.6.d CC report's reasoning before A.6.f substrate verification surfaced the divergence.

#### Cross-references

- **Phase A handoff substrate:** `docs/operations/PHASE_A_HANDOFF_2026-05-12.md` § 2.1 pattern entry 4.
- **Dispatch report:** A.6.d (CC report carrying inherited framing) + A.6.f (substrate verification).
- **Substrate file:** `backend/services/data_sources/hrn_workout_scraper.py:66` (current state — no CAPTCHA/bot-protection).

#### Audit-CC prophylactic check template

When the audited document references operational details inherited from prior cycles (CAPTCHA gating, bot-protection, scraper limitations, third-party-source behavior, deprecated infrastructure characteristics):

1. **Verify each inherited detail against current substrate.** Substrate citation required: file:line for code claims; live-AWS API response for resource claims; recent dispatch report for transient operational state.
2. **Session-memory citation insufficient.** "Per CC recall from prior cycle" is not a substrate citation.
3. **Flag MATERIAL** for session-memory-inherited claims not re-verified at the audited document's authorship-time.

### 4.29 QB-framing-not-substrate-verified-before-propagation (D4 Source 2 conflation case study)

#### Abstract rule

QB dispatch-text framing of operational architecture may conflate distinct entities (Lambda vs Lambda-action; rule-name vs Lambda-name; cron-schedule vs Lambda-invocation-timing). Ratified-by-Tony scope can inherit the conflation if CC doesn't verify entity-level claims against substrate before propagating them through dispatch text.

#### Worked example

Phase A D4 dispatch text (authored by QB) described Source 2 as "equine-results Lambda; cron 04:00 UTC via equine-fetch-results-nightly post-OCRC Input fix". Substrate verification at D4 execution:
- HRN-results-scraping = `equine-ingestion` Lambda's `fetch_results` action @ 01:30 UTC via EventBridge rule `equine-fetch-results-nightly` (Input payload `{"action":"fetch_results","date":"USE_TODAY_MINUS_1"}` per architecture_overview:3.6 line 151 InputTransformer).
- `equine-results` matcher Lambda is a SEPARATE reconciliation Lambda @ 04:00 UTC via EventBridge rule `equine-results-daily` (purpose-built, single-flow per architecture_overview:3.1).

QB conflated two distinct Lambda entities into a single "equine-results" framing. CC verified independently and surfaced the correction at D4 CC report.

#### Cross-references

- **Phase A handoff substrate:** `docs/operations/PHASE_A_HANDOFF_2026-05-12.md` § 2.1 pattern entry 5.
- **Dispatch report:** D4 (5-source operational enumeration with substrate correction).
- **Substrate cross-references:** `architecture_overview.md` § 3.1 (Lambda inventory enumerating `equine-ingestion` + `equine-results` distinctly) + § 3.6 (EventBridge rule inventory enumerating `equine-fetch-results-nightly` + `equine-results-daily` distinctly).

#### Audit-CC prophylactic check template

When QB framing of operational architecture is propagated through dispatch text:

1. **Verify each entity-level claim against substrate.** Specifically check: Lambda names, EventBridge rule names, cron schedules, Lambda actions (default-case vs admin-action dispatch).
2. **Cross-reference architecture_overview substrate** for Lambda inventory and EventBridge rule inventory.
3. **Flag MATERIAL** for QB-framing-not-substrate-verified-before-propagation when entity conflation detected. CC's halt-and-surface protocol is the correct response.

### 4.30 Dispatch-text-step-ordering-vs-API-dependency-requirements-mismatch (A.5-ext case study)

#### Abstract rule

Dispatch-text-prescribed step ordering must match API dependency requirements, not logical-deliverable order. AWS APIs that validate dependencies at API time require dependency-grant precedes config-write. QB dispatch text that prescribes logical-deliverable order may produce InvalidParameterValueException at API time if dependency-grants are not pre-applied.

#### Worked example

A.5-ext CC executed dispatch text in literal order:
- Step 2: `aws lambda put-function-event-invoke-config ... --destination-config '{"OnFailure":{"Destination":"<DLQ ARN>"}}'`
- Step 3: `aws iam put-role-policy ... AsyncDLQSend` granting `sqs:SendMessage` on DLQ.

Lambda's `PutFunctionEventInvokeConfig` API validates `sqs:SendMessage` permission on the destination at API time; Step 2 failed with `InvalidParameterValueException: The function execution role does not have permissions to call SendMessage on arn:aws:sqs:us-east-1:584812014683:equine-async-failure-dlq` before Step 3's IAM grant was applied. Recovery: reapply Step 2 after Step 3 succeeded; passed on first retry, no IAM-propagation lag observed.

The earlier Phase A-prime DLQ wiring (5 Lambdas) and A.5 DLQ wiring (3 Lambdas) executed correctly because CC discretion chained IAM-grant before event-invoke-config (masking the dispatch-text inversion). A.5-ext (1 Lambda, executed literal) surfaced the dependency requirement.

#### Cross-references

- **Phase A handoff substrate:** `docs/operations/PHASE_A_HANDOFF_2026-05-12.md` § 2.1 pattern entry 6 + § 2.3 AWS API validation discipline.
- **Bible cross-reference:** `data_pipeline_bible:4.5` (AWS API validation discipline section, D6 patched).
- **Dispatch report:** A.5-ext (NYRA workouts Lambda DLQ wiring; F-D4-1-α closure).
- **AWS API behavior reference:** Lambda `PutFunctionEventInvokeConfig` API documentation (validates IAM permissions at API time).

#### Audit-CC prophylactic check template

When the audited dispatch text prescribes step ordering for AWS resource provisioning (event-invoke-configs, S3 bucket policies, IAM role attachments, KMS key policies, cross-service ARN destinations):

1. **Verify the prescribed step order matches API dependency requirements.** Specifically:
   - IAM grants on target resources must precede config-writes that validate against those grants.
   - Dependent-resource creates must precede consuming-config writes.
2. **For AWS APIs that validate permissions at API time** (Lambda PutFunctionEventInvokeConfig, S3 PutBucketNotification destination-validation, EventBridge PutTargets ARN-permission-validation): the validation occurs before the config takes effect; grant-precedes-config is mandatory.
3. **Flag METHODOLOGY-INTERPOLATION** for dispatch-text step ordering not API-dependency-validated — QB authoring must validate against API behavior, not against logical-deliverable order.

### 4.31 Producer-attribution methodology refinement (5-case-study banking)

#### Abstract rule

Inference from operational signal does not establish operational reality. Operational signals include: S3 writes, IAM role usage patterns, log-line timestamps, code-symmetry between training and inference, throughput-volume log values. Each signal class supports inference at its own scope; promotion of inference to substrate-verified-fact requires either (a) substrate-direct verification (cron-defined schedule citation, function-source-code citation, DB-direct query, live-AWS API response) or (b) explicit Tony confirmation citation.

The refinement clarifies: producer-attribution at IAM-role level (the OCRC D1 substrate-classification convention) does not establish operational-producer attribution. Multiple operational actors can consume a shared IAM role; multiple producers can write to a shared S3 prefix; multiple consumers can read from a shared DB table. Operational-layer attribution requires identification of the producing entity (cron rule + Lambda + invocation payload), not its IAM role.

#### Worked example

Five case studies banked across Phase A operational cycle:

1. **A.6.c ambient delta speculation → DB-state-verified absence.** `rerun_inference` summary reported "LS=152 vs WR/PL=151"; CC speculation classified as "coupled-entry / AE handling artifact." A.6.c discriminating-entries query against `wr_predictions` ∪ `pl_predictions` ∪ `ls_predictions` filtered to AE/coupled returned ZERO rows; speculation disproven by substrate-direct DB query.

2. **A.6.d → A.6.f workouts producer attribution** (also catalogued at § 4.27 above). A.6.d inferred local HRN scrape from log signals + OCRC IAM-role attribution; Tony flagged inference; A.6.f surfaced actual producer (sibling-repo Equibase scraper). Five-element substrate chain (cron-defined schedule + script-source-code + S3-write-attribution + DB-row-count + Tony confirmation) verified actual producer.

3. **A.5.2 gonzo defect classification.** D1-defect verdict required substrate trace through 11 `compute_*` helpers + CloudWatch logs forensic + 'Tapit Shoes' discriminator analysis. Classification NOT inferred from code-symmetry between training and inference; substrate-direct trace through inference exception-suppression path.

4. **A.5.3 checkpoint #11 training behavior inference.** CC claimed "training-time same-helper run will silently filter same NaN rows" from code-symmetry. Methodology refinement applied prophylactically: claim recognized as inference-not-substrate-verified; deferred to Phase B substrate review of training pipeline rather than promoted to fact at A.5.3 fix scope.

5. **D4 Source 2 architecture conflation** (also catalogued at § 4.29 above). QB framing of `equine-ingestion fetch_results` action vs `equine-results` matcher Lambda was not substrate-verified before propagating to D4 dispatch text. CC verified independently and surfaced correction; refinement codified at § 4.29.

#### Cross-references

- **Phase A handoff substrate:** `docs/operations/PHASE_A_HANDOFF_2026-05-12.md` § 2.2 (5-case-study enumeration) + § 6.2 (refinement statement banking).
- **Case-study Lessons:** § 4.27 (A.6.d → A.6.f) + § 4.29 (D4 Source 2 conflation).
- **Dispatch reports:** A.6.c, A.6.d, A.6.f, A.5.2, A.5.3, D4 (all Phase A operational cycle).
- **OCRC D1 substrate classification convention:** `docs/operations/RESOURCE_INVENTORY_2026-05-09.md` § 2 legend (IAM-role attribution as classification basis).

#### Audit-CC prophylactic check template

For any operational-behavior claim in the audited document:

1. **Classify the claim** as substrate-direct-verified vs operational-signal-inference.
   - Substrate-direct: cron schedule citation, function-source-code citation, DB-direct query result, live-AWS API response output.
   - Operational-signal-inference: S3 write pattern, log-line timestamp, IAM-role attribution, code-symmetry between training and inference, throughput-volume log values.
2. **For inference-class claims**: verify the document flags the claim as inference (explicit inference-flagging language) OR cites explicit Tony confirmation. If neither, flag MATERIAL.
3. **IAM-role attribution check**: when the audited document attributes a producer to an IAM-role, verify the producer is independently identified (cron rule + Lambda + invocation payload), not solely by IAM-role. Multiple operational actors can consume a shared IAM role; IAM-role attribution alone is operational-signal-inference, not substrate-direct-verified.
4. **Throughput-volume check**: when the audited document cites a throughput volume from a log-line "inserted=N" or similar value, verify the N is net-new-DB-inserts (DB-direct query) rather than records-processed-from-payload (which may UPSERT-collapse). The two values can diverge by 5x or more per A.6.f investigation.

Flag MATERIAL for operational-signal-inference presented as fact without explicit inference-flagging or Tony-confirmation citation.

§ 4.32: one lesson banked at v3-patched-b (Phase A AUDIT_METHODOLOGY patch dispatch, 2026-05-12; substrate: 3 case studies surfaced across Phase A session arc).

### 4.32 Handoff-authoring-without-substrate-verification (deferred-classification-encoded-in-session-memory case-study expansion)

#### Abstract rule

Phase handoff documents classify resources as deletion candidates / orphan / deprecated / retirement-candidate only after independent substrate-grep verification across all inbound-reference classes (cross-Lambda invoke, API Gateway permissions, EventBridge rule targets, CDK declarations, IAM resource-based policies, CloudTrail invocation history, sibling-repo + script grep). Classification inherited from session memory or prior-cohort substrate WITHOUT grep verification at authoring time is **NOT substrate-grounded** and must be flagged as inference-not-substrate-verified until grep completes.

The rule applies symmetrically: (a) handoff documents authored from session memory; (b) QB dispatch text authored from prior-cohort substrate; (c) CC reports recommending classification. All three layers must perform substrate-grep at authoring time, not inherit framing from prior-layer reports.

This is a recursive application of § 4.31 (producer-attribution methodology refinement) to resource classification: just as operational behavior inference requires substrate verification, resource-class classification requires inbound-reference verification.

**Additional Abstract rule (v3-patched-d AMCS5 extension per Tony Decision 4 verbatim ratification):** Additionally, parallel-dispatch authorization under Directive 2 default cadence requires inter-dispatch source-state interaction analysis: dispatches operating on shared source files (CDK app, bible files, configuration files) may produce incompatible source-state combinations even when each dispatch is independently substrate-grounded. Authorization analysis must verify that the union of dispatch source modifications produces an executable state, not just that each dispatch is independently executable.

#### Worked example

Three case studies enumerated across Phase A session arc:

**Case Study 1 — D6 V1 dispatch catastrophic substrate divergence (2026-05-12).**

Substrate trace: handoff `PHASE_A_HANDOFF_2026-05-12.md` § 2 patch content + § 3.2 D6 dispatch scope authored against assumed bible state without verification of LOCKED 2026-05-11 re-lock-cycle structural state.

Actual state: 4 bibles + AUDIT_METHODOLOGY LOCKED at 2026-05-11 re-lock ceremony with cross-bible cross-reference freeze re-engaged; structural mismatches between handoff D6-{1,2,3,4,5,6} patch targets and current LOCKED bible structure surfaced as 6 divergence classes (D1-D6 enumerated at D6 V1 halt-and-surface report):
- D1: data_pipeline_bible § 4.2 per-source structure vs handoff "pattern entries" framing
- D2: data_pipeline_bible § 4.1 per-flow vs handoff "5-source extension"
- D3: architecture_overview § 3.10 ORPHAN-descriptor scattered vs handoff discrete subsection
- D4: handoff content overlap with already-incorporated bible substrate
- D5: § 4.2.4 NYRA deferred-disposition reservation explicit named but D6 patches did not address directly
- D6: UPSTREAM-CORRECTION § 7.2 step 4 ceremony scope conflict with Tier 2 single-CC dispatch

Mitigation: CC halted at Step 0/1 boundary per dispatch out-of-scope condition; QB re-authored D6 V2 with Decision Rule ("bible reflects reality + best practices") + Tony Q1-Q5 adjudications; V2 dispatch substrate-verification Step 0 + Decision Rule + adjudications produced 22-patch successful execution across 5 LOCKED bibles.

Classification: **handoff document substrate specifications not verified against current LOCKED bible state at handoff authoring time**.

**Case Study 2 — D6 patched Appendix A1 substrate-incorrect classification near-miss (2026-05-12 E3 prior dispatch).**

Substrate trace: handoff § 1.4 Appendix A1 classified `equine-inference` Lambda as "Deprecated; superseded by WR/PL/LS inference; retirement candidate"; classification propagated verbatim into D6 RC-3 `architecture_overview.md § 3.12.1` ORPHAN consolidated subsection at v3-patched-d.

Actual state: `equine-inference` Lambda is **production API handler** for 15+ API Gateway routes (`/health`, `/races/{date}`, `/races/today`, `/races/{raceId}/detail`, `/races/available-dates`, `/predictions/{date}`, `/predictions/today`, `/predictions/value`, `/predictions/run` GET+POST, `/predictions/{date}/{track_code}/{race_number}`, `/dashboard/metrics`, `/horses/{horse_id}/pps`, `/cards/{date}/{track_code}`) + cross-Lambda invoke at `backend/lambdas/ingestion/handler.py:843` (`lambda_client.invoke(FunctionName='equine-inference', InvocationType='Event', ...)` for batch-date dispatch). Only the `equine-inference-daily` cron rule is deprecated (DISABLED; superseded by per-model WR/PL/LS scheduled rules); the Lambda itself is load-bearing for the production EE API.

CC E3 Step 1 substrate-grep across 8 inbound-reference classes (cross-Lambda invoke / API Gateway resource-based policies / EventBridge targets / CDK declarations / IAM resource-based policies / CloudTrail / event-source-mappings / sibling-repo grep) surfaced the divergence within minutes of dispatch authorization.

Near-miss severity: if CC inbound-reference grep had not been performed before E3 deletion execution, entire EE production API would have gone offline at `cdk deploy EquineComputeStack` removing the `InferenceFunction` construct. Resource-based policies for API Gateway routes would have orphaned; subsequent API requests would have returned 502 errors across all 15+ routes.

Mitigation: E3 narrow-scope reframing (Tony Option 1 ratification) + bible reclassification patches (architecture_overview.md § 3.12.1 Appendix A1 corrected to production-class; § 3.10 alarm reclassification; deletion scope narrowed to `equine-feature-engineering` cohort only).

Classification: **handoff Appendix A1 classification inherited from session memory without substrate-grep verification of inbound references**. Recursive application of § 4.31 producer-attribution refinement: IAM-role inventory classification (the OCRC D1 substrate basis) does not establish operational-role classification.

**Case Study 3 — E1 Path 2 V1 dispatch CAPTCHA-solver scope propagation (2026-05-12 prior turn).**

Substrate trace: prior session directive established "no CAPTCHA solver service" stance per Tony's banked operational-cost-vs-benefit posture; E1 Step 1 CC diagnostic surfaced 4 Path candidates including Path 2 "probe-promotion-via-paid-solver" (referencing existing `equibase_probe/option_*_probe.py` exploratory cohort + Phase 5.3.18 backlog candidate disposition).

QB E1 Path 2 V1 dispatch authored vendor research scope (Capsolver / CapMonster / 2captcha / Anti-Captcha evaluation matrix across 8 dimensions × 4 vendors) without re-verifying against the prior directive substrate.

CC executed vendor research per dispatch authorization (Capsolver recommended; CapMonster ToS-blocked; 2captcha + Anti-Captcha don't support Imperva). Tony ratification at SP-E1P2-Step1 gate REJECTED procurement; cited prior directive ("no CAPTCHA solver service" banked decision); vendor research output discarded.

Path 2 RE-SCOPED to substrate investigation (discriminating-variable analysis of May 11 ~22:00 EDT successful manual run vs Apr 30 failed cron — investigation surfaced no manual-run substrate at that timestamp; .session_state.json mtime remains 2026-04-30 00:16:48 EDT; Branch B verdict per substrate-grounded headed-vs-headless fingerprint discrimination).

Classification: **QB dispatch authoring inherited CC diagnostic Path 2 framing without independent verification against prior session directive substrate**. The CC diagnostic correctly enumerated Path 2 as one of 4 candidates with "Tony decides" framing; QB dispatch authoring elevated it to actionable scope without re-checking the directive.

Mitigation: re-scoped Path 2 dispatch confines scope to substrate investigation + Branch A/B/C routing per substrate-determined discriminating variable; vendor research is discarded artifact; Tony directive substrate honored.

**Case Study 4 — QB-side framing-inheritance across multiple dispatch turns (2026-05-12 E1 Path 2 RE-SCOPED V2 + Xvfb investigation venue).**

Substrate trace: regression-frame framing propagated across **4 consecutive dispatch turns** before substrate investigation forced a design-state pivot.

- **Turn 1 — Phase A handoff § 5.1 authoring**: framed Equibase chart-failure as "FAILING DAILY exit=1 ... non-blocking for Source 4 workouts ... SNS alerts may be firing daily until disposition lands." Framing inherited regression-pattern session-memory inference (4-of-4-days continuous failure at handoff authoring time = "regression" assumption; no verification of pre-failure green-state evidence).
- **Turn 2 — E1 Step 1 diagnostic + Path enumeration**: CC inherited handoff regression-frame; classified failure mechanism as F-auth Imperva session expired (current-state finding); enumerated 4 Path candidates (Path 1 manual; Path 2 paid solver; Path 3 paid API; Path 4 drop). All 4 paths implicitly assumed regression-from-prior-green-state.
- **Turn 3 — E1 Path 1 bridge runbook authoring**: QB ratified bridge runbook scope; CC authored 22.5 KB runbook describing "session refresh + 13-day backfill" — the "bridge" framing implies resumption-from-green-state. No substrate verification of whether scraper was ever green in cron mode.
- **Turn 4 — E1 Path 2 V1 vendor research dispatch**: QB authored Capsolver / CapMonster / 2captcha / Anti-Captcha evaluation matrix; CC executed research; Tony directive substrate rejected procurement; vendor research discarded as artifact per Case Study 3 above.
- **Turn 5 — E1 Path 2 RE-SCOPED V1 dispatch**: QB authored discriminating-variable investigation (May 11 ~22:00 EDT successful manual run vs Apr 30 failed cron); CC investigated; surfaced headed-vs-headless Chromium fingerprint discriminator + reese84-vs-server-side-TTL mechanism. Branch B verdict (manual-touch requirement). **Still regression-frame implicit** — analysis assumed prior green-state existed.
- **Turn 6 — Tony surfaced methodology gap**: "discriminator-today finding is downstream of change-event finding; investigating downstream first risks misdiagnosis." Methodology refinement candidate banked: change-event-boundary-investigation must precede current-state discriminator analysis.
- **Turn 7 — E1 Path 2 RE-SCOPED V2 dispatch**: QB authored change-event substrate investigation per Tony's methodology gap surfacing. CC executed Classes 1-9 substrate investigation:
  - 15/15 captured cron runs failed since deployment 2026-04-27 evening
  - Zero cron-time-pattern S3 PDF uploads ever existed
  - README.md "Charts under cron — known limitation" section EXPLICITLY documents design-state at deployment time
  - Class 9 sub-question "Was scraper ever green in cron mode?" verdict: **NO** (substrate-definitive)
  - **No change-event boundary identifiable; scraper has been in design-state red since deployment.**
- **Turn 8 — QB ratified Branch R-irreversible (design-state qualifier)**: regression-frame retired; Xvfb investigation authorized per Directive 2 in-Phase-A scope.

Classification: **QB dispatch authoring inherits session-memory framing across multiple turns without periodic substrate-grounding verification**. The refinement applies RECURSIVELY to QB-side dispatch authoring discipline, not just at-handoff scope (Case Study 1) or at-CC-diagnostic scope (Case Studies 2-3). All three layers (handoff / QB / CC) must perform substrate-grounding verification at authoring time; framing inherited from prior-layer reports requires explicit substrate-verification step before propagation.

Mitigation pattern observed: Tony surfaced methodology gap (change-event-boundary-investigation refinement, banked as new queue entry per Phase A close-out cadence); CC executed substrate-grounded investigation; substrate-verified design-state verdict invalidated regression-frame assumption that had propagated for 4 consecutive dispatch turns.

Secondary lesson: Tony-side methodology-gap surfacing is the highest-leverage recursion gate. When neither handoff nor QB nor CC catches an inherited framing, Tony's outside-view perspective is the discriminator. The refinement may apply at Tony-ratification surfaces too (recursive); but Tony's outside-view is the canonical safety mechanism, not a layer requiring substrate-grep at authoring time.

**Case Study 5 — Parallel-dispatch source-state interaction analysis gap (2026-05-12 E3 Step 2 + E4 Step 2 cdk source conflict).**

Substrate trace:

- **Tony Directive 2 reinforcement**: "All operational work authorizes in parallel" — parallel-dispatch authorization becomes default cadence at Phase A entry directive.
- **QB authored 4 dispatches in single chat output** (E1 Path 2 RE-SCOPED + E2 + E3 + E4) per Directive 2 default cadence; CC executed all 4 SP-Step1 reports in parallel turn.
- **QB encoded E3 → E4 resource state sequencing** explicitly in E4 dispatch text ("E4 Step 3-4 executes AFTER E3 Step 2 deletion completes"). Resource-level dependency captured correctly.
- **QB did NOT analyze source-state interaction** between E3 Step 2 + E4 Step 2 dispatches; both modify `infrastructure/cdk/lib/compute-stack.ts`.
- **E4 Step 2 patches added ~556 LOC** to compute-stack.ts at lines 659-1207 (resource declarations for ~50 CLI-only resources via CDK constructs).
- **E3 Step 2 dispatched `cdk deploy`** from compute-stack.ts at the E4-Step-2-patched state; pre-execution analysis surfaced that `cdk deploy` would attempt to CREATE all ~50 new resource declarations (which already exist in AWS) producing "resource already exists" CloudFormation errors. Deployment would fail entirely; feature-engineering removal would not execute.
- **CC pre-execution substrate verification** caught the incompatibility before mid-execution failure (CC's defense-in-depth read at SP-E3NS-Step2 entry surfaced compute-stack.ts state post-E4-Step-2-patches; halt-and-surfaced sequencing conflict for Tony adjudication).
- **Resolution via Path 1 sequencing inversion** (resource-import-first → cdk diff verification → cdk deploy for feature-engineering removal only): execute E4 Step 3 Phase 1+2 (CloudFormation resource-import; brings ~50 resources under CFN management without creation) BEFORE E3 Step 2 cdk deploy (now only removes feature-engineering as net diff).

Classification: **parallel-dispatch authorization without inter-dispatch source-state interaction analysis**. Methodology gap distinct from substrate-grep-at-classification (Case Studies 1-4) but adjacent: at-authorization-time discipline applies to dispatch combinations, not just individual dispatches. The Directive 2 parallel-cadence default makes this gap class structurally probable; without inter-dispatch source-state union analysis, individually-substrate-grounded dispatches can produce structurally-incompatible execution states.

Mitigation pattern observed: CC pre-execution substrate verification caught the conflict (defense-in-depth at the CC pre-execution layer; not at QB authorization layer where the gap originated). QB-side mitigation (banked at this Case Study 5): at parallel-dispatch authorization time, analyze union of dispatch source modifications across shared source files (CDK app, bible files, configuration files) for executable-state compatibility before authorizing the parallel batch.

Cross-application across all 5 case studies: the refinement applies at multiple authoring scopes:
- **Case Studies 1-2**: handoff document authoring (at-handoff layer)
- **Case Studies 3-4**: QB single-dispatch authoring (at-QB-dispatch layer)
- **Case Study 5**: QB parallel-dispatch authorization (at-parallel-authorization layer; Directive 2 default cadence)

#### Case Study 6 — Stale-session-memory authoring discipline

**Abstract rule**: QB MUST verify bible state via CC substrate-discovery dispatch BEFORE authoring codification dispatch. Session-memory bible state references are substrate-untrustworthy — bible mutates across sessions; session memory decays; assumed bible state diverges from substrate-correct bible state. Authoring against session-memory bible state produces substrate-broken codification dispatches with version-state mismatch, slot collision, template violation, content fabrication risk, and substrate-source routing failure.

**Worked example**: SP-§4.32-CODIFICATION-12-CASE-STUDIES dispatch (2026-05-17) authored against assumed v2-patched bible state. CC halt surfaced 7 substrate-broken findings: actual bible at v3-patched-d (silent sed no-op risk); §§ 4.20-4.32 slots occupied (collision with proposed 4.20-4.34 assignments); 5-element template violation against actual 4-element convention; titles-only payload (verbatim banking text not in QB session memory; fabrication risk if proceeded); ceremony cap authorization missing; cross-reference targets misaligned. CC's substrate-discovery halt prevented bible substrate corruption. Recursive validation event same session — SP-§4.32-CODIFICATION-EXECUTION-AUTHORIZED dispatch (Phase 1 captured artifacts only, halted before Phase 2 mutations) referenced "per Tony adjudication turn output above" for verbatim content rather than embedding payload inline; CC halt caught reference-by-position substrate-broken pattern PLUS catastrophic uncommitted-substrate scope-inflation risk (v3-patched-a/b/c/d series uncommitted; commit would have bundled 428 prior insertions with v3-patched-e under unauthorized scope). Third recursive validation event same session — SP-§4.32-CODIFICATION-EXECUTION-RE-AUTHORED dispatch authored § 4.34 = alarms-encoding-design-state placeholder per QB session-memory bible-reservation assumption; CC Phase 1 substrate-discovery surfaced § 4.33 sibling-CC cross-references § 4.34 = forensic-gate activation discipline (lines 1586 + 1604); QB's planned § 4.34 placeholder would have created internal cross-reference inconsistency at mutation time. Sub-pattern A surfaced: QB routed Tony as substrate-source ("which Possibility I/II/III fired") instead of authoring CC read-only verification dispatch; Tony substrate-correct correction routed verification to CC inspection of substrate-authoritative bible file. Recursive validation event #4 same session — SP-§4.32-CODIFICATION-EXECUTION-RE-AUTHORED-v2 dispatch authored Option α adjudication assuming Possibility C confirmed (sibling-CC legitimately occupies §4.33; bible-reservation framing was QB misinterpretation); CC SP-§4.33-BIBLE-SUBSTRATE-VERIFICATION substrate-evidence verified Possibility I confirmed (sibling-CC §4.33 displaced bible-reserved change-event-boundary-investigation per line 17 v3-patched-c rev-history Tony-ratified banking-cadence reservation). Sub-pattern B surfaced: QB adjudications themselves require substrate-evidence basis; QB Option α adjudication based on partial substrate-evidence (Possibility C inferred from absent §4.34 + bible-reservation revision-history-mention) produced substrate-broken adjudication output. Recursive validation event #5 same session — SP-§4.32-CODIFICATION-EXECUTION-v3-PATCHED-e dispatch (Option Z) authored against substrate-state where v3-patched-e Option α had already committed in parallel CC terminal (commits a62f96d + 44088c7). QB lost track of substrate-state across parallel CC terminals; authored dispatch payload assuming Option Z disposition while substrate-actual reflected Option α codification. CC Phase 1 substrate-discovery halt #5 caught all 8 substrate divergences (header status / §4.34 occupancy / §4.35 occupancy / §4.36 occupancy / §4.32 CS6 occupancy / §4.33 cross-reference validity / git commit state / Tony adjudication branch). Sub-pattern C surfaced: QB substrate-state tracking across parallel CC terminals is substrate-untrustworthy without explicit substrate-discovery between adjacent dispatch authorings; when multiple CC terminals execute substrate-mutating work in parallel, QB MUST re-verify substrate-state via CC substrate-discovery dispatch BEFORE authoring next dispatch. The recursive validation observations — five independent substrate-broken dispatch authoring + adjudication patterns in same session, each caught by CC prophylactic substrate-discovery — is substrate-grounded evidence that methodology infrastructure is working as designed at scale. Five-event recursive validation cohort substrate-permanent demonstrates: CC halt-and-surface discipline scales with QB authoring frequency; prophylactic substrate-verification is non-optional; substrate-evidence basis is required for ALL QB outputs (dispatches AND adjudications).

**Cross-references**: § 4.24 (substrate-permanent claim verification protocol — applied to bible state itself); § 4.32 Case Studies 1-5 (handoff-authoring-without-substrate-verification — pattern-coherent extension to QB's own codification authoring); § 4.21 (Q5 worked example ceremony cap pattern); § 4.33 (per-layer training script registration discipline — adjacent: substrate-permanent fix executing in same session triggered Case Study 6 sub-pattern when QB acknowledged sibling-CC completion in some prose but retained pre-sibling-CC language elsewhere).

**Audit-CC prophylactic check template**: Before executing codification dispatch, CC verifies dispatch payload against actual bible substrate via Phase 1 substrate-discovery: (1) version header in dispatch matches actual bible version verbatim; (2) proposed § slots are actually open per current bible substrate; (3) entry convention element-count matches actual bible convention; (4) verbatim case study content embedded INLINE in dispatch payload (NOT referenced via "per prior turn" or "per surface document"); (5) ceremony cap override disclosure present for bulk-mutation scope; (6) git commit state inspection verifies no unauthorized scope inflation from prior uncommitted substrate; (7) cross-reference targets in proposed content match actual bible substrate (no semantic collision with sibling-CC content); (8) dispatch language coherent across all sections (revision history + commit message + insertion content all reflect same substrate-state assumption). If ANY check fails, CC halts dispatch with substrate-broken findings enumeration; QB re-authors against actual bible substrate.

**Case Study 6 sub-pattern A — QB substrate-source routing failure**: substrate-authoritative source is on-disk substrate (bible file / database schema / S3 substrate / etc.); CC read-only substrate-discovery dispatch is the substrate-grounded routing; QB asking Tony to identify substrate state is substrate-incorrect routing pattern (Tony memory/inference is substrate-untrustworthy for state Tony hasn't directly inspected). Prophylactic check: when QB encounters substrate-state-unknown, author CC read-only verification dispatch FIRST; route adjudication to Tony AFTER verbatim substrate evidence captured.

**Sub-pattern B — QB substrate-adjudication substrate-untrustworthy without substrate-evidence basis**: Adjudications based on partial substrate-evidence produce substrate-broken adjudication outputs. Substrate-grounded discipline: QB adjudication MUST surface substrate-evidence basis verbatim alongside adjudication; absence of verbatim substrate-evidence basis is signal that adjudication is substrate-untrustworthy. Prophylactic check: QB adjudication output template requires explicit "Substrate-evidence basis:" section with verbatim CC substrate-discovery quotation; adjudications without substrate-evidence basis are substrate-incomplete pending substrate-verification dispatch.

**Sub-pattern C — QB substrate-state tracking across parallel CC terminals**: When multiple CC terminals execute substrate-mutating work in parallel, QB substrate-state inference across terminals is substrate-untrustworthy. QB must NOT assume which terminal committed which substrate based on session-memory; substrate-state evidence requires CC substrate-discovery dispatch between adjacent dispatch authorings when parallel CC mutation in flight. Prophylactic check: QB tracks per-CC-terminal mutation scope verbatim; when authoring next dispatch downstream of parallel CC work, FIRST issue CC substrate-discovery to verify which mutations landed; only then author next dispatch payload against substrate-verified state.

**Recursive validation event #6 — BEL H3 Step 2 dispatch (2026-05-18)**: dispatch authoring inherited Path A (git apply patch) + Path B (env-var override) from handoff substrate as substrate-alternatives without verifying Path B substrate-coherence absent Path A. CC Phase 1 substrate-discovery surfaced Path A patch substrate-broken (off-by-one hunk header counts) AND Path B env-var-reading logic ABSENT from download_charts.py — neither path substrate-viable as authored. Methodology catch: Phase 1 substrate-discovery surfaced dual-path-substrate-incoherence pre-Phase-2 mutation; halt-and-surface led to Option α manual Edit application.

**Recursive validation event #7 — BEL H3 Phase 3 dispatch (2026-05-18)**: dispatch assumed `--days-back N` substrate-equivalent to "historical window backfill" without verifying cache mechanics. Substrate-actual: `download_log.txt` line-based cache; `is_done()` substrate-blocks re-download when `NR_TID_YYYYMMDD` entries pre-exist from prior runs. Stale NR_BEL entries from pre-BAQ-remap era substrate-blocked historical re-download under --days-back 18. Methodology catch: Phase 5 verification gate failed on substrate-incomplete cohort population (16 stale NR_BEL entries cached blocking 11 BEL historical dates); halt-and-surface led to Phase 2 cache-invalidation surgical patch.

**Recursive validation event #8 — BEL H3 Phase 1 dispatch scaffolding (2026-05-18)**: dispatch contaminated with QB-speculated cache substrate (.session_state.json) + speculated key schema (BEL date keys). Substrate-actual: `.session_state.json` is Playwright browser session substrate (`cookies` + `origins` keys only); cache substrate-actual at `download_log.txt`. CC Phase 1 substrate-discovery surfaced divergence pre-Phase-2 mutation; halt-and-surface led to dispatch re-issue with substrate-correct cache target.

**Recursive validation event #9 — BEL H3 Phase 4 dispatch (2026-05-18)**: dispatch included substrate-discovery sub-phase (Phase 4.1.1) asking CC to "report verbatim sync invocation pattern from run_daily_refresh.sh". Substrate-actual: pattern already verbatim in Phase 1.4 prior-turn report (single-action `aws s3 sync charts/ s3://equine-raw-data/charts/` + Lambda window-payload schema). CC re-issue substrate-state report detected duplicate substrate-discovery dispatch; substrate-pragmatic executed-anyway (substrate-coherence double-check, low-cost) but surfaced QB substrate-state-tracking failure mode where dispatch asks for substrate already in conversation.

**Sub-pattern B refinement (v3-patched-g; multi-instance accrual substrate-emphatic per Events #6-#9)**: QB dispatch authoring decoupled from CC verbatim substrate-evidence at authoring time. Failure modes:
  - Path-substrate-incoherence: alternatives presented in dispatch without verifying each path's substrate-coherence (Event #6).
  - Mechanic-assumption: dispatch assumes substrate-mechanic behavior (cache, scraper, idempotency) without substrate-evidence (Event #7).
  - Speculated-scaffolding: dispatch payload references substrate names/schemas that don't exist substrate-actually (Event #8).
  - Ceremony-laden re-discovery: dispatch asks CC to re-surface substrate already verbatim in prior turn (Event #9).

Pre-authoring prophylactic check (Audit-CC template extension): at dispatch authoring time, QB MUST cite verbatim CC substrate-evidence basis from prior turn(s) — OR explicitly authorize substrate-discovery sub-phase when substrate-evidence absent. Substrate-discovery sub-phase substrate-grounded when no prior CC report covers the substrate; substrate-redundant when verbatim already in conversation. CC enforcement: at Phase 1 of any multi-phase dispatch, CC verifies dispatch's substrate-assumptions against current substrate-actual; HALT on divergence. § 4.32 sub-pattern B Events #6-#9 substrate-precedent.

#### Cross-references

- **Phase A handoff substrate:** `docs/operations/PHASE_A_HANDOFF_2026-05-12.md` § 1.4 (Appendix A1 source of substrate-incorrect classification per Case Study 2); § 3.2 (D6 dispatch scope source per Case Study 1).
- **Related lessons:** § 4.27 (Inference-promoted-to-substrate-fact-without-Tony-confirmation — A.6.d case study; producer-attribution refinement applies to Case Study 2 recursively); § 4.29 (QB-framing-not-substrate-verified-before-propagation — D4 Source 2 case study; applies to Case Study 3 directly); § 4.31 (Producer-attribution methodology refinement — 5-case-study banking; recursive application to resource classification per this lesson).
- **Dispatch reports:** D6 V1 halt-and-surface report (Case Study 1 origin); E3 Step 1 prior dispatch (Case Study 2 substrate-grep methodology demonstration); E1 Path 2 V1 vendor research report (Case Study 3 artifact discarded per Tony directive substrate).
- **Substrate citation for substrate-grep methodology:** E3 Step 1 prior dispatch executed 8-class inbound-reference grep producing zero-false-positive substrate verification — methodology codified in Audit-CC prophylactic check template below.

#### Audit-CC prophylactic check template

When the audited document classifies a resource (Lambda / IAM role / EventBridge rule / SQS queue / CloudWatch alarm / S3 bucket / ECR repo / Secrets Manager entry) as orphan / deprecated / deletion-candidate / unused / retirement-candidate:

1. **Verify the audited document cites substrate-grep verification for ALL inbound-reference classes**, OR cites prior dispatch report performing the grep. The 8-class substrate-grep methodology (E3 Step 1 demonstration):
   - **Cross-Lambda invoke**: `grep -rn "FunctionName='<resource>'" backend/lambdas/ --include="*.py"` for `lambda_client.invoke(...)` patterns
   - **API Gateway resource-based policies**: `aws lambda get-policy --function-name <resource>` for Statement.Principal.Service "apigateway.amazonaws.com" entries
   - **EventBridge rule targets**: `aws events list-rules` + per-rule `aws events list-targets-by-rule --rule <rule>` for resource-as-target presence
   - **CDK declarations**: `grep -rn "<resource>" infrastructure/cdk/ --include="*.ts"` for CDK construct references
   - **IAM resource-based policies**: enumerate consuming services via resource ARN cross-reference
   - **CloudTrail invocation history**: `aws cloudtrail lookup-events --lookup-attributes AttributeKey=ResourceName,AttributeValue=<resource>` last 14d
   - **Event source mappings**: `aws lambda list-event-source-mappings --function-name <resource>` (Lambda-specific)
   - **Sibling-repo + script grep**: `grep -rn "<resource>" <sibling-repos> scripts/` for cron / scheduled / manual invocation patterns

2. **For each inbound-reference class returning non-zero hits**, document the consumer + dependency type. Any non-zero inbound reference invalidates orphan / deprecated / retirement-candidate classification; resource is substrate-grounded as production-class (or other load-bearing class).

3. **Verify the audited document distinguishes resource-LEVEL classification vs adjacent-rule classification.** Case Study 2 pattern: the Lambda itself is production-class but the associated EventBridge cron rule may be DISABLED/deprecated. These are SEPARATE resources; classifying the Lambda as deprecated because the rule is deprecated is a category error.

4. **Verify the audited document cites prior-cycle DIRECTIVE substrate** (if applicable): when the document propagates a recommendation that intersects with Tony's banked operational-cost-vs-benefit decisions, cross-reference the directive at authoring time. Case Study 3 pattern: vendor research scope should have re-checked "no CAPTCHA solver service" directive before authoring.

Flag MATERIAL for classification-inherited-from-session-memory-without-grep:
- Resource classified as orphan/deprecated/deletion-candidate without ≥ 3 of 8 inbound-reference classes substrate-verified
- Resource-level classification not distinguished from adjacent-rule classification (Case Study 2 pattern)
- Recommendation propagated past prior-cycle directive without cross-reference verification (Case Study 3 pattern)

Flag as **fabricated content (lock-blocker)** if classification contradicts substrate-grep results that ARE cited in the same document (internal-inconsistency).

**Additional check (QB-side dispatch authoring discipline; added at v3-patched-c per Case Study 4 banking):**

Before authoring any dispatch that classifies a resource state (orphan / deprecated / failure-mode / regression / design-state), QB executes ONE of the following substrate-grounding paths at dispatch-authoring time:

1. **Substrate-grep verification path** (canonical): execute the 8-class methodology directly at dispatch authoring (or cite prior-cycle CC report that performed the grep within the current substrate window).
2. **Design-state verification path**: read README + code comments + deployment-time hypotheses + deployment notes for the affected resource; verify whether failure mode is design-state-since-deployment (no regression to investigate) vs regression-from-prior-green-state. If design-state evidence is unambiguous (e.g. README "known limitation" section), no substrate-grep needed; failure-mode classification follows design-state framing.
3. **Change-event boundary verification path** (per AUDIT_METHODOLOGY § 4.33 candidate refinement; codification deferred to Phase A close-out): identify last-green vs first-red substrate boundary; if no green-state evidence exists in available substrate window, design-state diagnosis applies (Case Study 4 pattern).
4. **CC pre-investigation path**: CC executes a Tier-3 read-only substrate investigation BEFORE QB dispatch authors recommendations on the affected resource. Tier-3 investigation output substitutes for substrate-grep at QB dispatch authoring (banked at this dispatch as the operational pattern: Tony surfaces methodology gap → CC investigates → QB ratifies post-investigation).

Flag MATERIAL if QB dispatch authoring classifies a resource without one of these 4 substrate-grounding paths AND the classification propagates from session-memory framing inherited from prior dispatches (Case Study 4 pattern).

**Recursive application notice**: this prophylactic check operates at THREE layers:
- **At-handoff layer**: handoff document authoring (Case Study 1 + Case Study 2 patterns)
- **At-QB-dispatch layer**: QB dispatch authoring (Case Study 3 + Case Study 4 patterns)
- **At-CC-diagnostic layer**: CC report authoring (recursive via § 4.27 / § 4.31 + Case Study 2 producer-attribution refinement)

Tony-ratification layer operates as outside-view safety mechanism per Case Study 4 secondary lesson; not a layer requiring substrate-grep at authoring time (Tony's outside-view discriminator function is the recursion-base-case).

**Additional check (parallel-dispatch source-state interaction analysis; added at v3-patched-d per Case Study 5 banking):**

**Check name**: Inter-dispatch source-state interaction verification at parallel-dispatch authorization

**Trigger condition**: QB authorizes parallel dispatches under Directive 2 default cadence where two or more dispatches in the parallel-authorization batch modify shared source files (CDK app, bible files, configuration files).

**Mandatory verifications before parallel authorization is substrate-grounded**:

1. **Enumerate shared source files** across all dispatches in the parallel-authorization batch. Example: E3 Step 2 + E4 Step 2 both modify `infrastructure/cdk/lib/compute-stack.ts`.
2. **Per-shared-file: identify each dispatch's source modifications** (additions, deletions, modifications). Example: E3 Step 2 removes FeatureEngineeringFunction construct + IAM grants + rule; E4 Step 2 adds ~50 resource declarations.
3. **Per-shared-file: analyze union of modifications for compatibility**. The union must produce a valid executable state, not just each dispatch's modifications individually. Example: union of E3 Step 2 (FE removal) + E4 Step 2 (50 additions) produces compute-stack.ts with both feature-engineering-removed AND 50-new-declarations; `cdk deploy` on this union state would attempt to create the 50 new resources (fail: already exist) AND delete FE (intended).
4. **Identify sequencing constraints implicit in source-state combinations**. Example: E4 Step 2 source modifications require resource-import workflow before any `cdk deploy`; E3 Step 2 cdk deploy must execute after resource-import to avoid the create-already-exists failure mode.
5. **Encode discovered sequencing constraints explicitly in dispatch text**. Example: E4 Step 3 Phase 1+2 (resource-import) must execute before E3 Step 2 Phase 2 (cdk deploy) under shared compute-stack.ts source state.
6. **If source-state combinations are structurally incompatible without sequencing**: halt parallel authorization; require Tony adjudication of execution order before issuing dispatches.

**Failure mode**: parallel-dispatch execution fails mid-deploy with structural error (resource-already-exists, schema-conflict, similar) when union of source modifications is incompatible; CC pre-execution verification catches structural-incompatibility as defense-in-depth (Case Study 5 mitigation pattern), but root-cause is at QB parallel-authorization layer.

**Flag MATERIAL** if parallel-dispatch batch authorizes without Step 1-5 verifications, AND dispatches in the batch modify shared source files.

**Banking instance**: Case Study 5 enumerates Phase A E3 Step 2 + E4 Step 2 parallel-authorization without source-state union analysis; CC defense-in-depth caught the conflict before mid-execution failure; resolution via Path 1 sequencing inversion (resource-import-first).

**Recursive application notice (extended at v3-patched-d)**: this prophylactic check operates at FOUR layers:
- **At-handoff layer**: handoff document authoring (Case Study 1 + Case Study 2 patterns)
- **At-QB-single-dispatch layer**: QB single-dispatch authoring (Case Study 3 + Case Study 4 patterns)
- **At-QB-parallel-authorization layer** (NEW): QB parallel-dispatch authorization under Directive 2 default cadence (Case Study 5 pattern)
- **At-CC-diagnostic layer**: CC report authoring (recursive via § 4.27 / § 4.31 + Case Study 2 producer-attribution refinement; CC pre-execution verification serves as defense-in-depth for Case Study 5 gap class)

Tony-ratification layer operates as outside-view safety mechanism per Case Study 4 secondary lesson; recursion-base-case.

### 4.33 Per-layer training script registration discipline (substrate-permanent shared registration module)

#### Abstract rule

Per-layer ML training scripts (those that produce S3-uploaded artifact files outside of the canonical `model/training/train.py` entry point) MUST invoke `model.training.registration.register_trained_artifact()` immediately post-S3-upload, within the same Fargate training cycle that produced the artifact. The shared registration module is the substrate-permanent locus for `model_versions` INSERTs; no per-layer script may construct its own INSERT against `model_versions`, and no per-layer script may delegate registration to a post-cycle helper script.

Defaults `is_active=FALSE` per § 4.34 forensic-gate discipline (activation requires forensic substrate validation, not training-time eval). The shared module is responsible for `model_type` derivation (from `version_name` prefix-map when not explicitly passed), `feature_list` and `hyperparameters` JSONB serialization, unrecognized-extras folding into `hyperparameters._training_extras`, and rollback-on-failure semantics.

Substrate-prophylactic check: any new per-layer training script added under `model/<layer>/train.py` (or equivalent path) is reviewed at PR-time for a `register_trained_artifact` invocation guarded by try/except (registration failure must log-and-continue, never crash training — the S3 artifact is the primary substrate; registration is secondary durability).

#### Worked example

**Banking substrate (Tier 1 Phase 3.5, 2026-05-12 → SP-§4.33 bake-in 2026-05-17).**

Substrate trace: per-layer training scripts `model/wr/train.py`, `model/pl/train.py`, `model/longshot/train.py`, `model/ranker/train.py`, `model/ensemble/train.py`, `model/trajectory/train.py`, `model/win_prob/train.py` each implemented their own `save_artifacts()` (or inline equivalent) that wrote model + metadata + eval JSONs locally, then uploaded to `s3://equine-model-artifacts/<layer>/`. None of the seven invoked `register_model()` or `insert_model_version()` post-upload. Only canonical `model/training/train.py` registered.

Actual state (Tier 1 Phase 3.5 inventory): 37 lean58 artifacts present in S3 across `pl/`, `win_prob/`, `ranker/` prefixes; zero corresponding rows in `model_versions`. Forensic adjudication cycles requiring `model_version_id` foreign keys (predictions FK constraint per `schema.sql` line 386) could not proceed against unregistered artifacts.

Mitigation (Phase 3.5): `/tmp/phase3_register_artifacts.py` helper scanned S3 for unmatched lean58 base artifacts, read paired `_meta.json` + `_eval.json` sidecars, derived `model_type` from `version_name` prefix pattern, and inserted the missing rows with `is_active=FALSE`. Helper was substrate-pragmatic but session-ephemeral.

Bake-in fix (SP-§4.33, 2026-05-17): `model/training/registration.py` extracts the substrate-correct INSERT shape into a shared module; the seven per-layer scripts each gained a registration call following the S3 upload loop. Synthetic validation (`/tmp/sp_4_33_synthetic_validation.py`) verified: (a) `derive_model_type` maps the eight prefix-map cases substrate-correctly; (b) `register_trained_artifact` constructs a 19-column INSERT with positional params in canonical order, unrecognized metadata extras folded into `hyperparameters._training_extras` JSONB, `is_active=FALSE` default; (c) rollback-on-failure path engages cleanly without leaving partial state.

Classification: **per-layer training scripts inherited substrate-bug of skipping registration; bake-in fix prevents future Fargate training cycles from producing unregistered S3 artifacts**. Recursive application of § 4.31 producer-attribution methodology refinement: the producer of an S3 artifact bears registration responsibility within the same cycle, not a downstream helper.

**Related lesson**: § 4.34 (forensic-gate activation discipline — `is_active=FALSE` default is the substrate-pragmatic complement of this lesson; activation is a separate, forensic-substrate-gated step).

**Related lesson**: § 4.31 (producer-attribution methodology refinement — producer-bears-registration is a recursive application of producer-bears-attribution).

Substrate-permanent: all future Fargate training cycles produce registered artifacts automatically; Tier 2 retrain candidates (per alternate methodology 4A-4I) register cleanly without post-cycle backfill.

### 4.34 — Forensic-gate activation discipline (training-time eval vs forensic substrate divergence)

**Abstract rule**: Activation decisions on retrained ML artifacts MUST gate on forensic-window OOS substrate measurement, NOT on training-time eval substrate alone. Training-time eval is sample-internal; forensic-window substrate-clean OOS measurement is methodology-honest. New artifact registration produces is_active=FALSE by default per § 4.33; activation requires substrate-evidence from forensic-window re-measurement against substrate-clean cohort. Substrate-pragmatic complement to § 4.33: registration is automatic substrate-clean; activation is forensic-substrate-gated separate step. Empirically validated: training-time eval AUC over baseline confirms in OOS forensic at approximately 12% rate; majority of training-time-eval-predicted activations fail forensic substrate gate.

**Worked example**: Tier 1 Phase 3.5 forensic re-measurement (2026-05-17). Training-time eval substrate predicted 33 of 37 lean58 candidates would activate per Δ AUC threshold; substrate-pragmatic trust of training-time eval would have activated 33 layers. Forensic-window OOS re-measurement against substrate-clean cohort (2026-05-02..2026-05-10, 233 races, post-BEL-field_size-backfill + post-Top-5-feature substrate) validated only 4 of 37 candidates. Confirmation rate: approximately 12%. Without forensic gate, 29 layers would have activated with ROI hits ranging -15pp to -121pp vs current production substrate. Forensic-gate discipline prevented substrate-degrading activations on 29 layers. § 4.36 surfaced complementary pattern (AUC↑ + ROI↓ calibration degradation) explaining substrate-mechanical why forensic ≠ training-time eval: feature substrate over-fits training-distribution-pick-pattern that does not replicate forensic OOS.

**Cross-references**: § 4.33 (per-layer training script registration discipline — is_active=FALSE default is the substrate-pragmatic complement; registration automatic, activation forensic-gated); § 4.36 (AUC↑ + ROI↓ calibration degradation — substrate-mechanical explanation for forensic vs training-time eval divergence); § 4.26 (pre-committed activation threshold discipline — threshold applied AT forensic-substrate measurement, not training-time eval); § 4.29 (counterintuitive null result methodology verification — adjacent pattern: substrate-correct measurement methodology required before classifying null result as substrate-permanent).

**Audit-CC prophylactic check template**: At per-layer activation adjudication surface post-retraining, CC verifies: (1) Training-time eval metrics surfaced alongside forensic-window OOS metrics, not in place of; (2) Activation decision driven by forensic-window substrate, not training-time eval; (3) Δ AUC AND Δ ROI both measured against forensic-window substrate-clean cohort (per § 4.36 dual-criterion gate); (4) Per-track stratification applied where substrate coverage variance exists (per § 4.23); (5) BEL stratification explicit where BEL anomaly persists per cross-layer pattern (per § 4.28); (6) Substrate-evidence-grounded confirmation rate tracked for future calibration of training-time-eval substrate-trustworthiness. If training-time eval surfaces activation candidate but forensic-window substrate fails dual-criterion gate, KEEP CURRENT is substrate-honest answer; training-time eval substrate-trustworthiness is approximately 12% confirmation rate per validated banking.

### 4.35 — CC wall-clock and cost estimate substrate-untrustworthiness

**Abstract rule**: CC pre-execution estimates for wall-clock and infrastructure cost (Fargate, compute, token consumption) are substrate-untrustworthy without historical-actuals anchoring. CC pads worst-case bounds from first-principles arithmetic without verifying against substrate-actual prior training runs, inference invocations, or Fargate task executions in same codebase. Substrate-grounded reference is Tony historical actuals where present in substrate, not CC first-principles padding. Empirically validated: CC estimates substrate-inflate by approximately 10x on both wall-clock and cost axes.

**Worked example**: Tier 1 Phase 3 execution (2026-05-17). Scope: 53 Fargate training runs across pl_core / win_prob_core / wp_full / rk_full layer families. CC pre-estimate: 6-12 hours parallel wall-clock + $250-500 Fargate cost. Substrate-actual execution: approximately 50 minutes wall-clock + approximately $15-30 cost. Ratio: approximately 10x over-estimate on both axes. Pattern validated twice this session (Phase 3 retraining + earlier Phase 4 deploy estimates). § 4.31 prior banking on producer-attribution surfaces adjacent pattern; § 4.35 codifies CC estimate substrate-untrustworthiness specifically as distinct from producer-attribution.

**Cross-references**: § 4.31 (producer-attribution methodology refinement — adjacent pattern; CC estimate substrate-untrustworthiness extends producer-attribution discipline to CC's own predictions of substrate); § 4.32 Case Study 1 (handoff-authoring-without-substrate-verification — same substrate-untrustworthiness pattern applied to CC estimates vs Tony historical actuals).

**Audit-CC prophylactic check template**: Before accepting CC estimate for wall-clock OR infrastructure cost in execution dispatch authorization, QB verifies: (1) Has CC measured substrate-actuals from prior comparable execution in this codebase? (2) If yes, is estimate within 2x of measured actuals? (3) If no measured actuals, discount CC estimate by approximately 10x as substrate-pragmatic prior. (4) Surface CC estimate alongside substrate-actuals (if any) for Tony adjudication. (5) Post-execution: bank actual:estimate ratio for future calibration. Substrate-grounded: dispatch estimates carry "CC pre-estimate vs substrate-actuals will be re-measured" caveat language.

### 4.36 — AUC↑ + ROI↓ divergence equals calibration degradation

**Abstract rule**: When new ML artifact substrate-measurement surfaces AUC improvement vs current-active artifact AND ROI regression vs current-active artifact, the new artifact has produced higher race-level discrimination at the cost of degraded picking-level calibration. AUC measures rank-order signal; ROI measures pick-quality at top-1 selection. Substrate-pragmatic interpretation: new artifact picks "different but worse" — substrate-true discrimination at race-level does not translate to substrate-true picking at top-1 because feature substrate over-fits training-distribution-pick-pattern that does not replicate forensic OOS. Single-criterion activation gates (AUC-only) activate calibration-degraded layers; substrate-grounded discipline requires dual-criterion (AUC threshold AND ROI threshold) for activation.

**Worked example**: Tier 1 Phase 3.5 forensic re-measurement (2026-05-17) surfaced 23 of 33 lean58 candidates with AUC↑ + ROI↓ pattern across wp_full / rk_full / pl_core layer families. Specific example: rk_full_speed lean58 candidate AUC tied with current Phase B.x baseline; ROI -121.2pp vs current Phase B.x. Substrate-pragmatic activation gate per § 4.26 (pre-committed threshold discipline) extended to dual-criterion: activate iff Δ AUC ≥ +0.017 AND Δ ROI ≥ 0pp (no regression). Without dual-criterion gate, training-time-eval-only activation would have activated 33 layers; substrate-validated forensic + dual-criterion gate produced 4 activations (12% confirmation rate per § 4.34 banking candidate).

**Cross-references**: § 4.26 (pre-committed activation threshold discipline — dual-criterion extension); § 4.34 banking candidate (training-time eval vs forensic substrate divergence — adjacent pattern surfacing 12% confirmation rate from same Tier 1 substrate); § 4.23 (coverage-stratified forensic — per-tier metrics for both AUC AND ROI required).

**Audit-CC prophylactic check template**: At per-layer activation adjudication surface, CC produces dual-criterion table per candidate: Δ AUC (forensic) AND Δ ROI (forensic). Activation recommendation: ACTIVATE iff Δ AUC ≥ pre-committed threshold AND Δ ROI ≥ 0pp (substrate-pragmatic baseline: no regression). KEEP CURRENT iff dual-criterion fails on either axis. SUBSTRATE-AMBIGUOUS iff one axis improves materially while other regresses materially (Tony adjudication required; calibration-degradation hypothesis explicitly tested).

### 4.37 — Alarm authoring publisher-cadence × evaluation-period × TreatMissingData coherence

**Abstract rule**: CloudWatch metric alarms authored without explicit substrate-coherence between publisher cron schedule, alarm Period, and TreatMissingData semantic produce chronic false-positives or false-negatives. Three-axis coherence check required at alarm authoring time: (1) publisher cron cadence (how often metric data publishes), (2) alarm Period (evaluation window length), (3) TreatMissingData (notBreaching / breaching / missing / ignore semantic). Mismatch surface: daily-publishing metric + 5-minute evaluation period + breaching treatment fires ~287 false-positive alarms per day between publisher firings. Substrate-pragmatic alarm Period MUST be ≥ publisher cadence; TreatMissingData semantic MUST match operational expectation during between-publish windows.

**Worked example**: Equine Equalizer entries-deficit alarm authored with 5-minute Period and breaching TreatMissingData for entries-publisher metric publishing once daily at 11:15 UTC. Alarm chronically fired ALARM state continuously between 11:20 UTC and 11:15 UTC next day; 23 hours 55 minutes false-positive ALARM state per cron cycle. Substrate-grounded fix: Period adjusted to 1-day (matches publisher cadence); TreatMissingData adjusted to notBreaching (substrate-honest semantic for between-publisher windows). Alarm fix landed 2026-05-17 SP-ENTRIES-ALARM-CONFIG-FIX dispatch; CDK-deployed in 46.1s; substrate-grounded clean operation.

**Cross-references**: § 4.21 (Q5 worked example ceremony cap pattern — alarm authoring is substrate-prerequisite infrastructure; ceremony cap applies); § 4.16 (lock-CC metadata bundle discipline — same coherence-check pattern for bible authoring metadata as for alarm authoring substrate); § 4.32 Case Study 1 (handoff-authoring-without-substrate-verification — alarm Period default values inherited from CDK constructs without publisher-cadence verification is same anti-pattern).

**Audit-CC prophylactic check template**: At alarm authoring time, CC verifies trio coherence: (1) substrate-grep publisher cron schedule from CDK / scheduler substrate; surface cadence verbatim; (2) verify alarm Period ≥ publisher cadence (alarm Period < publisher cadence → false-positive guaranteed); (3) verify TreatMissingData semantic matches operational expectation during between-publisher windows (daily-publisher + breaching = false-positive; daily-publisher + notBreaching = substrate-correct); (4) at alarm-authoring-time, output verbatim trio coherence assertion in CC SP report (e.g., "publisher cadence: daily 11:15 UTC; alarm Period: 1-day; TreatMissingData: notBreaching; trio-coherent: YES"); (5) if any axis fails coherence: halt alarm authoring; surface substrate-broken finding to QB for re-adjudication.

---

### 4.38 — AS-OF discipline on per-row historical aggregates at race-fire-time inference (REPAIR-4 D4 case study)

**Abstract rule**: Any service that queries a historical-record table (past_performances, race history, sequence-feature table) at race-fire-time inference time MUST filter by `record_date < target_race.race_date`. Without this AS-OF predicate, the query returns the target race itself + any newer records as if they were "past" performances, leaking ground truth (finish_position, payouts, results) into feature_engineering. The substrate-honest test: at the precise moment a prediction is computed, the feature corpus must contain ONLY data that would have been visible BEFORE the target race ran. If race-being-predicted's outcome is in the corpus, the model is trained-and-evaluated on its own answer.

**Worked example**: Equine Equalizer `entry_repository.get_entries_by_race(race_id)` (substrate-state pre-REPAIR-4 Step B) queried past_performances by `horse_id` only with no `race_date` filter. At inference for race d50e069c (race_date 2026-05-13), 9 of 12 horses had their own race d50e069c row in returned pps. Feature_engineering ingested those rows with `finish_position` populated. Substrate-actual: a horse's "past performance" included its own future ground truth. Fix: `get_entries_by_race(race_id, as_of_date=None)` with `as_of_date` REQUIRED parameter (raises ValueError if missing per § 4.32 #18 prophylactic discipline) + SQL predicate `AND race_date < %s`. Substrate-applied at all 7 callsites + parallel pp_count subqueries.

**Cross-references**: § 4.32 sub-pattern B firing #18 (substrate-prophylactic mandatory-parameter pattern); § 4.27 (inference-promoted-to-substrate-fact — D4 surfaced through supp-2 audit, not through external bug report); § 4.26 (documentation-not-substrate-grounded — entry_repository's pre-fix docstring said "Last PP_LOOKBACK_STARTS past performances" with no AS-OF discipline mentioned).

**Audit-CC prophylactic check template**: At inference-service code review time, for every database query that loads historical records (pps, results, race history, sequence data) for use as model features: (1) substrate-grep the SQL string; (2) verify a date-filter predicate exists with the target race's race_date as the upper bound (exclusive); (3) if no predicate present, halt code review and surface as AS-OF discipline violation; (4) the predicate must be `<` (strict), not `<=` (same-day races may have outcomes by inference time); (5) at the callsite, verify the AS-OF anchor parameter is plumbed through from the race object (race.race_date), not from a fixed string or a default value; (6) flag as substrate-leakage class (lock-blocker for inference deployments).

---

### 4.39 — Aggregate-without-timestamp tables substrate-leak at backtest/training replay (REPAIR-4 C.5 case study)

**Abstract rule**: Any aggregate statistics table refreshed in-place (DELETE + re-INSERT) without snapshot-date column is substrate-leaky for backtest / training replay against historical races. At race-fire-time inference the in-place table is substrate-approximately AS-OF correct (refreshed nightly with prior day's data), but any retrospective query asking "what was the aggregate state on date X?" gets the current state, NOT the date-X state. Substrate-fix pattern: shadow `*_history` table with `snapshot_date` column; ingestion refresh dual-writes (in-place latest + snapshot append); inference reads with `WHERE snapshot_date <= race_date ORDER BY DESC LIMIT 1` AS-OF predicate. Cold-start substrate-acceptable (history empty initially, accumulates over time; fall-through to current latest at cold-start).

**Worked example**: Equine Equalizer `angle_stats` (trainer/angle win-rate aggregates) was refreshed in-place by ingestion Lambda `refresh_angle_stats` action (DELETE FROM angle_stats; INSERT new aggregates). At race-fire-time the table was approximately AS-OF (refreshed at 03:00 UTC nightly); for backtest/training the table was substrate-leaky (a 2024 race replay would see 2026 aggregate state). REPAIR-4 C.5 fix: created `angle_stats_history` (orig cols + `snapshot_date date` + NULLS NOT DISTINCT unique index on (angle_name, trainer_name, track_code, snapshot_date)); ingestion handler dual-writes; `_score_angles(row, ml_odds, race_date)` queries history with AS-OF predicate.

**Cross-references**: § 4.38 (AS-OF discipline at row-level — § 4.39 generalizes to aggregate-level); § 4.21 (UC-cycle audit-scope — aggregate-history schema migration is substrate-permanent infrastructure; ceremony cap applies); § 4.27 (inference-promoted-to-substrate-fact — angle_stats leakage class surfaced during supp-2 audit, NOT through model degradation alert).

**Audit-CC prophylactic check template**: At aggregate-statistics-table authoring time: (1) substrate-grep the table's DDL for `snapshot_date` or `as_of_date` or `created_at` column; (2) substrate-grep all INSERT/UPSERT paths to verify either (a) the table has snapshot-date semantics (every row carries the date it was computed for) OR (b) a shadow *_history table exists with snapshot_date; (3) substrate-grep all read paths for AS-OF predicates (`WHERE snapshot_date <= ?`); (4) if read path lacks AS-OF AND the table is queried during prediction generation OR backtest, flag as substrate-leakage class; (5) for legitimate in-place tables (e.g., current operational state like daily standings), require explicit comment in DDL stating "in-place by design — NOT for AS-OF replay"; (6) at backtest harness authoring time, require all aggregate reads to flow through AS-OF-aware history tables.

---

## 5. Audit-CC Prophylactic Check Templates Consolidated

This section consolidates the prophylactic checks from § 4 in paste-ready form for integration into Phase 1 audit prompts. Each check is preceded by its lesson reference for traceability.

§§ 5.1–5.7 are preserved verbatim from v2-patched (paste-ready forms of Lessons 1–7). §§ 5.8–5.9 are new at v3 (paste-ready forms for Lessons § 4.21 and § 4.20's gap-type-enumeration extension; banking origins per attribution metadata at end of each subsection).

The four-element-structure embedded checks in §§ 4.8–4.24 are not consolidated here at v3 — drafting CC integrates them into Phase 1 audit prompts case-by-case at audit-CC dispatch time. Future versions may consolidate the embedded checks into § 5 if pattern-recurrence warrants.

### 5.1 Verification-log precision check (Lesson 1, § 4.1)

For any aggregable count in the audited document:
- Verify count is decomposed where source supports decomposition (e.g., "8 = 5 Active + 3 INACTIVE").
- Verify decomposition matches source (no inflation, no compression).
- Verify "definitions vs uses vs imports" or analogous distinctions are explicit for code-reference counts.
- Verify sum is shown when decomposition has multiple parts.

Flag as MATERIAL if a count is presented compressibly when source supports decomposition.
Flag as **fabricated content (lock-blocker)** if decomposition components don't add to stated total OR if count contradicts source.

### 5.2 Methodology-interpolation check (Lesson 2, § 4.2)

For any methodology construct in the audited document, verify it traces to one of:
- Tony's locked instructions in this document's drafting spec.
- META_PLAN v9 or earlier locked Phase 0 documents (Tony-authored or QB-drafted-and-Tony-ratified).
- Operator-stated rationale per source-priority tier 5 (META_PLAN v9 § 4.5).

How to recognize:
- A construct stated as a rule with no source citation.
- A numerical threshold not present in source.
- A binary test asserting acceptability criteria not in source.
- A cadence specification not in source.
- A procedural sequencing rule not in source.
- A scoring rubric or percentage criterion not in source.

Flag as **METHODOLOGY-INTERPOLATION (lock-blocker per Tony's hard rule)** with citation to the audited section, quotation of the interpolated language, and resolution recommendation (Tony ratifies in next spec OR construct is dropped/cadence-neutralized).

### 5.3 Retroactive sweep discipline check (Lesson 3, § 4.3)

When the audited document is the first cycle after a new methodology rule lands:
- Verify the audit-CC spec for this cycle includes retroactive sweep covering all prior CC-introduced content.
- Verify the spec's retroactive sweep instruction was followed.
- Verify all flagged prior-cycle constructs map to either pre-rule grandfathered or post-rule sweep-eligible per the grandfathering clause's provenance discriminator.

Flag as MATERIAL if retroactive sweep was skipped or scoped incorrectly.

When the audited document is NOT the first cycle after a new rule lands, verify prior sweep's findings inheritance is documented.

### 5.4 Operator-verified external source check (Lesson 4, § 4.4)

When the audited document references an external source outside MCP scope:
- Verify the audit prompt provides the verbatim operator-verified quote inline.
- Verify document's prose accurately reflects the verbatim source without extension.
- Verify any nuance the source flags is preserved in the document's prose.

Flag if:
- Source referenced without operator verification provided → MATERIAL (verification gap).
- Document extends beyond what verbatim source states → MATERIAL or fabricated-content.
- Document silently softens a source's claim per a prior characterization that the verbatim source contradicts → surface as "Tony's locked decision based on a wrong premise" (Lesson 6) and recommend reframing.

### 5.5 Pattern-completion interpolation check (Lesson 5, § 4.5)

For any letter-prefix or numeric-prefix convention in the audited document:
- Grep for letter-prefix patterns (e.g., `[A-Z]\.<n>`).
- For each prefix, verify it is named in META_PLAN v9, BIBLE_STRUCTURE_SPEC v6, or a Tony-locked drafting spec for this document. Independently — pattern parallelism does NOT satisfy ratification.
- For unratified prefixes, flag as METHODOLOGY-INTERPOLATION (lock-blocker).

The check applies to: section-numbering letter prefixes, cross-reference syntax extensions, numeric-prefix conventions, any extension of an existing named pattern to adjacent cases.

The check does NOT apply to: pure numeric subsections of existing sections; references to ratified prefixes used within their established scope.

### 5.6 "Tony's locked decision based on a wrong premise" check (Lesson 6, § 4.6)

When verification of any audited claim surfaces that a Tony-locked premise underlying the claim is false:
- Audit-CC surfaces both: original locked decision's premise AND contrary verified facts.
- Audit-CC does NOT silently apply the audit recommendation when its premise is contradicted by verification.
- The pattern is bidirectional: applies to Tony's spec instructions AND to prior audit recommendations.

Flag the finding type as **"Tony's locked decision based on a wrong premise"**, severity MATERIAL. Resolution: surface to QB → Tony for explicit ratification of reframing or holding original. Do NOT pre-apply the reframing in the audit report.

### 5.7 TOC contradiction check (Lesson 7, § 4.7)

When the audited document contains shared templates referencing per-document sections by number:
- Verify all per-document templates use the same canonical section numbering for referenced positions.
- Verify cross-references between shared and per-document templates resolve consistently.
- Verify renumbering or restructuring does not break prior cross-references.

Flag as MATERIAL if any per-document template deviates from shared template's expected numbering OR if a shared-template cross-reference fails to resolve OR if renumbering broke a prior cross-reference.

The check is mechanical for the seven Phase 1 bibles: grep each bible's actual draft for canonical section headers; verify all seven drafts have the same absolute positions for the canonical 5/6/7/8 group. (Grep target is the bible drafts at `/docs/bible/<bible>.md`, not BIBLE_STRUCTURE_SPEC v6 § 6.X templates.)

### 5.8 Reference-drift refined check (refines existing reference-drift surface; new at v3 per queue item 11)

*Banked: UC-1 cycle, 2026-05-08. Patch CC's refinement of the original Q3 framing surfaced the stronger version codified here.*

For every Tier 4 working-tree-code claim in a locked bible, audit-CC cross-checks the claim against Tier 1 live state at lock authorship time. The check is especially load-bearing for claims that span multiple Lambdas with parallel implementations (Bug-#15-class drift surface): when the same logical operation is implemented in N parallel codepaths, drift between any two implementations creates a Tier-4-vs-Tier-1 mismatch surface that single-Lambda-scoped checks cannot catch.

The check is a refinement of, not replacement for, § 5.7's TOC contradiction check. § 5.7 covers intra-document TOC consistency; § 5.8 covers Tier 4 working-tree claims vs Tier 1 live state across the bible's substrate-grounded content.

How to perform:
- Enumerate Tier 4 working-tree-code claims in the audited document (file paths, function signatures, line numbers, behavior assertions tied to specific code locations).
- For each claim, cross-check against Tier 1 live state at lock authorship time (read the file at the cited path; verify the function signature; verify the line number; observe the behavior).
- For claims that span multiple Lambdas with parallel implementations (e.g., calibration logic implemented in wr_inference_service.py AND ls_inference_service.py), cross-check ALL parallel implementations, not just one.

Flag if:
- A Tier 4 claim diverges from Tier 1 live state → MATERIAL (substrate drift).
- A Tier 4 claim about parallel-implementation behavior was verified against only one implementation → MINOR (incomplete check) or MATERIAL if the unverified implementation diverges.

The check pairs with Bug #15-class drift surface awareness: when the cycle history shows parallel-implementation drift (e.g., calibration applied at one inference service but bypassed at another), the check is mandatory at lock tier.

### 5.9 Bidirectional consistency check with gap-type enumeration (refines audit-CC bidirectional checks; new at v3 per queue item 12)

*Banked: API & Frontend Bible cycle, 2026-05-08. Refines the strict-dangling interpretation of bidirectional consistency checks to enumerate four gap types.*

When auditing a Phase 1 bible's bidirectional cross-reference consistency (cross-references between this bible and other bibles in the corpus, or between this bible and locked Phase 0 documents), audit-CC enumerates five gap types (the strict-dangling case plus four extensions identified in the API & Frontend Bible cycle):

1. **Strict dangling references**: cross-reference target does not exist (the cited section / row / entry is not present in the target document). The classic dangling case.
2. **Deferral-language placeholders**: cross-reference resolves to a target that exists but contains deferral language ("[deferred to Phase X]", "[TBD]", "[pending]") rather than substantive content. The reference resolves syntactically but not semantically.
3. **NAME-vs-stable-identifier inconsistencies**: cross-reference uses a NAME (human-readable label) that may have shifted between cycles, where a stable-identifier (numeric ID, hash, immutable reference) would resolve unambiguously. Example: citing "the calibration bypass discussion" rather than "ml_layer_architecture_bible:4.3".
4. **TBD literal placeholders**: cross-reference target contains literal `TBD` or `[TBD]` placeholder content. Distinct from deferral-language placeholders by exactness of the placeholder marker.
5. **Substrate-undeterminable cells masked by deferral language**: cross-reference target's content is substrate-undeterminable (e.g., a count that depends on live state at lock time) but the bible masks the undeterminability with deferral language rather than acknowledging the substrate-undeterminability explicitly.

How to perform:
- Enumerate all bidirectional cross-references in the audited document.
- For each reference, classify against the five gap types (or PASS if none apply).
- Aggregate counts per gap type.

Flag as MATERIAL if:
- Any strict-dangling reference (gap type 1).
- Any cross-reference whose deferral-language target (gap type 2) prevents a downstream reader from completing the resolution.
- Any NAME-vs-stable-identifier inconsistency (gap type 3) that has plausible drift surface (e.g., the NAME has shifted in a recent cycle).
- Any TBD literal placeholder (gap type 4).
- Any substrate-undeterminable cell masked by deferral language (gap type 5) — the masking obscures the substrate state.

Flag as MINOR if a NAME-vs-stable-identifier inconsistency exists but the NAME is currently stable (style + reinforcement; promote to MATERIAL on observed drift).

The check is a refinement extension of the bidirectional consistency dimension of § 5.7 (TOC contradiction); the gap-type enumeration is the substantive content. Origin-cycle "Cluster B / Check 4+5" labels are unrecoverable origin-cycle artifacts; the gap-type enumeration is the codification of substantive content.

### 5.10 Pre-fix discovery comprehensiveness check (Lessons § 4.38 + § 4.39, REPAIR-4 case study)

*Banked: REPAIR-4 dispatch, 2026-05-19. When dispatching a substrate-fix for a discovered leakage class, audit-CC verifies the discovery scope is comprehensive across all known leakage surface classes before fix-code authoring begins.*

When the dispatch is a substrate-fix dispatch (UNFUCK / REPAIR class) authored in response to a substrate-divergence finding (D-class or C-class supp finding), audit-CC verifies the pre-fix discovery scope before reviewing fix-code:

1. **Row-level historical-record AS-OF discipline** (§ 4.38): substrate-grep every read path of every historical-record table (past_performances, race_history, sequence-feature tables, workout history). For each read path: does the SQL include `AND record_date < target_date`? If not, surface as candidate leakage.
2. **Aggregate-level snapshot-history discipline** (§ 4.39): substrate-grep every read path of every aggregate-statistics table (angle_stats, trainer_stats, jockey_stats, daily_variants). For each: is there a shadow `*_history` table with `snapshot_date` column? If not + the table is queried during prediction generation OR backtest, surface as candidate leakage.
3. **Write-once protection discipline** (REPAIR-4 Step B pattern): substrate-grep every INSERT into a prediction-class table. For each: does it use `ON CONFLICT (...) DO NOTHING` OR is there substrate-explicit comment documenting why DO UPDATE is intentional (e.g., DQ/payout corrections to race_results)? If neither, surface as candidate leakage class.
4. **Mandatory-parameter prophylactic guard discipline** (§ 4.32 #18 pattern): for any repository method that previously accepted an optional date filter, after fix-code adds the AS-OF predicate, verify the date parameter is REQUIRED (raises ValueError if missing) — not just defaulted to a current-date or None-with-skip. Optional date params permit substrate-regression at future callsite additions.
5. **Callsite plumbing completeness**: grep all callers of the fixed repository methods. Verify each callsite passes the AS-OF anchor parameter sourced from the race object (race.race_date) or its substrate-equivalent — not from a hardcoded value, not from environment, not from now().

How to perform: each gap class produces a substrate-pragmatic candidate list. Audit-CC submits the candidate-class enumeration verbatim to QB BEFORE fix-code authoring; QB ratifies the scope (or trims, or expands) before patch-CC dispatches. Substrate-precondition: REPAIR-4 substrate-pragmatically discovered ~2 weeks AFTER β arc supplemental investigation that pre-fix scope was substrate-incomplete (angle_stats AS-OF and ON CONFLICT DO UPDATE were not in initial discovery). The pre-fix-discovery comprehensiveness check is the prophylactic substrate-pragmatic safeguard against partial-fix dispatches.

Flag as MATERIAL if any of the five gap classes is unaudited at fix-code authoring time. Flag as **incomplete-fix-substrate (UNFUCK-class lock-blocker)** if discovery scope at dispatch time omits an applicable gap class that later substrate-surfaces during fix execution.

---

## 6. Phase 1 Audit-CC Prompt Template

This template is the canonical paste-ready structure for a Phase 1 per-bible audit-CC prompt. It extends META_PLAN v9 Appendix A.6's working example with the seven prophylactic checks from § 5. Per-bible audit prompts customize this template; the template ensures consistency across the seven Phase 1 bibles' audit cycles.

QB customizes the template per audited bible by filling the bracketed sections (`[BIBLE NAME]`, `[VERIFICATION TARGETS]`, `[REGRESSION CHECK ITEMS]`, etc.). The seven prophylactic checks remain constant across all Phase 1 audit prompts; the document-type-specific verification mandate varies per bible.

---

```
You are auditing a draft [BIBLE NAME] for the Equine Equalizer (EE) project. This is
an adversarial audit, not a friendly review. Your job is to find every reason this
document is NOT ready to be locked. Default-positive reviewing ("this looks fine")
is failure.

CONTEXT YOU NEED:

EE is a horse-racing prediction system whose Architecture Bible is being constructed
across multiple Phase 1 documents. Phase 0 produced five methodology documents
(META_PLAN v9, BIBLE_STRUCTURE_SPEC v6, AUDIT_METHODOLOGY v3, CONVERGENCE_CRITERIA v2,
TRIAGE_QUEUE_SPEC v1) that govern Phase 1 drafting. The bible you are auditing is one
of seven Phase 1 documents producing the canonical reference for what EE is.

This bible's role in the Phase 1 inventory: [PER BIBLE — drawn from BIBLE_STRUCTURE_SPEC v6 § 4.1].

The roles in this project:
  - Tony: operator, final architectural authority
  - QB: tactical orchestrator drafting Phase 0 documents and specing CC tasks
  - CC: fresh Claude Code sessions executing QB-authored specs (this is you)

The audit workflow: every Phase 1 deliverable goes through adversarial CC audit
before Tony reviews it. You are the audit-CC for this bible.

REFERENCE MATERIALS:
  - The locked Phase 0 documents at /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/
    (META_PLAN.md, BIBLE_STRUCTURE_SPEC.md, AUDIT_METHODOLOGY.md, CONVERGENCE_CRITERIA.md, TRIAGE_QUEUE_SPEC.md)
  - The DD Architecture Bible at /home/strakajagr/projects/dynasty-dugout/ARCHITECTURE_BIBLE.md
  - The EE current state dump at /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/EE_CURRENT_STATE_DUMP.md
    (NOTE: dump is best-available baseline, not source of truth; verify against live state per META_PLAN v9 § 4.5)
  - Live AWS state via `aws` CLI for any infrastructure claim verification
  - Live API endpoints (e.g., dashboard at gb5qlfy10h.execute-api.us-east-1.amazonaws.com/dashboard/metrics)
  - The EE codebase at /home/strakajagr/projects/equine-equalizer/

VERIFICATION DISCIPLINE (HARD RULE):
  - When you verify factual claims in this draft, prefer live AWS / database / code over the dump.
  - The dump has been wrong about multiple facts in prior audits. Independent verification is the safeguard.
  - For any claim about file paths, function signatures, line numbers, or behavior — read the file or run the command.
  - Counts must be decomposed (e.g., "3 instantiations + 1 import = 4 references"); do not accept compressible aggregations
    in the draft. Per the verification-log precision rule (META_PLAN v9 § 6.5; AUDIT_METHODOLOGY § 4.1).
  - Methodology constructs must trace to META_PLAN v9 / BIBLE_STRUCTURE_SPEC v6 / Tony-locked spec language.
    Per the methodology-interpolation rule (META_PLAN v9 § 6.1; AUDIT_METHODOLOGY § 4.2), CC-introduced methodology is
    a lock-blocker regardless of count.

[OPERATOR-VERIFIED EXTERNAL SOURCE BLOCK — IF APPLICABLE]
[If the audited bible references external operator-verified sources (e.g., Bug #28 memory file), QB inserts the verbatim
quote here so audit-CC can verify the document's prose against the source. Per AUDIT_METHODOLOGY § 4.4 / § 5.4.]
[Example block:
OPERATOR-VERIFIED EXTERNAL SOURCE: equine-equalizer-bug-28-hrn-scraper.md memory file's symptom statement reads
verbatim: "Place, show, and exacta payouts still populate. DD pool extraction at hrn_scraper.py:814 likely has the
same root cause." When the audited document references this source, verify document's prose matches verbatim;
flag any extension or softening.]

THE DRAFT:
[Path to draft on disk: /home/strakajagr/projects/equine-equalizer/docs/bible/<bible>.md]

COMPANION VERIFICATION LOG:
[Path to verification log: /home/strakajagr/projects/equine-equalizer/docs/bible/_audit/<bible>_v<N>_verification.md]
Read the verification log; spot-check several entries against live state; report any verification claims that don't
hold up. Per the verification-log precision rule, look specifically for compressible aggregations in log entries
that the main doc may have inflated.

YOUR ADVERSARIAL TASK:

Answer all six questions in order. Be specific. Cite section numbers. Quote draft language you are critiquing.

QUESTION 1: What's in this deliverable that I can't verify from referenced source material?
[Specific verification targets for this bible: e.g., 14 tables for Database & Schema Bible; 88 = 45 active + 43 inactive
for ML Layer Architecture Bible; 41 routes for API & Frontend Bible.]

QUESTION 2: What's missing based on the deliverable's stated scope?
[Specific scope-completeness checks: e.g., does the bible contain all canonical TOC sections per BIBLE_STRUCTURE_SPEC v6
§ 5.2? Does it satisfy its forcing function per § 3.2.1 / § 4.2 / § 4.3?]

QUESTION 3: Where is language ambiguous enough that two readers could interpret it differently?

QUESTION 4: Where does the deliverable contradict itself or other deliverables?

QUESTION 5: What sections feel rushed or hand-waved?

QUESTION 6: What examples are missing that would make abstract claims concrete?

PROPHYLACTIC CHECKS (per AUDIT_METHODOLOGY § 5):

PROPHYLACTIC CHECK 1 — Verification-log precision (§ 5.1):
[Check template inserted verbatim from § 5.1.]

PROPHYLACTIC CHECK 2 — Methodology-interpolation (§ 5.2):
[Check template inserted verbatim from § 5.2.]

PROPHYLACTIC CHECK 3 — Retroactive sweep discipline (§ 5.3):
[Check template inserted verbatim from § 5.3. Note: applicable when this audit is the first cycle after a new
methodology rule lands; otherwise verify prior sweep's findings inheritance.]

PROPHYLACTIC CHECK 4 — Operator-verified external source (§ 5.4):
[Check template inserted verbatim from § 5.4. Note: applicable when the audited document references external
sources outside MCP scope.]

PROPHYLACTIC CHECK 5 — Pattern-completion interpolation (§ 5.5):
[Check template inserted verbatim from § 5.5. Includes mechanical grep instruction.]

PROPHYLACTIC CHECK 6 — "Tony's locked decision based on a wrong premise" (§ 5.6):
[Check template inserted verbatim from § 5.6.]

PROPHYLACTIC CHECK 7 — TOC contradiction (§ 5.7):
[Check template inserted verbatim from § 5.7. Includes mechanical grep instruction over per-document templates'
canonical section headers.]

PROPHYLACTIC CHECK 8 — Reference-drift refined (§ 5.8) [NEW at v3]:
[Check template inserted verbatim from § 5.8. Tier 4 working-tree-code claims cross-checked against Tier 1 live
state; Bug-#15-class drift surface awareness for parallel implementations.]

PROPHYLACTIC CHECK 9 — Bidirectional consistency with gap-type enumeration (§ 5.9) [NEW at v3]:
[Check template inserted verbatim from § 5.9. Five gap types: strict dangling, deferral-language placeholders,
NAME-vs-stable-identifier inconsistencies, TBD literal placeholders, substrate-undeterminable cells masked
by deferral language.]

ADDITIONAL DOCUMENT-TYPE-SPECIFIC CHECKS:
[QB inserts per-bible checks here. The examples below are drawn from BIBLE_STRUCTURE_SPEC v6 § 6.X anchor verifications,
illustrative only — Phase 1 audit-CC customizations may differ based on what the specific bible drafting surfaces.
The slot's purpose is to ensure customization happens; the examples show what customization can look like.

Examples:
  - For Architecture Overview: verify the INDEX section links to all six other bibles with one-line summaries.
  - For Database & Schema Bible: verify all 14 tables documented + materialized view; verify migration discipline
    matches § 7.12.
  - For Feature Provenance Bible: verify the 14 Gonzo Sauce features named per Speed (4) + Trajectory (7) + Class (3)
    decomposition; verify the two-FE-implementation reality is documented honestly.
  - For ML Layer Architecture Bible: verify model registry semantics with 88 = 45 active + 43 inactive decomposition;
    verify the 7-layer LS stack composition matches § 9.3 CORRECT example.
  - For Model Evaluation & Retraining Bible: verify calibration bypass at wr_inference_service.py:616-626 documented
    honestly.
  - For Data Pipeline Bible: verify Bug #28 canonical entry includes verbatim quote from memory file.
  - For API & Frontend Bible: verify 41 routes documented with method/path/integration target.]

REGRESSION CHECK (for vN drafts where N >= 2):
The vN-1 audit returned specific findings. The vN draft claims fixes for each. Verify that each claimed fix
actually landed and is sound. Specifically verify:
[QB lists representative findings to spot-check, with severity and section references.]

OUTPUT FORMAT:

Produce the audit report at /home/strakajagr/projects/equine-equalizer/docs/bible/_audit/<bible>_v<N>_audit.md
with the following structure:

  - Front matter (audit subject, audit-CC role statement, threshold)
  - Summary verdict (Lock as-is / Lock after specific minor revisions / Revise + re-audit / Substantial rework)
  - Verification log audit (sample of N claims spot-checked against live state)
  - vN-1 finding regression check (if applicable)
  - Per-question findings (Q1-Q6 + prophylactic checks 1-9 + document-type-specific checks)
  - Severity assessment table (Finding # | Description | Section reference | Severity)
  - Material findings count + justification
  - Fabricated-content findings count + zero-tolerance check
  - Methodology-interpolation findings count + zero-tolerance check (post-grandfathering)
  - Recommendation (specific next actions)

SEVERITY ASSESSMENT:

Tag each finding: BLOCKER / MATERIAL / MINOR / STYLE.

  - BLOCKER: fabricated content; lock-blocker per Tony's threshold.
  - METHODOLOGY-INTERPOLATION: CC-introduced methodology Tony hasn't ratified; lock-blocker per Tony's hard rule
    regardless of MATERIAL count.
  - MATERIAL: structural issue affecting load-bearing function (methodology coherence, factual accuracy at scale,
    cross-reference integrity).
  - MINOR: localized issue, individually small.
  - STYLE: language polish, presentation choice.

THRESHOLD CONTEXT:

Tony's threshold (per META_PLAN v9 § 11; AUDIT_METHODOLOGY § 3.5):
  - < 5 MATERIAL findings AND
  - zero fabricated-content findings AND
  - zero methodology-interpolation findings (post-grandfathering)

Apply the MATERIAL/MINOR distinction honestly. A "missing example" is probably MINOR. A "the maintenance protocol
has an enforcement gap" is probably MATERIAL. A "CC-interpolated binary test that Tony hasn't ratified" is MATERIAL
by its nature per the methodology-interpolation rule and is a lock-blocker regardless of count. Use judgment —
Tony has explicitly cautioned against threshold-gaming. The operator values surfacing problems over reassurance.

If you find few flaws, the bar is wrong — re-read more skeptically.

RECOMMENDATION:

Choose one:
  - Lock as-is: zero MATERIAL, zero fabricated, zero methodology-interpolation; only MINORs/STYLE remain.
  - Lock after specific minor revisions: < 5 MATERIAL with surgical fixes available; zero fabricated; zero
    methodology-interpolation. Specify the surgical fixes.
  - Revise + re-audit: ≥ 5 MATERIAL OR ≥ 1 fabricated OR ≥ 1 methodology-interpolation. Specify the categorical
    issues that require revision and the focus of the next audit cycle.
  - Substantial rework: structural problems that require redesign of the deliverable's approach.

You are not friendly. You are looking for every reason this document is not ready. If you find few flaws, the bar
is wrong — re-read more skeptically. Begin.
```

---

## 7. Cross-Document Consistency Audit Prompt Template

The cross-document consistency audit runs after all seven Phase 1 bibles lock individually. It is a separate fresh CC session that reads all per-document audit reports as input and verifies internal consistency across the corpus. Per META_PLAN v9 § 3.3, three additional questions are appended to the six adversarial questions of META_PLAN v9 § 6.2 for cross-document audit.

The template below extends the per-bible template with cross-document-specific framing, scope, and questions.

---

```
You are conducting the cross-document consistency audit for the Equine Equalizer (EE) Phase 1 Architecture Bible.
This audit runs after all seven Phase 1 bibles have locked individually. Your scope is internal cross-document
consistency across the locked corpus. You are NOT performing the Phase 2 adversarial bible audit (which reconciles
the bible against the code; deferred to Phase 2 entry).

CONTEXT YOU NEED:

The seven Phase 1 bibles, all locked individually, are at /home/strakajagr/projects/equine-equalizer/docs/bible/:
  - architecture_overview.md
  - data_pipeline_bible.md
  - feature_provenance_bible.md
  - ml_layer_architecture_bible.md
  - model_evaluation_retraining_bible.md
  - database_schema_bible.md
  - api_frontend_bible.md

Each has a per-document audit report at /docs/bible/_audit/<bible>_audit.md and a companion verification log at
/docs/bible/_audit/<bible>_v<N>_verification.md.

The roles in this project:
  - Tony: operator, final architectural authority
  - QB: tactical orchestrator
  - CC: fresh Claude Code sessions (this is you)

You are the cross-document audit-CC. You did not draft any of the seven bibles; you did not audit any of them
individually. You are reading them all together for the first time.

REFERENCE MATERIALS:
  - All seven Phase 1 bibles + their audit reports + verification logs (paths above)
  - The locked Phase 0 documents at /docs/bible/_meta/ (META_PLAN, BIBLE_STRUCTURE_SPEC, AUDIT_METHODOLOGY,
    CONVERGENCE_CRITERIA, TRIAGE_QUEUE_SPEC)
  - The DD Architecture Bible at /home/strakajagr/projects/dynasty-dugout/ARCHITECTURE_BIBLE.md (for cross-reference
    pattern reference only)

VERIFICATION DISCIPLINE (HARD RULE):

The seven bibles are individually locked; their factual claims have been verified per their per-document audits.
Your job is NOT to re-verify per-bible factual claims (that's redundant with the per-bible audits). Your job IS to
verify cross-document consistency.

If you find a per-bible factual claim that contradicts another bible, surface the contradiction. If both bibles
have locked-but-contradictory claims, flag as cross-document MATERIAL and recommend which to revise (or surface
to Tony).

YOUR ADVERSARIAL TASK:

Answer all nine questions in order. Six are inherited from per-bible audits; three are cross-document-specific
per META_PLAN v9 § 3.3.

QUESTION 1: What's in any bible that I can't verify from the referenced source material across other bibles?
[Examples: a feature_provenance_bible reference to ml_layer_architecture_bible:5.4 — does that section exist?
a data_pipeline_bible reference to a flow that's documented in architecture_overview's Lambda inventory — do
the two descriptions match?]

QUESTION 2: What's missing across the corpus based on its stated scope?
[Per BIBLE_STRUCTURE_SPEC v6 § 4: are all canonical TOC sections present in all seven bibles? Per the convergence
test (META_PLAN v9 § 3.2.1): can a fresh CC session evaluate / rebuild / retrain a model in the gallery using only
the locked corpus?]

QUESTION 3: Where is language ambiguous enough that two readers could interpret it differently across bibles?

QUESTION 4: Where do bibles contradict each other across files?
[Specifically: same fact stated differently in different bibles; same canonical name used inconsistently;
cross-references broken.]

QUESTION 5: What sections feel rushed or hand-waved within the corpus context?

QUESTION 6: What examples are missing that would make abstract claims concrete across the corpus?

QUESTION 7 (cross-document, per META_PLAN v9 § 3.3): Does the bible say something the code does not do?
[Phase 1 cross-document scope: limit to claims surfaced by bible-vs-bible cross-reference analysis. Full code-vs-
bible reconciliation is Phase 2.]

QUESTION 8 (cross-document, per META_PLAN v9 § 3.3): Does the code do something the bible does not say?
[Phase 1 cross-document scope: limit to gaps in coverage that bible-vs-bible analysis surfaces. Full code-vs-bible
gap analysis is Phase 4.]

QUESTION 9 (cross-document, per META_PLAN v9 § 3.3): Where do bible documents contradict each other across files?
[The canonical cross-document audit question. Specifically:
  - Cross-cutting bug canonical-home assignments (per BIBLE_STRUCTURE_SPEC v6 § 5.3): is each cross-cutting bug
    homed in exactly one bible with cross-references from others, never duplicated?
  - Canonical object names (per BIBLE_STRUCTURE_SPEC v6 § 4.1.1 in architecture_overview): consistent across all
    bibles that reference them?
  - Canonical section numbering (per BIBLE_STRUCTURE_SPEC v6 § 5.2 mandatory 5/6/7/8): all seven bibles compliant?
  - Cross-bible references (`<bible_name>:<section_id>`): every reference resolves to an actual section in the
    target bible?]

PROPHYLACTIC CHECKS (per AUDIT_METHODOLOGY § 5):

The prophylactic checks apply across the corpus, not within single bibles:

PROPHYLACTIC CHECK 1 — Verification-log precision across the corpus (§ 5.1):
For aggregable counts cited across multiple bibles (e.g., 88 = 45 active + 43 inactive cited in ml_layer_architecture_bible
AND model_evaluation_retraining_bible AND elsewhere), verify decomposition matches across all citations.

PROPHYLACTIC CHECK 2 — Methodology-interpolation across the corpus (§ 5.2):
For methodology constructs introduced in any bible (e.g., a new discipline rule), verify the construct traces to
META_PLAN v9 / BIBLE_STRUCTURE_SPEC v6 / Tony-locked drafting spec. Per-bible audits should have caught individual
instances; this check sweeps for any that survived multiple per-bible audits.

PROPHYLACTIC CHECK 3 — Retroactive sweep discipline (§ 5.3):
Verify cross-document audit specifically sweeps for instances of newly-introduced rules that may not have been
caught by per-bible audits. Phase 1 introduces no new methodology rules (it operates under META_PLAN v9 +
BIBLE_STRUCTURE_SPEC v6 + AUDIT_METHODOLOGY v3 already-locked); the retroactive sweep here verifies all seven
bibles uniformly applied the locked rules.

PROPHYLACTIC CHECK 4 — Operator-verified external source (§ 5.4):
For operator-verified external sources cited across multiple bibles (e.g., Bug #28 memory file cited from
data_pipeline_bible's W.<n> entry and possibly cross-referenced from ml_layer_architecture_bible's calibration-bypass
discussion), verify all citations match the verbatim source.

PROPHYLACTIC CHECK 5 — Pattern-completion interpolation (§ 5.5):
For letter-prefix or numeric-prefix conventions used across the corpus (W.N is the only ratified letter-prefix per
BIBLE_STRUCTURE_SPEC v6 § 5.5), grep all seven bibles for any unratified prefix conventions. Pattern parallelism
across multiple bibles does NOT constitute ratification.

PROPHYLACTIC CHECK 6 — "Tony's locked decision based on a wrong premise" (§ 5.6):
When cross-document analysis surfaces that a Tony-locked premise underlying any bible's content is false (per
verification across the corpus), surface to QB → Tony per the bidirectional pattern.

PROPHYLACTIC CHECK 7 — TOC contradiction (§ 5.7):
The MECHANICAL CHECK: grep each of the seven bibles for canonical 5/6/7/8 section headers (Discipline rules /
Currently Open / Deprecated / What Was Fixed). Verify all seven bibles have these four sections at canonical
absolute positions. Verify cross-bible references targeting these positions resolve consistently.

PROPHYLACTIC CHECK 8 — Reference-drift refined (§ 5.8) [NEW at v3]:
For Tier 4 working-tree-code claims spanning multiple bibles (e.g., Lambda implementations referenced from
multiple bibles), cross-check each implementation against Tier 1 live state. Bug-#15-class drift surface
awareness for parallel implementations is operative across the corpus.

PROPHYLACTIC CHECK 9 — Bidirectional consistency with gap-type enumeration (§ 5.9) [NEW at v3]:
For all cross-bible references in the corpus, classify against the five gap types (strict dangling, deferral-language
placeholders, NAME-vs-stable-identifier inconsistencies, TBD literal placeholders, substrate-undeterminable cells
masked by deferral language). Aggregate counts per gap type.

CROSS-CUTTING CONSISTENCY ENUMERATION:

Specific cross-cutting consistency targets to verify:
  - Bug #28 canonical home in data_pipeline_bible:8.W.<n>; cross-references from any other bible by ID, never
    duplicated content.
  - Bug #15 canonical home in feature_provenance_bible:8.W.<n>; cross-references from ml_layer_architecture_bible:8
    and model_evaluation_retraining_bible:8 by ID, never duplicated content.
  - Bug #24 canonical home in model_evaluation_retraining_bible:8.W.<n>; cross-reference from ml_layer_architecture_bible:8
    by ID.
  - Calibration bypass state at wr_inference_service.py:616-626: documented in ml_layer_architecture_bible § 4.3 and
    cross-referenced from model_evaluation_retraining_bible § 4.2.1 — both descriptions consistent.
  - Model registry decomposition (88 = 45 active + 43 inactive): consistent across ml_layer_architecture_bible § 3.1
    and model_evaluation_retraining_bible § 4.3.1.
  - Lambda inventory (8 = 5 Active + 3 INACTIVE): documented in architecture_overview § 3.1; references from
    data_pipeline_bible's per-flow sections and api_frontend_bible's integration mapping consistent with the inventory.
  - The canonical TOC 5/6/7/8 mandate: all seven bibles compliant (mechanical grep check).
  - INDEX completeness in architecture_overview § 4.3: all six other bibles linked with one-line summaries.

OUTPUT FORMAT:

Produce the cross-document audit report at /home/strakajagr/projects/equine-equalizer/docs/bible/_audit/cross_document_audit.md
with the following structure:

  - Front matter (audit subject: cross-document consistency; audit-CC role; threshold)
  - Summary verdict
  - Per-bible cross-cutting trace (which bibles contain references to each canonical home; consistency verified)
  - Per-question findings (Q1-Q9 + prophylactic checks 1-9)
  - Cross-cutting consistency table (by canonical home: where homed, where referenced, consistency status)
  - Severity assessment table
  - Material findings count + justification
  - Recommendation

THRESHOLD CONTEXT:

Same threshold as per-bible audits:
  - < 5 MATERIAL findings AND
  - zero fabricated-content findings AND
  - zero methodology-interpolation findings (post-grandfathering)

Per-bible re-revision trigger: per META_PLAN v9 § 3.3, "if a per-document audit returns >5 MATERIAL findings, that
document goes back to Phase 1 revision before the cross-document audit runs." That trigger is checked before this
audit runs; you can assume the seven bibles are individually under threshold. Your job is to find any cross-document
issue not surfacing within any single bible's audit.

If cross-document audit returns ≥ 5 MATERIAL OR ≥ 1 fabricated OR ≥ 1 methodology-interpolation, the affected
bibles return to Phase 1 revision.

You are not friendly. You are looking for inconsistencies between locked documents that individual per-bible
audits could not have surfaced because they read only one bible at a time. If you find few inconsistencies across
seven independently-drafted bibles, the bar is wrong — re-read more skeptically. Begin.
```

---

## 8. Open Questions

Surfaced for resolution during Phase 0 iteration. Not blocking AUDIT_METHODOLOGY lock unless audit returns one as critical.

§§ 8.1–8.3 are preserved verbatim from v2-patched. §§ 8.4–8.5 are new at v3 per R8 substrate-grounded landing (queue item 21 + Candidate #6 per the AUDIT_METHODOLOGY meta-cycle).

### 8.1 Per-bible audit prompt customization granularity

§ 6's template includes `[ADDITIONAL DOCUMENT-TYPE-SPECIFIC CHECKS]` as a customization slot. The customizations listed in the template's example block (verify INDEX section for Architecture Overview; verify 14 tables for Database & Schema; etc.) are illustrative, not prescriptive. Whether each Phase 1 audit prompt is hand-customized by QB at audit time OR derived from a per-bible template QB pre-writes is a Phase 1 working-agreement decision per the pattern established in META_PLAN v9 § 7.13's deferral-to-Phase-5 framing applied to Phase 1 audit-CC prompt drafting cadence.

[OPEN — v3 cycle disposition: UNAFFECTED. The v3 cycle's queue items address methodology lessons + audit-CC checks + QB self-checks; no v3 promotion closes the per-bible audit prompt customization granularity question. Question carries forward.]

### 8.2 Cross-document audit re-trigger after per-bible revision

If the cross-document audit surfaces a finding that requires one bible to revise, that bible re-locks per its own per-bible cycle. Whether the cross-document audit re-runs immediately, runs only at Phase 1 final completion, or follows a different cadence is deferred — per META_PLAN v9's pattern of deferring cadence-shaped decisions to operational phase entry.

[OPEN — v3 cycle disposition: UNAFFECTED. Question carries forward; cadence-shape decisions remain deferred to operational phase entry.]

### 8.3 Inheritance verification across audit cycles

Per § 4.3's retroactive sweep discipline, when a methodology rule lands in cycle N, the audit-CC spec for cycle N+1 includes retroactive sweep. For Phase 1 audits, no new methodology rules are introduced (Phase 1 operates under locked Phase 0 documents); inheritance verification is the relevant check rather than retroactive sweep. The check template in § 5.3 covers both — when first-cycle-after-rule-introduction, perform sweep; otherwise, verify inheritance documented. Whether Phase 1 audits need any further refinement of the inheritance check is deferred until Phase 1 audit cycles surface a need.

[OPEN — v3 cycle disposition: UNAFFECTED. Question carries forward; § 4.21 (UC-cycle audit-scope methodology lesson) is related but addresses UPSTREAM-CORRECTION cycle audit-tier sizing, not inheritance verification at Phase 1 per-bible audit cycles.]

### 8.4 PHASE_5_BACKLOG.md vocabulary reconciliation strategy (NEW at v3 per queue item 21)

*Banked: AUDIT_METHODOLOGY meta-cycle (post-Phase-1 dispatch sequence 4 of 4), 2026-05-08. Per R8 substrate-grounded landing, queue item 21 lands under § 8 Open Questions umbrella; final strategy selection surfaces to Tony at SP-A2 review.*

PHASE_5_BACKLOG.md (substrate-verified at `/home/strakajagr/projects/equine-equalizer/docs/bible/PHASE_5_BACKLOG.md`) currently carries dual vocabulary:

- **Phase 5.3.1 seed entry**: retains META_PLAN v6 § 11 vocabulary (BLOCKER / MATERIAL / MINOR / STYLE) per origination context (the seed entry was created at Phase 0 exit per META_PLAN v6 § 8.2; its vocabulary mirrored the Phase 0 cycle's locked threshold language).
- **Phase 5.3.2 through 5.3.26 entries**: use TRIAGE_QUEUE_SPEC v1 vocabulary (HIGH / MEDIUM / LOW) per locked-2026-05-04 spec authoritative for Phase 1+ entries.

The reconciliation was deferred per PHASE_5_BACKLOG.md header line 12 declaration; the AUDIT_METHODOLOGY meta-cycle ratifies the reconciliation strategy. Three candidate strategies are codified here; final strategy selection is a Tony ratification surface at SP-A2.

#### Candidate strategy (a): Re-tag Phase 5.3.1 seed to TRIAGE_QUEUE_SPEC v1 vocabulary with substrate-grounded severity mapping

Re-tag the Phase 5.3.1 seed entry from META_PLAN v6 § 11 vocabulary (BLOCKER / MATERIAL / MINOR / STYLE) to TRIAGE_QUEUE_SPEC v1 vocabulary (HIGH / MEDIUM / LOW). The substrate-grounded mapping for the seed (Bug #28 — HRN scraper data-acquisition substrate corruption affecting production payout extraction) likely maps to **HIGH** severity given the production-impact substrate.

**Pros:** Single-vocabulary corpus across all 26 entries; future entries unambiguously tagged with the locked-2026-05-04 vocabulary. Eliminates ambiguity at Phase 5 execution time when the operator queries by severity.

**Cons:** Requires retroactive amendment of a Phase 0 exit artifact (Phase 5.3.1 seed). The original META_PLAN v6 vocabulary tag carries historical context (Phase 0 cycle's locked language); re-tagging loses the historical traceability unless preserved in a parenthetical annotation.

#### Candidate strategy (b): Preserve dual-vocabulary as documented historical-evolution record

Preserve Phase 5.3.1 seed at META_PLAN v6 § 11 vocabulary; preserve Phase 5.3.2-5.3.26 at TRIAGE_QUEUE_SPEC v1 vocabulary. PHASE_5_BACKLOG.md header line 12 declaration is upgraded from "deferred" to "ratified preservation" — the dual-vocabulary state is the locked record of methodology evolution.

**Pros:** No retroactive amendments; historical traceability preserved (the seed entry carries Phase 0 cycle's vocabulary; subsequent entries carry post-lock TRIAGE_QUEUE_SPEC v1 vocabulary; the boundary is the methodology-evolution marker).

**Cons:** Phase 5 execution must handle dual-vocabulary translation; future entries must explicitly tag the vocabulary they use; query-by-severity becomes less direct.

#### Candidate strategy (c): Alternative

Tony may direct an alternative strategy at SP-A2 ratification. Examples of alternatives that emerged during meta-cycle dispatch:

- (c.1) Maintain dual-vocabulary in body, but author a header-level translation table mapping vocabulary-A to vocabulary-B for Phase 5 query consumption. Combines (a)'s query-uniformity with (b)'s historical preservation.
- (c.2) Re-tag the seed AND amend PHASE_5_BACKLOG.md header line 12 declaration to "reconciled to TRIAGE_QUEUE_SPEC v1 vocabulary at AUDIT_METHODOLOGY v3 meta-cycle (2026-05-08); seed's prior vocabulary preserved in parenthetical annotation per § 4.17 locked-content preservation discipline."
- (c.3) Defer reconciliation to Phase 5 entry (when the operator first queries the backlog). The reconciliation timing is operational, not methodology-prescriptive.

#### Ratified strategy

[Pending Tony ratification at SP-A2.] Drafting CC's recommendation: **strategy (c.2)** — re-tag Phase 5.3.1 seed to TRIAGE_QUEUE_SPEC v1 vocabulary (HIGH for Bug #28 per substrate-grounded production-impact assessment) AND amend PHASE_5_BACKLOG.md header line 12 declaration to ratified-reconciliation language; seed's prior vocabulary preserved in parenthetical annotation per § 4.17. This combines (a)'s query-uniformity benefit with (b)'s historical-preservation benefit, and is consistent with § 4.17 locked-content preservation discipline (the seed's drafting-time vocabulary is preserved in annotation; the metadata transitions to current vocabulary).

The ratified strategy will be documented in the v3 changelog (§ 10) and applied to PHASE_5_BACKLOG.md as a separate mechanical-paste cycle post-AUDIT_METHODOLOGY-v3 lock.

### 8.5 Bible-corpus-uniform component-count standardization (Candidate #6, NEW at v3)

*Banked at PHASE_5_BACKLOG triage, API & Frontend Bible cycle. Per R8 substrate-grounded landing, Candidate #6 lands under § 8 Open Questions umbrella; final disposition surfaces to Tony at SP-A2 review.*

The seven Phase 1 bibles each carry component counts (e.g., 14 tables in Database & Schema; 88 = 45 active + 43 inactive in ML Layer Architecture; 41 routes in API & Frontend; 8 = 5 Active + 3 INACTIVE Lambdas in Architecture Overview; 14 Gonzo Sauce features in Feature Provenance). Whether the corpus benefits from a uniform component-count standardization rule (e.g., "every bible's Discipline rules section lists exactly N components per the canonical taxonomy") is a methodology question banked at PHASE_5_BACKLOG triage from the API & Frontend Bible cycle.

The question is methodology-shape, not Phase 5 work — uniformity may not be a virtue if the bibles' component types vary in their natural cardinality (a bible covering 14 tables ≠ a bible covering 41 routes ≠ a bible covering 88 model-registry rows). Forcing uniformity could introduce taxonomy contortions; preserving heterogeneity could leave query patterns inconsistent across the corpus.

#### Candidate disposition (a): Defer to Phase 5

Defer the standardization question to Phase 5 entry. Phase 5 is the operational phase; if the heterogeneity becomes a friction surface during Phase 5 query patterns, the standardization can be authored at that point with operational evidence.

**Pros:** No premature methodology constraint; Phase 5 operational evidence drives the decision.

**Cons:** The heterogeneity may continue as a low-grade query-pattern friction across Phase 5; if standardization is the right answer, deferring delays its benefit.

#### Candidate disposition (b): Codify uniform-count rule in BIBLE_STRUCTURE_SPEC

Author a uniform component-count rule in BIBLE_STRUCTURE_SPEC v6 (or future v7) requiring each bible's Discipline rules section to enumerate components per a canonical taxonomy. The rule would force taxonomy decisions at lock tier and produce uniform-count corpus.

**Pros:** Uniform query patterns across the corpus; operator can ask "how many components in <bible>" with consistent semantics.

**Cons:** Forcing uniformity may distort taxonomies; the natural cardinality of bibles varies; some bibles may need synthetic groupings to fit the uniform structure.

#### Candidate disposition (c): Preserve current heterogeneity

Maintain the heterogeneous component-count state explicitly. Each bible enumerates components per its natural cardinality; cross-bible queries handle heterogeneity at query time.

**Pros:** Honest taxonomies (each bible reflects its natural component structure); no taxonomy distortion.

**Cons:** Query patterns vary across the corpus; operators must adapt query approach per bible.

#### Drafting CC recommendation

[Pending Tony disposition at SP-A2.] Drafting CC's recommendation: **disposition (a) — defer to Phase 5**. The standardization question is methodology-shape but the cost-benefit analysis depends on operational evidence not yet accumulated. Phase 5 operational evidence (which query patterns are actually used; which bibles' heterogeneity creates friction) is the discriminator. Premature codification risks distortion; deferral preserves optionality.

The disposition will be documented in the v3 changelog (§ 10) and (if disposition (b)) propagated to BIBLE_STRUCTURE_SPEC v7 cycle scope at next Phase 0 cycle.

---

## 9. Lock Status

**Document status:** DRAFT v3, pre-audit
**Audit-CC pass:** pending (v3 audit pending after disk write at SP-A2)
**Verification log:** pending — v3 cycle's authorization scope (per Lesson § 4.12 bounded-authorization discipline) limited drafting CC's substrate reads to META_PLAN v9 + BIBLE_STRUCTURE_SPEC v6 + AUDIT_METHODOLOGY v2-patched + CONVERGENCE_CRITERIA v2 + TRIAGE_QUEUE_SPEC v1; v1-draft does not introduce new EE-substrate factual claims requiring verification log entries. Verification log scope assessment is a Tony ratification surface at SP-A2.
**Tony review:** pending (will see post-audit version per workflow discipline)
**Locked:** [pending audit + Tony review + iteration cycles]

**Phase 0 prerequisites carried over from META_PLAN v9 § 11:**
- All 5 Phase 0 documents pass adversarial audit (Tony's threshold: < 5 MATERIAL findings AND zero fabricated-content findings AND zero methodology-interpolation findings). Current Phase 0 lock state: META_PLAN v9 LOCKED 2026-05-05, BIBLE_STRUCTURE_SPEC v6 LOCKED 2026-05-05, AUDIT_METHODOLOGY (this document) DRAFT v3, CONVERGENCE_CRITERIA v2 DRAFT (pre-audit), TRIAGE_QUEUE_SPEC v1 DRAFT (pre-audit).

v3 meta-cycle executed against partial Phase 0 lock state: META_PLAN v9 + BIBLE_STRUCTURE_SPEC v6 LOCKED 2026-05-05; CONVERGENCE_CRITERIA v2 + TRIAGE_QUEUE_SPEC v1 in DRAFT state at v3 authorship time. Methodology baseline operationally sufficient for v3 cycle scope; future Phase 0 lock cycles for CONVERGENCE_CRITERIA v2 + TRIAGE_QUEUE_SPEC v1 may follow as separate post-Phase-1 work.
- Operating-model convergence test passes (META_PLAN v9 § 5.4)
- EE production code committed to baseline (META_PLAN v9 § 3.1.1)
- `.gitignore` baseline audit performed; findings documented at `_audits/gitignore_baseline_audit.md` (META_PLAN v9 § 7.14)
- `PHASE_5_BACKLOG.md` created with Bug #28 as first entry (META_PLAN v9 § 8.2). PHASE_5_BACKLOG.md current entry count was out-of-scope substrate for the v3 cycle (per spec § 2 substrate authorization). Entry count is verifiable post-lock at separate cycle; v3 cycle does not assert specific entry count.

**Phase 1 status:** Phase 1 bibles' lock state was out-of-scope substrate for the v3 cycle (per spec § 2 substrate authorization). v3 cycle dispatch context indicated Phase 1 cohort cycles completed prior to v3 dispatch; specific lock-version and lock-date enumeration is verifiable post-lock at separate cycle.

**v3 cycle pending actions:** QB writes paste-ready audit-CC prompt for v3 (separate session per Q1 ratification + Self-Audit Check 5 generalization (§ 12.5)). Tony runs audit. QB synthesizes findings. Patch CC tier dispatches if audit findings non-trivial. Lock-CC tier finalizes the three-element metadata bundle and transitions Status to LOCKED v3.

---

## 10. Changelog

Per spec § 8 metadata bundle requirements + R8.b ratification, § 10 is the revision-history block target. v3 entry authored chronological-forward per v2-patched § 10 existing convention (v1 → v2 ordered chronologically forward).

### v1 → v2

**MATERIAL fixes (v1 audit findings):**

- **Finding 1 — § 4.6 Lesson 6 worked example invocation 1 verbatim attribution.** v1 paraphrased the v2 audit Q2.2 text and Tony's Q4 directive while presenting them as verbatim quotes. v2 replaces both paraphrased strings with actual verbatim text from META_PLAN_v2_audit.md line 47 (the four-sentence finding text) and lines 237-241 (Tony's Q4's four bullets). Per Tony's Q2a Option (a) ratification: verbatim from source preserves the worked example's pedagogical force as a positive demonstration of the operator-verified-source pattern, rather than as an inadvertent demonstration of the rule's violation. Verification log Claim 42 added per Q2b.

- **Finding 3 — § 6 audit-CC prompt template customization slot refinement framing.** v1's `[ADDITIONAL DOCUMENT-TYPE-SPECIFIC CHECKS]` slot listed illustrative per-bible examples without Tony's Q3-ratified four-component refinement framing. v2 inserts the framing as the slot's preamble: "drawn from BIBLE_STRUCTURE_SPEC v3 § 6.X anchor verifications, illustrative only — Phase 1 audit-CC customizations may differ based on what the specific bible drafting surfaces. The slot's purpose is to ensure customization happens; the examples show what customization can look like."

**MINOR fixes (tightly coupled to MATERIALs in pedagogical purpose, per Tony's Q1 Option B):**

- **Finding 5 — § 4.2 prophylactic check pattern recognition example.** v1's recognition example listed two numerical thresholds: "3 consecutive iterations" (CC-introduced; caught in v5 audit M-1) and "5 MATERIAL findings" (Tony-ratified per v6 § 11). The latter is a Tony-locked construct and confused the recognition example by suggesting Tony-ratified content might be flaggable. v2 drops "5 MATERIAL findings"; example now reads: "A numerical threshold (e.g., '3 consecutive iterations') in the audited document not present in the drafting spec or locked source."

- **Finding 6 — § 4.7 / § 5.7 "per-document template" language ambiguity.** v1's mechanical grep instruction read "for the seven Phase 1 bibles, grep each per-document template for canonical section headers" — "per-document template" was ambiguous between (a) BIBLE_STRUCTURE_SPEC v3 § 6.X templates (the spec) and (b) the actual bible drafts at `/docs/bible/<bible>.md` (the audit target). v2 clarifies: "grep each bible's actual draft for canonical section headers" with parenthetical distinguishing the bible drafts from the spec templates.

**STYLE observations (#7-#9) deferred per Tony's Q1 ratification:** § 4.4 binary severity-mapping criterion clarification opportunity; § 4.3 "subsequent cycles inherit prior sweep" rationale opportunity; § 4.5 mechanical grep regex worked-trace example opportunity. Per the methodology-interpolation principle, these don't compound into Phase 1 risk and are deferred — Phase 1 first audit cycles will surface real-world friction if any exists.

**Methodology lesson recorded (v1 → v2):**

The v1 audit's catch on Finding 1 (paraphrase-as-verbatim in the document codifying the verification-log-precision rule) is a recursive instance of the rule. AUDIT_METHODOLOGY codifies the rule; AUDIT_METHODOLOGY's own content must demonstrate the rule. v1 violated; v2 demonstrates compliance. The worked example in § 4.6 invocation 1 now shows what Phase 1 audit-CCs should produce: the v2 audit text and Tony's Q4 directive presented in their full verbatim form, with no paraphrasing presented under quote marks.

The v1 cycle adds one data point to the methodology-interpolation rule's operational test: codifying the methodology rules themselves does not require introducing new methodology rules, but it DOES require recursive application of those rules to the codifying document's own content. The v1 audit-CC's catch demonstrates the rule's reflexivity; the v2 fix demonstrates compliance.

**Retained from v1 unchanged:**

Front matter (revised for v2 metadata), § 1, § 2, § 3, § 4 (front matter through § 4.5 except § 4.2's recognition example), § 4.5, § 4.6 (everything except invocation 1's verbatim quotes), § 4.7 (everything except the mechanical grep target language), § 5 (everything except § 5.7's mechanical grep target language), § 6 (everything except the customization slot's preamble), § 7, § 8, § 9, § 11. Verification log inherits 41 claims; v2 adds 1 new claim.

### v1 (initial draft)

Initial CC draft per Tony's locked Q1 (Phase 1 audit methodology only) and locked Q2 (Tier 3 with companion verification log). Document scope per Q1: Phase 1 per-bible audit cycle + Phase 1 cross-document consistency audit + audit-CC prophylactic check templates. Out of scope: Phase 0 audit cycles already settled; Phase 2-4 audit methodology (deferred to phase entry); bible content, success criteria, and triage queue format (BIBLE_STRUCTURE_SPEC v3 / CONVERGENCE_CRITERIA / TRIAGE_QUEUE_SPEC respectively).

Methodology lessons catalog (§ 4) covers seven items in empirical sequence of introduction across Phase 0 cycles: verification-log precision rule (META_PLAN v3 → v4); methodology-interpolation rule with named patterns + catch-all + grandfathering clause (META_PLAN v3 → v4 → v5 → v6); audit-CC retroactive sweep discipline (META_PLAN v5 → v6); operator-verified external source pattern (META_PLAN v6 cycle); pattern-completion interpolation pattern (BIBLE_STRUCTURE_SPEC v1 → v2); "Tony's locked decision based on a wrong premise" pattern (META_PLAN v3 + v6, recurring); TOC contradiction class (BIBLE_STRUCTURE_SPEC v1 → v2 → v3, recurring).

Each lesson presented with the four required structural elements: abstract rule statement; worked example from Phase 0 cycles with specific cycle, finding, and resolution citations; cross-references to META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 sections; audit-CC prophylactic check template (what to look for, how to recognize, how to flag).

§ 5 consolidates the seven prophylactic checks in paste-ready form for integration into Phase 1 audit prompts. § 6 provides the Phase 1 per-bible audit-CC prompt template extending META_PLAN v6 Appendix A.6. § 7 provides the cross-document consistency audit prompt template extending § 6 with three cross-document-specific questions per META_PLAN v6 § 3.3 plus cross-cutting consistency enumeration.

No new flagging thresholds introduced; thresholds inherited from META_PLAN v6 § 11. No new methodology constructs introduced beyond what META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 / Tony's locked drafting spec for this document explicitly authorize.

### v2 → v2-patched (2026-05-05)

Four lessons banked in § 4 (Lessons § 4.8 / § 4.9 / § 4.10 / § 4.11) emerged from the Database & Schema Bible v1 cycle (drafting + audit + Tony ratifications 2026-05-05). Lessons cover: § 4.8 QB substrate findings during spec authorship require Tony ratification; § 4.9 QB review pass is light surface only; § 4.10 verbatim-paste discipline for V1-N entries; § 4.11 grep predictions against bootstrap-mirror file unions. Each lesson follows the existing four-element structure (abstract rule + worked example + cross-references + audit-CC prophylactic check template). Banked at next-sequential slots per the file's § 4.X = Lesson X convention. Substrate observation surfaced in `database_schema_bible_v1_verification.md` Section I V1-patch-10.

### v2-patched → v3 (2026-05-08)

**Cycle:** AUDIT_METHODOLOGY meta-cycle (post-Phase-1 dispatch sequence 4 of 4).

**Cycle ratifications by Tony 2026-05-08:** Q1–Q8 + R1–R7 + R8 + R8.a + R8.b + D1–D4. Substrate-grounded section landing per R8 (new content integrates into existing v2-patched §§ 6–11 structure rather than displacing).

**Promotion summary:** 21 queue items + 3 awareness items integrated.

- **§ 4.X new lessons (§§ 4.12–4.24):** 13 new lessons banked at this cycle.
  - § 4.12 — Low-cost substrate verification at row-authorship (queue item 2; Phase 1 Cohort parallel-cohort handoff).
  - § 4.13 — Inheritance read-scope discipline (queue item 1; Phase 1 Cohort parallel-cohort handoff).
  - § 4.14 — Intra-document section reference convention (queue item 3; Phase 1 Cohort parallel-cohort handoff).
  - § 4.15 — Composite-row treatment for orphan classes (queue item 4; Phase 1 Cohort parallel-cohort handoff).
  - § 4.16 — Lock-CC three-element metadata bundle (queue item 5; Phase 1 Cohort parallel-cohort handoff).
  - § 4.17 — Locked bibles preserve drafting-time historical context (queue item 6; Phase 1 Cohort parallel-cohort handoff).
  - § 4.18 — Drafting-CC paste-prompts must mandate metadata-bundle initialization (queue item 7; Phase 1 Cohort parallel-cohort handoff).
  - § 4.19 — QB paste-verbatim discipline reinforcement (queue item 8; PHASE_5_BACKLOG.md reconciliation cycle).
  - § 4.20 — Pattern A bundling default + Pattern B exception (queue item 9; API & Frontend Bible cycle).
  - § 4.21 — UC-cycle audit-scope methodology lesson (queue item 10; UC-1 cycle).
  - § 4.22 — Two-tier cross-reference convention codification (queue item 18; carried-forward deferral from parallel cohort).
  - § 4.23 — database_schema_bible:V1-12 verification-log-claim-ID convention (queue item 19; carried-forward deferral from Database & Schema Bible cycle).
  - § 4.24 — Verbatim-paste verlog-growth modeling (queue item 20; carried-forward deferral from prior cycle).

- **§ 5.X new audit-CC prophylactic checks (§§ 5.8–5.9):** 2 new checks banked at this cycle.
  - § 5.8 — Reference-drift refined check (queue item 11; UC-1 cycle).
  - § 5.9 — Bidirectional consistency check with gap-type enumeration (queue item 12; API & Frontend Bible cycle).

- **§ 12 new section — QB Self-Audit Checks (§§ 12.1–12.5):** 5 new QB-tier self-audit checks banked at this cycle.
  - § 12.1 — Estimation calibration (queue item 13; cycle-originated Self-Audit Check finding).
  - § 12.2 — Self-describing authorization redundancy detection (queue item 14; cycle-originated).
  - § 12.3 — Paste-prompt transit-truncation discipline (queue item 15; cycle-originated; bookend markers PROMPT BEGINS / PROMPT ENDS).
  - § 12.4 — Within-message placeholder discipline (queue item 16; cycle-originated).
  - § 12.5 — Meta-document state claim substrate verification (queue item 17; cycle-originated; Awareness item B scope clause integrated verbatim).

- **§ 8.X new subsections (§§ 8.4–8.5):** Per R8 substrate-grounded landing, queue item 21 + Candidate #6 land under § 8 Open Questions umbrella with novel ratification surfaces at SP-A2.
  - § 8.4 — PHASE_5_BACKLOG.md vocabulary reconciliation strategy (queue item 21).
  - § 8.5 — Bible-corpus-uniform component-count standardization (Candidate #6).

- **Awareness item dispositions (3 items):**
  - Awareness item A (path drift retroactive correction scope): OUT-OF-SCOPE this cycle. Resolved at Q8 — added as PHASE_5_BACKLOG.md entry 5.3.27 LOW post-AUDIT_METHODOLOGY-v3 lock as separate mechanical-paste cycle. NOT integrated into v3 body.
  - Awareness item B (historically: 'Self-Audit Check 14 generalization scope'; now codified at § 12.5): FOLDED INTO § 12.5 codification as explicit scope clause covering "ALL meta-document inheritance, not just PHASE_5_BACKLOG.md" + "fabricated-by-accumulation" failure mode.
  - Awareness item C (three-tier-confirmed Lesson § 4.12 bounded-authorization positive operational precedent): integrated VERBATIM into revision history block (header v3 entry above + § 10 v3 entry below). Operational precedent banking text per spec § 6.

- **Phase 0 cross-reference re-validation (per Obs C / R7):** Header anchors updated from META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 to META_PLAN v9 / BIBLE_STRUCTURE_SPEC v6. In-body cross-references updated: most v6 § X.Y references preserved at same numbering in v9 (verified during authorship); the v6 § 12 reference in § 4.1, § 4.2, § 4.3, § 4.6 cross-references updated to v9 § 12.4 (the v5→v6 changelog subsection within v9 § 12 changelog). Historical citations referencing specific past versions (META_PLAN v3 audit, BIBLE_STRUCTURE_SPEC v1 audit, etc.) preserved verbatim as immutable historical references.

**Section-renumbering report:** Zero renumbering of v2-patched §§ 6–11 (R8 Option-b discipline). New § 12 appended; §§ 6, 7, 8, 9, 10, 11 preserved at original numbering. Eight intra-document cross-references at v2-patched lines 19, 124 (×2), 1209, 1266, 1276, 1292, 1293 preserved verbatim with original section numbers.

**Operational precedent banking (v3 authorship, 2026-05-08):** Lesson § 4.12 bounded-authorization discipline confirmed operating cleanly at drafting CC + audit CC + patch CC tiers across six post-Phase-0 cycle classes (Database & Schema, Data Pipeline, parallel cohort, API & Frontend, UC-1, PHASE_5_BACKLOG additions). Positive operational evidence; no methodology amendment required.

**Methodology lesson recorded (v2-patched → v3):**

The v3 cycle introduces the QB-tier self-audit-checks dimension (§ 12) parallel to the audit-CC prophylactic checks dimension (§ 5). The two dimensions serve different audiences: § 5 governs audit-CC adversarial passes against Phase 1 bible drafts; § 12 governs QB's own meta-cycle authorship discipline. The v3 cycle's audit (post-SP-A2) verifies that the two-dimension framing does not introduce cross-audience confusion (i.e., a Phase 1 audit-CC does not erroneously apply § 12 checks to bible drafts; a QB meta-cycle authoring step does not erroneously apply § 5 checks to its own work).

**Retained from v2-patched unchanged:** §§ 1–3 (with mechanical v6→v9 / v3→v6 anchor updates); §§ 4.1–4.11 (with mechanical anchor updates per Phase 0 cross-reference re-validation; historical citations preserved); §§ 5.1–5.7; § 6 (Phase 1 Audit-CC Prompt Template, with v6→v9 / v3→v6 anchor updates within the prompt body, and Prophylactic Checks 8–9 added per § 5.8–5.9 inclusion); § 7 (Cross-Document Consistency Audit Prompt Template, with anchor updates and Prophylactic Checks 8–9 inclusion); §§ 8.1–8.3 (preserved verbatim with v3 cycle disposition annotations: UNAFFECTED for all three); § 11 (CC Drafting Notes; § 11.1 with mechanical anchor updates per Phase 0 cross-reference re-validation; § 11.2.1 historical v1-era surfacing notes preserved verbatim per § 4.17 locked-content preservation discipline).

**Lock-cycle execution 2026-05-08:** full four-tier ceremony completed. Drafting CC tier: single-pass authorship with two SP-A1 / SP-A1.5 halts on substrate-vs-inheritance divergences (cohort handoff § 4.13 claim refuted by substrate-verified § 4.11 high-water mark; inferred-terminal-§5-structure refuted by substrate-verified §§ 6–11 substantive content). Audit CC tier (SP-A3): 11 findings delivered (2 BLOCKER, 4 MATERIAL, 5 MINOR/STYLE); 6 self-applying-discipline failures surfaced (v3 codified disciplines violated by v3 authorship in real time). Patch CC tier (SP-A4): 10 surgical patches + 1 wontfix-with-parenthetical applied; zero halt-and-surface events; zero conditional escalations. Lock-CC tier (SP-A5): metadata bundle finalization + canonical file replacement per R5 deferred ratification; v3-draft → AUDIT_METHODOLOGY.md per substrate version-in-header convention. Cycle outcome operationally validates Q1 four-tier ceremony cost for methodology-promotion cycles.

---

## 11. CC Drafting Notes (Self-Check Surfaces)

Per the methodology-interpolation rule, CC reviewed every new construct introduced in v1 against the rule. Items below are surfaced for Tony's awareness; CC's judgment on each is included.

### 11.1 Constructs explicitly authorized by META_PLAN v9 / BIBLE_STRUCTURE_SPEC v6 / Tony's locked drafting spec

- Tier 3 designation per META_PLAN v9 § 4.1.
- The seven methodology lessons in § 4 (each individually authorized by Tony's locked methodology lesson catalog in the drafting spec).
- The four required structural elements per lesson (rule + worked example + cross-references + prophylactic check template) — per Tony's locked drafting requirements.
- The order of the seven lessons (introduced empirically across cycles) — per Tony's locked language: "The order reflects the empirical sequence of their introduction across cycles; preserving the order documents the discipline's evolution."
- The audit-CC prompt template in § 6 extending META_PLAN v9 Appendix A.6.
- The cross-document audit prompt template in § 7 extending § 6 with three cross-document questions per META_PLAN v9 § 3.3.
- All threshold language inherited verbatim from META_PLAN v9 § 11.
- All edge cases inherited verbatim from META_PLAN v9 § 3.1.
- All workflow steps inherited from META_PLAN v9 § 3.1 + BIBLE_STRUCTURE_SPEC v6 § 8.3.

### 11.2 v1 / v2 surfacing notes

**Items resolved by Tony's v1 cycle decisions:** all five v1-surfaced constructs (§ 3.2 Q7/Q8 narrowing; § 6 customization slot examples; § 5 consolidated checks; § 7 cross-cutting consistency enumeration; § 4.7 mechanical grep instruction) RATIFIED per Tony's v1 cycle responses. The § 6 customization slot ratification carried a refinement framing requirement, integrated into v2 per Finding 3.

**v2 delta from v1:** v2 patches address v1 audit's 2 MATERIALs and 2 tightly-coupled MINORs per Tony's Q1 Option B + Q2a Option (a) + Q2b ratifications. v2 introduces no new methodology constructs beyond the v1 baseline. The v1 audit-CC's Finding 1 catch on the recursive verification-log-precision lapse is a methodology lesson (banked in § 10 v1 → v2 changelog): codifying the methodology rules in AUDIT_METHODOLOGY's own content requires recursive application of those rules to the codifying document.

**v2 surfacing (new content):**

The verbatim-from-source replacement in § 4.6 invocation 1 inserts substantial verbatim text from META_PLAN_v2_audit.md (line 47 + lines 237-241). This is content extracted from a Phase 0 audit document (already-locked source), not new methodology. Pattern-completion check: not introducing methodology; pedagogically demonstrating the operator-verified-source pattern's compliance. **Judged acceptable.**

The § 6 customization slot refinement framing inserts Tony's verbatim Q3 ratification language as the slot's preamble. Pattern-completion check: not new methodology; integrating Tony's already-ratified instruction into the document. **Authorized by Tony's v1 cycle Q3.**

CC reviewed every new methodology construct introduced in v2 against the methodology-interpolation rule and the pattern-completion check. **Net new methodology constructs in v2: zero.** All v2 changes are surgical patches per audit-CC's Finding 1, 3, 5, 6 recommendations + Tony's three locked decisions.

### 11.2.1 v1 surfacing notes (preserved from v1 for reference)

CC reviewed every new methodology construct introduced in v1 against the methodology-interpolation rule and the pattern-completion check.

1. **§ 3.2 cross-document audit's three additional questions framed as "Phase 1 cross-document scope" for Q7 and Q8.**
   - Tony's locked Q1 specified the cross-document audit covers META_PLAN v6 § 3.3's three questions. v6 § 3.3 frames those three questions in Phase-2 language ("the bible" treated as the locked corpus). For Phase 1 cross-document audit (which runs after individual Phase 1 bibles lock but before Phase 2 adversarial bible audit per v6 § 3.3's separate scope), CC scoped Q7 and Q8 to **internal cross-document consistency** rather than full code-vs-bible reconciliation.
   - Pattern-completion check: this is a scope-narrowing of inherited content (to fit the Phase 1 cycle's distinct purpose), not invention of new methodology. The narrowing is consistent with META_PLAN v6 § 3.3's own positioning of the cross-document audit at the end of Phase 1 (before Phase 2's full adversarial scope). 
   - **Surfaced for Tony's confirmation.** The narrowing may benefit from explicit Tony ratification; alternatively, Tony may direct that Phase 1 cross-document audit run the full v6 § 3.3 scope (in which case Q7 and Q8's framing should not narrow).

2. **§ 6 template's `[ADDITIONAL DOCUMENT-TYPE-SPECIFIC CHECKS]` slot with illustrative examples per bible.**
   - Tony's locked drafting spec required "Phase 1 audit-CC prompt template" as a paste-ready structure. Per-bible specifics necessarily vary; CC provided a customization slot rather than seven separate templates. The illustrative examples (Architecture Overview INDEX check; 14 tables for Database & Schema; etc.) are drawn from BIBLE_STRUCTURE_SPEC v3 § 6.1-§ 6.7's anchor verifications and stated purposes; they are not new methodology constructs.
   - Pattern-completion check: not introducing new methodology; surfacing existing per-bible verification anchors as customization examples.
   - **Judged acceptable.** The customization granularity question is surfaced as Open Question 8.1.

3. **§ 5 "consolidated prophylactic check templates."**
   - The drafting spec required "Audit-CC prophylactic check templates derived from each lesson" and "Phase 1 audit-CC prompt template incorporating all seven prophylactic checks." CC consolidated the check templates from § 4 into § 5 to support paste-ready integration into § 6 / § 7.
   - Pattern-completion check: § 5 is a re-presentation of § 4's already-Tony-authorized prophylactic checks. No new content introduced.
   - **Judged acceptable.**

4. **§ 7 cross-cutting consistency enumeration list.**
   - The drafting spec required "Cross-document consistency audit prompt template, addressing the three cross-document questions specifically." CC provided a "CROSS-CUTTING CONSISTENCY ENUMERATION" subsection listing specific items to verify (Bug #28 canonical home, Bug #15 canonical home, model registry decomposition consistency, etc.). Each item is drawn from META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 explicit content (cross-cutting bug rule per v6 § 7.4, canonical TOC mandate per v3 § 5.2, anchor verifications per v3 § 6.X).
   - Pattern-completion check: not introducing new methodology; surfacing existing cross-cutting concerns as enumerated audit targets.
   - **Judged acceptable.**

5. **§ 4.7 TOC contradiction check's mechanical grep instruction (specifically: `^### 5.* Discipline rules`, `^### 6.* Currently Open`, `^### 7.* Deprecated`, `^### 8.* What Was Fixed`).**
   - The grep pattern is a CC-authored instruction for how to mechanically execute the check. The grep itself is a verification mechanic (executable, falsifiable), not a methodology construct.
   - Pattern-completion check: not introducing new methodology; specifying the mechanical check form for the audit-CC.
   - **Judged acceptable.** Surfaced for awareness; if Tony wants the audit-CC to use a different verification mechanic (e.g., reading TOCs rather than grepping), the instruction should be revised.

### 11.3 Constructs explicitly NOT drafted (to avoid interpolation)

CC did not draft any of the following — each would have been pattern-completion or methodology-interpolation:

- **Iteration cap on Phase 1 audit cycles** — would be a numerical threshold not in source; deferred per META_PLAN v9's pattern.
- **Cadence specification for cross-document audit re-trigger after per-bible revision** — surfaced as Open Question 8.2 instead of drafting a cadence rule.
- **Severity thresholds beyond META_PLAN v9's < 5 MATERIAL** — not introduced; thresholds inherited verbatim from § 11.
- **Completeness criteria for prophylactic check application** — would be a binary pass/fail rule; deferred to Tony's existing < 5 MATERIAL threshold and methodology-interpolation rule's lock-blocker classification.
- **Scoring rubric for audit findings** — not introduced.
- **Percentage criterion for cross-document consistency** (e.g., "≥ 90% of cross-references must resolve") — not introduced; resolution-failure is treated qualitatively per the seven prophylactic checks.
- **Procedural sequencing rules beyond what META_PLAN v9 § 3.1 + BIBLE_STRUCTURE_SPEC v6 § 8.3 already specify** — not introduced.
- **Tiebreaker criteria for canonical-home determination in cross-cutting bugs** — explicitly deferred to Tony per BIBLE_STRUCTURE_SPEC v6 § 5.3's locked deferral.
- **New letter-prefix conventions** — not introduced (W.N remains the only ratified prefix per BIBLE_STRUCTURE_SPEC v6 § 5.5).
- **Worked examples beyond those drawn from Phase 0 cycle audit findings** — every worked example in § 4 references a specific cycle and specific finding; no hypothetical or invented examples.

The methodology-interpolation rule is operative; the discipline of self-surfacing remains. v1 surfaces what's new.

---

## 12. QB Self-Audit Checks (NEW at v3)

This section codifies QB-tier self-audit checks for QB's own meta-cycle authorship discipline. The checks operate at the QB orchestration tier — distinct from § 5's audit-CC prophylactic checks, which operate at the audit-CC adversarial-pass tier against Phase 1 bible drafts.

The audience separation is structural: § 5 governs audit-CC sessions auditing Phase 1 bible drafts; § 12 governs QB's own meta-cycle authorship of paste-prompts, transition messages, drafting specs, and meta-document references. A Phase 1 audit-CC does not apply § 12 checks to a bible draft (those checks target QB-authored artifacts); a QB meta-cycle authoring step does not apply § 5 checks to its own work (those checks target audit-CC's adversarial scope against bible drafts).

The five checks below were banked across cycle-originated Self-Audit Check findings during the AUDIT_METHODOLOGY meta-cycle dispatch sequence (2026-05-08). Each check follows the abstract-rule + worked-example + cross-references structure parallel to § 4 lessons; the prophylactic-check-template element is replaced with QB-tier self-application criteria.

### 12.1 QB Self-Audit Check — Estimation calibration

*Banked: cycle-originated Self-Audit Check finding, 2026-05-08*

#### Abstract rule

QB's pre-authorship size estimates for cycle artifacts (drafting spec size, paste-prompt size, audit report size, etc.) carry ±15-20% confidence interval at this cycle's domain complexity. The interval is post-calibration — refined from the original ±40% confidence interval observed across earlier cycles. Estimates outside this confidence interval signal either (a) cycle scope drift (the actual scope diverged from the estimate's premise) or (b) estimation method gap (the estimation heuristic does not capture the scope's actual complexity).

The check is QB-tier self-application: when QB authors a size estimate (chat output, paste-prompt size annotation, capacity-planning estimate), QB carries the ±15-20% confidence interval explicitly in the estimate language. Estimates without confidence intervals are flagged for QB self-correction.

The check is operational, not methodology-prescriptive: it informs QB's planning of paste cycles and capacity expectations; it does not constrain content scoping decisions.

#### Worked example

The check's calibration emerged from the API & Frontend Bible drafting spec cycle. QB's pre-authorship size estimate was 22 KB; the actual drafting spec landed at 29,991 bytes (~36% over estimate). The post-calibration confidence interval (±15-20%) reflects subsequent observations across the cycle's downstream paste-prompt sizes, where ±15-20% became the operational range.

The check is forward-looking: future QB size estimates carry the ±15-20% interval. Future cycles' actual sizes inform whether the calibration holds or requires re-tuning.

#### Cross-references

- **Origin:** API & Frontend Bible cycle, 2026-05-08; pre-authorship size estimate divergence.
- **Related cycle:** AUDIT_METHODOLOGY meta-cycle (2026-05-08); estimation surfacing.

#### QB self-application criteria

When QB authors a pre-authorship size estimate (paste-prompt size, drafting spec size, audit report expected size, capacity-planning estimate):

1. **Carry the ±15-20% confidence interval explicitly in the estimate.** Format: "estimated 22 KB ± 15-20%" or "estimated range 18-26 KB".
2. **Flag the estimate's confidence-interval source** (post-calibration estimate or fresh estimate-without-prior-data).
3. **For estimates outside ±15-20% post-cycle** (i.e., actual size diverges from estimate by >20%), surface the divergence in the cycle's changelog or self-check surfacing block. Categorize: scope drift (cycle scope diverged from premise) vs estimation method gap (heuristic insufficient).

The check is informational, not lock-blocking. It informs operator capacity-planning trust in QB estimates over time.

### 12.2 QB Self-Audit Check — Self-describing authorization redundancy detection

*Banked: cycle-originated Self-Audit Check finding, 2026-05-08*

#### Abstract rule

When QB authors a self-describing § X authorization clause inside a meta document (e.g., a drafting spec's § 15 "Authorization Clause" naming the document's own authorization scope), QB checks whether the wrapper paste-prompt at Step N+1 (the paste-prompt that pastes the meta document forward) is rendered redundant by the self-describing § X. If redundant, QB explicitly flags the redundancy in the same chat turn as the authorization clause authorship.

The check protects against the failure mode where a self-describing authorization clause inside a meta document and a wrapper paste-prompt's authorization framing both name the same scope, producing duplicate (or contradictory) authorization framings. The wrapper paste-prompt's value is in providing authorization framing; if the meta document's § X already provides equivalent framing, the wrapper paste-prompt is not adding value.

The check applies at QB's authoring time, not at audit time — the redundancy is QB's surface to flag at meta-document authorship; downstream audit-CC's adversarial scope catches surviving redundancies but the prevention is QB-tier.

#### Worked example

The check's catch emerged from the API & Frontend Bible cycle. QB authored a self-describing § 15 authorization clause inside the drafting spec; the Step 5 wrapper paste-prompt that paste-routed the spec to drafting CC was rendered redundant by § 15's self-authorization framing. Tony's bypass of Step 5 (direct paste using § 15's self-authorization) left the cycle's ledger off-by-one. QB-side prevention would have been: at § 15 authorship, QB explicitly flag "Step 5 wrapper paste-prompt rendered redundant by § 15 self-authorization; recommend bundling § 15 authorship with Step 5's bypassing-or-skipping decision in the same chat turn."

#### Cross-references

- **Origin:** API & Frontend Bible cycle, 2026-05-08; Step 5 ledger off-by-one drift.
- **Related lesson:** § 4.20 (Pattern A bundling default + Pattern B exception).

#### QB self-application criteria

When QB authors a self-describing § X authorization clause inside a meta document:

1. **Identify the wrapper paste-prompt at Step N+1 (or analogous downstream paste step).**
2. **Check whether § X's framing renders the wrapper paste-prompt's authorization scope redundant.** "Redundant" means the wrapper's framing duplicates or substantively overlaps with § X's framing.
3. **If redundant, flag the redundancy in the same chat turn as the § X authorship.** Surface to Tony with a recommendation: skip the wrapper paste-prompt; bundle § X authorship with the wrapper's bypass decision (Pattern A); or rewrite the wrapper to add framing § X does not cover.
4. **Surface the flag explicitly** — do not silently rely on operator catching the redundancy.

The check is QB-tier self-flagging discipline. Audit-CC's adversarial scope catches surviving redundancies but prevention is QB's responsibility.

### 12.3 QB Self-Audit Check — Paste-prompt transit-truncation discipline (bookend markers)

*Banked: cycle-originated Self-Audit Check finding, 2026-05-08*

#### Abstract rule

QB paste-prompts >15 KB carry bookend markers `PROMPT BEGINS` (at the start of the paste-prompt) and `PROMPT ENDS` (at the end of the paste-prompt) prophylactically. Receiving CC verifies bookend integrity at receipt — if either marker is absent or content between them appears truncated, receiving CC halts and reports rather than executing on potentially-truncated content.

The discipline protects against the failure mode where a paste-prompt is truncated in transit (chat-rendering, copy-paste, or transmission-layer truncation) and the receiving CC executes on the truncated content without detection. Receiving CC's truncation-detection-at-receipt is the prevention; mid-execution truncation discovery (where CC has already begun work and surfaces the truncation as a halt) is the failure mode the prevention avoids.

The 15 KB threshold is operational (paste-prompts under 15 KB are observably less prone to transit truncation in this cycle's transmission context). The threshold is not methodology-prescriptive; it is QB-tier self-application criterion.

For paste-prompts >15 KB with embedded content blocks (e.g., a SPEC-FILE-CONTENT-BEGINS / SPEC-FILE-CONTENT-ENDS block within a wrapper paste-prompt), the inner content blocks carry their own bookend markers; the outer wrapper carries `PROMPT BEGINS` / `PROMPT ENDS` at the wrapper's outermost boundaries.

#### Worked example

The check emerged from the API & Frontend Bible drafting CC dispatch (Step 7 truncation in transit). A ~17 KB paste-prompt was truncated mid-paste; the drafting CC's fragment-detection HALT was correctly applied at receipt rather than mid-authorship. The discipline is banked: bookend markers on paste-prompts >15 KB enable receipt-time truncation detection.

The AUDIT_METHODOLOGY meta-cycle's own paste-prompt sequence applied the discipline (PROMPT BEGINS / PROMPT ENDS bookends + SPEC-FILE-CONTENT-BEGINS / SPEC-FILE-CONTENT-ENDS inner bookends). All paste-prompts in the meta-cycle landed without transit truncation.

#### Cross-references

- **Origin:** API & Frontend Bible drafting CC dispatch, 2026-05-08; Step 7 transit truncation.
- **Operational evidence:** AUDIT_METHODOLOGY meta-cycle paste-prompt sequence (2026-05-08); bookend-marker discipline applied.

#### QB self-application criteria

When QB authors a paste-prompt:

1. **Estimate the paste-prompt size before authorship completes.** If estimated size > 15 KB, plan to include bookend markers.
2. **For paste-prompts > 15 KB, prepend `PROMPT BEGINS — <PASTE-PROMPT-NAME>` at the start and append `PROMPT ENDS — <PASTE-PROMPT-NAME>` at the end.**
3. **For paste-prompts with embedded content blocks (e.g., file-content blocks), wrap the embedded blocks in their own inner bookend markers** (e.g., `SPEC-FILE-CONTENT-BEGINS` / `SPEC-FILE-CONTENT-ENDS`).
4. **Direct the receiving CC to verify bookend integrity at receipt** — if either outer marker is absent or content between them appears truncated, halt and report rather than executing.

The check is operational; the 15 KB threshold informs QB's bookend-application decision but is not lock-blocking.

### 12.4 QB Self-Audit Check — Within-message placeholder discipline

*Banked: cycle-originated Self-Audit Check finding, 2026-05-08*

#### Abstract rule

QB transition messages between gates may contain placeholder syntax templating Tony's ratification values (e.g., `<X / Y>` placeholders awaiting Tony's selection between options). QB completes placeholder interpolation BEFORE rendering the transition message to chat. Rendering a transition message with un-interpolated placeholders to chat creates the failure mode where Tony parses a placeholder as ratifiable content (e.g., interpreting `<X / Y>` as "X" or "Y" based on context), introducing ambiguity at the gate's ratification surface.

Three acceptable resolution patterns:

(a) **Author transition message ONLY after explicit ratification.** QB defers transition-message authorship to the chat turn following Tony's ratification; the message reflects ratified values, not placeholders.

(b) **Author with explicit per-decision branches.** Transition message presents Tony's selection as explicit branches: "If Tony ratifies X: <message variant 1>; if Tony ratifies Y: <message variant 2>". No placeholders; all paths enumerated.

(c) **Author placeholders interpolated to neutral language.** Where neither (a) nor (b) is feasible, QB rewrites the placeholder syntax as neutral prose that does not commit to either option (e.g., "pending Tony's ratification of strategy choice between (a) and (b)" rather than `<a / b>`).

The check applies at QB's chat-rendering moment — the discipline is "no un-interpolated placeholders rendered to chat."

#### Worked example

The check's catch emerged from the API & Frontend Bible cycle's SP-A2 → SP-A3 transition (Observation 4). QB rendered a transition message containing angle-bracket placeholders `<X / Y>` without filled-in ratification value; drafting CC's HALT was correctly applied per Lesson § 4.12 bounded-authorization discipline (the placeholder syntax was not within the drafting CC's authorized substrate to interpolate).

The AUDIT_METHODOLOGY meta-cycle dispatch applied the discipline: transition messages between SP-A1 → resumption + SP-A1.5 → resumption used resolution pattern (a) — QB authored transition only after Tony's explicit ratification, presenting ratified values directly.

#### Cross-references

- **Origin:** API & Frontend Bible cycle, 2026-05-08; SP-A2 → SP-A3 transition Observation 4.
- **Related lesson:** § 4.12 bounded-authorization discipline (drafting CC's HALT-on-out-of-scope-content).

#### QB self-application criteria

When QB authors a transition message between gates:

1. **Identify any placeholder syntax in the draft message** (`<X / Y>`, `<X>`, `[TBD]`, `[pending]`, etc.).
2. **For each placeholder, select resolution pattern (a) / (b) / (c)** before rendering to chat.
3. **Resolution (a):** Defer message authorship to post-ratification turn. Render no message in current turn; render ratified-value message in subsequent turn.
4. **Resolution (b):** Author the message with explicit per-decision branches. Each branch presents the message variant for that ratification path; no placeholders survive.
5. **Resolution (c):** Rewrite placeholder as neutral prose. Render the neutral-prose message; ratification surface is in the prose, not in placeholder syntax.
6. **Halt and re-author** if a placeholder survives to chat-render time. Surface the failure to Tony with self-correction.

The check is QB-tier discipline; failures surface to Tony as transition-message ambiguity findings.

### 12.5 QB Self-Audit Check — Meta-document state claim substrate verification (with Awareness item B scope clause integrated verbatim)

*Banked: cycle-originated Self-Audit Check finding, 2026-05-08*

#### Abstract rule

Meta-document state claims must be substrate-verified at first cycle reference, not inherited as authoritative across cycles. Inherited unverified state claims accumulate into fabricated-by-accumulation substrate that surfaces only when a downstream cycle attempts to interact with the meta-document directly.

**Generalization scope: applies to ALL meta-document inheritance, not just PHASE_5_BACKLOG.md.** Inherited unverified state claims from prior cycles accumulate into fabricated-by-accumulation substrate regardless of meta-document type. First cycle reference of a meta-document state claim requires substrate verification; subsequent same-cycle references may rely on the verified state.

The check is QB-tier self-application: when QB authors a paste-prompt, drafting spec, or chat-output content that references a meta-document's state (count, path, version, content), QB substrate-verifies the state at first cycle reference. Inheritance from a prior cycle's authority is not substrate verification; the prior cycle's authority is itself a meta-document state claim subject to verification.

The check protects against the fabricated-by-accumulation failure mode: a meta-document state claim authored at cycle N (e.g., "the backlog has 26 entries at path X") is treated as authoritative at cycle N+1 without re-verification; cycle N+2 carries forward the inherited claim; by cycle N+M the inherited claim has been re-cited multiple times without substrate verification, and any drift between the original state and current state is invisible until a cycle directly interacts with the meta-document. The accumulation produces fabricated substrate (the claim is no longer verified by current state) without any single cycle being responsible for fabrication.

#### Worked example

The check's catch emerged across multiple cycles surfacing during PHASE_5_BACKLOG.md additions cycle dispatch. Three inherited claims were tested at substrate verification: 2 failed (path drift over 8+ paste-prompts; reconciliation-status drift cited as "complete" when actually deferred); 1 survived (entry count). The substrate verification was the prevention; without it, the failed claims would have continued propagating until a cycle attempted direct interaction.

The check applies to ALL meta-document state claims, not just PHASE_5_BACKLOG.md state claims. The generalization is operative across:

- File paths (inherited path claims may have drifted; substrate verify at first reference).
- Version state (inherited version claims may have drifted; substrate verify).
- Content count (inherited count claims may have drifted; substrate verify).
- Reconciliation status (inherited reconciliation claims may have drifted; substrate verify).
- Lock state (inherited lock-state claims may have drifted; substrate verify).
- Cross-reference targets (inherited cross-reference claims may have drifted; substrate verify).

#### Cross-references

- **Origin:** PHASE_5_BACKLOG.md additions cycle dispatch, 2026-05-08; path drift + reconciliation-status drift surfaced at first substrate verification.
- **Awareness item B (verbatim scope clause):** integrated above ("Generalization scope: applies to ALL meta-document inheritance, not just PHASE_5_BACKLOG.md. Inherited unverified state claims from prior cycles accumulate into fabricated-by-accumulation substrate regardless of meta-document type. First cycle reference of a meta-document state claim requires substrate verification; subsequent same-cycle references may rely on the verified state.").
- **Related lesson:** § 4.12 (Low-cost substrate verification at row-authorship — parallel discipline at CC tier).

#### QB self-application criteria

When QB authors a paste-prompt, drafting spec, or chat-output content that references a meta-document's state:

1. **Identify each meta-document state claim in the content.** State claims include path, version, content count, reconciliation status, lock state, cross-reference targets.
2. **For each state claim, identify whether it is a first cycle reference or a subsequent reference.** "First cycle reference" means QB has not substrate-verified the claim within the current cycle.
3. **For first cycle references, substrate-verify the claim.** Read the meta-document; verify the claim against current state; cite the verification in the content (e.g., "substrate-verified at YYYY-MM-DD HH:MM").
4. **For subsequent same-cycle references, rely on the verified state** (no need to re-verify within the same cycle).
5. **Flag any state claim that surfaces a substrate gap** (current state diverges from inherited claim). Surface the gap to Tony as a meta-document drift finding; do not silently propagate the inherited (now-divergent) claim.

The check is QB-tier discipline; failures surface as meta-document drift findings at the cycle's relevant gate.

---

**End-of-document footer:**

**Lock state confirmation:** LOCKED v3 confirmed 2026-05-08.

**Authorship CC tier:** drafting CC (this cycle, 2026-05-08); single-pass authorship to SP-A2 with two prior halts at SP-A1 (substrate verification report) + SP-A1.5 (renumbering check halt) ratified by Tony before resumption.
**Audit CC tier:** completed SP-A3 2026-05-08; 11 findings delivered (2 BLOCKER, 4 MATERIAL, 5 MINOR/STYLE); 6 self-applying-discipline failures surfaced (v3 codified disciplines violated by v3 authorship in real time); patch CC tier dispatched to address all findings.
**Patch CC tier:** completed SP-A4 2026-05-08; 10 surgical patches + 1 wontfix-with-parenthetical applied; file delta +1,162 bytes / −5 lines; zero halt-and-surface events; zero conditional escalations.
**Lock CC tier:** executed SP-A5 2026-05-08; canonical file replacement per L3 Option (a); v3-draft → AUDIT_METHODOLOGY.md per substrate version-in-header convention; L3.a defensive substrate check passed pre-overwrite (v2-patched canonical state confirmed not drifted); three-element metadata bundle finalized.
**Ratification owner:** Tony.

**Three-element metadata bundle (per § 4.16, § 4.18, and inaugural application to AUDIT_METHODOLOGY itself per spec § 8):**
- Element 1 (Header status field): top of document — Status (LOCKED v3), Authorship date (2026-05-08), Locked date (2026-05-08), Owner ratification (Tony), Tier (3), Anchored on (META_PLAN v9 + BIBLE_STRUCTURE_SPEC v6 LOCKED 2026-05-05).
- Element 2 (Revision history block): top of document (header revision-history list) + § 10 Changelog (v1 → v2 → v2-patched → v3 chronological-forward, with v3 entry extended through lock-cycle execution paragraph) per R8.b ratification.
- Element 3 (End-of-document footer): this footer block, all four CC tier fields populated with completion records.

**Operational precedent banking (v3 authorship, 2026-05-08):** Lesson § 4.12 bounded-authorization discipline confirmed operating cleanly at drafting CC + audit CC + patch CC tiers across six post-Phase-0 cycle classes (Database & Schema, Data Pipeline, parallel cohort, API & Frontend, UC-1, PHASE_5_BACKLOG additions). Positive operational evidence; no methodology amendment required.

**Four-tier ceremony precedent banking (v3 lock-cycle, 2026-05-08):** Q1's four-tier ceremony (drafting CC + audit CC + patch CC + lock-CC as four distinct sessions) operationally validated for methodology-promotion cycles. Self-Audit Check 14 generalization (§ 12.5) applied across all four tiers without authorization-boundary crossing. Cycle banking: four-tier discipline pays its cost at methodology-promotion scope; surgical-row patch (UC-1 class) cycles continue to use lighter QB-audit synthesis tier per § 4.21 (UC-cycle audit-scope methodology lesson).

End of AUDIT_METHODOLOGY.md v3 (LOCKED 2026-05-08).
