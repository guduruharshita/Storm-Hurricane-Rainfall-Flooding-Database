-- Advanced aggregation and join queries
USE weather_events;

-- Total deaths and event count by type
SELECT event_type,
       SUM(deaths)  AS total_deaths,
       COUNT(*)     AS event_count,
       AVG(deaths)  AS avg_deaths_per_event
FROM impact
GROUP BY event_type
ORDER BY total_deaths DESC;

-- Economic damage per death (cost per life)
SELECT location_name, event_type, event_year,
       deaths,
       damage_usd,
       ROUND(damage_usd / NULLIF(deaths, 0)) AS damage_per_death_usd
FROM impact
WHERE deaths > 0 AND damage_usd IS NOT NULL
ORDER BY damage_per_death_usd DESC;

-- Events with both location and impact data
SELECT l.location_name, l.event_type, l.event_year,
       COALESCE(i.deaths, 0)     AS deaths,
       COALESCE(i.damage_usd, 0) AS damage_usd
FROM location l
LEFT JOIN impact i ON l.event_id = i.event_id
ORDER BY i.deaths DESC;

-- Average hurricane wind speed by category
SELECT category,
       ROUND(AVG(wind_speed_mph), 1) AS avg_wind_mph,
       COUNT(*) AS hurricane_count
FROM hurricane
GROUP BY category
ORDER BY category;

-- Events per decade
SELECT FLOOR(event_year / 10) * 10 AS decade,
       event_type,
       COUNT(*) AS occurrences
FROM location
GROUP BY decade, event_type
ORDER BY decade, occurrences DESC;
