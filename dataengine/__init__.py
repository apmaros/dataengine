import os
import pathlib

from authlib.integrations.flask_client import OAuth
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from config import (
    AUTH0_CLIENT_ID,
    AUTO0_CLIENT_SECRET,
    AUTH0_API_BASE_URL,
    AUTH0_ACCESS_TOKEN_URL,
    AUTH0_AUTHORIZE_URL,
    AUTH0_CLIENT_KWARGS
)
from context import Context
from dataengine.config import SERVER_SECRET_KEY, SERVER_SESSION_TYPE, SESSION_COOKIE_NAME

SERVER_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(), "server")
TEMPLATE_FOLDER_PATH = os.path.join(SERVER_PATH, "templates")
STATIC_FOLDER_PATH = os.path.join(SERVER_PATH, "static")


def create_app():
    flask_app = Flask(__name__, template_folder=TEMPLATE_FOLDER_PATH)
    flask_app.static_folder = STATIC_FOLDER_PATH

    flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)

    # Configure
    flask_app.config['SECRET_KEY'] = SERVER_SECRET_KEY
    flask_app.config['SESSION_TYPE'] = SERVER_SESSION_TYPE
    flask_app.config['SESSION_COOKIE_NAME'] = SESSION_COOKIE_NAME

    # Register Routes
    from server.routes.core import core_bp
    flask_app.register_blueprint(core_bp)

    from server.routes.auth import auth_bp
    flask_app.register_blueprint(auth_bp)

    from server.routes.monzo import monzo_bp
    flask_app.register_blueprint(monzo_bp)

    from server.routes.physio import physio_bp
    flask_app.register_blueprint(physio_bp)

    # Setup OAuth
    oauth = OAuth(flask_app)
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

    Context.set_context(flask_app, auth0)

    return flask_app


app = create_app()
