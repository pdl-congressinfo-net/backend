from pydantic import BaseModel


class LocationTypeBase(BaseModel):
    name: str
    description: str | None = None


class LocationTypeCreate(LocationTypeBase):
    pass


class LocationTypeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class CountryBase(BaseModel):
    name: str
    code2: str
    code3: str
    devco: bool | None = False


class CountryCreate(CountryBase):
    pass


class CountryUpdate(BaseModel):
    name: str | None = None
    code2: str | None = None
    code3: str | None = None
    devco: bool | None = None


class CountryRead(CountryBase):
    id: str
    name: str
    code2: str
    code3: str
    devco: bool | None = False


class LocationTypeRead(LocationTypeBase):
    id: str


class LocationBase(BaseModel):
    name: str
    address: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country_id: str | None = None
    location_type_id: str | None = None


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country_id: str | None = None
    location_type_id: str | None = None


class LocationRead(LocationBase):
    id: str
    name: str
    address: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country_id: str | None = None
    location_type_id: str | None = None
