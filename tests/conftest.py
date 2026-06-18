import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from storm_db.api.main import create_app
from storm_db.database import get_session
from storm_db.models import (
    DisasterEvent,
    EarthquakeDetail,
    EventType,
    HurricaneDetail,
    Impact,
    Location,
)


@pytest.fixture(scope="session")
def engine():
    eng = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(eng)
    return eng


@pytest.fixture
def session(engine):
    with Session(engine) as s:
        yield s
        s.rollback()


@pytest.fixture
def client(engine):
    app = create_app()

    def override_session():
        with Session(engine) as s:
            yield s

    app.dependency_overrides[get_session] = override_session
    return TestClient(app)


# ── Seed helpers ─────────────────────────────────────────────────────────────

def make_location(session: Session, name: str = "Miami", country: str = "USA") -> Location:
    loc = Location(name=name, country=country, region="Southeast", latitude=25.8, longitude=-80.2)
    session.add(loc)
    session.flush()
    return loc


def make_hurricane(
    session: Session,
    loc: Location,
    name: str = "Katrina",
    year: int = 2005,
    category: int = 5,
    wind_speed_mph: int = 175,
    deaths: int = 1833,
    damage_usd: int = 125_000_000_000,
) -> DisasterEvent:
    event = DisasterEvent(
        location_id=loc.id,
        event_type=EventType.HURRICANE,
        year=year,
        name=name,
        duration_days=9,
    )
    session.add(event)
    session.flush()
    session.add(
        HurricaneDetail(event_id=event.id, category=category, wind_speed_mph=wind_speed_mph)
    )
    session.add(Impact(event_id=event.id, deaths=deaths, injuries=15000, damage_usd=damage_usd))
    session.commit()
    session.refresh(event)
    return event


def make_earthquake(
    session: Session,
    loc: Location,
    name: str = "Tohoku",
    year: int = 2011,
    magnitude: float = 9.1,
    deaths: int = 19747,
) -> DisasterEvent:
    event = DisasterEvent(
        location_id=loc.id,
        event_type=EventType.EARTHQUAKE,
        year=year,
        name=name,
        duration_days=1,
    )
    session.add(event)
    session.flush()
    session.add(EarthquakeDetail(event_id=event.id, magnitude=magnitude, depth_km=29.0))
    session.add(Impact(event_id=event.id, deaths=deaths, injuries=6000, damage_usd=360_000_000_000))
    session.commit()
    session.refresh(event)
    return event
