from sqlalchemy.orm import Session

from app.features.permissions.model import Permission
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query


# =========================
# PERMISSION REPO
# =========================
def list_permissions(db: Session, pagination: PaginationParams):
    query = db.query(Permission)
    return refine_query(query, Permission, pagination)


def get_permission_by_id(db: Session, permission_id: str):
    return db.query(Permission).filter(Permission.id == permission_id).first()


def get_permission_by_name(db: Session, name: str):
    return db.query(Permission).filter(Permission.name == name).first()


def create_permission(db: Session, permission: Permission):
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


def update_permission(db: Session, permission: Permission, updates: dict):
    for key, value in updates.items():
        setattr(permission, key, value)
    db.commit()
    db.refresh(permission)
    return permission


def delete_permission(db: Session, permission: Permission):
    db.delete(permission)
    db.commit()
