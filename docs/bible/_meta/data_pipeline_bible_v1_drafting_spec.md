# Data Pipeline Bible v1 Drafting Spec

**Document:** DATA_PIPELINE_BIBLE_V1_DRAFTING_SPEC
**Phase:** 1 deliverable 3 of 7 (drafting-order numbering per BIBLE_STRUCTURE_SPEC v6 § 8.2)
**Status:** AUTHORED 2026-05-06 — paste-ready for CC drafting session
**Author:** QB (Data Pipeline Bible cycle, 2026-05-06)
**Date:** 2026-05-06

**Spec authorship discipline:** Option 1 with 9 checks operative across 3 clusters per `QB_HANDOFF_DATA_PIPELINE_BIBLE_DRAFTING.md` § 3. QB substrate-verification log at this spec's § 11; QB-side handoff cross-reference corrections banked at § 10.

**Anchored on:**
- META_PLAN v9 (LOCKED 2026-05-05)
- BIBLE_STRUCTURE_SPEC v6 (LOCKED 2026-05-05)
- AUDIT_METHODOLOGY v2 (LOCKED 2026-05-05; § 4.8 + § 4.9 + § 4.10 + § 4.11 banked from cycle-2)
- CONVERGENCE_CRITERIA v2 (LOCKED 2026-05-04)
- TRIAGE_QUEUE_SPEC v1 (LOCKED 2026-05-04)
- Architecture Overview v3 (LOCKED 2026-05-05) — canonical references for cross-runtime topology
- Database & Schema Bible v1-patched-d1 (LOCKED 2026-05-05) — canonical references for per-table schema; F.2 + F.3 cross-reference targets
- PHASE_5_BACKLOG.md (CREATED 2026-05-04; ACTIVE) — Bug #28 entered at Phase 5.3.1 per TRIAGE_QUEUE_SPEC v1

---

## Table of contents (this spec)

1. CC paste-prompt — spec body that pastes into a fresh CC session
2. Reference materials and source-priority discipline
3. Operating disciplines CC must follow
4. Prescribed TOC and per-section drafting guidance (substrate-anchored)
5. Verification log structure and per-section content requirements
6. QB self-audit log Section H entries (to be reproduced char-exact in CC's verification log)
7. Bash-grep verification predictions (Check 9 precision)
8. Skip-audit pre-approval determination
9. Iteration expectation
10. Handoff cross-reference corrections (banked Check 1 findings)
11. QB substrate-verification log (Option 1 9-check self-audit)

---

## 1. CC paste-prompt

The block below is the paste-ready CC paste-prompt. Tony copies the text from `### 1.1 Paste-prompt body` through end-of-block into a fresh CC session. Sections 2–11 of this spec are QB-side context that does NOT paste into CC's session — they document the QB's spec authorship discipline for audit-trail purposes.

### 1.1 Paste-prompt body

> You are CC drafting **Data Pipeline Bible v1** for the Equine Equalizer (EE) Phase 1 cycle. This is Phase 1 deliverable 3 of 7 (drafting-order numbering per BIBLE_STRUCTURE_SPEC v6 § 8.2). Phase 1 deliverables 1 (Architecture Overview v3) and 2 (Database & Schema Bible v1-patched-d1) LOCKED 2026-05-05 and are the canonical references substrate this bible cross-references outward to.
>
> **Output target:** `/home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md` plus companion verification log at `/home/strakajagr/projects/equine-equalizer/docs/bible/_audit/data_pipeline_bible_v1_verification.md`.
>
> **Tier:** 3 per META_PLAN v9 § 4.1 + § 6.5. **HARD RULE: Drafts without companion verification logs are rejected by QB without audit. The verification log is not optional.**
>
> **Char-exact reproduction discipline does NOT apply** to this draft — full prose authoring latitude per CC drafter paste-prompt boilerplate (BIBLE_STRUCTURE_SPEC v6 + QB handoff § 7.1). Every factual claim requires a verification log entry per Tier 3 discipline.
>
> ---
>
> ### Reference materials (read FIRST, before drafting)
>
> 1. **Architecture Overview v3 LOCKED** at `/home/strakajagr/projects/equine-equalizer/docs/bible/architecture_overview.md` — canonical references for cross-runtime topology this bible cross-references outward to. § 3.1 (Lambda inventory + Active/INACTIVE State), § 3.2 (ECS Fargate task families), § 3.6 (EventBridge schedule with per-rule target verification + 4-fire-and-fail anomaly), § 5.1 (Forbidden Pattern: documenting a Lambda's role without verifying its current State), § 5.2 (Common Mistake: documenting an EventBridge rule's behavior without cross-referencing target State), and § 6 (fire-and-fail anomaly canonical home) are load-bearing for every § 4.1.X sub-section in this bible.
> 2. **Database & Schema Bible v1-patched-d1 LOCKED** at `/home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md` — canonical references for per-table schema this bible cross-references outward to. § 4.1 per-table sub-sections are load-bearing destinations for the per-flow detail this bible's § 4.1 enumerates. § 4.1.12 (`wr_predictions`) and § 4.1.14 (`ls_predictions`) carry the F.2 and F.3 substrate context that this bible cross-references at § 4.1.5 daily inference flow.
> 3. **BIBLE_STRUCTURE_SPEC v6 § 6.2** at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` (search for the "### 6.2 data_pipeline_bible.md" header; the section spans from that header to the next "### 6.3" header) — prescribed TOC, per-section guidance, and conditional triggers for THIS bible. **NORMATIVE for this draft.**
> 4. **BIBLE_STRUCTURE_SPEC v6 § 5.3** — cross-cutting bug scope rule: canonical home for cross-cutting bugs lives in one bible (the one whose discipline most directly prevents recurrence); other bibles cross-reference. Bug #28 canonical home is THIS bible (data-acquisition discipline prevents recurrence). The fire-and-fail anomaly canonical home is `architecture_overview:6` (cross-runtime invariant); THIS bible's § 6 carries one-line cross-reference per § 5.3 non-canonical-home rule.
> 5. **BIBLE_STRUCTURE_SPEC v6 § 5.5–§ 5.6** — W.N format, Forbidden Pattern, Common Mistakes, Deprecated entry templates (canonical). Per § 5.5.1 global Bug #N convention, cross-bible bug references use `<bible>:#<bug-id>`. Bug #28 uses the existing global ID; if § 8.W.2 (DD pool nuance) is determined to be a different root cause than Bug #28, a NEW global Bug #N gets assigned by QB at ratification (per § 5.5.1 monotonic rule).
> 6. **META_PLAN v9 § 4.5** — source-priority hierarchy: Tier 1 (live AWS) > Tier 2 (live API) > Tier 3 (live DB) > Tier 4 (working-tree code post-baseline 87dec36) > Tier 5 (operator-stated history) > Tier 6 (`EE_CURRENT_STATE_DUMP.md`) > Tier 7 (session logs).
> 7. **META_PLAN v9 § 6.5** — verification log precision rule (counts decomposed; definitions vs uses vs imports distinguished; no compressible aggregations).
> 8. **META_PLAN v9 § 7.3 placeholder-resolution sub-rule** (locked v7) — Phase 1 drafters MUST resolve W.N entry "fixed YYYY-MM-DD" dates via `git log` of the relevant primary source for any real fix where the date is git-recoverable. Placeholders only for forward-looking discipline codifications. **Operative for any W.N entry in this bible. NOTE: Bug #28 is NOT YET FIXED at lock; § 8.W.1 + § 8.W.2 carry placeholder Fix dates per Appendix A scope clause (forward-looking discipline codification).**
> 9. **META_PLAN v9 § 7.9 Data Acquisition Honesty Protocol** — per-source documentation discipline: what the source provides, current reliability state (verified empirically, not assumed), failure manifestation, current acquisition mode, honest disposition. **Mandatory for § 4.2 in this bible (6 sources per BIBLE_STRUCTURE_SPEC v6 § 6.2: HRN entries, HRN results, HRN workouts, NYRA workouts, Equibase chart parser, equibase_probe/).**
> 10. **PHASE_5_BACKLOG.md** at `/home/strakajagr/projects/equine-equalizer/docs/bible/PHASE_5_BACKLOG.md` — **EXISTS on disk (created 2026-05-04, predates this draft)**. Bug #28 entered at **Phase 5.3.1** per TRIAGE_QUEUE_SPEC v1 § 3 with Symptom/Root-cause/Manifestation/Operator-verified-external-source/Dependencies fields. Bible cross-reference for Bug #28 cites real **`Phase 5.3.1`** identifier (NOT `Phase 5.X.Y` placeholder). F.2 + F.3 cross-references continue to use `Phase 5.X.Y` placeholder per META_PLAN v9 Appendix A lead-paragraph scope clause (placeholder resolves when those specific entries land in PHASE_5_BACKLOG.md).
> 11. **EE_CURRENT_STATE_DUMP.md** at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/EE_CURRENT_STATE_DUMP.md` — Tier 6 baseline only. **Verify any inherited claim against live state per Lesson 1 (cross-project contamination check) + Lesson 2 (Phase 0 substrate errors).**
> 12. **Operator memory file `equine-equalizer-bug-28-hrn-scraper.md`** — Tier 5 source per META_PLAN v9 § 4.5; verbatim symptom quotes for Bug #28 are reproduced in PHASE_5_BACKLOG.md Phase 5.3.1 entry per META_PLAN v9 verification log Claim 15c pattern. CC inherits the verbatim quotes from PHASE_5_BACKLOG.md Phase 5.3.1 entry if the operator memory file is not directly accessible. Treat the operator memory file's symptom quote as primary substrate per Claim 15c regardless of access path.
> 13. **EE codebase at** `/home/strakajagr/projects/equine-equalizer/`. Specifically:
>     - `backend/services/data_sources/hrn_scraper.py` — HRN scraper module. Lines 802-804 contain `parse_payout(1)`, `parse_payout(2)`, `parse_payout(3)` for win/place/show extraction (Bug #28 column-shift defect surface). Line 814 contains the DD pool extraction loop (Bug #28 DD pool nuance per operator memory file).
>     - `backend/services/data_sources/` — data source module directory. CC enumerates contents at draft time via `ls backend/services/data_sources/` to surface chart parser entry point and any other data source modules.
>     - `backend/lambdas/ingestion/handler.py` — `equine-ingestion` Lambda dispatcher (INACTIVE per Architecture Overview § 3.1). Per Architecture Overview § 3.1 V3-2 sub-citation: 25 action handlers (5 data acquisition + 4 model lifecycle + 5 admin/diagnostic + 7 data backfills/ops + 3 originally-cited admin + 1 health = 25). Default-case dispatch at handler tail (lines 1669-1680 per V3-2) calls `IngestionService(conn).fetch_daily_entries(date.today())` when `event.get('action')` is None — the `equine-ingestion-daily` and `equine-fetch-results-nightly` cron-triggered path.
>     - `backend/services/wr_inference_service.py:718-730` — WR inference service: dynamic attribute attachment block per Architecture Overview § 4.2 (9 enrichment fields attached to base `Prediction` dataclass; canonical write target `wr_predictions`).
>     - `backend/services/pl_inference_service.py` — PL inference service (writes `pl_predictions`).
>     - `backend/services/ls_inference_service.py:388-401` — LS inference service: writes BOTH to `ls_predictions` (per `ON CONFLICT (race_id, entry_id, style)` upsert matching post-migration-010 constraint) AND to `wr_predictions` enrichment columns per F.3 substrate (database_schema_bible:4.1.14). The dual-write pattern is the F.3 cross-reference target at this bible's § 4.1.5.
>     - `equibase_probe/` — exploratory work directory. Verify production-runtime consumer count = 0 per Architecture Overview § 3.7 + § 3.8.
>
> ### Verification discipline (HARD RULE)
>
> - **Live AWS / database / code** prevails over EE_CURRENT_STATE_DUMP per § 4.5 source-priority. Tier 6 is best-available baseline only.
> - **Cross-project contamination check (Lesson 1):** any inherited Tier 6 claim verified against live state with explicit "is this EE substrate or bleed from an adjacent project?" test.
> - **Counts decomposed (META_PLAN v9 § 6.5):** every aggregable count must be broken down into its components in the verification log entry. The 13 EventBridge rules decomposition (10 ENABLED + 3 DISABLED) inherits from Architecture Overview § 3.6 verbatim; this bible re-cites the inherited substrate via `architecture_overview:3.6` section-anchor + per-rule line. No compressible aggregations.
> - **Methodology-interpolation rule (META_PLAN v9 § 6.1):** CC must NOT invent binary tests, cadence rules, completeness criteria, scoring rubrics, severity thresholds, iteration caps, percentage criteria, procedural sequencing rules, or other CC-prescribed methodology constructs Tony has not explicitly ratified. If verification or drafting reveals a need for such a construct, surface to QB via FRAMEWORK_GAP marker.
> - **Verbatim-paste discipline for V1-N entries (AUDIT_METHODOLOGY § 4.10).** Drafting CC MUST paste verbatim command output (raw `grep` / `git log` / `sed` / `wc` / `diff` / `cat` / `ls` output as it appears on stdout) for every V1-N entry. **Summarization of command output is treated as fabrication-class risk.** "Returns the expected output" / "matches the prediction" / "confirms the claim" without raw output is FORBIDDEN; rewrite as verbatim paste. Every grep / git log / read command result lands in Section C verbatim, NOT summarized.
> - **Per-resource verification when target/state are independent (AUDIT_METHODOLOGY § 4.5; Lesson 5).** EventBridge rule State and target Lambda State are independent AWS concepts. Per-rule `aws events list-targets-by-rule` is the canonical citation. **Inheritance discipline for THIS bible:** the 13-rule × per-rule-target verification was performed by Architecture Overview v3 per Lesson 5; this bible inherits Architecture Overview v3 § 3.6's locked output. CC re-cites the inherited substrate via `architecture_overview:3.6` section-anchor + the per-rule line within that table, NOT via fresh `aws` calls. **If audit-CC re-runs `aws events list-targets-by-rule` adversarially and surfaces drift from Architecture Overview v3's locked output, that drift is an upstream-correction question routed to QB per Lesson 6 — NOT silently corrected by drafting CC.**
> - **Framework-rejection markers (META_PLAN v9 § 6.5):**
>   - `<SPEC_GAP: explanation>` — entire spec premise wrong (e.g., spec asks CC to document a flow whose substrate doesn't exist).
>   - `<FRAMEWORK_GAP: explanation>` — specific framework slot can't be filled because the framework's structure doesn't accommodate the actual content (per Lesson 4: CC fills what fits, marks the gap, lets QB triage; if CC has a candidate reframing, CC presents it as candidate AND cites the substrate that supports OR refutes it).
> - **No fabrication.** If verification cannot confirm a claim, drop the claim or explicitly mark it as unverified-pending-Phase-X. Per META_PLAN v9 § 8.6.
>
> ### Methodology lessons + active discipline (operative throughout)
>
> 1. **Lesson 1 — Cross-project contamination check.** Tier 6 verification includes cross-project bleed check, not just freshness check.
> 2. **Lesson 2 — Phase 1 verification surfaces Phase 0 substrate errors.** Surgical correction expected; not Phase 0 re-lock. If this draft surfaces a Phase 0 substrate error, surface to QB rather than silently working around it.
> 3. **Lesson 3 (re-expanded) — Drafting specs cite primary verification log claim IDs, not paraphrased restatements.** Discipline applies to claim IDs, count statements, quoted text, attribution paraphrases, prescribed cross-reference section numbers, prescribed definition framing content, audit-CC enumeration completeness, line-number citations (Check 8 makes them line-shift-resistant), and bash-grep prediction precision (Check 9).
> 4. **Lesson 4 — FRAMEWORK_GAP discipline.** Any reframing CC introduces in its draft requires substrate verification. CC surfaces FRAMEWORK_GAP, fills what fits honestly, lets QB triage. If CC has a candidate reframing, present it as candidate AND cite the substrate that supports OR refutes it.
> 5. **Lesson 5 — Per-resource verification when target/state are independent AWS resources.** EventBridge rule State and target Lambda State are independent. Inheritance discipline operative for this bible (above).
> 6. **Lesson 6 — Synthesis verification.** When synthesizing audit-CC findings into upstream-correction scope, the upstream claim is substrate-verified before synthesis routes. Audit-CC's downstream finding does not propagate as upstream truth without QB substrate check.
> 7. **AUDIT_METHODOLOGY § 4.8 — QB substrate findings during spec authorship require Tony ratification.** Operative throughout the cycle: any substrate gap CC surfaces routes through QB → Tony ratification, NOT silently corrected.
> 8. **AUDIT_METHODOLOGY § 4.9 — QB review pass is light surface review only; substrate verification is audit-CC's job.** Operative on QB during the review cycle.
> 9. **AUDIT_METHODOLOGY § 4.10 — Verbatim-paste discipline for V1-N entries.** Operative throughout (above; HARD RULE).
> 10. **AUDIT_METHODOLOGY § 4.11 — V1-N grep predictions against unions of files must account for byte-identity edge cases.** Operative for any grep prediction in this spec that targets a union of files where bootstrap-mirror or duplicate-prefix pairs may exist. (Less load-bearing for this bible than for D&S Bible — Data Pipeline grep targets are mostly single-file substrate reads — but the rule applies wherever multi-file unions are used.)
> 11. **Check 7 — Mid-cycle scope extensions touch all narrative-referencing sections (banked Architecture Overview v3 H7).** When QB extends a spec mid-cycle, enumerate ALL narrative-referencing sections (verification log Sections G/H/I + main doc revision history + main doc body cross-references) and update each. Operative on QB if v2/v3 cycles extend scope.
> 12. **Check 8 — Line-shift-resistant citations replace literal line numbers (banked Architecture Overview v3 H8).** Cross-references between bibles use section IDs (`architecture_overview:3.6`) NOT literal line numbers. Literal line numbers acceptable only when tightly scoped to canonical-substrate identification (e.g., `hrn_scraper.py:802-804`, `ls_inference_service.py:388-401`) — never for cross-bible cross-reference. Operative starting D&S Bible spec; carries forward to this cycle.
>
> ### Bug #28 substrate disposition routing (per Tony's Item 2 ratification, 2026-05-05)
>
> Per § 6.2 default + Tony's Item 2 ratification: drafting CC drafts BOTH § 8.W.1 (column shift at `hrn_scraper.py:802-804` — win/DD-payout NULL since 2026-04-30) and § 8.W.2 (DD pool extraction nuance at `hrn_scraper.py:814`). The two-W.N default reflects the operator memory file's separate flagging of the DD pool nuance.
>
> **Substrate disposition routing for V1-N:**
> - Drafting CC reads `hrn_scraper.py:802-804` AND `hrn_scraper.py:814` directly and pastes verbatim source code in V1-N entries per Lesson § 4.10.
> - If V1-N substrate determines root cause IDENTICAL at both line ranges (same column-shift class affecting both result-dict and pool-table-loop) → CC surfaces FRAMEWORK_GAP F.X with substrate evidence; presents candidate reframing of "collapse to single § 8.W.1 with adjacent prose covering pool extraction manifestation" + cites substrate supporting collapse.
> - If V1-N substrate determines root cause DIFFERENT (separate defect classes; e.g., :802-804 is positional-cell-indexing, :814 is pool-table-loop iteration logic distinct from positional indexing) → both W.N entries stand as separate; § 8.W.2 may warrant its own global Bug #N (TBD pending QB → Tony ratification).
> - **Default disposition:** drafting CC drafts both as separate § 8.W.1 + § 8.W.2 entries. CC does NOT collapse to single entry without QB ratification per Lesson § 4.8. CC does NOT assign § 8.W.2 a new global Bug #N without QB ratification per § 5.5.1.
>
> **Bug #N global ID disposition for § 8.W.2:**
> - § 8.W.1 = Bug #28 (existing global ID per BIBLE_STRUCTURE_SPEC v6 § 5.5.1; PHASE_5_BACKLOG.md Phase 5.3.1).
> - § 8.W.2 Bug #N = TBD pending substrate determination (above). Drafting CC marks the § 8.W.2 entry's Bug-#N field as `[Bug #N TBD — pending QB ratification post-substrate verification]`.
>
> ### G-new-1 closure operative (candidate-roster numbering)
>
> If § 5 contains a candidate roster pending QB ratification (per § 5.7), use **numeric sub-section IDs** (`5.1`, `5.2`, ...) consistent with § 5.5 ratified-entry convention. **Provisional letter-prefixes (e.g., `5.A`, `5.F.1`) are NOT authorized.** Candidate status is conveyed by the § 5 header marker `[candidate roster pending QB ratification per § 5.7]`, not by letter-prefix.
>
> ---
>
> ### Prescribed TOC (mandatory per § 5.2 sections 5–8; recommended-strongly per § 5.2 sections 1–4 with drafter latitude per locality of reference)
>
> Per BIBLE_STRUCTURE_SPEC v6 § 6.2:
>
> 1. Scope
> 2. Definitions (HRN, NYRA, Equibase chart, "qualifying track")
> 3. Pipeline overview
> 4. Pipeline detail
>    - 4.1 Per-flow detail
>      - 4.1.1 Daily ingestion (race cards) — `equine-ingestion-daily` cron
>      - 4.1.2 Nightly results fetch — `equine-fetch-results-nightly` cron
>      - 4.1.3 Chart parser (S3 PDFs → results enrichment)
>      - 4.1.4 NYRA workout scrape — `equine-nyra-workouts-daily` cron
>      - 4.1.5 Daily inference (3 separate Lambdas: WR / PL / LS)
>      - 4.1.6 Results matcher — `equine-results-daily` cron
>      - 4.1.7 Angle stats refresh — `equine-angle-stats-nightly` cron
>      - 4.1.8 Daily retraining — `equine-daily-retrain-full` cron
>      - 4.1.9 Weekly retraining — `equine-weekly-retrain-wr` cron
>    - 4.2 Data Acquisition Honesty Protocol (per META_PLAN v9 § 7.9)
>      - 4.2.1 HRN entries
>      - 4.2.2 HRN results
>      - 4.2.3 HRN workouts
>      - 4.2.4 NYRA workouts
>      - 4.2.5 Equibase chart parser path
>      - 4.2.6 `equibase_probe/` exploratory work
> 5. Discipline rules
> 6. Currently Open
> 7. Deprecated
> 8. What Was Fixed (canonical home for Bug #28)
>
> **§ 5 candidate-roster workflow (per § 5.7):**
> 1. CC drafts § 5 with candidate roster (FORBIDDEN/CORRECT pairs per § 5.6.2; Common Mistakes per § 5.6.3).
> 2. CC produces § 5 verification log delta (Section C entries) enumerating each candidate rule's substrate evidence + provenance.
> 3. CC marks § 5 header `[candidate roster pending QB ratification per § 5.7]`.
> 4. QB reviews + ratifies (this happens in QB's review cycle, between draft submission and audit-CC pass).
>
> ---
>
> ### Per-section content requirements
>
> **§ 1 Scope (recommended-strongly per § 5.2):**
> - Mandatory: state what this bible documents (per-flow data movement: ingestion → DB → model → API; data acquisition discipline; retrain triggers as operational instances) and what it does NOT (per-table schema → `database_schema_bible:4.1`; per-feature consumption → `feature_provenance_bible:4`; per-model architecture → `ml_layer_architecture_bible:4`; success criteria/retrain mechanics → `model_evaluation_retraining_bible:4`; per-route detail → `api_frontend_bible:4.1`; cross-runtime topology → `architecture_overview:3`).
> - Cross-reference Architecture Overview § 3.1 (Lambda inventory), § 3.2 (ECS Fargate task families), § 3.6 (EventBridge schedule + fire-and-fail anomaly), § 5.1 + § 5.2 (Forbidden Pattern + Common Mistake governing § 4.1.X documentation discipline).
> - Cross-reference Database & Schema Bible § 4.1 per-table sub-sections as destinations for per-flow writes.
> - State source-priority hierarchy (Tier 1 AWS > Tier 4 working-tree code; matches META_PLAN v9 § 4.5).
> - Boundary statement: this bible is **flow-narrative** (per-flow walk from source through Lambda(s) to DB destination); other bibles are reference-style (D&S) or composition-narrative (ML Layer).
>
> **§ 2 Definitions:**
> - Mandatory terms: HRN (Horse Racing Nation, the scraper's source domain), NYRA (New York Racing Association), Equibase chart (the post-race PDF chart Equibase publishes), qualifying track (per `tracks.is_qualifying` flag in DB; cross-reference `database_schema_bible:4.1.tracks`), default-case dispatch (Lambda handler tail-end path triggered when `event.get('action')` is None — per Architecture Overview § 3.1 V3-2 sub-citation), fire-and-fail (ENABLED EventBridge rule targeting INACTIVE Lambda; cron fires, invocation returns `ResourceNotReadyException` — per Architecture Overview § 6).
> - Acronyms defined elsewhere (WR / PL / LS, Active vs Inactive Lambda) referenced from `architecture_overview:2`, NOT redefined.
> - Cross-reference META_PLAN v9 § 4.5 source-priority for tier-resolution semantics where relevant.
>
> **§ 3 Pipeline overview:**
> - High-level narrative: data flows from external sources (HRN, NYRA, Equibase) through scrapers/parsers (Lambdas + ECR images) into RDS, fed to inference Lambdas (WR/PL/LS) which write per-pipeline prediction tables, exposed via API Gateway integrations on `equine-inference` (per `architecture_overview:3.5`).
> - State the 9 cron-triggered flows enumerated at § 4.1; note that 4 of them (4.1.1, 4.1.2, 4.1.6, 4.1.7) target INACTIVE Lambdas (fire-and-fail per `architecture_overview:6`).
> - Cross-reference forward to § 4.1 for per-flow detail; § 4.2 for per-source honesty disposition.
>
> **§ 4.1 Per-flow detail (one sub-section per flow per § 6.2 prescribed TOC):**
>
> Per § 6.2 + § 5.6.4 mandatory fields, each § 4.1.X sub-section enumerates:
> - **Trigger:** EventBridge rule name + cron expression (UTC). Cite `architecture_overview:3.6` table row by section-anchor + rule name. For chart parser (4.1.3) which has no direct EventBridge rule, document the trigger mechanism (manual via admin action OR chained downstream of another flow); CC verifies at draft time per S.3 below.
> - **Source:** what produces the data being moved (HRN page, NYRA endpoint, Equibase PDF, manual upload, upstream DB table).
> - **Lambda(s) involved:** function name + Active/INACTIVE State + memory + timeout. Cite `architecture_overview:3.1` table row by section-anchor + function name (per Architecture Overview § 5.1 Forbidden Pattern: every Lambda role assertion cites State at the same lock time).
> - **Action(s) dispatched:** for `equine-ingestion`, the action name(s) the cron Input or default-case dispatch invokes (cite Architecture Overview § 3.1 V3-2 sub-citation for the 25-action surface + default-case behavior).
> - **Destination tables:** which DB tables the flow writes to. Cite `database_schema_bible:4.1.<table>` by section-anchor.
> - **Cross-reference Architecture Overview § 5.1 + § 5.2** explicitly: per Architecture Overview's Forbidden Pattern + Common Mistake, every § 4.1.X sub-section cites Lambda State + EventBridge target State at the same lock time. Each sub-section's documentation discipline must visibly satisfy these.
>
> Conditional fields (with triggers per § 6.2):
> - **If the flow has known failure modes:** enumerate with date discovered, manifestation symptoms (DB row patterns, log signatures, downstream model degradation).
> - **If the flow is currently impaired (source Lambda is INACTIVE):** document the impairment with cross-reference to `architecture_overview:6` (canonical impairment description). § 4.1.X sub-section's Currently-Open-touching-this-flow block carries a one-line cross-reference per § 5.3 non-canonical-home rule, NOT a duplicated description of the fire-and-fail anomaly.
> - **If the flow is canonically home to a What Was Fixed entry:** cross-reference per § 5.3 (Bug #28 → § 8.W.1 + § 8.W.2 in this bible).
> - **If the flow's failure mode is currently in `PHASE_5_BACKLOG.md`:** cite the phase number (Bug #28 → `Phase 5.3.1`).
>
> **§ 4.1.X mapping (cardinality 10 ENABLED rules across 9 sub-sections; § 4.1.5 holds 3 rules; § 4.1.3 holds 0 direct EventBridge rules):**
>
> - **§ 4.1.1 Daily ingestion (race cards).** EventBridge: `equine-ingestion-daily` (`cron(0 11 * * ? *)`, ENABLED). Target: `equine-ingestion` (INACTIVE). Action dispatched: default-case (no `action` Input → `IngestionService(conn).fetch_daily_entries(date.today())` per Architecture Overview § 3.1 V3-2 sub-citation, lines 1669-1680 of handler.py). Source: HRN entries page. Destination tables: `entries`, `races`, `horses`, `trainers`, `jockeys`, `tracks`, `past_performances` (the entry-row plus referenced foreign-key parents). Currently impaired: fire-and-fail per `architecture_overview:6`.
> - **§ 4.1.2 Nightly results fetch.** EventBridge: `equine-fetch-results-nightly` (`cron(30 1 * * ? *)`, ENABLED). Target: `equine-ingestion` (INACTIVE). Action dispatched: default-case (per Architecture Overview § 3.1 V3-2 — same default-case path as 4.1.1; rule's historical name "fetch-results-nightly" does not currently dispatch a results-specific action). Source: HRN results pages. Destination tables: `results` (and the win/place/show/exacta/trifecta/superfecta/daily_double payout fields therein — the column-shift defect surface for Bug #28). Currently impaired: fire-and-fail per `architecture_overview:6`. **Bug #28 cross-reference at § 8.W.1 (canonical home).**
> - **§ 4.1.3 Chart parser (S3 PDFs → results enrichment).** EventBridge: **none directly** — CC verifies at V1-N substrate read whether chart parser is invoked via (a) `parse_charts` admin action on `equine-ingestion` (manual or chained), (b) S3 ObjectCreated event on `equine-raw-data` triggering a Lambda, or (c) downstream chained from another flow. Source: PDF charts in `s3://equine-raw-data/` (per `architecture_overview:3.4`). Destination tables: `results` (enrichment columns from chart vs HRN-results-page; verify at draft time which columns chart parser populates vs HRN). If chart parser entry point is inside `equine-ingestion` and that Lambda is INACTIVE, document the impairment per § 5.1 discipline.
> - **§ 4.1.4 NYRA workout scrape.** EventBridge: `equine-nyra-workouts-daily` (`cron(0 10 * * ? *)`, ENABLED). Target: `equine-nyra-workouts` (Active, 512 MB, 300s). Source: NYRA workout endpoint (NYRA tracks only). Destination tables: `workouts`. Currently functional.
> - **§ 4.1.5 Daily inference (WR / PL / LS — 3 rules under one sub-section per § 6.2).** EventBridge rules:
>   - `equine-wr-inference-daily` (`cron(30 12 * * ? *)`, ENABLED) → `equine-wr-inference` (Active). Writes `wr_predictions` per `database_schema_bible:4.1.12`. Per Architecture Overview § 4.2: WR pipeline dynamically attaches 9 enrichment fields to base `Prediction` dataclass (`wr_inference_service.py:718-730`). **F.2 cross-reference (database_schema_bible:4.1.12):** `wr_predictions` schema has `style` and `model_used` columns added via out-of-band ALTER not preserved as a tracked migration; flow-context observation here, substantive description in D&S Bible.
>   - `equine-pl-inference-daily` (`cron(35 12 * * ? *)`, ENABLED) → `equine-pl-inference` (Active). Writes `pl_predictions` per `database_schema_bible:4.1.13`. **F.2 cross-reference (database_schema_bible:4.1.13)** for `pl_predictions.style` out-of-band column addition.
>   - `equine-ls-inference-daily` (`cron(40 12 * * ? *)`, ENABLED) → `equine-ls-inference` (Active). **Dual-write pattern (F.3 cross-reference):** `ls_inference_service.py:388-401` writes BOTH to `ls_predictions` (per `ON CONFLICT (race_id, entry_id, style)` upsert matching post-migration-010 constraint) AND to `wr_predictions` enrichment columns (LS-as-second-pass-enrichment per migration 010 preamble). Substantive description at `database_schema_bible:4.1.14`. Flow-context observation here.
>   - All three currently functional. Cross-reference forward to `ml_layer_architecture_bible:4.2` for per-pipeline ML composition.
> - **§ 4.1.6 Results matcher.** EventBridge: `equine-results-daily` (`cron(0 4 * * ? *)`, ENABLED). Target: `equine-results` (INACTIVE). Source: chart parser output + HRN results. Destination tables: `results` (matching/reconciliation pass after chart parsing). Currently impaired: fire-and-fail per `architecture_overview:6`.
> - **§ 4.1.7 Angle stats refresh.** EventBridge: `equine-angle-stats-nightly` (`cron(15 2 * * ? *)`, ENABLED). Target: `equine-ingestion` (INACTIVE). Action dispatched: `refresh_angle_stats` (Input `{"action":"refresh_angle_stats"}`; handler at `backend/lambdas/ingestion/handler.py:94` per Architecture Overview § 3.1 + § 3.6). Source: existing DB rows in `past_performances`, `results`. Destination tables: `angle_stats` (aggregation table; verify schema reference at `database_schema_bible:4.1.<angle_stats_or_equivalent>` if exists, OR document the absence at draft time). Currently impaired: fire-and-fail per `architecture_overview:6`.
> - **§ 4.1.8 Daily retraining.** EventBridge: `equine-daily-retrain-full` (`cron(30 2 * * ? *)`, ENABLED). Target: ECS task family `equine-training-daily-full` (per `architecture_overview:3.2` + § 3.6 — `EcsParameters.TaskDefinitionArn = arn:aws:ecs:us-east-1:584812014683:task-definition/equine-training-daily-full`). Source: training data from RDS (`past_performances`, `results`, `entries` joins). Destination: `s3://equine-model-artifacts/<family>/<version>.json` + `model_versions` registry rows. Cross-reference forward to `model_evaluation_retraining_bible:4` for retrain mechanics.
> - **§ 4.1.9 Weekly retraining.** EventBridge: `equine-weekly-retrain-wr` (`cron(0 4 ? * MON *)`, ENABLED). Target: ECS task family `equine-training-win-prob`. Same flow shape as 4.1.8, scoped to WR pipeline only. Cross-reference forward to `model_evaluation_retraining_bible:4`. **Note: `equine-weekly-retrain-pl` (DISABLED) targets `equine-training-pl`** — document at § 7 Deprecated, NOT § 4.1.9.
>
> **§ 4.2 Data Acquisition Honesty Protocol (per META_PLAN v9 § 7.9):**
>
> Per § 6.2 mandatory fields (per source: HRN entries, HRN results, HRN workouts, NYRA workouts, Equibase chart parser, equibase_probe/):
> - **What the source provides:** specific tables/fields populated.
> - **Current reliability state:** verified empirically, not assumed. For HRN entries: cite Bug #7 compound failures per META_PLAN v9 § 1.2. For HRN results: cite Bug #28 column shift per PHASE_5_BACKLOG.md Phase 5.3.1 + this bible's § 8.W.1 + § 8.W.2. For NYRA workouts: cite Active state of `equine-nyra-workouts` Lambda. For Equibase chart parser: cite chart-parser entry point's State (depends on V1-N substrate verification at § 4.1.3).
> - **Failure manifestation:** how silent failure presents (DB row symptoms, log signatures, downstream model degradation).
> - **Current acquisition mode:** autonomous / monitored / scheduled-manual / paid-replacement (per META_PLAN v9 § 3.5 disposition vocabulary).
> - **Honest disposition:** what the mode SHOULD be, with rationale.
>
> Conditional fields (with triggers):
> - **If the source has recent failure history:** include dates with the symptom statement (verbatim from operator memory file where applicable, per META_PLAN v9 verification log Claim 15c pattern).
> - **If the source's honest disposition differs from current mode:** flag the discrepancy and reference Phase 4 for the keep/refactor/replace/kill decision.
>
> **§ 4.2 substrate-anchored disposition guidance:**
> - § 4.2.1 HRN entries: scraper module is `hrn_scraper.py` (verified by QB substrate read of file paths via prior cycle inheritance). Bug #7 compound failures (per META_PLAN v9 § 1.2). Mode determination requires `equine-ingestion` Lambda State context.
> - § 4.2.2 HRN results: same scraper module; **Bug #28 column shift is the dominant honest-disposition concern**. Per PHASE_5_BACKLOG.md Phase 5.3.1: 2026-04-29 last clean day at 9/10 win-payout success; 2026-04-30 onward all 0/N. Mode = "currently broken in production" — honest disposition pending Phase 5.3.1 fix.
> - § 4.2.3 HRN workouts: scraper module path; reliability state TBD per draft-time substrate read.
> - § 4.2.4 NYRA workouts: `equine-nyra-workouts` Lambda Active per `architecture_overview:3.1`. Mode = autonomous; honest disposition = autonomous (matches).
> - § 4.2.5 Equibase chart parser: entry point determined by V1-N at § 4.1.3 substrate read. If entry point is inside INACTIVE `equine-ingestion`, mode is currently broken; honest disposition pending re-activation Phase 5 entry.
> - § 4.2.6 `equibase_probe/`: per Architecture Overview § 3.7 + § 3.8, zero production-runtime consumers of 2captcha + brightdata Secrets Manager entries. Disposition pending — kill / paid-replacement / scheduled-manual per META_PLAN v9 § 3.5.
>
> **§ 5 Discipline rules (sections 5–8 mandatory per § 5.2):**
>
> Per § 5.7 candidate-roster workflow + ratifications S.7 + S.8:
>
> - **§ 5.1 candidate Forbidden Pattern: Positional column indexing in scrapers without column-header verification.** Surfaced by Bug #28 per § 6.2 + PHASE_5_BACKLOG.md Phase 5.3.1 "Bible references on resolution" + META_PLAN v9 Appendix A.5. Provisionally numbered 5.1.
> - **§ 5.2 candidate Common Mistake: Producer-side parent-row verification before child INSERTs.** Inherited from D&S Bible Q3.3.c forward-deferral (database_schema_bible v1-patched § 5 lead paragraph). Provisionally numbered 5.2. Wrong instinct: "the FK constraint will catch missing parents." Corrected position: defensively assert parent exists at producer (e.g., `INSERT ... ON CONFLICT DO NOTHING` for the parent first, then the child); FK violation is symptom, not discoverability mechanism.
> - Additional rules surfaced by CC during candidate-roster enumeration: surface per § 5.7 workflow with substrate evidence. CC produces verification log Section C entries enumerating each candidate's substrate provenance.
> - **§ 5 header marker:** `[candidate roster pending QB ratification per § 5.7]`.
>
> **§ 6 Currently Open:**
> - Per BIBLE_STRUCTURE_SPEC v6 § 5.3 cross-cutting bug Currently Open scope rule.
> - **One-line cross-reference for fire-and-fail anomaly:** `Fire-and-fail anomaly (4 ENABLED rules → 2 INACTIVE Lambdas): canonical home architecture_overview:6.` This bible is non-canonical-home for the cross-runtime invariant; cross-reference only, NOT duplicated description.
> - **Bug #28 itself is canonically homed in THIS bible** (§ 8.W.1 + § 8.W.2). Per § 5.3, when a cross-cutting bug is currently open at lock time, it appears in § 6 of the canonical-home bible AS the substantive description PLUS in § 6 of every bible whose discipline its symptoms touch. **For Bug #28 in THIS bible's § 6:** since canonical home IS this bible, § 6 carries the substantive Currently-Open description (with cross-references to § 8.W.1 + § 8.W.2 once those entries land at lock — recursion-safe per § 5.3 Currently Open scope rule). At lock with Bug #28 still unfixed, § 6 description includes: substrate (PHASE_5_BACKLOG.md Phase 5.3.1), manifestation (NULL `results.win_payout` + NULL `results.daily_double_payout` since 2026-04-30), operator-verified external source (verbatim symptom quote per Claim 15c pattern), Phase 5 disposition (`Phase 5.3.1` — real identifier, NOT placeholder).
> - Empty-section explicit rule per § 5.2: if no other Currently Open entries surface, document explicitly with "No additional current open issues at lock canonically homed in this bible's domain."
>
> **§ 7 Deprecated:**
> - 3 DISABLED EventBridge rules per `architecture_overview:3.6` carry the deprecation candidate surface:
>   - `equine-feature-engineering-daily` (DISABLED, zero current targets) — operator-disabled when feature-engineering moved inference-side per Phase A3 (per Architecture Overview § 3.6 + V3-N).
>   - `equine-inference-daily` (DISABLED, zero current targets) — replaced by per-pipeline rules `equine-{wr,pl,ls}-inference-daily`.
>   - `equine-weekly-retrain-pl` (DISABLED) — operator-disabled (PL retrain currently in `equine-daily-retrain-full` umbrella).
> - Per § 5.6.4 conditional triggers + BIBLE_STRUCTURE_SPEC v6 § 6.2 conditional ("If a deprecated rule has been DISABLED but not removed"): document each rule with date disabled (if known via Architecture Overview substrate or git log), reason, status (DISABLED-not-removed). Cross-reference forward to `architecture_overview:3.6` for the per-rule target verification.
> - Empty-section explicit rule per § 5.2: if no further deprecated entries surface, document explicitly.
>
> **§ 8 What Was Fixed — canonical home for Bug #28:**
>
> Per § 5.6.1 mandatory + conditional fields. Per § 6.2 prescription:
>
> **§ 8.W.1: HRN scraper column-shift defect at `parse_payout` calls (Bug #28; fixed YYYY-MM-XX — placeholder per § 7.3 Appendix A scope clause; fix has not landed at lock).**
> - Bug #N: 28 (existing global identifier per BIBLE_STRUCTURE_SPEC v6 § 5.5.1; PHASE_5_BACKLOG.md Phase 5.3.1).
> - Fix date: placeholder per META_PLAN v9 Appendix A scope clause (forward-looking discipline codification; fix has not landed at lock — Bug #28 status is "open" in PHASE_5_BACKLOG.md).
> - Symptom: per PHASE_5_BACKLOG.md Phase 5.3.1 verbatim:
>   - `win_payout` NULL across all results rows from 2026-04-30 onward
>   - `daily_double_payout` NULL across same range
>   - `place_payout` stores values that should be in `win_payout`
>   - `show_payout` stores values that should be in `place_payout`
>   - Place, show, and exacta payouts still populate per operator memory file's symptom statement
> - Operator-verified external source (per META_PLAN v9 verification log Claim 15c pattern; verbatim quote inherited from PHASE_5_BACKLOG.md Phase 5.3.1):
>   > "starting 2026-04-30, all results.win_payout and results.daily_double_payout rows are NULL across every track/race scraped via HRN. Place, show, and exacta payouts still populate."
> - Root cause: HRN page structure changed circa 2026-04-30 (likely added an icon column to the payouts table). The `parse_payout(N)` calls at `backend/services/data_sources/hrn_scraper.py:802-804` use positional cell indexing that has been off-by-one ever since. CC pastes verbatim source code at lines 802-804 in V1-N entry per Lesson § 4.10.
> - Fix: pending Phase 5.3.1 per PHASE_5_BACKLOG.md disposition.
> - Why this entry exists: prevents recurrence of "positional column indexing in scrapers without column-header verification" (candidate Forbidden Pattern at § 5.1).
> - Conditional triggers (per § 5.6.1.2 tertiary-state notation):
>   - if-fix-involved-migration: DOES NOT FIRE (scraper bug; no schema migration involved).
>   - if-fix-invalidated-prior-content: DOES NOT FIRE (no prior bible content existed at fix time — pre-Phase-1 surfacing; bug not yet fixed).
>   - if-fix-produced-Forbidden-Pattern: FIRES (cross-reference to § 5.1 candidate Forbidden Pattern pending QB ratification).
>   - if-fix-touches-multiple-bibles: CONDITIONAL — symptoms touch `database_schema_bible:4.1.results` (NULL columns); D&S Bible § 6 carries one-line cross-reference per § 5.3. Adjacent prose caveat: cross-cutting symptom-touch is documented; canonical home remains this bible per § 5.3 (data-acquisition discipline most directly prevents recurrence).
>
> **§ 8.W.2: HRN scraper DD pool extraction nuance at `hrn_scraper.py:814` (Bug #N TBD — pending QB ratification post-substrate verification; fixed YYYY-MM-XX — placeholder per § 7.3 Appendix A scope clause; fix has not landed at lock).**
> - Bug #N: TBD per Tony's Item 2 ratification routing (above). Drafting CC marks the field as `[Bug #N TBD — pending QB ratification post-substrate verification]`.
> - Fix date: placeholder per § 7.3 Appendix A scope clause.
> - Symptom: per PHASE_5_BACKLOG.md Phase 5.3.1 verbatim:
>   > "DD pool extraction (hrn_scraper.py:814 'pool' table loop) likely has the same root cause — same site-wide column shift."
> - Root cause: per V1-N substrate verification (CC reads `hrn_scraper.py:814` and pastes verbatim source code; determines whether root cause is identical to § 8.W.1 :802-804 positional indexing OR distinct pool-table-loop logic).
>   - **If root cause IDENTICAL to § 8.W.1:** CC surfaces FRAMEWORK_GAP F.X with substrate evidence; presents candidate reframing of "collapse to single § 8.W.1 with adjacent prose covering pool extraction manifestation"; QB synthesizes; surfaces to Tony per Lesson § 4.8 for collapse-or-stand decision before bible locks.
>   - **If root cause DIFFERENT:** § 8.W.2 stands as separate; § 8.W.2 Bug #N gets new global identifier assigned by QB→Tony at ratification per BIBLE_STRUCTURE_SPEC v6 § 5.5.1 monotonic rule.
> - Fix: pending Phase 5.3.1 per PHASE_5_BACKLOG.md disposition (which currently includes "DD pool extraction status verification (Phase 1 audit's job)" as Phase 1-tracking item).
> - Conditional triggers: same template as § 8.W.1; CC populates per substrate determination.
>
> Empty-section explicit rule per § 5.2: if no other W.N entries surface, document explicitly with "No additional W.N entries at lock canonically homed in this bible's domain."
>
> ---
>
> ### Companion verification log structure
>
> File location: `/home/strakajagr/projects/equine-equalizer/docs/bible/_audit/data_pipeline_bible_v1_verification.md` (note: `_audit/` singular per META_PLAN v9 § 3.8; Phase 1 docs live there).
>
> Section structure per QB handoff § 7.2:
> - **Section A:** inherited claims from upstream Phase 0 / Phase 1 verification logs (META_PLAN v9 + Architecture Overview v3 + Database & Schema Bible v1) with re-verification timestamps.
> - **Section B:** inherited claims from prior cycles of THIS bible's verification log (NOT applicable for v1 — first cycle).
> - **Section C:** new V1-N claims with primary citations + verbatim command output per AUDIT_METHODOLOGY § 4.10. Each factual claim about EE has a V1-N entry per Tier 3 discipline.
> - **Section D:** methodology-interpolation self-check (target: ZERO new methodology constructs).
> - **Section E:** pattern-completion check (W.N exclusivity preserved; numeric IDs honored per § 5.5 + G-new-1).
> - **Section F:** FRAMEWORK_GAP / SPEC_GAP markers (target: ZERO unless surfaced honestly with substrate-cited reframing per Lesson 4).
> - **Section G:** prior-cycle audit findings closure verification (NOT applicable for v1).
> - **Section H:** QB self-audit log (reproduce char-exact from this spec's § 6).
> - **Section I:** new entries for surgical patch operations (NOT applicable for v1 — first cycle is full draft).
>
> ### Substrate-anchored verification claims CC must produce (Section C entries)
>
> Each item below corresponds to a Section C V1-N claim CC produces. **Every entry pastes verbatim command output per Lesson § 4.10 — no summarization.**
>
> 1. **V1-1: 13 EventBridge rules (10 ENABLED + 3 DISABLED) — substrate inheritance from Architecture Overview v3.** Verification: read `architecture_overview:3.6` table sections (the ENABLED + DISABLED tables) and quote the per-rule target rows as the substrate. Verbatim paste of the relevant rows (rule name + cron + target Lambda/ECS family + Lambda State at lock). Per Lesson 5 inheritance discipline: do NOT re-run `aws events list-targets-by-rule` from drafting CC sandbox. Source-tier: Tier 1 (inherited via Architecture Overview v3 verification log). Decomposition: 4 fire-and-fail (ENABLED → INACTIVE: ingestion-daily, fetch-results-nightly, angle-stats-nightly → equine-ingestion; results-daily → equine-results) + 4 active-Lambda (ENABLED → Active: ls-inference-daily, nyra-workouts-daily, pl-inference-daily, wr-inference-daily) + 2 ECS (daily-retrain-full, weekly-retrain-wr) + 3 DISABLED (feature-engineering-daily, inference-daily, weekly-retrain-pl). 4+4+2+3=13.
> 2. **V1-2: ECS Fargate task families inventory — substrate inheritance.** Verification: read `architecture_overview:3.2` table and quote 5 task families verbatim (`equine-training`, `equine-training-daily-full`, `equine-training-manual`, `equine-training-pl`, `equine-training-win-prob`).
> 3. **V1-3: HRN scraper Bug #28 column-shift defect at hrn_scraper.py:802-804.** Verification command: `sed -n '798,808p' backend/services/data_sources/hrn_scraper.py`. Paste verbatim output per Lesson § 4.10. Expected: substrate showing `parse_payout(1)`, `parse_payout(2)`, `parse_payout(3)` (or analogous positional cell-index calls). If substrate differs from META_PLAN v9 § 1.2 inheritance, surface FRAMEWORK_GAP per Lesson 2 (Phase 0 substrate-error class).
> 4. **V1-4: HRN scraper DD pool extraction at hrn_scraper.py:814.** Verification command: `sed -n '810,820p' backend/services/data_sources/hrn_scraper.py`. Paste verbatim output. Per Tony's Item 2 ratification: CC determines whether root cause is identical to V1-3 or distinct, surfaces FRAMEWORK_GAP if collapse-or-stand decision needed.
> 5. **V1-5: equine-ingestion handler default-case dispatch path.** Verification command: `sed -n '1665,1685p' backend/lambdas/ingestion/handler.py` (the tail-end default-case region per Architecture Overview § 3.1 V3-2 sub-citation). Paste verbatim. Cross-reference Architecture Overview § 3.1 V3-2.
> 6. **V1-6: ls_inference_service.py:388-401 dual-write substrate (F.3 cross-reference).** Verification command: `sed -n '385,405p' backend/services/ls_inference_service.py`. Paste verbatim. Confirms `ON CONFLICT (race_id, entry_id, style)` upsert into `ls_predictions` AND wr_predictions enrichment writes per database_schema_bible:4.1.14 F.3.
> 7. **V1-7: wr_inference_service.py:718-730 dynamic attribute attachment substrate.** Verification command: `sed -n '716,732p' backend/services/wr_inference_service.py`. Paste verbatim. Confirms 9 enrichment fields per Architecture Overview § 4.2.
> 8. **V1-8: backend/services/data_sources/ directory enumeration.** Verification command: `ls -la backend/services/data_sources/`. Paste verbatim. Surfaces chart parser entry point + any other data source modules. Cross-reference for § 4.1.3.
> 9. **V1-9: Chart parser trigger inheritance (per S.3 ratification).** Verification: substrate-determine § 4.1.3 chart parser trigger via direct read of `hrn_scraper.py` (search for chart-parser invocation), `backend/lambdas/ingestion/handler.py` (search for `parse_charts` or analogous admin action), and chart parser entry point (per V1-8 enumeration). Verification commands: `grep -n "chart_parser\|parse_chart\|parseChart" backend/lambdas/ingestion/handler.py backend/services/data_sources/*.py`. Paste verbatim. Determines: (a) `parse_charts` admin action on `equine-ingestion`, (b) S3 ObjectCreated event, (c) chained downstream from another flow. Documented at § 4.1.3 per substrate finding.
> 10. **V1-10: equibase_probe/ production-consumer count = 0 — substrate inheritance.** Verification: read `architecture_overview:3.7` (equine-equibase-acquisition ECR row) + `architecture_overview:3.8` (Secrets Manager 2captcha + brightdata rows). Paste verbatim the relevant table rows. Source-tier: Tier 4 inheritance.
> 11. **V1-11: PHASE_5_BACKLOG.md Phase 5.3.1 entry verbatim.** Verification command: `cat /home/strakajagr/projects/equine-equalizer/docs/bible/PHASE_5_BACKLOG.md`. Paste the Phase 5.3.1 entry verbatim. Confirms operator-verified external source quotes for Bug #28 per META_PLAN v9 Claim 15c pattern.
> 12. **V1-12: NYRA workouts Lambda Active state inheritance.** Verification: read `architecture_overview:3.1` Active table row for `equine-nyra-workouts`. Paste verbatim.
> 13. **V1-13: All Active inference Lambda configurations (WR / PL / LS) inheritance.** Verification: read `architecture_overview:3.1` Active table rows. Paste verbatim.
> 14. **V1-14: Bug #28 cross-reference at § 6 (single occurrence post-draft).** Verification command (post-draft): `grep -c "Bug #28" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md`. Expected: count ≥ 2 (Bug #28 appears at § 6 substantive description + § 8.W.1 entry header at minimum; cross-references throughout § 4.1 sub-sections may add more — CC documents the actual count with decomposition per Lesson § 4.10).
> 15. **V1-15: Three DISABLED EventBridge rules at § 7 substrate.** Verification: read `architecture_overview:3.6` DISABLED table; paste verbatim 3 rule rows.
>
> Additional V1-N entries arise from CC's per-flow substrate reads — one per (flow × table-write), one per (Lambda × State citation), etc. Aim for verification log entries that decompose every aggregable count and cite primary commands. **Every entry pastes verbatim command output per Lesson § 4.10.**
>
> ### Bash-grep verification predictions (Check 9 precision)
>
> Each prediction below distinguishes targeted-by-this-draft from total-on-disk-after-draft:
>
> - **`grep -c "Bug #28" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md` (post-draft)** → expected total ≥ 2 (§ 6 substantive description + § 8.W.1 entry header at minimum). Targeted-by-this-draft: ≥ 2 (CC writes the canonical-home substantive content). CC documents actual total with decomposition.
> - **`grep -c "Phase 5.3.1" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md` (post-draft)** → expected total ≥ 1 (§ 6 + § 8.W.1 entries cite real Phase 5.3.1 identifier per S.1 ratification). Targeted-by-this-draft: ≥ 1.
> - **`grep -c "Phase 5.X.Y" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md` (post-draft)** → expected total ≥ 0 (only F.2 + F.3 cross-references use this placeholder, if any are surfaced; substantive Bug #28 references use real Phase 5.3.1 per S.1 ratification). Targeted-by-this-draft: 0–2 (depending on whether F.2/F.3 cross-references appear in body).
> - **`grep -c "fire-and-fail" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md` (post-draft)** → expected total ≥ 5 (§ 4.1.1, § 4.1.2, § 4.1.6, § 4.1.7 each cite the term per S.4 + S.9 ratifications; § 6 one-line cross-reference cites it; possibly § 4.1.3 if chart parser trigger lands on INACTIVE Lambda). Targeted-by-this-draft: ≥ 5.
> - **`grep -c "architecture_overview:" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md` (post-draft)** → expected total ≥ 20 (per § 4.1.X cross-references to 3.1 + 3.6 + 5.1 + 5.2 + 6 across 9 sub-sections, plus § 1 Scope cross-references, plus § 4.2 Data Acquisition Honesty cross-references). Targeted-by-this-draft: ≥ 20. Verifies S.4 + S.9 cross-reference discipline operative.
> - **`grep -c "database_schema_bible:" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md` (post-draft)** → expected total ≥ 10 (per § 4.1.X destination-table cross-references; F.2 + F.3 cross-references at § 4.1.5; § 1 Scope cross-references). Targeted-by-this-draft: ≥ 10.
> - **`ls /home/strakajagr/projects/equine-equalizer/backend/services/data_sources/`** → expected total: directory listing of data source modules. CC documents actual contents in V1-8 with verbatim output per Lesson § 4.10.
> - **`grep -c "parse_payout" /home/strakajagr/projects/equine-equalizer/backend/services/data_sources/hrn_scraper.py`** → expected total ≥ 3 (parse_payout(1), parse_payout(2), parse_payout(3) at lines 802-804 per Architecture Overview § 1.2 inheritance). CC pastes verbatim grep output.
>
> Each prediction precisely scopes the pattern. Per AUDIT_METHODOLOGY § 4.11: this spec's grep targets are mostly single-file substrate reads (less load-bearing for byte-identity edge cases than D&S Bible's schema.sql + migrations grep). Where multi-file unions are used (e.g., `grep -c parse_payout backend/services/data_sources/*.py`), CC enumerates both distinct-occurrence count and on-disk-match count per § 4.11.
>
> ### Skip-audit pre-approval determination
>
> **Skip-audit does NOT apply.** This is initial v1 full-draft authoring, not a surgical-cosmetic patch cycle. Standard Phase 1 cycle process applies per QB handoff § 6.1: CC drafts → QB reviews + spot-checks → audit-CC adversarial pass → iterate to lock against threshold.
>
> ### Iteration expectation
>
> Per Option 1 with 9 checks operative trajectory expectation: if audit-CC catches NO new QB drafting-spec error class beyond the banked errors, Option 1 is converging.
>
> Tony's lock threshold per META_PLAN v9 § 11 + QB handoff § 6.5: zero fabricated content + zero methodology-interpolation findings + < 5 MATERIAL findings + zero un-closed prior-cycle findings. Data Pipeline Bible v1 has no prior cycle, so the regression check trivializes; the other 3 conditions apply.
>
> ### Closing reminder for CC
>
> 1. Read all 13 reference materials BEFORE drafting.
> 2. Run substrate verifications per V1-1 through V1-15 BEFORE writing per-section content; populate verification log Section C as you go with **verbatim command output per Lesson § 4.10**.
> 3. Surface FRAMEWORK_GAP / SPEC_GAP markers in Section F with substrate-cited candidate reframing per Lesson 4.
> 4. Reproduce QB self-audit log entries char-exact in Section H per QB handoff § 7.2.
> 5. Numeric sub-section IDs only — no provisional letter-prefixes (G-new-1).
> 6. Per Architecture Overview § 5.1 + § 5.2 governance: every § 4.1.X sub-section cites Lambda State + EventBridge target State at the same lock time.
> 7. Per Tony's Item 2 ratification: § 8.W.1 + § 8.W.2 default to separate entries; FRAMEWORK_GAP routing for collapse-or-stand decision via QB → Tony per Lesson § 4.8.
> 8. Cross-references between bibles use section-anchored format (`architecture_overview:3.6`, `database_schema_bible:4.1.12`), NOT literal line numbers (Check 8). Literal line numbers acceptable only for canonical-substrate identification (e.g., `hrn_scraper.py:802-804`).
> 9. Decompose every aggregable count per § 6.5 verification log precision rule.
> 10. EventBridge per-rule target verification inherits from `architecture_overview:3.6`; do NOT re-run `aws events list-targets-by-rule` from drafting CC sandbox per Lesson 5 inheritance discipline.
>
> Begin.

---

## 2. Reference materials and source-priority discipline (QB-side)

This section is QB context for spec authorship discipline. Not part of the CC paste-prompt.

The 13 reference materials enumerated in the paste-prompt § "Reference materials" subsection are the load-bearing substrate inputs. Per Lesson 3 (re-expanded), this drafting spec cites primary verification log claim IDs (V1-N format) AND the underlying primary substrate (file paths, grep commands, locked verification log entries) — NOT paraphrased restatements of META_PLAN or BIBLE_STRUCTURE_SPEC.

Source-priority hierarchy (META_PLAN v9 § 4.5) operative for the bible's content:
1. Live AWS state — for any infrastructure-context claim (inherited via Architecture Overview v3 verification log per Lesson 5 discipline).
2. Live API endpoints — for runtime data state.
3. Live DB state — for data-state claims.
4. Working-tree code (post-baseline 87dec36) — for "what does the scraper / handler / service declare?"
5. Operator-stated history — for "why decisions were made" (Bug #28 operator memory file inherits via PHASE_5_BACKLOG.md Phase 5.3.1).
6. EE_CURRENT_STATE_DUMP.md — best-available baseline only.
7. Session logs — tertiary.

The Data Pipeline Bible draws primarily from Tier 4 (working-tree scraper / handler / service code) and inherited Tier 1 (AWS state via Architecture Overview v3). Tier 5 (Bug #28 operator memory file) inherits via PHASE_5_BACKLOG.md Phase 5.3.1.

---

## 3. Operating disciplines CC must follow (QB-side)

Spec authorship discipline ratifies the CC operating disciplines enumerated in the paste-prompt's "Verification discipline" + "Methodology lessons + active discipline" subsections. These map to the 9-check Option 1 framework + Check 7 + Check 8 from Architecture Overview v3 cycle:

- Substrate verification cluster (Checks 1–3): cross-reference accuracy, count/arithmetic accuracy, substrate-grounded reframing.
- Content verification cluster (Checks 4–6): definition-framing internal consistency, synthesis verification, audit-CC enumeration completeness.
- Workflow verification cluster (Checks 7–9): mid-cycle scope extension narrative discipline, line-shift-resistant citations, bash-grep prediction precision.

Each check is operative on QB during spec authorship; the spec's § 11 (QB substrate-verification log) is the audit-trail.

Active discipline additions for this cycle:
- AUDIT_METHODOLOGY § 4.8 — QB substrate findings during spec authorship require Tony ratification (operationalized via S.1–S.9 ratification-routing this cycle).
- AUDIT_METHODOLOGY § 4.9 — QB review pass is light surface review only.
- AUDIT_METHODOLOGY § 4.10 — Verbatim-paste discipline for V1-N entries (HARD RULE in CC paste-prompt).
- AUDIT_METHODOLOGY § 4.11 — V1-N grep predictions against unions of files account for byte-identity edge cases (less load-bearing this cycle; applied where multi-file grep predictions exist).

---

## 4. Prescribed TOC and per-section drafting guidance (QB-side substrate anchors)

The paste-prompt's "Prescribed TOC" + "Per-section content requirements" subsections reproduce BIBLE_STRUCTURE_SPEC v6 § 6.2 normatively. QB substrate anchoring confirms:

| Anchor | Substrate-verified | Source |
|---|---|---|
| 13 EventBridge rules (10 ENABLED + 3 DISABLED) | ✅ inherited via Architecture Overview v3 § 3.6 | QB read of architecture_overview.md |
| 5 ECS Fargate task families | ✅ inherited via Architecture Overview v3 § 3.2 | QB read of architecture_overview.md |
| 9 § 4.1 sub-sections (10 ENABLED rules across 9 with § 4.1.5 holding 3, § 4.1.3 holding 0) | ✅ § 6.2 prescribed TOC + S.3 cardinality decision | QB read of BIBLE_STRUCTURE_SPEC v6 § 6.2 + Architecture Overview § 3.6 mapping |
| Bug #28 column-shift at hrn_scraper.py:802-804 | ⚠️ V1-3 (CC reads working-tree directly) | QB cannot read EE codebase per workflow constraint; CC verifies |
| Bug #28 DD pool nuance at hrn_scraper.py:814 | ⚠️ V1-4 (CC reads + determines root-cause disposition per Item 2 ratification) | CC verifies |
| equine-ingestion default-case dispatch (handler.py:1669-1680) | ✅ inherited via Architecture Overview § 3.1 V3-2 | Architecture Overview v3 verification log |
| ls_inference_service.py:388-401 dual-write (F.3) | ✅ inherited via database_schema_bible:4.1.14 F.3 | D&S Bible v1 verification log |
| wr_inference_service.py:718-730 dynamic attribute attachment | ✅ inherited via Architecture Overview § 4.2 | Architecture Overview v3 |
| PHASE_5_BACKLOG.md Phase 5.3.1 entry | ✅ direct read by QB during Phase B | QB read of PHASE_5_BACKLOG.md |
| Operator memory file Bug #28 verbatim quotes | ✅ inherited via PHASE_5_BACKLOG.md Phase 5.3.1 per Claim 15c pattern | QB read of PHASE_5_BACKLOG.md |

Items marked ⚠️ are CC-verified at draft time per Tier 4 source-priority; QB does not read EE codebase per workflow constraint (acknowledged 2026-05-06 hard reset).

---

## 5. Verification log structure (QB-side)

The paste-prompt's "Companion verification log structure" subsection prescribes the Section A–I structure per QB handoff § 7.2. QB-side note: Section A inherits from META_PLAN v9 verification log + Architecture Overview v3 verification log + Database & Schema Bible v1 verification log; Section B is empty (v1 first cycle); Section C is the new V1-N entries with verbatim paste discipline per § 4.10; Section D self-audit target ZERO; Section E pattern-completion preserves W.N exclusivity; Section F surfaces gaps with candidate reframing (FRAMEWORK_GAP F.X for § 8.W.1/§ 8.W.2 collapse-or-stand decision is the expected location if root-cause-identical substrate determination); Section G empty (v1 first cycle); Section H reproduces this spec's § 6 char-exact; Section I empty (full draft, not surgical patch).

---

## 6. QB self-audit log Section H entries (reproduced char-exact in CC's verification log Section H)

The 9 entries below are the Option 1 self-audit log for QB's spec authorship cycle. CC reproduces these char-exact in the verification log Section H per QB handoff § 7.2.

### H1 — Check 1 (cross-reference accuracy) self-audit

**Cross-references prescribed in this spec verified against substrate:**

- BIBLE_STRUCTURE_SPEC v6 § 6.2 → verified by QB direct read 2026-05-06; section spans from `### 6.2 data_pipeline_bible.md` header to `### 6.3 feature_provenance_bible.md (FF1)` header. Per-section guidance read in full.
- BIBLE_STRUCTURE_SPEC v6 § 5.3 (cross-cutting bug scope rule) → verified.
- BIBLE_STRUCTURE_SPEC v6 § 5.5 + § 5.6 → verified.
- BIBLE_STRUCTURE_SPEC v6 § 5.5.1 (global Bug #N convention) → verified.
- BIBLE_STRUCTURE_SPEC v6 § 5.7 (candidate roster workflow) → verified.
- META_PLAN v9 § 4.5 → verified.
- META_PLAN v9 § 6.5 → verified.
- META_PLAN v9 § 7.3 placeholder-resolution sub-rule → verified; locked v7.
- META_PLAN v9 § 7.9 Data Acquisition Honesty Protocol → verified.
- META_PLAN v9 Appendix A.5 Bug #28 worked example → verified.
- AUDIT_METHODOLOGY v2 § 4.8 / 4.9 / 4.10 / 4.11 → verified at primary source 2026-05-06; slot numbers match handoff per Lesson 3 expansion.
- Architecture Overview § 3.1 (Lambda inventory + V3-2 25-action sub-citation + default-case dispatch) → verified.
- Architecture Overview § 3.2 (5 ECS task families) → verified.
- Architecture Overview § 3.6 (13 EventBridge rules + per-rule targets + 4 fire-and-fail anomaly) → verified.
- Architecture Overview § 4.2 (per-pipeline prediction shapes + WR dynamic attribute attachment) → verified.
- Architecture Overview § 5.1 + § 5.2 (Forbidden Pattern + Common Mistake governing § 4.1.X documentation discipline) → verified.
- Architecture Overview § 6 (fire-and-fail anomaly canonical home) → verified.
- Database & Schema Bible § 4.1 (per-table sub-sections; F.2 at 4.1.12 + 4.1.13; F.3 at 4.1.14) → verified.
- PHASE_5_BACKLOG.md Phase 5.3.1 entry → verified by QB direct read 2026-05-06.

### H2 — Check 2 (count/arithmetic accuracy) self-audit

**Counts decomposed per META_PLAN v9 § 6.5 verification log precision rule:**

- 13 EventBridge rules = 10 ENABLED + 3 DISABLED. ENABLED decomposition: 4 fire-and-fail (3 → equine-ingestion: ingestion-daily + fetch-results-nightly + angle-stats-nightly; 1 → equine-results: results-daily) + 4 active-Lambda (ls-inference-daily, nyra-workouts-daily, pl-inference-daily, wr-inference-daily) + 2 ECS (daily-retrain-full, weekly-retrain-wr). 4+4+2=10. DISABLED: feature-engineering-daily, inference-daily, weekly-retrain-pl. 10+3=13.
- 9 § 4.1 sub-sections per § 6.2 prescribed TOC. EventBridge rule cardinality per sub-section: 1+1+0+1+3+1+1+1+1=10 (matches 10 ENABLED). § 4.1.5 holds 3 rules (WR/PL/LS); § 4.1.3 holds 0 direct EventBridge rules (chart parser trigger TBD per V1-9).
- 5 ECS Fargate task families: equine-training, equine-training-daily-full, equine-training-manual, equine-training-pl, equine-training-win-prob.
- 6 Data Acquisition Honesty sources per § 6.2: HRN entries, HRN results, HRN workouts, NYRA workouts, Equibase chart parser, equibase_probe/.
- 25 action handlers on equine-ingestion = 5 data acquisition + 4 model lifecycle + 5 admin/diagnostic + 7 data backfills/ops + 3 originally-cited admin + 1 health (per Architecture Overview § 3.1 V3-2 sub-citation).

Single-source citation: each count statement above traces to a specific upstream-locked verification log claim or this spec's V1-N. No multi-paraphrase counts.

### H3 — Check 3 (substrate-grounded reframing) self-audit

**Reframings introduced in this spec are substrate-grounded:**

- Bug #28 canonical home in this bible per BIBLE_STRUCTURE_SPEC v6 § 5.3 (data-acquisition discipline most directly prevents recurrence) — verified by QB direct read of § 5.3 + META_PLAN v9 Appendix A.5.
- § 8.W.1 + § 8.W.2 default to separate entries per § 6.2 + Tony's Item 2 ratification 2026-05-05 — verified by QB read of handoff document Item 2 ratification.
- Phase 5.3.1 real identifier (NOT placeholder) per S.1 ratification — verified by QB direct read of PHASE_5_BACKLOG.md (file exists; Bug #28 entered at Phase 5.3.1).
- Fire-and-fail anomaly canonical home is `architecture_overview:6` (cross-runtime invariant); this bible's § 6 carries one-line cross-reference per S.4 ratification — verified by QB direct read of Architecture Overview § 5.1 + § 5.2 + § 6.
- F.2 + F.3 cross-references at § 4.1.5 daily inference flow per S.6 ratification — verified by QB direct read of database_schema_bible:4.1.12 + § 4.1.13 + § 4.1.14 substrate.
- § 4.1.5 holds 3 EventBridge rules (WR/PL/LS) under one § 4.1 sub-section per § 6.2 prescribed TOC; § 4.1.3 chart parser holds 0 direct EventBridge rules (trigger TBD per V1-9) — verified by QB direct read of § 6.2 + cross-mapping to Architecture Overview § 3.6.

### H4 — Check 4 (definition-framing internal consistency) self-audit

**Definitions and enumerations reconcile internally:**

- § 2 Definitions enumerated terms (HRN, NYRA, Equibase chart, qualifying track, default-case dispatch, fire-and-fail) match § 4.1 sub-section content (HRN sources at 4.1.1/4.1.2/4.2.1/4.2.2/4.2.3; NYRA at 4.1.4/4.2.4; Equibase chart at 4.1.3/4.2.5; default-case dispatch at 4.1.1/4.1.2; fire-and-fail at 4.1.1/4.1.2/4.1.6/4.1.7).
- 10 ENABLED EventBridge rules in § 4.1 reconcile with 10 ENABLED in Architecture Overview § 3.6 (4+4+2 decomposition); 3 DISABLED rules at § 7 reconcile with 3 DISABLED in Architecture Overview § 3.6.
- 9 § 4.1 sub-sections reconcile with § 6.2 prescribed TOC; § 4.1.5 cardinality of 3 rules + § 4.1.3 cardinality of 0 direct rules sum to 10 ENABLED across 9 sub-sections (1+1+0+1+3+1+1+1+1=10).
- § 4.2 Data Acquisition Honesty 6 sources reconcile with § 6.2 prescribed TOC.

No internal contradiction between § 2 / § 4.1 / § 4.2 enumerations.

### H5 — Check 5 (synthesis verification) self-audit

**Synthesis-introduced upstream corrections substrate-verified:**

- The handoff cross-reference inaccuracies (PHASE_5_BACKLOG.md non-existence; Check 7 + Check 8 enumeration completeness) are surfaced as QB-side findings (§ 10) NOT propagated as upstream corrections to META_PLAN v9 / Architecture Overview / Database & Schema Bible. Per Lesson 6: substrate-verified at QB direct read.
- Bug #28 canonical-home assignment inherited from META_PLAN v9 § 1.2 + Appendix A.5 + BIBLE_STRUCTURE_SPEC v6 § 5.3 — QB substrate-verified.
- Fire-and-fail anomaly canonical home assignment inherited from Architecture Overview § 6 self-assignment (per § 5.1 + § 5.2 ratifications) — QB substrate-verified.
- F.2 + F.3 cross-reference targets (database_schema_bible:4.1.12 + § 4.1.14) — QB substrate-verified.
- § 5 candidate Common Mistake (producer-side parent-row verification) inherited from D&S Bible Q3.3.c forward-deferral note at database_schema_bible.md § 5 lead paragraph — QB substrate-verified.

### H6 — Check 6 (audit-CC enumeration completeness) self-audit

**Audit-CC enumeration inherited inventory per Check 6:**

- v1 first cycle has no prior audit-CC findings to inherit. Forward-looking: when v2 audit-CC enumerates findings, QB substrate-verifies each via grep before re-spec.
- For inherited substrate from upstream Phase 1 deliverables (Architecture Overview v3 + D&S Bible v1): QB direct read confirms Architecture Overview § 3.6 13-rule × per-rule-target verification (locked Lesson 5 inheritance), § 3.1 25-action V3-2 sub-citation, D&S Bible F.2 + F.3 substrate. No drift surfaced at spec-authorship.

### H7 — Check 7 (mid-cycle scope extensions) self-audit

**No mid-cycle scope extensions in this spec.** The spec authors v1 in a single pass. Forward-looking: if v2/v3 cycles extend scope post-CC-surfacing, QB enumerates ALL verification-log + main-doc sections referencing original scope and updates each per Check 7 discipline (banked Architecture Overview v3 H7).

For this v1 spec specifically, the spec is the initial scope; no Section H/I sub-section updates required.

### H8 — Check 8 (line-shift-resistant citations) self-audit

**Line-number citations replaced with section-anchored citations:**

- `architecture_overview:3.1` for Lambda inventory cross-references, NOT Architecture Overview line numbers.
- `architecture_overview:3.2` for ECS task families.
- `architecture_overview:3.6` for EventBridge schedule + per-rule targets.
- `architecture_overview:5.1` + `architecture_overview:5.2` for Forbidden Pattern + Common Mistake governance.
- `architecture_overview:6` for fire-and-fail anomaly canonical home.
- `database_schema_bible:4.1.<table>` for per-table cross-references.
- `database_schema_bible:4.1.12` + `database_schema_bible:4.1.13` for F.2 cross-reference targets.
- `database_schema_bible:4.1.14` for F.3 cross-reference target.
- BIBLE_STRUCTURE_SPEC `v6 § 6.2` (section anchor).
- META_PLAN `v9 § 4.5` / `v9 § 6.5` / `v9 § 7.3` / `v9 § 7.9` / Appendix A.5.
- AUDIT_METHODOLOGY `§ 4.8` / `§ 4.9` / `§ 4.10` / `§ 4.11`.

Literal line numbers retained ONLY where canonical-substrate identification requires them:
- `hrn_scraper.py:802-804` — Bug #28 column-shift defect surface; canonical-substrate identification per the v3 final-lock H8 lesson scope.
- `hrn_scraper.py:814` — Bug #28 DD pool nuance; canonical-substrate identification.
- `backend/lambdas/ingestion/handler.py:94` — refresh_angle_stats handler; canonical-substrate identification per Architecture Overview § 3.1 + § 3.6 inheritance.
- `backend/lambdas/ingestion/handler.py:1669-1680` — default-case dispatch path per Architecture Overview § 3.1 V3-2 inheritance; canonical-substrate identification.
- `wr_inference_service.py:718-730` — dynamic attribute attachment block per Architecture Overview § 4.2 inheritance; canonical-substrate identification.
- `ls_inference_service.py:388-401` — dual-write substrate per database_schema_bible:4.1.14 F.3 inheritance; canonical-substrate identification.
- Migration file paths cite the filename, not line numbers.

Cross-references between bibles use section IDs only; canonical-substrate citations to source code may include line numbers when tightly scoped.

### H9 — Check 9 (bash-grep verification predictions) self-audit

**Prescribed bash-grep predictions distinguish targeted vs total counts:**

Per spec § 7 "Bash-grep verification predictions (Check 9 precision)":
- `grep -c "Bug #28" data_pipeline_bible.md` (post-draft) → expected total ≥ 2; targeted-by-this-draft: ≥ 2.
- `grep -c "Phase 5.3.1" data_pipeline_bible.md` (post-draft) → expected ≥ 1; targeted: ≥ 1.
- `grep -c "Phase 5.X.Y" data_pipeline_bible.md` (post-draft) → expected ≥ 0; targeted: 0–2.
- `grep -c "fire-and-fail" data_pipeline_bible.md` (post-draft) → expected ≥ 5; targeted: ≥ 5.
- `grep -c "architecture_overview:" data_pipeline_bible.md` (post-draft) → expected ≥ 20; targeted: ≥ 20.
- `grep -c "database_schema_bible:" data_pipeline_bible.md` (post-draft) → expected ≥ 10; targeted: ≥ 10.
- `ls backend/services/data_sources/` → expected: directory listing.
- `grep -c "parse_payout" backend/services/data_sources/hrn_scraper.py` → expected ≥ 3.

Each prediction precisely scopes the pattern. Per AUDIT_METHODOLOGY § 4.11: this spec's grep targets are mostly single-file substrate reads; multi-file unions enumerate distinct-occurrence-count + on-disk-match-count where applied.

---

## 7. Bash-grep verification predictions (Check 9 precision; QB-side reproduced)

Reproduced for traceability. Same content as paste-prompt § "Bash-grep verification predictions (Check 9 precision)" subsection.

---

## 8. Skip-audit pre-approval determination (QB-side)

Skip-audit does NOT apply per spec § 1.1 paste-prompt "Skip-audit pre-approval determination" subsection. Standard Phase 1 cycle process applies.

---

## 9. Iteration expectation (QB-side)

Per Option 1 9-check + Check 7 + Check 8 trajectory expectation, this v1 cycle tests whether the now-11-check framework converges. Banked outcomes:

- v1 audit clean against threshold → bible locks v1; Option 1 declared converging at this measurement.
- v1 audit returns ≥ 1 new QB drafting-spec error class beyond the existing checks → bank as Check 12 (per Lesson 12-banking workflow consistent with H7/H8 banking precedent).
- v1 audit returns 0–4 MATERIAL findings within the existing check coverage → standard surgical-patch cycle.
- v1 audit returns ≥ 5 MATERIAL OR ≥ 1 BLOCKER → REVISE AND RE-AUDIT or SUBSTANTIAL REWORK per QB handoff § 6.5.

---

## 10. Handoff cross-reference corrections (banked Check 1 + Check 6 findings)

QB substrate-verification surfaced 2 inaccuracies in the QB handoff document. Banked here for transparency; spec content corrects them; future handoff-document cycles can incorporate the corrections. Both ratified by Tony 2026-05-06 per S.1 + S.2.

### 10.1 Handoff § 8.5 + § 8.6: PHASE_5_BACKLOG.md non-existence claim

**STATUS: REFUTED.** QB direct read of `/home/strakajagr/projects/equine-equalizer/docs/bible/PHASE_5_BACKLOG.md` 2026-05-06 confirms the file EXISTS on disk:
- Created 2026-05-04 (predates D&S Bible lock 2026-05-05 by ~24h).
- ACTIVE status per `TRIAGE_QUEUE_SPEC v1` § 4.3 transfer mechanism.
- Bug #28 entered at **Phase 5.3.1** with full TRIAGE_QUEUE_SPEC v1 § 3 fields: Severity (MATERIAL), Surfaced date (2026-05-03), Stable-known classification (provisional), Root cause, Manifestation, Operator-verified external source (verbatim quotes per Claim 15c pattern), Dependencies, Re-classification trigger, Audit-cycle reference, Disposition, Rollback, Bible references on resolution, Status (open), Created date.

Handoff § 8.5 claims F.2/F.3 "queue for PHASE_5_BACKLOG.md at Phase 0 exit"; § 8.6 claims "as of Database & Schema Bible v1 lock (2026-05-05), PHASE_5_BACKLOG.md does NOT yet exist on disk." Both REFUTED.

**Spec correction (per S.1 ratification):**
- Spec instructs drafting CC to cite **real `Phase 5.3.1`** for Bug #28 cross-reference (not `Phase 5.X.Y` placeholder).
- F.2 + F.3 cross-references continue to use `Phase 5.X.Y` placeholder per META_PLAN v9 Appendix A lead-paragraph scope clause (placeholder resolves when those specific entries land in PHASE_5_BACKLOG.md as separate triage queue entries).

### 10.2 Handoff § 4 enumeration of "10 banked QB drafting-spec errors": missed Check 7 + Check 8

**STATUS: INCOMPLETE.** QB direct read of `architecture_overview_v3_verification.md` Section H 2026-05-06 confirms:
- H7 (Check 7 — mid-cycle scope extensions touch all narrative-referencing sections) banked 2026-05-05 per v3 final-lock surgical patch.
- H8 (Check 8 — line-shift-resistant citations replace literal line numbers) banked 2026-05-05; **operative starting Database & Schema Bible spec, carries forward to this Data Pipeline Bible cycle**.

Handoff § 4 enumerates "10 banked QB drafting-spec errors" but does not surface H7 + H8 banking. Both checks are operative active discipline for this cycle.

**Spec correction (per S.2 ratification):**
- Spec § 1.1 paste-prompt § "Methodology lessons + active discipline" enumerates Check 7 + Check 8 explicitly as banked discipline (items 11 + 12 in the discipline list).
- Spec § 6 H7 + H8 self-audit entries reproduced char-exact in CC's verification log Section H per QB handoff § 7.2.
- Iteration expectation (§ 9) updated to reflect 11-check framework (9 + 2 banked from Architecture Overview v3 cycle).

---

## 11. QB substrate-verification log (Option 1 9-check + 2 banked self-audit; QB-side authoritative record)

This section is the QB-side authoritative record of substrate verifications run during spec authorship. Sections 6.H1 through 6.H9 reproduce content from this log.

### 11.1 Substrate verifications run by QB

| Anchor | Command (or read) | Result | Used in spec § |
|---|---|---|---|
| AUDIT_METHODOLOGY § 4.8 / 4.9 / 4.10 / 4.11 slot numbers | direct read of /home/strakajagr/.../AUDIT_METHODOLOGY.md | Confirmed at primary source 2026-05-06 | Lesson 3 expansion compliance |
| BIBLE_STRUCTURE_SPEC v6 § 6.2 prescribed TOC | direct read of /home/strakajagr/.../BIBLE_STRUCTURE_SPEC.md | 9 sub-sections + § 4.2 6 sources + § 5–8 mandatory | § 4 prescribed TOC |
| BIBLE_STRUCTURE_SPEC v6 § 5.3 cross-cutting bug scope rule | direct read | Verified canonical-home + non-canonical-home semantics | § 4.1.X impaired-flow + § 6 cross-references |
| Architecture Overview v3 § 3.1 + § 3.2 + § 3.6 + § 4.2 + § 5.1 + § 5.2 + § 6 | direct read of architecture_overview.md | Verified all inheritance substrate | § 4.1 per-flow cross-references |
| Architecture Overview v3 verification log Section H7 + H8 | direct read of architecture_overview_v3_verification.md | H7 + H8 banking confirmed; operative for this cycle | § 10.2 + Check 7 + Check 8 inheritance |
| Database & Schema Bible v1 § 4.1.12 + § 4.1.13 + § 4.1.14 | direct read of database_schema_bible.md | F.2 + F.3 substrate context confirmed | § 4.1.5 daily inference flow F.2 + F.3 cross-references |
| Database & Schema Bible v1 § 5 forward-deferral note (Q3.3.c) | direct read | Producer-side parent-row verification candidate Common Mistake inherited | § 5.2 candidate roster |
| PHASE_5_BACKLOG.md existence + Phase 5.3.1 entry | direct read of PHASE_5_BACKLOG.md | File exists (created 2026-05-04); Bug #28 entered with full TRIAGE_QUEUE_SPEC v1 § 3 fields | § 10.1 + S.1 ratification routing |
| BIBLE_STRUCTURE_SPEC v6 § 5.5.1 global Bug #N convention | direct read | Monotonic + never-reused; cross-bible reference uses #<bug-id> | § 8.W.2 Bug #N TBD routing per Item 2 |
| META_PLAN v9 § 7.3 placeholder-resolution sub-rule | direct read | Forward-looking placeholder applies for unfixed Bug #28 W.N entries | § 8.W.1 + § 8.W.2 Fix date placeholders |
| META_PLAN v9 § 7.9 Data Acquisition Honesty Protocol | direct read | 6-source mandatory fields confirmed | § 4.2 prescribed TOC |
| META_PLAN v9 Appendix A.5 Bug #28 worked example | direct read | Substrate-grounded Bug #28 framing inherited | § 4.1.2 + § 8.W.1 substrate |

### 11.2 Substrate verifications NOT runnable from QB (CC verifies)

Per the 2026-05-06 hard-reset workflow, QB does not read EE codebase. The following V1-N entries CC verifies at draft time:

| Anchor | CC verification command | Used in spec |
|---|---|---|
| hrn_scraper.py:802-804 verbatim | `sed -n '798,808p' backend/services/data_sources/hrn_scraper.py` | V1-3 |
| hrn_scraper.py:814 verbatim | `sed -n '810,820p' backend/services/data_sources/hrn_scraper.py` | V1-4 |
| equine-ingestion default-case dispatch verbatim | `sed -n '1665,1685p' backend/lambdas/ingestion/handler.py` | V1-5 |
| ls_inference_service.py:388-401 verbatim | `sed -n '385,405p' backend/services/ls_inference_service.py` | V1-6 |
| wr_inference_service.py:718-730 verbatim | `sed -n '716,732p' backend/services/wr_inference_service.py` | V1-7 |
| backend/services/data_sources/ directory listing | `ls -la backend/services/data_sources/` | V1-8 |
| Chart parser trigger inheritance | grep + ls per V1-9 commands | V1-9 |

### 11.3 Pattern-completion check (W.N exclusivity)

Spec authoring introduces ZERO new letter-prefixes. W.N remains the only ratified letter-prefix per BIBLE_STRUCTURE_SPEC v6 § 5.5. Cross-reference syntax extensions: NONE introduced beyond the existing `<bible>:#<bug-id>`. Numeric sub-section IDs operative for § 5 candidate roster per G-new-1.

### 11.4 Methodology-interpolation self-check

Spec authoring introduces ZERO CC-prescribed methodology constructs Tony has not explicitly ratified. The 9-check framework + Check 7 + Check 8 + Lessons 1–6 + AUDIT_METHODOLOGY § 4.8/4.9/4.10/4.11 are all upstream-ratified. The CONDITIONAL trigger application in § 8.W.1 / § 8.W.2 / § 7 (G7 closure) is upstream-ratified. The G-new-1 numeric-IDs-for-candidates rule is Tony-locked per BIBLE_STRUCTURE_SPEC v6 § 5.7.

The Bug #N TBD routing for § 8.W.2 (per Tony's Item 2 ratification) is operator-ratified, NOT a CC-introduced methodology construct.

### 11.5 FRAMEWORK_GAP / SPEC_GAP markers

ZERO surfaced in this spec. The handoff cross-reference inaccuracies surfaced in § 10 are downstream-synthesis errors (the handoff document itself), NOT framework-level gaps in the bible's spec premise OR slot structure. They route to the spec's content correction and to a future handoff-document update — NOT to FRAMEWORK_GAP routing.

Forward-looking: drafting CC may surface FRAMEWORK_GAP F.X for § 8.W.1 / § 8.W.2 collapse-or-stand decision per Tony's Item 2 ratification routing. That is the expected location for the Bug #28 DD pool nuance disposition.

### 11.6 Distinctness test for new banked checks

This spec does NOT bank any new checks. The framework remains 9-check Substrate (1–3) / Content (4–6) / Workflow (7–9) + Check 7 + Check 8 banked from Architecture Overview v3 cycle = 11 checks operative. No Check 12 surfaced during spec authorship. Forward-looking: if v1 audit-CC catches a new QB drafting-spec error class, evaluate whether it fits an existing check's coverage or warrants a Check 12.

### 11.7 Workflow-discipline self-check (banked 2026-05-06 per QB workflow drift)

QB workflow drift surfaced twice during this cycle's spec authorship:
1. QB substrate-verification overreach (running EE codebase reads as pre-spec verification rather than specifying CC V1-N work).
2. QB MCP write_file overreach (writing spec to disk rather than producing chat output for Tony mediation).

Per Tony's hard-reset 2026-05-06: QB outputs are chat messages; CC does all disk operations including spec writes. Lesson banking for AUDIT_METHODOLOGY routes via patch-CC after Tony ratification (chat-only QB output proposing slot + lesson content).

This self-check is QB-side audit-trail; Section H reproduces H1–H9 char-exact (no H10 added — workflow-discipline is QB role definition, not a Phase 1 verification check).

---

**End of Data Pipeline Bible v1 Drafting Spec.**

Spec authored under Option 1 with 9 checks operative across 3 clusters + Check 7 + Check 8 banked active discipline. QB substrate-verification log at § 11. Handoff cross-reference corrections banked at § 10. CC paste-prompt at § 1.1.

**Tony's next action:** review this spec. If approved, route to spec-write CC paste-prompt (separate chat block) for disk routing; then route to drafting CC paste-prompt for bible authorship.
