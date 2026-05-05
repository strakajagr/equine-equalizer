-- Migration 010: ls_predictions first-class
--
-- Background: ls_predictions has been an orphan since the LS service was
-- introduced. Its `insert_prediction` repo method has never been called;
-- LS data has been written as enrichment columns on wr_predictions
-- (longshot_alert, longshot_prob, ensemble_win_prob, etc.).
--
-- Tony's revised architecture (2026-05-01): treat LS as a first-class model
-- with its own ranking. LS will write to ls_predictions in addition to
-- continuing the wr_predictions enrichment (so frontend reads stay working
-- during transition).
--
-- This migration:
-- 1. Adds columns missing for first-class parity with wr_predictions
-- 2. Drops the old single-column UNIQUE (entry_id) — replaced with the
--    (race_id, entry_id, style) pattern matching wr_predictions /
--    pl_predictions UPSERT semantics. Existing rows: 0 (verified empty),
--    so the constraint switch is safe.

BEGIN;

-- ─── Add columns for first-class parity ───────────────────────────────
ALTER TABLE ls_predictions
  ADD COLUMN IF NOT EXISTS style VARCHAR(50) DEFAULT 'general',
  ADD COLUMN IF NOT EXISTS market_prob NUMERIC,
  ADD COLUMN IF NOT EXISTS edge_pct NUMERIC,
  ADD COLUMN IF NOT EXISTS is_top_pick BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS morning_line_implied_prob NUMERIC;

-- ─── Replace UNIQUE constraint with the standard pattern ──────────────
-- Old: UNIQUE (entry_id) — too restrictive (one row per entry, no style differentiation)
-- New: UNIQUE (race_id, entry_id, style) — matches wr_predictions / pl_predictions
-- The single-column UNIQUE is backed by an auto-generated index that
-- can only be dropped by dropping the constraint (PostgreSQL semantics).
ALTER TABLE ls_predictions
  DROP CONSTRAINT IF EXISTS ls_predictions_entry_id_key;
DROP INDEX IF EXISTS ls_predictions_entry_id_key;
ALTER TABLE ls_predictions
  ADD CONSTRAINT ls_predictions_unique_per_entry_style
  UNIQUE (race_id, entry_id, style);

COMMIT;
