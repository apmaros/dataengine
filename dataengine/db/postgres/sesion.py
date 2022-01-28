from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from dataengine.common.log import logger
from dataengine.db.postgres.config import DbConfig, get_db_url


def get_session(config: DbConfig) -> Session:
    logger.debug(
        f'creating db connection '
        f'database={config.database} '
        f'address={config.host}:{config.port}'
    )

    url = get_db_url(config)
    engine = create_engine(
        url,
        echo=config.echo_queries,
        pool_size=10,
        pool_recycle=3600
    )
    session_class = sessionmaker(bind=engine)
    return session_class()
