# PHASE_5_BACKLOG.md

**Document:** PHASE_5_BACKLOG
**Status:** ACTIVE (Phase 5 cleanup queue; continuously updated through Phase 4 per META_PLAN v6 § 4.3)
**Created:** 2026-05-04 (Phase 0 exit prerequisite per META_PLAN v6 § 8.2)
**Format:** per TRIAGE_QUEUE_SPEC v1 (locked 2026-05-04)

**Purpose:** This file is Phase 5's deferred-work tracker. Findings from Phase 1+ audits that operator defers to Phase 5 transfer here from the active triage queue per TRIAGE_QUEUE_SPEC v1 § 4.3. Bugs surfaced before Phase 1 (e.g., Bug #28 surfaced during EE_CURRENT_STATE_DUMP generation) enter directly per the Phase 0 exit-prerequisite seed.

**Format:** entries follow TRIAGE_QUEUE_SPEC v1 § 3 (mandatory + conditional fields). The active triage queue feeds into this file via explicit transfer per § 4.3; this file's internal organization (sectioning, prioritization, scheduling) is Phase 5's concern, governed by the entry format but not by additional discipline TRIAGE_QUEUE_SPEC codifies.

**Severity taxonomy:** inherited from META_PLAN v6 § 11. BLOCKER / MATERIAL / MINOR / STYLE. METHODOLOGY-INTERPOLATION applies to methodology drafts only; not used in this file (operational entries).

---

## Entries

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
