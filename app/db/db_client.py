import os
import typing as t
from influxdb_client import InfluxDBClient, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from pandas import DataFrame


class DbClient(object):
    def __init__(self, token: str, org: str, bucket: str, url: str):
        self.token = token
        self.org = org
        self.bucket = bucket
        self._inner: InfluxDBClient = InfluxDBClient(url=url, token=token, org=org, debug=True)
        self.write_client = self._inner.write_api(write_options=SYNCHRONOUS)
        self.read_client = self._inner.query_api()

    def write_dataframe(
        self,
        df: DataFrame,
        tag_columns: t.List[str],
        measurement_name: str
    ):
        self.write_client.write(
            bucket=self.bucket,
            record=df,
            data_frame_tag_columns=tag_columns,
            data_frame_measurement_name=measurement_name
        )

    def query(self, query: str):
        return self.read_client.query_data_frame(query)


def build_db_client() -> DbClient:
    return DbClient(
        token=os.environ.get('INFLUXDB_TOKEN'),
        org=os.environ.get('INFLUXDB_ORG'),
        bucket=os.environ.get('INFLUXDB_BUCKET'),
        url=os.environ.get('INFLUXDB_URL')
    )
