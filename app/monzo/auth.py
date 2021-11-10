# Monzo OAUTH2 Authorization
# Acquiring an access token is a three-step process:
#
# 1. Redirect the user to Monzo to authorise your app
# 2. Monzo redirects the user back to your app with an authorization code
# 3. Exchange the authorization code for an access token.

import os
from dataclasses import dataclass

import requests
from app.server import app
from app.util import random_str

monzo_client_id = os.environ.get('MONZO_CLIENT_ID')
monzo_client_secret = os.environ.get('MONZO_CLIENT_SECRET')
monzo_redirect_uri = 'http://127.0.0.1:8050/home?from=auth'
monzo_auth_base_url = 'https://auth.monzo.com'
base_url = 'https://api.monzo.com'


@dataclass
class MonzoToken:
    access_token: str
    client_id: str
    expires_in_sec: int
    refresh_token: str
    token_type: str
    user_id: str


def get_monzo_auth_url():
    return f"{monzo_auth_base_url}/?" \
                f"client_id={monzo_client_id}&" \
                f"redirect_uri={monzo_redirect_uri}&" \
                f"response_type=code&" \
                f"state={random_str()}"


def get_token(code: str) -> MonzoToken:
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
        raise RuntimeError(f"Failed to authenticate due to {auth_resp.content}")

    body = auth_resp.json()

    return MonzoToken(
        access_token=body["access_token"],
        client_id=body["client_id"],
        expires_in_sec=body["expires_in"],
        refresh_token=body["refresh_token"],
        token_type=body["token_type"],
        user_id=body["user_id"],
    )
