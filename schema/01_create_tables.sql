-- ============================================================
-- Natural Disaster Events Database — PostgreSQL DDL
-- Matches the SQLModel ORM in src/storm_db/models/models.py
-- ============================================================

CREATE TYPE event_type AS ENUM ('hurricane', 'earthquake', 'drought', 'tsunami', 'flood');

-- Geographic context shared across all event types
CREATE TABLE locations (
    id        SERIAL       PRIMARY KEY,
    name      VARCHAR(100) NOT NULL,
    country   VARCHAR(100) NOT NULL,
    region    VARCHAR(100),
    latitude  DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

CREATE INDEX idx_locations_country ON locations (country);
CREATE INDEX idx_locations_name    ON locations (name);

-- Master event record — one row per discrete event
CREATE TABLE disaster_events (
    id            SERIAL      PRIMARY KEY,
    location_id   INT         NOT NULL REFERENCES locations(id),
    event_type    event_type  NOT NULL,
    year          SMALLINT    NOT NULL CHECK (year BETWEEN 1800 AND 2100),
    duration_days SMALLINT    CHECK (duration_days >= 1),
    name          VARCHAR(100)
);

CREATE INDEX idx_events_type     ON disaster_events (event_type);
CREATE INDEX idx_events_year     ON disaster_events (year);
CREATE INDEX idx_events_location ON disaster_events (location_id);

-- Human and economic impact (optional — not all records have data)
CREATE TABLE impacts (
    id         SERIAL PRIMARY KEY,
    event_id   INT    NOT NULL UNIQUE REFERENCES disaster_events(id),
    deaths     INT    NOT NULL DEFAULT 0 CHECK (deaths >= 0),
    injuries   INT    NOT NULL DEFAULT 0 CHECK (injuries >= 0),
    damage_usd BIGINT CHECK (damage_usd >= 0)
);

-- Hurricane meteorological detail
CREATE TABLE hurricane_details (
    id            SERIAL   PRIMARY KEY,
    event_id      INT      NOT NULL UNIQUE REFERENCES disaster_events(id),
    category      SMALLINT NOT NULL CHECK (category BETWEEN 1 AND 5),
    wind_speed_mph INT     NOT NULL CHECK (wind_speed_mph >= 0),
    pressure_mb   INT
);

-- Earthquake seismic detail
CREATE TABLE earthquake_details (
    id        SERIAL          PRIMARY KEY,
    event_id  INT             NOT NULL UNIQUE REFERENCES disaster_events(id),
    magnitude NUMERIC(4, 2)   NOT NULL CHECK (magnitude >= 0),
    depth_km  DOUBLE PRECISION
);

-- Drought Palmer Drought Severity Index
CREATE TABLE drought_details (
    id            SERIAL PRIMARY KEY,
    event_id      INT    NOT NULL UNIQUE REFERENCES disaster_events(id),
    palmer_index  DOUBLE PRECISION,
    temperature_f INT
);

-- Tsunami wave data
CREATE TABLE tsunami_details (
    id             SERIAL          PRIMARY KEY,
    event_id       INT             NOT NULL UNIQUE REFERENCES disaster_events(id),
    max_height_m   DOUBLE PRECISION,
    wave_speed_mph INT
);

-- Convenience view for dashboard queries
CREATE VIEW event_summary AS
SELECT
    de.id,
    de.name,
    de.event_type,
    de.year,
    l.name       AS location_name,
    l.country,
    l.region,
    i.deaths,
    i.injuries,
    i.damage_usd
FROM disaster_events de
JOIN locations l ON l.id = de.location_id
LEFT JOIN impacts i ON i.event_id = de.id;
