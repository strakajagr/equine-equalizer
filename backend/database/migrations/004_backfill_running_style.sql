-- Migration 004: Backfill running_style from call_1_position
-- Uses per-horse average of call_1_position across all PPs.
-- Thresholds match RUNNING_STYLE_THRESHOLDS in constants.py.
-- transforms.py already computes this as a fallback at load
-- time, but storing it enables SQL-level filtering.

UPDATE past_performances pp
SET running_style = CASE
    WHEN avg_call1 <= 2.0 THEN 'front_runner'
    WHEN avg_call1 <= 4.0 THEN 'presser'
    WHEN avg_call1 <= 6.0 THEN 'midpack'
    ELSE 'closer'
END
FROM (
    SELECT horse_id, AVG(call_1_position) AS avg_call1
    FROM past_performances
    WHERE call_1_position IS NOT NULL
    GROUP BY horse_id
) sub
WHERE pp.horse_id = sub.horse_id
  AND pp.running_style IS NULL
  AND pp.call_1_position IS NOT NULL
