from fastapi import APIRouter, Depends, Response
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
from app.features.locations import service
from app.features.users.model import User
from app.utils.pagination import PaginationParams

locations_router = APIRouter()


@locations_router.get("/types", response_model=list[LocationTypeRead])
async def list_locations_types(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.List)),
):
    """List all locations types."""
    location_types, total = service.list_location_types(db, pagination)
    return refine_list_response(response, location_types, total)


@locations_router.get(
    "/types/{location_type_id}", response_model=ApiResponse[LocationTypeRead]
)
async def get_location_type(
    location_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.Show)),
):
    """Get location type by ID."""
    location_type = service.get_location_type(db, location_type_id)
    return ApiResponse(data=location_type)


@locations_router.post("/types", response_model=ApiResponse[LocationTypeRead])
async def create_location_type(
    location_type: LocationTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.Create)),
):
    """Create a new location type."""
    db_location_type = service.create_location_type(db, location_type)
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
    db_location_type = service.update_location_type(db, location_type_id, location_type)
    return ApiResponse(data=db_location_type)


@locations_router.delete("/types/{location_type_id}", response_model=MessageResponse)
async def delete_location_type(
    location_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.Delete)),
):
    """Delete a location type."""
    service.delete_location_type(db, location_type_id)
    return MessageResponse(message="Location type deleted successfully")


@locations_router.get("/countries", response_model=list[CountryRead])
async def list_countries(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.List)),
):
    """List all countries."""
    countries, total = service.list_countries(db, pagination)
    return refine_list_response(response, countries, total)


@locations_router.get(
    "/countries/{country_id}", response_model=ApiResponse[CountryRead]
)
async def get_country(
    country_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.Show)),
):
    """Get country by ID."""
    country = service.get_country(db, country_id)
    return ApiResponse(data=country)


@locations_router.post("/countries", response_model=ApiResponse[CountryRead])
async def create_country(
    country: CountryRead,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.Create)),
):
    """Create a new country."""
    db_country = service.create_country(db, country)
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
    db_country = service.update_country(db, country_id, country)
    return ApiResponse(data=db_country)


@locations_router.delete("/countries/{country_id}", response_model=MessageResponse)
async def delete_country(
    country_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.Delete)),
):
    """Delete a country."""
    service.delete_country(db, country_id)
    return MessageResponse(message="Country deleted successfully")


@locations_router.get("", response_model=list[LocationRead])
async def list_locations(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.List)),
):
    """List all locations."""
    results, total = service.list_locations(db, pagination)
    return refine_list_response(response, results, total)


@locations_router.get("/{location_id}", response_model=ApiResponse[LocationRead])
async def get_location(
    location_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.Show)),
):
    """Get location by ID."""
    location = service.get_location(db, location_id)
    return ApiResponse(data=location)


@locations_router.post("", response_model=ApiResponse[LocationRead])
async def create_location(
    location: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.Create)),
):
    """Create a new location."""
    db_location = service.create_location(db, location)
    return ApiResponse(data=db_location)


@locations_router.put("/{location_id}", response_model=ApiResponse[LocationRead])
async def update_location(
    location_id: str,
    location: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.Update)),
):
    """Update an existing location."""
    db_location = service.update_location(db, location_id, location)
    return ApiResponse(data=db_location)


@locations_router.delete("/{location_id}", response_model=MessageResponse)
async def delete_location(
    location_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.Delete)),
):
    """Delete a location."""
    service.delete_location(db, location_id)
    return MessageResponse(message="Location deleted successfully")
