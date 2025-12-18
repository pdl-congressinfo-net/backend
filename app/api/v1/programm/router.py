from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.v1.programm import schema
from app.common.deps import get_db, require_permission
from app.common.permissions import EventSessions, Programms
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.programm import service
from app.features.users.model import User
from app.utils.pagination import PaginationParams

programm_router = APIRouter()


# =========================
# PROGRAMM ENDPOINTS
# =========================
@programm_router.get("", response_model=list[schema.ProgrammRead])
async def list_programms(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Programms.List)),
):
    """List all programm entries."""
    results, total = service.list_programms(db, pagination)
    return refine_list_response(response, results, total)


@programm_router.get("/{programm_id}", response_model=ApiResponse[schema.ProgrammRead])
async def get_programm(
    programm_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Programms.Show)),
):
    """Get a specific programm by ID."""
    programm = service.get_programm(db, programm_id)
    return ApiResponse(data=programm)


@programm_router.post("", response_model=ApiResponse[schema.ProgrammRead])
async def create_programm(
    programm: schema.ProgrammCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Programms.Create)),
):
    """Create a new programm entry."""
    db_programm = service.create_programm(db, programm)
    return ApiResponse(data=db_programm)


@programm_router.patch(
    "/{programm_id}", response_model=ApiResponse[schema.ProgrammRead]
)
async def update_programm(
    programm_id: str,
    programm: schema.ProgrammUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Programms.Update)),
):
    """Update an existing programm entry."""
    db_programm = service.update_programm(db, programm_id, programm)
    return ApiResponse(data=db_programm)


@programm_router.delete("/{programm_id}", response_model=MessageResponse)
async def delete_programm(
    programm_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Programms.Delete)),
):
    """Delete a programm entry."""
    service.delete_programm(db, programm_id)
    return MessageResponse(message="Programm deleted successfully")


# =========================
# EVENT SESSION ENDPOINTS
# =========================
@programm_router.get("/sessions", response_model=list[schema.EventSessionRead])
async def list_event_sessions(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventSessions.List)),
):
    """List all event sessions."""
    results, total = service.list_event_sessions(db, pagination)
    return refine_list_response(response, results, total)


@programm_router.get(
    "/sessions/{session_id}", response_model=ApiResponse[schema.EventSessionRead]
)
async def get_event_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventSessions.Show)),
):
    """Get a specific event session by ID."""
    session = service.get_event_session(db, session_id)
    return ApiResponse(data=session)


@programm_router.post("/sessions", response_model=ApiResponse[schema.EventSessionRead])
async def create_event_session(
    session: schema.EventSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventSessions.Create)),
):
    """Create a new event session."""
    db_session = service.create_event_session(db, session)
    return ApiResponse(data=db_session)


@programm_router.patch(
    "/sessions/{session_id}", response_model=ApiResponse[schema.EventSessionRead]
)
async def update_event_session(
    session_id: str,
    session: schema.EventSessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventSessions.Update)),
):
    """Update an existing event session."""
    db_session = service.update_event_session(db, session_id, session)
    return ApiResponse(data=db_session)


@programm_router.delete("/sessions/{session_id}", response_model=MessageResponse)
async def delete_event_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(EventSessions.Delete)),
):
    """Delete an event session."""
    service.delete_event_session(db, session_id)
    return MessageResponse(message="Event session deleted successfully")
