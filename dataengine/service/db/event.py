import typing

from sqlalchemy import select

from dataengine import Context
from dataengine.common.log import logger
from dataengine.common.util import days_ago_datetime
from dataengine.config import EVENT_INFLUX_BUCKET
from dataengine.db.influxdb_client import build_influxdb_client
from dataengine.model.dao.event import Event
from dataengine.service.model.event_record import EventRecord


def get_events_since(user_id, days_ago) -> typing.List[Event]:
    statement = (select(Event)
                 .filter(Event.user_id == user_id)
                 .filter(Event.time > days_ago_datetime(days_ago)))

    return Context.db_session().execute(statement)


def flux_record_to_event_record(record) -> EventRecord:
    v = record.values

    return EventRecord(
        start=v['_start'],
        stop=v['_stop'],
        time=v['_time'],
        description=v['_value'],
        activity=v['activity'],
        duration=v['duration'],
        feel=v['feel'],
        user_id=v.get('user_id')
    )


def get_events(user_id, start=None, stop=None):
    if not start:
        start = "-30d"
    if not stop:
        stop = "now()"
    q = f"""
        from(bucket: "{EVENT_INFLUX_BUCKET}")
          |> range(start: {start}, stop: {stop})
          |> filter(fn: (r) => r._measurement == "events")
          |> filter(fn: (r) => r._field == "description")
          |> filter(fn: (r) => r["user_id"] == "{user_id}")
          |> group()
          |> sort(columns: ["_time"], desc: true)
    """

    try:
        result = build_influxdb_client().query(q)
        if result:
            return list(map(
                flux_record_to_event_record,
                result[0].records
            ))
        else:
            return []

    except RuntimeError as e:
        logger.error(f"Failed to db due to error {e}")
