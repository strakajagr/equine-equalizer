# Phase A Suspension Note — 2026-05-09

**Cycle ID:** PHASE_A_2026-05-08
**Cycle Class:** Operational Reliability Cycle (first instantiation)
**Cycle State:** SUSPENDED (not cancelled)
**Suspension Date:** 2026-05-09
**Methodology:** AUDIT_METHODOLOGY v3 (locked 2026-05-08)
**Owner:** Tony
**QB Session:** 2026-05-08 / 2026-05-09 (pre-suspension)
**Resume Gate:** Phase A-prime exits successfully + signal (a) DB evidence collectable for ≥3 consecutive days across all 6 sources

---

## 1. Suspension rationale

Phase A entry premise was Bug #28 column-shift defect as the most urgent reliability defect blocking Phase B (ML Layer Analysis) entry. S1 (D1 source enumeration drafting) surfaced a substantively different reality: production HRN ingestion has been fire-and-fail since 2026-05-02 due to `equine-ingestion` Lambda INACTIVE state (deleted ECR image). Phase A's stated goal — "every source ingests every day, nothing missed" — was already violated for 7+ days before Phase A was scoped. The substrate Phase A was designed to repair is largely absent rather than corrupted.

D2/D3/D4/D5 cannot meaningfully execute against absent substrate:
- D2 Bug #28 fix: parser-side fix is necessary but insufficient; production write path requires Lambda re-activation (PHASE_5_BACKLOG Phase 5.3.20)
- D3 backfill: scope coherence requires distinguishing rows-to-overwrite (Bug #28 corruption window) from rows-to-recover-by-rescraping (post-2026-05-02 fire-and-fail window); the latter is restoration-cycle work
- D4 runbook: documenting an inert system is wasted work
- D5 backlog cleanup: closures gated on D2/D3 outcomes

Tony decision (2026-05-09): suspend Phase A; restore ingestion via Phase A-prime; resume Phase A once resume gate met.

---

## 2. Phase A artifact state at suspension

| Artifact | Path | State |
|---|---|---|
| D1 source status snapshot | `docs/operations/SOURCE_STATUS_AUDIT_2026-05-08.md` | DRAFT — frozen at S1 output; PAUSED marker added to header |
| D1 audit (S2) | n/a | NOT DISPATCHED |
| D2 Bug #28 fix | n/a | SUSPENDED |
| D3 backfill script | n/a | SUSPENDED |
| D4 daily ingestion runbook | n/a | SUSPENDED |
| D5 PHASE_5_BACKLOG cleanup | n/a | SUSPENDED |
| Phase A handoff | `docs/operations/PHASE_A_HANDOFF.md` (proposed; save state TBD) | RATIFIED CONTENT — saved at Tony's discretion |
| Cycle close-out | n/a | DEFERRED until post-resumption cycle exit |

D1 snapshot is methodology-valuable as point-in-time pre-restoration baseline. NOT to be re-run after restoration — re-execute signal (a) against restored substrate produces a delta artifact, not a snapshot replacement.

---

## 3. Resume gate (substrate-verified preconditions)

Phase A resumes when ALL of:

1. `equine-ingestion` Lambda State = `Active` (verified via `aws lambda get-function`)
2. PHASE_5_BACKLOG Phase 5.3.20 closed with closing-evidence reference
3. Schema-drift errors from 2026-05-02→05-03 window resolved or empirically confirmed non-blocking (S1 § 4.2 + § 6.4 candidate 5.3.N+2)
4. Signal (a) DB evidence collectable across all 6 sources for ≥3 consecutive days post-restoration (operational definition: dashboard `counts.entries`, `counts.results` advance daily; NYRA workouts S3 producer + load completes daily; chart parser path executable; HRN workouts producer identified per § 4 below)
5. NYRA cron timing defect resolved (S1 § 6.4 candidate 5.3.N+1) — currently 7/7 production runs scrape zero workouts; resume gate requires non-zero NYRA workouts captured for ≥3 consecutive days

Resume gate verification is QB-tier work performed at Phase A resumption opening; no CC dispatch required to verify gate state.

---

## 4. New defect candidates surfaced by S1 (for PHASE_5_BACKLOG inclusion)

Per § 6.4 of D1 artifact. Add to PHASE_5_BACKLOG.md during Phase A-prime opening agenda or at Phase A resumption D5 work — Tony's choice; documenting both candidate timings. Severity tags pending § 8.4 vocabulary-uniform review at insertion time.

| Candidate | Description | Severity |
|---|---|---|
| 5.3.N+1 | NYRA Workout Cron Capture-Time Defect | HIGH |
| 5.3.N+2 | Schema Drift in equine-ingestion Image SQL | MEDIUM |
| 5.3.N+3 | Undocumented HRN Workout Producer | MEDIUM |
| 5.3.N+4 | HRN Entries Cron Capture-Time Risk (analogue) | LOW pending confirmation |

CloudTrail clue for 5.3.N+3: D1 artifact § 4.4 documents `equine-ingestion` IAM role activity (KMS decrypt at 07:00:53 UTC) coincident with daily HRN workouts S3 upload, despite Lambda INACTIVE. Probable producer candidates: CodeBuild job, ECS task assuming role, local cron with assumed-role credentials, forgotten Lambda with role attached. Phase A-prime restoration cycle's investigation surface.

---

## 5. Banking observation candidates (in-flight; carried across suspension)

Five candidates identified across Phase A entry through suspension. Ratification deferred to Phase A cycle close-out post-resumption per AUDIT_METHODOLOGY v3 banking discipline. Each captured here durably so methodology amendment proposals can be drafted from concrete evidence rather than reconstructed memory.

### 5.1 Operational reliability cycle pattern — first instantiation
**Source:** Q2 ratification, handoff § 9 candidate 1
**Observation:** Phase A established precedent for operational cycle class as distinct from Phase 1 architectural-documentation cohort. Pattern characteristics: hybrid asymmetric tier structure per § 4.21 discipline-scaling; three-signal triangulation per Q4; source code modification gating to dedicated CC sessions per Q3; SELECT-only DB scope as default authorization.
**Methodology amendment candidate:** new § in AUDIT_METHODOLOGY v3 codifying operational cycle class — entry gate, tier scaling, authorization defaults, exit criteria template.

### 5.2 Operational artifacts directory convention — first-of-class precedent
**Source:** Q6 ratification, handoff § 9 candidate 2
**Observation:** `docs/operations/` established sibling to `docs/bible/`. Distinguishes operational reference (runbooks, status snapshots, cycle logs, suspension notes) from architectural reference (bibles). Future operational cycles inherit convention.
**Methodology amendment candidate:** BIBLE_STRUCTURE_SPEC v6 → v7 amendment formalizing `docs/operations/` substructure (subdirs: runbooks/, cycle_logs/, audit_snapshots/, suspension_notes/).

### 5.3 Substrate-health entry gate — methodology gap
**Source:** S1 surfaced 7-day pre-existing blackout that Phase A scope would have caught had it been collected at cycle entry rather than D1 drafting
**Observation:** Operational reliability cycles need a substrate-health entry gate before scope ratification. If a scoping CC had collected signals (a) on all 6 sources as a Phase A entry-gate deliverable, the 7-day blackout would have surfaced before authoring the handoff. Phase A handoff anchored on Bug #28 because that's what Tony brought into the cycle; § 12.5 first-reference verification did not include substrate-health verification at scope-ratification time.
**Methodology amendment candidate:** operational cycle entry sequence amendment — substrate-health verification CC deliverable (D0) precedes structural Q ratification.

### 5.4 Sub-agent dispatch model — first instantiation
**Source:** Tony's Option 2 dispatch decision; QB raised concern about orchestrator-leak channel
**Observation:** Phase A dispatched via single CC orchestrator + isolated sub-agents rather than cohort-precedent fresh-conversation-per-session. Adversarial independence held at sub-agent boundary; methodology-compatibility of orchestrator framing channel is unverified at suspension time. S1's substantive findings being high-quality does not retroactively legitimize the dispatch model — quality of S1 work is uncorrelated with whether orchestrator briefing of S2 (had it dispatched) would have leaked context. Compounding novelty: Phase A is also first-instantiation of operational cycle class (5.1) and first-instantiation of operational artifacts directory (5.2); three structural novelties in one cycle.
**Methodology amendment candidate:** explicit ratification or rejection of sub-agent dispatch model with verification protocol (e.g., orchestrator must paste audit spec + drafting artifact verbatim with no framing additions; verification artifact = orchestrator's exact briefing prompt logged for QB inspection).

### 5.5 Non-DB write-surface enumeration in CC briefs — methodology gap
**Source:** S3 question / NYRA dry-run signal (c) wrote 2 small JSON files to S3 outside brief constraints
**Observation:** Operational-cycle CC briefs need explicit non-DB write-surface enumeration. Phase A brief covered DB writes only; NYRA dry-run surfaced S3 as omitted surface. Same gap likely covers SQS, SNS, Lambda invocations, file system writes outside artifact paths.
**Methodology amendment candidate:** brief-template amendment — write-surface enumeration table covering DB / S3 / SQS / SNS / Lambda invoke / EventBridge put / file system / external HTTP.

### 5.6 Spec-authorship gap — methodology integrity finding
**Source:** S1 worked from a brief whose DB-access pattern was substrate-stale (referenced `equine-ingestion` `raw_query` action which had been INACTIVE since 2026-05-02); brief was authored outside QB tier
**Observation:** SW1 spec for S1 was authored without QB-tier substrate verification at first reference per § 12.5. Brief's stale assumption forced S1 to work around the gap via indirect API paths — work that would have been unnecessary if the spec had verified DB-access path liveness at authorship time. CC-tier or self-derived spec authorship absorbs work that is QB-tier per cohort precedent. § 7.9 honesty discipline at CC-tier caught the gap, but pattern-level remedy requires preserving QB-tier spec-authorship monopoly.
**Methodology amendment candidate:** explicit rule prohibiting CC-tier or non-QB spec authorship; QB-tier substrate verification at first reference enforced for all CC dispatch specs; verification artifact = QB session's read-tool calls demonstrating substrate verification before spec authorship.

---

## 6. Phase A-prime entry handoff

Phase A-prime is a new operational reliability cycle (proposed; Tony ratifies at cycle entry). Distinct cycle ID, distinct handoff, distinct scope ratification. Suspension note serves as substrate input; D1 snapshot serves as diagnostic substrate.

### 6.1 Phase A-prime scope (proposed; Tony ratifies)
Restore `equine-ingestion` Lambda to functional state such that Phase A resume gate § 3 above is met. Inclusive of: ECR image rebuild, Lambda re-deploy, schema-drift remediation per S1 § 4.2 / § 6.4 candidate 5.3.N+2, NYRA cron timing fix per § 6.4 candidate 5.3.N+1, undocumented HRN workouts producer identification per § 6.4 candidate 5.3.N+3 + § 4.4 CloudTrail clue. NOT inclusive of: Bug #28 fix (Phase A D2 work; gated behind Phase A-prime exit), backfill execution (Phase A D3 work).

### 6.2 Phase A-prime structural questions (proposed at cycle entry)
1. Cycle frame: Phase A-prime as new operational reliability cycle vs in-place hot-fix sub-cycle vs Phase 5 entry execution batch
2. Authorization scope for AWS infrastructure work: Lambda config inspection, ECR image history, CloudWatch logs across all Lambda log groups, IAM role audit, EventBridge rule inspection, ECS service inventory — substantially broader than Phase A's SELECT-only DB + ingestion code scope
3. Deploy mechanism for Lambda re-activation: SAM rebuild + redeploy vs CDK redeploy vs manual ECR push
4. Schema-drift remediation scope: surgical SQL fixes in deployed image vs broader migration reconciliation
5. NYRA cron timing fix scope: cron retiming (EventBridge rule edit) vs handler default-date logic change vs both
6. HRN workouts producer identification scope: investigative CC session with CloudTrail + IAM + EventBridge read access
7. Phase A-prime exit criteria: minimum viable resume gate § 3 above vs broader operational health checklist
8. Phase A-prime tier structure: full four-tier ceremony for Lambda redeploy vs lighter tiers given operational nature

### 6.3 GM session involvement (architectural sanity check above QB-tier)
Phase A-prime architectural decisions (deploy mechanism, schema-drift remediation scope) warrant GM session weigh-in before QB ratification per established Tony / GM / QB / CC operating model. Phase A did not pull GM in; Phase A-prime should at structural Q surface time.

### 6.4 Sub-agent dispatch model decision pending
Phase A-prime should NOT inherit Option 2 dispatch model by default. Either (a) Tony explicitly ratifies sub-agent dispatch as operational cycle pattern, in which case banking observation 5.4 promotes from in-flight to ratified; or (b) Phase A-prime reverts to fresh-conversation-per-session cohort precedent, in which case 5.4 stays in-flight pending separate methodology amendment. Decision at Phase A-prime cycle entry.

---

## 7. Open methodology questions deferred to Phase A resumption / cycle close-out

1. Q9 close-out path resolution: `docs/bible/_meta/cycle_logs/` existence verification still pending. Suspension note recommends `docs/operations/cycle_logs/` per Q9 fallback path; final resolution at Phase A close-out.
2. Banking observation 5.1–5.6 ratification or rejection at Phase A close-out.
3. Methodology amendment proposals from ratified banking observations: drafted at Phase A close-out, ratified at separate methodology cycle.
4. Whether Phase A-prime itself surfaces additional banking observations to fold into Phase A close-out or stand as independent Phase A-prime close-out.

---

**End of Phase A Suspension Note — 2026-05-09.**
