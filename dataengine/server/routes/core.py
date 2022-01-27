from flask import (
    render_template,
    Blueprint,
    session,
)

from dataengine.server.routes.annotations import requires_auth
from dataengine.service.day_note import get_day_notes
from dataengine.service.db.event import get_events

core_bp = Blueprint('core', __name__)


@core_bp.route('/')
@requires_auth
def index():
    profile = session['profile']
    events = get_events(profile['user_id'])
    day_notes = get_day_notes(profile['user_id'], start='-7d')
    return render_template('home.html', user_profile=profile, events=events, day_notes=day_notes)


@core_bp.route('/about')
def about():
    return render_template('about.html')
