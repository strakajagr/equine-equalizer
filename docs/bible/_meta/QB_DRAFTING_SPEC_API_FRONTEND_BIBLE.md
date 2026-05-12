# Drafting Spec: API & Frontend Bible

Document: QB_DRAFTING_SPEC_API_FRONTEND_BIBLE
Phase: 1 (Bible) — deliverable 7 of 7 (drafting-order numbering per BIBLE_STRUCTURE_SPEC v6 § 8.2)
Status: Initial QB-authored content (drafting spec for fresh drafting CC session)
Author: QB (chat-authored; paste-routed via spec-write CC for disk persistence)
Date: 2026-05-07
Companion handoff: `_meta/QB_HANDOFF_API_FRONTEND_BIBLE_DRAFTING.md` (LOCKED 2026-05-07, 17,746 bytes)
Purpose: Specify the structural envelope, column schemas, V1 substrate-verification mandate, synchronization-point gates, audit-CC adversarial protocols, and verification log scope for drafting CC's V1-N work on `api_frontend_bible.md`.

---

## 1. Inheritance — read this first

Before any V1 substrate read, drafting CC reads:

1. **Companion handoff** `_meta/QB_HANDOFF_API_FRONTEND_BIBLE_DRAFTING.md` — full inheritance, seven-question ratifications, substrate authorization domains A-H, SP-A1/A2/A3 gate content, banked Lessons.
2. **Phase 0 substrate** (read-only context):
   - `_meta/META_PLAN.md` (v9 LOCKED) — Tier 1-7 source-priority hierarchy.
   - `_meta/BIBLE_STRUCTURE_SPEC.md` (v6 LOCKED) — § 3.2.1 + § 8.2 = forcing function for this bible; § 5.2 empty-section rule; § 5.3 cross-cutting canonical-home rule; § 5.6.1 § 8 What-Was-Fixed format; § 5.7 § 5 discipline-rule numbering; § 6.5 model-artifact-path conventions; § 7.5 INDEX role.
   - `_meta/AUDIT_METHODOLOGY.md` (v2-patched LOCKED) — § 4.1-4.11 banked; § 4.12 + § 4.13 operative pending patch.
   - `_meta/CONVERGENCE_CRITERIA.md` (v2 LOCKED) — V1-N convergence rules.
   - `_meta/TRIAGE_QUEUE_SPEC.md` (v1 LOCKED) — finding triage protocol.
3. **Domain H locked bibles** (read-only, for cross-reference declarations only):
   - `architecture_overview.md` v3 LOCKED 2026-05-05
   - `database_schema_bible.md` v1-patched-d2 LOCKED 2026-05-06
   - `data_pipeline_bible.md` v1-patched-c LOCKED 2026-05-06
   - `feature_provenance_bible.md` v1-patched-a-extended LOCKED 2026-05-07
   - `ml_layer_architecture_bible.md` v1 LOCKED 2026-05-07
   - `model_evaluation_retraining_bible.md` v1 LOCKED 2026-05-07

**Cross-bible cross-reference freeze: ACTIVE.** Drafting CC may declare cross-references INTO these bibles via Domain H read; drafting CC may NOT propose substantive corrections within this cycle. UPSTREAM-CORRECTION cycle per cohort Handoff § 7 = sole re-open path.

---

## 2. Forcing function (recap from handoff § 1)

Per BIBLE_STRUCTURE_SPEC v6 § 3.2.1 + § 8.2, `api_frontend_bible.md` documents:

- Per-endpoint API contracts (route, method, auth, request schema, response schema, error codes, status, cache policy).
- Per-frontend-component endpoint consumption mapping.
- Cross-coupling (API ↔ FE consumers).
- Auth/session flows (dedicated section).
- Caching/state-management boundaries (dedicated section).

Canonical home for: (a) per-endpoint contract surface; (b) per-component consumer mapping; (c) auth/session flow narrative; (d) FE state-management/caching architecture; (e) admin-action surface impact of upstream INACTIVE-Lambda fire-and-fail anomaly (per § 3.3 below).

---

## 3. Bible structural envelope — TOC for `api_frontend_bible.md` v1-draft

Drafting CC produces v1-draft with the following section structure. Numeric IDs per BIBLE_STRUCTURE_SPEC v6 conventions.
API & Frontend Bible
[lock-CC three-element metadata bundle: header status + revision history + footer]
[drafting CC initializes skeleton at v1-draft per banked Lesson 6 from Phase 1 Cohort cycle]

1. Scope of this bible
[Mission / Scope / Boundaries / Cross-Bible Cross-Reference Index]
2. Definitions
[domain-specific terminology; acronyms defined here once]
3. Runtime context for API & Frontend
3.1 Pointer-back cross-references to runtime topology
[architecture_overview:3.5 API Gateway v2 surface — 41 routes]
[architecture_overview:3.4 S3 SPA hosting — equine-frontend bucket + CloudFront]
[architecture_overview:3.1 Lambda inventory — 5 Active + 3 INACTIVE]
3.2 API/FE-domain anomalies inherited from upstream bibles
[fire-and-fail manifestations from architecture_overview:6 § Currently Open]
[any FP/MLA/MER cross-cutting anomalies that surface API/FE rendering — TBD by V1 substrate]
3.3 Admin-action surface impact (canonical home per architecture_overview:6 cross-reference contract)
[25-action admin dispatch on INACTIVE equine-ingestion Lambda]
[3 EventBridge-triggered admin actions: refresh_angle_stats + 2 default-case dispatches]
[22 manual-invoke admin actions error on invoke]
[explicit non-functional surface enumeration]
3.X [Drafting-CC-discovered API/FE-domain anomalies without upstream homes — added as needed during V1-N]
4. Endpoint inventory (per-endpoint exhaustive)
4.1 Endpoint table
[per-endpoint exhaustive row enumeration per § 5 column schema below in this drafting spec]
[ordering: deterministic by ENDPOINT_ID]
4.X [sub-sections only if endpoint groupings emerge as audit-helpful — drafting CC proposes, QB ratifies]
5. Component inventory (per-component exhaustive)
5.1 Component table
[per-component exhaustive row enumeration per § 6 column schema below in this drafting spec]
[ordering: deterministic by COMPONENT_ID]
6. Reverse index — Per-component endpoint consumption
[derived from § 5.1; bidirectional consistency with § 4.1 CONSUMED_BY]
[audit-CC adversarial protocol: bidirectional dangling-reference check per Q4 ratification]
7. Auth/session flows
7.1 Login flow
7.2 Token refresh / session continuation flow
7.3 Session expiry handling
7.4 Logout flow
7.5 Multi-tenancy boundary
[N/A — EE is single-user handicapping system; documented explicitly per BIBLE_STRUCTURE_SPEC v6 § 5.2]
8. Caching and state-management architecture
8.1 FE state-management library
[Redux / Zustand / React Query / Context / none — drafting CC discovers via Domain G substrate]
8.2 Per-endpoint cache policy summary
[aggregate view of CACHE_POLICY column from § 4.1]
8.3 CDN-edge caching (if any)
[CloudFront-level caching for SPA assets; per-route caching for API Gateway integrations if configured]
9. Discipline rules
[per BIBLE_STRUCTURE_SPEC v6 § 5.7 conventions; numeric sub-section IDs]
[drafting CC proposes; QB+Tony ratify at audit cycle for inclusion]
[two candidate rule patterns surfaced in this drafting spec § 11 below]
10. Currently Open
[per BIBLE_STRUCTURE_SPEC v6 § 5.2 — if empty, document explicitly as empty]
11. Deprecated
[per BIBLE_STRUCTURE_SPEC v6 § 5.2 — DEPRECATED endpoints/components from § 4.1/§ 5.1 STATUS column aggregated here]
12. What Was Fixed — Do Not Revert
[per BIBLE_STRUCTURE_SPEC v6 § 5.6.1 + § 5.6.1.2; if empty at lock, document explicitly]

---

## 4. SP-A1 substrate-verification mandate (drafting CC tasks before § 1 / § 2 authorship)

Per Q7 SP-A1 gate: column schemas locked at SP-A1 before § 4.1 / § 5.1 row population begins. SP-A1 cannot close until the following six discoveries are persisted in the bible's § 1 (Scope) or § 2 (Definitions):

| # | Discovery | Domain | Substrate-verification method | Persistence locus |
|---|-----------|--------|-------------------------------|-------------------|
| 1 | **FE tree directory location** | D | `ls /home/strakajagr/projects/equine-equalizer/` + identify SPA-source directory (likely `frontend/`, `web/`, `app/`, `client/`, `ui/`, or similar — verify via presence of `package.json` + React imports). Cite exact path. | § 2 (Definitions) — define "FE tree" with verified path. |
| 2 | **Backend route framework** | A | `grep -rnE "from (fastapi\|flask\|aiohttp\|starlette\|django)" backend/lambdas/inference/handler.py backend/lambdas/ingestion/handler.py` + inspect handler dispatch pattern. Cite framework + version from `requirements.txt` or equivalent. | § 2 (Definitions) — define route-framework convention. |
| 3 | **Request/response schema framework** | B | `grep -rnE "from (pydantic\|marshmallow\|attrs)" backend/` + inspect any OpenAPI YAML/JSON in repo root or `backend/`. If TS interfaces apply (i.e., FE-side schemas mirror backend), inspect FE tree. Cite primary source + version. | § 2 (Definitions) — define type-sig notation in use. |
| 4 | **Auth framework** | C | `grep -rnE "(authorize\|@requires_auth\|verify_token\|check_session\|@login_required\|jwt\|oauth)" backend/` + inspect auth middleware decorators. If no auth surface (single-user system, internal-only), document N/A explicitly. | § 2 + § 7 (Auth flows) — define auth-framework convention OR document N/A. |
| 5 | **FE routing config** | F | Within FE tree: `grep -rnE "(react-router\|@reach/router\|wouter)" <fe-tree>/package.json + <fe-tree>/src/`. Cite library + version. | § 2 (Definitions) — define FE-routing convention. |
| 6 | **FE state-management library** | G | Within FE tree: `grep -rnE "(redux\|zustand\|@tanstack/react-query\|jotai\|recoil\|mobx)" <fe-tree>/package.json`. If none, FE state is local-component-state only — document explicitly. | § 2 + § 8 (Cache/state-management) — define state-mgmt convention OR document N/A. |

**Discipline:** every discovery cited with primary-source command output (verbatim per Lesson § 4.10) in the V1-N verification log. Discoveries are convention identifiers per Lesson 3 expansion — verified at primary source at row-authorship, NOT inferred from upstream bibles.

**SP-A1 closure criterion:** all six discoveries persisted; § 4.1 endpoint row column schema and § 5.1 component row column schema declared in TOC content; auth/session § 7 skeleton + cache/state-management § 8 skeleton present; cross-bible cross-reference index in § 1 declared.

---

## 5. § 4.1 endpoint row column schema (locked at SP-A1; mandatory for every endpoint row)

Per Q1+Q3+Q5+Q4+Q6 ratifications. Column ordering is the row ordering at v1-draft.

| Col # | Column name | Value space | Source domain | Notes |
|-------|-------------|-------------|---------------|-------|
| 1 | `ENDPOINT_ID` | Stable identifier (e.g., `EP-001` through `EP-NN`); deterministic ordering | drafting CC assigns | Used by `CONSUMES` field in § 5.1 reverse-index reference. |
| 2 | `ROUTE` | HTTP path string (e.g., `/predictions/run`, `/races/{race_id}/detail`) | Domain A primary source | Verbatim from route handler dispatch. |
| 3 | `METHOD` | `GET` / `POST` / `PUT` / `DELETE` / `PATCH` / `OPTIONS` | Domain A primary source | Verbatim from route handler. |
| 4 | `AUTH` | `PUBLIC` / `SESSION-COOKIE` / `BEARER-TOKEN` / `API-KEY` / `INTERNAL` / `N/A` | Domain C primary source | Single value per row at lock; multi-value (comma-separated) reserved for future. |
| 5 | `STATUS` | `PRODUCTION` / `DEPRECATED` / `INTERNAL-ONLY` / `EXPERIMENTAL` | Drafting CC + Domain A primary source | Convention precedent: MLA calibration-state column. |
| 6 | `CACHE_POLICY` | `NO-CACHE` / `CLIENT-MEMO` / `SWR-STALE-WHILE-REVALIDATE` / `CDN-EDGE` / `N/A` | Domain B + Domain G primary source | Drafting CC discovers operative values. |
| 7 | `REQUEST_TYPE_SIG` | Type-sig in operative notation (Pydantic / TS / OpenAPI per Discovery #3) | Domain B primary source | Code-block formatted; full type signature including optional/nullable/enum. |
| 8 | `REQUEST_EXAMPLE` | One canonical example payload (JSON or notation-appropriate equivalent) | Domain B primary source OR drafting CC synthesizes from type-sig if no canonical example exists in source | Code-block formatted. |
| 9 | `RESPONSE_TYPE_SIG` | Type-sig in operative notation | Domain B primary source | Code-block formatted. |
| 10 | `RESPONSE_EXAMPLE` | One canonical example payload | Domain B primary source OR drafting CC synthesizes | Code-block formatted. |
| 11 | `ERROR_CODES` | Comma-separated HTTP status codes returned (e.g., `200, 400, 404, 500`) + per-code semantic if non-standard | Domain A primary source | Verbatim from route handler error-handling branches. |
| 12 | `CONSUMED_BY` | Comma-separated component identifiers from § 5.1 (deterministic ordering) | Domain D + E primary source via `grep` of FE tree | Forward index per Q4 ratification. Empty list = no FE consumers (e.g., admin actions invoked manually); document as `[]` not blank. |
| 13 | `BACKEND_HANDLER` | Path + line citation (e.g., `backend/lambdas/inference/handler.py:73-89`) | Domain A primary source | Lesson § 4.13 row-authorship verification. |
| 14 | `CROSS_REFERENCES` | Comma-separated `bible_name:section` references | Domain H read-only | E.g., `database_schema_bible:4.1.predictions, ml_layer_architecture_bible:4.2`. |

**Per-row primary-source-citation requirement:** every row's column #2-#13 values must be supported by a V1-N verification log entry with verbatim primary-source command output per Lesson § 4.10.

**Empty-list convention:** explicit empty-list `[]` per BIBLE_STRUCTURE_SPEC v6 § 5.2 empty-section rule (analogous treatment for empty-list cells); never blank.

---

## 6. § 5.1 component row column schema (locked at SP-A1; mandatory for every component row)

Per Q2+Q4+Q6 ratifications.

| Col # | Column name | Value space | Source domain | Notes |
|-------|-------------|-------------|---------------|-------|
| 1 | `COMPONENT_ID` | Stable identifier (e.g., `FE-001` through `FE-NN`); deterministic ordering | drafting CC assigns | Used by `CONSUMED_BY` field in § 4.1 forward-index reference. |
| 2 | `COMPONENT_PATH` | Path within FE tree (e.g., `<fe-tree>/src/components/RaceDetail.tsx`) | Domain D primary source | Verbatim path. |
| 3 | `TYPE` | `REACT-COMPONENT` (only value at lock) | Drafting CC + Domain D primary source | Other values (NEXT-PAGE / STATIC-HTML / VUE / TEMPLATE) reserved for future UPSTREAM-CORRECTION expansion. Single-value-at-lock posture documented explicitly in § 2 Definitions. |
| 4 | `RESPONSIVE_MODE` | `MOBILE-FIRST` / `RESPONSIVE` / `DESKTOP-ONLY` / `N/A` | Domain D primary source | Lesson § 4.13 row-authorship verification (inspect CSS / Tailwind / styled-components for responsive breakpoints). |
| 5 | `CONSUMES` | Comma-separated endpoint identifiers from § 4.1 (deterministic ordering) | Domain E primary source via `grep` of fetch/axios/useQuery/useMutation calls | Forward index in component direction; reverse-index source for § 6. Empty list = no API calls (purely presentational component); document as `[]`. |
| 6 | `STATE_MGMT_BINDING` | Library-specific identifier (e.g., `useQuery('races')`, `useSelector(state.predictions)`, `useStore(getRaces)`) OR `LOCAL-STATE-ONLY` | Domain G primary source | Cite primary source code line per Lesson § 4.13. |
| 7 | `CROSS_REFERENCES` | Comma-separated `bible_name:section` references | Domain H read-only | E.g., `architecture_overview:3.4` for SPA-hosting context where relevant. |

**Per-row primary-source-citation requirement:** every row's column #2-#6 values must be supported by a V1-N verification log entry with verbatim primary-source command output.

---

## 7. § 6 reverse index column schema

Derived from § 5.1. One row per component; deterministic ordering by `COMPONENT_ID`.

| Col # | Column name | Value space | Source |
|-------|-------------|-------------|--------|
| 1 | `COMPONENT_ID` | Same as § 5.1 col #1 | § 5.1 |
| 2 | `COMPONENT_PATH` | Same as § 5.1 col #2 | § 5.1 |
| 3 | `CONSUMES` | Same as § 5.1 col #5 | § 5.1 |

**Bidirectional consistency formal definition** (audit-CC adversarial protocol per Q4):

- For every `(EP_X, FE_Y)` pair where `FE_Y` appears in `EP_X.CONSUMED_BY` (§ 4.1), `EP_X` MUST appear in `FE_Y.CONSUMES` (§ 5.1 / § 6).
- For every `(FE_Y, EP_X)` pair where `EP_X` appears in `FE_Y.CONSUMES` (§ 5.1 / § 6), `FE_Y` MUST appear in `EP_X.CONSUMED_BY` (§ 4.1).
- Either direction's failure = audit finding (BLOCKER if ≥ 5 pairs; MATERIAL if 1-4 pairs).

---

## 8. SP-A2 gate content + closure criterion

Per Q7 SP-A2 gate: § 4.1 first 3 endpoint rows + § 5.1 first 3 component rows.

**Endpoint selection criterion (3 rows spanning AUTH value space):**

- Row 1: AUTH = `PUBLIC` (e.g., `/health` if exists; otherwise the lowest-auth-tier endpoint by AUTH column ordering).
- Row 2: AUTH = `SESSION-COOKIE` or `BEARER-TOKEN` (whichever is operative per Discovery #4 SP-A1; if both apply, pick whichever has the higher endpoint count in § 4.1).
- Row 3: AUTH = `INTERNAL` (e.g., admin action endpoints on `equine-ingestion` per Architecture Overview § 3.1; if no INTERNAL endpoints exist post-Discovery #4, substitute AUTH = `API-KEY` or document the value-space gap explicitly).

**Component selection criterion (3 rows spanning route trees):**

- Per Q7 ratification + Q2(b) TYPE narrowing to REACT-COMPONENT only at lock: span by FE-tree route grouping rather than TYPE diversity. Drafting CC selects 3 components from distinct route trees within the SPA (e.g., one from a dashboard route, one from a race-detail route, one from a prediction-run route — concrete groupings TBD by Discovery #5 SP-A1 routing-config substrate).

**SP-A2 closure criterion:** 6 rows populated (3 endpoint + 3 component); each row's columns fully populated; each row's V1-N verification log entries written with verbatim primary-source command output; row-format consistency check passes (audit-CC verifies SP-A2 row format matches SP-A1 column schemas exactly).

**Why SP-A2 matters:** validates row format across the column value spaces before drafting CC commits to populating all rows. SP-A2 row format becomes the v1-draft row format precedent.

---

## 9. SP-A3 gate content + closure criterion

Per Q7 SP-A3 gate: v1-draft complete.

**SP-A3 closure criterion (all of):**

- All endpoint rows populated in § 4.1 (count = 41 per Architecture Overview § 3.5 verified live 2026-05-05; if drafting CC's V1 substrate verification finds different count, surface to QB before SP-A3 closure).
- All component rows populated in § 5.1 (count TBD by V1 substrate verification within FE tree).
- § 6 reverse index populated; bidirectional consistency check passes per § 7 of this drafting spec.
- § 7 auth/session flows populated (or N/A documented per BIBLE_STRUCTURE_SPEC v6 § 5.2).
- § 8 cache/state-management populated (or N/A documented).
- § 1 + § 2 cross-bible cross-reference declarations complete.
- § 3.1 / § 3.2 / § 3.3 populated per Decision A § 3 sub-structure (pointer-back + anomaly inheritance + admin-action surface impact canonical-home content).
- § 10 / § 11 / § 12 declared (empty-section explicit declarations per BIBLE_STRUCTURE_SPEC v6 § 5.2 if applicable).
- Lock-CC three-element metadata bundle skeleton initialized (header status placeholder + revision history v1-draft entry + footer skeleton); lock CC populates final values at lock cycle, NOT drafting CC.

**Note on row count anchor:** Architecture Overview § 3.5 cites 41 routes verified live 2026-05-05 with `--max-results 100` to defeat default pagination. Drafting CC re-verifies live route count at SP-A1 substrate work via `aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100` (matching the Architecture Overview verification command exactly). If route count differs from 41, drafting CC surfaces to QB; QB surfaces to Tony for ratification before V1-N proceeds (this is a Tier 1 live AWS state finding which could be UPSTREAM-CORRECTION trigger on Architecture Overview § 3.5 if drift is found).

---

## 10. V1-N verification log scope (per Decision B ratification)

Drafting CC authors `_audit/api_frontend_bible_v1_verification.md` companion to v1-draft.

**V1-N entry structure (per Phase 1 cohort precedent):**
V1-N: <claim being verified>
Claim source: <bible section + row reference, e.g., § 4.1 row EP-007>
Substrate domain: <A/B/C/D/E/F/G/H>
Verification method: <command or read operation>
Verbatim output:
<verbatim primary-source command output — no summarization>
Conclusion: <CONFIRMED / REFUTED / PARTIAL — with explicit reasoning>

**Required V1-N entry coverage (the cardinality drives the verbatim-paste discipline test):**

| V1-N entry class | Approx count | Rationale |
|------------------|--------------|-----------|
| Endpoint row primary-source citations | ~41 (one per § 4.1 row × column #2-#13 verifications grouped per row) | Per Q1(a) per-endpoint exhaustive ratification. |
| Component row primary-source citations | TBD by V1 substrate (likely 20-100) | Per Q1(b) full-stack ratification. |
| SP-A1 discovery V1-N entries | 6 | Per § 4 of this drafting spec. |
| Cross-bible cross-reference V1-N entries | ~20-40 | Per § 1 + § 2 + § 3 cross-references to locked bibles. |
| Empty-section explicit-declaration V1-N entries | ~3-5 | Per BIBLE_STRUCTURE_SPEC v6 § 5.2 (multi-tenancy N/A; § 10 if empty; § 12 if empty; etc.). |

**Estimated total V1-N entries: 90-200.** Highest cohort volume. Lesson § 4.10 verbatim-paste discipline is itself a discipline test at this volume — surfaced explicitly per Decision B.

### Lesson § 4.10 verbatim-paste discipline reinforcement (per Decision B)

Banked from D-3.1 BLOCKER prototype (Data Pipeline Bible cycle, low V1-N volume context). At this bible's volume, summarization-at-scale is a foreseeable failure mode.

**Drafting CC discipline:**

1. Every V1-N entry's `**Verbatim output:**` block contains literal primary-source command output. No summarization, no truncation (except multi-line code blocks for readability — the *content* must remain verbatim).
2. If verbatim output exceeds 200 lines for a single command, drafting CC surfaces to QB for guidance before proceeding (do NOT silently truncate).
3. Multi-line code blocks per V1-N entry are permitted for readability formatting; content within remains verbatim from source.
4. `grep -n` line numbers preserved verbatim. File path prefixes preserved verbatim.
5. If primary source produces no matches (empty grep result), document explicitly: `**Verbatim output:** (no matches)` — this is itself substantive evidence for REFUTED conclusions.
6. **Anti-pattern:** "Drafting CC's paraphrase of grep result" — never. Always literal output.

---

## 11. Discipline rule candidates for § 9 of `api_frontend_bible.md`

Drafting CC proposes; QB+Tony ratify at audit cycle. Two candidate patterns surfaced based on cross-bible cohort lessons:

### Candidate 9.1: Forbidden Pattern — Documenting an endpoint without verifying its current Lambda target State

**Rule (proposed).** Any endpoint row in § 4.1 that asserts the endpoint's runtime behavior MUST cross-reference the target Lambda's State at the same lock time (per Architecture Overview § 5.1 Forbidden Pattern). Endpoints whose `BACKEND_HANDLER` resolves to an INACTIVE Lambda MUST carry an explicit fire-and-fail annotation in the row + § 3.3 admin-action surface impact narrative section.

**Rationale.** Architecture Overview § 5.1 + § 5.2 ratify the equivalent rule for runtime topology; the API & Frontend rendering of that rule is endpoint-row-level. EE has 4 ENABLED rules → INACTIVE Lambdas at lock; the API surface inherits this.

**Status:** Candidate; ratify at audit cycle.

### Candidate 9.2: Common Mistake — Documenting a frontend component's API consumption without verifying the consumed endpoint exists in § 4.1

**Wrong instinct (proposed):** *"the FE has a `useQuery('/predictions/run')` call, so the endpoint exists."*

**Corrected position (proposed):** NO. FE-side API call presence is necessary but not sufficient. The endpoint MUST exist in § 4.1 with `BACKEND_HANDLER` resolving to a real route handler (verified Domain A primary source). FE-side stale references to deprecated/removed endpoints are a real failure mode (analogous to Bug #28 home in Data Pipeline Bible § 8.W.1). Bidirectional consistency check per § 7 of this drafting spec catches this; the discipline rule formalizes it.

**Status:** Candidate; ratify at audit cycle.

---

## 12. Audit-CC adversarial protocol enumeration

Audit-CC paste-prompt at Step 8 will instantiate these protocols. Drafting spec lists them so drafting CC can self-audit at SP-A2 / SP-A3 gates per banked self-audit Cluster B + C checks.

| # | Protocol | Trigger | Failure severity |
|---|----------|---------|-------------------|
| 1 | **Bidirectional dangling-reference check** | Every `CONSUMED_BY` entry in § 4.1 must appear in § 5.1; every `CONSUMES` entry in § 5.1/§ 6 must appear in § 4.1. | BLOCKER if ≥ 5 dangling pairs; MATERIAL if 1-4. |
| 2 | **Per-row primary-source-citation completeness** | Every row column value (per § 5 + § 6 schemas) cites V1-N entry. | BLOCKER if ≥ 10% rows missing citations; MATERIAL if 1-9% missing. |
| 3 | **Empty-section explicit-declaration check** | § 7.5 multi-tenancy + any other empty section declared per BIBLE_STRUCTURE_SPEC v6 § 5.2. | MATERIAL if missing. |
| 4 | **Convention-identifier-source check** | Discoveries #1-#6 (§ 4 of drafting spec) cited at primary source per Lesson 3 expansion, NOT inferred from Domain H bibles. | MATERIAL if any Discovery sourced from Domain H without primary-source verification. |
| 5 | **Cross-reference-to-locked-bible accuracy** | Every `bible_name:section` reference in `CROSS_REFERENCES` columns + § 1/§ 2/§ 3 narrative resolves to a real section in the named locked bible. | MATERIAL if any reference dangles. |
| 6 | **Endpoint row count vs Architecture Overview § 3.5** | § 4.1 endpoint count matches Architecture Overview § 3.5 cited count (41 at last lock 2026-05-05) OR drafting CC surfaces drift to QB explicitly. | BLOCKER if drift undocumented; informational-only if drift documented (potential UPSTREAM-CORRECTION trigger). |
| 7 | **STATUS column distribution** | Every endpoint row has `STATUS` value populated; aggregated counts (PRODUCTION / DEPRECATED / INTERNAL-ONLY / EXPERIMENTAL) reported in § 1 narrative. | MATERIAL if any row missing STATUS. |
| 8 | **AUTH column verification at primary source** | Every row's AUTH value verified via Domain C primary-source read (auth middleware / decorator inspection), NOT inferred from route path naming patterns. | MATERIAL if any AUTH value lacks Domain C V1-N entry. |
| 9 | **CACHE_POLICY column verification** | Every row's CACHE_POLICY value verified via Domain B (response headers in handler) + Domain G (FE-side cache library config) primary source. | MATERIAL if any CACHE_POLICY value lacks both Domain B + Domain G V1-N entries. |
| 10 | **Verbatim-paste discipline at scale (Decision B reinforcement)** | Every V1-N entry's verbatim output block contains literal primary-source command output, not summarization. Audit-CC samples ≥ 20% of V1-N entries for verbatim-vs-summarization adjudication. | BLOCKER if any entry fails verbatim discipline (banked from D-3.1 BLOCKER prototype). |

---

## 13. Drafting CC paste-prompt scope preview (for Step 7)

The eventual Step 7 drafting CC paste-prompt will authorize:

- **Read scope:** Domain A-G primary substrate (per handoff § 4 Q6 ratification); Domain H locked-bible read for cross-reference declarations only.
- **Write scope:** `api_frontend_bible.md` (v1-draft authorship); `_audit/api_frontend_bible_v1_verification.md` (V1-N entries authorship).
- **No write authorization on:** any locked bible; any `_meta/` document; any other `_audit/` log; any backend or frontend source code.
- **Synchronization:** SP-A1 → SP-A2 → SP-A3 gated; CC pauses for QB+Tony ratification at each gate before proceeding.
- **Audit-CC handoff:** at SP-A3 closure, drafting CC's session ends; fresh audit-CC session opens for adversarial review per § 12 of this drafting spec.

This scope is materially larger than spec-write CC scope (mechanical-paste-only, single-file). Step 7 paste-prompt will detail authorization boundaries explicitly per banked Lessons 1 (inheritance read-scope discipline) + 7 (QB paste-verbatim discipline).

---

## 14. Structural decisions banked at handoff time (re-stated for drafting CC)

From `_meta/QB_HANDOFF_API_FRONTEND_BIBLE_DRAFTING.md` § 4 ratifications, the seven structural questions resolve as follows. These are operative constraints for drafting CC; do NOT re-litigate within this cycle.

- **Q1:** Per-endpoint exhaustive; full-stack; STATUS column with 4-value space.
- **Q2:** Single FE tree (React SPA); TYPE column narrows to REACT-COMPONENT only at lock; RESPONSIVE_MODE column populated at row-authorship.
- **Q3:** Type-sig + one canonical example per endpoint; type-sig notation per Discovery #3.
- **Q4:** Forward + reverse index; no NxM matrix; bidirectional dangling-reference audit.
- **Q5:** Both-and (per-endpoint AUTH + CACHE_POLICY columns + dedicated § 7 + § 8); multi-tenancy N/A explicit per BIBLE_STRUCTURE_SPEC v6 § 5.2.
- **Q6:** Eight-domain authorization (A-G primary; H read-only); out-of-domain reads = audit finding.
- **Q7:** SP-A1 column-schemas-locked; SP-A2 first-3-rows × 2; SP-A3 v1-draft complete; lock-CC three-element metadata bundle at lock cycle only.

From § 11 of this drafting spec, **Decision A** (§ 3 sub-structure): § 3.1 pointer-back / § 3.2 upstream anomaly inheritance / § 3.3 admin-action surface impact (canonical home per `architecture_overview:6` cross-reference contract).

From § 10 of this drafting spec, **Decision B** (V1-N verification log scope): standard pattern with Lesson § 4.10 verbatim-paste discipline reinforcement at high volume.

---

## 15. CC role authorization scope for THIS drafting spec document

The CC session that writes THIS file to disk has **mechanical paste authorization only**:

- Single-file write: `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/QB_DRAFTING_SPEC_API_FRONTEND_BIBLE.md`.
- Verbatim paste: no editing, summarizing, restructuring, or "improvement" of QB content.
- No substrate verification, no audit work, no other disk operations.
- If file already exists: error to QB; do NOT overwrite without QB authorization.

This authorization scope is distinct from drafting CC scope (which receives a separate paste-prompt at Step 7).

---

End of drafting spec content.
