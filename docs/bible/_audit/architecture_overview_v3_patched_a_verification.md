# architecture_overview v3-patched-a — Companion Verification Log

**Document:** architecture_overview_v3_patched_a_verification
**Phase:** 1 (Bible) — companion log for deliverable 1 of 7 (UPSTREAM-CORRECTION patch cycle)
**Companion bible:** `architecture_overview.md` (v3-patched-a; Phase 1 deliverable 1 of 7)
**Status:** LOCKED v3-patched-a (2026-05-08) — companion log for Phase 1 deliverable 1 of 7 v3-patched-a LOCKED; UC-1 UPSTREAM-CORRECTION close from `_audit/api_frontend_bible_v1_verification.md` V1-14
**Author:** UC-1 patch CC (surgical write authorization on § 3.1 equine-inference row + revision history + header per Tony-ratified UC-1 dispatch)
**Date:** 2026-05-08
**Tier:** 1 per META_PLAN v9 § 4.5 (live AWS state authoritative for "what infrastructure exists right now"; UC-1 patch substrate is Tier 1 `aws apigatewayv2 get-routes` + `get-integrations` output verified at patch time)

**Anchored on:** META_PLAN v9 (LOCKED 2026-05-05) + BIBLE_STRUCTURE_SPEC v6 (LOCKED 2026-05-05) + AUDIT_METHODOLOGY v2-patched (LOCKED 2026-05-05) + Architecture Overview v3 (LOCKED 2026-05-05; v3 lock-state body content + v3 verification log preserved verbatim per banked Lesson 5) + API & Frontend Bible v1 (LOCKED 2026-05-08; V1-14 substrate evidence triggering UC-1) + companion `_audit/api_frontend_bible_v1_verification.md` V1-LOCKED 2026-05-08.

**UC-1 origin:** API & Frontend Bible v1 verification log V1-14 (Tier 1 AWS state per `aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100` + `aws apigatewayv2 get-integrations`) PARTIAL conclusion identifying that 17 of the routes claimed at `architecture_overview:3.1` equine-inference Role text actually integrate with `equine-wr-inference` (`pxq2zgg`), NOT `equine-inference` (`g01nwrl`). UC-1 ratified MATERIAL severity per TRIAGE_QUEUE_SPEC v1 at API & Frontend Bible audit-cycle synthesis; sequenced post-API-Frontend-Bible-v1-lock as separate cycle per Tony Decision 1 sequencing ratification.

**Patch scope:** SURGICAL per Q1 Option A ratification — single row in § 3.1 (equine-inference Role + Cross-reference cells) + revision history append + header Status update. § 3.1 introductory prose ("5 Active + 3 Inactive" decomposition) preserved unless substrate refutes; PATCH ACTION 1 substrate re-verification confirms 5 Active + 3 Inactive count holds (equine-inference remains Active; the 4 other Active Lambdas + 3 Inactive Lambdas remain unchanged in role).

**Cross-bible cross-reference freeze:** ACTIVE since FP v1 lock per Phase 1 cohort Handoff § 6.1; UC-1 lifts freeze surgically for the equine-inference row only; freeze re-locks at v3-patched-a lock.

**Companion-log requirement:** per META_PLAN v9 § 6.5 (hard rule, not optional). v3 lock-state companion log at `_audit/architecture_overview_v3_verification.md` is preserved verbatim per banked Lesson 5; this NEW log captures only the v3 → v3-patched-a delta per surgical-cosmetic-patch convention precedent (cf. `database_schema_bible_v1_verification.md` post-patch entries; `data_pipeline_bible_v1_verification.md` post-patch entries).

---

## Section A — V1-N entries (UC-1 patch cycle substrate)

### V1-1: Substrate re-verification at patch time — Tier 1 AWS state confirms V1-14

**Claim source:** UC-1 dispatch Tony-ratified at API & Frontend Bible v1 audit-cycle synthesis; substrate evidence is `_audit/api_frontend_bible_v1_verification.md` V1-14 PARTIAL conclusion (Tier 1 AWS state 2026-05-07).

**Substrate domain:** Tier 1 (live AWS state per META_PLAN v9 § 4.5) — `aws apigatewayv2 get-routes` + `aws apigatewayv2 get-integrations` against API ID `gb5qlfy10h`.

**Verification method:**

```
$ aws apigatewayv2 get-routes --api-id gb5qlfy10h --max-results 100 --output json | jq -r '.Items[] | "\(.RouteKey)\t\(.Target)"' | sort
$ aws apigatewayv2 get-integrations --api-id gb5qlfy10h --max-results 100 --output json | jq -r '.Items[] | "\(.IntegrationId)\t\(.IntegrationUri // "N/A")"' | sort
```

**Verbatim output (1) — route → integration target mapping at patch time (2026-05-08):**

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

**Verbatim output (2) — integration ID → Lambda ARN mapping at patch time (2026-05-08):**

```
5e87ugh	arn:aws:lambda:us-east-1:584812014683:function:equine-pl-inference
g01nwrl	arn:aws:lambda:us-east-1:584812014683:function:equine-inference
pvjqh24	arn:aws:lambda:us-east-1:584812014683:function:equine-ls-inference
pxq2zgg	arn:aws:lambda:us-east-1:584812014683:function:equine-wr-inference
```

**Conclusion:** CONFIRMED V1-14. Substrate at patch time (2026-05-08) matches `_audit/api_frontend_bible_v1_verification.md` V1-14 substrate (2026-05-07) byte-for-byte: same 41 routes, same 4 integration IDs, same Lambda ARN mappings. No drift between V1-14 substrate authoring and UC-1 patch authoring.

Per Lesson § 4.13 (substrate verification at patch-authorship — execute, don't defer): substrate is re-verified at patch time, NOT inheritance from V1-14 alone. UC-1 dispatch foundation confirmed.

**Substrate-correct equine-inference (`g01nwrl`) integration set — 7 routes (5 GET + 1 POST + 1 regex-matched-cards):**

1. GET `/cards/{date}/{track_code}` (regex-matched route — `/cards/...` pattern; per V1-18 + V1-2 substrate in api_frontend_bible_v1_verification.md confirms inference Lambda regex-handles this path)
2. GET `/predictions/run` (legacy)
3. GET `/predictions/today` (legacy)
4. GET `/predictions/value` (legacy)
5. GET `/predictions/{date}` (legacy)
6. GET `/predictions/{date}/{track_code}/{race_number}` (legacy)
7. POST `/predictions/run` (legacy)

5 of 7 are candidate-DEPRECATED legacy `/predictions/*` GET routes per `api_frontend_bible:10.4` (FE client.ts substrate at V1-19 + V1-22: zero direct consumers of legacy `/predictions/*`; FE uses per-pipeline `/wr/predictions/*` paths via `runWRPredictions` / `getWRValuePlays` legacy aliases at client.ts:114-115). 1 is POST `/predictions/run` (legacy; no FE consumer). 1 is `/cards/{date}/{track_code}` (no FE consumer per EP-004 = `[]`).

The 17 routes claimed at v3 lock-state Role text as integrating with equine-inference (`/health`, `/dashboard/metrics`, `/races/today`, `/races/available-dates`, `/races/<id>/detail`, race-card/horse-pp/unified/pred-date/race-date paths) actually integrate with `equine-wr-inference` (`pxq2zgg`) per Tier 1 substrate. v3 lock-state Role text claim REFUTED for those 17 routes; CONFIRMED for the 7 substrate-correct routes.

---

### V1-2: Substrate-correct decomposition for § 3.1 equine-inference row content

**Claim source:** UC-1 patch scope — substrate-correct Role text + Cross-reference cell for the equine-inference row, derived from V1-1 above.

**Substrate domain:** Tier 1 (V1-1 above) + Tier 4 working-tree code (api_frontend_bible_v1_verification.md V1-2 inference handler.py:1-200 dispatch chain + V1-18 re-cite confirming 7 routes dispatch from inference Lambda).

**Verification method:** Synthesis from V1-1 substrate + cross-reference inheritance from `_audit/api_frontend_bible_v1_verification.md` V1-2 + V1-18 (Tier 4 working-tree code per V1-2 verbatim grep on `backend/lambdas/inference/handler.py`).

**Substrate-correct Role text decomposition:**

- **HTTP-path-based dispatch surface at lock:** 7 API Gateway integrations (5 GET legacy `/predictions/*` + 1 POST `/predictions/run` + 1 GET `/cards/{date}/{track_code}`).
- **Legacy `/predictions/*` deprecation surface:** 5 GET legacy routes are candidate-DEPRECATED per `api_frontend_bible:10.4`; FE client.ts uses per-pipeline `/wr/predictions/*` paths via legacy aliases (zero direct FE consumers of legacy /predictions/* per V1-19 + V1-22 substrate).
- **Per-pipeline narrowing:** dashboard / races / per-pipeline WR / PL / LS API surface integrates with the 3 per-pipeline inference Lambdas (`equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference`) at lock — NOT this Lambda; per Tier 1 V1-1 substrate.
- **Bug-#15-class parallel-implementation drift surface:** parallel HTTP-path dispatcher pattern between `backend/lambdas/inference/handler.py` and `backend/lambdas/wr-inference/handler.py` (+ pl-inference + ls-inference) creates 4 parallel implementations — first noted as drift surface in V1-14 PARTIAL conclusion.
- **EventBridge-source / batch-source code paths:** Tier 4 working-tree code at `backend/lambdas/inference/handler.py` lines 55 (`event['source'] == 'aws.events'`) + 64 (`event['source'] == 'batch'`) routes both to `run_daily_predictions(date.today())`. These code paths are dormant at lock because the only EventBridge rule originally targeting equine-inference (`equine-inference-daily`, DISABLED with zero current targets per § 3.6) does not fire.
- **No admin-action dispatch:** equine-inference does NOT handle action-based admin dispatch (that surface is hosted on `equine-ingestion` per § 3.1 row + § 6 Currently Open).

**Substrate-correct Cross-reference cell decomposition:**

- v3 lock-state Cross-reference cells: `data_pipeline_bible:4.1`, `api_frontend_bible:3.3`.
- Substrate-grounded re-evaluation:
  - `data_pipeline_bible:4.1` (per-flow data movement; daily inference flows): the daily inference flows are now performed by `equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference` — NOT this Lambda. equine-inference's narrowed role (legacy /predictions/* + /cards/{date}/{track_code}) is not a "daily inference flow" per Data Pipeline Bible structure. **Cross-reference REMOVED** as no longer substrate-grounded for this row.
  - `api_frontend_bible:3.3` (admin-action surface impact): equine-inference is NOT an admin-action Lambda (admin-action surface hosted on equine-ingestion). § 3.3 in api_frontend_bible canonically homes the admin-action surface impact narrative for the INACTIVE-equine-ingestion Lambda. **Cross-reference REMOVED** as substrate-incorrect for this row.
  - `api_frontend_bible:4.1` (per-route detail): the 7 inference-integrated routes (EP-004 `/cards/{date}/{track_code}` + EP-023..EP-028 legacy `/predictions/*`) are documented in api_frontend_bible:4.1 endpoint inventory. **Cross-reference ADDED** as substrate-grounded.
  - `api_frontend_bible:10.4` (legacy `/predictions/*` candidate-DEPRECATED Currently Open surfacing): 5 of the 7 routes are candidate-DEPRECATED per § 10.4 surfacing. **Cross-reference ADDED** as substrate-grounded.

Substrate-correct Cross-reference cell at v3-patched-a: `api_frontend_bible:4.1`, `api_frontend_bible:10.4`.

**Conclusion:** CONFIRMED — Role + Cross-reference cells substrate-correct decomposition complete. PATCH ACTION 3 applies these cell-level edits.

---

### V1-3: Surgical row amendment applied — verbatim before/after

**Claim source:** PATCH ACTION 3 surgical amendment to `architecture_overview.md` § 3.1 equine-inference row.

**Substrate domain:** X (patch target — architecture_overview.md § 3.1 row).

**Verification method:** Direct edit via Edit tool on `architecture_overview.md`; before/after captured verbatim below.

**Verbatim BEFORE (v3 lock-state row content; line 69 of v3 lock-state file):**

```
| `equine-inference` | 1024 | 300 | HTTP-path-based dispatcher for the dashboard + prediction-trigger API surface (`/health`, `/dashboard/metrics`, `/races/today`, `/races/available-dates`, `/races/<id>/detail`, `/predictions/run`, `/predictions/value`, `/predictions/today`, race-card/horse-pp/unified/pred-date/race-date paths — per `backend/lambdas/inference/handler.py` lines 51-180+); also handles EventBridge-source invocation via `event['source'] == 'aws.events'` (line 55) + ingestion-batch-source invocation via `event['source'] == 'batch'` (line 64), both routing to `run_daily_predictions(date.today())`. Does NOT handle action-based admin dispatch — see `equine-ingestion` row below. | `data_pipeline_bible:4.1`, `api_frontend_bible:3.3` |
```

**Verbatim AFTER (v3-patched-a row content; substrate-correct per V1-1 + V1-2):**

```
| `equine-inference` | 1024 | 300 | HTTP-path-based dispatcher for 7 legacy / fallback API Gateway integrations at lock: 5 GET legacy `/predictions/*` (`/predictions/run`, `/predictions/today`, `/predictions/value`, `/predictions/{date}`, `/predictions/{date}/{track_code}/{race_number}`) + 1 POST `/predictions/run` + 1 GET `/cards/{date}/{track_code}` — per `backend/lambdas/inference/handler.py` (parallel HTTP-path dispatcher pattern with the 3 per-pipeline inference Lambdas; Bug-#15-class parallel-implementation drift surface). The 5 GET legacy `/predictions/*` routes are candidate-DEPRECATED per `api_frontend_bible:10.4` (FE client.ts uses per-pipeline `/wr/predictions/*` paths via legacy aliases; zero direct FE consumers of legacy routes per V1-19 + V1-22 substrate of `_audit/api_frontend_bible_v1_verification.md`). The dashboard / races / per-pipeline WR / PL / LS API surface integrates with `equine-wr-inference` / `equine-pl-inference` / `equine-ls-inference` at lock — NOT this Lambda — per `aws apigatewayv2 get-integrations --api-id gb5qlfy10h` Tier 1 substrate (verified at v3-patched-a 2026-05-08 per companion log V1-1; matches `api_frontend_bible_v1_verification.md` V1-14 substrate 2026-05-07). Lambda also contains EventBridge-source invocation handler via `event['source'] == 'aws.events'` (line 55) + ingestion-batch-source invocation via `event['source'] == 'batch'` (line 64) routing to `run_daily_predictions(date.today())`; these code paths are dormant at lock because the only EventBridge rule originally targeting equine-inference (`equine-inference-daily`, DISABLED with zero current targets per § 3.6) does not fire. Does NOT handle action-based admin dispatch — see `equine-ingestion` row below. | `api_frontend_bible:4.1`, `api_frontend_bible:10.4` |
```

**Verbatim grep verification post-edit:**

```
$ grep -nE "^\| \`equine-inference\` \|" /home/strakajagr/projects/equine-equalizer/docs/bible/architecture_overview.md
69:| `equine-inference` | 1024 | 300 | HTTP-path-based dispatcher for 7 legacy / fallback API Gateway integrations at lock: ...
```

(Line number preserved at 69; row position in § 3.1 Active Lambda table preserved; other 4 Active rows + 3 Inactive rows preserved verbatim.)

**Conclusion:** CONFIRMED — surgical amendment applied to equine-inference row. Other rows in § 3.1 unchanged. § 3.1 introductory prose ("5 Active + 3 Inactive") unchanged (decomposition still substrate-correct: equine-inference remains Active; the other 4 Active + 3 Inactive Lambdas unchanged in role per Tier 1 substrate). § 3.1 trailing prose (anomaly note + temporal scoping note) unchanged. UC-1 surgical scope per Q1 Option A honored.

---

## Section B — Cross-bible cross-reference freeze status

**ACTIVE since FP v1 lock per Phase 1 cohort Handoff § 6.1.** UC-1 is the SOLE freeze re-open path per cohort Handoff § 7. UC-1 lifts freeze surgically for the equine-inference row only (Q1 Option A scope); freeze re-locks at v3-patched-a lock.

No other locked bible touched by this patch cycle. `api_frontend_bible.md` v1 LOCKED 2026-05-08 + companion verification log V1-LOCKED 2026-05-08 are read as substrate evidence (Domain V) only — no writes.

---

## Section C — Conditional downstream determination

Per Tony Decision 1 sequencing ratification at API & Frontend Bible v1 cycle close-out: API & Frontend Bible v1 → v1-patched-a is conditionally triggered IF v3-patched-a alters cross-references that API & Frontend Bible cites.

**Determination at v3-patched-a:**

- v3-patched-a Cross-reference cells changed: `data_pipeline_bible:4.1`, `api_frontend_bible:3.3` REMOVED; `api_frontend_bible:4.1`, `api_frontend_bible:10.4` ADDED.
- API & Frontend Bible v1 cites `architecture_overview:3.1` at multiple loci (e.g., row CROSS_REFERENCES columns; § 1.3 cross-reference index). All cites resolve to § 3.1 entirely — none of them cite "the equine-inference row's Cross-reference cell content" specifically. Cross-references RESOLVE consistently regardless of v3-patched-a row content delta.
- Net Gate 2 trigger determination: NEGATIVE — no API & Frontend Bible cross-reference is invalidated by v3-patched-a delta. Conditional downstream API & Frontend Bible v1-patched-a is NOT triggered by this UC-1 patch.
- Tony / QB synthesis tier may overrule this determination if substrate considerations not captured here surface at audit.

**Section C disposition:** Conditional Gate 2 NEGATIVE. API & Frontend Bible v1 lock state preserved.

---

## Section D — Banked methodology lessons (this cycle originates patterns; promotion to AUDIT_METHODOLOGY meta-cycle queue)

UC-1 is the FIRST UPSTREAM-CORRECTION cycle in the Phase 1 cohort. Patterns banked from this cycle (queued for AUDIT_METHODOLOGY meta-cycle promotion alongside the 17-item queue from API & Frontend Bible cycle close-out):

- **F.4 round-trip pattern explicit instantiation.** UC-1 instantiates the F.4 round-trip pattern (cross-bible substrate finding at downstream-bible verification → UPSTREAM-CORRECTION cycle on upstream bible → conditional downstream re-patch IF upstream patch invalidates downstream cross-references). Pattern precedent: F.4 cross-bible round-trip in Data Pipeline Bible v1-patched-a → Database & Schema Bible v1-patched-d2 → Data Pipeline Bible v1-patched-c. UC-1 is the second instantiation; pattern is now generalizable.
- **Q5 UC-cycle audit-scope methodology lesson.** UC-1 ratified Q5 Option C: QB-audit at synthesis tier rather than fresh audit-CC session. Justification: UC-cycle scope is surgical (single row + companion log); fresh audit-CC overhead disproportionate to scope. Pattern: UC-cycle audit scope ≠ initial-bible audit scope; lighter audit tier appropriate when patch scope is single-locus + substrate-grounded.
- **Q3 reference-drift Self-Audit Check candidate.** UC-1 surfaces a class of finding: "locked-bible factual claim refuted by Tier 1 / 2 / 3 substrate during downstream bible verification." Self-Audit Check candidate: "every Tier 4 working-tree-code claim in a locked bible should be cross-checked against Tier 1 live state at lock authorship time, especially for claims that span multiple Lambdas with parallel implementations (Bug-#15-class drift surface)." Banked for AUDIT_METHODOLOGY meta-cycle promotion.

These lessons are banked, NOT applied retroactively to v3 lock-state body content (per banked Lesson 5: locked bibles preserve drafting-time historical context).

---

## Section E — Self-audit (lock readiness)

Per AUDIT_METHODOLOGY v2-patched § 5.5 pattern-completion check + meta-plan v9 § 6.1 methodology-interpolation rule:

- **Net new methodology constructs introduced in v3-patched-a draft: ZERO.** UC-1 patch operations are: (a) row-cell content amendment per Tier 1 substrate; (b) revision history append per cohort precedent; (c) header Status field update per cohort precedent; (d) companion verification log creation per META_PLAN v9 § 6.5. No new conventions, no new vocabulary, no new section types.
- **Pattern-completion check trivially satisfied.** § 3.1 row-table format preserved (5 Active + 3 Inactive table structure unchanged); § 5.1 + § 5.2 numeric IDs preserved; § 8 W.N format preserved (no entries at v3-patched-a lock — same as v3 lock-state); cross-reference vocabulary unchanged (still `bible_name:section.subsection` per BIBLE_STRUCTURE_SPEC v6).
- **Verbatim-paste discipline (Lesson § 4.10).** V1-1 entry contains verbatim raw `aws apigatewayv2 get-routes` + `get-integrations` output (41 routes + 4 integration mappings); V1-3 entry contains verbatim before/after row content. No summarization.
- **Substrate verification at patch-authorship (Lesson § 4.13).** PATCH ACTION 1 substrate re-verification at patch time confirms V1-14 (no inheritance-only reliance).
- **Banked Lesson 5 (locked bibles preserve drafting-time historical context).** v3 lock-state body content (sections OUTSIDE the surgical UC-1 patch scope) preserved verbatim. v3 lock-state companion verification log at `_audit/architecture_overview_v3_verification.md` preserved verbatim — this NEW log captures only v3 → v3-patched-a delta.

Pattern-completion check **PASS**. Net new methodology constructs ZERO. Substrate-grounded surgical patch.

---

## Section F — FRAMEWORK_GAP / SPEC_GAP markers

UC-1 patch CC surfaces ZERO FRAMEWORK_GAP markers + ZERO SPEC_GAP markers in v3-patched-a draft. v3 lock-state had zero markers; v3-patched-a adds zero markers.

---

**END v3-patched-a verification log (UC-1 UPSTREAM-CORRECTION patch cycle).** Awaiting QB-audit synthesis per Q5 Option C ratification + Tony confirmation + post-this-lock cycle dispatches.
