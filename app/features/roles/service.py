from pydantic import BaseModel

from app.common.exceptions import NotFoundError
from app.features.roles import repo
from app.features.roles.model import Role


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


def get_role_by_name(db, name: str):
    role = repo.get_role_by_name(db, name)
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


# =========================
# ROLE PERMISSION SERVICE
# =========================
def list_role_permissions(db, pagination):
    return repo.list_role_permissions(db, pagination)


def get_role_permissions(db, role_id: str):
    permissions = repo.get_permissions_by_role_id(db, role_id)
    if not permissions:
        raise NotFoundError("Role permissions not found")
    return permissions


def assign_role_permission(db, role_id: str, permission_id: str):
    return repo.add_permission_to_role(db, role_id, permission_id)


def remove_role_permission(db, role_id: str, permission_id: str):
    return repo.remove_permission_from_role(db, role_id, permission_id)
