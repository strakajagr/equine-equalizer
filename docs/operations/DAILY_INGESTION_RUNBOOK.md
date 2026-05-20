# Daily Ingestion Runbook

**Authored**: 2026-05-12 (Phase A D5 dispatch)
**Source substrate**: `docs/operations/PHASE_A_HANDOFF_2026-05-12.md` (handoff)
**Scope**: Operational sources, alarm response procedures, manual recovery tools, known operational expectations

This runbook is the operator reference for the daily equine ingestion + inference pipeline. Every fact traces to a handoff section citation, prior dispatch citation, or file:line substrate citation.

---

## Section 1 — Operational Sources

Five operational sources feed the daily pipeline per handoff § 1.1. Each block below documents producer / schedule / tables / DLQ / alarms / healthy + degraded signals.

### Source 1 — HRN entries

- **Producer**: `equine-ingestion` Lambda (default action) (handoff § 1.1)
- **Schedule (UTC)**: `cron(0 11 * * ? *)` = 11:00 (handoff § 1.1)
- **Tables written**: entries, races, horses, trainers, jockeys, tracks, past_performances (handoff § 1.1)
- **DLQ status**: ✅ — OnFailure → `arn:aws:sqs:us-east-1:584812014683:equine-async-failure-dlq`, retry=2, age=3600 (handoff § 1.2)
- **Alarms covering this source** (handoff § 1.3 mapping):
  - `equine-entries-qualifying-tracks-missing` (composite output watcher)
  - `equine-ingestion-daily-cron-absence` (cron rule absence)
  - `equine-ingestion-errors` (Lambda-level)
  - `equine-ingestion-throttles` (Lambda-level)
  - `equine-ingestion-invocations-absence` (Lambda-level)
  - `equine-async-dlq-messages-present` (shared DLQ depth)
- **Healthy signal**: Lambda invocation log records successful run at scheduled time; entries + races rows present for current date covering 11 qualifying tracks (per `QUALIFYING_TRACKS` constant); `equine-entries-qualifying-tracks-missing` alarm in OK state.
- **Degraded signal + first response**: `equine-entries-qualifying-tracks-missing` alarm fires OR `equine-ingestion-errors` fires OR DLQ message arrives. First response: inspect CloudWatch Logs for `/aws/lambda/equine-ingestion` for the invocation window; if Lambda failed completely, check DLQ depth (`equine-async-dlq-messages-present`); for partial-track gap, run `backfill_d2.py` (Section 3) for affected date range.

### Source 2 — HRN results

- **Producer**: `equine-ingestion` Lambda (action=fetch_results) (handoff § 1.1)
- **Schedule (UTC)**: `cron(30 1 * * ? *)` = 01:30 (handoff § 1.1)
- **Tables written**: results (handoff § 1.1)
- **DLQ status**: ✅ (inherited from Lambda) (handoff § 1.1)
- **Architecture clarification** (handoff § 1.1 substrate correction): HRN-results-scraping is `equine-ingestion` Lambda's `fetch_results` action invoked via EventBridge rule `equine-fetch-results-nightly`. This is **NOT** the `equine-results` matcher Lambda (Appendix B per handoff § 1.4 — separate reconciliation Lambda updating `wr_predictions.actual_finish` against arriving results; NOT data ingestion).
- **Alarms covering this source** (handoff § 1.3 mapping):
  - `equine-fetch-results-nightly-cron-absence` (cron rule absence)
  - `equine-results-rows-written-today` (output watcher)
  - `equine-ingestion-errors` (Lambda-level, shared with Source 1)
  - `equine-ingestion-throttles` (Lambda-level, shared with Source 1)
  - `equine-ingestion-invocations-absence` (Lambda-level, shared with Source 1)
  - `equine-async-dlq-messages-present` (shared DLQ depth)
- **Healthy signal**: `equine-ingestion` invocation at 01:30 UTC succeeds with `action=fetch_results`; results rows written for prior race day(s); `equine-results-rows-written-today` alarm in OK state.
- **Degraded signal + first response**: `equine-results-rows-written-today` fires (no results written) OR `equine-fetch-results-nightly-cron-absence` fires (cron rule missing/disabled). First response: inspect CloudWatch Logs for `/aws/lambda/equine-ingestion` filtered to the 01:30 UTC window; verify EventBridge rule `equine-fetch-results-nightly` is ENABLED with Input payload specifying `action=fetch_results`; for confirmed gap, run `backfill_d3.py` (Section 3) for affected date range.

### Source 3 — NYRA workouts

- **Producer**: `equine-nyra-workouts` Lambda (handoff § 1.1)
- **Schedule (UTC)**: `cron(0 16 * * ? *)` = 16:00 (handoff § 1.1)
- **Tables written**: workouts (via S3 → load_workouts_from_s3) (handoff § 1.1)
- **DLQ status**: ✅ (A.5-ext) — OnFailure → `arn:aws:sqs:us-east-1:584812014683:equine-async-failure-dlq`, retry=2, age=3600 (handoff §§ 1.1, 1.2)
- **Alarms covering this source** (handoff § 1.3 mapping):
  - `equine-nyra-workouts-errors`
  - `equine-nyra-workouts-throttles`
  - `equine-nyra-workouts-invocations-absence`
  - `equine-nyra-workouts-daily-cron-absence`
  - `equine-workouts-objects-written-today` (shared with Source 4; S3-object-presence)
  - `equine-async-dlq-messages-present` (shared DLQ depth)
- **Healthy signal**: Lambda invocation at 16:00 UTC writes S3 object at `s3://equine-raw-data/workout-loads/{YYYYMMDD}_nyra_{YYYYMMDD_HHMMSS}.json` (handoff § 2.6); `equine-workouts-objects-written-today` alarm in OK state; subsequent `equine-ingestion` `load_workouts_from_s3` invocation persists rows into `workouts` table for SAR / BEL / AQU coverage.
- **Degraded signal + first response**: `equine-nyra-workouts-errors` fires OR `equine-nyra-workouts-invocations-absence` fires OR `equine-nyra-workouts-daily-cron-absence` fires OR DLQ message arrives. First response: inspect CloudWatch Logs `/aws/lambda/equine-nyra-workouts`; verify EventBridge rule for the daily cron is ENABLED; check DLQ depth; for confirmed gap, run `manual_nyra_workouts.py` (Section 3) for affected date range and tracks.

### Source 4 — Equibase workouts

- **Producer**: `/home/strakajagr/equibase_scraper/run_daily_refresh.sh` (local cron) (handoff § 1.1)
- **Schedule (UTC)**: `0 3 * * *` (03:00 EDT = 07:00 UTC) (handoff § 1.1)
- **Tables written**: workouts (via S3 → load_workouts_from_s3) (handoff § 1.1)
- **DLQ status**: N/A (out-of-band) (handoff § 1.1)
- **Architectural note** (handoff § 2.6): Sibling repo on Tony's local machine at `/home/strakajagr/equibase_scraper/`; not in `/home/strakajagr/projects/`. S3 path: `s3://equine-raw-data/workout-loads/{YYYYMMDD}_{HHMMSS}.json` (no `_nyra_` infix). Coverage: 8+ tracks per per-horse iteration (CD/GP/KEE/MTH/SA/OP plus NYRA-overlap SAR/BEL/AQU).
- **Alarms covering this source** (handoff § 1.3 mapping):
  - `equine-workouts-objects-written-today` (shared with Source 3; S3-object-presence)
- **Healthy signal**: S3 object written at expected path daily; `equine-workouts-objects-written-today` alarm in OK state; downstream `equine-ingestion` `load_workouts_from_s3` action persists rows into `workouts` table.
- **Degraded signal + first response**: `equine-workouts-objects-written-today` fires AND no NYRA-infix object present for the day (rule out Source 3 first; the alarm is shared). First response: SSH to Tony's local machine; inspect `/home/strakajagr/equibase_scraper/logs/cron.log` for the 03:00 EDT cron line; check exit codes and `new_pdfs` / workout count signals; for confirmed Source 4 gap with intact infrastructure, re-run `run_daily_refresh.sh` manually for affected date.

### Source 5 — Equibase charts

- **Producer**: `/home/strakajagr/equibase_scraper/download_charts.py` (handoff § 1.1)
- **Schedule (UTC)**: Same cron entry as Source 4 (handoff § 1.1)
- **Tables written**: None directly. PDF charts to `s3://equine-raw-data/charts/` (handoff § 1.1)
- **DLQ status**: N/A (out-of-band; FAILING DAILY exit=1) (handoff § 1.1)
- **Operational expectation** (handoff § 5.1): `download_charts.py` failing daily with exit=1, `new_pdfs=0` across 3 captured days (May 9/10/11). SNS_TOPIC_ARN set in cron env (`arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts`); SNS alerts may be firing daily until Tony disposition lands per handoff § 5.1.
- **Alarms covering this source** (handoff § 1.3 mapping): None CloudWatch-side (out-of-band; SNS-mediated only).
- **Healthy signal**: Not currently in healthy state per handoff § 5.1. Healthy state would be `new_pdfs > 0` and exit=0 in `/home/strakajagr/equibase_scraper/logs/cron.log`.
- **Degraded signal + first response**: Current daily state is degraded per handoff § 5.1. Non-blocking for Source 4 workouts step. No first-response action prescribed at runbook scope — disposition pending Tony decision per handoff § 5.1.

---

## Section 2 — Alarm Response Procedures

Twenty-nine alarms inventoried per handoff § 1.3 in verbatim ordering. Each block: Alarm / Maps to / What fired / What to check / What to do / When to escalate. Composite alarms + DLQ depth alarm + orphan-watching alarms have additional special-handling subsections after the per-alarm enumeration.

### 2.1 — Per-Alarm Blocks (Verbatim Ordering)

---

**Alarm 1: `equine-async-dlq-messages-present`**
- **Maps to**: DLQ (covers Sources 1+2, Appendix B matcher, 3 inference Lambdas, NYRA workouts) (handoff § 1.3)
- **What fired**: DLQ depth metric crossed threshold > 0 (handoff § 1.2 records baseline OK state with StateReason `0.0 was not greater than threshold (0.0)`).
- **What to check**: DLQ depth + per-message attribution:
  ```
  aws sqs get-queue-attributes \
      --queue-url https://sqs.us-east-1.amazonaws.com/584812014683/equine-async-failure-dlq \
      --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible
  ```
- **What to do**: Inspect message(s) non-consuming per § 2.3 DLQ depth alarm special-handling subsection below; apply replay-vs-drop decision tree per the 6 covered Lambdas.
- **When to escalate**: If DLQ depth re-grows after replay/drop OR if message attribution surfaces a Lambda not in the 6-covered list (handoff § 1.2).

---

**Alarm 2: `equine-entries-qualifying-tracks-missing`**
- **Maps to**: Source 1 (composite output watcher) (handoff § 1.3)
- **What fired**: Composite output watcher detected qualifying-tracks shortfall for current date. See § 2.2 composite alarms subsection for math substrate (handoff § 1.3 marks as composite; specific math expression not in handoff substrate).
- **What to check**: Inspect entries + races rows for current date filtered to `QUALIFYING_TRACKS` (per handoff § 2.4); CloudWatch Logs for `/aws/lambda/equine-ingestion` at the 11:00 UTC invocation window.
- **What to do**: Identify missing track(s); run `backfill_d2.py` (Section 3) for current date.
- **When to escalate**: If `backfill_d2.py` dry-run produces no rows for the gap OR if scraper returns zero entries for the missing track on retry.

---

**Alarm 3: `equine-feature-engineering-errors`**
- **Maps to**: Appendix A2 (ORPHAN) (handoff § 1.3, § 1.4)
- **What fired**: Lambda Errors metric breach on `equine-feature-engineering`. Note: this Lambda is an ORPHAN — zero EventBridge rules target it (handoff § 1.4). Firing here = anomaly per § 2.4 orphan-watching subsection below.
- **What to check**: CloudWatch Logs `/aws/lambda/equine-feature-engineering`; identify invocation source (should be none per orphan status).
- **What to do**: Substrate-trace anomalous invocation. No recovery tool applies — Lambda has no operational role per handoff § 1.4.
- **When to escalate**: Immediately if alarm fires — orphan-watching alarms are known-quiet baseline per handoff § 1.4.

---

**Alarm 4: `equine-feature-engineering-throttles`**
- **Maps to**: Appendix A2 (ORPHAN) (handoff § 1.3, § 1.4)
- **What fired**: Lambda Throttles metric breach on `equine-feature-engineering` ORPHAN Lambda.
- **What to check**: CloudWatch Logs + concurrency settings; identify invocation source (should be none).
- **What to do**: Substrate-trace anomalous invocation; orphan-watching anomaly per § 2.4.
- **When to escalate**: Immediately — orphan-watching alarm.

---

**Alarm 5: `equine-fetch-results-nightly-cron-absence`**
- **Maps to**: Source 2 (cron rule absence) (handoff § 1.3)
- **What fired**: EventBridge rule absence/disablement detected for the `equine-fetch-results-nightly` rule.
- **What to check**:
  ```
  aws events describe-rule --name equine-fetch-results-nightly --region us-east-1
  ```
- **What to do**: If rule is DISABLED or missing, re-enable; verify Input payload specifies `action=fetch_results` (per handoff § 1.1 producer description).
- **When to escalate**: If rule appears intact but alarm persists — possible alarm misconfiguration (halt-and-surface to Tony).

---

**Alarm 6: `equine-inference-errors`**
- **Maps to**: Appendix A1 (DISABLED rule; orphan-watching) (handoff § 1.3, § 1.4)
- **What fired**: Lambda Errors metric breach on `equine-inference` (legacy, deprecated per handoff § 1.4; EventBridge rule `equine-inference-daily` DISABLED).
- **What to check**: CloudWatch Logs `/aws/lambda/equine-inference`; identify invocation source (rule disabled).
- **What to do**: Substrate-trace anomalous invocation; orphan-watching anomaly.
- **When to escalate**: Immediately — orphan-watching alarm.

---

**Alarm 7: `equine-inference-throttles`**
- **Maps to**: Appendix A1 (DISABLED rule; orphan-watching) (handoff § 1.3, § 1.4)
- **What fired**: Lambda Throttles metric breach on legacy `equine-inference` Lambda.
- **What to check**: CloudWatch Logs + concurrency; identify invocation source.
- **What to do**: Substrate-trace; orphan-watching anomaly.
- **When to escalate**: Immediately — orphan-watching alarm.

---

**Alarm 8: `equine-ingestion-daily-cron-absence`**
- **Maps to**: Source 1 (cron rule absence) (handoff § 1.3)
- **What fired**: EventBridge rule absence/disablement detected for the Source 1 daily cron rule (`cron(0 11 * * ? *)` per handoff § 1.1).
- **What to check**:
  ```
  aws events list-rules --region us-east-1 --query 'Rules[?contains(Name, `ingestion`)]'
  ```
- **What to do**: If rule is DISABLED or missing, re-enable.
- **When to escalate**: If rule appears intact but alarm persists.

---

**Alarm 9: `equine-ingestion-errors`**
- **Maps to**: Sources 1+2 (Lambda-level) (handoff § 1.3)
- **What fired**: Lambda Errors metric breach on `equine-ingestion`. Covers both Source 1 (11:00 UTC entries) and Source 2 (01:30 UTC results) invocations.
- **What to check**: CloudWatch Logs `/aws/lambda/equine-ingestion` — filter by invocation window (11:00 UTC = Source 1; 01:30 UTC = Source 2) to identify which source class is affected.
- **What to do**: If Source 1 invocation failed, run `backfill_d2.py` (Section 3) for current date; if Source 2 invocation failed, run `backfill_d3.py` (Section 3) for current results date.
- **When to escalate**: If recovery action fails twice in same day OR if alarm re-fires after recovery tool execution.

---

**Alarm 10: `equine-ingestion-throttles`**
- **Maps to**: Sources 1+2 (Lambda-level) (handoff § 1.3)
- **What fired**: Lambda Throttles metric breach on `equine-ingestion`.
- **What to check**: CloudWatch concurrency metrics for `equine-ingestion`; account-level Lambda concurrency limits.
- **What to do**: If throttle was transient (single invocation), no action needed; if persistent, raise reserved concurrency or investigate concurrent invocation source.
- **When to escalate**: If throttles persist across multiple consecutive invocations.

---

**Alarm 11: `equine-ingestion-invocations-absence`**
- **Maps to**: Sources 1+2 (Lambda-level) (handoff § 1.3)
- **What fired**: Lambda Invocations metric absent over expected window (Source 1 at 11:00 UTC and/or Source 2 at 01:30 UTC).
- **What to check**: Last invocation timestamp via `aws lambda get-function --function-name equine-ingestion`; EventBridge rule state for both rules; CloudWatch Logs for the expected window.
- **What to do**: If both crons present and rule state ENABLED but no invocation, manually invoke via `aws lambda invoke` with appropriate action payload; investigate scheduler outage.
- **When to escalate**: If manual invocation also produces no log output OR if both Source 1 + Source 2 cron rules are intact but invocations consistently absent.

---

**Alarm 12: `equine-ls-inference-errors`**
- **Maps to**: Phase B LS inference (handoff § 1.3)
- **What fired**: Lambda Errors metric breach on `equine-ls-inference`.
- **What to check**: CloudWatch Logs `/aws/lambda/equine-ls-inference`; LS reads from `wr_predictions` per handoff § 2.11, so verify `wr_predictions` rows exist for target date as upstream precondition.
- **What to do**: If WR upstream succeeded (rows present) but LS failed, inspect specific error in logs; if WR upstream failed (no rows), recovery sequence is WR first then LS — run `rerun_inference.py --lambdas wr,ls` (Section 3) for affected date.
- **When to escalate**: If LS errors persist after WR upstream is confirmed healthy.

---

**Alarm 13: `equine-ls-inference-throttles`**
- **Maps to**: Phase B LS inference (handoff § 1.3)
- **What fired**: Lambda Throttles metric breach on `equine-ls-inference`.
- **What to check**: CloudWatch concurrency metrics; reserved concurrency setting.
- **What to do**: Same as `equine-ingestion-throttles` (Alarm 10).
- **When to escalate**: If throttles persist across multiple consecutive invocations.

---

**Alarm 14: `equine-ls-predictions-deficit`**
- **Maps to**: Phase B LS inference (A.5 deliverable; composite math alarm) (handoff § 1.3)
- **What fired**: Math expression `IF(m1 > 0, m1 - m2, 0) > 0` per handoff § 2.10 where m1 = `EquineExpectedLSPredictionsToday`, m2 = `EquineActualLSPredictionsToday`. Threshold > 0. TreatMissingData=breaching.
- **What to check**: Per handoff § 2.10, alarm catches cascading failure including LS clean-exit-empty (when WR/PL upstream produces 0). Inspect `wr_predictions` (LS upstream per handoff § 2.11) + `ls_predictions` row counts for target date; CloudWatch Logs `/aws/lambda/equine-ls-inference`.
- **What to do**: If `wr_predictions` empty/short, recover WR first; then run `rerun_inference.py --lambdas wr,ls` (Section 3) for affected date.
- **When to escalate**: If alarm re-fires after `rerun_inference.py --execute` completes successfully.

---

**Alarm 15: `equine-nyra-workouts-errors`**
- **Maps to**: Source 3 (handoff § 1.3)
- **What fired**: Lambda Errors metric breach on `equine-nyra-workouts`.
- **What to check**: CloudWatch Logs `/aws/lambda/equine-nyra-workouts` at 16:00 UTC invocation window.
- **What to do**: If Lambda failed completely, run `manual_nyra_workouts.py` (Section 3) for affected date(s) and tracks; check DLQ depth (`equine-async-dlq-messages-present`) for retry-exhausted invocations.
- **When to escalate**: If `manual_nyra_workouts.py --execute` also fails OR if NYRA scraper surfaces upstream defect (per A.6.a/A.6.b pattern referenced in handoff § 1.5).

---

**Alarm 16: `equine-nyra-workouts-throttles`**
- **Maps to**: Source 3 (handoff § 1.3)
- **What fired**: Lambda Throttles metric breach on `equine-nyra-workouts`.
- **What to check**: CloudWatch concurrency metrics.
- **What to do**: Same as Alarm 10.
- **When to escalate**: If throttles persist across multiple consecutive invocations.

---

**Alarm 17: `equine-nyra-workouts-invocations-absence`**
- **Maps to**: Source 3 (handoff § 1.3)
- **What fired**: Lambda Invocations metric absent over expected 16:00 UTC window.
- **What to check**: Last invocation timestamp; EventBridge rule state for the daily cron.
- **What to do**: If cron rule intact but invocations absent, manually invoke; if cron rule disabled/missing, re-enable.
- **When to escalate**: If manual invocation produces no log output.

---

**Alarm 18: `equine-nyra-workouts-daily-cron-absence`**
- **Maps to**: Source 3 (handoff § 1.3)
- **What fired**: EventBridge rule absence/disablement detected for the Source 3 daily cron rule.
- **What to check**:
  ```
  aws events list-rules --region us-east-1 --query 'Rules[?contains(Name, `nyra`)]'
  ```
- **What to do**: If rule DISABLED or missing, re-enable.
- **When to escalate**: If rule appears intact but alarm persists.

---

**Alarm 19: `equine-pl-inference-errors`**
- **Maps to**: Phase B PL inference (handoff § 1.3)
- **What fired**: Lambda Errors metric breach on `equine-pl-inference`.
- **What to check**: CloudWatch Logs `/aws/lambda/equine-pl-inference`.
- **What to do**: Run `rerun_inference.py --lambdas pl` (Section 3) for affected date.
- **When to escalate**: If PL errors persist after rerun.

---

**Alarm 20: `equine-pl-inference-throttles`**
- **Maps to**: Phase B PL inference (handoff § 1.3)
- **What fired**: Lambda Throttles metric breach on `equine-pl-inference`.
- **What to check**: CloudWatch concurrency metrics.
- **What to do**: Same as Alarm 10.
- **When to escalate**: If throttles persist.

---

**Alarm 21: `equine-pl-predictions-deficit`**
- **Maps to**: Phase B PL inference (A.5 deliverable) (handoff § 1.3)
- **What fired**: Math expression `IF(m1 > 0, m1 - m2, 0) > 0` per handoff § 2.10 where m1 = `EquineExpectedPLPredictionsToday`, m2 = `EquineActualPLPredictionsToday`. Threshold > 0. TreatMissingData=breaching.
- **What to check**: Inspect `pl_predictions` row count for target date; CloudWatch Logs `/aws/lambda/equine-pl-inference`.
- **What to do**: Run `rerun_inference.py --lambdas pl` (Section 3) for affected date.
- **When to escalate**: If alarm re-fires after `rerun_inference.py --execute` completes successfully.

---

**Alarm 22: `equine-results-errors`**
- **Maps to**: Appendix B matcher (handoff § 1.3, § 1.4)
- **What fired**: Lambda Errors metric breach on `equine-results` matcher Lambda (NOT data ingestion — reconciliation per handoff § 1.4).
- **What to check**: CloudWatch Logs `/aws/lambda/equine-results` at 04:00 UTC invocation window.
- **What to do**: Inspect failure detail; matcher Lambda updates `wr_predictions.actual_finish` against arriving results. No recovery tool prescribed at runbook scope (matcher logic re-runs on next invocation).
- **When to escalate**: If matcher errors persist across multiple days.

---

**Alarm 23: `equine-results-invocations-absence`**
- **Maps to**: Appendix B matcher (handoff § 1.3, § 1.4)
- **What fired**: Lambda Invocations metric absent over expected window.
- **What to check**: EventBridge rule `equine-results-daily cron(0 4 * * ? *)` state.
- **What to do**: Per handoff § 1.4 + § 1.6, this Lambda fired 2 of 7 days observed in last week. Open Thread 2 classifies as sparse-by-design vs silently-broken pending Phase B substrate review. Inspect last invocation timestamp + cron rule state before action; if cron disabled, re-enable.
- **When to escalate**: Defer to Phase B sparse-invocation classification per handoff § 5.2; do NOT issue disposition at runbook scope.

---

**Alarm 24: `equine-results-rows-written-today`**
- **Maps to**: Source 2 (output watcher) (handoff § 1.3)
- **What fired**: Composite output watcher detected `results` table empty/short for current date. See § 2.2 composite alarms subsection below.
- **What to check**: `results` row count for current date; CloudWatch Logs for `equine-ingestion` at 01:30 UTC invocation window.
- **What to do**: Run `backfill_d3.py` (Section 3) for current date.
- **When to escalate**: If `backfill_d3.py --execute` produces zero new rows.

---

**Alarm 25: `equine-results-throttles`**
- **Maps to**: Appendix B matcher (handoff § 1.3)
- **What fired**: Lambda Throttles metric breach on `equine-results` matcher Lambda.
- **What to check**: CloudWatch concurrency metrics.
- **What to do**: Same as Alarm 10.
- **When to escalate**: If throttles persist.

---

**Alarm 26: `equine-workouts-objects-written-today`**
- **Maps to**: Shared: Source 3 + Source 4 (S3-object-presence) (handoff § 1.3)
- **What fired**: S3-object-presence watcher detected no workout-load object written to `s3://equine-raw-data/workout-loads/` for current date. See § 2.2 composite alarms subsection below.
- **What to check**: List S3 prefix for current date:
  ```
  aws s3 ls s3://equine-raw-data/workout-loads/ | grep "$(date -u +%Y%m%d)"
  ```
  Distinguish NYRA-infix objects (`*_nyra_*.json`, Source 3 per handoff § 2.6) vs non-infix (Source 4 Equibase).
- **What to do**: If only Source 4 missing, follow Source 4 degraded-signal first response (Section 1); if only Source 3 missing, follow Source 3; if both, prioritize Source 3 recovery via `manual_nyra_workouts.py` (Section 3) then escalate Source 4 separately.
- **When to escalate**: If both producers consistently absent across multiple days OR if Source 4 SSH/local-cron-log inspection surfaces infrastructure failure.

---

**Alarm 27: `equine-wr-inference-errors`**
- **Maps to**: Phase B WR inference (handoff § 1.3)
- **What fired**: Lambda Errors metric breach on `equine-wr-inference`.
- **What to check**: CloudWatch Logs `/aws/lambda/equine-wr-inference`.
- **What to do**: Run `rerun_inference.py --lambdas wr` (Section 3) for affected date.
- **When to escalate**: If WR errors persist after rerun.

---

**Alarm 28: `equine-wr-inference-throttles`**
- **Maps to**: Phase B WR inference (handoff § 1.3)
- **What fired**: Lambda Throttles metric breach on `equine-wr-inference`.
- **What to check**: CloudWatch concurrency metrics.
- **What to do**: Same as Alarm 10.
- **When to escalate**: If throttles persist.

---

**Alarm 29: `equine-wr-predictions-deficit`**
- **Maps to**: Phase B WR inference (A.5 deliverable) (handoff § 1.3)
- **What fired**: Math expression `IF(m1 > 0, m1 - m2, 0) > 0` per handoff § 2.10 where m1 = `EquineExpectedWRPredictionsToday`, m2 = `EquineActualWRPredictionsToday`. Threshold > 0. TreatMissingData=breaching.
- **What to check**: Inspect `wr_predictions` row count for target date; CloudWatch Logs `/aws/lambda/equine-wr-inference`. Note: WR upstream affects LS per handoff § 2.11.
- **What to do**: Run `rerun_inference.py --lambdas wr,ls` (Section 3) for affected date (LS depends on WR per handoff § 2.11).
- **When to escalate**: If alarm re-fires after `rerun_inference.py --execute` completes successfully.

---

### 2.2 — Composite Alarms (Special Handling)

**`equine-entries-qualifying-tracks-missing`** (Alarm 2): Composite output watcher per handoff § 1.3. Detects when Source 1's daily output is missing entries for one or more of the 11 qualifying tracks (per `QUALIFYING_TRACKS = ['CD', 'SAR', 'KEE', 'BEL', 'SA', 'GP', 'DMR', 'OP', 'MTH', 'AQU', 'PIM']` per handoff § 2.4 / `backend/shared/constants.py`). Specific math expression substrate not present in handoff — inspect alarm config in CloudWatch console for detail.

**`equine-wr-predictions-deficit` / `equine-pl-predictions-deficit` / `equine-ls-predictions-deficit`** (Alarms 29, 21, 14): All three use math expression `IF(m1 > 0, m1 - m2, 0)` with threshold > 0 per handoff § 2.10. TreatMissingData=breaching. Metrics:
- m1 = Expected metric (`EquineExpectedWRPredictionsToday` / `EquineExpectedPLPredictionsToday` / `EquineExpectedLSPredictionsToday`)
- m2 = Actual metric (`EquineActualWRPredictionsToday` / `EquineActualPLPredictionsToday` / `EquineActualLSPredictionsToday`)

The 6 metrics are added to existing `equine-entries-tracks-publisher` Lambda per handoff § 2.10 (A.5-α extension). Expected calculation: SQL mirrors A.6.c race-eligibility filter (handoff § 2.4) + applies PREDICT_RACE_TOLERANCE=5 post-fetch (handoff § 2.5). Per-Lambda non-conflation is deliberate per handoff § 2.10 — cascading-failure detection: alarm fires even when Lambda itself succeeds with empty output (LS clean-exit-empty when WR/PL upstream produces 0 — alarm catches via Expected > 0, Actual = 0).

**`equine-results-rows-written-today`** (Alarm 24): Output watcher per handoff § 1.3. Produced by post-Source-2 row-count check on `results` table for current date. Specific threshold detail not in handoff — inspect alarm config in CloudWatch console for detail.

**`equine-workouts-objects-written-today`** (Alarm 26): S3-object-presence watcher per handoff § 1.3. Shared by Source 3 (NYRA, `*_nyra_*.json`) and Source 4 (Equibase, non-infix) per handoff § 2.6. Specific threshold detail not in handoff — inspect alarm config in CloudWatch console for detail.

### 2.3 — DLQ Depth Alarm Special Handling

**Alarm**: `equine-async-dlq-messages-present` (Alarm 1)
**DLQ ARN**: `arn:aws:sqs:us-east-1:584812014683:equine-async-failure-dlq` (handoff § 1.2)

**Inspection procedure (non-consuming)**:
```
aws sqs receive-message \
    --queue-url https://sqs.us-east-1.amazonaws.com/584812014683/equine-async-failure-dlq \
    --max-number-of-messages 10 \
    --visibility-timeout 0 \
    --attribute-names All \
    --message-attribute-names All
```

`--visibility-timeout 0` makes the receive non-consuming (message immediately re-visible to other consumers / continues to age in the queue). Inspect `Attributes` for `MessageGroupId`, `SentTimestamp`, and message body to identify the originating Lambda + payload.

**Replay-vs-drop decision tree** (per the 6 covered Lambdas in handoff § 1.2):

| Originating Lambda | Failure class | Recovery action |
|---|---|---|
| `equine-ingestion` (Source 1 — entries) | Async-drop on scheduled invocation | Replay: invoke Lambda with original cron payload via `aws lambda invoke` |
| `equine-ingestion` (Source 2 — fetch_results) | Async-drop on scheduled invocation | Replay: invoke Lambda with `action=fetch_results` payload |
| `equine-results` (matcher) | Async-drop on matcher invocation | Drop: matcher re-runs on next scheduled invocation; no payload-specific work |
| `equine-nyra-workouts` (Source 3) | Async-drop on scheduled invocation | Replay: invoke Lambda manually OR use `manual_nyra_workouts.py` (Section 3) |
| `equine-wr-inference` | Async-drop on inference invocation | Replay: `rerun_inference.py --lambdas wr` (Section 3) |
| `equine-pl-inference` | Async-drop on inference invocation | Replay: `rerun_inference.py --lambdas pl` (Section 3) |
| `equine-ls-inference` | Async-drop on inference invocation | Replay: `rerun_inference.py --lambdas ls` (Section 3) |

After replay/drop decision, consume the DLQ message:
```
aws sqs receive-message \
    --queue-url https://sqs.us-east-1.amazonaws.com/584812014683/equine-async-failure-dlq \
    --max-number-of-messages 1
# Note ReceiptHandle from output, then:
aws sqs delete-message \
    --queue-url https://sqs.us-east-1.amazonaws.com/584812014683/equine-async-failure-dlq \
    --receipt-handle <ReceiptHandle-from-receive>
```

If a DLQ message attributes to a Lambda **not** in the 6-covered list (handoff § 1.2), halt-and-surface to Tony — substrate divergence from documented coverage.

### 2.4 — Orphan-Watching Alarms (Special Handling)

Four alarms per handoff § 1.4 watch ORPHAN Lambdas (no active invocation source):
- `equine-feature-engineering-errors` (Alarm 3)
- `equine-feature-engineering-throttles` (Alarm 4)
- `equine-inference-errors` (Alarm 6)
- `equine-inference-throttles` (Alarm 7)

**Baseline expectation**: Known-quiet. These Lambdas have no recurring invocation source per handoff § 1.4 — `equine-feature-engineering` has zero EventBridge rules targeting it (full scan of 22 ENABLED rules); `equine-inference` legacy Lambda's daily rule is DISABLED.

**Firing = anomaly**: A firing orphan-watching alarm indicates an unexpected invocation has occurred. This is not a normal recovery path. Substrate-trace required: who invoked the Lambda? Console, ad-hoc CLI, residual scheduler, accidental cross-Lambda call.

**Disposition reference**: Post-Phase-B CDK reconciliation pass per handoff § 5.2 will retire both Lambdas + cleanup the 4 alarms. Do NOT modify alarm configuration at runbook scope.

---

## Section 3 — Manual Recovery Tools

Four tools at `scripts/`. Each tool sourced from argparse block with file:line citation. Worked-example sequence: dry-run → review → execute → smoke test.

### 3.1 — `manual_nyra_workouts.py`

- **File**: `scripts/manual_nyra_workouts.py` (argparse at lines 201–226)
- **When to use**: NYRA gap detected; Source 3 degraded (`equine-nyra-workouts-errors`, `equine-nyra-workouts-invocations-absence`, `equine-nyra-workouts-daily-cron-absence`, or `equine-workouts-objects-written-today` filtered to NYRA-infix absence). A.6.b deliverable per handoff § 1.5.
- **CLI args** (verbatim from argparse block at lines 204–225):
  - `--start-date` (required): Start date (YYYY-MM-DD, inclusive)
  - `--end-date` (required): End date (YYYY-MM-DD, inclusive)
  - `--execute` (action="store_true"): Apply writes to DB. Default behavior is dry-run (no writes); pass --execute to commit.
  - `--tracks` (default: `SAR,BEL,AQU`): Comma-separated NYRA tracks to fetch. Default: SAR,BEL,AQU (all NYRA_TRACKS).
- **Dry-run mode**: Omit `--execute` flag. Default behavior is dry-run (no writes).
- **`--execute` mode**: Pass `--execute` to apply writes to DB.
- **Smoke test post-run** (workouts table for target date):
  ```sql
  SELECT track, COUNT(*) AS workout_count
  FROM workouts
  WHERE work_date BETWEEN '<start-date>' AND '<end-date>'
    AND track IN ('SAR', 'BEL', 'AQU')
  GROUP BY track
  ORDER BY track;
  ```
- **Worked example** (recover NYRA gap for 2026-05-09):
  ```
  # 1. Dry-run
  python scripts/manual_nyra_workouts.py --start-date 2026-05-09 --end-date 2026-05-09
  # 2. Review dry-run output
  # 3. Execute
  python scripts/manual_nyra_workouts.py --start-date 2026-05-09 --end-date 2026-05-09 --execute
  # 4. Smoke test (run smoke SQL above with substituted dates)
  ```

### 3.2 — `backfill_d2.py`

- **File**: `scripts/backfill_d2.py` (argparse at lines 341–357)
- **When to use**: Entries+races backfill needed for specific date range; `equine-entries-qualifying-tracks-missing` alarm fired OR `equine-ingestion-errors` fired for the 11:00 UTC Source 1 invocation. Phase A recovery script per handoff § 1.5.
- **CLI args** (verbatim from argparse block at lines 342–356):
  - `--start-date` (required): Backfill start date (YYYY-MM-DD, inclusive)
  - `--end-date` (required): Backfill end date (YYYY-MM-DD, inclusive)
  - `--execute` (action="store_true"): Apply writes to DB. Default behavior is dry-run (no writes); pass --execute to commit.
- **Dry-run mode**: Omit `--execute` flag. Default behavior is dry-run.
- **`--execute` mode**: Pass `--execute` to apply writes to DB.
- **Smoke test post-run** (entries + races tables for target date):
  ```sql
  SELECT r.race_date, COUNT(DISTINCT r.race_id) AS races, COUNT(e.entry_id) AS entries
  FROM races r
  LEFT JOIN entries e ON e.race_id = r.race_id
  WHERE r.race_date BETWEEN '<start-date>' AND '<end-date>'
  GROUP BY r.race_date
  ORDER BY r.race_date;
  ```
- **Worked example** (recover entries gap for 2026-05-08):
  ```
  python scripts/backfill_d2.py --start-date 2026-05-08 --end-date 2026-05-08
  python scripts/backfill_d2.py --start-date 2026-05-08 --end-date 2026-05-08 --execute
  # Smoke test SQL with dates substituted
  ```

### 3.3 — `backfill_d3.py`

- **File**: `scripts/backfill_d3.py` (argparse at lines 256–272)
- **When to use**: Results backfill needed for specific date range; `equine-results-rows-written-today` alarm fired OR `equine-fetch-results-nightly-cron-absence` fired OR `equine-ingestion-errors` fired for the 01:30 UTC Source 2 invocation. Phase A recovery script per handoff § 1.5.
- **CLI args** (verbatim from argparse block at lines 257–271):
  - `--start-date` (required): Backfill start date (YYYY-MM-DD, inclusive)
  - `--end-date` (required): Backfill end date (YYYY-MM-DD, inclusive)
  - `--execute` (action="store_true"): Apply writes to DB. Default behavior is dry-run (no writes); pass --execute to commit.
- **Dry-run mode**: Omit `--execute` flag. Default behavior is dry-run.
- **`--execute` mode**: Pass `--execute` to apply writes to DB.
- **Smoke test post-run** (results table for target date):
  ```sql
  SELECT r.race_date, COUNT(*) AS results_rows
  FROM results res
  JOIN races r ON res.race_id = r.race_id
  WHERE r.race_date BETWEEN '<start-date>' AND '<end-date>'
  GROUP BY r.race_date
  ORDER BY r.race_date;
  ```
- **Worked example** (recover results gap for 2026-05-08):
  ```
  python scripts/backfill_d3.py --start-date 2026-05-08 --end-date 2026-05-08
  python scripts/backfill_d3.py --start-date 2026-05-08 --end-date 2026-05-08 --execute
  # Smoke test SQL with dates substituted
  ```

### 3.4 — `rerun_inference.py`

- **File**: `scripts/rerun_inference.py` (argparse at lines 141–174)
- **When to use**: Ad-hoc WR/PL/LS inference re-run for specific date range; any of `equine-wr-predictions-deficit`, `equine-pl-predictions-deficit`, `equine-ls-predictions-deficit` fired OR `equine-{wr,pl,ls}-inference-errors` fired.
- **CLI args** (verbatim from argparse block at lines 144–173):
  - `--start-date` (required): Re-trigger start date (YYYY-MM-DD, inclusive)
  - `--end-date` (required): Re-trigger end date (YYYY-MM-DD, inclusive)
  - `--execute` (action="store_true"): Invoke inference Lambdas. Default behavior is dry-run (no invocations); pass --execute to fire.
  - `--style` (default: `general`): WR/PL inference style override (default: general). LS handler does not accept style; key omitted from LS payload.
  - `--lambdas` (default: `wr,pl,ls`): Comma-separated subset of inference Lambdas to invoke. Tokens: wr, pl, ls. Default: wr,pl,ls (all three).
- **Dry-run mode**: Omit `--execute` flag. Default behavior is dry-run (no invocations).
- **`--execute` mode**: Pass `--execute` to fire (invoke inference Lambdas).
- **Wall-clock baseline**: 11-day window ≈ 7 min per handoff § 1.5 (rerun_inference 11-day window deliverable). Single-day runs are ~30–60s as proportional baseline.
- **Smoke test post-run** (wr_predictions + pl_predictions + ls_predictions per layer per target date):
  ```sql
  SELECT '<target-date>'::date AS race_date,
         (SELECT COUNT(*) FROM wr_predictions wp
          JOIN races r ON wp.race_id = r.race_id
          WHERE r.race_date = '<target-date>' AND wp.style = 'general') AS wr_general,
         (SELECT COUNT(*) FROM pl_predictions pp
          JOIN races r ON pp.race_id = r.race_id
          WHERE r.race_date = '<target-date>' AND pp.style = 'general') AS pl_general,
         (SELECT COUNT(*) FROM ls_predictions lp
          JOIN races r ON lp.race_id = r.race_id
          WHERE r.race_date = '<target-date>') AS ls_count;
  ```
  Per handoff § 1.5 (predictions spot-check 8 dates): WR=PL=LS exactly when pipeline is healthy. LS reads from `wr_predictions` per handoff § 2.11; LS handler does not accept style per A.6.b finding (handoff § 2.9).
- **Worked example** (rerun all three layers for 2026-05-08):
  ```
  # 1. Dry-run
  python scripts/rerun_inference.py --start-date 2026-05-08 --end-date 2026-05-08
  # 2. Review dry-run output
  # 3. Execute
  python scripts/rerun_inference.py --start-date 2026-05-08 --end-date 2026-05-08 --execute
  # 4. Smoke test SQL above with date substituted
  ```
- **Subset example** (rerun WR + LS only — common pattern when WR was broken and LS inherits from `wr_predictions`):
  ```
  python scripts/rerun_inference.py --start-date 2026-05-08 --end-date 2026-05-08 --lambdas wr,ls --execute
  ```

---

## Section 4 — Known Operational Expectations

Per handoff § 1.6 and §§ 5.1 / 5.2. Observational only — no disposition recommendations.

### 4.1 — Equibase Chart-Failure (Open Thread 1)

`download_charts.py` exits 1 daily with `new_pdfs=0` across 3 captured days (handoff §§ 1.6, 5.1). Non-blocking for Source 4 workouts step (Source 4 producer `run_daily_refresh.sh` continues to write workout-load S3 objects; chart-failure does not propagate to Source 4 outputs).

SNS_TOPIC_ARN set in cron env: `arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts` (verbatim from handoff § 5.1). SNS alerts may be firing daily until Tony decision lands per handoff § 5.1.

Operator action at runbook scope: none. Disposition options enumerated in handoff § 5.1 are pending Tony decision; runbook will be updated when disposition is ratified.

### 4.2 — Matcher Lambda Sparse Invocation (Open Thread 2)

`equine-results` matcher Lambda fired 2 of 7 days observed in last week (May 9 + May 11) per handoff §§ 1.6, 1.4. Per F-D4-2-β ratification (handoff § 5.2), Phase B substrate review will classify as **sparse-by-design** (matcher only runs on race-results-arriving days) vs **silently-broken-on-5-of-7-days**.

Operator action at runbook scope: `equine-results-invocations-absence` alarm (Alarm 23) firing should be observed but not actioned with the standard "invocation-absence → re-enable cron" path until Phase B classification lands. Inspect alarm + EventBridge rule state for substrate; defer disposition.

---

## End of Runbook

**Authoring scope**: Phase A D5 dispatch — operator reference for daily ingestion + inference pipeline. Scope matches handoff § 3.1 D5 authoring contract.

**Substrate citations**: All operational facts cite handoff section, prior dispatch report, or file:line. No fact stands without citation footprint. Where alarm-config detail (threshold values, evaluation periods, math expression for non-A.5-deliverable alarms) was not present in handoff substrate, runbook directs operator to "inspect alarm config in CloudWatch console for detail" rather than inventing values.

**Tools**: Argparse blocks verbatim from `scripts/manual_nyra_workouts.py:201-226`, `scripts/backfill_d2.py:341-357`, `scripts/backfill_d3.py:256-272`, `scripts/rerun_inference.py:141-174`.

**Next session**: D6 bundled bible patches (handoff § 3.2) → Phase A close-out (handoff § 3.3) → Phase B entry (handoff § 4).
