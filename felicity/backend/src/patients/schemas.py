import re
from datetime import datetime, date
from typing import Any, Optional
from pydantic import BaseModel, EmailStr, NameEmail, Field, field_validator, validator


class PatientBase(BaseModel):
    full_name: str
    date_of_birth: date
    contact_person: str
    contact_number: str = Field(max_length=12)
    email: Optional[EmailStr]

    @field_validator("date_of_birth", mode="before")
    @classmethod
    def parse_dob(cls, dob: date):
        return datetime.strptime(dob, "%Y-%d-%m").date()

    @field_validator("contact_number", mode="after")
    @classmethod
    def parse_contact_number(cls, cn: str):
        return f"63{int(cn)}" if cn.startswith(("0")) else cn


class PatientUpdateIn(PatientBase):
    pass


class PatientUpdate(PatientUpdateIn):
    updated_at: datetime = datetime.now()


# Properties to receive via API on creation
class PatientCreate(PatientBase):
    pass


class PatientInDBBase(PatientBase):
    id: int

    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        from_attributes = True


class Patient(PatientInDBBase):
    pass
