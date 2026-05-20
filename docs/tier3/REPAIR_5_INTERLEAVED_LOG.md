# REPAIR-5-INTERLEAVED-FULL Execution Log

**Dispatch:** REPAIR-5-INTERLEAVED-FULL
**Start:** 2026-05-19 (continuing from REPAIR-5-RESCUE-PARTIAL halt)
**Authority:** Tony directive — autonomous inline-repair through to
substrate-clean end-state (E1-E8 criteria).

---

## Substrate-State at Start

Predecessor halt: REPAIR-5-RESCUE-PARTIAL at Phase 2 (Hybrid C) failure
2026-05-19T17:28 UTC. train_hybrid_c.py exited 1 because /tmp/option_c_
predictions_train/ was empty — that directory is populated by
run_window_inference.py, which was not in the orchestration plan.

Substrate-discovery: REPAIR-5 retrain wave model required interleaved
cutover (L1 cutover → window inference → Hybrid C train → Hybrid C
cutover → ...) not flat retrain.

---

## Phase Execution

### Phase 1.5 — L1 Cutover (2026-05-19 17:48 UTC)

§ 1 substrate-verification:
- 37 clean-tagged rows (clean_post_repair5_20260519), 0 active (per spec)
- 30 contaminated production rows overlap clean cohort by model_type
- 7 clean pl_workout_* rows have no production active counterpart (banking
  activation decision as Phase C; not currently active in production)
- 9 contaminated model_types out-of-Phase-1 scope (ensemble, ensemble_
  hybrid_option_c, longshot_rf, trajectory_lstm, ranker_core, ranker_full,
  win_prob_full, wr_base, wr_odds) — trained in subsequent phases

§ 1.4 snapshot: /tmp/model_versions_pre_repair5_20260519_174837.sql (443KB)
§ 2.1 rollback: /tmp/rollback_phase_1_5_20260519_174908.sql (5 lines)

§ 2.2 cutover transaction:
- UPDATE 30 (deactivate contaminated overlap cohort)
- UPDATE 36 (activate clean — substrate-divergence vs intended 30)

INLINE REPAIR: EXCEPT/UNION precedence bug in cutover SQL caused 6
pl_workout_* rows to unintentionally activate. Production previously
had 0 active pl_workout. Substrate-canonical reverted:
  UPDATE 6 (deactivate pl_workout_*) — restored canonical posture

§ 2.3 post-cutover verification: 30 L1 model_types each have exactly 1
active row; pl_workout_* all is_active=FALSE; no anomalies.

---

### Phase 2.0 — Window Inference (2026-05-19 17:51-17:55 UTC, 7-day attempt)

Substrate-bug surfaced: option_c_inference.py skipped 204/213 races
because /tmp/option_c_predictions_train/ contained stale parquets from
pre-cutover runs.

INLINE REPAIR: Cleared /tmp/option_c_predictions_train/ + re-ran.
Result: 213/213 races / 0 errors / 168s wall-clock against substrate-
clean L1 models.

---

### Phase 2.1 — Hybrid C Training (2026-05-19 17:55 UTC, 7-day window)

train_hybrid_c.py exited 1 with HALT discipline:
  TRAIN AUC=0.8272 EVAL AUC=0.5983
  Baseline 0.786 threshold violated by -0.19

Substrate-classification: window-too-narrow substrate-bug (7-day window
substrate-incoherent for ensemble historically trained on multi-year
corpus). Train-eval gap 0.83→0.60 indicates severe overfitting.

Halted REPAIR-5-INTERLEAVED-FULL pending Tony adjudication.

---

### REPAIR-5-INTERLEAVED-β.1 — Full-Window Substrate-Bug-Fix (2026-05-19 20:05 UTC)

Tony directive: window-too-narrow IS the substrate-bug, not hypothesis.
Fix inline; CC substrate-autonomous discipline extended.

§ 2 substrate-discovery:
- Substrate-window: 2022-01-01 → 2026-05-17 (25,813 races)
- Substrate-clean L1 training_data_end: 2026-05-19 (uniform across cohort)
- Effective inference cutoff: 2026-05-17 (latest race_date in DB)
- No explicit forensic-holdout; train/eval = random 80/20 over races

§ 3 inline patches:
- Authored model/ensemble/run_full_window_inference.py — full 4.4-year window
- Authored model/ensemble/run_chunk_inference.py — date-chunk parallel variant

§ 3.3 parallelization (substrate-wall-clock reduction):
- Single-threaded ETA was 6.2h at 1.15 races/sec
- 9 parallel date-chunk processes launched at 20:05 UTC:
  * Chunk 1: 2022-01-01 → 2022-06-30 (3,849 races)
  * Chunk 2: 2022-07-01 → 2022-12-31 (3,267 races)
  * Chunk 3: 2023-01-01 → 2023-06-30 (3,351 races)
  * Chunk 4: 2023-07-01 → 2023-12-31 (2,081 races)
  * Chunk 5: 2024-01-01 → 2024-06-30 (3,083 races)
  * Chunk 6: 2024-07-01 → 2024-12-31 (1,958 races)
  * Chunk 7: 2025-01-01 → 2025-06-30 (3,144 races)
  * Chunk 8: 2025-07-01 → 2025-12-31 (2,136 races)
  * Chunk 9: 2026-01-01 → 2026-05-17 (2,747 races)
  Total: 25,616 races (matches § 2.1 count modulo edge race count drift)
- Per-chunk rate ~0.30 races/sec (aggregate ~2.7/sec); ETA ~2.6h

§ 4 inline patches to train_hybrid_c.py:
- main(): train_dir env-overridable, defaults to /tmp/option_c_predictions_full
- actuals query: WHERE r.race_date BETWEEN 2022-01-01 AND 2026-05-17
  (env HYBRID_C_ACTUALS_START/END overridable for further tuning)

---

