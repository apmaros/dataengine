from dataclasses import dataclass


@dataclass
class MonzoApiConfig:
    monzo_client_secret: str
    monzo_client_id: str
    monzo_account_id: str
    monzo_redirect_uri: str
    base_url: str
    redirect_uri: str
    auth_base_url: str
