from datetime import datetime

from pydantic import BaseModel

from app.features.programm.model import ProgrammType


# =========================
# PROGRAMM SCHEMAS
# =========================
class ProgrammBase(BaseModel):
    title: str
    description: str | None = None
    type: ProgrammType = ProgrammType.LECTURE
    location_id: str | None = None
    capacity: int | None = None
    start_time: datetime
    end_time: datetime
    level: str | None = None
    speaker_id: str | None = None
    tags: str | None = None
    session_id: str
    is_featured: bool = False


class ProgrammCreate(ProgrammBase):
    pass


class ProgrammUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    type: ProgrammType | None = None
    location_id: str | None = None
    capacity: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    level: str | None = None
    speaker_id: str | None = None
    tags: str | None = None
    session_id: str | None = None
    is_featured: bool | None = None


class ProgrammRead(ProgrammBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# =========================
# EVENT SESSION SCHEMAS
# =========================
class EventSessionBase(BaseModel):
    name: str
    start_time: datetime
    end_time: datetime
    event_id: str


class EventSessionCreate(EventSessionBase):
    pass


class EventSessionUpdate(BaseModel):
    name: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    event_id: str | None = None


class EventSessionRead(EventSessionBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
