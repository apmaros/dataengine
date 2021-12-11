import threading

from common.log import logger
from config import AUTH0_CLIENT_ID, AUTO0_CLIENT_SECRET, AUTH0_API_BASE_URL, AUTH0_ACCESS_TOKEN_URL, \
    AUTH0_AUTHORIZE_URL, AUTH0_CLIENT_KWARGS
from context import Context
from dataengine import app
from authlib.integrations.flask_client import OAuth


def start_app():
    logger.info("Starting Data Engine app")

    oauth = OAuth(app)
    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTO0_CLIENT_SECRET,
        api_base_url=AUTH0_API_BASE_URL,
        access_token_url=AUTH0_ACCESS_TOKEN_URL,
        authorize_url=AUTH0_AUTHORIZE_URL,
        client_kwargs={
            'scope': AUTH0_CLIENT_KWARGS,
        },
    )

    Context.set_context(app, auth0)

    threading.Thread(target=app.run).start()
    logger.info("Started Data Engine app")


if __name__ == '__main__':
    start_app()
