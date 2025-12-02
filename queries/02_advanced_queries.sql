-- Advanced join and aggregation queries
USE weather_events;

-- Total deaths by event type
SELECT event_type, SUM(deaths) AS total_deaths, COUNT(*) AS event_count
FROM impact
GROUP BY event_type
ORDER BY total_deaths DESC;

-- Events with both impact data and location info
SELECT l.location_name, l.event_type, l.event_year,
       i.deaths, i.damage_usd
FROM location l
LEFT JOIN impact i ON l.event_id = i.event_id
WHERE i.deaths > 100
ORDER BY i.deaths DESC;

-- Average wind speed by hurricane category
SELECT category, AVG(wind_speed_mph) AS avg_wind, COUNT(*) AS count
FROM hurricane
GROUP BY category
ORDER BY category;

-- Events by decade
SELECT FLOOR(event_year / 10) * 10 AS decade,
       event_type,
       COUNT(*) AS occurrences
FROM location
GROUP BY decade, event_type
ORDER BY decade, occurrences DESC;
