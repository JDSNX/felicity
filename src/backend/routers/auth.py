from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schema.schemas import Token

from services import (
    get_db, authenticate_user, create_token
)


router = APIRouter(prefix="/token", tags=['Authentication'])

@router.post("/", response_model=Token)
async def generate_token(creds: OAuth2PasswordRequestForm=Depends(), 
                         db: Session=Depends(get_db)) -> Token:
    
    account = await authenticate_user(creds.username, creds.password, db)

    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Credentials"
        )
    
    return await create_token(account=account)