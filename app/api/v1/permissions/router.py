from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.api.v1.permissions.schema import (
    PermissionCreate,
    PermissionRead,
    PermissionUpdate,
)
from app.common.deps import get_db, require_permission
from app.common.permissions import Permissions
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.permissions.model import Permission
from app.features.users.model import User
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query

permissions_router = APIRouter()


@permissions_router.get("", response_model=list[PermissionRead])
async def list_permissions(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Permissions.List)),
):
    """List all permissions."""
    query = db.query(Permission)
    results, total = refine_query(query, Permission, pagination)
    return refine_list_response(response, results, total)


@permissions_router.get("/{permission_id}", response_model=ApiResponse[PermissionRead])
async def get_permission(
    permission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Permissions.Show)),
):
    """Get permission by ID."""
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return ApiResponse(data=permission)


@permissions_router.post("", response_model=ApiResponse[PermissionRead])
async def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Permissions.Create)),
):
    """Create a new permission."""
    db_permission = Permission.model_validate(permission)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return ApiResponse(data=db_permission)


@permissions_router.put("/{permission_id}", response_model=ApiResponse[PermissionRead])
async def update_permission(
    permission_id: str,
    permission: PermissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Permissions.Update)),
):
    """Update an existing permission."""
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    for key, value in permission.model_dump(exclude_unset=True).items():
        setattr(db_permission, key, value)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return ApiResponse(data=db_permission)


@permissions_router.delete("/{permission_id}", response_model=MessageResponse)
async def delete_permission(
    permission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Permissions.Delete)),
):
    """Delete a permission."""
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.delete(db_permission)
    db.commit()
    return MessageResponse(message="Permission deleted successfully")
