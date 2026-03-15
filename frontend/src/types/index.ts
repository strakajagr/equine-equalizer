export interface Prediction {
  prediction_id: string;
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
  trainer_name: string;
  jockey_name: string | null;
  lasix_first_time: boolean;
  blinkers_first_time: boolean;
  equipment_change: boolean;
}

export interface Race {
  race_id: string;
  predictions: Prediction[];
}

export interface TodayResponse {
  date: string;
  race_count: number;
  races: Race[];
}

export interface ValuePlaysResponse {
  date: string;
  count: number;
  value_plays: Prediction[];
}
