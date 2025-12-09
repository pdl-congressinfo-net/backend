"""Service layer for Country business logic."""

from sqlmodel import Session

from app.utils.pagination import PaginationParams
from app.features.countries.repo import CountryRepository
from app.features.locations.model import Country


class CountryService:
    """Service for Country business logic operations."""

    def __init__(self, db: Session):
        """Initialize service with database session.

        Args:
            db: SQLModel database session
        """
        self.repo = CountryRepository(db)

    def get_by_id(self, country_id: str) -> Country | None:
        """Retrieve a country by its ID.

        Args:
            country_id: The UUID of the country

        Returns:
            Country if found, None otherwise
        """
        return self.repo.get_by_id(country_id)

    def get_by_name(self, name: str) -> Country | None:
        """Retrieve a country by its name.

        Args:
            name: The name of the country

        Returns:
            Country if found, None otherwise
        """
        return self.repo.get_by_name(name)

    def get_by_code2(self, code2: str) -> Country | None:
        """Retrieve a country by its ISO 2-letter code.

        Args:
            code2: The 2-letter country code

        Returns:
            Country if found, None otherwise
        """
        return self.repo.get_by_code2(code2)

    def get_by_code3(self, code3: str) -> Country | None:
        """Retrieve a country by its ISO 3-letter code.

        Args:
            code3: The 3-letter country code

        Returns:
            Country if found, None otherwise
        """
        return self.repo.get_by_code3(code3)

    def list(self, pagination: PaginationParams) -> list[Country]:
        """List all countries with pagination.

        Args:
            pagination: Pagination parameters for the query

        Returns:
            List of Country objects
        """
        return self.repo.list(pagination)

    def list_devco(self, pagination: PaginationParams) -> list[Country]:
        """List all developing countries with pagination.

        Args:
            pagination: Pagination parameters for the query

        Returns:
            List of Country objects where devco is True
        """
        return self.repo.list_devco(pagination)

    def list_preferred(self, pagination: PaginationParams) -> list[Country]:
        """List all preferred countries with pagination.

        Args:
            pagination: Pagination parameters for the query

        Returns:
            List of Country objects where preferred is True
        """
        return self.repo.list_preferred(pagination)

    def create(self, country_data: dict) -> Country:
        """Create a new country with validation.

        Args:
            country_data: Dictionary containing country data

        Returns:
            The created Country

        Raises:
            ValueError: If a country with the same name or codes already exists
        """
        # Normalize country codes to uppercase
        if "code2" in country_data:
            country_data["code2"] = country_data["code2"].upper()
        if "code3" in country_data:
            country_data["code3"] = country_data["code3"].upper()

        # Validate code lengths
        if len(country_data.get("code2", "")) != 2:
            raise ValueError("Country code2 must be exactly 2 characters")
        if len(country_data.get("code3", "")) != 3:
            raise ValueError("Country code3 must be exactly 3 characters")

        # Check for duplicate name
        existing = self.repo.get_by_name(country_data.get("name", ""))
        if existing:
            raise ValueError(f"Country with name '{country_data['name']}' already exists")

        # Check for duplicate code2
        existing = self.repo.get_by_code2(country_data.get("code2", ""))
        if existing:
            raise ValueError(f"Country with code2 '{country_data['code2']}' already exists")

        # Check for duplicate code3
        existing = self.repo.get_by_code3(country_data.get("code3", ""))
        if existing:
            raise ValueError(f"Country with code3 '{country_data['code3']}' already exists")

        country = Country(**country_data)
        return self.repo.create(country)

    def update(self, country_id: str, country_data: dict) -> Country:
        """Update an existing country with validation.

        Args:
            country_id: The UUID of the country to update
            country_data: Dictionary containing updated country data

        Returns:
            The updated Country

        Raises:
            ValueError: If country not found or name/code conflict exists
        """
        country = self.repo.get_by_id(country_id)
        if not country:
            raise ValueError(f"Country with ID '{country_id}' not found")

        # Normalize country codes to uppercase
        if "code2" in country_data:
            country_data["code2"] = country_data["code2"].upper()
            # Validate code length
            if len(country_data["code2"]) != 2:
                raise ValueError("Country code2 must be exactly 2 characters")

        if "code3" in country_data:
            country_data["code3"] = country_data["code3"].upper()
            # Validate code length
            if len(country_data["code3"]) != 3:
                raise ValueError("Country code3 must be exactly 3 characters")

        # Check for duplicate name if name is being changed
        if "name" in country_data and country_data["name"] != country.name:
            existing = self.repo.get_by_name(country_data["name"])
            if existing:
                raise ValueError(f"Country with name '{country_data['name']}' already exists")

        # Check for duplicate code2 if code2 is being changed
        if "code2" in country_data and country_data["code2"] != country.code2:
            existing = self.repo.get_by_code2(country_data["code2"])
            if existing:
                raise ValueError(f"Country with code2 '{country_data['code2']}' already exists")

        # Check for duplicate code3 if code3 is being changed
        if "code3" in country_data and country_data["code3"] != country.code3:
            existing = self.repo.get_by_code3(country_data["code3"])
            if existing:
                raise ValueError(f"Country with code3 '{country_data['code3']}' already exists")

        # Update fields
        for key, value in country_data.items():
            if hasattr(country, key):
                setattr(country, key, value)

        return self.repo.update(country)

    def delete(self, country_id: str) -> bool:
        """Delete a country by ID.

        Args:
            country_id: The UUID of the country to delete

        Returns:
            True if deleted successfully

        Raises:
            ValueError: If country not found or has associated locations
        """
        country = self.repo.get_by_id(country_id)
        if not country:
            raise ValueError(f"Country with ID '{country_id}' not found")

        # Check if country has associated locations
        if country.locations:
            raise ValueError(
                f"Cannot delete country '{country.name}' as it has {len(country.locations)} associated locations"
            )

        return self.repo.delete(country_id)

    def search(self, query: str, pagination: PaginationParams) -> list[Country]:
        """Search countries by name or codes.

        Args:
            query: Search string to match against name, code2, or code3
            pagination: Pagination parameters

        Returns:
            List of matching Country objects
        """
        return self.repo.search(query, pagination)
