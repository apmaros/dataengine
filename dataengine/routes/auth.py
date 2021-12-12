from flask import Blueprint
from flask import (
    session,
    url_for,
    redirect
)
from urllib.parse import urlencode

from common.log import logger
from config import AUTH0_CALLBACK_URL, AUTH0_CLIENT_ID, SERVER_NAME
from context import Context

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    return Context.auth0().authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL)


@auth_bp.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {
        'returnTo': SERVER_NAME,
        'client_id': AUTH0_CLIENT_ID
    }
    return redirect(Context.auth0().api_base_url + '/v2/logout?' + urlencode(params))


@auth_bp.route('/callback')
def callback_handling():
    auth0 = Context.auth0()
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    logger.warn(f"resp={resp}")
    userinfo = resp.json()

    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect(url_for('core.index'))
