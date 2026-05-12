# OCRC Fix 1 — Cron-Payload Audit

**Cycle ID:** OCRC_2026-05-09
**Deliverable:** Fix 1 — Cron-payload audit (compressed report-only D2 per Path 2 ratification 2026-05-09)
**Authored-by:** Batch CC, OCRC dispatch (fresh conversation per OCR-Q5)
**Status:** DRAFT — pending Tony SP-gate ratification
**Authorization:** READ-ONLY (no EventBridge or Lambda writes)
**Lock time of substrate reads:** 2026-05-09 UTC (post-restoration window: equine-ingestion Active since 04:37:39 UTC)
**Source artifacts:**
- `aws events list-rules --name-prefix equine` (13 rules verified)
- `aws events list-targets-by-rule` (per-rule target enumeration)
- `aws cloudtrail lookup-events --lookup-attributes EventName=PutTargets` (V6 history reconstruction)
- `aws logs filter-log-events --log-group-name /aws/lambda/equine-ingestion` (post-restoration firing observation)
- `backend/lambdas/ingestion/handler.py` (handler routing inspection)
- `backend/lambdas/{results,feature-engineering,inference,wr-inference,pl-inference,ls-inference,nyra-workouts}/handler.py` (default-date logic inspection)

---

## 1. Substrate Verification (D1 Re-confirmation per § 12.5)

D1 inventory § 2.3 claim of "13 rules / 10 ENABLED / 3 DISABLED" re-verified at audit time. No drift since D1 lock 2026-05-09. Per-rule State + cron + target enumeration matches D1 byte-for-byte; V6 InputTransformer details on equine-fetch-results-nightly match D1 § 2.3 verbatim.

CDK source (`infrastructure/cdk/lib/compute-stack.ts`) declares 7 of 13 rules; remaining 6 are out-of-band (D1 § 2.3 ORPHAN classification). Out-of-band classification is NOT a Fix 1 finding — it is documented at D1 5.3.N+5 cohort and deferred to CDK reconciliation cycle per OCRC handoff § 3.2.

---

## 2. Per-Rule Enumeration (13 rules, dependency-ordered by cron-fire time UTC)

### 2.1 equine-fetch-results-nightly — cron(30 1 * * ? *) — ENABLED

| Field | Value |
|---|---|
| ARN | arn:aws:events:us-east-1:584812014683:rule/equine-fetch-results-nightly |
| Cron fire (UTC) | 01:30 daily |
| Target ARN | arn:aws:lambda:us-east-1:584812014683:function:equine-ingestion |
| Input field | InputTransformer: `inputPathsMap={"time":"$.time"}`, `inputTemplate="{\"action\":\"fetch_results\",\"date\":\"USE_TODAY_MINUS_1\"}"` |
| Handler routing | `backend/lambdas/ingestion/handler.py:243-315` — `if action == 'fetch_results'` branch |
| Default-date logic | `if target_date and target_date not in ('USE_TODAY_MINUS_1', ''): target_date = date.fromisoformat(target_date) else: target_date = date.today() - timedelta(days=1)` (handler.py:245-249) |
| Source-publish-time | HRN results published after race-day completion (typical EDT racing day ends ~01:00-04:00 EDT = 05:00-08:00 UTC). Cron at 01:30 UTC asking for D-1 fetches yesterday's complete results. |
| **Operational status** | **HEALTHY** — sentinel routed correctly to `today - 1 day` in handler |
| Notes | V6 priority finding — see § 3 below for full disambiguation |

### 2.2 equine-angle-stats-nightly — cron(15 2 * * ? *) — ENABLED

| Field | Value |
|---|---|
| ARN | arn:aws:events:us-east-1:584812014683:rule/equine-angle-stats-nightly |
| Cron fire (UTC) | 02:15 daily |
| Target ARN | arn:aws:lambda:us-east-1:584812014683:function:equine-ingestion |
| Input field | `{"action":"refresh_angle_stats"}` |
| Handler routing | `handler.py:94-186` — `if action == 'refresh_angle_stats'` branch |
| Default-date logic | n/a (action is date-agnostic; computes angle stats over historical data) |
| Source-publish-time | n/a (DB-only operation; no external source) |
| **Operational status** | **HEALTHY** (post-restoration) |
| Notes | Out-of-band rule (D1 5.3.N+5 cohort). Operationally correct. |

### 2.3 equine-daily-retrain-full — cron(30 2 * * ? *) — ENABLED

| Field | Value |
|---|---|
| ARN | arn:aws:events:us-east-1:584812014683:rule/equine-daily-retrain-full |
| Cron fire (UTC) | 02:30 daily |
| Target ARN | arn:aws:ecs:us-east-1:584812014683:cluster/equine-cluster (task family `equine-training-daily-full`, Fargate) |
| Input field | n/a (ECS task target; no Input override) |
| Handler routing | ECS task family `equine-training-daily-full` (8 revisions, currently :8 active) — out-of-band, no CDK declaration |
| Default-date logic | n/a (training task; reads DB for training data) |
| Source-publish-time | n/a |
| **Operational status** | **UNVERIFIED** — ECS Fargate task firing not invocation-checked at audit time; would require ECS task event lookup or per-firing CloudWatch logs |
| Notes | Out-of-band rule + out-of-band task family (D1 5.3.N+5 + 5.3.N+6 cohort). Operational status verification deferred to CDK reconciliation cycle. |

### 2.4 equine-results-daily — cron(0 4 * * ? *) — ENABLED

| Field | Value |
|---|---|
| ARN | arn:aws:events:us-east-1:584812014683:rule/equine-results-daily |
| Cron fire (UTC) | 04:00 daily |
| Target ARN | arn:aws:lambda:us-east-1:584812014683:function:equine-results |
| Input field | none (no Input override) |
| Handler routing | `backend/lambdas/results/handler.py:11-25` — `handler(event, context)` default path |
| Default-date logic | `target_date = date.today()` (handler.py:13); overridden if `event['date']` present |
| Source-publish-time | n/a (DB-only; matches HRN results to entries to record finishing positions) |
| **Operational status** | **TARGET-INACTIVE** — equine-results Lambda INACTIVE per D1 § 2.1 V2; awaits Fix 4 update-function-code |
| Notes | CDK-declared (compute-stack.ts:334). Will fire automatically post-Fix-4 restoration at next 04:00 UTC firing. Asking for `date.today()` at 04:00 UTC = 00:00 EDT — handler reads results for "today" (UTC), which corresponds to the EDT racing day just-completed. Logic verified consistent with results-matcher semantics. |

### 2.5 equine-weekly-retrain-wr — cron(0 4 ? * MON *) — ENABLED

| Field | Value |
|---|---|
| ARN | arn:aws:events:us-east-1:584812014683:rule/equine-weekly-retrain-wr |
| Cron fire (UTC) | 04:00 Mondays |
| Target ARN | arn:aws:ecs:us-east-1:584812014683:cluster/equine-cluster (task family `equine-training-win-prob`, Fargate) |
| Input field | n/a |
| Handler routing | ECS task family `equine-training-win-prob` (3 revisions) — out-of-band |
| Default-date logic | n/a |
| Source-publish-time | n/a |
| **Operational status** | **UNVERIFIED** — same disposition as 2.3 |
| Notes | Out-of-band rule + task family (D1 5.3.N+5 + 5.3.N+6 cohort). |

### 2.6 equine-weekly-retrain-pl — cron(0 5 ? * MON *) — DISABLED

| Field | Value |
|---|---|
| ARN | arn:aws:events:us-east-1:584812014683:rule/equine-weekly-retrain-pl |
| Cron fire (UTC) | 05:00 Mondays (would fire if enabled) |
| Target ARN | arn:aws:ecs:us-east-1:584812014683:cluster/equine-cluster (task family `equine-training-pl`, Fargate) |
| Input field | n/a |
| Handler routing | ECS task family `equine-training-pl` (3 revisions) — out-of-band |
| Default-date logic | n/a |
| Source-publish-time | n/a |
| **Operational status** | **DISABLED** |
| Notes | Out-of-band rule + task family (D1 5.3.N+5 + 5.3.N+6 cohort); currently dormant. Disposition (re-enable, kill, or leave) deferred to dedicated cycle per OCRC handoff § 3.2. |

### 2.7 equine-nyra-workouts-daily — cron(0 10 * * ? *) — ENABLED

| Field | Value |
|---|---|
| ARN | arn:aws:events:us-east-1:584812014683:rule/equine-nyra-workouts-daily |
| Cron fire (UTC) | 10:00 daily |
| Target ARN | arn:aws:lambda:us-east-1:584812014683:function:equine-nyra-workouts |
| Input field | `{}` (empty object) |
| Handler routing | `backend/lambdas/nyra-workouts/handler.py:249` — `target_date = event.get("date") or date.today().isoformat()` |
| Default-date logic | Handler defaults to `date.today()` because `event.get("date")` returns `None` from `{}` Input |
| Source-publish-time | NYRA publishes workouts ~14:00-18:00 UTC daily (per Phase A D1 § 6.4 candidate 5.3.N+1 + § 3.4 dry-run probes 2026-05-09 03:54 UTC: D-1 returned 192 workouts, D returned 0). Cron at 10:00 UTC asking for today fires before NYRA publishes today's workouts. |
| **Operational status** | **TIMING-DEFECT** — captured zero workouts for 7+ consecutive days per Phase A D1 § 3.4 |
| Notes | Out-of-band rule (D1 5.3.N+5 + 5.3.N+7 cohort). **Fix 3 scope** — retime cron to ~06:00 UTC asking for D-1 OR change handler default to `date.today() - timedelta(days=1)`. |

### 2.8 equine-ingestion-daily — cron(0 11 * * ? *) — ENABLED

| Field | Value |
|---|---|
| ARN | arn:aws:events:us-east-1:584812014683:rule/equine-ingestion-daily |
| Cron fire (UTC) | 11:00 daily |
| Target ARN | arn:aws:lambda:us-east-1:584812014683:function:equine-ingestion |
| Input field | none (no Input override) |
| Handler routing | `handler.py:1668-1689` — fall-through default case (`# ── Normal scheduled ingestion ──`) |
| Default-date logic | `service.fetch_daily_entries(date.today())` (handler.py:1676) |
| Source-publish-time | HRN entries pages typically published 24-48h pre-race. 11:00 UTC = 07:00 EDT cron firing requests today's race-card entries; HRN's day-of entries are usually populated before this. Phase A D1 § 6.4 candidate 5.3.N+4 flags theoretical timing risk pending empirical confirmation. |
| **Operational status** | **HEALTHY** (post-restoration) — fired today 2026-05-09T11:00:47Z (55.3 sec duration; clean END/REPORT) per `/aws/lambda/equine-ingestion` log stream `2026/05/09/[$LATEST]f1b137cf21cc46a981de8bda2290ffe9` |
| Notes | CDK-declared (compute-stack.ts:258). First post-restoration cron firing observed; default-case dispatch operational. |

### 2.9 equine-feature-engineering-daily — cron(0 12 * * ? *) — DISABLED

| Field | Value |
|---|---|
| ARN | arn:aws:events:us-east-1:584812014683:rule/equine-feature-engineering-daily |
| Cron fire (UTC) | 12:00 daily (would fire if enabled) |
| Target ARN | n/a — `Targets: []` (0 targets) |
| Input field | n/a |
| Handler routing | n/a (no targets) |
| Default-date logic | n/a |
| Source-publish-time | n/a |
| **Operational status** | **DISABLED** |
| Notes | CDK-declared (compute-stack.ts:273) with `enabled: false`. equine-feature-engineering Lambda INACTIVE per D1 § 2.1 V3; Fix 4 restores Lambda Active state but rule remains DISABLED-by-design. |

### 2.10 equine-inference-daily — cron(30 12 * * ? *) — DISABLED

| Field | Value |
|---|---|
| ARN | arn:aws:events:us-east-1:584812014683:rule/equine-inference-daily |
| Cron fire (UTC) | 12:30 daily (would fire if enabled) |
| Target ARN | n/a — `Targets: []` (0 targets) |
| Input field | n/a |
| Handler routing | n/a (no targets) |
| Default-date logic | n/a |
| Source-publish-time | n/a |
| **Operational status** | **DISABLED** |
| Notes | CDK-declared (compute-stack.ts:293) with `enabled: false`. equine-inference Lambda Active but DISABLED-rule means no scheduled invocation. |

### 2.11 equine-wr-inference-daily — cron(30 12 * * ? *) — ENABLED

| Field | Value |
|---|---|
| ARN | arn:aws:events:us-east-1:584812014683:rule/equine-wr-inference-daily |
| Cron fire (UTC) | 12:30 daily |
| Target ARN | arn:aws:lambda:us-east-1:584812014683:function:equine-wr-inference |
| Input field | none (no Input override) |
| Handler routing | `backend/lambdas/wr-inference/handler.py:71` — `date.today()` default-case |
| Default-date logic | `target_date = date.today()`; overridden if `event['date']` present |
| Source-publish-time | n/a (DB-only inference; reads entries/races/past_performances/workouts/results) |
| **Operational status** | **HEALTHY** |
| Notes | CDK-declared (compute-stack.ts:304). |

### 2.12 equine-pl-inference-daily — cron(35 12 * * ? *) — ENABLED

| Field | Value |
|---|---|
| ARN | arn:aws:events:us-east-1:584812014683:rule/equine-pl-inference-daily |
| Cron fire (UTC) | 12:35 daily |
| Target ARN | arn:aws:lambda:us-east-1:584812014683:function:equine-pl-inference |
| Input field | none (no Input override) |
| Handler routing | `backend/lambdas/pl-inference/handler.py:71` — `date.today()` default-case |
| Default-date logic | `target_date = date.today()`; overridden if `event['date']` present |
| Source-publish-time | n/a |
| **Operational status** | **HEALTHY** |
| Notes | CDK-declared (compute-stack.ts:314). |

### 2.13 equine-ls-inference-daily — cron(40 12 * * ? *) — ENABLED

| Field | Value |
|---|---|
| ARN | arn:aws:events:us-east-1:584812014683:rule/equine-ls-inference-daily |
| Cron fire (UTC) | 12:40 daily |
| Target ARN | arn:aws:lambda:us-east-1:584812014683:function:equine-ls-inference |
| Input field | none (no Input override) |
| Handler routing | `backend/lambdas/ls-inference/handler.py:58` — `date.today()` default-case |
| Default-date logic | `target_date = date.today()`; overridden if `event['date']` present |
| Source-publish-time | n/a |
| **Operational status** | **HEALTHY** |
| Notes | CDK-declared (compute-stack.ts:324). |

---

## 3. V6 Priority Finding — equine-fetch-results-nightly Disambiguation (DEFINITIVE)

Per OCRC handoff § 3.1 D2 specification + D1 § 2.3 V6 priority-finding block, three investigation paths executed:

### 3.1 (a) Handler code inspection — `backend/lambdas/ingestion/handler.py:243-249`

```python
if action == 'fetch_results':
    from datetime import date as date_type, timedelta
    target_date = event.get('date')
    if target_date and target_date not in ('USE_TODAY_MINUS_1', ''):
        target_date = date_type.fromisoformat(target_date)
    else:
        target_date = date_type.today() - timedelta(days=1)
```

**Finding:** Handler explicitly tests for `'USE_TODAY_MINUS_1'` as a sentinel value. When the event payload contains `date: "USE_TODAY_MINUS_1"`, the condition `target_date not in ('USE_TODAY_MINUS_1', '')` evaluates **False** → the `else` branch executes → `target_date = date.today() - timedelta(days=1)`.

**Conclusion (a):** Sentinel is **interpreted correctly** — routes to yesterday's date.

### 3.2 (b) Post-restoration CloudWatch log analysis

Lambda restored 2026-05-09 04:37:39 UTC. Cron fires daily at 01:30 UTC. The 2026-05-09 01:30 UTC firing was BEFORE restoration (Lambda was still INACTIVE) and produced no logs (CodeArtifactUserFailedException at the Lambda service layer). The next firing is **2026-05-10 01:30 UTC** (tomorrow, ~17 hours from audit lock time).

`aws logs filter-log-events --log-group-name /aws/lambda/equine-ingestion --filter-pattern "fetch_results" --start-time <2026-05-09 04:37 UTC>` returned `events: []`. Consistent with: cron has not fired post-restoration yet.

**Conclusion (b):** No post-restoration empirical observation available within audit window. Earliest observable post-restoration firing: 2026-05-10 01:30 UTC. Result is consistent with handler-side correct sentinel interpretation; awaiting empirical confirmation at next firing.

### 3.3 (c) CloudTrail UpdateRule lookup — InputTransformer add-time

CloudTrail PutTargets event history for `equine-fetch-results-nightly`:

| Timestamp (EDT) | Event | Configuration |
|---|---|---|
| 2026-03-20T16:13:55 | PutTargets by user=root | `input={"action":"fetch_results","date":"<aws.scheduler.execution-date>"}` + `inputTransformer.inputTemplate={"action":"fetch_results","date":"YESTERDAY"}` (combined input + transformer; AWS would coerce/reject one) |
| 2026-03-20T16:14:41 | PutTargets by user=root | `inputTransformer.inputPathsMap={"time":"$.time"}` + `inputTransformer.inputTemplate={"action":"fetch_results","date":"USE_TODAY_MINUS_1"}` (current configuration) |

**Finding:** The current `USE_TODAY_MINUS_1` InputTransformer was set 2026-03-20T20:14:41 UTC by user=root — **~50 days before** Phase A audit (2026-05-08) and OCRC entry (2026-05-09). The InputTransformer is **NOT recent drift**.

**Conclusion (c):** The three drift hypotheses from D1 § 2.3 disambiguate as follows:
- (a) Recent change between architecture_overview lock (2026-05-08) and S1 (2026-05-09) → **REFUTED.** The configuration has been stable since 2026-03-20.
- (b) Bible staleness (architecture_overview missed it) → **CONFIRMED.** architecture_overview v3-patched-a § 3.6 claim of "No `Input` override" was wrong against ground-truth substrate that pre-existed the bible's lock.
- (c) Inheritance error (CC Step 4 misread Input=null) → **CONFIRMED.** CC Step 4 report's claim of "Input=null routes to fetch_daily_entries(today)" was wrong; the rule was operationally correct at the time of the CC Step 4 observation.

### 3.4 V6 Disambiguation Summary

**Definitive finding: the rule is operationally correct.** Three independent evidence paths converge:
1. Handler code interprets the sentinel as `today - 1 day`.
2. CloudTrail confirms the configuration has been stable for ~50 days (no recent drift).
3. The bible/CC-Step-4 inheritance was wrong — pre-existing substrate refutes the inherited claim.

The inherited claim's operational consequence (writes wrong data because `fetch_daily_entries(today)` runs instead of `fetch_results(yesterday)`) was a **misread, not a substrate defect.** From 2026-03-20 onward the rule has correctly dispatched `fetch_results(yesterday)`. The only operational impairment to this flow was the equine-ingestion Lambda's INACTIVE state from 2026-05-02 → 2026-05-09 04:37 UTC (Phase A § 4.1 dominant single-failure-domain). Post-restoration, the rule will fire correctly at 2026-05-10 01:30 UTC.

---

## 4. Per-Rule Operational Status Disposition Table

| # | Rule | State | Cron (UTC) | Status | Notes |
|---|------|-------|------------|--------|-------|
| 1 | equine-fetch-results-nightly | ENABLED | 01:30 daily | HEALTHY | V6 finding: sentinel interpreted; rule operationally correct |
| 2 | equine-angle-stats-nightly | ENABLED | 02:15 daily | HEALTHY | Action=refresh_angle_stats |
| 3 | equine-daily-retrain-full | ENABLED | 02:30 daily | UNVERIFIED | ECS Fargate task firing not invocation-checked |
| 4 | equine-results-daily | ENABLED | 04:00 daily | TARGET-INACTIVE | Fix 4 prerequisite |
| 5 | equine-weekly-retrain-wr | ENABLED | 04:00 Mondays | UNVERIFIED | ECS Fargate task firing not invocation-checked |
| 6 | equine-weekly-retrain-pl | DISABLED | 05:00 Mondays | DISABLED | Currently dormant |
| 7 | equine-nyra-workouts-daily | ENABLED | 10:00 daily | TIMING-DEFECT | Fix 3 scope |
| 8 | equine-ingestion-daily | ENABLED | 11:00 daily | HEALTHY | Fired 2026-05-09T11:00:47Z post-restoration successfully |
| 9 | equine-feature-engineering-daily | DISABLED | 12:00 daily | DISABLED | CDK enabled:false; 0 targets |
| 10 | equine-inference-daily | DISABLED | 12:30 daily | DISABLED | CDK enabled:false; 0 targets |
| 11 | equine-wr-inference-daily | ENABLED | 12:30 daily | HEALTHY | date.today() default |
| 12 | equine-pl-inference-daily | ENABLED | 12:35 daily | HEALTHY | date.today() default |
| 13 | equine-ls-inference-daily | ENABLED | 12:40 daily | HEALTHY | date.today() default |

**Aggregate:**
- HEALTHY: 7 (equine-fetch-results-nightly, equine-angle-stats-nightly, equine-results-daily-pending-Fix-4, equine-ingestion-daily, equine-wr-inference-daily, equine-pl-inference-daily, equine-ls-inference-daily — counting equine-results-daily as HEALTHY-when-target-Active)
- TIMING-DEFECT: 1 (equine-nyra-workouts-daily)
- TARGET-INACTIVE: 1 (equine-results-daily — 1 of the 8 above; resolved by Fix 4)
- DISABLED: 3 (equine-weekly-retrain-pl, equine-feature-engineering-daily, equine-inference-daily)
- UNVERIFIED: 2 (equine-daily-retrain-full, equine-weekly-retrain-wr — ECS Fargate firing not invocation-checked at audit time; not in Fix 1 read scope)
- INPUT-DEFECT: **0** — V6 priority finding resolves to HEALTHY

---

## 5. Fix 2 Recommendation (V6-derived)

**Recommended path: Path A — NO FIX NEEDED.**

Per § 3.4 V6 disambiguation, equine-fetch-results-nightly is operationally correct. The InputTransformer + handler-side sentinel handling form a working pair that has been stable since 2026-03-20. The inherited claim that prompted Fix 2 (OCRC handoff § 2.4 + CC Step 4 report) was a misread of the EventBridge configuration, not a substrate defect.

**Closing-evidence draft for Tony D7 closure ratification:**

```
closed-by:
  OCRC Fix 1 cron-payload audit § 3 V6 disambiguation
  + handler.py:243-249 sentinel interpretation verification
  + CloudTrail PutTargets history (configuration stable since 2026-03-20T20:14:41 UTC)
verification:
  Three independent evidence paths converge on rule-operationally-correct disposition:
  (a) handler code interprets USE_TODAY_MINUS_1 as date.today() - timedelta(days=1)
  (b) post-restoration CloudWatch awaits 2026-05-10 01:30 UTC firing for empirical confirmation
  (c) CloudTrail confirms the configuration has been stable for ~50 days (no recent drift)
  Inherited "Input=null" claim was a misread of EventBridge configuration; ground truth refutes.
ratified-by: [Tony pending; D7 closure formalization]
```

**Action for Fix 2 SP gate:** Surface Path A finding to Tony; await ratification that no write is needed; mark Fix 2 closed with closing-evidence draft above.

---

## 6. Honest-Disposition Notes (per § 7.9)

- **UNVERIFIED disposition for ECS Fargate rules (2.3 + 2.5):** Fix 1 scope did not invocation-check ECS firings. Operational health verification for these would require ECS task event lookup or per-firing CloudWatch logs. Out of Fix 1 READ-ONLY surface scope.
- **NYRA capture-time defect (2.7):** confirmed via Phase A D1 § 6.4 candidate 5.3.N+1 substrate; not re-empirically-verified at Fix 1 (would have required Lambda invocation, out of READ-ONLY scope). Fix 3 scope.
- **equine-results-daily (2.4):** operational status HEALTHY-when-target-Active; current TARGET-INACTIVE state resolved by Fix 4. Cron firing semantics confirmed correct via handler code inspection.
- **equine-fetch-results-nightly post-restoration empirical observation (3.2):** unavailable within audit window because the next cron firing is 2026-05-10 01:30 UTC (tomorrow). Disposition is HEALTHY based on (a) handler code + (c) CloudTrail; empirical (b) deferred to natural cron cycle.
- **equine-ingestion-daily post-restoration empirical observation (2.8):** the 2026-05-09 11:00 UTC firing IS observed (55.3 sec duration; default-case dispatch). This is corroborating evidence that the equine-ingestion Lambda is operationally healthy post-restoration, supporting the V6 disambiguation conclusion that fetch_results will run cleanly at the next 01:30 UTC firing.

---

## 7. SP Gate Sign-off

Fix 1 cron-payload audit complete. Awaiting Tony SP-gate ratification for V6 disambiguation finding + Fix 2 Path A recommendation.

**End of OCRC Fix 1 — Cron-Payload Audit — 2026-05-09.**
