import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Settings(BaseSettings):
    database_url: str
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
