from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class Location(str, Enum):
    LIVING_ROOM = 'LIVING ROOM'
    COMFORT_ROOM = 'COMFORT_ROOM'

class AccountUpdate(BaseModel):
    password: str 
    first_name: str 
    middle_name: str 
    last_name: str
    contact_number: str 

class AccountBase(AccountUpdate):
    username: str 
    is_admin: bool = Field(default=False)

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str="bearer"
