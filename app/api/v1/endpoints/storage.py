from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
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


# @router.get("/", response_model=schemas.StorageInDB)
# def get_storage(
#     project_name: str,
#     project_team: str,
#     db: Session = Depends(get_db)
# ):
#     storage = get_file(db, project_name, project_team)
#     if not storage:
#         raise HTTPException(status_code=404, detail="File not found")
#     return storage

# @router.get("/", response_model=schemas.StorageInDB)
# def get_storage(
#     project_name: str,
#     project_team: str,
#     db: Session = Depends(get_db)
# ):
#     storage_data = get_file(db, project_name, project_team)
#     if not storage_data:
#         raise HTTPException(status_code=404, detail="File not found")

#     # Returning the file and other metadata
#     return storage_data

@router.get("/", response_class=FileResponse)
def get_storage(
        project_name: str,
        project_team: str,
        db: Session = Depends(get_db)
):
    storage_file = get_file(db, project_name, project_team)
    if not storage_file:
        raise HTTPException(status_code=404, detail="File not found")

    return storage_file


@router.put("/{id}/", response_model=schemas.StorageInDB)
def update_storage(
        id: int,
        project_name: str,
        project_team: str, # project name va team qaysi foldetni update qilish kerakligini aniq bilish iuchun kerak
        file: UploadFile = File(None),
        db: Session = Depends(get_db)
):
    return update_file(db, id, file, project_name, project_team)


@router.delete("/{id}/", response_model=schemas.StorageInDB)
def delete_storage(
        id: int,
        db: Session = Depends(get_db)
):
    return delete_file(db, id) # deletega id ni bersa, projectni ichidagi fileni o'chirib tashlaydi


@router.get("/download", response_class=FileResponse)
def download_file(
        project_name: str,
        project_team: str,
        db: Session = Depends(get_db)
):
    storage_file = get_file(db, project_name, project_team)
    if not storage_file:
        raise HTTPException(status_code=404, detail="File not found")

    return storage_file
