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
from app.core.db import engine
from app.core.security import get_password_hash
from app.features.permissions.model import Permission
from app.features.roles.model import Role, RolePermission
from app.features.users.model import User, UserRole


def create_initial_data():
    """Seed initial roles, permissions, and an admin user."""

    # Create a session from the SessionLocal factory
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

        existing_permissions = session.exec(select(Permission)).all()
        if not existing_permissions:
            for name in permission_names:
                session.add(Permission(name=name))
            session.commit()

        # --- Roles ---
        admin_role = session.exec(select(Role).where(Role.name == "admin")).first()
        user_role = session.exec(select(Role).where(Role.name == "user")).first()
        guest_role = session.exec(select(Role).where(Role.name == "guest")).first()

        if not admin_role or not user_role or not guest_role:
            if not admin_role:
                admin_role = Role(name="admin")
                session.add(admin_role)
            if not user_role:
                user_role = Role(name="user")
                session.add(user_role)
            if not guest_role:
                guest_role = Role(name="guest")
                session.add(guest_role)
            session.commit()

        # --- Attach permissions to admin role ---
        existing_role_perms = session.exec(
            select(RolePermission).where(RolePermission.role_id == admin_role.id)
        ).all()
        if not existing_role_perms:
            print("Attaching permissions to admin role...")
            permissions = session.exec(select(Permission)).all()
            for perm in permissions:
                session.add(
                    RolePermission(role_id=admin_role.id, permission_id=perm.id)
                )
            session.commit()

        # --- Admin User ---
        existing_admin = session.exec(
            select(User).where(User.email == "admin@example.com")
        ).first()
        if not existing_admin:
            print("Creating admin user...")

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

        print("✅ Initial data created successfully.")


if __name__ == "__main__":
    create_initial_data()
