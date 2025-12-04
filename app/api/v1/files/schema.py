from datetime import datetime

from pydantic import BaseModel


class FileBase(BaseModel):
    name: str
    size: int
    uploaded_by: str
    created_at: datetime
    updated_at: datetime
    location: str
    external: bool


class FileCreate(FileBase):
    pass


class FileUpdate(BaseModel):
    name: str | None = None
    size: int | None = None
    uploaded_by: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    location: str | None = None
    external: bool | None = None


class FileRead(FileBase):
    id: str

    class Config:
        from_attributes = True
