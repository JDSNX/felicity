from typing import TYPE_CHECKING

from passlib import hash
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime
from database.core import Base

# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    date_of_birth = Column(String)
    contact_person = Column(String)
    contact_number = Column(String)
    email = Column(String, index=True, nullable=False)
    is_active = Column(Boolean(), default=True)
    room_no = Column(String, default="N/A")
    fall_status = Column(Boolean(), default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
