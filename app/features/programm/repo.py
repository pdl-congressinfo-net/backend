from sqlalchemy.orm import Session

from app.features.programm.model import EventSession, Programm
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query


# =========================
# PROGRAMM REPO
# =========================
def list_programms(db: Session, pagination: PaginationParams):
    query = db.query(Programm)
    return refine_query(query, Programm, pagination)


def get_programm_by_id(db: Session, programm_id: str):
    return db.query(Programm).filter(Programm.id == programm_id).first()


def create_programm(db: Session, programm: Programm):
    db.add(programm)
    db.commit()
    db.refresh(programm)
    return programm


def update_programm(db: Session, programm: Programm, updates: dict):
    for key, value in updates.items():
        setattr(programm, key, value)
    db.commit()
    db.refresh(programm)
    return programm


def delete_programm(db: Session, programm: Programm):
    db.delete(programm)
    db.commit()


# =========================
# EVENT SESSION REPO
# =========================


def list_event_sessions(db: Session, pagination: PaginationParams):
    query = db.query(EventSession)
    return refine_query(query, EventSession, pagination)


def get_event_session_by_id(db: Session, session_id: str):
    return db.query(EventSession).filter(EventSession.id == session_id).first()


def create_event_session(db: Session, session: EventSession):
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def update_event_session(db: Session, session: EventSession, updates: dict):
    for key, value in updates.items():
        setattr(session, key, value)
    db.commit()
    db.refresh(session)
    return session


def delete_event_session(db: Session, session: EventSession):
    db.delete(session)
    db.commit()
