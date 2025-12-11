from pydantic import BaseModel


# =========================
# LOCATION TYPE SCHEMAS
# =========================
class LocationTypeBase(BaseModel):
    name: str


class LocationTypeCreate(LocationTypeBase):
    pass


class LocationTypeUpdate(BaseModel):
    name: str | None = None


class LocationTypeRead(LocationTypeBase):
    id: str

    class Config:
        from_attributes = True


# =========================
# COUNTRY SCHEMAS
# =========================
class CountryBase(BaseModel):
    name: str
    code2: str
    code3: str
    devco: bool = False
    preferred: bool | None = False


class CountryCreate(CountryBase):
    pass


class CountryUpdate(BaseModel):
    name: str | None = None
    code2: str | None = None
    code3: str | None = None
    devco: bool | None = None
    preferred: bool | None = None


class CountryRead(CountryBase):
    id: str

    class Config:
        from_attributes = True


# =========================
# LOCATION SCHEMAS
# =========================
class LocationBase(BaseModel):
    name: str
    road: str | None = None
    number: str | None = None
    city: str | None = None
    postal_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    link: str | None = None
    country_id: str | None = None
    location_type_id: str | None = None


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: str | None = None
    road: str | None = None
    number: str | None = None
    city: str | None = None
    postal_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    link: str | None = None
    country_id: str | None = None
    location_type_id: str | None = None


class LocationRead(LocationBase):
    id: str

    class Config:
        from_attributes = True
