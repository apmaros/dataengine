from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from dataengine.config import SERVER_SECRET_KEY, SERVER_SESSION_TYPE


def create_app():
    flask_app = Flask(__name__)

    flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)

    flask_app.secret_key = SERVER_SECRET_KEY
    flask_app.config['SESSION_TYPE'] = SERVER_SESSION_TYPE

    from routes.auth import auth_bp
    flask_app.register_blueprint(auth_bp)

    from dataengine.routes.core import core_bp
    flask_app.register_blueprint(core_bp)

    return flask_app


app = create_app()
