from freezegun import freeze_time

from dataengine import format_timeline_datetime, format_relative_time_days
from factory.util import to_datetime


def test_format_timeline_datetime_formats_datetime():
    assert format_timeline_datetime(to_datetime("2022-02-17 08:50:00").date()) == "Thu, 17-02-2022"


def test_format_timeline_datetime_when_none_value_does_not_format_datetime():
    assert format_timeline_datetime(None) == "Not Scheduled"


@freeze_time("2022-02-02")
def test_format_relative_time_days_when_1_day_ago():
    assert format_relative_time_days(to_datetime('2022-02-01  08:50:00').date()) == '1 day ago'


@freeze_time("2022-02-02")
def test_format_relative_time_days_when_few_days_ago():
    assert format_relative_time_days(to_datetime('2022-01-28  08:50:00').date()) == '5 days ago'


@freeze_time("2022-02-01")
def test_format_relative_time_days_when_in_few_days():
    assert format_relative_time_days(to_datetime('2022-02-06  08:50:00').date()) == 'in 5 days'


@freeze_time("2022-02-01")
def test_format_relative_time_days_when_today():
    assert format_relative_time_days(to_datetime('2022-02-01  08:50:00').date()) == 'today'
