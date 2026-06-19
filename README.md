# Natural Disaster Events Database

[![CI](https://github.com/guduruharshita/storm-hurricane-rainfall-flooding-database/actions/workflows/ci.yml/badge.svg)](https://github.com/guduruharshita/storm-hurricane-rainfall-flooding-database/actions)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](pyproject.toml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](src/storm_db/api/main.py)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](schema/01_create_tables.sql)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Production-ready REST API and relational database for tracking and analysing **natural disaster events** — hurricanes, earthquakes, droughts, tsunamis, and floods. Features a normalized PostgreSQL schema, a FastAPI service layer, and analytics endpoints that aggregate human and economic impact across event types.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                  │
│                                                         │
│  POST /api/events          GET /api/analytics/summary   │
│  GET  /api/events          GET /api/analytics/by-type   │
│  GET  /api/events/{id}     GET /api/analytics/yearly-trend│
│  DELETE /api/events/{id}   GET /api/analytics/top-deadly │
│                            GET /api/analytics/hurricane-categories│
│                            GET /api/analytics/earthquake-magnitudes│
└────────────────────────┬────────────────────────────────┘
                         │ SQLModel ORM
┌────────────────────────▼────────────────────────────────┐
│                  PostgreSQL Database                    │
│                                                         │
│  locations ──────────── disaster_events                 │
│                               │                         │
│                    ┌──────────┼──────────┐              │
│                    │          │          │              │
│                 impacts  hurricane_  earthquake_        │
│                           details    details            │
│                          drought_   tsunami_            │
│                           details   details             │
└─────────────────────────────────────────────────────────┘
```

## Database Schema

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `locations` | Geographic context | `name`, `country`, `region`, `lat/lon` |
| `disaster_events` | Master event record | `event_type`, `year`, `duration_days`, `name` |
| `impacts` | Human & economic impact | `deaths`, `injuries`, `damage_usd` |
| `hurricane_details` | Meteorological data | `category` (1–5), `wind_speed_mph`, `pressure_mb` |
| `earthquake_details` | Seismic data | `magnitude`, `depth_km` |
| `drought_details` | Palmer Drought Index | `palmer_index`, `temperature_f` |
| `tsunami_details` | Wave data | `max_height_m`, `wave_speed_mph` |

All detail tables have a 1:1 foreign key to `disaster_events`, keeping the schema normalized and extensible.

## Quick Start

### Library / API (SQLite for local dev)

```bash
pip install -e ".[dev]"
uvicorn storm_db.api.main:app --reload
# Docs: http://localhost:8000/docs
```

### Docker Compose (PostgreSQL)

```bash
docker compose up --build
# API: http://localhost:8000/docs
# DB seeded automatically from schema/
```

## API Examples

```bash
# List all hurricane events
curl http://localhost:8000/api/events?event_type=hurricane

# Filter by country and year
curl "http://localhost:8000/api/events?country=USA&year=2005"

# Create a new event
curl -X POST http://localhost:8000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "location": {"name": "Homestead", "country": "USA", "region": "Southeast"},
    "event_type": "hurricane",
    "year": 1992,
    "name": "Hurricane Andrew",
    "impact": {"deaths": 65, "damage_usd": 27300000000},
    "hurricane_detail": {"category": 5, "wind_speed_mph": 165, "pressure_mb": 922}
  }'

# Analytics: summary stats
curl http://localhost:8000/api/analytics/summary
# {"total_events":15,"total_deaths":1163132,"total_damage_usd":570150000000,...}

# Top 5 deadliest events
curl "http://localhost:8000/api/analytics/top-deadly?n=5"

# Hurricane breakdown by Saffir-Simpson category
curl http://localhost:8000/api/analytics/hurricane-categories

# Earthquake magnitude distribution
curl http://localhost:8000/api/analytics/earthquake-magnitudes

# Yearly event and death trend (2000–2020)
curl "http://localhost:8000/api/analytics/yearly-trend?start_year=2000&end_year=2020"
```

## Project Structure

```
storm-hurricane-rainfall-flooding-database/
│
├── src/storm_db/
│   ├── config.py                    # pydantic-settings (STORM_* env vars)
│   ├── database.py                  # SQLAlchemy engine + session factory
│   ├── models/
│   │   └── models.py                # SQLModel ORM: Location, DisasterEvent, Impact,
│   │                                #   HurricaneDetail, EarthquakeDetail, DroughtDetail,
│   │                                #   TsunamiDetail
│   └── api/
│       ├── main.py                  # FastAPI app factory + startup hook
│       └── routers/
│           ├── events.py            # CRUD: POST/GET/DELETE /api/events
│           └── analytics.py        # Aggregation: /api/analytics/*
│
├── schema/
│   ├── 01_create_tables.sql         # PostgreSQL DDL + indexes + event_summary view
│   └── 02_seed_data.sql             # 15 historical disaster events
│
├── tests/
│   ├── conftest.py                  # SQLite in-memory DB + seed helpers
│   ├── test_events.py               # 11 CRUD tests
│   └── test_analytics.py           # 9 analytics tests
│
├── docker-compose.yml               # API + PostgreSQL 16
├── Dockerfile
├── .github/workflows/ci.yml
└── pyproject.toml
```

## Testing

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

```
tests/test_events.py::test_health PASSED
tests/test_events.py::test_list_events PASSED
tests/test_events.py::test_filter_by_type PASSED
tests/test_events.py::test_filter_by_country PASSED
tests/test_events.py::test_filter_by_year PASSED
tests/test_events.py::test_get_event_detail PASSED
tests/test_events.py::test_get_event_not_found PASSED
tests/test_events.py::test_create_event PASSED
tests/test_events.py::test_create_hurricane_event PASSED
tests/test_events.py::test_delete_event PASSED
tests/test_events.py::test_pagination PASSED
tests/test_analytics.py::test_summary PASSED
tests/test_analytics.py::test_by_type PASSED
tests/test_analytics.py::test_yearly_trend PASSED
tests/test_analytics.py::test_yearly_trend_range PASSED
tests/test_analytics.py::test_top_deadly PASSED
tests/test_analytics.py::test_top_deadly_by_type PASSED
tests/test_analytics.py::test_damage_leaders PASSED
tests/test_analytics.py::test_hurricane_categories PASSED
tests/test_analytics.py::test_earthquake_magnitudes PASSED

20 passed
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `STORM_DATABASE_URL` | `sqlite:///./storm_events.db` | Database connection string |
| `STORM_DEBUG` | `false` | Enable SQLAlchemy query logging |

## Skills Demonstrated

| Skill | Evidence |
|-------|---------|
| **Relational Database Design** | Normalized 7-table PostgreSQL schema with FK constraints, CHECK constraints, composite indexes, materialized view |
| **SQL** | DDL with enum types, indexes, `event_summary` view; 15-record seed with multi-table inserts |
| **FastAPI** | App factory, dependency injection, Pydantic v2 request/response schemas, 404/400 error handling |
| **SQLModel / SQLAlchemy** | ORM models with 1:1 and 1:N relationships, dynamic query building, aggregate functions |
| **Analytics Engineering** | GROUP BY aggregations, damage leaders, yearly trends, magnitude distribution bucketing |
| **Python Packaging** | `pyproject.toml`, `src/` layout, pydantic-settings for 12-factor config |
| **Docker** | Multi-service compose with PostgreSQL 16, health-check gated startup, schema auto-init |
| **Testing** | 20 pytest tests with SQLite in-memory DB, fixture-based isolation, conftest seed helpers |
| **CI/CD** | GitHub Actions: ruff lint + pytest on push to main and feature branches |

---

**Harshita Guduru** — [GitHub](https://github.com/guduruharshita) · [LinkedIn](https://linkedin.com/in/guduruharshita) · [Email](mailto:guduruharshita2001@gmail.com)
