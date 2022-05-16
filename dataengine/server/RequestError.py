from enum import Enum


class ErrorType(Enum):
    UNAUTHORISED = 'Unauthorised'
    VALIDATION = 'Validation'


class RequestError(Exception):
    def __init__(self, error_type, message: str):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)
