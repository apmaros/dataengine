import threading

from common.log import logger
from dataengine import app


def start_app():
    logger.info("Starting Data Engine app")
    threading.Thread(target=app.run).start()
    logger.info("Started Data Engine app")


if __name__ == '__main__':
    start_app()
