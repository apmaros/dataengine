from datetime import datetime

from dataengine.config import DATETIME_VIEW_FORMAT, DATETIME_LABEL_FORMAT, EVENT_NO_TIME_LABEL, DATETIME_LABEL_WITH_DOW


def format_label_datetime(value):
    return format_datetime(value, DATETIME_LABEL_FORMAT)


def format_datetime(value, fmt=DATETIME_VIEW_FORMAT):
    if value is None:
        return ""
    return value.strftime(fmt)


def format_timeline_datetime(value):
    if value is None:
        return EVENT_NO_TIME_LABEL

    return value.strftime(DATETIME_LABEL_WITH_DOW)


def format_relative_time_days(value):
    if value is None:
        return ""

    today = datetime.now().date()
    delta = (today - value.date()).days
    if abs(delta) == 1:
        formatted_days = 'day'
    else:
        formatted_days = 'days'

    if delta < 0:
        formatted = f"in {abs(delta)} {formatted_days}"
    elif delta > 0:
        formatted = f"{abs(delta)} {formatted_days} ago"
    else:
        formatted = "today"

    return formatted


def split_paragraphs(text):
    return text.split('\n')
