from flask import request, make_response, redirect, render_template, flash, url_for

from dataengine.db.influxdb_client import build_influxdb_client
from dataengine.monzo.api import get_balance, get_monzo_config, get_auth_url, get_transactions, get_accounts
from dataengine.monzo.monzo_client import monzo_client
from dataengine.monzo.monzo_scheduled_service import get_scheduled_monzo_service_instance
from dataengine.monzo.monzo_token import MonzoToken
from dataengine.monzo.security import logout as monzo_logout, get_access_token, set_access_token, set_account_id, get_account_id
from dataengine.transaction.transaction_provider import get_txs_as_points
from dataengine.util import chunks
from dataengine import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/home')
def home():
    handlers = {
        'auth': home_set_auth_handler,
    }

    handler = handlers.get(request.args.get("from"))
    return handler(request)


@app.route('/balance')
def balance():
    balance_resp = get_balance(
        get_account_id(request),
        get_access_token(request),
    )
    app.logger.info(f'balance_resp: {balance_resp}')
    return balance_resp


@app.route('/accounts')
def accounts():
    acc_resp = get_accounts(get_access_token(request))
    app.logger.info(f'acc_resp={acc_resp}')
    return acc_resp


@app.route('/transactions')
def transactions():
    resp = get_transactions(
        request.args.get("since"),
        request.args.get("from"),
        get_access_token(request),
        get_account_id(request),
    )
    app.logger.info(f'resp={resp}')
    return resp


@app.route("/sync-transactions")
def sync_transactions():
    try:
        since = datetime.datetime.now() - datetime.timedelta(30)
        batches = chunks(get_txs_as_points(request, since, None), 500)
        for batch in batches:
            build_influxdb_client().write_records(points=batch)

        app.logger.info(f"flushed transactions to db")
        flash('Transactions were synced', 'success')
    except Exception as e:
        app.logger.error(f"Failed to sync transactions due to {e}")
        flash('Transactions failed to sync')

    return redirect(url_for('index'))


def home_set_auth_handler(req):
    code = req.args.get("code")
    resp = make_response(redirect('index'))
    try:
        token: MonzoToken = monzo_client.acquire_token(code)
        set_access_token(resp, token.access_token)
        set_account_id(resp, token.account_id)
        monzo_client.login(token)
        scheduled_monzo = get_scheduled_monzo_service_instance(
            monzo_client=monzo_client,
            delay_sec=120
        )
        if not scheduled_monzo.is_running:
            app.logger.info("Starting Monzo Scheduled service")
            scheduled_monzo.start()
        else:
            app.logger.info("Monzo Scheduled service running, skipping")

        app.logger.info(f"token acquired until {token.expires_in_sec / 3600}h")
        flash('Successfully logged-in to Monzo')
    except RuntimeError as e:
        app.logger.error(f"Failed to login due to error={e}")
        flash('Failed to login to Monzo')
    return resp


@app.route('/login')
def login():
    return redirect(get_auth_url(get_monzo_config()))


@app.route('/logout')
def logout():
    resp = make_response(redirect('index'))
    monzo_logout(resp)
    flash("Successfully lodged-out")
    return resp

