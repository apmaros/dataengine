from flask import (
    request,
    Blueprint,
    flash,
    make_response,
    url_for,
    redirect,
    session,
    render_template
)

from dataengine.common.log import logger
from dataengine.config import DEFAULT_DISPLAY_RESOURCE_DAYS_AGO, ALCOHOL_METRIC
from dataengine.server.routes.annotations import requires_auth
from dataengine.service.db.physio import put_heart_rate_reading, get_heart_rate_readings_since
from service.db.metric import get_metrics_since

physio_bp = Blueprint('physio', __name__, url_prefix='/physio')


@physio_bp.route('/')
@requires_auth
def index():
    profile = session['profile']
    user_id = profile['user_id']
    bp_readings = get_heart_rate_readings_since(
        user_id,
        DEFAULT_DISPLAY_RESOURCE_DAYS_AGO
    )
    alcohol_metrics = get_metrics_since(user_id, ALCOHOL_METRIC, DEFAULT_DISPLAY_RESOURCE_DAYS_AGO)
    return render_template(
        'physio/index.html',
        user_profile=profile,
        bp_readings=bp_readings,
        alcohol_metrics=alcohol_metrics
    )


@physio_bp.route('/blood_pressure', methods=['POST'])
@requires_auth
def blood_pressure():
    try:
        put_heart_rate_reading(session['profile']['user_id'], request.form)
    except RuntimeError as e:
        logger.error(f"Failed to write to influxdb due to {e}")
        flash('Failed to write reading to database')

    flash("Recorded blood pressure reading", 'success')

    return make_response(redirect(url_for('physio.index')))
