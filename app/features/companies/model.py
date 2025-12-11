import uuid
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.features.locations.model import Location
from app.features.users.model import User


class CompanyEmployee(SQLModel, table=True):
    __tablename__ = "company_employees"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    departement: Optional[str] = None  # noqa: UP045
    function: Optional[str] = None  # noqa: UP045

    user_id: Optional[str] = Field(default=None, foreign_key="users.id")  # noqa: UP045
    company_id: Optional[str] = Field(default=None, foreign_key="companies.id")  # noqa: UP045

    company: Optional["Company"] = Relationship(back_populates="employees")
    user: Optional["User"] = Relationship(back_populates="company_employee")


class Company(SQLModel, table=True):
    __tablename__ = "companies"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)
    sponsoring: bool = Field(default=False)
    location_id: Optional[str] = Field(default=None, foreign_key="locations.id")  # noqa: UP045

    locations: Optional[Location] = Relationship(back_populates="company")  # noqa: UP045
    employees: List["CompanyEmployee"] = Relationship(back_populates="company")  # noqa: UP006
