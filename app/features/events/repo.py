from sqlalchemy.orm import Session

from app.features.events.model import Event, EventType
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query


# =========================
# EVENT TYPE REPO
# =========================
def list_event_types(db: Session, pagination: PaginationParams):
    query = db.query(EventType)
    return refine_query(query, EventType, pagination)


def get_event_type_by_id(db: Session, event_type_id: str):
    return db.query(EventType).filter(EventType.id == event_type_id).first()


def get_event_type_by_code(db: Session, code: str):
    return db.query(EventType).filter(EventType.code == code).first()


def create_event_type(db: Session, event_type: EventType):
    db.add(event_type)
    db.commit()
    db.refresh(event_type)
    return event_type


def update_event_type(db: Session, event_type: EventType, updates: dict):
    for key, value in updates.items():
        setattr(event_type, key, value)
    db.commit()
    db.refresh(event_type)
    return event_type


def delete_event_type(db: Session, event_type: EventType):
    db.delete(event_type)
    db.commit()


# =========================
# EVENT REPO
# =========================
def list_events(db: Session, pagination: PaginationParams):
    query = db.query(Event)
    return refine_query(query, Event, pagination)


def get_event_by_id(db: Session, event_id: str):
    return db.query(Event).filter(Event.id == event_id).first()


def create_event(db: Session, event: Event):
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def update_event(db: Session, event: Event, updates: dict):
    for key, value in updates.items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event


def delete_event(db: Session, event: Event):
    db.delete(event)
    db.commit()
