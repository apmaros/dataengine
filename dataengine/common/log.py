import logging
import os

from newrelic.agent import NewRelicContextFormatter

from common.env import is_dev

logger = logging.getLogger()

if not is_dev():
    # Instantiate a new log handler
    handler = logging.StreamHandler()

    # Instantiate the log formatter and add it to the log handler
    formatter = NewRelicContextFormatter()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
else:
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.StreamHandler()]
    )
    logger.info('logger for development environment was setup')
