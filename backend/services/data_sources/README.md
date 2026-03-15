# Data Sources

Modular data source layer for Equine Equalizer.

## Current Implementation
HRNScraper — scrapes Horse Racing Nation
(entries.horseracingnation.com)
Powered by Equibase data. Free, public access.

## Swapping Data Sources
1. Create new class in this directory
2. Extend DataSourceInterface from base.py
3. Implement fetch_entries() and fetch_results()
4. Change one line in ingestion_service.py:
   self.data_source = YourNewSource()

Zero other files change.

## Future Options
- TheRacingAPIClient — paid, cleaner data
- BRISFileReader — reads purchased PP files
- EquibaseDirectScraper — deeper PP data
