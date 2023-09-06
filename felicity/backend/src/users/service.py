from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib import hash
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from database.core import get_db
from config import settings
from jose import jwt

from .models import User as User_Model
from .schemas import User, UserCreate, UserUpdate

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


def get_user_by_email(email: str, db: Session) -> Optional[User_Model]:
    return db.query(User_Model).filter(User_Model.email == email).first()


def create(user: UserCreate, db: Session) -> User_Model:
    hashed_password = hash.bcrypt.hash(user.password)

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


def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
) -> User_Model:
    try:
        payload = jwt.decode(
            token=token, key=settings.secret_key, algorithms=[settings.algorithm]
        )
        user = db.query(User_Model).get(payload["id"])

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
        )

    return User.model_validate(user)


def _selector(id: int, db: Session) -> User_Model:
    user = db.query(User_Model).filter(User_Model.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exists."
        )

    return user


def get_users(db: Session) -> List[User]:
    user = db.query(User_Model).all()
    return list(map(User.model_validate, user))


def delete_user(email: str, db: Session) -> None:
    stud = _selector(email=email, db=db)
    db.delete(stud)
    db.commit()


def update_user(user_id: int, user: UserUpdate, db: Session) -> User_Model:
    user_db = _selector(id=user_id, db=db)
    user_db.hashed_password = hash.bcrypt.hash(user.password)

    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)

    return User.model_validate(user_db)
