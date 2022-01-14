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

from config import EVENT_INFLUX_BUCKET
from dataengine.common.log import logger
from dataengine.model.day_note import DayNote, day_note_to_record
from dataengine.server.routes.annotations import requires_auth
from db.influxdb_client import build_influxdb_client
from service.day_note import get_day_notes

day_note_bp = Blueprint('day_note', __name__, url_prefix='/day_note')


@day_note_bp.route('/')
@requires_auth
def index():
    profile = session['profile']
    day_notes = get_day_notes(profile['user_id'])
    return render_template('day_note/index.html', user_profile=profile, day_notes=day_notes)


@day_note_bp.route('/new', methods=['POST'])
@requires_auth
def new():
    day_note = DayNote(
        note=request.form['note'],
        sad=request.form['sad'],
        energetic=request.form['energetic'],
        anxious=request.form['anxious'],
        creative=request.form['creative'],
        user_id=session['profile']['user_id'],
    )
    try:
        build_influxdb_client(EVENT_INFLUX_BUCKET).write_record_sync(day_note_to_record(day_note))
    except RuntimeError as e:
        logger.error(f"Failed to write to database due to error {e}")
        flash('Failed to record day note due to error', 'error')

    flash(f"👌 Day note was recorded", 'success')

    return make_response(redirect(url_for('day_note.index')))
