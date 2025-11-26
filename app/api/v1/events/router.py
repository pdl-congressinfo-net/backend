from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.api.v1.events.schema import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    EventCreate,
    EventRead,
    EventTypeCreate,
    EventTypeRead,
    EventTypeUpdate,
    EventUpdate,
)
from app.common.deps import get_db, require_permission
from app.common.permissions import Categories, Events, EventTypes
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.events.model import Category, Event, EventType
from app.features.users.model import User
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query

events_router = APIRouter()


@events_router.get("/categories", response_model=list[CategoryRead])
async def list_event_categories(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.List)),
):
    """List all event categories."""
    query = db.query(Category)
    results, total = refine_query(query, Category, pagination)
    return refine_list_response(response, results, total)


@events_router.get(
    "/categories/{category_id}", response_model=ApiResponse[CategoryRead]
)
async def get_event_category(
    category_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Categories.Show)),
):
    """Get event category by ID."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Event category not found")
    return ApiResponse(data=category)


@events_router.post("/categories", response_model=ApiResponse[CategoryRead])
async def create_event_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Categories.Create)),
):
    """Create a new event category."""
    db_category = Category.model_validate(category)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return ApiResponse(data=db_category)


@events_router.put(
    "/categories/{category_id}", response_model=ApiResponse[CategoryRead]
)
async def update_event_category(
    category_id: str,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Categories.Update)),
):
    """Update an existing event category."""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Event category not found")
    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return ApiResponse(data=db_category)


@events_router.delete("/categories/{category_id}", response_model=MessageResponse)
async def delete_event_category(
    category_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Categories.Delete)),
):
    """Delete an event category."""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Event category not found")
    db.delete(db_category)
    db.commit()
    return MessageResponse(message="Event category deleted successfully")


@events_router.get("/types", response_model=list[EventTypeRead])
async def list_event_types(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.List)),
):
    """List all event types."""
    query = db.query(EventType)
    results, total = refine_query(query, EventType, pagination)
    return refine_list_response(response, results, total)


@events_router.get("/types/{event_type_id}", response_model=ApiResponse[EventTypeRead])
async def get_event(
    event_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.Show)),
):
    """Get event type by ID."""
    event_type = db.query(EventType).filter(EventType.id == event_type_id).first()
    if not event_type:
        raise HTTPException(status_code=404, detail="Event type not found")
    return ApiResponse(data=event_type)


@events_router.post("/types", response_model=ApiResponse[EventTypeRead])
async def create_event_type(
    event_type: EventTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.Create)),
):
    """Create a new event type."""
    db_event_type = EventType.model_validate(event_type)
    db.add(db_event_type)
    db.commit()
    db.refresh(db_event_type)
    return ApiResponse(data=db_event_type)


@events_router.put("/types/{event_type_id}", response_model=ApiResponse[EventTypeRead])
async def update_event_type(
    event_type_id: str,
    event_type: EventTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.Update)),
):
    """Update an existing event type."""
    db_event_type = db.query(EventType).filter(EventType.id == event_type_id).first()
    if not db_event_type:
        raise HTTPException(status_code=404, detail="Event type not found")
    for key, value in event_type.model_dump(exclude_unset=True).items():
        setattr(db_event_type, key, value)
    db.add(db_event_type)
    db.commit()
    db.refresh(db_event_type)
    return ApiResponse(data=db_event_type)


@events_router.delete("/types/{event_type_id}", response_model=MessageResponse)
async def delete_event_type(
    event_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventTypes.Delete)),
):
    """Delete an event type."""
    db_event_type = db.query(EventType).filter(EventType.id == event_type_id).first()
    if not db_event_type:
        raise HTTPException(status_code=404, detail="Event type not found")
    db.delete(db_event_type)
    db.commit()
    return MessageResponse(message="Event type deleted successfully")


@events_router.get("", response_model=list[EventRead])
async def list_events(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.List)),
):
    """List all events."""
    query = db.query(Event)
    results, total = refine_query(query, Event, pagination)
    return refine_list_response(response, results, total)


@events_router.get("/{event_id}", response_model=ApiResponse[EventRead])
async def get_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Show)),
):
    """Get event by ID."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return ApiResponse(data=event)


@events_router.post("", response_model=ApiResponse[EventRead])
async def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Create)),
):
    """Create a new event."""
    db_event = Event.model_validate(event)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return ApiResponse(data=db_event)


@events_router.put("/{event_id}", response_model=ApiResponse[EventRead])
async def update_event(
    event_id: str,
    event: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Update)),
):
    """Update an existing event."""
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in event.model_dump(exclude_unset=True).items():
        setattr(db_event, key, value)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return ApiResponse(data=db_event)


@events_router.delete("/{event_id}", response_model=MessageResponse)
async def delete_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Events.Delete)),
):
    """Delete an event."""
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return MessageResponse(message="Event deleted successfully")
