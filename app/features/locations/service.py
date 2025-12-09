"""Service layer for Location business logic."""

from sqlmodel import Session

from app.utils.pagination import PaginationParams
from app.features.countries.repo import CountryRepository
from app.features.location_types.repo import LocationTypeRepository
from app.features.locations.model import Location
from app.features.locations.repo import LocationRepository


class LocationService:
    """Service for Location business logic operations."""

    def __init__(self, db: Session):
        """Initialize service with database session.

        Args:
            db: SQLModel database session
        """
        self.repo = LocationRepository(db)
        self.country_repo = CountryRepository(db)
        self.location_type_repo = LocationTypeRepository(db)

    def get_by_id(self, location_id: str) -> Location | None:
        """Retrieve a location by its ID.

        Args:
            location_id: The UUID of the location

        Returns:
            Location if found, None otherwise
        """
        return self.repo.get_by_id(location_id)

    def get_by_name(self, name: str) -> Location | None:
        """Retrieve a location by its name.

        Args:
            name: The name of the location

        Returns:
            Location if found, None otherwise
        """
        return self.repo.get_by_name(name)

    def list(self, pagination: PaginationParams) -> list[Location]:
        """List all locations with pagination.

        Args:
            pagination: Pagination parameters for the query

        Returns:
            List of Location objects
        """
        return self.repo.list(pagination)

    def list_by_country(
        self, country_id: str, pagination: PaginationParams
    ) -> list[Location]:
        """List all locations in a specific country.

        Args:
            country_id: The UUID of the country
            pagination: Pagination parameters

        Returns:
            List of Location objects
        """
        return self.repo.list_by_country(country_id, pagination)

    def list_by_location_type(
        self, location_type_id: str, pagination: PaginationParams
    ) -> list[Location]:
        """List all locations of a specific type.

        Args:
            location_type_id: The UUID of the location type
            pagination: Pagination parameters

        Returns:
            List of Location objects
        """
        return self.repo.list_by_location_type(location_type_id, pagination)

    def list_by_city(self, city: str, pagination: PaginationParams) -> list[Location]:
        """List all locations in a specific city.

        Args:
            city: The city name
            pagination: Pagination parameters

        Returns:
            List of Location objects
        """
        return self.repo.list_by_city(city, pagination)

    def create(self, location_data: dict) -> Location:
        """Create a new location with validation.

        Args:
            location_data: Dictionary containing location data

        Returns:
            The created Location

        Raises:
            ValueError: If validation fails or referenced entities don't exist
        """
        # Check for duplicate name
        existing = self.repo.get_by_name(location_data.get("name", ""))
        if existing:
            raise ValueError(f"Location with name '{location_data['name']}' already exists")

        # Validate country exists
        country_id = location_data.get("country_id")
        if country_id:
            country = self.country_repo.get_by_id(country_id)
            if not country:
                raise ValueError(f"Country with ID '{country_id}' not found")
        else:
            raise ValueError("country_id is required")

        # Validate location type exists
        location_type_id = location_data.get("location_type_id")
        if location_type_id:
            location_type = self.location_type_repo.get_by_id(location_type_id)
            if not location_type:
                raise ValueError(f"Location type with ID '{location_type_id}' not found")
        else:
            raise ValueError("location_type_id is required")

        # Validate coordinates if provided
        latitude = location_data.get("latitude")
        longitude = location_data.get("longitude")
        if latitude is not None:
            if not -90 <= latitude <= 90:
                raise ValueError("Latitude must be between -90 and 90 degrees")
        if longitude is not None:
            if not -180 <= longitude <= 180:
                raise ValueError("Longitude must be between -180 and 180 degrees")

        location = Location(**location_data)
        return self.repo.create(location)

    def update(self, location_id: str, location_data: dict) -> Location:
        """Update an existing location with validation.

        Args:
            location_id: The UUID of the location to update
            location_data: Dictionary containing updated location data

        Returns:
            The updated Location

        Raises:
            ValueError: If location not found or validation fails
        """
        location = self.repo.get_by_id(location_id)
        if not location:
            raise ValueError(f"Location with ID '{location_id}' not found")

        # Check for duplicate name if name is being changed
        if "name" in location_data and location_data["name"] != location.name:
            existing = self.repo.get_by_name(location_data["name"])
            if existing:
                raise ValueError(f"Location with name '{location_data['name']}' already exists")

        # Validate country exists if being changed
        if "country_id" in location_data and location_data["country_id"] != location.country_id:
            country = self.country_repo.get_by_id(location_data["country_id"])
            if not country:
                raise ValueError(f"Country with ID '{location_data['country_id']}' not found")

        # Validate location type exists if being changed
        if "location_type_id" in location_data and location_data["location_type_id"] != location.location_type_id:
            location_type = self.location_type_repo.get_by_id(location_data["location_type_id"])
            if not location_type:
                raise ValueError(f"Location type with ID '{location_data['location_type_id']}' not found")

        # Validate coordinates if provided
        if "latitude" in location_data and location_data["latitude"] is not None:
            if not -90 <= location_data["latitude"] <= 90:
                raise ValueError("Latitude must be between -90 and 90 degrees")
        if "longitude" in location_data and location_data["longitude"] is not None:
            if not -180 <= location_data["longitude"] <= 180:
                raise ValueError("Longitude must be between -180 and 180 degrees")

        # Update fields
        for key, value in location_data.items():
            if hasattr(location, key):
                setattr(location, key, value)

        return self.repo.update(location)

    def delete(self, location_id: str) -> bool:
        """Delete a location by ID.

        Args:
            location_id: The UUID of the location to delete

        Returns:
            True if deleted successfully

        Raises:
            ValueError: If location not found or has associated events
        """
        location = self.repo.get_by_id(location_id)
        if not location:
            raise ValueError(f"Location with ID '{location_id}' not found")

        # Check if location has associated events
        if location.events:
            raise ValueError(
                f"Cannot delete location '{location.name}' as it has {len(location.events)} associated events"
            )

        return self.repo.delete(location_id)

    def search(self, query: str, pagination: PaginationParams) -> list[Location]:
        """Search locations by name, city, or address fields.

        Args:
            query: Search string to match against various location fields
            pagination: Pagination parameters

        Returns:
            List of matching Location objects
        """
        return self.repo.search(query, pagination)

    def find_nearby(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
        pagination: PaginationParams
    ) -> list[Location]:
        """Find locations within a certain radius of given coordinates.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius_km: Search radius in kilometers
            pagination: Pagination parameters

        Returns:
            List of Location objects within the radius

        Raises:
            ValueError: If coordinates are invalid
        """
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")
        if radius_km <= 0:
            raise ValueError("Radius must be greater than 0")

        return self.repo.find_nearby(latitude, longitude, radius_km, pagination)
