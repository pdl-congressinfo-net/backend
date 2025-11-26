import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.features.users.model import UserRole

if TYPE_CHECKING:
    from app.features.permissions.model import Permission
    from app.features.users.model import User


class RolePermission(SQLModel, table=True):
    __tablename__ = "role_permissions"
    role_id: str = Field(foreign_key="roles.id", primary_key=True, max_length=36)
    permission_id: str = Field(
        foreign_key="permissions.id", primary_key=True, max_length=36
    )


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)

    # Relationships
    permissions: list["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermission
    )
    users: list["User"] = Relationship(back_populates="roles", link_model=UserRole)
