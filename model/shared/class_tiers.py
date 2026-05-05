"""
Class-tier ranking for race-classification handicapping.

11-tier ordinal scale derived from race_type + claiming_price + purse,
since the schema lacks a populated `grade` column. G1/G2/G3 split is
purse-inferred (approximate but acceptable for V1 — revisit if/when
grade column is populated).

Used by:
- model/shared/specialists.py for class_riser / class_dropper sample weights
- (future) any inference path needing tier_delta as a feature
"""
from typing import Optional
import pandas as pd

TIER_LABELS = {
    1:  "Maiden Claiming",
    2:  "Low Claiming (≤$25K)",
    3:  "Maiden Special Weight",
    4:  "Mid Claiming ($25-50K)",
    5:  "High Claiming (>$50K)",
    6:  "Allowance",
    7:  "Optional Claiming / AOC",
    8:  "Listed Stakes",
    9:  "G3-equivalent (purse <$200K)",
    10: "G2-equivalent (purse $200-400K)",
    11: "G1-equivalent (purse ≥$400K)",
}


def race_class_tier(race_type: Optional[str],
                    claiming_price_entered: Optional[float],
                    purse: Optional[float],
                    grade: Optional[int] = None) -> Optional[int]:
    """Return ordinal tier 1-11, or None if unclassifiable.

    Inputs come from past_performances columns (race_type,
    claiming_price_entered, purse) plus `grade` joined from races
    (chart-parsed; NULL when the historical race wasn't a graded stakes
    or had a non-standard L2). Pure function for testability and reuse
    outside pandas.
    """
    if race_type is None:
        return None
    cp = claiming_price_entered if claiming_price_entered is not None else 0
    p  = purse if purse is not None else 0

    if race_type == "maiden_claiming":
        return 1
    if race_type == "claiming":
        if cp <= 25000: return 2
        if cp <= 50000: return 4
        return 5
    if race_type == "maiden":
        return 3
    if race_type == "allowance":
        return 6
    if race_type == "allowance_optional_claiming":
        return 7
    if race_type == "stakes":
        return 8
    if race_type == "graded_stakes":
        # Prefer chart-parsed grade when available.
        if grade == 3: return 9
        if grade == 2: return 10
        if grade == 1: return 11
        # Fallback for graded_stakes with NULL grade
        # (~1.9% — non-standard L2 layouts, deferred-bug list).
        if p <  200000: return 9
        if p <  400000: return 10
        return 11
    return None


def add_class_tier_columns(pps_df: pd.DataFrame) -> pd.DataFrame:
    """Add `class_tier`, `prior_class_tier`, `class_delta` columns.

    Sorts by (horse_id, race_date) for the LAG operation. Returns a copy.
    Required columns: horse_id, race_date, race_type,
    claiming_price_entered, purse, grade (grade may be NULL).
    """
    df = pps_df.copy().sort_values(["horse_id", "race_date"]).reset_index(drop=True)
    df["class_tier"] = df.apply(
        lambda r: race_class_tier(
            r.get("race_type"),
            r.get("claiming_price_entered"),
            r.get("purse"),
            r.get("grade"),
        ),
        axis=1,
    )
    df["prior_class_tier"] = df.groupby("horse_id")["class_tier"].shift(1)
    df["class_delta"] = df["class_tier"] - df["prior_class_tier"]
    return df
