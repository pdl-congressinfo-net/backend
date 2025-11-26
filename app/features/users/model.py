import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.features.permissions.model import Permission
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


# Main models
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    email: str = Field(unique=True, index=True)
    full_name: str | None = None
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: datetime | None = None

    # Relationships
    roles: list["Role"] = Relationship(back_populates="users", link_model=UserRole)
    permissions: list["Permission"] = Relationship(
        back_populates="users", link_model=UserPermission
    )
    login_otps: list["LoginOTP"] = Relationship(back_populates="user")


class LoginOTP(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True, nullable=True)

    email: str = Field(index=True)
    otp_code: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime = Field()
    resend_available_at: datetime = Field()
    used: bool = Field(default=False)

    user: User | None = Relationship(back_populates="login_otps")
