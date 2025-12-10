from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# =========================
# EVENT TYPE SCHEMAS
# =========================
class EventTypeBase(BaseModel):
    code: str
    name_de: str
    name_en: str
    description_de: Optional[str] = None
    description_en: Optional[str] = None


class EventTypeCreate(EventTypeBase):
    pass


class EventTypeUpdate(BaseModel):
    code: str | None = None
    name_de: str | None = None
    name_en: str | None = None
    description_de: str | None = None
    description_en: str | None = None


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
    event_type_id: Optional[str] = None
    location_id: Optional[str] = None


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
