from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from common.log import logger
from db.postgres.config import DbConfig, get_db_url


def get_session(config: DbConfig) -> Session:
    logger.info(f'creating db connection '
                f'database={config.database} '
                f'address={config.host}:{config.port}')

    url = get_db_url(config)
    engine = create_engine(
        url,
        echo=config.echo_queries,
        pool_size=10
    )
    session_class = sessionmaker(bind=engine)
    return session_class()
