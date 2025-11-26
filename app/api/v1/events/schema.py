from datetime import datetime

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class CategoryRead(CategoryBase):
    id: str

    class Config:
        from_attributes = True


class EventTypeBase(BaseModel):
    name: str
    description: str | None = None


class EventTypeCreate(EventTypeBase):
    pass


class EventTypeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class EventTypeRead(EventTypeBase):
    id: str

    class Config:
        from_attributes = True


class EventBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    is_published: bool = False

    location_id: str | None = None
    category_id: str | None = None
    event_type_id: str | None = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    is_published: bool | None = None

    location_id: str | None = None
    category_id: str | None = None
    event_type_id: str | None = None


class EventRead(EventBase):
    id: str

    class Config:
        from_attributes = True
