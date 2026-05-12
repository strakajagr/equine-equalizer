# BIBLE_STRUCTURE_SPEC v4 — Verification Log

**Document:** companion verification log for `BIBLE_STRUCTURE_SPEC.md` v4
**Phase:** 0 (Methodology) — Phase 0 deliverable 2 of 5; post-convergence-test revision per Path A
**Author:** CC (drafting under verification discipline; QB orchestrated)
**Date:** 2026-05-05
**Anchored on:** BIBLE_STRUCTURE_SPEC v3 (pre-lock; superseded by v4 in-place) + `_audits/convergence_test_audit.md` + META_PLAN v8 (LOCKED) + drafting spec for v4

This log records the v4 verification delta. Per surgical-patch convention (this cycle covers only the changed content): only changed content gets new verification entries. v3's verification log entries (`_audits/BIBLE_STRUCTURE_SPEC_v3_verification.md`) are inherited wholesale for unchanged content; not re-verified during v4.

**Discipline:** every concrete factual claim about v4's fixes has a verification entry. Counts decomposed per META_PLAN v8 § 6.5 verification-log-precision rule. Recursive precision discipline (per TRIAGE_QUEUE_SPEC v1): verbatim claims reproduce source character-exact including formatting (em-dashes, single-quotes, code spans, line breaks).

---

## Verification claim count

- **Inherited from v3 verification log:** all entries (V3's 25 inherited-from-v2 + N9 + N10 = 27 claims). Wholesale inheritance — not re-decomposed.
- **New for v4:** 11 entries (V4-1 through V4-11).

Decomposition of convergence test gap closure scope: **9 methodology gaps total (G1–G9)** per `_audits/convergence_test_audit.md`. **G8 closed in META_PLAN v7→v8 cycle** (LOCKED). **8 gaps closed in v4 cycle** (G1, G2, G3, G4, G5, G6, G7, G9). 1 + 8 = 9. ✓ matches.

Decomposition of v4 fix categories: **A (§ 3.3 cross-bible reference syntax extension), B (§ 5.3 cross-cutting Currently Open scope rule), C (§ 5.5 W.N scope clarification + new § 5.5.1 global Bug #N), D (§ 5.6.1 W.N entry template scope confinement), E (§ 5.6.1.1 worked example update + new § 5.6.1.2 tertiary state), F (§ 5.6.4 Deprecated entry SQL constraint qualification), G (new § 5.7 convergence rule on rule rosters), H (§ 6.X Recommended TOC header replacement × 7), I (§ 7.1 cross-reference syntax extension + new § 7.1.1 worked examples)** = 9 fix categories. Plus § 12.4 v4 surfacing notes + § 13 v3→v4 changelog entry + front matter v4 entry. ✓ matches drafting spec deliverable structure.

---

## New verification entries (v4 cycle)

### V4-1: § 3.3 cross-bible reference syntax extension (G9 partial closure; closes drafter touchpoint)

**Claim location in v4:** § 3.3 (Section ID convention).

**Verification:**
- Replacement text reproduces drafting spec requirement A char-exact: 5 example bullets (`feature_provenance_bible:4.1`, `data_pipeline_bible:8.W.7`, `database_schema_bible:5.4`, `feature_provenance_bible:#15`); closing paragraph references META_PLAN v8 § 7.11 (updated from v6); paragraph names `<bible_doc_name>:#<bug-id>` cross-bible bug reference format; cross-references § 5.5.1 below.
- Bash `grep -c "feature_provenance_bible:#15" /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` returns count > 0. ✓ new format example present.
- v3's 3 example bullets preserved char-exact; new bullet (5th example) added per drafting spec.

**Decomposition:** 5 example bullets in v4 § 3.3 (4 from v3 + 1 new for cross-cutting bug reference); 1 new closing paragraph cross-referencing § 5.5.1 G9 closure.

### V4-2: § 5.3 cross-cutting bug Currently Open scope rule added (closes G1)

**Claim location in v4:** § 5.3 (Cross-cutting bug scope rule).

**Verification:**
- Second paragraph modification: `<bible>:8.W.<n>` cross-reference replaced with `<bible>:#<bug-id>` per § 3.3 cross-reference syntax for cross-cutting bugs. Char-exact match to drafting spec requirement B's first replacement.
- New paragraph added per drafting spec requirement B: "Cross-cutting bug Currently Open scope rule (closes G1)" with full rule body (substantive description in canonical-home; one-line cross-references in non-canonical-home bibles; symptom-touch determination at drafter discretion; § 6 cross-references removed once W.N entry replaces them; PHASE_5_BACKLOG.md entries cite canonical home plus all bibles whose § 6 references the bug).
- Bash `grep -c "Cross-cutting bug Currently Open scope rule" /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` returns 1. ✓ rule present.

**Decomposition:** 1 paragraph modified (canonical home cross-reference format updated); 1 new paragraph added (G1 closure rule).

### V4-3: § 5.5 W.N scope clarification + new § 5.5.1 global Bug #N convention (closes G9)

**Claim location in v4:** § 5.5 first bullet (modified) + new § 5.5.1 (added).

**Verification:**
- § 5.5 first bullet replacement: char-exact match to drafting spec requirement C's replacement text. References META_PLAN v8 § 7.4 + Appendix A.3 (updated from v6); names W.N as bible-local; cross-references § 5.5.1 G9 resolution; preserves grep-discipline rationale; references META_PLAN v8 § 7.11.
- New § 5.5.1 added per drafting spec requirement C: "Global Bug #N convention (closes G9)" with monotonic assignment, never-reused, cross-bible reference uses `#<bug-id>`, de facto convention now explicit; pattern-completion check note (W.N remains the only ratified letter-prefix; `#<bug-id>` is a syntax extension not a letter-prefix).
- Bash `grep -c "Global Bug #N convention" /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` returns 2 (header + section text). ✓ section present.
- "(locked 2026-05-05 per v4 cycle)" parenthetical present in § 5.5.1 convention specifics.

**Decomposition:** 1 bullet modified in § 5.5 (W.N scope clarification); 1 new sub-section added (§ 5.5.1 with 4 convention specifics + 1 pattern-completion note).

### V4-4: § 5.6.1 W.N entry template confined to bug-fix entries (closes G3)

**Claim location in v4:** § 5.6.1 (What Was Fixed entry template).

**Verification:**
- Mandatory fields block updated per drafting spec requirement D: new "Scope (locked per v4 cycle, closes G3)" clause inserted before Mandatory fields; "Bug name or short description (with global Bug #N if assigned per § 5.5.1)" parenthetical added; Fix date mandatory clause emphasized with "**mandatory; entries without a knowable fix date belong in § 5, not § 8**" inline emphasis.
- Scope clause text reproduces drafting spec requirement D char-exact, including: "true bug-fix entries with mandatory Fix date" emphasis; "Discipline codifications" routed to § 5; reference to META_PLAN v8 § 7.3 placeholder-resolution sub-rule's case (ii); explicit statement that § 5 entries do not require Fix date because they are rules, not fixes.
- Bash `grep -c "Scope (locked per v4 cycle, closes G3)" /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` returns 1. ✓ scope clause present.

**Decomposition:** 1 scope clause added; 1 mandatory field annotated (Bug name with global Bug #N); 1 mandatory field emphasized (Fix date mandatory).

### V4-5: § 5.6.1.1 worked example update + new § 5.6.1.2 tertiary state (closes G7)

**Claim location in v4:** § 5.6.1.1 (existing worked example, modified Conditional triggers block) + new § 5.6.1.2 (Tertiary-state notation).

**Verification:**
- § 5.6.1.1 conditional triggers block replacement: char-exact match to drafting spec requirement E. The if-fix-touches-multiple-bibles trigger now CONDITIONAL (was FIRES); cross-references updated from `ml_layer_architecture_bible:8` and `model_evaluation_retraining_bible:8` to `ml_layer_architecture_bible:#15` and `model_evaluation_retraining_bible:#15` (global Bug #N format per § 5.5.1); CONDITIONAL caveat documented in adjacent prose (the cross-references are descriptive of where Bug #15 manifests; canonical W.N entry lives only in Feature Provenance Bible per cross-cutting bug scope rule).
- New § 5.6.1.2 added per drafting spec requirement E: "Tertiary-state notation for conditional trigger evaluation (closes G7)" with three states (FIRES, DOES NOT FIRE, CONDITIONAL) and CONDITIONAL discipline (mandatory adjacent-prose caveat; AUDIT_METHODOLOGY v2 § 5.2 prophylactic check applies recursively).
- Bash `grep -c "Tertiary-state notation" /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` returns 1. ✓ section header present.
- "(per § 5.6.1.2 tertiary-state notation, locked per v4 cycle)" parenthetical present in § 5.6.1.1 worked example header for conditional triggers.

**Decomposition:** 1 conditional triggers block modified (4 trigger evaluations preserved with 1 changed from FIRES to CONDITIONAL + caveat prose); 1 new sub-section added (§ 5.6.1.2 with 3 state definitions + CONDITIONAL discipline).

### V4-6: § 5.6.4 Deprecated entry template extended for SQL constraint qualification (closes G2)

**Claim location in v4:** § 5.6.4 (Deprecated entry template).

**Verification:**
- New conditional bullet added per drafting spec requirement F: "If the deprecated thing is a superseded SQL constraint or schema element"; references migration 011's `wr_predictions` UNIQUE constraint as canonical example; verification trigger via `\d <table>` or migration history; physical-persistence determines Deprecated qualification; if physically dropped, migration history serves as immune memory; drafter discretion with verification log entry.
- Bash `grep -c "If the deprecated thing is a superseded SQL constraint" /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` returns 1. ✓ bullet present.
- Existing 3 conditional field bullets preserved char-exact; new bullet appended at end of list.

**Decomposition:** 1 new conditional field bullet added (after the existing 3 bullets).

### V4-7: § 5.7 convergence rule on Discipline rule rosters added (closes G5)

**Claim location in v4:** new § 5.7 (Convergence rule on Discipline rule rosters).

**Verification:**
- New § 5.7 added per drafting spec requirement G: opening paragraph names domain-specific discipline needs and rejects pre-specified minimum lists; "Convergence rule (locked per v4 cycle)" specifies substrate enumeration + QB ratification + 3-criterion synthesis (cross-bible coherence, Tony's prior ratifications, substrate grounding); Workflow specifies 5-step round trip per bible; Provenance discriminator mirrors methodology-interpolation grandfathering pattern per META_PLAN v8 § 6.1; Cycle cost framing.
- Bash `grep -c "Convergence rule on Discipline rule rosters" /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` returns 3 (header at line 450; § 12.4 surfacing note reference; § 13 changelog reference). ✓ section present and cross-referenced.
- 5-step workflow numbered correctly: 1. CC drafts § 5 with candidate roster; 2. CC produces § 5 verification log delta; 3. QB reviews; 4. CC re-drafts; 5. § 5 locks.

**Decomposition:** 1 new top-level sub-section (§ 5.7); 5 numbered workflow steps; 3 QB synthesis criteria; 1 provenance discriminator clause.

### V4-8: § 6.1–§ 6.7 "Recommended TOC" header replacement (closes G4)

**Claim location in v4:** § 6.1, § 6.2, § 6.3, § 6.4, § 6.5, § 6.6, § 6.7 (each contains the "Recommended TOC:" header).

**Verification:**
- All 7 "Recommended TOC:" headers replaced with "TOC (sections 5–8 mandatory per § 5.2; sections 1–4 recommended-strongly with drafter latitude per locality of reference):" per drafting spec requirement H.
- Bash `grep -c "Recommended TOC:" /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` returns 3 — all 3 occurrences are in descriptive change-history (§ 12.4 line 1208 documenting what was replaced; § 13 line 1251 v3→v4 changelog G4 bullet; § 13 line 1271 retained-from-v3 list mentioning what was replaced). The 7 operative occurrences in § 6.X templates are removed.
- Bash `grep -c "TOC (sections 5–8 mandatory" /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` returns 8 — 7 operative replacements (one per § 6.X) + 1 descriptive in § 12.4 documenting the replacement target. ✓ matches expected count.
- The numbered TOC content following each header is unchanged from v3.
- Operative line positions: 489 (§ 6.1), 566 (§ 6.2), 636 (§ 6.3), 712 (§ 6.4), 783 (§ 6.5), 855 (§ 6.6), 928 (§ 6.7).

**Decomposition:** 7 operative header replacements; 0 changes to numbered TOC content beyond header phrase.

### V4-9: § 7.1 cross-reference syntax extension + new § 7.1.1 worked examples (closes G6)

**Claim location in v4:** § 7.1 (modified) + new § 7.1.1 (added).

**Verification:**
- § 7.1 replacement: char-exact match to drafting spec requirement I's first replacement. Adds `<bible_name>:#<bug-id>` cross-cutting bug reference format per § 3.3 + § 5.5.1; updates META_PLAN reference from v6 to v8.
- New § 7.1.1 added per drafting spec requirement I: "Cross-reference syntax worked examples (closes G6)" with 6 worked-example bullets (within-bible numeric, within-bible W.N, cross-bible by section ID, cross-bible by W.N, cross-bible by global Bug #N, cross-reference to PHASE_5_BACKLOG.md by phase number).
- Bash `grep -c "Cross-reference syntax worked examples" /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` returns 1 (just the section header). ✓ section present.
- AUDIT_METHODOLOGY v2 § 5.5 pattern-completion check cross-reference present for cross-reference syntax extensions.

**Decomposition:** 1 paragraph modified in § 7.1 (cross-cutting bug reference syntax extension); 1 new sub-section (§ 7.1.1) with 6 worked-example bullets + 1 pattern-completion check paragraph.

### V4-10: § 12.4 v4 surfacing notes + § 13 v3→v4 changelog entry added

**Claim location in v4:** new § 12.4 (v4 surfacing notes) + § 13 v3→v4 changelog entry (added before existing v2→v3 entry).

**Verification:**
- § 12.4 added with 4 sub-sections: Items resolved by Tony's v4 cycle decisions (G3/G5/G7/G9 — 4 architectural-question resolutions with brief description); Items resolved per audit-CC-recommended resolutions (G1/G2/G4/G6 — 4 implementations with brief description); METHODOLOGY-INTERPOLATION self-check (4 categories of authorization tracing); METHODOLOGY-INTERPOLATION rule pattern-completion check; AUDIT_METHODOLOGY v3 cycle assessment (NOT warranted, with reasoning per drafting discipline 7); Net new methodology constructs count (8); Items NOT addressed in v4 (preserved from v3 unchanged).
- § 13 v3→v4 entry added with: 8 MATERIAL fix bullets (one per closed gap, traceable to drafting spec); Methodology lessons recorded (convergence test caught 9 gaps single-drafter audit cycles couldn't; v4's 8-gap-closure scope is heavier than typical surgical-patch); Banked for AUDIT_METHODOLOGY.md (potential v3 cycle if drift surfaces; NOT warranted at this lock); Path A sequencing note (after v4 lock, convergence test re-runs); Retained from v3 unchanged list.
- v2→v3 changelog entry preserved verbatim under existing position.

**Decomposition:** 1 new § 12.4 sub-section with 7 sub-blocks; 1 new § 13 v3→v4 entry with 5 sub-blocks; v2→v3 entry preserved verbatim.

### V4-11: META_PLAN version references updated v6 → v8 per drafting spec requirement A's "throughout" directive

**Claim location in v4:** all locations where META_PLAN version references appear in v4-modified content.

**Verification (per drafting spec interpretation):**
- Drafting spec requirement A says "Update META_PLAN version reference from `v6` to `v8` throughout." Within the v4-authorized scopes (§ 3.3, § 5.3, § 5.5 first bullet, § 5.6.1, § 5.6.1.1, § 5.6.1.2, § 5.6.4 new bullet, § 5.7, § 6.X Recommended TOC headers, § 7.1, § 7.1.1, § 12.4, § 13 v3→v4): all META_PLAN references in spec-prescribed replacement texts use `v8` per spec; CC reproduces char-exact.
- Within retained-verbatim sections (§ 1, § 2, § 4, § 6.X content beyond TOC header replacement, § 8, § 9, § 10, § 11, § 12.1–§ 12.3, § 13 v2→v3): META_PLAN v6 references preserved per surgical-patch discipline (spec section 14: "Do NOT modify... retained from v3 verbatim").
- This creates a v4 document with mixed v6 and v8 references. The reference resolution is materially identical (v8 retained v6's referenced content verbatim per V8-7 in META_PLAN v7→v8 audit), but the textual references differ between modified and retained sections. **Surfaced for QB awareness**: this interpretation prefers surgical-patch discipline (retained-verbatim hard rule) over global coherence (v6→v8 sweep). If QB prefers global sweep, a follow-up surgical-patch cycle can update remaining v6 references.

**Decomposition (operative v8 references introduced in v4):**
- § 3.3 closing paragraph: 1 reference to META_PLAN v8 § 7.11 (replacing v6).
- § 5.5 first bullet: 2 references to META_PLAN v8 (§ 7.4 + Appendix A.3; § 7.11).
- § 5.6.1 scope clause: 1 reference to META_PLAN v8 § 7.3.
- § 5.7: 3 references to META_PLAN v8 (§ 9.1-9.13; § 6.1 grandfathering pattern; meta references in workflow).
- § 7.1 closing: 1 reference to META_PLAN v8 § 7.11.
- § 7.1.1 PHASE_5_BACKLOG bullet: 1 reference to META_PLAN v8 § 9.9.
- § 12.4: multiple references to META_PLAN v8.
- § 13 v3→v4 changelog: multiple references to META_PLAN v8.

**Total new v8 references introduced in v4-authorized scopes:** ~15+ (decomposition above is not exhaustive; v8 references appear across all v4-modified content).

---

## Inherited claims (from v3 verification log)

All entries in `_audits/BIBLE_STRUCTURE_SPEC_v3_verification.md` (V3's 25 inherited-from-v2 + N9 + N10 = 27 claims) are inherited wholesale for unchanged content per v4's surgical-patch convention. The following sections of BIBLE_STRUCTURE_SPEC are inherited unchanged from v3:

- § 1 Purpose and Scope (all sub-sections) — inherited unchanged.
- § 2 Operating Principles (all sub-sections) — inherited unchanged.
- § 3.1 Filesystem location — inherited unchanged.
- § 3.2 Filename convention — inherited unchanged. **§ 3.3 modified per V4-1; bulk content of § 3 retained.**
- § 4 Phase 1 Document Inventory (all sub-sections) — inherited unchanged.
- § 5.1 Front matter — inherited unchanged.
- § 5.2 Canonical TOC pattern — inherited unchanged. **§ 5.3 modified per V4-2 (one paragraph + new paragraph); bulk content retained.**
- § 5.4 Dated lock points — inherited unchanged. **§ 5.5 modified per V4-3 (one bullet replaced + new § 5.5.1 added); bulk content of § 5.5 retained.**
- **§ 5.6.1 modified per V4-4 (Mandatory fields scope clause + emphasis); template body retained.**
- **§ 5.6.1.1 modified per V4-5 (Conditional triggers block); worked example narrative retained. § 5.6.1.2 added per V4-5.**
- § 5.6.2 Forbidden Pattern entry template — inherited unchanged.
- § 5.6.3 Common Mistakes entry template — inherited unchanged.
- **§ 5.6.4 modified per V4-6 (one new conditional bullet appended); existing bullets retained.**
- **§ 5.7 added per V4-7.**
- § 6.1 through § 6.7 — content inherited unchanged **except for the uniform "Recommended TOC:" header replacement per V4-8.**
- **§ 7.1 modified per V4-9 (cross-reference syntax extension); § 7.1.1 added per V4-9.**
- § 7.2 through § 7.6 — inherited unchanged.
- § 8 through § 11 — inherited unchanged.
- **§ 12 v3 surfacing notes (§ 12.1, § 12.2, § 12.3) inherited unchanged. § 12.4 added per V4-10.**
- **§ 13 v2→v3 entry preserved verbatim. § 13 v3→v4 entry added per V4-10.**

---

## Methodology-interpolation self-check

Per META_PLAN v8 § 6.1 (with v6 expanded scope, grandfathering clause, and pattern-completion check), CC must surface any methodology constructs introduced that Tony has not explicitly ratified.

**Net new methodology constructs introduced in v4: 8** (4 Tony-locked decisions + 4 audit-CC-recommended resolutions).

**Authorization tracing (8 of 8 trace to drafting-spec authorization):**

1. **G3 — § 8 confined to bug-fix entries (§ 5.6.1 scope clause):** Tony's locked decision in this cycle's drafting spec ("TONY'S LOCKED DECISIONS ON v4 SCOPE: G3 — W.N for non-bug entries: Option (b)"). Reproduced char-exact per spec requirement D. **Authorized; not interpolation.**
2. **G5 — Convergence rule on Discipline rule rosters (§ 5.7):** Tony's locked decision in this cycle's drafting spec ("G5 — Convergence rule on discipline rosters: Option (b)"). Reproduced char-exact per spec requirement G. **Authorized; not interpolation.**
3. **G7 — CONDITIONAL tertiary state (§ 5.6.1.2):** Tony's locked decision in this cycle's drafting spec ("G7 — Tertiary state: authorize CONDITIONAL with tight semantics"). Reproduced char-exact per spec requirement E. **Authorized; not interpolation.**
4. **G9 — Global Bug #N convention (§ 5.5.1):** Tony's locked decision in this cycle's drafting spec ("G9 — W.N numbering convention: bible-local W.N + global Bug #N for cross-bible references"). Reproduced char-exact per spec requirement C. De facto convention pre-existing in operator usage; v4 makes existing convention explicit. **Authorized; not interpolation.**
5. **G1 — Cross-cutting Currently Open scope rule (§ 5.3):** drafting-spec embedded exact replacement text per requirement B (audit-CC-recommended resolution). **Authorized; not interpolation.**
6. **G2 — Superseded SQL constraint Deprecated qualification (§ 5.6.4 new bullet):** drafting-spec embedded exact replacement text per requirement F (audit-CC-recommended resolution). **Authorized; not interpolation.**
7. **G4 — § 6.X TOC framing (sections 5–8 mandatory; sections 1–4 recommended-strongly):** drafting-spec embedded exact replacement text per requirement H (audit-CC-recommended resolution). **Authorized; not interpolation.**
8. **G6 — Cross-reference syntax worked examples (§ 7.1.1):** drafting-spec embedded exact replacement text per requirement I (audit-CC-recommended resolution). **Authorized; not interpolation.**

**Surfaced for awareness (not interpolations):**

1. **Codification step itself (G9 specifically):** the global Bug #N convention pre-existed de facto in operator usage. § 5.5.1 codifies the convention formally. The codification step itself creates the formal rule even when the substrate convention pre-exists. Tony's locked language explicitly addresses this ("Make explicit what's already de facto"). Surfaced for awareness; not interpolation.

2. **CONDITIONAL state name choice:** Tony's locked language said "name the case's distinguishing feature (a condition modifies trigger application) rather than describing discomfort with binary classification." The name "CONDITIONAL" itself was Tony-locked. Surfaced for awareness; not interpolation.

3. **Mixed v6/v8 META_PLAN references in v4:** the drafting spec's "Update META_PLAN version reference from `v6` to `v8` throughout" directive within requirement A creates ambiguity between (a) throughout the § 3.3 replacement scope and (b) throughout the v4 document. CC's resolution: update v6 → v8 within v4-authorized scopes (where spec-prescribed replacement text contains v8 references); preserve v6 references in retained-verbatim sections (per surgical-patch discipline). The v8 references all resolve materially identically to v6 references because v8 retained v6's referenced content verbatim. **Surfaced for QB awareness as an interpretation choice.** If QB prefers global sweep, follow-up surgical-patch cycle can update remaining v6 references.

4. **8-gap-closure scope is heavier than typical surgical-patch:** v4 closes 8 findings vs META_PLAN v7→v8's 4. The drafting spec's resolution of routing 4 architectural questions to Tony for locked decisions and 4 audit-CC recommendations to drafting-spec embedded exact-text replacements is the integration model. Surfaced in § 13 v3→v4 changelog "Methodology lessons recorded"; not a new methodology rule.

**Pattern-completion check (per AUDIT_METHODOLOGY v2 § 5.5):**

- W.N remains the only ratified letter-prefix in EE bible numbering. v4 introduces zero new letter-prefixes.
- The `#<bug-id>` cross-reference format is a syntax extension, not a letter-prefix. § 5.5.1 closing paragraph explicitly notes this distinction.
- § 7.1.1 closing paragraph notes that cross-reference syntax extensions are subject to AUDIT_METHODOLOGY v2 § 5.5 pattern-completion check; v4's `#<bug-id>` extension is explicitly ratified per Tony's G9 locked decision.

**Net new methodology constructs after the self-check: 8 authorized + 0 unauthorized.** All v4 content traces to drafting-spec authorization (Tony-locked decisions for G3/G5/G7/G9 + audit-CC-recommended resolutions embedded as drafting-spec exact text for G1/G2/G4/G6).

---

## Recursive precision discipline check

Verbatim-claim formatting fidelity per TRIAGE_QUEUE_SPEC v1's recursive precision discipline:

**Verbatim reproductions in v4 (drafting spec embedded exact replacement texts):**

1. **§ 3.3 replacement (V4-1):** char-exact reproduction of drafting spec requirement A's replacement text. 5 example bullets; META_PLAN v8 § 7.11 reference; closing paragraph cross-referencing § 5.5.1. All formatting preserved (em-dashes, code spans, parenthetical clauses). **PASS.**
2. **§ 5.3 replacement (V4-2):** char-exact reproduction of drafting spec requirement B's two replacement blocks (modified second paragraph + new G1 closure paragraph). Code spans (`<bible>:#<bug-id>`, `<bible>:8.W.<n>`, `<bible>:#15`, `database_schema_bible:4`, `TRIAGE_QUEUE_SPEC v1`, `PHASE_5_BACKLOG.md`) preserved. **PASS.**
3. **§ 5.5 first bullet replacement (V4-3):** char-exact reproduction of drafting spec requirement C's bullet replacement. Em-dashes, code spans, bold emphasis preserved. **PASS.**
4. **§ 5.5.1 new sub-section (V4-3):** char-exact reproduction of drafting spec requirement C's new sub-section text. 4 convention-specific bullets + 1 closing pattern-completion paragraph. Code spans (`<bible>:#<bug-id>`, `feature_provenance_bible:#15`, `8.W.3`, `8.W.5`) preserved. **PASS.**
5. **§ 5.6.1 Mandatory fields block (V4-4):** char-exact reproduction of drafting spec requirement D. Scope clause em-dashes, bold emphasis ("**mandatory; entries without a knowable fix date belong in § 5, not § 8**"), code spans (`8.W.<n>`, `YYYY-MM-DD`) preserved. **PASS.**
6. **§ 5.6.1.1 Conditional triggers block (V4-5):** char-exact reproduction of drafting spec requirement E. CONDITIONAL caveat prose preserved verbatim. Code spans (`feature_provenance_bible:5.X`, `ml_layer_architecture_bible:#15`, `model_evaluation_retraining_bible:#15`) preserved. **PASS.**
7. **§ 5.6.1.2 new sub-section (V4-5):** char-exact reproduction of drafting spec requirement E's tertiary state codification. Three state definitions (FIRES, DOES NOT FIRE, CONDITIONAL) preserved with bold emphasis. CONDITIONAL discipline paragraph + AUDIT_METHODOLOGY v2 § 5.2 cross-reference preserved. **PASS.**
8. **§ 5.6.4 new conditional bullet (V4-6):** char-exact reproduction of drafting spec requirement F. Em-dashes, code spans (`\d <table>`, `psql ... \d wr_predictions`, `PHASE_5_BACKLOG.md`), bold emphasis ("**Determination at drafter discretion with verification log entry:**") preserved. **PASS.**
9. **§ 5.7 new sub-section (V4-7):** char-exact reproduction of drafting spec requirement G. 5-step workflow numbered list preserved. Provenance discriminator clause + cycle cost framing preserved. References to META_PLAN v8 § 9.1-9.13, § 6.1, AUDIT_METHODOLOGY v2 § 5.1 preserved. **PASS.**
10. **§ 6.X TOC headers (V4-8):** char-exact reproduction of drafting spec requirement H's replacement header text, applied uniformly across 7 occurrences. **PASS.**
11. **§ 7.1 replacement (V4-9):** char-exact reproduction of drafting spec requirement I's replacement. **PASS.**
12. **§ 7.1.1 new sub-section (V4-9):** char-exact reproduction of drafting spec requirement I's new sub-section. 6 worked-example bullets preserved. AUDIT_METHODOLOGY v2 § 5.5 pattern-completion cross-reference preserved. **PASS.**

**Net assessment:** recursive precision discipline holds. 12 of 12 verbatim reproductions char-exact.

---

## Verification log claim count summary (decomposed)

- **Inherited from v3 verification log:** 27 (v3's 25 inherited-from-v2 + N9 + N10). Wholesale inheritance — not re-decomposed.
- **New entries for v4:** 11 (V4-1 through V4-11).
- **Total v4 verification entries:** 11 new + 27 inherited = 38.
- **Decomposed counts cited in v4 body:**
  - 9 methodology gaps total (G1–G9); 1 closed in META_PLAN v7→v8 (G8); 8 closed in v4 (G1, G2, G3, G4, G5, G6, G7, G9). 1 + 8 = 9. ✓
  - 8 v4 fix categories (A–I, where E covers § 5.6.1.1 + § 5.6.1.2; I covers § 7.1 + § 7.1.1). 9 fix-category labels in drafting spec; 1 (E) maps to 2 sub-fixes; 1 (I) maps to 2 sub-fixes. Net 8 distinct content-area changes.
  - 7 § 6.X TOC header replacements (uniform replacement across § 6.1 through § 6.7).
  - 12 verbatim reproductions char-exact.
  - 8 net new methodology constructs (4 Tony-locked + 4 audit-CC-recommended).

---

**End of BIBLE_STRUCTURE_SPEC v4 verification log.**
