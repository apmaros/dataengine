from common.secrets import get_secret
from monzo.monzo_config import MonzoApiConfig

# Monzo
BASE_URL = 'https://api.monzo.com'
MONZO_REDIRECT_URL = get_secret('MONZO_REDIRECT_URL')
DEFAULT_MONZO_REDIRECT_URL = 'http://127.0.0.1:8050/home?from=auth'


def get_monzo_config():
    return MonzoApiConfig(
        monzo_client_secret=get_secret('MONZO_CLIENT_SECRET'),
        monzo_client_id=get_secret('MONZO_CLIENT_ID'),
        monzo_account_id=get_secret('MONZO_ACC_ID'),
        base_url=BASE_URL,
        redirect_uri=MONZO_REDIRECT_URL if MONZO_REDIRECT_URL else DEFAULT_MONZO_REDIRECT_URL,
        auth_base_url='https://auth.monzo.com'
    )


SERVER_SECRET_KEY = get_secret("SERVER_SECRET_KEY")
SERVER_SESSION_TYPE = 'filesystem'

# influxdb
INFLUXDB_TOKEN = get_secret('INFLUXDB_TOKEN_V3')
INFLUXDB_ORG = get_secret('INFLUXDB_ORG')
INFLUXDB_BUCKET = get_secret('INFLUXDB_BUCKET')
INFLUXDB_URL = get_secret("INFLUXDB_URL")

# redis
REDIS_PORT = 6379
REDIS_HOST = "redis"
