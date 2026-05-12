# Data Pipeline Bible v1 — Companion Verification Log

Document: data_pipeline_bible_v1_verification
Phase: 1 (Bible) — companion verification log for deliverable 3 of 7
Status: LOCKED v1-patched-c (2026-05-06) — companion log for Phase 1 deliverable 3 of 7 LOCKED; UPSTREAM-CORRECTION close (F.4 closed)
Author: CC (drafting under Tier 3 verification discipline; QB orchestrated)
Date: 2026-05-06

## Revision history

- v1 (2026-05-06): initial companion verification log for the v1 bible draft.
- v1-patched (2026-05-06): surgical patch closing F.1 (FRAMEWORK_GAP — § 8.W.1 / § 8.W.2 collapse-or-stand decision) per Tony's Option 3 ratification 2026-05-06. F.1 entry augmented with closure note; bible § 8.W.2 receives explicit deferral framing. See bible v1-patched revision-history bullet.
- v1-patched-a (2026-05-06): surgical patch closing audit-CC v1-patched audit findings (11 findings: 1 BLOCKER + 5 MATERIAL + 3 MINOR + 2 STYLE). V1-9 fabricated verbatim paste rewritten with actual stdout (G-A1 BLOCKER); Section C/E/F.1 narrative-referencing sections updated to post-patch state (G-A2 + G-A6 MATERIAL); FRAMEWORK_GAP F.4 surfaced for `angle_stats` out-of-band substrate gap with UPSTREAM-CORRECTION routed to D&S Bible patch cycle (G-A3 MATERIAL); V1-1 + V1-15 ellipsis-truncated rows re-pasted in full (G-A4 MATERIAL); empirical-discipline reframing for § 4.2.1 + § 4.2.3 + § 4.2.4 per Option C hybrid (G-A5 MATERIAL); plus G-A7 / G-A8 / G-A9 / G-A10 / G-A11 closures. New Section G documents per-finding closure substrate. See `data_pipeline_bible.md` v1-patched-a revision-history bullet.
- v1-patched-b (2026-05-06): surgical patch closing re-audit-CC v1-patched-a audit findings B1 (MATERIAL — bible § 4.2.1 ASSERTION_CLAUSE cross-reference correction per Op 1) + B2 (MINOR — F.1 FRAMEWORK_GAP marker format normalization per Op 2) + B4 (STYLE — bible EOF marker update per Op 3). B3 (Section G G-A7 + G-A10 template-fidelity polish) + B5 (§ 4.2.4 numbered-list format inconsistency) deferred to Phase 1 cleanup-cycle backlog per Tony's Decision 1 ratification 2026-05-06. Skip-audit ratified; no v1-patched-b audit cycle. See bible v1-patched-b revision-history bullet.
- v1-patched-b LOCKED (2026-05-06): companion log for Phase 1 deliverable 3 of 7 LOCKED. See bible v1-patched-b LOCKED revision-history bullet for threshold-condition summary + cross-bible context. Section G enumerates closure of 11 v1-patched audit findings (G-A1 through G-A11; all CLOSED). Section F.4 (angle_stats out-of-band substrate gap) open with UPSTREAM-CORRECTION pending separate D&S Bible v1-patched-d2 patch cycle.
- v1-patched-c (2026-05-06): surgical patch closing F.4 (FRAMEWORK_GAP — `angle_stats`) per UPSTREAM-CORRECTION close. § F.4 receives closure note pointing at `database_schema_bible:4.1.15` (D&S Bible v1-patched-d2 LOCKED 2026-05-06). Bible § 4.1.7 destination-table cross-reference re-ratified per Op 1. See bible v1-patched-c revision-history bullet for substrate provenance + threshold-condition summary.
- v1-patched-c LOCKED (2026-05-06): companion log for Phase 1 deliverable 3 of 7 re-LOCKED. See bible v1-patched-c LOCKED revision-history bullet for substrate provenance + threshold-condition summary. Section F F.4 marked CLOSED via UPSTREAM-CORRECTION close paragraph pointing at `database_schema_bible:4.1.15`. Section G closure verification preserved from v1-patched-a (11 of 11 prior-cycle audit findings CLOSED). v1-patched-c lock is final operation of session 2026-05-06.

This log is the companion verification artifact for `data_pipeline_bible.md` v1. Per META_PLAN v9 § 4.1 + § 6.5 Tier 3 discipline: drafts without companion verification logs are rejected by QB without audit. Section structure per QB handoff § 7.2 + the Data Pipeline Bible v1 Drafting Spec § 5:

- **Section A** — inherited claims from upstream Phase 0 / Phase 1 verification logs, with re-verification timestamps.
- **Section B** — NOT APPLICABLE for v1 (first cycle of this bible).
- **Section C** — new V1-N claims with primary citations + verbatim command output per AUDIT_METHODOLOGY § 4.10.
- **Section D** — methodology-interpolation self-check (target: ZERO new methodology constructs).
- **Section E** — pattern-completion check (W.N exclusivity preserved; numeric IDs per § 5.5 + G-new-1).
- **Section F** — FRAMEWORK_GAP / SPEC_GAP markers.
- **Section G** — NOT APPLICABLE for v1 (first cycle).
- **Section H** — QB self-audit log entries reproduced char-exact from the Drafting Spec § 6.
- **Section I** — NOT APPLICABLE for v1 (full draft, not surgical patch).

---

## Section A — Inherited claims from upstream verification logs

The substrate baseline for this bible inherits from three upstream Phase 0 / Phase 1 verification logs. Per Lesson 5 inheritance discipline + AUDIT_METHODOLOGY § 4.5 per-resource verification rule: re-verification timestamps below confirm the inherited substrate is still operative as of this draft's lock attempt 2026-05-06.

| Inherited claim | Source | Re-verification by drafting CC |
|---|---|---|
| 13 EventBridge rules (10 ENABLED + 3 DISABLED) with per-rule target verification | Architecture Overview v3 § 3.6 (LOCKED 2026-05-05) | Direct read of `architecture_overview.md` 2026-05-06: § 3.6 ENABLED table holds 10 rows; DISABLED table holds 3 rows. Per Lesson 5, no fresh `aws events list-targets-by-rule` calls run from drafting CC sandbox. |
| 5 ECS Fargate task families | Architecture Overview v3 § 3.2 | Direct read of `architecture_overview.md` 2026-05-06: § 3.2 table holds 5 rows: `equine-training`, `equine-training-daily-full`, `equine-training-manual`, `equine-training-pl`, `equine-training-win-prob`. |
| 8 Lambdas (5 Active + 3 Inactive) with per-Lambda State + memory + timeout | Architecture Overview v3 § 3.1 | Direct read 2026-05-06: § 3.1 Active table 5 rows; INACTIVE table 3 rows. |
| 4 fire-and-fail rules at lock (3 → equine-ingestion INACTIVE; 1 → equine-results INACTIVE) | Architecture Overview v3 § 3.6 anomaly note + § 6 Currently Open | Direct read 2026-05-06: anomaly note enumerates the 4 rules; § 6 Currently Open carries the substantive description (fire-and-fail anomaly canonical home). |
| `equine-ingestion` 25-action handler surface (5 data acquisition + 4 model lifecycle + 5 admin/diagnostic + 7 data backfills/ops + 3 originally-cited admin + 1 health = 25); default-case dispatch at handler tail | Architecture Overview v3 § 3.1 V3-2 sub-citation | Direct read 2026-05-06: `architecture_overview.md` line 79 row carries the V3-2 sub-citation; default-case at handler.py:1669-1680 confirmed at V1-5 below. |
| `wr_inference_service.py:718-730` 9 enrichment-field dynamic attribute attachment | Architecture Overview v3 § 4.2 | Direct read 2026-05-06; substrate confirmed at V1-7 below. |
| `ls_inference_service.py:388-401` dual-write pattern (F.3) | Database & Schema Bible v1 § 4.1.14 "Primary writers" + companion verification log | Direct read 2026-05-06; substrate confirmed at V1-6 below. |
| `wr_predictions` + `pl_predictions` out-of-band ALTER columns (F.2) | Database & Schema Bible v1 § 4.1.12 + § 4.1.13 | Direct read 2026-05-06: § 4.1.12 cites the `style` + `model_used` columns added via out-of-band ALTER not preserved as a tracked migration; § 4.1.13 cites the parallel observation for `pl_predictions`. |
| `ls_predictions` migration 010 column additions + post-migration-010 UNIQUE constraint `(race_id, entry_id, style)` | Database & Schema Bible v1 § 4.1.14 | Direct read 2026-05-06; matches the V1-6 substrate observation that `ls_inference_service.py:388-401` ON CONFLICT clause uses `(race_id, entry_id, style)`. |
| Bug #28 PHASE_5_BACKLOG.md Phase 5.3.1 entry (full TRIAGE_QUEUE_SPEC v1 § 3 fields) | PHASE_5_BACKLOG.md (CREATED 2026-05-04; ACTIVE) | Direct read of `PHASE_5_BACKLOG.md` 2026-05-06: file exists; Bug #28 entered at Phase 5.3.1 with all mandatory + conditional fields per TRIAGE_QUEUE_SPEC v1 § 3. Status "open" at lock. |
| `equibase_probe/` zero production-runtime consumers | Architecture Overview v3 § 3.7 + § 3.8 | Direct read 2026-05-06; substrate-confirmed at V1-10 below (fresh grep returns zero matches in `backend/` and `infrastructure/`). |

No drift surfaced between inherited substrate and drafting-CC re-verification. Lesson 6 (synthesis verification) gate satisfied: any inherited claim re-cited in this bible is substrate-verified at the upstream lock date AND re-confirmed at this draft's lock attempt.

---

## Section B — Inherited claims from prior cycles of this bible

NOT APPLICABLE. v1 is the first cycle of `data_pipeline_bible.md`; no prior cycles exist.

---

## Section C — New V1-N claims (verbatim command output per AUDIT_METHODOLOGY § 4.10)

Each entry below pastes verbatim command output as it appeared on stdout. Per the HARD RULE in the Drafting Spec § 1.1: summarization of command output is treated as fabrication-class risk and is FORBIDDEN.

### V1-1: 13 EventBridge rules (10 ENABLED + 3 DISABLED) — substrate inheritance from Architecture Overview v3 § 3.6

**Source-tier:** Tier 1 (live AWS state, inherited via Architecture Overview v3 § 3.6 verification log per Lesson 5 inheritance discipline).

**Decomposition:** 4 fire-and-fail (ENABLED → INACTIVE: ingestion-daily, fetch-results-nightly, angle-stats-nightly → equine-ingestion; results-daily → equine-results) + 4 active-Lambda (ENABLED → Active: ls-inference-daily, nyra-workouts-daily, pl-inference-daily, wr-inference-daily) + 2 ECS (daily-retrain-full, weekly-retrain-wr) + 3 DISABLED (feature-engineering-daily, inference-daily, weekly-retrain-pl). 4+4+2+3=13.

**Verification:** Direct read of `architecture_overview.md` § 3.6 ENABLED + DISABLED tables 2026-05-06 (per Lesson 5 — no fresh `aws events list-targets-by-rule` from drafting CC sandbox). Verbatim per-rule rows from architecture_overview.md § 3.6:

ENABLED table (lines 142-153 of architecture_overview.md; full row content re-pasted 2026-05-06 in v1-patched-a cycle to close audit-CC v1-patched A4 MATERIAL — ellipsis-truncation removed per AUDIT_METHODOLOGY § 4.10):
```
| Rule | Cron (UTC) | Target | Cross-reference |
|---|---|---|---|
| `equine-angle-stats-nightly` | `cron(15 2 * * ? *)` | **Lambda `equine-ingestion` (INACTIVE)** with `Input = {"action":"refresh_angle_stats"}` — fire-and-fail. The angle-stats refresh handler lives in `backend/lambdas/ingestion/handler.py:94`; target Lambda is INACTIVE; cron fires but invocation fails and the `angle_stats` table receives no fresh rows on those days. | `data_pipeline_bible:4.1` + § 6 below |
| `equine-daily-retrain-full` | `cron(30 2 * * ? *)` | ECS task family `equine-training-daily-full` (target ARN: cluster `equine-cluster`; `EcsParameters.TaskDefinitionArn = arn:aws:ecs:us-east-1:584812014683:task-definition/equine-training-daily-full`). | `model_evaluation_retraining_bible:4` |
| `equine-fetch-results-nightly` | `cron(30 1 * * ? *)` | **Lambda `equine-ingestion` (INACTIVE)** — fire-and-fail. No `Input` override. The "fetch results nightly" name is historical; current target is the ingestion Lambda (which is INACTIVE), not a separate results-fetch path. | `data_pipeline_bible:4.1` + § 6 below |
| `equine-ingestion-daily` | `cron(0 11 * * ? *)` | **Lambda `equine-ingestion` (INACTIVE)** — fire-and-fail. | `data_pipeline_bible:4.1` + § 6 below |
| `equine-ls-inference-daily` | `cron(40 12 * * ? *)` | Lambda `equine-ls-inference` (Active). | `data_pipeline_bible:4.1` |
| `equine-nyra-workouts-daily` | `cron(0 10 * * ? *)` | Lambda `equine-nyra-workouts` (Active). | `data_pipeline_bible:4.1` |
| `equine-pl-inference-daily` | `cron(35 12 * * ? *)` | Lambda `equine-pl-inference` (Active). | `data_pipeline_bible:4.1` |
| `equine-results-daily` | `cron(0 4 * * ? *)` | **Lambda `equine-results` (INACTIVE)** — fire-and-fail. | `data_pipeline_bible:4.1` + § 6 below |
| `equine-weekly-retrain-wr` | `cron(0 4 ? * MON *)` | ECS task family `equine-training-win-prob` (target ARN: cluster `equine-cluster`; `EcsParameters.TaskDefinitionArn = arn:aws:ecs:us-east-1:584812014683:task-definition/equine-training-win-prob`). | `model_evaluation_retraining_bible:4` |
| `equine-wr-inference-daily` | `cron(30 12 * * ? *)` | Lambda `equine-wr-inference` (Active). | `data_pipeline_bible:4.1` |
```

DISABLED table (lines 159-161 — data rows; full table block 157-161 includes header + separator):
```
| Rule | Cron (UTC) | Target (verified 2026-05-05) | Reason DISABLED |
|---|---|---|---|
| `equine-feature-engineering-daily` | `cron(0 12 * * ? *)` | **Zero current targets** (`aws events list-targets-by-rule --rule equine-feature-engineering-daily` returns empty Targets list). Originally targeted `equine-feature-engineering`; the target was removed at some point and the rule was disabled. | Operator-disabled when feature-engineering moved inference-side per Phase A3. |
| `equine-inference-daily` | `cron(30 12 * * ? *)` | **Zero current targets** (`aws events list-targets-by-rule --rule equine-inference-daily` returns empty Targets list). Originally targeted `equine-inference` for the legacy generic-inference EventBridge path. | Replaced by per-pipeline rules `equine-{wr,pl,ls}-inference-daily`. |
| `equine-weekly-retrain-pl` | `cron(0 5 ? * MON *)` | ECS task family `equine-training-pl` (target ARN: cluster `equine-cluster`; `EcsParameters.TaskDefinitionArn = arn:aws:ecs:us-east-1:584812014683:task-definition/equine-training-pl`). | Operator-disabled (PL retrain currently in `equine-daily-retrain-full` umbrella; standalone weekly suspended). |
```

10+3=13. Decomposition matches the Drafting Spec § 7 prediction. Used in this bible's § 3 + § 4.1.X + § 7.

### V1-2: ECS Fargate task families inventory — substrate inheritance from Architecture Overview v3 § 3.2

**Source-tier:** Tier 1 (live AWS state, inherited).

**Verification:** Direct read of `architecture_overview.md` § 3.2 table 2026-05-06. Verbatim 5 task family rows (lines 92-96; corrected from "92-97" off-by-one in v1-patched-a cycle to close audit-CC v1-patched A7 MINOR — line 97 is the post-table blank/separator, not a data row):

```
| `equine-training` | Generic training entrypoint (legacy/manual; precedes per-pipeline split). | Manual / unscheduled. |
| `equine-training-daily-full` | Full nightly retrain (all pipelines). | EventBridge `equine-daily-retrain-full` (`cron(30 2 * * ? *)`). |
| `equine-training-manual` | Operator-triggered manual retrain (ad-hoc). | Manual via console / CLI. |
| `equine-training-pl` | PL-specific training family. | EventBridge `equine-weekly-retrain-pl` (currently DISABLED). |
| `equine-training-win-prob` | WR-specific training family (win-probability ranker). | EventBridge `equine-weekly-retrain-wr` (`cron(0 4 ? * MON *)`). |
```

5 task families confirmed. Used in this bible's § 4.1.8 + § 4.1.9.

### V1-3: HRN scraper Bug #28 column-shift defect at hrn_scraper.py:802-804

**Source-tier:** Tier 4 (working-tree code post-baseline 87dec36).

**Verification command:** `sed -n '798,808p' /home/strakajagr/projects/equine-equalizer/backend/services/data_sources/hrn_scraper.py`

**Verbatim output:**
```
                'finish_position': i + 1,
                'official_finish': i + 1,
                'lengths_behind':  0.0,
                'final_time':      None,
                'win_payout':      parse_payout(1),
                'place_payout':    parse_payout(2),
                'show_payout':     parse_payout(3),
                'exacta_payout':   None,
                'trifecta_payout': None,
            })
```

**Verification command (line confirmation):** `grep -n "parse_payout" /home/strakajagr/projects/equine-equalizer/backend/services/data_sources/hrn_scraper.py`

**Verbatim output:**
```
785:            def parse_payout(idx):
802:                'win_payout':      parse_payout(1),
803:                'place_payout':    parse_payout(2),
804:                'show_payout':     parse_payout(3),
```

**Verification command (helper definition):** `sed -n '780,795p' /home/strakajagr/projects/equine-equalizer/backend/services/data_sources/hrn_scraper.py`

**Verbatim output:**
```
            )

            if not horse_name:
                continue

            def parse_payout(idx):
                if idx < len(cells):
                    txt = cells[idx].get_text(
                        strip=True
                    ).replace('$', '').replace(',', '').strip()
                    try:
                        return float(txt)
                    except ValueError:
                        return None
                return None
```

**Findings.** (a) `parse_payout(1)`, `parse_payout(2)`, `parse_payout(3)` calls are at exactly lines 802, 803, 804 — matches the Drafting Spec § 1.1 + Architecture Overview § 1.2 inheritance + PHASE_5_BACKLOG.md Phase 5.3.1 substrate. (b) The `parse_payout` helper at line 785 does `cells[idx].get_text(strip=True)` — purely positional cell indexing with NO column-header lookup. (c) Total `parse_payout` occurrences in the file: 4 (1 def at line 785 + 3 calls at lines 802-804). (d) Bug #28 substrate is confirmed at the canonical lines; no FRAMEWORK_GAP F (Phase 0 substrate-error class) is required for the line-number citation.

Used in this bible's § 4.1.2 + § 4.2.2 + § 5.1 + § 8.W.1.

### V1-4: HRN scraper DD pool extraction nuance at hrn_scraper.py:814

**Source-tier:** Tier 4 (working-tree code).

**Verification command:** `sed -n '810,820p' /home/strakajagr/projects/equine-equalizer/backend/services/data_sources/hrn_scraper.py`

**Verbatim output:**
```
            headers = [
                th.get_text(strip=True).lower()
                for th in table.find_all('th')
            ]
            if any('pool' in h for h in headers):
                for row in table.find_all('tr')[1:]:
                    cells = row.find_all('td')
                    if len(cells) < 3:
                        continue
                    pool = cells[0].get_text(strip=True).lower()
                    payout_txt = cells[2].get_text(
```

**Verification command (broader cell-indexing context):** `grep -n "table.find_all\|cells\[" /home/strakajagr/projects/equine-equalizer/backend/services/data_sources/hrn_scraper.py | head -30`

**Verbatim output:**
```
567:        for row in table.find_all('tr'):
661:        parent_row = cells[0].parent if cells else None
725:                and cell != cells[2]    # skip the horse cell
760:                for th in table.find_all('th')
771:            results_table.find_all('tr')[1:]
777:            horse_text = cells[0].get_text(strip=True)
787:                    txt = cells[idx].get_text(
812:                for th in table.find_all('th')
815:                for row in table.find_all('tr')[1:]:
819:                    pool = cells[0].get_text(strip=True).lower()
820:                    payout_txt = cells[2].get_text(
```

**Findings.** (a) Line 814 is the entry point of the pool-table-loop block (`if any('pool' in h for h in headers):`). The actual cell-indexing is at lines 819-820 (`cells[0]` for pool name; `cells[2]` for payout text). The Drafting Spec's reference to "line 814" identifies the entry point of the pool extraction logic; the positional-cell-indexing surface that bears the Bug #28-class defect is at lines 819-820. (b) The block has SOME column-header awareness — the table-level guard `if any('pool' in h for h in headers):` checks the table's `<th>` headers for the literal token `pool` — but this header check only identifies the table TYPE, not the column POSITIONS within the table. Once inside the loop, the code uses positional `cells[0]` / `cells[2]` indexing with no column-header lookup for which column holds pool name vs payout. (c) The defect class is the same as § 8.W.1: positional column indexing without column-header verification (→ § 5.1 candidate Forbidden Pattern). (d) The defect manifests in DIFFERENT code paths affecting DIFFERENT page tables: § 8.W.1 hits the finishing-positions/payouts row table; § 8.W.2 hits the pool-summary table. (e) Whether the upstream HRN-page-structure change of circa 2026-04-30 propagates to BOTH tables identically OR distinctly is not substrate-determinable from the working-tree code alone — it requires inspecting the live HRN page structure (which is Phase 5.3.1 scope per PHASE_5_BACKLOG.md "Dependencies" sub-section).

**Substrate disposition routing per Tony's Item 2 ratification (Drafting Spec § 1.1 paste-prompt "Bug #28 substrate disposition routing"):** the substrate observations support BOTH stand-alone and collapse dispositions:
- **Stand-alone:** different code paths, different page tables, different positional indices, different fields populated.
- **Collapse:** same defect class, both candidate-Forbidden-Pattern-relevant, PHASE_5_BACKLOG.md Phase 5.3.1 tracks them as a single Phase 5.3.1 item with DD pool extraction listed as a "Phase 1 audit's job" sub-dependency.

Per the spec: drafting CC drafts both as separate § 8.W.1 + § 8.W.2 entries by default; FRAMEWORK_GAP F.1 (Section F below) presents the substrate-cited candidate reframing for QB → Tony ratification per Lesson § 4.8.

Used in this bible's § 4.1.2 + § 4.2.2 + § 5.1 + § 8.W.2.

### V1-5: equine-ingestion handler default-case dispatch path

**Source-tier:** Tier 4.

**Verification command:** `sed -n '1665,1685p' /home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py`

**Verbatim output:**
```
                    'db_time': str(result['t'])
                })
            }

    # ── Normal scheduled ingestion ──
    logger.info(
        f"Daily ingestion triggered for {date.today()}"
    )
    try:
        with get_db() as conn:
            service = IngestionService(conn)
            service.fetch_daily_entries(date.today())
        return {
            'statusCode': 200,
            'body': 'Ingestion complete'
        }
    except Exception as e:
        logger.error(
            f"Ingestion failed: {e}",
            exc_info=True
        )
```

**Findings.** The "Normal scheduled ingestion" block at handler.py:1669-1680 is the default-case dispatch path: when `event.get('action')` is None (no `action` Input on the EventBridge target), the handler falls through all `if action == '<name>':` branches to the tail-end block which calls `IngestionService(conn).fetch_daily_entries(date.today())`. This confirms the Architecture Overview § 3.1 V3-2 sub-citation. The two EventBridge rules `equine-ingestion-daily` and `equine-fetch-results-nightly` exercise this default-case path per their Input absence at `architecture_overview:3.6`.

Used in this bible's § 2 (definition: default-case dispatch) + § 4.1.1 + § 4.1.2.

### V1-6: ls_inference_service.py:388-401 dual-write substrate (F.3 cross-reference)

**Source-tier:** Tier 4.

**Verification command:** `sed -n '385,405p' /home/strakajagr/projects/equine-equalizer/backend/services/ls_inference_service.py`

**Verbatim output:**
```
                    # Write 2: NEW first-class ls_predictions row
                    with self.conn.cursor() as cur:
                        cur.execute("""
                            INSERT INTO ls_predictions (
                                entry_id, race_id, horse_id, model_version_id,
                                style, final_win_probability,
                                longshot_alert, confidence,
                                predicted_rank, xgb_rank_score,
                                rf_longshot_prob, lstm_trajectory,
                                calibrated_win_prob, bayesian_angle_ev,
                                angle_description, market_prob, edge_pct,
                                is_top_pick, morning_line_implied_prob
                            ) VALUES (
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s
                            )
                            ON CONFLICT (race_id, entry_id, style) DO UPDATE SET
                                final_win_probability = EXCLUDED.final_win_probability,
                                longshot_alert = EXCLUDED.longshot_alert,
                                confidence = EXCLUDED.confidence,
                                predicted_rank = EXCLUDED.predicted_rank,
```

**Findings.** (a) The "Write 2: NEW first-class ls_predictions row" comment at line 385 confirms the dual-write nomenclature inherited from Database & Schema Bible § 4.1.14 (Write 1 is the LS-as-second-pass-enrichment on `wr_predictions` columns; Write 2 is the post-migration-010 first-class `ls_predictions` row). (b) The 19-column INSERT covers all migration-005 + migration-010 columns per `database_schema_bible:4.1.14` Migration 005 columns + Migration 010 additions tables (note: actual column count in the INSERT is 19; subtract `prediction_id` (UUID, default `gen_random_uuid()`) + `feature_importance` (JSONB, default `'{}'`) + `created_at` (TIMESTAMPTZ, default `NOW()`) + `confidence_score` from the migration 005 column count of 21 + 5 migration 010 columns = 26 declared columns − 4 default-populated columns − 3 backfill-only columns (`actual_finish`, `was_win`, `bet_profit`, `actual_odds`) = 19 INSERT columns; arithmetic confirms). (c) `ON CONFLICT (race_id, entry_id, style) DO UPDATE SET ...` matches the post-migration-010 UNIQUE constraint per `database_schema_bible:4.1.14` "UNIQUE constraints (current, post-migration 010)" sub-section. (d) The dual-write pattern is canonically described at `database_schema_bible:4.1.14`; this bible's § 4.1.5.3 carries the flow-context observation only.

Used in this bible's § 4.1.5.3 (F.3 cross-reference).

### V1-7: wr_inference_service.py:718-730 dynamic attribute attachment substrate

**Source-tier:** Tier 4.

**Verification command:** `sed -n '716,732p' /home/strakajagr/projects/equine-equalizer/backend/services/wr_inference_service.py`

**Verbatim output:**
```
            )
            # Attach extra fields for storage
            pred.raw_win_prob = round(float(raw_probs[idx]), 4)
            pred.handicapping_prob = round(handicapping_prob, 4)
            pred.market_prob = (
                round(market_prob, 4) if market_prob is not None else None
            )
            pred.edge_pct = (
                round(edge_pct, 4) if edge_pct is not None else None
            )
            pred.rank_score = round(float(rank_scores[idx]), 4)
            pred.kelly_fraction = value['kelly_fraction']
            pred.kelly_bet = value['kelly_bet']
            pred.has_workout_data = bool(has_workout[idx])
            pred.model_used = model_used[idx]
            predictions.append(pred)
```

**Findings.** 9 enrichment fields attached to the base `Prediction` dataclass via Python attribute assignment, matching Architecture Overview § 4.2 inheritance: `raw_win_prob` (line 718), `handicapping_prob` (719), `market_prob` (720-722), `edge_pct` (723-725), `rank_score` (726), `kelly_fraction` (727), `kelly_bet` (728), `has_workout_data` (729), `model_used` (730). The dynamically-attached fields are NOT in the dataclass schema. The append at line 731 closes the block.

Used in this bible's § 4.1.5.1.

### V1-8: backend/services/data_sources/ directory enumeration

**Source-tier:** Tier 4.

**Verification command:** `ls -la /home/strakajagr/projects/equine-equalizer/backend/services/data_sources/`

**Verbatim output:**
```
total 76
drwxr-xr-x 3 strakajagr strakajagr  4096 May  1 10:26 .
drwxr-xr-x 4 strakajagr strakajagr  4096 May  2 01:45 ..
-rw-r--r-- 1 strakajagr strakajagr   629 Mar 15 18:56 README.md
-rw-r--r-- 1 strakajagr strakajagr   195 Mar 17 19:14 __init__.py
drwxr-xr-x 2 strakajagr strakajagr  4096 Mar 15 19:08 __pycache__
-rw-r--r-- 1 strakajagr strakajagr  3456 Mar 15 18:55 base.py
-rw-r--r-- 1 strakajagr strakajagr 33506 May  1 10:26 hrn_scraper.py
-rw-r--r-- 1 strakajagr strakajagr 15205 Mar 17 19:33 hrn_workout_scraper.py
```

**Findings.** Three production data source modules in the directory: `base.py` (DataSourceInterface base class — confirmed via line 84 of hrn_scraper.py: `class HRNScraper(DataSourceInterface):`), `hrn_scraper.py` (the HRN entries + results scraper; Bug #28 surface), `hrn_workout_scraper.py` (HRN workout scraper; Bug #7 surface). The chart parser is NOT in this directory — it lives at `backend/services/chart_parser.py` per V1-9 substrate. Used in this bible's § 4.2.1 + § 4.2.2 + § 4.2.3 + § 4.2.5.

### V1-9: Chart parser trigger inheritance

**Source-tier:** Tier 4.

**Verification command:** `grep -n "chart_parser\|parse_chart\|parseChart" /home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py /home/strakajagr/projects/equine-equalizer/backend/services/data_sources/hrn_scraper.py /home/strakajagr/projects/equine-equalizer/backend/services/data_sources/hrn_workout_scraper.py /home/strakajagr/projects/equine-equalizer/backend/services/data_sources/base.py`

**Verbatim output:**
```
/home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py:540:    # Invoke: {"action": "parse_charts", "track": "GP"}
/home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py:541:    # Or all tracks: {"action": "parse_charts"}
/home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py:542:    if action == 'parse_charts':
/home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py:548:            from services.chart_parser import run_from_s3
```

**Verification command (broader search):** `grep -rn "chart_parser\|parse_chart\|chart_parsing\|ChartParser" /home/strakajagr/projects/equine-equalizer/backend/`

**Verbatim output (head):**
```
/home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py:540:    # Invoke: {"action": "parse_charts", "track": "GP"}
/home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py:541:    # Or all tracks: {"action": "parse_charts"}
/home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py:542:    if action == 'parse_charts':
/home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py:548:            from services.chart_parser import run_from_s3
/home/strakajagr/projects/equine-equalizer/backend/services/chart_parser.py:8:  {"action": "parse_charts", "track": "GP"}
/home/strakajagr/projects/equine-equalizer/backend/services/chart_parser.py:9:  {"action": "parse_charts"}  (all tracks)
```

**Verification command (handler context):** `sed -n '538,565p' /home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py`

**Verbatim output (re-run 2026-05-06 in v1-patched-a cycle to close audit-CC v1-patched A1 BLOCKER — fabricated paste rewritten with actual stdout per AUDIT_METHODOLOGY § 4.10):**
```
    # ── Parse charts action ──
    # Parse Equibase PDF charts from S3 into Aurora
    # Invoke: {"action": "parse_charts", "track": "GP"}
    # Or all tracks: {"action": "parse_charts"}
    if action == 'parse_charts':
        logger.info("Running chart parser")
        track = event.get('track')  # optional
        date_from = event.get('date_from')  # YYYYMMDD
        date_to = event.get('date_to')  # YYYYMMDD
        try:
            from services.chart_parser import run_from_s3
            with get_db() as conn:
                result = run_from_s3(
                    conn, track=track,
                    date_from=date_from, date_to=date_to
                )
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
        except Exception as e:
            logger.error(
                f"Chart parser failed: {e}",
                exc_info=True
            )
            return {
                'statusCode': 500,
                'body': json.dumps({
```

**Findings.** (a) Chart parser is invoked via the **`parse_charts` admin action** on `equine-ingestion` Lambda (handler at `backend/lambdas/ingestion/handler.py:540-558`). (b) The chart parser module itself lives at `backend/services/chart_parser.py` (not in `backend/services/data_sources/`). (c) **No EventBridge rule** at `architecture_overview:3.6` carries `parse_charts` as its `Input` action — the chart parser has no direct cron schedule. (d) Optional `date_from` / `date_to` parameters supported (`YYYYMMDD` format). (e) Per `architecture_overview:3.1` row for `equine-ingestion`: the Lambda is INACTIVE at lock; therefore the `parse_charts` admin action is non-functional via the production invocation path until the Lambda is re-activated.

Used in this bible's § 4.1.3 + § 4.2.5.

### V1-10: equibase_probe/ production-consumer count = 0 — substrate inheritance

**Source-tier:** Tier 4 inheritance (verified by Architecture Overview v3 § 3.7 + § 3.8) + drafting-CC re-verification.

**Verification command:** `grep -rn "equibase_probe" /home/strakajagr/projects/equine-equalizer/backend/ /home/strakajagr/projects/equine-equalizer/infrastructure/`

**Verbatim output (re-pasted 2026-05-06 in v1-patched-a cycle to close audit-CC v1-patched A10 STYLE — drafter's working-notes parenthetical stripped per AUDIT_METHODOLOGY § 4.10):**
```
<empty stdout; grep exit code 1 — zero matches>
```

**Verification command (probe directory contents):** `ls /home/strakajagr/projects/equine-equalizer/equibase_probe/`

**Verbatim output:**
```
Dockerfile
Dockerfile.optiona2
Dockerfile.optionb
Dockerfile.optiond
option_a2_probe.py
option_b_probe.py
option_d_probe.py
probe.py
```

**Findings.** (a) Zero matches of `equibase_probe` in `backend/` or `infrastructure/` confirms zero production-runtime consumers per `architecture_overview:3.7` + `architecture_overview:3.8` inheritance. (b) The probe directory holds 4 Python probe scripts + 4 Dockerfiles (1 base Dockerfile + 3 option-specific Dockerfiles). (c) The probe scripts are exploratory acquisition strategy work (Option A2 / B / D); they have not been promoted to a deployed Lambda or ECS task.

Used in this bible's § 4.2.6.

### V1-11: PHASE_5_BACKLOG.md Phase 5.3.1 entry verbatim

**Source-tier:** Tier 6 (PHASE_5_BACKLOG.md baseline) + inherits Tier 5 (operator memory file verbatim quotes).

**Verification command:** `cat /home/strakajagr/projects/equine-equalizer/docs/bible/PHASE_5_BACKLOG.md`

**Verbatim Phase 5.3.1 entry (lines 18-64 of PHASE_5_BACKLOG.md):**
```
### Phase 5.3.1: HRN Scraper Bug #28 (column shift)

**Severity:** MATERIAL (silent data loss; affects all win/DD payouts since 2026-04-30; structural failure in data acquisition layer per META_PLAN v6 § 7.9)

**Surfaced:** 2026-05-03 (during EE_CURRENT_STATE_DUMP generation; per operator memory file `equine-equalizer-bug-28-hrn-scraper.md`, the regression was sharp — 2026-04-29 last clean day at 9/10 win-payout success; 2026-04-30 onward all 0/N)

**Stable-known classification:** provisional. Backfill-feasibility AND DD-pool-extraction bounded-loss assumptions both pending Phase 1 Data Pipeline Bible audit verification (per META_PLAN v6 § 8.1).

**Root cause:** HRN page structure changed circa 2026-04-30 (likely added an icon column to the payouts table). The `parse_payout(N)` calls at `backend/services/data_sources/hrn_scraper.py:802-804` (verified) use positional cell indexing that has been off-by-one ever since.

**Manifestation:**
- `win_payout` is NULL across all results rows from 2026-04-30 onward
- `daily_double_payout` is NULL across same range
- `place_payout` stores values that should be in `win_payout`
- `show_payout` stores values that should be in `place_payout`
- Place, show, and exacta payouts still populate per operator memory file's symptom statement
- DD pool extraction at `hrn_scraper.py:814` flagged as "likely has the same root cause" — distinct code path from `daily_double_payout` result-dict field; Phase 1 verifies bounded-loss status

**Operator-verified external source:** the operator memory file `equine-equalizer-bug-28-hrn-scraper.md` contains the following verbatim passages per META_PLAN v6 verification log Claim 15c:

> "starting 2026-04-30, all results.win_payout and results.daily_double_payout rows are NULL across every track/race scraped via HRN. Place, show, and exacta payouts still populate."

> "DD pool extraction (hrn_scraper.py:814 'pool' table loop) likely has the same root cause — same site-wide column shift."

**Dependencies:**
- Resolution requires HRN page-structure verification (manual: visit a results page, confirm column structure)
- May require parser refactor if HRN structure is now variable-by-page-type
- Requires backfill of affected results rows after fix deploys (feasibility assumed; Phase 1 verifies)
- DD pool extraction status verification (Phase 1 Data Pipeline Bible audit's job)

No queue entries currently block or are blocked by Bug #28 (this is the seed entry).

**Re-classification trigger:** if Phase 1 Data Pipeline Bible audit verifies backfill is feasible AND DD pool extraction is bounded, the provisional qualifier drops at audit-lock time. If the audit verifies backfill is NOT feasible (or DD pool extraction reveals additional uncovered loss), Bug #28 re-classifies as either (a) "known but not stable" — § 8.1 exception logic could trigger if operator chooses to escalate, or (b) "stable known with permanent loss" — affected window's data unrecoverable, bible documents the data gap as permanent feature of historical record. Phase 1 audit's classification call is the lock-trigger.

**Audit-cycle reference:** N/A — Bug #28 surfaced pre-Phase-1 during EE_CURRENT_STATE_DUMP generation, not during a Phase 1+ audit cycle. Documented in META_PLAN v6 § 1.2 + § 8.1 + Appendix A.5 as the canonical seed entry for this file.

**Disposition:** Fix in Phase 5.3 before any Phase 5 work that depends on payout data.

**Rollback:** Standard git revert if fix introduces regression. No DB rollback needed (fix re-populates rows that are currently NULL).

**Bible references on resolution:**
- Update `data_pipeline_bible.md` § 7.9 (HRN scraper documentation)
- Add `data_pipeline_bible.md` § 8.W.<n> (What Was Fixed entry; canonical home per BIBLE_STRUCTURE_SPEC v3 § 5.3)
- Consider new Forbidden Pattern: positional column indexing in scrapers without column-header verification

**Status:** open
**Created:** 2026-05-04
```

**Findings.** (a) Phase 5.3.1 entry confirmed at PHASE_5_BACKLOG.md lines 18-64. (b) Operator-verified external source (Claim 15c quotes) reproduced verbatim in this bible's § 6 + § 8.W.1 + § 8.W.2. (c) The "Bible references on resolution" sub-section cites `data_pipeline_bible.md § 8.W.<n>` and "Consider new Forbidden Pattern: positional column indexing in scrapers without column-header verification" — this bible's § 8.W.1 + § 8.W.2 + § 5.1 satisfy these forward-references. (d) Note: PHASE_5_BACKLOG.md cites "META_PLAN v6 § 7.9" + "BIBLE_STRUCTURE_SPEC v3 § 5.3" by version (v6 / v3) reflecting the document state at PHASE_5_BACKLOG.md's creation 2026-05-04; the current locked versions are META_PLAN v9 § 7.9 + BIBLE_STRUCTURE_SPEC v6 § 5.3. The version numbers are stale but the section pointers remain operative.

Used in this bible's § 6 + § 8.W.1 + § 8.W.2.

### V1-12: NYRA workouts Lambda Active state inheritance

**Source-tier:** Tier 1 (live AWS state, inherited via Architecture Overview v3 § 3.1).

**Verification:** Direct read of `architecture_overview.md` § 3.1 Active table 2026-05-06. Verbatim row (line 73):
```
| `equine-nyra-workouts` | 512 | 300 | Daily NYRA workout scrape (NYRA tracks only). HRN scraper is separate (currently broken — EE Bug #7). | `data_pipeline_bible:4.1` |
```

**Findings.** `equine-nyra-workouts` is Active at lock; memory 512 MB; timeout 300 s. Used in this bible's § 4.1.4 + § 4.2.4.

### V1-13: All Active inference Lambda configurations (WR / PL / LS) inheritance

**Source-tier:** Tier 1 (inherited).

**Verification:** Direct read of `architecture_overview.md` § 3.1 Active table 2026-05-06. Verbatim rows (lines 70-72):
```
| `equine-wr-inference` | 1024 | 300 | Daily WR (win-and-rank) inference: produces ranking + win-probability per entry; writes `wr_predictions`. Uses base `Prediction` shape with attached enrichment fields per § 4.2. | `ml_layer_architecture_bible:4.2`, `data_pipeline_bible:4.1` |
| `equine-pl-inference` | 1024 | 300 | Daily PL (place/show) inference: writes `pl_predictions` with `PLPrediction` shape per § 4.2. | `ml_layer_architecture_bible:4.2`, `data_pipeline_bible:4.1` |
| `equine-ls-inference` | 1024 | 300 | Daily LS (longshot) inference: writes `ls_predictions` with `LSPrediction` shape per § 4.2; LS-specific 4-way strict-alert flag (see EE Bug #25). | `ml_layer_architecture_bible:4.2`, `data_pipeline_bible:4.1` |
```

**Findings.** All 3 inference Lambdas Active at lock; memory 1024 MB; timeout 300 s each. Used in this bible's § 4.1.5.1 + § 4.1.5.2 + § 4.1.5.3.

### V1-14: Bug #28 cross-reference count (post-draft)

**Source-tier:** Tier 4 (this bible's body).

**Verification command:** `grep -c "Bug #28" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md`

(Run by post-draft grep predictions; result reproduced in Section H9 + the post-draft grep prediction summary at end of Section C.)

**Decomposition (per Lesson § 4.10).** The Bug #28 occurrences in this bible's body track to: § 1 Scope (1 reference inside the source-priority paragraph context), § 3 Pipeline overview (1 in the Bug #28 surface paragraph), § 4.1.2 Nightly results fetch ("Bug #28 cross-reference" sub-block carries multiple), § 4.2.2 HRN results, § 5.1 candidate Forbidden Pattern (rationale paragraph + substrate provenance), § 6 Currently Open (substantive description carries multiple), § 8.W.1 entry header + body, § 8.W.2 entry body. The post-draft grep count is documented in the "Post-draft grep predictions" summary at the end of Section C.

### V1-15: Three DISABLED EventBridge rules at § 7 substrate

**Source-tier:** Tier 1 (inherited).

**Verification:** Direct read of `architecture_overview.md` § 3.6 DISABLED table 2026-05-06. Verbatim 3 rows (lines 159-161; full row content per AUDIT_METHODOLOGY § 4.10 — V1-15 row pastes had no ellipsis-truncation in v1 cycle so v1-patched-a A4 closure is a no-op for V1-15; substrate confirmed identical to V1-1 DISABLED table re-paste in Op 11):
```
| `equine-feature-engineering-daily` | `cron(0 12 * * ? *)` | **Zero current targets** (`aws events list-targets-by-rule --rule equine-feature-engineering-daily` returns empty Targets list). Originally targeted `equine-feature-engineering`; the target was removed at some point and the rule was disabled. | Operator-disabled when feature-engineering moved inference-side per Phase A3. |
| `equine-inference-daily` | `cron(30 12 * * ? *)` | **Zero current targets** (`aws events list-targets-by-rule --rule equine-inference-daily` returns empty Targets list). Originally targeted `equine-inference` for the legacy generic-inference EventBridge path. | Replaced by per-pipeline rules `equine-{wr,pl,ls}-inference-daily`. |
| `equine-weekly-retrain-pl` | `cron(0 5 ? * MON *)` | ECS task family `equine-training-pl` (target ARN: cluster `equine-cluster`; `EcsParameters.TaskDefinitionArn = arn:aws:ecs:us-east-1:584812014683:task-definition/equine-training-pl`). | Operator-disabled (PL retrain currently in `equine-daily-retrain-full` umbrella; standalone weekly suspended). |
```

**Findings.** 3 DISABLED rules confirmed; matches the Drafting Spec § 7 prediction. Used in this bible's § 7 (Deprecated).

### Post-draft grep predictions (Drafting Spec § 1.1 "Bash-grep verification predictions")

The grep predictions below are run AFTER the bible draft lands on disk; results are documented here verbatim per Lesson § 4.10. Run subsequent to bible Write.

**Prediction 1:** `grep -c "Bug #28" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md` → expected ≥ 2.

**Prediction 2:** `grep -c "Phase 5.3.1" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md` → expected ≥ 1.

**Prediction 3:** `grep -c "Phase 5.X.Y" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md` → expected 0–2.

**Prediction 4:** `grep -c "fire-and-fail" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md` → expected ≥ 5.

**Prediction 5:** `grep -c "architecture_overview:" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md` → expected ≥ 20.

**Prediction 6:** `grep -c "database_schema_bible:" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md` → expected ≥ 10.

The post-draft grep results are documented below verbatim, run subsequent to the bible Write 2026-05-06.

**Post-draft grep results (verbatim stdout; refreshed 2026-05-06 in v1-patched-a cycle to close audit-CC v1-patched A2 + A6 MATERIAL — stale post-patch counts updated):**

```
$ grep -c "Bug #28" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md
15
$ grep -c "Phase 5.3.1" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md
26
$ grep -c "Phase 5.X.Y" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md
0
$ grep -c "fire-and-fail" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md
8
$ grep -c "architecture_overview:" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md
76
$ grep -c "database_schema_bible:" /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md
29
$ wc -l /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md
583 /home/strakajagr/projects/equine-equalizer/docs/bible/data_pipeline_bible.md
```

**Reconciliation against Drafting Spec § 7 predictions (post-v1-patched-a):**

| Pattern | Predicted floor | Actual (v1-patched-a) | Status |
|---|---|---|---|
| `Bug #28` | ≥ 2 | 15 | ✅ exceeds floor |
| `Phase 5.3.1` | ≥ 1 | 26 | ✅ exceeds floor (post-v1-patched additions in revision-history bullet + deferral paragraph + Op 4 cross-reference + Op 8 revision-history bullet) |
| `Phase 5.X.Y` | 0–2 | 0 | ✅ within range (substantive F.2/F.3 disposition at database_schema_bible canonical home) |
| `fire-and-fail` | ≥ 5 | 8 | ✅ exceeds floor |
| `architecture_overview:` | ≥ 20 | 76 | ✅ exceeds floor (post-v1-patched-a: +2 from Op 7 NYRA two-source-check additions) |
| `database_schema_bible:` | ≥ 10 | 29 | ✅ exceeds floor (post-v1-patched-a: +2 from Op 4 angle_stats reframe references + Op 5 V1-12 substrate reference) |

All 6 grep predictions satisfied. No FRAMEWORK_GAP / SPEC_GAP surfaced by grep-prediction reconciliation.

---

## Section D — Methodology-interpolation self-check

**Target: ZERO new methodology constructs.**

This bible draft introduces ZERO CC-prescribed methodology constructs Tony has not explicitly ratified. Inherited methodology constructs operative in this draft:

- Tier 3 verification discipline (META_PLAN v9 § 4.1 + § 6.5) — upstream-ratified.
- Source-priority hierarchy (META_PLAN v9 § 4.5) — upstream-ratified.
- Verification log precision rule (META_PLAN v9 § 6.5) — upstream-ratified; counts decomposed in V1-1 (10 ENABLED + 3 DISABLED), V1-2 (5 task families), V1-3 (4 parse_payout occurrences = 1 def + 3 calls), etc.
- Verbatim-paste discipline (AUDIT_METHODOLOGY § 4.10) — upstream-ratified; operative for all V1-N entries above.
- Per-resource verification when target/state are independent (AUDIT_METHODOLOGY § 4.5; Lesson 5) — upstream-ratified; inheritance discipline operative for the 13-rule × per-rule-target verification (V1-1 inherits from `architecture_overview:3.6`; no fresh `aws events list-targets-by-rule` from drafting CC sandbox).
- Data Acquisition Honesty Protocol (META_PLAN v9 § 7.9) — upstream-ratified; § 4.2 of this bible follows the 5-mandatory-fields format (what / current reliability / failure manifestation / current acquisition mode / honest disposition).
- Placeholder-resolution sub-rule (META_PLAN v9 § 7.3) — upstream-ratified; operative for § 8.W.1 + § 8.W.2 Fix-date placeholders (forward-looking discipline codification; bug not yet fixed at lock).
- BIBLE_STRUCTURE_SPEC v6 § 5.3 cross-cutting bug scope rule — upstream-ratified; operative for Bug #28 canonical-home assignment in this bible + fire-and-fail anomaly cross-reference at § 6.
- BIBLE_STRUCTURE_SPEC v6 § 5.5.1 global Bug #N convention — upstream-ratified; operative for § 8.W.2 Bug #N TBD routing.
- BIBLE_STRUCTURE_SPEC v6 § 5.6.1.2 tertiary-state notation for conditional triggers — upstream-ratified; operative for § 8.W.1 + § 8.W.2 conditional-trigger blocks.
- BIBLE_STRUCTURE_SPEC v6 § 5.7 candidate-roster workflow + G-new-1 numeric-IDs-for-candidates rule — upstream-ratified; operative for § 5 candidate roster.
- Tony's Item 2 ratification 2026-05-05 (Bug #28 substrate disposition routing — § 8.W.1 + § 8.W.2 default to separate; FRAMEWORK_GAP routing for collapse-or-stand decision) — upstream-ratified; operative for § 8.W.1 + § 8.W.2 substrate disposition.
- Per Architecture Overview § 5.1 + § 5.2 governing rules — upstream-ratified; every § 4.1.X sub-section in this bible cites Lambda State + EventBridge target State at the same lock time.

NO new binary tests, cadence rules, completeness criteria, scoring rubrics, severity thresholds, iteration caps, percentage criteria, or procedural sequencing rules introduced in this draft. The conditional-trigger applications in § 8.W.1 / § 8.W.2 / § 7 (G-new-1 closure operative) are upstream-ratified.

---

## Section E — Pattern-completion check

**W.N exclusivity preserved.** Per BIBLE_STRUCTURE_SPEC v6 § 5.5: this bible's § 8 introduces ZERO new letter-prefixes beyond W.N. Two W.N entries surfaced: § 8.W.1 (Bug #28; column shift at hrn_scraper.py:802-804) and § 8.W.2 (Bug #N TBD; DD pool extraction nuance at hrn_scraper.py:814).

**Numeric IDs for candidate roster per § 5.5 + G-new-1.** This bible's § 5 candidate roster uses numeric sub-section IDs `5.1` and `5.2`, NOT provisional letter-prefixes (no `5.A`, `5.F.1`, etc.). Candidate status is conveyed by the § 5 header marker `[candidate roster pending QB ratification per § 5.7]`.

**Cross-bible bug reference syntax per § 5.5.1.** The single cross-bible bug reference in this draft is the implicit Bug #28 reference; the global Bug #N (28) is in use per `architecture_overview:1` revision history + META_PLAN v9 § 1.2. § 8.W.2's Bug #N is marked `[Bug #N TBD — pending Phase 5.3.1 fix-time substrate verification]` per Tony's Option 3 ratification 2026-05-06 — drafting CC does NOT assign a new global Bug #N here.

**Empty-section explicit rules per § 5.2.** § 6 Currently Open carries empty-section explicit text ("No additional Currently Open entries at lock canonically homed in this bible's domain.") below the substantive Bug #28 description + fire-and-fail one-line cross-reference. § 7 Deprecated enumerates the 3 DISABLED EventBridge rules + carries empty-section explicit text. § 8 What Was Fixed enumerates § 8.W.1 + § 8.W.2 + carries empty-section explicit text.

---

## Section F — FRAMEWORK_GAP / SPEC_GAP markers

### F.1 <FRAMEWORK_GAP: § 8.W.1 / § 8.W.2 collapse-or-stand decision> (per Tony's Item 2 ratification routing)

**Status.** Substrate-cited candidate reframing surfaced for QB → Tony ratification per AUDIT_METHODOLOGY § 4.8 + Lesson 4 + Drafting Spec § 1.1 paste-prompt "Bug #28 substrate disposition routing".

**Substrate evidence (from V1-3 + V1-4).**

- V1-3 confirms `parse_payout(1)` / `parse_payout(2)` / `parse_payout(3)` at `hrn_scraper.py:802-804` (results-table finishing-positions row; helper at line 785 indexes `cells[idx]` purely positionally).
- V1-4 confirms the pool-table loop at `hrn_scraper.py:814+` (table-level header guard `if any('pool' in h for h in headers):` at line 814; positional indexing `cells[0]` for pool name + `cells[2]` for payout text at lines 819-820 — no column-header verification within the row).

**Substrate observations bearing on the decision.**

- **Same defect class.** Both code paths use positional column indexing without per-column-header verification — exactly the candidate Forbidden Pattern at § 5.1.
- **Different code paths.** V1-3 hits a results-table finishing-positions row via the `parse_payout` helper; V1-4 hits a pool-table summary row via direct `cells[N]` indexing. Different page tables; different positional indices; different fields populated (`results.win_payout` / `place_payout` / `show_payout` vs the pool data).
- **Different observed manifestation symptoms.** V1-3's manifestation is documented in PHASE_5_BACKLOG.md Phase 5.3.1: NULL `win_payout` + NULL `daily_double_payout` + column-shifted `place_payout` / `show_payout`. V1-4's manifestation is **inferred** ("likely has the same root cause" per the operator memory file's verbatim quote) but not directly substrate-verified at this draft's lock attempt — verifying it requires inspecting the live HRN page structure (which is Phase 5.3.1 scope per PHASE_5_BACKLOG.md "Dependencies" sub-section).
- **PHASE_5_BACKLOG.md framing.** Phase 5.3.1 tracks BOTH as a single Phase 5.3.1 item, with "DD pool extraction status verification (Phase 1 Data Pipeline Bible audit's job)" listed as a sub-dependency. The operator memory file flags them as related-but-distinct concerns in two separate verbatim quotes.

**Candidate reframing 1 — STAND-ALONE (drafting-CC default per Drafting Spec).** Two W.N entries (§ 8.W.1 + § 8.W.2). Substrate that supports stand-alone:
- Different code paths in `hrn_scraper.py` (lines 802-804 vs lines 814-820).
- Different page tables affected (results table vs pool table).
- Different positional indices used (`parse_payout(1)/(2)/(3)` vs `cells[0]/cells[2]`).
- DIFFERENT root cause is plausible: an HRN page change might affect the results table (where icon column was added) but not the pool table (which may have unchanged structure). Substrate verification of the live HRN page is required to confirm.
- PHASE_5_BACKLOG.md operator memory file flags them with two separate verbatim quotes.

**Candidate reframing 2 — COLLAPSE.** Single W.N entry (§ 8.W.1) with adjacent prose covering pool extraction manifestation. Substrate that supports collapse:
- Same defect CLASS (positional column indexing without column-header verification).
- Both prevented by the same § 5.1 candidate Forbidden Pattern.
- PHASE_5_BACKLOG.md tracks them as a single Phase 5.3.1 item; bible-side single-W.N would parallel the backlog framing.
- Operator memory file's "likely has the same root cause" framing suggests operator-side hypothesis of identity.

**Drafting-CC disposition.** Default per Drafting Spec: BOTH § 8.W.1 + § 8.W.2 entries stand as separate. § 8.W.2 Bug #N field marked `[Bug #N TBD — pending QB ratification post-substrate verification]` per § 5.5.1 monotonic rule (drafting CC does NOT assign a new global Bug #N). FRAMEWORK_GAP F.1 (this entry) is the routing primitive for QB → Tony ratification per Lesson § 4.8: QB synthesizes; Tony ratifies; bible patches accordingly post-ratification. (historical — superseded by closure note above; the post-patch bible marker form is "[Bug #N TBD — pending Phase 5.3.1 fix-time substrate verification]" per Tony's Option 3 ratification 2026-05-06.)

**Routing.** QB review pass is light surface review only per AUDIT_METHODOLOGY § 4.9. Audit-CC's adversarial pass may surface additional substrate observations; QB synthesizes; Tony ratifies the collapse-or-stand decision before bible locks per AUDIT_METHODOLOGY § 4.8.

**Closure (Tony ratification, 2026-05-06):** Option 3 (defer disposition to Phase 5.3.1 fix-time substrate). § 8.W.2 stands as separate entry at lock with explicit deferral framing added per surgical patch operation 2 in this cycle. Bug #N assignment AND collapse-vs-stand decision both deferred to Phase 5.3.1 fix-time substrate verification. Bible re-ratifies via patch cycle when fix lands. Substrate-grounded honest state preserved at lock per META_PLAN v9 § 2.1; no speculation about root-cause identity at lock time.

### F.2 / F.3 cross-references (inherited from Database & Schema Bible v1)

The F.2 (`wr_predictions` + `pl_predictions` out-of-band ALTER columns) and F.3 (`ls_predictions` dual-write pattern) cross-references are not new gaps surfaced by this bible — they are inherited substrate observations from `database_schema_bible:4.1.12` + `:4.1.13` + `:4.1.14`. This bible's § 4.1.5 carries the flow-context cross-reference per the Drafting Spec § 4.1.5 prescription. Substantive description remains at the database_schema_bible canonical home. Phase 5 disposition for both inherits the `Phase 5.X.Y` placeholder per META_PLAN v9 Appendix A lead-paragraph scope clause (placeholder resolves when those specific entries land in PHASE_5_BACKLOG.md as separate triage queue entries).

### F.4 <FRAMEWORK_GAP: angle_stats table created out-of-band; not in `database_schema_bible:3.1` enumeration; not in any tracked migration file>

**Substrate (audit-CC v1-patched audit finding A3, 2026-05-06):**

```
$ grep -n -i "angle.stats\|angle_stats" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
EXIT_CODE=1   (zero matches)

$ grep -rn "angle_stats" /home/strakajagr/projects/equine-equalizer/backend/database/
EXIT_CODE=1   (zero matches in schema.sql + 12 migration files)

$ grep -n "angle_stats" /home/strakajagr/projects/equine-equalizer/backend/lambdas/ingestion/handler.py | head -10
93:    # ── Refresh angle_stats table ──
94:    if action == 'refresh_angle_stats':
98:                    cur.execute("DELETE FROM angle_stats")
100:                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
112:                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
123:                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
136:                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
147:                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
165:                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
181:                    cur.execute("SELECT COUNT(*) as cnt FROM angle_stats")
```

**Reframing candidate (CC-presented; substrate-cited):** `angle_stats` table is created out-of-band (no tracked migration file declares it; no schema.sql entry). Production handler at `backend/lambdas/ingestion/handler.py:94+` extensively references it (1 DELETE + 6 INSERTs + 1 SELECT COUNT(*) per substrate above). Structurally analogous to D&S Bible v1's F.2 substrate gap (out-of-band ALTER on `wr_predictions`/`pl_predictions`) but worse — `angle_stats` is the WHOLE TABLE created out-of-band, not just columns added to a tracked table.

**Resolution requested from QB / Tony:** UPSTREAM-CORRECTION routed to Database & Schema Bible patch cycle. D&S Bible v1-patched-d2 patch (separate cycle from this bible's re-lock) adds `angle_stats` to § 3.1 14-table enumeration → 15-table enumeration AND adds new sub-section at § 4.1.X documenting the table substrate (column list, primary key, UNIQUE/FK/index declarations, JSONB if any, primary writer = `equine-ingestion` Lambda's `refresh_angle_stats` admin action handler, primary readers TBD per D&S Bible substrate verification).

**Substrate citation supporting the reframing:** the grep output above (zero matches in tracked schema, 10+ references in production handler).

**Substrate citation refuting the alternative "angle_stats is in the schema and audit missed it":** N/A — substrate is conclusive; the table is out-of-band.

**Tony ratification 2026-05-06:** Tony ratified Option A on 2026-05-06 per QB synthesis of audit-CC v1-patched audit. F.4 stands open in this bible's verification log; UPSTREAM-CORRECTION queued for D&S Bible v1-patched-d2 separate patch cycle. This bible re-locks at v1-patched-a with F.4 marker present; F.4 closes when D&S Bible patches and this bible's § 4.1.7 cross-reference re-ratifies via subsequent patch.

**UPSTREAM-CORRECTION close (2026-05-06):** D&S Bible v1-patched-d2 LOCKED 2026-05-06 landed `angle_stats` substrate at `database_schema_bible:4.1.15` (column list + Currently Open entry + revision history bullet). This bible's § 4.1.7 destination-table cross-reference re-ratifies via this patch cycle (Data Pipeline Bible v1-patched-c, 2026-05-06) to point at the new `database_schema_bible:4.1.15` slot. F.4 status: **CLOSED at lock (UPSTREAM-CORRECTION resolved)**. Substrate-grounded honest disposition: column substrate is asserted-from-INSERT-tuples per D&S Bible PHASE 1 Approach B fallback; PK/FK/INDEX substrate is asserted-disposition-pending-credential-authorized-cycle per D&S Bible § 4.1.15 substrate-disposition framing. Formalization-via-migration is Phase 5 backlog scope per `database_schema_bible:6` Currently Open entry — does not block F.4 closure here; F.4's scope was the cross-reference resolution at D&S Bible side, which D&S Bible v1-patched-d2 closed.

### No additional FRAMEWORK_GAP / SPEC_GAP markers

Beyond F.1 (closed v1-patched per Tony's Option 3 ratification 2026-05-06; closure note above) + F.2 / F.3 (inherited cross-references from D&S Bible) + F.4 (this entry; UPSTREAM-CORRECTION pending D&S Bible patch), no additional gaps surfaced during substrate verification, bible authoring, or v1-patched-a surgical patch.

---

## Section G — v1-patched audit-CC findings closure verification

11 entries (G-A1 through G-A11) — 1 per audit-CC v1-patched audit finding. Format per entry: finding ID + severity + one-line summary + patch operation reference + post-patch substrate evidence + closure verification.

### G-A1: BLOCKER — V1-9 fabricated verbatim content
- Patch operation: Operation 10.
- Post-patch substrate evidence: V1-9's third verbatim-output block now contains actual `sed -n '538,565p' backend/lambdas/ingestion/handler.py` raw stdout per Operation 10 paste; the fabricated `'body': json.dumps({` nested-dict structure removed.
- Closure verification: Operation 10's "Verbatim output" block at this verification log now matches fresh `sed` re-run; bible § 4.1.3 conclusion (chart parser invoked via `parse_charts` admin action) remains substrate-correct, so no SUB-FINDING surfaced.
- Closure status: **CLOSED**.

### G-A2: MATERIAL — Surgical patch did not propagate post-patch state to all narrative-referencing sections (Check 7 inheritance)
- Patch operations: Operations 13 + 14 + 15.
- Post-patch substrate evidence: Section E now asserts post-patch marker form (Operation 13); Section F.1 historical record clarified as historical (Operation 14); Section C grep totals refreshed (Operation 15: `Phase 5.3.1` count 22→26; `architecture_overview:` 74→76; `database_schema_bible:` 27→29; bible line count 574→583).
- Closure verification: `grep -c "pending QB ratification post-substrate verification" data_pipeline_bible_v1_verification.md` returns 1 (the historical Section F.1 line, now annotated as historical). `grep -c "pending Phase 5.3.1 fix-time substrate verification" data_pipeline_bible_v1_verification.md` returns ≥ 1 (the post-patch Section E + bible cross-references).
- Closure status: **CLOSED**.

### G-A3: MATERIAL — angle_stats substrate gap (UPSTREAM-CORRECTION class)
- Patch operation: Operation 4 (bible § 4.1.7 destination-table cross-reference) + new FRAMEWORK_GAP F.4 added to verification log Section F (Operation 17).
- Post-patch substrate evidence: bible § 4.1.7 destination-table now cites FRAMEWORK_GAP F.4; verification log § F.4 documents the substrate gap with substrate-cited candidate reframings; UPSTREAM-CORRECTION routed to D&S Bible patch cycle (separate cycle from this bible's lock).
- Closure verification: bible § 4.1.7 + verification log § F.4 substrate-grounded; angle_stats-in-bible-only-as-FRAMEWORK_GAP discipline operative.
- Closure status: **CLOSED in this bible's scope** (UPSTREAM-CORRECTION pending in D&S Bible patch cycle; not blocking this bible's re-lock).

### G-A4: MATERIAL — V1-1 + V1-15 ellipsis-truncated rows
- Patch operations: Operations 11 + 12.
- Post-patch substrate evidence: V1-1 ENABLED table now contains full verbatim rows from `architecture_overview:3.6` per Operation 11 paste (10 rows, no `…` truncation; full Cross-reference column content preserved). V1-15 DISABLED table re-confirmed as already full-row (no truncation in v1 cycle); Operation 12 closure clause noted in entry.
- Closure verification: Manual review of V1-1 table block confirms all 10 ENABLED rows now end at the closing `|` of the Cross-reference cell, no `…` ellipsis. V1-15 paste unchanged; was already full per v1 substrate.
- Closure status: **CLOSED**.

### G-A5: MATERIAL — § 4.2.1 + § 4.2.3 + § 4.2.4 empirical-discipline violation
- Patch operations: Operations 5 + 6 + 7. PHASE 1 Empirical Check 1 + Empirical Check 2 verbatim output incorporated.
- Post-patch substrate evidence: bible § 4.2.1 cites `counts.entries = 198390` + `latest_date = 2026-05-03` + 3-day-gap ASSERTION_CLAUSE (Op 5). Bible § 4.2.3 cites dashboard-does-NOT-expose-counts.workouts + asserted-from-Bug-#7-fallback (Op 6). Bible § 4.2.4 cites Lambda-Active + NYRA-endpoint-HTTP-200 + dashboard-does-NOT-expose-counts.workouts caveat (Op 7).
- Closure verification: each entry cites either (a) PHASE 1 verbatim output OR (b) explicit asserted-not-empirical qualification with a documented reason; no entry asserts "verified empirically" without substrate or assertion-clause caveat.
- Closure status: **CLOSED**.

### G-A6: MATERIAL — Phase 5.3.1 count drift (subsumed under A2)
- Patch operation: Operation 15.
- Post-patch substrate evidence: Section C grep totals refreshed; Phase 5.3.1 count now reflects v1-patched-a state (26).
- Closure status: **CLOSED**.

### G-A7: MINOR — V1-2 line citation off-by-one
- Inline sub-operation executed: V1-2's "Verbatim 5 task family rows (lines 92-97)" line corrected to "lines 92-96" per audit-CC observation that line 97 is the post-table blank/separator, not a data row.
- Closure status: **CLOSED**.

### G-A8: MINOR — § 4.1.3 chart parser line range
- Patch operation: Operation 3 (bible). Replaced both occurrences of `handler.py:540-558` with `handler.py:542` entry (Check 8 line-shift-resistant lesson; tighter scope to entry-line citation only).
- Closure status: **CLOSED**.

### G-A9: MINOR — § 3 "7 Lambdas" framing
- Patch operation: Operation 2 (bible). Restructured to lead with per-State decomposition: "across 5 Active Lambdas + 2 of the 3 INACTIVE Lambdas (... ) — 7 of the 8-Lambda inventory at architecture_overview:3.1".
- Closure status: **CLOSED**.

### G-A10: STYLE — V1-10 drafter's working notes
- Inline sub-operation executed: V1-10's parenthetical working-notes content `(empty — exit code 0 → matches in 0 lines? Actually grep -r returns exit code 1 with no matches; pasting the exact stdout below)` stripped; replaced with `<empty stdout; grep exit code 1 — zero matches>` per AUDIT_METHODOLOGY § 4.10 verbatim-paste discipline.
- Closure status: **CLOSED**.

### G-A11: STYLE — § 3 fire-and-fail flow ordering
- Patch operation: Operation 1 (bible). Restructured § 3 line 79 prose to put rule list and subsection citations in TOC-monotonic order: 4 rules now flow as `equine-ingestion-daily` and `equine-fetch-results-nightly` (target equine-ingestion); `equine-results-daily` (target equine-results); `equine-angle-stats-nightly` (target equine-ingestion with refresh_angle_stats Input). Subsection list `§ 4.1.1, § 4.1.2, § 4.1.6, § 4.1.7 respectively` is now monotonic.
- Closure status: **CLOSED**.

**Section G summary:** 11 of 11 audit-CC v1-patched findings CLOSED in v1-patched-a. 1 BLOCKER closed (G-A1). 5 MATERIAL closed (G-A2 / G-A3 in-this-bible-scope / G-A4 / G-A5 / G-A6). 3 MINOR closed (G-A7 / G-A8 / G-A9). 2 STYLE closed (G-A10 / G-A11). Threshold per META_PLAN v9 § 11: zero fabricated content (closed via G-A1) + zero methodology-interpolation findings (audit-CC reported zero) + < 5 MATERIAL findings (4 distinct MATERIAL + 1 subsumed = 4; closed via G-A2/A3/A4/A5/A6) + zero un-closed prior-cycle findings (closed). v1-patched-a is pre-re-audit.

---

## Section H — QB self-audit log entries (reproduced char-exact from Drafting Spec § 6)

The 9 entries below reproduce char-exact the Drafting Spec § 6 entries H1 through H9 per QB handoff § 7.2 + Drafting Spec § 5 verification log structure.

### H1 — Check 1 (cross-reference accuracy) self-audit

**Cross-references prescribed in this spec verified against substrate:**

- BIBLE_STRUCTURE_SPEC v6 § 6.2 → verified by QB direct read 2026-05-06; section spans from `### 6.2 data_pipeline_bible.md` header to `### 6.3 feature_provenance_bible.md (FF1)` header. Per-section guidance read in full.
- BIBLE_STRUCTURE_SPEC v6 § 5.3 (cross-cutting bug scope rule) → verified.
- BIBLE_STRUCTURE_SPEC v6 § 5.5 + § 5.6 → verified.
- BIBLE_STRUCTURE_SPEC v6 § 5.5.1 (global Bug #N convention) → verified.
- BIBLE_STRUCTURE_SPEC v6 § 5.7 (candidate roster workflow) → verified.
- META_PLAN v9 § 4.5 → verified.
- META_PLAN v9 § 6.5 → verified.
- META_PLAN v9 § 7.3 placeholder-resolution sub-rule → verified; locked v7.
- META_PLAN v9 § 7.9 Data Acquisition Honesty Protocol → verified.
- META_PLAN v9 Appendix A.5 Bug #28 worked example → verified.
- AUDIT_METHODOLOGY v2 § 4.8 / 4.9 / 4.10 / 4.11 → verified at primary source 2026-05-06; slot numbers match handoff per Lesson 3 expansion.
- Architecture Overview § 3.1 (Lambda inventory + V3-2 25-action sub-citation + default-case dispatch) → verified.
- Architecture Overview § 3.2 (5 ECS task families) → verified.
- Architecture Overview § 3.6 (13 EventBridge rules + per-rule targets + 4 fire-and-fail anomaly) → verified.
- Architecture Overview § 4.2 (per-pipeline prediction shapes + WR dynamic attribute attachment) → verified.
- Architecture Overview § 5.1 + § 5.2 (Forbidden Pattern + Common Mistake governing § 4.1.X documentation discipline) → verified.
- Architecture Overview § 6 (fire-and-fail anomaly canonical home) → verified.
- Database & Schema Bible § 4.1 (per-table sub-sections; F.2 at 4.1.12 + 4.1.13; F.3 at 4.1.14) → verified.
- PHASE_5_BACKLOG.md Phase 5.3.1 entry → verified by QB direct read 2026-05-06.

### H2 — Check 2 (count/arithmetic accuracy) self-audit

**Counts decomposed per META_PLAN v9 § 6.5 verification log precision rule:**

- 13 EventBridge rules = 10 ENABLED + 3 DISABLED. ENABLED decomposition: 4 fire-and-fail (3 → equine-ingestion: ingestion-daily + fetch-results-nightly + angle-stats-nightly; 1 → equine-results: results-daily) + 4 active-Lambda (ls-inference-daily, nyra-workouts-daily, pl-inference-daily, wr-inference-daily) + 2 ECS (daily-retrain-full, weekly-retrain-wr). 4+4+2=10. DISABLED: feature-engineering-daily, inference-daily, weekly-retrain-pl. 10+3=13.
- 9 § 4.1 sub-sections per § 6.2 prescribed TOC. EventBridge rule cardinality per sub-section: 1+1+0+1+3+1+1+1+1=10 (matches 10 ENABLED). § 4.1.5 holds 3 rules (WR/PL/LS); § 4.1.3 holds 0 direct EventBridge rules (chart parser trigger TBD per V1-9).
- 5 ECS Fargate task families: equine-training, equine-training-daily-full, equine-training-manual, equine-training-pl, equine-training-win-prob.
- 6 Data Acquisition Honesty sources per § 6.2: HRN entries, HRN results, HRN workouts, NYRA workouts, Equibase chart parser, equibase_probe/.
- 25 action handlers on equine-ingestion = 5 data acquisition + 4 model lifecycle + 5 admin/diagnostic + 7 data backfills/ops + 3 originally-cited admin + 1 health (per Architecture Overview § 3.1 V3-2 sub-citation).

Single-source citation: each count statement above traces to a specific upstream-locked verification log claim or this spec's V1-N. No multi-paraphrase counts.

### H3 — Check 3 (substrate-grounded reframing) self-audit

**Reframings introduced in this spec are substrate-grounded:**

- Bug #28 canonical home in this bible per BIBLE_STRUCTURE_SPEC v6 § 5.3 (data-acquisition discipline most directly prevents recurrence) — verified by QB direct read of § 5.3 + META_PLAN v9 Appendix A.5.
- § 8.W.1 + § 8.W.2 default to separate entries per § 6.2 + Tony's Item 2 ratification 2026-05-05 — verified by QB read of handoff document Item 2 ratification.
- Phase 5.3.1 real identifier (NOT placeholder) per S.1 ratification — verified by QB direct read of PHASE_5_BACKLOG.md (file exists; Bug #28 entered at Phase 5.3.1).
- Fire-and-fail anomaly canonical home is `architecture_overview:6` (cross-runtime invariant); this bible's § 6 carries one-line cross-reference per S.4 ratification — verified by QB direct read of Architecture Overview § 5.1 + § 5.2 + § 6.
- F.2 + F.3 cross-references at § 4.1.5 daily inference flow per S.6 ratification — verified by QB direct read of database_schema_bible:4.1.12 + § 4.1.13 + § 4.1.14 substrate.
- § 4.1.5 holds 3 EventBridge rules (WR/PL/LS) under one § 4.1 sub-section per § 6.2 prescribed TOC; § 4.1.3 chart parser holds 0 direct EventBridge rules (trigger TBD per V1-9) — verified by QB direct read of § 6.2 + cross-mapping to Architecture Overview § 3.6.

### H4 — Check 4 (definition-framing internal consistency) self-audit

**Definitions and enumerations reconcile internally:**

- § 2 Definitions enumerated terms (HRN, NYRA, Equibase chart, qualifying track, default-case dispatch, fire-and-fail) match § 4.1 sub-section content (HRN sources at 4.1.1/4.1.2/4.2.1/4.2.2/4.2.3; NYRA at 4.1.4/4.2.4; Equibase chart at 4.1.3/4.2.5; default-case dispatch at 4.1.1/4.1.2; fire-and-fail at 4.1.1/4.1.2/4.1.6/4.1.7).
- 10 ENABLED EventBridge rules in § 4.1 reconcile with 10 ENABLED in Architecture Overview § 3.6 (4+4+2 decomposition); 3 DISABLED rules at § 7 reconcile with 3 DISABLED in Architecture Overview § 3.6.
- 9 § 4.1 sub-sections reconcile with § 6.2 prescribed TOC; § 4.1.5 cardinality of 3 rules + § 4.1.3 cardinality of 0 direct rules sum to 10 ENABLED across 9 sub-sections (1+1+0+1+3+1+1+1+1=10).
- § 4.2 Data Acquisition Honesty 6 sources reconcile with § 6.2 prescribed TOC.

No internal contradiction between § 2 / § 4.1 / § 4.2 enumerations.

### H5 — Check 5 (synthesis verification) self-audit

**Synthesis-introduced upstream corrections substrate-verified:**

- The handoff cross-reference inaccuracies (PHASE_5_BACKLOG.md non-existence; Check 7 + Check 8 enumeration completeness) are surfaced as QB-side findings (§ 10) NOT propagated as upstream corrections to META_PLAN v9 / Architecture Overview / Database & Schema Bible. Per Lesson 6: substrate-verified at QB direct read.
- Bug #28 canonical-home assignment inherited from META_PLAN v9 § 1.2 + Appendix A.5 + BIBLE_STRUCTURE_SPEC v6 § 5.3 — QB substrate-verified.
- Fire-and-fail anomaly canonical home assignment inherited from Architecture Overview § 6 self-assignment (per § 5.1 + § 5.2 ratifications) — QB substrate-verified.
- F.2 + F.3 cross-reference targets (database_schema_bible:4.1.12 + § 4.1.14) — QB substrate-verified.
- § 5 candidate Common Mistake (producer-side parent-row verification) inherited from D&S Bible Q3.3.c forward-deferral note at database_schema_bible.md § 5 lead paragraph — QB substrate-verified.

### H6 — Check 6 (audit-CC enumeration completeness) self-audit

**Audit-CC enumeration inherited inventory per Check 6:**

- v1 first cycle has no prior audit-CC findings to inherit. Forward-looking: when v2 audit-CC enumerates findings, QB substrate-verifies each via grep before re-spec.
- For inherited substrate from upstream Phase 1 deliverables (Architecture Overview v3 + D&S Bible v1): QB direct read confirms Architecture Overview § 3.6 13-rule × per-rule-target verification (locked Lesson 5 inheritance), § 3.1 25-action V3-2 sub-citation, D&S Bible F.2 + F.3 substrate. No drift surfaced at spec-authorship.

### H7 — Check 7 (mid-cycle scope extensions) self-audit

**No mid-cycle scope extensions in this spec.** The spec authors v1 in a single pass. Forward-looking: if v2/v3 cycles extend scope post-CC-surfacing, QB enumerates ALL verification-log + main-doc sections referencing original scope and updates each per Check 7 discipline (banked Architecture Overview v3 H7).

For this v1 spec specifically, the spec is the initial scope; no Section H/I sub-section updates required.

### H8 — Check 8 (line-shift-resistant citations) self-audit

**Line-number citations replaced with section-anchored citations:**

- `architecture_overview:3.1` for Lambda inventory cross-references, NOT Architecture Overview line numbers.
- `architecture_overview:3.2` for ECS task families.
- `architecture_overview:3.6` for EventBridge schedule + per-rule targets.
- `architecture_overview:5.1` + `architecture_overview:5.2` for Forbidden Pattern + Common Mistake governance.
- `architecture_overview:6` for fire-and-fail anomaly canonical home.
- `database_schema_bible:4.1.<table>` for per-table cross-references.
- `database_schema_bible:4.1.12` + `database_schema_bible:4.1.13` for F.2 cross-reference targets.
- `database_schema_bible:4.1.14` for F.3 cross-reference target.
- BIBLE_STRUCTURE_SPEC `v6 § 6.2` (section anchor).
- META_PLAN `v9 § 4.5` / `v9 § 6.5` / `v9 § 7.3` / `v9 § 7.9` / Appendix A.5.
- AUDIT_METHODOLOGY `§ 4.8` / `§ 4.9` / `§ 4.10` / `§ 4.11`.

Literal line numbers retained ONLY where canonical-substrate identification requires them:
- `hrn_scraper.py:802-804` — Bug #28 column-shift defect surface; canonical-substrate identification per the v3 final-lock H8 lesson scope.
- `hrn_scraper.py:814` — Bug #28 DD pool nuance; canonical-substrate identification.
- `backend/lambdas/ingestion/handler.py:94` — refresh_angle_stats handler; canonical-substrate identification per Architecture Overview § 3.1 + § 3.6 inheritance.
- `backend/lambdas/ingestion/handler.py:1669-1680` — default-case dispatch path per Architecture Overview § 3.1 V3-2 inheritance; canonical-substrate identification.
- `wr_inference_service.py:718-730` — dynamic attribute attachment block per Architecture Overview § 4.2 inheritance; canonical-substrate identification.
- `ls_inference_service.py:388-401` — dual-write substrate per database_schema_bible:4.1.14 F.3 inheritance; canonical-substrate identification.
- Migration file paths cite the filename, not line numbers.

Cross-references between bibles use section IDs only; canonical-substrate citations to source code may include line numbers when tightly scoped.

### H9 — Check 9 (bash-grep verification predictions) self-audit

**Prescribed bash-grep predictions distinguish targeted vs total counts:**

Per spec § 7 "Bash-grep verification predictions (Check 9 precision)":
- `grep -c "Bug #28" data_pipeline_bible.md` (post-draft) → expected total ≥ 2; targeted-by-this-draft: ≥ 2.
- `grep -c "Phase 5.3.1" data_pipeline_bible.md` (post-draft) → expected ≥ 1; targeted: ≥ 1.
- `grep -c "Phase 5.X.Y" data_pipeline_bible.md` (post-draft) → expected ≥ 0; targeted: 0–2.
- `grep -c "fire-and-fail" data_pipeline_bible.md` (post-draft) → expected ≥ 5; targeted: ≥ 5.
- `grep -c "architecture_overview:" data_pipeline_bible.md` (post-draft) → expected ≥ 20; targeted: ≥ 20.
- `grep -c "database_schema_bible:" data_pipeline_bible.md` (post-draft) → expected ≥ 10; targeted: ≥ 10.
- `ls backend/services/data_sources/` → expected: directory listing.
- `grep -c "parse_payout" backend/services/data_sources/hrn_scraper.py` → expected ≥ 3.

Each prediction precisely scopes the pattern. Per AUDIT_METHODOLOGY § 4.11: this spec's grep targets are mostly single-file substrate reads; multi-file unions enumerate distinct-occurrence-count + on-disk-match-count where applied.

---

## Section I — New entries for surgical patch operations

NOT APPLICABLE for v1 (first cycle is full draft, not surgical patch).

---

## End of Data Pipeline Bible v1 Companion Verification Log
