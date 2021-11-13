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
