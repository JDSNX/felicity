from typing import Any
from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session
from database.core import get_db

from .services import add, multi_patient, patient, get_user_by_id, update
from .schemas import Patient, PatientCreate, PatientUpdateIn
from .exceptions import PatientNotFound

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Patient)
async def add_patient(
    patient_in: PatientCreate, db: Session = Depends(get_db)
) -> Patient:
    patient = await add(patient_in, db)

    return patient


@router.get("/")
async def get_multi_patient(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    return await multi_patient(db=db, skip=skip, limit=limit)


@router.get("/{patient_id}")
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    _patient = await patient(db=db, patient_id=patient_id)

    if not _patient:
        raise PatientNotFound()

    return _patient


@router.put("/{patient_id}")
async def update_patient(
    patient_id: int, patient_obj: PatientUpdateIn, db: Session = Depends(get_db)
):
    patient = await get_user_by_id(db=db, patient_id=patient_id)

    if not patient:
        raise PatientNotFound()

    _patient = await update(patient_in=patient, obj=patient_obj, db=db)

    return _patient
