import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.features.locations.model import Location


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)
    description: str | None = None
    events: list["Event"] = Relationship(back_populates="category")


class EventType(SQLModel, table=True):
    __tablename__ = "event_types"
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)
    description: str | None = None
    events: list["Event"] = Relationship(back_populates="event_type")


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field()
    start_date: datetime
    end_date: datetime
    is_published: bool = Field(default=False)

    location_id: str | None = Field(default=None, foreign_key="locations.id")
    category_id: str | None = Field(default=None, foreign_key="categories.id")
    event_type_id: str | None = Field(default=None, foreign_key="event_types.id")

    event_type: Optional["EventType"] = Relationship(back_populates="events")
    location: Optional["Location"] = Relationship(back_populates="events")
    category: Optional["Category"] = Relationship(back_populates="events")
