"""Shared horse-name normalization & match-key utilities.

Two distinct functions, used together to fix the duplicate-horse-row bug
(see scripts/merge_duplicate_horses.py for the one-shot DB cleanup).

- normalize_horse_name(s): canonical *storage* form. Lowercases, trims,
  collapses internal multi-whitespace. Used at every site that *creates*
  a horse_name value.

- horse_match_key(s): aggressive *lookup* key. Lowercases and strips all
  non-alphanumerics. Treats 'Further Ado' / 'FurtherAdo' / "Further-Ado"
  as the same horse. Used ONLY for matching; never persisted.

The chart-parser pipeline derives names from PDF text where pdftotext
sometimes collapses inter-word whitespace ('Further Ado' -> 'FurtherAdo').
We can't recover the missing space deterministically, so we accept that
the canonical form may be either variant depending on which ingestion
path won the race. horse_match_key lets every future lookup find the
existing row regardless of variant, preventing further duplicates.
"""
from __future__ import annotations
import re

_WS_RE  = re.compile(r"\s+")
_KEY_RE = re.compile(r"[^a-z0-9]")


def normalize_horse_name(name: str | None) -> str:
    """Canonical storage form: lowercase + trim + collapse internal whitespace.

    Returns "" for None/empty input.

    Examples:
      'Further Ado'      -> 'further ado'
      '  Further  Ado  ' -> 'further ado'
      'FurtherAdo'       -> 'furtherado'   # spaces unrecoverable
    """
    if not name:
        return ""
    return _WS_RE.sub(" ", name.lower()).strip()


def horse_match_key(name: str | None) -> str:
    """Aggressive lookup key: lowercase, alphanumeric-only.

    Treats 'Further Ado', 'FurtherAdo', "Further-Ado", and 'Further  Ado'
    as identical. NEVER stored.

    Examples:
      'Further Ado'   -> 'furtherado'
      'FurtherAdo'    -> 'furtherado'
      "D'Andrade"     -> 'dandrade'
    """
    if not name:
        return ""
    return _KEY_RE.sub("", name.lower())


# SQL fragment for use in WHERE clauses — produces the same key server-side.
# Matches horse_match_key(s) computed in Python.
HORSE_MATCH_KEY_SQL = "REGEXP_REPLACE(LOWER(horse_name), '[^a-z0-9]', '', 'g')"
