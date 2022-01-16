import datetime
from dataclasses import dataclass

from dataengine.common.log import logger
from dataengine.config import EVENT_INFLUX_BUCKET
from db.influxdb_client import build_influxdb_client
from model.day_note import DAY_NOTE_MEASURE_NAME


@dataclass
class DayNoteRecord:
    time: datetime
    note: str
    sad: int
    energetic: int
    anxious: int
    creative: int
    user_id: str


def flux_record_to_day_note_record(record) -> DayNoteRecord:
    v = record.values

    return DayNoteRecord(
        time=v['_time'],
        note=v['_value'],
        sad=v['sad'],
        energetic=v['energetic'],
        anxious=v['anxious'],
        creative=v['creative'],
        user_id=v['user_id'],
    )


def get_day_notes(user_id, start=None, stop=None):
    if not start:
        start = "-30d"
    if not stop:
        stop = "now()"

    q = f"""
        from(bucket: "{EVENT_INFLUX_BUCKET}")
          |> range(start: {start}, stop: {stop})
          |> filter(fn: (r) => r._measurement == "{DAY_NOTE_MEASURE_NAME}")
          |> filter(fn: (r) => r._field == "note")
          |> filter(fn: (r) => r["user_id"] == "{user_id}")
          |> group()
          |> sort(columns: ["_time"], desc: true)
    """

    try:
        result = build_influxdb_client().query(q)
        if result:
            return list(map(
                flux_record_to_day_note_record,
                result[0].records
            ))
        else:
            return []

    except RuntimeError as e:
        logger.error(f"Failed to db due to error {e}")
