from typing import TYPE_CHECKING

from passlib import hash
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime
from database.core import Base

# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # created_at = Column(DateTime, default=datetime.utcnow)
    # last_updated = Column(DateTime, default=datetime.utcnow)

    def verify_password(self, password: str = None):
        return hash.bcrypt.verify(password, self.hashed_password)
