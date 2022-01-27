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

from dataengine.common.log import logger
from dataengine.config import DEFAULT_DISPLAY_RESOURCE_DAYS_AGO
from dataengine.server.routes.annotations import requires_auth
from dataengine.service.db.event import get_events_since

event_bp = Blueprint('event', __name__, url_prefix='/event')


@event_bp.route('/')
@requires_auth
def index():
    profile = session['profile']
    events = get_events_since(profile['user_id'], DEFAULT_DISPLAY_RESOURCE_DAYS_AGO)
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
        build_influxdb_client(EVENT_INFLUX_BUCKET).write_record_sync(event.as_point())
    except RuntimeError as e:
        logger.error(f"Failed to write to database due to error {e}")
        flash('Failed to record event due to error', 'error')

    flash(f"👌 Event was recorded", 'success')

    return make_response(redirect(url_for('event.index')))
