"""
Equibase PDF Result Chart Parser & Aurora Loader

Reads PDFs from S3 (equine-raw-data/charts/{TRACK}/)
or local disk. Parses race and runner data, loads to Aurora.

Called from ingestion Lambda via:
  {"action": "parse_charts", "track": "GP"}
  {"action": "parse_charts"}  (all tracks)
"""

import io
import json
import logging
import os
import re
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

import boto3
import pdfplumber

from shared.horse_naming import (
    normalize_horse_name,
    horse_match_key,
    HORSE_MATCH_KEY_SQL,
)

logger = logging.getLogger(__name__)

S3_BUCKET = 'equine-raw-data'
S3_PREFIX = 'charts/'

# ═══════════════════════════════════════════
# PDF TEXT EXTRACTION
# ═══════════════════════════════════════════

def extract_all_text(source) -> str:
    """Extract text from a PDF file path or bytes buffer."""
    with pdfplumber.open(source) as pdf:
        pages = []
        for pg in pdf.pages:
            t = pg.extract_text()
            if t:
                pages.append(t)
    return "\n".join(pages)


def split_into_races(full_text: str) -> list[str]:
    """Split full PDF text into individual race blocks."""
    pattern = re.compile(
        r'^[A-Z][A-Z ]*-[A-Z][a-z].*?-Race\d+',
        re.MULTILINE
    )
    matches = list(pattern.finditer(full_text))
    if not matches:
        return []

    blocks = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        blocks.append(full_text[start:end])
    return blocks


# ═══════════════════════════════════════════
# RACE HEADER PARSING
# ═══════════════════════════════════════════

def parse_race_header(block: str, track_code: str, file_date: date) -> dict | None:
    lines = block.split('\n')
    if len(lines) < 15:
        return None

    m = re.search(r'Race(\d+)', lines[0], re.IGNORECASE)
    if not m:
        return None
    race_number = int(m.group(1))

    race_type_raw = lines[2] if len(lines) > 2 else ""
    race_type = parse_race_type(race_type_raw)

    distance_furlongs = None
    surface = 'dirt'
    for line in lines[:12]:
        if 'distance:' in line.lower():
            distance_furlongs = parse_distance(line)
            surface = parse_surface(line)
            break

    purse = None
    for line in lines[:12]:
        if line.lower().startswith('purse:'):
            pm = re.search(r'\$([0-9,]+)', line)
            if pm:
                purse = int(pm.group(1).replace(',', ''))
            break

    claiming_price = None
    for line in lines[:6]:
        cm = re.search(r'ClaimingPrice:\$([0-9,]+)', line)
        if cm:
            claiming_price = int(cm.group(1).replace(',', ''))
            break

    track_condition = None
    temperature = None
    weather = None
    for line in lines[:15]:
        if 'weather:' in line.lower() and 'track:' in line.lower():
            wm = re.search(r'Weather:(\S+)', line)
            if wm:
                weather = wm.group(1).rstrip(',')
            tm = re.search(r',\s*(\d+)\xb0', line)
            if tm:
                temperature = int(tm.group(1))
            tcm = re.search(r'Track:(\S+)', line)
            if tcm:
                track_condition = tcm.group(1).lower()
            break

    post_time = None
    for line in lines[:15]:
        otm = re.search(r'Offat:(\d+:\d+)', line)
        if otm:
            try:
                t = datetime.strptime(otm.group(1), '%H:%M').time()
                post_time = datetime.combine(file_date, t)
            except ValueError:
                pass
            break

    fractions = []
    final_time = None
    for line in lines:
        if 'fractionaltimes:' in line.lower():
            times = re.findall(r'(\d+:\d+\.\d+|\d+\.\d+)', line)
            ftm = re.search(
                r'FinalTime:\s*(\d+:\d+\.\d+|\d+\.\d+)', line
            )
            if ftm:
                final_time = parse_time_to_seconds(ftm.group(1))
            for t in times:
                val = parse_time_to_seconds(t)
                if val and val != final_time:
                    fractions.append(val)
            break

    num_calls = 5
    header_idx = None
    for i, line in enumerate(lines[:30]):
        if 'LastRaced' in line and 'Pgm' in line:
            header_idx = i
            # Count call columns between "Start" and "Odds" — handles
            # sprints (3 calls: 1/4 Str Fin), miles (4: 1/4 1/2 Str Fin),
            # routes (5+: 1/4 1/2 3/4 Str Fin or longer). Pre-fix, the
            # default of 4 calls was wrong for short sprints, causing the
            # odds column to be consumed as a "call" — the first digit of
            # the odds got assigned as position, falsely tagging horses
            # as winners.
            m = re.search(r'\bStart\b\s+(.+?)\s+Odds\b', line)
            if m:
                num_calls = len(m.group(1).split())
            break

    # Quick first pass: count valid runner lines so parse_call_token can
    # correctly disambiguate 2-digit positions (e.g. '11' = pos 11 vs 1+1len).
    field_size_est = 0
    if header_idx is not None:
        for i in range(header_idx + 1, len(lines)):
            line = lines[i]
            if not line.strip():
                continue
            if line.startswith('FractionalTimes') or line.startswith('SplitTimes'):
                break
            if re.search(r'\d+[A-Z]?\s+[A-Z][^\(]+\([^\)]+\)', line):
                field_size_est += 1

    runners = []
    if header_idx is not None:
        for i in range(header_idx + 1, len(lines)):
            line = lines[i]
            if not line.strip():
                continue
            if line.startswith('FractionalTimes') or line.startswith('SplitTimes'):
                break
            runner = parse_runner_line(
                line, num_calls, field_size=field_size_est or 20,
                runner_idx=len(runners),
            )
            if runner:
                runners.append(runner)

    meta = extract_race_meta(block)

    return {
        'track_code': track_code,
        'race_date': file_date,
        'race_number': race_number,
        'race_type': race_type,
        'race_name': meta['race_name'],
        'conditions': meta['conditions'],
        'grade': meta['grade'],
        'distance_furlongs': distance_furlongs,
        'surface': surface,
        'purse': purse,
        'claiming_price': claiming_price,
        'track_condition': track_condition,
        'temperature': temperature,
        'weather_conditions': weather,
        'post_time': post_time,
        'fractions': fractions,
        'final_time': final_time,
        'num_calls': num_calls,
        'runners': runners,
        'field_size': len(runners),
    }


# ═══════════════════════════════════════════
# RUNNER LINE PARSING
# ═══════════════════════════════════════════

def parse_runner_line(
    line: str, num_calls: int, field_size: int = 20,
    runner_idx: int = 0,
) -> dict | None:
    """
    Parse a single runner line from an Equibase Result Chart.

    Extracts position AND lengths-behind at each call.  field_size is used
    to disambiguate 2-digit positions (e.g. '11' = pos 11 vs pos 1 + 1 len).
    """
    if not line.strip():
        return None
    if any(line.startswith(x) for x in [
        'Fractional', 'Split', 'Run-Up', 'Winner',
        'Breeder', 'Owner', 'Trainer', 'Claiming',
        'Scratched', 'Total', 'Pgm', 'Past', 'Footnote',
        'Copyright', 'Trainers:', 'Owners:', '$',
        'Value', 'Available', 'Includes', 'Plus',
    ]):
        return None

    # Greedy horse_name match; jockey paren must contain a comma
    # (= "Last,First" format; can have additional commas like "Ortiz,Jr.,Irad").
    # Country-suffix parens — (FR), (IRE), (GB), (JPN), (BRZ), (ARG), etc. —
    # have no comma, so they're absorbed into the horse_name match instead of
    # being treated as the jockey paren. Pre-fix, those horses were silently
    # dropped because the regex matched the country-suffix paren as jockey,
    # then weight = int(tokens[0]) on "(Jockey,Name)" raised ValueError.
    # Coupled-entry program numbers like 1A / 2B / 3X have a single uppercase
    # letter immediately following the digits (no whitespace), so [A-Z]? is
    # optional. Pre-fix, those rows were dropped wholesale, which under-counted
    # field_size_est and made 2-digit position disambiguation reject valid
    # cand_2 cases for the 10th-place horse — producing phantom multi-winners.
    # Jockey body allows ONE level of nested parens (e.g. an alias like
    # "Huayas,Gherson(Jason)") via the alternation `[^()]|\([^()]*\)`. The
    # comma-required structure preserves the country-suffix vs jockey
    # distinction (country suffixes have no comma, so they fail the inner
    # comma-anchored pattern and the regex backtracks past them to the
    # actual jockey paren).
    m = re.search(
        r'(\d+[A-Z]?)\s+([A-Z].+?)'
        r'\(((?:[^()]|\([^()]*\))*?,(?:[^()]|\([^()]*\))*)\)',
        line,
    )
    if not m:
        return None

    pgm = m.group(1)
    horse_name = normalize_horse_name(m.group(2))
    jockey_raw = m.group(3).strip()

    jockey_parts = jockey_raw.split(',')
    if len(jockey_parts) == 2:
        jockey_name = f"{jockey_parts[1].strip()} {jockey_parts[0].strip()}"
    else:
        jockey_name = jockey_raw

    pre_pgm = line[:m.start(1)].strip()
    last_raced_str = pre_pgm if pre_pgm and pre_pgm != '---' else None

    after_paren = line[m.end():]
    tokens = after_paren.split()

    # Bug F: pdftotext sometimes fuses the finish call token with the odds
    # column when the chart's columnar whitespace is tight. Example token:
    # "10101/4109.50" = finish position 10, lengths 10¼, odds 109.50. The
    # parser then can't recognise either piece — _parse_lengths_str rejects
    # the prefix because it has trailing extra digits, and odds float() fails.
    # When the last call token has a trailing odds-shaped suffix
    # (\d{1,3}\.\d{2}\*?) with a non-empty prefix, split unconditionally:
    # _parse_lengths_str never accepts decimal-with-period as a length, so
    # this suffix can only be fused odds. (A count-based gate doesn't work
    # because fusion shifts comments — a fused line + comments has the same
    # total token count as a non-fused line + comments.)
    last_call_idx = 3 + num_calls
    if 0 <= last_call_idx < len(tokens):
        fm = re.search(r'(\d{1,3}\.\d{2}\*?)$', tokens[last_call_idx])
        if fm and fm.start() > 0:
            pre = tokens[last_call_idx][:fm.start()]
            fused_odds = fm.group(1)
            tokens = (
                tokens[:last_call_idx] + [pre, fused_odds]
                + tokens[last_call_idx + 1:]
            )

    if len(tokens) < num_calls + 4:
        return None

    try:
        weight = int(tokens[0])
    except (ValueError, IndexError):
        return None

    me = tokens[1]
    lasix = 'L' in me
    blinkers = 'b' in me
    first_time_lasix = 'f' in me and lasix

    try:
        pp = int(tokens[2])
    except (ValueError, IndexError):
        return None

    try:
        start_pos = int(tokens[3])
    except (ValueError, IndexError):
        start_pos = None

    calls_raw = tokens[4:4 + num_calls]
    call_positions = []
    call_lengths = []
    # Equibase lists runners in finish order, so runner_idx + 1 is the
    # expected finish position. Pass it as a disambiguation hint to
    # parse_call_token — used as a tiebreaker when both 1-digit and
    # 2-digit interpretations of an ambiguous token are valid.
    expected = runner_idx + 1
    for c in calls_raw:
        pos, lengths = parse_call_token(
            c, field_size=field_size, expected_position=expected
        )
        call_positions.append(pos)
        call_lengths.append(lengths)

    finish_position = call_positions[-1] if call_positions else None
    finish_lengths = call_lengths[-1] if call_lengths else None

    odds_idx = 4 + num_calls
    odds = None
    if odds_idx < len(tokens):
        odds_str = tokens[odds_idx].rstrip('*')
        try:
            odds = float(odds_str)
        except ValueError:
            pass

    comments = ' '.join(tokens[odds_idx + 1:]) if odds_idx + 1 < len(tokens) else None

    last_raced_date = None
    last_raced_track = None
    if last_raced_str:
        lm = re.match(
            r'(\d{1,2})([A-Z][a-z]{2})(\d{2})'
            r'(\d+)([A-Z]{2,4})(\d+)',
            last_raced_str
        )
        if lm:
            day = int(lm.group(1))
            mon_str = lm.group(2).lower()
            yr = int(lm.group(3))
            last_raced_track = lm.group(5)
            mon_map = {
                'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
                'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
                'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
            }
            mon = mon_map.get(mon_str)
            if mon:
                full_yr = 2000 + yr if yr < 50 else 1900 + yr
                try:
                    last_raced_date = date(full_yr, mon, day)
                except ValueError:
                    pass

    return {
        'program_number': pgm,
        'horse_name': horse_name,
        'jockey_name': jockey_name,
        'post_position': pp,
        'weight_carried': weight,
        'lasix': lasix,
        'lasix_first_time': first_time_lasix,
        'blinkers_on': blinkers,
        'finish_position': finish_position,
        'finish_lengths_behind': finish_lengths,
        'morning_line_odds': odds,
        'start_position': start_pos,
        'calls': call_positions,       # positions at each call
        'call_lengths': call_lengths,  # lengths behind at each call
        'comments': comments,
        'last_raced_date': last_raced_date,
        'last_raced_track': last_raced_track,
    }


LENGTHS_WORDS = {
    'head': 0.1, 'hd': 0.1,
    'neck': 0.2, 'nk': 0.2,
    'nose': 0.05, 'no': 0.05, 'ns': 0.05,
}


def _parse_lengths_str(s: str) -> float | None:
    """
    Convert a lengths string (the part after the position digit) to float.
    Returns 0.0 for empty string (horse is right at the called position).
    Returns None if the string is unrecognisable.

    Handles: '', 'Head', 'Neck', 'Nose', '1/2', '3/4', '2',
             '11/2' (1½), '41/2' (4½), '131/2' (13½), '23/4' (2¾).
    """
    if not s:
        return 0.0
    lo = s.lower()
    if lo in LENGTHS_WORDS:
        return LENGTHS_WORDS[lo]
    # Pure fraction: "1/2", "3/4"
    m = re.fullmatch(r'(\d)/(\d)', s)
    if m:
        return int(m.group(1)) / int(m.group(2))
    # Pure integer 1–30
    m = re.fullmatch(r'(\d{1,2})', s)
    if m:
        return float(s)
    # Mixed number: {1-2 digit whole}{1-digit numerator}/{1-digit denominator}
    # e.g. "11/2"=1.5, "41/2"=4.5, "131/2"=13.5, "23/4"=2.75
    m = re.fullmatch(r'(\d{1,2})(\d)/(\d)', s)
    if m:
        return float(m.group(1)) + int(m.group(2)) / int(m.group(3))
    return None


def parse_call_token(
    s: str, field_size: int = 20,
    expected_position: int | None = None,
) -> tuple[int | None, float | None]:
    """
    Parse a concatenated position+lengths token into (position, lengths_behind).

    Equibase format: position number immediately followed by a lengths indicator
    with no separator.  Examples:
      '641/2' → (6, 4.5)   '11'    → (1, 1.0) for 8-horse / (11, 0.0) for 12-horse
      '2Head' → (2, 0.1)   '123/4' → (1, 2.75) for 8-horse
      '1Neck' → (1, 0.2)   '613/4' → (6, 1.75) — position 6, 1¾ lengths

    Disambiguation for 2-digit positions:
      - Try 2-digit position (10–min(field_size,20)) only when the remainder
        after removing 2 digits parses as valid lengths.
      - Otherwise fall back to 1-digit position.
    """
    s = s.strip().rstrip('*')
    if not s or not s[0].isdigit():
        return (None, None)

    # Compute both candidate parses without prematurely returning.
    cand_2 = None
    if len(s) >= 2 and s[1].isdigit():
        p2 = int(s[:2])
        if 10 <= p2 <= min(field_size, 20):
            l2 = _parse_lengths_str(s[2:])
            if l2 is not None:
                cand_2 = (p2, l2)

    pos1 = int(s[0])
    rest1 = s[1:]
    l1 = _parse_lengths_str(rest1)
    cand_1 = (pos1, l1) if l1 is not None else None

    # Disambiguation when both candidates are valid:
    # - With expected_position context (passed by parse_runner_line via
    #   runner_idx since Equibase lists runners in finish order), prefer
    #   the candidate whose position is closer to the expected.
    # - Without context, prefer 2-digit (statistically more correct in
    #   N-horse fields where exactly one horse is in pos 1; the rest are
    #   in pos 2..N).
    # Tokens like "11Head" only have a 2-digit candidate (since
    # _parse_lengths_str rejects "1Head"), so non-ambiguous tokens
    # resolve correctly regardless of this rule.
    if cand_1 and cand_2:
        if expected_position is not None:
            if abs(cand_1[0] - expected_position) < abs(cand_2[0] - expected_position):
                return cand_1
            return cand_2
        return cand_2
    if cand_2:
        return cand_2
    if cand_1:
        return cand_1
    return (pos1, None)


def parse_call_position(s: str) -> int | None:
    """Kept for backwards-compat. Prefer parse_call_token."""
    pos, _ = parse_call_token(s)
    return pos


# ═══════════════════════════════════════════
# FIELD PARSERS
# ═══════════════════════════════════════════

def parse_race_type(raw: str) -> str:
    lower = raw.lower()
    if 'graded' in lower or 'grade' in lower:
        return 'graded_stakes'
    if 'starter stakes' in lower:
        return 'stakes'
    if 'starter allowance' in lower:
        return 'allowance'
    if 'stakes' in lower:
        return 'stakes'
    if 'overnight' in lower:
        return 'stakes'
    if 'handicap' in lower:
        return 'stakes'
    if 'allowance' in lower and 'optional' in lower:
        return 'allowance_optional_claiming'
    if 'allowance' in lower:
        return 'allowance'
    if 'maiden' in lower and 'claiming' in lower:
        return 'maiden_claiming'
    if 'maiden' in lower:
        return 'maiden'
    if 'claiming' in lower:
        return 'claiming'
    return 'allowance'


# ═══════════════════════════════════════════
# RACE-NAME / CONDITIONS / GRADE EXTRACTION
# ═══════════════════════════════════════════

GRADE_RE       = re.compile(r'Grade\s*([1-3])(?!\d)', re.IGNORECASE)
LISTED_RE      = re.compile(r'Listed', re.IGNORECASE)
PRESENTEDBY_RE = re.compile(r'presentedby', re.IGNORECASE)
RACE_PREFIX_RE = re.compile(
    r'^(?:GRADED\s*STAKES|STARTER\s*STAKES|STAKES|'
    r'WAIVER\s*MAIDEN\s*CLAIMING|WAIVER\s*CLAIMING|'
    r'MAIDEN\s*SPECIAL\s*WEIGHT|'
    r'MAIDEN\s*OPTIONAL\s*CLAIMING|'
    r'MAIDEN\s*CLAIMING|MAIDEN|'
    r'ALLOWANCE\s*OPTIONAL\s*CLAIMING|'
    r'STARTER\s*OPTIONAL\s*CLAIMING|OPTIONAL\s*CLAIMING|'
    r'STARTER\s*ALLOWANCE|ALLOWANCE|'
    r'STARTER\s*HANDICAP|RATINGS\s*HANDICAP|HANDICAP|'
    r'CLAIMING)',
    re.IGNORECASE,
)


def _camel_split(s: str) -> str:
    s = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', s)
    s = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', ' ', s)
    s = re.sub(r'(?<=[a-zA-Z])(?=\d)', ' ', s)
    s = re.sub(r'(?<=\d)(?=[A-Z])', ' ', s)
    return s


def extract_race_meta(block: str) -> dict:
    """Pull race_name, conditions, grade from a race block.

    L2 of each block carries the type prefix + name + grade marker
    (mashed together by pdfplumber's text extraction). L3+ carries the
    eligibility/conditions text up to the 'Distance:' or similar line.
    Non-stakes races (maiden / claiming / allowance) have no proper
    name on the chart, so race_name returns None for those.
    """
    lines = block.split("\n")
    if len(lines) < 4:
        return {"race_name": None, "conditions": None, "grade": None}

    raw_l2 = lines[2] if len(lines) > 2 else ""
    cond_lines = []
    for j in range(3, min(len(lines), 12)):
        line = lines[j]
        ll = line.lower()
        if (ll.startswith("distance:") or ll.startswith("purse:")
                or ll.startswith("availablemoney:")
                or ll.startswith("valueofrace:")
                or ll.startswith("weather:") or ll.startswith("offat:")
                or ll.startswith("includes:")):
            break
        cond_lines.append(line)
    raw_conditions = " ".join(cond_lines).strip()

    rest = re.sub(r'\s*-\s*Thoroughbred\s*$', '', raw_l2.strip())

    grade = None
    gm = GRADE_RE.search(rest)
    if gm:
        grade = int(gm.group(1))
        rest = GRADE_RE.sub('', rest)
    else:
        rest = LISTED_RE.sub('', rest)

    name = RACE_PREFIX_RE.sub('', rest).strip(' -')

    if name:
        race_name = _camel_split(name)
        race_name = PRESENTEDBY_RE.sub(' presented by ', race_name)
        race_name = re.sub(r',(?=[A-Za-z])', ', ', race_name)
        race_name = re.sub(r'\.(?=[A-Z])', '. ', race_name)
        race_name = re.sub(r'\s+', ' ', race_name).strip()
        race_name = race_name[:200] or None
    else:
        race_name = None

    if raw_conditions:
        conditions = _camel_split(raw_conditions)
        conditions = PRESENTEDBY_RE.sub(' presented by ', conditions)
        conditions = re.sub(r',(?=[A-Za-z])', ', ', conditions)
        conditions = re.sub(r'\.(?=[A-Z])', '. ', conditions)
        conditions = re.sub(r'\s+', ' ', conditions).strip()
        conditions = conditions[:500] or None
    else:
        conditions = None

    return {"race_name": race_name, "conditions": conditions, "grade": grade}


DISTANCE_WORDS = {
    'oneandonesixteenthmiles': 8.5,
    'oneandoneeighthmiles': 9.0,
    'oneandthreesixteenthmiles': 9.5,
    'oneandonequartermiles': 10.0,
    'oneandthreeeighthmiles': 11.0,
    'oneandonehalf': 12.0,
    'onemile': 8.0,
    'sevenfurlongs': 7.0,
    'sixandonehalf': 6.5,
    'sixfurlongs': 6.0,
    'fiveandonehalf': 5.5,
    'fivefurlongs': 5.0,
    'fourandonehalf': 4.5,
    'fourfurlongs': 4.0,
    'eightandonehalf': 8.5,
}


def parse_distance(line: str) -> float | None:
    lower = line.lower().replace(' ', '').replace('-', '')
    for pattern, furlongs in sorted(
        DISTANCE_WORDS.items(), key=lambda x: -len(x[0])
    ):
        if pattern in lower:
            return furlongs
    m = re.search(r'(\d+(?:\.\d+)?)\s*furlong', lower)
    if m:
        return float(m.group(1))
    return None


def parse_surface(line: str) -> str:
    lower = line.lower()
    if 'turf' in lower:
        return 'turf'
    if 'all weather' in lower or 'allweather' in lower or 'synthetic' in lower:
        return 'synthetic'
    return 'dirt'


def parse_time_to_seconds(time_str: str) -> float | None:
    try:
        if ':' in time_str:
            parts = time_str.split(':')
            return float(parts[0]) * 60 + float(parts[1])
        return float(time_str)
    except (ValueError, IndexError):
        return None


# ═══════════════════════════════════════════
# DATABASE LOADING
# ═══════════════════════════════════════════

def upsert_track(conn, track_code: str) -> str | None:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT track_id FROM tracks WHERE track_code = %s",
            (track_code,)
        )
        row = cur.fetchone()
        return str(row['track_id']) if row else None


def upsert_horse(conn, horse_name: str) -> str:
    """Match by aggressive key, insert canonical form on miss."""
    canonical = normalize_horse_name(horse_name)
    key = horse_match_key(horse_name)
    with conn.cursor() as cur:
        if key:
            cur.execute(
                f"SELECT horse_id FROM horses "
                f"WHERE {HORSE_MATCH_KEY_SQL} = %s LIMIT 1",
                (key,)
            )
            row = cur.fetchone()
            if row:
                return str(row['horse_id'])
        cur.execute(
            "INSERT INTO horses (horse_name) VALUES (%s) "
            "RETURNING horse_id",
            (canonical,)
        )
        return str(cur.fetchone()['horse_id'])


def upsert_jockey(conn, jockey_name: str) -> str:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT jockey_id FROM jockeys "
            "WHERE LOWER(jockey_name) = LOWER(%s) LIMIT 1",
            (jockey_name,)
        )
        row = cur.fetchone()
        if row:
            return str(row['jockey_id'])
        cur.execute(
            "INSERT INTO jockeys (jockey_name) VALUES (%s) "
            "RETURNING jockey_id",
            (jockey_name,)
        )
        return str(cur.fetchone()['jockey_id'])


def upsert_trainer(conn, trainer_name: str) -> str:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT trainer_id FROM trainers "
            "WHERE LOWER(trainer_name) = LOWER(%s) LIMIT 1",
            (trainer_name,)
        )
        row = cur.fetchone()
        if row:
            return str(row['trainer_id'])
        cur.execute(
            "INSERT INTO trainers (trainer_name) VALUES (%s) "
            "RETURNING trainer_id",
            (trainer_name,)
        )
        return str(cur.fetchone()['trainer_id'])


def insert_race(conn, race: dict, track_id: str) -> str:
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO races (
                track_id, race_date, race_number,
                post_time, distance_furlongs, surface,
                race_type, race_name, conditions, grade,
                purse, claiming_price,
                field_size, track_condition,
                temperature, weather_conditions
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (track_id, race_date, race_number)
            DO UPDATE SET
                race_name = COALESCE(EXCLUDED.race_name, races.race_name),
                conditions = COALESCE(EXCLUDED.conditions, races.conditions),
                grade = COALESCE(EXCLUDED.grade, races.grade),
                field_size = EXCLUDED.field_size,
                track_condition = EXCLUDED.track_condition,
                temperature = EXCLUDED.temperature,
                weather_conditions = EXCLUDED.weather_conditions
            RETURNING race_id""",
            (
                track_id, race['race_date'], race['race_number'],
                race.get('post_time'), race['distance_furlongs'],
                race['surface'], race['race_type'],
                race.get('race_name'), race.get('conditions'),
                race.get('grade'),
                race.get('purse'), race.get('claiming_price'),
                race.get('field_size'), race.get('track_condition'),
                race.get('temperature'), race.get('weather_conditions'),
            )
        )
        return str(cur.fetchone()['race_id'])


def parse_payout_section(block: str) -> dict:
    """
    Extract mutuel payouts from a race block.
    Format (show wagering present):
      Pgm Horse Win Place Show WagerType Combo Payoff Pool
      5 Cagua 6.80 3.20 2.20 $1.00Exacta 5-6 12.50 71477
      6 Splicer 5.20 3.80 $0.50Trifecta 5-6-7 45.35 44964
      7 BrainTrust 5.40 $0.10Superfecta 5-6-7-3 26.86 30830

    Format (no show wagering — short field):
      Pgm Horse Win Place WagerType Combo Payoff Pool
      4 Frippet 2.20 2.10 $1.00Exacta 4-3 3.90 33520
      3 GoldWatch 3.20 $0.50Pick3 ...

    Returns dict with:
      wps: {pgm_number: {win, place, show}}
      exotics: {exacta: {combo, payout}, trifecta: ..., etc.}
    """
    result = {'wps': {}, 'exotics': {}}

    # Find payout section — use regex so variant spacing in PDFs
    # (e.g. "Pgm  Horse  Win  Place") doesn't cause a miss.
    # Header may or may not include 'Show' (short fields <5 starters).
    m = re.search(r'Pgm\s+Horse\s+Win\s+Place', block)
    if not m:
        return result
    idx = m.start()

    # Determine if show wagering exists from header line
    header_line_end = block.find('\n', idx)
    header_line = block[idx:header_line_end] if header_line_end > 0 else block[idx:]
    has_show = bool(re.search(r'\bShow\b', header_line))

    # Get lines between payout header and next section
    end_idx = block.find('PastPerformanceRunningLine', idx)
    if end_idx < 0:
        end_idx = block.find('Trainers:', idx)
    if end_idx < 0:
        end_idx = min(idx + 800, len(block))

    section = block[idx:end_idx]
    lines = section.split('\n')

    # Track WPS line order: line 0=winner, 1=2nd, 2=3rd
    # This lets us correctly assign win/place/show regardless
    # of whether show wagering exists (short-field races).
    wps_line_idx = 0

    for line in lines[1:]:  # skip header
        line = line.strip()
        if not line:
            continue

        # Try to parse WPS line:
        # "5 Cagua 6.80 3.20 2.20 $1.00Exacta 5-6 12.50 71,477"
        wps_match = re.match(
            r'^(\d+)\s+(\S+)\s+'
            r'(\d+\.\d{2})?\s*'
            r'(\d+\.\d{2})?\s*'
            r'(\d+\.\d{2})?\s*',
            line
        )
        if wps_match:
            pgm = wps_match.group(1)
            prices = [
                wps_match.group(3),
                wps_match.group(4),
                wps_match.group(5),
            ]
            prices = [
                float(p) for p in prices if p is not None
            ]

            wps = {}
            # Assign win/place/show by position in the payout
            # table (not by price count), so short-field races
            # without show wagering are handled correctly.
            if wps_line_idx == 0:  # winner
                if len(prices) >= 1:
                    wps['win'] = prices[0]
                if len(prices) >= 2:
                    wps['place'] = prices[1]
                if len(prices) >= 3:
                    wps['show'] = prices[2]
            elif wps_line_idx == 1:  # 2nd place
                if len(prices) >= 1:
                    wps['place'] = prices[0]
                if len(prices) >= 2 and has_show:
                    wps['show'] = prices[1]
            elif wps_line_idx == 2:  # 3rd place
                if len(prices) >= 1 and has_show:
                    wps['show'] = prices[0]

            wps_line_idx += 1

            if wps:
                result['wps'][pgm] = wps

        # Extract exotic payouts from this line
        # Pattern: $1.00Exacta 5-6 12.50 or $0.50Trifecta 5-6-7 45.35
        for exotic_match in re.finditer(
            r'\$[\d.]+?(Exacta|Trifecta|Superfecta|'
            r'DailyDouble|Quinella|Pick\s*\d|'
            r'SuperHighFive)\s+'
            r'([\d\-]+)\s+'
            r'([\d,]+\.\d{2})',
            line, re.IGNORECASE
        ):
            bet_type = exotic_match.group(1).lower()
            combo = exotic_match.group(2)
            payout = float(
                exotic_match.group(3).replace(',', '')
            )

            # Normalize bet type names
            if 'exacta' in bet_type:
                result['exotics']['exacta'] = {
                    'combo': combo, 'payout': payout
                }
            elif 'trifecta' in bet_type:
                result['exotics']['trifecta'] = {
                    'combo': combo, 'payout': payout
                }
            elif 'superfecta' in bet_type:
                result['exotics']['superfecta'] = {
                    'combo': combo, 'payout': payout
                }
            elif 'daily' in bet_type:
                result['exotics']['daily_double'] = {
                    'combo': combo, 'payout': payout
                }
            elif 'pick' in bet_type:
                result['exotics']['pick'] = {
                    'combo': combo, 'payout': payout
                }

    return result


def insert_result(conn, race_id, entry_id, horse_id, runner, race, payouts=None):
    positions = runner.get('calls', [])
    lengths   = runner.get('call_lengths', [None] * len(positions))

    c1     = positions[0] if len(positions) > 0 else None
    c1_len = lengths[0]   if len(lengths) > 0 else None
    c2     = positions[1] if len(positions) > 1 else None
    c2_len = lengths[1]   if len(lengths) > 1 else None
    stretch     = positions[-2] if len(positions) >= 2 else None
    stretch_len = lengths[-2]   if len(lengths) >= 2 else None
    finish  = runner.get('finish_position')
    fin_len = runner.get('finish_lengths_behind')

    if finish is None:
        return

    # Get WPS payouts for this horse's program number
    pgm = str(runner.get('program_number', ''))
    wps = {}
    exotics = {}
    if payouts:
        wps = payouts.get('wps', {}).get(pgm, {})
        exotics = payouts.get('exotics', {})

    # Only the winner gets exotic payouts stored
    win_payout = wps.get('win')
    place_payout = wps.get('place')
    show_payout = wps.get('show')
    exacta_payout = (
        exotics.get('exacta', {}).get('payout')
        if finish == 1 else None
    )
    trifecta_payout = (
        exotics.get('trifecta', {}).get('payout')
        if finish == 1 else None
    )
    superfecta_payout = (
        exotics.get('superfecta', {}).get('payout')
        if finish == 1 else None
    )
    dd_payout = (
        exotics.get('daily_double', {}).get('payout')
        if finish == 1 else None
    )

    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO results (
                entry_id, race_id, horse_id,
                finish_position, official_finish,
                call_1_position, call_1_lengths,
                call_2_position, call_2_lengths,
                stretch_position, stretch_lengths,
                lengths_behind,
                win_payout, place_payout, show_payout,
                exacta_payout, trifecta_payout,
                superfecta_payout, daily_double_payout
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (entry_id) DO UPDATE SET
                finish_position  = EXCLUDED.finish_position,
                official_finish  = EXCLUDED.official_finish,
                call_1_position  = EXCLUDED.call_1_position,
                call_1_lengths   = EXCLUDED.call_1_lengths,
                call_2_position  = EXCLUDED.call_2_position,
                call_2_lengths   = EXCLUDED.call_2_lengths,
                stretch_position = EXCLUDED.stretch_position,
                stretch_lengths  = EXCLUDED.stretch_lengths,
                lengths_behind   = EXCLUDED.lengths_behind,
                win_payout = COALESCE(
                    EXCLUDED.win_payout, results.win_payout
                ),
                place_payout = COALESCE(
                    EXCLUDED.place_payout, results.place_payout
                ),
                show_payout = COALESCE(
                    EXCLUDED.show_payout, results.show_payout
                ),
                exacta_payout = COALESCE(
                    EXCLUDED.exacta_payout,
                    results.exacta_payout
                ),
                trifecta_payout = COALESCE(
                    EXCLUDED.trifecta_payout,
                    results.trifecta_payout
                ),
                superfecta_payout = COALESCE(
                    EXCLUDED.superfecta_payout,
                    results.superfecta_payout
                ),
                daily_double_payout = COALESCE(
                    EXCLUDED.daily_double_payout,
                    results.daily_double_payout
                )""",
            (entry_id, race_id, horse_id,
             finish, finish,
             c1, c1_len, c2, c2_len,
             stretch, stretch_len, fin_len,
             win_payout, place_payout, show_payout,
             exacta_payout, trifecta_payout,
             superfecta_payout, dd_payout)
        )


def insert_past_performance(conn, horse_id, race, runner):
    positions = runner.get('calls', [])
    lengths   = runner.get('call_lengths', [None] * len(positions))
    num_calls = race.get('num_calls', len(positions))

    # Call index mapping:
    # 4-call race: [1/4, 1/2, Str, Fin]  → calls[0]=1/4, [1]=1/2, [-2]=Str, [-1]=Fin
    # 5-call race: [1/4, 1/2, 3/4, Str, Fin] → [0]=1/4, [1]=1/2, [2]=3/4, [-2]=Str, [-1]=Fin
    c1_pos = positions[0] if len(positions) > 0 else None
    c1_len = lengths[0]   if len(lengths) > 0 else None
    c2_pos = positions[1] if len(positions) > 1 else None
    c2_len = lengths[1]   if len(lengths) > 1 else None
    c3_pos = positions[2] if len(positions) > 2 and num_calls == 5 else None
    c3_len = lengths[2]   if len(lengths) > 2 and num_calls == 5 else None
    str_pos = positions[-2] if len(positions) >= 2 else None
    str_len = lengths[-2]   if len(lengths) >= 2 else None
    finish  = runner.get('finish_position')
    fin_len = runner.get('finish_lengths_behind')

    fracs = race.get('fractions', [])
    f1 = fracs[0] if len(fracs) > 0 else None
    f2 = fracs[1] if len(fracs) > 1 else None
    f3 = fracs[2] if len(fracs) > 2 else None

    days_since = None
    if runner.get('last_raced_date') and race.get('race_date'):
        days_since = (race['race_date'] - runner['last_raced_date']).days

    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO past_performances (
                horse_id, race_date, track_code,
                race_number, distance_furlongs, surface,
                race_type, purse, claiming_price_entered,
                field_size, track_condition,
                jockey_name, weight_carried,
                lasix, lasix_first_time, blinkers_on,
                post_position, finish_position, official_finish,
                call_1_position, call_1_lengths,
                call_2_position, call_2_lengths,
                call_3_position, call_3_lengths,
                stretch_position, stretch_lengths,
                lengths_behind,
                fraction_1, fraction_2, fraction_3,
                final_time, closing_odds,
                days_since_last_race, comment
            ) VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s
            )
            ON CONFLICT (horse_id, race_date, track_code, race_number)
            DO UPDATE SET
                finish_position  = EXCLUDED.finish_position,
                official_finish  = EXCLUDED.official_finish,
                call_1_position  = EXCLUDED.call_1_position,
                call_1_lengths   = EXCLUDED.call_1_lengths,
                call_2_position  = EXCLUDED.call_2_position,
                call_2_lengths   = EXCLUDED.call_2_lengths,
                call_3_position  = EXCLUDED.call_3_position,
                call_3_lengths   = EXCLUDED.call_3_lengths,
                stretch_position = EXCLUDED.stretch_position,
                stretch_lengths  = EXCLUDED.stretch_lengths,
                lengths_behind   = EXCLUDED.lengths_behind,
                closing_odds     = EXCLUDED.closing_odds""",
            (
                horse_id, race['race_date'], race['track_code'],
                race['race_number'], race.get('distance_furlongs'),
                race.get('surface'), race.get('race_type'),
                race.get('purse'), race.get('claiming_price'),
                race.get('field_size'), race.get('track_condition'),
                runner.get('jockey_name'), runner.get('weight_carried'),
                runner.get('lasix', False),
                runner.get('lasix_first_time', False),
                runner.get('blinkers_on', False),
                runner.get('post_position'), finish, finish,
                c1_pos, c1_len,
                c2_pos, c2_len,
                c3_pos, c3_len,
                str_pos, str_len,
                fin_len,
                f1, f2, f3,
                race.get('final_time'),
                runner.get('morning_line_odds'),
                days_since, runner.get('comments'),
            )
        )


def find_trainer_for_pgm(block: str, pgm: str) -> str | None:
    """Find the trainer for a given program number in a chart block.

    Bug H fix: pdftotext line-wraps the long "Trainers: 1-A;2-B;..." list
    when many trainers are listed. The wrap can split mid-name (e.g.
    "DeLauro,Edward" → "DeLauro," then "Edward"). When we hit a
    "Trainers:" line, concatenate it with subsequent continuation lines
    until a section-header line is reached (Owners:, Footnotes, etc.),
    then search the joined string. No separator is inserted between
    lines so split-mid-name reconstructs cleanly.
    """
    lines = block.split('\n')
    section_starts = (
        'Owners:', 'Footnotes', 'Copyright', 'Past',
        'Breeder:', 'Owner:', 'Scratched',
    )
    for i, line in enumerate(lines):
        if line.startswith('Trainer:') and '-' not in line[:20]:
            return line.replace('Trainer:', '').strip()
        if line.startswith('Trainers:'):
            joined = line[len('Trainers:'):]
            for j in range(i + 1, len(lines)):
                next_line = lines[j]
                if (any(next_line.startswith(s) for s in section_starts)
                        or next_line.startswith('Trainers:')
                        or next_line.startswith('Trainer:')):
                    break
                joined += next_line
            pattern = rf'\b{re.escape(pgm)}-([^;]+)'
            m_t = re.search(pattern, joined)
            if m_t:
                raw = m_t.group(1).strip()
                parts = raw.split(',')
                if len(parts) == 2:
                    return f"{parts[1].strip()} {parts[0].strip()}"
                return raw
            return None
    return None


# ═══════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════

def process_pdf(conn, source, filename: str) -> dict:
    """Process a PDF from a file path or bytes buffer.
    filename is like 'GP_20220101.pdf'."""
    stem = filename.replace('.pdf', '')
    parts = stem.split('_')
    if len(parts) != 2:
        return {'file': filename, 'error': 'bad filename'}

    track_code = parts[0]
    try:
        file_date = datetime.strptime(parts[1], '%Y%m%d').date()
    except ValueError:
        return {'file': filename, 'error': 'bad date'}

    full_text = extract_all_text(source)
    if not full_text:
        return {'file': filename, 'error': 'no text'}

    blocks = split_into_races(full_text)

    summary = {
        'file': filename,
        'track': track_code,
        'date': str(file_date),
        'races_found': len(blocks),
        'races_loaded': 0,
        'runners_loaded': 0,
        'errors': [],
    }

    track_id = upsert_track(conn, track_code)
    if not track_id:
        summary['errors'].append(f'track {track_code} not in DB')
        return summary

    for block in blocks:
        try:
            race = parse_race_header(block, track_code, file_date)
            if not race or not race.get('distance_furlongs'):
                continue

            # Parse payout data from this race block
            payouts = parse_payout_section(block)

            race_id = insert_race(conn, race, track_id)

            for runner in race['runners']:
                horse_id = upsert_horse(conn, runner['horse_name'])
                jockey_id = upsert_jockey(conn, runner['jockey_name'])

                trainer_name = find_trainer_for_pgm(
                    block, runner['program_number']
                )
                trainer_id = upsert_trainer(
                    conn, trainer_name or 'Unknown'
                )

                with conn.cursor() as cur:
                    cur.execute(
                        """INSERT INTO entries (
                            race_id, horse_id, trainer_id,
                            jockey_id, post_position,
                            program_number, morning_line_odds,
                            weight_carried, lasix,
                            lasix_first_time, blinkers_on
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON CONFLICT (race_id, horse_id) DO UPDATE SET
                            trainer_id        = EXCLUDED.trainer_id,
                            jockey_id         = EXCLUDED.jockey_id,
                            post_position     = EXCLUDED.post_position,
                            weight_carried    = EXCLUDED.weight_carried,
                            morning_line_odds = EXCLUDED.morning_line_odds,
                            lasix             = EXCLUDED.lasix,
                            lasix_first_time  = EXCLUDED.lasix_first_time,
                            blinkers_on       = EXCLUDED.blinkers_on
                        RETURNING entry_id""",
                        (
                            race_id, horse_id, trainer_id,
                            jockey_id,
                            runner['post_position'],
                            runner['program_number'],
                            runner.get('morning_line_odds'),
                            runner.get('weight_carried'),
                            runner.get('lasix', False),
                            runner.get('lasix_first_time', False),
                            runner.get('blinkers_on', False),
                        )
                    )
                    entry_id = str(cur.fetchone()['entry_id'])

                insert_result(
                    conn, race_id, entry_id, horse_id,
                    runner, race, payouts=payouts
                )
                insert_past_performance(conn, horse_id, race, runner)
                summary['runners_loaded'] += 1

            conn.commit()
            summary['races_loaded'] += 1

        except Exception as e:
            conn.rollback()
            summary['errors'].append(
                f"Race {race.get('race_number', '?')}: {e}"
            )

    return summary


def run_from_s3(
    conn, track: str = None,
    date_from: str = None, date_to: str = None
) -> dict:
    """
    List PDFs in S3, download each, parse, load to Aurora.
    Called from ingestion Lambda handler.
    Optional date_from/date_to filter filenames
    (format: YYYYMMDD, matched against filename pattern
     like GP_20251101.pdf).
    Returns summary dict.
    """
    s3 = boto3.client('s3')

    prefix = f"{S3_PREFIX}{track}/" if track else S3_PREFIX
    logger.info(
        f"Listing PDFs in s3://{S3_BUCKET}/{prefix}"
        f" date_from={date_from} date_to={date_to}"
    )

    # List all PDF keys
    keys = []
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(
        Bucket=S3_BUCKET, Prefix=prefix
    ):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('.pdf') and obj['Size'] > 10_000:
                # Date filter: extract YYYYMMDD from filename
                fname = obj['Key'].split('/')[-1]
                import re as _re
                dm = _re.search(r'(\d{8})', fname)
                if dm and (date_from or date_to):
                    fdate = dm.group(1)
                    if date_from and fdate < date_from:
                        continue
                    if date_to and fdate > date_to:
                        continue
                keys.append(obj['Key'])

    keys.sort()
    logger.info(f"Found {len(keys)} PDFs to process")

    total_races = 0
    total_runners = 0
    total_errors = 0
    files_processed = 0

    for i, key in enumerate(keys):
        filename = key.split('/')[-1]  # GP_20220101.pdf

        try:
            response = s3.get_object(
                Bucket=S3_BUCKET, Key=key
            )
            pdf_bytes = io.BytesIO(response['Body'].read())

            summary = process_pdf(conn, pdf_bytes, filename)
            total_races += summary.get('races_loaded', 0)
            total_runners += summary.get('runners_loaded', 0)
            files_processed += 1

            if summary.get('errors'):
                total_errors += len(summary['errors'])
                for err in summary['errors']:
                    logger.warning(f"  {filename}: {err}")

        except Exception as e:
            total_errors += 1
            logger.error(f"  {filename}: {e}")

        if (i + 1) % 50 == 0 or i == len(keys) - 1:
            logger.info(
                f"  [{i+1}/{len(keys)}] "
                f"races={total_races} "
                f"runners={total_runners} "
                f"errors={total_errors}"
            )

    result = {
        'files_found': len(keys),
        'files_processed': files_processed,
        'races_loaded': total_races,
        'runners_loaded': total_runners,
        'errors': total_errors,
    }
    logger.info(f"Done: {result}")
    return result
