import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.features.companies.model import Sponsoring
    from app.features.locations.model import Location
    from app.features.programm.model import EventSession


class EventType(SQLModel, table=True):
    __tablename__ = "event_types"
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    code: str = Field(unique=True, index=True, max_length=3, min_length=3)
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
    subject: Optional[str] = Field(default=None)  # noqa: UP045
    url: Optional[str] = Field(default=None)  # noqa: UP045
    language: Optional[str] = Field(default="de", max_length=2)  # noqa: UP045

    location_id: Optional[str] = Field(default=None, foreign_key="locations.id")  # noqa: UP045
    event_type_id: Optional[str] = Field(default=None, foreign_key="event_types.id")  # noqa: UP045

    event_type: Optional["EventType"] = Relationship(back_populates="events")
    location: Optional["Location"] = Relationship(back_populates="events")
    sponsorings: List["Sponsoring"] = Relationship(back_populates="events")  # noqa: UP006
    sessions: list["EventSession"] = Relationship(
        back_populates="event"
    )  # Day-level sessions with program items
