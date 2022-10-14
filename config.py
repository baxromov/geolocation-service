import logging
import os
from functools import lru_cache

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    """Class for storing settings."""

    kafka_host: str = os.getenv("KAFKA_HOST", 'localhost')
    kafka_port: str = os.getenv("KAFKA_PORT", '9092')
    kafka_topics: str = os.getenv("KAFKA_TOPICS", 'geolocation_service')
    kafka_instance = f"{kafka_host}:{kafka_port}"
    file_encoding: str = "utf-8"


@lru_cache()
def get_settings() -> BaseSettings:
    """Get application settings usually stored as environment variables.

    Returns:
        Settings: Application settings.
    """
    log.info("Loading config settings from the environment...")
    return Settings()