-- Sample seed data — 5 major historical events
USE weather_events;

INSERT INTO location (event_id, location_name, event_type, event_year, duration_days) VALUES
(1, 'Gulf of Mexico',    'Hurricane',   2005, 14),
(2, 'Sumatra, Indonesia','Earthquake',  2004,  1),
(3, 'Sahel, Africa',     'Drought',     2010, 365),
(4, 'Bangladesh',        'Flood',       2017,  45),
(5, 'Pacific Coast',     'Tsunami',     2011,   1);

INSERT INTO hurricane (event_id, location_id, hurricane_name, wind_speed_mph, temperature_f, category) VALUES
(1, 1, 'Katrina', 175, 82, 5);

INSERT INTO earthquake (event_id, location_id, duration, magnitude, depth_km) VALUES
(2, 2, '8-10 minutes', 9.1, 30.0);

INSERT INTO drought (event_id, location_id, temperature_f, palmer_index) VALUES
(3, 3, 110, -4.5);

INSERT INTO impact (event_id, location_id, location_name, event_type, event_year, deaths, injuries, damage_usd) VALUES
(1, 1, 'New Orleans, LA',  'Hurricane', 2005, 1833,   705000, 125000000000),
(2, 2, 'Indian Ocean',     'Tsunami',   2004, 227898, 500000,  10000000000),
(4, 4, 'Dhaka, Bangladesh','Flood',     2017, 156,      2400,   3000000000);

INSERT INTO tsunami (event_id, location_id, wave_speed_mph, max_height_m, temperature_f) VALUES
(5, 5, 500, 40.0, 65);
