# SESSION 003 — Repositories, Services, Routers, Lambda Handlers
**Date:** 2026-03-15
**Model:** Opus 4.6
**Goal:** Build the full backend layer stack: remaining repositories, service stubs, routers, Lambda handler wiring, and ML dependencies

---

## Repositories Built

| Repository | Methods | Role |
|-----------|---------|------|
| `workout_repository.py` | 7 | Workout CRUD, bullet work queries, speed index derivation |
| `prediction_repository.py` | 9 | Prediction CRUD, top picks, value plays, model performance aggregation |
| `result_repository.py` | 5 | Result CRUD, date range queries for evaluation |
| `model_version_repository.py` | 6 | Model lifecycle: insert, activate, deactivate, update metrics |

**Cumulative repository method count: 61** across 9 repository files (including 5 from prior session).

---

## Service Stubs

| Service | Methods | Responsibility |
|---------|---------|---------------|
| `ingestion_service.py` | 4 | Fetch external data, parse Equibase files, persist race cards, backfill historical |
| `feature_engineering_service.py` | 8 | Build ~70 feature matrix: speed, pace, workout, trainer/jockey, class, equipment, physical |
| `inference_service.py` | 5 | Load model from S3, predict races, rank fields, flag value plays, recommend exotics |
| `evaluation_service.py` | 5 | Record results, calculate hit rates, compute exotic EV, trigger retraining |

All services are stub implementations (pass/TODO) — logic comes in future sessions when data source and training pipeline are confirmed.

### Value Flagging Placement (Critical Architecture Decision)
Value flagging (`flag_value()`) lives in `inference_service.py` and runs **after** `rank_field()`. The model ranks horses using only the ~70 feature matrix which is completely odds-blind. Morning line odds are never in the feature set. Only after ranking is complete does `flag_value()` compare model probabilities to morning line implied probabilities to identify overlays. Odds never influence the model's ranking — they only determine which already-ranked horses represent betting value.

---

## Routers

| Router | Functions | Routes |
|--------|-----------|--------|
| `race_router.py` | 3 + `_response` | `GET /races/today`, `GET /races/{date}`, `GET /races/{raceId}/detail` |
| `prediction_router.py` | 3 + `_response` + `_serialize_prediction` | `GET /predictions/today`, `GET /predictions/{date}`, `GET /predictions/value` |
| `health_router.py` | 1 | `GET /health` |

**Router pattern:** Pure passthrough. Routers parse the HTTP event, call a service or repository, serialize the result, and return. The only transformation allowed is `_serialize_prediction()` which converts dataclass to JSON-safe dict. No business logic lives in routers.

---

## Lambda Handler Wiring

| Lambda | Handler Logic |
|--------|--------------|
| `ingestion/handler.py` | Calls `IngestionService.fetch_daily_entries(today)` |
| `feature-engineering/handler.py` | Stub — will call `FeatureEngineeringService` |
| `inference/handler.py` | Path-based router: dispatches to `race_router`, `prediction_router`, or `health_router` |
| `results/handler.py` | Calls `EvaluationService.record_results(today)` |

The inference handler acts as a lightweight HTTP dispatcher since API Gateway routes all requests to this single Lambda. Routes are matched by string containment on `rawPath`.

---

## ML Dependencies (`requirements.txt`)

| Package | Version | Purpose |
|---------|---------|---------|
| `psycopg2-binary` | 2.9.9 | PostgreSQL driver for all Lambda DB access |
| `boto3` | 1.34.0 | AWS SDK for S3 (model artifacts) and Secrets Manager (DB credentials) |
| `xgboost` | 2.0.3 | Gradient boosted tree model for race prediction |
| `pandas` | 2.1.4 | Feature matrix construction and data manipulation |
| `numpy` | 1.26.3 | Numerical operations underlying pandas and xgboost |
| `scikit-learn` | 1.3.2 | Train/test splitting, calibration, preprocessing utilities |
| `scipy` | 1.11.4 | Statistical functions for feature engineering (z-scores, distributions) |

---

## Files Created/Updated This Session

**New files (16):**
- `repositories/workout_repository.py`
- `repositories/prediction_repository.py`
- `repositories/result_repository.py`
- `repositories/model_version_repository.py`
- `services/__init__.py`
- `services/ingestion_service.py`
- `services/feature_engineering_service.py`
- `services/inference_service.py`
- `services/evaluation_service.py`
- `routers/__init__.py`
- `routers/race_router.py`
- `routers/prediction_router.py`
- `routers/health_router.py`

**Updated files (5):**
- `lambdas/ingestion/handler.py`
- `lambdas/feature-engineering/handler.py`
- `lambdas/inference/handler.py`
- `lambdas/results/handler.py`
- `layers/ml-dependencies/requirements.txt`

---

## Backend Layer Architecture (Complete)

```
HTTP Request
  → API Gateway
    → Lambda (inference/handler.py)
      → Router (race_router / prediction_router / health_router)
        → Service (inference_service / evaluation_service)
          → Repository (prediction_repository / race_repository / etc.)
            → transforms.py (raw dict → canonical dataclass)
              → shared/db.py (connection + query execution)
                → PostgreSQL (Aurora Serverless v2)
```

Each layer only talks to the layer directly below it. No skipping layers.

---

## Next Steps (Session 004+)

1. **Feature engineering implementation** — Fill in all `compute_*` methods with actual feature calculations from past performance data
2. **XGBoost training pipeline** — `model/training/train.py` using historical data to train initial model
3. **Equibase data parsing** — Implement `parse_equibase_file()` after confirming 2023 dataset format
4. **Historical backfill** — Load 2023 Equibase dataset to populate DB for training
5. **Frontend scaffold** — Initialize Vite/React app with race card and prediction views
