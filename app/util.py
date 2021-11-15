import time
import uuid
from datetime import datetime, date, timedelta
import pytz


def str_to_float(s: str):
    return float(s.replace(' ', ''))


# example 2021-03-04T00:00:00Z
def _day_to_daytime_str(date, is_end=False):
    time = "23:59:59Z" if is_end else "00:00:00Z"
    return datetime(date.year, date.month, date.day)\
        .replace(tzinfo=pytz.UTC)\
        .strftime(f"%Y-%m-%dT{time}")


def random_str():
    return str(uuid.uuid4())


def _last_week_date():
    return date.today() - timedelta(days=7)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def current_time_sec():
    return int(time.time())
