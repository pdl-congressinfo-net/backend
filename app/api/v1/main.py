from fastapi import APIRouter

from app.api.v1.auth.router import auth_router
from app.api.v1.companies.router import companies_router
from app.api.v1.events.router import events_router
from app.api.v1.locations.router import locations_router
from app.api.v1.permissions.router import permissions_router
from app.api.v1.programm.router import programm_router
from app.api.v1.roles.router import roles_router
from app.api.v1.users.router import users_router
from app.api.v1.utils.router import utils_router

v1_router = APIRouter()
v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(companies_router, prefix="/companies", tags=["companies"])
v1_router.include_router(events_router, prefix="/events", tags=["events"])
v1_router.include_router(locations_router, prefix="/locations", tags=["locations"])
v1_router.include_router(programm_router, prefix="/programm", tags=["programm"])
v1_router.include_router(
    permissions_router, prefix="/permissions", tags=["permissions"]
)

v1_router.include_router(roles_router, prefix="/roles", tags=["roles"])
v1_router.include_router(users_router, prefix="/users", tags=["users"])
v1_router.include_router(utils_router, prefix="/utils", tags=["utils"])
