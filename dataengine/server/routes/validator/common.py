import uuid
import typing as t

from dataengine.server.RequestError import RequestError, ErrorType


def is_present(form, field) -> bool:
    return field in form and form[field]


def validate_id(target_id: t.Optional[str], id_name: str):
    if target_id is None:
        RequestError.make_field_missing_validation_error(id_name)

    try:
        uuid.UUID(target_id)
    except ValueError:
        raise RequestError(
            ErrorType.VALIDATION,
            f"'{id_name}' is not a valid id"
        )


def validate_float_field(value, field_name):
    if value is None:
        RequestError.make_field_missing_validation_error(field_name)

    try:
        float(value)
    except ValueError:
        raise RequestError(
            ErrorType.VALIDATION,
            f"{field_name} (value={value}) must be float"
        )
