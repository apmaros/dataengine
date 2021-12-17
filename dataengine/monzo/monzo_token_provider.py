import json
import typing as t

from db.redis_client import get_redis_client
from monzo.model.monzo_token import MonzoToken

MONZO_TOKEN_KEY = "monzo_token"


def store_monzo_token(token: MonzoToken) -> None:
    """
    Save Monzo Token to remote store
    :param token: MonzoToken
    :raises: ConnectionError, TimeoutError
    :return: None
    """
    get_redis_client().set(
        MONZO_TOKEN_KEY,
        token.to_json()
    )


def remove_monzo_token():
    """
    Removes Monzo Token from remote store
    :raises: ConnectionError, TimeoutError
    :return:
    """
    get_redis_client().delete(MONZO_TOKEN_KEY)


def load_monzo_token() -> t.Optional[MonzoToken]:
    """
    Loads Monzo Token from remote store
    :raises: ConnectionError, TimeoutError
    :return: Optional[MonzoToken]
    """
    token_bytes = get_redis_client().get(MONZO_TOKEN_KEY)
    if not token_bytes:
        return None

    return MonzoToken(**json.loads(token_bytes.decode("utf-8")))
