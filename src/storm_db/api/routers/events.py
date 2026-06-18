from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from storm_db.database import get_session
from storm_db.models import (
    DisasterEvent,
    DroughtDetail,
    EarthquakeDetail,
    EventType,
    HurricaneDetail,
    Impact,
    Location,
    TsunamiDetail,
)

router = APIRouter(prefix="/api/events", tags=["events"])

SessionDep = Annotated[Session, Depends(get_session)]


# ── Request schemas ──────────────────────────────────────────────────────────

class LocationCreate(BaseModel):
    name: str
    country: str
    region: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class ImpactCreate(BaseModel):
    deaths: int = 0
    injuries: int = 0
    damage_usd: int | None = None


class HurricaneDetailCreate(BaseModel):
    category: int
    wind_speed_mph: int
    pressure_mb: int | None = None


class EarthquakeDetailCreate(BaseModel):
    magnitude: float
    depth_km: float | None = None


class DroughtDetailCreate(BaseModel):
    palmer_index: float | None = None
    temperature_f: int | None = None


class TsunamiDetailCreate(BaseModel):
    max_height_m: float | None = None
    wave_speed_mph: int | None = None


class EventCreate(BaseModel):
    location: LocationCreate
    event_type: EventType
    year: int
    duration_days: int | None = None
    name: str | None = None
    impact: ImpactCreate | None = None
    hurricane_detail: HurricaneDetailCreate | None = None
    earthquake_detail: EarthquakeDetailCreate | None = None
    drought_detail: DroughtDetailCreate | None = None
    tsunami_detail: TsunamiDetailCreate | None = None


# ── Response schemas ─────────────────────────────────────────────────────────

class LocationRead(BaseModel):
    id: int
    name: str
    country: str
    region: str | None
    latitude: float | None
    longitude: float | None


class ImpactRead(BaseModel):
    deaths: int
    injuries: int
    damage_usd: int | None


class HurricaneDetailRead(BaseModel):
    category: int
    wind_speed_mph: int
    pressure_mb: int | None


class EarthquakeDetailRead(BaseModel):
    magnitude: float
    depth_km: float | None


class DroughtDetailRead(BaseModel):
    palmer_index: float | None
    temperature_f: int | None


class TsunamiDetailRead(BaseModel):
    max_height_m: float | None
    wave_speed_mph: int | None


class EventRead(BaseModel):
    id: int
    event_type: EventType
    year: int
    duration_days: int | None
    name: str | None
    location: LocationRead
    impact: ImpactRead | None
    hurricane_detail: HurricaneDetailRead | None
    earthquake_detail: EarthquakeDetailRead | None
    drought_detail: DroughtDetailRead | None
    tsunami_detail: TsunamiDetailRead | None


class EventSummary(BaseModel):
    id: int
    name: str | None
    event_type: EventType
    year: int
    location_name: str
    country: str
    deaths: int | None
    damage_usd: int | None


# ── Helpers ──────────────────────────────────────────────────────────────────

def _to_event_read(event: DisasterEvent) -> EventRead:
    loc = event.location
    imp = event.impact
    return EventRead(
        id=event.id,
        event_type=event.event_type,
        year=event.year,
        duration_days=event.duration_days,
        name=event.name,
        location=LocationRead(
            id=loc.id,
            name=loc.name,
            country=loc.country,
            region=loc.region,
            latitude=loc.latitude,
            longitude=loc.longitude,
        ),
        impact=ImpactRead(
            deaths=imp.deaths,
            injuries=imp.injuries,
            damage_usd=imp.damage_usd,
        ) if imp else None,
        hurricane_detail=HurricaneDetailRead(
            category=event.hurricane_detail.category,
            wind_speed_mph=event.hurricane_detail.wind_speed_mph,
            pressure_mb=event.hurricane_detail.pressure_mb,
        ) if event.hurricane_detail else None,
        earthquake_detail=EarthquakeDetailRead(
            magnitude=event.earthquake_detail.magnitude,
            depth_km=event.earthquake_detail.depth_km,
        ) if event.earthquake_detail else None,
        drought_detail=DroughtDetailRead(
            palmer_index=event.drought_detail.palmer_index,
            temperature_f=event.drought_detail.temperature_f,
        ) if event.drought_detail else None,
        tsunami_detail=TsunamiDetailRead(
            max_height_m=event.tsunami_detail.max_height_m,
            wave_speed_mph=event.tsunami_detail.wave_speed_mph,
        ) if event.tsunami_detail else None,
    )


# ── Routes ───────────────────────────────────────────────────────────────────

@router.get("", response_model=list[EventSummary])
def list_events(
    session: SessionDep,
    event_type: EventType | None = Query(default=None),
    year: int | None = Query(default=None, ge=1800, le=2100),
    country: str | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[EventSummary]:
    stmt = (
        select(DisasterEvent, Location, Impact)
        .join(Location, DisasterEvent.location_id == Location.id)
        .outerjoin(Impact, Impact.event_id == DisasterEvent.id)
    )
    if event_type:
        stmt = stmt.where(DisasterEvent.event_type == event_type)
    if year:
        stmt = stmt.where(DisasterEvent.year == year)
    if country:
        stmt = stmt.where(Location.country.ilike(f"%{country}%"))
    stmt = stmt.offset(offset).limit(limit)

    rows = session.exec(stmt).all()
    return [
        EventSummary(
            id=ev.id,
            name=ev.name,
            event_type=ev.event_type,
            year=ev.year,
            location_name=loc.name,
            country=loc.country,
            deaths=imp.deaths if imp else None,
            damage_usd=imp.damage_usd if imp else None,
        )
        for ev, loc, imp in rows
    ]


@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, session: SessionDep) -> EventRead:
    event = session.get(DisasterEvent, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return _to_event_read(event)


@router.post("", response_model=EventRead, status_code=201)
def create_event(payload: EventCreate, session: SessionDep) -> EventRead:
    loc = Location(**payload.location.model_dump())
    session.add(loc)
    session.flush()

    event = DisasterEvent(
        location_id=loc.id,
        event_type=payload.event_type,
        year=payload.year,
        duration_days=payload.duration_days,
        name=payload.name,
    )
    session.add(event)
    session.flush()

    if payload.impact:
        session.add(Impact(event_id=event.id, **payload.impact.model_dump()))
    if payload.hurricane_detail:
        session.add(HurricaneDetail(event_id=event.id, **payload.hurricane_detail.model_dump()))
    if payload.earthquake_detail:
        session.add(EarthquakeDetail(event_id=event.id, **payload.earthquake_detail.model_dump()))
    if payload.drought_detail:
        session.add(DroughtDetail(event_id=event.id, **payload.drought_detail.model_dump()))
    if payload.tsunami_detail:
        session.add(TsunamiDetail(event_id=event.id, **payload.tsunami_detail.model_dump()))

    session.commit()
    session.refresh(event)
    return _to_event_read(event)


@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int, session: SessionDep) -> None:
    event = session.get(DisasterEvent, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    # cascade delete related rows
    for related in [event.impact, event.hurricane_detail, event.earthquake_detail,
                    event.drought_detail, event.tsunami_detail]:
        if related:
            session.delete(related)
    session.delete(event)
    if event.location and not event.location.events:
        session.delete(event.location)
    session.commit()
