export interface Prediction {
  prediction_id: string;
  race_id: string;
  horse_id: string;
  horse_name: string;
  post_position: number;
  program_number: string;
  win_probability: number;
  place_probability: number;
  show_probability: number;
  predicted_rank: number;
  confidence_score: number;
  is_top_pick: boolean;
  is_value_flag: boolean;
  overlay_pct: number | null;
  morning_line_odds: number | null;
  recommended_bet_type: string;
  exotic_partners: string[];
  feature_importance: Record<string, number>;
  top_feature: string | null;
  trainer_name: string;
  jockey_name: string | null;
  lasix_first_time: boolean;
  blinkers_first_time: boolean;
  equipment_change: boolean;
  weight_carried: number | null;
  sex: string | null;
  sire: string | null;
  actual_finish: number | null;
  was_win: boolean | null;
  was_place: boolean | null;
  was_show: boolean | null;
  exacta_hit: boolean | null;
  trifecta_hit: boolean | null;
  // Stream A2 dual-prediction
  handicapping_prob?: number | null;
  market_prob?: number | null;
  // Stream E results-aware fields
  actual_finish_position?: number | null;
  actual_win_payout?: number | null;
  actual_place_payout?: number | null;
  actual_show_payout?: number | null;
  prediction_outcome?: PredictionOutcome | null;
  flat_bet_pl?: number | null;
}

export type PredictionOutcome =
  | 'win' | 'place' | 'show' | 'lose' | 'pending' | 'scratched';

// Alias for clarity — WR model uses the base Prediction type
export type WRPrediction = Prediction;

export interface Race {
  race_id: string;
  race_number: number;
  distance_furlongs: number | null;
  surface: string | null;
  race_type: string | null;
  purse: number | null;
  claiming_price: number | null;
  conditions: string | null;
  post_time: string | null;
  field_size: number | null;
  race_name: string | null;
  track_condition: string | null;
  grade: string | null;
  track_code: string;
  track_name: string;
  predictions: Prediction[];
}

export interface Track {
  track_code: string;
  track_name: string;
  race_count: number;
}

export interface RacesResponse {
  date: string;
  race_count: number;
  races: Race[];
  tracks: Track[];
}

export interface ValuePlaysResponse {
  date: string;
  count: number;
  value_plays: Prediction[];
}

export interface AvailableDate {
  date: string;
  race_count: number;
  track_count: number;
  has_predictions: boolean;
}

export interface PastPerformance {
  race_date: string;
  track_code: string;
  race_number: number;
  distance_furlongs: number | null;
  surface: string | null;
  race_type: string | null;
  purse: number | null;
  field_size: number | null;
  track_condition: string | null;
  post_position: number | null;
  finish_position: number | null;
  official_finish: number | null;
  lengths_behind: number | null;
  beyer_speed_figure: number | null;
  final_time: number | null;
  closing_odds: number | null;
  jockey_name: string | null;
  trainer_name: string | null;
  weight_carried: number | null;
  comment: string | null;
  running_style: string | null;
  days_since_last_race: number | null;
  call_1_lengths: number | null;
  call_2_lengths: number | null;
  call_3_position: number | null;
  stretch_position: number | null;
  stretch_lengths: number | null;
  fraction_1: number | null;
  fraction_2: number | null;
  fraction_3: number | null;
  lasix: boolean;
  lasix_first_time: boolean;
  blinkers_on: boolean;
  model_rank: number | null;
}

export interface HorsePPsResponse {
  horse_id: string;
  horse_name: string | null;
  sire: string | null;
  dam: string | null;
  dam_sire: string | null;
  sex: string | null;
  country: string | null;
  best_speed_figure: number | null;
  speed_figures: number[];
  past_performances: PastPerformance[];
}

export interface DashboardMetrics {
  active_model: {
    model_version_id: string;
    version_name: string;
    training_date: string;
    training_race_count: number;
    exacta_hit_rate: number | null;
    trifecta_hit_rate: number | null;
    top1_accuracy: number | null;
    top3_accuracy: number | null;
    calibration_score: number | null;
    notes: string | null;
  } | null;
  model_history: {
    model_version_id: string;
    version_name: string;
    training_date: string;
    exacta_hit_rate: number | null;
    trifecta_hit_rate: number | null;
    top1_accuracy: number | null;
    is_active: boolean;
  }[];
  counts: {
    races: number;
    horses: number;
    entries: number;
    results: number;
    predictions: number;
    earliest_date: string;
    latest_date: string;
  };
  prediction_dates: { date: string; count: number }[];
}

// ── P&L Prediction ──
export interface PLPrediction {
  prediction_id: string;
  race_id: string;
  horse_id: string;
  horse_name: string;
  post_position: number;
  program_number: string;
  win_probability: number | null;
  predicted_ev: number | null;
  predicted_rank: number;
  confidence_score: number | null;
  is_top_pick: boolean;
  closing_odds: number | null;
  morning_line_odds: number | null;
  implied_probability: number | null;
  edge_pct: number | null;
  is_value_bet: boolean;
  is_strong_value: boolean;
  kelly_fraction: number | null;
  kelly_bet_size: number | null;
  feature_importance: Record<string, number>;
  trainer_name: string;
  jockey_name: string | null;
  lasix_first_time: boolean;
  blinkers_first_time: boolean;
  equipment_change: boolean | null;
  actual_finish: number | null;
  was_win: boolean | null;
  bet_profit: number | null;
  // Stream A2 dual-prediction
  handicapping_prob?: number | null;
  market_prob?: number | null;
  // Stream E results-aware fields
  actual_finish_position?: number | null;
  actual_win_payout?: number | null;
  actual_place_payout?: number | null;
  actual_show_payout?: number | null;
  prediction_outcome?: PredictionOutcome | null;
  flat_bet_pl?: number | null;
}

export interface PLValueBetsResponse {
  model: string;
  date: string;
  count: number;
  value_bets: PLPrediction[];
}

// ── LS Prediction ──
export interface LSPrediction {
  prediction_id: string;
  race_id: string;
  horse_id: string;
  horse_name: string;
  post_position: number;
  program_number: string;
  final_win_probability: number | null;
  longshot_alert: boolean;
  confidence: string | null;
  kelly_fraction: number | null;
  predicted_rank: number | null;
  xgb_rank_score: number | null;
  rf_longshot_prob: number | null;
  lstm_trajectory: number | null;
  calibrated_win_prob: number | null;
  bayesian_angle_ev: number | null;
  angle_description: string | null;
  feature_importance: Record<string, number>;
  trainer_name: string;
  jockey_name: string | null;
  morning_line_odds: number | null;
  actual_finish: number | null;
  was_win: boolean | null;
  actual_odds: number | null;
  bet_profit: number | null;
  // Race context (Bug 3)
  race_date: string | null;
  race_number: number | null;
  track_code: string | null;
  post_time: string | null;
  // Stream E results-aware fields
  actual_finish_position?: number | null;
  actual_win_payout?: number | null;
  actual_place_payout?: number | null;
  actual_show_payout?: number | null;
  prediction_outcome?: PredictionOutcome | null;
  flat_bet_pl?: number | null;
}

export interface LSAlertsResponse {
  model: string;
  date: string;
  count: number;
  longshot_alerts: LSPrediction[];
}

// Stream E4 — track-record aggregate banner shape (from /{model}/predictions/track-record).
export interface TrackRecord {
  window_days: number;
  n_predictions: number;
  n_settled: number;
  n_pending: number;
  wins: number;
  places: number;
  shows: number;
  hit_rate_win: number;
  hit_rate_place: number;
  hit_rate_show: number;
  flat_bet_pl_total: number;
  flat_bet_roi_pct: number;
  data_completeness: number | null;
  winners_data_completeness: number | null;
  best_day?: { date: string; wins: number; pl: number } | null;
  worst_day?: { date: string; wins: number; pl: number } | null;
  by_track?: Array<{ track_code: string; n: number; wins: number; hit_rate: number; roi: number }>;
}

// /wr/predictions/track-record-by-style — same shape + per-style breakdown.
export interface TrackRecordByStyle extends TrackRecord {
  by_style: Array<{
    style: string;
    n: number;
    n_settled: number;
    wins: number;
    places: number;
    hit_rate_win: number | null;
    hit_rate_place: number | null;
    roi: number | null;
    data_completeness: number | null;
    winners_data_completeness: number | null;
  }>;
}
