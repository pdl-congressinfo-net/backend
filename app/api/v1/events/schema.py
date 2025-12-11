from datetime import datetime

from pydantic import BaseModel


# =========================
# EVENT TYPE SCHEMAS
# =========================
class EventTypeBase(BaseModel):
    code: str


class EventTypeCreate(EventTypeBase):
    pass


class EventTypeUpdate(BaseModel):
    code: str | None = None


class EventTypeRead(EventTypeBase):
    id: str

    class Config:
        from_attributes = True


# =========================
# EVENT SCHEMAS
# =========================
class EventBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    is_public: bool = False
    event_type_id: str | None = None
    location_id: str | None = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    is_public: bool | None = None
    event_type_id: str | None = None
    location_id: str | None = None


class EventRead(EventBase):
    id: str

    class Config:
        from_attributes = True
