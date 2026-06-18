-- ============================================================
-- Sample seed data — 15 notable natural disaster events
-- Run after 01_create_tables.sql
-- ============================================================

-- Locations
INSERT INTO locations (name, country, region, latitude, longitude) VALUES
  ('New Orleans',      'USA',         'Southeast',       29.95,  -90.07),
  ('Houston',          'USA',         'South Central',   29.76,  -95.37),
  ('Sendai',           'Japan',       'Tohoku',          38.27,  140.87),
  ('Port-au-Prince',   'Haiti',       'Caribbean',       18.54,  -72.34),
  ('Kathmandu',        'Nepal',       'South Asia',      27.70,   85.32),
  ('Dhaka',            'Bangladesh',  'South Asia',      23.81,   90.41),
  ('Galveston',        'USA',         'South Central',   29.30,  -94.80),
  ('Sichuan',          'China',       'Southwest',       30.65,  104.07),
  ('Sumatra',          'Indonesia',   'Southeast Asia',  -0.79,  102.34),
  ('Sahel',            'Ethiopia',    'East Africa',     11.00,   40.00);

-- Disaster events
INSERT INTO disaster_events (location_id, event_type, year, duration_days, name) VALUES
  (1,  'hurricane',  2005, 9,  'Hurricane Katrina'),
  (2,  'hurricane',  2017, 6,  'Hurricane Harvey'),
  (7,  'hurricane',  1900, 7,  'Galveston Hurricane'),
  (3,  'earthquake', 2011, 1,  'Tohoku Earthquake'),
  (4,  'earthquake', 2010, 1,  'Haiti Earthquake'),
  (5,  'earthquake', 2015, 1,  'Nepal Earthquake'),
  (8,  'earthquake', 2008, 1,  'Sichuan Earthquake'),
  (9,  'earthquake', 2004, 1,  'Indian Ocean Earthquake'),
  (9,  'tsunami',    2004, 3,  'Indian Ocean Tsunami'),
  (10, 'drought',    1983, 730,'Ethiopian Famine Drought'),
  (6,  'flood',      1970, 5,  'Bhola Cyclone Flood'),
  (2,  'hurricane',  2005, 4,  'Hurricane Rita'),
  (1,  'hurricane',  2012, 3,  'Hurricane Isaac'),
  (3,  'tsunami',    2011, 2,  'Tohoku Tsunami'),
  (5,  'earthquake', 1934, 1,  'Nepal-Bihar Earthquake');

-- Impact data
INSERT INTO impacts (event_id, deaths, injuries, damage_usd) VALUES
  (1,  1833,   15000,  125000000000),
  (2,  103,     780,   125000000000),
  (3,  8000,   12000,   30000000000),
  (4,  19747,  6242,   210000000000),
  (5,  316000, 300000,   8000000000),
  (6,  8964,  22000,    5150000000),
  (7,  87587,   5000,    NULL),
  (8,  69197, 374177,  147000000000),
  (9,  227898,500000,    NULL),
  (10, 0,        0,     NULL),
  (11, 500000,   0,     NULL),
  (12, 120,    500,    10000000000),
  (13, 5,       25,     2000000000),
  (14, 19629,  6152,    NULL),
  (15, 10600,   0,      NULL);

-- Hurricane details
INSERT INTO hurricane_details (event_id, category, wind_speed_mph, pressure_mb) VALUES
  (1,  5, 175, 902),
  (2,  4, 130, 937),
  (3,  4, 145, 931),
  (12, 3, 120, 948),
  (13, 1,  80, 968);

-- Earthquake details
INSERT INTO earthquake_details (event_id, magnitude, depth_km) VALUES
  (4,  9.1, 29.0),
  (5,  7.0, 13.0),
  (6,  7.8, 15.0),
  (7,  7.9, 19.0),
  (8,  9.1, 30.0),
  (15, 8.0, 11.0);

-- Drought details
INSERT INTO drought_details (event_id, palmer_index, temperature_f) VALUES
  (10, -4.0, 110);

-- Tsunami details
INSERT INTO tsunami_details (event_id, max_height_m, wave_speed_mph) VALUES
  (9,  30.0, 500),
  (14, 40.5, 500);
