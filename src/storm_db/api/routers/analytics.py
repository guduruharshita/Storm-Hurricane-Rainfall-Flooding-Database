from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlmodel import Session, col, func, select

from storm_db.database import get_session
from storm_db.models import (
    DisasterEvent,
    EarthquakeDetail,
    EventType,
    HurricaneDetail,
    Impact,
    Location,
)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

SessionDep = Annotated[Session, Depends(get_session)]


# ── Response schemas ─────────────────────────────────────────────────────────

class SummaryStats(BaseModel):
    total_events: int
    total_deaths: int
    total_injuries: int
    total_damage_usd: int | None
    event_type_counts: dict[str, int]


class EventTypeBreakdown(BaseModel):
    event_type: str
    count: int
    total_deaths: int
    total_damage_usd: int | None


class YearlyTrend(BaseModel):
    year: int
    event_count: int
    total_deaths: int
    total_damage_usd: int | None


class TopDisaster(BaseModel):
    event_id: int
    name: str | None
    event_type: str
    year: int
    country: str
    deaths: int
    injuries: int
    damage_usd: int | None


class HurricaneStats(BaseModel):
    category: int
    count: int
    avg_wind_speed_mph: float
    total_deaths: int
    total_damage_usd: int | None


class MagnitudeDistribution(BaseModel):
    magnitude_bucket: str
    count: int
    avg_depth_km: float | None
    total_deaths: int


# ── Routes ───────────────────────────────────────────────────────────────────

@router.get("/summary", response_model=SummaryStats)
def get_summary(session: SessionDep) -> SummaryStats:
    total_events = session.exec(select(func.count(col(DisasterEvent.id)))).one()

    agg = session.exec(
        select(
            func.coalesce(func.sum(Impact.deaths), 0),
            func.coalesce(func.sum(Impact.injuries), 0),
            func.sum(Impact.damage_usd),
        ).select_from(Impact)
    ).one()
    total_deaths, total_injuries, total_damage = agg

    type_rows = session.exec(
        select(DisasterEvent.event_type, func.count(col(DisasterEvent.id)))
        .group_by(DisasterEvent.event_type)
    ).all()
    type_counts = {row[0]: row[1] for row in type_rows}

    return SummaryStats(
        total_events=total_events,
        total_deaths=total_deaths,
        total_injuries=total_injuries,
        total_damage_usd=total_damage,
        event_type_counts=type_counts,
    )


@router.get("/by-type", response_model=list[EventTypeBreakdown])
def breakdown_by_type(session: SessionDep) -> list[EventTypeBreakdown]:
    rows = session.exec(
        select(
            DisasterEvent.event_type,
            func.count(col(DisasterEvent.id)),
            func.coalesce(func.sum(Impact.deaths), 0),
            func.sum(Impact.damage_usd),
        )
        .outerjoin(Impact, Impact.event_id == DisasterEvent.id)
        .group_by(DisasterEvent.event_type)
        .order_by(func.count(col(DisasterEvent.id)).desc())
    ).all()
    return [
        EventTypeBreakdown(
            event_type=r[0],
            count=r[1],
            total_deaths=r[2],
            total_damage_usd=r[3],
        )
        for r in rows
    ]


@router.get("/yearly-trend", response_model=list[YearlyTrend])
def yearly_trend(
    session: SessionDep,
    start_year: int | None = Query(default=None, ge=1800),
    end_year: int | None = Query(default=None, le=2100),
) -> list[YearlyTrend]:
    stmt = (
        select(
            DisasterEvent.year,
            func.count(col(DisasterEvent.id)),
            func.coalesce(func.sum(Impact.deaths), 0),
            func.sum(Impact.damage_usd),
        )
        .outerjoin(Impact, Impact.event_id == DisasterEvent.id)
        .group_by(DisasterEvent.year)
        .order_by(DisasterEvent.year)
    )
    if start_year:
        stmt = stmt.where(DisasterEvent.year >= start_year)
    if end_year:
        stmt = stmt.where(DisasterEvent.year <= end_year)

    rows = session.exec(stmt).all()
    return [
        YearlyTrend(year=r[0], event_count=r[1], total_deaths=r[2], total_damage_usd=r[3])
        for r in rows
    ]


@router.get("/top-deadly", response_model=list[TopDisaster])
def top_deadly(
    session: SessionDep,
    n: int = Query(default=10, ge=1, le=100),
    event_type: EventType | None = None,
) -> list[TopDisaster]:
    stmt = (
        select(DisasterEvent, Location, Impact)
        .join(Location, DisasterEvent.location_id == Location.id)
        .join(Impact, Impact.event_id == DisasterEvent.id)
        .order_by(col(Impact.deaths).desc())
        .limit(n)
    )
    if event_type:
        stmt = stmt.where(DisasterEvent.event_type == event_type)

    rows = session.exec(stmt).all()
    return [
        TopDisaster(
            event_id=ev.id,
            name=ev.name,
            event_type=ev.event_type,
            year=ev.year,
            country=loc.country,
            deaths=imp.deaths,
            injuries=imp.injuries,
            damage_usd=imp.damage_usd,
        )
        for ev, loc, imp in rows
    ]


@router.get("/damage-leaders", response_model=list[TopDisaster])
def damage_leaders(
    session: SessionDep,
    n: int = Query(default=10, ge=1, le=100),
) -> list[TopDisaster]:
    stmt = (
        select(DisasterEvent, Location, Impact)
        .join(Location, DisasterEvent.location_id == Location.id)
        .join(Impact, Impact.event_id == DisasterEvent.id)
        .where(Impact.damage_usd.isnot(None))
        .order_by(col(Impact.damage_usd).desc())
        .limit(n)
    )
    rows = session.exec(stmt).all()
    return [
        TopDisaster(
            event_id=ev.id,
            name=ev.name,
            event_type=ev.event_type,
            year=ev.year,
            country=loc.country,
            deaths=imp.deaths,
            injuries=imp.injuries,
            damage_usd=imp.damage_usd,
        )
        for ev, loc, imp in rows
    ]


@router.get("/hurricane-categories", response_model=list[HurricaneStats])
def hurricane_by_category(session: SessionDep) -> list[HurricaneStats]:
    rows = session.exec(
        select(
            HurricaneDetail.category,
            func.count(col(HurricaneDetail.id)),
            func.avg(HurricaneDetail.wind_speed_mph),
            func.coalesce(func.sum(Impact.deaths), 0),
            func.sum(Impact.damage_usd),
        )
        .outerjoin(Impact, Impact.event_id == HurricaneDetail.event_id)
        .group_by(HurricaneDetail.category)
        .order_by(HurricaneDetail.category)
    ).all()
    return [
        HurricaneStats(
            category=r[0],
            count=r[1],
            avg_wind_speed_mph=round(r[2], 1),
            total_deaths=r[3],
            total_damage_usd=r[4],
        )
        for r in rows
    ]


@router.get("/earthquake-magnitudes", response_model=list[MagnitudeDistribution])
def earthquake_magnitude_dist(session: SessionDep) -> list[MagnitudeDistribution]:
    rows = session.exec(
        select(EarthquakeDetail, Impact)
        .outerjoin(Impact, Impact.event_id == EarthquakeDetail.event_id)
    ).all()

    buckets: dict[str, dict] = {}
    for detail, imp in rows:
        m = detail.magnitude
        if m < 4.0:
            bucket = "<4.0 Minor"
        elif m < 5.0:
            bucket = "4.0–4.9 Light"
        elif m < 6.0:
            bucket = "5.0–5.9 Moderate"
        elif m < 7.0:
            bucket = "6.0–6.9 Strong"
        elif m < 8.0:
            bucket = "7.0–7.9 Major"
        else:
            bucket = "≥8.0 Great"

        if bucket not in buckets:
            buckets[bucket] = {"count": 0, "depths": [], "deaths": 0}
        b = buckets[bucket]
        b["count"] += 1
        if detail.depth_km is not None:
            b["depths"].append(detail.depth_km)
        b["deaths"] += imp.deaths if imp else 0

    return [
        MagnitudeDistribution(
            magnitude_bucket=k,
            count=v["count"],
            avg_depth_km=round(sum(v["depths"]) / len(v["depths"]), 1) if v["depths"] else None,
            total_deaths=v["deaths"],
        )
        for k, v in sorted(buckets.items())
    ]
