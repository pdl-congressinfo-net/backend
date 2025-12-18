from pydantic import BaseModel

from app.common.exceptions import NotFoundError
from app.features.programm import repo
from app.features.programm.model import EventSession, Programm


# =========================
# PROGRAMM SERVICE
# =========================
def list_programms(db, pagination):
    return repo.list_programms(db, pagination)


def get_programm(db, programm_id: str):
    programm = repo.get_programm_by_id(db, programm_id)
    if not programm:
        raise NotFoundError("Programm not found")
    return programm


def create_programm(db, payload: BaseModel):
    programm = Programm.model_validate(payload)
    return repo.create_programm(db, programm)


def update_programm(db, programm_id: str, payload: BaseModel):
    programm = repo.get_programm_by_id(db, programm_id)
    if not programm:
        raise NotFoundError("Programm not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_programm(db, programm, updates)


def delete_programm(db, programm_id: str):
    programm = repo.get_programm_by_id(db, programm_id)
    if not programm:
        raise NotFoundError("Programm not found")
    repo.delete_programm(db, programm)


# =========================
# EVENT SESSION SERVICE
# =========================


def list_event_sessions(db, pagination):
    return repo.list_event_sessions(db, pagination)


def get_event_session(db, session_id: str):
    session = repo.get_event_session_by_id(db, session_id)
    if not session:
        raise NotFoundError("Event session not found")
    return session


def create_event_session(db, payload: BaseModel):
    session = EventSession.model_validate(payload)
    return repo.create_event_session(db, session)


def update_event_session(db, session_id: str, payload: BaseModel):
    session = repo.get_event_session_by_id(db, session_id)
    if not session:
        raise NotFoundError("Event session not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_event_session(db, session, updates)


def delete_event_session(db, session_id: str):
    session = repo.get_event_session_by_id(db, session_id)
    if not session:
        raise NotFoundError("Event session not found")
    repo.delete_event_session(db, session)
