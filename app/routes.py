from app.monzo.api import get_balance, get_accounts, get_transactions
from app.monzo.auth import get_token, get_monzo_auth_url
from app.monzo.security import set_access_token, logout
from app.server import app
from flask import request, make_response, redirect, render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', name="Maros", card_text="this is my card text. COOOL")


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
