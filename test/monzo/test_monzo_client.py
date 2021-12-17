import unittest
from unittest.mock import patch

import pytest

from dataengine.monzo.monzo_client import MonzoClient
from factory.transaction_factory import make_raw_transaction


@pytest.fixture(autouse=True)
def mock_monzo_api_config():
    with patch("dataengine.monzo.model.monzo_config.MonzoApiConfig") as mock:
        mock.monzo_account_id.return_value = 'client-id'
        yield mock


@pytest.fixture(autouse=True)
def mock_monzo_token():
    with patch("dataengine.monzo.model.monzo_token.MonzoToken") as mock:
        mock.access_token_value.return_value = "secrect-key"
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
        mock_get_transactions.return_value = [mock_raw_transaction]

        actual = under_test.get_transactions('123', '456')
        assert 1 == len(actual)
        assert mock_raw_transaction['id'] == 'actual[0].id'


if __name__ == '__main__':
    unittest.main()
