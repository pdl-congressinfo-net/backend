"""Repository layer for Country database operations."""

from sqlalchemy.orm import Session

from app.features.locations.model import Country
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query


class CountryRepository:
    """Repository for Country CRUD operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def get_by_id(self, country_id: str) -> Country | None:
        """Retrieve a country by its ID.

        Args:
            country_id: The UUID of the country

        Returns:
            Country if found, None otherwise
        """
        return self.db.query(Country).filter(Country.id == country_id).first()

    def get_by_name(self, name: str) -> Country | None:
        """Retrieve a country by its name.

        Args:
            name: The name of the country

        Returns:
            Country if found, None otherwise
        """
        return self.db.query(Country).filter(Country.name == name).first()

    def get_by_code2(self, code2: str) -> Country | None:
        """Retrieve a country by its ISO 2-letter code.

        Args:
            code2: The 2-letter country code

        Returns:
            Country if found, None otherwise
        """
        return self.db.query(Country).filter(Country.code2 == code2.upper()).first()

    def get_by_code3(self, code3: str) -> Country | None:
        """Retrieve a country by its ISO 3-letter code.

        Args:
            code3: The 3-letter country code

        Returns:
            Country if found, None otherwise
        """
        return self.db.query(Country).filter(Country.code3 == code3.upper()).first()

    def list(self, pagination: PaginationParams):
        """List all countries with pagination.

        Args:
            pagination: Pagination parameters for the query

        Returns:
            Tuple of (list of Country objects, total count)
        """
        query = self.db.query(Country)
        return refine_query(query, Country, pagination)

    def list_devco(self, pagination: PaginationParams):
        """List all developing countries with pagination.

        Args:
            pagination: Pagination parameters for the query

        Returns:
            Tuple of (list of Country objects, total count)
        """
        query = self.db.query(Country).filter(Country.devco == True)
        return refine_query(query, Country, pagination)

    def list_preferred(self, pagination: PaginationParams):
        """List all preferred countries with pagination.

        Args:
            pagination: Pagination parameters for the query

        Returns:
            Tuple of (list of Country objects, total count)
        """
        query = self.db.query(Country).filter(Country.preferred == True)
        return refine_query(query, Country, pagination)

    def create(self, country: Country) -> Country:
        """Create a new country.

        Args:
            country: Country instance to create

        Returns:
            The created Country
        """
        self.db.add(country)
        self.db.commit()
        self.db.refresh(country)
        return country

    def update(self, country: Country) -> Country:
        """Update an existing country.

        Args:
            country: Country instance with updated data

        Returns:
            The updated Country
        """
        self.db.add(country)
        self.db.commit()
        self.db.refresh(country)
        return country

    def delete(self, country_id: str) -> bool:
        """Delete a country by ID.

        Args:
            country_id: The UUID of the country to delete

        Returns:
            True if deleted successfully, False if not found
        """
        country = self.get_by_id(country_id)
        if country:
            self.db.delete(country)
            self.db.commit()
            return True
        return False

    def search(self, query: str, pagination: PaginationParams):
        """Search countries by name or codes.

        Args:
            query: Search string to match against name, code2, or code3
            pagination: Pagination parameters

        Returns:
            Tuple of (list of matching Country objects, total count)
        """
        db_query = self.db.query(Country).filter(
            (Country.name.ilike(f"%{query}%")) |
            (Country.code2.ilike(f"%{query}%")) |
            (Country.code3.ilike(f"%{query}%"))
        )
        return refine_query(db_query, Country, pagination)