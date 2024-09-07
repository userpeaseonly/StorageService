# app/main.py

from fastapi import FastAPI
from app.api.v1.endpoints import storage
from app.db.session import engine
from app.db.base import Base  # Import Base for table creation
from app.models.storage import Storage  # Import the model explicitly to ensure table creation
import os
import logging

app = FastAPI()

# Ensure the 'uploads/' directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.on_event("startup")
def on_startup():
    logging.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logging.info("Tables created!")

app.include_router(storage.router, prefix="/api/v1/storage")
