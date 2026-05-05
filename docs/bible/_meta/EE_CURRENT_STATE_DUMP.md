# Equine Equalizer — Current State Dump

**Generated:** 2026-05-03
**Purpose:** Phase 0 input for Architecture Bible build (modeled on Dynasty Dugout's `ARCHITECTURE_BIBLE.md`)
**Stance:** OBSERVATION ONLY. No fixes. No "this looks wrong." Pure inventory.

---

# 1. File Tree

Top-level directories (depth ≤3, excluding `node_modules`, `__pycache__`, `.git`, `build`, `dist`, `cdk.out`, `venv`, `layers`, `tmp`):

```
.
├── backend/                       Python source — services, repos, routers, lambdas, shared
│   ├── database/                  SQL schema + Alembic-style numbered migrations
│   │   ├── migrations/            011 numbered .sql files + migrate.py runner
│   │   ├── schema/                schema.sql (bootstrap reference, 415 lines)
│   │   └── seeds/
│   ├── lambdas/                   8 Lambda handler entry points (one dir per Lambda)
│   │   ├── feature-engineering/
│   │   ├── inference/
│   │   ├── ingestion/             Largest (1,689 lines) — 25 action types
│   │   ├── ls-inference/
│   │   ├── nyra-workouts/
│   │   ├── pl-inference/
│   │   ├── results/
│   │   └── wr-inference/
│   ├── models/                    Canonical dataclasses (Race, Entry, Prediction, etc.) — single file canonical.py
│   ├── repositories/              Per-table repos (DB → dataclass mapping)
│   ├── routers/                   Lambda-handler-as-router pattern (def get_*, def post_*)
│   ├── services/                  Business-logic layer (chart_parser, evaluation, ingestion, FE, inference x3)
│   │   └── data_sources/          Pluggable scraper interface (HRN active; DRF/BRIS/Equibase listed as future)
│   └── shared/                    constants.py, db.py, horse_naming.py, race_typing.py
├── data/                          Local data dir; raw/ and processed/ subdirs (largely unused outside dev)
│   ├── processed/
│   └── raw/
├── docs/                          Project docs, session logs
│   ├── bible/                     Phase 0 of Architecture Bible (this directory)
│   │   └── _meta/
│   └── sessions/                  SESSION_001..NNN.md history (not read here)
├── equibase_probe/                EXPLORATORY: 4 separate probe scripts (probe.py, option_a2/b/d_probe.py)
│                                  exploring playwright-stealth approaches to bypass Imperva. Not in production.
├── frontend/                      React 19 + TypeScript SPA
│   ├── public/
│   └── src/
│       ├── api/                   axios client (single client.ts)
│       ├── components/            Common, Compare, Layout, RaceCard, Stats, ValuePlays
│       ├── pages/                 9 page components (Today, Gonzo, Compare, BetBuilder, etc.)
│       └── types/
├── infrastructure/                CDK (TypeScript)
│   └── cdk/
│       ├── backend/               Lambda code synced into CDK during deploy (build artifact, not source-of-truth)
│       ├── bin/                   cdk.ts entry
│       ├── lib/                   4 stacks: ComputeStack, DatabaseStack, FrontendStack, StorageStack
│       └── test/
├── model/                         ML training infrastructure (separate from backend services)
│   ├── angles/                    Bayesian angle scorer (Layer 6 of LS stack)
│   ├── artifacts/                 Local artifact dir (S3 is canonical)
│   ├── ensemble/                  Stacking meta-learner (Layer 7 of LS stack)
│   ├── evaluation/                metrics.py
│   ├── features/                  ALT feature_definitions.py — 73-feature schema, distinct from shared/
│   ├── longshot/                  RandomForest longshot classifier (Layer 4)
│   ├── ls/                        README only — placeholder for unified LS docs
│   ├── pl/                        Path-2 P&L XGBoost trainer (per-style: general, specialists)
│   ├── ranker/                    LambdaMART rank:pairwise trainer (rk_core, rk_full)
│   ├── shared/                    Training-time data loader, gonzo features, par times, specialists
│   ├── trajectory/                LSTM trajectory predictor (Layer 5)
│   ├── training/                  Generic trainer + speed figure computation
│   ├── win_prob/                  Binary win/lose XGBoost trainer (Layer 1)
│   └── wr/                        Path-1 Win Rate XGBoost trainer (uses EV labels)
├── scripts/                       Operational scripts: deploy, calibration fitters, backfills, diagnostics
│   ├── reparse_charts.py
│   ├── reparse_payouts.py
│   ├── reparse_results.py
│   ├── reparse_horse_cascade.py
│   ├── fit_*_calibrations.py      4 calibration scripts (lean53, lean53_core, all, wp)
│   ├── reinfer_all_historical.py
│   ├── merge_duplicate_horses.py
│   ├── phase1_holdout_compare.py
│   ├── lean53_diagnostic.py
│   ├── longshot_bias_diagnostic.py
│   ├── post_calibration_diagnostic.py
│   ├── backfill.sh, backfill_race_types.py
│   ├── deploy-backend.sh, deploy-frontend.sh
│   └── run-migrations.sh, train-model.sh
└── tmp/                           Local scratch
```

Top-level Dockerfiles (build context for Lambdas/ECS):
- `Dockerfile.feature-engineering`, `Dockerfile.inference`, `Dockerfile.ingestion`, `Dockerfile.ls-inference`, `Dockerfile.nyra-workouts`, `Dockerfile.pl-inference`, `Dockerfile.results`, `Dockerfile.training`, `Dockerfile.wr-inference`

`deploy_all.sh` is the orchestration script (CDK deploy → frontend build → infer → eval).

---

# 2. Backend Module Inventory

## 2.1 Repositories (`backend/repositories/`)

| File | Lines | Purpose |
|---|---|---|
| `base_repository.py` | 75 | Shared `_query` / `_query_one` helpers |
| `entry_repository.py` | 237 | `entries` table CRUD + per-race entry list |
| `horse_repository.py` | 127 | `horses` table CRUD; horse name lookup/dedup |
| `model_version_repository.py` | 147 | `model_versions` registry — `get_active_model_by_type`, etc. |
| `past_performance_repository.py` | 314 | `past_performances` reads (history per horse for FE) |
| `prediction_repository.py` | 345 | Legacy `predictions` table (predates wr/pl/ls split) |
| `wr_prediction_repository.py` | 643 | `wr_predictions` writes/reads + serializers |
| `pl_prediction_repository.py` | 465 | `pl_predictions` writes/reads + value-bet flagging |
| `ls_prediction_repository.py` | 495 | `ls_predictions` reads (writes still go to `wr_predictions` enrichment columns per Bug #25 comment) |
| `race_repository.py` | 341 | `races` table CRUD + qualifying-race filter |
| `result_repository.py` | 212 | `results` table inserts (called from chart parser + HRN scraper) |
| `track_repository.py` | ~80 | `tracks` table reads |
| `track_record.py` | 177 | Aggregated hit-rate / ROI rollup queries |
| `transforms.py` | 650 | Row-dict → canonical-dataclass mappers (largest repo file) |
| `workout_repository.py` | 173 | `workouts` table reads/writes |

## 2.2 Services (`backend/services/`)

| File | Lines | Purpose |
|---|---|---|
| `chart_parser.py` | 1,372 | Equibase PDF → races/entries/results/PPs ingest. `parse_payout_section`, `process_pdf`, `run_from_s3` |
| `data_sources/base.py` | 131 | `DataSourceInterface` ABC for pluggable scrapers |
| `data_sources/hrn_scraper.py` | 974 | HRN entries + results scraper (playwright-stealth based) |
| `data_sources/hrn_workout_scraper.py` | 454 | HRN workout-page scraper (requests + BS4) |
| `evaluation_service.py` | 190 | `record_results` — joins predictions to results post-hoc |
| `feature_engineering_service.py` | 1,211 | INFERENCE-time feature matrix builder; mirrors `model/shared/data_loader.py` semantics |
| `inference_service.py` | 844 | Generic batch inference orchestrator (legacy, predates wr/pl/ls split) |
| `ingestion_service.py` | 665 | Wraps `DataSourceInterface` calls, persists race cards |
| `ls_inference_service.py` | 574 | LS pipeline (Layers 4–7); enriches `wr_predictions` rows in place |
| `pl_inference_service.py` | 612 | PL pipeline; writes `pl_predictions` |
| `wr_inference_service.py` | 890 | WR pipeline (Layers 1–3); writes `wr_predictions` |

## 2.3 Routers (`backend/routers/`)

Routers are NOT FastAPI — they expose `def get_*(event, context) -> dict` functions called directly from Lambda handlers. API Gateway routes map to specific function names.

| File | Lines | Purpose |
|---|---|---|
| `dashboard_router.py` | 173 | `/dashboard/metrics` endpoint |
| `health_router.py` | ~30 | `/health`, `/{model}/health` |
| `horse_router.py` | 188 | `/horses/{horse_id}/pps` |
| `ls_prediction_router.py` | 246 | `/ls/predictions/*` (today, by-date, per-race, alerts, longshots, run, track-record) |
| `pl_prediction_router.py` | 281 | `/pl/predictions/*` (parallel set to LS) |
| `prediction_router.py` | 148 | Legacy generic `/predictions/*` |
| `race_router.py` | 348 | `/races/{date}`, `/races/{raceId}/detail`, `/races/today`, `/races/available-dates`, `/cards/{date}/{track_code}` |
| `unified_prediction_router.py` | 118 | `/predictions/{date}/{track_code}/{race_number}` — combines all 3 models |
| `wr_prediction_router.py` | 460 | `/wr/predictions/*` + `/wr/predictions/track-record-by-style` + `/wr/predictions/{date}/compare` |

## 2.4 Lambda entry points (`backend/lambdas/<name>/handler.py`)

| Lambda | Memory | Timeout | Purpose |
|---|---|---|---|
| `equine-ingestion` | 2048 MB | 900 s | 25-action dispatcher (see Section 5 list); fetches results, parses charts, registers models, runs raw queries |
| `equine-feature-engineering` | 512 MB | 300 s | Stub (`# TODO: Wire to feature_engineering_service`) |
| `equine-inference` | 1024 MB | 300 s | Generic inference dispatcher + race/horse routing |
| `equine-wr-inference` | 1024 MB | 300 s | WR predictions (Layers 1–3) |
| `equine-pl-inference` | 1024 MB | 300 s | PL predictions |
| `equine-ls-inference` | 1024 MB | 300 s | LS enrichment (Layers 4–7) |
| `equine-results` | 512 MB | 300 s | Calls `EvaluationService.record_results(target_date)` |
| `equine-nyra-workouts` | 512 MB | 300 s | NYRA-specific workout scraper → S3 → `load_workouts_from_s3` ingestion action |

## 2.5 Shared utilities (`backend/shared/`)

| File | Lines | Purpose |
|---|---|---|
| `constants.py` | 155 | `QUALIFYING_TRACKS`, `MIN_CLAIMING_PRICE`, `OVERLAY_THRESHOLD`, `BANKROLL`, `KELLY_FRACTION`, `MAX_BET_PCT`, `MIN_EDGE_TO_BET`, `STRONG_VALUE_THRESHOLD`, `HANDICAPPING_BLEND_WEIGHT` |
| `db.py` | 133 | `get_db()` context manager, `execute_query`, `execute_one`. Reads DB credentials from Secrets Manager |
| `horse_naming.py` | ~50 | `normalize_horse_name`, `horse_match_key` (used for HRN→DB joins) |
| `race_typing.py` | ~60 | `classify_race_type` (raw chart text → canonical race_type code) |

## 2.6 Canonical dataclasses (`backend/models/canonical.py`)

481 lines, single file. Defines `Race`, `Entry`, `PastPerformance`, `Workout`, `Prediction`, `WRPrediction`, `PLPrediction`, `LSPrediction`, `Result`. Includes `equibase_speed_figure` and `equibase_race_id` fields.

---

# 3. ML Model Inventory

## 3.1 Model registry summary (live from `/dashboard/metrics`)

- **Total entries in `model_versions`:** 88
- **Currently `is_active=TRUE`:** 45

Multiple models can be active simultaneously because each `(model_type, style/specialist)` pair has its own active row.

## 3.2 Model families & types

### WR family (Win Rate / Path 1)
Trained with EV labels (`reg:squarederror`). Two layers:
- **Core (`wp_core_*`)**: 58 features (no workouts)
- **Workout (`wp_workout_*` / `wp_full_*`)**: core + 8 workout features

| Active version (sample) | Type | Style |
|---|---|---|
| `wp_full_gonzo_sauce_20260502_0316` | XGBoost reg:squarederror | gonzo_sauce |
| `wp_core_lean53_20260429_2338` | XGBoost reg:squarederror | lean53 general |
| `wp_core_lean53_speed_20260429_2348` | XGBoost reg:squarederror | speed specialist |
| `wp_core_lean53_closer_20260429_2348` | XGBoost reg:squarederror | closer specialist |
| `wp_core_lean53_class_dropper_*` | XGBoost reg:squarederror | class_dropper specialist |
| `wp_core_lean53_class_riser_*` | XGBoost reg:squarederror | class_riser specialist |
| `wp_core_lean53_sprint_*` | XGBoost reg:squarederror | sprint specialist |
| `wp_core_lean53_route_*` | XGBoost reg:squarederror | route specialist |
| `wp_full_lean53_*` (general + 6 specialists) | XGBoost reg:squarederror | lean53 full |

- **Training script:** `model/wr/train.py`
- **Inference path:** `equine-wr-inference` Lambda → `WRInferenceService` (`backend/services/wr_inference_service.py`)
- **Output:** `win_probability`, `place_probability`, `show_probability`, `predicted_rank`, `confidence_score`, `is_top_pick`, written to `wr_predictions`
- **Calibration:** sidecar JSON in S3 for `gonzo_sauce` only; "all styles bypass calibration at inference tonight" per `wr_inference_service.py:619` comment (Bug #24)

### Ranker family (Layer 2)
- **Active:** `rk_full_gonzo_sauce_20260502_0452`, `rk_full_lean53_*` (general + 6 specialists), `rk_core_20260322_0037`
- **Type:** XGBoost `rank:pairwise` (LambdaMART), eval `ndcg`
- **Training:** `model/ranker/train.py` (15K lines)
- **Inference:** loaded by `WRInferenceService` (NOT by a separate ranker service)
- **Feature counts:** rk_core 58, rk_full 53 (lean53) or 67 (gonzo_sauce). The `RANKER_FULL_CULL` 15-feature subtraction is documented in `model/shared/feature_definitions.py`.
- **Calibration:** sidecar `*_calibration.json` for gonzo_sauce ranker; method `sklearn.isotonic.IsotonicRegression(out_of_bounds='clip', y_min=0.0, y_max=1.0)`

### PL family (Path 2 — P&L Optimization)
- **Versions:** `pl_core_*` (15 active), `pl_workout_*` (14 active)
- **Type:** XGBoost reg:squarederror with EV labels (re-uses WR config via `model/pl/config.py`)
- **Training:** `model/pl/train.py` (388 lines)
- **Inference:** `equine-pl-inference` Lambda → `PLInferenceService`
- **Features:** `get_lean53_core_features()` = 47 features (lean53 pl_core) with legacy fallback to 58
- **Output:** `win_probability`, `predicted_ev`, `edge_pct`, `is_value_bet`, `is_strong_value`, `kelly_fraction`, `kelly_bet_size` → `pl_predictions`
- **Calibration:** none documented; uses temperature-scaled softmax (`SOFTMAX_TEMPERATURE=1.0`)

### Win Probability family (Layer 1, separate from WR)
- **Active:** various `wp_base_*`, `wp_odds_*` from Mar 17–20 (legacy Path 0?)
- **Type:** XGBoost `binary:logistic`, output is calibrated `P(win)` directly from sigmoid
- **Training:** `model/win_prob/train.py` (696 lines)
- **Per-style:** general + same 6 specialists

### LS Stack (5-7 layer)
Per `model/ls/README.md` (single README in dir):
- **Layer 1: `wp_*` (binary win)** — already covered above
- **Layer 2: ranker (`rk_*`)** — already covered above
- **Layer 3: Value overlay** — pure arithmetic, NOT a trained model. Lives in `wr_inference_service.py:compute_value_overlay`
- **Layer 4: `longshot_rf`** — RandomForestClassifier. Active version: `longshot_rf_20260322_0441`. Training: `model/longshot/train.py`. Binary label = "won at closing_odds ≥ 10.0".
- **Layer 5: `trajectory_lstm`** — PyTorch LSTM (`hidden_size=32`, 2 layers, dropout 0.3, sequence length 5, 8 features per step). Active: `trajectory_lstm_20260322_0541`. Predicts whether next-race speed figure improves vs. sequence average.
- **Layer 6: Bayesian angle scorer** — `model/angles/scorer.py` (174 lines). NOT XGBoost; uses Beta-Binomial posteriors (per `bayesian_angle_ev` field in `ls_predictions`).
- **Layer 7: `ensemble`** — Logistic regression meta-learner combining all base outputs. Active: `ensemble_20260322_0649`. Training: `model/ensemble/train.py` (271 lines). Trained on 2025 held-out OOF predictions. Features per `model/ensemble/config.py`: `[win_prob, rank_score, longshot_prob, trajectory_score, angle_ev, angle_posterior, closing_odds, morning_line_odds, race_quality_tier, field_size]` (10 features).
- **Inference path:** `equine-ls-inference` Lambda → `LSInferenceService`. Reads existing `wr_predictions` rows (post WR pass) and updates in place. ALSO writes to `ls_predictions` table per migration 010 (treated as "first-class" since 2026-05-01).

## 3.3 Models active per style/specialist

From the active set (45 models), distinct style/specialist combinations:
- `general` (default)
- `gonzo_sauce` (Phase A3 — only active for `wp_full` and `rk_full`)
- `lean53` (general)
- `speed`, `closer`, `class_riser`, `class_dropper`, `sprint`, `route` (6 specialist styles)

Other model types where style isn't applicable: `longshot_rf`, `trajectory_lstm`, `ensemble`.

Tony's spec named "general / gonzo_sauce" as the user-facing WR style toggle. The remaining specialists are present in the registry but are not exposed as `?style=` values in the WR API responses (only `general` and `gonzo_sauce` returned `count: 24` for Derby R12 when probed).

---

# 4. Database Schema Inventory

Database name: `equine_equalizer`
Cluster ARN: `arn:aws:rds:us-east-1:584812014683:cluster:equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`
Aurora Serverless PostgreSQL.

**NOTE:** Could not run `information_schema` introspection — `equine-ingestion` Lambda is currently INACTIVE (image deleted from ECR; Docker rebuild required). Schema inventory below is from `backend/database/schema/schema.sql` + migrations 001–011. Row counts approximated from API endpoints.

## 4.1 Tables

| Table | Cols | Source | Approx rows | Purpose |
|---|---|---|---|---|
| `tracks` | 8 | schema.sql | 11 (QUALIFYING_TRACKS) | Track metadata: code, name, surfaces, MIN_CLAIMING_PRICE |
| `horses` | 13 | schema.sql | unknown (>50K assumed) | Horse identity, sire/dam/dam_sire references (self-FK), foaling_date, sex, color, country |
| `trainers` | 4 | schema.sql | unknown | Trainer name + license |
| `jockeys` | 5 | schema.sql | unknown | Jockey name + license + apprentice flag |
| `races` | 24 | schema.sql | ~2,611 visible via API (100 days) | Race card metadata: distance, surface, type, grade, name, purse, claiming, conditions, weather, equibase_race_id |
| `entries` | 26 | schema.sql | ~30K | Per-horse-per-race entry: post position, program number, ML odds, weight, equipment flags (lasix/blinkers/etc.), scratch flag |
| `past_performances` | 91 | schema.sql | unknown (~250K+ from training context) | Per-horse historical race detail. Largest table by columns. Critical: `race_id` is NULL for ALL historical rows per data_loader.py docstring |
| `workouts` | 12 | schema.sql | 143K+ rows (per data_loader docstring) | Workout history: date, distance, time, bullet flag, type, rank_on_day |
| `results` | 25 | schema.sql | unknown | Race outcome per entry: finish position, payouts (win/place/show/exacta/trifecta/superfecta/daily_double), call positions, beyer figure |
| `predictions` | 23 | schema.sql | unknown (legacy table, predates 005) | Original single-table predictions; superseded by wr/pl/ls split in migration 005 |
| `model_versions` | 17 | schema.sql | 88 (45 active) | Model registry: version_name, training_date, training_race_count, top1_accuracy, exacta_hit_rate, calibration_score, feature_list (JSONB), hyperparameters (JSONB), s3_artifact_path, is_active, notes (JSONB-in-TEXT) |
| `wr_predictions` | 26 | migration 005 | unknown | Win Rate predictions (Layer 1+2+3 + LS enrichment columns added later) |
| `pl_predictions` | 23 | migration 005 | unknown | P&L predictions with Kelly + edge fields |
| `ls_predictions` | 24 (after 010) | migration 005 + 010 | 0 historical, populating since Phase A3 (May 2026) per migration 010 comment | LS predictions; first-class as of migration 010 (2026-05-01) |
| `trainer_stats` | 8 | migration 008 | derived | MATERIALIZED VIEW over `past_performances`: total_starts, win_rate, itm_rate, layoff_win_rate, lasix_win_rate, claimed_win_rate. Min 5 starts. Refresh manually after data loads. |

15 tables + 1 materialized view.

Notable schema constraints:
- `entries`: `UNIQUE(race_id, horse_id)`
- `races`: `UNIQUE(track_id, race_date, race_number)` + `UNIQUE(equibase_race_id)`
- `wr_predictions` / `pl_predictions`: `UNIQUE(entry_id)` (one prediction per horse per race per model)
- `ls_predictions`: `UNIQUE(race_id, entry_id, style)` (replaced single-col UNIQUE in migration 010 for style differentiation)
- `model_versions`: no UNIQUE on version_name (multiple rows per name observed)

## 4.2 Migrations 001–011

| # | Filename | Purpose |
|---|---|---|
| 001 | `001_initial_schema.sql` | Bootstrap of 11 base tables |
| 002 | `002_fix_race_type_length.sql` | VARCHAR widening for race_type |
| 003 | `003_widen_varchar_columns.sql` | Further VARCHAR widening |
| 004 | `004_backfill_running_style.sql` | Backfill running_style on past_performances |
| 005 | `005_backfill_pace_delta.sql` | Backfill pace_delta column |
| 005 | `005_three_prediction_tables.sql` | wr/pl/ls split (duplicate-numbered with 005 above) |
| 006 | `006_backfill_early_pace_pressure.sql` | Backfill early_pace_pressure |
| 007 | `007_backfill_trainer_name.sql` | Backfill trainer_name on past_performances |
| 008 | `008_create_trainer_stats.sql` | Create `trainer_stats` materialized view |
| 009 | `009_backfill_pace_delta_v2.sql` | Re-do pace_delta backfill |
| 010 | `010_ls_predictions_first_class.sql` | LS predictions table promoted to first-class (style col + new UNIQUE) |
| 011 | `011_wr_predictions_unique_fix.sql` | UNIQUE constraint adjustment on wr_predictions |

Two files share number `005`. There is no migration history table observable from outside the DB.

---

# 5. Data Pipeline Inventory

## 5.1 EventBridge cron schedules (from `aws events list-rules`)

| Rule name | Cron | State |
|---|---|---|
| `equine-ingestion-daily` | `cron(0 11 * * ? *)` | ENABLED |
| `equine-fetch-results-nightly` | `cron(30 1 * * ? *)` | ENABLED |
| `equine-results-daily` | `cron(0 4 * * ? *)` | ENABLED |
| `equine-angle-stats-nightly` | `cron(15 2 * * ? *)` | ENABLED |
| `equine-nyra-workouts-daily` | `cron(0 10 * * ? *)` | ENABLED |
| `equine-feature-engineering-daily` | `cron(0 12 * * ? *)` | DISABLED |
| `equine-inference-daily` | `cron(30 12 * * ? *)` | DISABLED |
| `equine-wr-inference-daily` | `cron(30 12 * * ? *)` | ENABLED |
| `equine-pl-inference-daily` | `cron(35 12 * * ? *)` | ENABLED |
| `equine-ls-inference-daily` | `cron(40 12 * * ? *)` | ENABLED |
| `equine-daily-retrain-full` | `cron(30 2 * * ? *)` | ENABLED |
| `equine-weekly-retrain-wr` | `cron(0 4 ? * MON *)` | ENABLED |
| `equine-weekly-retrain-pl` | `cron(0 5 ? * MON *)` | DISABLED |

13 rules total: 8 enabled, 5 disabled.

## 5.2 Pipelines (high-level)

### A. Daily ingestion (race cards)
- **Trigger:** `equine-ingestion-daily` @ 11:00 UTC
- **Lambda:** `equine-ingestion`, action likely `test_scrape` or HRN-based fetch (action specifics vary per cron payload)
- **Source:** HRN entries page (`HRNScraper`)
- **Destinations:** `tracks`, `horses`, `trainers`, `jockeys`, `races`, `entries`, `past_performances`

### B. Nightly results fetch
- **Trigger:** `equine-fetch-results-nightly` @ 1:30 UTC
- **Lambda:** `equine-ingestion`, action `fetch_results`
- **Source:** HRN results page
- **Destination:** `results` table
- **Known failure mode:** Bug #28 (off-by-one column shift) — `win_payout` and `daily_double_payout` NULL for all rows since 2026-04-30

### C. Chart parser (S3 PDFs → results enrichment)
- **Trigger:** `parse_charts` action invoked manually OR via scheduled task (no dedicated cron found)
- **Service:** `chart_parser.py` (`run_from_s3`)
- **Source:** Equibase PDFs in `s3://equine-raw-data/charts/<TRACK>/`
- **Destination:** `races`, `entries`, `results`, `past_performances`
- **Known issue:** PDFs for 2026-04-30, 2026-05-01, 2026-05-02 not yet in S3 (no Equibase fetcher in codebase; uploaded externally or by an unidentified process)

### D. NYRA workout scrape
- **Trigger:** `equine-nyra-workouts-daily` @ 10:00 UTC
- **Lambda:** `equine-nyra-workouts` → writes JSON to S3 → triggers `load_workouts_from_s3` action on `equine-ingestion`
- **Tracks:** SAR, BEL, AQU
- **Destination:** `workouts` table

### E. Daily inference (3 separate Lambdas)
- **Triggers:** WR @ 12:30 UTC, PL @ 12:35 UTC, LS @ 12:40 UTC
- **Order:** WR runs first (writes `wr_predictions` Layer 1+2+3), PL writes its own `pl_predictions`, LS reads `wr_predictions` and enriches Layers 4–7 in place + writes `ls_predictions`
- **Generic `equine-inference-daily` (12:30 UTC) is DISABLED** — replaced by per-model lineup

### F. Results matcher
- **Trigger:** `equine-results-daily` @ 4:00 UTC
- **Lambda:** `equine-results` → `EvaluationService.record_results(target_date)`
- **Joins:** results to predictions; populates `actual_finish`, `was_win`, `was_place`, `was_show`, `exacta_hit`, `trifecta_hit`, `bet_profit`

### G. Angle stats refresh
- **Trigger:** `equine-angle-stats-nightly` @ 2:15 UTC
- **Lambda:** `equine-ingestion`, action `refresh_angle_stats`
- **Used by:** Layer 6 Bayesian angle scorer

### H. Daily retraining
- **Trigger:** `equine-daily-retrain-full` @ 2:30 UTC
- **Compute:** ECS Fargate task `equine-training-daily-full` (8 revisions, current image `equine-training:clean-data-lean53-core-1777504361`, 2 vCPU / 4 GB)
- **Cluster:** `equine-cluster`

### I. Weekly retraining
- **Triggers:** `equine-weekly-retrain-wr` @ Mon 4:00 UTC (ENABLED), `equine-weekly-retrain-pl` @ Mon 5:00 UTC (DISABLED)
- **Compute:** ECS Fargate

## 5.3 Ingestion Lambda actions (`backend/lambdas/ingestion/handler.py`)

25 distinct actions dispatched via `event['action']`:
`migrate`, `refresh_angle_stats`, `collect_workouts`, `fetch_results`, `run_admin_sql`, `register_model`, `deactivate_all`, `train_wr_model`, `train_model`, `activate_model`, `parse_charts`, `test_scrape`, `raw_query`, `db_counts`, `set_active_model`, `query_dates`, `match_results`, `run_inference_batch`, `dedup_horses`, `backfill_workouts`, `compute_speed_figures`, `normalize_figures`, `backfill_trip_flags`, `load_workouts_from_s3`, `health`

---

# 6. Infrastructure Inventory

## 6.1 Lambda functions (Image package type)

| Name | Memory | Timeout | Last modified |
|---|---|---|---|
| `equine-ingestion` | 2048 | 900 | 2026-05-02 (currently INACTIVE — image deleted from ECR) |
| `equine-inference` | 1024 | 300 | 2026-05-02 |
| `equine-wr-inference` | 1024 | 300 | 2026-05-02 |
| `equine-pl-inference` | 1024 | 300 | 2026-05-02 |
| `equine-ls-inference` | 1024 | 300 | 2026-05-02 |
| `equine-feature-engineering` | 512 | 300 | 2026-05-02 |
| `equine-results` | 512 | 300 | 2026-05-02 |
| `equine-nyra-workouts` | 512 | 300 | 2026-04-27 |

8 Lambdas. All `PackageType=Image` (Docker images via ECR).

## 6.2 ECS / Fargate

- **Cluster:** `equine-cluster`
- **Task definition families (active):** `equine-training-daily-full` (revisions 1–8), `equine-training-manual` (rev 1), `equine-training-pl` (rev 1)
- **No long-running services.** Tasks are run on demand via EventBridge `RunTask` targets.
- **Image (current):** `584812014683.dkr.ecr.us-east-1.amazonaws.com/equine-training:clean-data-lean53-core-1777504361`

## 6.3 S3 buckets

| Bucket | Created | Contents |
|---|---|---|
| `equine-raw-data` | 2026-03-15 | `charts/` (Equibase PDFs by track), `laptop-runs/`, `workout-loads/` |
| `equine-processed-data` | 2026-03-15 | (empty/unused at top level) |
| `equine-model-artifacts` | 2026-03-15 | Per-model subdirs: `ensemble/`, `gonzo_sauce/`, `longshot/`, `models/`, `pl/`, `ranker/`, `trajectory/`, `win_prob/`, `wr/` — JSON model files + calibration sidecars |
| `equine-frontend` | 2026-03-15 | React build (`index.html`, `static/`, `asset-manifest.json`, etc.) |

## 6.4 ECR repositories

| Repository | Purpose |
|---|---|
| `equine-training` | Training container (used by ECS Fargate tasks) |
| `equine-nyra-workouts` | NYRA workout scraper Lambda image |
| `equine-equibase-acquisition` | Latest tag `optiona2-1777339857` (2026-04-27); appears tied to `equibase_probe/` exploratory work — not in current production wiring |
| `cdk-hnb659fds-container-assets-584812014683-us-east-1` | CDK-managed bucket for Lambda container images. **Currently has only 5 images; the tag `equine-ingestion` references is no longer present (cleanup likely from lifecycle policy)** |

## 6.5 API Gateway v2

- **API ID:** `gb5qlfy10h`
- **Endpoint:** `https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com`
- **Name:** `equine-api`
- **No CloudFront distribution found with `equine` in Comment** — frontend served directly from S3 OR via a CF distribution whose Comment doesn't match grep
- **Routes (41 distinct):**
  - **Shared:** `GET /health`, `GET /races/today`, `GET /races/available-dates`, `GET /races/{date}`, `GET /races/{raceId}/detail`, `GET /cards/{date}/{track_code}`, `GET /horses/{horse_id}/pps`, `GET /dashboard/metrics`
  - **Generic predictions:** `GET /predictions/today`, `GET /predictions/{date}`, `GET /predictions/{date}/{track_code}/{race_number}`, `GET /predictions/value`, `GET /predictions/run`, `POST /predictions/run`
  - **WR:** `GET /wr/health`, `GET /wr/predictions/today`, `GET /wr/predictions/{date}`, `GET /wr/predictions/{date}/{track_code}/{race_number}`, `GET /wr/predictions/{date}/compare`, `GET /wr/predictions/value`, `GET /wr/predictions/run`, `POST /wr/predictions/run`, `GET /wr/predictions/track-record`, `GET /wr/predictions/track-record-by-style`
  - **PL:** `GET /pl/health`, `GET /pl/predictions/today`, `GET /pl/predictions/{date}`, `GET /pl/predictions/{date}/{track_code}/{race_number}`, `GET /pl/predictions/value`, `GET /pl/predictions/run`, `POST /pl/predictions/run`, `GET /pl/predictions/track-record`
  - **LS:** `GET /ls/health`, `GET /ls/predictions/today`, `GET /ls/predictions/{date}`, `GET /ls/predictions/{date}/{track_code}/{race_number}`, `GET /ls/predictions/longshots`, `GET /ls/predictions/alerts`, `GET /ls/predictions/run`, `POST /ls/predictions/run`, `GET /ls/predictions/track-record`

## 6.6 SNS / SQS / DynamoDB

- **SNS topic:** `equine-equalizer-alerts` (1 topic, no subscribers verified)
- **SQS:** None
- **DynamoDB:** None (all DDB tables on the account belong to other projects)

## 6.7 Secrets Manager

| Secret name | Notes |
|---|---|
| `equine-equalizer/db-credentials` | Aurora cluster credentials (ARN `...secret:equine-equalizer/db-credentials-7CD7Mt`) |
| `equine-equalizer/2captcha-api-key` | Stored, but **no code references** found in `backend/`, `model/`, or `scripts/` |
| `equine-equalizer/brightdata-api-key` | Stored, but **no code references** found |

## 6.8 CDK stacks (`infrastructure/cdk/lib/`)

4 stacks:
- `StorageStack` — 4 S3 buckets
- `DatabaseStack` — Aurora cluster + Secrets Manager
- `ComputeStack` — 7 named Lambda functions (`ingestionFn`, `featureEngineeringFn`, `inferenceFn`, `resultsFn`, `wrInferenceFn`, `plInferenceFn`, `lsInferenceFn`), VPC, EventBridge rules, API Gateway v2
- `FrontendStack` — frontend bucket policy, presumably CloudFront

`ComputeStack` imports: `aws-lambda`, `aws-events`, `aws-events-targets`, `aws-apigatewayv2`, `aws-apigatewayv2-integrations`, `aws-ec2`, `aws-s3`, `aws-rds`, `aws-ecs`, `aws-logs`, `aws-iam`.

---

# 7. Frontend Inventory

`frontend/src/` (React 19 + TypeScript + Create-React-App via `react-scripts`).

## 7.1 Pages (`frontend/src/pages/`)

9 page components:
- `TodayPage.tsx` — main race card view
- `GonzoPage.tsx` — gonzo_sauce style view
- `ComparePage.tsx` — head-to-head model comparison
- `BetBuilderPage.tsx` — bet construction UI
- `ValuePlaysPage.tsx` — PL value bet surfacing
- `LongshotPage.tsx` — LS alerts/longshots
- `PerformancePage.tsx` — model track record
- `HistoryPage.tsx` — historical predictions
- `DashboardPage.tsx` — `/dashboard/metrics` consumer

## 7.2 Components (`frontend/src/components/`)

13 components, organized by domain:
- `Common/`: `EmptyState.tsx`, `LoadingSpinner.tsx`, `PredictionOutcome.tsx`, `TrackRecordBanner.tsx`
- `Compare/`: `ByStyleTable.tsx`, `CompareHorseRow.tsx`, `CompareRaceCard.tsx`, `StyleSelector.tsx`
- `Layout/`: `Header.tsx`, `Layout.tsx`
- `RaceCard/`: `BetBadge.tsx`, `HorseRow.tsx`, `RaceCard.tsx`
- `Stats/`: `ModelStats.tsx`
- `ValuePlays/`: `ValuePlayCard.tsx`

## 7.3 API client

Single file: `frontend/src/api/client.ts`. Uses `axios` with `BASE_URL` falling back to:
1. `process.env.REACT_APP_API_URL`
2. `localhost:3001` if hostname is `localhost`
3. `https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com` otherwise

Exports per-domain functions: `getAvailableDates`, `getHorsePPs`, `getDashboardMetrics`, `getWRRacesToday`, `getWRRacesByDate(date, style)`, etc.

## 7.4 State management

No external state library (no Redux, Zustand, Recoil, React Query, SWR in `package.json` dependencies). State is local React state + axios calls inline.

## 7.5 Routing

`react-router-dom` v7 (`BrowserRouter` + `Routes` + `Route`).

## 7.6 Build / deploy

- **Build:** `npm run build` (CRA)
- **Deploy:** `scripts/deploy-frontend.sh` syncs `build/` to `s3://equine-frontend` and invalidates CloudFront distribution `E3KVZ579NXFT4Q` (per `deploy_all.sh`)
- **CloudFront ID stored locally:** `.cf-distribution-id` file
- **Bucket name stored locally:** `.frontend-bucket` file

## 7.7 Dependencies (selected)

`axios ^1.13.6`, `date-fns ^4.1.0`, `react ^19.2.4`, `react-dom ^19.2.4`, `react-router-dom ^7.13.1`, `react-scripts 5.0.1`, `recharts ^3.8.0`, `typescript ^4.9.5`.

---

# 8. Feature Engineering Inventory

## 8.1 FE locations

| File | Lines | Train/Inf | Categories | Approx feature count |
|---|---|---|---|---|
| `model/shared/feature_definitions.py` | 401 | TRAINING (authoritative) | speed (11), pace (6), trip (8), trainer (5), workout (8), class (7), physical (10), equipment (5), odds (3), jockey (3) | **66** base; `get_core_features()` returns 58 (no workouts); `get_odds_blind_features()` returns 63; `get_lean53_features()` returns 53; `get_gonzo_sauce_features()` returns 67 |
| `model/features/feature_definitions.py` | 159 | UNCLEAR | `FEATURE_GROUPS` dict with `speed`, `pace`, `workouts`, etc. — **different field names** (`beyer_*`, `raw_speed_*` instead of `speed_fig_*`) | Header says "should be 73" but `ALL_FEATURES = []` is empty. **Possibly orphan or partially-deprecated.** Imported by `model/training/train.py`. |
| `model/shared/data_loader.py` | 889 | TRAINING | All categories — pulls from Aurora, computes 66 base features + 14 Gonzo features, applies par-time defaults | 66 + 14 |
| `model/shared/gonzo_features.py` | 569 | BOTH (single source of truth per its own docstring) | Speed (4), Trajectory (7), Class (3) — total 14 Gonzo Sauce features | 14 |
| `model/shared/par_times.py` | 161 | BOTH | Computes workout par-time medians keyed by surface/distance — feeds noteworthy-workout features | (helper) |
| `model/shared/specialists.py` | 173 | TRAINING | Specialist eligibility filters (sprint/route/closer/etc.) | (filter logic) |
| `model/training/compute_speed_figures.py` | 529 | TRAINING (one-shot pipeline) | Computes `computed_speed_figure` and writes back to `past_performances` | (no FE cols added) |
| `backend/services/feature_engineering_service.py` | 1,211 | INFERENCE | Same feature names as `data_loader.py`; explicit comment: "All feature computations MUST match `model/shared/data_loader.py` EXACTLY. data_loader.py is the source of truth." | 63 (odds-blind WR) / 66 (full) / +14 (Gonzo) |

## 8.2 Train/inference duplication (explicitly acknowledged in code)

`backend/services/feature_engineering_service.py` lines 25-33:
```python
# ── Constants matching model/shared/data_loader.py ──
LAYOFF_BUCKETS = [
    (0, 14, 1), (14, 28, 2), (28, 60, 3),
    (60, 120, 4), (120, 9999, 5),
]

TRAINER_DEFAULTS = { ... }  # matching data_loader.py
```

`gonzo_features.py` is the only module imported by BOTH paths. Its docstring states:
> "This module is the single source of truth for the 14 Gonzo Sauce features. NO duplication of computation logic between training and inference. Drift here = silent calibration bugs (per session learning post-Bug #15 — three distinct bugs this week traced to code-path drift between training and inference)."

The remaining ~52 base features have implementations in BOTH `model/shared/data_loader.py` and `backend/services/feature_engineering_service.py`. The two implementations are intentionally kept in lockstep via shared constants imports + manual review.

## 8.3 Feature lists as stored per-model in registry

Each `model_versions` row carries a `feature_list` JSONB column. The active `rk_full_gonzo_sauce_20260502_0452` has 67 features in its list (53 lean53 + 14 Gonzo). Models can therefore be re-loaded with their exact training feature schema even if the codebase drifts.

## 8.4 RANKER_FULL_CULL (lean53 cull list)

`model/shared/feature_definitions.py` defines `RANKER_FULL_CULL: tuple[str, ...]` listing 13–15 features dropped from `rk_full` only (other models keep all 66). Documented Phase 1 (2026-04-28) ablation. Both train and inference import `RANKER_FULL_CULL` and `get_ranker_full_features()` from this single source.

---

# 9. External Dependencies

## 9.1 Active integrations

### Horse Racing Nation (HRN) — `horseracingnation.com`
- **Code:** `backend/services/data_sources/hrn_scraper.py` (974 lines), `backend/services/data_sources/hrn_workout_scraper.py` (454 lines)
- **Purpose:** primary data source for entries, results, workouts. Free, public access.
- **Tech:** `playwright-stealth` (entries), `requests` + `BeautifulSoup` (workouts/results page)
- **Track slug map:** explicit dict for ~11 qualifying tracks (CD, SAR, KEE, BEL, SA, GP, DMR, OP, MTH, AQU, PIM)
- **Known issues:**
  - Bug #28 (newly identified 2026-05-03): off-by-one cell indexing in payout extraction since 2026-04-30 — `win_payout` and `daily_double_payout` NULL for all results

### Equibase — `equibase.com`
- **Code (production):** `backend/services/chart_parser.py` (1,372 lines) — parses already-uploaded PDFs from `s3://equine-raw-data/charts/`
- **Code (exploratory):** `equibase_probe/` directory — 4 separate playwright-stealth probe scripts attempting to bypass Imperva bot protection. Standalone Dockerfiles (`Dockerfile.optiona2`, `Dockerfile.optionb`, `Dockerfile.optiond`).
- **ECR image:** `equine-equibase-acquisition` (latest tag `optiona2-1777339857`, pushed 2026-04-27)
- **Status:** No automated Equibase-to-S3 pipeline. PDFs land in S3 by an unidentified external process (likely manual or scheduled task outside CDK).
- **Direct fetch attempted via WebFetch on 2026-05-03:** all standard URL patterns returned HTTP 403 (Imperva block).

### NYRA — `nyra.com` (via `equine-nyra-workouts` Lambda)
- **Code:** `backend/lambdas/nyra-workouts/handler.py` (358 lines)
- **Purpose:** Free public workout pages for SAR, BEL, AQU
- **Pipeline:** scrape → write JSON to S3 → invoke `equine-ingestion` `load_workouts_from_s3` action

## 9.2 Listed but not (yet) integrated

Per `backend/services/data_sources/README.md`:
> "Future Options: TheRacingAPIClient — paid, cleaner data; BRISFileReader — reads purchased PP files; EquibaseDirectScraper — deeper PP data."

## 9.3 Stored credentials with no code consumers

- `equine-equalizer/2captcha-api-key` — Stored in Secrets Manager. `grep -r "2captcha"` over `backend/`, `model/`, `scripts/` returns 0 hits. Likely planned for solving Imperva captchas in `equibase_probe/` work.
- `equine-equalizer/brightdata-api-key` — Same pattern. Likely planned for residential-proxy bypass on Equibase scraping.

## 9.4 Searched and NOT present

- **DRF / Daily Racing Form**: 0 references in `backend/`, `model/`, `scripts/`
- **pybaseball / Statcast**: 0 references (despite Tony's prior mention of a planned Statcast pipeline)
- **TwinSpires / TVG**: 0 references
- **DD app integration**: 0 references

## 9.5 Python library dependencies (production)

From `Dockerfile.ingestion`: `psycopg2-binary 2.9.9`, `boto3 1.34.0`, `xgboost 2.0.3`, `pandas 2.1.4`, `numpy 1.26.3`, `scikit-learn 1.3.2`, `scipy 1.11.4`, `beautifulsoup4 4.12.3`, `requests 2.31.0`, `lxml 4.9.3`. (Other Lambda Dockerfiles use a similar set; LS Lambda adds `torch` for the LSTM.)

---

# 10. Open Architectural Inconsistencies

(Listed as observations only. No judgment, no recommendations.)

1. **Two `feature_definitions.py` files with different feature schemas.** `model/shared/feature_definitions.py` (66 features, names like `speed_fig_last`) is imported by all production training/inference paths. `model/features/feature_definitions.py` (described in header as 73 features but `ALL_FEATURES = []` is empty) is imported by `model/training/train.py`. Field naming conventions differ (`speed_fig_*` vs `beyer_*` / `raw_speed_*`).

2. **Feature engineering implemented in two places.** `model/shared/data_loader.py` (training) and `backend/services/feature_engineering_service.py` (inference) compute the same 52 base features independently, with cross-references in code comments noting "must match exactly." Only the 14 Gonzo Sauce features are factored to a single shared module (`model/shared/gonzo_features.py`).

3. **Multiple "active" model versions per type.** Registry has 45 `is_active=TRUE` rows. For example, multiple `wp_core_lean53_*` entries are simultaneously active across general + 6 specialists. `get_active_model_by_type` resolution logic is in `repositories/model_version_repository.py`.

4. **Calibration is BYPASSED at inference** for all styles per code comment in `wr_inference_service.py:617-628`:
   > "All styles (including gonzo_sauce) bypass calibration at inference tonight. Original Phase A3 plan was to apply gonzo's fitted ranker calibration here, but that surfaced Bug #24..."
   Calibration sidecars exist in S3 for `gonzo_sauce` but are not loaded into the inference path.

5. **`ls_predictions` is partially orphaned.** Per code comment in `ls_prediction_repository.py:191-205`:
   > "LS data is written as second-pass enrichment to wr_predictions columns (ensemble_win_prob, longshot_prob, trajectory_score, angle_*, longshot_alert, confidence) — not to a separate ls_predictions table."
   Migration 010 (2026-05-01) added columns to `ls_predictions` to support first-class writes, but reads still go through `wr_predictions` enrichment columns.

6. **WR `style=general` and `style=gonzo_sauce` produced identical top picks for all 12 CD races on 2026-05-02** (verified via API probe). Win probabilities differ at the 4th decimal place. The user-facing differentiation between the two styles is not visible at the rank=1 level for that day's data.

7. **Per-horse `model_used` field** in API responses (`'core'` / `'full'`) is internal feature-routing metadata, NOT a model variant selector. The rank values within `model_used` subsets do not represent a coherent ranking; the global `predicted_rank` is the only well-defined ordering.

8. **`predictions` legacy table** exists alongside `wr_predictions` / `pl_predictions` / `ls_predictions`. Schema is similar to `wr_predictions`. Migration 005 introduced the split tables; the legacy `predictions` table was not dropped.

9. **`equine-feature-engineering` Lambda is a stub**: `# TODO: Wire to feature_engineering_service when implemented`. The cron `equine-feature-engineering-daily` is DISABLED.

10. **Two migration files numbered `005`** (`005_backfill_pace_delta.sql` and `005_three_prediction_tables.sql`). Migration ordering depends on `migrate.py` runner logic.

11. **No Equibase-to-S3 fetcher in production codebase.** `parse_charts` reads existing S3 PDFs. PDFs arrive in S3 by an unidentified mechanism; recent dates (2026-04-30 onward) are not present.

12. **Stored 2captcha + brightdata API keys with no code consumers** (Section 9.3).

13. **`equibase_probe/` directory contains 4 distinct probe scripts** (`probe.py`, `option_a2_probe.py`, `option_b_probe.py`, `option_d_probe.py`) with their own Dockerfiles. Exploratory Imperva-bypass research, not wired into production pipelines.

14. **`equine-ingestion` Lambda is currently INACTIVE.** ECR has only 5 images in the `cdk-hnb659fds-container-assets` repo; the tag the Lambda config references is no longer present (likely culled by an ECR lifecycle policy). State: `Inactive`, reason: "The function is trying to use a deleted image."

15. **TODOs in code:**
    - `backend/lambdas/feature-engineering/handler.py:16` — Wire to feature_engineering_service
    - `backend/services/ingestion_service.py:161` — Implement after receiving Equibase 2023
    - `backend/services/evaluation_service.py:144,155,172,188` — 4 TODOs for evaluation/post-trained-model functions

16. **Routers expose `def get_*` / `def post_*` functions** rather than FastAPI/Flask decorators. Routing is one layer up at API Gateway → specific Lambda → specific function.

17. **`raw_query` action is documented "diagnostic only"** but has been the primary DB-access path for ad-hoc analysis (since the public API is curated). No SELECT-only enforcement beyond `if not sql.strip().upper().startswith('SELECT')`.

---

# 11. Recent Major Changes (last 30 days)

`git log --since="30 days ago"` returns **EMPTY**. All commits in the repo's git history are dated **2026-03-15** (10 commits, single day, the initial-commit batch).

```
2a3d758 2026-03-15 Widen VARCHAR columns and isolate per-race DB connections
d93c4c4 2026-03-15 Fix post_time TIMESTAMPTZ, race_type length, and connection isolation
3185103 2026-03-15 Race quality tier feature, MIN_CLAIMING_PRICE to $15k, deploy scraper
e3a38ab 2026-03-15 Fix HRN scraper to match actual HTML structure
fbf2d95 2026-03-15 Add modular data source layer
9bfef12 2026-03-15 Add missing API routes, fix CORS config
1aff393 2026-03-15 Migrations complete, ingestion handler with action routing
fd681e4 2026-03-15 Fix ESLint warnings, deploy script improvements, Docker Lambda packaging
8d68f13 2026-03-15 Add deployment scripts
0bb2a6d 2026-03-15 Initial commit — complete Equine Equalizer application
```

**Tony deploys directly without committing.** All architectural changes since 2026-03-15 are visible only via file mtimes.

## 11.1 Recently modified files (proxy for change activity)

Backend (most recent):
- `backend/services/feature_engineering_service.py` — 2026-05-02 01:03 (42,932 bytes)
- `backend/services/wr_inference_service.py` — 2026-05-02 01:45 (35,565 bytes)
- `backend/routers/ls_prediction_router.py` — 2026-05-02 01:47
- `backend/routers/wr_prediction_router.py` — 2026-05-02 01:47
- `backend/routers/race_router.py` — 2026-05-02 07:52
- `backend/repositories/wr_prediction_repository.py` — 2026-05-02 07:53
- `backend/repositories/ls_prediction_repository.py` — 2026-05-02 09:31
- `backend/models/canonical.py` — 2026-05-02 10:41
- `backend/repositories/pl_prediction_repository.py` — 2026-05-02 10:41
- `backend/routers/pl_prediction_router.py` — 2026-05-02 10:42

Model:
- `model/shared/gonzo_features.py` — 2026-05-02 01:19 (21,862 bytes)
- `model/shared/data_loader.py` — 2026-05-01 22:44 (34,266 bytes)
- `model/win_prob/train.py` — 2026-05-01 22:40
- `model/ranker/train.py` — 2026-05-01 23:54
- `model/shared/feature_definitions.py` — 2026-05-01 20:21

Migrations:
- Migration 010 (`010_ls_predictions_first_class.sql`) — references "Tony's revised architecture (2026-05-01)"
- Migration 011 (`011_wr_predictions_unique_fix.sql`) — most recent

## 11.2 Visible architecture in flux

Based on file mtimes + code comments:
- **Phase A3** (2026-05-01..02): Gonzo Sauce features added (`gonzo_features.py`, gonzo_sauce model variants), par-time computation, Bug #15 calibration workstream
- **Phase A3.5** (planned, not landed): Bug #24 (calibration + 0-PP horses), Bug #25 (LS alert formula for thin-PP-history)
- **LS first-class promotion** (2026-05-01): migration 010
- **lean53 feature cull** (2026-04-28): per `RANKER_FULL_CULL` comment

## 11.3 Visible architecture as settled

- **Stack split into 4 services × 3 inference Lambdas** — settled since March
- **CDK 4-stack layout** — settled since March
- **Public API surface (41 routes)** — actively evolving (router files modified 2026-05-02) but URL pattern is stable

---

# 12. Outstanding Bugs

Searched code for `Bug #` references; cross-referenced session memory.

| ID | Status | Location | Severity | Phase | Description |
|---|---|---|---|---|---|
| **#15** | partially fixed | `backend/services/wr_inference_service.py:124-126`, `model/shared/gonzo_features.py:9` | HIGH | Phase A3 (gonzo_sauce only) | Calibration bypass from train/inference code-path drift. "Three distinct bugs this week traced to code-path drift between training and inference." Gallery-wide fix workstream not yet landed. Gonzo's fix path is the documented workaround. |
| **#24** | open | `backend/services/wr_inference_service.py:617-628` | HIGH | Phase A3.5 | Isotonic calibration of legitimate-PP horses' ranker_probs maps them to ≈ 0; 1/field_size override for 0-PP horses then dominates after renormalize → 0-PP horses become top picks (e.g., "Wonder Dean JPN at #1 in Derby smoke test"). Workaround: ALL styles bypass calibration at inference. Calibration sidecar remains in S3 for A3.5 use. |
| **#25** | open | `backend/repositories/ls_prediction_repository.py:195` | MEDIUM | Phase A3.5 | LS strict AND alert formula (with `traj_score>0`) fails for thin-PP-history 3yo fields; "Derby Day produces zero alerts on CD." A3.5 will fix the alert formula upstream. |
| **#28** | NEW (2026-05-03) | `backend/services/data_sources/hrn_scraper.py:802` (`parse_payout(1/2/3)` calls) | HIGH | not yet scoped | HRN scraper off-by-one column shift since 2026-04-30. HRN page structure changed (likely added an icon column). Result: `win_payout` and `daily_double_payout` NULL across all rows from 4/30 onward. `place_payout` stores Win values, `show_payout` stores Place values. Documented in `equine-equalizer-bug-28-hrn-scraper.md` memory file. Backfill via `fetch_results` re-run after fix. |

Bugs #7 and #20–#23, #26, #27 referenced in Tony's task spec were searched in code (`grep -r "Bug #"`) and **no matches found**. They may exist in:
- Session logs (`docs/sessions/SESSION_*.md`) — not searched in this dump
- Tony's external bug tracker
- Verbal/Slack-only history

The 4 above are the only `Bug #` references currently visible in code.

---

# Appendix: Investigation Limits

- **`equine-ingestion` Lambda is INACTIVE** at time of this dump (image deleted from ECR; CDK redeploy requires Docker, which is not running in this WSL distro). Direct DB queries via `raw_query` action were not possible. DB schema inventory is from `schema.sql` + migration files. Row counts are estimated from public API endpoints.
- **Git history covers only 2026-03-15.** Recent change activity inferred from file mtimes and code comments referencing Phases A3 / A3.5 / dates.
- **`docs/sessions/` directory was not read.** SESSION_*.md files may contain additional bug history, decision logs, and architectural rationale.
- **Frontend page contents were not opened beyond top-level imports.** Per-page state-management decisions and component prop interfaces not catalogued.
- **CDK stack contents beyond imports were not inspected** — IAM policy specifics, EventBridge rule targets, Lambda environment variables not enumerated.
- **No DB migrations were validated against actual current schema.** The 12-table schema described is the union of `schema.sql` and migrations 001–011 as written; actual production DB may differ if migrations were skipped, partially applied, or hand-edited.
