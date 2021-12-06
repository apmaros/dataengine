from common.log import logger
from dataengine import app


def start_app():
    logger.info("Starting Data Engine app")
    app.run()


if __name__ == '__main__':
    start_app()
