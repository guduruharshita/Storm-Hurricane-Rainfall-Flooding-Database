# Weather Database

A comprehensive SQL database for tracking and managing weather-related events including hurricanes, earthquakes, tsunamis, droughts, and their impacts.

## Database Overview

This database contains 6 related tables to store weather event data:

### Tables

1. **Location** - Stores location information for weather events
   - `event_id` - Event identifier
   - `location_id` - Primary key
   - `location_name` - Name of the location
   - `event_type` - Type of weather event
   - `date` - Year of the event
   - `duration` - Duration of the event

2. **Hurricane** - Stores hurricane-specific data
   - `event_id` - Primary key
   - `location_id` - Foreign key to Location
   - `hurricane_name` - Name of the hurricane
   - `wind_speed` - Wind speed in mph
   - `temperature` - Temperature reading

3. **Earthquake** - Stores earthquake data
   - `event_id` - Primary key
   - `location_id` - Foreign key to Location
   - `duration` - Duration of the earthquake
   - `magnitude` - Magnitude on Richter scale

4. **Impact** - Stores impact data of weather events
   - `event_id` - Primary key
   - `location_id` - Foreign key to Location
   - `location_name` - Name of affected location
   - `event_type` - Type of event
   - `date` - Year of event
   - `death` - Number of deaths

5. **Droughts** - Stores drought data
   - `event_id` - Primary key
   - `location_id` - Foreign key to Location
   - `temperature` - Temperature reading

6. **Tsunami** - Stores tsunami data
   - `event_id` - Primary key
   - `location_id` - Foreign key to Location
   - `wave_speed` - Speed of waves
   - `temperature` - Water temperature

## Getting Started

### Prerequisites

- MySQL Server
- MySQL Workbench (optional, for GUI)

### Installation

1. Create the database:
```sql
CREATE DATABASE weatherr;
USE weatherr;
```

2. Run the SQL script:
```sql
SOURCE weather_database.sql;
```

Or copy and execute the SQL commands in your MySQL client.

### CSV Data Files

The following CSV files are required for data insertion:
- `location.csv` - Location data
- `hurricane.csv` - Hurricane data
- `earthquake.csv` - Earthquake data
- `impact.csv` - Impact data
- `droughts.csv` - Drought data
- `tsunami.csv` - Tsunami data

Place these files in the appropriate directory and update the `LOAD DATA INFILE` paths as needed.

## Query Examples

```sql
-- View all locations
SELECT * FROM location;

-- View all hurricanes
SELECT * FROM hurricane;

-- View all earthquakes
SELECT * FROM earthquake;

-- View all impacts
SELECT * FROM impact;

-- View all droughts
SELECT * FROM droughts;

-- View all tsunamis
SELECT * FROM tsunami;
```

## License

This project is for educational purposes.

