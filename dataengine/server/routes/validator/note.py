from dataengine.server.RequestError import RequestError
from dataengine.server.routes.validator.common import (
    validate_float_field,
    is_present
)


def validate_note(form):
    if not is_present(form, 'body'):
        RequestError.make_field_missing_validation_error('body')

    if is_present(form, 'geo-lat'):
        validate_float_field(form.get('geo-lat'), 'geo-lat')

    if is_present(form, 'geo-lng'):
        validate_float_field(form.get('geo-lng'), 'geo-lng')
