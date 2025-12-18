import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.features.events.model import Event
    from app.features.locations.model import Location
    from app.features.users.model import Contact


class ProgrammType(str, Enum):
    """Enum for different types of program sessions"""

    LECTURE = "LCT"
    WORKSHOP = "WKS"
    DEMO = "DMO"
    NETWORKING = "NET"
    BREAK = "BRK"
    KEYNOTE = "KEY"
    OTHER = "OTH"


class Programm(SQLModel, table=True):
    """Single program item (e.g., lecture, workshop, break) that belongs to a day session."""

    __tablename__ = "programms"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    title: str = Field(index=True)
    description: str | None = Field(default=None)
    type: ProgrammType = Field(default=ProgrammType.LECTURE, index=True)

    # Location & Logistics
    location: Optional["Location"] = Field(default=None)  # Room or building
    capacity: int | None = Field(default=None)  # Max participants

    # Timing within the day session
    start_time: datetime = Field(index=True)
    end_time: datetime

    # Content Details
    level: str | None = Field(default=None)  # Beginner, Intermediate, Advanced
    speaker_id: Optional["Contact"] = Field(default=None)  # Speaker/Presenter name
    tags: str | None = Field(default=None)  # Comma-separated tags

    # Position within the day session
    session_id: str = Field(foreign_key="event_sessions.id", index=True)
    session: Optional["EventSession"] = Relationship(back_populates="program_items")

    # Metadata
    is_featured: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class EventSession(SQLModel, table=True):
    """A day-level session that holds multiple program items."""

    __tablename__ = "event_sessions"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field()  # e.g., "Day 1", "Workshop Day"

    # Day window
    start_time: datetime = Field(index=True)
    end_time: datetime

    # Owning event
    event_id: str = Field(foreign_key="events.id", index=True)
    event: Optional["Event"] = Relationship(back_populates="sessions")

    # Relationships
    program_items: list["Programm"] = Relationship(back_populates="session")
