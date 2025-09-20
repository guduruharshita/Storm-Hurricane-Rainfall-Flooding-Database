-- ============================================================
-- Weather Events Database Schema
-- Database: weather_events
-- ============================================================

CREATE DATABASE IF NOT EXISTS weather_events;
USE weather_events;

-- Location: geographic context for all weather events
CREATE TABLE location (
    location_id   INT          PRIMARY KEY AUTO_INCREMENT,
    event_id      INT          NOT NULL,
    location_name VARCHAR(100) NOT NULL,
    event_type    VARCHAR(50)  NOT NULL,
    event_year    YEAR         NOT NULL,
    duration_days INT          NOT NULL
);

-- Hurricane events with meteorological data
CREATE TABLE hurricane (
    event_id       INT          PRIMARY KEY,
    location_id    INT          NOT NULL,
    hurricane_name VARCHAR(100) NOT NULL,
    wind_speed_mph INT          NOT NULL,
    temperature_f  INT,
    category       TINYINT      CHECK (category BETWEEN 1 AND 5),
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

-- Earthquake events with seismic data
CREATE TABLE earthquake (
    event_id    INT           PRIMARY KEY,
    location_id INT           NOT NULL,
    duration    VARCHAR(50),
    magnitude   DECIMAL(4,2)  NOT NULL CHECK (magnitude >= 0),
    depth_km    FLOAT,
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

-- Flooding and storm impact data
CREATE TABLE impact (
    event_id      INT          PRIMARY KEY,
    location_id   INT          NOT NULL,
    location_name VARCHAR(100),
    event_type    VARCHAR(50),
    event_year    YEAR,
    deaths        INT          DEFAULT 0 CHECK (deaths >= 0),
    injuries      INT          DEFAULT 0,
    damage_usd    BIGINT,
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

-- Drought events
CREATE TABLE drought (
    event_id      INT  PRIMARY KEY,
    location_id   INT  NOT NULL,
    temperature_f INT,
    palmer_index  FLOAT,
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

-- Tsunami events
CREATE TABLE tsunami (
    event_id       INT  PRIMARY KEY,
    location_id    INT  NOT NULL,
    wave_speed_mph INT,
    max_height_m   FLOAT,
    temperature_f  INT,
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);
