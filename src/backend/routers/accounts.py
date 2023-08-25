from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from services import (
    get_db, get_user_by_username,
    add_account as _add_account,
    get_accounts as _get_accounts,
    create_token as _create_token,
    get_current_user as _get_current_user
)

from schema.schemas import (
    Account, AccountCreate, Token
)

router = APIRouter(prefix="/accounts", tags=['Accounts'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_account(account: AccountCreate,
                         db: Session=Depends(get_db)) -> Token:   
    db_user = await get_user_by_username(account.username, db)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Username: {account.username} is already registered."
        )

    _account = await _add_account(account=account, db=db)

    return await _create_token(account=_account)

@router.get('/', response_model=List[Account])
async def get_accounts(db: Session=Depends(get_db),
                       acct: Account=Depends(_get_current_user)) -> List[Account]:
    return await _get_accounts(db=db)

@router.post('/me', status_code=status.HTTP_201_CREATED, response_model=Account)
async def get_user(account: Account=Depends(_get_current_user)) -> Account:
    return account