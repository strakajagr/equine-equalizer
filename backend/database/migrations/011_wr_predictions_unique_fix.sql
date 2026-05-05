-- Migration 011: wr_predictions UNIQUE constraint fix + duplicate cleanup
--
-- Background:
--   wr_predictions had UNIQUE (race_id, entry_id, model_used, style).
--   model_used is a per-horse dispatch metadata flag set by
--   WRInferenceService.predict_race based on workout availability —
--   each horse goes through ONE model variant per inference, never both.
--
--   Including model_used in the UNIQUE constraint is an architectural
--   mistake: when workout data lands between inference runs, the same
--   (race_id, entry_id, style) accumulates a 'core' row AND a 'full' row.
--   The new variant doesn't conflict with the old key, so both persist.
--
--   Effect: 157 races (~1.35% of 11,629) accumulated 427 duplicate rows.
--   Downstream consumers (LS softmax, ComparePage Cartesian, track_record
--   double-counting) read both variants without filtering model_used.
--
-- Fix: match the PL / LS pattern — UNIQUE (race_id, entry_id, style).
--   model_used stays as a metadata column; the latest variant overwrites
--   cleanly via the existing SET clause in WR repo's INSERT statement.
--
-- This migration runs cleanup + constraint swap as a SINGLE transaction.
-- PostgreSQL acquires ACCESS EXCLUSIVE on wr_predictions during the
-- ALTER TABLE, so concurrent WR inference INSERTs either wait on the
-- lock or get aborted; their retry logic handles either case.

BEGIN;

-- ─── Pre-state visibility (informational only) ────────────────────────
DO $$
DECLARE
  dup_count INT;
  affected_races INT;
BEGIN
  SELECT COUNT(*), COUNT(DISTINCT race_id)
    INTO dup_count, affected_races
  FROM (
    SELECT race_id, ROW_NUMBER() OVER (
      PARTITION BY race_id, entry_id, style
      ORDER BY created_at DESC, prediction_id DESC
    ) AS rn FROM wr_predictions
  ) t WHERE rn > 1;

  RAISE NOTICE 'Pre-state: % duplicate rows across % races',
    dup_count, affected_races;
END $$;

-- ─── Delete older duplicates, keep most recent per key ─────────────────
DELETE FROM wr_predictions
WHERE prediction_id IN (
  SELECT prediction_id FROM (
    SELECT prediction_id,
      ROW_NUMBER() OVER (
        PARTITION BY race_id, entry_id, style
        ORDER BY created_at DESC, prediction_id DESC
      ) AS rn
    FROM wr_predictions
  ) ranked
  WHERE rn > 1
);

-- ─── Drop old UNIQUE; add the (race_id, entry_id, style) variant ──────
ALTER TABLE wr_predictions
  DROP CONSTRAINT IF EXISTS wr_predictions_unique_per_entry_model_style;

ALTER TABLE wr_predictions
  ADD CONSTRAINT wr_predictions_unique_per_entry_style
  UNIQUE (race_id, entry_id, style);

-- ─── Post-state checks (abort transaction if either fails) ────────────
DO $$
DECLARE
  remaining_dups INT;
  has_new_constraint INT;
BEGIN
  SELECT COUNT(*) INTO remaining_dups FROM (
    SELECT ROW_NUMBER() OVER (
      PARTITION BY race_id, entry_id, style
      ORDER BY created_at DESC, prediction_id DESC
    ) AS rn FROM wr_predictions
  ) t WHERE rn > 1;

  IF remaining_dups > 0 THEN
    RAISE EXCEPTION 'Cleanup left % duplicate rows', remaining_dups;
  END IF;

  SELECT COUNT(*) INTO has_new_constraint
  FROM pg_constraint
  WHERE conrelid = 'wr_predictions'::regclass
    AND conname = 'wr_predictions_unique_per_entry_style';

  IF has_new_constraint = 0 THEN
    RAISE EXCEPTION 'New UNIQUE constraint not found on wr_predictions';
  END IF;

  RAISE NOTICE 'Post-state: 0 duplicates, new constraint installed';
END $$;

COMMIT;
