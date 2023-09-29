import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Settings(BaseSettings):
    UDP_RECEIVER: str
    UDP_FROM_SERVER: str
    UDP_PATIENT_ID: int
    FALL_CONFIDENCE: int

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
