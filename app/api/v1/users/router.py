from fastapi import APIRouter, Depends

from app.api.v1.users.schema import UserRead
from app.common.deps import require_permission
from app.common.permissions import Users
from app.common.responses import ApiResponse
from app.features.users.model import User

users_router = APIRouter()


@users_router.get("/me", response_model=ApiResponse[UserRead])
async def read_current_user(
    current_user: User = Depends(require_permission(Users.ShowMe)),
):
    """Get current user details."""

    return ApiResponse(data=current_user)
