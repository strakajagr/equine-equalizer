"""Shared race-type classification logic.

Used by:
- hrn_scraper.py at parse time (forward fix for new rows)
- scripts/backfill_race_types.py to reclassify existing rows
  whose race_type was set to 'allowance' by the prior naive
  default (because dist_text alone lacked stakes keywords).

Decision order:
  1. Explicit grade markers ('grade 1/2/3', 'graded stakes')
     -> graded_stakes
  2. Optional-claiming variants -> allowance_optional_claiming
  3. Stakes indicator (derby, oaks, cup, classic, ' s.', stakes,
     handicap, memorial, breeders, futurity, juvenile, etc.)
     combined with purse threshold:
       purse >= $200K -> graded_stakes (G1-G3 equivalent)
       purse >= $100K -> stakes
       below $100K with stakes indicator -> falls through
  4. Maiden variants -> maiden / maiden_claiming
  5. 'claiming' alone -> claiming
  6. 'allowance' -> allowance
  7. Default -> allowance
"""
from __future__ import annotations
from typing import Optional

GRADE_MARKERS = ('graded stakes', 'grade 1', 'grade 2', 'grade 3')

OPTIONAL_CLAIMING = (
    'allowance optional claiming',
    'starter optional claiming',
    'optional claiming',
)

STAKES_INDICATORS = (
    ' s.', ' stakes', ' h.',
    'derby', 'oaks', 'cup', 'classic',
    'breeders', 'handicap', 'memorial',
    'invitational', 'championship', 'futurity',
    'juvenile', 'preakness', 'belmont',
    'overnight',
)

MAIDEN_VARIANTS = (
    ('maiden special weight', 'maiden'),
    ('maiden claiming',       'maiden_claiming'),
    ('maiden',                'maiden'),
)


def classify_race_type(
    dist_text: Optional[str] = None,
    race_name: Optional[str] = None,
    conditions: Optional[str] = None,
    purse: Optional[int] = None,
    grade: Optional[int] = None,
) -> str:
    """Return one of: graded_stakes / stakes / allowance_optional_claiming /
    allowance / maiden / maiden_claiming / claiming."""
    haystack = ' '.join(
        s for s in (dist_text, race_name, conditions) if s
    ).lower()
    p = int(purse or 0)

    if any(k in haystack for k in GRADE_MARKERS):
        return 'graded_stakes'

    # Authoritative grade-column shortcut: any row with grade 1/2/3 set
    # is by definition a graded stakes, regardless of what the
    # conditions text contains. Catches edge cases like "Apple Blossom
    # H." where race_name uses an abbreviation the keyword list doesn't
    # match.
    if grade is not None and grade in (1, 2, 3):
        return 'graded_stakes'

    if any(k in haystack for k in OPTIONAL_CLAIMING):
        return 'allowance_optional_claiming'

    has_stakes = any(k in haystack for k in STAKES_INDICATORS)
    if has_stakes:
        if p >= 200_000:
            return 'graded_stakes'
        if p >= 100_000:
            return 'stakes'
        # has_stakes==True with purse below threshold — still NOT an
        # allowance. Lower-purse handicaps, ratings handicaps, starter
        # stakes, and overnights all land here. Default to 'stakes'.
        return 'stakes'

    for keyword, rt in MAIDEN_VARIANTS:
        if keyword in haystack:
            return rt

    if 'claiming' in haystack:
        return 'claiming'

    if 'allowance' in haystack:
        return 'allowance'

    return 'allowance'
