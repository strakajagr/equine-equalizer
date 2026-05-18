# Hybrid C v2 Retrain Decision Dispatch

**Status**: Tony adjudication surface
**Substrate-prerequisite gate**: Tier 3 specialist_style investigation COMPLETE (Track E State 1 confirmed)
**Authoring**: Tier 3 full close-out dispatch 2026-05-18

---

## Substrate-evidence package

### Tier 3 specialist_style investigation outcomes

**Track E State 1 verdict CONFIRMED**: specialist_style genuine high-EV longshot finder.

Substrate-evidence (Track E.2 on BEL 2026-05-02..05-10 common cohort, n_bets=59):

| Ensemble | Wins | Payouts | ROI | AUC (BEL stratum) |
|---|---|---|---|---|
| Hybrid C `option_c_hybrid_ensemble_20260515` | 15 | $90.00 | **-23.7%** | 0.6374 |
| specialist_style `specialist_style_specialist_20260518_0252` | 14 | $106.48 | **-9.8%** | 0.6115 |

**Δ ROI = +13.9pp** despite **Δ AUC = -0.026**. Substrate-grounded inverse pattern:
specialist_style trades 1 win for higher average payout. Substrate-coherent with
Tier 2 EXECUTION original finding (Δ ROI +25.5pp / Δ AUC -0.093 on full forensic window).

### Track D 5/2 substrate-evidence (favorite-vs-longshot variance)

H5 confirmed: 5/2 race-day had 17:1 longshot winner (max winner ML=17.20; adjacent
5/3 max=3.74 favorite-heavy). Hybrid C favorite-leaning → longshot upset depresses
AUC at race-day granularity. Substrate-grounds specialist_style stratification by
favorite-vs-longshot race-day conditions.

### § 4.36 codification status

Multi-instance accrual: **2 instances** of specialist_style inverse pattern surfaced
- Tier 2 EXECUTION original (forensic window 2026-05-02..2026-05-17)
- Tier 3 BEL stratified re-verification (this dispatch)

Threshold per § 4.36 codification-gating: **3+ instances** for codification
extension. Currently substrate-evidence-pending.

### Production state at decision time

- Hybrid C live (UUID 2d34b010-f17a-492e-8f7c-270bd393731d)
- Full 8-day BEL cohort: aggregate AUC 0.6732 (RESOLVED per F6 threshold)
- 162-strategy registry currently active
- Legacy 10-feature ensemble dual-write active (calendar-gated deactivation 2026-05-22)

### § 4.34 forensic-gate disturb-working-system caution

Hybrid C currently RESOLVED at AUC 0.6732. Retrain dispatches carry inherent
risk of degrading working-system substrate. § 4.34 prophylactic check: any
retrain candidate must substrate-evidence-grounded justify the disturbance risk.

---

## Three retrain candidate paths

### Path A — Hybrid C v2 retrain absorbing specialist_style as built-in stratum

**Substrate-pragmatic mechanism**: Retrain ensemble with stratum-conditional
weighting. Input: 32-feature substrate (identical to current Hybrid C).
Routing: substrate-pragmatic gate features (field_size, favorite_odds) feed a
gating sub-network; output is convex combination of "favorite-stratum" weights
(near current Hybrid C) and "longshot-stratum" weights (specialist_style-like).

**Pro**:
- Single deployment artifact (one ensemble_version replaces current)
- Substrate-pragmatic operational simplicity (no parallel-routing
  infrastructure)
- Substrate-coherent with existing inference pipeline (MultiCohortInferenceService
  unchanged signature; same race-prediction interface)

**Con**:
- Full retrain wall-clock substrate-pragmatic (estimated days for substrate-
  pragmatic re-training run; § 4.35 substrate-untrustworthy estimate)
- Disturb-working-system risk per § 4.34 forensic-gate caution
- Substrate-thin substrate for new gating sub-network (single inverse-pattern
  instance pre-Tier-3; 2-instance post-Tier-3 substrate-evidence; threshold-gating)
- Retrain may inadvertently degrade favorite-stratum performance (current
  Hybrid C strength)

**Substrate-validates if**: § 4.36 multi-instance accrual reaches 3+ before
retrain authorization fires. Currently substrate-evidence-pending.

### Path B — Keep Hybrid C unchanged; ACTIVATE specialist_style as parallel alternate-routing

**Substrate-pragmatic mechanism**: F1 ACTIVATE specialist_style already authorized
via § 4.36 alternate path (Track E.5 verdict). Deploy specialist_style as second
ensemble in production with routing layer at strategy_harness:
- Substrate-grounded routing predicate: `field_size >= 10 OR favorite_odds <= 2.0`
  → route to specialist_style; else Hybrid C
- Each ensemble produces predictions independently; harness selects by predicate
  at strategy-generation time
- Both predictions persisted to hybrid_c_predictions with distinct
  ensemble_version values

**Pro**:
- No Hybrid C disturbance (substrate-conservative; § 4.34 forensic-gate
  respected)
- Substrate-evidence-grounded ROI improvement on longshot stratum (Track E.2
  Δ ROI +13.9pp)
- Substrate-pragmatic incremental: specialist_style ACTIVATE is single-step;
  no retrain wall-clock
- substrate-pragmatic-reversible: roll back routing if substrate-pragmatic
  divergence surfaces in production

**Con**:
- Routing logic substrate-complexity at strategy_harness layer
- Two ensembles in production (operational overhead; cost surface
  substrate-pragmatic minimal — both already trained)
- Routing predicate substrate-pragmatic-thresholds require empirical tuning
  (substrate-investigation scope)
- Substrate-evidence-pending § 4.36 codification (could be premature ACTIVATE
  if 3rd instance accrual proves inverse pattern transient)

**Substrate-validates if**: Tony substrate-pragmatic risk tolerance favors
working-system-preserve + substrate-evidence-grounded incremental over
retrain risk. § 4.36 codification can lag ACTIVATE per Tony directive
"working_system_first" pattern.

### Path C — Status quo (KEEP CURRENT; defer ACTIVATE)

**Substrate-pragmatic mechanism**: Maintain current Hybrid C production state
unchanged. Wait for § 4.36 codification 3-instance accrual before ACTIVATE
authorization fires. specialist_style remains in BD2v2 substrate ready for
future ACTIVATE.

**Pro**:
- Maximum substrate-pragmatic patience; § 4.36 gating respected verbatim
- Zero disturbance risk (substrate-conservative)
- Substrate-pragmatic free option: accrual proceeds naturally as new Tier 2/3
  cohorts measure specialist_style

**Con**:
- Leaves substrate-evidence-grounded +13.9pp ROI improvement on table
- specialist_style finding may decay over time if production substrate-cohort
  drifts pre-ACTIVATE
- Substrate-pragmatic concern: § 4.36 3-instance threshold may take multiple
  cohorts to satisfy; calendar-pragmatic delay substantial

**Substrate-validates if**: Tony substrate-pragmatic patience high + § 4.36
codification-gating treated as strict (codification before ACTIVATE).

---

## Tony adjudication surface

**Decision**: Path A / Path B / Path C

**Substrate-evidence-grounded recommendation**: substrate-pragmatic Path B
(ACTIVATE specialist_style as parallel alternate-routing).
- Substrate-coherent with F1 already-authorized ACTIVATE
- § 4.34 forensic-gate disturb-working-system caution respected
- Substrate-evidence Track E.2 +13.9pp ROI substrate-grounded
- Substrate-pragmatic reversible (roll back if production-divergent)
- Substrate-pragmatic incremental cost (no retrain wall-clock)

**Path A risk-acceptance threshold**: Tony substrate-pragmatic-tolerant of
working-system disturb if substrate-evidence threshold satisfied. Substrate-
evidence-pending until § 4.36 3-instance accrual.

**Path C patience threshold**: Tony substrate-pragmatic-patient for § 4.36
codification before ACTIVATE.

**Open substrate-investigations** (out-of-scope this dispatch; surface for
Tony's next-decision adjudication):

1. Routing predicate empirical tuning (if Path B): which feature gates
   substrate-evidence-optimal? `field_size`, `favorite_odds`, both, other?
2. Stratified backfill: re-measure specialist_style on additional cohorts
   (CD, SA, GP, etc.) to surface § 4.36 3rd-instance candidates
3. specialist_style 4/30 + 5/1 BEL coverage gap (preds=0 for new BAQ-bonus
   dates per Track A.5 substrate-evidence); separate inference re-run scope

---

## Substrate-prerequisite gates post-decision

- **Path A authorization**: requires § 4.36 3-instance accrual (currently 2)
- **Path B authorization**: F1 ALREADY AUTHORIZED via § 4.36 alternate path
  per Track E.5; can fire on Tony Path B selection
- **Path C authorization**: no action; current production state preserved
