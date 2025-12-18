import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import inspect
from sqlmodel import Field, Relationship, SQLModel

from app.core.config import settings

if TYPE_CHECKING:
    from app.features.companies.model import CompanyEmployee
    from app.features.permissions.model import ObjectPermission, Permission
    from app.features.roles.model import Role


# Link tables for many-to-many relationships
class UserRole(SQLModel, table=True):
    __tablename__ = "user_roles"
    user_id: str = Field(foreign_key="users.id", primary_key=True, max_length=36)
    role_id: str = Field(foreign_key="roles.id", primary_key=True, max_length=36)


class UserPermission(SQLModel, table=True):
    __tablename__ = "user_permissions"
    user_id: str = Field(foreign_key="users.id", primary_key=True, max_length=36)
    permission_id: str = Field(
        foreign_key="permissions.id", primary_key=True, max_length=36
    )


class Contact(SQLModel, table=True):
    __tablename__ = "contacts"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    email: str = Field(index=True, unique=True)
    titles: str | None = Field(default=None)  # noqa: UP007
    first_name: str  # noqa: UP007
    last_name: str | None = Field(default=None)  # noqa: UP007
    phone_number: str | None = Field(default=None)

    user_id: str | None = Field(foreign_key="users.id", index=True, nullable=True)
    user: Optional["User"] = Relationship(back_populates="contact")

    created_at: datetime = Field(default_factory=datetime.utcnow)

    company_employee: Optional["CompanyEmployee"] = Relationship(
        back_populates="contact"
    )


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: datetime | None = None  # noqa: UP007
    oeak_id: int | None = Field(default=None, index=True)  # noqa: UP007

    # Relationships
    roles: list["Role"] = Relationship(back_populates="users", link_model=UserRole)
    permissions: list["Permission"] = Relationship(
        back_populates="users", link_model=UserPermission
    )
    object_permissions: list["ObjectPermission"] = Relationship(back_populates="user")
    login_otps: list["LoginOTP"] = Relationship(back_populates="user")
    contact: Optional["Contact"] = Relationship(back_populates="user")  # noqa: UP006

    def _assert_roles_loaded(self) -> None:
        state = inspect(self)
        if "roles" in state.unloaded:
            raise RuntimeError("User roles are not loaded")

    def has_role(self, role_name: str) -> bool:
        self._assert_roles_loaded()
        return any(r.name == role_name for r in self.roles)

    def can_bypass_object_scopes(self, resource: str, action: str) -> bool:
        self._assert_roles_loaded()
        if self.has_role(settings.SYSTEM_ADMIN_ROLE_NAME):
            return True

        return any(role.bypass_object_scope for role in self.roles)

    def _assert_permissions_loaded(self) -> None:
        state = inspect(self)
        if "permissions" in state.unloaded:
            raise RuntimeError("User permissions are not loaded")

    def has_permission(self, permission_name: str) -> bool:
        self._assert_permissions_loaded()
        return any(p.name == permission_name for p in self.permissions)

    def effective_permissions(self) -> list["Permission"]:
        self._assert_permissions_loaded()
        self._assert_roles_loaded()
        perms: dict[str, Permission] = {}

        # direct user permissions
        for perm in self.permissions:
            perms[perm.id] = perm

        # role permissions
        for role in self.roles:
            for perm in role.permissions:
                perms.setdefault(perm.id, perm)

        return perms.values()


class LoginOTP(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True, nullable=True)

    email: str = Field(index=True)
    otp_code: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime = Field()
    resend_available_at: datetime = Field()
    used: bool = Field(default=False)

    user: Optional["User"] = Relationship(back_populates="login_otps")
