from flask import (
    request,
    Blueprint,
    flash,
    make_response,
    url_for,
    redirect
)
from influxdb_client import Point

from db.influxdb_client import build_influxdb_client
from server.routes.annotations import requires_auth

physio_bp = Blueprint('physio', __name__, url_prefix='/physio')


@physio_bp.route('/blood_pressure', methods=['POST'])
@requires_auth
def blood_pressure():
    systolic = int(request.form.get("systolic"))
    diastolic = int(request.form.get("diastolic"))
    heart_rate = int(request.form.get("heart-rate"))
    last_activity = request.form.get("last-activity")

    flash("Recorded blood pressure reading ("
          f"blood pressure: {systolic}/{diastolic}, heart rate: {heart_rate})")

    point = (Point('blood-pressure-reading')
             .tag('last_activity', last_activity)
             .field('systolic', systolic)
             .field('diastolic', diastolic)
             .field('heart_rate', heart_rate))

    build_influxdb_client("physio").write_record(point)

    return make_response(redirect(url_for('core.index')))
