from datetime import datetime, timedelta
from typing import Any
from passlib.hash import bcrypt

from sqlalchemy.orm import Session

from users.models import User as User_Model
from users.schemas import User, UserCreate, UserUpdate
from users.exceptions import InvalidCredentials


async def get_user_by_email(db: Session, *, email: str) -> User_Model:
    return db.query(User_Model).filter(User_Model.email == email).first()


async def get_user_by_id(db: Session, *, user_id: int) -> User_Model:
    return db.query(User_Model).filter(User_Model.id == user_id).first()


async def create(db: Session, *, user: UserCreate) -> User_Model:
    hashed_password = bcrypt.hash(user.password)

    user_obj = User_Model(
        email=user.email,
        hashed_password=hashed_password,
        is_superuser=user.is_superuser,
        full_name=user.full_name,
    )

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    return User.model_validate(user_obj)


async def update(db: Session, *, user_db: User_Model, obj: UserUpdate):
    user_db.hashed_password = bcrypt.hash(obj.password)

    user_data = obj.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)

    return User.model_validate(user_db)


async def authenticate(db: Session, *, email: str, password: str) -> dict[str, Any]:
    user = await get_user_by_email(email=email, db=db)

    if not user or not user.verify_password(password=password):
        raise InvalidCredentials()

    return user
