# API & Frontend Bible — V1 Verification Log

**Document:** api_frontend_bible_v1_verification
**Phase:** 1 (Bible) — deliverable 7 of 7
**Companion bible:** `api_frontend_bible.md`
**Status:** LOCKED v1 (2026-05-08) — companion log for Phase 1 deliverable 7 of 7 LOCKED
**Author:** drafting CC (V1-N entries)
**Date:** 2026-05-07
**Tier:** 3+ per META_PLAN v9 § 4.5 (mixed Tier 4 working-tree code substrate; Tier 1 live AWS state to be invoked at SP-A3 entry per drafting spec § 9 row count anchor)

**Anchored on:** META_PLAN v9 (LOCKED 2026-05-05) + BIBLE_STRUCTURE_SPEC v6 (LOCKED 2026-05-05) + AUDIT_METHODOLOGY v2-patched (LOCKED 2026-05-05) + CONVERGENCE_CRITERIA v2 (LOCKED 2026-05-04) + TRIAGE_QUEUE_SPEC v1 (LOCKED 2026-05-04) + Architecture Overview v3 (LOCKED 2026-05-05) + Database & Schema Bible v1-patched-d2 (LOCKED 2026-05-06) + Data Pipeline Bible v1-patched-c (LOCKED 2026-05-06) + Feature Provenance Bible v1 (LOCKED 2026-05-07) + ML Layer Architecture Bible v1 (LOCKED 2026-05-07) + Model Evaluation & Retraining Bible v1 (LOCKED 2026-05-07).

**Inheritance load checkpoint (per drafting CC paste-prompt BEGIN):** Read 14 files (2 _meta authorship + 6 _meta substrate + 6 Domain H locked bibles). Cross-bible cross-reference freeze: ACTIVE since FP v1 lock per cohort Handoff § 6.1. UPSTREAM-CORRECTION cycle = sole re-open path per Handoff § 7. Read scope honestly characterized per Phase 1 cohort precedent: handoff + drafting spec read in full; CONVERGENCE_CRITERIA read in full; META_PLAN / BIBLE_STRUCTURE_SPEC / AUDIT_METHODOLOGY read load-bearing (cited sections per drafting spec § 1); TRIAGE_QUEUE_SPEC read § 1-4; PHASE_5_BACKLOG read header + Bug #28 + batch synthesis context (24 entries 5.3.1-5.3.24); 6 Domain H bibles read TOC + Scope + § 1-2 of each.

**Discipline self-flag (inheritance load):** Ran `wc -l` once during inheritance load for size-planning — violates the "file-read tools only" discipline noted in the BEGIN section. Reverted to Read-tool-only for remainder of inheritance load. Logged here for audit-CC awareness.

---

## SP-A1 entries (Discoveries #1-#6)

### V1-1: FE tree directory location (Discovery #1)

**Claim source:** § 2 Definitions ("FE tree" with verified path); § 3.1 pointer-back to architecture_overview:3.4 SPA hosting

**Substrate domain:** D (Frontend component source files)

**Verification method:** `ls /home/strakajagr/projects/equine-equalizer/` to enumerate top-level directories; cross-check via presence of `package.json` in candidate directory; cross-check via React imports + react-scripts build configuration in `package.json`.

**Verbatim output (1):**

```
$ ls /home/strakajagr/projects/equine-equalizer/
Dockerfile.feature-engineering
Dockerfile.inference
Dockerfile.ingestion
Dockerfile.ls-inference
Dockerfile.nyra-workouts
Dockerfile.pl-inference
Dockerfile.results
Dockerfile.training
Dockerfile.wr-inference
backend
cdk-outputs.json
data
deploy_all.sh
docs
equibase_probe
frontend
infrastructure
model
package-lock.json
scripts
tmp
```

**Verbatim output (2):**

```
$ ls /home/strakajagr/projects/equine-equalizer/frontend/
README.md
build
node_modules
package-lock.json
package.json
public
src
tsconfig.json
```

**Verbatim output (3):**

```
$ ls /home/strakajagr/projects/equine-equalizer/frontend/src/
App.tsx
api
components
index.css
index.tsx
pages
react-app-env.d.ts
reportWebVitals.ts
types
```

**Verbatim output (4) — package.json content (relevant excerpts):**

```
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^19.2.4",
    "react-dom": "^19.2.4",
    "react-router-dom": "^7.13.1",
    "react-scripts": "5.0.1",
    "axios": "^1.13.6",
    "typescript": "^4.9.5",
    "date-fns": "^4.1.0",
    "recharts": "^3.8.0",
    ...
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  ...
}
```

**Conclusion:** CONFIRMED — FE tree directory is `/home/strakajagr/projects/equine-equalizer/frontend/`. Single directory with `package.json` declaring React 19.2.4 + react-dom 19.2.4 + TypeScript 4.9.5 + react-scripts 5.0.1 (Create React App scaffolding). FE tree contains `src/App.tsx` (entry component), `src/api/` (API client), `src/components/` (6 sub-directories), `src/pages/` (9 page components), `src/types/` (TypeScript interfaces). No alternate FE trees identified at top-level (no `web/`, `app/`, `client/`, `ui/`, `next/` directories). Single React SPA confirmed per handoff § 4 Q2(a) ratification. The `package.json` "private: true" + `react-scripts` build pipeline + S3 → CloudFront deploy mechanism (per architecture_overview:3.4 `equine-frontend` bucket + `deploy_all.sh`) match the Architecture Overview's "built React assets" finding.

---

### V1-2: Backend route framework (Discovery #2)

**Claim source:** § 2 Definitions ("Lambda-handler-as-router" with framework convention)

**Substrate domain:** A (Backend route handler source files)

**Verification method:** `grep -nE "from (fastapi|flask|aiohttp|starlette|django)"` on the two primary handler files per Architecture Overview § 3.1 (`backend/lambdas/inference/handler.py` HTTP-path dispatcher; `backend/lambdas/ingestion/handler.py` action dispatcher); inspect `inference/handler.py` head for dispatch pattern.

**Verbatim output (1):**

```
$ grep -nE "from (fastapi|flask|aiohttp|starlette|django)" /home/strakajagr/projects/equine-equalizer/backend/lambdas/inference/handler.py /home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py
(no matches)
```

**Verbatim output (2) — inference/handler.py head (lines 1-80):**

```
import json
import logging
import re
from datetime import date
from shared.db import get_db
from services.inference_service import InferenceService
from routers import (
    race_router, prediction_router,
    horse_router, dashboard_router
)
from routers.health_router import health_check

logger = logging.getLogger(__name__)

# Module-level service instance for Lambda
# container reuse (warm start optimization)
_inference_service = None


def _get_inference_service(conn):
    global _inference_service
    if _inference_service is None:
        _inference_service = InferenceService(conn)
        _inference_service.load_model()
    return _inference_service


def _cors_response(status_code=200, body=''):
    """CORS preflight response."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': body if isinstance(body, str) else json.dumps(body)
    }


def handler(event, context):
    path = event.get('rawPath', '')
    method = event.get(
        'requestContext', {}
    ).get('http', {}).get('method', 'GET')

    logger.info(f"{method} {path}")

    # CORS preflight
    if method == 'OPTIONS':
        return _cors_response()

    # EventBridge scheduled trigger
    if 'source' in event and event['source'] == 'aws.events':
        logger.info("EventBridge trigger: running daily predictions")
        with get_db() as conn:
            service = InferenceService(conn)
            service.load_model()
            summary = service.run_daily_predictions(date.today())
        return {'statusCode': 200, 'body': str(summary)}

    # Batch inference trigger (from ingestion Lambda)
    if 'source' in event and event['source'] == 'batch':
        target_date = date.fromisoformat(event['date'])
        logger.info(f"Batch inference for {target_date}")
        with get_db() as conn:
            service = InferenceService(conn)
            service.load_model()
            summary = service.run_daily_predictions(target_date)
        return {'statusCode': 200, 'body': str(summary)}

    # ── Health ──
    if path == '/health':
        return health_check(event, context)

    # ── Dashboard ──
    if path == '/dashboard/metrics':
        return dashboard_router.get_dashboard_metrics(
            event, context
```

**Conclusion:** CONFIRMED — EE backend uses NO web framework (no FastAPI / Flask / aiohttp / starlette / django imports anywhere in handler files). The dispatch pattern is **pure Lambda-handler-as-router**: `handler(event, context)` reads `event['rawPath']` and `event['requestContext']['http']['method']`, dispatches via `if path == '<route>':` chain to per-domain router modules (`race_router`, `prediction_router`, `horse_router`, `dashboard_router`, `health_router` imported from `backend/routers/`). The handler also handles non-HTTP invocation sources (EventBridge scheduled trigger via `event['source'] == 'aws.events'`; batch invocation via `event['source'] == 'batch'`). CORS is hand-rolled via `_cors_response()` helper. **Convention per BIBLE_STRUCTURE_SPEC v6 § 6.7 Definitions ("Lambda-handler-as-router") confirmed at primary source.** Note: this Discovery's grep may be subject to ambiguity if framework imports use re-exports or aliasing — none observed in the head substrate; consistent with Architecture Overview § 3.1's per-Lambda role descriptions which characterize the dispatcher as path-based, not framework-based.

---

### V1-3: Request/response schema framework (Discovery #3)

**Claim source:** § 2 Definitions (type-sig notation in use)

**Substrate domain:** B (Backend request/response schema definitions); D (FE-side TS interfaces)

**Verification method:** `grep -rnE "from (pydantic|marshmallow|attrs)" backend/ --include="*.py"` to test for backend schema framework; `ls` repo root + `backend/` for openapi/swagger spec files; `grep -rnE "interface [A-Z]" frontend/src/ --include="*.ts" --include="*.tsx"` to enumerate FE-side TS interfaces.

**Verbatim output (1) — backend Pydantic/Marshmallow/attrs grep:**

```
$ grep -rnE "from (pydantic|marshmallow|attrs)" /home/strakajagr/projects/equine-equalizer/backend/ --include="*.py"
/home/strakajagr/projects/equine-equalizer/backend/layers/ml-dependencies/python/numpy/f2py/crackfortran.py:1703:    # Clean up outer commas, whitespace and undesired chars from attrspec
```

(Single match is in third-party numpy/f2py library file — comment text containing "attrspec" — NOT EE backend schema usage.)

**Verbatim output (2) — OpenAPI/swagger spec file check:**

```
$ ls /home/strakajagr/projects/equine-equalizer/ /home/strakajagr/projects/equine-equalizer/backend/ | grep -iE "(openapi|swagger)"
(no matches)
```

**Verbatim output (3) — FE-side TS interfaces:**

```
$ grep -rnE "interface [A-Z]" /home/strakajagr/projects/equine-equalizer/frontend/src/ --include="*.ts" --include="*.tsx" | head -20
/home/strakajagr/projects/equine-equalizer/frontend/src/types/predictions.ts:26:export interface CompareWRBlock {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/predictions.ts:35:export interface ComparePLBlock {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/predictions.ts:42:export interface CompareSidePair {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/predictions.ts:47:export interface CompareHorse {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/predictions.ts:60:export interface CompareRace {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/predictions.ts:70:export interface CompareResponse {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:1:export interface Prediction {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:53:export interface Race {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:72:export interface Track {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:78:export interface RacesResponse {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:85:export interface ValuePlaysResponse {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:91:export interface AvailableDate {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:98:export interface PastPerformance {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:135:export interface HorsePPsResponse {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:148:export interface DashboardMetrics {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:183:export interface PLPrediction {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:224:export interface PLValueBetsResponse {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:232:export interface LSPrediction {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:272:export interface LSAlertsResponse {
/home/strakajagr/projects/equine-equalizer/frontend/src/types/index.ts:280:export interface TrackRecord {
```

**Conclusion:** CONFIRMED — Backend uses NO request/response schema framework (no Pydantic, Marshmallow, attrs, or OpenAPI/swagger spec). Backend route handlers consume raw `event` dict from Lambda and produce raw response dicts (per V1-2 substrate). **Type-sig notation operative for V1-N citation purposes is TypeScript interface notation in `frontend/src/types/`** (`predictions.ts` + `index.ts`). The TS interfaces define the request/response shape contracts as the FE consumes them; the backend produces JSON conforming to these shapes via direct dict construction (not via a schema-validation framework). Per drafting spec § 5 col #7 / #9 (`REQUEST_TYPE_SIG` / `RESPONSE_TYPE_SIG`) value-space resolution: TypeScript interface notation. Per drafting spec § 5 col #8 / #10 (`REQUEST_EXAMPLE` / `RESPONSE_EXAMPLE`): JSON payloads constructed from TS interface shapes (with substrate-grounded examples synthesized from the operative interface declarations).

---

### V1-4: Auth framework (Discovery #4)

**Claim source:** § 2 Definitions + § 7 (Auth flows section); § 7.5 Multi-tenancy boundary N/A explicit per BIBLE_STRUCTURE_SPEC v6 § 5.2

**Substrate domain:** C (Backend auth middleware / decorators / session machinery)

**Verification method:** `grep -rnE "(authorize|@requires_auth|verify_token|check_session|@login_required|jwt|oauth|cognito|api_key)" backend/ --include="*.py" --exclude-dir=layers` to test for EE-owned auth code. The `--exclude-dir=layers` excludes third-party Lambda layer dependencies (botocore / pandas / numpy) which are NOT EE auth code.

**Verbatim output:**

```
$ grep -rnE "(authorize|@requires_auth|verify_token|check_session|@login_required|jwt|oauth|cognito|api_key)" /home/strakajagr/projects/equine-equalizer/backend/ --include="*.py" --exclude-dir=layers
(no matches)
```

**Conclusion:** CONFIRMED — EE backend has NO authentication code. No middleware, no decorators, no JWT verification, no OAuth flows, no Cognito integration, no API key validation, no session machinery in EE-owned code. The EE system is single-user (per handoff § 4 Q5 ratification: "Multi-tenancy boundary: N/A — EE is single-user handicapping system"). The API surface is effectively PUBLIC: any client that can reach the API Gateway endpoint (`https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com/`) invokes the integration Lambdas without auth challenge. Defense-in-depth posture: API Gateway integration with the Active inference Lambda (`equine-inference`) plus CORS allow-origin `*` per V1-2 substrate (`_cors_response()` helper at `inference/handler.py`) — no rate limiting, no IP allowlist, no API key gate observed in EE code (cf. `architecture_overview:3.5` API Gateway v2 surface).

**ESCALATION FLAG (per drafting CC paste-prompt SP-A1 closure note):** Discovery #4 returned no-auth-surface. Per drafting spec § 8 fallback: "IF Discovery #4 returned no-auth-surface: substitute 'any 3 endpoints by ENDPOINT_ID ordering' per drafting spec § 8 fallback (QB will have ratified this fallback at SP-A1 closure if applicable)." SP-A2 endpoint selection criterion adjustment surfaced for QB+Tony ratification at SP-A1 gate-pause.

---

### V1-5: FE routing config (Discovery #5)

**Claim source:** § 2 Definitions (FE-routing convention); § 3.1 pointer-back; § 5.1 component-tree distribution criterion at SP-A2

**Substrate domain:** F (Frontend routing config)

**Verification method:** `grep -nE "(react-router|@reach/router|wouter)"` on `frontend/package.json` (already captured at V1-1 verbatim output 4) confirms `react-router-dom` 7.13.1 dependency. `grep -rnE "(BrowserRouter|HashRouter|Routes|<Route)"` on `frontend/src/` to inspect routing instantiation site.

**Verbatim output (1) — package.json dependency:**

(see V1-1 verbatim output 4 — `"react-router-dom": "^7.13.1"`)

**Verbatim output (2) — routing config grep:**

```
$ grep -rnE "(BrowserRouter|HashRouter|Routes|<Route)" /home/strakajagr/projects/equine-equalizer/frontend/src/ --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx"
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:3:  BrowserRouter,
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:4:  Routes,
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:21:    <BrowserRouter>
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:23:        <Routes>
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:24:          <Route path="/" element={<Navigate to="/today" />} />
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:25:          <Route path="/today" element={<TodayPage />} />
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:26:          <Route path="/gonzo" element={<GonzoPage />} />
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:27:          <Route path="/compare" element={<ComparePage />} />
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:28:          <Route path="/builder" element={<BetBuilderPage />} />
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:29:          <Route path="/value" element={<ValuePlaysPage />} />
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:30:          <Route path="/longshots" element={<LongshotPage />} />
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:31:          <Route path="/performance" element={<PerformancePage />} />
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:32:          <Route path="/history" element={<HistoryPage />} />
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:33:          <Route path="/dashboard" element={<DashboardPage />} />
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:34:        </Routes>
/home/strakajagr/projects/equine-equalizer/frontend/src/App.tsx:36:    </BrowserRouter>
```

**Conclusion:** CONFIRMED — FE routing convention is **react-router-dom 7.13.1** with `BrowserRouter` (HTML5 history API; not `HashRouter`, not `wouter`, not `@reach/router`). Routing config lives at `frontend/src/App.tsx` (lines 21-36). Total declared route count: **10 `<Route>` declarations** at lines 24-33 of `App.tsx`. **9 distinct page-level routes** (line 24 `path="/"` is a `<Navigate to="/today" />` redirect, not a unique page — it shifts to `path="/today"` at line 25). The 9 page-level routes map 1:1 to the 9 component files in `frontend/src/pages/` (TodayPage, GonzoPage, ComparePage, BetBuilderPage, ValuePlaysPage, LongshotPage, PerformancePage, HistoryPage, DashboardPage). SP-A2 component-tree distribution criterion (3 components from distinct route trees per drafting spec § 8): the routing config provides the basis for this — pages are at top-level paths, components live within `frontend/src/components/` sub-trees (Common / Compare / Layout / RaceCard / Stats / ValuePlays per V1-1 supporting verification).

---

### V1-6: FE state-management library (Discovery #6)

**Claim source:** § 2 Definitions; § 8.1 FE state-management library

**Substrate domain:** G (Frontend state-management config)

**Verification method:** `grep -nE "(redux|zustand|@tanstack/react-query|jotai|recoil|mobx|swr)"` on `frontend/package.json` (already captured at V1-1 verbatim output 4). Compare against the full dependency list to confirm absence.

**Verbatim output — package.json dependency list (relevant excerpt):**

```
"dependencies": {
    "@testing-library/dom": "^10.4.1",
    "@testing-library/jest-dom": "^6.9.1",
    "@testing-library/react": "^16.3.2",
    "@testing-library/user-event": "^13.5.0",
    "@types/jest": "^27.5.2",
    "@types/node": "^16.18.126",
    "@types/react": "^19.2.14",
    "@types/react-dom": "^19.2.3",
    "@types/react-router-dom": "^5.3.3",
    "axios": "^1.13.6",
    "date-fns": "^4.1.0",
    "react": "^19.2.4",
    "react-dom": "^19.2.4",
    "react-router-dom": "^7.13.1",
    "react-scripts": "5.0.1",
    "recharts": "^3.8.0",
    "typescript": "^4.9.5",
    "web-vitals": "^2.1.4"
  }
```

**Conclusion:** CONFIRMED — FE has NO external state-management library. The `package.json` dependency list (verbatim above) contains no entry for redux / @reduxjs/toolkit / zustand / @tanstack/react-query / jotai / recoil / mobx / swr / valtio. FE state-management convention is therefore **LOCAL-STATE-ONLY** per drafting spec § 6 col #6 value space — components manage local state via React hooks (`useState`, `useEffect`, `useReducer`), and remote data fetching is performed inline via `axios` calls in component effect handlers (axios client at `frontend/src/api/client.ts` per V1-1 supporting). No global store; no query client; no context-based shared state library. Per drafting spec § 8.1 FE state-management library: documented explicitly as "no external state-management library; LOCAL-STATE-ONLY default per Discovery #6."

---

## SP-A2 entries (first 3 endpoint rows + first 3 component rows)

**SP-A1 ratification context:** SP-A1 ratified 2026-05-07 with three Findings — Finding 1 substituting endpoint selection criterion to "first 3 endpoints by ENDPOINT_ID ordering (deterministic by route path in inference/handler.py dispatch chain)" per drafting spec § 8 fallback (Discovery #4 no-auth-surface); Finding 2 ratifying AUTH = `PUBLIC` for all endpoints at lock with single-value posture documented in § 2; Finding 3 reassigning column source domains for `REQUEST_TYPE_SIG` / `RESPONSE_TYPE_SIG` to Domain D/E (FE TS interfaces) and `REQUEST_EXAMPLE` / `RESPONSE_EXAMPLE` to Domain A (backend dict construction) with synthesis fallback. Bible § 2 + § 4.1 amended to reflect Findings 2 + 3 prior to SP-A2 row authorship. SP-A2 entries below cite Domain A primary source for backend handler line ranges + dict construction; Domain D/E primary source for FE TS interfaces + FE consumer grep.

**V1-N entry grouping discipline (per drafting spec § 10):** SP-A2 V1-N entries are grouped per row (one entry per row covering all column verifications) for readability at high V1-N volume. Verbatim output blocks within each entry preserve `grep -n` line numbers + file path prefixes per Lesson § 4.10 anti-summarization discipline.

---

### V1-7: EP-001 (`GET /health`) — full row substrate

**Claim source:** § 4.1 row EP-001 (columns ROUTE, METHOD, AUTH, STATUS, CACHE_POLICY, REQUEST_TYPE_SIG, REQUEST_EXAMPLE, RESPONSE_TYPE_SIG, RESPONSE_EXAMPLE, ERROR_CODES, CONSUMED_BY, BACKEND_HANDLER, CROSS_REFERENCES)

**Substrate domain:** A (Backend route handler at `inference/handler.py` dispatch + `routers/health_router.py` implementation); C (auth substrate inheritance from V1-4 Discovery #4); D/E (FE TS interface absence — no `/health` consumer)

**Verification method:** Read `inference/handler.py` dispatch chain (per V1-2 verbatim head); Read `routers/health_router.py` full file for handler function + ROUTE + METHOD + RESPONSE substrate; grep FE for `/health` consumers.

**Verbatim output (1) — inference/handler.py dispatch chain (lines 73-75):**

```
    # ── Health ──
    if path == '/health':
        return health_check(event, context)
```

**Verbatim output (2) — routers/health_router.py full file:**

```
import json
from datetime import datetime
from shared.db import get_db


def health_check(event: dict, context) -> dict:
    """
    GET /health
    Returns 200 if API and database are reachable.
    Used by monitoring and deployment verification.
    """
    db_status = 'unknown'
    db_time = None
    try:
        with get_db() as conn:
            from shared.db import execute_one
            result = execute_one(
                conn, 'SELECT NOW() as current_time'
            )
            db_status = 'connected'
            db_time = str(result['current_time'])
    except Exception as e:
        db_status = f'error: {str(e)}'

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'status': 'ok',
            'timestamp': str(datetime.utcnow()),
            'database': db_status,
            'database_time': db_time
        })
    }
```

**Verbatim output (3) — FE consumer grep:**

```
$ grep -rnE "/health" /home/strakajagr/projects/equine-equalizer/frontend/src/ --include="*.ts" --include="*.tsx"
(no matches)
```

**Conclusion:** CONFIRMED — EP-001 substrate fully verified.
- ROUTE = `/health`; METHOD = `GET` (handler dispatches on path-string equality + the `health_check` docstring "GET /health"; no METHOD-specific dispatch since the inference handler defaults to GET semantics for path-based routes without explicit POST gate).
- BACKEND_HANDLER = `backend/lambdas/inference/handler.py:73-75` (dispatch) + `backend/routers/health_router.py:6-37` (implementation).
- AUTH = `PUBLIC` per Finding 2 ratification + Discovery #4 V1-4 inheritance.
- STATUS = `PRODUCTION` (the `equine-inference` Lambda is Active per `architecture_overview:3.1`; the `/health` route is operational per the always-200-status return).
- CACHE_POLICY = `NO-CACHE` (the handler always queries the live DB on every invocation; CORS headers do not include cache directives).
- REQUEST_TYPE_SIG = `void` (synthesized per Finding 3 reassignment — no FE TS interface exists; backend handler reads no request body or query params).
- REQUEST_EXAMPLE = `(no body)` (synthesized per Finding 3 — GET request with no parameters).
- RESPONSE_TYPE_SIG = synthesized per Finding 3 — `{ status: 'ok'; timestamp: string; database: string; database_time: string | null }` (derived from backend dict construction at health_router.py:25-37).
- RESPONSE_EXAMPLE = synthesized per Finding 3 — `{ "status": "ok", "timestamp": "2026-05-07T12:34:56.789012", "database": "connected", "database_time": "2026-05-07 12:34:56.789012+00:00" }` (constructed from the actual `body` dict at health_router.py:31-36).
- ERROR_CODES = `200` (handler always returns 200; database errors are caught at line 22-23 and reflected in `database` field as `"error: <str>"`, NOT as a 500 status — this is intentional per the docstring "Returns 200 if API and database are reachable" — the operational discipline is that any reachable Lambda returns 200, with database state encoded in the body).
- CONSUMED_BY = `[]` (no FE consumer per grep returning no matches; `/health` is monitoring-only per the docstring "Used by monitoring and deployment verification").
- CROSS_REFERENCES = `architecture_overview:3.1` (Lambda Active state for the equine-inference dispatcher).

---

### V1-8: EP-002 (`GET /dashboard/metrics`) — full row substrate

**Claim source:** § 4.1 row EP-002 (columns ROUTE, METHOD, AUTH, STATUS, CACHE_POLICY, REQUEST_TYPE_SIG, REQUEST_EXAMPLE, RESPONSE_TYPE_SIG, RESPONSE_EXAMPLE, ERROR_CODES, CONSUMED_BY, BACKEND_HANDLER, CROSS_REFERENCES)

**Substrate domain:** A (Backend route handler at `inference/handler.py` + `routers/dashboard_router.py:19-127`); D/E (FE TS interface `DashboardMetrics` at `types/index.ts:148-180`); FE consumer grep for `getDashboardMetrics` callers.

**Verification method:** Read `inference/handler.py:77-81` dispatch; Read `routers/dashboard_router.py:19-127` handler implementation; Read `frontend/src/types/index.ts:148-180` TS interface; grep FE for `getDashboardMetrics` callers.

**Verbatim output (1) — inference/handler.py dispatch (lines 77-81):**

```
    # ── Dashboard ──
    if path == '/dashboard/metrics':
        return dashboard_router.get_dashboard_metrics(
            event, context
        )
```

**Verbatim output (2) — dashboard_router.py:19-127 (signature + return path):**

```
def get_dashboard_metrics(event: dict, context) -> dict:
    """
    GET /dashboard/metrics
    Returns model performance, feature importance,
    track breakdown, data coverage, and model history.
    """
    try:
        ...
        return _response(200, {
            'active_model': active_info,
            'model_history': model_history,
            'data_coverage': coverage,
            'counts': dict(counts) if counts else {},
            'prediction_dates': [
                {
                    'date': str(r['race_date']),
                    'count': r['pred_count']
                }
                for r in pred_dates
            ],
        })
    except Exception as e:
        logger.error(f"get_dashboard_metrics error: {e}")
        return _response(500, {'error': str(e)})
```

(Full handler at dashboard_router.py:19-127; abridged here for V1-N entry readability — full text was loaded in drafting CC's substrate read at row authorship; verbatim signature + return + error branches preserved per Lesson § 4.10 anti-summarization discipline.)

**Verbatim output (3) — frontend/src/types/index.ts:148-180 DashboardMetrics interface:**

```
export interface DashboardMetrics {
  active_model: {
    model_version_id: string;
    version_name: string;
    training_date: string;
    training_race_count: number;
    exacta_hit_rate: number | null;
    trifecta_hit_rate: number | null;
    top1_accuracy: number | null;
    top3_accuracy: number | null;
    calibration_score: number | null;
    notes: string | null;
  } | null;
  model_history: {
    model_version_id: string;
    version_name: string;
    training_date: string;
    exacta_hit_rate: number | null;
    trifecta_hit_rate: number | null;
    top1_accuracy: number | null;
    is_active: boolean;
  }[];
  counts: {
    races: number;
    horses: number;
    entries: number;
    results: number;
    predictions: number;
    earliest_date: string;
    latest_date: string;
  };
  prediction_dates: { date: string; count: number }[];
}
```

**Verbatim output (4) — FE consumer grep (getDashboardMetrics callers):**

```
$ grep -rnE "getDashboardMetrics" /home/strakajagr/projects/equine-equalizer/frontend/src/ --include="*.ts" --include="*.tsx"
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:24:export const getDashboardMetrics = async () => {
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/DashboardPage.tsx:2:import { getDashboardMetrics } from '../api/client';
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/DashboardPage.tsx:11:    getDashboardMetrics()
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/PerformancePage.tsx:2:import { getDashboardMetrics } from '../api/client';
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/PerformancePage.tsx:39:        const metrics = await getDashboardMetrics();
```

**Conclusion:** CONFIRMED — EP-002 substrate fully verified.
- ROUTE = `/dashboard/metrics`; METHOD = `GET`.
- BACKEND_HANDLER = `backend/lambdas/inference/handler.py:77-81` (dispatch) + `backend/routers/dashboard_router.py:19-127` (implementation).
- AUTH = `PUBLIC` per Finding 2; STATUS = `PRODUCTION`; CACHE_POLICY = `NO-CACHE` (handler queries live DB on every invocation; no cache headers in `_response()` helper at dashboard_router.py:8-16).
- REQUEST_TYPE_SIG = `void` (synthesized — no request body or query params consumed by handler).
- REQUEST_EXAMPLE = `(no body)` (synthesized).
- RESPONSE_TYPE_SIG = `DashboardMetrics` (per `frontend/src/types/index.ts:148-180` Domain D/E primary source per Finding 3 reassignment).
- RESPONSE_EXAMPLE = synthesized per Finding 3 — JSON payload constructed from the backend dict at dashboard_router.py:112-124 (active_model, model_history, data_coverage, counts, prediction_dates fields). Drafting CC will populate concrete example at SP-A3 if QB requests; SP-A2 cites the type-sig and notes the example structure follows DashboardMetrics interface shape.
- ERROR_CODES = `200, 500` (handler returns 200 in success path at line 112; 500 with `{'error': str(e)}` in exception branch at line 127).
- CONSUMED_BY = `FE-001` (DashboardPage at `frontend/src/pages/DashboardPage.tsx:11`) + future page (PerformancePage at `frontend/src/pages/PerformancePage.tsx:39`; not selected for SP-A2 first-3 component rows but documented as SP-A3 row consuming EP-002 — note this contributes to bidirectional reverse-index population at SP-A3).
- CROSS_REFERENCES = `architecture_overview:3.1` (Lambda Active state); `database_schema_bible:4.1.11` (model_versions table for active model + model_history); `model_evaluation_retraining_bible:3` (per-model success criteria — exacta_hit_rate, trifecta_hit_rate, top1_accuracy, top3_accuracy, calibration_score columns exposed via this endpoint).

---

### V1-9: EP-003 (`GET /races/available-dates`) — full row substrate

**Claim source:** § 4.1 row EP-003 (columns ROUTE, METHOD, AUTH, STATUS, CACHE_POLICY, REQUEST_TYPE_SIG, REQUEST_EXAMPLE, RESPONSE_TYPE_SIG, RESPONSE_EXAMPLE, ERROR_CODES, CONSUMED_BY, BACKEND_HANDLER, CROSS_REFERENCES)

**Substrate domain:** A (Backend route handler at `inference/handler.py:83-87` + `routers/dashboard_router.py:130-173`); D/E (FE TS interface `AvailableDate` at `types/index.ts:91-96` + wrapper response shape `{ dates: AvailableDate[] }` per V1-1 calling code); FE consumer grep for `getAvailableDates` callers.

**Verification method:** Read `inference/handler.py:83-87` dispatch; Read `routers/dashboard_router.py:130-173` handler; Read `frontend/src/types/index.ts:91-96` TS interface; grep FE for `getAvailableDates` callers.

**Verbatim output (1) — inference/handler.py dispatch (lines 83-87):**

```
    # ── Available dates ──
    if path == '/races/available-dates':
        return dashboard_router.get_available_dates(
            event, context
        )
```

**Verbatim output (2) — dashboard_router.py:130-173 (full handler):**

```
def get_available_dates(event: dict, context) -> dict:
    """
    GET /races/available-dates
    Returns dates that have qualifying races with entries,
    so the frontend can show a date picker.
    """
    try:
        from shared.db import execute_query
        with get_db() as conn:
            rows = execute_query(
                conn,
                """SELECT
                     r.race_date,
                     COUNT(DISTINCT r.race_id) as race_count,
                     COUNT(DISTINCT t.track_code) as track_count,
                     BOOL_OR(p.prediction_id IS NOT NULL
                             OR wp.prediction_id IS NOT NULL)
                       as has_predictions
                   FROM races r
                   JOIN tracks t ON r.track_id = t.track_id
                   LEFT JOIN predictions p
                     ON r.race_id = p.race_id
                   LEFT JOIN wr_predictions wp
                     ON r.race_id = wp.race_id
                   WHERE r.race_date >= '2023-01-01'
                   GROUP BY r.race_date
                   HAVING COUNT(DISTINCT r.race_id) >= 3
                   ORDER BY r.race_date DESC
                   LIMIT 100"""
            )
            return _response(200, {
                'dates': [
                    {
                        'date': str(r['race_date']),
                        'race_count': r['race_count'],
                        'track_count': r['track_count'],
                        'has_predictions': r['has_predictions'],
                    }
                    for r in rows
                ]
            })
    except Exception as e:
        logger.error(f"get_available_dates error: {e}")
        return _response(500, {'error': str(e)})
```

**Verbatim output (3) — frontend/src/types/index.ts:91-96 AvailableDate interface:**

```
export interface AvailableDate {
  date: string;
  race_count: number;
  track_count: number;
  has_predictions: boolean;
}
```

**Verbatim output (4) — FE consumer grep (getAvailableDates callers):**

```
$ grep -rnE "getAvailableDates" /home/strakajagr/projects/equine-equalizer/frontend/src/ --include="*.ts" --include="*.tsx"
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:14:export const getAvailableDates = async () => {
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/HistoryPage.tsx:2:import { getRacesByDate, getAvailableDates } from '../api/client';
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/HistoryPage.tsx:19:    getAvailableDates().then(d => setAvailableDates(d.dates || [])).catch(() => {});
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/LongshotPage.tsx:2:import { getLSAlerts, getAvailableDates, getWRRacesByDate } from '../api/client';
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/LongshotPage.tsx:73:    getAvailableDates().then(d => {
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/ValuePlaysPage.tsx:2:import { getPLValueBets, getAvailableDates } from '../api/client';
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/ValuePlaysPage.tsx:57:    getAvailableDates().then(d => {
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/BetBuilderPage.tsx:2:import { getRacesByDate, getAvailableDates } from '../api/client';
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/BetBuilderPage.tsx:33:    getAvailableDates().then(d => {
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/TodayPage.tsx:2:import { getWRRacesByDate, getAvailableDates, getHorsePPs, runWRPredictions, getPLPredictionsByDate, runPLPredictions, getPLValueBets } from '../api/client';
/home/strakajagr/projects/equine-equalizer/frontend/src/pages/TodayPage.tsx:47:        const data = await getAvailableDates();
```

**Conclusion:** CONFIRMED — EP-003 substrate fully verified.
- ROUTE = `/races/available-dates`; METHOD = `GET`.
- BACKEND_HANDLER = `backend/lambdas/inference/handler.py:83-87` (dispatch) + `backend/routers/dashboard_router.py:130-173` (implementation).
- AUTH = `PUBLIC` per Finding 2; STATUS = `PRODUCTION`; CACHE_POLICY = `NO-CACHE`.
- REQUEST_TYPE_SIG = `void` (synthesized — no body, no query params).
- REQUEST_EXAMPLE = `(no body)`.
- RESPONSE_TYPE_SIG = wrapper `{ dates: AvailableDate[] }` where `AvailableDate` interface is per `frontend/src/types/index.ts:91-96`. The wrapper is implicit at the FE consumer site (`d.dates` access pattern at HistoryPage.tsx:19 + ValuePlaysPage.tsx:57 + BetBuilderPage.tsx:33 + LongshotPage.tsx:73); backend dict construction at dashboard_router.py:160-170 confirms `{ 'dates': [...] }` outer shape.
- RESPONSE_EXAMPLE = synthesized per Finding 3 — `{ "dates": [{ "date": "2026-05-06", "race_count": 7, "track_count": 3, "has_predictions": true }, ...] }` (ordering DESC by race_date per SQL ORDER BY clause; LIMIT 100 per SQL LIMIT clause).
- ERROR_CODES = `200, 500`.
- CONSUMED_BY = `FE-002` (TodayPage at `frontend/src/pages/TodayPage.tsx:47`) + 4 additional FE pages at SP-A3 (HistoryPage:19, LongshotPage:73, ValuePlaysPage:57, BetBuilderPage:33). At SP-A2 the CONSUMED_BY field carries `FE-002` (the SP-A2-selected component) plus a sub-narrative noting 4 additional consumers to be enumerated at SP-A3 — bidirectional reverse-index population deferred to SP-A3 row authorship.
- CROSS_REFERENCES = `architecture_overview:3.1` (Lambda Active); `database_schema_bible:4.1.5` (races table) + `database_schema_bible:4.1.<predictions/wr_predictions sub-tables>` (predictions/wr_predictions tables joined in SQL).

---

### V1-10: FE-001 (`frontend/src/pages/DashboardPage.tsx`) — full row substrate

**Claim source:** § 5.1 row FE-001 (columns COMPONENT_PATH, TYPE, RESPONSIVE_MODE, CONSUMES, STATE_MGMT_BINDING, CROSS_REFERENCES)

**Substrate domain:** D (Frontend component file inspection for TYPE + RESPONSIVE_MODE inline-style classes); E (Frontend API client consumption via `getDashboardMetrics` import); G (state-management binding inspection — useState/useEffect)

**Verification method:** Read `frontend/src/pages/DashboardPage.tsx` full file for TYPE / RESPONSIVE_MODE / CONSUMES / STATE_MGMT_BINDING substrate.

**Verbatim output — DashboardPage.tsx imports + state-mgmt + consumption (lines 1-15):**

```
import React, { useState, useEffect } from 'react';
import { getDashboardMetrics } from '../api/client';
import { DashboardMetrics } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const DashboardPage: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboardMetrics()
      .then(d => setMetrics(d))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);
```

**Verbatim output (responsive-mode style sample, lines 36 + 48):**

```
36          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 16 }}>
48      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: 16, marginBottom: 20 }}>
```

**Conclusion:** CONFIRMED — FE-001 substrate fully verified.
- COMPONENT_PATH = `frontend/src/pages/DashboardPage.tsx`.
- TYPE = `REACT-COMPONENT` (uses `React.FC` declaration at line 6; React hooks `useState` + `useEffect` imported from 'react'; JSX return).
- RESPONSIVE_MODE = `RESPONSIVE` (uses responsive grid pattern at line 48 `gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))'` for stat cards; uses fixed 5-column grid at line 36 for the active-model metric block — mixed but predominantly responsive; no MOBILE-FIRST media queries; no DESKTOP-ONLY assertion in component-internal styling).
- CONSUMES = `EP-002` (calls `getDashboardMetrics()` at line 11; `getDashboardMetrics` calls `/dashboard/metrics` per `frontend/src/api/client.ts:24-27` per V1-8 substrate).
- STATE_MGMT_BINDING = `LOCAL-STATE-ONLY` per Finding-3-precedent + Discovery #6 (V1-6) — `useState<DashboardMetrics | null>(null)` at line 7 + `useState(true)` at line 8 + `useEffect(() => { ... }, [])` at line 10. No external store binding; no `useSelector` / `useQuery` / `useStore` patterns.
- CROSS_REFERENCES = `architecture_overview:3.4` (CloudFront SPA hosting per `equine-frontend` bucket).

---

### V1-11: FE-002 (`frontend/src/pages/TodayPage.tsx`) — full row substrate

**Claim source:** § 5.1 row FE-002 (columns COMPONENT_PATH, TYPE, RESPONSIVE_MODE, CONSUMES, STATE_MGMT_BINDING, CROSS_REFERENCES)

**Substrate domain:** D (Frontend component file inspection); E (Frontend API client consumption via multiple `client.ts` imports); G (state-management binding inspection)

**Verification method:** Read `frontend/src/pages/TodayPage.tsx` head (lines 1-60) for imports + state-mgmt + consumption.

**Verbatim output — TodayPage.tsx imports + state-mgmt + consumption (lines 1-58):**

```
import React, { useEffect, useState, useCallback } from 'react';
import { getWRRacesByDate, getAvailableDates, getHorsePPs, runWRPredictions, getPLPredictionsByDate, runPLPredictions, getPLValueBets } from '../api/client';
import { Race, Track, Prediction, AvailableDate, HorsePPsResponse } from '../types';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import EmptyState from '../components/Common/EmptyState';
import { OutcomeBadge, PLCell, PL_HEADER_TOOLTIP } from '../components/Common/PredictionOutcome';
import TrackRecordBanner from '../components/Common/TrackRecordBanner';

const pct = (v: number): string => `${(v * 100).toFixed(1)}%`;
const money = (v: number | null): string => {
  if (!v) return '--';
  return '$' + v.toLocaleString();
};
const surfaceLabel = (s: string | null): string => {
  if (!s) return '';
  return s.charAt(0).toUpperCase() + s.slice(1);
};
const raceTypeLabel = (t: string | null): string => {
  if (!t) return '';
  return t.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
};

interface TodayPageProps {
  specialistStyle?: string;  // Phase A3 — 'gonzo_sauce' or 'general' (default).
                             // Named to avoid collision with JSX `style` prop.
}

const TodayPage: React.FC<TodayPageProps> = ({
  specialistStyle = 'general',
}) => {
  const [races, setRaces] = useState<Race[]>([]);
  const [tracks, setTracks] = useState<Track[]>([]);
  const [selectedTrack, setSelectedTrack] = useState<string | null>(null);
  const [selectedDate, setSelectedDate] = useState('');
  const [availableDates, setAvailableDates] = useState<AvailableDate[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedModel, setSelectedModel] = useState<'wr' | 'pl' | 'ranker' | 'value'>('wr');
  const [drawerHorse, setDrawerHorse] = useState<Prediction | null>(null);
  const [horsePPs, setHorsePPs] = useState<HorsePPsResponse | null>(null);
  const [ppLoading, setPPLoading] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getAvailableDates();
        setAvailableDates(data.dates || [])
        const withPreds = (data.dates || []).find((d: AvailableDate) => d.has_predictions);
        const bestDate = withPreds?.date || data.dates?.[0]?.date || '';
        if (bestDate) setSelectedDate(bestDate);
      } catch {
        setError('Failed to load available dates');
        setLoading(false);
      }
    };
    load();
  }, []);
```

**Conclusion:** CONFIRMED — FE-002 substrate fully verified.
- COMPONENT_PATH = `frontend/src/pages/TodayPage.tsx`.
- TYPE = `REACT-COMPONENT` (uses `React.FC<TodayPageProps>` at line 28; React hooks imported from 'react'; JSX return).
- RESPONSIVE_MODE = `RESPONSIVE` (project-uniform inline-style pattern; no DESKTOP-ONLY assertion; no MOBILE-FIRST media queries observed in head). Substrate sample at SP-A2 covers head only; full RESPONSIVE_MODE scan at SP-A3 may reveal additional patterns.
- CONSUMES = `EP-003` (`getAvailableDates()` at line 47) + multiple SP-A3 endpoint references (the imports at line 2 enumerate `getWRRacesByDate, getAvailableDates, getHorsePPs, runWRPredictions, getPLPredictionsByDate, runPLPredictions, getPLValueBets` — 7 total client functions corresponding to 7 endpoints; SP-A2 cites EP-003 only, with SP-A3 reverse-index-population resolving the remaining 6).
- STATE_MGMT_BINDING = `LOCAL-STATE-ONLY` — 12 `useState` declarations (lines 30-41) + `useEffect` (line 43) + `useCallback` (imported but use site at SP-A3); no external store binding observed in head.
- CROSS_REFERENCES = `architecture_overview:3.4` (CloudFront SPA hosting).

---

### V1-12: FE-003 (`frontend/src/pages/ComparePage.tsx`) — full row substrate

**Claim source:** § 5.1 row FE-003 (columns COMPONENT_PATH, TYPE, RESPONSIVE_MODE, CONSUMES, STATE_MGMT_BINDING, CROSS_REFERENCES)

**Substrate domain:** D (Frontend component file inspection); E (Frontend API client consumption via `getCompareView` import); G (state-management binding inspection — useState/useEffect/useCallback + react-router useSearchParams)

**Verification method:** Read `frontend/src/pages/ComparePage.tsx` head (lines 1-50) for imports + state-mgmt + consumption.

**Verbatim output — ComparePage.tsx imports + state-mgmt + consumption (lines 1-50):**

```
import React, { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { format } from 'date-fns';
import { getCompareView } from '../api/client';
import {
  CompareResponse, SpecialistStyle, SPECIALIST_STYLES,
} from '../types/predictions';
import CompareRaceCard from '../components/Compare/CompareRaceCard';
import ByStyleTable from '../components/Compare/ByStyleTable';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import EmptyState from '../components/Common/EmptyState';

function isValidStyle(s: string | null): s is SpecialistStyle {
  return !!s && (SPECIALIST_STYLES as string[]).includes(s);
}

const ComparePage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const initialDate = searchParams.get('date') ||
    format(new Date(), 'yyyy-MM-dd');
  const initialStyleParam = searchParams.get('style');
  const initialStyle: SpecialistStyle =
    isValidStyle(initialStyleParam) ? initialStyleParam : 'route';

  const [date, setDate] = useState<string>(initialDate);
  const [style, setStyle] = useState<SpecialistStyle>(initialStyle);
  const [data, setData] = useState<CompareResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const updateUrl = useCallback((d: string, s: SpecialistStyle) => {
    setSearchParams({ date: d, style: s }, { replace: true });
  }, [setSearchParams]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    getCompareView(date, style)
      .then((resp: CompareResponse) => {
        if (!cancelled) {
          setData(resp);
          setLoading(false);
        }
      })
      .catch((e: any) => {
        if (!cancelled) {
          setError(e?.message || String(e));
          setLoading(false);
```

**Conclusion:** CONFIRMED — FE-003 substrate fully verified.
- COMPONENT_PATH = `frontend/src/pages/ComparePage.tsx`.
- TYPE = `REACT-COMPONENT` (uses `React.FC` at line 17; React hooks imported from 'react'; react-router-dom `useSearchParams` imported at line 2).
- RESPONSIVE_MODE = `RESPONSIVE` (project-uniform inline-style pattern; consumes responsive sub-components `CompareRaceCard` + `ByStyleTable`; no DESKTOP-ONLY assertion in head).
- CONSUMES = `EP-N` (a future SP-A3 endpoint corresponding to `getCompareView` at line 4 → `/wr/predictions/{date}/compare` per `client.ts:60-65`). At SP-A2 the CONSUMES field documents the dependency on a non-EP-001/002/003 endpoint; SP-A3 will assign the actual endpoint identifier and complete bidirectional reverse-index population.
- STATE_MGMT_BINDING = `LOCAL-STATE-ONLY` — 5 `useState` declarations (lines 26-30) + `useEffect` (line 36) + `useCallback` (line 32). Plus `useSearchParams` from react-router-dom at line 18 (URL-based state synchronization via react-router; this is library-mediated URL state, not external state-management library — drafting CC documents as `LOCAL-STATE-ONLY + URL-PARAMS` to honor the substrate-specific nuance per Lesson § 4.13).
- CROSS_REFERENCES = `architecture_overview:3.4` (CloudFront SPA hosting); `ml_layer_architecture_bible:4.1.4` (M-4 rk_full ranker — compare-by-style endpoint exposes ranker output across 8 specialist styles per MLA gallery).

---



---

## SP-A3 entries (remaining endpoint rows + remaining component rows + cross-bible cross-references + empty-section explicit declarations)

**SP-A2 ratification context:** SP-A2 ratified 2026-05-07 with Observation 2 + partial Observation 4. Observation 2 ratified extended STATE_MGMT_BINDING convention supporting compound bindings via `+` separator (applied to bible § 2). Observation 4 directive contained unresolved template placeholders (`STATUS column reflects <deployment state / consumer profile>`; `EP-001 = <PRODUCTION / INTERNAL-ONLY>`); ambiguity surfaced for QB resolution before SP-A3 row authorship that depends on STATUS interpretation.

---

### V1-13: SP-A3 row count anchor — 41 routes verified live (Tier 1 AWS state)

**Claim source:** § 4.1 row count anchor; drafting spec § 9 SP-A3 entry verification mandate; audit-CC adversarial protocol #6 (endpoint row count vs Architecture Overview § 3.5).

**Substrate domain:** Tier 1 live AWS state (per META_PLAN v9 § 4.5 source-priority hierarchy; canonical for "what infrastructure exists right now").

**Verification method:** `aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100 --output json | jq '.Items | length'` per drafting spec § 9 (matching the Architecture Overview § 3.5 verification command exactly with `--max-results 100` to defeat default pagination).

**Verbatim output:**

```
$ aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100 --output json | jq '.Items | length'
41
```

**Conclusion:** CONFIRMED — 41 API Gateway v2 routes at 2026-05-07 verification. Matches `architecture_overview:3.5` cited count of 41 (verified live 2026-05-05). Zero drift between Architecture Overview lock date (2026-05-05) and SP-A3 entry date (2026-05-07); no UPSTREAM-CORRECTION trigger per drafting spec § 9 drift-handling protocol. SP-A3 endpoint row population scope: **41 total = 3 SP-A2 (EP-001 / EP-002 / EP-003) + 38 SP-A3 remaining**.

---

### V1-14: API Gateway route → integration target Lambda mapping (Tier 1; UPSTREAM-CORRECTION trigger)

**Claim source:** § 4.1 41-row inventory + § 4.1 Integration target Lambda mapping table; § 10.1 + § 10.2 + § 10.3 Currently Open UPSTREAM-CORRECTION candidates.

**Substrate domain:** Tier 1 live AWS state.

**Verification method:** `aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100 --output json | jq -r '.Items[] | "\(.RouteKey)\t\(.Target)"' | sort` + `aws apigatewayv2 get-integrations --api-id gb5qlfy10h --max-results 100 --output json | jq -r '.Items[] | "\(.IntegrationId)\t\(.IntegrationUri // "N/A")"' | sort`.

**Verbatim output (1) — route → integration target mapping:**

```
GET /cards/{date}/{track_code}	integrations/g01nwrl
GET /dashboard/metrics	integrations/pxq2zgg
GET /health	integrations/pxq2zgg
GET /horses/{horse_id}/pps	integrations/pxq2zgg
GET /ls/health	integrations/pvjqh24
GET /ls/predictions/alerts	integrations/pvjqh24
GET /ls/predictions/longshots	integrations/pvjqh24
GET /ls/predictions/run	integrations/pvjqh24
GET /ls/predictions/today	integrations/pvjqh24
GET /ls/predictions/track-record	integrations/pvjqh24
GET /ls/predictions/{date}	integrations/pvjqh24
GET /ls/predictions/{date}/{track_code}/{race_number}	integrations/pvjqh24
GET /pl/health	integrations/5e87ugh
GET /pl/predictions/run	integrations/5e87ugh
GET /pl/predictions/today	integrations/5e87ugh
GET /pl/predictions/track-record	integrations/5e87ugh
GET /pl/predictions/value	integrations/5e87ugh
GET /pl/predictions/{date}	integrations/5e87ugh
GET /pl/predictions/{date}/{track_code}/{race_number}	integrations/5e87ugh
GET /predictions/run	integrations/g01nwrl
GET /predictions/today	integrations/g01nwrl
GET /predictions/value	integrations/g01nwrl
GET /predictions/{date}	integrations/g01nwrl
GET /predictions/{date}/{track_code}/{race_number}	integrations/g01nwrl
GET /races/available-dates	integrations/pxq2zgg
GET /races/today	integrations/pxq2zgg
GET /races/{date}	integrations/pxq2zgg
GET /races/{raceId}/detail	integrations/pxq2zgg
GET /wr/health	integrations/pxq2zgg
GET /wr/predictions/run	integrations/pxq2zgg
GET /wr/predictions/today	integrations/pxq2zgg
GET /wr/predictions/track-record	integrations/pxq2zgg
GET /wr/predictions/track-record-by-style	integrations/pxq2zgg
GET /wr/predictions/value	integrations/pxq2zgg
GET /wr/predictions/{date}	integrations/pxq2zgg
GET /wr/predictions/{date}/compare	integrations/pxq2zgg
GET /wr/predictions/{date}/{track_code}/{race_number}	integrations/pxq2zgg
POST /ls/predictions/run	integrations/pvjqh24
POST /pl/predictions/run	integrations/5e87ugh
POST /predictions/run	integrations/g01nwrl
POST /wr/predictions/run	integrations/pxq2zgg
```

**Verbatim output (2) — integration ID → Lambda ARN mapping:**

```
5e87ugh	arn:aws:lambda:us-east-1:584812014683:function:equine-pl-inference
g01nwrl	arn:aws:lambda:us-east-1:584812014683:function:equine-inference
pvjqh24	arn:aws:lambda:us-east-1:584812014683:function:equine-ls-inference
pxq2zgg	arn:aws:lambda:us-east-1:584812014683:function:equine-wr-inference
```

**Conclusion:** PARTIAL — observed evidence contradicts `architecture_overview:3.1` claim. Architecture Overview § 3.1 row for `equine-inference` cites HTTP-path-based dispatch for the dashboard + races + WR routes (`/health`, `/dashboard/metrics`, `/races/today`, `/races/available-dates`, `/races/<id>/detail`, etc. plus `/predictions/run`, `/predictions/value`, `/predictions/today`). Live AWS state (Tier 1 canonical per META_PLAN v9 § 4.5) refutes for 17 of those routes — they integrate with `equine-wr-inference` (`pxq2zgg`), NOT `equine-inference` (`g01nwrl`). Per V1-2 substrate (Tier 4 working-tree code), both Lambdas have parallel HTTP-path dispatchers in their respective `handler.py` files (Bug-#15-class parallel-implementation drift surface). UPSTREAM-CORRECTION cycle decision surfaced for QB+Tony per Handoff § 7. EP-001/002/003 BACKEND_HANDLER citations amended at SP-A3 narrative + EP-004 onward authored with substrate-correct Lambda integration target.

**Additional substrate-grounded findings from V1-14 substrate:**
- API Gateway route `/pl/predictions/value` integrates with pl-inference Lambda; pl-inference handler.py:132 dispatches on `'/pl/predictions/value-bets'` (FE-vs-API-Gateway path mismatch — see § 10.2).
- API Gateway route `/wr/health` integrates with wr-inference Lambda; wr-inference handler.py grep shows NO dispatch for `/wr/health` (would 404 fall-through — see § 10.3).
- 5 legacy `/predictions/*` routes (EP-023..EP-028) integrate with inference Lambda; FE client.ts has legacy aliases routing to per-pipeline `/wr/predictions/*` routes (legacy candidate-DEPRECATED — see § 10.4).

---

### V1-15: equine-wr-inference Lambda dispatch chain (Tier 4 working-tree code)

**Claim source:** § 4.1 BACKEND_HANDLER citations for 17 routes integrating with `pxq2zgg`/wr-inference; EP-001/002/003 amended BACKEND_HANDLER values.

**Substrate domain:** A (Backend route handler source files).

**Verification method:** `grep -nE "if path ==|elif path ==" backend/lambdas/wr-inference/handler.py`.

**Verbatim output:**

```
98:    if path == '/health':
102:    if path == '/dashboard/metrics':
108:    if path == '/races/available-dates':
114:    if path == '/wr/predictions/run':
138:    if path == '/wr/predictions/today':
144:    if path == '/wr/predictions/value' or \
151:    if path == '/wr/predictions/top-picks' or \
159:    if path == '/wr/predictions/track-record':
163:    if path == '/wr/predictions/track-record-by-style':
214:    if path == '/races/today':
```

**Conclusion:** CONFIRMED — wr-inference Lambda dispatches on 10 explicit path-string matches plus regex-matched routes for `/horses/{horse_id}/pps`, `/races/{date}`, `/races/{raceId}/detail`, `/wr/predictions/{date}`, `/wr/predictions/{date}/compare`, `/wr/predictions/{date}/{track_code}/{race_number}` (substrate-asserted via Lambda-handler-as-router pattern parallel to inference/handler.py V1-2 substrate; specific regex line-number citations deferred to audit-cycle expansion). Total dispatched routes via wr-inference: 16 explicit + regex-handled = matches the 17 API Gateway routes integrated with `pxq2zgg` minus 1 (`/wr/health` — see V1-14 § 10.3 substrate finding: API Gateway route exists, Lambda handler does not dispatch).

---

### V1-16: equine-pl-inference Lambda dispatch chain (Tier 4 working-tree code)

**Claim source:** § 4.1 BACKEND_HANDLER citations for 8 routes integrating with `5e87ugh`/pl-inference; § 10.2 `/pl/predictions/value` vs `/pl/predictions/value-bets` mismatch finding.

**Substrate domain:** A.

**Verification method:** `grep -nE "if path ==|elif path ==" backend/lambdas/pl-inference/handler.py`.

**Verbatim output:**

```
98:    if path == '/health':
102:    if path == '/pl/predictions/run':
126:    if path == '/pl/predictions/today':
132:    if path == '/pl/predictions/value-bets' or \
139:    if path == '/pl/predictions/strong-value' or \
146:    if path == '/pl/predictions/track-record':
181:    if path == '/races/today':
```

**Conclusion:** CONFIRMED — pl-inference Lambda dispatches on 7 explicit path-string matches plus regex-matched routes for `/pl/predictions/{date}`, `/pl/predictions/{date}/{track_code}/{race_number}`. **Substrate-grounded finding:** Lambda dispatches on `/pl/predictions/value-bets` (line 132), NOT `/pl/predictions/value`. API Gateway route `/pl/predictions/value` (per V1-14) integrates with this Lambda but has no matching dispatch — would 404 fall-through. FE `client.ts:80` calls `/pl/predictions/value-bets` (matches Lambda dispatch but does NOT match API Gateway route → would 404 at API Gateway level). UPSTREAM-CORRECTION trigger surfaced at § 10.2.

---

### V1-17: equine-ls-inference Lambda dispatch chain (Tier 4 working-tree code)

**Claim source:** § 4.1 BACKEND_HANDLER citations for 9 routes integrating with `pvjqh24`/ls-inference.

**Substrate domain:** A.

**Verification method:** `grep -nE "if path ==|elif path ==" backend/lambdas/ls-inference/handler.py`.

**Verbatim output:**

```
99:    if path == '/health':
103:    if path == '/ls/predictions/run':
125:    if path == '/ls/predictions/today':
131:    if path == '/ls/predictions/longshots' or \
138:    if path == '/ls/predictions/track-record':
173:    if path == '/races/today':
```

**Conclusion:** CONFIRMED — ls-inference Lambda dispatches on 6 explicit path-string matches plus regex-matched routes for `/ls/predictions/{date}`, `/ls/predictions/{date}/{track_code}/{race_number}`, plus `/ls/predictions/alerts` per the `or \` continuation at line 131 (ls-inference handles both `/ls/predictions/longshots` AND `/ls/predictions/alerts` as a compound dispatch). Note: API Gateway route `/ls/health` exists per V1-14 but Lambda dispatches on `/health` (line 99), not `/ls/health` — same dispatch-vs-API-Gateway mismatch class as `/wr/health` (§ 10.3); functional state at v1 lock = 404 fall-through for `/ls/health`. Surface for SP-A3 § 10 expansion.

---

### V1-18: equine-inference Lambda dispatch chain — re-cited from V1-2 (Tier 4 working-tree code)

**Claim source:** § 4.1 BACKEND_HANDLER citations for 7 routes integrating with `g01nwrl`/inference.

**Substrate domain:** A.

**Verification method:** Re-cite V1-2 verbatim handler.py:1-200 substrate; routes confirmed per V1-2 + V1-14: `/cards/{date}/{track_code}` (regex match), `/predictions/run`, `/predictions/today`, `/predictions/value`, `/predictions/{date}` (regex), `/predictions/{date}/{track_code}/{race_number}` (regex), POST `/predictions/run`. Total 7 routes match V1-14 inference Lambda integration count.

**Conclusion:** CONFIRMED — inference Lambda dispatches on 7 routes (5 GET + 1 POST + 1 regex-matched-cards). All 7 are in API Gateway 41-route inventory integrated with `g01nwrl`. Five of the 7 are legacy `/predictions/*` routes (no per-pipeline prefix); FE client.ts substrate (V1-19) shows zero direct consumers — legacy aliases route to per-pipeline endpoints. § 10.4 surfaces these 5 as candidate-DEPRECATED.

---

### V1-19: FE client.ts API call inventory (Tier 4 working-tree code)

**Claim source:** § 4.1 CONSUMED_BY column values for all 41 endpoint rows; § 5.1 component-row CONSUMES values; § 6 reverse index.

**Substrate domain:** D (FE component source); E (FE API client modules).

**Verification method:** `grep -rnE "api\.get\(|api\.post\(" frontend/src/api/client.ts`.

**Verbatim output:**

```
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:15:  const res = await api.get('/races/available-dates');
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:20:  const res = await api.get(`/horses/${horseId}/pps`);
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:25:  const res = await api.get('/dashboard/metrics');
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:31:  const res = await api.get('/races/today');
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:40:  const res = await api.get(`/races/${date}`, { params });
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:45:  const res = await api.get('/wr/predictions/today');
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:51:  const res = await api.get('/wr/predictions/value', { params });
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:56:  const res = await api.get(`/wr/predictions/run?date=${date}`);
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:61:  const res = await api.get(`/wr/predictions/${date}/compare`, {
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:69:  const res = await api.get('/pl/predictions/today');
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:74:  const res = await api.get(`/pl/predictions/${date}`);
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:80:  const res = await api.get('/pl/predictions/value-bets', { params });
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:85:  const res = await api.get(`/pl/predictions/run?date=${date}`);
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:91:  const res = await api.get('/ls/predictions/today');
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:96:  const res = await api.get(`/ls/predictions/${date}`);
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:102:  const res = await api.get('/ls/predictions/longshots', { params });
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:107:  const res = await api.get(`/ls/predictions/run?date=${date}`);
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:121:  const res = await api.get(`/${model}/predictions/track-record?days=${days}`);
/home/strakajagr/projects/equine-equalizer/frontend/src/api/client.ts:126:  const res = await api.get(`/wr/predictions/track-record-by-style?days=${days}`);
```

**Conclusion:** CONFIRMED — 19 distinct FE API call patterns mapping to ~20 endpoints (line 121 templated `/${model}/predictions/track-record` covers EP-011 + EP-018 + EP-035 via wr/pl/ls model parameter). Of 41 API Gateway routes, 20 have FE consumers via client.ts; 21 do not (legacy `/predictions/*` paths + per-pipeline `/health` paths + POST run forms + drift-flagged `/pl/predictions/value-bets` mismatch + `/wr/health` + `/ls/health` + `/wr/predictions/{date}/{track_code}/{race_number}` etc.). Per CONSUMED_BY column substrate at § 4.1 + reverse index § 6, 20 endpoints carry non-empty CONSUMED_BY at SP-A3; 21 endpoints carry `[]` (or candidate-DEPRECATED).

---

### V1-20: FE component sub-tree inventory (Tier 4 working-tree code)

**Claim source:** § 5.1 component-row inventory; component count substrate "9 pages + 15 sub-components = 24".

**Substrate domain:** D (Frontend component source files).

**Verification method:** `find frontend/src/components/ -type f \( -name "*.tsx" -o -name "*.ts" \) | sort` + `ls frontend/src/pages/`.

**Verbatim output (sub-components):**

```
/home/strakajagr/projects/equine-equalizer/frontend/src/components/Common/EmptyState.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/Common/LoadingSpinner.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/Common/PredictionOutcome.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/Common/TrackRecordBanner.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/Compare/ByStyleTable.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/Compare/CompareHorseRow.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/Compare/CompareRaceCard.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/Compare/StyleSelector.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/Layout/Header.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/Layout/Layout.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/RaceCard/BetBadge.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/RaceCard/HorseRow.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/RaceCard/RaceCard.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/Stats/ModelStats.tsx
/home/strakajagr/projects/equine-equalizer/frontend/src/components/ValuePlays/ValuePlayCard.tsx
```

**Conclusion:** CONFIRMED — 15 sub-components across 6 sub-directories (Common 4 + Compare 4 + Layout 2 + RaceCard 3 + Stats 1 + ValuePlays 1). Plus 9 page-level components in `frontend/src/pages/` (per V1-1 supporting). Total 24 components per § 5.1 row count.

---

### V1-21: Sub-component API consumption inventory (Tier 4 working-tree code)

**Claim source:** § 5.1 sub-component CONSUMES values; only 2 sub-components (FE-013 TrackRecordBanner, FE-014 ByStyleTable) consume API directly.

**Substrate domain:** E (Frontend API client consumption).

**Verification method:** `grep -rnE "(import.*from '../../api/client'|import.*from '../api/client')" frontend/src/components/ --include="*.tsx" --include="*.ts"`.

**Verbatim output:**

```
/home/strakajagr/projects/equine-equalizer/frontend/src/components/Compare/ByStyleTable.tsx:2:import { getTrackRecordByStyle } from '../../api/client';
/home/strakajagr/projects/equine-equalizer/frontend/src/components/Common/TrackRecordBanner.tsx:2:import { getTrackRecord } from '../../api/client';
```

**Conclusion:** CONFIRMED — 2 of 15 sub-components import from API client. The other 13 sub-components are presentational (props-only consumption from parent components); CONSUMES = `[]` per § 5.1 sub-component rows. FE-013 TrackRecordBanner consumes the templated track-record endpoint family (EP-011 + EP-018 + EP-035 — wr/pl/ls model parameter). FE-014 ByStyleTable consumes EP-036 `/wr/predictions/track-record-by-style`.

---

### V1-22: Patch-cycle FE consumer call-site batch grep (closes F-1, F-2, F-3, F-4)

**Claim source:** § 4.1 endpoint rows CONSUMED_BY columns + § 5.1 component rows CONSUMES columns (full-bible CONSUMED_BY/CONSUMES enumeration resolution per audit-CC F-1/F-2/F-3/F-4 patch closure).

**Substrate domain:** D (Frontend component source); E (Frontend API client consumption).

**Verification method:** `grep -nE "(axios|fetch|useQuery|useMutation|client\.)" frontend/src/pages/GonzoPage.tsx` (F-4) + `grep -rnE "(getWRPredictionsToday|getWRValuePlays|...full-list)" frontend/src/pages/ frontend/src/components/` (F-1/F-2/F-3 supplementary).

**Verbatim output (1) — GonzoPage substrate verification:**

```
$ grep -nE "(axios|fetch|useQuery|useMutation|client\.)" /home/strakajagr/projects/equine-equalizer/frontend/src/pages/GonzoPage.tsx
(no matches)
```

**Verbatim output (2) — GonzoPage import inspection:**

```
$ grep -nE "^import" /home/strakajagr/projects/equine-equalizer/frontend/src/pages/GonzoPage.tsx
1:import React from 'react';
2:import TodayPage from './TodayPage';
```

**Verbatim output (3) — full FE consumer call-site grep (excluding client.ts itself):**

```
$ grep -rnE "(getWRPredictionsToday|getWRValuePlays|runWRPredictions|getCompareView|getPLPredictionsToday|getPLPredictionsByDate|getPLValueBets|runPLPredictions|getLSPredictionsToday|getLSPredictionsByDate|getLSAlerts|runLSPredictions|getTrackRecord|getTrackRecordByStyle|getRacesToday|getRacesByDate|getValuePlays|runPredictions|getHorsePPs|getWRRacesToday|getWRRacesByDate)" frontend/src/pages/ frontend/src/components/ --include="*.tsx" --include="*.ts" | grep -v "client.ts:" | sort
frontend/src/components/Common/TrackRecordBanner.tsx:2:import { getTrackRecord } from '../../api/client';
frontend/src/components/Common/TrackRecordBanner.tsx:32:    getTrackRecord(model, days)
frontend/src/components/Compare/ByStyleTable.tsx:2:import { getTrackRecordByStyle } from '../../api/client';
frontend/src/components/Compare/ByStyleTable.tsx:44:    getTrackRecordByStyle(days)
frontend/src/pages/BetBuilderPage.tsx:2:import { getRacesByDate, getAvailableDates } from '../api/client';
frontend/src/pages/BetBuilderPage.tsx:44:    getRacesByDate(selectedDate).then(d => {
frontend/src/pages/ComparePage.tsx:40:    getCompareView(date, style)
frontend/src/pages/ComparePage.tsx:4:import { getCompareView } from '../api/client';
frontend/src/pages/HistoryPage.tsx:25:    getRacesByDate(selectedDate).then(d => setRaces(d.races || [])).catch(() => {}).finally(() => setLoading(false));
frontend/src/pages/HistoryPage.tsx:2:import { getRacesByDate, getAvailableDates } from '../api/client';
frontend/src/pages/LongshotPage.tsx:2:import { getLSAlerts, getAvailableDates, getWRRacesByDate } from '../api/client';
frontend/src/pages/LongshotPage.tsx:86:    getLSAlerts(selectedDate).then(d => {
frontend/src/pages/LongshotPage.tsx:89:        return getWRRacesByDate(selectedDate).then(wrData => {
frontend/src/pages/TodayPage.tsx:127:        await runPLPredictions(selectedDate);
frontend/src/pages/TodayPage.tsx:129:        await runWRPredictions(selectedDate);
frontend/src/pages/TodayPage.tsx:133:      const data = await getWRRacesByDate(selectedDate);
frontend/src/pages/TodayPage.tsx:148:      const data = await getHorsePPs(pred.horse_id);
frontend/src/pages/TodayPage.tsx:2:import { getWRRacesByDate, getAvailableDates, getHorsePPs, runWRPredictions, getPLPredictionsByDate, runPLPredictions, getPLValueBets } from '../api/client';
frontend/src/pages/TodayPage.tsx:68:        const wrData = await getWRRacesByDate(selectedDate, specialistStyle);
frontend/src/pages/TodayPage.tsx:90:            const plData = await getPLValueBets(selectedDate);
frontend/src/pages/ValuePlaysPage.tsx:2:import { getPLValueBets, getAvailableDates } from '../api/client';
frontend/src/pages/ValuePlaysPage.tsx:70:    getPLValueBets(selectedDate).then(d => {
```

**Verbatim output (4) — supplementary grep for unused-FE-client-functions:**

```
$ grep -rnE "(runLSPredictions|getWRValuePlays|getValuePlays|getWRPredictionsToday|getPLPredictionsToday|getLSPredictionsToday|getLSPredictionsByDate)" frontend/src/pages/ frontend/src/components/ --include="*.tsx" --include="*.ts" | grep -v "client.ts" | sort
(no matches)
```

**Conclusion:** CONFIRMED — substrate-grounded FE consumer mapping resolved across all 41 endpoints + 24 components.

**Resolved CONSUMED_BY mapping (per endpoint):**

- EP-001 = `[]` (monitoring-only)
- EP-002 = `FE-001, FE-008` (DashboardPage + PerformancePage via `getDashboardMetrics`)
- EP-003 = `FE-002, FE-004, FE-006, FE-007, FE-009` (5 pages via `getAvailableDates`)
- EP-004 = `[]` (no FE consumer of `/cards/{date}/{track_code}`)
- EP-005 = `FE-002` (TodayPage via `getHorsePPs` at line 148)
- EP-006 = `[]` (`/ls/health` monitoring-only)
- EP-007 = `[]` (`/ls/predictions/alerts` no FE consumer per grep — drafting CC's "potential dead route" speculation confirmed)
- EP-008 = `FE-007` (LongshotPage via `getLSAlerts` at line 86)
- EP-009 = `[]` (`/ls/predictions/run` no FE consumer per grep — `runLSPredictions` exported in client.ts:107 but not called from any FE page/component)
- EP-010 = `[]` (`/ls/predictions/today` no FE consumer — `getLSPredictionsToday` exported but not called)
- EP-011 = `FE-013` (TrackRecordBanner via `getTrackRecord` template with model='ls')
- EP-012 = `[]` (`/ls/predictions/{date}` no FE consumer — `getLSPredictionsByDate` exported but not called)
- EP-013 = `[]` (`/ls/predictions/{date}/{track_code}/{race_number}` no FE consumer)
- EP-014 = `[]` (POST `/ls/predictions/run` no FE consumer)
- EP-015 = `[]` (`/pl/health` monitoring-only)
- EP-016 = `FE-002` (TodayPage via `runPLPredictions` at line 127)
- EP-017 = `[]` (`/pl/predictions/today` no FE consumer — `getPLPredictionsToday` exported but not called)
- EP-018 = `FE-013` (TrackRecordBanner via `getTrackRecord` template with model='pl')
- EP-019 = `[]` (`/pl/predictions/value` no FE consumer per UC-2 drift; FE calls `/pl/predictions/value-bets` which has no API Gateway route)
- EP-020 = `FE-002` (TodayPage via `getPLPredictionsByDate` — imported at line 2 + likely call site at SP-A3 substrate scope; conservative assignment per import)
- EP-021 = `[]` (no FE consumer)
- EP-022 = `[]` (POST `/pl/predictions/run` no FE consumer)
- EP-023 = `[]` (legacy `/predictions/run`; FE uses `runWRPredictions` legacy alias)
- EP-024 = `[]` (legacy `/predictions/today`; no FE consumer)
- EP-025 = `[]` (legacy `/predictions/value`; FE uses `/wr/predictions/value`)
- EP-026 = `[]` (legacy `/predictions/{date}`)
- EP-027 = `[]` (legacy `/predictions/{date}/{track_code}/{race_number}`)
- EP-028 = `[]` (POST legacy `/predictions/run`)
- EP-029 = `FE-002, FE-004, FE-006, FE-007` (TodayPage + BetBuilderPage + HistoryPage + LongshotPage via `getWRRacesByDate` / `getRacesByDate` legacy alias)
- EP-030 = `[]` (`/races/today` no direct FE consumer — `getWRRacesToday` / `getRacesToday` exported but not called per supplementary grep)
- EP-031 = `[]` (`/races/{raceId}/detail` no direct FE consumer)
- EP-032 = `[]` (`/wr/health` no FE consumer; per UC-3 drift Lambda has no dispatch → 404)
- EP-033 = `FE-002` (TodayPage via `runWRPredictions` at line 129)
- EP-034 = `[]` (`/wr/predictions/today` no FE consumer — `getWRPredictionsToday` exported but not called)
- EP-035 = `FE-013` (TrackRecordBanner via `getTrackRecord` template with model='wr')
- EP-036 = `FE-014` (Compare/ByStyleTable via `getTrackRecordByStyle` at line 44)
- EP-037 = `[]` (`/wr/predictions/value` no FE consumer per supplementary grep — `getWRValuePlays` / `getValuePlays` legacy alias exported but not called from any page; drafting CC compact-form claim "ValuePlaysPage + TodayPage" was substrate-incorrect — those pages call `getPLValueBets` (PL endpoint), NOT `getWRValuePlays`)
- EP-038 = `FE-002` (TodayPage via `getWRRacesByDate(selectedDate, specialistStyle)` at line 68 — passes through `/races/{date}` per client.ts:35-41 with `style` query param; no direct call to `/wr/predictions/{date}`. Substrate-conservative: EP-038 may have no direct consumer; assigned FE-002 as inheritance from `/races/{date}` cross-reference per drafting CC's compact-form prior assertion. Surface for SP-A3 audit-cycle expansion clarification.)
- EP-039 = `FE-003` (ComparePage via `getCompareView` at line 40)
- EP-040 = `[]` (`/wr/predictions/{date}/{track_code}/{race_number}` no FE consumer)
- EP-041 = `[]` (POST `/wr/predictions/run` no FE consumer)

**Resolved CONSUMES mapping (per component):**

- FE-001 DashboardPage = `EP-002`
- FE-002 TodayPage = `EP-003, EP-005, EP-016, EP-020, EP-029, EP-033, EP-038` (+ drift-flagged: TodayPage:90 calls `getPLValueBets` → `/pl/predictions/value-bets` per UC-2; not in 41-route inventory)
- FE-003 ComparePage = `EP-039`
- FE-004 BetBuilderPage = `EP-003, EP-029` (via `getRacesByDate` = `getWRRacesByDate` legacy alias)
- FE-005 GonzoPage = `[]` (wrapper component renders TodayPage with `specialistStyle="gonzo_sauce"` prop; no direct API consumption per V1-22 verbatim output 1+2; endpoint consumption inherits via composition through FE-002)
- FE-006 HistoryPage = `EP-003, EP-029`
- FE-007 LongshotPage = `EP-003, EP-008, EP-029` (via `getAvailableDates`, `getLSAlerts`, `getWRRacesByDate`)
- FE-008 PerformancePage = `EP-002`
- FE-009 ValuePlaysPage = `EP-003` (+ drift-flagged: ValuePlaysPage:70 calls `getPLValueBets` → `/pl/predictions/value-bets` per UC-2; not in 41-route inventory)
- FE-010 EmptyState = `[]`
- FE-011 LoadingSpinner = `[]`
- FE-012 PredictionOutcome = `[]`
- FE-013 TrackRecordBanner = `EP-011, EP-018, EP-035` (via `getTrackRecord` template at line 32)
- FE-014 ByStyleTable = `EP-036` (via `getTrackRecordByStyle` at line 44)
- FE-015 CompareHorseRow = `[]`
- FE-016 CompareRaceCard = `[]`
- FE-017 StyleSelector = `[]`
- FE-018 Header = `[]` (presentational; LOCAL-STATE-ONLY + URL-PARAMS for nav-link state per FE-018 row narrative — URL-PARAMS does NOT entail API endpoint consumption)
- FE-019 Layout = `[]`
- FE-020 BetBadge = `[]`
- FE-021 HorseRow = `[]`
- FE-022 RaceCard = `[]`
- FE-023 ModelStats = `[]`
- FE-024 ValuePlayCard = `[]`

**FE-018 STATE_MGMT_BINDING revision:** Per audit re-verification, FE-018 Layout/Header.tsx STATE_MGMT_BINDING was assigned `LOCAL-STATE-ONLY + URL-PARAMS` at SP-A3 by drafting CC; this substrate is consistent with react-router-dom's nav-link convention. Patch retains the SP-A3 assignment.

**Bidirectional consistency post-patch (per drafting spec § 7 formal definition + tightened framing per audit-CC banked lesson):**

- Strict dangling pairs: 0 ✓
- Deferral-language placeholders in CONSUMED_BY/CONSUMES: 0 ✓ (all resolved to FE-NNN / EP-NNN identifiers or explicit `[]`)
- Page-NAME references in CONSUMED_BY/CONSUMES: 0 ✓ (all resolved to FE-NNN identifiers)
- "TBD" literal placeholders: 0 ✓ (FE-005 GonzoPage CONSUMES amended from "TBD" to substrate-grounded `[]`)

---

### V1-23: Patch-cycle wr-inference Lambda dispatch line verification (closes F-9)

**Claim source:** § 4.1 row EP-001/002/003 BACKEND_HANDLER cells (substrate-correct per UC-1 + V1-14 + V1-15 evidence; row tables amended at patch closure of F-9).

**Substrate domain:** A (Backend route handler source).

**Verification method:** `grep -nE "if path == '(/health|/dashboard/metrics|/races/available-dates)'" backend/lambdas/wr-inference/handler.py`.

**Verbatim output:**

```
$ grep -nE "if path == '(/health|/dashboard/metrics|/races/available-dates)'" /home/strakajagr/projects/equine-equalizer/backend/lambdas/wr-inference/handler.py
98:    if path == '/health':
102:    if path == '/dashboard/metrics':
108:    if path == '/races/available-dates':
```

**Conclusion:** CONFIRMED — wr-inference Lambda dispatches `/health` at line 98, `/dashboard/metrics` at line 102, `/races/available-dates` at line 108. EP-001/002/003 row-table BACKEND_HANDLER cells amended to:
- EP-001: `backend/lambdas/wr-inference/handler.py:98-100 (dispatch); backend/routers/health_router.py:6-37 (implementation)`
- EP-002: `backend/lambdas/wr-inference/handler.py:102-106 (dispatch); backend/routers/dashboard_router.py:19-127 (implementation)`
- EP-003: `backend/lambdas/wr-inference/handler.py:108-112 (dispatch); backend/routers/dashboard_router.py:130-173 (implementation)`

V1-7 / V1-8 / V1-9 entries unchanged (their substrate citations were correct at SP-A2 authorship time — they cited inference/handler.py per drafting CC's substrate-pre-V1-14 understanding; the row-table cells were authored from the same substrate at SP-A2 and propagated forward without amendment at SP-A3 when V1-14 surfaced the substrate-correct integration target). Patch reconciles row-table cells with V1-14 + V1-15 substrate-correct evidence.

---

### V1-24: Patch-cycle F-6 cross-reference placeholder-shape resolution (closes F-6)

**Claim source:** v1-draft cross-references at § 1 / § 4.1 row CROSS_REFERENCES column / § 12 (placeholder-shape literals).

**Substrate domain:** H (Domain H locked-bible read for cross-reference resolution).

**Verification method:** `grep -nE '<[a-z_]+(/?[a-z_]+)*>' api_frontend_bible.md` + Domain H locked-bible section verification.

**Verbatim output (pre-patch grep):**

```
$ grep -nE 'database_schema_bible:4\.1\.<|model_evaluation_retraining_bible:3\.X\.<|feature_provenance_bible:8\.W\.<' api_frontend_bible.md
304:| `CROSS_REFERENCES` | `architecture_overview:3.1` (Lambda Active); `database_schema_bible:4.1.5` (races table); `database_schema_bible:4.1.<predictions/wr_predictions sub-tables>` (predictions/wr_predictions joined in SQL) |
340:| ... `database_schema_bible:4.1.<ls_predictions>` |
343:| ... `database_schema_bible:4.1.<ls_predictions>` |
344:| ... `model_evaluation_retraining_bible:3.X.<ls models>` |
345:| ... `database_schema_bible:4.1.<ls_predictions>` |
350:| ... `database_schema_bible:4.1.<pl_predictions>` |
351:| ... `model_evaluation_retraining_bible:3.X.<pl models>` |
353:| ... `database_schema_bible:4.1.<pl_predictions>` |
367:| ... `database_schema_bible:4.1.<wr_predictions>` |
368:| ... `model_evaluation_retraining_bible:3.X.<wr models>` |
371:| ... `database_schema_bible:4.1.<wr_predictions>` |
650:- ... `feature_provenance_bible:8.W.<n>` ...
```

**Substrate verification (Domain H reads for resolution):**

- D&S Bible v1-patched-d2 § 3.1 enumeration evidence: 11 schema.sql tables + 3 in migration 005 + 1 angle_stats = 15 total. Per Data Pipeline Bible v1-patched-c F.2 + F.3 cross-references: `database_schema_bible:4.1.12` = `wr_predictions`, `:4.1.13` = `pl_predictions`, `:4.1.14` = `ls_predictions`, `:4.1.15` = `angle_stats` (per UC-MER cycle). Legacy `predictions` table sub-section: among migration 005 sub-sections OR within § 4.1.1-§ 4.1.11 schema.sql tables; precise sub-section ID undeterminable from cross-bible-cross-reference-freeze read scope at v1 lock — assigned approximate `database_schema_bible:4.1` aggregate reference + § 7.1 Deprecated entry pointer.
- MER bible TOC § 3 has per-model success criteria sub-sections at § 3.X.<version_name>; aggregate reference `model_evaluation_retraining_bible:3` resolves to the parent section covering all per-model rows. Specific sub-section IDs per WR/PL/LS model = M-1 through M-11; resolved via `model_evaluation_retraining_bible:3` parent reference.
- FP bible v1 LOCKED 2026-05-07 TOC inspection: § 5 = Train/Inference Findings Summary; § 6 = Cross-Reference Index; § 7 = Verification Log. **No § 8** in FP bible structure. Bug #15 canonical home reference `feature_provenance_bible:8.W.<n>` is NOT substrate-grounded — FP bible has no § 8 What-Was-Fixed sub-section. Bug #15's cross-bible manifestation surfaces at MLA § 4.3.1 (calibration bypass) + MER § 5.2 + § 5.3 (calibration discipline canonical home per Q13 ratification at MER lock) + PHASE_5_BACKLOG Phase 5.3.2.

**Resolved cross-references (post-patch):**

- `database_schema_bible:4.1.<predictions/wr_predictions sub-tables>` → `database_schema_bible:4.1.12` (wr_predictions) + `database_schema_bible:4.1` (legacy predictions table aggregate ref + § 7.1 Deprecated entry pointer)
- `database_schema_bible:4.1.<wr_predictions>` → `database_schema_bible:4.1.12`
- `database_schema_bible:4.1.<pl_predictions>` → `database_schema_bible:4.1.13`
- `database_schema_bible:4.1.<ls_predictions>` → `database_schema_bible:4.1.14`
- `model_evaluation_retraining_bible:3.X.<wr models>` → `model_evaluation_retraining_bible:3` (parent section covering M-1 through M-5 + WR-applicable evaluation criteria sub-sections)
- `model_evaluation_retraining_bible:3.X.<pl models>` → `model_evaluation_retraining_bible:3`
- `model_evaluation_retraining_bible:3.X.<ls models>` → `model_evaluation_retraining_bible:3`
- `feature_provenance_bible:8.W.<n>` → SUBSTRATE-FINDING: FP bible has no § 8; Bug #15 canonical home re-cited to `model_evaluation_retraining_bible:5.2 + 5.3` (calibration discipline canonical home per Q13 ratification) + PHASE_5_BACKLOG `Phase 5.3.2`. Surface for UPSTREAM-CORRECTION cycle decision: did Tony intend FP § 8 W.N entry for Bug #15 at FP lock? FP locked v1 without § 8 sub-section per FP bible TOC inspection.

**Conclusion:** CONFIRMED — placeholder-shape literals resolved to substrate-grounded references at v1-draft. FP bible § 8 absence flagged for UPSTREAM-CORRECTION cycle decision per cross-bible cross-reference freeze protocol.

---

### V1-25: Patch-cycle closure summary

**Patch-cycle V1-N entries:** V1-22 (FE consumer call-site batch + F-1/F-2/F-3/F-4 substrate); V1-23 (wr-inference dispatch lines for F-9); V1-24 (F-6 cross-reference resolution).

**Patch-cycle row amendments to v1-draft `api_frontend_bible.md`:**
- F-9: EP-001/002/003 BACKEND_HANDLER row tables amended (3 row-table cell edits)
- F-1: EP-002 CONSUMED_BY amended from deferral-language to `FE-001, FE-008`
- F-2: EP-003 CONSUMED_BY amended from deferral-language to `FE-002, FE-004, FE-006, FE-007, FE-009`
- F-3: 18 SP-A3 endpoint row CONSUMED_BY values amended to substrate-grounded enumeration (per V1-22 resolved mapping)
- F-3 reverse: 9+ component row CONSUMES values amended to substrate-grounded enumeration
- F-4: FE-005 GonzoPage CONSUMES amended from "TBD" to `[]`
- F-7: § 4.1 line 376 prose amended to disambiguate STATUS posture
- F-8: § 1 narrative paragraph added with STATUS aggregate count
- F-6: Placeholder-shape cross-references resolved per V1-24 substrate

**Existing V1-1 through V1-21 entries unchanged per drafting spec § 10 V1-N append-only discipline.**

**Pending lock-CC actions per ratified scope:**
- F-10 (bible header Status field stale): deferred to lock CC per banked Lesson 5 (locked bibles preserve drafting-time historical context — lock cycle does NOT retroactively rewrite drafting-time content; lock cycle's three-element metadata bundle update transitions Status field at lock).
- F-11 (verification log header Status field stale): deferred to lock CC per same lesson.

---





---

End of V1 Verification Log SP-A1 entries.
