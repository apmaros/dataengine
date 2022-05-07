import uuid

import pytest

from dataengine.server.RequestError import RequestError, ErrorType
from dataengine.server.routes.validator.common import validate_id


def test_id_does_not_raise_when_valid_id():
    validate_id(str(uuid.uuid4()), 'some-id')


def test_id_raises_when_id_missing():
    with pytest.raises(RequestError) as e:
        validate_id(None, 'some-id')

    assert e.value.error_type == ErrorType.VALIDATION
    assert e.value.message == "'some-id' must be present"


def test_id_raises_when_invalid_id():
    with pytest.raises(RequestError) as e:
        validate_id('invalid-id-type', 'some-id')

    assert e.value.error_type == ErrorType.VALIDATION
    assert e.value.message == "'some-id' is not a valid id"
