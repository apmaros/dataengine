import os
import requests
from app.monzo.security import get_access_token


monzo_redirect_uri = 'http://127.0.0.1:8050/home?from=auth'
monzo_client_secret = os.environ.get('MONZO_CLIENT_SECRET')
monzo_client_id = os.environ.get('MONZO_CLIENT_ID')
monzo_account_id = os.environ.get('MONZO_ACC_ID')
base_url = 'https://api.monzo.com'


def get_balance(access_token: str):
    url = f'{base_url}/balance?account_id={monzo_account_id}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f"Bearer {get_access_token(access_token)}"
    }
    return requests.get(
        url,
        headers=headers
    ).json()


def get_accounts(access_token: str):
    return requests.get(
        f'{base_url}/accounts',
        headers=get_authenticated_headers(access_token)
    ).json()


def get_transactions(access_token: str, since_date, before_date):
    """
    Returns transactions from Monzo API
    Date format is as following: format 'YYYY-MM-DDTHH:MM:SS+00:00' (e.g. '2021-03-05T00:00:00+00:00')
    :param access_token: str
    :param since_date: Starting point since (or from) to return transactions
    :param before_date: End point before (or to) which to return transactions
    :return: JSON Array of transactions

    """
    date_params = ""
    if since_date:
        date_params = f'{date_params}&since={since_date}'
    if before_date:
        date_params = f'{date_params}&before={before_date}'

    return requests.get(
        f'{base_url}/transactions?account_id={monzo_account_id}&{date_params}&expand[]=merchant',
        headers=get_authenticated_headers(access_token)
    ).json()


def get_all_transactions(access_token: str):
    return get_transactions(access_token, None, None)


def get_authenticated_headers(access_token):
    return {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f"Bearer {access_token}"
    }
