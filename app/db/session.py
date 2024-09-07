from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base  # Import Base from base.py

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine('postgresql://postgres:postgres@db/storage_db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
