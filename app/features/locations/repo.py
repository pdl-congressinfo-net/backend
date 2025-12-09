"""Repository layer for Location database operations."""

from sqlalchemy.orm import Session

from app.features.locations.model import Location
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query


class LocationRepository:
    """Repository for Location CRUD operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def get_by_id(self, location_id: str) -> Location | None:
        """Retrieve a location by its ID.

        Args:
            location_id: The UUID of the location

        Returns:
            Location if found, None otherwise
        """
        return self.db.query(Location).filter(Location.id == location_id).first()

    def get_by_name(self, name: str) -> Location | None:
        """Retrieve a location by its name.

        Args:
            name: The name of the location

        Returns:
            Location if found, None otherwise
        """
        return self.db.query(Location).filter(Location.name == name).first()

    def list(self, pagination: PaginationParams):
        """List all locations with pagination.

        Args:
            pagination: Pagination parameters for the query

        Returns:
            Tuple of (list of Location objects, total count)
        """
        query = self.db.query(Location)
        return refine_query(query, Location, pagination)

    def list_by_country(
        self, country_id: str, pagination: PaginationParams
    ):
        """List all locations in a specific country.

        Args:
            country_id: The UUID of the country
            pagination: Pagination parameters

        Returns:
            Tuple of (list of Location objects, total count)
        """
        query = self.db.query(Location).filter(Location.country_id == country_id)
        return refine_query(query, Location, pagination)

    def list_by_location_type(
        self, location_type_id: str, pagination: PaginationParams
    ):
        """List all locations of a specific type.

        Args:
            location_type_id: The UUID of the location type
            pagination: Pagination parameters

        Returns:
            Tuple of (list of Location objects, total count)
        """
        query = self.db.query(Location).filter(Location.location_type_id == location_type_id)
        return refine_query(query, Location, pagination)

    def list_by_city(self, city: str, pagination: PaginationParams):
        """List all locations in a specific city.

        Args:
            city: The city name
            pagination: Pagination parameters

        Returns:
            Tuple of (list of Location objects, total count)
        """
        query = self.db.query(Location).filter(Location.city == city)
        return refine_query(query, Location, pagination)

    def create(self, location: Location) -> Location:
        """Create a new location.

        Args:
            location: Location instance to create

        Returns:
            The created Location
        """
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return location

    def update(self, location: Location) -> Location:
        """Update an existing location.

        Args:
            location: Location instance with updated data

        Returns:
            The updated Location
        """
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return location

    def delete(self, location_id: str) -> bool:
        """Delete a location by ID.

        Args:
            location_id: The UUID of the location to delete

        Returns:
            True if deleted successfully, False if not found
        """
        location = self.get_by_id(location_id)
        if location:
            self.db.delete(location)
            self.db.commit()
            return True
        return False

    def search(self, query: str, pagination: PaginationParams):
        """Search locations by name, city, or address fields.

        Args:
            query: Search string to match against various location fields
            pagination: Pagination parameters

        Returns:
            Tuple of (list of matching Location objects, total count)
        """
        db_query = self.db.query(Location).filter(
            (Location.name.ilike(f"%{query}%")) |
            (Location.city.ilike(f"%{query}%")) |
            (Location.road.ilike(f"%{query}%")) |
            (Location.state.ilike(f"%{query}%")) |
            (Location.postal_code.ilike(f"%{query}%"))
        )
        return refine_query(db_query, Location, pagination)

    def find_nearby(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
        pagination: PaginationParams
    ):
        """Find locations within a certain radius of given coordinates.

        Note: This is a simple implementation. For production use, consider
        using PostGIS or similar spatial database extensions.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius_km: Search radius in kilometers
            pagination: Pagination parameters

        Returns:
            Tuple of (list of Location objects within the radius, total count)
        """
        # Approximate degrees per km (varies by latitude)
        degree_per_km = 1 / 111.0
        lat_range = radius_km * degree_per_km
        lon_range = radius_km * degree_per_km

        db_query = self.db.query(Location).filter(
            (Location.latitude.isnot(None)) &
            (Location.longitude.isnot(None)) &
            (Location.latitude >= latitude - lat_range) &
            (Location.latitude <= latitude + lat_range) &
            (Location.longitude >= longitude - lon_range) &
            (Location.longitude <= longitude + lon_range)
        )
        return refine_query(db_query, Location, pagination)
