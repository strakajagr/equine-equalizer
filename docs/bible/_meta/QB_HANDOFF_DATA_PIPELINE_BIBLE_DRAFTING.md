# QB Handoff: Data Pipeline Bible Drafting Spec Authorship

**Document:** QB_HANDOFF_DATA_PIPELINE_BIBLE_DRAFTING
**Phase:** 1 deliverable 3 of 7 preparation
**Status:** ACTIVE handoff for fresh QB session
**Author:** QB (Database & Schema Bible cycle, 2026-05-05)
**Date:** 2026-05-05

**Purpose:** Comprehensive context handoff from the Database & Schema Bible Phase 1 cycle (LOCKED 2026-05-05) to the fresh QB session beginning Data Pipeline Bible drafting spec authorship as Phase 1 deliverable 3 of 7 per BIBLE_STRUCTURE_SPEC v6 § 8.2 drafting order. Captures: methodology state, lock state, banked failure modes, standing process patterns, lessons banked across two Phase 1 cycles, and Data Pipeline Bible-specific drafting context. The fresh QB session opens this document FIRST before any other work.

---

## 1. Phase 0 / Phase 1 substrate state (as of 2026-05-05)

### 1.1 Phase 0 LOCKED deliverables

5 of 5 Phase 0 methodology documents LOCKED (unchanged from prior handoff):

- **META_PLAN v9** (LOCKED 2026-05-05) at `_meta/META_PLAN.md`. Companion log at `_audits/META_PLAN_v9_verification.md`.
- **BIBLE_STRUCTURE_SPEC v6** (LOCKED 2026-05-05) at `_meta/BIBLE_STRUCTURE_SPEC.md`. Companion log at `_audits/BIBLE_STRUCTURE_SPEC_v6_verification.md`.
- **AUDIT_METHODOLOGY** (LOCKED v2-patched 2026-05-05) at `_meta/AUDIT_METHODOLOGY.md`. The Database & Schema Bible cycle banked 4 new lessons at sequential § 4.X slots (per the file's § 4.X = Lesson X convention; § 4.8 / § 4.9 / § 4.10 / § 4.11 per patch-CC's surface during D-3.1 BLOCKER fix cycle). Fresh QB verifies actual slot numbers via primary-source read at spec-authorship time per Lesson 3 expansion (convention identifiers requiring primary-source verification).
- **CONVERGENCE_CRITERIA v2** (LOCKED 2026-05-04) at `_meta/CONVERGENCE_CRITERIA.md`.
- **TRIAGE_QUEUE_SPEC v1** (LOCKED 2026-05-04) at `_meta/TRIAGE_QUEUE_SPEC.md`.

### 1.2 Phase 1 progress

- **Deliverable 1 of 7 — Architecture Overview:** LOCKED v3 2026-05-05. 3-cycle audit history. Companion verification log at `_audit/architecture_overview_v3_verification.md`.
- **Deliverable 2 of 7 — Database & Schema Bible:** LOCKED v1-patched-d1 2026-05-05. Cycle: full draft → audit (1 BLOCKER + 5 MATERIAL + 3 MINOR) → surgical patch closing 9 findings → re-audit (1 MINOR D-1) → 1-line opportunistic patch → lock. Companion verification log at `_audit/database_schema_bible_v1_verification.md` (1112 lines; 17 V1-N entries + 11 V1-patch-N entries + Section A inheritance + Section F F.1/F.2/F.3 markers + Section H char-exact reproduction).
- **Deliverable 3 of 7 — Data Pipeline Bible:** drafting spec authorship in progress (this fresh QB session's deliverable).
- **Deliverables 4-7:** not yet started; drafting order per BIBLE_STRUCTURE_SPEC v6 § 8.2.

### 1.3 Substrate corrections inherited from Phase 1 cycles 1 + 2

**META_PLAN v9 Aurora correction (cycle 1):** EE uses standalone RDS PostgreSQL 16.6 instance `equine-db`. Cross-project contamination (Aurora ARN bleeding from `fantasy-baseball-serverless`) caught and corrected. Database & Schema Bible cross-references `architecture_overview:3.3` for canonical RDS metadata.

**Bible v1 BLOCKER fix (cycle 2):** drafting CC reported `git log` output for migration 002 that primary-source verification refuted. Pattern: drafter reported `tail -1` output without actually running the command. Caught by audit-CC's independent re-run; fixed by surgical patch updating § 8.W.2 fix date from 2026-05-04 (baseline-commit fallback) to 2026-03-15 (`d93c4c4` descriptive commit). **Lesson banked at AUDIT_METHODOLOGY § 4.10 (verbatim-paste discipline; per patch-CC's report of slot assignment):** drafting CC must paste verbatim grep / git log / read command output for V1-N entries; summarization is fabrication-class risk. Operative discipline for Data Pipeline Bible cycle: every V1-N entry in the verification log pastes verbatim command output, not summarization.

---

## 2. Upstream-locked canonical references for Data Pipeline Bible

Data Pipeline Bible inherits canonical references from Architecture Overview v3 + Database & Schema Bible v1-patched-d1.

### 2.1 Architecture Overview canonical references (load-bearing for Data Pipeline)

- **§ 3.1 Lambda inventory:** 8 Lambdas = 5 Active + 3 INACTIVE. Active: `equine-inference`, `equine-wr-inference`, `equine-pl-inference`, `equine-ls-inference`, `equine-nyra-workouts`. INACTIVE: `equine-ingestion`, `equine-feature-engineering`, `equine-results`. Data Pipeline Bible's per-flow documentation (§ 4.1.X) cross-references `architecture_overview:3.1` for Lambda Active/INACTIVE state per flow.
- **§ 3.4 ECS Fargate task families:** 5 task families enumerated. Load-bearing for Data Pipeline § 4.1.8 + § 4.1.9 (daily/weekly retraining flows).
- **§ 3.6 EventBridge schedule:** 13 rules = 10 ENABLED + 3 DISABLED. Per-rule `aws events list-targets-by-rule` substrate verified (Lesson 5 non-negotiable). Data Pipeline Bible's per-flow documentation lives in this bible; `architecture_overview:3.6` is the inventory reference.
- **§ 6 Currently Open fire-and-fail anomaly:** 4 ENABLED EventBridge rules target 2 INACTIVE Lambdas (`equine-ingestion` + `equine-results`). Cross-cutting concern for Data Pipeline § 4.1 per-flow documentation: ingestion-side flows + results-fetch flow are currently impaired.

### 2.2 Database & Schema Bible canonical references (load-bearing for Data Pipeline)

- **§ 4.1.X per-table writers:** Database & Schema Bible documents primary writers per table, deferring per-flow data movement to `data_pipeline_bible:4.1`. Data Pipeline Bible inverts the cross-reference: per-flow detail here, with cross-reference to `database_schema_bible:4.1.X` for table-level schema.
- **§ 6 Currently Open Bug #28 cross-reference:** Database & Schema Bible § 6 cross-references `data_pipeline_bible:#28` as canonical home. Data Pipeline Bible carries the substantive Bug #28 entry at § 8.W.<n>.
- **F.2 substrate gap (queued for PHASE_5_BACKLOG.md):** out-of-band ALTER TABLE script applied to production for `wr_predictions.style`, `wr_predictions.model_used`, `pl_predictions.style` columns; not preserved as a tracked migration. Data Pipeline Bible may surface this as schema-history discipline gap; canonical home determination per § 5.3 cross-cutting bug scope rule.
- **F.3 substrate observation (queued for PHASE_5_BACKLOG.md):** LS cross-table read pattern — `ls_prediction_repository.py:262, 374` issue `FROM wr_predictions p`. Documented at `database_schema_bible:4.1.12` + `database_schema_bible:4.1.14`. Data Pipeline Bible may reference per-flow context where LS enrichment writes to `wr_predictions` columns rather than `ls_predictions`.

### 2.3 BIBLE_STRUCTURE_SPEC v6 § 6.2 prescribes the Data Pipeline Bible template

Located in BIBLE_STRUCTURE_SPEC.md (verify exact line range via primary-source read at spec-authorship time per Lesson 3 expansion). Key sections:
- § 1 Scope, § 2 Definitions (HRN, NYRA, Equibase chart, "qualifying track"), § 3 Pipeline overview, § 4 Pipeline detail (§ 4.1 Per-flow + § 4.2 Data Acquisition Honesty Protocol), § 5 Discipline rules, § 6 Currently Open, § 7 Deprecated, § 8 What Was Fixed (canonical home for Bug #28).
- § 4.1 enumerates 9 per-flow sub-sections (4.1.1 daily ingestion through 4.1.9 weekly retraining).
- § 4.2 enumerates 6 Data Acquisition Honesty Protocol sub-sections per source (HRN entries, HRN results, HRN workouts, NYRA workouts, Equibase chart parser, equibase_probe/).

---

## 3. Option 1 self-audit framework — 9 checks across 3 clusters

**Framework UNCHANGED from prior handoff.** Operating principle: QB performs all 9 substrate-grounded checks BEFORE sending any drafting spec to CC.

**Substrate verification cluster (Checks 1-3):** Cross-reference accuracy / Count-arithmetic accuracy / Substrate-grounded reframing.

**Content verification cluster (Checks 4-6):** Definition-framing internal consistency / Synthesis verification / Audit-CC enumeration completeness.

**Workflow verification cluster (Checks 7-9):** Mid-cycle scope extension narrative discipline / Line-shift-resistant citations / Bash-grep verification predictions distinguishing targeted vs total counts.

**Trajectory observation across two Phase 1 cycles:** Architecture Overview (cycle 1) and Database & Schema Bible (cycle 2) both completed without surfacing a NEW QB drafting-spec error class beyond the 10 banked. Option 1 with 9 checks is converging. Continue operating under the framework for Data Pipeline Bible cycle.

---

## 4. 10 banked QB drafting-spec errors (UNCHANGED from prior handoff)

Comprehensive enumeration across 3 audit cycles + META_PLAN v9 cycle. The 10 errors trace to Checks 1-9 across the 3 clusters. Method-validity self-check confirmed: each banked check passes the distinctness test against existing checks. No new QB drafting-spec error class surfaced in cycle 2 (Database & Schema Bible). The cycle 2 BLOCKER (D-3.1 fabricated git log output) was a CC-discipline error, not a QB drafting-spec error class.

(See prior handoff `QB_HANDOFF_DATABASE_SCHEMA_BIBLE_DRAFTING.md` § 4 for full enumeration with classifications.)

---

## 5. Methodology lessons (active discipline for Data Pipeline Bible cycle)

Lessons 1-6 from META_PLAN v9 + Architecture Overview cycles + Database & Schema Bible cycle 4 new lessons banked at AUDIT_METHODOLOGY § 4.X slots.

**Original Lessons 1-6 (UNCHANGED):**

- **Lesson 1** — Tier 6 verification mandate includes cross-project contamination check, not just freshness check.
- **Lesson 2** — Phase 1 verification surfaces Phase 0 substrate errors; surgical correction to Phase 0 documents is expected response.
- **Lesson 3 (re-expanded per Database & Schema Bible cycle):** Drafting specs cite primary verification log claim IDs, not paraphrased restatements. **Expansion 2026-05-05:** convention identifiers (lesson labels, section numbering schemes, file naming conventions) require primary-source verification at spec-authorship time. Specifically: when the drafting spec references "Lesson N" or "§ X.Y" of an upstream-locked document, QB reads the upstream document to confirm the actual label/numbering matches the spec's reference. Do NOT extrapolate from prior cycles or conversational vocabulary.
- **Lesson 4** — Any FRAMEWORK_GAP reframing in CC's draft requires substrate verification before CC asserts it.
- **Lesson 5** — EventBridge documentation cites `aws events list-targets-by-rule` output per rule, not `aws events list-rules` output alone. Target and State are independent AWS resources. **Particularly load-bearing for Data Pipeline Bible:** § 4.1 per-flow documentation depends on accurate cron-target mapping; 13 rules × 2 verification commands minimum.
- **Lesson 6** — QB synthesis of audit findings into upstream-correction scope requires substrate verification of upstream claim.

**New lessons banked at AUDIT_METHODOLOGY § 4.X (Database & Schema Bible cycle):**

Per patch-CC's report during D-3.1 BLOCKER fix, 4 new lessons banked at sequential § 4.X slots (§ 4.8 / § 4.9 / § 4.10 / § 4.11 per AUDIT_METHODOLOGY's existing § 4.X = Lesson X convention). Fresh QB verifies actual slot numbers via primary-source read of AUDIT_METHODOLOGY.md at spec-authorship time per Lesson 3 expansion. Substantive content (verify against primary-source for exact wording at spec-authorship):

- **AUDIT_METHODOLOGY § 4.8 (conversationally "Lesson 11"):** QB substrate findings during spec authorship require Tony ratification before spec content corrects them. QB does not unilaterally route findings to spec corrections, even when Lesson 6 indicates upstream documents don't need correction. Route is always: QB surfaces → Tony ratifies → spec executes. **Operative discipline for Data Pipeline Bible cycle:** any substrate finding QB surfaces during spec-authorship (e.g., handoff cross-reference inaccuracy, refuted claim) routes to Tony before spec body asserts the correction.

- **AUDIT_METHODOLOGY § 4.9 (conversationally "Lesson 12"):** QB review pass is light surface review only. Substrate verification is audit-CC's job in a fresh adversarial session. QB does NOT spot-check verification log entries against primary substrate; QB does NOT run greps to verify CC's claims; QB does NOT declare V1-N entries PASS. QB reads the draft, surfaces FRAMEWORK_GAP markers and any obvious anomalies, then specs audit-CC. **Operative discipline for Data Pipeline Bible cycle:** when CC delivers the draft + verification log, QB's review pass reads both fully, flags FRAMEWORK_GAP markers and architectural decisions for Tony, and produces the audit-CC paste-prompt. QB does not run substrate verifications during the review pass.

- **AUDIT_METHODOLOGY § 4.10 (conversationally "Lesson 13"; verbatim-paste discipline):** Drafting CC must paste verbatim grep / git log / read command output for V1-N entries; summarization is fabrication-class risk. **Operative discipline for Data Pipeline Bible cycle:** the drafting spec § 1.1 paste-prompt MUST require CC to paste verbatim command output for every V1-N entry. The cycle-2 BLOCKER (D-3.1 fabricated migration 002 git log) was the prototype failure mode; explicit verbatim-paste prevention is non-negotiable. Apply to git log, grep, sed, wc, diff, WebFetch, and any other command-output-based verification.

- **AUDIT_METHODOLOGY § 4.11 (prediction-precision lesson banked from F.1 ratification):** Future bible drafting specs that prescribe `grep` against `schema.sql` + `migrations/*.sql` should account for the schema.sql ↔ migration-001 byte-identity case (or analogous mirror-file cases) in V1-N grep predictions. **Operative discipline for Data Pipeline Bible cycle:** less directly applicable since Data Pipeline Bible substrate is mostly Lambda code + scraper code + EventBridge rules (not schema files), but the underlying discipline applies: V1-N grep predictions account for known mirror-file or duplicate-source cases.

---

## 6. Phase 1 cycle process (cycle 2 observations integrated)

### 6.1 Standard cycle steps (UNCHANGED)

1. **Spec authorship (QB):** under Option 1 with 9 checks operative; substrate verifications run before spec goes to CC.
2. **CC drafts + verification log:** char-exact reproduction discipline; Tier 3 mandatory companion log; Lesson § 4.10 verbatim-paste discipline operative for V1-N entries.
3. **QB reviews (light surface review per Lesson § 4.9):** reads draft + verification log fully; flags FRAMEWORK_GAP markers + architectural decisions for Tony; does NOT run substrate verifications.
4. **Audit-CC adversarial review:** fresh CC session; META_PLAN v9 § 6.2 six adversarial questions + Phase 1 checklist additions + lesson application correctness checks + threshold judgment.
5. **QB synthesizes findings (per Lesson § 4.8):** surfaces architectural decisions to Tony; does NOT unilaterally route findings to spec corrections.
6. **Tony ratifies; QB authors patch-spec; patch-CC executes.**
7. **Re-audit if BLOCKER fixed or > 5 findings absorbed; skip-audit if surgical-cosmetic per § 6.2 conditions.**
8. **Iterate to lock against Tony's threshold (META_PLAN v9 § 11).**

### 6.2 Skip-audit pre-approval pattern (UNCHANGED — 4 conditions)

Surgical-cosmetic patches qualify for skip-audit when ALL hold: scope confined to corrections + cosmetic improvements; char-exact reproduction discipline operative; zero new methodology constructs introduced; zero new substantive content beyond audit-finding closures.

**Cycle 2 observation:** the Database & Schema Bible cycle did NOT skip-audit the surgical-patch cycle covering 9 findings — that patch was substantive (BLOCKER fix + 5 MATERIAL + 3 MINOR + 1 new FRAMEWORK_GAP F.3) and triggered a fresh re-audit. Re-audit returned 1 MINOR (D-1 stale cross-reference); D-1 cleared by 1-line opportunistic patch without further re-audit (re-audit verdict was READY FOR LOCK regardless; D-1 was below threshold). The 1-line opportunistic patch IS skip-audit pattern (surgical-cosmetic; zero methodology touch; zero new content).

### 6.3 BLOCKER findings always trigger fresh adversarial review (UNCHANGED)

Cycle 2 BLOCKER (D-3.1) triggered re-audit; surgical-patch alone insufficient. Confirmed.

### 6.4 Tony's hard threshold (UNCHANGED, reaffirmed)

For LOCK AFTER MINOR REVISIONS path: zero fabricated content + zero methodology-interpolation + < 5 MATERIAL + zero un-closed prior-cycle findings.

### 6.5 Light surface review discipline (NEW from cycle 2)

Per AUDIT_METHODOLOGY § 4.9: QB review pass is light surface review only. Reads draft fully, eyeballs verification log, surfaces obvious red flags or FRAMEWORK_GAP markers. Does NOT run substrate verifications. Substrate verification is audit-CC's job. The cycle-2 review pass that violated this discipline (QB ran greps to spot-check 4-6 V1-N entries during review pass) banked the lesson; subsequent audit-CC pass was the corrective.

---

## 7. Standing CC paste-prompt patterns (UNCHANGED)

CC drafter paste-prompt boilerplate; CC verification log structure (Sections A through I); audit-CC paste-prompt boilerplate. See prior handoff `QB_HANDOFF_DATABASE_SCHEMA_BIBLE_DRAFTING.md` § 7 for full content. Operative addition: Lesson § 4.10 verbatim-paste discipline must appear explicitly in drafter paste-prompt (every V1-N entry pastes verbatim command output).

---

## 8. Data Pipeline Bible-specific drafting context

### 8.1 BIBLE_STRUCTURE_SPEC v6 § 6.2 prescribes the template

Located in `_meta/BIBLE_STRUCTURE_SPEC.md`. Fresh QB reads § 6.2 in full at spec-authorship time per Check 1 (cross-reference accuracy) + Lesson 3 expansion (verify section identifiers via primary source; do NOT extrapolate from this handoff's reference).

### 8.2 9 cron-triggered flows at § 4.1 (per BIBLE_STRUCTURE_SPEC v6 § 6.2)

Per § 6.2 prescribed sub-sections:
- 4.1.1 Daily ingestion (race cards) — `equine-ingestion-daily` cron
- 4.1.2 Nightly results fetch — `equine-fetch-results-nightly` cron
- 4.1.3 Chart parser (S3 PDFs → results enrichment)
- 4.1.4 NYRA workout scrape — `equine-nyra-workouts-daily` cron
- 4.1.5 Daily inference (3 separate Lambdas: WR / PL / LS)
- 4.1.6 Results matcher — `equine-results-daily` cron
- 4.1.7 Angle stats refresh — `equine-angle-stats-nightly` cron
- 4.1.8 Daily retraining — `equine-daily-retrain-full` cron
- 4.1.9 Weekly retraining — `equine-weekly-retrain-wr` cron

Each per-flow sub-section's mandatory + conditional content per § 6.2: trigger (cron expression), source, destination tables, Lambda(s) involved, action name(s) dispatched. Conditional: known failure modes, current impairment state (with cross-reference to `architecture_overview:3.1` Lambda State), canonical W.N home (Bug #28 for results flow), PHASE_5_BACKLOG.md references.

### 8.3 6 Data Acquisition Honesty Protocol entries at § 4.2 (per META_PLAN v9 § 7.9)

Per § 6.2:
- 4.2.1 HRN entries
- 4.2.2 HRN results
- 4.2.3 HRN workouts
- 4.2.4 NYRA workouts
- 4.2.5 Equibase chart parser path
- 4.2.6 `equibase_probe/` exploratory work

Each entry's mandatory + conditional content per § 6.2: what the source provides, current reliability state (verified empirically), failure manifestation, current acquisition mode, honest disposition.

### 8.4 Bug #28 canonical home (per § 5.3 cross-cutting bug scope rule)

Bug #28 (HRN scraper column-shift defect producing NULL `results.win_payout` and `results.daily_double_payout`) is canonically homed in Data Pipeline Bible's § 8.W.<n>. Database & Schema Bible § 6 cross-references `data_pipeline_bible:#28`. The substantive entry — Symptom (verbatim quote from operator memory), Root cause, Fix, Why-this-entry-exists, conditional triggers — lives here.

**Operator memory file:** `equine-equalizer-bug-28-hrn-scraper.md` (path verified at spec-authorship). The verbatim quote per META_PLAN v9 Claim 15c: "Place, show, and exacta payouts still populate." Substrate citations: `hrn_scraper.py:802-804` (per Claim 15) plus the DD pool extraction nuance at `hrn_scraper.py:814` (separate W.N if substrate verifies as same-root-cause; QB ratifies before drafter commits).

### 8.5 F.2 + F.3 inheritance from Database & Schema Bible (queued for PHASE_5_BACKLOG.md)

**F.2 substrate gap** — `wr_predictions.style`, `wr_predictions.model_used`, `pl_predictions.style` columns referenced by migration 011 + `pl_prediction_repository.py:272` ON CONFLICT but not declared in any tracked migration; out-of-band script applied to production. Documented at `database_schema_bible:4.1.12` + `database_schema_bible:4.1.13`. Tony ratified Option C for v1 lock + queue for PHASE_5_BACKLOG.md at Phase 0 exit. Data Pipeline Bible: surface if any flow's documentation references the substrate gap; cross-reference Database & Schema Bible's substrate prose; do NOT duplicate the gap description here.

**F.3 substrate observation** — LS cross-table read pattern: `ls_prediction_repository.py:262, 374` issue `FROM wr_predictions p`. Documented at `database_schema_bible:4.1.12` + `database_schema_bible:4.1.14`. Tony ratified R2.3.a + queue for PHASE_5_BACKLOG.md. Data Pipeline Bible: § 4.1.5 (daily inference flow) may surface this when documenting LS pipeline writes. The LS pipeline writes BOTH to `ls_predictions` (via `ls_inference_service.py:388-401`) AND to `wr_predictions` enrichment columns (the cross-table read substrate). Data Pipeline § 4.1.5 documents the writer-side flow; Database & Schema § 4.1.12 + § 4.1.14 document the reader-side substrate. Cross-reference; do not duplicate.

### 8.6 PHASE_5_BACKLOG.md creation at Phase 0 exit

Per META_PLAN v9 § 8.2: PHASE_5_BACKLOG.md gets created at Phase 0 exit with Bug #28 as first entry. As of Database & Schema Bible v1 lock (2026-05-05), PHASE_5_BACKLOG.md does NOT yet exist on disk. Queued entries pending creation: Bug #28 (first entry), F.2 (substrate gap), F.3 (cross-table read pattern). When PHASE_5_BACKLOG.md is created, these three entries land first.

**Implication for Data Pipeline Bible spec-authorship:** Data Pipeline Bible cross-references to PHASE_5_BACKLOG.md by phase number (e.g., "Phase 5.X.Y") use placeholder syntax until the backlog file exists. Per META_PLAN v9 Appendix A lead-paragraph scope clause, placeholder `Phase 5.X.Y` is acceptable when the specific PHASE_5_BACKLOG.md entry does not yet exist; placeholder resolves when the backlog file gains the entry. Same pattern as Database & Schema Bible § 7.1 used for legacy `predictions` table phase reference.

### 8.7 Cross-references from other bibles

- **From `architecture_overview:3.6`:** every EventBridge rule cross-references this bible's per-flow section. Data Pipeline § 4.1 is the canonical home for cron-flow runtime behavior.
- **From `database_schema_bible:4.1.5` (races) + § 4.1.6 (entries) + § 4.1.7 (past_performances) + § 4.1.9 (results):** primary-writer cross-references defer to `data_pipeline_bible:4.1` for per-flow documentation.
- **From `database_schema_bible:6` (Currently Open):** Bug #28 cross-reference points to `data_pipeline_bible:#28` canonical home.

### 8.8 Anchor verifications inherited from META_PLAN v9 verification log

(Re-verified at Architecture Overview v3 lock 2026-05-05; carry forward to Data Pipeline Bible cycle.)

| Inherited Claim | Used in Data Pipeline Bible § |
|---|---|
| Claim 3 (13 EventBridge rules, 10 ENABLED + 3 DISABLED) | § 3, § 4.1 (per-flow) |
| Claim 15 (Bug #28 line ref `hrn_scraper.py:802-804`) | § 8.W.<n> Bug #28 canonical |
| Claim 15c (Bug #28 per-payout decomposition + DD pool extraction nuance at `hrn_scraper.py:814`) | § 8.W.<n> + adjacent W.N if applicable |
| Claim 20 (5 ECS task families) | § 4.1.8 + § 4.1.9 retraining flows |

---

## 9. Substrate verifications required before Data Pipeline Bible spec authorship

QB substrate-verification overhead estimate: 30-45 min minimum (per Option 1 with 9 checks). Lesson 5 verification overhead is heaviest: 13 EventBridge rules × per-rule `aws events list-targets-by-rule` = 13 commands minimum.

### 9.1 Per Check 1 (cross-reference accuracy)

- BIBLE_STRUCTURE_SPEC v6 § 6.2 — full read for prescribed TOC + per-section guidance + cross-references
- META_PLAN v9 § 7.9 (Data Acquisition Honesty Protocol) — full read
- META_PLAN v9 § 7.4 (cross-cutting bug scope rule + W.N format) — full read for Bug #28 canonical home discipline
- BIBLE_STRUCTURE_SPEC v6 § 5.3 + § 5.5.1 — cross-cutting bug scope rule + global Bug #N convention
- AUDIT_METHODOLOGY.md § 4.X (slots § 4.8 / § 4.9 / § 4.10 / § 4.11 per patch-CC report; verify via primary-source read) — Lessons 11/12/13 + prediction-precision lesson actual content
- Architecture Overview § 3.1 + § 3.4 + § 3.6 + § 6 — Lambda inventory + ECS task families + EventBridge schedule + Currently Open fire-and-fail anomaly
- Database & Schema Bible § 4.1 per-table primary writers + § 6 Currently Open Bug #28 cross-reference
- Operator memory file `equine-equalizer-bug-28-hrn-scraper.md` — full read for verbatim quote substrate

### 9.2 Per Check 2 (count accuracy)

- 13 EventBridge rules — re-verify via `aws events list-rules` + per-rule `aws events list-targets-by-rule` (Lesson 5 mandate; 13 verification commands for targets + 1 for rule list = 14 minimum)
- 9 cron-triggered flows enumerated at § 4.1 — cross-check against the 13 EventBridge rules (10 ENABLED is the operative count for cron flows; 3 DISABLED rules don't fire; 9 § 4.1 sub-sections is the prescribed count per § 6.2 — surface any drift)
- 5 ECS task families — re-verify via `aws ecs list-task-definition-families` per Architecture Overview § 3.4 substrate
- 6 Data Acquisition Honesty Protocol sources at § 4.2 — re-verify HRN entries / HRN results / HRN workouts / NYRA workouts / Equibase chart / equibase_probe/ are all present in EE codebase

### 9.3 Per Check 3 (substrate-grounded reframing)

- Bug #28 verbatim symptom statement from operator memory file (per META_PLAN v9 Claim 15c) — re-verify via direct read of `equine-equalizer-bug-28-hrn-scraper.md`
- `hrn_scraper.py:802-804` line range — re-verify via direct read; confirm column-shift defect surface
- `hrn_scraper.py:814` DD pool extraction nuance — re-verify via direct read; substrate-determine whether same-root-cause (separate W.N or single W.N with adjacent prose)
- Per-flow Lambda + EventBridge mapping — re-verify per-rule via `aws events list-targets-by-rule` (Lesson 5 non-negotiable)

### 9.4 Per Check 4 (definition-framing internal consistency)

- § 2 Definitions vs § 4.1 + § 4.2 enumeration consistency — verify HRN / NYRA / Equibase chart / "qualifying track" definitions reconcile against § 4.1 per-flow + § 4.2 per-source enumerations

### 9.5 Per Check 5 (synthesis verification per Lesson 6)

- Audit-CC findings from Architecture Overview v3 + Database & Schema Bible v1 cycles that touch Data Pipeline scope — substrate-verify before propagating to Data Pipeline drafting spec
- F.2 + F.3 inheritance from Database & Schema Bible — substrate-verify via re-read of database_schema_bible.md § 4.1.12 + § 4.1.14 + verification log F.2 + F.3 entries before referencing in Data Pipeline drafting spec

### 9.6 Per Check 9 (bash-grep prediction precision)

- Each prescribed bash-grep verification scoped with discriminating context regex; not bare pattern counts
- For each predicted count, QB explicitly distinguishes targeted-by-this-patch vs total-on-disk-after-patch

### 9.7 Per Lesson 5 (load-bearing for Data Pipeline)

EventBridge documentation cites `aws events list-targets-by-rule` output PER RULE, not `aws events list-rules` output alone. Target State and Lambda State are independent AWS resources. Per-rule verification = 13 commands minimum. Apply at spec-authorship: QB substrate-verifies the 13-rule count + per-rule target mapping; verification log V1-N entries paste verbatim command output per Lesson § 4.10 verbatim-paste discipline.

### 9.8 Per Lesson § 4.10 verbatim-paste discipline (cycle-2 BLOCKER prevention)

Drafting spec's § 1.1 paste-prompt MUST require CC to paste verbatim grep / git log / read / aws / WebFetch command output for every V1-N entry. Summarization is fabrication-class risk. Cycle-2 BLOCKER (D-3.1 fabricated migration 002 git log) prototype: drafter reported `tail -1` output without running command. Explicit verbatim-paste prevention in spec authoring is non-negotiable.

---

## 10. Action sequence for fresh QB session

1. **Read this handoff document** at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/QB_HANDOFF_DATA_PIPELINE_BIBLE_DRAFTING.md` FIRST.
2. **Read Architecture Overview LOCKED state** at `/home/strakajagr/projects/equine-equalizer/docs/bible/architecture_overview.md` for § 3.1 + § 3.4 + § 3.6 + § 6 canonical references.
3. **Read Database & Schema Bible LOCKED state** at `/home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md` for § 4.1 per-table writers + § 6 Bug #28 cross-reference. Read companion verification log F.1 + F.2 + F.3 entries at `/home/strakajagr/projects/equine-equalizer/docs/bible/_audit/database_schema_bible_v1_verification.md`.
4. **Read AUDIT_METHODOLOGY.md** at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/AUDIT_METHODOLOGY.md` to verify § 4.X slot positions for Lessons 11/12/13/prediction-precision (per Lesson 3 expansion: convention identifiers verified at primary source).
5. **Read BIBLE_STRUCTURE_SPEC v6 § 6.2** at `/home/strakajagr/projects/equine-equalizer/docs/bible/_meta/BIBLE_STRUCTURE_SPEC.md` for the Data Pipeline Bible template.
6. **Read META_PLAN v9 § 7.9 + § 7.4** for Data Acquisition Honesty Protocol + cross-cutting bug scope rule.
7. **Read operator memory file** `equine-equalizer-bug-28-hrn-scraper.md` for Bug #28 substrate.
8. **Run substrate verifications** per Section 9 of this handoff (~30-45 min). Lesson 5 mandate: 13 EventBridge rules × per-rule targets verification.
9. **Author Data Pipeline Bible drafting spec** under Option 1 with 9 checks operative + Lessons 1-6 + AUDIT_METHODOLOGY § 4.8/4.9/4.10/4.11 active discipline + Lesson 3 expansion (convention identifiers verified at spec-authorship). Drafting spec § 6 H1-H9 QB self-audit log entries reproduced for traceability.
10. **Spec output target:** paste-ready CC paste-prompt for the drafting CC. CC drafts + produces verification log per Tier 3 mandate. Lesson § 4.10 verbatim-paste discipline operative for V1-N entries.
11. **Standard Phase 1 cycle process** applies: CC drafts → QB light surface review (Lesson § 4.9) → audit-CC adversarial pass → iterate to lock against threshold (META_PLAN v9 § 11).

---

## 11. Standing observations for AUDIT_METHODOLOGY future cycle

Per Tony's prior ratification (Database & Schema Bible cycle): AUDIT_METHODOLOGY meta-cycle queued for ~Phase 1 deliverable 5 or 6 of 7. Lessons get durable across 3-4 Phase 1 cycles before codification. Premature codification after 1 cycle was rejected; same applies after 2.

When AUDIT_METHODOLOGY next cycles, codify:
- 9-check Option 1 framework as formal "QB drafting-and-synthesis discipline" rules (banked across 3 audit cycles + 2 Phase 1 cycles)
- 3-cluster organization (Substrate / Content / Workflow)
- Method-validity self-check discipline (distinctness test for new banked checks)
- Pattern-completion check operative on letter-prefixes (W.N exclusivity)
- Skip-audit pre-approval 4-condition pattern formalized
- **Lesson 3 expansion to convention identifiers** (lesson labels, section numbering schemes, file naming conventions require primary-source verification at spec-authorship; banked from Database & Schema Bible cycle's "Lesson 11/12/13" labeling vocabulary mismatch with AUDIT_METHODOLOGY § 4.X slot numbering)
- **Lessons § 4.8 / § 4.9 / § 4.10 / § 4.11** (QB ratification routing + light surface review + verbatim-paste discipline + grep-prediction-precision-on-mirror-files) consolidation if drift surfaces across Phase 1 deliverables 3-7
- Cross-CC convergence test methodology empirically validated as Phase 0 closure mechanism (per BIBLE_STRUCTURE_SPEC v6 cycle's run3-vs-run4 divergence resolution)

10 banked QB drafting-spec errors with classifications + 4 Phase 1 cycle 2 lessons banked at AUDIT_METHODOLOGY § 4.X slots serve as the worked-examples corpus for the codification.

---

**End of QB Handoff: Data Pipeline Bible Drafting Spec Authorship.**

Fresh QB session opens this document, then proceeds to substrate verifications + spec authorship. Database & Schema Bible LOCKED 2026-05-05; Phase 1 cycle 3 begins.
