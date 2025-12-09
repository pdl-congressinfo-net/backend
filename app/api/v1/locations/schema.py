"""Pydantic schemas for Location-related API endpoints."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


# LocationType Schemas
class LocationTypeBase(BaseModel):
    """Base LocationType schema with common fields."""

    name: str = Field(..., description="The name of the location type")
    description: str | None = Field(None, description="Optional description of the location type")


class LocationTypeCreate(LocationTypeBase):
    """Schema for creating a new LocationType."""

    pass


class LocationTypeUpdate(BaseModel):
    """Schema for updating an existing LocationType."""

    name: str | None = Field(None, description="The name of the location type")
    description: str | None = Field(None, description="Optional description of the location type")


class LocationTypeRead(LocationTypeBase):
    """Schema for reading a LocationType."""

    id: str = Field(..., description="The unique identifier of the location type")

    model_config = ConfigDict(from_attributes=True)


# Country Schemas
class CountryBase(BaseModel):
    """Base Country schema with common fields."""

    name: str = Field(..., description="The name of the country")
    code2: str = Field(..., min_length=2, max_length=2, description="ISO 3166-1 alpha-2 country code")
    code3: str = Field(..., min_length=3, max_length=3, description="ISO 3166-1 alpha-3 country code")
    devco: bool = Field(default=False, description="Whether this is a developing country")
    preferred: bool = Field(default=False, description="Whether this is a preferred country")

    @field_validator("code2", "code3")
    @classmethod
    def uppercase_codes(cls, v: str) -> str:
        """Convert country codes to uppercase."""
        return v.upper()


class CountryCreate(CountryBase):
    """Schema for creating a new Country."""

    pass


class CountryUpdate(BaseModel):
    """Schema for updating an existing Country."""

    name: str | None = Field(None, description="The name of the country")
    code2: str | None = Field(None, min_length=2, max_length=2, description="ISO 3166-1 alpha-2 country code")
    code3: str | None = Field(None, min_length=3, max_length=3, description="ISO 3166-1 alpha-3 country code")
    devco: bool | None = Field(None, description="Whether this is a developing country")
    preferred: bool | None = Field(None, description="Whether this is a preferred country")

    @field_validator("code2", "code3")
    @classmethod
    def uppercase_codes(cls, v: str | None) -> str | None:
        """Convert country codes to uppercase."""
        return v.upper() if v else None


class CountryRead(CountryBase):
    """Schema for reading a Country."""

    id: str = Field(..., description="The unique identifier of the country")

    model_config = ConfigDict(from_attributes=True)


# Location Schemas
class LocationBase(BaseModel):
    """Base Location schema with common fields."""

    name: str = Field(..., description="The name of the location")
    road: str | None = Field(None, description="Street or road name")
    number: str | None = Field(None, description="Street number")
    city: str | None = Field(None, description="City name")
    state: str | None = Field(None, description="State or province")
    postal_code: str | None = Field(None, description="Postal or ZIP code")
    latitude: float | None = Field(None, ge=-90, le=90, description="Latitude coordinate")
    longitude: float | None = Field(None, ge=-180, le=180, description="Longitude coordinate")
    link: str | None = Field(None, description="External link or URL")
    country_id: str = Field(..., description="UUID of the associated country")
    location_type_id: str = Field(..., description="UUID of the associated location type")


class LocationCreate(LocationBase):
    """Schema for creating a new Location."""

    pass


class LocationUpdate(BaseModel):
    """Schema for updating an existing Location."""

    name: str | None = Field(None, description="The name of the location")
    road: str | None = Field(None, description="Street or road name")
    number: str | None = Field(None, description="Street number")
    city: str | None = Field(None, description="City name")
    state: str | None = Field(None, description="State or province")
    postal_code: str | None = Field(None, description="Postal or ZIP code")
    latitude: float | None = Field(None, ge=-90, le=90, description="Latitude coordinate")
    longitude: float | None = Field(None, ge=-180, le=180, description="Longitude coordinate")
    link: str | None = Field(None, description="External link or URL")
    country_id: str | None = Field(None, description="UUID of the associated country")
    location_type_id: str | None = Field(None, description="UUID of the associated location type")


class LocationRead(LocationBase):
    """Schema for reading a Location."""

    id: str = Field(..., description="The unique identifier of the location")

    model_config = ConfigDict(from_attributes=True)


# Nested read schemas (with relationships)
class LocationTypeReadWithLocations(LocationTypeRead):
    """LocationType schema with nested locations."""

    locations: list[LocationRead] = Field(default_factory=list, description="Locations of this type")


class CountryReadWithLocations(CountryRead):
    """Country schema with nested locations."""

    locations: list[LocationRead] = Field(default_factory=list, description="Locations in this country")


class LocationReadWithRelations(LocationRead):
    """Location schema with nested country and location_type."""

    country: CountryRead | None = Field(None, description="The associated country")
    location_type: LocationTypeRead | None = Field(None, description="The associated location type")
