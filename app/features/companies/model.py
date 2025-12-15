import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.features.events.model import Event
    from app.features.locations.model import Location
    from app.features.users.model import Contact


class Sponsoring(SQLModel, table=True):
    __tablename__ = "sponsorings"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str
    value: float = Field(default=0.0)

    employee_id: Optional[str] = Field(default=None, foreign_key="company_employees.id")  # noqa: UP045
    event_id: Optional[str] = Field(default=None, foreign_key="events.id")  # noqa: UP045
    company_id: Optional[str] = Field(default=None, foreign_key="companies.id")  # noqa: UP045

    events: Optional["Event"] = Relationship(back_populates="sponsorings")  # noqa: UP045
    employee: Optional["CompanyEmployee"] = Relationship(back_populates="sponsorings")
    company: Optional["Company"] = Relationship(back_populates="sponsorings")


class CompanyEmployee(SQLModel, table=True):
    __tablename__ = "company_employees"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    departement: Optional[str] = None  # noqa: UP045
    function: Optional[str] = None  # noqa: UP045

    contact_id: Optional[str] = Field(default=None, foreign_key="contacts.id")  # noqa: UP045
    company_id: Optional[str] = Field(default=None, foreign_key="companies.id")  # noqa: UP045

    company: Optional["Company"] = Relationship(back_populates="employees")
    contact: Optional["Contact"] = Relationship(back_populates="company_employee")
    sponsorings: List["Sponsoring"] = Relationship(back_populates="employee")  # noqa: UP006


class Company(SQLModel, table=True):
    __tablename__ = "companies"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)
    sponsoring: bool = Field(default=False)
    location_id: Optional[str] = Field(default=None, foreign_key="locations.id")  # noqa: UP045

    location: Optional["Location"] = Relationship(back_populates="company")  # noqa: UP045
    employees: List["CompanyEmployee"] = Relationship(back_populates="company")  # noqa: UP006
    sponsorings: List["Sponsoring"] = Relationship(back_populates="company")  # noqa: UP006
