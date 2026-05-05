-- Migration 009: Backfill pace_delta using finish_position
-- Migration 005 used finish_call_position (0% populated).
-- finish_position is 99.5% populated and semantically identical
-- (position at the wire). Valid finish codes are 1–30; codes >= 90
-- mean DNF/pulled/vet scratch and are excluded.
-- pace_delta = finish_position - call_2_position
-- Negative = gained positions (good). Positive = backed up (bad).
-- e.g. call_2=4, finish=1 → 1-4 = -3 (gained 3 spots)

UPDATE past_performances
SET pace_delta = finish_position - call_2_position
WHERE call_2_position   IS NOT NULL
  AND finish_position   IS NOT NULL
  AND call_2_position   BETWEEN 1 AND 99
  AND finish_position   BETWEEN 1 AND 89
  AND pace_delta        IS NULL
