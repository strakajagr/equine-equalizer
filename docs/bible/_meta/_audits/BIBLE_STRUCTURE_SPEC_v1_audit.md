# BIBLE_STRUCTURE_SPEC.md DRAFT v1 — ADVERSARIAL AUDIT

**Auditor:** CC (fresh session per META_PLAN v6 § 3.1 cycle)
**Audit-CC adversarial scope:** META_PLAN v6 § 6.2 six questions + Tony's locked checks A–H from the spec prompt
**Date:** 2026-05-04

---

## Summary verdict

**Revise + re-audit.** v1 has four MATERIAL findings (above Tony's < 5 threshold strictly, but two of them — § 4.2 justification structure and § 6.X mandatory/conditional structure — were pre-flagged in the spec prompt as MATERIAL likelihoods, expected) AND one methodology-interpolation finding (§ 5.5 F.N/C.N/D.N naming convention extension is CC-introduced beyond META_PLAN's ratified W.N pattern, violating the zero-tolerance bar). The methodology-interpolation finding is the lock-blocker — Tony's hard rule is zero, regardless of MATERIAL count.

The verification log is sound: re-verification of inherited and new claims against live state holds. No fabricated content. The factual substrate is solid; the methodology-interpolation issue and the structural gaps in justification + mandatory/conditional templates are revisable surgically.

---

## Verification log audit

I re-ran or spot-checked the following verification log entries:

**New claim spot-checks:**
- **N1 (DD bible TOC):** Re-read DD bible lines 9–32. v1's enumeration of 21 numbered sections (1 through 21 with one sub-section at 4.5) matches. ✓
- **N2 (filename collision):** `find /docs/bible/ -name "*.md"` returns Phase 0 documents under `_meta/` only; no collisions at `/docs/bible/architecture_overview.md` etc. ✓
- **N3 (META_PLAN v6 cross-references):** Sampled 10 cross-references including § 3.2.1, § 6.5, § 7.4, § 7.11, § 7.12, § 8.5, § 9.13, § 10.2, § 10.3, § 10.4. All resolve to actual sections in v6. ✓
- **N4 (intra-document cross-references):** Sampled § 5.3, § 5.5, § 7.4, § 12.2 forward references. All resolve to existing sections in v1. ✓
- **N5 (filename-to-working-hypothesis mapping):** Verified all seven filenames map to META_PLAN v6 § 3.2 working-hypothesis names with consistent semantic translation. ✓

**Inherited claim spot-checks:**
- **Claim 1 (Lambda count):** `aws lambda list-functions ... | wc -l` → 8. Decomposition 5 Active + 3 INACTIVE re-verified via per-function `get-function`. ✓
- **Claim 7 (model registry):** `curl /dashboard/metrics`, parse model_history. Total 88, active 45, inactive 43. ✓
- **Claim 9 (`get_active_model_by_type` signature):** Re-read `model_version_repository.py:100-115`. Function takes only `model_type: str`; SQL exact match. No `_and_style` variant exists. ✓

**Code references in templates re-verified:**
- `model/shared/data_loader.py:45` — `from shared.gonzo_features import ...` confirmed ✓
- `backend/services/feature_engineering_service.py:16` — `from model.shared.gonzo_features import ...` confirmed ✓
- `wr_inference_service.py:616-626` — calibration bypass comment block at 616-625 + `handicapping_probs = ranker_probs.copy()` at line 626 confirmed ✓
- `backend/repositories/model_version_repository.py:100` — `def get_active_model_by_type` confirmed ✓
- `backend/database/migrations/migrate.py` — file exists ✓
- `frontend/src/api/client.ts` — file exists ✓

**Verification-log-precision-rule self-application to v1:**
v1's main-body counts that are aggregable:
- "8 Lambdas, 5 Active + 3 INACTIVE" ✓ decomposed
- "13 EventBridge rules, 10 ENABLED + 3 DISABLED" ✓ decomposed
- "14 tables + 1 matview" ✓ decomposed
- "88 = 45 active + 43 inactive" ✓ decomposed (in § 6.4)
- "12 migration files" — referenced in § 6.6 as standalone count, NOT decomposed by sequence-uniqueness state. v6 Claim 5 documents "12 files; 11 unique sequence numbers; sequence 005 duplicated" but v1 § 6.6 § 6.1 says only "12 existing migration filenames (verified) listed inline." **Marginal precision-rule application — could be sharper but the decomposition is implicitly available via Claim 5 inheritance. MINOR.**
- "9 pages + 13 components" in § 6.7 — referenced as "9 pages (`frontend/src/pages/`)" and "13 components (`frontend/src/components/`)" without decomposed sub-categories. The dump §§ 7.1–7.2 has the per-page/per-component lists; v1 doesn't restate. Acceptable as a template-level referent but Phase 1 drafter must enumerate. Not a v1 finding.

Verification log is sound. No fabricated content found. No re-verification claim failed.

---

## Justification artifact structure check (Additional Check A)

**FINDING — MATERIAL (pre-flagged).** v1 § 4.2 provides one numbered prose paragraph per non-ML document (and per ML document, conflated). Each paragraph names the document and lists its content scope. Missing: the three required subheadings — "What questions does this document answer?", "What audience does it serve?", "What would break if it were merged with another document?"

Sample from v1 § 4.2 row 1 (Architecture Overview):
> "**Architecture Overview** — system topology at the runtime-context level (Lambda + ECS + Aurora + S3 + API Gateway), cross-runtime invariants, canonical objects shared across the system, the INDEX section that links all six other bibles."

This is a content scope, not a justification. There is no "questions" enumeration; the "audience" is implicit (any reader who needs the system map — but only stated in § 6.1 prose, not in § 4.2); and the "merge-cost analysis" is entirely absent.

Same gap repeats for Data Pipeline (#2), Database & Schema (#6), API & Frontend (#7). The four non-ML documents collectively have zero of the twelve required justification pieces (4 docs × 3 pieces = 12) in clearly-distinguishable form.

**Recommendation:** restructure § 4.2 as one numbered subsection per non-ML document, each with three explicit subheadings. Drop the conflation with ML documents (§ 4.2 should be non-ML-only; ML documents are governed by META_PLAN v6 § 3.2.1's three forcing functions and don't require the same merge-cost analysis since the floor is locked). Drafting spec gave Tony-ratified template; v1 should follow it.

---

## Mandatory/conditional template structure check (Additional Check B)

**FINDING — MATERIAL.** v1 § 6.1 through § 6.7 provide TOCs (numbered section list with sub-numbered items) and "Per-section content guidance" prose. The content guidance does NOT distinguish mandatory content from conditional content with named triggers.

Sample from v1 § 6.1 § 3.1 Lambda inventory guidance:
> "the 8 Lambda functions, decomposed as 5 Active + 3 INACTIVE per META_PLAN v6 § 2.3 (verified 2026-05-04). For each Lambda: name, memory, timeout, current State, last-modified date, the action(s) it dispatches. Cross-reference Data Pipeline Bible for the daily-flow that uses each Lambda."

This lists fields ("name, memory, timeout, ...") but does not label them mandatory vs conditional. There are no "if X, then Y" triggers identifying when conditional content applies.

The drafting spec's Tony-ratified worked example for the What Was Fixed entry pattern was:
- **Mandatory fields:** entry ID, bug name, fix date, symptom, root cause, fix, "why this entry exists" rationale.
- **Conditional fields:** if-fix-involved-migration, if-fix-invalidated-prior-content, if-fix-produced-Forbidden-Pattern, if-fix-touches-multiple-bibles.

v1's templates do not apply this structure consistently. Sample inspection across § 6.1 through § 6.7:
- § 6.1 Architecture Overview: prose lists, no mandatory/conditional split.
- § 6.2 Data Pipeline: prose lists, no mandatory/conditional split.
- § 6.3 Feature Provenance: § 4 row template enumerated as bullets, but no mandatory/conditional labels.
- § 6.4 ML Layer Architecture: prose lists, no mandatory/conditional split.
- § 6.5 Model Evaluation: prose lists with implicit "current state" framing, no mandatory/conditional split.
- § 6.6 Database & Schema: per-table guidance lists fields with implicit "where applicable" semantics for some (e.g., "approximate row count"), but conditions not named.
- § 6.7 API & Frontend: similar prose-list pattern.

**Recommendation:** restructure each § 6.X per-section guidance into a two-block format:
- **Mandatory:** [bullet list of always-required fields]
- **Conditional (with triggers):** [if-X-then-Y bullet list]

The What Was Fixed template (§ 5 Common Document Structure) should also be expanded to show the mandatory/conditional structure explicitly, since it is shared across all seven bibles.

---

## Canonical-home tiebreaker check (Additional Check C)

**FINDING — MATERIAL.** v1 § 5.3 says: "If determination is unclear, QB triages." No tiebreaker criteria. No explicit deferral to AUDIT_METHODOLOGY.md.

The drafting spec's pre-flagged audit expectation: this should defer to AUDIT_METHODOLOGY.md rather than resolve here, because resolving here would interpolate methodology Tony hasn't ratified.

v1 does neither: it neither resolves with criteria nor defers explicitly. The phrasing "QB triages" is a placeholder that imports judgment without scaffolding. Two QB sessions encountering the same cross-cutting bug could plausibly home it in different bibles, with no audit-checkable rule for which is correct.

**Recommendation:** add a one-sentence explicit deferral to v1 § 5.3 + § 7.4. Suggested language: "Tiebreaker criteria for canonical-home determination when 'most directly prevents recurrence' is ambiguous are deferred to AUDIT_METHODOLOGY.md (Phase 0 deliverable 3). Until that document locks, QB surfaces ambiguous cases to Tony for explicit ratification per META_PLAN v6 § 8.3 decision-deferral discipline."

This converts the placeholder into a tracked deferral and surfaces the resolution path. Cost: < 5 lines.

---

## Methodology-interpolation rule self-application (with v6's expanded scope and grandfathering)

**FINDING — METHODOLOGY-INTERPOLATION (lock-blocker per Tony's zero-tolerance bar).**

v1 § 5.5 introduces a unified naming convention:
- Forbidden Patterns: `<section>.F.<n>` (e.g., `5.F.1`)
- What Was Fixed: `<section>.W.<n>` (e.g., `18.W.1`)
- Common Mistakes: `<section>.C.<n>`
- Deprecated entries: `<section>.D.<n>`

**Verification of grandfathering status:** The W.N format IS authorized — META_PLAN v6 § 7.4 explicitly specifies `W.N: <Bug name or short description>` and § 7.11 commit-message convention uses `bible: data_pipeline_bible:18.W.7`. W.N is grandfathered/ratified.

The F.N, C.N, and D.N extensions are NOT in META_PLAN v6:
- META_PLAN v6 Appendix A.1 (Forbidden Pattern worked example) labels its example as `6.4 Multiple Simultaneously-Active Model Versions (locked 2026-05-XX)` — using a sub-section numeric ID (`6.4`), NOT `F.N`.
- META_PLAN v6 Appendix A.4 (Deprecated Field Tracker) labels its example `21.1 Legacy `predictions` table — superseded but still read` — using `21.1`, NOT `D.N`.
- META_PLAN v6 § 9.1–9.13 anti-patterns use `9.X` numeric subsections, NOT `C.N`.
- `grep -nE "F\.[0-9]|F\.<n>|D\.[0-9]|D\.<n>|C\.[0-9]|C\.<n>"` over META_PLAN v6 returns zero hits for F., C., or D. patterns; only W.N appears.

The F.N / C.N / D.N convention is a **CC-introduced naming-convention extension** of META_PLAN's W.N pattern. It is a methodology construct (it shapes how every Phase 1 bible numbers its discipline-rule entries; downstream commit messages, cross-references, and audit-CC verification rely on it) that Tony has not ratified.

Per META_PLAN v6 § 6.1 catch-all clause ("or other CC-prescribed methodology constructs that Tony has not explicitly ratified") and v6's expanded scope, this is a flaggable interpolation.

**Resolution options for QB to surface to Tony:**

- **Option A (preferred — preserves CC's pattern, formalizes ratification):** Tony ratifies the F.N / C.N / D.N extension explicitly in BIBLE_STRUCTURE_SPEC v2. Add to v2 § 12.2 as a fifth surfaced construct with the rationale "extends META_PLAN's W.N pattern to the four discipline-rule entry types for greppable cross-bible identifiers."

- **Option B (matches META_PLAN's existing convention):** drop the F.N / C.N / D.N extensions; use sub-section numeric IDs (e.g., a Forbidden Pattern at section 5 of the ML Layer Architecture Bible would be `ml_layer_architecture_bible:5.4`, not `ml_layer_architecture_bible:5.F.4`). The cross-reference convention from META_PLAN v6 § 7.11 is preserved.

- **Option C (hybrid):** keep W.N (already ratified) and use sub-section numeric IDs for F / C / D (matches META_PLAN A.1 / A.4 / § 9.X patterns).

Tony picks; QB revises in v2.

**Additional methodology-interpolation candidates checked (not flagged):**

- **§ 5.5 "Identifiers are stable across the bible's lifetime (renumbering breaks cross-references)":** stability is structurally required by META_PLAN v6 § 7.11's commit-message convention (which depends on stable identifiers to grep usefully). Faithful restatement, not interpolation.
- **§ 5.2 recommended TOC sections-1-4-vs-5-8 boundary:** explicitly framed as recommendation, not rule. CC-introduced organizational suggestion. Borderline; not flagged because § 5.2's "recommended, not mandatory" language matches META_PLAN v6's pattern for non-binding recommendations (§ 5.2 + § 8.2 of v1 use the same framing as the ratified drafting-order recommendation in § 8.2).
- **§ 7.2 "Identifiers are stable across the bible's lifetime" (restated):** same as § 5.5 above. Faithful.
- **§ 8.4 convergence test:** faithful restatement of META_PLAN v6 § 3.2.1.
- **§ 5.3 cross-cutting bug rule:** faithful from META_PLAN v6 § 7.4.

The four CC-self-surfaced items (filename casing, _bible suffix, drafting order, TOC ordering) are all ratified per the spec prompt's reference block. They are not flagged.

**Net methodology-interpolation findings (post-grandfathering):** **1** (§ 5.5 F.N / C.N / D.N extension).

---

## Question 1: Unverifiable claims / verification gaps

1. **§ 5.2 mandatory-section authority overreach.** v1 § 5.2 says: "The sections themselves are required because META_PLAN v6 § 7.3, § 7.4, § 7.5, § 7.6, § 7.7 specify them as part of bible discipline." Verification: META_PLAN v6 § 7.4 DOES explicitly say "Each bible document includes a 'What Was Fixed — Do Not Revert' section." But § 7.5 (Forbidden Patterns) and § 7.6 (Common Mistakes) and § 7.7 (Deprecated) are formats / cross-reference rules; they don't explicitly mandate per-document inclusion. § 7.3 is dated lock points (a discipline applied within sections, not a section itself). § 5.2's claim that § 7.3, § 7.5, § 7.6, § 7.7 "specify [these sections] as part of bible discipline" is an overreach. Only § 7.4 carries the explicit per-document mandate. **MINOR — sharpen the citation.**

2. **§ 5.3 W.N reference example uses 18.** v1 § 5.3 says: "the cross-referencing bibles' 'Currently Open' or 'Deprecated' sections cite the canonical W.N by `<bible>:18.W.N`." This hardcodes section 18 as the What Was Fixed location, but § 5.2's recommended TOC puts What Was Fixed at position 8. Internal contradiction (also flagged in Q4). **MATERIAL — see Q4 finding.**

3. **§ 6.7 "9 pages + 13 components" inheritance:** v1 verification log inherits from META_PLAN v6's references to dump §§ 7.1–7.2 for the page and component counts. The v1 verification log entry for these counts (referenced in § 6.7 anchor verifications) is implicit only — there is no explicit Claim N entry for "9 pages + 13 components" in either META_PLAN v6 or v1's verification log. This is a coverage gap: a count cited in v1 main body without an explicit verification log entry. **MINOR — add an inherited entry "9 pages + 13 components per dump §§ 7.1–7.2; not independently re-verified" or run the verification.**

4. **§ 6.5 "4 calibration scripts (`scripts/fit_*_calibrations.py`)":** v1 § 6.5 references "4 calibration scripts" as anchor verification surfaced from dump § 1. This is dump-only; no live verification. The dump entry says "4 calibration scripts (lean53, lean53_core, all, wp)" — but v1 doesn't restate the names and doesn't verify the script files exist at the time of v1 lock. **MINOR — verify file existence or mark explicitly as dump-inherited.**

5. **Filename-to-section-number consistency:** v1 § 5.5 cross-bible reference example uses `feature_provenance_bible:18.W.7`. § 6.3 (feature_provenance_bible) TOC has What Was Fixed at "18. What Was Fixed". § 6.1 (architecture_overview) TOC has What Was Fixed at "8. What Was Fixed". A reader following § 5.5's cross-reference pattern to architecture_overview's What Was Fixed would write `architecture_overview:18.W.N` (per the example) — but the actual section is at 8. Internal contradiction surfaced as ambiguity. **MATERIAL — see Q4.**

---

## Question 2: Scope gaps

1. **§ 4.2 missing three-piece justification structure.** Pre-flagged MATERIAL — see Justification artifact structure check above.

2. **§ 6.X templates missing mandatory/conditional structure.** Pre-flagged MATERIAL — see Mandatory/conditional template structure check above.

3. **§ 5.3 missing explicit deferral for canonical-home tiebreaker.** MATERIAL — see Canonical-home tiebreaker check above.

4. **§ 5 missing fully-worked What Was Fixed entry template with mandatory/conditional fields.** META_PLAN v6 Appendix A.3 has W.3 (Gonzo Sauce FE Single-Source Extraction) as a worked entry. v1 § 5.5 cites the format inheritance but does NOT restate or expand the mandatory/conditional structure. The drafting spec's Tony-ratified worked example (mandatory: entry ID / bug name / fix date / symptom / root cause / fix / rationale; conditional: if-migration / if-prior-content-invalidated / if-Forbidden-Pattern-produced / if-cross-bible) should appear in v1 as an extracted shared template that all seven bibles cross-reference. Currently it lives only by reference to META_PLAN A.3, which doesn't show the mandatory/conditional structure either. **MATERIAL — paired with finding above on mandatory/conditional structure.**

5. **§ 5 should extract shared templates more aggressively.** The drafting spec's expectation: "Section 5 'Common Document Structure' should extract templates that appear in multiple bibles (What Was Fixed, Forbidden Patterns, Common Mistakes, Deprecated, dated lock points) so per-document sections cross-reference rather than duplicate." v1 § 5.4 (lock dates) and § 5.5 (numbering) extract some shared discipline; v1 § 5 does NOT extract a shared "Forbidden Patterns format" template, "Common Mistakes format" template, or "Deprecated entry format" template. Per-document templates (§ 6.X) reference META_PLAN v6 § 7.5 / § 7.6 / § 7.7 directly rather than a shared § 5 template. This is acceptable if META_PLAN's formats are stable, but it forces every Phase 1 drafter to read META_PLAN at draft time rather than reading the spec's extracted summary. **MINOR — § 5 could extract one-paragraph format summaries for FP/CM/Deprecated to reduce Phase 1 drafter context burden.**

6. **§ 8.4 convergence test missing per-bible audit success criteria.** v1 § 8.4 says specific success criteria are deferred to CONVERGENCE_CRITERIA.md. v1 does NOT mention success criteria for individual bible audits (separate from the convergence test for the inventory). META_PLAN v6 § 11 has Tony's threshold (< 5 MATERIAL findings, zero fabricated, zero methodology-interpolation) — applies to per-bible audit. Acceptable inheritance, but v1 § 8.3 step 6 says only "iterate until locked (Tony's threshold per META_PLAN § 11)" without restating the threshold. **MINOR — restate the threshold explicitly in § 8.3 step 6 for paste-ready clarity, OR confirm Phase 1 audit-CC prompts will carry it via § 6.2.**

7. **§ 10 Open Questions could close more.** § 10.5 (Phase 1 audit cadence per bible) is deferred to Phase 5 working agreements per the META_PLAN v6 § 7.13 deferral pattern. § 10.1 (drafting order) is recommended-not-locked. § 10.2 / § 10.3 / § 10.4 are resolved. v1 settled three of five; the remaining two are appropriately scoped as deferrals. Not a finding; positive note.

---

## Question 3: Ambiguous language

1. **§ 5.2 "the boundary" between sections 4 and 5.** v1 § 5.2 says: "The recommendation is that sections 1, 2, 3, 4 establish the domain and its canonical shapes; sections 5, 6, 7, 8 capture the discipline + the bug-history + the deprecated state. Reordering across that boundary is unusual; reordering within either group is fine when locality of reference is improved." "Unusual" is judgment-dependent; "boundary" is metaphorical. Two CCs given the same template could plausibly disagree on whether moving a domain-specific section from position 4.X to position 5.0 crosses "the boundary" — is 4.5 "Migration Discipline" within group 1-4 or crossing? **MINOR — sharpen wording or drop the recommendation.**

2. **§ 5.3 "QB triages when unclear."** Already flagged in Canonical-home tiebreaker check. Material.

3. **§ 5.5 numbering convention scoping ambiguity.** v1 § 5.5 says: "Forbidden Patterns are numbered as `<section>.F.<n>` (e.g., `5.F.1`, `5.F.2` within section 5 of a given bible)." Question: does this mean Forbidden Patterns ALWAYS live in a section dedicated to Forbidden Patterns (so § 5 is THE Forbidden Pattern section), OR can FP entries live in domain-specific sections (so a Migration Discipline section at 4.5 could have `4.5.F.1`)? The example (`5.F.1`) implies "always section 5"; the phrasing "within section 5 of a given bible" implies a per-bible variable. Two readings. **MINOR — pin the convention or clarify it's per-bible variable.**

4. **§ 6.X "Per-section content guidance":** see Mandatory/conditional template structure check. The guidance items are prose-recommendation-shaped; whether each item is mandatory or conditional is ambiguous. **MATERIAL — already flagged.**

5. **§ 7.2 "Identifiers are stable" but no insertion rule.** What if a Phase 5 bible update needs to insert a new section between existing sections 4.5.1 and 4.5.2? v1 § 7.2 says "renumbering breaks cross-references" but doesn't say "use decimal extension (4.5.1 → 4.5.1, 4.5.1.1, 4.5.2)" or "append at end (4.5.1, 4.5.2, 4.5.3 → original 4.5.1, 4.5.2 stay; new becomes 4.5.5)." **MINOR — pin insertion rule or surface as Phase 5 working agreement deferral.**

6. **§ 12.2 "Verging on interpolation; surfaced rather than locked."** Post-ratification, this language reads as defensive. The four items are now ratified (per the spec prompt's reference block). v1 § 12.2 should be updated in v2 to reflect ratification rather than continue surfacing them as if pending. **STYLE — light revision in v2.**

---

## Question 4: Contradictions

### Internal

1. **§ 5.2 vs § 5.5 vs § 6.X — "What Was Fixed" section number inconsistency.** v1 § 5.2 recommended TOC puts What Was Fixed at position **8**: "8. What Was Fixed — Do Not Revert." § 5.5 example uses **18**: "section 18 if section 18 is What Was Fixed" and cross-bible reference example `feature_provenance_bible:18.W.7`. Per-document templates split:
   - § 6.1 architecture_overview.md TOC: "8. What Was Fixed" (matches § 5.2)
   - § 6.2 data_pipeline_bible.md TOC: "8. Deprecated" then "18. What Was Fixed" (jumps from 8 to 18; matches § 5.5)
   - § 6.3 feature_provenance_bible.md TOC: "18. What Was Fixed" with "10. Deprecated" (matches § 5.5)
   - § 6.4 ml_layer_architecture_bible.md TOC: "18. What Was Fixed" (matches § 5.5)
   - § 6.5 model_evaluation_retraining_bible.md TOC: "18. What Was Fixed" (matches § 5.5)
   - § 6.6 database_schema_bible.md TOC: "18. What Was Fixed" (matches § 5.5)
   - § 6.7 api_frontend_bible.md TOC: "18. What Was Fixed" (matches § 5.5)
   
   Six of seven templates use 18; § 6.1 uses 8; § 5.2 says 8. The number 18 originates from DD bible § 18 (DD's What Was Fixed section number) but DD has 21 sections in a single file; EE bibles have ~8–10 sections each, so position 18 is structurally impossible (or requires huge gap-jumping). **MATERIAL — pick one canonical position for What Was Fixed across all bibles and apply consistently. Recommendation: position 8 (matching § 5.2's recommended TOC; abandon the DD-imported 18) since EE bibles are smaller documents than DD's single 21-section file.**

2. **§ 4.1 / § 4.2 mismatch on document type column.** § 4.1's table has 4 columns including "Type" (ML / Non-ML). § 4.2 then conflates ML and non-ML in a single numbered list (1 through 7 with no separation between ML rows 3-5 and non-ML rows 1-2 / 6-7). The drafting spec's Q1 was specifically about non-ML documents needing the three-piece justification. Conflation makes it unclear which rows of § 4.2 carry the justification-artifact obligation. **MINOR (paired with the MATERIAL § 4.2 finding) — separate non-ML and ML in v2.**

3. **§ 5.5 example identifiers vs § 5.2 boundary.** § 5.5 example: "5.F.1, 5.F.2 within section 5 of a given bible." § 5.2 says section 5 is "Discipline rules — Forbidden Patterns + Common Mistakes for this domain." So Forbidden Patterns at section 5 makes sense per § 5.2's recommended TOC. But § 5.5 also says What Was Fixed is at section 18 (per the example) — § 5.2 puts it at 8. Numbering scheme can't be both consistent with § 5.2 AND with § 5.5's section-18 example. **Same as finding 1; flagged jointly.**

### External

4. **v1 § 5.2 cites META_PLAN § 7.3, § 7.4, § 7.5, § 7.6, § 7.7 as authority for required sections.** Verification: META_PLAN v6 § 7.4 explicitly mandates per-document inclusion of What Was Fixed. § 7.3, § 7.5, § 7.6, § 7.7 are formats / discipline rules; they don't explicitly mandate per-document presence. v1 § 5.2's claim is overreach. **MINOR — sharpen.**

5. **v1 § 6.7 dump § 6.5 reference verified.** Dump § 6.5 is "API Gateway v2" with the per-domain route listing. v1 § 6.7 § 3.2 says "Per-domain route count (Shared / Generic predictions / WR / PL / LS — per dump § 6.5)" — this matches dump structure. ✓ Not a finding.

6. **v1 § 5.5 cites "META_PLAN v6 § 7.4 + Appendix A.3" for What Was Fixed format.** Verification: META_PLAN v6 § 7.4 specifies the W.N format with mandatory fields (Symptom / Root cause / Fix / Why this entry exists). Appendix A.3 (W.3 Gonzo Sauce FE Single-Source Extraction) shows a worked entry. ✓ Faithful.

7. **v1 § 5.5 cites "META_PLAN v6 § 7.5 + Appendix A.1" for Forbidden Pattern format.** Verification: META_PLAN v6 § 7.5 specifies "Format follows § 7.3 (dated lock point + rationale + FORBIDDEN/CORRECT pair)." Appendix A.1 (6.4 Multiple Simultaneously-Active Model Versions) shows a worked Forbidden Pattern. ✓ Faithful.

---

## Question 5: Rushed sections

1. **§ 4.2 one-line summaries.** Pre-flagged MATERIAL.

2. **§ 5.3 cross-cutting bug rule with no tiebreaker.** Pre-flagged MATERIAL.

3. **§ 5.5 numbering convention.** Compresses what could be a substantive shared template into 8 lines. Specifically: the F.N / C.N / D.N extensions are introduced in a bullet list without explanation of why this convention vs META_PLAN's existing patterns. Methodology-interpolation finding (above) is the dominant issue, but the section is also rushed in that it doesn't explain the design choice. **MINOR — paired with methodology-interpolation finding.**

4. **§ 6.X per-section content guidance varies in depth.** § 6.3 (Feature Provenance) has substantive per-feature row template with field list. § 6.5 (Model Evaluation) has thinner guidance — § 5 Calibration discipline guidance just lists "the calibration-fitting code paths surfaced from dump § 1 (`scripts/fit_*_calibrations.py` — 4 calibration scripts)" without telling Phase 1 drafter what fields per script to record. Inconsistent depth across templates. Phase 1 drafters working in parallel could produce different content depths because the spec doesn't level the depth bar. **MINOR — level depth guidance in v2.**

5. **§ 8.3 per-bible cycle compresses META_PLAN § 3.1's locked workflow into 7 numbered steps.** Faithful, but does not call out the verification log requirement explicitly per step. § 8.3 step 2 says "CC drafts + verification log" but doesn't restate that drafts without verification logs are rejected by QB without audit (META_PLAN v6 § 6.5 hard rule). **MINOR — restate the hard rule for paste-ready clarity.**

---

## Question 6: Missing examples

1. **§ 5 missing fully-worked What Was Fixed entry.** META_PLAN v6 Appendix A.3 has W.3. v1 § 5 references it but doesn't restate. For mandatory/conditional clarity, v1 § 5 should include one fully-worked example showing all mandatory fields populated AND each conditional trigger evaluated (some firing, some not). **MINOR.**

2. **§ 6.X per-document templates missing a fully-worked example section per bible.** Each per-bible template provides TOC + content guidance + cross-references + anchor verifications. None provides a fully-worked example of one section as Phase 1 would draft it. The drafting spec didn't require this; it would help Phase 1 drafters but isn't gating. **MINOR — add one worked-section example per bible in v2 if Tony agrees.**

3. **§ 7.2 section identifier discipline missing renumbering example.** Already flagged Q3 (5). **MINOR.**

4. **§ 8.4 convergence test missing pass/fail example.** v1 § 8.4 says "the test asks: given this bible's content, can a fresh CC session evaluate, rebuild, or retrain a model?" without showing what an example pass output vs fail output would look like. Deferring to CONVERGENCE_CRITERIA.md is reasonable; v1 could note the deferral explicitly. **MINOR — already noted in § 8.4 prose but could be sharper.**

---

## Additional adversarial findings

### F. § 13 changelog accuracy

v1 § 13 is a placeholder. Acceptable for v1.

### G. § 11 lock status vs Phase 0 exit prerequisites

v1 § 11 says "Phase 0 prerequisites carried over from META_PLAN v6 § 11: unchanged." META_PLAN v6 § 11 enumerates five prerequisites. v1 § 11 does not restate them. Per the verification-log-precision principle (broadly applied), the prerequisites should be re-listed for paste-ready clarity. **MINOR — restate in v2.**

### H. Cumulative MINOR weight

This is v1; no carry-over. Net MINOR count from this audit: see severity table.

### I. Verification log v1 has 25 claims = 20 inherited + 5 new.

Adequate for a Phase 0 deliverable 2 of 5. Coverage gap: the "9 pages + 13 components" reference in § 6.7 has no explicit verification log entry (Q1 finding 3). **MINOR.**

### J. § 6.X anchor verification listings are useful but inconsistent.

§ 6.1 lists 7 anchor claims; § 6.7 lists 2; § 6.5 lists "(per dump §§ 7.1, 7.2; Phase 1 re-verifies)" ambiguously. Consistency across § 6.X anchor verification subsections would help audit-CCs at Phase 1. **MINOR.**

---

## Severity assessment

| # | Finding | Section ref | Severity |
|---|---|---|---|
| 1 | § 4.2 missing three-piece justification structure | § 4.2 | **MATERIAL** |
| 2 | § 6.X templates missing mandatory/conditional structure with named triggers | § 6.1–6.7 | **MATERIAL** |
| 3 | § 5.3 canonical-home tiebreaker has no explicit deferral to AUDIT_METHODOLOGY | § 5.3 | **MATERIAL** |
| 4 | § 5.2 vs § 5.5 vs § 6.X "What Was Fixed" section number inconsistency (8 vs 18) | § 5.2, § 5.5, § 6.X | **MATERIAL** |
| 5 | § 5.5 F.N / C.N / D.N naming convention extension is CC-introduced beyond META_PLAN's W.N pattern | § 5.5 | **METHODOLOGY-INTERPOLATION** (lock-blocker) |
| 6 | § 5.2 mandatory-section authority overreach (§ 7.5, § 7.6, § 7.7 don't explicitly mandate per-document) | § 5.2 | MINOR |
| 7 | § 6.7 "9 pages + 13 components" lacks explicit verification log entry | § 6.7 | MINOR |
| 8 | § 6.5 "4 calibration scripts" is dump-only, not live-verified | § 6.5 | MINOR |
| 9 | § 5.2 "the boundary" between sections 4 and 5 is judgment-dependent | § 5.2 | MINOR |
| 10 | § 5.5 numbering convention scoping (always section 5? or per-bible variable?) ambiguous | § 5.5 | MINOR |
| 11 | § 7.2 missing insertion rule (decimal extension vs append-at-end) | § 7.2 | MINOR |
| 12 | § 4.1 Type column conflated with § 4.2 mixed-list treatment | § 4.1, § 4.2 | MINOR |
| 13 | § 5 missing extracted shared format templates for Forbidden Patterns / Common Mistakes / Deprecated | § 5 | MINOR |
| 14 | § 8.3 step 2 doesn't restate the verification-log hard rule | § 8.3 | MINOR |
| 15 | § 5 missing fully-worked What Was Fixed example with all mandatory + conditional fields | § 5 | MINOR |
| 16 | § 6.X content guidance depth inconsistent across templates | § 6.3 vs § 6.5 | MINOR |
| 17 | § 7.2 missing renumbering/insertion example | § 7.2 | MINOR |
| 18 | § 8.4 missing convergence test pass/fail example | § 8.4 | MINOR |
| 19 | § 11 lock status doesn't restate META_PLAN v6 § 11 prerequisites | § 11 | MINOR |
| 20 | § 6.X anchor verification subsections inconsistent in coverage | § 6.X | MINOR |
| 21 | § 12.2 "verging on interpolation" language defensive post-ratification | § 12.2 | STYLE |

---

## Material findings count

**MATERIAL: 4** (§ 4.2 justification structure, § 6.X mandatory/conditional structure, § 5.3 canonical-home tiebreaker, § 5.2/§ 5.5/§ 6.X What Was Fixed numbering inconsistency).

Tony's threshold of < 5 MATERIAL is met by count alone. However, two are pre-flagged in the spec prompt as expected MATERIAL findings (§ 4.2 + § 6.X) — they are not surprises but they are also not pre-resolved. v2 is required to address them.

The lock-blocker is the single methodology-interpolation finding, not the MATERIAL count.

---

## Fabricated-content findings

**0.** Verification log spot-checks held; new claims (N1–N5) re-verified live; inherited claims re-verified against original commands with values unchanged. No fabricated EE-codebase claim found.

---

## Methodology-interpolation findings

**1.** § 5.5 F.N / C.N / D.N naming convention extension. CC introduced unified entry-ID format extending META_PLAN v6's ratified W.N pattern to three additional discipline-rule entry types (Forbidden Patterns as F.N, Common Mistakes as C.N, Deprecated as D.N). META_PLAN v6 uses sub-section numeric IDs (e.g., 6.4 for FP, 21.1 for Deprecated, 9.X for Common Mistakes-style anti-patterns) — not the F./C./D. convention. CC-introduced; not Tony-ratified.

Per Tony's zero-tolerance bar on methodology interpolation post-grandfathering, this finding alone blocks v1 lock until either (a) Tony explicitly ratifies the F.N / C.N / D.N extension in BIBLE_STRUCTURE_SPEC v2's spec, or (b) v2 drops the extension and falls back to META_PLAN's existing sub-section numeric ID convention.

---

## Recommendation

**Revise + re-audit (v2).**

v2 must:

1. **Restructure § 4.2** as four numbered subsections (one per non-ML document), each with three explicit subheadings: questions answered / audience / merge-cost analysis. Apply the Tony-ratified template literally.

2. **Restructure § 6.1 through § 6.7 per-section content guidance** into mandatory + conditional blocks with named triggers, mirroring the Tony-ratified What Was Fixed worked example.

3. **Resolve § 5.3 canonical-home tiebreaker** by adding an explicit deferral to AUDIT_METHODOLOGY.md (one sentence, < 5 lines).

4. **Resolve "What Was Fixed" section number inconsistency** by picking one canonical position across all bibles (recommend: position 8 per § 5.2's recommended TOC; abandon the DD-imported position 18). Update § 5.2, § 5.5, and all § 6.X TOCs to match.

5. **Resolve § 5.5 F.N / C.N / D.N methodology-interpolation finding** by either (a) surfacing to Tony for explicit ratification with the rationale in BIBLE_STRUCTURE_SPEC v2 § 12.2, or (b) dropping the extension and using sub-section numeric IDs throughout (matches META_PLAN's existing convention).

6. Address MINOR findings opportunistically. The MINORs are surgical; QB can batch them with the MATERIAL revisions.

After v2 lands, re-audit with the same six-question scope plus the same five additional checks. Tony's threshold for v2 lock: < 5 MATERIAL, zero fabricated, zero methodology-interpolation.

The factual substrate is solid. The structural gaps are revisable. The methodology-interpolation finding is the single hardest decision (Tony's call between Option A ratify, Option B drop, Option C hybrid). v2 is achievable in 1–2 cycles.
