"""Service layer for LocationType business logic."""

from sqlmodel import Session

from app.utils.pagination import PaginationParams
from app.features.location_types.repo import LocationTypeRepository
from app.features.locations.model import LocationType


class LocationTypeService:
    """Service for LocationType business logic operations."""

    def __init__(self, db: Session):
        """Initialize service with database session.

        Args:
            db: SQLModel database session
        """
        self.repo = LocationTypeRepository(db)

    def get_by_id(self, location_type_id: str) -> LocationType | None:
        """Retrieve a location type by its ID.

        Args:
            location_type_id: The UUID of the location type

        Returns:
            LocationType if found, None otherwise
        """
        return self.repo.get_by_id(location_type_id)

    def get_by_name(self, name: str) -> LocationType | None:
        """Retrieve a location type by its name.

        Args:
            name: The name of the location type

        Returns:
            LocationType if found, None otherwise
        """
        return self.repo.get_by_name(name)

    def list(self, pagination: PaginationParams) -> list[LocationType]:
        """List all location types with pagination.

        Args:
            pagination: Pagination parameters for the query

        Returns:
            List of LocationType objects
        """
        return self.repo.list(pagination)

    def create(self, location_type_data: dict) -> LocationType:
        """Create a new location type with validation.

        Args:
            location_type_data: Dictionary containing location type data

        Returns:
            The created LocationType

        Raises:
            ValueError: If a location type with the same name already exists
        """
        # Check for duplicate name
        existing = self.repo.get_by_name(location_type_data.get("name", ""))
        if existing:
            raise ValueError(f"Location type with name '{location_type_data['name']}' already exists")

        location_type = LocationType(**location_type_data)
        return self.repo.create(location_type)

    def update(self, location_type_id: str, location_type_data: dict) -> LocationType:
        """Update an existing location type with validation.

        Args:
            location_type_id: The UUID of the location type to update
            location_type_data: Dictionary containing updated location type data

        Returns:
            The updated LocationType

        Raises:
            ValueError: If location type not found or name conflict exists
        """
        location_type = self.repo.get_by_id(location_type_id)
        if not location_type:
            raise ValueError(f"Location type with ID '{location_type_id}' not found")

        # Check for duplicate name if name is being changed
        if "name" in location_type_data and location_type_data["name"] != location_type.name:
            existing = self.repo.get_by_name(location_type_data["name"])
            if existing:
                raise ValueError(f"Location type with name '{location_type_data['name']}' already exists")

        # Update fields
        for key, value in location_type_data.items():
            if hasattr(location_type, key):
                setattr(location_type, key, value)

        return self.repo.update(location_type)

    def delete(self, location_type_id: str) -> bool:
        """Delete a location type by ID.

        Args:
            location_type_id: The UUID of the location type to delete

        Returns:
            True if deleted successfully

        Raises:
            ValueError: If location type not found or has associated locations
        """
        location_type = self.repo.get_by_id(location_type_id)
        if not location_type:
            raise ValueError(f"Location type with ID '{location_type_id}' not found")

        # Check if location type has associated locations
        if location_type.locations:
            raise ValueError(
                f"Cannot delete location type '{location_type.name}' as it has {len(location_type.locations)} associated locations"
            )

        return self.repo.delete(location_type_id)

    def search(self, query: str, pagination: PaginationParams) -> list[LocationType]:
        """Search location types by name or description.

        Args:
            query: Search string to match against name or description
            pagination: Pagination parameters

        Returns:
            List of matching LocationType objects
        """
        return self.repo.search(query, pagination)
