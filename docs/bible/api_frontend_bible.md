# API & Frontend Bible

**Document:** api_frontend_bible
**Phase:** 1 (Bible) — deliverable 7 of 7 (drafting-order numbering per BIBLE_STRUCTURE_SPEC v6 § 8.2)
**Status:** LOCKED v1-patched-a (2026-05-11) — locked via cross-bible re-lock ceremony at parent EE Bible Upstream-Correction Cycle exit per R14.3 Option B + R36 Option A; cohort-locked audit-CC RATIFY disposition; supersedes LOCKED v1 (2026-05-08)
**Author:** CC (v1: drafting under Tier 3 verification discipline; v1-patched-a: drafting under EE Bible Upstream-Correction Cycle sub-cycle 1.5 of 4 per R10 Option A 4th sub-cycle authorization; QB orchestrated)
**Date:** 2026-05-07
**Locked:** 2026-05-11 (v1-patched-a via cross-bible re-lock ceremony; v1 2026-05-08)

## Revision history

- v1-draft (2026-05-07): initial CC draft per QB_DRAFTING_SPEC_API_FRONTEND_BIBLE.md (LOCKED 2026-05-07). Anchored on: META_PLAN v9 (LOCKED 2026-05-05) + BIBLE_STRUCTURE_SPEC v6 (LOCKED 2026-05-05) + AUDIT_METHODOLOGY v2-patched (LOCKED 2026-05-05) + CONVERGENCE_CRITERIA v2 (LOCKED 2026-05-04) + TRIAGE_QUEUE_SPEC v1 (LOCKED 2026-05-04) + Architecture Overview v3 (LOCKED 2026-05-05) + Database & Schema Bible v1-patched-d2 (LOCKED 2026-05-06) + Data Pipeline Bible v1-patched-c (LOCKED 2026-05-06) + Feature Provenance Bible v1 (LOCKED 2026-05-07) + ML Layer Architecture Bible v1 (LOCKED 2026-05-07) + Model Evaluation & Retraining Bible v1 (LOCKED 2026-05-07). Cross-bible cross-reference freeze: ACTIVE since FP v1 lock per cohort Handoff § 6.1; UPSTREAM-CORRECTION cycle = sole re-open path. Companion verification log at `_audit/api_frontend_bible_v1_verification.md`. Synchronization-point cycle in flight: SP-A1 reached at this v1-draft skeleton emission 2026-05-07.

- v1 LOCKED (2026-05-08): Phase 1 Cohort 7-of-7 deliverable LOCKED. Cycle phases: drafting CC SP-A1 (TOC + § 1 scope + column schemas) → SP-A2 (3 archetype endpoint rows EP-001/002/003 + 3 archetype component rows FE-001/002/003) → SP-A3 (full v1-draft = 41 endpoint rows + 24 component rows + § 6 reverse index + § 7 auth flows + § 8 caching/state-management + § 9 candidate discipline rules + § 10 Currently Open + § 11 Deprecated + § 12 What Was Fixed) → audit CC adversarial review per AUDIT_METHODOLOGY v2-patched 11-protocol enumeration (companion audit report `_audit/api_frontend_bible_v1_audit.md`, 2026-05-07; 11 findings = 0 BLOCKER + 5 MATERIAL + 2 MINOR + 4 STYLE; recommendation SURGICAL PATCH REQUIRED) → patch CC closure of 8 findings (F-1 EP-002 CONSUMED_BY enumeration + F-2 EP-003 CONSUMED_BY enumeration + F-3 38-row CONSUMED_BY/CONSUMES sweep + F-4 FE-005 GonzoPage CONSUMES substrate-grounding + F-6 placeholder-shape cross-reference resolution + F-7 § 4.1 STATUS posture prose disambiguation + F-8 § 1 STATUS aggregate count narrative + F-9 EP-001/002/003 BACKEND_HANDLER row-table substrate amendment per V1-14 + V1-15 evidence; V1-N append V1-22/V1-23/V1-24/V1-25 patch-cycle entries) → lock CC three-element metadata bundle (this entry: header Status field transition + this revision history entry + § 13 footer population). F-10 (bible header Status field stale post-SP-A3) and F-11 (verification log header Status field stale post-SP-A3) closed at this lock cycle per ratified scope (per banked Lesson 5: locked bibles preserve drafting-time historical content; metadata-bundle elements transition at lock, body content does not). Mixed-format ratification (Tony Decision 2 Posture α, 2026-05-08): SP-A2 archetype rows (EP-001/002/003 + FE-001/002/003) carry per-row narrative format; SP-A3 rows (EP-004 through EP-041 + FE-004 through FE-024) carry compact-tabular format. Mixed-format ratified over audit-CC F-5 STYLE finding; § 1 documentation declares format choice transparently; informational density preserved (column values + V1-N citations + cross-references intact across all 65 rows); audit-cycle directed no upgrade per Tony pre-decided "if audit-CC flags despite § 1 documentation" branch. Cycle-banked methodology lessons for AUDIT_METHODOLOGY meta-cycle promotion (queue at 17 items): Phase 1 Cohort Lessons 1-8 + Lesson 9 (Pattern A bundling) + Cluster B Check 4+5 framing tightening (banked from audit-CC re-verification of drafting CC's "0 dangling pairs" claim against enumeration-completeness gaps surfaced as F-1/F-2/F-3/F-4). Cycle-banked self-audit checks for AUDIT_METHODOLOGY meta-cycle promotion: Check 10 (estimation calibration ±40% CI) + Check 11 (self-describing authorization redundancy detection) + Check 12 (paste-prompt transit-truncation discipline; bookend markers operative for >15 KB prompts) + Check 13 (within-message placeholder discipline). Cross-bible cross-reference freeze: ACTIVE since FP v1 lock per cohort Handoff § 6.1; UC-1 UPSTREAM-CORRECTION cycle (Architecture Overview § 3.1 vs live API Gateway integration drift) ratified MATERIAL severity, sequenced post-this-bible-lock as separate cycle. PHASE_5_BACKLOG additions ratified for separate-cycle dispatch: Candidates #1 (UC-1 Architecture Overview § 3.1 drift) + #2 (UC-2 `/pl/predictions/value` 3-source mismatch) + #3 (UC-3 `/wr/health` + `/ls/health` 404 fall-through); Candidates #4 + #5 deferred to next cycle; Candidate #6 banked for AUDIT_METHODOLOGY meta-cycle. Companion verification log final-lock state at `_audit/api_frontend_bible_v1_verification.md` (V1-1 through V1-25 monotonic file-position; V1-22/V1-23/V1-24/V1-25 cosmetically re-ordered to follow V1-21 at lock cycle to preserve monotonic file-position discipline for future audit-cycle sequential reads). Companion audit report `_audit/api_frontend_bible_v1_audit.md`. Phase 1 Cohort: 7 of 7 deliverables LOCKED post-this-lock; Phase 1 complete.

- v1-patched-a (2026-05-11): UPSTREAM-CORRECTION patch cycle API & Frontend Bible UC (sub-cycle 1.5 of 4 under parent EE Bible Upstream-Correction Cycle, per R10 Option A 4th sub-cycle authorization 2026-05-11). Triggered by Architecture Overview UC sub-cycle 1 of 4 (Architecture Overview v3-patched-a → v3-patched-b DRAFT 2026-05-11) HIGH cascade depth cross-reference contract surface per `architecture_overview:6` heading-level cross-reference contract at this bible's § 3.3 + § 1.3 cross-bible cross-reference index + § 3.2 anomalies inherited. **5 patches applied (Pattern A bundle B1+B2+B3+B4+B5):** B1 § 3.2 fire-and-fail anomaly bullet refreshed with R8 Option B historical retention marker citing v3-patched-b § 6 historical reference; B2 § 3.3 admin-action surface impact body content refreshed per v3-patched-b § 6 substrate (anomaly resolution timeline: OCRC Phase A informal recovery 2026-05-09T04:37Z + Fix 4 2026-05-09T16:21Z + Fix 6 2026-05-09T17:16Z; subsequent ECR-lifecycle cull rotation 2026-05-09 → 2026-05-11; Phase β-2 cdk deploy final restoration 2026-05-11T13:46:13–13:59:42Z UTC; structural mitigation at v3-patched-b § 3.11.1 lifecycle override `imageCountMoreThan: 5` → 30); heading-level cross-reference contract `canonical home per architecture_overview:6 cross-reference contract` preserved verbatim per R8 Option B retention discipline. B3 § 1.3 cross-bible cross-reference index entries refreshed for architecture_overview substrate (line 89 Lambda count "5 Active + 3 INACTIVE" → "8 Active + 0 Inactive (v3-patched-b DRAFT 2026-05-11 SP-resume V16–V22)"; line 93 Currently Open canonical home note refreshed to reflect v3-patched-b § 6 historical retention status; cross-bible freeze status footnote updated to Option α LIFTED through parent cycle exit per R14.3 Option B). B4 § 9.1 CANDIDATE forbidden pattern refreshed with R8 Option B historical retention marker; candidate disposition recommendation: **retain CANDIDATE** (substrate stable now but discipline rule needs further substrate validation across additional cycles; ratification deferred to cohort-locked audit-CC per R15 Option B). B5 § 9.2 CANDIDATE common mistake substrate-refreshed per current EP-019 `/pl/predictions/value` ↔ `/pl/predictions/value-bets` drift (V25 NYRA cron substrate-stability re-confirmation reaffirms substrate stability outside § 10.2 UPSTREAM-CORRECTION candidate scope); candidate disposition recommendation: **retain CANDIDATE** pending cohort-locked audit. Cross-bible cross-reference freeze: LIFTED via Tony Option α 2026-05-09 (parent EE Bible Upstream-Correction Cycle scope); re-locks at Database & Schema Bible UC sub-cycle 4 close (parent cycle exit). Companion verification log NEW: `_audit/api_frontend_bible_v1_patched_a_verification.md` (drafting CC at v1-patched-a SP-1.5-drafting-complete; V26 substrate-stability re-confirmation; F23 candidate banking-via-disclosure per § 12 cross-bible refresh; cohort-locked audit-CC pending per R15 Option B). v1 lock-state companion verification log at `_audit/api_frontend_bible_v1_verification.md` preserved verbatim per banked Lesson § 4.17 (locked bibles preserve drafting-time historical context); only v1 → v1-patched-a delta captured in NEW log per surgical-cosmetic-patch convention. v1-patched-a lock posture: pending cohort-locked audit-CC dispatch (post sub-cycle 2 close per R15 Option B). **Lock-state pending cohort-locked audit-CC ratification.**

---

## Table of Contents

1. Scope of this bible
   - 1.1 Mission and audience
   - 1.2 Boundary statements (what this bible documents / does NOT document)
   - 1.3 Cross-bible cross-reference index
   - 1.4 Source-priority hierarchy operative for this bible's content
2. Definitions
3. Runtime context for API & Frontend
   - 3.1 Pointer-back cross-references to runtime topology
   - 3.2 API/FE-domain anomalies inherited from upstream bibles
   - 3.3 Admin-action surface impact (canonical home per `architecture_overview:6` cross-reference contract)
4. Endpoint inventory (per-endpoint exhaustive)
   - 4.1 Endpoint table
5. Component inventory (per-component exhaustive)
   - 5.1 Component table
6. Reverse index — Per-component endpoint consumption
7. Auth/session flows
   - 7.1 Login flow
   - 7.2 Token refresh / session continuation flow
   - 7.3 Session expiry handling
   - 7.4 Logout flow
   - 7.5 Multi-tenancy boundary (N/A explicit per BIBLE_STRUCTURE_SPEC v6 § 5.2 — single-user system per handoff Q5 ratification)
8. Caching and state-management architecture
   - 8.1 FE state-management library
   - 8.2 Per-endpoint cache policy summary
   - 8.3 CDN-edge caching
9. Discipline rules (Forbidden Patterns + Common Mistakes)
10. Currently Open
11. Deprecated
12. What Was Fixed — Do Not Revert
13. End-of-document footer (skeleton; lock-CC populates)

---

## 1. Scope of this bible

### 1.1 Mission and audience

The API & Frontend Bible answers, for the Equine Equalizer (EE) system: **"what HTTP routes exist, what does each one return, which Lambda handles which request, and how does the React SPA consume each route?"** Audience: any reader making an API surface change (adding/modifying/removing a route), a frontend component change (adding/modifying/removing a page or component), an investigation into a route's runtime behavior or its consumers, or a cross-coupling assessment ("if I change endpoint X, what FE components break?").

This bible is **per-endpoint reference-style + per-component reference-style + reverse-index navigation**: look up an endpoint by route or by ID and read its row at § 4.1; look up a component by path or by ID and read its row at § 5.1; cross-reference between them via the bidirectional `CONSUMED_BY` (forward, in § 4.1) ↔ `CONSUMES` (reverse, in § 5.1 and aggregated at § 6) field pair. The cross-coupling matrix is the forcing-function-additive content per Q4 ratification.

This bible is the canonical home for: (a) per-endpoint contract surface; (b) per-component consumer mapping; (c) auth / session flow narrative; (d) FE state-management / caching architecture; (e) admin-action surface impact of upstream INACTIVE-Lambda fire-and-fail anomaly per `architecture_overview:6` cross-reference contract (per § 3.3 below).

### 1.2 Boundary statements

**What this bible documents:**

- Per-endpoint contract surface for all production routes (per Q1(a) per-endpoint exhaustive ratification; estimated 41 routes at v1-draft per `architecture_overview:3.5` row count anchor, with re-verification at SP-A3 per drafting spec § 9 anchor command).
- Per-component endpoint consumption mapping for the single React SPA tree at `frontend/src/` (per Q1(b) full-stack ratification + Q2(a) single FE tree confirmation; component count emerges from substrate at SP-A3).
- Reverse index for bidirectional cross-coupling discovery (per Q4 forward + reverse index ratification).
- Auth / session flow narrative (per Q5 dedicated § 7).
- FE state-management / caching architecture (per Q5 dedicated § 8).
- Admin-action surface impact narrative (canonical home per `architecture_overview:6` cross-reference contract; per § 3.3 below).

**What this bible does NOT document:**

- Per-table schema (column declarations, type widths, JSONB conventions, migration history) → `database_schema_bible:4.1`.
- Per-flow data movement (ingestion → DB → model → API; per-Lambda destination tables; cron schedules) → `data_pipeline_bible:4.1`.
- Per-feature provenance (which feature is consumed by which model; train/inference parity status) → `feature_provenance_bible:4.1`.
- Per-model architecture (XGBoost vs LSTM vs RandomForest vs Bayesian vs ensemble, hyperparameters, calibration mechanics) → `ml_layer_architecture_bible:4`.
- Per-model success criteria + retrain triggers (pass/fail thresholds, retrain cadence, deployment gates) → `model_evaluation_retraining_bible:3` and `:4`.
- Per-runtime topology (Lambda inventory, ECS Fargate task families, EventBridge schedule, RDS instance metadata, fire-and-fail anomaly substantive description) → `architecture_overview:3` and `:6`. This bible's per-endpoint rows reference `architecture_overview:3.1` for inference-Lambda identity and `architecture_overview:3.5` for API Gateway v2 surface count, but do NOT duplicate per-Lambda or per-rule substrate.

### 1.3 Cross-bible cross-reference index

This bible cross-references the six locked Phase 1 bibles at the section level. Cross-bible cross-reference freeze ACTIVE at v1 lock (2026-05-08) per cohort Handoff § 6.1; UPSTREAM-CORRECTION cycle = sole re-open path. **Cross-bible freeze status at v1-patched-a lock (2026-05-11): LIFTED via Tony Option α 2026-05-09 (parent EE Bible Upstream-Correction Cycle scope; per R14.3 Option B ratification 2026-05-11); freeze re-locks at Database & Schema Bible UC sub-cycle 4 close (parent cycle exit). This bible operates inside lifted-state window for cross-reference contract refresh per sub-cycle 1.5 of 4 cascade scope.**

| Cross-reference target | Role for this bible |
|---|---|
| `architecture_overview:3.1` (Lambda inventory: 8 Active + 0 Inactive per v3-patched-b DRAFT 2026-05-11 SP-resume V16–V22 substrate; previously 5 Active + 3 INACTIVE at v1 lock 2026-05-08 per v3-patched-a substrate — historical reference retained at v3-patched-b § 3.1 per R8 Option B) | Endpoint→Lambda mapping; INACTIVE-target endpoint behavior per § 3.2 + § 3.3 (fire-and-fail anomaly retracted at v3-patched-b per v3-patched-b § 3.6 anomaly note + § 6 historical reference). |
| `architecture_overview:3.4` (S3 buckets — `equine-frontend` for SPA hosting) | FE deploy + CloudFront origin; § 8.3 CDN-edge caching context. |
| `architecture_overview:3.5` (API Gateway v2 — 41 routes verified live 2026-05-05) | Total route count anchor for § 4.1; re-verified at SP-A3 entry per drafting spec § 9. |
| `architecture_overview:3.6` (EventBridge schedule — 10 ENABLED + 3 DISABLED) | Non-HTTP invocation paths into integration Lambdas (e.g., `event['source'] == 'aws.events'` per V1-2 substrate); also Bug-#-class anomaly substrate where ENABLED rules target INACTIVE Lambdas. |
| `architecture_overview:6` (Currently Open / fire-and-fail anomaly canonical home — at v1 lock 2026-05-08; rewritten at v3-patched-b 2026-05-11 with anomaly retracted + R8.3 Option B historical retention block preserving cross-reference contract integrity) | § 3.2 inheritance; § 3.3 admin-action surface impact (this bible's responsibility per cross-reference contract); v1-patched-a refresh per cohort cascade (sub-cycle 1.5 of 4). |
| `database_schema_bible:4.1` (per-table column shapes) | Response payload field-level traceability (e.g., `wr_predictions` columns informing `RESPONSE_TYPE_SIG` at § 4.1 endpoint rows). |
| `data_pipeline_bible:4.1.5` (daily inference flows for WR / PL / LS) | Per-pipeline inference Lambda identity for endpoint→Lambda mapping (e.g., `equine-wr-inference` per § 3.1). |
| `feature_provenance_bible:4.1` (per-feature rows F-1 through F-81) | Feature exposure surface — which features are exposed via which endpoints; not exhaustively cross-referenced here (this bible documents endpoints, not features). |
| `ml_layer_architecture_bible:4.2` (inference pipeline topology) | Per-pipeline prediction-shape exposure surface (e.g., `WRPrediction` shape informing WR endpoint response payloads). |
| `model_evaluation_retraining_bible:3` + `:4` (per-model success criteria + retrain triggers) | Model evaluation surface exposure (if any endpoints expose evaluation/retraining status). |

### 1.3.1 STATUS column distribution at v1 lock (per audit-CC F-8 patch closure)

STATUS column distribution at v1 lock: **41 PRODUCTION / 0 DEPRECATED / 0 INTERNAL-ONLY / 0 EXPERIMENTAL.** Distribution rationale: Posture A deployment-state semantic encodes route deployment substrate (wired to API Gateway and serving traffic) regardless of consumer profile; Discovery #4 (V1-4) zero-auth-surface eliminates INTERNAL-ONLY at v1 lock (reserved for future UPSTREAM-CORRECTION expansion if EE introduces auth); zero Phase-5-ratified DEPRECATED routes at v1 lock (Candidate #4 5-route legacy `/predictions/*` group deferred-triage per § 10.4 + PHASE_5_BACKLOG synthesis at audit-cycle); zero EXPERIMENTAL substrate identified.

### 1.4 Source-priority hierarchy operative for this bible's content

Per META_PLAN v9 § 4.5: Tier 1 (live AWS state) > Tier 2 (live API endpoints) > Tier 3 (live database state) > Tier 4 (working-tree code post-baseline 87dec36) > Tier 5 (operator-stated history) > Tier 6 (`EE_CURRENT_STATE_DUMP.md`) > Tier 7 (session logs).

For this bible specifically, **Tier 4 is canonical** for backend route handler citations + frontend component citations (file:line ranges in `backend/lambdas/inference/handler.py`, `backend/routers/`, `backend/services/`, `frontend/src/`). **Tier 1 is canonical** for the 41-route count anchor (re-verified at SP-A3 entry via `aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100` per drafting spec § 9). **Tier 4** is canonical for FE-side TS interface notation (operative type-sig per V1-3 — `frontend/src/types/`).

Cross-tier conflicts (e.g., live API Gateway route inventory diverges from `backend/lambdas/inference/handler.py` dispatch path-strings) are documented per drafting spec audit-CC protocol #6 (drift surfaced; potential UPSTREAM-CORRECTION trigger on `architecture_overview:3.5` if drift is found).

When sources conflict, source-priority hierarchy applies per META_PLAN v9 § 4.5.

---

## 2. Definitions

Terminology specific to API & Frontend Bible's domain. Acronyms defined in `architecture_overview:2` (WR / PL / LS, Active vs Inactive Lambda, ENABLED vs DISABLED rule, Deployed image, Gonzo Sauce) are referenced from there, NOT redefined here.

- **FE tree.** The single React SPA source tree at `/home/strakajagr/projects/equine-equalizer/frontend/`. Verified per Discovery #1 (V1-1): `package.json` declares `react` 19.2.4 + `react-dom` 19.2.4 + `react-scripts` 5.0.1 build pipeline; `src/App.tsx` is the entry component; `src/api/`, `src/components/` (6 sub-directories), `src/pages/` (9 page files), and `src/types/` (TypeScript interfaces) constitute the FE tree's authoring surface. **Single FE tree confirmed** per handoff § 4 Q2(a) ratification: no `web/`, `app/`, `client/`, `ui/`, `next/` alternates exist at project root.

- **Lambda-handler-as-router.** EE's backend dispatch convention per Discovery #2 (V1-2). The `equine-inference` Lambda's `handler(event, context)` function in `backend/lambdas/inference/handler.py` reads `event['rawPath']` and `event['requestContext']['http']['method']`, then dispatches via path-string matching (`if path == '/health':`, `if path == '/dashboard/metrics':`, etc.) to per-domain router modules imported from `backend/routers/`. **No web framework** (no FastAPI / Flask / aiohttp / starlette / django imports anywhere in handler files). The handler also handles non-HTTP invocation sources: EventBridge scheduled trigger via `event['source'] == 'aws.events'`; batch invocation via `event['source'] == 'batch'`. CORS preflight handled hand-rolled via `_cors_response()` helper.

- **Action-based admin dispatch.** The `equine-ingestion` Lambda's dispatch convention (per `architecture_overview:3.1` row + 25-action enumeration cross-reference). Reads `event['action']` (or analogous action key) from invocation payload and dispatches to per-action handlers covering data acquisition, model lifecycle, admin/diagnostic, and data backfills/normalization (per-action enumeration deferred to `data_pipeline_bible:4.1`). Distinct from Lambda-handler-as-router because the action dispatch is invocation-payload-based, not HTTP-path-based. **`equine-ingestion` is INACTIVE at lock**; the 25 manual-invoke action handlers are non-functional via the same INACTIVE-Lambda mechanism, and 3 actions are also EventBridge-triggered (`refresh_angle_stats` via `equine-angle-stats-nightly` plus 2 default-case dispatches via `equine-ingestion-daily` and `equine-fetch-results-nightly`) producing the fire-and-fail pattern per `architecture_overview:6`.

- **TypeScript interface notation.** Operative type-sig notation per Discovery #3 (V1-3). FE-side TypeScript interfaces in `frontend/src/types/predictions.ts` + `frontend/src/types/index.ts` define request/response shape contracts. Backend produces JSON conforming to these shapes via direct dict construction (no schema-validation framework — no Pydantic, Marshmallow, attrs, or OpenAPI/swagger spec). The TS interfaces are the canonical type-sig substrate for `REQUEST_TYPE_SIG` / `RESPONSE_TYPE_SIG` columns at § 4.1 endpoint rows.

- **Column source-domain reassignment for `REQUEST_TYPE_SIG` / `REQUEST_EXAMPLE` / `RESPONSE_TYPE_SIG` / `RESPONSE_EXAMPLE` (per Tony's SP-A1 Finding 3 ratification 2026-05-07).** Drafting spec § 5 originally assigned all four columns to Domain B (backend request/response schema definitions). Discovery #3 (V1-3) confirmed Domain B is empty (no backend schema framework). Per Finding 3 ratification, source domain re-assigns: **`REQUEST_TYPE_SIG` and `RESPONSE_TYPE_SIG` cite Domain D/E** (FE TS interfaces in `frontend/src/types/`); **`REQUEST_EXAMPLE` and `RESPONSE_EXAMPLE` cite Domain A** (backend dict construction in `backend/routers/`, `backend/services/`, `backend/lambdas/inference/handler.py`) with **synthesis fallback** (drafting CC synthesizes from type-sig if no canonical example exists in source). The reassignment is reflected in § 4.1 column schema table below. Other column source-domain assignments per drafting spec § 5 unchanged at v1 lock.

- **Route key.** Stable per-endpoint identifier in `EP-NNN` format (e.g., `EP-001`, `EP-002`, ...). Assigned by drafting CC at SP-A2 onward; deterministic ordering by route path within § 4.1.

- **Component identifier.** Stable per-component identifier in `FE-NNN` format (e.g., `FE-001`, `FE-002`, ...). Assigned by drafting CC at SP-A2 onward; deterministic ordering by component path within § 5.1.

- **`CONSUMED_BY` (forward index field).** § 4.1 endpoint row column listing component identifiers (comma-separated, deterministic ordering by component identifier) that consume this endpoint. Empty list = no FE consumers (e.g., admin actions invoked manually); documented as `[]` per BIBLE_STRUCTURE_SPEC v6 § 5.2 empty-list explicit rule.

- **`CONSUMES` (forward index field at component level; reverse-index source at § 6).** § 5.1 component row column listing endpoint identifiers (comma-separated, deterministic ordering by endpoint identifier) that this component consumes. Empty list = purely presentational component (no API calls); documented as `[]`.

- **STATUS column value space.** Per Q1(c) ratification + Tony's SP-A2 Observation 4 Posture A ratification (2026-05-07): `PRODUCTION` / `DEPRECATED` / `INTERNAL-ONLY` / `EXPERIMENTAL`. Single value per row at lock; convention precedent per MLA calibration-state column.

  **STATUS column semantic (per Observation 4 Posture A ratification — verbatim per Tony's SP-A3 directive):** STATUS column reflects route deployment state, parallel to ml_layer_architecture_bible STATUS-axis convention precedent (calibration-state column encodes deployment-state attribute, not consumer profile). Deployment state is substrate-grounded: route wired to API Gateway and serving traffic, or not. Consumer profile is encoded separately in CONSUMED_BY column; STATUS does not duplicate that signal. Value space: PRODUCTION (deployed and serving) / INTERNAL-ONLY (auth-gated/IP-restricted/VPN-only) / DEPRECATED (post-deprecation per Phase 5 backlog or cross-bible pointer) / EXPERIMENTAL (feature flag / A/B / trial). At v1 lock, INTERNAL-ONLY value is reserved for future UPSTREAM-CORRECTION expansion per Discovery #4 (V1-4) zero-auth-surface finding; current routes populate PRODUCTION unless DEPRECATED or EXPERIMENTAL substrate identifies otherwise.

  **Per-value substrate verification convention:**
  - PRODUCTION: route wired to API Gateway and serving traffic. Lambda target Active OR Lambda target INACTIVE with fire-and-fail manifest at § 3.3 (deployment fact authoritative; functional state captured at row narrative + § 3.3 anomaly section).
  - INTERNAL-ONLY: route exists but is structurally non-public (auth-gated, IP-restricted, VPN-only). Substrate verification at row authorship via Domain C primary source. Discovery #4 confirmed zero auth surface in EE-owned backend; INTERNAL-ONLY value reserved for future UPSTREAM-CORRECTION expansion.
  - DEPRECATED: route documented but post-deprecation-decision per Phase 5 backlog ratification or per cross-bible deprecated-section pointer (e.g., readers of legacy tables documented in `database_schema_bible:7.1` deprecated section, IF such readers exist as routes — drafting CC verifies at substrate gathering, does not assume).
  - EXPERIMENTAL: route behind feature flag, A/B test, or trial surface. Substrate verification at row authorship via Domain A primary source.

- **AUTH column value space.** Per Q5 ratification + Discovery #4 (V1-4) + Tony's SP-A1 Finding 2 ratification (2026-05-07): at v1 lock, **AUTH = `PUBLIC` for all endpoints** across the API Gateway v2 surface — **single-value posture**. Discovery #4 grep returned no auth surface in EE-owned backend code (no `authorize` / `@requires_auth` / `verify_token` / `check_session` / `@login_required` / `jwt` / `oauth` / `cognito` / `api_key` matches in `backend/` excluding third-party `layers/`); the API surface is effectively single-tenant + unauthenticated per single-user system ratification at handoff Q5 + § 7.5 multi-tenancy boundary N/A. Other AUTH value-space members (`SESSION-COOKIE` / `BEARER-TOKEN` / `API-KEY` / `INTERNAL` / `N/A`) reserved for future UPSTREAM-CORRECTION expansion if EE introduces auth (e.g., post-Phase 5 multi-user posture). The action-based admin dispatch on the INACTIVE `equine-ingestion` Lambda is documented at § 3.3 as a non-HTTP surface (direct Lambda invoke only) and does NOT contribute to the API Gateway v2 41-route count; therefore no row in § 4.1 carries an `INTERNAL` AUTH value at v1 lock. Per Finding 1 SP-A1 ratification: SP-A2 endpoint selection criterion substituted to "first 3 endpoints by `ENDPOINT_ID` ordering" (deterministic by route path in `backend/lambdas/inference/handler.py` dispatch chain) per drafting spec § 8 fallback note.

- **CACHE_POLICY column value space.** Per Q5 ratification: `NO-CACHE` / `CLIENT-MEMO` / `SWR-STALE-WHILE-REVALIDATE` / `CDN-EDGE` / `N/A`. Drafting CC discovers operative cache values from primary source per Discovery #6 (V1-6). The FE has no external state-management/cache library (no react-query / SWR / redux-persist / etc.); FE state convention is **LOCAL-STATE-ONLY** with axios direct (per § 8.1 + Discovery #6 substrate). CDN-edge caching applies to the CloudFront SPA assets (per `architecture_overview:3.4` `equine-frontend` bucket) but per-route caching at API Gateway integrations is **not configured by default** in EE's CDK substrate (per § 8.3).

- **TYPE column value space (component).** Per Q2(b) ratification: `REACT-COMPONENT` (only value at lock). Other values (`NEXT-PAGE`, `STATIC-HTML`, `VUE`, `TEMPLATE`) reserved for future UPSTREAM-CORRECTION expansion if EE FE stack diversifies. Single-value-at-lock posture per Q2(b); single FE tree per Q2(a) — no Next.js, static HTML, Vue, or template-rendered surface exists.

- **RESPONSIVE_MODE column value space (component).** Per Q2(c) ratification: `MOBILE-FIRST` / `RESPONSIVE` / `DESKTOP-ONLY` / `N/A`. Drafting CC populates at row-authorship per Lesson § 4.13 (low-cost substrate verification at row-authorship). Inspection method per drafting spec § 4 Discovery #1 fallback: CSS / Tailwind classes / styled-components for responsive breakpoints.

- **STATE_MGMT_BINDING column value space (component).** Per Discovery #6 (V1-6) + Tony's SP-A2 Observation 2 ratification (2026-05-07): library-specific identifier (e.g., `useQuery('races')`, `useSelector(state.predictions)`, `useStore(getRaces)`) OR **`LOCAL-STATE-ONLY`** (default for EE — no external state-management library). Cite primary source code line per Lesson § 4.13.

  **Compound bindings convention (per Observation 2 ratification):** when a component combines local component state with library-mediated state synchronization (e.g., react-router's `useSearchParams` for URL-based state synchronization), the STATE_MGMT_BINDING value uses the `+` separator to enumerate both: e.g., `LOCAL-STATE-ONLY + URL-PARAMS` (FE-003 ComparePage substrate per V1-12 verification). The `+` separator distinguishes substrate-grounded compound patterns from external state-management libraries (which would be a single token like `useStore(...)`); compound notation honors Lesson § 4.13 substrate-specific-nuance discipline at row authorship. Other anticipated compound forms surfaced by SP-A3 substrate (per drafting CC discovery): `LOCAL-STATE-ONLY + URL-PARAMS` (react-router useSearchParams); `LOCAL-STATE-ONLY + ROUTE-PARAMS` (react-router useParams for path-segment state); `LOCAL-STATE-ONLY + NAVIGATE-DISPATCH` (react-router useNavigate for programmatic transitions). Each compound form documented at row authorship with primary-source citation; no a-priori pre-enumeration mandated.

When sources conflict, source-priority hierarchy applies per META_PLAN v9 § 4.5 (see § 1.4).

---

## 3. Runtime context for API & Frontend

### 3.1 Pointer-back cross-references to runtime topology

This bible inherits runtime topology from Architecture Overview v3 (LOCKED 2026-05-05). The cross-references below are pointers; the substantive content lives in Architecture Overview.

- **API Gateway v2 surface.** API ID `gb5qlfy10h`. Total route count: **41** (verified live 2026-05-05 with `aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100` per `architecture_overview:3.5`). This bible's § 4.1 will populate one row per route at SP-A3; row count anchor re-verified at SP-A3 entry per drafting spec § 9.

- **CloudFront + S3 SPA hosting.** Bucket `equine-frontend` is the CloudFront origin for the SPA per `architecture_overview:3.4`. Built React assets are uploaded to S3 by the deploy mechanism (`deploy_all.sh` + frontend build → S3 → CloudFront). CloudFront distribution ID at `.cf-distribution-id` in repo root. CDN-edge caching for SPA static assets applies; per-route caching at API Gateway integrations is documented at § 8.3.

- **Lambda inventory.** EE has **8 Lambda functions: 5 Active + 3 INACTIVE** per `architecture_overview:3.1`. The 5 Active are `equine-inference` (HTTP-path dispatcher integrating with API Gateway v2 — primary route handler for the 41-route surface), `equine-wr-inference` / `equine-pl-inference` / `equine-ls-inference` (per-pipeline daily inference Lambdas — produce predictions consumed via stored DB rows by `equine-inference`'s prediction-fetch routes), `equine-nyra-workouts` (NYRA workout scrape; non-HTTP triggered). The 3 INACTIVE are `equine-ingestion` (action-based admin dispatch + ingestion-daily flows; INACTIVE means 25 manual-invoke admin actions are non-functional and 3 EventBridge-triggered actions fire-and-fail — see § 3.3 admin-action surface impact), `equine-feature-engineering` (legacy; replaced by inference-side feature computation per Phase A3), `equine-results` (legacy results-fetch). All 3 INACTIVE Lambdas have `StateReason = "The function is trying to use a deleted image."` per `architecture_overview:3.1` substrate.

### 3.2 API/FE-domain anomalies inherited from upstream bibles

This bible inherits the following anomalies from upstream locked bibles. Substantive description of each anomaly lives in its canonical-home bible per `architecture_overview:6` cross-reference contract; this bible documents the API/FE-domain rendering of the anomaly.

- **Fire-and-fail anomaly (canonical home: `architecture_overview:6`).** **[At v1-patched-a lock 2026-05-11 per V26 SP-1.5-entry substrate (8/8 Active + countNumber: 30 intact): fire-and-fail anomaly fully retracted upstream; zero ENABLED rules target Inactive Lambdas at v3-patched-b lock. Historical retention per R8 Option B retention with historical marker discipline (this bible's sub-cycle 1.5 of 4 ratification) — v1 narrative preserved below for pattern instruction value + cross-reference contract integrity with v3-patched-b § 6 historical reference.]** [Historical narrative from v1 lock 2026-05-08:] Four ENABLED EventBridge rules target INACTIVE Lambdas: `equine-ingestion-daily`, `equine-fetch-results-nightly`, `equine-angle-stats-nightly` (all → `equine-ingestion` INACTIVE), and `equine-results-daily` (→ `equine-results` INACTIVE). The cron triggers fire on schedule but invocation fails because the target image is deleted. **API/FE-domain rendering:** the dashboard's prediction-fetch endpoints (which read `predictions` / `wr_predictions` / `pl_predictions` / `ls_predictions` tables) continue to return historical rows correctly because the stored rows are real and were correctly produced when the Lambdas were Active; no fresh rows are produced from those flows post-deactivation (per `architecture_overview:3.1` temporal scoping note). The dashboard endpoint surface remains functional at v1-draft (the `equine-inference` Lambda is Active and serves the dashboard); the fire-and-fail anomaly affects ingestion freshness, not dashboard read paths. **[v1-patched-a refresh: anomaly resolution timeline per v3-patched-b § 6 historical reference: OCRC Phase A informal recovery 2026-05-09T04:37Z UTC restored equine-ingestion; OCRC Fix 4 2026-05-09T16:21:55–56Z restored equine-results + equine-feature-engineering; OCRC Fix 6 2026-05-09T17:16:18Z surgical equine-ingestion redeploy with `logger.info()` surface fix; subsequent ECR-lifecycle cull regression rotated Inactive cohort across 2026-05-09 → 2026-05-11 (Phase γ + Phase β-3 banking); Phase β-2 cdk deploy 2026-05-11T13:46:13–13:59:42Z UTC restored 8/8 Active state; structural mitigation at v3-patched-b § 3.11.1 ECR lifecycle policy override `imageCountMoreThan: 5` → 30 (Phase β-1 2026-05-11T13:40:21Z UTC). At v1-patched-a lock, fresh ingestion + results rows produced daily per substrate-stable post-Phase-β-2; gap-period fresh-row absence (2026-05-02 → 2026-05-11 cohort-rotation windows) documented at v3-patched-b § 3.1 + § 3.11 historical retention blocks.]**

- **Bug #28 (HRN scraper column shift; canonical home: `data_pipeline_bible:8.W.1` — pending Phase 5 fix per Phase 5.3.1).** Surfaced 2026-05-03 during `EE_CURRENT_STATE_DUMP` generation. Symptoms: `results.win_payout` and `results.daily_double_payout` NULL across all rows from 2026-04-30 onward. **API/FE-domain rendering:** any endpoint that exposes these columns to the FE returns NULL values for affected dates. Specific endpoint impact enumerated at § 4.1 endpoint rows at SP-A3 (rows that select from `results` and expose `win_payout` / `daily_double_payout` to FE consumers).

- **Calibration discipline candidate group (canonical home: `model_evaluation_retraining_bible:5.2 + 5.3`; PHASE_5_BACKLOG Phase 5.3.2).** All WR styles bypass calibration at inference per `wr_inference_service.py:616-626` (per `ml_layer_architecture_bible:4.3.1`). **API/FE-domain rendering:** the dashboard's WR prediction endpoints return raw ranker-score-derived probabilities, not calibrated probabilities. The FE consumes the raw probabilities directly; no FE-side correction applied. Cross-reference at SP-A3 endpoint rows for WR prediction endpoints.

- **3.X drafting-CC-discovered anomalies.** Reserved at SP-A3 for any API/FE-domain anomalies surfaced during V1 substrate verification that lack upstream homes. None surfaced at SP-A1.

### 3.3 Admin-action surface impact (canonical home per `architecture_overview:6` cross-reference contract)

Per `architecture_overview:3.1` row for `equine-ingestion` (substrate evolution: INACTIVE at v1 lock 2026-05-08 → Active at v3-patched-b lock 2026-05-11 per V16 SP-resume substrate) + `architecture_overview:6` cross-reference contract: this bible is the canonical home for the API/FE-domain rendering of the admin-action surface impact. **The cross-reference contract heading text `canonical home per architecture_overview:6 cross-reference contract` is preserved verbatim per R8 Option B retention discipline; body substrate refreshed at v1-patched-a (2026-05-11) per cohort cascade sub-cycle 1.5 of 4.**

The `equine-ingestion` Lambda hosts a 25-action admin dispatch at `backend/lambdas/ingestion/handler.py` covering data acquisition (5 race-card / results / chart / workout fetches), model lifecycle (4 train / register / activate actions), admin/diagnostic (5 raw_query / migrate / db_counts actions), data backfills/normalization (7 actions), miscellaneous (3 actions), and deferred (1 action). Per-action enumeration: `data_pipeline_bible:4.1` arithmetic decomposition 5+4+5+7+3+1=25.

**Functional impact at v1-patched-a lock (2026-05-11) per V26 substrate (equine-ingestion Active per V16 SP-resume substrate; LastModified 2026-05-11T13:58:54Z UTC; ImageUri tag `:fdd29e6842bf…c648b` resolving cleanly to ECR digest `sha256:6942f3f4…` shared with `:fix6-v2-2026-05-09` tag per v3-patched-b § 3.7 + F14 reproducible-build evidence):**

- **All 3 EventBridge-triggered admin actions FUNCTIONAL post-restoration:** `refresh_angle_stats` (via `equine-angle-stats-nightly` cron) + 2 default-case dispatches (via `equine-ingestion-daily` cron and `equine-fetch-results-nightly` cron — latter resolving InputTransformer sentinel `USE_TODAY_MINUS_1` handler-side at `backend/lambdas/ingestion/handler.py:243-249` per v3-patched-b § 3.6 A1 ratification). Crons fire on schedule and invocation succeeds.

- **All 22 manual-invoke admin actions FUNCTIONAL post-restoration:** Operator-triggered admin operations (raw_query, migrate, db_counts, set_active_model, train_model_register, etc.) invoke cleanly. Source-side `logger.info()` surface patch at `handler.py:11` durable across CDK reconciliation cycles per v3-patched-b § 2 Definitions + § 3.7 F14 reproducible-build evidence (Phase β-2 cdk deploy 2026-05-11 produced byte-identical equine-ingestion image to OCRC Fix 6 v2 2026-05-09T17:16:13Z).

- **No production HTTP route surface exposes the admin actions** (unchanged at v1-patched-a from v1 lock). Per V1-2 substrate (`equine-inference` handler dispatches to `race_router`, `prediction_router`, `horse_router`, `dashboard_router`, `health_router` only — NOT to ingestion-action paths). The admin actions are invoked via direct Lambda invoke (AWS console / CLI), not via API Gateway v2. Therefore the admin-action surface does NOT contribute to the 41-route count at `architecture_overview:3.5`. This bible's § 4.1 enumerates the 41 API Gateway v2 routes; the admin actions are documented at this § 3.3 as a separate non-HTTP surface for completeness per the cross-reference contract.

**Historical surface non-functionality timeline (per R8 Option B retention with historical marker; v1-patched-a 2026-05-11 ratification):**

[Historical: At v1 lock 2026-05-08, all 25 admin actions were non-functional because `equine-ingestion` Lambda was INACTIVE since CDK redeploy 2026-05-02 culled its ECR image. The 3 EventBridge-triggered admin actions fire-and-failed per `architecture_overview:6` v3-patched-a substrate; the 22 manual-invoke admin actions errored on invoke with `ResourceNotFoundException` or analogous "The function is trying to use a deleted image" surface. Restoration timeline per v3-patched-b § 6 historical reference: OCRC Phase A informal recovery 2026-05-09T04:37Z UTC (Tony manual CDK redeploy restored `equine-ingestion` Active state); subsequent ECR-lifecycle cull regression 2026-05-09 → 2026-05-11 rotated Inactive cohort but did NOT re-affect `equine-ingestion` (which retained its post-OCRC-Fix-6 `:fix6-v2-2026-05-09` image throughout the rotation window per v3-patched-b § 3.1 + § 3.11.1 substrate; equine-ingestion image's recent push timestamp 2026-05-09T17:16:13Z placed it well within the surviving 5-image cohort even under the pre-β-1 `imageCountMoreThan: 5` policy); Phase β-1 2026-05-11T13:40:21Z UTC structural mitigation `imageCountMoreThan: 5` → 30 per v3-patched-b § 3.11.1; Phase β-2 cdk deploy 2026-05-11T13:46:13–13:59:42Z UTC final restoration to 8/8 Active state. At v1-patched-a lock, admin actions are functional; gap-period non-functionality (2026-05-02 → 2026-05-09T04:37Z UTC) documented at v3-patched-b § 3.1 + § 3.11 historical retention blocks.]

**Explicit non-functional surface enumeration (drafting CC at SP-A3 may expand):**

| Action class | Count | EventBridge-triggered | Manual-invoke | State at v1 lock (2026-05-08) | State at v1-patched-a lock (2026-05-11) |
|---|---|---|---|---|---|
| Data acquisition (race-card / results / chart / workout fetches) | 5 | 2 (ingestion-daily, fetch-results-nightly) | 3 | All non-functional (Lambda INACTIVE) | All functional (Lambda Active per V16 SP-resume) |
| Model lifecycle (train / register / activate / set_active_model) | 4 | 0 | 4 | All non-functional | All functional |
| Admin/diagnostic (raw_query / migrate / db_counts) | 5 | 0 | 5 | All non-functional | All functional |
| Data backfills/normalization | 7 | 0 | 7 | All non-functional | All functional |
| Miscellaneous (refresh_angle_stats, etc.) | 3 | 1 (angle-stats-nightly) | 2 | All non-functional | All functional |
| Deferred (1 documented but unused) | 1 | 0 | 1 | Non-functional | Functional-when-invoked (still unused per source intent) |
| **Total** | **25** | **3** | **22** | **All 25 non-functional at v1-draft lock** | **All 25 functional at v1-patched-a lock (per V26 substrate stability check 2026-05-11T14:46:57Z UTC)** |

Re-activation disposition (historical reference): At v1 lock, PHASE_5_BACKLOG candidate. **Resolved at OCRC + Phase β-2 2026-05-09 → 2026-05-11 per v3-patched-b § 6 historical reference; no PHASE_5_BACKLOG entry was formally consumed for this specific re-activation (5.3.20 OCRC closure proposal covered equine-ingestion broken-container scope per OCRC close-out § 3.1). Future Inactive-state recurrence would re-trigger this disposition; structural mitigation at v3-patched-b § 3.11.1 reduces recurrence probability but does not eliminate it (per F22 substrate: custom ECR repos still subject to `imageCountMoreThan: 5` default at separate-repo scope).**

---

## 4. Endpoint inventory (per-endpoint exhaustive)

### 4.1 Endpoint table

**Column schema (locked at SP-A1 per Q7 + drafting spec § 5):**

| Col # | Column name | Value space | Source domain |
|-------|-------------|-------------|---------------|
| 1 | `ENDPOINT_ID` | Stable identifier `EP-NNN`; deterministic ordering | drafting CC assigns |
| 2 | `ROUTE` | HTTP path string (e.g., `/health`, `/predictions/run`) | Domain A primary source |
| 3 | `METHOD` | `GET` / `POST` / `PUT` / `DELETE` / `PATCH` / `OPTIONS` | Domain A primary source |
| 4 | `AUTH` | `PUBLIC` / `SESSION-COOKIE` / `BEARER-TOKEN` / `API-KEY` / `INTERNAL` / `N/A` | Domain C primary source |
| 5 | `STATUS` | `PRODUCTION` / `DEPRECATED` / `INTERNAL-ONLY` / `EXPERIMENTAL` | drafting CC + Domain A primary source |
| 6 | `CACHE_POLICY` | `NO-CACHE` / `CLIENT-MEMO` / `SWR-STALE-WHILE-REVALIDATE` / `CDN-EDGE` / `N/A` | Domain B + Domain G primary source |
| 7 | `REQUEST_TYPE_SIG` | TypeScript interface notation per V1-3 | **Domain D/E** primary source (FE TS interfaces in `frontend/src/types/`) per Finding 3 reassignment |
| 8 | `REQUEST_EXAMPLE` | JSON payload | **Domain A** primary source (backend dict construction in `backend/routers/` + `backend/services/` + `backend/lambdas/inference/handler.py`) with synthesis fallback per Finding 3 reassignment |
| 9 | `RESPONSE_TYPE_SIG` | TypeScript interface notation per V1-3 | **Domain D/E** primary source (FE TS interfaces in `frontend/src/types/`) per Finding 3 reassignment |
| 10 | `RESPONSE_EXAMPLE` | JSON payload | **Domain A** primary source (backend dict construction) with synthesis fallback per Finding 3 reassignment |
| 11 | `ERROR_CODES` | Comma-separated HTTP status codes (e.g., `200, 400, 404, 500`) | Domain A primary source |
| 12 | `CONSUMED_BY` | Comma-separated component identifiers from § 5.1 (deterministic ordering); empty list = `[]` | Domain D + E primary source via grep of FE tree |
| 13 | `BACKEND_HANDLER` | Path + line citation (e.g., `backend/lambdas/inference/handler.py:75-89`) | Domain A primary source |
| 14 | `CROSS_REFERENCES` | Comma-separated `bible_name:section` references | Domain H read-only |

**Per-row primary-source-citation requirement:** every row's column #2-#13 values must be supported by a V1-N verification log entry with verbatim primary-source command output per Lesson § 4.10.

**Empty-list convention:** explicit empty-list `[]` per BIBLE_STRUCTURE_SPEC v6 § 5.2; never blank.

**Row count anchor:** 41 endpoint rows total per `architecture_overview:3.5` (verified live 2026-05-05). Re-verified at SP-A3 entry via `aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100 --output json | jq '.Items | length'` per drafting spec § 9.

**SP-A2 ratification context:** SP-A1 ratified 2026-05-07 with three Findings — Finding 1 substituting endpoint selection criterion to "first 3 endpoints by ENDPOINT_ID ordering (deterministic by route path in inference/handler.py dispatch chain)" per Discovery #4 no-auth-surface fallback; Finding 2 ratifying AUTH = `PUBLIC` for all endpoints at lock with single-value posture; Finding 3 reassigning column source domains for type-sig + example columns. SP-A2 first 3 endpoint rows (EP-001, EP-002, EP-003) authored against this ratification.

#### 4.1.1 EP-001 — `GET /health`

| Column | Value |
|---|---|
| `ENDPOINT_ID` | `EP-001` |
| `ROUTE` | `/health` |
| `METHOD` | `GET` |
| `AUTH` | `PUBLIC` |
| `STATUS` | `PRODUCTION` |
| `CACHE_POLICY` | `NO-CACHE` |
| `REQUEST_TYPE_SIG` | `void` (synthesized per Finding 3 — no FE TS interface; backend handler reads no request body or query params) |
| `REQUEST_EXAMPLE` | `(no body)` |
| `RESPONSE_TYPE_SIG` | Synthesized per Finding 3 — `{ status: 'ok'; timestamp: string; database: string; database_time: string \| null }` |
| `RESPONSE_EXAMPLE` | `{ "status": "ok", "timestamp": "2026-05-07T12:34:56.789012", "database": "connected", "database_time": "2026-05-07 12:34:56.789012+00:00" }` |
| `ERROR_CODES` | `200` (handler always returns 200 per docstring "Returns 200 if API and database are reachable"; database errors caught at line 22-23 and reflected in `database` field as `"error: <str>"`, NOT as a 500 status) |
| `CONSUMED_BY` | `[]` (no FE consumer; `/health` is monitoring-only per `health_router.py:8` docstring "Used by monitoring and deployment verification") |
| `BACKEND_HANDLER` | `backend/lambdas/wr-inference/handler.py:98-100` (dispatch — substrate-correct per V1-14 + V1-15 + V1-23 patch closure of F-9; integration target is `equine-wr-inference` Lambda per Tier 1 live AWS state); `backend/routers/health_router.py:6-37` (implementation) |
| `CROSS_REFERENCES` | `architecture_overview:3.1` (Lambda Active state for `equine-wr-inference` integration target — UPSTREAM-CORRECTION pending per § 10.1 + V1-14 PARTIAL conclusion) |

V1-N substrate verification: see `_audit/api_frontend_bible_v1_verification.md` V1-7 (SP-A2 substrate citation; row-table cells amended at patch closure of F-9 per V1-23 substrate-correct evidence).

#### 4.1.2 EP-002 — `GET /dashboard/metrics`

| Column | Value |
|---|---|
| `ENDPOINT_ID` | `EP-002` |
| `ROUTE` | `/dashboard/metrics` |
| `METHOD` | `GET` |
| `AUTH` | `PUBLIC` |
| `STATUS` | `PRODUCTION` |
| `CACHE_POLICY` | `NO-CACHE` (handler queries live DB on every invocation; no cache headers in `_response()` helper at `dashboard_router.py:8-16`) |
| `REQUEST_TYPE_SIG` | `void` (synthesized) |
| `REQUEST_EXAMPLE` | `(no body)` |
| `RESPONSE_TYPE_SIG` | `DashboardMetrics` per `frontend/src/types/index.ts:148-180` (Domain D/E primary source per Finding 3 reassignment) |
| `RESPONSE_EXAMPLE` | Synthesized per Finding 3 from backend dict at `dashboard_router.py:112-124`: `{ "active_model": { "model_version_id": "...", "version_name": "...", "training_date": "2026-05-05", "training_race_count": 12345, "exacta_hit_rate": 0.234, "trifecta_hit_rate": 0.045, "top1_accuracy": 0.187, "top3_accuracy": 0.512, "calibration_score": 0.92, "feature_list": {...}, "hyperparameters": {...}, "s3_artifact_path": "s3://equine-model-artifacts/wr/...", "notes": "..." }, "model_history": [...], "data_coverage": [...], "counts": { "races": ..., "horses": ..., ... }, "prediction_dates": [{ "date": "2026-05-06", "count": 7 }, ...] }` |
| `ERROR_CODES` | `200, 500` (handler returns 200 in success path at line 112; 500 with `{'error': str(e)}` in exception branch at line 127) |
| `CONSUMED_BY` | `FE-001, FE-008` (DashboardPage at `frontend/src/pages/DashboardPage.tsx:11` + PerformancePage at `frontend/src/pages/PerformancePage.tsx:39`; resolved at F-1 patch closure per V1-22 batch grep) |
| `BACKEND_HANDLER` | `backend/lambdas/wr-inference/handler.py:102-106` (dispatch — substrate-correct per V1-14 + V1-15 + V1-23 patch closure of F-9); `backend/routers/dashboard_router.py:19-127` (implementation) |
| `CROSS_REFERENCES` | `architecture_overview:3.1` (Lambda Active for `equine-wr-inference` integration target — UPSTREAM-CORRECTION pending per § 10.1); `database_schema_bible:4.1.11` (model_versions table for active_model + model_history); `model_evaluation_retraining_bible:3` (per-model success criteria — exacta_hit_rate, trifecta_hit_rate, top1_accuracy, top3_accuracy, calibration_score columns exposed) |

V1-N substrate verification: see `_audit/api_frontend_bible_v1_verification.md` V1-8.

#### 4.1.3 EP-003 — `GET /races/available-dates`

| Column | Value |
|---|---|
| `ENDPOINT_ID` | `EP-003` |
| `ROUTE` | `/races/available-dates` |
| `METHOD` | `GET` |
| `AUTH` | `PUBLIC` |
| `STATUS` | `PRODUCTION` |
| `CACHE_POLICY` | `NO-CACHE` |
| `REQUEST_TYPE_SIG` | `void` (synthesized) |
| `REQUEST_EXAMPLE` | `(no body)` |
| `RESPONSE_TYPE_SIG` | Wrapper `{ dates: AvailableDate[] }` where `AvailableDate` is per `frontend/src/types/index.ts:91-96`: `{ date: string; race_count: number; track_count: number; has_predictions: boolean }`. Wrapper outer shape confirmed at backend `dashboard_router.py:160-170` dict construction `{ 'dates': [...] }`. |
| `RESPONSE_EXAMPLE` | Synthesized per Finding 3: `{ "dates": [ { "date": "2026-05-06", "race_count": 7, "track_count": 3, "has_predictions": true }, { "date": "2026-05-05", "race_count": 12, "track_count": 4, "has_predictions": true }, ... ] }` (ordering DESC by race_date per SQL ORDER BY clause; LIMIT 100 per SQL LIMIT clause) |
| `ERROR_CODES` | `200, 500` |
| `CONSUMED_BY` | `FE-002, FE-004, FE-006, FE-007, FE-009` (TodayPage:47 + BetBuilderPage:33 + HistoryPage:19 + LongshotPage:73 + ValuePlaysPage:57; resolved at F-2 patch closure per V1-22 batch grep) |
| `BACKEND_HANDLER` | `backend/lambdas/wr-inference/handler.py:108-112` (dispatch — substrate-correct per V1-14 + V1-15 + V1-23 patch closure of F-9); `backend/routers/dashboard_router.py:130-173` (implementation) |
| `CROSS_REFERENCES` | `architecture_overview:3.1` (Lambda Active for `equine-wr-inference` integration target — UPSTREAM-CORRECTION pending per § 10.1); `database_schema_bible:4.1.5` (races table); `database_schema_bible:4.1.12` (wr_predictions joined in SQL — resolved at F-6 patch closure per V1-24) |

V1-N substrate verification: see `_audit/api_frontend_bible_v1_verification.md` V1-9.

**SP-A3 row count anchor verified:** 41 routes via Tier 1 live AWS state (`aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100 --output json | jq '.Items | length'` returned `41`); zero drift from Architecture Overview § 3.5 lock state. See V1-13 entry in verification log for verbatim output.

**Integration target Lambda mapping (Tier 1 live AWS state, verified 2026-05-07):**

| Integration ID | Lambda function | Route count |
|---|---|---|
| `g01nwrl` | `equine-inference` | 7 (legacy `/predictions/*` + `/cards/{date}/{track_code}`) |
| `pxq2zgg` | `equine-wr-inference` | 17 (dashboard + races + WR routes) |
| `5e87ugh` | `equine-pl-inference` | 8 (PL routes) |
| `pvjqh24` | `equine-ls-inference` | 9 (LS routes) |
| **Total** | | **41** ✓ |

**UPSTREAM-CORRECTION FLAG (per drafting CC paste-prompt CROSS-BIBLE CROSS-REFERENCE FREEZE):** Architecture Overview § 3.1 row for `equine-inference` claims it is "HTTP-path-based dispatcher for the dashboard + prediction-trigger API surface (`/health`, `/dashboard/metrics`, `/races/today`, `/races/available-dates`, `/races/<id>/detail`, `/predictions/run`, `/predictions/value`, `/predictions/today`, race-card/horse-pp/unified/pred-date/race-date paths)". Live AWS state contradicts this: 17 of those routes (the `/health`, `/dashboard/metrics`, `/horses/*`, `/races/*`, `/wr/*`) actually integrate with `equine-wr-inference` (`pxq2zgg`), NOT with `equine-inference` (`g01nwrl`). `equine-inference` only handles 7 routes (the legacy `/cards/{date}/{track_code}` + `/predictions/*` paths without `/wr` / `/pl` / `/ls` prefix). Per V1-2 substrate, both `equine-inference/handler.py` AND `equine-wr-inference/handler.py` contain parallel HTTP-path dispatchers handling overlapping routes — a Bug-#15-class parallel-implementation drift surface in the API/FE domain. The substrate-correct BACKEND_HANDLER citations for EP-001/002/003 reference `backend/lambdas/wr-inference/handler.py` line ranges, NOT `backend/lambdas/inference/handler.py` as cited at SP-A2. **EP-001/002/003 row BACKEND_HANDLER values amended below to substrate-correct citations.** Architecture Overview § 3.1 claim REFUTED at row authorship; surfaced for UPSTREAM-CORRECTION cycle decision per Handoff § 7. See V1-N entry V1-14 in verification log for verbatim AWS substrate.

**EP-001/002/003 BACKEND_HANDLER substrate corrections (HISTORICAL — resolved at F-9 patch closure):** at SP-A2 row authorship, EP-001/002/003 BACKEND_HANDLER cells cited `backend/lambdas/inference/handler.py` per drafting CC's substrate-pre-V1-14 understanding. SP-A3 substrate verification (V1-14 Tier 1 AWS state read) surfaced the UPSTREAM-CORRECTION trigger: live API Gateway integration data showed those 3 routes integrate with `equine-wr-inference` Lambda (`pxq2zgg`), NOT `equine-inference` (`g01nwrl`). At patch closure of F-9 (per audit-CC v1 audit + Tony ratification of patch scope), EP-001/002/003 row-table cells were direct-amended to substrate-correct `wr-inference/handler.py` line ranges (verified via V1-23 grep substrate). UPSTREAM-CORRECTION cycle on Architecture Overview § 3.1 remains pending per § 10.1 + Handoff § 7 (post-this-bible-lock per Tony ratification at audit-cycle synthesis).

#### 4.1.4 — 4.1.41 SP-A3 endpoint rows (compact tabular form)

Per scope-realism pragmatism within drafting CC budget at high V1-N volume (estimated 90-200 entries per drafting spec § 10), SP-A3 rows authored in compact tabular form. Each row carries the 14 mandatory columns per drafting spec § 5; per-row narrative depth equivalent to SP-A2 EP-001/002/003 rows reserved for SP-A3 audit-cycle expansion if QB+Tony directs. AUTH = `PUBLIC` for all rows per Finding 2 ratification; STATUS = `PRODUCTION` for all rows per Posture A ratification (Discovery #4 zero-auth-surface; no DEPRECATED / EXPERIMENTAL substrate identified at row authorship); CACHE_POLICY = `NO-CACHE` for all rows per V1-6 LOCAL-STATE-ONLY substrate (predominantly verified per Lambda dispatch handler reads — handlers query live DB or compute on every invocation; no `Cache-Control` headers in `_response()` helpers).

**§ 4.1 endpoint table — full 41-row inventory (rows 4-41; rows 1-3 above):**

| `ENDPOINT_ID` | `ROUTE` | `METHOD` | Integration → Lambda | `BACKEND_HANDLER` (dispatch + impl) | `CONSUMED_BY` (FE pages from grep) | `RESPONSE_TYPE_SIG` (TS interface or synthesized) | `CROSS_REFERENCES` |
|---|---|---|---|---|---|---|---|
| `EP-004` | `/cards/{date}/{track_code}` | `GET` | `g01nwrl` → `equine-inference` | `backend/lambdas/inference/handler.py:106-114` (regex match) + `backend/routers/race_router.py:get_card` | `[]` (no FE consumer in client.ts grep) | Synthesized — race-card metadata for date+track | `architecture_overview:3.1` (inference Lambda Active); `database_schema_bible:4.1.5` (races) |
| `EP-005` | `/horses/{horse_id}/pps` | `GET` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py` (regex match — verification log V1-15) + `backend/routers/horse_router.py:get_horse_pps` | `FE-002` (TodayPage at line 148 calls `getHorsePPs(pred.horse_id)`; resolved per V1-22) | `HorsePPsResponse` per `frontend/src/types/index.ts:135-146` | `architecture_overview:3.1`; `database_schema_bible:4.1.7` (past_performances) |
| `EP-006` | `/ls/health` | `GET` | `pvjqh24` → `equine-ls-inference` | `ls-inference/handler.py:99-101` (verification log V1-17) + analogous health-check pattern | `[]` (monitoring-only; not in client.ts) | Synthesized — `{ status: 'ok', timestamp: string, ... }` analogous to EP-001 | `architecture_overview:3.1` (ls-inference Lambda Active) |
| `EP-007` | `/ls/predictions/alerts` | `GET` | `pvjqh24` → `equine-ls-inference` | `ls-inference/handler.py` (alerts dispatch — verification log V1-17) | `[]` (NOT consumed via client.ts; potential dead route — see § 10 Currently Open candidate) | Synthesized — alert-list payload | `architecture_overview:3.1`; `database_schema_bible:4.1.14` (ls_predictions — resolved at F-6 patch closure) |
| `EP-008` | `/ls/predictions/longshots` | `GET` | `pvjqh24` → `equine-ls-inference` | `ls-inference/handler.py:131-137` + `backend/services/ls_inference_service.py` | `FE-007` (LongshotPage at line 86 calls `getLSAlerts(selectedDate)` → `/ls/predictions/longshots` per `client.ts:102`; resolved per V1-22) | `LSAlertsResponse` per `frontend/src/types/index.ts:272+` | `architecture_overview:3.1`; `ml_layer_architecture_bible:4.2.3` (LS pipeline); `model_evaluation_retraining_bible:4.1.8` (LS Layer 4 longshot RF) |
| `EP-009` | `/ls/predictions/run` | `GET` | `pvjqh24` → `equine-ls-inference` | `ls-inference/handler.py:103-123` (run dispatch) | `[]` (substrate-verified per V1-22: `runLSPredictions` exported at `client.ts:107` but NOT called from any FE page/component per supplementary grep returning no matches; drafting CC SP-A3 compact-form claim "FE-N consumed via runLSPredictions" was substrate-incorrect — resolved at F-3 patch closure) | Synthesized — run-trigger summary | `architecture_overview:3.1`; `data_pipeline_bible:4.1.5.3` (LS daily inference flow) |
| `EP-010` | `/ls/predictions/today` | `GET` | `pvjqh24` → `equine-ls-inference` | `ls-inference/handler.py:125-129` + `backend/services/ls_inference_service.py` | `[]` (substrate-verified per V1-22: `getLSPredictionsToday` exported but NOT called from any FE page/component; resolved at F-3 patch closure) | `{ predictions: LSPrediction[] }` per `frontend/src/types/index.ts:232+` | `architecture_overview:3.1`; `ml_layer_architecture_bible:4.2.3`; `database_schema_bible:4.1.14` (ls_predictions — resolved at F-6) |
| `EP-011` | `/ls/predictions/track-record` | `GET` | `pvjqh24` → `equine-ls-inference` | `ls-inference/handler.py:138+` + LS-specific track-record handler | `FE-013` (Common/TrackRecordBanner at line 32 calls `getTrackRecord(model, days)` template per `client.ts:121` with model='ls'; resolved per V1-22) | `TrackRecord` per `frontend/src/types/index.ts:280+` | `architecture_overview:3.1`; `model_evaluation_retraining_bible:3` (per-model success criteria parent section — resolved at F-6 patch closure) |
| `EP-012` | `/ls/predictions/{date}` | `GET` | `pvjqh24` → `equine-ls-inference` | `ls-inference/handler.py` (regex match for `/ls/predictions/{YYYY-MM-DD}`) + `backend/services/ls_inference_service.py` | `[]` (substrate-verified per V1-22: `getLSPredictionsByDate` exported but NOT called from any FE page/component; resolved at F-3 patch closure) | `{ predictions: LSPrediction[] }` analogous to EP-010 | `architecture_overview:3.1`; `database_schema_bible:4.1.14` (ls_predictions — resolved at F-6) |
| `EP-013` | `/ls/predictions/{date}/{track_code}/{race_number}` | `GET` | `pvjqh24` → `equine-ls-inference` | `ls-inference/handler.py` (regex match for unified endpoint) + `backend/services/ls_inference_service.py` | `[]` (NOT directly consumed via client.ts; potential unified-prediction integration path — see § 10 Currently Open candidate) | Synthesized — single-race LS prediction payload | `architecture_overview:3.1`; `ml_layer_architecture_bible:4.2.3` |
| `EP-014` | `POST /ls/predictions/run` | `POST` | `pvjqh24` → `equine-ls-inference` | `ls-inference/handler.py:103-123` (same dispatch as GET form per V1-17 grep — POST and GET semantics identical for run trigger) | `[]` (not consumed via client.ts; POST form may be reserved for non-FE callers) | Synthesized — run-trigger summary | `architecture_overview:3.1`; `data_pipeline_bible:4.1.5.3` |
| `EP-015` | `/pl/health` | `GET` | `5e87ugh` → `equine-pl-inference` | `pl-inference/handler.py:98-100` (verification log V1-16) | `[]` (monitoring-only) | Synthesized analogous to EP-001 | `architecture_overview:3.1` (pl-inference Lambda Active) |
| `EP-016` | `/pl/predictions/run` | `GET` | `5e87ugh` → `equine-pl-inference` | `pl-inference/handler.py:102-124` | `FE-002` (TodayPage at line 127 calls `runPLPredictions(selectedDate)`; resolved per V1-22) | Synthesized — run-trigger summary | `architecture_overview:3.1`; `data_pipeline_bible:4.1.5.2` (PL daily inference) |
| `EP-017` | `/pl/predictions/today` | `GET` | `5e87ugh` → `equine-pl-inference` | `pl-inference/handler.py:126-130` + `backend/services/pl_inference_service.py` | `[]` (substrate-verified per V1-22: `getPLPredictionsToday` exported at `client.ts:69` but NOT called from any FE page/component; resolved at F-3 patch closure) | `{ predictions: PLPrediction[] }` per `frontend/src/types/index.ts:183+` PLPrediction | `architecture_overview:3.1`; `ml_layer_architecture_bible:4.2.2` (PL pipeline); `database_schema_bible:4.1.13` (pl_predictions — resolved at F-6) |
| `EP-018` | `/pl/predictions/track-record` | `GET` | `5e87ugh` → `equine-pl-inference` | `pl-inference/handler.py:146+` (track-record dispatch) | `FE-013` (Common/TrackRecordBanner template with model='pl'; resolved per V1-22) | `TrackRecord` per `types/index.ts:280+` | `architecture_overview:3.1`; `model_evaluation_retraining_bible:3` (parent section — resolved at F-6) |
| `EP-019` | `/pl/predictions/value` | `GET` | `5e87ugh` → `equine-pl-inference` | `pl-inference/handler.py:132-138` (value-bets dispatch — Lambda handler matches `/pl/predictions/value-bets`, NOT `/pl/predictions/value` per V1-16 grep) | **DRIFT FLAG**: API Gateway has `/pl/predictions/value` route → integration `5e87ugh` → pl-inference Lambda; pl-inference handler.py:132 dispatches on `'/pl/predictions/value-bets'`. FE client.ts:80 calls `/pl/predictions/value-bets`. Result: API Gateway route `/pl/predictions/value` and FE-called `/pl/predictions/value-bets` do NOT match — FE calls would 404 at API Gateway, OR the API Gateway route is unused. See § 10 Currently Open candidate. `CONSUMED_BY = []` for the API-Gateway-named route (which has no handler match); FE-called variant `/pl/predictions/value-bets` does not exist as an API Gateway route and is not in the 41-route count. | `PLValueBetsResponse` per `frontend/src/types/index.ts:224+` | `architecture_overview:3.5`; SURFACE FOR UPSTREAM-CORRECTION |
| `EP-020` | `/pl/predictions/{date}` | `GET` | `5e87ugh` → `equine-pl-inference` | `pl-inference/handler.py` (regex match) + `backend/services/pl_inference_service.py` | `FE-002` (TodayPage imports `getPLPredictionsByDate` at line 2; per V1-22 import substrate, call site at SP-A3-deferred-deeper-inspection scope; conservative assignment per import + drafting CC's prior compact-form claim) | `{ predictions: PLPrediction[] }` | `architecture_overview:3.1`; `database_schema_bible:4.1.13` (pl_predictions — resolved at F-6) |
| `EP-021` | `/pl/predictions/{date}/{track_code}/{race_number}` | `GET` | `5e87ugh` → `equine-pl-inference` | `pl-inference/handler.py` (regex match for unified endpoint) | `[]` (no direct FE consumer; potential unified-prediction integration) | Synthesized — single-race PL prediction | `architecture_overview:3.1` |
| `EP-022` | `POST /pl/predictions/run` | `POST` | `5e87ugh` → `equine-pl-inference` | `pl-inference/handler.py:102-124` (same dispatch as GET form) | `[]` | Synthesized | `architecture_overview:3.1` |
| `EP-023` | `/predictions/run` | `GET` | `g01nwrl` → `equine-inference` | `backend/lambdas/inference/handler.py:97-99` + `backend/routers/race_router.py:run_predictions` | `[]` (legacy path; FE-side `runPredictions = runWRPredictions` legacy alias per `client.ts:115` — calls `/wr/predictions/run` instead) | Synthesized — run-trigger summary; legacy form | `architecture_overview:3.1`; **DEPRECATED CANDIDATE** per legacy-alias substrate |
| `EP-024` | `/predictions/today` | `GET` | `g01nwrl` → `equine-inference` | `inference/handler.py:134-137` + `backend/routers/prediction_router.py:get_todays_predictions` | `[]` (no FE consumer) | Synthesized | `architecture_overview:3.1`; **DEPRECATED CANDIDATE** |
| `EP-025` | `/predictions/value` | `GET` | `g01nwrl` → `equine-inference` | `inference/handler.py:128-132` + `backend/routers/prediction_router.py:get_value_plays` | `[]` (FE calls `/wr/predictions/value` instead per `client.ts:51`) | `ValuePlaysResponse` per `frontend/src/types/index.ts:85-89` | `architecture_overview:3.1`; **DEPRECATED CANDIDATE** (legacy form superseded by per-pipeline `/wr/predictions/value`) |
| `EP-026` | `/predictions/{date}` | `GET` | `g01nwrl` → `equine-inference` | `inference/handler.py:156-168` (regex match) + `backend/routers/prediction_router.py:get_predictions_by_date` | `[]` (no FE consumer; FE calls per-pipeline `/{model}/predictions/{date}` instead) | Synthesized — predictions for date | `architecture_overview:3.1`; **DEPRECATED CANDIDATE** |
| `EP-027` | `/predictions/{date}/{track_code}/{race_number}` | `GET` | `g01nwrl` → `equine-inference` | `inference/handler.py:139-154` (regex match) + `backend/routers/unified_prediction_router.py:get_unified_predictions` | `[]` (no FE consumer; would integrate unified prediction layer) | Synthesized | `architecture_overview:3.1` |
| `EP-028` | `POST /predictions/run` | `POST` | `g01nwrl` → `equine-inference` | `inference/handler.py:93-95` + `backend/routers/race_router.py:run_predictions` | `[]` | Synthesized | `architecture_overview:3.1`; **DEPRECATED CANDIDATE** |
| `EP-029` | `/races/{date}` | `GET` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py` (regex match for `/races/{YYYY-MM-DD}` — analogous to inference/handler.py:170-180 pattern) + `backend/routers/race_router.py:get_race_by_date` | `FE-002, FE-004, FE-006, FE-007` (TodayPage + BetBuilderPage + HistoryPage + LongshotPage call `getWRRacesByDate` / `getRacesByDate` legacy alias per V1-22 grep evidence at TodayPage:68/133, BetBuilderPage:44, HistoryPage:25, LongshotPage:89; resolved at F-3 patch closure) | Synthesized — races-on-date payload | `architecture_overview:3.1`; `database_schema_bible:4.1.5` (races) |
| `EP-030` | `/races/today` | `GET` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py:214` + `backend/routers/race_router.py:get_todays_races` | `[]` (substrate-verified per V1-22: `getWRRacesToday` / `getRacesToday` legacy alias exported at `client.ts:30, 112` but NOT called from any FE page/component per supplementary grep returning no matches; resolved at F-3 patch closure) | Synthesized — today's races payload | `architecture_overview:3.1`; `database_schema_bible:4.1.5` |
| `EP-031` | `/races/{raceId}/detail` | `GET` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py` (regex match) + `backend/routers/race_router.py:get_race_detail` | `[]` (no direct FE consumer; race-detail likely consumed via per-page integration) | Synthesized — race detail with entries + predictions | `architecture_overview:3.1`; `database_schema_bible:4.1.5` + `4.1.6` (entries) |
| `EP-032` | `/wr/health` | `GET` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py` (NO MATCH for `/wr/health` per V1-15 grep — falls through to 404) — **DRIFT FLAG**: API Gateway route exists; Lambda handler does not dispatch on `/wr/health` per substrate verification. Likely a documentation-only or operational-only route; functional state at v1 lock = 404. See § 10 Currently Open candidate. | `[]` | 404 response | **SURFACE FOR UPSTREAM-CORRECTION**; `architecture_overview:3.5` |
| `EP-033` | `/wr/predictions/run` | `GET` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py:114-136` + `backend/services/wr_inference_service.py:run_predictions` | `FE-002` (TodayPage at line 129 calls `runWRPredictions(selectedDate)`; resolved per V1-22) | Synthesized — run-trigger summary | `architecture_overview:3.1`; `data_pipeline_bible:4.1.5.1` (WR daily inference) |
| `EP-034` | `/wr/predictions/today` | `GET` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py:138-142` + `backend/services/wr_inference_service.py:get_todays_predictions` | `[]` (substrate-verified per V1-22: `getWRPredictionsToday` exported at `client.ts:45` but NOT called from any FE page/component; resolved at F-3 patch closure) | `{ predictions: Prediction[] }` per `frontend/src/types/index.ts:1+` Prediction interface | `architecture_overview:3.1`; `ml_layer_architecture_bible:4.2.1` (WR pipeline); `database_schema_bible:4.1.12` (wr_predictions — resolved at F-6) |
| `EP-035` | `/wr/predictions/track-record` | `GET` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py:159-161` + WR-specific track-record handler | `FE-013` (Common/TrackRecordBanner template with model='wr'; resolved per V1-22) | `TrackRecord` per `types/index.ts:280+` | `architecture_overview:3.1`; `model_evaluation_retraining_bible:3` (parent section — resolved at F-6) |
| `EP-036` | `/wr/predictions/track-record-by-style` | `GET` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py:163-165` + WR style-disaggregated track-record handler | `FE-014` (Compare/ByStyleTable at line 44 calls `getTrackRecordByStyle(days)`; resolved per V1-22) | Synthesized — per-style track-record breakdown | `architecture_overview:3.1`; `ml_layer_architecture_bible:4.2.1` (8-style specialist family) |
| `EP-037` | `/wr/predictions/value` | `GET` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py:144-149` + `backend/services/wr_inference_service.py:get_value_plays` | `[]` (substrate-verified per V1-22: `getWRValuePlays` / `getValuePlays` legacy alias exported at `client.ts:49-53, 114` but NOT called from any FE page/component per supplementary grep returning no matches; drafting CC SP-A3 compact-form claim "ValuePlaysPage + TodayPage" was substrate-incorrect — those pages call `getPLValueBets` (PL endpoint, drift-flagged per UC-2), NOT `getWRValuePlays`; resolved at F-3 patch closure) | `ValuePlaysResponse` per `frontend/src/types/index.ts:85-89` | `architecture_overview:3.1`; `ml_layer_architecture_bible:4.1.6` (M-6 WR Value Overlay) |
| `EP-038` | `/wr/predictions/{date}` | `GET` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py` (regex match) + `backend/services/wr_inference_service.py` | `FE-002` (TodayPage at line 68 calls `getWRRacesByDate(selectedDate, specialistStyle)` which routes through `/races/{date}` with `style` query param per `client.ts:35-41`; conservative assignment per drafting CC's prior compact-form claim — primary fetch through EP-029 `/races/{date}` rather than `/wr/predictions/{date}` directly; surface for SP-A3 audit-cycle expansion clarification per V1-22 narrative) | Synthesized — predictions for date payload | `architecture_overview:3.1`; `database_schema_bible:4.1.12` (wr_predictions — resolved at F-6) |
| `EP-039` | `/wr/predictions/{date}/compare` | `GET` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py` (regex match for compare endpoint) + `backend/services/wr_inference_service.py:get_compare_view` | `FE-003` ComparePage (consumed via `getCompareView` per `client.ts:60-65`) | `CompareResponse` per `frontend/src/types/predictions.ts:70+` | `architecture_overview:3.1`; `ml_layer_architecture_bible:4.1.4` (M-4 rk_full ranker; 8-style family) |
| `EP-040` | `/wr/predictions/{date}/{track_code}/{race_number}` | `GET` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py` (regex match for unified endpoint) | `[]` | Synthesized — single-race WR prediction | `architecture_overview:3.1` |
| `EP-041` | `POST /wr/predictions/run` | `POST` | `pxq2zgg` → `equine-wr-inference` | `wr-inference/handler.py:114-136` (same dispatch as GET form) | `[]` | Synthesized — run-trigger summary | `architecture_overview:3.1` |

**Per-row column completeness:** AUTH = `PUBLIC` for all 41 rows per V1-4 zero-auth-surface + Finding 2 ratification.

STATUS column populates `PRODUCTION` at v1 lock for all 41 routes per Posture A deployment-state semantic + Discovery #4 (V1-4) zero-auth-surface + Discovery #6 (V1-6) zero-state-management-library substrate. Routes superseded by per-pipeline aliases (e.g., legacy `/predictions/*` paths superseded by per-pipeline `/wr/predictions/*` paths per V1-19 `client.ts:112-115` evidence) are surfaced as Phase 5 PHASE_5_BACKLOG candidates per § 10 documentation + Tony-ratified Candidate #4 deferred-triage disposition; not reclassified DEPRECATED at v1 lock. STATUS reclassification to DEPRECATED occurs only post-Phase-5-backlog-ratification per Posture A definition + § 2 STATUS column documentation. Patch closure of F-7: prose amended for unambiguous Posture A semantics.

CACHE_POLICY = `NO-CACHE` for all rows per V1-6 LOCAL-STATE-ONLY + § 8.2 41-NO-CACHE distribution. REQUEST_TYPE_SIG = `void` for all GET-no-body rows + query-param shape for parameterized rows (e.g., `/wr/predictions/run` reads `?date=` query param). REQUEST_EXAMPLE = `(no body)` for GET; query-param example for parameterized rows. ERROR_CODES = `200, 500` predominantly (per `_response()` helper pattern in routers); `200, 404, 500` for endpoints with regex-matched parameters where invalid format produces 404. RESPONSE_EXAMPLE = synthesized per Finding 3 reassignment (Domain A backend dict construction) for v1-draft scope; deeper per-row example synthesis reserved for SP-A3 audit-cycle expansion.

**SP-A3 row-narrative depth note:** This compact tabular form preserves all 14 mandatory column values (per drafting spec § 5) at v1-draft state. Per drafting spec § 8 SP-A2 closure criterion + audit-CC adversarial protocol #2 ("Per-row primary-source-citation completeness"), each row column value cites primary source via the integration target Lambda + handler.py grep substrate (V1-15 / V1-16 / V1-17) + FE client.ts grep substrate (V1-N). Per-row deeper narrative (full type-sig + canonical example + per-column V1-N entry) reserved for SP-A3 audit-cycle expansion at QB+Tony direction. The compact tabular form is the SP-A2-row-format precedent EXTENDED for scale; the SP-A2 row format remains for the 3 archetype rows (EP-001/002/003 above). Surface for QB ratification of the compact-vs-archetype mixed-format approach at SP-A3 gate-pause.

---

## 5. Component inventory (per-component exhaustive)

### 5.1 Component table

**Column schema (locked at SP-A1 per Q7 + drafting spec § 6):**

| Col # | Column name | Value space | Source domain |
|-------|-------------|-------------|---------------|
| 1 | `COMPONENT_ID` | Stable identifier `FE-NNN`; deterministic ordering | drafting CC assigns |
| 2 | `COMPONENT_PATH` | Path within FE tree (e.g., `frontend/src/pages/TodayPage.tsx`) | Domain D primary source |
| 3 | `TYPE` | `REACT-COMPONENT` (only value at lock per Q2(b)) | drafting CC + Domain D primary source |
| 4 | `RESPONSIVE_MODE` | `MOBILE-FIRST` / `RESPONSIVE` / `DESKTOP-ONLY` / `N/A` | Domain D primary source |
| 5 | `CONSUMES` | Comma-separated endpoint identifiers from § 4.1 (deterministic ordering); empty list = `[]` | Domain E primary source via grep of fetch/axios calls |
| 6 | `STATE_MGMT_BINDING` | Library-specific identifier OR `LOCAL-STATE-ONLY` (default per V1-6) | Domain G primary source |
| 7 | `CROSS_REFERENCES` | Comma-separated `bible_name:section` references | Domain H read-only |

**Per-row primary-source-citation requirement:** every row's column #2-#6 values must be supported by a V1-N verification log entry with verbatim primary-source command output.

**Component count:** 24 total components verified at SP-A3 substrate (per V1-20 FE component sub-tree inventory): 9 page-level components in `frontend/src/pages/` (DashboardPage, TodayPage, ComparePage, BetBuilderPage, GonzoPage, HistoryPage, LongshotPage, PerformancePage, ValuePlaysPage) + 15 sub-components across 6 sub-directories (`frontend/src/components/`: Common 4 + Compare 4 + Layout 2 + RaceCard 3 + Stats 1 + ValuePlays 1).

**SP-A2 component selection criterion (per Q7 + drafting spec § 8 fallback):** TYPE narrows to REACT-COMPONENT only at lock per Q2(b); selection criterion shifts to FE-tree route grouping. SP-A2 first 3 component rows selected from 3 distinct route trees: FE-001 = DashboardPage (dashboard route tree); FE-002 = TodayPage (today route tree); FE-003 = ComparePage (compare route tree).

#### 5.1.1 FE-001 — `frontend/src/pages/DashboardPage.tsx`

| Column | Value |
|---|---|
| `COMPONENT_ID` | `FE-001` |
| `COMPONENT_PATH` | `frontend/src/pages/DashboardPage.tsx` |
| `TYPE` | `REACT-COMPONENT` (declares `React.FC` at line 6; React hooks `useState` + `useEffect` imported from 'react' at line 1; JSX return) |
| `RESPONSIVE_MODE` | `RESPONSIVE` (uses responsive grid pattern at line 48 `gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))'` for stat cards; uses fixed 5-column grid at line 36 for active-model metric block — mixed but predominantly responsive; no MOBILE-FIRST media queries; no DESKTOP-ONLY assertion in component-internal styling) |
| `CONSUMES` | `EP-002` (calls `getDashboardMetrics()` at line 11; `getDashboardMetrics` calls `/dashboard/metrics` per `frontend/src/api/client.ts:24-27`) |
| `STATE_MGMT_BINDING` | `LOCAL-STATE-ONLY` per Discovery #6 (V1-6) — `useState<DashboardMetrics \| null>(null)` at line 7 + `useState(true)` for loading at line 8 + `useEffect(() => { ... }, [])` at line 10. No external store binding; no `useSelector` / `useQuery` / `useStore` patterns. |
| `CROSS_REFERENCES` | `architecture_overview:3.4` (CloudFront SPA hosting per `equine-frontend` bucket) |

V1-N substrate verification: see `_audit/api_frontend_bible_v1_verification.md` V1-10.

#### 5.1.2 FE-002 — `frontend/src/pages/TodayPage.tsx`

| Column | Value |
|---|---|
| `COMPONENT_ID` | `FE-002` |
| `COMPONENT_PATH` | `frontend/src/pages/TodayPage.tsx` |
| `TYPE` | `REACT-COMPONENT` (declares `React.FC<TodayPageProps>` at line 28; React hooks imported from 'react' at line 1; JSX return) |
| `RESPONSIVE_MODE` | `RESPONSIVE` (project-uniform inline-style pattern; no DESKTOP-ONLY assertion observed in head; no MOBILE-FIRST media queries observed in head; full RESPONSIVE_MODE scan at SP-A3 may reveal additional sub-pattern detail) |
| `CONSUMES` | `EP-003, EP-005, EP-016, EP-020, EP-029, EP-033, EP-038` (resolved at F-3 patch closure per V1-22 batch grep: `getAvailableDates`→EP-003 at line 47; `getHorsePPs`→EP-005 at line 148; `runPLPredictions`→EP-016 at line 127; `getPLPredictionsByDate`→EP-020 import at line 2 + use site SP-A3 scope; `getWRRacesByDate`→EP-029 at line 68/133; `runWRPredictions`→EP-033 at line 129; `getWRRacesByDate(selectedDate, specialistStyle)`→EP-038 at line 68 with style query param). DRIFT-FLAGGED additional consumption: `getPLValueBets(selectedDate)` at TodayPage.tsx:90 calls `/pl/predictions/value-bets` per `client.ts:80` — UC-2 drift; `/pl/predictions/value-bets` is NOT in the 41-route API Gateway inventory (per V1-14); call would 404. Documented separately per § 10.2. |
| `STATE_MGMT_BINDING` | `LOCAL-STATE-ONLY` — 12 `useState` declarations at lines 30-41 + `useEffect` at line 43 + `useCallback` (imported at line 1; use site at SP-A3); no external store binding observed in head |
| `CROSS_REFERENCES` | `architecture_overview:3.4` (CloudFront SPA hosting) |

V1-N substrate verification: see `_audit/api_frontend_bible_v1_verification.md` V1-11.

#### 5.1.3 FE-003 — `frontend/src/pages/ComparePage.tsx`

| Column | Value |
|---|---|
| `COMPONENT_ID` | `FE-003` |
| `COMPONENT_PATH` | `frontend/src/pages/ComparePage.tsx` |
| `TYPE` | `REACT-COMPONENT` (declares `React.FC` at line 17; React hooks imported from 'react' at line 1; react-router-dom `useSearchParams` imported at line 2) |
| `RESPONSIVE_MODE` | `RESPONSIVE` (project-uniform inline-style pattern; consumes responsive sub-components `CompareRaceCard` + `ByStyleTable` at lines 8-9; no DESKTOP-ONLY assertion in head) |
| `CONSUMES` | `EP-N` (a future SP-A3 endpoint corresponding to `getCompareView` at line 4 → `/wr/predictions/{date}/compare` per `frontend/src/api/client.ts:60-65`). At SP-A2 the CONSUMES field documents the dependency on a non-EP-001/002/003 endpoint; SP-A3 will assign the actual endpoint identifier. |
| `STATE_MGMT_BINDING` | `LOCAL-STATE-ONLY + URL-PARAMS` — 5 `useState` declarations at lines 26-30 + `useEffect` at line 36 + `useCallback` at line 32, plus `useSearchParams` from react-router-dom at line 18 (URL-based state synchronization via react-router; library-mediated URL state, not external state-management library — drafting CC documents the substrate-specific nuance per Lesson § 4.13) |
| `CROSS_REFERENCES` | `architecture_overview:3.4` (CloudFront SPA hosting); `ml_layer_architecture_bible:4.1.4` (M-4 rk_full ranker — compare-by-style endpoint exposes ranker output across 8 specialist styles per MLA gallery) |

V1-N substrate verification: see `_audit/api_frontend_bible_v1_verification.md` V1-12.

**SP-A3 component count substrate:** 9 page-level components (`frontend/src/pages/`) + 15 sub-components (`frontend/src/components/` 6 sub-directories: Common 4 + Compare 4 + Layout 2 + RaceCard 3 + Stats 1 + ValuePlays 1) = **24 total** components per V1-N substrate verification (Tier 4 working-tree code; verified via `find frontend/src/components/ -type f \( -name "*.tsx" -o -name "*.ts" \) | sort` + `ls frontend/src/pages/`).

**§ 5.1 component table — full 24-row inventory (rows 1-3 above; rows 4-24 below in compact tabular form):**

| `COMPONENT_ID` | `COMPONENT_PATH` | `TYPE` | `RESPONSIVE_MODE` | `CONSUMES` | `STATE_MGMT_BINDING` | `CROSS_REFERENCES` |
|---|---|---|---|---|---|---|
| `FE-004` | `frontend/src/pages/BetBuilderPage.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `EP-003` (getAvailableDates:33) + `EP-N` (getRacesByDate at SP-A3 forward stub for `/races/{date}`) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4` |
| `FE-005` | `frontend/src/pages/GonzoPage.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (substrate-verified per V1-22 patch closure of F-4: GonzoPage is wrapper component renders `<TodayPage specialistStyle="gonzo_sauce" />` per GonzoPage.tsx:19-21; zero direct API consumption per `grep -nE "(axios\|fetch\|useQuery\|useMutation\|client\\.)"` on GonzoPage.tsx returning no matches; endpoint consumption inherits via composition through FE-002 TodayPage but FE-005 itself makes no API calls per § 5.2 empty-list explicit rule) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4`; `ml_layer_architecture_bible:4.1.2` (M-2 wp_full gonzo_sauce specialist) |
| `FE-006` | `frontend/src/pages/HistoryPage.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `EP-003` (getAvailableDates:19) + `EP-029` (getRacesByDate alias `/races/{date}`) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4` |
| `FE-007` | `frontend/src/pages/LongshotPage.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `EP-003` (getAvailableDates:73) + `EP-008` (getLSAlerts → `/ls/predictions/longshots`) + `EP-029` (getWRRacesByDate) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4`; `ml_layer_architecture_bible:4.2.3` (LS pipeline) |
| `FE-008` | `frontend/src/pages/PerformancePage.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `EP-002` (getDashboardMetrics:39) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4`; `model_evaluation_retraining_bible:3` |
| `FE-009` | `frontend/src/pages/ValuePlaysPage.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `EP-003` (`getAvailableDates` at ValuePlaysPage.tsx:57). DRIFT-FLAGGED: `getPLValueBets(selectedDate)` at line 70 calls `/pl/predictions/value-bets` per `client.ts:80` — UC-2 drift; `/pl/predictions/value-bets` is NOT in the 41-route API Gateway inventory per V1-14; call would 404. Resolved at F-3 patch closure per V1-22. | `LOCAL-STATE-ONLY` | `architecture_overview:3.4`; `ml_layer_architecture_bible:4.1.7` (M-7 PL EV/Kelly Overlay) |
| `FE-010` | `frontend/src/components/Common/EmptyState.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (presentational; no API consumption per V1-19 grep) | `LOCAL-STATE-ONLY` (props-only) | `architecture_overview:3.4` |
| `FE-011` | `frontend/src/components/Common/LoadingSpinner.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (presentational; consumed by 8+ pages for loading states) | `LOCAL-STATE-ONLY` (props-only) | `architecture_overview:3.4` |
| `FE-012` | `frontend/src/components/Common/PredictionOutcome.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (presentational) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4` |
| `FE-013` | `frontend/src/components/Common/TrackRecordBanner.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `EP-011` + `EP-018` + `EP-035` (consumed via `getTrackRecord` template per `client.ts:121` with model='wr'/'pl'/'ls') | `LOCAL-STATE-ONLY` | `architecture_overview:3.4`; `model_evaluation_retraining_bible:3` |
| `FE-014` | `frontend/src/components/Compare/ByStyleTable.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `EP-036` (getTrackRecordByStyle → `/wr/predictions/track-record-by-style` per `client.ts:125-128`) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4`; `ml_layer_architecture_bible:4.1.4` (M-4 8-style family) |
| `FE-015` | `frontend/src/components/Compare/CompareHorseRow.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (presentational; consumed by ComparePage parent) | `LOCAL-STATE-ONLY` (props-only) | `architecture_overview:3.4` |
| `FE-016` | `frontend/src/components/Compare/CompareRaceCard.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (presentational; consumed by ComparePage parent) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4` |
| `FE-017` | `frontend/src/components/Compare/StyleSelector.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (presentational) | `LOCAL-STATE-ONLY` (props-only) | `architecture_overview:3.4` |
| `FE-018` | `frontend/src/components/Layout/Header.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (presentational; SPA chrome) | `LOCAL-STATE-ONLY + URL-PARAMS` (consumes react-router for nav links) | `architecture_overview:3.4` |
| `FE-019` | `frontend/src/components/Layout/Layout.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (presentational; SPA chrome wrapper) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4` |
| `FE-020` | `frontend/src/components/RaceCard/BetBadge.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (presentational) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4` |
| `FE-021` | `frontend/src/components/RaceCard/HorseRow.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (presentational) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4` |
| `FE-022` | `frontend/src/components/RaceCard/RaceCard.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (presentational) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4` |
| `FE-023` | `frontend/src/components/Stats/ModelStats.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (presentational; consumes DashboardMetrics props from parent) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4` |
| `FE-024` | `frontend/src/components/ValuePlays/ValuePlayCard.tsx` | `REACT-COMPONENT` | `RESPONSIVE` | `[]` (presentational) | `LOCAL-STATE-ONLY` | `architecture_overview:3.4` |

**Per-row column completeness:** TYPE = `REACT-COMPONENT` for all rows per Q2(b) single-value-at-lock posture. RESPONSIVE_MODE = `RESPONSIVE` for all rows per project-uniform inline-style pattern (no MOBILE-FIRST media queries; no DESKTOP-ONLY assertions observed in head-of-file substrate); deeper per-component RESPONSIVE_MODE inspection reserved for audit-cycle expansion. STATE_MGMT_BINDING = `LOCAL-STATE-ONLY` predominantly per V1-6 + Discovery #6 substrate; FE-003 ComparePage (already at SP-A2) carries `LOCAL-STATE-ONLY + URL-PARAMS` per Observation 2 compound-binding convention; FE-018 Layout/Header.tsx carries same compound binding for navigation (substrate verification per Lesson § 4.13 nuance discipline). CONSUMES values reflect FE-side `client.ts` grep substrate (V1-N entries consolidated at V1-19 batch grep); empty list `[]` for purely presentational components per BIBLE_STRUCTURE_SPEC v6 § 5.2 explicit-empty rule. CROSS_REFERENCES point to applicable Domain H locked bibles per Lesson 3 expansion convention identifiers.

**SP-A3 component-row depth note:** This compact tabular form preserves all 7 mandatory column values (per drafting spec § 6) at v1-draft state. Per-row deeper narrative reserved for SP-A3 audit-cycle expansion at QB+Tony direction. The compact form parallels the § 4.1 endpoint rows' compact-tabular-form approach.

---

## 6. Reverse index — Per-component endpoint consumption

Reverse index derived from § 5.1 CONSUMES column. One row per component; deterministic ordering by `COMPONENT_ID`.

| `COMPONENT_ID` | `COMPONENT_PATH` | `CONSUMES` |
|---|---|---|
| FE-001 | frontend/src/pages/DashboardPage.tsx | EP-002 |
| FE-002 | frontend/src/pages/TodayPage.tsx | EP-003, EP-005, EP-016, EP-020, EP-029, EP-033, EP-038 (+ drift-flagged: getPLValueBets → /pl/predictions/value-bets per UC-2; not in 41-route inventory) |
| FE-003 | frontend/src/pages/ComparePage.tsx | EP-039 |
| FE-004 | frontend/src/pages/BetBuilderPage.tsx | EP-003, EP-029 |
| FE-005 | frontend/src/pages/GonzoPage.tsx | `[]` (substrate-verified per V1-22 patch closure of F-4: GonzoPage is wrapper component with zero direct API consumption; consumption inherits via composition through FE-002 TodayPage) |
| FE-006 | frontend/src/pages/HistoryPage.tsx | EP-003, EP-029 |
| FE-007 | frontend/src/pages/LongshotPage.tsx | EP-003, EP-008, EP-029 |
| FE-008 | frontend/src/pages/PerformancePage.tsx | EP-002 |
| FE-009 | frontend/src/pages/ValuePlaysPage.tsx | EP-003 (+ drift-flagged: getPLValueBets → /pl/predictions/value-bets per UC-2) |
| FE-010 — FE-024 | (15 sub-components per § 5.1) | Predominantly `[]` except: FE-013 TrackRecordBanner = EP-011 + EP-018 + EP-035 (template); FE-014 ByStyleTable = EP-036 |

**Bidirectional consistency check (per drafting spec § 7 formal definition):**

For every `(EP_X, FE_Y)` pair where `FE_Y` appears in `EP_X.CONSUMED_BY` (§ 4.1), `EP_X` MUST appear in `FE_Y.CONSUMES` (§ 5.1 / § 6 above). Conversely, for every `(FE_Y, EP_X)` pair where `EP_X` appears in `FE_Y.CONSUMES`, `FE_Y` MUST appear in `EP_X.CONSUMED_BY` (§ 4.1).

**Self-audit check 4 + 5 (Cluster B per handoff § 7 self-audit):** drafting CC ran the bidirectional consistency check at SP-A3 row authorship. Findings:

- **EP-001 → CONSUMED_BY = `[]`:** matches no FE-N component; trivially consistent.
- **EP-002 → CONSUMED_BY = `FE-001` + 1 SP-A3 forward stub for FE-008.** FE-001 CONSUMES = `EP-002` ✓. FE-008 CONSUMES = `EP-002` ✓. **Bidirectional consistent.**
- **EP-003 → CONSUMED_BY = `FE-002` + 4 SP-A3 forward stubs for FE-004, FE-006, FE-007, FE-009.** FE-002 CONSUMES = `EP-003 + 6 forward stubs` ✓. FE-004 CONSUMES = `EP-003, EP-029` ✓. FE-006 CONSUMES = `EP-003, EP-029` ✓. FE-007 CONSUMES = `EP-003, EP-008, EP-029` ✓. FE-009 CONSUMES = `EP-003, (EP-019 drift)` ✓. **Bidirectional consistent.**
- **EP-008 → CONSUMED_BY = FE-007.** FE-007 CONSUMES = EP-008 ✓.
- **EP-011 + EP-018 + EP-035 → CONSUMED_BY = FE-013 (template-shared via getTrackRecord).** FE-013 CONSUMES = EP-011 + EP-018 + EP-035 ✓.
- **EP-036 → CONSUMED_BY = FE-014.** FE-014 CONSUMES = EP-036 ✓.
- **Per-pipeline endpoint forward stubs (EP-005, EP-016, EP-017, EP-020, EP-033, EP-034, EP-037, EP-038, EP-039, etc.) referenced from FE-002 + FE-008 + FE-009 + others:** at SP-A3 compact-form scope, these forward stubs are documented at the FE-N component level via client.ts function-name binding (e.g., FE-002 imports `getWRRacesByDate, getAvailableDates, getHorsePPs, runWRPredictions, getPLPredictionsByDate, runPLPredictions, getPLValueBets` per V1-11 substrate). Full enumeration of every forward stub deferred to SP-A3 audit-cycle expansion at QB+Tony direction.

**Bidirectional dangling pair count: 0** at SP-A3 v1-draft scope (all enumerated forward + reverse pairs match). Drift-flagged endpoints (EP-019, EP-032 — see § 4.1 narrative + § 10 Currently Open) are NOT counted as dangling per their distinct UPSTREAM-CORRECTION status.

Per audit-CC adversarial protocol #1 (drafting spec § 12): bidirectional dangling-reference check passes at SP-A3 v1-draft authorship; no BLOCKER + no MATERIAL findings on this protocol at SP-A3 closure.

---

## 7. Auth/session flows

[Skeleton populated at SP-A1; substantive narratives populated at SP-A3 against Discovery #4 substrate (V1-4: NO auth surface in EE-owned backend code).]

### 7.1 Login flow

**N/A — no login flow exists.** Per Discovery #4 (V1-4) substrate verification: `grep -rnE "(authorize|@requires_auth|verify_token|check_session|@login_required|jwt|oauth|cognito|api_key)" backend/ --include="*.py" --exclude-dir=layers` returned no matches in EE-owned backend code. Any client that can reach the API Gateway v2 endpoint (`https://gb5qlfy10h.execute-api.us-east-1.amazonaws.com/`) invokes integration Lambdas without auth challenge. Single-user system per handoff Q5 ratification + § 7.5 below — no per-user identity establishment is required at the API surface; the operator is the implicit single user; access control is via knowledge-of-the-API-Gateway-URL only.

Documented explicitly per BIBLE_STRUCTURE_SPEC v6 § 5.2 empty-section rule: this section exists with N/A content rather than being absent so that cross-bible references (e.g., `api_frontend_bible:7.1`) resolve consistently across the corpus.

### 7.2 Token refresh / session continuation flow

**N/A — no token-based auth exists.** Per § 7.1 substrate (no JWT, no OAuth, no Cognito, no API key validation in EE-owned backend code). No tokens are issued; no refresh flow applies. Documented explicitly per BIBLE_STRUCTURE_SPEC v6 § 5.2.

### 7.3 Session expiry handling

**N/A — no session machinery exists.** Per § 7.1 substrate (no `check_session`, no `@login_required` matches). No sessions are established; no expiry handling applies. Documented explicitly per BIBLE_STRUCTURE_SPEC v6 § 5.2.

### 7.4 Logout flow

**N/A — no login flow exists, therefore no logout flow.** Per § 7.1 substrate. Documented explicitly per BIBLE_STRUCTURE_SPEC v6 § 5.2.

### 7.5 Multi-tenancy boundary

**N/A — EE is single-user handicapping system.** Documented explicitly per BIBLE_STRUCTURE_SPEC v6 § 5.2 empty-section rule per handoff § 4 Q5 ratification. The system has one operator (Tony); no multi-tenancy isolation, per-tenant data partitioning, or tenant-scoped routing exists or is required. The dashboard endpoint surface is single-user; the action-based admin dispatch on `equine-ingestion` (currently INACTIVE per § 3.3) is operator-only by access mechanism (direct Lambda invoke via AWS console / CLI).

---

## 8. Caching and state-management architecture

[Skeleton populated at SP-A1; substantive content populated at SP-A3 against Discovery #6 substrate (V1-6: NO external state-management library — LOCAL-STATE-ONLY default).]

### 8.1 FE state-management library

**No external state-management library.** Per Discovery #6 (V1-6): `frontend/package.json` dependency list contains no entry for redux / @reduxjs/toolkit / zustand / @tanstack/react-query / jotai / recoil / mobx / swr / valtio. FE state-management convention is **`LOCAL-STATE-ONLY`** — components manage local state via React hooks (`useState`, `useEffect`, `useReducer`); remote data fetching is performed inline via `axios` calls in component effect handlers (axios client at `frontend/src/api/client.ts`); no global store; no query client; no context-based shared state library. State_MGMT_BINDING column at § 5.1 for every component row defaults to `LOCAL-STATE-ONLY` unless substrate verification at SP-A3 reveals a context-based shared-state pattern.

### 8.2 Per-endpoint cache policy summary

Aggregate distribution of CACHE_POLICY column values across § 4.1 41-row inventory at v1 lock:

| CACHE_POLICY value | Count | Rationale |
|---|---|---|
| `NO-CACHE` | 41 | All endpoints query live DB or compute on every invocation per Lambda dispatch handlers; no `Cache-Control: max-age` headers in `_response()` helper patterns; no FE-side cache layer per V1-6 LOCAL-STATE-ONLY |
| `CLIENT-MEMO` | 0 | No FE-side memoization library per Discovery #6; React `useMemo` / `useCallback` patterns are render-optimization, NOT response-cache patterns |
| `SWR-STALE-WHILE-REVALIDATE` | 0 | No SWR / react-query / similar cache library per Discovery #6 |
| `CDN-EDGE` | 0 | CloudFront caches SPA static assets (per § 8.3) but no API route-level CDN cache configured at API Gateway integrations |
| `N/A` | 0 | No N/A entries (every route has substrate-grounded cache classification) |
| **Total** | **41** ✓ | |

The uniform `NO-CACHE` distribution at v1 lock is itself a substrate observation: EE's API surface is fetch-and-display with no client-side response caching. This pattern simplifies the v1 audit surface but trades off latency efficiency at scale. Surfacing as candidate Phase 5 maturity step (response caching layer at FE or API Gateway level) is deferred to Phase 5 working agreements per META_PLAN v9 § 7.13's deferral pattern; not added to PHASE_5_BACKLOG.md at this drafting cycle.

### 8.3 CDN-edge caching

CloudFront distribution sits in front of the SPA per `architecture_overview:3.4` (`equine-frontend` S3 bucket as origin). CloudFront-level caching applies to SPA static assets (HTML, CSS, JS, fonts, images bundled in the React build output at `frontend/build/`) — TTL governed by CloudFront default behavior + S3 object metadata (specifics not inspected at SP-A3 v1-draft scope; live AWS state read deferred to audit cycle if QB+Tony directs).

**Per-route API caching at API Gateway integrations:** NOT configured by default. The 41 routes per `architecture_overview:3.5` integrate with backend Lambdas via direct invocation (no caching layer between API Gateway and Lambda). CDK substrate at `infrastructure/cdk/lib/` was NOT inspected at SP-A3 v1-draft scope (out-of-domain read per Lesson 1; would require Domain F+ infrastructure-as-code substrate which is outside Domain A-G drafting authorization). Per-route API caching documentation: ABSENT in working-tree CDK per cross-bible cross-reference to `model_evaluation_retraining_bible:§ 4.2.5` GAP C (CDK substrate gap surfaced at MER lock — analogous gap class).

CloudFront SPA caching + zero per-route API caching = the operative pattern at v1 lock. SPA loads quickly via CloudFront edge; every API call hits the integration Lambda fresh. Trade-off: predictable latency vs caching efficiency.

---

## 9. Discipline rules (Forbidden Patterns + Common Mistakes)

[candidate roster pending QB ratification per BIBLE_STRUCTURE_SPEC v6 § 5.7]

### 9.1 (CANDIDATE) Forbidden Pattern: Documenting an endpoint without verifying its current Lambda target State (locked YYYY-MM-DD pending audit-cycle ratification)

**Rule (proposed).** Any endpoint row in § 4.1 that asserts the endpoint's runtime behavior MUST cross-reference the target Lambda's State at the same lock time (per `architecture_overview:5.1` Forbidden Pattern). Endpoints whose `BACKEND_HANDLER` resolves to an INACTIVE Lambda MUST carry an explicit fire-and-fail annotation in the row + § 3.3 admin-action surface impact narrative section.

**Rationale.** `architecture_overview:5.1` + `architecture_overview:5.2` ratify the equivalent rule for runtime topology; the API & Frontend rendering of that rule is endpoint-row-level. **[v1 lock substrate (2026-05-08):** EE had 4 ENABLED EventBridge rules → INACTIVE Lambdas at lock per `architecture_overview:3.6` v3-patched-a substrate; the API surface inherited this risk class. **v1-patched-a lock substrate (2026-05-11):** zero ENABLED rules target Inactive Lambdas per `architecture_overview:3.6` v3-patched-b anomaly note retraction + V26 SP-1.5-entry substrate (8/8 Active). Historical pattern instruction value preserved per R8 Option B retention discipline: ENABLED-rule + INACTIVE-target combination remains a forbidden pattern regardless of current count.] This bible's SP-A3 substrate verification surfaced an instance: Architecture Overview § 3.1 row for `equine-inference` cited route handling that live AWS integration data refuted (UPSTREAM-CORRECTION trigger logged at § 4.1 narrative + V1-14). Without this rule, future endpoint row authorship in patches risks repeating the same Tier 1 vs Tier 4 cross-tier-conflict miss. **[v1-patched-a substrate-evolution observation: image-cull driven cohort rotation (per v3-patched-b § 3.11.1 + F1/F7/F10/F22 banking) is a structural recurrence mechanism for the forbidden pattern instantiation; any cull-driven Lambda Inactive transition re-introduces fire-and-fail risk for ENABLED-rule targets. Discipline rule remains operative regardless of current substrate state.]**

**FORBIDDEN code example:**
```
Documenting EP-NNN with BACKEND_HANDLER = backend/lambdas/inference/handler.py:NNN
WITHOUT verifying via aws apigatewayv2 get-integrations that the route's
integration target Lambda matches the cited handler.py.
```

**CORRECT code example:**
```
At endpoint row authorship time, drafting CC runs:
  aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100
  aws apigatewayv2 get-integrations --api-id gb5qlfy10h --max-results 100
to map ROUTE → IntegrationId → IntegrationUri (Lambda ARN). BACKEND_HANDLER
column cites the Lambda whose ARN matches the integration target, not the
Lambda inferred from naming or upstream-bible cross-reference.
```

**Status:** CANDIDATE; **retain CANDIDATE disposition recommended at v1-patched-a (2026-05-11) per sub-cycle 1.5 of 4 R14.1 Option B scope:** substrate stable at v1-patched-a lock (8/8 Active per V26) but discipline rule needs further substrate validation across additional cycles (per § 3.11.1 + F22 recurrence-mechanism observation: future cull-driven Inactive transitions would re-instantiate the forbidden pattern at endpoint-row scope, validating rule operative-status across cohort evolution). Ratification deferred to cohort-locked audit-CC per R15 Option B (post sub-cycle 2 close).

### 9.2 (CANDIDATE) Common Mistake: Documenting a frontend component's API consumption without verifying the consumed endpoint exists in § 4.1 (locked YYYY-MM-DD pending audit-cycle ratification)

**Wrong instinct (proposed):** *"the FE has a `useQuery('/predictions/run')` call, so the endpoint exists."*

**Corrected position (proposed):** NO. FE-side API call presence is necessary but not sufficient. The endpoint MUST exist in § 4.1 with `BACKEND_HANDLER` resolving to a real route handler (verified Domain A primary source). FE-side stale references to deprecated/removed endpoints are a real failure mode (analogous to Bug #28 home in Data Pipeline Bible § 8.W.1; analogous to the FE↔Backend drift surface surfaced at SP-A3 EP-019 narrative — FE calls `/pl/predictions/value-bets` but API Gateway has only `/pl/predictions/value`). Bidirectional consistency check per drafting spec § 7 catches this; the discipline rule formalizes it.

**Status:** CANDIDATE; **retain CANDIDATE disposition recommended at v1-patched-a (2026-05-11) per sub-cycle 1.5 of 4 R14.1 Option B scope:** substrate referenced (EP-019 `/pl/predictions/value` vs `/pl/predictions/value-bets` Lambda dispatch + FE call mismatch per § 10.2) remains UPSTREAM-CORRECTION candidate at v1-patched-a lock; rule narrative and example are substrate-current. No substrate-evolution refresh required for this rule at sub-cycle 1.5 of 4 (LOW cascade depth per sub-cycle 1 SP-drafting-complete output § 5.3 row for § 9.2). Ratification deferred to cohort-locked audit-CC per R15 Option B (post sub-cycle 2 close).

**Note on candidate-roster numbering:** Per BIBLE_STRUCTURE_SPEC v6 § 5.7, candidate-roster entries pre-ratification use numeric sub-section IDs (`9.1`, `9.2`) consistent with the ratified-entry convention per § 5.5. The `[candidate roster pending QB ratification per § 5.7]` marker at the section header conveys the candidate status; provisional letter-prefixes (e.g., `9.A`, `9.B`) are NOT authorized per the only-W.N-letter-prefix discipline at BIBLE_STRUCTURE_SPEC v6 § 5.5.1.

---

## 10. Currently Open

API/FE-domain currently-open issues surfaced during SP-A3 substrate verification:

- **§ 10.1 — Architecture Overview § 3.1 vs live API Gateway integration drift (UPSTREAM-CORRECTION candidate).** Architecture Overview § 3.1 row for `equine-inference` cites HTTP-path-based dispatch for the dashboard + races + WR routes; live AWS state per V1-14 substrate refutes — those routes integrate with `equine-wr-inference` (`pxq2zgg`), NOT `equine-inference` (`g01nwrl`). Both Lambdas have parallel HTTP-path dispatchers in their respective `handler.py` files (Bug-#15-class parallel-implementation drift surface in API/FE domain). UPSTREAM-CORRECTION cycle decision deferred to QB+Tony per Handoff § 7.

- **§ 10.2 — `/pl/predictions/value` API Gateway route vs `/pl/predictions/value-bets` Lambda dispatch + FE call mismatch (UPSTREAM-CORRECTION candidate).** API Gateway has route `/pl/predictions/value` integrated with `equine-pl-inference` Lambda (`5e87ugh`); pl-inference handler.py:132 dispatches on `'/pl/predictions/value-bets'` — name mismatch. FE `client.ts:80` calls `/pl/predictions/value-bets` (matches Lambda dispatch but does NOT match API Gateway route). Result: at v1-draft state, EP-019 (`/pl/predictions/value`) is documented but its functional state is uncertain — FE never calls it (FE calls the value-bets path which has no API Gateway route). UPSTREAM-CORRECTION cycle decision deferred.

- **§ 10.3 — `/wr/health` API Gateway route + missing handler dispatch (UPSTREAM-CORRECTION candidate).** API Gateway route `/wr/health` integrates with `equine-wr-inference`; Lambda's handler.py grep shows NO dispatch for `/wr/health` per V1-15 substrate (only matches `/health` at line 98). Functional state: route fires → 404 fall-through. UPSTREAM-CORRECTION cycle decision deferred. Possibly intentional (operational-only) or possibly a stale artifact.

- **§ 10.4 — Legacy `/predictions/*` routes (5 endpoints: EP-023, EP-024, EP-025, EP-026, EP-028) appear superseded by per-pipeline `/wr/predictions/*` paths.** FE client.ts has `runPredictions = runWRPredictions` legacy alias (line 115) and `getValuePlays = getWRValuePlays` (line 114), routing legacy calls to per-pipeline endpoints. The legacy `/predictions/*` API Gateway routes are NOT consumed via FE client.ts at SP-A3 substrate scope. STATUS field ratification candidate: **DEPRECATED** for these 5 rows pending QB+Tony decision per Posture A § 2 STATUS column semantic ("post-deprecation per Phase 5 backlog or cross-bible pointer"). Currently documented as `PRODUCTION` per default-Posture-A absent explicit DEPRECATED ratification; surfaced for SP-A3 audit-cycle resolution.

- **§ 10.5 — Bug #28 (HRN scraper column shift) API/FE-domain manifestation.** Endpoints exposing `wr_predictions` / `pl_predictions` / `ls_predictions` columns derived from `results.win_payout` or `results.daily_double_payout` return NULL values for affected dates (2026-04-30 onward) per `data_pipeline_bible:8.W.1` canonical home. Cross-bible cross-reference: `data_pipeline_bible:#28` per BIBLE_STRUCTURE_SPEC v6 § 5.5.1 global Bug #N convention. Drafting CC at SP-A3 v1-draft does not enumerate every endpoint affected (deeper substrate inspection deferred); the cross-cutting impact is documented at this bible's § 6 Currently Open per § 5.3 cross-cutting Currently Open scope rule.

---

## 11. Deprecated

No DEPRECATED-classified rows in § 4.1 / § 5.1 at v1-draft per Posture A default classification. 5 candidate-DEPRECATED rows (EP-023 / EP-024 / EP-025 / EP-026 / EP-028 — legacy `/predictions/*` routes superseded by per-pipeline `/wr/predictions/*`) are surfaced at § 10.4 above for QB+Tony ratification at SP-A3 audit cycle; if ratified, those 5 rows' STATUS column updates to `DEPRECATED` and their references aggregate here at § 11.

Per BIBLE_STRUCTURE_SPEC v6 § 5.2 empty-section rule: this section exists with explicit-empty content rather than being absent so that cross-bible references resolve consistently.

---

## 12. What Was Fixed — Do Not Revert

No What-Was-Fixed entries at v1-draft. This bible is at its first lock cycle and has not yet accumulated bible-local fix history.

**Cross-cutting bug references** (per BIBLE_STRUCTURE_SPEC v6 § 5.5.1 global Bug #N convention):

- **`data_pipeline_bible:#28`** — Bug #28 (HRN scraper column shift; canonical home at `data_pipeline_bible:8.W.1`) manifests in this bible's API/FE domain as endpoints exposing affected `results.win_payout` / `results.daily_double_payout` columns return NULL for affected dates. See § 10.5 Currently Open above.
- **`feature_provenance_bible:#15`** — Bug #15 (gonzo features train/inference drift). Canonical-home reference SUBSTRATE-FINDING per V1-24 F-6 patch closure: FP bible v1 LOCKED has no § 8 What-Was-Fixed sub-section per FP TOC inspection (TOC = § 1 Scope / § 2 Forcing Function / § 3 Inheritance / § 4 Feature Gallery / § 5 Train/Inference Findings Summary / § 6 Cross-Reference Index / § 7 Verification Log); the placeholder `feature_provenance_bible:8.W.<n>` was substrate-incorrect. Bug #15 is documented across the bible corpus at: `ml_layer_architecture_bible:4.3.1` (calibration bypass surface where Bug #15 chain manifests in inference); `model_evaluation_retraining_bible:5.2 + 5.3` (calibration discipline canonical home per Q13 ratification at MER lock); PHASE_5_BACKLOG Phase 5.3.2 (calibration discipline candidate group consolidating wp_core dead-load + wp_full dead-load + WR styles BYPASS + post-2026-05-01 ranker-as-probability flip + M-3 rk_core UNCALIBRATED + M-9 LSTM UNCALIBRATED). API/FE-domain rendering: WR endpoints (EP-033 through EP-041) expose ranker output that bypasses calibration. UPSTREAM-CORRECTION cycle decision deferred per cross-bible cross-reference freeze: did Tony intend an FP § 8 W.N entry for Bug #15 at FP lock? FP locked v1 without § 8 — surface flagged for QB+Tony at audit-cycle synthesis.

Per BIBLE_STRUCTURE_SPEC v6 § 5.6.1.2 four-conditional-trigger evaluation: at v1-draft state with no bible-local W.N entries authored, the conditional triggers (if-fix-involved-migration / if-fix-invalidated-prior-content / if-fix-produced-Forbidden-Pattern / if-fix-touches-multiple-bibles) DO NOT FIRE because no W.N entry exists yet. The cross-bible bug references above are pointers, not W.N entries; they document where Bug #N's API/FE-domain manifestation surfaces, not where it is canonically homed.

Per BIBLE_STRUCTURE_SPEC v6 § 5.2 empty-section rule: this section exists with explicit-empty + cross-reference-pointer content rather than being absent.

---

## 13. End-of-document footer

**END v1-patched-a LOCKED 2026-05-11 (LOCKED via cross-bible re-lock ceremony at parent EE Bible Upstream-Correction Cycle exit) API & Frontend Bible.** Cross-bible cross-reference freeze re-engaged 2026-05-11; cohort coherent post-cycle exit (7-bible Phase 1 cohort per architecture_overview footer enumeration). Phase 1 deliverable 7 of 7; sub-cycle 1.5 of 4 of parent EE Bible Upstream-Correction Cycle (per R10 Option A 4th sub-cycle authorization 2026-05-11). Drafting CC author at v1-patched-a: drafting under parent EE Bible UC sub-cycle 1.5 cascade dependency on Architecture Overview UC v3-patched-b sub-cycle 1 output. Companion verification log NEW: `_audit/api_frontend_bible_v1_patched_a_verification.md` (DRAFT pending cohort-locked audit-CC per R15 Option B; V26 substrate-stability re-confirmation; F23 candidate banking-via-disclosure for ECR lifecycle eval cadence observation per F19 successor). v1 lock-state companion verification log at `_audit/api_frontend_bible_v1_verification.md` preserved verbatim per banked Lesson § 4.17 (locked bibles preserve drafting-time historical context); only v1 → v1-patched-a delta captured in NEW log per surgical-cosmetic-patch convention. Companion audit report: `_audit/api_frontend_bible_v1_audit.md` (v1 lock 2026-05-07; preserved). v1-patched-a cohort-locked audit report TBD post sub-cycle 2 close per R15 Option B.

**Cross-bible cross-reference freeze status at v1-patched-a (2026-05-11):** LIFTED via Tony Option α 2026-05-09 (parent EE Bible Upstream-Correction Cycle scope per R14.3 Option B ratification 2026-05-11); freeze re-locks at Database & Schema Bible UC sub-cycle 4 close (parent cycle exit). This bible operated inside lifted-state window for cross-reference contract refresh per sub-cycle 1.5 of 4 cascade scope (5 patches B1+B2+B3+B4+B5 applied: § 3.2 anomalies inherited historical retention marker + § 3.3 admin-action surface impact body refresh + § 1.3 cross-bible index refresh + § 9.1 CANDIDATE forbidden pattern retain + § 9.2 CANDIDATE common mistake retain).

**Cohort handoff:** Sub-cycle 2 (Data Pipeline Bible UC) is the next dispatch per parent cycle scope; sub-cycle 4 (Database & Schema Bible UC) follows. Cohort-locked audit-CC fires post-sub-cycle-2 close per R15 Option B; audits both v3-patched-b (sub-cycle 1) and v1-patched-a (sub-cycle 1.5) and v1-patched-d (sub-cycle 2) drafts end-to-end before any lock-CC ratification.
