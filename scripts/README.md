# Equine Equalizer — Deployment Scripts

## First-Time Setup (run in this order)

### 1. Deploy AWS Infrastructure
```bash
./scripts/deploy-backend.sh --bootstrap
```
The `--bootstrap` flag is only needed once per AWS account/region. After that:
```bash
./scripts/deploy-backend.sh
```

### 2. Deploy Frontend
```bash
./scripts/deploy-frontend.sh
```
Automatically reads API URL from CDK outputs.

### 3. Run Database Migrations
```bash
# Local development
export DATABASE_URL=postgresql://...
./scripts/run-migrations.sh --local --seed

# AWS (via Lambda)
./scripts/run-migrations.sh --seed
```

### 4. Load Historical Data
Once Equibase 2023 dataset is downloaded:
```bash
./scripts/backfill.sh \
  --data-dir ~/Downloads/equibase-2023
```

### 5. Train First Model
```bash
# Train and review metrics
./scripts/train-model.sh

# If metrics look good, activate
./scripts/train-model.sh --activate
```

## Ongoing Deployments

### Backend changes (Lambda code)
```bash
./scripts/deploy-backend.sh
```

### Frontend changes (React UI)
```bash
./scripts/deploy-frontend.sh
```

### Retrain model
```bash
./scripts/train-model.sh \
  --version v1.1 \
  --activate
```

## Daily Pipeline (automated)
EventBridge runs automatically:
- 6:00 AM ET  — Data ingestion
- 7:00 AM ET  — Feature engineering
- 7:30 AM ET  — Model inference
- 11:00 PM ET — Results ingestion

No manual intervention needed once deployed.
