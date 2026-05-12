import re
import time
import asyncio
import logging
from datetime import date, datetime
from typing import Optional
from playwright.async_api import async_playwright, Page, Browser
from .base import DataSourceInterface
from shared.constants import (
    QUALIFYING_TRACKS,
    QUALIFYING_RACE_TYPES,
    MIN_CLAIMING_PRICE
)
from shared.horse_naming import normalize_horse_name
from shared.race_typing import classify_race_type

logger = logging.getLogger(__name__)

# Track slug to code mapping (exact match only)
# HRN uses slugified track names in URLs
HRN_TRACK_MAP = {
    'churchill-downs': 'CD',
    'saratoga-race-course': 'SAR',
    'saratoga': 'SAR',
    'keeneland': 'KEE',
    'belmont-park': 'BEL',
    'belmont-at-aqueduct': 'BEL',
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

# Reverse: track code → HRN slug for direct URL construction.
# Historical default for each code; the BEL entry is date-aware via
# get_track_slug() below because the Belmont meet relocated to Aqueduct
# (HRN slug `belmont-at-aqueduct`) on 2026-04-27. For dates < 2026-04-27
# BEL races at Belmont Park (slug `belmont-park`); for dates >=
# 2026-04-27 the meet is served under `belmont-at-aqueduct`.
TRACK_SLUGS = {
    'CD':  'churchill-downs',
    'SAR': 'saratoga-race-course',
    'KEE': 'keeneland',
    'BEL': 'belmont-park',
    'SA':  'santa-anita-park',
    'GP':  'gulfstream-park',
    'DMR': 'del-mar',
    'OP':  'oaklawn-park',
    'MTH': 'monmouth-park',
    'AQU': 'aqueduct',
    'PIM': 'pimlico-race-course',
}

# BEL meet relocated to Aqueduct branded "Belmont at the Big A" on
# 2026-04-27 (AQU's prior meet ended 2026-04-26 per `tracks` table
# `last_race_date` substrate at 2026-05-12). Pre-relocation: BEL races
# at Belmont Park (slug `belmont-park`). Post-relocation: HRN serves
# the meet under `belmont-at-aqueduct`. All other tracks have static
# slugs.
BEL_AT_AQU_START = date(2026, 4, 27)


def get_track_slug(track_code: str, race_date: date) -> str:
    """Date-aware HRN URL slug for a track_code.

    Required because BEL changed slug on BEL_AT_AQU_START (meet
    physically relocated to Aqueduct). All TRACK_SLUGS callsites must
    pass race_date; pre-relocation backfill of historical BEL data
    still resolves to `belmont-park` correctly.
    """
    if track_code == 'BEL' and race_date >= BEL_AT_AQU_START:
        return 'belmont-at-aqueduct'
    return TRACK_SLUGS.get(track_code, '')

# Surface normalization
SURFACE_MAP = {
    'all weather': 'synthetic',
    'all-weather': 'synthetic',
    'synthetic': 'synthetic',
    'turf': 'turf',
    'dirt': 'dirt',
}

BASE_URL     = 'https://entries.horseracingnation.com'
PAGE_TIMEOUT = 60_000   # ms — page navigation (longer for Lambda cold start)
WAIT_TIMEOUT = 20_000   # ms — wait for selectors
REQUEST_DELAY = 1.5     # seconds between track fetches


class HRNScraper(DataSourceInterface):
    """
    Scrapes Horse Racing Nation entries and results.

    HRN is a JavaScript SPA (Next.js / Phoenix LiveView).
    Requires Playwright to render content — plain requests
    returns an empty shell page.

    Runs headless in Lambda (HRN has no bot protection / CAPTCHA).

    Page structure after JS render (same as before):
      Each race lives inside a container div containing:
        h2  — "Track Race #N, HH:MM PM"
        div.race-distance  — distance, surface, race type, claiming price
        div.race-purse     — purse amount
        div.race-restrictions — conditions
        div.race-with-results.row
          table.table-entries — entries
          results table (if race complete)
    """

    def __init__(self):
        # Browser is created per-call in async context.
        # Kept as attributes so tests can inject mocks.
        self._browser: Optional[Browser] = None

    def get_source_name(self) -> str:
        return 'Horse Racing Nation (HRN)'

    # ─────────────────────────────────────────
    # PUBLIC: sync wrappers (called by ingestion
    # service which runs in sync Lambda context)
    # ─────────────────────────────────────────

    def fetch_entries(self, race_date: date) -> list[dict]:
        return asyncio.get_event_loop().run_until_complete(
            self._fetch_entries_async(race_date)
        )

    def fetch_results(self, race_date: date) -> list[dict]:
        return asyncio.get_event_loop().run_until_complete(
            self._fetch_results_async(race_date)
        )

    # ─────────────────────────────────────────
    # PRIVATE: async implementations
    # ─────────────────────────────────────────

    async def _fetch_entries_async(
        self, race_date: date
    ) -> list[dict]:
        logger.info(
            f"HRN Playwright: fetching entries for {race_date}"
        )
        results = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--single-process",    # required in Lambda
                ],
            )
            context = await browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )

            try:
                # Step 1: fetch daily index to find qualifying tracks
                tracks = await self._fetch_daily_tracks(
                    context, race_date
                )
                qualifying = [
                    t for t in tracks
                    if t['track_code'] in QUALIFYING_TRACKS
                ]
                logger.info(
                    f"HRN: {len(tracks)} tracks today, "
                    f"{len(qualifying)} qualifying"
                )

                # Step 2: fetch each qualifying track's card
                for track in qualifying:
                    try:
                        races = await self._fetch_track_card(
                            context, track, race_date
                        )
                        results.extend(races)
                        logger.info(
                            f"HRN: {track['track_code']} — "
                            f"{len(races)} qualifying races"
                        )
                        await asyncio.sleep(REQUEST_DELAY)
                    except Exception as e:
                        logger.error(
                            f"HRN: failed {track['track_code']}: {e}",
                            exc_info=True,
                        )
            finally:
                await browser.close()

        logger.info(
            f"HRN: total qualifying races "
            f"for {race_date}: {len(results)}"
        )
        return results

    async def _fetch_results_async(
        self, race_date: date
    ) -> list[dict]:
        logger.info(
            f"HRN Playwright: fetching results for {race_date}"
        )
        results = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--single-process",
                ],
            )
            context = await browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )

            try:
                tracks = await self._fetch_daily_tracks(
                    context, race_date
                )
                qualifying = [
                    t for t in tracks
                    if t['track_code'] in QUALIFYING_TRACKS
                ]

                for track in qualifying:
                    try:
                        track_results = (
                            await self._fetch_track_results(
                                context, track, race_date
                            )
                        )
                        results.extend(track_results)
                        await asyncio.sleep(REQUEST_DELAY)
                    except Exception as e:
                        logger.error(
                            f"HRN: results failed "
                            f"{track['track_code']}: {e}"
                        )
            finally:
                await browser.close()

        return results

    # ─────────────────────────────────────────
    # PRIVATE: page-level fetch helpers
    # ─────────────────────────────────────────

    async def _fetch_daily_tracks(
        self, context, race_date: date
    ) -> list[dict]:
        """
        Fetch the daily index page and extract qualifying track links.
        """
        date_str = race_date.strftime('%Y-%m-%d')
        url = f"{BASE_URL}/entries-results/{date_str}"

        page = await context.new_page()
        try:
            await page.goto(
                url, wait_until='domcontentloaded',
                timeout=PAGE_TIMEOUT,
            )
            # Wait for track links to appear
            try:
                await page.wait_for_selector(
                    'a[href*="/entries-results/"]',
                    timeout=WAIT_TIMEOUT,
                )
            except Exception:
                pass

            html = await page.content()
        finally:
            await page.close()

        tracks = []
        seen_codes = set()

        for m in re.finditer(
            r'href=["\']([^"\']*entries-results/([a-z0-9-]+)/[^"\']*)["\']',
            html
        ):
            href  = m.group(1)
            slug  = m.group(2)

            # Skip date-only slugs
            if re.match(r'^\d{4}-\d{2}-\d{2}$', slug):
                continue

            track_code = HRN_TRACK_MAP.get(slug)
            if track_code and track_code not in seen_codes:
                seen_codes.add(track_code)
                tracks.append({
                    'track_code': track_code,
                    'track_name': HRN_TRACK_NAMES.get(
                        track_code, track_code
                    ),
                    'hrn_slug': slug,
                })

        # Fallback: if index page didn't reveal tracks,
        # try all qualifying tracks directly
        if not tracks:
            logger.warning(
                "HRN daily index returned no tracks — "
                "will attempt qualifying tracks directly"
            )
            for code in QUALIFYING_TRACKS:
                slug = get_track_slug(code, race_date)
                if slug:
                    tracks.append({
                        'track_code': code,
                        'track_name': HRN_TRACK_NAMES.get(code, code),
                        'hrn_slug': slug,
                    })

        return tracks

    async def _fetch_track_card(
        self, context, track: dict, race_date: date
    ) -> list[dict]:
        """
        Fetch full race card for one track using Playwright.
        Waits for JS to render the entry tables.
        """
        date_str = race_date.strftime('%Y-%m-%d')
        slug = track.get('hrn_slug') or get_track_slug(
            track['track_code'], race_date
        )
        url = f"{BASE_URL}/entries-results/{slug}/{date_str}"

        page = await context.new_page()
        try:
            await page.goto(
                url, wait_until='domcontentloaded',
                timeout=PAGE_TIMEOUT,
            )

            # Wait for race content — either entry tables or race headers
            for selector in [
                'table.table-entries',
                'h2:has-text("Race")',
                'div.my-5',
                '.race-distance',
            ]:
                try:
                    await page.wait_for_selector(
                        selector, timeout=WAIT_TIMEOUT
                    )
                    break
                except Exception:
                    continue

            html = await page.content()
        finally:
            await page.close()

        return self._parse_track_card_html(html, track, race_date)

    async def _fetch_track_results(
        self, context, track: dict, race_date: date
    ) -> list[dict]:
        date_str = race_date.strftime('%Y-%m-%d')
        slug = track.get('hrn_slug') or get_track_slug(
            track['track_code'], race_date
        )
        url = f"{BASE_URL}/entries-results/{slug}/{date_str}"

        page = await context.new_page()
        try:
            await page.goto(
                url, wait_until='domcontentloaded',
                timeout=PAGE_TIMEOUT,
            )
            try:
                await page.wait_for_selector(
                    'table', timeout=WAIT_TIMEOUT
                )
            except Exception:
                pass
            html = await page.content()
        finally:
            await page.close()

        return self._parse_track_results_html(
            html, track['track_code'], race_date
        )

    # ─────────────────────────────────────────
    # PRIVATE: HTML parsing (unchanged logic
    # from original requests-based scraper)
    # ─────────────────────────────────────────

    def _parse_track_card_html(
        self, html: str, track: dict, race_date: date
    ) -> list[dict]:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        races = []

        race_containers = [
            h2 for h2 in soup.find_all('h2')
            if 'race #' in h2.get_text().lower()
        ]

        for h2 in race_containers:
            try:
                container = h2.parent
                race_dict = self._parse_race_container(
                    container, h2, track, race_date
                )
                # Race-type quality filter removed — applied at inference
                # layer instead (race_repository.get_qualifying_races_by_date).
                # The track loop above already only iterates QUALIFYING_TRACKS,
                # so non-qualifying tracks remain excluded here.
                if race_dict:
                    races.append(race_dict)
            except Exception as e:
                logger.warning(
                    f"HRN: race parse failed "
                    f"{track['track_code']}: {e}"
                )

        return races

    def _parse_track_results_html(
        self, html: str, track_code: str, race_date: date
    ) -> list[dict]:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        results = []

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
                    container, track_code,
                    race_date, race_number
                )
                if result:
                    results.append(result)
            except Exception as e:
                logger.warning(
                    f"HRN: result parse failed "
                    f"{track_code}: {e}"
                )

        return results

    # ─────────────────────────────────────────────────────────
    # The following parsing methods are identical to the
    # original requests-based scraper. No logic changes.
    # ─────────────────────────────────────────────────────────

    def _parse_race_container(
        self, container, h2, track: dict, race_date: date
    ) -> Optional[dict]:
        h2_text = h2.get_text(separator=' ', strip=True)
        race_num_match = re.search(
            r'Race\s*#\s*(\d+)', h2_text, re.I
        )
        race_number = int(
            race_num_match.group(1)
        ) if race_num_match else 1

        time_match = re.search(
            r'(\d{1,2}:\d{2}\s*[AP]M)', h2_text, re.I
        )
        post_time = time_match.group(1) if time_match else None

        dist_div = container.find('div', class_='race-distance')
        dist_text = dist_div.get_text(
            separator=' ', strip=True
        ) if dist_div else ''

        distance = self._parse_distance(dist_text)
        if not distance:
            return None

        surface = self._parse_surface(dist_text)

        # HRN's race-distance div is comma-delimited:
        # "DISTANCE, SURFACE, RACE_NAME". split(',', 2) keeps commas
        # inside the race name (e.g. "$80,000 Allowance...") in the
        # third segment intact.
        parts = dist_text.split(',', 2)
        race_name = parts[2].strip() if len(parts) >= 3 else None

        purse_div = container.find('div', class_='race-purse')
        purse_text = purse_div.get_text(
            strip=True
        ) if purse_div else ''
        purse = self._parse_purse(purse_text)

        restr_div = container.find(
            'div', class_='race-restrictions'
        )
        conditions = restr_div.get_text(
            separator=' ', strip=True
        ) if restr_div else ''

        race_type = classify_race_type(
            dist_text=dist_text, race_name=race_name,
            conditions=conditions, purse=purse,
        )
        claiming_price = self._parse_claiming_price(
            dist_text, race_type
        )

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
                'race_date':          race_date,
                'race_number':        race_number,
                'race_name':          race_name,
                'distance_furlongs':  distance,
                'surface':            surface,
                'race_type':          race_type,
                'purse':              purse,
                'claiming_price':     claiming_price,
                'conditions': (
                    f"{dist_text} | {conditions}"
                )[:500],
                'post_time':          post_time,
            },
            'entries': entries,
        }

    def _parse_entries_table(self, table) -> list[dict]:
        entries = []
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if not cells:
                continue
            entry = self._parse_entry_row_by_label(cells)
            if entry:
                entries.append(entry)
        return entries

    def _parse_entry_row_by_label(
        self, cells: list
    ) -> Optional[dict]:
        cell_map = {}
        for cell in cells:
            label = cell.get('data-label', '')
            cell_map[label] = cell

        horse_cell = cell_map.get('Horse / Sire')
        if not horse_cell:
            # Fallback: scan by position if data-label missing
            # (HRN SPA may not always emit data-label)
            return self._parse_entry_row_by_position(cells)

        horse_link = horse_cell.find('a', class_='horse-link')
        if not horse_link:
            h4 = horse_cell.find('h4')
            horse_name = normalize_horse_name(
                h4.get_text(strip=True)
            ) if h4 else None
        else:
            horse_name = normalize_horse_name(
                horse_link.get_text(strip=True)
            )

        if not horse_name:
            return None

        sire_p = horse_cell.find('p')
        sire = sire_p.get_text(strip=True) if sire_p else None

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

        pgm_num = str(post_position)
        for label, cell in cell_map.items():
            if label.startswith('Program Number'):
                m = re.search(r':\s*(\w+)', label)
                if m:
                    pgm_num = m.group(1)
                else:
                    img = cell.find('img')
                    if img:
                        pgm_num = img.get(
                            'alt', str(post_position)
                        )
                break

        tj_cell = cell_map.get('Trainer / Jockey')
        trainer_name = ''
        jockey_name  = ''
        if tj_cell:
            paragraphs = tj_cell.find_all('p')
            if len(paragraphs) >= 1:
                trainer_name = paragraphs[0].get_text(strip=True)
            if len(paragraphs) >= 2:
                jockey_name  = paragraphs[1].get_text(strip=True)

        if not trainer_name:
            return None

        ml_cell = cell_map.get('Morning Line Odds')
        ml_text = ''
        if ml_cell:
            ml_p = ml_cell.find('p')
            ml_text = ml_p.get_text(
                strip=True
            ) if ml_p else ml_cell.get_text(strip=True)
        morning_line = self._parse_odds(ml_text)

        scratch_cell = cell_map.get('Scratched?')
        if scratch_cell:
            if scratch_cell.get_text(
                strip=True
            ).lower() in ['s', 'scr', 'scratched']:
                return None

        parent_row = cells[0].parent if cells else None
        if parent_row:
            if 'scratch' in ' '.join(
                parent_row.get('class', [])
            ).lower():
                return None

        return {
            'horse':   {'horse_name': horse_name, 'sire': sire, 'dam': None},
            'trainer': {'trainer_name': trainer_name},
            'jockey':  {'jockey_name': jockey_name} if jockey_name else None,
            'entry': {
                'post_position':              post_position,
                'program_number':             pgm_num,
                'morning_line_odds':          morning_line,
                'weight_carried':             None,
                'lasix':                      False,
                'lasix_first_time':           False,
                'blinkers_on':                False,
                'blinkers_first_time':        False,
                'equipment_change_from_last': False,
                'medication_change_from_last': False,
            },
            'past_performances': [],
            'workouts':          [],
        }

    def _parse_entry_row_by_position(
        self, cells: list
    ) -> Optional[dict]:
        """
        Positional fallback when data-label attributes are absent
        (HRN SPA may render without them). Assumes column order:
        PgmNo | PostPos | Horse/Sire | Trainer/Jockey | ML Odds
        """
        if len(cells) < 3:
            return None

        # Horse name is usually in the 3rd or 4th cell
        # Try to find the cell with a horse name (has an <a> or <h4>)
        horse_name = None
        trainer_name = None
        post_position = 1
        morning_line = None

        for i, cell in enumerate(cells):
            # Horse cell — has anchor or bold text
            a = cell.find('a')
            h4 = cell.find('h4')
            if (a or h4) and not horse_name:
                candidate = normalize_horse_name(
                    (a or h4).get_text(strip=True)
                )
                if candidate and len(candidate) > 2:
                    horse_name = candidate

            # Trainer name — look for first standalone text > 4 chars
            # that looks like a person's name (has comma or space)
            text = cell.get_text(strip=True)
            if (
                not trainer_name
                and horse_name          # found horse already
                and len(text) > 4
                and re.search(r'[A-Z][a-z]+', text)
                and cell != cells[2]    # skip the horse cell
            ):
                trainer_name = text

        if not horse_name:
            return None

        return {
            'horse':   {'horse_name': horse_name, 'sire': None, 'dam': None},
            'trainer': {'trainer_name': trainer_name or 'Unknown'},
            'jockey':  None,
            'entry': {
                'post_position':              post_position,
                'program_number':             str(post_position),
                'morning_line_odds':          morning_line,
                'weight_carried':             None,
                'lasix':                      False,
                'lasix_first_time':           False,
                'blinkers_on':                False,
                'blinkers_first_time':        False,
                'equipment_change_from_last': False,
                'medication_change_from_last': False,
            },
            'past_performances': [],
            'workouts':          [],
        }

    def _parse_race_result(
        self, container, track_code: str,
        race_date: date, race_number: int
    ) -> Optional[dict]:
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

        # Header-aware column resolution for win/place/show payouts.
        # Bug #28 fix (Phase 5.3.1): HRN page structure changed circa
        # 2026-04-30 (added icon column per surfaced manifestation;
        # exact column count/position not manually verified per
        # Q-T1 = unverified). Resolve target columns by <th> header
        # substring match instead of fixed positional index, so the
        # parser is structure-change-resilient.
        # Forbidden Pattern target: positional column indexing in
        # scrapers without column-header verification.
        def _resolve_col(headers, *patterns):
            """First header index whose text contains any pattern
            (case-insensitive substring match). None if no match."""
            for pat in patterns:
                for i, h in enumerate(headers):
                    if pat in h:
                        return i
            return None

        # Q-T1 V2 fix: HRN runner-table header row uses
        # <th colspan="2">Runner (Speed)</th> while data rows render
        # 5 separate <td> cells (runner-name + an unmapped spacer +
        # win + place + show). Without colspan parsing, _resolve_col
        # returns header-row indices (0..3) but data rows are indexed
        # 0..4 → off-by-one read: cells[1]='' (empty spacer) parses to
        # None for every winner row. D1 Bug #28 header-aware fix
        # produced functionally-identical indices to the original
        # positional constants because both ignore colspan.
        # Fix: parse colspan, build header→cell-start-index mapping.
        result_headers = []
        header_to_cell_start = []  # parallel array: data-cell start
        cell_cursor = 0
        for th in results_table.find_all('th'):
            text = th.get_text(strip=True).lower()
            try:
                colspan = int(th.get('colspan', 1))
            except (TypeError, ValueError):
                colspan = 1
            result_headers.append(text)
            header_to_cell_start.append(cell_cursor)
            cell_cursor += colspan

        win_idx_h   = _resolve_col(result_headers, 'win $', 'win$', 'win pay', 'win')
        place_idx_h = _resolve_col(result_headers, 'place $', 'place$', 'place pay', 'place')
        show_idx_h  = _resolve_col(result_headers, 'show $', 'show$', 'show pay', 'show')

        win_idx   = header_to_cell_start[win_idx_h]   if win_idx_h   is not None else None
        place_idx = header_to_cell_start[place_idx_h] if place_idx_h is not None else None
        show_idx  = header_to_cell_start[show_idx_h]  if show_idx_h  is not None else None

        results = []
        for i, row in enumerate(
            results_table.find_all('tr')[1:]
        ):
            cells = row.find_all('td')
            if not cells:
                continue

            horse_text = cells[0].get_text(strip=True)
            horse_name = normalize_horse_name(
                re.sub(r'\s*\(\d+\*?\)\s*$', '', horse_text)
            )

            if not horse_name:
                continue

            def parse_payout(idx):
                if idx is None or idx >= len(cells):
                    return None
                txt = cells[idx].get_text(
                    strip=True
                ).replace('$', '').replace(',', '').strip()
                try:
                    return float(txt)
                except ValueError:
                    return None

            results.append({
                'horse_name':      horse_name,
                'finish_position': i + 1,
                'official_finish': i + 1,
                'lengths_behind':  0.0,
                'final_time':      None,
                'win_payout':      parse_payout(win_idx),
                'place_payout':    parse_payout(place_idx),
                'show_payout':     parse_payout(show_idx),
                'exacta_payout':   None,
                'trifecta_payout': None,
            })

        for table in container.find_all('table'):
            headers = [
                th.get_text(strip=True).lower()
                for th in table.find_all('th')
            ]
            if any('pool' in h for h in headers):
                # Bug #28 fix (Phase 5.3.1): header-aware resolution
                # for pool name + payout columns within this table.
                # Pre-fix used positional cells[0]/cells[2]; subject
                # to same off-by-one corruption as result-dict block.
                pool_idx   = _resolve_col(headers, 'pool')
                payout_idx = _resolve_col(headers, 'payout', 'payoff', 'pays', '$')
                if pool_idx is None or payout_idx is None:
                    break
                for row in table.find_all('tr')[1:]:
                    cells = row.find_all('td')
                    if pool_idx >= len(cells) or payout_idx >= len(cells):
                        continue
                    pool = cells[pool_idx].get_text(strip=True).lower()
                    payout_txt = cells[payout_idx].get_text(
                        strip=True
                    ).replace('$', '').replace(',', '').strip()
                    try:
                        payout = float(payout_txt)
                    except ValueError:
                        continue
                    if 'exacta' in pool and results:
                        results[0]['exacta_payout'] = payout
                    elif 'trifecta' in pool and results:
                        results[0]['trifecta_payout'] = payout
                break

        also_rans = container.find('div', class_='race-also-rans')
        if also_rans:
            ar_text = re.sub(r'^.*?:\s*', '', also_rans.get_text(strip=True))
            for name in ar_text.split(','):
                name = normalize_horse_name(
                    re.sub(r'\s*\(.*?\)\s*$', '', name).strip(' .')
                )
                if name and len(name) > 1:
                    results.append({
                        'horse_name':      name,
                        'finish_position': len(results) + 1,
                        'official_finish': len(results) + 1,
                        'lengths_behind':  0.0,
                        'final_time':      None,
                        'win_payout':      None,
                        'place_payout':    None,
                        'show_payout':     None,
                        'exacta_payout':   None,
                        'trifecta_payout': None,
                    })

        if not results:
            return None

        return {
            'track_code':  track_code,
            'race_number': race_number,
            'race_date':   race_date,
            'results':     results,
        }

    # ─────────────────────────────────────────
    # PRIVATE: field parsers (unchanged)
    # ─────────────────────────────────────────

    def _parse_distance(self, text: str) -> Optional[float]:
        text_lower = text.lower()
        m = re.search(
            r'(\d+(?:\s+\d+/\d+)?|\d+\.?\d*)\s*f\b',
            text_lower
        )
        if m:
            return self._parse_fraction(m.group(1))
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

    def _parse_fraction(self, text: str) -> Optional[float]:
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
        text_lower = text.lower()
        for keyword in sorted(
            SURFACE_MAP.keys(), key=len, reverse=True
        ):
            if keyword in text_lower:
                return SURFACE_MAP[keyword]
        return 'dirt'

    def _parse_purse(self, text: str) -> Optional[int]:
        m = re.search(r'\$\s*([\d,]+)', text)
        if m:
            try:
                return int(m.group(1).replace(',', ''))
            except ValueError:
                pass
        return None

    def _parse_claiming_price(
        self, text: str, race_type: str
    ) -> Optional[int]:
        if 'claiming' not in race_type:
            return None
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

    def _parse_odds(self, text: str) -> Optional[float]:
        if not text:
            return None
        text = text.strip()
        if text.lower() in ['evens', 'even', 'e']:
            return 1.0
        m = re.search(r'(\d+)\s*/\s*(\d+)', text)
        if m:
            num = float(m.group(1))
            den = float(m.group(2))
            if den > 0:
                return round(num / den, 2)
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
        self, track_code: str, race: dict
    ) -> bool:
        if track_code not in QUALIFYING_TRACKS:
            return False
        race_type      = race.get('race_type', '')
        claiming_price = race.get('claiming_price') or 0
        if race_type in QUALIFYING_RACE_TYPES:
            return True
        if (race_type == 'claiming'
                and claiming_price >= MIN_CLAIMING_PRICE):
            return True
        return False
