"""FastAPI router for location-related endpoints."""

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.v1.locations import schema
from app.common.deps import get_db, require_permission
from app.common.permissions import Countries, Locations, LocationTypes
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.countries.service import CountryService
from app.features.location_types.service import LocationTypeService
from app.features.locations.service import LocationService
from app.features.users.model import User
from app.utils.pagination import PaginationParams

locations_router = APIRouter()


# =========================
# LOCATION TYPES
# =========================


@locations_router.get("/types", response_model=list[schema.LocationTypeRead])
async def list_location_types(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.List)),
):
    """List all location types with pagination."""
    service = LocationTypeService(db)
    results, total = service.list(pagination)
    return refine_list_response(response, results, total)


@locations_router.get(
    "/types/{location_type_id}", response_model=ApiResponse[schema.LocationTypeRead]
)
async def get_location_type(
    location_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.Show)),
):
    """Get a specific location type by ID."""
    service = LocationTypeService(db)
    location_type = service.get_by_id(location_type_id)
    if not location_type:
        raise ValueError(f"Location type with ID '{location_type_id}' not found")
    return ApiResponse(data=location_type)


@locations_router.post("/types", response_model=ApiResponse[schema.LocationTypeRead])
async def create_location_type(
    location_type: schema.LocationTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.Create)),
):
    """Create a new location type."""
    service = LocationTypeService(db)
    created = service.create(location_type.model_dump())
    return ApiResponse(data=created)


@locations_router.put(
    "/types/{location_type_id}", response_model=ApiResponse[schema.LocationTypeRead]
)
async def update_location_type(
    location_type_id: str,
    location_type: schema.LocationTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.Update)),
):
    """Update an existing location type."""
    service = LocationTypeService(db)
    updated = service.update(location_type_id, location_type.model_dump(exclude_unset=True))
    return ApiResponse(data=updated)


@locations_router.delete("/types/{location_type_id}", response_model=MessageResponse)
async def delete_location_type(
    location_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.Delete)),
):
    """Delete a location type."""
    service = LocationTypeService(db)
    service.delete(location_type_id)
    return MessageResponse(message="Location type deleted successfully")


@locations_router.get("/types/search/{query}", response_model=list[schema.LocationTypeRead])
async def search_location_types(
    query: str,
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(LocationTypes.List)),
):
    """Search location types by name or description."""
    service = LocationTypeService(db)
    results, total = service.search(query, pagination)
    return refine_list_response(response, results, total)


# =========================
# COUNTRIES
# =========================


@locations_router.get("/countries", response_model=list[schema.CountryRead])
async def list_countries(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.List)),
):
    """List all countries with pagination."""
    service = CountryService(db)
    results, total = service.list(pagination)
    return refine_list_response(response, results, total)


@locations_router.get(
    "/countries/devco", response_model=list[schema.CountryRead]
)
async def list_devco_countries(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.List)),
):
    """List all developing countries."""
    service = CountryService(db)
    results, total = service.list_devco(pagination)
    return refine_list_response(response, results, total)


@locations_router.get(
    "/countries/preferred", response_model=list[schema.CountryRead]
)
async def list_preferred_countries(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.List)),
):
    """List all preferred countries."""
    service = CountryService(db)
    results, total = service.list_preferred(pagination)
    return refine_list_response(response, results, total)


@locations_router.get(
    "/countries/{country_id}", response_model=ApiResponse[schema.CountryRead]
)
async def get_country(
    country_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.Show)),
):
    """Get a specific country by ID."""
    service = CountryService(db)
    country = service.get_by_id(country_id)
    if not country:
        raise ValueError(f"Country with ID '{country_id}' not found")
    return ApiResponse(data=country)


@locations_router.post("/countries", response_model=ApiResponse[schema.CountryRead])
async def create_country(
    country: schema.CountryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.Create)),
):
    """Create a new country."""
    service = CountryService(db)
    created = service.create(country.model_dump())
    return ApiResponse(data=created)


@locations_router.put(
    "/countries/{country_id}", response_model=ApiResponse[schema.CountryRead]
)
async def update_country(
    country_id: str,
    country: schema.CountryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.Update)),
):
    """Update an existing country."""
    service = CountryService(db)
    updated = service.update(country_id, country.model_dump(exclude_unset=True))
    return ApiResponse(data=updated)


@locations_router.delete("/countries/{country_id}", response_model=MessageResponse)
async def delete_country(
    country_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.Delete)),
):
    """Delete a country."""
    service = CountryService(db)
    service.delete(country_id)
    return MessageResponse(message="Country deleted successfully")


@locations_router.get("/countries/search/{query}", response_model=list[schema.CountryRead])
async def search_countries(
    query: str,
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Countries.List)),
):
    """Search countries by name or codes."""
    service = CountryService(db)
    results, total = service.search(query, pagination)
    return refine_list_response(response, results, total)


# =========================
# LOCATIONS
# =========================


@locations_router.get("", response_model=list[schema.LocationRead])
async def list_locations(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.List)),
):
    """List all locations with pagination."""
    service = LocationService(db)
    results, total = service.list(pagination)
    return refine_list_response(response, results, total)


@locations_router.get(
    "/by-country/{country_id}", response_model=list[schema.LocationRead]
)
async def list_locations_by_country(
    country_id: str,
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.List)),
):
    """List all locations in a specific country."""
    service = LocationService(db)
    results, total = service.list_by_country(country_id, pagination)
    return refine_list_response(response, results, total)


@locations_router.get(
    "/by-type/{location_type_id}", response_model=list[schema.LocationRead]
)
async def list_locations_by_type(
    location_type_id: str,
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.List)),
):
    """List all locations of a specific type."""
    service = LocationService(db)
    results, total = service.list_by_location_type(location_type_id, pagination)
    return refine_list_response(response, results, total)


@locations_router.get(
    "/by-city/{city}", response_model=list[schema.LocationRead]
)
async def list_locations_by_city(
    city: str,
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.List)),
):
    """List all locations in a specific city."""
    service = LocationService(db)
    results, total = service.list_by_city(city, pagination)
    return refine_list_response(response, results, total)


@locations_router.get("/{location_id}", response_model=ApiResponse[schema.LocationRead])
async def get_location(
    location_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.Show)),
):
    """Get a specific location by ID."""
    service = LocationService(db)
    location = service.get_by_id(location_id)
    if not location:
        raise ValueError(f"Location with ID '{location_id}' not found")
    return ApiResponse(data=location)


@locations_router.post("", response_model=ApiResponse[schema.LocationRead])
async def create_location(
    location: schema.LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.Create)),
):
    """Create a new location."""
    service = LocationService(db)
    created = service.create(location.model_dump())
    return ApiResponse(data=created)


@locations_router.put(
    "/{location_id}", response_model=ApiResponse[schema.LocationRead]
)
async def update_location(
    location_id: str,
    location: schema.LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.Update)),
):
    """Update an existing location."""
    service = LocationService(db)
    updated = service.update(location_id, location.model_dump(exclude_unset=True))
    return ApiResponse(data=updated)


@locations_router.delete("/{location_id}", response_model=MessageResponse)
async def delete_location(
    location_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.Delete)),
):
    """Delete a location."""
    service = LocationService(db)
    service.delete(location_id)
    return MessageResponse(message="Location deleted successfully")


@locations_router.get("/search/{query}", response_model=list[schema.LocationRead])
async def search_locations(
    query: str,
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.List)),
):
    """Search locations by name, city, or address fields."""
    service = LocationService(db)
    results, total = service.search(query, pagination)
    return refine_list_response(response, results, total)


@locations_router.get("/nearby", response_model=list[schema.LocationRead])
async def find_nearby_locations(
    latitude: float,
    longitude: float,
    radius_km: float = 10.0,
    response: Response = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Locations.List)),
):
    """Find locations within a certain radius of given coordinates."""
    service = LocationService(db)
    results, total = service.find_nearby(latitude, longitude, radius_km, pagination)
    return refine_list_response(response, results, total)
