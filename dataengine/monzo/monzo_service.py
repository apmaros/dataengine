import datetime

from influxdb_client import Point

from common.log import logger
from common.util import current_time_sec, _day_to_daytime_str, chunks
from monzo.model.api_error import ApiError
from monzo.monzo_client import MonzoClient
from monzo.monzo_token_provider import store_monzo_token, load_monzo_token
from transaction.transaction_provider import transactions_to_records, build_transaction_with_merchant


class MonzoService:
    _DEFAULT_TXS_SINCE_DAYS_AGO = 30

    def __init__(self, monzo_client: MonzoClient, influxdb_client):
        if not monzo_client.is_authenticated():
            raise ValueError("MonzoClient is not authenticated")
        self._monzo_client = monzo_client
        self._influxdb_client = influxdb_client

    def sync_transactions(self, sync_since=_DEFAULT_TXS_SINCE_DAYS_AGO):
        if self._should_refresh_token():
            logger.info(f"Refreshing token")
            store_monzo_token(self._monzo_client.refresh_token())

        since = datetime.datetime.now() - datetime.timedelta(sync_since)
        try:
            txs = self._monzo_client.get_transactions(
                since_date=_day_to_daytime_str(since),
                before_date=None,
            )
            points = transactions_to_records(list(map(
                lambda tx: build_transaction_with_merchant(tx),
                txs['transactions']
            )))
            batches = chunks(points, 500)

            tx_metric = (Point(f"transaction-count")
                         .tag(f"period", self._DEFAULT_TXS_SINCE_DAYS_AGO)
                         .field("count", len(points)))
            self._influxdb_client.write_record(tx_metric)

            for batch in batches:
                self._influxdb_client.write_records(points=batch)

            logger.info(f"Flashed {len(points)} transactions flushed to influxdb")
        except ApiError as e:
            logger.error(f"Failed to load transactions due to ApiError: {e}")
            logger.error(f"Monzo API failed to load transactions due to {e}")
            # reload token - might have been evicted by rotation
            if e.is_unauthorised():
                self._monzo_client.login(load_monzo_token())
        except RuntimeError as e:
            logger.error(f"Failed to load transactions due to error: {e}")

    def _should_refresh_token(self) -> bool:
        return self._monzo_client.token.created_at_sec + self._monzo_client.get_expiry_sec() / 2 <= current_time_sec()
