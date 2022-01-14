from flask import (
    render_template,
    Blueprint,
    session,
)

from dataengine.server.routes.annotations import requires_auth

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@requires_auth
def index():
    profile = session['profile']
    return render_template('admin/index.html', user_profile=profile)
