from flask import (
    render_template,
    Blueprint,
    session,
    request,
    flash
)
from influxdb_client import Point

from common.util import get_uuid
from dataengine.server.routes.annotations import requires_auth
from db.influxdb_client import build_influxdb_client

core_bp = Blueprint('core', __name__)


@core_bp.route('/')
@core_bp.route('/index')
@requires_auth
def index():
    return render_template('home.html', user_profile=session['profile'])


@core_bp.route('/event', methods=['POST'])
@requires_auth
def event():
    start_time = request.form.get("start-time")
    end_time = request.form.get("end-time")
    title = request.form.get("title")
    description = request.form.get("description")
    tags = request.form.get("tags")

    flash(f"Recorded event: {title}")

    point = (Point('event')
             .tag('event_id', get_uuid())
             .field('start_time', start_time)
             .field('end_time', end_time)
             .field('title', title)
             .field('description', description)
             .field('tags', tags))

    build_influxdb_client("event").write_record(point)

    return render_template('home.html', user_profile=session['profile'])


@core_bp.route('/about')
def about():
    return render_template('about.html')
