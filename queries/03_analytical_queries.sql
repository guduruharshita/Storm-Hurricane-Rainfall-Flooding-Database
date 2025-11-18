-- Analytical views and reporting queries
USE weather_events;

-- Comprehensive event summary view
CREATE OR REPLACE VIEW event_summary AS
SELECT
    l.location_name,
    l.event_type,
    l.event_year,
    COALESCE(i.deaths, 0)       AS deaths,
    COALESCE(i.damage_usd, 0)   AS damage_usd,
    h.category                   AS hurricane_category,
    h.wind_speed_mph,
    e.magnitude                  AS earthquake_magnitude,
    t.max_height_m               AS tsunami_height_m
FROM location l
LEFT JOIN impact     i ON l.event_id = i.event_id
LEFT JOIN hurricane  h ON l.event_id = h.event_id
LEFT JOIN earthquake e ON l.event_id = e.event_id
LEFT JOIN tsunami    t ON l.event_id = t.event_id;

-- High-impact events (>1000 deaths AND >$1B damage)
SELECT location_name, event_type, event_year, deaths, damage_usd
FROM impact
WHERE deaths > 1000
  AND damage_usd > 1000000000
ORDER BY deaths DESC;

-- Severity index: weighted score combining deaths and damage
SELECT location_name, event_type, event_year,
       (deaths * 1000 + COALESCE(damage_usd / 1000000, 0)) AS severity_index
FROM impact
ORDER BY severity_index DESC;
