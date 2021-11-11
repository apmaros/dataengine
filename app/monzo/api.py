import os

import requests

from app.monzo.monzo_config import MonzoApiConfig
from app.monzo.monzo_token import MonzoToken
from app.server import app
from app.util import random_str


# Monzo OAUTH2 Authorization
# Acquiring an access token is a three-step process:
#
# 1. Redirect the user to Monzo to authorise your app
# 2. Monzo redirects the user back to your app with an authorization code
# 3. Exchange the authorization code for an access token.


BASE_URL = 'https://api.monzo.com'


def get_monzo_config():
    return MonzoApiConfig(
        monzo_redirect_uri='http://127.0.0.1:8050/home?from=auth',
        monzo_client_secret=os.environ.get('MONZO_CLIENT_SECRET'),
        monzo_client_id=os.environ.get('MONZO_CLIENT_ID'),
        monzo_account_id=os.environ.get('MONZO_ACC_ID'),
        base_url=os.environ.get('MONZO_BASE_URL') if os.environ.get('MONZO_BASE_URL') else 'https://api.monzo.com',
        redirect_uri=os.environ.get('MONZO_REDIRECT_URL') if os.environ.get(
            'MONZO_REDIRECT_URL') else 'http://127.0.0.1:8050/home?from=auth',
        auth_base_url='https://auth.monzo.com'
    )


def get_auth_url(config: MonzoApiConfig):
    return f"{config.auth_base_url}/?" \
           f"client_id={config.monzo_client_id}&" \
           f"redirect_uri={config.monzo_redirect_uri}&" \
           f"response_type=code&" \
           f"state={random_str()}"


def get_token(code: str, config: MonzoApiConfig):
    url = f"{config.base_url}/oauth2/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': config.monzo_client_id,
        'client_secret': config.monzo_client_secret,
        'redirect_uri': config.redirect_uri,
        'code': code
    }

    auth_resp = requests.post(
        url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    if auth_resp.status_code != 200:
        app.logger.error(
            f"failed to authenticate with monzo with status_code={auth_resp.status_code}, reason={auth_resp.reason}"
        )
        raise RuntimeError(f"Failed to authenticate due to {auth_resp.content}")

    body = auth_resp.json()

    return MonzoToken(
        access_token=body["access_token"],
        client_id=body["client_id"],
        expires_in_sec=body["expires_in"],
        refresh_token=body["refresh_token"],
        token_type=body["token_type"],
        user_id=body["user_id"],
        account_id=config.monzo_account_id,
    )


def get_transactions(
    since_date: str,
    before_date: str,
    token: str,
    account_id: str
):
    date_params = ""
    if since_date:
        date_params = f'{date_params}&since={since_date}'
    if before_date:
        date_params = f'{date_params}&before={before_date}'

    return requests.get(
        f'{BASE_URL}/transactions?account_id={account_id}&{date_params}&expand[]=merchant',
        headers=get_authenticated_headers(token)
    ).json()


def get_accounts(token: str):
    return requests.get(
        f'{BASE_URL}/accounts',
        headers=get_authenticated_headers(token)
    ).json()


def get_balance(account_id: str, token: str):
    url = f'{BASE_URL}/balance?account_id={account_id}'
    return requests.get(url, headers=get_authenticated_headers(token)).json()


def get_authenticated_headers(access_token: str):
    return {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f"Bearer {access_token}"
    }
