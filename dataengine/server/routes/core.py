from flask import (
    render_template,
    Blueprint,
    session,
)

from dataengine.server.routes.annotations import requires_auth
from service.event import get_events

core_bp = Blueprint('core', __name__)


@core_bp.route('/')
@requires_auth
def index():
    profile = session['profile']
    events = get_events(profile['user_id'])
    return render_template('home.html', user_profile=profile, events=events)


@core_bp.route('/about')
def about():
    return render_template('about.html')
