import pytest

from dataengine.server.RequestError import RequestError, ErrorType
from dataengine.server.routes.validator.note import validate_note


def test_validate_note_does_not_raise_when_valid_form():
    form = {'body': 'some body'}
    validate_note(form)


def test_validate_note_raise_when_note_does_not_have_body():
    with pytest.raises(RequestError) as e:
        validate_note({})

    assert e.value.error_type == ErrorType.VALIDATION
    assert e.value.message == "'body' must be present"


def test_validate_note_raise_when_geo_lat_is_invalid():
    with pytest.raises(RequestError) as e:
        validate_note({'body': 'some body', 'geo-lat': 'invalid'})

    assert e.value.error_type == ErrorType.VALIDATION
    assert e.value.message == "geo-lat (value=invalid) must be float"


def test_validate_note_raise_when_geo_lng_is_invalid():
    with pytest.raises(RequestError) as e:
        validate_note({'body': 'some body', 'geo-lng': 'invalid'})

    assert e.value.error_type == ErrorType.VALIDATION
    assert e.value.message == "geo-lng (value=invalid) must be float"
