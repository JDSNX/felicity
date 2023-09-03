from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List
from services import (
    get_current_user as _get_current_user,
    add_patient as _add_patient,
    get_patients as _get_patients,
    get_patient as _get_patient,
    delete_patient as _delete_patient,
    update_patient as _update_patient
)

from database.core import get_db

from schema.schemas import (
    Patient, PatientCreate,
    Account
)

router = APIRouter(prefix="/patients", tags=['Patients'])

@router.post(
        "/", 
        status_code=status.HTTP_201_CREATED
)
async def add_patients(
    patient: PatientCreate,
    acct: Account=Depends(_get_current_user),
    db: Session=Depends(get_db)) -> Patient:
    
    return await _add_patient(patient=patient, db=db)

@router.get(
        '/', 
        response_model=List[Patient]
)
async def get_patients(
    db: Session=Depends(get_db),
    acct: Patient=Depends(_get_current_user)
) -> List[Patient]:
    if acct is not None:
        return await _get_patients(db=db)
    
@router.get(
        '/{patient_id}', 
        status_code=status.HTTP_201_CREATED)
async def get_patient(
    patient_id: int, 
    acct: Account=Depends(_get_current_user),
    db: Session=Depends(get_db)
) -> dict():
    if acct is not None:
        return await _get_patient(patient_id=patient_id, db=db)

@router.delete(
        '/{patient_id}',
        status_code=status.HTTP_201_CREATED
)
async def delete_patient(
    patient_id: int, 
    acct: Account=Depends(_get_current_user),
    db: Session=Depends(get_db)
) -> dict():
    if acct is not None:
        await _delete_patient(patient_id=patient_id, db=db)

        return {
            "status": status.HTTP_200_OK,
            "message": f"Patient ID: {patient_id} - successfully deleted."
        }

@router.put(
        '/{patient_id}', 
        status_code=status.HTTP_201_CREATED
)
async def update_account(
    patient_id: int,
                         patient: PatientCreate, 
                         user: Account=Depends(_get_current_user),
                         db: Session=Depends(get_db)) -> dict():
    if user is not None:
        await _update_patient(
            patient_id=patient_id, 
            patient=patient, 
            db=db
        )

        return {
            "status": status.HTTP_200_OK,
            "message": f"Patient ID: {patient_id} - successfully updated.",
            "data": patient
        }
