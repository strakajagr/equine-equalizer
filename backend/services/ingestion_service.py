import logging
import json
import os
from datetime import date, datetime
from typing import Optional
from shared.db import get_db
from shared.constants import (
    QUALIFYING_TRACKS,
    QUALIFYING_RACE_TYPES,
    MIN_CLAIMING_PRICE
)
from repositories.track_repository import (
    TrackRepository
)
from repositories.horse_repository import (
    HorseRepository
)
from repositories.race_repository import (
    RaceRepository
)
from repositories.entry_repository import (
    EntryRepository
)
from repositories.past_performance_repository \
    import PastPerformanceRepository
from repositories.workout_repository import (
    WorkoutRepository
)
from models.canonical import RaceCard
from services.data_sources import HRNScraper

logger = logging.getLogger(__name__)


class IngestionService:
    """
    Responsible for pulling external race data
    and storing it in the database.

    Phase 1: Parses Equibase 2023 historical dataset
    Phase 2: Daily live pull from paid data feed

    Dependency order for storage (FK constraints):
    1. tracks       (no dependencies)
    2. horses       (no dependencies)
    3. trainers     (no dependencies)
    4. jockeys      (no dependencies)
    5. races        (depends on tracks)
    6. entries      (depends on races, horses,
                     trainers, jockeys)
    7. past_performances (depends on horses)
    8. workouts     (depends on horses)

    This order is enforced in store_race_card().
    Never deviate from it.
    """

    def __init__(self, conn):
        self.conn = conn
        self.track_repo = TrackRepository(conn)
        self.horse_repo = HorseRepository(conn)
        self.race_repo = RaceRepository(conn)
        self.entry_repo = EntryRepository(conn)
        self.pp_repo = PastPerformanceRepository(conn)
        self.workout_repo = WorkoutRepository(conn)

        # Data source — swap this one line to
        # change data providers
        self.data_source = HRNScraper()

    # ═══════════════════════════════════════════
    # PUBLIC: Daily pipeline entry point
    # ═══════════════════════════════════════════

    def fetch_daily_entries(
        self, race_date: date
    ) -> dict:
        """
        Pull today's race entries and PP data
        from configured data source.
        Store races, entries, horses, trainers,
        jockeys, past performances, workouts.
        Returns summary dict.
        """
        logger.info(
            f"Fetching entries for {race_date} "
            f"via {self.data_source.get_source_name()}"
        )

        races = self.data_source.fetch_entries(
            race_date
        )

        summary = {
            'date': str(race_date),
            'source': self.data_source.get_source_name(),
            'races_fetched': len(races),
            'races_stored': 0,
            'races_skipped': 0,
            'errors': []
        }

        for race_data in races:
            try:
                race_id = self.store_race_card(race_data)
                if race_id:
                    summary['races_stored'] += 1
                else:
                    summary['races_skipped'] += 1
            except Exception as e:
                summary['errors'].append(str(e))
                logger.error(
                    f"Failed to store race: {e}",
                    exc_info=True
                )

        logger.info(
            f"Ingestion complete for {race_date}: "
            f"{summary['races_stored']} stored, "
            f"{summary['races_skipped']} skipped"
        )
        return summary

    # ═══════════════════════════════════════════
    # PUBLIC: File parsing (stubbed)
    # ═══════════════════════════════════════════

    def parse_equibase_file(
        self, file_path: str
    ) -> list[dict]:
        """
        Parse a raw Equibase data file into a list
        of race dicts ready for store_race_card().

        Each dict in the returned list must contain:
        {
          'track': { track fields },
          'race': { race fields },
          'entries': [
            {
              'horse': { horse fields },
              'trainer': { trainer fields },
              'jockey': { jockey fields },
              'entry': { entry fields },
              'past_performances': [ pp dicts ],
              'workouts': [ workout dicts ]
            }
          ]
        }

        TODO: Implement after receiving Equibase 2023
        dataset and confirming file format.
        File format is expected to be fixed-width
        chart format or CSV depending on product tier.
        """
        logger.warning(
            f"parse_equibase_file called but not yet "
            f"implemented. File: {file_path}"
        )
        return []

    # ═══════════════════════════════════════════
    # PUBLIC: Store a fully parsed race card
    # ═══════════════════════════════════════════

    def store_race_card(
        self, race_data: dict
    ) -> Optional[str]:
        """
        Persist a fully parsed race to the database.
        Handles all tables in FK dependency order.
        Returns race_id on success, None on failure.

        race_data structure:
        {
          'track': { track_code, track_name, ... },
          'race': { race_date, race_number,
                    distance_furlongs, surface,
                    race_type, ... },
          'entries': [
            {
              'horse': { horse_name, sire, dam, ... },
              'trainer': { trainer_name, ... },
              'jockey': { jockey_name, ... } or None,
              'entry': { post_position,
                         morning_line_odds,
                         lasix, ... },
              'past_performances': [ pp dicts ],
              'workouts': [ workout dicts ]
            }
          ]
        }
        """
        try:
            # Step 1: Resolve track
            track_id = self._resolve_track(
                race_data['track']
            )
            if not track_id:
                logger.warning(
                    f"Skipping race — unknown track: "
                    f"{race_data['track'].get('track_code')}"
                )
                return None

            # Step 2: Quality filter
            if not self._is_qualifying_race(
                race_data['track'].get('track_code'),
                race_data['race']
            ):
                logger.debug(
                    f"Skipping non-qualifying race: "
                    f"{race_data['track'].get('track_code')} "
                    f"R{race_data['race'].get('race_number')} "
                    f"{race_data['race'].get('race_type')}"
                )
                return None

            # Step 3: Insert race
            race_insert = dict(race_data['race'])
            race_insert['track_id'] = track_id
            race_id = self.race_repo.insert_race(
                race_insert
            )
            logger.info(
                f"Stored race {race_id}: "
                f"{race_data['track'].get('track_code')} "
                f"R{race_data['race'].get('race_number')} "
                f"{race_data['race'].get('race_date')}"
            )

            # Step 4: Process each entry
            for entry_data in race_data.get(
                'entries', []
            ):
                self._store_entry(
                    race_id,
                    entry_data
                )

            return race_id

        except Exception as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            logger.error(
                f"store_race_card failed: {e}",
                exc_info=True
            )
            return None

    # ═══════════════════════════════════════════
    # PUBLIC: Backfill historical data
    # ═══════════════════════════════════════════

    def backfill_historical_data(
        self,
        file_paths: list[str]
    ) -> dict:
        """
        Process multiple historical data files.
        Used to load the Equibase 2023 free dataset.

        Processes files in alphabetical order.
        Skips files that fail to parse.
        Continues on individual race failures.

        Returns summary dict:
        {
          'files_processed': int,
          'files_failed': int,
          'races_stored': int,
          'races_skipped': int,
          'races_failed': int,
          'horses_seen': int,
          'pp_records_stored': int,
          'errors': [ error strings ]
        }
        """
        summary = {
            'files_processed': 0,
            'files_failed': 0,
            'races_stored': 0,
            'races_skipped': 0,
            'races_failed': 0,
            'horses_seen': set(),
            'pp_records_stored': 0,
            'errors': []
        }

        sorted_files = sorted(file_paths)
        total = len(sorted_files)

        logger.info(
            f"Starting backfill: {total} files"
        )

        for i, file_path in enumerate(sorted_files):
            logger.info(
                f"Processing file {i+1}/{total}: "
                f"{os.path.basename(file_path)}"
            )

            try:
                races = self.parse_equibase_file(file_path)
                summary['files_processed'] += 1

                if not races:
                    logger.warning(
                        f"No races parsed from: {file_path}"
                    )
                    continue

                for race_data in races:
                    try:
                        race_id = self.store_race_card(race_data)

                        if race_id:
                            summary['races_stored'] += 1
                            for entry in race_data.get(
                                'entries', []
                            ):
                                name = entry.get(
                                    'horse', {}
                                ).get('horse_name')
                                if name:
                                    summary['horses_seen'].add(name)
                            for entry in race_data.get(
                                'entries', []
                            ):
                                summary['pp_records_stored'] += len(
                                    entry.get('past_performances', [])
                                )
                        else:
                            summary['races_skipped'] += 1

                    except Exception as e:
                        summary['races_failed'] += 1
                        err = (
                            f"Race failed in {file_path}: {e}"
                        )
                        summary['errors'].append(err)
                        logger.error(err)

            except Exception as e:
                summary['files_failed'] += 1
                err = f"File failed: {file_path}: {e}"
                summary['errors'].append(err)
                logger.error(err)

        # Convert set to count for JSON serialization
        summary['horses_seen'] = len(
            summary['horses_seen']
        )

        logger.info(
            f"Backfill complete: "
            f"{summary['races_stored']} races stored, "
            f"{summary['races_skipped']} skipped, "
            f"{summary['races_failed']} failed, "
            f"{summary['horses_seen']} unique horses, "
            f"{summary['pp_records_stored']} PP records"
        )

        return summary

    # ═══════════════════════════════════════════
    # PRIVATE: Entry storage helper
    # ═══════════════════════════════════════════

    def _store_entry(
        self,
        race_id: str,
        entry_data: dict
    ) -> Optional[str]:
        """
        Store a single entry and all related data.
        Handles horse, trainer, jockey, entry,
        past performances, and workouts.
        Returns entry_id on success, None on failure.

        Called by store_race_card() for each entry.
        Failures are logged but do not abort the race.
        """
        try:
            # Resolve horse (upsert by registration_id
            # or insert by name if no ID)
            horse_id = self._resolve_horse(
                entry_data['horse']
            )

            # Resolve trainer
            trainer_id = self._resolve_trainer(
                entry_data['trainer']
            )

            # Resolve jockey (optional)
            jockey_id = None
            if entry_data.get('jockey'):
                jockey_id = self._resolve_jockey(
                    entry_data['jockey']
                )

            # Insert entry
            entry_insert = dict(entry_data['entry'])
            entry_insert['race_id'] = race_id
            entry_insert['horse_id'] = horse_id
            entry_insert['trainer_id'] = trainer_id
            entry_insert['jockey_id'] = jockey_id

            entry_id = self.entry_repo.insert_entry(
                entry_insert
            )

            # Store past performances
            pps = entry_data.get('past_performances', [])
            if pps:
                pp_list = []
                for pp in pps:
                    pp_insert = dict(pp)
                    pp_insert['horse_id'] = horse_id
                    pp_list.append(pp_insert)
                stored = self.pp_repo \
                    .bulk_insert_past_performances(pp_list)
                logger.debug(
                    f"Stored {stored}/{len(pp_list)} "
                    f"PPs for horse {horse_id}"
                )

            # Store workouts
            workouts = entry_data.get('workouts', [])
            if workouts:
                workout_list = []
                for w in workouts:
                    w_insert = dict(w)
                    w_insert['horse_id'] = horse_id
                    workout_list.append(w_insert)
                stored = self.workout_repo \
                    .bulk_insert_workouts(workout_list)
                logger.debug(
                    f"Stored {stored}/{len(workout_list)} "
                    f"workouts for horse {horse_id}"
                )

            return entry_id

        except Exception as e:
            logger.error(
                f"_store_entry failed for horse "
                f"{entry_data.get('horse', {}).get('horse_name')}"
                f": {e}",
                exc_info=True
            )
            return None

    # ═══════════════════════════════════════════
    # PRIVATE: Entity resolution helpers
    # ═══════════════════════════════════════════

    def _resolve_track(
        self, track_data: dict
    ) -> Optional[str]:
        """
        Get track_id for a track code.
        Tracks are seeded — we look up, never insert.
        Returns track_id or None if not found.
        """
        track_code = track_data.get('track_code', '')
        track = self.track_repo.get_track_by_code(
            track_code
        )
        if track:
            return track.track_id
        logger.warning(
            f"Track not found in DB: {track_code}"
        )
        return None

    def _resolve_horse(
        self, horse_data: dict
    ) -> str:
        """
        Upsert horse. Returns horse_id.

        Resolution order:
        1. Try registration_id (most reliable)
        2. Try exact name match
        3. Insert as new horse

        Horses are shared across races — we never
        create duplicates. ON CONFLICT in repo
        handles the upsert safely.
        """
        reg_id = horse_data.get('registration_id')

        if reg_id:
            return self.horse_repo.upsert_horse(
                horse_data
            )

        name = horse_data.get('horse_name', '')
        existing = self.horse_repo.get_horse_by_name(
            name
        )
        if existing:
            return existing.horse_id

        return self.horse_repo.insert_horse_no_conflict(
            horse_data
        )

    def _resolve_trainer(
        self, trainer_data: dict
    ) -> str:
        """
        Upsert trainer by name.
        Returns trainer_id.
        Trainers are identified by name in Equibase data
        — no unique registration ID in PP files.
        """
        from shared.db import execute_one, execute_write_returning

        name = trainer_data.get('trainer_name', '')

        row = execute_one(
            self.conn,
            """SELECT trainer_id FROM trainers
               WHERE LOWER(trainer_name) = LOWER(%s)
               LIMIT 1""",
            (name,)
        )
        if row:
            return str(row['trainer_id'])

        row = execute_write_returning(
            self.conn,
            """INSERT INTO trainers (trainer_name, country)
               VALUES (%s, %s)
               RETURNING trainer_id""",
            (name, trainer_data.get('country', 'USA'))
        )
        return str(row['trainer_id'])

    def _resolve_jockey(
        self, jockey_data: dict
    ) -> str:
        """
        Upsert jockey by name.
        Returns jockey_id.
        Same pattern as _resolve_trainer.
        """
        from shared.db import (
            execute_one, execute_write_returning
        )

        name = jockey_data.get('jockey_name', '')

        row = execute_one(
            self.conn,
            """SELECT jockey_id FROM jockeys
               WHERE LOWER(jockey_name) = LOWER(%s)
               LIMIT 1""",
            (name,)
        )
        if row:
            return str(row['jockey_id'])

        row = execute_write_returning(
            self.conn,
            """INSERT INTO jockeys (
                 jockey_name, country, is_apprentice
               ) VALUES (%s, %s, %s)
               RETURNING jockey_id""",
            (
                name,
                jockey_data.get('country', 'USA'),
                jockey_data.get('is_apprentice', False)
            )
        )
        return str(row['jockey_id'])

    def _is_qualifying_race(
        self,
        track_code: str,
        race_data: dict
    ) -> bool:
        """
        Apply quality filter to a race.

        Qualifies if:
        - Track is in QUALIFYING_TRACKS
        - AND one of:
          a) race_type in QUALIFYING_RACE_TYPES
          b) race_type = 'claiming' AND
             claiming_price >= MIN_CLAIMING_PRICE

        This is the same filter as
        race_repository.get_qualifying_races_by_date()
        but applied at ingestion time so we never
        store races we will never use.
        """
        if track_code not in QUALIFYING_TRACKS:
            return False

        race_type = race_data.get('race_type', '')
        claiming_price = race_data.get(
            'claiming_price', 0
        ) or 0

        if race_type in QUALIFYING_RACE_TYPES:
            return True

        if (race_type == 'claiming' and
                claiming_price >= MIN_CLAIMING_PRICE):
            return True

        return False

    # ═══════════════════════════════════════════
    # PUBLIC: Utility methods
    # ═══════════════════════════════════════════

    def get_ingestion_status(
        self, race_date: date
    ) -> dict:
        """
        Check what has been ingested for a given date.
        Used for monitoring and debugging.
        Returns counts of races, entries, PPs stored.
        """
        from shared.db import execute_one

        race_count = execute_one(
            self.conn,
            """SELECT COUNT(*) as count
               FROM races r
               JOIN tracks t ON r.track_id = t.track_id
               WHERE r.race_date = %s
                 AND t.is_qualifying = true""",
            (race_date,)
        )
        entry_count = execute_one(
            self.conn,
            """SELECT COUNT(*) as count
               FROM entries e
               JOIN races r ON e.race_id = r.race_id
               WHERE r.race_date = %s""",
            (race_date,)
        )

        return {
            'date': str(race_date),
            'qualifying_races': (
                race_count['count'] if race_count else 0
            ),
            'entries': (
                entry_count['count'] if entry_count else 0
            )
        }
