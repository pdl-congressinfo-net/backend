from pydantic import BaseModel

from app.common.deps import check_permissions_user
from app.common.exceptions import NotFoundError
from app.common.permissions import Events
from app.features.events import repo
from app.features.events.model import Category, Event, EventType


# =========================
# CATEGORY SERVICE
# =========================
def list_categories(db, pagination):
    return repo.list_categories(db, pagination)


def get_category(db, category_id: str):
    category = repo.get_category_by_id(db, category_id)
    if not category:
        raise NotFoundError("Event category not found")
    return category


def create_category(db, payload: BaseModel):
    category = Category.model_validate(payload)
    return repo.create_category(db, category)


def update_category(db, category_id: str, payload: BaseModel):
    category = repo.get_category_by_id(db, category_id)
    if not category:
        raise NotFoundError("Event category not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_category(db, category, updates)


def delete_category(db, category_id: str):
    category = repo.get_category_by_id(db, category_id)
    if not category:
        raise NotFoundError("Event category not found")

    repo.delete_category(db, category)


# =========================
# EVENT TYPE SERVICE
# =========================
def list_event_types(db, pagination):
    return repo.list_event_types(db, pagination)


def get_event_type(db, event_type_id: str):
    event_type = repo.get_event_type_by_id(db, event_type_id)
    if not event_type:
        raise NotFoundError("Event type not found")
    return event_type


def create_event_type(db, payload: BaseModel):
    event_type = EventType.model_validate(payload)
    return repo.create_event_type(db, event_type)


def update_event_type(db, event_type_id, payload):
    event_type = repo.get_event_type_by_id(db, event_type_id)
    if not event_type:
        raise NotFoundError("Event type not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_event_type(db, event_type, updates)


def delete_event_type(db, event_type_id: str):
    event_type = repo.get_event_type_by_id(db, event_type_id)
    if not event_type:
        raise NotFoundError("Event type not found")

    repo.delete_event_type(db, event_type)


# =========================
# EVENT SERVICE
# =========================
def list_events(db, user, pagination):
    can_view_all = check_permissions_user(user, [Events.ListAll])
    return repo.list_events(db, can_view_all, pagination)


def get_event(db, event_id):
    event = repo.get_event_by_id(db, event_id)
    if not event:
        raise NotFoundError("Event not found")
    return event


def create_event(db, payload: BaseModel):
    event = Event.model_validate(payload)
    return repo.create_event(db, event)


def update_event(db, event_id, payload):
    event = repo.get_event_by_id(db, event_id)
    if not event:
        raise NotFoundError("Event not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_event(db, event, updates)


def delete_event(db, event_id):
    event = repo.get_event_by_id(db, event_id)
    if not event:
        raise NotFoundError("Event not found")

    repo.delete_event(db, event)
