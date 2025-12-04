from pydantic import BaseModel

from app.common.exceptions import NotFoundError
from app.features.files import repo
from app.features.files.model import File, FileType
from app.integrations.sftp.service import delete_event_header, delete_event_logo


# =========================
# FILE TYPE SERVICE
# =========================
def list_file_types(db, pagination):
    return repo.list_file_types(db, pagination)


def get_file_type(db, type_id: str):
    file_type = repo.get_file_type_by_id(db, type_id)
    if not file_type:
        raise NotFoundError("File type not found")
    return file_type


def create_file_type(db, payload: BaseModel):
    file_type = FileType.model_validate(payload)
    return repo.create_file_type(db, file_type)


def update_file_type(db, type_id: str, payload: BaseModel):
    file_type = repo.get_file_type_by_id(db, type_id)
    if not file_type:
        raise NotFoundError("File type not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_file_type(db, file_type, updates)


def delete_file_type(db, type_id: str):
    file_type = repo.get_file_type_by_id(db, type_id)
    if not file_type:
        raise NotFoundError("File type not found")

    repo.delete_file_type(db, file_type)


# =========================
# FILE SERVICE
# =========================
def list_files(db, pagination):
    return repo.list_files(db, pagination)


def get_file(db, file_id: str):
    file = repo.get_file_by_id(db, file_id)
    if not file:
        raise NotFoundError("File not found")
    return file


def create_file(db, payload: BaseModel):
    file = File.model_validate(payload)
    return repo.create_file(db, file)


def update_file(db, file_id: str, payload: BaseModel):
    file = repo.get_file_by_id(db, file_id)
    if not file:
        raise NotFoundError("File not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_file(db, file, updates)


def delete_file(db, file_id: str):
    file = repo.get_file_by_id(db, file_id)
    if not file:
        raise NotFoundError("File not found")

    purpose = file.purpose

    if purpose == "header":
        delete_event_header(file.relation_id)
    elif purpose == "logo":
        delete_event_logo(file.relation_id)

    repo.delete_file(db, file)
