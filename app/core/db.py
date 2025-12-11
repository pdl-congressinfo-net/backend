from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool

from app.core.config import settings
from app.features.companies.model import Company, CompanyEmployee  # noqa: F401
from app.features.events.model import Event, EventType  # noqa: F401
from app.features.locations.model import Country, Location, LocationType  # noqa: F401
from app.features.permissions.model import Permission  # noqa: F401
from app.features.roles.model import Role, RolePermission  # noqa: F401
from app.features.users.model import User, UserPermission, UserRole  # noqa: F401

Base = declarative_base()


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=True,
    poolclass=QueuePool,
    pool_size=5,  # Number of connections to maintain
    max_overflow=10,  # Additional connections when pool is full
    pool_pre_ping=True,  # Test connections before using them (critical for remote DB)
    pool_recycle=3600,  # Recycle connections after 1 hour
    connect_args={
        "connect_timeout": 10,  # Connection timeout in seconds
        "read_timeout": 30,  # Read timeout in seconds
        "write_timeout": 30,  # Write timeout in seconds
    },
)
