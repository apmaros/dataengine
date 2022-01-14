import base64
from io import BytesIO

import matplotlib.pyplot as plt
from flask import (
    request,
    Blueprint,
    flash,
    make_response,
    url_for,
    redirect,
    session,
    render_template
)
from influxdb_client import Point

from dataengine.common.log import logger
from dataengine.db.influxdb_client import build_influxdb_client
from dataengine.server.routes.annotations import requires_auth
from service.physio import get_heart_pressure_reading_df

physio_bp = Blueprint('physio', __name__, url_prefix='/physio')


@physio_bp.route('/')
@requires_auth
def index():
    profile = session['profile']

    fig = plt.figure()
    ax = fig.add_subplot(111)

    df = get_heart_pressure_reading_df(profile['user_id'], start='-180d')
    # heart_pressure_reading_df.plot(ax=ax, x='_field', y='_value')

    for name in ['systolic', 'diastolic']:
        ax.plot(df[df._field == name]._time, df[df._field == name]._value, label=name)

    ax.set_xlabel("time")
    ax.set_ylabel("value")
    ax.legend(loc='best')

    # old below
    buf = BytesIO()
    fig.savefig(buf, format="png")

    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    fig, ax = plt.subplots()

    return render_template('physio/index.html', user_profile=profile, data=data)


@physio_bp.route('/blood_pressure', methods=['POST'])
@requires_auth
def blood_pressure():
    systolic = int(request.form.get("systolic"))
    diastolic = int(request.form.get("diastolic"))
    heart_rate = int(request.form.get("heart-rate"))
    last_activity = request.form.get("last-activity")
    user_id = session['profile']['user_id']

    point = (Point('blood-pressure-reading')
             .tag('last_activity', last_activity)
             .tag('user_id', user_id)
             .field('systolic', systolic)
             .field('diastolic', diastolic)
             .field('heart_rate', heart_rate))

    try:
        build_influxdb_client("physio").write_record(point)
    except RuntimeError as e:
        logger.error(f"Failed to write to influxdb due to {e}")
        flash('Failed to write reading to database')

    flash("Recorded blood pressure reading ("f"blood pressure: {systolic}/{diastolic}, heart rate: {heart_rate})",
          'success')

    return make_response(redirect(url_for('core.index')))
