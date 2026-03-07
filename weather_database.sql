-- Weather Database SQL Queries
-- Database: weatherr

-- =====================================================
-- Location Table
-- =====================================================
CREATE TABLE location(
    event_id INT,
    location_id INT PRIMARY KEY,
    location_name VARCHAR(50),
    event_type VARCHAR(50),
    date YEAR,
    duration INT
);

-- Data insertion for Location
LOAD DATA INFILE "E:\\location.csv" 
INTO TABLE weatherr.location 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(event_id, location_id, location_name, event_type, year, duration);

-- Query to show data
SELECT * FROM location;

-- =====================================================
-- Hurricane Table
-- =====================================================
CREATE TABLE hurricane(
    event_id INT(10) PRIMARY KEY,
    location_id INT(10),
    hurricane_name VARCHAR(50),
    wind_speed INT(10),
    temperature INT(10),
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

-- Data insertion for Hurricane
LOAD DATA INFILE "E:\\hurricane.csv" 
INTO TABLE weatherr.hurricane 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(event_id, location_id, hurricane_name, wind_speed, temperature);

-- Query to show data
SELECT * FROM hurricane;

-- =====================================================
-- Earthquake Table
-- =====================================================
CREATE TABLE earthquake(
    event_id INT PRIMARY KEY,
    location_id INT,
    duration VARCHAR(50),
    magnitude FLOAT(50,4),
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

-- Data insertion for Earthquake
LOAD DATA INFILE "E:\\earthquake.csv" 
INTO TABLE weatherr.earthquake 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(event_id, location_id, duration, magnitude);

-- Query to show data
SELECT * FROM earthquake;

-- =====================================================
-- Impact Table
-- =====================================================
CREATE TABLE impact(
    location_id INT,
    event_id INT PRIMARY KEY,
    location_name VARCHAR(50),
    event_type VARCHAR(50),
    date YEAR,
    death INT,
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

-- Data insertion for Impact
LOAD DATA INFILE "E:\\imapct.csv" 
INTO TABLE weatherr.impact 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(event_id, location_id, location_name, event_type, year, death);

-- Query to show data
SELECT * FROM impact;

-- =====================================================
-- Droughts Table
-- =====================================================
CREATE TABLE droughts(
    event_id INT PRIMARY KEY,
    location_id INT,
    temperature INT,
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

-- Data insertion for Droughts
LOAD DATA INFILE "E:\\droughts.csv" 
INTO TABLE weatherr.droughts 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(event_id, location_id, temperature);

-- Query to show data
SELECT * FROM droughts;

-- =====================================================
-- Tsunami Table
-- =====================================================
CREATE TABLE tsunami(
    event_id INT PRIMARY KEY,
    location_id INT,
    wave_speed INT,
    temperature INT,
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

-- Data insertion for Tsunami
LOAD DATA INFILE "E:\\tsunami.csv" 
INTO TABLE weatherr.tsunami 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(event_id, location_id, wave_speed, temperature);

-- Query to show data
SELECT * FROM tsunami;

