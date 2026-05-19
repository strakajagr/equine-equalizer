"""
Strategy harness — applies named strategy logic to per-race predictions.

Phase B design: every strategy is a candidate. No canonical "production" strategy.
Tony reads consolidated daily report; Tony decides; Tony bets.

Architecture:
  - StrategyBase = ABC. Concrete strategies subclass and implement recommend().
  - RacePredictions = uniform per-race input shape (all layers normalized).
  - BetRecommendation = uniform per-bet output shape.
  - Harness consumes existing prediction tables (wr_predictions, pl_predictions,
    ls_predictions). Production inference pipeline untouched.

Extension pattern:
  1. Subclass StrategyBase in strategy_registry.py
  2. Append instance to STRATEGIES list
  3. Strategy auto-appears in next day's report; auto-tracks historical P&L.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional, Any


@dataclass
class HorsePrediction:
    """Per-horse prediction with all layer outputs normalized."""
    horse_id: str
    horse_name: str
    program_number: Optional[str] = None
    morning_line_odds: Optional[float] = None
    # Layer outputs (any may be None if layer didn't run for this race/style)
    win_probability: Optional[float] = None       # wr_predictions / canonical wp
    place_probability: Optional[float] = None
    show_probability: Optional[float] = None
    ensemble_win_prob: Optional[float] = None
    handicapping_prob: Optional[float] = None     # market-blind model output
    market_prob: Optional[float] = None
    rank_score: Optional[float] = None            # ranker output
    pl_win_probability: Optional[float] = None    # pl_predictions
    pl_predicted_ev: Optional[float] = None
    pl_edge_pct: Optional[float] = None
    longshot_prob: Optional[float] = None
    longshot_alert: bool = False
    trajectory_score: Optional[float] = None
    hybrid_c_win_prob: Optional[float] = None    # Hybrid C culled-rebuilt ensemble output
    angle_name: Optional[str] = None
    angle_posterior: Optional[float] = None
    angle_ev: Optional[float] = None
    style: Optional[str] = None                   # which specialist style (general/speed/closer/...)
    # Production-strategy outputs (read-only context)
    recommended_bet_type: Optional[str] = None
    is_top_pick: bool = False
    is_value_flag: bool = False
    overlay_pct: Optional[float] = None
    kelly_fraction: Optional[float] = None


@dataclass
class RacePredictions:
    """All predictions for a single race, normalized."""
    race_id: str
    track_code: str
    race_date: date
    race_number: int
    field_size: int
    distance_furlongs: Optional[float] = None
    surface: Optional[str] = None
    race_type: Optional[str] = None
    purse: Optional[int] = None
    post_time: Optional[Any] = None
    horses: List[HorsePrediction] = field(default_factory=list)

    def top_n_by(self, attr: str, n: int = 5,
                 reverse: bool = True) -> List[HorsePrediction]:
        """Return top-N horses by the given attribute. Skips horses with None."""
        with_val = [h for h in self.horses if getattr(h, attr, None) is not None]
        return sorted(with_val, key=lambda h: getattr(h, attr), reverse=reverse)[:n]


@dataclass
class RaceContext:
    """Per-race context for strategy use beyond predictions."""
    race_id: str
    track_code: str
    race_date: date
    race_number: int
    field_size: int
    distance_furlongs: Optional[float] = None
    surface: Optional[str] = None
    race_type: Optional[str] = None
    day_of_week: Optional[int] = None  # Python weekday 0=Mon..6=Sun


@dataclass
class BetRecommendation:
    """Output from a strategy's recommend() or recommend_multi_race()."""
    strategy_name: str
    race_id: str
    bet_type: str                                    # 'win', 'exacta_box_3', 'pick3_2x2x2', etc.
    horses: List[str]                                # horse names (for single-race bets)
    legs: Optional[List[List[str]]] = None           # for multi-leg: horses per leg
    leg_race_ids: Optional[List[str]] = None         # race_ids per leg in order
    stake: float = 0.0                               # ticket cost in dollars
    confidence: Optional[float] = None               # strategy's confidence/EV signal
    rationale: str = ""                              # one-line "why this strategy chose this"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_skip(self) -> bool:
        return self.bet_type == 'skip' or self.stake == 0.0


# ── ABC ──

# Map (ranking_layer, default_field) → actual HorsePrediction attribute name.
RANKING_LAYER_FIELDS = {
    'ensemble': 'ensemble_win_prob',
    'ensemble_hybrid_option_c': 'hybrid_c_win_prob',
    'wr': 'win_probability',
    'pl': 'pl_win_probability',
    'ranker': 'rank_score',
    'longshot': 'longshot_prob',
    'trajectory': 'trajectory_score',
    'angle': 'angle_posterior',
    'handicapping': 'handicapping_prob',
}


class StrategyBase(ABC):
    """All strategies subclass this. Override the abstract properties + recommend(s).

    Class attributes (override at class level per strategy):
      - is_multi_leg: bool — False for single-race; True for DD/Pick-N
      - style: str — wr_predictions.style to load ('general' default; 'gonzo_sauce', 'speed', etc.)
      - ranking_layer: str — which layer's prob ranks horses ('ensemble' default;
                              'wr', 'pl', 'ranker', 'longshot', 'trajectory', 'angle', 'handicapping')
      - ranking_field: Optional[str] — explicit field override; if None, derived from ranking_layer

    Default impls:
      - recommend / recommend_multi_race return None / []; override for active strategies.
      - Errors during recommend() are caught at the harness layer.
    """
    is_multi_leg: bool = False
    style: str = 'general'
    ranking_layer: str = 'ensemble'
    ranking_field: Optional[str] = None  # None → use RANKING_LAYER_FIELDS[ranking_layer]

    @classmethod
    def get_ranking_field(cls) -> str:
        return cls.ranking_field or RANKING_LAYER_FIELDS[cls.ranking_layer]

    def top_n(self, rp: RacePredictions, n: int = 5) -> List[HorsePrediction]:
        """Convenience: top-N horses per this strategy's ranking layer."""
        return rp.top_n_by(self.get_ranking_field(), n=n)

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique string identifier. Used as DB key in strategy_recommendations.
        Convention: snake_case; include version if breaking-change is needed
        (e.g., 't1_1_6_ev_median', 't1_1_6_ev_median_v2')."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Short description shown in reports."""
        ...

    @property
    def category(self) -> str:
        """Optional grouping in report UI: 'ev', 'raw_layer', 'multi_leg', 'angle', 'bayesian'."""
        return 'other'

    def recommend(
        self, race_preds: RacePredictions, ctx: RaceContext
    ) -> Optional[BetRecommendation]:
        """Single-race recommendation. Default = skip (override for active strategies)."""
        return None

    def recommend_multi_race(
        self, card_preds: List[RacePredictions], card_ctx: List[RaceContext]
    ) -> List[BetRecommendation]:
        """Multi-leg recommendations across consecutive races on a card.
        Default = []. Override for DD/Pick-N strategies."""
        return []


# ── Harness execution ──

class StrategyHarness:
    """Runs all strategies in registry against per-race predictions.

    Error isolation: a strategy throwing an exception on one race does NOT
    break the report. Exception is logged + recommendation recorded as
    skip-with-error.
    """

    def __init__(self, strategies: List[StrategyBase]):
        self.strategies = strategies
        self._errors: List[Dict] = []  # per-strategy/per-race exceptions

    def run_race(
        self, race_preds: RacePredictions, ctx: RaceContext,
        only_strategies: Optional[List[str]] = None,
    ) -> Dict[str, Optional[BetRecommendation]]:
        """Apply every (single-race) strategy to one race.
        Returns dict {strategy_name: recommendation_or_None}."""
        out = {}
        for s in self.strategies:
            if s.is_multi_leg:
                continue
            if only_strategies and s.name not in only_strategies:
                continue
            try:
                rec = s.recommend(race_preds, ctx)
            except Exception as e:
                self._errors.append({
                    'strategy': s.name, 'race_id': race_preds.race_id,
                    'error_type': type(e).__name__, 'message': str(e),
                })
                rec = None
            out[s.name] = rec
        return out

    def run_card(
        self, card_preds: List[RacePredictions], card_ctx: List[RaceContext],
        only_strategies: Optional[List[str]] = None,
    ) -> Dict[str, List[BetRecommendation]]:
        """Apply every multi-leg strategy to a consecutive-race card.
        Returns dict {strategy_name: list_of_multi_leg_recommendations}."""
        out = {}
        for s in self.strategies:
            if not s.is_multi_leg:
                continue
            if only_strategies and s.name not in only_strategies:
                continue
            try:
                recs = s.recommend_multi_race(card_preds, card_ctx)
            except Exception as e:
                self._errors.append({
                    'strategy': s.name, 'card_first_race': card_preds[0].race_id if card_preds else None,
                    'error_type': type(e).__name__, 'message': str(e),
                })
                recs = []
            out[s.name] = recs
        return out

    @property
    def errors(self) -> List[Dict]:
        return list(self._errors)


# ── Substrate loaders (separate concern, no SQL inline in strategies) ──

class RacePredictionLoader:
    """Caches RacePredictions per (race_id, style) so multiple strategies
    requesting the same style on the same race issue one DB read."""

    def __init__(self, conn):
        self.conn = conn
        self._cache: Dict[tuple, Optional[RacePredictions]] = {}

    def load(self, race_id: str, style: str = 'general') -> Optional[RacePredictions]:
        key = (race_id, style)
        if key in self._cache:
            return self._cache[key]
        rp = load_race_predictions(self.conn, race_id, style)
        self._cache[key] = rp
        return rp

    def clear(self) -> None:
        self._cache.clear()


def load_race_predictions(
    conn, race_id: str, style: str = 'general'
) -> Optional[RacePredictions]:
    """Pull all layer predictions for a race from the existing tables.

    Strategy-agnostic loader: produces a uniform RacePredictions object;
    strategies don't touch SQL directly. Default style='general' (canonical
    ensemble path); strategies needing other styles override via separate
    loader calls.
    """
    # Pull race + track metadata
    rows = conn.cursor()
    rows.execute("""
        SELECT r.race_id, r.race_date, r.race_number, r.field_size,
               r.distance_furlongs, r.surface, r.race_type, r.purse,
               t.track_code
        FROM races r JOIN tracks t USING (track_id)
        WHERE r.race_id = %s
    """, (race_id,))
    rrow = rows.fetchone()
    if not rrow:
        return None
    rp = RacePredictions(
        race_id=str(rrow['race_id']), track_code=rrow['track_code'],
        race_date=rrow['race_date'], race_number=rrow['race_number'],
        field_size=rrow['field_size'] or 0,
        distance_furlongs=float(rrow['distance_furlongs']) if rrow['distance_furlongs'] else None,
        surface=rrow['surface'], race_type=rrow['race_type'],
        purse=int(rrow['purse']) if rrow['purse'] else None,
    )
    # Pull entries + wr_predictions joined
    rows.execute("""
        SELECT e.entry_id, e.horse_id, h.horse_name, e.program_number, e.morning_line_odds,
               wp.win_probability, wp.place_probability, wp.show_probability,
               wp.ensemble_win_prob, wp.handicapping_prob, wp.market_prob, wp.rank_score,
               wp.longshot_prob, wp.longshot_alert, wp.trajectory_score,
               wp.angle_name, wp.angle_posterior, wp.angle_ev,
               wp.recommended_bet_type, wp.is_top_pick, wp.is_value_flag,
               wp.overlay_pct, wp.kelly_fraction, wp.style
        FROM entries e
        JOIN horses h ON e.horse_id = h.horse_id
        LEFT JOIN wr_predictions wp ON wp.entry_id = e.entry_id AND wp.style = %s
        WHERE e.race_id = %s AND e.is_scratched = false
        ORDER BY e.post_position
    """, (style, race_id))
    for er in rows.fetchall():
        rp.horses.append(HorsePrediction(
            horse_id=str(er['horse_id']),
            horse_name=er['horse_name'],
            program_number=er.get('program_number'),
            morning_line_odds=float(er['morning_line_odds']) if er.get('morning_line_odds') else None,
            win_probability=float(er['win_probability']) if er.get('win_probability') is not None else None,
            place_probability=float(er['place_probability']) if er.get('place_probability') is not None else None,
            show_probability=float(er['show_probability']) if er.get('show_probability') is not None else None,
            ensemble_win_prob=float(er['ensemble_win_prob']) if er.get('ensemble_win_prob') is not None else None,
            handicapping_prob=float(er['handicapping_prob']) if er.get('handicapping_prob') is not None else None,
            market_prob=float(er['market_prob']) if er.get('market_prob') is not None else None,
            rank_score=float(er['rank_score']) if er.get('rank_score') is not None else None,
            longshot_prob=float(er['longshot_prob']) if er.get('longshot_prob') is not None else None,
            longshot_alert=bool(er.get('longshot_alert') or False),
            trajectory_score=float(er['trajectory_score']) if er.get('trajectory_score') is not None else None,
            angle_name=er.get('angle_name'),
            angle_posterior=float(er['angle_posterior']) if er.get('angle_posterior') is not None else None,
            angle_ev=float(er['angle_ev']) if er.get('angle_ev') is not None else None,
            recommended_bet_type=er.get('recommended_bet_type'),
            is_top_pick=bool(er.get('is_top_pick') or False),
            is_value_flag=bool(er.get('is_value_flag') or False),
            overlay_pct=float(er['overlay_pct']) if er.get('overlay_pct') is not None else None,
            kelly_fraction=float(er['kelly_fraction']) if er.get('kelly_fraction') is not None else None,
            style=er.get('style'),
        ))
    # PL outputs (separate table; merge into horses by horse_id)
    rows.execute("""
        SELECT pl.horse_id, pl.win_probability, pl.predicted_ev, pl.edge_pct
        FROM pl_predictions pl
        WHERE pl.race_id = %s
    """, (race_id,))
    pl_map = {str(r['horse_id']): r for r in rows.fetchall()}
    for hp in rp.horses:
        if hp.horse_id in pl_map:
            p = pl_map[hp.horse_id]
            hp.pl_win_probability = float(p['win_probability']) if p['win_probability'] is not None else None
            hp.pl_predicted_ev = float(p['predicted_ev']) if p['predicted_ev'] is not None else None
            hp.pl_edge_pct = float(p['edge_pct']) if p['edge_pct'] is not None else None
    # Hybrid C ensemble predictions (separate table; merge by horse_id)
    rows.execute("""
        SELECT horse_id, hybrid_c_win_probability
        FROM hybrid_c_predictions
        WHERE race_id = %s AND ensemble_version = 'option_c_hybrid_ensemble_20260515'
    """, (race_id,))
    hc_map = {str(r['horse_id']): float(r['hybrid_c_win_probability']) for r in rows.fetchall()}
    for hp in rp.horses:
        if hp.horse_id in hc_map:
            hp.hybrid_c_win_prob = hc_map[hp.horse_id]
    rows.close()
    return rp


def race_context_from_predictions(rp: RacePredictions) -> RaceContext:
    return RaceContext(
        race_id=rp.race_id, track_code=rp.track_code, race_date=rp.race_date,
        race_number=rp.race_number, field_size=rp.field_size,
        distance_furlongs=rp.distance_furlongs, surface=rp.surface,
        race_type=rp.race_type, day_of_week=rp.race_date.weekday(),
    )
