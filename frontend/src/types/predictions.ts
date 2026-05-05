// Specialist gallery types — used by the Compare view.

import { PredictionOutcome } from './index';

export type SpecialistStyle =
  | 'speed' | 'closer' | 'class_riser'
  | 'class_dropper' | 'sprint' | 'route'
  | 'gonzo_sauce';  // Phase A3 — lean53 + 14 features, distinct ranker + classifier

export const SPECIALIST_STYLES: SpecialistStyle[] = [
  'speed', 'closer', 'class_riser',
  'class_dropper', 'sprint', 'route',
  'gonzo_sauce',
];

export const STYLE_LABELS: Record<SpecialistStyle, string> = {
  speed: 'Speed',
  closer: 'Closer',
  class_riser: 'Class Riser',
  class_dropper: 'Class Dropper',
  sprint: 'Sprint',
  route: 'Route',
  gonzo_sauce: 'Gonzo Sauce',
};

export interface CompareWRBlock {
  predicted_rank: number | null;
  win_probability: number | null;
  edge_pct: number | null;
  kelly_fraction: number | null;
  is_top_pick: boolean;
  is_value_flag: boolean;
}

export interface ComparePLBlock {
  win_probability: number | null;
  edge_pct: number | null;
  kelly_fraction: number | null;
  is_value_bet: boolean;
}

export interface CompareSidePair {
  wr: CompareWRBlock;
  pl: ComparePLBlock;
}

export interface CompareHorse {
  entry_id: string;
  horse_id: string;
  horse_name: string | null;
  program_number: string | null;
  morning_line_odds: number | null;
  prediction_outcome?: PredictionOutcome | null;
  flat_bet_pl?: number | null;
  actual_finish_position?: number | null;
  general: CompareSidePair;
  specialist: CompareSidePair;
}

export interface CompareRace {
  race_id: string;
  race_number: number;
  race_name: string | null;
  post_time: string | null;
  purse: number | null;
  track_code: string | null;
  horses: CompareHorse[];
}

export interface CompareResponse {
  date: string;
  compare_style: SpecialistStyle;
  races: CompareRace[];
}
