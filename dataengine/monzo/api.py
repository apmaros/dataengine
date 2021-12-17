from typing import Dict

import requests

from common.log import logger
from common.util import random_str, current_time_sec
from config import BASE_URL
from monzo.model.api_error import ApiError
from monzo.model.monzo_config import MonzoApiConfig
from monzo.model.monzo_token import MonzoToken


# Monzo OAUTH2 Authorization
# Acquiring an access token is a three-step process:
#
# 1. Redirect the user to Monzo to authorise your app
# 2. Monzo redirects the user back to your app with an authorization code
# 3. Exchange the authorization code for an access token.


def get_auth_url(config: MonzoApiConfig):
    return f"{config.auth_base_url}/?" \
           f"client_id={config.monzo_client_id}&" \
           f"redirect_uri={config.redirect_uri}&" \
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
        logger.error(
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


def refresh_token(secret: str, token: MonzoToken) -> MonzoToken:
    url = f"{BASE_URL}/oauth2/token"
    data = {
        'grant_type': 'refresh_token',
        'client_id': token.client_id,
        'client_secret': secret,
        'refresh_token': token.refresh_token,
    }

    auth_resp = requests.post(
        url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    if auth_resp.status_code != 200:
        logger.error(
            f"failed to authenticate with monzo with status_code={auth_resp.status_code}, reason={auth_resp.reason}"
        )
        raise RuntimeError(f"Failed to authenticate due to {auth_resp.content}")

    body = auth_resp.json()

    token = MonzoToken(
        access_token=body["access_token"],
        client_id=body['client_id'],
        expires_in_sec=body['expires_in'],
        refresh_token=body['refresh_token'],
        token_type=body['token_type'],
        user_id=body['user_id'],
        account_id=token.account_id,
        created_at_sec=current_time_sec()
    )

    return token


def get_transactions(
    since_date: str,
    before_date: str,
    token: str,
    account_id: str
):
    """
    Returns transactions from Monzo API
    Date format is as following: format 'YYYY-MM-DDTHH:MM:SS+00:00' (e.g. '2021-03-05T00:00:00+00:00')
    :param account_id: monzo account id
    :param token: monzo access token
    :param since_date: Starting point since (or from) to return transactions
    :param before_date: End point before (or to) which to return transactions
    :return: JSON Array of transactions
    """
    date_params = ""
    if since_date:
        date_params = f'{date_params}&since={since_date}'
    if before_date:
        date_params = f'{date_params}&before={before_date}'

    result = requests.get(
        f'{BASE_URL}/transactions?account_id={account_id}&{date_params}&expand[]=merchant',
        headers=get_authenticated_headers(token)
    )
    content: Dict = result.json()
    if result.status_code == 200:
        return content
    else:
        raise ApiError(
            content.get('code', 'unknown'),
            content.get('message', 'Unknown error')
        )


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
