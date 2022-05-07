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
from dataengine.server.RequestError import RequestError, ErrorType
from dataengine.server.routes.annotations import requires_auth
from dataengine.service.db.metric import (
    put_metric,
    get_metrics_by_user_metric_id_since
)
from dataengine.service.db.user_metric import get_user_metric

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

    if request.referrer:
        redirect_to = request.referrer
    else:
        redirect_to = '/metric/'

    return make_response(redirect(redirect_to))


@metric_bp.route('/<user_metric_id>')
@requires_auth
def index(user_metric_id):
    profile = session['profile']
    user_id = profile['user_id']
    metrics = []
    user_metric = None

    try:
        user_metric = get_user_metric(user_metric_id)
        _validate_user(user_id, user_metric.user_id)

        metrics = get_metrics_by_user_metric_id_since(
            user_id,
            user_metric_id,
            DEFAULT_DISPLAY_RESOURCE_DAYS_AGO
        )
    except RequestError as e:
        logger.error(f"Failed to get metrics due to error {e}")
        flash('Failed to get metrics due to error', 'error')

    return render_template(
        'metric/index.html',
        user_profile=profile,
        user_metric=user_metric,
        metrics=metrics,
        referrer=request.referrer,
    )


def _validate_user(user_id: str, user_metric_user_id: str):
    if user_id != user_metric_user_id:
        raise RequestError(
            ErrorType.UNAUTHORISED,
            f'Metric does not belong to the user'
            f'user_id={user_id}, user_metric_user_id={user_metric_user_id}',
        )
