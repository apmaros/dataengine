import typing as t

from dataengine.server.RequestError import RequestError, ErrorType


def validate_user_metric_form(form: t.Dict):
    if 'name' not in form:
        raise RequestError(
            ErrorType.VALIDATION,
            "'name' must be present"
        )
