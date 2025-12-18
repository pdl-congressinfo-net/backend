from sqlalchemy.orm import Session, selectinload
from sqlmodel import select

from app.core.config import settings
from app.features.permissions.model import Permission
from app.features.roles.model import Role, RolePermission
from app.features.users.model import Contact, User, UserPermission, UserRole
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


def add_default_role_to_user(db: Session, user_id: str):
    default_role = db.query(Role).filter(Role.is_default == True).first()

    if default_role:
        return add_role_to_user(db, user_id, default_role.id)
    raise RuntimeError("No default role configured")


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


def list_guest_permissions(db: Session, request):
    guest_role = db.query(Role).filter(Role.name == settings.GUEST_ROLE_NAME).first()
    if not guest_role:
        return [], 0
    query = (
        db.query(Permission)
        .join(RolePermission)
        .filter(RolePermission.role_id == guest_role.id)
    )
    return refine_query(
        query, Permission, PaginationParams(request, _start=1, _end=1000)
    )


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
def list_users(db: Session, pagination: PaginationParams) -> list[User]:
    query = db.query(User)
    return refine_query(query, User, pagination)


def get_user_by_id(
    db: Session, user_id: str, with_permissions: bool = False
) -> User | None:
    if with_permissions:
        return db.exec(
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.permissions),
                selectinload(User.roles).selectinload(Role.permissions),
            )
        ).first()
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, updates: dict) -> User:
    for key, value in updates.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()


# =========================
# CONTACT REPO
# =========================
def get_contact_by_id(db: Session, contact_id: str) -> Contact | None:
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_contact_by_user_id(db: Session, user_id: str) -> Contact | None:
    return db.query(Contact).filter(Contact.user_id == user_id).first()


def list_contacts(db: Session, pagination: PaginationParams):
    query = db.query(Contact)
    return refine_query(query, Contact, pagination)


def create_contact(
    db: Session,
    *,
    user_id: str | None = None,
    email: str,
    titles: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    phone_number: str | None = None,
) -> Contact:
    contact = Contact(
        user_id=user_id,
        email=email,
        titles=titles,
        first_name=first_name or "",
        last_name=last_name,
        phone_number=phone_number,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def update_contact(db: Session, contact: Contact, updates: dict) -> Contact:
    for key, value in updates.items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(db: Session, contact: Contact) -> None:
    db.delete(contact)
    db.commit()
