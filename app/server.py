import os
from logging.config import dictConfig

from dash import dash
from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ.get("SERVER_SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


dash_app = dash.Dash(
        __name__,
        server=app,
        routes_pathname_prefix='/dash/',
        assets_folder='static'
    )
