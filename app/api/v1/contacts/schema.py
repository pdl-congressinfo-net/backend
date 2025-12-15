from datetime import datetime

from pydantic import BaseModel


class ContactBase(BaseModel):
    email: str
    titles: str | None = None
    first_name: str
    last_name: str | None = None
    phone_number: str | None = None


class ContactCreate(ContactBase):
    user_id: str | None = None


class ContactUpdate(BaseModel):
    email: str | None = None
    titles: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    user_id: str | None = None


class ContactRead(ContactBase):
    id: str
    user_id: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
