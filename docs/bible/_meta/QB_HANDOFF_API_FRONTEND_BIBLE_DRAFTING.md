# Handoff: API & Frontend Bible Drafting

Document: QB_HANDOFF_API_FRONTEND_BIBLE_DRAFTING
Phase: 1 (Bible) — deliverable 7 of 7 (drafting-order numbering per BIBLE_STRUCTURE_SPEC v6 § 8.2)
Status: Initial QB-authored content (pre-drafting-spec)
Author: QB (chat-authored; paste-routed via spec-write CC for disk persistence)
Date: 2026-05-07
Cohort: Standalone (not parallel; final Phase 1 deliverable)
Purpose: Capture inheritance + ratifications + substrate authorization to inform drafting CC V1-N work on `api_frontend_bible.md`.

---

## 1. Forcing function

Per BIBLE_STRUCTURE_SPEC v6 § 3.2.1 + § 8.2, API & Frontend Bible documents:

- Per-endpoint API contracts: route, method, auth, request schema, response schema, error codes, status, cache policy.
- Per-frontend-component endpoint consumption mapping.
- Cross-coupling between API contracts and frontend consumers (which components break if which contracts change).
- Auth/session flows (dedicated section).
- Caching / state-management boundaries (dedicated section).

This bible is the canonical home for: (a) per-endpoint contract surface; (b) per-component consumer mapping; (c) auth / session flow narrative; (d) FE state-management / caching architecture. It cross-references all six locked Phase 1 bibles for upstream context (see § 2 below).

---

## 2. Phase 1 inheritance — six bibles LOCKED at handoff

| # | Bible | Version | Lock date | Path | Cross-reference role for API & Frontend |
|---|-------|---------|-----------|------|------------------------------------------|
| 1 | Architecture Overview | v3 | 2026-05-05 | `docs/bible/architecture_overview.md` | Runtime topology — API Gateway v2 (§ 3.5, 41 routes), CloudFront + S3 SPA hosting (§ 3.4 `equine-frontend` bucket), Lambda inventory (§ 3.1, 5 Active + 3 INACTIVE) for endpoint→Lambda mapping. |
| 2 | Database & Schema Bible | v1-patched-d2 | 2026-05-06 | `docs/bible/database_schema_bible.md` | Data shape — 15 domain tables + `trainer_stats` matview; canonical column shapes informing API response schemas. |
| 3 | Data Pipeline Bible | v1-patched-c | 2026-05-06 | `docs/bible/data_pipeline_bible.md` | Data flow context — 9 flows; Bug #28 canonical home § 8.W.1; per-flow Lambda dispatch informing endpoint behavior. |
| 4 | Feature Provenance Bible | v1-patched-a-extended | 2026-05-07 | `docs/bible/feature_provenance_bible.md` | Feature exposure surface — 80 production features + F-81 ORPHAN; quaternary 75 DUPLICATED + 2 DIVERGENT-INTENTIONAL + 0 DIVERGENT-UNINTENTIONAL + 3 UNVERIFIED; informs which features are exposed via which endpoints. |
| 5 | ML Layer Architecture Bible | v1 | 2026-05-07 | `docs/bible/ml_layer_architecture_bible.md` | Model output exposure — 11-entity gallery (8 trained + 3 non-trained); 2 CALIBRATED + 4 UNCALIBRATED + 5 BYPASS; per-pipeline prediction-shape exposure surface. |
| 6 | Model Evaluation & Retraining Bible | v1 | 2026-05-07 | `docs/bible/model_evaluation_retraining_bible.md` | Model evaluation surface exposure — 11-row gallery mirror; 36 VERIFIED + 11 PARTIAL + 0 UNVERIFIED + 8 N/A; informs evaluation/retraining-status endpoint exposure (if any). |

**Cross-bible cross-reference freeze: ACTIVE** since FP v1 lock per cohort Handoff § 6.1. UPSTREAM-CORRECTION cycle per Handoff § 7 = sole re-open path. The freeze applies to all six locked bibles. API & Frontend drafting CC may declare cross-references INTO these bibles via Domain H read-only access; drafting CC may NOT propose substantive corrections to locked bibles within this cycle. If during V1 substrate verification CC observes evidence that contradicts a locked bible's claim, CC surfaces the finding to QB; QB surfaces to Tony for UPSTREAM-CORRECTION cycle decision; that re-open path is separate from this drafting cycle's lock.

---

## 3. Phase 0 substrate inheritance

- META_PLAN v9 (locked) — methodology + Tier 1-7 source-priority hierarchy
- BIBLE_STRUCTURE_SPEC v6 (locked) — § 3.2.1 + § 8.2 = forcing function for this bible
- AUDIT_METHODOLOGY v2-patched (locked) — § 4.1-4.11 banked; § 4.12 + § 4.13 operative pending patch
- CONVERGENCE_CRITERIA v2 (locked) — V1-N convergence rules
- TRIAGE_QUEUE_SPEC v1 (locked) — finding triage protocol

---

## 4. Seven structural questions — Tony-ratified resolutions (2026-05-07)

### Q1: Bible scope boundary — RATIFIED

- **(a) Per-endpoint exhaustive.** Per-row treatment matches D&S column enumeration / FP feature enumeration / MLA-MER entity enumeration precedent. No per-route-group representative sampling.
- **(b) Full-stack.** Backend route handlers + frontend consumers both in scope. The cross-coupling matrix is the forcing-function-additive content.
- **(c) Current-production exhaustive with STATUS column.** Status values: PRODUCTION / DEPRECATED / INTERNAL-ONLY / EXPERIMENTAL. Convention precedent: MLA calibration-state column.

### Q2: Frontend coverage — RATIFIED

- **(a) Single FE tree.** Resolved via narrow upstream substrate read on Architecture Overview v3 § 1 / § 3.4 / § 3.5 (2026-05-07): EE has a single React SPA hosted on `equine-frontend` S3 + CloudFront. No Next.js, static HTML, Vue, or template-rendered surface. FE tree path TBD by CC V1 substrate verification per Lesson § 4.13.
- **(b) Framework-agnostic with TYPE column.** TYPE column value space at lock: **REACT-COMPONENT** only. Other values (NEXT-PAGE, STATIC-HTML, VUE, TEMPLATE) reserved for future UPSTREAM-CORRECTION expansion if EE FE stack diversifies. Drafting spec states the single-value-at-lock posture explicitly.
- **(c) RESPONSIVE-MODE column populated at row-authorship per Lesson § 4.13.** Values: MOBILE-FIRST / RESPONSIVE / DESKTOP-ONLY / N/A. Deeper mobile UX audit deferred to Phase 5.

### Q3: API contract granularity — RATIFIED

Type-signature primary + one canonical example payload per endpoint. Drafting CC discovers operative type-sig notation from primary source (Pydantic models / TS interfaces / OpenAPI spec — whichever EE primary source uses). Drafting spec mandates type-sig notation source-discovery at V1 substrate verification.

### Q4: Cross-coupling documentation depth — RATIFIED

Forward + reverse index pattern.

- **Forward index (primary):** per-endpoint row carries `CONSUMED_BY` field listing component identifiers (comma-separated, deterministic ordering by component identifier).
- **Reverse index:** end-of-bible per-component table; each row carries `CONSUMES` field listing endpoint identifiers.
- **No NxM matrix.**
- **Audit-CC adversarial protocol:** bidirectional dangling-reference check — every `CONSUMED_BY` entry must appear in reverse index; every `CONSUMES` entry must point back. Bidirectional dangling = audit finding.

### Q5: Auth/session and cache/state-management — RATIFIED both-and

- **Per-endpoint AUTH column.** Values: PUBLIC / SESSION-COOKIE / BEARER-TOKEN / API-KEY / INTERNAL / etc. Single value per endpoint at lock; multi-value semantics via comma-separated list reserved for future.
- **Per-endpoint CACHE_POLICY column.** Values: NO-CACHE / CLIENT-MEMO / SWR-STALE-WHILE-REVALIDATE / CDN-EDGE / etc. Drafting CC discovers operative cache values from primary source.
- **Dedicated auth/session flow §** — login, token refresh, session expiry, logout, multi-tenancy boundary.
  - **Multi-tenancy boundary: N/A — EE is single-user handicapping system.** Documented explicitly per BIBLE_STRUCTURE_SPEC v6 § 5.2 empty-section rule.
- **Dedicated cache/state-management §** — Redux / Zustand / React Query / Context / none — drafting CC discovers via Domain G substrate verification.

### Q6: Substrate authorization domains for drafting CC — RATIFIED eight-domain authorization

A-G primary substrate; H locked-bible read-only.

- **Domain A:** Backend route handler source files (per Architecture Overview § 3.5: API Gateway v2 integrations route to `equine-inference` Lambda; route declarations live at `backend/lambdas/inference/handler.py` HTTP-path dispatcher per § 3.1 row + the 25-action admin dispatch in `backend/lambdas/ingestion/handler.py` for INACTIVE-Lambda admin surface coverage).
- **Domain B:** Backend request/response schema definitions (Pydantic / Marshmallow / TS / OpenAPI — primary source TBD by CC V1).
- **Domain C:** Backend auth middleware / decorators / session machinery (TBD by CC V1).
- **Domain D:** Frontend component source files within the single React SPA tree. Path TBD by CC V1 substrate verification (likely globs: `frontend/**`, `web/**`, `app/**`, `client/**`, `ui/**` — CC V1 must verify exact path before authorship).
- **Domain E:** Frontend API client modules — `fetch` / `axios` / `useQuery` / `useMutation` / SDK wrappers within the SPA tree.
- **Domain F:** Frontend routing config — likely React Router (not Next.js file-system routing per Architecture Overview FE substrate read finding); CC V1 verifies.
- **Domain G:** Frontend state-management config — store definitions / query client config / context providers within the SPA tree.
- **Domain H:** Six locked Phase 1 bibles (read-only, for cross-reference declarations only — NOT for feature/data/model/runtime claim sourcing). Lesson 3 expansion enforced: convention identifiers verified at primary source at row-authorship time, not via inheritance from Domain H.

**Drafting-CC discipline:** every row must cite primary source from Domains A-G at row-authorship per Lesson § 4.13. Domain H reads are for declaring cross-references only. Out-of-domain reads = audit finding.

### Q7: Synchronization point structure — RATIFIED

Per Q14 single-CC structure.

- **SP-A1 gate:** TOC + § 1 (Mission / Scope / Boundaries / Cross-Bible Cross-Reference Index) + auth/session flow § skeleton + cache/state-management § skeleton + endpoint table column schema definition + component table column schema definition. Column schemas locked at SP-A1 before § 4.1 / § 5.1 row population begins.
- **SP-A2 gate:** § 4.1 first 3 endpoint rows + § 5.1 first 3 component rows.
  - **Endpoint selection criterion:** span AUTH column value space (one PUBLIC, one SESSION-COOKIE / BEARER-TOKEN, one INTERNAL).
  - **Component selection criterion:** span TYPE column value space if heterogeneous FE confirmed at V1 substrate verification (it is not — see § 4 Q2(a) above; Q2(b) TYPE narrows to REACT-COMPONENT only at lock); fallback criterion: three components from distinct route trees within the SPA.
- **SP-A3 gate:** v1-draft complete = all endpoint rows in § 4 + all component rows in § 5 + reverse index (§ 6) + auth flows (§ 7) + cache/state-management (§ 8) + cross-bible cross-reference declarations (§ 2). Footer + revision history + status header per banked Lesson (lock-CC three-element metadata bundle) added at lock cycle, not at v1-draft.

---

## 5. Upstream substrate read findings — Architecture Overview v3 § 1 + § 3.4 + § 3.5 (FE tree section)

Narrow upstream substrate read executed 2026-05-07 per Tony's authorization (scoped to FE tree section only; Lesson 3 expansion compliant — verify against primary source at spec-authorship rather than guess).

**Findings:**

1. **Single FE tree (the React SPA).** Architecture Overview v3 § 3.4 `equine-frontend` S3 bucket row + § 3.5 API Gateway v2 + § 1 boundary all reference a singular SPA. No Next.js, static HTML, Vue, Jinja, or other framework-rendered surface.
2. **Stack: React.** § 3.4 reads "built React assets"; deploy mechanism `deploy_all.sh` + frontend build → S3 → CloudFront.
3. **FE tree path not specified in Architecture Overview.** Drafting CC V1 substrate verification must locate the FE tree directory at row-authorship before any Domain D / E / F / G read.

**Direct implications captured at Q2 / Q6 ratifications above.**

---

## 6. Drafting CC discipline — Lessons banked at handoff

### Lessons 1-6 from META_PLAN cycles
[banked from prior Phase 0 / Phase 1 cycles; operative]

### AUDIT_METHODOLOGY § 4.1-4.11
[banked from AUDIT_METHODOLOGY v2-patched]

### Lesson § 4.12 — QB does not invoke MCP write tools
QB outputs are chat messages. QB does NOT invoke write_file / edit_file / create_file / move_file / create_directory under any circumstances. All disk writes are mediated by Tony via paste-routing to fresh CC sessions (drafting CC, patch CC, audit CC, lock CC). Operative pending AUDIT_METHODOLOGY patch cycle.

### Lesson § 4.13 — Low-cost substrate verification at row-authorship: execute, don't defer
Drafting CC executes substrate verification at row-authorship rather than deferring to audit cycle. Banked from Phase 1 cohort cycle.

### Lesson 3 expansion — Convention identifiers verified at primary source at spec-authorship
Drafting CC verifies convention identifiers (e.g., type-sig notation, route-handler framework, state-management library name) against primary source code at row-authorship, not against Domain H locked-bible inheritance.

### 8 NEW Lessons banked from Phase 1 Cohort cycle (pending AUDIT_METHODOLOGY meta-cycle promotion)

1. **Inheritance read-scope discipline.** Drafting CC reads only from explicitly-authorized substrate domains; out-of-domain reads = audit finding even if "helpful context."
2. **Intra-document section reference convention.** Cross-references within a bible use `§ X.Y` form; cross-references to other bibles use `bible_name:X.Y` form per BIBLE_STRUCTURE_SPEC v6 convention.
3. **Composite-row treatment for orphan classes.** Orphan rows (e.g., F-81 ORPHAN composite in FP) carry explicit classification + provenance + scope-statement for audit traceability.
4. **Lock-CC three-element metadata bundle.** Lock cycle adds: header status update + revision history entry + footer metadata. All three at lock, not at v1-draft.
5. **Locked bibles preserve drafting-time historical context.** Lock cycle does NOT retroactively rewrite drafting-time content to reflect post-lock state; revision history captures evolution.
6. **Drafting-CC metadata-bundle initialization mandate.** Drafting CC initializes header / revision history / footer skeleton at v1-draft; lock CC populates final values.
7. **QB paste-verbatim discipline.** When QB pastes substrate content (line citations, file contents, prior-cycle output) into new chat output, paste verbatim — not summarized, not partial, not substantively-extracted-only. Surfaced at PHASE_5_BACKLOG.md reconciliation in prior cycle.
8. **Lesson § 4.13** (low-cost substrate verification at row-authorship — see above) is itself the eighth banked lesson.

---

## 7. Self-audit checks (Option 1, 9 checks across 3 clusters)

**Cluster A — Substrate verification:**
1. Every row cites primary source from authorized Domain at row-authorship.
2. No claims sourced from Domain H locked-bible inheritance for substantive content (only for cross-reference declarations).
3. Convention identifiers verified at primary source per Lesson 3 expansion.

**Cluster B — Content verification:**
4. Forward index (`CONSUMED_BY`) and reverse index (`CONSUMES`) bidirectionally consistent.
5. Every `CONSUMED_BY` component identifier appears as a row in § 5.1; every `CONSUMES` endpoint identifier appears as a row in § 4.1.
6. Empty sections documented explicitly per BIBLE_STRUCTURE_SPEC v6 § 5.2 (e.g., multi-tenancy boundary = N/A documented, not omitted).

**Cluster C — Workflow verification:**
7. SP-A1 column schemas locked before SP-A2 row population begins.
8. SP-A2 selection criteria honored (AUTH value space spanning + component-tree distribution).
9. Lock-CC three-element metadata bundle added at lock cycle, not at v1-draft.

---

## 8. PHASE_5_BACKLOG.md state

24 entries (Phase 5.3.1 through 5.3.24); dual-vocabulary header reconciled. Drafting CC may surface candidate Phase 5 items during V1 substrate verification (e.g., DEPRECATED endpoints not yet ratified for retirement; INTERNAL-ONLY endpoints whose disposition is pending); QB synthesizes and surfaces to Tony for ratification before any PHASE_5_BACKLOG addition.

---

## 9. CC role authorization scope for THIS handoff document

The CC session that writes THIS file to disk has **mechanical paste authorization only**:
- Single-file write: `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/QB_HANDOFF_API_FRONTEND_BIBLE_DRAFTING.md`.
- Verbatim paste: no editing, summarizing, restructuring, or "improvement" of QB content.
- No substrate verification, no audit work, no other disk operations.
- If file already exists: error to QB; do NOT overwrite without QB authorization.

This authorization scope is distinct from drafting CC scope (which has Domain A-G primary substrate read + bible authoring write authorization on `api_frontend_bible.md`). Drafting CC paste-prompt is authored separately after drafting spec lock.

---

## 10. Drafting workflow forward path (this cycle)

1. ✅ QB authors handoff content (this document) as chat output.
2. ✅ QB authors spec-write CC paste-prompt for handoff.
3. → Tony pastes spec-write prompt to fresh CC; CC writes this handoff to disk.
4. → QB authors drafting spec content as chat output (`QB_DRAFTING_SPEC_API_FRONTEND_BIBLE.md`).
5. → QB authors spec-write CC paste-prompt for drafting spec.
6. → Tony pastes; CC writes drafting spec to disk.
7. → QB authors drafting CC paste-prompt; Tony pastes; drafting CC drafts `api_frontend_bible.md` v1 with SP-A1 / SP-A2 / SP-A3 synchronization.
8. → Audit-CC paste-prompt; Tony pastes; audit-CC adversarial review.
9. → QB synthesizes findings, surfaces decisions to Tony, iterates to lock.
10. → Lock-CC paste-prompt with three-element metadata bundle scope.
11. → Phase 1 complete: 7 of 7 deliverables LOCKED.

---

End of handoff content.
