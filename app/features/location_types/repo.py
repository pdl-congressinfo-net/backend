"""Repository layer for LocationType database operations."""

from sqlalchemy.orm import Session

from app.features.locations.model import LocationType
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query


class LocationTypeRepository:
    """Repository for LocationType CRUD operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def get_by_id(self, location_type_id: str) -> LocationType | None:
        """Retrieve a location type by its ID.

        Args:
            location_type_id: The UUID of the location type

        Returns:
            LocationType if found, None otherwise
        """
        return self.db.query(LocationType).filter(LocationType.id == location_type_id).first()

    def get_by_name(self, name: str) -> LocationType | None:
        """Retrieve a location type by its name.

        Args:
            name: The name of the location type

        Returns:
            LocationType if found, None otherwise
        """
        return self.db.query(LocationType).filter(LocationType.name == name).first()

    def list(self, pagination: PaginationParams):
        """List all location types with pagination.

        Args:
            pagination: Pagination parameters for the query

        Returns:
            Tuple of (list of LocationType objects, total count)
        """
        query = self.db.query(LocationType)
        return refine_query(query, LocationType, pagination)

    def create(self, location_type: LocationType) -> LocationType:
        """Create a new location type.

        Args:
            location_type: LocationType instance to create

        Returns:
            The created LocationType
        """
        self.db.add(location_type)
        self.db.commit()
        self.db.refresh(location_type)
        return location_type

    def update(self, location_type: LocationType) -> LocationType:
        """Update an existing location type.

        Args:
            location_type: LocationType instance with updated data

        Returns:
            The updated LocationType
        """
        self.db.add(location_type)
        self.db.commit()
        self.db.refresh(location_type)
        return location_type

    def delete(self, location_type_id: str) -> bool:
        """Delete a location type by ID.

        Args:
            location_type_id: The UUID of the location type to delete

        Returns:
            True if deleted successfully, False if not found
        """
        location_type = self.get_by_id(location_type_id)
        if location_type:
            self.db.delete(location_type)
            self.db.commit()
            return True
        return False

    def search(self, query: str, pagination: PaginationParams):
        """Search location types by name or description.

        Args:
            query: Search string to match against name or description
            pagination: Pagination parameters

        Returns:
            Tuple of (list of matching LocationType objects, total count)
        """
        db_query = self.db.query(LocationType).filter(
            (LocationType.name.ilike(f"%{query}%")) |
            (LocationType.description.ilike(f"%{query}%"))
        )
        return refine_query(db_query, LocationType, pagination)