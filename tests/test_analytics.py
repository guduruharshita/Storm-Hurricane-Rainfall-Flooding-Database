import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from tests.conftest import make_earthquake, make_hurricane, make_location


@pytest.fixture(autouse=True)
def seed(session: Session, engine):
    loc_usa = make_location(session, "New Orleans", "USA")
    loc_jp = make_location(session, "Sendai", "Japan")
    loc_tx = make_location(session, "Houston", "USA")

    make_hurricane(
        session, loc_usa, name="Katrina", year=2005, category=5, wind_speed_mph=175,
        deaths=1833, damage_usd=125_000_000_000
    )
    make_hurricane(
        session, loc_tx, name="Harvey", year=2017, category=4, wind_speed_mph=130,
        deaths=103, damage_usd=125_000_000_000
    )
    make_earthquake(session, loc_jp, name="Tohoku", year=2011, magnitude=9.1, deaths=19747)

    yield
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def test_summary(client: TestClient):
    res = client.get("/api/analytics/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["total_events"] == 3
    assert data["total_deaths"] == 1833 + 103 + 19747
    assert "hurricane" in data["event_type_counts"]
    assert data["event_type_counts"]["hurricane"] == 2


def test_by_type(client: TestClient):
    res = client.get("/api/analytics/by-type")
    assert res.status_code == 200
    data = res.json()
    types = {row["event_type"]: row for row in data}
    assert "hurricane" in types
    assert types["hurricane"]["count"] == 2
    assert types["earthquake"]["total_deaths"] == 19747


def test_yearly_trend(client: TestClient):
    res = client.get("/api/analytics/yearly-trend")
    assert res.status_code == 200
    data = res.json()
    years = {row["year"]: row for row in data}
    assert 2005 in years
    assert years[2005]["event_count"] == 1


def test_yearly_trend_range(client: TestClient):
    res = client.get("/api/analytics/yearly-trend?start_year=2010&end_year=2015")
    data = res.json()
    assert all(2010 <= row["year"] <= 2015 for row in data)


def test_top_deadly(client: TestClient):
    res = client.get("/api/analytics/top-deadly?n=3")
    assert res.status_code == 200
    data = res.json()
    assert data[0]["deaths"] >= data[-1]["deaths"]  # sorted descending


def test_top_deadly_by_type(client: TestClient):
    res = client.get("/api/analytics/top-deadly?event_type=hurricane&n=5")
    data = res.json()
    assert all(e["event_type"] == "hurricane" for e in data)


def test_damage_leaders(client: TestClient):
    res = client.get("/api/analytics/damage-leaders?n=2")
    assert res.status_code == 200
    data = res.json()
    assert len(data) <= 2
    assert data[0]["damage_usd"] >= data[-1]["damage_usd"]


def test_hurricane_categories(client: TestClient):
    res = client.get("/api/analytics/hurricane-categories")
    assert res.status_code == 200
    data = res.json()
    cats = {row["category"]: row for row in data}
    assert 4 in cats
    assert 5 in cats
    assert cats[5]["count"] == 1


def test_earthquake_magnitudes(client: TestClient):
    res = client.get("/api/analytics/earthquake-magnitudes")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
    buckets = [row["magnitude_bucket"] for row in data]
    assert any("Great" in b or "Major" in b for b in buckets)
