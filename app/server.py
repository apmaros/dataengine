from dash import dash
from flask import Flask

app = Flask(__name__)

dash_app = dash.Dash(
        __name__,
        server=app,
        routes_pathname_prefix='/dash/',
        assets_folder='static'
    )
