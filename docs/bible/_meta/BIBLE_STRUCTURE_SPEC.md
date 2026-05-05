# BIBLE_STRUCTURE_SPEC.md

**Document:** BIBLE_STRUCTURE_SPEC
**Phase:** 0 (Methodology) — Phase 0 deliverable 2 of 5
**Status:** DRAFT v3 (pre-audit)
**Author:** CC (drafting under verification discipline; QB orchestrated and reviewed)
**Date:** 2026-05-04
**Locked:** [pending audit + Tony review + iteration cycles]

**Revision history:**
- v1 (2026-05-04): initial CC draft. Companion verification log at `_audits/BIBLE_STRUCTURE_SPEC_v1_verification.md`.
- v2 (2026-05-04): post-v1-audit surgical patch pass integrating Tony's five locked decisions (M-1 through M-5).
- v3 (2026-05-04): post-v2-audit surgical patch pass integrating Tony's three locked decisions (Findings 1, 2, 3). v2's structure preserved; sections without v2-audit findings against them retained unchanged. Companion verification log at `_audits/BIBLE_STRUCTURE_SPEC_v3_verification.md` inherits v2's 25 claims with re-verified-2026-05-04 timestamps and adds 2 new claims (N9 DD § 19 brevity confirmation; N10 cross-reference integrity post-renumbering).

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

Within each bible document, sections are numbered in dotted decimal form. Cross-bible references: `<bible_doc_name>:<section_id>`. Examples:
- `feature_provenance_bible:4.1` — section 4.1
- `data_pipeline_bible:8.W.7` — What Was Fixed entry W.7 in Data Pipeline Bible (§ 8 = canonical What Was Fixed position)
- `database_schema_bible:5.4` — sub-section numeric ID for a Forbidden Pattern (no letter prefix; see § 5.5)

Matches META_PLAN v6 § 7.11's commit message convention.

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

The canonical-home determination is made at the time the entry is created. The decision is recorded in the entry (the canonical home's W.N entry says "canonical; cross-referenced from <other bibles>"; the cross-referencing bibles' "Currently Open" or "Deprecated" sections cite the canonical W.N by `<bible>:8.W.<n>`).

**Tiebreaker deferral:** when "most directly prevents recurrence" is ambiguous (two QB sessions could plausibly assign the canonical home to different bibles), tiebreaker criteria are deferred to AUDIT_METHODOLOGY.md (Phase 0 deliverable 3). Until that document locks, QB surfaces ambiguous cases to Tony for explicit ratification per META_PLAN v6 § 8.3 decision-deferral discipline.

### 5.4 Dated lock points (per META_PLAN v6 § 7.3)

Every rule, pattern, decision in any bible carries a `Locked YYYY-MM-DD` parenthetical. Section headers, FORBIDDEN/CORRECT pairs, and W.N entries all carry lock dates. The format is identical to META_PLAN v6 § 7.3 + Appendix A.2.

### 5.5 Naming conventions inside each bible

- **What Was Fixed entries** are numbered as `<section>.W.<n>` (e.g., `8.W.1`, `8.W.2` within section 8 of a given bible). The format follows META_PLAN v6 § 7.4 + Appendix A.3. The W.N letter-prefix convention is the **only** letter-prefix in EE bible numbering: What Was Fixed entries require cross-bible-trackable identifiers because cross-cutting bugs (per § 5.3 canonical-home rule) reference each other across bibles, and a grep over `git log` for `W.7` retrieves every commit related to that immune-memory entry across all bibles per META_PLAN v6 § 7.11 commit-message convention.

- **Forbidden Patterns**, **Common Mistakes**, and **Deprecated entries** use **sub-section numeric IDs** (e.g., a Forbidden Pattern at section 5 of the ML Layer Architecture Bible is `ml_layer_architecture_bible:5.4`, not `ml_layer_architecture_bible:5.F.4`). The format follows META_PLAN v6 § 7.5 + Appendix A.1 (Forbidden Patterns), § 7.6 (Common Mistakes), § 7.7 + Appendix A.4 (Deprecated). This matches the DD bible's existing convention: DD § 6.4 for a Forbidden Pattern, DD § 21.1 for a Deprecated entry.

- **Cross-bible references** use the full path: `<bible_name>:<section_id>` (e.g., `feature_provenance_bible:8.W.7` for a What Was Fixed entry; `ml_layer_architecture_bible:5.4` for a Forbidden Pattern). Within a single bible, references can use just the local ID: `see § 5.4`, `see § 8.W.3`.

**Why W.N is special and F./C./D. are not:** What Was Fixed entries are the bible's institutional immune memory. Cross-cutting bugs require trackable identifiers across bibles. A grep for `W.7` finds every commit, every cross-reference, every related entry in O(n) wall-clock time. Forbidden Patterns, Common Mistakes, and Deprecated entries do not carry the same forcing function — they don't cross bibles in the same way. Sub-section numeric IDs suffice and match DD convention.

### 5.6 Canonical templates for shared content

The four discipline-rule entry types (What Was Fixed, Forbidden Patterns, Common Mistakes, Deprecated) appear in every Phase 1 bible. Their canonical templates are extracted here so per-document templates in § 6 cross-reference rather than duplicate.

#### 5.6.1 What Was Fixed entry template (per META_PLAN v6 § 7.4 + Appendix A.3)

```
8.W.<n>: <Bug name or short description> (fixed YYYY-MM-DD)
```

**Mandatory fields:**
- Entry ID (`8.W.<n>` format)
- Bug name or short description
- Fix date (YYYY-MM-DD)
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

Conditional triggers evaluated:
  - if-fix-involved-migration: DOES NOT FIRE. Gonzo extraction was a code refactor,
    not a schema change. No migration linkage.
  - if-fix-invalidated-prior-content: DOES NOT FIRE. No prior bible content existed
    at extraction time (pre-Phase-0).
  - if-fix-produced-Forbidden-Pattern: FIRES. Cross-reference to candidate Forbidden
    Pattern at feature_provenance_bible:5.X (placeholder; Phase 1 drafter assigns
    actual numeric ID at draft time): "Adding feature engineering logic to either
    training or inference path without parallel update to the other."
  - if-fix-touches-multiple-bibles: FIRES. The bug spans Feature Provenance Bible
    (canonical home, per § 5.3) and is cross-referenced from
    ml_layer_architecture_bible:8 and model_evaluation_retraining_bible:8 by ID.
```

Phase 1 drafters use this worked example as the integration model: when drafting their bible's What Was Fixed entries, evaluate each conditional trigger explicitly with FIRES / DOES NOT FIRE notation, even when the trigger doesn't apply.

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

**Recommended TOC:**

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

**Recommended TOC:**

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

**Recommended TOC:**

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

**Recommended TOC:**

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

**Recommended TOC:**

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

**Recommended TOC:**

1. Scope
2. Definitions (table, materialized view, migration, JSONB shadow, canonical column)
3. Schema overview
   - 3.1 14 tables (decomposed list)
   - 3.2 1 materialized view (`trainer_stats`)
   - 3.3 Schema bootstrap (`backend/database/schema/schema.sql`) vs migrations
4. Schema and migration detail
   - 4.1 Per-table documentation
     - 4.1.X.<table_name> — one subsection per table
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

**Recommended TOC:**

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

Within a bible: `§ <section_id>` (e.g., `§ 4.5.10`). Between bibles: `<bible_name>:<section_id>` (e.g., `feature_provenance_bible:8.W.7`; `ml_layer_architecture_bible:5.4`). Matches META_PLAN v6 § 7.11.

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

**Document status:** DRAFT v3, pre-audit
**Audit-CC pass:** pending (v3 audit pending after disk write)
**Verification log:** `_audits/BIBLE_STRUCTURE_SPEC_v3_verification.md` — inherits 25 claims from v2 with re-verified-2026-05-04 timestamps; adds 2 new claims (N9 DD § 19 brevity, N10 cross-reference integrity post-renumbering)
**Tony review:** pending (will see post-audit version per workflow discipline)
**Locked:** [pending]

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

---

## 13. Changelog

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
