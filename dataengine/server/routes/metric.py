from flask import (
    Blueprint,
    session,
    request,
    flash,
    make_response,
    redirect, render_template,
)

from dataengine.common.log import logger
from dataengine.config import DEFAULT_DISPLAY_RESOURCE_DAYS_AGO
from dataengine.server.routes.annotations import requires_auth
from dataengine.service.db.metric import put_metric, get_metrics_since, \
    get_metrics_by_user_metric_id_since

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


@metric_bp.route('/<user_metric_id>')
@requires_auth
def index(user_metric_id):
    profile = session['profile']

    metrics = []
    try:
        metrics = get_metrics_by_user_metric_id_since(
            profile['user_id'],
            user_metric_id,
            DEFAULT_DISPLAY_RESOURCE_DAYS_AGO
        )
    except RuntimeError as e:
        logger.error(f"Failed to get metrics due to error {e}")
        flash('Failed to get metrics due to error', 'error')


    return render_template(
        'metric/index.html',
        user_profile=profile,
        metrics=metrics,
    )
