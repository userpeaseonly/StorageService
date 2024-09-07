# app/models/storage.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base  # Import the Base from base.py

class Storage(Base):
    __tablename__ = "storage"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    project_team = Column(String, index=True)
    file = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # Default and on update
