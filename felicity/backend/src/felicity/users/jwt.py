from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config import settings

from users.schemas import JWTData
from users.exceptions import AuthorizationFailed, AuthRequired, InvalidToken
from users.models import User as User_Model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token", auto_error=False)


def create_access_token(
    *,
    user: User_Model,
    expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    jwt_data = {
        "sub": str(user.id),
        "exp": datetime.utcnow() + expires_delta,
        "is_admin": user.is_superuser,
    }

    return jwt.encode(jwt_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def parse_jwt_user_data_optional(
    token: str = Depends(oauth2_scheme),
):
    if not token:
        return None
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise InvalidToken()
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    return JWTData(**payload)


async def parse_jwt_user_data(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> JWTData:
    if not token:
        raise AuthRequired()
    return token


async def parse_jwt_admin_data(
    token: JWTData = Depends(parse_jwt_user_data),
) -> JWTData:
    if not token.is_admin:
        raise AuthorizationFailed()

    return token


async def validate_admin_access(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> None:
    if token and token.is_admin:
        return

    raise AuthorizationFailed()
