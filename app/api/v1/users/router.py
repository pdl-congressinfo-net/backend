from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.api.v1.users.schema import (
    UserPermissionCreate,
    UserPermissionRead,
    UserRead,
    UserRoleCreate,
    UserRoleRead,
    UserUpdate,
)
from app.common.deps import get_db, require_permission
from app.common.permissions import UserRoles, Users
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.users.model import User
from app.utils.pagination import PaginationParams

users_router = APIRouter()


@users_router.get("/me", response_model=ApiResponse[UserRead])
async def read_current_user(
    current_user: User = Depends(require_permission(Users.ShowMe)),
):
    """Get current user details."""

    return ApiResponse(data=current_user)


@users_router.get("/roles", response_model=list[UserRoleRead])
async def list_user_roles(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(UserRoles.List)),
):
    """List roles for the current user."""
    query = db.query(User).filter(User.id == current_user.id)
    results, total = query.first().roles, 1  # Assuming roles are pre-fetched
    return refine_list_response(response, results, total)


@users_router.get("/roles/{user_id}", response_model=ApiResponse[UserRoleRead])
async def get_user_roles(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(UserRoles.Show)),
):
    """Get roles for a specific user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ApiResponse(data=user.roles)


@users_router.post("/roles", response_model=ApiResponse[UserRoleRead])
async def create_user_role(
    user_role: UserRoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(UserRoles.Create)),
):
    """Create a new user role."""
    db_user = db.query(User).filter(User.id == user_role.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.roles.append(user_role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return ApiResponse(data=user_role)


@users_router.delete("/roles/{user_id}/{role_id}", response_model=MessageResponse)
async def delete_user_role(
    user_id: str,
    role_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(UserRoles.Delete)),
):
    """Delete a user role."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    role_to_remove = next((role for role in db_user.roles if role.id == role_id), None)
    if not role_to_remove:
        raise HTTPException(status_code=404, detail="Role not found for user")
    db_user.roles.remove(role_to_remove)
    db.add(db_user)
    db.commit()
    return MessageResponse(message="User role deleted successfully")


@users_router.get("/permissions", response_model=list[UserPermissionRead])
async def list_user_permissions(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Users.ListPermissions)),
):
    """List permissions for the current user."""
    query = db.query(User).filter(User.id == current_user.id)
    results, total = (
        query.first().permissions,
        1,
    )  # Assuming permissions are pre-fetched
    return refine_list_response(response, results, total)


@users_router.get(
    "/permissions/{user_id}", response_model=ApiResponse[UserPermissionRead]
)
async def get_user_permissions(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Users.ShowPermissions)),
):
    """Get permissions for a specific user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ApiResponse(data=user.permissions)


@users_router.post("/permissions", response_model=ApiResponse[UserPermissionRead])
async def create_user_permission(
    user_permission: UserPermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Users.CreatePermissions)),
):
    """Create a new user permission."""
    db_user = db.query(User).filter(User.id == user_permission.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.permissions.append(user_permission)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return ApiResponse(data=user_permission)


@users_router.delete(
    "/permissions/{user_id}/{permission_id}", response_model=MessageResponse
)
async def delete_user_permission(
    user_id: str,
    permission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Users.DeletePermissions)),
):
    """Delete a user permission."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    permission_to_remove = next(
        (perm for perm in db_user.permissions if perm.id == permission_id), None
    )
    if not permission_to_remove:
        raise HTTPException(status_code=404, detail="Permission not found for user")
    db_user.permissions.remove(permission_to_remove)
    db.add(db_user)
    db.commit()
    return MessageResponse(message="User permission deleted successfully")


@users_router.get("", response_model=ApiResponse[list[UserRead]])
async def list_users(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Users.List)),
):
    """List users."""
    query = db.query(User)
    total = query.count()
    users = query.offset(pagination.skip).limit(pagination.limit).all()
    return refine_list_response(response, users, total)


@users_router.get("/{user_id}", response_model=ApiResponse[UserRead])
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Users.Show)),
):
    """Get user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ApiResponse(data=user)


@users_router.put("/{user_id}", response_model=ApiResponse[UserRead])
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Users.Update)),
):
    """Update user details."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return ApiResponse(data=user)


@users_router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Users.Delete)),
):
    """Delete a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return MessageResponse(message="User deleted successfully")
