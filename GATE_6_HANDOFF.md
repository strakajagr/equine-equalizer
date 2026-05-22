# GATE 6 HANDOFF — MACHINE SWITCH

**Pushed:** 2026-05-22
**Branch:** `repair-5-clean-deploy`
**Latest commit:** `26d44b3 Gate 6: substrate cleanup`

---

## TO PULL ON LAPTOP

```bash
cd /path/to/equine-equalizer  # wherever your laptop checkout lives
git fetch origin
git checkout repair-5-clean-deploy
git pull origin repair-5-clean-deploy
```

If the branch doesn't exist locally yet:
```bash
git fetch origin
git checkout -b repair-5-clean-deploy origin/repair-5-clean-deploy
```

---

## 3 COMMITS LANDED THIS SESSION

| Commit | Subject |
|---|---|
| `26d44b3` | Gate 6: substrate cleanup — parser fixes, FE wiring, AS-OF backfills |
| `483bfff` | Gate 3 / 3B / 3C / 5 diagnostic scripts |
| `22b1478` | prior-session WIP carry-forward: daily_report_generator.py |

The bottom commit (`22b1478`) is YOUR prior-session WIP that was sitting
in the working tree when this session started. I committed it separately
for clean visibility — `git revert 22b1478` if you want to drop it.

---

## DB STATE — ALREADY LIVE, NOT IN REPO

All Gate 6 backfills landed server-side on Aurora. **The laptop pulls
code only — the DB is already current.** No DB action needed on switch.

Cumulative substrate state in Aurora:

| Table / Field | State |
|---|---|
| `past_performances.running_style` / `trainer_name` | 98-100% (Bug #28 fixed) |
| `races.temperature` / `weather_conditions` / `track_condition` | 77-95% (Sep cliff fixed) |
| `entries.weight_carried` | 75-91% (was 29-65%) |
| `results.is_disqualified` | 381 TRUE / 201,840 rows (was 100% FALSE) |
| `workouts` (NYRA Jan 2024 → Aug 2025) | ~70K rows added (was 0) |
| `trainer_stats_history` | 177K rows × 230 weekly snapshots |
| `angle_stats_history` | 872K rows × 233 snapshots, 7 angles |
| `jockey_stats_history` (new table) | 80K rows × 229 snapshots |
| `track_bias_history` (new table) | 4.6K rows × 229 snapshots |
| `idx_pp_trainer_date` index | Created (CREATE INDEX) |

---

## CODE STATE — IN REPO POST-PULL

Touched / created files (in commits above):

**Parser + FE pipeline:**
- `backend/services/chart_parser.py` — Bug #28 + DQ extension
- `backend/services/ls_inference_service.py` — LSTM NaN sentinel
- `model/shared/data_loader.py` — Phase B Top-5 wiring + trajectory
  feature + orphan handler
- `model/shared/feature_definitions.py` — TRAJECTORY_FEATURE_DEFS
- `model/shared/lstm_loader.py` (new) — TrajectoryLSTM + S3 loader
- `model/trajectory/train.py` — `--end-date` arg

**Backfill scripts (model/):**
- `gate6_trainer_stats_backfill.py`
- `gate6_angle_stats_backfill.py` (7 angles)
- `gate6_jockey_stats_backfill.py`
- `gate6_track_bias_backfill.py`
- `gate6_non_nyra_workouts_scrape.py` (proved BUY — see HELD)
- `gate3_diagnostic_train.py`
- `gate3c_specialist_inference.py`

**Re-parse / scrape launchers (scripts/):**
- `gate5_census.py` — the full census tool
- `gate3*_*.py` — Gate 3 / 3B / 3C analyses
- `gate6_*.sh` — re-parse + NYRA workouts launchers

**Migrations:**
- `backend/database/migrations/004_gate6_drop_dead_columns.sql` —
  21-column DROP, **HELD (SHAP-gated)**, do NOT execute

**Image (Dockerfile.training):**
- Added `requests==2.31.0` + `beautifulsoup4==4.12.0`

---

## HELD (DO NOT EXECUTE WITHOUT EXPLICIT GO)

1. **`004_gate6_drop_dead_columns.sql`** — 21-column DROP migration.
   SHAP-gated per the Gate 6 Finish dispatch. Only execute after SHAP
   confirms the candidate columns are truly dead (not just low-gain).

2. **Specialist retrain** — substrate is materially the cleanest it's
   been, but the non-NYRA workouts gap is a known BUY item. Your call
   whether to retrain now (with workouts gap acknowledged) or wait for
   a BUY decision.

3. **Re-launch angles v4 for the 2 partial angles** —
   `second_off_layoff` and `surface_switch` are populated Jan 2022 →
   Jun 2024 only (task hung mid-2024). Re-launching
   `gate6_angle_stats_backfill.py` would extend coverage to May 2026.
   Small follow-up.

---

## BUY ITEMS (consolidated for paid-feed decision)

These all require Equibase or DRF paid feed — not recoverable from
HRN or current Equibase chart PDFs:

1. **Pedigree** — sire / dam / damsire stats by surface, distance,
   precocity. Largest single missing signal.
2. **Trip notes** — narrative race comments ("bumped start, 5w turn,
   gamely")
3. **8 entry-table equipment/medication flags** — bute, tongue_tie,
   bar_shoes, front_bandages, mud_caulks, blinkers_off,
   blinkers_first_time, equipment_change_from_last,
   medication_change_from_last (HRN hard-codes them to FALSE)
4. **`first_off_claim` trainer angle** — needs claim-transfer
   detection (was_claimed always FALSE, claiming_price_taken 0% in PP)
5. **Non-NYRA workouts gap** — CD/GP/KEE/MTH/OP/PIM/SA/DMR for
   Jan 2024 → Aug 2025 (HRN's workout coverage is NYRA-only;
   confirmed via 99.9% miss-rate scrape attempt)

---

## NEXT-TURN PRIORITIES

1. **SHAP analysis** on current substrate — what does the model
   actually use? Confirms (or doesn't) the dead-column DROP candidates.
2. **Cull pass** based on SHAP findings — remove features that don't
   carry signal even with the cleaner substrate.
3. **Retrain** specialists + ensemble on the clean substrate (with
   AS-OF history tables now available for trainer/angle/jockey/bias
   features).
4. **Eval** vs Gate 2 baseline + market — did the clean substrate
   actually narrow the 14pp market gap?
5. **BUY decision** — pedigree first if going paid (biggest single
   gap); others as bundle.

---

## VERIFIED ARTIFACTS (in `/home/strakajagr/` on the workstation, not in repo)

- `EE_GATE6_CLOSE_20260522.md` — final Gate 6 verdict
- `EE_GATE6_FINISH_20260522.md` — pre-close Gate 6 Finish report
- `EE_GATE5_CENSUS_*.csv` — full data census master + timeline
- `EE_GATE3_VERDICT_20260521.md`, `EE_GATE3B_*`, `EE_GATE3C_*` — Gate 3 verdicts

These are workstation-only reports — not in the repo. Copy to laptop
if needed, or recreate from the committed scripts.
