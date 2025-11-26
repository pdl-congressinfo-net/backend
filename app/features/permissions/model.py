import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.features.roles.model import RolePermission
from app.features.users.model import UserPermission

if TYPE_CHECKING:
    from app.features.roles.model import Role
    from app.features.users.model import User


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)

    # Relationships
    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermission
    )
    users: list["User"] = Relationship(
        back_populates="permissions", link_model=UserPermission
    )
