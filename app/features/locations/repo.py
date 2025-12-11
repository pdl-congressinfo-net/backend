from sqlalchemy.orm import Session

from app.features.locations.model import Country, Location, LocationType
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query


# =========================
# LOCATION TYPE REPO
# =========================
def list_location_types(db: Session, pagination: PaginationParams):
    query = db.query(LocationType)
    return refine_query(query, LocationType, pagination)


def get_location_type_by_id(db: Session, location_type_id: str):
    return db.query(LocationType).filter(LocationType.id == location_type_id).first()


def get_location_type_by_code(db: Session, code: str):
    return db.query(LocationType).filter(LocationType.code == code).first()


def get_location_type_by_name(db: Session, name: str):
    return db.query(LocationType).filter(LocationType.name == name).first()


def create_location_type(db: Session, location_type: LocationType):
    db.add(location_type)
    db.commit()
    db.refresh(location_type)
    return location_type


def update_location_type(db: Session, location_type: LocationType, updates: dict):
    for key, value in updates.items():
        setattr(location_type, key, value)
    db.commit()
    db.refresh(location_type)
    return location_type


def delete_location_type(db: Session, location_type: LocationType):
    db.delete(location_type)
    db.commit()


# =========================
# COUNTRY REPO
# =========================
def list_countries(db: Session, pagination: PaginationParams):
    query = db.query(Country)
    return refine_query(query, Country, pagination)


def get_country_by_id(db: Session, country_id: str):
    return db.query(Country).filter(Country.id == country_id).first()


def get_country_by_code2(db: Session, code2: str):
    return db.query(Country).filter(Country.code2 == code2).first()


def get_country_by_code3(db: Session, code3: str):
    return db.query(Country).filter(Country.code3 == code3).first()


def create_country(db: Session, country: Country):
    db.add(country)
    db.commit()
    db.refresh(country)
    return country


def update_country(db: Session, country: Country, updates: dict):
    for key, value in updates.items():
        setattr(country, key, value)
    db.commit()
    db.refresh(country)
    return country


def delete_country(db: Session, country: Country):
    db.delete(country)
    db.commit()


# =========================
# LOCATION REPO
# =========================
def list_locations(db: Session, pagination: PaginationParams):
    query = db.query(Location)
    return refine_query(query, Location, pagination)


def get_location_by_id(db: Session, location_id: str):
    return db.query(Location).filter(Location.id == location_id).first()


def get_location_by_name(db: Session, name: str):
    return db.query(Location).filter(Location.name == name).first()


def create_location(db: Session, location: Location):
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def update_location(db: Session, location: Location, updates: dict):
    for key, value in updates.items():
        setattr(location, key, value)
    db.commit()
    db.refresh(location)
    return location


def delete_location(db: Session, location: Location):
    db.delete(location)
    db.commit()
