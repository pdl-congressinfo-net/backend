from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.api.v1.locations.schema import (
    CountryRead,
    CountryUpdate,
    LocationCreate,
    LocationRead,
    LocationTypeCreate,
    LocationTypeRead,
    LocationTypeUpdate,
    LocationUpdate,
)
from app.common.deps import get_db, require_permission
from app.common.permissions import Countries, Locations, LocationTypes
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.locations.model import Country, Location, LocationType
from app.features.users.model import User
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query

locations_router = APIRouter()


@locations_router.get("/types", response_model=list[LocationTypeRead])
async def list_locations_types(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.List)),
):
    """List all locations types."""
    query = db.query(LocationType)
    results, total = refine_query(query, LocationType, pagination)
    return refine_list_response(response, results, total)


@locations_router.get(
    "/types/{location_type_id}", response_model=ApiResponse[LocationTypeRead]
)
async def get_location_type(
    location_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.Show)),
):
    """Get location type by ID."""
    location_type = (
        db.query(LocationType).filter(LocationType.id == location_type_id).first()
    )
    if not location_type:
        raise HTTPException(status_code=404, detail="Location type not found")
    return ApiResponse(data=location_type)


@locations_router.post("/types", response_model=ApiResponse[LocationTypeRead])
async def create_location_type(
    location_type: LocationTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.Create)),
):
    """Create a new location type."""
    db_location_type = LocationType.model_validate(location_type)
    db.add(db_location_type)
    db.commit()
    db.refresh(db_location_type)
    return ApiResponse(data=db_location_type)


@locations_router.put(
    "/types/{location_type_id}", response_model=ApiResponse[LocationTypeRead]
)
async def update_location_type(
    location_type_id: str,
    location_type: LocationTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.Update)),
):
    """Update an existing location type."""
    db_location_type = (
        db.query(LocationType).filter(LocationType.id == location_type_id).first()
    )
    if not db_location_type:
        raise HTTPException(status_code=404, detail="Location type not found")
    for key, value in location_type.model_dump(exclude_unset=True).items():
        setattr(db_location_type, key, value)
    db.add(db_location_type)
    db.commit()
    db.refresh(db_location_type)
    return ApiResponse(data=db_location_type)


@locations_router.delete("/types/{location_type_id}", response_model=MessageResponse)
async def delete_location_type(
    location_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.Delete)),
):
    """Delete a location type."""
    db_location_type = (
        db.query(LocationType).filter(LocationType.id == location_type_id).first()
    )
    if not db_location_type:
        raise HTTPException(status_code=404, detail="Location type not found")
    db.delete(db_location_type)
    db.commit()
    return MessageResponse(message="Location type deleted successfully")


@locations_router.get("/countries", response_model=list[CountryRead])
async def list_countries(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.List)),
):
    """List all countries."""
    query = db.query(Country)
    results, total = refine_query(query, Country, pagination)
    return refine_list_response(response, results, total)


@locations_router.get(
    "/countries/{country_id}", response_model=ApiResponse[CountryRead]
)
async def get_country(
    country_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.Show)),
):
    """Get country by ID."""
    country = db.query(Country).filter(Country.id == country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return ApiResponse(data=country)


@locations_router.post("/countries", response_model=ApiResponse[CountryRead])
async def create_country(
    country: CountryRead,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.Create)),
):
    """Create a new country."""
    db_country = Country.model_validate(country)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return ApiResponse(data=db_country)


@locations_router.put(
    "/countries/{country_id}", response_model=ApiResponse[CountryRead]
)
async def update_country(
    country_id: str,
    country: CountryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.Update)),
):
    """Update an existing country."""
    db_country = db.query(Country).filter(Country.id == country_id).first()
    if not db_country:
        raise HTTPException(status_code=404, detail="Country not found")
    for key, value in country.model_dump(exclude_unset=True).items():
        setattr(db_country, key, value)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return ApiResponse(data=db_country)


@locations_router.delete("/countries/{country_id}", response_model=MessageResponse)
async def delete_country(
    country_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.Delete)),
):
    """Delete a country."""
    db_country = db.query(Country).filter(Country.id == country_id).first()
    if not db_country:
        raise HTTPException(status_code=404, detail="Country not found")
    db.delete(db_country)
    db.commit()
    return MessageResponse(message="Country deleted successfully")


@locations_router.get("", response_model=list[LocationRead])
async def list_locations(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.List)),
):
    """List all locations."""
    query = db.query(Location)
    results, total = refine_query(query, Location, pagination)
    return refine_list_response(response, results, total)


@locations_router.get("/{location_id}", response_model=ApiResponse[LocationRead])
async def get_location(
    location_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.Show)),
):
    """Get location by ID."""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return ApiResponse(data=location)


@locations_router.post("", response_model=ApiResponse[LocationRead])
async def create_location(
    location: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.Create)),
):
    """Create a new location."""
    db_location = Location.model_validate(location)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return ApiResponse(data=db_location)


@locations_router.put("/{location_id}", response_model=ApiResponse[LocationRead])
async def update_location(
    location_id: str,
    location: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.Update)),
):
    """Update an existing location."""
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    for key, value in location.model_dump(exclude_unset=True).items():
        setattr(db_location, key, value)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return ApiResponse(data=db_location)


@locations_router.delete("/{location_id}", response_model=MessageResponse)
async def delete_location(
    location_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.Delete)),
):
    """Delete a location."""
    db_location = db.query(Location).filter(Location.id == permission_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(db_location)
    db.commit()
    return MessageResponse(message="Location deleted successfully")
