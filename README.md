# Weather Events Database

[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql&logoColor=white)](https://mysql.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)

A normalized relational database modeling major weather and natural disaster events — hurricanes, earthquakes, droughts, floods, and tsunamis — with human impact and economic damage data.

## Schema

```
location (location_id PK, event_id, location_name, event_type, event_year, duration_days)
    |
    |── hurricane  (event_id PK, location_id FK, name, wind_speed_mph, category)
    |── earthquake (event_id PK, location_id FK, magnitude, depth_km)
    |── drought    (event_id PK, location_id FK, temperature_f, palmer_index)
    |── tsunami    (event_id PK, location_id FK, wave_speed_mph, max_height_m)
    |── impact     (event_id PK, location_id FK, deaths, injuries, damage_usd)
```

## Project Structure

```
├── schema/
│   ├── 01_create_tables.sql    # Table definitions with constraints
│   └── 02_seed_data.sql        # 5 major historical events
├── queries/
│   ├── 01_basic_queries.sql    # Retrieval and filtering
│   ├── 02_advanced_queries.sql # Aggregations and joins
│   └── 03_analytical_queries.sql # Views, severity index, reporting
└── .gitignore
```

## Quick Start

```bash
# Load schema and seed data
mysql -u root -p < schema/01_create_tables.sql
mysql -u root -p < schema/02_seed_data.sql

# Run queries
mysql -u root -p weather_events < queries/01_basic_queries.sql
```

## Sample Query

```sql
-- Top 5 deadliest events with economic damage
SELECT location_name, event_type, event_year, deaths, damage_usd
FROM impact
ORDER BY deaths DESC
LIMIT 5;
```

## Seed Data Includes

| Event | Year | Deaths | Damage |
|-------|------|--------|--------|
| Hurricane Katrina | 2005 | 1,833 | $125B |
| Indian Ocean Tsunami | 2004 | 227,898 | $10B |
| Bangladesh Flooding | 2017 | 156 | $3B |

## Author

**Harshita Guduru** — [GitHub](https://github.com/guduruharshita) · [LinkedIn](https://linkedin.com/in/harshita-guduru)
