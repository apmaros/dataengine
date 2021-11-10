import os
import typing as t
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDbClient(object):
    def __init__(self, token: str, org: str, bucket: str, url: str):
        self.token = token
        self.org = org
        self.bucket = bucket
        self._inner: InfluxDBClient = InfluxDBClient(url=url, token=token, org=org, debug=True)
        self.write_client = self._inner.write_api(write_options=SYNCHRONOUS)
        self.read_client = self._inner.query_api()

    def write_records(self, points: t.List[Point]):
        for point in points:
            self.write_record(point=point)

    def write_record(self, point: Point):
        self.write_client.write(
            bucket=self.bucket,
            record=point,
        )

    def query(self, query: str):
        return self.read_client.query(query)


def build_db_client() -> InfluxDbClient:
    return InfluxDbClient(
        token=os.environ.get('INFLUXDB_TOKEN'),
        org=os.environ.get('INFLUXDB_ORG'),
        bucket=os.environ.get('INFLUXDB_BUCKET'),
        url=os.environ.get('INFLUXDB_URL')
    )
