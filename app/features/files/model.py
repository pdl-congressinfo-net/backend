import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.features.users.model import User


class File(SQLModel, table=True):
    __tablename__ = "file"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(index=True)
    size: int = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()
    uploaded_by_id: str = Field(foreign_key="users.id", max_length=36)
    location: str = Field(index=True)
    external: bool = Field(default=False)

    uploaded_by: "User" = Relationship(back_populates="files")
