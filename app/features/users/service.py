from datetime import datetime, timedelta

from fastapi import Response
from pydantic import BaseModel

from app.common.exceptions import NotFoundError
from app.core.config import settings
from app.core.security import (
    create_access_token,
    get_password_hash,
    set_refresh_cookie,
    set_split_jwt_cookies,
    verify_password,
)
from app.features.users import repo
from app.features.users.model import Contact, User


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


def list_guest_permissions(db, request):
    return repo.list_guest_permissions(db, request)


def get_user_permissions(db, user_id: str):
    user = repo.get_user_by_id(db, user_id, True)
    print(user.permissions)
    permissions = user.effective_permissions()
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
    data = payload.model_dump()
    contact_payload = data.pop("contact", None)
    user = User.model_validate(data)
    user = repo.create_user(db, user)

    # Create linked contact if provided
    if contact_payload:
        repo.create_contact(
            db,
            user_id=user.id,
            email=user.email,
            titles=contact_payload.get("titles"),
            first_name=contact_payload.get("first_name"),
            last_name=contact_payload.get("last_name"),
            phone_number=contact_payload.get("phone_number"),
        )
    return user


def update_user(db, user_id: str, payload: BaseModel):
    user = repo.get_user_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")

    updates = payload.model_dump(exclude_unset=True)
    contact_updates = updates.pop("contact", None)
    updated_user = repo.update_user(db, user, updates) if updates else user

    if contact_updates is not None:
        # Ensure a contact exists, then update it
        contact = repo.get_contact_by_user_id(db, user.id)
        if contact:
            repo.update_contact(db, contact, contact_updates)
        else:
            repo.create_contact(
                db,
                user_id=user.id,
                email=user.email,
                titles=contact_updates.get("titles"),
                first_name=contact_updates.get("first_name"),
                last_name=contact_updates.get("last_name"),
                phone_number=contact_updates.get("phone_number"),
            )

    return updated_user


def delete_user(db, user_id: str):
    user = repo.get_user_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")
    repo.delete_user(db, user)


def login_user(db, response: Response, payload: BaseModel):
    user = repo.get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise NotFoundError("Invalid email or password")

    access_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires = timedelta(days=7)

    access_token = create_access_token({"sub": payload.email}, access_expires)
    refresh_token = create_access_token({"sub": payload.email}, refresh_expires)

    set_split_jwt_cookies(response, access_token)
    set_refresh_cookie(response, refresh_token)

    repo.update_user(db, user, {"last_login": datetime.utcnow()})

    return user


def register_user(db, payload: BaseModel):
    user = repo.get_user_by_email(db, payload.email)
    if user:
        raise NotFoundError("User with this email already exists")

    hashed_password = get_password_hash(payload.password)

    # Create user data dict with hashed password
    user_data = payload.model_dump(exclude={"password"})
    contact_payload = user_data.pop("contact", None)
    user_data["hashed_password"] = hashed_password

    user = User.model_validate(user_data)
    user = repo.create_user(db, user)

    repo.add_default_role_to_user(db, user.id)

    if contact_payload:
        repo.create_contact(
            db,
            user_id=user.id,
            email=user.email,
            titles=contact_payload.get("titles"),
            first_name=contact_payload.get("first_name"),
            last_name=contact_payload.get("last_name"),
            phone_number=contact_payload.get("phone_number"),
        )


# =========================
# CONTACT SERVICE
# =========================
def list_contacts(db, pagination):
    return repo.list_contacts(db, pagination)


def get_user_contact(db, contact_id: str):
    contact = repo.get_contact_by_id(db, contact_id)
    if not contact:
        raise NotFoundError("Contact not found")
    return contact


def create_user_contact(db, payload: BaseModel):
    contact = Contact.model_validate(payload)
    contact = repo.create_contact(db, contact)


def update_user_contact(db, contact_id: str, payload: BaseModel):
    contact = repo.get_contact_by_id(db, contact_id)
    if not contact:
        raise NotFoundError("Contact not found")
    updates = payload.model_dump(exclude_unset=True)
    return repo.update_contact(db, contact, updates)


def delete_user_contact(db, contact_id: str):
    contact = repo.get_contact_by_id(db, contact_id)
    if not contact:
        return
    repo.delete_contact(db, contact)
