import uuid
import typing as t

from dataengine.server.RequestError import RequestError, ErrorType


def validate_id(target_id: t.Optional[str], id_name: str):
    if target_id is None:
        raise RequestError(
            ErrorType.VALIDATION,
            f"'{id_name}' must be present"
        )

    try:
        uuid.UUID(target_id)
    except ValueError:
        raise RequestError(
            ErrorType.VALIDATION,
            f"'{id_name}' is not a valid id"
        )
