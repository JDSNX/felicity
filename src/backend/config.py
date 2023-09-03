import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class Settings(BaseSettings):
    fall_confidence: int
    udp_receiver: str
    udp_patient_id: int
    udp_from_server: str
    room_number: int
    database_url: str
    pin_light: int
    pin_window: int
    pin_door: int
    door: bool
    light: bool
    window: bool
    
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
