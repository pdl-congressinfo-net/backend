from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.api.v1.roles.schema import (
    RoleCreate,
    RolePermissionCreate,
    RolePermissionRead,
    RolePermissionUpdate,
    RoleRead,
    RoleUpdate,
)
from app.common.deps import get_db, require_permission
from app.common.permissions import RolePermissions, Roles
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.roles.model import Role, RolePermission
from app.features.users.model import User
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query

roles_router = APIRouter()


@roles_router.get("/permissions", response_model=list[RolePermissionRead])
async def list_role_permissions(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(RolePermissions.List)),
):
    """List all roles."""
    query = db.query(RolePermission)
    results, total = refine_query(query, RolePermission, pagination)
    return refine_list_response(response, results, total)


@roles_router.get(
    "/permissions/{role_permission_id}", response_model=ApiResponse[RolePermissionRead]
)
async def get_role_permission(
    role_permission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(RolePermissions.Show)),
):
    """Get role permission by ID."""
    role_permission = (
        db.query(RolePermission).filter(RolePermission.id == role_permission_id).first()
    )
    if not role_permission:
        raise HTTPException(status_code=404, detail="Role permission not found")
    return ApiResponse(data=role_permission)


@roles_router.post("/permissions", response_model=ApiResponse[RolePermissionRead])
async def create_role_permission(
    role_permission: RolePermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(RolePermissions.Create)),
):
    """Create a new role permission."""
    db_role_permission = RolePermission.model_validate(role_permission)
    db.add(db_role_permission)
    db.commit()
    db.refresh(db_role_permission)
    return ApiResponse(data=db_role_permission)


@roles_router.put(
    "/permissions/{role_id}/{permission_id}",
    response_model=ApiResponse[RolePermissionRead],
)
async def update_role_permission(
    role_id: str,
    permission_id: str,
    role_permission: RolePermissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(RolePermissions.Update)),
):
    """Update an existing role permission."""
    db_role_permission = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        )
        .first()
    )
    if not db_role_permission:
        raise HTTPException(status_code=404, detail="Role permission not found")
    for key, value in role_permission.model_dump(exclude_unset=True).items():
        setattr(db_role_permission, key, value)
    db.add(db_role_permission)
    db.commit()
    db.refresh(db_role_permission)
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
    """Delete a role permission."""
    db_role_permission = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        )
        .first()
    )
    if not db_role_permission:
        raise HTTPException(status_code=404, detail="Role permission not found")
    db.delete(db_role_permission)
    db.commit()
    return MessageResponse(message="Role deleted successfully")


@roles_router.get("", response_model=list[RoleRead])
async def list_roles(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Roles.List)),
):
    """List all roles."""
    query = db.query(Role)
    results, total = refine_query(query, Role, pagination)
    return refine_list_response(response, results, total)


@roles_router.get("/{role_id}", response_model=ApiResponse[RoleRead])
async def get_role(
    role_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Roles.Show)),
):
    """Get role by ID."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return ApiResponse(data=role)


@roles_router.post("", response_model=ApiResponse[RoleRead])
async def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Roles.Create)),
):
    """Create a new role."""
    db_role = Role.model_validate(role)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return ApiResponse(data=db_role)


@roles_router.put("/{role_id}", response_model=ApiResponse[RoleRead])
async def update_role(
    role_id: str,
    role: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Roles.Update)),
):
    """Update an existing role."""
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    for key, value in role.model_dump(exclude_unset=True).items():
        setattr(db_role, key, value)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return ApiResponse(data=db_role)


@roles_router.delete("/{role_id}", response_model=MessageResponse)
async def delete_role(
    role_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Roles.Delete)),
):
    """Delete a role."""
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(db_role)
    db.commit()
    return MessageResponse(message="Role deleted successfully")
