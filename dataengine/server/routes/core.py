from flask import (
    render_template,
    Blueprint,
    session,
    make_response,
    redirect,
    url_for
)

core_bp = Blueprint('core', __name__)


@core_bp.route('/')
def index():
    profile = session.get('profile', None)
    if profile:
        return make_response(redirect(url_for('user.home')))

    return render_template('index.html')


@core_bp.route('/about')
def about():
    return render_template('about.html')
