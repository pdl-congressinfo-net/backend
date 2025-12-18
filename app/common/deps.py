from collections.abc import Generator
from datetime import timedelta

from fastapi import Cookie, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlmodel import Session as SQLSession

from app.common.scopes import has_object_permission
from app.core.config import settings
from app.core.db import engine
from app.core.security import (
    create_access_token,
    set_refresh_cookie,
    set_split_jwt_cookies,
)
from app.features.permissions.model import Permission
from app.features.roles.model import Role
from app.features.users.model import User
from app.features.users.service import (
    get_user_by_email,
    list_guest_permissions,
)
from app.features.users.service import (
    get_user_permissions as service_get_user_permissions,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_db() -> Generator[Session, None, None]:
    """Database session dependency"""
    with SQLSession(engine) as session:
        yield session


async def get_current_user(
    request: Request,
    response: Response,
    jwt_hp: str = Cookie(None),
    jwt_sig: str = Cookie(None),
    refresh_token: str = Cookie(None),
    db: Session = Depends(get_db),
) -> User | None:
    """Optionally authenticate the user using split JWT cookies.
    Returns None if authentication fails.
    """

    if not jwt_hp or not jwt_sig:
        # Handle refresh token flow
        if refresh_token:
            try:
                payload = jwt.decode(
                    refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
                )
            except JWTError:
                return None
            if not payload:
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            email = payload["sub"]

            if not email:
                return None

            # Lookup user in DB

            user = get_user_by_email(db, email)
            if not user:
                return None

            access_expires = timedelta(minutes=15)
            refresh_expires = timedelta(days=7)

            access_token = create_access_token({"sub": email}, access_expires)
            refresh_token = create_access_token({"sub": email}, refresh_expires)

            set_refresh_cookie(response, refresh_token)
            set_split_jwt_cookies(response, access_token)
            return user
        return None

    # Reconstruct JWT from split cookies
    token = f"{jwt_hp}.{jwt_sig}"

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
    except JWTError:
        return None

    if not email:
        return None

    # Lookup user in DB
    user = get_user_by_email(db, email)
    if not user:
        return None

    return user


def require_permission(permission_name: Permission):
    """Dependency factory to check if user has specific permission or if available to guests"""

    async def permission_checker(
        request: Request,
        current_user: User | None = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        if request.method == "OPTIONS":
            return None
        # If no user is authenticated, check if permission is available to guests
        if current_user is None:
            guest_permissions, total = list_guest_permissions(db, request)
            print(guest_permissions)
            print(permission_name)
            guest_permission_names = [perm.name for perm in guest_permissions]
            if permission_name in guest_permission_names:
                return None

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Authentication required for permission '{permission_name}'",
            )

        # Check authenticated user's permissions
        user_permissions = service_get_user_permissions(db, current_user.id)
        user_permission_names = [perm.name for perm in user_permissions]

        if permission_name not in user_permission_names:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission_name}' required",
            )
        return current_user

    return permission_checker


def check_permissions_user(
    db: Session, user: User, required_permissions: list[str]
) -> bool:
    """Check if user has all required permissions"""
    user_permissions = service_get_user_permissions(db, user.id)
    user_permission_names = [perm.name for perm in user_permissions]
    return all(perm in user_permission_names for perm in required_permissions)


def get_role_permissions(role: str, db: Session) -> list[str]:
    """Get all permissions for a role"""
    role_obj = db.query(Role).filter(Role.name == role).first()
    if not role_obj:
        return []
    role_permissions = [perm.name for perm in role_obj.permissions]
    return role_permissions


def require_object_permission(resource: str, action: str):
    def dependency(
        object_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_permission(resource)),
    ):
        if not has_object_permission(
            db=db,
            user=current_user,
            resource=resource,
            object_id=object_id,
            action=action,
        ):
            raise HTTPException(status_code=404)

    return dependency
