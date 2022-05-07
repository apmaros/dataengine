import re
from unittest.mock import patch

from werkzeug.datastructures import ImmutableMultiDict

from conftest import auth_session
from dataengine.common.util import random_str
from factory.dao_factory import make_user_metric, make_metric


@patch('dataengine.server.routes.metric.get_user_metric')
@patch('dataengine.server.routes.metric.get_metrics_by_user_metric_id_since')
def test_index_fetches_metrics_for_user(
        mock_get_metrics_by_user_metric_id_since,
        mock_get_user_metric,
        client,
):
    user_metric = make_user_metric()
    mock_get_user_metric.return_value = user_metric
    mock_get_metrics_by_user_metric_id_since.return_value = [
        make_metric(user_metric_id=user_metric.id),
        make_metric(user_metric_id=user_metric.id)
    ]
    auth_session(client, user_metric.user_id)
    resp = client.get(f'/metric/{user_metric.id}')

    assert resp.status_code == 200

    mock_get_user_metric.assert_called_with(user_metric.id)
    mock_get_metrics_by_user_metric_id_since.assert_called_with(
        user_metric.user_id,
        user_metric.id,
        30
    )


@patch('dataengine.server.routes.metric.get_user_metric')
def test_index_fails_when_user_metric_does_not_belong_to_user(
        mock_get_user_metric,
        client,
):
    user_metric = make_user_metric()
    mock_get_user_metric.return_value = user_metric
    auth_session(client)

    resp = client.get(f'/metric/{user_metric.id}')

    assert re.search(
        'Failed to get metrics due to error',
        resp.get_data(as_text=True)
    )

    assert resp.status_code == 200


@patch('dataengine.server.routes.metric.put_metric')
def test_new_stores_new_metric(
        put_metric_mock,
        client
):
    user_id = random_str()
    metric_data = ImmutableMultiDict({'value': '3', 'event': 'some-event'})

    auth_session(client, user_id)
    resp = client.post(f'/metric/', data=metric_data)

    assert resp.status_code == 302
    put_metric_mock.assert_called_with(user_id, metric_data)
