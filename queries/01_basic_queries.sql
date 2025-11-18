-- Basic retrieval queries
USE weather_events;

-- All events by year (most recent first)
SELECT location_name, event_type, event_year, duration_days
FROM location
ORDER BY event_year DESC;

-- Hurricanes ranked by wind speed
SELECT h.hurricane_name, h.wind_speed_mph, h.category, l.location_name
FROM hurricane h
JOIN location l ON h.location_id = l.location_id
ORDER BY h.wind_speed_mph DESC;

-- High-magnitude earthquakes
SELECT e.event_id, l.location_name, e.magnitude, e.depth_km
FROM earthquake e
JOIN location l ON e.location_id = l.location_id
WHERE e.magnitude > 7.0
ORDER BY e.magnitude DESC;

-- Top 10 deadliest events
SELECT event_type, location_name, event_year, deaths
FROM impact
ORDER BY deaths DESC
LIMIT 10;
