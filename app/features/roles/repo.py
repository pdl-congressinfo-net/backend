from sqlalchemy.orm import Session

from app.features.roles.model import Role, RolePermission
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query


# =========================
# ROLE REPO
# =========================
def list_roles(db: Session, pagination: PaginationParams):
    query = db.query(Role)
    return refine_query(query, Role, pagination)


def get_role_by_id(db: Session, role_id: str):
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()


def create_role(db: Session, role: Role):
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def update_role(db: Session, role: Role, updates: dict):
    for key, value in updates.items():
        setattr(role, key, value)
    db.commit()
    db.refresh(role)
    return role


def delete_role(db: Session, role: Role):
    if role.is_default:
        raise ValueError("Cannot delete the default role")
    db.delete(role)
    db.commit()


# =========================
# ROLE PERMISSION REPO
# =========================
def list_role_permissions(db: Session, pagination: PaginationParams):
    query = db.query(RolePermission)
    return refine_query(query, RolePermission, pagination)


def get_permissions_by_role_id(db: Session, role_id: str):
    role = db.query(Role).filter(Role.id == role_id).first()
    return role.permissions if role else []


def add_permission_to_role(db: Session, role_id: str, permission_id: str):
    role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
    db.add(role_permission)
    db.commit()
    return role_permission


def remove_permission_from_role(db: Session, role_id: str, permission_id: str):
    role_permission = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        )
        .first()
    )
    if role_permission:
        db.delete(role_permission)
        db.commit()
