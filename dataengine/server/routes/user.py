from flask import (
    render_template,
    Blueprint,
    session,
)

from dataengine.server.routes.annotations import requires_auth

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/')
@requires_auth
def index():
    profile = session['profile']
    return render_template('user/index.html', user_profile=profile)
