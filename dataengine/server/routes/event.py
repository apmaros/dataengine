from flask import (
    render_template,
    Blueprint,
    session,
    request,
    flash,
    make_response,
    redirect,
    url_for
)

from common.util import utc_isoformat
from config import EVENT_INFLUX_BUCKET
from dataengine.common.log import logger
from dataengine.server.routes.annotations import requires_auth
from dataengine.service.event import get_events
from db.influxdb_client import build_influxdb_client
from model.event import Event

event_bp = Blueprint('event', __name__, url_prefix='/event')


@event_bp.route('/')
@requires_auth
def index():
    profile = session['profile']
    events = get_events(profile['user_id'])
    return render_template('event/index.html', user_profile=profile, events=events)


@event_bp.route('/', methods=['POST'])
@requires_auth
def new():
    time = request.form.get('time')
    event = Event(
        description=request.form['description'],
        activity=request.form['activity'],
        feel=int(request.form['feel']),
        time=time if time else utc_isoformat(),
        duration=request.form.get('duration'),
        user_id=session['profile']['user_id']
    )
    try:
        build_influxdb_client(EVENT_INFLUX_BUCKET).write_record(event.as_point())
    except RuntimeError as e:
        logger.error(f"Failed to write to database due to error {e}")
        flash('Failed to record event due to error', 'error')

    flash(f"👌 Event was recorded")

    return make_response(redirect(url_for('event.index')))
