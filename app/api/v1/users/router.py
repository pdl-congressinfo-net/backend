from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.v1.users import schema
from app.common.deps import get_db, require_permission
from app.common.permissions import UserPermissions, UserRoles, Users
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.users import service
from app.features.users.model import User
from app.utils.pagination import PaginationParams

users_router = APIRouter()


@users_router.get("/me", response_model=ApiResponse[schema.UserRead])
async def read_current_user(
    current_user: User = Depends(require_permission(Users.ShowMe)),
):
    """Get current user details."""
    return ApiResponse(data=current_user)


@users_router.get("/roles", response_model=list[schema.UserRoleRead])
async def list_user_roles(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(UserRoles.List)),
):
    """List roles for the current user."""
    results, total = service.list_user_roles(db, pagination)
    return refine_list_response(response, results, total)


@users_router.get("/roles/{user_id}", response_model=ApiResponse[schema.UserRoleRead])
async def get_user_roles(
    user_id: str,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(UserRoles.Show)),
):
    """Get roles for a specific user."""
    user = service.get_user_roles(db, user_id, pagination)
    return ApiResponse(data=user.roles)


@users_router.post("/roles", response_model=ApiResponse[schema.UserRoleRead])
async def create_user_role(
    user_role: schema.UserRoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(UserRoles.Create)),
):
    """Create a new user role."""
    db_roles = service.assign_user_role(db, user_role.user_id, user_role.role_id)
    return ApiResponse(data=db_roles)


@users_router.delete("/roles/{user_id}/{role_id}", response_model=MessageResponse)
async def delete_user_role(
    user_id: str,
    role_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(UserRoles.Delete)),
):
    """Delete a user role."""
    service.remove_user_role(db, user_id, role_id)
    return MessageResponse(message="User role deleted successfully")


@users_router.get("/permissions", response_model=list[schema.UserPermissionRead])
async def list_user_permissions(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(UserPermissions.List)),
):
    """List permissions for the current user."""
    results, total = service.list_user_permissions(db, pagination)
    return refine_list_response(response, results, total)


@users_router.get(
    "/permissions/{user_id}", response_model=ApiResponse[schema.UserPermissionRead]
)
async def get_user_permissions(
    user_id: str,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(UserPermissions.Show)),
):
    """Get permissions for a specific user."""
    user_permissions = service.get_user_permissions(db, user_id, pagination)
    return ApiResponse(data=user_permissions)


@users_router.post(
    "/permissions", response_model=ApiResponse[schema.UserPermissionRead]
)
async def create_user_permission(
    user_permission: schema.UserPermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(UserPermissions.Create)),
):
    """Create a new user permission."""
    user_permission = service.assign_user_permission(
        db, user_permission.user_id, user_permission.permission_id
    )
    return ApiResponse(data=user_permission)


@users_router.delete(
    "/permissions/{user_id}/{permission_id}", response_model=MessageResponse
)
async def delete_user_permission(
    user_id: str,
    permission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(UserPermissions.Delete)),
):
    """Delete a user permission."""
    service.remove_user_permission(db, user_id, permission_id)
    return MessageResponse(message="User permission deleted successfully")


@users_router.get("", response_model=list[schema.UserRead])
async def list_users(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Users.List)),
):
    """List users."""
    users, total = service.list_users(db, pagination)
    return refine_list_response(response, users, total)


@users_router.get("/{user_id}", response_model=ApiResponse[schema.UserRead])
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Users.Show)),
):
    """Get user by ID."""
    user = service.get_user(db, user_id)
    return ApiResponse(data=user)


@users_router.put("/{user_id}", response_model=ApiResponse[schema.UserRead])
async def update_user(
    user_id: str,
    user_update: schema.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Users.Update)),
):
    """Update user details."""
    user = service.update_user(db, user_id, user_update)
    return ApiResponse(data=user)


@users_router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Users.Delete)),
):
    """Delete a user."""
    service.delete_user(db, user_id)
    return MessageResponse(message="User deleted successfully")
