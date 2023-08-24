import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from passlib import hash
from database import session_local
from sqlalchemy.orm import Session
from typing import List
from schema.schemas import (
    AccountCreate, Account
)
from models import (
    Account as Account_Model
)
from config import logger

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

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