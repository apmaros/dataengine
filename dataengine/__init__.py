from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from dataengine.config import SERVER_SECRET_KEY, SERVER_SESSION_TYPE

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app)

app.secret_key = SERVER_SECRET_KEY
app.config['SESSION_TYPE'] = SERVER_SESSION_TYPE


import dataengine.routes.core
