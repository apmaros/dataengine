import string
from dataclasses import dataclass

from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


@dataclass
class DbConfig:
    username: string
    password: string
    host: string
    port: int
    database: string
    # logs ALL database queries
    echo_queries: bool
    # logs SQL engine debug operations
    engine_debug: bool

    def __init__(
        self,
        username=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        echo_queries=True,
        echo_debug=True
    ):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.echo_queries = echo_queries
        self.echo_debug = echo_debug


def get_db_url(config: DbConfig = DbConfig()):
    return "postgresql://{}:{}@{}:{}/{}".format(
        config.username,
        config.password,
        config.host,
        config.port,
        config.database,
    )
