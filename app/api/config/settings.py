import logging
import os
from functools import lru_cache

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    """Class for storing settings."""

    kafka_host: str = os.getenv("KAFKA_HOST")
    kafka_port: str = os.getenv("KAFKA_PORT")
    kafka_topics: str = os.getenv("KAFKA_TOPICS")
    kafka_instance = f"broker:29092"
    file_encoding: str = "utf-8"


@lru_cache()
def get_settings() -> BaseSettings:
    """Get application settings usually stored as environment variables.

    Returns:
        Settings: Application settings.
    """
    log.info("Loading config settings from the environment...")
    return Settings()


DATABASE = {
    "db": {
        "database": os.getenv("DB"),
        "username": os.getenv("DB_USERNAME"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
    }
}
