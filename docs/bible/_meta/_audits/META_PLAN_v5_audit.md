# META_PLAN.md DRAFT v5 — ADVERSARIAL AUDIT

**Audit-CC session:** fresh CC, 2026-05-04
**Auditing:** META_PLAN.md draft v5 at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/META_PLAN.md`
**Companion verification log audited:** `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/_audits/META_PLAN_v5_verification.md`
**Verification substrate:** live AWS, live API, working tree, DD bible, operator memory file
**Threshold:** Tony's "< 5 MATERIAL findings AND zero fabricated-content findings AND zero methodology-interpolation findings" criterion

---

## Summary verdict

Revise + re-audit. Zero fabricated content. v5's drafting complied with the methodology-interpolation rule for new content. **But v5 carried forward at least one CC-interpolated numerical criterion from an earlier cycle that the rule should have swept (§ 5.3 / § 3.1 "3 consecutive iterations" iteration cap — the specific number "3" was CC-chosen in v3, never Tony-ratified).** Per Tony's bar — methodology-interpolation findings fail regardless of count — this is a hard fail. Plus 2 additional MATERIAL gaps. The fix is surgical (drop the specific number; add scope clarification) but a re-audit is warranted because the audit's central question is whether the rule has been fully internalized; finding a carry-over interpolation answers no.

---

## Verification log audit

I re-ran the verification commands for the four modified entries (Claims 7, 16, 22, 26) and the new Claim 28.

| # | Claim | Re-verification | Holds up? |
|---|---|---|---|
| 7 | Model registry 88 = 45 active + 43 inactive | `curl /dashboard/metrics` parsed: total=88, active=45, inactive=43 | ✓ Decomposed correctly; sum verified |
| 16 | A.4 prediction_router.py + race_router.py decompositions | `grep -n "PredictionRepository" backend/routers/prediction_router.py` → 4 lines (line 6 import + 34, 61, 92 instantiations); `grep` race_router.py → 2 lines (273 import + 277 instantiation; plus separate WRPredictionRepository at 143-144 for context) | ✓ Decomposition matches; sums correct |
| 22 | Working-tree decomposed | `git status --porcelain \| awk '{print $1}' \| sort \| uniq -c` → 74 ?? + 29 M = 103 | ✓ |
| 26 | Calibration bypass 616-626 | `awk 'NR>=614 && NR<=632'` on wr_inference_service.py: comment block exactly at 616-625 (10 lines), bypass operation `handicapping_probs = ranker_probs.copy()` exactly at 626, blank line 627, next section starts at 628 | ✓ Range corrected from v4's 616-628; decomposition (10-line comment + 1-line operation) matches |
| 28 | Derby Day counterfactual (operator-stated) | Searched `~/.claude/projects/-home-strakajagr/memory/` for derby files: only `equine-equalizer-bug-28-hrn-scraper.md` mentions "Derby Day counterfactual analysis" without dollar amounts. SESSION_005.md mentions only "Derby Day Easter Egg" UI. wr_inference_service.py:622 corroborates "Wonder Dean JPN at #1 in Derby smoke test." Specific dollar amounts (~$-108 / ~$-150) not in any primary source. | ✓ Disclosure correct: explicitly flagged as operator-stated, not independently verified at primary-source granularity. Survives the "is the disclosure sufficient?" test (Question 1 below). |

**8/8 sampled entries hold up under re-verification (5 from this round + 3 from random sample of inherited claims I re-checked: Claim 1 Lambda counts, Claim 13 DD line count 2578, Claim 21 phase arithmetic).**

**Verification-log-precision rule self-application across v5 main doc:** Tony's locked decision in v5 cycle was Option B (broad sweep). Application:

- ✓ § 1.1, § 1.3 working-tree decomposed (74 untracked + 29 modified = 103)
- ✓ § 1.3, § 9.13 model registry decomposed (88 = 45 active + 43 inactive)
- ✓ § 2.3 EventBridge decomposed inline (10 ENABLED + 3 DISABLED) AND fully enumerated
- ✓ § 2.3 Lambda summary decomposed inline (5 Active + 3 INACTIVE) AND fully enumerated
- ✓ A.4 race_router.py summed ("= 2 references total")
- ✓ § 9.11 14 = 4+7+3 decomposition
- **✗ § 2.3 ECS Fargate "5 task definition families" — names only 2 of 5 inline ("dump missed `equine-training` and `equine-training-win-prob`"). The other 3 (equine-training-daily-full, equine-training-manual, equine-training-pl) are not enumerated in § 2.3.** By Tony's broad-sweep decision, all 5 should be named.
- **✗ § 2.3 ECR repositories: "currently 5 images" — the 5 images are not decomposed/named.** Defensible since image counts may rotate and listing tags would bloat the doc, but by strict broad-sweep rule the count is undefended.
- **✗ § 1.2 "three calibration bugs in one week"** — defensible (gonzo_features.py docstring says "three distinct bugs" without enumerating which). Source doesn't decompose; v5 can't fabricate. Note: Bug #15 + Bug #24 + a third are partly named in § 1.2 prose (Bug #15 / Bug #24 / Bug #25 are referenced separately) — so "three" likely IS Bug #15 + Bug #24 + (one more). Not closing this gap is defensible but the source-decomposition status should be cited.
- ✓ § 1.4 DD section/line decomposition (Player § 4 / line 590, etc.)

Three minor gaps remaining; collectively MINOR-cumulative, not MATERIAL.

---

## v4 finding regression check

| v4 finding | v5 fix verified? | Notes |
|---|---|---|
| MATERIAL #1 (precision-rule scope: broad sweep) | ✓ ADDRESSED | Decompositions applied across § 1.1, § 1.3, § 2.3, A.4 race_router.py. § 6.5 worked example added. Three minor decomposition gaps remain (above) but bulk applied. |
| MATERIAL #2 (Tier 1→3 migration: pre-hoc) | ✓ ADDRESSED | § 4.1 row 4 reads "Determined pre-hoc per § 6.5; see footnote." Footnote specifies QB judges at spec-writing time, defaults to Tier 3 if unclear. § 6.5 alignment clean. |
| MATERIAL #3 (Layer 1 physical form: hybrid deferral) | ✓ ADDRESSED | New § 7.13 subsection added. Tony's verbatim language ("operator mental ritual"; risk acknowledged; mitigation specified) matches spec. |
| MATERIAL #4 (Bug #28 stable-known: provisional) | ✓ ADDRESSED | § 8.1 case study restructured to operate as "provisionally stable known." Re-classification trigger paths (a) and (b) named verbatim from spec. |

**4/4 v4 MATERIALs cleanly addressed.** No regression.

---

## NEW MATERIAL #5 forcing function check

| Element | Verified? |
|---|---|
| Three forcing functions correctly named (Feature Provenance / ML Layer Architecture / Model Evaluation & Retraining) | ✓ § 3.2.1 names all three |
| Three separate documents minimum locked at META_PLAN level | ✓ § 3.2.1 "Authority" subsection: "BIBLE_STRUCTURE_SPEC.md may NOT merge these three forcing functions into fewer than three documents. The three forcing functions get three separate documents; this is locked at META_PLAN level, not deferred to BIBLE_STRUCTURE_SPEC." |
| BIBLE_STRUCTURE_SPEC may rename / restructure / add but may NOT reduce | ✓ Same subsection |
| Convergence test specified for Phase 1 inventory | ✓ "given this inventory, can a fresh CC session evaluate, rebuild, or retrain a model in the gallery?" matches Tony's verbatim language |
| Cross-references throughout v5 use new bible names consistently | Mostly ✓ — but see Question 4 finding 1 below |

**Key finding under check B:** § 3.2's working hypothesis list (revised in v5) cross-references documents 3, 4, 5 to forcing functions 2, 3, 1. Verified consistent. § 7.4, § 7.5, § 7.11, § 4.2, A.7 cross-references updated to "ML Layer Architecture Bible," "Feature Provenance Bible," etc. — verified consistent.

**One language gap (see Question 3 finding 1):** "may NOT merge into fewer than three documents." "Merge" is ambiguous — could a single document with three sections, one per forcing function, comply with the letter while violating the spirit?

---

## MINOR fixes regression check

| MINOR | v5 fix verified? | Notes |
|---|---|---|
| #5: § 9.13 binary test softened to descriptive prose | ✓ MOSTLY | "Removing any one converts to FORBIDDEN" sentence is gone. Replacement names three pieces with consequences-of-incomplete-documentation framing. Borderline: the descriptive prose still asserts "Documentation that names only the function (omitting both the reality and the gap) is the FORBIDDEN form." This is a re-statement of the existing FORBIDDEN/CORRECT pair, not a new binary test, so it survives. |
| #7: Claim 26 line range corrected | ✓ ADDRESSED | All references in § 1.2, § 9.12, A.2, log Claim 26 updated to 616-626 with explicit 10-line + 1-line decomposition. Re-verified live. |
| #8: A.4 race_router.py sum added | ✓ ADDRESSED | A.4 reads "1 instantiation, plus 1 import on line 273 = 2 references total." Matches prediction_router.py's pattern. |
| #9: § 7.10 "3-5 per heavy session, not 20" cadence dropped | ✓ ADDRESSED | Sentence gone; cadence framed as Phase 5 working-agreements decision. |

**4/4 expanded MINORs cleanly addressed.**

---

## Methodology-interpolation rule self-application

This is the new bar in v5. Methodology-interpolation findings fail the lock regardless of count.

**Rule per § 6.1:** CC "does NOT invent binary tests, cadence rules, completeness criteria, or scoring rubrics that Tony has not explicitly ratified."

**v5 drafting compliance (CC's three caught-and-rejected drafts):**
- ✓ § 3.2.1 numerical pass-criterion "3 of 3 forcing functions auditable" — verified absent in final v5; the convergence test asks the qualitative question only
- ✓ § 7.13 cadence prescription "operator should review checklist at minimum once per deploy session" — verified absent
- ✓ § 9.13 "documentation that names two of the three pieces is acceptable, naming one is forbidden" — verified absent; replacement uses descriptive prose

**Carry-over interpolations from earlier cycles that v5 did NOT sweep:**

**FINDING M-1 (METHODOLOGY INTERPOLATION):** § 5.3 contains: **"Iteration cap: if the convergence test fails on the same dimension in 3 consecutive iterations, QB escalates to Tony for protocol revision rather than continuing to iterate."** The same numerical iteration cap appears in § 3.1 edge-cases enumeration: **"If § 5.3's convergence test fails repeatedly (>3 iterations) on the same dimension, QB escalates to Tony for a methodology-protocol revision rather than continuing to iterate. This is an iteration cap on the convergence loop itself."**

The specific number **"3"** was CC-chosen in the v3 cycle. v3's drafting context: v2 audit Q2.8 said "no iteration cap" and asked for one to be added. The v3 drafting spec said "§ 5.3 iteration cap added: 3 consecutive same-dimension failures escalates to Tony for protocol revision" — but that text was the spec-writer's example wording, not Tony's locked verbatim. The "3" has never been Tony-explicitly-ratified across v1–v5 cycles.

This is the same root failure mode v4's Finding H named: CC inventing a numerical criterion (the iteration count) without Tony's explicit ratification. v3 § 7.10 ("same working session") and v4 § 9.13 ("Removing any one converts to FORBIDDEN") were the cycle-N instances; this is a cycle-N-2 instance that never got swept.

Per Tony's bar (methodology-interpolation findings fail regardless of count), this fails the lock criterion.

**Suggested resolution:** either (a) Tony explicitly ratifies "3" as the cap; or (b) replace "3 consecutive iterations" with cadence-neutral language deferring the count to operator judgment ("repeated failure on the same dimension triggers escalation; the count threshold is a Phase 5 working-agreements decision per § 7.13's pattern" or similar).

**Other potential interpolations swept and resolved:**

- § 5.3 "Material difference defined" exhaustive bullet list of categories. **Possible interpolation candidate** — the categories were drafted in v1 by QB and have persisted unchanged. By the rule's letter, the rule applies to CC inventions, not QB drafts; CC's preservation of QB-drafted material is not invention. Demoted to **MINOR concern** (not a methodology-interpolation finding).
- § 6.1 methodology-interpolation rule itself names "binary tests, cadence rules, completeness criteria, scoring rubrics" verbatim from Tony's drafting spec. Trace clean.
- § 3.2.1 convergence test verbatim from Tony's spec. Trace clean.
- § 8.1 Bug #28 paths (a) and (b) verbatim from Tony's spec. Trace clean.
- § 7.13 enforcement-failure recovery verbatim from Tony's v4 cycle Q3. Trace clean.
- § 7.13 emergency-hotfix waiver list of waived-vs-not-waived items: each item's classification is in Tony's v4 cycle spec. Trace clean.

**Net methodology-interpolation findings: 1.** Per Tony's bar, this fails regardless of MATERIAL count.

---

## Question 1: Unverifiable claims / verification gaps

1. **§ 3.2.1 forcing function descriptions — "Provenance is feature-centric (change-impact). Architecture is model-centric (composition). Evaluation is process-centric (operational)."** These audience characterizations match Tony's drafting spec verbatim. Verified.

2. **§ 6.5 worked example (v3 → v4 lesson)** — re-verified against the v3 verification log Claim 16 and v3 audit's quoted A.4 phrasing. Both match. Verified.

3. **§ 6.1 CC role expansion — characterization of v3 § 7.10 and v4 § 9.13 as CC interpolation.** v3 § 7.10's "same working session" sentence and v4 § 9.13's "Removing any one converts to FORBIDDEN" — both characterized as CC interpolation. Tony's v4 → v5 drafting spec confirms both: "v3 § 7.10 'same working session' cadence was CC interpolation; v4 § 9.13 'Removing any one converts to FORBIDDEN' was a CC-interpolated binary test." Verified.

4. **Coverage gap — § 5.3 "3 consecutive iterations" iteration cap.** Not in verification log. The number is methodology, not factual claim, so this is a methodology-interpolation finding (M-1 above), not a factual coverage gap. But noted here because the number's origin (CC v3 cycle) is not documented in the v5 changelog or anywhere else in v5.

5. **Coverage gap — § 8.1 "place/show/exacta payouts still populate" claim.** v5 § 8.1 says: "Failure mode is bounded (column shift produces NULLs for win_payout and daily_double_payout; place/show/exacta payouts still populate per the operator memory file's diagnostic)." The operator memory file confirms place/show payouts populate (as cell indices shift one over) but does NOT explicitly confirm exacta payouts still populate. Re-checking the memory file: it says "DD pool extraction... likely has the same root cause — same site-wide column shift" — implying exacta and DD pool extraction may also be affected. v5's "exacta_payouts still populate" claim is not directly supported by the memory file; the memory file is silent on exacta status specifically.

6. **§ 3.2.1 Derby Day counterfactual disclosure** — "operator-stated; not independently verified at primary-source granularity, but the lived-experience direction is the operative fact for this design constraint." Disclosure is honest. The dollar amounts are framed with "roughly" qualifiers. The "no model picked the Derby winner" and "gonzo == general at rank=1" claims have indirect corroboration via wr_inference_service.py:622 ("Wonder Dean JPN at #1 in Derby smoke test"). Disclosure sufficient. ✓

7. **§ 3.2 working hypothesis vs § 3.2.1 floor** — § 3.2 lists 7 documents; § 3.2.1 sets a floor of 3 ML-specific documents minimum. The 7-document list contains documents 3, 4, 5 mapped to forcing functions 2, 3, 1 (i.e., 3 ML documents). Total = 4 non-ML + 3 ML = 7. Math checks out.

---

## Question 2: Scope gaps

1. **Methodology-interpolation rule scope is incomplete (§ 6.1).** The rule names: "binary tests, cadence rules, completeness criteria, or scoring rubrics." It does NOT name: severity thresholds (e.g., the < 5 MATERIAL threshold itself — Tony-ratified), iteration caps (e.g., the "3 consecutive iterations" — NOT Tony-ratified, see M-1), percentage criteria, procedural sequencing rules. The rule's effectiveness depends on its scope. Two readings:
   - **Strict:** the rule applies broadly to "any methodology construct CC didn't get explicit Tony ratification for." The four listed categories are illustrative.
   - **Permissive:** the rule applies only to those four categories; other patterns are out-of-scope.
   
   v5's text doesn't disambiguate. The Question 6 below proposes adding a worked example.

2. **§ 3.2.1 "may NOT merge into fewer than three documents" workaround risk.** "Merge" reading 1: three documents must be physically separate files. Reading 2: three documents must be three logical units; could be three sections of one file. The intent (per Tony's spec) is clearly Reading 1, but the language doesn't enforce it. A drafter following only the letter could produce a single "ML_BIBLE.md" with three sections labeled by forcing function and claim compliance. **Suggested fix:** add "as separate files at separate paths" or "three documents = three distinct .md files each at a distinct path."

3. **Methodology-interpolation rule applies to CC, not QB (§ 6.1).** This is a real boundary in the role definitions, but it leaves ambiguity for cases where CC is preserving QB-drafted content from earlier cycles. Does CC's preservation of pre-rule QB content count as invention? § 6.1 doesn't say. Earlier cycles' QB drafts that may contain interpolations CC carries forward (e.g., § 5.3 material-difference categories) are in a gray zone. **Suggested fix:** add a sentence: "Pre-existing methodology constructs from earlier cycles' QB drafts are grandfathered; CC does not need to re-verify Tony's ratification of pre-existing content. New content CC introduces falls under the rule."

4. **Decomposition gaps remaining despite broad-sweep precision rule:**
   - § 2.3 ECS Fargate "5 task definition families" — names only 2 of 5 inline (the dump-missed ones).
   - § 2.3 ECR repositories "currently 5 images" — not decomposed.
   - Cumulative MINOR weight; not promoting to MATERIAL.

---

## Question 3: Ambiguous language

1. **§ 3.2.1 "may NOT merge these three forcing functions into fewer than three documents."** See Question 2 finding 2. "Merge" permits a section-based workaround.

2. **§ 6.1 "explicitly ratified."** What constitutes explicit ratification? Two readings:
   - **Active:** Tony's drafting-spec verbatim or a Tony-locked answer naming the construct directly.
   - **Passive:** Tony's silence after multiple draft cycles where the construct was visible without challenge.
   
   v5 implicitly applies Active for new content (CC's three caught-and-rejected drafts) but Passive for grandfathered content (§ 5.3 categories). The boundary isn't named.

3. **§ 6.5 "Anything aggregable must be aggregated explicitly."** After v5's broad-sweep clarification + worked example + Tony's Option B decision recorded inline, the rule's scope is now reasonably unambiguous.

4. **§ 7.13 "Layer 1 is currently operator mental ritual."** Stable category through Phase 5? § 7.13 says Phase 5 working agreements decides; the category persists until then. Acceptable.

5. **§ 8.1 Bug #28 re-classification trigger paths (a) and (b).** Are they exhaustive? Two scenarios:
   - (a) "known but not stable" — backfill not feasible AND operator chooses to escalate.
   - (b) "stable known with permanent loss" — backfill not feasible AND operator chooses NOT to escalate.
   
   What if Phase 1 audit finds backfill is *partially* feasible (e.g., 50% of affected dates have retrievable historical pages)? v5's binary doesn't accommodate partial. Not catastrophic; Tony's spec was explicit on the binary, so this is faithful. But future Phase 1 audit may need to surface "partial feasibility" as a third trigger path.

---

## Question 4: Contradictions

### Internal

1. **§ 3.2 working hypothesis vs § 3.2.1 floor.** No contradiction — the list contains 3 ML documents (items 3, 4, 5), satisfying the floor. The "may add additional documents" clause matches § 3.2.1's authority statement. ✓

2. **§ 4.1 vs § 6.5 Tier 3 description.** Both say "(CC-drafted under QB spec, with verification log; CC-audited)" for Tier 3 rows. § 4.1 row 4 (CONVERGENCE_CRITERIA) says "Determined pre-hoc per § 6.5; see footnote." § 6.5 says CONVERGENCE_CRITERIA is "the only Phase 0 document targeted as a Tier 1 candidate; final tier set pre-hoc when QB writes the spec." Aligned. ✓

   **Minor stylistic concern:** the § 4.1 table's Tier column should hold a tier number; "Determined pre-hoc per § 6.5; see footnote" reads as a procedural directive rather than a tier value. Could be: "1 (provisional)" or "1 / 3 (pre-hoc)" — anything that's tier-shaped while flagging the pre-hoc determination. STYLE.

3. **§ 6.1 methodology-interpolation rule vs § 3.2.1 convergence test.** § 6.1 forbids CC from inventing methodology constructs. § 3.2.1 contains a convergence-test question. Verified: § 3.2.1's question is verbatim from Tony's spec. Trace clean.

4. **§ 12 changelog accuracy.** Spot-checked claims:
   - "MATERIAL #1 — broad sweep applied" — § 1.1, § 1.3, § 2.3, A.4, etc. decompositions verified ✓
   - "§ 6.5 worked example added" — verified present ✓
   - "MATERIAL #2 — pre-hoc determination" — § 4.1 row 4 + § 6.5 verified ✓
   - "MATERIAL #3 — hybrid deferral" — § 7.13 new subsection verified ✓
   - "MATERIAL #4 — provisional classification" — § 8.1 case study restructure verified ✓
   - "NEW MATERIAL #5 — § 3.2.1" — verified ✓
   - "MINOR #5 — § 9.13 binary-test softening" — verified, with caveat ✓
   - "MINOR #7 — Claim 26 line range corrected" — verified ✓
   - "MINOR #8 — A.4 race_router.py sum added" — verified ✓
   - "MINOR #9 — § 7.10 cadence dropped" — verified ✓

   All claimed changes are present.

5. **§ 11 lock status vs § 3.1 exit criteria.** Both enumerate (a) all 5 documents pass adversarial audit, (b) § 5.4 convergence test, (c) § 3.1.1 baseline commit, (d) § 7.14 gitignore audit + findings, (e) § 8.2 PHASE_5_BACKLOG.md created. Match item-by-item. ✓

### External

6. **v5 alignment with Tony's drafting spec:** all five locked decisions verified verbatim.
   - Three forcing functions / three separate documents minimum: v5 § 3.2.1 ✓
   - Broad-sweep precision rule: v5 § 6.5 ✓
   - Pre-hoc tier determination: v5 § 4.1 + § 6.5 ✓
   - Layer 1 hybrid deferral: v5 § 7.13 ✓
   - Bug #28 provisional: v5 § 8.1 ✓

---

## Question 5: Rushed sections

1. **§ 3.4 / § 3.5 Phase 3 / Phase 4 still skeletal.** v3 audit MINOR carry-over; v4 audit MINOR carry-over; v5 didn't develop. META_PLAN's job is to name the phases; deeper specification belongs in subsequent documents. Stays MINOR.

2. **§ 8.1 Bug #28 re-classification paths (a) and (b).** Each is given a one-sentence definition. Phase 1 audit's classification call is named as the trigger but the audit's process for reaching the call isn't specified (which is appropriate — that belongs in AUDIT_METHODOLOGY.md). Acceptable.

3. **§ 6.1 CC role expansion.** Methodology-interpolation rule is stated abstractly as a CC role bullet. v5 doesn't include a worked example (Question 6 finding 2). Stays MINOR.

4. **§ 9.13 descriptive-prose replacement.** Re-read carefully: the replacement names the three pieces, describes consequences of two-piece documentation (descriptive but not actionable), and identifies one-piece documentation as the FORBIDDEN form. The "is the FORBIDDEN form" assertion is a re-statement of the existing FORBIDDEN/CORRECT pair within the same section, not a new binary methodology. Acceptable.

5. **§ 3.2.1 forcing function** — substantively developed. Each forcing function has audience + question-it-answers + reader's information needs. Authority subsection clear. Convergence test specified. Not rushed.

---

## Question 6: Missing examples

1. **§ 3.2.1 inventory passing/failing the convergence test** — would be useful, but per the methodology-interpolation rule (no scoring rubrics), CC should NOT draft a worked example showing what passes vs fails. Tony would need to specify. Defer to Phase 0 doc 3 (AUDIT_METHODOLOGY.md) or BIBLE_STRUCTURE_SPEC.md.

2. **§ 6.1 methodology-interpolation rule** — a worked example showing a hypothetical CC-interpolation that the rule would catch would help future CCs apply the rule. v5 references three caught-and-rejected drafts in the v5 cycle (per the CC summary) but does NOT show them inline. Could add a brief inline example: "E.g., a draft that introduced 'documentation that names two of three pieces is acceptable' would be caught — the rule asks: did Tony specify '2 of 3 = acceptable'? If not, drop the binary." This is illustrative, not prescriptive, so doesn't violate the rule itself. **Suggested addition.**

3. **§ 7.13 Layer 1 mental ritual** — no worked example of the ritual operating. Could be: "Tony, before each deploy, mentally walks the five checklist items: (1) git status... (5) commit message convention. No file is maintained." Illustrative, helps a reader (or future Tony) reproduce. **Suggested addition.**

4. **§ 6.5 SPEC_GAP / FRAMEWORK_GAP examples** — § 6.5 has each marker with a one-sentence example. The FRAMEWORK_GAP example uses DD's Player canonical-object analogy ("framework expects a 'single canonical Player object' but EE has multiple") which doesn't map cleanly onto EE (EE has horses, not players). The example signals "structural mismatch" but uses DD's vocabulary for the placeholder. MINOR. Could rewrite using an EE-specific hypothetical structural mismatch.

---

## Additional adversarial findings

### E. § 12 changelog accuracy

Spot-checked. All claimed changes are present in the diff. § 12 itself contains a self-referential entry ("§ 12 changelog (this section): acknowledges...") that's awkward but not inaccurate. STYLE.

### F. § 11 vs § 3.1 exit criteria parity

Match item-by-item. ✓

### H. Cumulative MINOR weight from carry-overs

v4 had ~12 MINORs; v5 addressed 4 explicitly (#5, #7, #8, #9). Of the 8 deferred:
- #6 (§ 4.5 worked example DB query unverified) — present in v5 (the equine-results worked example carries the unverified `SELECT MAX(created_at)` claim). Now framed with disclosure ("Phase 1 audit-CC runs this query; v5 main doc cannot independently verify"). Acceptable.
- #10 (§ 6.5 SPEC_GAP/FRAMEWORK_GAP "use more specific" requires judgment) — unchanged in v5. MINOR.
- #11 (§ 6.5 verification-log-precision rule worked example) — RESOLVED in v5 (§ 6.5 added the worked example).
- #12 (§ 7.13 Layer 1 waiver phrasing awkward) — minor wording, unchanged. MINOR.
- #13 (§ 8.5 "where applicable" scope) — unchanged. MINOR.
- #14 (A.7 no post-fill example) — unchanged. MINOR.
- #15 (§ 6.5 spot-check unquantified) — unchanged. MINOR.
- #16 (§ 3.4–3.6 skeletal) — unchanged. MINOR carry-over.

No cumulative-weight promotion to MATERIAL.

### Other observations

- **§ 2.3 broad-sweep gaps** (named in verification-log-audit section above): ECS task families 5 listed but only 2 named inline; ECR images 5 not decomposed. MINOR.
- **§ 1.2 "place/show/exacta payouts still populate"** (Question 1 finding 5): the operator memory file's diagnostic confirms place/show/exacta in the table for 2026-04-25 and 2026-04-29 (clean dates) but the file specifically calls out "DD pool extraction... likely has the same root cause" — implying exacta MAY also be affected. v5's claim that exacta payouts still populate is at best partly verified. MINOR.
- **§ 4.1 row 4 Tier column reads "Determined pre-hoc per § 6.5; see footnote"** instead of a tier value — semantic mismatch with the column header. STYLE.
- **§ 12 self-referential changelog entry** (carried from v4 audit STYLE finding). Still STYLE.

---

## Severity assessment

| # | Finding | Section | Severity |
|---|---|---|---|
| M-1 | § 5.3 / § 3.1 "3 consecutive iterations" iteration cap — CC-interpolated number never Tony-ratified | § 5.3, § 3.1 | **MATERIAL (methodology interpolation)** |
| M-2 | § 6.1 methodology-interpolation rule scope incomplete — names 4 categories without "or other" or scope clarifier | § 6.1 | MATERIAL |
| M-3 | § 3.2.1 "may NOT merge into fewer than three documents" permits section-based workaround | § 3.2.1 | MATERIAL |
| 4 | § 6.1 grandfathering of pre-existing QB-drafted constructs is implicit, not specified | § 6.1 | MINOR |
| 5 | § 1.2 "place/show/exacta payouts still populate" — exacta status partly unverified per operator memory | § 1.2, § 8.1 | MINOR |
| 6 | § 2.3 ECS Fargate "5 task definition families" — only 2 named inline despite broad-sweep rule | § 2.3 | MINOR |
| 7 | § 2.3 ECR "5 images" not decomposed | § 2.3 | MINOR |
| 8 | § 6.5 FRAMEWORK_GAP example uses DD's Player canonical-object analogy not EE-specific | § 6.5 | MINOR |
| 9 | § 6.1 methodology-interpolation rule lacks worked example | § 6.1 | MINOR |
| 10 | § 7.13 Layer 1 mental ritual lacks worked example | § 7.13 | MINOR |
| 11 | § 6.5 "explicitly ratified" boundary undefined (active vs passive ratification) | § 6.5 / § 6.1 | MINOR |
| 12 | § 8.1 Bug #28 re-classification paths binary; partial-feasibility not accommodated | § 8.1 | MINOR |
| 13 | § 4.1 row 4 Tier column holds non-tier value | § 4.1 | STYLE |
| 14 | § 12 self-referential changelog entry pattern | § 12 | STYLE |
| 15 | § 5.3 "Material difference defined" categories are CC-drafted-by-QB-in-v1 completeness criterion (grandfathered per the rule's letter; flagged for Tony awareness) | § 5.3 | STYLE / awareness |

---

## Material findings count

**3 MATERIAL** findings:

- **M-1 (§ 5.3 / § 3.1 iteration cap "3"):** MATERIAL by Tony's bar — methodology-interpolation findings count regardless of count. The number "3" was CC-chosen in v3 cycle without Tony's explicit ratification. Same root failure mode as v3 § 7.10 ("same working session") and v4 § 9.13 ("Removing any one converts to FORBIDDEN") — except this one survived through to v5.
- **M-2 (§ 6.1 rule scope incomplete):** MATERIAL because the rule's effectiveness depends on its scope. v5 introduces the rule as the v5 lesson; if its scope is indeterminate, future CCs cannot consistently apply it.
- **M-3 (§ 3.2.1 "merge" workaround):** MATERIAL because it permits a future BIBLE_STRUCTURE_SPEC.md to comply with the letter while violating the spirit of the forcing-function lock. Three logical sections in one document is a real risk; "merge" is the wrong word.

Three MATERIALs (within Tony's < 5 threshold). But:

---

## Fabricated-content findings

**ZERO.**

The fabrication path the v3 BLOCKER taught remains structurally closed. v5's verification log uses decomposed counts; v5's main doc carries the decomposition through.

---

## Methodology-interpolation findings

**ONE — M-1.**

§ 5.3 / § 3.1 "Iteration cap: if the convergence test fails on the same dimension in 3 consecutive iterations" — the specific number "3" was CC-chosen during v3 drafting in response to v2 audit Q2.8 ("no iteration cap"). The v3 drafting spec used "3" as the spec-writer's example number, not Tony's locked verbatim. Tony has never explicitly ratified "3" as the cap across v1–v5 cycles.

Per Tony's bar — methodology-interpolation findings fail regardless of count — this is a hard fail.

The constructive reading: v5's drafting did comply with the rule for new content (CC's three caught-and-rejected drafts in the v5 cycle). The miss is on retroactive sweep — v5 did not look for prior-cycle CC interpolations that pre-date the rule. The rule was operative for v5 onward; v5 did not interpret it as also requiring sweep of earlier cycles' content.

Either reading is defensible procedurally; the rule's letter does not specify retroactive scope. But the outcome — a CC-interpolated numerical criterion remaining in v5 — is the failure mode the rule exists to prevent.

---

## Recommendation

**Revise + re-audit.**

The three MATERIAL findings + one methodology-interpolation finding (which is itself one of the MATERIALs) are surgical:

1. **Drop the specific "3" in § 5.3 / § 3.1.** Two options:
   - **Option A:** Tony explicitly ratifies "3" as the iteration cap (one-line spec answer: "lock 3").
   - **Option B:** Replace with cadence-neutral language: "If § 5.3's convergence test fails repeatedly on the same dimension, QB escalates to Tony for protocol revision. The specific iteration count threshold is not specified at Phase 0; treated as operator judgment until Phase 5 working agreements specify cadence." Both occurrences (§ 5.3 and § 3.1 edge case) updated together.

2. **Sharpen § 6.1 methodology-interpolation rule scope.** Add: "and other CC-prescribed methodology constructs Tony has not explicitly ratified" or similar scope-broadening language. Optionally: name additional patterns (severity thresholds, iteration caps, percentage criteria, procedural sequencing) to demonstrate the rule's intended scope.

3. **Tighten § 3.2.1 "merge" language.** Replace "may NOT merge these three forcing functions into fewer than three documents" with "must produce three separate Phase 1 documents — three distinct .md files at three distinct paths — one per forcing function" or similar. Closes the section-based workaround.

4. **(Optional, Tony's call)** Sweep prior cycles for similar CC interpolations now that the rule is operative. Surface findings to Tony for explicit ratification or removal. § 5.3 "Material difference defined" categories are the most prominent candidate.

The methodology-interpolation finding is procedurally significant beyond its surgical fix because it indicates the rule has not yet been retroactively applied. A v6 cycle that fixes M-1, M-2, M-3 plus does the retroactive sweep would lock cleanly.

The structural soundness of v5 is unchanged: verification work is solid, fabrication path closed, v4 MATERIALs all addressed, NEW MATERIAL #5 (forcing function) substantively developed. The remaining work is methodology-rule discipline at the level of pre-existing content, not new content.

---

End of audit.
