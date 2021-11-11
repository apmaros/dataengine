from dataclasses import dataclass


@dataclass
class MonzoToken:
    access_token: str
    client_id: str
    expires_in_sec: int
    refresh_token: str
    token_type: str
    user_id: str
    account_id: str
