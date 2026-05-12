# Source Status Audit — 2026-05-08

**Cycle:** PHASE_A_2026-05-08 / Deliverable D1
**Drafting CC:** S1 (no prior conversation context)
**Status:** DRAFT — **PHASE A PAUSED 2026-05-09** pending substrate restoration. S2 adversarial audit NOT dispatched.
**Pause rationale:** S1 surfaced that production HRN ingestion has been fire-and-fail since 2026-05-02 (`equine-ingestion` Lambda INACTIVE, deleted ECR image). Phase A's 3-signal triangulation cannot complete column-level evidence collection against a dead substrate. Tony decision (2026-05-09): pause Phase A; restore ingestion first; resume once signal (a) DB evidence is collectable. S1 stands as a frozen point-in-time artifact.
**Lock time of substrate reads:** 2026-05-08 (UTC midnight had not yet passed when reads began; some Lambda-side timestamps roll into 2026-05-09 UTC due to UTC-clock probes — flagged inline where relevant).
**Resumption preconditions (when ingestion restored):** Re-execute signal (a) DB queries for all 6 sources against restored substrate; re-validate signal (b) error/success patterns over the restoration window; then dispatch S2 audit against this snapshot + the re-execution delta.

---

## 1. Substrate verification

### 1.1 Bible source list (Data Pipeline Bible § 4.2)

The brief inherited a list of **6 sources**. Verified against `data_pipeline_bible.md` § 4.2.1 through § 4.2.6:

| # | Bible source ID | Bible label                          | Brief label              | Match? |
|---|-----------------|--------------------------------------|--------------------------|--------|
| 1 | § 4.2.1         | HRN entries                          | HRN entries              | YES    |
| 2 | § 4.2.2         | HRN results                          | HRN results              | YES    |
| 3 | § 4.2.3         | HRN workouts                         | HRN workouts             | YES    |
| 4 | § 4.2.4         | NYRA workouts                        | NYRA workouts            | YES    |
| 5 | § 4.2.5         | Equibase chart parser path           | Equibase chart parser    | YES    |
| 6 | § 4.2.6         | `equibase_probe/` exploratory work   | equibase_probe           | YES    |

**No discrepancy.** The bible's § 4.2 source list is identical (in count and identity) to the brief's inherited list.

### 1.2 Brief-asserted DB access pattern

The brief specifies:

> Production DB: SELECT-only via the `equine-ingestion` Lambda `raw_query` action.

**This pattern is currently NON-FUNCTIONAL.** Verified empirically 2026-05-08:

```
$ aws lambda invoke --function-name equine-ingestion ... --payload '{"action":"raw_query","sql":"SELECT 1"}'
An error occurred (CodeArtifactUserFailedException) when calling the Invoke operation:
ERROR: Lambda cannot initialize the provided container image. Verify the image.
```

`equine-ingestion` Lambda State = `Inactive`, StateReason = `"The function is trying to use a deleted image."` since 2026-05-02 per `architecture_overview:3.1` and verified again at S1 lock time. Cross-reference `data_pipeline_bible.md` § 4.1.1 which canonically documents this. The brief's documented DB access pattern was authored under the assumption that re-activation had occurred or was about to; at S1 lock time it has not. **This is a methodological constraint on D1**: signal (a) (DB evidence) is collected via INDIRECT paths (public API at `https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com/`, served by the Active `equine-wr-inference` Lambda's API-router handler) wherever possible, and explicitly marked as DEFERRED where indirect paths cannot reach the column-level evidence required (most acutely: Bug #28 NULL-column verification on `results` rows).

PHASE_5_BACKLOG.md Phase 5.3.20 ("equine-ingestion Broken Container — CodeArtifactUserFailedException") already tracks the underlying fix; this audit's exposure is bridging-note material for D5.

### 1.3 Other substrate checks

- **Data Pipeline Bible § 4.1 flow inventory:** 9 sub-sections; 10 EventBridge rules; verified identical to `aws events list-rules` output 2026-05-08 (12 equine rules total = 10 ENABLED + 2 DISABLED, where the 2 DISABLED rules — `equine-feature-engineering-daily`, `equine-inference-daily` — and `equine-weekly-retrain-pl` are documented at § 7 Deprecated, the other 10 ENABLED at § 4.1).
- **Lambda runtime state:** `aws lambda get-function` confirms 2026-05-08:
  - INACTIVE: `equine-ingestion`, `equine-results`, `equine-feature-engineering` (3 of 8)
  - ACTIVE: `equine-nyra-workouts`, `equine-pl-inference`, `equine-wr-inference`, `equine-ls-inference`, `equine-inference` (5 of 8)
  - All 3 INACTIVE share StateReason `"The function is trying to use a deleted image."`. Tracked at PHASE_5_BACKLOG Phase 5.3.17 (3 INACTIVE Lambdas with Deleted ECR Images).
- **Bible § 4.1.1 line:104 substrate** ("INACTIVE since CDK redeploy 2026-05-02 culled its ECR image"): empirically verified — ImageUri retrieved 2026-05-08 still resolves to a CDK-managed ECR image SHA, but the underlying image tag was replaced by the 2026-05-02 redeploy and the prior tag's manifest deleted.

---

## 2. Methodology

Three signals per source per § 3.4 Q4 ratification:

- **Signal (a) — DB evidence:** trailing 14-day daily row counts + last successful ingest timestamp. Collected via indirect API paths (public `/races/{date}` and `/wr/predictions/{date}` endpoints + `/dashboard/metrics` aggregate) due to § 1.2 blocker. Column-level evidence (e.g., `results.win_payout` NULL distribution for Bug #28) is NOT reachable via these paths and is explicitly marked DEFERRED.
- **Signal (b) — Log evidence:** trailing 7-day CloudWatch scrape per source's Lambda log group. Success-marker counting via `START` filter; error filter `?ERROR ?Error ?error ?fail ?FAIL ?Failed ?Exception`.
- **Signal (c) — Dry-run / test invocation:**
  - HRN-family sources (entries, results, workouts): **DEFERRED** per brief sequencing — Bug #28 (open at PHASE_5_BACKLOG Phase 5.3.1) corrupts payout extraction; signal (c) is re-executed at S7 after S3 ships the fix.
  - NYRA workouts: executed via Lambda invoke (Active Lambda).
  - Equibase chart parser: executed via local Python import + most-recent S3 PDF (production Lambda invoke path is non-functional per § 1.2).
  - equibase_probe: NOT executed (paid-service surface; no production runtime; treated as audit observation only).

Per § 7.9 honest disposition: signals not collected are explicitly recorded as "not collected" with reason; never inferred or fabricated.

---

## 3. Per-source status

### 3.1 HRN entries (bible § 4.2.1)

**Module:** `backend/services/data_sources/hrn_scraper.py` (entry method `fetch_entries(race_date)` at line 118; called from `backend/services/ingestion_service.py` `IngestionService.fetch_daily_entries()`).

**Production trigger:** EventBridge rule `equine-ingestion-daily` cron `(0 11 * * ? *)` → Lambda `equine-ingestion` (default-case dispatch path per bible § 4.1.1).

**Canonical destination tables:** `entries` (primary writer), `races`, `horses`, `trainers`, `jockeys`, `tracks`, `past_performances` (parent rows). Timestamp column for "last ingest" purposes: `races.race_date` (the schedule's target date), not an `inserted_at` column (which is not exposed by any reachable API).

**Signal (a) — DB evidence:**

Trailing 14d daily race counts (via `GET /races/{date}` indirect path):

| Date       | Race count | Notes |
|------------|------------|-------|
| 2026-05-08 | 0          | no scrape |
| 2026-05-07 | 0          | no scrape |
| 2026-05-06 | 0          | no scrape |
| 2026-05-05 | 0          | no scrape |
| 2026-05-04 | 0          | no scrape |
| 2026-05-03 | 7          | last day with rows; partial |
| 2026-05-02 | 30         | full |
| 2026-05-01 | 30         | full |
| 2026-04-30 | 19         | partial (Bug #28 column-shift window starts) |
| 2026-04-29 | 7          | partial (last clean day per bible § 4.2.2) |
| 2026-04-28 | 7          | partial |
| 2026-04-27 | 0          | no scrape (pre-INACTIVE; gap predates Lambda image deletion) |
| 2026-04-26 | 29         | full |
| 2026-04-25 | 35         | full |

Dashboard `counts.entries = 198,390`; `counts.latest_date = 2026-05-03`. Last successful ingest = **2026-05-03** (5 days stale at lock).

**Disposition:** Severely impaired. Fire-and-fail since 2026-05-02 per bible § 4.1.1 + empirical INACTIVE state at § 1.3. The 2026-04-27 zero count predates the INACTIVE redeploy and is a separate event (consistent with bible's noted Bug #7 compound failure history per § 4.2.1).

**Signal (b) — Log evidence (`/aws/lambda/equine-ingestion`, 7d):**

- Total events 7d: 188 (concentrated 2026-05-02 → 2026-05-03)
- START events: last seen `2026-05-03T06:29:40 UTC` — no invocations after this. EventBridge cron continued to fire (rule ENABLED), but Lambda's INACTIVE state means invocations error out at the Lambda service layer before the function's log group receives any logs (`CodeArtifactUserFailedException` is a Lambda-service-side error, not a per-invocation log event).
- Notable errors observed in the 2026-05-02 → 2026-05-03 final-active window (verbatim samples, all from after the new image was deployed but before image-deletion took effect at the Lambda runtime):
  - `[ERROR] Database error: UndefinedColumn: column "distance" does not exist`
  - `[ERROR] Database error: AmbiguousColumn: column reference "race_id" is ambiguous`
  - `[ERROR] Database error: UndefinedColumn: column e.scratched does not exist`
- These three error patterns are **schema-drift defects between the deployed image's SQL and the live RDS schema** — not directly an HRN-source-reachability issue. They are operationally distinct from Bug #7 (HRN scraper) and Bug #28 (HRN scraper column-shift) and surface a NEW finding (see § 6 below).

**Signal (c) — Dry-run:** **DEFERRED** — pending Bug #28 fix (S3 → S7 sequence). Additionally, dry-run via Lambda invoke is presently impossible per § 1.2 even setting Bug #28 aside; local-import dry-run of `hrn_scraper.fetch_entries()` is technically feasible but defers to S7 per the Bug-#28-driven sequencing rationale.

**Per-source epistemic standing:** **moderate-to-low** — (a) collected indirectly with date-level granularity only (no row-level NULL audit reachable); (b) collected with new schema-drift errors surfaced; (c) deferred by sequencing AND by § 1.2 path-blocker.

---

### 3.2 HRN results (bible § 4.2.2)

**Module:** `backend/services/data_sources/hrn_scraper.py` (entry method `fetch_results(race_date)` at line 123; bug-bearing functions at lines 802-804 `parse_payout(N)` calls and lines 819-820 pool-table cell indexing).

**Production trigger:** EventBridge rule `equine-fetch-results-nightly` cron `(30 1 * * ? *)` → Lambda `equine-ingestion` (default-case dispatch — same Lambda as § 3.1).

**Canonical destination table:** `results`. Schema canonicalized at `database_schema_bible:4.1.9`. Timestamp proxy: `r.race_date` of the parent `races` row.

**Signal (a) — DB evidence:**

Dashboard `counts.results = 196,316`. The dashboard does not expose a `latest_results_date` field directly; the indirect inference is that any race date < `counts.latest_date` (2026-05-03) is the maximum possible results date. Available-dates endpoint reveals races with predictions through 2026-05-03; results state for those races is not directly readable via the API surface.

**Bug #28 NULL-distribution check:** **DEFERRED** — would require column-level SELECT against `results.win_payout`, `results.daily_double_payout`, `results.place_payout`, `results.show_payout` for race_date ∈ {2026-04-30, 2026-05-01, 2026-05-02} per bible § 4.2.2 Failure manifestation. The brief-asserted `raw_query` path is non-functional per § 1.2; the public API does not expose payout columns at any reachable endpoint inspected (`/cards/{date}/{track_code}` returns only race-level metadata, not result-row payouts).

**Disposition:** Severely impaired and undermined by two compounding mechanisms:
1. Bug #28 column-shift (canonically homed at bible § 8.W.1 + § 8.W.2; tracked at PHASE_5_BACKLOG Phase 5.3.1) — corrupts results written 2026-04-30 → 2026-05-02.
2. Fire-and-fail since 2026-05-02 — no fresh `results` rows on this flow at all.

**Signal (b) — Log evidence:** Same log group as § 3.1 (`/aws/lambda/equine-ingestion`); shared analysis. Cron at 01:30 UTC nightly continues to fire but no log events are produced post-2026-05-03 due to INACTIVE-Lambda-service-layer error. The fire-and-fail at the EventBridge → Lambda boundary is observable only by absence of logs, not by error logs in CloudWatch (consistent with bible § 4.1.2).

**Signal (c) — Dry-run:** **DEFERRED — pending Bug #28 fix (S3 → S7 sequence).**

**Per-source epistemic standing:** **low** — (a) only at aggregate-count granularity; the column-level Bug #28 disposition is unverified at this audit's lock time and is the highest-uncertainty open question in the snapshot. (b) shared analysis. (c) deferred.

---

### 3.3 HRN workouts (bible § 4.2.3)

**Module:** `backend/services/data_sources/hrn_workout_scraper.py` (entry method `fetch_workouts(...)`, line 108).

**Production trigger:** **NONE on EventBridge that S1 could discover.** No EventBridge rule named `equine-hrn-workouts-*` or similar exists (`aws events list-rules` enumerated 2026-05-08; only NYRA workouts has a dedicated daily cron at § 4.1.4). The bible (§ 4.2.3) states HRN workouts populate `workouts` for non-NYRA tracks but does NOT name a § 4.1 flow that drives this.

**Yet:** S3 prefix `s3://equine-raw-data/workout-loads/` shows daily uploads matching the HRN-workout payload schema (verbatim sample row keys: `horse_name`, `eq_refno`, `sex`, `distance_furlongs`, `workout_time`, `is_bullet`, `track_condition`, `workout_type`, `rank_on_day`, `total_works_on_day`, `workout_date`, `track_code`). Sample file `workout-loads/20260508_070049.json` (uploaded 2026-05-08T07:00:51 UTC) contains 3,180 workout records spanning multiple non-NYRA tracks (CD, etc.). Last 7 daily files (uploads at ~03:00 EDT / 07:00 UTC daily): 2026-05-02 → 2026-05-08 inclusive. **The producer is undocumented** — see § 6 New Defects.

**Canonical destination table:** `workouts` (per bible § 4.1.4 + repository at `backend/repositories/workout_repository.py:126` `INSERT INTO workouts (...)`). Timestamp column: `workout_date`.

**Signal (a) — DB evidence:**

- Dashboard `/dashboard/metrics` does NOT expose `counts.workouts` (verified per bible § 4.2.3 + re-verified 2026-05-08 against current API response — JSON body parsed; counts dict contains `races, horses, entries, results, past_performances, predictions, earliest_date, latest_date` only).
- DB-direct `SELECT COUNT(*) FROM workouts WHERE workout_date BETWEEN ... AND ...` is **DEFERRED** per § 1.2 blocker.
- S3-side proxy: 7 consecutive daily HRN-style workout files uploaded 2026-05-02 → 2026-05-08, suggesting the SCRAPE half of the pipeline runs but the LOAD half (which would invoke `equine-ingestion` `load_workouts_from_s3` action — see § 4.1 of this audit) cannot complete because the target Lambda is INACTIVE.

**Disposition:** Asserted-only-from-historical-record per bible § 4.2.3 (Bug #7 compound failures); empirical status at S1 lock time is "scrape side appears alive on S3, load side cannot complete." DB row-freshness for `workouts` table cannot be confirmed at this audit.

**Signal (b) — Log evidence:** No CloudWatch log group is associated with the HRN workouts producer (the producer is not a discoverable Lambda — see § 6.1). Ingestion-Lambda log group is shared with HRN entries/results and was scanned in § 3.1; no `load_workouts_from_s3` success or error events appear post-2026-05-03 (consistent with INACTIVE-Lambda fire-and-fail).

**Signal (c) — Dry-run:** **DEFERRED — pending Bug #28 fix per brief sequencing**, plus separate blocker that producer is undiscovered.

**Per-source epistemic standing:** **low** — (a) S3 proxy only; row-level DB freshness deferred. (b) producer log group unknown. (c) deferred.

---

### 3.4 NYRA workouts (bible § 4.2.4)

**Module:** `backend/lambdas/nyra-workouts/handler.py`. Self-contained Lambda (no shared service dependency); writes scraped workouts to S3 then invokes `equine-ingestion` `load_workouts_from_s3` action to load to RDS.

**Production trigger:** EventBridge rule `equine-nyra-workouts-daily` cron `(0 10 * * ? *)` → Lambda `equine-nyra-workouts` (Active per § 1.3).

**Canonical destination table:** `workouts`. Timestamp column: `workout_date`.

**Signal (a) — DB evidence:** Same blocker as § 3.3 — `counts.workouts` not exposed; raw_query unavailable. Deferred.

S3-side proxy of NYRA scrape success/failure (filename pattern `{date_str}_nyra_{timestamp}.json` in `workout-loads/`):

| Cron run (UTC)      | Production scrape result                            |
|---------------------|------------------------------------------------------|
| 2026-05-02 10:00    | zero workouts; S3 upload SKIPPED                    |
| 2026-05-03 10:00    | zero workouts; S3 upload SKIPPED                    |
| 2026-05-04 10:00    | zero workouts; S3 upload SKIPPED                    |
| 2026-05-05 10:00    | zero workouts; S3 upload SKIPPED                    |
| 2026-05-06 10:00    | zero workouts; S3 upload SKIPPED                    |
| 2026-05-07 10:00    | zero workouts; S3 upload SKIPPED                    |
| 2026-05-08 10:00    | zero workouts; S3 upload SKIPPED                    |

Production cron has produced **zero NYRA workouts every day for 7 consecutive days**. Verbatim log line per day: `NYRA: scraped zero workouts across all tracks; skipping S3 upload + load`.

**Signal (b) — Log evidence (`/aws/lambda/equine-nyra-workouts`, 7d):**

- 88 events / 8 START events 7d (one per day cron + 3 S1 manual probes 2026-05-09 03:54 UTC).
- ZERO error-pattern matches (`?ERROR ?Error ?error ?fail ?FAIL ?Failed ?Exception` filter returned `[]`).
- Lambda completes successfully every cron firing — but with 0 workouts found. The handler's "all tracks empty" path returns statusCode 200 with `total_workouts: 0` (line 301-313 of handler.py); it does not raise. Therefore CloudWatch shows healthy execution while the data outcome is empty.

**Signal (c) — Dry-run:** **EXECUTED 2026-05-09 03:54 UTC** (UTC clock had rolled past 2026-05-08 by S1 lock time).
- Probe 1: `{"trigger_load":false}` (default-date = today UTC = 2026-05-09 at probe time): SAR 0, BEL 0, AQU 0, total 0 (consistent with: NYRA hasn't published 2026-05-09 workouts at 03:54 UTC because the racing day hasn't begun).
- Probe 2: `{"date":"2026-05-08","trigger_load":false}`: **SAR 33, BEL 159, AQU 0, total 192**. Output structure matches expected schema (per `parse_nyra_html` at handler.py:148-245 producing dicts with keys `horse_name, eq_refno, sex, workout_date, track_code, distance_furlongs, workout_time, is_bullet, track_condition, workout_type, rank_on_day, total_works_on_day`).
- Probe 3: `{"date":"2026-05-07","trigger_load":false}`: SAR 2, BEL 6, AQU 0, total 8.

**The dry-run reveals a TIMING DEFECT:** when cron fires at 10:00 UTC on date D asking for date D, NYRA returns zero workouts because workouts for date D have not yet been published (NYRA publishes workouts during morning EDT, ≈10:00-14:00 EDT = 14:00-18:00 UTC, AFTER the 10:00 UTC cron). When the same Lambda is asked at 03:54 UTC for date D-1 (i.e., the previous day, now complete), NYRA returns full workout data (192 for 2026-05-08). **All 7 daily cron runs in the window have asked for the wrong date** (today UTC) and consequently scraped zero. See § 6 New Defects.

**Caveat on signal (c) side-effect:** Probe 2 and Probe 3 each wrote a small JSON file to `s3://equine-raw-data/workout-loads/` even with `trigger_load=false`, because the handler unconditionally calls `s3.put_object` at handler.py:320-325 before the `trigger_load` branch at line 330. Two files written (≈54KB and ≈2KB respectively); S3 write was unavoidable to execute signal (c) without a code change. Brief constraints did not call out S3 writes; flagged transparently here for S2 to assess. Files are valid workout JSON; no DB writes occurred (`trigger_load=false` skipped the load Lambda invoke; even if not skipped, the load target is INACTIVE and would have errored).

**Disposition (revised vs. bible § 4.2.4):** The bible at lock time (2026-05-06) recorded NYRA as the only flow with both Active Lambda AND empirically-confirmed source reachability, with disposition "Autonomous (matches current mode). No disposition change needed." S1's signal (c) shows the bible's disposition is **partially incorrect**: source reachable, Lambda runs cleanly, but cron timing produces zero workouts every day. The autonomous mode is operating but failing to capture data. Promote disposition to "broken-autonomous: capture-time defect."

**Per-source epistemic standing:** **high** — all three signals collected; (a) S3 proxy with strong corroboration from (b) and (c); (b) clean (no errors); (c) reveals a previously undocumented capture-time defect.

---

### 3.5 Equibase chart parser (bible § 4.2.5)

**Module:** `backend/services/chart_parser.py`. Public entry: `process_pdf(conn, source, filename)` at line 1176; production wrapper `run_from_s3` referenced from `backend/lambdas/ingestion/handler.py:542` (the `parse_charts` admin action).

**Production trigger:** **None directly.** Manual via `aws lambda invoke ... '{"action":"parse_charts","track":"<code>"}'` per bible § 4.1.3.

**Canonical destination table:** `results` (enrichment columns: fractional times, beaten lengths, run-up distances, pace figures per bible § 4.1.3).

**Source-side staleness (input PDF inventory, S3 bucket `equine-raw-data/charts/{TRACK}/`):**

Most-recent PDF per track per `aws s3 ls`:

| Track | Most recent PDF      | Days stale (vs 2026-05-08) |
|-------|----------------------|----------------------------|
| AQU   | AQU_20260426.pdf     | 12                         |
| BEL   | BEL_20230709.pdf     | 1,034 (effectively never refreshed) |
| CD    | CD_20260429.pdf      | 9                          |
| DMR   | DMR_20250906.pdf     | 244                        |
| GP    | GP_20260426.pdf      | 12                         |
| KEE   | KEE_20260424.pdf     | 14                         |
| MTH   | MTH_20250914.pdf     | 236                        |
| OP    | OP_20260426.pdf      | 12                         |
| PIM   | PIM_20250517.pdf     | 356                        |
| SA    | SA_20260426.pdf      | 12                         |
| SAR   | SAR_20250901.pdf     | 249                        |

The active-meet tracks (AQU, CD, GP, KEE, OP, SA — those with PDFs from late April 2026) are 9-14 days stale. Off-meet tracks (BEL, DMR, MTH, PIM, SAR) are months-to-years stale (consistent with their racing seasons). PDF source pipeline (whatever populates `s3://equine-raw-data/charts/`) has not produced new charts since 2026-04-29 (last CD chart). This is an upstream-of-parser concern: even if the chart parser were reachable, there is no fresh substrate to parse.

**Signal (a) — DB evidence:** Same blocker as other sources — column-level SELECT (e.g., `SELECT COUNT(*) FROM results WHERE chart_parsed = true AND race_date >= NOW() - INTERVAL '14 days'`) is unavailable. Deferred at the column level. Aggregate `counts.results = 196,316` reflects accumulated history but does not isolate chart-parser-write counts.

**Signal (b) — Log evidence:** Same log group as § 3.1 (`/aws/lambda/equine-ingestion`); the chart parser is invoked via the same Lambda. No `parse_charts` action logs found in 7d (the action requires manual invoke, which has not been attempted by any operator in the trailing 7d).

**Signal (c) — Dry-run: EXECUTED locally 2026-05-08.**
- Method: copied `s3://equine-raw-data/charts/CD/CD_20260429.pdf` (160,374 bytes) to local `/tmp/test_chart.pdf`; imported `services.chart_parser` from local checkout; called `extract_all_text(...)` then `split_into_races(...)` then `parse_race_header(...)` and `parse_payout_section(...)` on each split block.
- Output: 47,567 chars extracted; 10 race blocks split; **10/10 races parsed cleanly** (every block returned a header dict with all expected keys and a payouts dict containing `wps` (per-program win/place/show) plus `exotics` (exacta, trifecta, superfecta).
- Sample race-1 payout (verbatim): `{'wps': {'1': {'win': 3.86, 'place': 2.68, 'show': 2.52}, '5': {'place': 12.52, 'show': 6.3}, '6': {'show': 3.72}}, 'exotics': {'exacta': {'combo': '1-5', 'payout': 69.42}, 'trifecta': {'combo': '1-5-6', 'payout': 66.38}, 'superfecta': {'combo': '1-5-6-8', 'payout': 21.29}}}`
- Header keys (verbatim): `track_code, race_date, race_number, race_type, race_name, conditions, grade, distance_furlongs, surface, purse, claiming_price, track_condition, temperature, weather_conditions, post_time, fractions, final_time, num_calls, runners, field_size`.

**The chart parser code itself is functional on stored substrate.** The impairment is wholly downstream of (i) Lambda INACTIVE state and (ii) upstream PDF freshness, not in parser logic.

**Disposition:** Bible § 4.2.5 disposition holds — pending `equine-ingestion` re-activation. S1 adds: parser logic is empirically clean on most-recent stored PDF; backfill scope is bounded by the freshness of the S3 PDFs, not by parser bugs.

**Per-source epistemic standing:** **high (parser logic) / moderate (production path)** — (a) deferred at column level but bounded by aggregate count; (b) shared analysis with § 3.1; (c) executed locally on real production substrate with 10/10 success.

---

### 3.6 equibase_probe (bible § 4.2.6)

**Module:** `equibase_probe/` at repo root. Four probe scripts (`probe.py`, `option_a2_probe.py`, `option_b_probe.py`, `option_d_probe.py`) plus 4 Dockerfiles.

**Production trigger:** **None.** Per bible § 4.2.6 + § 1.3 verification: zero production code readers; not on any EventBridge rule's target; not in the Lambda inventory; not in ECS task family inventory (`equine-training`, `equine-training-daily-full`, `equine-training-manual`, `equine-training-pl`, `equine-training-win-prob` — none reference equibase_probe). Secrets Manager entries `equine-equalizer/2captcha-api-key` and `equine-equalizer/brightdata-api-key` exist (per bible § 4.2.6 reference); empirical re-verification of consumer-count not performed at this audit.

**Canonical destination tables:** N/A (no production writer).

**Signal (a) — DB evidence:** N/A (no production runtime → no DB writes to evidence).

**Signal (b) — Log evidence:** No CloudWatch log group exists. Probe scripts are intended for ad-hoc local execution.

**Signal (c) — Dry-run:** **NOT EXECUTED** — three reasons stated:
1. Probes consume paid third-party services (2Captcha at ≈$0.001-0.003/solve; Bright Data at $0.0015/unlock per bible § 4.2.6). Even an audit-scale dry-run incurs operator-billable cost. Brief did not authorize discretionary cost-bearing operations.
2. Probes require Playwright/Playwright-stealth runtime + Imperva/CAPTCHA target setup beyond the SELECT-only / read-only audit scope.
3. Probe purpose is exploratory (assessing whether a production strategy is viable); a one-shot dry-run from S1 would not produce a disposition more confident than the existing PHASE_5_BACKLOG candidate dispositions (kill / paid-replacement / scheduled-manual per bible § 4.2.6 honest disposition).

**Disposition:** Bible § 4.2.6 disposition holds — exploratory; pending Phase 5 disposition decision. S1 surfaces no new evidence to refine the kill/promote/scheduled-manual choice.

**Per-source epistemic standing:** **low (by design)** — (a) N/A; (b) no log group; (c) not executed (cost + scope). Standing is consistent with the source's exploratory state and is not a signal-collection failure.

---

## 4. Cross-source observations

### 4.1 Shared infrastructure failure mode dominates

5 of 6 sources have at least one signal whose disposition is "blocked or compromised by `equine-ingestion` INACTIVE state":
- HRN entries: production write path INACTIVE.
- HRN results: production write path INACTIVE.
- HRN workouts: load-side INACTIVE; scrape-side runs (per S3 evidence) but cannot land in DB.
- Equibase chart parser: production invocation path INACTIVE.
- equibase_probe: not affected (no production runtime to break).
- NYRA workouts: load-side INACTIVE (the Lambda's S3-upload + load-invoke flow falls back gracefully — log message `Don't fail — data is in S3, can be re-loaded manually` at handler.py:346 — but DB rows are not written).

PHASE_5_BACKLOG.md Phase 5.3.20 already tracks the underlying cause. **Bridging implication for D2 and D3** (Bug #28 fix and backfill scope): a fix to Bug #28 in `hrn_scraper.py:802-804` does NOT by itself restore production writes — `equine-ingestion` re-activation is a prerequisite even after the parser fix lands. D2 should sequence: (1) parser fix in source; (2) Lambda re-activation (Phase 5.3.20); (3) backfill of the affected window (Phase 5.3.1 closure).

### 4.2 Schema-drift errors in the final-active window (NEW finding — § 6)

The 2026-05-02 → 2026-05-03 final-active window of `equine-ingestion` produced three error patterns that are NOT documented in the bible's failure-mode inventory:
- `UndefinedColumn: column "distance" does not exist`
- `AmbiguousColumn: column reference "race_id" is ambiguous`
- `UndefinedColumn: column e.scratched does not exist`

These are SQL-vs-schema mismatches in the deployed image's queries. They are distinct from Bug #28 (parser-side) and from Bug #7 (HRN-source-side). They represent migration drift between the in-image SQL and the live RDS schema. When `equine-ingestion` is re-activated, these errors will resurface unless the in-image SQL is reconciled with current schema. **This is a defect candidate (see § 6).**

### 4.3 Cron timing vs source-publish-time mismatch (NEW finding — § 6)

NYRA workout cron at 10:00 UTC fires before NYRA publishes the day's workouts (≈14:00-18:00 UTC). All 7 production cron runs in the trailing 7d window scraped zero workouts despite the source being healthy. Manual probe at 03:54 UTC for the previous-day date returned 192 workouts. Dispositional implication: shifting cron to ≈06:00 UTC (asking for D-1) would restore data capture. (NB: the same class of defect may apply to the HRN entries cron at 11:00 UTC — entries publish ≈14:00 UTC = 10:00 EDT; the ENABLED cron may be marginal even when Lambda is restored. Out-of-scope to confirm at S1; flagged for D5 / D2 followup.)

### 4.4 Auxiliary/undocumented producers

The HRN-style daily workout file at `s3://equine-raw-data/workout-loads/{date_str}_{HHMMSS}.json` (e.g., `20260508_070049.json`, 3,180 records, uploaded daily at ≈07:00 UTC = 03:00 EDT) is produced by an **unknown agent**. CloudTrail does not log S3 PutObject events by default; CloudTrail Management events around the upload time show `equine-ingestion` IAM role activity (KMS decrypt at 07:00:53 UTC) but the Lambda is INACTIVE — the role-session activity may indicate a non-Lambda principal using the role's session, OR an EventBridge-driven action that triggers env-var decryption pre-runtime-failure. No discoverable producer Lambda; no discoverable cron rule; no ECS service running; no EC2 instance with the role. **Producer identification is an open question (see § 7).**

---

## 5. Summary table

Legend: ✓ collected; △ partial / indirect; DEFER deferred per sequencing; N/A not applicable.

| Source                | Signal (a) DB    | Signal (b) Logs | Signal (c) Dry-run            | Standing |
|-----------------------|------------------|-----------------|-------------------------------|----------|
| HRN entries           | △ (date-level)   | ✓ (with new errors) | DEFER (Bug #28 sequencing)    | moderate-to-low |
| HRN results           | △ (count-level)  | △ (shared LG)    | DEFER (Bug #28 sequencing)    | low |
| HRN workouts          | △ (S3 proxy)     | △ (no LG)        | DEFER (Bug #28 sequencing)    | low |
| NYRA workouts         | △ (S3 proxy)     | ✓ (clean)        | ✓ (timing defect surfaced)    | high |
| Equibase chart parser | △ (count-level)  | △ (shared LG)    | ✓ (10/10 local parse)         | high (logic) / moderate (path) |
| equibase_probe        | N/A              | N/A              | N/A (cost + scope)            | low (by design) |

---

## 6. Phase A bridging notes

### 6.1 Findings relevant to D2 (Bug #28 fix)

- Sequencing: fix in `hrn_scraper.py:802-804` is necessary but not sufficient for production data flow. `equine-ingestion` re-activation (Phase 5.3.20) is a parallel dependency.
- Bug #28's secondary surface — DD pool extraction at `hrn_scraper.py:819-820` per bible § 8.W.2 — was inspected but not empirically tested at S1. S3 fix should address both surfaces.
- Local-import dry-run of `hrn_scraper.fetch_results()` against a current HRN page is a feasible validation step S3 could use post-fix; would let S3 confirm parser correctness independent of the INACTIVE-Lambda blocker.

### 6.2 Findings relevant to D3 (backfill scope)

- Bug #28 column-shift NULL window per bible § 4.2.2: 2026-04-30 → 2026-05-02. **Empirical NULL distribution unverified at S1** due to § 1.2 blocker — this is the largest open verification S3 should run as soon as `equine-ingestion` raw_query is restored.
- Bug #28 does NOT affect the 2026-04-29 day (last clean per bible) or any earlier date.
- Fire-and-fail window (post-2026-05-02): no rows written at all → not a backfill target for parser-fix purposes (no corrupted rows to overwrite); rather, a re-scrape target for missed-data-recovery purposes.
- Chart parser PDF freshness: no fresh PDFs since 2026-04-29 → backfill scope for chart parser enrichment is at most the 2026-04-30 → 2026-04-30 window plus pre-existing PDF inventory not yet processed.
- NYRA workout backfill candidate window: 2026-05-02 → 2026-05-08 (7 days × ~200 workouts/day = ~1,400 workouts missed). Recovery is straightforward — invoke NYRA Lambda with `{"date":"2026-05-XX","trigger_load":true}` for each day, AFTER `equine-ingestion` `load_workouts_from_s3` is restored.

### 6.3 Findings relevant to D5 (PHASE_5_BACKLOG closures)

- Existing entries that intersect this audit:
  - **Phase 5.3.1** (Bug #28 column shift) — DO NOT CLOSE; close after S3/S7 + backfill verification.
  - **Phase 5.3.17** (3 INACTIVE Lambdas with deleted ECR images) — DO NOT CLOSE; entry correctly captures all 3 (`equine-ingestion`, `equine-results`, `equine-feature-engineering`).
  - **Phase 5.3.18** (2 Secrets Manager entries with zero consumers) — relevant to equibase_probe disposition; bridge to D5.
  - **Phase 5.3.20** (equine-ingestion broken container) — DO NOT CLOSE; entry remains the canonical fix anchor.

### 6.4 New defects surfaced (candidates for new PHASE_5_BACKLOG entries)

**Candidate 5.3.N+1 — NYRA Workout Cron Capture-Time Defect (NEW, severity HIGH).**
EventBridge rule `equine-nyra-workouts-daily` fires at 10:00 UTC asking for today's date in UTC. NYRA publishes that day's workouts during ≈14:00-18:00 UTC. Net result: 7/7 production cron runs in the trailing 7d window scraped zero workouts. Empirical evidence: log lines `NYRA: scraped zero workouts across all tracks; skipping S3 upload + load` for 2026-05-02 through 2026-05-08; manual probe at 03:54 UTC for D-1 returns full data. Disposition: shift cron to ≈06:00 UTC (asking for D-1) OR change handler default-date logic to `(date.today() - timedelta(days=1))`. Severity HIGH because the NYRA workouts source has been silently producing zero rows for at least 7 consecutive days while looking healthy in CloudWatch (no errors logged); the in-bible "Currently functional / no failure mode" disposition at § 4.1.4 + § 4.2.4 is empirically incorrect.

**Candidate 5.3.N+2 — Schema Drift in `equine-ingestion` Image SQL (NEW, severity MEDIUM).**
The 2026-05-02 → 2026-05-03 final-active window logged `UndefinedColumn: column "distance" does not exist`, `AmbiguousColumn: column reference "race_id" is ambiguous`, and `UndefinedColumn: column e.scratched does not exist`. These are NOT bug #7, NOT bug #28; they are SQL-vs-live-schema mismatches in the deployed image. Disposition: when Phase 5.3.20 re-activates the Lambda, these errors will resurface unless the in-image SQL is updated against current `database_schema_bible.md` schema. Severity MEDIUM because the issue is bounded (specific named column references) and a coordinated re-deploy can fix all three together; downgrade to LOW if discovered to be cosmetic / non-blocking on actual data flow.

**Candidate 5.3.N+3 — Undocumented HRN Workout Producer (NEW, severity MEDIUM).**
A daily process uploads non-NYRA workout data to `s3://equine-raw-data/workout-loads/{date_str}_{HHMMSS}.json` at ≈07:00 UTC, producing files of substantive size (≈900KB / 3,180 workout records on 2026-05-08). The producer is not a discoverable Lambda, ECS task, EventBridge rule, or EC2 instance. Disposition: identify the producer (probable candidates: Tony's local cron; a forgotten ECS service; a CodeBuild job). Either document it in bible § 4.2.3 and add an EventBridge surface, OR — if it's a deprecated path — kill it. Severity MEDIUM because the data IS being captured (S3 proxy is healthy) but the load-to-DB half is broken (per § 4.1) and the producer's invisibility makes maintenance/debugging fragile. NB: this finding is consistent with bible § 4.2.3's "asserted-not-empirical" disposition and operationalizes it.

**Candidate 5.3.N+4 — HRN Entries Cron Capture-Time Risk (NEW, severity LOW pending confirmation).**
By analogy to the NYRA timing defect: `equine-ingestion-daily` fires at 11:00 UTC asking for today's race-card entries. HRN typically publishes entries in advance (often 24-48h prior), so this cron may NOT have the same defect. However, S1 did not empirically confirm. Recommendation: when Phase 5.3.20 restores the Lambda, log the first cron run's per-track find counts to verify that the 11:00 UTC capture window catches all expected entries. Severity LOW pending the confirmation step.

### 6.5 Findings relevant to other deliverables

- **For D4 (whatever it is — not specified in brief):** Cross-source observation § 4.1 establishes the dominant single-failure-domain (INACTIVE Lambda); any system-restoration plan should sequence Lambda re-activation as a top-priority precondition.

---

## 7. Open questions for Tony / blocking issues

### 7.1 The brief's documented DB-access pattern is non-functional

The brief instructs:
> Production DB: SELECT-only via the `equine-ingestion` Lambda `raw_query` action.

`equine-ingestion` is INACTIVE per Phase 5.3.20. **No DB-direct verification of `results` column-level Bug #28 evidence is possible without restoration.** S1 worked around this for trace-level signals (using public API, S3 listings, log scans) but the Bug #28 NULL-distribution check on `results.win_payout` etc. is genuinely unverified at S1 lock time. Two options:

(a) **Tony grants S1 (or S2) a fallback DB access path** (e.g., authorize `aws rds-data execute-statement` directly with cluster ARN and secret ARN; or stand up a temporary read-only Lambda). Allows column-level Bug #28 verification before S2 audit.
(b) **Accept the deferral.** S2 audits this snapshot's column-level claims as DEFERRED, ratifies anyway, and Bug #28 NULL-distribution verification waits for Phase 5.3.20 closure.

Recommend (b) for cycle velocity unless (a) is operationally cheap.

### 7.2 The undocumented HRN workouts producer (§ 4.4 / § 6.4 candidate 5.3.N+3)

S1 could not identify the producer. Tony likely knows. Identifying it is a 1-question answer for Tony but is a multi-hour rabbit-hole for a CC. **Recommend Tony briefly clarify** what process uploads `s3://equine-raw-data/workout-loads/{date_str}_{HHMMSS}.json` daily before S2 dispatch; the answer affects the severity of candidate 5.3.N+3 and may simplify the bridging notes.

### 7.3 NYRA cron timing defect (§ 6.4 candidate 5.3.N+1)

This finding contradicts the bible's § 4.1.4 / § 4.2.4 "currently functional" disposition. S2 should re-validate independently. If confirmed, the bible's per-source disposition will need a patch on next bible-revision pass.

### 7.4 S3 side-effect during NYRA dry-run

§ 3.4 signal (c) wrote 2 small JSON files to `s3://equine-raw-data/workout-loads/` (Probes 2 and 3). The brief did not authorize S3 writes; only DB writes were forbidden. S1 disclosed transparently. **If Tony judges this out-of-bounds**, S2 should review whether the side-effect invalidates D1; otherwise, the files are valid workout data and may be picked up by a future load-batch (after Lambda re-activation) without harm.

---

**End of Source Status Audit — 2026-05-08.**
