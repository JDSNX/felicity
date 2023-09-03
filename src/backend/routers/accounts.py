from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from services import (
    get_user_by_username,
    add_account as _add_account,
    get_accounts as _get_accounts,
    create_token as _create_token,
    get_current_user as _get_current_user,
    update_account as _update_account,
    delete_account as _delete_account,
    get_id_by_username
)

from database.core import get_db

from schema.schemas import (
    Account, AccountCreate, Token, AccountUpdate
)

router = APIRouter(prefix="/accounts", tags=['Accounts'])

@router.post(
        "/", 
        status_code=status.HTTP_201_CREATED, 
        response_model=Token
)
async def create_account(
    account: AccountCreate,
    db: Session=Depends(get_db)
) -> Token:   
    db_user = await get_user_by_username(account.username, db)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Username: {account.username} is already registered."
        )

    _account = await _add_account(account=account, db=db)

    return await _create_token(account=_account)

@router.get(
        '/', 
        response_model=List[Account]
)
async def get_accounts(
    db: Session=Depends(get_db),
    acct: Account=Depends(_get_current_user)
) -> List[Account]:
    if acct is not None:
        return await _get_accounts(db=db)

@router.post(
        '/me', 
        status_code=status.HTTP_201_CREATED, 
        response_model=Account
    )
async def get_user(
    account: Account=Depends(_get_current_user)) -> Account:
    return account

@router.delete(
        '/{username}',
        status_code=status.HTTP_201_CREATED)
async def delete_account(
    username: str, 
    user: Account=Depends(_get_current_user),
    db: Session=Depends(get_db)
) -> dict():
    if user is not None:
        await _delete_account(username=username, db=db)

        return {
            "status": status.HTTP_200_OK,
            "message": f"Username: {username} - successfully deleted."
        }

@router.put(
        '/{username}', 
        status_code=status.HTTP_201_CREATED
)
async def update_account(
    username: str,
    account: AccountUpdate, 
    user: Account=Depends(_get_current_user),
    db: Session=Depends(get_db)
) -> dict():
    if user is not None:
        await _update_account(
            username=username, 
            account=account, 
            db=db
        )

        return {
            "status": status.HTTP_200_OK,
            "message": f"Username: {username} - successfully updated.",
            "data": account
        }
