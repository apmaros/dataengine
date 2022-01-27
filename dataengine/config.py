from dataengine.common.secrets import get_secret
from dataengine.monzo.model.monzo_config import MonzoApiConfig

SERVER_NAME = get_secret('SERVER_NAME')

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
SESSION_COOKIE_NAME = 'mysession'

# influxdb
INFLUXDB_TOKEN = get_secret('INFLUXDB_TOKEN_V3')
INFLUXDB_ORG = get_secret('INFLUXDB_ORG')
INFLUXDB_BUCKET = get_secret('INFLUXDB_BUCKET')
INFLUXDB_URL = get_secret("INFLUXDB_URL")

# redis
REDIS_PORT = 6379
REDIS_HOST = "redis"

# Auth0
AUTH0_CLIENT_ID = get_secret('AUTH0_CLIENT_ID')
AUTO0_CLIENT_SECRET = get_secret('AUTH0_CLIENT_SECRET')
AUTH0_API_BASE_URL = get_secret('AUTH0_API_BASE_URL')
AUTH0_ACCESS_TOKEN_URL = f'{AUTH0_API_BASE_URL}/oauth/token'
AUTH0_AUTHORIZE_URL = f'{AUTH0_API_BASE_URL}/authorize'
AUTH0_CLIENT_KWARGS = 'openid profile email'
AUTH0_CALLBACK_URL = get_secret('AUTH0_CALLBACK_URL')

# DB
DB_USERNAME = get_secret("POSTGRES_USER")
DB_PASSWORD = get_secret("POSTGRES_PASSWORD")
DB_HOST = get_secret("POSTGRES_HOST")
DB_PORT = 5432
DB_NAME = get_secret("POSTGRES_DB") if get_secret("POSTGRES_DB") else 'dataengine'

# Service
EVENT_INFLUX_BUCKET = 'events'

# View
# DDD at hh:mm (dd/mm/yyyy)
DATETIME_VIEW_FORMAT = "%a at %H:%M (%d/%m/%y)"
DEFAULT_DISPLAY_RESOURCE_DAYS_AGO = 30
