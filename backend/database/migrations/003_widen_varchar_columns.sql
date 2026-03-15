-- Widen all VARCHAR columns that may receive
-- values longer than 20 characters from
-- real-world race data

-- race_type already fixed in 002
-- Fix remaining columns throughout schema

ALTER TABLE races
  ALTER COLUMN surface TYPE VARCHAR(50),
  ALTER COLUMN track_condition TYPE VARCHAR(50),
  ALTER COLUMN moisture_level TYPE VARCHAR(50),
  ALTER COLUMN weather_conditions TYPE VARCHAR(100),
  ALTER COLUMN wind_direction TYPE VARCHAR(20);

ALTER TABLE entries
  ALTER COLUMN program_number TYPE VARCHAR(10);

ALTER TABLE past_performances
  ALTER COLUMN surface TYPE VARCHAR(50),
  ALTER COLUMN race_type TYPE VARCHAR(50),
  ALTER COLUMN track_condition TYPE VARCHAR(50),
  ALTER COLUMN moisture_level TYPE VARCHAR(50),
  ALTER COLUMN weather_conditions TYPE VARCHAR(100),
  ALTER COLUMN wind_direction TYPE VARCHAR(20),
  ALTER COLUMN running_style TYPE VARCHAR(30),
  ALTER COLUMN pace_scenario TYPE VARCHAR(30);

ALTER TABLE workouts
  ALTER COLUMN track_condition TYPE VARCHAR(50),
  ALTER COLUMN workout_type TYPE VARCHAR(50);
