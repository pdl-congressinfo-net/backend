from datetime import datetime

from pydantic import BaseModel


class CategoryBase(BaseModel):
    code: str
    name_de: str
    name_en: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    code: str | None = None
    name_de: str | None = None
    name_en: str | None = None


class CategoryRead(CategoryBase):
    id: str

    class Config:
        from_attributes = True


class EventTypeBase(BaseModel):
    code: str
    name_de: str
    name_en: str
    description_de: str | None = None
    description_en: str | None = None


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


class EventBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    is_published: bool = False

    location_id: str | None = None
    category_id: str | None = None
    file_id: str | None = None
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
    file_id: str | None = None
    event_type_id: str | None = None


class EventRead(EventBase):
    id: str

    class Config:
        from_attributes = True
