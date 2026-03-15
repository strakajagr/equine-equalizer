from typing import Optional
from .base_repository import BaseRepository
from .transforms import transform_track
from models.canonical import Track


class TrackRepository(BaseRepository):

    def get_track_by_code(
        self, track_code: str
    ) -> Optional[Track]:
        """Get single track by its code e.g. 'CD'"""
        row = self._query_one(
            "SELECT * FROM tracks WHERE track_code = %s",
            (track_code,)
        )
        return transform_track(row) if row else None

    def get_qualifying_tracks(self) -> list[Track]:
        """Get all tracks where is_qualifying = true"""
        rows = self._query(
            """SELECT * FROM tracks
               WHERE is_qualifying = true
               ORDER BY track_name"""
        )
        return [transform_track(r) for r in rows]

    def get_all_tracks(self) -> list[Track]:
        rows = self._query(
            "SELECT * FROM tracks ORDER BY track_name"
        )
        return [transform_track(r) for r in rows]

    def upsert_track(self, track_data: dict) -> str:
        """
        Insert or update track.
        Returns track_id.
        """
        row = self._write_returning(
            """INSERT INTO tracks (
                 track_code, track_name, location,
                 timezone, surfaces, is_qualifying,
                 min_claiming_price
               ) VALUES (%s,%s,%s,%s,%s,%s,%s)
               ON CONFLICT (track_code) DO UPDATE SET
                 track_name = EXCLUDED.track_name,
                 location = EXCLUDED.location,
                 timezone = EXCLUDED.timezone,
                 surfaces = EXCLUDED.surfaces,
                 is_qualifying = EXCLUDED.is_qualifying,
                 min_claiming_price =
                   EXCLUDED.min_claiming_price
               RETURNING track_id""",
            (
                track_data['track_code'],
                track_data['track_name'],
                track_data.get('location'),
                track_data.get('timezone', 'America/New_York'),
                track_data.get('surfaces', []),
                track_data.get('is_qualifying', False),
                track_data.get('min_claiming_price')
            )
        )
        return str(row['track_id'])
