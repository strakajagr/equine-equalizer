import re
import time
import logging
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
from typing import Optional
from .base import DataSourceInterface
from shared.constants import (
    QUALIFYING_TRACKS,
    QUALIFYING_RACE_TYPES,
    MIN_CLAIMING_PRICE
)

logger = logging.getLogger(__name__)

# Track name to code mapping
# HRN uses full names, we need Equibase codes
HRN_TRACK_MAP = {
    'churchill-downs': 'CD',
    'saratoga': 'SAR',
    'saratoga-race-course': 'SAR',
    'keeneland': 'KEE',
    'belmont-park': 'BEL',
    'belmont': 'BEL',
    'santa-anita': 'SA',
    'santa-anita-park': 'SA',
    'gulfstream-park': 'GP',
    'gulfstream': 'GP',
    'del-mar': 'DMR',
    'oaklawn-park': 'OP',
    'oaklawn': 'OP',
    'monmouth-park': 'MTH',
    'monmouth': 'MTH',
    'aqueduct': 'AQU',
    'pimlico': 'PIM',
    'pimlico-race-course': 'PIM',
}

HRN_TRACK_NAMES = {
    'CD':  'Churchill Downs',
    'SAR': 'Saratoga Race Course',
    'KEE': 'Keeneland',
    'BEL': 'Belmont Park',
    'SA':  'Santa Anita Park',
    'GP':  'Gulfstream Park',
    'DMR': 'Del Mar',
    'OP':  'Oaklawn Park',
    'MTH': 'Monmouth Park',
    'AQU': 'Aqueduct',
    'PIM': 'Pimlico Race Course',
}

# Surface normalization
SURFACE_MAP = {
    'dirt': 'dirt',
    'd': 'dirt',
    'turf': 'turf',
    't': 'turf',
    'synthetic': 'synthetic',
    'synth': 'synthetic',
    's': 'synthetic',
    'all weather': 'synthetic',
    'aw': 'synthetic',
}

# Race type normalization
RACE_TYPE_MAP = {
    'maiden special weight': 'maiden',
    'msw': 'maiden',
    'maiden': 'maiden',
    'maiden claiming': 'maiden_claiming',
    'mc': 'maiden_claiming',
    'claiming': 'claiming',
    'clm': 'claiming',
    'allowance': 'allowance',
    'alw': 'allowance',
    'allowance optional claiming':
        'allowance_optional_claiming',
    'aoc': 'allowance_optional_claiming',
    'optional claiming':
        'allowance_optional_claiming',
    'starter optional claiming':
        'allowance_optional_claiming',
    'stakes': 'stakes',
    'stk': 'stakes',
    'grade 1': 'graded_stakes',
    'grade 2': 'graded_stakes',
    'grade 3': 'graded_stakes',
    'graded stakes': 'graded_stakes',
    'listed': 'stakes',
}

BASE_URL = 'https://entries.horseracingnation.com'
REQUEST_DELAY = 2.0  # seconds between requests
REQUEST_TIMEOUT = 30  # seconds


class HRNScraper(DataSourceInterface):
    """
    Scrapes Horse Racing Nation entries and results.

    HRN is powered by Equibase data and provides
    free public access to entries and results for
    all North American thoroughbred tracks.

    URL structure:
    Entries: entries.horseracingnation.com/
             entries-results/{track}/{date}
    Date:    YYYY-MM-DD

    Respects rate limits with REQUEST_DELAY
    between requests to avoid overloading server.
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
        self._last_request_time = 0

    def get_source_name(self) -> str:
        return 'Horse Racing Nation (HRN)'

    # ─────────────────────────────────────────
    # PUBLIC: Fetch entries
    # ─────────────────────────────────────────

    def fetch_entries(
        self, race_date: date
    ) -> list[dict]:
        """
        Fetch all qualifying race entries for date.

        1. Fetch daily index page to find qualifying tracks
        2. For each qualifying track, fetch race card page
        3. Parse each race and its entries
        4. Return list of store_race_card() compatible dicts
        """
        logger.info(
            f"HRN: fetching entries for {race_date}"
        )
        results = []

        # Get list of tracks racing today
        tracks = self._fetch_daily_tracks(race_date)

        qualifying = [
            t for t in tracks
            if t['track_code'] in QUALIFYING_TRACKS
        ]

        logger.info(
            f"HRN: found {len(tracks)} tracks today, "
            f"{len(qualifying)} qualifying"
        )

        for track in qualifying:
            try:
                races = self._fetch_track_card(
                    track, race_date
                )
                results.extend(races)
                logger.info(
                    f"HRN: {track['track_code']} — "
                    f"{len(races)} qualifying races"
                )
            except Exception as e:
                logger.error(
                    f"HRN: failed to fetch "
                    f"{track['track_code']}: {e}",
                    exc_info=True
                )

        logger.info(
            f"HRN: total qualifying races "
            f"for {race_date}: {len(results)}"
        )
        return results

    # ─────────────────────────────────────────
    # PUBLIC: Fetch results
    # ─────────────────────────────────────────

    def fetch_results(
        self, race_date: date
    ) -> list[dict]:
        """
        Fetch race results for all qualifying tracks.
        Results are available same day after each race.
        """
        logger.info(
            f"HRN: fetching results for {race_date}"
        )
        results = []

        tracks = self._fetch_daily_tracks(race_date)
        qualifying = [
            t for t in tracks
            if t['track_code'] in QUALIFYING_TRACKS
        ]

        for track in qualifying:
            try:
                track_results = self._fetch_track_results(
                    track, race_date
                )
                results.extend(track_results)
            except Exception as e:
                logger.error(
                    f"HRN: results failed for "
                    f"{track['track_code']}: {e}",
                    exc_info=True
                )

        return results

    # ─────────────────────────────────────────
    # PRIVATE: Fetch daily track index
    # ─────────────────────────────────────────

    def _fetch_daily_tracks(
        self, race_date: date
    ) -> list[dict]:
        """
        Fetch the daily index page and extract
        list of tracks racing today.

        URL: entries.horseracingnation.com/
             entries-results/YYYY-MM-DD
        """
        date_str = race_date.strftime('%Y-%m-%d')
        url = f"{BASE_URL}/entries-results/{date_str}"

        soup = self._fetch_page(url)
        if not soup:
            return []

        tracks = []

        # Find the tracks table
        # HRN shows a table with Time | Track | Purses
        # | #/race | Dirt | Turf | Synth columns
        tables = soup.find_all('table')
        for table in tables:
            headers = table.find_all('th')
            header_text = [
                h.get_text(strip=True).lower()
                for h in headers
            ]
            if 'track' in header_text:
                rows = table.find_all('tr')[1:]
                # Skip header row
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) < 2:
                        continue
                    # Find the track link
                    track_link = row.find('a')
                    if not track_link:
                        continue
                    href = track_link.get('href', '')
                    track_code = self._extract_track_code(
                        href
                    )
                    if track_code:
                        tracks.append({
                            'track_code': track_code,
                            'track_name': HRN_TRACK_NAMES.get(
                                track_code, track_code
                            ),
                            'hrn_url': href,
                        })

        return tracks

    # ─────────────────────────────────────────
    # PRIVATE: Fetch track race card
    # ─────────────────────────────────────────

    def _fetch_track_card(
        self,
        track: dict,
        race_date: date
    ) -> list[dict]:
        """
        Fetch full race card for one track.
        Returns list of race dicts.
        """
        date_str = race_date.strftime('%Y-%m-%d')
        track_slug = track['hrn_url'].split(
            '/entries-results/'
        )[-1].split('/')[0]
        url = (
            f"{BASE_URL}/entries-results/"
            f"{track_slug}/{date_str}"
        )

        soup = self._fetch_page(url)
        if not soup:
            return []

        races = []

        # Find individual race sections
        # HRN marks each race with an anchor
        # like <div id="race-1"> or similar
        race_sections = soup.find_all(
            'div', class_=lambda c: c and 'race' in c.lower()
        )

        if not race_sections:
            # Try finding by race headers
            race_sections = soup.find_all(
                ['h2', 'h3'],
                string=re.compile(r'race\s+\d+', re.I)
            )

        for i, section in enumerate(race_sections):
            try:
                race_dict = self._parse_race_section(
                    section,
                    track,
                    race_date,
                    i + 1
                )
                if race_dict and self._is_qualifying_race(
                    track['track_code'],
                    race_dict['race']
                ):
                    races.append(race_dict)
            except Exception as e:
                logger.warning(
                    f"HRN: failed to parse race "
                    f"{i+1} at {track['track_code']}: {e}"
                )

        return races

    # ─────────────────────────────────────────
    # PRIVATE: Parse race section HTML
    # ─────────────────────────────────────────

    def _parse_race_section(
        self,
        section,
        track: dict,
        race_date: date,
        race_number: int
    ) -> Optional[dict]:
        """
        Parse a single race section from HTML.
        Extract race conditions and entry list.
        """
        text = section.get_text(separator=' ', strip=True)

        # Extract distance
        distance = self._parse_distance(text)
        if not distance:
            return None

        # Extract surface
        surface = self._parse_surface(text)

        # Extract race type
        race_type = self._parse_race_type(text)

        # Extract purse
        purse = self._parse_purse(text)

        # Extract claiming price
        claiming_price = self._parse_claiming_price(
            text, race_type
        )

        # Extract entries table
        entries = self._parse_entries_table(section)

        if not entries:
            return None

        return {
            'track': {
                'track_code': track['track_code'],
                'track_name': track['track_name'],
            },
            'race': {
                'race_date': race_date,
                'race_number': race_number,
                'distance_furlongs': distance,
                'surface': surface,
                'race_type': race_type,
                'purse': purse,
                'claiming_price': claiming_price,
                'conditions': text[:500],
                'post_time': None,
            },
            'entries': entries,
        }

    # ─────────────────────────────────────────
    # PRIVATE: Parse entries table
    # ─────────────────────────────────────────

    def _parse_entries_table(
        self, section
    ) -> list[dict]:
        """
        Find and parse the entries table in a
        race section. Returns list of entry dicts.
        """
        entries = []

        # Find tables within this section
        # or the next sibling elements
        tables = section.find_all('table')
        if not tables:
            # Look in siblings
            sibling = section.find_next_sibling()
            while sibling:
                tables = sibling.find_all('table')
                if tables:
                    break
                sibling = sibling.find_next_sibling()

        for table in tables:
            rows = table.find_all('tr')
            if len(rows) < 2:
                continue

            # Check if this looks like an entries table
            header_cells = rows[0].find_all(
                ['th', 'td']
            )
            header_text = ' '.join(
                c.get_text(strip=True).lower()
                for c in header_cells
            )

            if not any(
                kw in header_text
                for kw in ['horse', 'jockey', 'trainer', 'pp']
            ):
                continue

            # Parse column positions
            cols = self._detect_columns(header_cells)

            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 2:
                    continue
                entry = self._parse_entry_row(cells, cols)
                if entry:
                    entries.append(entry)

        return entries

    # ─────────────────────────────────────────
    # PRIVATE: Parse single entry row
    # ─────────────────────────────────────────

    def _parse_entry_row(
        self,
        cells: list,
        cols: dict
    ) -> Optional[dict]:
        """Parse one horse entry from a table row."""

        def cell_text(col_name: str) -> str:
            idx = cols.get(col_name)
            if idx is not None and idx < len(cells):
                return cells[idx].get_text(strip=True)
            return ''

        horse_name = cell_text('horse')
        if not horse_name or horse_name.lower() in [
            'horse', 'name', ''
        ]:
            return None

        # Clean horse name
        # Remove program number if prepended
        horse_name = re.sub(
            r'^\d+[a-zA-Z]?\s+', '', horse_name
        ).strip()

        # Post position
        pp_text = cell_text('pp')
        try:
            post_position = int(
                re.search(r'\d+', pp_text).group()
            ) if pp_text else 1
        except (AttributeError, ValueError):
            post_position = 1

        # Morning line
        ml_text = cell_text('ml')
        morning_line = self._parse_odds(ml_text)

        # Jockey
        jockey_name = cell_text('jockey')

        # Trainer
        trainer_name = cell_text('trainer')

        # Weight
        wgt_text = cell_text('weight')
        try:
            weight = int(
                re.search(r'\d+', wgt_text).group()
            ) if wgt_text else None
        except (AttributeError, ValueError):
            weight = None

        # Medication/equipment flags
        # Look for M/E column or parse from horse name
        me_text = cell_text('me') or cell_text('medication')
        lasix = 'L' in me_text.upper()
        lasix_first = (
            'L1' in me_text.upper() or
            'FL' in me_text.upper()
        )
        blinkers = 'B' in me_text.upper()

        if not trainer_name:
            return None

        return {
            'horse': {
                'horse_name': horse_name,
                'sire': None,
                'dam': None,
            },
            'trainer': {
                'trainer_name': trainer_name,
            },
            'jockey': {
                'jockey_name': jockey_name,
            } if jockey_name else None,
            'entry': {
                'post_position': post_position,
                'program_number': pp_text or str(
                    post_position
                ),
                'morning_line_odds': morning_line,
                'weight_carried': weight,
                'lasix': lasix,
                'lasix_first_time': lasix_first,
                'blinkers_on': blinkers,
                'blinkers_first_time': False,
                'equipment_change_from_last': False,
                'medication_change_from_last': False,
            },
            'past_performances': [],
            'workouts': [],
        }

    # ─────────────────────────────────────────
    # PRIVATE: Fetch track results
    # ─────────────────────────────────────────

    def _fetch_track_results(
        self,
        track: dict,
        race_date: date
    ) -> list[dict]:
        """
        Fetch results for all races at a track.
        HRN shows results on the same page as entries
        after races have been run.
        """
        date_str = race_date.strftime('%Y-%m-%d')
        track_slug = track['hrn_url'].split(
            '/entries-results/'
        )[-1].split('/')[0]
        url = (
            f"{BASE_URL}/entries-results/"
            f"{track_slug}/{date_str}"
        )

        soup = self._fetch_page(url)
        if not soup:
            return []

        results = []
        # Results parsing — HRN shows finish order
        # after races complete, same page structure
        # Look for result indicators in race sections
        race_sections = soup.find_all(
            'div',
            class_=lambda c: c and 'race' in c.lower()
        )

        for i, section in enumerate(race_sections):
            try:
                result = self._parse_race_result(
                    section,
                    track['track_code'],
                    race_date,
                    i + 1
                )
                if result:
                    results.append(result)
            except Exception as e:
                logger.warning(
                    f"HRN: result parse failed "
                    f"race {i+1} {track['track_code']}: {e}"
                )

        return results

    def _parse_race_result(
        self,
        section,
        track_code: str,
        race_date: date,
        race_number: int
    ) -> Optional[dict]:
        """
        Parse finish order and payouts from
        a race section that has completed.
        """
        text = section.get_text(separator=' ', strip=True)

        # Look for finish position indicators
        # HRN shows "1st", "2nd", "3rd" or
        # numbered finish order in result table
        result_rows = []

        tables = section.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) < 2:
                    continue
                row_text = ' '.join(
                    c.get_text(strip=True)
                    for c in cells
                )
                # Look for rows with finish positions
                if re.search(r'\b[1-9]\b', row_text):
                    result_rows.append(cells)

        if not result_rows:
            return None

        results = []
        for i, cells in enumerate(result_rows[:20]):
            cell_texts = [
                c.get_text(strip=True) for c in cells
            ]
            horse_name = None
            for ct in cell_texts:
                if (len(ct) > 2 and
                        not ct.isdigit() and
                        not re.match(r'^\d+[\./]\d+', ct)):
                    horse_name = ct
                    break

            if horse_name:
                results.append({
                    'horse_name': horse_name,
                    'finish_position': i + 1,
                    'official_finish': i + 1,
                    'lengths_behind': 0.0,
                    'final_time': None,
                    'win_payout': None,
                    'place_payout': None,
                    'show_payout': None,
                    'exacta_payout': None,
                    'trifecta_payout': None,
                })

        if not results:
            return None

        return {
            'track_code': track_code,
            'race_number': race_number,
            'race_date': race_date,
            'results': results,
        }

    # ─────────────────────────────────────────
    # PRIVATE: HTTP + parsing helpers
    # ─────────────────────────────────────────

    def _fetch_page(
        self, url: str
    ) -> Optional[BeautifulSoup]:
        """
        Fetch a page with rate limiting.
        Returns BeautifulSoup or None on failure.
        """
        # Rate limit
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < REQUEST_DELAY:
            time.sleep(REQUEST_DELAY - elapsed)
        self._last_request_time = time.time()

        try:
            logger.debug(f"HRN: fetching {url}")
            response = self.session.get(
                url, timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return BeautifulSoup(
                response.text, 'html.parser'
            )
        except requests.RequestException as e:
            logger.error(f"HRN: request failed {url}: {e}")
            return None

    def _extract_track_code(
        self, href: str
    ) -> Optional[str]:
        """
        Extract track code from HRN URL.
        /entries-results/gulfstream-park/2026-03-14
        -> 'GP'
        """
        parts = href.strip('/').split('/')
        # Find the track slug part
        for part in parts:
            if part in HRN_TRACK_MAP:
                return HRN_TRACK_MAP[part]
            # Try partial match
            for slug, code in HRN_TRACK_MAP.items():
                if slug in part or part in slug:
                    return code
        return None

    def _detect_columns(
        self, header_cells: list
    ) -> dict:
        """
        Detect column positions from header cells.
        Returns dict mapping column name to index.
        """
        cols = {}
        for i, cell in enumerate(header_cells):
            text = cell.get_text(strip=True).lower()
            if any(
                kw in text
                for kw in ['horse', 'name']
            ):
                cols['horse'] = i
            elif any(
                kw in text
                for kw in ['pp', 'post', '#']
            ):
                cols['pp'] = i
            elif any(
                kw in text
                for kw in ['jockey', 'jock']
            ):
                cols['jockey'] = i
            elif 'trainer' in text:
                cols['trainer'] = i
            elif any(
                kw in text
                for kw in ['wt', 'weight', 'lbs']
            ):
                cols['weight'] = i
            elif any(
                kw in text
                for kw in ['ml', 'morning', 'odds', 'ml odds']
            ):
                cols['ml'] = i
            elif any(
                kw in text
                for kw in ['m/e', 'med', 'equip']
            ):
                cols['me'] = i
        return cols

    def _parse_distance(
        self, text: str
    ) -> Optional[float]:
        """
        Parse distance in furlongs from text.
        Examples: '6f', '6 furlongs', '1 mile',
        '1 1/16 miles', '1m', '5 1/2f'
        """
        text = text.lower()

        # Match furlongs: 6f, 5.5f, 5 1/2f
        m = re.search(
            r'(\d+(?:\s+\d+/\d+)?|\d+\.?\d*)'
            r'\s*(?:f|fur|furlong)',
            text
        )
        if m:
            return self._parse_fraction(m.group(1))

        # Match miles: 1 mile, 1 1/16 miles,
        # 1m, 1 1/16m
        m = re.search(
            r'(\d+(?:\s+\d+/\d+)?|\d+\.?\d*)'
            r'\s*(?:m|mi|mile)',
            text
        )
        if m:
            miles = self._parse_fraction(m.group(1))
            if miles:
                return round(miles * 8, 1)
                # 1 mile = 8 furlongs

        return None

    def _parse_fraction(
        self, text: str
    ) -> Optional[float]:
        """Parse '5 1/2' or '1 1/16' to float."""
        text = text.strip()
        parts = text.split()
        if len(parts) == 2:
            # e.g. '5 1/2'
            whole = float(parts[0])
            num, den = parts[1].split('/')
            return whole + float(num) / float(den)
        elif '/' in text:
            num, den = text.split('/')
            return float(num) / float(den)
        else:
            try:
                return float(text)
            except ValueError:
                return None

    def _parse_surface(self, text: str) -> str:
        """Extract surface from race conditions."""
        text_lower = text.lower()
        for keyword, surface in SURFACE_MAP.items():
            if keyword in text_lower:
                return surface
        return 'dirt'  # default

    def _parse_race_type(self, text: str) -> str:
        """Normalize race type from conditions text."""
        text_lower = text.lower()
        # Check longest matches first
        for keyword in sorted(
            RACE_TYPE_MAP.keys(),
            key=len,
            reverse=True
        ):
            if keyword in text_lower:
                return RACE_TYPE_MAP[keyword]
        return 'allowance'  # safe default

    def _parse_purse(
        self, text: str
    ) -> Optional[int]:
        """Extract purse amount from text."""
        m = re.search(
            r'\$\s*([\d,]+)',
            text
        )
        if m:
            try:
                return int(m.group(1).replace(',', ''))
            except ValueError:
                pass
        return None

    def _parse_claiming_price(
        self,
        text: str,
        race_type: str
    ) -> Optional[int]:
        """Extract claiming price if claiming race."""
        if 'claiming' not in race_type:
            return None
        m = re.search(
            r'clm\s*\$?([\d,]+)|'
            r'claiming\s*\$?([\d,]+)|'
            r'\$?([\d,]+)\s*claiming',
            text.lower()
        )
        if m:
            val = next(
                g for g in m.groups() if g
            )
            try:
                return int(val.replace(',', ''))
            except ValueError:
                pass
        return None

    def _parse_odds(
        self, text: str
    ) -> Optional[float]:
        """
        Parse morning line odds to decimal.
        '5-1' -> 5.0
        '8-5' -> 1.6 (not 8/5 -- it's X to 1 basis)
        '3-2' -> 1.5
        'Evens' or '1-1' -> 1.0
        """
        if not text:
            return None
        text = text.strip()
        if text.lower() in ['evens', 'even', 'e']:
            return 1.0
        m = re.search(r'(\d+)-(\d+)', text)
        if m:
            num = float(m.group(1))
            den = float(m.group(2))
            if den > 0:
                return round(num / den, 2)
        try:
            return float(text)
        except ValueError:
            return None

    def _is_qualifying_race(
        self,
        track_code: str,
        race: dict
    ) -> bool:
        """Apply quality filter to race."""
        if track_code not in QUALIFYING_TRACKS:
            return False
        race_type = race.get('race_type', '')
        claiming_price = race.get('claiming_price') or 0
        if race_type in QUALIFYING_RACE_TYPES:
            return True
        if (race_type == 'claiming' and
                claiming_price >= MIN_CLAIMING_PRICE):
            return True
        return False
