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
    raw_token = get_redis_client().get(MONZO_TOKEN_KEY)
    if not raw_token:
        return None

    token = MonzoToken(**json.load(raw_token))
    # TODO validate token not expired

    return token
