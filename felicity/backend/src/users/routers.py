from typing import Any
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.core import get_db

from .schemas import UserCreate
from .services import (
    create,
    get_user_by_email,
    get_user_by_id,
    authenticate,
    update,
)
from .jwt import parse_jwt_user_data, create_access_token, parse_jwt_admin_data
from .schemas import User, JWTData, AccessTokenResponse, UserUpdate, UserUpdated
from .exceptions import EmailTaken, InvalidCredentials

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    user = await get_user_by_email(user_in.email, db)
    if user:
        raise EmailTaken()

    _user = await create(user=user_in, db=db)

    return _user


@router.get("/me", response_model=User)
async def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data), db: Session = Depends(get_db)
) -> None:
    user = await get_user_by_id(jwt_data.id, db)

    return user


@router.post("/token", response_model=AccessTokenResponse)
async def auth_user(
    auth_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> AccessTokenResponse:
    user = await authenticate(
        email=auth_data.username, password=auth_data.password, db=db
    )

    if not user:
        raise InvalidCredentials()

    return AccessTokenResponse(access_token=create_access_token(user=user))


@router.put("/{user_id}", response_model=UserUpdated)
async def update_user(
    user_id: int,
    user_obj: UserUpdate,
    jwt_data: JWTData = Depends(parse_jwt_admin_data),
    db: Session = Depends(get_db),
) -> dict():
    user = await get_user_by_id(user_id=user_id, db=db)
    if user:
        await update(user_db=user, obj=user_obj, db=db)

    return UserUpdated(id=user.id, email=user.email, last_updated=user.updated_at)
