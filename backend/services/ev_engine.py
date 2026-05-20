"""
EV computation engine for horse racing exotic bets — T1.1.5.

Expanded bet-type space:
  Single-race:
    win, place, show
    exacta: box (2/3/4/5), key, wheel, part_wheel
    trifecta: box (3/4/5/6), key_2_over_N, part_wheel
    superfecta: box (4/5/6), key
  Multi-race (multi-horse spread):
    daily_double (legs × horses)
    pick3, pick4, pick5 (legs × horses)

Conditional joint probability: Harville.
Known bias: overweights favorites in deep fields. Effect concentrates
in "key" bet types where key horse has elevated win-prob multiplied
through the joint. T1.1 OOS confirmed trifecta_key_1_over_N at -90% ROI.
DISABLED in this engine (recommend() omits from candidate set) pending
PL-inference or empirical-conditional replacement.

Payout substrate (`/tmp/t11_5_payout_lookup.json`):
  - Pick-N: per-dollar normalized (payout ÷ base_unit at row level)
  - All others: raw realized payouts at chart-quoted base unit
  Standardized base units assumed: exa $2, tri $1, sf $0.10, dd $2.
"""
import json
import math
from typing import Dict, List, Optional, Tuple


# Base units for ticket-cost math (real-world tote standards).
BASE_UNIT = {
    'win': 2.0, 'place': 2.0, 'show': 2.0,
    'exacta': 2.0,
    'trifecta': 1.0,
    'superfecta': 0.1,
    'daily_double': 2.0,
    'pick3': 0.5, 'pick4': 0.5, 'pick5': 0.5, 'pick6': 1.0,
    'super_high_five': 1.0,
    'quinella': 2.0,
}


class EVEngine:

    def __init__(self, payout_lookup: dict, payout_estimator: str = 'median',
                 pool_proxy: Optional[dict] = None, pool_quartiles: Optional[dict] = None,
                 conditional: bool = False):
        """
        payout_lookup: T1.1.5 format {bet: {fs: {median, mean, n}}}
            OR T1.4 conditional format {bet: {fs: {pool_bucket: {median, mean, n}}}}
        payout_estimator: 'median' (typical race; production default) or 'mean'.
        pool_proxy: T1.4 — {bet: {track_code: {dow_int|'avg': median_pool}}}
        pool_quartiles: T1.4 — {bet: {q1, q2, q3, n}} bucket thresholds
        conditional: True → use T1.4 pool-conditional lookup with race-context buckets.
        """
        self.lookup = payout_lookup
        self.estimator = payout_estimator
        self.pool_proxy = pool_proxy or {}
        self.pool_quartiles = pool_quartiles or {}
        self.conditional = conditional
        self.race_pool_buckets = {}  # set per-race via set_race_context

    def set_race_context(self, track_code: str, race_date) -> None:
        """T1.4: precompute pool_bucket per bet type for this race using pool_proxy."""
        self.race_pool_buckets = {}
        if not self.conditional:
            return
        # day_of_week: 0=Mon..6=Sun via Python weekday(); convert to Postgres DoW (0=Sun..6=Sat)
        py_wd = race_date.weekday()  # Mon=0..Sun=6
        pg_dow = (py_wd + 1) % 7      # Sun=0..Sat=6 matches DB EXTRACT(DOW)
        for bet, quart in self.pool_quartiles.items():
            track_map = self.pool_proxy.get(bet, {}).get(track_code, {})
            pool_est = track_map.get(pg_dow)
            if pool_est is None:
                pool_est = track_map.get('avg')
            if pool_est is None:
                self.race_pool_buckets[bet] = 'any'
                continue
            if pool_est < quart['q1']: bucket = 'low'
            elif pool_est < quart['q2']: bucket = 'med-low'
            elif pool_est < quart['q3']: bucket = 'med-high'
            else: bucket = 'high'
            self.race_pool_buckets[bet] = bucket

    def expected_payout(self, bet_type: str, field_size: int) -> float:
        """Lookup payout for (bet, fs[, pool_bucket]). For Pick-N this is per-$1 normalized;
        for others, it's the chart-quoted base-unit payout."""
        d = self.lookup.get(bet_type, {})
        fs_key = str(int(field_size))

        # T1.4 conditional path: pool_bucket from race context
        if self.conditional:
            bucket = self.race_pool_buckets.get(bet_type, 'any')
            # Try exact (fs, bucket); fallback to (fs, 'any'); fallback to neighbors
            entry = d.get(fs_key, {}).get(bucket)
            if entry and entry.get('n', 0) >= 5:
                return float(entry[self.estimator])
            entry = d.get(fs_key, {}).get('any')
            if entry and entry.get('n', 0) >= 5:
                return float(entry[self.estimator])
            for delta in [1, -1, 2, -2]:
                alt = str(int(field_size) + delta)
                e2 = d.get(alt, {}).get(bucket) or d.get(alt, {}).get('any')
                if e2 and e2.get('n', 0) >= 5:
                    return float(e2[self.estimator])
            return 0.0

        # T1.1.5 flat path (backward compat)
        if fs_key in d and isinstance(d[fs_key], dict) and 'n' in d[fs_key] and d[fs_key]['n'] >= 5:
            return float(d[fs_key][self.estimator])
        for delta in [1, -1, 2, -2]:
            alt = str(int(field_size) + delta)
            if alt in d and isinstance(d[alt], dict) and 'n' in d[alt] and d[alt]['n'] >= 5:
                return float(d[alt][self.estimator])
        return float(d.get('*', {}).get(self.estimator, 0))

    # ── Harville joint probability helper ──

    @staticmethod
    def harville_joint(probs: List[float], k: int) -> float:
        """P(probs[0] first, probs[1] second, ..., probs[k-1] kth) under Harville:
        p_1 × p_2/(1-p_1) × p_3/(1-p_1-p_2) × ..."""
        p_sum = 0.0
        out = 1.0
        for i, pi in enumerate(probs[:k]):
            if i == 0:
                out *= pi
            else:
                denom = 1.0 - p_sum
                if denom < 1e-9:
                    return 0.0
                out *= pi / denom
            p_sum += pi
        return out

    # ── Single-horse bets ──

    def ev_win(self, win_prob: float, fs: int) -> Tuple[float, float, float]:
        exp = self.expected_payout('win', fs)
        ticket = 2.0
        return win_prob * exp - ticket, win_prob, ticket

    def ev_place(self, place_prob: float, fs: int) -> Tuple[float, float, float]:
        exp = self.expected_payout('place', fs)
        ticket = 2.0
        return place_prob * exp - ticket, place_prob, ticket

    def ev_show(self, show_prob: float, fs: int) -> Tuple[float, float, float]:
        exp = self.expected_payout('show', fs)
        ticket = 2.0
        return show_prob * exp - ticket, show_prob, ticket

    # ── Exacta: box, key, wheel, part-wheel ──

    def ev_exacta_box(self, horses: List[Dict], fs: int) -> Tuple[float, float, float]:
        n = len(horses)
        if n < 2: return -1e9, 0.0, 0.0
        ticket = n * (n - 1) * BASE_UNIT['exacta']
        exp = self.expected_payout('exacta', fs)
        p_hit = 0.0
        for i, hi in enumerate(horses):
            for j, hj in enumerate(horses):
                if i != j:
                    p_hit += self.harville_joint([hi['win_prob'], hj['win_prob']], 2)
        return p_hit * exp - ticket, p_hit, ticket

    def ev_exacta_key(self, key: Dict, partners: List[Dict], fs: int) -> Tuple[float, float, float]:
        """Key in 1st, any partner in 2nd. Unidirectional."""
        n = len(partners)
        if n < 1: return -1e9, 0.0, 0.0
        ticket = n * BASE_UNIT['exacta']
        exp = self.expected_payout('exacta', fs)
        p_hit = sum(self.harville_joint([key['win_prob'], p['win_prob']], 2) for p in partners)
        return p_hit * exp - ticket, p_hit, ticket

    def ev_exacta_wheel(self, key: Dict, others: List[Dict], fs: int) -> Tuple[float, float, float]:
        """Key with ALL others, both directions (key 1st OR 2nd).
        Ticket = 2 × n_others × $2."""
        n = len(others)
        if n < 1: return -1e9, 0.0, 0.0
        ticket = 2 * n * BASE_UNIT['exacta']
        exp = self.expected_payout('exacta', fs)
        # P(key 1st & other 2nd) + P(other 1st & key 2nd)
        p_hit = 0.0
        for o in others:
            p_hit += self.harville_joint([key['win_prob'], o['win_prob']], 2)
            p_hit += self.harville_joint([o['win_prob'], key['win_prob']], 2)
        return p_hit * exp - ticket, p_hit, ticket

    def ev_exacta_part_wheel(self, key: Dict, partners: List[Dict], fs: int) -> Tuple[float, float, float]:
        """Alias for ev_exacta_key — unidirectional key over selected partners."""
        return self.ev_exacta_key(key, partners, fs)

    # ── Trifecta: box, key_2_over_N, part-wheel ──

    def ev_trifecta_box(self, horses: List[Dict], fs: int) -> Tuple[float, float, float]:
        n = len(horses)
        if n < 3: return -1e9, 0.0, 0.0
        ticket = n * (n - 1) * (n - 2) * BASE_UNIT['trifecta']
        exp = self.expected_payout('trifecta', fs)
        p_hit = 0.0
        for i in range(n):
            for j in range(n):
                if j == i: continue
                for k in range(n):
                    if k == i or k == j: continue
                    p_hit += self.harville_joint(
                        [horses[i]['win_prob'], horses[j]['win_prob'], horses[k]['win_prob']], 3
                    )
        return p_hit * exp - ticket, p_hit, ticket

    # trifecta_key_1_over_N — DISABLED per T1.1 OOS findings (-90% ROI Harville bias)

    def ev_trifecta_key_2_over_N(self, two_keys: List[Dict], partners: List[Dict], fs: int) -> Tuple[float, float, float]:
        """Two keys fill 1st-2nd in either order; partners fill 3rd.
        Ticket = 2 × n_partners × $1 (2 orderings of keys × n partner choices)."""
        if len(two_keys) != 2 or len(partners) < 1:
            return -1e9, 0.0, 0.0
        n = len(partners)
        ticket = 2 * n * BASE_UNIT['trifecta']
        exp = self.expected_payout('trifecta', fs)
        p_hit = 0.0
        for a_idx in range(2):
            b_idx = 1 - a_idx
            for p in partners:
                p_hit += self.harville_joint(
                    [two_keys[a_idx]['win_prob'], two_keys[b_idx]['win_prob'], p['win_prob']], 3
                )
        return p_hit * exp - ticket, p_hit, ticket

    def ev_trifecta_part_wheel(self, top_2: List[Dict], partners: List[Dict], fs: int) -> Tuple[float, float, float]:
        """Top-2 fill 1-2 in either order, partners (NOT top-2) fill 3rd.
        Equivalent to trifecta_key_2 over partners excluding top-2."""
        clean_partners = [p for p in partners if p['horse_id'] not in {top_2[0]['horse_id'], top_2[1]['horse_id']}]
        return self.ev_trifecta_key_2_over_N(top_2, clean_partners, fs)

    # ── Superfecta: box, key ──

    def ev_superfecta_box(self, horses: List[Dict], fs: int) -> Tuple[float, float, float]:
        n = len(horses)
        if n < 4: return -1e9, 0.0, 0.0
        n_combos = n * (n - 1) * (n - 2) * (n - 3)
        ticket = n_combos * BASE_UNIT['superfecta']
        exp = self.expected_payout('superfecta', fs)
        p_hit = 0.0
        for a in range(n):
            for b in range(n):
                if b == a: continue
                for c in range(n):
                    if c == a or c == b: continue
                    for d in range(n):
                        if d == a or d == b or d == c: continue
                        p_hit += self.harville_joint(
                            [horses[a]['win_prob'], horses[b]['win_prob'],
                             horses[c]['win_prob'], horses[d]['win_prob']], 4
                        )
        return p_hit * exp - ticket, p_hit, ticket

    def ev_superfecta_key(self, key: Dict, partners: List[Dict], fs: int) -> Tuple[float, float, float]:
        """Key 1st + 3 partners fill 2/3/4 in any order."""
        n = len(partners)
        if n < 3: return -1e9, 0.0, 0.0
        n_combos = n * (n - 1) * (n - 2)
        ticket = n_combos * BASE_UNIT['superfecta']
        exp = self.expected_payout('superfecta', fs)
        p_hit = 0.0
        for i in range(n):
            for j in range(n):
                if j == i: continue
                for k in range(n):
                    if k == i or k == j: continue
                    p_hit += self.harville_joint(
                        [key['win_prob'], partners[i]['win_prob'],
                         partners[j]['win_prob'], partners[k]['win_prob']], 4
                    )
        return p_hit * exp - ticket, p_hit, ticket

    # ── Multi-leg multi-horse ──

    def ev_daily_double_spread(self, leg1_horses: List[Dict], leg2_horses: List[Dict],
                                fs_avg: int) -> Tuple[float, float, float]:
        n1, n2 = len(leg1_horses), len(leg2_horses)
        if n1 < 1 or n2 < 1: return -1e9, 0.0, 0.0
        ticket = n1 * n2 * BASE_UNIT['daily_double']
        exp = self.expected_payout('daily_double', fs_avg)
        p_hit = (sum(h['win_prob'] for h in leg1_horses) *
                 sum(h['win_prob'] for h in leg2_horses))
        return p_hit * exp - ticket, p_hit, ticket

    def ev_pickN_spread(self, leg_horses: List[List[Dict]], n_legs: int,
                        fs_avg: int) -> Tuple[float, float, float]:
        """Multi-horse Pick-N (n_legs ∈ {3,4,5,6}).
        Uses per-dollar payout lookup × base_unit for on-hit reward."""
        if len(leg_horses) != n_legs or any(len(l) < 1 for l in leg_horses):
            return -1e9, 0.0, 0.0
        bet_type = f'pick{n_legs}'
        base = BASE_UNIT[bet_type]
        n_combos = 1
        for legs in leg_horses:
            n_combos *= len(legs)
        ticket = n_combos * base
        per_dollar = self.expected_payout(bet_type, fs_avg)  # already normalized per $1
        on_hit_reward = per_dollar * base
        p_hit = 1.0
        for legs in leg_horses:
            p_hit *= sum(h['win_prob'] for h in legs)
        return p_hit * on_hit_reward - ticket, p_hit, ticket

    # ── Recommendation ──

    def recommend(self, race_predictions: List[Dict], field_size: int,
                  min_ev_threshold: float = 0.0,
                  enable_keys: bool = False) -> List[dict]:
        """Enumerate single-race bet candidates. Returns sorted (highest EV first).

        DISABLED bet types (substrate-grounded; do not enumerate):
          - trifecta_key_1_over_N: -90% ROI in T1.1 OOS (Harville bias overweights favorite
            in 3-deep joint; key horse rarely wins as model predicts)
          - trifecta_key_2_over_N: -40% to -100% ROI in T1.1.5 OOS (two-key version
            dampens but doesn't eliminate Harville bias)
          - exacta_key_1_over_N: -100% in T1.1.5 (1 OOS bet; same Harville root cause; 2-deep
            joint less amplified but still biased)
        Re-enable by passing enable_keys=True or extending engine after PL-inference
        conditional probability replacement."""
        sorted_h = sorted(race_predictions, key=lambda h: h['win_prob'], reverse=True)
        if len(sorted_h) < 3:
            return []
        candidates = []

        # WIN/PLACE/SHOW on top-1
        ev, p, c = self.ev_win(sorted_h[0]['win_prob'], field_size)
        candidates.append({'bet_type': 'win', 'horses': [sorted_h[0]], 'ticket_cost': c, 'p_hit': p, 'ev': ev})
        p_place_top1 = sorted_h[0]['win_prob']
        for j in range(1, len(sorted_h)):
            p_place_top1 += self.harville_joint([sorted_h[j]['win_prob'], sorted_h[0]['win_prob']], 2)
        ev, p, c = self.ev_place(p_place_top1, field_size)
        candidates.append({'bet_type': 'place', 'horses': [sorted_h[0]], 'ticket_cost': c, 'p_hit': p, 'ev': ev})

        # EXACTA — box 2-5, key 1-over-2/3/4, wheel
        for nbox in (2, 3, 4, 5):
            if len(sorted_h) >= nbox:
                ev, p, c = self.ev_exacta_box(sorted_h[:nbox], field_size)
                candidates.append({'bet_type': f'exacta_box_{nbox}', 'horses': sorted_h[:nbox],
                                   'ticket_cost': c, 'p_hit': p, 'ev': ev})
        # exacta_key_1_over_N: DISABLED (Harville bias; -100% in T1.1.5 OOS)
        if enable_keys:
            for n_part in (2, 3, 4):
                if len(sorted_h) >= n_part + 1:
                    ev, p, c = self.ev_exacta_key(sorted_h[0], sorted_h[1:1 + n_part], field_size)
                    candidates.append({'bet_type': f'exacta_key_1_over_{n_part}',
                                       'horses': sorted_h[:1 + n_part],
                                       'ticket_cost': c, 'p_hit': p, 'ev': ev})
        # exacta_wheel: kept (bidirectional; less favorite-overweight than unidirectional key)
        if len(sorted_h) >= 4:
            ev, p, c = self.ev_exacta_wheel(sorted_h[0], sorted_h[1:5], field_size)
            candidates.append({'bet_type': 'exacta_wheel_top1_x_4', 'horses': sorted_h[:5],
                               'ticket_cost': c, 'p_hit': p, 'ev': ev})

        # TRIFECTA — box 3-6, key_2_over_N (1-3), part_wheel
        for nbox in (3, 4, 5, 6):
            if len(sorted_h) >= nbox:
                ev, p, c = self.ev_trifecta_box(sorted_h[:nbox], field_size)
                candidates.append({'bet_type': f'trifecta_box_{nbox}', 'horses': sorted_h[:nbox],
                                   'ticket_cost': c, 'p_hit': p, 'ev': ev})
        # trifecta_key_2_over_N: DISABLED (Harville bias confirmed in T1.1.5 OOS at
        # -40% to -100% ROI). Re-enable via enable_keys=True after conditional prob upgrade.
        if enable_keys:
            for n_part in (1, 2, 3):
                if len(sorted_h) >= 2 + n_part:
                    ev, p, c = self.ev_trifecta_key_2_over_N(sorted_h[:2], sorted_h[2:2 + n_part], field_size)
                    candidates.append({'bet_type': f'trifecta_key_2_over_{n_part}',
                                       'horses': sorted_h[:2 + n_part],
                                       'ticket_cost': c, 'p_hit': p, 'ev': ev})
        # trifecta_key_1_over_N intentionally NOT enumerated (Harville bias; T1.1 OOS)

        # SUPERFECTA — box 4-6, key
        for nbox in (4, 5, 6):
            if len(sorted_h) >= nbox:
                ev, p, c = self.ev_superfecta_box(sorted_h[:nbox], field_size)
                candidates.append({'bet_type': f'superfecta_box_{nbox}', 'horses': sorted_h[:nbox],
                                   'ticket_cost': c, 'p_hit': p, 'ev': ev})
        if len(sorted_h) >= 4:
            ev, p, c = self.ev_superfecta_key(sorted_h[0], sorted_h[1:5], field_size)
            candidates.append({'bet_type': 'superfecta_key_top1_x_3+', 'horses': sorted_h[:5],
                               'ticket_cost': c, 'p_hit': p, 'ev': ev})

        candidates = [c for c in candidates if c['ev'] > min_ev_threshold]
        candidates.sort(key=lambda x: x['ev'], reverse=True)
        return candidates


def load_default_lookup(path: str = '/tmp/t11_5_payout_lookup.json') -> dict:
    with open(path) as f:
        return json.load(f)


if __name__ == '__main__':
    lookup = load_default_lookup()
    ev = EVEngine(lookup, payout_estimator='median')
    fake_preds = [
        {'horse_id': 'a', 'horse_name': 'Top', 'win_prob': 0.30},
        {'horse_id': 'b', 'horse_name': 'Two', 'win_prob': 0.22},
        {'horse_id': 'c', 'horse_name': 'Three', 'win_prob': 0.15},
        {'horse_id': 'd', 'horse_name': 'Four', 'win_prob': 0.10},
        {'horse_id': 'e', 'horse_name': 'Five', 'win_prob': 0.08},
        {'horse_id': 'f', 'horse_name': 'Six', 'win_prob': 0.06},
        {'horse_id': 'g', 'horse_name': 'Seven', 'win_prob': 0.05},
        {'horse_id': 'h', 'horse_name': 'Eight', 'win_prob': 0.04},
    ]
    print("EV engine smoke test (median estimator, fs=8, top1=30%)")
    cands = ev.recommend(fake_preds, field_size=8)
    print(f"  Top 8 candidates:")
    for c in cands[:8]:
        print(f"    {c['bet_type']:<32} ticket=${c['ticket_cost']:>7.2f} "
              f"p_hit={c['p_hit']:.4f} EV=${c['ev']:+8.2f}")

    # Smoke test multi-leg
    print("\n  Multi-leg smoke test (Pick-3 2×2×2 spread, fs_avg=8):")
    leg_horses = [fake_preds[:2], fake_preds[:2], fake_preds[:2]]
    ev3, p3, t3 = ev.ev_pickN_spread(leg_horses, 3, 8)
    print(f"    pick3_spread_2x2x2: ticket=${t3:.2f} p_hit={p3:.4f} EV=${ev3:+.2f}")
    ev4_2222, p4_2222, t4_2222 = ev.ev_pickN_spread([fake_preds[:2]] * 4, 4, 8)
    print(f"    pick4_spread_2x2x2x2: ticket=${t4_2222:.2f} p_hit={p4_2222:.4f} EV=${ev4_2222:+.2f}")
