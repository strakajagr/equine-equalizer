# SESSION 002 — CDK Infrastructure
**Date:** 2026-03-15
**Model:** Opus 4.6
**Goal:** Build all four CDK stacks — storage, database, compute, frontend

---

## Stacks Created

### 1. StorageStack (`lib/storage-stack.ts`)
Four S3 buckets:
| Bucket | Purpose | Key Config |
|--------|---------|------------|
| `equine-raw-data` | Raw PP files from Equibase | Versioned, private, Glacier after 90 days |
| `equine-processed-data` | Feature-engineered datasets | Versioned, private |
| `equine-model-artifacts` | Trained XGBoost model files | Versioned, private (rollback capability) |
| `equine-frontend` | React static build output | Private (CloudFront serves via OAI) |

All bucket ARNs and names exported as CloudFormation outputs.

### 2. DatabaseStack (`lib/database-stack.ts`)
| Resource | Purpose |
|----------|---------|
| **VPC** | Dedicated network with 2 AZs — public + private subnets |
| **Aurora Serverless v2 PostgreSQL 15.4** | Database: `equine_equalizer`, 0.5–4 ACUs |
| **Secrets Manager secret** | Auto-generated credentials (`equine-equalizer/db-credentials`) |
| **DB Security Group** | Inbound port 5432 from Lambda SG only |
| **Lambda Security Group** | Attached to all Lambda functions, outbound-all |

**Why private subnets for the database:**
Aurora is placed in `PRIVATE_WITH_EGRESS` subnets, meaning it has no public IP and cannot be reached from the internet. Only resources in the same VPC with the correct security group (i.e., the Lambda functions) can connect on port 5432. This is defense in depth — even if credentials leak, the database is not network-reachable from outside the VPC.

**Secrets Manager for credentials:**
Database password is auto-generated and stored in Secrets Manager (never hardcoded). Lambdas read the secret ARN at runtime to connect. Supports automatic rotation.

### 3. ComputeStack (`lib/compute-stack.ts`)
**Four Lambda Functions (Python 3.11):**
| Function | Memory | Description |
|----------|--------|-------------|
| `equine-ingestion` | 512 MB | Pulls daily race entries and PP data |
| `equine-feature-engineering` | 512 MB | Transforms raw PP data into model features |
| `equine-inference` | 1024 MB | Loads model artifact, runs predictions |
| `equine-results` | 512 MB | Ingests race results for model evaluation |

All Lambdas: 5-min timeout, VPC-attached (same VPC as DB), env vars for DB_SECRET_ARN and all bucket names.

**IAM Permissions:**
- All: read DB secret from Secrets Manager
- Ingestion: read/write `equine-raw-data`
- Feature Engineering: read `equine-raw-data`, read/write `equine-processed-data`
- Inference: read `equine-model-artifacts` + `equine-processed-data`
- Results: read `equine-raw-data`, read/write `equine-processed-data`

**EventBridge Cron Schedule (daily pipeline):**
| UTC Time | ET Time | Rule | Target |
|----------|---------|------|--------|
| 11:00 AM | 6:00 AM | `equine-ingestion-daily` | equine-ingestion |
| 12:00 PM | 7:00 AM | `equine-feature-engineering-daily` | equine-feature-engineering |
| 12:30 PM | 7:30 AM | `equine-inference-daily` | equine-inference |
| 4:00 AM | 11:00 PM (prev day) | `equine-results-daily` | equine-results |

**HTTP API Gateway (`equine-api`):**
| Route | Lambda | Purpose |
|-------|--------|---------|
| `GET /races/today` | equine-inference | Today's predictions |
| `GET /races/{date}` | equine-inference | Predictions for a specific date |
| `GET /races/{raceId}/detail` | equine-inference | Single race detail |
| `GET /health` | equine-inference | Health check |

### 4. FrontendStack (`lib/frontend-stack.ts`)
| Resource | Purpose |
|----------|---------|
| **Origin Access Identity** | Lets CloudFront read from the private S3 bucket |
| **CloudFront Distribution** | HTTPS-only, cache-optimized, SPA error handling (403/404 → index.html) |

CloudFront distribution URL exported as output.

## Stack Dependency Order
```
StorageStack ──┬──→ ComputeStack
DatabaseStack ─┘
StorageStack ────→ FrontendStack
```

## AWS Services Introduced
| Service | Why |
|---------|-----|
| S3 | Object storage for data pipeline stages and frontend hosting |
| Aurora Serverless v2 | PostgreSQL database that scales to near-zero when idle |
| Secrets Manager | Secure credential storage for database password |
| VPC / Subnets / Security Groups | Network isolation for database |
| Lambda | Serverless compute for all backend logic |
| EventBridge | Cron-based scheduling for the daily data pipeline |
| API Gateway (HTTP) | Lightweight HTTP API to expose predictions to frontend |
| CloudFront | CDN for serving React frontend with HTTPS |

## Next Steps (Session 003+)
1. **Database schema** — Design and create tables: `horses`, `races`, `entries`, `predictions`, `results`, `model_runs`
2. **Lambda handler logic** — Implement actual ingestion, feature engineering, inference, and results handlers
3. **ML layer** — Bundle `requirements.txt` into a Lambda layer for pandas/numpy/xgboost
4. **Frontend scaffold** — Initialize Vite/React project with basic routing
