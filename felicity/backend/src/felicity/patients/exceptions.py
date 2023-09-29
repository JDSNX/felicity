from .constants import ErrorCode
from exceptions import NotFound


class PatientNotFound(NotFound):
    DETAIL = ErrorCode.INVALID_PATIENT
