from sqlalchemy.orm import Session
from jose import jwt

from config import settings

from users.models import User as User_Model
from users.service import get_user_by_email
from users.schemas import User

from .schemas import Token


def authenticate_user(email: str, password: str, db: Session) -> User_Model:
    user = get_user_by_email(email=email, db=db)

    if not user or not user.verify_password(password=password):
        return False

    return user


def create_token(account: User_Model) -> Token:
    account_obj = User.model_validate(account)
    token = jwt.encode(account_obj.model_dump(), settings.secret_key)

    return Token(access_token=token)
