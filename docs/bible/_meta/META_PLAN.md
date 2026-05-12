# META_PLAN.md

**Document:** META_PLAN
**Phase:** 0 (Methodology)
**Status:** LOCKED v9 (2026-05-05)
**Author:** CC (drafting under verification discipline; QB orchestrated and reviewed)
**Date:** 2026-05-05
**Locked:** 2026-05-05

**Revision history:**
- v1 (2026-05-03): initial QB draft
- v2 (2026-05-03): post-v1-audit revision integrating audit findings + Tony's three architectural answers
- v3 (2026-05-03): post-v2-audit revision. v2 introduced fabricated factual content in its worked-example appendix. v3 was CC-drafted under hard verification discipline; companion verification log at `_audits/META_PLAN_v3_verification.md`.
- v4 (2026-05-04): post-v3-audit revision. v3 audit returned 1 BLOCKER (A.4 "4 references including the import" → "4 instantiations" inflation) and 6 MATERIALs (methodology coherence). v4 is a localized fix pass plus the verification-log-precision lesson the BLOCKER taught.
- v5 (2026-05-04): post-v4-audit revision. v4 audit returned 0 BLOCKERs and 4 MATERIALs (precision-rule scope, Tier-migration mechanics, Layer 1 physical form, Bug #28 stable-known). v5 is a localized patch pass plus one substantive addition (§ 3.2.1 — the Phase 1 ML re-architecture forcing function locked at META_PLAN level). v4's audit also surfaced a methodology-interpolation pattern (Finding H); v5 corrects v4's instance and operates under the rule going forward.
- v6 (2026-05-04): post-v5-audit revision. v5 audit returned 0 BLOCKERs, 0 fabricated-content findings, and 3 MATERIALs — but one MATERIAL was a methodology-interpolation finding (M-1: § 5.3 / § 3.1 "3 consecutive iterations" iteration cap, CC-introduced in v3 cycle without Tony's explicit ratification). Per Tony's bar, methodology-interpolation findings fail the lock regardless of count. v6 is a surgical patch pass: M-1 cadence-neutralized; M-2 methodology-interpolation rule scope expanded with named patterns + catch-all clause; M-3 § 3.2.1 "merge" language tightened to require physically separate documents; § 6.1 grandfathering clause added making the "explicitly ratified" boundary computable; expanded MINORs #5 (exacta payout claim) and #6 (ECS task families enumeration). Companion verification log at `_audits/META_PLAN_v6_verification.md`.
- v7 (2026-05-05): post-convergence-test revision addressing G8 from `_audits/convergence_test_audit.md`. The operating-model convergence test on Database & Schema Bible (run1 vs run2) returned 21 material differences + 9 methodology gaps. G8 was the single methodology gap routed to META_PLAN: the Appendix A `YYYY-MM-XX` placeholder convention is interpreted differently between conservative-uses-placeholder and commit-to-actual-date drafters when knowable real dates exist from git log. Per Tony's locked direction (Path A revision), v7 is a surgical patch: § 7.3 sub-rule added requiring `git log` resolution for real fixes with knowable dates; Appendix A lead paragraph scope-clarified to explicitly bound the placeholder convention to worked examples + forward-looking entries; § 12 multi-cycle changelog with v6→v7 entry. All other sections retained from v6 verbatim. Companion verification log at `_audits/META_PLAN_v7_verification.md`. The remaining 8 methodology gaps (G1–G7, G9) are routed to BIBLE_STRUCTURE_SPEC v4, which follows v7 lock per Path A sequencing.
- v8 (2026-05-05): post-v7-audit revision per `_audits/META_PLAN_v7_audit.md`. v7 audit returned 0 BLOCKER, 1 MATERIAL (F-F methodology-interpolation finding: § 12.1 second methodology-lesson paragraph asserted a methodology-pattern generalization beyond drafting-spec authorization), 0 fabricated, 6 MINOR/STYLE. Per Tony's bar (methodology-interpolation findings fail the lock regardless of count), v7 could not lock. Per Tony's locked Option 2 directive, v8 closes 1 MATERIAL + 3 MINOR/STYLE = 4 findings. F-F: paragraph deleted (no relabel; resolution chosen over relabel to eliminate ambiguity). A2: § 12 intro paragraph replaced with explicit-descriptive framing of v8's actual organization. A3: "surgical-patch discipline" terminology promotion struck; replaced with plain-language descriptive bullet. Q3.A2: normative "future Phase 0 cycles should treat" softened to descriptive past-tense referencing v6 § 5.4. Three remaining MINOR/STYLE findings (R3 G8 placeholder normalization, X7 BIBLE_STRUCTURE_SPEC v4 forward reference, X8 v4 MINOR-pass close paraphrase) flagged STYLE/acceptable in v7 audit; no remediation required. v8 introduces zero new methodology constructs (pure deletion + spec-prescribed replacements). All other sections retained from v7 verbatim. Companion verification log at `_audits/META_PLAN_v8_verification.md`. BIBLE_STRUCTURE_SPEC v4 follows v8 lock per Path A sequencing.
- v9 (2026-05-05): post-Phase-0-closure surgical correction triggered by Phase 1 Architecture Overview v1 verification. Architecture Overview v1 verification log Claim A.8 REFUTED the inherited Aurora cluster ARN claim — live AWS verification returned `DBClusterNotFoundFault` for the cited cluster identifier. Substrate reality (Architecture Overview v1 verification log Claim V1-11): EE uses standalone RDS PostgreSQL 16.6 instance `equine-db` (db.t4g.micro, endpoint `equine-db.cgtuh834bttd.us-east-1.rds.amazonaws.com:5432`, `DBClusterIdentifier=None`) — not an Aurora cluster. Source of inherited error traced to cross-project contamination from `fantasy-baseball-serverless` Aurora cluster ARN bleed into EE_CURRENT_STATE_DUMP.md (Tier 6). Per META_PLAN v8 § 4.5 source-priority, Tier 1 (live AWS state) governs over Tier 6. v9 corrects three Aurora references in body (§ 2.3 in-scope artifact bullet, § 7.12 Migration testing paragraph, § 9.2 anti-pattern illustrative example) and updates metadata hygiene (front matter Status + Locked fields, § 11 Lock Status block — all carrying drift from prior cycles where Phase 0 closure metadata never propagated to disk). All other sections retained from v8 verbatim. v9 introduces zero new methodology constructs (pure correction + metadata hygiene). Companion verification log at `_audits/META_PLAN_v9_verification.md`. Methodology lesson banked for AUDIT_METHODOLOGY future cycle: Tier 6 verification mandate includes cross-project contamination check, not just freshness check.

---

## 1. Motivation

### 1.1 Why this document exists

Equine Equalizer (EE) has accumulated drift between what its operator believes the system does, what the code does, and what the deployed system does. The proximate trigger for confronting that drift was Derby Day (May 2, 2026). The root cause is older and more structural: there is no canonical reference for what EE is, so every fix is local, so drift is inevitable, and the operator deploys without committing — meaning git history cannot serve as a forcing function for honesty. (Verified: last git commit on EE main branch is `2a3d758` on 2026-03-15; working tree currently has 103 entries per `git status --porcelain | wc -l`, decomposed as 74 untracked + 29 modified per `git status --porcelain | awk '{print $1}' | sort | uniq -c`.)

This document — META_PLAN.md — is the first artifact of a Phase 0 methodology effort whose purpose is to construct an Architecture Bible for EE modeled on the Dynasty Dugout (DD) bible at `/home/strakajagr/projects/dynasty-dugout/ARCHITECTURE_BIBLE.md`. The DD bible is a 2,578-line single-file canonical reference (verified: `wc -l`). EE differs from DD in operationally meaningful ways that will require the bible to span multiple files (rationale in § 3.2, with the Phase 1 ML re-architecture forcing function specified in § 3.2.1). Phase 0 produces the methodology that governs how the EE bible gets built; it does not itself build the bible.

### 1.2 What surfaced the need

Derby Day made multiple architectural concerns simultaneously visible. Each is a specific manifestation of the same root cause:

- **Bug #28 (HRN scraper, 2026-04-30 onward):** off-by-one column shift in payout extraction at `backend/services/data_sources/hrn_scraper.py:802-804` (verified: lines contain `parse_payout(1)`, `parse_payout(2)`, `parse_payout(3)` for win/place/show payouts). Result: `win_payout` and `daily_double_payout` NULL across all results since the page-structure change. Documented in operator memory file `equine-equalizer-bug-28-hrn-scraper.md` (verified: discovered 2026-05-03; sharp regression — last clean day 2026-04-29 at 9/10 win-payout success; 2026-04-30 / 2026-05-01 / 2026-05-02 all 0/N — i.e., the silent-failure window between regression and discovery is at least three days). **No in-code marker exists yet** — `grep "Bug #28"` over `hrn_scraper.py` returns zero hits.
- **Bug #7 (a/b/c) compound failures** in the HRN scraper for entries data.
- **Gonzo Sauce style (Phase A3) producing predictions near-identical to general style** for all 12 Churchill Downs races on 2026-05-02. The user-facing differentiation does not manifest at rank=1.
- **LS strict-AND alert formula (Bug #25)** failing to produce any alerts for thin-PP-history Derby fields.
- **Calibration bypass at inference.** Per `wr_inference_service.py` (verified): the bypass is implemented as a comment block at lines 616–625 followed by the bypass operation `handicapping_probs = ranker_probs.copy()` at line 626 — i.e., bypass-related code spans lines 616–626, not 616–628 as v4 cited (the next two lines 627–628 are blank + the start of an unrelated 0-PP override comment block). The line-617 prose reads "All styles (including gonzo_sauce) bypass calibration at inference tonight"; the bypass affects ALL styles. The bypass was introduced as a workaround for the chain Bug #15 (train/inference FE drift) → Bug #24 (isotonic clip on legitimate-PP horses produced wrong rank-1 picks). The bypass is documented in code comments only, not in any architectural document.
- **Bug #15 train-vs-inference feature engineering drift** — three calibration bugs in one week traced to silent code-path drift between `model/shared/data_loader.py` (training) and `backend/services/feature_engineering_service.py` (inference). The "three distinct bugs this week" attribution is verified against the docstring at `model/shared/gonzo_features.py:7-11` (the file's own institutional-memory comment). Only the 14 Gonzo Sauce features have been factored to a single shared module (`model/shared/gonzo_features.py`); the remaining base features still live in two implementations kept in sync by manual cross-reference review.

The pattern is consistent: silent failures in critical paths, workarounds documented only in code comments, train/inference drift as a recurring failure mode, no canonical reference for what the system is supposed to be doing.

### 1.3 The deeper structural problem

The bugs above are symptoms. The structural problem is threefold:

1. **No canonical reference exists.** When a calibration decision is made, the rationale lives in a code comment that the next session may not read. When a train/inference duplication is discovered, the discipline that prevented its recurrence (gonzo_features.py extraction) lives only in that file's docstring and operator memory.

2. **The operator deploys without committing.** Verified: 103 entries in the EE working tree (74 untracked + 29 modified per `git status --porcelain | awk '{print $1}' | sort | uniq -c`) at audit time; last commit dated 2026-03-15. The bible's discipline of "every code change updates the bible" cannot function without commits, because there is no atomic unit to which the bible update can be tied.

3. **The system has grown faster than its documentation.** Verified inventory: EE has 8 Lambda functions (5 Active + 3 INACTIVE — see § 2.3 for the names), 14 database tables plus 1 materialized view, 88 model registry entries (88 = 45 active + 43 inactive per live dashboard query — the 88-row, 45-active multi-row reality is the topic of § 9.13), three independent inference pipelines (WR/PL/LS), two parallel feature engineering implementations (`model/shared/data_loader.py` for training and `backend/services/feature_engineering_service.py` for inference, reconciled only for the 14 Gonzo Sauce features per § 9.11), and a polyglot data acquisition layer. No one document captures all of this.

### 1.4 Why a bible

The DD bible solved an analogous problem at larger scale. It is the operator's stated gold standard. Empirical evidence from DD: every code change updates the bible; the bible has dated lock points; the bible has a "What Was Fixed — Do Not Revert" section (verified: DD § 18 at line 2160) that functions as institutional immune memory; the bible has Forbidden Patterns (verified: DD § 20 at line 2394, dated "locked 2026-04-21") distinct from Common Mistakes (verified: DD § 19 at line 2258) and Deprecated Fields (verified: DD § 21 at line 2456). The discipline has prevented regression on a system spanning Lambda + Node.js EC2 draft server + worker_package + frontend (verified: DD bible lines 418, 1768, 2161 reference the EC2 Node.js draft server; DD has multiple canonical objects — Player at § 4 / line 590, Contract-Salary-Keeper "Financial" at § 4.5 / line 800, League at § 5 / line 1365, Pricing at § 10 / line 1657 — all verified by grep).

DD's single-file bible is feasible because DD's complexity, while broad, is organized under one dependency graph and one primary deploy unit (with the draft server as a clearly-bounded peripheral). EE's complexity is differently organized: separate inference pipelines per model family, separate Lambda code paths per runtime context, train/inference FE as a structural duplication kept in lockstep. The bible spanning multiple files (working hypothesis: 5–7 documents per § 3.2, with three ML-specific documents minimum locked in § 3.2.1) is a response to **navigability and locality of reference** at expected scale plus the substantive forcing functions § 3.2.1 names.

EE needs the same discipline DD has. The bible is the substrate that makes the discipline possible.

### 1.5 Why this is a "plan to plan"

Phase 0 is methodology, not content. Five documents define how the bible gets built; they do not contain bible material themselves (with the limited exception that worked examples in this document and others must use real EE patterns to be useful as templates — see § 6.5 on the tier model). The cleanest possible separation between methodology (Phase 0) and substance (Phase 1) preserves a property the operator considers non-negotiable: the methodology must be rigorous enough that when QB specs (or CC drafts) a Phase 1 task, execution is reproducible — different CC sessions given the same spec produce structurally equivalent output. Drift between executions is the failure mode this whole effort is trying to prevent at the system level; the same property must hold at the methodology level.

---

## 2. Scope

### 2.1 What the bible IS

The Architecture Bible is the authoritative reference for what EE is, how it works, and what rules govern changes to it. It documents the system as it exists, not as anyone wishes it existed. It captures dated lock points so that future readers know when each rule was last validated against reality. It includes Forbidden Patterns (design rules new code must not violate), Common Mistakes (real bugs that recurred and must not be reintroduced), and Deprecated Fields (queue of cleanup work tracked in adjacent phase documents).

The bible is the law for new development. Every code change updates it. Every architectural decision is captured in it with a dated lock point. The operator does not deploy code that violates it without first updating it.

### 2.2 What the bible IS NOT

The bible is not a tutorial. It is not a sales document. It is not aspirational. It is not a specification for what EE should become — that's Phase 4's gap analysis output. It is not a backlog tracker; cleanup queues live in `PHASE_5_BACKLOG.md` (modeled on DD's `PHASE_B_BACKLOG.md` discipline). It is not where session logs go. It is not where running notes go.

The bible is not generated fresh from a clean room — it documents what exists, including the parts the operator may decide to throw out in Phase 5.

### 2.3 In-scope artifacts (everything in EE)

The full EE footprint is in scope for the bible. Inventory below verified against live AWS state:

- **Code:** all of `/home/strakajagr/projects/equine-equalizer/`, including `backend/`, `frontend/`, `model/`, `infrastructure/`, `scripts/`, and `equibase_probe/`
- **AWS Lambda functions (8 total = 5 Active + 3 INACTIVE):**
  - Active (5): `equine-inference`, `equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference`, `equine-nyra-workouts`
  - **INACTIVE (3): `equine-ingestion`, `equine-feature-engineering`, `equine-results`** (all three with StateReason: "The function is trying to use a deleted image"). Verified via `aws lambda get-function` per Lambda. Note: this corrects v2's claim of 2 INACTIVE; the third (`equine-results`) was missed by both the dump and v2 audit.
- **EventBridge rules (13 total = 10 ENABLED + 3 DISABLED):** verified live. DISABLED (3): `equine-feature-engineering-daily`, `equine-inference-daily`, `equine-weekly-retrain-pl`. ENABLED (10): `equine-angle-stats-nightly`, `equine-daily-retrain-full`, `equine-fetch-results-nightly`, `equine-ingestion-daily`, `equine-ls-inference-daily`, `equine-nyra-workouts-daily`, `equine-pl-inference-daily`, `equine-results-daily`, `equine-weekly-retrain-wr`, `equine-wr-inference-daily`.
- **ECS Fargate:** cluster `equine-cluster`; 5 task definition families starting with `equine`: `equine-training`, `equine-training-daily-full`, `equine-training-manual`, `equine-training-pl`, `equine-training-win-prob` (verified live; dump listed 3 — the dump missed `equine-training` and `equine-training-win-prob`). Phase 1 ML Layer Architecture Bible enumerates active vs retired families.
- **S3 buckets (4):** `equine-frontend`, `equine-model-artifacts`, `equine-processed-data`, `equine-raw-data`
- **API Gateway v2:** id `gb5qlfy10h`, 41 routes (verified live)
- **ECR repositories:** `equine-training`, `equine-nyra-workouts`, `equine-equibase-acquisition`, plus `cdk-hnb659fds-container-assets-584812014683-us-east-1` (CDK-managed, currently 5 images — INACTIVE Lambda images have been culled)
- **RDS PostgreSQL instance** `equine-db` (one; standalone instance, not part of an RDS cluster — `DBClusterIdentifier=None`. Engine `postgres` 16.6, `db.t4g.micro`, endpoint `equine-db.cgtuh834bttd.us-east-1.rds.amazonaws.com:5432`. Verified live 2026-05-05 per Architecture Overview v1 verification log Claim V1-11. Inherited Aurora cluster ARN claim REFUTED 2026-05-05 per Architecture Overview v1 verification log Claim A.8.)
- **Secrets Manager (3 entries):** `equine-equalizer/db-credentials`, `equine-equalizer/2captcha-api-key`, `equine-equalizer/brightdata-api-key` (the latter two have zero code consumers per `grep -r 2captcha\|brightdata`)
- **SNS:** `equine-equalizer-alerts` (1 topic)
- **Database:** 14 tables + 1 materialized view (`trainer_stats`) — verified by counting unique CREATE TABLE statements across `schema.sql` and migrations 001–011. Includes the migration runner mechanism (`backend/database/migrations/migrate.py`, tracking by filename in `schema_migrations` table).
- **External integrations:** HRN scraper, NYRA scraper, Equibase chart parser path (PDFs in S3), the `equibase_probe/` exploratory work, ECR image `equine-equibase-acquisition`
- **Stored-but-unused credentials:** 2captcha API key, brightdata API key
- **Disabled-but-existing infrastructure:** disabled cron rules, INACTIVE Lambdas, deleted ECR images that Lambda configs still reference

Nothing about EE is out of scope for the bible's audit and documentation work. This explicitly includes parts that are broken, partially-built, exploratory, or arguably should be deleted. The bible documents what is, not what should be — Phase 4 makes the should-be calls.

The data acquisition layer is in scope. Documentation discipline for this layer is specified in § 7.9 (Data Acquisition Honesty Protocol). Disposition vocabulary (autonomous / monitored / scheduled-manual / paid-replacement / kill) is specified in § 3.5 as a Phase 4 prerequisite. Vocabulary is shared across § 7.9 and § 3.5; aligned in v3.

### 2.4 Out of scope for the bible (but in scope for the project)

A small number of things belong to the project but not to the bible itself:

- **Session logs** in `docs/sessions/SESSION_*.md`. Treated as historical reference only — the directory contains files dated 2026-03-15, predating the architectural work that the bible documents. The bible regenerates fresh from code, AWS state, operator-stated history, and behavioral observation. Session logs may be selectively mined if Phase 1 audits surface decisions that cannot be reconstructed from primary sources, but they are not foundational input. Edge case: if a Phase 1 audit cannot reconstruct architectural rationale from primary sources, QB surfaces to Tony, who decides whether to read the relevant session log into the audit substrate. This is a per-finding judgment, not a default behavior.
- **Bug tickets and triage queue.** The bible names known bugs in the "What Was Fixed" and "Currently Open" sections, but the working triage queue lives in `PHASE_5_BACKLOG.md` (TRIAGE_QUEUE_SPEC.md defines the format).
- **Phase-specific cleanup work.** Modeled on DD's `PHASE_B_BACKLOG.md` — referenced from the bible by phase number (e.g., "Phase 5.7.2") without detailing in the bible itself.
- **Audit responses and verification logs.** Live at `/docs/bible/_meta/_audits/` per the convention documented in § 3.8.

---

## 3. Workflow Across All Five Phases

### 3.1 Phase 0 — Methodology (current phase)

**Goal:** produce 5 methodology documents at `/docs/bible/_meta/`.

**Deliverables (sequential, each depends on prior):**
1. `META_PLAN.md` — this document. Why, what, workflow, document inventory, roles, drafting authority, convergence criterion, maintenance protocol. **Includes the Phase 1 ML re-architecture forcing function (§ 3.2.1).**
2. `BIBLE_STRUCTURE_SPEC.md` — TOC and section templates for every Phase 1 bible document, including the three ML-specific documents per § 3.2.1.
3. `AUDIT_METHODOLOGY.md` — how to conduct Phase 1 audits.
4. `CONVERGENCE_CRITERIA.md` — how each phase knows it is done.
5. `TRIAGE_QUEUE_SPEC.md` — format for findings discovered during audit.

**Discipline:** observation-only on the codebase. Phase 0 documents do not contain EE specifics for content purposes — only methodology. However, *worked examples in Phase 0 documents* must use real EE patterns; this is the overlap that v2 mishandled and that § 6.5's revised tier model addresses. Phase 0 sessions read EE only enough to (a) validate that methodology is achievable and (b) ground worked examples in real patterns; they do not draft bible content.

**Per-deliverable cycle (the locked workflow):**
1. Drafting authority is determined per document type per § 6.5 (verification-aware tier model)
2. The drafting party (QB or CC) produces the draft under verification discipline
3. QB reads draft fully (synthesizing if CC drafted)
4. QB specs audit-CC task with explicit adversarial scope (six questions per § 6.2)
5. QB runs audit CC fresh
6. Audit findings return; QB synthesizes
7. If routine: QB re-specs/re-drafts, re-runs, repeats 3–6 until audit clean
8. If architectural: QB surfaces to Tony with proposed resolutions and tradeoffs; Tony decides
9. Repeat until audit clean (Tony's threshold: < 5 MATERIAL findings AND zero fabricated-content findings AND zero methodology-interpolation findings)
10. Deliverable locks

**Edge cases in the cycle:**

- **CC↔audit-CC disagreement:** When CC defends its draft against audit-CC findings (rare — CC sessions don't persist between audits), the default is **audit-CC wins**. CC is fire-and-forget. If QB judges the audit-CC finding itself questionable, QB may run a third fresh CC session to adjudicate, but this is a last resort.

- **Audit-CC error:** Audit-CCs can be wrong too. v3 surfaced one v2-audit error: the v2 audit claimed deploy artifacts were not gitignored, but they were. v6 surfaces another: the v5 audit characterized the operator memory file as "silent on exacta payout status," but re-reading the file shows it explicitly states "Place, show, and exacta payouts still populate." When verification contradicts an audit-CC finding, QB surfaces both: the original audit finding AND the contrary verification, and Tony decides whether the audit-CC needs the methodology refined or whether the draft missed something.

- **Tony's locked decision based on a wrong premise:** When verification surfaces that a Tony-locked decision was based on a premise that turns out to be false (e.g., Tony's Q4 in the v3 cycle was based on v2 audit's incorrect "not gitignored" claim; Tony's MINOR #5 instruction in the v6 cycle was based on v5 audit's incorrect "memory file silent on exacta" claim), CC does NOT silently revise. CC surfaces the contradiction to QB, who surfaces it to Tony with the verified facts. Tony ratifies the reframing or holds the original. v3 → v4: this happened with Q4. v5 → v6: this happened with the exacta claim — v6 applies a reframing that's faithful to the memory file and surfaces.

- **CC methodology-interpolation pattern (v3 → v4 → v5 → v6 lessons):** CC has a recurring failure mode — extending Tony's locked answers with adjacent policy CC believes follows from the answer. Instances surfaced and dropped in successive cycles: v3 § 7.10 ("Steps 5 and 6 happen in the same working session"), v4 § 9.13 ("Removing any one converts the documentation back to the FORBIDDEN form"), v5 audit's M-1 finding (§ 5.3 "3 consecutive iterations" iteration cap, CC-introduced in v3 cycle without Tony's explicit ratification). v6 cadence-neutralizes M-1 and expands the methodology-interpolation rule's scope (§ 6.1) with named patterns + catch-all clause + grandfathering clause that makes the "explicitly ratified" boundary computable.

- **Post-lock revision:** If a Phase 0 document locks, then weeks later a finding contradicts locked content, the procedure is: QB surfaces to Tony. Tony decides whether to (a) revise the locked document and trigger re-audit + dependent-document re-validation per § 4.1's dependency chain, or (b) document the discrepancy as a known-issue with dated note. Default is (a).

- **Audit findings with downstream consequences:** When audit-CC surfaces a fact that contradicts not just the audited document but the upstream substrate (e.g., audit-CC verifies live AWS and finds the dump is wrong), the procedure is: (1) revise the document being audited to use the verified fact, (2) flag the substrate inaccuracy for Phase 1 to correct, (3) note in the document's revision history that the discrepancy was caught here.

- **Convergence test failure (§ 5.4):** If § 5.3's convergence test fails repeatedly on the same dimension, QB escalates to Tony for a methodology-protocol revision rather than continuing to iterate. Specific count threshold is deferred to Phase 5 working agreements per the pattern established in § 7.10 and § 7.13.

**Phase 0 exit criteria:**
- All 5 Phase 0 documents locked
- The operating-model convergence test (§ 5.4) returns clean
- EE production code is committed to baseline (§ 3.1.1)
- `.gitignore` baseline audit performed and findings documented at `_audits/gitignore_baseline_audit.md` (§ 7.14)
- `PHASE_5_BACKLOG.md` created at `/docs/bible/PHASE_5_BACKLOG.md` (or final location per BIBLE_STRUCTURE_SPEC.md) with Bug #28 as first entry (§ 8.2)

### 3.1.1 Pre-Phase-1 commit-to-baseline prerequisite

Before Phase 1 begins, Tony commits all uncommitted EE production code to a baseline commit. This is a Phase 0 exit prerequisite, not a Phase 1 finding.

Rationale: Phase 1 builds the bible. The bible documents what is deployed. If the bible is documenting code that exists in production but in no commit, the bible itself is documenting a fiction. Commit-to-baseline is a prerequisite for honest bible content.

The baseline commit message reads: "Pre-bible baseline commit. Code state captured here is what Phase 1 will document. Discrepancies found during Phase 1 audit will be flagged and resolved." From this commit forward, the commit-before-deploy discipline (§ 7.10) is in force.

If Phase 1 audits find deployed-state-vs-baseline drift after the baseline commit (e.g., a Lambda image whose source no longer exists in any commit), each instance is a Phase 1 triage queue entry. Remediation is committing the deployed source as a remediation commit before Phase 5 work touches that Lambda.

### 3.1.2 Phase 0 deliverable duration estimates

Deliberately wide ranges. These are estimates of effort, not commitments. The cadence in the v1 → v6 cycle (multiple drafts per day) reflects compressed per-cycle iteration; the estimates below are calendar-time-to-lock including audit cycles converging.

| Deliverable | Estimate | Notes |
|---|---|---|
| META_PLAN.md (lock) | 2–5 days | Tier 3 under revised model; v6 in progress |
| BIBLE_STRUCTURE_SPEC.md | 3–7 days | Tier 3, multi-document scope; satisfies § 3.2.1 forcing functions |
| AUDIT_METHODOLOGY.md | 3–7 days | Tier 3, procedural with templates |
| CONVERGENCE_CRITERIA.md | 1–3 days | Tier determined pre-hoc per § 4.1 |
| TRIAGE_QUEUE_SPEC.md | 2–4 days | Tier 3, format-heavy with example entries |
| Convergence test execution | 2–5 days | One spec, two CC executions, one audit |
| Pre-Phase-1 baseline commit | < 1 day | Tony performs |
| `.gitignore` audit sweep | < 1 day | ~15-minute task; QB compares deploy script artifact-writes vs `.gitignore`; findings in `_audits/gitignore_baseline_audit.md` (§ 7.14) |

**Phase 0 total estimate: 2–4 weeks.** Operator has stated no time limit; duration is governed by audit cycles converging, not by calendar.

### 3.2 Phase 1 — Build the Bible

**Goal:** produce 5–7 EE-specific bible documents at `/docs/bible/` (final location, names, internal structure decided in BIBLE_STRUCTURE_SPEC.md, subject to the floor on ML-specific documents established in § 3.2.1).

**Working hypothesis on document split (provisional names; BIBLE_STRUCTURE_SPEC.md may rename):**
1. **Architecture Overview** — system topology, deployment unit boundaries, data flow at the runtime-context level, the cross-runtime invariants, the canonical objects shared across the system, an INDEX section linking to the other bible documents
2. **Data Pipeline Bible** — daily ingestion, results matching, workout collection, chart parsing, retraining cadence, EventBridge schedule, failure modes, the Data Acquisition Honesty inventory (per § 7.9 protocol)
3. **ML Layer Architecture Bible** (provisional name; satisfies Forcing Function 2 per § 3.2.1) — model families (WR/PL/LS), model registry semantics (specifically: what "active" means when 88 = 45 active + 43 inactive simultaneously per § 1.3 decomposition), per-model type / inputs / outputs / pipeline position / target latent / composition with other models, calibration / bypass state, the 7-layer LS stack
4. **Model Evaluation & Retraining Bible** (provisional name; satisfies Forcing Function 3 per § 3.2.1) — per-model success criteria, retraining triggers (data drift detection, performance degradation thresholds, scheduled retrains), calibration discipline as process (when calibration is fitted, when it is bypassed, why), model artifact version control beyond the registry's `is_active` flag, deployment gating (what must be true for a new artifact to ship to production)
5. **Feature Provenance Bible** (provisional name; satisfies Forcing Function 1 per § 3.2.1) — for every feature × every model: source data → engineering code → consuming model(s) → target latent. The train/inference duplication structural reality, the single-source-of-truth pattern (gonzo_features.py) and the manual-review pattern (everything else), feature schema canonical definitions, RANKER_FULL_CULL discipline
6. **Database & Schema Bible** — 14 tables + materialized view, migration discipline (per § 7.12 specific rules), JSONB conventions where present, the predictions-table family (predictions / wr_predictions / pl_predictions / ls_predictions, including the legacy table whose status is documented in Appendix A.4)
7. **API & Frontend Bible** — Lambda-handler-as-router pattern, 41 API Gateway routes, frontend consumption rules, axios client conventions

(BIBLE_STRUCTURE_SPEC.md may revise the names, internal structure, or add additional documents; per § 3.2.1, BIBLE_STRUCTURE_SPEC.md may NOT reduce the three ML-specific documents below three. The non-ML documents in this list are provisional and may be merged or split.)

**Rationale for multi-file (vs DD's single file):** DD's bible is at 2,578 lines (verified via `wc -l`) and the operator has stated it is approaching the size at which a single file becomes hard to navigate. EE has multi-pipeline + multi-runtime breadth that will exceed DD's size comfortably, AND has the Phase 1 ML re-architecture forcing function locked in § 3.2.1 — the three ML-specific documents serve three audiences (feature-centric, model-centric, process-centric) that resist combination. The split is for navigability + locality of reference + forcing-function service, not because EE is "structurally different from DD" — DD is also multi-runtime (Lambda + Node.js EC2 draft server, verified at DD bible lines 418/1768/2161). The split is a navigation + audit-discipline choice, not solely an architectural one.

**Per-document cycle:** same locked workflow from § 3.1, with drafting authority per § 6.5. Multiple CC sessions may execute different bible documents in parallel; each goes through its own audit cycle.

**Discipline:** observation-only on the codebase. Phase 1 documents the system as it exists. No fixes during audit. No "this looks wrong, let me change it." Findings go to the triage queue (TRIAGE_QUEUE_SPEC.md format).

**Phase 1 exit criterion:** all bible documents locked AND a final cross-document consistency audit passes.

**Phase 1 estimate: 4–8 weeks.**

### 3.2.1 Phase 1 design constraint (the ML re-architecture forcing function)

The Architecture Bible exists to make ML re-architecture tractable. The current model gallery does not predict winners well — Derby Day 2026 evidence (operator-stated; not independently verified at primary-source granularity, but the lived-experience direction is the operative fact for this design constraint): counterfactual loss roughly $-108 against operator's actual roughly $-150; no model picked the Derby winner; gonzo style produced predictions identical to general style at rank=1 due to feature gaps. Fixing this requires evaluating, rebuilding, and retraining models against new data, with multiple ML layers (Bayesian, XGBoost, LSTM, RF, ensemble) composing effectively. A bible that thoroughly documents the current code and infrastructure but does not directly support evaluate / rebuild / retrain workflows would be the wrong bible.

BIBLE_STRUCTURE_SPEC.md (the next Phase 0 deliverable) must produce a Phase 1 document inventory that satisfies three forcing functions, served by three separate Phase 1 documents minimum:

**Forcing function 1: Feature Provenance**

A bible document that documents, for every feature × every model: source data → engineering code → consuming model(s) → target latent → train/inference duplication or divergence. Forcing function answers: "if I change feature X, what breaks?" Audience: feature-centric change-impact analysis. The reader needs to trace any feature from its raw data source through engineering to every model that consumes it, and identify whether the engineering is shared (single source) or duplicated (parallel implementations subject to drift).

**Forcing function 2: ML Layer Architecture**

A bible document that documents, for every model in the gallery: type (XGB / LSTM / Bayesian / RF / ensemble), inputs, outputs, position in inference pipeline, target latent, output composition with other models, calibration / bypass state. Forcing function answers: "if I add a new ML layer, where does it plug in?" Audience: model-centric composition design. The reader needs to understand how the gallery's models compose: which feed which, what each measures, where calibration is applied or bypassed, how a new layer would integrate.

**Forcing function 3: Model Evaluation & Retraining**

A bible document that documents per-model: success criteria, retraining triggers (data drift, performance degradation, schedule), calibration discipline as process, model artifact version control, deployment gating. Forcing function answers: "is the model still working, when do I retrain it, what gates deployment?" Audience: process-centric operational discipline. The reader needs to know when a given model is failing, what triggers re-training, what discipline governs the calibration applied to it, and what must be true for a new model artifact to deploy.

**Why three separate documents minimum, not one combined "ML Bible":**

The three forcing functions answer different questions for different audiences. Provenance is feature-centric (change-impact). Architecture is model-centric (composition). Evaluation is process-centric (operational). Merging produces a document where the weakest framing wins — a combined "ML Bible" can be technically exhaustive and operationally useless because it answers everything in aggregate and nothing cleanly. Three separate documents force three separate audit cycles against three distinct criteria, which is the discipline that prevents shortchange of any single forcing function.

**Authority:**

BIBLE_STRUCTURE_SPEC.md may rename these documents, specify their internal structure, or add ML-specific documents beyond these three. **BIBLE_STRUCTURE_SPEC.md must specify three separate Phase 1 documents — three distinct .md files at three distinct paths — one per forcing function. A single file with three sections does not satisfy this requirement; the documents must be physically separate files at separate paths so they receive separate audit cycles, separate lock dates, and separate maintenance discipline.** This is locked at META_PLAN level, not deferred to BIBLE_STRUCTURE_SPEC.

**The other Phase 1 documents** (Architecture Overview, Data Pipeline, Database & Schema, API & Frontend, plus any others BIBLE_STRUCTURE_SPEC adds) document infrastructure context that the three ML documents reference. They support the ML re-architecture; the ML documents are the artifact's load-bearing core.

**Convergence test for the Phase 1 inventory:** any Phase 1 document inventory BIBLE_STRUCTURE_SPEC.md produces must be auditable against the question: "given this inventory, can a fresh CC session evaluate, rebuild, or retrain a model in the gallery?" If the answer is no for any of the three workflows, the inventory has not satisfied the forcing function and must be revised.

### 3.3 Phase 2 — Adversarial Bible Audit

**Goal:** Phase 1 produced bible content. Phase 2 stress-tests it.

A fresh CC session, with no involvement in Phase 1 drafting, audits the entire bible against the actual codebase. Adversarial scope is the same six questions specified in § 6.2 plus three Phase 2-specific additions:

1. Does the bible say something the code does not do?
2. Does the code do something the bible does not say?
3. Where do bible documents contradict each other across files?

Per-document deliverable: an audit report file at `/docs/bible/_audit/<bible_doc_name>_audit.md` enumerating findings. After all per-document audits, a cross-document consistency audit produces `/docs/bible/_audit/cross_document_audit.md`.

Phase 2 audit-CCs are independent across documents — each gets its own paste-ready prompt; no sharing of draft state across audits. The cross-document audit is a separate session that reads all per-document audits as input.

If a per-document audit returns >5 MATERIAL findings, that document goes back to Phase 1 revision before the cross-document audit runs.

Adversarial findings go to QB → Tony for resolution. Resolution may be: revise the bible, fix the code (deferred to Phase 5), or document an intentional exception with rationale and dated lock point.

**Phase 2 exit criterion:** all adversarial findings resolved or scheduled.

**Phase 2 estimate: 1–2 weeks.**

### 3.4 Phase 3 — Predictive Concept Inventory

**Goal:** independent of current code, enumerate everything that CAN be predicted from horse racing data, organized by latent factors.

This phase is **domain-driven, not code-driven**. The bible (Phases 1–2) documented what the code does. Phase 3 asks: what could the code do, given the data available and the domain's predictive structure?

**Deliverable format:** `/docs/bible/PREDICTIVE_CONCEPTS.md`. One section per latent factor. Each section documents:
- Factor name and definition
- Data signal (what raw data captures this factor)
- Current EE coverage (which features in the existing code capture it, if any) — cross-references the Feature Provenance Bible by section
- Theoretical maximum coverage (what features could capture it given current data)
- Cross-references to bible documents that touch this factor

Quality bar for "all major latent factors documented": each operator-surfaced factor has a section AND any factor surfaced during Phase 3 by domain reasoning has a section. CC may not skip a candidate because "current EE has no coverage"; the absence is the finding.

Candidate latent factors (operator-surfaced, not exhaustive):
- Pace shape projection from PP call positions
- Per-horse pace-driver detection (drives / presses / sits / closes)
- Surface transitions (dirt vs poly vs turf, first-time-on-surface)
- Sire/dam genetics (sire's turf record, dam's distance preferences)
- Layoff patterns and trainer angles
- Race-shape × running style interaction
- Equipment changes (first-time blinkers, Lasix)
- Trainer/jockey combinations
- Class moves (up/down)
- Distance changes (stretch out / cut back)

**Phase 3 exit criterion:** PREDICTIVE_CONCEPTS.md locked, all operator-surfaced and Phase-3-surfaced factors documented.

**Phase 3 estimate: 1–2 weeks.**

### 3.5 Phase 4 — Gap Analysis

**Goal:** compare bible (Phase 1+2) against concept inventory (Phase 3). Produce three deliverables:

1. **Feature taxonomy** (`/docs/bible/FEATURE_TAXONOMY.md`)
2. **ML re-architecture spec** (`/docs/bible/ML_RE_ARCHITECTURE_SPEC.md`)
3. **Per-component disposition** (`/docs/bible/COMPONENT_DISPOSITION.md`): for every existing feature, model, table, scraper, Lambda — assign a disposition.

**Disposition vocabulary (canonical, shared across § 3.5 and § 7.9):**

| Disposition | Meaning |
|---|---|
| keep | Component continues unchanged |
| refactor | Component continues but is rewritten |
| replace | Component is removed and replaced with different implementation |
| kill | Component is deleted with no replacement |
| autonomous | (Data sources only) Continues to run without human intervention; failure mode is monitored |
| monitored | (Data sources only) Continues to run autonomously; failure escalates to operator within hours, not days |
| scheduled-manual | (Data sources only) Operator runs daily script to acquire data; no autonomous attempt |
| paid-replacement | (Data sources only) Replace with paid API |

**Disposition gating:**
- "kill" decisions require Tony's explicit signoff before Phase 5 acts
- "replace" dispositions must be paired with a Phase 5 spec specifying the replacement before Phase 5 acts
- "refactor" dispositions must specify the discipline change being introduced (often a new Forbidden Pattern)
- Data source dispositions tie back to § 7.9 Data Acquisition Honesty Protocol — each source must have a documented honest disposition

**Phase 4 exit criterion:** all three deliverables locked; per-component disposition complete with gating satisfied.

**Phase 4 estimate: 1–3 weeks.**

### 3.6 Phase 5 — Execution

**Goal:** build the missing features, retrain models against new feature taxonomy, deploy, integrate triage-queue bug fixes (#7, #15, #24, #25, #28, plus anything Phase 1–4 surfaces).

**Discipline shifts:** Phases 0–4 are observation-only. Phase 5 makes changes. Every change updates the bible per the maintenance protocol (§ 7). Every change is committed before deploy per § 7.10. Every commit references the bible section affected per § 7.11.

**Phase 5 working agreements (audit cadence, drift-detection cadence, commit cadence, Layer 1 enforcement form, iteration-cap thresholds, session protocols):** designed at Phase 5 entry, not in Phase 0. Phase 0 documents the disciplines that survive into Phase 5; Phase 5 designs the operating cadences, count thresholds, and physical-form choices that govern Phase 5 sessions.

**Phase 5 exit criterion:** open-ended. Phase 5 is where EE goes back to being a normal active codebase under bible discipline.

### 3.7 Total estimate

Phases 0–4 sum: low 2+4+1+1+1 = **9 weeks**; high 4+8+2+2+3 = **19 weeks**. The wide range reflects audit-cycle dependence on convergence, not calendar-driven delivery. Operator has stated no time limit.

(v2 reported 9–17 weeks, which was an arithmetic error — the high end is 19, not 17. v3 corrected.)

### 3.8 Audit and verification subdirectory convention

All audit responses and verification logs live at `/docs/bible/_meta/_audits/` (for Phase 0 documents) or `/docs/bible/_audit/` (for Phase 1 bible documents per § 3.3).

Naming convention:
- Adversarial audit: `<doc>_v<N>_audit.md`
- Verification log: `<doc>_v<N>_verification.md` (companion to any CC-drafted Tier 3 deliverable per § 6.5)
- Phase 0 prerequisite audits: descriptive names (e.g., `gitignore_baseline_audit.md`)

Examples:
- `_audits/META_PLAN_v5_audit.md`
- `_audits/META_PLAN_v6_verification.md`
- `_audits/gitignore_baseline_audit.md`
- `_audit/data_pipeline_bible_v1_audit.md` (Phase 1)

This convention is canonical from v3 forward. Phase 1 documents follow the same pattern.

---

## 4. Document Inventory (Phase 0 + Phase 1)

### 4.1 Phase 0 documents (this phase)

All at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/`:

| Order | Document | Purpose | Tier |
|---|---|---|---|
| 1 | META_PLAN.md | This document. Top-level plan. | **3** (CC-drafted under QB spec, with verification log; CC-audited) |
| 2 | BIBLE_STRUCTURE_SPEC.md | TOC and section templates for Phase 1 bible documents; satisfies § 3.2.1 forcing functions. | **3** (CC-drafted under QB spec, with verification log; CC-audited) |
| 3 | AUDIT_METHODOLOGY.md | How to conduct Phase 1 audits. | **3** (CC-drafted under QB spec, with verification log; CC-audited) |
| 4 | CONVERGENCE_CRITERIA.md | How each phase knows it is done. | Determined pre-hoc per § 6.5; see footnote |
| 5 | TRIAGE_QUEUE_SPEC.md | Format for findings discovered during audit. | **3** (CC-drafted under QB spec, with verification log; CC-audited) |

Tier assignments updated from v2 per § 6.5's revised model. Sequence is intentional. Each later document depends on earlier ones being locked.

**CONVERGENCE_CRITERIA.md tier determination (pre-hoc, per § 6.5):** QB judges at spec-writing time whether the document can be drafted without any EE-specific factual claims. If clearly yes, QB writes a Tier 1 spec; if clearly no, QB writes a Tier 3 spec; if unclear, QB defaults to Tier 3 (a Tier 3 spec is strictly more rigorous than a Tier 1 spec, so the default protects against undetected EE references). The tier determination is recorded in the spec itself; it is not revisited mid-draft.

### 4.2 Phase 1 documents (next phase, working hypothesis)

Working count: 5–7 bible documents (5 minimum: 3 ML-specific per § 3.2.1 plus at least Architecture Overview and one infrastructure document; final count up to BIBLE_STRUCTURE_SPEC.md). All Tier 3. Final count, names, location, and split decided in BIBLE_STRUCTURE_SPEC.md, not here, subject to the floor on ML-specific documents (≥ 3) established in § 3.2.1.

Whether a top-level INDEX file exists (linking bible documents into a coherent corpus) is a BIBLE_STRUCTURE_SPEC.md decision. Open question § 10.2.

### 4.3 Adjacent project documents (referenced from bible, not part of bible)

Modeled on DD's discipline. The single canonical name for the cleanup queue document is **`PHASE_5_BACKLOG.md`** (decided in v2; preserved through v6). All references in this document and downstream documents use this name.

| Document | Purpose | Drafting timing |
|---|---|---|
| `PHASE_5_BACKLOG.md` | Cleanup queue work scheduled for Phase 5. | Created at Phase 0 exit with Bug #28 as first entry (resolves v2 § 10.5 deferral). Continuously updated through Phase 4. Format defined by TRIAGE_QUEUE_SPEC.md (Phase 0 deliverable 5), which therefore must be locked before PHASE_5_BACKLOG.md is created. |
| `EE_CURRENT_STATE_DUMP.md` | Phase 0 input. Already exists. | Created pre-Phase-0. May be re-generated if it goes stale (§ 4.4). |
| `SESSION_HANDOFF_*.md` | Operator's running session notes. | Operator-managed. Not bible material. |
| `/docs/bible/_meta/_audits/<doc>_v<N>_audit.md` | Phase 0 adversarial audit responses. | Created during Phase 0 per § 3.8. |
| `/docs/bible/_meta/_audits/<doc>_v<N>_verification.md` | Verification logs for CC-drafted Tier 3 Phase 0 docs. | Created at Phase 0 drafting time per § 3.8. |
| `/docs/bible/_meta/_audits/gitignore_baseline_audit.md` | Phase 0 prerequisite audit per § 7.14. | Created at Phase 0 exit. |
| `/docs/bible/_audit/<doc>_audit.md` | Phase 2 per-document audit reports. | Created during Phase 2. |
| `/docs/bible/_audit/cross_document_audit.md` | Phase 2 cross-document consistency audit. | Created during Phase 2. |

### 4.4 EE_CURRENT_STATE_DUMP staleness procedure

The dump was generated 2026-05-03. Phase 1 may begin weeks later. If during Phase 1, audit-CC verifies a dump claim against live state and finds disagreement, the procedure is:

1. Document the discrepancy in the audit report
2. The Phase 1 document being drafted uses the verified live state, not the dump value
3. The dump itself is NOT updated — it remains a snapshot-in-time reference
4. If discrepancies accumulate (>5 per Phase 1 document), QB surfaces to Tony, who may order dump regeneration

The dump is **best-available baseline, not source of truth**. The v3 verification process found multiple dump errors (INACTIVE Lambda count, ECS task family count) — Phase 1 audits will find more. Dump errors are expected; verification is the safeguard.

### 4.5 Source authority hierarchy

When sources conflict, this is the priority order. (Detailed resolution rules in § 8.5.)

1. **Live AWS state** (introspection via `aws` CLI): authoritative for "what infrastructure exists right now"
2. **Live API endpoints** (HTTPS calls to `gb5qlfy10h.execute-api.us-east-1.amazonaws.com`): authoritative for runtime data state when the relevant Lambda is Active. Note: dashboard endpoint works even when `equine-ingestion` is INACTIVE because it is served by `equine-inference`.
3. **Live database state** (introspection via `raw_query` action when `equine-ingestion` is restored, or direct connection via DB credentials): authoritative for "what data exists right now" when Lambda-mediated path is unavailable
4. **Code in working tree** (after pre-Phase-1 baseline commit): authoritative for "what the source-of-deployed-code says the system does." Pre-baseline-commit, working tree may diverge from deployed Lambda images; tier 1 (AWS state) governs in that case.
5. **Operator-stated history** (Tony's verbal/written context): authoritative for "why decisions were made"
6. **EE_CURRENT_STATE_DUMP.md**: best-available baseline only
7. **Session logs** (`docs/sessions/`): tertiary reference, used only when 1–6 cannot reconstruct rationale

**Worked example — AWS-vs-DB conflict resolution for `equine-results`:**

Question asked of Phase 1 audit-CC: "Is `equine-results` Lambda currently running, and does it have produced output?"

- **Tier 1 (AWS):** `aws lambda get-function --function-name equine-results --query 'Configuration.[State,StateReason]'` returns `Inactive | The function is trying to use a deleted image.`
- **Tier 3 (DB):** `SELECT MAX(created_at) FROM results;` returns a timestamp from before the deactivation date. (Phase 1 audit-CC runs this query; v6 main doc cannot independently verify the timestamp because production DB access requires the path through equine-ingestion which is INACTIVE. Documented as analytical pattern, not as verified current state.)
- **Tier 1 wins for "currently running":** Lambda is INACTIVE; it is not currently producing output.
- **Tier 3 wins for "produced output historically":** the rows in `results` exist and are real; they were produced when the Lambda was Active.

**Bible documents both, separately scoped:** "Lambda `equine-results` is INACTIVE as of [date]; production rows in the `results` table from before [date] were produced when the Lambda was Active. Re-activation requires rebuilding the deleted ECR image (Phase 5.X.Y)."

This is the canonical pattern: tier 1 governs current state; tier 3 governs historical evidence; both go in the bible with explicit temporal scoping.

**Cross-tier conflict resolution (added in v3, refined in v4):**

- **AWS vs DB state** (e.g., AWS shows Lambda INACTIVE but DB has rows that imply it ran): per worked example above — AWS for current state, DB for historical record, both documented with temporal scope.
- **Conflict between code modules** (e.g., `model/features/feature_definitions.py` exports a `FEATURE_GROUPS` schema and a different module also defines features): the bible documents both, identifies which is authoritative based on usage patterns (which one production training imports? which one production inference imports?), and queues the unused one for cleanup disposition. Verified case: `model/features/feature_definitions.py` is imported by `model/training/train.py:40` and `backend/services/inference_service.py:28` — it is NOT orphaned despite older claims.
- **Code vs operator memory:** bible documents what the code does (factual) and notes operator's stated rationale separately (intent). Both can coexist; the bible is honest about which is observable and which is asserted.

---

## 5. Convergence Criterion (Phase 0 specifically)

### 5.1 What we are testing for

The convergence test is **on the operating model, not output identity**. Three CCs given the same spec do not need to produce identical bible files. They need to produce structurally equivalent execution: same target questions answered, same depth of investigation, same format adherence, no drift in interpretation of the methodology.

The failure mode being tested against is silent drift between CC executions. If two CCs given the same Phase 1 spec produce documents that disagree on a system fact, audit must catch it.

### 5.2 Reproducibility of *output given the same spec*, not reproducibility of the spec itself

The methodology does not need to be so prescriptive that any Phase 1 spec is mechanically derivable from Phase 0 documents alone. The methodology needs to be rigorous enough that **once QB writes a Phase 1 spec, multiple CCs executing that spec converge on equivalent output, and audit-CC catches any divergence reliably**.

### 5.3 The test

When all 5 Phase 0 documents are drafted, audited, and locked:

1. QB writes a sample Phase 1 spec for one bible document (e.g., the Database & Schema Bible).
2. Two fresh CC sessions execute the spec independently.
3. A third fresh CC session audits both outputs against each other and against Phase 0 methodology.
4. The audit identifies all material differences between the two outputs.
5. QB reviews the audit. If material differences exist that audit-CC reliably caught, methodology is converged. If material differences exist that audit-CC missed, the methodology has gaps and Phase 0 documents need revision.

**Material difference defined:**

A difference is **material** if it falls into any of these categories:
- A factual claim about EE that differs (e.g., one says "8 Lambdas," the other says "9")
- A scope claim that differs (e.g., one includes the probe directory in its inventory, the other doesn't)
- A rule statement that differs (e.g., one document says "every change updates the bible," the other says "major changes update the bible")
- A canonical name or path that differs at the same layer (e.g., one uses `wr_predictions` table name, the other uses `wr_prediction`; cross-layer differences like `WRPrediction` dataclass vs `wr_predictions` table are NOT material because they're correct in their layers)
- A cross-reference to a different bible section (e.g., one cites "see § 7.4," the other cites "see § 8.2")

A difference is **not material** if it falls into any of these categories:
- Different ordering of sections within a chapter (assuming no canonical order is specified)
- Different choice of synonyms in non-quoted prose
- Different illustrative examples (assuming both are concrete and accurate)
- Different paragraph breaks or sentence structure

When borderline, audit-CC flags as material and lets Tony decide.

**Iteration escalation:** if the convergence test fails repeatedly on the same dimension, QB escalates to Tony for protocol revision rather than continuing to iterate. The specific count threshold for "repeatedly" is operator judgment; cadence specification (including any numerical iteration cap) is a Phase 5 working-agreements decision per the pattern established in § 7.10 (commit cadence) and § 7.13 (audit cadence). Until then, escalation timing is QB's call surfaced to Tony.

### 5.4 What "converged" looks like

Phase 0 is converged when:
- All 5 documents are locked
- The § 5.3 test runs and audit-CC catches material differences reliably
- QB's review of the audit returns no methodology gaps
- Pre-Phase-1 baseline commit is performed (§ 3.1.1)
- `.gitignore` baseline audited (§ 7.14)
- `PHASE_5_BACKLOG.md` created with Bug #28 as first entry (§ 8.2)

If § 5.3 surfaces gaps, the affected Phase 0 documents revise and re-lock. The test re-runs.

### 5.5 Generalized criterion for Phases 1–5

CONVERGENCE_CRITERIA.md (Phase 0 doc 4) generalizes this discipline for later phases. The general pattern: "phase N is done when its deliverables are audited clean and the discipline established in phase N is empirically reproducible by fresh CC sessions."

---

## 6. Roles and Drafting Authority

### 6.1 The three roles

**Tony** (operator):
- Final architectural authority
- Day-to-day owner; QB reports to Tony
- Reviews audited deliverables, not raw drafts
- Runs CC sessions (paste-ready prompts authored by QB)
- Performs pre-Phase-1 baseline commit (§ 3.1.1)
- Deploys; never delegates deployment
- From Phase 1 onward: commits before every deploy (§ 7.10), with the emergency exception specified in § 7.10

**QB** (this role):
- Tactical authority over iteration
- Drafts Tier 1 documents (per § 6.5)
- For Tier 3 documents: writes specs for CC; orchestrates CC drafting; reads CC output fully; synthesizes audit findings
- Specs audit-CC tasks (paste-ready prompts with explicit adversarial scope)
- Surfaces architectural questions to Tony with proposed resolutions and tradeoffs
- Iterates until each deliverable locks

**CC** (Claude Code, fresh sessions per task):
- Executes specs QB authors
- For Tier 3 documents: drafts under QB spec, **with hard verification discipline** (§ 6.5)
- Audits other CC sessions' output AND QB-drafted documents (separate fresh session per audit)
- No persistence between sessions; QB and Tony hold continuity
- Produces verification log alongside any Tier 3 draft (§ 6.5)
- Does NOT silently extend Tony's locked answers. If verification or drafting reveals a need for additional policy, CC surfaces to QB → Tony for explicit ratification rather than interpolating.
- Does NOT invent **binary tests, cadence rules, completeness criteria, scoring rubrics, severity thresholds, iteration caps, percentage criteria, procedural sequencing rules, or other CC-prescribed methodology constructs** that Tony has not explicitly ratified. The named patterns are illustrative, not exhaustive; the catch-all clause covers what is not named. If verification or drafting reveals a need for such a construct, CC surfaces to QB → Tony for explicit ratification rather than interpolating. (v3 → v4 → v5 → v6 lessons: v3 § 7.10 "same working session" cadence was CC interpolation; v4 § 9.13 "Removing any one converts to FORBIDDEN" was a CC-interpolated binary test; v5 audit caught v3-cycle § 5.3 "3 consecutive iterations" iteration cap as a CC-interpolated numerical threshold. All three dropped on subsequent cycles. The rule is operative immediately; it will be formally codified in AUDIT_METHODOLOGY.md.)
- **Grandfathering clause (per Tony's locked language in v6 cycle):** Pre-existing methodology constructs from earlier cycles' QB drafts are grandfathered; CC does not need to re-verify Tony's ratification of pre-existing content. New content CC introduces falls under the rule. "Pre-existing" means content that existed in any version prior to the cycle in which the rule was introduced. When a new methodology rule lands in cycle N, the cycle-N retroactive sweep covers v1 through v(N-1) CC-introduced content but treats v1 through v(N-1) QB-drafted content as grandfathered. The methodology-interpolation rule landed in cycle 5 (v5); v6's retroactive sweep covers v1-v4 CC-introduced content and treats v1-v4 QB-drafted content as grandfathered. The boundary is computable, not judgment-dependent — provenance (CC-introduced vs QB-drafted) is the discriminator, not the operator's recall of what was ratified.

### 6.2 Audit-CC explicit adversarial scope

When QB specs an audit-CC task, the spec includes these six questions verbatim:

1. What's in this deliverable that I can't verify from referenced source material?
2. What's missing based on the deliverable's stated scope?
3. Where is language ambiguous enough that two readers could interpret it differently?
4. Where does the deliverable contradict itself or other deliverables?
5. What sections feel rushed or hand-waved?
6. What examples are missing that would make abstract claims concrete?

Without explicit adversarial scope, audit-CCs default to "this looks fine." The scope forces them to find every reason the deliverable isn't ready to lock.

For Phase 2 bible audits, three additional questions are appended (§ 3.3).

A working example of the audit-CC prompt structure is in **Appendix A.6**. AUDIT_METHODOLOGY.md will produce the canonical paste-ready template; until then, A.6 is the working reference.

### 6.3 Authority boundaries

- **QB has tactical authority over iteration.** QB may propose architectural resolutions but never lock them. Tony's affirmative response is required to lock anything tagged "architectural" in the audit synthesis.
- **Tony has architectural authority.** Tony decides; Tony locks; Tony's decisions go into the bible with dated lock points.
- **CC has execution authority.** CC drafts what QB specs; CC audits what QB specs; CC does not decide architecture and does not surface findings directly to Tony.

### 6.4 What QB never does

- Never modifies code (Phases 0–4 are observation-only)
- Never deploys
- Never picks an architectural direction without surfacing to Tony when audit findings raise architectural questions
- Never accepts CC output without reading it fully (Tier 3 large outputs may be skim-read in non-critical sections, but critical sections — every fact-bearing claim, every prescription — are read fully; "critical" defaults to anywhere with verifiable claims, and audit-CC catches what skim missed)
- Never accepts an audit return without synthesizing findings and either re-specing or surfacing
- Never escalates to a "GM session" — there is no GM post-Phase 0 (§ 6.6)

### 6.5 Drafting authority by document type (verification-aware tier model)

**The methodology principle (locked):** any document containing verifiable EE-specific claims (file paths, function signatures, AWS resources, DB state, code patterns, behavior assertions, line numbers) is **Tier 3**, regardless of methodology framing density. Tier 1 is reserved for documents with **no EE-specific factual claims**. Mixed-content documents do not exist — if a document needs both methodology framing AND EE-specific examples, it is Tier 3, and the methodology framing is drafted under the same verification discipline as the examples.

This principle is the v2→v3 lesson. v2 was framed as Tier 1 (QB-drafted) because most of its content was procedural — but its Appendix A had EE-specific worked examples, and three of the five examples turned out to contain fabricated content. QB cannot prevent fabrication without filesystem access. The fix is to make any document with EE-specific claims a CC-drafted Tier 3 document, with companion verification log.

**Tier determination is pre-hoc.** QB judges at spec-writing time whether the document can be drafted without any EE-specific factual claims. If clearly yes, QB writes a Tier 1 spec; if clearly no, QB writes a Tier 3 spec; if unclear, QB defaults to Tier 3 (a Tier 3 spec is strictly more rigorous than a Tier 1 spec, so the default protects against undetected EE references). The tier determination is recorded in the spec; it is not revisited mid-draft.

**Tier 1: QB-drafted, CC-audited.**
For documents that are pure procedure with no EE-specific factual claims.

- CONVERGENCE_CRITERIA.md (only Phase 0 document targeted as a Tier 1 candidate; final tier set pre-hoc when QB writes the spec)

**Workflow:** QB drafts; QB writes audit-CC prompt; CC audits; QB synthesizes findings and revises; iterate until locked.

**Tier 3: CC drafts under QB spec, with verification log; CC audits.**
For documents that contain any verifiable EE-specific claims, regardless of methodology density.

- META_PLAN.md (this document; Appendix A has EE-specific examples)
- BIBLE_STRUCTURE_SPEC.md (section templates reference real EE patterns surfaced from current code)
- AUDIT_METHODOLOGY.md (worked examples need real EE patterns)
- TRIAGE_QUEUE_SPEC.md (example entries need real bugs)
- EE_CURRENT_STATE_DUMP.md (already exists)
- All Phase 1 bible documents (including the three ML-specific documents per § 3.2.1)
- Phase 2 audit reports
- Phase 3 PREDICTIVE_CONCEPTS.md
- Phase 4 deliverables (FEATURE_TAXONOMY.md, ML_RE_ARCHITECTURE_SPEC.md, COMPONENT_DISPOSITION.md)

**Workflow:**
1. QB writes spec: target questions, format, depth bar, source-priority rules, output location, **explicit verification discipline** (no fabrication; verify before claiming; produce companion verification log).
2. CC drafts AND produces verification log. Every factual claim about EE has a verification entry.
3. QB reads draft fully (synthesizing). QB skims verification log to spot-check entries.
4. QB writes audit-CC prompt. The audit prompt includes verification-against-live-system mandate.
5. CC audits. Audit-CC reads both the draft and the verification log; verifies a sample of verification claims against live state; reports any verification-log entries that don't hold up.
6. QB synthesizes findings; either re-specs (CC re-drafts) or surfaces architectural findings to Tony.
7. Iterate until locked.

**Verification log precision rule (v3 → v4 lesson):** verification log entries must be PRECISE about what was counted, in a form that cannot be compressed by readers. Specifically:
- Counts must be decomposed: "3 instantiations + 1 import = 4 references," not "4 references including the import"
- Claims must distinguish definitions vs uses vs imports
- Anything aggregable must be aggregated explicitly so a reader cannot compress with judgment

**Worked example of the rule (the v3 → v4 lesson concretely):**

> **v3 verification log entry (loose):** "PredictionRepository instantiated in prediction_router.py:34, 61, 92 (4 references including the import)"
>
> **v3 main doc (compressed):** "prediction_router.py (4 instantiations of PredictionRepository)"
>
> **v4 verification log entry (decomposed):** "PredictionRepository: 1 import on line 6 + 3 instantiations on lines 34, 61, 92 = 4 references total"
>
> **v4 main doc (carries the decomposition):** "3 instantiations of PredictionRepository at lines 34, 61, 92, plus 1 import on line 6 = 4 references total"

The v3 phrasing allowed a downstream reader to compress "4 references including the import" into "4 instantiations" by judgment. The v4 phrasing makes the components explicit; no compression is possible without altering the count visibly.

**Scope of the rule (per Tony's locked decision in v5 cycle):** the rule applies broadly — to any aggregable count anywhere in a Tier 3 document, not only to code-reference counts that look like the v3 BLOCKER pattern. v5 applied it to working-tree status counts (74 untracked + 29 modified = 103), model registry counts (88 = 45 active + 43 inactive), EventBridge rule counts (13 = 10 ENABLED + 3 DISABLED), and Lambda counts (8 = 5 Active + 3 INACTIVE). v6 extends to ECS task families enumerated by name (5 named in § 2.3). When in doubt, decompose; over-decomposition costs verification-log length but never costs accuracy.

**Hard rule:** Tier 3 drafts that omit a companion verification log are rejected by QB without audit. The verification log is not optional.

**Framework-rejection protocol — two markers, distinct scopes:**

When CC's verification reveals that the spec or its framing is wrong, CC returns the partial draft annotated with one of two markers:

- **`<SPEC_GAP: explanation>`** — the **entire spec's premise** is wrong. Use when verification reveals the document being specified should not exist as drafted. Example: spec asks CC to document a function that does not exist in the codebase (`get_active_model_by_type_and_style`); CC verifies the function is fictional and returns `<SPEC_GAP: function does not exist; spec needs revision before any draft can be produced>`.

- **`<FRAMEWORK_GAP: explanation>`** — a **specific framework slot** can't be filled because the framework's structure does not accommodate the actual content, but the spec's overall premise is sound. Use when the framework expects (e.g.) a "single canonical Player object" section but EE has multiple valid canonical objects per pipeline. CC fills what fits, marks the gap, and lets QB triage.

The distinction: `<SPEC_GAP>` invalidates the draft; `<FRAMEWORK_GAP>` requests a structural patch within an otherwise-valid draft. Use the more specific marker when both apply.

CC does not silently fabricate to fill either kind of gap. QB triages whether to revise the spec, the framework, or the spec's premise.

### 6.6 No GM session

GM was a methodology-drafting role during Phase 0 setup. Going forward, foundational architectural decisions belong to Tony. There is no GM session to escalate to.

When QB encounters foundational architectural questions:
1. QB surfaces to Tony with proposed resolutions and tradeoffs
2. Tony decides
3. QB executes

QB has Tony for architectural calls and the bible itself (plus the DD bible as reference) to anchor decisions. No external safety net beyond Tony.

---

## 7. Maintenance Protocol

The bible is only valuable if it stays current. DD's discipline: every code change updates the bible. EE inherits this discipline as the target state, with explicit transition mechanics (§ 7.10) to bridge from current uncommitted-deploy practice.

### 7.1 The rule

Every code change that affects anything documented in the bible — architecture, data model, API surface, ML stack, feature schema, infrastructure, data acquisition — updates the relevant bible document in the same commit as the code change.

### 7.2 What this looks like in practice (Phase 5 onward)

When Tony works on a code change with CC:
1. Before writing code, CC reads the relevant bible section
2. CC writes the code
3. CC writes the bible update for the same change
4. Tony reviews both
5. Both commit together; the commit message includes a bible reference per § 7.11
6. Tony deploys after commit (§ 7.10)

If the change introduces a new pattern, a new section gets added with a dated lock point. If the change deprecates an existing pattern, the deprecation is recorded in the bible's "Deprecated Fields" section with a phase reference for cleanup (§ 7.7).

### 7.3 Dated lock points

Every rule, pattern, decision in the bible carries a date. Format: a parenthetical "Locked YYYY-MM-DD" attached to the rule, section, or section header.

Example structure of a fully-formed locked rule (Appendix A.2 shows EE-flavored full version):

```
4.5.10 Train/Inference Feature Engineering Discipline (locked 2026-04-22)

[rule body explaining what discipline applies]

Rationale: [why this rule exists, often referencing the bug history that produced it]

Forbidden: [what new code must not do]
[FORBIDDEN code example, 3-8 lines]

Correct: [what new code must do]
[CORRECT code example, 3-8 lines]
```

When a rule changes, the new date supersedes the old. The history is preserved in git, and the bible itself shows the audit trail of when each rule was last validated.

**Placeholder-resolution sub-rule (locked 2026-05-05 per v7 cycle):**

> Phase 1 drafters MUST resolve the date placeholder via `git log` of the relevant primary source (migration file, code commit, etc.) before locking the bible document containing a W.N entry for a real fix. Placeholder (`YYYY-MM-XX`) is reserved for Appendix A's worked-example documents (Phase 0 methodology) and any other entries where the fix has not actually happened yet (forward-looking discipline codification). For real bug fixes where git log can resolve the date, the drafter MUST resolve and use the actual date.

Rationale: this sub-rule discharges a methodology gap (G8) surfaced by the operating-model convergence test on the Database & Schema Bible draft (`_audits/convergence_test_audit.md`). Two CC sessions given the same Phase 1 spec interpreted Appendix A's placeholder convention differently — one used `fixed 2026-05-XX` for migration 011's `wr_predictions` UNIQUE fix (a real fix whose date is knowable from `git log` of `011_wr_predictions_unique_fix.sql`), the other resolved to `fixed 2026-05-01`. Both choices were defensible against v6's existing language, which established the placeholder convention only for Appendix A worked examples (entries that don't yet have real dates because the bible entries don't yet exist). The convention did NOT specify what Phase 1 drafters do when writing W.N entries for fixes whose real dates ARE knowable. The sub-rule closes the divergence by making `git log` resolution mandatory whenever the fix has actually happened and the date is knowable from a primary source. The placeholder convention remains operative for the two cases it was designed for: (i) Appendix A's worked examples, where the bible entry does not yet exist; and (ii) forward-looking entries that codify discipline for fixes that haven't happened yet (the discipline locks now; the W.N entry's "fixed" date does not exist until the fix lands). Cross-reference: Appendix A lead paragraph carries the same scope-bound clarification.

### 7.4 What Was Fixed — Do Not Revert

Each bible document includes a "What Was Fixed — Do Not Revert" section scoped to that document's domain. (Divergence from DD: DD has one consolidated "What Was Fixed" section in its single bible file; EE's multi-file structure means each bible document carries its own immune memory for the bugs in its scope. Divergence is intentional.)

**Cross-cutting bug scope rule:** when a bug spans multiple bible documents (e.g., Bug #15 train/inference FE drift touches Feature Provenance Bible AND ML Layer Architecture Bible), the canonical entry lives in the document whose discipline most directly prevents recurrence (here: Feature Provenance Bible, since the prevention is a feature-engineering pattern). Other affected documents reference the canonical entry by ID. **No duplication.**

Each entry is a real bug that was found, fixed, and might be reintroduced if the lesson isn't preserved. New entries get added when bugs are fixed; entries are never removed.

Format (Appendix A.3 shows EE-flavored full version):

```
W.N: <Bug name or short description> (fixed YYYY-MM-DD)

Symptom: [how the bug manifested]

Root cause: [what the actual problem was]

Fix: [what was changed]

Why this entry exists: [what discipline must persist to prevent recurrence]
```

### 7.5 Forbidden Patterns

Separate from "What Was Fixed." Forbidden Patterns are design rules that new code MUST NOT violate, distinct from bugs that have already happened. They have lock dates and rationale.

Format follows § 7.3 (dated lock point + rationale + FORBIDDEN/CORRECT pair). Appendix A.1 shows EE-flavored full version using a real EE pattern.

EE-specific Forbidden Patterns will be developed during Phase 1 bible drafting; verified candidates surfaced from current code:

- Calling `get_active_model_by_type(model_type)` without addressing the multi-active-row reality (88 = 45 active + 43 inactive simultaneously; see § 9.13)
- Adding feature engineering logic to either `model/shared/data_loader.py` or `backend/services/feature_engineering_service.py` without parallel update to the other (the manual-cross-reference discipline, until Phase 5 extracts shared modules)

### 7.6 Common Mistakes

Distinct from both "What Was Fixed" and "Forbidden Patterns." Common Mistakes are recurring instincts the operator or CC repeatedly has that lead to bugs, captured as "wrong instinct → corrected position" pairs. Each entry begins with the wrong instinct and the corrected position.

Format inherited from DD § 19.

### 7.7 Deprecated Fields / Patterns

For things being phased out. References `PHASE_5_BACKLOG.md` by phase number. Format inherited from DD § 21.

Worked example (Appendix A.4) uses a verified EE deprecated pattern: the legacy `predictions` table that migration 005 created replacements for but did not drop, still actively read by `prediction_router.py` and `dashboard_router.py`. (v2 used `model/features/feature_definitions.py` as this example; v3 verification revealed that file is NOT orphaned. v3 replaced with the verified `predictions`-table example. v4 corrected v3's inflation. v5 maintained the v4 decomposition and added the sum on race_router.py; v6 unchanged.)

### 7.8 Triage Queue

When findings emerge during Phase 1+ audits that aren't addressed inline, they go to `PHASE_5_BACKLOG.md` per the format defined in `TRIAGE_QUEUE_SPEC.md`. Worked example sketch in Appendix A.5.

### 7.9 Data Acquisition Honesty Protocol

Per-source documentation discipline for data acquisition components (HRN scraper, NYRA scraper, Equibase chart parser, plus any future sources).

Each data source has a dedicated bible section (in the Data Pipeline Bible per § 3.2's working hypothesis) documenting:

- **What the source provides:** specific tables/fields populated
- **Current reliability state:** verified empirically, not assumed. Includes recent failure history with dates.
- **Failure manifestation:** how silent failure presents (DB row symptoms, log signatures, downstream model degradation patterns)
- **Current acquisition mode:** autonomous / monitored / scheduled-manual / paid-replacement (per § 3.5 disposition vocabulary, aligned)
- **Honest disposition:** what this source's acquisition mode SHOULD be, with rationale

The bible documents reality. Phase 4 makes the keep/refactor/replace/kill calls on dispositions that are dishonest (e.g., a source classified "autonomous" that actually has a 3-day silent failure history, like HRN at the time of Bug #28 discovery).

### 7.10 Commit-Before-Deploy Discipline

**Hard rule from Phase 1 onward.** Every deploy is gated on:

1. `git status` clean
2. `git log -1` shows a commit corresponding to the deployed state
3. Bible diff has been reviewed at commit time

**Mechanics:**
- Bible diff review happens at commit time, not deploy time
- Commits SHOULD represent deploy-ready iteration states. "Deploy-ready" means: the operator believes the current state is what the next deploy should ship; not "no in-progress work" (every iterative session has in-progress work). Intermediate WIP commits are allowed; the gating is on deploys, not commits. Cadence (commits per session, frequency, size) is a Phase 5 working-agreements decision; Phase 0 specifies the gating discipline, not the cadence.
- All Phase 5 execution operates under this rule
- The pre-Phase-1 baseline commit (§ 3.1.1) establishes the starting point

**Existing uncommitted production code at Phase 0 exit is handled by § 3.1.1's baseline commit.** Drift surfaced after the baseline (during Phase 1 audit) becomes a triage queue entry; remediation is committing the deployed source as a remediation commit before Phase 5 work touches that Lambda.

**Why this is non-negotiable:**
The maintenance protocol (§ 7.1–7.2) requires "every code change updates the bible in the same commit as the code change." If commits don't exist, the bible cannot be tied to code changes, and discipline degrades. The rule is structural, not aspirational.

**Emergency hotfix exception (per Tony's locked language):**

In cases where production is broken and waiting for commit + bible review would cause user-facing harm or data loss, deploy may proceed before commit, subject to:

- Deploy flagged as emergency in deploy command (e.g., `EMERGENCY=true ./deploy.sh`); audit trail records the exception
- Commit within 4 hours of deploy
- Bible entry within 24 hours of deploy
- Triage queue entry created at deploy time recording: what broke, what was deployed, why bible-first discipline was bypassed, what the retroactive update plan is
- Two emergency deploys within 7 days triggers architectural review of why this keeps happening

**Rationale:** Default-deny is fantasy. Discipline isn't preventing emergency deploys; it's making sure they don't accumulate as silent debt. The exception is a forensic record, not a quiet bypass.

### 7.11 Commit Message Convention

Every commit that touches the bible includes a reference of the form:

```
bible: <doc_name>:<section> - <short description>

[commit message body]
```

Examples:

```
bible: data_pipeline_bible:7.9-hrn-scraper - HRN Bug #28 fix + scraper hardening
```

```
bible: ml_layer_architecture_bible:6.2-calibration - Re-enable gonzo calibration sidecar after Bug #24 resolution
```

Multiple bible references allowed if the change spans documents:

```
bible: ml_layer_architecture_bible:6.2-calibration; feature_provenance_bible:4.1-train-inference-parity - Phase A3 calibration + FE parity
```

Commits that don't touch the bible omit the prefix entirely (no `[no-bible]` tag — silence is the indicator).

Commits that touch ONLY the bible (documentation cleanup, reformat) use:

```
bible: <doc>:<section> [docs] - <short description>
```

**End-to-end pattern (bug fix + bible W.N entry):** when a commit fixes a bug AND adds the corresponding "What Was Fixed" entry to the bible, the commit message references the new W.N entry by section identifier:

```
bible: data_pipeline_bible:18.W.7 - Bug #28 column-shift fix; add W.7 entry

Fix HRN scraper off-by-one column indexing (parse_payout(1/2/3) → parse_payout(2/3/4))
after HRN added an icon column. Backfill of affected results rows scheduled separately.
Adds data_pipeline_bible.md § 18.W.7 (What Was Fixed) entry documenting the fix
and the regression-test discipline that should prevent recurrence.
```

The W.N section identifier in the commit message lets `git log --grep="W.7"` retrieve every commit related to that immune-memory entry.

### 7.12 Migration Discipline

**Format (per Tony's grandfathering decision):**

- Migrations 001–011 keep their existing `NNN_short_description.sql` format. No renaming. No Phase 0 prerequisite to update.
- Migration 012 onward uses `NNN_YYYYMMDD_short_description.sql` format. The date in the filename is the date the migration was authored.
- Bible entry for migration 012 documents the cutover and rationale.
- Migration runner is unaffected — `backend/database/migrations/migrate.py` tracks applied migrations by filename in the `schema_migrations` table (verified). Both formats coexist as filenames; the runner sees both as opaque strings.

**The duplicate-005 case:** existing duplicate (`005_backfill_pace_delta.sql` and `005_three_prediction_tables.sql`) is an inherited problem. Phase 1 audit documents it; remediation lives in `PHASE_5_BACKLOG.md`. The forward rule (no new duplicates) applies to Phase 5 onward. No Phase 0 action.

If unified format desired in future, that's optional Phase 5+ cleanup, not Phase 0 work.

**Bible update required:** every migration corresponds to a bible entry documenting:
- What schema changed (tables/columns/indices/constraints affected)
- What code paths depend on the new state (which repos, services, Lambdas)
- What the rollback path is (see "Rollback format" below)

**Rollback format (specified):**
- Rollback SQL lives in the **same migration file**, after the up SQL, in a clearly-delimited block.
- The migration runner does NOT auto-execute the down block. Rollback is operator-driven.
- The bible entry references the migration file; it does not duplicate the rollback SQL.

**Illustrative full migration example** (this is a *hypothetical* migration — 012 does not yet exist; the shape is what new migrations should follow from 012 onward):

```sql
-- 012_20260601_add_calibration_metadata_column.sql
--
-- Up: add column to model_versions tracking which calibration sidecar
-- was fitted alongside the model. Required for Phase 5.X.Y re-enable
-- of calibration after Bug #15 + Bug #24 chain resolution.

ALTER TABLE model_versions
    ADD COLUMN calibration_sidecar_s3_key VARCHAR(512) NULL;

CREATE INDEX idx_model_versions_calibration_sidecar
    ON model_versions(calibration_sidecar_s3_key)
    WHERE calibration_sidecar_s3_key IS NOT NULL;

-- ============================================
-- DOWN MIGRATION (manual; not auto-run)
-- ============================================
-- Reverses up by dropping the index and the column. Safe to run while
-- the column is unused; data loss if rows have populated values.
--
-- DROP INDEX IF EXISTS idx_model_versions_calibration_sidecar;
-- ALTER TABLE model_versions DROP COLUMN IF EXISTS calibration_sidecar_s3_key;
```

For non-reversible migrations, the down block reads:

```sql
-- ============================================
-- DOWN MIGRATION
-- ============================================
-- NON-REVERSIBLE because: <reason — e.g., "data backfilled from external
-- source that is no longer available; column drop would lose the only copy">
-- Recovery procedure if rollback needed:
-- 1. <step>
-- 2. <step>
```

**Migration testing:** non-production database first. **"Non-production" definition:** local Postgres instance matching production engine version (PostgreSQL 16.6) OR a dedicated dev RDS PostgreSQL instance (when one exists; one does NOT currently exist for EE). Until a dev RDS instance exists, migrations are tested against local Postgres only. Production engine is standalone RDS PostgreSQL 16.6 (`equine-db` instance, not Aurora — corrected v9 per Architecture Overview v1 verification log Claim A.8 REFUTATION + Claim V1-11 substrate). Phase 5 should add a dev RDS instance as a triage-queue item; until then, the rule has reduced enforcement, and Tony should treat untested-against-RDS as elevated risk.

**Migration commit discipline:** schema migration file + bible entry + code that uses the schema all in same commit (or same PR when PR workflow is adopted; see § 7.13).

### 7.13 Enforcement mechanics

The discipline only works if it is enforced. Three layers:

**Layer 1: Pre-deploy checklist (Tony's responsibility, immediate-term):**

For every deploy, Tony confirms:
- [ ] `git status` clean
- [ ] `git log -1` shows current state
- [ ] If any bible-touched files in this commit: bible diff reviewed
- [ ] If migration in this commit: migration tested against non-production DB per § 7.12
- [ ] Commit message follows § 7.11 convention

**Layer 1 under emergency hotfix exception (per § 7.10):** when the emergency hotfix carve-out applies, the following items waive at deploy time and apply retroactively at the within-4-hours commit:

- `[ ] git status clean` — **waived at deploy** (emergency state precedes commit). Applies retroactively at commit.
- `[ ] git log -1 shows current state` — **waived at deploy** (commit happens after deploy by definition of the carve-out). Applies retroactively at commit.
- `[ ] If any bible-touched files in this commit: bible diff reviewed` — **waived at deploy**; applies when the within-4-hours commit and within-24-hours bible entry land.
- `[ ] If migration in this commit: migration tested against non-production DB per § 7.12` — **NOT waived**. Untested migrations against production are forbidden under emergency or any other condition. If an emergency requires a migration, the operator either has a pre-tested migration ready or holds the deploy until one exists.
- `[ ] Commit message follows § 7.11 convention` — **NOT waived**; applies at the within-4-hours commit. The triage queue entry created at deploy time per § 7.10 also follows the convention.

The triage queue entry created at emergency-deploy time records which Layer 1 items waived and the retroactive deadlines for each.

**Layer 1 physical form (current state and deferred formalization):**

Layer 1 is currently operator mental ritual — Tony confirms each checklist item before each deploy without a maintained checklist file. This is honest about the current operating state.

Whether to formalize Layer 1 as a written checklist file (e.g., `.deploy-checklist.md` at repo root, with the five checkboxes maintained explicitly per deploy) OR to graduate enforcement to Layer 2 (PR workflow with a template) is a Phase 5 working-agreements decision, not specified here. Phase 5 may decide the mental-ritual form is sufficient given operator practice; Phase 5 may decide formalization is needed; Phase 5 may decide PR workflow adoption supersedes both. Until Phase 5 makes that call, Layer 1 is mental ritual.

The risk of unspecified-form Layer 1 — that "Tony confirms" reduces to "Tony remembers" — is acknowledged. The mitigation is operator discipline plus the audit-cycle drift detection deferred to Phase 5 working agreements per § 7.13's enforcement-failure recovery deferral. Both deferrals are intentional and aligned: cadence and form both belong to Phase 5's design.

**Layer 2: PR template (when PR workflow is adopted):**

PR template includes:
- Checkbox: "bible updated for changed sections"
- Checkbox: "migration tested in non-production DB" (if applicable)
- Checkbox: "What Was Fixed entry added" (if fixing a bug)
- Checkbox: "Forbidden Pattern added" (if introducing new architectural rule)

PR workflow adoption is **out of scope for Phase 0**. Phase 5 may revisit. Until then, Layer 2 is dormant; Layer 1 carries enforcement.

**Layer 3: Bible diff review at commit time (clarified):**

The "Tony reviews the bible diff" rule applies to **bible-touching commits only**, not every commit. Bible-touching is determined by the commit message prefix per § 7.11's silence convention: commits whose message starts with `bible:` get diff-review; commits without the prefix do not.

**Drift detection and recovery (per Tony's locked deferral):**

> Drift between deployed code and bible state is detected by operator judgment or by focused audits the operator chooses to run. Audit cadence is a Phase 5 working-agreement decision, not specified here. When Phase 5 working agreements are designed, they will define cadence; until then, operator catches drift through normal use of the codebase and any audits called.

Phase 0 documents the disciplines that survive into Phase 5; Phase 5 designs the operating cadences that govern Phase 5 sessions. This subsection's deferral is intentional, not a gap.

### 7.14 .gitignore baseline (Phase 0 prerequisite)

The current `.gitignore` (verified at audit time) already excludes the known deploy artifacts:

```
# Deployment artifacts (machine-specific)
.frontend-bucket
.cf-distribution-id
cdk-outputs.json
frontend/.env.production
```

(v2 audit Q2.2 incorrectly claimed these were not gitignored; verification shows they were already covered. This is documented in `_audits/META_PLAN_v3_verification.md` Claim 11. Tony's Q4 originally said "add as Phase 0 prerequisite"; v3 reframed as "audit deploy scripts for any uncovered artifacts" once verification revealed the assumed gap was actually closed; Tony ratified the reframing in the v4 cycle.)

**Phase 0 prerequisite — gitignore audit sweep:**

QB performs a quick (~15-minute) audit pass comparing all deploy script artifact-writes (verified locations include `scripts/deploy-backend.sh:229,243,262`) against `.gitignore`. Any gaps are added in one sweep. Findings are documented at:

`/docs/bible/_meta/_audits/gitignore_baseline_audit.md`

This file establishes a clean commit-hygiene baseline before Phase 1 starts. Phase 0 does not lock until this audit file exists.

**Going-forward rule:** any new deploy script that writes a machine-specific artifact must update `.gitignore` in the same commit. This is repository-hygiene discipline parallel to (not a sub-rule of) § 7.1's bible-update discipline; both share the principle "every change is captured in the commit that produces it."

---

## 8. Working Agreements

### 8.1 Observation-only during Phases 0–4

No code changes. No "I'll just fix this real quick." Findings go to the triage queue (§ 7.8). Phase 5 is when fixes happen.

This is non-negotiable because the bible's job in Phases 1–2 is to document the system as it exists. If audit work concurrently changes the system, the bible is documenting a moving target.

**The single exception** — if audit-CC discovers any of:
- An unbounded ongoing loss (not a known stable failure mode) — e.g., a payment processor stuck in a retry loop
- A loss event that compounds (data integrity degradation that worsens over time, financial settlement drift)
- A security exposure with active attacker risk
- A bug actively dropping data that cannot be recovered later (e.g., a webhook handler dropping events permanently)

QB surfaces immediately to Tony, who decides whether to break observation-only for that specific issue. Default is still observation-only.

**"Stable known failure mode" criterion:** a bug qualifies as "stable known" only when (a) the failure mode is bounded — no compounding, no escalation; (b) the loss is recoverable through backfill or re-run; (c) the operator has explicitly chosen not to interrupt observation-only to fix it. The mere fact that the bug has been observed does NOT make it "stable known" — that's post-hoc reasoning.

**Bug #28 case (provisional stable-known classification):** HRN scraper drops payout fields silently. Failure mode is bounded — column shift produces NULLs for `win_payout` and `daily_double_payout`; place, show, and exacta payouts still populate per the operator memory file's symptom statement (verbatim: "Place, show, and exacta payouts still populate"). The memory file additionally flags DD pool extraction at `hrn_scraper.py:814` as "likely has the same root cause" — a distinct code path from the `daily_double_payout` field already accounted for in the result-dict, and may surface as additional NULL fields once Phase 1 audits the pool-table loop. Loss is recoverable in principle if backfill is feasible — the assumption being that fetch_results re-run can access historical HRN pages and re-extract the missing payouts after the column-shift fix. **This assumption is unverified at v6 lock time; Phase 1 Data Pipeline Bible audit verifies it, including DD pool extraction status.** Until verification, Bug #28 is classified as **provisionally stable known**: provisional because the bounded-and-recoverable criterion (b) of the § 8.1 stable-known definition rests on the unverified backfill assumption AND the unverified DD-pool-extraction status. Tony has chosen to defer fix to Phase 5; Bug #28 goes to `PHASE_5_BACKLOG.md` as the first entry; the bible documents it as Currently Open under the provisional classification.

**Re-classification trigger:** if Phase 1 Data Pipeline Bible audit verifies backfill is feasible (and DD pool extraction is bounded), the provisional qualifier is dropped at audit-lock time. If the audit verifies backfill is NOT feasible (or DD pool extraction reveals additional uncovered loss), Bug #28 re-classifies as either (a) "known but not stable" — meaning § 8.1's exception logic could trigger if the operator chooses to escalate, or (b) "stable known with permanent loss" — meaning the affected window's data is unrecoverable and the bible documents the data gap as a permanent feature of the historical record. Phase 1 audit's classification call is the lock-trigger.

**Exception interaction with § 7.10:** if the § 8.1 exception fires during Phase 5 (during an unbounded-loss event), the § 7.10 commit-before-deploy hard rule still applies — but the emergency hotfix carve-out in § 7.10 covers this case. The two exceptions are aligned.

### 8.2 Triage queue discipline

Every finding from Phase 1+ audits goes to `PHASE_5_BACKLOG.md` in TRIAGE_QUEUE_SPEC.md format. Severity-tagged. Dependency-tracked. Phase-scheduled.

`PHASE_5_BACKLOG.md` is **created at Phase 0 exit**, with Bug #28 as the first entry (resolves v2 § 10.5 deferral). Creation depends on TRIAGE_QUEUE_SPEC.md being locked first (the spec defines the entry format). § 4.3 documents the dependency.

Findings are not lost. Findings are not silently fixed. Findings accumulate until Phase 5 schedules them.

### 8.3 Decision deferral

Architectural decisions surfaced during audit are deferred to Tony. QB's job is to surface them clearly with proposed resolutions and tradeoffs; Tony decides. QB does not pick architectural directions on Tony's behalf.

Routine iteration (deliverable doesn't pass audit, needs re-spec, needs revision) stays inside QB's loop.

### 8.4 Paste-ready CC prompts

QB authors every CC prompt as a self-contained block, paste-ready into a fresh CC session. No "adapt as needed" handoffs. Each prompt includes:
- Target questions
- Format expectations
- Depth bar
- Source-priority order (per § 4.5)
- Output location
- For Tier 3 drafting: explicit verification discipline (no fabrication; produce verification log; verification log entries must be precise about what was counted per § 6.5; methodology-interpolation rule per § 6.1 operative)
- For audit prompts: the six adversarial questions (§ 6.2) plus document-type-specific verification mandate

A working example appears in Appendix A.6.

### 8.5 Source priority — resolution rules

Codified in § 4.5 (seven-tier hierarchy). Resolution rules:

- **AWS vs DB state:** AWS wins for "current state"; DB wins for "historical record." Document both when they tell a different story (e.g., INACTIVE Lambda + production rows that imply it ran). § 4.5's worked example for `equine-results` shows the canonical pattern.
- **AWS vs API endpoint:** API endpoint wins for runtime data state ONLY when the serving Lambda is Active per AWS state. When the serving Lambda is INACTIVE, behavior is route-specific — some routes may fail with 5xx; others may serve stale cached state via API Gateway integration responses; others may have routing-level fallbacks. The behavior of any specific route under INACTIVE-Lambda conditions is to be documented per route in the Phase 1 API & Frontend Bible, not asserted globally here. The Phase 1 audit's job includes mapping each of the 41 routes to its integration target and recording observed INACTIVE-target behavior where applicable.
- **Code vs code (two modules contradict):** identify the authoritative module via import/usage patterns. Document both; queue the unused module for cleanup disposition.
- **Code vs operator memory:** bible documents what the code does (factual) and notes operator's stated rationale separately (intent). Both can coexist.
- **Live state vs dump:** live state always wins. The dump is best-available baseline only. Phase 1 verification is expected to surface dump errors; v3 itself surfaced two (INACTIVE Lambda count, ECS task family count).

### 8.6 No fabrication

CC must never paper over uncertainty. If CC cannot verify something from referenced sources, CC says so explicitly. "I could not access X, so this section is unverified" is acceptable; "X is the case" without verification is not.

For Tier 3 documents, verification is enforced via the companion verification log (§ 6.5). Every concrete claim has an entry. Claims that cannot be verified are dropped or explicitly flagged as unverifiable. Verification log entries follow the precision rule (§ 6.5): counts decomposed, definitions vs uses vs imports distinguished, no compressible aggregations.

This is inherited operator discipline from DD's "zero tolerance for fabricated success reports."

### 8.7 Context window awareness

CC sessions and QB sessions both have context limits. QB warns Tony proactively when context is getting long. Long deliverables (especially Tier 3 Phase 1 bibles) get split across sessions if necessary, with explicit handoff documents.

Tier 3 drafting consumes more CC context than Tier 1 because verification reads files. QB monitors and may ask CC to verify in batches and produce the verification log incrementally.

---

## 9. Anti-Patterns (What NOT to Put in the Bible)

The bible is load-bearing. Putting the wrong things in it dilutes the parts that have to be right.

### 9.1 Aspirational architecture

The bible documents what is, not what should be. Aspirations belong in Phase 4 gap-analysis output, not the bible. If a section starts with "the system should..." or "in the future we will...", it does not belong.

### 9.2 Tutorials and explanations

The bible is a reference, not a learning resource. It does not explain why XGBoost is a gradient-boosted decision tree. It does not explain RDS PostgreSQL. It assumes a reader who already knows the technology and needs to know what THIS system does with it.

### 9.3 Marketing language

"Sophisticated ML stack," "institutional-grade pipeline," "cutting-edge architecture." None of this. The bible is dry. The bible is precise.

**FORBIDDEN:** "EE uses an advanced multi-layer ensemble approach with proprietary calibration."

**CORRECT:** "EE's LS stack is 7 layers: WR (binary win XGBoost), ranker (LambdaMART rank:pairwise), value overlay (arithmetic, not trained), longshot RandomForest classifier, trajectory LSTM (PyTorch, hidden_size=32, 2 layers, dropout 0.3), Bayesian angle scorer (Beta-Binomial posteriors), ensemble (logistic regression meta-learner)."

The boundary: precise terminology (named layers, specific algorithms, exact hyperparameters) is correct. Marketing-adjacent abstraction ("advanced," "proprietary," "approach") is forbidden.

### 9.4 Backlog items

Triage queue work goes to `PHASE_5_BACKLOG.md`. The bible references items by phase number. It does not contain the working backlog.

### 9.5 Session logs

Session logs are not bible material.

### 9.6 Code snippets longer than the rule they illustrate

FORBIDDEN/CORRECT pairs are 3–8 lines per side, mirroring DD's pattern. If an example needs 50 lines to make its point, the rule is too vague — sharpen the rule.

### 9.7 Apologetic or hedging language

"This might be wrong, but..." "I think the system does..." "Probably the case that..." None of this. Either the rule is verified and gets a dated lock point, or it goes to the audit queue for verification. The bible never hedges; it states the rule and dates the lock.

### 9.8 Anything without a dated lock point

Every rule, pattern, decision has a lock date. No exceptions.

### 9.9 Cross-referenced backlog items without phase numbers

If the bible says "tracked in `PHASE_5_BACKLOG.md`," it cites the specific phase number. "Phase 5.7.2" not "tracked in the queue."

### 9.10 The current bug list in narrative form

Open bugs go to the triage queue. The bible's "Currently Open" section is a numbered list with one-line descriptions and `PHASE_5_BACKLOG.md` pointers. Narrative explanations belong in the triage queue entries.

### 9.11 EE-specific anti-pattern: Pretending feature engineering has one source of truth

EE has two parallel feature engineering implementations: `model/shared/data_loader.py` (training) and `backend/services/feature_engineering_service.py` (inference). Only the 14 Gonzo Sauce features are factored to a single shared module (`model/shared/gonzo_features.py` — verified: docstring explicitly enumerates Speed (4) + Trajectory (7) + Class (3) = 14 features and states the file is "the single source of truth"). The bible MUST document this duplication as the structural reality, not pretend a single source exists.

**FORBIDDEN:** "Feature engineering is implemented in `model/shared/data_loader.py`."

**CORRECT:** "Feature engineering is implemented in two locations: `model/shared/data_loader.py` (training) and `backend/services/feature_engineering_service.py` (inference). The 14 Gonzo Sauce features are factored to `model/shared/gonzo_features.py`, the single shared module imported by both. The remaining base features have parallel implementations kept in sync by manual cross-reference review. See [Forbidden Pattern X.Y] for the discipline that prevents drift."

### 9.12 EE-specific anti-pattern: Pretending calibration is applied at inference

The code at `backend/services/wr_inference_service.py:616-626` (verified — the comment block at lines 616–625 explicitly reads "All styles (including gonzo_sauce) bypass calibration at inference tonight," followed at line 626 by `handicapping_probs = ranker_probs.copy()`) explicitly bypasses calibration for ALL styles. Calibration sidecars exist in S3 for `gonzo_sauce` but are not loaded. The bible MUST document the bypass as the current state, with the chain Bug #15 → Bug #24 as the rationale.

**FORBIDDEN:** "Inference applies isotonic calibration via the fitted sidecar in S3."

**CORRECT:** "Inference currently bypasses calibration for ALL styles, including gonzo_sauce. The bypass was introduced as a workaround for Bug #15 (train/inference FE drift) → Bug #24 (calibrated 0-PP horse override misranks). Calibration sidecars exist in S3 for gonzo_sauce ranker output but are not loaded. Re-enabling calibration is tracked as Phase 5.X.Y."

### 9.13 EE-specific anti-pattern: Pretending the model registry has one active row per type

The model registry (`model_versions` table) has 88 entries decomposed as 45 active + 43 inactive (verified live via dashboard endpoint). The 45 active rows span (model_type, style, specialist) combinations. Code that calls `get_active_model_by_type(model_type)` returns an arbitrary row from the active set when multiple rows match — the function takes only `model_type`, queries `WHERE is_active = true AND model_type = %s LIMIT 1`, and returns whatever Postgres orders first.

**FORBIDDEN documenting pattern:** "Active model is selected via `get_active_model_by_type(model_type)`."

This treats the call as a complete API. It is not — it returns *one* of 45 active rows non-deterministically when called for any of the three model types that have multiple style/specialist combinations. The documenter who writes this either does not know about the multi-active-row reality or thinks it doesn't matter; the bible's job is to prevent both.

**CORRECT documenting pattern:** "Active model is currently selected via `get_active_model_by_type(model_type)` at `backend/repositories/model_version_repository.py:100`. The function takes only `model_type`, queries `WHERE is_active = true AND model_type = %s LIMIT 1`, and returns the first matching row. **Multi-active-row reality:** 45 of 88 rows in `model_versions` are `is_active=TRUE` simultaneously, spanning (model_type × style × specialist) combinations. When multiple rows match `model_type`, LIMIT 1 picks an arbitrary row from the active set; behavior is non-deterministic across calls. **A style-aware variant does not yet exist; introducing one is Phase 5.X.Y.**"

The CORRECT pattern names three pieces: the function, the multi-active-row reality, and the missing style-aware variant as a tracked Phase 5 item. Documentation that names only the function and the multi-active-row reality (omitting the style-aware-variant gap) is descriptive but not actionable — a reader knows the current state but not the path forward. Documentation that names only the function (omitting both the reality and the gap) is the FORBIDDEN form. The three-piece pattern surfaces all three — current state, current limitation, planned resolution — so that future documentation maintenance preserves the path forward as the codebase evolves.

(v2 used a fictional `get_active_model_by_type_and_style` function in this anti-pattern's CORRECT example. v3 verification confirmed the function does not exist; v3 rewrote honestly. v4 sharpened the FORBIDDEN/CORRECT contrast but introduced a binary "Removing any one converts to FORBIDDEN" test — CC-interpolated methodology Tony hadn't ratified. v5 replaced the binary test with descriptive prose that explains the consequences of incomplete documentation rather than prescribing a binary pass/fail.)

---

## 10. Open Questions

Surfaced for resolution during Phase 0 iteration. Not blocking META_PLAN lock unless audit returns one as critical.

### 10.1 Phase 1 document count and split

Working hypothesis (§ 3.2) is 5–7 documents with the floor on ML-specific documents (≥ 3) locked in § 3.2.1. BIBLE_STRUCTURE_SPEC.md decides final names, internal structure, and additional documents. The decision is made empirically.

### 10.2 Top-level INDEX file

DD has one bible file. EE will have multiple. Question: does an explicit `BIBLE_INDEX.md` or `ARCHITECTURE_BIBLE.md` index file exist linking the parts, or does the Architecture Overview document (per § 3.2's working hypothesis #1) serve that purpose? Answered in BIBLE_STRUCTURE_SPEC.md.

### 10.3 Repo-root vs `/docs/bible/`

DD's bible lives at repo root (`ARCHITECTURE_BIBLE.md`). EE's is planned at `/docs/bible/`. Whether to put a top-level pointer at EE repo root is a navigability question. Answered in BIBLE_STRUCTURE_SPEC.md.

### 10.4 Frontend bible split

Frontend is small (9 pages, 13 components, single axios client, no state library). It might warrant its own bible document, or be a section of the API & Frontend bible, or be a chapter of the Architecture Overview. Answered in BIBLE_STRUCTURE_SPEC.md.

### 10.5 (resolved) — Bug #28 destination

Resolved in v3: `PHASE_5_BACKLOG.md` is created at Phase 0 exit with Bug #28 as the first entry (per § 8.2). v5 refined the classification to "provisionally stable known" pending Phase 1 backfill verification (§ 8.1). v6 expanded the verification scope to include DD pool extraction status. Re-classification trigger documented inline.

---

## 11. Lock Status

**Document status:** LOCKED v9 (post-Phase-0-closure surgical correction)
**Audit-CC pass:** v8 audit closed 2026-05-05 (per `_audits/META_PLAN_v8_verification.md`); v9 surgical-cosmetic patch skips re-audit per BIBLE_STRUCTURE_SPEC v5/v6 surgical-cosmetic pattern
**Verification log:** `_audits/META_PLAN_v9_verification.md` — Aurora claim REFUTATION verified per Architecture Overview v1 verification log Claim A.8 + V1-11; metadata hygiene drift corrected; v6→v7→v8→v9 trajectory documented
**Tony review:** complete (Path C ratified 2026-05-05)
**Locked:** 2026-05-05

**Phase 0 exit prerequisites (per § 3.1):**
- [ ] All 5 Phase 0 documents pass adversarial audit (Tony's threshold: < 5 MATERIAL findings AND zero fabricated-content findings AND zero methodology-interpolation findings)
- [ ] Operating-model convergence test passes (§ 5.4)
- [ ] EE production code committed to baseline (§ 3.1.1)
- [ ] `.gitignore` baseline audit performed; findings documented at `_audits/gitignore_baseline_audit.md` (§ 7.14)
- [ ] `PHASE_5_BACKLOG.md` created with Bug #28 as first entry (§ 8.2)

**Next action:** QB writes paste-ready audit-CC prompt for v6. Tony runs audit. QB synthesizes findings.

---

## 12. Changelog

This section carries the changelog across multiple cycles. In v9's organization, § 12.1 holds the v8→v9 changelog, § 12.2 holds the v7→v8 changelog, § 12.3 holds the v6→v7 changelog, and § 12.4 holds the v5→v6 changelog (preserved verbatim from v6's § 12). Earlier-than-v5→v6 changelog content lives in git history at the corresponding version commits.

### 12.1 v8 → v9 Changelog

**Surgical correction (Phase 1 verification surfaced Phase 0 substrate error):**

- **Aurora cluster ARN claim REFUTED — replaced with standalone RDS PostgreSQL substrate.** META_PLAN v8 inherited from earlier cycles' verification logs (via wholesale v6→v7→v8 inheritance) the claim that EE uses an Aurora Serverless cluster with ARN `arn:aws:rds:us-east-1:584812014683:cluster:equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`. Architecture Overview v1 verification log Claim A.8 ran `aws rds describe-db-clusters --db-cluster-identifier equinedatabasestack-equinedatabase648a3917-y8mww81ea82f` 2026-05-05; live AWS returned `DBClusterNotFoundFault`. Architecture Overview v1 verification log Claim V1-11 ran `aws rds describe-db-instances --db-instance-identifier equine-db` 2026-05-05; live AWS returned standalone PostgreSQL 16.6 instance `equine-db` (`DBClusterIdentifier=None`). Source of the inherited error traced to cross-project contamination — `EE_CURRENT_STATE_DUMP.md` (Tier 6) likely incorporated the Aurora cluster ARN from the adjacent `fantasy-baseball-serverless` Aurora cluster (a different project). Per § 4.5 source-priority hierarchy, Tier 1 (live AWS state) governs over Tier 6 (dump-derived claim). v9 corrects three body locations: § 2.3 in-scope artifact bullet (`Aurora Serverless cluster (one)` → `RDS PostgreSQL instance equine-db (one; standalone instance ...)`), § 7.12 Migration testing paragraph (`dev Aurora cluster` / `Aurora-specific behaviors` references replaced with `dev RDS PostgreSQL instance` / standalone RDS framing), § 9.2 illustrative example (`It does not explain Aurora Serverless.` → `It does not explain RDS PostgreSQL.`).

**Metadata hygiene drift corrected (drift origin: Phase 0 closure metadata never propagated to disk in v7 + v8 cycles):**

- **Front matter Status field** updated from `DRAFT v8 (pre-audit)` to `LOCKED v9 (2026-05-05)`.
- **Front matter Locked field** updated from `[pending audit + Tony review + iteration cycles]` to `2026-05-05`.
- **§ 11 Lock Status block 5 sub-fields** updated to reflect v9 metadata + v6→v7→v8→v9 trajectory + Phase 0 closure context. § 11's Phase 0 exit prerequisites checklist (immediately following the 5 sub-fields) preserved unchanged — those prerequisites are Phase 0 exit semantics, not v9 metadata hygiene.

**Methodology lessons banked (for future AUDIT_METHODOLOGY cycle, when warranted):**

- **Lesson 1 — Tier 6 verification mandate includes cross-project contamination check, not just freshness check.** The Aurora ARN inherited from `EE_CURRENT_STATE_DUMP.md` was not stale EE state; it was content from a different project (`fantasy-baseball-serverless`). Verification protocols against Tier 6 must check for cross-project bleed, not only stale-EE-state.
- **Lesson 2 — Phase 1 verification surfaces Phase 0 substrate errors; surgical correction to Phase 0 documents is the expected response, not Phase 0 re-lock.** The v9 cycle is the canonical pattern: Phase 1 audit-CC catches an inherited claim that doesn't hold against live state; QB triages as substrate error; Phase 0 document receives surgical patch (this cycle) rather than full re-audit.
- **Lessons 3–6 — QB drafting and synthesis discipline (cluster).** Four QB-side errors surfaced in the Architecture Overview v1 cycle (deliverable numbering arithmetic, broken cross-reference to META_PLAN § 7.10, FRAMEWORK_GAP reframing assertion, upstream-correction synthesis error) all trace to the same root failure: QB asserted from synthesis when substrate verification was required. Cluster as `QB drafting and synthesis discipline` for AUDIT_METHODOLOGY codification: (3) drafting specs cite primary verification log claim IDs, not paraphrased restatements; (4) QB triage of FRAMEWORK_GAP markers requires substrate verification before ratification; (5) EventBridge documentation cites `list-targets-by-rule` output per rule, not `list-rules` output alone; (6) QB synthesis of audit findings into upstream-correction scope requires substrate verification of the upstream claim, not propagation of audit-CC's downstream finding.

**Verification log v9 deltas:**

- New entry V9-1 (9 sub-entries, A through I): each Target's substrate citation, char-exact replacement verification, and bash-grep confirmation of removal/insertion. Decomposition: 8 patch targets (A through H) + 1 structural sub-section renumbering (I) = 9 sub-entries total.
- All other entries inherited from v8 verification log; not re-verified during v9 (this cycle covers only the changed content).

**Retained from v8 unchanged:**

- All v7-added § 7.3 placeholder-resolution sub-rule + rationale paragraph.
- All v7-added Appendix A scope-clarification paragraph.
- All v8-added § 12 intro paragraph re-instantiated for v9 organization (Target H).
- All v8-added § 12.1 (renumbered to v9 § 12.2) v7→v8 changelog content.
- All v7 § 12.2 (renumbered to v9 § 12.3) v6→v7 changelog content.
- All v6 § 12 (renumbered to v9 § 12.4) v5→v6 changelog content.
- All other sections (§ 1, § 2.1, § 2.2, § 2.3 except the corrected Aurora bullet, § 2.4, § 3, § 4, § 5, § 6, § 7.1, § 7.2, § 7.3, § 7.4–§ 7.11, § 7.12 except the corrected Migration testing paragraph, § 7.13, § 7.14, § 8, § 9.1, § 9.2 except the corrected illustrative-example sentence, § 9.3–§ 9.13, § 10, § 11 except the corrected 5 sub-fields, Appendix A.1–A.7) retained verbatim. v9 is a surgical-cosmetic patch, not a substantive revision.

**Path forward note:**

v9 closes the Phase 0 substrate correction triggered by Architecture Overview v1 verification. After v9 lock, the next QB deliverable is Architecture Overview v2 drafting spec, which inherits corrected META_PLAN v9 substrate + applies the 8 MATERIAL corrections + 10 MINOR fixes from the Architecture Overview v1 audit + applies the 6 active methodology lessons (lessons 1–2 already operative; lessons 3–6 now banked for AUDIT_METHODOLOGY codification but operative as discipline starting v2 spec).

### 12.2 v7 → v8 Changelog

**MATERIAL fix (v7 audit finding):**

- **F-F — § 12.1 second methodology-lesson paragraph deleted.** The v7 audit (`_audits/META_PLAN_v7_audit.md`) flagged a CC-prescribed methodology-pattern generalization in v7 § 12.1's "Methodology lesson recorded (v6 → v7)" subsection. The flagged paragraph asserted that v7's surgical-patch shape is a pattern "robust across cycles" and that "precise audit findings produce precise revisions" — a generalization claim about methodology cycle shape that Tony had not ratified. Per v6 § 6.1's catch-all clause ("or other CC-prescribed methodology constructs that Tony has not explicitly ratified"), audit-CC classified this as MATERIAL methodology-interpolation. Per Tony's bar, methodology-interpolation findings fail the lock regardless of count. Per Tony's locked F-F resolution: the paragraph is deleted entirely (not relabeled). Deletion eliminates the drafter-authored prose surface from re-evaluation in future audits. After deletion, "Methodology lesson recorded (v6 → v7)" contains exactly one paragraph (the spec-authorized lesson about the convergence test surfacing methodology gaps that audit cycles alone cannot).

**MINOR/STYLE fixes (v7 audit findings):**

- **A2 — § 12 intro paragraph tightened to descriptive framing.** v7's intro paragraph contained "Most-recent cycle first; prior cycles preserved verbatim for audit-trail continuity" — readable as forward-looking discipline by future-cycle drafters. Replaced with explicit-descriptive framing naming v8's actual organization (§ 12.1 / § 12.2 / § 12.3). The replacement describes what v8 did without prescribing for future cycles.
- **A3 — "surgical-patch discipline" terminology promotion struck.** v7 § 12.1's "Verification log v7 deltas" subsection's final bullet contained an em-dashed clause defining "surgical-patch discipline" as "only changed content gets new verification entries" — a CC-introduced sub-rule about verification-log behavior in surgical-patch cycles, beyond v6's grandfathered "surgical patch" descriptive vocabulary. Replaced the em-dashed clause with plain-language descriptive framing ("this cycle covers only the changed content"). Removes the terminology promotion without changing the operational meaning.
- **Q3.A2 — normative-"should" softened to descriptive past-tense with v6 § 5.4 cross-reference.** v7 § 12.1's first methodology-lesson paragraph closed with "future Phase 0 cycles should treat the convergence test as load-bearing, not optional" — a normative restatement of v6 § 5.4's existing locked rule. Replaced with "the convergence test is load-bearing per v6 § 5.4, not optional — the v7 cycle treated it as such." References the existing locked rule explicitly; describes v7's actual treatment without prescribing for future cycles.

**MINOR/STYLE findings NOT addressed in v8 (v7 audit flagged STYLE/acceptable; no remediation required):**

- **R3** — G8 placeholder normalization (`YYYY-XX-XX` in convergence_test_audit.md → `YYYY-MM-XX` in v7's revision history). Surfaced in v7 verification log V7-3; defensible because (a) v7's reference is paraphrase-shaped, not a verbatim quote, and (b) the substitution aligns with Tony's locked sub-rule's strict form. STYLE (acceptable).
- **X7** — Forward reference to BIBLE_STRUCTURE_SPEC v4 (which does not yet exist). Acceptable per Path A sequencing (v4 cycle follows v8 lock). STYLE (acceptable).
- **X8** — "v4's MINOR-pass" close paraphrase of v4's revision-history "localized fix pass" framing. Inside the (now-deleted) F-F paragraph in v7; the F-F deletion in v8 incidentally removes this paraphrase too. Closed by F-F deletion as a side-effect.

**Verification log v8 deltas:**

- New entry: F-F paragraph deletion verified (the verbatim paragraph is no longer present in § 12.2; "Methodology lesson recorded (v6 → v7)" subsection now contains exactly one paragraph).
- New entry: A2 § 12 intro paragraph replacement verified (new text matches drafting-spec embedded language; original "Most-recent cycle first" language removed).
- New entry: A3 § 12.2 verification log bullet replacement verified ("surgical-patch discipline" terminology removed; new descriptive language present).
- New entry: Q3.A2 § 12.2 normative-"should" sentence replacement verified ("future Phase 0 cycles should treat" removed; new descriptive sentence with v6 § 5.4 cross-reference present).
- New entry: § 12 sub-section renumbering verified (v7's § 12.1 v6→v7 renumbered to § 12.2; v7's § 12.2 v5→v6 renumbered to § 12.3; new § 12.1 holds v7→v8 changelog).
- All other entries inherited from v7 verification log; not re-verified during v8 (this cycle covers only the changed content).

**Retained from v7 unchanged:**

- All v7-added § 7.3 placeholder-resolution sub-rule + rationale paragraph.
- All v7-added Appendix A scope-clarification paragraph.
- All v7 § 12.2 (renumbered from v7 § 12.1) v6→v7 changelog content beyond the F-F / A3 / Q3.A2 fixes.
- All v7 § 12.3 (renumbered from v7 § 12.2) v5→v6 changelog content (preserved verbatim from v6's § 12).
- All other sections (§ 1, § 2, § 3, § 4, § 5, § 6, § 7.1, § 7.2, § 7.4–§ 7.14, § 8, § 9, § 10, § 11, Appendix A.1–A.7) retained verbatim. v8 is a surgical patch, not a substantive revision.

**Path A sequencing note:**

v8 is the second of two Phase 0 revisions triggered by the convergence test (after v7 closed G8; v8 closes the v7-audit findings F-F + A2 + A3 + Q3.A2). After v8 lock, BIBLE_STRUCTURE_SPEC v4 cycle addresses the remaining 8 methodology gaps (G1, G2, G3, G4, G5, G6, G7, G9) per Path A. Once v8 and v4 lock, the convergence test re-runs on the same Database & Schema Bible spec to validate that all gaps are closed. If gaps re-surface, escalate per § 5.3 "Iteration escalation" rule.

### 12.3 v6 → v7 Changelog

**MATERIAL fix (convergence test audit finding):**

- **G8 — Appendix A placeholder convention scope clarified + § 7.3 sub-rule added.** The operating-model convergence test on the Database & Schema Bible draft (per § 5.3 step 3 of v6) produced two structurally non-equivalent outputs from two CC sessions executing the same Phase 1 spec. Audit-CC enumerated 21 material differences and 9 methodology gaps in `_audits/convergence_test_audit.md`. G8 was the single methodology gap routed to META_PLAN (the remaining 8 gaps — G1, G2, G3, G4, G5, G6, G7, G9 — are routed to BIBLE_STRUCTURE_SPEC v4 per Path A sequencing). G8's symptom: run1 used `fixed 2026-05-XX` for migration 011's `wr_predictions` UNIQUE fix (a real fix whose date is knowable from `git log` as 2026-05-01); run2 used `fixed 2026-05-01`. Both choices were defensible against v6's language, which established the placeholder convention only for Appendix A worked examples and did not specify Phase 1 drafter behavior when writing W.N entries for fixes whose real dates are knowable. v7 closes the divergence with two coupled changes: (a) § 7.3 receives a placeholder-resolution sub-rule mandating `git log` resolution for real fixes with knowable dates; (b) Appendix A's lead paragraph receives a scope-clarification clause that explicitly bounds the placeholder convention to (i) Appendix A's worked-example documents and (ii) forward-looking entries codifying discipline for fixes that haven't happened yet. The two changes are coupled — § 7.3 sets the methodology rule; Appendix A's note explains where the placeholder convention does and does not apply.

**Methodology lesson recorded (v6 → v7):**

The convergence test surfaced a methodology gap that audit cycles alone could not have surfaced. Per-document audit cycles (META_PLAN v6 audit, BIBLE_STRUCTURE_SPEC v3 audit, etc.) are adversarial against a single drafter's content; they do not test for **silent drift between drafters given the same spec**. The convergence test (per § 5.3) is structurally distinct adversarial discipline: it pits two CC sessions' interpretations against each other and routes their differences through audit-CC. G8 surfaced only because two drafters interpreted the placeholder convention differently — neither interpretation would have failed a single-drafter audit. The lesson is that the convergence test is NOT redundant with per-document audits; it is the only mechanism that catches drafter-interpretation drift. v7's surgical patch closes G8 specifically; the broader methodology lesson is that the convergence test is load-bearing per v6 § 5.4, not optional — the v7 cycle treated it as such.

**Verification log v7 deltas:**

- New entry: § 7.3 sub-rule text matches Tony's locked language verbatim.
- New entry: Appendix A lead-paragraph scope clarification preserves the original two claims char-exact while adding the scope-bound clause.
- New entry: § 12.2 (this section) cross-reference to `_audits/convergence_test_audit.md` resolves; G8 finding text matches the audit document.
- All other entries inherited from v6 verification log; not re-verified during v7 (this cycle covers only the changed content).

**Retained from v6 unchanged:**

- All § 7.3 content prior to the new sub-rule (the bulk discipline, the example-structure block, and the rule-supersession paragraph).
- All Appendix A content beyond the lead-paragraph scope-clarification clause (A.1 through A.7 worked examples).
- All other sections (§ 1, § 2, § 3, § 4, § 5, § 6, § 7.1, § 7.2, § 7.4–§ 7.14, § 8, § 9, § 10, § 11) retained verbatim. v7 is a surgical patch, not a substantive revision.

**Path A sequencing note:**

v7 is the first of two Phase 0 revisions triggered by the convergence test. After v7 lock, BIBLE_STRUCTURE_SPEC v4 cycle addresses the remaining 8 methodology gaps (G1, G2, G3, G4, G5, G6, G7, G9) per Path A. Once both revisions land and lock, the convergence test re-runs on the same Database & Schema Bible spec to validate that the gaps are closed. If gaps re-surface, escalate per § 5.3 "Iteration escalation" rule.

### 12.4 v5 → v6 Changelog

**MATERIAL fixes (v5 audit findings):**

- **M-1 — § 5.3 / § 3.1 iteration cap converted to cadence-neutral language per Tony's Option B.** v5's "in 3 consecutive iterations" replaced with "repeatedly on the same dimension." Both occurrences (§ 5.3 iteration escalation and § 3.1 edge case "Convergence test failure") updated together. Specific count threshold deferred to Phase 5 working agreements per the pattern established in § 7.10 (commit cadence) and § 7.13 (audit cadence + Layer 1 physical form). All cadence-shaped decisions defer to Phase 5 uniformly. The "3" was a v3-cycle CC interpolation; v6 closes the loop.
- **M-2 — § 6.1 methodology-interpolation rule scope expanded.** Named patterns now include severity thresholds, iteration caps, percentage criteria, procedural sequencing rules in addition to the original four (binary tests, cadence rules, completeness criteria, scoring rubrics). Catch-all clause added: "or other CC-prescribed methodology constructs that Tony has not explicitly ratified. The named patterns are illustrative, not exhaustive; the catch-all clause covers what is not named." Lessons-learned summary expanded to include the v5 audit's M-1 finding.
- **M-3 — § 3.2.1 "merge" language tightened.** v5's "may NOT merge these three forcing functions into fewer than three documents" replaced with "must specify three separate Phase 1 documents — three distinct .md files at three distinct paths — one per forcing function. A single file with three sections does not satisfy this requirement; the documents must be physically separate files at separate paths so they receive separate audit cycles, separate lock dates, and separate maintenance discipline." The operational reasoning (separate audit cycles + lock dates + maintenance discipline) is the substantive expansion.

**Grandfathering clause added (§ 6.1):**

Per Tony's locked language: pre-existing methodology constructs from earlier cycles' QB drafts are grandfathered; CC-introduced content from prior cycles is subject to the rule. The cycle-N retroactive sweep covers v1 through v(N-1) CC-introduced content; v1 through v(N-1) QB-drafted content is grandfathered. Boundary is computable, not judgment-dependent — provenance (CC-introduced vs QB-drafted) is the discriminator. Dispatches v5 audit's MINOR #11 ("explicitly ratified" boundary undefined). The methodology-interpolation rule landed in cycle 5 (v5); v6's retroactive sweep covers v1-v4 CC-introduced content and treats v1-v4 QB-drafted content as grandfathered.

**MINOR fixes:**

- **MINOR #5 — § 8.1 Bug #28 exacta payout claim re-grounded.** Re-verification of the operator memory file revealed the v5 audit's characterization ("memory file silent on exacta status") was itself wrong. The memory file's symptom statement explicitly reads "Place, show, and exacta payouts still populate." v6 keeps the place/show/exacta still-populate claim AND adds the DD-pool-extraction nuance the memory file does flag ("DD pool extraction at hrn_scraper.py:814 likely has the same root cause" — distinct from `daily_double_payout` already accounted for in the result-dict). Phase 1 Data Pipeline Bible audit verifies the full per-payout-type bounded-loss claim including DD pool extraction status. This is a "Tony's locked decision based on a wrong premise" instance per § 3.1's edge-case enumeration; v6 surfaces and applies the verified-fact reframing.
- **MINOR #6 — § 2.3 ECS Fargate task families fully enumerated.** v5 named only 2 of 5 inline (the dump-missed ones). v6 names all 5: `equine-training`, `equine-training-daily-full`, `equine-training-manual`, `equine-training-pl`, `equine-training-win-prob`. Re-verified live in v6 cycle.

**Other v5 audit MINORs deferred to v7:**

#8 (FRAMEWORK_GAP example uses DD's Player vocab), #9 (rule lacks worked example), #10 (Layer 1 mental ritual lacks worked example), #12 (Bug #28 binary re-classification doesn't accommodate partial), #13 (§ 4.1 row 4 Tier column reads non-tier value), #14 (§ 12 self-referential changelog). These are language polish or deferred-to-AUDIT-METHODOLOGY items; surface for v7 if audit-CC promotes any.

**Methodology lesson recorded (v5 → v6):**

The v5 audit's M-1 finding revealed that methodology rules introduced mid-cycle do not enforce their own retroactive application. The audit must explicitly include retroactive sweep in its scope when a new rule lands. This becomes a discipline that AUDIT_METHODOLOGY.md (Phase 0 doc 3) must codify: when a new methodology rule is introduced in cycle N, the audit-CC spec for cycle N+1 explicitly includes "sweep prior content for instances of this pattern" as a required adversarial check. The rule itself doesn't enforce its own retroactive application — the audit spec does. Banked for AUDIT_METHODOLOGY drafting.

A related lesson: v6 also surfaced an audit-CC characterization error (v5 audit's "memory file silent on exacta" claim contradicted by the file's verbatim text). The "Tony's locked decision based on a wrong premise" edge case in § 3.1 has been invoked twice now (Q4 in v3, MINOR #5 in v6). The pattern is robust: when verification contradicts a Tony-locked decision, surface to QB → Tony rather than silently complying. v6 surfaces; the resulting reframing is faithful to the verified source.

**Verification log v6 deltas:**

- ECS task family entry re-verified live with full enumeration of 5 families.
- Bug #28 / payout-status entry re-verified against operator memory file with explicit verbatim quote of the symptom statement plus the DD-pool-extraction nuance.
- All other entries inherited from v5 with re-verified-2026-05-04 timestamps.

**Retained from v5 unchanged:**

- All § 3.2.1 forcing function content beyond the M-3 "merge" language fix.
- All § 6.5 verification-log-precision rule content including the worked example.
- All § 7.13 Layer 1 physical form content.
- All § 8.1 Bug #28 case study structure beyond the MINOR #5 exacta-claim re-grounding.
- All other sections without v5 audit findings against them.

---

## Appendix A: Worked Examples

These are the bible content patterns Phase 1 will produce. **Every example uses verified EE patterns.** Verification entries are in `_audits/META_PLAN_v6_verification.md`.

Note on placeholders: where a real bible entry would carry a date and a Phase 5 backlog reference, this document uses `Locked 2026-05-XX` and `Phase 5.X.Y` because real Phase 5 numbering does not yet exist (PHASE_5_BACKLOG.md is created at Phase 0 exit). The pattern is real; the specific identifiers are placeholders that get filled when the entry actually lives in a bible document.

**Scope of the placeholder convention (clarified per v7 cycle, 2026-05-05):** the `YYYY-MM-XX` / `Phase 5.X.Y` placeholders in this Appendix apply only to (i) Appendix A's worked-example documents (this Phase 0 methodology document) and (ii) forward-looking entries in Phase 1 bibles that codify discipline for fixes that haven't happened yet — i.e., the rule locks now but the W.N "fixed" date does not exist until the fix lands. The convention does NOT apply to real bug-fix entries in Phase 1 bibles whose dates are knowable from `git log` of the relevant primary source. For those, § 7.3's placeholder-resolution sub-rule applies: Phase 1 drafters MUST resolve the date via `git log` and use the actual date before locking the bible. See § 7.3 for the full sub-rule and rationale.

### A.1: FORBIDDEN/CORRECT — Model Registry Multi-Active-Row Reality

Pattern from `backend/repositories/model_version_repository.py:100` (verified). This is what a Forbidden Pattern entry in the ML Layer Architecture Bible would look like.

```
6.4 Model Registry Multi-Active-Row Reality (locked 2026-05-XX)

The model_versions table has 88 entries decomposed as 45 active + 43 inactive
(verified live via dashboard endpoint). The 45 active rows span (model_type,
style, specialist) combinations. The current selection function at
backend/repositories/model_version_repository.py:100 takes only model_type:

    def get_active_model_by_type(self, model_type: str) -> Optional[ModelVersion]:
        row = self._query_one(
            """SELECT * FROM model_versions
               WHERE is_active = true
               AND model_type = %s
               LIMIT 1""",
            (model_type,)
        )

When multiple rows match (the common case), LIMIT 1 returns an arbitrary row from
the active set. Documentation that names this function without naming the gap is
incomplete.

Rationale: EE's per-style architecture (general / gonzo_sauce / lean53 + 6 specialists)
means each (model_type × style) pair has its own active row. A style-aware variant
of the selection function does not yet exist; introducing one is Phase 5.X.Y.

FORBIDDEN documentation:
"Active model is selected via get_active_model_by_type(model_type)."

CORRECT documentation:
"Active model is currently selected via get_active_model_by_type(model_type) at
model_version_repository.py:100. The function returns the first matching is_active=TRUE
row via LIMIT 1; when multiple rows match (88 = 45 active + 43 inactive currently),
the returned row is arbitrary. A style-aware variant is Phase 5.X.Y."

Cross-reference: see W.4 in ml_layer_architecture_bible.md for the bug history that produced this rule.
```

### A.2: Dated Lock Point — Calibration Bypass Discipline

Pattern from the verified `backend/services/wr_inference_service.py:616-626` calibration bypass (10-line comment block at 616–625 + 1-line bypass operation at 626). Drawn from the Bug #15 → Bug #24 chain.

```
6.2 Inference Calibration Discipline (locked 2026-05-XX)

All WR inference styles currently bypass calibration sidecars at
backend/services/wr_inference_service.py:616-626 (comment block at 616-625,
bypass operation at 626). The bypass was introduced as a workaround for the chain:

  Bug #15: Train/inference FE drift produced miscalibrated probability estimates.
    Train pipeline computed feature X via path P1; inference pipeline computed
    feature X via path P2; values disagreed.

  Bug #24: When isotonic calibration was applied to ranker outputs in
    wr_inference_service.py, legitimate-PP horses' calibrated probabilities
    were clipped to ~0, causing the 1/field_size override for 0-PP horses to
    dominate. Result: 0-PP horses (e.g., "Wonder Dean JPN" in Derby smoke test)
    ranked at #1.

Current state: ALL styles bypass calibration. Calibration sidecars in S3 for
gonzo_sauce ranker output exist but are not loaded.

Rationale: until Phase 5.X.Y addresses the underlying chain, re-enabling
calibration would re-introduce Bug #24's misranking.

FORBIDDEN:
    # WRONG — re-enables calibration in current state
    calibrator = load_calibration_sidecar(style='gonzo_sauce')
    calibrated = calibrator.predict(raw_ranker_scores)

CORRECT:
    # Right — passes through raw scores; bypass remains in effect per § 6.2
    calibrated = raw_ranker_scores  # bypass until Phase 5.X.Y

Resolution path: Phase 5.X.Y addresses Bug #15 root cause (FE single-source
extraction for the remaining base features), then Bug #24 (0-PP override
interaction with calibration). Calibration re-enabled after both fixes deploy
and are validated.
```

### A.3: What Was Fixed Entry — Gonzo FE Single-Source Extraction

Pattern from the verified `model/shared/gonzo_features.py` extraction (per its docstring; verified: docstring at lines 1–28 enumerates the 14 features as Speed (4) + Trajectory (7) + Class (3) and explicitly states the file is the "single source of truth"). Institutional immune memory entry.

```
W.3: Gonzo Sauce Feature Engineering Single-Source Extraction (fixed 2026-04-22)

Symptom: Three calibration bugs surfaced in one week (early April 2026; verified
against gonzo_features.py docstring lines 7-11 which name the count). Each had
a different proximate cause but the same root cause: feature values computed during
training disagreed with feature values computed during inference for identical inputs.

Root cause: model/shared/data_loader.py (training-time FE) and
backend/services/feature_engineering_service.py (inference-time FE) had drifted
in their implementation of the 14 Gonzo Sauce features. Defaults differed,
edge-case handling differed, par-time computation differed in subtle ways.

Fix: All 14 Gonzo Sauce feature computations were extracted to
model/shared/gonzo_features.py, imported by both training and inference paths
(verified imports: model/shared/data_loader.py:45 and
backend/services/feature_engineering_service.py:16). The module's docstring
states: "This module is the single source of truth for the 14 Gonzo Sauce
features. NO duplication of computation logic between training and inference."

Why this entry exists: the 14 Gonzo Sauce features are factored cleanly. The
remaining base features still have parallel implementations in
model/shared/data_loader.py and backend/services/feature_engineering_service.py,
kept in sync by manual cross-reference review. The discipline of "if you change
a feature in one place, change it in the other" is procedurally enforced, not
architecturally enforced. Phase 5.X.Y tracks the broader extraction work.

Forbidden Pattern produced: see § X.Y "Adding feature engineering logic to
either training or inference path without parallel update to the other."
```

### A.4: Deprecated Field Tracker — Legacy `predictions` Table

Pattern from the verified legacy `predictions` table that migration 005 superseded but did not drop. v4 corrected v3's "4 instantiations" inflation; v5 maintained the v4 decomposition and added the sum on race_router.py for parallel precision; v6 unchanged.

```
21.1 Legacy `predictions` table — superseded but still read

| Field/Module | Canonical Source | Notes |
|---|---|---|
| `predictions` table | `wr_predictions` (per-style WR), `pl_predictions` (P&L), `ls_predictions` (LS enrichment); created by migration 005 | The legacy `predictions` table was created by `001_initial_schema.sql:327` (verified). Migration 005 (`005_three_prediction_tables.sql`) created `wr_predictions`, `pl_predictions`, `ls_predictions` as the per-pipeline replacement (verified: zero `DROP TABLE` statements in the migration). The legacy table currently holds 6,600 rows (verified live via dashboard `counts.predictions`). It still has active readers: `prediction_router.py` (3 instantiations of `PredictionRepository` at lines 34, 61, 92, plus 1 import on line 6 = 4 references total), `race_router.py` (1 instantiation on line 277, plus 1 import on line 273 = 2 references total), `dashboard_router.py:93,105` (direct SELECT for race-record summaries), `horse_router.py:66` (direct SELECT in horse-PPs query). Planned removal: Phase 5.X.Y after readers are migrated to the per-pipeline tables. Until removal, new code MUST NOT write to the legacy table; reads are tolerated only from the legacy router paths. |
```

### A.5: Triage Queue Entry — Bug #28

Pattern showing what a `PHASE_5_BACKLOG.md` entry looks like. Final format defined in `TRIAGE_QUEUE_SPEC.md`. References to line numbers verified.

```
Phase 5.3.1: HRN Scraper Bug #28 (column shift)

Severity: HIGH (silent data loss; affects all win/DD payouts since 2026-04-30)
Surfaced: 2026-05-03 (during EE_CURRENT_STATE_DUMP generation; per operator
memory file equine-equalizer-bug-28-hrn-scraper.md, the regression was sharp —
2026-04-29 last clean day at 9/10 win-payout success; 2026-04-30 onward all 0/N)

Stable-known classification: provisional. Backfill-feasibility AND DD-pool-extraction
bounded-loss assumptions both pending Phase 1 Data Pipeline Bible audit verification
(per § 8.1).

Root cause: HRN page structure changed circa 2026-04-30 (likely added an icon
column to the payouts table). The parse_payout(N) calls at
backend/services/data_sources/hrn_scraper.py:802-804 (verified) use positional
cell indexing that has been off-by-one ever since.

Manifestation:
  - win_payout is NULL across all results rows from 2026-04-30 onward
  - daily_double_payout is NULL across same range
  - place_payout stores values that should be in win_payout
  - show_payout stores values that should be in place_payout
  - Place, show, and exacta payouts still populate per operator memory file's
    symptom statement
  - DD pool extraction at hrn_scraper.py:814 flagged as "likely has the same
    root cause" — distinct code path from daily_double_payout result-dict
    field; Phase 1 verifies bounded-loss status

Dependencies:
  - Resolution requires HRN page-structure verification (manual: visit a results
    page, confirm column structure)
  - May require parser refactor if HRN structure is now variable-by-page-type
  - Requires backfill of affected results rows after fix deploys (feasibility
    assumed; Phase 1 verifies)
  - DD pool extraction status verification (Phase 1 audit's job)

Disposition: Fix in Phase 5.3 before any Phase 5 work that depends on payout data.

Rollback: Standard git revert if fix introduces regression. No DB rollback needed
(fix re-populates rows that are currently NULL).

Bible references on resolution:
  - Update data_pipeline_bible.md § 7.9 (HRN scraper documentation)
  - Add data_pipeline_bible.md W.N (What Was Fixed entry)
  - Consider new Forbidden Pattern: positional column indexing in scrapers
    without column-header verification
```

### A.6: Audit-CC Prompt Skeleton

This is the working example of an audit-CC paste-ready prompt structure. AUDIT_METHODOLOGY.md (Phase 0 doc 3) will produce the canonical template; until then, this is the reference.

```
You are auditing a draft [DOCUMENT TYPE] for the Equine Equalizer project. This is
an adversarial audit, not a friendly review. Your job is to find every reason this
document is NOT ready to be locked. Default-positive reviewing ("this looks fine")
is failure.

CONTEXT YOU NEED:
[Project context: 2-3 paragraphs explaining what EE is, why this document is being
audited, where it sits in the phase sequence]

The roles in this project:
  - Tony: operator, final architectural authority
  - QB: tactical orchestrator drafting Phase 0 documents and specing CC tasks
  - CC: fresh Claude Code sessions executing QB-authored specs (this is you)

The audit workflow: every Phase 0 deliverable goes through adversarial CC audit
before Tony reviews it. You are the audit-CC for this document.

REFERENCE MATERIALS:
  - The DD Architecture Bible at /home/strakajagr/projects/dynasty-dugout/ARCHITECTURE_BIBLE.md
  - The EE current state dump at /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/EE_CURRENT_STATE_DUMP.md
    (NOTE: dump is best-available baseline, not source of truth; verify against live state)
  - Live AWS state via `aws` CLI for any infrastructure claim verification
  - Live API endpoints (e.g., dashboard at gb5qlfy10h.execute-api.us-east-1.amazonaws.com/dashboard/metrics)
  - The EE codebase at /home/strakajagr/projects/equine-equalizer/

VERIFICATION DISCIPLINE (HARD RULE):
  - When you verify factual claims in this draft, prefer live AWS / database / code over the dump.
  - The dump has been wrong about multiple facts in prior audits. Independent verification is the safeguard.
  - For any claim about file paths, function signatures, line numbers, or behavior — read the file or run the command.
  - Counts must be decomposed (e.g., "3 instantiations + 1 import = 4 references"); do not accept compressible aggregations in the draft. Per the v3 → v4 verification log precision rule (§ 6.5).

THE DRAFT:
[Path to draft on disk OR inline content]

COMPANION VERIFICATION LOG (if Tier 3):
[Path to verification log on disk]
[Include instruction: "Read the verification log; spot-check several entries against live state; report any verification claims that don't hold up. Per the v3 → v4 lesson, look specifically for compressible aggregations in log entries that the main doc may have inflated."]

YOUR ADVERSARIAL TASK:

Answer all six questions in order. Be specific. Cite section numbers. Quote draft
language you are critiquing.

QUESTION 1: What's in this deliverable that I can't verify from referenced source material?
[Specific verification targets for this document type]

QUESTION 2: What's missing based on the deliverable's stated scope?
[Specific scope-completeness checks for this document type]

QUESTION 3: Where is language ambiguous enough that two readers could interpret it differently?

QUESTION 4: Where does the deliverable contradict itself or other deliverables?

QUESTION 5: What sections feel rushed or hand-waved?

QUESTION 6: What examples are missing that would make abstract claims concrete?

ADDITIONAL CHECKS:
[Document-type-specific adversarial checks]

REGRESSION CHECK (for vN drafts where N >= 2):
The vN-1 audit returned specific findings. The vN draft claims fixes for each.
Verify that each claimed fix actually landed and is sound. Specifically verify:
[List representative findings to spot-check]

OUTPUT FORMAT:
[Standardized structure for findings]

SEVERITY ASSESSMENT:
[Tag each finding: BLOCKER / MATERIAL / MINOR / STYLE]

THRESHOLD CONTEXT:
Tony's threshold: if this audit returns < 5 MATERIAL findings AND zero
fabricated-content findings AND zero methodology-interpolation findings,
the document locks. Apply the MATERIAL/MINOR distinction honestly. A "missing
example" is probably MINOR. A "the maintenance protocol has an enforcement gap"
is probably MATERIAL. A "CC-interpolated binary test that Tony hasn't ratified"
is MATERIAL by its nature per the methodology-interpolation rule (§ 6.1).
Use judgment — Tony has explicitly cautioned against threshold-gaming. The
operator values surfacing problems over reassurance.

RECOMMENDATION:
[Lock as-is / lock after specific minor revisions / revise and re-audit /
substantial rework]

You are not friendly. You are looking for every reason this document is not ready.
If you find few flaws, the bar is wrong — re-read more skeptically. Begin.
```

### A.7: Methodology Skeleton with Template Slots (template-slot pattern reference)

This is the example of a documentation pattern used when QB writes framework prose and CC fills enumerated content slots. v2 had this as a Tier 2 model; v3 retired the tier but the *pattern* — explicit template slot delimiters — remains useful for any document where framework and content can be cleanly separated. Use this pattern when it helps; don't use it when it adds friction.

The framework-rejection markers from § 6.5 apply within this pattern:

- `<SPEC_GAP: explanation>` if CC's verification reveals the spec's premise is wrong (use sparingly; this invalidates the draft and routes back to QB for spec revision).
- `<FRAMEWORK_GAP: explanation>` if a specific template slot can't be filled because the framework's structure doesn't accommodate the actual content (more common; CC fills what fits and marks the gap).

Example (showing what BIBLE_STRUCTURE_SPEC.md *might* look like for one section):

```
## 4. Bible document structure

### 4.1 TOC pattern (framework, written by drafter)

Every Phase 1 bible document opens with a Table of Contents that lists numbered
sections. Section numbers are stable across the document's lifetime (renumbering
breaks cross-references in other bibles).

The TOC for any bible document includes these mandatory sections in this order:

  1. Scope of this bible
  2. Definitions (terminology specific to this bible's domain)
  3. Architecture overview (this bible's slice of the system)
  4. Canonical objects (data shapes that cross this bible's boundary)
  5. Discipline rules (Forbidden Patterns + Common Mistakes for this domain)
  6. What Was Fixed — Do Not Revert (institutional immune memory for this domain)
  7. Currently Open (one-line bug list with PHASE_5_BACKLOG pointers)
  8. Deprecated (cross-references to PHASE_5_BACKLOG entries)

### 4.2 Per-bible TOC fills (template slots, filled by drafter)

<TEMPLATE: Database & Schema Bible TOC — fill per § 4.1 framework + the verified
schema inventory in EE_CURRENT_STATE_DUMP.md § 4. Section 3 (Architecture
overview) for this bible should include: 14-table inventory with materialized
view, migration runner mechanism, predictions-table family. Section 4 (Canonical
objects) should include: WRPrediction, PLPrediction, LSPrediction dataclasses
from backend/models/canonical.py. Verify schema counts against live before filling.>

<TEMPLATE: ML Layer Architecture Bible TOC — fill per § 4.1 framework + the verified
model inventory in EE_CURRENT_STATE_DUMP.md § 3 + Forcing Function 2 per § 3.2.1.
Section 3 (Architecture overview) should include: 7-layer LS stack, model registry
semantics with the 88 = 45 active + 43 inactive multi-row reality, calibration
policy. Verify model counts against live dashboard before filling.>

<TEMPLATE: ... [one slot per Phase 1 bible document]>
```

When CC fills slots, the convention is:
- Replace the `<TEMPLATE: ...>` line with the filled content
- Preserve framework prose (sections 4.1, etc.) unmodified
- If a template slot cannot be filled because the framework's structure doesn't accommodate the content (e.g., the framework requires a "single canonical object" section but the bible's domain has multiple), CC returns the document with `<FRAMEWORK_GAP: explanation>` and a verification log entry showing the contradiction. QB triages whether to revise the framework or revise the slot spec.
- If verification reveals the entire spec's premise is wrong (e.g., the spec asks CC to document a function that doesn't exist), CC returns `<SPEC_GAP: explanation>` instead — this routes back to QB for spec revision, not framework revision.

This pattern is optional. Use it when framework and content can be cleanly
separated; skip it when separation adds more friction than it saves.

---

End of Appendix A.
