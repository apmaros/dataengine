from flask import (
    request,
    make_response,
    redirect,
    render_template,
    flash,
    url_for,
    Blueprint,
    session
)
from influxdb_client import Point

from dataengine.db.influxdb_client import build_influxdb_client
from dataengine.server.routes.annotations import requires_auth

core_bp = Blueprint('core', __name__)


@core_bp.route('/')
@core_bp.route('/index')
@requires_auth
def index():
    return render_template('home.html', user_profile=session['profile'])


@core_bp.route('/blood_pressure')
@requires_auth
def blood_pressure():
    systolic = int(request.args.get("systolic"))
    diastolic = int(request.args.get("diastolic"))
    heart_rate = int(request.args.get("heart-rate"))
    last_activity = request.args.get("last-activity")

    flash("Recorded blood pressure reading ("
          f"blood pressure: {systolic}/{diastolic}, heart rate: {heart_rate})")

    db = build_influxdb_client("physio")

    point = (Point('blood-pressure-reading')
             .tag('last_activity', last_activity)
             .field('systolic', systolic)
             .field('diastolic', diastolic)
             .field('heart_rate', heart_rate))

    db.write_record(point)

    return make_response(redirect(url_for('core.index')))
