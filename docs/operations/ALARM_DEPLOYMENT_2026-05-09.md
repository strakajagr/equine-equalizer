# OCRC Fix 5 — CloudWatch Alarms Deployment

**Cycle ID:** OCRC_2026-05-09
**Deliverable:** Fix 5 — CloudWatch alarms deployment (compressed D9 per Path 2 ratification)
**Authored-by:** Batch CC, OCRC dispatch
**Status:** DRAFT — pending Tony SP-gate ratification
**Authorization:** `aws cloudwatch put-metric-alarm` + alarm documentation save (per OCR-Q3 § 5.2 + batch prompt § FIX 5)
**Closes:** D1 5.3.N+11 (0 CloudWatch alarms on any equine resource)
**Lock time of substrate reads:** 2026-05-09 ~16:30 UTC

---

## 1. Coverage Scope

22 alarms deployed across 3 alarm classes:

| Class | Count | Purpose |
|---|---|---|
| Lambda Errors | 8 | Per-Lambda Errors metric > 0 over 5min |
| Lambda Throttles | 8 | Per-Lambda Throttles metric > 0 over 5min |
| Lambda Invocations-absence | 3 | Per-Lambda Invocations < 1 over 24h (data-pipeline criticality) |
| Cron-firing absence | 3 | Per-rule Invocations < 1 over 24h (cron-not-firing detection) |

### 1.1 Coverage rationale (per Tony's "use judgment" + 4-inference-Lambda hint)

**Errors + Throttles applied to all 8 Lambdas** — minimum visibility floor; cheap in operational cost.

**Invocations-absence applied to 3 Lambdas** (equine-ingestion + equine-results + equine-nyra-workouts):
- equine-ingestion: central pipeline; runs 3 cron-driven actions; high silent-failure risk
- equine-results: just restored from INACTIVE 2026-05-09 16:21:55Z; high observability value during stabilization
- equine-nyra-workouts: just-retimed cron 2026-05-09 16:11:44Z; high observability value during stabilization

**Invocations-absence skipped on 5 Lambdas:**
- equine-feature-engineering: cron DISABLED-by-design per CDK compute-stack.ts:273; absence alarm would always breach
- equine-inference: cron DISABLED-by-design per CDK compute-stack.ts:293; same
- equine-wr-inference, equine-pl-inference, equine-ls-inference: daily cron + downstream-consumer-visibility (per Tony's hint that "downstream consumers would notice gaps")

**Cron-firing absence applied to 3 EventBridge rules** per batch prompt § FIX 5:
- equine-fetch-results-nightly (cron(30 1 * * ? *))
- equine-nyra-workouts-daily (cron(0 16 * * ? *) post-Fix-3 retime)
- equine-ingestion-daily (cron(0 11 * * ? *))

---

## 2. Window Constraint Note (24h vs 26h)

Batch prompt § FIX 5 specified 26-hour window for invocations-absence and cron-firing alarms (rationale: "26-hour window allows ±2hr cron jitter").

**AWS hard constraint:** `Period × EvaluationPeriods ≤ 86400 sec` per CloudWatch alarm. Single-alarm window cannot exceed 24 hours. Confirmed via AWS CloudWatch PutMetricAlarm API documentation.

**Implementation:** Period=86400, EvaluationPeriods=1 → 24-hour single-period window. 2-hour shortfall vs prompt's ideal documented here.

**False-positive risk assessment:** AWS EventBridge cron jitter is empirically sub-minute. The 24h window with daily cron creates aligned UTC midnight-to-midnight buckets; a daily cron firing at any UTC time within a bucket counts as a hit. False-positive risk from cron jitter alone is negligible.

**Workaround if 26h is later required:** composite alarm combining two 13h-period alarms via OR semantics. Out of Fix 5 scope; deferred unless 24h window proves insufficient operationally.

---

## 3. Per-Alarm Definitions

### 3.1 Errors alarms (8 deployed)

Common spec:
- **Namespace:** `AWS/Lambda`
- **MetricName:** `Errors`
- **Statistic:** `Sum`
- **Period:** 300 (5 min)
- **EvaluationPeriods:** 1
- **Threshold:** 0
- **ComparisonOperator:** `GreaterThanThreshold`
- **TreatMissingData:** `notBreaching`
- **AlarmActions:** `arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts`

Per-alarm dimensions (FunctionName) + alarm name:

| Alarm Name | FunctionName |
|---|---|
| equine-ingestion-errors | equine-ingestion |
| equine-results-errors | equine-results |
| equine-feature-engineering-errors | equine-feature-engineering |
| equine-inference-errors | equine-inference |
| equine-wr-inference-errors | equine-wr-inference |
| equine-pl-inference-errors | equine-pl-inference |
| equine-ls-inference-errors | equine-ls-inference |
| equine-nyra-workouts-errors | equine-nyra-workouts |

### 3.2 Throttles alarms (8 deployed)

Common spec same as 3.1 except:
- **MetricName:** `Throttles`

| Alarm Name | FunctionName |
|---|---|
| equine-ingestion-throttles | equine-ingestion |
| equine-results-throttles | equine-results |
| equine-feature-engineering-throttles | equine-feature-engineering |
| equine-inference-throttles | equine-inference |
| equine-wr-inference-throttles | equine-wr-inference |
| equine-pl-inference-throttles | equine-pl-inference |
| equine-ls-inference-throttles | equine-ls-inference |
| equine-nyra-workouts-throttles | equine-nyra-workouts |

### 3.3 Lambda invocations-absence alarms (3 deployed)

Common spec:
- **Namespace:** `AWS/Lambda`
- **MetricName:** `Invocations`
- **Statistic:** `Sum`
- **Period:** 86400 (24h)
- **EvaluationPeriods:** 1
- **Threshold:** 1
- **ComparisonOperator:** `LessThanThreshold`
- **TreatMissingData:** `breaching`
- **AlarmActions:** `arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts`

| Alarm Name | FunctionName |
|---|---|
| equine-ingestion-invocations-absence | equine-ingestion |
| equine-results-invocations-absence | equine-results |
| equine-nyra-workouts-invocations-absence | equine-nyra-workouts |

### 3.4 Cron-firing absence alarms (3 deployed)

Common spec:
- **Namespace:** `AWS/Events`
- **MetricName:** `Invocations`
- **Statistic:** `Sum`
- **Period:** 86400 (24h)
- **EvaluationPeriods:** 1
- **Threshold:** 1
- **ComparisonOperator:** `LessThanThreshold`
- **TreatMissingData:** `breaching`
- **AlarmActions:** `arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts`

| Alarm Name | RuleName |
|---|---|
| equine-fetch-results-nightly-cron-absence | equine-fetch-results-nightly |
| equine-nyra-workouts-daily-cron-absence | equine-nyra-workouts-daily |
| equine-ingestion-daily-cron-absence | equine-ingestion-daily |

---

## 4. SNS Routing Verification

**Topic:** `arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts`
**Subscription:** email → `tonyragano@gmail.com`
**Subscription state:** confirmed-active (SubscriptionArn = `arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts:02fccc90-97e0-4891-b4f7-068d37ff3eb6` — UUID present, not "PendingConfirmation")

All 22 alarms verified to have `AlarmActions` containing the SNS topic ARN at deploy time. Alarms transition OK → ALARM will publish to topic; SNS will email Tony.

---

## 5. Post-Deploy State

| Alarm | StateValue (at +T~5min) |
|---|---|
| equine-ingestion-errors | OK |
| equine-feature-engineering-errors | INSUFFICIENT_DATA |
| equine-feature-engineering-throttles | INSUFFICIENT_DATA |
| equine-fetch-results-nightly-cron-absence | INSUFFICIENT_DATA |
| equine-inference-errors | INSUFFICIENT_DATA |
| equine-inference-throttles | INSUFFICIENT_DATA |
| equine-ingestion-daily-cron-absence | INSUFFICIENT_DATA |
| equine-ingestion-invocations-absence | INSUFFICIENT_DATA |
| equine-ingestion-throttles | INSUFFICIENT_DATA |
| equine-ls-inference-errors | INSUFFICIENT_DATA |
| equine-ls-inference-throttles | INSUFFICIENT_DATA |
| equine-nyra-workouts-daily-cron-absence | INSUFFICIENT_DATA |
| equine-nyra-workouts-errors | INSUFFICIENT_DATA |
| equine-nyra-workouts-invocations-absence | INSUFFICIENT_DATA |
| equine-nyra-workouts-throttles | INSUFFICIENT_DATA |
| equine-pl-inference-errors | INSUFFICIENT_DATA |
| equine-pl-inference-throttles | INSUFFICIENT_DATA |
| equine-results-errors | INSUFFICIENT_DATA |
| equine-results-invocations-absence | INSUFFICIENT_DATA |
| equine-results-throttles | INSUFFICIENT_DATA |
| equine-wr-inference-errors | INSUFFICIENT_DATA |
| equine-wr-inference-throttles | INSUFFICIENT_DATA |

INSUFFICIENT_DATA is expected post-deploy — alarms need 1+ data-collection cycle before reporting OK. The single OK alarm (equine-ingestion-errors) reflects equine-ingestion's 11:00:47Z + 16:11:33Z invocations with 0 Errors over the trailing 5min Period evaluation.

---

## 6. Operational Notes

### 6.1 First expected ALARM-state surfacings (none expected absent regression)

- **Lambda Errors / Throttles alarms:** will surface ALARM only on actual Errors or Throttles within 5min. Absent regression, all stay OK after data warmup.
- **equine-ingestion-invocations-absence:** equine-ingestion fires daily at 01:30 UTC + 02:15 UTC + 11:00 UTC; 3+ invocations per 24h; alarm should never fire absent broad pipeline failure.
- **equine-results-invocations-absence:** equine-results fires daily at 04:00 UTC; 1 invocation per 24h; alarm should not fire absent regression.
- **equine-nyra-workouts-invocations-absence:** equine-nyra-workouts now fires daily at 16:00 UTC post-Fix-3; 1 invocation per 24h; alarm should not fire absent regression.
- **3 cron-firing absence alarms:** will fire if EventBridge rule itself fails to invoke target (rule disabled, IAM permission revoked, etc.).

### 6.2 First expected post-deploy data points

| Alarm | Expected first ALARM-or-OK reporting |
|---|---|
| Lambda Errors / Throttles (16) | Within ~5-10 min of deploy (5min period) — all should be OK absent regression |
| Lambda Invocations-absence (3) | After ~24h bucket completes (i.e., 2026-05-10 ~UTC midnight or ingest-time-aligned) |
| Cron-firing absence (3) | Same — after first 24h evaluation period |

### 6.3 Manual-triggered detection complement

Per OCRC handoff § 8 item 5 compression: post-Fix-3 NYRA verification compressed to 1-day at fix time + ongoing operational detection. The `equine-nyra-workouts-daily-cron-absence` + `equine-nyra-workouts-invocations-absence` alarms provide the ongoing detection coverage — Tony will receive email if the next-firing 2026-05-10T16:00:00Z fails to trigger or fails to invoke the Lambda.

### 6.4 Alarms NOT deployed (deferred / intentionally absent)

- **Duration alarms:** SKIP per batch prompt § FIX 5 ("skip if uncertain"). Per-Lambda timeout configuration is the safety net (default 300s); a Duration alarm requires a per-Lambda baseline study to set thresholds.
- **ECS task family alarms:** out of Fix 5 scope. Equine-training-{daily-full, pl, win-prob, manual} ECS task families have no operational health monitoring. Deferred to CDK reconciliation cycle (D1 5.3.N+5/+6 cohort).
- **RDS alarms:** out of Fix 5 scope.
- **Composite alarms / SNS-wired runbook integration:** out of Fix 5 scope.
- **5 Lambda invocations-absence alarms** (equine-feature-engineering, equine-inference, equine-wr-inference, equine-pl-inference, equine-ls-inference): per § 1.1 rationale.

---

## 7. Banking-via-Disclosure Acknowledgment

Per batch prompt § FIX 5 implementation guidance: "deploy via direct CLI as out-of-band-but-documented operational infrastructure (acknowledging this adds to 5.3.N+5/+6/+7 cohort but is operationally necessary; banking-via-disclosure rather than CDK-via-future-cycle)."

22 alarms deployed via direct `aws cloudwatch put-metric-alarm` CLI (not CDK). Each alarm is now ORPHAN per D1 § 2 classification taxonomy: present in AWS (E1), not declared in CDK source (E3), not in CFN (E2). This contributes to the CDK-reconciliation backlog cohort (D1 § 5.2 5.3.N+5 / 5.3.N+11). Disposition deferred to future CDK-reconciliation cycle per OCRC handoff § 3.2.

This disclosure is intentional and ratified by Tony at OCRC entry.

---

## 8. Closing-Evidence Draft for D7/D8

D1 5.3.N+11 closure draft:

```
closed-by:
  OCRC Fix 5 alarm deployment 2026-05-09
  + 22 alarms verified via aws cloudwatch describe-alarms
  + SNS routing verified via aws sns list-subscriptions (subscription confirmed-active)
verification:
  All 22 alarms present in CloudWatch with AlarmActions wired to
  arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts;
  alarm states OK (1) + INSUFFICIENT_DATA (21) at deploy time +5min
  (INSUFFICIENT_DATA expected pre-data-warmup);
  per-Lambda Errors + Throttles coverage for all 8 equine Lambdas;
  invocations-absence coverage for 3 critical pipeline Lambdas
  (equine-ingestion + equine-results + equine-nyra-workouts);
  cron-firing absence coverage for 3 EventBridge rules
  (equine-fetch-results-nightly, equine-nyra-workouts-daily,
  equine-ingestion-daily).
ratified-by: [Tony pending; D7 closure formalization]

NOTE: 24h window applied (vs prompt's 26h ideal) per AWS hard constraint
Period × EvaluationPeriods ≤ 86400 sec; documented in § 2.
NOTE: 5 Lambdas without invocations-absence coverage per Tony's
"4-inference-hint" + 2 cron-DISABLED-by-design Lambdas; documented
in § 1.1.
NOTE: Alarms deployed out-of-band (CLI, not CDK); contributes to
5.3.N+5/+11 backlog cohort per banking-via-disclosure pattern.
```

---

**End of OCRC Fix 5 — Alarm Deployment — 2026-05-09.**
