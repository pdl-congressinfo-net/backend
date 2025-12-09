from sqlalchemy.orm import Session

from app.core.config import settings
from app.features.users.model import User, UserPermission, UserRole
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query


# =========================
# USER ROLE REPO
# =========================
def list_user_roles(db: Session, pagination: PaginationParams):
    query = db.query(UserRole)
    return refine_query(query, UserRole, pagination)


def get_roles_by_user_id(db: Session, user_id: str):
    return db.query(UserRole).filter(UserRole.user_id == user_id).all()


def add_role_to_user(db: Session, user_id: str, role_id: str):
    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role


def remove_role_from_user(db: Session, user_id: str, role_id: str):
    user_role = (
        db.query(UserRole)
        .filter(UserRole.user_id == user_id, UserRole.role_id == role_id)
        .first()
    )
    if user_role:
        db.delete(user_role)
        db.commit()
    return user_role


# =========================
# USER PERMISSION REPO
# =========================
def list_user_permissions(db: Session, permission: UserPermission):
    query = db.query(UserPermission)
    return refine_query(query, UserPermission, permission)


def list_guest_permissions(db: Session):
    guest_role = (
        db.query(UserRole).filter(UserRole.name == settings.GUEST_ROLE_NAME).first()
    )
    if not guest_role:
        return [], 0
    query = db.query(UserPermission).filter(UserPermission.role_id == guest_role.id)
    return refine_query(query, UserPermission, PaginationParams(page=1, size=1000))


def get_permissions_by_user_id(db: Session, user_id: str):
    query = db.query(UserPermission).filter(UserPermission.user_id == user_id)
    return query.all()


def add_permission_to_user(db: Session, user_id: str, permission_id: str):
    user_permission = UserPermission(user_id=user_id, permission_id=permission_id)
    db.add(user_permission)
    db.commit()
    db.refresh(user_permission)
    return user_permission


def remove_permission_from_user(db: Session, user_id: str, permission_id: str):
    user_permission = (
        db.query(UserPermission)
        .filter(
            UserPermission.user_id == user_id,
            UserPermission.permission_id == permission_id,
        )
        .first()
    )
    if user_permission:
        db.delete(user_permission)
        db.commit()
    return user_permission


# =========================
# USER REPO
# =========================
def list_users(db: Session, pagination: PaginationParams):
    query = db.query(User)
    return refine_query(query, User, pagination)


def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, updates: dict):
    for key, value in updates.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
