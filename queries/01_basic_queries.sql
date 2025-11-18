-- Basic retrieval queries
USE weather_events;

-- All locations and event types
SELECT location_name, event_type, event_year FROM location ORDER BY event_year DESC;

-- All hurricanes ordered by wind speed
SELECT hurricane_name, wind_speed_mph, category, l.location_name
FROM hurricane h JOIN location l ON h.location_id = l.location_id
ORDER BY wind_speed_mph DESC;

-- Earthquakes with magnitude > 7.0
SELECT e.event_id, l.location_name, e.magnitude, e.depth_km
FROM earthquake e JOIN location l ON e.location_id = l.location_id
WHERE e.magnitude > 7.0
ORDER BY e.magnitude DESC;

-- Deadliest events
SELECT i.event_type, i.location_name, i.event_year, i.deaths
FROM impact i
ORDER BY i.deaths DESC
LIMIT 10;
