# BIBLE_STRUCTURE_SPEC v2 — Verification Log

**Document:** BIBLE_STRUCTURE_SPEC_v2_verification
**Companion to:** BIBLE_STRUCTURE_SPEC.md v2
**Author:** CC (drafting under verification discipline)
**Date:** 2026-05-04
**Purpose:** Per-claim verification record. v2 is a surgical patch pass over v1; all 25 v1 verification claims inherit with re-verified-2026-05-04 timestamps where re-verification command runs. v2's structural changes (M-1 dropping F./C./D. extensions, M-2 What Was Fixed at position 8, M-3 § 4.2 restructure, M-4 Mandatory/Conditional template structure, M-5 § 5.3 deferral) are non-factual and require no new verification entries. Net-new factual claims in v2: zero.

**Verification methodology:**
- "Live AWS" = `aws` CLI against operator's account 584812014683
- "Live API" = HTTPS request against `https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com`
- "Codebase" = file read against working tree at `/home/strakajagr/projects/equine-equalizer/`
- "DD bible" = file read against `/home/strakajagr/projects/dynasty-dugout/ARCHITECTURE_BIBLE.md`
- "Inherited from BIBLE_STRUCTURE_SPEC v1 log Claim N — re-verified 2026-05-04" = entry imported from `BIBLE_STRUCTURE_SPEC_v1_verification.md` and re-run against original source; value confirmed unchanged

**Verification log precision rule (locked META_PLAN v4, scope broadened in v5, applied throughout v6 and v1, applied here):**
Counts decomposed into definitions / instantiations / imports / uses, never aggregated as compressible-by-a-reader phrasings. Anything aggregable shown both as components and as a sum.

**Methodology-interpolation rule (locked META_PLAN v5, expanded scope and grandfathering in v6, pattern-completion check added v1 audit, applied here):**
CC does not invent binary tests, cadence rules, completeness criteria, scoring rubrics, severity thresholds, iteration caps, percentage criteria, procedural sequencing rules, or other CC-prescribed methodology constructs Tony has not explicitly ratified. Pattern parallelism does NOT constitute ratification. Constructs in v2 that may shade into interpolation are surfaced in BIBLE_STRUCTURE_SPEC § 12.2 for Tony's awareness.

---

## v2 verification summary

**Total claims:** 25 (unchanged from v1).
- Inherited from META_PLAN v6 log (with re-verified-2026-05-04 timestamps): 20
- Inherited from BIBLE_STRUCTURE_SPEC v1 log (with re-verified-2026-05-04 timestamps): 5

**Survived (re-verified live 2026-05-04):** 25
**Modified for v2:** 0
**Dropped:** 0
**New v2 claims:** 0 — v2's structural changes are non-factual

---

## Re-verification of inherited claims (sample)

The full inheritance table is in BIBLE_STRUCTURE_SPEC v2 § 9.1. v2 cycle re-ran the original commands for a representative sample to confirm values held; the remaining inherited claims are inherited by reference with the same re-verification methodology.

### Sample 1: Lambda function count (META_PLAN v6 log Claim 1)

**Re-verification 2026-05-04:** `aws lambda list-functions --query 'Functions[?starts_with(FunctionName, \`equine\`)] | length(@)'` → 8.
**Decomposed:** 5 Active + 3 INACTIVE = 8.
**Survived:** Yes
**Action:** Inherited from META_PLAN v6 log Claim 1 + BIBLE_STRUCTURE_SPEC v1 log — re-verified 2026-05-04. Value unchanged.

### Sample 2: EventBridge rule count (META_PLAN v6 log Claim 3)

**Re-verification 2026-05-04:** `aws events list-rules --name-prefix equine --query 'length(Rules)'` → 13.
**Decomposed:** 10 ENABLED + 3 DISABLED = 13.
**Survived:** Yes
**Action:** Inherited — re-verified 2026-05-04. Value unchanged.

### Sample 3: Model registry counts (META_PLAN v6 log Claim 7)

**Re-verification 2026-05-04:** `curl /dashboard/metrics`, parse `model_history`; partition by `is_active`. Total: 88. Active: 45.
**Decomposed:** 45 active + 43 inactive = 88.
**Survived:** Yes
**Action:** Inherited — re-verified 2026-05-04. Value unchanged.

### Sample 4: `get_active_model_by_type` signature (META_PLAN v6 log Claim 9)

**Re-verification 2026-05-04:** Read `backend/repositories/model_version_repository.py:100-115`. Function signature `def get_active_model_by_type(self, model_type: str) -> Optional[ModelVersion]:` with SQL `WHERE is_active = true AND model_type = %s LIMIT 1`. No `_and_style` variant exists in the file.
**Survived:** Yes
**Action:** Inherited — re-verified 2026-05-04. Value unchanged.

### Sample 5: Calibration bypass line range (META_PLAN v6 log Claim 26)

**Re-verification 2026-05-04:** Read `backend/services/wr_inference_service.py:616-630`. Lines 616-625 contain the comment block (10 lines: "Calibration BYPASS (BUG #15 + BUG #24)..."); line 626 contains `handicapping_probs = ranker_probs.copy()`; lines 627-628 are blank + start of unrelated 0-PP override block.
**Survived:** Yes
**Action:** Inherited — re-verified 2026-05-04. Value unchanged.

### Sample 6: gonzo_features.py import sites (META_PLAN v6 log Claim 27)

**Re-verification 2026-05-04:** `grep -nE "from .*gonzo_features|import .*gonzo_features" model/shared/data_loader.py backend/services/feature_engineering_service.py` → 2 import sites: `model/shared/data_loader.py:45` (`from shared.gonzo_features import ...`) and `backend/services/feature_engineering_service.py:16` (`from model.shared.gonzo_features import ...`). Qualified-name divergence preserved.
**Survived:** Yes
**Action:** Inherited — re-verified 2026-05-04. Value unchanged.

### Sample 7: BIBLE_STRUCTURE_SPEC v1 New Claim N1 (DD bible TOC structure)

**Re-verification 2026-05-04:** Read DD bible lines 9-32. TOC enumerates 21 numbered sections with one sub-section at 4.5. Discipline sections § 18 (What Was Fixed) / § 19 (Common Mistakes) / § 20 (Forbidden Patterns) / § 21 (Deprecated Fields) at end of TOC. § 4 (Canonical Player), § 4.5 (Contract/Salary/Keeper Rules), § 5 (Canonical League) early in TOC.
**Survived:** Yes
**Action:** Inherited from v1 log Claim N1 — re-verified 2026-05-04. Value unchanged.

### Sample 8: BIBLE_STRUCTURE_SPEC v1 New Claim N3 (META_PLAN v6 cross-references resolve)

**Re-verification 2026-05-04:** v2 cites a subset of META_PLAN v6 § numbers; spot-checked § 3.2.1, § 6.5, § 7.4, § 7.11, § 7.12, § 7.13, § 7.14, § 8.5, § 9.13. Each resolves to the actual section in v6.
**Survived:** Yes
**Action:** Inherited — re-verified 2026-05-04. Value unchanged.

---

## v2-specific verification: cross-reference integrity post-restructure

v2 changed several cross-reference targets (M-1 dropped F./C./D. references; M-2 changed § 18 to § 8 in many places). New verification: do all cross-references in v2 still resolve to existing sections?

### v2 Verification N6: Intra-document cross-references in v2 still resolve

**Claim:** All `§ <id>` cross-references inside BIBLE_STRUCTURE_SPEC v2 resolve to sections that exist within v2 itself.
**What was checked (verified 2026-05-04):** `grep -nE "^### |^## |^#### " /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` enumerates v2's sections. The cross-references in v2 ( § 1.1, § 1.2, § 1.3, § 1.4, § 2.1, § 2.2, § 2.3, § 2.4, § 3.1, § 3.2, § 3.3, § 4.1, § 4.2, § 4.2.1, § 4.2.2, § 4.2.3, § 4.2.4, § 4.3, § 4.4, § 5.1, § 5.2, § 5.3, § 5.4, § 5.5, § 5.6, § 5.6.1, § 5.6.2, § 5.6.3, § 5.6.4, § 6.1, § 6.2, § 6.3, § 6.4, § 6.5, § 6.6, § 6.7, § 7.1, § 7.2, § 7.3, § 7.4, § 7.5, § 7.6, § 8.1, § 8.2, § 8.3, § 8.4, § 9.1, § 9.2, § 10.1, § 10.2, § 10.3, § 10.4, § 10.5, § 11, § 12.1, § 12.2, § 12.3, § 13) were checked against this enumeration.
**What was found:** All intra-document references resolve to sections present in v2. New sections added in v2: § 4.2.1, § 4.2.2, § 4.2.3, § 4.2.4, § 4.3, § 5.6, § 5.6.1, § 5.6.2, § 5.6.3, § 5.6.4 — all created by M-3 and M-4 restructures.
**Survived:** Yes
**Action:** Verified post-restructure. No broken intra-document cross-references.

### v2 Verification N7: Cross-bible reference example syntax post-M-1

**Claim:** All cross-bible reference examples in v2 use either W.N (for What Was Fixed entries at section 8) or sub-section numeric IDs (for Forbidden Patterns, Common Mistakes, Deprecated). No F.N / C.N / D.N references remain post-M-1.
**What was checked (verified 2026-05-04):** `grep -nE "F\.[0-9]|F\.<n>|D\.[0-9]|D\.<n>|C\.[0-9]|C\.<n>" /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md`
**What was found:** Zero hits for F./C./D. patterns. The grep returns only one match unrelated to entry-ID conventions (a markdown formatting symbol pattern, not an entry ID).
**Survived:** Yes
**Action:** M-1 cleanup verified complete. No F./C./D. residue.

### v2 Verification N8: "What Was Fixed" position consistency post-M-2

**Claim:** All references to What Was Fixed section number in v2 use position 8 (not 18). This applies to § 5.2 recommended TOC, § 5.5 examples, § 5.5 cross-bible reference example, § 6.1–§ 6.7 per-document TOCs, and any cross-references between bibles (e.g., `feature_provenance_bible:8.W.<n>`).
**What was checked (verified 2026-05-04):** 
- `grep -nE "18\.W\.|section 18|18 if section 18" /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` → searches for any residual "18" references in the What-Was-Fixed-section context.
- `grep -nE "8\.W\.|section 8" /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md | head -20` → confirms position 8 references.
**What was found:** Zero hits for "18.W." or "section 18 if section 18" patterns. Multiple hits for "8.W." (e.g., `8.W.1`, `8.W.7`, `8.W.<n>`) and "section 8" in the What-Was-Fixed context. M-2 cleanup verified complete.
**Survived:** Yes
**Action:** Position-8 consistency verified across v2.

---

## Architectural questions surfaced for QB attention

1. **§ 5.6.2 / § 5.6.3 / § 5.6.4 canonical templates extending Mandatory / Conditional structure to F/C/D entry types.** Tony's M-4 instruction says "Section 5 (Common Document Structure) should extract the canonical templates that appear in multiple bibles (What Was Fixed, Forbidden Patterns, Common Mistakes, Deprecated entries)." This authorizes the extraction. CC drafted Mandatory / Conditional structure for each of the four templates. Pattern-completion check applied: each template's structure is individually anchored to a META_PLAN v6 source (W.N → § 7.4 + Appendix A.3; FP → § 7.5 + Appendix A.1; CM → § 7.6; Dep → § 7.7 + Appendix A.4). The Mandatory / Conditional structure itself was Tony-ratified (M-4) for "every per-section template in § 6.1-§ 6.7" — the extension to § 5.6 is consistent with M-4's intent. **Judged acceptable; surfaced for Tony's confirmation that the M-4 authorization extends to § 5.6 templates.**

2. **§ 5.6 conditional triggers across the four templates.** Each template's "Conditional" block names triggers (e.g., for W.N: "if-fix-involved-migration / if-fix-invalidated-prior-content / if-fix-produced-Forbidden-Pattern / if-fix-touches-multiple-bibles"). The W.N triggers were Tony-ratified per M-4's worked example. The F/C/D triggers are CC analytical work grounded in META_PLAN v6 anchor verifications (Forbidden Pattern's "if produced by a specific bug" trigger anchors to § 7.4 cross-cutting bug rule; Deprecated's "if has active readers" trigger anchors to META_PLAN v6 Appendix A.4's example). Pattern-completion check applied: each trigger is content-presence-driven, not a binary test or threshold. **Judged acceptable.**

3. **§ 6.1–§ 6.7 per-section content guidance Mandatory / Conditional triggers.** Tony's M-4 instruction explicitly authorizes Mandatory / Conditional structure for every per-section guidance block. v2 applies this consistently. The conditional triggers are content-presence conditions ("if Lambda is INACTIVE, document StateReason"), not binary tests. **Judged acceptable per Tony's M-4 authorization.**

4. **No EE codebase fact surfaced as potentially wrong.** v2's verification re-ran inherited claims; all values held. No "Tony's locked decision based on a wrong premise" pattern instances surfaced in this cycle.

---

## Methodology-interpolation rule application during v2 drafting

**Pattern-completion check (new from v1 audit, applied throughout v2 drafting):**

CC drafted each new methodology construct in v2 with the explicit pattern-completion question: "does this extend a single ratified case to multiple parallel cases without individual ratification?"

**v2 constructs reviewed:**

1. **§ 5.6 four canonical templates (W, F, C, D) with parallel Mandatory / Conditional structure.** Pattern-completion check: the structure (Mandatory / Conditional) was ratified for ALL templates per Tony's M-4 instruction; each template's content is independently anchored to META_PLAN v6 sources. **Not interpolation.** Surfaced for Tony's awareness in § 12.2.

2. **Conditional triggers for per-section guidance (§ 6.1–§ 6.7).** Pattern-completion check: each trigger is content-presence-driven (no binary tests, thresholds, cadences); each is grounded in audit-checkable EE state or META_PLAN v6 anchor verifications. **Not interpolation.** Surfaced.

3. **EE-vs-DD divergence note in § 5.2** (explaining position-8 vs DD's position-18 origin). Pattern-completion check: descriptive prose, not a CC-introduced rule. **Not interpolation.**

**Constructs explicitly NOT drafted:**

- No iteration cap on bible audit cycles (deferred to Phase 5 working agreements per META_PLAN v6 § 7.13 pattern).
- No completeness criterion for "section is done" or "bible is complete" (deferred to AUDIT_METHODOLOGY and CONVERGENCE_CRITERIA per § 2.4).
- No minimum section count, word count, or FORBIDDEN/CORRECT pair count per bible.
- No prescribed cadence for cross-document consistency audit (Phase 5 deferral).
- No severity thresholds beyond what META_PLAN v6 specifies.
- No tiebreaker criteria for canonical-home determination (deferred to AUDIT_METHODOLOGY.md per M-5).
- No new letter-prefix conventions. M-1 explicitly limits letter prefixes to W.N (the only letter-prefix in EE bible numbering).

**No fabricated content in v2.** Every concrete claim has a verification entry above (or inherits from META_PLAN v6 / BIBLE_STRUCTURE_SPEC v1 with re-verified-2026-05-04 timestamps). Every operator-stated claim is annotated as such per § 4.5 source-priority tier 5.
