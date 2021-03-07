import uuid
from datetime import datetime
import pytz


def str_to_float(s: str):
    return float(s.replace(' ', ''))


# 2021-03-04T00:00:00Z
def _day_to_daytime_str(date, is_end=False):
    time = "23:59:59Z" if is_end else "00:00:00Z"
    return datetime(date.year, date.month, date.day)\
        .replace(tzinfo=pytz.UTC)\
        .strftime(f"%Y-%m-%dT{time}")


def random_str():
    return str(uuid.uuid4())
