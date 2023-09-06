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


def _selector(email: str, db: Session) -> User_Model:
    acct = db.query(User_Model).filter(User_Model.email == email).first()

    if acct is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exists."
        )

    return acct


def get_users(db: Session) -> List[User]:
    user = db.query(User_Model).all()
    return list(map(User.model_validate, user))


def delete_user(email: str, db: Session) -> None:
    stud = _selector(email=email, db=db)
    db.delete(stud)
    db.commit()


def update_user(email: str, user: UserUpdate, db: Session) -> User_Model:
    user_db = _selector(email=email, db=db)

    user_db.id = User_Model.id
    user_db.email = user.email
    user_db.full_name = user.full_name
    user_db.is_active = user.is_active
    user_db.hashed_password = hash.bcrypt.hash(user.password)
    user_db.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(user_db)

    return User_Model.model_validate(user_db)
