import json

from db.redis_client import get_redis_client
from monzo.monzo_token import MonzoToken
import typing as t

MONZO_TOKEN_KEY = "monzo_token"


def store_monzo_token(token: MonzoToken):
    get_redis_client().set(
        MONZO_TOKEN_KEY,
        token.to_json()
    )


def load_monzo_token() -> t.Optional[MonzoToken]:
    token_bytes = get_redis_client().get(MONZO_TOKEN_KEY)
    if not token_bytes:
        return None

    token = MonzoToken(**json.loads(token_bytes.decode("utf-8")))
    # TODO validate token not expired

    return token
