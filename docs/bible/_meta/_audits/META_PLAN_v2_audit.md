markdown# META_PLAN.md DRAFT v2 — ADVERSARIAL AUDIT

**Audit-CC session:** fresh CC, 2026-05-03
**Auditing:** META_PLAN.md draft v2 at /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/META_PLAN.md
**Reference materials read:** DD bible at /home/strakajagr/projects/dynasty-dugout/ARCHITECTURE_BIBLE.md, EE_CURRENT_STATE_DUMP.md, live AWS state, EE codebase
**Threshold:** Tony's "<5 MATERIAL findings AND zero fabricated content findings" criterion applies

## Summary verdict

Revise + re-audit. v2 fixed every v1 BLOCKER it claimed to fix in form, but introduced new factual errors in the worked-example appendix that are at least as serious as v1's, prescribed a forward migration format that contradicts the existing migration runner, and left several load-bearing rules (commit gate, "non-production database," rollback format, Tier 2 handoff worked example) underspecified in ways that will block the very next Phase 0 deliverable (BIBLE_STRUCTURE_SPEC).

## v1 finding regression check

| v1 finding | v2 fix claim | Verified | Notes |
|---|---|---|---|
| Q1.1: EventBridge "5 disabled" | "3 disabled" per live AWS | ✓ FIXED | Live AWS confirms 13 rules, 3 DISABLED |
| Q1.2: "15 tables + 1 matview" | "14 tables + 1 matview" | ✓ FIXED | CREATE TABLE count = 14, matview = 1 |
| Q1.4: DD mischaracterization | § 1.4 rewritten | ✓ FIXED | v2 § 1.4 now correctly characterizes DD as multi-runtime with multiple canonical objects |
| Q4.1: Phase duration arithmetic | "6–8 weeks → 9–17 weeks" | ✗ STILL WRONG | Per-phase low: 2+4+1+1+1=9 ✓; per-phase high: 4+8+2+2+3=19, not 17. Off-by-2 at the high end. |
| Q2.5: Migration discipline deferral | § 7.12 added | ✓ ADDRESSED but contradicts existing runner (see Q1 below) | |
| Q1.8: Two INACTIVE Lambdas | "ingestion + feature-engineering per live AWS verification" | ✗ STILL WRONG | Live AWS shows three INACTIVE: ingestion, feature-engineering, results. v2 explicitly claims "per live AWS verification" — verification was not actually performed. |

4 of 6 representative v1 findings landed cleanly; 2 of 6 still have factual errors (one inherited, one introduced).

## Question 1: Unverifiable / wrong claims

1. **§ 2.3 — "all 8 Lambda functions (including currently-INACTIVE equine-ingestion and equine-feature-engineering per live AWS verification)."** Live AWS shows three INACTIVE Lambdas, not two. `equine-results` is also Inactive (verified via `aws lambda get-function --function-name equine-results --query 'Configuration.State'` → Inactive). The phrase "per live AWS verification" makes the error worse — v2 is asserting verification it didn't actually do. Either drop the parenthetical or run the actual verification.

2. **§ A.4 / § 9.11 — "model/features/feature_definitions.py … exports `ALL_FEATURES = []` (empty list) and is imported by model/training/train.py."** The `ALL_FEATURES = []` is just the initialization line; the next two lines (140–142) populate it via `for group in FEATURE_GROUPS.values(): ALL_FEATURES.extend(group['features'])`. Verified runtime: `len(ALL_FEATURES) == 73` and `FEATURE_COUNT == 73`. The module is NOT orphaned: actively imported by both `model/training/train.py:40` AND `backend/services/inference_service.py:28` (two production paths, not one). v2 inherits the dump's misreading and uses it as the worked example for the Deprecated Field Tracker pattern. The example claims to "use real EE patterns surfaced from EE_CURRENT_STATE_DUMP.md" (Appendix A intro) but is materially wrong about the surfacing.

3. **§ A.1 — `get_active_model_by_type_and_style('wp_full', style='gonzo_sauce')` CORRECT example.** This function does not exist in the codebase. Only `get_active_model_by_type(model_type: str)` exists at `model_version_repository.py:100`, and its docstring restricts model_type to `'wr' | 'pl' | 'ls'` (not `'wp_full'`). All callers (`pl_inference_service.py:96`, `ls_inference_service.py:139`, `wr_inference_service.py:269`) pass only model_type. v2 § A.1 presents a fabricated API as the canonical CORRECT example. The intent of the pattern (code should select on style too) is correct; the specific function name is fictional. Either rewrite using a real function signature, or rewrite as "the corrected API would be `get_active_model_by_type_and_style(...)`, which does not yet exist — see Phase 5.X.Y."

4. **§ 7.12 migration format prescription — "NNN_YYYYMMDD_short_description.sql. Monotonic, unique, sequential."** All 12 existing migrations are `NNN_short_description.sql` (no date in name). Verified by `find … -name "*.sql"`. v2 prescribes a forward format that 100% of existing migrations violate, without a transition rule. Furthermore, the migration runner at `backend/database/migrations/migrate.py:48-58` tracks applied migrations by FILENAME in the `schema_migrations` table — renaming an existing file would make the runner think it had not been applied. v2's § 7.12 mentions only the duplicate-005 problem and is silent on:
   - The naming-convention transition (do all 12 existing migrations get renamed pre-Phase-1? Or does the rule apply only to new migrations, with existing ones grandfathered?)
   - The `schema_migrations` filename-tracking mechanism that would break under rename

5. **§ 3.7 — "Phases 0–4 sum: 9–17 weeks."** Arithmetic still wrong on the high end. Per-phase highs: Phase 0 (4 wk) + Phase 1 (8) + Phase 2 (2) + Phase 3 (2) + Phase 4 (3) = 19 weeks, not 17. v1 audit caught the 6–8 vs 7–11 mismatch; v2 fixed the framing but not the arithmetic.

6. **§ A.5 — "backend/services/data_sources/hrn_scraper.py:802."** Line 802 is verified as the `win_payout: parse_payout(1)` line in the result dict. The reference is approximately correct (the parse_payout calls span lines 802–804) ✓ — verifiable.

7. **§ 9.13 — "45 simultaneously active rows across (model_type, style, specialist) combinations."** Only verifiable via dashboard query (per dump § 3.1). Cannot verify directly because `equine-ingestion` Lambda is INACTIVE so `raw_query` is unavailable. Defensibly inherited but worth a "(per dashboard, not direct DB read)" caveat.

## Question 2: Scope gaps

1. **§ 7.10 commit-before-deploy — no exception clause for emergency hotfix.** Audit prompt explicitly asked: "What happens when commit-before-deploy fails mid-Phase-5 (e.g., an emergency hotfix is deployed without commit due to time pressure)?" v2 § 7.10 has no exception. § 8.1's "actively losing money" exception is scoped to Phases 0–4. Phase 5 has zero defined exception protocol.

2. **§ 7.10 git-status-clean rule has practical conflict with deploy artifacts.** `.cf-distribution-id` and `.frontend-bucket` are not in `.gitignore` (verified). Both files exist on disk (verified). They are written by `scripts/deploy-backend.sh:243` and `:262`. After every deploy, `git status` would show modifications, blocking the next "git status clean" gate per § 7.10.

3. **§ 7.12 migration discipline — "non-production database first" is undefined.** EE has Aurora Serverless production cluster (the only one referenced in code), no documented staging environment, no CDK construct creating one, and the dump notes `equine-ingestion` is INACTIVE (the path that exposes `raw_query`). What does Tony actually run migrations against?

4. **§ 7.12 rollback format underspecified.** v2 says "explicit SQL OR explicit 'non-reversible because X' with fallback recovery procedure." But where does the rollback live? In the migration file (paired down/up SQL)? In a sibling `down_NNN.sql` file? In the bible entry only? In `PHASE_5_BACKLOG.md`? Phase 1 cannot draft the Database Bible's migration discipline section without this.

5. **§ 6.5 Tier 2 "skeleton with template slots marked" — no worked example.** The next Phase 0 deliverable (BIBLE_STRUCTURE_SPEC.md) is Tier 2 — meaning QB is about to draft a framework with template slots and there is zero concrete reference for what `<TEMPLATE: ...>` syntax looks like in practice.

6. **§ 8.1 observation-only exception has no protocol for Bug #28-like findings discovered DURING Phase 0.** v2 § 8.1 says Bug #28 "goes to the triage queue and waits for Phase 5." But § 8.2 says "Every finding from Phase 1+ audits goes to PHASE_5_BACKLOG.md" — note "Phase 1+." Bug #28 was surfaced during Phase 0 dump generation. § 4.3 says PHASE_5_BACKLOG.md is "Created when first triage queue entry is generated (Phase 1)." Per v2's own structure, Bug #28 has no destination right now.

7. **§ 7.13 enforcement mechanics — no "what to do when enforcement fails" protocol.** § 7.13 names "Tony reviews the bible diff" as the immediate-term enforcement. What if Tony commits without bible update? Drift cascades silently.

8. **§ 5.3 convergence test does not specify what happens if it fails on second iteration.** § 5.4 says "If § 5.3 surfaces gaps, the affected Phase 0 documents revise and re-lock. The test re-runs. Repeat until clean." No iteration cap. No "if it doesn't converge after N attempts, escalate to Tony for protocol revision."

## Question 3: Ambiguous language

1. **§ 7.13 — "Tony reviews the bible diff before each commit."** Two readings:
   - Reader A: Tony reviews bible diff for every commit (including non-bible commits), with the diff being empty for non-bible commits — reduces to "every commit goes through Tony review."
   - Reader B: Tony reviews bible diff only for commits that touch the bible (per § 7.11's prefix-or-no-prefix split) — doesn't apply to bible-untouching commits.

2. **§ 7.10 — "Commits represent stable iteration states worth deploying."** "Stable" is undefined.

3. **§ 7.12 — "non-production database first."** Discussed in Q2.3.

4. **§ 5.3 material difference — example uses DD pattern, not EE.** Borderline cases involving EE cross-layer naming would help.

5. **§ 8.1 Bug #28 case study — "stable known failure mode."** Bug #28 was unknown until 2026-05-03 (per § 1.2). It was discovered three days into a silent ongoing data corruption. v2 immediately classifies it as "stable known" once known. This is post-hoc reasoning.

6. **§ 6.5 Tier 2 — "QB hands the skeleton to CC with a spec for what each template slot must contain."** What if CC's fill reveals that the framework is wrong?

7. **§ 4.5 source authority hierarchy — six tiers but § 8.5 only resolves three pairs.** Missing: AWS-vs-database conflict resolution.

8. **§ 6.4 — "for Tier 3 large outputs, without reading critical sections fully and skim-reading the rest with audit-CC catching what skim missed."** "Critical sections" undefined.

## Question 4: Contradictions

### Internal

1. **§ 4.5 vs § 8.5 — database tier disagreement on AWS-vs-DB.** § 4.5 ranks AWS above database; § 8.5 doesn't restate that for the AWS-vs-database conflict.

2. **§ 7.10 commit-before-deploy vs § 8.1 observation-only exception.** If § 8.1 exception fires during Phase 1 audit and resulting fix is deployed, does § 7.10 require commit-before-deploy for the fix?

3. **§ 7.4 "Every bible document includes 'What Was Fixed'" vs § 3.2 hypothetical Architecture Overview.** Architecture Overview spans the whole system. Its What-Was-Fixed would aggregate cross-cutting bugs from every other document, or duplicate them. v2 doesn't specify scoping rule.

4. **§ 12 changelog claim "§ 1.1: Two INACTIVE Lambdas acknowledged (was one in v1)" vs live AWS.** v2 fixed v1's count from one to two; live shows three. Changelog claim is true (count went from 1 → 2) but incomplete (still missing one).

### External

5. **§ 7.12 "monotonic, unique, sequential" vs current EE migrations.** All 12 existing files violate at least one criterion: 005 is duplicated, and the proposed `NNN_YYYYMMDD_*` format is novel.

6. **§ 1.4 DD characterization vs DD bible reality.** ✓ Fixed cleanly.

7. **§ 7.4 "divergence from DD's pattern" vs DD § 18.** ✓ Fixed cleanly. (But see internal contradiction #3.)

8. **§ 6.6 "no GM session" vs residual references.** ✓ Cleanly retired.

## Question 5: Rushed sections

1. **§ 3.3 Phase 2.** Better than v1, still missing iteration discipline, continuity-risk handling, blind-vs-shared audit-CC access.

2. **§ 3.4 Phase 3.** Quality bar undefined, document structure unclear, conflict resolution rule with Phase 1 missing.

3. **§ 7.13 enforcement mechanics.** Names categories but doesn't operationalize. PR template "(when PR workflow is adopted)" is deferred-indefinitely.

4. **§ 9.11–9.13 EE-specific anti-patterns.** § 9.13's CORRECT example references non-existent function (Q1.3). The fictional API weakens all three by association.

5. **§ 10 Open Questions.** § 10.5 Bug #28 destination is not legitimately deferred — needs decision today.

6. **§ 6.4 Tier 3 skim-reading discipline.** One sentence, load-bearing for Phase 1.

## Question 6: Missing examples

1. **§ 6.5 Tier 2 — no concrete "skeleton with template slots" example.** Critical gap because BIBLE_STRUCTURE_SPEC is next.

2. **§ 7.10 — no concrete commit-with-bible-update workflow example.**

3. **§ 7.11 — examples don't cover all variants.** Missing "untouching" case explicit treatment.

4. **§ 7.12 migration discipline — no concrete example migration with rollback.**

5. **§ 9.13 anti-pattern CORRECT example.** Replace fictional function.

6. **§ A.4 — broken Deprecated Field Tracker example.** Wrong file plus broken markdown table rendering.

## Additional adversarial findings

A. **v1 finding regression.** Two of six representative v1 findings still have factual errors. v2 cites "per live AWS verification" without verifying.

B. **Three-tier model coherence.** Tier assignments internally consistent. Tier 2 handoff has hidden coupling problem (CC's fill reveals framework wrong → no protocol).

C. **Commit-before-deploy practical verification.** Pre-Phase-1 baseline achievable. Deploy artifact gitignore gap. PR workflow deferred-indefinitely.

D. **§ 7.9 Data Acquisition Honesty Protocol integration.** § 7 placement defensible. § 7.9 says "paid" while § 3.5 says "paid-replacement" — vocabulary mismatch.

E. **A.6 audit-CC skeleton vs. actual practice.** A.6 lacks: live-verification mandate, severity threshold context, v1→v2 changelog regression check, threshold-gaming caution. The actual working prompt I'm executing has all four.

F. Other findings:
- Line 1 "markdown# META_PLAN.md" — copy-paste artifact prepending "markdown" to H1
- § A.4 broken markdown table rendering
- Worked example placeholders ("Phase 5.X.Y", "locked 2026-05-XX") — defensible but appendix intro overclaims "real EE patterns"

## Severity assessment

**BLOCKERs (5):**
- Q1.1: Three INACTIVE Lambdas, not two; "per live AWS verification" is false
- Q1.2: A.4 deprecated-field example wrong (file not orphaned, ALL_FEATURES = 73)
- Q1.3: A.1 / § 9.13 CORRECT example uses non-existent function
- Q1.4: § 7.12 migration format prescription contradicts existing runner
- Q1.5: § 3.7 phase total still wrong (high end 17 vs 19)

**MATERIALs (11):**
- Q2.1: § 7.10 no emergency hotfix exception
- Q2.2: § 7.10 / deploy-artifact gitignore gap
- Q2.3: § 7.12 "non-production database" undefined
- Q2.4: § 7.12 rollback format underspecified
- Q2.5: § 6.5 Tier 2 no skeleton-with-template-slots example
- Q2.6: Bug #28 has no Phase 0 destination
- Q3.1: § 7.13 "each commit" ambiguity
- Q3.6: § 6.5 Tier 2 framework-rejection protocol
- Q3.7 / Q4.1: § 4.5 vs § 8.5 — AWS-vs-DB tier conflict resolution missing
- Q4.3: § 7.4 What-Was-Fixed cross-cutting scope
- Q5.3 + E: § 7.13 enforcement abstract + A.6 lacks practice gaps

**MINORs (12):** various; not enumerated here for brevity but listed in original audit.

**STYLEs (5):** including line 1 "markdown" artifact, broken markdown table, vocabulary mismatch (paid vs paid-replacement), placeholder caveats.

## Material findings count

Per Tony's "use judgment, don't game the threshold" instruction, MATERIAL count is 11 (or 12 if § 7.13 + A.6 are split). BLOCKER count is 5.

Three BLOCKERs (Q1.1, Q1.2, Q1.3) are fabricated/unverified content findings. Per Tony's hard rule ("zero fabricated content findings"), v2 fails this criterion regardless of MATERIAL count.

## Recommendation

Revise + re-audit. Do not lock.

The MATERIAL count (11–12) is well above Tony's threshold of < 5. The BLOCKERs (5) include three new factual errors introduced in v2's worked-example appendix — exactly the artifact added to address v1's "missing examples" finding. Adding examples without verifying them propagated the dump's errors into ostensibly-canonical bible-pattern templates, which is worse than not having the examples at all.

Specific revision priorities:

1. Run live-state verification on every fact in Appendix A before re-audit.
2. Fix the five BLOCKERs.
3. Address the 11 MATERIALs systematically. The cluster around § 7.10 + § 7.12 + § 7.13 + § 6.5 is the most consequential.
4. Update A.6 audit-CC skeleton to include live-verification mandate, severity threshold context, v1→v2 changelog regression check pattern, and threshold-gaming caution.

The document's structure and direction are sound. The substance has not yet survived adversarial verification. Re-audit after revision.
That's the v2 audit. Save to /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/_audits/META_PLAN_v2_audit.md.

Artifact 2: v3 drafting spec for CC. Paste-ready into a fresh CC session once the audit file is on disk.
You are drafting META_PLAN.md v3 for the Equine Equalizer (EE) project. v2 failed adversarial audit and must be revised. You are taking over drafting from QB because v2's failure mode was fabricated factual content in a Tier 1 document — a class of failure QB cannot prevent without filesystem access. v3 is therefore drafted by you (CC) under verification discipline.

This is a Tier 3 drafting task per the document's own three-tier model (which v3 also revises — see methodology question below).

## Read these documents first, in this order:

1. The current v2 draft on disk: /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/META_PLAN.md
2. The v2 audit response: /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/_audits/META_PLAN_v2_audit.md
3. The DD bible (structural anchor): /home/strakajagr/projects/dynasty-dugout/ARCHITECTURE_BIBLE.md
4. The EE current state dump: /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/EE_CURRENT_STATE_DUMP.md

The v2 audit is the most important input. Every BLOCKER and MATERIAL it identifies must be addressed in v3 or explicitly justified for non-action.

## Tony's four locked answers (integrate as required content):

**Q1 — Migration format: option (b) grandfathering.**
- Migrations 001-011 keep legacy `NNN_short_description.sql` format
- Migrations 012+ use `NNN_YYYYMMDD_short_description.sql` format
- Bible entry for migration 012 documents the cutover and rationale
- Migration runner unaffected (tracks by filename, both formats valid)
- Phase 1 audit notes legacy-format migrations as findings, not blockers
- No Phase 0 prerequisite to rename existing migrations
- If unified format desired in future, that's optional Phase 5+ cleanup, not Phase 0 work

**Q2 — schema_migrations tracking: no action required under (b).**
- Runner keeps tracking 001-011 by current filenames
- 012+ tracked by new filenames same way
- No migration runner changes needed

**Q3 — Emergency hotfix protocol for § 7.10: carve-out with tight friction.**
Specific language Tony wrote:
> Emergency hotfix exception: in cases where production is broken and waiting for commit + bible review would cause user-facing harm or data loss, deploy may proceed before commit, subject to:
> - Deploy flagged as emergency in deploy command (e.g., `EMERGENCY=true ./deploy.sh`); audit trail records the exception
> - Commit within 4 hours of deploy
> - Bible entry within 24 hours of deploy
> - Triage queue entry created at deploy time recording: what broke, what was deployed, why bible-first discipline was bypassed, what the retroactive update plan is
> - Two emergency deploys within 7 days triggers architectural review of why this keeps happening

Tony's rationale: "Default-deny is fantasy. Discipline isn't preventing emergency deploys; it's making sure they don't accumulate as silent debt. The exception is a forensic record, not a quiet bypass."

**Q4 — Deploy artifacts: gitignore as Phase 0 prerequisite.**
- Add `.cf-distribution-id` and `.frontend-bucket` to `.gitignore`
- Audit deploy scripts for other untracked artifacts during Phase 0; add all to `.gitignore` in one sweep
- Document in v3 § 7 that the `.gitignore` was established at Phase 0 baseline along with rationale
- Deploy artifacts have no business in commits — they're cached infrastructure identifiers, not source state

## Methodology question for v3 to resolve

The three-tier drafting authority model (v2 § 6.5) breaks down when "methodology document" and "contains verifiable EE-specific claims" overlap. v2 proved this overlap is unstable — fabrications crept into Appendix A because the document had Tier 1 framing but Tier 3 content demands.

GM's proposed resolution (you may refine the wording but the principle is locked):

> Any document containing verifiable EE-specific claims (file paths, function signatures, AWS resources, DB state, code patterns) is Tier 3, regardless of methodology framing density. Tier 1 reserved for pure procedural documents with no EE-specific factual claims. Mixed-content documents do not exist — if a document needs both methodology framing AND EE-specific examples, it's Tier 3, and the methodology framing is drafted under same verification discipline as the examples (no fabrication, citations where claims appear).

Practical consequences v3 should articulate:
- META_PLAN itself is now Tier 3 (it has Appendix A with EE-specific examples)
- BIBLE_STRUCTURE_SPEC is Tier 3 (section templates reference real bible content patterns)
- AUDIT_METHODOLOGY is Tier 3 (worked examples need real EE patterns)
- TRIAGE_QUEUE_SPEC is Tier 3 (example entries need real bugs)
- CONVERGENCE_CRITERIA may stay Tier 1 if it can be written as pure procedure

v3 must:
- Revise § 6.5 to reflect this two-tier-effective-three-tier-on-paper model
- Update § 4.1's tier assignments accordingly
- Reflect this in workflow discipline: any document with EE-specific claims is CC-drafted under verification discipline, regardless of methodology framing

## Verification discipline (HARD RULE for v3)

**No fabrication. No unverified claims. Verify before claiming.**

Specifically:
1. Every factual claim about EE in v3 — file paths, function signatures, line numbers, AWS resource state, EventBridge rule states, Lambda memory/timeout configs, table counts, migration filenames, code patterns, behavior assertions — must be verified against the source before being written into v3.
2. Verification means: read the file, run the AWS CLI command, query the database (where possible), or trace the code path. Inheriting a claim from EE_CURRENT_STATE_DUMP.md without independent verification does NOT satisfy this rule. The dump was wrong about multiple facts in v1 and v2.
3. If verification cannot be performed (e.g., DB query path unavailable because Lambda is INACTIVE), state explicitly: "Cannot verify directly because [reason]; inherited from [source] which itself reports [value]." Do not present unverified claims as verified.
4. If a claim cannot be verified at all, drop it from the document. Better to have fewer concrete claims than to have fictional ones.

## Verification log (REQUIRED DELIVERABLE)

Alongside v3 META_PLAN, produce a verification log at:

`/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/_audits/META_PLAN_v3_verification.md`

Format per claim:
Claim N: [brief description of claim]
Document location: [v3 § X.Y]
What was checked: [file path + line numbers, AWS CLI command, SQL query, etc.]
What was found: [actual value or output]
Claim survived verification: [Yes/No/Partial - explain]
Action taken: [included as-is / modified / dropped]

Specific verification list (you may extend; do not omit):
1. Lambda counts — total functions, INACTIVE function names and count (verify all 8, not just the two v2 named)
2. EventBridge rule count and disabled count (verify against v2's "13 rules, 3 disabled")
3. Database table count (verify CREATE TABLE statements across schema.sql + all migrations 001-011)
4. Migration filename format (verify all 12 existing migrations actually use NNN_short_description.sql format, including the duplicate-005 case)
5. Migration runner mechanism (verify backend/database/migrations/migrate.py tracks by filename in schema_migrations table)
6. Model registry counts (88 entries, 45 active) — verify via dashboard endpoint or note as unverifiable due to Lambda INACTIVE
7. API Gateway route count (verify 41 routes against `aws apigatewayv2 get-routes`)
8. Function signature for any code referenced in Appendix A worked examples — every function name, every parameter, every behavior claim
9. File existence and content for any file referenced in Appendix A — including model/features/feature_definitions.py vs model/shared/feature_definitions.py distinction (which v2 misread)
10. .gitignore contents (verify .cf-distribution-id and .frontend-bucket are NOT currently in .gitignore)
11. Deploy script artifact writes (verify scripts/deploy-backend.sh:243 and :262 write the deploy artifacts as v2 audit claims)
12. DD bible structural facts (line count, section names) cited in v3's Motivation
13. Bug #28 line reference (backend/services/data_sources/hrn_scraper.py:802)
14. ALL Appendix A worked example claims — every function name, every file path, every line number, every behavior assertion. This is the most important verification because v2's worst failures were here.

## What v3 must contain (substance)

Address every BLOCKER and MATERIAL from the v2 audit. Specifically:

### Five BLOCKERs to fix:
1. Lambda INACTIVE count: verify and state correctly. v2 said 2; audit said 3 (ingestion, feature-engineering, results). Verify yourself; do not inherit either claim.
2. Appendix A.4 deprecated field tracker: replace example entirely. The file v2 cited (`model/features/feature_definitions.py`) is NOT orphaned per audit verification. Use a different deprecated pattern — audit suggested the legacy `predictions` table that migration 005 split but didn't drop. Verify any replacement candidate before using it.
3. Appendix A.1 / § 9.13 fictional function: the function `get_active_model_by_type_and_style` does not exist. Either (a) rewrite using the real signature `get_active_model_by_type(model_type)` and the FORBIDDEN/CORRECT pair shows passing style as an additional parameter (specifying that the style-aware version is Phase 5.X.Y work that doesn't yet exist), OR (b) replace this anti-pattern entirely with a different real EE pattern from the dump.
4. Migration discipline: integrate Tony's Q1+Q2 answers (grandfather existing, new format from 012+, no rename, no runner changes). Address the schema_migrations tracking compatibility explicitly.
5. Phase duration arithmetic: per-phase highs sum to 19, not 17. Compute correctly.

### Eleven MATERIALs to address:
1. § 7.10 emergency hotfix exception (integrate Tony's Q3 carve-out language)
2. § 7.10 deploy-artifact gitignore (integrate Tony's Q4; document in § 7 that .gitignore was established at Phase 0 baseline)
3. § 7.12 "non-production database" definition (specify what Tony actually runs migrations against; if no staging exists, say so and acknowledge the rule has reduced enforcement until staging exists)
4. § 7.12 rollback format (specify: paired down/up SQL in same migration file, OR sibling down_NNN_*.sql, OR rationale block in bible entry — pick one and justify)
5. § 6.5 Tier 2 skeleton-with-template-slots concrete example (add to Appendix A — show 15-20 line stub with QB framework prose + template slot delimiter + sample CC fill)
6. Bug #28 destination during Phase 0 (decide: create empty PHASE_5_BACKLOG.md now with Bug #28 as first entry, OR create a Phase-0-specific findings document, OR note in bible itself; resolve § 10.5)
7. § 7.13 "each commit" ambiguity (sharpen: bible-touching commits only per § 7.11)
8. § 6.5 Tier 2 framework-rejection protocol (CC returns skeleton with `<FRAMEWORK_GAP: ...>` markers when fill reveals framework wrong; QB triages)
9. § 4.5 vs § 8.5 AWS-vs-DB conflict resolution (resolve which wins when AWS shows Lambda INACTIVE but DB has rows that imply it ran — likely AWS for "current state" and DB for "historical record"; specify)
10. § 7.4 cross-cutting What-Was-Fixed scope (specify: each bug lives in document whose discipline it most directly affects; cross-references from related documents; no duplication)
11. § 7.13 enforcement mechanics + A.6 audit-CC skeleton (operationalize enforcement; update A.6 to match working prompt patterns including live-verification mandate, threshold context, regression check, threshold-gaming caution)

### Twelve MINORs and Five STYLEs:
Address per audit. Drop fictional content; sharpen ambiguous language; fix the line-1 "markdown" artifact; fix the broken markdown table in A.4; align "paid" vs "paid-replacement" vocabulary between § 7.9 and § 3.5.

## What v3 must contain (structural)

Same overall structure as v2 with these specific changes:

1. Section 6.5 (drafting authority): revised per methodology question above
2. Section 7.10: emergency hotfix exception added
3. Section 7.12: migration discipline rewritten per Tony's Q1+Q2; rollback format specified
4. Section 7.13: enforcement mechanics operationalized; ambiguity resolved
5. Section 7.X (new): document .gitignore baseline as Phase 0 prerequisite
6. Section 4.1: tier assignments updated per methodology revision
7. Section 4.5 + 8.5: AWS-vs-DB conflict resolution added
8. Section 10.5: Bug #28 destination resolved
9. Appendix A: every example verified against actual code/AWS/DB; fabricated examples replaced; new Tier 2 worked example added
10. Section 12: changelog updated honestly — including the methodology revision and v3's correction of v2's factual errors

## Workflow conventions to document in v3

Audit subdirectory pattern:
- All audit responses live at `/docs/bible/_meta/_audits/`
- Naming convention: `<doc>_v<N>_audit.md` for adversarial audits, `<doc>_v<N>_verification.md` for verification logs
- Pattern applies to all Phase 0 and Phase 1 documents
- Document this in v3's workflow section so the convention is canonical

## Output requirements

1. **v3 META_PLAN.md** at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/META_PLAN.md` (overwrite v2)
2. **Verification log** at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/_audits/META_PLAN_v3_verification.md`

Both must be on disk before declaring task complete. The verification log is not optional and is not a summary — it is per-claim documentation that audit-CC will use to validate your verification work.

## Discipline reminders

- No fabrication. If you can't verify, drop the claim or mark it explicitly as unverifiable.
- The dump is not source of truth. Verify against live state.
- The DD bible is structural anchor only. Do not inherit DD's specific facts about DD into EE's bible.
- Tony's threshold: v3 audit must return < 5 MATERIAL findings AND zero fabricated-content findings to lock. The fabricated-content bar is hard.
- Better four examples in Appendix A than five with one fabricated. Better three than four with one fabricated.
- This document is the foundation for every subsequent Phase 0 document. Errors here compound.

## Output format

Produce the v3 META_PLAN as a complete markdown document. Do not produce diffs against v2 — produce the full revised document. Estimated length 7,000-9,000 words including expanded Appendix A and new sections.

When you finish drafting v3 and the verification log, return a single summary message:
- Confirmation that both files are on disk
- Total word count of v3
- Number of claims in verification log
- Number of claims that survived verification
- Number of claims dropped due to verification failure
- Any notes about claims you could not verify and how you handled them
- Any architectural questions surfaced during verification that need QB attention before audit

Do not begin drafting v3 until you have read v2, the v2 audit, the DD bible, and the EE current state dump. Verification is the bottleneck of this work, not drafting.

Begin.