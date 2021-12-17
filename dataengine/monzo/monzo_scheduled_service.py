from dataclasses import dataclass
from threading import Timer
from typing import Optional

from common.log import logger
from dataengine.db.influxdb_client import build_influxdb_client
from dataengine.monzo.monzo_client import MonzoClient
from monzo.monzo_service import MonzoService


class MonzoScheduledService(object):
    _DEFAULT_TXS_SINCE_DAYS_AGO = 30
    _TASK_DESCRIPTION = "Synchronise Monzo transactions"

    def __init__(
        self,
        monzo_service: MonzoService,
        delay_sec: int,
    ):
        self.monzo_service: MonzoService = monzo_service
        self.timer: Timer = None
        self.is_running = False
        self.delay_sec = delay_sec

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
            self._sync_and_schedule
        )
        self.timer.start()

    def _sync_and_schedule(self):
        if not self.is_running:
            logger.warn("Attempting to run task that was stopped, skipping")
            return

        logger.info(f"start: {self._TASK_DESCRIPTION}")
        try:
            self.monzo_service.sync_transactions()
        except RuntimeError as e:
            logger(f"Unexpected error in scheduled task: {e}")
        logger.info(f"finish: {self._TASK_DESCRIPTION}")
        self.schedule()


@dataclass
class MonzoScheduledServiceInstance:
    _instance: Optional[MonzoScheduledService]

    def is_initialized(self):
        return self._instance is not None


monzo_scheduled_service_instance: MonzoScheduledServiceInstance = MonzoScheduledServiceInstance(None)


def get_scheduled_monzo_service_instance(
    monzo_client: MonzoClient,
    delay_sec: int
):
    if monzo_scheduled_service_instance.is_initialized():
        return monzo_scheduled_service_instance.instance

    service = MonzoScheduledService(
        monzo_service=MonzoService(monzo_client, build_influxdb_client()),
        delay_sec=delay_sec
    )

    monzo_scheduled_service_instance.instance = service

    return monzo_scheduled_service_instance.instance
