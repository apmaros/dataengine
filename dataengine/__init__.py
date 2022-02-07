import os
import pathlib

from authlib.integrations.flask_client import OAuth
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from dataengine.config import (
    AUTH0_CLIENT_ID,
    AUTO0_CLIENT_SECRET,
    AUTH0_API_BASE_URL,
    AUTH0_ACCESS_TOKEN_URL,
    AUTH0_AUTHORIZE_URL,
    AUTH0_CLIENT_KWARGS
)
from dataengine.config import SERVER_SECRET_KEY, SERVER_SESSION_TYPE, SESSION_COOKIE_NAME
from dataengine.context import Context
from dataengine.db.postgres.config import DbConfig
from dataengine.db.postgres.sesion import get_session
from dataengine.server.util import format_datetime, split_paragraphs, format_label_datetime, or_zero

SERVER_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(), "server")
TEMPLATE_FOLDER_PATH = os.path.join(SERVER_PATH, "templates")
STATIC_FOLDER_PATH = os.path.join(SERVER_PATH, "static")


def create_app():
    """
    Create and configure the APP by:
        - set configuration
        - add template filters for view
        - set routes
        - set OAuth
        - Set global context
    :return: instance of the APP ready to run
    """
    flask_app = Flask(__name__, template_folder=TEMPLATE_FOLDER_PATH)
    flask_app.static_folder = STATIC_FOLDER_PATH

    flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)

    # Configure
    flask_app.config['SECRET_KEY'] = SERVER_SECRET_KEY
    flask_app.config['SESSION_TYPE'] = SERVER_SESSION_TYPE
    flask_app.config['SESSION_COOKIE_NAME'] = SESSION_COOKIE_NAME

    # Template filters
    flask_app.jinja_env.filters['format_datetime'] = format_datetime
    flask_app.jinja_env.filters['split_paragraphs'] = split_paragraphs
    flask_app.jinja_env.filters['format_label_datetime'] = format_label_datetime
    flask_app.jinja_env.filters['or_zero'] = or_zero

    # Register Routes
    from server.routes.core import core_bp
    flask_app.register_blueprint(core_bp)

    from server.routes.auth import auth_bp
    flask_app.register_blueprint(auth_bp)

    from server.routes.monzo import monzo_bp
    flask_app.register_blueprint(monzo_bp)

    from server.routes.physio import physio_bp
    flask_app.register_blueprint(physio_bp)

    from server.routes.event import event_bp
    flask_app.register_blueprint(event_bp)

    from server.routes.note import note_bp
    flask_app.register_blueprint(note_bp)

    from server.routes.admin import admin_bp
    flask_app.register_blueprint(admin_bp)

    from server.routes.user import user_bp
    flask_app.register_blueprint(user_bp)

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
    db_session = get_session(DbConfig())

    Context.set_context(flask_app, auth0, db_session)

    return flask_app


app = create_app()
