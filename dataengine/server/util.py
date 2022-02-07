from dataengine.config import DATETIME_VIEW_FORMAT, DATETIME_LABEL_FORMAT


def format_label_datetime(value):
    return format_datetime(value, DATETIME_LABEL_FORMAT)


def format_datetime(value, fmt=DATETIME_VIEW_FORMAT):
    if value is None:
        return ""
    return value.strftime(fmt)


def split_paragraphs(text):
    return text.split('\n')


def or_zero(value):
    if value:
        return value
    else:
        return 'null'
