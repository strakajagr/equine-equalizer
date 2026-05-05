-- Migration 007: Backfill trainer_name into past_performances
-- Links PP rows → entries → trainers via the races table.
-- Join path: pp.(race_date+track_code+race_number+horse_id)
--          → races.(race_date+track_id+race_number)
--          → entries.(race_id+horse_id)
--          → trainers.(trainer_id)
-- Enables trainer win-rate features in feature_engineering_service.

UPDATE past_performances pp
SET trainer_name = t.trainer_name
FROM entries e
JOIN races r
    ON r.race_id = e.race_id
JOIN trainers t
    ON t.trainer_id = e.trainer_id
JOIN tracks tk
    ON tk.track_id = r.track_id
WHERE r.race_date   = pp.race_date
  AND tk.track_code = pp.track_code
  AND r.race_number = pp.race_number
  AND e.horse_id    = pp.horse_id
  AND pp.trainer_name IS NULL
  AND t.trainer_name IS NOT NULL
