# Equine CDK Infrastructure

CDK stacks for the Equine Equalizer project.

## Stacks

- **EquineStorageStack** — S3 buckets (raw data, processed data, model artifacts)
- **EquineDatabaseStack** — VPC + Aurora Serverless PostgreSQL
- **EquineComputeStack** — Lambdas, EventBridge schedules, API Gateway
- **EquineFrontendStack** — CloudFront + S3 hosting

## Deploy

### Substrate-pragmatic invocation pattern (WSL2 non-TTY env)

CDK CLI in WSL2/non-TTY environment requires explicit verbose-output env vars;
otherwise progress emission goes to TTY-only stream and silently suppresses
(exit 0 with zero stdout/stderr; Lambda code NOT updated). Substrate-validated
2026-05-18 per Tier 3 Track C investigation.

**Substrate-validated deploy pattern**:

```bash
cd infrastructure/cdk
JSII_DEBUG=1 npx cdk deploy EquineComputeStack --require-approval never
```

`JSII_DEBUG=1` forces JSII subprocess verbose logging, producing the
CloudFormation template generation output. Without it, default-env synth
silently runs and exits 0 without emitting progress or completing asset
rebuild.

### Alternative — direct ECR push (D.1.β fallback pipeline)

When CDK substrate-pragmatic-divergent or for hot-fix deploys:

```bash
cd <project root>
ECR_URI=584812014683.dkr.ecr.us-east-1.amazonaws.com/cdk-hnb659fds-container-assets-584812014683-us-east-1
TAG=<descriptive>-<short-commit-hash>

aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin 584812014683.dkr.ecr.us-east-1.amazonaws.com

docker buildx build --platform linux/amd64 \
    --provenance=false --sbom=false \
    -f Dockerfile.<lambda-name> \
    -t $ECR_URI:$TAG \
    --push .

aws lambda update-function-code \
    --function-name <lambda-name> \
    --image-uri $ECR_URI:$TAG \
    --publish

aws lambda wait function-updated --function-name <lambda-name>
```

**Important flags**:
- `--provenance=false --sbom=false`: Lambda requires Docker v2 manifest;
  buildx attestations produce OCI manifest list which Lambda rejects
- `--platform linux/amd64`: Lambda runs x86_64

**Risk**: D.1.β ECR tags don't match CDK asset hash naming. Subsequent
interactive CDK deploy MAY overwrite manual update (or detect no-change if
same content hash).

## Substrate-discovery — CDK silent-deploy root cause (Tier 3 Track C 2026-05-18)

Hypothesis testing outcomes:
- **H1** (TTY-detection): negative; `CI=false FORCE_COLOR=1` doesn't help
- **H2** (synth hang): partial; default-env synth hangs >180s
- **H10** (JSII_DEBUG): ✓ CONFIRMED — env var forces output emission
- **H11** (synth-to-file): exit 124 timeout at 180s default; substrate-pragmatic
  longer timeout required for cache-cold first run

Substrate-pragmatic conclusion: CDK CLI v2.1111.0 in WSL2 non-TTY env suppresses
progress output by default. JSII_DEBUG=1 is the substrate-validated workaround.

## Useful commands

- `npm run build` — compile typescript to js
- `npm run watch` — watch for changes and compile
- `npm run test`  — perform the jest unit tests
- `JSII_DEBUG=1 npx cdk deploy <stack>` — deploy with verbose output
- `JSII_DEBUG=1 npx cdk diff <stack>` — compare deployed vs current
- `JSII_DEBUG=1 npx cdk synth <stack>` — emit CFN template

## Stack architecture

See `bin/cdk.ts` for stack instantiation + dependencies.
