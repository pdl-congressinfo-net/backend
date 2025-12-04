from sqlalchemy.orm import Session

from app.features.files.model import File, FileType
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query


# =========================
# FILE TYPE REPO
# =========================
def list_file_types(db: Session, pagination: PaginationParams):
    query = db.query(FileType)
    return refine_query(query, FileType, pagination)


def get_file_type_by_id(db: Session, type_id: str):
    return db.query(FileType).filter(FileType.id == type_id).first()


def create_file_type(db: Session, file_type: FileType):
    db.add(file_type)
    db.commit()
    db.refresh(file_type)
    return file_type


def update_file_type(db: Session, file_type: FileType, updates: dict):
    for key, value in updates.items():
        setattr(file_type, key, value)
    db.commit()
    db.refresh(file_type)
    return file_type


def delete_file_type(db: Session, file_type: FileType):
    db.delete(file_type)
    db.commit()


# =========================
# FILE REPO
# =========================
def list_files(db: Session, pagination: PaginationParams):
    query = db.query(File)
    return refine_query(query, File, pagination)


def get_file_by_id(db: Session, file_id: str):
    return db.query(File).filter(File.id == file_id).first()


def create_file(db: Session, file: File):
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


def update_file(db: Session, file: File, updates: dict):
    for key, value in updates.items():
        setattr(file, key, value)
    db.commit()
    db.refresh(file)
    return file


def delete_file(db: Session, file: File):
    db.delete(file)
    db.commit()
