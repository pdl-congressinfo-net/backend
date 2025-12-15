from pydantic import BaseModel

from app.common.exceptions import NotFoundError
from app.features.permissions import repo
from app.features.permissions.model import Permission
from app.features.roles.repo import add_permission_to_role, get_role_by_name


# =========================
# PERMISSION SERVICE
# =========================
def list_permissions(db, pagination):
    return repo.list_permissions(db, pagination)


def get_permission(db, permission_id: str):
    permission = repo.get_permission_by_id(db, permission_id)
    if not permission:
        raise NotFoundError("Permission not found")
    return permission


def get_permission_by_name(db, name: str):
    permission = repo.get_permission_by_name(db, name)
    if not permission:
        raise NotFoundError("Permission not found")
    return permission


def create_permission(db, payload: BaseModel):
    """
    Create either a single permission or a full resource with default actions.

    If payload.name is provided: creates a single permission
    If payload.resource_name is provided: creates all default actions (list, show, create, update, delete)
    """
    # Check if this is a resource creation (resource_name provided)
    if hasattr(payload, "resource_name") and payload.resource_name:
        resource_name = payload.resource_name
        default_actions = ["list", "show", "create", "update", "delete"]
        created_permissions = []

        admin_role = get_role_by_name(db, "admin")

        for action in default_actions:
            permission_name = f"{resource_name}:{action}"
            permission = Permission(name=permission_name)
            created_permission = repo.create_permission(db, permission)
            created_permissions.append(created_permission)

            # Add to admin role
            if admin_role:
                add_permission_to_role(db, admin_role.id, created_permission.id)

        # Return the first permission (could return all, but API expects single response)
        return created_permissions[0] if created_permissions else None

    # Standard single permission creation
    permission = Permission.model_validate(payload)
    created_permission = repo.create_permission(db, permission)

    admin_role = get_role_by_name(db, "admin")
    if admin_role:
        add_permission_to_role(db, admin_role.id, created_permission.id)
    return created_permission


def update_permission(db, permission_id: str, payload: BaseModel):
    permission = repo.get_permission_by_id(db, permission_id)
    if not permission:
        raise NotFoundError("Permission not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_permission(db, permission, updates)


def delete_permission(db, permission_id: str):
    permission = repo.get_permission_by_id(db, permission_id)
    if not permission:
        raise NotFoundError("Permission not found")
    repo.delete_permission(db, permission)
