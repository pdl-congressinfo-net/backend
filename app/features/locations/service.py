from pydantic import BaseModel

from app.api.v1.locations.schema import LocationUpdate
from app.common.exceptions import NotFoundError
from app.features.locations import repo
from app.features.locations.model import Country, Location, LocationType


# =========================
# LOCATION TYPE SERVICE
# =========================
def list_location_types(db, pagination):
    return repo.list_location_types(db, pagination)


def get_location_type(db, location_type_id: str):
    location_type = repo.get_location_type_by_id(db, location_type_id)
    if not location_type:
        raise NotFoundError("Location type not found")
    return location_type


def get_location_type_by_code(db, code: str):
    location_type = repo.get_location_type_by_code(db, code)
    if not location_type:
        raise NotFoundError("Location type not found")
    return location_type


def get_location_type_by_name(db, name: str):
    location_type = repo.get_location_type_by_name(db, name)
    if not location_type:
        raise NotFoundError("Location type not found")
    return location_type


def create_location_type(db, payload: BaseModel):
    location_type = LocationType.model_validate(payload)
    return repo.create_location_type(db, location_type)


def update_location_type(db, location_type_id: str, payload: BaseModel):
    location_type = repo.get_location_type_by_id(db, location_type_id)
    if not location_type:
        raise NotFoundError("Location type not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_location_type(db, location_type, updates)


def delete_location_type(db, location_type_id: str):
    location_type = repo.get_location_type_by_id(db, location_type_id)
    if not location_type:
        raise NotFoundError("Location type not found")
    repo.delete_location_type(db, location_type)


# =========================
# COUNTRY SERVICE
# =========================
def list_countries(db, pagination):
    return repo.list_countries(db, pagination)


def get_country(db, country_id: str):
    country = repo.get_country_by_id(db, country_id)
    if not country:
        raise NotFoundError("Country not found")
    return country


def get_country_by_code2(db, code2: str):
    country = repo.get_country_by_code2(db, code2)
    if not country:
        raise NotFoundError("Country not found")
    return country


def get_country_by_code3(db, code3: str):
    country = repo.get_country_by_code3(db, code3)
    if not country:
        raise NotFoundError("Country not found")
    return country


def create_country(db, payload: BaseModel):
    country = Country.model_validate(payload)
    return repo.create_country(db, country)


def update_country(db, country_id: str, payload: BaseModel):
    country = repo.get_country_by_id(db, country_id)
    if not country:
        raise NotFoundError("Country not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_country(db, country, updates)


def delete_country(db, country_id: str):
    country = repo.get_country_by_id(db, country_id)
    if not country:
        raise NotFoundError("Country not found")
    repo.delete_country(db, country)


# =========================
# LOCATION SERVICE
# =========================
def list_locations(db, pagination):
    return repo.list_locations(db, pagination)


def get_location(db, location_id: str):
    location = repo.get_location_by_id(db, location_id)
    if not location:
        raise NotFoundError("Location not found")
    return location


def get_location_by_name(db, name: str):
    location = repo.get_location_by_name(db, name)
    if not location:
        raise NotFoundError("Location not found")
    return location


def create_location(db, payload: BaseModel):
    location = Location.model_validate(payload)
    return repo.create_location(db, location)


def update_location(db, location_id: str, payload: LocationUpdate):
    location = repo.get_location_by_id(db, location_id)
    if not location:
        raise NotFoundError("Location not found")

    # Add location_type based if link is given or not
    location_type = get_location_type_by_code(db, "WEB" if payload.link else "SIT")
    if location_type:
        payload.location_type_id = location_type.id

    # Remove link when on SIT and address when WEB
    if location_type.code == "SIT":
        payload.link = None
    elif location_type.code == "WEB":
        payload.road = None
        payload.number = None
        payload.city = None
        payload.postal_code = None
        payload.latitude = None
        payload.longitude = None
        payload.country_id = None

    updates = payload.model_dump()
    return repo.update_location(db, location, updates)


def delete_location(db, location_id: str):
    location = repo.get_location_by_id(db, location_id)
    if not location:
        raise NotFoundError("Location not found")
    repo.delete_location(db, location)
