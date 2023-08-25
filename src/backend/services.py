import os
import sys
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from passlib import hash
from database import session_local
from sqlalchemy.orm import Session
from typing import List
from schema.schemas import (
    AccountCreate, Account, Token
)
from models import (
    Account as Account_Model
)
from config import settings
from jwt import encode, decode

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

async def authenticate_user(username: str, 
                            password: str, 
                            db: Session) -> Account_Model:
    user = await get_user_by_username(username=username, db=db)

    if not user or not user.verify_password(password=password):
        return False
    
    return user

async def get_current_user(token: str=Depends(oauth2_schema), 
                           db: Session=Depends(get_db)) -> Account:
    try:
        payload = decode(
            token, 
            settings.secret_key, 
            [settings.algorithm]
        )
    
        account = db.query(Account_Model).get(payload['id'])

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid Email or Password'
        )
    
    return Account.model_validate(account)

async def create_token(account: Account_Model) -> Token:
    account_obj = Account.model_validate(account)
    token = encode(account_obj.model_dump(), settings.secret_key)

    return Token(access_token=token)

async def get_user_by_username(username: str, db: Session) -> Account_Model:
    return db.query(Account_Model).filter(Account_Model.username == username).first()

async def add_account(account: AccountCreate, db: Session) -> Account_Model:
    account.password=hash.bcrypt.hash(account.password)
    acct_obj = Account_Model(**account.model_dump())
    
    db.add(acct_obj)
    db.commit()
    db.refresh(acct_obj)
    
    return Account.model_validate(acct_obj)

async def get_accounts(db:Session) -> List[Account]:
    acct = db.query(Account_Model).all()
    return list(map(Account.model_validate, acct))