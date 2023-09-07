from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.core import get_db

from .schemas import Token
from .service import authenticate_user, create_token

from src.exceptions import NotAuthenticated

router = APIRouter(prefix="/token", tags=["Authentication"])


@router.post("/", response_model=Token)
async def generate_token(
    creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(email=creds.username, password=creds.password, db=db)

    if not user:
        raise NotAuthenticated()

    return create_token(user=user)
