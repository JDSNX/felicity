from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from database.core import Base

if TYPE_CHECKING:
    from patients.models import Patient  # noqa: F401


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    is_occupied = Column(Boolean(), default=False)
    patients_id = Column(Integer, ForeignKey("patients.id"))
    patients = relationship("Patient", back_populates="room")

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
