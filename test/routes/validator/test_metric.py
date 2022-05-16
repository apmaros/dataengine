import pytest

from dataengine.server.RequestError import RequestError, ErrorType
from dataengine.server.routes.validator.metric import validate_metric


def test_validate_metric_does_not_raise_when_valid_form():
    form = {'event': 'some event', 'value': 'some values'}

    validate_metric(form)


def test_validate_metric_raise_when_event_is_missing():
    with pytest.raises(RequestError) as e:
        validate_metric({'value': 3})

    assert e.value.error_type == ErrorType.VALIDATION
    assert e.value.message == "'event' must be present"


def test_validate_metric_raise_when_value_is_missing():
    with pytest.raises(RequestError) as e:
        validate_metric({'event': 'some event'})

    assert e.value.error_type == ErrorType.VALIDATION
    assert e.value.message == "'value' must be present"
