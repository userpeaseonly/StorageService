import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.storage import Storage
from uuid import uuid4

STORAGE_PATH = "uploads/"

def save_file(file: UploadFile) -> str:
    filename = f"{uuid4()}.{file.filename.split('.')[-1]}"
    file_path = os.path.join(STORAGE_PATH, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_path

def create_file(db: Session, project_name: str, project_team: str, file: UploadFile):
    file_path = save_file(file)
    storage = Storage(project_name=project_name, project_team=project_team, file=file_path)
    db.add(storage)
    db.commit()
    db.refresh(storage)
    return storage

def get_file(db: Session, project_name: str, project_team: str):
    return db.query(Storage).filter_by(project_name=project_name, project_team=project_team).first()

def update_file(db: Session, id: int, file: UploadFile):
    storage = db.query(Storage).filter_by(id=id).first()
    if file:
        storage.file = save_file(file)
    db.commit()
    db.refresh(storage)
    return storage

def delete_file(db: Session, id: int):
    storage = db.query(Storage).filter_by(id=id).first()
    if storage:
        os.remove(storage.file)
        db.delete(storage)
        db.commit()
    return storage
