from dataengine.server.RequestError import RequestError, ErrorType


def validate_metric(form):
    if 'event' not in form:
        raise RequestError(
            ErrorType.VALIDATION,
            "'event' must be present"
        )

    if 'value' not in form:
        raise RequestError(
            ErrorType.VALIDATION,
            "'value' must be present"
        )
