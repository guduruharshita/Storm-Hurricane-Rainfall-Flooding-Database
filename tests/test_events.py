import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.conftest import make_earthquake, make_hurricane, make_location


@pytest.fixture(autouse=True)
def seed(session: Session, engine):
    loc_usa = make_location(session, "New Orleans", "USA")
    loc_jp = make_location(session, "Sendai", "Japan")
    make_hurricane(session, loc_usa)
    make_earthquake(session, loc_jp)
    yield
    from sqlmodel import SQLModel
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def test_health(client: TestClient):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_list_events(client: TestClient):
    res = client.get("/api/events")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2


def test_filter_by_type(client: TestClient):
    res = client.get("/api/events?event_type=hurricane")
    assert res.status_code == 200
    assert all(e["event_type"] == "hurricane" for e in res.json())


def test_filter_by_country(client: TestClient):
    res = client.get("/api/events?country=Japan")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["country"] == "Japan"


def test_filter_by_year(client: TestClient):
    res = client.get("/api/events?year=2005")
    data = res.json()
    assert all(e["year"] == 2005 for e in data)


def test_get_event_detail(client: TestClient):
    list_res = client.get("/api/events?event_type=hurricane")
    event_id = list_res.json()[0]["id"]

    res = client.get(f"/api/events/{event_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["event_type"] == "hurricane"
    assert data["hurricane_detail"]["category"] == 5
    assert data["impact"]["deaths"] == 1833


def test_get_event_not_found(client: TestClient):
    res = client.get("/api/events/99999")
    assert res.status_code == 404


def test_create_event(client: TestClient):
    payload = {
        "location": {"name": "Port-au-Prince", "country": "Haiti"},
        "event_type": "earthquake",
        "year": 2010,
        "name": "Haiti earthquake",
        "impact": {"deaths": 316000, "injuries": 300000, "damage_usd": 8000000000},
        "earthquake_detail": {"magnitude": 7.0, "depth_km": 13.0},
    }
    res = client.post("/api/events", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["earthquake_detail"]["magnitude"] == 7.0
    assert data["location"]["country"] == "Haiti"


def test_create_hurricane_event(client: TestClient):
    payload = {
        "location": {"name": "Houston", "country": "USA"},
        "event_type": "hurricane",
        "year": 2017,
        "name": "Harvey",
        "impact": {"deaths": 103, "damage_usd": 125000000000},
        "hurricane_detail": {"category": 4, "wind_speed_mph": 130, "pressure_mb": 937},
    }
    res = client.post("/api/events", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["hurricane_detail"]["category"] == 4


def test_delete_event(client: TestClient):
    list_res = client.get("/api/events?event_type=hurricane")
    event_id = list_res.json()[0]["id"]

    del_res = client.delete(f"/api/events/{event_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/api/events/{event_id}")
    assert get_res.status_code == 404


def test_pagination(client: TestClient):
    res = client.get("/api/events?limit=1&offset=0")
    assert len(res.json()) == 1
