from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StorageBase(BaseModel):
    project_name: str
    project_team: str

class StorageCreate(StorageBase):
    file: str

class StorageUpdate(BaseModel):
    file: Optional[str] = None

class StorageInDB(StorageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
