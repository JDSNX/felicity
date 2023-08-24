from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from services import (
    get_db, get_user_by_username,
    add_account as _add_account,
    get_accounts as _get_accounts,
)

from schema.schemas import (
    Account, AccountCreate
)

router = APIRouter(prefix="/accounts", tags=['Accounts'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Account)
async def add_account(account: AccountCreate, 
                      db: Session=Depends(get_db)) -> Account:   
    db_user = await get_user_by_username(account.username, db)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Account: {account.username} is already registered."
        )

    return await _add_account(account=account, db=db)


@router.get('/', response_model=List[Account])
async def get_accounts(db: Session=Depends(get_db)) -> List[Account]:    
    return await _get_accounts(db=db)