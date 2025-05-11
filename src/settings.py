import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    logging_level: str = logging.WARNING
    api_token: str = "token"
    kafka_host: str = "localhost"
    kafka_port: int = 9092


settings = Settings()
logging.basicConfig(level=settings.logging_level)
