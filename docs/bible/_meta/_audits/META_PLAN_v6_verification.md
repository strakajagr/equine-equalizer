# META_PLAN v6 — Verification Log

**Document:** META_PLAN_v6_verification
**Companion to:** META_PLAN.md v6
**Author:** CC (drafting under verification discipline)
**Date:** 2026-05-04
**Purpose:** Per-claim verification record. v6 is a surgical patch pass over v5; most entries inherit from v5's log with re-verified-2026-05-04 timestamps. Two entries have substantive updates: Claim 20 (ECS task families full enumeration) and Claim 15c (NEW — Bug #28 exacta payout claim re-grounded against operator memory file's verbatim symptom statement).

**Verification methodology:**
- "Live AWS" = `aws` CLI against operator's account 584812014683
- "Live API" = HTTPS request against `https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com`
- "Codebase" = file read against working tree at `/home/strakajagr/projects/equine-equalizer/`
- "Operator memory" = file read against `~/.claude/projects/-home-strakajagr/memory/<filename>.md`
- "Operator-stated" = claim sourced from Tony's verbal/written framing in this drafting cycle's spec; verified against operator framing, NOT against primary code/AWS/DB source. Per § 4.5 source-priority tier 5.
- "Inherited from v5 log Claim N — re-verified [date]" = entry imported from `META_PLAN_v5_verification.md` and re-run; value confirmed unchanged

**Verification log precision rule (locked v4, scope broadened in v5, applied throughout v6):**
Counts are decomposed into definitions / instantiations / imports / uses, never aggregated as compressible-by-a-reader phrasings. Anything aggregable is shown both as components and as a sum. Scope: rule applies broadly — to any aggregable count anywhere in a Tier 3 document.

**Methodology-interpolation rule (locked v5, expanded scope in v6):**
CC does not invent binary tests, cadence rules, completeness criteria, scoring rubrics, severity thresholds, iteration caps, percentage criteria, procedural sequencing rules, or other CC-prescribed methodology constructs Tony has not explicitly ratified. v6 grandfathering clause: pre-existing QB-drafted content from earlier cycles is grandfathered; CC-introduced content from earlier cycles is subject to the rule's retroactive sweep.

---

## Claim 1: Lambda function count

**Claim:** EE has 8 Lambda functions, decomposed as 5 Active + 3 INACTIVE.
**Document location:** v6 § 1.3, § 2.3
**What was checked (re-verified 2026-05-04):** `aws lambda list-functions` + per-function `get-function`
**What was found:** 8 functions. Active (5): equine-inference, equine-wr-inference, equine-pl-inference, equine-ls-inference, equine-nyra-workouts. INACTIVE (3): equine-ingestion, equine-feature-engineering, equine-results.
**Survived:** Yes
**Action:** Inherited from v5 log Claim 1 — re-verified

## Claim 3: EventBridge rule count

**Claim:** 13 rules, decomposed as 10 ENABLED + 3 DISABLED.
**Document location:** v6 § 1.3, § 2.3
**What was checked (re-verified 2026-05-04):** `aws events list-rules --name-prefix equine`
**What was found:** 13 rules; ENABLED (10) and DISABLED (3) lists fully enumerated in v6 § 2.3.
**Survived:** Yes
**Action:** Inherited from v5 log Claim 3 — re-verified

## Claim 4: Database table count

**Claim:** 14 tables + 1 materialized view.
**Document location:** v6 § 1.3, § 2.3
**Survived:** Yes
**Action:** Inherited from v5 log Claim 4 — re-verified

## Claim 5: Migration filename format and duplicate-005 case

**Claim:** 12 migration files; 11 unique sequence numbers; sequence 005 duplicated.
**Document location:** v6 § 7.12
**Survived:** Yes
**Action:** Inherited from v5 log Claim 5 — re-verified

## Claim 6: Migration runner mechanism

**Claim:** `migrate.py` tracks applied migrations by filename in `schema_migrations` table.
**Document location:** v6 § 7.12
**Survived:** Yes
**Action:** Inherited from v5 log Claim 6 — re-verified

## Claim 7: Model registry counts

**Claim:** 88 entries, decomposed as 45 active + 43 inactive.
**Document location:** v6 § 1.3, § 9.13, A.1
**What was checked (re-verified 2026-05-04):** `curl /dashboard/metrics`, parse `model_history`; partition by `is_active`
**What was found:** total=88, active=45, inactive=43. Sum verified: 45 + 43 = 88.
**Survived:** Yes
**Action:** Inherited from v5 log Claim 7 — re-verified

## Claim 8: API Gateway route count

**Claim:** 41 routes on `gb5qlfy10h`.
**Document location:** v6 § 8.5
**Survived:** Yes
**Action:** Inherited from v5 log Claim 8 — re-verified

## Claim 9: `get_active_model_by_type` signature and SQL

**Claim:** Function takes only `model_type: str`; SQL `WHERE is_active = true AND model_type = %s LIMIT 1`; no `_and_style` variant exists.
**Document location:** v6 § 9.13, Appendix A.1
**Survived:** Yes
**Action:** Inherited from v5 log Claim 9 — re-verified

## Claim 10: `model/features/feature_definitions.py` runtime state

**Claim:** ALL_FEATURES = 73 at runtime; not orphaned; imported by 2 production paths.
**Document location:** v6 § 4.5
**Survived:** Yes
**Action:** Inherited from v5 log Claim 10 — re-verified

## Claim 11: `.gitignore` already contains deploy artifacts

**Claim:** Four artifacts already gitignored.
**Document location:** v6 § 7.14
**Survived:** Yes
**Action:** Inherited from v5 log Claim 11 — re-verified. Tony ratified the v3 reframing in the v4 cycle.

## Claim 12: Deploy script artifact writes

**Claim:** `scripts/deploy-backend.sh:243` writes `.frontend-bucket`; line 262 `.cf-distribution-id`; line 229 `frontend/.env.production`.
**Document location:** v6 § 7.14
**Survived:** Yes
**Action:** Inherited from v5 log Claim 12 — re-verified

## Claim 13: DD bible line count

**Claim:** 2,578 lines.
**Document location:** v6 § 1.2, § 3.2
**Survived:** Yes
**Action:** Inherited from v5 log Claim 13 — re-verified

## Claim 14: DD bible "What Was Fixed / Common Mistakes / Forbidden Patterns / Deprecated Fields" section heads

**Claim:** § 18 at L2160; § 19 at L2258; § 20 at L2394; § 21 at L2456.
**Document location:** v6 § 1.4
**Survived:** Yes
**Action:** Inherited from v5 log Claim 14 — re-verified

## Claim 14b: DD bible canonical-object section numbers and lines

**Claim:** § 4 at L590, § 4.5 at L800, § 5 at L1365, § 10 at L1657.
**Document location:** v6 § 1.4
**Survived:** Yes
**Action:** Inherited from v5 log Claim 14b — re-verified

## Claim 15: Bug #28 line reference

**Claim:** `parse_payout(N)` calls at `hrn_scraper.py:802-804`.
**Document location:** v6 § 1.2, Appendix A.5
**Survived:** Yes
**Action:** Inherited from v5 log Claim 15 — re-verified

## Claim 15b: Bug #28 silent-failure window

**Claim:** Discovery 2026-05-03; sharp regression beginning 2026-04-30; window at least three days.
**Document location:** v6 § 1.2
**Survived:** Yes
**Action:** Inherited from v5 log Claim 15b — re-verified

## Claim 15c (NEW v6): Bug #28 per-payout-type bounded-loss claim

**Claim:** Per the operator memory file's symptom statement (verbatim): `win_payout` and `daily_double_payout` NULL since 2026-04-30; place, show, and exacta payouts still populate. The memory file additionally flags DD pool extraction at `hrn_scraper.py:814` as "likely has the same root cause" — distinct from the `daily_double_payout` field already accounted for in the result-dict.
**Document location:** v6 § 1.2, § 8.1
**What was checked:** Read operator memory file `~/.claude/projects/-home-strakajagr/memory/equine-equalizer-bug-28-hrn-scraper.md`
**What was found (verbatim from the file):**

Symptom block (lines 9-10): `"starting 2026-04-30, all results.win_payout and results.daily_double_payout rows are NULL across every track/race scraped via HRN. Place, show, and exacta payouts still populate."`

DD pool extraction note (line 30): `"DD pool extraction (hrn_scraper.py:814 'pool' table loop) likely has the same root cause — same site-wide column shift."`

Decomposed: 5 payout fields total in the affected dictionary
- `win_payout` — NULL since 2026-04-30 (verified per file)
- `daily_double_payout` — NULL since 2026-04-30 (verified per file)
- `place_payout` — populates with shifted values (verified per file)
- `show_payout` — populates with shifted values (verified per file)
- `exacta_payout` — still populates per file's symptom statement (verified per file)

Plus 1 distinct extraction path: DD pool extraction at line 814 — flagged as "likely has the same root cause" but NOT verified by file as bounded; Phase 1 audit's job.

Total: 5 result-dict fields with explicit per-field status + 1 distinct-path uncertainty (DD pool extraction).

**Survived:** Yes
**Action:** New in v6. Closes v5 audit's MINOR #5 with the verified-correct claim per operator memory file. Note: the v5 audit's characterization that the memory file was "silent on exacta status" was itself wrong — the file explicitly states "Place, show, and exacta payouts still populate." This is a "Tony's locked decision based on a wrong premise" instance per § 3.1's edge case enumeration; v6 surfaces it and applies the verified-fact reframing rather than silently complying with the v5-audit-inferred softening that contradicts the source.

**Architectural question for QB attention:** The v5 audit-CC misread the memory file. Tony's v6 spec explicitly authorized the contingency: "If the memory file makes statements about exacta status that contradict this softening, flag in the verification log." v6 keeps the original v5 claim about exacta (faithful to memory file) AND adds the DD-pool-extraction nuance the memory file does flag. Tony should confirm the v6 reframing.

## Claim 16: Legacy `predictions` table — A.4 example

**Claim:** prediction_router.py = 1 import + 3 instantiations = 4 references; race_router.py = 1 import + 1 instantiation = 2 references; legacy table not dropped; 6,600 rows live.
**Document location:** v6 Appendix A.4
**Survived:** Yes
**Action:** Inherited from v5 log Claim 16 — re-verified

## Claim 17: ECR image count in CDK assets bucket

**Claim:** 5 images in `cdk-hnb659fds-container-assets-584812014683-us-east-1`.
**Document location:** v6 § 2.3
**Survived:** Yes
**Action:** Inherited from v5 log Claim 17 — re-verified

## Claim 18: S3 bucket count

**Claim:** 4 EE-related S3 buckets.
**Document location:** v6 § 2.3
**Survived:** Yes
**Action:** Inherited from v5 log Claim 18 — re-verified

## Claim 19: Secrets Manager entries

**Claim:** 3 secrets = 1 used + 2 unused.
**Document location:** v6 § 2.3
**Survived:** Yes
**Action:** Inherited from v5 log Claim 19 — re-verified

## Claim 20: ECS task definition families (UPDATED v6 — full enumeration)

**Claim:** 5 ECS task families starting with `equine`, fully enumerated: `equine-training`, `equine-training-daily-full`, `equine-training-manual`, `equine-training-pl`, `equine-training-win-prob`.
**Document location:** v6 § 2.3
**What was checked (re-verified 2026-05-04):** `aws ecs list-task-definition-families --query 'families[?starts_with(@, \`equine\`)]' --output text`
**What was found:** Exactly 5 families: equine-training, equine-training-daily-full, equine-training-manual, equine-training-pl, equine-training-win-prob.

Decomposed: 5 families, each named explicitly. The dump listed 3 (missing `equine-training` and `equine-training-win-prob`); v6 records all 5 inline per Tony's broad-sweep precision rule.
**Survived:** Yes
**Action:** Modified from v5 log Claim 20. v5 named only 2 of 5 inline (the dump-missed ones); v6 names all 5 in § 2.3. Per Tony's MINOR #6 in the v6 cycle (broad-sweep precision rule extension).

## Claim 21: Phase duration arithmetic

**Claim:** Per-phase highs sum to 19 weeks; lows sum to 9 weeks.
**Document location:** v6 § 3.7
**Survived:** Yes
**Action:** Inherited from v5 log Claim 21 — re-verified

## Claim 22: Git working-tree state

**Claim:** 103 entries = 74 untracked + 29 modified. Last commit `2a3d758` 2026-03-15.
**Document location:** v6 § 1.1, § 1.3
**What was checked (re-verified 2026-05-04):** `git log -1`, `git status --porcelain | wc -l`, `git status --porcelain | awk '{print $1}' | sort | uniq -c`
**What was found:** Last commit hash 2a3d758, date 2026-03-15. Total: 103. Decomposed: 74 ?? (untracked) + 29 M (modified) = 103.
**Survived:** Yes
**Action:** Inherited from v5 log Claim 22 — re-verified

## Claim 23: DD bible structural facts

**Claim:** DD multi-runtime; multiple canonical objects.
**Document location:** v6 § 1.4
**Survived:** Yes
**Action:** Inherited from v5 log Claim 23 — re-verified

## Claim 24: "14 Gonzo Sauce features" count

**Claim:** 14 = Speed (4) + Trajectory (7) + Class (3) per gonzo_features.py docstring.
**Document location:** v6 § 1.2, § 9.11, A.3
**Survived:** Yes
**Action:** Inherited from v5 log Claim 24 — re-verified

## Claim 25: "Three calibration bugs in one week"

**Claim:** Verbatim quote from gonzo_features.py:7-11 docstring.
**Document location:** v6 § 1.2, A.3
**Survived:** Yes
**Action:** Inherited from v5 log Claim 25 — re-verified

## Claim 26: Calibration bypass at `wr_inference_service.py`

**Claim:** Lines 616-626 = comment block at 616-625 (10 lines) + bypass operation `handicapping_probs = ranker_probs.copy()` at line 626 (1 line). Lines 627-628 are blank + start of unrelated 0-PP override block.
**Document location:** v6 § 1.2, § 9.12, A.2
**Survived:** Yes
**Action:** Inherited from v5 log Claim 26 — re-verified

## Claim 27: `gonzo_features.py` import sites

**Claim:** 2 import sites with 2 different qualified names: `model/shared/data_loader.py:45` (`from shared.gonzo_features`) and `backend/services/feature_engineering_service.py:16` (`from model.shared.gonzo_features`).
**Document location:** v6 Appendix A.3
**Survived:** Yes
**Action:** Inherited from v5 log Claim 27 — re-verified

## Claim 28: Derby Day 2026 counterfactual loss claim

**Claim:** Operator-stated; not independently verified at primary-source granularity. v6 § 3.2.1 prose flags this explicitly.
**Document location:** v6 § 3.2.1
**What was checked (carry-over from v5):**
1. `ls ~/.claude/projects/-home-strakajagr/memory/ | grep -i derby` → no specific Derby file
2. `grep -nE "(derby|Derby|counterfactual|108|150|gonzo.*general|rank=1)" docs/sessions/SESSION_005.md` → 1 hit on "Derby Day Easter Egg" UI, not analysis
3. `equine-equalizer-bug-28-hrn-scraper.md` mentions "Derby Day counterfactual analysis" as a use case but does NOT cite specific dollar amounts
4. `wr_inference_service.py:622` references "Wonder Dean JPN at #1 in Derby smoke test" — corroborates gonzo-vs-general rank-1 issue but not dollar amounts
**What was found:** Same as v5 — specific dollar amounts unverifiable; lived-experience direction operator-stated.
**Survived:** Partial. Source authority: operator-stated (per § 4.5 tier 5). Disclosure preserved in v6 § 3.2.1 prose.
**Action:** Inherited from v5 log Claim 28 — re-verified

---

## Verification summary

**Total claims documented:** 29 (28 inherited from v5 + 1 new — Claim 15c on Bug #28 per-payout decomposition; 1 modified for v6 — Claim 20 ECS full enumeration)
**Survived as-is (re-verified live 2026-05-04):** 27
**Modified for v6:** 1 (Claim 20 — ECS task families fully enumerated per Tony's MINOR #6 broad-sweep precision-rule extension)
**New v6 claim:** 1 (Claim 15c — Bug #28 per-payout-type decomposition with verbatim memory file quote)
**Dropped:** 0
**Architectural questions surfaced for QB attention:** 1
- The v5 audit-CC's characterization of the operator memory file as "silent on exacta payout status" was itself incorrect — the file's symptom statement explicitly reads "Place, show, and exacta payouts still populate." Tony's v6 spec explicitly authorized this contingency ("If the memory file makes statements about exacta status that contradict this softening, flag in the verification log"). v6 applied a reframing faithful to the memory file (preserves exacta-populates claim, adds the DD-pool-extraction nuance the memory file does flag) rather than silently complying with the v5-audit-inferred softening that contradicted the source. Per § 3.1 edge case "Tony's locked decision based on a wrong premise," surfacing rather than silent compliance is the correct procedure. Tony should ratify the v6 reframing.

**Verification log precision rule scope (locked v5, applied v6):** The rule applies broadly — to any aggregable count anywhere in a Tier 3 document. v6 extends application to ECS task families (5 families enumerated by name) and to Bug #28 payout decomposition (5 result-dict fields with per-field status + 1 distinct-path uncertainty). When in doubt, decompose.

**Methodology-interpolation rule scope (locked v5, expanded v6):** The rule applies to CC-introduced content. Pre-existing QB-drafted content from earlier cycles is grandfathered. The v6 cycle's retroactive sweep covers v1-v5 CC-introduced content; v1-v5 QB-drafted content is grandfathered. The boundary is computable, not judgment-dependent — provenance (CC-introduced vs QB-drafted) is the discriminator.

The v5 audit's M-1 finding (the v3-cycle "3 consecutive iterations" iteration cap) was an instance of CC-introduced content surviving the rule's introduction. v6 closes that instance: § 5.3 and § 3.1 cadence-neutralized to "repeatedly," with explicit deferral to Phase 5 working agreements per the established pattern.

**No fabricated content in v6.** Every concrete claim has a verification entry above with decomposed counts. Every operator-stated claim is explicitly annotated as such. The v5 audit-CC error (re: operator memory file's exacta claim) is surfaced and resolved by re-grounding against the memory file's verbatim text.
