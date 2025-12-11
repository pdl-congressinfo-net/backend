from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.v1.roles import schema
from app.common.deps import get_db, require_permission
from app.common.permissions import RolePermissions, Roles
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.roles import service
from app.features.users.model import User
from app.utils.pagination import PaginationParams

roles_router = APIRouter()


# =========================
# ROLE ENDPOINTS
# =========================
@roles_router.get("", response_model=list[schema.RoleRead])
async def list_roles(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Roles.List)),
):
    """List all roles."""
    results, total = service.list_roles(db, pagination)
    return refine_list_response(response, results, total)


@roles_router.get("/{role_id}", response_model=ApiResponse[schema.RoleRead])
async def get_role(
    role_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Roles.Show)),
):
    """Get a specific role by ID."""
    role = service.get_role(db, role_id)
    return ApiResponse(data=role)


@roles_router.post("", response_model=ApiResponse[schema.RoleRead])
async def create_role(
    role: schema.RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Roles.Create)),
):
    """Create a new role."""
    db_role = service.create_role(db, role)
    return ApiResponse(data=db_role)


@roles_router.patch("/{role_id}", response_model=ApiResponse[schema.RoleRead])
async def update_role(
    role_id: str,
    role: schema.RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Roles.Update)),
):
    """Update an existing role."""
    db_role = service.update_role(db, role_id, role)
    return ApiResponse(data=db_role)


@roles_router.delete("/{role_id}", response_model=MessageResponse)
async def delete_role(
    role_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Roles.Delete)),
):
    """Delete a role."""
    service.delete_role(db, role_id)
    return MessageResponse(message="Role deleted successfully")


# =========================
# ROLE PERMISSION ENDPOINTS
# =========================
@roles_router.get("/permissions/all", response_model=list[schema.RolePermissionRead])
async def list_role_permissions(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(RolePermissions.List)),
):
    """List all role permissions."""
    results, total = service.list_role_permissions(db, pagination)
    return refine_list_response(response, results, total)


@roles_router.get("/{role_id}/permissions")
async def get_role_permissions(
    role_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(RolePermissions.Show)),
):
    """Get permissions for a specific role."""
    permissions = service.get_role_permissions(db, role_id)
    return ApiResponse(data=permissions)


@roles_router.post(
    "/permissions", response_model=ApiResponse[schema.RolePermissionRead]
)
async def create_role_permission(
    role_permission: schema.RolePermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(RolePermissions.Create)),
):
    """Assign a permission to a role."""
    db_role_permission = service.assign_role_permission(
        db, role_permission.role_id, role_permission.permission_id
    )
    return ApiResponse(data=db_role_permission)


@roles_router.delete(
    "/permissions/{role_id}/{permission_id}", response_model=MessageResponse
)
async def delete_role_permission(
    role_id: str,
    permission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(RolePermissions.Delete)),
):
    """Remove a permission from a role."""
    service.remove_role_permission(db, role_id, permission_id)
    return MessageResponse(message="Role permission deleted successfully")
