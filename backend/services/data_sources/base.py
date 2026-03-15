from abc import ABC, abstractmethod
from datetime import date
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DataSourceInterface(ABC):
    """
    Abstract base class for all race data sources.

    Any data source (scraper, API, file reader)
    must implement this interface.

    To swap data sources:
    1. Create a new class implementing this interface
    2. Change one line in ingestion_service.py
    3. Zero other files change

    All implementations must return the same
    dict structure that store_race_card() expects:
    {
      'track': {
        'track_code': str,
        'track_name': str,
      },
      'race': {
        'race_date': date,
        'race_number': int,
        'distance_furlongs': float,
        'surface': str,
        'race_type': str,
        'purse': int,
        'claiming_price': int or None,
        'conditions': str,
        'post_time': str or None,
      },
      'entries': [
        {
          'horse': {
            'horse_name': str,
            'sire': str or None,
            'dam': str or None,
          },
          'trainer': {
            'trainer_name': str,
          },
          'jockey': {
            'jockey_name': str,
          } or None,
          'entry': {
            'post_position': int,
            'morning_line_odds': float or None,
            'lasix': bool,
            'lasix_first_time': bool,
            'blinkers_on': bool,
            'blinkers_first_time': bool,
            'equipment_change_from_last': bool,
            'medication_change_from_last': bool,
            'weight_carried': int or None,
            'program_number': str or None,
          },
          'past_performances': [],
          'workouts': [],
        }
      ]
    }
    """

    @abstractmethod
    def fetch_entries(
        self, race_date: date
    ) -> list[dict]:
        """
        Fetch all race entries for a given date.
        Returns list of race dicts matching
        store_race_card() expected structure.
        Must filter to qualifying tracks only.
        Must handle errors gracefully and return
        partial results rather than raising.
        """
        pass

    @abstractmethod
    def fetch_results(
        self, race_date: date
    ) -> list[dict]:
        """
        Fetch race results for a given date.
        Returns list of result dicts.

        Each result dict:
        {
          'track_code': str,
          'race_number': int,
          'race_date': date,
          'results': [
            {
              'horse_name': str,
              'finish_position': int,
              'official_finish': int,
              'lengths_behind': float,
              'final_time': float or None,
              'win_payout': float or None,
              'place_payout': float or None,
              'show_payout': float or None,
              'exacta_payout': float or None,
              'trifecta_payout': float or None,
            }
          ]
        }
        """
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """Human readable name for logging."""
        pass

    def fetch_past_performances(
        self,
        horse_name: str,
        track_code: str
    ) -> list[dict]:
        """
        Optional: fetch deep PP data for a horse.
        Base implementation returns empty list.
        Override in implementations that support it.
        """
        return []
