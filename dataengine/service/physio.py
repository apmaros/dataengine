from dataengine.common.log import logger
from dataengine.config import PHYSIO_INFLUX_BUCKET
from dataengine.db.influxdb_client import build_influxdb_client


def get_heart_pressure_reading_df(user_id: str, start: str = None, stop: str = None):
    if not start:
        start = "-30d"
    if not stop:
        stop = "now()"

    q = f"""
        from(bucket: "{PHYSIO_INFLUX_BUCKET}")
          |> range(start: {start}, stop: {stop})
          |> filter(fn: (r) => r["_measurement"] == "blood-pressure-reading")
          |> filter(fn: (r) => 
              r["_field"] == "diastolic" 
              or r["_field"] == "systolic"
              or r["_field"] == "heart_rate")
          |> group(columns: ["_field"])
          |> yield(name: "mean")
    """

    try:
        return build_influxdb_client().query_dataframe(q)
    except RuntimeError as e:
        logger.error(f"Failed fetch heart pressure reading due to error {e}")
