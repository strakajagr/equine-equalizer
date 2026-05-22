-- Gate 6 §A — drop schema columns that are dead-no-source after census audit
--
-- All listed columns were verified by /scripts/gate5_census.py to be
-- 100% NULL (or 100% FALSE for booleans) across 2022-01 → 2026-05-31.
-- They have no ingestion path that ever populates them.
--
-- Status: AUTHORED. Do NOT execute without reviewing the impact on:
--   - models/canonical.py (PastPerformance dataclass references these)
--   - repositories/transforms.py (reads these from row dicts)
--   - chart_parser.py (likely doesn't write them but check)
--
-- Backout: each DROP can be reversed by ALTER TABLE ADD COLUMN.
--
-- AUDIT EVIDENCE (from EE_GATE5_CENSUS_MASTER_20260522_0156.csv):
--   entries.bute                          : always FALSE (0/207,409 TRUE)
--   entries.blinkers_first_time           : always FALSE (0/207,409)
--   entries.tongue_tie                    : always FALSE (0/207,409)
--   entries.bar_shoes                     : always FALSE (0/207,409)
--   entries.front_bandages                : always FALSE (0/207,409)
--   entries.mud_caulks                    : always FALSE (0/207,409)
--   entries.equipment_change_from_last    : always FALSE (0/207,409)
--   entries.medication_change_from_last   : always FALSE (0/207,409)
--   entries.is_entry                      : always FALSE (0/207,409)
--   races.going_stick_reading             : 0% non-null
--   races.moisture_level                  : 0% non-null
--   races.rail_position                   : 0% non-null
--   races.track_variant                   : 0% non-null
--   races.wind_speed                      : 0% non-null
--   races.wind_direction                  : 0% non-null
--   races.off_turf                        : always FALSE (0/25,951)
--   results.is_disqualified               : always FALSE (0/201,469)
--   results.beyer_speed_figure            : 0% non-null (real Beyer in PPs already)
--   results.final_time                    : 0% non-null (final_time in PPs already)
--   past_performances.race_start_number   : 0% non-null
--   workouts.exercise_rider               : 0% non-null
--
-- past_performances.race_id is EXCLUDED from this drop — it's documented in
-- CLAUDE.md as NULL-by-design and used elsewhere as a nullable foreign key.

-- ─── entries: 9 dead boolean flags ──────────────────────────────
ALTER TABLE entries DROP COLUMN IF EXISTS bute;
ALTER TABLE entries DROP COLUMN IF EXISTS blinkers_first_time;
ALTER TABLE entries DROP COLUMN IF EXISTS tongue_tie;
ALTER TABLE entries DROP COLUMN IF EXISTS bar_shoes;
ALTER TABLE entries DROP COLUMN IF EXISTS front_bandages;
ALTER TABLE entries DROP COLUMN IF EXISTS mud_caulks;
ALTER TABLE entries DROP COLUMN IF EXISTS equipment_change_from_last;
ALTER TABLE entries DROP COLUMN IF EXISTS medication_change_from_last;
ALTER TABLE entries DROP COLUMN IF EXISTS is_entry;

-- ─── races: 7 dead environmental fields ─────────────────────────
ALTER TABLE races DROP COLUMN IF EXISTS going_stick_reading;
ALTER TABLE races DROP COLUMN IF EXISTS moisture_level;
ALTER TABLE races DROP COLUMN IF EXISTS rail_position;
ALTER TABLE races DROP COLUMN IF EXISTS track_variant;
ALTER TABLE races DROP COLUMN IF EXISTS wind_speed;
ALTER TABLE races DROP COLUMN IF EXISTS wind_direction;
ALTER TABLE races DROP COLUMN IF EXISTS off_turf;

-- ─── results: 3 dead/redundant fields ───────────────────────────
ALTER TABLE results DROP COLUMN IF EXISTS is_disqualified;
ALTER TABLE results DROP COLUMN IF EXISTS beyer_speed_figure;
ALTER TABLE results DROP COLUMN IF EXISTS final_time;

-- ─── past_performances: 1 dead field ────────────────────────────
ALTER TABLE past_performances DROP COLUMN IF EXISTS race_start_number;

-- ─── workouts: 1 dead field ─────────────────────────────────────
ALTER TABLE workouts DROP COLUMN IF EXISTS exercise_rider;

-- Total: 21 columns dropped across 5 tables.
