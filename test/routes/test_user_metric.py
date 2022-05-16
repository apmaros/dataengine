from unittest.mock import patch

from werkzeug.datastructures import ImmutableMultiDict

from conftest import auth_session
from factory.dao_factory import make_user_metric


@patch('dataengine.server.routes.user_metric.get_user_metrics')
def test_index_displays_user_metrics(get_user_metrics_mock, client):
    user_id = auth_session(client)
    get_user_metrics_mock.return_value = [
        make_user_metric(),
        make_user_metric()
    ]

    assert client.get('/user/metric/').status_code == 200
    get_user_metrics_mock.assert_called_with(user_id)


@patch('dataengine.server.routes.user_metric.put_user_metric')
def test_new_stores_user_metric(put_user_metric, client):
    user_id = auth_session(client)
    user_metric_data = ImmutableMultiDict({'name': 'my user metric'})

    resp = client.post('/user/metric/', data=user_metric_data)

    assert resp.status_code == 302
    put_user_metric.assert_called_with(user_id, user_metric_data)
