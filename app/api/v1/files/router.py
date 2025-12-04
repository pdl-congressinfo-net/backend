import uuid
from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
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
from app.core.config import settings
from app.core.files import sftp_connect
from app.features.files.model import File as FileModel
from app.features.users.model import User

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

    # Upload to SFTP
    try:
        sftp = sftp_connect()

        with sftp.file(remote_path, "wb") as f:
            f.write(contents)

        sftp.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SFTP upload failed: {str(e)}")

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
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Files.List)),
):
    files = db.query(FileModel).all()
    return files


@files_router.get("/{file_id}", response_model=FileRead)
async def get_file(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Files.Show)),
):
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return file


@files_router.get("/{file_id}/download")
async def download_file(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Files.Download)),
):
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Download from SFTP
    try:
        sftp = sftp_connect()
        with sftp.file(file.location, "rb") as f:
            data = f.read()
        sftp.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SFTP download failed: {str(e)}")

    return Response(
        content=data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file.name}"},
    )


@files_router.delete("/{file_id}", status_code=204)
async def delete_file(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Files.Delete)),
):
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Delete from SFTP
    try:
        sftp = sftp_connect()
        sftp.remove(file.location)
        sftp.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SFTP delete failed: {str(e)}")

    db.delete(file)
    db.commit()

    return Response(status_code=204)
