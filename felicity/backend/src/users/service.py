from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib import hash
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session

from database.core import get_db
from config import settings
from jose import jwt

from .models import User as User_Model
from .schemas import User, UserCreate, UserUpdate

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


def get_user_by_email(email: str, db: Session) -> User_Model:
    return db.query(User_Model).filter(User_Model.email == email).first()


def add_account(user: UserCreate, db: Session) -> User_Model:
    user.password = hash.bcrypt.hash(user.password)
    user_obj = User_Model(**user.model_dump())

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    return User.model_validate(user_obj)


def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, [settings.algorithm])

        account = db.query(User_Model).get(payload["id"])

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email or Password"
        )

    return User.model_validate(account)


def _selector(email: str, db: Session) -> User_Model:
    acct = db.query(User_Model).filter(User_Model.email == email).first()

    if acct is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exists."
        )

    return acct


def get_accounts(db: Session) -> List[User]:
    acct = db.query(User_Model).all()
    return list(map(User.model_validate, acct))


def delete_user(email: str, db: Session) -> None:
    stud = _selector(email=email, db=db)
    db.delete(stud)
    db.commit()


def update_user(email: str, user: UserUpdate, db: Session) -> User:
    user_db = _selector(email=email, db=db)

    user_db.id = User_Model.id
    user_db.email = user.email
    user_db.full_name = user.full_name
    user_db.is_active = user.is_active
    user_db.hashed_password = hash.bcrypt.hash(user.password)
    user_db.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(user_db)

    return User.model_validate(user_db)
