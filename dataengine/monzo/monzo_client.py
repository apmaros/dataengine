import json
import typing as t

from config import get_monzo_config
from dataengine.monzo.api import (
    get_token,
    get_auth_url,
    get_authenticated_headers,
    get_transactions,
    get_accounts,
    get_balance,
    refresh_token
)
from db.redis_client import get_redis_client
from monzo.model.monzo_config import MonzoApiConfig
from monzo.model.monzo_token import MonzoToken


class AuthenticationException(Exception):
    pass


class MonzoClient(object):
    _REDIS_MONZO_TOKEN_KEY = 'monzo_token'

    def __init__(self, config: MonzoApiConfig, token: MonzoToken = None):
        self.config = config
        self.token: t.Optional[MonzoToken] = token

    def acquire_token(self, code: str) -> MonzoToken:
        return get_token(code, self.config)

    def get_token(self) -> MonzoToken:
        return self.token

    def get_monzo_auth_url(self):
        get_auth_url(self.config)

    def get_balance(self):
        return get_balance(self.config.monzo_account_id, self.token.access_token)

    def get_accounts(self):
        return get_accounts(self.token.access_token)

    def get_transactions(self, since_date, before_date=None):
        return get_transactions(since_date, before_date, self.token.access_token, self.config.monzo_account_id)

    def get_all_transactions(self):
        return self.get_transactions(None, None)

    def get_expiry_sec(self):
        return self.token.expires_in_sec

    def login(self, token: MonzoToken):
        self.token = token

    def is_authenticated(self):
        return self.token is not None

    def refresh_token(self) -> MonzoToken:
        if not self.is_authenticated():
            raise AuthenticationException("Client not logged in - token not present")
        new_token = refresh_token(self.config.monzo_client_secret, self.token)
        self.token = new_token

        return self.token

    def load_monzo_token(self) -> t.Optional[MonzoToken]:
        token_bytes = get_redis_client().get(self._REDIS_MONZO_TOKEN_KEY)
        if not token_bytes:
            return None
        self.token = MonzoToken(**json.loads(token_bytes.decode("utf-8")))

    def _get_authenticated_headers(self):
        if not self.token:
            raise AuthenticationException("Client not logged in - token not present")

        get_authenticated_headers(self.token.access_token)


def build_monzo_client(token: MonzoToken = None) -> MonzoClient:
    client = MonzoClient(get_monzo_config())
    if MonzoToken:
        client.login(token)
    return client
