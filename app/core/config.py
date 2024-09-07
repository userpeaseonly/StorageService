import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")  # Set default to 'local'
    DATABASE_URL: str

    class Config:
        env_file = f".env.{os.getenv('ENVIRONMENT', 'local')}"

# Create an instance of the Settings class
settings = Settings()
