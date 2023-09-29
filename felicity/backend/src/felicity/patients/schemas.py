import re
from datetime import datetime, date
from typing import Any, Optional
from pydantic import ConfigDict, BaseModel, EmailStr, Field, field_validator

from rooms.schemas import Room


class PatientBase(BaseModel):
    full_name: str
    date_of_birth: date
    contact_person: str
    contact_number: str = Field(max_length=12)
    email: Optional[EmailStr] = None

    @field_validator("date_of_birth", mode="before")
    @classmethod
    def parse_dob(cls, dob: date):
        return datetime.strptime(dob, "%Y-%m-%d").date()

    @field_validator("contact_number", mode="after")
    @classmethod
    def parse_contact_number(cls, cn: str):
        return f"63{int(cn)}" if cn.startswith(("0")) else cn


class PatientUpdate(PatientBase):
    pass


# Properties to receive via API on creation
class PatientCreate(PatientBase):
    pass


class PatientInDBBase(PatientBase):
    id: int
    room: list[Room]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    model_config = ConfigDict(from_attributes=True)


class Patient(PatientInDBBase):
    pass


class PatientStatus(BaseModel):
    id: int
    is_active: bool
