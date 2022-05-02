import datetime
import time
import uuid
from datetime import datetime as datetime_fn, date, timedelta

import pytz


def str_to_float(s: str):
    return float(s.replace(' ', ''))


# example 2021-03-04T00:00:00Z
def day_to_daytime_str(date, is_end=False):
    time = "23:59:59Z" if is_end else "00:00:00Z"
    return datetime_fn(date.year, date.month, date.day) \
        .replace(tzinfo=pytz.UTC) \
        .strftime(f"%Y-%m-%dT{time}")


def random_str():
    return get_uuid()


def get_uuid():
    return str(uuid.uuid4())


def week_ago_date():
    return date.today() - timedelta(days=7)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def current_time_sec():
    return int(time.time())


def utc_isoformat(target_datetime=None):
    """
    Returns datetime formatted to ISO RFC-3339 (https://datatracker.ietf.org/doc/html/rfc3339),
    compatible with influxdb time datatype.

    If no datetime is provided, datetime `now` is used.
    @target_datetime: optional date time to be formatted
    :return: ISO formatted string representing target datetime
    """
    if not target_datetime:
        target_datetime = datetime.datetime.now()

    return target_datetime.isoformat()


def days_ago_datetime(since) -> datetime:
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=since)

    return now - delta
