import datetime
import traceback

from flask import (
    request,
    make_response,
    redirect,
    render_template,
    flash,
    url_for,
    Blueprint
)
from common.log import logger
from common.util import chunks
from config import get_monzo_config
from dataengine.db.influxdb_client import build_influxdb_client
from dataengine.monzo.api import get_balance, get_auth_url, get_transactions, get_accounts
from dataengine.monzo.monzo_scheduled_service import get_scheduled_monzo_service_instance
from dataengine.monzo.monzo_token import MonzoToken
from dataengine.monzo.security import logout as monzo_logout, get_access_token, set_access_token, set_account_id, \
    get_account_id
from dataengine.transaction.transaction_provider import get_txs_as_points
from monzo.monzo_client import build_monzo_client
from monzo.monzo_token_provider import store_monzo_token, load_monzo_token

core_bp = Blueprint('core', __name__)


@core_bp.route('/')
@core_bp.route('/index')
def index():
    return render_template('home.html')


@core_bp.route('/home')
def home():
    handlers = {
        'auth': home_set_auth_handler,
    }

    handler = handlers.get(request.args.get("from"))
    return handler(request)


@core_bp.route('/balance')
def balance():
    balance_resp = get_balance(
        get_account_id(request),
        get_access_token(request),
    )
    logger.info(f'balance_resp: {balance_resp}')
    return balance_resp


@core_bp.route('/accounts')
def accounts():
    acc_resp = get_accounts(get_access_token(request))
    logger.info(f'acc_resp={acc_resp}')
    return acc_resp


@core_bp.route('/transactions')
def transactions():
    resp = get_transactions(
        request.args.get("since"),
        request.args.get("from"),
        get_access_token(request),
        get_account_id(request),
    )
    logger.info(f'resp={resp}')
    return resp


@core_bp.route("/sync-transactions")
def sync_transactions():
    try:
        since = datetime.datetime.now() - datetime.timedelta(30)
        batches = chunks(get_txs_as_points(request, since, None), 500)
        for batch in batches:
            build_influxdb_client().write_records(points=batch)

        logger.info(f"flushed transactions to db")
        flash('Transactions were synced', 'success')
    except Exception as e:
        logger.error(f"Failed to sync transactions due to {e}")
        flash('Transactions failed to sync')

    return redirect(url_for('index'))


@core_bp.route("/schedule-monzo-sync")
def schedule_monzo_sync():
    try:
        token = load_monzo_token()
        if not token:
            logger.warn("Can not schedule Monzo sync, Monzo token not found")
            flash("Monzo token not found, please login to Monzo")
            return make_response(redirect('index'))

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

    return make_response(redirect('index'))


def home_set_auth_handler(req):
    code = req.args.get("code")
    resp = make_response(redirect('index'))
    monzo_client = build_monzo_client()
    try:
        token: MonzoToken = monzo_client.acquire_token(code)
        set_access_token(resp, token.access_token)
        set_account_id(resp, token.account_id)

        try:
            store_monzo_token(token)
        except RuntimeError as e:
            logger.error(f"Failed to store monzo token due to {e}")

        monzo_client.login(token)

        logger.info(f"token acquired until {token.expires_in_sec / 3600}h")
        flash('Successfully logged-in to Monzo')
    except RuntimeError as e:
        logger.error(f"Failed to login due to error={e}")
        flash('Failed to login to Monzo')
    return resp


@core_bp.route('/login-monzo')
def login():
    return redirect(get_auth_url(get_monzo_config()))


@core_bp.route('/logout-monzo')
def logout():
    resp = make_response(redirect('index'))
    monzo_logout(resp)
    flash("Successfully lodged-out")
    return resp

