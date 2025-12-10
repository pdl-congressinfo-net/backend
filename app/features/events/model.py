import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from app.features.locations.model import Location
from sqlmodel import Field, Relationship, SQLModel

class EventType(SQLModel, table=True):
    __tablename__ = "event_types"
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    code: str = Field(unique=True, index=True, max_length=3, min_length=3)
    name_de: str = Field(unique=True, index=True)
    name_en: str = Field(unique=True, index=True)
    description_de: Optional[str] = None  # noqa: UP045
    description_en: Optional[str] = None  # noqa: UP045
    events: List["Event"] = Relationship(back_populates="event_type")  # noqa: UP006


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field()
    start_date: datetime
    end_date: datetime
    is_public: bool = Field(default=False)
    
    location_id: Optional[str] = Field(default=None, foreign_key="locations.id")  # noqa: UP045
    event_type_id: Optional[str] = Field(default=None, foreign_key="event_types.id")  # noqa: UP045

    event_type: Optional["EventType"] = Relationship(back_populates="events")
    location: Optional["Location"] = Relationship(back_populates="events")
