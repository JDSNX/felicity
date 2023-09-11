from datetime import datetime
from typing import Any

from fastapi import Cookie, Depends

from .services import get_user_by_id
from .exceptions import EmailTaken, RefreshTokenNotValid
from .services import get_user_by_email
from .schemas import User


async def valid_user_create(user: User) -> User:
    if await get_user_by_email(user.email):
        raise EmailTaken()

    return user


# async def valid_refresh_token(
#     refresh_token: str = Cookie(..., alias="refreshToken"),
# ) -> dict[str, Any]:
#     db_refresh_token = await get_refresh_token(refresh_token)
#     if not db_refresh_token:
#         raise RefreshTokenNotValid()

#     if not _is_valid_refresh_token(db_refresh_token):
#         raise RefreshTokenNotValid()

#     return db_refresh_token


# async def valid_refresh_token_user(
#     refresh_token: dict[str, Any] = Depends(valid_refresh_token),
# ) -> dict[str, Any]:
#     user = await get_user_by_id(refresh_token["user_id"])
#     if not user:
#         raise RefreshTokenNotValid()

#     return user


# def _is_valid_refresh_token(db_refresh_token: dict[str, Any]) -> bool:
#     return datetime.utcnow() <= db_refresh_token["expires_at"]