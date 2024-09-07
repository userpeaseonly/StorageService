# app/schemas/storage.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StorageBase(BaseModel):
    project_name: str
    project_team: str

class StorageCreate(StorageBase):
    file: str

# class StorageInDB(StorageBase):
#     id: int
#     created_at: datetime
#     updated_at: Optional[datetime]  # Ensure this is Optional to handle cases where it's None

#     class Config:
#         from_attributes = True

class StorageInDB(StorageBase):
    id: int
    file: bytes  # Store the file content as bytes
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

