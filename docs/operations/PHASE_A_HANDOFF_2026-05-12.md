# Phase A Session Handoff — 2026-05-12

**Session**: Phase A operational recovery (data gap recovery + DLQ coverage + predictions-deficit alarm class + filter trace + producer attribution + 5-source enumeration)
**Authored**: 2026-05-12 (UTC-4); break-before-D5 per Z1 ratification
**Status**: Phase A operationally complete; D5 + D6 + close-out remaining (~2-3 dispatches)
**Successor session scope**: D5 daily ingestion runbook → D6 bundled bible patches → Phase A close-out → Phase B entry

---

## Section 1 — Phase A Operational State (Verbatim Final)

### 1.1 — 5 Operational Sources (D4 Inventory)

| # | Source | Producer | Schedule (UTC) | Tables | DLQ |
|---|---|---|---|---|---|
| 1 | HRN entries | equine-ingestion Lambda (default action) | cron(0 11 * * ? *) = 11:00 | entries, races, horses, trainers, jockeys, tracks, past_performances | ✅ |
| 2 | HRN results | equine-ingestion Lambda (action=fetch_results) | cron(30 1 * * ? *) = 01:30 | results | ✅ (inherited from Lambda) |
| 3 | NYRA workouts | equine-nyra-workouts Lambda | cron(0 16 * * ? *) = 16:00 | workouts (via S3 → load_workouts_from_s3) | ✅ (A.5-ext) |
| 4 | Equibase workouts | /home/strakajagr/equibase_scraper/run_daily_refresh.sh (local cron) | 0 3 * * * (03:00 EDT = 07:00 UTC) | workouts (via S3 → load_workouts_from_s3) | N/A (out-of-band) |
| 5 | Equibase charts | /home/strakajagr/equibase_scraper/download_charts.py | Same cron entry as Source 4 | PDF charts to s3://equine-raw-data/charts/ | N/A (out-of-band; FAILING DAILY exit=1) |

**Source 2 architecture clarification** (D4 substrate correction): HRN-results-scraping is `equine-ingestion` Lambda's `fetch_results` action, NOT `equine-results` Lambda. The `equine-results` Lambda is a separate matcher/reconciliation Lambda (Appendix B; updates `wr_predictions.actual_finish` against arriving results; NOT data ingestion).

### 1.2 — 6-Lambda DLQ Coverage Final Tally

All 6 async-drop-affected Lambdas in operational ingestion + inference pipeline:

| Lambda | Role | event-invoke-config | AsyncDLQSend policy |
|---|---|---|---|
| equine-ingestion | EquineComputeStack-IngestionFunctionServiceRoleBEA1-XH5nDS6UEvc3 | ✅ Phase A-prime | ✅ |
| equine-results | EquineComputeStack-ResultsFunctionServiceRoleD637EE-oHseSEGvKf3M | ✅ Phase A-prime | ✅ |
| equine-nyra-workouts | equine-nyra-workouts-role | ✅ A.5-ext (2026-05-12T01:09:13-04:00) | ✅ A.5-ext |
| equine-wr-inference | EquineComputeStack-WRInferenceFunctionServiceRole50-3h7rtE6J9Zwg | ✅ A.5 | ✅ |
| equine-pl-inference | EquineComputeStack-PLInferenceFunctionServiceRoleE9-AicisfzONYB9 | ✅ A.5 | ✅ |
| equine-ls-inference | EquineComputeStack-LSInferenceFunctionServiceRoleAC-ogxzjOvAqKNG | ✅ A.5 | ✅ |

**All**: `OnFailure → arn:aws:sqs:us-east-1:584812014683:equine-async-failure-dlq`, retry=2, age=3600.

**DLQ depth alarm**: `equine-async-dlq-messages-present` (Phase A-prime); currently OK.

### 1.3 — 29 Alarms Inventory + Source Mapping

| # | Alarm | Maps to |
|---|---|---|
| 1 | equine-async-dlq-messages-present | DLQ (covers Sources 1+2, Appendix B matcher, 3 inference Lambdas, NYRA workouts) |
| 2 | equine-entries-qualifying-tracks-missing | Source 1 (composite output watcher) |
| 3 | equine-feature-engineering-errors | Appendix A2 (ORPHAN) |
| 4 | equine-feature-engineering-throttles | Appendix A2 (ORPHAN) |
| 5 | equine-fetch-results-nightly-cron-absence | Source 2 (cron rule absence) |
| 6 | equine-inference-errors | Appendix A1 (DISABLED rule; orphan-watching) |
| 7 | equine-inference-throttles | Appendix A1 (DISABLED rule; orphan-watching) |
| 8 | equine-ingestion-daily-cron-absence | Source 1 (cron rule absence) |
| 9 | equine-ingestion-errors | Sources 1+2 (Lambda-level) |
| 10 | equine-ingestion-throttles | Sources 1+2 (Lambda-level) |
| 11 | equine-ingestion-invocations-absence | Sources 1+2 (Lambda-level) |
| 12 | equine-ls-inference-errors | Phase B LS inference |
| 13 | equine-ls-inference-throttles | Phase B LS inference |
| 14 | equine-ls-predictions-deficit | Phase B LS inference (A.5 deliverable; composite math alarm) |
| 15 | equine-nyra-workouts-errors | Source 3 |
| 16 | equine-nyra-workouts-throttles | Source 3 |
| 17 | equine-nyra-workouts-invocations-absence | Source 3 |
| 18 | equine-nyra-workouts-daily-cron-absence | Source 3 |
| 19 | equine-pl-inference-errors | Phase B PL inference |
| 20 | equine-pl-inference-throttles | Phase B PL inference |
| 21 | equine-pl-predictions-deficit | Phase B PL inference (A.5 deliverable) |
| 22 | equine-results-errors | Appendix B matcher |
| 23 | equine-results-invocations-absence | Appendix B matcher |
| 24 | equine-results-rows-written-today | Source 2 (output watcher) |
| 25 | equine-results-throttles | Appendix B matcher |
| 26 | equine-workouts-objects-written-today | Shared: Source 3 + Source 4 (S3-object-presence) |
| 27 | equine-wr-inference-errors | Phase B WR inference |
| 28 | equine-wr-inference-throttles | Phase B WR inference |
| 29 | equine-wr-predictions-deficit | Phase B WR inference (A.5 deliverable) |

**4 orphan-watching alarms**: #3, #4, #6, #7 (feature-engineering Lambda + inference legacy Lambda; neither has an active invocation source).

### 1.4 — 3 Orphan Lambdas + 4 Orphan-Watching Alarms (Post-Phase-B CDK Reconciliation Bundle)

**Appendix A1 — equine-inference (legacy)**:
- Code: `backend/lambdas/inference/handler.py`
- EventBridge rule: `equine-inference-daily cron(30 12 * * ? *)` — **DISABLED**
- Status: Deprecated; superseded by WR/PL/LS inference per `architecture_overview:3.1 v3-patched-a UC-1`
- Orphan-watching alarms: equine-inference-errors, equine-inference-throttles
- Disposition: Retirement candidate; bundled with post-Phase-B CDK reconciliation pass

**Appendix A2 — equine-feature-engineering (ORPHAN)**:
- LastModified: 2026-05-12T04:38:17Z (mechanically rebuilt by A.5.3 CDK deploy; not invoked)
- EventBridge rules targeting: ZERO (full scan of 22 ENABLED rules)
- Disabled-rule check: `equine-feature-engineering-daily` exists in DISABLED state
- Last 14d invocations: 1 (incidental; not from a recurring source)
- Orphan-watching alarms: equine-feature-engineering-errors, equine-feature-engineering-throttles
- Disposition: Retirement candidate; bundled with post-Phase-B CDK reconciliation pass

**Appendix B — equine-results matcher Lambda (clarification not deprecated)**:
- Code: `backend/lambdas/results/handler.py`
- EventBridge rule: `equine-results-daily cron(0 4 * * ? *) = 04:00 UTC` ENABLED
- Function: Prediction matching/reconciliation (updates `wr_predictions.actual_finish` etc.); NOT data ingestion
- Last 7d invocations: 2 (May 9: 1; May 11: 2; sparse)
- Disposition: Phase B input candidate (sparse-by-design vs silently-broken-on-5-of-7-days classification per F-D4-2-β ratification)

### 1.5 — All Phase A Deliverables Status

| Deliverable | Owner | Status |
|---|---|---|
| Recovery scripts (D2/D3 backfill) | Tony | ✓ COMPLETE; 1,882 rows UPSERTed (843 D3 + 1039 D2) |
| BEL fix end-to-end verification (May 7/8) | Tony | ✓ COMPLETE |
| CDK deploy bundle (Q-T1 V2 colspan + BEL forward+reverse) | CC + Tony | ✓ COMPLETE; commit 9b96f0d; EquineComputeStack 119.37s |
| rerun_inference 11-day window | Tony | ✓ COMPLETE; 33/33 OK, 7min wall-clock |
| Predictions spot-check 8 dates | CC | ✓ COMPLETE; WR=PL=LS exactly; multi-style inventory confirmed |
| A.6.a NYRA TypeError diagnostic | CC | ✓ COMPLETE; V-N2 caller-side tuple-unpack mismatch identified |
| A.6.b NYRA fix bundle | CC + Tony | ✓ COMPLETE; manual_nyra_workouts.py authored + SAR smoke test 48 workouts |
| A.6.d workouts source architecture diagnostic | CC | ✓ COMPLETE (with framing errors corrected by A.6.f) |
| A.6.f workouts producer attribution verification | CC | ✓ COMPLETE; V-P1 confirmed (Equibase sibling-repo cron, not HRN) |
| A.6.c races_processed + ambient delta diagnostic | CC | ✓ COMPLETE; D1 disposition (intentional architectural filter) |
| A.5 inference DLQ + 3 predictions-deficit alarms | CC + Tony | ✓ COMPLETE; 9 substrate mutations |
| A.5.1 predict_race filter trace + Expected SQL refinement | CC | ✓ COMPLETE; PREDICT_RACE_TOLERANCE=5 applied |
| A.5.2 build_entry_features trace + May 1 forensic | CC | ✓ COMPLETE; D1-defect + D2-γ variant classified |
| A.5.3 gonzo_features int(NaN) surgical fix | CC + Tony | ✓ COMPLETE; commit e1d6d4a; CDK deploy 122.41s; 9/9 horses recovered |
| A.5-ext NYRA workouts DLQ wiring | CC + Tony | ✓ COMPLETE; F-D4-1-α closed |
| D4 5-source operational status enumeration | CC | ✓ COMPLETE; C-5 confirmed |

### 1.6 — 2 Open Threads (Both Deferred per Ratifications)

**Open Thread 1 — Equibase chart-failure disposition**:
- `download_charts.py` failing daily with exit=1, new_pdfs=0 across 3 captured days
- SNS_TOPIC_ARN set in cron env; SNS alerts MAY be firing daily to equine-equalizer-alerts topic
- Tony decision pending: bundle-to-D6 + standalone post-Phase-A diagnostic OR bundle-to-D6 + SNS-delivery-investigation
- Independent thread; not blocking Phase A close-out

**Open Thread 2 — Matcher Lambda sparse-invocation classification**:
- `equine-results` matcher Lambda fired 2 of 7 days in last week (May 9 + May 11)
- Per F-D4-2-β: documented in D6 as Phase B input candidate
- Classification needed at Phase B substrate review: sparse-by-design (matcher only runs on race-results-arriving days) vs silently-broken-on-5-of-7-days

---

## Section 2 — D6 Queue Verbatim (All Bible Patch Content Authored Explicitly)

### 2.1 — § 4.2 Data Acquisition Honesty Protocol — 6 Pattern Entries

**Pattern entry 1 — D2 cosmetic bug (entries-summary key mismatch)**:
- Substrate location: scripts/backfill_d2.py
- Defect: D2 read `entries_inserted` key from service-summary dict; service returned `races_stored` key
- Classification: code-passes-review-without-implementation-reality-verified
- Disposition: Fixed in A.6.b bundle alongside NYRA TypeError

**Pattern entry 2 — NYRA handler docstring vs implementation mismatch**:
- Substrate location: backend/lambdas/nyra-workouts/handler.py
- Defect: `fetch_track_page` and `parse_nyra_html` return 2-tuples per implementation; docstrings claim singular returns
- Classification: documentation-not-substrate-grounded
- Disposition: D6 documentation candidate; bundle with post-Phase-B CDK reconciliation pass

**Pattern entry 3 — A.6.d source misattribution (HRN inferred → Equibase actual)**:
- Substrate trace: A.6.d CC report inferred "Tony's local HRN scrape ~4000 rows/day" from log signals + IAM-role attribution
- Actual producer (A.6.f verification): /home/strakajagr/equibase_scraper/run_daily_refresh.sh — sibling repo, Equibase scraper, not HRN
- Classification: inference from operational signal promoted to substrate-verified fact without explicit Tony confirmation
- Disposition: foundational case study for producer-attribution methodology refinement (see § 2.2 below)

**Pattern entry 4 — HRN CAPTCHA framing not substrate-grounded**:
- Substrate location: backend/services/data_sources/hrn_workout_scraper.py:66
- Pre-A.6.d framing assumed CAPTCHA-gating on HRN workouts scraper; substrate proves "no CAPTCHA or bot-protection"
- Classification: dispatch-text framing inherited from session memory, not substrate-verified
- Disposition: D6 documentation

**Pattern entry 5 — D4 Source 2 conflation**:
- Substrate trace: QB D4 dispatch text described Source 2 as "equine-results Lambda; cron 04:00 UTC via equine-fetch-results-nightly post-OCRC Input fix"
- Actual architecture (D4 substrate verification):
  - HRN-results-scraping = equine-ingestion Lambda's fetch_results action @ 01:30 UTC via equine-fetch-results-nightly rule
  - Separate Appendix B = equine-results matcher Lambda @ 04:00 UTC via equine-results-daily rule (reconciliation, not data ingestion)
- Classification: QB framing of operational architecture not substrate-verified before propagating to dispatch text; ratified-by-Tony scope inherited the conflation
- Disposition: D6 documentation; methodology refinement reinforced

**Pattern entry 6 — A.5-ext API step-ordering**:
- Substrate trace: A.5-ext CC executed dispatch text in literal order (Step 2 event-invoke-config before Step 3 IAM policy)
- Failure: PutFunctionEventInvokeConfig validates `sqs:SendMessage` permission at API time; failed with InvalidParameterValueException
- Recovery: reapply Step 2 after Step 3 succeeded; passed on first retry; no IAM-propagation lag observed
- Classification: dispatch-text-prescribed step ordering not always equivalent to API-required step ordering; A.5 happened to execute in correct dependency order (CC discretion) which masked this defect in earlier dispatches
- Refinement: QB dispatch-text must specify step ordering per API dependency requirements, not per logical-deliverable order
- Disposition: D6 documentation + AWS API validation discipline entry (see § 2.3 below)

### 2.2 — Producer-Attribution Methodology Refinement

**Refinement statement**: Producer attribution at IAM-role level (OCRC-class finding) does not establish operational-producer attribution. When QB or CC infers daily-operational behavior from substrate evidence (S3 writes, IAM role usage patterns, log line timestamps, code-symmetry between training and inference), the inference must be explicitly flagged as inference — NOT propagated as substrate-verified fact. Explicit Tony confirmation required to promote inference to operational reality.

**Five case studies documented across Phase A**:

1. **A.6.c ambient delta speculation → DB-state-verified absence**: rerun_inference summary reported "LS=152 vs WR/PL=151"; speculation classified as "coupled-entry / AE handling artifact"; A.6.c discriminating-entries query returned zero rows; speculation disproven.

2. **A.6.d → A.6.f workouts producer attribution**: A.6.d inferred "Tony's local HRN scrape" from log signals + OCRC IAM-role attribution; Tony correctly identified inference vs operational reality; A.6.f verification surfaced actual producer (/home/strakajagr/equibase_scraper/run_daily_refresh.sh sibling-repo Equibase scraper); methodology refinement banked.

3. **A.5.2 gonzo defect classification**: D1-defect verdict required substrate trace through 11 compute_* helpers + CloudWatch logs forensic + 'Tapit Shoes' discriminator analysis; classification not inferred from code-symmetry alone.

4. **A.5.3 checkpoint #11 training behavior inference**: CC claimed "training-time same-helper run will silently filter same NaN rows" from code-symmetry; methodology refinement applied prophylactically — claim recognized as inference-not-substrate-verified; deferred to Phase B substrate review of training pipeline.

5. **D4 Source 2 architecture conflation**: QB framing of equine-ingestion fetch_results action vs equine-results matcher Lambda was not substrate-verified before propagating to D4 dispatch text; CC verified independently and surfaced correction.

### 2.3 — AWS API Validation Discipline Entry

**Substrate fact**: AWS Lambda's `PutFunctionEventInvokeConfig` API validates the target role's `sqs:SendMessage` permission at API time, BEFORE event-invoke-config takes effect. If the role lacks the permission, the API call fails with `InvalidParameterValueException`.

**Operational discipline**: For DLQ wiring across mixed greenfield/brownfield roles, IAM grant must precede event-invoke-config, sequentially — never parallel/chained.

**Dispatch-text discipline**: QB dispatch text must specify step ordering per API dependency requirements:
- ❌ Wrong: "Step 2: Apply event-invoke-config; Step 3: Apply IAM AsyncDLQSend policy"
- ✅ Right: "Step 2: Apply IAM AsyncDLQSend policy; Step 3: Apply event-invoke-config"

**Banked instances**:
- Phase A-prime DLQ wiring (5 Lambdas): executed correctly (CC discretion masked dispatch-text inversion)
- A.5 DLQ wiring (3 Lambdas): executed correctly (CC discretion)
- A.5-ext DLQ wiring (1 Lambda): executed in dispatch-text order; surfaced the dependency requirement

**Future scope**: Any future Lambda DLQ wiring dispatch must use correct API-dependency-order in dispatch text.

### 2.4 — Race-Eligibility Filter Architecture (A.6.c Verdict)

**Substrate location**: `backend/services/race_repository.py:66-94` (SQL filter) + WR/PL `_inference_service.py` (in-memory field-size filter)

**Filter composition** (3 components, all intentional):

1. **F-race-type (SQL)**: `r.race_type = ANY(QUALIFYING_RACE_TYPES)` where `QUALIFYING_RACE_TYPES = ['allowance', 'allowance_optional_claiming', 'stakes', 'graded_stakes']` (per `backend/shared/constants.py`)
2. **F-claim-price (SQL)**: `r.race_type = 'claiming' AND r.claiming_price >= MIN_CLAIMING_PRICE` where `MIN_CLAIMING_PRICE = 15000` (per constants.py; git commit 3185103 tightened from earlier value)
3. **F-field-size (in-memory)**: `if len(race.entries) < 4: continue` at WR/PL inference service iterations; LS inherits via wr_predictions read + adds `is_scratched=FALSE` filter

**Empirical impact on May 2 substrate** (A.6.c evidence):
- 59 qualifying-track races total
- 37 PROCESSED
- 22 EXCLUDED: 10 maiden_claiming (F-race-type) + 8 maiden (F-race-type) + 4 claiming-below-$15K (F-claim-price); 0 field-size exclusions

**Architectural classification**: D1 disposition (intentional architectural filter; correct behavior; no fix needed).

### 2.5 — predict_race Internal Filter (A.5.1/A.5.2/A.5.3 Substrate)

**Substrate location**: `backend/services/feature_engineering_service.py:94-116` (catch-all exception filter) + `model/shared/gonzo_features.py:558` (post-A.5.3 NaN guard)

**Pre-A.5.3 defect**: `compute_gonzo_class_features` at `gonzo_features.py:561` and `:566` performed `int(f)` on `at_or_above_finishes` list elements without NaN-handling; ValueError caught by outer try/except at `feature_engineering_service.py:110`; entry silently dropped.

**Filter classification**: F-side-effect (exception-handler-based, not field-driven, heterogeneous failure modes).

**A.5.3 fix** (commit e1d6d4a):
- File: `model/shared/gonzo_features.py:558` filter expression
- Change: `if t >= today_tier and pp_finishes[i] is not None and not pd.isna(pp_finishes[i])`
- 1 file changed, 13 insertions, 2 deletions
- CDK deploy 122.41s (7 Lambda asset hash + 1 ECS TaskDef replace)
- 9 affected horses recovered: LatetotheGame, Toga d'Oro, Anmer Hall, On the Hill, Vancougar, MakerandSons, City Blocks, Tap Me a Song, Tapit Shoes
- 7 predictions recovered across 5 dates (May 2, 3, 7, 8, 10); per-date deltas converged to 0
- May 1 -2 delta persists (D2-γ scratched-after-prediction surplus; architectural)

**Upstream gap flagged**: `_load_raw_pps` SQL filter is `WHERE finish_position IS NOT NULL AND finish_position < 90` per docstring at `gonzo_features.py:499-501`; empirical evidence suggests pandas coercion of SQL-NULL or empty-string sentinel → NaN during `pd.read_sql_query` despite SQL-side filter; defense-in-depth at helper level is operationally correct; upstream gap investigation is Phase B candidate.

**PREDICT_RACE_TOLERANCE=5** (interim defense-in-depth):
- Location: `backend/lambdas/entries_tracks_publisher/handler.py` module constant
- Rationale: max observed positive delta (+3 on May 3) + 2 safety buffer
- A.5.4 reduction candidate: after 2-4 weeks observation post-A.5.3, reducible to 0 or 1
- Retained at 5 post-A.5.3: defense-in-depth for future feature-engineering edge cases beyond the documented gonzo NaN class

### 2.6 — Workouts Source Architecture (A.6.f Findings)

**Two daily producers feeding `workouts` table via shared S3 → load_workouts_from_s3 hop**:

**Producer 1 — NYRA Lambda cron @ 16:00 UTC**:
- Lambda: `equine-nyra-workouts`
- Coverage: SAR, BEL, AQU only
- S3 path: `s3://equine-raw-data/workout-loads/{YYYYMMDD}_nyra_{YYYYMMDD_HHMMSS}.json`
- Architectural: ORPHAN (CLI-deployed; not in CDK)

**Producer 2 — Equibase sibling-repo cron @ 03:00 EDT / 07:00 UTC**:
- Producer: `/home/strakajagr/equibase_scraper/collect_daily_workouts.py` invoked by `run_daily_refresh.sh`
- Local crontab: `0 3 * * * SNS_TOPIC_ARN=arn:aws:sns:...equine-equalizer-alerts AWS_DEFAULT_REGION=us-east-1 PATH=...:/home/strakajagr/equibase_scraper/venv/bin /home/strakajagr/equibase_scraper/run_daily_refresh.sh >> /home/strakajagr/equibase_scraper/logs/cron.log 2>&1`
- Coverage: 8+ tracks per per-horse iteration (CD/GP/KEE/MTH/SA/OP plus NYRA-overlap SAR/BEL/AQU)
- S3 path: `s3://equine-raw-data/workout-loads/{YYYYMMDD}_{HHMMSS}.json` (NO `_nyra_` infix)
- Architectural: OUT-OF-BAND (sibling repo on Tony's local machine; not in `/home/strakajagr/projects/`)

**Convergence**: both producers' S3 outputs are loaded into DB via `equine-ingestion` Lambda's `load_workouts_from_s3` action.

**Tony's "local HRN scrape operational backbone" framing correction**: pre-A.6.f session memory included framing of "Tony's local HRN scrape ~4000 rows/day daily operational backbone"; A.6.f verification surfaced that no local HRN script exists; the daily producer is Equibase sibling-repo (not HRN); volume claim was misread (Lambda `inserted=N` log value is records-processed-from-JSON, not net-new-DB-inserts — UPSERT collapse yields ~12-22% of file volume as net-new rows).

### 2.7 — Q-T1 V2 Colspan Mechanism + Fix

**Substrate location**: `backend/services/data_sources/hrn_scraper.py` line 558+ (post-fix; commit 9b96f0d)

**Mechanism**: HRN entries page table layout uses `<th colspan="N">` headers spanning multiple data columns. Pre-fix parser used positional column indices; V2 fix resolves columns via colspan-aware header walk.

**Fix scope** (commit 9b96f0d):
- Colspan-aware header indexing in scraper
- BEL forward+reverse mapping for `HRN_TRACK_MAP['belmont-at-aqueduct']` + `get_track_slug()` date-conditional helper (BEL_AT_AQU_START = 2026-04-27)

### 2.8 — D1 Functionally-Inert Fix Case Study

**Context**: Bug #28 commit `3465195` (D1 verification) claimed header-resolution fix; A.5.2 substrate verification showed header-resolved indices were coincidentally identical to original positional constants — fix landed but was functionally inert.

**Classification**: code-passes-review-without-implementation-reality-verified (first instance of § 4.2 pattern).

### 2.9 — Multi-Style Inventory

- WR: 8 styles (general + 7 specialized)
- PL: 7 styles (general + 6 specialized)
- LS: 1 style (no style column; LS handler doesn't accept style per A.6.b finding)

### 2.10 — Inference Lambda DLQ + Predictions-Deficit Alarm Pattern (A.5 Architecture)

**3 per-Lambda predictions-deficit math alarms** (deliberate non-conflation per Tony's prior anti-conflation directive):
- `equine-wr-predictions-deficit`
- `equine-pl-predictions-deficit`
- `equine-ls-predictions-deficit`

**Math expression per alarm**: `IF(m1 > 0, m1 - m2, 0)` where m1 = Expected metric, m2 = Actual metric. Threshold > 0. TreatMissingData=breaching.

**6 new metrics** (added to existing `equine-entries-tracks-publisher` Lambda via A.5-α extension):
- EquineExpected{WR,PL,LS}PredictionsToday
- EquineActual{WR,PL,LS}PredictionsToday

**Cascading-failure detection**: alarm fires even when Lambda itself succeeds with empty output (LS clean-exit-empty when WR/PL upstream produces 0; alarm catches via Expected > 0, Actual = 0).

**Expected calculation** (per A.5.1 refinement): SQL mirrors A.6.c race-eligibility filter + applies PREDICT_RACE_TOLERANCE=5 post-fetch.

### 2.11 — LS Second-Pass Enrichment Architecture

**Substrate**: `ls_inference_service.py:144-260` (per A.6.c Step 1.2 substrate)

**LS does NOT iterate races independently** — second-pass enrichment reading from `wr_predictions`:

```sql
SELECT wp.prediction_id, wp.horse_id, wp.race_id, wp.entry_id, ...
FROM wr_predictions wp
JOIN entries e ON wp.entry_id = e.entry_id
JOIN races r ON wp.race_id = r.race_id
...
WHERE r.race_date = %s
  AND wp.style = 'general'
  AND COALESCE(e.is_scratched, FALSE) = FALSE
```

LS inherits WR's race set minus scratched entries. Architecturally distinct from WR + PL primary inference.

### 2.12 — Open Threads Documented as D6 Patches

**Equibase chart-failure flag**:
- Daily exit=1 with `new_pdfs=0`
- SNS_TOPIC_ARN set in cron env; SNS alerts may be firing daily
- D5 runbook documents operational expectation (chart download is non-blocking for workouts step)
- Disposition pending Tony decision on SNS-delivery-investigation vs alarm-fatigue acceptance

**Matcher Lambda sparse-invocation flag**:
- `equine-results` Lambda fired 2 of 7 days in last week
- Phase B input candidate per F-D4-2-β
- Classification needed: sparse-by-design vs silently-broken-on-5-of-7-days

### 2.13 — Workouts Source-Column Schema-Evolution Candidate

**Current state**: `workouts` table has no `source` column. Producer attribution (NYRA vs Equibase vs manual) requires substrate archaeology per A.6.f investigation.

**Proposed enhancement**: Add `source VARCHAR` column to `workouts` table with values like `'nyra'`, `'equibase'`, `'manual'`. Would enable single-SQL-query producer attribution for future investigations.

**Disposition**: D6 documentation; implementation deferred (schema migration scope; not in Phase A).

### 2.14 — Train-Test Skew Phase B Flag

**Substrate**: `model/shared/gonzo_features.py` is shared between training pipeline and inference Lambdas.

**A.5.3 fix scope**: Inference-only per F3 ratification.

**Phase B substrate review required**:
- (a) Whether training pipeline exercises `compute_gonzo_class_features` at all
- (b) Data shape at training time
- (c) Whether NaN finish_positions are present in training inputs OR pre-filtered upstream
- (d) Train-test skew characterization
- (e) Re-train decision based on above

**Annotation**: per A.5.3 methodology refinement application — CC's checkpoint #11 claim "training-time same-helper run will silently filter same NaN rows" was inference from code-symmetry, NOT substrate-verified. Phase B verifies.

### 2.15 — Sub-Finding 2 from A.5.2 (May 1 Scratched-After-Prediction Surplus)

**Substrate**: CD R13 May 1 had 17 entries total; 2 scratched ('Bella Ballerina' pgm 12, 'My Miss Mo' pgm 6); 15 active; 17 WR-general predictions (one per entry including the 2 scratched).

**Classification**: D2-γ variant (scratched-after-prediction surplus).

**Architectural correctness**: Predictions are history-preserving. Scratch event updates `entries.is_scratched=TRUE` but does NOT cascade-delete `wr_predictions` rows. Predictions persist for downstream consumers (matcher Lambda backfilling `actual_finish`, retrospective analysis, audit trail).

**Expected vs Actual asymmetry**: Expected SQL counts forward-looking active entries (post-scratch eligibility); Actual is history-preserving prediction count. Alarm math correctly handles asymmetry (negative delta → e1 negative → alarm OK).

**Disposition**: D6 documentation only; architecturally correct; no fix needed.

### 2.16 — Sub-Finding 1 from A.5.2 (build_entry_features Exception Cause Beyond Gonzo)

**Substrate**: A.5.2 trace identified ALL 9 affected horses on rerun_inference invocation hit same exception: `compute_gonzo_class_features int(NaN)`. A.5.3 fixed this. But the broader `_build_entry_features` catch-all exception handler at `feature_engineering_service.py:110` still suppresses any future heterogeneous failure mode silently.

**Phase B input candidate**: investigate whether other compute_* helpers have NaN-vulnerable or similar latent defects; characterize the exception-suppression discipline; consider per-helper explicit handling vs catch-all retention.

---

## Section 3 — Phase A Close-Out Path

### 3.1 — D5 Daily Ingestion Runbook (Tier 3 single-CC)

**Scope**: per D4 enumeration + 2 open threads documented as known operational expectations + manual recovery tools.

**Section 1 — Operational sources** (per D4 verbatim inventory):
- Source-by-source: producer / schedule / tables / alarms / DLQ
- "When this source is healthy" + "When this source has degraded" rubric per source

**Section 2 — Alarm response procedures**:
- 29 alarms × per-alarm runbook: what fired / what to check / what to do / when to escalate
- Special-handling: composite alarms (qualifying-tracks-missing, predictions-deficit, results-rows-written-today, workouts-objects-written-today)
- DLQ depth alarm (`equine-async-dlq-messages-present`): inspection procedure + replay-vs-drop decision tree

**Section 3 — Manual recovery tools**:
- `manual_nyra_workouts.py` (A.6.b deliverable): ad-hoc NYRA workouts backfill
- `backfill_d2.py` / `backfill_d3.py`: ad-hoc entries+races / results backfill (Phase A recovery scripts)
- `rerun_inference.py`: ad-hoc WR/PL/LS inference re-run for specific date range
- Usage patterns per tool: when to use, CLI args, dry-run mode, --execute mode, smoke test post-run

**Section 4 — Known operational expectations** (per 2 open threads):
- Equibase chart-failure: documented expectation that `download_charts.py` exits 1 daily; workouts step (Source 4) unaffected; SNS alerts may fire daily until disposition lands
- Matcher Lambda sparse invocation: documented expectation that `equine-results` may not fire daily; Phase B substrate review classifies sparse-by-design vs broken

**Authoring approach**: CC reads D4 enumeration + this handoff document + prior dispatch reports as substrate; produces single runbook document. SP gate halt at runbook authored + saved-diff review-ready.

### 3.2 — D6 Bundled Bible Patches (Tier 2, F.4 pattern)

**Scope**: multi-bible surgical patches per § 2 verbatim content above.

**Bundle decision at D6 dispatch authoring** (CC determines based on cross-reference impact assessment):
- **Option D6-α**: single CC dispatch covers all bible patches simultaneously
- **Option D6-β**: per-bible CC dispatches sequenced; bibles touched: `data_pipeline_bible.md` (primary), `architecture_overview.md` (inventory + cleanup-class architectural classification), `ml_layer_architecture_bible.md` (LS second-pass enrichment + multi-style inventory), possibly `database_schema_bible.md` (workouts-source-column candidate)

**Per-bible patch scope**:

`data_pipeline_bible.md`:
- § 4.1 cron-flow extension: 5-source inventory + producer/schedule/tables per source
- § 4.2 Data Acquisition Honesty Protocol: 6 pattern entries verbatim (per § 2.1 above)
- § 4.x new section: AWS API validation discipline (per § 2.3 above)
- § 4.x new section: predict_race internal filter + A.5.3 fix (per § 2.5 above)
- § 4.x new section: workouts source architecture (per § 2.6 above)
- § 4.x new section: scratched-after-prediction surplus pattern (per § 2.15 above)

`architecture_overview.md`:
- § 3.x update: 6-Lambda DLQ coverage final tally (per § 1.2 above)
- § 3.x update: race-eligibility filter architecture (per § 2.4 above)
- § 3.10 ORPHAN classification update: post-A.5-ext final state (per § 1.4 above)

`ml_layer_architecture_bible.md`:
- LS second-pass enrichment architecture (per § 2.11 above)
- Multi-style inventory (per § 2.9 above)
- Inference Lambda DLQ + predictions-deficit alarm pattern (per § 2.10 above)
- Train-test skew Phase B flag (per § 2.14 above)
- Sub-finding 1 Phase B input candidate (per § 2.16 above)

`database_schema_bible.md` (if touched):
- Workouts source-column schema-evolution candidate (per § 2.13 above)
- Matcher Lambda sparse-invocation flag → Phase B context (per § 2.12 above)

### 3.3 — Phase A Close-Out

**Brief saved-diff summary**: enumerate all Phase A deliverables (per § 1.5 above) + final operational state (per § 1.1-1.4) + 2 open threads disposition + D6 patches landed + Phase B handoff readiness.

**Closure criteria** (per Directive 2):
- All known defects + open questions in Phase A scope resolved OR documented with root cause: ✓
- All operational gaps closed OR documented as known-state: ✓
- Phase B substrate inputs explicitly flagged: ✓ (train-test skew, sub-finding 1 build_entry_features cause, matcher Lambda sparse-invocation classification)
- 2 open threads non-blocking: ✓ (Equibase chart-failure + matcher Lambda sparse)

---

## Section 4 — Phase B Entry Directive (Referenced; Full Directive Authored at Close-Out)

**Phase B scope**: ML layer analysis
- Per-layer features inventory (7-layer ensemble per session memory)
- AUCs per layer
- Ensemble contribution analysis (which layer drives which decisions)
- Strategies analysis (8 WR styles + 7 PL styles + 1 LS style behavior characterization)
- ML rebuild work (model versioning, retrain triggers, drift detection)

**Phase B ceremony**: Tier 3 cap at Phase B entry (per session memory standing directive).

**Phase B initial scope items** (from Phase A handoff):
1. Train-test skew investigation (per § 2.14 above)
2. Matcher Lambda sparse-invocation classification (per § 2.12 above)
3. Sub-finding 1 build_entry_features exception cause beyond gonzo (per § 2.16 above)

**Phase B entry handoff requirement**: fresh QB session reads this handoff document + D5 runbook + D6 bible patches + recent userMemories before Phase B dispatch authoring.

---

## Section 5 — Open Threads

### 5.1 — Equibase Chart-Failure Disposition (Tony Decision Pending)

**Substrate**: `download_charts.py` failing daily with exit=1, new_pdfs=0 across 3 captured days (May 9/10/11). SNS_TOPIC_ARN set in cron env (`arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts`); SNS alerts may be firing daily.

**Decision options** (deferred from Phase A close-out):
- (a) Bundle-to-D6 + standalone post-Phase-A diagnostic on chart-failure root cause itself (Tony receiving SNS alerts; alarm not muted)
- (b) Bundle-to-D6 + SNS-delivery-investigation post-Phase-A (Tony NOT receiving alerts; delivery path defect is urgent)
- (c) Bundle-to-D6 + accept as known operational state (Tony receiving alerts; alarm fatigue accepted; no investigation)

**Tony email-check signal**: pending.

### 5.2 — Post-Phase-B CDK Reconciliation Pass (Queued)

**Bundle scope**:
- Orphan Lambda retirement: `equine-feature-engineering` + `equine-inference` (legacy)
- Orphan alarm cleanup: 4 orphan-watching alarms (equine-feature-engineering-errors/throttles + equine-inference-errors/throttles)
- Matcher Lambda sparse-invocation diagnostic (if Phase B classifies as silently-broken)
- All CLI-only ORPHAN resources per D4 § 4.3 (3 Lambdas + 1 SQS + 5 inline policies + 30 alarms + 4 EventBridge rules + 1 ECR override)

**Ceremony**: TBD at Phase B close-out; likely Tier 2 surgical per item with batching where ratified.

---

## Section 6 — Methodology Refinement Summary

### 6.1 — § 4.2 Data Acquisition Honesty Protocol — 6 Pattern Entries Enumerated

Per § 2.1 above. Pattern entries finalized at this scope unless further D5 / D6 work surfaces additional instances.

### 6.2 — Producer-Attribution Methodology Refinement

**Statement**: Inference from operational signal (S3 writes, IAM role usage, log timestamps, code-symmetry between training and inference) does not establish operational reality. Explicit substrate verification or Tony confirmation required to promote inference to fact.

**Five case studies enumerated** per § 2.2 above.

### 6.3 — AWS API Validation Discipline

**Statement**: Dispatch-text-prescribed step ordering must match API dependency requirements, not logical-deliverable order.

**Banked instance**: A.5-ext IAM-grant-precedes-event-invoke-config rule per § 2.3 above.

### 6.4 — Tier Discrimination Operational Test

**Phase A dispatch ceremony record**: 12+ consecutive operational tests passing.
- Tier 3 single-CC ceremonies (read-only investigations + small-scope mutations): A.6.{a,c,d,f}, A.5.1, A.5.2, D4, A.5-ext
- Tier 2 ceremonies (drafting CC + Tony saved-diff review): A.6.b, A.5, A.5.3
- All ceremonies held to dispatch-text scope; halt-and-surface protocol exercised correctly when out-of-scope findings surfaced (A.5 calibration sub-finding → A.5.1, A.5.1 sub-findings → A.5.2, A.5.2 D1-defect → A.5.3, D4 F-D4-1 gap → A.5-ext)

**Discipline validation**: pattern-discipline-now bias (Directive 2: nothing deferred from Phase A scope) held across all dispatch cycles; no Phase A finding deferred to Phase B that wasn't explicitly architectural (gonzo training-side semantics, build_entry_features exception cause beyond gonzo, matcher Lambda sparse classification, upstream pandas NaN coercion mechanism).

---

## End of Handoff Document

**Phase A operational state**: Healthy. 5 sources daily-operational; 6-Lambda DLQ coverage complete; 29 alarms inventoried; 2 open threads non-blocking.

**Next session entry**: D5 daily ingestion runbook authoring (Tier 3 single-CC dispatch).

**Fresh QB session reading order**:
1. This handoff document (`docs/operations/PHASE_A_HANDOFF_2026-05-12.md`)
2. Recent userMemories (Phase A state already partially compacted in)
3. Project root bibles (current state pre-D6 patches)
4. `docs/bible/_meta/AUDIT_METHODOLOGY.md` (ceremony discipline reference)

**Resume cadence**: D5 → D6 → Phase A close-out → Phase B entry. Approximately 2-3 dispatches remaining for Phase A close-out per pre-handoff assessment.
