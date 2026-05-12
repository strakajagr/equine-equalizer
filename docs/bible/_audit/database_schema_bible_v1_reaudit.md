# Database & Schema Bible v1-patched — Re-audit Report

**Document:** database_schema_bible_v1_reaudit
**Phase:** 1 (Bible) — adversarial re-audit of v1-patched (post-surgical-patch state of deliverable 2 of 7)
**Status:** RE-AUDIT v1 (re-audit-CC pass complete)
**Author:** re-audit-CC (fresh adversarial session under META_PLAN v9 § 6.2 explicit adversarial scope)
**Date:** 2026-05-05

**Tier:** 3 per META_PLAN v9 § 4.1 + § 6.5.

**Anchored on:** META_PLAN v9 (LOCKED 2026-05-05) + BIBLE_STRUCTURE_SPEC v6 (LOCKED 2026-05-05) + Architecture Overview v3 (LOCKED 2026-05-05) + AUDIT_METHODOLOGY v2-patched (lessons § 4.8-§ 4.11 banked 2026-05-05).

**Subject documents:**
- Bible draft (v1-patched): `database_schema_bible.md` (890 lines)
- Companion verification log (v1-patched): `_audit/database_schema_bible_v1_verification.md` (1081 lines)
- AUDIT_METHODOLOGY.md (v2-patched): `_meta/AUDIT_METHODOLOGY.md` (1360 lines)
- Prior audit report (driving findings the patch was supposed to close): `_audit/database_schema_bible_v1_audit.md` (464 lines)
- Drafting spec (the original contract): `_meta/database_schema_bible_v1_drafting_spec.md` (584 lines)

**Adversarial scope.** Per META_PLAN v9 § 6.2: this re-audit operates under the six-question scope (what's unverifiable from referenced material; what's missing per stated scope; where is language ambiguous; where does the deliverable contradict itself or other deliverables; what feels rushed/hand-waved; what examples are missing). Re-audit-CC has no investment in the patches landing as the patch-spec promised; the patch-CC and QB do.

---

## Section A: Re-audit scope and method

**Documents read in full at re-audit time:**
- `database_schema_bible.md` (v1-patched, 890 lines) — full read
- `_audit/database_schema_bible_v1_verification.md` (v1-patched, 1081 lines) — full read
- `_meta/AUDIT_METHODOLOGY.md` (v2-patched, 1360 lines) — full read of patched lessons § 4.8-§ 4.11 + revision history; rest of file already in re-audit-CC's cache from prior cycle
- `_audit/database_schema_bible_v1_audit.md` (the prior audit driving the patch, 464 lines) — full read
- `_meta/database_schema_bible_v1_drafting_spec.md` — already in re-audit-CC's cache
- META_PLAN v9 § 4.5, § 6.1, § 6.2, § 6.5, § 7.3, § 7.12, § 8.6, § 11 — already in re-audit-CC's cache
- BIBLE_STRUCTURE_SPEC v6 § 5.3, § 5.5, § 5.6, § 5.7, § 6.6 — already in re-audit-CC's cache
- `architecture_overview.md` v3 — already in re-audit-CC's cache

**Verification commands re-run at re-audit time:**
- `git log --format="%cs %h %s" -- backend/database/migrations/002_fix_race_type_length.sql` (D-3.1 closure verification)
- Per-migration `git log` loop covering all 12 migration files (V1-patch-1 verbatim-paste re-verification)
- `grep -nE "FROM wr_predictions|FROM ls_predictions" backend/repositories/ls_prediction_repository.py` (V1-patch-5 re-verification + D-8 closure)
- `head -6 backend/database/migrations/005_backfill_pace_delta.sql` and `head -6 backend/database/migrations/009_backfill_pace_delta_v2.sql` (V1-patch-7 re-verification)
- `grep -c "Bug #28"` / `awk + grep -c "trainer_stats"` / `grep -c "candidate; pending QB ratification"` / `grep -nE "^### 5\."` / `grep -c "DELETE FROM schema_migrations"` / `grep -c "ls backend/database/migrations"` against patched bible (V1-patch-9 + Step 6 sweep re-verification)
- `grep -nE "^### F\." verification.md` (Section F entry presence)
- `grep -nE "^### 4\." AUDIT_METHODOLOGY.md` (lesson banking presence)
- Per-section diff `diff <(awk H<n>) <(awk H<n>)` for H1-H9 char-exact reproduction
- `grep -nE "§ 5\.3|§ 5.3"` against bible + verification log (stale cross-reference scan)
- Read of patched § 4.2.4 / § 4.1.12 / § 4.1.14 / § 8.W.2 prose for new methodology-interpolation
- All 14 Primary readers lines re-read for R2.2.b compression consistency

**Sandbox limitations declared:**
- Live API endpoint (`gb5qlfy10h.execute-api.us-east-1.amazonaws.com/dashboard/metrics`) is reachable but not re-fetched at re-audit time (V1-12 was independently verified in the prior audit; not re-verified here because no patch touched V1-12).
- Live AWS state and direct DB queries are NOT runnable from the sandbox; any V1-N claim depending on those is not independently re-verifiable here. None of the patches introduced new Tier 1 / Tier 3 claims; no new exposure.
- `git log` runnable; V1-8 rewrite + V1-patch-1 verbatim sweep independently re-verifiable.

---

## Section B: Prior-finding closure status

### B.1 D-3.1 BLOCKER (§ 8.W.2 fabricated fix date)

**Finding: CLOSED.**

**Re-audit substrate (verbatim, 2026-05-05):**

```
$ git log --format="%cs %h %s" -- backend/database/migrations/002_fix_race_type_length.sql
2026-03-15 d93c4c4 Fix post_time TIMESTAMPTZ, race_type length, and connection isolation
```

Bible § 8.W.2 line 865 title: `### 8.W.2 races.race_type VARCHAR(20) too short for canonical race-type strings (no global Bug #N; fixed 2026-03-15)`. Bible § 8.W.2 line 869 fix-date prose: `**Fix date: 2026-03-15** (per `git log --format="%cs %h %s" -- backend/database/migrations/002_fix_race_type_length.sql`, returning `2026-03-15 d93c4c4 Fix post_time TIMESTAMPTZ, race_type length, and connection isolation`). Per META_PLAN v9 § 7.3 placeholder-resolution sub-rule, this is the canonical W.N Fix date — the actual descriptive commit `d93c4c4` is git-recoverable for migration 002, distinct from the baseline-commit-only history of migration 011 (8.W.1).` The bible cites the verbatim git-log output and applies META_PLAN v9 § 7.3 honestly.

**V1-8 verification log rewrite verified verbatim per Lesson § 4.10 (verbatim-paste discipline):** independent re-run of the per-migration `git log` sweep matches the verification log Section C V1-8 entry's pasted output character-for-character. All 12 migrations enumerated; 3 (001/002/003) with real 2026-03-15 commits + 9 (004-011) with baseline-commit-only 2026-05-04. No summarization; no paraphrase. Lesson § 4.10 satisfied.

**No drift introduced.**

### B.2 D-1.1 MATERIAL (§ 4.2.1 procedural-sequencing prose)

**Finding: CLOSED.**

**Re-audit substrate (verbatim, 2026-05-05):**

```
$ grep -c "ls backend/database/migrations" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
0
```

Zero hits. The "per-author discipline ensures the next NNN slot is consulted (via `ls backend/database/migrations/`) before a filename is committed" prose was deleted from § 4.2.1. The retained sentence "the date component disambiguates same-day siblings via prefix uniqueness" is substrate-grounded (about the format itself, not procedural prescription).

**No drift introduced.**

### B.3 D-1.2 MATERIAL (§ 4.2.4 procedural rollback workflow)

**Finding: CLOSED.**

**Re-audit substrate (verbatim, 2026-05-05):**

```
$ grep -c "DELETE FROM schema_migrations" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
0
```

Zero hits. The "manually executes the down-block SQL ... then manually `DELETE FROM schema_migrations WHERE filename = '<rolled-back-file>'`" procedural sequencing was deleted from § 4.2.4. The retained prose paraphrases META_PLAN v9 § 7.12 lines 864-867 directly: "rollback SQL lives in the **same migration file**, after the up SQL, in a clearly-delimited block. The migration runner does NOT auto-execute the down block. Rollback is operator-driven."

**Independent methodology-interpolation re-scan of patched § 4.2.4 prose (re-audit-CC):** the retained sentences trace to META_PLAN v9 § 7.12 verbatim or paraphrase. The "Current state of in-file down-blocks at lock" paragraph is a substrate observation about migration 010 + 011 BEGIN/COMMIT structure, with explicit "this is per-migration safety, not a rollback path" disclaimer; not procedural prescription. No new methodology-interpolation introduced.

**No drift introduced.**

### B.4 D-4.1 MATERIAL (§ 4.1.12 wr_predictions reader inventory)

**Finding: CLOSED.**

**Re-audit substrate (read of bible § 4.1.12 line 549, verbatim):**

> "**Primary readers.** `wr_prediction_repository.py` for the WR-specific repo surface. Cross-table reads from `ls_prediction_repository.py:262` (`get_longshot_alerts_by_date` — `FROM wr_predictions p`) and `ls_prediction_repository.py:374` (`get_track_record` — `FROM wr_predictions p`); these methods read `wr_predictions` despite living in the LSPredictionRepository class because LS data is currently second-pass enrichment on `wr_predictions` columns (per migration 010 preamble + verification log F.3). Migration 011 preamble names downstream LS softmax + ComparePage Cartesian + track_record consumers as the duplicate-row consumers fixed by § 8.W.1. Per-route detail at `api_frontend_bible:4.1`."

The patched § 4.1.12 reader inventory:
- Names `wr_prediction_repository.py` (the repo module).
- Adds the LS cross-table reads at `ls_prediction_repository.py:262` and `:374` with method-name + FROM-clause citation per R2.3.a.
- Defers per-route HTTP detail to `api_frontend_bible:4.1`.

The R2.2.b compression intent is honored: per-route enumeration deferred, repo-module-level + cross-table reads documented at the schema-bible-domain layer.

**Independent re-verification of cited line numbers (Lesson § 4.10 verbatim-paste discipline applied):**

```
$ grep -nE "FROM wr_predictions|FROM ls_predictions" backend/repositories/ls_prediction_repository.py
98:               FROM ls_predictions p
158:               FROM ls_predictions p
262:               FROM wr_predictions p
374:               FROM wr_predictions p
```

Line 262 + line 374 both confirmed. No line-shift drift between patch authoring and re-audit time.

**No drift introduced.**

### B.5 D-4.2 MATERIAL (§ 4.1.13 + § 4.1.14 reader inventories)

**Finding: CLOSED.**

**Re-audit substrate (read of bible § 4.1.13 + § 4.1.14 Primary readers, verbatim):**

§ 4.1.13 (line 584): `**Primary readers.** `pl_prediction_repository.py` for the PL-specific repo surface. Per-route detail at `api_frontend_bible:4.1`.`

§ 4.1.14 (line 632): `**Primary readers.** `ls_prediction_repository.py`. Read methods that query `ls_predictions` directly: `get_predictions_by_race` (line 98), `get_predictions_by_date` (line 158), `get_todays_predictions` (delegates to by-date). Read methods on the same class that query `wr_predictions` instead (the LS-as-enrichment-on-wr_predictions pattern per migration 010 preamble): `get_longshot_alerts_by_date` (line 262), `get_track_record` (line 374). Writer: `insert_prediction` (line 282) is dead code per migration 010 preamble's note. Per-route detail at `api_frontend_bible:4.1`.`

§ 4.1.13 compressed per R2.2.b. § 4.1.14 enumerates per-method read targets with line citations per R2.3.a (the substrate gap audit-CC D-4.2 + D-8 surfaced is now documented).

**Per-method decomposition check (META_PLAN v9 § 6.5 verification log precision rule applied to bible body):** "3 read FROM ls_predictions; 2 read FROM wr_predictions" decomposes per the cited line numbers (98 + 158 + delegates-to-by-date for ls_predictions; 262 + 374 for wr_predictions). The "delegates to by-date" attribution for `get_todays_predictions` is substrate-grounded (re-audit-CC's prior full read of `ls_prediction_repository.py:175-182` confirms the method calls `self.get_predictions_by_date(date_type.today())`). Decomposition: 3 + 2 = 5 active read methods; +1 dead-code writer (`insert_prediction` at line 282); = 6 method-level entries on the class. Sound.

**No drift introduced.**

### B.6 D-8 MATERIAL (F.3 LS cross-table read pattern documentation)

**Finding: CLOSED.**

**Re-audit substrate (verification log Section F line 665, verbatim):**

> "### F.3 <FRAMEWORK_GAP: ls_prediction_repository.py cross-table read pattern (LS class methods reading FROM wr_predictions)>"

F.3 entry includes:
- Substrate (verbatim grep output for lines 98/158/262/374).
- Class docstring quote at lines 199-204 ("LS data is written as second-pass enrichment to wr_predictions columns ...").
- Reframing candidate per Lesson 4 (one-repo-per-table assumption violated; symmetric § 4.1.12 + § 4.1.14 documentation).
- Substrate citations supporting and refuting alternative reframings.
- Tony ratification stamp 2026-05-05 with R2.3.a + Phase 5 backlog queue notation.

The bible's § 4.1.12 + § 4.1.14 cite F.3 by name (verification log F.3); the cross-bible navigation closes the loop. Substrate-completeness gap is honestly surfaced and documented per Lesson 4 discipline.

**No drift introduced.**

### B.7 D-1.3 MINOR (§ 5.3 borderline-procedural last paragraph)

**Finding: CLOSED (resolved by Q3.3.c § 5.3 deletion).**

**Re-audit substrate (verbatim, 2026-05-05):**

```
$ grep -nE "^### 5\." /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
729:### 5.1 Forbidden Pattern: Including per-row dispatch metadata in a UNIQUE constraint when the dispatch is cross-row coherent at a coarser key
758:### 5.2 JSONB conventions — schemas live in writer code
```

§ 5 contains only § 5.1 + § 5.2; § 5.3 deleted entirely per Q3.3.c. The "Document the absence of `ON DELETE CASCADE` explicitly; if cascading deletes are desired, add them via migration with explicit reasoning in the migration preamble" sentence (the audit-CC D-1.3 borderline-procedural prose) was inside the deleted § 5.3 and is no longer in the bible.

**Forward-deferral note presence (per Q3.3.c instruction "Add a forward-deferral note at end of § 5"):** the note exists at bible line 800 with substrate-grounded language pointing to `data_pipeline_bible:5`. The note is unnumbered (no `### 5.3` header); see Section D-1 finding for the stale-reference issue this introduces.

**No drift introduced specifically by the § 5.3 deletion**, but a downstream stale cross-reference at § 5 lead paragraph surfaces in Section D-1 as a NEW MINOR finding.

### B.8 D-9 MINOR (§ 4.2.5 self-contradiction)

**Finding: CLOSED.**

**Re-audit substrate (read of bible § 4.2.5 line 721, verbatim):**

> "**Production target.** Cross-reference `architecture_overview:3.3` for the canonical RDS instance metadata (engine version, instance class, endpoint, database name); this bible does not duplicate the metadata."

The duplicated metadata (engine version `postgres 16.6`, instance class `db.t4g.micro`, endpoint `equine-db.cgtuh834bttd.us-east-1.rds.amazonaws.com:5432`, database `equine_equalizer`) was removed from the v1 sentence; the cross-reference to `architecture_overview:3.3` retained; the "this bible does not duplicate the metadata" claim is now accurate (no preceding duplication to contradict it).

**No drift introduced.**

### B.9 D-10 MINOR (§ 4.1.7 backfill enumeration completeness)

**Finding: CLOSED.**

**Re-audit substrate (read of bible § 4.1.7 line 362, verbatim):**

> "Several columns are **computed-stored** (pace_delta, running_style, early_pace_pressure) and were populated by backfill migrations (004, 005's `005_backfill_pace_delta.sql`, 006, 009 — migration 009 superseded migration 005's pace_delta backfill because `finish_call_position` was 0%-populated; see § 4.2.1 + § 4.2.2 duplicate-005 case)."

Migration 005's `005_backfill_pace_delta.sql` now included in the enumeration with the supersession note. Cross-references to § 4.2.1 + § 4.2.2 resolve correctly.

**Independent re-verification (Lesson § 4.10 applied; V1-patch-7 substrate sample):**

```
$ head -2 backend/database/migrations/005_backfill_pace_delta.sql
-- Migration 005: Compute pace_delta from position change
-- pace_delta = finish_call_position - call_2_position
$ head -3 backend/database/migrations/009_backfill_pace_delta_v2.sql
-- Migration 009: Backfill pace_delta using finish_position
-- Migration 005 used finish_call_position (0% populated).
-- finish_position is 99.5% populated and semantically identical
```

The bible's "migration 009 superseded migration 005's pace_delta backfill because `finish_call_position` was 0%-populated" claim is verbatim-grounded against migration 009's preamble. Sound.

**No drift introduced.**

---

## Section C: Tony ratification landing status

### C.1 Q1 (F.1 ratification)

**Status: LANDED.**

**Substrate:** verification log Section F F.1 entry line 649 carries ratification stamp: `**Tony ratification 2026-05-05:** Tony ratified F.1 on 2026-05-05; bible content stands; prediction-precision lesson banked in AUDIT_METHODOLOGY.md.`

**Banking verification:** AUDIT_METHODOLOGY.md § 4.11 (line 681) "V1-N grep predictions against `schema.sql` + `migrations/*.sql` must account for byte-identity edge cases" carries the substantive prediction-precision lesson. Four-element structure verified (Abstract rule + Worked example + Cross-references + Audit-CC prophylactic check template).

### C.2 Q2.d (F.2 Option C + queue for PHASE_5_BACKLOG)

**Status: LANDED.**

**Substrate:** verification log Section F F.2 entry line 663 carries ratification stamp: `**Tony ratification 2026-05-05:** Tony ratified Option C on 2026-05-05; bible content stands; queued for PHASE_5_BACKLOG.md addition at Phase 0 exit alongside Bug #28 first-entry.`

**Bible content unchanged** for the F.2-related substrate gap prose at § 4.1.12 + § 4.1.13 (Option C: accepted as known-substrate-gap noted in bible prose with neutral language).

### C.3 Q3.1 (§ 5.1 Forbidden Pattern ratification)

**Status: LANDED.**

**Substrate:**

```
$ grep -nE "^### 5\.1" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
729:### 5.1 Forbidden Pattern: Including per-row dispatch metadata in a UNIQUE constraint when the dispatch is cross-row coherent at a coarser key
```

§ 5.1 title no longer carries the "(candidate; pending QB ratification)" suffix.

```
$ grep -c "candidate; pending QB ratification" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
0
$ grep -c "candidate roster pending" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
0
```

The `[candidate roster pending QB ratification per § 5.7]` header marker at § 5 lead is removed.

### C.4 Q3.2 (§ 5.2 JSONB conventions ratification)

**Status: LANDED.**

**Substrate:**

```
$ grep -nE "^### 5\.2" /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
758:### 5.2 JSONB conventions — schemas live in writer code
```

§ 5.2 title no longer carries the "(candidate; pending QB ratification)" suffix.

### C.5 Q3.3.c (§ 5.3 moved to data_pipeline_bible)

**Status: LANDED with MINOR drift surfaced as Section D-1 finding.**

**Substrate (deletion verified):**

```
$ grep -nE "^### 5\." /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
729:### 5.1 Forbidden Pattern: Including per-row dispatch metadata in a UNIQUE constraint when the dispatch is cross-row coherent at a coarser key
758:### 5.2 JSONB conventions — schemas live in writer code
```

§ 5.3 absent. The forward-deferral note appears at bible line 800 (unnumbered; no ### header):

> "**Forward deferral note (Tony's Q3.3.c ratification 2026-05-05).** A candidate Common Mistake about producer-side parent-row verification before child INSERTs is canonically homed in `data_pipeline_bible:5` per BIBLE_STRUCTURE_SPEC v6 § 5.3 cross-cutting bug scope rule (the producer-side discipline is canonically homed where the producer's flow lives). Candidate-roster status pending data_pipeline_bible drafting cycle."

**Drift:** the § 5 lead paragraph at bible line 727 references "§ 5.3 forward-deferral note below" but § 5.3 was deleted entirely; the note exists below but is unnumbered. See Section D-1 finding (NEW MINOR).

### C.6 R4.b (Lesson 13 banking)

**Status: LANDED at AUDIT_METHODOLOGY.md § 4.10 per file's existing § 4.X = Lesson X convention.**

**Substrate:**

```
$ grep -nE "^### 4\." /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/AUDIT_METHODOLOGY.md
177:### 4.1 Verification-log precision rule
229:### 4.2 Methodology-interpolation rule with named patterns + catch-all + grandfathering clause
298:### 4.3 Audit-CC retroactive sweep discipline
341:### 4.4 Operator-verified external source pattern
385:### 4.5 Pattern-completion interpolation pattern
435:### 4.6 "Tony's locked decision based on a wrong premise" pattern
495:### 4.7 TOC contradiction class (architectural insight)
553:### 4.8 QB substrate findings during spec authorship require Tony ratification before spec corrections
596:### 4.9 QB review pass is light surface review only; substrate verification is audit-CC's job
640:### 4.10 Verbatim-paste discipline for V1-N entries
681:### 4.11 V1-N grep predictions against `schema.sql` + `migrations/*.sql` must account for byte-identity edge cases
```

§ 4.10 carries the verbatim-paste discipline (the patch-spec called it "Lesson 13"; AUDIT_METHODOLOGY.md's § 4.X = Lesson X convention re-numbers it as Lesson 10). The substrate observation about labeling-vocabulary mismatch is captured in verification log Section I V1-patch-10.

**Four-element structure verified (per AUDIT_METHODOLOGY.md's existing convention):**

```
$ sed -n '640,680p' /home/strakajagr/projects/equine-equalizer/docs/bible/_meta/AUDIT_METHODOLOGY.md | grep -E "^####"
#### Abstract rule
#### Worked example
#### Cross-references
#### Audit-CC prophylactic check template
```

All four required structural elements present. Same verified for § 4.8, § 4.9, § 4.11.

**AUDIT_METHODOLOGY.md revision history entry verified at line 13:** `v2-patched (2026-05-05): four lessons banked in § 4 (Lessons § 4.8 / § 4.9 / § 4.10 / § 4.11) emerged from the Database & Schema Bible v1 cycle ...`

---

## Section D: New adversarial findings

### D-1 (MINOR): § 5 lead paragraph cites "§ 5.3 forward-deferral note below" but § 5.3 was deleted

**Bible § 5 lead paragraph at line 727 (verbatim):**

> "Two rules surfaced from substrate analysis (the schema files + migration files + repository writer code) and ratified by Tony on 2026-05-05. A third candidate (Common Mistake about producer-side parent-row verification before child INSERTs) was moved to data_pipeline_bible's candidate roster per § 5.3 forward-deferral note below."

**Substrate (verbatim, 2026-05-05):**

```
$ grep -nE "^### 5\." /home/strakajagr/projects/equine-equalizer/docs/bible/database_schema_bible.md
729:### 5.1 Forbidden Pattern: Including per-row dispatch metadata in a UNIQUE constraint when the dispatch is cross-row coherent at a coarser key
758:### 5.2 JSONB conventions — schemas live in writer code
```

§ 5.3 does not exist in the bible. Per Q3.3.c ratification, § 5.3 was deleted entirely; the forward-deferral note was added but as an unnumbered paragraph (no `### 5.3` header), placed at bible line 800 inside § 5.2's substrate-provenance paragraph immediate vicinity.

**Drift class:** stale internal cross-reference. The reader can find the note descriptively ("below") but the "§ 5.3" label is incorrect — § 5.3 doesn't exist as a numbered sub-section. The cross-reference fails to resolve to a sub-section ID.

**Severity: MINOR.** Per META_PLAN v9 § 6.3 (severity tiers operative throughout v9): citation accuracy issues that don't fabricate substrate AND don't block reader navigation are MINOR. The reader is not misled about substance (the note exists and says what § 5 lead claims it says); the navigational label is the only inaccuracy. MINOR findings do not bear on Tony's lock threshold (META_PLAN v9 § 11) — but should be opportunistically patched.

**Recommendation:** rephrase the § 5 lead paragraph reference. Two equivalent options:

- Option (a) — descriptive: "...per the forward-deferral note at end of § 5 below."
- Option (b) — promote to numbered sub-section: re-add `### 5.3 Forward-deferral note (Common Mistake homed in data_pipeline_bible per Q3.3.c ratification)` as a third sub-section header containing the existing forward-deferral note text. (Note: this would re-introduce a § 5.3 sub-section but as a forward-deferral marker, not as a discipline rule. Whether this aligns with Q3.3.c's intent — "delete § 5.3 entirely" — is QB's call.)

Audit-CC recommends Option (a) (descriptive, no § 5.3 re-introduction; minimum semantic change consistent with Q3.3.c's "delete entirely" intent).

### D-2 through D-N: ZERO additional new findings surfaced

**Methodology-interpolation re-scan (target ZERO):** independent scan of patched § 4.2.4 (rollback prose), § 4.1.12 / § 4.1.13 / § 4.1.14 (reader inventory prose), § 8.W.2 (fix-date prose), F.3 (verification log Section F entry), and AUDIT_METHODOLOGY.md § 4.8-§ 4.11 (banked lessons) surfaces ZERO new methodology-interpolation. Each new sentence traces to META_PLAN v9 § 7.12 / § 7.3 / § 6.5 / § 8.6 / § 6.1 / Tony ratification 2026-05-05 / substrate verification.

The patched § 4.2.4 retained substrate-observation paragraphs ("Current state of in-file down-blocks at lock") which are descriptive, not procedurally prescriptive ("Migration 010 and 011 wrap their schema mutations in BEGIN; ... COMMIT;" + explicit "this is per-migration safety, not a rollback path" disclaimer). No new procedural sequencing.

The new prose in F.3 ("the bible's per-table reader-inventory frame assumes one repository module ↔ one table") is a substrate-grounded observation about the framework slot, not a methodology-interpolation; per Lesson 4 (BIBLE_STRUCTURE_SPEC v6 § 5.3 / META_PLAN v9 § 6.5 + audit-CC's prior banking), surfacing framework gaps with reframing IS the discipline.

The new lessons § 4.8-§ 4.11 banked in AUDIT_METHODOLOGY.md introduce methodology constructs — but they ARE methodology (the file is the methodology corpus); each lesson explicitly traces to META_PLAN v9 / Tony ratification / substrate verification per its Cross-references subsection. Banking new methodology in AUDIT_METHODOLOGY.md is the file's purpose. No interpolation in the bible itself.

**Pattern-completion re-scan (G-new-1 + G-new-2):** § 5 has § 5.1 + § 5.2 only (no § 5.A, § 5.4, etc.). G-new-2 closure: `awk + grep -c "trainer_stats"` returns 0 in § 4.1 region. No new letter-prefixes. PASS.

**Citation accuracy re-scan (Check 1, Check 8):** new line numbers (`ls_prediction_repository.py:262, 374`; `wr_inference_service.py:616-626`) re-verified against the working tree at re-audit time; no line-shift drift. The git-log substrate citations (`d93c4c4`, `2026-03-15`) re-verified by independent re-run. Cross-bible references (`architecture_overview:3.3`, `data_pipeline_bible:5`, `data_pipeline_bible:#28`, `feature_provenance_bible:4.2`, `ml_layer_architecture_bible:4.3`, `api_frontend_bible:4.1`) use section-anchor format per Check 8.

The one stale citation (D-1 above: `§ 5.3 forward-deferral note below`) is the only Check 1 finding. All other cross-references resolve correctly.

**Count decomposition re-scan (META_PLAN v9 § 6.5):** patched § 4.1.14 enumerates "3 read FROM ls_predictions; 2 read FROM wr_predictions" with line citations; decomposition matches independent grep output. No compressible aggregations introduced.

**No-fabrication re-scan (META_PLAN v9 § 8.6) + Lesson § 4.10 verbatim-paste discipline:** sampled V1-patch-1, V1-patch-5, V1-patch-7, V1-patch-9 for verbatim-paste compliance. Each entry's pasted command output matches independent re-run character-for-character at re-audit time. No PARAPHRASE-DRIFT or DRIFT findings.

**Source-priority discipline re-scan (META_PLAN v9 § 4.5):** patches added Tier 4 substrate citations only (working-tree code post-baseline 87dec36 via `grep` / `git log` / file reads). No Tier 4 confidence applied to non-Tier-4 sources.

**FRAMEWORK_GAP / SPEC_GAP completeness:** F.1 + F.2 + F.3 stand with Tony ratification stamps. No new substrate gaps surfaced beyond the already-documented three.

**Boundary-statement adherence re-scan:** D-9 § 4.2.5 RDS metadata duplication closed; § 4.1.X reader inventories defer per-route detail to `api_frontend_bible:4.1` consistently. No remaining boundary lapses.

**AUDIT_METHODOLOGY.md structural integrity:** 4 new lessons banked at sequential § 4.X slots; revision history entry added at v2-patched; each lesson follows the file's existing four-element structure; no new structural conventions invented. The labeling-vocabulary mismatch (patch-spec said "Lesson 11/12/13" but file uses § 4.X = Lesson X with continuation at slot 8) is documented honestly in verification log Section I V1-patch-10. No new findings.

---

## Section E: Lock threshold re-evaluation (META_PLAN v9 § 11)

| Gate | v1 audit state | v1-patched re-audit state |
|---|---|---|
| Zero fabricated-content findings | **FAIL** (D-3.1 BLOCKER fabricated fix date) | **PASS** (D-3.1 closed; § 8.W.2 fix date corrected to 2026-03-15 with verbatim git-log substrate; V1-8 rewrite uses verbatim per-migration sweep) |
| Zero methodology-interpolation findings | **FAIL** (D-1.1 + D-1.2 MATERIAL methodology-interpolation; D-1.3 MINOR borderline) | **PASS** (D-1.1 + D-1.2 deleted; D-1.3 vanished with § 5.3 deletion; independent re-scan of patched prose surfaces zero new methodology-interpolation) |
| < 5 MATERIAL findings | **FAIL** (5 MATERIAL: D-1.1, D-1.2, D-4.1, D-4.2, D-8) | **PASS** (zero MATERIAL findings post-patch; the one new finding D-1 is MINOR, not MATERIAL) |
| Zero un-closed prior-cycle findings | N/A (v1 first cycle) | **PASS** (all 9 prior findings closed: D-3.1 + D-1.1 + D-1.2 + D-4.1 + D-4.2 + D-8 + D-1.3 + D-9 + D-10) |

**Re-audit verdict:** Tony's lock threshold (META_PLAN v9 § 11) is met: zero fabricated-content findings, zero methodology-interpolation findings, < 5 MATERIAL findings (zero MATERIAL), zero un-closed prior-cycle findings.

The one new finding D-1 is MINOR per META_PLAN v9 § 6.3 severity tiers; MINOR findings do not bear on the lock threshold per Tony's bar.

---

## Section F: Recommended dispositions

| ID | Severity | Finding | Recommendation | Rationale |
|---|---|---|---|---|
| D-1 | MINOR | § 5 lead paragraph stale "§ 5.3 forward-deferral note below" reference | **Surgical patch (opportunistic).** Replace "per § 5.3 forward-deferral note below" with "per the forward-deferral note at end of § 5 below" (Option (a) from § D-1 above). MINOR severity does not block lock per Tony's threshold. | META_PLAN v9 § 6.3 severity tiers; Q3.3.c "delete § 5.3 entirely" intent honored by Option (a) descriptive replacement |

**Lock recommendation:** **READY FOR LOCK** at Tony's threshold. The one MINOR (D-1) is opportunistically patchable but not lock-blocking.

If Tony accepts the v1-patched draft as-is with D-1 deferred, lock proceeds. If Tony wants D-1 closed before lock, a 1-line surgical patch (replace "§ 5.3 forward-deferral note below" with "the forward-deferral note at end of § 5 below" at bible line 727) satisfies the closure with no other surface touched.

QB synthesizes this re-audit + Tony decides the lock pathway.

---

## Section G: Re-audit-CC self-discipline check

**Methodology-interpolation by re-audit-CC: ZERO new constructs introduced in this re-audit report.**

The re-audit operates under upstream-ratified frameworks:
- **Severity tiers (BLOCKER / MATERIAL / MINOR):** ratified throughout META_PLAN v9 (§ 11 lock threshold; revision history references). No new severity tier introduced.
- **Finding forms (CLOSED / DRIFT-INTRODUCED / INCOMPLETE / REGRESSED / VERIFIED / DRIFT / METHODOLOGY-INTERPOLATION / PARAPHRASE-DRIFT / UNVERIFIABLE-FROM-WORKING-TREE):** prescribed by the re-audit prompt itself (Step 2 + Step 4). No new finding form introduced.
- **Six-question adversarial scope:** ratified in META_PLAN v9 § 6.2. Re-audit-CC operated under the six questions verbatim.
- **Lesson § 4.10 verbatim-paste discipline:** newly banked but per Tony's R4.b ratification 2026-05-05; operative as upstream-locked methodology starting v1-patched. Re-audit-CC applied the discipline to its own findings — verbatim quotes from primary sources, not summaries (see B.1, B.2, B.3, B.4, B.5, B.7, B.8, B.9 substrate sections; D-1 substrate quote).
- **No-fabrication rule (META_PLAN v9 § 8.6):** invoked, not extended.
- **Lock threshold (META_PLAN v9 § 11):** invoked, not extended.
- **Source-priority hierarchy (META_PLAN v9 § 4.5):** invoked, not extended.

**No re-audit-CC-prescribed:**
- Binary tests beyond those ratified upstream.
- Cadence rules (re-audit-CC does not specify when re-re-audit must happen if D-1 is deferred; that is QB's call).
- Completeness criteria (re-audit-CC does not specify how many findings constitute "complete"; the prompt prescribes the scope).
- Scoring rubrics (re-audit-CC does not score the bible quantitatively; severity tiers come from META_PLAN v9).
- Iteration caps (re-audit-CC does not specify how many surgical-patch cycles before SUBSTANTIAL REWORK; that is QB's call per QB handoff § 6.5).
- Percentage criteria (re-audit-CC does not assert "X% of findings are MATERIAL"; finding count is what it is — 1 MINOR).
- Procedural sequencing rules (re-audit-CC does not prescribe operator workflow; recommendations route to QB synthesis).

**Re-audit-CC's recommendations defer to upstream authority:** the D-1 disposition routes to QB for synthesis, with Tony as the architectural authority per META_PLAN v9 § 6.3. Re-audit-CC does not lock anything.

**Verbatim-paste discipline applied to re-audit-CC's own substrate citations:** every command output cited in this report is pasted verbatim from independent re-run at re-audit time, not summarized. Quoted bible text is char-exact from the patched draft.

**Self-discipline check: PASS.**

---

## End of Re-audit Report

**Findings summary:** 9 prior findings CLOSED (1 BLOCKER + 5 MATERIAL + 3 MINOR) + 6 Tony ratifications LANDED (Q1, Q2.d, Q3.1, Q3.2, Q3.3.c, R4.b) + 1 NEW MINOR (D-1 stale § 5.3 reference). Section H char-exact reproduction PASS for H1-H8 (H9 boundary marker drift expected, not real).

**Lock threshold verdict:** Tony's threshold met (zero fab + zero methodology-interp + < 5 MATERIAL + zero un-closed). **READY FOR LOCK.**

**Disposition recommendation:** lock as-is with D-1 deferred OR 1-line surgical patch closing D-1 then lock. QB synthesizes; Tony decides.

**Re-audit-CC self-discipline:** ZERO new methodology constructs introduced; severity tiers, finding forms, no-fabrication rule, source-priority hierarchy, lock threshold, and Lesson § 4.10 verbatim-paste discipline all trace to upstream-locked META_PLAN v9 / BIBLE_STRUCTURE_SPEC v6 / AUDIT_METHODOLOGY v2-patched / re-audit prompt prescriptions.
