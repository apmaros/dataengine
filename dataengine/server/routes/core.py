from flask import (
    render_template,
    Blueprint,
    session,
    request,
    flash
)

from dataengine.common.log import logger
from dataengine.server.routes.annotations import requires_auth
from db.influxdb_client import build_influxdb_client
from model.event import Event

core_bp = Blueprint('core', __name__)


@core_bp.route('/')
@core_bp.route('/index')
@requires_auth
def index():
    return render_template('home.html', user_profile=session['profile'])


@core_bp.route('/event', methods=['POST'])
@requires_auth
def event():
    time = request.form.get('time')
    duration = request.form.get('duration')

    event_model = Event(
        description=request.form.get('description'),
        activity=request.form.get('activity'),
        time=time if time else utcnow_isoformat(),
        duration=duration
    )
    try:
        build_influxdb_client("event").write_record(event_model.as_point())
    except RuntimeError as e:
        logger.error(f"Failed to write to database due to error {e}")
        flash('Failed to record event due to error', 'error')

    flash(f"Recorded event")

    return render_template('home.html', user_profile=session['profile'])


@core_bp.route('/about')
def about():
    return render_template('about.html')
