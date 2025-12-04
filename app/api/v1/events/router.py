from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.v1.events import schema
from app.common.deps import get_db, require_permission
from app.common.permissions import Categories, Events, EventTypes
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.events import service
from app.features.users.model import User
from app.utils.pagination import PaginationParams

events_router = APIRouter()


# =========================
# CATEGORIES
# =========================


@events_router.get("/categories", response_model=list[schema.CategoryRead])
async def list_event_categories(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.List)),
):
    results, total = service.list_categories(db, pagination)
    return refine_list_response(response, results, total)


@events_router.get(
    "/categories/{category_id}", response_model=ApiResponse[schema.CategoryRead]
)
async def get_event_category(
    category_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Categories.Show)),
):
    category = service.get_category(db, category_id)
    return ApiResponse(data=category)


@events_router.post("/categories", response_model=ApiResponse[schema.CategoryRead])
async def create_event_category(
    category: schema.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Categories.Create)),
):
    category = service.create_category(db, category)
    return ApiResponse(data=category)


@events_router.put(
    "/categories/{category_id}", response_model=ApiResponse[schema.CategoryRead]
)
async def update_event_category(
    category_id: str,
    category: schema.CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Categories.Update)),
):
    category = service.update_category(db, category_id, category)
    return ApiResponse(data=category)


@events_router.delete("/categories/{category_id}", response_model=MessageResponse)
async def delete_event_category(
    category_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Categories.Delete)),
):
    service.delete_category(db, category_id)
    return MessageResponse(message="Event category deleted successfully")


# =========================
# EVENT TYPES
# =========================


@events_router.get("/types", response_model=list[schema.EventTypeRead])
async def list_event_types(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.List)),
):
    results, total = service.list_event_types(db, pagination)
    return refine_list_response(response, results, total)


@events_router.get(
    "/types/{event_type_id}", response_model=ApiResponse[schema.EventTypeRead]
)
async def get_event_type(
    event_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.Show)),
):
    event_type = service.get_event_type(db, event_type_id)
    return ApiResponse(data=event_type)


@events_router.post("/types", response_model=ApiResponse[schema.EventTypeRead])
async def create_event_type(
    event_type: schema.EventTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.Create)),
):
    event_type = service.create_event_type(db, event_type)
    return ApiResponse(data=event_type)


@events_router.put(
    "/types/{event_type_id}", response_model=ApiResponse[schema.EventTypeRead]
)
async def update_event_type(
    event_type_id: str,
    event_type: schema.EventTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.Update)),
):
    event_type = service.update_event_type(db, event_type_id, event_type)
    return ApiResponse(data=event_type)


@events_router.delete("/types/{event_type_id}", response_model=MessageResponse)
async def delete_event_type(
    event_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.Delete)),
):
    service.delete_event_type(db, event_type_id)
    return MessageResponse(message="Event type deleted successfully")


# =========================
# EVENTS
# =========================


@events_router.get("", response_model=list[schema.EventRead])
async def list_events(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.List)),
):
    results, total = service.list_events(db, current_user, pagination)
    return refine_list_response(response, results, total)


@events_router.get("/{event_id}", response_model=ApiResponse[schema.EventRead])
async def get_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Show)),
):
    event = service.get_event(db, event_id)
    return ApiResponse(data=event)


@events_router.post("", response_model=ApiResponse[schema.EventRead])
async def create_event(
    event: schema.EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Create)),
):
    event = service.create_event(db, event)
    return ApiResponse(data=event)


@events_router.put("/{event_id}", response_model=ApiResponse[schema.EventRead])
async def update_event(
    event_id: str,
    event: schema.EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Update)),
):
    event = service.update_event(db, event_id, event)
    return ApiResponse(data=event)


@events_router.delete("/{event_id}", response_model=MessageResponse)
async def delete_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Delete)),
):
    service.delete_event(db, event_id)
    return MessageResponse(message="Event deleted successfully")
