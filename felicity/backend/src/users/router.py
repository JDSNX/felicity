from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.core import get_db

from .schemas import User, UserCreate, UserUpdate
from .service import (
    get_user_by_email,
    create,
    get_users as _get_users,
    get_current_user,
    delete_user as _delete_user,
    update_user as _update_user,
)

from auth.service import create_token
from auth.schemas import Token

router = APIRouter(prefix="/Users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_user(user_in: UserCreate, db: Session = Depends(get_db)) -> Token:
    user = get_user_by_email(user_in.email, db)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{user_in.email} is already registered.",
        )

    _user = create(user=user_in, db=db)

    return create_token(user=_user)


@router.get("/", response_model=List[User])
async def get_users(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> List[User]:
    if user:
        return _get_users(db=db)


@router.delete("/{user_id}", status_code=status.HTTP_201_CREATED)
async def delete_user(
    user_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict():
    if user is not None:
        _delete_user(user_id=user_id, db=db)

        return {
            "status": status.HTTP_200_OK,
            "message": f"ID: {user_id} - successfully deleted.",
        }


@router.put("/{user_id}", status_code=status.HTTP_201_CREATED)
async def update_user(
    user_id: int,
    user_obj: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict():
    if user is not None:
        _update_user(user_id=user_id, user=user_obj, db=db)

        return {
            "status": status.HTTP_200_OK,
            "message": f"ID: {id} - successfully updated.",
            "data": user_obj,
        }
