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

# Track slug to code mapping (exact match only)
# HRN uses slugified track names in URLs
HRN_TRACK_MAP = {
    'churchill-downs': 'CD',
    'saratoga-race-course': 'SAR',
    'saratoga': 'SAR',
    'keeneland': 'KEE',
    'belmont-park': 'BEL',
    'belmont-at-the-big-a': 'BEL',
    'santa-anita-park': 'SA',
    'santa-anita': 'SA',
    'gulfstream-park': 'GP',
    'del-mar': 'DMR',
    'oaklawn-park': 'OP',
    'oaklawn': 'OP',
    'monmouth-park': 'MTH',
    'aqueduct': 'AQU',
    'pimlico-race-course': 'PIM',
    'pimlico': 'PIM',
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
    'all weather': 'synthetic',
    'all-weather': 'synthetic',
    'synthetic': 'synthetic',
    'turf': 'turf',
    'dirt': 'dirt',
}

# Race type normalization (longest match first)
RACE_TYPE_MAP = {
    'allowance optional claiming':
        'allowance_optional_claiming',
    'starter optional claiming':
        'allowance_optional_claiming',
    'optional claiming':
        'allowance_optional_claiming',
    'maiden special weight': 'maiden',
    'maiden claiming': 'maiden_claiming',
    'graded stakes': 'graded_stakes',
    'grade 1': 'graded_stakes',
    'grade 2': 'graded_stakes',
    'grade 3': 'graded_stakes',
    'allowance': 'allowance',
    'claiming': 'claiming',
    'maiden': 'maiden',
    'stakes': 'stakes',
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

    Page structure (per track/date):
    Each race lives inside a <div class="my-5">
    containing:
      <h2>  — track name, race number, post time
      <div class="race-distance"> — distance, surface,
                                    race type, claiming
      <div class="race-purse">   — purse amount
      <div class="race-restrictions"> — conditions
      <div class="race-with-results row"> — two cols:
        col 1: <table class="table-entries"> — entries
        col 2: results table (if race is complete)

    Entries table uses data-label attributes:
      "Post Position", "Horse / Sire",
      "Trainer / Jockey", "Morning Line Odds"
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

        Deduplicates by track_code so we only
        fetch each track's card once.
        """
        date_str = race_date.strftime('%Y-%m-%d')
        url = f"{BASE_URL}/entries-results/{date_str}"

        soup = self._fetch_page(url)
        if not soup:
            return []

        tracks = []
        seen_codes = set()

        # Find all links to track pages
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/entries-results/' not in href:
                continue
            track_code = self._extract_track_code(href)
            if track_code and track_code not in seen_codes:
                seen_codes.add(track_code)
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

        Each race lives inside a <div class="my-5">
        parent containing the h2 header, race info
        divs, and the entries/results table.
        """
        date_str = race_date.strftime('%Y-%m-%d')
        track_slug = self._get_track_slug(
            track['hrn_url']
        )
        url = (
            f"{BASE_URL}/entries-results/"
            f"{track_slug}/{date_str}"
        )

        soup = self._fetch_page(url)
        if not soup:
            return []

        races = []

        # Each race is in a <div class="my-5"> that
        # contains an h2 with "Race #N"
        # h2.string is None (mixed content), so
        # filter via get_text() instead
        race_containers = [
            h2 for h2 in soup.find_all('h2')
            if 'race #' in h2.get_text().lower()
        ]

        for h2 in race_containers:
            try:
                # The parent <div class="my-5"> is
                # the full race container
                container = h2.parent

                race_dict = self._parse_race_container(
                    container,
                    h2,
                    track,
                    race_date
                )
                if race_dict and self._is_qualifying_race(
                    track['track_code'],
                    race_dict['race']
                ):
                    races.append(race_dict)
            except Exception as e:
                logger.warning(
                    f"HRN: failed to parse race "
                    f"at {track['track_code']}: {e}"
                )

        return races

    # ─────────────────────────────────────────
    # PRIVATE: Parse race container
    # ─────────────────────────────────────────

    def _parse_race_container(
        self,
        container,
        h2,
        track: dict,
        race_date: date
    ) -> Optional[dict]:
        """
        Parse a full race container div.

        Structure:
          <h2> "Track Race #N, HH:MM PM"
          <div class="race-distance"> distance, surface
          <div class="race-purse"> purse
          <div class="race-restrictions"> conditions
          <div class="race-with-results">
            <table class="table-entries"> entries
        """
        # Extract race number from h2
        # Format: "Track Race #\nN,HH:MM PM"
        h2_text = h2.get_text(separator=' ', strip=True)
        race_num_match = re.search(
            r'Race\s*#\s*(\d+)', h2_text, re.I
        )
        race_number = int(
            race_num_match.group(1)
        ) if race_num_match else 1

        # Extract post time from h2
        time_match = re.search(
            r'(\d{1,2}:\d{2}\s*[AP]M)', h2_text, re.I
        )
        post_time = time_match.group(1) if time_match else None

        # Race distance div — contains distance,
        # surface, race type, claiming price
        dist_div = container.find(
            'div', class_='race-distance'
        )
        dist_text = dist_div.get_text(
            separator=' ', strip=True
        ) if dist_div else ''

        distance = self._parse_distance(dist_text)
        if not distance:
            return None

        surface = self._parse_surface(dist_text)
        race_type = self._parse_race_type(dist_text)
        claiming_price = self._parse_claiming_price(
            dist_text, race_type
        )

        # Purse div
        purse_div = container.find(
            'div', class_='race-purse'
        )
        purse_text = purse_div.get_text(
            strip=True
        ) if purse_div else ''
        purse = self._parse_purse(purse_text)

        # Restrictions div — race conditions
        restr_div = container.find(
            'div', class_='race-restrictions'
        )
        conditions = restr_div.get_text(
            separator=' ', strip=True
        ) if restr_div else ''

        # Entries table
        entries_table = container.find(
            'table', class_='table-entries'
        )
        entries = self._parse_entries_table(
            entries_table
        ) if entries_table else []

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
                'conditions': (
                    f"{dist_text} | {conditions}"
                )[:500],
                'post_time': post_time,
            },
            'entries': entries,
        }

    # ─────────────────────────────────────────
    # PRIVATE: Parse entries table
    # ─────────────────────────────────────────

    def _parse_entries_table(
        self, table
    ) -> list[dict]:
        """
        Parse the entries table using data-label
        attributes on <td> elements.

        HRN table structure per row:
          td[data-label^="Program Number"] — pgm #
          td[data-label="Post Position"]   — PP
          td[data-label="Horse / Sire"]    — horse/sire
          td[data-label="Trainer / Jockey"] — trainer/jock
          td[data-label="Morning Line Odds"] — ML
        """
        entries = []

        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if not cells:
                continue

            entry = self._parse_entry_row_by_label(cells)
            if entry:
                entries.append(entry)

        return entries

    # ─────────────────────────────────────────
    # PRIVATE: Parse single entry row
    # ─────────────────────────────────────────

    def _parse_entry_row_by_label(
        self,
        cells: list
    ) -> Optional[dict]:
        """
        Parse one horse entry using data-label
        attributes to identify each cell's role.
        """
        cell_map = {}
        for cell in cells:
            label = cell.get('data-label', '')
            cell_map[label] = cell

        # ── Horse name + sire ──
        horse_cell = cell_map.get('Horse / Sire')
        if not horse_cell:
            return None

        # Horse name is in <h4><a class="horse-link">
        horse_link = horse_cell.find(
            'a', class_='horse-link'
        )
        if not horse_link:
            # Fallback: try any <h4>
            h4 = horse_cell.find('h4')
            horse_name = h4.get_text(
                strip=True
            ) if h4 else None
        else:
            horse_name = horse_link.get_text(strip=True)

        if not horse_name:
            return None

        # Sire is in the <p> below
        sire_p = horse_cell.find('p')
        sire = sire_p.get_text(
            strip=True
        ) if sire_p else None

        # ── Post position ──
        pp_cell = cell_map.get('Post Position')
        pp_text = pp_cell.get_text(
            strip=True
        ) if pp_cell else ''
        try:
            post_position = int(
                re.search(r'\d+', pp_text).group()
            )
        except (AttributeError, ValueError):
            post_position = 1

        # ── Program number ──
        # data-label starts with "Program Number"
        pgm_num = str(post_position)
        for label, cell in cell_map.items():
            if label.startswith('Program Number'):
                # Extract from "Program Number: X"
                m = re.search(r':\s*(\w+)', label)
                if m:
                    pgm_num = m.group(1)
                else:
                    # Try from img alt attribute
                    img = cell.find('img')
                    if img:
                        pgm_num = img.get(
                            'alt', str(post_position)
                        )
                break

        # ── Trainer + Jockey ──
        tj_cell = cell_map.get('Trainer / Jockey')
        trainer_name = ''
        jockey_name = ''
        if tj_cell:
            paragraphs = tj_cell.find_all('p')
            if len(paragraphs) >= 1:
                trainer_name = paragraphs[0].get_text(
                    strip=True
                )
            if len(paragraphs) >= 2:
                jockey_name = paragraphs[1].get_text(
                    strip=True
                )

        if not trainer_name:
            return None

        # ── Morning line odds ──
        ml_cell = cell_map.get('Morning Line Odds')
        ml_text = ''
        if ml_cell:
            ml_p = ml_cell.find('p')
            ml_text = ml_p.get_text(
                strip=True
            ) if ml_p else ml_cell.get_text(strip=True)
        morning_line = self._parse_odds(ml_text)

        # ── Scratch check ──
        scratch_cell = cell_map.get('Scratched?')
        if scratch_cell:
            scratch_text = scratch_cell.get_text(
                strip=True
            ).lower()
            if scratch_text in ['s', 'scr', 'scratched']:
                return None

        # Check if row has scratch CSS class
        parent_row = cells[0].parent if cells else None
        if parent_row:
            row_classes = ' '.join(
                parent_row.get('class', [])
            ).lower()
            if 'scratch' in row_classes:
                return None

        return {
            'horse': {
                'horse_name': horse_name,
                'sire': sire,
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
                'program_number': pgm_num,
                'morning_line_odds': morning_line,
                'weight_carried': None,
                'lasix': False,
                'lasix_first_time': False,
                'blinkers_on': False,
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
        in the second column of race-with-results div.

        Results table headers:
          Runner(Speed) | Win | Place | Show
        Exotic payouts in a separate table:
          Pool | Finish | $2 Payout | Total Pool
        """
        date_str = race_date.strftime('%Y-%m-%d')
        track_slug = self._get_track_slug(
            track['hrn_url']
        )
        url = (
            f"{BASE_URL}/entries-results/"
            f"{track_slug}/{date_str}"
        )

        soup = self._fetch_page(url)
        if not soup:
            return []

        results = []

        # Find race containers via h2 headers
        race_headers = [
            h2 for h2 in soup.find_all('h2')
            if 'race #' in h2.get_text().lower()
        ]

        for h2 in race_headers:
            try:
                container = h2.parent
                race_num_match = re.search(
                    r'Race\s*#\s*(\d+)',
                    h2.get_text(strip=True), re.I
                )
                race_number = int(
                    race_num_match.group(1)
                ) if race_num_match else 0

                result = self._parse_race_result(
                    container,
                    track['track_code'],
                    race_date,
                    race_number
                )
                if result:
                    results.append(result)
            except Exception as e:
                logger.warning(
                    f"HRN: result parse failed "
                    f"{track['track_code']}: {e}"
                )

        return results

    def _parse_race_result(
        self,
        container,
        track_code: str,
        race_date: date,
        race_number: int
    ) -> Optional[dict]:
        """
        Parse finish order and payouts from the
        results column of a race-with-results div.

        Results table has Runner(Speed) header.
        Each row: horse name | win $ | place $ | show $
        """
        # Find the results table (has Runner header)
        results_table = None
        for table in container.find_all('table'):
            headers = [
                th.get_text(strip=True).lower()
                for th in table.find_all('th')
            ]
            if any('runner' in h for h in headers):
                results_table = table
                break

        if not results_table:
            return None

        results = []
        for i, row in enumerate(
            results_table.find_all('tr')[1:]
        ):
            cells = row.find_all('td')
            if not cells:
                continue

            # First cell: horse name (with speed fig)
            horse_text = cells[0].get_text(strip=True)
            # Remove speed figure: "Horse Name (93*)"
            horse_name = re.sub(
                r'\s*\(\d+\*?\)\s*$', '', horse_text
            ).strip()

            if not horse_name:
                continue

            # Payout cells
            def parse_payout(idx):
                if idx < len(cells):
                    txt = cells[idx].get_text(strip=True)
                    txt = txt.replace('$', '').replace(
                        ',', ''
                    ).strip()
                    try:
                        return float(txt)
                    except ValueError:
                        return None
                return None

            results.append({
                'horse_name': horse_name,
                'finish_position': i + 1,
                'official_finish': i + 1,
                'lengths_behind': 0.0,
                'final_time': None,
                'win_payout': parse_payout(1),
                'place_payout': parse_payout(2),
                'show_payout': parse_payout(3),
                'exacta_payout': None,
                'trifecta_payout': None,
            })

        # Parse exotic payouts from pool table
        for table in container.find_all('table'):
            headers = [
                th.get_text(strip=True).lower()
                for th in table.find_all('th')
            ]
            if any('pool' in h for h in headers):
                for row in table.find_all('tr')[1:]:
                    cells = row.find_all('td')
                    if len(cells) < 3:
                        continue
                    pool = cells[0].get_text(
                        strip=True
                    ).lower()
                    payout_txt = cells[2].get_text(
                        strip=True
                    ).replace('$', '').replace(
                        ',', ''
                    ).strip()
                    try:
                        payout = float(payout_txt)
                    except ValueError:
                        continue
                    if 'exacta' in pool and results:
                        results[0]['exacta_payout'] = payout
                    elif 'trifecta' in pool and results:
                        results[0]['trifecta_payout'] = payout
                break

        # Also check for also-rans (horses that
        # finished but aren't in the top 3 table)
        also_rans = container.find(
            'div', class_='race-also-rans'
        )
        if also_rans:
            ar_text = also_rans.get_text(strip=True)
            # Parse comma-separated horse names
            # after "Also Ran:" or similar prefix
            ar_text = re.sub(
                r'^.*?:\s*', '', ar_text
            )
            for name in ar_text.split(','):
                name = name.strip()
                # Remove trailing period or parenthetical
                name = re.sub(
                    r'\s*\(.*?\)\s*$', '', name
                ).strip(' .')
                if name and len(name) > 1:
                    results.append({
                        'horse_name': name,
                        'finish_position': len(results) + 1,
                        'official_finish': len(results) + 1,
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

        Uses exact slug matching only to avoid
        false positives from partial matches.
        """
        # Extract the track slug from the URL path
        m = re.search(
            r'/entries-results/([a-z0-9-]+)',
            href.lower()
        )
        if not m:
            return None

        slug = m.group(1)

        # Skip date-only slugs (YYYY-MM-DD)
        if re.match(r'^\d{4}-\d{2}-\d{2}$', slug):
            return None

        # Exact match only
        return HRN_TRACK_MAP.get(slug)

    def _get_track_slug(self, hrn_url: str) -> str:
        """Extract track slug from HRN URL path."""
        m = re.search(
            r'/entries-results/([a-z0-9-]+)',
            hrn_url.lower()
        )
        return m.group(1) if m else ''

    def _parse_distance(
        self, text: str
    ) -> Optional[float]:
        """
        Parse distance in furlongs from text.
        HRN formats: '6F', '5 1/2F', '1 1/16M',
        '1 Mile', '1 1/8 Miles', '5 f'
        """
        text_lower = text.lower()

        # Match furlongs: 6f, 5.5f, 5 1/2f, 5 1/2 f
        m = re.search(
            r'(\d+(?:\s+\d+/\d+)?|\d+\.?\d*)'
            r'\s*f\b',
            text_lower
        )
        if m:
            return self._parse_fraction(m.group(1))

        # Match miles: 1m, 1 1/16m, 1 mile,
        # 1 1/16 miles, 1 1/8miles
        m = re.search(
            r'(\d+(?:\s+\d+/\d+)?|\d+\.?\d*)'
            r'\s*m(?:ile|iles?)?\b',
            text_lower
        )
        if m:
            miles = self._parse_fraction(m.group(1))
            if miles:
                return round(miles * 8, 1)

        return None

    def _parse_fraction(
        self, text: str
    ) -> Optional[float]:
        """Parse '5 1/2' or '1 1/16' to float."""
        text = text.strip()
        parts = text.split()
        if len(parts) == 2:
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
        # Check longest matches first
        for keyword in sorted(
            SURFACE_MAP.keys(), key=len, reverse=True
        ):
            if keyword in text_lower:
                return SURFACE_MAP[keyword]
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
        # HRN format: "$17,500 Maiden Claiming"
        # or "Claiming $25,000"
        m = re.search(
            r'\$([\d,]+)\s*(?:maiden\s+)?claiming|'
            r'claiming\s*\$([\d,]+)',
            text.lower()
        )
        if m:
            val = m.group(1) or m.group(2)
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
        '5/1' -> 5.0, '8/5' -> 1.6,
        '3/2' -> 1.5, 'Evens' -> 1.0
        HRN uses slash format: '20/1', '8/5'
        """
        if not text:
            return None
        text = text.strip()
        if text.lower() in ['evens', 'even', 'e']:
            return 1.0
        # HRN uses slash: 20/1, 8/5
        m = re.search(r'(\d+)\s*/\s*(\d+)', text)
        if m:
            num = float(m.group(1))
            den = float(m.group(2))
            if den > 0:
                return round(num / den, 2)
        # Also try dash: 5-1
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
