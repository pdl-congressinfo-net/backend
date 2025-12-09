from pydantic import BaseModel

from app.common.exceptions import NotFoundError
from app.features.permissions import repo
from app.features.permissions.model import Permission


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


def create_permission(db, payload: BaseModel):
    permission = Permission.model_validate(payload)
    return repo.create_permission(db, permission)


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
