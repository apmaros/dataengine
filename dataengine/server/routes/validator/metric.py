from dataengine.server.RequestError import RequestError, ErrorType


def validate_metric(form):
    if 'event' not in form:
        RequestError.make_field_missing_validation_error('event')

    if 'value' not in form:
        RequestError.make_field_missing_validation_error('value')
