# architecture_overview v3 — Verification Log

Companion log to `architecture_overview.md` v3 (DRAFT, 2026-05-05). Tier 3 surgical-cosmetic patch per Path REVISE AND RE-AUDIT (Tony-confirmed Q(a) 2026-05-05). Companion-log requirement is a hard rule per META_PLAN v9 § 6.5 (not optional).

Author: CC. Date: 2026-05-05. Re-verification timestamp: 2026-05-05T20:15Z (single-session re-verification window).

Substrate inheritance: META_PLAN v9 (locked 2026-05-05; companion verification log `_audits/META_PLAN_v9_verification.md`) + BIBLE_STRUCTURE_SPEC v6 (locked 2026-05-05) + Architecture Overview v2 verification log (`_audit/architecture_overview_v2_verification.md`, preserved as-is for audit-trail; Sections A/B/C inherited by reference per surgical-cosmetic-patch convention) + Architecture Overview v2 audit findings (`_audit/architecture_overview_v2_audit.md`, 8 findings: 1 BLOCKER + 2 MATERIAL + 2 MINOR + 3 STYLE).

Per surgical-cosmetic-patch convention (this cycle covers only the changed content): only changed content gets new verification entries. v2 verification log entries (Sections A/B/C with 45 substantive claims) are inherited wholesale for unchanged content; not re-verified during v3.

---

## Section A — META_PLAN v9 inheritance (preserved from v2 verification log)

2 entries inherited unchanged from `_audit/architecture_overview_v2_verification.md` Section A:

- **A.M9-1** — META_PLAN v9 V9-1.D substrate replacement (RDS PostgreSQL standalone). Status: CONFIRMED. v3 inherits cleanly.
- **A.M9-2** — META_PLAN v9 inheritance of 8-Lambda + 13-EventBridge + 41-route + 4-S3 + 3-ECR-named + 5-CDK-image + 5-ECS-family + 3-Secrets counts. Status: CONFIRMED. v3 inherits cleanly.

---

## Section B — Architecture Overview v1 inheritance (preserved from v2 verification log)

23 entries inherited unchanged from `_audit/architecture_overview_v2_verification.md` Section B:

- **B.A1 through B.A11** (11 entries): the 11 v1 Section A claims (8 Lambdas, 13 EventBridge, 41 routes, 5 CDK images, 4 S3 buckets, 3 Secrets, 5 ECS families, Aurora REFUTED preserved, API Gateway ID, SNS topic, ECS cluster). Status: 10 CONFIRMED + 1 REFUTED preserved.
- **B.V1-1 through B.V1-12** (12 entries): the 12 V1-N claims from v1 verification log. Status: CONFIRMED.

---

## Section C — V2-N entries (preserved from v2 verification log)

20 V2-N entries inherited unchanged from `_audit/architecture_overview_v2_verification.md` Section C:

- **V2-1** through **V2-20** — substrate citations for v2's substantive claims (per-Lambda configuration, per-EventBridge-rule target enumeration via Lesson 5, equine-inference handler dispatch, equine-ingestion admin actions, db.py line range, canonical class declarations, dynamic attribute attachment, equine-equibase-acquisition disposition, deliverable numbering, Bug #15 routing, § 5 marker, § 5.1+5.2 lock dates, § 5.2 template form rewrite, § 5.1 FORBIDDEN expansion, § 5.1 substrate provenance update, § 2 widening, § 3.4 model-artifact-layout citation [SUPERSEDED by V3-1 below], § 3.1 temporal-scoping, § 4.3 navigation-paths walked, § 6 arithmetic correction).

V3 surgical patch does not invalidate v2's substantive verifications; v3 only adjusts 8 specific claim sites per V3-N entries below. V2-17 (model-artifact-layout citation) is superseded by V3-1; V2-N entries otherwise unchanged.

---

## Section D — Methodology-interpolation self-check (re-asserted for v3)

Per META_PLAN v9 § 6.1. Drafter audits v3 patch operations for net new methodology constructs:

- **Net new methodology constructs introduced in v3 draft: ZERO.**
- Verified by adversarial reading of v3 patch operations:
  - Op 1 (G1) — cross-reference correction (§ 6.4 → § 6.5). No new construct.
  - Op 2 (G2) — equine-ingestion role description widening to 25 actions + per-action enumeration deferral. Substrate-grounded per audit-CC G2 grep output (25 action handlers); no new construct.
  - Op 3 (G3) — § 2 Runtime context definition adds "scheduling (EventBridge)" 7th category. Substrate-grounded per § 3.6 enumeration; no new construct.
  - Ops 4 + 5 + 6 (G4) — three PHASE_5_BACKLOG.md reference reframes from "see/Pointer/open in" to "pending an explicit ... entry". Substrate-grounded per META_PLAN v9 § 9.9; no new construct.
  - Op 7 (G5) — § 4.1 Prediction row calibration framing sharpens "where applicable" to "bypassed for all production specialists except gonzo_sauce per § 3.4 Bug #15+#24 chain." Substrate-grounded per v2 § 3.4 itself; no new construct.
  - Op 8a (G6) — § 1 BIBLE_INDEX redundancy drop. Editorial change only; no new construct.
  - Op 8b (G7) — § 4.2 cross-reference precision (`:4.2` → `:4.2.1`). Substrate-grounded per BIBLE_STRUCTURE_SPEC v6 § 6.4 § 4.2.1 verified at QB self-audit H1; no new construct.
  - Op 8c (G8) — § 3.6 ENABLED sub-decomposition (4+4+2=10) made explicit. Decomposition discipline per META_PLAN v9 § 6.5 (grandfathered); no new construct.
- **Pattern-completion check trivially satisfied:** no new letter-prefixes; § 5.1 + § 5.2 numeric IDs preserved; § 8 W.N format preserved (no entries at v3 lock); cross-reference vocabulary unchanged.

Grandfathering clause confirmed operative: pre-existing methodology constructs from META_PLAN v9 + BIBLE_STRUCTURE_SPEC v6 are inherited; v3 introduced none.

---

## Section E — Pattern-completion check (re-asserted)

Per AUDIT_METHODOLOGY v2 § 5.5.

- **Letter-prefix exclusivity preserved.** W.N is the only letter-prefix; no § 8 entries at v3 lock; no W.N entries introduced.
- **§ 5 ratified-rule numeric IDs.** § 5.1 + § 5.2 numeric IDs preserved per G-new-1 closure.
- **§ 8 W.N format preserved.** N/A — empty section at v3 lock.
- **Decomposition discipline applied.** v3 Op 8c makes the implicit "10 ENABLED = 4 fire-and-fail + 4 active-Lambda + 2 ECS" sub-decomposition explicit, tightening compliance with META_PLAN v9 § 6.5 verification-log precision rule (broad scope: "when in doubt, decompose"). All other decompositions inherited from v2.
- **G-new-2 inheritance pattern preserved.** § 3.7 "named ECR vs CDK-managed assets repository" distinction preserved; § 3.1 Active vs Inactive preserved; § 3.6 ENABLED vs DISABLED preserved (with new sub-decomposition added per Op 8c).

Pattern-completion check **PASS**.

---

## Section F — FRAMEWORK_GAP / SPEC_GAP markers

Drafter surfaces ZERO FRAMEWORK_GAP markers + ZERO SPEC_GAP markers in v3 draft. v2 had zero markers; v3 adds zero markers.

---

## Section G — v2 audit findings closure verification

8 entries (G1 through G8) — 1 per v2 audit finding. Format per entry: finding ID + severity + one-line summary + v3 patch operation reference + V3-N substrate evidence + closure verification.

### G1: BLOCKER — § 3.4 § 6.4 → § 6.5 cross-reference correction (broken cross-reference)
- v3 patch operation: Operation 1 (§ 3.4 row 2, equine-model-artifacts row, "Role" column).
- v3 substrate evidence: V3-1 verification log entry below.
- Closure verification: bash-grep `grep -n "BIBLE_STRUCTURE_SPEC v6 § 6\." architecture_overview.md` returns line 124 with `BIBLE_STRUCTURE_SPEC v6 § 6.5` (not § 6.4) for the S3 artifact-paths citation; same line carries `per § 6.4 template` for the calibration-mechanics cross-reference (correct since § 6.4 is the ml_layer_architecture_bible.md template). Both cross-references substrate-grounded per QB self-audit H1.
- Closure status: **CLOSED**.

### G2: MATERIAL — § 3.1 equine-ingestion role 25-action surface (undercount of admin-action surface)
- v3 patch operation: Operation 2 (§ 3.1 INACTIVE table, equine-ingestion row, Original role column).
- v3 substrate evidence: V3-2 verification log entry below.
- Closure verification: bash-grep `grep -n "25 action handlers" architecture_overview.md` returns line 79 with the 25-action framing + category enumeration + per-action deferral to `data_pipeline_bible:4.1` + 3-action EventBridge-triggered subset (refresh_angle_stats + 2 default-case dispatches). Substrate-grounded per audit-CC G2 grep output (25 action handlers at lines 25/191/243/318/335/366/380/421/524/542/572/595/616/645/668/705/803/868/1041/1136/1390/1456/1536/1655); category arithmetic per QB self-audit H2: 5 (data acquisition) + 4 (model lifecycle) + 5 (admin/diagnostic) + 7 (data backfills) + 3 (originally-cited admin) + 1 (health) = 25.
- Closure status: **CLOSED**.

### G3: MATERIAL — § 2 Runtime context definition with EventBridge added (internal contradiction with § 3.6)
- v3 patch operation: Operation 3 (§ 2 first definition entry, "Runtime context").
- v3 substrate evidence: V3-3 verification log entry below.
- Closure verification: bash-grep `grep -n "scheduling (EventBridge)" architecture_overview.md` returns line 45 with the new 7th category. Internal consistency confirmed per QB self-audit H3 + H4: § 2 enumerates 9 services × 7 categories matching § 3.1 through § 3.8 enumeration (with § 3.8 holding 2 services: SNS + Secrets Manager). § 3.6 EventBridge now has § 2 representation under "scheduling" category.
- Closure status: **CLOSED**.

### G4: MINOR — META_PLAN v9 § 9.9 violations: PHASE_5_BACKLOG.md references without phase numbers (5 instances closed by patch + 1 pre-existing § 3.7 already-compliant = 6 substantive total)
- v3 patch operations: Operations 4 + 5 + 6 (v3 main spec: § 3.1 Re-activation paragraph + § 6 Currently Open last sentence + § 7 Deprecated last sentence) + Operations 9 + 10 (v3 extension: § 4.3 navigation path Step 3 + § 5.1 CORRECT example block).
- v3 substrate evidence: V3-4 + V3-5 + V3-6 + V3-9 + V3-10 verification log entries below.
- Closure verification: bash-grep `grep -n "PHASE_5_BACKLOG\.md" architecture_overview.md` 2026-05-05 returns 6 substantive instances at § 3.1 Re-activation paragraph + § 3.7 equibase-acquisition row (pre-existing already-compliant from v2 F18 closure) + § 4.3 navigation path Step 3 + § 5.1 CORRECT example + § 6 Currently Open + § 7 Deprecated; all 6 G4-pattern-compliant ("pending an explicit `PHASE_5_BACKLOG.md` entry" form or "pending explicit `PHASE_5_BACKLOG.md` entries" plural form). 5 of 5 patch operations CLOSED ✓; 1 pre-existing already-compliant requires no patch.
- Closure status: **CLOSED**.

### G5: STYLE — § 4.1 Prediction row "calibrated probability where applicable" stale framing
- v3 patch operation: Operation 7 (§ 4.1 Prediction row, Purpose column).
- v3 substrate evidence: V3-7 verification log entry below.
- Closure verification: bash-grep `grep -n "calibrated probability" architecture_overview.md` returns line 214 with the new "bypassed for all production specialists except gonzo_sauce per § 3.4 Bug #15+#24 chain" framing. Substrate-grounded per v2 § 3.4 itself (which states the bypass).
- Closure status: **CLOSED**.

### G6: STYLE — § 1 + § 4.3 redundant restatement of "no separate BIBLE_INDEX.md exists per § 7.5"
- v3 patch operation: Operation 8a (§ 1 paragraph 2).
- v3 substrate evidence: V3-8a verification log entry below.
- Closure verification: bash-grep `grep -n "no separate \`BIBLE_INDEX.md\` exists" architecture_overview.md` returns 1 line (§ 4.3) instead of v2's 2 lines (§ 1 + § 4.3). § 1 now references § 4.3 for the substantive citation without re-asserting the same authority.
- Closure status: **CLOSED**.

### G7: STYLE — § 4.2 cross-reference precision (`ml_layer_architecture_bible:4.2` → `:4.2.1` for WR-pipeline-specific)
- v3 patch operation: Operation 8b (§ 4.2 last sentence of architectural-dissonance paragraph).
- v3 substrate evidence: V3-8b verification log entry below.
- Closure verification: bash-grep `grep -n "ml_layer_architecture_bible:4.2.1" architecture_overview.md` returns line 228 with the tightened cross-reference. Substrate-grounded per QB self-audit H1: BIBLE_STRUCTURE_SPEC v6 § 6.4 template § 4.2 = "Inference pipeline composition" with § 4.2.1 = "WR pipeline (`equine-wr-inference` Lambda → `WRInferenceService`)".
- Closure status: **CLOSED**.

### G8: MINOR — § 3.6 decomposition opportunity (10 ENABLED sub-decomposition explicit)
- v3 patch operation: Operation 8c (§ 3.6 paragraph immediately preceding ENABLED table).
- v3 substrate evidence: V3-8c verification log entry below.
- Closure verification: bash-grep `grep -n "4+4+2=10" architecture_overview.md` returns line 138 with the explicit sub-decomposition: "Of the 10 ENABLED rules: 4 target INACTIVE Lambdas (3 → equine-ingestion ...; 1 → equine-results ...); 4 target Active Lambdas (per-pipeline daily inference); 2 target ECS task families (daily-retrain-full + weekly-retrain-wr). 4+4+2=10." Decomposition discipline per META_PLAN v9 § 6.5 broad-scope rule.
- Closure status: **CLOSED**.

**Section G summary:** 8 of 8 v2 audit findings CLOSED in v3. 1 BLOCKER closed (G1 cross-reference correction). 2 MATERIALs closed (G2 25-action surface; G3 EventBridge category addition). 2 MINORs closed (G4 PHASE_5_BACKLOG reframes; G8 sub-decomposition). 3 STYLEs closed (G5 calibration framing; G6 redundancy drop; G7 cross-ref precision).

---

## Section H — QB self-audit log (Option 1 discipline; reproduced char-exact from drafting spec)

5 entries documenting QB's spec-authorship verifications. Per Option 1 discipline: substrate verifications for v3 prescribed cross-references and definition framing were performed by QB at spec-authorship time; CC reproduces the descriptive log entries (CC does NOT re-run the QB self-audit).

### H1: Cross-reference accuracy (G1 BLOCKER + G7 STYLE)
- Verification: QB direct read of BIBLE_STRUCTURE_SPEC v6 lines 1-810 2026-05-05.
- Result: § 6.5 starts at line 783; § 4.3.2 S3 artifact paths in § 6.5 confirmed; § 4.2.1 WR pipeline in § 6.4 confirmed.
- Outcome: G1 prescribed cross-ref (§ 6.4 → § 6.5) substrate-grounded; G7 prescribed cross-ref (4.2 → 4.2.1) substrate-grounded.

### H2: Count/arithmetic accuracy (G2 MATERIAL)
- Verification: audit-CC grep output adopted (25 action handlers, line numbers enumerated).
- Result: 25 = 5 (data acquisition) + 4 (model lifecycle) + 5 (admin/diagnostic) + 7 (data backfills) + 3 (originally-cited admin) + 1 (health).
- Outcome: G2 prescribed deferral framing substrate-grounded.

### H3: Substrate-grounded reframing (G3 MATERIAL)
- Verification: structural mapping of § 3.1-§ 3.8 to proposed 7-category framing.
- Result: 9 services × 7 categories matching 8 sub-sections (§ 3.8 holds 2 services).
- Outcome: G3 prescribed 7th category "scheduling (EventBridge)" substrate-grounded.

### H4: Definition-framing internal consistency (G3 MATERIAL)
- Verification: H3 mapping check.
- Result: § 2 9-services-7-categories framing consistent with § 3.1-§ 3.8 enumeration.
- Outcome: internal consistency confirmed.

### H5: Synthesis verification
- Verification: N/A — v3 is surgical patch applying audit findings, not synthesizing upstream corrections.
- Outcome: N/A.

### H6: Audit-CC enumeration completeness check (banked 2026-05-05 post-CC-surfacing)
- Verification: when QB inherits count claims from audit-CC findings, QB grep-verifies against disk state at spec-authorship.
- Result: v3 cycle gap surfaced — audit-CC enumerated 4 PHASE_5_BACKLOG.md instances under G4, but disk-state grep returned 6 instances (lines 250 + 297 in addition to the 4 originally enumerated). v3 spec extension closes the gap with Operations 9 + 10.
- Outcome: Check 6 (audit-CC enumeration completeness — QB grep-verifies count claims inherited from audit-CC against disk state at spec-authorship) added to QB self-audit checklist for Database & Schema Bible drafting spec onward.

### H7: Mid-cycle scope extension narrative staleness (Check 7; banked 2026-05-05 post-v3-audit per H1 finding)
- Failure mode: when QB extends a spec mid-cycle (e.g., v3 extension Operations 9 + 10 added post-CC-surfacing), narrative-referencing sections that summarize the original scope (Section G closure entries; main doc revision history; etc.) require explicit update to reflect the extended scope. v3 cycle: Section G G4 closure entry was authored against pre-extension scope ("4 instances" + Ops 4/5/6); post-extension Section H6 + Section I V3-9 + V3-10 reflected new scope, but Section G G4 narrative wasn't updated, creating internal contradiction caught by audit-CC H1.
- Operationalization: when extending a spec mid-cycle, enumerate ALL narrative-referencing sections (verification log Sections G/H/I + main doc revision history + main doc body cross-references) that reference the original scope; update each to reflect extended scope. Don't assume Section H/I update suffices.
- Outcome: Check 7 added to QB self-audit checklist; not promoted to Phase 0 methodology document; future AUDIT_METHODOLOGY cycle codifies.

### H8: Line-shift-resistant citations replace literal line numbers (Check 8; banked 2026-05-05 post-v3-audit per H5 finding)
- Failure mode: literal line-number citations in verification log entries are fragile against any document edit that shifts surrounding lines. v3 cycle: Section G entries cited line numbers (123/78/44/213/227/137) authored against pre-revision-history-bullet-insertion snapshot; v3 patch inserted the revision history bullet at line 14, shifting all subsequent line numbers down by 1. Audit-CC H5 caught the off-by-one drift across 6 entries.
- Operationalization: when prescribing line numbers in verification log entries, prefer line-shift-resistant citations: section anchors (e.g., "§ 3.6 paragraph immediately preceding ENABLED table"), quoted content prefixes (e.g., "the line beginning '4+4+2=10'"), or bash-grep regex patterns (e.g., `grep -n "ml_layer_architecture_bible:4.2.1"`). Literal line numbers acceptable only when tightly scoped to a specific operation's old_str/new_str pair where char-exact matching is required.
- Outcome: Check 8 added to QB self-audit checklist; operative starting Database & Schema Bible drafting spec; not retroactive to existing Architecture Overview citations (which are bumped by H5 fix per Operations 12-17).

---

## Section I — V3-N new entries

10 V3-N entries — 1 per patch operation (8 from v3 spec + 2 from v3 spec extension). Format per entry: target, old text (char-exact match), new text (char-exact replacement), substrate evidence, closure of audit finding.

### V3-1: Operation 1 substrate citation (G1)
- Patch target: `architecture_overview.md` § 3.4 S3 buckets, row 2 (equine-model-artifacts row, "Role" column).
- Old text (char-exact match, removed):
  > `Model registry artifact storage; layout s3://equine-model-artifacts/<family>/<version>.json per BIBLE_STRUCTURE_SPEC v6 § 6.4 (the ml_layer_architecture_bible.md template's § 4.3.2 S3 artifact paths sub-section). Holds training artifacts including calibration sidecars where present.`
- New text (char-exact replacement, present):
  > `Model registry artifact storage; layout s3://equine-model-artifacts/<family>/<version>.json per BIBLE_STRUCTURE_SPEC v6 § 6.5 (the model_evaluation_retraining_bible.md template's § 4.3.2 S3 artifact paths sub-section, within § 4.3 Model artifact version control). Holds training artifacts including calibration sidecars where present (calibration mechanics canonical home is ml_layer_architecture_bible:4.3 per § 6.4 template).`
- Substrate evidence:
  - BIBLE_STRUCTURE_SPEC v6 line 783: `### 6.5 model_evaluation_retraining_bible.md (FF3)` (start of § 6.5).
  - BIBLE_STRUCTURE_SPEC v6 § 6.5 § 4.3.2: `S3 artifact paths (s3://equine-model-artifacts/<family>/<version>.json)` (verified by QB direct read 2026-05-05; line 804).
  - BIBLE_STRUCTURE_SPEC v6 § 6.4 § 4.3 = "Calibration / bypass state" with § 4.3.2 "Calibration sidecars in S3 (gonzo_sauce only)" — distinct content (verified by QB direct read 2026-05-05).
  - v2 audit finding G1 (BLOCKER) closed by replacement.
- Closure of audit finding: G1 (BLOCKER).

### V3-2: Operation 2 substrate citation (G2)
- Patch target: `architecture_overview.md` § 3.1 Lambda inventory and roles, INACTIVE table, equine-ingestion row (Original role column).
- Old text (char-exact match, removed):
  > `Daily Equibase ingestion (PP fetch, race-card fetch). Also hosts the action-based admin dispatch at backend/lambdas/ingestion/handler.py: action == 'refresh_angle_stats' (line 94), action == 'raw_query' (line 595), action == 'set_active_model' (line 645). Because the Lambda is INACTIVE, all three admin actions are currently non-functional.`
- New text (char-exact replacement, present):
  > `Daily Equibase ingestion (PP fetch, race-card fetch) plus an action-based admin dispatch at backend/lambdas/ingestion/handler.py covering 25 action handlers spanning data acquisition (race-card / results / chart / workout fetches), model lifecycle (train / register / activate), admin/diagnostic (raw_query / migrate / db_counts), and data backfills/normalization. Per-action enumeration deferred to data_pipeline_bible:4.1. Because the Lambda is INACTIVE, all 25 manual-invoke action handlers are currently non-functional via the same INACTIVE-Lambda mechanism; 3 actions are also EventBridge-triggered (refresh_angle_stats via equine-angle-stats-nightly plus 2 default-case dispatches via equine-ingestion-daily and equine-fetch-results-nightly) and therefore fire-and-fail per § 3.6 anomaly note.`
- Substrate evidence:
  - audit-CC G2 grep output: 25 action handlers at lines 25/191/243/318/335/366/380/421/524/542/572/595/616/645/668/705/803/868/1041/1136/1390/1456/1536/1655.
  - Action-handler categories: data acquisition (collect_workouts/fetch_results/parse_charts/match_results/test_scrape = 5); model lifecycle (register_model/train_wr_model/train_model/activate_model = 4); admin/diagnostic (migrate/run_admin_sql/deactivate_all/db_counts/query_dates = 5); data backfills/ops (run_inference_batch/dedup_horses/backfill_workouts/compute_speed_figures/normalize_figures/backfill_trip_flags/load_workouts_from_s3 = 7); admin actions originally cited (refresh_angle_stats/raw_query/set_active_model = 3); health (1) — 5+4+5+7+3+1 = 25.
  - v2 audit finding G2 (MATERIAL) closed by deferral.
  - **Substrate sub-verification (added 2026-05-05 per H4 audit finding):** `grep -nE "action = event\.get|if not action|action or|else:" backend/lambdas/ingestion/handler.py` returns: line 20 `action = event.get('action')` (top-level dispatch read); line 197/248/580/1095 `else:` (per-action branch internals, not top-level fall-through). Default-case dispatch behavior at handler top-level: handler reads `action` from event payload at line 20; falls through all 25 `if action == 'X':` branches when `action` is None or unrecognized; reaches the `# ── Normal scheduled ingestion ──` tail-end path at lines 1669-1680, which calls `IngestionService(conn).fetch_daily_entries(date.today())`. The "default-case dispatches via equine-ingestion-daily and equine-fetch-results-nightly" interpretation in v3 § 3.1 corresponds to: both rules invoke equine-ingestion with `Input = None` (no action field); the handler's `event.get('action')` returns None; no `if action == 'X':` branch matches; control flows to the tail-end "Normal scheduled ingestion" daily-entries fetch path. Substrate confirmed: the default-case dispatch IS a real handler path, not CC inference.
- Closure of audit finding: G2 (MATERIAL).

### V3-3: Operation 3 substrate citation (G3)
- Patch target: `architecture_overview.md` § 2 Definitions, first definition entry ("Runtime context").
- Old text (char-exact match, removed):
  > `**Runtime context.** A distinct AWS-resource class in EE's runtime architecture: compute (Lambda, ECS Fargate), data (RDS PostgreSQL, S3), connectivity (API Gateway v2), config/secrets (Secrets Manager), messaging (SNS), image registry (ECR). § 3.1 through § 3.8 enumerate the 8 resource classes. A "canonical" object is one whose shape does not change as it crosses these contexts (per § 4.1).`
- New text (char-exact replacement, present):
  > `**Runtime context.** A distinct AWS-resource class in EE's runtime architecture: compute (Lambda, ECS Fargate), data (RDS PostgreSQL, S3), connectivity (API Gateway v2), scheduling (EventBridge), config/secrets (Secrets Manager), messaging (SNS), image registry (ECR). § 3.1 through § 3.8 enumerate the 9 services across 7 categories (with § 3.8 holding 2 services: SNS + Secrets Manager). A "canonical" object is one whose shape does not change as it crosses these contexts (per § 4.1).`
- Substrate evidence:
  - § 3.1 Lambda + § 3.2 ECS Fargate → compute (2 services).
  - § 3.3 RDS PostgreSQL + § 3.4 S3 → data (2 services).
  - § 3.5 API Gateway v2 → connectivity (1).
  - § 3.6 EventBridge → scheduling (1) ← NEW 7th category.
  - § 3.7 ECR → image registry (1).
  - § 3.8 SNS + Secrets Manager → messaging (1) + config/secrets (1) = 2 services.
  - Total: 9 services × 7 categories matching 8 sub-sections (§ 3.8 holds 2 services); internal consistency confirmed.
  - v2 audit finding G3 (MATERIAL) closed by 7th category addition.
- Closure of audit finding: G3 (MATERIAL).

### V3-4: Operation 4 substrate citation (G4 instance 1 of 3)
- Patch target: `architecture_overview.md` § 3.1 Lambda inventory and roles, paragraph immediately following INACTIVE table.
- Old text (char-exact match, removed):
  > `Re-activation requires a CDK redeploy that re-pushes images and updates Configuration.ImageUri to a still-present hash. Re-activation disposition is Phase 5 work; see PHASE_5_BACKLOG.md.`
- New text (char-exact replacement, present):
  > `Re-activation requires a CDK redeploy that re-pushes images and updates Configuration.ImageUri to a still-present hash. Re-activation disposition is Phase 5 work pending an explicit PHASE_5_BACKLOG.md entry.`
- Substrate evidence: META_PLAN v9 § 9.9 (cite-specific-phase-number rule) + v2 § 3.7 pre-existing "pending an explicit PHASE_5_BACKLOG.md entry" framing as canonical pattern.
- Closure of audit finding: G4 (MINOR; instance 1 of 3).

### V3-5: Operation 5 substrate citation (G4 instance 2 of 3)
- Patch target: `architecture_overview.md` § 6 Currently Open, last sentence of fire-and-fail anomaly bullet.
- Old text (char-exact match, removed):
  > `Pointer: PHASE_5_BACKLOG.md re-activation entry. Canonical-home for the cross-runtime invariant: this bible (per § 5.1 + § 5.2 ratifications); cross-references from data_pipeline_bible:4.1 (downstream pipeline impact) and api_frontend_bible:3.3 (admin-action surface impact).`
- New text (char-exact replacement, present):
  > `Pointer: re-activation pending an explicit PHASE_5_BACKLOG.md entry. Canonical-home for the cross-runtime invariant: this bible (per § 5.1 + § 5.2 ratifications); cross-references from data_pipeline_bible:4.1 (downstream pipeline impact) and api_frontend_bible:3.3 (admin-action surface impact).`
- Substrate evidence: same as V3-4.
- Closure of audit finding: G4 (MINOR; instance 2 of 3).

### V3-6: Operation 6 substrate citation (G4 instance 3 of 3)
- Patch target: `architecture_overview.md` § 7 Deprecated.
- Old text (char-exact match, removed):
  > `Conditional triggers (Lambda slated for kill in Phase 5; ECR repository superseded; the equine-equibase-acquisition ECR repository with zero production code readers per § 3.7) do not currently fire — none of these items have been ratified as deprecated; their dispositions are open in PHASE_5_BACKLOG.md.`
- New text (char-exact replacement, present):
  > `Conditional triggers (Lambda slated for kill in Phase 5; ECR repository superseded; the equine-equibase-acquisition ECR repository with zero production code readers per § 3.7) do not currently fire — none of these items have been ratified as deprecated; their dispositions are pending explicit PHASE_5_BACKLOG.md entries.`
- Substrate evidence: same as V3-4.
- Closure of audit finding: G4 (MINOR; instance 3 of 3).

### V3-7: Operation 7 substrate citation (G5)
- Patch target: `architecture_overview.md` § 4.1 Race / Entry / PastPerformance / Workout / Result / Prediction, Prediction row Purpose column.
- Old text (char-exact match, removed):
  > `The base prediction shape (entry-level model output: probability, ranking-score, calibrated probability where applicable). Used by the WR pipeline directly + augmented via dynamic attribute attachment per § 4.2.`
- New text (char-exact replacement, present):
  > `The base prediction shape (entry-level model output: probability, ranking-score, calibrated probability — bypassed for all production specialists except gonzo_sauce per § 3.4 Bug #15+#24 chain). Used by the WR pipeline directly + augmented via dynamic attribute attachment per § 4.2.`
- Substrate evidence: v2 § 3.4 itself (which states `post-EE Bug #15 + Bug #24, all production specialists currently bypass calibration except gonzo_sauce`).
- Closure of audit finding: G5 (STYLE).

### V3-8a: Operation 8a substrate citation (G6)
- Patch target: `architecture_overview.md` § 1 Scope of this bible, paragraph 2.
- Old text (char-exact match, removed):
  > `Architecture Overview is the **bible-corpus-level entry point** and **navigation hub**. Per BIBLE_STRUCTURE_SPEC v6 § 7.5, no separate BIBLE_INDEX.md exists; § 4.3 below serves the index function for the entire 7-document bible corpus. By design, every other Phase 1 bible's Scope section cross-references back to this document for system topology; this bible cross-references outward for per-domain depth.`
- New text (char-exact replacement, present):
  > `Architecture Overview is the **bible-corpus-level entry point** and **navigation hub**. § 4.3 below serves the index function for the entire 7-document bible corpus (per BIBLE_STRUCTURE_SPEC v6 § 7.5; the substantive citation is in § 4.3 itself). By design, every other Phase 1 bible's Scope section cross-references back to this document for system topology; this bible cross-references outward for per-domain depth.`
- Substrate evidence: editorial change only; v2 audit G6 surfaced redundant restatement of "no separate BIBLE_INDEX.md exists per § 7.5" across § 1 + § 4.3. v3 keeps the substantive citation in § 4.3 and references it from § 1 without repeating.
- Closure of audit finding: G6 (STYLE).

### V3-8b: Operation 8b substrate citation (G7)
- Patch target: `architecture_overview.md` § 4.2 Per-pipeline prediction shapes, last sentence of architectural-dissonance paragraph.
- Old text (char-exact match, removed):
  > `Canonicalizing the dynamically-attached WR enrichment fields into the dataclass (or extracting a WRPrediction subclass) is candidate Phase 5 work; substantive disposition belongs to ml_layer_architecture_bible:4.2 once that drafts.`
- New text (char-exact replacement, present):
  > `Canonicalizing the dynamically-attached WR enrichment fields into the dataclass (or extracting a WRPrediction subclass) is candidate Phase 5 work; substantive disposition belongs to ml_layer_architecture_bible:4.2.1 (WR pipeline sub-section) once that drafts.`
- Substrate evidence: BIBLE_STRUCTURE_SPEC v6 § 6.4 template § 4.2 = "Inference pipeline composition" with § 4.2.1 "WR pipeline (equine-wr-inference Lambda → WRInferenceService)" (verified by QB direct read 2026-05-05).
- Closure of audit finding: G7 (STYLE).

### V3-8c: Operation 8c substrate citation (G8)
- Patch target: `architecture_overview.md` § 3.6 EventBridge schedule, paragraph immediately preceding ENABLED table.
- Old text (char-exact match, removed):
  > `Decomposed as **10 ENABLED + 3 DISABLED**. Target column populated from aws events list-targets-by-rule --rule <name> per rule; EcsParameters.TaskDefinitionArn extracted for ECS targets.`
- New text (char-exact replacement, present):
  > `Decomposed as **10 ENABLED + 3 DISABLED**. Of the 10 ENABLED rules: 4 target INACTIVE Lambdas (3 → equine-ingestion: ingestion-daily + fetch-results-nightly + angle-stats-nightly; 1 → equine-results: results-daily) — see anomaly note below; 4 target Active Lambdas (per-pipeline daily inference: ls-inference-daily + nyra-workouts-daily + pl-inference-daily + wr-inference-daily); 2 target ECS task families (daily-retrain-full + weekly-retrain-wr). 4+4+2=10. Target column populated from aws events list-targets-by-rule --rule <name> per rule; EcsParameters.TaskDefinitionArn extracted for ECS targets.`
- Substrate evidence: V2-2 verification log entry (per-rule list-targets-by-rule decomposition, inherited from v2). Decomposition discipline per META_PLAN v9 § 6.5 broad-scope rule.
- Closure of audit finding: G8 (MINOR).

### V3-9: Operation 9 substrate citation (G4 extension instance 1 of 2; closes residual G4 surface)
- Patch target: `architecture_overview.md` § 4.3 INDEX (cross-bible navigation), Common navigation paths, "I'm chasing a 'function trying to use deleted image' alert" walked scenario, Step 3.
- Old text (char-exact match, removed):
  > `*Step 3:* file disposition in PHASE_5_BACKLOG.md re-activation entry. Resolved as known fire-and-fail anomaly per § 6.`
- New text (char-exact replacement, present):
  > `*Step 3:* file disposition pending an explicit PHASE_5_BACKLOG.md re-activation entry. Resolved as known fire-and-fail anomaly per § 6.`
- Substrate evidence: META_PLAN v9 § 9.9 (cite-specific-phase-number rule). v2 audit G4 enumerated 4 instances; v3 patch verification (post-CC-surfacing) identified this as a 5th instance missed by v2 audit. Ratified by pattern under Tony's Q(c) 2026-05-05.
- Closure of audit finding: G4 (MINOR; instance 4 of 5 — v3 spec extension; closes residual G4 surface enumeration gap).

### V3-10: Operation 10 substrate citation (G4 extension instance 2 of 2; CORRECT example § 9.9-compliance preserved)
- Patch target: `architecture_overview.md` § 5.1 Forbidden Pattern, CORRECT code example block (last line).
- Old text (char-exact match, removed):
  > `Re-activation pending Phase 5 (PHASE_5_BACKLOG.md).`
- New text (char-exact replacement, present):
  > `Re-activation pending an explicit PHASE_5_BACKLOG.md entry.`
- Substrate evidence: META_PLAN v9 § 9.9 (cite-specific-phase-number rule) applied to CORRECT example block. Per spec rationale: § 5.1's CORRECT example shows readers what well-formed Lambda-State documentation looks like; if the CORRECT example itself violates § 9.9, readers will copy the violation. Reframing to G4 pattern keeps the CORRECT example § 9.9-compliant. Note: char-exact substantive content matches spec ("Re-activation pending an explicit `PHASE_5_BACKLOG.md` entry."); the CORRECT example block's markdown line-wrap places the line break between "Re-activation" and "pending" rather than between "pending" and "Phase" (as in the original) — visual width of the 5-line code block preserved.
- Closure of audit finding: G4 (MINOR; instance 5 of 5 — v3 spec extension; closes residual G4 surface enumeration gap).

### V3-11: Final-lock surgical patch summary (2026-05-05; covers H1 + H2 + H3 + H4 + H5 audit findings)
- Patch operations: Op 11 (H1 Section G G4 rewrite to reflect 5-of-5-closed-by-patch + 1-pre-existing-already-compliant = 6 substantive total) + Ops 12-17 (H5 6 line-number bumps in Section G G1/G2/G3/G5/G7/G8 closure verifications: 123→124, 78→79, 44→45, 213→214, 227→228, 137→138) + Op 18 (H3 § 3.1 V3-2 cross-reference add: per-category arithmetic 5+4+5+7+3+1=25 made traceable from main doc to verification log) + Ops 19-23 (H2 5 main-doc "at v2 lock" → "at lock" generic-framing replaces at § 4.3 disclaimer + § 5.2 corrected position + § 6 Currently Open header + § 6 body + § 8) + Op 24 (H4 handler default-case dispatch grep + V3-2 substrate sub-citation) + Ops 25-27 (front matter Status DRAFT v3 → LOCKED v3 + Locked → 2026-05-05 + revision history v3 final-lock summary) + Ops 28 (Section H H7 + H8 banking) + Op 29 (this entry).
- Substrate citations (Check 8 line-shift-resistant pattern operative for V3-11 internal references):
  - H1 substrate: 5 patch ops identified by V3-4/5/6/9/10 entry IDs (not line numbers); 6 substantive PHASE_5_BACKLOG.md instances at § anchors enumerated in G4 closure verification text.
  - H5 substrate: 6 line numbers bumped from pre-revision-history-bullet snapshot to post-bullet disk state (each Gn entry's literal-line-number citation corrected by +1).
  - H3 substrate: V3-2 entry's 5+4+5+7+3+1=25 arithmetic preserved char-exact; cross-reference from § 3.1 main doc to V3-2 added.
  - H4 substrate: Op 24 grep result + handler-read documenting default-case dispatch behavior; result appended as V3-2 substrate sub-verification (see V3-2 above for the appended sub-citation).
  - H2 substrate: 5 main-doc "at v2 lock" instances identified by audit-CC H2 line citations (245/306/316/322/336); replaced with generic "at lock" framing for cross-bible durability (Architecture Overview is referenced by all 6 downstream Phase 1 bibles).
- Closure of audit-CC v3 audit findings:
  - H1 MATERIAL — CLOSED ✓ (Section G G4 entry now reflects post-extension scope).
  - H2 STYLE — CLOSED ✓ (5 main-doc "v2 lock" → "lock" + front matter Locked → 2026-05-05; 0 stale "v2 lock" forms remain on grep verification).
  - H3 MINOR — CLOSED ✓ (Option (b) cross-reference added; § 3.1 main-doc topological framing preserved).
  - H4 MINOR — CLOSED ✓ (handler default-case dispatch substrate-verified; V3-2 sub-citation documents result).
  - H5 MINOR — CLOSED ✓ (6 line-number bumps applied; Check 8 banked for future cycles).
- Methodology-interpolation: ZERO net new constructs (Section D re-asserted). Pattern-completion: PASS (Section E re-asserted; W.N still only ratified letter-prefix).
- Front matter post-patch: Status = LOCKED v3 (2026-05-05); Locked = 2026-05-05; revision history v3 entry includes final-lock summary.
- Architecture Overview Phase 1 deliverable 1 of 7: LOCKED 2026-05-05.

---

## Verification log claim count summary

- **Section A inherited from v2 (META_PLAN v9 inheritance):** 2 entries (A.M9-1, A.M9-2). Inherited unchanged.
- **Section B inherited from v2 (Architecture Overview v1 inheritance):** 23 entries (11 v1 Section A + 12 V1-N). Inherited unchanged.
- **Section C inherited from v2 (V2-N):** 20 entries (V2-1 through V2-20). Inherited unchanged; V2-17 superseded by V3-1.
- **Section D net new methodology constructs:** 0.
- **Section E pattern-completion check:** PASS.
- **Section F FRAMEWORK_GAP / SPEC_GAP markers:** 0 FRAMEWORK_GAP, 0 SPEC_GAP.
- **Section G v2-audit-finding closure:** 8 of 8 CLOSED (1 BLOCKER + 2 MATERIAL + 2 MINOR + 3 STYLE).
- **Section H QB self-audit log:** 8 entries (H1-H8; H7 + H8 added per v3-final-lock patch banking Check 7 + Check 8).
- **Section I V3-N new entries:** 11 entries (V3-1 through V3-8c + V3-9 + V3-10 + V3-11).
- **Total verifiable substantive claims:** 56 (2 + 23 + 20 + 11 V3-N).

---

**End of Architecture Overview v3 verification log.**
