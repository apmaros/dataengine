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
from dataengine.service.db.event import get_events_since, put_event, get_event, update_event

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
    # todo: add validation
    profile = session['profile']
    try:
        put_event(profile['user_id'], request.form)
    except RuntimeError as e:
        logger.error(f"Failed to write to database due to error {e}")
        flash('Failed to record event due to error', 'error')

    flash(f"👌 Event was recorded", 'success')

    return make_response(redirect(url_for('event.index')))


@event_bp.route('/edit')
@requires_auth
def edit():
    event = get_event(request.args['id'])
    return make_response(render_template(
        'event/edit.html',
        event=event,
        referrer=request.referrer,
    ))


@event_bp.route('/edit', methods=['POST'])
@requires_auth
def edit_post():
    profile = session['profile']
    update_event(request.form, profile['user_id'])

    return make_response(redirect(url_for('event.index')))


@event_bp.route('/delete')
@requires_auth
def delete():
    pass
