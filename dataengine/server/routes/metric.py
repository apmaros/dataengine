from flask import (
    Blueprint,
    session,
    request,
    flash,
    make_response,
    redirect,
)

from dataengine.common.log import logger
from dataengine.server.routes.annotations import requires_auth
from dataengine.service.db.metric import put_metric

metric_bp = Blueprint('metric', __name__, url_prefix='/metric')


@metric_bp.route('/', methods=['POST'])
@requires_auth
def new():
    # todo: add validation
    profile = session['profile']
    try:
        put_metric(profile['user_id'], request.form)
    except RuntimeError as e:
        logger.error(f"Failed to write to database due to error {e}")
        flash('Failed to record event due to error', 'error')

    flash(f"👌 Metric was recorded", 'success')

    return make_response(redirect(request.referrer))
