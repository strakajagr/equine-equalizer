# SESSION 001 — Project Scaffolding
**Date:** 2026-03-15
**Model:** Sonnet 4.6
**Goal:** Stand up the bare directory structure and placeholder files for equine-equalizer

---

## What Was Built

Complete project skeleton with placeholder files (single-comment stubs) across five top-level domains:

| Area | Files Created |
|------|--------------|
| `infrastructure/cdk/` | `bin/app.ts`, `lib/storage-stack.ts`, `lib/database-stack.ts`, `lib/compute-stack.ts`, `lib/frontend-stack.ts`, `package.json`, `tsconfig.json` |
| `backend/lambdas/` | `ingestion/handler.py`, `feature-engineering/handler.py`, `inference/handler.py`, `results/handler.py` |
| `backend/layers/` | `ml-dependencies/requirements.txt` |
| `backend/shared/` | `db.py`, `constants.py` |
| `model/` | `training/train.py`, `features/feature_definitions.py`, `evaluation/metrics.py` |
| `frontend/src/` | `App.tsx`, empty `components/` and `pages/` directories |
| `data/` | empty `raw/` and `processed/` directories |

No packages installed. No application logic written.

---

## Project Purpose

**Equine Equalizer** is a horse racing prediction system that:

1. **Ingests** race data from external sources into S3/PostgreSQL
2. **Engineers features** from raw data (horse form, jockey stats, track conditions, etc.)
3. **Runs ML inference** to rank horses by predicted finish probability before each race
4. **Scores results** after races to track model performance and ROI
5. **Presents predictions** via a React frontend with race-day dashboards

The system is fully serverless on AWS (Lambda + Aurora Serverless + S3 + CloudFront), orchestrated via CDK.

---

## Intended Next Steps (Session 002+)

1. **Infrastructure** — Fill in real CDK stacks: S3 buckets, Aurora cluster, Lambda functions with layers, EventBridge schedule, API Gateway
2. **Database schema** — Design tables: `horses`, `races`, `entries`, `predictions`, `results`, `model_runs`
3. **Data source** — Identify and integrate a race data API (e.g., Equibase, Racing Reference, or a scrape target)
4. **Feature definitions** — Define initial feature set: speed ratings, class drops, trainer/jockey combos, days since last race, surface/distance fit
5. **Training pipeline** — Wire `train.py` to pull processed data, train an initial XGBoost ranker, push artifact to S3
6. **Inference pipeline** — Wire inference Lambda to load artifact and score upcoming entries
7. **Frontend skeleton** — Scaffold Vite/React app with a race card view and prediction display
