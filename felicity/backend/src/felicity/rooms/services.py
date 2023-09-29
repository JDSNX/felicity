from sqlalchemy.orm import Session

from rooms.models import Room as Room_Model
from rooms.schemas import Room, RoomCreate

from patients.models import Patient as Patient_Model

from rooms.exceptions import RoomOccupied


async def get_user_by_id(db: Session, *, patient_id: int) -> Room_Model:
    return db.query(Room_Model).filter(Room_Model.id == patient_id).first()


async def room_name(db: Session, *, name: str):
    return db.query(Room_Model).filter(Room_Model.name == name).first()


async def multi_room(db: Session, skip: int, limit: int):
    return db.query(Room_Model).limit(limit).offset(skip).all()


async def get_room_by_id(db: Session, room_id: int):
    return db.query(Room_Model).filter(Room_Model.id == room_id).first()


async def add(db: Session, *, room_in: RoomCreate) -> Room_Model:
    room_obj = Room_Model(name=room_in.name)

    db.add(room_obj)
    db.commit()
    db.refresh(room_obj)

    return Room.model_validate(room_obj)


async def update_room_status(db: Session, *, room: Room_Model, status: bool):
    room.is_occupied = not room.is_occupied

    db.commit()
    db.refresh(room)

    return Room.model_validate(room)


async def add_patient_to_room(db: Session, *, room: Room_Model, patient: Patient_Model):
    if room.is_occupied:
        raise RoomOccupied()

    room.patients_id = patient.id

    await update_room_status(db=db, room=room, status=room.is_occupied)

    db.commit()
    db.refresh(room)

    return Room.model_validate(room)
