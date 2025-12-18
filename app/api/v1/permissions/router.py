from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.v1.permissions import schema
from app.common.deps import get_db, require_permission
from app.common.permissions import Permissions
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.permissions import service
from app.features.users.model import User
from app.utils.pagination import PaginationParams

permissions_router = APIRouter()


# =========================
# PERMISSION ENDPOINTS
# =========================
@permissions_router.get("", response_model=list[schema.PermissionRead])
async def list_permissions(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Permissions.List)),
):
    """List all permissions."""
    results, total = service.list_permissions(db, pagination)
    return refine_list_response(response, results, total)


@permissions_router.post("", response_model=ApiResponse[schema.PermissionRead])
async def create_permission(
    permission: schema.PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Permissions.Create)),
):
    """Create a new permission."""
    db_permission = service.create_permission(db, permission)
    return ApiResponse(data=db_permission)


@permissions_router.delete("/{permission_id}", response_model=MessageResponse)
async def delete_permission(
    permission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Permissions.Delete)),
):
    """Delete a permission."""
    service.delete_permission(db, permission_id)
    return MessageResponse(message="Permission deleted successfully")
