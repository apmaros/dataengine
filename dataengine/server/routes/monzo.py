import traceback

from flask import (
    make_response,
    redirect,
    flash,
    url_for,
    Blueprint,
    request
)

from dataengine.common.log import logger
from dataengine.config import get_monzo_config
from dataengine.db.influxdb_client import build_influxdb_client
from dataengine.monzo.api import get_auth_url
from dataengine.monzo.model.monzo_token import MonzoToken
from dataengine.monzo.monzo_client import build_monzo_client
from dataengine.monzo.monzo_scheduled_service import get_scheduled_monzo_service_instance
from dataengine.monzo.monzo_service import MonzoService
from dataengine.monzo.monzo_token_provider import load_monzo_token, remove_monzo_token, store_monzo_token
from dataengine.server.routes.annotations import requires_auth

monzo_bp = Blueprint('monzo', __name__, url_prefix='/monzo')


@monzo_bp.route("/sync")
@requires_auth
def sync():
    try:
        token = load_monzo_token()
        if not token:
            logger.warn("Can not schedule Monzo sync, Monzo token not found")
            flash("Monzo token not found, please login to Monzo")
            return make_response(redirect(url_for('core.index')))

        sync_success = MonzoService(
            build_monzo_client(token),
            build_influxdb_client()
        ).sync_transactions(sync_since_days=None)  # None - from the beginning of time

        if sync_success:
            flash('Transactions were synced', 'success')
        else:
            flash('Failed to sync transactions', 'failure')
    except Exception as e:
        logger.error(f"Failed to sync transactions due to {e}")
        flash('Transactions failed to sync')

    return make_response(redirect(url_for('core.index')))


@monzo_bp.route("/schedule")
@requires_auth
def schedule():
    try:
        token = load_monzo_token()
        if not token:
            logger.warn("Can not schedule Monzo sync, Monzo token not found")
            flash("Monzo token not found, please login to Monzo")
            return make_response(redirect(url_for('core.index')))

        monzo_client = build_monzo_client(token)
        scheduled_monzo = get_scheduled_monzo_service_instance(
            monzo_client=monzo_client,
            delay_sec=120
        )
        if not scheduled_monzo.is_running:
            logger.info("Starting Monzo Scheduled service")
            scheduled_monzo.start()
            flash("Scheduled Monzo Sync")
        else:
            logger.info("Monzo Scheduled service running, skipping")
            flash("Monzo already scheduled")
    except Exception as e:
        logger.error(f"Failed to schedule Mozno sync due to {e}")
        logger.error(traceback.print_exc())

    return make_response(redirect(url_for('core.index')))


@monzo_bp.route('/login')
@requires_auth
def login():
    return redirect(get_auth_url(get_monzo_config()))


@monzo_bp.route('/callback')
@requires_auth
def callback():
    code = request.args.get("code")
    resp = make_response(redirect(url_for('core.index')))
    monzo_client = build_monzo_client()
    try:
        token: MonzoToken = monzo_client.acquire_token(code)
        try:
            store_monzo_token(token)
        except RuntimeError as e:
            logger.error(f"Failed to store monzo token due to {e}")

        monzo_client.login(token)

        logger.info(f"token acquired (Valid for {round(token.expires_in_sec / 3600, 2)} hours)")
        flash('Successfully logged-in to Monzo')
    except RuntimeError as e:
        logger.error(f"Failed to login due to error={e}")
        flash('Failed to login to Monzo')
    return resp


@monzo_bp.route('/logout')
@requires_auth
def logout():
    resp = make_response(redirect(url_for('core.index')))
    remove_monzo_token()
    flash("Successfully lodged-out")
    return resp
