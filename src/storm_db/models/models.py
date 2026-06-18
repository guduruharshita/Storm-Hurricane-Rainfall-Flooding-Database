from enum import StrEnum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class EventType(StrEnum):
    HURRICANE = "hurricane"
    EARTHQUAKE = "earthquake"
    DROUGHT = "drought"
    TSUNAMI = "tsunami"
    FLOOD = "flood"


class Location(SQLModel, table=True):
    __tablename__ = "locations"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, index=True)
    country: str = Field(max_length=100, index=True)
    region: str | None = Field(default=None, max_length=100)
    latitude: float | None = None
    longitude: float | None = None

    events: list["DisasterEvent"] = Relationship(back_populates="location")


class DisasterEvent(SQLModel, table=True):
    __tablename__ = "disaster_events"

    id: int | None = Field(default=None, primary_key=True)
    location_id: int = Field(foreign_key="locations.id", index=True)
    event_type: EventType = Field(index=True)
    year: int = Field(index=True)
    duration_days: int | None = Field(default=None, ge=1)
    name: str | None = Field(default=None, max_length=100)

    location: Location | None = Relationship(back_populates="events")
    impact: Optional["Impact"] = Relationship(back_populates="event")
    hurricane_detail: Optional["HurricaneDetail"] = Relationship(back_populates="event")
    earthquake_detail: Optional["EarthquakeDetail"] = Relationship(back_populates="event")
    drought_detail: Optional["DroughtDetail"] = Relationship(back_populates="event")
    tsunami_detail: Optional["TsunamiDetail"] = Relationship(back_populates="event")


class Impact(SQLModel, table=True):
    __tablename__ = "impacts"

    id: int | None = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="disaster_events.id", unique=True, index=True)
    deaths: int = Field(default=0, ge=0)
    injuries: int = Field(default=0, ge=0)
    damage_usd: int | None = Field(default=None, ge=0)

    event: DisasterEvent | None = Relationship(back_populates="impact")


class HurricaneDetail(SQLModel, table=True):
    __tablename__ = "hurricane_details"

    id: int | None = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="disaster_events.id", unique=True, index=True)
    category: int = Field(ge=1, le=5)
    wind_speed_mph: int = Field(ge=0)
    pressure_mb: int | None = None

    event: DisasterEvent | None = Relationship(back_populates="hurricane_detail")


class EarthquakeDetail(SQLModel, table=True):
    __tablename__ = "earthquake_details"

    id: int | None = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="disaster_events.id", unique=True, index=True)
    magnitude: float = Field(ge=0.0)
    depth_km: float | None = None

    event: DisasterEvent | None = Relationship(back_populates="earthquake_detail")


class DroughtDetail(SQLModel, table=True):
    __tablename__ = "drought_details"

    id: int | None = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="disaster_events.id", unique=True, index=True)
    palmer_index: float | None = None
    temperature_f: int | None = None

    event: DisasterEvent | None = Relationship(back_populates="drought_detail")


class TsunamiDetail(SQLModel, table=True):
    __tablename__ = "tsunami_details"

    id: int | None = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="disaster_events.id", unique=True, index=True)
    max_height_m: float | None = None
    wave_speed_mph: int | None = None

    event: DisasterEvent | None = Relationship(back_populates="tsunami_detail")
