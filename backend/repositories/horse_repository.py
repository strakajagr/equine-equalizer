from typing import Optional
from .base_repository import BaseRepository
from .transforms import transform_horse
from models.canonical import Horse


class HorseRepository(BaseRepository):

    def get_horse_by_id(
        self, horse_id: str
    ) -> Optional[Horse]:
        row = self._query_one(
            "SELECT * FROM horses WHERE horse_id = %s",
            (horse_id,)
        )
        return transform_horse(row) if row else None

    def get_horse_by_registration(
        self, registration_id: str
    ) -> Optional[Horse]:
        row = self._query_one(
            """SELECT * FROM horses
               WHERE registration_id = %s""",
            (registration_id,)
        )
        return transform_horse(row) if row else None

    def get_horse_by_name(
        self, name: str
    ) -> Optional[Horse]:
        """
        Case-insensitive name search.
        Returns first match or None.
        """
        row = self._query_one(
            """SELECT * FROM horses
               WHERE LOWER(horse_name) = LOWER(%s)
               LIMIT 1""",
            (name,)
        )
        return transform_horse(row) if row else None

    def search_horses_by_name(
        self, name: str
    ) -> list[Horse]:
        """
        Partial name search using pg_trgm similarity.
        Returns up to 10 matches ordered by similarity.
        """
        rows = self._query(
            """SELECT * FROM horses
               WHERE horse_name ILIKE %s
               ORDER BY horse_name
               LIMIT 10""",
            (f'%{name}%',)
        )
        return [transform_horse(r) for r in rows]

    def upsert_horse(self, horse_data: dict) -> str:
        """
        Insert or update horse by registration_id.
        If no registration_id, insert only.
        Returns horse_id.
        """
        row = self._write_returning(
            """INSERT INTO horses (
                 registration_id, horse_name, sire, dam,
                 dam_sire, foaling_date, country_of_origin,
                 sex, color
               ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
               ON CONFLICT (registration_id) DO UPDATE SET
                 horse_name = EXCLUDED.horse_name,
                 sire = EXCLUDED.sire,
                 dam = EXCLUDED.dam,
                 dam_sire = EXCLUDED.dam_sire,
                 foaling_date = EXCLUDED.foaling_date,
                 updated_at = NOW()
               RETURNING horse_id""",
            (
                horse_data.get('registration_id'),
                horse_data['horse_name'],
                horse_data.get('sire'),
                horse_data.get('dam'),
                horse_data.get('dam_sire'),
                horse_data.get('foaling_date'),
                horse_data.get('country_of_origin', 'USA'),
                horse_data.get('sex'),
                horse_data.get('color')
            )
        )
        return str(row['horse_id'])

    def insert_horse_no_conflict(
        self, horse_data: dict
    ) -> str:
        """
        Insert horse when no registration_id available.
        Used for horses without Equibase IDs.
        Returns horse_id.
        """
        row = self._write_returning(
            """INSERT INTO horses (
                 horse_name, sire, dam, dam_sire,
                 foaling_date, country_of_origin, sex, color
               ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
               RETURNING horse_id""",
            (
                horse_data['horse_name'],
                horse_data.get('sire'),
                horse_data.get('dam'),
                horse_data.get('dam_sire'),
                horse_data.get('foaling_date'),
                horse_data.get('country_of_origin', 'USA'),
                horse_data.get('sex'),
                horse_data.get('color')
            )
        )
        return str(row['horse_id'])
