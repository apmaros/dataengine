from dataengine.config import DATETIME_VIEW_FORMAT


def format_datetime(value):
    if value is None:
        return ""
    return value.strftime(DATETIME_VIEW_FORMAT)


def split_paragraphs(text):
    return text.split('\n')
