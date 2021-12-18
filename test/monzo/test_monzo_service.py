import unittest
from unittest.mock import patch

import pytest

from dataengine.monzo.monzo_service import MonzoService
from factory.transaction_factory import make_transaction


@pytest.fixture
def influxdb_client():
    with patch("dataengine.db.influxdb_client.InfluxDbClient") as mock:
        yield mock


@pytest.fixture
def monzo_client():
    with patch("dataengine.monzo.monzo_client.MonzoClient") as mock:
        mock.is_authenticated.return_value = True
        mock.should_refresh_token.return_value = False
        mock.get_transactions.return_value = [make_transaction()]

        yield mock


class TestMonzoService:
    def test_sync_transactions_synchronises_txs_with_db(self, monzo_client, influxdb_client):
        MonzoService(monzo_client, influxdb_client).sync_transactions()

        assert monzo_client.get_transactions.call_count == 1
        # write metric
        assert influxdb_client.write_record.call_count == 1
        # write transactions
        assert influxdb_client.write_records.call_count == 1


if __name__ == '__main__':
    unittest.main()
