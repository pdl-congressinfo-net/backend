import uuid
from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    Response,
    UploadFile,
)
from fastapi import (
    File as UploadFileType,
)
from sqlalchemy.orm import Session

from app.api.v1.files.schema import FileRead
from app.common.deps import get_db, require_permission
from app.common.permissions import Files
from app.common.refine import refine_list_response
from app.common.responses import MessageResponse
from app.core.config import settings
from app.features.files import service
from app.features.files.model import File as FileModel
from app.features.users.model import User
from app.utils.pagination import PaginationParams

files_router = APIRouter()


@files_router.post("/upload", response_model=FileRead)
async def upload_file(
    uploaded_file: UploadFile = UploadFileType(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Files.Upload)),
):
    contents = await uploaded_file.read()

    file_id = str(uuid.uuid4())
    sftp_filename = f"{file_id}_{uploaded_file.filename}"
    remote_path = f"{settings.SFTP_DIRECTORY}/{sftp_filename}"

    # Save DB metadata
    now = datetime.utcnow()

    file = FileModel(
        id=file_id,
        name=uploaded_file.filename,
        size=len(contents),
        created_at=now,
        updated_at=now,
        uploaded_by=current_user.id,
        location=remote_path,
        external=False,
    )

    db.add(file)
    db.commit()
    db.refresh(file)

    return file


@files_router.get("", response_model=list[FileRead])
async def list_files(
    response: Response,
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(require_permission(Files.List)),
):
    files, total = service.list_files(db, pagination)
    return refine_list_response(response, files, total)


@files_router.get("/{file_id}", response_model=FileRead)
async def get_file(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Files.Show)),
):
    file = service.get_file(db, file_id)
    return file


@files_router.get("/{file_id}/download")
async def download_file(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Files.Download)),
):
    file = service.get_file(db, file_id)

    return Response(
        content="await service.download_file_contents(file.location)",
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file.name}"},
    )


@files_router.delete("/{file_id}", response_model=MessageResponse)
async def delete_file(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Files.Delete)),
):
    service.delete_file(db, file_id)

    return MessageResponse(message="File deleted successfully")
