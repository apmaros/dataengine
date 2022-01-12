from dataengine import app
from dataengine.common.log import logger


def start_app():
    logger.info("Starting Data Engine app")
    app.run()
    logger.info("Started Data Engine app")


if __name__ == '__main__':
    start_app()
