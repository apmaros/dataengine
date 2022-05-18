from dataengine.server.RequestError import RequestError
from dataengine.server.routes.validator.common import validate_float_field


def validate_note(form):
    if 'body' not in form:
        RequestError.make_field_missing_validation_error('body')

    if 'geo-lat' in form:
        validate_float_field(form.get('geo-lat'), 'geo-lat')

    if 'geo-lng' in form:
        validate_float_field(form.get('geo-lng'), 'geo-lng')
