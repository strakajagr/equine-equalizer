# META_PLAN.md DRAFT v4 — ADVERSARIAL AUDIT

**Audit-CC session:** fresh CC, 2026-05-04
**Auditing:** META_PLAN.md draft v4 at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/META_PLAN.md`
**Companion verification log audited:** `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/_audits/META_PLAN_v4_verification.md`
**Verification substrate:** live AWS, live API, working tree, DD bible, operator memory file
**Threshold:** Tony's "< 5 MATERIAL findings AND zero fabricated-content findings" criterion

---

## Summary verdict

Lock after specific minor revisions. The fabrication path the v3 BLOCKER taught is structurally closed; no new fabricated content. v3's six MATERIALs are addressed. Four MATERIALs surface in v4, all surgical: scope of the verification-log-precision rule itself, Tier 1→3 migration trigger mechanics, Layer 1 checklist physical form, and Bug #28's "stable known" classification depending on an unverified backfill assumption. Threshold technically met (< 5 MATERIAL); the call between "lock with revisions" vs "revise + re-audit" is a judgment one — see Recommendation.

---

## Verification log audit

I re-ran 8 verification log claims against live state (focus: corrected Claim 16 + new claims 14b/15b/24/25/26/27 + updated Claim 22).

| # | Claim | Re-verified result | Holds up? |
|---|---|---|---|
| 16 | `prediction_router.py` reference count | `grep -n "PredictionRepository" backend/routers/prediction_router.py` → 4 lines: `:6:` import, `:34:`, `:61:`, `:92:` instantiations. v4 log decomposes "1 import + 3 instantiations = 4 references." | ✓ Decomposed accurately |
| 22 | working-tree count | `git status --porcelain \| wc -l` → 103. **Decomposition (NEW finding):** `git status --porcelain \| awk '{print $1}' \| sort \| uniq -c` returns `74 ??` (untracked) + `29 M` (modified) = 103. v4 § 1.1 / § 1.3 say "103 modified-or-untracked entries" without decomposing 74 untracked + 29 modified. | ✓ Number accurate; **precision-rule application incomplete — see C below** |
| 14b | DD canonical-object section numbers | `grep -nE "^## (4\\.|5\\.|10\\.)" /home/strakajagr/projects/dynasty-dugout/ARCHITECTURE_BIBLE.md` → L590 § 4 Player; L800 § 4.5 Contract/Salary/Keeper; L1365 § 5 League; L1657 § 10 Pricing | ✓ Lines and labels match. Footnote in log honestly notes the "Financial" framing is v4 prose's gloss over DD's literal "CONTRACT, SALARY, AND KEEPER" — disclosure is correct |
| 15b | Bug #28 silent-failure window | Read operator memory file: discovery 2026-05-03; last clean 2026-04-29; broken from 2026-04-30 → 2026-05-02 (3 dates). Window is 2026-04-30 → 2026-05-03 = 3 calendar days. v4 says "at least three days." | ✓ Lower-bound phrasing matches evidence |
| 24 | 14 Gonzo features | gonzo_features.py docstring at lines 19/21/24: Speed (4) / Trajectory (7) / Class (3); `grep "^def compute_gonzo"` returns 3 functions at lines 290, 400, 477 | ✓ 4+7+3=14 confirmed; 3 public functions confirmed |
| 25 | "three calibration bugs in one week" | gonzo_features.py docstring lines 7-11: "three distinct bugs this week traced to code-path drift between training and inference" | ✓ Verbatim in file |
| 26 | calibration bypass at lines 616-628 | Read lines 614-630 of `wr_inference_service.py`: comment block at 616-625; `handicapping_probs = ranker_probs.copy()` at 626; blank line 627; next comment block at 628 | ✓ "ALL styles" claim verified at line 617. **Minor imprecision:** the bypass itself spans 616-626; lines 627-628 are post-bypass (blank + next section). v4's "616-628" range is approximate, off by 2 lines on the upper bound. Not fabrication; mild scope inflation. |
| 27 | gonzo_features.py import sites | `grep "gonzo_features" model/shared/data_loader.py backend/services/feature_engineering_service.py` confirms `data_loader.py:45` uses `from shared.gonzo_features import (` while `feature_engineering_service.py:16` uses `from model.shared.gonzo_features import (` — different qualified names | ✓ Both forms recorded honestly in log |

**Net assessment of v4 verification work:** 8/8 spot-checked entries hold up. Two have soft-edges:

- **Claim 22 — precision-rule self-application gap.** v4 corrected v3's "28+ modified files" → "103 modified-or-untracked entries." But v4 didn't decompose into "74 untracked + 29 modified = 103." The same precision-rule that closed the BLOCKER is not applied here.
- **Claim 26 — line range slightly inflated.** Cited as 616-628; actual bypass is 616-626. Two-line scope inflation is not fabrication, but a Tier 3 verification log should hit exact line bounds.

**Verification-log-precision-rule self-application across v4 main doc:**

The rule (§ 6.5) reads: "Counts must be decomposed... Anything aggregable must be aggregated explicitly so a reader cannot compress with judgment."

Where v4 applies it correctly:
- A.4 prediction_router.py: "3 instantiations + 1 import = 4 references" ✓
- A.4 race_router.py: "1 instantiation, plus 1 import on line 273" — partial (no sum) ✗
- § 1.3 / § 2.3 Lambda: "8 total" + § 2.3 enumerates "Active (5)" and "INACTIVE (3)" ✓
- § 1.3 / § 2.3 EventBridge: "13 total, 3 disabled" + § 2.3 names all 3 disabled ✓
- § 9.11 + Claim 24: "14 = Speed (4) + Trajectory (7) + Class (3)" ✓

Where v4 applies it incompletely:
- § 1.1 / § 1.3: "103 modified-or-untracked entries" — should decompose to "74 untracked + 29 modified = 103." This is exactly the kind of phrase a downstream reader could compress ("103 modifications"). Same failure pattern as v3's "4 references including the import."
- § 1.3: "two parallel feature engineering implementations" — doesn't name them inline. § 9.11 names them, but the rule's compression-resistance test is satisfied only if no upstream reader can compress; cross-reference-only naming requires the reader to look up the cross-reference.
- § 1.3: "88 model registry entries (45 simultaneously active per live dashboard query)" — implies 43 inactive but doesn't state it. "88 = 45 active + 43 inactive" would be fully decomposed.
- A.4 race_router.py: gives "1 instantiation, plus 1 import on line 273" but doesn't sum. By the rule's own pattern from prediction_router.py ("= 4 references total"), this should also sum: "= 2 references total."

This is the substantive concern. v4 was supposed to internalize the rule. It internalized it for code-reference counts that Looked-like-the-v3-failure but not for non-code aggregations. Either the rule's scope is narrower than § 6.5's "anything aggregable" suggests (in which case § 6.5 should say so), or v4 is inconsistently applying its own rule (in which case v4 needs another sweep).

---

## v3 finding regression check

| v3 finding | v4 fix verified? | Notes |
|---|---|---|
| BLOCKER F1: A.4 inflated count | ✓ FIXED | A.4 reads "3 instantiations of `PredictionRepository` at lines 34, 61, 92, plus 1 import on line 6 = 4 references total." Decomposed and summed correctly. |
| MATERIAL #1: § 4.1 Tier 3 description | ✓ FIXED | All four Tier 3 rows (META_PLAN, BIBLE_STRUCTURE_SPEC, AUDIT_METHODOLOGY, TRIAGE_QUEUE_SPEC) read "(CC-drafted under QB spec, with verification log; CC-audited)." Matches § 6.5. |
| MATERIAL #2: SPEC_GAP/FRAMEWORK_GAP collision | ✓ FIXED | § 6.5 explicitly defines both with distinct scopes (whole-doc vs slot-level). A.7 references both with consistent definitions. The "use the more specific marker when both apply" instruction adds a judgment layer (see Question 3 below). |
| MATERIAL #3: § 7.10 same-working-session interpolation | ✓ FIXED | Sentence dropped from § 7.10. Searching v4: no occurrence of "same working session." § 6.1 CC role definition adds an explicit "does NOT silently extend Tony's locked answers" rule, capturing the lesson. |
| MATERIAL #4: Layer 1 + emergency hotfix interaction | ✓ FIXED | § 7.13 has explicit waiver subsection: 3 items waive at deploy (`git status clean`, `git log -1`, bible diff review); 2 items NOT waive (migration testing, commit message convention). Each marked with rationale. |
| MATERIAL #5: enforcement-failure recovery cadence | ✓ FIXED | § 7.13 contains Tony's verbatim deferral language to Phase 5 working agreements. |
| MATERIAL #6: § 8.5 AWS-vs-API global assertion | ✓ FIXED | § 8.5 deferral to Phase 1 API & Frontend Bible per-route documentation, scoped "where applicable" (only routes targeting INACTIVE Lambdas). |

**Verdict:** all 1 BLOCKER + 6 MATERIAL fixed cleanly. No regression. (Compare to v3's regression: v3 replaced one wrong A.4 example with another wrong count; v4 doesn't repeat the pattern.)

---

## Question 1: Unverifiable claims / verification gaps

1. **§ 4.5 worked example for `equine-results` AWS-vs-DB resolution.** Tier 3 (DB) line says: `SELECT MAX(created_at) FROM results;` returns a timestamp from before the deactivation date. I cannot verify this without DB access. The example is framed as an analytical pattern ("Question asked of Phase 1 audit-CC..."), so it's illustrative — but a fresh CC reading § 4.5 might assume the timestamp claim is verified. No verification log entry covers it. Coverage gap.

2. **§ 7.5 second candidate Forbidden Pattern** ("Adding feature engineering logic to either `model/shared/data_loader.py` or `backend/services/feature_engineering_service.py` without parallel update to the other"). The two files ARE confirmed by Claim 27. But the pattern's premise — that drift between them silently produces calibration bugs — is asserted, not verified for that specific pattern. The premise traces to Claim 25's gonzo_features.py docstring "three distinct bugs this week," but that quote is the institutional memory; no log entry verifies the manual-cross-reference discipline as currently enforced.

3. **§ 9.13 sharpening — "three required pieces" claim.** v4 § 9.13 says "Removing any one converts the documentation back to the FORBIDDEN form." This is a methodology assertion (CC-prescribed), not factual claim. But it's stated as a rule. There's no verification log entry because there's nothing to verify — but the claim functions as a binary criterion on documentation acceptability. Tony hasn't ratified that the three-piece test is binary. CC interpolated this as the sharpening pattern. (Echo of v3 MATERIAL #3 lesson: CC extending methodology beyond what was specified.)

4. **§ 8.1 Bug #28 "stable known failure mode" classification depends on unverified backfill assumption.** v4 added the caveat: "backfill specifically depends on fetch_results re-run having access to the historical pages, which the Phase 1 Data Pipeline Bible audit will verify." Until that verification happens, the "stable known" classification rests on an unverified assumption. If backfill proves infeasible, Bug #28 would NOT qualify as stable known per § 8.1's criteria, and the observation-only exception logic shifts. The case study's worked-example status is therefore conditional in a way the document's prose doesn't fully signal.

5. **Verification log Claim 26 line-range imprecision.** v4 cites `wr_inference_service.py:616-628` for the calibration bypass. Live re-verification: the bypass comment block is lines 616-625; the actual bypass operation `handicapping_probs = ranker_probs.copy()` is line 626; line 627 is blank; line 628 begins the next comment block ("Patch (β): 0-PP override AFTER calibration"). The bypass-related range is 616-626, not 616-628. Not fabrication, but precision drift in a Tier 3 deliverable. Same wording carries through § 1.2, § 9.12, and A.2.

---

## Question 2: Scope gaps

1. **Verification-log-precision rule scope undefined.** § 6.5's rule says "Counts must be decomposed" and "Anything aggregable must be aggregated explicitly." The rule is silent on whether it applies to:
   - Code references only (its origin in the v3 BLOCKER)
   - Any count of categorized things (Lambda Active/Inactive, EventBridge enabled/disabled)
   - All counts including text-content aggregations (modified vs untracked files, train vs inference modules)
   
   v4's behavior implies "where compression is plausible" — but this is the drafter's judgment, which is exactly what the rule is supposed to constrain. The rule's scope is itself a methodology gap.

2. **§ 4.1 CONVERGENCE_CRITERIA Tier 1 conditional migration mechanics undefined.** v4 says: "Tier 1 status holds only if drafting confirms zero EE references — otherwise it migrates to Tier 3 per § 6.5's 'any document with verifiable EE-specific claims' rule." But:
   - When is "drafting confirms" decided — at spec time, draft start, mid-draft, post-draft?
   - If it migrates mid-draft, does the verification-log discipline apply retroactively to the prior text?
   - Does QB write a different spec for Tier 3, or augment the Tier 1 spec?
   
   Without these mechanics, CONVERGENCE_CRITERIA's drafting workflow has a hidden branch.

3. **§ 7.13 Layer 1 pre-deploy checklist physical form unspecified.** v4 carries v3's checklist verbatim. The format `- [ ] git status clean` etc. implies a written form. But no file path is specified. § 7.14 doesn't list a `.deploy-checklist.md` or equivalent. Layer 2 is dormant ("PR workflow out of scope for Phase 0"). Layer 3 only fires on bible-touching commits. Therefore Layer 1 IS the active enforcement — and its physical form is undefined. Tony's deploy ritual could be entirely mental, in which case "Tony confirms" reduces to "Tony remembers." This was a v3 MINOR (#13); on close re-read, given Layer 1 is the only active enforcement tier, it warrants MATERIAL.

4. **§ 6.5 "use the more specific marker when both apply" requires judgment.** SPEC_GAP vs FRAMEWORK_GAP: a slot whose unfillability *indicates* the spec was wrong from the start is ambiguous. CC has to decide whether the issue is whole-document or slot-level. The rule says "use the more specific" but specificity is itself a judgment. § 6.5 doesn't give a worked example of an ambiguous case.

5. **§ 8.5 deferral scope.** v4 says: "documented per route in the Phase 1 API & Frontend Bible." The next sentence: "Phase 1 audit's job includes mapping each of the 41 routes to its integration target and recording observed INACTIVE-target behavior **where applicable**." The "where applicable" clause limits the documentation requirement to routes-targeting-INACTIVE-Lambdas — but how is "applicable" determined? The Phase 1 audit does the route mapping, but until then we don't know which routes target INACTIVE Lambdas. Mild scope-of-work ambiguity for the Phase 1 audit task.

6. **§ 7.13 "bible-touching" determination is circular.** v4 § 7.13 Layer 3 says bible-touching is determined by commit message prefix per § 7.11's silence convention. § 7.11 says non-bible-touching commits omit the prefix. But what determines whether the prefix is added? The drafter's judgment. So a commit "touches the bible" iff the drafter says it does. The discipline depends on drafter honesty, not on a mechanical determination. Not a v4-introduced issue (v3 had this); not addressed in v4.

---

## Question 3: Ambiguous language

1. **§ 6.5 "Anything aggregable must be aggregated explicitly so a reader cannot compress with judgment."** What counts as "aggregable"? Two readings:
   - **Strict:** any count of multiple things — including "two parallel implementations," "103 modified-or-untracked entries."
   - **Permissive:** counts where compression has produced past errors — i.e., code-reference counts following the v3 BLOCKER pattern.
   
   v4's behavior is permissive; v4's stated rule is strict. Two readers could apply the rule differently to the same draft.

2. **§ 7.13 Layer 1 waiver "applies retroactively at the within-4-hours commit and within-24-hours bible entry."** Two retroactive deadlines, two separate events. The phrasing implies bible diff review happens twice retroactively — which it doesn't; it happens once, but the verification of "diff is reviewed" applies to both events. Awkward phrasing; a reader might interpret as "review the diff at the 4h commit AND review again at the 24h bible entry." Could be tightened to: "applies retroactively when the within-4-hours commit and within-24-hours bible entry land."

3. **§ 9.13 CORRECT pattern's three required pieces.** v4 names them: function + multi-active-row reality + missing style-aware variant. Then asserts: "Removing any one converts the documentation back to the FORBIDDEN form." A reader following v4 strictly might over-format every multi-active-row reference with all three pieces; a reader reading loosely might cite just the function + reality and consider the documentation acceptable. The binary form is itself a CC-interpolated discipline (§ 6.1 lesson — see Question 1 finding 3).

4. **§ 4.1 footnote** — "CONVERGENCE_CRITERIA's Tier 1 status holds only if drafting reveals it can be written without EE-specific factual claims." "Drafting reveals" is vague — does it mean "after a complete draft passes audit without EE references" (post-hoc) or "QB judges at spec time the document can be written without EE refs" (pre-hoc)?

5. **§ 6.1 CC role: "does NOT silently extend Tony's locked answers."** What constitutes silent extension vs legitimate elaboration? If Tony locks "test in non-prod DB first" and CC drafts "test in non-prod DB first; do not skip" — is the "do not skip" silent extension? § 6.1 captures the spirit but doesn't define the line. (See § 7.10's surviving "typically 3-5 per heavy session, not 20" — the boundary case.)

---

## Question 4: Contradictions

### Internal

1. **§ 6.5 verification-log-precision rule vs v4's actual application in § 1.1 / § 1.3.** Rule says "anything aggregable must be aggregated explicitly." Application: "103 modified-or-untracked entries" is aggregable (74 untracked + 29 modified) but not decomposed. The rule and its application in the same document disagree.

2. **A.4 paragraph internal inconsistency on decomposition format.** prediction_router.py decomposes and sums: "3 instantiations + 1 import = 4 references total." race_router.py decomposes but doesn't sum: "1 instantiation, plus 1 import on line 273." Either both should sum or neither. Per § 6.5's rule, both should sum.

3. **§ 7.10 Mechanics vs § 6.1 CC-doesn't-silently-extend.** § 7.10 still contains: "Commits SHOULD represent deploy-ready iteration states — typically 3–5 per heavy session, not 20." The "3–5 per heavy session, not 20" range is unsourced policy carried from v2/v3 unchanged. By the v4 lesson (§ 6.1), this is exactly the pattern of CC silently interpolating cadence policy that v4's Q1 demanded be removed. The "same working session" sentence was the egregious case; the "3-5 per heavy session" specification is the milder case still in the document. Either Tony has implicitly ratified by silence, or the lesson is half-applied.

4. **§ 11 "Phase 0 exit prerequisites" vs § 3.1 "Phase 0 exit criteria" — match.** Verified: both enumerate (a) all 5 documents pass adversarial audit, (b) convergence test, (c) baseline commit, (d) gitignore audit, (e) PHASE_5_BACKLOG.md created. ✓

5. **§ 12 changelog accuracy.** Spot-checked claims:
   - "§ 4.1 Tier 3 description synced to § 6.5" ✓
   - "<SPEC_GAP> vs <FRAMEWORK_GAP> distinction made explicit" ✓
   - "§ 7.10 'same working session' sentence dropped" ✓
   - "§ 7.13 Layer 1 emergency-hotfix waiver subsection added" ✓
   - "§ 7.13 enforcement-failure recovery replaced" ✓
   - "§ 8.5 AWS-vs-API rule rewritten narrowly" ✓
   - "§ 7.11 end-to-end commit-message example added" ✓
   - "§ 7.12 illustrative full migration example added" ✓
   - "§ 4.5 worked example for AWS-vs-DB conflict resolution added" ✓
   
   All claimed changes are present.

### External

6. **§ 3.1 edge case "Tony's locked decision based on a wrong premise"** vs Tony's verbatim ratification quoted in v3 verification log. v4 § 3.1 says: "v3 → v4: this happened with Q4; Tony ratified the reframing in the v4 cycle." Tony's verbatim from the v4 drafting spec: "Reframing is correct because facts on the ground decided it." The ratification claim matches the verbatim. ✓

---

## Question 5: Rushed sections

1. **§ 3.4 Phase 3 (Predictive Concept Inventory) and § 3.5 Phase 4 (Gap Analysis) still skeletal.** v3 audit flagged this as MINOR; v4 didn't develop further. On close re-read: META_PLAN's stated job is to provide "the cleanest possible separation between methodology (Phase 0) and substance (Phase 1)" (§ 1.5). Phase-2-onward specification depending on subsequent documents is consistent with that scope. Stays MINOR; not a v4 regression.

2. **§ 3.6 Phase 5 (Execution).** v4 added the "Phase 5 working agreements" deferral note. Acceptable — it's the same pattern as § 7.13's enforcement-failure recovery deferral. Both honestly defer rather than half-specify. OK.

3. **§ 4.1 CONVERGENCE_CRITERIA Tier 1 conditional.** v4's framing is honest but the migration mechanics aren't specified (Question 2 finding 2). This is on the edge between MINOR (defer to AUDIT_METHODOLOGY.md) and MATERIAL (the mechanics affect Phase 0 deliverable workflow).

4. **§ 7.13 Layer 1 pre-deploy checklist physical form.** Same item as Question 2 finding 3 — Layer 1 is the only active enforcement tier; its physical form being undefined is more material than v3 audit gave credit for.

5. **§ 9.13 binary three-piece test.** Sharpened well in v4, but the "Removing any one converts the documentation back to the FORBIDDEN form" assertion is CC-interpolated methodology (Question 1 finding 3, Question 3 finding 3). The sharpening exposed CC's methodology-extension habit even after v3's correction.

---

## Question 6: Missing examples

1. **§ 6.5 verification-log-precision rule — no worked example of the v3 → v4 lesson pattern.** A two-line example showing "v3 log entry: '4 references including the import' / v3 main doc inflation: '4 instantiations' / v4 log entry: '3 instantiations + 1 import = 4 references' / v4 main doc: '3 instantiations + 1 import = 4 references total'" would make the rule self-evidently scoped and applied. Without it, a future Tier 3 drafter has the rule but no concrete model.

2. **§ 6.5 SPEC_GAP / FRAMEWORK_GAP — disambiguation example missing.** The two markers each have a one-sentence example. Missing: an example of an ambiguous case where both could apply, with the resolution shown. Question 3 finding 1's risk is concrete: a future CC will hit a borderline case with no precedent.

3. **§ 7.13 Layer 1 emergency-hotfix waiver — no worked triage queue entry.** Specifying which items waive is good; showing what the resulting triage queue entry looks like is better. The PHASE_5_BACKLOG entry created at emergency-deploy time should have a canonical structure (what broke, what was deployed, why bypass, retroactive plan, which Layer 1 items waived). A.5 has a Bug #28 example but it's not an emergency-hotfix triage entry.

4. **§ 8.5 AWS-vs-API per-route documentation — no example of how a single route's behavior under INACTIVE-target conditions would be documented.** The deferral is clean, but a one-paragraph example would make it concrete: e.g., "If route `POST /ingest` targets equine-ingestion (INACTIVE), Phase 1 documents: 'route returns 502 Bad Gateway when invoked; integration target is INACTIVE Lambda whose ECR image is missing; behavior was verified [date].'"

5. **§ 9.13 — example of the sharpening's binary test being applied or violated.** The text says removing any one of the three pieces "converts the documentation back to the FORBIDDEN form." A two-line example showing "two-piece documentation that fails the test" would make the binary actionable.

---

## Additional adversarial findings

### A. v3 finding regression

Per the regression check table above. **All 7 findings (1 BLOCKER + 6 MATERIALs) addressed cleanly.** No regression. (v3 had a regression on Q1.2 — replacing one wrong example with another. v4 does not repeat that pattern.)

### B. Verification log audit

8 spot-checked entries: 6 hold up cleanly; 2 have soft-edges (Claim 22 doesn't decompose untracked vs modified; Claim 26 line range slightly inflated). Neither is fabrication; both are v4's own precision rule applied loosely. See verification log audit table above for details.

### C. Verification-log-precision-rule self-application

Reported in detail in Question 2 finding 1. Summary: rule applied for code-reference counts following the v3 BLOCKER pattern; not applied for non-code aggregations ("103 modified-or-untracked entries," "two parallel feature engineering implementations," "88 model registry entries (45 simultaneously active)"). Either § 6.5 should narrow the rule's scope ("applies to code-reference counts") or v4's main doc should sweep all aggregations.

### D. § 4.1 CONVERGENCE_CRITERIA Tier 1 conditional

Migration trigger mechanics undefined. See Question 2 finding 2. Borderline MATERIAL; promoted because the conditional affects how QB writes the spec for the next Phase 0 deliverable (CONVERGENCE_CRITERIA is doc 4 in the sequence).

### E. § 12 changelog accuracy

Spot-checked. All claimed changes are present in the diff. ✓

### F. § 11 lock status vs § 3.1 exit criteria

Match item-by-item. ✓

### G. Cumulative MINOR weight from v3 carry-overs

v3 had 17 MINORs; v4 addressed 7. Of the 10 deferred:
- #7 PHASE_5_BACKLOG sequencing — v4 § 4.3 added explicit dependency note; sufficient.
- #10 § 7.10 "If existing EE has uncommitted code at Phase 0 exit" — v4 rewrote; sufficient.
- #11 § 7.14 conflation language — v4 improved with "parallel to (not a sub-rule of)"; acceptable.
- #12 spot-check undefined — still undefined.
- #13 Layer 1 ritual vs file form — promoted to MATERIAL in this audit (Question 2 finding 3).
- #14 § 3.1.2 estimate inconsistency — v4 added context note; addressed.
- #17 A.7 no post-fill example — still missing.
- #19 § 6.5 SPEC_GAP no annotation example — v4 added text-form examples; partial.
- #21 § 3.4 / § 3.5 still skeletal — unchanged; remains MINOR.

One promotion (#13 → MATERIAL); rest stay MINOR.

### H. New v4 pattern — CC's methodology-interpolation habit at the discipline-rule level

The v3 BLOCKER was a count fabrication. The v4 pattern (Question 1 finding 3, Question 5 finding 5) is methodology-interpolation: § 9.13's "Removing any one converts the documentation back to the FORBIDDEN form" prescribes a binary test Tony hasn't ratified. Same root failure mode as the v3 § 7.10 "same working session" sentence — CC extending operator policy at the level the rule applies. v4 fixed the v3 instance but introduced a new instance at a different level. This deserves naming as a recurring pattern, not a one-off.

---

## Severity assessment

| # | Finding | Section | Severity |
|---|---|---|---|
| 1 | Verification-log-precision rule scope undefined; v4 applies inconsistently | § 6.5 + § 1.1 / § 1.3 / A.4 race_router.py | MATERIAL |
| 2 | § 4.1 CONVERGENCE_CRITERIA Tier 1→3 migration mechanics undefined | § 4.1 + § 6.5 | MATERIAL |
| 3 | § 7.13 Layer 1 checklist physical form unspecified; Layer 1 is sole active enforcement | § 7.13 | MATERIAL |
| 4 | § 8.1 Bug #28 "stable known" depends on unverified backfill assumption | § 8.1 | MATERIAL |
| 5 | § 9.13 "three required pieces" + "Removing any one... FORBIDDEN" is CC-interpolated binary methodology not Tony-ratified | § 9.13 | MINOR (echo of v3 #3 pattern at different level) |
| 6 | § 4.5 worked example DB query (`SELECT MAX(created_at) FROM results`) asserted without verification | § 4.5 | MINOR |
| 7 | Claim 26 line range "616-628" — actual bypass spans 616-626 | § 1.2, § 9.12, A.2, log Claim 26 | MINOR |
| 8 | A.4 race_router.py decomposed but not summed (inconsistent with prediction_router.py) | A.4 | MINOR |
| 9 | § 7.10 "typically 3–5 per heavy session, not 20" — surviving CC-interpolated cadence (parallel to dropped same-session sentence) | § 7.10 | MINOR |
| 10 | § 6.5 SPEC_GAP/FRAMEWORK_GAP "use more specific" requires judgment without example | § 6.5 | MINOR |
| 11 | § 6.5 verification-log-precision rule has no worked example | § 6.5 | MINOR |
| 12 | § 7.13 Layer 1 waiver phrasing for bible diff review awkward (two retroactive deadlines, single review event) | § 7.13 | MINOR |
| 13 | § 8.5 "where applicable" scope of route documentation slightly ambiguous | § 8.5 | MINOR |
| 14 | A.7 no post-fill example (v3 carry-over #17) | A.7 | MINOR |
| 15 | § 6.5 spot-check still unquantified (v3 carry-over #12) | § 6.5 | MINOR |
| 16 | § 3.4 / § 3.5 / § 3.6 still skeletal (v3 carry-over #21) | § 3.4–3.6 | MINOR |
| 17 | § 12 self-referential entry about the changelog itself | § 12 | STYLE |
| 18 | § 7.13 "bible-touching" determination is circular (drafter judgment) — v3 carry-over | § 7.13 + § 7.11 | STYLE |

---

## Material findings count

**4 MATERIAL** findings (#1–#4 in the table). Justification per Tony's "use judgment" rule:

- **#1 (precision-rule scope undefined and inconsistently applied):** MATERIAL because the rule is the methodology lesson v4 was supposed to internalize. Inconsistent application means the lesson isn't yet at methodology quality. The rule's scope determines whether future Tier 3 drafters bloat verification logs or re-introduce the v3 BLOCKER. This is a load-bearing rule with undefined scope.
- **#2 (Tier 1→3 migration mechanics):** MATERIAL because CONVERGENCE_CRITERIA is the next Phase 0 deliverable in sequence (doc 4). QB writes the spec next. Without migration mechanics specified, the spec has a hidden branch (Tier 1 spec vs Tier 3 spec; what triggers the swap; whether mid-draft re-spec is needed).
- **#3 (Layer 1 checklist physical form):** MATERIAL because Layer 2 is dormant ("PR workflow out of scope for Phase 0") and Layer 3 only fires on bible-touching commits per § 7.11's silence convention. Layer 1 is the SOLE active enforcement tier from Phase 1 onward. Its physical form being undefined leaves the entire commit-before-deploy discipline depending on Tony's mental ritual.
- **#4 (Bug #28 "stable known" assumption):** MATERIAL because § 8.1 uses Bug #28 as the worked-example for the "stable known" exception logic. If the assumption (backfill feasible) is wrong, the case study is wrong, and the exception logic is misapplied. v4 added the caveat but the worked example still classifies Bug #28 as stable known on the basis of an unverified assumption.

**MINOR (#5–#16):** individually small; cumulative weight does not promote any to MATERIAL beyond those above.

**STYLE (#17–#18):** framing only.

---

## Fabricated-content findings

**ZERO.**

The fabrication path the v3 BLOCKER taught is structurally closed. v4's verification log uses decomposed counts; v4's main doc carries the decomposition through (with the noted A.4 race_router.py inconsistency that doesn't rise to fabrication — it's a precision-rule application gap, not a count error).

Soft-edges noted (Claim 22 not decomposed into untracked + modified; Claim 26 line range off by 2 lines) are precision drift, not fabrication. Both are accurate-but-imprecise rather than wrong.

Per Tony's hard rule, v4 passes the fabricated-content bar.

---

## Recommendation

**Lock after specific minor revisions.**

v4 meets Tony's threshold (4 MATERIAL < 5; zero fabricated-content). The four MATERIALs are surgical:

1. **Narrow § 6.5's precision-rule scope explicitly** ("applies to code-reference counts; non-code aggregations may be partially decomposed if cross-reference makes them unambiguous") OR sweep v4 main doc for the remaining non-decomposed aggregations (specifically: "103 modified-or-untracked entries" → "74 untracked + 29 modified = 103"; race_router.py reference count to add the sum; "88 model registry entries (45 simultaneously active)" → "88 = 45 active + 43 inactive"). Either resolution is acceptable; the choice is a Tony architectural call.

2. **Specify § 4.1's Tier 1→3 migration trigger.** Two possible specifications:
   - Pre-hoc: "QB judges at spec time whether the document can be drafted without EE references. If unclear, default to Tier 3."
   - Post-hoc: "Document drafted as Tier 1; if completed draft contains any EE-specific factual claim, document is re-specced as Tier 3 with verification log applied retroactively to existing text."
   
   Either works; pick one.

3. **Specify Layer 1 checklist physical form.** Either: "Tony maintains `~/.claude/projects/.../deploy-checklist.md` (or equivalent) with the five checkboxes; checks them before each deploy" OR explicitly accept "Layer 1 is operator mental ritual; future PR workflow adoption (Layer 2) replaces it" — the latter is honest but weakens enforcement.

4. **Add a Bug #28 backfill-assumption-resolution note to § 8.1.** Either re-classify Bug #28 as "provisionally stable known pending Phase 1 verification of backfill feasibility" or explicitly state that re-classification is possible if the verification fails. Don't leave the worked example resting on an unverified assumption with only a footnote.

The 12 MINORs and 2 STYLEs may be addressed opportunistically or deferred to v6 (if a v5 cycle is needed) without delaying lock.

**Alternative reading:** if Tony judges the four MATERIALs insufficiently surgical (specifically: if precision-rule scope ambiguity is judged a methodology-foundation issue rather than a clarity edit), recommendation shifts to "revise + re-audit." The four MATERIALs are addressable in one revision pass; whether that pass needs a fresh adversarial audit or just Tony review is the architectural call.

The structure and direction of v4 are sound. The fabrication path is closed. The remaining work is methodology coherence, not factual correctness.

---

End of audit.
