from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.core import get_db

from .schemas import Token
from .service import authenticate_user, create_token

router = APIRouter(prefix="/token", tags=["Authentisscation"])


@router.post("/", response_model=Token)
async def generate_token(
    creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    account = authenticate_user(creds.username, creds.password, db)

    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    return create_token(account=account)
