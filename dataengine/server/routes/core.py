from flask import (
    render_template,
    Blueprint,
    session
)

from dataengine.server.routes.annotations import requires_auth

core_bp = Blueprint('core', __name__)


@core_bp.route('/')
@core_bp.route('/index')
@requires_auth
def index():
    return render_template('home.html', user_profile=session['profile'])
