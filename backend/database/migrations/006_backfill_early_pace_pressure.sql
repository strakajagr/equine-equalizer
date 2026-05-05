-- Migration 006: Compute early_pace_pressure per race
-- Count of horses at call_1_position <= 3 in the same race.
-- Joined via (race_date, track_code, race_number) because
-- race_id is not populated in past_performances (0%).
-- Higher value = more speed horses = contested early pace.

UPDATE past_performances pp
SET early_pace_pressure = sub.front_pack_count
FROM (
    SELECT
        race_date,
        track_code,
        race_number,
        COUNT(*) AS front_pack_count
    FROM past_performances
    WHERE call_1_position <= 3
      AND call_1_position IS NOT NULL
      AND race_number IS NOT NULL
    GROUP BY race_date, track_code, race_number
) sub
WHERE pp.race_date   = sub.race_date
  AND pp.track_code  = sub.track_code
  AND pp.race_number = sub.race_number
  AND pp.early_pace_pressure IS NULL
