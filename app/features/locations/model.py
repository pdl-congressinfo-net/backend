import uuid
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.features.companies.model import Company
    from app.features.events.model import Event


class LocationType(SQLModel, table=True):
    __tablename__ = "location_types"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    code: str = Field(unique=True, index=True, max_length=3, min_length=3)

    locations: list["Location"] = Relationship(back_populates="location_type")


class Country(SQLModel, table=True):
    __tablename__ = "countries"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)
    code2: str = Field(unique=True, index=True, max_length=2)
    code3: str = Field(unique=True, index=True, max_length=3)
    devco: bool | None = Field(default=False)
    preferred: bool | None = Field(default=False)

    locations: list["Location"] = Relationship(back_populates="country")


class Location(SQLModel, table=True):
    __tablename__ = "locations"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)
    road: str | None = None
    number: str | None = None
    city: str | None = None
    postal_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    link: str | None = None

    country_id: str | None = Field(default=None, foreign_key="countries.id")
    location_type_id: str | None = Field(default=None, foreign_key="location_types.id")

    country: Country | None = Relationship(back_populates="locations")
    location_type: LocationType | None = Relationship(back_populates="locations")
    events: list["Event"] = Relationship(back_populates="location")
    company: Optional["Company"] = Relationship(back_populates="location")  # noqa: UP006
