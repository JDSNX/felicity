from pydantic import BaseModel
from enum import Enum

class Location(str, Enum):
    LIVING_ROOM = 'LIVING ROOM'
    COMFORT_ROOM = 'COMFORT_ROOM'