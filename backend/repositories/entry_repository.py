from typing import Optional
from .base_repository import BaseRepository
from .transforms import (
    transform_entry, transform_horse,
    transform_trainer, transform_jockey,
    transform_past_performance
)
from models.canonical import Entry
from shared.constants import PP_LOOKBACK_STARTS


class EntryRepository(BaseRepository):

    def get_entries_by_race(
        self, race_id: str
    ) -> list[Entry]:
        """
        Load all entries for a race.
        Each entry includes:
        - Nested Horse, Trainer, Jockey objects
        - Last PP_LOOKBACK_STARTS past performances
          ordered by race_date DESC
        Excludes scratched entries.
        Orders by post_position.
        """
        entry_rows = self._query(
            """SELECT
                 e.*,
                 h.horse_id, h.registration_id,
                 h.horse_name, h.sire, h.dam,
                 h.dam_sire, h.foaling_date,
                 h.country_of_origin, h.sex, h.color,
                 t.trainer_id, t.trainer_name,
                 t.license_number as trainer_license,
                 j.jockey_id, j.jockey_name,
                 j.license_number as jockey_license,
                 j.is_apprentice
               FROM entries e
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               WHERE e.race_id = %s
                 AND e.is_scratched = false
               ORDER BY e.post_position""",
            (race_id,)
        )

        entries = []
        for row in entry_rows:
            horse = transform_horse({
                'horse_id': row['horse_id'],
                'registration_id': row['registration_id'],
                'horse_name': row['horse_name'],
                'sire': row['sire'],
                'dam': row['dam'],
                'dam_sire': row['dam_sire'],
                'foaling_date': row['foaling_date'],
                'country_of_origin': row['country_of_origin'],
                'sex': row['sex'],
                'color': row['color']
            })

            trainer = transform_trainer({
                'trainer_id': row['trainer_id'],
                'trainer_name': row['trainer_name'],
                'license_number': row['trainer_license']
            })

            jockey = None
            if row.get('jockey_id'):
                jockey = transform_jockey({
                    'jockey_id': row['jockey_id'],
                    'jockey_name': row['jockey_name'],
                    'license_number': row['jockey_license'],
                    'is_apprentice': row['is_apprentice']
                })

            pp_rows = self._query(
                """SELECT * FROM past_performances
                   WHERE horse_id = %s
                   ORDER BY race_date DESC
                   LIMIT %s""",
                (row['horse_id'], PP_LOOKBACK_STARTS)
            )
            past_performances = [
                transform_past_performance(pp)
                for pp in pp_rows
            ]

            entries.append(
                transform_entry(
                    row, horse, trainer,
                    jockey, past_performances
                )
            )

        return entries

    def get_entry_by_id(
        self, entry_id: str
    ) -> Optional[Entry]:
        """Single entry with full nested objects."""
        row = self._query_one(
            """SELECT
                 e.*,
                 h.horse_id, h.registration_id,
                 h.horse_name, h.sire, h.dam,
                 h.dam_sire, h.foaling_date,
                 h.country_of_origin, h.sex, h.color,
                 t.trainer_id, t.trainer_name,
                 t.license_number as trainer_license,
                 j.jockey_id, j.jockey_name,
                 j.license_number as jockey_license,
                 j.is_apprentice
               FROM entries e
               JOIN horses h ON e.horse_id = h.horse_id
               JOIN trainers t ON e.trainer_id = t.trainer_id
               LEFT JOIN jockeys j
                 ON e.jockey_id = j.jockey_id
               WHERE e.entry_id = %s""",
            (entry_id,)
        )
        if not row:
            return None

        horse = transform_horse(row)
        trainer = transform_trainer({
            'trainer_id': row['trainer_id'],
            'trainer_name': row['trainer_name'],
            'license_number': row['trainer_license']
        })
        jockey = None
        if row.get('jockey_id'):
            jockey = transform_jockey({
                'jockey_id': row['jockey_id'],
                'jockey_name': row['jockey_name'],
                'license_number': row['jockey_license'],
                'is_apprentice': row['is_apprentice']
            })

        pp_rows = self._query(
            """SELECT * FROM past_performances
               WHERE horse_id = %s
               ORDER BY race_date DESC
               LIMIT %s""",
            (row['horse_id'], PP_LOOKBACK_STARTS)
        )
        past_performances = [
            transform_past_performance(pp)
            for pp in pp_rows
        ]

        return transform_entry(
            row, horse, trainer, jockey, past_performances
        )

    def insert_entry(self, entry_data: dict) -> str:
        """Insert entry. Returns entry_id."""
        row = self._write_returning(
            """INSERT INTO entries (
                 race_id, horse_id, trainer_id, jockey_id,
                 post_position, program_number,
                 morning_line_odds, weight_carried,
                 allowance_weight, apprentice_allowance,
                 lasix, lasix_first_time, bute,
                 blinkers_on, blinkers_off,
                 blinkers_first_time, tongue_tie,
                 bar_shoes, front_bandages, mud_caulks,
                 equipment_change_from_last,
                 medication_change_from_last,
                 is_scratched, is_entry
               ) VALUES (
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s
               )
               ON CONFLICT (race_id, horse_id) DO UPDATE SET
                 jockey_id = EXCLUDED.jockey_id,
                 morning_line_odds = EXCLUDED.morning_line_odds,
                 weight_carried = EXCLUDED.weight_carried,
                 lasix = EXCLUDED.lasix,
                 lasix_first_time = EXCLUDED.lasix_first_time,
                 blinkers_on = EXCLUDED.blinkers_on,
                 blinkers_off = EXCLUDED.blinkers_off,
                 blinkers_first_time =
                   EXCLUDED.blinkers_first_time,
                 equipment_change_from_last =
                   EXCLUDED.equipment_change_from_last,
                 medication_change_from_last =
                   EXCLUDED.medication_change_from_last,
                 updated_at = NOW()
               RETURNING entry_id""",
            (
                entry_data['race_id'],
                entry_data['horse_id'],
                entry_data['trainer_id'],
                entry_data.get('jockey_id'),
                entry_data['post_position'],
                entry_data.get('program_number'),
                entry_data.get('morning_line_odds'),
                entry_data.get('weight_carried'),
                entry_data.get('allowance_weight', 0),
                entry_data.get('apprentice_allowance', 0),
                entry_data.get('lasix', False),
                entry_data.get('lasix_first_time', False),
                entry_data.get('bute', False),
                entry_data.get('blinkers_on', False),
                entry_data.get('blinkers_off', False),
                entry_data.get('blinkers_first_time', False),
                entry_data.get('tongue_tie', False),
                entry_data.get('bar_shoes', False),
                entry_data.get('front_bandages', False),
                entry_data.get('mud_caulks', False),
                entry_data.get(
                    'equipment_change_from_last', False),
                entry_data.get(
                    'medication_change_from_last', False),
                entry_data.get('is_scratched', False),
                entry_data.get('is_entry', False)
            )
        )
        return str(row['entry_id'])

    def mark_scratched(
        self,
        entry_id: str,
        reason: str = None
    ) -> None:
        self._write(
            """UPDATE entries
               SET is_scratched = true,
                   scratch_reason = %s,
                   updated_at = NOW()
               WHERE entry_id = %s""",
            (reason, entry_id)
        )
