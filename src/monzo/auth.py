# Monzo OAUTH2 Authorization
# Acquiring an access token is a three-step process:
#
# 1. Redirect the user to Monzo to authorise your app
# 2. Monzo redirects the user back to your app with an authorization code
# 3. Exchange the authorization code for an access token.

import os
import requests
from flask import make_response
from src.server import app
from src.util import random_str

monzo_client_id = os.environ.get('MONZO_CLIENT_ID')
monzo_client_secret = os.environ.get('MONZO_CLIENT_SECRET')
monzo_redirect_uri = 'http://127.0.0.1:8050/home?from=auth'
monzo_auth_base_url = 'https://auth.monzo.com'
base_url = 'https://api.monzo.com'


def get_monzo_auth_url():
    return f"{monzo_auth_base_url}/?" \
                f"client_id={monzo_client_id}&" \
                f"redirect_uri={monzo_redirect_uri}&" \
                f"response_type=code&" \
                f"state={random_str()}"


def get_token(code: str) -> str:
    url = f"{base_url}/oauth2/token"
    data = {
            'grant_type': 'authorization_code',
            'client_id': monzo_client_id,
            'client_secret': monzo_client_secret,
            'redirect_uri': monzo_redirect_uri,
            'code': code
        }
    auth_resp = requests.post(
        url,
        data=data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )

    if auth_resp.status_code != 200:
        app.logger.error(
            f"failed to authenticate with monzo with status_code={auth_resp.status_code}, reason={auth_resp.reason}"
        )
        app.logger.error(f'error response = {auth_resp.content}')
        return make_response('Failed to authenticate')

    body = auth_resp.json()

    resp = make_response()
    resp.set_cookie('monzo_access_token', body['access_token'])

    return body['access_token']
