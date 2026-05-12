# Convergence Test Audit — v5 Substrate Re-Run (Phase 0 § 5.3 step 5)

**Audit subject:** convergence test re-run on `database_schema_bible.md` against locked v5/v8 substrate
**Audit-CC role:** third fresh CC session — no involvement in run3 or run4 drafting
**Threshold per META_PLAN v8 § 5.3:** identify all material differences between run3 and run4; surface anything borderline as material per the explicit instruction "When borderline, audit-CC flags as material and lets Tony decide." Identify any methodology gaps not closed by G1–G9 in BIBLE_STRUCTURE_SPEC v5 § 12.4.
**Date:** 2026-05-05

**Inputs:**
- `_convergence_test_v5/database_schema_bible_run3.md` (498 lines)
- `_convergence_test_v5/database_schema_bible_run3_verification.md` (467 lines)
- `_convergence_test_v5/database_schema_bible_run4.md` (516 lines)
- `_convergence_test_v5/database_schema_bible_run4_verification.md` (316 lines)

**References (Phase 0 locked):**
- META_PLAN v8 (`_meta/META_PLAN.md`, 1,649 lines)
- BIBLE_STRUCTURE_SPEC v5 (`_meta/BIBLE_STRUCTURE_SPEC.md`, 1,371 lines)
- AUDIT_METHODOLOGY v2 (`_meta/AUDIT_METHODOLOGY.md`)
- CONVERGENCE_CRITERIA v2 (`_meta/CONVERGENCE_CRITERIA.md`)
- TRIAGE_QUEUE_SPEC v1 (`_meta/TRIAGE_QUEUE_SPEC.md`)

**Original test reference:** `_meta/_audits/convergence_test_audit.md` (21 material differences M1–M21 + 9 methodology gaps G1–G9)

**Live substrate cross-checks performed:**
- `wc -l backend/database/migrations/migrate.py` → 157 (confirms both runs)
- `wc -l backend/database/schema/schema.sql backend/database/migrations/001_initial_schema.sql` → 415 / 415 (confirms both runs)
- `grep -hE "^CREATE TABLE" schema.sql migrations/*.sql` → 11 + 11 + 3 = 14 unique tables (confirms both runs)
- `grep -nE "AS total_starts|AS wins|AS win_rate|AS itm|AS itm_rate|AS layoff|AS lasix|AS claimed" 008_create_trainer_stats.sql` → 8 aggregates (confirms both runs)
- `grep -c "^CREATE INDEX" schema.sql` → 12 (confirms run3 N10 self-correction from 13 → 12)
- `grep -nE "model_used|ALTER TABLE wr_predictions ADD COLUMN" migrations/*.sql schema.sql` → zero `ADD COLUMN model_used` statements; only references in 011 preamble (confirms both runs' drift observation)
- `grep -nE "wr_predictions_entry_id_key" migrations/*.sql` → zero matches (the auto-generated 005-form name is not explicitly named in any DROP statement; relevant to G2 application divergence)
- `sed -n '14p' 011_wr_predictions_unique_fix.sql` → "--   Effect: 157 races (~1.35% of 11,629) accumulated 427 duplicate rows." (confirms both runs' verbatim reproduction)

---

## Summary verdict: **CONVERGED-WITH-RESIDUAL**

The v5/v8 gap closures held at structural-equivalence level for all 9 original gaps (G1–G9). Where the original test surfaced direct factual contradictions (M1 RDS Data API yes/no), drift-misses (M2 wr_predictions schema-vs-migration; M3 pl_predictions UNIQUE), and disjoint discipline rosters (M11 1-of-4 / 1-of-7 overlap), the re-run shows convergent factual claims and structurally-aligned interpretations of every closed gap. **All 21 original material differences are addressed at the structural-equivalence layer**: most converge to the same conclusion; the remaining divergences are the substrate-analysis variance the convergence test methodology accepts as expected (per META_PLAN v8 § 5.3 step 5).

The re-run surfaces **2 NEW methodology gaps** not addressed by G1–G9 (within the 1-3 tolerable range per the Path A bar described in the audit prompt):

- **G-new-1: Candidate-roster numbering convention.** § 5.7 G5 closure does not legislate the numbering format Phase 1 drafters use for candidate (pre-ratification) entries. Run3 introduced a CC-flagged `5.A`–`5.I` letter-prefix; run4 used numeric `5.1`–`5.8`. Both are defensible; both surface the choice; the spec under-constrains.
- **G-new-2: Whether the matview counts as a "table" for § 4.1 sub-section enumeration.** § 6.6 § 4.1 says "4.1.X.<table_name> — one subsection per table." Run3 stops at 4.1.14 (excludes `trainer_stats`); run4 includes 4.1.15 (`trainer_stats` as matview-not-table with deferral note). Spec definitions in § 2 distinguish table from matview but § 4.1's enumeration scope is silent on whether matviews enter that loop.

Additionally, **G8 closure (META_PLAN v8 § 7.3 placeholder-resolution sub-rule) shows a drafter-compliance variance** that is not a methodology gap but is worth surfacing: run3's § 8.W.1 still uses "fixed 2026-05-XX" placeholder for migration 011 (a real fix whose date is `git log`-resolvable), and run3's § 8.W.3 uses the non-YYYY-MM-DD form "(fixed via migration 009, date per migration filename)." Run4 ran `stat -c "%y %n"` (V4-13) and committed to `2026-05-01`. The spec is unambiguous (G8 closure mandates resolution); run3 did not apply it. This is execution-discipline drift, not a new methodology gap.

**Recommendation:** Phase 0 has substantially converged. Recommend a **BIBLE_STRUCTURE_SPEC v6 surgical-cosmetic cycle** to close G-new-1 and G-new-2 (both are narrow, substrate-grounded, and admit direct embedded-text resolutions like the v3→v4 audit-CC-recommended resolutions for G1/G2/G4/G6). Phase 0 closes after v6 lock; Phase 1 begins. The G8 compliance variance does not require a methodology revision — it surfaces in Phase 1 audit-CC scope as an existing rule to enforce.

---

## Per-question findings

### Q1 — Read both drafts in full

Both drafts read in full. Section-by-section comparison performed.

- Run3: 8 mandatory sections present; § 1–4 organized with 5-subsection § 3 (3.1 cluster / 3.2 14 tables / 3.3 1 matview / 3.4 bootstrap-vs-migrations / 3.5 prediction-table family at-a-glance) and 14-subsection § 4.1 (one per table 4.1.1–4.1.14) + 5-subsection § 4.2 (matches spec).
- Run4: 8 mandatory sections present; § 1–4 organized with 3-subsection § 3 (3.1 14 tables / 3.2 1 matview / 3.3 schema bootstrap vs migrations) — matches spec § 6.6 verbatim — and 15-subsection § 4.1 (one per table 4.1.1–4.1.14 + 4.1.15 trainer_stats matview with deferral) + 5-subsection § 4.2 (matches spec).
- Both use canonical 5/6/7/8 ordering (mandatory per § 5.2). Both verification logs self-check this.
- Both follow § 5.5 W.N-only-letter-prefix discipline for § 8 entries.

### Q2 — Material differences (per META_PLAN v8 § 5.3 explicit categories)

Enumerated below in **Material-difference enumeration (consolidated)**. Total: **18 material differences**, comparable to the original test's 21.

The major convergence improvements (relative to the original 21 M-list) are these — they are NOT new material differences in the re-run but the original tests' M-list items that the v5/v8 closures resolved:
- Original M1 (RDS Data API direct contradiction): both runs now agree NOT used (run3 N8 + run4 V4-10 with grep evidence).
- Original M3 (pl_predictions UNIQUE): both runs now agree `UNIQUE(entry_id)` per migration 005 + note 011 preamble's "PL/LS pattern" is forward-aspirational (run3 § 4.1.13 + N14; run4 § 4.1.13 + V4-7).
- Original M4 (migrate.py line count 157 vs 158): both runs now agree 157 with explicit note about Read-tool-vs-`wc -l` counting convention (run3 N5; run4 V4-2).
- Original M5 (schema.sql line count 415 vs 416): both runs now agree 415 with the same convention note (run3 N9; run4 V4-1).
- Original M6 (trainer_stats aggregates 7 vs 8): both runs now agree 8 with line-by-line decomposition (run3 N4; run4 V4-3).
- Original M7 (Bug #28 in § 6 yes/no): both runs include with `data_pipeline_bible:#28` cross-reference per G1 closure.
- Original M8 (Deprecated entry count 3 vs 1): both runs converge to 1 main Deprecated entry (legacy `predictions`); both apply G2 closure.
- Original M16 (cross-reference syntax snake_case vs Title Case): both runs use canonical `<bible>:<section>` and `<bible>:#<bug>` per G6 closure.
- Original M17 (JSONB shadow definition disagreement): partial — run3 omits JSONB shadow definition entirely; run4 includes per spec § 6.6 § 2 (this re-emerges as new M16 below).
- Original M18 (fix date placeholder vs committed): re-emerges as new M12/M13 below — G8 closure compliance variance, addressed in **G8 verification** below.

### Q3 — NEW methodology gaps (not closed by G1–G9 in v5)

Two surfaced; see **Methodology-gap findings (NEW gaps)** below.

### Q4 — Gap-closure effectiveness for G1–G9

Per-gap PASS/PARTIAL/FAIL verdicts in **Gap-closure effectiveness verification** below. Summary: **8 PASS + 1 PARTIAL + 0 FAIL** of 9 (G8 partial due to drafter-compliance variance, not methodology ambiguity).

### Q5 — Prophylactic checks (AUDIT_METHODOLOGY v2)

- **§ 5.1 verification-log precision (counts decomposed):** both runs decompose. Run3 decomposes 14 tables = 11 bootstrap + 3 from 005; 12 migrations = 11 prefixes + 1 dup-005; trainer_stats = 1 group key + 8 aggregates; predictions reader inventory = 4 + 2 = 6. Run4 decomposes the same way (Inherited Claim 4, Inherited Claim 5, V4-3, Inherited Claim 16). PASS for both.
- **§ 5.2 methodology-interpolation:** both runs surface candidate constructs explicitly. Run3 self-flags `5.A–5.I` letter-prefix as CC-introduced (verification log methodology-interpolation self-check item 2). Run4 explicitly evaluates 7 surfaced constructs and 2 borderline cases (V4 § D), all traced to authorized sources. **One CC-introduced construct in run3 (the letter-prefix) is the substantive interpolation surface — surfaced for QB per the rule.** PASS at the surfacing level; the construct itself is the substrate of G-new-1 below.
- **§ 5.5 pattern-completion:** both runs respect W.N as the only ratified letter-prefix in published numbering. Run3's `5.A–5.I` is explicitly flagged as provisional candidate-roster IDs (not published rules); QB will renumber to numeric on ratification. Run4 § F explicitly checks pattern-completion clean. PASS for both at the published-rule level.
- **§ 5.7 TOC contradiction (canonical 5/6/7/8 ordering):** both runs hold the canonical ordering. Run3's verification log section "§ 1–4 reorganization deviation log" explicitly evaluates spec § 6.6 latitude. Run4's § G "Convention choices surfaced" explicitly states "NO § 1–4 reorganization deviation taken." PASS for both.

### Q6 — Verdict

CONVERGED-WITH-RESIDUAL — see Summary verdict above. Recommend BIBLE_STRUCTURE_SPEC v6 surgical-cosmetic cycle to close G-new-1 + G-new-2.

---

## Material-difference enumeration (consolidated)

In order of severity (audit-CC judgment; Tony adjudicates).

**M1. § 8 W.N entry count and roster.**
- Run3: 3 W.N entries — 8.W.1 wr_predictions UNIQUE (migration 011), 8.W.2 ls_predictions first-class (migration 010), 8.W.3 pace_delta backfill (migration 009).
- Run4: 1 W.N entry — 8.W.1 wr_predictions UNIQUE (migration 011) only.
- **Audit-CC verification:** all three migration files exist (011, 010, 009) and are real bug-fix-class events per their preambles. G3 closure does not legislate a roster minimum; both rosters are defensible against § 5.6.1 ("one entry per fix the bible's domain remembers"). Whether LS first-class promotion (migration 010) and pace_delta backfill (migration 009) qualify as bug fixes vs design evolutions is drafter judgment. **Material per § 5.3 "scope claim that differs."**

**M2. § 8.W.<n> numbering reordering for the one shared entry.**
- Run3 § 8.W.1 = wr_predictions UNIQUE = migration 011. Run4 § 8.W.1 = wr_predictions UNIQUE = migration 011. **Same fact at same slot — no reordering.** This is a CONVERGENCE relative to original M10 (which had Run1 8.W.1 = pace_delta, Run2 8.W.1 = wr_predictions UNIQUE). G9 (W.N bible-local) + G3 (true bug-fix entries with priority by topic) appear to have stabilized the lead-entry slot through a roster-priority effect. Surfacing only because the original test flagged this as material; the re-run's residual is small.

**M3. § 6 Currently Open entry count and scope.**
- Run3 § 6: 4 entries (Bug #28 cross-reference; wr_predictions schema-vs-migration drift on `model_used`; no dev Aurora cluster; no migration carries down-block).
- Run4 § 6: 1 entry (Bug #28 cross-reference only).
- **Audit-CC verification:** Bug #28 cross-reference entries are convergent (G1 closure HELD). Run3's three additional entries are substrate-grounded: `model_used` drift is real (verified — zero ADD COLUMN statements; column read by `transforms.py:604`); dev Aurora cluster non-existence is operator-stated (META_PLAN v8 § 7.12); down-block absence is verifiable (no DOWN block in migrations 001–011 per substrate read). Run4 does not include these as Currently Open entries; run4 § 4.1.12 mentions the wr_predictions un-audited DDL but does not surface as Currently Open. **Material per § 5.3 "scope claim that differs."** This is the residual of original M7's broader "what counts as Currently Open" question — G1 closure addresses cross-cutting bugs but does not address non-bug-class operational debt. (See G-new-1.5 candidate observation under prophylactic check considerations.)

**M4. § 5 candidate-roster numbering convention.**
- Run3: `5.A`, `5.B`, …, `5.I` (letter-prefix; 9 candidates; CC-introduced and explicitly self-flagged in verification-log methodology-interpolation self-check item 2).
- Run4: `5.1`, `5.2`, …, `5.8` (numeric; 8 candidates).
- **Material per § 5.3 "structural choice that differs in load-bearing way"** because the candidate-roster numbering propagates to all cross-references inside § 5 and from § 8.W.<n>'s "if-fix-produced-Forbidden-Pattern" trigger. Underlies G-new-1.

**M5. § 5 candidate-roster size and overlap.**
- Run3: 9 candidates (5.A–5.I): dispatch metadata in UNIQUE; renaming applied migrations; writing to legacy `predictions`; joining `past_performances` by `race_id` without IS NOT NULL; adding undocumented JSONB; counting `schema_migrations` as 15th table; duplicate-005 is a bug; pace_delta from `finish_call_position`; `schema.sql` is generated.
- Run4: 8 candidates (5.1–5.8): missing rollback DOWN block in 012+; duplicate prefix in 012+; dispatch metadata in UNIQUE; modifying `schema.sql` directly; writing to legacy `predictions`; past_performances.race_id NOT NULL; `model_versions.notes` as JSONB; `feature_importance` defaulting asymmetry.
- **Overlap (3 of 9 / 3 of 8 = ~33%):** dispatch metadata in UNIQUE (run3 5.A = run4 5.3); writing to legacy predictions (run3 5.C = run4 5.5); past_performances.race_id discipline (run3 5.D Forbidden Pattern, run4 5.6 Common Mistake — same substrate, different forcing-function classification).
- **Material.** This is a strong improvement over original M11 (1-of-4 / 1-of-7 = ~14%), but the candidate-roster convergence rule (G5 closure) explicitly says QB ratification is the convergence mechanism — drafters surface candidates, QB picks. Disjoint pre-QB rosters are now expected, not a methodology failure. Surfaced as material because spec is silent on how much overlap is the target.

**M6. § 5 forcing-function classification of the past_performances.race_id NULL discipline.**
- Run3 5.D: Forbidden Pattern ("Joining past_performances by race_id without IS NOT NULL guard").
- Run4 5.6: Common Mistake ("I'll add a NOT NULL constraint to enforce referential integrity" — wrong instinct + corrected position).
- **Same substrate fact, different § 5.6.2 vs § 5.6.3 classification.** Material per § 5.3 "rule statement that differs." (The original test's run2 § 8.W.3 had this as a "discipline codification W.N entry" — both v5 runs correctly route to § 5 per G3 closure; classification within § 5 is the residual question.)

**M7. § 7 Deprecated qualification conclusion for `wr_predictions` superseded UNIQUE forms.**
- Run3 § 7 prose: defers to Phase 1 audit-CC live `\d wr_predictions` verification because the pre-005 auto-generated `wr_predictions_entry_id_key` constraint is not named in any DROP statement and may persist alongside the post-011 form. Conservative reading.
- Run4 § 7.1 sub-section "Superseded SQL constraint Deprecated qualification": commits — both pre-005 form's auto-index ("would have been dropped when the intermediate `unique_per_entry_model_style` form was added (PostgreSQL replacement semantics)") and the intermediate form (DROPped explicitly at 011:64) are physically dropped from the live schema. Decisive reading.
- **Audit-CC verification:** `grep -nE "wr_predictions_entry_id_key" migrations/*.sql` returns zero matches. PostgreSQL replacement semantics — adding a new UNIQUE constraint over a different column tuple does NOT automatically drop the prior auto-generated index. Run3's caution has a substrate basis; run4's "PostgreSQL replacement semantics" claim overreaches. Without live `\d wr_predictions`, neither can be definitively right. **Material per § 5.3 "factual claim that differs"** (substrate-analysis variance under G2's drafter-discretion clause; G2 closure HELD but produces divergent conclusions on the same fact).

**M8. § 6 Currently Open inclusion of wr_predictions `model_used` schema-vs-migration drift.**
- Run3 § 6 #2: explicit Currently Open entry for the drift.
- Run4: noted in § 4.1.12 prose ("intermediate state un-audited DDL") and V4-5 verification, but NOT surfaced as a § 6 Currently Open entry.
- **Audit-CC verification:** verified live — zero `ALTER TABLE wr_predictions ADD COLUMN model_used` statements; column referenced in 011 preamble; column written by `wr_prediction_repository.py:304`. The drift is real. Whether it qualifies as "currently open" or as "documented quirk" is drafter judgment. Material per § 5.3 "scope claim that differs."

**M9. § 4.1 sub-section count and matview enumeration.**
- Run3: 14 sub-sections (4.1.1–4.1.14), one per `CREATE TABLE`. Matview documented at § 3.3 only.
- Run4: 15 sub-sections (4.1.1–4.1.15), with 4.1.15 = `trainer_stats` (matview, not a table) carrying a one-line deferral to § 3.2.
- **Material per § 5.3 "structural choice that differs."** Underlies G-new-2.

**M10. § 3 sub-section count and § 3 framing.**
- Run3 § 3: 5 sub-sections (3.1 cluster / 3.2 14 tables / 3.3 1 matview / 3.4 bootstrap-vs-migrations / 3.5 prediction-table family at-a-glance summary table). Verification log explicitly logs as "deviation: spec has 3 sub-sections; this draft has 5" with rationale.
- Run4 § 3: 3 sub-sections (3.1 / 3.2 / 3.3) — matches spec § 6.6 verbatim. Verification log explicitly states "NO § 1–4 reorganization deviation taken."
- **Material per § 5.3 "structural choice that differs."** Both choices are authorized by G4 closure ("drafter latitude per locality of reference"); both surfaced explicitly. This is G4 application variance, not G4 closure failure.

**M11. § 8.W.1 fix-date format (G8 compliance variance).**
- Run3 § 8.W.1: "fixed 2026-05-XX" (placeholder convention).
- Run4 § 8.W.1: "fixed 2026-05-01" (resolved per `stat -c "%y %n"` in V4-13).
- **Audit-CC verification:** META_PLAN v8 § 7.3 placeholder-resolution sub-rule (locked 2026-05-05 per v7 cycle) mandates: "Phase 1 drafters MUST resolve the date placeholder via `git log` of the relevant primary source ... before locking the bible document containing a W.N entry for a real fix." Migration 011 is a real fix; the date IS knowable from `stat`/`git log`. Run3 violates the locked rule; run4 complies. **Material per § 5.3 "factual claim that differs"** AND a G8 compliance failure by run3 (drafter discipline, not methodology ambiguity).

**M12. § 8.W.3 fix-date format (G3/G8 compounding compliance issue, run3-only).**
- Run3 § 8.W.3 header: "(fixed via migration 009, date per migration filename)" — non-YYYY-MM-DD form.
- Run4: no 8.W.3 entry (LS first-class promoted to 8.W.2 in run3; pace_delta absent in run4).
- Per § 5.6.1 G3 closure: "Fix date (YYYY-MM-DD) — mandatory; entries without a knowable fix date belong in § 5, not § 8." The migration 009 mtime is `stat`-resolvable. Run3 did not run `stat`. **Material per § 5.3 "factual claim that differs."** This is a run3 G8 compliance issue compounding M11.

**M13. § 4.1.12 framing of wr_predictions un-audited DDL.**
- Run3 § 4.1.12: "Schema-vs-migration drift note" prose — describes `model_used` and `wr_predictions_unique_per_entry_model_style` as un-attributable to retained migrations.
- Run4 § 4.1.12: "Intermediate state (un-audited DDL — see § 8.W.1 below): UNIQUE (race_id, entry_id, model_used, style)..." — uses "un-audited DDL" framing across multiple references. Adds LS-enrichment-on-wr_predictions claim per dump § 10 finding #5 (`ensemble_win_prob`, `longshot_prob`, `trajectory_score`, `angle_*`, `longshot_alert`, `confidence` columns alleged to be on wr_predictions).
- **Audit-CC verification:** `grep -nE "longshot_alert|longshot_prob|ensemble_win_prob|trajectory_score" migrations/*.sql schema.sql` finds these as `ls_predictions` columns (lines 68, 73 of 005), NOT as wr_predictions columns. Run4's claim that they exist on wr_predictions traces only to dump finding (not verifiable from migrations alone); without live `\d wr_predictions`, this is dump-as-source. Run3 makes the narrower (only `model_used`) claim. **Material per § 5.3 "factual claim that differs."**

**M14. § 2 "JSONB shadow" definition.**
- Run3 § 2: defines "JSONB column" only; does NOT define "JSONB shadow."
- Run4 § 2: defines both "JSONB shadow" (as a JSONB column with stable-key contract) and "Canonical column."
- **Audit-CC verification:** spec § 6.6 § 2 EXPLICITLY lists "JSONB shadow" among the recommended Definitions for this bible. Run3 omits a spec-prescribed definition. **Material per § 5.3 "scope claim that differs"** (in run3's case: a spec-mandate omission). Note: this is a partial recurrence of original M17 (JSONB shadow definition disagreement); v5 spec is explicit, run3 didn't include.

**M15. Reader inventory file count for legacy `predictions`.**
- Run3 § 4.1.10: 4 files cited — prediction_router.py (4 refs); race_router.py (2 refs); dashboard_router.py:93,105 (direct SELECT); horse_router.py:66 (direct SELECT). Inherits all 4 from META_PLAN v8 Claim 16.
- Run4 § 4.1.10: 2 files cited — prediction_router.py (4 refs); race_router.py (2 refs). "Total 6 references across 2 files."
- **Audit-CC verification:** META_PLAN v8 Claim 16 inventory includes all 4 files (V9 + V10 in run3 verification log inherit them verbatim from META_PLAN). Run4 omits dashboard_router.py and horse_router.py. **Material per § 5.3 "factual claim that differs"** — run4 incomplete relative to the inherited claim.

**M16. Live AWS state verification of cluster ARN.**
- Run3 V4 [INHERITED]: "not directly re-verified live during this draft (no AWS CLI auth available in drafting environment)."
- Run4 V4-11: ran `aws sts get-caller-identity` (account 584812014683 confirmed) and `aws rds describe-db-clusters` (returned `fantasy-baseball-serverless` only — EE cluster not visible). Surfaces a live-state divergence: dump cluster ARN cannot be re-verified at draft time. Three explanatory hypotheses recorded (cluster deleted; constrained role; paused).
- **Material per § 5.3 "scope claim that differs"** (one drafter ran live verification with a divergence finding; the other did not). Run4's surfacing follows AUDIT_METHODOLOGY v2 § 4.5 source-priority discipline (tier 1 trumps tier 6).

**M17. Approximate row counts in per-table sub-sections.**
- Run3: omits row counts in per-table sub-sections (only legacy `predictions` 6,600 cited per inherited Claim 16).
- Run4: includes approximate row counts per dump § 4.1 (tracks 11; entries ~30K; races ~2,611 over 100 days; workouts 143K+; past_performances ~250K+; `predictions` 6,600). Some are operator-stated dump values; not all live-verified.
- **Material per § 5.3 "scope claim that differs"** — run4 includes a class of facts run3 omits.

**M18. § 1 Out-of-scope structuring.**
- Run3 § 1: in-prose negation ("What this bible does **not** document:" with bullets covering data-flow, inference, API, feature-semantics, AWS-config — all with bible-name cross-references).
- Run4 § 1: explicit "**Out of scope (covered by other bibles):**" sub-heading with 5-bullet list naming the canonical-home bible for each, plus an extra Bug #28 cross-cutting bug bullet.
- **Material per § 5.3 "structural choice that differs"** (presentation-equivalent but different reader affordance). Both follow spec § 5.2 canonical TOC item 1.

**Total material differences: 18.**

---

## Methodology-gap findings (NEW gaps not in original G1–G9)

### G-new-1: Candidate-roster numbering convention not specified by § 5.7

**Symptom:** Underlies M4. Run3 introduces letter-prefix `5.A`–`5.I` (CC-introduced; explicitly self-flagged); run4 uses numeric `5.1`–`5.8`. Both interpretations are defensible against the v5 spec.

**Spec under-constraint citation:**
- BIBLE_STRUCTURE_SPEC v5 § 5.7 (locked per v4 cycle) specifies the candidate-roster workflow ("CC drafts § 5 with candidate roster ... CC re-drafts § 5 to match ratified roster") but says nothing about the numeric/alphabetic ID format used for candidates pre-ratification.
- BIBLE_STRUCTURE_SPEC v5 § 5.5 specifies that "Forbidden Patterns, Common Mistakes, and Deprecated entries use sub-section numeric IDs" — this is unambiguous for **ratified** entries. Whether the same numeric IDs apply to **candidate** (pre-ratification) entries, or whether a provisional letter-prefix is acceptable to distinguish unratified from ratified, is not addressed.
- BIBLE_STRUCTURE_SPEC v5 § 5.5.1 (G9 closure) and § 12.4 reaffirm "W.N remains the only ratified letter-prefix in EE bible numbering" — which run3's `5.A`–`5.I` arguably violates, even with the "provisional" flag. Run3's verification log self-check item 2 acknowledges this and surfaces for QB.

**Recommended resolution direction (for BIBLE_STRUCTURE_SPEC v6):**
Embed an explicit clarification at § 5.7 (or § 5.5.1 closing clause): candidate-roster entries pre-ratification use **numeric sub-section IDs** (`5.1`, `5.2`, …) consistent with the ratified-entry convention. The "candidate" status is conveyed by the bible's § 5 header marker (`[candidate roster pending QB ratification per § 5.7]`) — not by ID format. QB renumbering to a final numeric set after ratification preserves drafter-chosen numerics where possible. This eliminates the letter-prefix-as-provisional-marker pattern that runs counter to § 5.5.1's W.N-as-only-ratified-letter-prefix invariant.

### G-new-2: Whether the matview counts as a "table" for § 4.1 sub-section enumeration

**Symptom:** Underlies M9. Run3 omits `trainer_stats` from § 4.1; run4 includes as 4.1.15 with deferral to § 3.

**Spec under-constraint citation:**
- BIBLE_STRUCTURE_SPEC v5 § 6.6 § 4.1: "4.1.X.<table_name> — one subsection per table." The placeholder is `<table_name>`; the matview's name is `trainer_stats`. Whether "table" in this template includes "materialized view" is unspecified.
- BIBLE_STRUCTURE_SPEC v5 § 6.6 § 3.2 ("1 materialized view (`trainer_stats`)") puts the matview in § 3 — suggesting § 3 is its primary home and § 4.1 is the table-only enumeration.
- But § 6.6 also lists `trainer_stats` as part of the schema being documented; under "documented in § 4.1 with one sub-section per persistent storage object" reading, the matview enters the loop.
- § 2 Definitions explicitly distinguishes "Table" (`CREATE TABLE` declaration) from "Materialized view" (`CREATE MATERIALIZED VIEW` declaration). Under that definitional distinction, the matview is NOT a table; § 4.1 enumerates only tables; run3's reading is correct. But run4's reading (include with deferral for completeness) is also defensible because the matview is part of the persistent storage layer documented by this bible.

**Recommended resolution direction (for BIBLE_STRUCTURE_SPEC v6):**
Embed an explicit clarification at § 6.6 § 4.1: "one subsection per persistent relation including matviews" (run4's reading) OR "one subsection per `CREATE TABLE` declaration; matviews documented at § 3 only" (run3's reading). Either resolution is fine — what matters is the spec stating the choice. Audit-CC's recommendation: choose run3's reading (matview at § 3 only, NOT in § 4.1 enumeration) because the § 2 definitional distinction between table and matview is load-bearing for the bible's vocabulary; treating them differently in the enumeration honors the definition.

---

**Subsidiary observation (not surfaced as a third NEW gap; flagged for awareness):**

§ 5.3 G1 closure addresses Currently Open scope for **cross-cutting bugs** (Bug #28 case). It does NOT address whether non-bug-class operational debt (no dev Aurora cluster; no down-block on existing migrations; schema-vs-migration drift on `model_used`) should appear in § 6 Currently Open. Run3 includes 3 such entries; run4 includes 0. Both interpretations are defensible; spec § 5.6 (Currently Open) does not legislate the scope beyond cross-cutting bugs. **This is NOT a NEW methodology gap because § 5.3 explicitly scopes G1 closure to cross-cutting bugs only — the broader Currently Open scope question was never claimed to be closed by G1.** Phase 1 drafters of other bibles (e.g., `data_pipeline_bible:6` Currently Open scope for non-bug operational items) may surface the same question; if it recurs, a v7 cycle could add a Currently Open scope rule. For this re-run, the divergence is within tolerated drafter latitude.

---

## Gap-closure effectiveness verification (G1–G9 from original test)

### G1 (Currently Open scope for cross-cutting bugs) — **PASS**

Both runs apply § 5.3 cross-cutting Currently Open scope rule consistently to Bug #28: both include a one-line cross-reference to `data_pipeline_bible:#28` in their § 6, with substantive description deferred to canonical home.
- Run3 § 6 #1: "Bug #28 (HRN scraper column-shift) — cross-reference to canonical home `data_pipeline_bible:#28`. ... Per BIBLE_STRUCTURE_SPEC v5 § 5.3 G1 closure ..."
- Run4 § 6: "Bug #28 (HRN scraper column-shift; canonical home `data_pipeline_bible:#28`). ... Per BIBLE_STRUCTURE_SPEC v5 § 5.3 G1 closure, this bible includes a one-line cross-reference to the canonical home; the substantive description ... lives in `data_pipeline_bible:#28`."

Original M7's direct disagreement (run1 omits / run2 includes) is closed.

### G2 (Superseded SQL constraint Deprecated qualification) — **PASS** (with substrate-analysis variance per drafter-discretion clause)

Both runs apply § 5.6.4 G2 closure conditional bullet consistently. Both reach "no Deprecated entry required" determinations for the surveyed superseded forms, with verification log entries documenting the determination.
- Run3 § 7 prose + N22: applies G2; concludes neither superseded `wr_predictions` four-column form nor `ls_predictions UNIQUE(entry_id)` qualifies; defers a residual question (pre-005 auto-generated `wr_predictions_entry_id_key`) to Phase 1 audit-CC live `\d` verification. Conservative reading.
- Run4 § 7.1 sub-section + V4-5/V4-6: applies G2; concludes both superseded forms physically dropped; commits. Decisive reading.

Both runs honor the closure's "drafter discretion with verification log entry" clause. The conclusion divergence (M7) is substrate-analysis variance under that explicit drafter-discretion authorization, NOT a closure failure. Original M8's "3 vs 1 Deprecated entries" disagreement is closed at the methodology level (both converge to 1 main entry).

### G3 (§ 8 confined to bug-fix entries with mandatory Fix date) — **PASS**

Neither run includes a non-bug-fix W.N entry. Run2's original 8.W.3 (past_performances.race_id NULL acceptance — discipline codification, not a bug fix) does NOT appear in either run3 or run4. Both runs route this discipline to § 5 (run3 5.D Forbidden Pattern; run4 5.6 Common Mistake).

Both runs' § 8.W.<n> entries are real bug fixes:
- Run3 8.W.1, 8.W.2, 8.W.3 are migrations 011, 010, 009 — all real fix events with corrective DDL.
- Run4 8.W.1 is migration 011.

### G4 (§ 6.X TOC framing — "sections 5–8 mandatory; sections 1–4 recommended-strongly with drafter latitude") — **PASS**

Both runs hold canonical 5/6/7/8 ordering. Both interpret § 1–4 latitude:
- Run3 expands § 3 to 5 sub-sections (logged as "deviation: spec has 3 sub-sections; this draft has 5" with rationale in verification log).
- Run4 holds § 3 at the spec's 3 sub-sections (logged as "NO § 1–4 reorganization deviation taken" in verification log).

Original M12 + M13 (run1 = "Schema and migration detail" § 4; run2 = "Canonical objects" § 4 with PLPrediction/LSPrediction dataclass enumerations) are closed: BOTH v5 runs use "Schema and migration detail" framing for § 4 (run3 § 4 header; run4 § 4 header). Neither run dedicates § 4 to canonical-object documentation; both defer canonical-object documentation to `architecture_overview` per BIBLE_STRUCTURE_SPEC v5 § 4.2.1 boundary.

The M10 § 3 sub-section count residual (5 vs 3) and M9 § 4.1 sub-section count residual (14 vs 15) are within G4's authorized latitude.

### G5 (Discipline rule roster convergence — § 5.7 candidate roster) — **PASS** (at the methodology level; G-new-1 is the residual)

Both runs:
- Mark § 5 as "[candidate roster pending QB ratification per § 5.7]".
- Surface candidate rules from substrate.
- Annotate each candidate with provenance (substrate-grounded vs CC-introduced) per § 5.7 closing clause.
- Defer § 5 lock to QB ratification round-trip per § 5.7 workflow.

Both runs' § 5 closing prose explicitly surfaces the workflow. Run4 surfaces 3 specific QB ratification questions; run3 does not enumerate questions but flags every CC-introduced candidate explicitly.

Original M11 (1-of-4 / 1-of-7 = ~14% overlap on the assumption that the rosters were final) is closed at the methodology level: rosters are candidates pre-ratification, not final. Overlap improves to ~33% (3 of 8/9) which is expected for a candidate-vs-candidate comparison; QB ratification is the convergence step.

The numbering-format divergence (M4 / G-new-1) is the residual — orthogonal to G5 itself.

### G6 (Cross-reference syntax — canonical `<bible>:<section>` and `<bible>:#<bug-id>`) — **PASS**

Both runs use the canonical syntax consistently:
- `data_pipeline_bible:#28` (cross-cutting bug) — in run3 § 6 #1 + N21; in run4 § 1 + § 6 + V4-G.
- `architecture_overview:3.3`, `data_pipeline_bible:3` and `:4`, `feature_provenance_bible:4`, `ml_layer_architecture_bible:4`, `api_frontend_bible:4` — used consistently across both runs.
- `database_schema_bible:8.W.1` (run4 § 8.W.1 CONDITIONAL caveat self-reference using full path).
- `Phase 5.X.Y` PHASE_5_BACKLOG.md placeholder — used in both runs per § 7.1.1 worked example.

Original M16 (snake_case `.md` filenames vs Title Case prose) is closed.

### G7 (CONDITIONAL tertiary state) — **PASS**

Both runs use FIRES / DOES NOT FIRE / CONDITIONAL per § 5.6.1.2 with mandatory adjacent-prose caveats for CONDITIONAL.
- Run3 § 8.W.1, § 8.W.2, § 8.W.3: each conditional-trigger-evaluation block uses FIRES / DOES NOT FIRE / CONDITIONAL with adjacent-prose caveats explicitly headed "The CONDITIONAL caveat:".
- Run4 § 8.W.1 conditional-triggers-evaluated block: same pattern with explicit adjacent-prose caveat.

Neither run uses "PARTIAL" (the original run1 deviation) or "FIRES (advisory)" (the original run2 deviation). G7 closure is tight; both runs comply.

### G8 (Placeholder convention scope; closed in META_PLAN v8 § 7.3 sub-rule) — **PARTIAL**

The closure (META_PLAN v8 § 7.3 placeholder-resolution sub-rule, locked 2026-05-05) mandates that drafters MUST resolve YYYY-MM-XX placeholders via `git log` of the primary source for real fix events whose dates are knowable. Migration 011 is such a real fix; migration 010 is such a real fix; migration 009 is such a real fix.

- Run4: ran `stat -c "%y %n" 011_wr_predictions_unique_fix.sql` (V4-13) → 2026-05-01; committed to "fixed 2026-05-01" in § 8.W.1. **Compliant.**
- Run3: § 8.W.2 (LS first-class) "fixed 2026-05-01" — compliant. § 8.W.1 (wr_predictions UNIQUE) "fixed 2026-05-XX" — **non-compliant; placeholder used for a knowable date.** § 8.W.3 (pace_delta) "fixed via migration 009, date per migration filename" — **non-compliant; not in YYYY-MM-DD form at all.** Run3's verification log does NOT include a `stat`/`git log` resolution step for any of the three migrations.

This is **drafter-compliance variance, not methodology ambiguity.** The locked rule is unambiguous. Run3 did not apply the locked discipline; run4 did. Per § 5.3 step 5 ("If material differences exist that audit-CC reliably caught, methodology is converged"), audit-CC catches the divergence — methodology is converged at the rule level. **PARTIAL** flag here surfaces the within-cycle drafter-discipline drift; it does NOT trigger a methodology revision. Phase 1 audit-CC scope must include this rule on every W.N entry check.

**Recommended next-cycle action:** No spec revision needed for G8. Phase 1 audit-CC checklist includes "verify every W.N entry's Fix date is YYYY-MM-DD form, not placeholder, when fix date is `git log`-resolvable." Bank for AUDIT_METHODOLOGY v3 if pattern recurs across Phase 1 bibles.

### G9 (W.N bible-local; global Bug #N for cross-bible) — **PASS**

Both runs:
- Use `<bible>:#<bug-id>` for cross-cutting bug references (`data_pipeline_bible:#28` in both).
- Treat W.N as bible-local; the W.N reordering between runs (run3 has 8.W.1/2/3; run4 has 8.W.1) does NOT propagate to cross-bible references because cross-references use `#<bug-id>` not `W.<n>`.
- Run4 § 8.W.1 explicitly self-references via `database_schema_bible:8.W.1` (full path) for the CONDITIONAL caveat narrative — illustrating G9's bible-local-W.N + full-path-for-cross-bible discipline.

Original M14 + M15 (W.<n> reordering causes cross-reference target divergence) are closed at the methodology level: cross-references use #N, not W.N. The within-bible W.N reordering is no longer load-bearing for cross-bible reference integrity.

### Summary (PASS / PARTIAL / FAIL): **8 PASS + 1 PARTIAL + 0 FAIL of 9**

---

## Recursive precision discipline check

Both runs reproduce verbatim SQL fragments and source quotes char-exact at the substantive-content level.

- **Migration 011 line 14 ("157 races (~1.35% of 11,629) accumulated 427 duplicate rows."):** both runs reproduce numerics, em-dash, tilde, and parenthetical clause char-exact. Run3 N16 + bible § 8.W.1 Symptom; run4 V4-12 + bible § 8.W.1 Symptom. Run3 adds the words "total" and "prediction" for readability (self-flagged in N16); run4 paraphrases word order from "157 races (~1.35% of 11,629) accumulated 427 duplicate rows" to "427 duplicate rows accumulated across 157 races (~1.35% of 11,629 races)" (self-flagged in § E item 1). Both deviations are minor non-numeric prose adjustments; numerics are char-exact in both. **Compliant.**
- **trainer_stats filter clause:** run4 V4-4 reproduces verbatim including the multi-space alignment of `IS NOT NULL` after `trainer_name    ` (4 spaces) and `finish_position ` (1 space) — the strictest verbatim case in either run4 verification log. Run3 N3 reproduces the HAVING clause only. Both **compliant**.
- **Aurora cluster ARN:** both runs reproduce char-exact (`arn:aws:rds:us-east-1:584812014683:cluster:equinedatabasestack-equinedatabase648a3917-y8mww81ea82f`) including kebab-case region, colon-separated ARN segments, and lowercase hex suffix.
- **schema_migrations DDL:** run3 V3 + run4 V4-section-A re-verification both reproduce `CREATE TABLE IF NOT EXISTS schema_migrations (migration_id SERIAL PRIMARY KEY, filename VARCHAR(255) UNIQUE NOT NULL, applied_at TIMESTAMPTZ DEFAULT NOW())` char-exact at the SQL-content level (Python wrapping indentation stripped per "DDL as executed" convention).

**No precision deviations of the original run1's "elision of `IF NOT EXISTS`" class surface in either run3 or run4.** Run3 does NOT reproduce the `idx_active_model_per_type` UNIQUE INDEX statement verbatim (avoiding the elision risk). Run4 § 4.1.11 paraphrases the index as "partial UNIQUE INDEX permitting one active row per (model_type) value" without quoting the DDL — also avoiding elision risk.

**Net assessment: recursive precision discipline holds in both runs; no MATERIAL precision deviations.**

---

## Recommendation

**Verdict: CONVERGED-WITH-RESIDUAL.** Phase 0 has substantially converged. Recommend a **BIBLE_STRUCTURE_SPEC v6 surgical-cosmetic cycle** to close G-new-1 and G-new-2, both of which admit direct embedded-text resolutions in the v3→v4 audit-CC-recommended-resolution model:

1. **G-new-1 resolution embedded text (§ 5.7 closing clause OR § 5.5.1 closing clause):** Candidate-roster entries pre-ratification use **numeric sub-section IDs** (`5.1`, `5.2`, …) consistent with the ratified-entry convention. The "candidate" status is conveyed by the bible's § 5 header marker (`[candidate roster pending QB ratification per § 5.7]`) — not by a provisional letter-prefix. W.N remains the only ratified letter-prefix.

2. **G-new-2 resolution embedded text (§ 6.6 § 4.1 first sentence):** "one subsection per `CREATE TABLE` declaration; matviews documented at § 3 only" — honoring the § 2 Definitions table-vs-matview distinction. Or, alternatively, "one subsection per persistent storage object (tables AND matviews); matviews carry a one-line deferral to § 3 to avoid duplication." Tony's pick. Audit-CC recommendation: the first option (matview at § 3 only) is more consistent with the bible's vocabulary discipline.

**Path A sequencing (per META_PLAN v8 § 5.4 + BIBLE_STRUCTURE_SPEC v5 § 12.5):** v6 is the third Phase 0 revision triggered by the convergence test. Expected scope is narrow (2 surgical-text embeds). After v6 lock, **the convergence test does NOT need to re-run** — both new gaps are spec-text clarifications with no architectural decision content (cf. v3→v4's 8-gap closure which DID require re-running because architectural decisions resolved). v6 lock can immediately precede Phase 1 start.

**G8 compliance variance:** No spec revision needed. Bank as Phase 1 audit-CC checklist item ("every W.N entry's Fix date is YYYY-MM-DD form when `git log`-resolvable; placeholders only for forward-looking discipline codifications"). If pattern recurs across Phase 1 bibles, AUDIT_METHODOLOGY v3 cycle absorbs it. For now, the rule is unambiguous and run3's drift is a one-bible-one-drafter-one-cycle compliance miss, not a recurring class pattern.

**Alternative path (if Tony judges G-new-1 + G-new-2 below the surgical-cycle threshold):** declare convergence as-is and start Phase 1; let Phase 1 drafters of the other 6 bibles surface the same questions if they recur. The candidate-roster numbering question almost certainly recurs (every Phase 1 bible has § 5); the matview-as-table question is database-specific (only this bible has matviews). If declaring convergence as-is, Phase 1 drafters of all bibles use numeric `5.1`–`5.N` for candidate-roster entries (run4's pattern) by audit-CC adjudication of the W.N-as-only-ratified-letter-prefix rule.

**Audit-CC's recommendation:** Path B (declare convergence as-is) is defensible. Path A (v6 surgical cycle) is cleaner and adds <1 cycle to Phase 0; the cost is small and the coherence value is high. Tony to decide.

---

**End of convergence test audit (v5 substrate re-run).**
