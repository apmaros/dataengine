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

from dataengine.common.log import logger
from dataengine.config import MAPBOX_ACCESS_TOKEN
from dataengine.server.routes.annotations import requires_auth
from dataengine.server.routes.validator.note import validate_note
from dataengine.service.db.note import get_notes_since, put_note, delete_note, get_note, update_note

note_bp = Blueprint('note', __name__, url_prefix='/note')


@note_bp.route('/')
@requires_auth
def index():
    profile = session['profile']
    notes = get_notes_since(profile['user_id'], 30)
    return render_template(
        'note/index.html',
        user_profile=profile,
        notes=notes,
        mapbox_token=MAPBOX_ACCESS_TOKEN
    )


@note_bp.route('/', methods=['POST'])
@requires_auth
def new():
    try:
        validate_note(request.form)
        put_note(session['profile']['user_id'], request.form)
        flash(f"👌 Day note was recorded", 'success')
    except Exception as e:
        logger.error(f"Failed to write a note to database due to error", e)
        flash('Failed to store a note due to an error', 'error')

    return make_response(redirect(url_for('note.index')))


@note_bp.route('/edit')
@requires_auth
def edit():
    note = get_note(request.args['id'])
    return make_response(render_template(
        'note/edit.html',
        note=note,
        referrer=request.referrer,
    ))


@note_bp.route('/edit', methods=['POST'])
@requires_auth
def edit_post():
    try:
        update_note(request.args)
        flash(f"👌 Day note was updated", 'success')
    except Exception as e:
        logger.error(f"Failed to update note due to error {e}")
        flash('Failed to update note due to an error', 'error')

    return make_response(redirect(url_for('note.index')))


@note_bp.route('/delete', )
@requires_auth
def delete():
    try:
        delete_note(request.args['id'])
        flash('👌 Note was deleted', 'success')
    except Exception as e:
        logger.error(f"Failed to delete note {e}")
        flash('Failed to delete a note due to an error', 'error')

    return make_response(redirect(url_for('note.index')))
