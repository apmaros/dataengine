from dash import dash
from flask import Flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Flask(__name__)

dash_app = dash.Dash(
        __name__,
        server=app,
        external_stylesheets=external_stylesheets,
        routes_pathname_prefix='/dash/'
    )
