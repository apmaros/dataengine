from flask import Blueprint, session, render_template, flash, make_response, \
    url_for
from werkzeug.utils import redirect
from flask import request
from dataengine.common.log import logger
from dataengine.server.routes.annotations import requires_auth
from dataengine.server.routes.validator.user_metric import (
    validate_user_metric_form
)
from dataengine.service.db.user_metric import get_user_metrics, put_user_metric

user_metric_bp = Blueprint('user_metric', __name__, url_prefix='/user/metric')


@user_metric_bp.route('/')
@requires_auth
def index():
    profile = session['profile']
    user_metrics = get_user_metrics(profile['user_id'])

    return render_template(
        'user_metric/index.html',
        user_profile=profile,
        user_metrics=user_metrics,
    )


@user_metric_bp.route('/', methods=["POST"])
@requires_auth
def new():
    profile = session['profile']
    try:
        validate_user_metric_form(request.form)
        put_user_metric(profile['user_id'], request.form)
    except Exception as e:
        logger.error(f'Failed to write to database due to error {e}')
        flash('Failed to record event due to error', 'error')

    flash(f"👌 Event was recorded", 'success')

    return make_response(redirect(url_for('user_metric.index')))
