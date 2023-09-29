from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.core import Base

if TYPE_CHECKING:
    from rooms.models import Room  # noqa: F401


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    date_of_birth = Column(String)
    contact_person = Column(String)
    contact_number = Column(String)
    email = Column(String, index=True, nullable=False)
    is_active = Column(Boolean(), default=True)
    fall_status = Column(Boolean(), default=False)
    room = relationship("Room", back_populates="patients")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
