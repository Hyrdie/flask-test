from functools import lru_cache
import os
import logging

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str
    LOG_LEVEL: int = logging.INFO
    LOG_FILE: str = "logs/akasia.log"
    GET_LOGGER: str = "akasia_service"
    ORIGINS: list
    CORS_ALLOW_METHODS: list
    CORS_ALLOW_HEADERS: list
    TOKEN: str

    class Config:
        env_file = os.environ.get('ENV_FILE', 'app/.env')
        env_file_encoding = 'utf-8'

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()