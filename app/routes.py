from app.db.db_client import build_db_client
from app.monzo.api import get_balance, get_accounts, get_transactions
from app.monzo.auth import get_token, get_monzo_auth_url
from app.monzo.security import set_access_token, logout
from app.server import app
from flask import request, make_response, redirect, render_template, flash, url_for
from app.transaction.transaction_provider import get_txs_df


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
    resp = handler(request)

    return resp


@app.route('/balance')
def balance():
    balance_resp = get_balance(request)
    app.logger.info(f'balance_resp: {balance_resp}')
    return balance_resp


@app.route('/accounts')
def accounts():
    acc_resp = get_accounts(request)
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
        txs = get_txs_df(request, None, None)
        txs.set_index('time', inplace=True)
        app.logger.info(f"Loaded {len(txs)} transactions")
        build_db_client().write_dataframe(
            txs,
            ['category', 'type', 'abs_amount', 'amount'],
            'transactions'
        )
        app.logger.info(f"flushed transactions to db")
        flash('Transactions were synced', 'success')
    except Exception as e:
        app.logger.error(f"Failed to sync transactions due to {e}")
        flash('Transactions failed to sync')

    return redirect(url_for('index'))


def home_set_auth_handler(req):
    code = req.args.get("code")
    app.logger.info(f"Requesting token")
    resp = make_response("Login was successful")
    set_access_token(resp, get_token(code))
    app.logger.info(f"Token acquired")

    return resp


@app.route('/login')
def auth():
    logout(make_response())
    return redirect(get_monzo_auth_url())
