import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.features.events.model import Event


class LocationType(SQLModel, table=True):
    __tablename__ = "location_types"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)
    description: str | None = None  # noqa: UP007

    locations: list["Location"] = Relationship(back_populates="location_type")


class Country(SQLModel, table=True):
    __tablename__ = "countries"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)
    code2: str = Field(unique=True, index=True, max_length=2)
    code3: str = Field(unique=True, index=True, max_length=3)
    devco: bool | None = Field(default=False)  # noqa: UP007
    preferred: bool | None = Field(default=False)  # noqa: UP007

    locations: list["Location"] = Relationship(back_populates="country")


class Location(SQLModel, table=True):
    __tablename__ = "locations"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)
    road: str | None = None  # noqa: UP007
    number: str | None = None  # noqa: UP007
    city: str | None = None  # noqa: UP007
    state: str | None = None  # noqa: UP007
    postal_code: str | None = None  # noqa: UP007
    latitude: float | None = None  # noqa: UP007
    longitude: float | None = None  # noqa: UP007
    link: str | None = None  # noqa: UP007

    country_id: str | None = Field(default=None, foreign_key="countries.id")  # noqa: UP007
    location_type_id: str | None = Field(default=None, foreign_key="location_types.id")  # noqa: UP007

    country: Country | None = Relationship(back_populates="locations")  # noqa: UP007
    location_type: LocationType | None = Relationship(back_populates="locations")  # noqa: UP007
    events: list["Event"] = Relationship(back_populates="location")
