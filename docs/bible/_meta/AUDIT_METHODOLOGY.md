# AUDIT_METHODOLOGY.md

**Document:** AUDIT_METHODOLOGY
**Phase:** 0 (Methodology) — Phase 0 deliverable 3 of 5
**Status:** DRAFT v2 (pre-audit)
**Author:** CC (drafting under verification discipline; QB orchestrated and reviewed)
**Date:** 2026-05-04
**Locked:** [pending audit + Tony review + iteration cycles]

**Revision history:**
- v1 (2026-05-04): initial CC draft. Companion verification log at `_audits/AUDIT_METHODOLOGY_v1_verification.md`.
- v2 (2026-05-04): post-v1-audit surgical patch pass integrating Tony's three locked decisions (Q1: Option B addressing MATERIALs + tightly coupled MINORs; Q2a: Option (a) verbatim from source for § 4.6 quote attributions; Q2b: verification log delta with Claim 42 confirming verbatim accuracy). Companion verification log at `_audits/AUDIT_METHODOLOGY_v2_verification.md` inherits v1's 41 claims with re-verified-2026-05-04 timestamps and adds 1 new claim (Claim 42 — verbatim attribution of v2 audit Q2.2 + Tony's Q4 in § 4.6).

**Tier:** 3 per META_PLAN v6 § 4.1 + § 6.5. CC-drafted under QB spec; companion verification log required; CC-audited.

**Anchored on:** META_PLAN v6 (locked 2026-05-04) and BIBLE_STRUCTURE_SPEC v3 (locked 2026-05-04). Section references throughout this document point to v6 / v3 § numbers.

**Methodology-interpolation rule (operative per META_PLAN v6 § 6.1, with v6's expanded scope and grandfathering clause; pattern-completion check operative per BIBLE_STRUCTURE_SPEC v1 audit lesson):** This draft does not invent binary tests, cadence rules, completeness criteria, scoring rubrics, severity thresholds, iteration caps, percentage criteria, procedural sequencing rules, or other CC-prescribed methodology constructs Tony has not explicitly ratified. Pattern-completion interpolation check operative; v1 surfacing notes in § 11.

---

## 1. Motivation

### 1.1 Why this document exists

AUDIT_METHODOLOGY.md is the third Phase 0 methodology deliverable. Its job is to give Phase 1 audit-CCs the prophylactic checks empirically learned across nine Phase 0 audit cycles (META_PLAN v1→v6, six cycles; BIBLE_STRUCTURE_SPEC v1→v3, three cycles), plus the Phase 1-specific cycle workflow that takes a CC-drafted Phase 1 bible from initial draft to lock.

Phase 0's audit cycle pattern emerged organically across those nine cycles: the v3 BLOCKER taught the verification-log-precision rule; the v3 / v4 / v5 / v6 cycles taught the methodology-interpolation rule with progressive scope expansion and grandfathering; the BIBLE_STRUCTURE_SPEC v1 / v2 cycles taught the pattern-completion check and the TOC contradiction class. AUDIT_METHODOLOGY codifies these lessons so that fresh Phase 1 audit-CCs apply them from cycle 1 rather than re-discovering them across multiple cycles.

The document is load-bearing for Phase 1 in the same way that META_PLAN v6 is load-bearing for Phase 0: a Phase 1 audit-CC handed only the six adversarial questions (META_PLAN v6 § 6.2) without the prophylactic checks below would re-introduce class-of-failure patterns Phase 0 already paid for.

### 1.2 Why now

Phase 1 begins after all five Phase 0 documents lock. Phase 1 produces seven bible documents (per BIBLE_STRUCTURE_SPEC v3 § 4.1) under Tier 3 discipline; each goes through its own audit cycle; multiple CC sessions may execute in parallel. AUDIT_METHODOLOGY ensures consistent audit discipline across those parallel cycles.

### 1.3 The Phase 0 audit cycle as worked example

Per Tony's locked Q1 in this document's drafting spec, AUDIT_METHODOLOGY is scoped to Phase 1 audits only. Phase 0 audit cycles have empirically converged across nine cycles; their lessons are codified and internalized. Phase 2-4 audit methodologies operate against different criteria, source material, and convergence definitions; they live where they're operational, defined when those phases begin. If they want to inherit Phase 0's audit cycle pattern, they reference META_PLAN v6 and BIBLE_STRUCTURE_SPEC v3 directly as worked examples.

This document treats Phase 0's nine audit cycles as the empirical substrate from which Phase 1 audit-CC discipline is derived. Worked examples in § 4 reference specific Phase 0 cycle findings; those references serve a pedagogical purpose, not an authority one.

---

## 2. Scope

### 2.1 What this document specifies

- **Phase 1 per-bible audit cycle** — the audit cycle for each individual Phase 1 bible (per META_PLAN v6 § 3.1's locked workflow + BIBLE_STRUCTURE_SPEC v3 § 8.3's per-bible cycle, as applied to Phase 1 documents).
- **Phase 1 cross-document consistency audit** — the audit per META_PLAN v6 § 3.3 that runs after all individual bibles lock, verifying internal consistency across the corpus.
- **Audit-CC prophylactic check templates** — seven prophylactic checks derived from the empirically grounded Phase 0 lessons, each with abstract rule statement, worked example, cross-references to origin sections, and check template form for paste-ready integration into Phase 1 audit prompts.
- **Phase 1 audit-CC prompt template** — paste-ready structure incorporating all seven prophylactic checks plus the six adversarial questions from META_PLAN v6 § 6.2.
- **Cross-document consistency audit prompt template** — paste-ready structure for the cross-document audit per META_PLAN v6 § 3.3, addressing the three cross-document questions.

### 2.2 What this document does NOT specify

- **Phase 0 audit methodology** — already empirically settled across the nine cycles documented above; not re-codified here.
- **Phase 2 adversarial bible audit methodology** — Phase 2 operates against the locked corpus (not against drafts), with different criteria (does the bible match the code?). Phase 2 methodology is deferred to Phase 2 entry. If Phase 2 wants to inherit Phase 0's audit cycle pattern, it references this document and META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 directly.
- **Phase 3 predictive concept inventory audit methodology** — deferred to Phase 3 entry.
- **Phase 4 gap analysis audit methodology** — deferred to Phase 4 entry.
- **What bible content goes where** — that's BIBLE_STRUCTURE_SPEC v3.
- **What success looks like for each phase** — that's CONVERGENCE_CRITERIA.md (Phase 0 deliverable 4).
- **Format for findings discovered during audit** — that's TRIAGE_QUEUE_SPEC.md (Phase 0 deliverable 5).
- **New methodology constructs not present in META_PLAN v6 or BIBLE_STRUCTURE_SPEC v3** — per the methodology-interpolation rule (§ 4.2 below), this document codifies methodology already locked in those documents; it does not extend or generalize them.

### 2.3 Authority chain

Per META_PLAN v6 § 4.1, AUDIT_METHODOLOGY is Tier 3; CC drafts under QB spec with companion verification log; audit-CC verifies. Per Tony's locked Q1 in this document's drafting spec, scope is Phase 1 audits only — both per-bible and cross-document. Per Tony's locked Q2, each methodology lesson is presented with an abstract rule statement, at least one worked example from Phase 0 cycles, cross-references to origin sections, and an audit-CC prophylactic check template.

---

## 3. Phase 1 Audit Cycle Workflow

### 3.1 Per-bible audit cycle

The per-bible audit cycle for each of the seven Phase 1 bibles (per BIBLE_STRUCTURE_SPEC v3 § 4.1) follows META_PLAN v6 § 3.1's locked Phase 0 per-deliverable cycle, with the per-document drafting authority determined per META_PLAN v6 § 6.5 (all Phase 1 bibles are Tier 3 per § 4.1 + § 6.5). BIBLE_STRUCTURE_SPEC v3 § 8.3 restates the cycle for Phase 1; the steps below cite both authorities.

**Steps (per META_PLAN v6 § 3.1 + BIBLE_STRUCTURE_SPEC v3 § 8.3):**

1. QB writes Phase 1 spec (target questions, format, depth bar, source-priority rules per META_PLAN v6 § 4.5, output location, explicit verification discipline including the methodology-interpolation rule per META_PLAN v6 § 6.1 and the verification-log precision rule per META_PLAN v6 § 6.5).
2. CC drafts the bible AND produces the companion verification log. Every factual claim about EE has a verification entry. **Per META_PLAN v6 § 6.5 hard rule, Tier 3 drafts that omit a companion verification log are rejected by QB without audit; the verification log is not optional.**
3. QB reads draft fully (synthesizing). QB skims verification log to spot-check entries.
4. QB writes audit-CC prompt incorporating: the six adversarial questions per META_PLAN v6 § 6.2, the prophylactic checks per § 5 of this document, the verification-against-live-system mandate, and the regression check for prior-cycle findings if vN ≥ 2.
5. QB runs audit-CC fresh.
6. Audit findings return; QB synthesizes.
7. If routine: QB re-specs/re-drafts, re-runs, repeats steps 3-6.
8. If architectural: QB surfaces to Tony with proposed resolutions and tradeoffs; Tony decides.
9. Repeat until audit clean per § 3.5's threshold.
10. Bible locks.

**Edge cases inherited from META_PLAN v6 § 3.1 (each operative for Phase 1 audits):**

- **CC↔audit-CC disagreement.** Default: audit-CC wins. If QB judges the audit-CC finding itself questionable, QB may run a third fresh CC session to adjudicate (last resort).
- **Audit-CC error.** Audit-CCs can be wrong. When verification contradicts an audit-CC finding, QB surfaces both: the original audit finding AND the contrary verification, and Tony decides whether the audit-CC needs the methodology refined or whether the draft missed something.
- **Tony's locked decision based on a wrong premise.** When verification surfaces that a Tony-locked decision was based on a premise that turns out to be false, CC does NOT silently revise — CC surfaces the contradiction to QB → Tony with the verified facts. Tony ratifies the reframing or holds the original. (Pattern invoked twice in Phase 0 cycles; codified as Lesson 6 in § 4.6.)
- **CC methodology-interpolation pattern.** CC has a recurring failure mode of extending Tony's locked answers with adjacent policy CC believes follows from the answer. The methodology-interpolation rule (§ 4.2) governs.
- **Post-lock revision.** If a Phase 1 bible locks, then weeks later a finding contradicts locked content, the procedure per META_PLAN v6 § 3.1 applies: QB surfaces to Tony; default is revise the locked document and trigger re-audit + dependent-document re-validation.
- **Audit findings with downstream consequences.** When audit-CC surfaces a fact that contradicts not just the audited document but the upstream substrate, the procedure is: revise the audited document to use the verified fact, flag the substrate inaccuracy for downstream correction, note the discrepancy in the document's revision history.

**Phase 1 drafting order (recommended per BIBLE_STRUCTURE_SPEC v3 § 8.2):** Architecture Overview first; Database & Schema second; Data Pipeline third; the three ML bibles in parallel; API & Frontend last. Recommended, not mandatory.

### 3.2 Cross-document consistency audit

After all seven Phase 1 bibles lock individually, a cross-document consistency audit runs per META_PLAN v6 § 3.3. The cross-document audit is governed by three additional questions appended to the six adversarial questions of META_PLAN v6 § 6.2:

1. Does the bible say something the code does not do?
2. Does the code do something the bible does not say?
3. Where do bible documents contradict each other across files?

Note: questions 1 and 2 are framed at META_PLAN v6 § 3.3 in Phase-2 language ("the bible" treated as the locked corpus); for Phase 1's cross-document audit (which runs after individual Phase 1 bibles lock but before the Phase 2 adversarial bible audit per META_PLAN v6 § 3.3's separate scope), these three questions are scoped to **internal cross-document consistency** rather than full code-vs-bible reconciliation. Code-vs-bible reconciliation at full Phase 2 scope is deferred to Phase 2.

**Cross-document audit deliverable structure (per META_PLAN v6 § 3.3):**

- One cross-document audit report at `/docs/bible/_audit/cross_document_audit.md`.
- Per-bible audit reports already exist at `/docs/bible/_audit/<bible_doc_name>_audit.md` from individual cycles.
- The cross-document audit reads all per-document audit reports as input; it is a separate fresh CC session.

**Cross-document audit threshold:** the same threshold as per-bible audits (§ 3.5 below). Findings that surface cross-document contradictions are MATERIAL by their nature when they require a bible to revise; MINOR when they're style or convention drift.

**Per-bible re-revision trigger:** per META_PLAN v6 § 3.3, "if a per-document audit returns >5 MATERIAL findings, that document goes back to Phase 1 revision before the cross-document audit runs." Cross-document audit does not run until all individual bibles meet Tony's threshold.

### 3.3 Audit-CC paste-ready prompt structure

Audit prompts must be paste-ready per META_PLAN v6 § 8.4. The Phase 1 audit-CC prompt template is in § 6 below; the cross-document audit-CC prompt template is in § 7. Both extend META_PLAN v6 Appendix A.6's working example.

Each prompt's structure (standardized per META_PLAN v6 § 8.4):

- Project context (what EE is, what this document is, where it sits in the phase sequence)
- The roles in this project (Tony, QB, CC)
- The audit workflow (every Phase 1 deliverable goes through adversarial CC audit before Tony reviews)
- Reference materials (DD bible, EE current state dump, live AWS, live API endpoints, EE codebase)
- Verification discipline (HARD RULE: live state preferred over dump; precision rule applied broadly; no fabrication)
- The draft (path on disk or inline)
- Companion verification log (if Tier 3; instruction to spot-check)
- Adversarial task: six adversarial questions per META_PLAN v6 § 6.2 plus document-type-specific adversarial checks
- Prophylactic checks per § 5 of this document
- Regression check (for vN ≥ 2)
- Output format (standardized findings structure)
- Severity assessment (BLOCKER / MATERIAL / MINOR / STYLE)
- Threshold context (per § 3.5)
- Recommendation form (lock as-is / lock after specific minor revisions / revise and re-audit / substantial rework)

### 3.4 Verification log requirements for Phase 1 bibles

Every Phase 1 bible draft is Tier 3 per BIBLE_STRUCTURE_SPEC v3 § 4.1; therefore every Phase 1 bible draft has a companion verification log per META_PLAN v6 § 6.5. The verification log:

- Lives at `/docs/bible/_audit/<bible_doc_name>_v<N>_verification.md` per BIBLE_STRUCTURE_SPEC v3 § 5.1's front matter pattern.
- Has one entry per concrete factual claim about EE.
- Distinguishes inherited claims (already verified in META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 verification logs) from new claims (introduced by this Phase 1 bible).
- Applies the verification-log precision rule per META_PLAN v6 § 6.5 (counts decomposed; definitions vs uses vs imports distinguished; aggregable counts explicitly aggregated). The full lesson is captured as Lesson 1 in § 4.1 below.
- Includes operator-verified external source quotes verbatim where applicable per META_PLAN v6 verification log Claim 15c pattern. The full lesson is captured as Lesson 4 in § 4.4 below.

The audit-CC reads both the draft and the verification log; verifies a sample of verification claims against live state; reports any verification-log entries that don't hold up.

### 3.5 Tony's threshold for lock per audit cycle

A Phase 1 bible locks when its audit returns:

- **< 5 MATERIAL findings** AND
- **zero fabricated-content findings** AND
- **zero methodology-interpolation findings (post-grandfathering)**

This threshold is inherited verbatim from META_PLAN v6 § 11 (Lock Status), where it has been operative across nine Phase 0 audit cycles. Per Tony's hard rule (per META_PLAN v6 § 6.1 + audit history): methodology-interpolation findings fail the lock regardless of count.

**MATERIAL/MINOR distinction (per META_PLAN v6 Appendix A.6):** "A 'missing example' is probably MINOR. A 'the maintenance protocol has an enforcement gap' is probably MATERIAL. A 'CC-interpolated binary test that Tony hasn't ratified' is MATERIAL by its nature per the methodology-interpolation rule."

**Audit-CC must apply the distinction honestly.** Per META_PLAN v6 Appendix A.6: "Tony has explicitly cautioned against threshold-gaming. The operator values surfacing problems over reassurance." If an audit-CC finds few flaws, the bar is wrong — re-read more skeptically.

**No new flagging thresholds are introduced by this document.** Each prophylactic check below states what to look for, how to recognize the pattern, and how to flag — but the threshold for flagging is delegated to Tony's existing < 5 MATERIAL threshold or to the methodology-interpolation rule's lock-blocker classification.

---

## 4. Methodology Lessons Catalog

The seven lessons below appear in the empirical sequence of their introduction across Phase 0 cycles. Order is preserved to document the discipline's evolution. Each lesson has the same four required structural elements (per Tony's locked drafting requirements): abstract rule statement, worked example from Phase 0 cycles, cross-references to origin META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 sections, and an audit-CC prophylactic check template.

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

The v5 cycle locked broad-sweep scope (per Tony's locked decision in v5 cycle): the rule applies broadly. v5 applied it to working-tree status counts (74 untracked + 29 modified = 103 per META_PLAN v6 verification log Claim 22), model registry counts (88 = 45 active + 43 inactive per Claim 7), EventBridge rules (13 = 10 ENABLED + 3 DISABLED), and Lambda counts (8 = 5 Active + 3 INACTIVE). The v6 cycle extended to ECS task families enumerated by name (5 named in META_PLAN v6 § 2.3 per Claim 20).

#### Cross-references

- **Rule statement:** META_PLAN v6 § 6.5 ("Verification log precision rule").
- **Decomposition examples in main doc:** META_PLAN v6 § 1.1 (working-tree state), § 1.3 (registry / Lambda / EventBridge), § 2.3 (ECS task families), § 9.13 (registry multi-active-row), Appendix A.4 (legacy `predictions` references).
- **BLOCKER finding:** META_PLAN v3 audit (severity table, F1).
- **Rule introduction:** META_PLAN v4 (per § 6.5's rule body and the v4 changelog).
- **Broad-sweep ratification:** META_PLAN v5 cycle (per Tony's locked decision; v6 § 6.5 carries the locked language).
- **v6 application to enumeration:** META_PLAN v6 § 12 (MINOR #6 — ECS task families fully enumerated).

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

- **Rule statement with named patterns + catch-all:** META_PLAN v6 § 6.1 (CC role definition).
- **Grandfathering clause:** META_PLAN v6 § 6.1 (the "Grandfathering clause" paragraph).
- **v3 catch and resolution:** META_PLAN v3 audit (severity table #3); META_PLAN v4 changelog (drop confirmed in v3 finding regression check).
- **v4 catch and resolution:** META_PLAN v4 audit (Question 1 finding 3 / Question 3 finding 3 / Severity table #5); META_PLAN v5 (replacement with descriptive prose, per v5 changelog).
- **v5 catch and resolution:** META_PLAN v5 audit M-1 finding (Methodology-interpolation rule self-application section); META_PLAN v6 § 12 (M-1 cadence-neutralized).
- **v6 clean lock:** META_PLAN v6 audit (Methodology-interpolation findings: ZERO post-grandfathering).

#### Audit-CC prophylactic check template

For any methodology construct in the audited document, verify it traces back to one of:

1. Tony's locked instructions in a drafting spec for this document, OR
2. META_PLAN v6 or earlier locked Phase 0 documents (with content authored by Tony or by QB and ratified by Tony), OR
3. Operator-stated rationale per source-priority tier 5 (META_PLAN v6 § 4.5).

If the construct does not trace to one of those three, flag as **methodology-interpolation finding**.

Methodology-interpolation findings are MATERIAL by their nature per the methodology-interpolation rule (META_PLAN v6 § 6.1) and **lock-blockers regardless of count** per Tony's hard rule.

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

Key observation from the v5 → v6 transition (per META_PLAN v6 changelog "Methodology lesson recorded (v5 → v6)"):

> The v5 audit's M-1 finding revealed that methodology rules introduced mid-cycle do not enforce their own retroactive application. The audit must explicitly include retroactive sweep in its scope when a new rule lands. This becomes a discipline that AUDIT_METHODOLOGY.md (Phase 0 doc 3) must codify: when a new methodology rule is introduced in cycle N, the audit-CC spec for cycle N+1 explicitly includes "sweep prior content for instances of this pattern" as a required adversarial check. The rule itself doesn't enforce its own retroactive application — the audit spec does.

The v6 audit applied the rule retroactively + verified the v5-introduced rule's prior-content sweep was complete. The v6 audit's "Methodology-interpolation rule self-application" section explicitly enumerates grandfathered content (v1-v4 QB-drafted) and sweep-eligible content (v1-v4 CC-introduced) and confirmed zero CC-introduced violations remained post-grandfathering.

#### Cross-references

- **The v5 audit's catch:** META_PLAN v5 audit M-1 finding ("Methodology-interpolation rule self-application" section).
- **The grandfathering clause that bounds the sweep:** META_PLAN v6 § 6.1 (per Tony's locked v6 spec language).
- **v6's verification of correct sweep application:** META_PLAN v6 audit (Methodology-interpolation rule self-application section + Grandfathering clause check section).
- **v6 changelog's banking the lesson for AUDIT_METHODOLOGY:** META_PLAN v6 § 12 ("Methodology lesson recorded (v5 → v6)" subsection).

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

- **Edge case enumeration:** META_PLAN v6 § 3.1 ("Audit-CC error" + "Tony's locked decision based on a wrong premise" patterns).
- **Bug #28 case study with the verbatim quote:** META_PLAN v6 § 8.1 (the "provisional stable-known classification" paragraph quoting "Place, show, and exacta payouts still populate").
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

**v2 cycle:** Per Tony's Option B in the v1 cycle response, BIBLE_STRUCTURE_SPEC v2 dropped the F.N / C.N / D.N extensions and used sub-section numeric IDs throughout (matching DD bible's existing convention). W.N was retained as the only letter-prefix because the cross-bible bug-tracking forcing function (per META_PLAN v6 § 7.11 commit-message convention; a grep over `git log` for `W.7` retrieves every commit related to that immune-memory entry across all bibles) justifies the asymmetry.

**v3 cycle:** BIBLE_STRUCTURE_SPEC v3 § 5.5 carries the locked convention: "The W.N letter-prefix convention is the **only** letter-prefix in EE bible numbering: What Was Fixed entries require cross-bible-trackable identifiers because cross-cutting bugs (per § 5.3 canonical-home rule) reference each other across bibles, and a grep over `git log` for `W.7` retrieves every commit related to that immune-memory entry across all bibles per META_PLAN v6 § 7.11 commit-message convention."

#### Cross-references

- **v1 catch:** BIBLE_STRUCTURE_SPEC v1 audit (severity table #5; Methodology-interpolation rule self-application section).
- **Tony's Option B resolution:** BIBLE_STRUCTURE_SPEC v1 audit (Recommendation #5 with both Option A and Option B); BIBLE_STRUCTURE_SPEC v2 changelog ("M-1 — F.N / C.N / D.N naming convention extension dropped per Tony's Option B").
- **v2 post-Option-B convention:** BIBLE_STRUCTURE_SPEC v2 § 5.5.
- **v3 locked convention:** BIBLE_STRUCTURE_SPEC v3 § 5.5 and § 7.2.
- **v3 changelog banking the lesson for AUDIT_METHODOLOGY:** BIBLE_STRUCTURE_SPEC v3 § 13 (v1 → v2 changelog "Methodology-interpolation finding resolved" subsection: "Pattern-completion interpolation lesson banked for AUDIT_METHODOLOGY.md").

#### Audit-CC prophylactic check template

For any letter-prefix or numeric-prefix convention introduced or referenced in the audited document:

1. **Grep for letter-prefix patterns.** Search for `[A-Z]\.[0-9]` or `[A-Z]\.<n>` patterns within the document's section numbering and cross-reference syntax. Enumerate each unique prefix.
2. **For each prefix found, verify the prefix is named in META_PLAN v6, BIBLE_STRUCTURE_SPEC v3, or a Tony-locked drafting spec for this document.** Independently — pattern parallelism does NOT satisfy ratification. If W.N is ratified, that does NOT ratify F.N or C.N or D.N.
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

v3 verification revealed the artifacts were already covered. The current `.gitignore` already excluded `.frontend-bucket`, `.cf-distribution-id`, `cdk-outputs.json`, and `frontend/.env.production` (per META_PLAN v6 § 7.14 verbatim). v3 § 7.14 surfaced the contradiction in the verification log (Claim 11) and reframed the prerequisite: dropped the "add to gitignore" step (already done); kept the "audit deploy scripts for any uncovered artifacts" step. Tony ratified the reframing in the v4 cycle.

**Invocation 2: v6 cycle — Bug #28 exacta payout claim.**

Tony's MINOR #5 in the v6 cycle was based on v5 audit's claim that the operator memory file was "silent on exacta payout status." Tony's MINOR #5 directed: "soften the exacta claim per the v5 audit's characterization."

v6 verification (with the operator memory file's verbatim quote provided in the v6 audit-CC prompt's OPERATOR-VERIFIED EXTERNAL SOURCE block) revealed the memory file's symptom statement explicitly reads "Place, show, and exacta payouts still populate." v6 § 8.1 applied a reframing faithful to the source: kept the place/show/exacta still-populate claim AND added the DD-pool-extraction nuance the memory file does flag ("DD pool extraction at hrn_scraper.py:814 likely has the same root cause" — distinct from `daily_double_payout` already accounted for in the result-dict). v6 verification log Claim 15c surfaced the contradiction explicitly. The v6 audit's "Operator-verified external source check" section verified the reframing was faithful to the source.

Per META_PLAN v6 changelog ("Methodology lesson recorded (v5 → v6)"): "The 'Tony's locked decision based on a wrong premise' edge case in § 3.1 has been invoked twice now (Q4 in v3, MINOR #5 in v6). The pattern is robust: when verification contradicts a Tony-locked decision, surface to QB → Tony rather than silently complying. v6 surfaces; the resulting reframing is faithful to the verified source."

#### Cross-references

- **Edge case enumeration:** META_PLAN v6 § 3.1 ("Tony's locked decision based on a wrong premise" pattern).
- **v3 invocation (gitignore):** META_PLAN v3 verification log Claim 11; META_PLAN v3 audit (additional adversarial finding "D. v3 reframing of Tony's Q4"); META_PLAN v6 § 7.14 (post-reframing locked content).
- **v6 invocation (exacta):** META_PLAN v6 verification log Claim 15c; META_PLAN v6 § 8.1 (post-reframing locked content); META_PLAN v6 audit (Operator-verified external source check section).
- **v6 changelog's pattern recognition:** META_PLAN v6 § 12 ("Methodology lesson recorded (v5 → v6)").

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

**v3 resolution:** Per Tony's Option I in the v3 cycle, all seven per-document templates were renumbered to match § 5.2's canonical 5/6/7/8 ordering. v3 § 5.2 strengthened the language: "**mandatory for sections 5–8** (per Tony's v3-cycle Finding 1 ratification); domain-specific sections at positions 1–4 may be reorganized per locality of reference." Future drafters of new bibles must conform.

The v2 audit's banking statement (per the v2 → v3 changelog "Methodology lessons recorded" subsection): "When shared templates reference per-document sections by number, audit-CC's prophylactic check should include: 'verify all per-document templates use the same canonical section numbering for the referenced positions; deviations break shared-template cross-references.' This is a special case of the broader contradiction-detection question (META_PLAN v6 § 6.2 Q4) but worth naming explicitly given the recurrence across both v1 and v2 audits."

#### Cross-references

- **v1 catch (8-vs-18):** BIBLE_STRUCTURE_SPEC v1 audit (Question 4 finding 1; severity table #4).
- **v1 → v2 resolution:** BIBLE_STRUCTURE_SPEC v2 changelog (M-2: What Was Fixed positioned at section 8).
- **v2 catch (5-vs-7):** BIBLE_STRUCTURE_SPEC v2 audit (Question 4 finding 1; severity table MATERIAL #1).
- **v2 → v3 resolution + lesson banking:** BIBLE_STRUCTURE_SPEC v3 § 5.2 (canonical 5/6/7/8 mandate); BIBLE_STRUCTURE_SPEC v3 § 13 (v2 → v3 changelog "Methodology lessons recorded" subsection).
- **v3 locked canonical mandate:** BIBLE_STRUCTURE_SPEC v3 § 5.2 + § 5.6 (canonical templates depending on stable numbering); BIBLE_STRUCTURE_SPEC v3 § 6.1-§ 6.7 (all seven per-document templates conforming).
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

The check is mechanical: for the seven Phase 1 bibles, grep each bible's actual draft for canonical section headers (e.g., `^### 5.* Discipline rules`, `^### 6.* Currently Open`, `^### 7.* Deprecated`, `^### 8.* What Was Fixed`); verify all seven drafts have the same absolute positions for these four sections. (The mechanical grep target is the bible drafts at `/docs/bible/<bible>.md`, not BIBLE_STRUCTURE_SPEC v3's per-document templates at v3 § 6.X — those templates are the spec the drafts should conform to.)

---

## 5. Audit-CC Prophylactic Check Templates Consolidated

This section consolidates the seven prophylactic checks from § 4 in paste-ready form for integration into Phase 1 audit prompts. Each check is preceded by its lesson reference for traceability.

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
- META_PLAN v6 or earlier locked Phase 0 documents (Tony-authored or QB-drafted-and-Tony-ratified).
- Operator-stated rationale per source-priority tier 5 (META_PLAN v6 § 4.5).

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
- For each prefix, verify it is named in META_PLAN v6, BIBLE_STRUCTURE_SPEC v3, or a Tony-locked drafting spec for this document. Independently — pattern parallelism does NOT satisfy ratification.
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

The check is mechanical for the seven Phase 1 bibles: grep each bible's actual draft for canonical section headers; verify all seven drafts have the same absolute positions for the canonical 5/6/7/8 group. (Grep target is the bible drafts at `/docs/bible/<bible>.md`, not BIBLE_STRUCTURE_SPEC v3 § 6.X templates.)

---

## 6. Phase 1 Audit-CC Prompt Template

This template is the canonical paste-ready structure for a Phase 1 per-bible audit-CC prompt. It extends META_PLAN v6 Appendix A.6's working example with the seven prophylactic checks from § 5. Per-bible audit prompts customize this template; the template ensures consistency across the seven Phase 1 bibles' audit cycles.

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
(META_PLAN v6, BIBLE_STRUCTURE_SPEC v3, AUDIT_METHODOLOGY v1, CONVERGENCE_CRITERIA,
TRIAGE_QUEUE_SPEC) that govern Phase 1 drafting. The bible you are auditing is one
of seven Phase 1 documents producing the canonical reference for what EE is.

This bible's role in the Phase 1 inventory: [PER BIBLE — drawn from BIBLE_STRUCTURE_SPEC v3 § 4.1].

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
    (NOTE: dump is best-available baseline, not source of truth; verify against live state per META_PLAN v6 § 4.5)
  - Live AWS state via `aws` CLI for any infrastructure claim verification
  - Live API endpoints (e.g., dashboard at gb5qlfy10h.execute-api.us-east-1.amazonaws.com/dashboard/metrics)
  - The EE codebase at /home/strakajagr/projects/equine-equalizer/

VERIFICATION DISCIPLINE (HARD RULE):
  - When you verify factual claims in this draft, prefer live AWS / database / code over the dump.
  - The dump has been wrong about multiple facts in prior audits. Independent verification is the safeguard.
  - For any claim about file paths, function signatures, line numbers, or behavior — read the file or run the command.
  - Counts must be decomposed (e.g., "3 instantiations + 1 import = 4 references"); do not accept compressible aggregations
    in the draft. Per the verification-log precision rule (META_PLAN v6 § 6.5; AUDIT_METHODOLOGY § 4.1).
  - Methodology constructs must trace to META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 / Tony-locked spec language.
    Per the methodology-interpolation rule (META_PLAN v6 § 6.1; AUDIT_METHODOLOGY § 4.2), CC-introduced methodology is
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
[Specific scope-completeness checks: e.g., does the bible contain all canonical TOC sections per BIBLE_STRUCTURE_SPEC v3
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

ADDITIONAL DOCUMENT-TYPE-SPECIFIC CHECKS:
[QB inserts per-bible checks here. The examples below are drawn from BIBLE_STRUCTURE_SPEC v3 § 6.X anchor verifications,
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
  - Per-question findings (Q1-Q6 + prophylactic checks 1-7 + document-type-specific checks)
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

Tony's threshold (per META_PLAN v6 § 11; AUDIT_METHODOLOGY § 3.5):
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

The cross-document consistency audit runs after all seven Phase 1 bibles lock individually. It is a separate fresh CC session that reads all per-document audit reports as input and verifies internal consistency across the corpus. Per META_PLAN v6 § 3.3, three additional questions are appended to the six adversarial questions of META_PLAN v6 § 6.2 for cross-document audit.

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
per META_PLAN v6 § 3.3.

QUESTION 1: What's in any bible that I can't verify from the referenced source material across other bibles?
[Examples: a feature_provenance_bible reference to ml_layer_architecture_bible:5.4 — does that section exist?
a data_pipeline_bible reference to a flow that's documented in architecture_overview's Lambda inventory — do
the two descriptions match?]

QUESTION 2: What's missing across the corpus based on its stated scope?
[Per BIBLE_STRUCTURE_SPEC v3 § 4: are all canonical TOC sections present in all seven bibles? Per the convergence
test (META_PLAN v6 § 3.2.1): can a fresh CC session evaluate / rebuild / retrain a model in the gallery using only
the locked corpus?]

QUESTION 3: Where is language ambiguous enough that two readers could interpret it differently across bibles?

QUESTION 4: Where do bibles contradict each other across files?
[Specifically: same fact stated differently in different bibles; same canonical name used inconsistently;
cross-references broken.]

QUESTION 5: What sections feel rushed or hand-waved within the corpus context?

QUESTION 6: What examples are missing that would make abstract claims concrete across the corpus?

QUESTION 7 (cross-document, per META_PLAN v6 § 3.3): Does the bible say something the code does not do?
[Phase 1 cross-document scope: limit to claims surfaced by bible-vs-bible cross-reference analysis. Full code-vs-
bible reconciliation is Phase 2.]

QUESTION 8 (cross-document, per META_PLAN v6 § 3.3): Does the code do something the bible does not say?
[Phase 1 cross-document scope: limit to gaps in coverage that bible-vs-bible analysis surfaces. Full code-vs-bible
gap analysis is Phase 4.]

QUESTION 9 (cross-document, per META_PLAN v6 § 3.3): Where do bible documents contradict each other across files?
[The canonical cross-document audit question. Specifically:
  - Cross-cutting bug canonical-home assignments (per BIBLE_STRUCTURE_SPEC v3 § 5.3): is each cross-cutting bug
    homed in exactly one bible with cross-references from others, never duplicated?
  - Canonical object names (per BIBLE_STRUCTURE_SPEC v3 § 4.1.1 in architecture_overview): consistent across all
    bibles that reference them?
  - Canonical section numbering (per BIBLE_STRUCTURE_SPEC v3 § 5.2 mandatory 5/6/7/8): all seven bibles compliant?
  - Cross-bible references (`<bible_name>:<section_id>`): every reference resolves to an actual section in the
    target bible?]

PROPHYLACTIC CHECKS (per AUDIT_METHODOLOGY § 5):

The seven prophylactic checks apply across the corpus, not within single bibles:

PROPHYLACTIC CHECK 1 — Verification-log precision across the corpus (§ 5.1):
For aggregable counts cited across multiple bibles (e.g., 88 = 45 active + 43 inactive cited in ml_layer_architecture_bible
AND model_evaluation_retraining_bible AND elsewhere), verify decomposition matches across all citations.

PROPHYLACTIC CHECK 2 — Methodology-interpolation across the corpus (§ 5.2):
For methodology constructs introduced in any bible (e.g., a new discipline rule), verify the construct traces to
META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 / Tony-locked drafting spec. Per-bible audits should have caught individual
instances; this check sweeps for any that survived multiple per-bible audits.

PROPHYLACTIC CHECK 3 — Retroactive sweep discipline (§ 5.3):
Verify cross-document audit specifically sweeps for instances of newly-introduced rules that may not have been
caught by per-bible audits. Phase 1 introduces no new methodology rules (it operates under META_PLAN v6 +
BIBLE_STRUCTURE_SPEC v3 + AUDIT_METHODOLOGY v1 already-locked); the retroactive sweep here verifies all seven
bibles uniformly applied the locked rules.

PROPHYLACTIC CHECK 4 — Operator-verified external source (§ 5.4):
For operator-verified external sources cited across multiple bibles (e.g., Bug #28 memory file cited from
data_pipeline_bible's W.<n> entry and possibly cross-referenced from ml_layer_architecture_bible's calibration-bypass
discussion), verify all citations match the verbatim source.

PROPHYLACTIC CHECK 5 — Pattern-completion interpolation (§ 5.5):
For letter-prefix or numeric-prefix conventions used across the corpus (W.N is the only ratified letter-prefix per
BIBLE_STRUCTURE_SPEC v3 § 5.5), grep all seven bibles for any unratified prefix conventions. Pattern parallelism
across multiple bibles does NOT constitute ratification.

PROPHYLACTIC CHECK 6 — "Tony's locked decision based on a wrong premise" (§ 5.6):
When cross-document analysis surfaces that a Tony-locked premise underlying any bible's content is false (per
verification across the corpus), surface to QB → Tony per the bidirectional pattern.

PROPHYLACTIC CHECK 7 — TOC contradiction (§ 5.7):
The MECHANICAL CHECK: grep each of the seven bibles for canonical 5/6/7/8 section headers (Discipline rules /
Currently Open / Deprecated / What Was Fixed). Verify all seven bibles have these four sections at canonical
absolute positions. Verify cross-bible references targeting these positions resolve consistently.

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
  - Per-question findings (Q1-Q9 + prophylactic checks 1-7)
  - Cross-cutting consistency table (by canonical home: where homed, where referenced, consistency status)
  - Severity assessment table
  - Material findings count + justification
  - Recommendation

THRESHOLD CONTEXT:

Same threshold as per-bible audits:
  - < 5 MATERIAL findings AND
  - zero fabricated-content findings AND
  - zero methodology-interpolation findings (post-grandfathering)

Per-bible re-revision trigger: per META_PLAN v6 § 3.3, "if a per-document audit returns >5 MATERIAL findings, that
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

### 8.1 Per-bible audit prompt customization granularity

§ 6's template includes `[ADDITIONAL DOCUMENT-TYPE-SPECIFIC CHECKS]` as a customization slot. The customizations listed in the template's example block (verify INDEX section for Architecture Overview; verify 14 tables for Database & Schema; etc.) are illustrative, not prescriptive. Whether each Phase 1 audit prompt is hand-customized by QB at audit time OR derived from a per-bible template QB pre-writes is a Phase 1 working-agreement decision per the pattern established in META_PLAN v6 § 7.13's deferral-to-Phase-5 framing applied to Phase 1 audit-CC prompt drafting cadence.

### 8.2 Cross-document audit re-trigger after per-bible revision

If the cross-document audit surfaces a finding that requires one bible to revise, that bible re-locks per its own per-bible cycle. Whether the cross-document audit re-runs immediately, runs only at Phase 1 final completion, or follows a different cadence is deferred — per META_PLAN v6's pattern of deferring cadence-shaped decisions to operational phase entry.

### 8.3 Inheritance verification across audit cycles

Per § 4.3's retroactive sweep discipline, when a methodology rule lands in cycle N, the audit-CC spec for cycle N+1 includes retroactive sweep. For Phase 1 audits, no new methodology rules are introduced (Phase 1 operates under locked Phase 0 documents); inheritance verification is the relevant check rather than retroactive sweep. The check template in § 5.3 covers both — when first-cycle-after-rule-introduction, perform sweep; otherwise, verify inheritance documented. Whether Phase 1 audits need any further refinement of the inheritance check is deferred until Phase 1 audit cycles surface a need.

---

## 9. Lock Status

**Document status:** DRAFT v2, pre-audit
**Audit-CC pass:** pending (v2 audit pending after disk write)
**Verification log:** `_audits/AUDIT_METHODOLOGY_v2_verification.md` — inherits v1's 41 claims with re-verified-2026-05-04 timestamps; adds 1 new claim (Claim 42 — verbatim attribution of v2 audit Q2.2 + Tony's Q4 in § 4.6)
**Tony review:** pending (will see post-audit version per workflow discipline)
**Locked:** [pending]

**Phase 0 prerequisites carried over from META_PLAN v6 § 11:**
- All 5 Phase 0 documents pass adversarial audit (Tony's threshold: < 5 MATERIAL findings AND zero fabricated-content findings AND zero methodology-interpolation findings)
- Operating-model convergence test passes (META_PLAN v6 § 5.4)
- EE production code committed to baseline (META_PLAN v6 § 3.1.1)
- `.gitignore` baseline audit performed; findings documented at `_audits/gitignore_baseline_audit.md` (META_PLAN v6 § 7.14)
- `PHASE_5_BACKLOG.md` created with Bug #28 as first entry (META_PLAN v6 § 8.2)

**Next action:** QB writes paste-ready audit-CC prompt for v2. Tony runs audit. QB synthesizes findings.

---

## 10. Changelog

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

---

## 11. CC Drafting Notes (Self-Check Surfaces)

Per the methodology-interpolation rule, CC reviewed every new construct introduced in v1 against the rule. Items below are surfaced for Tony's awareness; CC's judgment on each is included.

### 11.1 Constructs explicitly authorized by META_PLAN v6 / BIBLE_STRUCTURE_SPEC v3 / Tony's locked drafting spec

- Tier 3 designation per META_PLAN v6 § 4.1.
- The seven methodology lessons in § 4 (each individually authorized by Tony's locked methodology lesson catalog in the drafting spec).
- The four required structural elements per lesson (rule + worked example + cross-references + prophylactic check template) — per Tony's locked drafting requirements.
- The order of the seven lessons (introduced empirically across cycles) — per Tony's locked language: "The order reflects the empirical sequence of their introduction across cycles; preserving the order documents the discipline's evolution."
- The audit-CC prompt template in § 6 extending META_PLAN v6 Appendix A.6.
- The cross-document audit prompt template in § 7 extending § 6 with three cross-document questions per META_PLAN v6 § 3.3.
- All threshold language inherited verbatim from META_PLAN v6 § 11.
- All edge cases inherited verbatim from META_PLAN v6 § 3.1.
- All workflow steps inherited from META_PLAN v6 § 3.1 + BIBLE_STRUCTURE_SPEC v3 § 8.3.

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

- **Iteration cap on Phase 1 audit cycles** — would be a numerical threshold not in source; deferred per META_PLAN v6's pattern.
- **Cadence specification for cross-document audit re-trigger after per-bible revision** — surfaced as Open Question 8.2 instead of drafting a cadence rule.
- **Severity thresholds beyond META_PLAN v6's < 5 MATERIAL** — not introduced; thresholds inherited verbatim from § 11.
- **Completeness criteria for prophylactic check application** — would be a binary pass/fail rule; deferred to Tony's existing < 5 MATERIAL threshold and methodology-interpolation rule's lock-blocker classification.
- **Scoring rubric for audit findings** — not introduced.
- **Percentage criterion for cross-document consistency** (e.g., "≥ 90% of cross-references must resolve") — not introduced; resolution-failure is treated qualitatively per the seven prophylactic checks.
- **Procedural sequencing rules beyond what META_PLAN v6 § 3.1 + BIBLE_STRUCTURE_SPEC v3 § 8.3 already specify** — not introduced.
- **Tiebreaker criteria for canonical-home determination in cross-cutting bugs** — explicitly deferred to Tony per BIBLE_STRUCTURE_SPEC v3 § 5.3's locked deferral.
- **New letter-prefix conventions** — not introduced (W.N remains the only ratified prefix per BIBLE_STRUCTURE_SPEC v3 § 5.5).
- **Worked examples beyond those drawn from Phase 0 cycle audit findings** — every worked example in § 4 references a specific cycle and specific finding; no hypothetical or invented examples.

The methodology-interpolation rule is operative; the discipline of self-surfacing remains. v1 surfaces what's new.

---

End of AUDIT_METHODOLOGY.md v1.
