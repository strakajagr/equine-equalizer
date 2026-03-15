INSERT INTO tracks
  (track_code, track_name, location, timezone,
   surfaces, is_qualifying, min_claiming_price)
VALUES
  ('CD',  'Churchill Downs',
   'Louisville, KY',      'America/New_York',
   ARRAY['dirt','turf'],  true, 25000),

  ('SAR', 'Saratoga Race Course',
   'Saratoga Springs, NY', 'America/New_York',
   ARRAY['dirt','turf'],  true, 25000),

  ('KEE', 'Keeneland',
   'Lexington, KY',       'America/New_York',
   ARRAY['dirt','turf'],  true, 25000),

  ('BEL', 'Belmont Park',
   'Elmont, NY',          'America/New_York',
   ARRAY['dirt','turf'],  true, 25000),

  ('SA',  'Santa Anita Park',
   'Arcadia, CA',         'America/Los_Angeles',
   ARRAY['dirt','turf'],  true, 25000),

  ('GP',  'Gulfstream Park',
   'Hallandale Beach, FL', 'America/New_York',
   ARRAY['dirt','turf'],  true, 25000),

  ('DMR', 'Del Mar',
   'Del Mar, CA',         'America/Los_Angeles',
   ARRAY['dirt','turf'],  true, 25000),

  ('OP',  'Oaklawn Park',
   'Hot Springs, AR',     'America/Chicago',
   ARRAY['dirt'],         true, 25000),

  ('MTH', 'Monmouth Park',
   'Oceanport, NJ',       'America/New_York',
   ARRAY['dirt','turf'],  true, 25000),

  ('AQU', 'Aqueduct',
   'Jamaica, NY',         'America/New_York',
   ARRAY['dirt'],         true, 25000),

  ('PIM', 'Pimlico Race Course',
   'Baltimore, MD',       'America/New_York',
   ARRAY['dirt','turf'],  true, 25000)
ON CONFLICT DO NOTHING;
