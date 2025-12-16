-- Analytical and reporting queries
USE weather_events;

-- Damage-to-death ratio (economic cost per life lost)
SELECT i.location_name, i.event_type, i.event_year,
       i.deaths, i.damage_usd,
       ROUND(i.damage_usd / NULLIF(i.deaths, 0)) AS damage_per_death
FROM impact i
WHERE i.deaths > 0 AND i.damage_usd IS NOT NULL
ORDER BY damage_per_death DESC;

-- Rolling 10-year event frequency
SELECT event_year, event_type, COUNT(*) AS events_that_year
FROM location
GROUP BY event_year, event_type
ORDER BY event_year;

-- High-impact events (deaths > 1000 AND damage > $1B)
SELECT i.location_name, i.event_type, i.event_year,
       i.deaths, i.damage_usd
FROM impact i
WHERE i.deaths > 1000 AND i.damage_usd > 1000000000
ORDER BY i.deaths DESC;

-- Cross-event correlation view
CREATE OR REPLACE VIEW event_summary AS
SELECT l.location_name, l.event_type, l.event_year,
       COALESCE(i.deaths, 0)     AS deaths,
       COALESCE(i.damage_usd, 0) AS damage_usd,
       h.category                AS hurricane_category,
       e.magnitude               AS earthquake_magnitude
FROM location l
LEFT JOIN impact     i ON l.event_id = i.event_id
LEFT JOIN hurricane  h ON l.event_id = h.event_id
LEFT JOIN earthquake e ON l.event_id = e.event_id;
