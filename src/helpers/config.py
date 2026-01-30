from pathlib import Path
import json
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = ""
    APP_VERSION: str = ""
    OPENAI_API_KEY: str = ""

    FILE_ALLOWED_EXTENSIONS: List[str] = ["text/plain", "application/pdf"]
    FILE_MAX_SIZE: int = 10 * 1024 * 1024 
    FILE_CHUNK_SIZE: int = 512000


    class Config:
        env_file = ".env"

def get_settings():
    return Settings()