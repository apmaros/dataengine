from dataengine.common.log import logger
from dataengine.config import EVENT_INFLUX_BUCKET
from dataengine.db.influxdb_client import build_influxdb_client
from dataengine.service.model.event_record import EventRecord


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


if __name__ == '__main__':
    a = get_events(None)
    print(a)