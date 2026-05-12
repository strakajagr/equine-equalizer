# Data Pipeline Bible

Document: data_pipeline_bible
Phase: 1 (Bible) — deliverable 3 of 7 (drafting-order numbering per BIBLE_STRUCTURE_SPEC v6 § 8.2)
Status: LOCKED v1-patched-d (2026-05-11) — locked via cross-bible re-lock ceremony at parent EE Bible Upstream-Correction Cycle exit per R14.3 Option B + R36 Option A; cohort-locked audit-CC RATIFY disposition; Finding 1 § 4.1.4 closure substrate-grounded (§ 4.2.4 deferred to Phase A re-dispatch per R14.2 Option A); supersedes LOCKED v1-patched-c (2026-05-06)
Author: CC (v1-patched-c: drafting under Tier 3 verification discipline; v1-patched-d: drafting under EE Bible Upstream-Correction Cycle sub-cycle 2 of 4 per R10 Option A 4th sub-cycle authorization; QB orchestrated)
Date: 2026-05-06

## Revision history

- v1 (2026-05-06): initial CC draft per BIBLE_STRUCTURE_SPEC v6 § 6.2 + Data Pipeline Bible v1 Drafting Spec (2026-05-06). Tier: 3 per META_PLAN v9 § 4.1 + § 6.5. Companion verification log at `_audit/data_pipeline_bible_v1_verification.md`. Anchored on: META_PLAN v9 (LOCKED 2026-05-05) + BIBLE_STRUCTURE_SPEC v6 (LOCKED 2026-05-05) + AUDIT_METHODOLOGY v2 (LOCKED 2026-05-05) + Architecture Overview v3 (LOCKED 2026-05-05) + Database & Schema Bible v1-patched-d1 (LOCKED 2026-05-05) + PHASE_5_BACKLOG.md (CREATED 2026-05-04; ACTIVE).
- v1-patched (2026-05-06): surgical patch closing F.1 (FRAMEWORK_GAP — § 8.W.1 / § 8.W.2 collapse-or-stand decision) per Tony's Option 3 ratification 2026-05-06. § 8.W.2 stands as separate entry; Bug #N assignment + collapse-vs-stand disposition deferred to Phase 5.3.1 fix-time substrate verification. See verification log § F.1 closure note.
- v1-patched-a (2026-05-06): surgical patch closing audit-CC v1-patched audit findings A1 (BLOCKER — V1-9 fabricated paste rewritten with verbatim stdout), A2 (MATERIAL — verification log Section C/E/F.1 narrative-referencing sections updated to post-patch state), A3 (MATERIAL — angle_stats substrate gap surfaced as FRAMEWORK_GAP F.4 in verification log § F; UPSTREAM-CORRECTION routed to D&S Bible patch cycle separately), A4 (MATERIAL — V1-1 + V1-15 ellipsis-truncated rows re-pasted in full), A5 (MATERIAL — § 4.2.1 + § 4.2.3 + § 4.2.4 empirical-discipline reframing per Option C hybrid: dashboard endpoint queries + NYRA endpoint curl + asserted-not-empirical fallback), plus MINOR A7/A8/A9 + STYLE A10/A11. See verification log § G (audit-finding closure verification) for per-finding closure substrate.
- v1-patched-b (2026-05-06): surgical patch closing re-audit-CC v1-patched-a audit findings B1 (MATERIAL — § 4.2.1 ASSERTION_CLAUSE cross-reference per § 4.2.2 → per § 4.2.3 correction; resolves to substantive Bug #7 documentation in this bible per re-audit recommendation Option (a)), B2 (MINOR — F.1 FRAMEWORK_GAP marker format normalized [FRAMEWORK_GAP] → <FRAMEWORK_GAP: ...> per META_PLAN v9 § 6.5), B4 (STYLE — EOF marker text updated to post-lock state). B3 + B5 deferred to Phase 1 cleanup-cycle backlog per Tony's Decision 1 ratification 2026-05-06. Skip-audit ratified for this patch scope; bible re-locks at v1-patched-b after this patch lands clean (no third audit cycle).
- v1-patched-b LOCKED (2026-05-06): Phase 1 deliverable 3 of 7 LOCKED. Skip-audit ratified by Tony per re-audit-CC v1-patched-a recommendation LOCK AFTER SPECIFIC MINOR REVISIONS; B1 + B2 + B4 closed in v1-patched-b surgical patch; B3 + B5 deferred to Phase 1 cleanup-cycle backlog. All threshold conditions PASS (zero fabricated content; zero methodology-interpolation; 1 MATERIAL B-finding < 5 floor; 11 of 11 prior-cycle findings CLOSED). Bible joins Architecture Overview v3 LOCKED (2026-05-05) + Database & Schema Bible v1-patched-d1 LOCKED (2026-05-05) as locked Phase 1 substrate. F.4 (angle_stats out-of-band substrate gap) remains open in this bible's verification log § F.4 with UPSTREAM-CORRECTION pending separate D&S Bible v1-patched-d2 patch cycle (does not block this bible's lock). § 8.W.2 disposition (collapse-or-stand + Bug #N assignment) deferred to Phase 5.3.1 fix-time substrate verification; bible re-ratifies via patch when fix lands.
- v1-patched-c (2026-05-06): surgical patch closing F.4 (FRAMEWORK_GAP — `angle_stats` out-of-band substrate gap) per UPSTREAM-CORRECTION close. D&S Bible v1-patched-d2 LOCKED 2026-05-06 landed `angle_stats` substrate at `database_schema_bible:4.1.15`. § 4.1.7 destination-table cross-reference re-ratified to point at the new D&S Bible slot (replaces the prior "see FRAMEWORK_GAP F.4" deferred-pending-UPSTREAM-CORRECTION text). Verification log § F.4 receives closure note. Skip-audit ratified by Tony per the surgical pointer-update class scope. Bible re-locks at v1-patched-c LOCKED via subsequent lock-CC paste-prompt; supersedes v1-patched-b LOCKED state (2026-05-06 earlier today).
- v1-patched-c LOCKED (2026-05-06): Phase 1 deliverable 3 of 7 re-LOCKED. UPSTREAM-CORRECTION close: F.4 (FRAMEWORK_GAP — `angle_stats` out-of-band substrate gap) closed via D&S Bible v1-patched-d2 LOCKED (2026-05-06). § 4.1.7 destination-table cross-reference re-ratified to point at `database_schema_bible:4.1.15` (replaces prior "see FRAMEWORK_GAP F.4" deferred-pending-UPSTREAM-CORRECTION text). Verification log § F.4 receives closure note. Skip-audit ratified by Tony per the surgical pointer-update class scope. Bible joins Architecture Overview v3 LOCKED (2026-05-05) + Database & Schema Bible v1-patched-d2 LOCKED (2026-05-06) as locked Phase 1 substrate; v1-patched-c lock supersedes v1-patched-b LOCKED state (2026-05-06 earlier today). § 8.W.2 disposition (collapse-or-stand + Bug #N assignment) remains deferred to Phase 5.3.1 fix-time substrate verification per Tony's Option 3 ratification 2026-05-06; bible re-ratifies via patch when fix lands. Phase 1 deliverable 3 of 7 LOCKED — final operation of session 2026-05-06.

- v1-patched-d (2026-05-11): UPSTREAM-CORRECTION patch cycle Data Pipeline Bible UC (sub-cycle 2 of 4 under parent EE Bible Upstream-Correction Cycle, per R10 Option A 4th sub-cycle authorization 2026-05-11). Origin: parent cycle Finding 1 (this bible's § 4.1.4 + § 4.2.4 NYRA disposition "currently functional" claim substrate-refuted by 7+ day zero-result scrapes pre-OCRC) was original cycle-entry trigger. Scope expanded via cascade from sub-cycle 1 (Architecture Overview UC v3-patched-a → v3-patched-b DRAFT 2026-05-11; A1 InputTransformer cascade to § 4.1.2 + A4 Lambda State refresh across 7 per-flow narratives + A5 NYRA cron retiming cascade to § 4.1.4). **7 patches applied (Pattern A bundle C1-C7) per R14.2 Option A scope:** C1 § 4.1.1 daily ingestion (equine-ingestion State INACTIVE → Active per V16 SP-resume; fire-and-fail anomaly retracted; R8 Option B retention marker preserving v1-patched-c "fire-and-fail at lock" narrative); C2 § 4.1.2 nightly results fetch (A1 InputTransformer cascade per v3-patched-b § 3.6 line 147; refutes v1-patched-c "Default-case dispatch (the rule carries no `Input` override)" claim — corrected per OCRC D1 V6 priority-finding block + OCRC Fix 1 disambiguation + handler.py:243-249 sentinel-routing logic + CloudTrail PutTargets 2026-03-20T20:14:41 UTC; substrate-correct InputTransformer disclosure with `USE_TODAY_MINUS_1` sentinel handler-side interpretation; equine-ingestion State refresh INACTIVE → Active per V16; cite-NOT discipline applied per B8 — no citation of OCRC handoff § 2.4 nor "Input=null" CC Step 4 report); C3 § 4.1.4 NYRA workout scrape (A5 cron retiming cascade per v3-patched-b § 3.6 line 150 — `cron(0 10 * * ? *)` → `cron(0 16 * * ? *)` per OCRC Fix 3 2026-05-09; Finding 1 closure block documenting 7-day zero-result baseline pre-OCRC + 99-workouts-at-fix-time evidence + post-fix substrate stability per V25 SP-resume substrate; R8 Option B retention marker preserving v1-patched-c "currently functional" narrative + ADDING substrate-refutation context); C4 § 4.1.5 + § 4.1.5.1 + § 4.1.5.2 + § 4.1.5.3 daily inference WR/PL/LS (Lambda State refresh per V20/V21/V22 SP-resume substrate; R8 Option B retention marker documenting substrate-evolution timeline including SP-A2 cull rotation → Phase β-2 restoration); C5 § 4.1.6 results matcher (equine-results State INACTIVE → Active per V18 SP-resume; fire-and-fail anomaly retracted; R8 Option B retention marker); C6 § 4.1.7 angle stats refresh (equine-ingestion State INACTIVE → Active per V16 SP-resume; fire-and-fail anomaly retracted; R8 Option B retention marker); C7 § 6 Currently Open (Bug #28 substrate refresh — equine-ingestion no longer INACTIVE so post-2026-05-02 fire-and-fail clause retracted; fire-and-fail anomaly cross-reference refreshed per v3-patched-b § 6 historical retention). **§ 4.2 Data Acquisition Honesty Protocol NOT in scope per R14.2 Option A explicit exclusion**; § 4.2.4 NYRA disposition refresh deferred to Phase A re-dispatch venue per Tony ratification (Finding 1 closure for § 4.1.4 stands; § 4.2.4 closure deferred). Cross-bible cross-reference freeze: LIFTED via Tony Option α 2026-05-09 (parent EE Bible Upstream-Correction Cycle scope); re-locks at Database & Schema Bible UC sub-cycle 4 close per R14.3 Option B. Cohort-locked audit-CC pending per R15 Option B; audit covers sub-cycle 1 v3-patched-b + sub-cycle 1.5 v1-patched-a + sub-cycle 2 v1-patched-d end-to-end coherence verification. Companion verification log NEW: `_audit/data_pipeline_bible_v1_patched_d_verification.md` (drafting CC at v1-patched-d SP-2-drafting-complete; V27 substrate-stability re-confirmation; cohort-locked audit-CC pending). v1-patched-c lock-state companion verification log preserved verbatim per banked Lesson § 4.17 (locked bibles preserve drafting-time historical context); only v1-patched-c → v1-patched-d delta captured in NEW log per surgical-cosmetic-patch convention. v1-patched-d lock posture: pending cohort-locked audit-CC dispatch.

---

## 1. Scope of this bible

The Data Pipeline Bible answers a single per-flow question: **"how does data move from external source to DB to model to API in EE?"** Audience: any reader touching ingestion, scrapers, results-matching, daily inference, retraining cadence, or data-acquisition reliability.

This bible is **flow-narrative**: each § 4.1 sub-section walks one EventBridge-triggered flow from its source through the Lambda(s) or ECS task that runs it to the destination DB tables. § 4.2 then re-cuts the same surface from a per-source honesty-protocol angle. Other Phase 1 bibles are reference-style (Database & Schema) or composition-narrative (ML Layer Architecture); cross-references resolve outward to those for per-domain depth.

**Boundary statements — what this bible documents:**
- Per-flow data movement: ingestion → DB → model → API (one sub-section per flow at § 4.1).
- Data acquisition discipline per source (HRN entries / HRN results / HRN workouts / NYRA workouts / Equibase chart parser / `equibase_probe/`) per META_PLAN v9 § 7.9 Data Acquisition Honesty Protocol at § 4.2.
- Retrain cadence as the operational instance of training triggers (the daily/weekly retrain crons live at § 4.1.8 and § 4.1.9 as flow descriptions; per-pipeline retrain mechanics live elsewhere).
- Discipline rules and What Was Fixed entries scoped to data-acquisition prevention.

**Boundary statements — what this bible does NOT document:**
- Per-table schema → `database_schema_bible:4.1`.
- Per-feature consumption (which model uses which feature) → `feature_provenance_bible:4`.
- Per-model architecture (ranker layers, calibration, ensembling) → `ml_layer_architecture_bible:4`.
- Per-model success criteria + retrain mechanics → `model_evaluation_retraining_bible:4`.
- Per-route detail (HTTP routes, request/response shapes) → `api_frontend_bible:4.1`.
- Cross-runtime topology (Lambda inventory, ECS Fargate fleet, EventBridge schedule per-rule target verification) → `architecture_overview:3`.
- Fire-and-fail anomaly substantive description → `architecture_overview:6` (canonical home per BIBLE_STRUCTURE_SPEC v6 § 5.3 cross-cutting bug scope rule); this bible carries one-line cross-references at § 6 + per-flow impairment notes at § 4.1.X where ENABLED rules target INACTIVE Lambdas.

**Cross-bible references that govern this bible's documentation discipline:**
- `architecture_overview:5.1` (Forbidden Pattern: documenting a Lambda's role without verifying its current State) and `architecture_overview:5.2` (Common Mistake: documenting an EventBridge rule's behavior without cross-referencing target State) — every § 4.1.X sub-section in this bible cites Lambda State + EventBridge target State at the same lock time per these governing rules.
- `architecture_overview:3.1` (Lambda inventory) — destination for Lambda-State cross-references.
- `architecture_overview:3.2` (ECS Fargate task families) — destination for ECS task family cross-references at § 4.1.8 + § 4.1.9.
- `architecture_overview:3.6` (EventBridge schedule with per-rule target verification) — inherited substrate for the 13-rule decomposition; this bible re-cites the inherited locked output by section anchor per Lesson 5 inheritance discipline rather than re-running `aws events list-targets-by-rule` from drafting CC sandbox.
- `architecture_overview:4.2` (per-pipeline prediction shapes) — destination for the WR dynamic attribute attachment cross-reference at § 4.1.5.
- `database_schema_bible:4.1` (per-table sub-sections) — destination for every flow's destination-table cross-reference.
- `database_schema_bible:4.1.12` + `database_schema_bible:4.1.13` (F.2 cross-reference targets) — out-of-band ALTER columns on `wr_predictions` + `pl_predictions` substrate context cross-referenced at § 4.1.5.
- `database_schema_bible:4.1.14` (F.3 cross-reference target) — `ls_predictions` dual-write substrate cross-referenced at § 4.1.5.

**Source-priority hierarchy operative for this bible's content** (per META_PLAN v9 § 4.5): Tier 1 (live AWS state, inherited via `architecture_overview:3.1` + `architecture_overview:3.6`) > Tier 2 (live API endpoints) > Tier 3 (live DB state) > Tier 4 (working-tree code post-baseline 87dec36; Bug #28 substrate at `hrn_scraper.py:802-804` and `hrn_scraper.py:814` are Tier 4) > Tier 5 (operator-stated history; Bug #28 verbatim symptom quote inherits from PHASE_5_BACKLOG.md Phase 5.3.1 per Claim 15c pattern) > Tier 6 (`EE_CURRENT_STATE_DUMP.md`) > Tier 7 (session logs).

---

## 2. Definitions

Terminology specific to the data pipeline domain. Acronyms defined in `architecture_overview:2` (WR / PL / LS, Active vs Inactive Lambda, ENABLED vs DISABLED rule, Deployed image, Gonzo Sauce) are referenced from there, NOT redefined here.

- **HRN.** Horse Racing Nation, the website domain `https://entries.horseracingnation.com/` (and adjacent paths) that the HRN scraper module (`backend/services/data_sources/hrn_scraper.py`) targets for race-card entries, results, and pool data. Source for § 4.1.1 daily ingestion + § 4.1.2 nightly results fetch + § 4.2.1 + § 4.2.2 + § 4.2.3 honesty entries.
- **NYRA.** New York Racing Association, the operator of NYRA-track venues (Aqueduct, Belmont Park, Saratoga). The NYRA workout scraper (`equine-nyra-workouts` Lambda) targets NYRA-published workout endpoints for NYRA tracks only. Source for § 4.1.4 + § 4.2.4.
- **Equibase chart.** The post-race PDF chart Equibase publishes per (track, date) tuple. Equibase charts are the canonical post-race source of truth for finishing positions, payouts, beaten lengths, fractional times, and run-up distances. The chart parser (`backend/services/chart_parser.py`) reads PDFs from `s3://equine-raw-data/` and writes enrichment rows back to `results`. Source for § 4.1.3 + § 4.2.5.
- **Qualifying track.** A track flagged `is_qualifying = TRUE` on the `tracks` row (per `database_schema_bible:4.1.tracks` — the canonical home for the column definition). Inference and downstream UI restrict to qualifying tracks per the `equine-inference` dispatcher's filtering layer. Defined here for cross-bible reference; the substantive column documentation lives at `database_schema_bible:4.1`.
- **Default-case dispatch.** The Lambda handler tail-end code path triggered when the invocation event does not carry an `action` field — i.e., when `event.get('action')` returns `None`. For `equine-ingestion`, the default-case dispatch invokes `IngestionService(conn).fetch_daily_entries(date.today())` (the "Normal scheduled ingestion" block at `backend/lambdas/ingestion/handler.py:1669-1680`); this is the path EventBridge rules `equine-ingestion-daily` and `equine-fetch-results-nightly` exercise. Per `architecture_overview:3.1` V3-2 sub-citation.
- **Fire-and-fail.** An ENABLED EventBridge rule whose target Lambda is INACTIVE. Cron fires; invocation returns `ResourceNotReadyException` because the deployed image has been culled from the CDK assets repository; downstream pipeline stages receive no fresh data on those days. Canonical home is `architecture_overview:6`; this bible's § 4.1.X impaired-flow notes and § 6 carry one-line cross-references per BIBLE_STRUCTURE_SPEC v6 § 5.3 non-canonical-home rule.
- **Action-based admin dispatch.** The 25-action handler surface on `equine-ingestion` per `architecture_overview:3.1` V3-2 sub-citation: 5 data acquisition + 4 model lifecycle + 5 admin/diagnostic + 7 data backfills/ops + 3 originally-cited admin + 1 health = 25. Three of the 25 actions are EventBridge-triggered at lock (`refresh_angle_stats` via `equine-angle-stats-nightly`; default-case via `equine-ingestion-daily` and `equine-fetch-results-nightly`); the remaining 22 are manual-invoke only. All 25 are currently non-functional via the same INACTIVE-Lambda mechanism.

When sources conflict, source-priority hierarchy applies per META_PLAN v9 § 4.5.

---

## 3. Pipeline overview

EE's data pipeline is a 9-flow EventBridge-scheduled choreography across 5 Active Lambdas + 2 of the 3 INACTIVE Lambdas (the third INACTIVE Lambda `equine-feature-engineering` does not participate in any cron flow because its only EventBridge rule is DISABLED with zero current targets) — 7 of the 8-Lambda inventory at `architecture_overview:3.1` — plus 2 ECS Fargate task families (`equine-training-daily-full` and `equine-training-win-prob` per `architecture_overview:3.2`).

**Source ingress.** External data enters via three families of source: HRN web pages (entries + results pages, scraped by `hrn_scraper.py` running inside `equine-ingestion`); NYRA workout endpoints (consumed by `equine-nyra-workouts` Active Lambda); and Equibase PDF charts (delivered via S3 to `equine-raw-data`, parsed by `chart_parser.py` running inside `equine-ingestion` via the `parse_charts` admin action). The probe directory `equibase_probe/` carries exploratory acquisition work with zero production-runtime consumers per `architecture_overview:3.7` + `architecture_overview:3.8`; § 4.2.6 documents its disposition.

**DB persistence.** Persisted rows land in the 14 domain tables enumerated at `database_schema_bible:3.1`. Per-flow destination-table cross-references appear in each § 4.1.X sub-section; the canonical home for every table's schema is `database_schema_bible:4.1.<table>`.

**Inference fan-out.** Three Active inference Lambdas (`equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference` per `architecture_overview:3.1`) read `entries` / `races` / `past_performances` / `workouts` / `results` and write per-pipeline prediction rows to `wr_predictions`, `pl_predictions`, `ls_predictions` (per `database_schema_bible:4.1.12` / `:4.1.13` / `:4.1.14`). § 4.1.5 enumerates the three inference flows under one § 4.1 sub-section per BIBLE_STRUCTURE_SPEC v6 § 6.2 prescribed TOC.

**API surface.** Predictions are read by API Gateway integrations on the Active `equine-inference` dispatcher per `architecture_overview:3.5`. Per-route detail is `api_frontend_bible:4.1` responsibility.

**Operational reality at lock — fire-and-fail anomaly.** Of the 10 ENABLED EventBridge rules in `architecture_overview:3.6`, **4 target INACTIVE Lambdas**: `equine-ingestion-daily` and `equine-fetch-results-nightly` target `equine-ingestion` (INACTIVE); `equine-results-daily` targets `equine-results` (INACTIVE); `equine-angle-stats-nightly` targets `equine-ingestion` (INACTIVE) with `Input = {"action":"refresh_angle_stats"}`. These four flows are documented in this bible at § 4.1.1, § 4.1.2, § 4.1.6, § 4.1.7 respectively, each carrying a one-line cross-reference to `architecture_overview:6` (the canonical home for the cross-runtime invariant). Substantive description of the fire-and-fail anomaly lives at `architecture_overview:6` per BIBLE_STRUCTURE_SPEC v6 § 5.3.

**Bug #28 surface.** Bug #28 (HRN scraper column-shift defect) is canonically homed in this bible at § 8.W.1 + § 8.W.2 per BIBLE_STRUCTURE_SPEC v6 § 5.3 (data-acquisition discipline most directly prevents recurrence). At lock the bug is open; tracked at PHASE_5_BACKLOG.md Phase 5.3.1 per TRIAGE_QUEUE_SPEC v1 § 3. § 6 Currently Open carries the substantive Currently-Open description; § 8.W.1 + § 8.W.2 enumerate the canonical W.N entries.

---

## 4. Pipeline detail

### 4.1 Per-flow detail

The 9 sub-sections below enumerate every cron-triggered flow. Per BIBLE_STRUCTURE_SPEC v6 § 6.2 prescribed TOC, § 4.1.5 holds 3 EventBridge rules under one sub-section (the per-pipeline inference Lambdas WR/PL/LS); § 4.1.3 holds 0 direct EventBridge rules (the chart parser is invoked via admin action, not directly scheduled). EventBridge rule cardinality per sub-section: 1+1+0+1+3+1+1+1+1=10, matching the 10 ENABLED rules at `architecture_overview:3.6`.

Per `architecture_overview:5.1` (Forbidden Pattern) + `architecture_overview:5.2` (Common Mistake): every sub-section below cites Lambda State + EventBridge target State at the same lock time (2026-05-05 inherited from Architecture Overview v3 verification log per Lesson 5 inheritance discipline).

#### 4.1.1 Daily ingestion (race cards) — `equine-ingestion-daily` cron

**Trigger.** EventBridge rule `equine-ingestion-daily`, cron `cron(0 11 * * ? *)`, ENABLED at lock per `architecture_overview:3.6`.

**Source.** HRN entries pages (`entries.horseracingnation.com/<track>/<date>` and adjacent paths); see § 4.2.1.

**Lambda(s) involved.** Target Lambda: `equine-ingestion` (**Active at v1-patched-d lock per `architecture_overview:3.1` v3-patched-b SP-resume V16 substrate**; memory 2048 MB, timeout 900 s; LastModified 2026-05-11T13:58:54Z UTC; ImageUri tag `:fdd29e6842bf…c648b` resolving cleanly to ECR digest `sha256:6942f3f4…` per v3-patched-b § 3.7 F14 reproducible-build evidence).

**Action(s) dispatched.** Default-case dispatch (no `action` Input on the EventBridge target → `event.get('action')` returns `None` → handler tail-end "Normal scheduled ingestion" block at `backend/lambdas/ingestion/handler.py:1669-1680` invokes `IngestionService(conn).fetch_daily_entries(date.today())`). Per `architecture_overview:3.1` V3-2 sub-citation. Verified at substrate read V1-5 (this bible's verification log).

**Destination tables.** `entries`, `races`, `horses`, `trainers`, `jockeys`, `tracks`, `past_performances` (the entry-row plus the foreign-key parent rows the producer must defensively assert; per `database_schema_bible:4.1.entries`, `:4.1.races`, `:4.1.horses`, `:4.1.trainers`, `:4.1.jockeys`, `:4.1.tracks`, `:4.1.past_performances`).

**Currently functional at v1-patched-d lock (2026-05-11).** Lambda Active per V16 SP-resume substrate; rule ENABLED; cron fires; daily race-card entries refresh on this flow's schedule. **[Historical retention per R8 Option B (v1-patched-d 2026-05-11 ratification): At v1-patched-c lock (2026-05-06), this flow was Fire-and-fail — ENABLED rule targeting INACTIVE `equine-ingestion` Lambda; downstream stages operated against stale entries on impacted days. Anomaly resolution timeline per `architecture_overview:6` v3-patched-b historical retention block: OCRC Phase A informal recovery 2026-05-09T04:37Z UTC restored `equine-ingestion` Active state; OCRC Fix 6 2026-05-09T17:16:18Z UTC surgical redeploy with `logger.info()` surface fix; subsequent ECR-lifecycle cull regression did NOT re-affect `equine-ingestion` (its recent push survived the cull window per v3-patched-b § 3.1 + § 3.11.1 substrate); Phase β-2 cdk deploy 2026-05-11T13:46:13–13:59:42Z UTC confirmed 8/8 Active state; structural mitigation at v3-patched-b § 3.11.1 ECR lifecycle policy override `imageCountMoreThan: 5` → 30 (Phase β-1 2026-05-11T13:40:21Z UTC) reduces future cull-driven recurrence probability. Cross-reference `architecture_overview:6` for canonical home historical retention.]**

**Failure modes.** Beyond the resolved fire-and-fail impairment (historical): the underlying HRN scraper has compound failure history per § 4.2.1 (Bug #7 — per META_PLAN v9 § 1.2). Bug #7 is canonically homed elsewhere; § 4.2.1 documents the data-acquisition honesty disposition. **Note: § 4.2.1 substrate refresh deferred to Phase A re-dispatch per R14.2 Option A scope exclusion of § 4.2 territory; § 4.2.1 v1-patched-c narrative retained verbatim and may carry substrate-stale Lambda State claims at v1-patched-d lock.**

#### 4.1.2 Nightly results fetch — `equine-fetch-results-nightly` cron

**Trigger.** EventBridge rule `equine-fetch-results-nightly`, cron `cron(30 1 * * ? *)`, ENABLED at lock per `architecture_overview:3.6`.

**Source.** HRN results pages; see § 4.2.2.

**Lambda(s) involved.** Target Lambda: `equine-ingestion` (**Active at v1-patched-d lock per `architecture_overview:3.1` v3-patched-b SP-resume V16 substrate**; same memory/timeout as § 4.1.1; same ImageUri tag `:fdd29e6842bf…c648b` per F14 reproducible-build evidence — the target is the same Lambda).

**Action(s) dispatched.** **InputTransformer dispatch (substrate-corrected at v1-patched-d per A1 cascade from v3-patched-b § 3.6 line 147 + OCRC D1 § 2.3 V6 priority-finding block + OCRC Fix 1 cron-payload audit disambiguation per `docs/operations/CRON_PAYLOAD_AUDIT_2026-05-09.md`).** The EventBridge rule carries an `InputTransformer` with `InputPathsMap: {"time": "$.time"}` (dead substrate; no `<time>` placeholder in template; harmless residue per OCRC D1 V6) and `InputTemplate: {"action":"fetch_results","date":"USE_TODAY_MINUS_1"}`. The literal sentinel `USE_TODAY_MINUS_1` is interpreted handler-side at `backend/lambdas/ingestion/handler.py:243-249` (action `fetch_results` branch tests `target_date not in ('USE_TODAY_MINUS_1', '')` and falls to `date.today() - timedelta(days=1)`); EventBridge does not perform date arithmetic. Configuration stable since 2026-03-20T20:14:41 UTC (CloudTrail PutTargets by root user; ~52-day stable at v1-patched-d lock). The dispatched action is **`fetch_results`** with effective date = yesterday — NOT default-case dispatch as v1-patched-c § 4.1.2 narrative claimed. **[Substrate-correction observation per A1 cascade discipline: v1-patched-c "Default-case dispatch (the rule carries no `Input` override)" claim refuted by OCRC D1 V6 substrate; corrected verbatim at v1-patched-d per substrate-verification-at-first-reference discipline. Cite-NOT block per B8: original inheritance claims from OCRC handoff § 2.4 + "Input=null" CC Step 4 report are NOT cited (both refuted at OCRC D1 V6 priority-finding block).]**

**Destination tables.** `results` (and the win/place/show/exacta/trifecta/superfecta/daily_double payout fields therein per `database_schema_bible:4.1.9`). The win/place/show payout fields are the column-shift defect surface for Bug #28 — see § 8.W.1.

**Currently functional at v1-patched-d lock (2026-05-11).** Lambda Active per V16 SP-resume substrate; rule ENABLED; cron fires; `fetch_results` action dispatches handler-side with target_date = yesterday per InputTransformer sentinel interpretation. **[Historical retention per R8 Option B: v1-patched-c lock state was fire-and-fail (ENABLED rule + INACTIVE target); anomaly resolved per `architecture_overview:6` v3-patched-b historical retention block (OCRC + Phase β-2 timeline as in § 4.1.1).]**

**Bug #28 cross-reference.** Bug #28 (HRN scraper column-shift defect) is canonically homed in this bible at § 8.W.1 (column shift at `hrn_scraper.py:802-804`) and § 8.W.2 (DD pool extraction nuance at `hrn_scraper.py:814`). PHASE_5_BACKLOG.md Phase 5.3.1 tracks the open status. **[At v1-patched-d lock: Bug #28 status unchanged — open and tracked at Phase 5.3.1. With `equine-ingestion` Active at v1-patched-d, the underlying HRN scraper now writes column-shifted payout rows DAILY on this flow's schedule (vs the pre-2026-05-09 fire-and-fail window where no rows were written at all). Bug #28 fix is required to prevent ongoing column-shifted-row accumulation; backfill scope from PHASE_5_BACKLOG.md expands daily until fix lands. Historical: at v1-patched-c lock 2026-05-06, Bug #28 column-shifted rows existed in the 2026-04-30 → 2026-05-02 window; post-2026-05-02 the flow was fire-and-fail and wrote no rows at all. Post-2026-05-09 (OCRC equine-ingestion restoration), the flow resumes writing — including writing further column-shifted rows pending Bug #28 fix.]**

**Failure modes.** (a) **Bug #28 column shift OPEN at v1-patched-d lock** — column-shifted rows being written daily on this schedule pending Phase 5.3.1 fix (escalation of impact severity since v1-patched-c lock per restored-Lambda + still-broken-scraper combination). (b) Compound HRN reliability per § 4.2.2 (substrate refresh deferred to Phase A re-dispatch per R14.2 Option A scope exclusion). (c) Historical fire-and-fail period 2026-05-02 → 2026-05-09 produced no rows (gap-period); fresh-row resumption per V16 SP-resume substrate.

#### 4.1.3 Chart parser (S3 PDFs → results enrichment)

**Trigger.** **None directly** — per `architecture_overview:3.6` ENABLED + DISABLED tables, no EventBridge rule's target carries Equibase chart parsing as its action. Substrate verification (V1-9) confirms the chart parser is invoked via the **`parse_charts` admin action** on `equine-ingestion` (handler at `backend/lambdas/ingestion/handler.py:542` entry; the handler imports `services.chart_parser.run_from_s3` and calls it). Invocation path: manual via `aws lambda invoke` with payload `{"action": "parse_charts", "track": "<code>"}` or `{"action": "parse_charts"}` for all tracks. Optional `date_from` / `date_to` parameters supported (`YYYYMMDD` format).

**Source.** PDF charts in `s3://equine-raw-data/` (per `architecture_overview:3.4`).

**Lambda(s) involved.** Target Lambda for the `parse_charts` admin action: `equine-ingestion` (INACTIVE at lock per `architecture_overview:3.1`).

**Action(s) dispatched.** `parse_charts` admin action (manual invocation only; not on any EventBridge rule's target list at lock).

**Destination tables.** `results` (chart parser fills enrichment columns from the Equibase PDF chart that HRN results pages do not provide — fractional times, beaten lengths, run-up distances, pace figures; per `database_schema_bible:4.1.9` for the column inventory).

**Currently impaired.** **Manual-invoke action on INACTIVE Lambda — non-functional at lock.** Distinct from fire-and-fail (no cron fires); the impairment manifests on manual invoke as `ResourceNotReadyException`. Cross-reference `architecture_overview:6` (the canonical home documents the INACTIVE-Lambda mechanism that produces this impairment for both EventBridge and manual-invoke paths).

**Failure modes.** (a) Lambda INACTIVE since 2026-05-02; chart parser is non-functional via `parse_charts` admin action. (b) Pre-INACTIVE-state operational reliability per § 4.2.5.

#### 4.1.4 NYRA workout scrape — `equine-nyra-workouts-daily` cron

**Trigger.** EventBridge rule `equine-nyra-workouts-daily`, **cron `cron(0 16 * * ? *)`** (retimed at OCRC Fix 3 2026-05-09 from `cron(0 10 * * ? *)` per OCRC close-out § 1.2 item 5 + `docs/operations/CRON_PAYLOAD_AUDIT_2026-05-09.md` + V25 SP-resume substrate re-confirmation 2026-05-11T14:31:09Z UTC), ENABLED at v1-patched-d lock per `architecture_overview:3.6` v3-patched-b § 3.6 line 150 A5 substrate.

**Source.** NYRA workout endpoint (NYRA tracks only — Aqueduct, Belmont Park, Saratoga); see § 4.2.4 (substrate refresh deferred to Phase A re-dispatch per R14.2 Option A; § 4.2.4 v1-patched-c narrative retained verbatim).

**Lambda(s) involved.** Target Lambda: `equine-nyra-workouts` (Active at v1-patched-d lock per `architecture_overview:3.1` v3-patched-b V6 substrate; LastModified 2026-04-27T22:11:00Z UTC; ImageUri tag `:v1-1777327653` from separate custom ECR repo `equine-nyra-workouts` per v3-patched-b § 3.7 + § 3.11.2 F22 substrate; memory 512 MB, timeout 300 s).

**Action(s) dispatched.** Lambda is purpose-built (single-flow Lambda; no action dispatch surface). Direct invocation runs the NYRA scrape.

**Destination tables.** `workouts` (per `database_schema_bible:4.1.8`).

**Currently functional at v1-patched-d lock (2026-05-11).** Lambda Active per V6 SP-A1 substrate; rule ENABLED with retimed cron `cron(0 16 * * ? *)` per V25 SP-resume; target Lambda Active. NYRA workouts table receives fresh rows daily on this schedule.

**[Finding 1 closure block per v1-patched-d (parent cycle-entry trigger ratification 2026-05-11):**

At v1-patched-c lock (2026-05-06), this sub-section's "Currently functional" claim was substrate-grounded against then-available substrate (Lambda Active per `architecture_overview:3.1` v1-patched-c-era substrate; NYRA endpoint reachable per § 4.2.4 PHASE 1 Empirical Check 2 verification 2026-05-06). However, **parent EE Bible Upstream-Correction Cycle Finding 1 surfaced that this "currently functional" claim was substrate-refuted** by operational reality across 2026-05-02 → 2026-05-09: the pre-OCRC NYRA cron timing (`cron(0 10 * * ? *)` = 10:00 UTC daily) executed BEFORE NYRA publishes daily workout data on its endpoint, producing **7+ consecutive days of zero-result scrapes** (verified empirically post-OCRC). The "currently functional" claim in this bible's v1-patched-c lock was correct re: Lambda State + endpoint reachability but incorrect re: operational outcome (data acquisition).

**OCRC Fix 3 resolution (2026-05-09 UTC):** NYRA cron retimed from `cron(0 10 * * ? *)` to `cron(0 16 * * ? *)` (16:00 UTC daily) per `docs/operations/CRON_PAYLOAD_AUDIT_2026-05-09.md` + OCRC close-out § 1.2 item 5. Manual invocation at fix-time (2026-05-09T16:12:33Z UTC) captured **99 workouts** (SAR=50 + BEL=49 + AQU=0) vs pre-fix 7-day zero-baseline. Post-fix substrate stability verified at V25 SP-resume 2026-05-11T14:31:09Z UTC (cron still `cron(0 16 * * ? *)`, ENABLED, target equine-nyra-workouts Lambda).

**Finding 1 closure determination at v1-patched-d:** Per v3-patched-b § 3.6 line 150 (A5 patch) + V25 SP-resume substrate, the NYRA workout scrape flow is operationally functional at v1-patched-d lock — Lambda Active + cron retimed to publication-window-aligned 16:00 UTC + endpoint reachable + 99-workouts-at-fix-time evidence. The original substrate-refutation has been resolved.

**§ 4.2.4 deferral disclosure:** Per R14.2 Option A scope exclusion, this bible's § 4.2.4 NYRA workouts sub-section is NOT refreshed at v1-patched-d. § 4.2.4 retains v1-patched-c narrative verbatim and may carry substrate-stale empirical-verification claims (e.g., 2026-05-06 PHASE 1 Empirical Check 2 timestamp). § 4.2.4 closure deferred to Phase A re-dispatch venue per Tony ratification.]**

**Failure modes.** None at v1-patched-d lock per the documented operational state (Lambda Active + cron retimed to operationally-correct 16:00 UTC + 99-workouts-at-fix-time evidence per Finding 1 closure block above).

#### 4.1.5 Daily inference (WR / PL / LS — 3 rules under one sub-section per § 6.2)

This sub-section enumerates the 3 EventBridge rules under one § 4.1 sub-section per BIBLE_STRUCTURE_SPEC v6 § 6.2 prescribed TOC. Each rule targets a different Active per-pipeline Lambda; each Lambda writes a different prediction table.

##### 4.1.5.1 WR daily inference

**Trigger.** `equine-wr-inference-daily`, cron `cron(30 12 * * ? *)`, ENABLED per `architecture_overview:3.6`.

**Source.** Reads `entries`, `races`, `past_performances`, `workouts`, `results` (the input feature surface; per-feature consumption documented at `feature_provenance_bible:4`).

**Lambda(s) involved.** `equine-wr-inference` (Active at v1-patched-d lock per `architecture_overview:3.1` v3-patched-b SP-resume V20 substrate; LastModified 2026-05-11T13:58:26Z UTC; ImageUri tag `:775e987d2b8f…af5c5` post-Phase-β-2 cdk deploy; memory 1024 MB, timeout 300 s).

**Destination tables.** `wr_predictions` per `database_schema_bible:4.1.12`.

**WR pipeline shape.** Per `architecture_overview:4.2`, WR instantiates the base `Prediction` dataclass and dynamically attaches 9 enrichment fields via Python attribute assignment at `backend/services/wr_inference_service.py:718-730`: `raw_win_prob`, `handicapping_prob`, `market_prob`, `edge_pct`, `rank_score`, `kelly_fraction`, `kelly_bet`, `has_workout_data`, `model_used`. The dynamically-attached fields are NOT in the dataclass schema. Substrate evidence at V1-7. Canonicalization disposition (extracting a `WRPrediction` subclass) is forward-looking work documented at `architecture_overview:4.2`.

**F.2 cross-reference (database_schema_bible:4.1.12).** `wr_predictions` schema includes `style` and `model_used` columns that were added via out-of-band ALTER and are NOT preserved as a tracked migration file. Substantive description and disposition live at `database_schema_bible:4.1.12`; this bible's flow-context observation is that the WR write-path currently inserts rows with `(race_id, entry_id, style)` ON CONFLICT semantics matching the post-migration-011 UNIQUE constraint per `database_schema_bible:4.1.12` "Primary writers" sub-section.

**Currently functional at v1-patched-d lock (2026-05-11).** Lambda Active; rule ENABLED; cron fires; predictions written daily. **[Historical retention per R8 Option B: At v1-patched-c lock 2026-05-06, equine-wr-inference was Active (OCRC D1 V4 substrate). Across 2026-05-09 → 2026-05-11, the Lambda rotated to Inactive via ECR-lifecycle cull regression per `architecture_overview:3.11.1` + F1/F7/F10 banking findings (cull-driven cohort rotation triggered by OCRC Fix 4 + Fix 6 image pushes; `imageCountMoreThan: 5` Bootstrap default policy culled the equine-wr-inference image `:f89865ae…b98215`); fire-and-fail anomaly re-instantiated at this flow during the rotation window (per `architecture_overview:6` v3-patched-b historical retention). Restoration via Phase β-2 cdk deploy 2026-05-11T13:46:13–13:59:42Z UTC; image push `:775e987d2b8f…af5c5` to `cdk-hnb659fds-…` repo per V20 SP-resume substrate. Structural mitigation at Phase β-1 lifecycle policy override `imageCountMoreThan: 5` → 30 per `architecture_overview:3.11.1`. Substrate evolution documented for pattern instruction value: image-cull-driven cohort rotation as substrate failure mode (per `architecture_overview:6` v3-patched-b cross-cutting-topic entry).]**

##### 4.1.5.2 PL daily inference

**Trigger.** `equine-pl-inference-daily`, cron `cron(35 12 * * ? *)`, ENABLED per `architecture_overview:3.6`.

**Source.** Same input feature surface as WR.

**Lambda(s) involved.** `equine-pl-inference` (Active at v1-patched-d lock per `architecture_overview:3.1` v3-patched-b SP-resume V21 substrate; LastModified 2026-05-11T13:58:26Z UTC; ImageUri tag `:5aa74068f237…eb37a` post-Phase-β-2 cdk deploy; memory 1024 MB, timeout 300 s).

**Destination tables.** `pl_predictions` per `database_schema_bible:4.1.13`.

**PL pipeline shape.** PL uses the canonical `PLPrediction` dataclass per `architecture_overview:4.2` (~26 fields all in the dataclass schema; PL storage is type-safer than WR's hybrid object).

**F.2 cross-reference (database_schema_bible:4.1.13).** `pl_predictions` has the same out-of-band `style` column observation as `wr_predictions`. Substantive description at `database_schema_bible:4.1.13`; this bible's flow-context observation is that `pl_prediction_repository.py:255` ON CONFLICT clause matches the post-out-of-band-ALTER `(race_id, entry_id, style)` constraint.

**Currently functional at v1-patched-d lock (2026-05-11).** Lambda Active; rule ENABLED. **[Historical retention per R8 Option B: equine-pl-inference followed same substrate-evolution trajectory as equine-wr-inference per § 4.1.5.1 historical retention block — Active at v1-patched-c lock → rotated Inactive 2026-05-09 → 2026-05-11 via cull regression → restored at Phase β-2 cdk deploy 2026-05-11; image push `:5aa74068f237…eb37a` to `cdk-hnb659fds-…` repo per V21 SP-resume substrate.]**

##### 4.1.5.3 LS daily inference (dual-write pattern; F.3 cross-reference)

**Trigger.** `equine-ls-inference-daily`, cron `cron(40 12 * * ? *)`, ENABLED per `architecture_overview:3.6`.

**Source.** Same input feature surface as WR / PL.

**Lambda(s) involved.** `equine-ls-inference` (Active at v1-patched-d lock per `architecture_overview:3.1` v3-patched-b SP-resume V22 substrate; LastModified 2026-05-11T13:58:26Z UTC; ImageUri tag `:02063b416a6e…f5c6` post-Phase-β-2 cdk deploy; memory 1024 MB, timeout 300 s). **[Historical retention per R8 Option B: equine-ls-inference also followed substrate-evolution trajectory per § 4.1.5.1 — Active at v1-patched-c → rotated Inactive 2026-05-09 → 2026-05-11 (later in the rotation than wr/pl per cull-timing asymmetry surfaced at SP-A2 V22 → Step 0 Inactive transition between SP-A2 and Phase γ Step 0) → restored at Phase β-2 cdk deploy 2026-05-11.]**

**Destination tables.** `ls_predictions` AND `wr_predictions` (see dual-write pattern below) per `database_schema_bible:4.1.14` and `database_schema_bible:4.1.12`.

**F.3 cross-reference (database_schema_bible:4.1.14) — dual-write pattern.** The production INSERT path is `backend/services/ls_inference_service.py:388-401` (substrate at V1-6). The service performs TWO writes per LS prediction:

- **Write 2 (first-class ls_predictions row).** `INSERT INTO ls_predictions (...) ON CONFLICT (race_id, entry_id, style) DO UPDATE SET ...` — matches the post-migration-010 UNIQUE constraint per `database_schema_bible:4.1.14`. The 19-column INSERT covers all migration-005 + migration-010 columns.
- **Write 1 (LS-as-second-pass-enrichment on wr_predictions columns).** Migration 010's preamble describes LS originally landing as second-pass enrichment writing back to `wr_predictions` enrichment columns; the dual-write keeps backwards-compatibility with downstream LS-on-wr_predictions readers per `database_schema_bible:4.1.14` "Primary readers" sub-section (which enumerates `ls_prediction_repository.py:262 get_longshot_alerts_by_date` and `:374 get_track_record` reading `FROM wr_predictions p`).

The substantive description of the dual-write pattern lives at `database_schema_bible:4.1.14`; this bible's flow-context observation is that the LS inference Lambda is the ONLY production writer that touches both prediction tables per invocation.

**LS-specific operational state.** LS-specific 4-way strict-alert flag (per `architecture_overview:3.1` row) and Bug #25 (LS strict alert flag too restrictive for 3yos; per memory file `project_ee_bug_25_ls_strict_alert_3yos.md`) is canonically homed elsewhere.

**Currently functional.** Lambda Active; rule ENABLED.

**Forward cross-reference for all 3 inference flows.** Per-pipeline ML composition (ranker → calibrator → 0-PP-override) and per-pipeline retrain mechanics live at `ml_layer_architecture_bible:4.2` and `model_evaluation_retraining_bible:4` respectively.

#### 4.1.6 Results matcher — `equine-results-daily` cron

**Trigger.** EventBridge rule `equine-results-daily`, cron `cron(0 4 * * ? *)`, ENABLED at lock per `architecture_overview:3.6`.

**Source.** Chart parser output (when available) plus HRN results (when available); the results matcher reconciles per (race, entry) tuple.

**Lambda(s) involved.** Target Lambda: `equine-results` (**Active at v1-patched-d lock per `architecture_overview:3.1` v3-patched-b SP-resume V18 substrate**; LastModified 2026-05-11T13:58:26Z UTC; ImageUri tag `:3eaada0d87ee…7c98` post-Phase-β-2 cdk deploy; memory 512 MB, timeout 300 s).

**Action(s) dispatched.** Lambda is purpose-built (single-flow; no action dispatch surface) per `architecture_overview:3.1` row.

**Destination tables.** `results` (matching/reconciliation pass post-chart-parse-or-HRN-results-write per `database_schema_bible:4.1.9`).

**Currently functional at v1-patched-d lock (2026-05-11).** Lambda Active per V18 SP-resume substrate; rule ENABLED; cron fires; reconciliation pass runs on its schedule. **[Historical retention per R8 Option B: At v1-patched-c lock 2026-05-06, this flow was fire-and-fail — ENABLED rule targeting INACTIVE `equine-results` Lambda; reconciliation pass did not run on its schedule. Anomaly resolution timeline per `architecture_overview:6` v3-patched-b historical retention block: OCRC Fix 4 update-function-code 2026-05-09T16:21:55Z UTC restored equine-results Active state (image `:9f2ce334…d6e91` existing pre-fix per OCRC close-out § 3.1); subsequent ECR-lifecycle cull regression rotated equine-results back to Inactive between SP-A2 (2026-05-09) and Phase γ Step 0 (2026-05-11T13:00Z UTC) per F1/F7 banking findings; Phase β-2 cdk deploy 2026-05-11 final restoration with new image push `:3eaada0d87ee…7c98`; structural mitigation at `architecture_overview:3.11.1` lifecycle policy override.]**

**Failure modes.** None at v1-patched-d lock per the documented operational state.

#### 4.1.7 Angle stats refresh — `equine-angle-stats-nightly` cron

**Trigger.** EventBridge rule `equine-angle-stats-nightly`, cron `cron(15 2 * * ? *)`, ENABLED at lock per `architecture_overview:3.6`. The rule's `Input` payload is `{"action":"refresh_angle_stats"}` per `architecture_overview:3.6` table row.

**Source.** Existing DB rows in `past_performances` and `entries` (the SQL aggregate; no external source — angle stats are derived from the existing DB state).

**Lambda(s) involved.** Target Lambda: `equine-ingestion` (**Active at v1-patched-d lock per `architecture_overview:3.1` v3-patched-b SP-resume V16 substrate**; same Lambda as § 4.1.1, § 4.1.2; LastModified 2026-05-11T13:58:54Z UTC; ImageUri tag `:fdd29e6842bf…c648b`).

**Action(s) dispatched.** `refresh_angle_stats` admin action (handler at `backend/lambdas/ingestion/handler.py:94` per `architecture_overview:3.1` + `architecture_overview:3.6`). The handler does `DELETE FROM angle_stats` then re-INSERTs aggregated rows from joined `past_performances` + `entries` data per the SQL block at lines 94+.

**Destination tables.** `angle_stats` — see `database_schema_bible:4.1.15` for canonical schema substrate (column list asserted-from-INSERT-tuples per D&S Bible v1-patched-d2 PHASE 1 Approach B fallback; PK/FK/INDEX substrate asserted-disposition-pending-credential-authorized-cycle). Production handler at `backend/lambdas/ingestion/handler.py:94+` is the canonical primary writer (1 DELETE + 6 INSERTs + 1 SELECT COUNT(*) per audit-CC adversarial verification 2026-05-06; substrate captured at D&S Bible v1-patched-d2 V1-20). UPSTREAM-CORRECTION close: F.4 at this bible's verification log § F closed 2026-05-06 per D&S Bible v1-patched-d2 LOCKED. The table remains created out-of-band (no tracked migration declares it at lock; formalization-via-migration is Phase 5 backlog scope per `database_schema_bible:6` Currently Open entry).

**Currently functional at v1-patched-d lock (2026-05-11).** Lambda Active per V16 SP-resume substrate; rule ENABLED; cron fires; `refresh_angle_stats` action dispatches at 02:15 UTC daily; `angle_stats` table receives refreshed rows on this schedule. **[Historical retention per R8 Option B: At v1-patched-c lock 2026-05-06, this flow was fire-and-fail — ENABLED rule targeting INACTIVE `equine-ingestion` Lambda with `Input = {"action":"refresh_angle_stats"}`; angle-stats refresh did not run on its schedule. Anomaly resolution per OCRC Phase A informal recovery 2026-05-09T04:37Z UTC restored equine-ingestion Active state; per `architecture_overview:6` v3-patched-b historical retention block, this admin-action path was the third of three actions on `equine-ingestion` reachable via EventBridge that all returned to functional state post-OCRC.]**

**Failure modes.** None at v1-patched-d lock per the documented operational state.

#### 4.1.8 Daily retraining — `equine-daily-retrain-full` cron

**Trigger.** EventBridge rule `equine-daily-retrain-full`, cron `cron(30 2 * * ? *)`, ENABLED at lock per `architecture_overview:3.6`.

**Source.** Training data from RDS (`past_performances`, `results`, `entries` joins; per-feature derivation at `feature_provenance_bible:4`).

**Lambda(s) involved.** None — this is an **ECS Fargate task** trigger.

**ECS task family.** `equine-training-daily-full` per `architecture_overview:3.2`. The EventBridge target carries `EcsParameters.TaskDefinitionArn = arn:aws:ecs:us-east-1:584812014683:task-definition/equine-training-daily-full` per `architecture_overview:3.6` (full nightly retrain across all pipelines).

**Destination.** `s3://equine-model-artifacts/<family>/<version>.json` per `architecture_overview:3.4` artifact-path layout. `model_versions` registry rows are inserted/updated per `database_schema_bible:4.1.11`.

**Currently functional.** ECS task family + rule both at expected operational state. Per-pipeline retrain mechanics + retrain-trigger semantics live at `model_evaluation_retraining_bible:4`.

**Failure modes.** None canonically homed in this bible. Operational reliability of ECS task runs is `model_evaluation_retraining_bible` responsibility; this bible documents the trigger/source/destination chain only.

#### 4.1.9 Weekly retraining — `equine-weekly-retrain-wr` cron

**Trigger.** EventBridge rule `equine-weekly-retrain-wr`, cron `cron(0 4 ? * MON *)`, ENABLED at lock per `architecture_overview:3.6`. (UTC Monday 04:00 — weekly schedule.)

**Source.** Same as § 4.1.8 but scoped to WR-pipeline-specific training data.

**Lambda(s) involved.** None — ECS Fargate task.

**ECS task family.** `equine-training-win-prob` per `architecture_overview:3.2`. The EventBridge target carries `EcsParameters.TaskDefinitionArn = arn:aws:ecs:us-east-1:584812014683:task-definition/equine-training-win-prob` per `architecture_overview:3.6` (WR-specific weekly retrain).

**Destination.** Same artifact path layout as § 4.1.8, scoped to the WR family.

**Currently functional.** ECS task family + rule both at expected operational state.

**Note on `equine-weekly-retrain-pl`.** A symmetric weekly PL-retrain rule (`equine-weekly-retrain-pl` targeting `equine-training-pl`) exists in EE's EventBridge inventory but is **DISABLED** at lock per `architecture_overview:3.6`. Documented at § 7 Deprecated below, NOT here at § 4.1.9 — this sub-section is scoped to currently-firing weekly retrain flows only.

**Forward cross-reference.** Retrain mechanics canonical home: `model_evaluation_retraining_bible:4`.

### 4.2 Data Acquisition Honesty Protocol (per META_PLAN v9 § 7.9)

Per BIBLE_STRUCTURE_SPEC v6 § 6.2 + META_PLAN v9 § 7.9: each source enumerates **what the source provides**, **current reliability state** (verified empirically, not assumed), **failure manifestation**, **current acquisition mode** (autonomous / monitored / scheduled-manual / paid-replacement per META_PLAN v9 § 3.5 disposition vocabulary), and **honest disposition** (what the mode SHOULD be, with rationale). Conditional fields fire as noted.

#### 4.2.1 HRN entries

**What the source provides.** Daily race-card entry data per (track, date) tuple: race conditions (distance, surface, purse, race class), entry list (horse, jockey, trainer, post position, weight, morning-line odds, scratched flag), and parent-row identity for `tracks` / `horses` / `trainers` / `jockeys`. Populates `entries` + parent-row tables on the daily ingestion flow per § 4.1.1.

**Current reliability state.** Empirically verified 2026-05-06 via dashboard endpoint (per `architecture_overview:3.5` + `database_schema_bible:V1-12` substrate): `counts.entries = 198390`; `latest_date = 2026-05-03`. Current reliability: dashboard substrate shows entries last refreshed `2026-05-03` — gap of `3` days from patch time; consistent with Bug #7 compound failure history per § 4.2.3 + impaired ingestion flow per § 4.1.1 (fire-and-fail per `architecture_overview:6`). Bug #7 compound failure history (per META_PLAN v9 § 1.2) remains the dominant historical concern; current row-freshness state is documented above for honest at-lock disposition. Compounding the source-level reliability gap, the daily ingestion flow at § 4.1.1 is **fire-and-fail at lock** — `equine-ingestion` Lambda is INACTIVE per `architecture_overview:3.1`, so even when the HRN source is reachable, no fresh `entries` rows are written via the `equine-ingestion-daily` cron.

**Failure manifestation.** When the source is partially reachable, HRN scrape returns sparse or shape-shifted data; downstream FK violations or NULL-column rows result. When the source is unreachable, HRN scrape produces no rows; downstream stages (inference) operate against stale entries. Under the current INACTIVE-Lambda condition, no scrape attempts run; downstream stages see the most recent successful scrape's rows (no movement post-2026-05-02).

**Current acquisition mode.** Autonomous (intended) → effectively NON-FUNCTIONAL at lock (Lambda INACTIVE). Per META_PLAN v9 § 3.5 vocabulary, the current mode is best characterized as "currently broken" pending re-activation.

**Honest disposition.** Re-activation pending an explicit `PHASE_5_BACKLOG.md` entry. Re-activation alone does not resolve the upstream Bug #7 surface; that is separately tracked.

#### 4.2.2 HRN results

**What the source provides.** Post-race results per (track, date, race_number) tuple: finishing positions, win/place/show payouts, exacta/trifecta/superfecta payouts, daily double payout, pool sizes, beaten lengths, final time. Populates `results` rows on the nightly results fetch flow per § 4.1.2.

**Current reliability state.** **Severely compromised.** Bug #28 (HRN scraper column-shift defect at `hrn_scraper.py:802-804`) is the dominant honest-disposition concern. Per PHASE_5_BACKLOG.md Phase 5.3.1: 2026-04-29 was the last clean day at 9/10 win-payout success; from 2026-04-30 onward all `win_payout` and `daily_double_payout` rows are NULL. Substantive description at § 8.W.1 + § 8.W.2 in this bible.

The DD pool extraction at `hrn_scraper.py:814` (the pool-table loop) carries the same defect class (positional column indexing without column-header verification — see § 5.1 candidate Forbidden Pattern); whether the underlying root cause is identical to § 8.W.1's column-shift or distinct is documented at § 8.W.2. The PHASE_5_BACKLOG.md Phase 5.3.1 entry tracks both as a single Phase 5.3.1 item (DD pool extraction status verification listed as a Phase 1-tracking dependency).

Compounding: § 4.1.2 (the flow that runs this scrape) is **fire-and-fail at lock** — same INACTIVE-Lambda mechanism as § 4.1.1.

**Failure manifestation.** Pre-INACTIVE-state (rows written 2026-04-30 → 2026-05-02): `results.win_payout` and `results.daily_double_payout` are NULL across every track/race scraped via HRN; `place_payout` stores values that should be in `win_payout`; `show_payout` stores values that should be in `place_payout`. Place, show, and exacta payouts still populate (verbatim per operator memory file's symptom statement; inherited via PHASE_5_BACKLOG.md Phase 5.3.1 per Claim 15c pattern). Post-INACTIVE-state (post 2026-05-02): no rows written at all (fire-and-fail).

**Current acquisition mode.** Autonomous (intended) → effectively "currently broken in production" per PHASE_5_BACKLOG.md Phase 5.3.1.

**Honest disposition.** Pending Phase 5.3.1 fix (HRN page structure verification + parser repair + backfill of affected rows). The `equine-ingestion` Lambda re-activation is a separate dependency for the post-2026-05-02 fire-and-fail window; the Bug #28 column-shift fix targets the parser logic that ran during the 2026-04-30 → 2026-05-02 window.

#### 4.2.3 HRN workouts

**What the source provides.** Daily workout data per horse (training-track location, date, distance, time, surface condition). Populates `workouts` rows for non-NYRA tracks (NYRA-track workouts come from § 4.2.4).

**Current reliability state.** Empirical verification attempted 2026-05-06 via dashboard endpoint (per `architecture_overview:3.5` + `database_schema_bible:V1-12` substrate): dashboard exposes counts for races/horses/entries/results/past_performances/predictions but does NOT expose `counts.workouts` at the `/dashboard/metrics` route (verified verbatim per PHASE 1 Empirical Check 1 in V1-N entries below). Asserted from Bug #7 (HRN workout scraper failures per memory file `project_ee_bug_7_hrn_workout_scraper_expanded.md`) — not empirically verified at lock for `workouts` row freshness; empirical verification deferred to credential-authorized cycle when DB-direct query of `workouts` row counts + latest workout-row date is accessible. Three compounding scraper failures documented per Bug #7: (a) DEBUG-level logs hidden, (b) slug separator drift hyphen→underscore, (c) workouts not on `/horse/<slug>` URL anymore. Bug #7 is canonically homed elsewhere (Phase A3.5 per the memory file); the source-level reliability state is "broken" per the asserted-not-empirical historical record.

**Failure manifestation.** Workouts table sees thin or absent rows for non-NYRA-track horses in the affected window; downstream feature engineering observes lower workout-coverage rates for non-NYRA tracks.

**Current acquisition mode.** Autonomous (intended) → degraded (Bug #7).

**Honest disposition.** Pending Phase A3.5 per Bug #7 disposition.

#### 4.2.4 NYRA workouts

**What the source provides.** NYRA-track workout data via NYRA-published endpoints. Populates `workouts` rows for NYRA tracks (Aqueduct, Belmont Park, Saratoga).

**Current reliability state.** Empirically verified 2026-05-06 via two-source check:
  1. Lambda runtime State per `architecture_overview:3.1`: `equine-nyra-workouts` Active (memory 512 MB, timeout 300s).
  2. NYRA endpoint reachability per PHASE 1 Empirical Check 2: HTTP `200` against `https://www.nyra.com/aqueduct/racing/workouts/?detail=2026-05-06` at patch time 2026-05-06. URL pattern is `https://www.nyra.com/{track_slug}/racing/workouts/?detail={target_date_iso}` per `backend/lambdas/nyra-workouts/handler.py:138`.
  3. Dashboard substrate per `architecture_overview:3.5`: dashboard exposes counts for races/horses/entries/results/past_performances/predictions but does NOT expose `counts.workouts` at the `/dashboard/metrics` route (verified verbatim per PHASE 1 Empirical Check 1 in V1-N entries below); workout-row freshness deferred to credential-authorized cycle.

Current reliability: NYRA endpoint reachable (HTTP 200) + Lambda Active confirms the endpoint and runtime State are in good order; workout-row freshness in DB cannot be empirically confirmed at lock from dashboard substrate alone (counts.workouts not exposed). The flow at § 4.1.4 is the only § 4.1.X flow at lock with both Lambda State Active AND source endpoint reachability empirically confirmed.

**Failure manifestation.** No current failure manifestation documented at lock.

**Current acquisition mode.** Autonomous.

**Honest disposition.** Autonomous (matches current mode). No disposition change needed.

#### 4.2.5 Equibase chart parser path

**What the source provides.** Post-race PDF charts via S3 `equine-raw-data` bucket; the chart parser extracts enrichment columns (fractional times, beaten lengths, run-up distances, pace figures) for `results` rows. Equibase charts are the canonical post-race source of truth where they are available; HRN results provides the same surface less reliably.

**Current reliability state.** **Compromised by INACTIVE-Lambda mechanism.** The chart parser entry point (`backend/services/chart_parser.py` exposes `run_from_s3`) is invoked via the `parse_charts` admin action on `equine-ingestion` (handler at `backend/lambdas/ingestion/handler.py:542` entry per V1-9 substrate). `equine-ingestion` is INACTIVE at lock per `architecture_overview:3.1`; therefore the chart parser is non-functional via the production invocation path until the Lambda is re-activated.

**Failure manifestation.** Manual `aws lambda invoke` of `equine-ingestion` with `parse_charts` payload returns `ResourceNotReadyException` ("The function is trying to use a deleted image"). Pre-INACTIVE-state behavior: chart parser was operationally functional via manual invocation; cadence was operator-discretionary (no EventBridge schedule).

**Current acquisition mode.** Scheduled-manual (intended; pre-INACTIVE-state) → effectively "currently broken" pending Lambda re-activation.

**Honest disposition.** Re-activation pending an explicit `PHASE_5_BACKLOG.md` entry that addresses `equine-ingestion` re-activation. The chart parser itself does not appear to have its own outstanding bug history at lock; the impairment is wholly downstream of the Lambda-State invariant.

#### 4.2.6 `equibase_probe/` exploratory work

**What the source provides.** Three probe-script families (`option_a2_probe.py`, `option_b_probe.py`, `option_d_probe.py` plus `probe.py` and 4 Dockerfiles) exploring alternative Equibase acquisition strategies (CAPTCHA-bypass, residential proxies, etc.). The probe scripts consume the `equine-equalizer/2captcha-api-key` and `equine-equalizer/brightdata-api-key` Secrets Manager entries per `architecture_overview:3.8`.

**Current reliability state.** **Not in production.** Per `architecture_overview:3.7` (the `equine-equibase-acquisition` ECR repository row): zero production code readers in `backend/` or `infrastructure/` (verified via `grep -rln equine-equibase-acquisition backend/ infrastructure/` returning only documentation files at the Architecture Overview v3 lock). Per `architecture_overview:3.8` (Secrets Manager rows): zero production-Lambda consumers of 2captcha + brightdata secrets. Substrate evidence at V1-10. The 4 probe-script families and 4 Dockerfiles in `equibase_probe/` exist as exploratory work that has not been promoted to a deployed Lambda or ECS task.

**Failure manifestation.** Not applicable — no production runtime exists.

**Current acquisition mode.** Exploratory (no production runtime).

**Honest disposition.** Pending Phase 5 disposition decision per META_PLAN v9 § 3.5 vocabulary: kill (delete the probe directory + its Secrets Manager entries) / paid-replacement (promote one option to production) / scheduled-manual (run probes on a manual cadence for ongoing capture). The current zero-production-consumer state is a 2-vector cost: the Secrets Manager entries cost storage; the probe directory carries unused code complexity. Disposition is `PHASE_5_BACKLOG.md` work pending an explicit entry.

### 4.3 Invocation pathway diagnostics — EventBridge → Lambda divergence signature

The 22 invocation-class alarms (per `architecture_overview:3.10`) detect Lambda Errors/Throttles + EventBridge cron-absence + Lambda-invocations-absence; they do NOT detect the divergence signature where EventBridge fires successfully AND Lambda async invocation is dropped silently. Phase A-prime diagnostic 2026-05-11 confirmed the gap substrate: `AWS/Events` `Invocations`=1 every day 2026-04-27 → 2026-05-11 for results-related rules (zero `FailedInvocations`), but `AWS/Lambda` `AsyncEventsDropped` > 0 on 2026-05-04 → 2026-05-08 (4-of-4 daily for `equine-ingestion`; 1-of-1 daily for `equine-results`) and on 2026-05-11 04:00 UTC for `equine-results` (1-of-1 dropped, pre-Phase-β-2 restoration at 13:58Z UTC). Drop attribution: Lambda `State=Inactive` due to ECR image cull per § 3.11.1 of `architecture_overview`; async invocations to Inactive Lambdas drop after 6-hour `MaximumEventAgeInSeconds` default with no DLQ destination (`aws lambda get-function-event-invoke-config` returns ResourceNotFoundException for both `equine-ingestion` and `equine-results` at v1-patched-d lock — no event-destination config exists on either). Three relevant metrics at the EventBridge → Lambda boundary: (1) `AWS/Events::Invocations` (rule firings; dimension `RuleName`); (2) `AWS/Lambda::AsyncEventsReceived` (events delivered to Lambda async queue; dimension `FunctionName`); (3) `AWS/Lambda::Invocations` (function executions; dimension `FunctionName`). Steady-state: signal 1 ≈ signal 2 ≈ signal 3 + `AsyncEventsDropped`. Failure signature: 1 = 2 > 3 with `AsyncEventsDropped` > 0. Diagnostic checklist when ingestion silently stops: (a) check EventBridge rule state + `AWS/Events::Invocations`; (b) check `AWS/Lambda::Invocations` same window; (c) check `AsyncEventsReceived` + `AsyncEventsDropped` for divergence; (d) on divergence: `aws lambda get-function` → `State` + `LastUpdateStatus` (`State=Inactive` indicates cull recurrence per § 3.11.1 banking); (e) CloudTrail event history for `UpdateFunctionCode`/`UpdateFunctionConfiguration`/`DeleteFunction`/`PutFunctionConcurrency` targeting the affected Lambda + AttachRolePolicy/DetachRolePolicy/PutRolePolicy on the execution role; (f) Lambda Service Quotas (`L-B99A9384` Concurrent executions; EE = 1000 default at this lock). Outcome alarms (per `architecture_overview:3.10` extension; 3 alarms deployed 2026-05-11) close the gap independently by measuring end-of-pipeline row presence (results + entries DB rows) and S3 object presence (workouts) — detecting failure even when invocation-class alarms remain green (the async-drop case where signal 1 ≥ 1 leaves `*-invocations-absence` un-triggered, but downstream rows/objects = 0).

**Root cause resolution (Phase A-prime targeted fix CC 2026-05-11).** Async events are dropped at Lambda function-level admission control. With no DLQ destination configured, the only ground-truth signal of the drop is `AWS/Lambda::AsyncEventsDropped` — drops leave no captured event artifact for post-hoc inspection of what was dropped. The 2026-05-04 → 2026-05-08 outage was reconstructible only because the diagnostic CC computed `AsyncEventsReceived − AsyncEventsDropped ≈ 0` daily; the individual events themselves are unrecoverable. The 2026-05-09 OCRC Fix 4/6 `UpdateFunctionCode` events on both Lambdas (CloudTrail-verified) reset whatever init-time admission-control state had been poisoning delivery — the actual code-level proximate cause was NOT investigated at OCRC; mitigated by redeploy alone. **Durable fix (this dispatch): Lambda async event invoke config applied to both `equine-ingestion` and `equine-results`, OnFailure routing to shared SQS DLQ `equine-async-failure-dlq` (ARN `arn:aws:sqs:us-east-1:584812014683:equine-async-failure-dlq`). MaximumRetryAttempts=2 (AWS default preserved). MaximumEventAgeInSeconds=3600 (tightened from 6 hr default — ingestion cadence is daily, an event older than 1 hr is past useful window; aggressive retry timeout means DLQ message arrives quickly and pages quickly). Lambda execution roles `EquineComputeStack-IngestionFunctionServiceRoleBEA1-XH5nDS6UEvc3` and `EquineComputeStack-ResultsFunctionServiceRoleD637EE-oHseSEGvKf3M` carry inline policy `AsyncDLQSend` granting `sqs:SendMessage` on the DLQ ARN. DLQ depth alarm `equine-async-dlq-messages-present` (`AWS/SQS::ApproximateNumberOfMessagesVisible`; threshold > 0; Period 300 s; TreatMissingData notBreaching) routes to SNS `equine-equalizer-alerts` and pages within ≤ 5 min of first drop. ORPHAN classification — CLI deploy; not in CDK source.** Diagnostic checklist when async drops recur post-fix: (i) `aws sqs receive-message --queue-url … --visibility-timeout 0 --max-number-of-messages 10` to peek captured messages without consuming (returned events include `requestContext` with the dropped event payload + `responsePayload` indicating drop reason if Lambda emitted one); (ii) inspect `AWS/Lambda::AsyncEventsDropped` daily counts vs `AsyncEventsReceived` to confirm the failure-mode signature; (iii) `aws cloudtrail lookup-events` for function-config changes in the window; (iv) inspect Lambda init-time code paths for recent commits introducing cold-start failures; (v) last resort — `UpdateFunctionCode` redeploy (OCRC Fix pattern) often resets admission-control state even without root-cause identification.

**Composite HRN-gated entries alarm (Entries-alarm HRN-gating CC 2026-05-12).** The Dispatch 1 outcome alarm `equine-entries-rows-written-today` was retired and replaced by composite alarm `equine-entries-qualifying-tracks-missing` because the original alarm produced false positives on Monday/Tuesday-dark days (no qualifying-track racing → DB legitimately has zero entries → original alarm fired daily on Mondays + Tuesdays) AND silently missed partial-ingestion failures (e.g., 8 of 11 qualifying tracks ingested, 3 dropped — original alarm sees row count > 0 and stays OK). Composite alarm pattern: two metrics in namespace `EquineEqualizer/Ingestion` — `EquineExpectedQualifyingTracksToday` (HRN ground truth: count of `QUALIFYING_TRACKS` slugs racing today per direct HRN fetch + `HRN_SLUG_TO_TRACK_CODE` mapping in `backend/shared/constants.py`) + `EquineActualQualifyingTracksWithEntriesToday` (DB ground truth: `SELECT COUNT(DISTINCT t.track_code) FROM entries e JOIN races r ON e.race_id = r.race_id JOIN tracks t ON r.track_id = t.track_id WHERE r.race_date = TODAY AND t.track_code = ANY(QUALIFYING_TRACKS)`). Alarm math: `IF(m1 > 0, m1 - m2, 0) > 0` — fires when expected > 0 AND actual < expected (deficit > 0); IF gate suppresses alarm when expected=0 (dark day). Period 300 s; TreatMissingData breaching (missing data = upstream broken). Publisher Lambda `equine-entries-tracks-publisher` (Zip; psycopg2-binary 2.9.12; combines Component 1 + Component 2 per dispatch — drafting CC deviation from "extend ingestion Lambda" spec to avoid heavyweight Docker rebuild + CDK redeploy of `equine-ingestion`; failure isolation between Expected and Actual paths preserved via independent try/except). Schedule: EventBridge `equine-entries-tracks-publisher-daily` cron `(15 11 * * ? *)` = 11:15 UTC daily (15 min after `equine-ingestion-daily` cron at 11:00 UTC — schedule deviation from dispatch literal "03:30 UTC, 30 min before existing ingestion at 04:00 UTC" because actual entries-fetch cron per `data_pipeline_bible:4.1.1` is 11:00 UTC not 04:00 UTC; 11:15 UTC publishes both metrics after entries-fetch typically completes within ~3 min per substrate 14-day median). HRN fetch-failure handling: if HRN HTTP fetch fails OR body < 1000 bytes (empty-shell detector), Lambda publishes `EquineExpectedFetchFailed=1` instead of Expected metric — composite alarm TreatMissingData=breaching then fires correctly. Slug-to-code mapping verification at deploy: all 13 slugs (11 QUALIFYING_TRACKS + 2 BEL variants `belmont-at-aqueduct` + `belmont-at-the-big-a` for current Aqueduct meet) hit HRN URL `entries-results/{slug}/2026-05-09` (Saturday — most tracks active) and returned HTTP 200 + non-empty body. ORPHAN classification — CLI deploy; not in CDK source.

**BEL/AQU mapping verdict + deeper-finding surface (BEL slug verification + bible finalization CC 2026-05-12).** Query against production DB for entries on 2026-05-08/09/10 filtered to `track_code IN ('BEL','AQU')` returned **zero rows for both codes on all three dates**. HRN substrate probe for the same three dates returned `belmont-at-aqueduct` slug ACTIVE (228 KB–262 KB body sizes; > 200 KB active threshold) and `aqueduct` slug off-season template (~119 KB) and `belmont-park` slug off-season template (~119 KB). Decision matrix branches do not cleanly match: the "Neither present" branch assumes off-season but HRN substrate refutes that for `belmont-at-aqueduct`. Substrate evidence per `hrn_scraper.py:19-65` shows existing scraper convention: `HRN_TRACK_MAP['belmont-at-the-big-a'] = 'BEL'` and `HRN_TRACK_MAP['aqueduct'] = 'AQU'`; reverse `TRACK_SLUGS['BEL'] = 'belmont-park'` (stale — belmont-park slug returns off-season template since BEL meet relocated to Aqueduct facility) and `TRACK_SLUGS['AQU'] = 'aqueduct'`. New publisher Lambda's `HRN_SLUG_TO_TRACK_CODE['belmont-at-aqueduct'] = 'BEL'` is internally consistent with the existing scraper forward mapping (both `belmont-at-the-big-a` and `belmont-at-aqueduct` → BEL); **mapping unchanged**. Deeper finding surfaced for Tony review (out of dispatch scope; flagged not fixed): `tracks` table substrate shows BEL last race 2023-07-09 + AQU last race 2026-04-26; the existing HRN scraper's reverse-mapping `BEL → belmont-park` URL construction has been hitting an off-season-template page since the Belmont meet moved to Aqueduct branded as "Belmont at the Big A", silently producing zero BEL entries for the duration of the current meet (~2 weeks at lock). The new composite alarm `equine-entries-qualifying-tracks-missing` will fire on the next active racing day where Expected (HRN-truth) ≥ 1 for BEL but Actual (DB-truth) = 0 — surfacing this pre-existing silent ingestion failure independently. **EntriesRowsToday publish path retired (concurrent with this CC).** Source code: `_count_entries_today()` helper + the `metric == "entries"` handler branch removed from `backend/lambdas/outcome_metrics/handler.py` (verbatim diff: -13 lines from `_count_entries_today` helper, -4 lines from handler branch, -1 char from error message ValueError text); Lambda redeployed via `aws lambda update-function-code`; EventBridge rule `equine-outcome-entries-check` disabled + target `outcome-entries` removed (rule artifact retained per dispatch directive). Post-redeploy canary: `aws lambda invoke {"metric":"results"}` returned StatusCode 200 + `{"metric":"results","value":0}`; `{"metric":"workouts"}` returned StatusCode 200 + `{"metric":"workouts","value":0}`; `{"metric":"entries"}` returned StatusCode 200 with `FunctionError=Unhandled` + `ValueError: Unknown metric: 'entries' (expected results|workouts)` — intentional retired-canary behavior; will not fire in production because EventBridge rule is DISABLED + targets removed.

**HRN slug verification methodology (reusable pattern; deployable at any future track-list or qualifying-tracks change).** Verification recipe: `curl -sL -A 'Mozilla/5.0' 'https://entries.horseracingnation.com/entries-results/{slug}/{active-saturday-date}' -o /dev/null -w '%{http_code} %{size_download}'`. Saturday-date selection rule: pick the most recent Saturday in the substrate window (most US thoroughbred tracks race Saturdays). Verdict thresholds at body-size dimension: **> 200 KB body ≈ ACTIVE racing day at that track**; **~119 KB body ≈ "no racing today" template page** (track recognized by HRN but dark on that date — slug is valid for the mapping); **< 1000 bytes ≈ empty-shell** (likely HRN broken or slug malformed — fail). All three thresholds verify slug recognition; only the empty-shell case indicates a mapping problem. Reference example — 13-slug verification table (Entries-alarm HRN-gating CC 2026-05-12; probe date 2026-05-09 Saturday): `churchill-downs → CD` (200 290,551 B, ACTIVE); `saratoga → SAR` (200 119,077 B, off-season); `keeneland → KEE` (200 119,077 B, off-season); `belmont-park → BEL` (200 119,077 B, off-season — classic-Belmont location dormant); `belmont-at-aqueduct → BEL` (200 262,818 B, ACTIVE — current meet); `belmont-at-the-big-a → BEL` (200 262,820 B, ACTIVE — alias of preceding; identical body bytes); `santa-anita-park → SA` (200 231,646 B, ACTIVE); `gulfstream-park → GP` (200 256,665 B, ACTIVE); `del-mar → DMR` (200 119,078 B, off-season); `oaklawn-park → OP` (200 119,077 B, off-season); `monmouth-park → MTH` (200 218,381 B, ACTIVE); `aqueduct → AQU` (200 119,077 B, off-season — current Belmont meet is under `belmont-at-aqueduct` slug, NOT `aqueduct`); `pimlico → PIM` (200 119,077 B, off-season). Methodology output is the `HRN_SLUG_TO_TRACK_CODE` dict in `backend/shared/constants.py:6-19`. Re-run on QUALIFYING_TRACKS expansion or HRN URL-scheme change.

---

## 5. Discipline rules [candidate roster pending QB ratification per § 5.7]

Per BIBLE_STRUCTURE_SPEC v6 § 5.7 candidate-roster workflow: this section enumerates candidate Forbidden Patterns and Common Mistakes scoped to data-acquisition discipline. Numeric sub-section IDs per § 5.5 + G-new-1; candidate status conveyed by the section header marker, NOT by letter-prefix.

### 5.1 [candidate] Forbidden Pattern: Positional column indexing in scrapers without column-header verification

**Rule.** Scraper code that extracts data from web tables MUST verify column position against table headers before indexing cells positionally. Indexing by raw integer position (e.g., `cells[0]`, `cells[2]`, or a helper that wraps `cells[idx].get_text(...)` for a fixed `idx`) without first reading the table's `<th>` headers and resolving each target column's index dynamically produces a defect class that fails silently when the upstream page structure changes (e.g., when a new icon column is added to the left of the data columns).

**Rationale.** Bug #28 (canonically homed at § 8.W.1 + § 8.W.2 in this bible) is the worked example. The HRN scraper's `parse_payout(N)` calls at `backend/services/data_sources/hrn_scraper.py:802-804` (`parse_payout(1)`, `parse_payout(2)`, `parse_payout(3)` for win/place/show payouts respectively) and the pool-table-loop cell indexing at `hrn_scraper.py:819-820` (`cells[0]` for pool name, `cells[2]` for payout text) both use positional cell indexing without consulting the row's header structure. When HRN added an icon column to the payouts table circa 2026-04-30 (presumed cause per PHASE_5_BACKLOG.md Phase 5.3.1), every positional index shifted off-by-one; `win_payout` and `daily_double_payout` rows have been NULL across every track/race scraped via HRN since.

**FORBIDDEN example** (paraphrased from `hrn_scraper.py:785-804`):

```python
def parse_payout(idx):
    if idx < len(cells):
        txt = cells[idx].get_text(strip=True).replace('$', '').replace(',', '')
        try:
            return float(txt)
        except ValueError:
            return None
    return None

results.append({
    'finish_position': i + 1,
    'win_payout':   parse_payout(1),  # POSITIONAL — assumes column 1 is win
    'place_payout': parse_payout(2),  # POSITIONAL — assumes column 2 is place
    'show_payout':  parse_payout(3),  # POSITIONAL — assumes column 3 is show
})
```

**CORRECT example** (sketch; column-header-aware extraction):

```python
def find_column_idx(headers, name):
    for i, h in enumerate(headers):
        if name in h.lower():
            return i
    return None

headers = [th.get_text(strip=True) for th in table.find_all('th')]
win_idx = find_column_idx(headers, 'win')
place_idx = find_column_idx(headers, 'place')
show_idx = find_column_idx(headers, 'show')

results.append({
    'finish_position': i + 1,
    'win_payout':   parse_payout(win_idx) if win_idx is not None else None,
    'place_payout': parse_payout(place_idx) if place_idx is not None else None,
    'show_payout':  parse_payout(show_idx) if show_idx is not None else None,
})
```

**Substrate provenance.** PHASE_5_BACKLOG.md Phase 5.3.1 entry; META_PLAN v9 Appendix A.5 (Bug #28 worked example); this bible's § 8.W.1 + § 8.W.2; substrate evidence at verification log V1-3 + V1-4.

### 5.2 [candidate] Common Mistake: Producer-side parent-row verification before child INSERTs

**Wrong instinct:** *"the FK constraint will catch missing parents at INSERT time, so I don't need to check parent existence in the producer."*

**Corrected position:** NO. FK violations from the database surface a runtime error that aborts the producer's transaction; they are not a discoverability mechanism for missing parents. Producer code that inserts a child row whose parent does not exist must defensively assert the parent first — typically via `INSERT INTO <parent> ... ON CONFLICT DO NOTHING` followed by the child INSERT — rather than rely on the FK constraint to surface the gap. The FK constraint is a backstop, not a contract.

**Rationale.** This rule was forward-deferred from `database_schema_bible:5` per Tony's Q3.3.c ratification 2026-05-05 (see `database_schema_bible.md` § 5 lead paragraph + the forward-deferral note at end of § 5 in that bible). The deferral routes the rule to this bible because the rule's primary subject (producer code that inserts child rows from upstream sources) lives in the data pipeline domain. Specifically: ingestion-side scrapers (HRN entries scrape, NYRA workouts scrape, chart parser) consume external data and must ensure parent `tracks` / `horses` / `trainers` / `jockeys` rows exist before child `entries` / `workouts` / `results` rows can land.

**FORBIDDEN example** (sketch):

```python
# Producer assumes parent row exists; FK violation aborts the transaction
cur.execute("""
    INSERT INTO entries (entry_id, race_id, horse_id, jockey_id, ...)
    VALUES (%s, %s, %s, %s, ...)
""", (entry_id, race_id, horse_id, jockey_id, ...))
# If horse_id does not exist in horses, FK violation; transaction aborts.
```

**CORRECT example** (sketch):

```python
# Defensively assert each parent first
cur.execute("""
    INSERT INTO horses (horse_id, name, ...) VALUES (%s, %s, ...)
    ON CONFLICT (horse_id) DO NOTHING
""", (horse_id, horse_name, ...))
# Then insert child
cur.execute("""
    INSERT INTO entries (entry_id, race_id, horse_id, ...)
    VALUES (%s, %s, %s, ...)
""", (entry_id, race_id, horse_id, ...))
```

**Substrate provenance.** Forward-deferral note at `database_schema_bible.md` § 5 lead paragraph + the "Forward deferral note (Tony's Q3.3.c ratification 2026-05-05)" paragraph at end of § 5.2 in that bible. No standalone bug entry has yet pinned this candidate; promoting to a § 5.2 ratified entry is QB → Tony decision per § 5.7.

---

## 6. Currently Open

Cross-cutting bugs whose substantive description is canonically homed in this bible's domain, plus one-line cross-references for cross-cutting bugs whose canonical home is elsewhere but whose symptoms touch this bible's domain.

**Bug #28 — HRN scraper column-shift defect (canonical home: this bible at § 8.W.1 + § 8.W.2; PHASE_5_BACKLOG.md Phase 5.3.1).**

Per BIBLE_STRUCTURE_SPEC v6 § 5.3 cross-cutting bug scope rule: when a cross-cutting bug is canonically homed in a bible AND currently open at lock, the canonical-home bible's § 6 carries the substantive Currently-Open description; non-canonical-home bibles' § 6 carry one-line cross-references. Bug #28 is canonically homed here; the substantive description follows.

- **Substrate.** PHASE_5_BACKLOG.md Phase 5.3.1 entry (created 2026-05-04; ACTIVE; severity MATERIAL; surfaced 2026-05-03 during EE_CURRENT_STATE_DUMP generation; stable-known classification provisional pending Phase 1 audit verification).
- **Manifestation.** `results.win_payout` and `results.daily_double_payout` are NULL across every track/race scraped via HRN since 2026-04-30. `place_payout` stores values that should be in `win_payout`; `show_payout` stores values that should be in `place_payout`. Place, show, and exacta payouts still populate. **[Substrate evolution per v1-patched-d (2026-05-11):** Post-2026-05-02 the `equine-ingestion` Lambda was INACTIVE per `architecture_overview:3.1` v3-patched-a substrate so no fresh `results` rows were written via the HRN-scrape flow at all during the 2026-05-02 → 2026-05-09 window. OCRC Phase A informal recovery 2026-05-09T04:37Z UTC restored equine-ingestion Active state per `architecture_overview:6` v3-patched-b historical retention block. **At v1-patched-d lock (2026-05-11): equine-ingestion is Active per V16 SP-resume substrate; the HRN-scrape flow at § 4.1.2 now writes column-shifted rows DAILY pending Phase 5.3.1 fix.** Bug #28 impact severity has escalated since v1-patched-c lock per restored-Lambda + still-broken-scraper combination — column-shifted-row accumulation resumes daily; backfill scope expands per day until fix lands.]
- **Operator-verified external source** (per META_PLAN v9 verification log Claim 15c pattern; verbatim quote inherited from PHASE_5_BACKLOG.md Phase 5.3.1):
  > "starting 2026-04-30, all results.win_payout and results.daily_double_payout rows are NULL across every track/race scraped via HRN. Place, show, and exacta payouts still populate."
  > "DD pool extraction (hrn_scraper.py:814 'pool' table loop) likely has the same root cause — same site-wide column shift."
- **Phase 5 disposition.** `Phase 5.3.1` per PHASE_5_BACKLOG.md (real identifier; not a placeholder). Re-classification trigger: if Phase 1 audit verifies backfill is feasible AND DD pool extraction is bounded, the provisional qualifier drops at audit-lock time. If backfill is NOT feasible (or DD pool extraction reveals additional uncovered loss), Bug #28 re-classifies per PHASE_5_BACKLOG.md Phase 5.3.1's re-classification trigger paragraph.
- **Bible cross-references.** § 8.W.1 (canonical W.N entry for the column shift at `hrn_scraper.py:802-804`); § 8.W.2 (canonical W.N entry for the DD pool extraction nuance at `hrn_scraper.py:814`); § 5.1 (candidate Forbidden Pattern that prevents recurrence). `database_schema_bible:6` carries the one-line non-canonical-home cross-reference per § 5.3.

**Fire-and-fail anomaly cross-reference.**

> Fire-and-fail anomaly: canonical home `architecture_overview:6` (rewritten at v3-patched-b 2026-05-11 with anomaly fully retracted per R8.3 Option B historical retention block; zero ENABLED rules target Inactive Lambdas at v3-patched-b lock per V16–V22 substrate; structural mitigation at `architecture_overview:3.11.1` ECR lifecycle policy override `imageCountMoreThan: 5` → 30).

This bible is non-canonical-home for the cross-runtime invariant; the one-line cross-reference above satisfies the § 5.3 non-canonical-home discipline. **[v1-patched-d refresh per C7 (sub-cycle 2 of 4): At v1-patched-c lock, this cross-reference described 4 ENABLED rules → 2 INACTIVE Lambdas anomaly substrate-current at v1-patched-c. At v1-patched-d lock, anomaly retracted upstream per v3-patched-b § 6 historical retention; this bible's per-flow narratives at § 4.1.1, § 4.1.2, § 4.1.6, § 4.1.7 also retracted from "Currently impaired" → "Currently functional" with R8 Option B historical retention markers per C1/C2/C5/C6 patches. Cross-reference text refreshed to point at v3-patched-b § 6 historical retention block per cohort cascade scope.]**

**Empty-section explicit per § 5.2.** No additional Currently Open entries at lock canonically homed in this bible's domain.

---

## 7. Deprecated

Three DISABLED EventBridge rules carry the deprecation surface for this bible per `architecture_overview:3.6` DISABLED table. Per BIBLE_STRUCTURE_SPEC v6 § 6.2 conditional clause + § 5.6.4 conditional triggers: each rule is DISABLED-not-removed at lock; removal disposition is Phase 5 work pending an explicit `PHASE_5_BACKLOG.md` entry.

### 7.1 `equine-feature-engineering-daily` (DISABLED)

- **Cron:** `cron(0 12 * * ? *)`.
- **Target at lock:** zero current targets (`aws events list-targets-by-rule --rule equine-feature-engineering-daily` returned empty Targets list at the Architecture Overview v3 lock; per `architecture_overview:3.6` DISABLED table). Originally targeted `equine-feature-engineering` (INACTIVE Lambda per `architecture_overview:3.1`); the target was removed at some point and the rule was disabled.
- **Reason DISABLED.** Operator-disabled when feature-engineering moved inference-side per Phase A3 (per `architecture_overview:3.6` DISABLED table). Feature engineering now runs inside the per-pipeline inference Lambdas (WR / PL / LS) per `architecture_overview:4.2` discussion of dynamic attribute attachment.
- **Status.** DISABLED-not-removed at lock. Removal disposition: Phase 5 work pending an explicit `PHASE_5_BACKLOG.md` entry.
- **Cross-reference.** `architecture_overview:3.6` (per-rule target verification; canonical home for the DISABLED-rule inventory).

### 7.2 `equine-inference-daily` (DISABLED)

- **Cron:** `cron(30 12 * * ? *)` (note: the cron expression collides with the active `equine-wr-inference-daily` cron at the same minute; the rule being DISABLED prevents the collision from firing at lock).
- **Target at lock:** zero current targets per `architecture_overview:3.6` DISABLED table. Originally targeted `equine-inference` (Active Lambda) for the legacy generic-inference EventBridge path.
- **Reason DISABLED.** Replaced by per-pipeline rules `equine-{wr,pl,ls}-inference-daily` (the 3 rules at § 4.1.5 in this bible). The legacy generic-inference path is dead; per-pipeline rules dispatch to the per-pipeline Active Lambdas.
- **Status.** DISABLED-not-removed at lock. Removal disposition: Phase 5 work pending an explicit `PHASE_5_BACKLOG.md` entry.
- **Cross-reference.** `architecture_overview:3.6` (per-rule target verification).

### 7.3 `equine-weekly-retrain-pl` (DISABLED)

- **Cron:** `cron(0 5 ? * MON *)`.
- **Target at lock:** ECS task family `equine-training-pl` (target ARN: cluster `equine-cluster`; `EcsParameters.TaskDefinitionArn = arn:aws:ecs:us-east-1:584812014683:task-definition/equine-training-pl`) per `architecture_overview:3.6` DISABLED table.
- **Reason DISABLED.** Operator-disabled (PL retrain currently in `equine-daily-retrain-full` umbrella; standalone weekly suspended). Per `architecture_overview:3.6`. The rule's target ECS task family `equine-training-pl` exists at `architecture_overview:3.2` and is not invoked from any other current EventBridge rule.
- **Status.** DISABLED-not-removed at lock. Re-activation OR removal disposition is `model_evaluation_retraining_bible:4` responsibility (the question of "should PL have its own weekly retrain?" is a retrain-cadence question).

**Empty-section explicit per § 5.2.** No additional Deprecated entries at lock canonically homed in this bible's domain.

---

## 8. What Was Fixed — Do Not Revert

This section is the canonical home for Bug #28 per BIBLE_STRUCTURE_SPEC v6 § 5.3 (data-acquisition discipline most directly prevents recurrence). Per Tony's Item 2 ratification 2026-05-05: § 8.W.1 (column shift at `hrn_scraper.py:802-804`) and § 8.W.2 (DD pool extraction nuance at `hrn_scraper.py:814`) are drafted as separate W.N entries by default; FRAMEWORK_GAP F.1 (verification log Section F) surfaces the substrate observations bearing on the collapse-or-stand decision for QB → Tony ratification.

### 8.W.1 HRN scraper column-shift defect at `parse_payout` calls (Bug #28; fixed YYYY-MM-XX)

- **Bug #N.** 28 (existing global identifier per BIBLE_STRUCTURE_SPEC v6 § 5.5.1; PHASE_5_BACKLOG.md Phase 5.3.1).
- **Fix date.** Placeholder per META_PLAN v9 § 7.3 + Appendix A scope clause (forward-looking discipline codification; fix has not landed at lock — Bug #28 status is "open" per PHASE_5_BACKLOG.md).
- **Symptom.** Per PHASE_5_BACKLOG.md Phase 5.3.1 manifestation block:
  - `results.win_payout` is NULL across all rows from 2026-04-30 onward.
  - `results.daily_double_payout` is NULL across the same range.
  - `results.place_payout` stores values that should be in `win_payout`.
  - `results.show_payout` stores values that should be in `place_payout`.
  - Place, show, and exacta payouts still populate per the operator memory file's symptom statement.
- **Operator-verified external source** (per META_PLAN v9 verification log Claim 15c pattern; verbatim quote inherited from PHASE_5_BACKLOG.md Phase 5.3.1):
  > "starting 2026-04-30, all results.win_payout and results.daily_double_payout rows are NULL across every track/race scraped via HRN. Place, show, and exacta payouts still populate."
- **Root cause.** HRN page structure changed circa 2026-04-30 (likely added an icon column to the payouts table). The `parse_payout(N)` calls at `backend/services/data_sources/hrn_scraper.py:802-804` use positional cell indexing that has been off-by-one ever since. Substrate evidence (verbatim source code) at verification log V1-3:
  ```python
  'win_payout':      parse_payout(1),
  'place_payout':    parse_payout(2),
  'show_payout':     parse_payout(3),
  ```
  The `parse_payout` helper itself is defined at `hrn_scraper.py:785` and does `cells[idx].get_text(strip=True)` — purely positional cell indexing with no header lookup.
- **Fix.** Pending per PHASE_5_BACKLOG.md Phase 5.3.1 disposition. Fix shape is column-header-aware extraction per § 5.1 candidate Forbidden Pattern's CORRECT example (resolve target column indices dynamically by reading the table's `<th>` headers; index `cells[idx]` only at the resolved index for each named target column).
- **Why this entry exists.** Prevents recurrence of "positional column indexing in scrapers without column-header verification" — codified at § 5.1 candidate Forbidden Pattern.
- **Conditional triggers** (per BIBLE_STRUCTURE_SPEC v6 § 5.6.1.2 tertiary-state notation):
  - **if-fix-involved-migration: DOES NOT FIRE.** Scraper bug; no schema migration involved in the fix.
  - **if-fix-invalidated-prior-content: DOES NOT FIRE.** No prior bible content existed at fix time (this bible is v1 first cycle; bug not yet fixed at lock).
  - **if-fix-produced-Forbidden-Pattern: FIRES.** Cross-reference to § 5.1 candidate Forbidden Pattern pending QB ratification.
  - **if-fix-touches-multiple-bibles: FIRES.** Symptoms touch `database_schema_bible:4.1.9` (NULL columns on `results` rows). Per BIBLE_STRUCTURE_SPEC v6 § 5.3, `database_schema_bible:6` carries the one-line cross-reference; canonical home remains this bible per the data-acquisition-discipline-most-directly-prevents-recurrence rule.

### 8.W.2 HRN scraper DD pool extraction nuance at `hrn_scraper.py:814` ([Bug #N TBD — pending Phase 5.3.1 fix-time substrate verification]; fixed YYYY-MM-XX)

**Disposition deferral (Tony-ratified 2026-05-06).** The § 8.W.1 / § 8.W.2 collapse-vs-stand disposition AND § 8.W.2's global Bug #N assignment are both deferred to Phase 5.3.1 fix-time substrate verification. Substrate-grounded honest state at lock: two code paths show the same defect class (positional column indexing without column-header verification per § 5.1 candidate Forbidden Pattern); whether the root cause is literally identical (single upstream HRN icon-column shift affecting both result-table and pool-table rows) OR distinct (separate HRN page-structure changes hitting two surfaces) is verifiable only at fix time when live HRN page inspection lands per `Phase 5.3.1` "Dependencies" in `PHASE_5_BACKLOG.md`. Per META_PLAN v9 § 2.1 (bibles document what IS, not speculation), this entry stands as separate at lock with disposition pending. When Phase 5.3.1 fix lands, the bible re-ratifies via patch cycle: if root cause is identical → § 8.W.2 collapses into § 8.W.1 with adjacent prose covering pool extraction manifestation, no Bug #N assigned; if root cause is distinct → § 8.W.2 stands separately and gets a new monotonic global Bug #N per BIBLE_STRUCTURE_SPEC v6 § 5.5.1.

- **Bug #N.** [Bug #N TBD — pending Phase 5.3.1 fix-time substrate verification]. Per Tony's Item 2 ratification routing: drafting CC does NOT assign a new global Bug #N here per BIBLE_STRUCTURE_SPEC v6 § 5.5.1 monotonic rule. Substrate verification at V1-4 surfaces observations bearing on the collapse-or-stand decision; FRAMEWORK_GAP F.1 (verification log Section F) presents candidate reframings with substrate citations supporting both stand-alone and collapse dispositions.
- **Fix date.** Placeholder per META_PLAN v9 § 7.3 + Appendix A scope clause.
- **Symptom.** Per PHASE_5_BACKLOG.md Phase 5.3.1 verbatim:
  > "DD pool extraction (hrn_scraper.py:814 'pool' table loop) likely has the same root cause — same site-wide column shift."
- **Root cause** (substrate-evidenced; final disposition pending QB → Tony ratification per F.1). Substrate at verification log V1-4 confirms `hrn_scraper.py:814` is the entry point of the pool-table-loop block:
  ```python
  if any('pool' in h for h in headers):
      for row in table.find_all('tr')[1:]:
          cells = row.find_all('td')
          if len(cells) < 3:
              continue
          pool = cells[0].get_text(strip=True).lower()
          payout_txt = cells[2].get_text(...)
  ```
  The block uses positional cell indexing (`cells[0]` for pool name; `cells[2]` for payout text) **without column-header verification within the row** — only the table-identification check `any('pool' in h for h in headers)` is header-aware. The defect class is the same as § 8.W.1 (positional column indexing without column-header verification → § 5.1 candidate Forbidden Pattern). Whether the root cause (the specific HRN page structure change of circa 2026-04-30) propagates to this code path identically to § 8.W.1's results-table loop OR distinctly is not substrate-determinable without HRN-page-structure inspection (Phase 5.3.1 scope per PHASE_5_BACKLOG.md "Dependencies" sub-section). FRAMEWORK_GAP F.1 in the verification log surfaces both candidate dispositions with substrate citations.
- **Fix.** Pending per PHASE_5_BACKLOG.md Phase 5.3.1 disposition (the entry currently includes "DD pool extraction status verification (Phase 1 Data Pipeline Bible audit's job)" as a Phase 1-tracking dependency).
- **Why this entry exists.** Same prevention rule as § 8.W.1 — § 5.1 candidate Forbidden Pattern.
- **Conditional triggers** (per BIBLE_STRUCTURE_SPEC v6 § 5.6.1.2):
  - **if-fix-involved-migration: DOES NOT FIRE.**
  - **if-fix-invalidated-prior-content: DOES NOT FIRE.**
  - **if-fix-produced-Forbidden-Pattern: FIRES.** Cross-reference to § 5.1 candidate Forbidden Pattern.
  - **if-fix-touches-multiple-bibles: CONDITIONAL.** If DD-pool extraction populates a column on `results` (per `database_schema_bible:4.1.9`) that is currently NULL or column-shifted, the symptom touches `database_schema_bible`. Substrate verification of which `results` column the DD pool data populates is Phase 5.3.1 scope; this bible's flow-context observation is that the producer code path at `hrn_scraper.py:814+` writes pool-table data into the `results` row dict alongside the parse_payout-derived payout fields.

**Empty-section explicit per § 5.2.** No additional W.N entries at lock canonically homed in this bible's domain.

---

## End of Data Pipeline Bible v1-patched-d (LOCKED — Phase 1 deliverable 3 of 7; locked 2026-05-11 via cross-bible re-lock ceremony at parent EE Bible Upstream-Correction Cycle exit). Cross-bible cross-reference freeze re-engaged 2026-05-11; cohort coherent post-cycle exit (7-bible Phase 1 cohort per architecture_overview footer enumeration). Finding 1 § 4.1.4 closure substrate-grounded; § 4.2.4 deferred to Phase A re-dispatch venue.

Companion verification log NEW: `_audit/data_pipeline_bible_v1_patched_d_verification.md` (DRAFT pending cohort-locked audit-CC per R15 Option B; V27 substrate-stability re-confirmation 2026-05-11T14:58:02Z UTC; sub-cycle 2 of 4 cascade documentation). v1-patched-c lock-state companion verification log preserved verbatim per banked Lesson § 4.17 (locked bibles preserve drafting-time historical context); only v1-patched-c → v1-patched-d delta captured in NEW log per surgical-cosmetic-patch convention.

**Cross-bible cross-reference freeze status at v1-patched-d (2026-05-11):** LIFTED via Tony Option α 2026-05-09 (parent EE Bible Upstream-Correction Cycle scope per R14.3 Option B ratification 2026-05-11); re-locks at Database & Schema Bible UC sub-cycle 4 close (parent cycle exit). This bible operated inside lifted-state window for cross-reference contract refresh per sub-cycle 2 of 4 cascade scope (7 patches C1-C7 applied per R14.2 Option A scope; § 4.2 Data Acquisition Honesty Protocol NOT in scope; § 4.2.4 substrate refresh deferred to Phase A re-dispatch venue).

**Cohort handoff:** Sub-cycle 4 (Database & Schema Bible UC; per R14.3 Option A scope) is the next dispatch per parent cycle scope. Cohort-locked audit-CC fires post-sub-cycle-2 close per R15 Option B; audits sub-cycle 1 v3-patched-b + sub-cycle 1.5 v1-patched-a + sub-cycle 2 v1-patched-d drafts end-to-end before any lock-CC ratification.

**Finding 1 closure determination (parent cycle-entry trigger ratification 2026-05-11):** Per § 4.1.4 Finding 1 closure block above, the original substrate-refutation of "currently functional" NYRA disposition claim has been resolved via OCRC Fix 3 NYRA cron retiming (`cron(0 10 * * ? *)` → `cron(0 16 * * ? *)` 2026-05-09) per v3-patched-b § 3.6 line 150 A5 substrate. § 4.2.4 closure deferred to Phase A re-dispatch venue per R14.2 Option A scope exclusion.
