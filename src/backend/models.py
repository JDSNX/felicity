from database.core import Base
from datetime import datetime
from passlib import hash
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    Boolean,
    ForeignKey
)

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    contact_number = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow)

    
    def verify_password(self, password: str=None):
        return hash.bcrypt.verify(password, self.password)

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, index=True)
    room_no = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    place_of_birth = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    contact_person = Column(String, nullable=False)
    contact_number = Column(String, nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    is_connected = Column(Boolean, nullable=False, default=False)
    is_fall = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow)

class Fall(Base):
    __tablename__ = 'falls'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    date_of_fall = Column(DateTime, index=True)

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    room_number = Column(String, index=True)

    