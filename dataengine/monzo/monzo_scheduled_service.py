import datetime
from dataclasses import dataclass
from threading import Timer
from typing import Optional
from dataengine.db.influxdb_client import InfluxDbClient, build_influxdb_client
from common.log import logger
from dataengine.monzo.api_error import ApiError
from dataengine.monzo.monzo_client import MonzoClient
from dataengine.transaction.transaction_provider import transactions_to_records, build_transaction_with_merchant
from common.util import current_time_sec, _day_to_daytime_str, chunks
from monzo.monzo_token_provider import load_monzo_token
from influxdb_client import Point


class MonzoScheduledService(object):
    _DEFAULT_TXS_SINCE_DAYS_AGO = 30
    _TASK_DESCRIPTION = "Synchronise Monzo transactions"

    def __init__(
        self,
        monzo_client: MonzoClient,
        influxdb_client: InfluxDbClient,
        delay_sec: float
    ):
        self.monzo_client = monzo_client
        self.influxdb_client = influxdb_client
        self.delay_sec = delay_sec
        self.refresh_token_delay_sec = monzo_client.get_expiry_sec() / 2
        self.timer: Timer = None
        self.is_running = False

    def start(self):
        logger.info(f"scheduled: {self._TASK_DESCRIPTION}")
        self.schedule()
        self.is_running = True

    def stop(self):
        if not self.is_running:
            logger.info("Scheduler not running does, not need to stop")
            return

        self.timer.cancel()
        self.is_running = False

    def schedule(self) -> None:
        self.timer = Timer(
            self.delay_sec,
            self._load_and_schedule
        )
        self.timer.start()

    def _load_and_schedule(self):
        if not self.is_running:
            logger.warn("Attempting to run task that was stopped, skipping")
            return

        logger.info(f"start: {self._TASK_DESCRIPTION}")
        try:
            self._sync_transactions()
        except ApiError as err:
            logger.error(f"Monzo API failed to load transactions due to {err}")
            if err.is_unauthorised():
                self.monzo_client.login(
                    load_monzo_token()
                )
        except Exception as err:
            logger.error(f"Failed to load transactions {err}")
        logger.info(f"finish: {self._TASK_DESCRIPTION}")
        self.schedule()

    def _sync_transactions(self):
        if not self.monzo_client.is_authenticated():
            logger.error("Monzo client not authenticated. Authenticate to load transactions")
            return

        logger.info(f"Token created at {self.monzo_client.token.created_at_sec}")

        if (
            self.monzo_client.token.created_at_sec + self.refresh_token_delay_sec
            <= current_time_sec()
        ):
            logger.info(f"Refreshing token - "
                        f"{self.monzo_client.token.created_at_sec + self.delay_sec} <= {current_time_sec()}")
            self.monzo_client.refresh_token()

        since = datetime.datetime.now() - datetime.timedelta(self._DEFAULT_TXS_SINCE_DAYS_AGO)
        try:
            txs = self.monzo_client.get_transactions(
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
            self.influxdb_client.write_record(tx_metric)

            for batch in batches:
                self.influxdb_client.write_records(points=batch)

            logger.info(f"Flashed {len(points)} transactions flushed to influxdb")
        except ApiError as e:
            logger.error(f"Failed to load transactions due to ApiError: {e}")
        except RuntimeError as e:
            logger.error(f"Failed to load transactions due to error: {e}")


@dataclass
class MonzoScheduledServiceInstance:
    instance: Optional[MonzoScheduledService]

    def is_initialized(self):
        return self.instance is not None


monzo_scheduled_service_instance: MonzoScheduledServiceInstance = MonzoScheduledServiceInstance(None)


def get_scheduled_monzo_service_instance(
    monzo_client: MonzoClient,
    delay_sec: int
):
    if monzo_scheduled_service_instance.is_initialized():
        return monzo_scheduled_service_instance.instance

    service = MonzoScheduledService(
        monzo_client=monzo_client,
        influxdb_client=build_influxdb_client(),
        delay_sec=delay_sec
    )

    monzo_scheduled_service_instance.instance = service

    return monzo_scheduled_service_instance.instance
