"""
EV-maximized exotic betting strategy — T1.1.5.

Per-race recommendation across expanded bet-type space.
Multi-race recommender enumerates DD / Pick-3 / Pick-4 / Pick-5 spread
combinations over consecutive races.
"""
from typing import List, Dict, Optional, Tuple
from services.ev_engine import EVEngine, BASE_UNIT


# Multi-leg spreads to enumerate per N legs. Tuples = (horses_per_leg, ...).
MULTI_LEG_SPREADS = {
    2: [(1, 1), (2, 1), (1, 2), (2, 2)],
    3: [(1, 1, 1), (2, 1, 1), (1, 2, 1), (1, 1, 2),
        (2, 2, 1), (2, 1, 2), (1, 2, 2), (2, 2, 2),
        (3, 2, 2), (2, 3, 2), (2, 2, 3), (3, 3, 3)],
    # Pick-4 spreads capped at 2-wide max per leg.
    # T1.1.5 OOS showed 3-wide spreads structurally negative-EV:
    #   pick4_3x3x3x3: -25% ROI, ticket $40.50
    #   pick4_3x3x3x2: -100% ROI, ticket $31.50
    #   pick4_3x2x2x2: -100% ROI, ticket $24
    # Probability density doesn't compensate for ticket-cost growth on wide spreads.
    4: [(1, 1, 1, 1),
        (2, 1, 1, 1), (1, 2, 1, 1), (1, 1, 2, 1), (1, 1, 1, 2),
        (2, 2, 1, 1), (2, 1, 2, 1), (2, 1, 1, 2),
        (1, 2, 2, 1), (1, 2, 1, 2), (1, 1, 2, 2),
        (2, 2, 2, 1), (2, 2, 1, 2), (2, 1, 2, 2), (1, 2, 2, 2),
        (2, 2, 2, 2)],
    5: [(1, 1, 1, 1, 1),
        (2, 1, 1, 1, 1), (1, 2, 1, 1, 1), (1, 1, 2, 1, 1), (1, 1, 1, 2, 1), (1, 1, 1, 1, 2),
        (2, 2, 1, 1, 1), (2, 2, 2, 1, 1), (2, 2, 2, 2, 1), (2, 2, 2, 2, 2),
        (3, 2, 2, 2, 2), (3, 3, 2, 2, 2), (3, 3, 3, 3, 3)],
}


class EVStrategy:
    """Multi-bet recommendation engine."""

    def __init__(self, ev_engine: EVEngine, min_ev_threshold: float = 0.0,
                 max_ticket_cost: float = 60.0):
        self.engine = ev_engine
        self.min_ev = min_ev_threshold
        self.max_ticket = max_ticket_cost

    def recommend_bet(self, race_predictions: List[Dict], field_size: int) -> dict:
        """Single-race highest-EV bet recommendation."""
        candidates = self.engine.recommend(
            race_predictions, field_size, min_ev_threshold=self.min_ev
        )
        candidates = [c for c in candidates if c['ticket_cost'] <= self.max_ticket]
        if not candidates:
            return {'bet_type': 'skip', 'horses': [], 'ticket_cost': 0.0,
                    'p_hit': 0.0, 'expected_ev': 0.0}
        best = candidates[0]
        return {'bet_type': best['bet_type'], 'horses': best['horses'],
                'ticket_cost': best['ticket_cost'], 'p_hit': best['p_hit'],
                'expected_ev': best['ev']}

    def recommend_multi_race(self, races_predictions: List[List[Dict]],
                              field_sizes: List[int]) -> List[dict]:
        """Enumerate DD / Pick-3 / Pick-4 / Pick-5 spread bets across consecutive races.

        races_predictions[i] = sorted list of {horse_id, horse_name, win_prob} for race i.
        field_sizes[i] = field_size for race i.

        Returns one recommendation per (multi_leg_type, race_start_index) that has positive EV
        (or skip if no spread is positive-EV)."""
        recommendations = []
        n_races = len(races_predictions)

        # For each window length 2..5
        for n_legs in (2, 3, 4, 5):
            if n_races < n_legs: continue
            for start in range(n_races - n_legs + 1):
                window_preds = races_predictions[start:start + n_legs]
                window_fs = field_sizes[start:start + n_legs]
                fs_avg = int(sum(window_fs) / len(window_fs))

                best_spread = None
                best_ev = -1e9
                for spread in MULTI_LEG_SPREADS[n_legs]:
                    leg_horses = []
                    for i, n_horses in enumerate(spread):
                        if len(window_preds[i]) < n_horses:
                            leg_horses = None; break
                        # Take top-n_horses by win_prob from each leg
                        s = sorted(window_preds[i], key=lambda h: h['win_prob'], reverse=True)
                        leg_horses.append(s[:n_horses])
                    if leg_horses is None: continue

                    if n_legs == 2:
                        ev, p, ticket = self.engine.ev_daily_double_spread(
                            leg_horses[0], leg_horses[1], fs_avg
                        )
                    else:
                        ev, p, ticket = self.engine.ev_pickN_spread(leg_horses, n_legs, fs_avg)

                    if ticket > self.max_ticket: continue
                    if ev > best_ev:
                        best_ev = ev
                        best_spread = {
                            'bet_type': f"{'dd' if n_legs == 2 else f'pick{n_legs}'}_{'x'.join(str(s) for s in spread)}",
                            'n_legs': n_legs,
                            'spread': spread,
                            'leg_horses': leg_horses,
                            'race_start_index': start,
                            'ticket_cost': ticket,
                            'p_hit': p,
                            'expected_ev': ev,
                        }

                if best_spread and best_ev > self.min_ev:
                    recommendations.append(best_spread)

        return recommendations
