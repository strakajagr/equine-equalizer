import re
import time
import logging
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
from typing import Optional

logger = logging.getLogger(__name__)

HRN_BASE = 'https://www.horseracingnation.com'
REQUEST_DELAY = 1.5   # seconds between requests (polite crawl)
REQUEST_TIMEOUT = 30

# Common HRN/Equibase abbreviations that map to our codes
TRACK_CODE_MAP = {
    'CD':  'CD',  'CHD': 'CD',
    'SAR': 'SAR',
    'KEE': 'KEE',
    'BEL': 'BEL',
    'SA':  'SA',
    'GP':  'GP',  'GPW': 'GP',   # GP West counts
    'DMR': 'DMR', 'DEL': 'DMR',
    'OP':  'OP',  'OPH': 'OP',
    'MTH': 'MTH', 'MNR': 'MTH',
    'AQU': 'AQU',
    'PIM': 'PIM',
}

# Full-name fragments → code (fallback when abbreviation unknown)
TRACK_NAME_MAP = {
    'gulfstream': 'GP',
    'churchill':  'CD',
    'keeneland':  'KEE',
    'saratoga':   'SAR',
    'belmont':    'BEL',
    'santa anita': 'SA',
    'del mar':    'DMR',
    'oaklawn':    'OP',
    'monmouth':   'MTH',
    'aqueduct':   'AQU',
    'pimlico':    'PIM',
}


def horse_name_to_hrn_slug(horse_name: str) -> str:
    """
    Convert horse name to HRN URL slug.
    'Life Is Good'  → 'life-is-good'
    "O'Brien's Run" → 'obriens-run'
    """
    slug = horse_name.lower()
    slug = re.sub(r"['\u2019\u2018]", '', slug)   # apostrophes
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)       # non-alphanum
    # Bug #7b fix (2026-05-16): HRN switched separator from hyphen to underscore.
    # Verified 2026-05-02: /horse/right-to-party → 404; /horse/right_to_party → 200.
    slug = re.sub(r'[\s-]+', '_', slug.strip())     # spaces/hyphens → underscore
    slug = re.sub(r'_+', '_', slug)                 # collapse underscores
    return slug


class HRNWorkoutScraper:
    """
    Scrapes workout history from HRN horse profile pages.

    Target: https://www.horseracingnation.com/horse/{slug}

    HRN uses plain HTTP — no CAPTCHA or bot-protection.
    Rate limited to 1.5 s between requests.

    Workout table structure on profile pages:
      <table>
        <thead>
          <tr><th>Date</th><th>Track</th><th>Dist</th>
              <th>Time</th><th>Cond</th><th>Bullet</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>03/12/2026</td><td>GP</td><td>5f</td>
            <td>:59.2 (1/8)</td><td>Fast</td><td>•</td>
          </tr>
          ...
        </tbody>
      </table>

    Time format variations handled:
      ':59.2', '0:59.2', '1:00.2', '59.2', ':59.2(1/8)'
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            ),
            'Accept': (
                'text/html,application/xhtml+xml,'
                'application/xml;q=0.9,*/*;q=0.8'
            ),
            'Accept-Language': 'en-US,en;q=0.5',
        })
        self._last_request_time = 0.0

    # ─────────────────────────────────────────────────
    # PUBLIC
    # ─────────────────────────────────────────────────

    def fetch_workouts(
        self,
        horse_id: str,
        horse_name: str,
        cutoff_start: Optional[date] = None,
    ) -> list[dict]:
        """
        Fetch all workouts for a horse from HRN profile.

        cutoff_start — ignore workouts before this date (e.g. 2022-01-01)

        Returns list of dicts compatible with
        WorkoutRepository.insert_workout().
        """
        slug = horse_name_to_hrn_slug(horse_name)
        url = f"{HRN_BASE}/horse/{slug}"

        soup = self._fetch_page(url)
        if not soup:
            # Bug #7a fix (2026-05-16): elevated DEBUG→INFO so Lambda surfaces
            # diagnostic visibility (AWS runtime defaults to INFO level).
            logger.info(
                f"HRN workout: no page for {horse_name!r} (slug={slug!r}, url={url})"
            )
            return []

        workouts = self._parse_workouts(soup, horse_id, cutoff_start)
        logger.info(
            f"HRN workout: {horse_name!r} → {len(workouts)} workouts"
        )
        return workouts

    # ─────────────────────────────────────────────────
    # PRIVATE: page parsing
    # ─────────────────────────────────────────────────

    def _parse_workouts(
        self,
        soup: BeautifulSoup,
        horse_id: str,
        cutoff_start: Optional[date],
    ) -> list[dict]:
        table = self._find_workout_table(soup)
        if not table:
            return []

        thead = table.find('thead')
        if not thead:
            return []

        headers = [
            th.get_text(strip=True).lower()
            for th in thead.find_all('th')
        ]
        col_map = self._map_columns(headers)

        tbody = table.find('tbody')
        if not tbody:
            return []

        workouts = []
        for row in tbody.find_all('tr'):
            cells = row.find_all('td')
            if not cells:
                continue
            w = self._parse_row(cells, col_map, horse_id)
            if w is None:
                continue
            if cutoff_start and w['workout_date'] < cutoff_start:
                continue
            workouts.append(w)

        return workouts

    def _find_workout_table(
        self, soup: BeautifulSoup
    ) -> Optional[BeautifulSoup]:
        """
        Locate the workout table on the horse profile page.

        Strategies (in order):
          1. Heading containing "workout" → next table sibling
          2. Section/div with id or class matching "workout"
          3. Any table whose headers contain date + dist + time
        """
        # Strategy 1: heading-based
        for heading in soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6']):
            if 'workout' in heading.get_text().lower():
                for sibling in heading.find_next_siblings():
                    if sibling.name == 'table':
                        return sibling
                    if sibling.name in ('div', 'section'):
                        tbl = sibling.find('table')
                        if tbl:
                            return tbl

        # Strategy 2: id/class match
        for tag in soup.find_all(
            ['section', 'div'],
            id=re.compile(r'workout', re.I),
        ):
            tbl = tag.find('table')
            if tbl:
                return tbl

        for tag in soup.find_all(
            ['section', 'div'],
            class_=re.compile(r'workout', re.I),
        ):
            tbl = tag.find('table')
            if tbl:
                return tbl

        # Strategy 3: column-header heuristic
        for tbl in soup.find_all('table'):
            hdrs = [
                th.get_text(strip=True).lower()
                for th in tbl.find_all('th')
            ]
            hdr_str = ' '.join(hdrs)
            if (
                'date' in hdr_str
                and ('dist' in hdr_str or 'fur' in hdr_str)
                and 'time' in hdr_str
            ):
                return tbl

        return None

    def _map_columns(self, headers: list[str]) -> dict:
        """
        Map column index to semantic key based on header text.
        Returns dict: {'date': i, 'track': i, 'distance': i,
                        'time': i, 'condition': i, 'bullet': i}
        """
        col_map = {}
        for i, h in enumerate(headers):
            if 'date' in h:
                col_map.setdefault('date', i)
            elif 'track' in h or 'trk' in h:
                col_map.setdefault('track', i)
            elif 'dist' in h or 'fur' in h or 'length' in h:
                col_map.setdefault('distance', i)
            elif 'time' in h:
                col_map.setdefault('time', i)
            elif 'cond' in h or 'surface' in h or 'track cond' in h:
                col_map.setdefault('condition', i)
            elif any(
                kw in h for kw in
                ['bullet', 'rank', 'best', 'work type', 'type']
            ):
                col_map.setdefault('bullet', i)
        return col_map

    def _parse_row(
        self,
        cells: list,
        col_map: dict,
        horse_id: str,
    ) -> Optional[dict]:
        def cell_text(key: str) -> str:
            idx = col_map.get(key)
            if idx is None or idx >= len(cells):
                return ''
            return cells[idx].get_text(strip=True)

        # Date
        workout_date = self._parse_date(cell_text('date'))
        if not workout_date:
            return None

        # Track — only keep qualifying tracks
        track_raw = cell_text('track').strip()
        track_code = self._normalize_track(track_raw)
        if not track_code:
            return None

        # Distance
        distance_furlongs = self._parse_distance(
            cell_text('distance')
        )
        if not distance_furlongs:
            return None

        # Time + optional rank
        time_raw = cell_text('time')
        workout_time, rank_on_day, total_works = (
            self._parse_time_and_rank(time_raw)
        )
        if not workout_time:
            return None

        # Track condition
        condition_raw = cell_text('condition').lower().strip()
        condition = condition_raw or None

        # Bullet: cell may be '•', 'B', 'Bullet', 'Yes', or empty
        bullet_raw = cell_text('bullet').strip().lower()
        is_bullet = bullet_raw not in ('', '-', 'no', 'n')

        return {
            'horse_id': horse_id,
            'workout_date': workout_date,
            'track_code': track_code,
            'distance_furlongs': distance_furlongs,
            'workout_time': workout_time,
            'is_bullet': is_bullet,
            'track_condition': condition,
            'workout_type': None,      # HRN doesn't expose handily/breezing
            'rank_on_day': rank_on_day,
            'total_works_on_day': total_works,
            'exercise_rider': None,
        }

    # ─────────────────────────────────────────────────
    # PRIVATE: field parsers
    # ─────────────────────────────────────────────────

    def _parse_date(self, s: str) -> Optional[date]:
        for fmt in ('%m/%d/%Y', '%Y-%m-%d', '%m/%d/%y', '%b %d, %Y'):
            try:
                return datetime.strptime(s.strip(), fmt).date()
            except ValueError:
                continue
        return None

    def _normalize_track(self, raw: str) -> Optional[str]:
        """
        Normalize track string to a track code.
        We keep workouts at ALL tracks, not just qualifying ones —
        horses train wherever they're stabled, and the workout time/
        distance features don't depend on which track it was at.
        Returns None only if raw is empty/unrecognisable garbage.
        """
        upper = raw.upper().strip()
        if not upper:
            return None

        # Apply known normalizations (e.g., GPW → GP, MNR → MTH)
        code = TRACK_CODE_MAP.get(upper)
        if code:
            return code

        # Full-name fragment → known code
        lower = raw.lower()
        for fragment, mapped in TRACK_NAME_MAP.items():
            if fragment in lower:
                return mapped

        # Unknown track — keep as-is if it looks like a 2-5 letter code.
        # This preserves workouts at Fair Grounds (FG), Aqueduct (AQU),
        # Fair Hill (FH), OTC training centers, etc.
        if re.match(r'^[A-Z0-9]{2,6}$', upper):
            return upper

        return None

    def _parse_distance(self, s: str) -> Optional[float]:
        """
        Parse workout distance in furlongs.
        Handles: '5f', '5 f', '5F', '4 1/2f', '4.5f'
        """
        s = s.lower().strip()
        # Whole + fraction: '4 1/2f'
        m = re.search(r'(\d+)\s+(\d)/(\d)\s*f', s)
        if m:
            return float(m.group(1)) + int(m.group(2)) / int(m.group(3))
        # Decimal: '4.5f'
        m = re.search(r'(\d+(?:\.\d+)?)\s*f', s)
        if m:
            return float(m.group(1))
        return None

    def _parse_time_and_rank(
        self, s: str
    ) -> tuple[Optional[float], Optional[int], Optional[int]]:
        """
        Parse workout time string.

        Returns (workout_time_seconds, rank_on_day, total_works_on_day).

        Handled formats:
          ':59.2'          → 59.2
          '0:59.2'         → 59.2
          '1:00.2'         → 60.2
          ':59'            → 59.0
          '59.2'           → 59.2
          ':59.2 (1/8)'    → 59.2, rank=1, total=8
          ':59.2(1/8)'     → same
          '0:59.2 1/8'     → same
        """
        s = s.strip()
        rank_on_day: Optional[int] = None
        total_works: Optional[int] = None

        # Extract rank: (N/M) or standalone N/M
        rank_m = re.search(r'\(?\s*(\d+)\s*/\s*(\d+)\s*\)?', s)
        if rank_m:
            rank_on_day = int(rank_m.group(1))
            total_works = int(rank_m.group(2))
            s = (s[:rank_m.start()] + s[rank_m.end():]).strip()

        # ':59.2' or '0:59.2'
        m = re.fullmatch(r'0?:(\d+\.\d+)', s)
        if m:
            return float(m.group(1)), rank_on_day, total_works

        # '1:00.2' (minutes:seconds.tenths)
        m = re.fullmatch(r'(\d+):(\d+\.\d+)', s)
        if m:
            return (
                int(m.group(1)) * 60 + float(m.group(2)),
                rank_on_day, total_works,
            )

        # ':59' (no decimal)
        m = re.fullmatch(r'0?:(\d+)', s)
        if m:
            return float(m.group(1)), rank_on_day, total_works

        # '59.2' (bare seconds)
        m = re.fullmatch(r'(\d+\.\d+)', s)
        if m:
            return float(m.group(1)), rank_on_day, total_works

        return None, None, None

    # ─────────────────────────────────────────────────
    # PRIVATE: HTTP
    # ─────────────────────────────────────────────────

    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch URL with rate limiting. Returns None on 404 or error."""
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < REQUEST_DELAY:
            time.sleep(REQUEST_DELAY - elapsed)
        self._last_request_time = time.time()

        try:
            logger.debug(f"HRN workout fetch: {url}")
            resp = self.session.get(url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return BeautifulSoup(resp.text, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"HRN workout fetch failed {url}: {e}")
            return None
