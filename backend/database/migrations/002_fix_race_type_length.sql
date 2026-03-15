-- race_type VARCHAR(20) is too short for
-- 'allowance_optional_claiming' (28 chars).
-- Also widen past_performances.race_type
-- to match.
ALTER TABLE races
  ALTER COLUMN race_type TYPE VARCHAR(50);

ALTER TABLE past_performances
  ALTER COLUMN race_type TYPE VARCHAR(50);
