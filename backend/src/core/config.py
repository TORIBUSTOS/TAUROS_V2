from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    """Configuración central - NO hardcoding"""
    DATABASE_URL: str = "sqlite:///./toro_prime.db"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
