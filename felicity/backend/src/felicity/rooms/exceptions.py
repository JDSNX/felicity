from .constants import ErrorCode
from exceptions import BadRequest, NotFound


class RoomExists(BadRequest):
    DETAIL = ErrorCode.ROOM_EXISTS


class RoomNotFound(NotFound):
    DETAIL = ErrorCode.NO_ROOM


class RoomOccupied(BadRequest):
    DETAIL = ErrorCode.ROOM_OCCUPIED
