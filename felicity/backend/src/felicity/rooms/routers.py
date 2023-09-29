from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session
from database.core import get_db

from users.jwt import parse_jwt_admin_data
from users.schemas import JWTData

from patients.services import get_user_by_id
from patients.exceptions import PatientNotFound

from rooms.services import (
    add,
    room_name,
    multi_room,
    get_room_by_id,
    add_patient_to_room,
)
from rooms.schemas import Room, RoomCreate
from rooms.exceptions import RoomExists, RoomNotFound

router = APIRouter(prefix="/room", tags=["Room"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_room(
    room_in: RoomCreate,
    db: Session = Depends(get_db),
    _: JWTData = Depends(parse_jwt_admin_data),
) -> Room:
    if await room_name(db=db, name=room_in.name):
        raise RoomExists()

    room = await add(db=db, room_in=room_in)

    return room


@router.get("/")
async def get_rooms(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return await multi_room(db=db, skip=skip, limit=limit)


@router.get("/{room_id}")
async def room_status(room_id: int, *, db: Session = Depends(get_db)):
    _room = await get_room_by_id(db=db, room_id=room_id)

    if not _room:
        raise RoomNotFound()

    return _room


@router.patch("/add/{room_id}")
async def patch_patient(
    room_id: int,
    patient_id: int,
    db: Session = Depends(get_db),
    _: JWTData = Depends(parse_jwt_admin_data),
):
    _patient = await get_user_by_id(db=db, patient_id=patient_id)
    _room = await get_room_by_id(db=db, room_id=room_id)

    if not _patient:
        raise PatientNotFound()

    if not _room:
        raise RoomNotFound()

    room_details = await add_patient_to_room(db=db, room=_room, patient=_patient)

    return room_details
