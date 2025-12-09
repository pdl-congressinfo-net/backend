from sqlalchemy.orm import Session

from app.features.files.model import File
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query


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
