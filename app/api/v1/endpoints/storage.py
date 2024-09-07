from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.schemas import storage as schemas
from app.models.storage import Storage
from app.db.session import get_db
from app.services.storage_service import create_file, get_file, update_file, delete_file

router = APIRouter()

@router.post("/", response_model=schemas.StorageInDB)
def upload_file(
    project_name: str,
    project_team: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return create_file(db, project_name, project_team, file)

@router.get("/", response_model=schemas.StorageInDB)
def get_storage(
    project_name: str,
    project_team: str,
    db: Session = Depends(get_db)
):
    storage = get_file(db, project_name, project_team)
    if not storage:
        raise HTTPException(status_code=404, detail="File not found")
    return storage

@router.put("/{id}", response_model=schemas.StorageInDB)
def update_storage(
    id: int,
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    return update_file(db, id, file)

@router.delete("/{id}", response_model=schemas.StorageInDB)
def delete_storage(id: int, db: Session = Depends(get_db)):
    return delete_file(db, id)
