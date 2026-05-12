# Operational Catastrophe Recovery Cycle — Handoff

**Cycle ID:** OCRC_2026-05-09
**Cycle Class:** Operational Catastrophe Recovery Cycle (first instantiation)
**Status:** RATIFIED — CC dispatch authorized
**Methodology:** AUDIT_METHODOLOGY v3 (locked 2026-05-08)
**Owner:** Tony
**QB Session:** 2026-05-09
**Prior Cycle:** PHASE_A_2026-05-08 (HALTED per P-Q1 ratification 2026-05-09)
**Banking observation candidates flagged:** 7 cumulative this session + 8 cohort-handoff = 15 queued for AUDIT_METHODOLOGY v4 meta-cycle

[NOTE TO SPEC-WRITE CC: the line above contains a known reconciliation gap per Tony
surface note 1 — "7 cumulative this session + 8 cohort-handoff = 15" supersedes-by
later § 9 enumeration "11 this session + 8 cohort = 19". Save VERBATIM as authored;
reconciliation is D8 close-out work, not spec-write CC tier work. Do NOT correct.]

---

## 1. Cycle Class Establishment

OCRC is the second new methodology cycle class established this session. Phase A
established Operational Reliability Cycle (banking candidate 1, CANDIDATE-this-session,
first instantiation suspended). OCRC establishes Operational Catastrophe Recovery Cycle
(banking candidate 2, CANDIDATE-this-session, first instantiation entering).

Cycle class distinction: Operational Reliability Cycle assumes substrate is functional
and audits per-source ingestion reliability. Operational Catastrophe Recovery Cycle
assumes substrate is non-functional or partially non-functional and executes
substrate-discovery + restoration to operational baseline. The distinction matters
because tier scaling, authorization scope, and entry gate differ.

OCRC's existence is itself diagnostic of methodology gap: had operational health
monitoring existed as first-class methodology infrastructure, OCRC may not have been
necessary. Banking candidate 5 (§ 4.X new sub-section: QB-tier prophylactic checks
triggered by 'novel scope detected' classifier) is adjacent to but distinct from
operational health monitoring as methodology infrastructure. Both queue for v4
meta-cycle.

---

## 2. Inheritance State (substrate-verified at first reference per § 12.5)

### 2.1 Phase A halted state

PHASE_A_2026-05-08 halted per P-Q1 ratification 2026-05-09. Phase A artifacts preserved:

| Artifact | Path | State (tier-status tag) |
|---|---|---|
| Phase A handoff | `docs/operations/PHASE_A_HANDOFF_2026-05-08.md` | SAVED — VERIFIED-this-session |
| Phase A suspension note | `docs/operations/PHASE_A_SUSPENSION_NOTE_2026-05-09.md` | SAVED — VERIFIED-this-session |
| Phase A D1 snapshot | `docs/operations/SOURCE_STATUS_AUDIT_2026-05-08.md` | FROZEN — VERIFIED-this-session |
| Phase A D2-D6 | n/a | NEVER DISPATCHED |

Phase A re-dispatch deferred until OCRC exits at operational baseline per OCRC exit gate
§ 8 below.

### 2.2 Cohort lock state

| Item | State (tier-status tag) |
|---|---|
| 7 Phase 1 bibles | LOCKED — INHERITED-not-verified-this-session |
| AUDIT_METHODOLOGY v3 | LOCKED 2026-05-08 — INHERITED-not-verified-this-session |
| META_PLAN v9 + BIBLE_STRUCTURE_SPEC v6 | LOCKED 2026-05-05 — INHERITED-not-verified-this-session |
| Cross-bible cross-reference freeze | ACTIVE — INHERITED-not-verified-this-session |
| CONVERGENCE_CRITERIA v2 + TRIAGE_QUEUE_SPEC v1 | DRAFT pre-audit — INHERITED-not-verified-this-session |

OCRC inventory pass first dispatch substrate-verifies items in 2.1 and 2.2 at first
authorized read per OCR-Q8.

### 2.3 Backlog state

PHASE_5_BACKLOG.md at `/home/strakajagr/projects/equine-equalizer/docs/bible/PHASE_5_BACKLOG.md`
- 27 entries (5.3.1 through 5.3.27) — INHERITED-not-verified-this-session per § 12.5;
  subject to drift if entries added/closed since prior cycle close-out
- Vocabulary-uniform per § 8.4 ratified strategy (c.2) — INHERITED-not-verified-this-session

### 2.4 Production substrate state

| Resource | State (tier-status tag) |
|---|---|
| equine-ingestion Lambda | Active 2026-05-09 ~04:37 UTC — VERIFIED-this-session via CC restoration Step 4 report; subject to drift since last verification |
| equine-results Lambda | INACTIVE — VERIFIED-this-session via CC Step 4 report; ECR image restored as CDK side-effect; awaits update-function-code |
| equine-feature-engineering Lambda | INACTIVE — VERIFIED-this-session via CC Step 4 report; ECR image restored as CDK side-effect; awaits update-function-code |
| 5 Active Lambdas (equine-nyra-workouts, equine-pl-inference, equine-wr-inference, equine-ls-inference, equine-inference) | Active — INHERITED-from-Phase-A-D1 § 1.3; not re-verified at OCRC entry |
| 3 DISABLED EventBridge rules (equine-feature-engineering-daily, equine-inference-daily, equine-weekly-retrain-pl) | DISABLED — INHERITED-from-Phase-A-D1 § 1.3; disposition unknown |
| equine-fetch-results-nightly EventBridge rule | Input=null routes to fetch_daily_entries(today) instead of fetch_results(yesterday) — VERIFIED-this-session via CC Step 4 report new defect surface |

OCRC inventory pass first dispatch substrate-verifies all production state at first
authorized read.

---

## 3. OCRC Scope (per OCR-Q1 ratification)

**OCRC scope = substrate-discovery + restoration to operational baseline.**

### 3.1 In-scope deliverables

D1. **Resource enumeration pass** — 4-source triangulation (AWS API + CloudFormation +
CDK source + repo) with classification taxonomy per OCR-Q4. Includes HRN workouts
producer hunt per P-Q5 ratification.

D2. **Cron-payload audit** — full enumeration of equine-* EventBridge rules + Input
field + handler routing + source-publish-time vs cron-fire-time analysis. Sequenced
after D1 per OCR-Q4 ratification (audits known-complete EventBridge rule list rather
than substrate-discovered subset).

D3. **Schema-drift verification across Active Lambdas** — verify SQL-vs-live-schema
alignment for the 5 Lambdas not exercised during equine-ingestion restoration. May
escalate to four-tier ceremony per OCR-Q2 if latent corruption surfaces requiring SQL
fixes.

D4. **Restoration of `equine-results` + `equine-feature-engineering`** — three-tier
ceremony per OCR-Q2 (drafting + audit + lock). ECR images already restored as CDK
side-effect 2026-05-09; restoration deliverable is update-function-code + post-Active
verification + cron-firing observation.

D5. **NYRA cron timing fix** — three-tier ceremony per OCR-Q2 (drafting + audit + lock),
patch tier escalation if timing-fix proposal surfaces handler-side complications.
Surgical fix scope: cron retiming (EventBridge rule edit) OR handler default-date logic
change OR both.

D6. **CloudWatch logging gap remediation** — investigate why application-level
logger.info() output didn't surface during equine-ingestion 70.77s default-case invocation
post-restoration (CC Step 4 report finding 3). Likely logging.basicConfig() not configured
at module level. Surgical fix if simple; defer if requires substantial refactor.

D7. **OCRC closure proposals for existing PHASE_5_BACKLOG entries** — drafting CC work
per P-Q3 + OCR-Q7. Tony ratifies closures individually with closing-evidence format.
Candidate closures: 5.3.20 (equine-ingestion broken container — restoration evidence
exists), possibly 5.3.17 (3 INACTIVE Lambdas — pending D4 restoration completion),
possibly 5.3.18 (Secrets Manager orphans — pending D1 inventory pass disposition).

D8. **OCRC close-out summary** — banking observation candidate ratification + cycle
exit verification + Phase A re-dispatch entry handoff. QB-authored chat output per
Pattern A bundling.

### 3.2 Out-of-scope (deferred to specified cycle)

| Out-of-scope item | Deferred to |
|---|---|
| Bug #28 fix + backfill | Phase A re-dispatch post-OCRC exit |
| 7-day data gap backfill (2026-05-02 → 2026-05-08) | Phase A re-dispatch post-OCRC exit |
| Bible amendments (NYRA disposition correction § 4.1.4 / § 4.2.4 + others surfaced) | Separate upstream-correction cycle post-OCRC + post-Phase-A |
| RDS Data API enablement | Methodology infrastructure cycle |
| Race-count delta deep investigation | Phase A re-dispatch unless D1 surfaces resolution incidentally |
| 3 DISABLED EventBridge rules disposition | Resource inventory disposition decision: documented in D1 with proposed disposition; execution deferred to dedicated cycle if disposition is anything other than "leave as-is" |
| ECS task family operational state | D1 inventory documents state; operational changes deferred to dedicated cycle if needed |
| Bug #28 priority comparison (P-Q6) | Deferred until inventory + cron-audit + producer hunt complete + ML Layer Architecture / Feature Provenance / Model Evaluation & Retraining substrate review |

---

## 4. Tier Structure (per OCR-Q2 ratification)

| Deliverable | Tier | CC Sessions Required |
|---|---|---|
| D1 Resource enumeration pass | 2-tier (conditional 3rd) | drafting + audit |
| D2 Cron-payload audit | 2-tier (conditional 3rd) | drafting + audit |
| D3 Schema-drift verification | 2-tier escalating to 4-tier if SQL fixes surface | drafting + audit (+ patch + lock if escalated) |
| D4 Restoration `equine-results` + `equine-feature-engineering` | 3-tier | drafting + audit + lock |
| D5 NYRA cron timing fix | 3-tier (conditional 4th) | drafting + audit + lock (+ patch if escalated) |
| D6 CloudWatch logging gap | 2-tier (conditional 3rd) | drafting + audit |
| D7 PHASE_5_BACKLOG closure proposals | 2-tier | drafting (per session per closure proposal) + audit |
| D8 OCRC close-out summary | QB-authored chat output | n/a (QB tier) |

Hybrid asymmetric per § 4.21 discipline-scaling.

---

## 5. Substrate Authorization Scope (per OCR-Q3 ratification)

### 5.1 Read access (all CC sessions)

- All 7 locked Phase 1 bibles
- META_PLAN v9 + BIBLE_STRUCTURE_SPEC v6 + AUDIT_METHODOLOGY v3
- PHASE_5_BACKLOG.md
- All Phase A artifacts (handoff, suspension note, D1 snapshot)
- Full EE repository read access
- AWS Lambda config (`get-function`, `list-versions`, `get-function-configuration`)
- ECR (read; image history, manifest inspection)
- CDK source (`infrastructure/cdk/`)
- CloudFormation (`list-stack-resources`, `describe-stacks`, `describe-stack-events`)
- CloudWatch logs (all equine-* log groups)
- IAM (read; role configuration, policy inspection, role-session activity)
- EventBridge (read; `list-rules`, `list-targets-by-rule`, `describe-rule`)
- RDS via equine-ingestion raw_query path SELECT-only
- S3 (read; listings, object metadata, content read for verification)
- CloudTrail (read; for producer hunt + role-session investigation)
- ECS (read; task family inventory, task definition inspection, service state)
- Secrets Manager (read; entry inventory + consumer count via IAM policy analysis)

### 5.2 Write access scoped per deliverable per dedicated CC session

Each write scope requires Tony explicit authorization at CC dispatch time as separate
ratification surface (per OCR-Q3 ratification refinement).

| Write scope | Authorized in deliverable | Restriction |
|---|---|---|
| Lambda update-function-code on `equine-results` | D4 restoration drafting CC | Single named Lambda only |
| Lambda update-function-code on `equine-feature-engineering` | D4 restoration drafting CC | Single named Lambda only |
| EventBridge rule modification (NYRA cron timing) | D5 NYRA cron timing fix CC | Single named rule only |
| Source code modification (handler default-date logic if D5 escalates) | D5 NYRA cron timing fix CC | Single named handler only |
| CDK deploy (if D3 escalates to SQL fixes) | D3 schema-drift patch CC | Per-Lambda or per-stack scope as escalation specifies |
| CloudWatch logging configuration (D6) | D6 CC | Source code only; no infrastructure changes |
| Deliverable artifact paths in `docs/operations/` | All drafting CCs | Per-deliverable path only |
| PHASE_5_BACKLOG.md proposed updates | D7 drafting CC | Proposed-only; Tony ratifies before write commits |

### 5.3 Explicitly prohibited (no CC session)

- DB DDL (CREATE / ALTER / DROP / etc.)
- DB DML (INSERT / UPDATE / DELETE)
- RDS Data API enablement (`modify-db-cluster --enable-http-endpoint`)
- Modifying Phase 1 bibles
- Modifying META_PLAN, BIBLE_STRUCTURE_SPEC, AUDIT_METHODOLOGY
- Modifying CONVERGENCE_CRITERIA, TRIAGE_QUEUE_SPEC
- Bug #28 fix in `hrn_scraper.py` (Phase A re-dispatch territory)
- Backfill execution (Phase A re-dispatch territory)
- Creating new IAM roles or policies
- Creating new AWS resources (Lambdas, EventBridge rules, S3 buckets, etc.) outside
  named restoration scope

---

## 6. CC Session Sequencing

Dependency-ordered. Sub-agent dispatch model REVERTED to fresh-conversation-per-session
per OCR-Q5 ratification.
S1: D1 drafting CC (resource enumeration pass with 4-source triangulation;
HRN workouts producer hunt embedded; substrate-verifies all inheritance
state per OCR-Q8)
↓
S2: D1 audit CC (adversarial re-enumeration + classification spot-check)
↓
[Tony ratifies D1; closure proposals for existing entries flow to D7 input]
↓
S3: D2 drafting CC (cron-payload audit; informed by D1 EventBridge rule list)
↓
S4: D2 audit CC
↓
[Tony ratifies D2]
↓
S5: D3 drafting CC (schema-drift verification across 5 Active Lambdas;
raw_query path now Active per equine-ingestion restoration)
↓
S6: D3 audit CC
↓
[Tony ratifies D3; patch tier escalation if SQL fixes surface]
↓
S7: D4 drafting CC (restoration of equine-results + equine-feature-engineering;
update-function-code + post-Active verification + cron-firing observation)
↓
S8: D4 audit CC
↓
S9: D4 lock CC (or QB ratification of audit findings as lock)
↓
[Tony ratifies + restoration lands]
↓
S10: D5 drafting CC (NYRA cron timing fix; informed by D2 cron-payload audit findings)
↓
S11: D5 audit CC
↓
S12: D5 lock CC (or QB ratification)
↓
[Tony ratifies + fix lands]
↓
S13: D6 drafting CC (CloudWatch logging gap)
↓
S14: D6 audit CC
↓
[Tony ratifies D6]
↓
S15: D7 drafting CC (closure proposals per identified candidates)
↓
S16: D7 audit CC
↓
[Tony ratifies closures individually]
↓
S17: QB authors D8 close-out summary (banking observation candidate ratification,
cycle exit verification, Phase A re-dispatch entry handoff)

Sequencing rationale: D1 establishes inventory baseline; D2 audits crons against known
EventBridge rule list; D3 verifies schema across Active Lambdas using restored
raw_query path; D4 restoration extends Active Lambda set; D5 fixes operational defect
in newly-Active resource (NYRA was Active throughout but operationally broken);
D6 addresses logging gap; D7 closes backlog entries with accumulated evidence;
D8 closes cycle.

---

## 7. Substrate Verification Requirements (per § 12.5)

Per banking candidate 4 tier-status tag discipline. Each CC session re-verifies
substrate facts at first reference rather than inheriting from this handoff. Critical
re-verification requirements:

| Substrate fact | Verifying CC | Inherited claim subject to drift |
|---|---|---|
| equine-ingestion Lambda Active | S1 | "Active 2026-05-09 ~04:37 UTC" — VERIFIED-this-session by prior CC; subject to drift |
| equine-results + equine-feature-engineering INACTIVE | S1 | VERIFIED-this-session by prior CC Step 4 report; subject to drift |
| 5 Active Lambdas state | S1 | INHERITED from Phase A D1 § 1.3; not re-verified this session |
| 3 DISABLED EventBridge rules | S1 | INHERITED from Phase A D1 § 1.3 |
| equine-fetch-results-nightly Input=null | S3 (D2 drafting) | VERIFIED-this-session by prior CC Step 4 |
| PHASE_5_BACKLOG 27-entry count | S15 (D7 drafting) | INHERITED-not-verified-this-session |
| 7 Phase 1 bibles locked + cohort lock state | S1 (incidentally during inheritance read) | INHERITED-not-verified-this-session |

---

## 8. OCRC Exit Gate (Operational Baseline Definition)

Per OCR-Q1 ratification. OCRC closes when ALL of:

1. D1 resource inventory LOCKED (Tony ratification)
2. D2 cron-payload audit LOCKED (Tony ratification)
3. D3 schema-drift verification LOCKED (Tony ratification); SQL fixes deployed if
   D3 escalated
4. D4 restoration LANDED — `equine-results` + `equine-feature-engineering` Active state
   verified + at least one cron firing observed writing to expected destination tables
   (or rationale documented if cron firing not observable within session window)
5. D5 NYRA cron timing fix LANDED — non-zero NYRA workouts captured for ≥3 consecutive
   days post-fix
6. D6 CloudWatch logging gap remediated OR explicitly deferred with rationale
7. D7 closure proposals for OCRC-eligible PHASE_5_BACKLOG entries RATIFIED individually
8. D8 close-out summary AUTHORED and SAVED
9. Banking observation candidates surfaced this cycle ENUMERATED in close-out (tier-status
   tag CANDIDATE-this-session); ratification deferred to v4 meta-cycle
10. All 8 equine-* Lambdas in expected state (Active or DISABLED-with-rationale-documented)
11. Every cron's Input ↔ handler routing verified
12. Every cron's timing verified against source-publish-time
13. Every documented S3 producer identified
14. Signal (a) DB evidence collectable via at least one ratified path

OCRC exit enables Phase A re-dispatch entry against verified-clean operational substrate.

---

## 9. Banking Observation Candidates (cumulative; tier-status tagged)

Per banking candidate 4 tier-status discipline. All current candidates are
CANDIDATE-this-session or CANDIDATE-prior-session; none RATIFIED. v4 meta-cycle is
the ratification venue.

### From Phase A entry + suspension + OCRC entry (this session)

1. Operational Reliability Cycle pattern — first instantiation (Phase A; CANDIDATE-this-session)
2. Operational Catastrophe Recovery Cycle pattern — first instantiation (OCRC; CANDIDATE-this-session)
3. QB-tier discipline degradation under catastrophe pressure — 4-pattern enumeration
   (Derby urgency inheritance / Pattern A bundling violation / closure as fait accompli /
   methodology amendment proposed unilaterally) (CANDIDATE-this-session)
4. QB-authored candidate vs ratified observation tier-status tag discipline
   (CANDIDATE-this-session)
5. § 4.X new sub-section: QB-tier prophylactic checks triggered by 'novel scope detected'
   classifier (CANDIDATE-this-session)
6. 'Novel scope detected' classifier as methodology infrastructure (CANDIDATE-this-session)
7. `docs/operations/` directory convention establishment (CANDIDATE-this-session)
8. Sub-agent dispatch model methodology-compatibility unverified — banking before
   normalized by use (CANDIDATE-this-session)
9. Substrate-health entry gate as methodology infrastructure (CANDIDATE-this-session;
   surfaced in Phase A suspension note; NOT ratified-cohort-inheritance per banking
   candidate 4 retroactive correction)
10. Non-DB write-surface enumeration in CC briefs — methodology gap (CANDIDATE-this-session)
11. Spec-authorship gap — QB-tier substrate verification at first reference enforced
    for all CC dispatch specs (CANDIDATE-this-session)

### From cohort handoff (prior session)

8 cohort-handoff banking observations from prior cycle — INHERITED-not-verified-this-session.
Carried forward to v4 meta-cycle queue.

### Methodology infrastructure adjacent (informational; not banking)

- Operational health monitoring as first-class methodology infrastructure (informational
  observation surfaced this session; not banked because adjacent to banking candidate 5
  rather than distinct)

---

## 10. Phase A Re-Dispatch Entry Handoff (deferred to OCRC exit)

OCRC D8 close-out summary authors Phase A re-dispatch entry handoff. Substrate inputs
at re-dispatch entry:
- OCRC inventory (D1)
- OCRC cron-payload audit (D2)
- OCRC schema-drift verification (D3)
- OCRC restoration log
- OCRC closure-ratification record
- Phase A original handoff + suspension note + D1 snapshot
- 7-day data gap window enumerated per inventory pass findings

Phase A re-dispatch may inherit Phase A original Q1-Q8 ratifications subject to
substrate drift verification, OR re-ratify if substrate has changed materially.
Decision at re-dispatch entry; not pre-decided here.

---

**End of OCRC Handoff — 2026-05-09.**
