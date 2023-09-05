from pydantic import BaseModel, Field
from datetime import datetime


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


class PatientBase(BaseModel):
    room_no: str = Field(default="RM ###")
    first_name: str
    middle_name: str
    last_name: str
    address: str
    place_of_birth: str
    date_of_birth: datetime = Field(default=datetime.utcnow())
    gender: str
    contact_person: str
    contact_number: str


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    id: int

    last_updated: datetime

    class Config:
        from_attributes = True


class PatientPi(Patient):
    is_fall: bool = False
    is_connected: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
