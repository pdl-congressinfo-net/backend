import uuid
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.features.events.model import Event


class LocationType(SQLModel, table=True):
    __tablename__ = "location_types"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)

    locations: list["Location"] = Relationship(back_populates="location_type")


class Country(SQLModel, table=True):
    __tablename__ = "countries"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)
    code2: str = Field(unique=True, index=True, max_length=2)
    code3: str = Field(unique=True, index=True, max_length=3)
    devco: Optional[bool] = Field(default=False)
    preferred: Optional[bool] = Field(default=False)

    locations: list["Location"] = Relationship(back_populates="country")


class Location(SQLModel, table=True):
    __tablename__ = "locations"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36
    )
    name: str = Field(unique=True, index=True)
    road: Optional[str] = None
    number: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    link: Optional[str] = None

    country_id: Optional[str] = Field(default=None, foreign_key="countries.id")
    location_type_id: Optional[str] = Field(default=None, foreign_key="location_types.id")

    country: Optional[Country] = Relationship(back_populates="locations")
    location_type: Optional[LocationType] = Relationship(back_populates="locations")
    events: list["Event"] = Relationship(back_populates="location")
