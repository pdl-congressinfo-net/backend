from pydantic import BaseModel

from app.common.exceptions import NotFoundError
from app.features.roles import repo
from app.features.roles.model import Role


# =========================
# ROLE PERMISSION SERVICE
# =========================
def list_role_permissions(db, pagination):
    return repo.list_role_permissions(db, pagination)


def get_role_permission(db, role_id: str, permission_id: str):
    role_permission = repo.get_role_permission(db, role_id, permission_id)
    if not role_permission:
        raise NotFoundError("Role permission not found")
    return role_permission


def get_permissions_by_role(db, role_id: str):
    return repo.get_permissions_by_role(db, role_id)


def create_role_permission(db, payload: BaseModel):
    role_permission = repo.RolePermission.model_validate(payload)
    return repo.create_role_permission(db, role_permission)


def delete_role_permission(db, role_id: str, permission_id: str):
    role_permission = repo.get_role_permission(db, role_id, permission_id)
    if not role_permission:
        raise NotFoundError("Role permission not found")

    repo.delete_role_permission(db, role_permission)


# =========================
# ROLE SERVICE
# =========================
def list_roles(db, pagination):
    return repo.list_roles(db, pagination)


def get_role(db, role_id: str):
    role = repo.get_role_by_id(db, role_id)
    if not role:
        raise NotFoundError("Role not found")
    return role


def get_role_by_name(db, role_name: str):
    role = repo.get_role_by_name(db, role_name)
    if not role:
        raise NotFoundError("Role not found")
    return role


def create_role(db, payload: BaseModel):
    role = Role.model_validate(payload)
    return repo.create_role(db, role)


def update_role(db, role_id: str, payload: BaseModel):
    role = repo.get_role_by_id(db, role_id)
    if not role:
        raise NotFoundError("Role not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_role(db, role, updates)


def delete_role(db, role_id: str):
    role = repo.get_role_by_id(db, role_id)
    if not role:
        raise NotFoundError("Role not found")

    repo.delete_role(db, role)
