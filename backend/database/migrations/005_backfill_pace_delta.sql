-- Migration 005: Compute pace_delta from position change
-- pace_delta = finish_call_position - call_2_position
-- Negative = gained positions (good), consistent with the
-- existing convention where negative = accelerated.
-- Example: call_2=4, finish=1 → 1-4 = -3 (gained 3 spots)
-- transforms.py fallback now also uses this formula.

UPDATE past_performances
SET pace_delta = finish_call_position - call_2_position
WHERE call_2_position IS NOT NULL
  AND finish_call_position IS NOT NULL
  AND pace_delta IS NULL
