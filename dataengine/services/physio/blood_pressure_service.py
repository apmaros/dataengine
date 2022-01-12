from dataengine.db.influxdb_client import build_influxdb_client

BUCKET = 'physio'


def get_blood_pressure_for_last_3_months(user_id):
    q = f"""
        from(bucket: "{BUCKET}")
          |> range(start: -90d)
          |> filter(fn: (r) => r["_measurement"] == "blood-pressure-reading")
          |> filter(fn: (r) => r["user_id"] == "{user_id}")
          |> group(columns: ["_field"])
    """

    return build_influxdb_client().query_df(q)



if __name__ == '__main__':
    a = get_blood_pressure_for_last_3_months('google-oauth2|110459704254662008312')
    print(a)
