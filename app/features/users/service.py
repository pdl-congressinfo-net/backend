from pydantic import BaseModel

from app.common.exceptions import NotFoundError
from app.features.users import repo
from app.features.users.model import User


# =========================
# USER ROLE SERVICE
# =========================
def list_user_roles(db, pagination):
    return repo.list_user_roles(db, pagination)


def get_user_roles(db, user_id: str, pagination):
    roles = repo.get_roles_by_user_id(db, user_id, pagination)
    if not roles:
        raise NotFoundError("User roles not found")
    return roles


def assign_user_role(db, user_id: str, role_id: str):
    return repo.add_role_to_user(db, user_id, role_id)


def remove_user_role(db, user_id: str, role_id: str):
    return repo.remove_role_from_user(db, user_id, role_id)


# =========================
# USER PERMISSION SERVICE
# =========================
def list_user_permissions(db, pagination):
    return repo.list_user_permissions(db, pagination)


def get_user_permissions(db, user_id: str, pagination):
    permissions = repo.get_permissions_by_user_id(db, user_id, pagination)
    if not permissions:
        raise NotFoundError("User permissions not found")
    return permissions


def assign_user_permission(db, user_id: str, permission_id: str):
    return repo.add_permission_to_user(db, user_id, permission_id)


def remove_user_permission(db, user_id: str, permission_id: str):
    return repo.remove_permission_from_user(db, user_id, permission_id)


# =========================
# USER SERVICE
# =========================
def list_users(db, pagination):
    return repo.list_users(db, pagination)


def get_user(db, user_id: str):
    user = repo.get_user_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")
    return user


def get_user_by_email(db, email: str):
    user = repo.get_user_by_email(db, email)
    if not user:
        raise NotFoundError("User not found")
    return user


def create_user(db, payload: BaseModel):
    user = User.model_validate(payload)
    return repo.create_user(db, user)


def update_user(db, user_id: str, payload: BaseModel):
    user = repo.get_user_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_user(db, user, updates)


def delete_user(db, user_id: str):
    user = repo.get_user_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")
    repo.delete_user(db, user)
