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

from common.log import logger
from db.influxdb_client import build_influxdb_client
from server.routes.annotations import requires_auth

physio_bp = Blueprint('physio', __name__, url_prefix='/physio')


@physio_bp.route('/')
@requires_auth
def index():
    return render_template('physio.html', user_profile=session['profile'])


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

    return _get_response(request)


def _get_response(req):
    if req.referrer.split('/')[-2] == 'physio':
        return make_response(redirect(url_for('physio.index')))
    else:
        return make_response(redirect(url_for('core.index')))
