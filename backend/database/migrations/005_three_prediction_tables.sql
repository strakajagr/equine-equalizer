-- Migration 005: Three prediction tables + model_versions update
-- 2026-03-18

-- WR Predictions
CREATE TABLE IF NOT EXISTS wr_predictions (
    prediction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entry_id UUID NOT NULL REFERENCES entries(entry_id),
    race_id UUID NOT NULL REFERENCES races(race_id),
    horse_id UUID NOT NULL REFERENCES horses(horse_id),
    model_version_id UUID REFERENCES model_versions(model_version_id),
    win_probability DECIMAL(6,4),
    place_probability DECIMAL(6,4),
    show_probability DECIMAL(6,4),
    predicted_rank INTEGER,
    confidence_score DECIMAL(8,4),
    is_top_pick BOOLEAN DEFAULT FALSE,
    morning_line_implied_prob DECIMAL(6,4),
    overlay_pct DECIMAL(6,4),
    is_value_flag BOOLEAN DEFAULT FALSE,
    recommended_bet_type VARCHAR(20),
    exotic_partners UUID[] DEFAULT '{}',
    feature_importance JSONB DEFAULT '{}',
    actual_finish INTEGER,
    was_win BOOLEAN,
    was_place BOOLEAN,
    was_show BOOLEAN,
    exacta_hit BOOLEAN,
    trifecta_hit BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(entry_id)
);

-- P&L Predictions
CREATE TABLE IF NOT EXISTS pl_predictions (
    prediction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entry_id UUID NOT NULL REFERENCES entries(entry_id),
    race_id UUID NOT NULL REFERENCES races(race_id),
    horse_id UUID NOT NULL REFERENCES horses(horse_id),
    model_version_id UUID REFERENCES model_versions(model_version_id),
    win_probability DECIMAL(6,4),
    predicted_ev DECIMAL(8,4),
    confidence_score DECIMAL(8,4),
    predicted_rank INTEGER,
    is_top_pick BOOLEAN DEFAULT FALSE,
    closing_odds DECIMAL(8,2),
    implied_probability DECIMAL(6,4),
    edge_pct DECIMAL(6,4),
    is_value_bet BOOLEAN DEFAULT FALSE,
    is_strong_value BOOLEAN DEFAULT FALSE,
    kelly_fraction DECIMAL(6,4),
    kelly_bet_size DECIMAL(8,2),
    feature_importance JSONB DEFAULT '{}',
    actual_finish INTEGER,
    was_win BOOLEAN,
    bet_profit DECIMAL(8,2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(entry_id)
);

-- LS Predictions (stub)
CREATE TABLE IF NOT EXISTS ls_predictions (
    prediction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entry_id UUID NOT NULL REFERENCES entries(entry_id),
    race_id UUID NOT NULL REFERENCES races(race_id),
    horse_id UUID NOT NULL REFERENCES horses(horse_id),
    model_version_id UUID REFERENCES model_versions(model_version_id),
    final_win_probability DECIMAL(6,4),
    longshot_alert BOOLEAN DEFAULT FALSE,
    confidence VARCHAR(10),
    kelly_fraction DECIMAL(6,4),
    predicted_rank INTEGER,
    xgb_rank_score DECIMAL(8,4),
    rf_longshot_prob DECIMAL(6,4),
    lstm_trajectory DECIMAL(6,4),
    calibrated_win_prob DECIMAL(6,4),
    bayesian_angle_ev DECIMAL(8,4),
    angle_description TEXT,
    feature_importance JSONB DEFAULT '{}',
    actual_finish INTEGER,
    was_win BOOLEAN,
    actual_odds DECIMAL(8,2),
    bet_profit DECIMAL(8,2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(entry_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_wr_predictions_race ON wr_predictions(race_id, predicted_rank);
CREATE INDEX IF NOT EXISTS idx_wr_predictions_date ON wr_predictions(created_at);
CREATE INDEX IF NOT EXISTS idx_pl_predictions_race ON pl_predictions(race_id, predicted_rank);
CREATE INDEX IF NOT EXISTS idx_pl_predictions_value ON pl_predictions(race_id) WHERE is_value_bet = true;
CREATE INDEX IF NOT EXISTS idx_ls_predictions_race ON ls_predictions(race_id, predicted_rank);
CREATE INDEX IF NOT EXISTS idx_ls_predictions_alert ON ls_predictions(race_id) WHERE longshot_alert = true;

-- Update model_versions: add model_type column
ALTER TABLE model_versions
ADD COLUMN IF NOT EXISTS model_type VARCHAR(10) DEFAULT 'wr'
    CHECK (model_type IN ('wr', 'pl', 'ls'));

-- P&L-specific evaluation columns
ALTER TABLE model_versions
ADD COLUMN IF NOT EXISTS flat_bet_roi DECIMAL(8,4),
ADD COLUMN IF NOT EXISTS kelly_roi DECIMAL(8,4),
ADD COLUMN IF NOT EXISTS value_bet_win_rate DECIMAL(6,4);

-- Allow one active model PER TYPE (not one globally)
DROP INDEX IF EXISTS idx_active_model;
CREATE UNIQUE INDEX IF NOT EXISTS idx_active_model_per_type
ON model_versions (model_type) WHERE is_active = true;
