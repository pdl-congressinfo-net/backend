import uuid
from typing import TYPE_CHECKING

from sqlalchemy import inspect
from sqlmodel import Field, Relationship, SQLModel

from app.features.roles.model import RolePermission
from app.features.users.model import UserPermission

if TYPE_CHECKING:
    from app.features.roles.model import Role
    from app.features.users.model import User


class ObjectPermission(SQLModel, table=True):
    __tablename__ = "object_permissions"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    user_id: str = Field(foreign_key="users.id", index=True, max_length=36)
    resource: str = Field(index=True)
    object_id: str = Field(index=True, max_length=36)

    can_show: bool = False
    can_update: bool = False
    can_delete: bool = False

    user: "User" = Relationship(back_populates="object_permissions")

    def _assert_user_loaded(self) -> None:
        state = inspect(self)
        if "user" in state.unloaded:
            raise RuntimeError("User is not loaded in Object Permission")

    def is_user(self, user_id: str) -> bool:
        self._assert_user_loaded()
        return self.user.id == user_id

    def show(self) -> bool:
        return self.can_show

    def update(self) -> bool:
        return self.can_update

    def delete(self) -> bool:
        return self.can_delete


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)

    allow_object_bypass: bool = Field(default=False)

    # Relationships
    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermission
    )
    users: list["User"] = Relationship(
        back_populates="permissions", link_model=UserPermission
    )
