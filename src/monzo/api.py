import os
import requests
from src.monzo.security import get_access_token, get_authenticated_headers


monzo_redirect_uri = 'http://127.0.0.1:8050/home?from=auth'
monzo_client_secret = os.environ.get('MONZO_CLIENT_SECRET')
monzo_client_id = os.environ.get('MONZO_CLIENT_ID')
base_url = 'https://api.monzo.com'


def get_balance(req):
    url = f'{base_url}/balance?account_id=acc_00009R9wohAMOeu47J6j4r'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f"Bearer {get_access_token(req)}"
    }
    return requests.get(
        url,
        headers=headers
    ).json()


def get_accounts(req):
    return requests.get(
        f'{base_url}/accounts',
        headers=get_authenticated_headers(req)
    ).json()


# '2021-03-05T00:00:00+00:00'
def get_transactions(req, since_date, before_date):
    date_params = ""
    if since_date:
        date_params = f'{date_params}&since={since_date}'
    if before_date:
        date_params = f'{date_params}&before={before_date}'

    return requests.get(
        f'{base_url}/transactions?account_id=acc_00009R9wohAMOeu47J6j4r{date_params}&expand[]=merchant',
        headers=get_authenticated_headers(req)
    ).json()


def get_all_transactions(req):
    return get_transactions(req, None, None)