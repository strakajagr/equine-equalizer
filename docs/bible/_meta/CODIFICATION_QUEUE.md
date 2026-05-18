# CODIFICATION_QUEUE

Substrate-banked codification candidates awaiting bible amendment. Single-instance candidates are substrate-thin per § 4.36 codification-gating; multi-instance accrual required before promotion.

## Promotion threshold

- **2 instances**: substrate-evidence-pending; surface for adjudication.
- **3 instances**: substrate-emphatic; codification authorized.
- **4+ instances**: substrate-emphatic; immediate codification authoring.

---

## Promoted-this-session

### § 4.32 Case Study 6 sub-pattern B Events #6-#9 — 4-instance multi-instance accrual

Pattern framing: **QB dispatch authoring decoupled from CC's verbatim substrate-evidence report at authoring time.** QB authors dispatch payload against speculated/inherited substrate-state instead of substrate-actual evidence already surfaced in prior CC report.

Multi-instance accrual (substrate-emphatic; 4 events this Tier 3 prerequisite arc):

**Event #6 — Step 2 dispatch Path A/B inherited as alternatives without substrate-coherence verification**
- Dispatch: BEL H3 backfill Phase 2 (cache invalidation)
- QB substrate-assumption: `.session_state.json` cache substrate
- CC substrate-actual: `download_log.txt` line-based cache; `.session_state.json` is Playwright cookies-only
- Halt-and-surface required before any Phase 2 mutation

**Event #7 — Step 3 dispatch assumed --days-back N substrate-equivalent to historical backfill without cache-mechanic verification**
- Dispatch: BEL H3 Step 3 (--days-back 20 expected to fetch historical)
- QB substrate-assumption: --days-back loop iterates dates fresh
- CC substrate-actual: `is_done()` check skips entries already in download_log.txt; stale NR entries from pre-BAQ-remap era cached "no_racing"
- Halt-and-surface led to Phase 2 cache-invalidation patch

**Event #8 — Phase 1 dispatch scaffolding contaminated with QB-speculated cache substrate**
- Dispatch: BEL H3 backfill Phase 1.2 (.session_state.json key schema)
- QB substrate-assumption: cache stored at `.session_state.json` with BEL-keyed entries
- CC substrate-actual: `.session_state.json` is Playwright {cookies, origins} only; cache is at `download_log.txt`
- Phase 1 gate fired correctly; halt-and-surface before Phase 2

**Event #9 — Phase 4 dispatch included substrate-discovery sub-phase asking CC to re-surface substrate already verbatim in Phase 1.4**
- Dispatch: BEL H3 Phase 4.1.1 — "verbatim sync invocation pattern from run_daily_refresh.sh"
- QB substrate-actual: pattern already surfaced verbatim in Phase 1.4 report (single-action invocation; window-payload schema; substrate-coherent)
- CC could substrate-pragmatic skip re-discovery; substrate-pragmatic decision to execute as substrate-coherence-double-check
- Substrate-pragmatic minor; documents that QB dispatch text re-asks substrate already in conversation

### Pattern remedy (substrate-prophylactic addition to § 4.32)

QB authoring discipline: at dispatch time, QB MUST verify CC's last verbatim substrate-evidence report matches dispatch's substrate-assumption set. If divergence detected → re-issue dispatch grounded against verbatim substrate. If no recent CC report → dispatch FIRST a substrate-discovery sub-phase before mutation phases.

Audit-CC check: at Phase 1 of any multi-phase dispatch, CC verifies dispatch's substrate-assumptions against current substrate-actual; HALT on divergence. (This is the pattern already encoded as sub-pattern B; the 4-event accrual validates the prophylactic.)

**Codification action**: bible amendment to § 4.32 Case Study 6 sub-pattern B in AUDIT_METHODOLOGY.md. Deferred to next codification cycle batch (Phase A close-out cadence per Tony substrate-pragmatic batching).

---

## Single-instance candidates (substrate-thin; awaiting multi-instance accrual)

### Item 5 — SQL UPSERT INSERT-vs-UPDATE asymmetry

**Pattern**: New column added to schema + repository INSERT column list + parser race-dict output, but `ON CONFLICT DO UPDATE SET` clause NOT updated. Existing rows route through UPDATE path → new column stays NULL. Pattern surfaces only when ROWS PRE-EXIST (e.g., entries-scraper creates rows before chart-parser writes them).

**Single instance**: equibase_race_id in chart_parser.py:insert_race (BEL H3 dispatch, commit 8df2eb8). Substrate-correct fix required adding `equibase_race_id = EXCLUDED.equibase_race_id` to DO UPDATE clause.

**Substrate-thin per § 4.36 codification-gating**. Bank for multi-instance accrual.

**Audit-CC prophylactic candidate**: at code-review time, any new column added to INSERT column list MUST be cross-referenced against DO UPDATE SET clause; HALT if absent.

---

## Track-banked candidates (Tier 3 full close-out dispatch 2026-05-18)

### Track B — entries-scraper is_scratched lag

**Substrate-evidence**: 95 BEL horses across 4/30-5/10 have `is_scratched=FALSE` in entries despite being scratched per chart-PDF "ScratchedHorse(s):" lines.

**Substrate-actual root cause**: chart_parser.py has ZERO ScratchedHorse extraction. Parser doesn't update `is_scratched` post-race. Entries-scraper is pre-race snapshot; vet scratches happen post-snapshot.

**Substrate-pragmatic remediation** (substantial parser extension scope; deferred):
1. Add ScratchedHorse(s) regex extraction to `parse_race_block`
2. Add `UPDATE entries SET is_scratched=TRUE WHERE race_id=... AND horse_id IN (...)` to insert_race or new function
3. Re-invoke parse_charts on backfill window

Banked pending separate Tier 3 dispatch.

### Track C — CDK silent-deploy substrate-bug in CC env

**Substrate-evidence**: `npx cdk deploy/synth EquineComputeStack` exits 0 in CC env with zero stdout/stderr, no asset rebuild. TTY-wrap via `script -qfc` produces spinner output only. Even `CI=false FORCE_COLOR=1` env override doesn't help.

**Hypothesis space (untested)**:
- ts-node compile fails silently
- CDK CLI v2.1111.0 has non-TTY output mode
- Asset hashing hangs on first run

**Substrate-pragmatic workaround**: direct Docker build + ECR push + `aws lambda update-function-code` (D.1.β pipeline). Used canonically for BEL H3 fix (commits c45d619, a995e17, 8df2eb8).

**Risk**: D.1.β ECR tags don't match CDK asset hash; next CDK deploy (if Tony interactively triggers it) WILL overwrite manual updates.

Banked pending substrate-investigation dispatch.

### Track D — 5/2 BEL AUC 0.5065 substrate-confound investigation

**Substrate-evidence verdict**: 5/2 race-day had 17:1 longshot winner (max winner ML = 17.20; adjacent 5/3 max = 3.74 favorite-heavy). Hybrid C is favorite-leaning → longshot upset degrades AUC at race-day granularity.

**6-hypothesis test outcomes**:
- H1 off-turf: negative (0 off-turf on 5/2)
- H2 stakes-day: weak (1 graded on 5/2 vs 3 on 5/3 with AUC 0.66)
- H3 weather: negative (fast+firm substrate-standard)
- H4 parser substrate-thin: negative (tc/eqb/fs all 100% on 5/2)
- H5 field composition: **CONFIRMED** (17:1 winner)
- H6 Hybrid C feature sparsity: negative (avg_p 0.117 ≈ adjacent dates)

**Substrate-pragmatic verdict**: 5/2 substrate-coherent race-day variance, NOT substrate-bug. Substrate-evidence-grounded race-day variance is signal for Tier 3 specialist_style stratification (consistent with specialist_style's stronger ROI when favorites lose).

### Track E — Tier 3 specialist_style inverse-pattern investigation (STATE 1 CONFIRMED)

**Substrate-evidence**: specialist_style ensemble on BEL 5/2-5/10 stratum (n_bets=59 common races with Hybrid C):
- Hybrid C: 15 wins / payouts $90.00 / ROI **-23.7%**
- specialist_style: 14 wins / payouts $106.48 / ROI **-9.8%**
- Δ ROI = +13.9pp despite Δ AUC = -0.026

**State 1 verdict** (genuine high-EV longshot finder): specialist_style finds longer-priced winners than Hybrid C. Trades 1 win for higher average payout. Substrate-grounded inverse pattern.

**F1 outcome**: **ACTIVATE specialist_style via § 4.36 alternate path** authorized (substrate-evidence-grounded; stratified BEL substrate validates Tier 2 EXECUTION finding under H3-fix-clean substrate).

**F3 outcome**: § 4.36 codification extension **substrate-evidence-pending**. 2-instance accrual (Tier 2 EXECUTION original + this BEL stratified re-verification) substrate-thin per § 4.36 multi-instance gating (3+ required). Bank for accrual.

**F4 outcome**: Hybrid C v2 retrain candidacy substrate-pragmatic candidate via specialist_style alternate routing (use specialist_style for substrate-stratified race-conditions, Hybrid C for substrate-standard). Detailed retrain scope deferred to separate dispatch.

---

## Codification cadence

Per Tony substrate-pragmatic batching: codification dispatches fire at Phase A close-out cadence OR when accrual threshold crossed. § 4.32 CS6 sub-pattern B Events #6-#9 are substrate-emphatic (4-instance); ready for next codification cycle.
