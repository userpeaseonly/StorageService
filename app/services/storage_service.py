import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.storage import Storage
from fastapi.responses import FileResponse
from uuid import uuid4

STORAGE_PATH = "uploads/"

# def save_file(file: UploadFile) -> str:
#     filename = f"{uuid4()}.{file.filename.split('.')[-1]}"
#     file_path = os.path.join(STORAGE_PATH, filename)
#     with open(file_path, "wb") as buffer:
#         buffer.write(file.file.read())
#     return file_path

def save_file(file: UploadFile, project_team: str, project_name: str) -> str:
    # Create directories in the format project_team/project_name
    folder_path = os.path.join(STORAGE_PATH, project_team, project_name)
    os.makedirs(folder_path, exist_ok=True)

    # Save the file in the corresponding project directory
    filename = f"{uuid4()}.{file.filename.split('.')[-1]}"
    file_path = os.path.join(folder_path, filename)

    # Save file to disk
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path

# def create_file(db: Session, project_name: str, project_team: str, file: UploadFile):
#     file_path = save_file(file)
#     storage = Storage(project_name=project_name, project_team=project_team, file=file_path)
#     db.add(storage)
#     db.commit()
#     db.refresh(storage)
#     return storage

def create_file(db: Session, project_name: str, project_team: str, file: UploadFile):
    # Save the file with the project_team/project_name folder structure
    file_path = save_file(file, project_team, project_name)
    storage = Storage(project_name=project_name, project_team=project_team, file=file_path)
    db.add(storage)
    db.commit()
    db.refresh(storage)
    return storage

# def get_file(db: Session, project_name: str, project_team: str):
#     return db.query(Storage).filter_by(project_name=project_name, project_team=project_team).first()

# def get_file(db: Session, project_name: str, project_team: str):
#     storage = db.query(Storage).filter_by(project_name=project_name, project_team=project_team).first()
#     if storage:
#         # Read the file and return its binary content
#         with open(storage.file, "rb") as f:
#             file_content = f.read()
#         return {
#             "id": storage.id,
#             "project_name": storage.project_name,
#             "project_team": storage.project_team,
#             "file": file_content,  # Return the actual file content
#             "created_at": storage.created_at,
#             "updated_at": storage.updated_at,
#         }
#     return None


def get_file(db: Session, project_name: str, project_team: str):
    storage = db.query(Storage).filter_by(project_name=project_name, project_team=project_team).first()
    if storage:
        # Return the file as a FileResponse
        return FileResponse(path=storage.file, media_type="application/octet-stream", filename=storage.file.split("/")[-1])
    return None

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
