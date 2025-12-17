import csv
import logging

from sqlmodel import Session, select

from app.common.permissions import (
    Categories,
    Countries,
    Events,
    EventTypes,
    Locations,
    LocationTypes,
    Permissions,
    RolePermissions,
    Roles,
    UserPermissions,
    UserRoles,
    Users,
)
from app.core.config import settings
from app.core.db import engine
from app.core.security import get_password_hash
from app.features.events.model import EventType
from app.features.locations.model import Country, LocationType
from app.features.permissions.model import Permission
from app.features.roles.model import Role, RolePermission
from app.features.users.model import User, UserRole
from app.prestart.initial.sponsors import (
    load_sponsor_company_data,
    load_sponsor_contact_data,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_country_data():
    """Load initial country data into the database."""

    logger.info("Loading initial country data")
    with open("app/prestart/data/countries.csv", encoding="utf-8") as csvfile:
        country_reader = csv.DictReader(csvfile)
        with Session(engine) as session:
            # Check if countries already exist
            existing_countries = session.exec(select(Country)).first()
            if existing_countries:
                logger.info("Country data already exists, skipping initialization")
                return

            for row in country_reader:
                country = Country(
                    id=row["id"],
                    name=row["name"],
                    code2=row["code2"],
                    code3=row["code3"],
                    devco=bool(row["devco"]),
                )
                session.add(country)
            session.commit()
    logger.info("Country data loaded successfully")
    return


def load_event_type_data():
    """Load initial event type data into the database."""
    logger.info("Loading initial event type data")
    event_types = ["CON", "WKS", "SEM", "WEB"]

    with Session(engine) as session:
        existing_event_types = session.exec(select(EventType)).first()
        if existing_event_types:
            logger.info("Event type data already exists, skipping initialization")
            return

        for event_type_code in event_types:
            event_type = EventType(
                code=event_type_code,
            )
            session.add(event_type)
        session.commit()
    logger.info("Event type data loaded successfully")
    return


def create_location_types():
    logger.info("Loading initial event types")
    event_types = [
        {"code": "WEB", "name": "Webinar"},
        {"code": "SIT", "name": "On Site"},
        {"code": "COM", "name": "Company"},
    ]
    with Session(engine) as session:
        existing_location_types = session.exec(select(LocationType)).first()
        if existing_location_types:
            logger.info("Location type data already exists, skipping initialization")
            return

        for location_type_data in event_types:
            location_type = LocationType(
                code=location_type_data["code"],
                name=location_type_data["name"],
            )
            session.add(location_type)
        session.commit()
    logger.info("Location type data loaded successfully")
    return


def create_initial_data():
    load_country_data()
    load_event_type_data()
    create_location_types()
    # Create a session from the SessionLocal factory
    logger.info("Creating session for initial data seeding")
    with Session(engine) as session:
        # --- Permissions ---
        permission_names = [
            Categories.List,
            Categories.Show,
            Categories.Create,
            Categories.Update,
            Categories.Delete,
            Countries.List,
            Countries.Show,
            Countries.Create,
            Countries.Update,
            Countries.Delete,
            Events.List,
            Events.Show,
            Events.Create,
            Events.Update,
            Events.Delete,
            EventTypes.List,
            EventTypes.Show,
            EventTypes.Create,
            EventTypes.Update,
            EventTypes.Delete,
            Locations.List,
            Locations.Show,
            Locations.Create,
            Locations.Update,
            Locations.Delete,
            LocationTypes.List,
            LocationTypes.Show,
            LocationTypes.Create,
            LocationTypes.Update,
            LocationTypes.Delete,
            Permissions.List,
            Permissions.Show,
            Permissions.Create,
            Permissions.Update,
            Permissions.Delete,
            Roles.List,
            Roles.Show,
            Roles.Create,
            Roles.Update,
            Roles.Delete,
            RolePermissions.List,
            RolePermissions.Show,
            RolePermissions.Create,
            RolePermissions.Update,
            RolePermissions.Delete,
            Users.List,
            Users.Show,
            Users.Create,
            Users.Update,
            Users.Delete,
            Users.ChangePassword,
            Users.ShowMe,
            UserPermissions.List,
            UserPermissions.Show,
            UserPermissions.Create,
            UserPermissions.Update,
            UserPermissions.Delete,
            UserRoles.List,
            UserRoles.Show,
            UserRoles.Create,
            UserRoles.Update,
            UserRoles.Delete,
        ]
        logger.info("Checking existing permissions in the database")
        existing_permissions = session.exec(select(Permission)).all()
        logger.info(f"Existing permissions: {existing_permissions}")
        if not existing_permissions:
            logger.info(permission_names)
            logger.info("Seeding initial permissions")
            for name in permission_names:
                session.add(Permission(name=name))
            session.commit()

        admin_role = session.exec(
            select(Role).where(Role.name == settings.ADMIN_ROLE_NAME)
        ).first()
        user_role = session.exec(
            select(Role).where(Role.name == settings.USER_ROLE_NAME)
        ).first()
        guest_role = session.exec(
            select(Role).where(Role.name == settings.GUEST_ROLE_NAME)
        ).first()
        logger.debug("Checking existing roles in the database")
        if not admin_role or not user_role or not guest_role:
            if not admin_role:
                logger.info("Seeding admin role")
                admin_role = Role(name=settings.ADMIN_ROLE_NAME)
                session.add(admin_role)
            if not user_role:
                logger.info("Seeding user role")
                user_role = Role(name=settings.USER_ROLE_NAME)
                session.add(user_role)
            if not guest_role:
                logger.info("Seeding guest role")
                guest_role = Role(name=settings.GUEST_ROLE_NAME)
                session.add(guest_role)
            session.commit()

        # --- Attach permissions to admin role ---
        logger.debug("Checking existing role permissions for admin role")
        existing_role_perms = session.exec(
            select(RolePermission).where(RolePermission.role_id == admin_role.id)
        ).all()
        if not existing_role_perms:
            logger.info("Seeding role permissions for admin role")
            permissions = session.exec(select(Permission)).all()
            for perm in permissions:
                session.add(
                    RolePermission(role_id=admin_role.id, permission_id=perm.id)
                )
            session.commit()

        # --- Admin User ---
        logger.debug("Checking existing admin user in the database")
        existing_admin = session.exec(
            select(User).where(User.email == "admin@example.com")
        ).first()
        if not existing_admin:
            logger.info("Seeding admin user")
            hashed_password = get_password_hash("admin123")

            admin_user = User(
                email="admin@example.com",
                full_name="Administrator",
                hashed_password=hashed_password,
            )
            session.add(admin_user)
            session.commit()  # ensures admin_user.id is populated

            # Link admin user to admin role
            session.add(UserRole(user_id=admin_user.id, role_id=admin_role.id))
            session.commit()


if __name__ == "__main__":
    create_initial_data()
    load_sponsor_company_data()
    load_sponsor_contact_data()
