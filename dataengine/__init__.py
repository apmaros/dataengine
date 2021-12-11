from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from dataengine.config import SERVER_SECRET_KEY, SERVER_SESSION_TYPE
from authlib.integrations.flask_client import OAuth
from config import AUTH0_CLIENT_ID, AUTO0_CLIENT_SECRET, AUTH0_API_BASE_URL, AUTH0_ACCESS_TOKEN_URL, \
    AUTH0_AUTHORIZE_URL, AUTH0_CLIENT_KWARGS
from context import Context


def create_app():
    flask_app = Flask(__name__)

    flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)

    flask_app.secret_key = SERVER_SECRET_KEY
    flask_app.config['SESSION_TYPE'] = SERVER_SESSION_TYPE

    # register routes blueprints
    from dataengine.routes.core import core_bp
    flask_app.register_blueprint(core_bp)

    from dataengine.routes.auth import auth_bp
    flask_app.register_blueprint(auth_bp)


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
