import os

from dash import dash
from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ.get("SERVER_SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'

dash_app = dash.Dash(
        __name__,
        server=app,
        routes_pathname_prefix='/dash/',
        assets_folder='static'
    )
