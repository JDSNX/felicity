import os
import sys
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from passlib import hash
from database import session_local
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from schema.schemas import (
    AccountCreate, Account, Token, AccountUpdate,
    PatientCreate, Patient,
)
from models import (
    Account as Account_Model,
    Patient as Patient_Model
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

async def get_id_by_username(username: str, db: Session) -> Account_Model:
    return db.query(Account_Model).filter(Account_Model.username == username).first().id

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

async def _account_selector(username: str, 
                    db: Session) -> Account_Model:
    acct = (
        db.query(Account_Model)
        .filter(Account_Model.username == username)
        .first()
    )

    if acct is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account does not exists."
        )
    
    return acct

async def _patient_selector(patient_id: int, 
                            db: Session) -> Patient_Model:
    acct = (
        db.query(Patient_Model)
        .filter(Patient_Model.id == patient_id)
        .first()
    )

    if acct is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient does not exists."
        )
    
    return acct

async def delete_account(username: str, 
                         db: Session) -> None:
    stud = await _account_selector(
        username=username,
        db=db
    )
    db.delete(stud)  
    db.commit()

async def update_account(username: str, 
                         account: AccountUpdate,
                         db: Session) -> Account:
    acc_db = await _account_selector(
        username=username,
        db=db
    )
    account.password=hash.bcrypt.hash(account.password)

    acc_db.id = Account_Model.id
    acc_db.password = account.password
    acc_db.first_name = account.last_name
    acc_db.middle_name = account.middle_name
    acc_db.last_name = account.last_name
    acc_db.contact_number = account.contact_number
    acc_db.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(acc_db)

    return Account.model_validate(acc_db)

async def add_patient(patient: PatientCreate, 
                      db: Session) -> Patient_Model:
    patient = Patient_Model(**patient.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    
    return Patient.model_validate(patient)

async def get_patients(db:Session) -> List[Patient]:
    patient = db.query(Patient_Model).all()
    return list(map(Patient.model_validate, patient))

async def get_patient(patient_id: int,
                      db: Session) -> Patient:
    return await _patient_selector(patient_id=patient_id, db=db)

async def delete_patient(patient_id: str, 
                         db: Session) -> None:
    patient = await _patient_selector(
        patient_id=patient_id,
        db=db
    )
    db.delete(patient)  
    db.commit()

async def update_patient(patient_id: int, 
                         patient: PatientCreate,
                         db: Session) -> Patient:
    patient_db = await _patient_selector(
        patient_id=patient_id,
        db=db
    )

    patient_db.room_no = patient.room_no
    patient_db.first_name = patient.last_name
    patient_db.middle_name = patient.middle_name
    patient_db.last_name = patient.last_name
    patient_db.contact_number = patient.contact_number
    patient_db.address = patient.address
    patient_db.place_of_birth = patient.place_of_birth
    patient_db.gender = patient.gender
    patient_db.contact_person = patient.contact_person
    patient_db.contact_number = patient.contact_number
    patient_db.date_of_birth = patient.date_of_birth
    db.commit()
    db.refresh(patient_db)

    return Patient.model_validate(patient_db)