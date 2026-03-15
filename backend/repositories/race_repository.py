from typing import Optional
from datetime import date
from .base_repository import BaseRepository
from .transforms import transform_race, transform_track
from models.canonical import Race, RaceCard
from shared.constants import (
    QUALIFYING_TRACKS,
    QUALIFYING_RACE_TYPES,
    MIN_CLAIMING_PRICE
)


class RaceRepository(BaseRepository):

    def get_race_by_id(
        self, race_id: str
    ) -> Optional[Race]:
        """
        Get single race with nested track.
        Does not load entries — use entry_repository
        separately when entries are needed.
        """
        row = self._query_one(
            """SELECT r.*,
                      t.track_code, t.track_name,
                      t.location, t.timezone,
                      t.surfaces, t.is_qualifying,
                      t.min_claiming_price
               FROM races r
               JOIN tracks t ON r.track_id = t.track_id
               WHERE r.race_id = %s""",
            (race_id,)
        )
        if not row:
            return None
        track = transform_track({
            'track_id': row['track_id'],
            'track_code': row['track_code'],
            'track_name': row['track_name'],
            'location': row['location'],
            'timezone': row['timezone'],
            'surfaces': row['surfaces'],
            'is_qualifying': row['is_qualifying'],
            'min_claiming_price': row['min_claiming_price']
        })
        return transform_race(row, track, entries=[])

    def get_races_by_date(
        self, race_date: date
    ) -> list[Race]:
        """All races on a given date across all tracks."""
        rows = self._query(
            """SELECT r.*,
                      t.track_code, t.track_name,
                      t.location, t.timezone,
                      t.surfaces, t.is_qualifying,
                      t.min_claiming_price
               FROM races r
               JOIN tracks t ON r.track_id = t.track_id
               WHERE r.race_date = %s
               ORDER BY t.track_code, r.race_number""",
            (race_date,)
        )
        return self._build_race_list(rows)

    def get_qualifying_races_by_date(
        self, race_date: date
    ) -> list[Race]:
        """
        Qualifying races only:
        - Track must be in QUALIFYING_TRACKS
        - Race type must be in QUALIFYING_RACE_TYPES
          OR claiming_price >= MIN_CLAIMING_PRICE
        - Ordered by track then race number
        """
        rows = self._query(
            """SELECT r.*,
                      t.track_code, t.track_name,
                      t.location, t.timezone,
                      t.surfaces, t.is_qualifying,
                      t.min_claiming_price
               FROM races r
               JOIN tracks t ON r.track_id = t.track_id
               WHERE t.track_code = ANY(%s)
                 AND t.is_qualifying = true
                 AND (
                   r.race_type = ANY(%s)
                   OR (
                     r.race_type = 'claiming'
                     AND r.claiming_price >= %s
                   )
                 )
                 AND r.race_date = %s
               ORDER BY t.track_code, r.race_number""",
            (
                QUALIFYING_TRACKS,
                QUALIFYING_RACE_TYPES,
                MIN_CLAIMING_PRICE,
                race_date
            )
        )
        return self._build_race_list(rows)

    def get_race_card(
        self,
        track_code: str,
        race_date: date
    ) -> Optional[RaceCard]:
        """
        Full race card for one track on one date.
        Returns RaceCard with nested Track.
        Entries loaded separately by entry_repository.
        """
        rows = self._query(
            """SELECT r.*,
                      t.track_code, t.track_name,
                      t.location, t.timezone,
                      t.surfaces, t.is_qualifying,
                      t.min_claiming_price
               FROM races r
               JOIN tracks t ON r.track_id = t.track_id
               WHERE t.track_code = %s
                 AND r.race_date = %s
               ORDER BY r.race_number""",
            (track_code, race_date)
        )
        if not rows:
            return None
        track = transform_track({
            'track_id': rows[0]['track_id'],
            'track_code': rows[0]['track_code'],
            'track_name': rows[0]['track_name'],
            'location': rows[0]['location'],
            'timezone': rows[0]['timezone'],
            'surfaces': rows[0]['surfaces'],
            'is_qualifying': rows[0]['is_qualifying'],
            'min_claiming_price': rows[0]['min_claiming_price']
        })
        races = self._build_race_list(rows)
        return RaceCard(
            track=track,
            race_date=race_date,
            races=races
        )

    def insert_race(self, race_data: dict) -> str:
        """Insert race. Returns race_id."""
        row = self._write_returning(
            """INSERT INTO races (
                 track_id, race_date, race_number,
                 post_time, distance_furlongs, surface,
                 race_type, grade, race_name, purse,
                 claiming_price, conditions, field_size,
                 rail_position, track_condition,
                 moisture_level, track_variant,
                 going_stick_reading, temperature,
                 weather_conditions, wind_speed,
                 wind_direction, off_turf,
                 equibase_race_id
               ) VALUES (
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s
               )
               ON CONFLICT (track_id, race_date, race_number)
               DO UPDATE SET
                 post_time = EXCLUDED.post_time,
                 field_size = EXCLUDED.field_size,
                 track_condition = EXCLUDED.track_condition,
                 moisture_level = EXCLUDED.moisture_level,
                 track_variant = EXCLUDED.track_variant,
                 temperature = EXCLUDED.temperature,
                 weather_conditions =
                   EXCLUDED.weather_conditions,
                 wind_speed = EXCLUDED.wind_speed,
                 wind_direction = EXCLUDED.wind_direction,
                 off_turf = EXCLUDED.off_turf
               RETURNING race_id""",
            (
                race_data['track_id'],
                race_data['race_date'],
                race_data['race_number'],
                self._parse_post_time(
                    race_data.get('post_time'),
                    race_data.get('race_date')
                ),
                race_data['distance_furlongs'],
                race_data['surface'],
                race_data['race_type'],
                race_data.get('grade'),
                race_data.get('race_name'),
                race_data.get('purse'),
                race_data.get('claiming_price'),
                race_data.get('conditions'),
                race_data.get('field_size'),
                race_data.get('rail_position'),
                race_data.get('track_condition'),
                race_data.get('moisture_level'),
                race_data.get('track_variant'),
                race_data.get('going_stick_reading'),
                race_data.get('temperature'),
                race_data.get('weather_conditions'),
                race_data.get('wind_speed'),
                race_data.get('wind_direction'),
                race_data.get('off_turf', False),
                race_data.get('equibase_race_id')
            )
        )
        return str(row['race_id'])

    def update_track_condition(
        self,
        race_id: str,
        condition: str,
        moisture_level: str = None
    ) -> None:
        self._write(
            """UPDATE races
               SET track_condition = %s,
                   moisture_level = %s
               WHERE race_id = %s""",
            (condition, moisture_level, race_id)
        )

    def _parse_post_time(self, post_time_str, race_date):
        """
        Convert bare time string '1:33 PM' to datetime
        using race_date for the date component.
        Returns None if post_time_str is None or unparseable.
        """
        if not post_time_str:
            return None
        if hasattr(post_time_str, 'hour'):
            # Already a time or datetime object
            return post_time_str
        try:
            from datetime import datetime
            t = datetime.strptime(
                str(post_time_str).strip(), '%I:%M %p'
            ).time()
            if race_date:
                d = race_date if hasattr(race_date, 'year') \
                    else date.fromisoformat(str(race_date))
                return datetime(
                    d.year, d.month, d.day,
                    t.hour, t.minute, t.second
                )
            return t
        except (ValueError, AttributeError):
            return None

    def _build_race_list(
        self, rows: list[dict]
    ) -> list[Race]:
        """
        Private helper. Builds Race objects from
        joined query rows. Handles track extraction
        from joined columns. No entries loaded here.
        """
        races = []
        for row in rows:
            track = transform_track({
                'track_id': row['track_id'],
                'track_code': row['track_code'],
                'track_name': row['track_name'],
                'location': row['location'],
                'timezone': row['timezone'],
                'surfaces': row['surfaces'],
                'is_qualifying': row['is_qualifying'],
                'min_claiming_price': row['min_claiming_price']
            })
            races.append(
                transform_race(row, track, entries=[])
            )
        return races
