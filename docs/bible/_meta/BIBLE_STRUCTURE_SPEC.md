# BIBLE_STRUCTURE_SPEC.md

**Document:** BIBLE_STRUCTURE_SPEC
**Phase:** 0 (Methodology) — Phase 0 deliverable 2 of 5
**Status:** LOCKED v6 (2026-05-05)
**Author:** CC (drafting under verification discipline; QB orchestrated and reviewed)
**Date:** 2026-05-05
**Locked:** 2026-05-05

**Revision history:**
- v1 (2026-05-04): initial CC draft. Companion verification log at `_audits/BIBLE_STRUCTURE_SPEC_v1_verification.md`.
- v2 (2026-05-04): post-v1-audit surgical patch pass integrating Tony's five locked decisions (M-1 through M-5).
- v3 (2026-05-04): post-v2-audit surgical patch pass integrating Tony's three locked decisions (Findings 1, 2, 3). v2's structure preserved; sections without v2-audit findings against them retained unchanged. Companion verification log at `_audits/BIBLE_STRUCTURE_SPEC_v3_verification.md` inherits v2's 25 claims with re-verified-2026-05-04 timestamps and adds 2 new claims (N9 DD § 19 brevity confirmation; N10 cross-reference integrity post-renumbering).
- v4 (2026-05-05): post-convergence-test revision per Path A sequencing. The operating-model convergence test on Database & Schema Bible draft (`_audits/convergence_test_audit.md`) returned 21 material differences + 9 methodology gaps. G8 was closed in META_PLAN v7→v8 cycle (LOCKED). v4 closes the remaining 8 methodology gaps: G1 (cross-cutting Currently Open scope), G2 (superseded SQL constraint Deprecated qualification), G3 (W.N entry confined to bug fixes; discipline codifications routed to § 5), G4 (TOC framing — sections 5–8 mandatory, sections 1–4 recommended-strongly), G5 (convergence rule on discipline rule rosters), G6 (cross-reference syntax worked examples), G7 (CONDITIONAL tertiary state for conditional trigger evaluation), G9 (W.N bible-local + global Bug #N convention for cross-bible references). Tony locked decisions on G3/G5/G7/G9 architectural questions; G1/G2/G4/G6 implemented per audit-CC-recommended resolutions embedded as drafting-spec exact-text replacements. Companion verification log at `_audits/BIBLE_STRUCTURE_SPEC_v4_verification.md`. After v4 lock, the convergence test re-runs on the same Database & Schema Bible spec to validate gap closure.
- v5 (2026-05-05): post-v4-audit surgical-cosmetic patch closing the single blocking-for-clean-lock finding (§ 11 Lock Status metadata block at lines 1142–1146 was missed during v4 drafting; front matter Status was correctly updated to v4 but § 11 metadata sub-fields still referenced v3). v4 audit returned 0 BLOCKER + 0 MATERIAL + 0 fabricated + 0 methodology-interpolation + 2 MINOR + 4 STYLE; cleanest substantive cycle of v3-v5 sequence. v5 fix is pure metadata pointer hygiene; no methodology touch; no content modification beyond § 11 + front matter Status/Locked + revision history + § 12.5 + § 13 v4→v5 changelog entry. Companion verification log at `_audits/BIBLE_STRUCTURE_SPEC_v5_verification.md` (V5-1 entry for the metadata fix; V4-1 through V4-11 inherited wholesale).
- v6 (2026-05-05): post-convergence-test-re-run surgical-cosmetic patch closing 2 NEW methodology gaps surfaced by the v5/v8-substrate convergence test (`_audits/convergence_test_v5_audit.md`). Re-run verdict: CONVERGED-WITH-RESIDUAL — 18 material differences (down from 21 in original test); 8 PASS + 1 PARTIAL + 0 FAIL on the 9 original G1-G9 gap closures (G8 PARTIAL is drafter-compliance variance, not methodology ambiguity; banked for Phase 1 audit-CC checklist). v6 closes G-new-1 (candidate-roster numbering: numeric sub-section IDs per Tony's locked Option (a); embedded as § 5.7 closing-clause paragraph) and G-new-2 (matview enumeration scope: § 4.1 enumerates CREATE TABLE declarations only per Tony's locked Option (a); embedded as § 6.6 § 4.1 first-sentence qualification). Zero new methodology constructs; both closures embed Tony-locked decisions char-exact per drafting-spec. Companion verification log at `_audits/BIBLE_STRUCTURE_SPEC_v6_verification.md` (V6-1 entry for the 2 surgical embeds; V5-1 + V4-1 through V4-11 + 27 v3-inherited preserved wholesale).

**Tier:** 3 per META_PLAN v6 § 4.1 + § 6.5. CC-drafted under QB spec; companion verification log required; CC-audited.

**Anchored on:** META_PLAN v6 (locked). Section references throughout this document point to v6 § numbers.

**Methodology-interpolation rule (operative per META_PLAN v6 § 6.1, with v6 expanded scope and grandfathering clause; pattern-completion check operative per BIBLE_STRUCTURE_SPEC v1 audit lesson):** This draft does not invent binary tests, cadence rules, completeness criteria, scoring rubrics, severity thresholds, iteration caps, percentage criteria, procedural sequencing rules, or other CC-prescribed methodology constructs Tony has not explicitly ratified. Pattern-completion interpolation check operative; v3 surfacing notes in § 12.2.

---

## 1. Purpose and Scope

### 1.1 What this document is

BIBLE_STRUCTURE_SPEC.md is the second Phase 0 methodology deliverable. Its job is to translate META_PLAN v6's Phase 1 design constraints into an actionable inventory of Phase 1 bible documents with concrete TOCs, per-section content guidance, and shared cross-document conventions. After this document locks, Phase 1 drafting CCs receive specs that point at this document for "what does each bible look like, what sections does it contain, what content goes in each section." This document is the structural anchor that prevents Phase 1 drift across multiple parallel CC sessions.

### 1.2 What this document is NOT

This document does not draft Phase 1 bible content. It specifies the structure into which Phase 1 content will be drafted. The TOCs and section guidance below are templates, not finished bible material. Phase 1 CC sessions fill the templates against the actual EE codebase under verification discipline.

This document does not specify how to audit Phase 1 bibles — that's AUDIT_METHODOLOGY.md (Phase 0 deliverable 3). This document does not specify what "done" looks like for any phase — that's CONVERGENCE_CRITERIA.md (deliverable 4). This document does not specify the format for findings in `PHASE_5_BACKLOG.md` — that's TRIAGE_QUEUE_SPEC.md (deliverable 5).

### 1.3 Authority chain

The Phase 1 document inventory below satisfies three locked-at-META_PLAN-level constraints:

- **META_PLAN v6 § 3.2.1 ML floor:** three separate Phase 1 documents minimum, three distinct .md files at three distinct paths, one per forcing function (Feature Provenance, ML Layer Architecture, Model Evaluation & Retraining). A single file with three sections does not satisfy this requirement. This spec preserves the floor; it does not relax it.
- **META_PLAN v6 § 3.2 working hypothesis:** 5–7 documents total; non-ML documents are provisional and may be merged or split. This spec's analytical output (§ 4) settles on 7 documents (3 ML + 4 non-ML).
- **META_PLAN v6 § 3.2.1 convergence test:** "given this inventory, can a fresh CC session evaluate, rebuild, or retrain a model in the gallery?" This spec's § 11 traces the inventory back to this test.

### 1.4 What this document inherits from META_PLAN v6

The following are inherited and not restated here; cross-reference by section number:

- Tier model (§ 6.5)
- Verification log precision rule (§ 6.5)
- Methodology-interpolation rule with grandfathering clause (§ 6.1)
- Source authority hierarchy (§ 4.5, § 8.5)
- Maintenance protocol (§ 7.1–7.14)
- Anti-patterns for bible content (§ 9.1–9.13)
- Audit-CC adversarial scope (§ 6.2)
- Audit/verification subdirectory convention (§ 3.8)

Phase 1 bibles reference these META_PLAN sections directly; they do not duplicate the rules.

---

## 2. Operating Principles

### 2.1 Bibles document what is, not what should be

(Inherited from META_PLAN v6 § 2.1.) Every Phase 1 bible documents the system as it exists at lock time. Aspirations belong in Phase 4 deliverables, not in any Phase 1 document. This is the dominant constraint shaping every TOC below.

### 2.2 Locality of reference governs the split

(Per META_PLAN v6 § 3.2 rationale.) The multi-file split exists because EE's complexity will exceed DD's 2,578-line single-file size comfortably AND because the three ML forcing functions resist combination. The split is for navigability and forcing-function service.

### 2.3 Cross-cutting content lives in one canonical home

(Per META_PLAN v6 § 7.4 cross-cutting bug scope rule.) When a topic spans multiple bibles, the canonical content lives in the bible whose discipline most directly affects the topic. Other bibles cross-reference by ID, not duplicate.

### 2.4 Templates do not legislate completeness

This spec's TOCs and per-section guidance describe the **structure** Phase 1 drafters fill. They do not dictate when a section is "complete." Completeness is determined per-document by the audit-CC adversarial scope (META_PLAN § 6.2) plus document-specific verification mandate.

---

## 3. Document Locations and Naming

### 3.1 Filesystem location

All Phase 1 bible documents live at `/home/strakajagr/projects/equine-equalizer/docs/bible/`.

### 3.2 Filename convention (Tony-ratified per v1 cycle)

Filenames are lowercase with underscores, ending in `.md`:

- `architecture_overview.md`
- `data_pipeline_bible.md`
- `feature_provenance_bible.md`
- `ml_layer_architecture_bible.md`
- `model_evaluation_retraining_bible.md`
- `database_schema_bible.md`
- `api_frontend_bible.md`

Lowercase-underscore matches `migrate.py` and the Python codebase convention. Uppercase-with-underscores like `META_PLAN.md` is reserved for Phase 0 methodology documents.

The `_bible` suffix asymmetry (Tony-ratified per v1 cycle): files in `/docs/bible/` use `_bible.md` suffix EXCEPT documents that are inherently bible-corpus-level (Architecture Overview; future BIBLE_INDEX.md if ever created).

### 3.3 Section ID convention

Within each bible document, sections are numbered in dotted decimal form. Cross-bible references: `<bible_doc_name>:<section_id>`. Cross-bible references for cross-cutting bugs use a separate format: `<bible_doc_name>:#<bug-id>` where `<bug-id>` is the canonical global Bug #N (per § 5.5.1 below). Examples:
- `feature_provenance_bible:4.1` — section 4.1
- `data_pipeline_bible:8.W.7` — What Was Fixed entry W.7 in Data Pipeline Bible (§ 8 = canonical What Was Fixed position; W.N is bible-local per § 5.5)
- `database_schema_bible:5.4` — sub-section numeric ID for a Forbidden Pattern (no letter prefix; see § 5.5)
- `feature_provenance_bible:#15` — cross-cutting reference to Bug #15's canonical home (Feature Provenance Bible's W.N entry for Bug #15; per § 5.5.1 global Bug #N convention)

Matches META_PLAN v8 § 7.11's commit message convention. The `#<bug-id>` cross-reference format closes G9 (W.N numbering instability across CC executions): bible-local W.N entries are stable within a bible's lifetime but not cross-bible-coordinated; the global Bug #N is the durable cross-bible reference per § 5.5.1.

---

## 4. Phase 1 Document Inventory

### 4.1 Document list

Seven Phase 1 bible documents. Three ML-specific (per META_PLAN v6 § 3.2.1 floor). Four non-ML.

| # | Filename | Type | Forcing function / audience |
|---|---|---|---|
| 1 | `architecture_overview.md` | Non-ML | System topology + INDEX for cross-bible navigation |
| 2 | `data_pipeline_bible.md` | Non-ML | Daily ingestion, results, scrapers, EventBridge schedule |
| 3 | `feature_provenance_bible.md` | ML | FF1: feature × model — source data → eng → consumer |
| 4 | `ml_layer_architecture_bible.md` | ML | FF2: per-model type / inputs / outputs / pipeline position |
| 5 | `model_evaluation_retraining_bible.md` | ML | FF3: success criteria / retrain triggers / artifact lifecycle |
| 6 | `database_schema_bible.md` | Non-ML | 14 tables + 1 matview, migration discipline, JSONB conventions |
| 7 | `api_frontend_bible.md` | Non-ML | 41 API Gateway routes, Lambda-handler-as-router pattern, axios client |

Visual grouping: rows 1–2 + 6–7 are non-ML; rows 3–5 are ML.

### 4.2 Non-ML document justification

Per Tony's locked Q1 from the v1 drafting spec, each non-ML document carries a justification artifact with three audit-checkable pieces.

#### 4.2.1 architecture_overview.md

**What questions does this document answer?**

- "What does EE look like at the runtime-context level?" (Lambda inventory, ECS Fargate fleet, Aurora cluster, S3 buckets, API Gateway v2, EventBridge rules, ECR repositories, SNS, Secrets Manager.)
- "What canonical objects cross runtime contexts?" (Race / Entry / PastPerformance / Workout / Result / Prediction at `backend/models/canonical.py`; per-pipeline prediction shapes WRPrediction / PLPrediction / LSPrediction.)
- "Which bible should I read for X?" (The INDEX section linking out to the six other bibles with one-line summaries and the kinds of questions each answers.)

**What audience does it serve?**

Any reader who needs the system map or needs to navigate to a specific bible. Architecture Overview is the canonical entry point: a reader who lands in `/docs/bible/` for the first time reads this first. It is also the cross-bible navigation hub — every other bible's Scope section cross-references back here for the system topology, and the INDEX in Architecture Overview's § 5 (or equivalent positioning) points outward to all six.

**What would break if merged with another document?**

- **If merged with Data Pipeline Bible:** the runtime topology and the INDEX function would be subordinated to flow-level detail. A reader asking "where do I find the bible for X?" would have to scan past pipeline-flow descriptions to find the navigation map. Merging conflates the system map (where things are) with the data flow (how things move) — structurally different concepts; merging buries the map.
- **If merged with API & Frontend Bible:** runtime topology beyond Lambda + API Gateway (specifically: ECS Fargate training fleet, Aurora Serverless, S3 buckets, EventBridge rules) would lose its home. The API & Frontend audience is client-engagement-focused; ECS and EventBridge are not part of that audience's primary concerns.
- **The INDEX role makes Architecture Overview the canonical entry point.** Merging it into any other bible displaces the entry point; readers would have to know the merge target's name to find the navigation map, defeating the purpose of an INDEX.

#### 4.2.2 data_pipeline_bible.md

**What questions does this document answer?**

- "How does data move from external source to DB to model to API?" (Daily ingestion flow, results-fetch flow, workout collection, chart parsing, retraining cadence.)
- "What's the EventBridge schedule and what does each cron flow do?" (13 rules: 10 ENABLED + 3 DISABLED per live verification.)
- "How does each data source (HRN, NYRA, Equibase) behave in terms of reliability and silent failure?" (Per-source Data Acquisition Honesty Protocol entries per META_PLAN v6 § 7.9.)
- "Where did Bug #28 surface, and what's the canonical fix path?" (Bug #28 column-shift fix is canonically homed here.)

**What audience does it serve?**

Anyone touching ingestion, scrapers, results-matching, or retraining schedule. Operational engineers working on flow-level reliability and operators debugging silent-failure scenarios. The audience is process-centric (how does data flow?), distinct from structure-centric audiences (Architecture Overview's "what exists?" or Database & Schema Bible's "what columns are canonical?").

**What would break if merged with another document?**

- **If merged with Database & Schema Bible:** the data-acquisition discipline (per META_PLAN v6 § 7.9) and per-flow failure-mode tracking would mix with table-level documentation. A reader debugging a Bug #28-style scraper issue would have to filter through schema discussions to find pipeline-flow detail.
- **If merged with Architecture Overview:** the per-flow detail (9 cron-triggered flows + on-demand inference + retraining task families) would crowd out runtime topology. Architecture Overview's INDEX function would be diluted by flow-by-flow narrative.
- **Bug #28 canonical home (per § 5.3 cross-cutting rule):** Bug #28 surfaced via the nightly results fetch flow; its canonical home is Data Pipeline Bible § 8.W.<n>. Merging this bible would relocate the canonical entry, breaking the cross-cutting bug discipline at META_PLAN v6 § 7.4.

#### 4.2.3 database_schema_bible.md

**What questions does this document answer?**

- "What tables exist?" (14 tables + 1 materialized view per verified count.)
- "What columns are canonical, and what are their types/constraints?" (Per-table column lists, primary keys, UNIQUE constraints, FK constraints.)
- "What are the JSONB conventions where present?" (Shape documentation for fields like `model_versions.feature_list`, `model_versions.hyperparameters`.)
- "How do migrations work?" (Per META_PLAN v6 § 7.12: NNN_short_description.sql for 001–011 grandfathered; NNN_YYYYMMDD_*.sql from 012+. The duplicate-005 case. The `schema_migrations` runner mechanism.)
- "What is the predictions-table family?" (Legacy `predictions` + per-pipeline `wr_predictions` / `pl_predictions` / `ls_predictions` split.)

**What audience does it serve?**

Anyone touching schema, repos, or migrations. Engineers writing new repository methods, DBAs reviewing migration safety, ML engineers verifying that a feature's source column exists with the expected type. The audience is reference-focused: this bible is consulted for "what is the canonical column?" or "what's the migration discipline?", not read end-to-end.

**What would break if merged with another document?**

- **If merged with Data Pipeline Bible:** the canonical column lists, JSONB conventions, and migration discipline would mix with flow-level documentation. The schema's reference-style access pattern (look up a table or column by name) is incompatible with the Data Pipeline's flow-narrative access pattern.
- **If merged with Architecture Overview:** per-table detail would dilute system-level topology.
- **The schema is foundational reference content that other bibles cite.** Feature Provenance cites raw data source columns. ML Layer Architecture cites the model_versions table for the registry semantics. Merging buries the reference.

#### 4.2.4 api_frontend_bible.md

**What questions does this document answer?**

- "What HTTP routes exist, and what does each one return?" (41 API Gateway routes per verified count, with per-route method/path/integration target.)
- "How does Lambda dispatch route requests?" (Lambda-handler-as-router pattern: API Gateway → Lambda → `def get_*` / `def post_*` function in `backend/routers/`.)
- "How does the React frontend consume the API?" (axios client at `frontend/src/api/client.ts`; per-domain function exports; BASE_URL fallback chain.)
- "What's the per-route Lambda integration mapping, and what happens when the integration target is INACTIVE?" (Per META_PLAN v6 § 8.5 AWS-vs-API source-priority resolution.)

**What audience does it serve?**

Anyone touching the API surface or the React SPA. Client-engagement-focused: how does a frontend developer or external API consumer understand and use the surface? The audience is descriptive-focused (what does each route do?), distinct from infrastructure-focused (Architecture Overview) or process-focused (Data Pipeline).

**What would break if merged with another document?**

- **If merged with Architecture Overview:** the per-route documentation (41 routes) would dilute system-level topology. The 41-row route inventory is high-frequency reference content; embedding it in Architecture Overview makes Architecture Overview structurally lopsided.
- **If merged with Data Pipeline Bible:** the API surface (consumer-facing) would mix with backend processing (ingestion / inference / retraining). Audiences differ — frontend developer vs pipeline engineer.
- **The API surface is the system's contract with consumers.** Documenting it separately gives consumers a stable reference. Merging loses the contract framing.

### 4.3 ML document inventory (one-line summaries)

The three ML documents are governed by META_PLAN v6 § 3.2.1's locked forcing functions. Their floor (≥ 3 separate documents at 3 distinct paths) and their non-mergeability are locked at META_PLAN level; merge-cost analysis is therefore not required here.

3. **Feature Provenance Bible** (`feature_provenance_bible.md`) — for every feature × every model: source data path → engineering code (training-side and inference-side, or shared module) → consuming model(s) → target latent. The 14 Gonzo Sauce features as the single-source-of-truth pattern (`model/shared/gonzo_features.py`); the remaining base features as the manual-cross-reference parallel-implementation pattern.
4. **ML Layer Architecture Bible** (`ml_layer_architecture_bible.md`) — for every model in the gallery: type (XGBoost / LSTM / RandomForest / Bayesian / logistic regression ensemble), inputs, outputs, pipeline position, target latent, output composition with other models, calibration / bypass state. The 7-layer LS stack composition. The model registry's multi-active-row reality (88 = 45 active + 43 inactive per META_PLAN v6 § 9.13 + Claim 7).
5. **Model Evaluation & Retraining Bible** (`model_evaluation_retraining_bible.md`) — per-model success criteria, retraining triggers (data drift detection, performance degradation thresholds, scheduled retrains), calibration discipline as process (when calibration is fitted, when it is bypassed, why), model artifact version control beyond `is_active`, deployment gating.

### 4.4 What this inventory does NOT include

- **PHASE_5_BACKLOG.md** is adjacent to the bible (per META_PLAN v6 § 4.3), not part of it.
- **Phase 2 audit reports** at `/docs/bible/_audit/` are bible-by-bible audit outputs, not bible content.
- **Phase 3 PREDICTIVE_CONCEPTS.md and Phase 4 deliverables** are downstream deliverables.
- **Frontend bible split (Tony-ratified per v1 cycle):** frontend stays as a section of the API & Frontend Bible.

---

## 5. Common Document Structure (Shared Across All Seven Bibles)

Every Phase 1 bible document includes the following sections in the canonical order. The order is **mandatory for the discipline-rule + bug-history group at sections 5–8** (per Tony's v3-cycle Finding 1 ratification); domain-specific sections at positions 1–4 may be reorganized per locality of reference. The What Was Fixed section is mandated per-document explicitly by META_PLAN v6 § 7.4; the Forbidden Patterns / Common Mistakes / Deprecated formats are mandated by § 7.5 / § 7.6 / § 7.7 as inherited DD discipline patterns.

### 5.1 Front matter

Every bible document opens with:

```
# <Document Title>

**Document:** <document name>
**Phase:** 1 (Bible)
**Status:** DRAFT v<N> (pre-audit) / LOCKED (<date>)
**Author:** CC (drafting under verification discipline; QB orchestrated)
**Date:** <YYYY-MM-DD>
**Locked:** [pending] / <YYYY-MM-DD>

**Revision history:**
- v<N> (<date>): <one-line summary>

**Tier:** 3 per META_PLAN v<N> § 4.1 + § 6.5.

**Anchored on:** META_PLAN v<locked> + BIBLE_STRUCTURE_SPEC v<locked>.

**Companion verification log:** `_audit/<doc>_v<N>_verification.md`.
```

The front matter mirrors META_PLAN v6's pattern.

### 5.2 Canonical TOC pattern

The numbered sections inside each bible follow this **canonical** outline (mandatory for sections 5–8 per Tony's v3-cycle Finding 1; recommended-strongly for sections 1–4):

1. **Scope of this bible** — what this bible documents, what it does not, what other bibles cover its boundary topics
2. **Definitions** — terminology specific to this bible's domain (acronyms, named patterns)
3. **Architecture overview** — this bible's slice of the system at a runtime-context level
4. **Domain-specific content** (canonical objects + per-X documentation specific to this bible's audience), sub-numbered as 4.X. May extend to multiple sub-sections (4.1, 4.2, 4.3, ...) as content density requires.
5. **Discipline rules** — Forbidden Patterns + Common Mistakes for this domain (per META_PLAN § 7.5 + § 7.6 formats)
6. **Currently Open** — one-line bug list with `PHASE_5_BACKLOG.md` pointers (per META_PLAN § 7.8 + § 9.10)
7. **Deprecated** — cross-references to `PHASE_5_BACKLOG.md` entries (per META_PLAN § 7.7 + § 9.4)
8. **What Was Fixed — Do Not Revert** — institutional immune memory entries scoped to this bible's domain (per META_PLAN § 7.4); entries follow the W.N format (see § 5.5) sub-numbered as 8.W.<n>

**Authority for canonical 5–8 ordering:** § 7.4 of META_PLAN v6 explicitly mandates per-document inclusion of What Was Fixed. § 5.6's canonical templates assume sections 5/6/7/8 are at fixed positions across all bibles so cross-bible references (e.g., the example in § 5.6.2 "section 5 of the ML Layer Architecture Bible is `ml_layer_architecture_bible:5.4`") resolve consistently. Deviating per-document would break the shared-template cross-references.

**Empty sections are explicit, not absent:** a bible with no current open issues at lock time still includes a § 6 "Currently Open" section reading "No current open issues at lock." A bible with no deprecated entries still includes § 7 "Deprecated" reading "No deprecated entries at lock." Better an explicit empty section than a missing one that breaks cross-bible references.

**EE convention divergence from DD:** DD's What Was Fixed section is at DD § 18 because DD's bible has 21 sections in a single file. EE bibles have 8–10 sections each (with domain-specific 4.X sub-sections), so What Was Fixed at position 8 is the EE convention. Future readers comparing bibles should treat this as intentional divergence per the multi-file context.

### 5.3 Cross-cutting bug scope rule (per META_PLAN v6 § 7.4)

When a bug spans multiple bibles, the canonical "What Was Fixed" entry lives in one bible (the one whose discipline most directly prevents recurrence). Other bibles reference by ID. **No duplication.**

The canonical-home determination is made at the time the entry is created. The decision is recorded in the entry (the canonical home's W.N entry says "canonical; cross-referenced from <other bibles>"; the cross-referencing bibles' "Currently Open" or "Deprecated" sections cite the canonical home by `<bible>:#<bug-id>` per § 3.3 cross-reference syntax for cross-cutting bugs.

**Cross-cutting bug Currently Open scope rule (closes G1):** When a cross-cutting bug is currently open at lock time, it appears in § 6 (Currently Open) of the canonical-home bible AND in § 6 of every bible whose discipline its symptoms touch, with cross-reference to the canonical home. The canonical-home bible's § 6 entry is the substantive description; non-canonical-home bibles' § 6 entries are one-line cross-references to the canonical home in `<bible>:#<bug-id>` format. Symptom-touch determination is at drafter discretion: if the bug's manifestation is documented in this bible's domain (e.g., Bug #28's NULL payout fields manifest in `database_schema_bible:4` table-level documentation of the `results` table), the bug appears in this bible's § 6 as a cross-reference. Once the bug is fixed and documented in the canonical home's § 8 W.N entry, non-canonical-home bibles' § 6 entries are removed (the W.N entry replaces them). Cross-cutting bug entries in `PHASE_5_BACKLOG.md` (per `TRIAGE_QUEUE_SPEC v1` format) cite the canonical home plus all bibles whose § 6 references the bug.

**Tiebreaker deferral:** when "most directly prevents recurrence" is ambiguous (two QB sessions could plausibly assign the canonical home to different bibles), tiebreaker criteria are deferred to AUDIT_METHODOLOGY.md (Phase 0 deliverable 3). Until that document locks, QB surfaces ambiguous cases to Tony for explicit ratification per META_PLAN v6 § 8.3 decision-deferral discipline.

### 5.4 Dated lock points (per META_PLAN v6 § 7.3)

Every rule, pattern, decision in any bible carries a `Locked YYYY-MM-DD` parenthetical. Section headers, FORBIDDEN/CORRECT pairs, and W.N entries all carry lock dates. The format is identical to META_PLAN v6 § 7.3 + Appendix A.2.

### 5.5 Naming conventions inside each bible

- **What Was Fixed entries** are numbered as `<section>.W.<n>` (e.g., `8.W.1`, `8.W.2` within section 8 of a given bible). The format follows META_PLAN v8 § 7.4 + Appendix A.3. The W.N letter-prefix convention is the **only** letter-prefix in EE bible numbering. **W.N is bible-local, not cross-bible-stable (per § 5.5.1 G9 resolution):** within a bible, W.N entries are stable across the bible's re-drafts; across bibles, a `W.7` entry in `feature_provenance_bible` may number a different bug than a `W.7` entry in `data_pipeline_bible`. Cross-bible references to bugs use the canonical global Bug #N convention per § 5.5.1, NOT bible-local W.N section numbers. The W.N letter-prefix is preserved for in-bible bug-tracking forcing function (a grep over a single bible's contents for `W.7` retrieves entries within that bible per META_PLAN v8 § 7.11 commit-message convention).

- **Forbidden Patterns**, **Common Mistakes**, and **Deprecated entries** use **sub-section numeric IDs** (e.g., a Forbidden Pattern at section 5 of the ML Layer Architecture Bible is `ml_layer_architecture_bible:5.4`, not `ml_layer_architecture_bible:5.F.4`). The format follows META_PLAN v6 § 7.5 + Appendix A.1 (Forbidden Patterns), § 7.6 (Common Mistakes), § 7.7 + Appendix A.4 (Deprecated). This matches the DD bible's existing convention: DD § 6.4 for a Forbidden Pattern, DD § 21.1 for a Deprecated entry.

- **Cross-bible references** use the full path: `<bible_name>:<section_id>` (e.g., `feature_provenance_bible:8.W.7` for a What Was Fixed entry; `ml_layer_architecture_bible:5.4` for a Forbidden Pattern). Within a single bible, references can use just the local ID: `see § 5.4`, `see § 8.W.3`.

**Why W.N is special and F./C./D. are not:** What Was Fixed entries are the bible's institutional immune memory. Cross-cutting bugs require trackable identifiers across bibles. A grep for `W.7` finds every commit, every cross-reference, every related entry in O(n) wall-clock time. Forbidden Patterns, Common Mistakes, and Deprecated entries do not carry the same forcing function — they don't cross bibles in the same way. Sub-section numeric IDs suffice and match DD convention.

#### 5.5.1 Global Bug #N convention (closes G9)

Bugs that surface during EE development are assigned a canonical global Bug #N at discovery time. The convention is monotonic and never reused: Bug #1, Bug #2, ..., Bug #28, Bug #29, ... Each Bug #N has exactly one canonical home in exactly one bible (per § 5.3 cross-cutting bug scope rule); references to the bug from other bibles use the `<bible>:#<bug-id>` format per § 3.3 cross-reference syntax.

**Convention specifics (locked 2026-05-05 per v4 cycle):**
- **Monotonic assignment:** Bug numbers are assigned in order of discovery, not in order of fix or in order of severity. Bug #28 was assigned because it was the 28th bug discovered, regardless of when it was fixed (or whether it has been fixed at lock time).
- **Never reused:** when a bug is fixed and its W.N entry locked, the Bug #N is retired but never re-assigned. If a bug is determined to be a duplicate of an earlier Bug #M, the duplicate's Bug #N is closed without re-assignment.
- **Cross-bible reference uses `#<bug-id>` not `W.<n>`:** because bible-local W.N is not cross-bible-stable (a fix lands as `8.W.3` in feature_provenance_bible AND as `8.W.5` in another bible), the cross-reference target is the global Bug #N, not the bible-local W.N. Example: `feature_provenance_bible:#15` references the canonical home of Bug #15, which is the bible-local W.N entry for Bug #15 in `feature_provenance_bible`.
- **De facto convention is now explicit:** EE has used Bug #28, Bug #15, Bug #24 as global identifiers in operator-stated context and Phase 0 documents (per META_PLAN v8 § 1.2). This sub-rule makes the existing convention explicit rather than introducing a new one.

The global Bug #N convention does not introduce a new letter-prefix. The pattern-completion check (per AUDIT_METHODOLOGY v2 § 5.5) applies to letter-prefixes; `#<bug-id>` is a cross-reference syntax extension, not a section-numbering letter-prefix. W.N remains the only ratified letter-prefix in EE bible numbering.

### 5.6 Canonical templates for shared content

The four discipline-rule entry types (What Was Fixed, Forbidden Patterns, Common Mistakes, Deprecated) appear in every Phase 1 bible. Their canonical templates are extracted here so per-document templates in § 6 cross-reference rather than duplicate.

#### 5.6.1 What Was Fixed entry template (per META_PLAN v6 § 7.4 + Appendix A.3)

```
8.W.<n>: <Bug name or short description> (fixed YYYY-MM-DD)
```

**Scope (locked per v4 cycle, closes G3):** § 8 What Was Fixed entries are confined to **true bug-fix entries with mandatory Fix date**. § 8 is institutional immune memory ("we hit this bug, fixed it, here's what changed and when"); the Fix date is part of the value proposition. **Discipline codifications** (rules captured against future drift; e.g., "past_performances.race_id NULL acceptance") are NOT § 8 entries — they belong in § 5 (Discipline rules) per § 5.6.2 (Forbidden Pattern template) or § 5.6.3 (Common Mistakes template). Forward-looking entries that codify discipline for fixes that haven't happened yet (per META_PLAN v8 § 7.3 placeholder-resolution sub-rule's case (ii)) also belong in § 5, not § 8 — § 5 entries do not require a Fix date because they are rules, not fixes.

**Mandatory fields:**
- Entry ID (`8.W.<n>` format)
- Bug name or short description (with global Bug #N if assigned per § 5.5.1)
- Fix date (YYYY-MM-DD) — **mandatory; entries without a knowable fix date belong in § 5, not § 8**
- **Symptom:** how the bug manifested
- **Root cause:** what the actual problem was
- **Fix:** what was changed
- **Why this entry exists:** what discipline must persist to prevent recurrence

**Conditional fields (with triggers):**
- **If the fix involved a migration:** link to the migration entry per § 7.12 format (file path + migration number)
- **If the fix invalidated prior bible content:** mark the prior content with a deprecation note linking forward to this entry
- **If the fix produced a Forbidden Pattern:** cross-reference the Forbidden Pattern's section ID (`<bible>:<section_id>`)
- **If the fix touches multiple bibles:** the entry lives in the canonical document per § 5.3 cross-cutting bug scope rule; other bibles cross-reference by `<bible>:8.W.<n>`

##### 5.6.1.1 Worked example: W.3 Gonzo Sauce FE Single-Source Extraction (illustrative)

The example below shows META_PLAN v6 Appendix A.3's W.3 entry as it would appear in the Feature Provenance Bible's § 8 What Was Fixed section. Each conditional trigger is explicitly evaluated. Placeholder section IDs (e.g., `5.X` for a Forbidden Pattern that does not yet exist) follow META_PLAN v6 Appendix A's placeholder convention.

```
8.W.3: Gonzo Sauce Feature Engineering Single-Source Extraction (fixed 2026-04-22)

Symptom: Three calibration bugs surfaced in one week (early April 2026). Each had
a different proximate cause but the same root cause: feature values computed during
training disagreed with feature values computed during inference for identical inputs.

Root cause: model/shared/data_loader.py (training-time FE) and
backend/services/feature_engineering_service.py (inference-time FE) had drifted in
their implementation of the 14 Gonzo Sauce features. Defaults differed, edge-case
handling differed, par-time computation differed in subtle ways.

Fix: All 14 Gonzo Sauce feature computations were extracted to
model/shared/gonzo_features.py, imported by both training and inference paths.

Why this entry exists: the 14 Gonzo Sauce features are factored cleanly. The
remaining base features still have parallel implementations in two locations,
kept in sync by manual cross-reference review. The discipline of "if you change
a feature in one place, change it in the other" is procedurally enforced, not
architecturally enforced.

Conditional triggers evaluated (per § 5.6.1.2 tertiary-state notation, locked per v4 cycle):
  - if-fix-involved-migration: DOES NOT FIRE. Gonzo extraction was a code refactor,
    not a schema change. No migration linkage.
  - if-fix-invalidated-prior-content: DOES NOT FIRE. No prior bible content existed
    at extraction time (pre-Phase-0).
  - if-fix-produced-Forbidden-Pattern: FIRES. Cross-reference to candidate Forbidden
    Pattern at `feature_provenance_bible:5.X` (placeholder; Phase 1 drafter assigns
    actual numeric ID at draft time): "Adding feature engineering logic to either
    training or inference path without parallel update to the other."
  - if-fix-touches-multiple-bibles: CONDITIONAL. The bug spans Feature Provenance
    Bible (canonical home, per § 5.3) and is cross-referenced from
    `ml_layer_architecture_bible:#15` and `model_evaluation_retraining_bible:#15`
    by global Bug #N per § 5.5.1. The CONDITIONAL caveat: the cross-references are
    descriptive of where Bug #15 manifests (calibration bypass at inference, retrain
    discipline implications) but the canonical W.N entry — including Symptom, Root
    cause, Fix, and Why — lives only in this bible (Feature Provenance Bible) per
    the cross-cutting bug scope rule's no-duplication mandate.
```

Phase 1 drafters use this worked example as the integration model: when drafting their bible's What Was Fixed entries, evaluate each conditional trigger explicitly with FIRES / DOES NOT FIRE notation, even when the trigger doesn't apply.

##### 5.6.1.2 Tertiary-state notation for conditional trigger evaluation (closes G7)

Conditional triggers in W.N entries (and other discipline-rule entries with conditional fields) are evaluated using three states, locked per v4 cycle:

- **FIRES:** the trigger applies; the conditional field MUST be included with full content.
- **DOES NOT FIRE:** the trigger does not apply; the conditional field is not relevant. The drafter writes "DOES NOT FIRE" with a brief reason (one phrase, not a full sentence).
- **CONDITIONAL:** the trigger applies with an explicit caveat; the drafter MUST document the caveat in adjacent prose (the prose immediately following the trigger evaluation, not deferred to a separate section). The CONDITIONAL state is more semantically precise than "PARTIAL" or "FIRES (advisory)" — it names the case's distinguishing feature (a condition modifies trigger application) rather than describing discomfort with binary classification.

**CONDITIONAL discipline:** mandatory adjacent-prose documentation of the caveat prevents the tertiary state from becoming an escape hatch. If a drafter cannot articulate the caveat in adjacent prose, the trigger is not CONDITIONAL — it's either FIRES (commit to inclusion) or DOES NOT FIRE (commit to exclusion). The audit-CC prophylactic check at AUDIT_METHODOLOGY v2 § 5.2 (methodology-interpolation) applies recursively here: a CONDITIONAL trigger without adjacent-prose caveat is a CC-introduced soft-classification that Tony hasn't ratified.

**Worked examples in § 5.6.1.1 use the tertiary notation explicitly.** Phase 1 drafters use § 5.6.1.1 as the integration model for evaluating conditional triggers; if a trigger is CONDITIONAL, the drafter writes the caveat in adjacent prose at draft time, not at audit time.

#### 5.6.2 Forbidden Pattern entry template (per META_PLAN v6 § 7.5 + Appendix A.1)

Forbidden Patterns live at sub-section numeric IDs within section 5 (Discipline rules) of each bible.

**Mandatory fields:**
- Section ID (`<section>.<n>`, e.g., `5.4`)
- Pattern name (in section header) with `(locked YYYY-MM-DD)` parenthetical
- Rule body explaining what discipline applies
- **Rationale:** why this rule exists, often referencing the bug history that produced it
- **FORBIDDEN code example** (3–8 lines per META_PLAN v6 § 9.6)
- **CORRECT code example** (3–8 lines)

**Conditional fields (with triggers):**
- **If the pattern was produced by a specific bug:** cross-reference the canonical W.N entry by full path (`<bible>:8.W.<n>`)
- **If the pattern affects multiple bibles:** the rule lives in the bible whose discipline most directly enforces it; other bibles cross-reference by section ID
- **If a real EE function illustrates the FORBIDDEN/CORRECT contrast:** cite the function with file:line (e.g., `model_version_repository.py:100`) per META_PLAN v6 Appendix A.1's pattern
- **If the rule supersedes a prior locked rule:** the new lock date supersedes the old; git log preserves the audit trail per § 5.4

#### 5.6.3 Common Mistakes entry template (per META_PLAN v6 § 7.6)

**Source-spec depth note:** META_PLAN v6 § 7.6 inherits DD § 19's format without expansion ("Format inherited from DD § 19"). DD § 19's Common Mistakes entries are intentionally brief — wrong instinct + corrected position pairs without elaborate field structure (verified per BIBLE_STRUCTURE_SPEC v3 verification log Claim N9). This template reflects that source-spec depth. Phase 1 drafters expand entries with bug-class context and rationale as needed; the template specifies the minimum (wrong instinct + corrected position) rather than mandating greater depth.

Common Mistakes live at sub-section numeric IDs within section 5 (Discipline rules), distinct from Forbidden Patterns.

**Mandatory fields:**
- Section ID (`<section>.<n>`)
- Wrong instinct (the recurring CC or operator mistake, in quotation form: "I'll just add a fallback...")
- Corrected position (the right approach, with explicit rationale: "NO. Fallbacks hide bugs.")

**Conditional fields (with triggers):**
- **If the mistake was caught in a specific audit cycle:** reference the cycle in a parenthetical (e.g., "caught in v3 audit" — operator-stated rationale per § 4.5 source-priority tier 5)
- **If correction differs from a Forbidden Pattern, distinguish:** Common Mistakes are recurring instincts; Forbidden Patterns are design rules. The distinction is META_PLAN v6 § 7.5 vs § 7.6 — same domain, different forcing function

#### 5.6.4 Deprecated entry template (per META_PLAN v6 § 7.7 + Appendix A.4)

Deprecated entries live at sub-section numeric IDs within section 7 (Deprecated).

**Mandatory fields:**
- Section ID (`<section>.<n>`, e.g., `7.1`)
- Field/Module name being deprecated
- Canonical source (the replacement; what new code should use)
- Notes (state of the deprecated thing: row count if a table, reader inventory if code, etc.)
- Phase 5 backlog reference (specific phase number, e.g., "Phase 5.X.Y")

**Conditional fields (with triggers):**
- **If the deprecated thing has active readers** (e.g., legacy `predictions` table read by `prediction_router.py` and `dashboard_router.py`): enumerate readers per § 4.5 source-priority discipline
- **If the deprecation is partial** (e.g., the thing exists but is read by only one path which is itself slated for removal): document the dependency chain
- **If the deprecation produced a Forbidden Pattern** (e.g., "MUST NOT write to legacy `predictions` table"): cross-reference the Forbidden Pattern's section ID
- **If the deprecated thing is a superseded SQL constraint or schema element** (e.g., migration 011 added `wr_predictions` UNIQUE constraint that superseded the migration 005 form): the prior form qualifies for a Deprecated entry IF the superseded form persists in the DB schema (verifiable via `\d <table>` or migration history). The Deprecated entry documents the prior form, the superseding migration, and the planned removal in `PHASE_5_BACKLOG.md`. If the superseded form has been physically dropped (DDL operation removed it), the Deprecated entry is NOT required — the migration history serves as immune memory. **Determination at drafter discretion with verification log entry:** the drafter records in the verification log whether the superseded form persists or has been physically dropped, with the verification command output (e.g., `psql ... \d wr_predictions` showing the current constraint state).

### 5.7 Convergence rule on Discipline rule rosters (closes G5)

§ 5 (Discipline rules) of each Phase 1 bible holds Forbidden Patterns and Common Mistakes for that bible's domain. The roster of rules (which rules belong, in what numeric order, with what scope) is determined per-bible by Phase 1 drafters from substrate analysis, NOT pre-specified by this document. Each bible's domain has different discipline needs; pre-specified minimum lists either over-constrain (forcing irrelevant rules) or under-constrain (omitting real ones).

**Convergence rule (locked per v4 cycle):** Phase 1 drafters enumerate candidate rules from substrate (the bible's domain code, AWS infrastructure, prior audits, Phase 0 anti-pattern catalog at META_PLAN v8 § 9.1-9.13, operator-stated history). The candidate roster is surfaced to QB for ratification BEFORE § 5 of the bible locks. QB synthesizes the candidate roster against:
- Cross-bible coherence (does this rule belong here, or in another bible whose discipline more directly enforces it per § 5.3 cross-cutting scope rule?)
- Tony's prior ratifications (does Tony's locked language in META_PLAN v8 or the bible's own drafting spec name this rule? If yes, ratification is automatic; if no, QB surfaces to Tony.)
- Substrate grounding (is the rule traceable to verifiable EE patterns? Per AUDIT_METHODOLOGY v2 § 5.1 verification-log precision, ungrounded rules are flagged.)

**Workflow (one round trip per bible during § 5 drafting):**
1. CC drafts § 5 with candidate roster (FORBIDDEN/CORRECT pairs per § 5.6.2; Common Mistakes per § 5.6.3).
2. CC produces § 5 verification log delta enumerating each candidate rule's substrate evidence + provenance.
3. QB reviews candidate roster + verification log; decides which to ratify, which to surface to Tony, which to drop.
4. CC re-drafts § 5 to match ratified roster.
5. § 5 locks; the rest of the bible can proceed to lock per its own cycle.

**Provenance discriminator (mirrors methodology-interpolation grandfathering pattern per META_PLAN v8 § 6.1):** rules surfaced from existing locked Phase 0 documents (META_PLAN v8 § 9.X anti-patterns; BIBLE_STRUCTURE_SPEC v4 § 9.X if any) are grandfathered; CC-introduced rules require QB ratification.

**Cycle cost:** small (one round trip per bible). Cross-bible roster convergence value: high (audit-CC catches roster drift via § 5.2 methodology-interpolation check; QB ratification before lock is cheaper than post-lock revision).

**Candidate-roster numbering (locked per v6 cycle, closes G-new-1):** Candidate-roster entries pre-ratification use numeric sub-section IDs (`5.1`, `5.2`, ...) consistent with the ratified-entry convention per § 5.5. The "candidate" status is conveyed by the bible's § 5 header marker (`[candidate roster pending QB ratification per § 5.7]`) — not by a provisional letter-prefix. W.N remains the only ratified letter-prefix per § 5.5.1; provisional letter-prefixes (e.g., `5.A`, `5.B` for unratified candidates) are NOT authorized. QB ratification preserves the drafter-chosen numeric IDs where the candidate is ratified as-is; renumbering occurs only when QB drops, merges, or reorders candidates during ratification. Pattern-completion check (per AUDIT_METHODOLOGY v2 § 5.5) confirms compliance: numeric sub-section IDs for candidates do not introduce a new letter-prefix.

---

## 6. Per-Document Templates

For each of the seven Phase 1 bibles, this section provides:

- Filename
- Stated purpose
- Domain-specific TOC sections at 4.X positions
- Per-section content guidance with Mandatory / Conditional structure
- Cross-references to other bibles
- Anchor verifications

**All seven per-document templates use the canonical 5/6/7/8 ordering** for discipline-rule + bug-history sections (per Tony's v3-cycle Finding 1 ratification). Domain-specific content lives at 4.X sub-positions; the 5–8 group is fixed across all bibles.

### 6.1 architecture_overview.md

**Purpose:** answer "what does EE look like at the runtime-context level, and how do I find which bible to read for X?" Audience: any reader who needs the system map or needs to navigate to a specific bible.

**TOC (sections 5–8 mandatory per § 5.2; sections 1–4 recommended-strongly with drafter latitude per locality of reference):**

1. Scope of this bible
2. Definitions
3. System topology (runtime-context level)
   - 3.1 Lambda inventory and roles
   - 3.2 ECS Fargate training fleet
   - 3.3 Aurora Serverless cluster
   - 3.4 S3 buckets
   - 3.5 API Gateway v2 (`gb5qlfy10h`)
   - 3.6 EventBridge schedule
   - 3.7 ECR repositories
   - 3.8 SNS, Secrets Manager
4. Canonical cross-runtime objects and INDEX
   - 4.1 Race / Entry / PastPerformance / Workout / Result / Prediction (`backend/models/canonical.py`)
   - 4.2 Per-pipeline prediction shapes (WRPrediction / PLPrediction / LSPrediction)
   - 4.3 INDEX (cross-bible navigation)
     - Bible-by-bible one-line summary with hyperlinks
     - Common navigation paths ("if you need to know X, start here")
5. Discipline rules (Forbidden Patterns + Common Mistakes for cross-runtime invariants)
6. Currently Open
7. Deprecated
8. What Was Fixed

**Per-section content guidance:**

**§ 3.1 Lambda inventory:**
- **Mandatory:** for each of the 8 Lambda functions: name, memory, timeout, current State (Active / INACTIVE), the action(s) it dispatches.
- **Conditional (with triggers):**
  - If INACTIVE: include StateReason from `aws lambda get-function`, last-modified date, cross-reference to `PHASE_5_BACKLOG.md` entry for re-activation if any exists.
  - If Active: cross-reference Data Pipeline Bible flow that uses this Lambda.
  - If has multiple actions: enumerate per action with parameters.

**§ 3.6 EventBridge schedule:**
- **Mandatory:** for each of the 13 rules: rule name, cron expression, target Lambda, current State (ENABLED / DISABLED).
- **Conditional (with triggers):**
  - If DISABLED: state the reason (operator decision, replaced by per-model lineup, etc.).
  - For every rule: cross-reference Data Pipeline Bible's per-flow section that documents the runtime behavior of the cron.

**§ 4 Canonical objects:**
- **Mandatory:** for each dataclass in `backend/models/canonical.py`: field list with types, one-line semantic summary.
- **Conditional (with triggers):**
  - If the dataclass corresponds to a DB table: cross-reference Database & Schema Bible's per-table section.
  - If the dataclass is consumed by an inference service: cross-reference ML Layer Architecture Bible's per-pipeline section.

**§ 4.3 INDEX:**
- **Mandatory:** bullet list of the six other bibles with one-line summary per bible.
- **Conditional (with triggers):**
  - If a reader-need pattern has a canonical entry-bible (e.g., "if you're debugging a feature, start with Feature Provenance Bible"): document the navigation path.

**§ 5 Discipline rules:**
- **Mandatory:** Forbidden Patterns and Common Mistakes scoped to cross-runtime invariants. Phase 1 drafter enumerates as patterns surface. (Architecture Overview is unlikely to be the canonical home for many discipline rules — most are scoped to a more specific bible. Empty-or-near-empty is acceptable; document explicitly.)
- **Conditional (with triggers):**
  - If a pattern produced by a specific bug: cross-reference the canonical W.N entry per § 5.3.

**§ 6 Currently Open / § 7 Deprecated:** likely empty for Architecture Overview at lock; document explicitly with "No current open issues at lock" / "No deprecated entries at lock."

**§ 8 What Was Fixed:**
- **Mandatory** per § 5.6.1.
- **Conditional** per § 5.6.1.
- Architecture Overview is unlikely to be the canonical home for many bugs — most bugs are scoped to a more specific bible. This bible's What Was Fixed section may have few entries; that's expected.

**Cross-references to other bibles:** Architecture Overview is the most-cross-referencing bible by design. Every other bible's Scope section cross-references back here for the system topology.

**Anchor verifications (inherited from META_PLAN v6 verification log):**
- 8 Lambdas (Claim 1) — decomposed as 5 Active + 3 INACTIVE
- 13 EventBridge rules (Claim 3) — decomposed as 10 ENABLED + 3 DISABLED
- 41 API routes (Claim 8)
- 4 S3 buckets (Claim 18)
- 5 ECR images in CDK assets bucket (Claim 17)
- 3 Secrets (Claim 19)
- 5 ECS task families (Claim 20) — fully enumerated

### 6.2 data_pipeline_bible.md

**Purpose:** answer "how does data move from external source to DB to model to API?" Audience: anyone touching ingestion, scrapers, results-matching, retraining schedule.

**TOC (sections 5–8 mandatory per § 5.2; sections 1–4 recommended-strongly with drafter latitude per locality of reference):**

1. Scope
2. Definitions (HRN, NYRA, Equibase chart, "qualifying track")
3. Pipeline overview
4. Pipeline detail
   - 4.1 Per-flow detail
     - 4.1.1 Daily ingestion (race cards) — `equine-ingestion-daily` cron
     - 4.1.2 Nightly results fetch — `equine-fetch-results-nightly` cron
     - 4.1.3 Chart parser (S3 PDFs → results enrichment)
     - 4.1.4 NYRA workout scrape — `equine-nyra-workouts-daily` cron
     - 4.1.5 Daily inference (3 separate Lambdas: WR / PL / LS)
     - 4.1.6 Results matcher — `equine-results-daily` cron
     - 4.1.7 Angle stats refresh — `equine-angle-stats-nightly` cron
     - 4.1.8 Daily retraining — `equine-daily-retrain-full` cron
     - 4.1.9 Weekly retraining — `equine-weekly-retrain-wr` cron
   - 4.2 Data Acquisition Honesty Protocol (per META_PLAN v6 § 7.9)
     - 4.2.1 HRN entries
     - 4.2.2 HRN results
     - 4.2.3 HRN workouts
     - 4.2.4 NYRA workouts
     - 4.2.5 Equibase chart parser path
     - 4.2.6 (`equibase_probe/` exploratory work)
5. Discipline rules (Forbidden Patterns + Common Mistakes for data-acquisition discipline)
6. Currently Open
7. Deprecated
8. What Was Fixed (canonical home for Bug #28)

**Per-section content guidance:**

**§ 4.1 Per-flow detail (one sub-section per flow):**
- **Mandatory:** trigger (cron expression or manual invocation), source (HRN / NYRA / Equibase / manual), destination tables, Lambda(s) involved, action name(s) dispatched.
- **Conditional (with triggers):**
  - If the flow has known failure modes: enumerate with date discovered, manifestation symptoms (DB row patterns, log signatures, downstream model degradation).
  - If the flow is currently impaired (e.g., source Lambda is INACTIVE): document the impairment with cross-reference to the canonical impairment bible (Architecture Overview's Lambda inventory).
  - If the flow is canonically home to a What Was Fixed entry: cross-reference per § 5.3 (Bug #28 → § 8.W.<n> in this bible).
  - If the flow's failure mode is currently in `PHASE_5_BACKLOG.md`: cite the phase number.

**§ 4.2 Data Acquisition Honesty Protocol entries (per META_PLAN v6 § 7.9):**
- **Mandatory** (per source: HRN entries, HRN results, HRN workouts, NYRA workouts, Equibase chart parser, equibase_probe/):
  - What the source provides (specific tables/fields populated)
  - Current reliability state (verified empirically, not assumed)
  - Failure manifestation (DB row symptoms, log signatures, downstream model degradation)
  - Current acquisition mode (autonomous / monitored / scheduled-manual / paid-replacement per META_PLAN v6 § 3.5 disposition vocabulary)
  - Honest disposition (what the mode SHOULD be, with rationale)
- **Conditional (with triggers):**
  - If the source has recent failure history: include dates with the symptom statement (verbatim from operator memory file where applicable, per META_PLAN v6 verification log Claim 15c pattern).
  - If the source's honest disposition differs from current mode: flag the discrepancy and reference Phase 4 for the keep/refactor/replace/kill decision.

**§ 5 Discipline rules:** Forbidden Patterns and Common Mistakes scoped to data-acquisition discipline. Candidate Forbidden Pattern surfaced by Bug #28: "positional column indexing in scrapers without column-header verification." Sub-numbered as 5.1, 5.2, etc.

**§ 8.W.<n> Bug #28 canonical entry:**
- Per § 5.6.1 mandatory + conditional fields.
- **Required verbatim quote** from operator memory file's symptom statement (per META_PLAN v6 Claim 15c): "Place, show, and exacta payouts still populate."
- **DD pool extraction nuance** documented separately: the operator memory file flags `hrn_scraper.py:814` ("pool" table loop) as "likely has the same root cause" — distinct from the `daily_double_payout` field already accounted for in the result-dict. This nuance has its own section identifier (e.g., `8.W.<n+1>`) until Phase 1 audit verifies the DD-pool-extraction status.

**Cross-references to other bibles:**
- ML Layer Architecture Bible § 4 (model gallery) — the 3 daily-inference Lambda flows feed the gallery
- Model Evaluation & Retraining Bible § 4 (retrain triggers) — the daily/weekly retrain crons are operational instances of retrain triggers
- Database & Schema Bible § 4 (table descriptions) — every flow's destination table is documented there

**Anchor verifications:**
- 13 EventBridge rules (Claim 3) — decomposed as 10 ENABLED + 3 DISABLED
- Bug #28 line ref `hrn_scraper.py:802-804` (Claim 15)
- Bug #28 per-payout decomposition (Claim 15c) including the DD pool extraction nuance at line 814

### 6.3 feature_provenance_bible.md (FF1)

**Purpose:** answer "if I change feature X, what breaks?" Audience: feature-centric change-impact analysis.

**TOC (sections 5–8 mandatory per § 5.2; sections 1–4 recommended-strongly with drafter latitude per locality of reference):**

1. Scope (this bible's slice of the ML system: feature × model traceability)
2. Definitions (feature, latent factor, FE module, training-side vs inference-side)
3. Feature engineering architecture overview
   - 3.1 The two-FE-implementation reality (`model/shared/data_loader.py` training vs `backend/services/feature_engineering_service.py` inference)
   - 3.2 The single-source-of-truth pattern (`model/shared/gonzo_features.py` as the only shared module)
   - 3.3 The manual-cross-reference pattern (the remaining base features kept in lockstep by review)
4. Feature × model documentation
   - 4.1 Per-feature provenance
     - 4.1.X.<feature_name> — one subsection per documented feature
   - 4.2 Per-model feature consumption
     - 4.2.X.<model_name> — one subsection per model with its feature schema
5. Discipline rules
6. Currently Open
7. Deprecated
8. What Was Fixed (canonical home for Bug #15 chain since the prevention is a feature-engineering pattern per META_PLAN v6 § 7.4)

**Per-section content guidance:**

**§ 3.1 The two-FE-implementation reality:**
- **Mandatory:** documents the structural duplication; verifies file paths and key import sites. Names the 14 Gonzo Sauce features (per META_PLAN v6 Claim 24 — decomposed as Speed (4) + Trajectory (7) + Class (3) = 14).
- **Conditional (with triggers):**
  - If a feature is in the gonzo subset: document its single-source-of-truth location.
  - If a feature is in the remaining base set: document its training-side and inference-side implementations with file:line ranges.

**§ 3.2 Single-source pattern:**
- **Mandatory:** verbatim quote of the `gonzo_features.py` docstring (per META_PLAN v6 Claim 25). Documents the 2 import sites with their qualified-name divergence (per META_PLAN v6 Claim 27): `model/shared/data_loader.py:45` (`from shared.gonzo_features`) and `backend/services/feature_engineering_service.py:16` (`from model.shared.gonzo_features`).
- **Conditional (with triggers):**
  - If a future feature is extracted to gonzo_features.py: update this section with the new feature's name and import site.
  - If the qualified-name divergence is resolved: document the change with a dated lock point per § 5.4.

**§ 4.1 Per-feature provenance (one subsection per feature):**
- **Mandatory:**
  - Feature name + canonical definition
  - Source data (which raw DB column or computed input)
  - Training-side engineering location (file:line range)
  - Inference-side engineering location (file:line range, OR "shared module" with cross-reference to § 3.2)
  - Consuming model(s) — list by `model_versions.version_name`
  - Target latent (which predictive concept this feature aims to capture)
  - Drift risk (single-source vs parallel-implementation)
- **Conditional (with triggers):**
  - If the feature has been involved in a Bug #15-class drift: cross-reference the canonical W.N entry.
  - If the feature is in the RANKER_FULL_CULL set: note the cull and its discipline.

**§ 4.2 Per-model feature consumption (one subsection per model):**
- **Mandatory:** the feature_list JSONB from `model_versions` is the canonical source. Document with verification: query the `model_versions` table or the dashboard endpoint and record the exact feature_list at lock time. The listed features ARE what the model was trained on.
- **Conditional (with triggers):**
  - If the inference path computes different features than the feature_list indicates: that's a Bug #15-style drift surface — flag in Currently Open and cross-reference the canonical W.N.
  - If the model is currently active (per `is_active=TRUE`): note the active-row count and the (model_type, style) pair this row covers.

**§ 5 Discipline rules:** Candidate Forbidden Pattern (from § 7.5 v6 candidate): "Adding feature engineering logic to either training or inference path without parallel update to the other." Sub-numbered as 5.X.

**§ 8.W.<n> Gonzo extraction (canonical home for Bug #15):**
- Per § 5.6.1 mandatory + conditional fields.
- **Required:** verbatim quote of the "three calibration bugs in one week" claim (per META_PLAN v6 Claim 25) from `gonzo_features.py:7-11` docstring.
- Cross-referenced from `ml_layer_architecture_bible:8` and `model_evaluation_retraining_bible:8` by ID.
- The fully-worked example for this entry is at § 5.6.1.1 above.

**Cross-references to other bibles:**
- ML Layer Architecture Bible § 4 — model definitions consume features documented here
- Model Evaluation & Retraining Bible § 4 — retraining triggers may include feature-schema-drift detection
- Database & Schema Bible § 4 — raw data source columns

**Anchor verifications:**
- 14 Gonzo Sauce features (Claim 24)
- "Three calibration bugs in one week" verbatim (Claim 25)
- 2 import sites with divergent qualified names (Claim 27)
- `model/features/feature_definitions.py` runtime state (Claim 10)

**Convergence test trace:** this bible satisfies META_PLAN v6 § 3.2.1 Forcing Function 1.

### 6.4 ml_layer_architecture_bible.md (FF2)

**Purpose:** answer "if I add a new ML layer, where does it plug in?" Audience: model-centric composition design.

**TOC (sections 5–8 mandatory per § 5.2; sections 1–4 recommended-strongly with drafter latitude per locality of reference):**

1. Scope (model composition; not feature-engineering, not retraining-process)
2. Definitions (model_type, style, specialist, calibration sidecar, per-pipeline prediction)
3. Model gallery overview
   - 3.1 Model registry semantics (`model_versions` table; multi-active-row reality)
   - 3.2 Per-pipeline structure (WR / PL / LS as distinct inference services + Lambdas)
   - 3.3 The 7-layer LS stack
4. Model and pipeline detail
   - 4.1 Per-model detail
     - 4.1.X.<version_name> — one subsection per active model
   - 4.2 Inference pipeline composition
     - 4.2.1 WR pipeline (`equine-wr-inference` Lambda → `WRInferenceService`)
     - 4.2.2 PL pipeline (`equine-pl-inference` Lambda → `PLInferenceService`)
     - 4.2.3 LS pipeline (`equine-ls-inference` Lambda → `LSInferenceService`)
   - 4.3 Calibration / bypass state
     - 4.3.1 Current state: ALL styles bypass at inference
     - 4.3.2 Calibration sidecars in S3 (gonzo_sauce only)
     - 4.3.3 Bug #15 → Bug #24 chain producing the bypass
5. Discipline rules
   - 5.1 (Forbidden Pattern) — Calling `get_active_model_by_type` without addressing multi-active-row reality (per META_PLAN v6 § 9.13 and Appendix A.1)
6. Currently Open
7. Deprecated
8. What Was Fixed (cross-references to `feature_provenance_bible:8.W.<n>` for Bug #15 canonical)

**Per-section content guidance:**

**§ 3.1 Model registry semantics:**
- **Mandatory:** registry total decomposed as 88 = 45 active + 43 inactive (per META_PLAN v6 Claim 7, verified live 2026-05-04). The multi-active-row reality (per META_PLAN v6 § 9.13) is the load-bearing observation. Document the `get_active_model_by_type` signature and SQL verbatim per META_PLAN v6 Claim 9.
- **Conditional (with triggers):**
  - If the active count differs from 45 at lock time: document the new decomposition with verification log entry.
  - If a style-aware variant of `get_active_model_by_type` is added (Phase 5.X.Y): update the section and cross-reference the resolution path.

**§ 3.3 The 7-layer LS stack:**
- **Mandatory:** per META_PLAN v6 § 9.3 CORRECT example, the canonical layer naming is: WR (binary win XGBoost) / ranker (LambdaMART rank:pairwise) / value overlay (arithmetic, not trained) / longshot RandomForest classifier / trajectory LSTM / Bayesian angle scorer / ensemble (logistic regression meta-learner). Cross-reference dump § 3 for per-layer training file paths and active-version names; verify against live dashboard at lock time.
- **Conditional (with triggers):**
  - If a layer is currently impaired (e.g., calibration bypassed): note the impairment with cross-reference to § 4.3.
  - If a layer's active version differs from the most-recent-trained version: explain the discrepancy.

**§ 4.1 Per-model detail (one subsection per active model):**
- **Mandatory:** version_name, model_type, training script path, inference path (Lambda + Service class), output fields written to which prediction table, feature_list (cross-reference Feature Provenance Bible § 4.2).
- **Conditional (with triggers):**
  - If the model has a calibration sidecar in S3: document the sidecar path and current load state (loaded vs bypassed per § 4.3).
  - If the model is one of multiple active rows for its model_type: document the (model_type, style) pair this row covers.

**§ 4.3 Calibration / bypass state:**
- **Mandatory:** § 4.3.1 documents the current bypass at `wr_inference_service.py:616-626` (per META_PLAN v6 Claim 26 — comment block at 616-625, bypass operation `handicapping_probs = ranker_probs.copy()` at line 626). § 4.3.3 cross-references the Bug #15 → Bug #24 chain.
- **Conditional (with triggers):**
  - If the bypass is lifted (Phase 5.X.Y resolution): update with new dated lock point per § 5.4.
  - If a sidecar is added for a style other than gonzo_sauce: document with verification.

**§ 5.1 Forbidden Pattern:**
- Per § 5.6.2 mandatory + conditional fields.
- The full FORBIDDEN/CORRECT pair from META_PLAN v6 Appendix A.1 with the three-piece pattern: the function, the multi-active-row reality, and the missing style-aware variant as a tracked Phase 5 item (per META_PLAN v6 § 9.13).

**Cross-references to other bibles:**
- Feature Provenance Bible § 4.2 — per-model feature consumption
- Model Evaluation & Retraining Bible § 4 — per-model success criteria, retrain triggers
- Data Pipeline Bible § 4.1.5 — daily inference Lambda flows

**Anchor verifications:**
- Model registry counts: 88 = 45 active + 43 inactive (Claim 7)
- `get_active_model_by_type` signature (Claim 9)
- Calibration bypass line range (Claim 26)

**Convergence test trace:** this bible satisfies META_PLAN v6 § 3.2.1 Forcing Function 2.

### 6.5 model_evaluation_retraining_bible.md (FF3)

**Purpose:** answer "is this model still working, when do I retrain it, what gates deployment?" Audience: process-centric operational discipline.

**TOC (sections 5–8 mandatory per § 5.2; sections 1–4 recommended-strongly with drafter latitude per locality of reference):**

1. Scope (operational discipline for the model gallery; not composition, not feature-engineering)
2. Definitions (success criterion, retrain trigger, calibration discipline, deployment gate, artifact version)
3. Per-model success criteria
   - 3.X.<version_name> — one subsection per active model
4. Operational discipline
   - 4.1 Retraining triggers
     - 4.1.1 Scheduled retrains (cron-based — `equine-daily-retrain-full`, `equine-weekly-retrain-wr`)
     - 4.1.2 Data drift detection (current state: none; Phase 5 candidate)
     - 4.1.3 Performance degradation thresholds (current state: operator-judgment; Phase 5 candidate)
   - 4.2 Calibration discipline as process
     - 4.2.1 Current state: ALL styles bypass at inference (cross-reference `ml_layer_architecture_bible:4.3.1`)
     - 4.2.2 Calibration sidecar fitting (where, when, by what code)
     - 4.2.3 The Bug #15 → Bug #24 chain (cross-reference `feature_provenance_bible:8.W.<n>` and § 8.W.<n> below for Bug #24 canonical)
   - 4.3 Model artifact version control
     - 4.3.1 The `is_active` flag and its multi-row semantics (cross-reference `ml_layer_architecture_bible:3.1`)
     - 4.3.2 S3 artifact paths (`s3://equine-model-artifacts/<family>/<version>.json`)
     - 4.3.3 ECR image tags for ECS training tasks (cross-reference `architecture_overview:3.7`)
   - 4.4 Deployment gating
     - 4.4.1 Current state: manual operator decision (`set_active_model` action on `equine-ingestion`)
     - 4.4.2 What must be true for a new artifact to ship to production
5. Discipline rules
6. Currently Open
7. Deprecated
8. What Was Fixed
   - 8.W.<n> — Bug #24 (calibration + 0-PP override interaction); canonical home for Bug #24 since the prevention is a calibration-applied-as-process discipline.

**Per-section content guidance:**

**§ 3 Per-model success criteria:**
- **Mandatory:** for each active model, document the metric the model is judged on (top1_accuracy, exacta_hit_rate, calibration_score, etc. — these are columns in `model_versions`), current value at lock time.
- **Conditional (with triggers):**
  - If the model has a historical performance trend visible from registry rows (multiple training_dates over time): document the trend.
  - If the metric value at lock time is below a documented threshold: cross-reference Currently Open / PHASE_5_BACKLOG.
  - If "current state: not codified" applies to the threshold (operator judgment): state honestly.

**§ 4.1 Retraining triggers:**
- **Mandatory:** § 4.1.1 documents what runs on cron (per Architecture Overview § 3.6 cross-reference). § 4.1.2 and § 4.1.3 explicitly document the absence of automated drift detection or threshold-based retrains.
- **Conditional (with triggers):**
  - If a Phase 5 candidate item is documented: cross-reference `PHASE_5_BACKLOG.md` by phase number per META_PLAN v6 § 9.9.

**§ 4.2 Calibration discipline:**
- **Mandatory:** § 4.2.2 documents the calibration-fitting code paths surfaced from dump § 1 (`scripts/fit_*_calibrations.py` — the dump cites 4 calibration scripts; Phase 1 drafter re-verifies script names by `ls scripts/fit_*_calibrations.py` at draft time).
- **Conditional (with triggers):**
  - If calibration is fitted but bypassed at inference: document both the fitting and the bypass state.
  - If a calibration sidecar's S3 path differs from the convention: document the deviation.

**§ 4.4.2 Deployment gating:**
- **Mandatory:** the current discipline (or lack thereof) for "what must be true." Document: is there a hold-out test pass? A diff-of-feature-list check?
- **Conditional (with triggers):**
  - If "current state: operator judgment" applies: state honestly with cross-reference to Phase 5 candidate for hardened gating.
  - If a specific gate exists in code: document with file:line.

**§ 8.W.<n> Bug #24 (canonical):**
- Per § 5.6.1 mandatory + conditional fields.
- Cross-referenced from `ml_layer_architecture_bible:8` by ID.

**Cross-references to other bibles:**
- ML Layer Architecture Bible § 4.3 — calibration / bypass state at the model-composition level
- Feature Provenance Bible § 8 — Bug #15 (canonical)
- Data Pipeline Bible § 4.1.8, § 4.1.9 — daily/weekly retraining cron flows

**Anchor verifications:**
- Calibration bypass at `wr_inference_service.py:616-626` (Claim 26)

**Convergence test trace:** this bible satisfies META_PLAN v6 § 3.2.1 Forcing Function 3.

### 6.6 database_schema_bible.md

**Purpose:** answer "what tables exist, what columns are canonical, how do migrations work, what JSONB conventions apply?" Audience: anyone touching schema, repos, or migrations.

**TOC (sections 5–8 mandatory per § 5.2; sections 1–4 recommended-strongly with drafter latitude per locality of reference):**

1. Scope
2. Definitions (table, materialized view, migration, JSONB shadow, canonical column)
3. Schema overview
   - 3.1 14 tables (decomposed list)
   - 3.2 1 materialized view (`trainer_stats`)
   - 3.3 Schema bootstrap (`backend/database/schema/schema.sql`) vs migrations
4. Schema and migration detail
   - 4.1 Per-table documentation
     - 4.1.X.<table_name> — one subsection per CREATE TABLE declaration; matviews documented at § 3 only (per § 2 Definitions table-vs-matview distinction; closes G-new-2)
   - 4.2 Migration discipline (per META_PLAN v6 § 7.12)
     - 4.2.1 Numbering format (grandfathered 001–011 + NNN_YYYYMMDD from 012+)
     - 4.2.2 The duplicate-005 case
     - 4.2.3 The `schema_migrations` runner mechanism
     - 4.2.4 Rollback format (in-file down-block)
     - 4.2.5 Migration testing (non-production database first)
5. Discipline rules
   - 5.1 UNIQUE constraints (per dump § 4.1 notable schema constraints)
   - 5.2 JSONB conventions (where present; what fields, what shapes)
   - 5.3 Cross-table FK conventions
6. Currently Open
7. Deprecated
   - 7.1 Legacy `predictions` table (per META_PLAN v6 Appendix A.4; canonical home for the legacy-table deprecated entry)
8. What Was Fixed

**Per-section content guidance:**

**§ 3.1 14 tables:**
- **Mandatory:** the decomposed list per META_PLAN v6 Claim 4 (verified 2026-05-04). Phase 1 drafter cross-checks the list against `grep -hE "^CREATE TABLE" backend/database/schema/schema.sql backend/database/migrations/*.sql` at draft time and records any drift in the verification log.
- **Conditional (with triggers):**
  - If a new table is added between v6 lock and v1 Phase 1 lock: document with verification log entry.

**§ 4.1 Per-table documentation (one subsection per table):**
- **Mandatory:**
  - Column list with types
  - Primary key
  - Purpose
  - Primary writers (which Lambda or service writes)
  - Primary readers (which router or service reads)
- **Conditional (with triggers):**
  - If has UNIQUE constraints: enumerate.
  - If has FK constraints: enumerate.
  - If has JSONB columns: document JSONB shape per § 5.2 conventions.
  - If has approximate row count available from live dashboard: cite count with verification log entry (e.g., `predictions: 6,600` per META_PLAN v6 Claim 16).

**§ 4.2 Migration discipline:**
- **Mandatory:** the full grandfathering rule per META_PLAN v6 § 7.12. The 12 existing migration filenames (verified) listed inline in § 4.2.1. The duplicate-005 case (`005_backfill_pace_delta.sql` and `005_three_prediction_tables.sql`) documented in § 4.2.2 with the operational note that lexical sort orders them deterministically and the migration runner sees them as opaque distinct filenames. § 4.2.3 documents the `schema_migrations` table mechanism per META_PLAN v6 Claim 6.
- **Conditional (with triggers):**
  - If migration 012+ has been authored by Phase 1 lock time: document the cutover with the new format example.
  - If a migration's rollback path is non-reversible: document the rationale per META_PLAN v6 § 7.12 illustrative example.

**§ 7.1 Legacy `predictions` table (Deprecated entry):**
- Per § 5.6.4 mandatory + conditional fields.
- Reader inventory decomposed: prediction_router.py = 1 import + 3 instantiations = 4 references; race_router.py = 1 import + 1 instantiation = 2 references.
- Live row count: 6,600 (per dashboard at v6 lock).

**Cross-references to other bibles:**
- ML Layer Architecture Bible § 4 — per-pipeline inference writers
- Feature Provenance Bible § 4 — raw data source columns
- Data Pipeline Bible § 4 — flows that write each table
- API & Frontend Bible § 4 — the routers that read from `predictions`

**Anchor verifications:**
- 14 tables + 1 matview (Claim 4)
- 12 migration files (Claim 5) — including duplicate-005
- `schema_migrations` runner (Claim 6)
- Legacy `predictions` row count and reader inventory (Claim 16)

### 6.7 api_frontend_bible.md

**Purpose:** answer "what HTTP routes exist, what does each Lambda dispatch to, how does the frontend consume them?" Audience: anyone touching the API surface or the React SPA.

**TOC (sections 5–8 mandatory per § 5.2; sections 1–4 recommended-strongly with drafter latitude per locality of reference):**

1. Scope
2. Definitions (Lambda-handler-as-router, axios client, route key, integration target)
3. API overview
   - 3.1 API Gateway v2 configuration (`gb5qlfy10h`)
   - 3.2 Per-domain route count (Shared / Generic predictions / WR / PL / LS — per dump § 6.5)
   - 3.3 Lambda integration mapping (route → Lambda)
   - 3.4 Lambda-handler-as-router pattern (`def get_*` / `def post_*` in `backend/routers/`)
4. Route, frontend, and consumption detail
   - 4.1 Per-route detail
     - 4.1.X.<route_key> — one subsection per of the 41 routes
   - 4.2 Frontend consumption
     - 4.2.1 axios client (`frontend/src/api/client.ts`)
     - 4.2.2 BASE_URL fallback chain (env → localhost → API Gateway)
     - 4.2.3 Per-domain function exports
   - 4.3 Frontend pages and components
     - 4.3.1 9 pages (`frontend/src/pages/`)
     - 4.3.2 13 components (`frontend/src/components/`)
     - 4.3.3 State management (no external library; React state + axios inline)
5. Discipline rules
   - 5.1 (Forbidden Pattern) — Routers as passthroughs (no business logic). Anchored on DD § 1's Layer Boundary rule (DD bible line 38) — adapted to EE's `def get_*` / `def post_*` pattern.
6. Currently Open
7. Deprecated
8. What Was Fixed

**Per-section content guidance:**

**§ 3.2 Per-domain route count:**
- **Mandatory:** 41 routes total (per META_PLAN v6 Claim 8). Phase 1 drafter re-verifies the per-domain decomposition at draft time per dump § 6.5: Shared / Generic predictions / WR / PL / LS.
- **Conditional (with triggers):**
  - If the per-domain decomposition differs from the dump at re-verification: document the drift with verification log entry.

**§ 3.3 Lambda integration mapping:**
- **Mandatory:** per META_PLAN v6 § 8.5 AWS-vs-API resolution rule, the per-route integration mapping is the load-bearing dataset for the "INACTIVE-Lambda behavior" question. Phase 1 drafter records: route → integration target Lambda → current State of that Lambda.
- **Conditional (with triggers):**
  - If the integration target is currently INACTIVE: document observed route behavior (5xx, stale cache, fallback) per META_PLAN v6 § 8.5.
  - If a route has multiple integration paths: enumerate.

**§ 4.1 Per-route detail (one subsection per route):**
- **Mandatory:**
  - Method (GET/POST)
  - Path
  - Integration Lambda
  - Dispatched function name
  - Request shape
  - Response shape
- **Conditional (with triggers):**
  - If the route's integration target is INACTIVE: document current behavior under that condition.
  - If the route returns data from a deprecated source (e.g., legacy `predictions` table per § 6.6 § 7.1): cross-reference the Deprecated entry.

**§ 5.1 Routers as passthroughs:**
- **Mandatory** per § 5.6.2: dated lock point + rationale + FORBIDDEN/CORRECT pair.
- **Conditional (with triggers):**
  - If a router contains business logic (a violation): document as Currently Open with cross-reference to this Forbidden Pattern.

**§ 4.2 Frontend consumption:**
- **Mandatory:** the axios client structure; the per-domain function exports (`getAvailableDates`, `getHorsePPs`, etc. per dump § 7.3).
- **Conditional (with triggers):**
  - If a page consumes routes that touch INACTIVE Lambdas: cross-reference the per-route detail's INACTIVE-behavior documentation.

**Cross-references to other bibles:**
- Architecture Overview § 3.5 — API Gateway configuration
- Architecture Overview § 3.1 — Lambda inventory (for the Active/INACTIVE state per route)
- ML Layer Architecture Bible § 4.2 — per-pipeline inference services that the WR/PL/LS routes wrap

**Anchor verifications:**
- 41 routes (Claim 8)
- 9 pages + 13 components per dump §§ 7.1–7.2; Phase 1 drafter re-verifies live at draft time and records any drift in the verification log

---

## 7. Cross-Document Conventions

### 7.1 Cross-reference syntax

Within a bible: `§ <section_id>` (e.g., `§ 4.5.10`). Between bibles: `<bible_name>:<section_id>` (e.g., `feature_provenance_bible:8.W.7`; `ml_layer_architecture_bible:5.4`). For cross-cutting bug references: `<bible_name>:#<bug-id>` per § 3.3 + § 5.5.1. Matches META_PLAN v8 § 7.11.

Phase 1 drafters use these formats consistently in cross-reference text. Per-bible templates' "Cross-references to other bibles" guidance includes the worked examples in § 7.1.1 below.

#### 7.1.1 Cross-reference syntax worked examples (closes G6)

The cross-reference formats are mechanical. Drafters use these examples as the integration model when authoring cross-references in Phase 1 bibles:

- **Within-bible reference (numeric section):** `§ 4.5.10`
- **Within-bible reference (W.N entry):** `§ 8.W.3`
- **Cross-bible reference by section ID:** `feature_provenance_bible:5.4` (Forbidden Pattern in Feature Provenance Bible's § 5)
- **Cross-bible reference by W.N entry:** `feature_provenance_bible:8.W.3` (What Was Fixed entry W.3 in Feature Provenance Bible; W.N is bible-local per § 5.5)
- **Cross-bible reference by global Bug #N (cross-cutting bugs only):** `feature_provenance_bible:#15` (canonical home of Bug #15)
- **Cross-reference TO `PHASE_5_BACKLOG.md`:** by phase number, e.g., `Phase 5.X.Y` (per META_PLAN v8 § 9.9)

Drafters who introduce a new cross-reference format that doesn't match these examples surface for QB ratification before lock — pattern-completion of cross-reference vocabulary is subject to AUDIT_METHODOLOGY v2 § 5.5 pattern-completion check (cross-reference syntax extensions require explicit ratification).

### 7.2 Section identifier discipline (per META_PLAN v6 § 7.4 + § 7.5)

- **What Was Fixed entries:** `<section>.W.<n>` per § 5.5. Letter-prefix W is preserved for cross-bible bug-tracking forcing function.
- **All other discipline-rule entries** (Forbidden Patterns, Common Mistakes, Deprecated): sub-section numeric IDs per § 5.5.

Identifiers are stable across the bible's lifetime (renumbering breaks cross-references). When entries are added, they take the next available numeric ID; W.N entries are never removed (per META_PLAN v6 § 7.4 immune-memory discipline).

### 7.3 Lock dates on every rule

Per § 5.4 + META_PLAN v6 § 7.3 + § 9.8.

### 7.4 Cross-cutting bug canonical-home determination

(Restated from § 5.3.) Per META_PLAN v6 § 7.4. Determined at entry creation; tiebreaker criteria deferred to AUDIT_METHODOLOGY.md per § 5.3.

### 7.5 INDEX file question (resolves META_PLAN v6 § 10.2; Tony-ratified per v1 cycle)

The Architecture Overview's role as the most-cross-referencing bible serves the index function — every other bible's Scope section cross-references back to Architecture Overview, and Architecture Overview's per-section subsections (Lambda inventory, EventBridge, canonical objects, INDEX at § 4.3) cross-reference outward to the relevant bibles. A separate top-level `BIBLE_INDEX.md` is not created.

### 7.6 Repo-root pointer file (recommendation; Tony-ratified per v1 cycle)

A single-line pointer file at repo root is recommended: either `/BIBLE.md` or an extended `/README.md` section pointing to `/docs/bible/architecture_overview.md` as the EE Architecture Bible's entry point. Tony's call whether to ship.

---

## 8. Phase 1 Drafting Workflow (Per Bible)

### 8.1 Authority

Phase 1 bibles are Tier 3 per META_PLAN v6 § 4.1 + § 6.5. CC drafts under QB spec. Verification log required.

### 8.2 Recommended drafting order (Tony-ratified per v1 cycle as recommendation)

1. Architecture Overview first
2. Database & Schema Bible second
3. Data Pipeline Bible third
4. Feature Provenance / ML Layer Architecture / Model Evaluation & Retraining Bibles in parallel
5. API & Frontend Bible last

### 8.3 Per-bible cycle

1. QB writes Phase 1 spec (target questions, source-priority, verification mandate)
2. CC drafts + verification log. **Per META_PLAN v6 § 6.5 hard rule, drafts without verification logs are rejected by QB without audit; the verification log is not optional.**
3. QB reads draft fully; spot-checks verification log
4. QB writes audit-CC prompt (six adversarial questions per META_PLAN § 6.2 + Phase 2 additions per § 3.3)
5. CC audits
6. QB synthesizes; iterate until locked (Tony's threshold per META_PLAN v6 § 11: < 5 MATERIAL findings AND zero fabricated-content findings AND zero methodology-interpolation findings)
7. Bible locks; cross-document consistency audit (per META_PLAN § 3.3) runs after all bibles lock individually

### 8.4 Convergence test application

Per META_PLAN v6 § 3.2.1, after the three ML bibles lock, the convergence test runs: "given this inventory, can a fresh CC session evaluate, rebuild, or retrain a model in the gallery?" Specific success criteria deferred to CONVERGENCE_CRITERIA.md.

---

## 9. Verification Anchors (Inherited Plus New)

### 9.1 Inherited from META_PLAN v6 verification log

(Re-verified 2026-05-04 by re-running the original commands; all values held.)

| Inherited Claim | Used in spec § |
|---|---|
| Claim 1 (8 Lambdas, 5 Active + 3 INACTIVE) | § 6.1 |
| Claim 3 (13 EventBridge rules, 10 ENABLED + 3 DISABLED) | § 6.1, § 6.2 |
| Claim 4 (14 tables + 1 matview) | § 6.6 |
| Claim 5 (12 migrations, duplicate 005) | § 6.6 |
| Claim 6 (`schema_migrations` runner) | § 6.6 |
| Claim 7 (88 model registry, 45 active + 43 inactive) | § 6.4 |
| Claim 8 (41 API routes) | § 6.7 |
| Claim 9 (`get_active_model_by_type` signature) | § 6.4 |
| Claim 10 (`feature_definitions.py` not orphaned) | § 6.3 |
| Claim 15 (Bug #28 line ref `hrn_scraper.py:802-804`) | § 6.2 |
| Claim 15c (Bug #28 per-payout decomposition) | § 6.2 |
| Claim 16 (legacy `predictions` table state) | § 6.6 |
| Claim 17 (5 ECR images) | § 6.1 |
| Claim 18 (4 S3 buckets) | § 6.1 |
| Claim 19 (3 Secrets) | § 6.1 |
| Claim 20 (5 ECS task families enumerated) | § 6.1 |
| Claim 24 (14 Gonzo features) | § 6.3 |
| Claim 25 ("Three calibration bugs" verbatim) | § 6.3, § 5.6.1.1 |
| Claim 26 (calibration bypass line range) | § 6.4, § 6.5 |
| Claim 27 (gonzo_features.py 2 import sites) | § 6.3 |

### 9.2 New verifications introduced (v1 + v2 + v3)

v1 introduced 5 new claims (DD bible TOC, filename collision, META_PLAN cross-ref resolution, intra-doc cross-ref, filename mapping). v2 introduced 3 (cross-reference integrity, F./C./D. residue, position-8 consistency). v3 introduces 2 new claims:

- **Claim N9:** DD § 19 brevity confirmation (per Finding 3 honest-path resolution).
- **Claim N10:** Cross-reference integrity post-renumbering of § 6.1–§ 6.7 templates.

Total new claims across cycles: 10. Per-cycle verification log delta documented in respective verification logs.

---

## 10. Open Questions

### 10.1 Drafting order (recommended in § 8.2)

Tony-ratified per v1 cycle as recommendation, not mandatory order.

### 10.2 Top-level INDEX file (resolved in § 7.5)

Resolved per Tony's v1-cycle ratification.

### 10.3 Repo-root pointer file (recommendation in § 7.6)

Tony-ratified per v1 cycle as recommendation.

### 10.4 Frontend bible split (resolved in § 4.4)

Tony-ratified per v1 cycle: frontend stays as a section of the API & Frontend Bible.

### 10.5 Phase 1 audit cadence per bible

Cross-document audit cadence is a Phase 5 working-agreements decision per META_PLAN v6 § 7.13 deferral pattern.

---

## 11. Lock Status

**Document status:** LOCKED v6 (post-convergence-test-re-run surgical-cosmetic cycle closing G-new-1 + G-new-2)
**Audit-CC pass:** v4 audit clean (0 BLOCKER + 0 MATERIAL + 0 fabricated + 0 methodology-interpolation; 2 MINOR + 4 STYLE non-blocking); v5 cycle closed § 11 metadata pointer; convergence test re-run on v5/v8 substrate produced CONVERGED-WITH-RESIDUAL verdict (18 material differences + 2 NEW methodology gaps + 8 PASS / 1 PARTIAL / 0 FAIL on G1-G9 closures); v6 cycle closes the 2 NEW gaps (G-new-1, G-new-2) per Tony's locked Option (a) decisions on both. Per audit-CC's pre-approval, v6 cycle skips re-audit since scope is pure surgical-cosmetic embed of audit-CC-recommended resolutions.
**Verification log:** `_audits/BIBLE_STRUCTURE_SPEC_v6_verification.md` — 1 v6 entry (V6-1: 2 surgical embeds for G-new-1 + G-new-2 closures); inherits 1 V5-1 + 11 v4 (V4-1 through V4-11) + 27 v3-inherited (via v4) wholesale = 40 total claims.
**Tony review:** post-v6 lock confirmation
**Locked:** 2026-05-05

**Phase 0 prerequisites carried over from META_PLAN v6 § 11:**
- All 5 Phase 0 documents pass adversarial audit (Tony's threshold: < 5 MATERIAL findings AND zero fabricated-content findings AND zero methodology-interpolation findings)
- Operating-model convergence test passes (META_PLAN v6 § 5.4)
- EE production code committed to baseline (META_PLAN v6 § 3.1.1)
- `.gitignore` baseline audit performed; findings documented at `_audits/gitignore_baseline_audit.md` (META_PLAN v6 § 7.14)
- `PHASE_5_BACKLOG.md` created with Bug #28 as first entry (META_PLAN v6 § 8.2)

**Next action:** QB writes paste-ready audit-CC prompt for v3. Tony runs audit. QB synthesizes findings.

---

## 12. v3 Drafting Notes (CC self-check surfaces)

### 12.1 Constructs explicitly authorized by META_PLAN v6 or BIBLE_STRUCTURE_SPEC drafting specs

(Inherited from v2 § 12.1 — full list unchanged.) All ratifications carry forward: tier model, methodology-interpolation rule, source authority hierarchy, maintenance protocol, anti-patterns, ML floor, Tony's threshold, filename casing, `_bible` suffix asymmetry, recommended drafting order, recommended TOC ordering (within sections 1–4), W.N letter-prefix as the only letter-prefix, position-8 for What Was Fixed, § 4.2 four-subsection justification structure, § 6.X Mandatory/Conditional structure, § 5.6 four canonical templates, § 5.3 + § 7.4 explicit deferral. Per Tony's v3-cycle ratifications: canonical 5/6/7/8 ordering for discipline-rule + bug-history group; § 5.6.1.1 worked example; § 5.6.3 source-spec depth note.

### 12.2 v3 surfacing notes (delta from v2)

**Items resolved by Tony's v3 cycle decisions:**

- **Finding 1 (per-document TOC renumbering to align Discipline rules at section 5):** RESOLVED per Tony's Option I. All seven per-document templates now follow canonical 5/6/7/8 ordering. Domain-specific content consolidated under § 4.X sub-positions where needed (§ 6.3 § 4.1+§ 4.2; § 6.4 § 4.1+§ 4.2+§ 4.3; § 6.5 § 4.1+§ 4.2+§ 4.3+§ 4.4; § 6.6 § 4.1+§ 4.2; § 6.7 § 4.1+§ 4.2+§ 4.3). Empty Currently Open and Deprecated sections in some bibles are explicit ("No current open issues at lock"). § 5.2 canonical TOC text strengthened to mandate sections 5–8 ordering.

- **Finding 2 (§ 5.6.1 fully-worked example):** RESOLVED. § 5.6.1.1 added showing W.3 Gonzo Sauce FE Single-Source Extraction with each conditional trigger evaluated (FIRES / DOES NOT FIRE notation). Phase 1 drafters use this as the integration model.

- **Finding 3 (§ 5.6.3 Common Mistakes template depth honesty):** RESOLVED. Source-spec depth note added prefacing § 5.6.3, acknowledging META_PLAN v6 § 7.6 inherits DD § 19's brevity without expansion (DD § 19 brevity verified per Claim N9). Honest-path chosen over depth-parity to avoid pattern-completion interpolation.

**Cross-reference integrity post-renumbering:** verified per Claim N10. § 5.6.2 Forbidden Pattern example "section 5 of the ML Layer Architecture Bible is `ml_layer_architecture_bible:5.4`" now resolves correctly with § 6.4 placing Discipline rules at canonical position 5.

**New constructs introduced during v3 drafting that may verge on interpolation, applying the pattern-completion check:**

CC reviewed every new methodology construct introduced in v3 against the pattern-completion check.

1. **§ 5.2 "mandatory for sections 5–8 / recommended-strongly for sections 1–4" framing.** Tony's Option I instruction stated "renumber all seven per-document templates to match § 5.2's canonical order." This authorizes the canonical 5/6/7/8 mandate. The "recommended-strongly for sections 1–4" framing for the upper portion preserves v2's flexibility for domain-specific content. Pattern-completion check: the mandate-for-5-through-8 is anchored to Tony's instruction directly; the recommended-for-1-through-4 is a preservation of v2's existing language. **Not interpolation.** Surfaced for Tony's confirmation.

2. **§ 5.2 "Empty sections are explicit, not absent" rule.** Tony's spec instructed: "Even bibles with thin Currently Open or Deprecated sections include them as explicit empty (or near-empty) sections — better to have an empty 'no current open issues' section than a missing one that breaks cross-bible references." This is verbatim Tony language; the ratification is explicit. **Not interpolation.**

3. **§ 5.6.1.1 worked example using FIRES / DOES NOT FIRE notation.** Tony's spec explicitly required "Each conditional trigger explicitly evaluated (this is the load-bearing pedagogical content)" with the example showing each trigger with explicit evaluation. The FIRES / DOES NOT FIRE notation is CC's analytical translation of "explicitly evaluated" — could equally be "yes/no" or "applies/does-not-apply." Pattern-completion check: not a binary test, threshold, cadence, or rule — it's a notation choice for how to render the four conditional triggers (each individually authorized by the M-4 worked example). **Judged acceptable, not interpolation.** Surfaced for Tony's awareness.

4. **§ 5.6.3 "Phase 1 drafters expand entries with bug-class context and rationale as needed" language.** This is descriptive (drafters do work) rather than prescriptive (CC inventing a methodology rule). The framing acknowledges Phase 1 drafter discretion within the source-spec brevity acknowledged above. **Not interpolation.**

The methodology-interpolation rule is operative; the discipline of self-surfacing remains. v3 surfaces what's new.

### 12.3 Constructs explicitly NOT drafted (to avoid interpolation)

(Inherited from v2 § 12.3 — list unchanged.) No iteration cap; no completeness criterion; no minimum section count, word count, or FORBIDDEN/CORRECT pair count; no prescribed cadence for cross-document audit; no severity thresholds beyond META_PLAN v6; no tiebreaker criteria for canonical-home determination; no new letter-prefix conventions.

### 12.4 v4 surfacing notes (delta from v3)

**Items resolved by Tony's v4 cycle decisions (architectural questions G3 / G5 / G7 / G9):**

- **G3 (W.N for non-bug entries) — RESOLVED per Tony's Option (b).** § 8 confined to true bug-fix entries with mandatory Fix date. Discipline codifications routed to § 5 (Discipline rules). § 5.6.1 template scope clause added explicitly. The convergence test surfaced this when run2's 8.W.3 (past_performances.race_id NULL acceptance) violated the W.N template's mandatory Fix date field by carrying "locked 2026-05-04" instead.
- **G5 (Convergence rule on Discipline rule rosters) — RESOLVED per Tony's Option (b).** Phase 1 drafters enumerate candidate rules from substrate; QB ratifies before § 5 locks. New § 5.7 codifies the workflow. Provenance discriminator (mirrors methodology-interpolation grandfathering pattern) prevents pattern-completion creep.
- **G7 (Tertiary state) — RESOLVED with CONDITIONAL state authorized.** Three states for conditional trigger evaluation: FIRES, DOES NOT FIRE, CONDITIONAL. CONDITIONAL requires mandatory adjacent-prose caveat documentation. New § 5.6.1.2 codifies the notation. § 5.6.1.1 worked example updated to use CONDITIONAL where the cross-cutting case applies.
- **G9 (W.N numbering convention) — RESOLVED with bible-local W.N + global Bug #N for cross-bible references.** New § 5.5.1 codifies the global Bug #N convention; § 3.3 cross-reference syntax extended with `<bible>:#<bug-id>` format. Existing de facto convention (Bug #28, Bug #15, Bug #24) made explicit.

**Items resolved per audit-CC-recommended resolutions (G1 / G2 / G4 / G6 — direct, substrate-grounded, embedded as drafting-spec exact-text replacements):**

- **G1 (Currently Open scope for cross-cutting bugs) — IMPLEMENTED.** § 5.3 extended with cross-cutting bug Currently Open scope rule. Non-canonical-home bibles list cross-cutting open bugs in their § 6 as one-line cross-references; canonical-home bible carries the substantive description. Once fixed, § 6 cross-references are removed (W.N entry replaces them).
- **G2 (Superseded SQL constraint qualification) — IMPLEMENTED.** § 5.6.4 Deprecated entry template gets new conditional bullet: superseded form qualifies for Deprecated entry IF physically persisting in DB schema (verifiable). If physically dropped, migration history is sufficient immune memory. Drafter discretion with verification log entry.
- **G4 (TOC framing tightening) — IMPLEMENTED.** All seven per-document templates' "Recommended TOC:" headers replaced with explicit "TOC (sections 5–8 mandatory per § 5.2; sections 1–4 recommended-strongly with drafter latitude per locality of reference):" framing. Aligns § 6.X templates with § 5.2's canonical 5/6/7/8 mandate while preserving drafter latitude for domain-specific § 1–4.
- **G6 (Cross-reference syntax adoption) — IMPLEMENTED.** § 7.1 extended with `<bible>:#<bug-id>` format; new § 7.1.1 adds worked examples for each cross-reference type (within-bible numeric, within-bible W.N, cross-bible by section ID, cross-bible by W.N, cross-bible by global Bug #N, cross-reference to PHASE_5_BACKLOG.md by phase number).

**METHODOLOGY-INTERPOLATION self-check (v4):**

Per the methodology-interpolation rule (META_PLAN v8 § 6.1, with v6 expanded scope, grandfathering clause, and pattern-completion check), CC reviewed every new methodology construct introduced in v4 against authorization sources:

- Tony-locked decisions (G3, G5, G7, G9): all 4 architectural-question resolutions trace directly to Tony's locked language in this cycle's drafting spec. Reproduced char-exact per spec-prescribed text. **Not interpolation.**
- Audit-CC-recommended resolutions (G1, G2, G4, G6): all 4 implementations trace directly to drafting-spec embedded exact replacement text. The audit-CC recommendations were locked into the drafting spec as authorized; CC reproduced char-exact. **Not interpolation.**
- "CONDITIONAL" tertiary-state name (G7): the name choice was Tony-locked in this cycle's drafting spec ("more semantically precise than 'PARTIAL' or 'FIRES (advisory)'"). Reproduced char-exact. **Not interpolation.**
- "Global Bug #N convention" (G9): the convention itself was de facto in operator usage (Bug #28, Bug #15, Bug #24 cited in META_PLAN v8 + operator memory files). § 5.5.1 makes the existing convention explicit, not introducing a new one. **Not interpolation.** Surfaced for awareness: the codification step itself creates the formal rule even when the substrate convention pre-exists.

**METHODOLOGY-INTERPOLATION rule pattern-completion check (v4):**

The v4 cycle introduces ZERO new letter-prefixes (W.N remains the only ratified letter-prefix). The `#<bug-id>` cross-reference format is a syntax extension, not a letter-prefix. The pattern-completion check (AUDIT_METHODOLOGY v2 § 5.5) for letter-prefixes confirms compliance.

Cross-reference syntax extensions (`<bible>:#<bug-id>`) are subject to AUDIT_METHODOLOGY v2 § 5.5 pattern-completion check; v4's extension is explicitly ratified per Tony's G9 locked decision; v4 documents this in § 7.1.1.

**AUDIT_METHODOLOGY v3 cycle assessment (per drafting spec discipline 7):**

Per QB's pre-drafting assessment (verified against AUDIT_METHODOLOGY v2 substrate read): **AUDIT_METHODOLOGY v3 cycle is NOT warranted.** v2's prophylactic checks (§ 4.1–§ 4.7 audit-CC adversarial scope; § 5.1–§ 5.7 prophylactic checks including methodology-interpolation, verification-log precision, and pattern-completion) remain operationally valid against v4. Version-references in AUDIT_METHODOLOGY (`BIBLE_STRUCTURE_SPEC v3`) update interpretively at each new lock cycle; these are document-version pointers, not load-bearing methodology constructs. The content of v2's checks (the rules themselves) does not depend on v3 vs v4 specifics. Surfaced for v4 audit-CC review. If audit-CC catches a coherence drift, AUDIT_METHODOLOGY v3 becomes part of the post-v4 sequence.

**Net new methodology constructs introduced in v4: 8** (4 Tony-locked decisions + 4 audit-CC-recommended resolutions, all embedded with drafting-spec authorization; zero unauthorized constructs surfaced).

**Items NOT addressed in v4 (preserved from v3 unchanged):**

- All § 1, § 2, § 4, § 6.X (beyond TOC header replacement), § 8, § 9, § 10, § 11 content retained verbatim from v3.
- v3 surfacing notes (§ 12.1, § 12.2, § 12.3) preserved verbatim.
- v2→v3 changelog (§ 13) preserved verbatim; v3→v4 entry appended.

### 12.5 v5 surfacing notes (delta from v4)

**Items resolved by v4 audit's lock-after-one-MINOR-revision recommendation:**

- **§ 11 Lock Status metadata pointer hygiene — IMPLEMENTED.** Front matter Status correctly updated to v4 in v4 cycle; § 11 Lock Status sub-fields (Document status, Audit-CC pass, Verification log, Tony review, Locked) still referenced v3 metadata. v5 surgical-cosmetic patch updates § 11 to v5 metadata reflecting the v4-clean-audit + v5-metadata-fix lock trajectory.

**METHODOLOGY-INTERPOLATION self-check (v5):**

Net new methodology constructs introduced in v5: 0. v5 modifies ONLY metadata pointers (§ 11 + front matter Status/Locked + revision history). Zero methodology touch. The pattern-completion check applies trivially: no new constructs, no new conventions, no new cross-reference vocabularies. Pure pointer hygiene.

**METHODOLOGY-INTERPOLATION rule pattern-completion check (v5):**

W.N remains the only ratified letter-prefix. `#<bug-id>` cross-reference syntax extension preserved per v4's G9 ratification. No new syntax extensions introduced.

**Items NOT addressed in v5 (preserved from v4 unchanged):**

- All § 1, § 2, § 3, § 4, § 5, § 6, § 7, § 8, § 9, § 10 content retained verbatim from v4.
- v3 surfacing notes (§ 12.1, § 12.2, § 12.3) preserved verbatim.
- v4 surfacing notes (§ 12.4) preserved verbatim.
- v2→v3 changelog and v3→v4 changelog (§ 13) preserved verbatim; v4→v5 entry appended.
- V4-11 mixed v6/v8 META_PLAN references — adjudicated by v4 audit as (a) acceptable surgical-patch discipline application; preserved as-is in v5. Future-cycle cleanup remains cheap if QB later prefers global sweep.

**Net new methodology constructs introduced in v5: 0.**

### 12.6 v6 surfacing notes (delta from v5)

**Items resolved by Tony's v6 cycle decisions (architectural questions G-new-1 / G-new-2):**

- **G-new-1 (Candidate-roster numbering convention) — RESOLVED per Tony's Option (a).** Candidate-roster entries pre-ratification use numeric sub-section IDs (`5.1`, `5.2`, ...) consistent with ratified-entry convention. Candidate status conveyed by § 5 header marker, not by provisional letter-prefix. W.N remains only ratified letter-prefix per § 5.5.1. New § 5.7 closing-clause paragraph codifies the rule. Closes the convergence test re-run's run3 (`5.A`–`5.I` letter-prefix) vs run4 (`5.1`–`5.8` numeric) divergence by ratifying numeric.
- **G-new-2 (Matview as "table" for § 4.1 enumeration scope) — RESOLVED per Tony's Option (a).** § 6.6 § 4.1 enumerates CREATE TABLE declarations only; matviews documented at § 3 only per § 2 Definitions table-vs-matview distinction. § 6.6 § 4.1 first-sentence qualification clause added. Closes the convergence test re-run's run3 (matview at § 3 only) vs run4 (matview as 4.1.15 with deferral) divergence by ratifying run3's reading.

**METHODOLOGY-INTERPOLATION self-check (v6):**

Per the methodology-interpolation rule (META_PLAN v8 § 6.1, with v6 expanded scope, grandfathering clause, and pattern-completion check), CC reviewed every new methodology construct introduced in v6 against authorization sources:

- **Tony-locked decisions (G-new-1, G-new-2):** both architectural-question resolutions trace directly to Tony's locked language in this cycle's drafting spec. Reproduced char-exact per spec-prescribed text. Not interpolation.
- **"Numeric sub-section IDs for candidates" rule (G-new-1):** the rule was Tony-locked in this cycle's drafting spec. Reproduced char-exact. Not interpolation. The rule prevents pattern-completion drift (provisional letter-prefixes were the run3 surface for letter-prefix proliferation past W.N) by routing candidates to the existing ratified-entry convention.
- **"CREATE TABLE declaration" enumeration scope (G-new-2):** the scope was Tony-locked in this cycle's drafting spec. Reproduced char-exact. Not interpolation. The scope rule honors § 2 Definitions' explicit table-vs-matview distinction.

**METHODOLOGY-INTERPOLATION rule pattern-completion check (v6):**

The v6 cycle introduces ZERO new letter-prefixes (W.N remains the only ratified letter-prefix). The G-new-1 closure explicitly forbids provisional letter-prefixes for candidate entries, reinforcing W.N exclusivity. Pattern-completion check (AUDIT_METHODOLOGY v2 § 5.5) for letter-prefixes confirms compliance.

Cross-reference syntax extensions: NONE introduced in v6. `<bible>:#<bug-id>` syntax extension preserved per v4's G9 ratification. No new cross-reference vocabularies.

**AUDIT_METHODOLOGY v3 cycle assessment (per drafting spec discipline):**

Per QB's pre-drafting assessment: AUDIT_METHODOLOGY v3 cycle is NOT warranted at v6 lock. v2's prophylactic checks (§ 4.1–§ 4.7 audit-CC adversarial scope; § 5.1–§ 5.7 prophylactic checks) remain operationally valid against v6. The G8 compliance variance from the convergence test re-run is drafter-discipline drift on an unambiguous locked rule (META_PLAN v8 § 7.3 placeholder-resolution sub-rule); banked for Phase 1 audit-CC checklist as "verify every W.N entry's Fix date is YYYY-MM-DD form, not placeholder, when fix date is git log-resolvable." If pattern recurs across Phase 1 bibles, AUDIT_METHODOLOGY v3 cycle absorbs it.

**Net new methodology constructs introduced in v6: 0.**

(Both closures are spec-text clarifications of existing conventions: G-new-1 codifies "numeric for candidates" which is the natural application of § 5.5's existing numeric-sub-section-ID rule to pre-ratification entries; G-new-2 codifies "CREATE TABLE declaration only" which is the natural application of § 2 Definitions' existing table-vs-matview distinction to § 4.1 enumeration scope.)

**Items NOT addressed in v6 (preserved from v5 unchanged):**

- All § 1, § 2, § 3, § 4, § 5.1-5.6 content retained verbatim from v5.
- § 5.7 content retained verbatim other than the new closing-clause paragraph (G-new-1 closure).
- § 6.1-6.5 content retained verbatim from v5.
- § 6.6 content retained verbatim other than the § 4.1 first-sentence qualification (G-new-2 closure).
- § 6.7 content retained verbatim from v5.
- § 7, § 8, § 9, § 10 content retained verbatim from v5.
- v3/v4/v5 surfacing notes (§ 12.1-12.5) preserved verbatim.
- v1→v2, v2→v3, v3→v4, v4→v5 changelog entries preserved verbatim; v5→v6 entry prepended.
- V4-11 mixed v6/v8 META_PLAN references — adjudicated by v4 audit as (a) acceptable surgical-patch discipline application; preserved as-is in v6. Future-cycle cleanup remains cheap if QB later prefers global sweep.
- G8 compliance variance from convergence test re-run — banked for Phase 1 audit-CC checklist; not closed in v6 spec.

**Net new methodology constructs introduced in v6: 0.**

---

## 13. Changelog

### v5 → v6

**Methodology fixes (convergence test re-run findings — 2 NEW methodology gaps):**

The convergence test re-run on v5/v8 substrate (`_audits/convergence_test_v5_audit.md`) produced verdict CONVERGED-WITH-RESIDUAL: 18 material differences (down from original test's 21), 8 PASS + 1 PARTIAL + 0 FAIL on the 9 original G1-G9 gap closures, and 2 NEW methodology gaps not closed by G1-G9. Tony locked Option (a) on both NEW gaps; v6 embeds the resolutions per the v3→v4 audit-CC-recommended-resolution model.

- **G-new-1 — Candidate-roster numbering convention codified (§ 5.7 closing clause).** Candidate-roster entries pre-ratification use numeric sub-section IDs (`5.1`, `5.2`, ...) per the existing § 5.5 numeric-sub-section-ID rule. The "candidate" status is conveyed by the § 5 header marker, NOT by a provisional letter-prefix. W.N remains only ratified letter-prefix per § 5.5.1. Closes the convergence test re-run's run3 vs run4 divergence on letter-prefix vs numeric for candidates. Per Tony's locked Option (a).
- **G-new-2 — Matview enumeration scope codified (§ 6.6 § 4.1 first-sentence qualification).** § 6.6 § 4.1 enumerates CREATE TABLE declarations only; matviews documented at § 3 only per § 2 Definitions table-vs-matview distinction. Closes the convergence test re-run's run3 (matview at § 3 only) vs run4 (matview as 4.1.15 with deferral) divergence by ratifying run3's reading. Per Tony's locked Option (a).

**G8 compliance variance — banked for Phase 1 audit-CC checklist (no spec revision):**

The convergence test re-run surfaced run3's failure to apply META_PLAN v8 § 7.3 placeholder-resolution sub-rule (run3 used "fixed 2026-05-XX" placeholder for migration 011 — a real fix whose date is git log-resolvable). Run4 ran `stat -c "%y %n"` and committed to "fixed 2026-05-01" per the locked rule. This is drafter-compliance variance on an unambiguous locked rule, NOT methodology ambiguity. No spec revision needed. Phase 1 audit-CC checklist gains: "verify every W.N entry's Fix date is YYYY-MM-DD form, not placeholder, when fix date is git log-resolvable; placeholders only for forward-looking discipline codifications." If pattern recurs across Phase 1 bibles, AUDIT_METHODOLOGY v3 cycle absorbs.

**Methodology lessons recorded (v5 → v6):**

The convergence test re-run on v5/v8 substrate validated the v3→v4 surgical-patch closure cycle's effectiveness: 8 of 9 original gaps closed at structural-equivalence level (the 1 PARTIAL is drafter-compliance, not methodology ambiguity). 17 of 21 original material differences resolved. The convergence test methodology itself is now empirically validated as a Phase 0 closure mechanism: it reliably catches both methodology gaps (closeable by spec revision) and drafter-discipline drift (closeable by audit-CC checklist), distinguishing the two. The v3→v4→v5→v6 trajectory establishes the integration model:

- Architectural-decision gaps → Tony locks Option (a)/(b); CC embeds char-exact.
- Audit-CC-recommended-resolution gaps → drafting spec embeds the recommendation char-exact; Tony's role is ratification by inclusion.
- Drafter-compliance variance on unambiguous rules → bank for next-phase audit-CC checklist; no spec revision.

The pattern is generalizable to Phase 1 bible audit cycles: when audit-CC findings differentiate between architectural-decision-class and clarification-class issues, route the former to Tony and embed the latter directly per audit-CC's recommendation.

**Path A sequencing complete:**

v6 is the third Phase 0 revision triggered by the convergence test (META_PLAN v7→v8 closed G8; BIBLE_STRUCTURE_SPEC v3→v4 closed G1-G7+G9; v4→v5 closed metadata-pointer oversight; v5→v6 closes G-new-1 + G-new-2). Per audit-CC's pre-approval, v6 skips re-audit since scope is pure surgical-cosmetic embed of audit-CC-recommended resolutions. After v6 lock, Phase 0 closes. Phase 1 begins per BIBLE_STRUCTURE_SPEC v6 § 8.2 (Architecture Overview first; Database & Schema Bible second — run3 and run4 from convergence test re-run are NOT Phase 1 lock-targets directly, but serve as substrate-grounded reference content QB and Tony decide how to use at Database & Schema Bible Phase 1 cycle).

**Retained from v5 unchanged:**

All § 1 through § 5.6 content, § 5.7 (other than the new closing-clause paragraph for G-new-1), § 6.1–§ 6.5, § 6.6 (other than the § 4.1 first-sentence qualification for G-new-2), § 6.7, § 7 through § 10, § 11 (other than the metadata block update for v6 lock), § 12.1 through § 12.5 (with new § 12.6 surfacing notes added), § 13 v4→v5 + v3→v4 + v2→v3 + v1→v2 entries (with new v5→v6 entry prepended). Front matter (other than Status update + v6 revision history entry; Locked field unchanged at 2026-05-05). Verification log inherits v5's V5-1 + v4's V4-1 through V4-11 + v3-inherited (via v4) wholesale; v6 adds 1 new entry (V6-1: 2 surgical embeds for G-new-1 + G-new-2 closures).

### v4 → v5

**MINOR fix (v4 audit finding):**

The v4 audit returned 0 BLOCKER + 0 MATERIAL + 0 fabricated + 0 methodology-interpolation + 2 MINOR + 4 STYLE — cleanest substantive cycle of v3-v5 sequence. The single blocking-for-clean-lock finding was a missed metadata pointer update at § 11 Lock Status block (lines 1142–1146 in v4). Front matter Status was correctly updated to "DRAFT v4 (pre-audit)" in v4 drafting; § 11 sub-fields (Document status, Audit-CC pass, Verification log, Tony review, Locked) still referenced v3 metadata.

**v5 surgical-cosmetic patch:**

- § 11 Lock Status block updated to v5 metadata reflecting v4-clean-audit + v5-metadata-fix lock trajectory.
- Front matter Status updated from "DRAFT v4 (pre-audit)" to "LOCKED v5 (2026-05-05)".
- Front matter Locked field updated from "[pending audit + Tony review + iteration cycles]" to "2026-05-05".
- Revision history v5 entry appended naming the surgical-cosmetic scope + 1-cycle close per v4 audit-CC's recommendation.
- § 12.5 v5 surfacing notes added (zero net new methodology constructs).

**Methodology lessons recorded (v4 → v5):**

The v4 cycle's surgical-patch discipline was applied with high fidelity to all 9 fix categories (A-I; 12/12 verbatim reproductions char-exact; 0 unauthorized changes). The single metadata-pointer miss (§ 11) reflects a pattern: when surgical-patch focus is on content fix categories, peripheral metadata blocks are vulnerable to oversight. Banked for AUDIT_METHODOLOGY.md as a future prophylactic check candidate: "When any front matter or status block in the audited document references version metadata, verify ALL such blocks are updated coherently." Not warranted as AUDIT_METHODOLOGY v3 cycle trigger at this lock; the lesson is empirical and Phase 1 audits will surface real friction if the pattern recurs.

**Path A sequencing complete:**

v5 is the second of two Phase 0 revisions triggered by the convergence test, with v4 closing 8 methodology gaps (G1-G7+G9) and v5 closing the v4-cycle metadata-pointer oversight. After v5 lock (this cycle), the convergence test re-runs on the same Database & Schema Bible spec to validate that all gaps are closed. If gaps re-surface, escalate per META_PLAN v8 § 5.3 "Iteration escalation" rule. If clean, Phase 0 closes; Phase 1 begins per BIBLE_STRUCTURE_SPEC v5 § 8.2 (Architecture Overview first).

**Retained from v4 unchanged:**

All § 1 through § 10 content, § 11 (other than the metadata pointer hygiene update at lines 1142–1146), § 12.1 through § 12.4 (with new § 12.5 surfacing notes added), § 13 v3→v4 + v2→v3 + v1→v2 entries (with new v4→v5 entry prepended). Front matter (other than Status + Locked field updates + v5 revision history entry). Verification log inherits v4's 11 new entries + v3's 27 inherited entries wholesale; v5 adds 1 new entry (V5-1: § 11 metadata fix verification).

### v3 → v4

**MATERIAL fixes (convergence test audit findings — 8 of 9 methodology gaps; G8 closed in META_PLAN v7→v8):**

The operating-model convergence test on the Database & Schema Bible draft (`_audits/convergence_test_audit.md`) returned 21 material differences + 9 methodology gaps. G8 (placeholder convention scope) was closed in the META_PLAN v7→v8 cycle (LOCKED). The remaining 8 gaps were routed to BIBLE_STRUCTURE_SPEC v4 per Path A sequencing:

- **G1 — Cross-cutting bug Currently Open scope clarified.** § 5.3 extended with explicit rule: cross-cutting open bugs appear in § 6 of canonical-home bible (substantive description) AND in § 6 of every bible whose discipline its symptoms touch (one-line cross-reference in `<bible>:#<bug-id>` format). When fixed, non-canonical-home § 6 references are removed; the W.N entry replaces them. Closes run1-vs-run2 divergence on Bug #28 cross-reference inclusion.
- **G2 — Superseded SQL constraint Deprecated qualification clarified.** § 5.6.4 Deprecated entry template gets new conditional bullet: superseded SQL constraints qualify for Deprecated entry IF physically persisting in the DB schema; otherwise migration history is sufficient immune memory. Drafter discretion with verification log entry. Closes run1-vs-run2 divergence on pre-011 wr_predictions UNIQUE inclusion.
- **G3 — § 8 W.N entry confined to true bug-fix entries.** § 5.6.1 template scope clause added: § 8 entries require mandatory Fix date; discipline codifications routed to § 5 (Discipline rules). Closes run2's 8.W.3 (past_performances.race_id NULL acceptance) violation of W.N template's Fix date mandate. Per Tony's locked Option (b) on the G3 architectural question.
- **G4 — § 6.X "Recommended TOC" tightened to "sections 5–8 mandatory; sections 1–4 recommended-strongly with drafter latitude."** All seven per-document templates' "Recommended TOC:" headers replaced uniformly. Aligns § 6.X with § 5.2's canonical 5/6/7/8 mandate while preserving drafter latitude for domain-specific § 1–4 reorganization. Closes run1-vs-run2 divergence on § 4 framing.
- **G5 — Convergence rule on Discipline rule rosters added (§ 5.7).** Phase 1 drafters enumerate candidate § 5 rules from substrate; QB ratifies before § 5 locks. Workflow specified (one round trip per bible). Provenance discriminator (mirrors methodology-interpolation grandfathering pattern) prevents pattern-completion creep. Per Tony's locked Option (b). Closes run1-vs-run2 divergence on rule rosters (4 rules vs 7 rules; only 1 overlapped).
- **G6 — § 7.1 cross-reference syntax + new § 7.1.1 worked examples.** § 7.1 extended with `<bible>:#<bug-id>` format; new § 7.1.1 codifies worked examples for each cross-reference type. Phase 1 drafters see canonical syntax at drafter touchpoint. Closes run1-vs-run2 divergence on cross-reference format adoption (snake_case .md vs Title Case prose; neither matched § 7.1's spec).
- **G7 — Tertiary state CONDITIONAL authorized for conditional trigger evaluation.** § 5.6.1.1 worked example updated to use CONDITIONAL where the cross-cutting case applies; new § 5.6.1.2 codifies the three states (FIRES, DOES NOT FIRE, CONDITIONAL) with mandatory adjacent-prose caveat for CONDITIONAL. Per Tony's locked decision. Closes run1's "PARTIAL" / run2's "FIRES (advisory)" divergence by ratifying a single tertiary state with tight semantics.
- **G9 — Bible-local W.N + global Bug #N for cross-bible references.** § 3.3 cross-reference syntax extended with `<bible>:#<bug-id>` format for cross-cutting bugs; § 5.5 W.N scope clarified as bible-local; new § 5.5.1 codifies global Bug #N convention (monotonic assignment, never reused, de facto convention now explicit). Per Tony's locked decision. Closes run1's W.N renumbering instability by routing cross-bible references to the durable global Bug #N.

**Methodology lessons recorded (v3 → v4):**

The convergence test (META_PLAN v8 § 5.3) caught 9 methodology gaps that single-drafter audit cycles could not have caught. Each gap surfaced because two CC sessions interpreted the same v3 spec differently. The lesson: structural-equivalence drift between drafters is detectable only by adversarial cross-CC comparison; per-document audit cycles validate within-drafter coherence but not cross-drafter convergence.

The v4 cycle's 8-gap closure scope is heavier than typical surgical-patch cycles (META_PLAN v7→v8 closed 4; META_PLAN v6→v7 closed 1). The drafting spec's resolution of routing 4 architectural questions to Tony for locked decisions and 4 audit-CC recommendations to drafting-spec embedded exact-text replacements is the integration model: when convergence-test gaps land at architectural-decision level, Tony locks; when at recommendation-level (substrate-grounded, narrow), audit-CC's recommendation embeds as drafting-spec exact text.

**Banked for AUDIT_METHODOLOGY.md (potential v3 cycle if drift surfaces):** the convergence test pattern (operating-model convergence test on a Phase 1 spec; audit-CC enumerates material differences and methodology gaps; gap closures route through subsequent Phase 0 revision cycles) is now empirically validated. AUDIT_METHODOLOGY v3 cycle is NOT warranted at this lock per QB assessment (v2's prophylactic checks remain operationally valid; version-references update interpretively). If audit-CC catches a coherence drift, AUDIT_METHODOLOGY v3 becomes part of the post-v4 sequence.

**Path A sequencing note:**

v4 is the second of two Phase 0 revisions triggered by the convergence test (after META_PLAN v7→v8 closed G8; v4 closes G1, G2, G3, G4, G5, G6, G7, G9). After v4 lock, the convergence test re-runs on the same Database & Schema Bible spec to validate that all gaps are closed. If gaps re-surface, escalate per META_PLAN v8 § 5.3 "Iteration escalation" rule.

**Retained from v3 unchanged:**

Front matter (revised for v4 metadata + revision history v4 entry), § 1, § 2, § 3.1, § 3.2 (§ 3.3 modified per v4 requirement A), § 4, § 5.1, § 5.2, § 5.3 (other than the modified second paragraph + new cross-cutting Currently Open scope rule), § 5.4, § 5.5 (other than the modified first bullet + new § 5.5.1), § 5.6.1 template (other than the new Scope clause + Mandatory fields update), § 5.6.1.1 worked example (other than the modified Conditional triggers block + new § 5.6.1.2), § 5.6.2, § 5.6.3, § 5.6.4 (other than the new conditional bullet for SQL constraints), § 6.1–§ 6.7 content (other than the uniform "Recommended TOC:" header replacement), § 7.1 (other than the modified syntax + new § 7.1.1), § 7.2–§ 7.6, § 8, § 9, § 10, § 11, § 12.1–§ 12.3 (with new § 12.4 surfacing notes added). § 13 v2→v3 entry preserved verbatim. Verification log inherits v3's claims with re-verified-2026-05-05 timestamps and adds new v4 claims per v4 fix categories.

### v2 → v3

**MATERIAL fixes (v2 audit findings):**

- **Finding 1 — § 6.1–§ 6.7 per-document templates renumbered to align Discipline rules at section 5 per Tony's Option I.** All seven per-document templates now follow the canonical 5/6/7/8 ordering: 5 Discipline rules / 6 Currently Open / 7 Deprecated / 8 What Was Fixed. Domain-specific sections consolidated under § 4.X sub-positions:
  - § 6.1 architecture_overview: § 4 Canonical objects + INDEX (4.1, 4.2, 4.3) — minor renumber
  - § 6.2 data_pipeline: § 4 Pipeline detail (4.1 Per-flow, 4.2 Data Acquisition Honesty Protocol)
  - § 6.3 feature_provenance: § 4 Feature × model documentation (4.1 Per-feature, 4.2 Per-model)
  - § 6.4 ml_layer_architecture: § 4 Model and pipeline detail (4.1 Per-model, 4.2 Inference pipeline composition, 4.3 Calibration / bypass state)
  - § 6.5 model_evaluation_retraining: § 4 Operational discipline (4.1 Retraining triggers, 4.2 Calibration discipline, 4.3 Model artifact version control, 4.4 Deployment gating)
  - § 6.6 database_schema: § 4 Schema and migration detail (4.1 Per-table, 4.2 Migration discipline)
  - § 6.7 api_frontend: § 4 Route, frontend, and consumption detail (4.1 Per-route, 4.2 Frontend consumption, 4.3 Frontend pages and components)
  
  Empty Currently Open or Deprecated sections in some bibles are explicit (e.g., "No current open issues at lock") rather than absent. Cross-references updated post-renumbering; verification log Claim N10 confirms integrity.

- **Finding 2 — § 5.6.1.1 worked example added.** Shows META_PLAN v6 Appendix A.3's W.3 entry (Gonzo Sauce FE Single-Source Extraction) with each conditional trigger explicitly evaluated using FIRES / DOES NOT FIRE notation: if-fix-involved-migration (DOES NOT FIRE), if-fix-invalidated-prior-content (DOES NOT FIRE), if-fix-produced-Forbidden-Pattern (FIRES with cross-reference), if-fix-touches-multiple-bibles (FIRES with canonical-home note). Phase 1 drafters use this as the integration model. ~25 lines net.

- **Finding 3 — § 5.6.3 source-spec depth note added.** One-paragraph acknowledgment that META_PLAN v6 § 7.6 inherits DD § 19's brevity without expansion; the template's depth reflects that source-spec depth. Honest path chosen over depth-parity to avoid pattern-completion interpolation. DD § 19 brevity confirmed via verification log Claim N9.

**MINORs deferred to Phase 1 opportunistic:**

The 7 carry-over MINORs from v2 audit (§ 6.7 "9 pages + 13 components" verification log entry, § 6.5 "4 calibration scripts" dump-only, § 7.2 insertion rule, § 5.2 boundary language, § 5.6.2/§ 5.6.4 worked examples, § 8.4 convergence test pass/fail example, § 6.X anchor verification subsection length variation) remain deferred. Phase 1 drafters address as friction surfaces.

**Methodology lessons recorded (v2 → v3):**

The v2 audit caught the same contradiction class as v1 (TOC numbering inconsistency: 8-vs-18 in v1, 5-vs-7 in v2). The pattern is structural: extracting shared templates (§ 5.6) creates reference dependencies on canonical section numbers that per-document templates may deviate from. v3's renumbering establishes the canonical 5/6/7/8 ordering as non-negotiable across all bibles; future drafters of new bibles must conform.

**Banked for AUDIT_METHODOLOGY.md:** when shared templates reference per-document sections by number, audit-CC's prophylactic check should include: "verify all per-document templates use the same canonical section numbering for the referenced positions; deviations break shared-template cross-references." This is a special case of the broader contradiction-detection question (META_PLAN v6 § 6.2 Q4) but worth naming explicitly given the recurrence across both v1 and v2 audits.

**Retained from v2 unchanged:**

Front matter (revised for v3 metadata), § 1, § 2, § 3, § 4 (front matter through § 4.4), § 5.1, § 5.2 (with the canonical 5–8 mandate strengthening), § 5.3, § 5.4, § 5.5, § 5.6.2, § 5.6.4, § 7, § 8 (with cross-reference target updates), § 9.1 (with Claim N9 + N10 added in § 9.2), § 10, § 11. Verification log inherits 25 claims with re-verification timestamps; v3 adds 2 new claims.

### v1 → v2 (preserved from v2 changelog for reference)

**MATERIAL fixes (v1 audit findings):**

- M-1 — F.N / C.N / D.N naming convention extension dropped per Tony's Option B
- M-2 — What Was Fixed positioned at section 8 across all instances
- M-3 — § 4.2 restructured as four numbered subsections with three explicit subheadings each
- M-4 — § 6.1–§ 6.7 per-section guidance restructured as Mandatory / Conditional two-block format; § 5.6 extracts canonical templates
- M-5 — § 5.3 + § 7.4 canonical-home tiebreaker explicit deferral

**Methodology-interpolation finding resolved:**

v1 § 5.5's F.N / C.N / D.N extension was caught by audit-CC as pattern-completion interpolation past META_PLAN v6's ratified W.N pattern. v2 dropped the extension; Tony's Option B aligned EE bible numbering with DD bible's existing convention. Pattern-completion interpolation lesson banked for AUDIT_METHODOLOGY.md.

**MINORs addressed in v2 (tightly coupled to MATERIALs):** MINOR #1 through #5.
