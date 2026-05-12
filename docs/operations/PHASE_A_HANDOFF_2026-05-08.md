# Phase A Handoff — Data Acquisition Reliability Cycle

**Cycle ID:** PHASE_A_2026-05-08
**Cycle Class:** Operational Reliability Cycle (first instantiation)
**Status:** RATIFIED — CC dispatch authorized
**Methodology:** AUDIT_METHODOLOGY v3 (locked 2026-05-08)
**Owner:** Tony
**QB Session:** 2026-05-08
**Banking observation candidates flagged:** 2 (see § 9)

---

## 1. Inheritance State (substrate-verified at first reference per § 12.5)

### 1.1 Phase 1 lock state
All 7 Phase 1 deliverables LOCKED:
- Architecture Overview v3-patched-a
- Database & Schema v1-patched-d2
- Data Pipeline v1-patched-c
- Feature Provenance v1-patched-a-extended
- ML Layer Architecture v1
- Model Evaluation & Retraining v1
- API & Frontend v1

### 1.2 Methodology + structural lock state
- AUDIT_METHODOLOGY v3 LOCKED 2026-05-08
- META_PLAN v9 + BIBLE_STRUCTURE_SPEC v6 LOCKED 2026-05-05
- Cross-bible cross-reference freeze ACTIVE
- CONVERGENCE_CRITERIA v2 + TRIAGE_QUEUE_SPEC v1 in DRAFT pre-audit (per § 9 transparency note)

### 1.3 Backlog state
PHASE_5_BACKLOG.md at `/home/strakajagr/projects/equine-equalizer/docs/bible/PHASE_5_BACKLOG.md`
- 27 entries (5.3.1 through 5.3.27)
- Vocabulary-uniform per § 8.4 ratified strategy (c.2)

---

## 2. Phase A Scope

**Stated goal (Tony):** Data acquisition reliability across all 6 sources documented in Data Pipeline Bible v1-patched-c § 4.2. Every source ingests every day. Nothing missed. Manual scripts acceptable where automation isn't viable.

**Six sources (per Data Pipeline Bible § 4.2):**
1. HRN entries
2. HRN results
3. HRN workouts
4. NYRA workouts
5. Equibase chart parser
6. equibase_probe

**Phase A precedence rationale:** Bug #28 corrupts EV labels used for ML training. Phase B (ML layer analysis) gated behind Phase A because ML analysis against corrupted substrate is unfocused. Substrate integrity first; analysis second.

---

## 3. Ratified Resolutions (Q1–Q9)

### 3.1 Q1 — Hybrid asymmetric tier structure
- **Bug #28 fix:** full four-tier ceremony (drafting CC + adversarial audit CC + patch CC if surfaced + lock)
- **Source enumeration + backfill script + runbook:** lighter two-tier (drafting CC + audit CC) with conditional patch tier escalation if audit surfaces blocking findings
- **Principle:** § 4.21 discipline-scaling — tier weight tracks blast radius

### 3.2 Q2 — Operational reliability cycle as new methodology class
- Phase A consumes and closes Phase 5 entries; Phase 5 remains the inventory
- New defects surfaced during Phase A enter Phase 5 with § 8.4-uniform vocabulary + severity tags
- Bibles preserved as architectural reference; operational cycles get explicit closure mechanism

### 3.3 Q3 — Substrate authorization with SELECT-only DB refinement
**Drafting/working CCs read scope:**
- All 7 locked Phase 1 bibles (Data Pipeline primary)
- `backend/services/data_sources/` + adjacent ingestion modules
- Production DB **SELECT-only** for empirical verification (last-ingest timestamps, daily row counts, gap detection)
- Log directory (CC discovers path)

**Drafting/working CCs write scope:**
- Deliverable artifact paths only (per § 7 below)

**Code modification gating:**
- `hrn_scraper.py` modifications: dedicated Bug #28 fix CC session ONLY
- Backfill script CC session: writes script only; does NOT execute against production DB
- Tony executes backfill manually post-audit
- No CC session modifies production DB structure (no INSERT/UPDATE/DELETE/schema-changes)

### 3.4 Q4 — Three-signal triangulation per source
For each of 6 sources, drafting CC collects:
- **(a)** DB query: last successful ingest timestamp + daily row counts for trailing 14 days
- **(b)** Trailing 7 days of scraper logs scanned for error patterns + success markers
- **(c)** Dry-run / test invocation against today's data with output structure comparison

**HRN-specific:** Signal (c) tests against Bug #28 cases — doubles as Bug #28 fix verification (signal (c) sequencing therefore depends on fix landing first; see § 5 sequencing).

**Honest disposition (§ 7.9 applied operationally):** Per-source signal coverage recorded in source status snapshot. Source with only (a) is in worse epistemic standing than source with all three. Runbook records remaining epistemic gaps.

### 3.5 Q5 — Surgical fix + git-blame-driven backfill scope
- **Fix scope:** surgical line-level at substrate-verified line numbers. Fix CC RE-CONFIRMS current line numbers before patch authorship — close-out summary inheritance "lines 802–804 + 814" SUBJECT TO SUBSTRATE DRIFT
- **Refactor OUT of scope.** Adjacent issues encountered file as new Phase 5 entries; not acted on in Phase A
- **Backfill scope:** determined by `git blame` on affected lines for true defect-introduction date — substrate verification SUPERSEDES inherited "since 2026-04-30" claim
- **Backfill script audit verifies:** idempotency + dry-run output + downstream EV-label update logic
- **Execution:** Tony manual post-audit

### 3.6 Q6 — `docs/operations/` directory established
- Sibling to `docs/bible/`
- Daily runbook: `docs/operations/DAILY_INGESTION_RUNBOOK.md`
- Source status snapshot: `docs/operations/SOURCE_STATUS_AUDIT_2026-05-08.md` (point-in-time, dated)

### 3.7 Q7 — PHASE_5_BACKLOG cleanup with individual ratification
- Drafting CC substrate-verifies all 27 entries
- Drafting CC identifies Phase A scope subset; proposes closures with closing-evidence references
- **Tony ratifies closures individually; QB does NOT unilaterally close**
- **Closing-evidence format:** Phase A artifact reference + date + verification artifact reference
  - Example: `closed-by: docs/operations/SOURCE_STATUS_AUDIT_2026-05-08.md § 4.2 (HRN payout extraction verified post-fix); fix-commit: <SHA>; verified: 2026-05-DD`
- New entries surfaced during Phase A appended with § 8.4-uniform vocabulary + severity tags

### 3.8 Q8 + Q9 — Output paths
| Artifact | Path |
|---|---|
| Source status snapshot | `docs/operations/SOURCE_STATUS_AUDIT_2026-05-08.md` |
| Bug #28 fix | in-place: `backend/services/data_sources/hrn_scraper.py` + tests at existing test path (CC discovers) |
| Backfill script | `scripts/backfill/bug_28_payout_backfill.py` |
| Daily ingestion runbook | `docs/operations/DAILY_INGESTION_RUNBOOK.md` |
| PHASE_5_BACKLOG updates | in-place: `/home/strakajagr/projects/equine-equalizer/docs/bible/PHASE_5_BACKLOG.md` |
| Cycle close-out | per Q9 decision tree below |

**Q9 close-out location decision tree:**
1. CC checks `docs/bible/_meta/` for existing `cycle_logs/` convention via `list_directory`
2. **If `cycle_logs/` exists in `_meta/`:** use `docs/bible/_meta/cycle_logs/PHASE_A_2026-05-08_CLOSE_OUT.md` (cohort precedent honored)
3. **If absent:** use `docs/operations/cycle_logs/PHASE_A_2026-05-08_CLOSE_OUT.md` (consistent with Q6 docs/operations/ scope; establishes operational close-out convention)

---

## 4. Deliverable Enumeration with Tier Assignments

| # | Deliverable | Tier | CC Sessions Required |
|---|---|---|---|
| D1 | Source status snapshot (6 sources × 3 signals) | 2-tier (conditional 3rd) | drafting + audit |
| D2 | Bug #28 surgical fix + tests | 4-tier full | drafting + audit + patch (if surfaced) + lock |
| D3 | Bug #28 backfill script | 2-tier (conditional 3rd) | drafting + audit |
| D4 | Daily ingestion runbook | 2-tier (conditional 3rd) | drafting + audit |
| D5 | PHASE_5_BACKLOG cleanup proposals | 2-tier (conditional 3rd) | drafting + audit |
| D6 | Cycle close-out summary | QB-authored chat output → Tony saves | n/a (QB tier) |

---

## 5. CC Session Sequencing (dependency-ordered)

**Sequence rationale:** dependencies driven by (a) substrate evidence flow — source enumeration DB queries inform Bug #28 backfill scope independent of git blame; (b) Signal (c) for HRN requires Bug #28 fix to have landed before verification can complete; (c) runbook synthesis requires source enumeration to be complete.

S1: D1 drafting CC (source enumeration; signals (a) + (b) for all 6 sources;
signal (c) for non-HRN sources; signal (c) for HRN DEFERRED)
↓
S2: D1 audit CC
↓
[Tony ratifies D1; closures proposed feed into S6/S7 inputs]
↓
S3: D2 drafting CC (Bug #28 surgical fix; substrate-verifies line numbers;
git blame for defect-introduction date; tests authored)
↓
S4: D2 audit CC (adversarial)
↓
[Patch tier if surfaced]
↓
[Tony ratifies + lands fix; signal (c) for HRN now executable]
↓
S5: D3 drafting CC (backfill script; informed by D1 signal (a) DB evidence
+ D2 git blame defect-introduction date)
↓
S6: D3 audit CC (idempotency + dry-run + EV-label update logic verified)
↓
[Tony ratifies; executes backfill manually]
↓
S7: D1 signal (c) HRN re-execution (verifies fix landed; appends to D1)
↓
S8: D4 drafting CC (runbook; informed by all of above)
↓
S9: D4 audit CC
↓
S10: D5 drafting CC (PHASE_5_BACKLOG cleanup; substrate-verifies all 27;
proposes closures with closing-evidence references)
↓
S11: D5 audit CC
↓
[Tony ratifies closures individually]
↓
S12: QB authors close-out summary (banking observations + D6)

**Critical sequencing constraint:** S3 → S4 → fix-lands MUST complete before S7 (signal (c) HRN) can execute. Signal (c) failure on HRN before S3 is expected and not a bug; signal (c) failure on HRN after fix-lands is a bug-#28-fix regression and triggers S4 patch tier escalation retroactively.

---

## 6. Substrate Verification Requirements

Per § 12.5 Self-Audit Check 5 / Check 14 generalization, each CC session re-verifies substrate facts at first reference rather than inheriting from this handoff. Specific re-verification requirements:

| Substrate fact | Verifying CC | Inherited claim subject to drift |
|---|---|---|
| `hrn_scraper.py` line numbers for fix | S3 (D2 drafting) | "lines 802–804 + 814" (Tony explicit Q5 ratification) |
| Bug #28 defect-introduction date | S3 (D2 drafting via git blame) | "since 2026-04-30" (close-out summary inheritance) |
| PHASE_5_BACKLOG entry count | S10 (D5 drafting) | "27 entries (5.3.1 through 5.3.27)" |
| Data Pipeline Bible § 4.2 source list | S1 (D1 drafting) | "6 sources" (HRN entries/results/workouts, NYRA workouts, Equibase chart parser, equibase_probe) |
| `cycle_logs/` convention existence | S12 (QB pre-close-out via authorized read) | absent / present (Q9 decision tree input) |

---

## 7. Authorization Scope Matrix

| CC Session | Read scope | Write scope | DB scope |
|---|---|---|---|
| S1 (D1 drafting) | 7 Phase 1 bibles + ingestion code + logs | `docs/operations/SOURCE_STATUS_AUDIT_2026-05-08.md` | SELECT-only |
| S2 (D1 audit) | same as S1 + S1 output | audit findings only (chat output back to QB) | SELECT-only |
| S3 (D2 drafting) | Data Pipeline Bible + `hrn_scraper.py` + adjacent + git history | `hrn_scraper.py` + tests at existing test path | SELECT-only (verification queries) |
| S4 (D2 audit) | same as S3 + S3 diff | audit findings only | SELECT-only |
| S5 (D3 drafting) | Data Pipeline Bible + DB schema + S3 fix + S1 evidence | `scripts/backfill/bug_28_payout_backfill.py` | SELECT-only (no execution) |
| S6 (D3 audit) | same as S5 + S5 output | audit findings only | SELECT-only |
| S8 (D4 drafting) | All Phase A artifacts to date | `docs/operations/DAILY_INGESTION_RUNBOOK.md` | none |
| S9 (D4 audit) | same as S8 + S8 output | audit findings only | none |
| S10 (D5 drafting) | PHASE_5_BACKLOG + all Phase A artifacts | `PHASE_5_BACKLOG.md` (proposed updates only — Tony ratifies) | none |
| S11 (D5 audit) | same as S10 + S10 diff | audit findings only | none |

**No CC session has write access to:**
- Production DB structure (no DDL, no DML)
- Other Phase 1 bibles
- META_PLAN, BIBLE_STRUCTURE_SPEC, AUDIT_METHODOLOGY
- CONVERGENCE_CRITERIA, TRIAGE_QUEUE_SPEC

---

## 8. Closing-Evidence Format (per Q7 ratification)

When drafting CC proposes a PHASE_5_BACKLOG entry closure during S10, format:

closed-by: <Phase A artifact path> § <section>
verification: <verification artifact path or SHA>
date: 2026-05-DD
ratified-by: Tony, 2026-05-DD

Example for Bug #28 / 5.3.1 closure:

closed-by: docs/operations/SOURCE_STATUS_AUDIT_2026-05-08.md § 4.2
(HRN payout extraction verified post-fix via signal (c))
verification: backend/services/data_sources/hrn_scraper.py @ <fix-SHA>
+ scripts/backfill/bug_28_payout_backfill.py @ <SHA>
date: 2026-05-DD
ratified-by: Tony, 2026-05-DD

QB does NOT pre-fill ratified-by; Tony pre-fills upon individual closure ratification.

---

## 9. Banking Observation Candidates (deferred to cycle close-out)

1. **Operational reliability cycle pattern — first instantiation.** Phase A establishes precedent for operational cycle class as distinct from Phase 1 architectural-documentation cohort. Pattern characteristics: hybrid asymmetric tier structure, three-signal triangulation, source code modification gating to dedicated CC sessions, SELECT-only DB scope as default.

2. **Operational artifacts directory convention — first-of-class precedent.** `docs/operations/` established sibling to `docs/bible/`. Distinguishes operational reference (runbooks, status snapshots, cycle logs) from architectural reference (bibles). Future operational cycles inherit convention.

Banking discipline: candidates surfaced here at cycle entry; ratification deferred to S12 cycle close-out per AUDIT_METHODOLOGY v3 banking observation lifecycle.

---

## 10. Cycle Exit Criteria

Phase A cycle CLOSES when:
- D1 source status snapshot LOCKED (Tony ratification)
- D2 Bug #28 fix LANDED (Tony ratification + commit)
- D3 backfill script LANDED + EXECUTED (Tony manual execution)
- D4 daily ingestion runbook LOCKED (Tony ratification)
- D5 PHASE_5_BACKLOG closures RATIFIED individually (Tony per-entry ratification)
- D6 close-out summary AUTHORED + SAVED (per Q9 decision tree path)
- Banking observations RATIFIED or REJECTED (Tony decision)

Phase A enables Phase B (ML Layer Analysis) entry only after exit criteria met.
