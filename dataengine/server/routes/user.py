from flask import (
    render_template,
    Blueprint,
    session,
)

from dataengine.config import DEFAULT_DISPLAY_RESOURCE_SHORT_DAYS_AGO
from dataengine.server.routes.annotations import requires_auth
from dataengine.service.db.event import get_events_since
from dataengine.service.db.note import get_notes_since
from dataengine.service.event import group_events_by_date

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/')
@requires_auth
def index():
    profile = session['profile']
    return render_template('user/index.html', user_profile=profile)


@user_bp.route('/home')
@requires_auth
def home():
    profile = session['profile']
    events = get_events_since(profile['user_id'], days_ago=DEFAULT_DISPLAY_RESOURCE_SHORT_DAYS_AGO)
    notes = get_notes_since(profile['user_id'], days_ago=DEFAULT_DISPLAY_RESOURCE_SHORT_DAYS_AGO)
    grouped_events = group_events_by_date(events).values()
    return render_template(
        'user/index.html',
        user_profile=profile,
        grouped_events=grouped_events,
        notes=notes
    )
