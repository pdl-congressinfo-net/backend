from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.v1.events import schema
from app.common.deps import get_db, require_permission
from app.common.permissions import EventTypes, Events
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.events import service
from app.features.users.model import User
from app.utils.pagination import PaginationParams

events_router = APIRouter()


# =========================
# EVENT TYPE ENDPOINTS
# =========================
@events_router.get("/types", response_model=list[schema.EventTypeRead])
async def list_event_types(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.List)),
):
    """List all event types."""
    results, total = service.list_event_types(db, pagination)
    return refine_list_response(response, results, total)


@events_router.get("/types/{event_type_id}", response_model=ApiResponse[schema.EventTypeRead])
async def get_event_type(
    event_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.Show)),
):
    """Get a specific event type by ID."""
    event_type = service.get_event_type(db, event_type_id)
    return ApiResponse(data=event_type)


@events_router.post("/types", response_model=ApiResponse[schema.EventTypeRead])
async def create_event_type(
    event_type: schema.EventTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.Create)),
):
    """Create a new event type."""
    db_event_type = service.create_event_type(db, event_type)
    return ApiResponse(data=db_event_type)


@events_router.patch("/types/{event_type_id}", response_model=ApiResponse[schema.EventTypeRead])
async def update_event_type(
    event_type_id: str,
    event_type: schema.EventTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.Update)),
):
    """Update an existing event type."""
    db_event_type = service.update_event_type(db, event_type_id, event_type)
    return ApiResponse(data=db_event_type)


@events_router.delete("/types/{event_type_id}", response_model=MessageResponse)
async def delete_event_type(
    event_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.Delete)),
):
    """Delete an event type."""
    service.delete_event_type(db, event_type_id)
    return MessageResponse(message="Event type deleted successfully")


# =========================
# EVENT ENDPOINTS
# =========================
@events_router.get("/", response_model=list[schema.EventRead])
async def list_events(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.List)),
):
    """List all events."""
    results, total = service.list_events(db, pagination)
    return refine_list_response(response, results, total)


@events_router.get("/{event_id}", response_model=ApiResponse[schema.EventRead])
async def get_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Show)),
):
    """Get a specific event by ID."""
    event = service.get_event(db, event_id)
    return ApiResponse(data=event)


@events_router.post("/", response_model=ApiResponse[schema.EventRead])
async def create_event(
    event: schema.EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Create)),
):
    """Create a new event."""
    db_event = service.create_event(db, event)
    return ApiResponse(data=db_event)


@events_router.patch("/{event_id}", response_model=ApiResponse[schema.EventRead])
async def update_event(
    event_id: str,
    event: schema.EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Update)),
):
    """Update an existing event."""
    db_event = service.update_event(db, event_id, event)
    return ApiResponse(data=db_event)


@events_router.delete("/{event_id}", response_model=MessageResponse)
async def delete_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Delete)),
):
    """Delete an event."""
    service.delete_event(db, event_id)
    return MessageResponse(message="Event deleted successfully")


@events_router.post("/{event_id}/publish", response_model=ApiResponse[schema.EventRead])
async def publish_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Publish)),
):
    """Publish an event (make it public)."""
    db_event = service.publish_event(db, event_id)
    return ApiResponse(data=db_event)


@events_router.post("/{event_id}/unpublish", response_model=ApiResponse[schema.EventRead])
async def unpublish_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Publish)),
):
    """Unpublish an event (make it private)."""
    db_event = service.unpublish_event(db, event_id)
    return ApiResponse(data=db_event)
