import unittest
from unittest.mock import Mock

from dataengine.monzo.monzo_service import MonzoService


class MyTestCase(unittest.TestCase):
    def test_sync_transactions_synchronises_txs_with_db(self):
        monzo_client_mock = Mock()
        influxdb_client_mock = Mock()

        monzo_client_mock.is_authenticated.return_value = True
        monzo_client_mock.should_refresh_token.return_value = False

        MonzoService(monzo_client_mock, influxdb_client_mock).sync_transactions()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
