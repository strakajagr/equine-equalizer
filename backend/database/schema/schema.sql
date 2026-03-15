-- ═══════════════════════════════════════════
-- EXTENSIONS
-- ═══════════════════════════════════════════

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ═══════════════════════════════════════════
-- TABLE 1: tracks
-- ═══════════════════════════════════════════

CREATE TABLE tracks (
  track_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  track_code VARCHAR(10) UNIQUE NOT NULL,
  track_name VARCHAR(100) NOT NULL,
  location VARCHAR(100),
  timezone VARCHAR(50) DEFAULT 'America/New_York',
  surfaces TEXT[],
  is_qualifying BOOLEAN DEFAULT false,
  min_claiming_price INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════
-- TABLE 2: horses
-- ═══════════════════════════════════════════

CREATE TABLE horses (
  horse_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  registration_id VARCHAR(50) UNIQUE,
  horse_name VARCHAR(100) NOT NULL,
  sire VARCHAR(100),
  dam VARCHAR(100),
  dam_sire VARCHAR(100),
  sire_id UUID REFERENCES horses(horse_id),
  dam_id UUID REFERENCES horses(horse_id),
  dam_sire_id UUID REFERENCES horses(horse_id),
  foaling_date DATE,
  country_of_origin VARCHAR(10) DEFAULT 'USA',
  sex VARCHAR(10),
  color VARCHAR(50),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════
-- TABLE 3: trainers
-- ═══════════════════════════════════════════

CREATE TABLE trainers (
  trainer_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  trainer_name VARCHAR(100) NOT NULL,
  license_number VARCHAR(50),
  country VARCHAR(10) DEFAULT 'USA',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════
-- TABLE 4: jockeys
-- ═══════════════════════════════════════════

CREATE TABLE jockeys (
  jockey_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  jockey_name VARCHAR(100) NOT NULL,
  license_number VARCHAR(50),
  country VARCHAR(10) DEFAULT 'USA',
  is_apprentice BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════
-- TABLE 5: races
-- ═══════════════════════════════════════════

CREATE TABLE races (
  race_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  track_id UUID NOT NULL REFERENCES tracks(track_id),
  race_date DATE NOT NULL,
  race_number INTEGER NOT NULL,
  post_time TIMESTAMPTZ,
  distance_furlongs DECIMAL(4,1) NOT NULL,
  surface VARCHAR(20) NOT NULL,
  race_type VARCHAR(20) NOT NULL,
  grade INTEGER,
  race_name VARCHAR(200),
  purse INTEGER,
  claiming_price INTEGER,
  conditions TEXT,
  field_size INTEGER,
  rail_position DECIMAL(4,1),
  track_condition VARCHAR(20),
  moisture_level VARCHAR(20),
  track_variant INTEGER,
  going_stick_reading DECIMAL(4,2),
  temperature INTEGER,
  weather_conditions VARCHAR(50),
  wind_speed INTEGER,
  wind_direction VARCHAR(10),
  off_turf BOOLEAN DEFAULT false,
  equibase_race_id VARCHAR(100) UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(track_id, race_date, race_number)
);

-- ═══════════════════════════════════════════
-- TABLE 6: entries
-- ═══════════════════════════════════════════

CREATE TABLE entries (
  entry_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  race_id UUID NOT NULL REFERENCES races(race_id),
  horse_id UUID NOT NULL REFERENCES horses(horse_id),
  trainer_id UUID NOT NULL REFERENCES trainers(trainer_id),
  jockey_id UUID REFERENCES jockeys(jockey_id),
  post_position INTEGER NOT NULL,
  program_number VARCHAR(5),
  morning_line_odds DECIMAL(8,2),
  weight_carried INTEGER,
  allowance_weight INTEGER DEFAULT 0,
  apprentice_allowance INTEGER DEFAULT 0,
  lasix BOOLEAN DEFAULT false,
  lasix_first_time BOOLEAN DEFAULT false,
  bute BOOLEAN DEFAULT false,
  blinkers_on BOOLEAN DEFAULT false,
  blinkers_off BOOLEAN DEFAULT false,
  blinkers_first_time BOOLEAN DEFAULT false,
  tongue_tie BOOLEAN DEFAULT false,
  bar_shoes BOOLEAN DEFAULT false,
  front_bandages BOOLEAN DEFAULT false,
  mud_caulks BOOLEAN DEFAULT false,
  equipment_change_from_last BOOLEAN DEFAULT false,
  medication_change_from_last BOOLEAN DEFAULT false,
  is_scratched BOOLEAN DEFAULT false,
  scratch_reason VARCHAR(200),
  is_entry BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(race_id, horse_id)
);

-- ═══════════════════════════════════════════
-- TABLE 7: past_performances
-- ═══════════════════════════════════════════

CREATE TABLE past_performances (
  pp_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  horse_id UUID NOT NULL REFERENCES horses(horse_id),
  race_id UUID REFERENCES races(race_id),

  -- Race identification
  race_date DATE NOT NULL,
  track_code VARCHAR(10) NOT NULL,
  race_number INTEGER,
  race_start_number INTEGER,

  -- Race conditions
  distance_furlongs DECIMAL(4,1),
  surface VARCHAR(20),
  race_type VARCHAR(20),
  claiming_price_entered INTEGER,
  claiming_price_taken INTEGER,
  was_claimed BOOLEAN DEFAULT false,
  purse INTEGER,
  field_size INTEGER,
  track_condition VARCHAR(20),
  moisture_level VARCHAR(20),
  track_variant INTEGER,
  going_stick_reading DECIMAL(4,2),
  temperature INTEGER,
  weather_conditions VARCHAR(50),
  wind_speed INTEGER,
  wind_direction VARCHAR(10),
  off_turf BOOLEAN DEFAULT false,

  -- Connections
  jockey_name VARCHAR(100),
  trainer_name VARCHAR(100),
  previous_trainer VARCHAR(100),
  trainer_change BOOLEAN DEFAULT false,
  jockey_change BOOLEAN DEFAULT false,
  apprentice_allowance INTEGER DEFAULT 0,
  weight_carried INTEGER,

  -- Medication
  lasix BOOLEAN DEFAULT false,
  lasix_first_time BOOLEAN DEFAULT false,
  bute BOOLEAN DEFAULT false,

  -- Equipment
  blinkers_on BOOLEAN DEFAULT false,
  blinkers_off BOOLEAN DEFAULT false,
  blinkers_first_time BOOLEAN DEFAULT false,
  tongue_tie BOOLEAN DEFAULT false,
  bar_shoes BOOLEAN DEFAULT false,
  front_bandages BOOLEAN DEFAULT false,
  mud_caulks BOOLEAN DEFAULT false,
  equipment_change_from_last BOOLEAN DEFAULT false,
  medication_change_from_last BOOLEAN DEFAULT false,

  -- Post and finish
  post_position INTEGER,
  finish_position INTEGER,
  official_finish INTEGER,
  lengths_behind DECIMAL(5,2),
  is_disqualified BOOLEAN DEFAULT false,
  photo_finish BOOLEAN DEFAULT false,
  nose_bob BOOLEAN DEFAULT false,
  disqualification_involved BOOLEAN DEFAULT false,
  stewards_inquiry BOOLEAN DEFAULT false,

  -- Speed figures
  beyer_speed_figure INTEGER,
  timeform_rating INTEGER,
  equibase_speed_figure INTEGER,
  winner_beyer INTEGER,
  field_average_beyer DECIMAL(6,2),

  -- Leader fractional times (seconds)
  fraction_1 DECIMAL(6,2),
  fraction_2 DECIMAL(6,2),
  fraction_3 DECIMAL(6,2),
  final_time DECIMAL(6,2),

  -- This horse's own fractional times (seconds)
  horse_fraction_1 DECIMAL(6,2),
  horse_fraction_2 DECIMAL(6,2),
  horse_fraction_3 DECIMAL(6,2),

  -- Running positions at each call
  call_1_position INTEGER,
  call_1_lengths DECIMAL(5,2),
  call_2_position INTEGER,
  call_2_lengths DECIMAL(5,2),
  call_3_position INTEGER,
  call_3_lengths DECIMAL(5,2),
  stretch_position INTEGER,
  stretch_lengths DECIMAL(5,2),
  finish_call_position INTEGER,

  -- Pace (computed in transform, stored for performance)
  early_pace_figure DECIMAL(6,2),
  late_pace_figure DECIMAL(6,2),
  pace_delta DECIMAL(6,2),
  pace_scenario VARCHAR(20),
  running_style VARCHAR(20),
  early_pace_pressure INTEGER,

  -- Race context
  winner_name VARCHAR(100),
  second_name VARCHAR(100),
  third_name VARCHAR(100),
  winner_time DECIMAL(6,2),
  closing_odds DECIMAL(8,2),
  morning_line_that_day DECIMAL(8,2),
  was_favorite BOOLEAN DEFAULT false,
  odds_rank_in_field INTEGER,
  class_rating INTEGER,
  days_since_last_race INTEGER,

  -- Comments
  comment TEXT,
  trouble_comment TEXT,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(horse_id, race_date, track_code, race_number)
);

-- ═══════════════════════════════════════════
-- TABLE 8: workouts
-- ═══════════════════════════════════════════

CREATE TABLE workouts (
  workout_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  horse_id UUID NOT NULL REFERENCES horses(horse_id),
  workout_date DATE NOT NULL,
  track_code VARCHAR(10) NOT NULL,
  distance_furlongs DECIMAL(4,1) NOT NULL,
  workout_time DECIMAL(6,2) NOT NULL,
  is_bullet BOOLEAN DEFAULT false,
  track_condition VARCHAR(20),
  workout_type VARCHAR(20),
  rank_on_day INTEGER,
  total_works_on_day INTEGER,
  exercise_rider VARCHAR(100),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(horse_id, workout_date, track_code, distance_furlongs)
);

-- ═══════════════════════════════════════════
-- TABLE 9: results
-- ═══════════════════════════════════════════

CREATE TABLE results (
  result_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  entry_id UUID NOT NULL REFERENCES entries(entry_id),
  race_id UUID NOT NULL REFERENCES races(race_id),
  horse_id UUID NOT NULL REFERENCES horses(horse_id),
  finish_position INTEGER NOT NULL,
  official_finish INTEGER NOT NULL,
  is_disqualified BOOLEAN DEFAULT false,
  dq_from INTEGER,
  dq_to INTEGER,
  lengths_behind DECIMAL(5,2),
  final_time DECIMAL(6,2),
  beyer_speed_figure INTEGER,
  call_1_position INTEGER,
  call_1_lengths DECIMAL(5,2),
  call_2_position INTEGER,
  call_2_lengths DECIMAL(5,2),
  stretch_position INTEGER,
  stretch_lengths DECIMAL(5,2),
  win_payout DECIMAL(8,2),
  place_payout DECIMAL(8,2),
  show_payout DECIMAL(8,2),
  exacta_payout DECIMAL(10,2),
  trifecta_payout DECIMAL(10,2),
  superfecta_payout DECIMAL(10,2),
  daily_double_payout DECIMAL(10,2),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(entry_id)
);

-- ═══════════════════════════════════════════
-- TABLE 10: predictions
-- ═══════════════════════════════════════════

CREATE TABLE predictions (
  prediction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  entry_id UUID NOT NULL REFERENCES entries(entry_id),
  race_id UUID NOT NULL REFERENCES races(race_id),
  horse_id UUID NOT NULL REFERENCES horses(horse_id),
  model_version_id UUID,
  win_probability DECIMAL(6,4),
  place_probability DECIMAL(6,4),
  show_probability DECIMAL(6,4),
  predicted_rank INTEGER,
  confidence_score DECIMAL(6,4),
  is_top_pick BOOLEAN DEFAULT false,
  is_value_flag BOOLEAN DEFAULT false,
  morning_line_implied_prob DECIMAL(6,4),
  overlay_pct DECIMAL(6,4),
  feature_importance JSONB,
  recommended_bet_type VARCHAR(50),
  exotic_partners UUID[],
  actual_finish INTEGER,
  was_win BOOLEAN,
  was_place BOOLEAN,
  was_show BOOLEAN,
  exacta_hit BOOLEAN,
  trifecta_hit BOOLEAN,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(entry_id)
);

-- ═══════════════════════════════════════════
-- TABLE 11: model_versions
-- ═══════════════════════════════════════════

CREATE TABLE model_versions (
  model_version_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  version_name VARCHAR(50) NOT NULL,
  training_date TIMESTAMPTZ NOT NULL,
  training_data_start DATE NOT NULL,
  training_data_end DATE NOT NULL,
  training_race_count INTEGER,
  exacta_hit_rate DECIMAL(6,4),
  trifecta_hit_rate DECIMAL(6,4),
  top1_accuracy DECIMAL(6,4),
  top3_accuracy DECIMAL(6,4),
  calibration_score DECIMAL(6,4),
  feature_list JSONB,
  hyperparameters JSONB,
  s3_artifact_path VARCHAR(500),
  is_active BOOLEAN DEFAULT false,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════
-- FK CONSTRAINT (added after both tables exist)
-- ═══════════════════════════════════════════

ALTER TABLE predictions
ADD CONSTRAINT fk_model_version
FOREIGN KEY (model_version_id)
REFERENCES model_versions(model_version_id);

-- ═══════════════════════════════════════════
-- INDEXES
-- ═══════════════════════════════════════════

CREATE INDEX idx_races_date
  ON races(race_date);
CREATE INDEX idx_races_track_date
  ON races(track_id, race_date);
CREATE INDEX idx_entries_race
  ON entries(race_id);
CREATE INDEX idx_entries_horse
  ON entries(horse_id);
CREATE INDEX idx_pp_horse
  ON past_performances(horse_id);
CREATE INDEX idx_pp_horse_date
  ON past_performances(horse_id, race_date DESC);
CREATE INDEX idx_pp_track_date
  ON past_performances(track_code, race_date);
CREATE INDEX idx_workouts_horse
  ON workouts(horse_id);
CREATE INDEX idx_workouts_horse_date
  ON workouts(horse_id, workout_date DESC);
CREATE INDEX idx_predictions_race
  ON predictions(race_id);
CREATE INDEX idx_predictions_date
  ON predictions(created_at);
CREATE INDEX idx_results_race
  ON results(race_id);
