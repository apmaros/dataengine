import pytest

from dataengine.server.RequestError import RequestError, ErrorType
from dataengine.server.routes.validator.user_metric import (
    validate_user_metric_form
)


def test_validate_user_metric_does_not_raise_when_valid_form():
    form = {'name': 'some error name'}

    validate_user_metric_form(form)


def test_validate_user_metric_does_raises_when_name_missing():
    with pytest.raises(RequestError) as e:
        validate_user_metric_form({})
    assert e.value.error_type == ErrorType.VALIDATION
    assert e.value.message == "'name' must be present"




