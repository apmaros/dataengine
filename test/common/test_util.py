import datetime

from dataengine.common.util import utc_isoformat


def test_utcnow_isoformat_formats_time_to_rfc339_string():
    test_datetime = datetime.datetime(2020, 5, 17, 15, 21, 1)

    assert utc_isoformat(test_datetime) == "2020-05-17T15:21:01"
