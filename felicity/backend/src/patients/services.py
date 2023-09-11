from datetime import datetime, timedelta
from typing import Any
from fastapi.encoders import jsonable_encoder
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from .models import Patient as Patient_Model
from .schemas import Patient, PatientCreate, PatientUpdate


async def get_user_by_id(patient_id: int, db: Session) -> Patient_Model:
    return db.query(Patient_Model).filter(Patient_Model.id == patient_id).first()


async def add(db: Session, patient: PatientCreate) -> Patient_Model:
    patient_obj = Patient_Model(
        full_name=patient.full_name,
        date_of_birth=patient.date_of_birth,
        contact_person=patient.contact_person,
        contact_number=patient.contact_number,
        email=patient.email,
    )

    db.add(patient_obj)
    db.commit()
    db.refresh(patient_obj)

    return Patient.model_validate(patient_obj)


async def multi_patient(db: Session, skip: int, limit: int):
    return db.query(Patient_Model).limit(limit).offset(skip).all()


async def patient(db: Session, patient_id: int):
    return db.query(Patient_Model).filter(Patient_Model.id == patient_id).first()


async def update(patient_in: Patient_Model, obj: PatientUpdate, db: Session):
    patient_in.updated_at = datetime.now()

    patient_data = obj.model_dump(exclude_unset=True)
    for key, value in patient_data.items():
        setattr(patient_in, key, value)

    db.commit()
    db.refresh(patient_in)

    return Patient.model_validate(patient_in)
