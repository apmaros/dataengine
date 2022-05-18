from enum import Enum


class ErrorType(Enum):
    UNAUTHORISED = 'Unauthorised'
    VALIDATION = 'Validation'


class RequestError(Exception):
    def __init__(self, error_type, message: str):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)

    @staticmethod
    def make_field_missing_validation_error(field):
        raise RequestError(
            ErrorType.VALIDATION,
            f"'{field}' must be present"
        )
