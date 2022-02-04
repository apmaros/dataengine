import logging
import os

from newrelic.agent import NewRelicContextFormatter

from dataengine.common.env import is_dev

logger = logging.getLogger()

if not is_dev():
    handler = logging.StreamHandler()
    # Instantiate the log formatter and add it to the log handler
    formatter = NewRelicContextFormatter()
    handler.setFormatter(formatter)
    # use only newrelic logging handler
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.info("Logger for prod environment was setup")
else:
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.StreamHandler()]
    )
    logger.info('Logger for development environment was setup')
