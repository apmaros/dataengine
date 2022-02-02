from flask import (
    render_template,
    Blueprint,
    session,
)

from dataengine.config import DEFAULT_DISPLAY_RESOURCE_SHORT_DAYS_AGO
from dataengine.server.routes.annotations import requires_auth
from dataengine.service.db.event import get_events_since
from dataengine.service.db.note import get_notes_since

core_bp = Blueprint('core', __name__)


@core_bp.route('/')
@requires_auth
def index():
    profile = session['profile']
    events = get_events_since(profile['user_id'], days_ago=DEFAULT_DISPLAY_RESOURCE_SHORT_DAYS_AGO)
    notes = get_notes_since(profile['user_id'], days_ago=DEFAULT_DISPLAY_RESOURCE_SHORT_DAYS_AGO)
    return render_template('home.html', user_profile=profile, events=events, notes_with_sentiment=notes)


@core_bp.route('/about')
def about():
    return render_template('about.html')
