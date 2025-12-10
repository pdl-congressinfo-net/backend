from pydantic import BaseModel

from app.common.exceptions import NotFoundError
from app.features.events import repo
from app.features.events.model import Event, EventType


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


def get_event_type_by_code(db, code: str):
    event_type = repo.get_event_type_by_code(db, code)
    if not event_type:
        raise NotFoundError("Event type not found")
    return event_type


def create_event_type(db, payload: BaseModel):
    event_type = EventType.model_validate(payload)
    return repo.create_event_type(db, event_type)


def update_event_type(db, event_type_id: str, payload: BaseModel):
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
def list_events(db, pagination):
    return repo.list_events(db, pagination)


def get_event(db, event_id: str):
    event = repo.get_event_by_id(db, event_id)
    if not event:
        raise NotFoundError("Event not found")
    return event


def create_event(db, payload: BaseModel):
    event = Event.model_validate(payload)
    return repo.create_event(db, event)


def update_event(db, event_id: str, payload: BaseModel):
    event = repo.get_event_by_id(db, event_id)
    if not event:
        raise NotFoundError("Event not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_event(db, event, updates)


def delete_event(db, event_id: str):
    event = repo.get_event_by_id(db, event_id)
    if not event:
        raise NotFoundError("Event not found")
    repo.delete_event(db, event)


def publish_event(db, event_id: str):
    event = repo.get_event_by_id(db, event_id)
    if not event:
        raise NotFoundError("Event not found")

    updates = {"is_public": True}
    return repo.update_event(db, event, updates)


def unpublish_event(db, event_id: str):
    event = repo.get_event_by_id(db, event_id)
    if not event:
        raise NotFoundError("Event not found")

    updates = {"is_public": False}
    return repo.update_event(db, event, updates)
