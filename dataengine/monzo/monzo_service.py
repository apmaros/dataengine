import datetime

from influxdb_client import Point

from dataengine.common.log import logger
from dataengine.common.util import current_time_sec, _day_to_daytime_str
from dataengine.monzo.model.api_error import ApiError
from dataengine.monzo.monzo_client import MonzoClient
from dataengine.monzo.monzo_token_provider import store_monzo_token, load_monzo_token
from dataengine.monzo.transaction_mapper import to_points


class MonzoService:
    _DEFAULT_TXS_SINCE_DAYS_AGO = 30

    def __init__(self, monzo_client: MonzoClient, influxdb_client):
        if not monzo_client.is_authenticated():
            raise ValueError("MonzoClient is not authenticated")
        self._monzo_client = monzo_client
        self._influxdb_client = influxdb_client

    def sync_transactions(self, sync_since=_DEFAULT_TXS_SINCE_DAYS_AGO):
        if self._monzo_client.should_refresh_token(current_time_sec()):
            logger.info(f"Refreshing token")
            store_monzo_token(self._monzo_client.refresh_token())

        since = datetime.datetime.now() - datetime.timedelta(sync_since)
        try:
            transactions = self._monzo_client.get_transactions(
                since_date=_day_to_daytime_str(since),
                before_date=None,
            )

            # todo extract
            tx_metric = (Point(f"transaction-count")
                         .tag(f"period", self._DEFAULT_TXS_SINCE_DAYS_AGO)
                         .field("count", len(transactions)))

            self._influxdb_client.write_record(tx_metric)
            self._influxdb_client.write_records(points=to_points(transactions))

            logger.info(f"Flashed {len(transactions)} transactions flushed to influxdb")
            return True

        # TODO Should not swallow exception
        except ApiError as e:
            logger.error(f"Failed to load transactions due to ApiError: {e}")
            # reload token - might have been evicted by rotation
            if e.is_unauthorised():
                self._monzo_client.login(load_monzo_token())
            return False
        except RuntimeError as e:
            logger.error(f"Failed to load transactions due to error: {e}")
            return False
