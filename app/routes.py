from app.db.influxdb_client import build_influxdb_client
from app.monzo.api import get_balance, get_accounts, get_transactions
from app.monzo.auth import get_token, get_monzo_auth_url, MonzoToken
from app.monzo.security import logout, get_access_token, set_access_token
from app.server import app
from flask import request, make_response, redirect, render_template, flash, url_for
from app.transaction.transaction_provider import get_txs_as_points
from app.util import chunks


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
    balance_resp = get_balance(get_access_token(request))
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
        request,
        request.args.get("since"),
        request.args.get("from")
    )
    app.logger.info(f'resp={resp}')
    return resp


@app.route("/sync-transactions")
def sync_transactions():
    try:
        batches = chunks(get_txs_as_points(request, None, None), 500)
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
    app.logger.info(f"Requesting token")
    resp = make_response(render_template('home.html'))
    try:
        token: MonzoToken = get_token(code)
        logout(resp)
        set_access_token(resp, token.access_token)
        app.logger.info(f"token acquired until {token.expires_in_sec / 3600}")
        flash('Successfully logged-in to Monzo')
    except RuntimeError as e:
        app.logger.error(e)
        flash('Failed to login to Monzo')
    return resp


@app.route('/login')
def auth():
    logout(make_response())
    return redirect(get_monzo_auth_url())
