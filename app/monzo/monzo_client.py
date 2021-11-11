from typing import Optional
from app.monzo.api import (
    get_token,
    get_auth_url,
    get_authenticated_headers,
    get_transactions,
    get_accounts,
    get_balance,
    get_monzo_config
)
from app.monzo.monzo_config import MonzoApiConfig
from app.monzo.monzo_token import MonzoToken


class AuthenticationException(Exception):
    pass


class MonzoClient(object):
    def get_token(self, code: str) -> MonzoToken:
        return get_token(code, self.config)

    def get_monzo_auth_url(self):
        get_auth_url(self.config)

    def get_balance(self):
        return get_balance(self.config.monzo_account_id, self.token.access_token)

    def get_accounts(self):
        return get_accounts(self.token.access_token)

    def get_transactions(self, since_date, before_date):
        """
        Returns transactions from Monzo API
        Date format is as following: format 'YYYY-MM-DDTHH:MM:SS+00:00' (e.g. '2021-03-05T00:00:00+00:00')
        :param since_date: Starting point since (or from) to return transactions
        :param before_date: End point before (or to) which to return transactions
        :return: JSON Array of transactions
        """
        return get_transactions(since_date, before_date, self.token.access_token, self.config.monzo_account_id)

    def get_all_transactions(self):
        return self.get_transactions(None, None)

    def _get_authenticated_headers(self):
        if not self.token:
            raise AuthenticationException("Client not logged in - token not present")

        get_authenticated_headers(self.token.access_token)

    def login(self, token: MonzoToken):
        self.token = token

    def __init__(self, config: MonzoApiConfig):
        self.config = config
        self.token: Optional[MonzoToken] = None


def build_monzo_client() -> MonzoClient:
    return MonzoClient(get_monzo_config())


monzo_client = build_monzo_client()
