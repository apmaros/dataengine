import unittest
from unittest.mock import patch

import pytest

from dataengine.monzo.monzo_client import MonzoClient
from factory.transaction_factory import make_raw_transaction


@pytest.fixture(autouse=True)
def mock_monzo_api_config():
    with patch(
        "dataengine.monzo.model.monzo_config.MonzoApiConfig",
        monzo_account_id='client-id'
    ) as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_monzo_token():
    with patch(
        "dataengine.monzo.model.monzo_token.MonzoToken",
        access_token="secret-key"
    ) as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_get_transactions():
    with patch('dataengine.monzo.monzo_client.get_transactions') as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_raw_transaction():
    return make_raw_transaction()


class TestMonzoClient:
    def test_get_transactions_returns_transactions(
        self,
        mock_monzo_api_config,
        mock_monzo_token,
        mock_get_transactions,
        mock_raw_transaction
    ):
        under_test = MonzoClient(mock_monzo_api_config, mock_monzo_token)
        mock_get_transactions.return_value = {'transactions': [mock_raw_transaction]}

        actual = under_test.get_transactions('123', '456')
        assert 1 == len(actual)
        assert mock_raw_transaction['id'] == actual[0].id
        mock_get_transactions.assert_called_with(
            since_date='123',
            before_date='456',
            account_id='client-id',
            token='secret-key'
        )


if __name__ == '__main__':
    unittest.main()
