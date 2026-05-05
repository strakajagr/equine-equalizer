# META_PLAN.md DRAFT v3 — ADVERSARIAL AUDIT

**Audit-CC session:** fresh CC, 2026-05-04
**Auditing:** META_PLAN.md draft v3 at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/META_PLAN.md`
**Companion verification log audited:** `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/_audits/META_PLAN_v3_verification.md`
**Verification substrate:** live AWS, live API endpoint, working tree at `/home/strakajagr/projects/equine-equalizer/`, DD bible
**Threshold:** Tony's "< 5 MATERIAL AND zero fabricated-content findings" criterion

---

## Summary verdict

Revise + re-audit. The verification log itself is solid on 19 of 23 entries when spot-checked against live state, but one claim in v3's main body inflates a count beyond what its own verification log supports — a fabricated-content finding. Plus 5 MATERIALs that surface enforcement and methodology coherence gaps not yet plugged.

---

## Verification log audit

I re-ran 8 verification log claims against live state. Results:

| # | Claim | Re-verified result | Holds up? |
|---|---|---|---|
| 1 | 8 EE Lambdas | `aws lambda list-functions` returns 8 starting with `equine` | ✓ |
| 2 | 3 INACTIVE Lambdas (ingestion, feature-engineering, results) | `aws lambda get-function` for each; all three Inactive with deleted-image StateReason | ✓ |
| 3 | 13 EventBridge rules, 3 disabled | `aws events list-rules --name-prefix equine`: 13 rules, 3 DISABLED matching named set | ✓ |
| 5 | 12 migrations, duplicate-005 | `find` returns 12 files including `005_backfill_pace_delta.sql` and `005_three_prediction_tables.sql` | ✓ |
| 7 | 88 entries / 45 active | `curl /dashboard/metrics`: total 88, active 45 | ✓ |
| 9 | `get_active_model_by_type(model_type: str)` | Read of `model_version_repository.py:100-115` — signature matches; SQL has `LIMIT 1` | ✓ |
| 10 | `ALL_FEATURES = 73`, dual-imported | `python3 -c` returns `73 73`; grep confirms imports at `inference_service.py:28` and `train.py:40` | ✓ |
| 13 | DD bible 2,578 lines | `wc -l` = 2578 | ✓ |
| 16 | predictions table, 6,600 rows, multiple readers | `001_initial_schema.sql:327` ✓; no DROP in `005`; `counts.predictions: 6600` ✓; readers verified | **Partial — see F1 below** |

**Format compliance:** entries follow the prescribed schema (claim, location, what was checked, what was found, survived, action). All 23 entries have these fields. **No format gaps in the log itself.**

**Verification entries that DON'T hold up under re-verification:**

- **F1: Verification log Claim 16 vs main-doc A.4 — internal inconsistency on PredictionRepository count.** The verification log entry reads: "`PredictionRepository(conn)` instantiated in `prediction_router.py:34, 61, 92` (4 references including the import)" — explicitly listing 3 line numbers and clarifying "4 references" includes the import line (which is on `prediction_router.py:6`, verified). But Appendix A.4 in v3's main body reads: **"`prediction_router.py` (4 instantiations of `PredictionRepository`)"** — promoting "4 references including the import" to "4 instantiations." Re-verified live: `grep "PredictionRepository(" backend/routers/prediction_router.py` returns lines 34, 61, 92 — **three** instantiations. The fourth reference is the import statement at line 6, not an instantiation. **The verification log's own wording is loose, and the main document inflates that looseness into a wrong count.** This is fabricated content.

**Verification log claims that survived but reveal looseness in v3 main-doc claims:**

- **Verification log Claim 22 documents "28+ modified files" in working tree.** Re-verified live: `git status --porcelain | wc -l` returns **103**. "28+" is technically consistent with 103 (≥ 28), but v3 § 1.1 and § 1.3 carry the stale "28+" figure rather than the live 103 — and v3 was drafted under verification discipline. The "+" plays threshold-game with the reader. Minor, not fabrication.

**Verification log coverage gaps (claims in v3 main doc with no log entry):**

- **§ 1.2 "three calibration bugs in one week"** — no entry. Number unverified.
- **§ 1.2 "14 Gonzo Sauce features"** — also stated in § 9.11 and A.3. No entry verifying the count is 14. (gonzo_features.py exists, verified, but the count of 14 is asserted four times without a verification entry.)
- **§ 1.2 Bug #28 "failed silently for at least three days before being noticed"** — no entry.
- **§ 9.12 calibration bypass at `wr_inference_service.py:616-628` "for ALL styles"** — code re-verified against live (the comment block says "All styles (including gonzo_sauce) bypass calibration at inference tonight"), but no log entry for this claim. The line range and the all-styles claim are accurate, but coverage gap exists.
- **§ 1.4 DD section numbers** — log Claim 23 says "all present" without listing the specific numbers cited (§ 4, § 4.5, § 5, § 10).
- **§ 1.4 "DD has multiple canonical objects" + the four headings cited** — partial: log Claim 23 names them, but doesn't show the section-number-to-canonical-object mapping is verified rather than asserted.
- **§ 7.5 second candidate Forbidden Pattern** ("Adding feature engineering logic to either `model/shared/data_loader.py` or `backend/services/feature_engineering_service.py`") — no log entry verifying both files exist with FE logic. (Independently verified by me — both exist — but coverage gap in the log.)

**Net assessment of verification work:** discipline mostly held. The substantive failure is the A.4 inflation (F1), which the verification log itself partly enabled by writing "4 references including the import" instead of "3 instantiations + 1 import line." This is the kind of looseness that lets fabrication slip through when the main document drafter reads the log entry quickly. The v3 verification log is a real safeguard — but the safeguard had a soft spot on Claim 16 that the main doc walked through.

---

## v2 finding regression check

| v2 finding | v3 fix verified? | Notes |
|---|---|---|
| Q1.1: 3 INACTIVE Lambdas | ✓ FIXED | § 2.3 names `equine-ingestion`, `equine-feature-engineering`, `equine-results`; verified live |
| Q1.2: A.4 deprecated example replaced | ✗ **REGRESSED** | New `predictions` table example is conceptually correct, but the count "4 instantiations" is wrong (F1). Replacing one factual error with another is not a fix. |
| Q1.3: A.1 / § 9.13 fictional function removed | ✓ FIXED | A.1 and § 9.13 now use the real `get_active_model_by_type(model_type: str)` and explicitly note the style-aware variant doesn't exist. Honest framing. |
| Q1.4: § 7.12 grandfathering integrates Tony's Q1/Q2 | ✓ FIXED | § 7.12 lists 001–011 keep legacy, 012+ uses dated format, runner unchanged. |
| Q1.5: Phase arithmetic 9–19 | ✓ FIXED | § 3.7: "low 2+4+1+1+1 = **9 weeks**; high 4+8+2+2+3 = **19 weeks**." Arithmetic correct. |
| Q2.5 (MATERIAL): Tier 2 worked example added | ✓ ADDRESSED w/ caveat | A.7 added but Tier 2 was retired in v3 § 6.5. A.7 frames itself as "documentation pattern reference." Internally consistent with the retirement. (See Q4 finding below — `<SPEC_GAP>` vs `<FRAMEWORK_GAP>` inconsistency.) |
| Q2.6 (MATERIAL): Bug #28 has destination | ✓ FIXED | § 8.2 + § 4.3 + § 10.5 + § 11 all consistently say PHASE_5_BACKLOG.md is created at Phase 0 exit with Bug #28 as first entry. |
| Q4.3 (MATERIAL): § 7.4 cross-cutting What-Was-Fixed scope rule | ✓ FIXED | § 7.4: "canonical entry lives in document whose discipline most directly prevents recurrence; cross-references from related documents; no duplication." |

**Verdict:** 7 of 8 sampled v2 findings cleanly fixed in v3; Q1.2 regressed by replacing one wrong example with a different-but-still-wrong count.

---

## Question 1: Unverifiable claims / verification gaps

1. **§ 7.10 "Steps 5 and 6 happen in the same working session — not 'commit today, deploy tomorrow' except by explicit operator decision."** This is policy, not factual. It is NOT in Tony's locked Q3 language (which only specifies the emergency carve-out). The drafting spec asked CC to integrate Tony's Q3 verbatim — CC additionally interpolated this sentence. No verification log entry covers it (it isn't a verifiable claim, but it IS a policy claim attributed to no one). CC has effectively introduced operator policy without operator confirmation.

2. **§ 7.12 "non-production database" — claim that "dev Aurora cluster ... does NOT currently exist for EE."** Plausible, but the verification log has no entry. I did not run `aws rds describe-db-clusters` to independently verify. Coverage gap on a claim § 7.12 leans on heavily.

3. **§ 7.13 Layer 3 + § 7.11 "silence convention" — assertion that the bible-touching-vs-not split is determinable from commit message prefix.** No mechanical specification of HOW Layer 3 is enforced. The rule reduces to "Tony reviews bible diffs on commits whose message starts with `bible:`." Not verifiable, just convention. But not stated as such — stated as enforcement layer.

4. **§ 8.5 "AWS vs API endpoint" rule.** The rule says: "If the serving Lambda is INACTIVE, the API endpoint either fails or serves stale cached state; either way, AWS wins." I did not test an INACTIVE-Lambda-serving endpoint. The dashboard endpoint, cited as the verification example for this rule, is served by `equine-inference` (Active), not by an INACTIVE Lambda — so the dashboard case does NOT actually exercise the INACTIVE-fails branch. The rule's actual behavior under INACTIVE-Lambda routes is asserted, not demonstrated. (And there are 41 routes; some may route to INACTIVE Lambdas.)

5. **§ 1.2 "Bug #28 failed silently for at least three days before being noticed" + "circa 2026-04-30."** The dates and the silent-failure duration aren't in the verification log. Inherited from operator memory file (referenced).

6. **§ 1.2 "three calibration bugs in one week" — no log entry.**

7. **§ 1.2 + § 9.11 + A.3 "14 Gonzo Sauce features" — count repeated four times, no log entry verifying it.**

8. **§ 7.13 enforcement-failure recovery: "Drift is detected during the next audit cycle (Phase 5 sessions audit recent commits against bible diff)."** "Next audit cycle" is undefined. Phase 5's audit cadence is not specified anywhere in the document. The recovery procedure depends on a process that doesn't exist yet.

---

## Question 2: Scope gaps

1. **§ 7.13 Layer 1 pre-deploy checklist + § 7.10 emergency hotfix exception interaction is unspecified.** § 8.1 says "the two exceptions are aligned" — but that's about the § 8.1 unbounded-loss exception meeting § 7.10's hotfix carve-out, not about the pre-deploy checklist. Specifically: under emergency hotfix, does Tony still tick `[ ] git status clean`? `[ ] git log -1 shows current state`? `[ ] bible diff reviewed`? Tony's locked language says "deploy may proceed before commit" — so `git log -1 shows current state` is necessarily false. The checklist therefore CANNOT all-pass under the hotfix exception. Document is silent on which checklist items waive.

2. **PHASE_5_BACKLOG.md format chicken-and-egg.** Phase 0 exit prerequisite says "PHASE_5_BACKLOG.md created with Bug #28 as first entry." TRIAGE_QUEUE_SPEC.md — the document defining PHASE_5_BACKLOG.md format — is the LAST Phase 0 deliverable (per § 3.1 deliverable order 5). So PHASE_5_BACKLOG.md is created using a format defined by the just-locked TRIAGE_QUEUE_SPEC. Appendix A.5 acknowledges the gap ("Final format defined in TRIAGE_QUEUE_SPEC.md") but the META_PLAN itself doesn't articulate that the prerequisite IS gated on TRIAGE_QUEUE_SPEC locking. Sequencing is implicit, not explicit.

3. **§ 6.5 framework-rejection protocol uses `<SPEC_GAP>` markers; Appendix A.7 uses `<FRAMEWORK_GAP>` markers.** Two protocols, one purpose, two names. (See contradiction Q4.)

4. **§ 3.1 audit-CC error case** says "Tony decides whether the audit-CC needs the methodology refined or whether v3 missed something." Doesn't cover: Tony decision based on a wrong premise. Tony's Q4 was based on v2 audit's incorrect claim that deploy artifacts weren't gitignored. CC's verification surfaced the contradiction; v3 reframed accordingly. The reframing is documented in the verification log "Architectural questions surfaced for QB attention" #1, but § 3.1's edge-case enumeration doesn't name "Tony's locked decision was based on a wrong premise" as a category. Procedure was followed; the procedure itself isn't named.

5. **§ 6.5 "QB skims verification log to spot-check entries" — "spot-check" not quantified.** How many? 5? 50%? "A few"? The audit-CC discipline (this audit included spot-checking 8 of 23 entries) wasn't prescribed by v3. Asymmetric: audit-CC has implicit "spot-check substantively"; QB has "skim."

6. **§ 7.10 "Commits represent 'deploy-ready iteration states' — typically 3–5 per heavy session, not 20."** Defines "deploy-ready" in plain terms, but no rule for what to do when an in-progress session's iteration is NOT deploy-ready. Are non-deploy-ready commits forbidden? Allowed if not deployed? § 7.10's gating is on deploys, not commits — so technically non-deploy-ready commits are fine. But the framing "commits represent" rules out non-deploy-ready commits semantically. Tension unresolved.

7. **§ 3.1.2 META_PLAN.md duration estimate "2–5 days"** — but v1, v2, and v3 all dated 2026-05-03 (per cover and revision history). Either the estimate doesn't apply to v1–v3 (in which case the estimate is for what?) or the cover is wrong. Inconsistency between estimate scale and actual cadence.

---

## Question 3: Ambiguous language

1. **§ 6.5 "verifiable EE-specific claims" — boundary undefined.** "EE has 8 Lambdas" appears in v3 § 1.3 in passing. By the rule, this single fact in a methodology overview triggers Tier 3 for the entire document. The rule operates correctly here (META_PLAN IS Tier 3). But the rule does not specify a threshold: zero EE-specific claims = Tier 1; ≥1 claim = Tier 3. CONVERGENCE_CRITERIA.md is the only document § 4.1 keeps as Tier 1; can it actually be drafted with ZERO EE-specific claims when its purpose is generalizing § 5.3's discipline (which references EE-specific examples)? The rule may force CONVERGENCE_CRITERIA to also be Tier 3, retiring Tier 1 entirely.

2. **§ 6.5 "companion verification log."** For a document that is 95% methodology framing with 5% EE-specific examples (which is what META_PLAN approximates), does the log cover only the 5%, or every claim including framing? v3's own log covers concrete EE facts (counts, paths, signatures) but not policy claims (e.g., § 7.10 "Steps 5 and 6 happen in the same working session"). The rule's scope is ambiguous; v3 implicitly chose "concrete facts only," but didn't say so.

3. **§ 7.10 "same working session" — undefined.** Working day? Continuous editing window? Until next sleep? The carve-out clause (Tony deciding) makes this looser, but the default is unspecified.

4. **§ 7.13 Layer 1 "Pre-deploy checklist (Tony's responsibility, immediate-term)."** Is this a checklist Tony maintains in writing (e.g., a `.deploy-checklist.md` Tony ticks before each deploy), or a mental ritual? The format `- [ ] git status clean` etc. implies a written form, but no file path is specified. § 7.14 doesn't list a pre-deploy checklist file.

5. **§ 7.13 Layer 3 "bible-touching commits only."** Determined how? § 7.11's silence convention says non-bible-touching commits omit the prefix. So Layer 3 reduces to: "if the commit message starts with `bible:`, Tony reviews the bible diff." That's mechanical and verifiable, but never stated. Reader must connect dots between § 7.11 and § 7.13.

6. **§ 8.1 Bug #28 case study: "Loss is recoverable (backfill via fetch_results re-run after fix)."** Plausible but unverified. `equine-results` Lambda is INACTIVE (verified). `equine-fetch-results-nightly` EventBridge rule is ENABLED (verified) — but if `equine-results` Lambda is its target, the rule fires nothing. Whether `fetch_results` re-run actually backfills the affected payouts depends on architecture I haven't audited. Not in verification log. Could be wrong; v3 leans on it as a "stable known" exception case.

7. **§ 4.5 Tier 4 "Code in working tree (after pre-Phase-1 baseline commit): authoritative for 'what the system does'."** Authoritative for source state, but "what the system does" depends on what's deployed, not what's in the tree. Pre-baseline-commit, the deployed state diverges from the tree. Post-baseline-commit, they match (until the next deploy). Tier 4 reads as if working-tree-after-baseline-commit IS deployed state, which is true at exactly that commit instant.

8. **Appendix A.7 "Use this pattern when it helps; don't use it when it adds friction."** Wide latitude. The rule is "use judgment." Defensible — but it leaves BIBLE_STRUCTURE_SPEC's drafter free to either use slot delimiters or not. If the choice depends on drafter preference, two CC sessions executing the same spec could produce structurally different output (the convergence test failure mode being guarded against).

---

## Question 4: Contradictions

### Internal

1. **§ 4.1 vs § 6.5 — Tier 3 description.** § 4.1 row 1 says META_PLAN is Tier 3 with parenthetical "(CC-drafted under verification, CC-audited)." § 6.5 says Tier 3 is "CC drafts under QB spec, with verification log; CC audits." § 4.1 omits the "QB spec" component entirely. Either a section is wrong, or the rule is "QB writes spec, CC drafts" (per role definitions in § 6.1) and § 4.1's parenthetical is incomplete.

2. **§ 6.5 framework-rejection protocol vs A.7.** § 6.5 says CC returns drafts with a top-level `<SPEC_GAP>` note when the spec's premise is wrong. A.7 says: "If a template slot cannot be filled because the framework's structure is wrong... CC returns the document with `<FRAMEWORK_GAP: explanation>`." Two markers for the same scenario. Either rename one, or specify when each applies (e.g., `<SPEC_GAP>` for entire-document issues; `<FRAMEWORK_GAP>` for slot-level issues).

3. **§ 12 changelog "v3 corrects v2's factual errors" and § 7.14 "audit Q2.2 was wrong"** — vs Tony's Q4 wording. Tony's locked Q4 explicitly said "Add `.cf-distribution-id` and `.frontend-bucket` to `.gitignore`" as a Phase 0 prerequisite. v3 dropped the "add" instruction (because verification showed they're already there) and kept only the audit-sweep instruction. The reframing is correct on the facts and properly disclosed in the verification log "Architectural questions surfaced" section. But § 12 changelog says "Note: Verification revealed v2 audit Q2.2 was wrong" — without flagging that this also implicitly required revising Tony's Q4 instruction. Tony hasn't ratified the reframing. Per § 6.5 framework-rejection protocol, CC should have surfaced "spec premise is wrong" rather than silently revised. The verification log does surface — but the main doc § 12 reads as if v3 unilaterally corrected. This is a procedural ambiguity.

4. **§ 7.10 "If existing EE has uncommitted production code at Phase 0 exit"** — but § 3.1.1 makes the baseline commit a Phase 0 exit prerequisite. So at Phase 0 exit, there IS no uncommitted production code (by construction). § 7.10's "If" branch fires at a time that, by § 3.1.1, cannot exist. Internally redundant or contradictory.

5. **§ 4.5 (six-source hierarchy) vs § 8.5 (resolution rules).** § 4.5 lists `EE_CURRENT_STATE_DUMP.md` as **tier 6** (penultimate), and "Session logs" as tier 7. But § 4.5's introduction says "When sources conflict, this is the priority order" and only enumerates 7 tiers. § 8.5 adds a "Live state vs dump" resolution rule, which is just the tier 1 vs tier 6 conflict already implicit in § 4.5. Slight redundancy, no contradiction.

### External

6. **§ 7.14 "going-forward rule: any new deploy script that writes a machine-specific artifact must update `.gitignore` in the same commit. This is part of § 7.1's 'every change updates the bible' applied to repository hygiene."** § 7.1 is about *bible* updates. `.gitignore` is not a bible document. v3 conflates the bible-update discipline with gitignore hygiene. They're related disciplines, not the same one.

7. **§ 6.5 vs role definitions in § 6.1.** § 6.1 says CC "executes specs QB authors." § 6.5 says Tier 3 documents are "CC drafts under QB spec." § 4.1 (row 1) says META_PLAN is "CC-drafted under verification, CC-audited" — eliding the QB-spec layer. § 6.1 + § 6.5 are consistent with each other; § 4.1 is inconsistent with both.

---

## Question 5: Rushed sections

1. **§ 3.4 Phase 3 (Predictive Concept Inventory).** Only ~25 lines. Quality bar is one sentence. Document structure is one bullet list. Conflict resolution with Phase 1 cross-references is unspecified. v2 audit flagged this; v3 didn't develop further.

2. **§ 3.5 Phase 4 (Gap Analysis).** Slightly more developed than Phase 3 because of disposition gating, but the three deliverables (FEATURE_TAXONOMY, ML_RE_ARCHITECTURE_SPEC, COMPONENT_DISPOSITION) get one-line descriptions each. v2 audit flagged Phase 2/3/4 as rushed; v3 modestly improved Phase 2 (added the >5 MATERIAL → revision rule) but Phase 3 and Phase 4 remain skeletal.

3. **§ 3.6 Phase 5 (Execution).** Six lines. "Open-ended." Acceptable as a placeholder, but if Phase 5's audit cadence drives § 7.13 enforcement-failure recovery, the lack of specification here cascades.

4. **§ 7.13 Layer 1 pre-deploy checklist.** Five concrete checkboxes — better than v2 ("PR template (when adopted)"). But no specification of where the checklist lives, whether it's actually maintained, or what happens when Tony does the deploy ad-hoc without checking. The checkboxes look concrete but the enforcement is still mental ritual.

5. **§ 7.13 enforcement-failure recovery.** Three steps: drift detected, catch-up entry, accumulated drift triggers focused audit. Steps 1 and 3 depend on processes (Phase 5 audit cadence, "focused audit" definition) that aren't defined. Step 2 (catch-up entry with "noted retroactively" tag) is concrete. Two-thirds is hand-waved.

6. **§ 9.13 EE-specific anti-pattern (rewritten).** Now sharp on the verified facts (the function exists, takes only `model_type`, returns LIMIT 1 arbitrarily). But the FORBIDDEN/CORRECT contrast is weaker than § 9.11 and § 9.12: § 9.11 contrasts "single source of truth" with "two implementations + manual review"; § 9.12 contrasts "calibration applied" with "calibration bypassed for ALL styles, with chain Bug #15 → Bug #24"; § 9.13 contrasts "active model selected via X" with "active model currently selected via X — A style-aware variant is Phase 5.X.Y." The CORRECT pattern is essentially "name the gap." That's accurate but didactically thin.

---

## Question 6: Missing examples

1. **§ 7.12 migration discipline — no full example migration with both up and down blocks.** § 7.12 prescribes the down-block format inside a migration file, but doesn't show one. A 12-line example with `CREATE TABLE foo` up + `DROP TABLE foo` down + the delimiter comment block would make the pattern concrete.

2. **§ 7.11 commit message convention — no end-to-end example showing a bug-fix commit with both code change AND bible "What Was Fixed" entry.** The provided examples cover bible-touching, multi-doc, bible-only-docs cases. Missing: the canonical pattern of "bug fix commit references the new W.N entry being added."

3. **A.7 "skeleton with template slots" example — partly concrete, partly placeholder.** The 4.1 framework section is concrete (mandatory section list); the 4.2 fill section uses `<TEMPLATE: ... >` markers that themselves contain "[one slot per Phase 1 bible document]" placeholder. A second-level example of WHAT a filled template slot looks like (e.g., the actual Database & Schema TOC after a CC fill, alongside the unfilled template) would make the pattern reproducible. As written, A.7 shows the pre-fill state but not the post-fill state.

4. **§ 4.5 source-priority hierarchy — no example showing how a specific conflict actually resolves.** The Lambda-INACTIVE-but-DB-has-rows case is referenced abstractly. A concrete: "Question: 'is `equine-results` running today?' → AWS says INACTIVE → DB shows last result row from 2026-04-30 → bible records: 'INACTIVE since on or before 2026-04-30; final results row produced before deactivation'" would ground the rule.

5. **§ 6.5 framework-rejection protocol — no example of `<SPEC_GAP>` annotation in practice.** Tells CC what to do when verification reveals the spec is wrong; doesn't show what the marker looks like in a draft.

---

## Additional adversarial findings

### A. v2 finding regression

Per the table above. **Q1.2 regressed** — the new A.4 example replaces a wrong example with a different-but-still-wrong count ("4 instantiations"). The replacement is conceptually correct (legacy `predictions` table is genuinely deprecated and still read by multiple routers), but the count is off. This is a v3 finding.

### B. Verification log audit

8 spot-checked entries: 7 hold up, 1 internally inconsistent (Claim 16's "4 references including the import" is loose phrasing that the main doc walked through to inflate "4 references" → "4 instantiations"). See F1 above.

### C. Tier model coherence stress test

§ 4.1 lists CONVERGENCE_CRITERIA as Tier 1 ("only document with no EE-specific examples"). I cannot verify this without reading CONVERGENCE_CRITERIA.md (which doesn't exist yet). If CONVERGENCE_CRITERIA must reference EE patterns to generalize § 5.3's discipline (which itself uses EE-specific examples like "8 Lambdas" vs "9 Lambdas" as material-difference examples), then CONVERGENCE_CRITERIA may inevitably need EE-specific claims and become Tier 3, retiring Tier 1 entirely. v3 doesn't acknowledge this risk.

The "verification log alongside Tier 3 draft" rule (§ 6.5) is silent on whether **Tier 1 audit responses** require verification logs. Audit responses are themselves drafted under verification (this audit response is) — but § 6.5's verification-log rule is scoped to drafts, not audits. Edge case worth resolving.

### D. v3 reframing of Tony's Q4

Tony's locked Q4 had two parts: (1) "Add `.cf-distribution-id` and `.frontend-bucket` to `.gitignore`"; (2) "Audit deploy scripts for other untracked artifacts during Phase 0." v3 verification confirmed part (1) is already done, so v3 § 7.14 dropped that step and kept only part (2). The verification log surfaces this for QB/Tony attention. Procedurally correct under § 3.1's "audit findings with downstream consequences" edge case.

But: Tony has not ratified the reframing as of v3 lock-pending. The reframing is informationally honest (the two artifacts ARE in `.gitignore`), but architecturally the document substitutes a less-prescriptive task for Tony's more-prescriptive instruction. If Tony's intent in Q4 was "I want this baseline written into the methodology even though I haven't checked," v3 has soft-substituted "QB will audit; assume nothing." The substitution is defensible — but it's worth surfacing as a Tony-confirmation prerequisite to lock, not as already-resolved.

### E. § 7.10 emergency hotfix language drift

I compared v3 § 7.10's emergency hotfix block against Tony's locked Q3 language in the v2-audit-derived spec. **Verbatim match:** the four bulleted requirements (emergency flag, commit within 4 hours, bible entry within 24 hours, triage queue entry, two deploys/7-day rule) are reproduced. The framing sentence ("In cases where production is broken and waiting for commit + bible review would cause user-facing harm or data loss, deploy may proceed before commit, subject to:") is also verbatim. The rationale paragraph quotes Tony's stated rationale verbatim. **No drift.**

### F. Verification log format/completeness

23 entries; format (Claim/Document location/What was checked/What was found/Survived/Action) is followed in every entry. Methodology preamble is clear. Verification summary at the end is concise. **Format compliance: clean.** Only structural critique is Claim 16's loose "4 references including the import" phrasing that enabled the main-doc fabrication (F1).

### G. § 3.1.2 estimate inconsistency

"META_PLAN.md (v3) | 2–5 days" but the cover dates v1, v2, and v3 all on 2026-05-03. Either the table estimate is for "from spec to lock through audit cycles" (in which case v3 is mid-estimate) or it's effort-only (in which case 2–5 days substantially overshot the actual cadence). Inconsistency unresolved.

---

## Severity assessment

| # | Finding | Section | Severity |
|---|---|---|---|
| F1 | A.4 says "4 instantiations of `PredictionRepository`" — actual count is 3 | § A.4 | **BLOCKER (fabricated content)** |
| 1 | § 4.1 Tier 3 description elides QB-spec layer; inconsistent with § 6.5 + § 6.1 | § 4.1 vs § 6.5 / § 6.1 | MATERIAL |
| 2 | `<SPEC_GAP>` (§ 6.5) vs `<FRAMEWORK_GAP>` (A.7) — same protocol, two markers | § 6.5 vs A.7 | MATERIAL |
| 3 | § 7.10 "Steps 5 and 6 happen in the same working session" is CC-interpolated policy not in Tony's locked language | § 7.10 | MATERIAL |
| 4 | § 7.13 Layer 1 pre-deploy checklist + § 7.10 emergency hotfix interaction unspecified | § 7.13 + § 7.10 | MATERIAL |
| 5 | § 7.13 enforcement-failure recovery references undefined "next audit cycle" / Phase 5 audit cadence | § 7.13 | MATERIAL |
| 6 | § 8.5 "AWS vs API endpoint" rule for INACTIVE Lambda case is asserted without verified test endpoint | § 8.5 | MATERIAL |
| 7 | PHASE_5_BACKLOG.md created at Phase 0 exit using format defined by Phase-0-ending TRIAGE_QUEUE_SPEC.md — sequencing implicit, not explicit | § 8.2 + § 11 | MINOR |
| 8 | Verification log Claim 22 / § 1.1 / § 1.3 says "28+ modified files"; live shows 103 | § 1.1, § 1.3, log Claim 22 | MINOR |
| 9 | "14 Gonzo Sauce features" stated four times without verification log entry | § 1.2, § 9.11, A.3 | MINOR |
| 10 | § 7.10 "If existing EE has uncommitted production code at Phase 0 exit" branch fires at a time that § 3.1.1 makes impossible | § 7.10 | MINOR |
| 11 | § 7.14 conflates `.gitignore` hygiene with § 7.1 bible-update discipline | § 7.14 | MINOR |
| 12 | § 6.5 "QB skims verification log to spot-check entries" — "spot-check" not quantified | § 6.5 | MINOR |
| 13 | § 7.13 Layer 1 unclear whether pre-deploy checklist is a maintained file or mental ritual | § 7.13 | MINOR |
| 14 | § 3.1.2 META_PLAN duration estimate (2–5 days) inconsistent with v1/v2/v3 same-day cover | § 3.1.2 | MINOR |
| 15 | § 7.12 prescribes down-block format but no full example migration shown | § 7.12 | MINOR |
| 16 | § 7.11 missing end-to-end example showing bug-fix commit + bible W.N entry reference | § 7.11 | MINOR |
| 17 | A.7 shows pre-fill template state but no post-fill example | A.7 | MINOR |
| 18 | § 4.5 source priority lacks worked example | § 4.5 / § 8.5 | MINOR |
| 19 | § 6.5 framework-rejection protocol no `<SPEC_GAP>` annotation example | § 6.5 | MINOR |
| 20 | § 9.13 CORRECT pattern is "name the gap" — didactically thinner than § 9.11 / § 9.12 | § 9.13 | MINOR |
| 21 | § 3.4 Phase 3, § 3.5 Phase 4 still skeletal (v2 carry-over) | § 3.4, § 3.5 | MINOR |
| 22 | Verification log coverage gaps on: Bug #28 dates, three-bugs-in-one-week, calibration bypass code claim, DD section number mapping | log | MINOR |
| 23 | § 12 changelog reframes Tony's Q4 as "v2 audit Q2.2 was wrong" without surfacing that Tony's Q4 instruction also needs ratification of the reframing | § 12 | MINOR |
| 24 | § 7.10 "deploy-ready iteration states" semantically rules out non-deploy-ready commits but § 7.10 only gates deploys | § 7.10 | STYLE |

---

## Material findings count

**6 MATERIAL** findings (#1–#6 in the table above). Justification per Tony's "use judgment" rule:

- **#1 (§ 4.1 vs § 6.5 Tier 3 description):** MATERIAL because methodology coherence is the document's load-bearing function. A reader who reads § 4.1 first and § 6.5 second gets two definitions of Tier 3 — and the "QB spec" component is the gating artifact, not optional. This is not "missing example" territory; it's "the methodology table contradicts the methodology section."
- **#2 (`<SPEC_GAP>` vs `<FRAMEWORK_GAP>`):** MATERIAL because the protocol governs what CC does when verification reveals the spec is wrong. Two names = ambiguity at the precise moment ambiguity costs most. A fresh CC executing the methodology won't know which marker to use.
- **#3 (§ 7.10 interpolated policy):** MATERIAL because v3 introduces operator policy ("same working session") in a section that also includes Tony's verbatim locked language. A reader can't easily tell which sentences are Tony's locked rules vs which are CC's interpolated framing. v3's drafting discipline includes "no fabrication," but policy interpolation is a different failure mode the discipline didn't catch.
- **#4 (Layer 1 + emergency hotfix interaction):** MATERIAL because the pre-deploy checklist physically cannot all-pass under emergency hotfix (`git log -1 shows current state` is false by construction), and the document is silent on which boxes waive. Operator running an emergency deploy in Phase 5 has no documented guidance.
- **#5 (enforcement-failure recovery):** MATERIAL because the recovery procedure depends on Phase 5 audit cadence that isn't defined anywhere in any Phase 0 document. The recovery is procedurally hollow.
- **#6 (§ 8.5 AWS-vs-API rule):** MATERIAL because the rule is asserted to handle INACTIVE Lambdas serving routes, and the route count is 41. Some routes plausibly target INACTIVE Lambdas; the rule's behavior under that case is asserted, not verified. v3's verification discipline didn't extend to testing route-level behavior.

**MINORs** (#7–#23): individually small; cumulative weight does not promote any to MATERIAL.

**STYLE** (#24): single tension in framing, not load-bearing.

---

## Fabricated-content findings

**ONE.**

- **F1: § A.4 — "`prediction_router.py` (4 instantiations of `PredictionRepository`)" is wrong.** Actual instantiations: 3 (lines 34, 61, 92, verified live via `grep`). The fourth reference is the import on line 6, not an instantiation. The verification log (Claim 16) acknowledges this with the phrase "4 references including the import" — but the main doc inflates "4 references" into "4 instantiations." This is fabricated content per Tony's hard rule, regardless of whether the verification log enabled it through loose phrasing.

Per Tony's threshold ("zero fabricated-content findings to lock"), this single finding is sufficient to fail v3.

---

## Recommendation

**Revise + re-audit.** Specifically:

1. **Fix F1 (BLOCKER, fabricated content):** rewrite A.4 to read "`prediction_router.py` (3 instantiations of `PredictionRepository` at lines 34, 61, 92, plus 1 import)" — or simply "3 instantiations." Update the verification log Claim 16 to the same — "3 instantiations + 1 import = 4 references" — so the looseness that enabled the inflation is closed.

2. **Address the 6 MATERIALs systematically:**
   - Sync § 4.1's Tier 3 parenthetical to match § 6.5 ("CC drafts under QB spec, with verification log; CC audits").
   - Pick one marker name (`<SPEC_GAP>` or `<FRAMEWORK_GAP>`) and use it in both § 6.5 and A.7. (`<SPEC_GAP>` is more general; `<FRAMEWORK_GAP>` is a narrow case of it. Either keep both with explicit "use X for whole-doc, Y for slot-level" or collapse to one.)
   - Either remove the "Steps 5 and 6 happen in the same working session" sentence (it's CC-interpolated policy not in Tony's Q3) OR surface it to Tony for ratification before lock.
   - Specify Layer 1 checklist behavior under emergency hotfix: which boxes waive, which still apply.
   - Either define Phase 5 audit cadence in § 3.6 (and § 7.13 references it) OR rewrite § 7.13's enforcement-failure recovery to not depend on undefined cadence.
   - Either run the live test on an INACTIVE-Lambda-serving route (if such a route exists in the 41) and document the actual behavior, OR weaken § 8.5 to "AWS state is authoritative for whether a route is currently being served; API behavior under INACTIVE-Lambda routing is route-specific and to be documented per route in the API & Frontend Bible."

3. **Consider promoting MINORs that cluster:** the verification-log-coverage gaps (#9, #22, "28+ modified files") share a root: v3's verification discipline applied rigorously to AWS/code claims and loosely to operator-stated history claims (bug timing, count of features). A separate revision pass extending verification log entries to cover narrative claims would close this cluster.

4. **Re-audit after the 7 fixes (1 BLOCKER + 6 MATERIAL).** v3's structure and direction are sound. The verification discipline mostly worked. The fabrication slipped on a single count where the verification log itself was loose; closing that loop is straightforward.

The bar Tony set is hard ("zero fabricated content"). v3 came close — one inflation in one example, in a paragraph that's otherwise carefully verified. But "close" doesn't lock under that bar.

---

End of audit.
