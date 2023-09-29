from datetime import datetime
from typing import Optional
from pydantic import ConfigDict, BaseModel


class RoomBase(BaseModel):
    name: str


class RoomCreate(RoomBase):
    pass


class RoomInDBBase(RoomBase):
    id: int

    updated_at: datetime = datetime.now()
    model_config = ConfigDict(from_attributes=True)


class Room(RoomInDBBase):
    pass
